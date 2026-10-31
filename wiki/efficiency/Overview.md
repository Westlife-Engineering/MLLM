---
type: overview
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf]]"
  - "[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]"
  - "[[raw/lectures/VLM-2.pdf]]"
---

# 效率：先确定成本发生在哪里

高效 MLLM 不能只按参数量排序。小骨干、视觉 token 压缩、稀疏专家、KV 共享和少更新参数，分别改变不同资源；任务质量还可能随输入细节和生成预算变化。**本页把效率读成“在给定任务质量与条件下，减少哪段资源消耗”**，这是依据 S001 多章节及 S002/S003 预算个案形成的本库阅读框架。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=4|S001 · §2 · pp.4–10]] [[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=14|S001 · §4–5 · pp.14–19]]

## 一份可重复使用的成本账本

| 成本位置 | 至少记录什么 | 哪类改动主要作用于此 |
| --- | --- | --- |
| 输入和视觉前端 | 分辨率、视图/帧数、encoder、前端耗时 | resize、原生分辨率、多尺度、视觉骨干压缩 |
| 跨模态接口 | 输入/输出视觉 token、query、merger、额外网络计算 | 连接器聚合、重采样、合并 |
| LLM 输入处理 | 视觉与文本总长度、结构、激活计算 | token 压缩、稀疏专家、不同序列骨干 |
| 自回归生成 | 输出长度、KV 配置、解码策略、内存与延迟 | KV 共享、推测解码、减少无效生成 |
| 训练 | 开放参数、梯度/优化器状态、累计 token、硬件与时间 | 冻结、PEFT、优化器、数据和阶段组织 |
| 推理系统 | 候选数、搜索节点、工具调用、失败重试、墙钟时间 | best-of-N、搜索、裁剪/检索/代码工具 |

这是本库账本，**不是 S001 已完成的统一测量表**。前五行的机制依据是 S001 §2、4、5，最后一行依据 S002 长推理与工具讨论。不同列不能只用一个 token 总数替代。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=6|S001 · §2.2–2.5 · pp.6–10]] [[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=14|§4–5 · pp.14–19]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=15|S002 · §3.3 · pp.15–19]]

## 少 token、少激活与少更新改变不同量

视觉 token 减少会缩短接口输出或后续层的序列；更小的 LLM 主要改变权重规模；稀疏 MoE 区分总参数与每次激活参数；GQA/MQA 共享的是 KV 头。即使某方法在其中一列更小，路由、通信、压缩和硬件实现仍会影响实测延迟。**参数统计与理论复杂度适合解释成本来源，不能代替端到端测量。**[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=7|S001 · §2.3–2.5 · pp.7–10]] [[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=14|S001 · §4.1、Fig.12 · pp.14–15]]

少更新参数属于训练账本：冻结骨干仍需参与前向，PEFT 的 trainable parameters 不代表总权重消失，也不直接确定推理速度。S001 对 LoRA、Adapter 等个别解释存在疑点，相关句子没有在这里沿用成定义；具体疑点保留在唯一综述页。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=16|S001 · §4.3、§5.4 · pp.16–19]] [[wiki/surveys/Efficient Multimodal Large Language Models A Survey#语言侧效率：小模型、少激活、少搬运与少更新不是一回事|S001 的机制与原文疑点]]

## 压缩可能转移成本

S2 在不同尺度上重复使用同一个视觉模型，再合并、池化和拼接。parameter-free 表示该包装不额外训练参数，图中多条编码路径仍有计算。整图加 tiles 同样可能先增加前端工作，再用 merger 减少 LLM 输入。**本库综合：**报告压缩比例时应注明它相对哪个位置的 token，计算是否包括生成压缩特征的视觉前端。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=9|S001 · Fig.7 · p.9]] [[raw/lectures/VLM-2.pdf#page=68|S003 · DeepSeek-VL2 · p.68]]

注意力的两两交互随序列长度增加而迅速增长，是 S001 讨论视觉 token 压力的理由；这一描述有特定算子与序列条件，不能写成整个多模态系统所有成本都按图片边长同一幂次增长。视频还同时增加帧数、时间结构和上下文负担，需回到账本逐项看。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=7|S001 · §2.4 · pp.7–9]] [[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=14|§4.1 · p.14]]

## 质量和预算要成对报告

S002 图6标注一次 o3 reasoning 用时8分13秒；它展示裁剪、修正观察和解题的过程，但没有预算曲线或控制消融，不能证明计算越多越好。S003 的 Toggle 图同时标出5项成绩提升、2项下降及7项 token 使用减少，恰好提醒成本降低和质量变化可以同时出现，且该页未给完整可复现协议。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=26|S002 · §4.1、Fig.6 · p.26]] [[raw/lectures/VLM-2.pdf#page=82|S003 · Toggle · p.82]]

S001 Table 4 主要列能力分数，没有统一硬件、延迟、显存和能耗字段。因此它支持寻找需要进一步核查的模型设置，不能直接形成“同等预算下最高效”的结论。进入 [[wiki/evaluation/Overview|评测页]] 先核任务、划分与判分，再比较质量—成本关系。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=22|S001 · §6.3、Table 4 · pp.21–22]]

来源入口：[[wiki/surveys/Efficient Multimodal Large Language Models A Survey|S001]] · [[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models|S002]] · [[wiki/lectures/VLM-2|S003]]。返回 [[wiki/overview|总览]]；本库未测模型速度，Obsidian 内显示未测。
