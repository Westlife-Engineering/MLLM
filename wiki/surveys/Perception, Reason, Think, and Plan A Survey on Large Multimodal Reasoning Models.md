---
type: survey
source_id: S002
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]"
reading_status: read
ingest_status: integrating
---

# Perception, Reason, Think, and Plan：从多模态解题走向交互式推理

这篇综述最有用的问题是：**模型能看图回答、能生成较长的推理过程，为什么仍未必能可靠地在多模态环境中完成任务？** 作者把已有研究组织为模块化感知、语言中心的短推理、语言中心的长推理三类路线，再提出 Native Large Multimodal Reasoning Models（N-LMRMs）作为第四阶段展望。其核心关切是让推理过程持续利用模态信息，并能根据行动后的环境反馈调整，而不仅是让最终回答更长。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=4|PDF p4–6，§1–2]]

> [!important] 怎样使用这张地图
> 四阶段是**作者的历史组织方式与研究主张**，不是已验证的普遍演进定律，也不是模型成熟度评分尺。前三阶段的机制可组合、可交叠；第四阶段在 §2 明标 “Prospect”。本页直接读到的是本综述，文中引用的其他论文均未因此成为本库已读原论文。个案结果、综述转述、本库推断与作者展望分别标明。

## 来源身份与实际阅读范围

| 项目 | 登记 |
| --- | --- |
| 正式题名 | Perception, Reason, Think, and Plan: A Survey on Large Multimodal Reasoning Models |
| 作者 | Yunxin Li、Zhenyu Liu、Zitao Li（共同一作）；Xuanyu Zhang、Zhenran Xu、Xinyu Chen、Haoyuan Shi、Shenyuan Jiang、Xintong Wang、Jifang Wang、Shouzheng Huang、Xinping Zhao、Borui Jiang、Lanqing Hong、Longyue Wang、Zhuotao Tian、Baoxing Huai、Wenhan Luo、Weihua Luo、Zheng Zhang、Baotian Hu（通讯作者）、Min Zhang |
| 机构与版本 | 首页列 Harbin Institute of Technology, Shenzhen；arXiv:2505.04921v2 [cs.CV]，2025-07-06；身份依据本地 PDF 首页与元数据 |
| 原始来源 | [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf\|本地原始 PDF]]；[arXiv v2](https://arxiv.org/abs/2505.04921v2)，[版本 PDF](https://arxiv.org/pdf/2505.04921v2) |
| 作者列出的项目 | [Awesome-Large-Multimodal-Reasoning-Models](https://github.com/HITsz-TMG/Awesome-Large-Multimodal-Reasoning-Models)；本次未检查仓库与代码，不把链接当复现证据 |
| 文件校验 | 9,855,511 bytes；SHA-256：`94bf79d9c9bbeeae25b997cd35a290e056dc4ba561bf5a9b4cd7a786e98cdd94` |
| 阅读日期与正文 | 2026-10-31；共91页，实际阅读 PDF p1–42：摘要、目录、§1–6正文与表格；p43核对参考文献起点及 GQA 引用身份。页码从 PDF 首页起算，正文与印刷页码一致 |
| 原页视觉核查 | p1、3、7、10、16、19、25–30、32–33、35、41；图1–10全部查看，表6、12–15查看原页；其他表读取内容与上下文，未逐项追索其原论文 |
| 公式与机制图 | 正文未见独立编号的数学推导；图5的 DPO、GRPO、奖励类型示意已看，不能据图声称掌握完整优化目标或实现细节 |
| 未读与未测 | p44–91参考文献未逐条阅读；未追索被引原论文，未复现模型/benchmark，未审计数据、代码或隐藏推理过程；Obsidian 内显示未测 |
| 整合状态 | 本页已通过登记范围的独立内容审查并接入初始主题/索引；完整来源综合、结构与主 Agent 最终验收仍待收尾，状态保持 integrating |

## 四阶段究竟改变了什么

作者的分类同时涉及**推理在哪里发生、用什么中间表示、怎样获得能力、是否与环境交互**。把这些轴分开，比按年份排列模型更有助于比较。下表是依原文整理的阅读地图，阶段间不表示必然因果或互相替代。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=7|PDF p7，图3；p4–6，§2]]

| 作者阶段 | 主要改变 | 代表机制及解决的问题 | 不能据此推出 |
| --- | --- | --- | --- |
| 1. Perception-Driven Modular Reasoning | 在表示、对齐、融合与任务模块中处理推理 | 注意力、记忆、关系模块及预训练 VLM，把视觉与问题中的相关信息联系起来；后续包含 vision-encoder–LLM 架构 | 没有显式 CoT 不等于完全没有推理；不同 VLM 不能仅凭这个大类视为同构 |
| 2. Language-Centric Short Reasoning | 把中间步骤显式组织为 MCoT | 提示、rationale 学习、预定义步骤、局部视觉定位，以及搜索/检索/工具增强 | 有步骤说明不等于解释忠实；有工具调用也不自动具有长时程任务能力 |
| 3. Language-Centric Long Reasoning | 扩大推理路径、监督与反馈优化 | 图文交错信息、长 CoT 微调、best-of-N/beam search/MCTS、偏好优化和 RL；强调分解、反思、纠错 | token 更多不保证推理更好；任务内提升不等于跨任务泛化；System-2 是作者类比 |
| 4. Native Multimodal Reasoning（展望） | 希望统一多模态理解、生成和目标驱动交互 | 全模态表征、交错生成式推理、反馈驱动规划、经验学习 | 综述未给出一个已完整验证的 N-LMRM；第四阶段不是现有所有模型必须采用的架构规范 |

Stage 1 的细分见 [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=6|PDF p6–9，§3.1、表1]]；Stage 2 见 [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=10|PDF p10–15，§3.2、图4、表2–3]]；Stage 3 见 [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=15|PDF p15–18，§3.3、图5、表4–5]]。

**本库判断：阶段不是互斥的机制集合。** 原文 Stage 2 已讨论搜索、记忆、工具以及长时程任务，Stage 3 又按更深的推理与训练方式重新组织类似部件。因此更稳妥的读法是“作者认为研究重心如何转移”，不能写成“工具只属于第二阶段”“第三阶段才有规划”，也不能将 short/long 当作已有统一阈值的能力测量。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=13|PDF p13–18，§3.2.3–3.3]]

## Perception、Reason、Think、Plan 不是四个严格串行模块

**本库解释，依据作者用法整理：** perception 关心可用信息是否正确进入系统；reason 关心由信息到结论的关系；think 在本文主要指更长、可分解、可反思的推理过程；plan 把目标转成行动安排，并在交互中更新。论文没有给出四者互斥的形式定义或统一的可测阈值，不能把标题直接译成一个经过验证的认知架构。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=5|PDF p5–6，§2]]

图6提供了比“先感知再推理”更具体的例子：o3先尝试裁剪图形、发现裁剪范围不足、调整后再分析规则。这里推理会反过来决定**下一步看什么、如何看**；感知不是一次性完成的前处理。图8的六指图误判又说明，更长或更强的语言推理不能代替对当前视觉证据的检查。两者均为作者个案，不能估计发生频率。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=26|PDF p26，§4.1、图6]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=28|PDF p28，图8]]

对 planning 也要分两种要求：写出一个看似合理的计划，与执行后能根据新观察调整计划，证据需求不同。作者在 §4.2 强调的 agentic reasoning 是后者，包括层级分解、实时适应与环境交互。**本库推断：**若评测只检查计划文本或单次选择题，就不能直接确认闭环任务完成能力。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=27|PDF p27–30，§4.2、图9]]

## 从语言中心到原生多模态，差别在哪里

**作者主张：**语言中心系统主要借助语言模型组织推理，并把其他模态通过编码、描述、工具输出等方式接入。文本作为中间媒介有利于复用已有语言能力，但可能难以保留模态特有信息，也未必足以支持跨模态生成、反思和控制。作者因此提出 N-LMRM，应把 **Multimodal Agentic Reasoning** 与 **Omni-Modal Understanding and Generative Reasoning** 结合。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=5|PDF p5–6，§2]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=27|PDF p27–31，§4.2–4.3、表13、图9]]

| 检查轴 | 语言中心方法常见做法（综述归纳） | N-LMRM 的目标（作者展望） | 还需要什么证据 |
| --- | --- | --- | --- |
| 推理载体 | 以文本步骤为组织中心，视觉信息通过编码、caption、局部图块或工具接入 | 多模态信息在推理过程中持续交错参与，生成可充当中间推理资源 | 相同任务和预算下，保留模态信息是否带来可归因收益 |
| 模态范围 | 重点是图像/视频与语言 | 将音频、触觉、传感器、时序及结构化数据纳入统一处理 | 是否真正利用每种模态，冲突、缺失或噪声输入下是否仍可靠 |
| 交互方式 | 主要完成静态输入上的回答，也可外接工具 | 面向目标行动，接收反馈，调整策略 | 可执行动作、状态变化与任务终态的独立验证 |
| 学习方式 | 预训练、监督微调、偏好与奖励优化 | 从世界交互中积累可迁移经验，持续改进 | 环境交互带来的学习增益、遗忘、迁移和长期稳定性 |

表中最后一列是**本库提出的验证要求**，不是作者已完成的实验。特别要避免把“统一”理解为所有模态必须共用一个编码器：§4.3同时讨论统一表示与模态专门的 MoE 专家，并保留语言骨干的作用。更合适的开放问题是怎样协调表征与信息交互，而不是在“有无模态模块”之间作二元判定。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=30|PDF p30–31，§4.3]]

**原生多模态不等于不使用工具。** 作者把 o3/o4-mini 的裁剪、缩放等工具操作视作走向交错多模态思考的初步方向；这不能揭示闭源模型内部表示，更不能证明它们已经满足作者设想的全模态、持续学习和环境交互要求。表13将 agentic 与 omni-modal 模型分列，§4.2也说明所列工作只探索其中部分能力。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=29|PDF p29–31，表13、§4.2–4.3]]

## 训练改变能力，测试时机制分配计算：两者要分开看

综述把许多方法放进 o1-like / R1-like 叙事，但这些标签不是同一训练配方。**以下机制是综述转述，相关原论文未读**；这里只保留比较方法时必要的维度。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=16|PDF p16–19，图5、§3.3.2–3.3.3、表5–6]]

| 发生位置 | 机制 | 实际改变 | 证据边界 |
| --- | --- | --- | --- |
| 训练时 | rationale/CoT 监督、结构化阶段微调 | 学习中间步骤与输出格式，将分解、caption、thinking、answer 等写入生成习惯 | 文本格式可以被学会，正确性与忠实性仍须单独验证 |
| 训练时 | 偏好优化（如 DPO） | 用成对偏好约束模型输出分布 | 不能仅因综述将其归在 RL 脉络，就视为与在线环境 RL 同一算法 |
| 训练时 | GRPO 等奖励优化 | 对候选输出施加奖励，图5区分格式、答案、IoU、长度及奖励模型信号 | 奖励所测对象和任务真实目标是否一致，不能从算法名称判断 |
| 测试时 | best-of-N、beam search、MCTS | 增加候选路径，或对中间节点评分并选择/扩展 | 依赖采样数量、评分器、搜索预算；综述对搜索收益的归纳不是统一预算的独立比较 |
| 测试时/系统侧 | 裁剪、检索、代码、视觉专家与记忆 | 改变可用信息、外部计算和反馈路径 | 系统整体收益不应全归因于模型内部推理；工具权限与可靠性是条件 |

图5以流程示意展示算法，没有给出完整损失函数推导；本页不据此补造公式。作者也明确写到，多模态 R1 类工作常限制于特定任务，数学等任务学到的长 CoT 尚未普遍转成一般能力。表6还同时列 RLOO、PPO、GRPO、DPO，说明“R1类”不是“全都采用 GRPO”。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=18|PDF p18–19，§3.3.3、表6]]

**本库推断：**讨论效率至少要同时记录答案质量、输入视觉 token/分辨率、生成长度、候选数、工具调用与墙钟时间。本文图6的8分13秒是一个案例的耗时，未提供不同预算的控制实验，不能作为 test-time scaling 曲线或计算越多越好的证据。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=26|PDF p26，图6、§4.1]]

## o3 / o4-mini：作者实际展示了什么

§4.1的标题写 “Preliminary Study with o3 and o4-mini”，但**图6、7、8的图注明确都是 o3 case study**，正文详细分析也主要针对 o3。因此本页称其为“作者展示的 o3 个案”，不写成双模型对照实验，也不据此比较 o3 与 o4-mini 的能力高低。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=26|PDF p26–28，§4.1、图6–8]]

| 作者展示的个案 | 图中可观察或作者报告的结果 | 可以支持的有限判断 | 不能支持的推论 |
| --- | --- | --- | --- |
| 公务员考试图形题，图6 | 裁剪、调整、规则分析后答对；标注8分13秒 | 存在以工具调整视觉观察、再继续解题的成功案例 | 不能估计整体成功率，或证明长推理/裁剪的独立因果效果 |
| 定位照片、图形解题与预算活动选择，图7–8 | 作者给出成功输出与所用线索/代码过程 | 模型与工具组合可以处理部分复杂输入 | 不是跨分布鲁棒性、重复稳定性或完全自主任务能力的验证 |
| 六指手势，图8 | 图有六指，输出仍称四指加拇指、共五指 | 该例视觉内容与输出不一致；作者解释为语言先验干扰 | 单例不能隔离内部失误机制，也不能证明所有错误都源于语言中心架构 |
| 数独，图7 | 作者标注最终答案正确，但展示的逐步解释含错误 | 终答正确与解释步骤可靠可以分离 | 不能据此推断模型主观欺骗意图，或直接断定其完全没有相应解题能力 |
| 简历、播客、多媒体，图7–8 | 简历表有空白/错误/重复经历；播客仅截取前两分钟；生成素材未满足红熊猫等要求 | 交付文件存在不等于内容满足任务；工具与执行环境会限制能力 | 不能把当时工具/联网限制推广为模型永久能力上限 |

作者对数独案例使用了 “lies” 并推测可能导致训练中的欺骗。本页将其保留为**作者解释及担忧**。图中证据更稳妥地支持“展示给用户的解释并不可靠地对应正确解法”，没有意图识别实验，也没有可独立审计的完整内部推理。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=27|PDF p27，§4.1、图7]]

这组案例的局限也要与结果一同保留：§4.1和图6–8未报告统一样本总数、抽样规则、重复次数、完整调用配置与对照消融；图中有任务提示和部分过程摘录，仍不足以形成可复现的性能评估协议。**本库判断：**它们适合提出故障模式和下一步测量问题，不足以证明“换成原生多模态架构即可消除这些问题”。

## 数据与评测：任务地图不等于能力证明

作者将数据与 benchmark 组织为 Understanding、Generation、Reasoning、Planning 四个任务群：理解包含视觉与音频；生成区分跨模态生成与联合多模态生成；推理区分通用视觉与专门领域；规划包含 GUI 与具身/模拟环境。这是**任务组织图**，不是四种能力独立可测、严格互斥的结论。表14–15同时列训练数据与 benchmark，使用时须继续确认具体划分与用途。作者称该部分更新至2025-06-30，不代表当前完整目录。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=4|PDF p4，§1]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=32|PDF p32–40，§5、图10、表14–15]]

**综述转述：**§4.1汇集全模态及 agent benchmark 的较低分数，用以说明静态问答成功与真实交互之间仍有距离。这些分数来自被引工作，而非本文统一配置下重新运行的实验；本次未追索对应原论文，因而不抄成模型排行榜，也不把跨 benchmark 的数值差直接解释为模态融合或规划缺陷的因果证据。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=25|PDF p25–26，§4.1、表12]]

§5.5列出四类判分方法。下面将作者分类与本库使用时的限制并列，避免把评测器自身的输出当作无条件真值。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=41|PDF p41，§5.5]]

| 判分方法（原文分类） | 它检查什么 | 本库需要保留的限制 |
| --- | --- | --- |
| Exact/Fuzzy Matching | 输出与参考答案的精确/模糊匹配 | 答案等价性、文本规范化与参考答案覆盖会影响得分；不验证推理过程 |
| Options Matching | 从给定选项中选答案；作者举 CircularEval 处理选项偏好 | 选项改变任务形态；选择正确不等于能开放式完成真实任务 |
| LLM/MLLM Scoring | 用问题、参考答案、输出和评分提示让模型打分 | 必须核对评分器能力、提示、稳定性及与人类判断的对齐；本文概述不构成这种验证 |
| Agentic Evaluation | 让评价系统使用工具或多 agent 讨论来评估输出 | 此处指“agent参与判分”，不等同于“评测被测agent”；共识不自动保证正确性 |

**本库综合：**评估真实完成情况至少需要区分感知是否正确、推理结果是否正确、解释是否可靠、动作是否实际执行、最终状态是否满足目标。它们可以彼此脱钩，本文的六指、数独和文件个案正好提示了这种分离；但本文没有给出一套覆盖这五项的统一验证器。

## 来源自身的限制与待核查点

1. **地图覆盖面大，不等于每个条目已独立核验。** 作者声称覆盖约700篇出版物，但本页未验证检索完整性、收录偏差或每篇归类。最适合把它用于问题导航与机制分层，不作为全部模型/数据集事实的最终依据。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=4|PDF p4，§1]]
2. **本PDF内部已有可核对的引用不一致。** p33 §5.1.1把视觉问答数据集 GQA 引为 Ainslie et al. (2023)，但 p43参考文献该条实际题名是 *GQA: training generalized multi-query transformer models from multi-head checkpoints*；同页表14则将视觉问答 GQA 关联到 Hudson & Manning (2019)。这至少是局部引用错配，提示不可无核查复制条目身份，不推论整篇综述无效。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=33|PDF p33，§5.1.1、表14]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=43|PDF p43，References：Ainslie条目]]
3. **路线的可行性与必要性仍待验证。** 统一表征、交错长 CoT、世界经验学习和数据合成是作者提出的方向，本文未提供一种完成这些目标的统一架构与控制实验。它没有证明语言中心路线必然无法解决交互任务，也没有证明全部模态统一后一定更高效。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=30|PDF p30–31，§4.3、图9]]
4. **未来问题应落到可检验条件。** 值得保留的问题是：在相同预算和工具条件下，图像中间表示是否比文字描述少丢失任务信息；视觉证据与语言先验冲突时怎样识别和纠正；解释正确性与终答正确性怎样分别测量；任务内RL收益怎样迁移到新模态和环境。这些是本库根据本文提出的问题，不是本文已解答或已证实的研究空白。

## 本库主题落点

本页已实际接入以下初始地图；四阶段仍是作者组织与展望，个案仍是个案，模型案例在本页仍以综述为依据。其他唯一来源页的原论文阅读情况以 [[wiki/index|索引]] 为准。

- [[wiki/overview|总览]] 与 [[wiki/foundations/Formalization|基础]]：感知、推理与规划的工作区分，输出和任务证据的层次。
- [[wiki/architecture/Overview|架构]] 与 [[wiki/reasoning/Overview|推理]]：推理载体、接口、工具与动作—观察闭环；native 仍须落实到机制和验证。
- [[wiki/training/Overview|训练]] 与 [[wiki/efficiency/Overview|效率]]：训练形成的能力与测试时路径/计算分配分别记录。
- [[wiki/evaluation/Overview|评测]] 与 [[wiki/models/Overview|模型演进]]：答案、解释、执行和终态取证，以及任务分类、判分和演进叙事的不同用途。
