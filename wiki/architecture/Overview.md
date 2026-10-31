---
type: overview
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf]]"
  - "[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]"
  - "[[raw/lectures/VLM-2.pdf]]"
---

# 架构：共享什么，在哪里交换信息

比较多模态架构，先把三个问题拆开：**参数是否共享、一次前向中哪些 token 能相互读取、视觉适配发生在什么位置。** “统一”“专家”“连接器”只回答其中部分问题。S001 给常见组件框架，S003 提供共享/专用参数与接口实例；下文具体模型仍为综述或讲义转述。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=4|S001 · §2 · pp.4–7]] [[raw/lectures/VLM-2.pdf#page=4|S003 · VLMo · pp.4–7]]

## 共享参数不等于每次都融合信息

讲义 VLMo 的不同模态复用注意力参数，FFN 按模态 hard routing。图文对比学习可分别编码图像与文本，融合任务才让联合序列在内部交互；检索可用双塔，分类可用单塔。**参数共享描述模型怎样复用权重，token 可见性描述当前计算能访问什么信息。** 两者须分别画、分别读。[[raw/lectures/VLM-2.pdf#page=4|S003 · VLMo · pp.4–7]]

课程 BEiT-3 进一步把掩码建模框架用于图像、文字和图文，同时展示视觉编码器、语言编码器、融合、双编码器与生成等用法。“统一预训练”并未消除下游任务的 mask、输出头和推理流程差异。[[raw/lectures/VLM-2.pdf#page=8|S003 · BEiT-3 · pp.8–9]]

## 接口位置与信息选择

| 接口组织 | 信息怎样传递 | 阅读时要检查什么 |
| --- | --- | --- |
| 输入端线性 / MLP 投影 | 将视觉特征映射到语言模型可接受的嵌入维度 | 是否同时改 token 数，视觉空间结构怎样保留 |
| 可学习 query 与 cross-attention | 少量 query 从视觉特征读取信息 | query 数、可见范围、是否受任务指令影响 |
| LLM 内部视觉专用参数 | 视觉位置用专用投影 / FFN，再在组合序列交互 | 专用参数在哪些层，注意力如何跨模态 |
| 多深度视觉特征注入 | 不同深度视觉特征接向不同 LLM 层 | 接口数量、注入位置、是否额外保留输入视觉序列 |

表为本库机制重组：前两行依据 S001 §2.2 与讲义 BLIP-2 / LLaVA，后两行分别对应课程 CogVLM 与 DeepStack。接口越复杂不自动越好，收益仍依训练和任务。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=6|S001 · §2.2 · pp.6–7]] [[raw/lectures/VLM-2.pdf#page=22|S003 · pp.22–23]] [[raw/lectures/VLM-2.pdf#page=28|S003 · LLaVA · pp.28–30]] [[raw/lectures/VLM-2.pdf#page=74|S003 · p.74]] [[raw/lectures/VLM-2.pdf#page=60|S003 · p.60]]

**BLIP-2 的 mask 让“连接”更具体。** 课程图中 ITC 的 query/text 互不读取；ITM 全双向；生成 mask 让文本读 query 与过去文本，query 不读文本。连接器结构相同，不同 mask 就会改变可用于学习和预测的信息。InstructBLIP 再把指令输入 Q-Former，使视觉提取随任务变化，而非仅在 LLM 末端附加问题。[[raw/lectures/VLM-2.pdf#page=22|S003 · BLIP-2 masks · p.22]] [[raw/lectures/VLM-2.pdf#page=26|S003 · InstructBLIP · p.26]]

## “专家”按什么条件选择

VLMo 的模态 FFN 由 token 模态决定；CogVLM 的视觉位置使用专用 Q/K/V 和 FFN，并在组合序列上注意力交互；S001 的稀疏 MoE 则强调总容量与每次激活参数的区别。把三者统称“用了专家”会丢掉路由依据、共享对象和成本位置。[[raw/lectures/VLM-2.pdf#page=4|S003 · p.4]] [[raw/lectures/VLM-2.pdf#page=74|S003 · p.74]] [[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=9|S001 · §2.5 · p.9]]

训练范围是另一个轴。冻结视觉编码器/LLM、仅训练连接器，与使用哪种连接结构并非同一选择；同一接口也可以分阶段解冻。具体问题转到 [[wiki/training/Overview|训练页]]，避免由“adapter”名称推断全流程成本。

## 原生多模态是研究主张，还需落实到机制

S002 主张让模态信息持续参与推理、生成和环境交互，但同时讨论统一表示与模态专用 MoE。由此不能把 native 定义成“只有一个编码器”或“绝不使用工具”。更有用的比较是：中间信息用文字、图像还是其他表示；在哪些层交互；行动后新观察怎样回来。作者的 N-LMRM 在四阶段图中属于展望，不能给现有模型直接贴成熟度分数。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=5|S002 · §2、Fig.3 · pp.5–7]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=30|S002 · §4.3 · pp.30–31]]

来源入口：[[wiki/surveys/Efficient Multimodal Large Language Models A Survey|S001]] · [[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models|S002]] · [[wiki/lectures/VLM-2|S003]]。返回 [[wiki/overview|总览]]；Obsidian 内显示未测。
