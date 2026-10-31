# R001 独立学术审查：S001 / S002

- 审查日期：2026-10-31（Asia/Shanghai）。角色 G，未参与被审页撰写；只写本报告，无 Git、Raw、知识页、主题、registry 或索引修改。
- 被审页：[[wiki/surveys/Efficient Multimodal Large Language Models A Survey]]、[[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models]]。
- 方法：读取当前 AGENTS.md 与 workflows/lint.md，使用 academic-researcher / pdf 技能；从归档 PDF 独立提取页文本、渲染关键页并检查。没有用 D 的 handoff 代替原文证据；本次未读取 handoff。
- 页码均从 PDF 第一页起算。以下“支持”指归档综述足以支持 Wiki 的归纳及其身份限定，不表示独立验证所引原论文、模型实测或综述全部技术解释。
- 入口检查时 wiki/index.md、wiki/log.md 尚不存在；按正在整合的任务状态记录，不据此否定来源页的内容质量，也不宣布整库验收完成。

## 审查结论

S001 核心机制、六类地图、视觉 token / 参数 / 激活计算 / 更新参数区分及评测边界可接受；建议在最终收尾前修正一处训练目标措辞，见 R1。另有一个新核出的原综述图注引用错配，见 R2；现有 Wiki 的机制解释受正确正文支持，故该错配不是整段解释失效。

S002 在本次核查范围内学术层可接受，无必须修改的事实错误。四阶段、native 与工具关系、o3 个案边界、Agentic Evaluation 和 GQA 错配均有直接原页依据。两页均能独立理解，不是逐章摘抄，也没有用限制声明替代主要内容；不要求扩增未读来源。

这是来源页的有限范围学术审查；不等于 ingest complete、全库结构通过或 Obsidian 显示通过。

## S001：逐项 claim 检查

原件：[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf]]，36 页，5,055,945 bytes；本次重算 SHA-256 为 `f62a5e5635507195c0571731aa46924e6336a13997c339ddc72c9e6b4ae83926`，与页内登记相同。

| 编号 | 当前页面主张 / 检查对象 | 判断 | 原页定位、检查结果及边界 |
| --- | --- | --- | --- |
| S001-C01 | 标题、作者、v3 / 2026-01-22、Preprint / Under review | 支持 | PDF p1 原页及文件元数据一致；首页两位作者有共同贡献标记。未核外部正式出版状态，当前页面也没有声称已核。 |
| S001-C02 | 三模块接口：视觉编码器、连接器、语言模型，自回归输出 | 支持 | pp4–7 §2，Eq.1 是 Zv=g(Xv)，p5 Eq.2 是 Hv=P(Zv)，p7 Eq.3 按输出前缀分解概率。Wiki 没把低权重占比与低视觉计算混为一谈，额外解释标为本库归纳。 |
| S001-C03 | 引言六类，Fig.2 只有四条顶层分支 | 支持 | p2 明列 architecture / efficient vision / efficient LLMs / training / data and benchmarks / applications；p3 Fig.2 渲染可见四分支；p10 Fig.9 与 p14 Fig.11 分别独立展开视觉与语言。没有误造六分支原图。 |
| S001-C04 | 视觉高分辨率与 token 压缩是相连但不同的环节，不能把平方开销扩大到全部 MLLM | 支持 | p7 §2.4 讨论分辨率提高导致更多 visual tokens；p14 §4.1 明确 n 是序列长度、复杂度来自 token 两两交互。Wiki 的限定合理，未把图像边长等同序列长度。 |
| S001-C05 | MLP、query 聚合、LDPv2、C/D-Abstractor 的机制区别 | 支持 | p6 §2.2 分别给出变换、可学习 query、pooling + PEG、卷积与 deformable attention 的机制；Wiki 的“输出长度、局部关系、查询/采样”是合理比较轴，不是性能排名。 |
| S001-C06 | S2 parameter-free 不代表额外视觉计算为零 | 支持 | p8 §2.4 解释不必从头训练额外参数；p9 Fig.7 显示 224 输入与 448 切成四块经同一 ViT-B，merge / pool 后沿通道 concat。Wiki 准确描述结构，并将计算辨析标为本库判断。 |
| S001-C07 | FastV / VTW 在后层减少或去除视觉 token，不能推出视觉 token 普遍无用 | 支持 | p10 §2.5 的两段描述分别指第二层以后及特定层之后；Wiki 保留层位置和任务外推边界，没有照搬作者“无性能损失”为普遍结论。 |
| S001-C08 | Efficient Vision 是可借鉴技术图谱，并非都已验证于完整 MLLM | 支持 | p10 §3 明写 may be used for efficient MLLMs，Fig.9 列紧凑架构、剪枝、蒸馏、量化。页面没有把单模态收益升级为跨模态证明。 |
| S001-C09 | 小于 3B 是典型描述而非严格筛选阈值 | 支持 | p7 §2.3 用 typically；p5 Table 1 中 Bunny-v1.1-4B 为 3.8B，MM1 条目另标 activated parameters。页面保留了案例集合的身份。 |
| S001-C10 | MoE 总参数与激活参数不同，Mamba 是另一种序列处理结构 | 支持 | p9 §2.5 明说增总参数但维持激活参数，pp15–16 §4.2 讨论 SSM / Mamba；Wiki 未从结构复杂度直接推出特定设备加速。 |
| S001-C11 | GQA/MQA 共享 Key/Value 头，主要连接自回归解码内存带宽 | 支持 | p14 §4.1 正文、p15 Fig.12 原图与 Wiki 一致。但图注 GQA[59] 引用编号错误：p28 [59] 是视觉问答数据集，p33 [143] 才是 GQA 注意力论文。正文 p14 使用 [143]，所以机制仍有支持；见 R2。 |
| S001-C12 | 低秩求逆、MoE 参数共享缩小模型、LoRA 分解原权重缩小模型、Adapter 加快推理这些可疑句确实在综述里 | 支持 | p15 §4.1 原文写两个低维矩阵求逆以近似 attention inverse；同页 §4.2 写专家参数训练共享并减少总参数；p17 §4.3 写分解 original weight matrices / compact model；p16 §4.3 写 faster training and inference。Wiki 将其隔离且不作为教学定义，处理恰当。本审查没有追读对应原论文以完成纠错。 |
| S001-C13 | PT/IT 常用相同自回归目标，常见冻结/更新范围不同 | 支持，但总结句需小修 | pp17–18 §5.1、Eq.4 与 Fig.14 支持 PT 训练 projector；p19 §5.2 明写 same auto-regressive training objective，典型 IT 固定视觉编码器、更新 projector 与 SLM。Wiki 前文正确，但“区别不仅是损失函数”可能暗示本文两阶段损失有差异；见 R1。p18 Eq.5 是对话序列构造规则，不是第二种损失。 |
| S001-C14 | Fig.14 非规范流水线，可开放更多参数、多阶段或单阶段 | 支持 | p18 Which part to unfreeze / Multi-stage pre-training；p19 §5.3 分别讨论 SPHINX-X、Cobra、TinyGPT-V。页面没有把阶段数少等同端到端更高效。 |
| S001-C15 | 数据表统计单位不同；强模型生成细 caption 涉及成本转移 | 支持 | p20 Table 2 区分 X / Text / X-T，MMC4 和 Obelics 标 Instances；p21 Table 3 为 Instance。p20 ShareGPT4V 段描述先训 captioner 再扩量。Wiki 没把这些表直接加总成训练 token 或 GPU 预算。 |
| S001-C16 | Table 4 不是统一资源测量，脚注影响比较 | 支持 | p22 原页表头只有模型/骨干及能力基准，未列统一硬件、时延、显存、能耗或训练成本；脚注核实 MMMU val/test、SEED whole/image、† 两 split 合计、* 训练时见过训练图像。Wiki 没把缺失当零或据颜色作总体排名。 |
| S001-C17 | 医学/视频案例是综述转述，未来方向是作者观点 | 支持 | pp22–23 §7 对应医学、视频表述；pp23–24 §8 为展望及覆盖限制。页面没有把医疗报告生成等同临床安全，也没有把未来方向当查新证明。 |
| S001-C18 | 本地版本日期不等于系统覆盖到 2026 年；阅读范围可登记正文 p1–24 | 部分支持 / 阅读行为无法独立判断 | p1 确为 2026-01-22 v3，p24 正文结束、p25 起参考文献。阅读范围结构合理；独立审查不能重建原 D 是否逐页通读的行为事实，也未在本次审查穷尽验证所有收录时间。页面未声称系统覆盖到 2026 年是正确边界。 |

## S002：逐项 claim 检查

原件：[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]，91 页，9,855,511 bytes；本次重算 SHA-256 为 `94bf79d9c9bbeeae25b997cd35a290e056dc4ba561bf5a9b4cd7a786e98cdd94`，与页内登记相同。

| 编号 | 当前页面主张 / 检查对象 | 判断 | 原页定位、检查结果及边界 |
| --- | --- | --- | --- |
| S002-C01 | 正式题名、作者、共同一作/通讯、v2 / 2025-07-06、91页 | 支持 | p1 原页及 PDF 元数据相符；三位共同一作与 Baotian Hu 通讯符号清楚。未外查正式出版与仓库当前状态，页面也未冒称核验。 |
| S002-C02 | 四阶段是作者组织方式，Stage 4 为 Prospect | 支持 | pp4–6 §2 列 Stage 1–4，p5 明标 Stage 4 … (Prospect)；p7 Fig.3 给四支分类树。Wiki 将必然性限制为本库解释，未伪称作者已证明演化定律。 |
| S002-C03 | 前三阶段机制不互斥，工具/长时程规划并非 Stage 3 才有 | 支持 | p13 §3.2.3 已讨论 search / tools / long-horizon planning；pp14–15 有 MCoT-Memory；pp15–16 §3.3.1 继续用工具。由这些重叠支持 Wiki 的本库判断。 |
| S002-C04 | Perception / Reason / Think / Plan 不是经过验证的四个串行模块 | 支持 | pp4–6 是叙事性阶段定义而非四个形式模块；p26 Fig.6 又示范裁剪观察与规则分析交替。Wiki 给自己的解释明确标身份，并无伪造形式定义。 |
| S002-C05 | N-LMRM 将 agentic reasoning 与 omni-modal understanding/generative reasoning 结合 | 支持 | p6 §2、p27 §4.2 列两种能力；p30 Fig.9 原图有 environment → perception、control 与 learning from experience 的循环关系。Wiki 以展望呈现，没有当成已验证系统。 |
| S002-C06 | 统一不意味着所有模态必须一个编码器，也不排除语言骨干与模态专家 | 支持 | pp30–31 §4.3 将统一表示作为挑战与可能路径，同时提出 modality-specialized MoE 及 core language model。Wiki 合理保留多种实现可能。 |
| S002-C07 | Native 多模态不等于不使用工具，o3/o4-mini 只是初步方向 | 支持 | p30 §4.3 直接写结合 diverse tools；p31 Interleaved Multimodal Long CoT 直接列 zoom / crop / flip / enhance，并称 pioneering steps。Wiki 未从闭源工具行为推断内部架构。 |
| S002-C08 | 训练与测试时计算应分开；图5只提供 DPO/GRPO 示意 | 支持 | p16 Fig.5 显示偏好路径、GRPO 分组路径与格式/答案/IoU/长度奖励；p18 上半段为 Best-of-N、beam search、MCTS，后半段为 RL。没有完整目标推导，页面不补造公式是恰当的。 |
| S002-C09 | R1-like 非统一 GRPO；任务收益不自动一般化 | 支持 | p19 Table 6 同列 DPO、RLOO、PPO、GRPO；p18 §3.3.3 明言现有工作常局限特定任务，数学长 CoT 尚未泛化为一般能力。Wiki 归因于综述，没有独立宣判所有 RL 结果。 |
| S002-C10 | 图6、7、8都是 o3 case study，不是 o3/o4-mini 对照 | 支持 | pp26–28 三个图注明确 o3；p26 小节标题同时提两模型，但后续正文明确 evaluated o3。Wiki 正确按可见证据缩窄范围。 |
| S002-C11 | 图6为裁剪试错后答对的8分13秒案例，不能证明 scaling 曲线 | 支持 | p26 Fig.6 标 8min13s、A及勾号，并显示不充分裁剪→扩大范围→规则分析；正文报告同一用时。没有同预算对照/重复统计。Wiki 把效率测量要求标本库推断合理。严格说图中给的是作者标注的 reasoning 时长，不是独立计时日志。 |
| S002-C12 | 数独终答正确但步骤说明有错，不支持主观欺骗意图结论 | 支持 | p27 Fig.7 展示 Solution by o3 勾号及红字错误步骤；正文用 lies、deceive 和未掌握思路的强解释。Wiki 保留为作者担忧，并将可见结果限定在解释可靠性，符合证据强度。未复算全部数独解，Wiki 本来也说“作者标注”。 |
| S002-C13 | 六指误报五指是个案；语言先验干扰是作者解释 | 支持 | p28 Fig.8 原图为六指，输出明确 four fingers plus a thumb / five fingers；p26 正文将其解释为 language knowledge interference。Wiki 没从一个例子识别内部因果机制。 |
| S002-C14 | 简历表、播客、红熊猫动画说明交付存在与完成要求可分离 | 支持 | p28 Fig.8 标空白、错误、重复简历信息；播客要求剪精彩句，输出仅 first two minutes；p27 Fig.7 的红熊猫要求与生成图不符。Wiki 限于作者报告的当时工具/网络条件，没有推广永久上限。 |
| S002-C15 | 这些图不是可复现性能协议，没有统一样本/抽样/配置/消融报告 | 支持（限定 §4.1 与图6–8） | 本次完整读取 pp25–28 §4.1 与案例图，见提示和摘录，没有所述统一实验协议；Wiki 对缺失的范围限定正确。不能据此否认其他所引 benchmark 各自可能有协议。 |
| S002-C16 | Understanding / Generation / Reasoning / Planning 是任务目录，且包含数据与 benchmark | 支持 | p32 Fig.10 图注与 §5 明列四类；p33 Table 14 明分 Benchmark / Dataset；p4 明示该部分更新至 2025-06-30。Wiki 没将它当当前完整能力目录。 |
| S002-C17 | Agentic Evaluation 指 agent/工具参与判分，并非单指评测被测 agent | 支持 | p41 §5.5 Agentic Evaluation 举 CIGEval toolbox 与 cooperative/adversarial multi-agent assessment；页面解释抓住评价方角色，与 p25 agent benchmarks 的被评对象区分正确。 |
| S002-C18 | GQA 在 p33 正文与表14 / p43书目之间存在引用错配 | 支持 | p33 正文写 GQA (Ainslie et al., 2023)，表14是 Hudson & Manning (2019)；p43 Ainslie 题名为 generalized multi-query transformer models。PDF 内就足以确认错配，不需新增来源，也不意味着整篇无效。 |
| S002-C19 | 读 p1–42 正文、p43参考文献起点，未追索所引论文 | 部分支持 / 阅读行为无法独立判断 | p41 开始 §6、p42续结论、p43参考文献，范围登记符合文档结构。G 无法证明 D 的全部阅读行为；本次审查覆盖关键代表主张而非全部91页。未见页面将综述所引论文升级为已读。 |

## 具体修订意见与处置优先级

### R1：S001 训练目标总结需小修，低严重度

位置：`## 训练与数据：接口能力由哪些参数、什么监督共同形成` 第一段末句。

现句：“训练阶段的区别不仅是损失函数，还包括数据内容、参数开放范围与想获得的行为。”

理由：该句容易让读者以为本综述 PT 与 IT 的主要差异包括不同损失，而 p19 §5.2 明确说使用相同自回归训练目标；同段 Wiki 前两句已经正确说明。不是机制整体误读，但总结句应与直接证据对齐。

建议替换：“两阶段可以使用相同的自回归训练目标，主要区别在数据内容、参数开放范围与希望获得的行为。”可继续用 pp17–19、Fig.14；若提公式，明确 Eq.4 为目标、Eq.5 为指令序列组织。

### R2：S001 新核出的原综述图注引用错配，建议记录，不阻断当前机制解释

位置：`GQA/MQA 的共享对象是 Key/Value 头` 段或紧邻的“不直接沿用的技术解释” Callout。

事实：p15 Fig.12 图注写 GQA[59]，而 p28 [59] 是 Hudson / Manning 的视觉问答数据集；p14 §4.1 正文使用 [143]，p33 [143] 是 Ainslie 等人的 GQA 注意力论文。现有 Wiki 链到整篇综述并解释图义，没有把 [59] 转录为正确注意力来源，因此现有机制说明仍获 p14 正文与图本身支持。

建议仅加一句：“Fig.12 图注将 GQA 注意力误标为[59]（p28为视觉问答数据集），其正文对应引用应为[143]（p33）；本页依据正文与图中头共享关系解释，未追读该注意力论文。”不需要展开成另一知识主题或增加未读来源。

### S002：无必须修改项

保留当前对四阶段、工具、数独“lies”、终态完成与 agent 判分的限定。可以将“8分13秒是一个案例的耗时”改得更精确为“作者在图中标注的 reasoning 用时”，但上下文已明示作者个案且未拿它作硬件基准，这属于可选精炼，不是阻断问题。

## 信息密度与可独立理解性

- S001 的主线是信息流和资源发生位置，连接器、S2、MoE、KV 共享、冻结参数与数据单位给出实质内容；六类表承担导航，后面的段落承担解释，分工成立。警示框是在处理综述确有的技术问题，不是空泛免责声明。完成 R1 后无需为篇幅而补更多模型名。
- S002 用四阶段地图、训练/测试时机制表与具体案例搭建“回答、解释、交付、环境终态”的区别，足以独立理解。案例有限性的重复稍多，但每次对应不同推论，不构成空壳式限制堆叠。当前不建议为了缩短而删除 o3 / o4-mini 范围辨析或 GQA 错配证据。
- 两页将主题整合明确留给协调者，未建立不存在的主题链接。审查时索引/日志未落地与 ingest_status: integrating 一致；最终主题双向关系与状态更新仍需主 Agent 检查。

## 实际覆盖与未覆盖

S001 本次回读文本：p1–10、p14–24，以及 p27–28、p33 的相关书目条目；视觉核查 p1、3、9、15、17、18、22。重点涵盖六类/Fig.2、S2/Fig.7、GQA/Fig.12、训练/Fig.14及公式、Table 4。没有逐项核查 §3 全部剪枝/蒸馏/量化案例、全部图表、参考文献或每个性能数字；未核实每个原论文算法正确性。

S002 本次回读文本：p1、4–6、13–16、18–19、25–33、41–43；视觉核查 p1、7、16、26、27、28、30、33、41。重点涵盖 Fig.3、5、6–9、Table 6与14、Agentic Evaluation 和 GQA 书目。未逐篇核查约700篇条目的身份/归类、未完整核读全部 benchmark 列表或所有训练数据条目，未统计作者案例总体成功率。

独立生成的文本与 PNG 位于系统临时目录 `C:/Users/ZENGZX/AppData/Local/Temp/mllm-kb-20261031/review/surveys/`。未改动归档 PDF。没有联网追读新来源、运行模型、复算全部案例、审计工具环境、访问 Obsidian、验证 Markdown 应用显示或测试 PDF 跳转。结构完整性、全库链接、registry、索引和最终 ingest 状态由协调者另行验收。


## 2026-10-31 修订复核：R1 / R2 关闭

G 重新读取当前 S001 来源页相关段落，并以本次独立提取的原 PDF p19、p15 / p28 / p33 定位复核，未重做整篇审查。

- **R1 已解决。** 现句明确两阶段可用相同自回归目标，差别在数据、开放参数与目标行为；并将 Eq.4 目标和 Eq.5 指令组织分开。与原文 p19 的 same auto-regressive training objective 一致。
- **R2 已解决。** 原文 Fig.12 的 GQA[59] 错配已加入原疑点框，注明 [59] 数据集与 [143] 注意力论文及其页码；仍以正文与图义为机制依据，未把被引论文登记已读。

S001 在本报告覆盖范围内没有未关闭的必须返工项。S002 原结论不变。此次关闭不替代共享主题、索引、registry、全库结构或应用显示验收。
