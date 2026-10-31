---
type: overview
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]"
  - "[[raw/lectures/VLM-2.pdf]]"
---

# 推理与交互：更多步骤怎样用到视觉证据

多模态推理的关键不只在“想多久”，还在**每一步依据什么信息、怎样选择下一步、最后验证了什么结果**。S002 把模块化感知、语言中心短推理和长推理组织成历史路线，再展望 native multimodal reasoning；它提供比较视角，并未证明一条必然演进规律。本页以该综述为主，具体案例保留作者个案或综述转述身份。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=5|S002 · §2、Fig.3 · pp.5–7]]

## 三个位置决定机制差别

| 位置 | 可能怎样改变推理 | 需要问的证据问题 |
| --- | --- | --- |
| 训练时 | rationale/CoT 监督、偏好、奖励优化形成输出与解题习惯 | 信号奖励格式、终答还是过程？任务内收益能否迁移？ |
| 测试时的路径分配 | 多候选、beam、MCTS、评分选择与反思 | 候选/节点多少，评分器是否可靠，预算是否匹配？ |
| 信息与环境接口 | 裁剪、检索、代码、视觉专家、工具和记忆 | 是否获得新证据或外部计算，动作后有无新观察？ |

表为本库重组；综述 Stage 2 已包含搜索、工具和长时程问题，Stage 3 又围绕更深推理与训练重新组织类似部件，不能把阶段视作互斥机制清单。DPO、PPO、GRPO 等也不能凭 R1-like 标签当作同一算法。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=13|S002 · §3.2.3–3.3、Fig.5、Table 6 · pp.13–19]]

## 反思可以改变下一次观察

S002 图6的 o3 个案先裁剪图形，发现观察范围不足，再调整裁剪并继续解题。这里中间决策改变下一步看到什么，感知不是一次性前处理。图8的六指误判则展示视觉内容与输出不一致：更长语言推理本身不足以保证视觉证据被正确利用。成功与失败都只是作者展示的个案，未给发生率或隔离内部机制的实验。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=26|S002 · §4.1、Fig.6–8 · pp.26–28]]

本库据此区分两种增加计算：**在同一表示上生成更多推理**，以及**通过动作取得新的任务信息**。两者可组合，但不能把裁剪工具、代码计算和模型内部推断的全部收益归给“长 CoT”。同样，best-of-N 的提升还依赖候选生成与判分，若不记评分器成本就漏掉系统开销。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=15|S002 · §3.3 · pp.15–18]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=26|S002 · Fig.6 · p.26]]

## 从计划文本走向动作—观察循环

```mermaid
flowchart LR
    O[当前观察与目标] --> D[推断 / 规划]
    D --> A[动作或工具调用]
    A --> E[环境变化与返回]
    E -->|新观察| O
    E --> V[核查目标状态]
```

此图为本库对闭环关系的教学整理：行动改变环境，返回提供新信息，目标核查还需判断任务要求是否满足。依据为 S002 对 agentic reasoning 的论述与 S003 Kimi K2.5 图中的 Act/Obs 方向；不是作者已验证的通用控制算法。讲义还画了 rollout、judge 与训练服务，它们说明交互轨迹可以进入训练系统，并未仅靠箭头定义完整 reward 或学习规则。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=27|S002 · §4.2、Fig.9 · pp.27–30]] [[raw/lectures/VLM-2.pdf#page=81|S003 · Kimi K2.5 · p.81]]

“写出计划”“调用成功”“任务终态满足要求”需要不同观察。S002 的简历和媒体生成案例中，产物存在仍可能缺项或违背要求；数独案例则表现出终答正确、展示解释有误。这些现象支持将答案、解释、执行与完成分开取证，不支持推断模型具有欺骗意图或完全没有解题能力。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=27|S002 · §4.1、Fig.7–8 · pp.27–28]]

## 原生多模态留下怎样的可检验问题

作者希望多模态中间表示、交错生成和世界反馈持续参与推理；N-LMRM 仍是展望。可继续检验：相同任务与预算下，图像中间表示比文字描述保留了什么；视觉与语言先验冲突时能否识别；训练奖励与真实任务终态是否一致；工具失效后能否恢复。这里是本库把作者方向转成验证问题，尚未形成已确认研究空白，也不据此扩展本轮来源。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=30|S002 · §4.3 · pp.30–31]]

继续到 [[wiki/evaluation/Overview|评测]] 检查判分对象，或到 [[wiki/efficiency/Overview|效率]] 记录搜索与工具预算。来源入口：[[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models|S002]]、[[wiki/lectures/VLM-2|S003]]；返回 [[wiki/overview|总览]]。未运行交互系统；Obsidian 内 Mermaid 与显示未测。
