# R001 H：检查工具、迁移字节与代表 TeX 工程验收

日期：2026-10-31（Asia/Shanghai）。角色 H，gpt-6-astra / high；未参与 C 的工具开发，未派发子代理。此报告是施工期间独立工程检查，不是全库学术验收或最终 strict 验收。

## 结论与待处理项

- **迁移字节验收通过**：独立遍历得到 288 Raw 文件、320,669,809 字节；实际集合与 manifest 的 261 原件 + 1 理念文章 + 26 官方新增原件完全一致，全部大小及 SHA-256 匹配。四次 TeX 编译前后对全部 Raw 重算哈希，集合、字节均无变化。
- **代表编译验收通过**：四份冻结 TeX 的完整旧笔记包复制到系统临时区，在副本上以现有 TeX Live 2026 / XeLaTeX + latexmk 编译，均 exit 0，无缺字、缺图、致命错误或 Overfull 警告。实际查看了 12 个代表页，详见下表。
- **工具主体覆盖符合结构检查定位，H-01 已修复并通过独立复核**：初始23 tests 全通过后，独立反例发现 Markdown 块锚点只存在于 fenced code 或 HTML 注释时仍被判为有效；C 定向修复后，H 重跑25 tests及原九个独立 fixture，全符合预期。历史发现与修复证据保留在下文。该漏报未证明当前 Wiki 有实际坏锚点，不应记成来源作者内容错误。
- **施工检查通过，不等于初始化完成**：本次 `--allow-incomplete` 快照 0 errors、35 warnings（32 来源页尚未建立、索引尚未建立、两份现有综述未进入索引）。这些是建设队列，不能据此宣称 complete。最终内容与索引完成后须重新运行 strict 并检查实际报告。
- 本次不审定学术主张、文献真实身份的全部外部证据、网页远程资产完整性或 Obsidian 显示。未操作 Obsidian，**Obsidian 内显示未测**。

## 范围、输入与可复核性

完整读过 `AGENTS.md`、`workflows/lint.md`、`workflows/structure.md`、初始化计划与迁移说明，读过 latex-compile 与 pdf 技能。入口时 `wiki/index.md`、`wiki/log.md` 尚不存在，已如实记录为施工状态，未补写。

检查对象：`scripts/check_vault.py`、`tests/test_check_vault.py`、`maintenance/source-registry.json`、`maintenance/migrations/2026-10-31-initialization.json`，以及当前全部 Raw 和当时已存在的 Wiki/规则/维护 Markdown。工具与测试初查 SHA-256：

| 文件 | 初查 SHA-256 |
| --- | --- |
| scripts/check_vault.py | 847ab35eb15c667b82bb09160d70e6583837698211787aaa4fafad84c4ba9534 |
| tests/test_check_vault.py | 1cd7662946ac883595aac2792b7d632f93b0e70e3329d79b72effb66bfda480e |

临时证据根：`C:/Users/ZENGZX/AppData/Local/Temp/mllm-kb-20261031/validation/`。其中 `tests.txt`、`construction.json`、`independent-integrity.json`、`probe-results.json`、`raw-before.json`、`raw-after.json`、`build-results.json`、各编译 `.log/.fls` 和代表页 PNG 保留供定向返工/最终验收；不是 Raw 来源或永久知识正文。

H 唯一库内写入为本报告；未改 Raw、Wiki、Schema、registry、工具或测试，未操作 Git、安装工具或修改全局环境。所有 Python 使用 `-B`。原先 `scripts/__pycache__/check_vault.cpython-311.pyc` 与 `tests/__pycache__/test_check_vault.cpython-311.pyc` 已存在；按协调要求仅登记，未删除或重试已被策略拒绝的清理动作。

## 工具覆盖与独立反例

执行 `python -B -m unittest discover -s tests -v`：23 项通过，耗时约 1.57 秒。逐段审读实现，而非仅依据测试数量判定。

| 验收维度 | 实际覆盖及证据 | 边界 |
| --- | --- | --- |
| 原件完整/未读 Raw | manifest 与 registry 各自验证 SHA/大小，实际 Raw 集合对照登记；未读且已取得原件可作为 pending 工作，allow 模式降级未建页；未取得原件只允许 unread/pending、空 raw_files、无来源页 | SHA 一致只证明字节，不证明作者/标题身份 |
| 原件变更不可放行 | 自建 fixture 在有效 PDF 后追加字节，allow 模式仍报 raw_hash / raw_size；前后 fixture 文件字节相同，检查器未写文件 | 不能通过刷新登记哈希“修复”真实原件变更 |
| 身份与版本 | 检查重复 source_id、identity_key、wiki_path、raw_path；arXiv identity_key 去掉 vN；一个来源容纳多版本 raw_files；23 tests 内有正负覆盖 | 不是按全文标题/作者/DOI 别名推理身份；canonical identity_key 的分配仍由主代理核验，不能称自动学术去重完备 |
| source / lecture / survey / paper | 四类均递归识别并核对来源目录、页面 type/id/状态，paper/source 主方向与路径、paper/survey PDF 镜像；lecture/source 原件目录类型有检查 | 正文读到哪里、版本解释与真实性须人工核读 |
| 来源页对应 | 强制主原件在 sources、原件哈希出现于页内、registry/page 状态相符；独立 lecture→topic 反例报 registry_page_mismatch | 出现哈希并不保证正文解释正确 |
| 链接与 PDF 页码 | 普通链接、图片、wikilink、表格别名转义、标题锚点、PDF page=N 范围及越界、越出 Vault 检测 | HTML 远程 URL/锚点不网络验证；块锚点漏报见下 |
| 主题双向关系 | 对 registry.integrated_topics 验证来源→主题和主题→来源；独立缺回链反例报 theme_backlink | 未声明的实际主题关系不能靠该字段自动推断；主题综合质量人工审查 |
| figw 与 TeX | 实际提取 figw 定义展开参数；当前 31 TeX 共165次静态资源与迁移审计相符；VLMo 临时实编 `.fls` 读取九个真实图片 | 非通用 TeX 解释器；不会证明任意宏/条件展开、字体可用性或编译成功；本轮另做实编 |
| 空页/空目录/嵌套 | 空 Markdown、仅标题正文、空子目录、wiki 嵌套、重解析点有检查；独立空页/空目录 fixture 正确报错 | “有正文”不等于有学术内容；根目录与导航/日志的全部内容质量仍需最终清单检查 |
| 历史断链 | 3 条冻结 Raw 原有缺失链接只按迁移记录报告；普通当前文档使用同样旧路径仍报 link_target | 不能把历史 Raw 例外扩展到新 Wiki |
| 只读 | 源码无写文件、网络、Git、编译调用；九个独立 fixture 检查前后文件集合及字节全部相同 | 工具结果是当次快照，其他作者施工可能改变后续状态 |

独立 fixture 未调用交付测试的 fixture helper，自行构造单页讲义、真实一页 PDF、manifest、registry 与索引。九个场景为：有效基线、Raw 改字节、PDF 第2页越界、空页与空目录、lecture 页面伪装 topic、声明主题无回链、当前文档使用迁移前路径、代码块内伪块锚点、HTML 注释内伪块锚点。前七个行为符合预期；后两个复现同一漏报。

### H-01：块锚点目标未屏蔽示例与注释

当前 `markdown()` 在 `anchor.startswith("^")` 分支直接对 `self.text(dest)` 执行行尾块 ID 正则。目标页正文若只包含 fenced code 示例 `example ^fake`，或同样文本只在 HTML 注释内，链接 `[[wiki/lectures/example#^fake]]` 仍返回 passed=true。预期应报 `link_anchor`，因为这些不是可引用的正文块。标题检查已使用 masked_markdown，块检查应采用一致屏蔽原则，并保留实际正文块 ID 正向测试。

复现文件位于上述临时根的 `probes/block_anchor_only_in_code/` 与 `probes/block_anchor_only_in_comment/`；运行 `python -B scripts/check_vault.py --root <fixture绝对路径> --allow-incomplete`。已向主代理发送具体原因与建议，H 未自行修改工具。初次报告时该项待返工核验；现已完成定向修复验收，见文末追加记录。

## 迁移与来源登记复核

独立计算未复用检查器 digest/inventory 函数：288 个文件集合无缺失/额外文件，所有 manifest 项的大小及 SHA 一致；registry 的 36 项 raw_files 逐项匹配实际字节。34 个登记来源的类型数为29 paper、2 survey、1 lecture、2 source；这些是身份登记数，不是已读数，也不等于31工作对象或288文件。

26 个官方新增原件逐项核对 manifest.source_id、new_path、sha256、original_url/final_url 与对应 registry.raw_files：无不一致。S024 为官方博客 HTML 与架构 PNG，S029 为同一固定 Hugging Face commit 的 README/config；未把 HTML/README 伪称 PDF，也未把两个附件增加为新来源。这里只确认本地登记与字节对应，不宣称重新完成 A 角色的全部外部身份核验。

31 TeX 的迁移依赖清单165项均有实际文件；本次实编的 `.fls` 再确认所用资源：VLMo 9、NaViT 5、Qwen 21（含4个 redraw/exports PDF）、DeepSeek 15。NaViT 的 fig-01/fig-04 两个同字节文件均保留，且两处引用都进入实编。

对旧 Markdown 19条本地链接独立按迁移后的原包相对路径求解：16条存在、3条缺失，与迁移记录完全一致。缺失项是 Qwen 复刻说明所指旧输出 PDF，以及视觉编码器 README 所指两个历史 `.work` 过程文件。原件保持字节，不为其创建占位文件；这些记录不豁免新 Wiki 断链。

## 临时编译与实际视觉验收

环境检测：`D:/texlive/2026/bin/windows/xelatex.exe`、同目录 `latexmk.exe`；系统已有 Poppler。未安装或更新工具。完整复制 `raw/notes/` 至临时 `validation/notes/`，保全所有包内相对依赖，再从每份副本的所在目录执行：

```text
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=<validation/builds/对应文档> <原TeX文件名>
```

所有编译产物与中间文件只在临时副本/临时 build 目录；冻结 TeX 未做排版优化。日志逐项检索 Missing character、缺资源、致命错误、Overfull/Underfull、一般 Warning；实际 PDF 以 Poppler 渲染并查看，下表页码从 PDF 第一页起。

| 冻结 TeX（raw/notes/ 下） | 实编结果 | 代表页实际查看 | 结果 |
| --- | --- | --- | --- |
| 多模态经典/2022-NeurIPS-VLMo总结.tex | exit 0，12页 | 1、2、8 | 首页文字与公式可读；第2页 figw 架构图正常；第8页三栏说明和 Callout 未裁切 |
| 视觉编码器/NaViT总结.tex | exit 0，3页 | 1、3 | fig-01/fig-04 重复图都正常出现，页3额外实验图完整；重复是冻结原件事实 |
| MLLM实例/Qwen/Qwen3.8-Flash-Next总结.tex | exit 0，14页 | 1、3、8、10 | 首页两架构图、页3对比表/公式可读；页8的fig-297/299和页10的fig-309/311完整，层次与连接线没有缺失；图中小字需按正常PDF放大阅读 |
| MLLM实例/Deepseek/DeepSeek-V4.1-Flash训练总结.tex | exit 0，13页 | 1、3、9 | 首页完整，页3 Sinkhorn 条件/公式和页9长度惩罚公式均无裁切、重叠或越界 |

四份均有3条 `xeCJK` 字体家族重定义 Warning，来自原 TeX 设置；视觉查看没有缺字/方框。VLMo 另有6条 Underfull（355、360、365行三栏内容），Qwen 另有12条 Underfull（231、420–421、460–461、525–526行）；代表页的窄栏/对齐留白不影响文字与公式阅读。NaViT 和 DeepSeek 无 Underfull。四份均无 Missing character、Overfull、缺图或致命错误。本次未查看四份合计42页的每一页，不能把12个代表页检查写成全文逐页视觉验收。

## 后续最终门槛

1. H-01 定向修复验收已完成：25 tests 与原九个独立 fixture 全符合预期；无待处理 H-01 项。
2. 所有来源、主题、索引、日志与图解完成后再运行 strict；本次施工快照不替代最终全库检查。
3. 主代理按实际任务边界统一处理缓存、Git 暂存与临时恢复集；H 不对本次未执行的清理、Git 或应用操作作通过声明。


## 2026-10-31 追加：H-01 修复独立复核通过

C 将块锚点匹配的目的文本改为 `masked_markdown(self.text(dest), False)`，沿用已有 fenced-code / HTML-comment 屏蔽逻辑；新增两个针对代码块与 HTML 注释伪块 ID 的负例。H 读取并审查该行及两个测试。把此一行在内存中逆向还原后，SHA-256 正好等于初查源码哈希；从当前测试字节中仅移除新增两个测试块后，SHA-256 正好等于初查测试哈希，确认此修复没有附带其他代码/测试改动。没有对交付文件执行逆向写入。

- 独立执行 `python -B -m unittest discover -s tests -v`：25 tests 全通过，约1.55秒，包含既有真实正文块锚点正向用例。
- 对初查保存的九个 fixture 原样重新调用当前 Checker，不重新生成 fixture：此前漏报的两个场景现在各正确产生 `link_anchor`；其余七个场景的 errors/warnings 与原结果一致。九个场景的检查前后文件集合及字节全部相同。
- 复核后源码 SHA-256：`5313bb474d51ed2db8047077e0de240b6b70a73258a460544f8fc92441d8fbb0`；测试 SHA-256：`0bb606bbbff091dff41263004fd7203eeb75392b9d25ba044ed2cecd8a951aa6`。
- 临时证据新增 `tests-h01-fixed.txt`、`probe-results-h01-fixed.json`，原始 `tests.txt` 和 `probe-results.json` 继续保留，历史失败不被覆盖。

此次定向复核未重新运行已通过的四份 TeX 与代表页视觉检查，修复不涉及 TeX、资源、Raw 或编译流程。主库仍处施工期，讲义新页与 registry 的同步不作为本次工具修复缺陷；本次未以施工期间状态代替最终 strict 验收，也未改 Wiki/registry。

主代理进一步确认先前缓存清理命令是在 CreateProcess 前被策略拒绝，返回理由只有 `blocked by policy`；H 仅补记这一确切状态，未推测更多原因、未删除缓存或重试。H-01 关闭；初始化最终 strict、学术、应用与 Git 验收边界保持不变。
