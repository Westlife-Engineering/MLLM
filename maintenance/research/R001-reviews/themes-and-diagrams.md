# R001 G 学术审查：主题综合、地图与两张机制图

审查者：独立 G（Astra/high）；日期：2026-10-31。使用 academic-researcher、pdf；对自建评测的测量对象与判分有效性使用 benchmark-paper-reading；图的语义审查遵循项目 presentation 与 excalidraw-diagrams。没有派发子代理。本报告是学术与图解语义审核，不替代 F 的数学/Mermaid 渲染、H 的结构验收或主 Agent 的整体交付验收。

## 结论与真实范围

已全文阅读全部 **18 个 overview/topic 页面**，独立查看最终 **2 张 PNG**，读取两份 `.excalidraw` 的文本、分区和全部 **17 根箭头**（9+8），并核对图旁 caption、来源身份与正文关系。以原文回读检验跨来源综合，没有以来源首稿、作者交接或“前一组通过”替代本次审核。

发现 **3 项必须修正的证据定位问题**，均由主 Agent 修复并经最终差异回核关闭；另提出 **2 处地图导航补充**，也已落实。当前未关闭 must-fix 为 **0**。主题与图在本报告覆盖范围内通过学术审核。未发现需要改公式、Mermaid 或两张图语义的错误。

这里的“通过”表示关键解释与比较边界可回证，不表示逐条复算所有论文表格、完整审计评测代码、重做实验或验证所有外部链接历史状态。Obsidian 内显示未测。没有运行模型、官方代码、benchmark 或递归扩展参考文献。

## 逐页检查与判定

每页均读完整正文、公式/图示说明、来源入口与限定。下表列实质检查对象，而非机械按每页凑相同条数；“支持”同时包含作者原述可回证、教学推导边界明确这两种情形。

| 页面 | 核查的关键机制、综合关系与条件 | 判定及主要原文定位 |
| --- | --- | --- |
| `wiki/overview.md` | 总览以问题和机制导读；视觉接入不被限定为统一三段流水线；观察反馈环被标为可选教学重组；票据例子区分像素、接口与任务成功 | 支持。S014 pp.3–4；S016 pp.4–6；S021 pp.3–5；S002 pp.26–28。没有把地图或教学例子算为新增实验 |
| `wiki/foundations/Formalization.md` | 条件概率分解是教学形式；连续视觉位置与离散预测目标分开；权重共享、可见性与路由分开；冻结不等于无前向或无输入梯度；目标名不等于训练阶段 | 支持。S014 pp.3–6；S015 pp.3–5；S017 pp.3–4；S021 pp.3–5。对一般 dense attention/KV 的公式假设没有冒充所有结构 |
| `wiki/vision/Overview.md` | 监督要保存的信息与输入预算联合决定可用表示；SoViT 形状分配、NaViT batch组织、AIMv2 native适配是不同轴；视觉分辨率与LLM序列长度可分离 | 支持。S005 p.8；S006 pp.2–5；S007 pp.3–5；S026 pp.3–4；S031 p.10；S032 p.5 |
| `wiki/vision/Objectives-and-Transfer.md` | softmax双向归一化与SigLIP逐对logistic不同；监督并非逐patch与词的一对一真值；SigLIP2区域/局部/掩码监督与加入时间区分；AIMv2 prefix视觉与causal多模态decoder职责；probe与全调条件 | 支持。S009 p.3公式与Fig.1；S010 pp.3–5；S007 pp.3–5；S005 p.8。没有把多种目标当多个必然阶段，也未以异协议分数排统一榜 |
| `wiki/vision/Resolution-and-Token-Budget.md` | native保比例、packing、有限grid tiling、固定query与空间合并不同；整批patch预算不保证总FLOPs恒定；Qwen各代位置机制、DeepSeek通道/tiles/OCR压缩区别；VL2公式中的全局、局部、换行位置 | 支持。S006 pp.2–5；S007 p.4；S010 pp.4–5；S024 HTML Dynamic High Resolution及原PNG；S026–S028方法页；S031 p.10；S032 p.5；S033 pp.5–12。图见后文 |
| `wiki/architecture/Overview.md` | 参数复用、token可见性、信息路由与输出接口四轴；共享attention不自动造成分别前向图文交互；直接网格/query双路与DeepStack正确；新序列记忆专题可从地图进入 | 支持；导航补充已闭环。S014 pp.3–4；S015 p.4 Fig.3；S025 p.5 Fig.4；S028 pp.3–4 |
| `wiki/architecture/Visibility-and-Connections.md` | VLMo底层联合attention已可融合，不待顶部VL-FFN；BLIP各模式共享范围与mask；CoCa前后decoder及级联pooler；Flamingo内部CA、BLIP-2前缀、LLaVA逐位置投影；BLIP-2下游VQA也可问题条件化 | 支持。S014 p.3 Fig.1及pp.4–6；S012 p.3；S013 pp.4–5/12；S016 pp.4–6/24；S017 pp.3–4/7；S022 pp.4–5；S023 pp.3–4。图见后文 |
| `wiki/architecture/Generative-Output-Interfaces.md` | 输入视觉表示、文本/坐标输出、图像生成条件与扩散像素输出分工；MiniGPT-5输入32和输出8位置不同；冻结U-Net仍可传递条件梯度；caption-free范围；生成接口不自动是世界反馈推理 | 支持。S015 p.4及caption协议；S021 pp.3–5/12–15；S002 pp.30–31为展望身份。FID与人物纹理/身份保持的边界正确 |
| `wiki/architecture/Sequence-Memory-and-Retrieval.md` | GDN状态与误差修正；QSA mean key/max teacher、因果完整块与tail、原始token回读、仍二次索引项；CSA2 cache/索引共享区别；GR残差存储与参数ngram记忆不同；S030语言报告范围 | 支持；Fig.5页段定位已修。S030 p.4 Eqs5–10、pp.5–9 Eqs12–20/Fig.5、pp.10–15；S034 pp.10–12。r=4/i=6算例从mask推得且明确教学身份；未偷读未来块 |
| `wiki/training/Overview.md` | 数据/目标监督位置/开放参数/预算四列；监督内容与路径不同；BLIP-2下游视觉解冻、VL与VL2 alignment不同、InternVL第二阶段视觉冻结 | 支持。S011 pp.4–5；S012 pp.3–4；S017 pp.4/7–8；S025 p.6；S031 pp.12–16；S032 pp.9–10。没有把训练冻结表静态推广到所有任务 |
| `wiki/training/Supervision-and-Stages.md` | EMA软目标与CapFilt数据重构；BEiT随机缩放初始化不等于载入BEiT权重；Owl阶段2原文冲突保留；DeepSeek两代模态比例；Qwen阶段/上下文课程；reward、verifier与环境的职责 | 支持；S031 Table1页码已修。S011 pp.4–5；S012 pp.3–4/6；S015 p.5脚注4；S020 pp.4–5及原文冲突；S031 pp.6–7/13–14；S032 pp.6/9–10；S028 pp.4–13；S034 pp.25–32 |
| `wiki/efficiency/Overview.md` | token、参数、KV、长度、工具与墙钟分账；形状、样本曝光与分块矩阵没有共同分母；VL2型号限定；V4.1持久缓存与近似重放边界 | 支持。S005 p.8；S006 pp.4–5；S009 pp.3–4；S032 p.5；S034 pp.19–20；S025 p.11。未把编码吞吐当聊天延迟 |
| `wiki/efficiency/Resource-Ledger.md` | dense计算和KV式假设；总/激活/可训练/外部表参数区分；S030 kernel预算不等于端到端；V4.1 CED、CSA2、global KV、持久SWA重放各省不同对象；OCR输入压缩仍有输出成本 | 支持。S029固定config；S030 pp.8–9/14–15/22–23；S034 pp.7–14/19–20；S033 pp.7/10–12；S005 p.8。890 bytes/token只限global KV、bounded replay近似、1/8持久化范围未混淆 |
| `wiki/reasoning/Overview.md` | 增加计算/新增观察/改变环境三类资源；裁剪工具训练与目标调用次数；坐标/执行结束/虚拟终态分开；effort长度惩罚及非单调准确率；长序列/OCR不是推理成功证明 | 支持。S002 pp.26–28；S003 p.81课程图；S027 pp.10/13/46；S028 pp.12–13/15/25；S034 pp.29–30/49–51；S030 pp.22–23。长度奖励公式与条件性解释一致 |
| `wiki/evaluation/Overview.md` | 任务、成功观察、输入预算共同定义分数；答案/解释/动作/终态分离；zero-shot、probe、harness与effort附条件 | 支持；S028节号传播错误已修。S002 pp.26–28；S022 pp.6–9；S013 p.9；S011 p.6；S015 p.16；S007 p.5；S005 p.8；S028 p.25 §5.12.3 |
| `wiki/evaluation/Judges-and-Task-Success.md` | 文本教师、参考生成、评分裁判、系统组合器与reward judge不同；人评小集合与参考覆盖的测量边界；OCR/NIAH/patch similarity不冒充推理或执行成功；sample数量与Pass@k不同；multi-agent墙钟不等于总预算 | 支持。S019 pp.6–8/15；S020 p.6；S021 pp.6–7/13–15；S022 pp.6–9；S028 pp.20/25；S030 pp.22–23脚注1；S033 pp.10–12；S034 pp.33–36/47–48。作者自建评测仅在报告的协议内解释 |
| `wiki/models/Overview.md` | 家族是定位入口，变化轴才是可比较对象；官方文档与语言架构报告单列；范围外课程工作与综述展望未升格直接证据 | 支持；S030原文与唯一入口补链已闭环。S024官方HTML、S029固定卡/config、S030 pp.2/22–23；其余模型证据见前组原页审查范围 |
| `wiki/models/Family-Changes.md` | 家族演进不作单因素因果解释；LLaVA普通336与HD/AnyRes；Qwen固定256、动态merge、DeepStack及S029/30身份；VL通道与VL2位置；OCR领域任务与V4.1系统；InternVL直接/query双路 | 支持。S022–S034前组已独立核过的对应方法/训练/表格原页用于本次逐段综合比较，并补查S031 p.7。没有把Qwen3.7-Plus-Base当S029后训练，也未从S030补造视觉架构或分数 |

## 跨来源解释与教学推导的专项结论

- **共享与可见性：**VLMo Fig.1、BEiT-3 Fig.3的联合分支在下层便拼入图文，顶部VL-FFN改变专家路径；双塔分别前向仍不跨模态读取。主题没有用“共享attention”替代mask和输入条件。
- **接口与预算：**BLIP-2的32 queries、Flamingo的64 resampler slots、Qwen-VL的256 queries不被解释成规则patch网格。LLaVA逐位置MLP改变通道，不自动压缩位置；InternVL直接与query双路也保留。NaViT定长容器、AIMv2整批面积×batch、NeXT单图局部+全局各有不同固定边界。
- **目标、阶段与梯度：**ALBEF联合目标、EMA KL软监督，BLIP CapFilt生成/筛数据，BEiT-3 MDM，BLIP-2两阶段与下游解冻均独立解释；没有把“采用caption目标”泛化为所有组件被更新。冻结扩散模型仍可向输入条件反传的解释是数学推断，未声称训练所有扩散权重。
- **S030正面方法：**状态递推的遗忘/误差修正、QSA索引与原内容读取、GR可读写残差流和ngram参数查表都有实质信息流解释。固定r下O(n²/r)未误称线性；mean与max目的不同。语言骨干主结果保留base身份、额外host表与kernel条件。
- **S034正面方法：**CED减少长输入prefill，CSA2区分Full/Reindex/Reuse，低比特global KV与局部SWA持久化策略分开；effort通过长度惩罚调整成本偏好而非硬上限。准确率文字概括与曲线非单调情况保留，没有把附录条件推导写成普遍定理。
- **测量与终态：**LLaVA-Bench文本裁判复评分散小不等于人类一致性；ScienceQA92.53是组合系统；MiniGPT-4随机单caption覆盖与幻觉可并存；OCR转写、NIAH检索、SWEBench-Pretrain patch序列相似都没有升级为一般推理/执行成功。172个golden任务、Almost@1门槛与wall-clock的多agent比较保留筛选和预算限制。
- **来源关系：**实质主体以来源定位支撑，然后链接唯一页；来源入口通常可在正文找到具体机制或条件用途。两处新专题/来源地图遗漏已补。HTML与固定README/config没有伪造论文页码；旧TeX/MD未成为论证依据。

## 两张图的独立检查

### visual-entry

实际查看初版PNG以及F从持久源重渲染后的最终PNG；最终为2200×2649。源含65个未删除元素、9根箭头。逐一检查视觉编码器→resampler/query/projection、视觉K/V与语言Q进入gated CA、CA→原LM块、FC→视觉前缀、逐位置投影→网格位置等方向与端点。

Flamingo内部接入和主训练冻结边界得到S016 pp.4–6支持，最近前图mask还回查p.24 Fig.7；BLIP-2两阶段和OPT/FlanT5区别得到S017 pp.3–4支持；LLaVA/1.5冻结表与逐位置接口依据S022 pp.4–5、S023 pp.3–4。箭头定义为表示/隐状态传递，不被误认作反向梯度或模型性能因果。图旁和图内均标为本库机制综合，来源图未被重绘替代。无must-fix。

### resolution-boundaries

实际查看初版PNG以及最终PNG；最终为2200×2825。源含80个未删除元素、8根箭头。NaViT分样本隔离、独立pooling和padding loss屏蔽与原文pp.2–5一致；mask限制可见性不自动证明dense算子跳过所有乘法。AIMv2 p.4的C=AᵢBᵢ与保比例/padding一致；4×3=2×6明确为教学计数，非原实验batch与真实FLOPs承诺。NeXT一张图展开局部tiles与缩小全局图，二者分别编码再接LLM；没有画成NaViT多独立样本打包。S024保持2026-10-31官方快照身份，未称获得2024年原始网页字节。图中面积/方块不代表真实token计数，不能据方块数推LLM长度。无must-fix。

## 实际原文回查与未覆盖部分

本次新/补回读的重点正文页：S002 pp.26/28；S003 p.81；S005 p.8；S006 pp.2–5/20；S007 pp.3–5；S009 p.3；S010 pp.3–5；S011 pp.4–6；S012 pp.3–4/6；S013 pp.4–5/9/12；S014 pp.3–6；S015 pp.3–5/16；S016 pp.4–6/24；S017 pp.3–4/7–8；S019 pp.6–8/15；S020 pp.4–6；S031 pp.6–7。对于图表/公式，实际打开渲染图而非仅提取文字的本轮页包括：S002 p.26/28、S003 p.81、S005 p.8、S006 p.2、S007 p.4/5、S009 p.3、S011 p.4、S014 p.3、S015 p.4、S016 p.5、S017 p.3。渲染后未打开的PNG不计已目视检查。

S021–S034原页审查范围复用自本审查者刚完成的 `models-and-generation.md`，本次重新逐段判断主题如何组合这些证据，特别是S029固定文档/S030语言骨干/S034系统成本的跨来源解释。前组已实际查看的关键公式、图表与HTML/JSON/PNG可回用，但没有将“前组通过”作为逻辑证明。未重新逐页读全部34来源；S001/S004/S008/S018的完整来源审查不属于本轮重新通读范围，涉及它们的地图和主题只作关键综合条件审查，未声称重新完成所有原表复核。原始身份与hash以registry的固定版本为准；本轮主题hash和图hash见下。

## 问题闭环与最终差异

| ID | 发现与最小修法 | 回核结论 |
| --- | --- | --- |
| T-G01（must-fix） | Supervision-and-Stages把S031 Table1标为p.6；p.6仅引表，表体实在p.7 | 已改anchor与标签为p.7；唯一来源页同时拆成p.6 §2.1与p.7 Table1邻近定位。再次核原文和修订行，关闭 |
| T-G02（must-fix） | Sequence-Memory的QSA段以pp.6–8包含Fig.5，原图在p.9 | 已扩为pp.6–9；公式/因果算例未变。回核修订，关闭 |
| T-G03（must-fix） | evaluation/Overview把Qwen3-VL p.25标§6.3，实际§5.12.3；深专题原已正确 | 已改§5.12.3。与前组p.25原页证据相符，关闭 |
| T-N01（地图补充） | architecture/Overview入口表漏Sequence-Memory新专题 | 已添加固定状态、KV检索、残差流和参数查表导航；无新增未经论证断言，关闭 |
| T-N02（地图补充） | models/Overview提Next但没有S030原文/唯一页入口 | 已补raw来源、p.2/pp.22–23定位与唯一页入口；语言报告限定保留，关闭 |

已比较初始22文件快照与最终内容：正文变化仅上述5个Markdown页面的定位/导航修补；另2张PNG由持久源离线重渲染，独立再看后语义一致；2份可编辑源没有变化。其他13个Markdown页面与初始快照字节一致。初始snapshot已包含E的图嵌入与本轮所见Mermaid方向，不能把F先前的LR→TB修改计作本次新发现。没有未经回核的最终学术改动。

## 最终文件校验值

以下SHA-256固定本报告审查的最终字节；hash只表明字节身份，不替代内容证据。初始快照、逐文件diff与最终manifest保存在本任务Temp/review/themes用于恢复；长期校验值保存在本节。

| 文件 | 最终SHA-256 |
| --- | --- |
| `wiki/overview.md` | `d85a9e42cc2580574631327da60a99237518f7b43881a34f823fde51e727ec12` |
| `wiki/architecture/Generative-Output-Interfaces.md` | `18253ebaa50b62ce30346ad99b9151d2b53ff5ce0cfe395d5aaff2d74fecd78e` |
| `wiki/architecture/Overview.md` | `c189d8c82a3878d07b96ff76ce36dd6cd51bfbe07e8ad7a22ce0e3b71e4cdd2f` |
| `wiki/architecture/Sequence-Memory-and-Retrieval.md` | `f96724eb30a9fe9b37b50a63aa9e13e4496a268b7291761903a1e0d8486303e3` |
| `wiki/architecture/Visibility-and-Connections.md` | `d060a1bb71f3c4749ff08cdbc5197bedb0ee15dd52f007f05b9d10a9c4388292` |
| `wiki/efficiency/Overview.md` | `821d9a2e4d2cd023246cac6143c1955cfef7d5980fb6717e1076b13a2881e4ae` |
| `wiki/efficiency/Resource-Ledger.md` | `664f8a72a84565d02553897f5c665b2ac8517617713f8abd2ebd38675bd7b40d` |
| `wiki/evaluation/Judges-and-Task-Success.md` | `96fc335940b44c35d95a9134c8ab58b7153c73d2ee6c6d6acfff2a7540828dc5` |
| `wiki/evaluation/Overview.md` | `ed230131160d44ea5c9ca8efb2cd9023f218c912d3c750fef5e3ebefc4a76d42` |
| `wiki/foundations/Formalization.md` | `c0b8d4fb51865a8c6b60d41c09fe4fed9fc800147ad32830b20ad98fe7fa7b08` |
| `wiki/models/Family-Changes.md` | `2f831794d6dbc7a0ab625e0924c3ec4cb12a54cf58ea67355b2cc31e8791cad7` |
| `wiki/models/Overview.md` | `275c84a9700407e6d08f9d715776dab18f7256b4596e54ef32898b831418ac64` |
| `wiki/reasoning/Overview.md` | `5cd7c4f72aca1aef326d052200d35b02d1573ead6920927834cf8a453cf6988a` |
| `wiki/training/Overview.md` | `3be6eb665701ab352c4d7bb66a6b6ede1feb3ff04612be206bebb8f6b3932867` |
| `wiki/training/Supervision-and-Stages.md` | `68139ffae629a46ba62110ddafbf7a869d36b3902875de9477c0f98ba3aae63b` |
| `wiki/vision/Objectives-and-Transfer.md` | `a6d3434292fab5e781257e8b96f4012a33df453467a61a8d7f5f6f7b573b7fb9` |
| `wiki/vision/Overview.md` | `d1dbe34d750a224c95ced7e1c7bd5fc77fc7ef7b145f27f177008bb84d2634df` |
| `wiki/vision/Resolution-and-Token-Budget.md` | `83ab246a6bc3b37b05fb5979d68e3c8cd03abe5c885b28f7ce7aac8c9cd461f5` |
| `wiki/assets/diagrams/visual-entry/visual-entry.excalidraw` | `f1a2b11708e8d81e9cc907fc887670bf14dd7e4d4b62ce4e9d0415fd7376d186` |
| `wiki/assets/diagrams/visual-entry/visual-entry.png` | `731a7c467ade38257038000f7561f2a7c6578ffa17a8558bc76d893a401b31c6` |
| `wiki/assets/diagrams/resolution-boundaries/resolution-boundaries.excalidraw` | `7133a549db82e88c4aa49000737c3b7a0b071b619c59ececef2bf6c8b8831689` |
| `wiki/assets/diagrams/resolution-boundaries/resolution-boundaries.png` | `837edc41b5e0b484397a5083b9ddebdf721a0315aab08da312a514ca572da175` |
