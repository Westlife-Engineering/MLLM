# R001 阅读表达与实际渲染验收

检查者：F；日期：2026-10-31（Asia/Shanghai）。本报告只登记阅读表达、渲染和资产恢复性，不代替 G 学术审查或主 Agent 最终验收。

## 范围和方法

E 释放正文后于 2026-10-31T08:56:22.512Z 完成最终快照渲染。递归枚举 wiki 下 54 张实际 Markdown（52 知识页及 index/log），没有只按预期目录抽样。提取时排除 frontmatter、代码围栏和行内代码，枚举实际 dollar/LaTeX 定界数学及 Mermaid 围栏。每个实际数学表达均调用 KaTeX 0.16.47 渲染到 HTML/MathML；全部渲染结果再由 headless Chrome 加载真实 KaTeX CSS/字体，实际截图。Mermaid 11.17.2 对每块执行 render 并将 SVG 插入浏览器截图。验证页面宽度 1100px（内容约1006px），不修改本机 Obsidian 设置。

初次 headless 启动发现当前 Playwright 所期待的 bundled Chromium 未安装，随后使用本机现有 Chrome 的独立 headless 进程；没有安装浏览器或依赖。临时 localhost 静态服务和 headless 浏览器均在脚本 finally 中关闭。

## 数学与 Mermaid 结果

- 实际数学：539 项 = 65 显示公式 + 474 行内表达；KaTeX parse/render 错误 0、strict 警告 0。包括 S030 唯一页十块显示公式及 Sequence-Memory-and-Retrieval 的两块 GDN 公式。
- 实际 Mermaid：16 块，全部 SVG 渲染成功，失败 0。
- 已实际查看所有65块显示公式（10张检查页）、所有16块 Mermaid，以及474项行内数学的16张长页截图。显示公式逐块检查上下标、分式、矩阵、cases、范数、括号和文字；行内长页为整体视觉检查，没有逐项回原论文做学术复核。
- 发现7张 LR 长链在1100px页面中将字缩至约8–12px；向 E 提交后，E 保持节点/边/文字改为 TB：Generative-Output-Interfaces、MiniGPT-5、DeepSeek-OCR、DeepSeek-V4.1-Flash、DeepSeek-VL、DeepSeek-VL2、NaViT。已对最终7张重渲染并逐张看图，文字可读、箭头/分支完整。其余9张内容 hash 未变。
- 预渲染与 E 释放后快照的数学内容在统一 CRLF/LF 后完全相同：true。后一次仍全部重新渲染；最终已知差异不只用定界符配对处理。

临时脚本、539项逐块source/hash、54文件字节hash、16块Mermaid source/hash、截图与初稿快照保留在系统临时目录 `%TEMP%/mllm-kb-20261031/rendering/`，作为本轮恢复材料；它们不是知识正文或新学术来源。持久核对使用下方内容指纹：指纹对换行统一为LF，保留其余数学/图代码字符、文件、顺序及数学display身份，不依赖行号/frontmatter状态。

- 数学全量内容 SHA-256：`9e2a65b4e17e9f3bc22547bcede6b1459299b9a8c69a4c8bcbd5a5f59acd35b3`。
- Mermaid 全量内容 SHA-256：`74c3d655d0bcd9a54205dd9f1d32ba4a5acccf49227fe9188cc766a431ead73d`。

## 两张可编辑图

绘制前已读项目适配、通用 Excalidraw skill/runtime 与 MCP guide；回读相关唯一来源及关键原页/原图：Flamingo p.5 Fig.4、BLIP-2 pp.3–4 Figs2–3、LLaVA p.4 Fig.1、NaViT p.2 Fig.2、AIMv2 p.4 §2.4、S024 本地官方架构 PNG。图均标“本库机制综合”，不作论文效果排名。

MCP 初始 describe 确认空画布；批量绘制，实际看截图后修正 Flamingo 连线穿文字、NaViT A/B/C 标签、AnyRes 面板边距，完成分组与箭头绑定。每图持久导出后才清空自用场景，最后 describe 验证恢复初始空画布；没有覆盖用户或其他 Agent 的非空场景。

最终 PNG 特意从持久 .excalidraw 源以现有 CLI 离线重渲染（scale 2、padding 25），随后实际查看最终PNG；因而源文件可独立恢复，不依赖内存canvas。MCP现场截图与离线renderer对矩形圆角有差异，正式PNG采用离线重渲染结果。中文使用系统fallback，其他机器字体可能不同。

### visual-entry

- 源：[[wiki/assets/diagrams/visual-entry/visual-entry.excalidraw]]；图：[[wiki/assets/diagrams/visual-entry/visual-entry.png]]。
- 65 元素、9 箭头、14 分组；双端绑定无悬空引用：true。JSON解析/源离线render通过，实际查看PNG通过。
- 源 SHA-256：`f1a2b11708e8d81e9cc907fc887670bf14dd7e4d4b62ce4e9d0415fd7376d186`。
- PNG SHA-256：`731a7c467ade38257038000f7561f2a7c6578ffa17a8558bc76d893a401b31c6`。

### resolution-boundaries

- 源：[[wiki/assets/diagrams/resolution-boundaries/resolution-boundaries.excalidraw]]；图：[[wiki/assets/diagrams/resolution-boundaries/resolution-boundaries.png]]。
- 80 元素、8 箭头、28 分组；双端绑定无悬空引用：true。JSON解析/源离线render通过，实际查看PNG通过。
- 源 SHA-256：`7133a549db82e88c4aa49000737c3b7a0b071b619c59ececef2bf6c8b8831689`。
- PNG SHA-256：`837edc41b5e0b484397a5083b9ddebdf721a0315aab08da312a514ca572da175`。

图一在 [[wiki/architecture/Visibility-and-Connections]] 嵌入；图二在 [[wiki/vision/Resolution-and-Token-Budget]] 嵌入，均附相对PNG链接、标准原生源链接、机制综合身份及原始来源定位。AIMv2图中的4×3与2×6明确为教学计数；AnyRes图中方块不能当真实token计数。

## 数学分文件覆盖

以下按文件列实际表达数与该文件数学内容指纹；无数学文件仍已参与全量扫描。

| 文件 | 显示 / 行内 | 数学内容 SHA-256 |
| --- | ---: | --- |
| wiki/architecture/Generative-Output-Interfaces.md | 1 / 0 | `476cbb8794e4c0e2c918749887b94b52f3e3a74fa96b1b953b32dc4fa838a0be` |
| wiki/architecture/Sequence-Memory-and-Retrieval.md | 2 / 16 | `36bc9f5c03cc53533f556ec087f8d9909450f0f8f962f0b3d16df65acefc5e9d` |
| wiki/architecture/Visibility-and-Connections.md | 0 / 1 | `4957c1738ad1679f98b8d4a55620f16451b42b90cd81ae3cc46189e93750b838` |
| wiki/efficiency/Resource-Ledger.md | 0 / 8 | `fcde783f0d0640c1e68f0ea48e0e660ea421ca2d456bb9892cbdc410252eaf18` |
| wiki/foundations/Formalization.md | 1 / 11 | `906579478b17f9132fb580cd4602f4362ba72332076d4e0bf3a1be36a029eb0b` |
| wiki/lectures/VLM-2.md | 6 / 42 | `6f84d50d844913b3dfc95f51c7ca489b8bfe0190285510e9c8237f9c9a13dc34` |
| wiki/models/Family-Changes.md | 0 / 2 | `ccd01f4a99151532838b8ce1f1ac542576e24f3cf4ae0537650f495ad1c57c18` |
| wiki/papers/architecture/connectors/BLIP-2.md | 0 / 1 | `165e3ec0595e7ab044d999120e945e9d10cca2049b4ca8ec27202269d7ba15d4` |
| wiki/papers/architecture/connectors/Flamingo.md | 2 / 2 | `bd6c1792dc8e3d5e23963e9fb39fb18439417adb713acd96c0fbec6474910c3f` |
| wiki/papers/architecture/connectors/InstructBLIP.md | 1 / 2 | `032f4503ad29561ddb35012c51a325989b753a5cff3618d6dcc9e2a13c4ec15e` |
| wiki/papers/architecture/connectors/mPLUG-Owl.md | 0 / 6 | `308f5a7ce842c0c740642cbbc91864d23395cd8a4ddb49a2b9342f00590e4675` |
| wiki/papers/architecture/generation/MiniGPT-5.md | 2 / 13 | `19f628a893e2f74baabaef5d4a4ae1d83580d0a3945ecb1ec3ce1b738b826f63` |
| wiki/papers/architecture/pretraining/ALBEF.md | 6 / 20 | `96a580d567a25505e520f91e5a3a704e18796fb52bbe213a398e06b3edc7abb4` |
| wiki/papers/architecture/pretraining/BEiT-v3.md | 1 / 21 | `2649e31699f5b1a5d1765143064080761ea7c1594be8f3bd62b9f31ddec56871` |
| wiki/papers/architecture/pretraining/BLIP.md | 2 / 8 | `712741419197b7958defe51a38cff75d847e36b60fbd579132c00876ebdc1814` |
| wiki/papers/architecture/pretraining/CoCa.md | 2 / 15 | `4759ead0578d35f3bee67dddd7d2ee1ecb7002976b69f94c3249972280db45a8` |
| wiki/papers/architecture/pretraining/VLMo.md | 2 / 19 | `95f52482a25267eb517a34eba8b4098e036badf47aed4a1d0429e3f1418b72b4` |
| wiki/papers/models/deepseek/DeepSeek-OCR.md | 2 / 15 | `62b2ae09b4115bdd2412f3147222da75ccc13cc903a9ef1dfc72772797d04185` |
| wiki/papers/models/deepseek/DeepSeek-V4.1-Flash.md | 4 / 23 | `75360126748b9ecc984a90ac03f3259408233db7a9a546a4c9466d36edbd51b4` |
| wiki/papers/models/deepseek/DeepSeek-VL.md | 0 / 4 | `7ba472c9c1e4515ec32cc037b5ff6f9d846038d4fbfa219ed87c70a58da7bc66` |
| wiki/papers/models/deepseek/DeepSeek-VL2.md | 1 / 15 | `d7850d462bfc26b33e0540bb8803c31934cb0dad854fb6c145b2bd801b08a82d` |
| wiki/papers/models/internvl/InternVL.md | 0 / 3 | `bca08a10c33aa60ee88fec13a62937b11c3c45141bbcd62a278bfcb03a5c4f4b` |
| wiki/papers/models/llava/LLaVA-1.5.md | 0 / 2 | `86b8c7a5699e9f62b555ac665948bc526782cc14819352df1f1b96c464cf6ac0` |
| wiki/papers/models/llava/LLaVA.md | 0 / 6 | `bd96ee52d4475772cce773b059f0d156c36063e77c25ea21bffa7098a1eaa6fc` |
| wiki/papers/models/qwen/Qwen-VL.md | 1 / 9 | `03f5ff2ca58d16b85c568f1e1f44b0e109256378bade025afd6dfeb016ae22c9` |
| wiki/papers/models/qwen/Qwen2-VL.md | 1 / 7 | `6f0a7b7b561006745e1f002af5c9f99670be8f0b9163b6edd08d34363eb4774b` |
| wiki/papers/models/qwen/Qwen3-VL.md | 0 / 2 | `5a332dcadb0cee921fad0b44d2bbe76003d1ba5c6075db6c1c446028a304ea14` |
| wiki/papers/models/qwen/Qwen3.8-Flash-Next.md | 10 / 49 | `5b427457f42fef74569431ce02a48291fa268fe794caf2b49336b9d4f30b9ec2` |
| wiki/papers/vision/alignment/CLIP.md | 2 / 15 | `57ec5d3a267bc884848170686109aeae157831dba43dbb406a6bea0814e4a228` |
| wiki/papers/vision/alignment/SigLIP.md | 2 / 32 | `e14fc05c59ac0826ccd6b99a600b8eafb6d1543bda574ed0582a1e19729fc7b7` |
| wiki/papers/vision/alignment/SigLIP2.md | 1 / 6 | `35939726203733256f3ec6da477109f8cb80cc7b958962aff3ce32d90f514818` |
| wiki/papers/vision/encoders/AIMv2.md | 3 / 23 | `3e4eea3de810fb1061c7b6592ca513573291ee486cdcf383d231d7d7087a3814` |
| wiki/papers/vision/encoders/NaViT.md | 2 / 18 | `369651979a0c7094f1cff1a53a5daf3fb8d3f8b899c36a50cd9e9333d482745e` |
| wiki/papers/vision/encoders/SoViT.md | 2 / 20 | `8bc341fd1529483ec41e639090fda59a130ad25c6bdf1a7f900b3ee1d6e6e7a0` |
| wiki/papers/vision/encoders/ViT.md | 2 / 9 | `43e1d2a45c44846b56559623c1921b4a9c4041cb004bb3728c313e3351b3edd8` |
| wiki/reasoning/Overview.md | 1 / 0 | `0393a4d06b089ab86ff68573a176046ae726ecc2a28d9c7e33fb9ca962f211ef` |
| wiki/sources/models/llava/LLaVA-NeXT.md | 0 / 1 | `02705da6e355e4e1819ebd62eb1833e343590c49ccd803d116c744f0065684b2` |
| wiki/sources/models/qwen/Qwen-3.5.md | 0 / 1 | `664e40201fa2370156f1f86512db7d1f6b0ca727309763d202bedc688023a2e5` |
| wiki/surveys/Efficient Multimodal Large Language Models A Survey.md | 0 / 4 | `d11d94b1954de3ee33c5613606ae3d631f042c6c0363dce3850e957cc10e996d` |
| wiki/training/Supervision-and-Stages.md | 0 / 3 | `f4ed101733e469d9b92f512c3af35fb14c05024e436bb063e222e34262396b95` |
| wiki/vision/Objectives-and-Transfer.md | 2 / 7 | `d96c1feacd322c8e3092eecb3a5c30229b25916337e769572cd881cb1a0ed029` |
| wiki/vision/Resolution-and-Token-Budget.md | 1 / 13 | `3a5b1c5678cb7735e18c28c892b1959f067e7fe3a8fc33df2d7df51c28c2d807` |

## Mermaid 逐块覆盖

| 文件与快照行号 | 渲染 / 实看 | 代码 SHA-256（LF） |
| --- | --- | --- |
| wiki/architecture/Generative-Output-Interfaces.md:29 | 成功 / 已看 | `1d20dcc589ef1c0b28e8514aa298c3ffaaffa5026b16d201e5c56e29694357a1` |
| wiki/lectures/VLM-2.md:158 | 成功 / 已看 | `9932f4dd30a1612b2fcda0bb1358ac2e9b2a3de56a88c147acdff5084ee64ea7` |
| wiki/overview.md:20 | 成功 / 已看 | `017844674575ef0c66cebad58b248b4e2ac18526ca294e9a42720ed6e1114d41` |
| wiki/papers/architecture/connectors/InstructBLIP.md:31 | 成功 / 已看 | `430e26cf10d56fafc9744ee446547825978fe9b1636daedc9e79abc74351bec1` |
| wiki/papers/architecture/generation/MiniGPT-5.md:28 | 成功 / 已看 | `95d7455d79782e3978d77e22b4c4d5318443d9a3e69b814b9e1a311a6fd0d51a` |
| wiki/papers/models/deepseek/DeepSeek-OCR.md:31 | 成功 / 已看 | `33bc7e99d1d62f5051afd3a90ab139f8b8106afcf51d5e3854dde70538bd1c6a` |
| wiki/papers/models/deepseek/DeepSeek-V4.1-Flash.md:46 | 成功 / 已看 | `087197d4b0b177a806920431f95d75346a11d65ed41efe8f234a6b8512b72a0b` |
| wiki/papers/models/deepseek/DeepSeek-VL.md:31 | 成功 / 已看 | `089820d96878705a8981566bce294ed9272511898da99c1644112af09896db4f` |
| wiki/papers/models/deepseek/DeepSeek-VL2.md:31 | 成功 / 已看 | `d57dd46ffa0f396e2e335000666eed6e8eeacaaf84f064aa7edddac2ffdf15d2` |
| wiki/papers/models/internvl/InternVL.md:41 | 成功 / 已看 | `4b42d9683ce4b2f003abd5caba5579ad8a0a5be500721c178d7f17f53df0fd51` |
| wiki/papers/models/llava/LLaVA-1.5.md:68 | 成功 / 已看 | `cd143f0b4cf75ca7cb23417e53955dcac325e3d2e50a78fa2d709d690bb51a36` |
| wiki/papers/models/llava/LLaVA.md:35 | 成功 / 已看 | `5363146307ed1cb242f4582a11fb1c1a45f4e02962dcce08f0a1c6a7e6a81e50` |
| wiki/papers/vision/encoders/AIMv2.md:41 | 成功 / 已看 | `c3fd36505d8ff2db8ce63a9a07a22c85a4fa86f91909ba3336f2d1ddcc0283e3` |
| wiki/papers/vision/encoders/NaViT.md:32 | 成功 / 已看 | `3d9efdeb92e70f917d5e5a2fe2ec55ed3b4f37fc018c3774e57cf93d8da7a91d` |
| wiki/reasoning/Overview.md:30 | 成功 / 已看 | `7b20753a50d4887f86744212511b5a53eee807f064131b0293ac6c6d40916821` |
| wiki/surveys/Efficient Multimodal Large Language Models A Survey.md:23 | 成功 / 已看 | `43d7d4661c3c3d6d7ac550f695b14f7690913e8d4e1df4f6120fcc7f295eeb33` |

## 限制与后续校验

这是标准渲染器实际输出验收；未打开 Obsidian，故“Obsidian 内显示未测”，没有验证插件原生编辑、主题CSS或应用内PDF跳转。检查页保留公式本身和来源文件/行号，没有重建每张完整Markdown页面的所有排版，不声称已实看全库正文每一行。渲染通过不证明每个公式语义、所有论文论证或模型能力正确；独立学术验收仍归 G/主 Agent。

root 后续统一 ingest 状态与 index/log、仅改 prose/来源状态时，按数学/Mermaid内容指纹判断是否仍覆盖；如再修改公式、Mermaid代码或正式图源，须定向补渲染并更新本报告。
