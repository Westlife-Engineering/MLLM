# MLLM Wiki：阅读入口

本库围绕视觉—语言研究建立可回证的机制笔记：来源页保存身份、实际阅读范围和原件定位，主题页承担跨来源解释。**本轮初始化已完成：34项来源均已形成阅读页、整合主题，并通过独立内容审查、图文与结构验收，状态为read / complete。** read仅覆盖各页登记的实际阅读范围，不表示全部附录、代码和引文都已核读；未复现实验，Obsidian内显示与PDF跳转未实测。

## 材料与来源计数

| 口径 | 当前事实 |
| --- | --- |
| 用户原始文件 | 261份，完整笔记包/原论文/综述/讲义等，不等于261篇论文 |
| Raw文件 | 288份 = 261原始文件 + 1理念文章 + 26新增证据文件 |
| 旧独立材料工作对象 | 31个；InternViT/InternVL共一学术身份，V4.1两总结共一报告 |
| 去重学术来源 | 31项 = 29论文/报告 + 2综述 |
| 其他登记来源 | 1讲义 + 2官方文档 |
| 来源登记/唯一来源页 | 34项，S001–S034；全部read / complete |
| 当前Wiki知识页 | 52页 = 18总览/主题 + 34唯一来源页；索引、日志与图资产不计知识页 |

计数依据：[[maintenance/migrations/2026-10-31-initialization.json|迁移清单]]、[[maintenance/source-registry.json|来源登记]]；队列与审查记录见[[maintenance/research/R001-initialization|R001维护记录]]。原始文件、工作对象、学术身份与其他来源分别计数。

## 主题地图与阅读路线

初读“基础→视觉→架构→训练”；评估结果接“效率→评测”；讨论工具、Agent与长序列接推理、序列记忆与家族变化。音频、3D及范围外工作在地图材料中的出现不表示另有一手论文覆盖。

| 页面 | 一句话入口 |
| --- | --- |
| [[wiki/overview\|MLLM：沿视觉证据、学习接口与任务结果建立理解]] | 沿视觉证据、接口、学习与任务结果串起八个阅读视角。 |
| [[wiki/foundations/Formalization\|基础：把信息、参数与任务证据分成三个层次]] | 建立token、冻结、共享、可见性与能力证据的工作语言。 |
| [[wiki/vision/Overview\|视觉表示：从监督、输入保真到下游可读性]] | 视觉监督、输入保真与下游可读性的地图。 |
| [[wiki/vision/Objectives-and-Transfer\|视觉预训练：目标要求保留什么，迁移又读取什么？]] | 比较分类/对比/生成/局部目标及不同迁移读出。 |
| [[wiki/vision/Resolution-and-Token-Budget\|分辨率、packing与tiling：预算到底在哪个位置？]] | 分清native、packing、tiling与压缩位置，核单图/多图预算。 |
| [[wiki/architecture/Overview\|架构：分开读取权重、可见性、路由与输出接口]] | 以权重、可见性、路由与输出职责组织架构问题。 |
| [[wiki/architecture/Visibility-and-Connections\|可见性、路由与连接：视觉信息在哪里与语言相遇？]] | 解释独立/融合表示及Flamingo、BLIP-2、LLaVA等接入通路。 |
| [[wiki/architecture/Generative-Output-Interfaces\|生成输出接口：读入图片、输出文字、合成图片分别由谁完成？]] | 分开输入视觉特征、文字/坐标、输出vokens和扩散条件。 |
| [[wiki/architecture/Sequence-Memory-and-Retrieval\|序列记忆与检索：固定状态、稀疏KV、残差流和查表容量分别保存什么？]] | 比较固定状态、稀疏KV、残差流与host参数记忆。 |
| [[wiki/training/Overview\|训练与数据：监督怎样穿过接口，更新哪些参数？]] | 用监督、开放参数和预算读取训练路线。 |
| [[wiki/training/Supervision-and-Stages\|监督与阶段：数据、目标、开放参数和预算如何一起改变？]] | 连起目标、EMA/语料自举、指令、冻结、模态比例与奖励环境。 |
| [[wiki/efficiency/Overview\|效率与成本：用资源对象解释节省，用任务质量限定收益]] | 按资源对象与任务质量进入效率比较。 |
| [[wiki/efficiency/Resource-Ledger\|资源账本：视觉token、激活参数、KV与系统预算分别省在哪里？]] | 分账视觉、激活/存储、prefill/decode、cache、训练与系统循环。 |
| [[wiki/reasoning/Overview\|推理与交互：增加计算、改变观察、控制环境怎样分别起作用？]] | 分开继续计算、新观察、动作—反馈与effort成本偏好。 |
| [[wiki/evaluation/Overview\|评测与证据：任务对象、判分和预算一起决定分数]] | 以任务对象、判分与输入/计算条件约束分数解释。 |
| [[wiki/evaluation/Judges-and-Task-Success\|裁判与任务成功：答案、解释、生成物和终态怎样分别取证？]] | 区分模型裁判/人评、代理指标、转写、检索和真实终态。 |
| [[wiki/models/Overview\|模型演进：按机制变化轴进入家族，按证据条件读结果]] | 按变化轴进入家族，并保持论文/官方文档版本身份。 |
| [[wiki/models/Family-Changes\|家族变化轴：输入、接口、数据和计算怎样共同演进？]] | 跨LLaVA、Qwen、DeepSeek与InternVL比较联合变化及证据条件。 |

## 综述与讲义

三项地图来源保留综述/课程转述身份；已有独立原论文者从其唯一页核直接证据，不将地图阅读计为被引论文精读。

| ID与唯一页 | 摘要 | 主方向 / 实际交叉视角 | 阅读 / 摄入 |
| --- | --- | --- | --- |
| S001 · [[wiki/surveys/Efficient Multimodal Large Language Models A Survey\|Efficient-MLLM-Survey]] | 按组件、训练和数据组织效率地图，保留汇表条件与原文疑点。 | survey（不设技术主方向）；foundations、efficiency、evaluation | read / complete |
| S002 · [[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models\|Multimodal-Reasoning-Survey]] | 梳理多模态推理、工具/环境与判分，分开作者个案和路线展望。 | survey（不设技术主方向）；reasoning、evaluation、architecture | read / complete |
| S003 · [[wiki/lectures/VLM-2\|VLM-2]] | 92页课程入口，串起共享/专用参数、连接、位置、家族与课程勘误。 | lecture（不设技术主方向）；architecture、reasoning、models | read / complete |

## 论文与官方文档：按唯一主归属导航

技术交叉方向仅记录已发生的正式目录关系；实际主题视角由机制综合和双向链接承接，不为它们另复制来源正文。下表性能/机制摘要均以固定原件版本为边界。

### vision/encoders

| ID与唯一页 | 类型与摘要 | 主方向 / 已登记技术交叉方向 | 实际主题视角 | 阅读 / 摄入 |
| --- | --- | --- | --- | --- |
| S004 · [[wiki/papers/vision/encoders/ViT\|ViT]] | paper；以patch Transformer研究大规模监督分类与迁移，限定数据/读出条件。 | vision/encoders；交叉：无另登记 | vision、foundations | read / complete |
| S005 · [[wiki/papers/vision/encoders/SoViT\|SoViT]] | paper；以固定计算研究width/depth/MLP/训练时长的形状分配。 | vision/encoders；交叉：无另登记 | vision、efficiency、evaluation | read / complete |
| S006 · [[wiki/papers/vision/encoders/NaViT\|NaViT]] | paper；用样本隔离的Patch n’ Pack组织保比例、混合分辨率训练。 | vision/encoders；交叉：无另登记 | vision、efficiency | read / complete |
| S007 · [[wiki/papers/vision/encoders/AIMv2\|AIMv2]] | paper；用prefix图像/文本自回归目标训练可迁移视觉编码器。 | vision/encoders；交叉：architecture/pretraining、vision/alignment | vision、evaluation、training | read / complete |

### vision/alignment

| ID与唯一页 | 类型与摘要 | 主方向 / 已登记技术交叉方向 | 实际主题视角 | 阅读 / 摄入 |
| --- | --- | --- | --- | --- |
| S008 · [[wiki/papers/vision/alignment/CLIP\|CLIP]] | paper；以批内双向配对学习图文空间，再由类别文字构造分类接口。 | vision/alignment；交叉：vision/encoders | vision | read / complete |
| S009 · [[wiki/papers/vision/alignment/SigLIP\|SigLIP]] | paper；将跨候选softmax改为逐对sigmoid，研究batch/负例与分块计算。 | vision/alignment；交叉：无另登记 | vision、efficiency | read / complete |
| S010 · [[wiki/papers/vision/alignment/SigLIP2\|SigLIP2]] | paper；组合全局、区域与密集监督，并区分固定分辨率/NaFlex/蒸馏分支。 | vision/alignment；交叉：vision/encoders | vision、training | read / complete |

### architecture/pretraining

| ID与唯一页 | 类型与摘要 | 主方向 / 已登记技术交叉方向 | 实际主题视角 | 阅读 / 摄入 |
| --- | --- | --- | --- | --- |
| S011 · [[wiki/papers/architecture/pretraining/ALBEF\|ALBEF]] | paper；以ITC、融合ITM/MLM与EMA软目标联合学习对齐和条件理解。 | architecture/pretraining；交叉：vision/alignment | architecture、training、evaluation、models | read / complete |
| S012 · [[wiki/papers/architecture/pretraining/BLIP\|BLIP]] | paper；以MED共享/专用路径和CapFilt语料自举连接理解与生成。 | architecture/pretraining；交叉：vision/alignment、architecture/generation | architecture、training、evaluation、models | read / complete |
| S013 · [[wiki/papers/architecture/pretraining/CoCa\|CoCa]] | paper；把causal decoder分为纯文本/视觉条件两段，兼顾对比与caption。 | architecture/pretraining；交叉：vision/alignment、architecture/generation | architecture、vision、evaluation、models | read / complete |
| S014 · [[wiki/papers/architecture/pretraining/VLMo\|VLMo]] | paper；共享attention并按模态/层路由FFN，形成双塔和融合路径。 | architecture/pretraining；交叉：vision/alignment | architecture、training、foundations、models | read / complete |
| S015 · [[wiki/papers/architecture/pretraining/BEiT-v3\|BEiT-v3]] | paper；以multiway骨干和MDM统一预训练，任务适配仍改变接口/目标。 | architecture/pretraining；交叉：vision/encoders、vision/alignment | architecture、training、foundations、evaluation、models | read / complete |

### architecture/connectors

| ID与唯一页 | 类型与摘要 | 主方向 / 已登记技术交叉方向 | 实际主题视角 | 阅读 / 摄入 |
| --- | --- | --- | --- | --- |
| S016 · [[wiki/papers/architecture/connectors/Flamingo\|Flamingo]] | paper；以64-latent重采样和LM内部gated CA接入交错图文/视频。 | architecture/connectors；交叉：architecture/pretraining | architecture、foundations、models | read / complete |
| S017 · [[wiki/papers/architecture/connectors/BLIP-2\|BLIP-2]] | paper；以三目标mask训练Q-Former，再接冻结LLM视觉前缀。 | architecture/connectors；交叉：architecture/pretraining | architecture、training、efficiency、foundations、models | read / complete |
| S018 · [[wiki/papers/architecture/connectors/InstructBLIP\|InstructBLIP]] | paper；使指令在视觉提取阶段生效，研究多任务与留出泛化。 | architecture/connectors；交叉：architecture/pretraining | architecture、training、evaluation、models | read / complete |
| S019 · [[wiki/papers/architecture/connectors/MiniGPT-4\|MiniGPT-4]] | paper；复用冻结视觉桥与Vicuna，训练线性接口并用精炼长描述改善输出。 | architecture/connectors；交叉：无另登记 | architecture、training、evaluation、models | read / complete |
| S020 · [[wiki/papers/architecture/connectors/mPLUG-Owl\|mPLUG-Owl]] | paper；以视觉abstractor与阶段参数调整构建视觉助手，保留v3冲突与OwlEval边界。 | architecture/connectors；交叉：无另登记 | architecture、training、evaluation、models | read / complete |

### architecture/generation

| ID与唯一页 | 类型与摘要 | 主方向 / 已登记技术交叉方向 | 实际主题视角 | 阅读 / 摄入 |
| --- | --- | --- | --- | --- |
| S021 · [[wiki/papers/architecture/generation/MiniGPT-5\|MiniGPT-5]] | paper；以生成vokens和mapper把交错文字输出接到扩散图像生成。 | architecture/generation；交叉：无另登记 | architecture、training、evaluation、foundations、reasoning、models | read / complete |

### models/llava

| ID与唯一页 | 类型与摘要 | 主方向 / 已登记技术交叉方向 | 实际主题视角 | 阅读 / 摄入 |
| --- | --- | --- | --- | --- |
| S022 · [[wiki/papers/models/llava/LLaVA\|LLaVA]] | paper；用文字教师的视觉指令数据训练线性网格接口，区分评分裁判和系统内judge。 | models/llava；交叉：architecture/connectors | architecture、training、evaluation、models、foundations | read / complete |
| S023 · [[wiki/papers/models/llava/LLaVA-1.5\|LLaVA-1.5]] | paper；将MLP、格式指令、任务数据和336基线组合，并另测HD局部/全局视图。 | models/llava；交叉：architecture/connectors、vision/encoders | architecture、training、models | read / complete |
| S024 · [[wiki/sources/models/llava/LLaVA-NeXT\|LLaVA-NeXT]] | source；2024年1月官方技术说明快照，记录336-AnyRes、数据与模型卡变化。 | models/llava；交叉：architecture/connectors、vision/encoders | vision、training、models、efficiency | read / complete |

### models/internvl

| ID与唯一页 | 类型与摘要 | 主方向 / 已登记技术交叉方向 | 实际主题视角 | 阅读 / 摄入 |
| --- | --- | --- | --- | --- |
| S025 · [[wiki/papers/models/internvl/InternVL\|InternVL]] | paper；扩展InternViT并以QLLaMA渐进对齐，区分独立表示与直接/query Chat。 | models/internvl；交叉：vision/encoders、vision/alignment、architecture/connectors | vision、architecture、efficiency、models、training | read / complete |

### models/qwen

| ID与唯一页 | 类型与摘要 | 主方向 / 已登记技术交叉方向 | 实际主题视角 | 阅读 / 摄入 |
| --- | --- | --- | --- | --- |
| S026 · [[wiki/papers/models/qwen/Qwen-VL\|Qwen-VL]] | paper；以固定256-query位置感知接口和细粒度多任务建立Qwen视觉输入。 | models/qwen；交叉：vision/encoders、architecture/connectors | vision、training、architecture、models、foundations | read / complete |
| S027 · [[wiki/papers/models/qwen/Qwen2-VL\|Qwen2-VL]] | paper；以动态空间token和M-RoPE统一图像/视频，区分工具与终态测量。 | models/qwen；交叉：vision/encoders、architecture/connectors | vision、reasoning、evaluation、foundations、models | read / complete |
| S028 · [[wiki/papers/models/qwen/Qwen3-VL\|Qwen3-VL]] | paper；以DeepStack、交错位置与时间戳发展长多模态序列及后训练。 | models/qwen；交叉：vision/encoders、architecture/connectors | vision、architecture、training、reasoning、evaluation、models | read / complete |
| S029 · [[wiki/sources/models/qwen/Qwen-3.5\|Qwen-3.5]] | source；固定官方模型卡/配置，确认hybrid/MoE/视觉字段与原生/外推上下文。 | models/qwen；交叉：architecture/connectors | architecture、efficiency、models | read / complete |
| S030 · [[wiki/papers/models/qwen/Qwen3.8-Flash-Next\|Qwen3.8-Flash-Next]] | paper；语言骨干报告，联合研究GDN/QSA/GR/host查表/优化与代理测量。 | models/qwen；交叉：architecture/pretraining | architecture、efficiency、models、evaluation、reasoning | read / complete |

### models/deepseek

| ID与唯一页 | 类型与摘要 | 主方向 / 已登记技术交叉方向 | 实际主题视角 | 阅读 / 摄入 |
| --- | --- | --- | --- | --- |
| S031 · [[wiki/papers/models/deepseek/DeepSeek-VL\|DeepSeek-VL]] | paper；以双视觉通道融合保持576位置，并通过阶段/模态比例控制语言遗忘。 | models/deepseek；交叉：vision/encoders、architecture/connectors | vision、training、models | read / complete |
| S032 · [[wiki/papers/models/deepseek/DeepSeek-VL2\|DeepSeek-VL2]] | paper；以动态tiles、稀疏MoE和部分型号MLA组织视觉细节与后端成本。 | models/deepseek；交叉：vision/encoders、architecture/connectors | vision、efficiency、training、models、architecture、foundations | read / complete |
| S033 · [[wiki/papers/models/deepseek/DeepSeek-OCR\|DeepSeek-OCR]] | paper；以压缩视觉编码做领域转写/解析，光学长上下文推理仍待验证。 | models/deepseek；交叉：vision/encoders、architecture/connectors | vision、efficiency、evaluation、reasoning、models、training | read / complete |
| S034 · [[wiki/papers/models/deepseek/DeepSeek-V4.1-Flash\|DeepSeek-V4.1-Flash]] | paper；以CED、CSA2、低比特/重放cache和训练系统降低长会话资源开销。 | models/deepseek；交叉：vision/encoders、architecture/connectors、architecture/pretraining | architecture、efficiency、training、reasoning、evaluation、models | read / complete |

旧TeX/PDF/Markdown冻结在Raw，只作为旧理解输入；新正文修订在Wiki。维护入口为[[AGENTS|AGENTS]]；历史操作见[[wiki/log|追加日志]]。后续新增材料依摄入工作流更新唯一来源页、实质主题关系与本索引；本轮验收范围和记录见R001。
