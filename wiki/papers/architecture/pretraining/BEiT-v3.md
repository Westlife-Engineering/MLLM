---
type: paper
source_id: S015
primary_direction: architecture/pretraining
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/architecture/pretraining/BEiT-v3.pdf]]"
reading_status: read
ingest_status: integrating
---

# BEiT-3：以 masked data modeling 统一视觉与视觉语言预训练

## 问题与核心认识

BEiT-3 问的是：图像、文本和图文对能否使用同一种“遮蔽后预测”任务，训练一套可切换为视觉编码器、双塔或融合编码器的骨干？它沿用 Multiway Transformer 的共享 self-attention 与模态专家 FFN，以离散视觉 token 和文本 token 为预测目标，联合利用单模态及配对数据。所谓把图像视为一种外语 **Imglish**，是统一建模的设计类比，不是关于图像天然具有自然语言语法的实验证明。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=2|p.2–4 · §1–2 / Figs.2–3]]

本文“只用一个目标”限定在**主预训练阶段**。检索主结果还使用 image-text contrastive learning 做中间微调；captioning、分类、检测与分割也各有任务适配。统一骨干不表示所有任务使用同一 attention 可见性、同一输出头或相同训练预算。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=4|p.4 · §2.2 / Fig.3]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=7|p.7–9 · §3.1–3.2]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=16|p.16 · Appendix A]]

## 来源、版本与阅读边界

| 项目 | 本次确认 |
| --- | --- |
| 标题 | Image as a Foreign Language: BEiT Pretraining for All Vision and Vision-Language Tasks |
| 作者 / 机构 | Wenhui Wang、Hangbo Bao、Li Dong（共同贡献），Johan Bjorck、Zhiliang Peng、Qiang Liu、Kriti Aggarwal、Owais Khan Mohammed、Saksham Singhal、Subhojit Som、Furu Wei；Microsoft Corporation |
| 版本 | arXiv:2208.10442v2，2022-08-31；[原件 URL](https://arxiv.org/pdf/2208.10442v2)。旧笔记文件名中的“2023-CVPR”不替代本地原件版本身份 |
| 原件 / 页数 | [[raw/papers/architecture/pretraining/BEiT-v3.pdf\|BEiT-v3.pdf]]，18 页 |
| SHA-256 | f02c366d9a3e02d744807fac11f5f89255aff2532108a0795d4ee2736c1376d4 |
| 阅读日期与范围 | 2026-10-31；正文 p.1–9、Appendix A–C p.16–18 已读；参考文献 p.10–15 仅定位，未逐篇独立核读 |
| 原页视觉核对 | p.3–9、16–18；Multiway 架构、任务路径、训练及结果表、检索中间微调对照、各任务附录参数均核看 |
| 旧笔记输入 | [[raw/notes/多模态经典/2023-CVPR-BEiT-v3总结.tex\|旧 TeX]]、[[raw/notes/多模态经典/Latex_out/2023-CVPR-BEiT-v3总结.pdf\|旧编译 PDF]]；正文已读、编译 PDF 全 4 页已核看；它们是二手理解输入 |
| 未做事项 | 未运行模型、复现实验或审计代码；未独立审计语料许可/可获取性；Obsidian 内显示未测 |

## 1. Multiway：共享运算与模态专门参数

### 1.1 同一骨干怎样形成不同接口

每层有共享 self-attention 与按模态选择的 FFN；全部 40 层有视觉 V-FFN 和语言 L-FFN，顶部 3 层另有 VL-FFN。单图像路径使用视觉专家，单文本路径使用语言专家；图文融合路径的底层按 token 模态分流到 V/L-FFN，顶层使用 VL-FFN。这个选择由任务输入和层位置决定，论文没有在这里报告内容驱动的 top-$k$ router 或负载均衡机制。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=3|p.3 · §2.1 / Fig.2]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=5|p.5 · §2.3]]

**专家分流与 attention 可见性是两件事。** 图文融合路径使用联合图文序列，底层 attention 已能交换图文信息；顶层 VL-FFN 不是第一次跨模态交互。双塔路径则独立编码两种模态，虽然 attention 参数共享，当前图像 token 与当前文本 token 并不在编码时互相读取。Fig.3 的五条路径应按这一差别阅读，不能理解为任意重排已经训练的层。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=4|p.4 · Fig.3(a–e)]]

| 路径 | 核心接口与用途 |
| --- | --- |
| Vision encoder | 视觉 token 经共享 attention 与 V-FFN，作为分类/检测/分割骨干 |
| Language encoder | 文本 token 经共享 attention 与 L-FFN，承担 masked language modeling |
| Fusion encoder | 联合图文序列，底部 V/L-FFN、顶部 VL-FFN，用于 masked vision-language modeling、VQA、NLVR2 |
| Dual encoder | 两种模态独立编码，以相似度匹配；检索适配可加对比目标 |
| Image-to-text generation | 联合输入配合非对称序列可见性，支持条件生成；不是普通全双向融合 mask |

[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=4|p.4 · Fig.3]]

### 1.2 模型规模不等于每次激活全部参数

模型有 40 层、hidden size 1,408、FFN intermediate size 6,144、16 attention heads。Table 2 给出总参数 1.9B，其中 V-FFN 692M、L-FFN 692M、VL-FFN 52M、共享 attention 317M；纯视觉编码只激活视觉相关部分，作者称约 1B、与 ViT-giant 可比。因此不能说“视觉与语言各占总参数的一半”：还存在共享参数与融合专家，表中列出的模块也不要求机械相加等于四舍五入后的总数。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=5|p.5 · Table 2 / Backbone Network]]

## 2. Masked data modeling 统一了什么

### 2.1 统一预测形式，保留不同目标空间

文本使用 64k 词表的 SentencePiece；图像输入仍由 patches 的 embeddings 表示，而 BEiT v2 tokenizer 产生的**离散视觉 token 是重建目标**。视觉任务不是直接回归 RGB 像素，也不能把目标 tokenizer 误当成用离散 token 取代所有图像输入 patch embeddings 的证据。图文对可借助另一模态的可见上下文预测被遮蔽内容。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=4|p.4 · §2.2 / Fig.3]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=5|p.5 · Pretraining Settings]]

为理解共同形式，可将训练概括为下式；这是**教学记号**，不是论文编号公式，也没有补入论文未明确展开的各数据源 loss 权重或输出头共享方式：

$$
\mathcal L_{\mathrm{MDM}}
=-\sum_{i\in\mathcal M}\log p_\theta(z_i\mid\widetilde x).
$$

$\mathcal M$ 是被遮蔽位置，$\widetilde x$ 是遮蔽后的单模态或图文输入；$z_i$ 在文本位置是词表 token，在视觉位置是离散视觉目标。共同点是预测被遮蔽单位，差异仍包括输入、目标词表、可用上下文与专家路径。这里包含 masked language modeling，不能写成“不需要 MLM”。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=4|p.4 · §2.2]]

| 数据 / 模态 | 遮蔽设置 |
| --- | --- |
| 单模态文本 | 随机遮蔽 15% tokens |
| 图文对中的文本 | 随机遮蔽 50% tokens |
| 图像 | 40% patches，采用 block-wise masking |

[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=4|p.4 · §2.2]]

较高的配对文本遮蔽率与跨模态条件预测相容，但本文没有给出一组控制其它条件不变的遮蔽率扫描，不能把“50% 比 15% 更能强迫看图”提升为本篇已独立验证的因果结论。预测离散视觉目标也不等于本文验证了高质量图像生成。

### 2.2 不依赖批内负例，不意味着 batch 不影响性能

主预训练没有同时优化 ITC、ITM 等目标；作者强调 mask-then-predict 可采用相对较小的 batch。实际 batch 为 6,144，对比文中列举的 CoCa 65k、CLIP 32k、Florence 24k。目标形式不要求以其它样本作为对比负例，是理解这一设计的理由；但优化稳定性、梯度估计与吞吐仍可能受 batch 影响。本文没有证明任意调整 batch 都不会改变性能，也没有报告全面的同预算 batch 敏感性实验。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=4|p.4 · §2.2 / footnote 2]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=5|p.5 · Pretraining Settings]]

## 3. 数据、初始化与主预训练预算

| 条件 | 本文报告 |
| --- | --- |
| 图文数据 | CC12M、CC3M、SBU、COCO、VG；约 15M 图像、21M 图文对 |
| 单图像数据 | ImageNet-21K，14M 图像 |
| 纯文本数据 | English Wikipedia、BookCorpus、OpenWebText、CC-News、Stories；160GB documents |
| 每步数据组成 | 2,048 图像 + 2,048 文本 + 2,048 图文对，共 6,144 样本 |
| 训练长度 / 图像 | 1M steps；$224\times224$ 输入、$14\times14$ patch |
| 优化 | AdamW，$\beta=(0.9,0.98)$、$\epsilon=10^{-6}$；峰值学习率 $10^{-3}$、10k steps warmup、cosine decay、weight decay 0.05 |
| 正则 / 位置 | dropout 关闭，drop path 0.1；Table 11 标明不使用 relative positional embeddings |

[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=5|p.5 · §2.3 / Table 3]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=16|p.16 · Appendix B / Table 11]]

由分辨率与 patch 大小可算出 $16\times16=256$ 个图像 patches；这是几何推算，不包含额外特殊 token。作者称数据 academically accessible，是原文的数据可得性表述，不是本次独立完成的许可审计。相对小的 batch 也不能单独推出总算力低：模型有 1.9B 参数并训练 1M 步，本文未报告足以在这里确认的完整设备数量、总墙钟时长与全任务适配总成本。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=5|p.5 · Tables 2–3 / Pretraining Settings]]

这里的 **BEiT initialization algorithm** 指随机初始化后，按层深度 $l$ 将 attention 与 FFN 子层的输出矩阵缩放 $1/\sqrt{2l}$；它不是“加载已训练 BEiT 权重”的同义词。这与 VLMo 先采用 BEiT 预训练参数、再固定 attention 学语言专家的阶段策略不同。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=5|p.5 · footnote 4]] 参见 [[wiki/papers/architecture/pretraining/VLMo|VLMo（S014）]]。

## 4. 任务适配如何改变信息流

### 4.1 VQA 与 NLVR2：联合编码后的分类

VQA 将图像和问题联合编码，再用池化表示预测 3,129 个候选答案中的类别；本文不是不受候选集限制的自由生成 VQA。VQAv2 微调分辨率为 $756^2$、10 epochs、batch 128，test-dev/test-std 分别为 84.19/84.03。不能把 VLMo Large++ 的 $768^2$ 直接套到本篇。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=6|p.6 · §3.1 / Table 4]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=17|p.17 · Table 12]]

NLVR2 将一个文本与两张图分别构成两个图文对，经融合后拼接池化表示做分类。微调输入为 $224^2$、20 epochs、batch 256；dev/test-P 为 91.51/92.58。它与 VQA 的样本结构、分辨率和答案接口不同，分数不能当作同一“理解能力”量尺。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=6|p.6 · §3.1 / Table 4]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=17|p.17 · Table 12]]

### 4.2 Captioning：非对称可见性避免读取未来答案

Captioning 借用 sequence-to-sequence masking：**图像 token 可以双向读取图像，不能读取 caption；caption token 可以读取图像、左侧文本与自身位置。** 训练随机遮蔽 caption token（包括结束用的 [SEP]），预测时受上述可见性约束；推理按顺序生成文本。图像侧不可读取 caption 这一点很关键，否则未来文本可能通过图像表示间接泄漏给当前文本位置。后一句是对 mask 作用的教学解释。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=6|p.6–7 · §3.1 / Image Captioning]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=4|p.4 · Fig.3(e)]]

COCO 使用 Karpathy split；微调分辨率 $392^2$、16k steps、batch 256、caption mask probability 0.6、label smoothing 0.1，推理 beam size 3。Table 4 报告 BLEU-4 44.1、METEOR 32.4、CIDEr 147.6、SPICE 25.4，未做 CIDEr 强化学习优化。该表 CoCa 的 METEOR 为 33.9，不能把 BEiT-3 写成每个 captioning 指标都领先；不同数据、规模与适配预算也未统一。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=6|p.6 · Table 4]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=17|p.17 · Table 13]]

### 4.3 检索：双塔接口与额外对比训练必须同时说明

检索分别编码图像和文本，以 cosine similarity 比较，可预计算各自向量。主预训练使用 MDM，随后可在下游以 ITC 微调；主表还在下游微调之前，额外使用预训练图文对做 **5 epochs、batch 16k、$224^2$ 输入**的对比式 intermediate fine-tuning，峰值学习率 $3\times10^{-5}$。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=7|p.7 · §3.1 / Image-Text Retrieval]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=16|p.16 · Appendix A]]

| Table 10 的 R@1 对照 | 直接下游微调 | 加中间对比微调后再下游微调 |
| --- | --- | --- |
| COCO 5k test，image→text | 82.7 | 84.8 |
| COCO 5k test，text→image | 65.1 | 67.2 |
| Flickr30k 1k test，image→text | 97.5 | 98.0 |
| Flickr30k 1k test，text→image | 89.1 | 90.3 |

[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=16|p.16 · Table 10]]

这组实验支持“MDM 得到的骨干可以经对比微调用于双塔检索”，并量化了额外中间训练的收益；左列也经过下游对比微调，不能解释成“从未使用对比目标”。主表的 Flickr30k zero-shot R@1 为 94.9/81.5，同样基于中间对比训练，zero-shot 指不在该目标检索集上训练，不表示原始 MDM 权重未经任何适配。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=7|p.7 · §3.1 / Image-Text Retrieval / Table 6]]

下游检索微调分辨率为 $420^2$、batch 3k；COCO 15 epochs、Flickr30k 20 epochs，峰值学习率均为 $10^{-5}$。这一流程与 ALBEF 的双塔筛选后融合重排不同，也不能只用最终 R@1 对训练或推理效率下结论。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=17|p.17 · Table 14]] 参见 [[wiki/papers/architecture/pretraining/ALBEF|ALBEF（S011）]]。

## 5. 纯视觉结果的条件与证据边界

| 任务 | 适配与评估条件 | 代表结果 |
| --- | --- | --- |
| COCO detection / instance segmentation | ViTDet 式 feature pyramid/window attention 与 Cascade Mask R-CNN；先 Objects365 中间训练，再 COCO；推理使用 soft-NMS、多尺度评估；最大训练图像尺寸 1,280 | box AP 63.7、mask AP 54.8 |
| ADE20K semantic segmentation | ViT-Adapter 与 Mask2Former；150 类，896 crop；区分单尺度与多尺度推理 | mIoU 62.0 single-scale、62.8 multi-scale |
| ImageNet-1K classification | 把类别文本与图像做双塔匹配；先 ImageNet-21K 中间微调，再 ImageNet-1K；推理可缓存类别文本特征；最终输入 $336^2$ | top-1 89.6 |

[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=8|p.8–9 · §3.2 / Tables 7–9]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=18|p.18 · Tables 15–17]]

这些数字不属于“同一个预训练权重零样本直接完成全部视觉任务”：Objects365 中间检测训练为 15 epochs，COCO 再训练 20 epochs；分割训练 80k steps；分类先在 ImageNet-21K 训练 50 epochs，再在 ImageNet-1K 训练 15 epochs。任务头、adapter、额外监督和评估分辨率都是最终性能条件。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=18|p.18 · Appendix C]]

ImageNet 的 89.6 强调公开 image-tag 数据条件，不能与使用私有 JFT 的 CoCa 91.0 脱离数据与训练流程直接排序。检测表的历史对照还依赖作者当时引用的排行榜快照，不表示当前排名。本文展示广泛任务适配，但没有对每项性能增益分别隔离规模、数据、MDM、模态专家和下游训练的作用；Appendix A 的检索中间微调对照不能替代所有这些消融。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=8|p.8–9 · Tables 7–9]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=16|p.16 · Appendix A]]

## 6. 旧理解修订与跨来源联系

| 旧笔记说法 | 本次原文核读后的修订 |
| --- | --- |
| 不需要 ITC、ITM、MLM 等任务 | 主预训练统一为 MDM，包含文本 MLM；检索中间/下游微调仍使用 ITC |
| 视觉与语言参数各一半 | 区分两类 FFN、共享 attention 和 VL-FFN；纯视觉仅激活相关参数 |
| 只有最后三层才开始图文融合 | 底层联合 attention 已交互；顶部三层增加 VL-FFN |
| 已训练模块可以随意拼装 | 原文展示规定的专家路径与任务 mask，不证明任意层排列都有效 |
| 图像 tokenizer 的离散序列就是全部输入 | 图像 patch embeddings 是输入，离散视觉 token 是 MIM 预测目标 |
| batch 可以自由调整且不影响性能 | 无批内负例依赖不等于无 batch 敏感性；论文未给该强结论 |
| 使用 BEiT 初始化就是加载 BEiT 模型 | 此处是随机初始化及按层缩放输出矩阵的算法 |
| 没有新内容 / 不是真正 foundation model / CNN 无法适配其它模态 | 属于旧笔记评价或泛化推断，不是本文受控实验结论；本页保留具体机制、结果与局限 |

与 [[wiki/papers/architecture/pretraining/VLMo|VLMo（S014）]] 相比，BEiT-3 继承模态专家骨干，但将多种单模态/图文预训练统一到 masked prediction，并采用联合大规模主预训练；二者不能只凭相似架构图认为训练策略相同。与 [[wiki/papers/architecture/pretraining/ALBEF|ALBEF（S011）]]、[[wiki/papers/architecture/pretraining/BLIP|BLIP（S012）]] 相比，本篇主预训练不使用它们的 ITC+ITM 组合；与 [[wiki/papers/architecture/pretraining/CoCa|CoCa（S013）]] 相比，本篇也没有在主预训练采用 contrastive+autoregressive captioning 双目标。这里比较的是训练机制，不是用异条件成绩推断优劣。

可整合到主题的问题包括：统一目标与统一接口的区别；attention 可见性和 FFN 路由如何共同决定信息流；主预训练与中间适配应怎样计入性能条件；离散视觉目标与文本目标的共性和差异。待核问题是同等模型、数据及总预算下 MDM 与多目标方法的差别，以及哪些收益来自扩大单模态数据。作者在结尾提出 multilingual、audio 与 in-context learning 等未来方向，本篇没有完成这些能力的验证。[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=9|p.9 · §4]]
