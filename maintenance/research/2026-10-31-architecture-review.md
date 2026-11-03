# 2026-10-31 架构方案审核与实施记录

> 2026-11-03 状态补充：用户明确要求删除根目录实施方案及 Raw 原始提案；本页继续保存已实施的决策和证据定位。删除后当前 Raw 为288份；下文289份及未提交的验收状态属于2026-10-31历史快照。撤下与提交准备见[[maintenance/research/2026-11-03-proposal-withdrawal|本次维护记录]]。

## 范围、基线与决策责任

用户要求审核未实施的架构提案，合理修改、不合理保留现状，并指定可用 gpt-6.1-sol / high 协助细节；所有核心判断和修改由主 Agent 完成。使用三名只读 subagent 核查视觉/骨干、接口/模型、工程迁移细节，未给予仓库写权限，未再派发。

开始时 Git HEAD 为 `1f4705869bef5f3d09cb5a063e0efe60e72b2ea9`，跟踪文件干净，只有原始提案未跟踪。修改前 strict 为0错误/0警告。288份Raw，共320669809字节；34来源、31去重学术身份、52知识页，registry有141条已登记关系。

原始提案SHA-256为 `bd0ed4665fa9a65d093e41f5370489f995e8188ad2313dee2b5213b1ce98b539`，56001字节；当时冻结为 `raw/articles/2026-10-31-MLLM知识库架构调整方案-原始提案.md`，现已按用户明确要求删除，见[[maintenance/research/2026-11-03-proposal-withdrawal|撤下记录]]。其内部旧路径和“待确认”描述是历史材料，不再作为生效规则。初始保全清单见[[maintenance/research/2026-10-31-architecture-baseline.json|基线]]，已采用的决策由本页、34项决策表及现行目录规则继续保存；根目录实施方案已撤下。

## 主 Agent 的取舍

- 采用视觉表示合并、多模态骨干重命名、视觉/生成/语言接口分开、五篇指令/对话适配归训练、OCR归有任务边界的上下文压缩。来源页新增本库归属理由及原文定位；源文实验、冻结冲突与能力限制保持。
- 保留联合系统的家族目录，Flamingo继续归视觉接入，现有18个总览/主题不拆页。家族/组件导航在模型总览补一节；不把作者有完整系统和多任务评测当成迁到系统目录的充分条件。
- 保留registry v1；仅增加现用方向词表，明确交叉导航与实质使用不是同一字段。不引入全量coverage/topic_relations/任务/模态/家族字段。来源覆盖和使用可用有定位的正文/小表表达。

这些是本库的导航决策，原文用于限定研究对象和解释范围，不证明唯一目录。下表只列本次实际移动的23项；其余11项（含3份地图材料）保持原位，不代表未审核其系统/类型边界。

## 逐项移动与证据理由

| ID与唯一页 | 原方向 → 现方向 | 主 Agent 采用的理由与原文定位 |
| --- | --- | --- |
| S004 · [[wiki/papers/vision/representation/ViT\|ViT]] | `vision/encoders` → `vision/representation` | patch Transformer 的主要复用对象是视觉编码与迁移表示；分类任务是其验证方式。 [[raw/papers/vision/representation/ViT.pdf#page=3\|PDF §3.1/Fig.1]] |
| S005 · [[wiki/papers/vision/representation/SoViT\|SoViT]] | `vision/encoders` → `vision/representation` | 以视觉模型形状为主入口；固定计算下的 shape 优化是主要贡献，效率主题继续承担强入口，不能将其降为附带收益。 [[raw/papers/vision/representation/SoViT.pdf#page=2\|PDF pp.2–4，贡献/§3]] |
| S006 · [[wiki/papers/vision/representation/NaViT\|NaViT]] | `vision/encoders` → `vision/representation` | 原生分辨率、packing、位置与样本隔离共同改变视觉编码组织；训练组织和资源折中仍在主题页解释。 [[raw/papers/vision/representation/NaViT.pdf#page=2\|PDF pp.2–4，Fig.2/§2]] |
| S007 · [[wiki/papers/vision/representation/AIMv2\|AIMv2]] | `vision/encoders` → `vision/representation` | 目标是强视觉 encoder；多模态 decoder 服务预训练，不因此将来源主归图像生成接口。 [[raw/papers/vision/representation/AIMv2.pdf#page=2\|PDF pp.2–3，§2.1–2.2/Fig.1]] |
| S008 · [[wiki/papers/vision/representation/CLIP\|CLIP]] | `vision/alignment` → `vision/representation` | 包含视觉与文本两侧的成对表示及文字分类接口，不能将 representation 理解成只有视觉塔。 [[raw/papers/vision/representation/CLIP.pdf#page=2\|PDF pp.2–4，Fig.1/§2]] |
| S009 · [[wiki/papers/vision/representation/SigLIP\|SigLIP]] | `vision/alignment` → `vision/representation` | 按图文表示对象归类；逐对损失和分块实现是主要方法，训练与效率解释保留，不推广为所有 loss 论文都归视觉。 [[raw/papers/vision/representation/SigLIP.pdf#page=2\|PDF pp.1–3，Algorithm1/§3]] |
| S010 · [[wiki/papers/vision/representation/SigLIP2\|SigLIP2]] | `vision/alignment` → `vision/representation` | 全局、局部与密集表示是复用对象；辅助 decoder 仅服务表示学习且不在发布模型中。 [[raw/papers/vision/representation/SigLIP2.pdf#page=3\|PDF §2.2–2.3]] |
| S011 · [[wiki/papers/architecture/multimodal-backbones/ALBEF\|ALBEF]] | `architecture/pretraining` → `architecture/multimodal-backbones` | 保留独立对齐与融合编码接口；MoD/EMA 的训练贡献仍由训练主题解释。 [[raw/papers/architecture/multimodal-backbones/ALBEF.pdf#page=3\|PDF pp.3–4，Fig.1/§3]] |
| S012 · [[wiki/papers/architecture/multimodal-backbones/BLIP\|BLIP]] | `architecture/pretraining` → `architecture/multimodal-backbones` | 以 MED 的独立、条件编码及条件解码接口为主入口；CapFilt 是并列主要贡献，不能因目录选择而降格。 [[raw/papers/architecture/multimodal-backbones/BLIP.pdf#page=2\|PDF pp.2–4，Figs.2–3/§3]] |
| S013 · [[wiki/papers/architecture/multimodal-backbones/CoCa\|CoCa]] | `architecture/pretraining` → `architecture/multimodal-backbones` | 独立文本表示与视觉条件解码同时保留；按多模态骨干组织，避免把双塔、融合和生成当互斥身份。 [[raw/papers/architecture/multimodal-backbones/CoCa.pdf#page=4\|PDF pp.4–5，Fig.2/§3.2]] |
| S014 · [[wiki/papers/architecture/multimodal-backbones/VLMo\|VLMo]] | `architecture/pretraining` → `architecture/multimodal-backbones` | 共享 attention 与模态专家支持多种运行模式；共享骨干不表示全部参数共享。 [[raw/papers/architecture/multimodal-backbones/VLMo.pdf#page=3\|PDF pp.3–5，Figs.1–3/§3]] |
| S015 · [[wiki/papers/architecture/multimodal-backbones/BEiT-v3\|BEiT-v3]] | `architecture/pretraining` → `architecture/multimodal-backbones` | Multiway 骨干可经任务适配用于独立、融合与条件接口；不宣称未经适配的一套权重直接完成全部任务。 [[raw/papers/architecture/multimodal-backbones/BEiT-v3.pdf#page=3\|PDF pp.3–4，Figs.2–3/§2]] |
| S016 · [[wiki/papers/architecture/visual-interfaces/Flamingo\|Flamingo]] | `architecture/connectors` → `architecture/visual-interfaces` | 保留视觉接入主归属：Resampler 与插入冻结 LM 的 gated cross-attention 已能组织核心接口论证。交错数据、few-shot 协议与模型家族共同贡献保留；不因完整系统存在而迁入系统目录。 [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=4\|PDF pp.4–6，贡献/§2/Figs.3–4]] |
| S017 · [[wiki/papers/architecture/visual-interfaces/BLIP-2\|BLIP-2]] | `architecture/connectors` → `architecture/visual-interfaces` | Q-Former 桥接冻结视觉与语言骨干是核心复用接口；两阶段预训练是桥接方法的核心组成，不同 LLM 接法保留为具体实现与验证条件。 [[raw/papers/architecture/visual-interfaces/BLIP-2.pdf#page=3\|PDF pp.3–4，§3/Figs.2–3]] |
| S018 · [[wiki/papers/training/instruction-adaptation/InstructBLIP\|InstructBLIP]] | `architecture/connectors` → `training/instruction-adaptation` | 主要研究视觉指令适配及未见任务泛化；指令条件化视觉提取与采样是实质方法，冻结 LLM 不改变其训练研究身份。 [[raw/papers/training/instruction-adaptation/InstructBLIP.pdf#page=3\|PDF pp.3–5，贡献/§2/Fig.3]] |
| S019 · [[wiki/papers/training/instruction-adaptation/MiniGPT-4\|MiniGPT-4]] | `architecture/connectors` → `training/instruction-adaptation` | 归宽口径的指令/对话输出适配：复用冻结视觉桥与 Vicuna，仅训练线性投影，并用高质量详细描述改善输出。与更新 LLM 的 LLaVA 不视作同一算法。 [[raw/papers/training/instruction-adaptation/MiniGPT-4.pdf#page=4\|PDF pp.4–5，§3.1–3.3；Fig.1见p.2]] |
| S020 · [[wiki/papers/training/instruction-adaptation/mPLUG-Owl\|mPLUG-Owl]] | `architecture/connectors` → `training/instruction-adaptation` | 模块化训练、视觉侧开放参数与联合指令适配是主线；abstractor 仍在架构主题解释，第二阶段冻结描述的原文冲突不因迁移消失。 [[raw/papers/training/instruction-adaptation/mPLUG-Owl.pdf#page=4\|PDF pp.3–5，§3/Figs.1–2]] |
| S021 · [[wiki/papers/architecture/generative-interfaces/MiniGPT-5\|MiniGPT-5]] | `architecture/generation` → `architecture/generative-interfaces` | 核心新增运行接口是 vokens/mapper 将 LLM 输出接到图像生成条件；输入图像特征、caption 和输出图像条件分开。 [[raw/papers/architecture/generative-interfaces/MiniGPT-5.pdf#page=3\|PDF pp.3–5，§3/Fig.2]] |
| S022 · [[wiki/papers/training/instruction-adaptation/LLaVA\|LLaVA]] | `models/llava` → `training/instruction-adaptation` | 视觉指令数据构造与训练是主要问题；轻量投影用于开展 data-centric experiments，保留模型与评测贡献。 [[raw/papers/training/instruction-adaptation/LLaVA.pdf#page=4\|PDF pp.3–5，§3–4/Fig.1]] |
| S023 · [[wiki/papers/training/instruction-adaptation/LLaVA-1.5\|LLaVA-1.5]] | `models/llava` → `training/instruction-adaptation` | 数据、响应格式、输入与 MLP 改动共同回答视觉指令适配配方问题，按训练入口组织；承认联合系统也是合理候选，不把联合提升归给单因素。 [[raw/papers/training/instruction-adaptation/LLaVA-1.5.pdf#page=3\|PDF pp.1–4，§3/Tables1–2]] |
| S025 · [[wiki/papers/architecture/multimodal-backbones/InternVL\|InternVL]] | `models/internvl` → `architecture/multimodal-backbones` | InternViT 与 QLLaMA 保留独立表示、对齐和条件生成接口，按多模态骨干组织；Chat/SFT 的系统线仍有家族入口，InternViT 不另计论文身份。 [[raw/papers/architecture/multimodal-backbones/InternVL.pdf#page=4\|PDF pp.4–6，§3/Figs.3–4]] |
| S030 · [[wiki/papers/architecture/language-backbones/Qwen3.8-Flash-Next\|Qwen3.8-Flash-Next]] | `models/qwen` → `architecture/language-backbones` | 报告组织语言序列结构、成本与训练稳定性，作为 MLLM 邻接机制证据；家族名不构成视觉验证。 [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=1\|PDF pp.1–3、22，§1–2/§4–5]] |
| S033 · [[wiki/papers/efficiency/context-compression/DeepSeek-OCR\|DeepSeek-OCR]] | `models/deepseek` → `efficiency/context-compression` | 主问题是视觉文本压缩与恢复的资源折中；直接证据限 OCR/文档解析，不能由 context-compression 目录推成一般长上下文推理已验证。 [[raw/papers/efficiency/context-compression/DeepSeek-OCR.pdf#page=3\|PDF §1；p.19 §6 明确限制]] |

## 关系审核：纠正登记，不批量制造使用

主 Agent 回读目标正文后采用以下四项校正：

| 来源 → 主题 | 决定 | 定位和理由 |
| --- | --- | --- |
| S001 → 训练总览 | 补实质关系 | 综述pp.18–19 §5/Fig.14；正文用它组织阶段、开放参数与监督位置。 |
| S002 → 评测总览 | 补实质关系 | 综述p.32 Fig.10、p.41 §5.5；正文分开任务对象与判分。 |
| S003 → 可见性与连接 | 补实质关系 | 讲义p.74 CogVLM图；专门参数与联合attention的具体反例，仍为讲义转述。 |
| S004 → 基础形式化 | 移除实质关系 | 本轮现稿只有frontmatter和来源入口链接，无正文论证作用；同时移除该页的ViT证据列表项。 |

S002→生成输出接口保留：原文p.30 §4.3/Fig.9是展望，目标页用它限制从具体输出接口推出完整native reasoning的推论。使用深度取决于论证作用，不能因为证据是作者展望就自动降为background。原文身份仍是综述转述/作者展望。

新登记数为143。正文引用差集只作为人工候选；Overview概括、旁引和导航不自动增加integrated关系。此次不是对全部关系贡献深度的逐条重验，原“141条实质关系”的历史措辞保留，日志追加计数口径更正。

## 本轮实际核查范围

| 承担者 | 核查内容 |
| --- | --- |
| 主 Agent | live规则、完整方案、索引/registry、相关主题/来源页、检查器和测试；直接核PDF：S010 p.3，S013 p.4，S016 pp.4–5，S018 pp.3–4，S019 pp.4–5，S020 pp.3–4，S023 pp.1/3，S025 pp.4–5，S030 p.1，S033 pp.3/19；地图材料S001 pp.18–19，S002 pp.30/32/41，S003 pp.74–75/81。实际看图：S016 p.5、S025 p.5、S013 p.4、S020 p.4、S001 p.18、S002 p.30、S003 pp.74/81。 |
| 视觉/骨干核验 subagent，gpt-6.1-sol/high | S004–S010主要pp.1–5、S011–S015主要方法/贡献pp.1–5、S025 pp.1–6；实际看各篇关键结构页，指出SoViT/SigLIP的方法边界及InternVL系统线。 |
| 接口/模型核验 subagent，gpt-6.1-sol/high | S016 pp.1/4–6/8；S017 pp.1–4；S018–S020主要pp.1–5；S021 pp.1/3–5；S022 pp.1–2/4–5；S023 pp.1–4；S030 pp.1–3/22–23；S033 pp.1/3–7/10/19。实际查看12张关键图页。 |
| 工程核验 subagent，gpt-6.1-sol/high | 规则、源码、测试、registry、历史清单和主题正文；只读检查当前接口并在主 Agent 修改后再次审查，独立构造临时反例。 |

未联网刷新版本、未追引文、未重审全部成绩/附录/代码、未复现模型。引用旧的read/complete只保留既有登记范围，本次定向回核不冒充新一轮全文精读。PDF与讲义回读分别使用academic-researcher/pdf/course-pdf-knowledge方法。

## 工具修改与独立复核返工

检查器先收全部Raw迁移，再沿链核各跳和终点；Wiki移动单列，历史维护文档逐份hash授权旧路径追溯，当前内容继续严格。新词表校验方向和入口；关系路径要求规范`.md`，目标类型/互链/重复受检；正文差集只输出候选。

首轮32项回归中，临时fixture使用Windows沙箱不支持的rename，5项在构造阶段失败；改成构造迁移后字节快照后32项通过。独立工程复核又发现两项可复现漏洞：不同同字节Raw可汇合到一文件、无扩展名与`.md`别名可重复计关系。主 Agent 独立确认并修复，新增对应负例，最终结果见下节。它们说明检查通过不能代替对保全约束的审查。

## 保全、回退与验收

迁移清单为[[maintenance/migrations/2026-10-31-architecture-review.json|Raw/Wiki逐文件记录]]，决策恢复点为[[maintenance/research/2026-10-31-architecture-decisions.json|34项决策表]]。Raw每项先验旧哈希、再移动、再验新哈希，目标存在即停止；全部路径解析至本库，检查重解析点。仅移除因此留下的空目录，不删除原件或旧包。

基线中的`protected_history`保存当时maintenance快照；其中`maintenance/source-registry.json`是本轮允许维护的活动登记表，其余历史文件冻结。日志只能追加，按初始长度核前缀哈希。Wiki移动检查点哈希记录本次最终页；其后修订不受旧文本哈希锁定，但历史身份必须沿同一source_id。

回退先停写，按映射核查并恢复原路径，用Git基线恢复本轮变更的可维护文件，先比较当前diff并保留后续用户修改。原提案仍保留在Raw；不采用整树覆盖、强制覆盖同名文件或刷新原件哈希。

验收状态：**完成本次架构审核与所采用调整。**

- 结构：最终strict为0错误、0警告；34来源、52知识页、143条已登记关系，检查31份TeX的165项静态依赖。历史链接报告20项：17项经迁移追溯，另3项为初始化已登记的冻结旧Markdown断链；当前内容不依靠历史例外。完整快照见[[maintenance/research/2026-10-31-architecture-validation.json|结构验收JSON]]。
- 工具：34项回归全部通过；新增覆盖迁移链、循环/分叉/同字节汇合、历史范围与定位、Wiki身份、词表、关系别名与正文候选扫描。`git diff --check`通过。
- 保全：原288份Raw、320669809字节逐项核验一致；新增仅56001字节用户原提案，现Raw289份/320725810字节。13份历史维护文件字节不变，日志原前缀hash一致；34来源身份、版本、读取状态不变。详见[[maintenance/research/2026-10-31-architecture-preservation.json|保全报告]]。
- 学术：完成上列定向原文核验与最终分类段复核；全部决策由主Agent完成，未新增全文精读或实验声明。最终接口/模型复核无必须修问题；主Agent采纳BLIP-2两阶段训练是核心方法的措辞澄清。mPLUG-Owl p.4图中第二阶段abstractor的雪花由主Agent看原页确认，保留现有“摘要/引言与图/正文冲突”的表述，未采用子代理首轮对该图的误述。
- 表达与应用：4个现有图资产逐字节相同，539个数学片段和16个Mermaid块与基线文本一致；这是内容保全，不是本轮重新渲染验收。实际看过的原PDF图页见上表；Obsidian显示与跳转未测。

正文引用候选差集为81条，作为信息项保存，不是结构错误，也不是81条已确认遗漏。这些候选不自动构成错误，本轮未对其逐条作语义裁决，也未机械新增或降级；后续具体Query/主题修订时可逐项判断。当前143只表示登记总数。

本轮没有Git暂存、提交或push；HEAD保持基线。操作产物全部在本库，临时PDF渲染只用于本次核验，未建立长期过程目录。
