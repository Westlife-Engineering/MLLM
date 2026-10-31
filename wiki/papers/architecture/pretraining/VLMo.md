---
type: paper
source_id: S014
primary_direction: architecture/pretraining
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/architecture/pretraining/VLMo.pdf]]"
reading_status: read
ingest_status: integrating
---

# VLMo：共享注意力、模态专家与两种任务接口

## 问题与核心认识

双塔编码便于预先保存图像和文本向量，适合大规模检索；融合编码可让图文 token 在多层网络中互相读取，适合条件理解。VLMo 希望两种接口来自同一套预训练骨干，使用 **Mixture-of-Modality-Experts（MoME）**：同层 self-attention 参数共享，FFN 按模态与层位置选择视觉、语言或视觉语言专家。其另一个重点是先利用单图、纯文本语料，再进行图文预训练。[[raw/papers/architecture/pretraining/VLMo.pdf#page=1|p.1–3 · §1 / Fig.1]]

最容易混淆的两点必须先分开：**共享 attention 权重不等于所有运行方式都有跨模态 token 交互；专家不同也不等于图文在 attention 中彼此隔离。** 双塔模式分别编码，融合模式拼接图文并从底层共享 self-attention 开始交互；顶层 VL-FFN 增强联合处理，不是首次出现跨模态信息的地方。[[raw/papers/architecture/pretraining/VLMo.pdf#page=3|p.3–5 · Figs.1、3 / §3.2]] [[raw/papers/architecture/pretraining/VLMo.pdf#page=16|p.16 · Appendix A]]

## 来源、版本与阅读边界

| 项目 | 本次确认 |
| --- | --- |
| 标题 | VLMO: Unified Vision-Language Pre-Training with Mixture-of-Modality-Experts |
| 作者 / 机构 | Hangbo Bao、Wenhui Wang（共同贡献）、Li Dong、Qiang Liu、Owais Khan Mohammed、Kriti Aggarwal、Subhojit Som、Furu Wei；Microsoft |
| 版本 | arXiv:2111.02358v2，2022-05-27；本地用户原件；[原件 URL](https://arxiv.org/pdf/2111.02358v2) |
| 原件 / 页数 | [[raw/papers/architecture/pretraining/VLMo.pdf\|VLMo.pdf]]，16 页 |
| SHA-256 | 636d9dfd99492bdf57e2ec517f5587af7fcdc7dcb3470a6cddc68f53cdb2e5ee |
| 阅读日期与范围 | 2026-10-31；正文 p.1–10、Appendix A–D p.16 已读；参考文献 p.10–15 只定位，未逐篇独立核查 |
| 原页视觉核对 | p.3–5、7–10、16；架构/训练阶段、公式、结果及消融表、附录原页已看 |
| 旧笔记输入 | [[raw/notes/多模态经典/2022-NeurIPS-VLMo总结.tex\|旧 TeX]]、[[raw/notes/多模态经典/Latex_out/2022-NeurIPS-VLMo总结.pdf\|旧编译 PDF]]；机制正文已读并对照，编译 p.7–9、12 核看 |
| 未做事项 | 未运行模型/复现/审计官方代码；旧笔记引用的外部 BEiT 教学资料不升级为本篇直接证据；Obsidian 内显示未测 |

## 1. MoME 中“共享”与“专门处理”如何组合

### 1.1 输入与残差块

图像切成 patches，经线性投影，加 [I_CLS]、可学习一维位置编码与 image type embedding；文本使用 **WordPiece** 分词，加入 [T_CLS]、[T_SEP]、文本位置与类型编码。融合输入是两种序列的拼接 $H_0^{vl}=[H_0^w;H_0^v]$。位置编码使同一 attention 运算能够区分不同位置，类型编码提供模态信息；不能因为核心运算统一，就说模态和位置从此无关。[[raw/papers/architecture/pretraining/VLMo.pdf#page=4|p.4 · §3.1]]

原文 MoME block 保留 pre-norm 与残差：

$$
H'_l=\mathrm{MSA}(\mathrm{LN}(H_{l-1}))+H_{l-1},
\qquad
H_l=\mathrm{MoME\!-\!FFN}(\mathrm{LN}(H'_l))+H'_l.
$$

与标准 Transformer 的主要差异是 FFN 的选择，self-attention 在同一层的不同模态/任务调用之间复用。这里不表示所有深度层共用同一份参数。[[raw/papers/architecture/pretraining/VLMo.pdf#page=4|p.4 · §3.2 / Eqs.1–2]]

### 1.2 专家是按规则选择，不是学习一个任意路由器

| 运行输入 / 层段 | Attention 实际读取对象 | FFN 使用方式 |
| --- | --- | --- |
| 纯图像，全部层 | 这张图像的 token 序列 | V-FFN |
| 纯文本，全部层 | 这段文本的 token 序列 | L-FFN |
| 图文融合，底部 $L-F$ 层 | 拼接后的图像与文本 token | 图像 token 走 V-FFN，文本 token 走 L-FFN |
| 图文融合，顶部 $F$ 层 | 同一联合 token 序列 | VL-FFN 处理联合表示 |

[[raw/papers/architecture/pretraining/VLMo.pdf#page=3|p.3 · Fig.1]] [[raw/papers/architecture/pretraining/VLMo.pdf#page=5|p.5 · §3.2 / Fig.3]]

用“按模态/层位置的 hard routing”概括这种规则是合理的机制解释，但本文没有报告内容驱动的可学习 top-$k$ router、负载均衡损失或自动搜索最佳专家组合。并非每个 token 都先计算三个 FFN 再加权融合。视觉语言输入的底层虽然走不同 FFN，attention 之前已能读到另一模态的信息；“底层 V-FFN 的输入只含原始视觉信息”也不准确。

Base 共 12 层，顶部 2 层使用 VL-FFN；Large 共 24 层，顶部 3 层使用 VL-FFN。因此“后两层才融合”既误解信息流，也把 Base 的配置套到了 Large。[[raw/papers/architecture/pretraining/VLMo.pdf#page=6|p.6 · §4.1]]

### 1.3 用 task mask 理解可见性时，哪些是教学补充

原文的 ITC 路径画成独立图像、独立文本编码，融合任务画成联合输入。若为解释而把两段序列写在一张 attention 矩阵中，双塔的等价可见性可表示为只保留图像—图像与文本—文本块、屏蔽交叉块；融合则允许交叉块。**这只是等价计算语义的教学说明，本论文没有据此报告“实现必然拼接输入并使用某张 block-diagonal mask”。** 旧笔记将这种实现猜测写成实验事实，本页不沿用。[[raw/papers/architecture/pretraining/VLMo.pdf#page=3|p.3 · Fig.1]] [[raw/papers/architecture/pretraining/VLMo.pdf#page=5|p.5 · Fig.3]]

同样，MLM 的 [MASK] 是输入 token 被遮蔽，不是自回归 causal attention mask。该任务仍从可见上下文与图像恢复遮蔽词；本文没有以 captioning loss 训练自由文本生成。[[raw/papers/architecture/pretraining/VLMo.pdf#page=5|p.5 · §3.3]] [[raw/papers/architecture/pretraining/VLMo.pdf#page=10|p.10 · §5 展望]]

## 2. 图文预训练目标与全局难负例

ITC 分别取图像 [I_CLS] 与文本 [T_CLS]，投影并归一化后计算点积相似度。以图到文方向为例：

$$
s_{ij}=\hat h_i^{v\top}\hat h_j^w,\qquad
p_i=\frac{\exp(s_{ii}/\sigma)}{\sum_j\exp(s_{ij}/\sigma)}.
$$

学习两个方向的交叉熵，$\sigma$ 是可学习温度。同批 $N$ 对样本产生 $N^2-N$ 个非配对候选。该任务作用于独立表示，使之后检索可以缓存两侧特征。[[raw/papers/architecture/pretraining/VLMo.pdf#page=5|p.5 · §3.3 / Eqs.3–4]]

MLM 在文本上使用 15% masking，并采用 whole-word masking；联合图文编码后对被遮蔽位置做词表分类。ITM 则对融合后的 [T_CLS] 做图文匹配二分类。三个目标共享 MoME 参数，但运行模式和输入可见性不同；不能把三个 loss 合在一起的说法理解为所有任务只执行相同的一次输入路径。[[raw/papers/architecture/pretraining/VLMo.pdf#page=5|p.5–6 · §3.3、§4.1]]

ITM 按 ITC 相似度抽取 hard negatives，扩展点在于候选从所有 GPU 收集。论文将 ALBEF 式单 GPU 候选称为 local，而 VLMo 的跨 GPU 候选称为 global。Table 6 在 32 张 V100、每卡 32、总 batch 1,024 的控制中，local 只有 32 个候选、global 有 1,024 个，NLVR2 test-P 77.95→79.48。这个“global”指当次分布式训练批次，不是从完整训练语料中检索全部样本。对 ALBEF 的实现描述属于本论文的比较，本次没有代码审计来推广到所有版本。[[raw/papers/architecture/pretraining/VLMo.pdf#page=6|p.6 · §3.3]] [[raw/papers/architecture/pretraining/VLMo.pdf#page=10|p.10 · Table 6]]

## 3. Stagewise pre-training：先得到什么，再固定什么

Fig.2 的顺序是：

1. **视觉阶段**：利用 BEiT 的 masked image modeling 预训练结果，初始化 self-attention 与视觉专家；原文说实际直接使用 BEiT 预训练参数。
2. **纯文本阶段**：冻结 self-attention 与视觉专家，在纯文本上以 MLM 学习语言专家。
3. **图文阶段**：从上述参数开始，用 ITC+MLM+ITM 训练整个 MoME，建立对齐与联合理解。

[[raw/papers/architecture/pretraining/VLMo.pdf#page=4|p.4 · Fig.2]] [[raw/papers/architecture/pretraining/VLMo.pdf#page=6|p.6 · §3.4]]

这表明在本文配置中，固定来自视觉预训练的 attention、再训练语言专家，是一个可用的初始化方式。它不证明视觉 attention 天生比语言 attention 更通用，不证明文本只能建模局部依赖，也不证明反向迁移在所有设置下都失败。原文借用 ViLT 的初始化观察属于对其它论文的转述；本次不能把旧笔记关于“2D 比 1D 更强”的因果故事当作 VLMo 已验证结论。[[raw/papers/architecture/pretraining/VLMo.pdf#page=9|p.9 · §4.6 / Stagewise Pre-Training]]

纯文本阶段使用 English Wikipedia 与 BookCorpus，最大序列长 196，batch=1,024，峰值学习率 $2\times10^{-4}$；Base 500k 步、Large 200k 步。图文表格的“4M 图像”没有包含这些纯文本训练及 BEiT 初始化成本。原文没有在本篇完整重述 BEiT 的全部训练数据与预算，也未在这里明确列全每个新专家的初始化细节；不从旧教学补充填成已核事实。[[raw/papers/architecture/pretraining/VLMo.pdf#page=16|p.16 · Appendix B]]

## 4. 模型、数据与下游设置

| 条件 | 本文报告 |
| --- | --- |
| Base | 12 层、hidden 768、12 heads、FFN intermediate 3,072；顶部 2 层 VL-FFN |
| Large | 24 层、hidden 1,024、16 heads、FFN intermediate 4,096；顶部 3 层 VL-FFN |
| 常规图文语料 | CC、SBU、COCO、VG；约 4M 图像、10M 图文对。此配对统计与其它论文不可按相同数据集名直接视为相同处理版本 |
| 常规图文训练 | $224^2$ 分辨率、patch $16^2$、文本最长 40；200k 步、batch 1,024、AdamW |
| 报告计算量 | 图文阶段 Base 约 2 天/64 张 V100 32GB，Large 约 3 天/128 张 V100 32GB；不是完整三阶段总成本 |
| Large++ | 1B noisy web pairs；200k 步 batch 16k，再 100k 步 batch 32k，不能与常规 Large 当成同预算 |

[[raw/papers/architecture/pretraining/VLMo.pdf#page=6|p.6–7 · §4.1–4.2]]

VQA2 被设为 3,129 个答案的分类，融合 [T_CLS] 输入分类头。NLVR2 将一个文本—两图三元组改为两个图文对，分别融合后拼接两个 [T_CLS] 再分类。常规 VQA 微调图像分辨率 $480^2$，Large++ 提高到 $768^2$；NLVR2 主表使用 $384^2$。因此 Large++ 的 VQA 增益同时伴随数据、batch 与下游分辨率变化，不能归因于某一个因素。[[raw/papers/architecture/pretraining/VLMo.pdf#page=7|p.7 · §4.3]] [[raw/papers/architecture/pretraining/VLMo.pdf#page=16|p.16 · Appendix C]]

检索微调仅用 ITC，推理直接比较独立向量，没有 ITM 重排。COCO 使用 $384^2$、batch 2,048，Base 微调 20 epochs、Large 10 epochs。主表 Flickr30k 使用 COCO 微调模型初始化后，再在 Flickr30k 微调 40 epochs；不是 Flickr 零样本。消融则用 $224^2$、更短训练；不能将消融行与主表直接相减解释某个组件收益。[[raw/papers/architecture/pretraining/VLMo.pdf#page=6|p.6 · §3.5]] [[raw/papers/architecture/pretraining/VLMo.pdf#page=16|p.16 · Appendix D]]

独立编码确实把昂贵的编码计算从每个图文组合移到每个单项。但若显式算全体 $N$ 图、$M$ 文的相似度矩阵，点积数量仍为 $NM$；原文“linear vs quadratic”的直观比较针对重型联合编码次数，不能改写成全量检索端到端计算必为线性。原文未给统一硬件/索引/候选规模下的端到端延迟表。[[raw/papers/architecture/pretraining/VLMo.pdf#page=1|p.1 · §1]] [[raw/papers/architecture/pretraining/VLMo.pdf#page=8|p.8 · §4.4]]

## 5. 结果与消融支持的具体判断

### 5.1 主结果不意味着每列都胜过融合模型

4M 配置 Base 的 VQA test-std=76.89、NLVR2 test-P=83.34；Large 为 79.98、86.86；1B Large++ 为 82.78、89.54。它们都是下游微调结果，并包含上文不同预算/分辨率条件。[[raw/papers/architecture/pretraining/VLMo.pdf#page=7|p.7 · Table 1]]

Base 在 COCO 5k test 检索 TR/IR R@1=74.8/57.2，在 Flickr30k 1k test 为 92.3/79.3。Table 2 的 ALBEF-Base 对应 Flickr30k 为 94.3/82.8，高于 VLMo-Base，但 ALBEF 使用融合重排。准确结论是 VLMo 展示了有竞争力的纯双塔检索接口，不能写成“所有检索指标都超过融合编码器”。[[raw/papers/architecture/pretraining/VLMo.pdf#page=8|p.8 · Table 2]]

视觉任务中 VLMo-Base 的 ImageNet top-1=85.5、ADE20K mIoU=53.4，相比 BEiT-Base 的 85.2/52.8 略高；两者均做 ImageNet-21k intermediate fine-tuning。此结果不能被描述成预训练权重直接 zero-shot 分割，也不足以单独证明跨模态训练在任意纯视觉任务上必有收益。[[raw/papers/architecture/pretraining/VLMo.pdf#page=8|p.8–9 · §4.5 / Table 3]]

### 5.2 哪些设计有对应消融

| 对照 | 代表证据与条件 |
| --- | --- |
| 加纯文本预训练 | NLVR2 test-P 81.06→82.49；Flickr IR mean recall 87.69→88.52。是初始化策略对照；p.9 Table 4 |
| 标准 Transformer → MoME | 三个任务均启用时，NLVR2 test-P 79.27→80.31；Flickr TR/IR 均值 93.37/85.73→95.17/87.25。该组用 ViT-Base 初始化；p.9–10 Table 5 |
| 去除 VL expert → 完整 MoME | NLVR2 test-P 80.11→80.31；结果支持顶层 VL-FFN 的增益，但不是跨模态交互首次发生的证据；p.10 Table 5 |
| 仅 ITC → 三目标 | NLVR2 test-P 58.83→80.31；融合任务监督显著重要，不能归为单纯检索目标自动产生同等联合理解；p.10 Table 5 |
| 独立 attention → 共享 attention | 前 $L-F$ 层使用独立权重时 test-P=78.95，共享时 80.31；支持本文架构中的共享，不证明 attention 与模态完全无关；p.16 Table 7 |

[[raw/papers/architecture/pretraining/VLMo.pdf#page=9|p.9–10 · §4.6 / Tables 4–6]] [[raw/papers/architecture/pretraining/VLMo.pdf#page=16|p.16 · Appendix A / Table 7]]

这些消融的 Flickr TR/IR 是 R@1、R@5、R@10 的**平均值**；NLVR2 消融平均 3 次运行，但表中没有给标准差。主表和消融的分辨率、训练长度、初始化不完全相同，不能将所有数字混成同一条连续加组件实验。

## 6. 旧理解修订与整合建议

| 旧笔记说法 | 原文核读后的修订 |
| --- | --- |
| 文本沿用 BPE | 本文明确 WordPiece / uncased BERT tokenizer；不额外复制旧文本投影维度公式 |
| 只有最后两层做模态融合 | 融合路径底层 attention 已交互；顶层使用 VL-FFN；Large 顶部为三层 |
| ITC 实验一定把图文拼起来再加 mask | 原文只确认独立编码接口；block-diagonal mask 可作等价教学说明，不能冒充实现审计 |
| attention 在“前后层”都共享 | 共享是同层不同模态/任务调用间共享，不是跨深度层参数绑定 |
| 自动调度最优专家组合 | 按模态与层段硬选择，未报告学习型 router |
| 视觉 attention 天生更通用，文本主要局部/无法空间建模 | 无对应控制证据；删去这些强因果解释，保留具体阶段训练事实 |
| attention 参数和模态无关 | 本文只支持该模型、任务和训练配置下共享有效 |
| 详细 BEiT tokenizer/遮蔽算法都由 VLMo 验证 | VLMo 采用 BEiT 初始化；旧笔记的外部教学扩展单独降级，不冒充本篇实验 |

与 [[wiki/papers/architecture/pretraining/ALBEF|ALBEF（S011）]] 比较，VLMo 在融合时用拼接序列的 self-attention 承担图文交互，而不是单独的文本查询图像 cross-attention 模块；两者都有 ITC/ITM/MLM，但参数复用与阶段初始化不同。与 [[wiki/papers/architecture/pretraining/BLIP|BLIP（S012）]]、[[wiki/papers/architecture/pretraining/CoCa|CoCa（S013）]] 比较，VLMo 本篇重点是理解/检索与可共享骨干，captioning 仍列为未来工作，不能据“统一”一词补出已验证生成能力。

可整合的问题包括模态专家路由与 attention 可见性的独立设计、单模态资源怎样初始化多模态网络、候选规模与负例难度、检索重型编码成本与全库打分成本。未解决的问题包括同等总预算下阶段预训练与联合从头训练的比较、共享 attention 对其它模态的边界，以及更大图文数据与阶段初始化之间是否存在可替代关系；本篇没有覆盖全部对照。
