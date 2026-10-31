---
type: overview
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/models/llava/LLaVA.pdf]]"
  - "[[raw/papers/models/llava/LLaVA-1.5.pdf]]"
  - "[[raw/web/S024-LLaVA-NeXT/official-blog.html]]"
  - "[[raw/papers/models/qwen/Qwen-VL.pdf]]"
  - "[[raw/papers/models/qwen/Qwen2-VL.pdf]]"
  - "[[raw/papers/models/qwen/Qwen3-VL.pdf]]"
  - "[[raw/web/S029-Qwen-3.5/config.json]]"
  - "[[raw/papers/models/qwen/Qwen3.8-Flash-Next.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-VL.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-VL2.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-OCR.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf]]"
  - "[[raw/papers/models/internvl/InternVL.pdf]]"
  - "[[raw/lectures/VLM-2.pdf]]"
  - "[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]"
  - "[[raw/web/S029-Qwen-3.5/README.md]]"
---

# 模型演进：按机制变化轴进入家族，按证据条件读结果

**家族页承担跨版本比较，唯一来源页承担身份与原始证据。** 同一代常同时改变输入、连接、语言结构、数据、训练与评价，版本后缀不能替代因果消融。本轮完整比较从[[wiki/models/Family-Changes|家族变化轴]]进入。

| 家族/路线 | 本轮可解释的变化 |
| --- | --- |
| 预训练VLM与视觉助手 | 独立/融合表示、共享骨干、冻结接口、指令与图像输出接口 |
| LLaVA→1.5→NeXT | 线性→MLP、任务/格式数据、普通336/HD/AnyRes、语言主干与官方文档粒度 |
| Qwen-VL→2/3-VL | 固定query→动态merger→多层注入；空间/时间位置与长上下文课程 |
| Qwen3.5官方卡与Next骨干 | 固定checkpoint配置与语言架构预训练证据分别解释，不伪装成同类视觉实验 |
| DeepSeek VL→VL2 | 固定通道融合→动态tiles、MoE、部分型号MLA与数据/冻结变化 |
| DeepSeek OCR与V4.1 | 领域转写压缩与通用长会话系统的不同优化目标 |
| InternVL/InternViT | 视觉规模、中间件、直接/query双路与任务适配；同论文不重复计数 |

关键定位：[[raw/papers/models/llava/LLaVA.pdf#page=3|S022 · pp.3–5]]、[[raw/papers/models/llava/LLaVA-1.5.pdf#page=3|S023 · pp.3–5]]、[S024官方技术说明](https://llava-vl.github.io/blog/2024-01-30-llava-next/#detailed-technical-improvement)（2026-10-31，[[raw/web/S024-LLaVA-NeXT/official-blog.html|快照]]）、[[raw/papers/models/qwen/Qwen-VL.pdf#page=3|S026 · pp.3–6]]、[[raw/papers/models/qwen/Qwen2-VL.pdf#page=4|S027 · pp.4–5]]、[[raw/papers/models/qwen/Qwen3-VL.pdf#page=3|S028 · pp.3–5]]、[[raw/web/S029-Qwen-3.5/config.json|S029固定配置]]、[[raw/papers/models/qwen/Qwen3.8-Flash-Next.pdf#page=2|S030 · p.2架构、pp.22–23语言评估]]、[[raw/papers/models/deepseek/DeepSeek-VL.pdf#page=10|S031 · pp.10–16]]、[[raw/papers/models/deepseek/DeepSeek-VL2.pdf#page=4|S032 · pp.4–10]]、[[raw/papers/models/deepseek/DeepSeek-OCR.pdf#page=5|S033 · pp.5–10]]、[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=7|S034 · pp.7–14]]、[[raw/papers/models/internvl/InternVL.pdf#page=4|S025 · pp.4–6]]。

共同问题先读[[wiki/vision/Overview|视觉]]、[[wiki/architecture/Overview|架构]]和[[wiki/training/Overview|训练]]，研究比较再接[[wiki/efficiency/Overview|效率]]与[[wiki/evaluation/Overview|评测]]。S003里的后续系列与范围外工作仍是课程叙述，S002的native路线是作者综合/展望，均不因出现在家族地图就变成独立原论文已读。[[raw/lectures/VLM-2.pdf#page=48|S003 · pp.48–84家族页段]] [[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=30|S002 · pp.30–31 §4.3]]

## 实际来源入口

[[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models|S002 Multimodal-Reasoning-Survey]] · [[wiki/lectures/VLM-2|S003 VLM-2]] · [[wiki/papers/models/llava/LLaVA|S022 LLaVA]] · [[wiki/papers/models/llava/LLaVA-1.5|S023 LLaVA-1.5]] · [[wiki/sources/models/llava/LLaVA-NeXT|S024 LLaVA-NeXT]] · [[wiki/papers/models/internvl/InternVL|S025 InternVL]] · [[wiki/papers/models/qwen/Qwen-VL|S026 Qwen-VL]] · [[wiki/papers/models/qwen/Qwen2-VL|S027 Qwen2-VL]] · [[wiki/papers/models/qwen/Qwen3-VL|S028 Qwen3-VL]] · [[wiki/sources/models/qwen/Qwen-3.5|S029 Qwen-3.5]] · [[wiki/papers/models/qwen/Qwen3.8-Flash-Next|S030 Qwen3.8-Flash-Next]] · [[wiki/papers/models/deepseek/DeepSeek-VL|S031 DeepSeek-VL]] · [[wiki/papers/models/deepseek/DeepSeek-VL2|S032 DeepSeek-VL2]] · [[wiki/papers/models/deepseek/DeepSeek-OCR|S033 DeepSeek-OCR]] · [[wiki/papers/models/deepseek/DeepSeek-V4.1-Flash|S034 DeepSeek-V4.1-Flash]]。原始定位在上文；唯一页保存身份、读取范围和实验条件。
