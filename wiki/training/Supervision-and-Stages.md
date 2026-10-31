---
type: topic
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/architecture/pretraining/ALBEF.pdf]]"
  - "[[raw/papers/architecture/pretraining/VLMo.pdf]]"
  - "[[raw/papers/architecture/pretraining/BEiT-v3.pdf]]"
  - "[[raw/papers/architecture/pretraining/CoCa.pdf]]"
  - "[[raw/papers/models/llava/LLaVA.pdf]]"
  - "[[raw/papers/models/qwen/Qwen-VL.pdf]]"
  - "[[raw/papers/vision/encoders/AIMv2.pdf]]"
  - "[[raw/papers/vision/alignment/SigLIP2.pdf]]"
  - "[[raw/papers/architecture/generation/MiniGPT-5.pdf]]"
  - "[[raw/papers/architecture/pretraining/BLIP.pdf]]"
  - "[[raw/papers/architecture/connectors/MiniGPT-4.pdf]]"
  - "[[raw/web/S024-LLaVA-NeXT/official-blog.html]]"
  - "[[raw/papers/architecture/connectors/BLIP-2.pdf]]"
  - "[[raw/papers/architecture/connectors/mPLUG-Owl.pdf]]"
  - "[[raw/papers/architecture/connectors/InstructBLIP.pdf]]"
  - "[[raw/papers/models/llava/LLaVA-1.5.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-VL.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-VL2.pdf]]"
  - "[[raw/papers/models/qwen/Qwen3-VL.pdf]]"
  - "[[raw/papers/models/internvl/InternVL.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-OCR.pdf]]"
---

# 监督与阶段：数据、目标、开放参数和预算如何一起改变？

训练阶段应写成四元组：**数据与采样、预测目标与监督位置、可更新参数、输入与累计预算**。两个模型都说“两阶段”并不代表学了同一件事；同一next-token loss既能学习图文接口，也能学习回答格式或工具行为。本页比较机制与训练条件，不把不同报告的数据量和分数直接排成效率榜。

## 目标先决定“什么错误会收到信号”

| 目标 | 直接被约束的对象 | 已核例子 |
| --- | --- | --- |
| ITC / sigmoid图文对齐 | 独立全局表示与候选配对关系 | CLIP/SigLIP；详见[[wiki/vision/Objectives-and-Transfer\|视觉目标]] |
| ITM | 图文融合后的匹配判定 | ALBEF/BLIP；难负例由相似度分布抽样 |
| MLM / MDM | 遮蔽位置的词或离散视觉目标 | VLMo、BEiT-3；mask token与causal attention mask不同 |
| 条件语言生成 | 给定输入下的后续文字或指定答案位置 | CoCa、LLaVA、Qwen-VL；任务格式决定哪些位置计loss |
| 像素/特征预测 | 图像内容或教师特征 | AIMv2归一化patch回归；SigLIP2 masked教师特征 |
| 扩散条件学习 | 条件特征能否帮助去噪恢复目标图 | MiniGPT-5的mapper；冻结生成主干仍传输入梯度 |

机制定位：[[raw/papers/architecture/pretraining/ALBEF.pdf#page=3|S011 · pp.3–5 §3.2–3.4]]、[[raw/papers/architecture/pretraining/VLMo.pdf#page=5|S014 · pp.5–6 §3.3]]、[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=4|S015 · pp.4–5 §2.2]]、[[raw/papers/architecture/pretraining/CoCa.pdf#page=4|S013 · pp.4–5]]、[[raw/papers/models/llava/LLaVA.pdf#page=5|S022 · p.5 §4.2]]、[[raw/papers/models/qwen/Qwen-VL.pdf#page=19|S026 · pp.19–20监督格式]]、[[raw/papers/vision/encoders/AIMv2.pdf#page=2|S007 · pp.2–3]]、[[raw/papers/vision/alignment/SigLIP2.pdf#page=4|S010 · p.4]]、[[raw/papers/architecture/generation/MiniGPT-5.pdf#page=4|S021 · pp.4–5]]。

**本库解释：**“ITC对齐、ITM匹配、LM生成”不是可完全分割的能力清单。它们可共享参数、样本和梯度；对比任务找到粗看相似的难负例，融合任务再学习属性或关系差异。ALBEF的“先对齐后融合”是路径与目标分工，三个loss联合优化，不是两个独立先后训练阶段。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=3|S011 · pp.3–4 §3.1–3.2]]

## 模型自己生成监督：软目标和语料改写是两件事

ALBEF的EMA教师给ITC/MLM提供概率分布，按$\alpha$与原硬标签混合。对固定教师$q$，$\mathrm{KL}(q\Vert p)=H(q,p)-H(q)$，因此软目标交叉熵与教师到学生KL对学生有相同梯度；交叉熵并不只接受one-hot。教师是自身参数历史平均，不是独立的事实裁判，软化标签不能保证改错方向。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=4|S011 · pp.4–6 §3.3–4、式6/11]]

BLIP CapFilt则先用captioner生成新文字，再用独立微调的filter筛原文与合成文，合并人工配对后训练新模型。它改变了**训练数据集合**；不是把每次LM forward当作已完成数据自举。重复原文到相同样本数没有得到同类收益，支持内容/筛选作用，但成本还包含初始训练、生成和过滤。作者只报告这一轮bootstrap，多轮是展望。[[raw/papers/architecture/pretraining/BLIP.pdf#page=4|S012 · pp.4–6 §3.3–4.4、Tables1–4]] [[raw/papers/architecture/pretraining/BLIP.pdf#page=8|pp.8–9 Tables12–13、§7]]

LLaVA让文本GPT-4依据caption/box生成指令答案，学生才读图片；MiniGPT-4则先由自身生成长描述，再由ChatGPT修文并人工精炼。两条流程都扩展语言监督形式，但教师未见像素或只修文字时，无法自动确认缺失视觉事实。NeXT官方说明改用GPT-4V生成部分用户请求回复，监督的信息接口也随之变化。[[raw/papers/models/llava/LLaVA.pdf#page=3|S022 · pp.3–4 §3、pp.22–25合成prompt]] [[raw/papers/architecture/connectors/MiniGPT-4.pdf#page=4|S019 · pp.4–5 §3.2–3.3]] [S024 Data Mixture](https://llava-vl.github.io/blog/2024-01-30-llava-next/#2-data-mixture)（2026-10-31访问；[[raw/web/S024-LLaVA-NeXT/official-blog.html|快照]]）。

## 同叫“对齐阶段”，开放参数却不同

| 系统 | 前一阶段 | 后续学习 | 应保留的例外 |
| --- | --- | --- | --- |
| VLMo | BEiT权重→固定attention/视觉专家学文本FFN | 联合图文训练整个MoME | 视觉初始化的既有成本在图文阶段之外 |
| BEiT-3 | 随机初始化及按层缩放，三类数据共同MDM | 检索额外中间ITC训练、各任务适配 | 不能将BEiT initialization误作加载BEiT权重 |
| BLIP-2 | 冻结encoder，Q-Former学ITC/ITG/ITM | 冻结LLM，以生成loss学习视觉前缀 | 下游caption/VQA/retrieval会解冻视觉编码器 |
| MiniGPT-4 | 冻结已有ViT+Q-Former+Vicuna，只训线性层 | 小量长描述继续训接口 | 不是从裸ViT起步的线性对齐 |
| mPLUG-Owl | 训练ViT+abstractor，冻结LLaMA | 冻结语言底权重，训练LoRA等 | Stage2 abstractor可训/冻结在v3内部冲突，未裁定 |
| LLaVA | 仅训投影 | 投影+Vicuna；视觉冻结 | ScienceQA专门分支与聊天分支不同 |

定位：[[raw/papers/architecture/pretraining/VLMo.pdf#page=4|S014 · pp.4–6 §3.4、p.16 AppendixB]]、[[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=5|S015 · p.5、p.16 AppendixA]]、[[raw/papers/architecture/connectors/BLIP-2.pdf#page=3|S017 · pp.3–4、7–8]]、[[raw/papers/architecture/connectors/MiniGPT-4.pdf#page=4|S019 · pp.4–5]]、[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=1|S020 · p.1与pp.4–5]]、[[raw/papers/models/llava/LLaVA.pdf#page=5|S022 · p.5、p.20]]。

InstructBLIP把指令进入Q-Former与指令进入LLM分开，冻结视觉/LLM，只调整桥接部分；数据集采样按规模平方根并有手调。LLaVA-1.5则将短答案、选项字母、Unanswerable写成明确格式指令，与完整网格+可训练LLM结合。前者改变特征选择条件，后者使回答格式可控；最终差异还含数据与预算，不能只比较连接器名字。[[raw/papers/architecture/connectors/InstructBLIP.pdf#page=5|S018 · pp.5–6 §2.3–2.6]] [[raw/papers/models/llava/LLaVA-1.5.pdf#page=3|S023 · pp.3–4 §3.2–3.3、p.9格式prompt]]

## 模态比例和上下文课程必须按版本读

DeepSeek-VL主预训练为约70%语言、30%多模态，且从高语言比例warmup到目标；VL2明确为70%VL、30%text-only，alignment还训练视觉编码器。两代都使用纯文本，却不能照抄同一个比例或冻结方案。第一代图4图注反向问题在唯一页保留，综合采用正文与Table1，不将冲突变成第二套已确认配方。[[raw/papers/models/deepseek/DeepSeek-VL.pdf#page=7|S031 · p.7 Table1、pp.13–14 §3.2.2]] [[raw/papers/models/deepseek/DeepSeek-VL2.pdf#page=6|S032 · pp.6、9–10 §3.2/4.1、Table2]]

Qwen-VL从ViT+adapter开放、LLM冻结，变为全开多任务，再冻结ViT做Chat SFT；Qwen3-VL从merger-only对齐到全参数8K/32K/256K上下文课程。最大长度、累计训练token与唯一图片数是不同量；多模态训练是否保留文本能力，还须和**实际初始化checkpoint**比较，不能拿发布更晚的文本模型替代起点。[[raw/papers/models/qwen/Qwen-VL.pdf#page=4|S026 · pp.4–6 Fig.3、p.20 Table8、p.23 Table11]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=4|S028 · pp.4–5 Table1、pp.21–22 Tables5–7]]

InternVL的4.98B是清洗后数据池、28.7B是第一阶段曝光；第二阶段冻结视觉和继承语言权重，只训新query/CA。DeepSeek-V4.1又先做视觉对比与视觉自回归训练，丢弃辅助LLM后接主干；主训练早期冻结ViT，norm/projector始终可训，后续解冻。累计45T联合token不能当作独立图文对数。[[raw/papers/models/internvl/InternVL.pdf#page=5|S025 · pp.5–6、p.12 Table20]] [[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=15|S034 · p.15视觉规则、pp.21–23 §4]]

DeepSeek-OCR没有SFT、不是chatbot；70%OCR/20%通用视觉/10%纯文本以转写/解析为中心。SAM+compressor冻结、CLIP与MoE decoder训练，不能套用“先对齐再指令”的通用叙事。[[raw/papers/models/deepseek/DeepSeek-OCR.pdf#page=9|S033 · pp.9–10 §3.5、p.18 Fig.12]]

## 从答案监督到奖励与环境

Qwen3-VL区分可规则/代码验证的推理RL、通用模型评审与工具使用奖励；部分函数调用数据可不实际执行，不能把全部合成轨迹当真实工具证据。DeepSeek-V4.1把任务写为problem/environment/verifier，训练还需处理异步rollout的length bias与off-policy staleness；奖励通过不自动等于任务意图满足。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=8|S028 · pp.8–13 §3.2.10、§4]] [[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=25|S034 · pp.25–32 §5.1–5.2]]

训练奖励、实际闭环和终态分别进入[[wiki/reasoning/Overview|推理地图]]与[[wiki/evaluation/Judges-and-Task-Success|任务成功页]]；成本进入[[wiki/efficiency/Resource-Ledger|资源账本]]。S029官方卡没有完整数据/阶段预算，不从early fusion概括补造统一训练时间线；固定文档能确认的配置见[[wiki/sources/models/qwen/Qwen-3.5|唯一页]]。

## 实际来源入口

[[wiki/papers/vision/encoders/AIMv2|S007 AIMv2]] · [[wiki/papers/vision/alignment/SigLIP2|S010 SigLIP2]] · [[wiki/papers/architecture/pretraining/ALBEF|S011 ALBEF]] · [[wiki/papers/architecture/pretraining/BLIP|S012 BLIP]] · [[wiki/papers/architecture/pretraining/CoCa|S013 CoCa]] · [[wiki/papers/architecture/pretraining/VLMo|S014 VLMo]] · [[wiki/papers/architecture/pretraining/BEiT-v3|S015 BEiT-v3]] · [[wiki/papers/architecture/connectors/BLIP-2|S017 BLIP-2]] · [[wiki/papers/architecture/connectors/InstructBLIP|S018 InstructBLIP]] · [[wiki/papers/architecture/connectors/MiniGPT-4|S019 MiniGPT-4]] · [[wiki/papers/architecture/connectors/mPLUG-Owl|S020 mPLUG-Owl]] · [[wiki/papers/architecture/generation/MiniGPT-5|S021 MiniGPT-5]] · [[wiki/papers/models/llava/LLaVA|S022 LLaVA]] · [[wiki/papers/models/llava/LLaVA-1.5|S023 LLaVA-1.5]] · [[wiki/sources/models/llava/LLaVA-NeXT|S024 LLaVA-NeXT]] · [[wiki/papers/models/internvl/InternVL|S025 InternVL]] · [[wiki/papers/models/qwen/Qwen-VL|S026 Qwen-VL]] · [[wiki/papers/models/qwen/Qwen3-VL|S028 Qwen3-VL]] · [[wiki/papers/models/deepseek/DeepSeek-VL|S031 DeepSeek-VL]] · [[wiki/papers/models/deepseek/DeepSeek-VL2|S032 DeepSeek-VL2]] · [[wiki/papers/models/deepseek/DeepSeek-OCR|S033 DeepSeek-OCR]] · [[wiki/papers/models/deepseek/DeepSeek-V4.1-Flash|S034 DeepSeek-V4.1-Flash]]。原始定位在上文；唯一页保存身份、读取范围和实验条件。
