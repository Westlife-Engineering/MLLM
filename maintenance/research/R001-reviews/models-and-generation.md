# R001 G 学术审查：模型与生成 S021–S034

审查者：独立 G（Astra/high）；日期2026-10-31。职责限于来源核心学术内容，不写 Wiki、Raw、登记表、索引、日志、Schema 或 Git。使用 academic-researcher、pdf；S022自建评测、S028自建测试与S030 SWEBench-Pretrain另按benchmark-paper-reading方法审查。原件由审查者重新打开提取正文并渲染关键页；D 交接只作导航，不作证据。

## 状态与范围

已完成 S021–S034，共14个唯一来源（12论文报告、2官方文档）、139条实质核查点。发现3项must-fix，主Agent修订后已全部回核关闭，当前must-fix为0。下文各来源段保留发现时状态，最新状态以末尾“修正闭环与最终结论”为准。此结论不代替整体研究验收或共享主题/图解审核。支持范围限所列页段；没有复现、运行模型、审核完整代码或实测Obsidian。

全部 S021–S034 的16个登记原始文件已重新计算SHA-256并与registry匹配；其中12 PDF、1 HTML、1 PNG、1 Markdown、1 JSON。身份另核首页/正文，不用哈希冒充文献身份核验。

## S021 MiniGPT-5

原件SHA-256 `496647dc686fa0955af3f7346940273e92052fd0828776747a35d8214549c9f1`。核读PDF pp.1、3–8、12–15；实际查看原页PNG p.3、4、6、7。首页确认v4/2025-12-09、三作者和题名单数Voken；同一模型不同题名前缀不能重复计数。

| 核查主张 | 原页证据 | 判定 |
| --- | --- | --- |
| 32个输入视觉特征与默认8个生成vokens分工不同 | p.3 §3.1、图2 | 支持；Wiki信息流正确 |
| voken隐藏状态经两层MLP、四层enc-dec与queries得到SD条件 | p.4 §3.2、式2；p.3图2 | 支持；未将Vicuna说成像素解码器 |
| LM位置损失与LDM图像监督、LCAP辅助损失不同 | pp.4–5式1–4 | 支持；冻结仍可反传的教学解释正确 |
| caption-free只限后续阶段；MMDialog至多一历史turn | p.12 A.2；p.5 §3.3 | 支持；未夸长对话 |
| CFG对mapper输入置零10%，不是简单空文本prompt | p.5式5 | 支持 |
| VIST FID366.62、故事内协议与final-step不同 | p.6表1；pp.13、15 B.3/表9 | 支持；不能由FID推出逐对象纹理身份 |
| 人评5000序列/每项2人；三项胜+平并非都>70% | pp.6–7表3及正文 | 支持；Wiki保留原文概括与数字冲突 |
| 删除LCAP/LDM与固定query存在不同指标折中 | pp.7–8表5/7 | 支持 |

无must-fix。未逐图核p.16–19演示、未查人评原始记录和代码；不背书实验可复现性。

## S022 LLaVA

原件SHA-256 `dc8bace378a282ea78caa9b5959306202fbfa3b8cedaf8a66541a9af18f4d3bf`。独立核读PDF pp.1、3–9、20；实际看p.4、5、7、9。首页确认Visual Instruction Tuning、四作者、NeurIPS 2023、v2/2023-12-11。

| 核查主张 | 原页证据 | 判定 |
| --- | --- | --- |
| 教师GPT-4只读caption/box文字，学生读图 | p.3表1与§3 | 支持 |
| 158K分为58K/23K/77K；数据类别扩展不等于逐条核图保证 | pp.3–4 | 支持 |
| CLIP网格线性投影到Vicuna，不含Q-Former | p.4图1/式1 | 支持 |
| 先只训W，后训W+LLM且视觉始终冻结；loss仅助手/停止 | p.5表2/§4.2 | 支持 |
| 595K、1epoch；158K、3epoch；8A100及4h/10h | p.5与p.20附录C | 支持；不含主干原预训练 |
| COCO90问与Wild60问测开放式指令回复，文本教师/参考/裁判需区分 | pp.6–7 §5.1表4/5 | 支持；相对85.1非正确率 |
| 固定输出三次裁判66.7±0.3不证明人类一致 | p.7表5脚注 | 支持；与生成三次推理67.3±2.0已区分 |
| ScienceQA90.92单模型与92.53组合；特征/规模消融有条件 | pp.8–9表7/8 | 支持 |

无must-fix。评测批判与正面方法解释均完整；未检验全部附录prompt、原始判分、代码或全部演示图。

## S023 LLaVA-1.5

原件SHA-256 `b7074a6dad218e0dd109f2a80311548d447e1cf4b9e31c002696985784cc05b9`。核读PDF pp.1、3–6、9–10；实际看p.4、5、9。首页确认四作者、v2/2024-05-15。

| 核查主张 | 原页证据 | 判定 |
| --- | --- | --- |
| 格式prompt协调短答/长答；Q-Former容量解释是作者假说 | p.3 §3.2表1 | 支持 |
| 336普通版、两层MLP、Vicuna1.5与HD224切块分开 | pp.3–4 §3.3；p.9 A.1；p.10 A.3 | 支持 |
| 558K/665K及数据单位、同图QA合并 | p.5表3；p.9表7/A.2 | 支持 |
| 1epoch、batch256/128、LR1e-3/2e-5、greedy解码 | p.10表9 | 支持 |
| 逐步累加实验不是全因素；分辨率/格式并非各项全升 | p.4表2 | 支持，Wiki所列数字逐项吻合 |
| 主表ScienceQA图像子集零样本不能比初版专门训练全测试组合器 | p.5 §4.1表3；S022 pp.8–9 | 支持 |
| HD局部网格、去padding、行末token与全局缩图 | p.4图2；p.9 A.1；p.6全局消融 | 支持 |
| 至多6块与最大672×448原文表述有范围歧义 | p.9 A.1.1 | Wiki保留而未擅改，合适 |

无must-fix。未逐图检查附录写作/多语言案例，不把表结构通过当成代码训练方案审计。

## S024 LLaVA-NeXT 官方网页

HTML SHA-256 `23029ba42dcf6bba3b006770a839f44e76b52763b600d8780ab2d9712d7c886e`；PNG SHA-256 `7f8ed15e0ef0d16843297e1deb4a5d7ac2f386e681e44690d939b543b6d1f848`。完整抽读已登记HTML，包括Results展开表、Detailed Technical Improvement、Model Card、Team；实际查看本地架构PNG。页内发布日2024-01-30与2026-10-31快照取得日已区分。

| 核查主张 | HTML标题/原图 | 判定 |
| --- | --- | --- |
| 4倍是像素数，有限AnyRes网格基础336 | 导语、Dynamic High Resolution、Model Card | 支持 |
| 局部块+缩小整图两路再展平给LLM | high_res_arch_v2.png | 支持；图块数没有冒充真实token数 |
| 删除TextCaps因与TextVQA训练图重合，换DocVQA/SynDog | Data Mixture | 支持 |
| 用户15K、GPT-4V回复、图表数据及不同LLM同时变化 | Data Mixture、Scaling LLM backbone | 支持 |
| 558K Connector/760K Full model粒度保留 | Model Card | 支持；未臆造逐模块冻结表 |
| 34B总参数34.75B、32×30h而非精确一天 | Model Card/导语 | 支持 |
| 13B MMMU36.2低于1.5 36.4；34B并非各项超过Gemini Pro | Results及展开表 | 支持 |
| 网页成绩与1.5论文小差异分源保留 | Results与S023 p.5 | 支持 |

无must-fix。未访问后续博客、未补抓示例图、未审训练代码；不声称此HTML等于发布当天原字节。

## S025 InternVL / InternViT

原件SHA-256 `a948f7499c06b8a6cb0073149f1b8f41d3acd10c4bb29fe79f250806f32e5fab`。核读PDF pp.1、4–6、8–9、11–12；实际查看p.4、5、8、12。首页确认InternVL题名、作者及v3/2024-01-15。InternViT为同报告组件。

| 核查主张 | 原页证据 | 判定 |
| --- | --- | --- |
| InternViT48层/宽3200/25heads/5903M；QLLaMA约8B与新增约1B不同 | p.4表1/§3.2 | 支持 |
| C直接视觉池化/G query池化，EOS文本；Chat有直接视觉+query双路 | p.5图4/§3.2 | 支持；Wiki没有误画成唯一query瓶颈 |
| 随机视觉与预训练语言阶段1全部训；阶段2冻结已有权重 | pp.6、12表20 | 支持 |
| 4.98B/1.03B集合与28.7B/1.6B曝光分开；196→224及mask | pp.5、12表2/20 | 支持 |
| ITC+ITM+ITG在新接口学习，不等于阶段2视觉继续训练 | p.6 §3.3 | 支持 |
| 第三阶段多种冻结/解冻配置，不能一句概括全部行 | p.4图3；p.8表9；p.12 A.3 | 支持；映射未明处已标记 |
| 同配置MLP13B TextVQA58.7低于LLaVA61.3；QLLaMA系统含不同PT/SFT | p.8表9 | 支持 |
| 表12只训MLP的665K对照，表示一致性为间接解释 | p.9表12 | 支持 |
| 图文编码20.4/28.6ms与聊天生成速度区分；364是检索微调 | pp.11–12表19/21 | 支持 |

无must-fix。未逐表复算所有分类/检索数据，未读后续系列代码。旧稿关于归一化的数学澄清正确，但不据此认定本报告实现。

## S026 Qwen-VL

原件SHA-256 `b4eca60ae9d3c1548242da02ece0e2f35ce23d3a983255830d98212aa92e3167`。核读PDF pp.1、3–8、19–24；实际查看p.4、19、20、22。首页确认九作者、v3/2023-10-13。

| 核查主张 | 原页证据 | 判定 |
| --- | --- | --- |
| bigG1.9B、adapter0.08B、语言7.7B，单层cross-attention固定256 queries | pp.3–4表1 | 支持 |
| query/key二维绝对位置；224/448压缩前256/1024，输出均256 | pp.3–4、20表8 | 支持；无损未被宣称 |
| 框归一化[0,1000)，坐标文字与ref/box；OCR可用quad | p.4 §2.2、p.19格式 | 支持 |
| 三阶段分别冻LLM、全解冻、冻ViT；预算与350K SFT | pp.5–6、20表8；p.4图3 | 支持 |
| 1.4B数据池、1.5B样本暴露与500B图文token分开 | pp.5、20 | 支持 |
| 监督蓝字与条件黑字不同，格式例子回答天气不匹配不作能力证明 | p.19原页 | 支持 |
| 查询数消融仅ViT-L224训练loss；窗口896更快但仍有总时间代价 | pp.21–23图7/8表10 | 支持 |
| base/chat分数不单调；文本比较应对intermediate初始化 | pp.7–8表4/5；p.23表11 | 支持 |

无must-fix。未审核完整OCR制造代码、全量数据、所有图示和部署。

## S027 Qwen2-VL

原件SHA-256 `30bb0f6c9babf910295d6b7cd34b6f54824236f68782664c3c93fbf4803275d0`。核读pp.1、3–6、10、12–16；实际查看p.4、5、14、15。首页确认Qwen Team作者、v2/2024-10-03。自建function-calling按benchmark-paper-reading审其测量对象与公开协议。

| 核查主张 | 原页证据 | 判定 |
| --- | --- | --- |
| 675M ViT、DFN初始化、动态视觉token及2×2合并 | pp.3–5表1/§2.1 | 支持 |
| ViT移除绝对PE用2D-RoPE，LLM采用三轴M-RoPE | pp.4–5图3 | 支持；模块未混淆 |
| 224图像64视觉位置加边界共66；文本三轴同ID、后模态max+1 | pp.4–5 | 支持 |
| 视频2fps、时间深度2的3D卷积、图像复制两帧、16K视频预算 | p.5 | 支持 |
| 600B+800B含图文token、仅监督文字；三阶段冻结不补造merger细节 | pp.5–6 | 支持 |
| 动态平均1924与固定3136各有胜负，放大不是单调增益 | p.14表7/图4 | 支持 |
| MRoPE消融用Qwen2-1.5B/ViT-L，80K外推另用72B | p.15表8/图5 | 支持 |
| 自建FnCall的TM/EM判函数/参数，53.2不是端到端成功 | pp.10、12–13 | 支持；不虚构人工一致性 |
| AITZ动作匹配、ALFRED虚拟+SAM、导航弱于专用系统 | pp.10、13 | 支持 |

无must-fix。未验证原始function-calling样本、完整judge及长附录全部演示。

## S028 Qwen3-VL

原件SHA-256 `ee075d08e67de1148d6437c6c1d481f7894183b8793905a2deb5f62664f49380`。核读pp.1、3–4、10–13、15、20、24–25；实际查看p.3、4、15、24、25。首页双日期差异属实。自建测试按benchmark-paper-reading审。

| 核查主张 | 原页证据 | 判定 |
| --- | --- | --- |
| SigLIP2动态训练、2D-RoPE+插值绝对PE，2×2 merger | p.3 §2 | 支持 |
| 三个ViT中间特征经专用merger加到LLM前三层 | pp.3–4图1/§2.2 | 支持 |
| Interleaved MRoPE为维度频率分配，文本时间戳每temporal patch前缀 | pp.3–4 §2.1–2.3 | 支持 |
| S0只Merger67B；S1/S2全参数各约1T；S3全参数100B/256K | p.4表1 | 支持 |
| SFT1.2M及1:2文本/多模态，Thinking筛选是模型条件而非绝对视觉必要性 | pp.10–11 | 支持 |
| 235B Thinking/Instruct有OCR与数学折中，V*85.9/93.7+非同一checkpoint控制 | p.15表2 | 支持 |
| 视频帧数/API预算不同；text-centric生成参数不能套全部视觉评测 | p.20 | 支持 |
| ViT与DeepStack消融不同骨干/预算；DeepStack有TextVQA微降 | p.24表11/12 | 支持 |
| NIAH256K原生与YaRN约1M不同；协议缺口保留 | p.25图3/§5.12.3 | 支持 |

**M-G28-01（待修复回核）：引用节号系统错位。** PDF p24实际§5.12.1/5.12.2，p25为§5.12.3，Wiki写§6.1/6.2/6.3；p10冷启动§4.2、p11蒸馏§4.3、pp.11–12 RL§4.4、pp.12–13 Thinking with Images§4.5，Wiki部分引用写§4.1/4.2/4.3。已通知主Agent；最小修改为引用节号，正文机制与数字无需随之改动。独立回核后方关闭。

未逐条核完整榜单、所有附录提示与模型内部实现。

## S029 Qwen3.5-397B-A17B 固定官方文档

README SHA-256 `bda4b24e975f65ac677985306ddbad33362e65064637660654c8bb7dea7edf50`；config SHA-256 `3ae7fa89c2f7d1354096418ddaf1331e9e0898a8ca11e804fb6dbaa087efb7da`。重新读取全config，读取模型卡全部正文、HTML表格与脚注、接口示例（仅阅读未执行）。原件身份为固定HF commit `8472618112abcbd45acbcdc58436aff4233c23f7` 的post-trained配置，不是已取得方法论文。

| 核查主张 | 文件定位 | 判定 |
| --- | --- | --- |
| 60层3:1线性/全attention，397B/17B及MoE10+1 | README Model Overview；config text_config | 支持 |
| DeltaNet16QK/64V、attention32Q/2KV、尺寸区别 | 同上 | 支持；未用字段猜完整递推 |
| vision27层/1152宽/patch16/temporal2/merge2 | config vision_config | 支持 |
| DeepStack索引为空，2304位置表非最终token固定长度 | config vision_config | 支持，限定此checkpoint |
| 默认rope_type非YaRN，262144原生与1010000外推、Plus默认1M不同 | config rope_parameters；README开头及Ultra-Long | 支持 |
| MTP一层配置、后端steps/draft候选不同 | config、SGLang/vLLM | 支持 |
| MathVision提示条件、BabyVision/V*工具、BrowseComp历史管理影响结果 | 两榜单脚注 | 支持，未制造裸模型排行榜 |
| 训练效率与百万环境是官方宣称，缺阶段/预算不补论文结论 | Highlights | 支持 |

无must-fix。未下载远端图片或权重、未运行示例、未审底层代码/外链评测协议；模型卡自建子集不扩成新增来源。

## S031 DeepSeek-VL

原件SHA-256 `09e6a250407a046b156a0f97c81ac681b57983d89c8287ccdc77d51e379692b9`；首页v2/2024-03-11、33页。核读pp.1、6–8、10–22；实际看p.10、12、14、16、19、22原页。

| 核查主张 | 原页证据 | 判定 |
| --- | --- | --- |
| 7B并行SigLIP384与SAM1024，576位置通道合并；小模型仅SigLIP | p.10 §3.1；p.16表4 | 支持；不是SAM输出分割mask给语言模型 |
| SAM 64²→96²→两次stride2→24²，独立linear后通道拼接 | p.10 §3.1 | 支持；位置数和2048维不混淆 |
| stage1仅adaptor；stage2视觉冻结；stage3 SigLIP可训SAM冻结 | pp.12–15图3/§3.2 | 支持；GPU限制与冻结边界一致 |
| 3.75M对齐数据、7B 15K/42K/10K步和256/2304/256 batch | pp.12、15–16表4 | 支持；训练天数保持作者报告身份 |
| 正文最终语言70%与Figure4 caption的相反比例有冲突 | p.13、p.14图4；p.21 warmup | 支持；Wiki保留冲突，不以图注静默改配方 |
| 公开多模态greedy、MMBench dev与语言保留并非全面提升 | pp.16–18表5/7 | 支持；GSM与MMLU差异保留 |
| 100人评题与99 GPT-4V裁判题不同，GPT相对胜出≠人类一致 | pp.18–19图6/7 | 支持；人评5.65与GPT4V6.3、各胜负计数可回证 |
| projector扩大数据不保证增益；联合预训练/融合消融有条件 | pp.19–22表8–10 | 支持；HybridMLP平均55.9并非每列最高 |

无must-fix。未核全部定性输出正确性或旧稿代码执行；主结论核对不等于独立人评/复现。

## S032 DeepSeek-VL2

原件SHA-256 `cff2bd0ad1656769d7447f0e3cf3a1885902333894f123bdac27fce05c97459e`；首页v1/2024-12-13、28页。核读pp.1、4–12、17、20；实际看p.5、10、11、12及p.12表头放大。

| 核查主张 | 原页证据 | 判定 |
| --- | --- | --- |
| 单一SigLIP-SO400M384，通常mn≤9；>2图停动态切块 | p.4 §2 | 支持；InfoVQA≤18另列，p.11脚注 |
| 729→196，局部网格重组并逐行newline，总210+1+14m(14n+1) | p.5图3/§2 | 支持；3×3=2017为透明推算 |
| Tiny MHA，Small/main MLA512；专家/激活/总参数口径不同 | p.5表1、p.10表2 | 支持；摘要概括没有覆盖Tiny例外 |
| 对齐ViT+MLP可训、LLM冻结；其余全训，visualLR0.1 | pp.9–10 §4.1/表2 | 支持；§3.1简称冲突已处理 |
| stage2约800B训练暴露，70%VL/30%text；非VL1相同比例 | p.6 §3.2、p.10表2 | 支持 |
| Grounding ref/det与0–999坐标、负例和跨图提示 | pp.7、9 | 支持；未夸为执行动作 |
| OCR主模型811低于Small834；文档指标保留split | p.11表3 | 支持 |
| MMBench83.1误标en test，实际79.6才为en test | p.12表4 | **M-G32-01 must-fix**；最小改法见下 |
| 无单独消融隔离tiling/MLA/MoE贡献；跨组grounding受训练条件影响 | pp.12、17、20 | 支持该限制；未补造复现条件 |

M-G32-01：初次反馈曾将83.1猜读为en dev，主Agent放大原表后纠正，审查者再次实际查看放大表头确认第一列为`MMBench (sum)`，第二列`MMBench (en test)`，第三列`MMBench-V1.1 (cn test)`。最终最小修正：**MMBench（原表标sum）83.1、MMBench-en test79.6、MMBench-v1.1 cn test79.2**；没有原文依据补写dev。待主Agent修后回核。

## S033 DeepSeek-OCR

原件SHA-256 `a7297788968f8ad9ed21bcd273110814e4889efbbc99bfea86dca12205797a90`；v1/2025-10-21、22页。核读pp.1、5–12、18–19；实际看p.5、6、10、11、12、19。

| 核查主张 | 原页证据 | 判定 |
| --- | --- | --- |
| SAM→两层stride2卷积→去patch embedding的CLIP串联 | p.5图3/§3.2.1 | 支持；4096→256发生在全局attention之前 |
| encoder380M、decoder3B/570Mactive，口径不同 | pp.5、7 | 支持；未将570M称整系统激活量 |
| native64/100/256/400与Gundam100n+256、Master256n+400 | pp.6–7图4/表1 | 支持；Master继续训练6M不等同条件 |
| Nvalid是padding有效位置估计，不是实际attention预算 | p.6式1；p.11表3 | 支持；图4 R文字矛盾被如实保留 |
| OCR1/2数据30M页、10Mchart/5Mchem/1Mgeometry，70/20/10配方 | pp.7–9 | 支持；结构解析不等于科学推理 |
| SAM/compressor冻结，CLIP及decoder可训；无SFT且非chatbot | p.10 §3.5；p.18图12注 | 支持；第一阶段小LM冻结未知未编造 |
| Fox100页600–1300tokens、tokenizer分子、64/100分母及precision | p.10表2 | 支持；4页长桶和59.1%限制保留 |
| OmniDocBench平均795≠每页上限；Master1853+200dpi+继续训练 | p.11表3 | 支持；dots英文text0.032优于0.049反例正确 |
| Table4 financial0.289原样、两表overall不静默合并 | p.12表4 | 支持；未按趋势“修正”原数 |
| deep parsing二次调用；context-memory是提案，OCR不足证一般推理 | p.12 §4.3.1、p.19图13/结论 | 支持；保留未做NIAH等作者边界 |

无must-fix。未独立审Fox判分代码、OCR示例逐字正确性或实际生产吞吐。Wiki的实验范围和可读性足以区分压缩预算、转写质量和推理主张。

## S034 DeepSeek-V4.1-Flash

原件SHA-256 `0cfdda19c8e1691b5226dd0d4949e2397051268e8a823c2fb61db94ea20c4ac0`；首页v1/2026-09-17、51页；两份旧总结不能拆来源。核读pp.1、7–16、19–24、29–37、48–51，其他正文按具体主张查定位。实际看p.7、9、10、14、16、20、24、29、33、35、36、50、51。

| 核查主张 | 原页证据 | 判定 |
| --- | --- | --- |
| 552B backbone+196B Engram；prefill8B/decode16B | p.7图3/§2.1 | 支持；不是552B包括全表 |
| DeepSeekViT32层1024宽patch14、2DRoPE、3×3unshuffle与MLP | pp.8、22 | 支持；1344²→1024位置为有条件推算 |
| modality-specific bias只影响专家选取，仍有sequence balance loss | pp.8、22 | 支持；aux-loss-free未夸零辅助loss |
| CED通用式与实际decoder只有Full层生产globalKV分开 | p.9式1、pp.11、22 | 支持；SWA本层KV并未共享 |
| Full/Reindex/Reuse区分存储与TopK；层调度2/8/14、20/24/28/32/36 | pp.7、10–12、22 | 支持；零起始换算正确 |
| 首Full扫描全部、后层候选最多16384再选512 | pp.11–12、22 | 支持；不是整个模型常数检索 |
| mainKV E2M1+16channelE4M3、indexerMXFP4、SWAFP8 | p.14 §2.4.4 | 支持；QAT后训练与RoPE后量化保留 |
| global890bytes/token与persistent1/8不同；72h/分钟TTL/10%DRAM条件 | pp.19–20、37 | 支持；非全运行时显存890bytes/token |
| encoder/decoder bounded replay128近似、后缀状态依cachehit改变 | p.20 §3.2.2 | 支持；未声称严格等价 |
| single-pass mHC移用Al-1、traffic(4n+4)d→(2n+2)d | pp.12–13式2–6 | 支持；不是整体FLOPs减半 |
| DSpark三层五draft且需验证；骨干冻结专训、后训梯度隔离 | pp.13–14 | 支持 |
| SinkhornMomentum带符号L2/RMS归一，非概率双随机矩阵 | pp.15–16式7/算法1、p.22 | 支持；K11不冒充收敛证明 |
| 47Bpair/236Btoken视觉训练、45T联合、7:1、28T解冻与34T扩1M | pp.15、21–23 | 支持；冻结与finalnorm例外正确 |
| 异步RL lengthbias与offpolicy两问题分开；40+teacher OPD | pp.30–32 | 支持；未把状态恢复称严格onpolicy |
| effort奖励式与未cap内点近似；实际曲线非单调 | p.29式8–10、pp.35、48–51 | 支持；图9/12可见回落，作者强措辞被限缩 |
| Base表DocVQA4shotLLMjudge与语言退化、后训表Pass@k/version | pp.24、32–33 | 支持；未把95.6拼为VL2同协议 |
| scaffold固定checkpoint但原生prompt/tools变；8/3samples非bestof | pp.34–35、48 | 支持；69.8–74.2等行数值可回证 |
| multiagent172golden、Almost@1逐rollout、wallclock非总算力 | pp.35–36图10 | 支持；8h峰值后回落与选择最强配置保留 |
| 最后一页“印刷页1” | 实际渲染PDF p.51 | **M-G34-01 must-fix**：页脚为51，删错误差异说明并修链接别名 |

除最后页码说明外，核心学术主张在已核范围支持。未审实现/权重、完整训练数据、工具版本运行、原始RL轨迹或统计显著性；优化模块整套结果不被当单变量因果证明。M-G34-01已交主Agent，待回核。

## S030 Qwen3.8-Flash-Next（D释放后补审）

原件SHA-256 `17db868acaa0b86caaf89cd9516e0a92f79d7e161431e5e274b70a3123d60ef7`；首页标题On the Design of Qwen3.8-Next Architecture: Evaluation, Efficiency, and Training Stability、Qwen Team；首页日期2026-09-01与arXiv v1侧栏2026-08-31并列正确，28页。核读pp.1–9、11–12、14–23及p.26身份引用；实际看p.2、4、6、8、9、11、15、20、21、23。SWEBench-Pretrain自建度量按benchmark-paper-reading方法核判分有效性，不扩读所引SWE-bench。

| 核查主张 | 原页证据 | 判定 |
| --- | --- | --- |
| 125B主干/6B激活与额外51B主机表；3GDN:1attention、CPT换QSA | pp.1–2图1、p.7、p.23表11 | 支持；未把51B忽略为无成本 |
| GDN转置约定dk×dv，先衰减、读取预测、写残差的delta项 | p.4式1–5 | 支持；展开式维度与负rankone项正确 |
| qkv卷积/SiLU、qkL2、两更新门及sigmoid输出门不同 | p.4式6–11 | 支持；NoPE后训练观察有条件 |
| GDN对照25B-A3B、400B+80B、8/9与7/9及EvalPlus反例 | p.5表1 | 支持；没推独立组件因果 |
| QSA key先mean后RoPE，完整块mask、K2048/r4与最多3tail | pp.6–7式12–16/19 | 支持；i=6教学例子由mask有效推出 |
| teacher做max pooling再归一、KL teacher→indexer；阶段2只选块 | pp.6–7式17–20 | 支持；mean/max分工未混淆 |
| QSA stage1仅indexer1000steps约2B，stage2联合8000steps约200B | p.7 Training Details | 支持；未充作最终全训练预算 |
| QSA普通任务7/8与MRCR128/256K降、512K/1M升但绝对下降 | p.8表2–4 | 支持；accepted length不是概率 |
| 7.6×/4.9×为内核，最后16Kchunk、batch1/4、nextn4；indexer仍O(n²/r) | p.9图5–6 | 支持；未外推全模型延迟或线性复杂度 |
| GR四残差分支、逐通道read/逐分支scalarwrite、无Hres但有共享耦合 | p.11式29–34、p.12 | 支持；替代pre-norm不重复叠层 |
| loss与task不同步，GR1.590/54.66 vs动态mHC1.594/54.47；AttnRes例外 | pp.11–12表5–6 | 支持；未夸胜所有残差方法 |
| ngram固定总预算与固定MoE额外表实验分开；Layer2主机预取 | pp.14–15表7–9 | 支持；旧稿“20–200×固定预算”得到纠正 |
| Muon矩阵、AdamW router/GR等、表Adam无WD；head/gateup拆分 | p.16 §3.1 | 支持；未将全部矩阵无差别Muon |
| batch/LR共同变，小模型4T与48层156B-A7B419B实验非最终模型 | pp.17–19图8–9/表10 | 支持；单次评估排名不当显著性证据 |
| 去batchwarmup非去LRwarmup；压力测试clip0.5、GatedNorm单变量贡献 | pp.18–22图10–13 | 支持；“无激活clip”未混为无gradientclip |
| Table11基线是Qwen3.7-Plus-Base，14项赢27B/8项赢397B；相对1/9FLOPs | pp.22–23表11 | 支持；与S029后训练模型卡没有混身份 |
| SWEBench-Pretrain由diff序列相似判分，非执行测试通过率 | p.22脚注1、p.23表11 | 支持；可操作测量目标与未知校准明确 |
| 报告直接证据为语言骨干，视觉接口/成绩未提供 | 全部正文结构及p.22–23评测 | 支持；旧视觉实现未升级原文证据 |

无must-fix。额外直接搜索冻结旧TeX核对“20–200×固定预算”、48层和视觉代码字段存在，相关降级不是凭空制造旧稿错误。未逐项复核旧PDF重绘图与代码，不声称实现、内核测速和所有定量表已复现。

## 修正闭环与最终结论

2026-10-31回读主Agent实际修订后的Wiki，并对照前述原页证据：

| 编号 | 原问题与修正 | 回核结论 |
| --- | --- | --- |
| M-G28-01 | Qwen3-VL p24消融应§5.12.1/5.12.2、p25 NIAH§5.12.3；冷启动/蒸馏§4.2–4.3、RL§4.4、Thinking with Images§4.5 | 来源页所有列出项已改，关闭；共享主题传播另由后续主题审核确认 |
| M-G32-01 | 83.1误标en test，修为原表sum；另列en test79.6、v1.1 cn test79.2 | 已改且与放大表头/行一致，关闭；审查者初报dev的猜读亦已撤回 |
| M-G34-01 | 第51页误称印刷页1 | 阅读范围与附录链接别名均改为51，实际页图确认，关闭 |

当前must-fix **0**。本文件记录的14个唯一来源（12论文报告、2官方文档）在已核范围通过核心学术审查，不等于全库Goal或主题/图解最终验收通过。16个登记原件哈希均匹配；HTML/Markdown/JSON来源未伪造PDF页码。审查核对的是主张与固定原件之间的关系；没有独立复跑基准、检查训练数据污染、审计全部模型代码、验证闭源基线、统计重算、Obsidian应用测试或宣称参考文献全部精读。

旧笔记纠错的依据主要为论文原文；另直接查验S030固定预算/48层/视觉字段，S031 SAM解释，S033 Instruction Tuning/冻结LLM/猜测全参数与后文冻结表的冲突，S034 196B总参数与MXFP4混写的旧TeX原句。没有把旧TeX作为支持新学术主张的证据。视觉检查覆盖上列实际打开的原页图表和公式；来源页文字与Mermaid逻辑核看不证明Obsidian内渲染。
