# Ingest 清单

规则入口：[[AGENTS#4. Ingest：读取并整合新来源|AGENTS · Ingest]]。用户提交资料、要求纳入来源或明确启动有边界研究时触发；不代表后台任务。

## 从原文到知识更新

1. 读索引、最近日志、相关主题与来源，递归排查 survey / paper / lecture / source。按标题、作者、DOI/arXiv、官方 URL 和版本核实身份；旧笔记名称只是线索。取得总协调者分配的唯一来源 ID、目标路径、文件所有权。
2. 依 [[workflows/structure|目录规则]] 归档原件，记录来源 URL、获取日期、版本、SHA-256 和大小。归档前后核对字节。用户输入全部保留；旧笔记包冻结。官方 HTML 无需转造 PDF，来源获取失败须记录真实状态。
3. 使用 academic-researcher 分析；PDF 用 pdf skill 核读原页，讲义用 course-pdf-knowledge 建页段地图、按 core / medium / brief 抓重点。benchmark 论文按任务需要读 benchmark-paper-reading。先读相关正文、方法、证据、局限及必要附录，重要公式/图表必须查看原页；只读摘要属于筛选。
4. 在唯一来源页写已核身份、source_id、原件/哈希、实际读取日期与范围、未读部分、核心理解、证据定位与局限。旧总结作为待校正输入另列，不放入直接学术证据链。发现旧稿错误应在 Wiki 纠正并保留必要说明，不能回写冻结原件。
5. 围绕已有主题写清支持、限制、修订、冲突或补充了什么；维护来源与主题双向链接。无实质新认识也如实说明，不强求创新点；有内容才建主题。
6. 取得共享写入时段后重读当前主题、索引、登记表；整合、更新摘要/状态/日期，按 [[workflows/presentation|阅读表达]] 同步图文。不能用旧整文件副本覆盖别人的新内容。
7. 完成局部 [[workflows/lint|Lint]]，返回证据定位与交付包。学术审查疑点回原页，结构问题定向修补；主 Agent 验收后进入收尾时段，追加简短 ingest 日志、更新状态并再次确认。失败、未整合和待审核不能提前写 complete。

## 状态与计数

所有来源页在最小知识页字段外增加 source_id、reading_status、ingest_status；paper / source 必有 primary_direction。字段与来源登记保持一致。

| 字段 | 值 | 含义 |
| --- | --- | --- |
| reading_status | unread | 未实际读取正文；下载或元数据核对不算阅读 |
| reading_status | partial | 已读明确部分；正文写已读/未读范围 |
| reading_status | read | 已完成来源页登记的正文/关键附录阅读范围；正文必填实际范围，不暗示全部附录和代码全读 |
| ingest_status | pending / reading | 待处理 / 正在阅读 |
| ingest_status | integrating | 已读待整合，或正在整合主题与索引 |
| ingest_status | reviewing | 内容已交付，等待学术/结构/主 Agent 验收 |
| ingest_status | complete | 原件、身份、读取、整合、检查、验收与日志收尾已完成 |
| ingest_status | blocked | 具体获取或验证障碍已登记，不表示内容可靠 |

尚未取得原文的来源只登记在 registry / 维护队列：raw_files 为空，reading_status 为 unread，ingest_status 为 pending，不生成 Wiki 来源页。raw_path 此时只是计划位置，不能当成已存证据。已取得但受阻的原件可保留真实状态，不能伪造已读分析。工作对象（旧独立材料）、原件文件、去重学术来源、非论文官方资料分别计数；同论文多个版本/附件/总结不重复计学术身份，讲义也不替代其引用论文。

### 来源登记接口

`maintenance/source-registry.json` 由主 Agent 统一维护，顶层 `schema_version: 1` 与 `sources` 数组。每项有 `source_id`、`slug`、`type`（survey / lecture / paper / source）、`title`、`primary_direction`（survey / lecture 可为 null）、`identity_key`、`raw_path`、`wiki_path`、`raw_files`、`legacy_inputs`、`reading_status`、`ingest_status`、`integrated_topics`。raw_files 是 `{path, sha256, url, version}` 的数组，实际新增 Raw 逐项登记；legacy_inputs 为冻结输入路径数组。初始原件由迁移 manifest 覆盖，不因未逐份列入 raw_files 就漏掉保全检查。owner / review 等本轮说明可按需增加，不为脚本方便无限扩展 Schema。登记页与来源页状态一致，主路径不替代实际 raw_files 清单。子代理交付更新建议，不能并发写登记表。

## 单篇分析要回答什么

| 分析问题 | 研究信息 |
| --- | --- |
| 具体困难 | 视觉表示、跨模态对齐、连接、训练、生成、推理或评测中的具体问题，适用任务和失败现象 |
| 改变了什么 | 输入/输出、视觉编码器、连接器、语言模型、数据、目标函数、训练阶段或推理流程；信息怎样传递 |
| 为什么可能有效 | 作者机制解释、明说前提及本库推断；冻结/可训练参数、模态信息损失、监督和计算代价等相关条件 |
| 证据支持到哪里 | 任务、数据划分、模型规模、分辨率/token、预算、指标、基线、消融和评测协议；作者主张与实验证据分开 |
| 最接近工作差异 | 已核读原文之间的机制与条件比较；未读对方时只写作者比较或待核验 |
| 未解释之处 | 替代解释、缺失消融、未测条件、失败例；未测试不等于无效，不等于领域空白 |
| 对本库的影响 | 哪个判断被支持、限制、修订或挑战，冲突是否源于条件/术语 |
| 下一条证据 | 有价值的补读/核查及理由；允许没有新研究问题，不自动扩展本轮范围 |

重要主张就近引用 PDF 页码与章节/图表，或 HTML URL/标题/日期。综述重地图和分类；讲义按实际页序串联概念、公式、图和例子，补充讲解另标；官方文档重版本/功能/公开信息边界；评测重测量对象、任务、判分与混杂；理论区分假设、证明与经验验证。不是所有来源都填同一套实验模板。

## Subagent 交付与验收

按 [[workflows/autoresearch#派发与共享写入|角色和共享写入协议]] 执行，单篇由 D 负责并承接返工；A 核验身份，G 独立学术审查，H 检查结构，主 Agent 终审。交付包括身份/ID/类型/归属、原件与哈希、实际读取范围、关键理解和原页定位、证据边界、主题变化/双向链接、文件清单、状态与日志草稿、检查结果和未测项。

“已读待整合”“待验收”如实保留。Obsidian 不可用或未授权时，完成文件与可执行渲染检查，单列应用未测，不冒充全部展示通过。临时清理仅处理本任务可再生过程文件，原件、用户输入与冻结包不自动清理。
