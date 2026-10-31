---
type: overview
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]"
  - "[[raw/papers/models/llava/LLaVA.pdf]]"
  - "[[raw/papers/architecture/pretraining/CoCa.pdf]]"
  - "[[raw/papers/architecture/pretraining/ALBEF.pdf]]"
  - "[[raw/papers/architecture/pretraining/BEiT-v3.pdf]]"
  - "[[raw/papers/vision/encoders/AIMv2.pdf]]"
  - "[[raw/papers/vision/encoders/SoViT.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-OCR.pdf]]"
  - "[[raw/papers/models/qwen/Qwen3-VL.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf]]"
---

# 评测与证据：任务对象、判分和预算一起决定分数

一个分数至少连接三件事：**任务是什么、什么观察算成功、在什么输入与预算下运行。** 任务地图和判分地图不相同；S002的Understanding/Generation/Reasoning/Planning与其matching/model-scoring分类就回答不同问题。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=32|S002 · pp.32–41 §5]]

深入页[[wiki/evaluation/Judges-and-Task-Success|裁判与任务成功]]用LLaVA-Bench、MiniGPT-4、OwlEval、MiniGPT-5、Qwen和DeepSeek原始实验解释：人评、模型评审、参考覆盖、转写precision、检索诊断、动作匹配和真实终态不能互换。

| 要确认什么 | 应看的证据 |
| --- | --- |
| 图像细节正确 | 输出与实际视觉内容/位置对应 |
| 终答正确 | 参考答案或可验证约束 |
| 解释可靠 | 展示步骤成立，并非只看最终答案 |
| 动作执行 | 工具日志、环境变化、实际产物 |
| 任务完成 | 最终产物/环境满足全部要求 |

表为本库证据分解，S002的数独与产物案例说明这些对象可以分离；不能以个案估计失败率。LLaVA的GPT-4相对评分、ScienceQA系统内judge和训练reward judge又是不同角色。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=26|S002 · pp.26–28 Figs6–8]] [[raw/papers/models/llava/LLaVA.pdf#page=6|S022 · pp.6–9 §5]]

“zero-shot”“held-out”“probe”都要附协议：CoCa冻结检索、ALBEF从COCO适配后转移、BEiT-3中间对比训练并非同条件；AIMv2 attentive probe与SoViT全调也不同。所有表格保留任务划分、训练见图标记、视觉输入、模型/接口、生成/候选/工具预算及指标聚合。[[raw/papers/architecture/pretraining/CoCa.pdf#page=9|S013 · p.9]] [[raw/papers/architecture/pretraining/ALBEF.pdf#page=6|S011 · p.6]] [[raw/papers/architecture/pretraining/BEiT-v3.pdf#page=16|S015 · p.16]] [[raw/papers/vision/encoders/AIMv2.pdf#page=5|S007 · p.5]] [[raw/papers/vision/encoders/SoViT.pdf#page=8|S005 · p.8]]

OCR转写不是一般长上下文推理；needle retrieval不是长视频因果理解；坐标输出不是交互成功；harness与effort会改变agent成绩。成本接[[wiki/efficiency/Overview|效率]]，动作—观察循环接[[wiki/reasoning/Overview|推理]]。本库未运行benchmark或审计完整评测代码，不从作者表格建立独立排行榜。[[raw/papers/models/deepseek/DeepSeek-OCR.pdf#page=19|S033 · p.19 §5–6]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=25|S028 · p.25 §5.12.3]] [[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=35|S034 · p.35 Table4]]

## 实际来源入口

[[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models|S002 Multimodal-Reasoning-Survey]] · [[wiki/papers/vision/encoders/SoViT|S005 SoViT]] · [[wiki/papers/vision/encoders/AIMv2|S007 AIMv2]] · [[wiki/papers/architecture/pretraining/ALBEF|S011 ALBEF]] · [[wiki/papers/architecture/pretraining/CoCa|S013 CoCa]] · [[wiki/papers/architecture/pretraining/BEiT-v3|S015 BEiT-v3]] · [[wiki/papers/models/llava/LLaVA|S022 LLaVA]] · [[wiki/papers/models/qwen/Qwen3-VL|S028 Qwen3-VL]] · [[wiki/papers/models/deepseek/DeepSeek-OCR|S033 DeepSeek-OCR]] · [[wiki/papers/models/deepseek/DeepSeek-V4.1-Flash|S034 DeepSeek-V4.1-Flash]]。原始定位在上文；唯一页保存身份、读取范围和实验条件。
