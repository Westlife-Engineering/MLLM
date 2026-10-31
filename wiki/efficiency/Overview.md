---
type: overview
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf]]"
  - "[[raw/papers/vision/encoders/SoViT.pdf]]"
  - "[[raw/papers/vision/encoders/NaViT.pdf]]"
  - "[[raw/papers/vision/alignment/SigLIP.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-VL2.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-OCR.pdf]]"
  - "[[raw/papers/models/internvl/InternVL.pdf]]"
---

# 效率与成本：用资源对象解释节省，用任务质量限定收益

**效率不是一个参数数字，而是在给定任务质量与运行条件下节省哪段资源。** 输入token、总/激活参数、训练状态、global/local KV、生成长度、工具预算与墙钟时间须分别记。S001提供地图，原始报告进一步显示同一个“压缩”可作用于完全不同环节。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=4|S001 · pp.4–10 §2、pp.14–19 §4–5]]

主入口是[[wiki/efficiency/Resource-Ledger|资源账本]]：从视觉前端到接口、prefill、decode/cache、训练与系统循环，逐笔说明机制、公式与适用边界。

| 常见说法 | 应追问的资源对象 |
| --- | --- |
| 更少视觉token | 在encoder之前、之后还是LLM接口？压缩前端是否更贵？ |
| 更少参数 | 总容量、每token激活还是可训练参数？权重存储/通信是否算入？ |
| 更小KV | 低维表示、跨层共享、低比特、滑窗或持久化政策？ |
| 更多推理更高分 | 同任务同checkpoint吗？输出、候选、工具和重试各用多少？ |

SoViT通过形状/时长分配提高FLOPs折中；NaViT通过输入组织增加同预算曝光；SigLIP分块省中间矩阵。这三种效率没有同一分母。VL2的MoE与MLA分别控制稀疏计算和KV；V4.1进一步区分prefill计算、global KV与persistent cache，并承认bounded replay非严格等价。[[raw/papers/vision/encoders/SoViT.pdf#page=8|S005 · p.8 Table1]] [[raw/papers/vision/encoders/NaViT.pdf#page=4|S006 · pp.4–5]] [[raw/papers/vision/alignment/SigLIP.pdf#page=4|S009 · p.4 §3.3]] [[raw/papers/models/deepseek/DeepSeek-VL2.pdf#page=5|S032 · p.5 Table1]] [[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=19|S034 · pp.19–20 §3.2]]

DeepSeek-OCR的少输入位置仍需生成完整转写；InternVL的编码ms不等于聊天TTFT；多agent匹配deadline不等于总算力相等。将结果接回[[wiki/evaluation/Overview|评测]]的任务条件，才可比较质量—成本关系。本库未测速或复现实验。[[raw/papers/models/deepseek/DeepSeek-OCR.pdf#page=7|S033 · p.7 Eq.2、pp.10–11]] [[raw/papers/models/internvl/InternVL.pdf#page=11|S025 · p.11 Table19]] [[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=36|S034 · p.36 §5.3.5]]

## 实际来源入口

[[wiki/surveys/Efficient Multimodal Large Language Models A Survey|S001 Efficient-MLLM-Survey]] · [[wiki/papers/vision/encoders/SoViT|S005 SoViT]] · [[wiki/papers/vision/encoders/NaViT|S006 NaViT]] · [[wiki/papers/vision/alignment/SigLIP|S009 SigLIP]] · [[wiki/papers/models/internvl/InternVL|S025 InternVL]] · [[wiki/papers/models/deepseek/DeepSeek-VL2|S032 DeepSeek-VL2]] · [[wiki/papers/models/deepseek/DeepSeek-OCR|S033 DeepSeek-OCR]] · [[wiki/papers/models/deepseek/DeepSeek-V4.1-Flash|S034 DeepSeek-V4.1-Flash]]。原始定位在上文；唯一页保存身份、读取范围和实验条件。
