---
type: overview
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/vision/encoders/ViT.pdf]]"
  - "[[raw/papers/vision/alignment/CLIP.pdf]]"
  - "[[raw/papers/vision/alignment/SigLIP.pdf]]"
  - "[[raw/papers/vision/alignment/SigLIP2.pdf]]"
  - "[[raw/papers/vision/encoders/AIMv2.pdf]]"
  - "[[raw/papers/vision/encoders/SoViT.pdf]]"
  - "[[raw/papers/vision/encoders/NaViT.pdf]]"
  - "[[raw/papers/models/qwen/Qwen-VL.pdf]]"
  - "[[raw/papers/models/qwen/Qwen2-VL.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-VL.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-VL2.pdf]]"
  - "[[raw/papers/models/deepseek/DeepSeek-OCR.pdf]]"
---

# 视觉表示：从监督、输入保真到下游可读性

视觉表示要同时回答两个问题：**训练要求保存什么信息，输入预算允许看清什么信息？** ViT展示patch Transformer在大规模分类预训练后的迁移；CLIP/SigLIP把语义接口扩到文字；SigLIP2与AIMv2进一步让区域、密集特征或像素预测进入监督。它们的分数必须跟读出协议走，不能把分类、定位和接LLM的结果当一种能力。[[raw/papers/vision/encoders/ViT.pdf#page=3|S004 · pp.3–4]] [[raw/papers/vision/alignment/CLIP.pdf#page=4|S008 · pp.4–7]] [[raw/papers/vision/alignment/SigLIP.pdf#page=3|S009 · pp.3–5]] [[raw/papers/vision/alignment/SigLIP2.pdf#page=2|S010 · pp.2–4]] [[raw/papers/vision/encoders/AIMv2.pdf#page=2|S007 · pp.2–3]]

| 阅读入口 | 主要解释 |
| --- | --- |
| [[wiki/vision/Objectives-and-Transfer\|视觉目标与迁移]] | 分类/对比/生成/局部监督各约束什么；linear/attentive probe、全调和MLLM适配怎样区分。 |
| [[wiki/vision/Resolution-and-Token-Budget\|分辨率与token预算]] | native、packing、tiling、query与空间合并作用的位置；单tile与整图/多图预算。 |

## 先看数据与任务，再看尺寸与形状

SoViT说明在训练计算固定时，形状、容量与训练时长需要联合选择；NaViT把固定形状约束移到打包容器，并保留样本隔离；AIMv2 native适配用变batch维持patch预算。三者分别优化模型形状、batch组织与分辨率训练，不是同一种“动态视觉encoder”。[[raw/papers/vision/encoders/SoViT.pdf#page=4|S005 · pp.4–6 §3]] [[raw/papers/vision/encoders/NaViT.pdf#page=2|S006 · pp.2–5 Fig.2]] [[raw/papers/vision/encoders/AIMv2.pdf#page=4|S007 · p.4 §2.4]]

## 视觉到语言之间还有信息预算

提高分辨率后，Qwen-VL仍输出256query；Qwen2-VL输出变长merger序列；DeepSeek-VL在固定576位置增加通道；VL2用tiles增加位置并恢复二维结构；OCR先压缩再做全局attention。它们说明“图像看得更细”与“LLM收到更多位置”可以分离。[[raw/papers/models/qwen/Qwen-VL.pdf#page=3|S026 · pp.3–4]] [[raw/papers/models/qwen/Qwen2-VL.pdf#page=4|S027 · p.4]] [[raw/papers/models/deepseek/DeepSeek-VL.pdf#page=10|S031 · p.10]] [[raw/papers/models/deepseek/DeepSeek-VL2.pdf#page=5|S032 · p.5]] [[raw/papers/models/deepseek/DeepSeek-OCR.pdf#page=5|S033 · pp.5–7]]

后续接口见[[wiki/architecture/Overview|架构]]；前端与后端成本见[[wiki/efficiency/Overview|效率]]；视觉质量如何取证见[[wiki/evaluation/Overview|评测]]。[[wiki/lectures/VLM-2|S003讲义]]仍保留课程主线和范围外例子，已读原论文的具体条件在上述主题与唯一页中区分。

## 实际来源入口

[[wiki/papers/vision/encoders/ViT|S004 ViT]] · [[wiki/papers/vision/encoders/SoViT|S005 SoViT]] · [[wiki/papers/vision/encoders/NaViT|S006 NaViT]] · [[wiki/papers/vision/encoders/AIMv2|S007 AIMv2]] · [[wiki/papers/vision/alignment/CLIP|S008 CLIP]] · [[wiki/papers/vision/alignment/SigLIP|S009 SigLIP]] · [[wiki/papers/vision/alignment/SigLIP2|S010 SigLIP2]] · [[wiki/papers/models/qwen/Qwen-VL|S026 Qwen-VL]] · [[wiki/papers/models/qwen/Qwen2-VL|S027 Qwen2-VL]] · [[wiki/papers/models/deepseek/DeepSeek-VL|S031 DeepSeek-VL]] · [[wiki/papers/models/deepseek/DeepSeek-VL2|S032 DeepSeek-VL2]] · [[wiki/papers/models/deepseek/DeepSeek-OCR|S033 DeepSeek-OCR]]。原始定位在上文；唯一页保存身份、读取范围和实验条件。
