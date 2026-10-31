---
type: paper
source_id: S012
primary_direction: architecture/pretraining
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/architecture/pretraining/BLIP.pdf]]"
reading_status: read
ingest_status: integrating
---

# BLIP：将理解、生成和训练数据改进接成一个流程

## 问题与核心认识

BLIP 同时处理模型接口与数据质量两个问题。模型方面，希望同一套预训练表示支持独立图文检索、图文联合理解和图像条件文本生成；数据方面，网页 alt-text 常常只是页面上下文，未必准确描述图片。其贡献分别是 **Multimodal Mixture of Encoder-Decoder（MED）** 与 **Captioning and Filtering（CapFilt）**：前者在共享参数的同时保留编码和生成的不同注意力约束，后者通过生成与筛选实际重构训练语料。生成任务是论文明确的研究目标之一，不能解释成“只是为了清洗数据不得已加入”。[[raw/papers/architecture/pretraining/BLIP.pdf#page=1|p.1–4 · §1、§3 / Figs.1–3]]

与 [[wiki/papers/architecture/pretraining/ALBEF|ALBEF（S011）]] 的关键联系是：BLIP 沿用 ITC 的动量软目标与 ITM 的难负例策略，但用自回归 LM 支持 captioning；CapFilt 又把模型判断变成新的文本样本和样本保留决策。软化一个已有配对的训练目标，与改变后续训练集包含哪些配对，是两个不同层面的操作。[[raw/papers/architecture/pretraining/BLIP.pdf#page=3|p.3–4 · §3.2–3.3]]

## 来源与实际阅读

| 项目 | 本次确认 |
| --- | --- |
| 标题 | BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation |
| 作者 / 机构 | Junnan Li、Dongxu Li、Caiming Xiong、Steven Hoi；Salesforce Research |
| 版本 | arXiv:2201.12086v2，首页日期 2022-02-15；[原件 URL](https://arxiv.org/pdf/2201.12086v2) |
| 原件 / 页数 | [[raw/papers/architecture/pretraining/BLIP.pdf\|BLIP.pdf]]；12 页 |
| SHA-256 | 63e0335cdd57c3d92b907b89c93d10befdd29b8aeed108091bbde90c121ed97a |
| 阅读日期与范围 | 2026-10-31；正文 p.1–9、Appendix A–C p.12 已读；p.9–11 参考文献仅定位，未独立核读被引论文 |
| 原页视觉核对 | p.2、4–9、12，覆盖 MED 架构、CapFilt 数据流、参数共享、全部结果/消融表与附录样例 |
| 旧笔记输入 | [[raw/notes/多模态经典/2022-ICML-BLIP总结.tex\|旧 TeX]]、[[raw/notes/多模态经典/Latex_out/2022-ICML-BLIP总结.pdf\|旧编译 PDF]]；二手解释，已对照机制段及编译 PDF p.1、4–5 |
| 未做事项 | 未运行代码或复现实验；旧笔记代码未与官方仓库逐行核验；Obsidian 内显示未测 |

## 1. MED：共享哪些参数，改变哪些可见关系

### 1.1 三种运行方式不是三个完全独立模型

图像始终先通过 ViT，产生 patch 与 [CLS] 表示。文本侧根据任务切换三种功能，Fig.2 中相同颜色表示共享参数：

| 功能 | 文本的可见信息 | 输出与任务 |
| --- | --- | --- |
| Unimodal encoder | 文本双向 self-attention；不读取图像 token | 文本 [CLS] 与图像 [CLS] 对比，支持 ITC |
| Image-grounded text encoder | 双向 self-attention 后，以 cross-attention 读取图像 | [Encode] 输出为整对图文的联合表示，线性 ITM head 判断匹配 |
| Image-grounded text decoder | causal self-attention 只允许当前及历史文本；cross-attention 可读取图像 | 从 [Decode] 开始，直到结束符，自回归生成 caption，支持 LM |

[[raw/papers/architecture/pretraining/BLIP.pdf#page=2|p.2–3 · Fig.2 / §3.1–3.2]]

编码器与解码器共享 embedding、cross-attention 与 FFN，**self-attention 参数分开**，因为双向理解与因果生成的表示需求不同。这里既改变 mask，也保留不同 self-attention 参数；不能说两者只是同一 attention 权重换一张 mask。单模态文本编码与图像条件编码则共享相应文本模块，条件编码额外启用 cross-attention。[[raw/papers/architecture/pretraining/BLIP.pdf#page=3|p.3 · §3.2 / Parameter sharing]]

一次图文对的三个目标共用一次图像前向，文本侧运行三条相应路径。参数共享减小模型参数存储并促进多任务学习，不等于三次文本计算消失；实际 FLOPs、吞吐和端到端成本不能只由参数量推断。[[raw/papers/architecture/pretraining/BLIP.pdf#page=3|p.3 · §3.2]]

### 1.2 三个目标各自约束什么

- **ITC**：独立图像/文本表示的对比对齐；沿用 ALBEF 的动量编码器与软目标，考虑名义负例中潜在合理配对。它没有执行 CapFilt 那样的文本删除。
- **ITM**：融合 [Encode] 表示上的匹配二分类；批内对比相似度越高，负例被选中的概率越高。不是每次固定选择最难的那一个。
- **LM**：给定图像，自回归预测 caption，使用交叉熵与 0.1 label smoothing。训练时的目标来自当前训练语料；不能把每一次 LM 前向等同于已经生成并筛选了新的训练数据。

以上目标共同预训练 MED。[[raw/papers/architecture/pretraining/BLIP.pdf#page=3|p.3 · §3.2]]

为解释 causal mask 与生成目标的关系，可将原文 LM 描述写成

$$
\mathcal L_{\mathrm{LM}}=-\sum_{t=1}^{|T|}
\log p_\theta(T_t\mid T_{<t},I).
$$

这是原文文字目标的教学展开，省略其 label smoothing 的显式分布写法。$T_{<t}$ 说明预测不能读取未来目标词；图像则是整个生成过程共享的条件。它与恢复少数被遮蔽位置的 MLM 在训练信息可见性和输出接口上不同，本文没有证明“LM 在所有条件下都比 MLM 更难或更好”。

### 1.3 参数共享消融支持的是具体折中

在 14M 图像、原始 web text 的配置中，Table 3 比较：全部共享 224M 参数；除 CA 外共享 252M；除 SA 外共享 252M；完全不共享 361M。除 SA 外共享的 COCO 检索 TR/IR R@1=78.4/60.7、caption CIDEr=127.8，全部共享为 77.3/59.5、125.9，完全不共享为 78.3/60.5、127.4。它支持本文分离 SA 的设计，但这些小差异没有置信区间，不能推成所有编码—解码系统的普遍最优共享方案。[[raw/papers/architecture/pretraining/BLIP.pdf#page=5|p.5–6 · §4.4 / Table 3]]

## 2. CapFilt：一个先生成、再筛选、再训练的语料流程

### 2.1 从初始 MED 到新训练集

Fig.3 需要按模型流和数据流分别读：

1. 先用网页图文对与人工标注图文对预训练初始 MED。
2. 从同一个预训练模型初始化两个副本，在 COCO 上**分别微调**：captioner 用 LM，filter 用 ITC+ITM。
3. Captioner 对每张 web image 生成一条合成文本。
4. Filter 同时评估原始 web text 和合成 text，ITM head 判为 unmatched 的配对被删除。
5. 将保留的网页配对、保留的合成配对与人工标注配对合并，用来预训练一个新模型。

[[raw/papers/architecture/pretraining/BLIP.pdf#page=4|p.4 · §3.3 / Fig.3]]

以 $\mathcal F$ 表示 filter 的保留操作，流程可教学性地记作

$$
D_{\mathrm{new}}=
\mathcal F\{(I_w,T_w)\}
\cup\mathcal F\{(I_w,T_s)\}
\cup\{(I_h,T_h)\}.
$$

这不是把原网页描述无条件替换成合成描述：同一图像可以保留原文本、合成文本或两者。Fig.4 的城堡例子甚至保留原网页历史描述而拒绝泛泛的合成描述，说明“生成的一定更准确”不是该机制的前提。模型接受某文本也不等于人工确认其全部事实为真；这里的“noise”首先是 filter 的判定。[[raw/papers/architecture/pretraining/BLIP.pdf#page=5|p.5 · Fig.4]] [[raw/papers/architecture/pretraining/BLIP.pdf#page=12|p.12 · Appendix B / Fig.6]]

论文只报告这里的一轮数据 bootstrap。多轮、每图多条合成文本以及多个 captioner/filter 集成，放在结论的未来方向中，不能登记为已完成实验。[[raw/papers/architecture/pretraining/BLIP.pdf#page=9|p.9 · §7]]

### 2.2 为什么生成多样性与过滤要一起讨论

合成文本采用 nucleus sampling，累计概率阈值 $p=0.9$。Table 2 将其与 beam search 比较：filter 判定的 noise ratio 为 25% 对 19%，但 nucleus 的 COCO TR/IR R@1=80.6/63.1，优于 beam 的 79.6/61.9；COCO CIDEr 为 129.7 对 128.9。作者解释为随机采样带来更丰富、新颖的信息。这是与结果一致的假说，表中并未独立控制所有“多样性”变量；25% 也不是经人工标注得到的真实错误率。[[raw/papers/architecture/pretraining/BLIP.pdf#page=5|p.5 · §4.3 / Table 2]]

预训练阶段共享 MED 参数，与 CapFilt 阶段分离两个微调模型并不矛盾。Table 4 中，captioner/filter 继续共享参数时仅拒绝 8%，独立微调时拒绝 25%，后者下游更好。作者将其解释为共享导致 confirmation bias：生成器产生的错误不易被同源判别器拒绝。表支持这一设置的收益，但没有证明独立微调后完全不存在相关偏差。[[raw/papers/architecture/pretraining/BLIP.pdf#page=6|p.6 · §4.4 / Table 4]]

### 2.3 数据收益不只是多训练了几步

14M 图像、ViT-B/16 下的组件消融如下：

| 训练语料处理 | COCO 检索 TR/IR R@1 | COCO caption CIDEr | NoCaps CIDEr |
| --- | --- | --- | --- |
| 原始语料 | 78.4 / 60.7 | 127.8 | 102.2 |
| 只 filter | 79.1 / 61.5 | 128.2 | 102.7 |
| 只 captioner | 79.7 / 62.0 | 128.9 | 103.4 |
| captioner + filter | 80.6 / 63.1 | 129.7 | 105.1 |

[[raw/papers/architecture/pretraining/BLIP.pdf#page=5|p.5 · Table 1]]

生成新文本使每 epoch 样本增多。为检查“其实只是训练更久”，Table 12 将原始文本重复到相同 24.7M 样本量，与原始 15.3M 及 CapFilt 24.7M 比较。仅重复原文没有得到同类增益，支持语料内容/选择确实重要；这项控制匹配了每 epoch 样本数，却不是把初始模型训练、captioner/filter 微调和数据生成的全部成本都算成相同预算。[[raw/papers/architecture/pretraining/BLIP.pdf#page=8|p.8–9 · §6 / Table 12]]

Table 13 比较在新语料上继续训练旧模型或预训练新模型。作者选择后者；不过表中不是每个指标都严格更好，例如继续训练的 COCO CIDEr 为 129.9，新模型为 129.7。因此“新模型总体更合适”应限制在报告对照中，不能从作者的强措辞推成“学生绝对不能从教师权重初始化”。[[raw/papers/architecture/pretraining/BLIP.pdf#page=9|p.9 · Table 13]]

## 3. 训练规模、下游接口与结果条件

### 3.1 预训练的 14M 与 129M

基础语料约 14M 图像，包括 COCO、VG、CC3M、CC12M、SBU；扩大配置增加 115M LAION 图像，形成约 129M。这里 LAION 是从 LAION400M 中取得的子集，短边大于 256 像素，且每 epoch 只用其五分之一，不能写成每轮遍历全部 129M 图像。图像数与文本数也不同，Appendix C 分别登记。[[raw/papers/architecture/pretraining/BLIP.pdf#page=4|p.4 · §4.1、脚注 1]] [[raw/papers/architecture/pretraining/BLIP.pdf#page=12|p.12 · Table 15]]

图像侧尝试 ViT-B/16 与 ViT-L/16，初始化自 ImageNet 预训练权重；文本侧初始化 BERT-base。默认 BLIP 是 ViT-B。预训练 20 epochs，在两个各 16 GPU 的节点运行，batch 为 B 版本 2,880、L 版本 2,400，AdamW weight decay=0.05；预训练随机裁剪 $224^2$。下游一般使用 $384^2$，**VQA 例外为 $480^2$**。本文没有报告这里所有环节可对照的总 GPU 时长，因此不能把更少图像直接换算成更低总计算成本。[[raw/papers/architecture/pretraining/BLIP.pdf#page=4|p.4 · §4.1]] [[raw/papers/architecture/pretraining/BLIP.pdf#page=12|p.12 · Appendix A / Table 14]]

BLIPCapFilt-L 表示用 ViT-L captioner/filter 构造语料，再训练 ViT-B 模型；BLIPViT-L 才是最终模型的视觉骨干也为 ViT-L。比较时不能把二者混为同一个“大模型”条件。[[raw/papers/architecture/pretraining/BLIP.pdf#page=6|p.6 · Table 5 注释]]

### 3.2 检索、captioning 与 VQA

检索微调用 ITC+ITM，先以独立表示筛候选，再融合重排；COCO 的 $k=256$，Flickr30k 的 $k=128$。14M BLIP 在 COCO 5k test 的 TR/IR R@1=80.6/63.1，对照表中 ALBEF 为 77.6/60.7。平均增益 2.7 个百分点对应这些任务条件，不是一般视觉理解能力提高 2.7%。Flickr30k “zero-shot”是从 **COCO 检索微调模型**直接转移，并非从无下游监督模型直接测量。[[raw/papers/architecture/pretraining/BLIP.pdf#page=6|p.6 · §5.1 / Tables 5–6]]

Captioning 在 COCO Karpathy train 上以 LM 微调，再测 COCO Karpathy test 和 NoCaps validation；提示前缀为 “a picture of”，推理 beam size=3、最大生成长度=20。14M 配置 COCO CIDEr=129.7、NoCaps overall CIDEr=105.1。不同方法可能使用额外 detector 标注、不同分辨率、骨干与数据量；论文表中的比较不能分离这些因素。[[raw/papers/architecture/pretraining/BLIP.pdf#page=6|p.6–7 · §5.2 / Table 7]] [[raw/papers/architecture/pretraining/BLIP.pdf#page=12|p.12 · Appendix A]]

VQA 将图像—问题先编码，再由 answer decoder 用 LM 学习答案；训练使用 VQA2 train+val 及 VG 数据。虽然 §5.3 强调接口支持 open-ended VQA，附录实际评测描述是 **用 decoder 排序 3,128 个候选答案**。这里保留本版本原文数字；ALBEF 原文的数字是 3,192，未核代码前不擅自统一或宣称哪一个是排版错误。14M BLIP 的 VQA test-std=77.62，属于该候选与分辨率设置下的结果。[[raw/papers/architecture/pretraining/BLIP.pdf#page=7|p.7 · §5.3 / Fig.5(a)、Table 8]] [[raw/papers/architecture/pretraining/BLIP.pdf#page=12|p.12 · Appendix A / VQA]]

### 3.3 多图、对话与视频的能力边界

NLVR2 输入两张图像：每层设置两条 cross-attention，输出先合并再送入 FFN；早期层采用平均，后期层用拼接加线性投影。原文层边界措辞为 “first 6 layers” 与 “layer 6–12”，此处不把重叠编号自行解释成已核代码事实。它没有 ALBEF 的额外文本分配预训练；14M 的 test-P=82.30，129M 为 83.08，扩大语料也不是所有指标稳定增长。作者将较小收益猜测为域差异，不是已隔离验证的原因。[[raw/papers/architecture/pretraining/BLIP.pdf#page=7|p.7–8 · §5.4 / Fig.5(b)、Table 8]]

VisDial 使用候选答案排序的判别设置，条件包括图像、caption、问题与对话历史；ITM 训练候选真假，报告 VisDial v1.0 validation 的排序指标。不能凭“visual dialog”名称把它当作任意自由对话测试。[[raw/papers/architecture/pretraining/BLIP.pdf#page=8|p.8 · §5.5 / Table 9]]

视频迁移把 COCO 检索或 VQA 微调模型直接用于目标视频数据，不在目标视频任务上训练。检索均匀采 8 帧，QA 采 16 帧，再拼接帧特征；原文明确说此方法忽略时间信息。MSRVTT 1k test 检索 R@1=43.3，MSRVTT-QA/MSVD-QA top-1=19.2/35.2。它说明静态视觉—语言表示在这些数据上的迁移价值，不能证明学到了时间顺序、运动因果或长期视频推理。[[raw/papers/architecture/pretraining/BLIP.pdf#page=8|p.8 · §5.6 / Tables 10–11]]

## 4. 旧理解修订与后续问题

| 旧笔记表述 | 本页处理 |
| --- | --- |
| BLIP 是吸收 VLMo 思想的 ALBEF | 原论文未提供这条因果归属证据；保留机制比较的可能性，不登记为作者确认的继承关系 |
| Encoder-decoder 不能用于检索，因为不能提取图像特征 | 改为当时方法在不同任务上的接口/效果取舍；不是架构上不可能 |
| 为处理数据“不得已”加入生成 | 原文明确把理解与生成统一列为模型目标 |
| ITM 用融合输出再与图像 embedding 匹配 | 实际对融合 [Encode] 表示用线性头分类，不是重新做两向量相似度 |
| 每次取最难负例；动量 encoder 做数据级清理 | 分布抽样与软监督，不等于 argmax，也不等于删除训练样本 |
| COCO 微调后 filter 判断必然精准、数据已经干净 | 改为模型判定的保留/拒绝；保留错误、偏差与域差异可能性 |
| ALBEF 等均爬取 4 亿图像 | ALBEF 本文设置为 4M/14M；BLIP 本文为 14M/129M，不能把其它模型的数据规模转移过来 |

已核读材料支持的综合问题是：共享表示与任务专用注意力如何折中；优化软监督与直接改造语料各自解决什么噪声；合成多样性怎样在 filter 偏差下保留。尚待验证的是过滤决策相对人工事实判断的误差、多轮 bootstrap 是否积累同源错误、完整训练—生成成本，以及候选式 VQA 和忽略时间的视频结果能多大程度迁移到更开放任务。后续主题整合应围绕这些条件展开，不只按多任务分数排序。
