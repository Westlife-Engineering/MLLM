---
type: paper
source_id: S017
primary_direction: architecture/connectors
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/architecture/connectors/BLIP-2.pdf]]"
reading_status: read
ingest_status: integrating
---

# BLIP-2：先训练视觉查询，再对齐冻结语言模型

> [!important] 核心理解
> BLIP-2 将“提取与文本有关的视觉表示”和“让已有 LLM 使用这些表示”分成两段预训练。Q-Former 输出32个 query 表示，经线性投影作为 LLM 的视觉前缀；**两侧冻结适用于预训练**，论文的下游 captioning／VQA／retrieval 微调会更新视觉编码器。三种第一阶段 mask 是控制信息通路，不是三个独立模型。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=3|§3.1–3.2，图2]] [[raw/papers/architecture/connectors/BLIP-2.pdf#page=4|§3.3，图3]] [[raw/papers/architecture/connectors/BLIP-2.pdf#page=7|§4.2–4.3]]

## 来源与阅读范围

- **身份**：Junnan Li、Dongxu Li、Silvio Savarese、Steven Hoi，*BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models*，Salesforce Research。固定 arXiv:2301.12597v3（2023-06-15），[原件URL](https://arxiv.org/pdf/2301.12597v3)；首页核对标题／作者／版本。
- **原件**：[[raw/papers/architecture/connectors/BLIP-2.pdf]]，13页；以下使用PDF页序。SHA-256：`6bc5d399d6127a64ace5167a2f0c00112a49725d2475d80322dbf0083f139e80`，本次复核一致。
- **2026-10-31实际读取**：正文pp.1–8，附录pp.12–13的微调参数／失败样例／VQA结构；参考文献不逐项核读。实际渲染查看pp.3、4、6、7、8、12、13，核对mask、阶段结构、结果表和视觉编码器解冻标记；无代码审计／复现，Obsidian内显示未测。
- **旧笔记输入**：[[raw/notes/多模态经典/2023-ICML-BLIP-2.md]]、[[raw/notes/多模态经典/2023-ICML-BLIP-2总结.tex]]及其冻结编译包[[raw/notes/多模态经典/Latex_out/2023-ICML-BLIP-2总结.pdf]]。本次对照前两者；旧代码摘录不是本次实际核读仓库。

## 连接的具体困难

冻结视觉模型和LLM避免重训两大骨干，但它们并没有自动共享表征接口：视觉网格不能仅因维度相同就被LLM正确解释。作者让Q-Former先获得受文本监督的视觉瓶颈，再通过冻结LLM的生成损失训练该接口。该方法减少可训练参数，却仍需视觉前向、LLM前向及通向连接器的梯度计算；不是跳过大模型计算。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=2|§3]] [[raw/papers/architecture/connectors/BLIP-2.pdf#page=4|§3.3–3.4]]

## 第一阶段：同一个Q-Former，三条不同的信息通路

Q-Former从BERT-base初始化，新增cross-attention随机初始化；32个learned queries，每个768维，输出 $Z\in\mathbb{R}^{32\times768}$。query经共享self-attention互相交互，每隔一个Transformer block通过cross-attention读冻结视觉特征。文本分支与query分支共享self-attention；称为“两套互不相关的塔”会漏掉这一关键。整体Q-Former报告188M参数，query本身也属于参数。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=3|§3.1，图2]]

| 目标 | query能看什么 | text能看什么 | 监督读出与目的 |
| --- | --- | --- | --- |
| ITC：image-text contrastive | 其他query与视觉；不能看text | text双向；不能看query | 每个query与文本CLS算相似度，取最大值作图文相似度；in-batch negatives |
| ITM：image-text matching | query和所有text，并从视觉提特征 | 所有query和text | 各query输出二分类logits，跨query取平均，判断配对；用hard negative mining |
| ITG：image-grounded text generation | query彼此可见，不能看text | 所有query和过去text，不能看未来text | 以图像为条件预测文本；起始CLS换为DEC |

依据图2与§3.2；ITC的禁止交互用于防止目标信息泄漏，ITG的因果限制保证生成条件，ITM则需要双向融合。三种mask不能统一理解成“因为共享权重所以都防泄漏”。文本本身没有直接连到视觉编码器的cross-attention，ITG迫使视觉信息先经过query。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=3|图2、§3.2]]

## 第二阶段：query变成哪一种LLM输入

视觉编码器继续冻结，Q-Former继续训练，新FC层把768维query表示投影到所选LLM的embedding维度，拼在文本embedding前。

- **OPT（decoder-only）**：视觉前缀条件下，预测整段文本，使用language modeling loss。
- **FlanT5（encoder-decoder）**：将文本分prefix与suffix，视觉前缀＋prefix进encoder，decoder预测suffix，使用prefix language modeling loss。

图3明确是**线性FC投影**；本论文没有把它描述为任意多层MLP。第一阶段的ITG由Q-Former文本分支完成，第二阶段的文本生成由外部冻结LLM完成，二者不能混为同一次生成。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=4|§3.3，图3]]

与已核读的[[wiki/papers/architecture/connectors/Flamingo|Flamingo]]相比，这里的视觉信息先变成LLM输入前缀；Flamingo则在冻结LM内部插入多个gated cross-attention块。两者都有query式视觉压缩，但注入位置、训练目标、可训练参数和交错训练数据并不相同。[[raw/papers/architecture/connectors/Flamingo.pdf#page=5|图4]] [[raw/papers/architecture/connectors/BLIP-2.pdf#page=4|图3]]

## 数据、骨干和预算构成了实验条件

预训练共129M图像，含COCO、Visual Genome、CC3M、CC12M、SBU和115M LAION400M图像。CapFilt用BLIP-large每图生成10个caption，再与原caption一起经CLIP ViT-L/14排序，保留前2个，训练时随机取一个。视觉骨干为CLIP ViT-L/14或EVA-CLIP ViT-g/14，使用倒数第二层特征；预训练图像224×224。语言骨干测试OPT2.7B／6.7B与FlanT5-XL／XXL。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=4|§3.4]] [[raw/papers/architecture/connectors/BLIP-2.pdf#page=6|表2]]

第一阶段250k steps，batch 2320（ViT-L）／1680（ViT-g）；第二阶段80k steps，batch1920（OPT）／1520（FlanT5）。最大ViT-g＋FlanT5-XXL在16张A100 40GB上，报告两阶段分别少于6天、3天。该成本不包含骨干已有预训练，也不能仅据可训练参数比例推导实际速度比。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=4|§3.4]]

## 哪些结果来自预训练，哪些已微调

| 结果 | 具体配置与数值 | 必须保留的协议 |
| --- | --- | --- |
| Zero-shot VQA | ViT-g＋FlanT5-XXL：VQAv2 test-dev 65.0、OK-VQA test45.9、GQA test-dev44.7 | 无VQA下游微调；beam5、length penalty −1；FlanT5提示含Short answer |
| COCO caption／NoCaps | ViT-g＋FlanT5-XL：COCO CIDEr144.5；NoCaps val CIDEr121.6、SPICE15.8 | 先在COCO微调视觉编码器＋Q-Former；NoCaps是未在NoCaps训练的迁移 |
| VQA fine-tuned | ViT-g＋OPT6.7B：VQAv2 test-dev82.19、test-std82.30 | VQAv2 train/val＋VG训练；更新视觉编码器和Q-Former；问题也输入Q-Former |
| Retrieval | ViT-g：Flickr30K 1K test图→文R@1 97.6、文→图89.7 | 第一阶段模型、不接LLM；COCO微调，再迁移Flickr30K；相似度选128候选再ITM重排 |

分别见[[raw/papers/architecture/connectors/BLIP-2.pdf#page=6|表2、§4.1]]、[[raw/papers/architecture/connectors/BLIP-2.pdf#page=7|表3–4、§4.2–4.3]]、[[raw/papers/architecture/connectors/BLIP-2.pdf#page=8|表5、§4.4]]。下游5个epochs；caption/retrieval分辨率364，VQA分辨率490；不是将所有表格视为同一224分辨率、两侧冻结模型。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=12|表7–9]]

作者与Flamingo-80B比较的VQAv2差值是65.0−56.3＝**8.7个百分点**；“54倍更少可训练参数”来自10.2B对188M的预训练口径。表2生成配置另列约103–108M，不能把两个口径混写；总参数、数据、LLM、提示均不同，该跨模型比较不证明Q-Former对Flamingo连接器的独立因果优势。OK-VQA上Flamingo-80B的50.6仍高于45.9。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=6|表1–2]]

图5在ViT-g＋OPT6.7B及FlanT5-XL下比较有无第一阶段，去掉后zero-shot VQA明显更差，支持两阶段配方在该设置中的作用。它不等于证明任何模型只用生成损失都不能成功。表6中COCO retrieval加入ITG后图→文R@1由84.5到85.4，文→图由67.2到68.3，是有条件的小幅支持。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=7|图5]] [[raw/papers/architecture/connectors/BLIP-2.pdf#page=8|表6]]

## 必须修正的旧笔记判断

1. **“视觉模型始终冻结”**应限定为BLIP-2预训练；正文下游微调明确更新视觉编码器。图7的问题条件化Q-Former也表明，不能将所有使用场景都说成“Q-Former从不读问题”。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=7|§4.2–4.4]] [[raw/papers/architecture/connectors/BLIP-2.pdf#page=13|图7]]
2. **“hidden_dim全部设为vision_dim”错误**：论文明确query hidden为768，举例ViT-L视觉特征宽度1024；cross-attention投影可以处理不同输入宽度。旧代码里的encoder_width不等于把全部hidden_size重设。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=3|§3.1]]
3. **旧稿同时写“无hard negative”和“每次必取最高负例”**：前者与§3.2明确采用hard negative mining冲突；后者是过强的实现断言，本次未审计仓库，也未另读被引ALBEF方法，不把它当本文正文已证明的确定argmax策略。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=3|ITM段]]
4. **“MLP或cross-attention普遍优于Q-Former”“理论和实验证明Q-Former导致DocVQA不足及幻觉”**没有这篇原文的对应控制实验，本库撤回为定论。瓶颈可能损失细节是合理待检验问题，不能由32个token直接推出具体任务失败的唯一原因。
5. 旧稿“query已理解图片”“生成能力都来自LLM”换成可操作描述：query学习了有利于文本任务的视觉表示；系统能力受视觉表征、训练目标、投影、LLM及数据共同影响。定性图4不能把所有推理能力评为已量化成立。

## 局限与后续问题

作者未观察到加入in-context VQA示例能提升该模型表现，并将其归因于单图文对训练缺少跨样例关联；这是作者解释，不是已排除所有架构／提示因素的因果实验。失败图6展示知识、推理和时效错误；论文正文§5误指Figure7，本页按实际失败图所在p12 Figure6定位。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=8|§5]] [[raw/papers/architecture/connectors/BLIP-2.pdf#page=12|图6]]

可整合主题：视觉信息瓶颈与注入位置、三目标mask、预训练与下游微调的冻结边界、zero-shot transfer的不同含义。主题页建立后由协调者补双向链接。
