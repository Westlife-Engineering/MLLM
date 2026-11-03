---
type: topic
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf]]"
  - "[[raw/papers/vision/representation/NaViT.pdf]]"
  - "[[raw/papers/vision/representation/ViT.pdf]]"
  - "[[raw/papers/vision/representation/SoViT.pdf]]"
  - "[[raw/papers/vision/representation/SigLIP.pdf]]"
  - "[[raw/papers/architecture/visual-interfaces/BLIP-2.pdf]]"
  - "[[raw/papers/architecture/generative-interfaces/MiniGPT-5.pdf]]"
  - "[[raw/papers/architecture/multimodal-backbones/BEiT-v3.pdf]]"
  - "[[raw/papers/architecture/multimodal-backbones/VLMo.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-VL2.pdf]]"
  - "[[raw/web/S029-Qwen-3.5/README.md]]"
  - "[[raw/web/S029-Qwen-3.5/config.json]]"
  - "[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf]]"
  - "[[raw/papers/efficiency/context-compression/DeepSeek-OCR.pdf]]"
  - "[[raw/papers/architecture/multimodal-backbones/InternVL.pdf]]"
  - "[[raw/web/S024-LLaVA-NeXT/official-blog.html]]"
---

# 资源账本：视觉token、激活参数、KV与系统预算分别省在哪里？

效率比较先注明**资源对象与质量条件**。视觉序列压缩、MoE、冻结、KV共享、低比特缓存和推测解码分别作用于不同环节；同一个比例不能在这些账本之间自由转移。S001提供组件/训练/数据效率地图，本页用本轮原始报告把它展开。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=4|S001 · pp.4–10 §2、pp.14–19 §4–5]]

## 一次请求至少有六笔成本

| 账目 | 必须保留的量 | 已核机制 |
| --- | --- | --- |
| 视觉前端 | 像素、tiles/帧数、encoder、编码时间 | NaViT混合输入；DeepSeek-VL双视觉；OCR串联压缩 |
| 接口输出 | 压缩前后位置、query/merger计算 | BLIP-2 32query；Qwen-VL256query；VL2单tile196 |
| LLM prefill | 总上下文、激活计算、attention结构 | 动态视觉token、hybrid序列层、CED |
| decode与运行cache | 输出长度、KV头/latent、global/local缓存 | VL2 MLA；V4.1跨层共享+低比特+replay |
| 训练 | 可更新参数、梯度/优化器、累计曝光、设备时间 | 冻结、LoRA、形状/训练时长调整 |
| 系统循环 | 多候选、工具/子调用、重试、墙钟与总计算 | 裁剪推理、agent scaffold、并发与评分器 |

本表为本库分账，不是某论文给出的统一测量。具体证据分别见下节与[[wiki/vision/Resolution-and-Token-Budget|视觉预算]]、[[wiki/training/Supervision-and-Stages|训练阶段]]、[[wiki/reasoning/Overview|推理交互]]。

## token少、参数少、训练量少不是同一方向

**教学近似：**普通dense Transformer层，长度$N$、hidden维$d$时，投影/FFN包含$O(Nd^2)$项，成对attention包含$O(N^2d)$项；具体系数、FFN宽度、稀疏/融合实现另计。视觉token缩短能减轻后端，却可能先增加多尺度编码或压缩网络成本。NaViT还通过低分辨率和drop在同预算下看更多图，不能把组合收益全算成mask本身提速。[[raw/papers/vision/representation/NaViT.pdf#page=4|S006 · p.4 §2.3、p.18 Table2]] [[raw/papers/vision/representation/ViT.pdf#page=3|S004 · pp.3–4架构]]

SoViT在固定训练FLOPs下重分配模型形状与处理样本数，428M模型推理FLOPs较低，但实测TPUv3 core-hours为230k对210k（SoViT/ViT-g）。**相同FLOPs不是墙钟完全相同，参数更少不是所有任务质量相同。**[[raw/papers/vision/representation/SoViT.pdf#page=8|S005 · pp.8–10 Tables1–4]]

SigLIP分块省相似度中间矩阵，仍有配对计算与通信；SigLiT冻结视觉塔还能预计算图像特征，但其既有预训练/预计算成本不应消失。BLIP-2冻结两侧主干时仍需LLM前向及对接口输入的梯度；MiniGPT-5冻结扩散主干也会通过它传条件梯度。可训练参数主要影响训练状态，不直接给出部署tokens/s。[[raw/papers/vision/representation/SigLIP.pdf#page=4|S009 · pp.4–6 §3.3–4.4]] [[raw/papers/architecture/visual-interfaces/BLIP-2.pdf#page=4|S017 · p.4 §3.3–3.4]] [[raw/papers/architecture/generative-interfaces/MiniGPT-5.pdf#page=4|S021 · pp.4–5]]

## 总参数、激活参数与存储分列

VLMo/BEiT-3的模态FFN按输入规则选择，区别于内容router的top-k稀疏MoE。VL2主模型LLM总27B、激活4.1B，加视觉约4.5B激活口径；Tiny为MHA，Small/main为MLA。总权重仍要存储或搬运，稀疏路由又可能引入通信与负载不均，不能由激活量直接推断显存/延迟同比缩小。[[raw/papers/architecture/multimodal-backbones/BEiT-v3.pdf#page=5|S015 · p.5 Table2]] [[raw/papers/architecture/multimodal-backbones/VLMo.pdf#page=5|S014 · p.5 §3.2]] [[raw/papers/models/deepseek/DeepSeek-VL2.pdf#page=5|S032 · p.5 Table1、p.10 Table2]]

S029固定官方配置为397B总/17B激活、45层linear attention与15层full attention、512 routed experts中选10加shared；这些是特定checkpoint的官方口径及配置计数，不能当作已实测吞吐或通用MLLM部署显存。视觉deepstack索引为空也只是该配置事实。[[raw/web/S029-Qwen-3.5/README.md#Model Overview|S029 · Model Overview]] [[raw/web/S029-Qwen-3.5/config.json|text_config/vision_config，固定commit8472618，2026-10-31读取]]

Qwen3.8-Next还区分固定状态GDN、原token稀疏检索QSA、四分支残差GR与额外51B host查表。QSA的7.6× prefill/4.9× decode属于特定attention内核和batch/chunk条件，不是全模型速度；n-gram扩大总容量时loss降低，也不保证所有任务同步提高。机制见[[wiki/architecture/Sequence-Memory-and-Retrieval|序列记忆]]。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=9|S030 · p.9 Fig.6、pp.14–15 Tables7–9、p.23 Table11]]

## KV账本：序列压缩、跨层共享和持久化政策

普通MHA/GQA的教学计数是$M_{KV}\approx2LNh_{kv}d_hb$，其中2表示K/V，$b$是每标量字节。该式假设每层独立缓存、无额外量化scale、无压缩/共享，不可直接套MLA或V4.1。MLA减少每token存储的表示维度，跨层共享减少独立份数，低比特改变字节数，滑窗限制局部长度，它们作用的因子不同。S001对GQA/MQA的讨论是地图；VL2只报告MLA配置，不在本文展开完整推导。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=14|S001 · pp.14–15 §4.1、Fig.12]] [[raw/papers/models/deepseek/DeepSeek-VL2.pdf#page=5|S032 · p.5 Table1]]

DeepSeek-V4.1把长prompt多数位置只算20层causal encoder；decoder global KV从encoder末层投影，并按Full/Reindex/Reuse组织共享cache和索引。decode新token仍经过全40层。由于decoder每层还有自己的局部SWA状态，prefill尾部需要bounded replay，不能称“decoder完全不计算”。当$N\gg128$时，$O(20N+20\times128)$解释近半深度的prompt计算，不能推广成端到端所有延迟严格减半。[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=9|S034 · pp.9–12 §2.2–2.3]] [[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=20|p.20 §3.2.2]]

其三种cache还须区分：

- **global KV**：跨前缀增长；主KV采用E2M1+E4M3 scale的FP4，indexer Q/K采用MXFP4，二者格式不同；SWA KV仍FP8。
- **运行局部SWA**：滑窗128限制当前局部状态规模；每层独立，不因global共享而合并。
- **persistent cache**：跨会话保留的状态。报告持久化global KV，encoder SWA放分钟级短期池，decoder SWA重放重建；少存局部状态进一步降低长期存储。

作者的890 bytes/token是global main KV+indexer K口径，不包含权重、全部激活、视觉前端和局部SWA；persistent约1/8还依赖典型负载的原缓存组成。bounded replay截断依赖，数学上不严格等价，cache-hit边界可能改变后缀状态。[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=14|S034 · p.14 §2.4.4]] [[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=19|pp.19–20 §3.2]]

DSpark与上述cache压缩又不同：它并行提出draft候选，仍由主干验证，scheduler依据吞吐曲线决定验证长度。它减少生成开销，不能把五个draft位置写成无需验证的一次生成五个正式token。Engram条件查表也有存储/通信成本，在线host预取与RL rollout驻GPU是不同条件。[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=13|S034 · pp.13–14 §2.4.2–2.4.3、p.18 §3.1.3]]

## 输入压缩后还要输出、判断和执行

DeepSeek-OCR以100个视觉位置转写约1000个参考token时，节省的是输入表征长度；1000个输出仍要生成，原图渲染、编码和文档解析也有成本。其100页英文转写实验没有测一般长上下文推理质量。InternVL的20.4/28.6ms是batch128下图文编码，不是聊天首token延迟。NeXT官方GPU×小时是本次训练阶段报告，不含CLIP/LLM生命周期全部成本。[[raw/papers/efficiency/context-compression/DeepSeek-OCR.pdf#page=7|S033 · p.7 Eq.2、pp.10–11 §4.1]] [[raw/papers/architecture/multimodal-backbones/InternVL.pdf#page=11|S025 · p.11 Table19]] [S024 Model Card](https://llava-vl.github.io/blog/2024-01-30-llava-next/#model-card)（2026-10-31，[[raw/web/S024-LLaVA-NeXT/official-blog.html|快照]]）。

推理中还要把工具裁剪、代码、候选评分、重试和并行总token加入账本。V4.1多agent实验匹配wall-clock deadline，却没有证明总token/GPU预算相等；提升成功率和降低等待时间可以伴随总资源上升。质量—成本关系须在同一任务与判分条件下读，详见[[wiki/evaluation/Judges-and-Task-Success|任务成功]]。[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=35|S034 · pp.35–36 §5.3.5、Fig.10]]

## 实际来源入口

[[wiki/surveys/Efficient Multimodal Large Language Models A Survey|S001 Efficient-MLLM-Survey]] · [[wiki/papers/vision/representation/ViT|S004 ViT]] · [[wiki/papers/vision/representation/SoViT|S005 SoViT]] · [[wiki/papers/vision/representation/NaViT|S006 NaViT]] · [[wiki/papers/vision/representation/SigLIP|S009 SigLIP]] · [[wiki/papers/architecture/multimodal-backbones/VLMo|S014 VLMo]] · [[wiki/papers/architecture/multimodal-backbones/BEiT-v3|S015 BEiT-v3]] · [[wiki/papers/architecture/visual-interfaces/BLIP-2|S017 BLIP-2]] · [[wiki/papers/architecture/generative-interfaces/MiniGPT-5|S021 MiniGPT-5]] · [[wiki/sources/models/llava/LLaVA-NeXT|S024 LLaVA-NeXT]] · [[wiki/papers/architecture/multimodal-backbones/InternVL|S025 InternVL]] · [[wiki/sources/models/qwen/Qwen-3.5|S029 Qwen-3.5]] · [[wiki/papers/architecture/language-backbones/Qwen3.8-Flash-Next|S030 Qwen3.8-Flash-Next]] · [[wiki/papers/models/deepseek/DeepSeek-VL2|S032 DeepSeek-VL2]] · [[wiki/papers/efficiency/context-compression/DeepSeek-OCR|S033 DeepSeek-OCR]] · [[wiki/papers/models/deepseek/DeepSeek-V4.1-Flash|S034 DeepSeek-V4.1-Flash]]。原始定位在上文；唯一页保存身份、读取范围和实验条件。
