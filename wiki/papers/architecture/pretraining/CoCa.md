---
type: paper
source_id: S013
primary_direction: architecture/pretraining
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/architecture/pretraining/CoCa.pdf]]"
reading_status: read
ingest_status: complete
related_directions:
  - vision/alignment
  - architecture/generation
---

# CoCa：在一次计算图中保留对比表示和条件生成

## 问题与核心认识

CoCa（Contrastive Captioners）希望一个预训练模型同时提供三种接口：视觉分类所需的图像表示、检索所需的独立图文表示、联合理解与生成所需的图文融合表示。关键困难在于：对比学习需要不依赖候选图像的文本向量，captioning 却需要图像条件下的 token 表示。CoCa 将同一个因果文本 decoder 分成两段，前段不读取图像、后段增加 cross-attention，于是一次前向就能取得两种表示。[[raw/papers/architecture/pretraining/CoCa.pdf#page=2|p.2 · Fig.1]] [[raw/papers/architecture/pretraining/CoCa.pdf#page=4|p.4–5 · §3.2 / Fig.2]]

本文的“统一”还包括把图像分类标签写成文本，与网页 alt-text 一起使用 contrastive + captioning 两个目标训练。它不需要先单独训练视觉分类器再接语言模块，但训练仍使用巨量数据与计算；“增添第二个目标的开销很小”不等于模型的总训练便宜。不同下游结果也分别来自 zero-shot、冻结骨干训练任务头、全模型微调，不能称作一个未经适配的模型直接完成了所有任务。[[raw/papers/architecture/pretraining/CoCa.pdf#page=5|p.5–7 · §3.2–4.1]]

## 来源与实际阅读

| 项目 | 本次确认 |
| --- | --- |
| 标题 | CoCa: Contrastive Captioners are Image-Text Foundation Models |
| 作者 / 机构 | Jiahui Yu、Zirui Wang（共同贡献）、Vijay Vasudevan、Legg Yeung、Mojtaba Seyedhosseini、Yonghui Wu；Google Research |
| 版本 | arXiv:2205.01917v2，2022-06-14；首页标 Preprint；[原件 URL](https://arxiv.org/pdf/2205.01917v2) |
| 原件 / 页数 | [[raw/papers/architecture/pretraining/CoCa.pdf\|CoCa.pdf]]，19 页 |
| SHA-256 | ebb8ecad1667502a8e016241b499b2479e296d59c7df06abdedb5cb51d26457b |
| 阅读日期与范围 | 2026-10-31；正文 p.1–13、Appendix A–B p.18–19 已读；p.13–17 参考文献仅定位，没有逐篇独立验证 |
| 原页视觉核对 | p.2、4–7、9–12、18；架构、伪代码、公式、结果/关键消融及附录超参表已核看 |
| 旧笔记输入 | [[raw/notes/多模态经典/2022-CoCa总结.tex\|旧 TeX]]、[[raw/notes/多模态经典/Latex_out/2022-CoCa总结.pdf\|旧编译 PDF]]；机制正文已对照，编译 PDF p.1–3 原页已看；代码部分非本次审计对象 |
| 验证边界 | 未运行训练、官方代码或复现；原文结果按作者报告登记；Obsidian 内显示未测 |

## 1. 解耦 decoder 的信息流

### 1.1 前半段必须保留纯文本表示

图像经过 ViT 成为视觉 token 序列。文本以开始符和词序列输入，末尾附加一个可学习 [CLS] token：

- 前 $n_{\mathrm{uni}}$ 层只有 causal self-attention 与文本变换，不能读取图像；末尾 [CLS] 因为位于整句之后，可以汇总此前全部文本，其输出用于对比学习。
- 后 $n_{\mathrm{multi}}$ 层继续使用 causal self-attention，并通过 cross-attention 读取视觉表示；它们输出各位置的下一词预测，用于 captioning。
- Fig.2 的伪代码将末尾 [CLS] 输出用于对比，把其余文本位置送入多模态段。默认两段层数相同。

[[raw/papers/architecture/pretraining/CoCa.pdf#page=4|p.4–5 · Fig.2、Algorithm 1 / §3.2]]

两段都用因果 mask，故前半段已经算出的词表示能直接供后半段使用，不必为了 MLM 再构造一份被遮蔽文本。训练采用 teacher forcing：完整目标序列可并行送入模型，但每个位置被 mask 限制，不能偷看它要预测的未来词。推理生成仍逐 token 进行。“训练一次前向”不能解释为一轮前向就能自由生成任意长度句子。[[raw/papers/architecture/pretraining/CoCa.pdf#page=4|p.4 · Eq.3 / Encoder-Decoder Captioning]] [[raw/papers/architecture/pretraining/CoCa.pdf#page=5|p.5 · Pretraining Efficiency]]

解耦指输入信息与输出用途的分工，不表示梯度完全互不影响。Captioning 使用前半段产生的表示，因此两个目标共享和共同更新部分计算图；本文也通过目标权重消融检查这种协作。所谓“保证互不干扰”超出了论文证据。[[raw/papers/architecture/pretraining/CoCa.pdf#page=11|p.11–12 · §4.3 / Table 8]]

### 1.2 Attentional pooler：query 数量不是向量维数

Pooler 是一个 multi-head attention 层：可学习 queries 向视觉 tokens 提问，后者作为 keys/values，输出与 query 数量相同的一组表示。对比需要 1 个全局向量，生成需要保留细粒度信息的 256 个视觉向量。**1 与 256 是 query/token 数量，不是 embedding 维数。** 也不是把一组 256 个输出切成“第一个用于对比、剩下 255 个用于生成”。[[raw/papers/architecture/pretraining/CoCa.pdf#page=5|p.5 · Attentional Poolers]]

Fig.2 画的是两个 pooler 并联读取 ViT 输出。§4.3 又明确比较了 parallel 与 cascade，并说明**所有正式 CoCa 默认采用 cascade：先生成 256 个 generative pooler 输出，再由 contrastive pooler 从其上提取 1 个对比向量**。原图可帮助理解任务接口，但具体默认连接应以该实验说明为准。[[raw/papers/architecture/pretraining/CoCa.pdf#page=4|p.4 · Fig.2]] [[raw/papers/architecture/pretraining/CoCa.pdf#page=12|p.12 · Table 8(f) / Attentional Poolers]]

这也不应自动类比成强压缩：基础预训练输入为 $288\times288$、patch size $18\times18$，本来就是 256 个图像 token；256-query pooler 此时主要学习重组视觉表示。更高分辨率时输入长度另变，不能把所有配置统一说成相同比例压缩。[[raw/papers/architecture/pretraining/CoCa.pdf#page=5|p.5 · §3.2]]

## 2. 两个训练目标与标签文本化

对 batch 中 $N$ 对图文，令 $x_i,y_i$ 为归一化图像/纯文本向量，$\sigma$ 为温度。论文对比目标是两个方向之和：

$$
\mathcal L_{\mathrm{Con}}=-\frac1N\sum_i\left[
\log\frac{\exp(x_i^\top y_i/\sigma)}
{\sum_j\exp(x_i^\top y_j/\sigma)}
+\log\frac{\exp(y_i^\top x_i/\sigma)}
{\sum_j\exp(y_i^\top x_j/\sigma)}
\right].
$$

它将配对项与同批其它候选对比，使用全局表示；无需先对每个候选运行图文融合。生成目标则要求逐词预测：

$$
\mathcal L_{\mathrm{Cap}}=-\sum_t
\log P_\theta(y_t\mid y_{<t},x),\qquad
\mathcal L_{\mathrm{CoCa}}=
\lambda_{\mathrm{Con}}\mathcal L_{\mathrm{Con}}+
\lambda_{\mathrm{Cap}}\mathcal L_{\mathrm{Cap}}.
$$

正式训练采用 $\lambda_{\mathrm{Con}}=1$、$\lambda_{\mathrm{Cap}}=2$。这是 **ITC/contrastive 与 captioning**，没有另外加入 ITM 二分类损失。对比温度可学习，初值 0.07。[[raw/papers/architecture/pretraining/CoCa.pdf#page=4|p.4–5 · Eqs.2–4]] [[raw/papers/architecture/pretraining/CoCa.pdf#page=7|p.7 · §4.1]]

数据来自 JFT-3B 的图像标签与 ALIGN 的网页 alt-text。JFT 的多个类名随机排序、拼接，再加采样提示，如 “a photo of the cat, animal”。这样原本离散类标签也能参与相同两个文本目标。作者将分类交叉熵视作“词表由类别名称构成时”的生成特例；这是解释统一监督接口的观点，不意味着现实中的多 token 类名序列与每种分类损失都数值等价。[[raw/papers/architecture/pretraining/CoCa.pdf#page=5|p.5 · Eq.4 后说明]] [[raw/papers/architecture/pretraining/CoCa.pdf#page=6|p.6 · §4.1 / Data]]

相关消融在 JFT 上比较分类与 captioning 预训练：linear evaluation 为 81.0 对 82.1，微调为 85.1 对 84.9。结果说明生成监督能形成有用视觉表示，但不是 captioning 对分类训练在所有评测上严格占优。[[raw/papers/architecture/pretraining/CoCa.pdf#page=11|p.11–12 · Table 8(a)]]

## 3. 规模与预算：结构简洁不等于低成本

| 版本 | 图像 encoder 层数 / 参数 | 文本 uni+multi 层数 / 参数 | 总参数 |
| --- | --- | --- | --- |
| CoCa-Base | 12 / 86M | 12+12 / 297M | 383M |
| CoCa-Large | 24 / 303M | 12+12 / 484M | 787M |
| CoCa（最大版） | 40 / 1B | 18+18 / 1.1B | 2.1B |

[[raw/papers/architecture/pretraining/CoCa.pdf#page=5|p.5 · Table 1]]

模型端到端从头训练，不从预训练图像/语言编码器初始化。Batch size=65,536，每批 JFT 与 ALIGN 各占一半；500k 步，大约对应 JFT 5 epochs、ALIGN 10 epochs。使用 Adafactor、weight decay=0.01，前 2% 步数 warmup 至 $8\times10^{-4}$ 后线性下降。最大版预训练约 5 天、2,048 Cloud TPU v4 chips；之后又在 $576\times576$ 分辨率继续预训练 1 epoch。“单阶段”是同时从头学习模块与目标的说法，不能隐去后续高分辨率继续训练。[[raw/papers/architecture/pretraining/CoCa.pdf#page=6|p.6–7 · §4.1]]

作者报告沿既有去重程序移除 3.6M 与下游近域相关的图像。这是作者的数据处理报告，本次没有获取完整训练集或重新执行去重，因此不能把它升级为独立验证的“完全无污染”。论文也明确 zero-shot 不采用传统“预训练绝未出现相关类别监督”的严格定义，而是转移阶段不使用目标任务监督样本。[[raw/papers/architecture/pretraining/CoCa.pdf#page=6|p.6 · §3.3、§4.1]]

## 4. 消融怎样支持设计

Table 8 使用缩小实验：CoCa-Base 骨架，但 decoder 总层数减至 12、batch size=4,096。**不能把这些数直接当作 2.1B 正式模型结果。**

| 目标 | ImageNet zero-shot top-1 | VQA dev | 相对 TPU 成本 |
| --- | --- | --- | --- |
| 仅 contrastive | 70.7 | 59.2 | 1.00× |
| 仅 captioning | 不提供该对比式接口 | 68.9 | 1.17× |
| CoCa 双目标 | 71.6 | 69.0 | 1.18× |

这里的成本以 TPUv3-core-days 比较，说明在该配置中双目标只比已有 captioner 增加很少开销，仍高于纯对比模型。纯对比基线用于 VQA 时需要额外融合模块，因此 VQA 差异不只是一行 loss 系数改变的纯控制。[[raw/papers/architecture/pretraining/CoCa.pdf#page=11|p.11–12 · §4.3 / Table 8(b)]]

权重比 $\lambda_{\mathrm{Cap}}:\lambda_{\mathrm{Con}}=2:1$ 比 1:1、1:2 在所列两项上更好；作者猜测生成监督有助于细粒度文本表示。总 12 层时，3/9、6/6、9/3 的 uni/multi 分配对两项任务有不同影响，6/6 是本文折中，不是已证明的架构定律。[[raw/papers/architecture/pretraining/CoCa.pdf#page=12|p.12 · Table 8(c–d)]]

视觉生成接口只剩 1 个 query 时，VQA 为 64.4；32 个为 68.2；默认 256 个为 69.0。不使用 generative pooler、直接用所有 ViT token（表中 $n_{\mathrm{query}}=0$）也为 69.0。因此该实验更支持“保留足够视觉信息”，不能说只有 pooler 才能实现细粒度理解。Parallel 与 cascade 分别为 zero-shot 71.2/71.6、VQA 68.7/69.0，作为选择默认串联的依据。[[raw/papers/architecture/pretraining/CoCa.pdf#page=12|p.12 · Table 8(f)]]

## 5. 三类适配与结果不能混用

### 5.1 图像分类：86.3、90.6 与 91.0 对应不同监督

Zero-shot 分类使用类别名称及提示的文本向量，与图像向量比较，最大版 ImageNet top-1=86.3；冻结图像骨干后**训练新的 attentional pooler 与分类头**得到 90.6；再微调骨干得到 91.0。90.6 不是线性探针结果，也不是完全不训练任何参数。若比较视觉 encoder 参数效率，还需记住预训练整个 CoCa 的 2.1B 参数与文本训练成本。[[raw/papers/architecture/pretraining/CoCa.pdf#page=7|p.7–9 · Table 2、§4.2.1、Table 4]] [[raw/papers/architecture/pretraining/CoCa.pdf#page=18|p.18 · Appendix A]]

实现复用前还需解决原文超参差异：正文 §4.2.1 说微调 encoder 用 $10^{-4}$，Appendix A Table 9 列出 $5\times10^{-4}$；正文对 frozen-feature 的 batch 概述与 ImageNet 附录配置也不完全相同。本页保留这项待核，不凭经验选择一个数字当作实际复现配置。[[raw/papers/architecture/pretraining/CoCa.pdf#page=8|p.8 · §4.2.1]] [[raw/papers/architecture/pretraining/CoCa.pdf#page=18|p.18 · Table 9]]

### 5.2 检索：真正的独立表示，且目标划分要对齐

图文检索完全冻结预训练模型，用对比训练接口的独立向量计算全测试集 cosine similarity，不调用多模态 decoder 重排。最大版 Flickr30k 1k test 图→文/文→图 R@1=92.5/80.4，COCO 5k test 为 66.3/51.2。这与 ALBEF、BLIP 先做 COCO 检索微调后转移的“Flickr zero-shot”协议不同，不能按名称相同直接排优劣。[[raw/papers/architecture/pretraining/CoCa.pdf#page=9|p.9 · §4.2.2 / Table 3]]

视频检索平均 16 个均匀采样帧的向量，再与文本向量比较。MSR-VTT 使用 full split 中当时仍可取得视频的**子集**；作者对部分基线重新计算相同 subset 结果。Table 5 CoCa subset 的文→视频 R@1=30.0、视频→文 R@1=49.9，不能直接与 BLIP 的 MSRVTT 1k test 数字比较，也不能把 subset 当完整测试集。可取得样本的完整清单与本次独立去重审计均未完成。[[raw/papers/architecture/pretraining/CoCa.pdf#page=6|p.6 · §3.3]] [[raw/papers/architecture/pretraining/CoCa.pdf#page=9|p.9–10 · Table 5 前说明]]

### 5.3 联合理解与生成：有 decoder 不代表所有任务自由生成

VQA、SNLI-VE 与 NLVR2 在最终 decoder 表示上再用 pooler 和线性分类头微调。VQA 是训练集最常见 **3,129 个答案**的分类，并额外在问答拼接文本上共同训练生成损失。NLVR2 分别构造两张图与相同描述的输入对，将表示拼给分类器；不是在此任务中直接生成任意解释。最大版 VQA test-std=82.3、SNLI-VE test=87.1、NLVR2 test-p=87.0，均依赖这些下游训练。[[raw/papers/architecture/pretraining/CoCa.pdf#page=10|p.10 · §4.2.3 / Table 6]] [[raw/papers/architecture/pretraining/CoCa.pdf#page=18|p.18–19 · Appendix B]]

Captioning 在 COCO 上仅用 captioning 交叉熵微调，不做 CIDEr 专项强化优化；报告 COCO Karpathy test CIDEr=143.6，NoCaps validation/test=122.4/120.6。Table 7 也列了使用 CIDEr 优化的方法，二者训练条件不同。Fig.6 是作者挑选的生成示例，不能当成整体幻觉率或 OCR 正确率评测。[[raw/papers/architecture/pretraining/CoCa.pdf#page=10|p.10–11 · §4.2.3 / Table 7、Fig.6]]

视频动作识别逐帧使用图像编码器，再训练任务 pooler 聚合空间与帧 tokens；冻结或微调骨干属于不同设置。预训练只用图像，不等于下游视频结果没有视频标签监督；它也没有在早期视觉编码中进行时序融合。[[raw/papers/architecture/pretraining/CoCa.pdf#page=6|p.6 · Fig.3]] [[raw/papers/architecture/pretraining/CoCa.pdf#page=8|p.8 · §4.2.1]]

## 6. 旧总结校正与来源间关系

| 旧笔记问题 | 原文核读后的处理 |
| --- | --- |
| “CoCa 没有引用 ALBEF” | p.3 明确讨论 ALBEF，参考文献 [36] 在 p.15；删除错误判断 |
| “Single(Fusion)-encoder” 混名 | 本文 single-encoder 指视觉分类预训练器，不等于图文 fusion encoder |
| 第 0 位用于对比、后 255 位用于 captioning | 两个任务 pooler 分别输出 1 和 256 tokens；默认为 cascade |
| query “维度”是 1 或 256 | 改为 query 数量；hidden width 另列于 Table 1 |
| 同时计算 ITM 与 LM | 实际 contrastive + captioning，无 ITM 目标 |
| 解耦使两目标保证互不干扰 | 共享计算图仍共同优化；不能保证无梯度冲突 |
| 计算很少所以可从头训练；效果远超所有前作 | 改为增量开销、完整预算及具体协议下结果；不做无条件总成本/领先判断 |
| 目标检测是已展示下游能力 | 本文主要实验未给目标检测结果，不登记为已验证任务 |

与 [[wiki/papers/architecture/pretraining/ALBEF|ALBEF（S011）]]、[[wiki/papers/architecture/pretraining/BLIP|BLIP（S012）]] 比较时，值得保留的是信息可见性与训练接口：ALBEF 用双向文本/融合路径和 MLM；BLIP 为编码和生成保留不同 SA 参数并训练 ITC+ITM+LM；CoCa 的同一因果文本流前后分段，只训练 contrastive+captioning。三者的数据规模、初始化、监督与评测接口差异很大，架构相似性不能代替控制实验。

实际整合的问题是“独立表示与融合表示的统一”“任务 pooler 与信息保留”“共享计算图的增量成本”“zero-shot、冻结特征和微调的证据边界”。仍需新证据的问题包括：相同数据与预算下双目标收益能否保持，pooler 与 decoder 分层选择如何随规模变化，去重与缺失视频对子集结果的影响，以及全局对齐的提升是否伴随更可靠的细粒度事实生成。

## 实际整合关系

支撑因果decoder前后分段、串联pooler与共享计算，区分zero-shot、attentive读出与任务适配。

- [[wiki/architecture/Visibility-and-Connections|可见性、路由与连接：视觉信息在哪里与语言相遇？]]。
- [[wiki/architecture/Generative-Output-Interfaces|生成输出接口：读入图片、输出文字、合成图片分别由谁完成？]]。
- [[wiki/vision/Objectives-and-Transfer|视觉预训练：目标要求保留什么，迁移又读取什么？]]。
- [[wiki/evaluation/Judges-and-Task-Success|裁判与任务成功：答案、解释、生成物和终态怎样分别取证？]]。
- [[wiki/models/Family-Changes|家族变化轴：输入、接口、数据和计算怎样共同演进？]]。
