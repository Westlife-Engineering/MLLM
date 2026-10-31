---
type: paper
source_id: S009
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/vision/alignment/SigLIP.pdf]]"
primary_direction: vision/alignment
reading_status: read
ingest_status: complete
---

# SigLIP：把批内选择改成逐对判别，究竟改变了什么？

> [!abstract] 核心理解
> SigLIP 保留图像/文本双编码器和正负配对监督，把 CLIP 的双向 batch softmax 改成每个图文对的 sigmoid 二分类。去掉跨候选的归一化后，损失可逐块累加、可单独控制负例配对；这不代表“不需要负样本”“完全没有跨设备通信”或“batch 大小不再影响学习”。作者在明确的模型、数据及训练长度下发现，小 batch 尤其受益，约32k已接近较佳区域，百万 batch 的收益有限。[[raw/papers/vision/alignment/SigLIP.pdf#page=3|pp.3–4 §3、Fig.1–2]]

## 来源、版本与实际读取

- **身份**：Xiaohua Zhai、Basil Mustafa、Alexander Kolesnikov、Lucas Beyer，*Sigmoid Loss for Language Image Pre-Training*；arXiv:2303.15343，本轮固定 **v4**，PDF 共17页，页码与印刷页一致。题名/作者对照首页，版本按固定下载 URL 与登记记录确认。
- **原件**：[[raw/papers/vision/alignment/SigLIP.pdf]]；[arXiv v4](https://arxiv.org/pdf/2303.15343v4)；SHA-256：2efade8de3baeffe9eba759aab9f510ea8f8ac3c365f02f0da75d9baf9ffa2db，本次重算一致。
- **2026-10-31 阅读**：正文 pp.1–10，附录 pp.14–17；参考文献仅定位，不扩读被引工作。视觉核查 pp.2、3、4、7、8、9、14 的算法、损失公式、分块图、batch/负例曲线和主结果/消融表；附录逐语言表未逐格视觉审核。不声称复现或代码审计；Obsidian 内显示未测。
- **旧笔记输入**：[[raw/notes/视觉编码器/SigLIP总结.tex]] 与 [[raw/notes/视觉编码器/Latex_out/SigLIP总结.pdf]]；核对 TeX 中公式、分块表述和结果主张，编译版不另算来源。

## 从“在这一批里选谁”到“这一对是否匹配”

[[wiki/papers/vision/alignment/CLIP|CLIP]] 的两次 softmax 分别沿图像和文本候选集合归一化。SigLIP 的图像向量 $u_i=f(I_i)/\|f(I_i)\|_2$、文本向量 $v_j=g(T_j)/\|g(T_j)\|_2$ 仍处在共同空间；$N$ 个原始图文样本构成 $N^2$ 个组合，对角线上是正对，其他组合标为负对。原文明说这是 noisy and imperfect 的负例假设：不同网页样本仍可能语义匹配。[[raw/papers/vision/alignment/SigLIP.pdf#page=2|p.2 §3]]、[[raw/papers/vision/alignment/SigLIP.pdf#page=3|p.3 §3.1–3.2]]

以下**统一采用 Algorithm 1 的偏置符号约定**：

$$
a_{ij}=\exp(t')u_i^\top v_j+b,\qquad
z_{ij}=\begin{cases}+1&i=j\\-1&i\ne j,\end{cases}
$$

$$
\mathcal L_{\rm sigmoid}
=-\frac1N\sum_{i=1}^{N}\sum_{j=1}^{N}
\log\sigma(z_{ij}a_{ij})
=\frac1N\sum_{i,j}\log(1+\exp(-z_{ij}a_{ij})).
$$

$\sigma(q)=1/(1+e^{-q})$；$t'$ 和 $b$ 都可学习，默认初始值分别为 $\log 10$、$-10$。正对需要较大 logit，负对需要较小 logit；没有沿行/列跨候选的 softmax 分母。原文用 **$1/N$**，并不是对 $N^2$ 项做均值。数学上每项可独立求值，但共享编码器仍使所有训练样本通过参数更新关联。“对称”表示交换图文角色不会产生另一套不同的归一化损失，不是要求图像和文本编码器相同。[[raw/papers/vision/alignment/SigLIP.pdf#page=2|p.2 Algorithm 1]]、[[raw/papers/vision/alignment/SigLIP.pdf#page=9|p.9 §4.9、Table 4]]

> [!warning] 固定版本内的公式冲突
> v4 的 p.3 展示式指数为 $z_{ij}(-t\,u_i^\top v_j+b)$，而 p.2 Algorithm 1 的 logit 是 $t\,u_i^\top v_j+b$，再计算 log-sigmoid(label × logit)，后者展开的指数是 $-z_{ij}(t\,u_i^\top v_j+b)$。两者对 $b$ 的符号不一致。只有把两式的 bias 重定义为相反数才能对应，但原文同时指定 $b=-10$。本页保留该冲突，以算法和负偏置抑制初始负例损失的解释为书写约定，未冒称已核对作者代码。旧 TeX 照录了展示式，因此不能直接把其公式与 Algorithm 1 的参数值混用。

负偏置为何有用？一个 batch 只有 $N$ 正对，却有 $N(N-1)$ 负对；初始相似度接近0时，$b=-10$ 使初始匹配概率很小，减少海量负对驱动的大幅初始校正。Table 4 在 B 模型、batch8k、9亿 seen examples 下，加入初始化为−10的 bias 后 ImageNet 零样本为63.0%，无bias为62.0%；这支持该初始化配方，不能证明每个数据分布都应固定−10。[[raw/papers/vision/alignment/SigLIP.pdf#page=9|p.9 §4.9、Table 4]]

## 分块节省的是什么？

设有 $D$ 台设备，每台本地 batch 为 $m=N/D$（这里用 $m$ 避免与 bias $b$ 混淆）。先计算本地图像与本地文本的 $m\times m$ 项，含对角正例；然后跨设备轮换文本表示，计算其他块中的负例，最终累加。Fig.1 的三个设备、每台4样本只是示意；最终仍覆盖全局12×12配对。[[raw/papers/vision/alignment/SigLIP.pdf#page=3|pp.3–4 §3.3、Fig.1]]

独立损失使中间相似度矩阵不必一次全部驻留：图示把相似度工作块从 $N^2$ 减为 $m^2$。**这不是整体模型显存都只剩 $m^2$，也没有把全部配对计算自动从二次变线性**；仍要存模型/激活、交换表示并累积梯度。作者实现避免 full all-gather，使用 collective permute，仍有通信。论文对朴素 softmax 的效率比较不应写成“任何 softmax 实现都必须全矩阵常驻”的下界。[[raw/papers/vision/alignment/SigLIP.pdf#page=4|p.4 §3.3]]

## batch、样本和配对必须分别计量

增大 batch 同时增加每步原始样本数、每个正例的负例数和每步配对数；固定累计 seen examples 时，更新步数反而减少。Sigmoid 的可加性让作者可以 mask 某些负对，研究“更多样本”与“更多配对”的差异，但并没有彻底去掉优化与采样的相互影响。大 batch 若 schedule 过短，可能来不及完成足够更新。[[raw/papers/vision/alignment/SigLIP.pdf#page=5|p.5 Fig.3]]、[[raw/papers/vision/alignment/SigLIP.pdf#page=8|pp.8–9 §4.8]]

| 实验分支 | 固定条件 | 结果及其范围 |
| --- | --- | --- |
| **SigLiT**：锁定预训练视觉塔，仅训练文本塔 | ViT-g 预计算图像特征，288×288；B 文本塔；LiT图文数据；18B seen examples | 从512到约1M batch；32k后增益较小，256k/1M附近约84.7%。不是双塔从零训练的百万batch实验。[[raw/papers/vision/alignment/SigLIP.pdf#page=4\|§4.1]]、[[raw/papers/vision/alignment/SigLIP.pdf#page=14\|pp.14–15 §A、Table 8]] |
| **SigLIP**：两塔从零训练的受控loss比较 | WebLI英文；ViT-B/16、B文本塔；224×224；16文本tokens；9B seen examples | batch4k：68.4 vs66.6；32k：73.4 vs72.9；307k：71.6 vs72.6，分别为sigmoid/softmax。不是每个batch都胜出。[[raw/papers/vision/alignment/SigLIP.pdf#page=5\|p.5 §4.2]]、[[raw/papers/vision/alignment/SigLIP.pdf#page=14\|p.14 Table 5]] |
| **mSigLIP**：多语言两塔训练 | WebLI约100语言；Base规模；30B seen examples；XM3600 36语言平均T→I R@1 | 32k为34.9，240k降至32.7；ImageNet约73.2后趋平。多语言数据不必然要求更大batch，但此结论限本配方。[[raw/papers/vision/alignment/SigLIP.pdf#page=5\|pp.5–6 §4.3、Table 2]] |
| 小设备 **SigLiT** | 冻结ViT-g/14 + Large文本塔，20k batch，107k步；4 TPUv4、约2天 | ImageNet84.5%；预训练视觉骨干和预计算并非免费的从零成本，不能与CLIP全模型预训练天数直接作同成本比较。[[raw/papers/vision/alignment/SigLIP.pdf#page=6\|p.6 §4.4]] |

表中的 seen examples 是累计输入样本次数，不是独立数据集大小，更不是 $N^2$ 配对数。附录 Table 7 的5次重复在32k、3B设置下为 softmax $69.9\pm0.1$、sigmoid $70.1\pm0.2$，表明该设置差异很小；不能把小batch的优势概括成全部训练条件下的大幅提升。[[raw/papers/vision/alignment/SigLIP.pdf#page=14|p.14 §C、Table 7]]

## 负例越均衡越好？困难负例越多越好？

§4.8 在固定16k batch的 SigLiT 中屏蔽负例，从约1:16k到接近平衡的1:1.6。随机减少负例会降低表现，只留容易负例更差；保留困难负例较能维持质量。另一路为匹配总配对量而延长训练，所以其提升伴随更长训练预算，不能称为免费收益，也不能把“只留困难负例”自动当作可直接部署的高效挖掘算法。[[raw/papers/vision/alignment/SigLIP.pdf#page=7|p.7 Fig.6]]、[[raw/papers/vision/alignment/SigLIP.pdf#page=8|pp.8–9 §4.8]]

这一节原文写“900 M steps”，与多处其他实验的“900 M examples”用语不同；本页不擅自把这项消融改成已确认的样本预算，也不据此计算实际更新次数。结果支持“原配方的正负不平衡没有明显阻止学习”，并不表示负例质量不重要或 false negatives 已解决。

噪声实验使用 M/16 图像塔与 M 文本塔、batch16,384、3.6B seen examples，分别注入随机图像、随机文本、配对打乱及组合噪声；sigmoid保留相对优势。它测的是这些人为噪声机制，而非穷尽真实网络错误、语义歧义或所有OOD鲁棒性。[[raw/papers/vision/alignment/SigLIP.pdf#page=9|p.9 §4.10、Fig.7]]、[[raw/papers/vision/alignment/SigLIP.pdf#page=15|p.15 §E]]

## 发布模型的高分，不能全部归给换损失

Table 3 的较强模型来自另一个扩展配方：40B seen examples、32k batch、256 image patches、64文本tokens，并为目标分辨率继续5B样本、学习率降100倍且不再weight decay。B、L、So400m以及不同patch数不能混为同一成本。作者报告 L/16、256 patches 的 ImageNet80.5%，576 patches为82.1%；So400m、729 patches为83.2%。这些是论文自身比较中的结果，其数据、训练长度、架构及分辨率与其他公开模型不一致。**支持损失贡献的主要证据应看受控 softmax 对照，而非跨模型排行榜。**[[raw/papers/vision/alignment/SigLIP.pdf#page=7|p.7 §4.6]]、[[raw/papers/vision/alignment/SigLIP.pdf#page=8|p.8 Table 3]]

本文也包含训练工程条件：把 Adam/AdaFactor 的 $\beta_2$ 从0.999调到0.95缓解大batch梯度尖峰；从已有视觉权重继续训练时，作者在所测配置中移除该视觉塔的weight decay并使用0.1学习率倍数。两项均不能省略后再把全部结果算到sigmoid本身。[[raw/papers/vision/alignment/SigLIP.pdf#page=6|pp.6–8 Figs.4–5、§4.5/4.7]]

## 旧笔记修订与可继续追问的问题

旧 TeX 对逐对二分类的主线基本正确，但需补上：$1/N$归一化、bias展示式冲突、分块只节省中间矩阵、SigLiT与SigLIP训练成本不同，以及排行榜不是单变量消融。旧稿“全面超越先前模型”改为原作者在Table 3特定模型/任务集合中的比较主张。

本库已经可以与 [[wiki/papers/vision/alignment/CLIP|CLIP]] 比较**训练目标的归一化范围**，不能把两篇原始表格直接拼成同条件性能结论。建议主题落点：图文对齐、负例构造、分布式训练的内存/通信、受控实验与预算。未解问题包括：固定唯一数据、总计算与优化步数后的loss效应；高效困难负例筛选如何同时处理假负例；逐对全局对齐是否足够支持局部dense features。后一个问题需要新的原文证据。

## 实际整合关系

支撑逐对sigmoid的归一化/负例假设，以及分块中间矩阵、通信与全配对计算的区别。

- [[wiki/vision/Objectives-and-Transfer|视觉预训练：目标要求保留什么，迁移又读取什么？]]。
- [[wiki/efficiency/Resource-Ledger|资源账本：视觉token、激活参数、KV与系统预算分别省在哪里？]]。
