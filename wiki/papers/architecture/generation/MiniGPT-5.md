---
type: paper
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/architecture/generation/MiniGPT-5.pdf]]"
source_id: S021
reading_status: read
ingest_status: integrating
primary_direction: architecture/generation
---

# MiniGPT-5：用生成接口把交错文本接到扩散模型

MiniGPT-5 要解决的是：给定前面的图片和叙述，模型怎样决定下一段文字、何时插图，以及插入什么图。LLM 输出文字和标记图像位置的 **generative vokens**；这些位置的隐藏状态经 feature mapper 变成扩散条件，真正合成图像的是 Stable Diffusion。它不是把 RGB 像素纳入普通文本词表后由 Vicuna 直接逐像素生成。[[raw/papers/architecture/generation/MiniGPT-5.pdf#page=3|§3、图2，PDF p.3–4]]

## 身份与实际阅读

- 作者：Kaizhi Zheng、Xuehai He、Xin Eric Wang。arXiv:2310.02239 **v4，2025-12-09**；[固定版本](https://arxiv.org/pdf/2310.02239v4)。首稿年份与本次所读版本年份不可混写。
- v4 PDF 题名为 *Interleaved Vision-and-Language Generation via Generative Voken*；arXiv 元数据沿用 *MiniGPT-5: Interleaved Vision-and-Language Generation via Generative Vokens*。前缀与单复数不同，但作者和摘要中的模型身份一致，维持一个 S021。
- 原件：[[raw/papers/architecture/generation/MiniGPT-5.pdf]]；SHA-256：`496647dc686fa0955af3f7346940273e92052fd0828776747a35d8214549c9f1`。
- 2026-10-31 实际读正文 PDF pp.1–8、附录 A/B 与 C 说明 pp.12–15；查看 pp.3–8、13–15 原页，核对图2–6、公式1–5、表1–9。参考文献未逐条追读；pp.16–19 额外示例未逐图视觉审核。未审代码、未运行模型或复现；Obsidian 内显示未测。

## 三种表示各做什么

输入图片由 MiniGPT-4 的 ViT、Q-Former 和线性投影转为 $32\times d$ 视觉特征，与文字 embedding 拼接，供 Vicuna 理解上下文。输出词表另加默认 8 个 `[IMG1]…[IMG8]`。它们不是输入的32个视觉特征：**输入特征承载已见图像，输出 vokens 的位置和隐藏状态指定将要生成的图像**。[[raw/papers/architecture/generation/MiniGPT-5.pdf#page=3|§3.1，PDF p.3]]

```mermaid
flowchart LR
  A[已有图像与文字] --> B[MiniGPT-4 编码及 Vicuna]
  B --> C[文字 token 与图像 vokens]
  C --> D[voken 位置的隐藏状态]
  D --> E[MLP 与 encoder-decoder mapper]
  E --> F[Stable Diffusion 条件去噪与图像解码]
```

这是依原文整理的信息流示意；箭头表示表示传递，不表示所有模块都训练。mapper 用两层 MLP、四层 encoder-decoder Transformer 和可学习 decoder queries $q$，将 $n$ 个状态转为扩散文本条件所需的 $L\times\hat d$ 序列：

$$
\hat h_{\mathrm{voken}}=\theta_{\mathrm{enc-dec}}(\theta_{\mathrm{MLP}}(h_{\mathrm{voken}}),q).
$$

这里的 Transformer decoder 负责生成**条件特征**；SD 的 U-Net 负责预测去噪量，VAE 负责图像潜变量与图像的转换。不能把三个“decoder/生成”职责合成一个模块。[[raw/papers/architecture/generation/MiniGPT-5.pdf#page=4|§3.2、式2–3，PDF p.4]]

## 为何既有语言损失，又有扩散损失

语言损失 $L_{\mathrm{text}}$ 在文字与 vokens 的联合序列上做下一 token 预测，使模型学会插图位置；对真实目标图像编码并加噪后，冻结 U-Net 的噪声预测误差反传到 mapper 与可训练接口：

$$
L_{\mathrm{LDM}}=\mathbb E_{\epsilon,t}\left[\|\epsilon-\epsilon_\theta(z_t,t,\hat h_{\mathrm{voken}})\|_2^2\right].
$$

“冻结”指不更新预训练权重，不意味着不能经过该模块传递梯度。此损失让生成接口直接得到目标图像监督，不必把每张下游图片先转成详细 caption。[[raw/papers/architecture/generation/MiniGPT-5.pdf#page=4|§3.2，式1–3，PDF p.4]]

| 阶段 | 数据与目标 | 更新参数与预算 |
| --- | --- | --- |
| 单图对齐 | CC3M 可用约220万图文对；$0.01L_{text}+L_{LDM}+0.1L_{CAP}$，其中 $L_{CAP}=\mathrm{MSE}(\hat h,\tau(c))$ | 新 voken 输入/输出 embedding、完整 mapper；Vicuna-7B 与图像/扩散主干冻结；2 epochs、batch 48、LR $2\times10^{-4}$ |
| 交错微调 | VIST/MMDialog；下一图→文字、下一文字→图像、上下文→图文对三类任务；$0.01L_{text}+L_{LDM}$ | voken embedding、Vicuna LoRA、mapper encoder-decoder；固定 MLP 和 decoder queries；4 epochs、batch 32、LR $2\times10^{-5}$ |

表据 [[raw/papers/architecture/generation/MiniGPT-5.pdf#page=5|§3.3–4.1，PDF p.5]] 与 [[raw/papers/architecture/generation/MiniGPT-5.pdf#page=12|附录A，PDF p.12]]。作者报告微调可训练参数约6.6M、4张 A6000；不是整个系统只有6.6M参数。已读实现段未明确输入像素分辨率和推理去噪步数，不能从 SD 版本自行补定。

**description-free 有阶段边界。** 第一阶段明确使用 CC3M caption 和 SD 文本编码器监督；第二阶段不要求另配每幅图的详细描述，仍使用 VIST 故事文本或 MMDialog 对话。MMDialog 为资源限制只保留最多一个历史 turn，不能以此证明任意长对话一致性。[[raw/papers/architecture/generation/MiniGPT-5.pdf#page=12|附录A.1–A.2，PDF p.12]]

CFG 训练以10%概率将 mapper **输入**的 voken 状态置零，再经过同一个 mapper 得到无条件表示；推理结合条件/无条件预测。这不同于仅把 SD 文本提示置空。CFG scale 增大在图5中有折中，不能写成越大越好。[[raw/papers/architecture/generation/MiniGPT-5.pdf#page=5|§3.3，式5，PDF p.5]] [[raw/papers/architecture/generation/MiniGPT-5.pdf#page=14|附录B，图5–6，PDF p.14]]

## 实验支持什么

| 设置 | 可核结果 | 解释边界 |
| --- | --- | --- |
| VIST validation，给历史并逐步生成图 | LoRA 版本 CLIP-I 0.66、FID 366.62；two-stage 为0.57、403.06 | 表1 FID 按故事序列计算，不能与后面 final-step 全集合 FID 拼接 |
| VIST narration，三模型同 LoRA 配置 | MiniGPT-5 S-BERT 0.6315、Rouge-L 0.3373、Meteor 0.3263；MiniGPT-4 为0.6273、0.3401、0.3296 | 不同指标有升有降，只支持该任务中未见一致大幅退化，非理解能力全面保持 |
| VIST 人评，随机5000序列、每项2名众包评审 | 语言连续性/图像质量/图文一致性胜率55.22%/52.43%/56.90% | 是相对 two-stage 的偏好，不是通用正确率 |
| MMDialog test | MM-Relevance 0.67 对 GILL 0.64、Divter 0.62；IS 20.23低于 GILL 23.78 | 综合相关性与图像分布指标并不同时领先 |

定位：[[raw/papers/architecture/generation/MiniGPT-5.pdf#page=6|§4.2–4.3，表1–3，PDF p.6]]；[[raw/papers/architecture/generation/MiniGPT-5.pdf#page=7|§4.3，表4，PDF p.7]]。two-stage 先生成 caption 再调用 SD；作者为它用 InstructBLIP-13B 合成监督，GILL 在可用 CC3M 上重训并用额外描述微调。因此这些是作者构建的系统比较，不是仅改 voken 一项的控制实验。

人评界面确实要求看同一上下文的两份候选，并允许 Tie；已读范围未报告评审者一致性、置信区间和顺序随机化。表3 caption 说“超过70%更好或持平”，但语言连续性胜率加平局为65.11%，图像质量为62.21%，只有图文一致性为71.12%；保留数字，不把该概括扩展到三项。[[raw/papers/architecture/generation/MiniGPT-5.pdf#page=6|表3，PDF p.6]] [[raw/papers/architecture/generation/MiniGPT-5.pdf#page=13|图4，PDF p.13]]

CC3M 消融中删除 $L_{CAP}$ 的 FID 从31.47变40.24，删除 $L_{LDM}$ 变34.65；固定 queries 却有更好的 FID 30.56、较低的 CLIP-I 0.60，说明指标之间存在折中，不能说所有可学习设计全面优越。[[raw/papers/architecture/generation/MiniGPT-5.pdf#page=7|表5，PDF p.7]] [[raw/papers/architecture/generation/MiniGPT-5.pdf#page=8|表7，PDF p.8]]

v4 表8新增 Qwen2.5-VL+SD3 等组合，不应当成2023初版实验证据；同时换理解和生成主干不能单独归因于某个接口。附录表9 final-step FID 为61.85/59.48/56.32，与表1的故事内 FID 非同一协议。**本库分析：**分布级 FID 改善不足以直接证明逐对象纹理身份保持；原文结论也承认纹理维持困难。[[raw/papers/architecture/generation/MiniGPT-5.pdf#page=8|表8与§5，PDF p.8]] [[raw/papers/architecture/generation/MiniGPT-5.pdf#page=13|附录B.3，PDF pp.13–15]]

## 冻结旧稿的校正

旧笔记输入：[[raw/notes/多模态经典/2023-MiniGPT-5总结.tex]]、[[raw/notes/多模态经典/Latex_out/2023-MiniGPT-5总结.pdf]]，均为二手解释，不增加论文证据。

旧稿“替换 SD 的 CLIP 文本编码器”可作粗略接口类比，但本页明确保留 mapper、voken 定位与扩散生成的职责；训练仍使用原文本编码器的 $L_{CAP}$，不能解释为从系统彻底移除它。旧稿“同时生成”改为交错自回归文字/vokens与条件扩散协作；“完美结合”和无条件长序列能力不保留。本次另补阶段冻结、实际数据范围、指标分歧及 v4 新实验边界。

## 待整合问题

接口主题可比较“输入视觉压缩”与“输出生成条件”；训练主题可用此例解释冻结模块仍传梯度、caption-free 的阶段限定；评测主题可比较语义相似、人类偏好、分布 FID 与身份一致性四种证据。共享主题由协调者后续整合，当前不声称双向综合已完成。
