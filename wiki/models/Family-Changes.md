---
type: topic
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/architecture/multimodal-backbones/ALBEF.pdf]]"
  - "[[raw/papers/architecture/multimodal-backbones/BLIP.pdf]]"
  - "[[raw/papers/architecture/multimodal-backbones/CoCa.pdf]]"
  - "[[raw/papers/architecture/multimodal-backbones/VLMo.pdf]]"
  - "[[raw/papers/architecture/multimodal-backbones/BEiT-v3.pdf]]"
  - "[[raw/papers/architecture/visual-interfaces/BLIP-2.pdf]]"
  - "[[raw/papers/architecture/visual-interfaces/Flamingo.pdf]]"
  - "[[raw/papers/training/instruction-adaptation/InstructBLIP.pdf]]"
  - "[[raw/papers/training/instruction-adaptation/MiniGPT-4.pdf]]"
  - "[[raw/papers/training/instruction-adaptation/mPLUG-Owl.pdf]]"
  - "[[raw/papers/architecture/generative-interfaces/MiniGPT-5.pdf]]"
  - "[[raw/papers/training/instruction-adaptation/LLaVA.pdf]]"
  - "[[raw/papers/training/instruction-adaptation/LLaVA-1.5.pdf]]"
  - "[[raw/web/S024-LLaVA-NeXT/official-blog.html]]"
  - "[[raw/papers/models/qwen/Qwen-VL.pdf]]"
  - "[[raw/papers/models/qwen/Qwen2-VL.pdf]]"
  - "[[raw/papers/models/qwen/Qwen3-VL.pdf]]"
  - "[[raw/web/S029-Qwen-3.5/README.md]]"
  - "[[raw/web/S029-Qwen-3.5/config.json]]"
  - "[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-VL.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-VL2.pdf]]"
  - "[[raw/papers/efficiency/context-compression/DeepSeek-OCR.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf]]"
  - "[[raw/papers/architecture/multimodal-backbones/InternVL.pdf]]"
---

# 家族变化轴：输入、接口、数据和计算怎样共同演进？

家族名称帮助定位版本，**变化轴帮助提出可核问题**。以下不是年份排行榜，也不把几项联合升级后的成绩差归给单个组件。比较围绕输入保真、接入位置、语言结构、监督与评测条件；原文完整身份与局限在唯一来源页。

## 从预训练VLM到视觉助手，改变的不只是连接器

ALBEF/BLIP保留独立表示与条件融合路径，CoCa把因果decoder分成不读图/读图两段；VLMo/BEiT-3则复用attention并以模态FFN和task mask形成多种接口。它们研究检索、分类、caption与条件理解，不应只按“是否接入chat LLM”衡量价值。BLIP-2复用冻结视觉/语言骨干而学习query前缀，Flamingo在冻结LM内部插入CA并用交错网页学习ICL；简单或复杂是结构属性，任务与训练数据才决定比较的含义。[[raw/papers/architecture/multimodal-backbones/ALBEF.pdf#page=3|S011 · pp.3–5]] [[raw/papers/architecture/multimodal-backbones/BLIP.pdf#page=2|S012 · pp.2–4]] [[raw/papers/architecture/multimodal-backbones/CoCa.pdf#page=4|S013 · pp.4–5]] [[raw/papers/architecture/multimodal-backbones/VLMo.pdf#page=3|S014 · pp.3–6]] [[raw/papers/architecture/multimodal-backbones/BEiT-v3.pdf#page=3|S015 · pp.3–5]] [[raw/papers/architecture/visual-interfaces/BLIP-2.pdf#page=3|S017 · pp.3–4]] [[raw/papers/architecture/visual-interfaces/Flamingo.pdf#page=4|S016 · pp.4–6]]

InstructBLIP把任务指令送入视觉提取，MiniGPT-4复用冻结的BLIP-2视觉桥并用小量精炼长描述改善生成形式，mPLUG-Owl第一阶段训练视觉编码器与abstractor、第二阶段用LoRA改变语言行为。它们分别改变任务条件化、既有桥复用和开放参数，不能简化成“都只训adapter”。MiniGPT-5再扩展到输出图像条件，而非仅提升视觉问答。[[raw/papers/training/instruction-adaptation/InstructBLIP.pdf#page=4|S018 · pp.4–6]] [[raw/papers/training/instruction-adaptation/MiniGPT-4.pdf#page=4|S019 · pp.4–5]] [[raw/papers/training/instruction-adaptation/mPLUG-Owl.pdf#page=4|S020 · pp.4–5，Stage2冲突见唯一页]] [[raw/papers/architecture/generative-interfaces/MiniGPT-5.pdf#page=3|S021 · pp.3–5]]

## LLaVA：线性接口、格式指令与动态视图

| 轴 | 初版S022 | 1.5 S023 | NeXT官方快照S024 |
| --- | --- | --- | --- |
| 接口 | CLIP网格→线性→Vicuna | 两层MLP，完整网格；普通版336² | 复用1.5预训练connector，336局部块+全局图 |
| 数据 | 文本GPT-4依据caption/box合成158K | 665K多任务+纯文本对话，格式指令 | 760K指令；更多文档/图表及GPT-4V回复 |
| 对齐数据 | 595K | 558K | Stage1 558K，复用connector |
| 输入要区分 | 原文未明确完整像素/token配置 | 336基线与224-tile实验HD分开 | 有限AnyRes网格，约4倍像素预算 |

原文定位：[[raw/papers/training/instruction-adaptation/LLaVA.pdf#page=3|S022 · pp.3–5 §3–4、p.20]]、[[raw/papers/training/instruction-adaptation/LLaVA-1.5.pdf#page=3|S023 · pp.3–5 §3、p.9 AppendixA]]；[S024技术细节与Model Card](https://llava-vl.github.io/blog/2024-01-30-llava-next/#detailed-technical-improvement)（2026-10-31访问；[[raw/web/S024-LLaVA-NeXT/official-blog.html|本地快照]]）。HTML卡片Stage2只写Full model，不能从旧1.5冻结表补造所有模块的更新范围。

这条线给出的正面认识是：简单投影也能学到多样指令响应，格式能作为任务条件，局部视图与全局视图互补。证据却不支持把全体提升都归给MLP或像素；1.5逐步累加实验存在个别回退，NeXT同13B的MMMU也并未增加。初版ScienceQA专门微调与1.5的SQA-IMG零样本、开放回答GPT-4相对评分更不能混成一条能力曲线。[[raw/papers/training/instruction-adaptation/LLaVA-1.5.pdf#page=4|S023 · pp.4–6 Tables2–4]] [[raw/papers/training/instruction-adaptation/LLaVA.pdf#page=8|S022 · pp.8–9 Table7]] [S024 Results](https://llava-vl.github.io/blog/2024-01-30-llava-next/#results)（同快照）。

## Qwen：固定瓶颈、动态序列、多层注入与骨干效率

Qwen-VL提高224→448输入时，adapter仍输出256 query位置；Qwen2-VL改为动态分辨率和空间$2\times2$合并，LLM位置随输入面积变化，并用M-RoPE表达时间/高/宽；Qwen3-VL在动态输入上新增DeepStack、Interleaved MRoPE与文本时间戳。它们分别回答“压多少”“怎么给位置”“哪些视觉深度进入语言计算”。[[raw/papers/models/qwen/Qwen-VL.pdf#page=3|S026 · pp.3–4 §2、p.20 Table8]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=4|S027 · pp.4–5 §2.1]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=3|S028 · pp.3–4 §2]]

对应训练也从Qwen-VL三阶段模块开放与区域/OCR多任务，发展到Qwen3-VL的merger-only→全参数→32K/256K课程及Thinking/工具后训练。Chat/Thinking并非无条件更强：Qwen-VL-Chat部分传统任务低于base；Qwen3-VL Thinking在STEM若干任务提高，OCR/定位却有回退。应比较同任务、同checkpoint模式和解码预算。[[raw/papers/models/qwen/Qwen-VL.pdf#page=7|S026 · pp.7–9 Tables4–7]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=4|S028 · p.4 Table1、p.15 Table2、pp.20–22生成条件]]

Qwen3.5-397B-A17B是固定官方卡/配置来源：397B总与17B激活、3:1的linear/full attention、视觉patch16与spatial merge2、空DeepStack索引可确认；不能从这些字段反推完整early-fusion训练流程或宣称所有Qwen3.5变体一致。262144原生、1010000外推和托管Plus默认配置也不同。[[raw/web/S029-Qwen-3.5/README.md#Model Overview|S029 · Model Overview]] [[raw/web/S029-Qwen-3.5/config.json|固定config]] [[raw/web/S029-Qwen-3.5/README.md#Processing Ultra-Long Texts|超长上下文说明，commit8472618、2026-10-31访问]]

Qwen3.8-Flash-Next旧对象对应Qwen3.8-Next语言骨干报告：GDN以误差修正更新固定状态，QSA先选块再读原始token，GR扩展残差存储，host n-gram表增加参数记忆。主干125B/激活6B另有51B表；并未给视觉接口或视觉成绩。Table11的397B-A17B基线名为Qwen3.7-Plus-Base，不能与S029 Qwen3.5后训练checkpoint等同；报告的约1/9训练FLOPs也不等于全部部署成本。机制详见[[wiki/architecture/Sequence-Memory-and-Retrieval|序列记忆与检索]]。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=4|S030 · pp.4–7 §2.1、pp.10–15 §2.2–2.3、pp.22–23 §4/Table11]]

## DeepSeek：通道融合、tiles/MoE、转写压缩与长会话系统

第一代VL用SigLIP+SAM在固定576位置沿通道融合，控制后端长度；VL2改为共享SigLIP编码全局+局部tiles、重建二维顺序，并加入稀疏MoE与Small/main MLA。数据、解冻与模态比例也改变：VL语言约70%，VL2语言30%。**固定位置上加通道与增加空间位置是不同取舍，MoE与KV压缩又分别影响计算和存储。**[[raw/papers/models/deepseek/DeepSeek-VL.pdf#page=10|S031 · pp.10–16 §3、Table4]] [[raw/papers/models/deepseek/DeepSeek-VL2.pdf#page=4|S032 · pp.4–10 §2–4、Tables1–2]]

OCR则转向领域化转写/解析：SAM→compressor→CLIP串联，在全局attention之前压缩位置，decoder生成原文或结构标记，没有SFT。它与VL2同属DeepSeek并不意味着相同任务、参数或评价；OCR的precision/ED不能与通用问答分数直接比较。把文本渲染成图像用于长上下文是作者待验证方向。[[raw/papers/efficiency/context-compression/DeepSeek-OCR.pdf#page=5|S033 · pp.5–10 §3–4、pp.18–19 §5–6]]

V4.1-Flash将优化对象扩展到input-heavy agent：因果encoder产生decoder global KV以省prefill，CSA2跨层共享与FP4省全局存储，bounded replay省持久化局部状态；视觉仍经ViT与$3\times3$空间合并接入。552B backbone另有196B Engram，prefill/decode激活分别8B/16B，不能只写一个“总参数/激活参数”对。它的多模态、工具和代码成绩必须与harness、effort、输入窗口及Pass@k一起读，不能视为VL2的单因素后继消融。[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=7|S034 · pp.7–14 §2、pp.19–20 §3.2、pp.33–36 Tables3–4]]

## InternVL补出视觉规模与中间件这条轴

InternVL同时扩大InternViT和QLLaMA；Chat可选直接网格，或直接网格+query双路，不是所有视觉信息都必经96query。它在相近LLaVA1.5配方下替换视觉底座后，有些指标提高、有些下降；完整QLLaMA版又使用不同预训练/SFT数据。由此可问“视觉表示是否易被小接口使用”，却不能仅由最终分数确定视觉规模失衡就是唯一瓶颈。InternViT与InternVL保持同一个S025身份。[[raw/papers/architecture/multimodal-backbones/InternVL.pdf#page=4|S025 · pp.4–6 Figs3–4、p.8 Table9、p.9 Table12]]

这些家族共享的比较框架是[[wiki/vision/Resolution-and-Token-Budget|输入与token]]、[[wiki/architecture/Visibility-and-Connections|可见性与接口]]、[[wiki/training/Supervision-and-Stages|监督/阶段]]、[[wiki/efficiency/Resource-Ledger|资源账本]]、[[wiki/evaluation/Judges-and-Task-Success|测量条件]]。本页是跨来源机制综合，未复现实验，也不凭模型代数推断未来能力。

## 实际来源入口

[[wiki/papers/architecture/multimodal-backbones/ALBEF|S011 ALBEF]] · [[wiki/papers/architecture/multimodal-backbones/BLIP|S012 BLIP]] · [[wiki/papers/architecture/multimodal-backbones/CoCa|S013 CoCa]] · [[wiki/papers/architecture/multimodal-backbones/VLMo|S014 VLMo]] · [[wiki/papers/architecture/multimodal-backbones/BEiT-v3|S015 BEiT-v3]] · [[wiki/papers/architecture/visual-interfaces/Flamingo|S016 Flamingo]] · [[wiki/papers/architecture/visual-interfaces/BLIP-2|S017 BLIP-2]] · [[wiki/papers/training/instruction-adaptation/InstructBLIP|S018 InstructBLIP]] · [[wiki/papers/training/instruction-adaptation/MiniGPT-4|S019 MiniGPT-4]] · [[wiki/papers/training/instruction-adaptation/mPLUG-Owl|S020 mPLUG-Owl]] · [[wiki/papers/architecture/generative-interfaces/MiniGPT-5|S021 MiniGPT-5]] · [[wiki/papers/training/instruction-adaptation/LLaVA|S022 LLaVA]] · [[wiki/papers/training/instruction-adaptation/LLaVA-1.5|S023 LLaVA-1.5]] · [[wiki/sources/models/llava/LLaVA-NeXT|S024 LLaVA-NeXT]] · [[wiki/papers/architecture/multimodal-backbones/InternVL|S025 InternVL]] · [[wiki/papers/models/qwen/Qwen-VL|S026 Qwen-VL]] · [[wiki/papers/models/qwen/Qwen2-VL|S027 Qwen2-VL]] · [[wiki/papers/models/qwen/Qwen3-VL|S028 Qwen3-VL]] · [[wiki/sources/models/qwen/Qwen-3.5|S029 Qwen-3.5]] · [[wiki/papers/architecture/language-backbones/Qwen3.8-Flash-Next|S030 Qwen3.8-Flash-Next]] · [[wiki/papers/models/deepseek/DeepSeek-VL|S031 DeepSeek-VL]] · [[wiki/papers/models/deepseek/DeepSeek-VL2|S032 DeepSeek-VL2]] · [[wiki/papers/efficiency/context-compression/DeepSeek-OCR|S033 DeepSeek-OCR]] · [[wiki/papers/models/deepseek/DeepSeek-V4.1-Flash|S034 DeepSeek-V4.1-Flash]]。原始定位在上文；唯一页保存身份、读取范围和实验条件。
