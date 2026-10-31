---
type: source
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/web/S024-LLaVA-NeXT/official-blog.html]]"
  - "[[raw/web/S024-LLaVA-NeXT/high_res_arch_v2.png]]"
source_id: S024
reading_status: read
ingest_status: complete
primary_direction: models/llava
related_directions:
  - architecture/connectors
  - vision/encoders
---

# LLaVA-NeXT：2024年1月版本的官方技术说明

此页依据 *LLaVA-NeXT: Improved reasoning, OCR, and world knowledge* 官方博客，解释动态高分辨率、数据混合和语言主干的变化。**它是官方网页来源，不是独立方法论文；本地证据固定于2026-10-31抓取状态，不保证与2024-01-30发布当天字节相同。** 本页不覆盖后来同名系列的视频、更多模型规模或后续发布。

## 身份、快照与读取范围

- [官方页面](https://llava-vl.github.io/blog/2024-01-30-llava-next/)；显示发布日期2024-01-30。作者：Haotian Liu、Chunyuan Li、Yuheng Li、Bo Li、Yuanhan Zhang、Sheng Shen、Yong Jae Lee。
- HTML原件：[[raw/web/S024-LLaVA-NeXT/official-blog.html]]；SHA-256：`23029ba42dcf6bba3b006770a839f44e76b52763b600d8780ab2d9712d7c886e`。
- 架构图原件：[[raw/web/S024-LLaVA-NeXT/high_res_arch_v2.png]]；[官方图URL](https://llava-vl.github.io/blog/assets/images/llava-1-6/high_res_arch_v2.png)；SHA-256：`7f8ed15e0ef0d16843297e1deb4a5d7ac2f386e681e44690d939b543b6d1f848`。
- 访问/读取日期2026-10-31。实际读完整HTML正文、Results及展开表、Detailed Technical Improvement、Model Card；查看本地架构PNG。Logo和对话示例图片未本地归档，示例仅核对HTML文字，不能宣称已核图中事实。未读链接指向的代码/模型卡和后续博客，未运行模型/部署；Obsidian 内显示未测。网页引用用标题与锚点，不造PDF页码。

## AnyRes 改变的是什么

博客将最大输入提高到相对336²约4倍像素，列672×672、336×1344、1344×336；这是**像素数**四倍，不是宽和高各四倍。支持网格 $\{2\times2,1\times\{2,3,4\},\{2,3,4\}\times1\}$，每个基础块336×336。选择有限网格是细节与计算成本的折中，“AnyRes”不意味着任意尺寸无预算上限。[Dynamic High Resolution](https://llava-vl.github.io/blog/2024-01-30-llava-next/#1-dynamic-high-resolution)、[Model Card](https://llava-vl.github.io/blog/2024-01-30-llava-next/#model-card)（访问2026-10-31；[[raw/web/S024-LLaVA-NeXT/official-blog.html|本地HTML快照]]）。

![[raw/web/S024-LLaVA-NeXT/high_res_arch_v2.png]]

上图是官方原图，展示2×2局部切块分别编码，再展平送入LLM；下路把整图缩小后编码，为局部特征补全局布局。不能把图中彩色小方块数当真实视觉token数。博客未完整展开padding移除、行末token、最终序列长度和动态网格选择算法；其链接指向更新后的1.5技术报告，相关报告细节见 [[wiki/papers/models/llava/LLaVA-1.5|LLaVA-1.5]]，但不能把报告的224像素HD设置原样覆盖此处336设置。[同节](https://llava-vl.github.io/blog/2024-01-30-llava-next/#1-dynamic-high-resolution)（访问2026-10-31；上述HTML与PNG原件）。

**本库分析：**局部切块提供更多小字与物体细节，整图分支提供跨块关系；它增加视觉序列计算，并未自动保证多图理解、OCR正确或幻觉消失。博客关于细节提升和幻觉减少属于作者对机制/效果的解释，未附完整隔离消融。

## 数据变化不仅是“比例调整”

| 变化 | 博客给出的做法 | 对解释的影响 |
| --- | --- | --- |
| 用户指令 | 使用LAION-GPT-V、ShareGPT-4V；另取demo真实用户请求/图片组成15K，经隐私/有害样本过滤，GPT-4V生成回复 | 教师可读视觉，与初版仅文字caption/box教师不同；“高质量”仍是作者的数据设计目标 |
| OCR | 移除TextCaps，因其训练图片与TextVQA相同；以DocVQA、SynDog-EN替换 | 有意减少开发评测的已见图混淆，不证明整个基础模型无污染 |
| 图表与示意图 | 添加ChartQA、DVQA、AI2D | 改变任务覆盖，不能把所有增益归于输入分辨率 |
| 语言主干 | Vicuna-1.5 7B/13B之外增加Mistral-7B和Nous-Hermes-2-Yi-34B | 对话、双语和推理成绩同时受到语言主干变化影响 |

来源：[Data Mixture](https://llava-vl.github.io/blog/2024-01-30-llava-next/#2-data-mixture)、[Scaling LLM backbone](https://llava-vl.github.io/blog/2024-01-30-llava-next/#3-scaling-llm-backbone)（访问2026-10-31；[[raw/web/S024-LLaVA-NeXT/official-blog.html|本地HTML快照]]）。具体各数据集占比、去重统计和样本级过滤质量未在该博客完整报告；不从“760K总量”补造混合比例。

## 训练与模块：照录明确字段，保留粗粒度之处

博客说复用1.5预训练connector。Model Card列Stage-1 558K、trainable module=Connector；Stage-2 760K、trainable module=**Full model**。本页保留官方原词；该表没有逐模块冻结清单，未审训练代码，不能自行把它改成“视觉一定冻结”或推断每个参数都更新。训练目标、学习率、epoch和推理解码预算也未完整给出。[Model Card](https://llava-vl.github.io/blog/2024-01-30-llava-next/#model-card)（访问2026-10-31；[[raw/web/S024-LLaVA-NeXT/official-blog.html|本地HTML快照]]）。

| 卡片字段 | 7B | 13B | 34B |
| --- | ---: | ---: | ---: |
| 总参数 | 7.06B | 13.35B | 34.75B |
| 视觉编码器 | 303.5M | 303.5M | 303.5M |
| Connector | 21M | 31.5M | 58.7M |
| GPU×小时 | 8×20 | 16×24 | 32×30 |

卡片总训练样本1318K=558K+760K。导语“34B约一天/32 A100”是粗略表述，具体卡片为32×30小时；保留二者的粒度差别。博客“100–1000倍低成本”未在该页给完整成本归一协议，不作为独立验证的成本比，更不包含已预训练视觉/语言主干的全生命周期成本。[Results](https://llava-vl.github.io/blog/2024-01-30-llava-next/#results)、[Model Card](https://llava-vl.github.io/blog/2024-01-30-llava-next/#model-card)（访问2026-10-31；本地HTML快照同上）。

## Results 是带版本和条件的作者报告

| 博客结果（本快照） | LLaVA-1.5-13B | NeXT-13B | NeXT-34B |
| --- | ---: | ---: | ---: |
| MMMU val | 36.4 | 36.2 | 51.1 |
| MathVista | 27.6 | 35.3 | 46.5 |
| MMB-ENG | 67.8 | 70.0 | 79.3 |
| MM-Vet | 36.3 | 48.4 | 57.4 |
| TextVQA | 61.3（训练图像已见标记） | 67.1 | 69.5 |

[Results及展开表](https://llava-vl.github.io/blog/2024-01-30-llava-next/#results)（访问2026-10-31；[[raw/web/S024-LLaVA-NeXT/official-blog.html|本地HTML快照]]）。表中34B和13B同时变化主干，13B也改变数据与分辨率；不能据跨版本分数做单因素因果归因。MMMU13B并未提高，也不能用34B好成绩掩盖这个边界。

“超过Gemini Pro”限定在选定指标：该快照NeXT34B MMMU val51.1对47.9、MathVista46.5对45.2，但MM-Vet57.4低于64.3。不能概括成全面超过。表格明确区分specialist、监督微调、训练图像已见与zero-shot；HTML文本抽取会丢背景灰色含义，比较时应回到原始单元格属性，不能只据一列纯文本判所有行零样本。本文不重建完整异构排行榜。

博客未在此报告结果方差、逐任务人工判分对齐、全部prompt和API快照。其1.5参考分数也与S023论文表格有小差异（例如MM-Vet36.3 vs36.1、MMB-ENG67.8 vs67.7）；本页保持网页数字，不与论文数值静默混合，差异原因未确认。[Results](https://llava-vl.github.io/blog/2024-01-30-llava-next/#results)；[[raw/papers/models/llava/LLaVA-1.5.pdf#page=5|S023表4，PDF p.5]]。

SGLang被列为部署/推理支持，但博客没有相同硬件、batch、输出长度下的吞吐/延迟对照，不能将其作为本机效率已验证。网页中仍有“coming soon”，这是抓取文本的状态，不用它判断代码当前是否已发布，也未为此扩展访问外部仓库。

## 旧稿输入与修正

冻结输入：[[raw/notes/多模态经典/2024-LLaVA-NeXT总结.tex]]、[[raw/notes/多模态经典/Latex_out/2024-LLaVA-NeXT总结.pdf]]；本次对照TeX正文，排版副本未逐页核查。

旧稿“分辨率提高4倍”改成4倍像素；224块只属于旧HD例子，此版按Model Card写336；“改变比例”扩成可核的数据替换/新增；“34B超过Gemini-Pro”补选定指标和反例。旧稿总结“每代视觉编码器、连接器、LLM都更强”删除：博客明确复用连接器且视觉参数规模相同，没有逐项能力因果证据。团队也不能缩成单一Microsoft Research归属。

本库整合：视觉主题比较固定336、224-HD和336-AnyRes；训练/评测主题登记训练图像重叠与删除TextCaps的动机；模型主题按组件、数据、预算、来源版本分别组织。实际共享主题关系见页末。

## 实际整合关系

支撑336-AnyRes有限网格、GPT-4V及任务数据变化、模型卡预算；HTML按固定快照解释。

- [[wiki/vision/Resolution-and-Token-Budget|分辨率、packing与tiling：预算到底在哪个位置？]]。
- [[wiki/training/Supervision-and-Stages|监督与阶段：数据、目标、开放参数和预算如何一起改变？]]。
- [[wiki/models/Family-Changes|家族变化轴：输入、接口、数据和计算怎样共同演进？]]。
- [[wiki/efficiency/Resource-Ledger|资源账本：视觉token、激活参数、KV与系统预算分别省在哪里？]]。
