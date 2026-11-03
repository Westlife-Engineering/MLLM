---
type: paper
source_id: S028
primary_direction: models/qwen
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/models/qwen/Qwen3-VL.pdf]]"
reading_status: read
ingest_status: complete
related_directions:
  - vision/representation
  - architecture/visual-interfaces
---

# Qwen3-VL：把视觉层级、时间与长上下文接入同一语言骨干

Qwen3-VL 要解决的问题不只是提高单张图片问答分数：动态分辨率视觉输入进入语言模型后，如何保留不同深度的视觉信息，如何表达长视频的时间，以及如何让多模态训练与文本能力共同发展。报告给出的主要结构变化是 **Interleaved MRoPE、DeepStack 和显式文本时间戳**；它们分别处理位置频率分配、跨层视觉特征注入和时间表达，不能视为同一个技术的三个名字。训练还同时扩展数据、上下文和后训练，因此最终能力变化不能全部归因于这三项结构。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=2|原文 p2–4 §1–2]]

## 来源与阅读边界

| 项目 | 本次确认 |
| --- | --- |
| 身份 | Qwen Team，*Qwen3-VL Technical Report*；arXiv:2511.21631v2 |
| 版本日期 | 首页正文日期 December 1, 2025；arXiv 侧栏标记 v2、27 Nov 2025，两者照录 |
| 原件 | [[raw/papers/models/qwen/Qwen3-VL.pdf]]，42 页；[固定版本原始 URL](https://arxiv.org/pdf/2511.21631v2) |
| SHA-256 | ee075d08e67de1148d6437c6c1d481f7894183b8793905a2deb5f62664f49380 |
| 实际阅读 | 2026-10-31；正文 p1–25、附录 A/B p33–42；贡献者 p26 与参考文献 p26–32 仅用于结构与来源导航，未逐项追读引用 |
| 原页图像核看 | p3–4 架构/训练表，p15–18 结果与 OCR 图，p20–22 评估条件/文本比较，p24–25 消融/NIAH，p37、40、42 提示模板 |
| 旧笔记输入 | [[raw/notes/MLLM实例/Qwen/Qwen3-VL总结.tex]] 正文比对；[[raw/notes/MLLM实例/Qwen/Latex_out/Qwen3-VL总结.pdf]] 共 9 页，核看 p2–5、9。均为二手输入 |
| 未实施 | 未审计模型实现、未运行推理或复现训练/评测；Obsidian 内显示未测 |

以下性能是报告作者的实验，不是本库独立验证。自建 OCR、OmniBench 和长视频检索测试按其公开协议范围解释。

## 1. 从视觉 patch 到语言隐藏状态

### 1.1 视觉编码器与模型家族

语言骨干覆盖 dense 2B、4B、8B、32B，以及 MoE 30B-A3B、235B-A22B，均有 Instruct 与 Thinking 版本；A 表示激活参数规模，不能与总参数混用。视觉侧默认采用 SigLIP-2-SO400M，2B/4B 使用 SigLIP-2-Large（300M），并继续预训练以适应动态分辨率。视觉编码器同时采用 **2D-RoPE 和插值绝对位置编码**，不能沿用上一代“去掉绝对位置编码”的描述。两层 MLP merger 将相邻 $2\times2$ 视觉特征合并并映射到语言隐藏维度；DeepStack 另有对应的 merger。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=3|p3 §2、Figure 1]]

与 [[wiki/papers/models/qwen/Qwen2-VL|Qwen2-VL（S027）]] 相比，动态输入与空间合并仍是控制视觉序列成本的重要机制，但本报告新增的中间特征注入不能仅用“把更多视觉 token 拼到开头”解释。旧 TeX 中 patch size、bias、激活函数、具体中间层索引及代码变量属于实现层笔记；本次没有审计对应代码，不能把它们升级为已核实实现事实。

### 1.2 DeepStack：增加进入语言层的视觉通道，不增加序列长度

通常连接器只取视觉编码器最终输出，语言模型后续层只能反复处理这一份压缩后的视觉表示。这里从 ViT **三个不同深度**提取特征，各自经过 merger，加入语言模型**前三层**相应的隐藏状态。图 1 的纵向连接表示不同视觉深度进入不同语言深度，不表示重新输入三张图片，也不表示新增三倍视觉序列长度。报告明确说该注入不增加上下文长度；具体三个 ViT 层号没有在正文给出。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=3|p3–4 Figure 1、§2.2]]

作者的消融使用内部 15B-A2B 语言骨干、200B tokens 预训练、**没有后训练**。Table 12 中平均分 74.7→76.0，InfoVQA 71.9→74.2、DocVQA 89.5→91.1；TextVQA 则 80.6→80.5。因此较稳妥的结论是，在这个验证设置中，多层注入总体有益，但没有逐项提高；这不是对 235B 最终模型所有改进来源的分解。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=24|p24 §5.12.2、Table 12]]

### 1.3 Interleaved MRoPE 与文本时间戳各自解决什么

MRoPE 将时间、两个空间轴编码进旋转位置表示。旧的分块分配方式会使各轴占据不同频率范围；Interleaved MRoPE 将轴对应的维度交错分布，改善三轴在高低频段的分配。这里的“交错”指位置编码频率维度的组织，不是图文样本交错数据；正文没有提供完整轴维数比例或逐维排列公式，本页不补造。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=3|p3 §2.1]]

视频另在每个 temporal patch 前放显式文本时间戳，如 “3.0 seconds”，也可用时分秒。作者指出，将实际时间绑定为过大的位置 ID 会造成稀疏位置分布，并与采样帧率耦合；文本时间戳让语言模型直接读取时间语义，代价是增加少量序列。它没有取消 MRoPE 的时间维，也不意味着任意采样策略下定位精度保持不变。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=4|p4 §2.3]]

## 2. 训练预算：视觉对齐、全参数融合与长度扩展

| 阶段 | 更新参数 | 训练 token 预算 | 序列长度 | 作用 |
| --- | --- | --- | --- | --- |
| S0 | Merger | 67B | 8,192 | 视觉—语言接口对齐 |
| S1 | All | 约 1T | 8,192 | 多模态预训练 |
| S2 | All | 约 1T | 32,768 | 长上下文；增加文本、视频与 agent 数据 |
| S3 | All | 100B | 262,144 | 超长文档与长视频适配 |

上述值直接来自 Table 1；SigLIP-2 的动态分辨率继续预训练发生在此前，其独立预算未在此表报告。约数不能相加后写成精确总训练量。报告还说明将 per-sample loss 改为 square-root-normalized per-token loss，以平衡不同数据；没有给出可完整复现的归一化公式或全部权重，因此不据名称自行推导实现。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=4|p4–5 §3.1、Table 1]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=2|p2 §1]]

### 2.1 数据不是一个无差别的“合成集”

图像 caption 由 Qwen2.5-VL-32B 结合原描述重新生成细节；语义去重针对**重新生成的文本**，视觉嵌入聚类另用于发现覆盖稀疏的概念。书籍/网页解析使用 7B 模型整理交错图文，将相邻页组成最长 256K 序列，并过滤图文比例及质量。知识实体采取重要性采样，对显著性较高的实体增加采样，不是对长尾一律均匀加权。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=5|p5–6 §3.2.1–3.2.3]]

OCR 包含 30M 内部伪标注样本；多语言部分另有约 30M 合成样本和超过 1M 真实样本。文档解析使用约 3M PDF（十类来源）和 4M 内部文档，先预测区域与阅读顺序，再用 Qwen2.5-VL-72B 识别。QwenVL-HTML 保留细粒度位置；QwenVL-Markdown 主要定位图片与表格，训练描述中表格使用 LaTeX。但附录 OmniDocBench 评估提示要求 HTML 表格，因此训练表示与任务输出格式不能强行统一。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=6|p6 §3.2.4]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=36|p36 Appendix B.4]]

2D 定位把坐标归一化至 $[0,1000]$；计数包括直接回答、框辅助和点辅助。3D 数据则把单目图像及指代表达映射为 9DoF box：中心三维坐标、三维尺寸和 roll/pitch/yaw，在统一的虚拟相机坐标系组织，并过滤遮挡和噪声标注。这是学习结构化空间预测的监督形式，不能仅由“输出了三维数字”断言已获得可靠的物理尺度或可执行机器人动作。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=7|p7 §3.2.5–3.2.6]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=37|p37 Appendix B.5]]

视频根据长度约束调整 fps 和最大帧数，并生成带时间信息的密集 caption；STEM 使用几何点标注、感知与 caption 数据，以及超过 60M 习题和超过 12M 长推理样本。GUI 数据结合自演化轨迹和人工定向检查。函数调用的一部分数据可以**不实际执行函数**，由模型生成响应；报告另述真实在线搜索轨迹，两者证据身份不同。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=8|p8–9 §3.2.8–3.2.10]]

### 2.2 后训练为什么要区分答案、过程与工具奖励

SFT 约 1.2M 样本，约三分之一纯文本、三分之二多模态，先以 32K 训练一个 epoch，再以包含长样本的混合数据训练第二个 epoch，长度扩至 256K。Thinking 冷启动中视觉/文本约 1:1，并用纯文本模型排除无需图像也可解的样本；这种筛选只能说明对该筛选模型的难度，不能证明每题对所有模型都必须看图。蒸馏包括教师离线响应与学生在线 rollout 的 logit KL 对齐，但报告未给完整 KL 方向和权重公式。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=10|p10–11 §4.2–4.3]]

推理 RL 选择可由规则或代码验证的任务，以多次采样滤掉过难及过易问题，形成约 30K 查询；报告使用 SAPO，但没有展开完整算法公式。通用 RL 同时用规则与模型评审，减少 reward hacking 是设计目标，不是已证明不会发生。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=11|p11–12 §4.4]]

“Thinking with Images” 先对 Qwen2.5-VL-32B 做约 10K grounding 冷启动和多轮工具 RL，再将约 120K 交互蒸馏到 Qwen3-VL 并继续训练。奖励分别覆盖答案、推理质量和工具调用次数；报告观察到仅有前两者时会出现过早单次调用的捷径。目标调用次数由离线 Qwen2.5-VL-72B 估计，原文的 expert-estimated **不是人工专家标注证明**。附录实际工具是 image_zoom_in_tool，以 box、标签、图像索引裁剪放大；提示里的 research 不代表联网搜索。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=12|p12–13 §4.5]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=40|p40–41 Appendix B.9]]

## 3. 结果应回答哪些问题

### 3.1 Thinking 更适合哪些任务，而非是否“全面更强”

旗舰 235B-A22B 的 Table 2 中，Thinking/Instruct 在 MMMU 为 80.6/78.7、MathVision 为 74.6/66.5；OCRBench 为 875/920、DocVQA 为 96.5/97.1，ODinW-13 为 43.2/48.6。长推理在若干 STEM 任务有益，但感知、OCR 与定位并不统一改善，不能把这两种后训练模式排成单一等级。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=15|p15 Table 2]]

工具结果同样要看列条件：V* 的 85.9 是 Thinking 无加号列，93.7 是 Instruct 带工具列，不能相减后称为同一 checkpoint 的纯工具增益。HRBench 的加号也标记工具使用。GUI grounding（ScreenSpot、OSWorld-G）与在线任务（OSWorld、AndroidWorld）测量不同；例如附录 grounding 提示只允许鼠标移动/点击，不能据此假定完整在线任务也只有这两个动作。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=15|p15 Table 2]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=20|p20 §5.10]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=42|p42 Appendix B.11]]

定位评估还有容易忽略的条件：ODinW 提示一次列出类别，将预测置信度统一设为 1 后计算 mAP；3D 使用 Omni3D 协议和 IoU 0.15，也将置信度设为 1。这既不是通常直觉中的 IoU 0.5，也不是机器人执行成功率。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=19|p19 §5.5]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=37|p37 提示]]

### 3.2 视频比较：输入预算本身会影响胜负

视频评估最多 2,048 帧、总视觉 token 不超过 224K；VideoMMMU/MMVU 每帧最多 768 tokens，其余 640。Charades-STA 取 4 fps，其余 2 fps。受接口限制，作者对 Gemini 2.5 Pro、GPT-5、Claude Opus 4.1 分别最多输入 512、256、100 帧，并明确承认不能保证完全公平。VideoMMMU 改用模型评分，因为规则评分被认为不够准确；报告未给评审器与人工一致性的量化校准。以上约束是结果的一部分，不能仅比较视频分数。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=20|p20 §5.9]]

### 3.3 文本能力保留：必须绑定基线版本与生成预算

报告的文本测试对大小模型及 Thinking/Instruct 使用不同 temperature、top-p、top-k 和 presence penalty；默认最大输出 32,768，Thinking 的 AIME/HMMT/LiveCodeBench 扩至 81,920。该设置位于 **text-centric tasks**，不能无依据推广为所有视觉测试的统一参数。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=20|p20–21 §5.11]]

以旗舰为例，Instruct 相对 Qwen3-235B-A22B-Instruct-2507 在 AIME-25 为 74.7 对 70.3，但 MMLU-Pro 为 81.8 对 83.0、GPQA 为 74.3 对 77.5。Thinking 相对相应 2507 文本模型的 GPQA 为 77.1 对 81.1、AIME 为 89.7 对 92.3。因此“多模态训练保留并可促进文本能力”是需要按规模、任务及基线版本限定的判断，不能改写为所有文本指标均提升。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=21|p21–22 Tables 5–7]]

### 3.4 两类消融与三个自建评测的证据强度

视觉编码器消融统一配 1.7B Qwen3 并训练 1.5T tokens：Qwen3-ViT 相对 SigLIP2 的 RealWorldQA 为 66.1 对 58.7，内部 OmniBench 53.0 对 50.1；但 ImageNet-R 为 95.7 对 96.1、ImageNet-Sketch 为 74.5 对 76.2。视觉语言能力的改善没有要求所有纯视觉迁移指标同步提高。该比较与前述 DeepStack 消融分别使用不同语言骨干和训练预算，不能合并为同一实验。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=24|p24 §5.12.1–5.12.2、Tables 11–12]]

| 内部测试 | 原文实际测量 | 可以支持什么 | 尚缺什么 |
| --- | --- | --- | --- |
| 多语言 OCR | 39 个非中英语言的自建集；32 个语言准确率超过 70% | 该测试中语言覆盖扩大 | 每语言样本量、标签/判分细节、人类校准；70% 是作者选定实用阈值 |
| OmniBench | 视觉编码器消融表内的内部指标 | 相同配套训练下表内比较 | 足够完整的数据构建及评分协议，无法独立解释其全部能力含义 |
| 视频 NIAH | 插入含目标语义的 needle 帧，改变视频长度与插入深度；1 fps、动态分辨率 | 指定模型在此检索诊断中能找回目标 | 样本数、needle 多样性、完整判分及人类一致性；不等于长视频因果推理 |

OCR 见 [[raw/papers/models/qwen/Qwen3-VL.pdf#page=17|p17 §5.4、Figure 2]]；OmniBench 见 [[raw/papers/models/qwen/Qwen3-VL.pdf#page=24|p24 Table 11]]；NIAH 见 [[raw/papers/models/qwen/Qwen3-VL.pdf#page=25|p25 §5.12.3、Figure 3]]。这些自建测试的协议缺口不应由本库自行补齐。

NIAH 在 235B-A22B-Instruct 上报告 256K、约 30 分钟范围内 100% retrieval；通过 YaRN 扩到约 1M、两小时后为 99.5%。**原生窗口是 256K，约 1M 是扩展设置**。正文同时写到固定视觉 token 预算与长度变化，未交代足以复现其具体分配方式，本页保留这一实施细节未知。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=25|p25 §5.12.3]]

## 4. 原文内部差异、旧笔记修正与未解问题

原文有少量叙述与表格不一致：§5.1 对 32B Thinking 的 RealWorldQA 叙述为 79.4，但 Table 3 为 78.4；HRBench 旗舰带工具的正文为 85.3/82.3，Table 2 为 85.4/82.4。本页采用明确表格列作结果引用，同时保留差异，未擅自判定哪个是作者最终正确数值。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=14|p14 §5.1]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=16|p16 Table 3]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=19|p19 §5.7]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=15|p15 Table 2]]

旧总结有价值的主线是中间层视觉特征、训练四阶段和多模态后训练。本页补足了实验条件与反例，并把代码级细节降为未核查输入。报告未公开全部奖励实现，不等于可以断言作者“因为保密”而不公开；模型估计工具调用预算也不能写成人工专家标准。旧总结对后来模型的主观比较未作为本报告证据。

仍值得追问：交错位置频率与显式时间戳分别贡献多少；多层注入是否在低预算或更长视频下仍有益；工具使用奖励如何避免“正确次数、错误区域”；模型评审的偏差会怎样影响视频与代码结果。当前报告没有提供足以逐项回答的独立对照。Design2Code 附录采用模型比较参考图与渲染图的视觉相似度，不等于 HTML/CSS 的交互功能测试。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=41|p41–42 Appendix B.10]]

## 5. 本库关联

与 [[wiki/papers/models/qwen/Qwen2-VL|S027 Qwen2-VL]] 可沿“动态分辨率→位置编码→视频预算”比较；与 [[wiki/papers/models/qwen/Qwen-VL|S026 Qwen-VL]] 可沿“固定 256-query 压缩→动态 token→多层注入”比较。后者是本库跨来源综合路线，不是报告自己做过的统一消融。主题整合建议为位置编码、视觉连接器、长视频评估和多模态后训练；实际共享主题已写入，最终摄入验收仍由主协调者完成。

## 实际整合关系

支撑DeepStack、交错位置/时间戳与长上下文课程，区分Thinking/工具训练、视频预算和检索诊断。

- [[wiki/vision/Resolution-and-Token-Budget|分辨率、packing与tiling：预算到底在哪个位置？]]。
- [[wiki/architecture/Visibility-and-Connections|可见性、路由与连接：视觉信息在哪里与语言相遇？]]。
- [[wiki/training/Supervision-and-Stages|监督与阶段：数据、目标、开放参数和预算如何一起改变？]]。
- [[wiki/reasoning/Overview|推理与交互：增加计算、改变观察、控制环境怎样分别起作用？]]。
- [[wiki/evaluation/Judges-and-Task-Success|裁判与任务成功：答案、解释、生成物和终态怎样分别取证？]]。
- [[wiki/models/Family-Changes|家族变化轴：输入、接口、数据和计算怎样共同演进？]]。
