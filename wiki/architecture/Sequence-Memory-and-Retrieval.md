---
type: topic
created: 2026-10-31
updated: 2026-10-31
sources:
  - "[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf]]"
  - "[[raw/web/S029-Qwen-3.5/config.json]]"
  - "[[raw/web/S029-Qwen-3.5/README.md]]"
  - "[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf]]"
---

# 序列记忆与检索：固定状态、稀疏KV、残差流和查表容量分别保存什么？

多模态输入最后仍要经过序列骨干。**视觉接口决定送入什么，语言端记忆结构决定历史怎样被保留和访问。** Qwen3.8-Next报告提供语言骨干机制与预训练消融，S029只提供特定多模态checkpoint配置，DeepSeek-V4.1则把因果主干与cache/agent系统联动设计。三者证据粒度不同；本页不把语言任务分数升级成视觉实验证据。

## 固定状态记忆与显式历史检索可以共存

普通full attention显式保存过去token的KV，当前query可直接检索；滑窗只直接访问近邻，窗外影响依赖间接传播。Qwen3.8-Next的Gated DeltaNet（GDN）把历史压进固定大小矩阵状态，并每四层保留一层global attention；二者分别承担压缩记忆与显式检索。固定状态不能据名称保证保留所有细节。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=3|S030 · pp.3–5 §2.1.1、Table1]]

依报告转置约定，$q_t,k_t\in\mathbb R^{d_k}$、$v_t\in\mathbb R^{d_v}$、$S_t\in\mathbb R^{d_k\times d_v}$：

$$
\widetilde S_{t-1}=\alpha_tS_{t-1},\qquad
e_t=v_t-\widetilde S_{t-1}^{\top}k_t,
$$
$$
S_t=\widetilde S_{t-1}+\beta_tk_te_t^\top,
\qquad y_t=S_t^\top q_t.
$$

先读出旧状态对当前key的预测，再写误差$e_t$，是delta correction。**本库例子：**若衰减后的预测已等于$v_t$，本次误差为0，不会重复累加同一关联；删去负修正项就变成另一种递推。$\alpha$作用于运行状态，不等于优化器的weight decay；输出门、写入门和衰减门也控制不同位置。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=4|S030 · p.4 Eqs1–11]]

S029固定配置同样是45层linear/15层full的3:1布局，但配置文件没有完整状态方程和消融。不能因命名相似就把S030所有实现字段、最终结构与视觉行为回填到S029后训练checkpoint。[[raw/web/S029-Qwen-3.5/config.json|S029 · text_config.layer_types，commit8472618，2026-10-31]] [[raw/web/S029-Qwen-3.5/README.md#Model Overview|Model Overview]]

## 稀疏索引的压缩对象：索引key不等于最终内容

Qwen Sparse Attention把连续$r$个indexer key先平均，再归一化、以块起点施加partial RoPE；query仍保留自己的位置。indexer选块后展开回**原始token**供core attention，未满尾块另保留。固定$r$下，索引从$O(n^2)$变为$O(n^2/r)$，仍非线性复杂度；平均池化没有把最终attention内容也平均成一个值。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=5|S030 · pp.5–7 §2.1.2、Eqs12–20]]

因果条件要求块尾$p_b+r-1\le i$。以$r=4$、零起始query位置6为例，只能给0–3完整块打分，4–6作为tail，不能平均到未来位置7；到$i=7$后4–7才可参与top-k。该算例由mask推得，不是新增实验。teacher对块内attention概率取max构造监督，而indexer key取mean做表示；用途不同。训练先dense蒸馏indexer，再联合稀疏训练主干，直接切稀疏的退化支持训练适配必要性。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=6|S030 · pp.6–9 Eqs15–20、Fig.5]]

DeepSeek-V4.1的CSA2又分开cache复用与索引复用：Full生成global KV并选位置，Reindex复用KV但用自己的query重选，Reuse连索引也复用。decoder首Full扫描历史，形成最多16384位置候选池，后层再选Top512；固定候选限制后续打分，不取消首层扫描，也可能漏掉首池之外的信息。[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=10|S034 · pp.10–12 §2.3、Figs4–5]]

## 残差流保存的是层间特征，不是历史KV

Qwen3.8-Next Gated Residual扩展四条残差流，逐通道读门组合成一个$d$维输入给原attention/MLP，再按分支标量写回。**扩展的是残差存储，不是把整个Transformer复制四份，也不是四个视觉token。** 去掉显式跨分支混合仍有共同门和共同子层输出的关联。其读机制替代原pre-norm，不能再机械叠加一份norm。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=10|S030 · pp.10–12 §2.2、Eqs21–34]]

V4.1 Single-Pass mHC则把输入混合系数延后一block使用，便于融合读写kernel；报告残差路径activation traffic从$(4n+4)d$到$(2n+2)d$，不是全模型FLOPs减半。两者都研究残差通路，但不能仅凭多分支外观称为同一公式。[[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=12|S034 · pp.12–13 Eqs2–6]]

## n-gram容量是参数记忆，运行cache是序列状态

Qwen3.8-Next额外51B n-gram表通过输入token确定索引并从host预取，主干125B、激活6B另列；V4.1 Engram为196B条件记忆，在线host/RDMA与rollout驻GPU不同。它们是训练得到的查表参数，不是外部可编辑知识库，也不是当前会话的KV cache。查表仍有存储、通信、投影与门控成本。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=14|S030 · pp.14–15 §2.3、p.23 Table11]] [[raw/papers/models/deepseek/DeepSeek-V4.1-Flash.pdf#page=13|S034 · p.13 §2.4.2、p.18 §3.1.3]]

S030的表扩容实验分两种：固定总参数预算时表与专家争容量；固定MoE预算、额外加表时总参数增长。20×→200×属于后者。loss持续降而某些任务饱和，GR只保留两个最高门分支又在后训练退化，说明训练loss和局部proxy不能替代完整后训练验证。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=14|S030 · pp.14–15 Tables7–9]]

最终Table11是base语言任务比较，Qwen3.7-Plus-Base不能静默等同S029 Qwen3.5后训练模型。SWEBench-Pretrain按patch序列相似度评分，不执行测试；QSA的7.6×/4.9×是特定attention内核prefill/decode条件，不能直接当完整模型加速。机制、代理测量、端到端成本分别接[[wiki/evaluation/Judges-and-Task-Success|评测]]、[[wiki/efficiency/Resource-Ledger|账本]]和[[wiki/models/Family-Changes|家族变化]]。[[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=9|S030 · p.9 Fig.6]] [[raw/papers/architecture/language-backbones/Qwen3.8-Flash-Next.pdf#page=22|pp.22–23 §4、Table11、脚注1]]

## 实际来源入口

[[wiki/sources/models/qwen/Qwen-3.5|S029 Qwen-3.5]] · [[wiki/papers/architecture/language-backbones/Qwen3.8-Flash-Next|S030 Qwen3.8-Flash-Next]] · [[wiki/papers/models/deepseek/DeepSeek-V4.1-Flash|S034 DeepSeek-V4.1-Flash]]。原始定位在上文；唯一页保存身份、读取范围和实验条件。
