# IMRAD 结构指南

## 概述

IMRAD（简介、方法、结果和讨论）是原创研究的科学期刊文章的主要组织结构。自 20 世纪 70 年代以来已成为主流格式，现已成为医学、健康、生物、化学、工程和计算机科学领域的标准。

## 为什么选择 IMRAD？

IMRAD 结构反映了科学方法：
- **简介**：你问了什么问题？
- **方法**：你是如何学习的它？
- **结果**：你发现了什么？
- **讨论**：这是什么意思？

这个逻辑流程使科学论文更容易编写、阅读和评估。

## 完整的手稿组件

完整的科学手稿通常按顺序包括这些部分：

1. **标题**
2. **摘要**
3. **简介**
4. **方法**（也称为材料和方法、方法论）
5. **结果**
6. **讨论**（有时与结果结合）
7. **结论**（有时是讨论的一部分）
8. **致谢**
9. **参考**
10. **补充材料**（如果适用）

## 标题

### 目的
吸引读者并准确表达论文内容。

### 指南
- 简洁但具有描述性（通常为10-15个字）
- 包括关键变量和关系研究
- 避免缩写、行话和问题格式（除非期刊允许）
- 使其足够具体以区别于其他研究
- 包括可发现性的关键搜索词

### 示例
- 好：“高强度间歇训练对老年人心血管功能的影响”
- 太模糊：“运动与健康”
- 太详细：“一项随机对照试验，检验高强度间歇训练与中等连续训练对老年人心血管功能（通过最大摄氧量测量）的影响60-75 年"

## 摘要

### 目的
提供完整、独立的摘要，使读者能够决定全文是否与他们相关。

### 格式：流动段落（默认）

* *⚠️ 关键：将摘要写成流动段落，而不是带标签**

大多数科学论文都使用**非结构化摘要**，写成一两个连贯的段落。这是大多数期刊的标准格式，包括 Nature、Science、Cell、PNAS 和大多数特定领域期刊。

❌ **错误 - 带标签的结构化摘要：**
```
Background: Hospital-acquired infections remain a major cause of morbidity.
Methods: We conducted a 12-month before-after study...
Results: Post-intervention, surface contamination decreased by 47%...
Conclusions: UV-C disinfection significantly reduced infection rates.
```

✅ **正确 - 流畅的段落风格：**
```
Hospital-acquired infections remain a major cause of morbidity, yet optimal 
disinfection strategies remain unclear. We conducted a 12-month before-after 
study in a 500-bed teaching hospital to evaluate UV-C disinfection added to 
standard cleaning protocols. Environmental surfaces were cultured monthly and 
infection rates tracked via surveillance data. Post-intervention, surface 
contamination decreased by 47% (95% CI: 38-56%, p<0.001), and catheter-associated 
urinary tract infections declined from 3.2 to 1.8 per 1000 catheter-days (RR=0.56, 
95% CI: 0.38-0.83, p=0.004). No adverse effects were observed. These findings 
demonstrate that UV-C disinfection significantly reduces environmental contamination 
and infection rates, suggesting it may be a valuable addition to hospital infection 
control programs.
```

### 摘要结构（作为统一段落）

虽然写成流畅的散文，但摘要应按顺序涵盖这些元素：

1. **背景和问题**（1-2 句话）：为什么研究很重要，存在什么差距
2. **研究描述**（1-2 句话）：做了什么以及如何进行（研究设计、方法）
3. **主要发现**（2-4 句话）：具体定量数据的主要结果
4. **重要性**（1-2 句话）：解释、含义和结论

### 长度
- 通常为 150-300 个单词（检查期刊要求）
- 某些期刊允许最多 350 个单词

### 关键规则
- 写摘要**最后**（完成所有其他部分后）
- **写成流畅的段落** - 没有标记的部分
- 使其在不阅读论文的情况下完全理解
- 不要在摘要中引用参考文献
- 避免缩写或在第一次使用时定义它们
- 使用过去方法和结果的时态，结论的现在时
- 包括关键定量结果和统计测量
- 使用过渡自然地连接句子

### 何时使用结构化摘要（例外）

仅在以下情况下使用标记部分（背景/目标、方法、结果、结论）：
- 期刊**明确要求** 作者使用结构化摘要指南
- 常见于一些医学期刊（JAMA、BMJ、Annals of Internal Medicine）
- 在格式化之前务必检查期刊要求

即使对于结构化摘要，也将每个部分写成完整的句子，而不是片段。

### 示例：流动段落摘要

```
Transcriptomic aging clocks offer unique advantages for assessing biological age by 
capturing dynamic cellular states and acute responses to perturbations. Using the 
ARCHS4 database containing uniformly processed RNA-seq data from over 1.2 million 
human samples, we developed deep neural network models to predict chronological age 
from gene expression profiles. Our best-performing model achieved a mean absolute 
error of 4.2 years (R² = 0.89) on held-out test data, substantially outperforming 
traditional machine learning approaches including elastic net regression (MAE = 6.8 
years) and random forests (MAE = 5.9 years). Feature importance analysis identified 
genes enriched in senescence, inflammation, and mitochondrial function pathways as 
the strongest predictors. Cross-tissue validation revealed that lung and blood 
samples yielded the most accurate predictions, while liver showed the highest 
variance. These findings establish deep learning as a powerful approach for 
transcriptomic age prediction and identify candidate biomarkers for biological 
aging assessment.
```

## 简介

### 目的
让读者相信该研究使用适当的方法解决了一个重要问题。

### 结构和内容

* *第1段：大局**
- 建立广泛的研究区域
- 解释为什么这个主题很重要
- 对既定事实使用现在时
- 让非专业人士也能理解

* *第2-3段：缩小范围**
- 回顾相关的先前研究
- 显示已知的内容
- 识别现有工作中的争议或限制
- 创建一个通向差距的逻辑进展

* *第4段：差距**
- 明确识别仍然未知的内容
- 解释为什么这个知识差距是有问题的
- 将差距与大局重要性联系起来

* *最后一段：本研究**
- 陈述具体的研究问题或假设
- 简要描述总体方法
- 解释这项研究如何解决差距
- 可选：预览关键发现（一些期刊不鼓励这样做）

### 长度
- 通常为1.5-2 页（取决于期刊）
- 通常 4-5 段
- 信件/简短通信较短

### 动词时态
- **现在时**：既定事实（“锻炼改善心血管健康”）
- **过去时**：以前的研究及其发现（“史密斯等人发现”）那...”)
- **现在/过去时**：您的研究目标（“这项研究调查...”或“这项研究调查...”）

### 要避免的常见错误
- 起点太宽泛（例如，“从一开始...”）
- 详尽的文献综述（保存以供审查）文章）
- 引用不相关或过时的参考文献
- 未能确定明显的差距
- 研究的理由薄弱
- 没有陈述明确的研究问题或假设
- 包括方法或结果（这些属于后面的部分）

### 关键问题答案
1. 我们对这个话题了解多少？
2. 什么是我们不知道的？ （间隙）
3. 为什么这个差距很重要？
4. 这项研究的目的是找出什么？

## 方法

### 目的
为其他人提供足够的细节以复制该研究并评估其有效性。

### 关键原则
该领域的另一位专家应该能够完全按照您执行的方式重复您的实验。

### 标准小节

#### 研究设计
- 说明总体设计（例如，随机对照试验、队列研究、横断面调查）
- 如果不明显，请证明设计选择的合理性
- 如果适用，请提及盲法、随机化或对照

#### 参与者/受试者/样本
- 定义感兴趣的人群
- 准确描述纳入和排除标准
- 报告样本大小及其确定方式（功效分析）
- 解释招募方法和设置
- 对于动物：指定物种、品系、年龄、性别、居住条件

#### 材料和设备
- 列出使用的所有材料、试剂和设备
- 包括制造商名称和位置（在括号中）
- 指定专用项目的目录号
- 报告软件名称和版本

#### 程序
- 按时间顺序描述所做的事情
- 包括足够的详细信息复制
- 使用副标题组织复杂的程序
- 指定时间（例如，“在37°C下孵育2小时”）
- 用于调查/访谈：描述仪器、验证、管理

#### 测量和结果
- 定义所有变量测量
- 指定主要和次要结果
- 描述测量仪器及其有效性
- 包括测量单位

#### 统计分析
- 列出所有使用的统计测试
- 证明测试选择的合理性
- 说明显着性水平（通常α = 0.05)
- 报告样本量的功效分析
- 命名统计软件及其版本
- 描述缺失数据的处理
- 如果适用，提及多重比较的调整

#### 道德考虑
- 州IRB/道德委员会批准（经批准）编号）
- 提及知情同意程序
- 对于人类研究：声明遵守赫尔辛基宣言
- 对于动物研究：声明遵守相关指南（例如，到达）

### 长度
- 通常为2-4页
- 与研究成比例复杂度

### 动词时态
- **您执行的操作的过去时**（“我们测量...”、“参与者完成...”）
- **既定程序的现在时**（“PCR 放大...”、“调查问卷包含...”）

### 常见错误
- 复制细节不足
- 方法首次出现在结果中
- 包括结果或讨论
- 缺少统计测试
- 未定义缩写
- 缺乏道德批准声明

## 结果

### 目的
客观地呈现结果，无需解释。

### 关键原理
展示，请勿解读。保存讨论的解释。

### 结构和内容

* *开头段落**
- 描述参与者/样本特征
- 报告招募流程（例如，筛选、登记、完成）
- 考虑包括CONSORT风格的流程图

* *后续段落**
- 按逻辑顺序呈现结果（通常首先是主要结果）
- 遵循简介中规定的目标顺序
- 根据最清晰的内容按主题或按时间顺序组织
- 按编号参考图和表

* *每个发现应包括：**
- 观察到的结果结果
- 效果的方向
- 效果的大小
- 统计显着性
- 置信区间

* *示例**：“与对照组中的3 mmHg 相比，干预组的平均收缩压降低了12 mmHg（差异：9 mmHg，95%） CI：4-14 mmHg，p=0.002）。“

### 与图形和表格集成

* *何时使用：**
- **图形**：趋势、模式、分布、比较、关系
- **表格**：精确值、人口统计数据、多个变量

* *如何参考：**
- “图1显示...的分布”（不是“下面的图1”）
- “表2呈现基线特征...”
- 不要在文本中重复所有表格数据；突出显示主要发现
- 每个图/表应在文本中引用

### 图和表指南
- 按提及顺序连续编号
- 包括完整的独立标题
- 在标题或脚注中定义所有缩写
- 报告样本大小(n)
- 指示统计数据显着性（*、p 值）
- 使用一致的格式

### 统计报告

* *必需元素：**
- 检验统计量（t、F、χ2 等）
- 自由度
- p 值（如果 p > 则精确） 0.001，否则报告为“p < 0.001”）
- 效应大小和置信区间
- 样本大小

* *示例**：“各组在测试表现上存在显着差异（t(48) = 3.21，p = 0.002，Cohen's d = 0.87，95% CI： 0.34-1.40)."

### 长度
- 通常为 2-4 页
- 大致相当于方法长度

### 动词时态
- **过去时** 为您的发现（“平均值是...”，“参与者显示...“）

### 常见错误
- 解释结果（保存讨论）
- 重复文本中的所有表格/图形数据
- 提出新方法
- 统计细节不足
- 单位或符号不一致
- 不解决负面或意外的发现
- 选择性报告（应报告所有测试的假设）

### 组织策略

* *按目标：**
```
Effect of intervention on primary outcome
Effect of intervention on secondary outcome A
Effect of intervention on secondary outcome B
```

* *按分析类型：**
```
Descriptive statistics
Univariate analyses
Multivariate analyses
```

* *时间顺序：**
```
Baseline characteristics
Short-term outcomes (1 month)
Long-term outcomes (6 months)
```

## 讨论

### 目的
解释研究结果，将其与现有知识联系起来，承认局限性，并提出未来方向。

### 结构和内容

* *第 1 段：主要发现摘要**
- 重申主要目标或假设
- 用 2-4 个句子总结主要发现
- 避免重复结果中的细节
- 清楚说明假设是否得到支持

* * 第 2-4 段：上下文中的解释**
- 比较您的结果与先前研究的发现
- 解释与先前工作的一致和分歧
- 提出研究结果的机制或解释
- 讨论意外结果
- 考虑替代解释
- 解决研究结果是否支持或反驳现有理论

* *第5段：优点和局限性**
- 诚实地承认研究局限性
- 解释局限性如何影响解释
- 提及研究优势（设计、样本、方法）
- 避免一般性限制（“需要更大的样本”）——具体

* *第6段：影响**
- 临床影响（对于医学研究）
- 实际应用
- 政策影响
- 理论贡献

* *最后一段：结论和未来方向**
- 总结主要信息
- 建议未来的具体研究以解决差距或局限性
- 以强有力的结论结束陈述

### 长度
- 通常为3-5页
- 通常是最长的部分

### 动词时态
- **过去时**：你的研究结果（“我们发现......”，“结果显示......”）
- **现在时**：既定事实和你的解释（“这表明......”，“这些发现表明......”）
- **将来时**：含义和未来研究（“未来的研究应该调查......”）

### 讨论策略

* *与之前的工作相比：**
```
"Our finding of a 30% reduction in symptoms aligns with Smith et al. (2023), who
reported a 28% reduction using a similar intervention. However, Jones et al. (2022)
found no significant effect, possibly due to their use of a less intensive protocol."
```

* *提议机制：**
```
"The observed improvement in cognitive function may result from increased cerebral
blood flow, as evidenced by the concurrent increase in functional MRI signals in the
prefrontal cortex. This interpretation is consistent with the vascular hypothesis of
cognitive enhancement."
```

* *承认限制：**
```
"The cross-sectional design prevents causal inference. Additionally, the convenience
sample from a single academic medical center may limit generalizability to community
settings. Self-reported measures may introduce recall bias, though we attempted to
minimize this through structured interviews."
```

### 常见错误
- 简单地重复结果而不进行解释
- 过度解释结果或在没有根据的情况下声称因果关系
- 忽略不一致或负面的结果
- 未能与现有文献进行比较
- 引入新的数据或方法
- 对局限性进行一般或肤浅的讨论
- 超出研究范围的过度概括人口
- 缺少“那又怎样？”——未能解释重要性

### 要回答的关键问题
1. 这些发现意味着什么？
2. 它们与之前的研究相比如何？
3. 为什么会存在差异？
4. 有哪些替代解释？
5. 有什么限制？
6. 有什么实际意义？
7. 未来的研究应该调查什么？

## 结论

### 目的
提供主要发现及其意义的简明总结。

### 放置
- 可能是一个单独的部分或讨论的最后一段（检查期刊要求）

### 内容
- 最多 1-2 段
- 重述主要发现
- 强调意义或含义
- 以强有力的、令人难忘的陈述结束
- 不要引入新信息

### 示例
```
This randomized trial demonstrates that a 12-week mindfulness intervention significantly
reduces anxiety symptoms in college students, with effects persisting at 6-month follow-up.
These findings support the integration of mindfulness-based programs into university mental
health services. Given the scalability and cost-effectiveness of group-based mindfulness
training, this approach offers a promising strategy to address the growing mental health
crisis in higher education.
```

## 其他章节

### 致谢
- 感谢资金来源（附赠款编号）
- 致谢不符合作者身份的实质性贡献
- 感谢提供材料、设备或协助的人
- 声明任何利益冲突

### 参考文献
- 格式根据期刊风格（参见 `citation_styles.md`）
- 验证所有引文是否准确
- 确保所有引文出现在文本中，反之亦然
- 典型范围：原始研究的 20-50 条参考文献

### 补充材料
- 附加图形、表格或数据集
- 详细协议或调查问卷
- 视频或音频文件
- 大型数据集或代码存储库

## Tense 用法摘要

|部分|动词时态 |
|---------|-----------|
|摘要-背景|现在（既定事实）或过去（先前研究）|
|摘要-方法|过去|
|摘要-结果|过去|
|摘要-结论|目前|
|简介- 一般背景|礼物|
|简介-先前的研究|过去|
|简介 - 您的目标 |现在或过去|
|方法 |过去（你的行为），现在（一般程序）|
|结果 |过去|
|讨论 - 您的发现 |过去|
|讨论-解释|礼物|
|讨论 - 之前的工作 |现在或过去 |
|结论 |呈现 |

## IMRAD 变体

### 综合结果和讨论
- 一些期刊允许或要求这种格式
- 交织呈现和解释
- 每个结果呈现然后立即讨论
- 对于多个实验的复杂研究有用

### IMRaD 没有单独的结论
- 结论纳入最终讨论段落
- 在许多期刊中常见

### 扩展 IMRAD (ILMRaD)
- 添加“文献综述”作为单独的部分
- 在论文和论文中更常见

## 使 IMRAD 适应不同研究类型

### 临床试验
- 在结果中添加CONSORT流程图
- 在方法中包括试验注册号
- 在结果中报告不良事件

### 系统评价/荟萃分析
- 方法描述搜索策略和纳入标准
- 结果包括PRISMA流程图和综合
- 可能有附加部分（偏差评估风险）

### 病例报告
- 简介：病情背景
- 病例演示：替换方法和结果
- 讨论：将病例与文献联系起来

### 观察研究
- 遵循STROBE 指南
- 仔细注意方法中的潜在混杂因素
- 讨论地址因果关系限制

## 场地特定结构期望

### 期刊与会议格式

|场地类型 |长度|结构|方法安置 |重点聚焦 |
|---------|--------|-----------|--------------------|-----------|
| **自然/科学** | 2,000-4,500 字 |修改后的IMRAD |补充|广泛意义|
| **医疗** | 2,700-3,500 字 |严格的IMRAD |正文|临床结果|
| **领域期刊** | 3,000-6,000 字 |标准IMRAD |正文 |技术深度|
| **机器学习会议** | 8-9 页（约 6,000 字）|介绍-方法-实验-结论|正文（简洁）|小说贡献|

### ML会议结构（NeurIPS/ICML/ICLR）

* *典型8页结构：**
1. **摘要**（150-200字）：问题、方法、关键结果
2. **简介**（1页）：动机、贡献总结、相关工作概述
3. **方法**（2-3页）：技术方法、架构、算法
4. **实验**（2-3 页）：设置、数据集、基线、结果、消融
5. **相关工作**（0.5-1页，通常在附录中）：详细文献比较
6. **结论**（0.25-0.5 页）：总结、局限性、未来工作
7. **参考文献**（在页数限制内或根据会议分开）
8. **附录/补充**（无限制）：附加实验、证明、细节

* *与期刊的主要区别：**
- **贡献项目符号**：通常在介绍中编号列表（例如，“我们的贡献是：（1）...（2）...（3）...”）
- **没有单独的结果/讨论**：集成在实验部分
- **消融研究**：显示重要内容的关键组件
- **计算要求**：经常需要（训练时间、GPU、内存）
- **代码可用性**：越来越期望

### 节长度比例

|地点 |简介 |方法 |结果/实验|讨论/结论 |
|-------|--------|---------|----------------------|------------------------|
| **自然/科学** | 10% | 15%* | 40% | 35% |
| **医学（NEJM/JAMA）** | 10% | 25% | 30% | 35% |
| **领域期刊** | 20% | 25% | 30% | 25% |
| **机器学习会议** | 12-15% | 30-35% | 40-45% | 5-8% |

* 经常作为 Nature/Science 补充的方法

* *主要医学期刊特征：**
- NEJM/Lancet/JAMA：严格 IMRAD；临床重点；结构化讨论； CONSORT/STROBE 合规性
- 明确的主要/次要结果；统计预规范

* *关键机器学习会议功能：**
- 介绍中的编号贡献列表
- 带有伪代码/方程的方法详细信息
- 广泛的实验：主要结果、消融、分析
- 简要结论（指出限制）
- 相关工作经常在附录

### 写作风格（按场地）

|地点 |观众|简介焦点 |方法详情 |结果/实验|讨论/结论|
|------|----------|--------------|----------------|----------------------|----------------------|
| **自然/科学** |非专家|广泛意义|简要、补充|故事驱动|广泛的影响|
| **医疗** |临床医生|临床问题 |综合|主要成果优先 |临床相关性|
| **专业** |专家 |领域背景 |技术全面|通过实验|机械深度|
| **机器学习会议** |机器学习研究人员 |小说贡献 |可重复|基线、消融|简要、局限性|

* *ML会议重点：**
- **简介**：清晰的问题陈述；编号的捐款；定位与先前工作
- **方法**：数学符号；伪代码;架构图；复杂性分析
- **实验**：描述的数据集；多个基线；消融研究；错误分析
- **结论**：总结；承认局限性；更广泛的影响（如果需要）

### 跨场地评估

* *检查内容：**
- **适合**：适合场地范围和观众
- **长度**：在限制范围内（严格适用于会议）
- **清晰度**：写作质量足够；支持的声明
- **再现性**：方法能够复制
- **完整性**：报告的所有结果；承认局限性

* *常见拒绝原因：**
- 对场地意义不足
- 方法缺乏再现细节
- 结果不支持声明
- 讨论夸大了结果
- 超出页/字限制（会议严格）

* *机器学习会议具体评估：**
- 清晰的问题表述和动机
- 新颖性和贡献清晰明确超参数）

### 快速适配指南

* *期刊→ML会议：**
- Condense intro；添加编号的贡献
- 方法：保持简洁，添加伪代码
- 组合结果+讨论→实验部分
- 添加广泛的消融和基线比较
- 带有限制的简要结论

* *ML会议→期刊：**
- 用更多背景扩展介绍
- 单独的方法包含完整详细信息的部分
- 将实验拆分为结果和讨论
- 删除贡献编号
- 扩展限制讨论

* *专家→广泛期刊：**
- 简化介绍；强调广泛意义
- 移动技术方法进行补充
- 故事驱动的结果组织
- 引导有影响的讨论

* *广泛→专家：**
- 添加详细的文献综述
- 正文中的完整方法
- 通过实验组织结果
- 添加机制讨论深度

### 提交前结构检查表

* *所有场地：**
- [ ]字数/页数在限制内
- [ ]章节比例适当
- [ ]写作风格匹配场地
- [ ]方法启用重现性
- []承认的限制

* *ML 会议添加：**
- []明确列出贡献
- []包括消融研究
- []基线综合
- []超参数/种子报告
- [ ]代码可用性声明
