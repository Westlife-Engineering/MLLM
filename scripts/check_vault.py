"""Read-only vault integrity and Markdown checks (not scholarly or UI validation).

Run ``python scripts/check_vault.py`` from any directory. ``--root`` selects a
fixture/other vault; ``--allow-incomplete`` permits only pending source pages and
index coverage to be absent. Uses the already installed PyYAML and PyMuPDF.
No network, Git operations, compilation, or file writes are performed.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

import fitz
import yaml

SOURCE_TYPES = {"paper", "survey", "lecture", "source"}
READING = {"unread", "partial", "read"}
INGEST = {"pending", "reading", "integrating", "reviewing", "complete", "blocked"}
WIKI = re.compile(r"!?\[\[([^\]\n]+)\]\]")


def masked_markdown(text: str, inline: bool = True) -> str:
    """Hide code examples/comments while retaining line positions."""
    lines, fence = [], None
    for line in text.splitlines(keepends=True):
        mark = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence:
            if mark and mark[1][0] == fence[0] and len(mark[1]) >= len(fence):
                fence = None
            lines.append("\n" if line.endswith("\n") else "")
        elif mark:
            fence = mark[1]
            lines.append("\n" if line.endswith("\n") else "")
        else:
            lines.append(line)
    text = "".join(lines)
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m[0].count("\n"), text, flags=re.S)
    if inline:
        text = re.sub(r"(`+)([^`\n]|(?!\1)`)*?\1", "", text)
    return text


def group(text: str, pos: int, opener: str = "{", closer: str = "}"):
    """Return a balanced TeX/Markdown group and the next position."""
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if pos >= len(text) or text[pos] != opener:
        return None, pos
    start, depth = pos + 1, 1
    pos += 1
    while pos < len(text):
        if text[pos] == "\\":
            pos += 2
            continue
        depth += (text[pos] == opener) - (text[pos] == closer)
        if not depth:
            return text[start:pos], pos + 1
        pos += 1
    return None, pos


def markdown_links(text: str):
    """Yield (target, line, is_wikilink, original) including local images."""
    clean = masked_markdown(text)
    for match in WIKI.finditer(clean):
        target = match[1].replace("\\|", "|").split("|", 1)[0].strip()
        yield target, clean[:match.start()].count("\n") + 1, True, match[1]
    ordinary = WIKI.sub("", clean)
    for match in re.finditer(r"!?\[(?:\\.|[^\]\n])*\]\(", ordinary):
        value, end = group(ordinary, match.end() - 1, "(", ")")
        if value is None:
            continue
        value = value.strip()
        if value.startswith("<") and ">" in value:
            value = value[1:value.index(">")]
        else:
            value = re.sub(r'\s+[\"\'][^\n]*[\"\']\s*$', "", value)
        yield value, ordinary[:match.start()].count("\n") + 1, False, value
    # Reference-style destinations are checked at their definitions.
    for match in re.finditer(r"^\s{0,3}\[[^\]\n]+\]:\s*(<[^>]+>|\S+)", ordinary, re.M):
        yield match[1].strip("<>"), ordinary[:match.start()].count("\n") + 1, False, match[1]


def heading_forms(text: str) -> set[str]:
    forms, seen = set(), Counter()
    for heading in re.findall(r"^#{1,6}[ \t]+(.+)$", masked_markdown(text, False), re.M):
        heading = re.sub(r"\s+#+\s*$", "", heading).strip()
        plain = re.sub(r"[*_`]", "", heading)
        slug = re.sub(r"[^\w\- ]", "", plain.lower()).replace(" ", "-")
        forms.update((heading, plain, slug if not seen[slug] else f"{slug}-{seen[slug]}"))
        seen[slug] += 1
    return forms


def identity_key(value: str) -> str:
    """arXiv versions share one work identity; DOI identifiers ignore case."""
    value = value.strip()
    if value.lower().startswith("arxiv:"):
        return re.sub(r"v\d+$", "", value.lower())
    if value.lower().startswith("doi:"):
        return value.lower()
    return value


def tex_dependencies(text: str):
    """Static local resources; expand the actual figw definition, not a hardcoded path."""
    text = re.sub(r"(?<!\\)%[^\n]*", "", text)
    macros = {}
    # Remove macro bodies from the direct scan; #n paths are templates, not files.
    for match in reversed(list(re.finditer(r"\\(?:newcommand|renewcommand|providecommand)\*?", text))):
        name, pos = group(text, match.end())
        if name is None:
            continue
        while text[pos:pos + 1] == "[":
            _, pos = group(text, pos, "[", "]")
        body, end = group(text, pos)
        if body is not None:
            macros[name.lstrip("\\")] = body
            text = text[:match.start()] + "\n" * text[match.start():end].count("\n") + text[end:]
    graphics_dirs = [""]
    for match in re.finditer(r"\\graphicspath", text):
        value, _ = group(text, match.end())
        if value:
            graphics_dirs += re.findall(r"\{([^{}]*)\}", value)
    commands = {"includegraphics", "includepdf", "input", "include", "subfile",
                "bibliography", "addbibresource", "lstinputlisting", "verbatiminput",
                "includesvg", "includeinkscape", "attachfile", "inputminted", "figw"}
    dependencies = []
    for match in re.finditer(r"\\([A-Za-z]+)\*?", text):
        command, pos = match[1], match.end()
        if command not in commands:
            continue
        while pos < len(text) and text[pos].isspace():
            pos += 1
        while text[pos:pos + 1] == "[":
            _, pos = group(text, pos, "[", "]")
            while pos < len(text) and text[pos].isspace():
                pos += 1
        argument, pos = group(text, pos)
        if command in {"figw", "inputminted"}:
            second, pos = group(text, pos)
            if command == "inputminted":
                argument = second
            else:
                template = macros.get("figw", "")
                template = template.replace("#1", argument or "").replace("#2", second or "")
                inner = re.search(r"\\includegraphics(?:\[[^]]*\])?\s*\{([^{}]+)\}", template)
                argument = inner[1] if inner else None
        if argument is None:
            dependencies.append((command, None, [], text[:match.start()].count("\n") + 1))
        else:
            for value in argument.split(",") if command == "bibliography" else [argument]:
                dirs = graphics_dirs if command in {"includegraphics", "figw"} else [""]
                dependencies.append((command, value, dirs, text[:match.start()].count("\n") + 1))
    return dependencies


class Checker:
    def __init__(self, root: Path, allow_incomplete: bool = False):
        self.root = root.resolve()
        self.allow = allow_incomplete
        self.errors, self.warnings, self.historical = [], [], []
        self.texts, self.hashes, self.pages = {}, {}, {}
        self.links, self.frontmatter, self.sources = {}, {}, []
        self.raw_expected, self.old_paths = {}, {}
        self.manifests = []
        self.counts = Counter()

    def issue(self, check, file, detail, *, pending=False, line=None):
        record = {"check": check, "file": str(file), "detail": str(detail)}
        if line is not None:
            record["line"] = line
        (self.warnings if pending and self.allow else self.errors).append(record)

    def path(self, relative: str) -> Path:
        path = (self.root / relative).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError(f"path outside vault: {relative}")
        return path

    def rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def text(self, path: Path) -> str:
        if path not in self.texts:
            self.texts[path] = path.read_text(encoding="utf-8-sig")
        return self.texts[path]

    def digest(self, path: Path) -> str:
        if path not in self.hashes:
            with path.open("rb") as stream:
                self.hashes[path] = hashlib.file_digest(stream, "sha256").hexdigest()
        return self.hashes[path]

    def pdf_pages(self, path: Path) -> int:
        if path not in self.pages:
            with fitz.open(path) as pdf:
                self.pages[path] = len(pdf)
        return self.pages[path]

    def verify_raw(self, row, origin, path_key="new_path"):
        relative = row.get(path_key, "")
        try:
            path = self.path(relative)
            if not relative.startswith("raw/"):
                raise ValueError("registered raw path must begin raw/")
            if not path.is_file():
                raise ValueError("registered raw file missing")
            expected = row.get("sha256", "")
            if not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
                self.issue("raw_hash_format", relative, origin)
            elif self.digest(path) != expected.lower():
                self.issue("raw_hash", relative, f"SHA-256 differs from {origin}")
            if "size" in row and path.stat().st_size != row["size"]:
                self.issue("raw_size", relative, f"size differs from {origin}")
            if relative in self.raw_expected and self.raw_expected[relative].lower() != expected.lower():
                self.issue("raw_registration_conflict", relative, origin)
            self.raw_expected[relative] = expected
        except (OSError, ValueError) as exc:
            self.raw_expected[relative] = row.get("sha256", "")
            self.issue("raw_file", relative, exc)

    def load_manifests(self):
        paths = sorted((self.root / "maintenance/migrations").glob("*.json"))
        if not paths:
            self.issue("migration_manifest", "maintenance/migrations", "no manifest")
        for path in paths:
            data = json.loads(self.text(path))
            self.manifests.append(data)
            if data.get("schema_version") != 1:
                self.issue("manifest_schema", self.rel(path), "expected schema_version 1")
            official = data.get("imported_official_sources", {})
            official = official.get("files", []) if isinstance(official, dict) else official
            original = data.get("files", [])
            records = original + data.get("imported_reference", []) + official
            summary = data.get("summary", {})
            for field, actual in (("original_file_count", len(original)),
                                  ("original_total_bytes", sum(r.get("size", 0) for r in original)),
                                  ("imported_reference_file_count", len(data.get("imported_reference", []))),
                                  ("new_official_raw_file_count", len(official))):
                if field in summary and summary[field] != actual:
                    self.issue("manifest_total", self.rel(path), field)
            seen = set()
            for row in records:
                if row.get("new_path") in seen:
                    self.issue("manifest_duplicate_path", self.rel(path), row.get("new_path"))
                seen.add(row.get("new_path"))
                if "size" not in row:
                    self.issue("manifest_size", self.rel(path), row.get("new_path"))
                self.verify_raw(row, self.rel(path))
                if row.get("old_path"):
                    self.old_paths[row["old_path"]] = row
            self.counts["manifest_raw_records"] += len(records)
            for row in data.get("markdown_dependency_audit", {}).get("local_links", []):
                if row.get("status") == "missing":
                    old = self.old_paths.get(row.get("source"))
                    if not old:
                        self.issue("historical_registration", self.rel(path), row)
                    else:
                        self.historical.append({"file": old["new_path"], "line": row.get("line"),
                                                "target": row.get("argument"), "kind": "frozen_raw_missing_link"})

    def registry(self):
        file = "maintenance/source-registry.json"
        data = json.loads(self.text(self.path(file)))
        if data.get("schema_version") != 1 or not isinstance(data.get("sources"), list):
            self.issue("registry_schema", file, "expected v1 sources array")
            return
        self.sources = data["sources"]
        seen = {key: set() for key in ("source_id", "identity_key", "wiki_path", "raw_path")}
        for row in self.sources:
            sid = row.get("source_id", "")
            for key in ("source_id", "slug", "type", "title", "primary_direction", "identity_key",
                        "raw_path", "wiki_path", "raw_files", "legacy_inputs", "reading_status",
                        "ingest_status", "integrated_topics"):
                if key not in row:
                    self.issue("registry_field", file, f"{sid}: missing {key}")
            for key, values in seen.items():
                value = row.get(key)
                if key == "identity_key" and isinstance(value, str):
                    value = identity_key(value)
                if not value or value in values:
                    self.issue(f"duplicate_{key}" if value else "registry_identity", file, f"{sid}: {key}={value}")
                values.add(value)
            if not re.fullmatch(r"S\d+", sid):
                self.issue("source_id", file, sid)
            typ, direction = row.get("type"), row.get("primary_direction")
            if typ not in SOURCE_TYPES:
                self.issue("source_type", file, f"{sid}: {typ}")
                continue
            reading, status = row.get("reading_status"), row.get("ingest_status")
            if reading not in READING or status not in INGEST:
                self.issue("source_status", file, f"{sid}: {reading}/{status}")
            if status == "complete" and reading != "read":
                self.issue("source_status", file, f"{sid}: complete requires read")
            page = self.path(row["wiki_path"])
            prefix = {"paper": "papers", "source": "sources", "survey": "surveys", "lecture": "lectures"}[typ]
            expected_parent = f"wiki/{prefix}"
            if typ in {"paper", "source"}:
                if not isinstance(direction, str) or not re.fullmatch(r"[a-z0-9-]+/[a-z0-9-]+", direction):
                    self.issue("primary_direction", file, f"{sid}: {direction}")
                expected_parent += "/" + str(direction)
            if self.rel(page.parent) != expected_parent or page.suffix != ".md":
                self.issue("source_directory", row["wiki_path"], expected_parent)
            raw_files = row.get("raw_files", [])
            if not raw_files:
                if (reading, status) != ("unread", "pending") or page.exists():
                    self.issue("unacquired_source", file, f"{sid}: no raw files requires unread/pending and no page")
                continue
            if row["raw_path"] not in {r.get("path") for r in raw_files}:
                self.issue("main_raw", file, f"{sid}: raw_path absent from raw_files")
            for raw in raw_files:
                for field in ("path", "sha256", "url", "version"):
                    if field not in raw:
                        self.issue("raw_registry_field", file, f"{sid}: missing {field}")
                self.verify_raw(raw, f"registry {sid}", "path")
            raw_main = self.path(row["raw_path"])
            if typ in {"paper", "survey"} and raw_main.suffix.lower() == ".pdf":
                expected = "raw/" + self.rel(page)[5:-3] + ".pdf"
                if row["raw_path"] != expected:
                    self.issue("primary_mirror", row["wiki_path"], row["raw_path"])
            elif typ == "lecture" and not row["raw_path"].startswith("raw/lectures/"):
                self.issue("lecture_directory", file, sid)
            elif typ == "source" and not row["raw_path"].startswith(("raw/web/", "raw/code/")):
                self.issue("official_source_directory", file, sid)
            elif typ in {"paper", "survey"} and not row["raw_path"].startswith("raw/web/"):
                self.issue("main_raw_type", file, sid)
            if raw_main.is_file() and raw_main.suffix.lower() == ".pdf":
                try:
                    pages = self.pdf_pages(raw_main)
                    if "pages" in row and row["pages"] != pages:
                        self.issue("registry_pdf_pages", file, f"{sid}: {row['pages']} != {pages}")
                except (OSError, RuntimeError, ValueError) as exc:
                    self.issue("pdf_read", row["raw_path"], exc)
            for legacy in row.get("legacy_inputs", []):
                if not legacy.startswith("raw/notes/") or not self.path(legacy).is_file():
                    self.issue("legacy_input", file, f"{sid}: {legacy}")
            if not page.is_file():
                self.issue("source_page_missing", row["wiki_path"], sid, pending=status != "complete")

    def resolve_link(self, target: str, source: Path, wiki: bool):
        target = re.sub(r"\\([()\[\] ])", r"\1", target)
        if re.match(r"^(?:https?|mailto|data|obsidian|plugin|codex|app):", target, re.I) or target.startswith("//"):
            return None, ""
        path, _, anchor = target.partition("#")
        path, anchor = unquote(path), unquote(anchor)
        if re.match(r"^[A-Za-z]:", path) or path.startswith("/"):
            candidate = Path(path).resolve()
        else:
            candidate = ((self.root if wiki else source.parent) / path).resolve() if path else source
        if wiki and not candidate.exists() and candidate.suffix.lower() not in {
            ".md", ".pdf", ".png", ".svg", ".jpg", ".jpeg", ".webp", ".html", ".json", ".excalidraw"
        }:
            candidate = Path(str(candidate) + ".md")
        if not candidate.is_relative_to(self.root):
            raise ValueError(f"outside vault: {target}")
        return candidate, anchor

    def markdown(self):
        files = [self.root / "AGENTS.md"]
        for tree in ("wiki", "workflows", "conversation-to-note", "maintenance", "组会"):
            files.extend(sorted((self.root / tree).rglob("*.md")))
        files = [p for p in files if p.is_file()]
        for path in files:
            text, relative = self.text(path), self.rel(path)
            self.links[path] = set()
            if not text.strip():
                self.issue("empty_page", relative, "empty Markdown")
            match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|$)", text, re.S)
            fm = {}
            if match:
                try:
                    fm = yaml.safe_load(match[1]) or {}
                    if not isinstance(fm, dict):
                        raise ValueError("frontmatter must be a mapping")
                except (yaml.YAMLError, ValueError) as exc:
                    self.issue("frontmatter_yaml", relative, exc)
                    fm = {}
            self.frontmatter[path] = fm
            if relative.startswith("wiki/") and not relative.startswith("wiki/assets/") and path.name not in {"index.md", "log.md"}:
                for key in ("type", "created", "updated", "sources"):
                    if key not in fm:
                        self.issue("frontmatter", relative, f"missing {key}")
                if not isinstance(fm.get("sources"), list):
                    self.issue("frontmatter_sources", relative, "sources must be a list")
                else:
                    for source in fm["sources"]:
                        if not isinstance(source, str):
                            self.issue("frontmatter_sources", relative, "source must be a string link/path")
                            continue
                        links = list(markdown_links(source))
                        target = links[0][0] if links else source
                        target = target.partition("#")[0]
                        if not target.startswith("raw/") or not self.path(target).is_file():
                            self.issue("frontmatter_sources", relative, f"not a reachable Raw source: {source}")
                for key in ("created", "updated"):
                    try:
                        date.fromisoformat(str(fm.get(key)))
                    except ValueError:
                        self.issue("frontmatter_date", relative, key)
                body = text[match.end():] if match else text
                if not re.sub(r"(?m)^\s*#+[^\n]*$", "", body).strip():
                    self.issue("empty_page", relative, "no substantive body")
            for target, line, wiki, original in markdown_links(text):
                self.counts["links_checked"] += 1
                if wiki and text.splitlines()[line - 1].lstrip().startswith("|") and re.search(r"(?<!\\)\|", original):
                    self.issue("table_alias_escape", relative, original, line=line)
                try:
                    dest, anchor = self.resolve_link(target, path, wiki)
                    if dest is None:
                        continue
                    self.links[path].add(dest)
                    if not dest.is_file():
                        # Only the log can refer to documented, verified historical migrations.
                        mapped = self.old_paths.get(target.partition("#")[0]) if relative == "wiki/log.md" else None
                        if mapped and self.path(mapped["new_path"]).is_file() and self.digest(self.path(mapped["new_path"])) == mapped["sha256"]:
                            self.historical.append({"file": relative, "target": target, "kind": "documented_migration"})
                        else:
                            self.issue("link_target", relative, target, line=line)
                        continue
                    if anchor and dest.suffix.lower() == ".md":
                        valid = bool(re.search(r"\^" + re.escape(anchor[1:]) + r"\s*$", masked_markdown(self.text(dest), False), re.M)) if anchor.startswith("^") else anchor in heading_forms(self.text(dest))
                        if not valid:
                            self.issue("link_anchor", relative, target, line=line)
                    if anchor and dest.suffix.lower() == ".pdf":
                        page = re.search(r"(?:^|&)page=([^&]*)(?:&|$)", anchor)
                        if page and (not page[1].isdigit() or not 1 <= int(page[1]) <= self.pdf_pages(dest)):
                            self.issue("pdf_page", relative, target, line=line)
                except (OSError, ValueError, RuntimeError) as exc:
                    self.issue("linked_file", relative, f"{target}: {exc}", line=line)
        self.counts["markdown_files"] = len(files)

    def source_pages_and_index(self):
        by_page = {self.path(r["wiki_path"]): r for r in self.sources}
        ids = Counter()
        for path, fm in self.frontmatter.items():
            if not self.rel(path).startswith("wiki/"):
                continue
            row = by_page.get(path)
            if row is None and fm.get("type") not in SOURCE_TYPES:
                continue
            ids[fm.get("source_id")] += 1
            if row is None:
                self.issue("unregistered_source_page", self.rel(path), fm.get("source_id"))
                continue
            for key in ("type", "source_id", "reading_status", "ingest_status"):
                if fm.get(key) != row.get(key):
                    self.issue("registry_page_mismatch", self.rel(path), key)
            if row["type"] in {"paper", "source"} and fm.get("primary_direction") != row["primary_direction"]:
                self.issue("registry_page_mismatch", self.rel(path), "primary_direction")
            text = self.text(path)
            linked_raw = set()
            for value in fm.get("sources", []) if isinstance(fm.get("sources"), list) else []:
                if isinstance(value, str):
                    parsed = list(markdown_links(value))
                    linked_raw.add((parsed[0][0] if parsed else value).partition("#")[0])
            if row["raw_path"] not in linked_raw:
                self.issue("source_page_raw", self.rel(path), "main original absent from sources")
            for raw in row.get("raw_files", []):
                if raw["sha256"].lower() not in text.lower():
                    self.issue("source_page_hash", self.rel(path), raw["path"])
            for topic in row.get("integrated_topics", []):
                target = self.path(topic if topic.endswith(".md") else topic + ".md")
                if not target.is_file() or target not in self.links.get(path, set()) or path not in self.links.get(target, set()):
                    self.issue("theme_backlink", self.rel(path), topic)
        for sid, count in ids.items():
            if not sid or count != 1:
                self.issue("duplicate_page_source_id", "wiki", f"{sid}: {count}")
        index = self.root / "wiki/index.md"
        if not index.is_file():
            self.issue("index_missing", "wiki/index.md", "index not created", pending=True)
        for path in self.frontmatter:
            relative = self.rel(path)
            if relative.startswith("wiki/") and not relative.startswith("wiki/assets/") and path.name not in {"index.md", "log.md"} and path not in self.links.get(index, set()):
                self.issue("index_coverage", relative, "not linked from wiki/index.md", pending=True)

    def tex(self):
        actual = []
        suffixes = {"input": [".tex"], "include": [".tex"], "subfile": [".tex"],
                    "bibliography": [".bib"], "addbibresource": [".bib"], "includesvg": [".svg"]}
        for path in sorted((self.root / "raw/notes").rglob("*.tex")):
            self.counts["tex_files"] += 1
            for command, argument, dirs, line in tex_dependencies(self.text(path)):
                self.counts["tex_dependencies"] += 1
                if argument is None or re.search(r"[#\\]", argument):
                    self.issue("tex_unresolved", self.rel(path), f"{command}: {argument}", line=line)
                    continue
                candidates = []
                for directory in dirs:
                    candidate = path.parent / directory / argument
                    candidates.append(candidate)
                    if not candidate.suffix:
                        candidates += [Path(str(candidate) + ext) for ext in suffixes.get(command, [".pdf", ".png", ".jpg", ".eps", ".svg"])]
                found = next((p.resolve() for p in candidates if p.is_file()), None)
                if found is None or not found.is_relative_to(self.root):
                    self.issue("tex_dependency", self.rel(path), f"{command}: {argument}", line=line)
                else:
                    actual.append((self.rel(path), self.rel(found)))
        registered = []
        for manifest in self.manifests:
            for doc in manifest.get("tex_dependency_audit", {}).get("documents", []):
                for dep in doc.get("dependencies", []):
                    registered.append((doc["new_source"], dep.get("resolved_new_path")))
        if registered and Counter(registered) != Counter(actual):
            self.issue("tex_audit_mismatch", "maintenance/migrations", "static dependencies differ from registered audit")

    def inventory(self):
        actual = {self.rel(p) for p in (self.root / "raw").rglob("*") if p.is_file()}
        expected = set(self.raw_expected)
        if actual != expected:
            self.issue("raw_inventory", "raw", json.dumps({"unregistered": sorted(actual - expected), "missing": sorted(expected - actual)}, ensure_ascii=False))
        self.counts["raw_files"] = len(actual)
        self.counts["raw_bytes"] = sum(self.path(p).stat().st_size for p in actual)
        for tree in ("raw", "wiki", "workflows", "maintenance", "conversation-to-note", "scripts", "tests"):
            for path in (self.root / tree).rglob("*"):
                if "__pycache__" in path.parts:
                    continue
                if path.is_symlink() or getattr(path.stat(), "st_file_attributes", 0) & 0x400:
                    self.issue("reparse_point", str(path), "link/reparse point not permitted")
                if path.is_dir() and not any(path.iterdir()):
                    self.issue("empty_directory", self.rel(path), "empty directory")
                if tree == "wiki" and self.rel(path).split("/").count("wiki") > 1:
                    self.issue("nested_wiki", self.rel(path), "nested wiki path")

    def run(self):
        for operation in (self.load_manifests, self.registry, self.markdown,
                          self.source_pages_and_index, self.tex, self.inventory):
            try:
                operation()
            except (OSError, ValueError, KeyError, TypeError) as exc:
                self.issue("check_failed", operation.__name__, exc)
        return {"scope": "Structural integrity only; no scholarly correctness, TeX compilation, remote resource completeness, or Obsidian UI validation.",
                "root": str(self.root), "allow_incomplete": self.allow,
                "counts": dict(self.counts), "registry_sources": len(self.sources),
                "registry_types": dict(Counter(r.get("type") for r in self.sources)),
                "pdfs_checked": len(self.pages), "errors": self.errors, "warnings": self.warnings,
                "documented_historical_links": self.historical, "passed": not self.errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    result = Checker(args.root, args.allow_incomplete).run()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
