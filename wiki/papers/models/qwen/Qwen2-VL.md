---
type: paper
source_id: S027
primary_direction: models/qwen
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/models/qwen/Qwen2-VL.pdf]]"
reading_status: read
ingest_status: complete
related_directions:
  - vision/encoders
  - architecture/connectors
---

# Qwen2-VL：动态视觉 token、M-RoPE 与图像视频统一输入

## 问题与核心认识

相对 [[wiki/papers/models/qwen/Qwen-VL|Qwen-VL（S026）]] 的固定分辨率与每图 256 token，Qwen2-VL 把视觉输入改为**随图像尺寸变化的 token 序列**，用邻近 $2\times2$ 合并控制长度；视觉编码器使用 2D-RoPE，语言模型使用时间、高、宽三分量的 M-RoPE。两种位置机制作用位置不同，不能把“MRoPE”和“RoPE-2D”当成同一模块。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=4|p.4–5 · §2.1 / Figs.2–3]]

动态分辨率让预算能够随输入细节变化，但“任意分辨率”仍受到像素/token 上限约束。视频也在帧数、分辨率与总 token 之间取舍；agent 结果则包含 Qwen-Agent、预定义动作及部分外部感知工具，不能只用语言模型名字概括完整实验系统。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=5|p.5 · Unified Image and Video Understanding]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=12|p.12–14 · §3.2.7、§3.3.1]]

## 来源与阅读范围

| 项目 | 记录 |
| --- | --- |
| 标题 | Qwen2-VL: Enhancing Vision-Language Model’s Perception of the World at Any Resolution |
| 作者 / 机构 | Peng Wang、Shuai Bai、Sinan Tan、Shijie Wang、Zhihao Fan、Jinze Bai 等；Qwen Team，Alibaba Group；完整署名见原件首页 |
| 版本 | arXiv:2409.12191v2，2024-10-03；[固定版本](https://arxiv.org/pdf/2409.12191v2) |
| 原件 / SHA-256 | [[raw/papers/models/qwen/Qwen2-VL.pdf\|52 页 PDF]]；30bb0f6c9babf910295d6b7cd34b6f54824236f68782664c3c93fbf4803275d0 |
| 阅读日期 / 内容 | 2026-10-31；正文 p.1–16 已读；Appendix A p.25–52 的说明与示例输出已读，未逐条执行或独立验证每个示例；参考文献 p.17–24 仅导航 |
| 原页视觉核看 | p.3–6、9–10、12、14–16、27、45–46、51；架构、位置图、监督着色、主要表及消融、代表性文档/工具/交互示例 |
| 旧笔记 | [[raw/notes/MLLM实例/Qwen/Qwen2-VL总结.tex\|旧 TeX]] 正文已读；[[raw/notes/MLLM实例/Qwen/Latex_out/Qwen2-VL总结.pdf\|旧 PDF]] 全 3 页核看，均为二手输入 |
| 未做事项 | 未读官方实现/训练代码，未运行模型或复现；自建 function-calling 仅审本文公开协议；Obsidian 内显示未测 |

## 1. 动态分辨率不是“无限增大图片”

三个型号共用 675M 参数视觉编码器，初始化来自 DFN ViT；语言模型来自 Qwen2。Table 1 将 2B/7B/72B 型号的 LLM 分项列为 1.5B/7.6B/72B，正文又用约 2B/8B/72B 总规模概括。型号名、语言部分与取整后的系统规模不是同一精确计数，不应机械由名称反推所有模块参数。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=3|p.3 · Table 1 / §2]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=5|p.5 · §2.2]]

Naive Dynamic Resolution 去掉 ViT 原来的绝对位置 embedding，加入 2D-RoPE；不同尺寸图像产生不同数量 patch tokens，并通过 packing 与长度上限控制显存。ViT 后的 MLP 将相邻 $2\times2$ tokens 合并，保留可变长度，而非把每张图都压到固定 query 数。原文称 simple MLP layer，没有在本篇完整给出旧笔记中的类名、两层投影代码或实现归属，不把这些当作本次代码审计结果。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=4|p.4 · Naive Dynamic Resolution]]

对满足网格对齐的图像，以下是根据 patch 14 与 $2\times2$ 合并得到的**教学算式**：

$$
N_{\mathrm{visual}}=\frac{H}{28}\frac{W}{28}.
$$

它不包含边界符，也不替代实际 resize/对齐实现。论文例子 $224^2$ 得到 64 个视觉 token，加起止标记后送入 LLM 的序列为 66 tokens；不能把 66 误读为 patch 数。相较前代，接口长度跟随图像面积变化，细节和语言计算开销随之变化。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=4|p.4 · §2.1]]

### 动态预算的消融究竟比较了什么

Table 7 的 fixed strategy 固定的是视觉 token 数，仍保留图像比例，并非强行缩成相同长宽；dynamic 设置为 min_pixels=$100\times28\times28$、max_pixels=$16384\times28\times28$。Qwen2-VL-7B 动态方案平均 1,924 tokens，相比固定 3,136 tokens，InfoVQA val 75.89 vs 77.27、RealWorldQA 70.07 vs 70.59、OCRBench 866 vs 786、MMMU 同为 53.44。合理结论是不同任务上的预算折中，不是动态策略每列最高或比每种固定预算都更省。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=14|p.14 · §3.3.1 / Table 7]]

Fig.4 表明适度放大小图可以提高一些感知任务成绩，但 OCRBench 在过高 min_pixels 下明显下降，MMMU 改善有限。作者将其分别解释为偏离训练分布、推理瓶颈；这些是解释假说，没有在本篇完成因果隔离。插值不会创造新的原始细节，新增 token/计算也不保证持续收益。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=14|p.14–15 · §3.3.1 / Fig.4]]

## 2. M-RoPE：把序列次序拆成时间与空间坐标

语言模型中将 rotary embedding 分成 temporal、height、width 三部分。文本 token 的三个 position IDs 相同，因此退化为普通 1D-RoPE；单张图像的 temporal ID 固定，高宽 ID 根据网格位置变化；视频随帧推进 temporal ID，高宽沿用图像组织。后续模态从前一模态的最大 position ID 加一开始编号。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=5|p.5 · Fig.3 / M-RoPE]]

例如，同一幅图中左右相邻 token 可具有相同时间/高度、不同宽度 ID；上下邻居则高度不同。这个教学例子说明它保留的是结构坐标，而非仅把整幅图铺平成连续自然数。**时间 ID 在本篇描述中随帧递增，不是已经确认的实际秒数编码**；不能把后续代际的时间戳设计反写进本篇。

论文没有给出本实现完整维度分配表、每个频率块的索引公式或所有视频边界情形，本页不从旧代码讲解补成原论文内容。位置编码减少图像/视频使用的最大 ID，是作者说明长度外推的理由之一；不等于已证明所有长上下文任务都能稳定外推。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=5|p.5 · §2.1]]

Table 8 用 **Qwen2-1.5B + ViT-L 的预训练模型**比较 1D-RoPE 与 M-RoPE。视频三项 PerceptionTest/NextQA/STAR 从 46.6/43.9/55.5 到 47.4/46.0/57.9；图像任务并非全升，RealWorldQA 54.5→53.7、InfoVQA 50.8→50.3，MMStar 不变。这个消融不应标成最终 72B 的全模型比较。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=15|p.15 · §3.3.2 / Table 8]]

## 3. 视频：时间压缩与空间预算共同决定可读长度

训练视频以 2 fps 抽样，depth=2 的 3D convolution 将两帧组成时空 tube；静态图像复制为两帧以共用输入路径。对长视频动态调整每帧分辨率，限制每视频总 token 为 16,384。空间合并和时间两帧分组作用不同；不能把“压缩两帧”理解为直接丢掉一帧，也不能声称所有原始视频信息都被无损保留。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=5|p.5 · Unified Image and Video Understanding]]

Video-MME 评估最多取 768 帧，需与“视频本身可长达一小时”区分。Table 4 中 72B 无字幕/有字幕分数为 71.2/77.8；字幕提供额外信息，不是同条件提升。另一个外推实验在 **Video-MME medium videos** 上把推理长度从 8K 扩到 80K，Fig.5 的 16K/48K/80K 为 70.1/71.3/71.1；表现并非单调增加，且没有同图给出 1D-RoPE 的匹配长度对照。它支持特定视频集合上的长序列使用，不构成任意 80K 输入的可靠性保证。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=10|p.10 · Table 4]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=12|p.12 · §3.2.6]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=15|p.15 · Fig.5]]

## 4. 训练、监督位置与系统成本

| 阶段 | 原文开放参数描述 | 数据与训练量 |
| --- | --- | --- |
| 第一阶段 | 专门训练 ViT，语言部分保持原有 Qwen2 初始化 | 约 600B tokens；图文关系、OCR、图像分类 |
| 第二阶段 | 解冻全部参数 | 额外约 800B tokens；交错图文、VQA、多任务与纯文本 |
| 指令微调 | 冻结 ViT，微调 LLM | ChatML；图像问答、文档解析、多图比较、视频/流式对话、agent 交互与纯文本对话 |

[[raw/papers/models/qwen/Qwen2-VL.pdf#page=5|p.5–6 · §2.2]]

前两阶段合计 1.4T **包含图像和文字**的 token，但只对文本 token 提供监督。论文阶段描述没有像 Qwen-VL 的 Table 8 那样细列 merger 在每阶段的独立冻结状态、学习率、batch 和步数，故表中不凭旧总结补齐。ChatML 原页还用蓝色标出被监督的答案和特殊符号，用户内容本身不是全部作为答案监督。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=6|p.6 · §2.2–2.2.1]]

报告的数据来源为清洗网页、开源数据与合成数据，作者给出的知识数据截止日期为 2023-06；这不是已完成训练污染审计的声明。基础设施包括 DP/TP/PP、ZeRO-1、sequence parallelism、selective activation checkpointing 和 FlashAttention；视频解码成为瓶颈，采用缓存解码。动态 token 节省不必然转化成相同比例端到端加速，实际成本还受解码、打包、并行和输入分布影响。本文没有给完整型号统一硬件下的推理延迟/显存扫描。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=5|p.5 · §2.2]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=8|p.8 · §2.3]]

## 5. 结果的强项、反例与统计边界

72B 在 DocVQA test 为 96.5、InfoVQA test 为 84.5、OCRBench 为 877，显示文档文字任务的强表现；但 MMMU val 64.5 低于表中 GPT-4o 69.1，MathVision 25.9 也低于 30.4。内部多语言 OCR 表中阿拉伯语 70.7 低于 GPT-4o 75.9，不支持“所有语言都超过”的概括。不同 metric、分辨率与闭源版本条件并未在主表全部对齐，本页不将这些数字变为当前排行榜结论。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=9|p.9 · Tables 2–3]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=11|p.11 · §3.2.2–3.2.4]]

RefCOCO+ test-B 的 72B 为 85.6，7B 为 79.5，2B 为 71.0；2B 并非在所有定位列都超过前代 Qwen-VL。Fig.6 展示型号扩大和第二阶段训练推进时的总体改善，但这些不是等总算力的受控比较，也没有拟合带不确定性区间的通用 scaling-law 方程。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=12|p.12 · Table 6]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=15|p.15–16 · §3.3.3 / Fig.6]]

### 5.1 内部 function-calling：测的是选函数和填参数

该测试的动机是衡量模型从图像提取信息并转成工具调用的能力。构建过程为：按视觉应用分场景，选网页图像，用 LVLM 提取视觉/文字信息，再由 LLM 生成问题、函数及所需参数。TM 是正确函数选择的比例，EM 是参数与记录信息精确匹配的比例；72B/GPT-4o 分别为 TM 93.1/90.2、EM 53.2/50.0。它揭示“选对工具”与“填对参数”之间的明显差距。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=12|p.12 · §3.2.7]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=10|p.10 · Table 5]]

Appendix A.4 的航班例子展示了完整意图：读目的地和到达时间→调用天气查询→从返回时段提取天气。这个流程中，选对天气函数并填“北京”还不足以保证最终回答对上到达时间；本库据此区分调用指标和端到端回答验收。正文未报告内部测试集规模、各类权重、合成标签的独立人工复核、人类一致性、等价参数处理、重复运行方差或置信区间；内部多语言 OCR 也缺少完整构造和判分细节。因此这些测试可作本文内部诊断，不能独立建立真实任务总体成功率。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=45|p.45 · Fig.26]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=9|p.9 · Table 3]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=12|p.12–13 · Function Calling]]

### 5.2 Agent 成绩属于模型与执行环境的组合

模型在 Qwen-Agent 中保留观察/动作历史，原文此处给出 32K context；每次执行动作后追加新观察。AITZ 的 TM/EM 为动作类型及位置/文本/方向匹配，不能把 72.1 EM 读成真实手机端到端成功率。ALFRED 是 AI2THOR 虚拟环境，高层动作包含 GotoLocation、Pickup、Slice 等，且结合 SAM 定位操作对象；valid-unseen 的 SR/GC=67.8/75.8 不是实物机器人的成功率。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=13|p.13 · §3.2.7]]

R2R/REVERIE valid-unseen SR=51.7/31.0，落后于表中专用系统 79.0/61.0；作者将不足联系到地图信息不完整、缺乏结构化，但未给出控制干预来证明唯一瓶颈。Point24 SR 仅 4.5，也反对把“支持 agent”当作所有复杂任务可靠完成的承诺。定性示例中代码解释器返回 Finished execution 只说明该次调用执行，尤其 p.46 的 placeholder 函数并未实现模块功能。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=10|p.10 · Table 5]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=13|p.13 · Vision-Language Navigation]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=46|p.46 · Fig.27]]

## 6. 旧稿修订与整合方向

旧笔记将视觉 RoPE-2D 与 LLM M-RoPE 混称，现分开其位置和职责；保留 MLP 合并邻近 $2\times2$ 的事实，但代码类名、两层结构和具体频率索引未经本次代码核查，不当作论文细节。旧稿“测试时放大图片就会提升”改成有限范围内的任务相关收益，并加入 OCR 下降和 MMMU 弱变化。训练阶段不补造 merger 冻结状态。

本页可支持 [[wiki/vision/Overview|视觉表示]] 的空间/时间 token 预算，[[wiki/architecture/Overview|架构]] 的前端与 LLM 位置机制分工，[[wiki/reasoning/Overview|推理与交互]] 的模型—工具—环境关系，以及 [[wiki/evaluation/Overview|评测]] 的内部合成测试与完整任务验收区别。实际共享主题关系见页末；本文原页已读不表示上述定性示例全部经过本次独立验算，也不把其它来源图像中的产品限制或公式当成本模型的新架构。

## 实际整合关系

支撑动态空间合并、视觉2D-RoPE/LLM M-RoPE分工，及动作匹配/模拟终态/定性执行的不同证据。

- [[wiki/vision/Resolution-and-Token-Budget|分辨率、packing与tiling：预算到底在哪个位置？]]。
- [[wiki/reasoning/Overview|推理与交互：增加计算、改变观察、控制环境怎样分别起作用？]]。
- [[wiki/evaluation/Judges-and-Task-Success|裁判与任务成功：答案、解释、生成物和终态怎样分别取证？]]。
- [[wiki/foundations/Formalization|基础：把信息、参数与任务证据分成三个层次]]。
- [[wiki/models/Family-Changes|家族变化轴：输入、接口、数据和计算怎样共同演进？]]。
