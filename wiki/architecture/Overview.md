---
type: overview
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/architecture/pretraining/VLMo.pdf]]"
  - "[[raw/papers/architecture/connectors/BLIP-2.pdf]]"
  - "[[raw/papers/architecture/generation/MiniGPT-5.pdf]]"
  - "[[raw/papers/architecture/pretraining/ALBEF.pdf]]"
  - "[[raw/papers/architecture/pretraining/BLIP.pdf]]"
  - "[[raw/papers/architecture/pretraining/CoCa.pdf]]"
  - "[[raw/papers/architecture/pretraining/BEiT-v3.pdf]]"
  - "[[raw/papers/architecture/connectors/InstructBLIP.pdf]]"
  - "[[raw/papers/architecture/connectors/MiniGPT-4.pdf]]"
  - "[[raw/papers/architecture/connectors/mPLUG-Owl.pdf]]"
  - "[[raw/papers/models/internvl/InternVL.pdf]]"
  - "[[raw/papers/models/qwen/Qwen3-VL.pdf]]"
  - "[[raw/lectures/VLM-2.pdf]]"
  - "[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]"
---

# 架构：分开读取权重、可见性、路由与输出接口

比较架构先问：**参数复用谁，当前token能读谁，信息经过哪条路，输出交给谁？** 统一骨干、查询压缩、跨层注入与生成vokens回答不同问题。本库按这些轴组织，而不是把模型分成互斥的“简单/复杂”两类。[[raw/papers/architecture/pretraining/VLMo.pdf#page=3|S014 · pp.3–5]] [[raw/papers/architecture/connectors/BLIP-2.pdf#page=3|S017 · pp.3–4]] [[raw/papers/architecture/generation/MiniGPT-5.pdf#page=3|S021 · pp.3–4]]

| 阅读入口 | 关键区分 |
| --- | --- |
| [[wiki/architecture/Visibility-and-Connections\|可见性、路由与连接]] | 双塔/融合；共享attention与模态FFN；Flamingo内部CA、BLIP-2 query前缀、LLaVA逐位置投影。 |
| [[wiki/architecture/Generative-Output-Interfaces\|生成输出接口]] | 输入视觉特征、输出文字/坐标、输出图像条件与扩散合成的职责。 |
| [[wiki/architecture/Sequence-Memory-and-Retrieval\|序列记忆与检索]] | 固定状态、显式KV检索、层间残差流与参数查表分别保存什么。 |

ALBEF、BLIP、CoCa表明独立表示和条件融合可在同系统共存；VLMo/BEiT-3共享attention却仍按任务改变输入和mask。共享权重不会让分别前向的图文自动交互；顶部VL-FFN也不是联合attention第一次融合的位置。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=3|S011 · pp.3–4]] [[raw/papers/architecture/pretraining/BLIP.pdf#page=2|S012 · pp.2–3]] [[raw/papers/architecture/pretraining/CoCa.pdf#page=4|S013 · pp.4–5]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=4|S015 · p.4 Fig.3]]

query既可以压缩视觉，也可以被任务条件化；InstructBLIP把指令送入提取模块，MiniGPT-4则冻结既有Q-Former桥，mPLUG-Owl用abstractor接输入端。InternVL还能保留直接网格与query双路，Qwen3-VL DeepStack以跨层注入增加视觉通道而不增长序列。结构图必须保留这些关系，不能将所有连接器都画成同一个方框。[[raw/papers/architecture/connectors/InstructBLIP.pdf#page=5|S018 · p.5 Fig.3]] [[raw/papers/architecture/connectors/MiniGPT-4.pdf#page=2|S019 · p.2 Fig.1]] [[raw/papers/architecture/connectors/mPLUG-Owl.pdf#page=4|S020 · p.4 Fig.2]] [[raw/papers/models/internvl/InternVL.pdf#page=5|S025 · p.5 Fig.4]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=3|S028 · pp.3–4 Fig.1]]

冻结范围进入[[wiki/training/Overview|训练]]，长度与计算进入[[wiki/efficiency/Overview|效率]]。课程CogVLM等范围外例子保留[[wiki/lectures/VLM-2|S003转述]]身份；S002的native multimodal reasoning属于综合与展望，不能据名称判定现有模型成熟度。[[raw/lectures/VLM-2.pdf#page=74|S003 · pp.74–75]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=30|S002 · pp.30–31 §4.3]]

## 实际来源入口

[[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models|S002 Multimodal-Reasoning-Survey]] · [[wiki/lectures/VLM-2|S003 VLM-2]] · [[wiki/papers/architecture/pretraining/ALBEF|S011 ALBEF]] · [[wiki/papers/architecture/pretraining/BLIP|S012 BLIP]] · [[wiki/papers/architecture/pretraining/CoCa|S013 CoCa]] · [[wiki/papers/architecture/pretraining/VLMo|S014 VLMo]] · [[wiki/papers/architecture/pretraining/BEiT-v3|S015 BEiT-v3]] · [[wiki/papers/architecture/connectors/BLIP-2|S017 BLIP-2]] · [[wiki/papers/architecture/connectors/InstructBLIP|S018 InstructBLIP]] · [[wiki/papers/architecture/connectors/MiniGPT-4|S019 MiniGPT-4]] · [[wiki/papers/architecture/connectors/mPLUG-Owl|S020 mPLUG-Owl]] · [[wiki/papers/architecture/generation/MiniGPT-5|S021 MiniGPT-5]] · [[wiki/papers/models/internvl/InternVL|S025 InternVL]] · [[wiki/papers/models/qwen/Qwen3-VL|S028 Qwen3-VL]]。原始定位在上文；唯一页保存身份、读取范围和实验条件。
