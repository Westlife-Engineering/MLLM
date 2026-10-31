---
type: overview
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf]]"
  - "[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]"
  - "[[raw/lectures/VLM-2.pdf]]"
---

# 评测：任务、判分与证据范围

一个分数的含义由三件事共同决定：**交给模型什么任务、怎样认定输出成功、在什么输入与预算条件下运行。** S002 的 Understanding / Generation / Reasoning / Planning 是任务地图，§5.5 是判分方法地图；两者不是同一分类。S001 的能力结果汇表和 S003 的教学比较则说明，分数必须连着划分、指标和设置读。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=32|S002 · §5、Fig.10 · pp.32–41]] [[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=22|S001 · Table 4 · p.22]]

## 先明确成功对象

| 要确认的对象 | 可观察证据 | 单独不足以替代它的观察 |
| --- | --- | --- |
| 感知正确 | 输入中的对象、文字、位置与报告对应 | 回答流畅或引用常识 |
| 答案正确 | 符合参考答案或可验证约束 | 有很长的推理过程 |
| 解释可靠 | 展示步骤逐项成立并与解法相容 | 最终答案恰好正确 |
| 执行发生 | 工具结果、环境变化、实际生成物 | 模型说已调用或已完成 |
| 任务完成 | 最终产物或环境状态满足全部要求 | 文件存在、进程正常结束或某局部动作成功 |

这是本库的证据分解，不是综述提供的一套统一评测器。S002 的六指、数独、简历与媒体个案提示这些观察可以分离；个案未报告统一样本总数与控制协议，不能估计各类失败概率。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=26|S002 · §4.1、Fig.6–8 · pp.26–28]]

## 谁来判、按什么规则判

| S002 判分分类 | 主要比较对象 | 应保留的条件 |
| --- | --- | --- |
| Exact / Fuzzy Matching | 输出与参考答案 | 规范化、同义表达、参考答案覆盖及模糊匹配规则 |
| Options Matching | 选项或其标签 | 选项顺序、提取规则、选择题与开放生成的任务差别 |
| LLM / MLLM Scoring | 评分提示中的输出与要求 | 评分器版本、提示、视觉可见性、稳定性与人工对齐 |
| Agentic Evaluation | 工具或多 agent 辅助形成评价 | 工具证据、讨论组织和错误相关性 |

表中分类来自 S002，右列是本库的协议核查问题。**Agentic Evaluation 在此指 agent 参与评价，不能自动理解成评测对象是 Agent。** 多评价者一致也不直接增加事实证据强度。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=41|S002 · §5.5 · p.41]]

## 分数比较前保留哪些条件

S001 Table 4 的 MMMU 两个值对应 val/test，SEED 对应整体/image 子集，MME 的 perception/cognition 与两者合计不同；星号还标注训练时见过相应数据集训练图像。把斜杠两侧混比、缺失当零分、合计与单项混比，会直接改变结论。星号本身也不足以完成全部污染分析。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=22|S001 · Table 4 脚注 · p.22]]

课程 BEiT-3 的例子同时含 VQA score、Accuracy 和 CIDEr，且分别来自 VQAv2、NLVR2、COCO 的不同划分。指标回答不同问题，不能相加为一个通用能力数。课程嵌入的基线成绩也不是本库独立复跑或预算匹配消融。[[raw/lectures/VLM-2.pdf#page=12|S003 · BEiT-3 配置与结果 · pp.12–13]]

本库据此在实际对照中保留：任务与划分、模型和视觉/语言骨干、分辨率及视觉 token、训练数据可见性、提示与解码、候选和工具预算、判分规则及基线条件。缺失项写未确认；不为了填完整表格推定作者没报告或系统不存在。能力汇表若没有硬件、时延、显存和能耗，就不能回答整体效率最优。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=5|S001 · Table 1 · p.5]] [[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=21|S001 · §6.3、Table 4 · pp.21–22]]

## 代理指标何时越过证据边界

“输出 CoT”“得到了奖励”“产物已生成”“某基准得高分”分别是格式、训练信号、执行结果和受限任务成绩。只有核对它们与目标要求的关系，才可讨论能力。本库据 S002 个案提出这一分层，未据此证明任何代理指标普遍无效，也未确认一个覆盖所有场景的完成判据。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=16|S002 · Fig.5 · pp.16–18]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=27|S002 · §4.1 · pp.27–28]]

后续遇到新 benchmark，应核它测量的任务、判分有效性、人工对齐和可泛化范围；当前这三份地图材料中的 benchmark 列表只是导航，不能把表中每个被引评测都计作本库已读来源。训练信号见 [[wiki/training/Overview|训练]]，运行反馈见 [[wiki/reasoning/Overview|推理]]，成本见 [[wiki/efficiency/Overview|效率]]。

来源入口：[[wiki/surveys/Efficient Multimodal Large Language Models A Survey|S001]] · [[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models|S002]] · [[wiki/lectures/VLM-2|S003]]。返回 [[wiki/overview|总览]]；未运行 benchmark，Obsidian 内显示未测。
