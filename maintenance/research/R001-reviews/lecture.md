# R001 独立学术审查：S003 / VLM-2

- 日期：2026-10-31（Asia/Shanghai）。角色 G，未参与讲义来源页撰写；不派子代理、不执行 Git，不修改 Raw、知识页、registry、索引或日志。
- 被审页：[[wiki/lectures/VLM-2]]。原件：[[raw/lectures/VLM-2.pdf]]。
- 本次重新读取最新 AGENTS.md、workflows/lint.md，应用 academic-researcher、course-pdf-knowledge 与 pdf 方法；从 Raw 原件独立提取页文本并渲染关键页。未用 D 的 handoff 或渲染图作为事实证明。
- 92 页、14,833,206 bytes；本次重算 SHA-256：`a81bcec1ed8f630632c2abccbba88bf3ddeaaab95f47aaa5fdf68596233b1a64`，与来源页登记一致。PDF 元数据创建和修改日期均为 2026-05-22，标题以实际封面为准，而非乱码的 PDF 元数据标题。
- “支持”表示当前笔记忠实反映讲义并正确标识本库解释，不表示独立验证讲义所引论文、官方模型规格或实验效果。本报告页码均从 PDF 首页起算。

## 结论

**S003 在本次代表性原页核查范围内，学术内容可接受，没有必须返工的事实或公式错误。** 其冻结范围、mask 可见性、动态视觉输入、位置编码、训练预算、课程图义及限制条件均能回到原页。p41 / p45 / p61 的问题确实存在于讲义中；笔记没有静默改原件，而是以明确的本库符号整理或歧义说明处理。

教学主线清楚：共享/专用参数 → 连接视觉与语言 → 输入和位置组织 → 家族实例 → 视觉表征训练。并未被课程勘误压过。只有两条非阻断的可选表达改进，见后文；不要求新增未读论文或补造缺失实现。

此结论不代表本轮全库 complete，也不代表讲义所列全部论文已读、实验已复现或 Obsidian 显示已经通过。

## 18 项代表性 claim 检查

| 编号 | 当前页主张 / 检查对象 | 判断 | 独立原页核对与边界 |
| --- | --- | --- | --- |
| S003-C01 | 课程身份、日期、版本、92页及读取范围 | 支持身份；原作者阅读行为无法独立确认 | p1 封面确为 Advanced Computer Vision / THU×SENSETIME–80231202、Chapter 3–Section 12、Vision Language Models–II、Dr. Li Yali、Acknowledge: Zeyuan Wu、Friday May 22 2026；页数和元数据日期吻合。G 本次不是全92页重读，不能独立证明 D 逐页看过的历史行为；当前阅读范围登记无结构上的明显矛盾。 |
| S003-C02 | VLMo MoME按模态 hard routing，共享 self-attention；三阶段冻结；检索双塔/分类融合 | 支持，第一段可选精炼 | p4 明写 modality of input token / hard routing / shared self-attention；p5 分 ITC、ITM、MLM 的信息流；p6 中间阶段 V-FFN 与 attention 有冻结斜线，正文明确只训 L-FFN，最后 whole model；p7 明示 two-tower retrieval 与 single-tower classification。注意参数共享不等于所有任务都交叉读取图文 token，当前后续任务表和单/双塔说明已基本消解这一潜在歧义。 |
| S003-C03 | BEiT-3 参数、数据规模及带划分/指标的成绩转录 | 支持 | p12 原图为40层、1408 hidden、6144 MLP、1.9B，数据21M pairs / 14M images / 160GB documents；p13 Table 4 的84.19/84.03、91.51/92.58、CIDEr147.6及 Karpathy test / 未用CIDEr optimization均吻合。没有把多任务指标加成统一分数，也没有将基线当预算匹配消融。 |
| S003-C04 | BLIP-2 三种 mask 与两阶段接口 | 支持 | p22 图中灰格masked、白格unmasked：ITC 的Q/T互不可见，ITM全部双向，生成mask允许文本读query及过去文本、query不读文本。p21明确representation/generative两阶段；p23 frozen image encoder与LLM、FC映射，以及OPT decoder-only / FlanT5 prefix-to-encoder接口与笔记一致。没有编造query数量。 |
| S003-C05 | InstructBLIP指令进入Q-Former与LLM；LLaVA第二阶段end-to-end仍冻结视觉编码器 | 支持 | p26 原图两处instruction箭头、冻结image encoder/LLM和instruction-aware visual features图注直接支持；p30第二阶段原文同时写End-to-End与visual encoder weights frozen，更新projection和LLM。笔记没有按术语扩大训练范围。 |
| S003-C06 | Mini-Gemini、NaViT、AnyRes是不同的高分辨率组织方式 | 支持 | p37 Q(N)、K&V(N×M²)、Tᵥ(N)与SDXL optional支持低分辨率query从高分辨率窗口挖取细节；p39明写same example内注意力与pad mask，并有patchify/token drop/packed sequence；p40有split与整图resize两支，网格集合与笔记一致。跨方案成本比较明确是本库框架，没有无依据给加速比例。 |
| S003-C07 | 绝对位置编码p41索引修正 | 支持 | p41左侧确写pᵢ,₂ₜ但正弦/余弦分子为k，投影式和右图均沿i定位。笔记统一成i，并将投影类索引改用a避免与通道t混用，是合理符号整理，且显式声明。正余弦分母指数2t/d转录正确。 |
| S003-C08 | RoPE二维旋转块、相对位移推导、Wq转置校正及“2D”标签边界 | 支持 | p43为单个2×2旋转块、标1D；p44–46标2D却仍只有位置索引m。p45末项确缺Wq转置。由qₘ=RₘWqxₘ和矩阵转置规则独立展开，得xₘᵀWqᵀRₘᵀRₙWkxₙ，再由RₘᵀRₙ=Rₙ₋ₘ得到笔记公式。不能从单个位置m声称已给h/w多轴公式；笔记区分正确。未宣称无限上下文外推。 |
| S003-C09 | M-RoPE把t/h/w与频率通道分开，interleaved改变频率分配 | 支持 | p47左图为t/h/w三支，右图TTTT/HHHH/WWWW对比THWTHW；p58帧位置三元组与文本同值三元组清楚。笔记依据图讲轴/频率区别，不补分配比例或源码实现，且未将后续设计全部归于页脚RoFormer。 |
| S003-C10 | Qwen家族比较保留课程身份；Qwen3 DeepStack、视觉merger及dense数量矛盾 | 支持 | pp48–52课程确有所述四变化轴及Qwen3.5概览；p54–55的初始化、cross-attention和冻结标记一致。p60 DeepStack箭头跨视觉深度接LLM多层；p61明确2×2→单token、默认SigLIP2-SO-400M、小LLM用300M Large，同时写three却列2B/4B/8B/32B四尺寸。数量矛盾说明必要，未擅改成外部官方事实。 |
| S003-C11 | Qwen3四阶段训练预算/序列长度及后训练 | 支持 | p62原表S0 Merger/67B/8192、S1 All/~1T/8192、S2 All/~1T/32768、S3 All/100B/262144全部一致；p63明列32k→256k、thinking/non-thinking格式、text-only strong-to-weak distillation与Reasoning/General RL。没有把累计token预算当单条序列长度或GPU成本。 |
| S003-C12 | DeepSeek-VL与VL2的冻结范围有差别 | 支持 | p65 Stage1只训adaptor，Stage2训adaptor+LLM且视觉图标冻结，Stage3正文限定低分辨率SigLIP-L+adaptor+LLM；不凭大火焰断言SAM-B也解冻。p70 VL2第一阶段明确train vision encoder and adaptor MLP / language fixed；后两阶段没有完整冻结明细。笔记正是转述课程，未把缺失实施细节补成事实。 |
| S003-C13 | DeepSeek-VL2整图/tiles序列结构及型号配置 | 支持 | p68原图区分整图与局部tiles、encode&merge、view separator与每行new line；p69表支持12/27/30层、Tiny MHA、后两者MLA rank512、64/64/72路由专家、2共享、topK6、Softmax/Softmax/Sigmoid及仅VL2 correction bias。笔记不把表扩成MLA推导。 |
| S003-C14 | CogVLM视觉专用Q/K/V和FFN仍在组合序列上注意力交互 | 支持 | p74公式及紫色/灰色双参数路径支持concat(XIWI,XTWT)，注意力算子接联合Q/K/V，而非独立双塔。笔记的行向量公式一致；对Tril只按因果mask简记解释，没有把上三角“置0后softmax”当实现。 |
| S003-C15 | Kimi K2.5图为交互系统；Toggle体现成绩/token权衡 | 支持 | p81 Obs箭头由环境回core loop、Act指向环境；有工具/Judge、rollout manager、推理/训练服务。p82左下5 improved/2 degraded，右下7 reduced/0 increased，轴含Overall。笔记未称所有成绩提高，也没由两图推导完整Toggle算法。 |
| S003-C16 | InternVL p83三阶段的训练/冻结标记与用途 | 支持 | p83 Stage1 InternViT-6B及LLaMA-7B均火焰；Stage2视觉与QLLaMA冰块、cross-attention火焰，并列matching/contrastive/generative；Stage3视觉/QLLaMA/cross-attention冻结、MLP火焰、Vicuna同时火焰和冰块。笔记保留最后标记歧义、不指定单一Vicuna策略，符合原图。InternViT没有另计论文来源。 |
| S003-C17 | SigLIP2各训练目标与20%图例边界 | 支持 | pp86–90总图及局部图显示sigmoid图文目标、LocCa captioning/dense/referring、EMA teacher/stop gradient；p87 AREF/GCAP含区域坐标与描述；p88 local-to-global self-distillation；p89 contrastive/self-distillation/masking并列；p90 MAP head。图标20%/100%确在，但这些页没有足以指定精确日程/损失权重/数据配比的文字。笔记不擅定含义恰当。p87 LocLa与LocCa拼写差异真实。 |
| S003-C18 | SigLIP2数据与训练累计量、模型规模和NaFlex | 支持 | p86原页10B images、12B alt-texts、109 languages、90/10语言页来源、batch32k、20k warmup、40B examples、2048 TPUv5e；p90 ViT-B86M/L303M/So400m400M/g1B与NaFlex variable aspect/resolution一致。笔记将原始数据规模和累计处理量分开，不推广到所有checkpoint。 |

## 必须返工

无。本次没有发现需要阻止来源页继续整合的错误或被引页不支持的核心结论。若后续用此页建立模型官方规格或原论文性能对照，仍须回到各唯一来源页的一手核读；本报告没有授予这种升级。

## 可选改进

### O1：VLMo“共享注意力”的一句话可更精确

位置：§1.1 第一段“共享注意力承担跨模态信息交互，专用FFN保留模态相关变换”。

建议：“不同模态复用注意力参数；在图文融合任务中，联合token序列通过注意力交互，专用FFN保留模态相关变换。”

理由：p5对比学习分支与p7双塔分别编码图像和文字。共享参数本身不保证每次前向中两个模态token相互读取。当前后续表格及单/双塔解释已经正确，所以这是降低初学者误读风险的表达优化，不是整节机制错误。

### O2：把 SigLIP2 表中的“分支”表头改成“目标 / 模块”

位置：§7 SigLIP2 四行表。

理由：LocCa、SILC、TIPS主要描述训练目标/方法，MAP head是池化模块。四行内容目前准确，表头统一为“目标 / 模块”能直接说明它们不属于同一层级；不需补数学损失、百分比含义或训练源码。

## 信息密度与教学表达判断

1. **主线有实际解释，不是目录和免责声明。** VLMo说明共享/专用参数，BLIP-2用mask解释信息可见性，LLaVA强调连接和训练是不同轴，NaViT/AnyRes比较输入组织，RoPE有符号、推导与结论，家族段落再回到这些轴。阅读层次与92页课程长度相称。
2. **勘误没有压过教学。** p41索引、p45转置直接影响公式理解，放在相邻概念处有用；p61数量矛盾只用短句处理；p87拼写说明简短；末尾回收问题便于查阅。没有必要为“少讲限制”删除这些可复查的精确说明。
3. **原件图义被转为文字。** mask、冻结标记、DeepStack、切片序列、teacher/student、动作观察方向等均解释其关系含义。并未靠一串英文术语替代机制；也没有把所有概念都强行画图。
4. **个别family名称仍依课程限定。** Qwen3.5 / Qwen3.5-VL、后期Kimi图等没有被用来声称独立核验官方型号或当前最新能力，范围控制恰当。
5. **结构与视觉验收分开。** 本次没有运行Markdown/Obsidian渲染；从源文本看公式分隔、aligned环境及Mermaid信息流可读，但不能据此报告应用显示通过。

## 覆盖与未覆盖

- 本次完整读取当前 `wiki/lectures/VLM-2.md`，重新读取规则；独立检查Raw字节与PDF元数据。读取了相关页提取文本，重要图表与公式采用重新渲染的原页视觉检查。
- 实际视觉核查：p1、4–7、12–13、22–23、26、30、37、39–41、43–47、55、58、60–62、65、68–70、74、81–83、86–90。另回读p3、21、31–32、48–52、54、63、67的提取文本用于局部定位；p31–32提取结果很少，未把它当作完整图审。
- **未覆盖：**未对全部92页做第二次全量阅读；未逐项复核Meta-Transformer、Florence-2、MiniGPT-4演示、MoE-LLaVA散点/训练图、CogVLM训练数据细表及全部示例。对每篇所引原论文均未追读，未上网核验官方规格、数据收录、性能或实现，不在本报告中给其独立已读身份。
- 未运行模型、复现实验、计算性能显著性、验证全部演示答案、推导讲义未给出的完整loss/训练日程，也未审计全部页脚引用。没有操作Obsidian或检查全库registry/索引/双向链接。
- 临时独立提取文本和PNG保存在 `C:/Users/ZENGZX/AppData/Local/Temp/mllm-kb-20261031/review/lecture/`。只有本报告与此前 `surveys.md` 的修订关闭记录是此次持久写入；Raw原件未改动。
