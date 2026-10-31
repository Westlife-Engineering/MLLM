---
type: topic
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]"
  - "[[raw/papers/models/llava/LLaVA.pdf]]"
  - "[[raw/papers/models/qwen/Qwen3-VL.pdf]]"
  - "[[raw/papers/architecture/connectors/MiniGPT-4.pdf]]"
  - "[[raw/papers/architecture/connectors/mPLUG-Owl.pdf]]"
  - "[[raw/papers/architecture/generation/MiniGPT-5.pdf]]"
  - "[[raw/papers/architecture/pretraining/CoCa.pdf]]"
  - "[[raw/papers/architecture/pretraining/ALBEF.pdf]]"
  - "[[raw/papers/architecture/pretraining/BLIP.pdf]]"
  - "[[raw/papers/architecture/pretraining/BEiT-v3.pdf]]"
  - "[[raw/papers/architecture/connectors/InstructBLIP.pdf]]"
  - "[[raw/papers/vision/encoders/AIMv2.pdf]]"
  - "[[raw/papers/vision/encoders/SoViT.pdf]]"
  - "[[raw/papers/vision/encoders/ViT.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-OCR.pdf]]"
  - "[[raw/papers/models/qwen/Qwen2-VL.pdf]]"
  - "[[raw/papers/models/qwen/Qwen3.8-Flash-Next.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf]]"
  - "[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf]]"
---

# 裁判与任务成功：答案、解释、生成物和终态怎样分别取证？

评测链路是**任务输入 → 系统输出/执行 → 判定规则 → 聚合分数**。任何一环改变，分数含义都可能改变。流畅、参考覆盖、视觉正确、解释可靠、动作执行和任务完成是不同对象；先拆清对象，才知道模型评审与人评能提供什么证据。S002的任务地图与判分类是入口，下面以本轮原始实验具体展开。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=32|S002 · pp.32–41 §5、Fig.10]]

## 同一个“judge”可能做三种事

LLaVA-Bench把图片交给候选视觉模型，却把人工/标注的文字图像描述交给文本GPT-4生成参考，再由GPT-4读描述、问题、两份答案作1–10整体评分，聚合成相对参考分数。85.1表示这套相对评分，不是85.1%答对，也不是“多模态GPT-4能力的85.1%”。重复裁判稳定说明复评分散小，不能代替与独立人类判分的一致性校准。[[raw/papers/models/llava/LLaVA.pdf#page=6|S022 · pp.6–7 §5.1、Tables4–5]]

同篇ScienceQA的GPT-4 judge却在LLaVA与GPT-4答案分歧时综合答案，成为**被测推理系统的一部分**；最终按选择题正确率判分。92.53属于组合系统，LLaVA单模型为90.92。这与开放回答的评分裁判职责不同。第三种是训练中的reward model/judge：例如Qwen3-VL通用RL用模型评审提供学习信号，它影响被训练分布，不能当作独立测试事实。[[raw/papers/models/llava/LLaVA.pdf#page=8|S022 · pp.8–9 §5.2、Table7]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=11|S028 · pp.11–12 §4.4]]

## 人工参与，也要问参与了哪一环

| 实验 | 人或模型实际看什么、判什么 | 能支持的范围 |
| --- | --- | --- |
| MiniGPT-4四类请求人评 | 每类25图，共100，是否满足meme/食谱/广告/诗歌请求 | 作者该小集合的请求响应，不是通用视觉准确率 |
| MiniGPT-4 COCO覆盖判定 | ChatGPT只看每图随机一条参考caption与生成caption，判对象/关系覆盖 | 不直接检查额外幻觉，也不看原图 |
| OwlEval | 作者整理50图82问，人工A–D分级与能力标签 | 有目的的诊断集合；多轮相关，82问非82独立场景 |
| MiniGPT-5 VIST人评 | 两份图文候选按连贯性/图质/图文一致性偏好，允许Tie | 相对指定baseline的偏好，不是逐事实正确率 |

原文定位：[[raw/papers/architecture/connectors/MiniGPT-4.pdf#page=6|S019 · pp.6–8 Tables1–5、p.15 AppendixA.3]]、[[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=6|S020 · pp.6–8 §4.2–4.3、Tables1–2]]、[[raw/papers/architecture/generation/MiniGPT-5.pdf#page=6|S021 · p.6 Table3、p.13 Fig.4]]。评分者人数、盲法、分歧、一致性或区间没有充分报告时，保留为报告缺口；人工参与不会自动完成测量有效性验证。

**本库例子：**长描述可同时“覆盖参考中的杯子和桌子”又额外编出桌布。MiniGPT-4参考覆盖提高，与其CHAIR对象幻觉和输出长度数据并不矛盾；它们测的是不同性质。类似地FID衡量图像分布差异，不能单独证明跨图人物纹理身份保持。[[raw/papers/architecture/connectors/MiniGPT-4.pdf#page=7|S019 · pp.7–9 Tables2/5]] [[raw/papers/architecture/generation/MiniGPT-5.pdf#page=8|S021 · p.8 §5、pp.13–15 AppendixB.3]]

## zero-shot、held-out、probe是协议词

CoCa检索是预训练模型冻结直接测；ALBEF/BLIP的Flickr zero-shot可从COCO检索微调后转移；BEiT-3检索还先做中间对比训练。这些标签均围绕**目标集是否再训练**，不是等同“全流程没有任务监督”。InstructBLIP的held-out包括数据集留出和整个任务类别留出，但历史骨干预训练并未因此被证明完全无相关内容；TextVQA还输入OCR tokens。[[raw/papers/architecture/pretraining/CoCa.pdf#page=9|S013 · p.9 §4.2.2]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=6|S011 · p.6 §5]] [[raw/papers/architecture/pretraining/BLIP.pdf#page=6|S012 · p.6 §5.1]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=16|S015 · p.16 AppendixA]] [[raw/papers/architecture/connectors/InstructBLIP.pdf#page=4|S018 · pp.4–6 §2.2–2.5、p.17 OCR输入]]

视觉质量还需分冻结linear、attentive probe、全参数适配、再接LLM/SFT。AIMv2的89.5是高分辨率适配后冻结encoder加attentive probe，不能与SoViT的90.3整网微调直接排名。S004 ViT的JFT子集图是5-shot线性读出，不是所有模型端到端微调的数据阈值。[[raw/papers/vision/encoders/AIMv2.pdf#page=5|S007 · p.5 Table3、p.15 TableA2]] [[raw/papers/vision/encoders/SoViT.pdf#page=8|S005 · p.8 Table1]] [[raw/papers/vision/encoders/ViT.pdf#page=7|S004 · p.7 Fig.4]]

## OCR、长序列检索、一般推理的测量不同

DeepSeek-OCR选择Fox中600–1300参考token的100页英文文档，测试64/100视觉token的转写precision曲线。十倍附近高precision不能改称十倍上下文仍保留97%一般推理，也不表示整页97%概率无错。OmniDocBench还分文字/公式/表格/阅读顺序ED；Gundam平均795与Gundam-M1853视觉位置、额外继续训练不同，不能把最好分记到最省预算名下。[[raw/papers/models/deepseek/DeepSeek-OCR.pdf#page=10|S033 · pp.10–12 §4、Tables2–4]]

Qwen3-VL的视频NIAH是把目标语义帧插入长视频的检索诊断；256K原生与约1M经YaRN扩展不同。其视频主比较又对不同API模型设不同最大帧数，VideoMMMU采用模型评分但未量化人工一致性；得分包含输入预算和判分条件。模型能找回needle不等于理解整段视频的因果关系。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=20|S028 · p.20 §5.9、p.25 §5.12.3]]

## 从动作匹配到真实终态

Qwen2-VL的AITZ TM/EM检查动作类型与位置/文字/方向匹配；ALFRED是在AI2THOR虚拟环境中用工具执行并测SR/GC。它们不是实物机器人成功率，也不是同一尺度。Point24等成绩与导航专用系统的差距提示“支持Agent”不能当作可靠完成承诺；工具返回Finished execution只证明代码跑到结束，不证明placeholder已实现任务。[[raw/papers/models/qwen/Qwen2-VL.pdf#page=10|S027 · p.10 Table5、p.13 §3.2.7、p.46 Fig.27]]

S002的数独、简历和媒体案例进一步说明：答案可对而解释错，文件可存在而内容缺项。**本库的终态分解**是：动作是否执行→产物/环境是否改变→全部要求是否满足；每一步需相应可观察证据。上述案例没有总体抽样，不能用来估计失败率或推断欺骗意图。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=26|S002 · pp.26–30 §4.1–4.2、Figs6–9]]

Qwen3.8-Next的SWEBench-Pretrain又是代码代理指标：给问题和相关代码，按生成diff与golden patch的序列相似度评分，不执行测试。50.99不是50.99% issue resolved；语义等价不同修法与表面相近错误修法都可能使代理偏离功能成功，报告未给两者校准。[[raw/papers/models/qwen/Qwen3.8-Flash-Next.pdf#page=22|S030 · pp.22–23 §4、脚注1、Table11]]

## harness与预算本身属于被测系统

DeepSeek-V4.1固定checkpoint、max effort100与任务，换scaffold后DeepSWE范围为65.5–74.2；所有组仍保留各自prompt/tools/context管理，所以不是仅改工具数的纯消融。Terminal每题3 samples用来估计Pass@1，不是best-of-3；ZeroBench主表Pass@5又是另一量。跨benchmark版本、子集与Pass@k不能拼作一个总成功率。[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=33|S034 · pp.33–35 Tables3–4、pp.47–48 AppendixB.1]]

自动验证器也可能被gaming。其ProgramBench多agent实验在参考解隐藏测试通过率≥95%的172个golden任务上，Almost@1表示**单rollout得分≥0.95**的比例；wall-clock deadline相同不等于总token/并发/GPU相同。选择“最强multi”与“可用最强single”还是作者的初步比较，不构成多agent普遍优越证明。[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=35|S034 · pp.35–36 §5.3.5、Fig.10]]

实际比较至少保留任务/划分、训练可见性、输入像素/token/帧、模型与接口、prompt与解码、工具/harness、评分器与聚合方式、资源预算。S001 Table4的val/test、子集、MME合计与训练见图标记就是这些差异的具体例子。主题关联为[[wiki/reasoning/Overview|推理交互]]、[[wiki/efficiency/Resource-Ledger|资源账本]]与[[wiki/models/Family-Changes|家族变化]]。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=22|S001 · p.22 Table4脚注]]

## 实际来源入口

[[wiki/surveys/Efficient Multimodal Large Language Models A Survey|S001 Efficient-MLLM-Survey]] · [[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models|S002 Multimodal-Reasoning-Survey]] · [[wiki/papers/vision/encoders/ViT|S004 ViT]] · [[wiki/papers/vision/encoders/SoViT|S005 SoViT]] · [[wiki/papers/vision/encoders/AIMv2|S007 AIMv2]] · [[wiki/papers/architecture/pretraining/ALBEF|S011 ALBEF]] · [[wiki/papers/architecture/pretraining/BLIP|S012 BLIP]] · [[wiki/papers/architecture/pretraining/CoCa|S013 CoCa]] · [[wiki/papers/architecture/pretraining/BEiT-v3|S015 BEiT-v3]] · [[wiki/papers/architecture/connectors/InstructBLIP|S018 InstructBLIP]] · [[wiki/papers/architecture/connectors/MiniGPT-4|S019 MiniGPT-4]] · [[wiki/papers/architecture/connectors/mPLUG-Owl|S020 mPLUG-Owl]] · [[wiki/papers/architecture/generation/MiniGPT-5|S021 MiniGPT-5]] · [[wiki/papers/models/llava/LLaVA|S022 LLaVA]] · [[wiki/papers/models/qwen/Qwen2-VL|S027 Qwen2-VL]] · [[wiki/papers/models/qwen/Qwen3-VL|S028 Qwen3-VL]] · [[wiki/papers/models/qwen/Qwen3.8-Flash-Next|S030 Qwen3.8-Flash-Next]] · [[wiki/papers/models/deepseek/DeepSeek-OCR|S033 DeepSeek-OCR]] · [[wiki/papers/models/deepseek/DeepSeek-V4.1-Flash|S034 DeepSeek-V4.1-Flash]]。原始定位在上文；唯一页保存身份、读取范围和实验条件。
