---
type: paper
source_id: S010
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/vision/alignment/SigLIP2.pdf]]"
primary_direction: vision/alignment
reading_status: read
ingest_status: integrating
---

# SigLIP 2：全局对齐之外，怎样学习可定位的视觉特征？

> [!abstract] 核心理解
> SigLIP 2 是视觉/文本编码器家族及组合训练配方：保留逐对 sigmoid 图文对齐，加入理解区域的解码器任务，再在固定分辨率主配方的最后20%训练中加入视觉自蒸馏和 masked prediction。它希望同时改善全局语义、区域定位和 dense features。**训练时增加的解码器不是发布的聊天模型；NaFlex、小模型蒸馏和标准固定分辨率模型也不是完全相同的训练分支。**[[raw/papers/vision/alignment/SigLIP2.pdf#page=2|pp.2–5 Fig.1、§2]]

## 来源身份与实际阅读

- **论文**：Michael Tschannen、Alexey Gritsenko、Xiao Wang、Muhammad Ferjad Naeem、Ibrahim Alabdulmohsin 等，*SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features*。本地固定 arXiv:2502.14786 **v1，2025-02-20**，20页；题名/作者/版本日期已对照首页。页码均为PDF页码，与印刷页一致。
- **原件**：[[raw/papers/vision/alignment/SigLIP2.pdf]]；[arXiv v1](https://arxiv.org/pdf/2502.14786v1)；SHA-256：b840240c075aad94d46f739712c594cb6848d0bf0e5b516da5d8da7586ad6bb9，本次重算一致。
- **2026-10-31 阅读范围**：正文 pp.1–12，附录 pp.17–20。实际视觉核查 pp.2、3、4、5、7、9、11、17、18、20：训练架构、权重和schedule、分类/检索、NaFlex、dense probing、定位、VLM与公平性表。参考文献未逐条核读，也未追读 LocCa/SILC/TIPS/ACID/NaViT 的原论文；下述关于这些技术只确认本报告如何采用。
- **旧笔记输入**：[[raw/notes/视觉编码器/SigLIP2总结.tex]]、[[raw/notes/视觉编码器/Latex_out/SigLIP2总结.pdf]]；本次读取TeX机制与实验解释，旧编译PDF不另计来源。未复现、未审计代码；Obsidian 内显示未测。当前 integrating，待主题整合与独立审核。

## 为什么全局相似度还不够？

[[wiki/papers/vision/alignment/CLIP|CLIP]] 与 [[wiki/papers/vision/alignment/SigLIP|SigLIP]] 的对齐以整图/整段文本表示为核心。**本库解释**：把整张图“认作包含什么”与保留“哪个patch对应哪个对象、边界或位置”是不同约束，前者高分不能自动证明后者。SigLIP 2 明确以定位、分割、深度等下游任务检验未池化视觉特征，并让训练监督触达这些特征。[[raw/papers/vision/alignment/SigLIP2.pdf#page=1|pp.1–3 引言、§2.2–2.3]]、[[raw/papers/vision/alignment/SigLIP2.pdf#page=9|p.9 §3.3–3.4]]

固定分辨率版本仍采用标准ViT、可学习位置编码和MAP attention pooling；图像/文本塔通常同规模，g视觉塔搭配So400m文本塔。文本长度64，用256k词表的多语言Gemma tokenizer，先转小写。发布尺度为B（86M）、L（303M）、So400m（400M）、g（1B），这里是视觉塔尺度，不能当作双塔加辅助解码器的全部训练参数。[[raw/papers/vision/alignment/SigLIP2.pdf#page=1|p.1 模型家族]]、[[raw/papers/vision/alignment/SigLIP2.pdf#page=2|pp.2–3 §2.1]]

## 三种监督怎样到达同一个视觉编码器？

### 1. Sigmoid：保留全局图文匹配

与 SigLIP 一样，batch内所有图文组合构成逐对二分类，原始配对为正，其他配对当作负。这里的变化主要不在新发明一个匹配损失，而在把其他监督组合到该编码器。基础 sigmoid 公式、归一化及负例假设见 [[wiki/papers/vision/alignment/SigLIP|SigLIP]]；本报告说使用原实现，未重新给出独立损失推导。[[raw/papers/vision/alignment/SigLIP2.pdf#page=3|p.3 §2.2]]

### 2. LocCa式解码器：既说整图，也把语言和区域互相对应

辅助Transformer decoder用cross-attention读取 **MAP池化之前的视觉patch序列**。它的形状随文本编码器，但层数减半，并增加cross-attention。每个例子训练三个目标、对应三次decoder forward：

- **captioning**：图像→整图描述。
- **automatic referring expression prediction**：给区域描述，预测对应bbox坐标。
- **grounded captioning**：给bbox坐标，预测该区域的描述。

区域—文本对为自动标注：从alt-text提取n-gram后用开放词汇检测，也使用固定对象类别。不能把自动区域注释当成人工精标。Captioning以50%概率采用parallel prediction，即从mask tokens并行预测且不用causal attention mask；**此处50%是captioning训练方式的抽样概率**。decoder仅用于表征学习，不在模型发布中。[[raw/papers/vision/alignment/SigLIP2.pdf#page=3|p.3 §2.2]]

### 3. 自蒸馏与masked prediction：补局部对应约束

**Local-to-global consistency**：学生视觉编码器看8个局部增强视图，教师看1个全局视图，在独立MLP head产生的高维空间做表示匹配。教师参数是学生参数的EMA；Fig.1标出teacher侧stop-gradient。教师提供的是模型自身逐步形成的目标，不是新增人工标签。[[raw/papers/vision/alignment/SigLIP2.pdf#page=2|p.2 Fig.1]]、[[raw/papers/vision/alignment/SigLIP2.pdf#page=3|pp.3–4 §2.3]]

**Masked prediction**：学生与教师看同一个全局视图，学生的50%嵌入patch被替换为mask token，学生在被mask的位置预测教师的patch特征。匹配损失形式同前项，但从图像级表示改到patch级；这不是像素重建，也不是每个patch直接匹配一个文本词。**这里50%是patch遮挡比例**，与captioning的50%概率不是同一个量。原报告把具体损失/温度等实现细节交由引用工作，本轮不冒充已读这些原论文。[[raw/papers/vision/alignment/SigLIP2.pdf#page=4|p.4 §2.3]]

Sigmoid和LocCa在原始图像上计算；新增视觉目标使用额外增强视图。作者这样安排是为了避免额外增强破坏图文语义对齐，属于训练设计依据，不是已证明对所有增强成立的定律。[[raw/papers/vision/alignment/SigLIP2.pdf#page=4|p.4 §2.3]]

## 图中的20%究竟是什么？

> [!important] 训练时段、loss权重、数据比例是三个量
> 原文Fig.1 caption明确写自蒸馏和masked prediction在 **最后20%训练** 中启用；§2.3说在80%完成时加入。20%不是loss系数，不是每批取20%图片，也不是EMA更新率。Sigmoid/LocCa旁的100%对应主训练全程；不应把示意图标签替代下面的真实系数。[[raw/papers/vision/alignment/SigLIP2.pdf#page=2|p.2 Fig.1及caption]]、[[raw/papers/vision/alignment/SigLIP2.pdf#page=4|p.4 §2.3]]

依据正文，可将**固定分辨率主训练**整理为以下组合式（本库按文字重写，非原文编号公式）：

$$
\mathcal L(s)=\mathcal L_{\rm sigmoid}+\mathcal L_{\rm LocCa}
+\mathbf1[s\ge0.8]\,c_M
\left(\mathcal L_{\rm local/global}+0.25\mathcal L_{\rm masked}\right).
$$

$s$ 表示主训练进度；sigmoid与LocCa等权；局部/全局一致性和masked项的内部权重是1与0.25。模型尺度系数 $c_M$ 分别为 B：0.25、L：0.5、So400m：1.0、g：0.5。80%节点以学生初始化教师，新增heads、mask token和相应优化器参数随机初始化。该公式不套用到NaFlex分支或额外小模型蒸馏阶段。[[raw/papers/vision/alignment/SigLIP2.pdf#page=3|p.3 §2.2]]、[[raw/papers/vision/alignment/SigLIP2.pdf#page=4|p.4 §2.3]]

主配方数据源WebLI报告包含100亿图像、120亿alt-text、109语言；训练混合按90%英语网页来源、10%非英语网页来源组成，并施加去偏过滤。主训练40B **累计样本次数**、batch32k，Adam、学习率$10^{-3}$、解耦weight decay $10^{-4}$、clip norm1，cosine schedule与20k warmup steps；不是每个模型都只有40B总预算，因为分支还会追加训练。初始分辨率256、patch16，得到256视觉tokens。[[raw/papers/vision/alignment/SigLIP2.pdf#page=3|p.3 §2.1–2.2]]

## 标准分辨率、NaFlex、小模型蒸馏如何分支？

| 分支 | 起点与训练变化 | 读结果时必须保留的条件 |
| --- | --- | --- |
| 固定分辨率适配 | 从95%进度checkpoint恢复，resize位置编码，必要时patch16→14使用PI-resize，再在目标尺寸继续所有loss | 每个目标尺寸为单独checkpoint；不是全部训完后统一附加一个无weight-decay微调。[[raw/papers/vision/alignment/SigLIP2.pdf#page=4\|§2.4.1]] |
| **NaFlex** | 从§2.2基础训练的90%checkpoint切到近原比例resize；每batch随机预定义sequence length；最后10%的schedule拉长3.75倍；最长长度batch减半、步数加倍 | **不使用§2.3自蒸馏与masked prediction**；额外时长不同，不能把比较结果纯归因于aspect ratio。[[raw/papers/vision/alignment/SigLIP2.pdf#page=4\|pp.4–5 §2.4.2]] |
| B/16、B/32固定模型的数据筛选蒸馏 | 再训练4B样本，只用sigmoid；学习率$10^{-5}$，无weight decay。teacher和learner共同给样本learnability打分、从super-batch筛32k | B/16用0.5 filtering ratio、64k super-batch；B/32采用0.75 ratio。是通过选数据的隐式蒸馏，不是这里增加了显式teacher-logit KL loss。[[raw/papers/vision/alignment/SigLIP2.pdf#page=6\|p.6 §2.5]] |

蒸馏teacher先取SigLIP 2 So400m，再在高质量curated数据上微调1B examples；teacher训练与筛选开销也是资源条件。其完整ACID算法的细节本轮只依本文简述，不宣称已核查引用工作。[[raw/papers/vision/alignment/SigLIP2.pdf#page=6|p.6 §2.5]]

### NaFlex到底保留了什么？

给定patch size和目标sequence length，输入resize后的高宽为patch大小整数倍，实际patch数不超过目标长度，并尽量减少比例变形。因此“native aspect ratio”是**尽量保持**，并非数学上的零失真。实际grid不足长度时padding；attention和MAP都通过mask忽略padding。原始16×16的可学习位置grid经带anti-aliasing的双线性插值变为当前非方形grid。[[raw/papers/vision/alignment/SigLIP2.pdf#page=4|p.4 §2.4.2]]

正文列出的训练长度是 $\{128,256,576,784,1024\}$。Fig.3/Table7还报告64、144、676、900等评测长度；**报告结果不等于该长度参加了训练**。Fig.3 caption对“横轴标注均是训练长度”的概括与正文128及图中64也不完全一致，本页以§2.4.2明确列表登记训练配置，并保留这项版本内差异。作者说训练范围间插值较好、向范围外外推较差（外推图未展示）；不能宣传为任意尺寸无损。[[raw/papers/vision/alignment/SigLIP2.pdf#page=5|p.5 §2.4.2]]、[[raw/papers/vision/alignment/SigLIP2.pdf#page=7|p.7 Fig.3]]、[[raw/papers/vision/alignment/SigLIP2.pdf#page=18|p.18 Table 7]]

## 哪些实验真正检验了dense features和定位？

| 实验问题 | 协议与代表结果 | 证据含义 |
| --- | --- | --- |
| 全局分类/检索是否改善？ | 固定L/16、256px、256tokens：ImageNet val零样本80.5→82.5；COCO T→I R@1 51.2→54.7，SigLIP→SigLIP2 | 组合配方的同尺度比较；不是只换一个loss的消融。[[raw/papers/vision/alignment/SigLIP2.pdf#page=5\|p.5 Table 1]] |
| 冻结视觉表示能否供dense任务使用？ | 冻结特征加linear或DPT probe；So/14、384px：ADE20k mIoU40.8→45.4，NYUv2 depth RMSE0.563→0.466 | 训练了下游头，并非编码器直接零样本输出深度/分割；MAP embedding替代协议中的CLS拼接。[[raw/papers/vision/alignment/SigLIP2.pdf#page=9\|p.9 Table 2、§3.3.1]] |
| 语言指定区域能否被定位？ | 冻结未池化特征，另训6层cross-attention decoder，使用RefCOCO各版本混合；L、256tokens：RefCOCO val Acc@0.5为67.33→86.04 | 下游定位probe大幅提升；未复用预训练decoder。该同尺度行仍低于LocCa的88.34。[[raw/papers/vision/alignment/SigLIP2.pdf#page=9\|§3.4.1]]、[[raw/papers/vision/alignment/SigLIP2.pdf#page=11\|p.11 Table 5]] |
| 能否支持开放词汇分割/检测？ | Cat-Seg在COCO-Stuff-164k、172类训练，再跨词表测试；OWL-ViT适配后B/16 LVIS APr31.0→32.7 | 这些是训练后系统的评测，不是原编码器无需适配即可分割/检测。[[raw/papers/vision/alignment/SigLIP2.pdf#page=9\|pp.9–10 §3.3.2、Tables 3–4]] |
| NaFlex是否总更好？ | B/16、256tokens：HierText T→I R@1标准6.1、NaFlex7.4；ImageNet val标准79.1、NaFlex78.5 | 文档/文字相关任务常获益，标准B模型在自然图像上仍有优势；两分支的自监督和小模型蒸馏不同。[[raw/papers/vision/alignment/SigLIP2.pdf#page=18\|p.18 Table 7]] |

上面不能合成为无条件“全面超越”。Table1中mSigLIP So/16的XM3600检索高于SigLIP2，某些DFN检索行也更高；Table6逐任务存在回退，例如Large的AOKVQA-MC val由78.3到77.6。作者的总体优势主张应理解为广泛任务/规模的趋势，不是每格必胜。[[raw/papers/vision/alignment/SigLIP2.pdf#page=5|p.5 Table 1]]、[[raw/papers/vision/alignment/SigLIP2.pdf#page=17|p.17 Table 6]]

### 作为VLM底座：提升发生在哪个协议里？

作者把视觉编码器与 **Gemma 2 2B** 组合，保持视觉编码器冻结，在caption、OCR、grounded caption、VQA、检测、实例分割混合上训练50M **examples**，再按各下游数据集fine-tune。224/256px比较控制为256视觉tokens；384px重新跑stage1，而非从低分辨率模型简单继续。Fig.4 caption写“50M steps”，与正文“50M examples”有单位冲突，本页采用正文的样本预算并登记冲突，不能据图注算出5000万优化步。[[raw/papers/vision/alignment/SigLIP2.pdf#page=8|pp.8–9 §3.2、Fig.4]]、[[raw/papers/vision/alignment/SigLIP2.pdf#page=17|p.17 Table 6]]

这支持“在该VLM构建/任务适配协议中，替换视觉表征通常有益”。它没有证明任意LLM、任意connector、冻结/全参数训练或更长视觉token预算都有相同比例收益。旧TeX的“冻结对质量几乎无影响”来自本文对另一工作的引用，不能当作本报告独立做了冻结/解冻消融。

## 组合配方的证据限度与公平性

本版未给出把所有新组件逐一移除的完整受控消融矩阵。它有跨模型、跨尺度、分辨率与训练分支比较，但数据混合、去偏、decoder、自监督、额外蒸馏及预算同时变化。作者把定位提升归于decoder预训练，把某些差距归于多语言数据，这是作者解释；本文结果本身不能唯一确定各因素的因果贡献。[[raw/papers/vision/alignment/SigLIP2.pdf#page=9|pp.9–10 §3.4.1]]、[[raw/papers/vision/alignment/SigLIP2.pdf#page=7|p.7 §3.1.1]]

公平性也必须按指标说：L/16 256px的representation bias由35.5降为7.3，但Dollar Street按收入分组的最大准确率差距仅32.0→31.1。第一项测随机对象与性别的关联倾向，第二项测收入群体性能差距，均不能概括为“已消除偏见”。作者明确说按收入/地理群体拆分时收益有限或没有收益。[[raw/papers/vision/alignment/SigLIP2.pdf#page=11|p.11 §3.5]]、[[raw/papers/vision/alignment/SigLIP2.pdf#page=20|p.20 Table 9]]

## 旧笔记修订与本库落点

- 旧TeX已正确写80%节点，但主线需显式解释原图的20%为训练时段；loss权重、两种50%以及90/10语言比例分别标注。
- “SigLIP2采用NaFlex”收紧为**另一个变体**；标准分辨率checkpoints、NaFlex、B模型数据筛选阶段分开登记。NaFlex不继承全部自监督目标，且并非任意比例完全无失真。
- 旧稿“性能都优于其他基准”改为带反例与任务条件的总体趋势；dense和定位分数明确需要下游训练。
- 原文引用的LocCa/SILC/TIPS等机制仍标为**本报告的采用说明**，不新建被引论文页或增加精读来源数。

建议整合主题：全局对齐与局部特征、视觉预训练目标组合、分辨率/视觉token预算、视觉编码器对MLLM的迁移。可继续追问：固定数据与总成本时哪个新增监督提供多少收益；NaFlex和固定分辨率在相同训练目标下如何比较；新编码器对未测LLM及真实文档长宽比的收益是否稳定。这些是待检验问题，不是已证实的研究空白。
