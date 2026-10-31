---
type: paper
source_id: S005
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/vision/encoders/SoViT.pdf]]"
primary_direction: vision/encoders
reading_status: read
ingest_status: complete
---

# SoViT：固定计算预算下，应该把 ViT 做宽、做深，还是增大 MLP？

> [!summary] 先记住什么
> 参数量不足以描述 ViT 的设计。SoViT 联合考虑 width、depth、MLP hidden dimension 与训练时长，在作者的 JFT-3B 设置中用约428M参数模型接近约1B ViT-g的多项迁移成绩，预训练FLOPs相同、推理FLOPs较少。它不是压缩已有大模型，也没有证明一种形状对所有视觉/多模态任务最优：全景分割是明确的反例。[[raw/papers/vision/encoders/SoViT.pdf#page=8|p.8 §5、表1]]；[[raw/papers/vision/encoders/SoViT.pdf#page=9|p.9 §5.4]]

## 来源身份与阅读范围

- **论文**：Ibrahim Alabdulmohsin、Xiaohua Zhai、Alexander Kolesnikov、Lucas Beyer，*Getting ViT in Shape: Scaling Laws for Compute-Optimal Model Design*；NeurIPS 2023。PDF首页为 arXiv:2305.13035 **v5，2024-01-09**，21页；[固定版本](https://arxiv.org/pdf/2305.13035v5)。
- **原件**：[[raw/papers/vision/encoders/SoViT.pdf]]；SHA-256 `360540d5b39e666adc1a72bf6f50c803b5494c05bf4e03b666bf479cc7ab903b`。
- **读取**：2026-10-31，正文pp.1–10，附录A–E pp.16–21；实际渲染查看pp.4、5、7、8、10、16、17，核对目标函数、解析式、搜索流程、消融、主结果与训练设置。参考文献未沿引文扩读；未审代码、未复现、Obsidian内显示未测。
- **旧笔记输入**：[[raw/notes/视觉编码器/SoViT总结.tex]] 与 [[raw/notes/视觉编码器/Latex_out/SoViT总结.pdf]]。本次对照TeX正文，编译PDF不单独充当证据。

## 1. 为什么“参数更多”不是同预算下的答案？

扩大模型通常会提高单个样本的计算成本。在训练总计算固定时，更大的网络能看到的样本次数更少；容量收益可能抵不过训练不足。本文还进一步问：相同参数量，宽度、层数、MLP大小的分配是否一样好？评价目标使用下游 ImageNet 10-shot error，而不只看上游预训练loss；任务一变，小模型的优选形状也会改变。[[raw/papers/vision/encoders/SoViT.pdf#page=3|pp.3–4 §3、图3]]

**本库解释**：这里“compute-optimal”是在给定指标、数据、训练设置和搜索近似下的效率前沿，不是对所有架构的全局最优证明。作者目标式(1)本身允许正的误差容忍度。[[raw/papers/vision/encoders/SoViT.pdf#page=4|p.4 式(1)]]

## 2. 先拟合单维的容量—训练折中

令$x_k$为某一形状维度、$t$为训练计算，作者假设其他形状维度足够大而不形成瓶颈、数据充足而不会因有限数据过拟合，拟合：

$$
f_k(x_k,t)\sim\alpha_kx_k^{-a_k}+(\beta_kx_k^{b_k}+\xi_k)t^{-c}+\varepsilon_k.
$$

所有系数/指数为正。第一项随该维度增大而下降，第二项在计算固定时随该维度增大而上升；因此“容量更大但训练不足”的两种效应能在同一曲线上表示。$\varepsilon_k$是该拟合式的残余误差项，不能当成已精确测出的任务Bayes error。这个形式是作者的经验模型，有理论动机和拟合验证，不是Transformer必然服从的定律。[[raw/papers/vision/encoders/SoViT.pdf#page=4|p.4 式(2)、假设及说明]]

令对$x_k$的导数为0，得到：

$$
-\alpha_ka_kx_k^{-a_k-1}+\beta_kb_kt^{-c}x_k^{b_k-1}=0,
\quad
x_k^*=\left(\frac{\alpha_ka_k t^c}{\beta_kb_k}\right)^{1/(a_k+b_k)},
\quad s_k=\frac{c}{a_k+b_k}.
$$

这个连续最优解说明单维最优尺寸按$t^{s_k}$增长；实际层数等仍需取可实现的离散形状。附录证明该拟合函数对单维先减后增、具有准凸性；这证明的是假设函数的性质，不是证明真实训练loss全局准凸。[[raw/papers/vision/encoders/SoViT.pdf#page=5|p.5 式(4)]]；[[raw/papers/vision/encoders/SoViT.pdf#page=16|p.16 附录A.1]]

## 3. Star sweep 与小模型 grid sweep 分别解决什么？

1. **Star sweep估计增长指数**。取大中心$(width,depth,MLP)=(1968,40,6144)$，每次只降低/扫描一个维度，另两个维度固定较大，尽量避免别的瓶颈污染拟合。每个架构训练500k/1M/2M steps，patch14、16 heads；附录表5写明这些搜索使用224分辨率、batch128、AdaFactor。正文概述提Adam，因此不把概述直接覆盖搜索阶段的明确配置。[[raw/papers/vision/encoders/SoViT.pdf#page=5|p.5 §3]]；[[raw/papers/vision/encoders/SoViT.pdf#page=17|p.17 B.1–B.2、表5]]
2. **Grid sweep确定起点与比例系数**。在小模型组合上各训练600M次样本，选择小预算的前沿点$(608,10,928)$。候选应处于网格内部且在一段预算上有效；边界最优可能只是搜索范围不够。这里的“小”也不是几百万样本的低成本玩具验证。[[raw/papers/vision/encoders/SoViT.pdf#page=5|p.5 Grid Sweep]]；[[raw/papers/vision/encoders/SoViT.pdf#page=17|p.17 B.3]]
3. **把预算增长分配给多个维度**。论文使用$w_k=1/D$的平均预算分配；由于各维的$s_k$不同，不能解释成宽、深、MLP按同一个倍数增长。分类拟合得到$s_{width}\approx0.22,s_{depth}\approx0.45,s_{MLP}\approx0.60$，作者结果为MLP增长最快，其次depth，最后width。[[raw/papers/vision/encoders/SoViT.pdf#page=5|pp.5–6 Scaling、§4.1]]

> [!note] 原文符号歧义保留
> p.5 Scaling 段把预算子增量与形状增量都写成$\tau^{w_k}$，未在该处显式带上前文$s_k$。**本库依据式(4)重建**：分给第$k$维的预算倍率若为$\tau^{w_k}$，相应形状倍率应为$\tau^{w_ks_k}$；三维平均分配时是$\tau^{s_k/3}$。这与图1从1T到100T时width约1.5倍、depth约2倍、MLP约2.6倍相符。该解释未核验实现代码，不能伪称原文逐字公式。[[raw/papers/vision/encoders/SoViT.pdf#page=2|p.2 图1]]；[[raw/papers/vision/encoders/SoViT.pdf#page=5|p.5 式(4)及Scaling段]]

## 4. 得到的模型与等预算比较

SoViT-400m/14形状为width1152、27层、MLP4304，表1实际参数428M。JFT-3B约3B不同图像，**40B examples指训练处理次数而非400亿独立图像**。SoViT训练40B次、ViT-g/14训练16B次，两者约9T GFLOPs；v5给出的实测时间分别230k与210k TPUv3 core-hours。所以“FLOPs相同”不等于“耗时严格相同”或“预训练成本降低2.5倍”。[[raw/papers/vision/encoders/SoViT.pdf#page=7|p.7 §4.1]]；[[raw/papers/vision/encoders/SoViT.pdf#page=8|p.8 Compute、表1]]

| 评估协议 | SoViT-400m/14 | ViT-g/14 | 条件与含义 |
| --- | --- | --- | --- |
| ImageNet整网微调，518² | 90.3% Val，1374G FLOPs | 90.2%，3208G FLOPs | 同JFT来源与作者受控设置；SoViT约428M对1011M；每次推理FLOPs较低 |
| ImageNet冻结线性探测 | 88.2% Val | 88.4% | 不是90.3%那一协议；同表ReaL、ObjectNet等有各自胜负 |
| ImageNet 10-shot线性 | 84.1% | 84.0% | 表3还包含多类下游分类任务，接近不表示逐项最好 |
| LiT后ImageNet zero-shot | 82.2% | 82.4% | 另用WebLI训练文本编码器；并非原分类encoder天然具有zero-shot文本对齐 |
| COCO captioning | CIDEr125 | CIDEr126 | 固定两层multitask decoder，224²输入 |
| VQAv2 / GQA | 67.7% / 56.0% | 68.8% / 58.0% | 不能从“接近”改写成全面多模态领先 |
| COCO panoptic UViM，512² | PQ43.7 | PQ44.8 | 密集任务上有差距，作者明确列作限制 |

表格依据：[[raw/papers/vision/encoders/SoViT.pdf#page=8|p.8 表1–2]]；[[raw/papers/vision/encoders/SoViT.pdf#page=9|p.9 表3、§5.2–5.4]]；[[raw/papers/vision/encoders/SoViT.pdf#page=10|p.10 表4]]。ImageNet微调50k steps、batch512、SGD momentum0.9，使用训练集留出2%选超参，518²有RandAugment和mixup；LiT表7处理900M样本、batch32k。[[raw/papers/vision/encoders/SoViT.pdf#page=19|pp.19–20 表7–8]]

形状消融也有一个重要限定：等FLOPs下，SoViT-150m的10-shot为78.5%，超过B/14的76.6%和同参数规模B-150m的77.9%，支持形状不仅是参数量的替代写法；但将depth增加33%或200%得78.8/78.9，局部变体仍可能更高。因此作者得到的是可外推的近优配方，并非每个邻居都严格更差。[[raw/papers/vision/encoders/SoViT.pdf#page=7|p.7 图6]]

## 5. 哪些边界会改变使用判断？

- **目标依赖**：分类与两层decoder任务的单维指数接近，不代表小模型最优起点相同；分割差距也表明分类导出的形状未必适合密集预测。[[raw/papers/vision/encoders/SoViT.pdf#page=4|p.4 图3]]；[[raw/papers/vision/encoders/SoViT.pdf#page=9|p.9 §5.4]]
- **搜索轴有限**：主要优化width/depth/MLP，patch固定14；后续FlexiSoViT说明变patch仍有效，作者明确说它不排除其他patch才是计算最优。不能用后续适配替代patch联合搜索。[[raw/papers/vision/encoders/SoViT.pdf#page=10|p.10 §5.5续]]
- **实验非普适理论**：数据充足、其他轴无瓶颈、幂律拟合、预算分配均是条件。大JFT训练与专用TPU的证据不直接给出公开数据、其他硬件或有限数据循环训练的最优形状。
- **附录报告差异**：E.2正文说线性探测留出2%，表9却列99%/1%；本库不自行统一。需要精确复现实验时应回查实现/作者说明。[[raw/papers/vision/encoders/SoViT.pdf#page=20|pp.20–21 E.2、表9]]

## 旧笔记校正与知识整合建议

旧稿把“目前主流ViT都参数冗余”“SoViT效果最佳”“最能体现VLM优越性”写得过广。本页改为**本文基线、预算、任务与decoder设置下的竞争性结果**，保留GQA/VQAv2及分割差距。旧稿“无限计算时增大$x_k$仍因第二项暴增”的句子混淆了极限：固定$x_k$令$t\to\infty$时第二项消失；只有固定/受限计算下增大$x_k$才出现代价。平均分配预算也不等于相同形状增长率。

**本库整合主题**：编码器设计中的容量、形状与训练时长；FLOPs/墙钟时间/推理成本的分离；分类表示与语言解码、密集预测的目标差异。实际主题入链见页末。与[[wiki/papers/vision/encoders/ViT|ViT]]的连接在于：ViT证明了大数据下标准架构的可扩展性，SoViT继续询问同一类架构如何分配有限计算；二者具体数据、训练配方和评估年份不同，不能直接用最终分数判架构进步的因果来源。

## 实际整合关系

支撑形状/时长/容量的预算分配，解释FLOPs、参数与墙钟的分离及密集任务边界。

- [[wiki/vision/Objectives-and-Transfer|视觉预训练：目标要求保留什么，迁移又读取什么？]]。
- [[wiki/efficiency/Resource-Ledger|资源账本：视觉token、激活参数、KV与系统预算分别省在哪里？]]。
- [[wiki/evaluation/Judges-and-Task-Success|裁判与任务成功：答案、解释、生成物和终态怎样分别取证？]]。
