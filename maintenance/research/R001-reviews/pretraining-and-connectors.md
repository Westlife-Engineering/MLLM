# R001 独立学术审查：预训练与连接器（S011–S020）

审查日期：2026-10-31；角色 G，未参与本组首稿，不派发子代理。仅写本报告与任务临时目录，不修改来源页、Raw、registry、共享主题、索引、日志或 Git。沿用已读 AGENTS/workflows/lint、academic-researcher、pdf 的原件与证据边界；对 S020 的 OwlEval 另外使用 benchmark-paper-reading 技能。

本文按来源页先读、归档原文回查的顺序进行。来源作者的 handoff 只用于导航，不代替证据。全部页码从 PDF 首页起计；完整提取文本仅用于定位，不等于全文逐项审查。版本按 registry 登记，哈希重算与登记匹配；另回查十篇首页的标题、作者与 arXiv 版本行，未发现身份错配，不把哈希当作身份证明。暂存证据位于 `C:/Users/ZENGZX/AppData/Local/Temp/mllm-kb-20261031/review/pretraining-connectors/`。

> 正式状态：S011–S020 全部完成本报告所列独立学术审查，共 83 项实质主张；64 张论文原页及 S003 讲义 p.5 实际渲染查看。G-S003-1 与 G-BLIP2-1 已修订并回核关闭，剩余必须返工项：无。通过仅限下述实际范围，不代表代码、复现或应用渲染验收。

## 1. 原件身份与范围

| ID | 归档文件 | 版本 / 页数 | 实算 SHA-256 |
| --- | --- | --- | --- |
| S003 | `raw/lectures/VLM-2.pdf` | 2026-05-22 course slides / 92 | `a81bcec1ed8f630632c2abccbba88bf3ddeaaab95f47aaa5fdf68596233b1a64` |
| S011 | `raw/papers/architecture/pretraining/ALBEF.pdf` | v2 / 16 | `137c937c0834d8aa116bac93cae46cabe86cf7b7645f3b6339639b194273b229` |
| S012 | `raw/papers/architecture/pretraining/BLIP.pdf` | v2 / 12 | `63e0335cdd57c3d92b907b89c93d10befdd29b8aeed108091bbde90c121ed97a` |
| S013 | `raw/papers/architecture/pretraining/CoCa.pdf` | v2 / 19 | `ebb8ecad1667502a8e016241b499b2479e296d59c7df06abdedb5cb51d26457b` |
| S014 | `raw/papers/architecture/pretraining/VLMo.pdf` | v2 / 16 | `636d9dfd99492bdf57e2ec517f5587af7fcdc7dcb3470a6cddc68f53cdb2e5ee` |
| S015 | `raw/papers/architecture/pretraining/BEiT-v3.pdf` | v2 / 18 | `f02c366d9a3e02d744807fac11f5f89255aff2532108a0795d4ee2736c1376d4` |
| S016 | `raw/papers/architecture/connectors/Flamingo.pdf` | v2 / 54 | `27af622bf50987fd98a03451a27a670adfaeefd5218a3e990b37abc326ba63f0` |
| S017 | `raw/papers/architecture/connectors/BLIP-2.pdf` | v3 / 13 | `6bc5d399d6127a64ace5167a2f0c00112a49725d2475d80322dbf0083f139e80` |
| S018 | `raw/papers/architecture/connectors/InstructBLIP.pdf` | v2 / 17 | `31c03f3ee54016e6da875593ed9d98419899d4164af638dc8cca76a4871beb35` |
| S019 | `raw/papers/architecture/connectors/MiniGPT-4.pdf` | v2 / 15 | `a78f64448a86d91bd3c821178686cbe129312d53ee2b7eaf29ab412ce44c2ac0` |
| S020 | `raw/papers/architecture/connectors/mPLUG-Owl.pdf` | v3 / 21 | `997b330fb3b0b6e4972f7e98ae7753cfbadf81512d0d070eae654e3be2085ffd` |

S003 仅为指定专项：讲义 p.5 及 Wiki §1.1 的 ITM/MLM 信息组织，不重新声称读完 92 页讲义。

## 2. S011 ALBEF

对象：[[wiki/papers/architecture/pretraining/ALBEF]]。范围内通过。实际查看渲染页：p.3、4、6、7、9、13；另回读 p.5 训练与目标说明。未逐项核查所有主表、p.14–16 全部热图或代码；未独立验证全部互信息理论假设。

| 项 | 主张与判断 | 原件依据及边界 |
| --- | --- | --- |
| A1 | **支持：**“align before fuse”主要是独立表示与融合表示的分工，三个预训练目标联合优化，不是先完整训完 ITC 再训融合的两阶段。 | p.3 Fig.1、§3.1–3.2，p.4 Eq.5；12层 ViT、6层文本、6层多模态，后者每层 cross-attention 读视觉。 |
| A2 | **支持：**ITC 用归一化 256维投影、在线/动量表示与候选 softmax，本来就有正负配对标签。 | p.3 Eqs.1–2。现页分母、温度、两个方向平均正确；与 ITM 的差别是独立向量候选比较与融合后二分类，而非有无标签。 |
| A3 | **支持：**ITM 为每张图/每段文本按相似度分布抽负例，不固定 argmax；MLM 预测被选文本位置。 | p.4 §3.2、Eqs.3–5 及脚注：15% token选择，80/10/10替换规则。将“相似名义负例可能实际合理”标为机制限制合理。 |
| A4 | **支持：**MoD 用 EMA 教师给 ITC/MLM 软目标，按 α 混合原标签，而非全部替换；教师正确性无保证。 | p.4 Eq.6、p.5 Eq.7；m=0.995、queue=65536、第一epoch α从0到0.4。EMA教学式与参数说明相符，未把教师当外部真值。 |
| A5 | **支持：**固定教师时 KL(q∥p)=H(q,p)−H(q)，与软目标交叉熵对学生同梯度；原文局部反向记号不应照抄。 | p.6 Eq.11之前确写 KL(p,q)，但展开为−Σq log p，与p.4 Eq.6同向。已看原页确认非提取器问题。现页推导与混合目标解释正确。 |
| A6 | **支持：**4M/14M 是图像规模，基础4M约5.1M配对；30epochs、batch512、256²预训练、384²适配等是成绩条件。 | p.5 §3.4–3.5；8 A100不等于完整成本已知，页面未从设备数臆造耗时。 |
| A7 | **支持：**检索先ITC筛候选再ITM重排；Flickr“zero-shot”先用COCO微调；VQA实际限制3192候选，NLVR2有双图改造与额外TA训练。 | p.6 检索、p.7 Fig.3与正文、p.13 Appendix A。不同任务的输出/监督接口已正面解释。 |
| A8 | **支持：**逐步消融总体有效但非每列单调，TR/IR是三档recall均值；grounding有额外detector proposals及预训练图像重叠。 | p.7 Table1 ITC MoD使NLVR2 80.35→80.34；p.9 Tables5–7重排及定位；p.13明确承认RefCOCO+ val/test图像在预训练出现。不能称严格未见图像泛化。 |

旧稿纠错：已搜索冻结 ALBEF TeX 与动量蒸馏 Markdown 的相关段落，确认 argmax、ITC无显式正负、EMA保证正确方向等旧理解确有依据需要纠正；新 Markdown 原有部分合理澄清也被保留。代码片段未审计，报告不据此确认实现。教学评价：独立编码—融合—软监督三个作用能独立理解；数学解释服务于“为什么软分布能训练”，没有只堆限制。无必须返工。

## 3. S012 BLIP

对象：[[wiki/papers/architecture/pretraining/BLIP]]。范围内通过。实际查看渲染页：p.2、4、5、6、9、12；文字回读 p.3、7–8。未全面校勘每个模型/任务的所有分数与训练实现。

| 项 | 主张与判断 | 原件依据及边界 |
| --- | --- | --- |
| B1 | **支持：**MED有单模态encoder、图像条件encoder、图像条件decoder三种功能；理解双向SA、生成因果SA。 | p.2 Fig.2、p.3 §3.1。encoder/decoder除SA外共享参数，不能只描述成相同SA权重换mask。 |
| B2 | **支持：**ITC、ITM、LM分别约束全局对齐、融合匹配、条件生成；一次视觉前向、三次文本前向。 | p.3 §3.2，LM label smoothing=0.1。现页LM教学式明确省略smoothing而非冒充完整实现式；ITM采样不是argmax。 |
| B3 | **支持：**CapFilt从初始MED分别微调captioner/filter，生成文本后筛原文和合成文，再与人工配对合并训练新模型。 | p.4 Fig.3与§3.3。保留操作的集合式合理；同图可保留两条而非无条件替换。p.5城堡例子确保留原文、拒绝合成文。 |
| B4 | **支持：**nucleus p=0.9及filter拒绝率不是人工真实错误率；共享预训练参数与后续分离两模型不矛盾。 | p.5 Table2：25%对19%，COCO TR/IR 80.6/63.1对79.6/61.9；p.6 Table4共享/分离拒绝率8%/25%。confirmation bias归因保留为作者解释，不声称已消除全部相关偏差。 |
| B5 | **支持：**分离SA在具体消融中兼顾参数量与效果，非普遍架构定律。 | p.5 Table3：全共享224M、除SA外共享252M、完全独立361M；TR/IR和CIDEr数值与当前页一致。 |
| B6 | **支持：**重复原始文本到等样本数不能复制CapFilt收益，但这不匹配整个bootstrap成本；新模型也不是每指标都赢继续训练。 | p.9 Tables12–13：24.7M重复 vs CapFilt；继续训练CIDEr129.9高于新模型129.7。p.9多轮/多caption/集成仅未来方向。 |
| B7 | **支持：**14M/129M、LAION每epoch仅1/5、ViT-B/L和CapFilt-L概念不同，VQA分辨率为480²例外。 | p.4训练及脚注、p.6 Table5注、p.12 Appendix A/C；CapFilt-L指造数据模型大，不必最终骨干大。 |
| B8 | **支持：**Flickr零样本是COCO检索微调后转移，VQA以3128候选排序，视频迁移无时间建模。 | p.6 §5.1；p.12确印3128，不能私自统一为ALBEF的3192；p.8明确8/16帧及忽略时间信息。当前页不把候选式VQA、VisDial排序或帧拼接升级成开放通用能力。 |

旧稿纠错覆盖“不得已加入生成”、ITM再做embedding匹配、确定性最难负例、filter保证精准及ALBEF数据规模移植等；依据是原件功能、流程和表格，不是另一篇总结。教学评价：参数共享与数据流分开解释尤其有效，能够理解三个loss与CapFilt发生在不同计算层面。无必须返工。

## 4. S013 CoCa

对象：[[wiki/papers/architecture/pretraining/CoCa]]。范围内通过。实际查看渲染页：p.4、5、9、12、18；另回读p.6–8、11。未全面核验视频子集清单、全部下游成绩或代码。

| 项 | 主张与判断 | 原件依据及边界 |
| --- | --- | --- |
| C1 | **支持：**同一因果decoder前段不读图像、后段cross-attention；末尾CLS从前段取纯文本表示，其他位置传后段。 | p.4 Fig.2/Algorithm1、p.5方法。两段因果性允许复用一次计算图；teacher forcing训练并行不等于推理一次生成整句。 |
| C2 | **支持：**两个pooler输出1与256个token而非维度/第0位与余255位；正式模型默认cascade。 | p.5 pooler、p.12 Table8(f)与正文。p.4图/伪代码是parallel展示，正文明确所有CoCa默认cascade，页面已分清。 |
| C3 | **支持：**对比损失按原件为1/N的双向之和，配captioning，权重1:2，没有ITM二分类。 | p.4 Eqs.2–3、p.5 Eq.4、p.7训练。公式没有擅改为CLIP常见1/(2N)；温度0.07和加权目标正确。 |
| C4 | **支持：**JFT类名文本化与ALIGN alt-text联合训练，从头初始化；此“single-stage”不抹掉高分辨率继续预训练。 | p.6–7：每批各半、65536、500k、约5天/2048 TPUv4 chips，随后576²再1epoch。低增量成本不是低总成本。 |
| C5 | **支持：**shared计算不保证目标无梯度冲突；小规模消融支持双目标及6/6折中。 | p.11–12 Table8，实验为缩减12层decoder/batch4096；纯contrastive VQA另需融合。71.6/69.0、1.18×相对1.17×captioner与1×contrastive成立。 |
| C6 | **支持：**保留多个视觉token有利，但不能声称只有pooler能形成细粒度能力。 | p.12 Table8(f)：1query VQA64.4、32query68.2、默认256为69.0，去generative pooler也69.0。288/18本来256patch，非普遍强压缩。 |
| C7 | **支持：**ImageNet86.3、90.6、91.0分别是zero-shot、冻结encoder训练pooler/head、微调整体；90.6不是linear probe。 | p.9 Table4、p.7 Table2文字记录、p.8与p.18适配。正文encoder lr1e−4与附录5e−4差异真实，当前页保留，不伪造复现配置。 |
| C8 | **支持：**zero-shot检索全冻结独立表示，无多模态decoder重排；不同于ALBEF/BLIP的COCO适配后Flickr转移。 | p.9 Table3与正文：Flickr92.5/80.4、COCO66.3/51.2；video用可取得subset非完整测试集。p.18 VQA3129候选和任务head说明也支持页内适配区分。 |

旧稿中“未引用ALBEF”、query维度、0+255、ITM、互不干扰、因计算少所以能从头训练等已定位；当前机制与预算足以纠正。教学评价：很好地区分纯文本全局表示、条件token表示与pooler的不同接口。无必须返工。

## 5. S014 VLMo 与 S003 讲义专项

对象：[[wiki/papers/architecture/pretraining/VLMo]]。S014范围内通过。实际查看渲染页：p.3、4、5、10、16；文字回读p.6与相关训练段落。S003实际查看原件p.5并读Wiki§1.1。未重新审查讲义其它章节，也未审计VLMo的mask实现。

| 项 | 主张与判断 | 原件依据及边界 |
| --- | --- | --- |
| V1 | **支持：**融合输入拼接图文，从底层SA开始交互；低层V/L-FFN、顶层VL-FFN。 | p.3 Fig1、p.4 §3.1–3.2 Eqs.1–2、p.5 Fig3、p.16 Appendix A明确fuse at bottom layers。S014当前表述正确。 |
| V2 | **支持：**attention共享是同层跨模态/任务调用，不是所有深度参数绑定；FFN按输入模态和层位置选，不是学习型top-k router。 | p.4 Eqs.1–2、p.5 §3.2；前norm/残差公式正确。Base顶部2层、Large顶部3层见p.6，不能一概“后两层”。 |
| V3 | **支持：**独立双塔共享权重不等于token相互可见；block-diagonal mask只可作等价教学语义。 | p.3与p.5图示分别独立编码/联合编码；未给出足够实现证据证明ITC必拼接并打mask。现页准确标识教学补充。 |
| V4 | **支持：**ITC用独立CLS归一化点积、双向softmax，ITM融合分类，MLM15%/whole-word masking。 | p.5 Eqs.3–4、p.6训练。MLM mask不是causal mask；captioning是p.10未来方向而非本篇已验证接口。 |
| V5 | **支持：**global hard negatives是当次所有GPU batch，不是全训练库。 | p.10 Table6：32×32=1024候选，local32，NLVR2 test-P77.95→79.48。对ALBEF的实现比较仍为本文作者口径。 |
| V6 | **支持：**先用BEiT参数初始化attention/V-FFN，固定它们训练L-FFN，再全模型图文训练；不支持视觉attention天然更通用的强因果故事。 | p.4 Fig2、p.6 §3.4、p.16 Appendix B：Wikipedia/BookCorpus，Base500k/Large200k；4M配对训练规模未包含前序所有成本。 |
| V7 | **支持：**去VL专家、仅ITC、分离attention消融测试的是具体配置，不等于只有顶层才有交互。 | p.10 Table5：去VL80.11/完整80.31；ITC-only58.83；p.16 Table7共享80.31对分离78.95。NLVR2平均3次未附方差，不能从小差异推普适定律。 |
| V8 | **支持：**纯双塔检索无ITM重排，下游/消融分辨率和训练长度不同；缓存编码不消灭全对全NM打分。 | p.6 §3.5与p.16 Appendix D。主表Flickr由COCO初始化再微调，非Flickr零样本；当前页成本解释合理。 |

旧稿的BPE、跨层共享、必用block mask、自动最优router及2D注意力天然更通用等已搜索定位；原件WordPiece、路由规则和stagewise事实支持纠正。教学评价：区分“参数共享”“token可见性”“FFN选择”三个问题，解释可以独立成立。

**必须修订 G-S003-1（已提交主协调者）：**讲义页§1.1表中ITM“先处理各模态，再在融合层交互”、MLM“在融合层交互”易暗示只在顶层交互。讲义p.5与S014原图一致，底层SA已联合读取。建议分别改为“图文拼接后从底层self-attention交互，低层分模态FFN、顶层VL-FFN”和“遮蔽部分文本，联合图文从底层attention交互以预测被遮蔽词”。原D已定向修订；G回核最终两行及就近的讲义p.5／S014 p.4–5、p.16“原论文补核”依据，与上述原件一致，**已关闭**。此问题不要求机械改写按任务接口组织的architecture/foundations主题。

## 6. S015 BEiT-v3

对象：[[wiki/papers/architecture/pretraining/BEiT-v3]]。范围内通过。实际查看渲染页：p.3、4、5、6、7、16、17、18。未完整复核纯视觉主表排名、全部检测/分割组件和代码实现。

| 项 | 主张与判断 | 原件依据及边界 |
| --- | --- | --- |
| E1 | **支持：**Multiway共享SA并按模态/层段用FFN；40层、顶部3层VL-FFN，融合底层已交互。 | p.3 Fig2、p.4 Fig3、p.5 Table2；五种任务接口不是任意重排已训练层。 |
| E2 | **支持：**1.9B总参数与纯视觉约1B激活参数不同，不是视觉/文本简单各一半。 | p.5 Table2与正文692M/692M/52M/317M，另有其它参数，模块四舍五入数不能硬求和成总值。 |
| E3 | **支持：**主预训练统一mask-then-predict，文本token与离散视觉token是不同目标空间；视觉输入仍为patch embeddings。 | p.4 §2.2：BEiTv2 tokenizer提供视觉重建目标，不是RGB回归；文本15%、配对文本50%、图像40% blockmask。教学MDM交叉熵式明确非原文编号公式。 |
| E4 | **支持：**无批内负例依赖不等于任意batch不影响性能；数据和预算是独立约束。 | p.5：每步2048图+2048文+2048图文，1M步、224/14、15M图/21M配对及160GB文本。缺完整设备/时长不能推总算力低。 |
| E5 | **支持：**这里BEiT initialization是随机初始化后按1/√(2l)缩放输出矩阵，不是加载预训练BEiT权重。 | p.5脚注4原页明确，区别于VLMo的stagewise初始化；p.16 Table11 dropout关闭、drop path0.1等一致。 |
| E6 | **支持：**captioning非对称mask防止未来caption经视觉分支泄漏；VQA是3129类而非自由答案生成。 | p.6 §3.1：图像只互看，caption看图/左文/自身；p.17 Tables12–13，VQA756²、caption392²、mask0.6/beam3，与页内条件一致。 |
| E7 | **支持：**检索主表额外有5epochs/batch16k对比中间训练，未中间训练的对照也已做下游ITC。 | p.7正文、p.16 Table10/Appendix A：COCO R@1 82.7/65.1→84.8/67.2；Flickr97.5/89.1→98.0/90.3。不能把左列称“从未对比训练”；zero-shot也基于中间适配。 |
| E8 | **支持：**不同任务成绩含额外监督/heads/分辨率，不能称未经适配裸模型全能；caption各指标也非全领先。 | p.6 Table4 METEOR32.4低于CoCa33.9；p.18训练条件显示Objects365→COCO、分割80k、ImageNet21k50epochs→1k15epochs。当前页保存这些条件。 |

旧稿“不需要MLM”、参数各半、离散token即全部输入、batch任意调整无影响等已搜索定位并得到纠正。教学评价：以统一目标形式和不同可见性/输出接口解释“统一”，并明确主预训练与适配边界。无必须返工。

## 7. S016 Flamingo

对象：[[wiki/papers/architecture/connectors/Flamingo]]。范围内通过。实际查看渲染页：p.4、5、7、8、23、24、35；另回读p.6、26–29、33的协议、数据与适配。未审查54页全部案例、全部分类表格及社会影响讨论，未审计去重代码。

| 项 | 主张与判断 | 原件依据及边界 |
| --- | --- | --- |
| F1 | **支持：**冻结NFNet-F6与语言骨干，训练resampler及插入的视觉交互层；视觉token不是直接替换词向量。 | p.4–5 Figs.3–4、p.23 Fig.5。64个latent queries读取视觉特征与latents拼接的K/V；视频加时间位置编码，未显式加空间位置编码。现页教学注意力式与图一致。 |
| F2 | **支持：**gated cross-attention和额外FFW各有零初始化tanh门，新模块插在原LM block之前，起点保留原LM函数。 | p.5 Fig.4、p.23 §A.1.2；两门不是单一全模型标量。门绝对值不能直接当视觉语义融合强弱，激活尺度会变化。 |
| F3 | **支持：**通常文本cross-attention只看最近的先前图像，但仍可经LM self-attention间接访问更早信息。 | p.6与p.24 Fig.7。M3W训练随机选previous/next图像的页面级增强是明确例外，不应把“只看前图”绝对化。 |
| F4 | **支持：**3B/9B/80B含新增参数，骨干分别约1.4B/7.1B/70B；插入频率不同。 | p.28 Table5、p.29：每1/4/7层插入，从首层开始；视觉435M、resampler约194M另列。p.29新增参数口径含resampler，与表中Xattn单列并非实质冲突。 |
| F5 | **支持：**交错网页、图文对、视频数据通过加权文本似然训练；大数据与预算不能由“冻结”省略。 | p.27–29：M3W43M网页、ALIGN1.8B、LTIP312M、VTP27M；权重1/0.2/0.2/0.03，50万步、1536 TPUv4、约15天。320输入、训练8帧1FPS，推理可30帧3FPS。 |
| F6 | **支持：**zero-shot与few-shot必须保留prompt协议、DEV/held-out和任务输出区别。 | p.7 Table1、p.26：开放生成zero-shot仍用两个纯文本示范，封闭分类不必；5个DEV任务与11个held-out分开。80B的0/4/32-shot OKVQA50.6/57.4/57.8、VQAv2 56.3/63.1/67.6等核对正确。p.7图注seven与正文six冲突确实存在。 |
| F7 | **支持：**消融支持所试模块与单图mask在具体预算下的优势，不是数学必要性。 | p.8 Table3、p.35 Table10；3B、5个DEV、4shot、缩短预算，归一化平均70.7、去M3W53.4、去门66.5、MLP66.6；看所有先前图63.5低于只看最近图70.7。替代模块并非无能力。 |
| F8 | **支持：**预训练冻结不覆盖所有下游；去重也不是所有数据全覆盖。 | p.33 §B.2.2解冻视觉并升480²，LM仍冻；p.28 §A.3.4：M3W事后找到125个exact duplicates、VTP未去重、配对数据仅指定集合。当前页保留了有限泛化和重叠边界。 |

旧TeX“层深增加则视觉语义融合加大”已定位，其门值解释需要收回；当前页同时保留零门初始化的合理旧解释，并将模块“必须”改为条件化消融优势。教学评价：压缩视觉序列、在LM内部注入、控制跨图可见性三个步骤清楚。无必须返工。

## 8. S017 BLIP-2

对象：[[wiki/papers/architecture/connectors/BLIP-2]]。经定向修订后范围内通过。实际查看渲染页：p.3、4、6、7、8、12、13；另回读p.5训练段落。未审计实现、全部prompt变体及所有附录失败图文字。

| 项 | 主张与判断 | 原件依据及边界 |
| --- | --- | --- |
| Q1 | **支持：**Q-Former以32×768 learned queries读取冻结视觉特征，文本分支共享self-attention；188M是预训练模块参数量。 | p.3 Fig.2、§3.1，BERT初始化、隔层cross-attention。query是可学习输入与条件化输出的两个阶段，非同一个已编码视觉向量。 |
| Q2 | **支持：**ITC/ITM/ITG三种mask分别服务独立对齐、融合匹配、条件生成。 | p.3 Fig.2：ITC禁止query/text互看且用query相似度最大值；ITM双向交互并平均query logits；ITG的queries不读文本，文本读queries与过去文本。不能把ITG改成MLM。 |
| Q3 | **支持：**第二阶段线性FC映射为LLM soft prefix，OPT用因果LM，FlanT5用prefix/suffix的encoder-decoder目标。 | p.4 Fig.3、§3.3。不是统一指定的多层MLP，也不是所有LLM统一输出维度；两主干在预训练冻结。 |
| Q4 | **支持：**数据清洗、视觉层选择与两阶段预算影响结果。 | p.4–5：129M配对；BLIP-L生成10条加原文，CLIP-L排序选top2随机采样；CLIP-L/EVA-g取倒数第二层，224²；250k/80k steps，batch因骨干与阶段不同，16 A100 40GB。未把已有主干预训练成本计为零。 |
| Q5 | **支持：**zero-shot VQA提升不在所有任务成立，188M与生成路径103–108M不能混作不同协议的统一成本。 | p.6 Table1：FlanT5-XXL VQAv2 65.0相对Flamingo56.3为8.7个百分点，OKVQA45.9低于50.6。该表不证明所有任务或完整系统成本都优。 |
| Q6 | **支持（修订后）：**下游caption/VQA微调视觉编码器与Q-Former，LLM保持冻结；VQA让问题条件化Q-Former。 | p.7 §4.2–4.3、p.8 §4.4、p.13 Fig.7。但Fig.7视觉编码器仍有雪花，不能称“解冻标记”。现页明确图文冲突，以正文登记可训练范围、以图确认问题路径。 |
| Q7 | **支持：**检索仅使用第一阶段模型、不需LLM；top128用ITM重排，Flickr是COCO适配后转移。 | p.8 Table4/§4.4，COCO ITG消融84.5/67.2→85.4/68.3；Flickr97.6/89.7。p.12：caption/retrieval364²，VQA490²，不能当全程224²裸模型成绩。 |
| Q8 | **支持：**未观察到VQA in-context收益是特定实验结论，单图对数据不足跨样例联系是作者解释；局限图号须按实际定位。 | p.8 §5、p.12 Fig.6；正文误指Fig.7可由实际图内容消解。当前页未将作者归因升级成排除了其它变量的因果结论。 |

**必须修订 G-BLIP2-1，已关闭：**审查发现读取记录称核对“视觉编码器解冻标记”，而p.13实际是冻结雪花。主协调者定向将记录改为“冻结标记及正文微调范围”，旧稿纠错段补明上述原件冲突；G重读最终两处，准确。旧TeX“图像编码器始终冻结”“Q-Former后MLP”亦已定位，修订后没有反向把正文明确的下游解冻否定掉。教学评价：三个mask与两阶段目标解释自洽，图文不一致得到局部处理。

## 9. S018 InstructBLIP

对象：[[wiki/papers/architecture/connectors/InstructBLIP]]。范围内通过。实际查看渲染页：p.4、5、6、7、8、9、17；文字回读p.3、13、15–16。附录案例只核作者比较来源/结论边界，未逐像素判定全部回答真实性。

| 项 | 主张与判断 | 原件依据及边界 |
| --- | --- | --- |
| I1 | **支持：**instruction同时进入Q-Former与LLM，前者通过SA影响queries读取视觉特征，输出经FC成为LLM视觉提示。 | p.4–5 §2.3/Fig.3；视觉和LLM冻结。原件以K表示query数，当前页将32追溯至BLIP-2而非冒称本文独立报告或代码核实。 |
| I2 | **支持：**26个数据集/任务实例、13 held-in与13 held-out、11任务类是作者组织口径，不等于26个完全独立图像来源。 | p.4 Fig.2：VQG复用VQA来源、LLaVA拆三类；四类任务全held-out。p.16列具体split；当前页未把仅本轮未见等同所有主干预训练都未见。 |
| I3 | **支持：**模板令任务与短答要求条件化；外部OCR tokens属于评测输入。 | p.3 §2.1、p.17 Tables5/§E：非所有问题必须短答，LLaVA已有指令不重加模板；TextVQA不能称只依赖224²视觉编码读字。 |
| I4 | **支持：**平方根数据集采样式正确，且额外手调A-OKVQA/OKVQA权重；训练时长只属指令阶段。 | p.5 §2.4；p.6 §2.6最多60k步、每3k验证，单个选定checkpoint用于全部数据集；16 A100 40GB/1.5天，不包括Vicuna版本另行BLIP-2式预训练。 |
| I5 | **支持：**候选log-likelihood排序、开放生成和视频4帧拼接是不同接口。 | p.5–6 §2.5：ScienceQA等指定任务候选排序；视频逐帧独立视觉/Q-Former、未用时序数据训练，不能外推为连续跟踪能力。 |
| I6 | **支持：**表1的指标/变体条件保留准确，不能把家族最佳概括成每变体全胜。 | p.6 Table1：XL NoCaps104.5→119.9、ScienceQA54.9→70.4、iVQA40.4→53.1；XXL VSR68.2→65.6是反例。CIDEr/AUC/MRR和accuracy不等价。 |
| I7 | **支持：**指令感知与采样消融支持具体机制作用，平均的任务组成须分清。 | p.7 Table2：去指令感知XL ScienceQA70.4→63.4、VizWiz32.7→25.1；去balanced Vicuna IconQA43.1→43.5例外。Table2 held-in只4项，Fig.4全部held-in；Fig.4 held-out是8项，52.9对45.5–46.8。 |
| I8 | **支持：**ScienceQA90.7是额外下游微调，而非zero-shot70.6；定性GPT-4比较非总体胜率。 | p.8–9 §3.5/Table3仍冻视觉、224²；p.13/15 Figs.5/7比较答案来自论文或demo，未给受控总体评估。当前页正确收回“优于GPT-4”“确保不漏细节”等强结论。 |

旧TeX中ITC/MLM/ITM误列、输入query_embeds与输出混淆及总体能力推断已按原件纠正；原有“指令进入Q-Former”与13/13划分基本理解被保留。教学评价：解释了指令影响视觉读取的具体路径，而非只用“instruction-aware”名称替代机制。无必须返工。

## 10. S019 MiniGPT-4

对象：[[wiki/papers/architecture/connectors/MiniGPT-4]]。范围内通过。实际查看渲染页：p.2、6、7、8、14、15；文字回读p.4–5、9。未审计代码、全部定性案例或人评原始记录；没扩读CHAIR原始论文。

| 项 | 主张与判断 | 原件依据及边界 |
| --- | --- | --- |
| M1 | **支持：**主方案复用EVA-CLIP ViT-G/14与BLIP-2 Q-Former，连接至冻结Vicuna，只训练单线性映射。 | p.2 Fig.1及正文、p.4 §3.1；指令直接给LLM，不能混成InstructBLIP的指令感知Q-Former。768→4096不应被当成ViT到任意LLM的固定关系。 |
| M2 | **支持：**第一阶段约5M是本次20k×256训练配对规模，第二阶段小数据不是从零获得全部能力。 | p.4–5：CC/SBU/LAION，4 A100 80GB约10小时；3500条、400steps/batch12、单A100约7分钟。未计入已有BLIP-2与LLM预训练全部预算。 |
| M3 | **支持：**3500条精炼数据有明确生成—修文—人工流程，ChatGPT不直接看图标注。 | p.4–5 §3.2–3.3：5000 CC图、阶段1模型描述、不足80tokens续写、ChatGPT修文、规则与人工筛改；对话prompt不计loss。语言修文与视觉事实保证不能等同。 |
| M4 | **支持：**四类请求人工评估的65/100仅为作者所选小集满足请求率。 | p.6 Table1：梗图8/25、食谱18/25、广告19/25、诗20/25，对照0/4/1/0；未充分报告人评人数、盲法、一致性，不是全任务视觉正确率或普遍人类偏好。 |
| M5 | **支持：**COCO3310/5000对1376/5000是单参考caption的文本覆盖判定，不能当完整幻觉测量。 | p.7 Table2、p.15 Appendix A.3：每图随机选一条参考，ChatGPT只读两段文本yes/no，未看图且不检查全部额外断言；长输出覆盖更多与幻觉更多可同时发生。 |
| M6 | **支持：**阶段2降低特定生成失败，但2%/1%不是“全部小于2例”，也不证明全部事实正确。 | p.7 Table3与p.8 §4.3确有措辞小冲突；100张COCO test、长描述35→2、诗32→1，现页准确保留表值及失败定义不足。 |
| M7 | **支持：**Q-Former/映射深度消融限于两任务与有限数据，不足建立模块普遍必要或无用。 | p.8 Table4、p.9 §4.4：58.2/32.2；去Q56.9/33.4；3层49.7/31.0；训练Q52.1/28.0。三层linear未详述激活，不可擅自指定MLP实现。 |
| M8 | **支持：**原模型传统VQA落后，另一个LoRA变体也增加VQA监督，收益不能只归参数更新。 | p.14 Appendix A.2/Table6：BLIP-2 80.2/42.4，原Mini58.2/32.2，LoRA67.2/43.5；正文增加VQAv2、OKVQA、A-OKVQA，表中5M简写不抹去额外训练。 |
| M9 | **支持：**CHAIR对象幻觉、空间错误和语言流畅性是不同维度；图示能力不等于执行验收。 | p.8 Table5/Fig.6、p.9：CHAIRi1.3/7.2/9.6对应6.5/28.8/175词，short<20提示未严格遵守；不存在的桌布、错误窗户位置可见。p.7网页与p.14食谱/植物例只属示范，非网站功能或领域正确率验证。 |

旧TeX的维度混同、GPT-4“没有的能力”、与LLaVA猜测比较、“质量>数量”的普遍结论均应按现页收窄；最后一项确未控制数据格式、规模、模型与预算。教学评价：轻量桥接为什么能借已有能力、为什么还需第二阶段，以及流畅/覆盖/事实正确三者关系解释充分。无必须返工。

## 11. S020 mPLUG-Owl 与 OwlEval

对象：[[wiki/papers/architecture/connectors/mPLUG-Owl]]。范围内通过。实际查看渲染页：p.1、4、6、7、8、9、18；文字回读p.2–5、11–12。按benchmark-paper-reading审查测量、样本、判分和比较条件；未扩读Self-Instruct或其它引文，未审计benchmark代码、原始逐题标签/回答或全部附录案例。

| 项 | 主张与判断 | 原件依据及边界 |
| --- | --- | --- |
| O1 | **支持：**固定v3用CLIP初始化ViT-L/14与原始LLaMA-7B，abstractor压缩后在LLM输入端拼接。 | p.4 Fig.2、p.5 §4.1；24层hidden1024、patch14，learned queries也进入拼接K/V支路。相似resampler结构不代表Flamingo的LM内部gated注入；7.2B总量非可训练量。 |
| O2 | **支持：**stage1训练视觉与abstractor、冻LLM一致；stage2 abstractor冻结状态的原件矛盾真实。 | p.1摘要/p.2引言明确abstractor与LoRA共同训练，p.4 Fig.2画雪花、§3.2写freeze entire model后加LoRA。不是提取器错误，现页并列未冒称代码已裁决。 |
| O3 | **支持：**条件文本LM目标、两类指令混合、数据量与超参数差异登记正确。 | p.5与p.18：stage1 50k/224²、104B tokens；stage2 Alpaca102k/Vicuna90k/Baize50k/LLaVA150k，2k/batch256。lr1e−4 vs2e−4、wd0.1 vs0.01、warmup2000 vs375真冲突；2.1M tokens与4096×512可以兼容。 |
| O4 | **支持：**OwlEval测作者选图上的开放视觉指令响应与人工能力标签，不直接测真实工作完成。 | p.6 §4.2：50图82题，21/13/9/3/4来自MiniGPT-4/MM-REACT/BLIP-2/GPT-4/作者；非随机真实用户流量。p.9 Fig.6展示人物与物体指代的多轮回答，未要求操作环境或验证外部结果。 |
| O5 | **支持：**A–D是人工有序等级，66个A+B不是66个完全正确，不能由无D宣称无失败。 | p.6 Fig.3：mOwl51/15/16/0，Mini46/8/26/2，各总82。原件只引用Self-Instruct评级法，未完整展开rubric；现页不编造A–D定义。 |
| O6 | **支持：**六能力标签是人工判定标准，与总体等级分开；IU不要求答案正确。 | p.7 §4.3/p.8 Table1：VU/OCR超过60%信息，KTA/MDA超过80%标准，RA可接受正确最终答无显式过程或大体正确过程。未给充分评分人数、盲法、一致性与不确定性；人工不自动等于有效可靠性校准。 |
| O7 | **支持：**单轮50和多轮52重叠，标签列也不是同一82题分母；MM-REACT筛除失败改变比较集合。 | p.6–7 Fig.4：50首问及52多轮问题，不是102独立题；p.18 Fig.15全题栏实际68个有效回答。当前页明确条件而未把筛选后的表现称无条件成功率。 |
| O8 | **支持：**完整训练配方优于所试消融，但不能单独归因可训练视觉；r3/r4确有编号冲突。 | p.8 Table2的r3勾预训练+纯文、r4预训练+图文，p.7及p.9 Table3却称r4为无多模态；r5六列100/95.2/56.7/87.5/80/95正确。表格勾选已实际看原页，非抽取错位。 |
| O9 | **支持：**纯文本86.07→86.71是ChatGPT评分比，既非能力百分比，也未建立显著提升。 | p.9 Table3：80题，587/682与600/692，参照回答评分分母也改变；p.7脚注以ChatGPT代GPT-4评分。未给重复judge变异、人评校准或误差条。 |
| O10 | **支持：**baseline实现与定性探索范围限制比较；没有全配置通用领先证据。 | p.5–6本地OpenFlamingo/BLIP-2代码与其它demo混合，版本/采样预算未齐；p.11–12承认多图初步、OCR数值/文档失败，部分未评分例子不在OwlEval。不能把OpenFlamingo当原Flamingo权重或把例子并入样本量。 |

旧TeX确有LLaVA50k、SentencePiece“文本编码器”、与“2025最新结构一致”等表述；当前页按固定v3校正，并保留abstractor信息流的合理部分。教学评价：先解释模块和两阶段目的，再解释OwlEval如何从问题得到回答、等级与能力标签，读者能够理解其测量价值；限制紧接实际操作与分数，没有只堆免责声明。无必须返工。

## 12. 正式结论与交付边界

- **学术审查：**十篇各8项以上，共83项实质主张（前五篇各8，Flamingo/BLIP-2/InstructBLIP各8，MiniGPT-4为9，mPLUG-Owl为10）。全部已按所列原件范围评判；当前范围内通过。表中“支持”指支持来源页保留条件后的主张，不认可被其纠正的旧断言。
- **两项必须修订已闭环：**G-S003-1底层attention信息交互，原D修订后G回核；G-BLIP2-1图7冻结标记/正文微调范围，主协调者修订后G回核。剩余必须返工：**无**。原件内部未能消解的配置冲突作为知识边界保留，不虚构复现配置。
- **可选改善：**后续若用户要做实现级对比，可锁定S020对应v3的代码commit核abstractor/LoRA配置和评分细则；这不是本轮通过的前置条件，也不建议靠扩读引文填满本轮。共享主题宜保留冻结发生的阶段、视觉信息注入位置、适配/零样本口径、开放生成/候选排序/人工评测的区别，具体整合由E与主协调者负责。
- **视觉核验：**64张论文原页加讲义p.5，共65张实际渲染查看；本报告逐篇列出页码。额外提取文本用于定位/查协议，不冒称渲染全篇。原件图表公式核查不等于Wiki在Obsidian显示已测。
- **结构与应用：**仅核本报告引用对象、各篇证据定位和本次返工；不替代H的全库路径/状态/索引检查或F的公式/图示渲染检查。不运行模型、训练、benchmark或仓库代码，不做Git操作，不声称复现或独立重算作者结果。全部论文的未覆盖范围保留于各节。

报告及临时证据已完成并释放，待主协调者最终验收。
