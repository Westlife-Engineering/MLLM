---
type: paper
source_id: S008
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/vision/representation/CLIP.pdf]]"
primary_direction: vision/representation
reading_status: read
ingest_status: complete
---

# CLIP：从批内图文配对到由文字生成分类器

> [!note] 主归属（本库导航判断）
> 包含视觉与文本两侧的成对表示及文字分类接口，不能将 representation 理解成只有视觉塔。 [[raw/papers/vision/representation/CLIP.pdf#page=2|pp.2–4，Fig.1/§2]]

> [!abstract] 核心理解
> CLIP 学习两个可分别运行的编码器，让图像与文本在共同空间中可比较。训练是批内双向配对，零样本分类则把候选类别的文字描述编码成分类器权重。它展示了大规模自然语言监督的迁移价值，但“零样本分数高”“视觉特征好”“适应分布变化”是三个需要分别验证的判断。它不是生成式聊天模型，也没有在本文中把局部视觉定位作为训练目标。依据：[[raw/papers/vision/representation/CLIP.pdf#page=2|p.2 Fig.1]]、[[raw/papers/vision/representation/CLIP.pdf#page=6|p.6 §3.1.2]]。

## 来源身份与阅读范围

- **论文**：Alec Radford、Jong Wook Kim 等，*Learning Transferable Visual Models From Natural Language Supervision*，2021；本地为 arXiv:2103.00020 **v1，2021-02-26**，共 48 页。题名、首作者、版本标识已对照首页；以下页码均为 PDF 页码，本版与正文印刷页相同。
- **原件**：[[raw/papers/vision/representation/CLIP.pdf]]；登记 URL：[arXiv v1 原文](https://arxiv.org/pdf/2103.00020v1) 。原件 SHA-256：`6478b6e571a7d6fcd846d8ef77bfd60c285f1986abb8f475eedc43de403074f5`，本次重算一致。
- **2026-10-31 实际阅读**：正文 pp.1–20（引言、方法、迁移实验、稳健性、人类比较、重叠检测及局限）；补读 pp.21–24 社会偏差讨论；附录 pp.37–38 线性评估协议、p.44 去重及数据消融、pp.45–48 检索/OCR/动作/定位及超参数。关键原页视觉核查：pp.2、3、5、7、8、12、16、44、46、48。
- **未穷尽范围**：pp.25–27 后续 broader impacts/讨论未逐段核读，参考文献未逐条追溯；pp.39–43 全量逐数据集表格和定性图片未逐格审核。未复现、未审计代码；Obsidian 内显示未测。`read` 仅指本页登记的阅读范围；摄入状态见页首。
- **旧笔记输入**：[[raw/notes/多模态经典/2021-ICML-CLIP.md]]、[[raw/notes/多模态经典/2021-ICML-CLIP总结.tex]]、[[raw/notes/多模态经典/Latex_out/2021-ICML-CLIP总结.pdf]] 为冻结二手材料；本次重点核对 Markdown 解释与 TeX 身份，不把旧编译 PDF 另计学术来源。

## 为什么用配对，而不直接预测整段配文？

网页配文可以描述对象、动作、地点、文字等，也可能只和图像松散相关。逐词预测要求模型解释具体措辞，而 CLIP 把任务收窄为“这一批文字里，哪段原本与这张图成对”。作者在早期 ResNet-50 等设置中发现：词袋预测的零样本 ImageNet 学习效率高于 Transformer caption baseline，词袋上的对比目标又进一步提高效率。Fig.2 的横轴是**处理过的图像数**，不能把图中的 3×、4×读成最终大模型的固定 wall-clock 加速或所有 captioning 方法的普遍下界。[[raw/papers/vision/representation/CLIP.pdf#page=3|p.3 Fig.2]]、[[raw/papers/vision/representation/CLIP.pdf#page=4|p.4 §2.3]]

训练数据 WIT 为约 4 亿图文对，来自公开网络来源；构建时使用约 50 万查询，每个查询最多保留 2 万对以缓和不平衡。这是自然语言监督，不能因没有人工整理的下游类别标签就称“完全没有监督”。图文配对也不保证句句准确。[[raw/papers/vision/representation/CLIP.pdf#page=3|pp.3–4 §2.1–2.2]]

## 一个 batch 内，谁在和谁竞争？

设 batch 有 $N$ 个原始图文对 $(x_i,t_i)$。图像与文本分别经编码器和线性投影，得到 L2 归一化向量 $u_i,v_i$。令

$$
s_{ij}=\alpha u_i^\top v_j,\qquad \alpha=\exp(a)>0.
$$

这里 $a$ 是可学习的 logit scale 参数，不是图像特征；$s_{ij}$ 是缩放后的 cosine similarity。对角线 $i=j$ 是数据中提供的正配对；其他 $N^2-N$ 对按训练构造当作负配对，并不意味着语义上绝对不匹配。按照 §2.3 与 Fig.3，双向损失可展开为：

$$
\mathcal L_{\rm CLIP}=-\frac{1}{2N}\sum_{i=1}^{N}
\left[\log\frac{\exp(s_{ii})}{\sum_{j=1}^{N}\exp(s_{ij})}
+\log\frac{\exp(s_{ii})}{\sum_{j=1}^{N}\exp(s_{ji})}\right].
$$

第一项让每张图在 **本 batch 的 $N$ 段文本**间选择；第二项让每段文本在 **本 batch 的 $N$ 张图**间选择。每个方向都含 softmax 分母，改变竞争候选会影响同一正对的归一化概率。$1/(2N)$ 是两个方向、每个方向 $N$ 个分类问题的平均，不是 $N^2$ 个独立二分类的平均。[[raw/papers/vision/representation/CLIP.pdf#page=4|p.4 §2.3]]、[[raw/papers/vision/representation/CLIP.pdf#page=5|p.5 Fig.3]]

> [!note] 公式的边界
> 把“配对拉近、错配推远”当直觉可以，但它不能替代分母。CLIP 的训练约束是相对批内候选的双向分类；后续 sigmoid 方法逐对判别时，其数学耦合与归一化范围发生变化，不能只说“把 softmax 函数换一个名字”。上式是依据原文伪代码的等价展开。

两端均从头训练：视觉端比较改造的 ResNet 与 ViT，文本端是带 causal mask 的 Transformer，取 EOS 位置表示，再投影到共同空间。线性投影不等于跨模态 token 融合；图文直到相似度计算才相遇。原文 §2.4 写最大序列长为 76，此处应理解为 **token 序列**，不是“76 个英文单词”。本版正文词表数 49,152 与附录表18的 49,408 存在出入，本文保留版本内差异，未用未核查实现强行消解。[[raw/papers/vision/representation/CLIP.pdf#page=5|p.5 §2.4]]、[[raw/papers/vision/representation/CLIP.pdf#page=48|p.48 Table 18]]

## 零样本推理：类别名怎样变成权重？

给定目标数据集的候选类别，把每类写成提示语，例如 `A photo of a {label}.`；编码后得到每类向量 $w_k$。对输入图像的归一化表示 $u$，比较 $u^\top w_k$，可用温度缩放与候选类别上的 softmax 输出分布。这相当于**归一化输入、归一化权重、无偏置的线性分类器**，权重由文本编码器生成，可以预先缓存。此时 softmax 的候选集合是目标类别，不是训练 batch。[[raw/papers/vision/representation/CLIP.pdf#page=6|p.6 §3.1.2]]

提示语解决的具体问题包括词义歧义和预训练/推理的文本分布差异：`boxer` 可能是狗或拳击手，宠物上下文帮助消歧。作者还在 embedding 空间平均同类的多个提示；ImageNet 使用 80 个提示，避免每张图重复计算所有文本。简单模板相对裸类名提升约 1.3 个百分点，80 提示集成相对该模板再提升约 3.5 个百分点；这些是论文条件下的结果。作者承认开发过程中反复查询验证集，因此不能把 zero-shot 理解成“整个开发流程从未接触过任何目标任务反馈”。[[raw/papers/vision/representation/CLIP.pdf#page=7|pp.7–8 §3.1.4]]、[[raw/papers/vision/representation/CLIP.pdf#page=20|p.20 §6]]

## 实验支持到哪里？

通用训练设置为 batch 32,768、32 epochs、Adam 加解耦 weight decay、cosine learning-rate schedule；logit scale 初始对应温度 0.07，缩放因子上限为 100。ViT-L/14 基础训练分辨率 224，再以 336 多训一轮，默认最优结果为 **ViT-L/14@336px**。4 亿独立样本与 32 轮累计约 128 亿次图像呈现必须区分。最大 ViT 的基础训练报告为 256 张 V100、12 天；不同视觉结构和分辨率不共享同一成本。[[raw/papers/vision/representation/CLIP.pdf#page=5|p.5 §2.5]]、[[raw/papers/vision/representation/CLIP.pdf#page=48|p.48 Tables 18–20]]

| 问题与协议 | 原文结果 | 能得出的结论与限制 |
| --- | --- | --- |
| ImageNet 零样本，ViT-L/14@336px、文字分类器 | top-1 76.2%，接近原版监督 ResNet-50；Table 1 的早期零样本参照为 Visual N-Grams | 展示可用的零样本迁移；数据、模型及计算未匹配，不能由此单独识别损失的贡献。[[raw/papers/vision/representation/CLIP.pdf#page=7\|p.7 Table 1、比较限制]] |
| 27 数据集，零样本 CLIP 对监督 ResNet-50 特征线性分类器 | 16/27 胜出，CLEVRCounts、EuroSAT 等明显落后 | 对手是特定旧基线，不是每个任务的最佳系统。[[raw/papers/vision/representation/CLIP.pdf#page=8\|p.8 Fig.5]] |
| 20 个每类至少16样本的数据集，冻结特征 few-shot logistic regression | 零样本平均约等于相同 CLIP 特征的4-shot | 仅是这组协议上的均值，不是“每类天然等效4张图”；各任务差异很大。[[raw/papers/vision/representation/CLIP.pdf#page=9\|pp.9–10 Figs.6–8]] |
| 冻结特征，全数据 linear probe；12与27数据集套件 | 最佳 CLIP 对最佳被评估旧模型的平均优势约2.6和5个百分点 | 不是端到端微调结果；27套件与作者开发共同演进，存在选择偏差。[[raw/papers/vision/representation/CLIP.pdf#page=12\|p.12 Fig.10]]、[[raw/papers/vision/representation/CLIP.pdf#page=38\|p.38 §A.3]] |
| RN50，过滤 YFCC 与等大 WIT 子集，各32轮 | 平均迁移相近，具体数据集差异可很大 | 支持不完全依赖 WIT 的特定来源；不证明任意数据质量均可，也不控制完整4亿规模。[[raw/papers/vision/representation/CLIP.pdf#page=44\|pp.44–45 Table 12、§D]] |

线性评估使用冻结表示、L-BFGS 拟合 logistic regression，并在验证划分上选择 L2 正则；CLIP-ViT 用投影到共同空间之前的特征。它测试的是特征的线性可分性，不能把它与直接用文本向量的零样本结果混成同一种推理协议。[[raw/papers/vision/representation/CLIP.pdf#page=38|p.38 §A.3]]

## 稳健性为何不能写成一个已经证明的因果故事？

作者在 7 个自然分布变化数据集上区分 **relative robustness**（OOD 分数提高）和 **effective robustness**（超出由 ID 分数预测的 OOD 水平）。零样本 CLIP 的 effective robustness 较高；把相同特征适配到 ImageNet 标签后，ImageNet 从 76.2% 提高到 85.4%，但平均分布变化分数略降，ImageNetV2 则上升。[[raw/papers/vision/representation/CLIP.pdf#page=13|pp.13–16 §3.3、Fig.14]]

**原文谨慎结论**：这一干预提示目标分布适配会改变稳健性，但作者没有确定数据规模、多样性、自然语言监督、特征与线性适配的各自因果贡献，也未据此证明所有端到端微调都会损害泛化。**本库推断**：评价 MLLM 视觉底座时，不能仅以 ImageNet 适配后的分数代替开放概念/分布转移能力；应保留实际适配协议。[[raw/papers/vision/representation/CLIP.pdf#page=14|pp.14–16 §3.3]]

## 失败、数据重叠与任务边界

CLIP 在计数、部分细粒度识别、低分辨率/手写数字和不常见于网络配文的任务上明显薄弱。Table 14 中零样本 MNIST 为 88.4%、SVHN 完整数字识别为 51.0%；这并非一般 OCR 转录系统。检索也须分方向：Table 13 的 **text retrieval 是给图找文**，image retrieval 是给文找图；Flickr30k 上接近当时微调最好结果的是前者，不能反读。MSCOCO 为 5k 测试集，零样本与微调结果分列。[[raw/papers/vision/representation/CLIP.pdf#page=19|pp.19–20 §6]]、[[raw/papers/vision/representation/CLIP.pdf#page=46|p.46 Tables 13–14]]

重叠分析使用 **RN50x64**，在35个数据集上先检测近重复，再比较完整集和清洁子集；作者检测到的总体准确率最大增量约0.6个百分点。但检测器无法确认对4亿数据的整体召回率，重叠/清洁子集也可能难度不同；结论是本检测协议下影响较小，不能保证无污染。[[raw/papers/vision/representation/CLIP.pdf#page=18|pp.18–19 §5、Fig.17]]、[[raw/papers/vision/representation/CLIP.pdf#page=44|p.44 §C]]

候选类别和措辞不仅影响准确率，也影响偏差表现；正文的 class-design 探针显示增减类别能显著改变错误分布，不能把某套标签上的高分类准确率当作部署公平性的证明。[[raw/papers/vision/representation/CLIP.pdf#page=22|pp.22–23 §7.1]]

## 对旧笔记的修订与本库落点

1. 旧导读的“更稳是因为没有拟合 ImageNet”改成上面的**实验观察与未完成归因**，保留其他解释。
2. “一句最长76个词”改为原文报告的 token 序列长度；同时登记 v1 词表数字的内部不一致，不混用后续实现。
3. 旧导读把 Flickr30k 接近最好结果的检索方向写反：原表是 **给图找文**。零样本分类、检索、冻结特征回归各自记录，不统称同一种 zero-shot 能力。
4. “不会框出物体”限定为**本文方法没有直接的检测输出/局部监督验证**；不能外推为任何基于 CLIP 的后续系统均不能定位。

本库整合主题：视觉表示与图文对齐、对比损失的归一化范围、零样本评估与提示、分布变化下的迁移。本页保持唯一来源入口，实际主题关系见页末。待检验问题是：在固定数据、模型和算力下，批内竞争与逐对判别分别如何影响对齐、负例敏感性和局部特征；本论文不能单独回答。

## 实际整合关系

支撑批内双向softmax、文本类别接口和zero-shot/冻结probe的不同评估。

- [[wiki/vision/Objectives-and-Transfer|视觉预训练：目标要求保留什么，迁移又读取什么？]]。
