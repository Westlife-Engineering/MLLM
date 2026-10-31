---
type: overview
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf]]"
  - "[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]"
  - "[[raw/lectures/VLM-2.pdf]]"
---

# 模型演进：按变化轴读一代改了什么

模型家族的代际变化往往同时涉及视觉输入、连接、语言骨干、数据、训练和任务范围。**家族名字能帮助定位材料，机制变化轴才能解释研究问题。** 本页先用已审课程与两份综述形成比较框架；模型细节保留讲义/综述转述身份，不是当前官方规格或性能排行榜。[[raw/lectures/VLM-2.pdf#page=48|S003 · Qwen VL 系列 · pp.48–63]] [[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=5|S001 · Table 1 · p.5]]

## 每一代至少沿六条轴看

| 变化轴 | 具体记录什么 | 它会怎样改变解释 |
| --- | --- | --- |
| 视觉输入 | 尺寸、长宽比、整图/tiles、多图、视频帧 | 模型可能先看到更多细节或时序信息 |
| 视觉表示与位置 | encoder、局部特征、空间/时间坐标 | 输入增多之后，还要保留各位置和时间关系 |
| 连接与融合 | query、MLP merger、cross-attention、跨层注入 | 视觉信息选择及进入语言计算的位置不同 |
| 语言与激活结构 | 骨干、dense/MoE、总/激活参数 | 容量、单次计算与部署负担的口径不同 |
| 训练 | 数据、目标、开放模块、上下文课程与预算 | 结构相同也可能因学习材料和开放参数而行为不同 |
| 输出与任务 | 问答、grounding、文档、长视频、thinking、工具交互 | 支持任务种类与任务可靠完成需分开验证 |

表为本库综合，依据 S003 的家族页段、S001 的组件/训练表和 S002 的推理/任务地图。它不把多项同时改变后的提升归因于其中一项。[[raw/lectures/VLM-2.pdf#page=48|S003 · pp.48–70]] [[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=18|S001 · §5 · pp.18–19]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=32|S002 · §5、Fig.10 · p.32]]

## 一个家族怎样沿轴展开：课程 Qwen 示例

课程将 Qwen-VL 描述为固定分辨率、cross-attention adapter 和多阶段对齐；Qwen2-VL 转向动态分辨率与 M-RoPE；Qwen2.5-VL 加入窗口/全局注意力安排和真实时间对齐；Qwen3-VL 展示 DeepStack 跨层视觉特征注入、Interleaved-MRoPE 与长交错序列。**这是课程对结构变化的叙述**，足以提出各代解决什么输入和接口问题，但不足以隔离每项变化的独立贡献。[[raw/lectures/VLM-2.pdf#page=54|S003 · Qwen-VL · pp.54–55]] [[raw/lectures/VLM-2.pdf#page=57|S003 · Qwen2 / 2.5 · pp.57–59]] [[raw/lectures/VLM-2.pdf#page=60|S003 · Qwen3-VL · pp.60–63]]

课程 Qwen3-VL 的训练表把 merger-only 对齐、全参数多模态预训练和更长上下文适配分开；这说明“支持长上下文”不仅是位置编码名称，还伴随长度与训练预算的安排。至于某项长文档/视频能力提升来自哪一步，仍需原论文实验。课程概览中的 Qwen3.5 命名和 early fusion 也不能单凭一行替代正式文档核验。[[raw/lectures/VLM-2.pdf#page=62|S003 · 训练表 · pp.62–63]] [[raw/lectures/VLM-2.pdf#page=52|S003 · 概览 · p.52]]

## 跨家族比较从相同问题开始

课程中的 LLaVA 展示投影连接和指令学习；BLIP-2 / InstructBLIP 用 query 接口及指令感知提取；DeepSeek-VL / VL2 展示混合编码到切片/MoE 的不同组合；InternVL 展示扩大视觉骨干与分阶段对齐。合理的横向问题是“细节在哪里取得”“连接器选择多少信息”“哪些参数开放”，而不是把这些例子按年份排成替代链。[[raw/lectures/VLM-2.pdf#page=22|S003 · pp.22–30]] [[raw/lectures/VLM-2.pdf#page=64|S003 · pp.64–70]] [[raw/lectures/VLM-2.pdf#page=83|S003 · pp.83–84]]

InternViT 在课程 InternVL 图中是视觉组件，不因两个名称就产生两个论文身份。类似地，模型系列名、checkpoint 名、论文和官方更新文档也须分别核对；本库按唯一来源页和 registry 管理身份，家族页只作跨向导航。[[raw/lectures/VLM-2.pdf#page=83|S003 · InternVL · pp.83–84]]

## 推理路线也不能当模型成熟度等级

S002 的四阶段图同时涉及表征载体、训练、推理预算和环境控制。它把 N-LMRM 标为展望，既未给普遍量化阈值，也未证明工具只属于某一阶段。因此“更长 CoT”“native”“agentic”需要落实成机制与任务证据，不能作为高于另一家族的等级标签。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=5|S002 · §2、Fig.3 · pp.5–7]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=13|S002 · §3.2.3–3.3 · pp.13–18]]

原论文/官方文档的当前入口集中在 [[wiki/index|索引]]；本轮尚未审核整合的模型不在此提前补规格。继续比较前，先读 [[wiki/vision/Overview|视觉]]、[[wiki/architecture/Overview|架构]] 和 [[wiki/training/Overview|训练]] 的共同维度，再用 [[wiki/evaluation/Overview|评测]] 与 [[wiki/efficiency/Overview|效率]] 限定结论。

来源入口：[[wiki/surveys/Efficient Multimodal Large Language Models A Survey|S001]] · [[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models|S002]] · [[wiki/lectures/VLM-2|S003]]。返回 [[wiki/overview|总览]]；Obsidian 内显示未测。
