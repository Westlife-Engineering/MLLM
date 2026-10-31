---
type: source
source_id: S029
primary_direction: models/qwen
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/web/S029-Qwen-3.5/README.md]]"
  - "[[raw/web/S029-Qwen-3.5/config.json]]"
reading_status: read
ingest_status: complete
related_directions:
  - architecture/connectors
---

# Qwen3.5-397B-A17B：固定模型卡与配置能确认什么

本页读取的是 **Qwen/Qwen3.5-397B-A17B 的官方模型卡和配置快照**，不是一篇已取得的 Qwen3.5 方法论文。它最清楚地回答两个问题：这个具体 checkpoint 的视觉/语言结构如何配置，以及官方如何建议运行和比较它。模型卡对早期多模态融合、强化学习规模和训练效率的概括属于官方声明；现有快照不足以重建完整训练算法或独立验证官方榜单。[[raw/web/S029-Qwen-3.5/README.md#Qwen3.5 Highlights|README：Highlights]] [[raw/web/S029-Qwen-3.5/README.md#Model Overview|README：Model Overview]]

## 来源身份与实际读取

| 项目 | 记录 |
| --- | --- |
| 官方身份 | Qwen Team，Qwen/Qwen3.5-397B-A17B；模型卡声明此仓库为 post-trained 模型的 Transformers 权重/配置 |
| 固定版本 | Hugging Face commit 8472618112abcbd45acbcdc58436aff4233c23f7；读取/快照访问日 2026-10-31 |
| README 原始 URL | [固定 commit README](https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/8472618112abcbd45acbcdc58436aff4233c23f7/README.md) |
| config 原始 URL | [固定 commit config.json](https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/8472618112abcbd45acbcdc58436aff4233c23f7/config.json) |
| README SHA-256 | bda4b24e975f65ac677985306ddbad33362e65064637660654c8bb7dea7edf50 |
| config SHA-256 | 3ae7fa89c2f7d1354096418ddaf1331e9e0898a8ca11e804fb6dbaa087efb7da |
| 实际阅读 | README 全文（含 HTML 表格、脚注、服务/接口示例、长上下文与最佳实践）；config.json 全部字段 |
| 附件边界 | README 中远端 logo/分数图片、链接博客及外部部署文档没有作为本次已读来源；快照未包含这些图片字节。HTML 表格直接核对文本单元格，不伪造 PDF 页码 |
| 旧笔记输入 | [[raw/notes/MLLM实例/Qwen/Qwen-3.5总结.tex]] 全正文；[[raw/notes/MLLM实例/Qwen/Latex_out/Qwen-3.5总结.pdf]] 共 4 页，全文比对、图像核看 p1–3 |
| 未实施 | 未取得/运行权重，未审计模型实现或 Transformers PR，未测试服务命令、工具调用或评分；Obsidian 内显示未测 |

模型卡 Citation 给出 *Qwen3.5: Towards Native Multimodal Agents*、February 2026 与博客 URL，不能据此补造 arXiv 身份或“原论文 PDF”。本页适用于上述固定 commit，不保证动态 main 或托管服务此后的行为。

## 1. 语言骨干：在每四层里保留一层全注意力

模型卡把语言模型标为总参数 397B、激活参数 17B，隐藏维度 4,096，60 层。基本布局重复 15 次：三层 Gated DeltaNet→MoE，接一层 Gated Attention→MoE。config 的 layer_types 也确实列出三次 linear_attention 后一次 full_attention，总计 45 个线性层、15 个全注意力层；这些计数是由固定配置直接汇总，并非通过运行模型测得。[[raw/web/S029-Qwen-3.5/README.md#Model Overview|README：Model Overview]] [[raw/web/S029-Qwen-3.5/config.json|config：text_config.layer_types、full_attention_interval、num_hidden_layers]]

**机制层面的可用理解：**这种结构让多数层采用线性 attention 路径，并周期性保留全 attention，试图平衡序列成本与跨 token 交互能力。模型卡将该混合结构列为效率来源，但没有给出与纯 attention、纯 DeltaNet 的同预算消融，也没有展开状态递推公式。因此不能从 3:1 直接推导固定速度倍数、延迟或长上下文无损结论。[[raw/web/S029-Qwen-3.5/README.md#Qwen3.5 Highlights|README：Efficient Hybrid Architecture]] [[raw/web/S029-Qwen-3.5/README.md#Serving Qwen3.5|README：Serving，明确效率依赖框架]]

| 组件 | 固定配置/模型卡数值 | 解释边界 |
| --- | --- | --- |
| Gated DeltaNet | QK 16 heads、V 64 heads，key/value head_dim 均 128；linear_conv_kernel_dim=4 | 头数及卷积宽度可确认；状态更新、门位置、归一化运算不能只凭字段完整恢复 |
| Gated Attention | 32 Q heads、2 KV heads，head_dim=256，attn_output_gate=true | 可以确认输出门配置；未核实现中的具体投影拆分 |
| MoE | 512 routed experts，token 激活 10 routed + 1 shared；各 expert 中间维度 1,024 | 激活参数和总存储量不同；配置没有给出部署显存实测 |
| 词表/输出 | vocab_size=248,320；tie_word_embeddings=false | 模型卡将词表标为 padded；不能把 padded 数当成真实自然语言词数 |
| MTP | 模型卡称 multi-steps；config 的 mtp_num_hidden_layers=1 | MTP 层数、训练预测步数、推测解码候选长度是不同维度，不能互相替代 |

表内证据：[[raw/web/S029-Qwen-3.5/README.md#Model Overview|README：Model Overview]] 与 [[raw/web/S029-Qwen-3.5/config.json|config：text_config、tie_word_embeddings]]。router_aux_loss_coef=0.001 是配置字段，不能单凭它还原实际训练中的全部负载均衡方法和损失权重调度。

## 2. 视觉输入与位置：从配置确认接口，避免反推未公开训练

视觉配置给出 depth=27、hidden_size=1,152、intermediate_size=4,304、16 heads、RGB 三通道，patch_size=16、temporal_patch_size=2、spatial_merge_size=2，输出宽度 4,096 与语言隐藏维度对齐。由这些尺寸可理解其空间合并粒度为 $2\times2$ patch，但配置本身没有提供完整的图像缩放/裁剪/打包算法，也没有逐项报告图像/视频训练 token 上下限。[[raw/web/S029-Qwen-3.5/config.json|config：vision_config]]

这里 **deepstack_visual_indexes=[]**。可确认这个 checkpoint 没有配置 DeepStack 中间视觉层索引，区别于 [[wiki/papers/models/qwen/Qwen3-VL|Qwen3-VL（S028）]] 报告中的三层视觉注入；不能进一步说“任何 Qwen3.5 变体均以完全相同代码移除了 DeepStack”。同样，num_position_embeddings=2304 是配置表尺寸，不能将它直接当成每张图片最终送入语言模型的固定 token 数。[[raw/web/S029-Qwen-3.5/config.json|config：vision_config.deepstack_visual_indexes、num_position_embeddings]]

语言位置配置为 interleaved MRoPE，mrope_section=[11,11,10]、rope_theta=10,000,000、partial_rotary_factor=0.25，head_dim=256；模型卡据此给出旋转维度 64。固定配置的 rope_type 是 default，**不是已开启 YaRN**。此处核实的是字段及模型卡说明，没有审计这些字段在每种推理后端的实现语义。[[raw/web/S029-Qwen-3.5/config.json|config：text_config.rope_parameters]] [[raw/web/S029-Qwen-3.5/README.md#Model Overview|README：Gated Attention]]

## 3. 256K 原生、约 1M 外推与托管版本要分开

本 checkpoint 原生上下文 262,144 tokens，模型卡给出的外推上限为 1,010,000；输入与输出共同占用窗口。官方提供 YaRN factor=4、original_max_position_embeddings=262144 的修改示例，也提醒静态 YaRN 可能影响短文本表现。它没有给出本快照内的完整长度—性能曲线，因此“配置能启动到约 1M”不能自动写成所有任务在该长度可靠。[[raw/web/S029-Qwen-3.5/README.md#Processing Ultra-Long Texts|README：Processing Ultra-Long Texts]]

开头另把 Qwen3.5-Plus 描述为对应的托管版本，默认 1M 上下文并带内建工具与自适应工具使用。这是服务说明，不能拿来覆盖开源 checkpoint 的原生长度、工具依赖或部署行为。[[raw/web/S029-Qwen-3.5/README.md#Qwen3.5-397B-A17B|README：开头 Tip]]

视频 API 示例默认 fps=2、do_sample_frames=true，并注明通过该 extra_body 调采样的示例在此文档时点仅支持 vLLM 且需相应服务启动参数。Best Practices 建议长视频将 video_preprocessor_config 的 longest_edge 改为 469,762,048，对应约 224K video tokens；这是长视频建议预算，不能把这个数字理解成图像单边像素长度。本轮只有 README/config 两个文件，**未读取实际 video_preprocessor_config.json**，故不宣称其默认值已独立核实。[[raw/web/S029-Qwen-3.5/README.md#Video Input|README：Video Input]] [[raw/web/S029-Qwen-3.5/README.md#Best Practices|README：Best Practices 第5项]]

## 4. 使用协议也是比较条件

模型卡默认 Thinking；关闭思考的本地兼容 API 示例使用 chat_template_kwargs 中的 enable_thinking=false，托管 Model Studio 示例则直接传 enable_thinking=false。文档明确不正式支持 Qwen3 的 /think、/nothink 软开关。这是固定版本说明，本页不执行命令，也不把外部框架的 main 安装指令当成永远有效的部署指南。[[raw/web/S029-Qwen-3.5/README.md#Instruct (or Non-Thinking) Mode|README：Instruct (or Non-Thinking) Mode]]

| 模式 | temperature / top-p / top-k | presence penalty | 建议输出预算 |
| --- | --- | --- | --- |
| Thinking | 0.6 / 0.95 / 20 | API 提示为 0.0 | 一般任务 32,768；复杂数学/编程基准 81,920 |
| Non-thinking | 0.7 / 0.8 / 20 | API 提示为 1.5 | 直接回答示例 32,768 |

上述是建议与示例，不是所有排行榜行已逐项确认的统一评估参数。模型卡还建议历史轮只保留最终输出，不带先前 thinking 内容，并指出 presence penalty 较高可能带来语言混合和轻微退化。[[raw/web/S029-Qwen-3.5/README.md#Using Qwen3.5 via the Chat Completions API|README：采样提示]] [[raw/web/S029-Qwen-3.5/README.md#Best Practices|README：Best Practices]]

服务示例以 8 路 tensor parallel 启动；MTP 的 SGLang 示例设 3 steps/4 draft tokens，vLLM 示例设 num_speculative_tokens=2，说明后端启用参数不是一个可直接互换的数字。text-only 服务选项跳过视觉编码器和多模态 profiling，文档称可给 KV cache 腾出显存；这不等于模型架构变成另一种纯文本 checkpoint。[[raw/web/S029-Qwen-3.5/README.md#SGLang|README：SGLang]] [[raw/web/S029-Qwen-3.5/README.md#vLLM|README：vLLM]]

## 5. 如何阅读官方结果而不制造“独立验证”

模型卡 Language 与 Vision Language 两张表包含不同领域、基线和工具设置。本页只抽取能说明条件差异的例子，不把它们合成跨任务总排名。

| 官方表中的例子 | 应保留的条件 | 可以得出的限定判断 |
| --- | --- | --- |
| MathVision 88.6 | 本模型固定 step-by-step/boxed 提示；对其他模型取有/无 boxed 较高结果 | 是模型卡该提示协议下的比较，非完全同一提示对照 |
| BabyVision 52.3 / 43.3 | 前者开启 Code Interpreter，后者关闭 | 工具条件影响成绩，不能只报较高值当无工具感知能力 |
| V* 95.8 / 91.1 | 同样分别为有/无 Code Interpreter | 不与其他来源的 crop-only 工具设置直接等同 |
| BrowseComp 69.0 / 78.6 | simple context-folding / discard-all 两种上下文管理 | 同一模型的外部历史管理可显著影响最终成绩 |
| VideoMME 87.5 / 83.7 | 有字幕 / 无字幕 | 文本辅助条件必须保留；当前快照未逐模型报告完整帧/token 预算 |
| OCRBench 93.1 | 本模型卡采用该数值尺度；S028 报告以 875 等数值呈现其模型 | 跨来源先对齐指标定义与尺度，不能直接相减 |

视觉例子见 [[raw/web/S029-Qwen-3.5/README.md#Vision Language|README：Vision Language 表及脚注]]；搜索例子见 [[raw/web/S029-Qwen-3.5/README.md#Language|README：Language 表及脚注]]。例如本模型 MMMU 85.0 仍低于同表 Gemini-3 Pro 87.2，SimpleVQA 67.1 也低于 73.2；Highlights 的整体能力宣传不能读成表内每个任务均领先。

搜索 agent 多采用 256K 上下文，工具响应达到阈值后删除早期响应；WideSearch 则明确在 256K 内不做上下文管理。MCPMark 使用 GitHub MCP v0.30.3，并把 Playwright 工具响应截断到 32K；TAU2 航空域使用额外修复。这些脚手架与数据处理属于测量条件，不能归入模型裸能力。[[raw/web/S029-Qwen-3.5/README.md#Language|README：Language 脚注]]

模型卡还介绍 HLE-Verified（经核验修订的 HLE，声称有错误分类与逐组件核验）和 WMT24++（难度标注/重平衡后的较难子集，以 XCOMET-XXL 评 55 语言）。本次只读到模型卡脚注，没有取得这些对象的完整构建、样本量、人工核验一致性或评分校准协议；不据此新建已读 benchmark 页，也不把自建子集分数当作已独立审计。[[raw/web/S029-Qwen-3.5/README.md#Language|README：HLE-Verified、WMT24++ 脚注]]

## 6. 训练与旧笔记：哪些解释需要收紧

官方 Highlights 称使用 early fusion 多模态训练、百万 agent 环境规模、201 种语言/方言和接近纯文本的多模态训练效率。这些是官方概括，本快照没有给训练阶段冻结表、训练 token 量、数据混合比例、完整 RL 奖励、硬件成本及同预算消融，因而无法像 [[wiki/papers/models/qwen/Qwen3-VL|S028 报告]] 那样重建分阶段配方。近 100% 训练效率尤其缺少此处可复核的测量口径。[[raw/web/S029-Qwen-3.5/README.md#Qwen3.5 Highlights|README：Highlights]]

旧 TeX 主要解释架构代码，范围包含 dense 与 MoE 家族；本页只有 **397B-A17B MoE** 的固定一手配置，不能证明全家族除 FFN 外“其余完全一致”。旧文把 Gated DeltaNet 写成遗忘加 key-value 外积的递推，但当前 README/config 没有相应公式，不能把旧式当成官方定义；要确认其 delta correction 必须另有已读一手公式或实现。旧文“scale=1 类似恒等映射”的表述也需要区分：即使缩放系数为 1，归一化运算本身仍会改变一般输入；“不减均值因而不稳定”的因果解释不由当前来源支持。

由空 DeepStack 索引可以确认本 checkpoint 的配置差异，却不能把“NaViT”和“DeepStack”写成二选一的同层概念：一个涉及视觉输入/编码处理，另一个涉及中间视觉特征如何注入语言层。具体 reshape、共享专家 sigmoid 门和 QK norm 代码在旧笔记里有说明，但本次未回读 PR，保留为待实现核查内容。旧笔记不是对已读模型卡的补充实验。

## 7. 本库关联与待解决问题

与 [[wiki/papers/models/qwen/Qwen3-VL|S028]] 的可证比较是视觉层级注入配置、位置参数和上下文声明；与 [[wiki/papers/models/qwen/Qwen2-VL|S027]] 可比较视觉 token 控制的不同证据公开程度。进一步主题建议为混合 attention、稀疏激活与总存储、工具/上下文管理对评估的影响。实际主题关系见页末。

仍未知的是：线性/全注意力比例的独立收益、视觉继续预训练来源与预算、实际训练各阶段的解冻策略、完整长视频采样限制、不同后端的数值一致性，以及官方评测的全套运行配置。现有文档足以建立版本明确的使用和配置认识，不足以将这些未知填成方法论文结论。

## 实际整合关系

支撑固定模型卡/配置的混合attention、MoE、视觉索引和上下文声明；不反推完整训练或实际速度。

- [[wiki/architecture/Sequence-Memory-and-Retrieval|序列记忆与检索：固定状态、稀疏KV、残差流和查表容量分别保存什么？]]。
- [[wiki/efficiency/Resource-Ledger|资源账本：视觉token、激活参数、KV与系统预算分别省在哪里？]]。
- [[wiki/models/Family-Changes|家族变化轴：输入、接口、数据和计算怎样共同演进？]]。
