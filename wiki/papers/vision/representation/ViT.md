---
type: paper
source_id: S004
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/vision/representation/ViT.pdf]]"
primary_direction: vision/representation
reading_status: read
ingest_status: complete
---

# ViT：图块序列上的标准 Transformer，何时能学好视觉表示？

> [!note] 主归属（本库导航判断）
> patch Transformer 的主要复用对象是视觉编码与迁移表示；分类任务是其验证方式。 [[raw/papers/vision/representation/ViT.pdf#page=3|§3.1/Fig.1]]

> [!summary] 核心判断与边界
> ViT 把图像切成 patch，再用标准 Transformer encoder 做有监督分类预训练。本文的重要证据是：在作者测试的数据、模型和优化设置下，足够大的预训练数据让这种较少视觉归纳偏置的架构具有很好的分类迁移与计算折中。它没有证明“小数据从零训练也优于 CNN”，也没有验证 MLLM 问答、检测或分割能力。[[raw/papers/vision/representation/ViT.pdf#page=7|PDF p.7 §4.3、图3–5]]；[[raw/papers/vision/representation/ViT.pdf#page=9|p.9 §5]]

## 来源身份与实际阅读

- **原文**：Alexey Dosovitskiy、Lucas Beyer、Alexander Kolesnikov 等，*An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*；ICLR 2021。归档为 arXiv:2010.11929 **v2，2021-06-03**，22页；[固定版本 URL](https://arxiv.org/pdf/2010.11929v2)。标题、作者、版本据 PDF 首页核对。
- **原件**：[[raw/papers/vision/representation/ViT.pdf]]；SHA-256 `8ce7b83971a14508ca711a27c875c9b6914c4f6767cf3150fb1ca6c07aa056d6`。
- **读取日期/范围**：2026-10-31；正文 pp.1–9；关键附录 A–D 的方法、训练与消融 pp.13–20，p.22 VTAB分项。原页渲染核对 pp.3、4、6、7、13、15、17 的机制图、公式、主结果和消融表。
- **未读/未做**：参考文献未逐项追读；p.21 的128例注意力图未逐例视觉检查；未运行代码或复现；Obsidian 内显示未测。下文不把附录图示当成定量因果证据。
- **旧笔记输入**：[[raw/notes/多模态经典/2021-ICLR-ViT.md]]，冻结的二手解释，不计论文证据。

## 1. 问题不只是“把 CNN 换成注意力”

直接以像素作为 token 会产生很长的序列，全局注意力的成对交互随序列长度平方增加。ViT 的工程选择是先将图像分成固定大小的块，以块作为序列单位，尽量复用标准 Transformer。另一项代价是放弃 CNN 在各层内置的局部性、二维邻域与平移等变性，因此必须同时研究数据规模，而不能只比一次 ImageNet 训练。作者也承认已有类似 patch-attention 设计；本文不应被写成所有组成模块的首次发明。[[raw/papers/vision/representation/ViT.pdf#page=2|p.2 §2]]；[[raw/papers/vision/representation/ViT.pdf#page=4|p.4 §3.1]]

## 2. 信息怎样从图像走到分类结果？

输入图像为 $H\times W\times C$，块边长为 $P$，得到 $N=HW/P^2$ 个展平的 $P^2C$ 维块。共享线性投影 $E$ 把每块变为 $D$ 维，前置可学习的 classification token，再加可学习的一维位置表：

$$
z_0=[x_{\mathrm{class}};x_p^1E;\ldots;x_p^NE]+E_{\mathrm{pos}}.
$$

每层先以 self-attention 交换 token 间的信息，再逐 token 做两层 GELU MLP；两者均为 pre-LayerNorm 和残差结构：

$$
z'_\ell=\mathrm{MSA}(\mathrm{LN}(z_{\ell-1}))+z_{\ell-1},\qquad
z_\ell=\mathrm{MLP}(\mathrm{LN}(z'_\ell))+z'_\ell.
$$

最终图像表示为 $y=\mathrm{LN}(z_L^0)$。预训练分类头有一个 tanh 隐藏层；迁移时丢弃整颗头，换零初始化线性分类头，继续微调整个网络。这里 encoder 内每个 token 都经过的 MLP 与最终分类头是不同模块。上述公式与结构对应原文式(1)–(4)、图1。[[raw/papers/vision/representation/ViT.pdf#page=3|pp.3–4 §3.1、图1与式(1)–(4)]]；[[raw/papers/vision/representation/ViT.pdf#page=14|p.14 B.1.1]]

例如 $224\times224$ 图像、$P=16$ 时有196个图像 token，加分类 token 后为197；升到384分辨率时为576+1。**本库算例**用于解释长度变化，并非新增实验。提高分辨率保持 patch 大小不变，把预训练位置向量按原二维网格插值。网络可接不同长度，不意味着位置表或内存开销自动解决。论文仍显式使用了切块与二维插值这两处空间结构，所以“没有任何视觉归纳偏置”过强。[[raw/papers/vision/representation/ViT.pdf#page=4|p.4 §3.2]]

一种对照是 hybrid：先用 ResNet 特征图，再以其空间位置形成 Transformer 输入；这保留卷积前端，并不属于纯像素块 ViT。分类 token 也不是理论必需：重新调整学习率后，global average pooling 可获得相近的5-shot结果。[[raw/papers/vision/representation/ViT.pdf#page=4|p.4 Hybrid Architecture]]；[[raw/papers/vision/representation/ViT.pdf#page=17|p.17 D.3、图9]]

## 3. 实验要分开读：数据、读出和预算都在变

模型 B/L/H 分别为12/24/32层，隐藏维768/1024/1280，参数86M/307M/632M；`/16`、`/14` 是 patch 边长，不能误当层数。预训练数据为 ImageNet（约1.3M）、ImageNet-21k（约14M）和 JFT（303M）；作者对下游测试集做预训练去重。[[raw/papers/vision/representation/ViT.pdf#page=4|pp.4–5 §4.1、表1]]

| 证据 | 条件与观测 | 能支持的结论 |
| --- | --- | --- |
| 主结果表2 | JFT 预训练 ViT-H/14：ImageNet 88.55±0.04%、CIFAR-100 94.55±0.04%、VTAB19任务平均77.63±0.23%；三次微调均值和标准差 | 大规模监督预训练后的分类迁移有效；不是从零训练或冻结线性探测结果 |
| 数据规模图3/表5 | ImageNet 预训练时 L 落后 B；ImageNet-21k接近，JFT上大模型获益；表5默认384微调 | 数据规模改变大模型的收益，不能抽成一个跨设置固定门槛 |
| JFT子集图4 | 9M/30M/90M/全量；相同超参、小子集未另加正则，使用早停；冻结表示上 ImageNet **5-shot** 最小二乘分类 | 在该协议下，卷积的小数据优势与 ViT 的大数据优势发生转换；不是全量微调曲线 |
| 计算图5/表6 | JFT，ViT/ResNet/hybrid，7或14 epochs，报告预训练exaFLOPs及多个下游分类准确率 | 作者估计ViT达同等五任务平均成绩约少2–4倍计算；范围仅此组训练方案 |

定位：[[raw/papers/vision/representation/ViT.pdf#page=6|p.6 表2、§4.3]]；[[raw/papers/vision/representation/ViT.pdf#page=7|p.7 图3–5]]；[[raw/papers/vision/representation/ViT.pdf#page=8|p.8 §4.4]]；[[raw/papers/vision/representation/ViT.pdf#page=15|p.15 表5–6]]。

表2的旗舰结果有额外条件：预训练分辨率224，JFT H/14训练14 epochs；ImageNet微调 H/14使用518分辨率、L/16使用512，并加 Polyak averaging。常规表5/6默认384，不应混用成绩。主训练 Adam、batch4096；微调为 momentum SGD、batch512，ImageNet 20k steps。[[raw/papers/vision/representation/ViT.pdf#page=5|p.5 训练说明]]；[[raw/papers/vision/representation/ViT.pdf#page=13|pp.13–14 表3–4]]

表2列出H/14为2.5k、L/16为0.68k、BiT-L为9.9k TPUv3-core-days，但这组文献比较同时受日程、优化器、weight decay影响，不能把耗时差全归因于架构。正文“L/16胜过BiT-L所有任务”的措辞也比表格严格：VTAB为76.28±0.46对76.29±1.70，数值几乎相同且前者略低。本库以表格保留这个例外。[[raw/papers/vision/representation/ViT.pdf#page=6|p.6 表2及限制说明]]

## 4. 哪些消融真正解释了方法？

- **位置有用，但这一实验里复杂位置结构未显著占优**：ViT-B/16 ImageNet 5-shot，无位置0.61382，默认1D位置0.64206；2D、相对位置也约0.64。它支持“需要位置且普通可学习表足够”，不支持所有分辨率/任务都不需要二维编码。[[raw/papers/vision/representation/ViT.pdf#page=17|pp.17–18 D.4、表8]]
- **读出选择与学习率耦合**：图9中GAP用分类token的学习率表现差，调低学习率后接近。不能把一次未调参的差异解释为分类token独有的机制收益。[[raw/papers/vision/representation/ViT.pdf#page=17|p.17 图9]]
- **自监督是附加初探**：ViT-B/16遮块预测后ImageNet为79.9%，正文称比从零高2个百分点、比监督预训练低4个百分点。最终报告的是被扰动块的3-bit平均颜色分类；附录还试过缩小patch和全像素L2，不能写成“只研究了平均颜色”或“本文没有像素重建尝试”。[[raw/papers/vision/representation/ViT.pdf#page=9|p.9 §4.6]]；[[raw/papers/vision/representation/ViT.pdf#page=14|p.14 B.1.2]]

## 5. 限制、旧笔记校正与主题落点

**作者研究范围**主要是分类迁移；检测、分割与更强自监督列为后续工作。JFT属于非公开大数据，不能据此承诺普通公开数据训练也复现旗舰结果。作者内部注意力可视化揭示相关模式，不构成特定头具有可解释因果功能的证明。[[raw/papers/vision/representation/ViT.pdf#page=9|p.9 §5]]；[[raw/papers/vision/representation/ViT.pdf#page=20|p.20 D.7–D.8]]

**旧笔记差异**：保留其“先解释输入与迁移，再读实验”的顺序；把“大约9000万张前后”的说法收紧为特定模型、JFT子集和5-shot协议，不设通用数据阈值；把“混合前端只在小模型值得留”改为本组预算下的观测；去掉以位置相似度作为插值有效性的充分因果理由。明确原文也试过全像素L2目标，主结果仍是监督训练。旧稿不回写。

**本库整合主题**：视觉编码器的输入离散化与位置；归纳偏置与数据规模；表示评估中冻结探测、few-shot与整网微调的区别；理论FLOPs与硬件成本。实际主题与双向关系见页末。

**待检验问题**：当目标从整图分类变为细粒度定位、OCR或多模态语言生成时，哪些patch大小、空间编码和读出设计仍合适？这些问题不由本文分类分数回答。

## 实际整合关系

支撑patch计数、位置适配、数据规模与归纳偏置条件，并区分分类预训练和迁移读出。

- [[wiki/vision/Objectives-and-Transfer|视觉预训练：目标要求保留什么，迁移又读取什么？]]。
- [[wiki/vision/Resolution-and-Token-Budget|分辨率、packing与tiling：预算到底在哪个位置？]]。
