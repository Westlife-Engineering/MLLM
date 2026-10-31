---
type: overview
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf]]"
  - "[[raw/papers/models/qwen/Qwen3-VL.pdf]]"
  - "[[raw/lectures/VLM-2.pdf]]"
  - "[[raw/papers/models/qwen/Qwen2-VL.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-OCR.pdf]]"
  - "[[raw/papers/models/qwen/Qwen3.8-Flash-Next.pdf]]"
  - "[[raw/papers/architecture/generation/MiniGPT-5.pdf]]"
---

# 推理与交互：增加计算、改变观察、控制环境怎样分别起作用？

多模态推理至少有三类资源：**在已有表示上继续计算，通过工具取得新信息，让动作改变环境并接收反馈。** 它们可组合，任务收益不能全部归为“更长CoT”。S002提供推理路线与任务地图；Qwen2/3-VL和DeepSeek-V4.1给出具体系统与训练条件，以下明确区分作者个案、原报告实验与本库解释。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=13|S002 · pp.13–19 §3.2.3–3.3]]

## 推理为什么可能反过来改变感知

S002 Fig.6中先裁剪图形，发现观察范围不足，再调整裁剪并继续解题；这改变下一步可见证据。六指与数独失败则展示：视觉观察、推理解释和终答正确性可以分离。案例说明机制问题，没有总体样本量或匹配消融，不能估计长推理的平均收益。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=26|S002 · pp.26–28 Figs6–8]]

Qwen3-VL的Thinking with Images实际采用image_zoom_in_tool裁剪放大；冷启动、多轮工具RL和蒸馏训练都参与。奖励同时管答案、推理质量和调用次数，报告观察到只奖前两者会学到过早单次调用的捷径。目标调用次数由离线模型估计，不能写成人工专家真值；控制次数也不保证每次都裁到正确区域。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=12|S028 · pp.12–13 §4.5、pp.40–41 AppendixB.9]]

**本库教学例子：**票据金额不清时裁剪原图是增加可用证据，计算器求和是外部计算，重写一段解释则仍依赖原输入。三者成本与失败模式不同；成功调用工具也需核对返回是否满足任务。

## 行动—观察循环需要真实环境结果

```mermaid
flowchart LR
    O[当前观察与目标] --> P[推断与规划]
    P --> A[动作或工具调用]
    A --> E[环境变化与返回]
    E -->|新观察| O
    E --> V[核查最终要求]
```

这是本库对闭环的教学重组。S003 Kimi K2.5课程图连接rollout、工具/judge、环境和训练服务，保留讲义转述；Qwen2-VL在Qwen-Agent追加动作后的观察，但AITZ动作匹配与ALFRED虚拟环境成功率是不同测量。输出坐标、调用结束、模拟环境成功与实物任务完成不能替代彼此。[[raw/lectures/VLM-2.pdf#page=81|S003 · p.81]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=13|S027 · p.13 §3.2.7、p.46 Fig.27]]

DeepSeek-V4.1把训练任务定义为problem/environment/verification system，任务合成要检查可运行性、测试和答案痕迹。验证器可能被gaming，环境崩溃也进入失败信号。Qwen3-VL的一部分函数调用训练可不执行函数，与真实在线轨迹应分开；合成返回不能直接变成真实执行证据。[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=25|S034 · pp.25–29 §5.1]] [[raw/papers/models/qwen/Qwen3-VL.pdf#page=8|S028 · pp.8–9 §3.2.10]]

## 更多thinking不是所有任务的单向升级

Qwen3-VL旗舰Thinking相对Instruct在MathVision等提高，OCRBench、DocVQA与定位有回退；工具列还可能换checkpoint，不能把跨列差算成纯工具增益。训练策略、输入和预算须与指标并读。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=15|S028 · p.15 Table2、pp.19–21评估设置]]

V4.1 effort通过长度奖励改变成本偏好：

$$
r^{len}_{b,j}=-\min\{C_{max},k(b)\ell_{b,j}/L_{norm}\},
\qquad k(b)=k_0\exp(-(b-b_{min})/\tau).
$$

effort越高，长度惩罚越弱；它不是保证执行的硬token上限。相对advantage在相同effort subgroup内算。输出长度整体可调，准确率曲线仍有plateau/dip；附录局部线性最优长度推导依赖未触cap、内点最优与边际收益假设，不能当所有任务必单调的定理。[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=29|S034 · pp.29–30 Eqs8–10]] [[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=49|pp.49–51 AppendixC、Figures11–12]]

## 长序列与压缩是推理的条件，不是推理成功证明

Qwen3-VL NIAH证明指定检索诊断中能找回needle，不等于长视频因果理解；DeepSeek-OCR验证页面转写/解析，尚未验证把任意对话光学压缩后一般推理保持。Qwen3.8-Next研究语言端固定状态与稀疏检索，任务是base语言评估，本报告没有视觉实验。三条路线应分别看[[wiki/vision/Resolution-and-Token-Budget|视觉输入]]与[[wiki/architecture/Sequence-Memory-and-Retrieval|序列记忆]]，不能只凭长窗口或低token称“更会推理”。[[raw/papers/models/qwen/Qwen3-VL.pdf#page=25|S028 · p.25 §5.12.3]] [[raw/papers/models/deepseek/DeepSeek-OCR.pdf#page=19|S033 · p.19 §5–6]] [[raw/papers/models/qwen/Qwen3.8-Flash-Next.pdf#page=22|S030 · pp.22–23 §4–5]]

S002的native multimodal reasoning仍是作者展望；MiniGPT-5提供交错文字/图像生成接口，却没有因此验证完整世界反馈推理能力。模型评审、人评、harness与终态判据接[[wiki/evaluation/Judges-and-Task-Success|任务成功]]，搜索/候选/工具的完整预算接[[wiki/efficiency/Resource-Ledger|资源账本]]。[[raw/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models.pdf#page=30|S002 · pp.30–31 §4.3]] [[raw/papers/architecture/generation/MiniGPT-5.pdf#page=3|S021 · pp.3–5]]

## 实际来源入口

[[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models|S002 Multimodal-Reasoning-Survey]] · [[wiki/lectures/VLM-2|S003 VLM-2]] · [[wiki/papers/architecture/generation/MiniGPT-5|S021 MiniGPT-5]] · [[wiki/papers/models/qwen/Qwen2-VL|S027 Qwen2-VL]] · [[wiki/papers/models/qwen/Qwen3-VL|S028 Qwen3-VL]] · [[wiki/papers/models/qwen/Qwen3.8-Flash-Next|S030 Qwen3.8-Flash-Next]] · [[wiki/papers/models/deepseek/DeepSeek-OCR|S033 DeepSeek-OCR]] · [[wiki/papers/models/deepseek/DeepSeek-V4.1-Flash|S034 DeepSeek-V4.1-Flash]]。原始定位在上文；唯一页保存身份、读取范围和实验条件。
