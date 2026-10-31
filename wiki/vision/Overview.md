---
type: overview
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf]]"
  - "[[raw/lectures/VLM-2.pdf]]"
---

# 视觉表示：保留什么细节，在哪一步压缩

MLLM 的视觉输入问题可以沿四个位置检查：**输入尺寸与视图 → patch 与编码 → 连接后的 token → 语言模型实际使用的信息**。高分辨率、原生分辨率和 token 压缩并非同一种改动；某一步保留了细节，也不保证后续接口保留任务所需内容。此页以 S001 综述与 S003 讲义搭建机制地图，模型例子保留转述身份。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=7|S001 · §2.4 · pp.7–9]] [[raw/lectures/VLM-2.pdf#page=37|S003 · Mini-Gemini / Preliminary · pp.37–40]]

## 尺寸、patch 与视图数共同决定输入

本库教学近似：单幅图像尺寸为 $H\times W$、非重叠方形 patch 边长为 $P$，且整除、无额外标记时，patch 数为

$$
N_{\mathrm{patch}}=(H/P)(W/P).
$$

它是输入组织的计数，不是最终送入 LLM 的 token 数公式；padding、切片、重采样或 merger 都会改变后续数量。S001 将分辨率提高与视觉 token 压力联系，S003 图中则明确分开 patchify、token drop、packing 和后续 pooling。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=7|S001 · §2.4 · p.7]] [[raw/lectures/VLM-2.pdf#page=39|S003 · NaViT · p.39]]

| 操作位置 | 希望保留或改变什么 | 需要单独追问的代价 / 条件 |
| --- | --- | --- |
| 将整图 resize 到固定尺寸 | 用固定输入预算覆盖整图 | 长宽比变化与小字缩小会影响任务细节 |
| 整图缩略图加局部 tiles | 同时提供全局上下文和局部细节 | 视图数、重复覆盖、局部位置及 LLM token 开销 |
| 原生尺寸 / 长宽比的变长 patch 序列 | 减少强制方形 resize，适配不同形状 | 变长 batch 如何打包，样本间 attention 如何隔离 |
| 编码后聚合 / 重采样 / 合并 | 控制进入 LLM 的表示长度 | 哪些局部关系在压缩中保留，压缩模块自身的计算 |

表为本库重组。前两类依据 S001 多视图讨论与 S003 AnyRes 图；第三类依据课程 NaViT 图；第四类依据 S001 连接器和压缩讨论。[[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=6|S001 · §2.2、2.4 · pp.6–8]] [[raw/lectures/VLM-2.pdf#page=39|S003 · pp.39–40]]

## 三种“多看细节”走不同信息路径

**原生分辨率与 packing。** 讲义 NaViT 图先把不同形状图像 patchify，再 pack 到序列；attention mask 把每个 token 的可见范围限制在同一样本，padding 还须在 attention、pooling 和 loss 中排除。这里打包的是多个样本的计算组织，不能画成跨图像混合语义。[[raw/lectures/VLM-2.pdf#page=39|S003 · NaViT 原图 · p.39]]

**整图与局部视图。** AnyRes 图保留 resize 整图与 split 局部两支；DeepSeek-VL2 图再用 view separator 和行标记组织局部特征。多视图不仅是输入更多块，也要让下游分辨它们的空间关系。这里说的是课程图展示的组织方式，不提供各方案统一预算下的收益比较。[[raw/lectures/VLM-2.pdf#page=40|S003 · AnyRes · p.40]] [[raw/lectures/VLM-2.pdf#page=68|S003 · DeepSeek-VL2 · p.68]]

**高分辨率特征被低分辨率 query 读取。** 课程 Mini-Gemini 图让较少 query 读取高分辨率窗口的信息；S001 的 S2 图则对不同尺度重复编码、合并池化并沿通道拼接。前者侧重检索式聚合，后者侧重多尺度表征包装。S2 的 parameter-free 描述没有取消多次视觉编码成本。[[raw/lectures/VLM-2.pdf#page=37|S003 · Mini-Gemini · p.37]] [[raw/surveys/Efficient Multimodal Large Language Models A Survey.pdf#page=9|S001 · Fig.7、§2.4 · pp.8–9]]

## 全局对齐与局部可用特征不是同一目标

讲义 SigLIP 2 部分把全局 sigmoid 图文目标、location-aware captioning、局部到全局自蒸馏和 masked prediction 放在一起。本库据此提出的机制问题是：整图与一句话相似，是否足以支持下游定位、OCR 和密集任务？局部监督与密集预测为不同位置提供更具体的约束，但改善幅度和因果归属必须等待相应原论文证据，不能由目标名称直接确定。[[raw/lectures/VLM-2.pdf#page=86|S003 · SigLIP 2 · pp.86–90]]

位置组织也属于表示接口。课程 M-RoPE 用 $t/h/w$ 区分时间和空间坐标，interleaved 图改变轴与频率通道的分配；它们不等于简单把全部 token 重新编号。图像位置、视频帧采样和真实时间对齐应分别记录。[[raw/lectures/VLM-2.pdf#page=47|S003 · M-RoPE · p.47]] [[raw/lectures/VLM-2.pdf#page=58|S003 · Qwen2-VL / 2.5-VL · pp.58–59]]

继续阅读：接口怎样用这些特征见 [[wiki/architecture/Overview|架构]]，预算怎样核算见 [[wiki/efficiency/Overview|效率]]。来源入口为 [[wiki/surveys/Efficient Multimodal Large Language Models A Survey|S001]] 与 [[wiki/lectures/VLM-2|S003]]；编码器原论文入口和真实审核状态集中在 [[wiki/index|索引]]。Obsidian 内显示未测。
