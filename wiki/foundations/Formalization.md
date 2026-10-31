---
type: topic
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf]]"
  - "[[raw/papers/models/llava/LLaVA.pdf]]"
  - "[[raw/papers/architecture/connectors/BLIP-2.pdf]]"
  - "[[raw/papers/architecture/connectors/Flamingo.pdf]]"
  - "[[raw/papers/architecture/pretraining/BEiT-v3.pdf]]"
  - "[[raw/papers/architecture/generation/MiniGPT-5.pdf]]"
  - "[[raw/papers/models/qwen/Qwen-VL.pdf]]"
  - "[[raw/papers/models/qwen/Qwen2-VL.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-VL2.pdf]]"
  - "[[raw/papers/architecture/pretraining/VLMo.pdf]]"
  - "[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]"
  - "[[raw/papers/vision/encoders/ViT.pdf]]"
---

# 基础：把信息、参数与任务证据分成三个层次

阅读MLLM先区分三件事：**模型收到哪些信息，训练更新哪些参数，结果测到了哪种要求。** 下面是本库依据已读原论文与地图材料整理的工作语言；教学公式用于说明常见路径，不宣称覆盖所有架构。

## 从图像到条件语言的最小记法

设图像$X_v$、视觉encoder$g_\phi$、连接器$P_\psi$、文本嵌入$H_q$，输入端连接可写为

$$Z_v=g_\phi(X_v),\quad H_v=P_\psi(Z_v),\qquad
p_\omega(Y\mid H_v,H_q)=\prod_{i=1}^{L}p_\omega(y_i\mid H_v,H_q,y_{<i}).$$

这沿S001组件记法加入参数下标，便于描述冻结。$Z_v/H_v$通常是连续特征，不是已经转写的文字；$P$可仅映射宽度，也可选择、压缩位置。LLaVA线性网格与BLIP-2 query前缀就是两种不同$P$。Flamingo在LM内部多处cross-attention注入视觉，不能由这条简式误画成只接输入端。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=4|S001 · pp.4–7 §2、Eqs1–3]] [[raw/papers/models/llava/LLaVA.pdf#page=4|S022 · p.4 §4.1]] [[raw/papers/architecture/connectors/BLIP-2.pdf#page=3|S017 · pp.3–4]] [[raw/papers/architecture/connectors/Flamingo.pdf#page=5|S016 · p.5 Fig.4]]

## token是计算位置，不是统一信息单位

文本token先是离散词表编号，embedding后参与计算；视觉patch、learned queries、merger输出也被称visual tokens，却不必属于离散词表。BEiT-3离散视觉token是masked预测目标，输入仍是patch embedding；MiniGPT-5输出image vokens又是调用图像生成接口的位置，和输入视觉特征不同。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=4|S015 · pp.4–5 §2.2]] [[raw/papers/architecture/generation/MiniGPT-5.pdf#page=3|S021 · pp.3–4 §3.1–3.2]]

本库因此区分$N_{patch}$、$N_{visual}$、LLM上下文总长与输出长。Qwen-VL的1024patch可压成256query，Qwen2-VL224²为64视觉位置加2边界符，VL2单tile196却不是整图预算。数字相同不证明信息量相同；多了标记也不等于多看图像面积。[[raw/papers/models/qwen/Qwen-VL.pdf#page=20|S026 · p.20 Table8、p.22 E.2]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=4|S027 · p.4]] [[raw/papers/models/deepseek/DeepSeek-VL2.pdf#page=5|S032 · p.5]]

## 参与计算、参数共享、参数更新分开

令全部参数$\Theta=\{\phi,\psi,\omega\}$，某阶段开放子集$\Theta_{train}\subseteq\Theta$。冻结表示优化器不更新该参数，仍可能前向计算并对输入传梯度；少更新参数不等于少存权重、少输入计算或部署必更快。MiniGPT-5冻结扩散U-Net仍传条件梯度，BLIP-2冻结LLM仍训练前面的Q-Former。[[raw/papers/architecture/generation/MiniGPT-5.pdf#page=4|S021 · pp.4–5]] [[raw/papers/architecture/connectors/BLIP-2.pdf#page=4|S017 · p.4 §3.3]]

共享描述复用权重；可见性描述当前前向可以访问的token；路由描述经过哪组变换。VLMo分别前向的图文复用attention却不交换当前信息；联合路径底层已经cross-modal attention，模态FFN并不恢复纯模态输入。冻结范围又是第四个独立轴。[[raw/papers/architecture/pretraining/VLMo.pdf#page=3|S014 · pp.3–6 Figs1–3、§3]]

## 训练阶段不由loss名字单独定义

图文对齐与指令微调可都用自回归交叉熵，差别在条件、监督位置、数据和开放参数。LLaVA只在助手回答和停止标记计loss；BEiT-3主预训练统一MDM，但检索还用中间/下游ITC训练。预训练不等于无监督，也不必从零训练整个LLM。[[raw/papers/models/llava/LLaVA.pdf#page=5|S022 · p.5 §4.2]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=4|S015 · pp.4–5 §2.2、p.16 AppendixA]]

## 能力描述跟着观察对象走

| 工作区分 | 要观察什么 |
| --- | --- |
| 感知 | 输入中的对象、文字、属性、位置能否准确报告 |
| 推理 | 能否用证据和约束得到正确结论，展示解释是否成立 |
| 规划/交互 | 动作是否可执行，反馈是否被利用，最终环境/产物是否满足要求 |

这是依据S002形成的非互斥工作区分；感知可被后续推理引导，终答正确与解释正确可分离。裁剪工具、候选搜索、模型参数和真实环境共同组成被测系统，不能仅凭输出CoT或“执行成功”认定任务完成。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=5|S002 · pp.5–7 §2、pp.26–30 §4.1–4.2]]

接下来沿[[wiki/vision/Overview|视觉]]、[[wiki/architecture/Overview|架构]]、[[wiki/training/Overview|训练]]建立机制，再接[[wiki/efficiency/Overview|效率]]、[[wiki/evaluation/Overview|评测]]与[[wiki/reasoning/Overview|推理]]。[[wiki/lectures/VLM-2|S003]]保留课程推导及勘误；讲义或综述提及的范围外论文仍是转述。本页未运行模型，Obsidian公式显示未测。

## 实际来源入口

[[wiki/surveys/Efficient Multimodal Large Language Models A Survey|S001 Efficient-MLLM-Survey]] · [[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models|S002 Multimodal-Reasoning-Survey]] · [[wiki/papers/architecture/pretraining/VLMo|S014 VLMo]] · [[wiki/papers/architecture/pretraining/BEiT-v3|S015 BEiT-v3]] · [[wiki/papers/architecture/connectors/Flamingo|S016 Flamingo]] · [[wiki/papers/architecture/connectors/BLIP-2|S017 BLIP-2]] · [[wiki/papers/architecture/generation/MiniGPT-5|S021 MiniGPT-5]] · [[wiki/papers/models/llava/LLaVA|S022 LLaVA]] · [[wiki/papers/models/qwen/Qwen-VL|S026 Qwen-VL]] · [[wiki/papers/models/qwen/Qwen2-VL|S027 Qwen2-VL]] · [[wiki/papers/models/deepseek/DeepSeek-VL2|S032 DeepSeek-VL2]] · [[wiki/papers/vision/encoders/ViT|S004 ViT]]。原始定位在上文；唯一页保存身份、读取范围和实验条件。
