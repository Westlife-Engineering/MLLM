---
type: paper
source_id: S030
primary_direction: architecture/language-backbones
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf]]"
reading_status: read
ingest_status: complete
---

# Qwen3.8-Flash-Next：把记忆、检索、残差与优化成本一起设计

> [!note] 主归属（本库导航判断）
> 报告组织语言序列结构、成本与训练稳定性，作为 MLLM 邻接机制证据；家族名不构成视觉验证。 [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=1|pp.1–3、22，§1–2/§4–5]]

这份报告研究的是语言骨干：如何以较少的激活参数和训练计算，保留大型 base model 的知识、推理、代码与多语言能力。作者组合了 Gated DeltaNet（GDN）、Qwen Sparse Attention（QSA）、Gated Residual（GR）、主机侧 n-gram embedding 与 Muon 优化，并分别检查 loss、下游分数、训练/推理成本和稳定性。最值得保留的认识是：**loss 更低不必然使任务更好，预训练看似无害的改动也可能在后训练后暴露退化。**[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=1|p1–3 Abstract、§1]]

本报告没有给出视觉编码器、图像/视频 token 接口或直接视觉评测。本库将它纳入 MLLM 演进中的**语言端架构与效率证据**；不能因为旧笔记位于“MLLM实例”，就补成已验证的多模态报告。

## 来源、版本与实际阅读

| 项目 | 记录 |
| --- | --- |
| 标题/作者 | *On the Design of Qwen3.8-Next Architecture: Evaluation, Efficiency, and Training Stability*；Qwen Team，贡献者见 p23 |
| 身份/日期 | arXiv:2608.30320v1；首页正文 2026-09-01，侧栏提交日期 31 Aug 2026，分别照录 |
| 原件 | [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf]]，28 页；[固定版本 URL](https://arxiv.org/pdf/2608.30320v1) |
| SHA-256 | 17db868acaa0b86caaf89cd9516e0a92f79d7e161431e5e274b70a3123d60ef7 |
| 实际阅读 | 2026-10-31；正文 p1–23 全文与全部公式/表格；作者和参考文献 p23–28 用于身份与导航，未逐项扩读；本版本无另列附录 |
| 原页图像核看 | p2、4–13、15–23；包括总架构、GDN/QSA/GR 公式、mask、训练表、长检索/内核速度、残差路径图、n-gram 消融、优化/稳定性曲线及最终结果 |
| 旧笔记输入 | [[raw/notes/MLLM实例/Qwen/Qwen3.8-Flash-Next总结.tex]] 全正文比对；[[raw/notes/MLLM实例/Qwen/Latex_out/Qwen3.8-Flash-Next总结_排版调整.pdf]] 共 14 页，图像核看 p3、6、8、10、12–14 |
| 未实施 | 未审计模型/内核/优化器代码，未运行模型、复现训练或评测，未验证旧图对应代码版本；Obsidian 内显示未测 |

下文“作者发现”均限于报告实验。报告涉及其他方法的介绍不等于本次已读其原论文。

## 1. 三种容量不是同一个参数预算

最终模型主干总参数 **125B**，每 token 激活 **6B**，另有 **51B n-gram 表参数保存在加速器之外**。因此不能只报“125B”而让读者误认为全部可学习参数和存储均包含在其中，也不能把 51B 表等同于每 token 都做乘法的 dense 网络。Table 11 将这三个量分行列出。主机内存卸载降低的是加速器驻留压力，不会让存储与数据传输成本消失。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=1|p1 Abstract]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=23|p23 Table 11]]

Figure 1 的主干每四层为三层 GDN、一层全局 attention；在继续预训练（CPT）阶段，全局层及 MTP 内对应 attention 替换成 QSA。每个 attention/MLP 子层前后通过 GR 读写四条残差分支；n-gram 模块只放在 Layer 2，为主机预取留下第一层计算的重叠时间。图中的四个小圆是残差分支，不是四个 token 或四个专家。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=2|p2 Figure 1]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=7|p7 Implementation Details]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=14|p14 §2.3.1]]

## 2. GDN：保存的是可更新的键值关联，而非不断相加的历史

### 2.1 为什么线性状态与全局检索共存

完整 self-attention 能直接访问历史 token，但 prefill 的 token 交互计算随长度平方增长，生成时 KV cache 随历史线性增长。滑动窗口限制直接访问范围，窗外信息依赖跨层间接传播。GDN 则把前缀压进固定大小的矩阵状态，按当前内容更新；有限状态仍难以精确保留任意历史 token，所以作者周期性保留全局 attention。这里的“全局”是内容检索路径，“固定状态”是压缩记忆路径，两者分工不同。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=3|p3–4 §2.1.1]]

架构对照采用 28 层、25B-A3B MoE：先 400B tokens、4K context，再 80B tokens、32K context；SWA 窗口为 128，两个 hybrid 都每四层保留一层 full attention。GDN hybrid 相对全 attention 提高 8/9 项，相对 SWA hybrid 提高 7/9 项，平均分为 53.81、49.87、51.15；但 GDN 的 EvalPlus 49.71 低于全 attention 51.01 与 SWA 52.12。此对照支持该混合方案在这些条件下有效，不独立识别每个内部组件的因果贡献。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=5|p5 Table 1、Architecture Ablation]]

### 2.2 Delta correction 是公式里不能省掉的一步

每个 head 令 $q_t,k_t\in\mathbb R^{d_k}$、$v_t\in\mathbb R^{d_v}$，状态 $S_t\in\mathbb R^{d_k\times d_v}$。报告采用下列转置约定：

$$
\widetilde S_{t-1}=\alpha_t S_{t-1},\qquad
e_t=v_t-\widetilde S_{t-1}^{\top}k_t,
$$
$$
S_t=\widetilde S_{t-1}+\beta_t k_t e_t^\top,\qquad
y_t=S_t^\top q_t .
$$

$\alpha_t\in(0,1)$ 衰减旧状态，$\beta_t\in(0,1)$ 控制本次写入强度。关键是先用当前 key 从旧状态读出已有值，再只写入与 $v_t$ 的差 $e_t$。重复或相似 key 因而修改已有关联，而非无限累积同一外积。展开后：

$$
S_t=\alpha_t(I-\beta_t k_tk_t^\top)S_{t-1}+\beta_t k_tv_t^\top .
$$

其中负的 rank-one 修正正是 delta rule；删去它就变成另一类遗忘加外积的递推，不能继续称为这里的 GDN。以上对应原式 (1)–(5)，矩阵维度已按原页核看。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=4|p4 Eqs.1–5]]

**教学例子（由公式推得）**：若衰减后的状态对 key 的预测已恰好等于 $v_t$，则 $e_t=0$，这次不再重复写入；若预测有偏差，修正只沿当前 key 方向发生。这个例子解释更新式，不是作者另做的实验。状态衰减发生在推理状态上，旧笔记把它直接等同于优化器 weight decay 会混淆对象。

### 2.3 局部卷积、归一化和输出门分别在哪里

$q/k/v$ 先经过投影、短深度因果卷积和 SiLU，$q/k$ 再做 L2Norm；局部卷积提供短程模式，归一化约束 rank-one 转移的尺度。门参数化为

$$
\beta_t=\sigma(W_\beta x_t),\qquad
\alpha_t=\exp[-\exp(A)\operatorname{softplus}(W_\alpha x_t+b_\alpha)].
$$

各 head 更新后，输出采用

$$
o_t=W_o[\sigma(W_zx_t)\odot\operatorname{RMSNorm}(y_t)].
$$

作者将原 GDN 的 SiLU 输出门改为有界 sigmoid，并使用 zero-centered RMSNorm。输出门与衰减门/写入门控制不同位置，不能混写成单一 gate。全 attention 层保留 RoPE：作者报告 NoPE 与 RoPE 预训练差异小，但 NoPE 后训练后不终止生成更常见；正文没有给完整频率统计，故仅保留为作者观察。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=4|p4 Eqs.6–11 及末段]]

## 3. QSA：先低成本找块，再对原始 token 做稀疏 attention

### 3.1 平均池化的是索引 key，不是最终 attention 的内容

已有 token-level indexer 即使只服务稀疏 attention，也仍需对长序列打分。QSA 将 key 分成长度 $r$ 的不重叠 micro-block，先 average pooling、再 RMSNorm，然后以块起点 $p_b=br$ 施加 partial RoPE。query 仍保留自己的 token 位置 $i$。**先压缩后加位置**避免把不同旋转相位的 key 直接平均。索引器采用 MQA：最终为 4 个 query heads、1 个共享 key head，每头 128 维中的 64 维旋转。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=5|p5 Figure 3]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=6|p6 Eqs.12–14]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=7|p7 实现配置]]

令压缩并旋转后的 key 为 $\bar k_b$，块重要性为：

$$
I_{ib}=
\begin{cases}
\sum_{h=1}^{H}\operatorname{ReLU}(\langle q_i^h,\bar k_b\rangle),&p_b+r-1\le i,\\
-\infty,&\text{otherwise}.
\end{cases}
$$

条件 $p_b+r-1\le i$ 要求整块已被观测，防止池化 key 偷看未来。选出 $K_B=\lceil K/r\rceil$ 个高分块后，再展开回**原 token 索引**供 core attention；当前末尾未满块的 token 另外保留。最终 $K=2048,r=4$，最多选 512 个完整块，另加最多 3 个 tail tokens，因此不宜写成“总是严格只看 2048 tokens”。Figure 3 下方左图是压缩因果 mask，右图是展开后的块稀疏 mask；它们不是同一尺寸的 attention 矩阵。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=6|p6 Eqs.15–16]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=7|p7 Eq.19、Implementation Details]]

**教学例子**：$r=4$、位置从 0 计时，query $i=6$ 只能给已完整出现的块 0–3 打分；4–6 作为 tail 直接纳入，不能先平均包含未来位置 7 的块。等到 $i=7$，4–7 才能成为参与 top-k 的完整块。这是由原 mask 推导的示意。

### 3.2 两阶段训练中，key 的 mean 与 teacher 的 max 不可混淆

第一阶段仍使用稠密 attention，把主干所有 teacher heads 的 softmax 概率求和并 L1 归一化，得到 token 分布 $a_i$。为对齐块级索引目标，对每块做 **max pooling**，再归一化为 $\hat a_i$；这样保留块内显著 token 的信号。索引 key 用 mean 是计算表示，teacher 用 max 是构造监督目标，二者用途不同。KL 的方向为：

$$
\mathcal L_{\mathrm{KL}}=\frac1N\sum_i
D_{\mathrm{KL}}\!\left(\hat a_i\,\|\,\operatorname{Softmax}(I_i)\right).
$$

仅对当前 query 已完整可见的块计算。第二阶段打开稀疏 core attention，联合更新主干和 indexer；KL 只在选中的块集合 $\mathcal B_i$ 上计算，teacher 在此集合内重新归一化。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=6|p6 Eqs.17–18]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=7|p7 Eqs.19–20]]

| QSA CPT 阶段 | 更新对象 | 步数 / 学习率 | 每步序列与长度 | 原文约计 tokens |
| --- | --- | --- | --- | --- |
| Dense Distillation | 仅 indexer | 1,000 / $10^{-3}$ | 8 × 256K | 2B |
| Sparse Training | 主干与 indexer | 8,000 / $2.5\times10^{-5}$ | 96 × 256K | 200B |

表来自 [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=7|p7 Training Details]]。这只是 QSA 引入阶段，不是最终模型全部预训练预算。35B-A3B 消融显示，只蒸馏后立即切到稀疏模式会掉分，经过联合训练才恢复；4 个 query heads 是性能与索引成本的折中。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=8|p8–9 Architecture Ablation、Figure 5]]

### 3.3 保留能力与内核提速的边界

QSA 对照在八项普通任务上 7 项更高、平均 75.9→76.8，但 MMMLU 81.8→81.1。长检索也非全长区间都提高：8-needle MRCR 的 128K/256K 略降，512K 从 30.66→40.53、1M 从 20.71→26.44。后两者相对变好，绝对值仍明显下降，不能写成“1M 可靠记住所有信息”。RULER 是按长度区间汇总的另一套检索测试，不能与 MRCR 当成相同题目。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=8|p8 Tables 2–3]]

索引复杂度由 $O(n^2)$ 变为 $O(n^2/r)$，在固定 $r$ 下仍是二次量级，不能称为全模型线性复杂度。1M 时的 7.6× prefill、4.9× decode 是 **attention 内核级**结果，包含 indexer 与 sparse core，对照 FlashInfer paged GQA。Prefill 测最后 16K chunk、batch=1；decode 为 batch=4、next_n=4，对应三个额外 MTP 预测步。该图未报告足以将结果换算为完整模型端到端延迟的全部成本，硬件具体型号在此实验段未给。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=9|p9 Figure 6、Efficiency Analysis]]

MTP 跨预测步复用 QSA top-k 索引，Table 4 的平均 accepted length 为 4.06/4.07。表称 four-step speculative decoding，图 6 则明确 next_n=4 对应三个 MTP 预测步；保留各自口径，不能把 accepted length 当作“接受率超过 100%”。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=8|p8 Table 4]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=9|p9 Figure 6]]

## 4. GR：增加残差存储宽度，把精细控制放在“读”上

### 4.1 四条残差流不意味着四套 Transformer

普通 pre-norm 子层从一条累积残差流读取；早期特征会与后来写入竞争。作者先扩成多分支，再研究读、写、分支间混合的复杂度是否值得。HC/mHC 的对照形式包含 read $H_{\rm mix}$、write $H_{\rm combine}$ 和分支混合 $H_{\rm res}$。GR 保留更精细的动态 read 与标量 write，去掉显式分支混合。其子层 $F$ 仍接收一个宽度 $d$ 的向量；扩宽的是残差存储，不是把全部 attention/MoE 计算复制四份。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=10|p10 §2.2、Eqs.21–28]]

令 $n_r=4$、每条流 $R_i\in\mathbb R^d$。先逐分支归一化，再从所有分支预测逐元素读门：

$$
\hat R_i=\operatorname{RMSNorm}(R_i;\gamma_i),
$$
$$
G=\operatorname{unvec}\,\sigma\!\left(
W_u\operatorname{SiLU}\!\left(\frac1{n_r}W_d\operatorname{vec}(\hat R)\right)\right),
\qquad
x=\frac1{n_r}\sum_{i=1}^{n_r}G_i\odot\hat R_i.
$$

低秩瓶颈宽度为 $d/8$。子层输出 $y=F(x)$ 再由每分支一个动态标量写回：

$$
s=2\sigma\!\left(\frac1{n_r}W_w\operatorname{vec}(\hat R)\right),\qquad
R_i'=R_i+s_i y.
$$

读门为“分支×通道”，写门为“分支”标量；没有 $H_{\rm res}R$ 的交叉混合，但分支仍通过共同生成门和共同子层输出发生信息关联，不能理解为四条完全互不影响的网络。读中已经有归一化与门控，**GR 替代子层原 pre-norm，不是在原 pre-norm 前再叠一层**。每层 attention 和 MLP 各有独立 GR 模块。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=11|p11 Eqs.29–34]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=12|p12 首三段]]

### 4.2 Loss 与 benchmark 的反例

Table 5 固定 25B-A3B、560B tokens、四分支：pre-norm→静态 mHC 的 loss 降 0.021，平均分提高 1.58；静态→动态只再降 0.002，平均分却提高 1.98。GR 为 loss 1.590、平均 54.66，动态 mHC 为 1.594、54.47，不能夸成 GR 对后者有巨大能力优势；设计取舍还包括去掉 $H_{\rm res}$ 所节省的一次完整残差读取和约束复杂度。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=11|p11 Table 5]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=12|p12 效率讨论]]

Table 6 的 Full AttnRes 不加 GN 时 loss 1.762，与 GR 相同；加 GN 后为 1.758。故该表不能支撑“GR loss 胜过所有残差方法”。不同表的模型/训练设置也不能直接混算。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=12|p12 Table 6]]

### 4.3 原路径图展示什么，不能证明什么

作者利用无 $H_{\rm res}$ 的累加结构，固定实际 forward 中的门值，分解早期子层输出对后续读入的向量贡献，再取各贡献范数占比 $\pi_{uv}$，比较 GR 与同设置单流参考模型的差 $\Delta_{uv}$。Figure 7 使用 20 层 MoE，展示 780 对路径中满足 $\Delta_{uv}\ge0.05$ 且至少跨一层的 21 条；一条分支主要保存早期输出，其他分支较局部。多个 checkpoint 出现相似模式，但分支编号本身可交换。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=12|p12–14 Eqs.35–37、Figure 7]]

这是对已实现前向计算的**贡献分解与观察**；范数占比不是“这条路径对正确答案的因果贡献率”，也没有证明删掉其余路径不会影响任务。作者确实尝试只保留最高门的两条分支：预训练 loss/分数变化小，后训练后明显退化，最终未采用。FP8 残差存储与融合读写内核则被采用；FP8 相对 BF16 将该状态的字节量减半，不代表整模型显存都减半。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=14|p14 Inference Efficiency]]

## 5. N-gram 表：增加静态查表容量，不能替代全部专家容量

以当前 token 结尾的短 n-gram 通过 multi-head hashing 查 embedding 表，再以 contextual gate 融入残差。索引只依赖输入 token，因此可以提前确定访问行，把主机传输与计算重叠。Layer 2 的选择不仅关乎表征，还为了用第一层计算掩盖预取延迟。报告未给最终 n-gram 阶数、每阶 heads、哈希函数、各表长度或完整融合方程；旧笔记中的代码细节不能填补此处。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=14|p14 §2.3]]

位置消融固定 n-gram 总参数预算，第二层平均分 47.94，第二+第二十五层 47.75，即便后者 loss 1.540 略低于 1.541，也没有变成更好的下游平均分。多层不具稳定收益，单层足够是这一消融范围内的选择，不是任意模型的普遍定理。该组实验以 300 tokens per active parameter 组织，不能把所有中等规模实验预算自动套给最终模型。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=14|p14 §2.3]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=15|p15 Table 7]]

必须区分两种扩容问题：

| 设置 | 哪个量固定 | 结果与含义 |
| --- | --- | --- |
| Table 8：表与专家争同一总参数预算 | 增加 n-gram 表时减少 MoE experts | loss 在 10× 基础词表、表占 25% 时最低，但域外 PPL 和下游没有同样明确最优点；不支持用表无损替代专家 |
| Table 9：额外增加表容量 | MoE 预算固定，总参数随表增大 | 20×→200× 时 loss 持续降，MATH、GSM8K、BBH 等饱和或波动；中文 C-Eval/CMMLU 随表规模持续提高 |

表中基础词表尺度为 250K。旧总结把 20×–200× 写成“固定预算”需要纠正：**固定的是 MoE 预算，不是模型总参数**。作者也尝试 token normalization、不同 n-gram 阶数间非均匀分配、频率分区，未观察到稳定收益。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=15|p15 Tables 8–9]]

## 6. Muon 与超参数：不能只把优化器名称换掉

### 6.1 按参数的数学角色划分优化器

Muon 对真正作为二维线性映射的矩阵做 momentum 正交化。报告使用 Nesterov momentum $\mu=0.95$、8 步 Newton–Schulz、Polar Express 系数安排；对形状 $A\times B$ 的更新缩放为 $\gamma(A,B)=0.2\sqrt{\max(A,B)}$。矩阵形状影响计算与尺度，参数个数不是全部成本。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=16|p16 §3.1 Orthogonalization]]

| 优化器 | 报告列出的对象 |
| --- | --- |
| Muon | attention q/k/v 与输出映射、GDN 输入/输出映射中的适用矩阵、routed/shared experts 的 fc1/fc2、n-gram 模块 key/value 投影 |
| AdamW | 输入 embedding、输出 head、MoE router、GR 两个低秩投影；output gates 的对照也更适合或不差于 AdamW |
| Adam（无 weight decay） | n-gram embedding 表 |

GDN decay/beta 投影每 head 只产生标量，不应当成普通二维语义映射正交化。摘要对非 Muon 对象作了概括，实际以 §3.1 更细的表/矩阵区分为准。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=16|p16 Which Parameters Use Muon、Splitting Fused Parameters]]

融合存储的 qkv、GDN 输入和 SwiGLU fc1 先拆分：qkv/GDN 按 head，fc1 按 gate/up，再分别做正交化并恢复布局。否则会混合语义独立子块的奇异方向，也用错更新缩放的矩阵形状。实现上通过 Canzona 按估计正交化 FLOPs 分配完整矩阵，跨 TP 重构矩阵，用 CUDA graph 减少大量小 kernel launch 成本。这是报告中的工程解释，本次未核代码。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=16|p16 Implementation]]

### 6.2 更大 batch 与学习率的验证条件

新结构/优化器改变最优超参数，所以作者重拟合而非照搬 Qwen3.5 配方。小模型长预算测试为 20 层 10.8B-A0.89B、4T tokens：batch 从 12.6M 到预测的 25.2M，同时采用对应学习率，最终 loss 从 1.5774 到 1.5702；37.7M 为 1.5707。由于 batch 和其配套学习率共同变化，不能把整个改进都归因于 batch 单一因素。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=17|p17 Figure 8、§3.2]]

把 batch 从 6.3M 逐步升至 25.2M 的两种 ramp 变体均未改善终点，并多用 18.8% optimizer steps。因此该配方去掉的是 **batch-size warmup**，不是取消 learning-rate warmup；Figure 13 仍明确标出学习率 warmup。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=18|p18 Batch-Size Warmup]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=21|p21 Figure 13]]

大模型短预算测试是 48 层 **156B-A7B**、419B tokens，不是最终 125B-A6B。预测设置为 batch 8.4M、学习率 $1.76\times10^{-3}$，与学习率乘除 $\sqrt2$、batch 增 25% 等比较；相近设置的 loss 差接近噪声。Table 10 作者明确每个 run 仅一次评估，小幅排名仅作观察，不能宣称已经完成严格统计显著性检验。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=18|p18–19 Figure 9、Table 10]]

### 6.3 稳定性的定义、门的单变量证据与仍保留的 clipping

压力测试在 28 层 25B-A3B 上固定学习率为最优值的 2×/4×，相同 batch、gradient clipping threshold=0.5；loss spike 定义为超过 201-step rolling median 0.1，同时观察 pre-clip gradient norm 的 p99.9/越阈次数和激活极值。在 4× 下，AdamW 旧结构有 183 spikes/10K steps；两个 Muon 版本都未越 clipping 阈值，Muon+GR 没有 loss spike。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=19|p19–20 Figures 10–11、Stress Test]]

更接近单变量归因的实验固定 AdamW、结构和数据顺序，仅开关 GatedNorm，在 3× 学习率下 spike 从 32.0 降到 3.2/10K steps，越阈次数从 256 降到 20。它支持 gate 对此设置的稳定性贡献；不是门能保证所有训练永不发散的证明。生产条件另比较前三个配方的前 276B tokens，观察到 GR 降低 loss 和梯度波动。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=20|p20–22 Figures 12–13、§3.3]]

“没有使用 qk-clip/SwiGLU-clip 等显式激活控制”不等于“完全没有任何梯度裁剪机制”：前述实验明确设置 gradient-norm clipping threshold。门使给定范围内较少触发阈值，与删除裁剪设施是不同主张。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=20|p20 Stress Test Design]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=22|p22 稳定性讨论]]

## 7. 最终评估：base model、语言任务与约 1/9 FLOPs

Table 11 比较 Qwen3.8-Flash-Next-Base、Qwen3.8-27B-Base、Qwen3.7-Plus-Base。Flash-Next 在 14 项上均高于 27B，在 8 项高于 397B-A17B 的 Qwen3.7-Plus，另 6 项差距最多约 2.6；例如 MMLU-Pro 73.23 对 70.90，但 MATH 72.78 对 74.38，MultiPL-E 79.09 对 81.68。这支持该组 base 评估里的能力/计算折中，不是对所有任务或后训练 agent 的胜出。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=23|p23 Table 11]]

评测包含 MMLU 5-shot、MMLU-Pro/SuperGPQA/GPQA 的 5-shot CoT、BBH 3-shot CoT、GSM8K/MATH 4-shot CoT、MGSM 8-shot CoT；EvalPlus 为四个代码测试集合的 0-shot 平均，MultiPL-E 为八语言 0-shot。CoT few-shot 条件不等于交互式 chat 或 RL agent。本段没有给出所有生成参数、最大输出、逐项重复次数和污染检查的完整配置，不能据表格重建全部运行协议。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=22|p22 §4]]

作者称激活参数和训练 tokens 各约为前代三分之一，训练 FLOPs 约九分之一。这是报告的相对预算陈述；完整最终训练 token 绝对数、端到端时长、硬件利用率和所有主机内存成本没有在此处完整公开。不能把 QSA 的约 202B CPT tokens 当作全训练总量，也不能把 FLOPs 比例等同于费用或墙钟时间比例。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=1|p1 Abstract]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=22|p22 §4–5]]

> [!important] 基线身份不能静默合并
> 引言将前代 397B-A17B 与 Qwen Team 2026 引文相连，参考文献对应 Qwen3.5；§4/Table 11 实际列名却是 Qwen3.7-Plus-Base。本页结果按表中具体名称登记，保留这一来源内的命名差异，不把它直接等同于 [[wiki/sources/models/qwen/Qwen-3.5|S029 的 Qwen3.5-397B-A17B 后训练模型卡]]。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=1|p1 §1]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=23|p23 Table 11]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=26|p26 Qwen Team 引文]]

### SWEBench-Pretrain 实际测到什么

报告自建这一变体：给 base model 问题描述和相关代码文件，要求生成 diff patch，以生成补丁与 golden patch 的**序列相似度**作为分数。其目标是给预训练模型提供可负担的代码修复代理测量，但不执行测试来验收修复。50.99 对 49.24 因而不能写成 50.99% 对 49.24% 的真实 issue resolution rate。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=22|p22 脚注1]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=23|p23 Table 11]]

从测量有效性看，文本接近参考补丁可能反映定位与补丁格式能力，却可能惩罚语义等价的不同修法，也可能奖励表面相近但功能错误的修改。报告未给样本规模/划分、相似度算法、相关代码选择过程、测试成功率或人工核验一致性的详细协议；因此它与真实工程修复之间的相关性尚未在这份材料中建立。这里的局限是由评分定义作出的本库分析，不是宣称该数据已被发现无效。本次未扩读或新建 SWE-bench/Agentless 来源。

## 8. 与冻结旧稿的关系及主题落点

旧总结的 GDN、QSA 两阶段与 GR 读写公式主线可由本报告回证，但有几处需要降低证据等级或纠正：

- 旧稿的 48 层、隐藏维度 2,560、专家数/Top-k、n-gram 阶数与哈希实现、qwen4_exp 代码路径均未由本次报告阅读完整验证；报告里的 48 层 156B-A7B 是超参数实验，不能移作最终模型结构表。
- 20×–200× n-gram 词表实验增加总参数，不能称总预算固定；主机 51B 表是额外容量。
- 旧稿的 Vision Encoder、PatchMerger、Interleaved MRoPE、图像 token 不进 n-gram 等代码讨论，不是本报告的视觉证据；保持二手输入身份，待有明确代码审计范围再核查。
- 旧稿与 Engram、Kimi/GLM/DeepSeek 的详细比较没有在本次扩读；“就是 Engram”“是 Qwen4 探索产物”等属于解释或推测，不能写成本报告确认的模型身份。
- 状态遗忘与优化器 weight decay 不是同一操作；稀疏 indexer 不是固定比率下的线性复杂度；GR 去掉混合算子也不意味着网络不存在跨分支信息关联。

与 [[wiki/sources/models/qwen/Qwen-3.5|S029]] 可比较混合 attention 的公开配置与本报告的机制消融；与 [[wiki/papers/models/qwen/Qwen3-VL|S028]] 可比较“多层视觉注入”与“多分支语言残差”如何处理不同信息通路，但两者不是同一模块，也没有本次统一实验。本页的主题联系包括语言骨干的压缩记忆/显式检索、残差读写与稳定性、参数/带宽/计算三类预算、loss 与任务测量的偏离。实际共享主题见页末。

## 实际整合关系

支撑语言端GDN误差更新、QSA因果块索引、GR残差读写与host查表，区分内核速度/loss/任务代理。

- [[wiki/architecture/Sequence-Memory-and-Retrieval|序列记忆与检索：固定状态、稀疏KV、残差流和查表容量分别保存什么？]]。
- [[wiki/efficiency/Resource-Ledger|资源账本：视觉token、激活参数、KV与系统预算分别省在哪里？]]。
- [[wiki/models/Family-Changes|家族变化轴：输入、接口、数据和计算怎样共同演进？]]。
- [[wiki/evaluation/Judges-and-Task-Success|裁判与任务成功：答案、解释、生成物和终态怎样分别取证？]]。
- [[wiki/reasoning/Overview|推理与交互：增加计算、改变观察、控制环境怎样分别起作用？]]。
