# MLLM Wiki 追加日志

## [2026-10-31] schema | 建立本库规则与执行入口

- 以 AGENTS 为唯一规则入口，落地目录、摄入、查询、阅读表达、研究与检查工作流，区分 Raw、Wiki、Schema 及证据等级；规则检查点为本地提交 `a30aaf5`。
- 初始化的范围、来源登记与文件所有权见 [[maintenance/research/R001-initialization|R001维护记录]]；规则落盘不等于来源阅读或全库验收完成。

## [2026-10-31] lint | 原件迁移保全与工具初验

- 按迁移与审核记录，261份原始文件及后续原件已归档为288份Raw，磁盘与Git暂存字节核验一致；保全检查点为 `beb0088`、`5f6359e`。
- 检查工具、H-01定向修复与独立复核，以及四份旧TeX临时编译/代表页检查已登记于 [[maintenance/research/R001-reviews/structure-tool-and-builds|结构与编译初验报告]]，工具检查点为 `e19dbce`。此处不将初验记为全库学术或应用验收通过。

## [2026-10-31] ingest | 完成首轮MLLM原始来源阅读与跨主题整合

- 在31个旧工作对象、两综述与讲义的范围内，核验并建立34个唯一来源页（29论文/报告、2综述、1讲义、2官方文档），保留实际阅读范围、原文冲突和冻结旧笔记纠错；原有261文件逐字节保全，Raw共288文件。
- 深化18个总览/专题，形成52个知识页与141条实质双向整合关系；两张可编辑Excalidraw及PNG解释视觉接入与分辨率组织，正文区分原始证据、课程/综述转述和本库综合。
- 独立来源审查及主题图解审查的必须修订均已回核关闭，34来源统一为read / complete；内容范围、纠错、身份与审核记录见[[maintenance/research/R001-initialization|R001维护记录]]和[[maintenance/research/R001-reviews/themes-and-diagrams|主题图解审查]]。

## [2026-10-31] lint | 完成全库结构与图文验收

- [[maintenance/research/R001-reviews/final-structure|独立结构验收]]确认Raw集合/哈希、34来源、52知识页、141双向关系、索引与31TeX的165处依赖；严格检查无错误或警告。三条冻结旧Markdown历史断链登记保留，未回写原件。
- [[maintenance/research/R001-reviews/rendering|实际渲染验收]]覆盖539个数学表达与16个Mermaid；七条长流程改为纵向并复看，两张图由持久源重渲染。既有25项测试/9个独立反例与四份代表TeX编译结果见[[maintenance/research/R001-reviews/structure-tool-and-builds|工具与编译报告]]；Obsidian及模型实验未实测。
