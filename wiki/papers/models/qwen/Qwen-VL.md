---
type: paper
source_id: S026
primary_direction: models/qwen
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/models/qwen/Qwen-VL.pdf]]"
reading_status: read
ingest_status: integrating
---

# Qwen-VL：固定视觉接口、细粒度监督与三阶段训练

## 问题与核心认识

Qwen-VL 希望给已有 Qwen 语言模型加入图像理解、文字读取和区域定位能力，同时保留中英文对话。关键不只是加一个视觉编码器：它用位置感知 cross-attention 将图像压成固定 256 个视觉 token，以统一文本格式表达问题、答案和坐标，再分阶段改变训练数据、分辨率与可训练模块。最终 **Qwen-VL 是第二阶段模型，Qwen-VL-Chat 是第三阶段指令微调模型**，二者在传统任务上并非全面单调提升。[[raw/papers/models/qwen/Qwen-VL.pdf#page=3|p.3–6 · §2–4 / Fig.3]]

## 来源与实际阅读范围

| 项目 | 记录 |
| --- | --- |
| 标题 | Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond |
| 作者 / 机构 | Jinze Bai、Shuai Bai、Shusheng Yang（共同贡献）、Shijie Wang、Sinan Tan、Peng Wang、Junyang Lin、Chang Zhou、Jingren Zhou；Alibaba Group |
| 版本 / URL | arXiv:2308.12966v3，2023-10-13；[固定版本](https://arxiv.org/pdf/2308.12966v3) |
| 原件 / SHA-256 | [[raw/papers/models/qwen/Qwen-VL.pdf\|24 页 PDF]]；b4eca60ae9d3c1548242da02ece0e2f35ce23d3a983255830d98212aa92e3167 |
| 阅读 | 2026-10-31；正文 p.1–10、附录 A–E p.16–24 已读；参考文献 p.10–15 仅导航，未逐篇核读 |
| 原页核看 | p.4–9、19–23：架构与冻结状态、数据及主结果、带颜色的监督格式、超参数、查询数/窗口消融、文本对照 |
| 旧笔记 | [[raw/notes/MLLM实例/Qwen/Qwen-VL总结.tex\|旧 TeX]] 正文已读；[[raw/notes/MLLM实例/Qwen/Latex_out/Qwen-VL总结.pdf\|旧编译 PDF]] p.1、4 核看；二者是二手输入 |
| 边界 | 未审计代码、运行模型或复现；未独立核验外部 benchmark 的完整协议；Obsidian 内显示未测 |

## 1. 从图像到语言模型：压缩长度与空间信息

视觉编码器来自 OpenCLIP ViT-bigG，图像按指定分辨率 resize，以 stride 14 分 patch。语言骨干来自 Qwen-7B；Table 1 的实际参数分项为视觉 1.9B、adapter 0.08B、LLM 7.7B、总计约 9.6B，所以“7B 模型”常指语言骨干而非完整系统参数。附录进一步说明使用的是 Qwen-7B **中间 checkpoint**，不是最终发布 checkpoint。[[raw/papers/models/qwen/Qwen-VL.pdf#page=3|p.3–4 · §2.1 / Table 1]] [[raw/papers/models/qwen/Qwen-VL.pdf#page=23|p.23 · Appendix E.4]]

Position-aware Vision-Language Adapter 是随机初始化的单层 cross-attention，256 个可训练 query 从视觉特征读取信息；query/key 中加入二维绝对位置编码，以减轻压缩造成的空间细节损失。它产生固定长度视觉表示，再送入 LLM，图像序列两端以 &lt;img&gt; 和 &lt;/img&gt; 标记。这里的 query 是学习参数，不是用户问题本身；也不能凭“二维绝对位置编码”补写本篇未给出的完整实现公式或可训练性。[[raw/papers/models/qwen/Qwen-VL.pdf#page=3|p.3–4 · §2.1–2.2]]

输入分辨率改变的是压缩前视觉序列：$224/14=16$，产生 256 patches；$448/14=32$，产生 1,024 patches。两种设置输出均为 256 个视觉 token。因此第二阶段提高分辨率，使 adapter 可读取更细的输入，但不增加每图送入 LLM 的特征数；这也留下固定瓶颈可能遗漏小字或局部细节的问题，本文没有证明该压缩是无损的。[[raw/papers/models/qwen/Qwen-VL.pdf#page=20|p.20 · Table 8]] [[raw/papers/models/qwen/Qwen-VL.pdf#page=22|p.22 · Appendix E.2]]

### 查询数与全局注意力的证据

查询数消融比较 64、144、256、400，但用的是 **ViT-L/14、224 输入**，不是最终 bigG/448 的完整下游控制实验。Fig.7 比较初始与 1k–5k steps 的训练 loss，作者结合第二阶段 1,024 个视觉 patches 的信息保留考虑选择 256。它支持这个工程折中，不能解释成“256 已被所有下游指标证明最优”。[[raw/papers/models/qwen/Qwen-VL.pdf#page=21|p.21–22 · Appendix E.2 / Fig.7]]

高分辨率 ViT 的另一个选择是 window attention：大多数层局部处理、少量层全局处理。448 输入时全局/窗口约 10/9 秒每步，896 时约 60/25 秒；窗口能明显减少 896 的时间，但其 loss 曲线与预算仍使作者最终采用 448 全局 attention。896 窗口达到与 448 设置相近 loss 需要约 2.5 倍时间，不能把这个结论推广为窗口注意力在所有架构和训练条件下无效；表格也没有给足硬件条件来推导通用吞吐。[[raw/papers/models/qwen/Qwen-VL.pdf#page=22|p.22–23 · Appendix E.3 / Table 10 / Fig.8]]

## 2. 让定位和 OCR 进入文本接口

区域边界框先归一化到 $[0,1000)$，写为左上、右下角坐标字符串，用普通文本 tokenizer 处理，不增设一整套坐标词表；&lt;box&gt; 标记框，&lt;ref&gt; 标记所指表达。**定位能力来自带区域监督的数据与生成格式，不是模型看到这些特殊符号就自动学会空间关系。**[[raw/papers/models/qwen/Qwen-VL.pdf#page=4|p.4 · §2.2]]

附录的三个方向清楚展示监督差别：referring grounding 给图像和短语，预测框；grounded captioning 给图像和框，预测描述；caption with grounding 同时生成描述与所指区域。OCR with grounding 则输出文字及 quadrilateral，使用 &lt;quad&gt;，不能把所有 OCR 位置都当作矩形的两个角。原页黑字是无 loss 的条件输入，蓝字才是监督目标；这比笼统说“所有 token 都做 next-token loss”更准确。[[raw/papers/models/qwen/Qwen-VL.pdf#page=19|p.19 · Appendix B.1 / 数据格式]]

OCR 数据包括 SynthDoG 中英文合成文本，以及 PDF/HTML 页面渲染和文字位置提取。合成背景来自 COCO train2017/unlabeled2017，使用 41 种英文字体与 11 种中文字体；PDF 使用 PyMuPDF 提取文本/框并渲染，HTML 使用 Puppeteer。此流程提供文字与位置监督，但不等于真实场景所有文档类型都有同样可靠标注。[[raw/papers/models/qwen/Qwen-VL.pdf#page=16|p.16–18 · Appendix A.4]]

## 3. 三阶段分别学什么、更新什么

| 阶段 | 开放参数 | 输入与预算 | 学习内容 |
| --- | --- | --- | --- |
| Stage 1 pre-training | ViT 与 adapter；LLM 冻结 | $224^2$；LLM length 512；50k steps；global batch 30,720；peak LR $2\times10^{-4}$ | 大规模图文对，文本交叉熵对齐 |
| Stage 2 multi-task | 全模型 | $448^2$；length 2,048；19k steps；batch 4,096；peak LR $5\times10^{-5}$ | caption、VQA、grounding、ref grounding、grounded caption、OCR、纯文本自回归 |
| Stage 3 SFT | adapter 与 LLM；ViT 冻结 | $448^2$；length 2,048；8k steps；batch 128；peak LR $10^{-5}$ | 多轮/多图/定位对话与纯文本对话，得到 Qwen-VL-Chat |

[[raw/papers/models/qwen/Qwen-VL.pdf#page=4|p.4 · Fig.3]] [[raw/papers/models/qwen/Qwen-VL.pdf#page=5|p.5–6 · §3]] [[raw/papers/models/qwen/Qwen-VL.pdf#page=20|p.20 · Table 8]]

Stage 1 原始约 5B 图文对，经宽高比、尺寸、CLIP 分数、语言字符及文本模式清洗后约 1.4B，英文/中文文本比例为 77.3%/22.7%；包括公开与内部数据。实际训练消耗约 1.5B 样本、500B image-text tokens。数据池规模、训练样本暴露数、token 数是不同口径，不能都写成“训练集有 500B 文本”。[[raw/papers/models/qwen/Qwen-VL.pdf#page=5|p.5 · Table 2]] [[raw/papers/models/qwen/Qwen-VL.pdf#page=16|p.16 · Appendix A.1]] [[raw/papers/models/qwen/Qwen-VL.pdf#page=20|p.20 · Appendix C]]

Stage 2 加入细粒度任务数据：Table 3 列 caption 19.7M、VQA 3.6M、grounding 3.5M、双向区域任务各 8.7M、OCR 24.8M、纯文本 7.8M。作者将同任务样本 pack 成长度 2,048 的交错序列。相同图像可能承担多个监督任务，不能把各行直接相加当作独立去重图像数；captioning 仍来自相近源，但不包含 LAION-COCO。[[raw/papers/models/qwen/Qwen-VL.pdf#page=5|p.5–6 · §3.2 / Table 3]]

Stage 3 的 350k 指令数据结合人工标注、模型生成与策略串联，补入定位和多图理解。ChatML 格式仅监督答案与相应特殊符号，不监督角色名和问题提示；多图在输入前标记 Picture id。正文中的示范第二轮问天气却回答标志形状，宜视为格式示例中的不匹配内容，不能用它证明对话正确性。[[raw/papers/models/qwen/Qwen-VL.pdf#page=6|p.6 · §3.3]] [[raw/papers/models/qwen/Qwen-VL.pdf#page=19|p.19 · Appendix B.2]]

可用下面的教学记号概括文本目标，而不冒充论文编号公式：

$$
\mathcal L=-\sum_{t\in\mathcal T_{\mathrm{supervised}}}
\log p_\theta(y_t\mid y_{<t},\,\text{visual tokens},\,\text{prompt}).
$$

重点在监督位置集合随任务格式改变，三个阶段还改变可更新参数。论文报告 bfloat16、AdamW 与 optimizer sharding；本次没有训练代码或设备实测，不能从配置表反推完整训练成本。[[raw/papers/models/qwen/Qwen-VL.pdf#page=19|p.19–20 · Appendices B–C]]

## 4. 结果怎样支持细粒度理解，怎样限制“全面提升”

### 通用任务与文字任务不是一种判分

Captioning 用 greedy decoding 与指定英文提示；Flickr30k Karpathy-test 的 zero-shot CIDEr 为 Qwen-VL 85.8、Chat 81.0。VQAv2 test-dev 为 79.5/78.2；DocVQA test 的 ANLS 为 65.1/62.6；ChartQA test relaxed EM 为 65.7/66.3。这些例子既显示多任务能力，也说明 SFT 不能被概括为每项指标都提升。不同表包含更强 specialist，作者关于 generalist 的比较不等于超过所有专用系统。[[raw/papers/models/qwen/Qwen-VL.pdf#page=7|p.7–8 · Tables 4–5]] [[raw/papers/models/qwen/Qwen-VL.pdf#page=21|p.21 · Table 9]]

VQAv2、OKVQA、GQA、VizWiz 采用开放答案生成与 greedy decoding；ScienceQA-Img 则限制候选选项并选择最高置信度选项，报告 top-1 accuracy。训练已包含 VQAv2、GQA、TextVQA、DocVQA 等，不能把整张表都叫 zero-shot；仅对论文明确标注的目标任务采用该标签。本文没有把完整 benchmark judge 协议和人类一致性实验全部重做，本页不代为补齐。[[raw/papers/models/qwen/Qwen-VL.pdf#page=6|p.6 · Table 3]] [[raw/papers/models/qwen/Qwen-VL.pdf#page=7|p.7 · §4.1]]

### 定位、多图与视频的不同证据强度

RefCOCO、RefCOCO+、RefCOCOg 和 GRIT 评价给定表达的区域定位；例如 Qwen-VL 在 RefCOCO test-A/test-B 为 92.26/85.34。它是受表达引导的目标定位，不能当作开放世界检测、任意图形编辑或动作执行成功率；Appendix D 仅将其指标列为 Accuracy，本篇未完整重述所有几何判分细节。训练 GRIT（Peng 等的 grounded image-text 数据）与评测 GRIT（Gupta 等的 benchmark）还需按引用身份区分，不能仅按同名认定完全相同。[[raw/papers/models/qwen/Qwen-VL.pdf#page=5|p.5–6 · §3.2]] [[raw/papers/models/qwen/Qwen-VL.pdf#page=8|p.8 · Table 6]] [[raw/papers/models/qwen/Qwen-VL.pdf#page=21|p.21 · Table 9]]

Few-shot 采用随机抽样示例，未使用 RICES；Fig.4 显示部分任务从增加上下文示例获益，但 TextVQA 曲线并非随 shot 数持续上升。SEED-Bench 视频任务只抽 4 帧，说明多图输入可迁移到部分视频题，不是专用连续时序编码或长视频训练的证明。[[raw/papers/models/qwen/Qwen-VL.pdf#page=8|p.8–9 · §4.4–4.5 / Fig.4]]

TouchStone 为 GPT-4 评分的开放指令测试，SEED-Bench 为多项选择，MME 包含感知/认知子任务；它们的原始分数不可直接互相比大小，也不足以独立保证真实部署中的可靠性。本文使用这些现有 benchmark；未在本页虚构新的评测协议或人类一致性验证。[[raw/papers/models/qwen/Qwen-VL.pdf#page=9|p.9 · §4.5 / Table 7]] [[raw/papers/models/qwen/Qwen-VL.pdf#page=21|p.21 · Table 9]]

### 文本能力保持：比较正确的初始化

Table 11 的 Qwen-7B intermediate 在 MMLU/C-Eval 为 49.9/48.5，Qwen-VL 为 50.7/51.1；最终发布 Qwen-7B 则为 58.2/63.5。前一对支持作者在这些任务上的“不退化”观察，后一差距不能简单归因为多模态训练损害文本能力，因为起点不同。未给出的 intermediate CMMLU、更多语言任务与重复运行不确定性，不能用一张表填满。[[raw/papers/models/qwen/Qwen-VL.pdf#page=23|p.23–24 · Appendix E.4 / Table 11]]

## 5. 旧理解修订与主题落点

旧笔记的三阶段冻结关系、256 query 与 2D 位置设计可保留；“ViT 可学习 1D PE、resampler 不可学习 2D PE”及与其它实现的细节比较，在本次论文已读范围未被完整展开，不作为本篇直接证据。“缓解 1D 位置编码损失”宜收紧为原文说的“缓解压缩中的位置细节损失”；主张对象不同。补充 Qwen-7B intermediate 身份、查询数消融的 ViT-L 条件、窗口实验与实际训练预算，使旧稿的架构介绍能够对应证据范围。

本来源可支持 [[wiki/vision/Overview|视觉表示]] 中固定 token 瓶颈与细粒度监督的讨论，[[wiki/training/Overview|训练]] 中三阶段开放参数与文本混合的比较，以及 [[wiki/evaluation/Overview|评测]] 中 base/chat、开放生成/选项判分和初始化差异的区分。共享主题尚待协调者整合；本篇没有单独隔离分辨率、位置编码、数据量与所有目标任务提升的因果贡献。作者提出未来扩展音频/视频与图像/语音生成，这些不属于本报告已经验证的完整能力。[[raw/papers/models/qwen/Qwen-VL.pdf#page=10|p.10 · §6]]
