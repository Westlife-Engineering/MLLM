# MLLM Wiki：阅读入口

**当前为初始化施工状态。** 主题地图先依据已完成登记范围阅读并经独立内容审查的 S001–S003 形成；其余来源按下表的真实状态导航，已读首稿仍须独立审核与跨来源深化。`read` 表示来源页登记的阅读范围，`integrating` 表示尚未完成整轮摄入验收。

本轮材料以视觉—语言为主；音频、3D等在地图材料中的出现，不代表已有相应一手论文覆盖。Obsidian 内显示与 PDF 跳转未实测。

## 材料与来源计数

| 口径 | 当前事实 |
| --- | --- |
| 用户原始文件 | 261份；旧笔记包、原论文、综述、讲义等按迁移清单保全，不等于261篇论文 |
| Raw文件 | 288份 = 261原始文件 + 1理念文章 + 26新增原始证据文件 |
| 旧独立材料工作对象 | 31个；多份旧总结可能指向同一作品身份 |
| 去重学术来源 | 31项 = 29论文/报告 + 2综述 |
| 其他登记来源 | 1份讲义 + 2项官方文档 |
| 统一来源登记 | 34项（S001–S034）；当前 registry 为 15 read、19 unread，未完成状态仍保留 |
| 当前 Wiki 知识页 | 24页 = 9张总览/主题地图 + 15张实际来源页；索引与日志不计知识页 |

计数依据：[[maintenance/migrations/2026-10-31-initialization.json|原件迁移清单]]、[[maintenance/source-registry.json|来源登记]]。完整范围、队列与既有检查点见 [[maintenance/research/R001-initialization|R001 初始化维护记录]]；未建来源页只在登记与队列保留，不制造待读空页。

## 主题地图与阅读路线

初读依次读基础、视觉、架构和训练；评估结果时接效率与评测；讨论多模态思考和系统交互时再读推理与模型变化轴。

| 页面 | 一句话入口 |
| --- | --- |
| [[wiki/overview\|MLLM 总览]] | 沿输入、视觉表示、连接、语言生成与验证串起研究问题。 |
| [[wiki/foundations/Formalization\|基础定义]] | 用信息、参数和任务证据三个层次理解 token、冻结和能力描述。 |
| [[wiki/vision/Overview\|视觉表示]] | 比较分辨率、patch、切片、压缩与位置组织各自改变的环节。 |
| [[wiki/architecture/Overview\|架构与接口]] | 区分共享参数、token 可见性、专用模块与视觉信息注入位置。 |
| [[wiki/training/Overview\|训练与数据]] | 按数据、目标、开放参数和预算读训练阶段。 |
| [[wiki/efficiency/Overview\|效率与成本]] | 分账视觉前端、接口、语言计算、训练状态和系统调用成本。 |
| [[wiki/reasoning/Overview\|推理与交互]] | 解释训练、搜索、工具和动作—观察循环怎样使用视觉证据。 |
| [[wiki/evaluation/Overview\|评测与证据]] | 将任务对象、判分规则、协议条件和代理指标分开。 |
| [[wiki/models/Overview\|模型演进]] | 沿机制变化轴读模型家族，避免以代际叙事代替因果比较。 |

## 综述与讲义

以下三份是当前主题综合的地图依据；具体模型在这些页面中的叙述保留综述/讲义转述身份，其他原论文的独立阅读以其唯一页为准。

| ID与唯一页 | 摘要 | 主方向 / 交叉落点 | 阅读 / 摄入 |
| --- | --- | --- | --- |
| S001 · [[wiki/surveys/Efficient Multimodal Large Language Models A Survey\|效率综述]] | 从组件、训练、数据与应用分析多模态效率，保留原综述疑点和性能表条件。 | 综述（不设技术主方向）；交叉落点见页末主题关系 | read / integrating |
| S002 · [[wiki/surveys/Perception, Reason, Think, and Plan A Survey on Large Multimodal Reasoning Models\|推理综述]] | 以推理载体、计算与交互组织路线，区分个案、任务地图、判分和作者展望。 | 综述（不设技术主方向）；交叉落点见页末主题关系 | read / integrating |
| S003 · [[wiki/lectures/VLM-2\|VLM-2讲义]] | 92页课程入口，串联共享/专用参数、连接、视觉输入、位置与模型家族。 | 讲义（不设技术主方向）；交叉落点见页末主题关系 | read / integrating |

## 论文与官方文档：按模块和主方向

下列页面存在且可进入；S004以后本阶段只作来源导航，其新结论尚未并入上述初始主题。未登记的交叉方向不凭模型名称推定，待实际跨来源综合后补充。

### vision/encoders

| ID与唯一页 | 类型与摘要 | 主方向 | 已登记交叉方向 | 阅读 / 摄入 |
| --- | --- | --- | --- | --- |
| S004 · [[wiki/papers/vision/encoders/ViT\|ViT]] | paper；视觉 Transformer 的 patch、预训练规模与迁移条件；原页定位见唯一页。 | vision/encoders | 未登记 | read / integrating |
| S005 · [[wiki/papers/vision/encoders/SoViT\|SoViT]] | paper；在计算预算下研究 ViT 的形状与规模配置。 | vision/encoders | 未登记 | read / integrating |
| S006 · [[wiki/papers/vision/encoders/NaViT\|NaViT]] | paper；以原生尺寸和序列打包组织视觉输入及样本边界。 | vision/encoders | 未登记 | read / integrating |
| S007 · [[wiki/papers/vision/encoders/AIMv2\|AIMv2]] | paper；以多模态自回归预训练学习大型视觉编码器。 | vision/encoders | 未登记 | read / integrating |

### vision/alignment

| ID与唯一页 | 类型与摘要 | 主方向 | 已登记交叉方向 | 阅读 / 摄入 |
| --- | --- | --- | --- | --- |
| S008 · [[wiki/papers/vision/alignment/CLIP\|CLIP]] | paper；以图文对比监督学习可迁移视觉表示及文本类别接口。 | vision/alignment | 未登记 | read / integrating |
| S009 · [[wiki/papers/vision/alignment/SigLIP\|SigLIP]] | paper；用 sigmoid 图文目标研究视觉语言预训练及批量条件。 | vision/alignment | 未登记 | read / integrating |
| S010 · [[wiki/papers/vision/alignment/SigLIP2\|SigLIP2]] | paper；组合图文与局部/密集监督，讨论多语言和不同视觉接口。 | vision/alignment | 未登记 | read / integrating |

### architecture/pretraining

| ID与唯一页 | 类型与摘要 | 主方向 | 已登记交叉方向 | 阅读 / 摄入 |
| --- | --- | --- | --- | --- |
| S011 · [[wiki/papers/architecture/pretraining/ALBEF\|ALBEF]] | paper；以先对齐后融合与动量蒸馏组织视觉语言预训练。 | architecture/pretraining | 未登记 | read / integrating |
| S012 · [[wiki/papers/architecture/pretraining/BLIP\|BLIP]] | paper；以统一理解/生成模型及数据自举组织视觉语言预训练。 | architecture/pretraining | 未登记 | read / integrating |

### architecture/connectors

| ID与唯一页 | 类型与摘要 | 主方向 | 已登记交叉方向 | 阅读 / 摄入 |
| --- | --- | --- | --- | --- |
| S016 · [[wiki/papers/architecture/connectors/Flamingo\|Flamingo]] | paper；用视觉重采样和跨注意力接入语言模型，研究交错输入与少样本使用。 | architecture/connectors | 未登记 | read / integrating |
| S017 · [[wiki/papers/architecture/connectors/BLIP-2\|BLIP-2]] | paper；用查询接口连接冻结视觉编码器与语言模型。 | architecture/connectors | 未登记 | read / integrating |
| S018 · [[wiki/papers/architecture/connectors/InstructBLIP\|InstructBLIP]] | paper；让指令进入视觉提取接口并组织多任务指令学习。 | architecture/connectors | 未登记 | read / integrating |

## 当前使用方式

来源页负责身份、读取范围和可回证细节；主题页负责机制、条件与问题综合。旧 TeX/PDF/Markdown 冻结在 Raw 笔记包，只作为旧理解输入，不作独立学术证据。后续原论文核读可能修订当前课程或综述解释，修订应回到相应唯一页和主题。

维护规则从 [[AGENTS|AGENTS]] 进入；已完成规则与迁移初验记录见 [[wiki/log|追加日志]]。本索引是本次交付时快照，后续新增来源页随下一次协调整合补入。
