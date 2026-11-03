---
type: topic
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/vision/representation/ViT.pdf]]"
  - "[[raw/papers/vision/representation/CLIP.pdf]]"
  - "[[raw/papers/vision/representation/SigLIP.pdf]]"
  - "[[raw/papers/vision/representation/SigLIP2.pdf]]"
  - "[[raw/papers/vision/representation/AIMv2.pdf]]"
  - "[[raw/papers/vision/representation/SoViT.pdf]]"
  - "[[raw/papers/architecture/multimodal-backbones/InternVL.pdf]]"
  - "[[raw/papers/architecture/multimodal-backbones/CoCa.pdf]]"
---

# 视觉预训练：目标要求保留什么，迁移又读取什么？

视觉编码器的“质量”没有脱离任务的单一读数。**预训练规定哪些信息受到监督，迁移接口决定下游怎样读取它。** 整图分类、图文检索、局部定位和接入LLM分别需要不同读出；相同encoder在其中一项得高分，并不自动回答其余问题。本页按监督约束组织已核原论文，而不是排列编码器的排行榜。

## 从分类语义到可由语言选择的概念

ViT把图像切成patch，线性映射后加位置表示，通过全局self-attention和逐位置MLP形成表示。以224²、patch16为例，196个图像位置加一个分类token；分类头的监督聚焦于训练标签，迁移时又可更换分类头并微调整个网络。其JFT子集实验说明数据规模会改变模型大小与归纳偏置的折中，不能从“使用Transformer”单独预测小数据效果。[[raw/papers/vision/representation/ViT.pdf#page=3|S004 · pp.3–4 §3、式1–4]] [[raw/papers/vision/representation/ViT.pdf#page=7|pp.7–8 §4.3–4.4]]

CLIP进一步将监督从固定类别扩成自然语言配对。训练时两塔分别编码图像和文字，以全局向量比较；推理时把候选类别写成提示语，经文本塔得到分类器权重。**语言描述决定了可检索的语义接口，而不是将双塔变成图文逐token融合器。** 例如“boxer”加入宠物或拳击语境后，类别向量不同；zero-shot仍依赖候选类别、提示与开发反馈。[[raw/papers/vision/representation/CLIP.pdf#page=4|S008 · pp.4–5 §2.3、Fig.3]] [[raw/papers/vision/representation/CLIP.pdf#page=6|pp.6–8 §3.1.2–3.1.4]]

令归一化图文向量为$u_i,v_j$，$s_{ij}$为带温度的相似度。CLIP的一个方向为

$$
\mathcal L_{i2t}=-\frac1N\sum_i\log\frac{\exp(s_{ii})}{\sum_j\exp(s_{ij})}.
$$

分母使一对图文的概率依赖同批其他候选；双向目标再加文到图方向。SigLIP则把每对关系作为二分类，以$z_{ij}\in\{-1,1\}$标记原始配对与非配对，可概括为

$$
\mathcal L_{\rm sigmoid}=\frac1N\sum_{i,j}\log(1+\exp(-z_{ij}s_{ij})).
$$

这里的$1/N$保留SigLIP原始归一化，不是$N^2$项平均；相似度含可学习scale和bias。**softmax的全局竞争与sigmoid的逐对判别是损失耦合方式的区别，不是“有负例/无负例”的区别。** 二者都把非原始配对当作负关系，语义上却可能存在合理替代描述。SigLIP分块计算可少保存中间矩阵，但没有自动取消所有$N^2$配对计算。[[raw/papers/vision/representation/CLIP.pdf#page=5|S008 · p.5 Fig.3]] [[raw/papers/vision/representation/SigLIP.pdf#page=3|S009 · pp.3–5 §3、算法1–2]]

## 为什么局部特征还需要额外约束

**本库算例：**“桌上有红杯子”能约束整图语义，但只靠全局向量，不容易判定红色属于左杯还是右杯、杯沿在哪里。SigLIP2让监督进入未池化patch序列：辅助decoder做caption、区域描述→框、框→区域描述；另用EMA教师的全局视图监督局部视图，并在遮挡patch位置预测教师特征。它们分别补充语言—区域对应、局部/全局一致性与密集位置约束，不要求每个patch与一个文本词一一配对。[[raw/papers/vision/representation/SigLIP2.pdf#page=2|S010 · pp.2–4 Fig.1、§2.2–2.3]]

固定分辨率主配方在最后20%训练中启用视觉自蒸馏和masked prediction；20%是时间段，masked的50%是patch比例，captioning的50%是并行预测概率。NaFlex是另一分支，未使用这两项视觉自监督，因此不能把标准模型的全部目标与NaFlex的输入灵活性拼成同一个实验。冻结特征的dense probe、另训定位decoder以及接Gemma2-2B的VLM适配，才分别验证下游可读性；辅助预训练decoder本身没有发布成聊天模型。[[raw/papers/vision/representation/SigLIP2.pdf#page=4|S010 · pp.4–6 §2.3–2.5]] [[raw/papers/vision/representation/SigLIP2.pdf#page=9|pp.9–11 §3.3–3.4、Tables2–5]]

AIMv2走另一条密集监督路径：prefix视觉encoder接causal multimodal decoder，在图像侧回归归一化下一patch像素，在文本侧预测下一token。联合损失$L_{text}+\alpha L_{img}$中，图像损失只覆盖非prefix区域；训练decoder和后续接入的LLM是不同模块。表9控制ViT-L、224²、2B样本后，在同样prefix设置下加图像目标，TextVQA从36.5到37.5，提供了有限但更直接的增量证据。它不证明所有细节都被无损保存。[[raw/papers/vision/representation/AIMv2.pdf#page=2|S007 · pp.2–3 §2.1–2.2、Fig.1]] [[raw/papers/vision/representation/AIMv2.pdf#page=8|p.8 Table9a–b]]

## 容量、形状和接口一起决定迁移

SoViT固定训练FLOPs，联合调整width、depth、MLP宽度与训练时长。更大的每样本计算会挤压可处理样本数；因此“参数更多”不是同预算下的唯一方向。其428M模型与约1B ViT-g在同一预训练FLOPs下接近多项迁移结果，却在panoptic segmentation上有差距。分类导出的近优形状需要按目标任务解释，不能由ImageNet直接推定密集任务同样最优。[[raw/papers/vision/representation/SoViT.pdf#page=4|S005 · pp.4–6 §3、式2/4]] [[raw/papers/vision/representation/SoViT.pdf#page=8|pp.8–10 §5、Tables1–4]]

InternVL扩大视觉主干至InternViT-6B，并先对比训练、再冻结视觉主干训练QLLaMA新接口。第二阶段的caption生成目标并没有继续更新InternViT；“系统用了生成监督”不等于“视觉编码器同时被生成目标训练”。其Chat还可同时保留直接视觉网格与query通路，视觉规模与语言中间件规模应分列。InternViT与InternVL在本库共用S025身份。[[raw/papers/architecture/multimodal-backbones/InternVL.pdf#page=4|S025 · pp.4–6 §3.2–3.3、Figs3–4]]

| 迁移读出 | 实际新训练了什么 | 它回答的问题 |
| --- | --- | --- |
| 文本zero-shot分类（CLIP） | 目标集不另训分类器，类别经文本塔编码 | 现有图文空间能否按这些类别文字选择 |
| 冻结linear probe（ViT/SoViT） | 线性分类头 | 特征对目标标签是否线性可分 |
| attentive probe（AIMv2/CoCa） | attention pooler和任务头 | 冻结骨干能否被更强读出使用 |
| encoder全调 | 骨干和任务头 | 给定监督与预算下适配后的性能 |
| 新LLM+connector+SFT | 依实验开放接口/LLM等 | 特征在特定多模态系统中是否有效 |

表的协议证据：[[raw/papers/vision/representation/CLIP.pdf#page=38|S008 · p.38 §A.3]]、[[raw/papers/vision/representation/SoViT.pdf#page=8|S005 · pp.8–9]]、[[raw/papers/vision/representation/AIMv2.pdf#page=5|S007 · pp.5–7 §4]]、[[raw/papers/architecture/multimodal-backbones/CoCa.pdf#page=7|S013 · pp.7–9 §4.2.1]]。这些读出不构成同一标尺。

继续到[[wiki/vision/Resolution-and-Token-Budget|分辨率与token预算]]检查信息在输入时是否保留，到[[wiki/training/Supervision-and-Stages|监督与阶段]]检查目标更新了谁，到[[wiki/evaluation/Overview|评测地图]]核读出条件。综述/讲义入口见[[wiki/surveys/Efficient Multimodal Large Language Models A Survey|S001]]、[[wiki/lectures/VLM-2|S003]]；本页具体机制已由上述原论文定位支撑，不能据此将其余被引工作计为已读。

## 实际来源入口

[[wiki/papers/vision/representation/ViT|S004 ViT]] · [[wiki/papers/vision/representation/SoViT|S005 SoViT]] · [[wiki/papers/vision/representation/AIMv2|S007 AIMv2]] · [[wiki/papers/vision/representation/CLIP|S008 CLIP]] · [[wiki/papers/vision/representation/SigLIP|S009 SigLIP]] · [[wiki/papers/vision/representation/SigLIP2|S010 SigLIP2]] · [[wiki/papers/architecture/multimodal-backbones/CoCa|S013 CoCa]] · [[wiki/papers/architecture/multimodal-backbones/InternVL|S025 InternVL]]。原始定位在上文；唯一页保存身份、读取范围和实验条件。
