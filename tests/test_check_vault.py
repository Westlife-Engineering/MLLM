"""Temporary-vault positive/negative tests; no production inputs are modified."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import fitz

SPEC = importlib.util.spec_from_file_location("check_vault", Path(__file__).resolve().parents[1] / "scripts/check_vault.py")
vault = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(vault)


class VaultTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.rows, self.raw = [], []
        self.write("AGENTS.md", "# Rules\nRead-only fixture.\n")
        self.write("wiki/index.md", "# Index\n")

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def add_raw(self, relative, data=b"original"):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        row = {"old_path": relative.removeprefix("raw/"), "new_path": relative,
               "sha256": hashlib.sha256(data).hexdigest(), "size": len(data), "kind": "fixture"}
        self.raw.append(row)
        return {"path": relative, "sha256": row["sha256"], "url": None, "version": "v1"}

    def pdf_bytes(self, pages=2):
        with fitz.open() as doc:
            for _ in range(pages):
                doc.new_page()
            return doc.tobytes()

    def source(self, typ="paper", page=True, unread=False):
        sid = f"S{len(self.rows) + 1:03}"
        direction = "vision/encoders" if typ in {"paper", "source"} else None
        branch = {"paper": "papers/vision/encoders", "survey": "surveys", "lecture": "lectures", "source": "sources/vision/encoders"}[typ]
        raw_path = f"raw/{branch}/{sid}.pdf" if typ != "source" else f"raw/web/{sid}/official.html"
        data = b"<html>Official source</html>" if typ == "source" else self.pdf_bytes()
        row = {"source_id": sid, "slug": sid, "type": typ, "title": "Fixture " + sid,
               "identity_key": "identity:" + sid, "primary_direction": direction,
               "raw_path": raw_path, "wiki_path": f"wiki/{branch}/{sid}.md",
               "raw_files": [self.add_raw(raw_path, data)], "legacy_inputs": [],
               "reading_status": "unread" if unread else "read",
               "ingest_status": "pending" if unread else "complete", "integrated_topics": []}
        self.rows.append(row)
        if page:
            self.source_page(row)
        return row

    def source_page(self, row):
        raw_links = "\n".join(f'  - "[[{r["path"]}]]"' for r in row["raw_files"])
        text = (f'---\ntype: {row["type"]}\ncreated: 2026-10-31\nupdated: 2026-10-31\n'
                f'source_id: {row["source_id"]}\nreading_status: {row["reading_status"]}\n'
                f'ingest_status: {row["ingest_status"]}\nprimary_direction: {row["primary_direction"] or "null"}\n'
                f'sources:\n{raw_links}\n---\n# Source\nActual reading scope: main text.\n')
        text += "\n".join(r["sha256"] for r in row["raw_files"]) + "\n"
        self.write(row["wiki_path"], text)
        index = self.root / "wiki/index.md"
        index.write_text(index.read_text(encoding="utf-8") + f'[[{row["wiki_path"]}|Fixture summary]]\n', encoding="utf-8")

    def run_check(self, allow=False, manifest_extra=None):
        self.write("maintenance/source-registry.json", json.dumps({"schema_version": 1, "sources": self.rows}))
        manifest = {"schema_version": 1, "files": self.raw}
        manifest.update(manifest_extra or {})
        self.write("maintenance/migrations/fixture.json", json.dumps(manifest))
        return vault.Checker(self.root, allow).run()

    def assertPass(self, report):
        self.assertTrue(report["passed"], report["errors"])

    def assertCheck(self, report, code):
        self.assertIn(code, [r["check"] for r in report["errors"]], report)

    def test_valid_paper_and_read_only(self):
        self.source()
        self.run_check()
        before = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertPass(vault.Checker(self.root).run())
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_original_byte_change_never_suppressed(self):
        row = self.source()
        path = self.root / row["raw_path"]
        path.write_bytes(path.read_bytes() + b"changed")
        report = self.run_check(True)
        self.assertCheck(report, "raw_hash")
        self.assertCheck(report, "raw_size")

    def test_duplicate_id_and_identity(self):
        first, second = self.source(), self.source()
        second["source_id"] = first["source_id"]
        second["identity_key"] = first["identity_key"]
        report = self.run_check()
        self.assertCheck(report, "duplicate_source_id")
        self.assertCheck(report, "duplicate_identity_key")

    def test_arxiv_versions_do_not_create_two_identities(self):
        first, second = self.source(), self.source()
        first["identity_key"] = "arxiv:2401.12345v1"
        second["identity_key"] = "arxiv:2401.12345v2"
        self.assertCheck(self.run_check(), "duplicate_identity_key")

    def test_multiple_versions_share_one_source(self):
        row = self.source(page=False)
        row["raw_files"].append(self.add_raw("raw/papers/vision/encoders/S001-v2.pdf", self.pdf_bytes(3)))
        self.source_page(row)
        self.assertPass(self.run_check())

    def test_lecture_survey_and_official_source(self):
        for typ in ("lecture", "survey", "source"):
            self.source(typ)
        self.assertPass(self.run_check())

    def test_unread_original_is_valid_pending_work(self):
        self.source(page=False, unread=True)
        report = self.run_check(True)
        self.assertPass(report)
        self.assertIn("source_page_missing", [r["check"] for r in report["warnings"]])
        self.assertCheck(self.run_check(False), "source_page_missing")

    def test_unacquired_planned_path_is_not_missing_raw(self):
        row = self.source(page=False, unread=True)
        (self.root / row["raw_path"]).unlink()
        # No physical Raw remains, so remove fixture-created empty source folders.
        for p in reversed(list((self.root / "raw").rglob("*"))):
            if p.is_dir():
                p.rmdir()
        row["raw_files"], self.raw = [], []
        self.assertPass(self.run_check())

    def test_pdf_out_of_range_and_malformed_pages(self):
        row = self.source()
        for page in ("0", "3", "banana"):
            self.write("AGENTS.md", f'[[{row["raw_path"]}#page={page}|Evidence]]\n')
            self.assertCheck(self.run_check(True), "pdf_page")

    def test_valid_pdf_heading_and_block_anchor(self):
        row = self.source()
        with (self.root / row["wiki_path"]).open("a", encoding="utf-8") as stream:
            stream.write("## Mechanism and limits\nEvidence. ^evidence\n")
        self.write("AGENTS.md", f'[[{row["raw_path"]}#page=2]]\n[[{row["wiki_path"]}#Mechanism and limits]]\n[[{row["wiki_path"]}#^evidence]]\n')
        self.assertPass(self.run_check())

    def test_block_anchor_in_fenced_code_is_not_a_target(self):
        row = self.source()
        with (self.root / row["wiki_path"]).open("a", encoding="utf-8") as stream:
            stream.write("```markdown\nexample ^fake\n```\n")
        self.write("AGENTS.md", f'[[{row["wiki_path"]}#^fake]]\n')
        self.assertCheck(self.run_check(True), "link_anchor")

    def test_block_anchor_in_html_comment_is_not_a_target(self):
        row = self.source()
        with (self.root / row["wiki_path"]).open("a", encoding="utf-8") as stream:
            stream.write("<!--\nexample ^fake\n-->\n")
        self.write("AGENTS.md", f'[[{row["wiki_path"]}#^fake]]\n')
        self.assertCheck(self.run_check(True), "link_anchor")

    def test_markdown_image_and_editable_link(self):
        self.source()
        self.write("wiki/assets/diagram/figure.excalidraw", "{}")
        self.write("wiki/assets/diagram/figure.png", "fixture asset")
        self.write("AGENTS.md", "[Editable](wiki/assets/diagram/figure.excalidraw)\n![Preview](<wiki/assets/diagram/figure.png>)\n")
        self.assertPass(self.run_check())
        (self.root / "wiki/assets/diagram/figure.excalidraw").unlink()
        self.assertCheck(self.run_check(True), "link_target")

    def test_table_wikilink_alias_requires_escape(self):
        row = self.source()
        self.write("AGENTS.md", f'| Link |\n| --- |\n| [[{row["wiki_path"]}\\|Good]] |\n')
        self.assertPass(self.run_check())
        self.write("AGENTS.md", f'| Link |\n| --- |\n| [[{row["wiki_path"]}|Bad]] |\n')
        self.assertCheck(self.run_check(True), "table_alias_escape")

    def test_code_examples_are_not_actual_links(self):
        self.source()
        self.write("AGENTS.md", '# Rules\n`[[wiki/missing]]`\n```md\n[[missing]]\n[example](missing.pdf)\n```\n')
        self.assertPass(self.run_check())

    def test_tex_figw_and_direct_dependencies(self):
        self.source()
        self.add_raw("raw/notes/package/images/a.png")
        self.add_raw("raw/notes/package/images/b.png")
        tex = r"\newcommand{\figw}[2]{\includegraphics[width=#1\linewidth]{images/#2}}" + "\n"
        tex += r"\figw{0.5}{a.png}" + "\n" + r"\includegraphics{images/b.png}"
        self.add_raw("raw/notes/package/note.tex", tex.encode())
        report = self.run_check()
        self.assertPass(report)
        self.assertEqual(2, report["counts"]["tex_dependencies"])
        (self.root / "raw/notes/package/images/a.png").unlink()
        self.assertCheck(self.run_check(True), "tex_dependency")

    def test_tex_input_and_optional_graphicspath(self):
        self.source()
        self.add_raw("raw/notes/package/images/a.png")
        self.add_raw("raw/notes/package/chapter.tex", b"Text")
        tex = r"\graphicspath{{images/}}\includegraphics[width=1cm]{a}\input{chapter}"
        self.add_raw("raw/notes/package/note.tex", tex.encode())
        self.assertPass(self.run_check())

    def test_raw_markdown_only_registered_historical_links_reported(self):
        self.source()
        raw = self.add_raw("raw/notes/old.md", b"[Already missing](old.pdf)")
        extra = {"markdown_dependency_audit": {"local_links": [
            {"source": "notes/old.md", "line": 1, "argument": "old.pdf", "status": "missing"}]}}
        report = self.run_check(manifest_extra=extra)
        self.assertPass(report)
        self.assertEqual(1, len(report["documented_historical_links"]))

    def test_unregistered_raw_is_error(self):
        self.source()
        self.write("raw/unregistered.txt", "Untracked original")
        self.assertCheck(self.run_check(True), "raw_inventory")

    def test_registry_frontmatter_mismatch_is_error(self):
        row = self.source()
        path = self.root / row["wiki_path"]
        path.write_text(path.read_text(encoding="utf-8").replace("reading_status: read", "reading_status: partial"), encoding="utf-8")
        self.assertCheck(self.run_check(True), "registry_page_mismatch")

    def test_registered_source_cannot_hide_as_topic(self):
        row = self.source()
        path = self.root / row["wiki_path"]
        path.write_text(path.read_text(encoding="utf-8").replace("type: paper", "type: topic"), encoding="utf-8")
        self.assertCheck(self.run_check(True), "registry_page_mismatch")

    def test_source_frontmatter_requires_main_original(self):
        row = self.source()
        path = self.root / row["wiki_path"]
        text = path.read_text(encoding="utf-8")
        text = text.replace(f'sources:\n  - "[[{row["raw_path"]}]]"', "sources: []")
        path.write_text(text, encoding="utf-8")
        self.assertCheck(self.run_check(True), "source_page_raw")

    def test_declared_theme_links_must_be_bidirectional(self):
        row = self.source()
        row["integrated_topics"] = ["wiki/vision/Overview.md"]
        self.write("wiki/vision/Overview.md", '---\ntype: topic\ncreated: 2026-10-31\nupdated: 2026-10-31\nsources: []\n---\n# Vision\nMeaningful synthesis.\n')
        self.assertCheck(self.run_check(True), "theme_backlink")
        with (self.root / row["wiki_path"]).open("a", encoding="utf-8") as f:
            f.write("[[wiki/vision/Overview]]\n")
        with (self.root / "wiki/vision/Overview.md").open("a", encoding="utf-8") as f:
            f.write(f'[[{row["wiki_path"]}]]\n')
        self.assertPass(self.run_check(True))

    def test_complete_page_absence_not_suppressed(self):
        self.source(page=False)
        self.assertCheck(self.run_check(True), "source_page_missing")

    def test_bad_anchor_and_outside_vault_link(self):
        row = self.source()
        self.write("AGENTS.md", f'[[{row["wiki_path"]}#Missing heading]]\n[Outside](../external.md)\n')
        report = self.run_check(True)
        self.assertCheck(report, "link_anchor")
        self.assertCheck(report, "linked_file")


if __name__ == "__main__":
    unittest.main()
