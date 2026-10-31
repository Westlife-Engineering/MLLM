---
type: topic
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf]]"
  - "[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]"
  - "[[raw/lectures/VLM-2.pdf]]"
---

# 基础：信息、参数与任务的三个层次

读 MLLM 时最容易混淆三件事：**模型能接收哪些信息、训练更新哪些参数、结果证明哪种能力。** 下面先用一个常见接口建立符号，再把三个层次分开。此处是本库的教学整理，依据 S001 组件框架、S003 机制讲解和 S002 能力证据讨论，不宣称定义覆盖所有多模态架构。

## 图像如何进入语言生成

设图像为 $X_v$，视觉编码器为 $g_\phi$，连接器为 $P_\psi$，文本指令嵌入为 $H_q$。常见的输入端连接方案可写为：

$$
Z_v=g_\phi(X_v),\qquad H_v=P_\psi(Z_v),
$$

$$
p_\omega(Y\mid H_v,H_q)=\prod_{i=1}^{L}p_\omega(y_i\mid H_v,H_q,y_{<i}).
$$

$Z_v$ 是视觉特征，$H_v$ 是送给语言模型的视觉嵌入，$Y$ 是生成文本，$L$ 是输出长度。$\phi,\psi,\omega$ 分别标记组件参数，便于后面描述冻结范围；这是在 S001 符号上增加的教学下标。连接器可以改变维度，也可以聚合信息或改变 token 数，并非只把图片“翻译成一段文字”。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=4|S001 · §2.1–2.3、Eq.1–3 · pp.4–7]]

这组公式不要求所有系统都只在第一层接视觉输入。讲义中的 BLIP-2 用 query 读取视觉特征，CogVLM 在语言模型内部给视觉位置配置专用参数，DeepStack 将不同深度视觉特征接入 LLM 多层。它们是理解接口位置的教学例子，此处尚未以被引原论文建立直接证据。[[raw/lectures/VLM-2.pdf#page=22|S003 · BLIP-2 · pp.22–23]] [[raw/lectures/VLM-2.pdf#page=74|S003 · CogVLM · p.74]] [[raw/lectures/VLM-2.pdf#page=60|S003 · Qwen3-VL · p.60]]

## token 是计算位置，不是统一的信息单位

文本 tokenizer 把字符串映射成离散编号，再取得嵌入；视觉 patch 经编码得到连续向量，也常被称为 visual tokens。两者都可以成为模型处理的序列位置，但视觉 token 不必对应词表中的离散“词”。讲义还展示 learned query、view separator 和 new line 等位置，它们承担聚合或结构标记职责，不能都当作同等面积的图像块。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=7|S001 · §2.3–2.4 · p.7]] [[raw/lectures/VLM-2.pdf#page=22|S003 · learned queries · p.22]] [[raw/lectures/VLM-2.pdf#page=68|S003 · view / row structure · p.68]]

因此，问“用了多少 token”还要问：是视觉编码前的 patch 数，连接后的视觉位置数，语言上下文总长度，还是输出 token 数？这些量影响不同计算；不同压缩接口下，一个视觉 token 承载的信息也不相同。详见 [[wiki/vision/Overview|视觉表示]] 与 [[wiki/efficiency/Overview|效率账本]]。

## 冻结与更新：参数参与计算不等于参与学习

设总参数集合为 $\Theta=\{\phi,\psi,\omega\}$，当前训练开放的子集为 $\Theta_{\mathrm{train}}\subseteq\Theta$。**冻结**指参数在该阶段不被优化器更新，不能据此认为它不参加前向计算，或不再占据存储。这里是参数集合的教学记法；S001 与课程图用冰块/火焰展示不同开放范围。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=18|S001 · §5、Fig.14 · pp.18–19]] [[raw/lectures/VLM-2.pdf#page=23|S003 · BLIP-2 · p.23]]

例如，讲义的 LLaVA 第二阶段名为 Fine-tuning End-to-End，同时明确冻结视觉编码器、更新投影层和 LLM。阶段名称不足以确定 $\Theta_{\mathrm{train}}$。共享注意力参数也不足以证明图文正在互相读取：VLMo 对比任务可以分塔编码，融合任务才让联合序列交互。[[raw/lectures/VLM-2.pdf#page=30|S003 · LLaVA · p.30]] [[raw/lectures/VLM-2.pdf#page=4|S003 · VLMo · pp.4–7]]

## 预训练与指令微调怎样区分

S001 的常见流程先用图文对学习跨模态接口，再用指令—回答学习任务行为；**两阶段可以使用相同自回归目标**。因此不能把 pre-training 定义为“无监督”、把 instruction-tuning 定义为“换一种损失”。应问数据怎样组织、哪些输出位置受监督、哪些参数开放、希望形成什么行为。这里的多模态预训练也不必意味着从零训练整个语言模型。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=18|S001 · §5.1–5.2、Eq.4–5 · pp.18–19]]

讲义还展示图文对比、匹配、掩码建模和生成目标。它们分别约束表示相似性、配对判断、缺失内容恢复或条件生成；同一个架构可组合多种目标。阶段与目标的具体关系进入 [[wiki/training/Overview|训练页]]，不靠“预训练模型”一个标签判断。[[raw/lectures/VLM-2.pdf#page=5|S003 · VLMo 目标 · p.5]] [[raw/lectures/VLM-2.pdf#page=22|S003 · BLIP-2 masks · p.22]]

## 能力描述要跟着证据对象走

| 描述 | 本库阅读时关心什么 | 至少不能省略的核查 |
| --- | --- | --- |
| Perception / 感知 | 相关视觉信息是否被提取并正确报告 | 输入内容与回答是否一致，细节/位置是否正确 |
| Reasoning / 推理 | 如何利用信息得到满足约束的结论 | 终答正确性、条件变化及必要的中间步骤核查 |
| Planning / 规划 | 怎样把目标转成行动安排并依据反馈调整 | 计划可执行性、实际动作、观察及最终环境状态 |

这是依据 S002 用法形成的**工作区分**，不是作者给出的三个互斥数学定义。其图6中推理会引导再次裁剪，感知与推理可循环；图7数独展示终答正确与解释错误分离，文件案例展示交付存在与内容满足要求分离。个案说明为什么要分层取证，不能用来估计总体失误率。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=5|S002 · §2 · pp.5–6]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=26|§4.1、Fig.6–8 · pp.26–28]]

来源入口：[[wiki/surveys/Efficient Multimodal Large Language Models A Survey|S001]] · [[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models|S002]] · [[wiki/lectures/VLM-2|S003]]。回到 [[wiki/overview|总览]]；Obsidian 内公式与显示未测。
