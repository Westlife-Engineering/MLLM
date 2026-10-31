# 2026-10-31 初始化迁移记录

**状态：迁移完成，261 件原件字节及依赖已复核。** 本记录不代表已完成正式知识页、学术核读、重新编译或 Obsidian 验收。

本次用户已授权将原件保持字节不变迁入 `raw/` 并建立仅本地 Git。参考 Long-Horizon-Agents 的原件保护与迁移方式，但不沿用参考库的历史授权、目录词表或任务状态。Git 检查点由主协调者统一执行。主协调者先将 261 原件及 4 份基线治理文件提交为 `beb00884709059882482b9dc8d6059949608faef`，并逐件核对暂存 blob；迁移代理未执行提交。

## 完整性基线

- 原件 261 件，共 159,091,076 字节。PDF 45、TeX 31、PNG 171、Markdown 10、Excalidraw 4。
- 归档类别：综述 PDF 2、讲义 PDF 1、论文正文 PDF 7；既有笔记包 251 件（31 TeX、35 PDF、171 PNG、10 Markdown、4 Excalidraw）。笔记包的 35 PDF 包括 31 份阅读输出和 4 份图形导出。
- 全部原件已计算 SHA-256，并在写记录前再次逐项核对大小与哈希；261 个目标路径无大小写冲突，迁移前目标均不存在；未检测到原目录中的重解析点。
- 完整逐文件映射见同名 JSON 的 `files`，每项字段为 `old_path`、`new_path`、`sha256`、`size`、`kind`。路径统一为相对本库根目录的正斜杠路径，`size` 单位为字节，`sha256` 为小写十六进制。
- JSON 顶层 `schema_version: 1`、`date: 2026-10-31`、`status: migration_completed_byte_verified`；依赖审计和异常亦保存于该 JSON，不另造 Raw 说明文件。

## 已核对的迁移映射

| 旧路径 | 计划新路径 |
| --- | --- |
| `Efficient Multimodal Large Language Models A Survey.pdf` | `raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf` |
| `Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf` | `raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf` |
| `VLM-2.pdf` | `raw/lectures/VLM-2.pdf` |
| `多模态经典/2021-ICLR-ViT.pdf` | `raw/papers/vision/encoders/ViT.pdf` |
| `多模态经典/2021-ICML-CLIP.pdf` | `raw/papers/vision/alignment/CLIP.pdf` |
| `多模态经典/2022-NeurIPS-Flamingo.pdf` | `raw/papers/architecture/connectors/Flamingo.pdf` |
| `多模态经典/2022-NeurIPS-VLMo.pdf` | `raw/papers/architecture/pretraining/VLMo.pdf` |
| `多模态经典/2023-ICML-BLIP-2.pdf` | `raw/papers/architecture/connectors/BLIP-2.pdf` |
| `多模态经典/2023-NeurIPS-LLaVA.pdf` | `raw/papers/models/llava/LLaVA.pdf` |
| `多模态经典/2024-CVPR-InternVL.pdf` | `raw/papers/models/internvl/InternVL.pdf` |

上述映射已全部执行。其余三个原目录按内部相对结构完整归入 `raw/notes/多模态经典/`、`raw/notes/视觉编码器/`、`raw/notes/MLLM实例/`。原 PDF、TeX、Markdown、PNG、Excalidraw 和图形 PDF 导出全部保留；不因重复、未引用或可再生成而删除。

## TeX 本地依赖

- 静态检查覆盖 31 TeX 的 `includegraphics`、`input/include`、`includepdf`、`bibliography/addbibresource`、`lstinputlisting/verbatiminput`、`subfile`、`import/subimport`、`inputminted`、SVG/附件/文件存在判断、图像搜索路径及本地超链接等；处理注释、可选参数与配对花括号。
- 实际资源引用 165 次：直接 `includegraphics` 156 次，另有 VLMo 的 `figw` 调用 9 次。词法出现的 `includegraphics` 共 157 次，其中 1 次是宏定义；JSON 将含模板的词法次数与实际引用次数分别登记。VLMo 宏定义 `images/2022-NeurIPS-VLMo/#2` 作为模板另列，不将模板中的 `#2` 误报为缺失文件。
- 165 次引用全部可解析到原件；没有缺失或未解析项。未发现 `input/include`、`includepdf`、书目文件或其他本地源文件引用；相关命令的检查不等于发现其实际使用。
- 7 篇拟单独分类的论文 PDF 均未被 TeX 当作资源引用；已在新路径再次验证全部 165 次引用存在，TeX 与其图片的相对关系保持，无迁移引入的 TeX 资源断链。
- 环境依赖独立登记：`ctexart`、TeX 包、XeLaTeX/latexmk 及 Windows 字体（如 Microsoft YaHei、Times New Roman、Consolas、Segoe UI Emoji）。本阶段未检查运行环境、未重新编译，静态依赖通过不代表编译验收。
- TeX 中的外部 URL 已登记，未访问网络验证其有效性。

## 原件中的历史路径与现存断链

10 份原始 Markdown 中共检查到 19 个本地 Markdown 链接，其中 16 个目标存在且相对关系保持。以下 3 条在迁移前已经缺失；保留原件字节，在记录中说明，不重写原文：

| 原件及行号 | 原链接 | 说明 |
| --- | --- | --- |
| `MLLM实例/Qwen/复刻说明.md:11` | `Latex_out/Qwen3.8-Flash-Next总结.pdf` | 当前文件为 `Latex_out/Qwen3.8-Flash-Next总结_排版调整.pdf`；旧版文件不在本次原件集合内。 |
| `视觉编码器/README.md:43` | `../.work/visual-encoders/continuation-main/review.md` | 历史过程资料未随当前原件提供。 |
| `视觉编码器/README.md:43` | `../.work/visual-encoders/continuation-main/final-verification.json` | 历史过程资料未随当前原件提供。 |

部分既有 Markdown 在行内代码中记载同目录论文 PDF 名称。7 篇正文 PDF 已与笔记分流，这类原文说明保持历史身份，其旧新路径可通过 JSON `files` 和 `markdown_dependency_audit.literal_and_historical_paths` 追溯；不在旧路径复制原件。Qwen 说明中的系统临时区路径也仅登记为历史文字，不视为编译依赖或保证仍可访问的证据。

## 同字节文件

检测到以下 2 组同 SHA-256 文件；本次均按原路径关系完整保留：

- `视觉编码器/images/AIMv2/fig-02.png`；`视觉编码器/images/AIMv2/fig-03.png`
- `视觉编码器/images/NaViT/fig-01.png`；`视觉编码器/images/NaViT/fig-04.png`

## 执行结果与独立导入

- 原件迁移：261 件，159,091,076 字节；全部旧路径已不存在，全部新路径的大小与 SHA-256 和基线一致。未删除或覆盖任何原件，亦未修改 TeX/Markdown 原文字节。
- 空目录清理：仅对迁移前已登记的三个旧目录树执行非递归空目录删除，共 47 个目录；三个旧顶层目录均已清空移除。没有递归删除文件或触及新目录。
- 理念文章：另从 `C:\Users\ZENGZX\Desktop\Long-Horizon-Agents\raw\articles\llm-wiki.md` 原字节复制到 `raw/articles/llm-wiki.md`，11,985 字节，SHA-256 为 `dc3efe98ae62f23dd08acad13aba2e95287beb20b6bec2f4af0423557fe37401`。源文件亦复核未变；在 JSON `imported_reference` 单独登记，不计入原 261 件。
- 官方新增来源：主协调者独立核对 acquisition 的 24 个对象、26 原件后授权导入。已按 `download_path → planned_raw_path` 复制并逐项核验哈希与大小；包括 22 篇 PDF（主协调者核查共 534 页）、S024 官方博客 HTML/架构 PNG、S029 模型卡 README/config。临时提取文本和首页文本没有进入 Raw；未复制 acquisition.json 到本库。导入映射见 JSON `imported_official_sources`，身份与阅读状态由主协调者统一 source registry 登记。
- 本记录覆盖三类不同操作：261 件已有原件迁移、1 件理念参考原件导入、26 件官方新增原件导入，三类分别统计；不将文件迁入 Raw 视作学术核读完成。

## Git 与未测试项目

基线本地提交：`beb00884709059882482b9dc8d6059949608faef`。迁移结果、独立导入及更新后的维护记录尚待主协调者统一检查和提交；迁移代理未执行 Git 提交或远端操作。

本次已经复核原件字节、路径边界、目标不覆盖、TeX 静态资源和原有历史断链；未重新编译 TeX，未测试 Obsidian 展示。`.gitattributes` 的原目录与 `raw/**` 均保持 `-text`，PDF 为 binary；主协调者的初始暂存 blob 核验已确认 261 原件字节。
