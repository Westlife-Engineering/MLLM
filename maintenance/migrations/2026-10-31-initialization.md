# 2026-10-31 初始化迁移记录

**状态：仅完成基线准备，尚未执行迁移。** 本记录不代表已建立正式知识页、完成学术核读或通过 Obsidian 验收。

本次用户已授权将原件保持字节不变迁入 `raw/` 并建立仅本地 Git。参考 Long-Horizon-Agents 的原件保护与迁移方式，但不沿用参考库的历史授权、目录词表或任务状态。Git 检查点由主协调者统一执行，本阶段未执行 Git 提交。

## 完整性基线

- 原件 261 件，共 159,091,076 字节。PDF 45、TeX 31、PNG 171、Markdown 10、Excalidraw 4。
- 归档类别：综述 PDF 2、讲义 PDF 1、论文正文 PDF 7；既有笔记包 251 件（31 TeX、35 PDF、171 PNG、10 Markdown、4 Excalidraw）。笔记包的 35 PDF 包括 31 份阅读输出和 4 份图形导出。
- 全部原件已计算 SHA-256，并在写记录前再次逐项核对大小与哈希；261 个目标路径无大小写冲突，目标均不存在；未检测到原目录中的重解析点。
- 完整逐文件映射见同名 JSON 的 `files`，每项字段为 `old_path`、`new_path`、`sha256`、`size`、`kind`。路径统一为相对本库根目录的正斜杠路径，`size` 单位为字节，`sha256` 为小写十六进制。
- JSON 顶层 `schema_version: 1`、`date: 2026-10-31`、`status: baseline_prepared_migration_not_started`；依赖审计和异常亦保存于该 JSON，不另造 Raw 说明文件。

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

其余三个原目录按内部相对结构完整归入 `raw/notes/多模态经典/`、`raw/notes/视觉编码器/`、`raw/notes/MLLM实例/`。原 PDF、TeX、Markdown、PNG、Excalidraw 和图形 PDF 导出全部保留；不因重复、未引用或可再生成而删除。

## TeX 本地依赖

- 静态检查覆盖 31 TeX 的 `includegraphics`、`input/include`、`includepdf`、`bibliography/addbibresource`、`lstinputlisting/verbatiminput`、`subfile`、`import/subimport`、`inputminted`、SVG/附件/文件存在判断、图像搜索路径及本地超链接等；处理注释、可选参数与配对花括号。
- 实际资源引用 165 次：直接 `includegraphics` 156 次，另有 VLMo 的 `figw` 调用 9 次。VLMo 宏定义 `images/2022-NeurIPS-VLMo/#2` 作为模板另列，不将模板中的 `#2` 误报为缺失文件。
- 165 次引用全部可解析到原件；没有缺失或未解析项。未发现 `input/include`、`includepdf`、书目文件或其他本地源文件引用；相关命令的检查不等于发现其实际使用。
- 7 篇拟单独分类的论文 PDF 均未被 TeX 当作资源引用；本次映射保留了全部 TeX 与其图片的相对关系，预计无迁移引入的 TeX 资源断链。
- 环境依赖独立登记：`ctexart`、TeX 包、XeLaTeX/latexmk 及 Windows 字体（如 Microsoft YaHei、Times New Roman、Consolas、Segoe UI Emoji）。本阶段未检查运行环境、未重新编译，静态依赖通过不代表编译验收。
- TeX 中的外部 URL 已登记，未访问网络验证其有效性。

## 原件中的历史路径与现存断链

10 份原始 Markdown 中共检查到 19 个本地 Markdown 链接，其中 16 个目标存在且相对关系会保留。以下 3 条在迁移前已经缺失；保留原件字节，在记录中说明，不重写原文：

| 原件及行号 | 原链接 | 说明 |
| --- | --- | --- |
| `MLLM实例/Qwen/复刻说明.md:11` | `Latex_out/Qwen3.8-Flash-Next总结.pdf` | 当前文件为 `Latex_out/Qwen3.8-Flash-Next总结_排版调整.pdf`；旧版文件不在本次原件集合内。 |
| `视觉编码器/README.md:43` | `../.work/visual-encoders/continuation-main/review.md` | 历史过程资料未随当前原件提供。 |
| `视觉编码器/README.md:43` | `../.work/visual-encoders/continuation-main/final-verification.json` | 历史过程资料未随当前原件提供。 |

部分既有 Markdown 在行内代码中记载同目录论文 PDF 名称。7 篇正文 PDF 将与笔记分流，这类原文说明保持历史身份，其旧新路径可通过 JSON `files` 和 `markdown_dependency_audit.literal_and_historical_paths` 追溯；不在旧路径复制原件。Qwen 说明中的系统临时区路径也仅登记为历史文字，不视为编译依赖或保证仍可访问的证据。

## 同字节文件

检测到以下 2 组同 SHA-256 文件；本次均按原路径关系完整保留：

- `视觉编码器/images/AIMv2/fig-02.png`；`视觉编码器/images/AIMv2/fig-03.png`
- `视觉编码器/images/NaViT/fig-01.png`；`视觉编码器/images/NaViT/fig-04.png`

## 后续执行与验收门槛

1. 主协调者审查基线并提交初始本地 Git 检查点；不得推送远端。
2. 获协调者通知后，按 JSON 中的明确映射移动原件，禁止覆盖目标；使用原生 PowerShell `-LiteralPath` 并验证绝对源/目标均在本库边界内。
3. 迁移后逐项复核 261 件原件的 SHA-256 与大小，核对总量、文件类型、TeX 资源及历史路径说明；如发现变化或缺失即停止。
4. 完成后将本记录与 JSON 状态更新为实际结果，明确 Git 检查点与尚未测试的项目；本阶段不得提前写“已迁移”。

本阶段新增且供主协调者统一提交的文件：`.gitignore`、`.gitattributes`、`maintenance/migrations/2026-10-31-initialization.json`、`maintenance/migrations/2026-10-31-initialization.md`。
