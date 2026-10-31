---
type: paper
source_id: S011
primary_direction: architecture/pretraining
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/architecture/pretraining/ALBEF.pdf]]"
reading_status: read
ingest_status: complete
related_directions:
  - vision/alignment
---

# ALBEF：先对齐表示，再学习细粒度融合

## 问题与核心认识

ALBEF 要解决两个相连的问题：图像 patch 与文本 token 最初不在可比较的语义空间中，直接交给融合层会增加学习负担；网页配对又不等于唯一、完整、完全正确的图像描述，严格的配对标签会把潜在合理关系当成错误。其回答是用 **Image-Text Contrastive Learning（ITC）约束独立编码的全局表示，用跨注意力融合处理细粒度关系，并用 Momentum Distillation（MoD）软化部分预训练监督**。这里的“先对齐再融合”首先是架构与目标的分工，不是先独立完成对比预训练、再开始融合训练的两个独立阶段。三个预训练任务联合优化。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=1|p.1–4 · §1、§3 / Fig.1]]

最值得保留的认识是：对齐目标可以同时支持高效检索和难负例选择；融合目标学习局部图文关系；动量教师提供的是模型自身历史形成的概率判断，并不是经人工核验的新标签。论文的消融支持这套组合在报告任务中的作用，但不证明教师每次判断正确，也不证明所有下游任务都应采用同样组合。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=4|p.4–5 · §3.2–3.4 / Eqs.5–7]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=7|p.7 · §6.1 / Table 1]]

## 来源、版本与阅读边界

| 项目 | 本次确认 |
| --- | --- |
| 原始标题 | Align before Fuse: Vision and Language Representation Learning with Momentum Distillation |
| 作者 / 机构 | Junnan Li、Ramprasaath R. Selvaraju、Akhilesh D. Gotmare、Shafiq Joty、Caiming Xiong、Steven C.H. Hoi；Salesforce Research |
| 身份 / 版本 | NeurIPS 2021；arXiv:2107.07651v2，首页标注 2021-10-07；[原件 URL](https://arxiv.org/pdf/2107.07651v2) |
| 原件 | [[raw/papers/architecture/pretraining/ALBEF.pdf\|ALBEF.pdf]]，16 页 |
| SHA-256 | 137c937c0834d8aa116bac93cae46cabe86cf7b7645f3b6339639b194273b229 |
| 阅读日期与范围 | 2026-10-31；正文 p.1–10、附录 A–E p.13–16 已读；p.10–12 参考文献仅用于文内定位，未逐篇核查被引来源 |
| 原页视觉核对 | p.1、3–9、13–16；架构、损失、Tables 1–8、Figs.1–12 的图表内容已结合原页检查。其余页使用原 PDF 提取文本 |
| 旧笔记输入 | [[raw/notes/多模态经典/2021-NeurIPS-ALBEF总结.tex\|旧 TeX]]、[[raw/notes/多模态经典/Latex_out/2021-NeurIPS-ALBEF总结.pdf\|旧编译 PDF]]、[[raw/notes/多模态经典/ALBEF动量蒸馏.md\|动量蒸馏讨论]]；均为二手理解，不能替代原论文 |
| 实际验证边界 | 未运行代码、训练或复现实验；未核查整个官方代码仓库；Obsidian 内显示未测 |

## 1. 两种表示各自承担什么

### 1.1 独立编码负责对齐，融合编码负责条件理解

图像编码器是 12 层 ViT-B/16，将图像变为 patch 序列及 [CLS]；文本编码器是 6 层 Transformer，将句子变为 token 序列及 [CLS]；另一个 6 层多模态编码器以文本表示为输入，在每层通过 cross-attention 读取图像表示。文本编码器和多模态编码器分别由 BERT-base 前六层与后六层初始化；图像编码器使用 ImageNet-1k 预训练权重。图像编码器约 85.8M 参数，文本与融合模块合计约 123.7M。这是本文的具体配置，不是“视觉必须比语言大”或“融合越大越好”的结论。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=3|p.3 · §3.1 / Fig.1]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=5|p.5 · §3.5]]

Fig.1 的三条训练路径解释了这种分工：ITC 比较图像与文本各自的全局 [CLS]，无需给每一对候选运行融合层；ITM 用融合后的 [CLS] 判断整对是否匹配；MLM 在图像与上下文条件下恢复被遮蔽的文本 token。一个图像可以为检索预先编码，但某一文本和某一图像之间的细粒度融合表示不能直接作为所有候选通用的独立向量。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=3|p.3–4 · §3.1–3.2 / Fig.1]]

### 1.2 ITC：在候选集合内识别配对关系

图像与文本 [CLS] 分别经过投影，得到归一化的 256 维表示。令 $g_v(v_{\mathrm{cls}})$ 为在线图像表示，$g'_w(w'_{\mathrm{cls}})$ 为动量文本表示，则一个方向的相似度为

$$
s(I,T)=g_v(v_{\mathrm{cls}})^\top g'_w(w'_{\mathrm{cls}}).
$$

对队列中的候选文本 $T_m$，模型预测

$$
p_m^{i2t}(I)=\frac{\exp(s(I,T_m)/\tau)}
{\sum_{n=1}^{M}\exp(s(I,T_n)/\tau)}.
$$

文本到图像方向对称；$\tau$ 是可学习温度。两个方向的交叉熵求平均，构成原始 $\mathcal L_{\mathrm{itc}}$。预训练的配对标签为 one-hot，因此 **ITC 已经明确区分正配对与其他候选**；它与 ITM 的差别不是“有无正负标签”，而是独立表示上的候选相对比较与融合表示上的二分类。动量编码器维护近期表示队列，以扩大候选集合。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=3|p.3 · §3.2 / Eqs.1–2]]

### 1.3 ITM 难负例：按相似度抽样，不是固定选最大值

ITM 将融合 [CLS] 输入二分类头。若只取明显不相关的随机图文，模型可以依赖粗粒度差异完成判断，难以被迫学习关系、属性等细节。本文利用 ITC 的批内相似度分布，为每张图像抽一个负文本、为每段文本抽一个负图像；相似度越大，被抽中的概率越高。**这是按分布随机抽样，不是 argmax。** 原正例和这些负配对共同参与 ITM。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=4|p.4 · §3.2 / Image-Text Matching]]

这一设计把两种目标接在一起：全局相似度帮助找到“粗看合理、细看可能不匹配”的候选，融合层再学习区分它们。相似不等于真的负例，网页描述也可能多义；因此难负例并没有消除数据标签的不确定性。后一点是机制所暴露的限制，不是论文额外验证过的噪声率。

### 1.4 MLM：图像与上下文共同预测被遮蔽词

MLM 遮蔽 15% 文本 token，其中 80% 换成 [MASK]、10% 换成随机 token、10% 保持原词。预测条件包括剩余文本和图像表示，原始目标是被选位置真实词的负对数似然。MLM 让融合表示服务于局部语义恢复，而 ITM 服务于整对匹配。原始联合目标为

$$
\mathcal L=\mathcal L_{\mathrm{itc}}+
\mathcal L_{\mathrm{mlm}}+\mathcal L_{\mathrm{itm}}.
$$

[[raw/papers/architecture/pretraining/ALBEF.pdf#page=4|p.4 · §3.2 / Eqs.3–5、脚注 1]]

## 2. 动量蒸馏怎样处理不唯一的监督

### 2.1 教师从哪里来，软目标在哪些地方使用

教师是在线模型参数的指数移动平均，包括单模态编码器与多模态编码器。用通常的记号展开其更新：

$$
\theta'_t=m\theta'_{t-1}+(1-m)\theta_t.
$$

这条式子是对论文“exponential-moving-average”的教学展开；本文实现设置 $m=0.995$。教师不是另外取得的更大模型，也不是独立人工标注器。它对候选配对给出 $q^{i2t},q^{t2i}$，对 masked token 给出 $q^{\mathrm{msk}}$，用这些分布补充原标签。论文明确修改 ITC 和 MLM；ITM 保留原任务目标，不能由此推论“ITM 原理上不能蒸馏”。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=4|p.4–5 · §3.3–3.4 / Eqs.6–7]]

以 ITC 为例：

$$
\mathcal L_{\mathrm{itc}}^{\mathrm{mod}}
=(1-\alpha)\mathcal L_{\mathrm{itc}}
+\frac{\alpha}{2}\mathbb E\left[
\mathrm{KL}(q^{i2t}\Vert p^{i2t})+
\mathrm{KL}(q^{t2i}\Vert p^{t2i})
\right].
$$

MLM 同样混合原始词标签损失与教师到学生的 KL 项。$\alpha$ 在第一个 epoch 从 0 增至 0.4，队列大小为 65,536。因而准确说法是 **硬标签与软目标混合**，不是把 one-hot 全部替换成教师输出。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=4|p.4–5 · Eqs.6–7、§3.4]]

### 2.2 交叉熵可以接受软目标

这里保留一个对旧笔记很重要的数学澄清。对学生更新时把教师 $q$ 视为固定目标，有

$$
\mathrm{KL}(q\Vert p)
=-\sum_j q_j\log p_j+\sum_j q_j\log q_j
=H(q,p)-H(q).
$$

所以教师到学生 KL 与软目标交叉熵对学生具有相同梯度；交叉熵不只适用于 one-hot。混合损失在忽略与学生无关的常数后，相当于以 $\tilde y=(1-\alpha)y+\alpha q$ 为目标做交叉熵。这是由原文目标直接得到的教学推导，不是本文另外报告的实验。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=4|p.4 · Eq.6]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=6|p.6 · Eq.11]]

原文 §4 在 Eq.11 前一句将 KL 参数写成 $(p,q)$，但 Eq.6 及 Eq.11 展开的 $-\sum q\log p$ 对应 $q\Vert p$；本文按显式损失式解释这一局部记号不一致，不把它静默改成反向 KL。

### 2.3 软目标有何作用，又不能保证什么

Fig.2 中，北极熊描述的被遮蔽位置原标签是 “wild”，教师同时给 “zoo”“pool”“water”等候选一定概率；其它例子说明配对文本也可能只是图像的一种描述。作者用这些例子说明“标注词不一定是唯一语义合理答案”。教师概率可以降低对其它合理候选的绝对排斥，但这些示例并不证明所有高概率词都事实正确。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=4|p.4 · Fig.2]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=15|p.15–16 · Appendix D / Figs.11–12]]

EMA 平滑参数更新，不能保证教师始终更准确，也不能保证噪声监督被纠正到“正确方向”。对某候选给非零软目标，也不意味着该候选概率永远不会降低：更新仍取决于当前预测与混合目标之间的差异。论文的互信息视角把 ITC、MLM 与 MoD 理解为从不同或替代视图学习相关信息；这是目标解释及其界的讨论，不是对教师正确性、全部联合目标或人类式理解的普遍证明。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=5|p.5–6 · §4 / Eqs.8–11]]

## 3. 数据、训练与任务适配决定结果的含义

### 3.1 两种预训练规模

基础配置使用 Conceptual Captions、SBU、COCO、Visual Genome，约 4.0M 独立图像、5.1M 图文对；加入更噪的 CC12M 后约 14.1M 独立图像。“4M/14M”在本文指图像规模，不能直接当作配对数。附录分别列出 COCO 113k 图像/567k 文本、VG 100k 图像/769k 文本等统计。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=5|p.5 · §3.4]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=16|p.16 · Appendix E / Table 8]]

训练 30 epochs、batch size 512、8 张 A100；AdamW 权重衰减 0.02，学习率前 1,000 步升至 $10^{-4}$，之后余弦降至 $10^{-5}$。预训练分辨率 $256\times256$，下游微调提高至 $384\times384$ 并插值位置编码；RandAugment 排除会改颜色的增强，以免破坏颜色词语义。论文未在这些设置旁报告可直接复用的完整总训练时长/能耗，不能仅凭 GPU 数推算成本。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=5|p.5 · §3.4–3.5]]

### 3.2 相同骨干不等于相同评测接口

| 下游任务 | 实际接口与边界 |
| --- | --- |
| 图文检索 | ITC 先从全库筛 top-$k$，ITM 对候选重排；微调时同图多描述使用多正例目标。COCO 使用 Karpathy 划分，Flickr30k 使用 29k/1k/1k 图像划分。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=6\|p.6 · §5]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=13\|p.13 · Appendix A]] |
| “零样本” Flickr30k 检索 | 此处模型先在 COCO 检索上微调，再直接用于 Flickr30k；零样本指没有 Flickr30k 微调，不能写成完全没有检索任务监督。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=6\|p.6 · §5]] |
| VQA | 6 层答案 decoder 根据图像—问题表示自回归生成；为公平比较，报告评测时将候选答案限制为 3,192 个。训练接口是生成式，报告分数不是无限制开放答案评测。使用 VQA train+val 与 VG QA。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=7\|p.7 · §5 / Fig.3]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=13\|p.13 · Appendix A]] |
| NLVR2 | 一个文本对应两张图像；融合层适配为顺序读取两图，并共享部分 cross-attention 投影。微调前额外做 1 epoch 文本分配预训练，判断文本属于第一图、第二图或都不属于。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=6\|p.6–7 · §5]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=13\|p.13 · Appendix A / Fig.5]] |
| 视觉蕴含 | SNLI-VE 三分类：entailment、neutral、contradiction。原文另提醒测试标签噪声问题；不能把少量分差直接归因于推理能力。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=6\|p.6 · §5、脚注 4]] |
| 弱监督 grounding | 用 Grad-CAM 将 ITC/ITM 对文本相关区域的响应转为定位依据，没有用 RefCOCO+ 框标签微调；评测仍使用外部 detector 的 region proposals 选框。预训练表示不依赖 detector，不代表这个定位评测完全不使用 detector。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=9\|p.9 · §6.3 / Table 5]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=13\|p.13 · Appendix A / Grounding]] |

## 4. 证据支持到哪一步

### 4.1 消融支持目标组合，但不是每项对每个任务都严格增加

Table 1 在 4M 图像设置中逐项加入目标与组件。下面保留有解释力的代表指标；检索的 TR/IR 是 **R@1、R@5、R@10 的均值**，不是单独 R@1。

| 配置 | Flickr30k TR / IR 均值 | NLVR2 test-P | VQA test-dev |
| --- | --- | --- | --- |
| MLM + ITM | 93.96 / 88.55 | 77.51 | 71.40 |
| + ITC | 96.55 / 91.69 | 79.88 | 73.29 |
| + ITM hard negatives | 97.01 / 92.16 | 80.35 | 73.81 |
| + ITC MoD | 97.33 / 92.43 | 80.34 | 74.06 |
| + MLM MoD（完整预训练） | 97.47 / 92.58 | 80.44 | 74.42 |

这些是论文报告的逐步消融；例如加入 ITC MoD 后 NLVR2 80.35→80.34，并非每列单调上升。它支持“联合系统在这些任务和配置下总体有效”，但不是完整因子实验，未分离所有组件交互，也没有给这些微小差异配置信区间。作者另报告下游 MoD 及扩大到 14M 的配置，不宜把数据量与蒸馏贡献混在一起。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=7|p.7 · §6.1 / Table 1]]

### 4.2 检索的准确率与计算接口要一起看

14M 预训练配置在 COCO 5k 测试集上报告文本检索 R@1=77.6、图像检索 R@1=60.7；Flickr30k 微调后对应 95.9、85.6。它们来自不同数据集，不能混为同一评测。Table 6 的 Flickr30k 消融则显示，纯 ITC 的 TR/IR 均值 97.30/90.95，增加 top-16 重排为 98.60/93.64，top-128 为 98.57/93.99；更多候选不是每个方向都持续提高。该结果支持有限候选的融合重排价值，不支持“融合检索必须对全库逐对计算”。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=8|p.8 · Table 2]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=9|p.9 · §6.4 / Table 6]]

Table 4 中 14M 配置 VQA test-std=76.04、NLVR2 test-P=83.14、SNLI-VE test=80.91。论文以这些任务分数和当时方法比较；所列预训练数据、目标与下游适配并不全相同，不能把表中相对结果当作纯架构的因果排名。NLVR2 自身还受额外文本分配预训练与参数共享方式影响，Table 7 的最佳组合为 83.14；没有该额外预训练时，不同共享方案的关系也会变化。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=8|p.8 · §6.2 / Table 4]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=9|p.9 · Table 7]]

### 4.3 Grounding 与注意力可视化的额外限制

RefCOCO+ 上 ITM Grad-CAM 的 val/testA/testB 为 58.46/65.89/46.25，高于 ITC 的 51.58/60.09/40.19；论文据此分析融合表示更适合条件定位。**附录明确承认这些验证、测试图像曾在预训练中出现。** 作者认为相关样本占比较小，影响可能有限，但本次材料没有提供移除重叠后的重新训练对照；因此不能把该表称为严格未见图像的泛化证据。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=9|p.9 · Table 5]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=13|p.13 · Appendix A / Grounding]]

可视化也依赖层和头的选择：Appendix B 比较不同 cross-attention 层，并以第三层产生 ITM Grad-CAM。Appendix C 在 1,374 个验证图像—问题对上，用真实答案生成 Grad-CAM，与人类注意力比较报告秩相关 0.205。热图与该相关值能帮助理解模型关注区域，不等同于证明模型按人类因果推理过程作答。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=14|p.14 · Appendix B / Fig.8]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=15|p.15 · Appendix C / Fig.10]]

## 5. 与旧笔记的校正关系

| 旧理解或措辞 | 原文核读后的处理 |
| --- | --- |
| 难负例取相似度最高项；同页又说按概率抽样 | 统一为批内按相似度分布抽样；不保留 argmax 说法。原文 p.4 |
| ITC 没有显式区分正负样本 | Eq.2 已使用配对标签；区别在独立表示对比与融合二分类。原文 p.3–4 |
| 交叉熵用于 one-hot，软分布必须用 KL | 软目标交叉熵合法；固定教师时 KL 与软交叉熵对学生梯度相同。原文 Eqs.6、11 加本页推导 |
| 教师伪目标替代原标签 | 实际按 $\alpha$ 混合；动量蒸馏旧 Markdown 已讨论这一点，本页统一以原文目标为准。原文 p.4–5 |
| 教师保证不偏离正确方向 | 删除保证；EMA 稳定性不等于伪标签真实性 |
| NLVR 判断文本是否描述“一张图片” | 本文 NLVR2 输入是一对图像，且有专门适配与额外训练。原文 p.6–7、13 |
| ALBEF 不能充分使用高质量数据、检索一定很慢 | 论文未证明这种普遍限制；其数据包含 COCO/VG，并有 ITC 筛选—ITM 重排。它没有 CapFilt 式数据重写流程，与“不能用高质量图文”是不同判断 |

旧 TeX 与其编译 PDF 中的这些解释不作为独立学术证据；动量蒸馏 Markdown 中的代码片段也没有在本次与官方实现逐行比对，因此不据此登记代码已审计。

## 6. 可持续追问与整合落点

本来源可支持“全局对齐与局部融合的互补”“自生成软监督”“检索两阶段计算”“监督噪声与伪目标不确定性”等主题。这些关系已由页末实际主题承接；跨来源综合保留各自证据身份。

仍未解决的问题是：教师什么时候会强化错误配对；不同噪声类型、数据质量和规模下，硬标签/软目标的最合适混合比例是否改变；没有预训练图像重叠时 grounding 增益还剩多少；当后续模型同时学习 captioning 或直接改写数据时，改进究竟来自目标、数据还是模型预算。本文没有提供覆盖这些问题的完整控制实验。

## 实际整合关系

支撑对齐/融合分工、相似度难负例与EMA软目标，说明检索重排及KL/软交叉熵关系。

- [[wiki/architecture/Visibility-and-Connections|可见性、路由与连接：视觉信息在哪里与语言相遇？]]。
- [[wiki/training/Supervision-and-Stages|监督与阶段：数据、目标、开放参数和预算如何一起改变？]]。
- [[wiki/evaluation/Judges-and-Task-Success|裁判与任务成功：答案、解释、生成物和终态怎样分别取证？]]。
- [[wiki/models/Family-Changes|家族变化轴：输入、接口、数据和计算怎样共同演进？]]。
