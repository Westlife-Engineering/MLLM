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

## [2026-10-31] schema | 审核并实施来源目录调整

- 主Agent审核提案并采用23份PDF/23个唯一页的技术方向迁移，保留Flamingo视觉接入与联合系统家族目录，registry保留v1；原提案逐字节存入Raw，采用/不采用理由见[[MLLM知识库架构调整方案|实施方案]]与[[maintenance/research/2026-10-31-architecture-review|审核记录]]。
- 关系登记补S001→训练总览、S002→评测总览、S003→可见性与连接，移除ViT→基础形式化的仅导航关系；141改为143。更正计数口径：双向链接不证明实质使用，当前143是已登记数，另81条正文引用差集仅供人工判断。
- 原288份Raw与13份历史维护文件字节保全，新增仅1份原提案；34来源/31学术身份/52知识页不变。34项回归及strict通过，图资产和公式/Mermaid内容未变；迁移与历史追溯见[[maintenance/migrations/2026-10-31-architecture-review.json|清单]]，Obsidian未实测，未提交或push。


## [2026-11-03] schema | 按用户要求撤下已实施方案并整理本地提交

- 用户明确要求删除根目录实施方案及Raw原始提案；仅删除这两份未跟踪文件，保留已实施的架构调整与审核/迁移记录。原路径、删除前哈希与授权见[[maintenance/migrations/2026-11-03-proposal-withdrawal.json|撤下清单]]，替代阅读入口为[[maintenance/research/2026-10-31-architecture-review|架构审核记录]]。
- 当前Raw回到288份，初始化原件与34来源/31学术身份/52知识页不变；旧日志和2026-10-31验收文件中的289份为当时快照。Git提交范围与本次验证见[[maintenance/research/2026-11-03-proposal-withdrawal|维护记录]]。
