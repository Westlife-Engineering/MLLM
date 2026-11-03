---
type: paper
source_id: S016
primary_direction: architecture/visual-interfaces
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/architecture/visual-interfaces/Flamingo.pdf]]"
reading_status: read
ingest_status: complete
related_directions:
  - architecture/multimodal-backbones
---

# Flamingo：把交错视觉上下文接入冻结语言模型

> [!note] 主归属（本库导航判断）
> 保留视觉接入主归属：Resampler 与插入冻结 LM 的 gated cross-attention 已能组织核心接口论证。交错数据、few-shot 协议与模型家族共同贡献保留；不因完整系统存在而迁入系统目录。 [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=4|pp.4–6，贡献/§2/Figs.3–4]]

> [!important] 核心理解与证据边界
> Flamingo 用 **Perceiver Resampler 压缩每个视觉输入**，再以 **gated cross-attention 在冻结 LM 内部多处注入视觉条件**。训练于交错网页及图文、视频文对后，它用提示中的示例适应任务，few-shot 阶段不更新权重。论文的证据是指定数据、模型与提示协议下的图像／视频任务表现，不能推出任意多图推理可靠，也不能把效果全归因于一个“adapter”。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=4|§2，图3]] [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=8|§3，表2–3]]

## 来源身份与本次阅读

- **标题／作者／发表**：*Flamingo: a Visual Language Model for Few-Shot Learning*；Jean-Baptiste Alayrac、Jeff Donahue、Pauline Luc、Antoine Miech 等，DeepMind；NeurIPS 2022。身份以本地 PDF 首页核对。
- **固定版本**：arXiv:2204.14198v2，2022-11-15；[原始 URL](https://arxiv.org/pdf/2204.14198v2)。本地原件：[[raw/papers/architecture/visual-interfaces/Flamingo.pdf]]，54 页；PDF 页码与正文印刷页码一致。
- **SHA-256**：`27af622bf50987fd98a03451a27a670adfaeefd5218a3e990b37abc326ba63f0`，本次核对字节一致；哈希不替代身份核验。
- **读取日期／范围**：2026-10-31；正文 PDF pp.1–10，关键附录 pp.23–36（结构、数据、训练、划分、评估、消融），pp.41–42 局限；实际渲染检查 pp.4、5、6、7、8、23、24、35 的架构、公式、mask 和结果表。
- **未穷尽**：参考文献逐项、pp.37–40 全部定性样例、pp.43–54 社会影响／model card／datasheets／图片授权未逐项核读；不宣称代码审计、复现或 Obsidian 显示实测。
- **旧笔记输入**：[[raw/notes/多模态经典/2022-NeurIPS-Flamingo.md]]、[[raw/notes/多模态经典/2022-NeurIPS-Flamingo总结.tex]]、[[raw/notes/多模态经典/Latex_out/2022-NeurIPS-Flamingo总结.pdf]]。本次对照 Markdown 与 TeX 正文；冻结 PDF 仅登记包成员。这些是二手输入，不是独立学术来源。

## 它要解决的任务变化是什么

目标不是为每个任务再训练一个头，而是让同一模型接收 `图像／视频—文本—图像／视频—文本` 的上下文，最后生成查询视觉输入的文本答案。开放任务用生成，封闭候选任务用条件 log-likelihood 排序。这里的“适应”是 in-context learning：支持示例占用推理上下文，没有梯度更新。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=6|§2.5]] [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=25|附录A.2，图8]]

## 信息如何经过三段结构

### 1. 视觉编码器与 Resampler：变长网格转成64个槽位

视觉编码器为预先用 ALIGN＋LTIP 图文对比学习得到的 **NFNet-F6**；Flamingo 主训练冻结它。输出保留空间网格，视频逐帧编码，加可学习**时间** embedding 后展平。Resampler 用64个 learned latents 作 query，而 key/value 是视觉特征与当前 latents 的拼接；6层、hidden size 1536、16 heads，约194M参数。它不是简单平均池化，也不是把64个独立类别逐一识别出来；槽位的语义没有这种先验规定。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=5|§2.1]] [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=23|附录A.1.1，图5]] [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=25|表4]]

依图5可将一次更新写作：

$$
X\leftarrow X+\operatorname{Attention}(Q=X,K=V=[X_f;X]),\qquad
X\leftarrow X+\operatorname{FFW}(X).
$$

这里是概念化记法，省略投影与归一化。论文没有添加显式 spatial grid position embedding；作者推测 CNN 通道已隐含空间信息，不是证明所有视觉编码器都不需要位置编码。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=23|附录A.1.1，图5及解释]]

### 2. Gated XATTN-DENSE：注入点位于已有LM块之前

语言隐状态 $Y$ 作 query、64个视觉 token 作 key/value。新增 cross-attention 与新增 FFW 各有独立可学习标量 gate，初始化为0：

$$
Y' = Y+\tanh(\alpha_{\mathrm{xattn}})\operatorname{XAttn}(Y,X),\qquad
Y''=Y'+\tanh(\alpha_{\mathrm{dense}})\operatorname{FFW}(Y').
$$

随后才进入冻结 LM 原有 self-attention／FFW。零初始化令新增残差分支初始贡献为0；**不是把 LM 原有注意力改成 cross-attention，也不是只在输入端拼视觉前缀**。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=5|图4、§2.2]]

| 模型 | 冻结Chinchilla | 新块位置 | 新cross-attention模块参数 |
| --- | --- | --- | --- |
| Flamingo-3B | 1.4B，24层 | 从首层起，每个LM块之前 | 1.2B |
| Flamingo-9B | 7.1B，40层 | 从首层起，每4个LM块之前 | 1.6B |
| Flamingo-80B | 70B，80层 | 从首层起，每7个LM块之前 | 约10B |

共同冻结视觉编码器435M、共同训练Resampler194M；表中参数分量来自表5，不能将“冻结大部分参数”误写为整个模型只训练一个很小线性层。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=28|表5]] [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=29|附录B.1.1]]

### 3. Image causality：直接看最近图，间接保留历史图

正常推理时，每个文本 token 的 cross-attention 只看其前面最近的一个图像／视频；在第一张图之前没有可见视觉输入。更早图像的影响可经已被视觉条件化的历史文本隐状态，再通过 LM causal self-attention 传播。因此，“只直接看一图”不等于“上下文只能容纳一图”。图7里的深色 mask 表示允许访问的视觉块，而不是给每张图建立一个独立语言模型。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=6|§2.3]] [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=24|附录A.1.3，图7]]

> [!note] 训练数据增强的例外
> M3W 网页中图文对应不明确，训练时以 $p_{next}=0.5$ 按网页随机选择文本对齐前一图或后一图；不能把“推理只看最近前图”未经限定地推广为所有训练样本都按网页原顺序只看前图。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=27|附录A.3.2]]

## 为什么需要交错数据，训练成本又是多少

M3W 从约4300万网页获得交错图文，每个样本随机取256个文本 token、最多5张图。另混合 ALIGN 1.8B图文对、LTIP 312M图文对、VTP 27M视频文对（视频平均约22秒）。对各数据集的条件文本负对数似然加权，权重分别1.0／0.2／0.2／0.03，跨数据集累积梯度。主训练视觉输入320×320；视频训练8帧、1 FPS，推理30帧、3 FPS并插值时间 embedding。正文的1 FPS不能当作所有推理设置。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=6|§2.4，式2]] [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=29|附录B.1.2]]

论文报告通常训练500k steps，80B使用1536个TPUv4芯片训练15天；这不包含“只训练新增层所以训练几乎免费”的含义。分辨率、视频帧数、语言模型预训练和数据规模都属于结果条件。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=29|附录B.1.2]]

## 结果怎样读才不夸大

主要16个多模态benchmark中，COCO、OKVQA、VQAv2、MSVDQA、VATEX这5个DEV任务参与设计选择，其余11个在设计结束后评估。支持集与查询集分离；DEV还区分validation与test的support/query。正文所谓zero-shot开放任务仍给**两个去掉视觉输入的任务文本示例**；封闭候选评分可以不给文本示例。开放生成通常beam size 3。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=7|§3]] [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=26|附录A.2]] [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=31|附录B.1.4]]

| 同为Flamingo-80B、不更新权重 | 0-shot | 4-shot | 32-shot | 条件／指标 |
| --- | ---: | ---: | ---: | --- |
| OKVQA | 50.6 | 57.4 | 57.8 | val，VQA accuracy |
| VQAv2 | 56.3 | 63.1 | 67.6 | test-dev，VQA accuracy |
| COCO | 84.3 | 103.2 | 113.8 | test，CIDEr |
| MSVDQA | 35.6 | 41.7 | 52.3 | test，top-1 accuracy |

数值来自表1，划分／指标对照附录表6；这些不同指标不能直接相加排名。论文正文称32-shot超过fine-tuned SotA的任务为6个，表1caption却写7个；本库保留版本内不一致，不以caption扩张主张。表2的下游fine-tuning另外解冻视觉编码器、提高到480×480，LM仍冻结，不能与不更新权重的few-shot混为同一协议。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=7|表1及§3.1]] [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=31|表6]] [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=33|附录B.2.2]]

消融是 **Flamingo-3B、5个DEV验证子集、4-shot、较短训练／较小batch**；Overall是各任务分数除以所选SotA再平均的聚合量。基线70.7，去M3W为53.4、去tanh gating为66.5、Resampler换MLP为66.6；只看最近图70.7，直接看所有历史图63.5。这支持这些设计在该组合中有用，但不证明每个模块“不可替代”，也不独立识别80B最终表现的因果贡献。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=8|表3与§3.3]] [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=35|表10及B.3.1]]

## 局限与旧笔记校正

- **泛化边界**：训练最多5图，评估可受益于最多32个示例，是有限范围内的证据，不是无限上下文承诺。作者报告超过低样本范围会遇到上下文成本、提示敏感、性能平台；定性对话样例也不等于可靠多图推理评测。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=10|§5]] [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=41|附录D.1]]
- **数据重叠**：配对图文做了指定数据集去重；M3W没有训练前整库去重，事后在所查集合发现125个exact duplicates；VTP未做该去重。不能说所有评估样本已全面排除。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=28|附录A.3.4]]
- **旧TeX“层越深视觉语义融合越大”应收回**：图6画的是gate绝对值；作者明确提醒各层门前激活尺度可能不同，不能据此直接量化语义融合强弱。[[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=23|附录A.1.2]]
- **旧TeX“gating、resampler、cross attention都是必须的”改为受条件约束的消融优势**；替代结构仍有非零性能。旧Markdown称VLM术语使用的“起点”没有本论文内足够历史证据，本页不采用。旧稿对1 FPS与mask的表述补上了训练／推理及M3W增强区别。

## 本库整合问题

本页支持：视觉token压缩与LLM内部注入的区别；冻结参数如何影响训练成本与遗忘；交错数据、attention mask与in-context评估之间的关系。与其他连接机制的正式比较需回到各自原文及同条件实验，不能由模块外观相似直接判断优劣。实际双向主题关系见页末。

## 实际整合关系

支撑64-latent压缩与LM内部gated CA分工、最近图直接可见性及交错训练/ICL条件。

- [[wiki/architecture/Visibility-and-Connections|可见性、路由与连接：视觉信息在哪里与语言相遇？]]。
- [[wiki/foundations/Formalization|基础：把信息、参数与任务证据分成三个层次]]。
- [[wiki/models/Family-Changes|家族变化轴：输入、接口、数据和计算怎样共同演进？]]。
