---
type: overview
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf]]"
  - "[[raw/papers/models/llava/LLaVA.pdf]]"
  - "[[raw/papers/architecture/pretraining/ALBEF.pdf]]"
  - "[[raw/papers/architecture/pretraining/BLIP.pdf]]"
  - "[[raw/papers/architecture/connectors/MiniGPT-4.pdf]]"
  - "[[raw/papers/architecture/connectors/InstructBLIP.pdf]]"
  - "[[raw/papers/models/llava/LLaVA-1.5.pdf]]"
  - "[[raw/papers/architecture/connectors/BLIP-2.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-VL.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-VL2.pdf]]"
  - "[[raw/papers/models/internvl/InternVL.pdf]]"
  - "[[raw/papers/models/qwen/Qwen3-VL.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf]]"
---

# 训练与数据：监督怎样穿过接口，更新哪些参数？

一个训练阶段至少写四列：**数据、目标与监督位置、开放参数、输入与累计预算**。预训练和指令微调可以都用next-token loss；生成目标也可以服务于视觉表示、语言输出或图像条件。阶段名称和“端到端”不足以恢复实际计算。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=18|S001 · pp.18–19 §5]] [[raw/papers/models/llava/LLaVA.pdf#page=5|S022 · p.5 §4.2]]

详读[[wiki/training/Supervision-and-Stages|监督与阶段]]，其中把目标比较、自生成监督、冻结表、模态比例和奖励/环境放在同一条证据链。

## 先问监督改了什么

ALBEF混合硬标签与EMA软目标；BLIP CapFilt重写/筛选语料；LLaVA用文字标注教师合成多类指令；MiniGPT-4用小量精炼长描述调整输出；InstructBLIP使指令进入视觉提取，LLaVA-1.5将回答格式变成明确条件。它们改变的是监督内容或路径，不只是多加一些样本。[[raw/papers/architecture/pretraining/ALBEF.pdf#page=4|S011 · pp.4–5]] [[raw/papers/architecture/pretraining/BLIP.pdf#page=4|S012 · pp.4–6]] [[raw/papers/models/llava/LLaVA.pdf#page=3|S022 · pp.3–4]] [[raw/papers/architecture/connectors/MiniGPT-4.pdf#page=4|S019 · pp.4–5]] [[raw/papers/architecture/connectors/InstructBLIP.pdf#page=5|S018 · pp.5–6]] [[raw/papers/models/llava/LLaVA-1.5.pdf#page=3|S023 · pp.3–4]]

## 再问同名阶段更新了谁

BLIP-2预训练冻结两侧骨干，下游VQA等会解冻视觉；DeepSeek-VL alignment仅训连接器，VL2 alignment同时训视觉；InternVL第二阶段caption目标不更新视觉主干。模型用了某目标，不等于它所有组件都受到该目标更新。[[raw/papers/architecture/connectors/BLIP-2.pdf#page=4|S017 · p.4、pp.7–8]] [[raw/papers/models/deepseek/DeepSeek-VL.pdf#page=12|S031 · pp.12–16]] [[raw/papers/models/deepseek/DeepSeek-VL2.pdf#page=9|S032 · pp.9–10]] [[raw/papers/models/internvl/InternVL.pdf#page=6|S025 · p.6 §3.3]]

Qwen3-VL的长上下文课程与后训练同时改变数据、长度和预算；DeepSeek-V4.1还加入异步rollout、验证器和OPD，不能把SFT/RL当一个无需环境条件的标签。奖励的测量对象见[[wiki/evaluation/Overview|评测]]，运行时反馈见[[wiki/reasoning/Overview|推理]]，既有主干与数据生成成本见[[wiki/efficiency/Overview|效率]]。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=4|S028 · pp.4–13 §3–4]] [[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=25|S034 · pp.25–32 §5.1–5.2]]

## 实际来源入口

[[wiki/surveys/Efficient Multimodal Large Language Models A Survey|S001 Efficient-MLLM-Survey]] · [[wiki/papers/architecture/pretraining/ALBEF|S011 ALBEF]] · [[wiki/papers/architecture/pretraining/BLIP|S012 BLIP]] · [[wiki/papers/architecture/connectors/BLIP-2|S017 BLIP-2]] · [[wiki/papers/architecture/connectors/InstructBLIP|S018 InstructBLIP]] · [[wiki/papers/architecture/connectors/MiniGPT-4|S019 MiniGPT-4]] · [[wiki/papers/models/llava/LLaVA|S022 LLaVA]] · [[wiki/papers/models/llava/LLaVA-1.5|S023 LLaVA-1.5]] · [[wiki/papers/models/internvl/InternVL|S025 InternVL]] · [[wiki/papers/models/qwen/Qwen3-VL|S028 Qwen3-VL]] · [[wiki/papers/models/deepseek/DeepSeek-VL|S031 DeepSeek-VL]] · [[wiki/papers/models/deepseek/DeepSeek-VL2|S032 DeepSeek-VL2]] · [[wiki/papers/models/deepseek/DeepSeek-V4.1-Flash|S034 DeepSeek-V4.1-Flash]]。原始定位在上文；唯一页保存身份、读取范围和实验条件。
