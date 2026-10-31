---
type: paper
source_id: S020
primary_direction: architecture/connectors
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/architecture/connectors/mPLUG-Owl.pdf]]"
reading_status: read
ingest_status: complete
---

# mPLUG-Owl：分阶段调整视觉与语言参数，使用视觉抽象器压缩输入

> [!important] 核心理解与尚未解决的版本冲突
> 第一阶段训练视觉编码器与visual abstractor、冻结LLaMA；第二阶段冻结视觉编码器、通过LoRA调整语言行为，并混合纯文本与多模态指令。**第二阶段abstractor是否继续训练，固定v3内部说法不一致**：摘要／引言称与LoRA一起训练，图2及§3.2却画／写成冻结原模型后仅加LoRA。本页并列保留，不能冒充已由代码确认。模型优势主要来自作者自建小规模OwlEval与定性例子，不应等同通用多模态推理优势。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=1|摘要]] [[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=4|图2、§3.2]]

## 来源身份与读取记录

- **身份**：Qinghao Ye、Haiyang Xu、Guohai Xu 等；*mPLUG-Owl: Modularization Empowers Large Language Models with Multimodality*，Alibaba DAMO Academy；首页Preprint / Under review。
- **固定版本**：arXiv:2304.14178v3，2024-03-29。虽然工作名称常与2023年相关，本页依据已存v3，不混用其他版本。[原件URL](https://arxiv.org/pdf/2304.14178v3)；[[raw/papers/architecture/connectors/mPLUG-Owl.pdf]]，21页。
- **SHA-256**：`997b330fb3b0b6e4972f7e98ae7753cfbadf81512d0d070eae654e3be2085ffd`，本次复核一致。
- **2026-10-31实际读取**：正文pp.1–14，关键附录p18训练表／MM-REACT比较，pp.19–21样例文字；参考文献未逐项核读。渲染检查pp.3、4、6、7、8、9、18的参数冻结图、abstractor、判分／消融及训练表。附录全部截图文字并未逐像素核对；无代码审计、复现或Obsidian显示实测。
- **旧输入**：[[raw/notes/多模态经典/2023-mPLUG-OWL总结.tex]]与[[raw/notes/多模态经典/Latex_out/2023-mPLUG-OWL总结.pdf]]；已对照TeX正文与其中代码摘录，冻结PDF仅登记包成员。旧代码不能替代对应版本仓库核验。

## Visual Abstractor究竟抽象了什么

视觉骨干 $f_V$ 是CLIP初始化的ViT-L/14（24层、hidden1024、patch14），LLM $f_L$ 是**原始LLaMA-7B**，并非先用Vicuna。图像被转成密集patch特征；visual abstractor $f_K$ 以learnable tokens作为query，通过cross-attention读视觉信息，将长视觉序列汇聚成较短的语义序列，再与文本输入组合进入LLM。论文总模型参数报告约7.2B；此数字不等于本轮可训练参数。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=4|§3.1，图2]] [[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=5|§4.1]]

图2的abstractor放大图显示：learnable token既作为查询，也与patch feature拼接后进入cross-attention的另一输入支路。这与已核读[[wiki/papers/architecture/connectors/Flamingo|Flamingo]]图5中latent＋视觉特征构成K/V的结构相似；但mPLUG-Owl的结果在**LLM输入端**与文本组合，不采用Flamingo插入LLM多个内部层的gated cross-attention路线。不能把两个“有query压缩”模块看成整个系统等同。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=4|图2]] [[raw/papers/architecture/connectors/Flamingo.pdf#page=23|图5]] [[raw/papers/architecture/connectors/Flamingo.pdf#page=5|图4]]

> [!note] 本版本没有交代到的实现量
> 已核正文／附录没有明确给出abstractor的query数、层数、hidden维度、LoRA rank及具体注入模块。它说“several learnable tokens”而非一个可直接复现的完整配置。本库不从其他mPLUG版本或旧代码片段补猜，也不把“高层语义表示”当作每个token均有明确可解释概念的证明。

## 两阶段训练：哪些参数动、哪些数据进来

| 模块／数据 | Stage 1：multimodal pretraining | Stage 2：joint instruction tuning |
| --- | --- | --- |
| ViT视觉骨干 | 可训练 | 冻结 |
| Visual abstractor | 可训练 | 摘要／引言：可训练；图2／§3.2：冻结，待核 |
| 原始LLaMA权重 | 冻结 | 基础权重冻结，训练新增LoRA |
| 输入监督 | 图像-caption对 | 纯文本指令＋图文指令 |
| 预测目标 | 条件文本token | 对话中的response token，不对视觉连续表示算生成目标 |

第一阶段参数路线在原文内部一致；第二阶段冲突见p1摘要、p2引言与p4图2／p4–5§3.2，不能只选最符合旧认知的一处。这里的LoRA也不等于全量微调LLM。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=2|引言]] [[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=4|§3.2]] [[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=5|训练目标]]

第一阶段数据来自LAION-400M、COYO-700M、Conceptual Captions、MSCOCO；224×224输入，50k steps，正文报告每batch约2.1M tokens、累计约104B tokens。SentencePiece是tokenizer，不是新的文本编码器。第二阶段纯文本数据为作者报告的Alpaca102k、Vicuna90k、Baize50k，加LLaVA多模态指令**150k**；2k steps，总batch256，learning rate $2\times10^{-5}$，按纯文本和多模态多个batch累积梯度。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=5|§4.1]]

### 第一阶段超参数的版本内不一致

| 项 | 正文§4.1（p5） | 附录A表4（p18） |
| --- | --- | --- |
| Learning rate | $10^{-4}$ | $2\times10^{-4}$ |
| Weight decay | 0.1 | 0.01 |
| Warmup steps | 2,000 | 375 |
| Batch说明 | 2.1M tokens | 4,096 image-caption pairs；max length512 |

token batch与样本batch可以是两种描述口径，不能直接认定矛盾；但前三行确实无法从本版本消解。第二阶段附录表5还给文本与图文batch各128、max length1024、warmup50、weight decay0.0001。不能用一份漂亮的超参数表掩盖正文冲突；本轮不启动训练，也未取得对应代码commit来裁定。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=5|§4.1]] [[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=18|附录A，表4–5]]

## OwlEval测到什么，怎样得到分数

**测量定位（本库归纳）**：在作者选定的50张图、82个开放问题及指定baseline运行方式下，以人工回答质量与能力标签评估系统的视觉相关指令响应，适合发现典型失败和比较该集合内表现；对真实工作分布、通用推理或可靠部署表现的代表性有限。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=6|§4.2]]

图片来自MiniGPT-4演示21张、MM-REACT13张、BLIP-2 9张、GPT-4 3张和作者补充4张。问题覆盖自然图、图示／流程图、OCR、创作、知识QA与指代交互，部分多轮。它不是从广泛用户流量随机抽样，也未给独立的大规模样本量。一个图的多轮问题高度相关，82个回答不能视为82个独立场景。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=6|§4.2]]

以p9图6为例：用户先问图中右侧人物，后续问左侧人物、其动作和手中物体；模型要结合原图与对话中的指代给答案，人工评审再给回答等级。这样的题保留了自然多轮上下文，却不包含实际环境操作、工具执行或外部结果验收；自然语言看似合理仍可能认错人／物。图中展示A/B等标签，但不能用某一例的A级推导所有指代任务可靠。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=9|图6]]

总体回答按A>B>C>D人工分级。图3报告mPLUG-Owl的A/B/C/D分别51／15／16／0，总82；MiniGPT-4为46／8／26／2，A+B是66对54。**无D不是所有答案完全正确**，仍有B/C。具体A–D rubric在本版本仅指向Self-Instruct评分方法，未完整展开；本次未扩读该被引来源，不能补造其定义。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=6|图3及§4.2]]

能力诊断另分IU、VU、OCR、KTA、RA、MDA：IU只要求理解／回应指令，不要求正确；VU/OCR要求反映超过60%相关视觉／文字信息，KTA与MDA等采用超过80%的描述性门槛。作者先人工标题目所需能力，再标回答体现哪些能力；这些“百分比”来自人工判断标准，不能自动当逐token客观准确率。已核原文未充分报告评分者人数、盲法、分歧裁决、人与人一致性或置信区间，不能因人工评分就宣称已完成独立可靠性验证。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=7|§4.3]] [[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=8|表1–2]]

单轮集合是50图的首问，多轮集合含52个问题；二者有重叠，因此50＋52不是另一套102个互异问题。MM-REACT比较排除了它未成功生成的样例，p18图15是在改变后的有效样本集合上比较，不是全82题的无条件成功率。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=6|§4.2]] [[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=7|图4]] [[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=18|附录B，图15]]

## 消融证明了整套训练有用，但不独立验证每个部件

表2中完整两阶段＋两类指令（r5）在IU／VU／OCR／KTA／RA／MDA分别100.0／95.2／56.7／87.5／80.0／95.0。去掉指令训练r1明显下降；只做指令而无多模态预训练r2也下降。它支持前置视觉学习与后续指令学习在作者设定内互补，但没有独立控制“仅换视觉编码器冻结状态”或“仅换abstractor结构”，不能把全部差值归给可训练ViT。各列分母是需要对应能力的题目，不是所有82题，也不能将六列直接当六份相同样本量的测试。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=8|表2]]

> [!warning] r3／r4编号也有冲突
> 表2勾选标明r3＝预训练＋纯文本指令，r4＝预训练＋多模态指令；但p7说明及p9表3把“无multimodal tuning”的文本版本标为r4。这里保留语义描述，不把冲突编号用来推导额外结论。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=7|Instruction Data Ablation]] [[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=8|表2]] [[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=9|表3]]

80个纯文本问题由ChatGPT分别评候选与ChatGPT参照回答，表3比例为86.07%到86.71%。这些是judge总分比，不是“获得ChatGPT 86.71%的真实能力”；比较对中的ChatGPT参照总分也从682变692。未给重复评分方差／人评校准，0.64个百分点的变化不能独立建立统计显著的纯文本能力提升。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=7|§4.3及脚注8]] [[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=9|表3]]

baseline来源混合本地released code与在线demo：OpenFlamingo-9B、BLIP-2 ViT-G FlanT5-XXL采用代码，MiniGPT-4／LLaVA／MM-REACT采用demo。论文没有给齐所有demo的固定快照、采样参数、版本与运行预算；结果是这些运行配置的比较，不能自动升级为对各模型所有可用配置的排名。OpenFlamingo也不是原始Flamingo的同一权重。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=5|§4.1 Baselines]] [[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=6|Baselines续]]

## 局限、旧稿校正与可整合问题

作者明确将多图关联称为初步且不强的能力，展示四图关联失败与幻觉；多语言能理解不保证用对应语言回答；OCR、数字、复杂图文和文档应用仍失败。部分讨论例子不属于OwlEval且未评分，不能并入量化能力总数。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=11|§5]] [[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=12|§5续]]

旧TeX保留有用的abstractor结构线索，但需三项纠正：

1. 第二阶段LLaVA多模态指令写成50k，固定v3正文写150k；Wiki以该版本正文校正。[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=5|§4.1]]
2. 把SentencePiece称“文本编码器”应改为tokenizer；“ViT参数0.2B”未由本文单独参数表确认，不能用总7.2B减LLaMA名义7B就精确归给视觉骨干。
3. “已和最新2025 MLLM结构基本一致”是无边界的历史概括，当前页不采用。三模块表象不保证训练方式、token保留、跨注意力位置相同；正文新增了参数路线／超参数／r编号三组原文冲突，而不是静默沿用旧稿单一版本。

建议整合到视觉连接器、参数冻结与LoRA路线、开放式人评及能力标签边界；对应主题页建立后补双向链接。下一步若需实现级比较，须先锁定与v3相符的仓库commit，再核abstractor与LoRA配置；本轮不启动代码审计或训练。

## 实际整合关系

支撑abstractor输入接入与分阶段开放参数，OwlEval用作有范围的人工诊断；阶段2冲突保持未裁定。

- [[wiki/architecture/Visibility-and-Connections|可见性、路由与连接：视觉信息在哪里与语言相遇？]]。
- [[wiki/training/Supervision-and-Stages|监督与阶段：数据、目标、开放参数和预算如何一起改变？]]。
- [[wiki/evaluation/Judges-and-Task-Success|裁判与任务成功：答案、解释、生成物和终态怎样分别取证？]]。
- [[wiki/models/Family-Changes|家族变化轴：输入、接口、数据和计算怎样共同演进？]]。
