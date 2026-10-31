---
type: overview
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf]]"
  - "[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]"
  - "[[raw/lectures/VLM-2.pdf]]"
---

# 训练：数据、目标、开放参数与预算一起读

“两阶段训练”“端到端”“使用 RL”都不是充分的训练描述。要理解能力怎样形成，至少同时记录**监督材料、预测目标、可训练模块和输入/计算预算**。同一损失可以服务不同阶段，同一结构也可在不同阶段改变冻结范围。下文以 S001 的训练地图、S003 的教学实例和 S002 的推理训练分类建立阅读框架，具体模型仍保留转述身份。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=18|S001 · §5、Fig.14 · pp.18–19]] [[raw/lectures/VLM-2.pdf#page=30|S003 · LLaVA · p.30]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=16|S002 · §3.3、Fig.5 · pp.16–19]]

## 训练目标约束什么

| 监督 / 目标 | 学习时要求模型做什么 | 容易混淆的边界 |
| --- | --- | --- |
| 图文对比（contrastive） | 让匹配图文的表示比不匹配项更相容 | 全局表示对齐不等于每个局部都可定位 |
| 图文匹配（matching） | 在图文交互表示上判断是否配对 | 不等于可以预先独立算完两塔所有任务分数 |
| 掩码建模（masked modeling） | 用可见上下文恢复被遮挡信息 | mask 和可用上下文决定任务，不能只看同一目标名 |
| 条件生成 / 自回归监督 | 在图像、指令及输出前缀条件下预测后续文本 | 学会回答格式不能单独证明解释忠实或任务完成 |
| 偏好 / 奖励优化 | 用偏好对或奖励改变输出分布与选择倾向 | 信号测到了什么，决定优化实际鼓励什么 |

前四行据课程 VLMo、BEiT-3 与 BLIP-2 整理；最后一行据 S002 的 DPO、GRPO 与奖励类型示意。表是目标层次的比较，不是将不同算法归成同一个损失。[[raw/lectures/VLM-2.pdf#page=5|S003 · pp.5、8–9、22]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=16|S002 · Fig.5、§3.3.2–3.3.3 · pp.16–19]]

## 阶段名后面还要补四列

S001 的典型流程先用图文对学习接口，再做 instruction-tuning，后者可以沿用相同自回归训练目标。训练的差别在数据内容、参数开放范围和希望形成的行为，不能用“预训练/微调”两个词代替。Fig.14 也只是典型图，正文列出开放更多参数、按分辨率分阶段和单阶段等变体。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=18|S001 · §5.1–5.3、Eq.4–5 · pp.18–19]]

| 阶段阅读项 | 要写清的内容 | 课程中揭示区别的例子 |
| --- | --- | --- |
| 数据 | 图文对、交错图文、纯文本、任务 QA、长文档/视频 | Qwen-VL 随阶段改变数据与分辨率，p.55 |
| 目标与监督位置 | 对比、生成、指令答案；哪些位置计算 loss | CogVLM 的 REC 将坐标作为答案，loss 仅在 Answer，p.75 |
| 参数范围 | encoder、connector、LLM；全开、部分开或冻结 | LLaVA 第二阶段仍冻结视觉编码器，p.30 |
| 输入与预算 | 分辨率、最大序列长度、累计 token、样本、步数、batch | Qwen3-VL 的 token budget 与 sequence length 分两列，p.62 |

定位：[[raw/lectures/VLM-2.pdf#page=55|S003 · p.55]]、[[raw/lectures/VLM-2.pdf#page=75|p.75]]、[[raw/lectures/VLM-2.pdf#page=30|p.30]]、[[raw/lectures/VLM-2.pdf#page=62|p.62]]。这些是课程嵌入的训练信息，未在此页升级为官方实现核验。

## 冻结策略没有通用答案

冻结强骨干、训练轻量接口，可减少被更新的参数并复用已有表征；但它是否足以建立目标任务的对齐，依赖数据、骨干和所需视觉细节。S001 正文在常见 projector-only 方案之后就讨论开放更多视觉/语言参数的变体，因而不能将 Fig.14 解释成所有 MLLM 的标准冻结规则。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=18|S001 · Which part to unfreeze? · p.18]]

课程给出可直接对照的差别：DeepSeek-VL 第一阶段只训练 adaptor；DeepSeek-VL2 第一阶段明确训练视觉编码器与 adaptor MLP、冻结语言模型。同是“对齐阶段”，开放范围已不同。这里支持的是课程对两个方案的叙述不同，不能在没有预算匹配消融时断言哪种冻结策略更优。[[raw/lectures/VLM-2.pdf#page=65|S003 · DeepSeek-VL · p.65]] [[raw/lectures/VLM-2.pdf#page=70|S003 · DeepSeek-VL2 · p.70]]

## 数据规模与计算量的单位要保留

S001 数据表同时使用 images、texts、pairs 和 instances；一个交错 instance 可能含多个图文元素。S003 SigLIP 2 又把原始数据规模与累计处理 examples 分开。由此形成的本库记录原则是：不把不同单位相加，不从数据集总量推出模型实际见过的唯一图像数，不把累计 token budget 当最大上下文长度。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=20|S001 · §6.1–6.2、Tables 2–3 · pp.20–21]] [[raw/lectures/VLM-2.pdf#page=86|S003 · SigLIP 2 · p.86]] [[raw/lectures/VLM-2.pdf#page=62|S003 · p.62]]

推理训练还须追问信号：格式奖励、终答奖励、IoU、长度惩罚和模型奖励不会自动评价同一项真实目标。S002 归纳的 R1-like 工作含多种优化方法，不能把标签等同于 GRPO，也不能由数学任务提升推定一般多模态推理迁移。训练如何与运行时搜索、工具配合，见 [[wiki/reasoning/Overview|推理与交互]]；资源核算见 [[wiki/efficiency/Overview|效率]]。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=16|S002 · §3.3.2–3.3.3、Table 6 · pp.16–19]]

来源入口：[[wiki/surveys/Efficient Multimodal Large Language Models A Survey|S001]] · [[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models|S002]] · [[wiki/lectures/VLM-2|S003]]。返回 [[wiki/overview|总览]]；Obsidian 内显示未测。
