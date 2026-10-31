# R001 H：独立最终结构与交付验收

日期：2026-10-31（Asia/Shanghai）。角色 H，gpt-6-astra / high。只读核验正式内容，只写本报告和系统临时目录 `C:/Users/ZENGZX/AppData/Local/Temp/mllm-kb-20261031/final-acceptance/`；未派子代理，未改 Raw、Wiki、登记表、Schema、检查器或 Git，未打开 Obsidian、安装依赖或运行研究实验。

**结论：当前快照的结构可以交付；尚不在本报告中宣布整轮 Goal 完成。** 34 来源处于 read / reviewing 是实际终审阶段状态，不是 strict 缺陷。H 发现的正文状态漂移已由主代理修复并回核；没有剩余结构 must-fix。主代理仍须完成 G 主题/图解审查闭环、最终状态与追加日志、本地 Git 和临时恢复材料收尾，再运行最终 strict。

## 独立方法与原件保全

H 重新读取本库 AGENTS、全部七工作流、项目 conversation-to-note 技能、索引/日志、R001维护记录、迁移清单和来源登记；核对既有工具/编译报告及 F 实渲染报告。参考 Long-Horizon-Agents 的规则、工作流和技能仅只读。下列集合/哈希/拓扑、页面和表达核验使用本轮临时检查逻辑独立计算，不以主代理先前通过结果代替。

| 项目 | 本轮实核结果 |
| --- | --- |
| Raw 实际集合 | 288 文件；320,669,809 字节；与 manifest 三类清单并集严格相等，无多出/缺失 |
| 用户原始文件 | 261 文件；159,091,076 字节；磁盘每件大小/SHA-256与迁移清单一致 |
| 原始基线交叉验证 | 用 Git cat-file batch 实际读取迁移前提交 beb00884709059882482b9dc8d6059949608faef 的261个旧路径blob；全部大小/SHA-256与当前原件一致，未仅信任清单自报 |
| 旧 TeX 包 | 31 TeX、165次实际资源依赖；逐项比较旧源→资源与新源→资源相对路径，拓扑全部保持，当前资源存在 |
| 理念文章 | 1文件，11,985字节；独立计数，不增加学术来源 |
| 补齐证据 | 24对象对应26原件：22 PDF及S024/S029两组官方资料各2文件；逐件新路径/SHA与唯一source_id交叉匹配，无一件归到多身份 |
| 冻结旧理解输入 | registry共69个不同legacy_inputs，无重复分配；原始31份TeX均被覆盖；完整笔记包的其余附件由迁移manifest保全，不要求每张图单独登记为来源 |

Raw 全量集合指纹：`0a71ce15083efb802a56916dd754128c006b95fb51fe022a16f0a0718d8b61f7`。算法为：按 POSIX 相对路径排序，每行 `path<TAB>十进制字节数<TAB>小写SHA256<LF>`，保留最后 LF，对 UTF-8 串计算 SHA-256。逐件结果暂存在 `final-acceptance/raw-files.json`；摘要为 `raw-audit.json`，补源归属为 `imports-map.json`。

哈希验证证明字节保全，不单独证明文献标题或学术正确性。H 另对34个identity_key、完整题名、类型、原件/唯一页路径和来源页身份说明做交叉核对：34身份唯一，29 paper、2 survey、1 lecture、2 source。S024保持官方博客HTML/架构PNG身份，S029保持固定checkpoint的README/config身份，未伪造论文PDF。InternViT与InternVL在S025合并；DeepSeek V4.1两旧总结在S034合并；两综述、讲义与31工作对象分开统计。实质原文判断仍由对应 G 回证报告支持。

## 页面、导航与关系

实际递归枚举 Wiki Markdown 54文件，其中知识页52（34唯一来源页、18地图/专题），index/log另计；知识页类型为8 overview、10 topic、29 paper、2 survey、1 lecture、2 source。不能把18张地图/专题误称18个overview类型。

- 34页的source_id、type、reading_status、ingest_status均与registry一致，当前全部read / reviewing。paper/source主方向与正式目录一致，29论文与2综述的PDF/来源页镜像正确。
- 24来源填写related_directions；每个技术交叉方向均能对应现存正式技术目录，未把任意主题视角混作目录方向。141个声明的integrated_topics逐项核对来源→主题和主题→唯一来源双向链接，全部成立。链接存在只证明结构关系，其实质综合内容由G主题审查负责。
- 52知识页在索引恰有一个精确目标链接和对应一句摘要；18地图/专题条目均为实有页面。独立检查最初用字符串前缀误把SigLIP/SigLIP2等计为重项，改为解析完整wikilink目标后全部为1；这是本次临时检查逻辑的假阳性，不是库缺陷。
- 逐项阅读34页实际范围/未读未做说明，保留正文、关键附录、原页视觉核查、参考文献未追读、代码/复现未做等区别；S024/S029保留网页快照缺失和固定版本边界。read不被解释为每页附录、代码与引用文献全部核读。
- 当前无空目录、空知识页、施工占位文字或wiki嵌套副本。8张overview类型地图与10张topic类型页面有实质内容，未用占位页凑齐主题词表。
- 人工核对两正式图在对应主题旁有PNG嵌入、原生源链接、综合身份与来源定位；学术源与表达资产没有混计。

独立页面摘要与范围摘录暂存在 `page-audit.json`、`reading-scope-excerpts.json`。页码范围、现存链接/锚点与所有Markdown由strict递归检查；静态通过不证明每条引用位置的学术语义正确。

## 发现与返工闭环

H发现34页末的统一段落仍称ingest_status为integrating，与FM/registry reviewing漂移；少量简介/表格也残留待整合/待审状态。主代理移除重复施工句并将必要位置指回页首状态/页末主题，保留实际阅读范围、研究未知与未测试边界。H二次读范围段发现CLIP“整合与独立审核尚未完成”和DeepSeek-VL“独立审核与最终验收仍在进行”两处残留，主代理亦定向修复；再次搜索无残留。历史维护进度和追加日志未因状态更新被抹改。

原检查器H-01已在工具初验中闭环。本轮核验源码SHA-256仍为 `5313bb474d51ed2db8047077e0de240b6b70a73258a460544f8fc92441d8fbb0`，测试为 `0bb606bbbff091dff41263004fd7203eeb75392b9d25ba044ed2cecd8a951aa6`，与25项单测和9个独立fixture通过时一致。因此不机械重跑未改工具的全部测试。四份代表旧TeX临时编译成功及12原页实看沿用初验的明确范围；本轮确认原件未变，不重新编译，也不把4份推成31份均编译。

## 实际渲染覆盖与图源一致性

H独立重新枚举当前数学/Mermaid内容，排除frontmatter、代码围栏与行内代码后，与F渲染manifest按文件、顺序、display身份和LF规范化源码逐项比较，全部相同：

| 实际内容 | 数量与内容指纹 |
| --- | --- |
| 数学 | 539项＝65显示＋474行内；`9e2a65b4e17e9f3bc22547bcede6b1459299b9a8c69a4c8bcbd5a5f59acd35b3` |
| Mermaid | 16块；`74c3d655d0bcd9a54205dd9f1d32ba4a5acccf49227fe9188cc766a431ead73d` |

因此F对KaTeX/Mermaid的实际渲染覆盖仍适用于本快照；H没有把此内容一致性核对冒充再次全量渲染或逐个公式学术回证。F报告保留1100px/headless Chrome实看范围、7条长链改纵向及全量渲染无错的事实。

4个正式图资产均实际存在。两Excalidraw为标准JSON，visual-entry有65元素/9箭头/14组，resolution-boundaries有80元素/8箭头/28组；所有箭头双端绑定指向存在元素。PNG经PIL完整性校验，分别2200×2649、2200×2825；H实际打开两张最终PNG，未见内容截断、连线穿字或不可辨标签，图内综合身份和边界可见。正式源与PNG的4个SHA全部与F离线源渲染后登记值一致，未发生报告后单改源/图。临时roundtrip PNG是1100px宽的1倍输出，不与正式2倍图按字节相等作误判。

完整图资产指纹和结构核验存 `rendering-continuity.json`；正式指纹见 [[maintenance/research/R001-reviews/rendering|F渲染报告]]。此处的原生源结构、哈希连续性和独立实看，与F实际从持久源导出的证据共同确认对应版本，不宣称H重跑了导出。

## Schema、仓库与明确边界

七工作流与conversation-to-note覆盖三层边界、身份查重、证据等级、唯一来源、Query积累、独立审查、实际阅读表达、追加日志、有限研究与串行共享写入。与参考库对照后，本库没有继承其S001引用选文授权、每方向5篇/总91篇预算、2026-10-25历史完成状态、项目内临时区例外、自动精简Raw辅助材料权限或Harness/Optimization分类；MLLM视觉/架构/模型归属及讲义、官方source已明确适配。项目技能仍为Query操作指南，不是第二Schema入口。

只读Git快照：分支main，HEAD `3c7893d1b6254aefee2e75e92be8ae6ae7918950`；检查时暂存区为空，未配置remote；存在本轮已改及未跟踪Wiki/审核/图资产，尚待主代理统一显式暂存与本地提交。该快照不声称未来提交已完成。Raw的.gitattributes保持-text。

除已登记缓存外，根目录与非Raw文件清单未发现意外过程脚本、提取文本、HTML分享副本或额外临时目录。仍有两个被忽略的既有缓存：`scripts/__pycache__/check_vault.cpython-311.pyc`（52,757字节）、`tests/__pycache__/test_check_vault.cpython-311.pyc`（27,038字节），共79,795字节。此前清理在CreateProcess前被工具策略以blocked by policy拒绝；H未删除、未重试绕过，也不把gitignore当作已清理。系统Temp仍保留本轮恢复材料，最终保留/清理记录由主代理负责。

允许且明确保留的历史项：冻结旧Markdown三条原有断链（Qwen旧PDF文件名1条，视觉编码器旧.work过程路径2条），已在迁移记录逐条登记。原件字节必须保全，不能回写“修好”；strict单列documented_historical_links，不把它们伪装为新Wiki零断链。两组原始同字节PNG也保留。见 [[maintenance/migrations/2026-10-31-initialization|迁移记录]]。

应用边界：未打开Obsidian，因此Obsidian内显示、主题CSS、窄栏/深色模式、插件编辑、应用内PDF跳转未测。标准渲染器成功不保证这些应用表现；未跑模型、训练或benchmark，原文阅读和学术审查不等于复现。

## 主代理最终置complete条件

1. G主题/两图审查及定向定位修订全部回核关闭；主代理通读并接受实际证据范围，不以H结构通过代替学术验收。
2. 最终统一34来源FM、registry和index为真实状态，追加一次实质ingest收尾及必要lint记录；保留历史日志、阅读/未读/未测范围与既存原文冲突。
3. 对最终文件快照运行不带allow-incomplete的strict，确认无错误/警告；若数学、Mermaid或图源再有变化，定向补实渲染并更新报告，否则用上述内容指纹确认覆盖。
4. 主代理显式核对diff/暂存范围，完成授权的本地Git检查点并确认Raw暂存/提交字节；不配置remote、不push。不以本报告预支尚未执行的Git结果。
5. 按已知策略约束记录临时恢复集去向及缓存未删除事实，不绕过拒绝；完成Goal时如实给出结构、学术、渲染与应用四类验收边界。

本报告所引工具初验入口为 [[maintenance/research/R001-reviews/structure-tool-and-builds|工具与代表编译报告]]；整轮状态由 [[maintenance/research/R001-initialization|R001维护记录]] 和主代理最终验收管理。

## H本次strict执行输出

报告初稿落盘、主代理状态正文修复及G定向定位修订后，独立执行 `python -B scripts/check_vault.py`，未传 `--allow-incomplete`；退出码 0。有效JSON报告 `allow_incomplete: false`、`passed: true`，errors=0、warnings=0。计数：288个manifest Raw、2481条链接、73个受检查Markdown、31 TeX/165依赖、288 Raw/320669809字节、34来源、32主PDF；三条冻结原件历史断链仍独立列明。执行原始JSON存系统临时目录 `final-acceptance/strict-final.json`。该链接数是此时快照值，后续新增日志/报告链接可正常增加，不能硬编码为长期门槛。
