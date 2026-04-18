---
name: scientific-writing
description: 深度研究和写作工具的核心技能。用完整的段落撰写科学手稿（不要要点）。使用两阶段过程，(1)使用 research-lookup 勾勒出带有要点的章节大纲，然后 (2)转换为流畅的散文。 IMRAD 结构、引文（APA/AMA/温哥华）、图表、报告指南（CONSORT/STROBE/PRISMA），用于研究论文和期刊提交。
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 科学写作

## 概述

* *这是深度研究和写作工具的核心技能**——将人工智能驱动的深度研究与格式良好的书面输出相结合。生成的每份文档都经过全面的文献检索和通过 research-lookup 技能验证的引文的支持。

科学写作是精确清晰地交流研究的过程。使用 IMRAD 结构、引文（APA/AMA/温哥华）、图表/表格和报告指南（CONSORT/STROBE/PRISMA）撰写手稿。将这项技能应用于研究论文和期刊提交。

* *关键原则：始终以流畅的散文写出完整的段落。切勿在最终稿件中提交要点。** 使用两阶段过程：首先使用 research-lookup 创建包含要点的章节大纲，然后将这些大纲转换为完整的段落。

## 何时使用此技能

此技能应在以下情况下使用：
- 撰写或修改科学手稿的任何部分（摘要、引言、方法、结果、讨论）
- 使用 IMRAD 或其他标准格式构建研究论文
- 以特定样式格式化引文和参考文献（APA、AMA、温哥华、芝加哥、IEEE）
- 创建、格式化或改进图形、表格和数据可视化
- 应用特定于研究的报告指南（试验的 CONSORT、观察性研究的 STROBE、观察性研究的 PRISMA）评论）
- 起草符合期刊要求的摘要（结构化或非结构化）
- 准备稿件以提交给特定期刊
- 提高写作清晰度、简洁性和准确性
- 确保正确使用特定领域的术语和命名法
- 解决审稿人意见并进行修改手稿

## 科学原理图的视觉增强

* *⚠️ 强制：每篇科学论文必须包含图形摘要以及 1-2 个使用 scientific-schematics 技能由 AI 生成的附加图形。**

 这不是可选的。没有视觉元素的科学论文是不完整的。在最终确定任何文件之前：
1. **始终生成图形摘要**作为第一个视觉元素
2. 使用科学原理图 
3 生成至少一个附加原理图或图表。综合性论文最好有 3-4 个总图（图形摘要 + 方法流程图 + 结果可视化 + 概念图）

### 图形摘要（必需）

* *每一篇科学论文都必须包含图形摘要。** 这是论文的视觉摘要：
- 出现在文本摘要之前或紧随其后
- 将整篇论文的关键信息集中在一个摘要中image
- 适用于期刊目录显示
- 使用横向方向（通常为 1200x600 像素）

* *首先生成图形摘要：**
```bash
python scripts/generate_schematic.py "Graphical abstract for [paper title]: [brief description showing workflow from input → methods → key findings → conclusions]" -o figures/graphical_abstract.png
```

* *图形摘要要求：**
- **内容**：显示工作流程的视觉摘要，关键方法、主要发现和结论
- **风格**：干净、专业，适合期刊TOC
- **元素**：包括3-5个带有连接箭头或流程的关键步骤/概念
- **文本**：最小标签，大可读字体
- 日志：`[HH:MM:SS] GENERATED: Graphical abstract for paper summary`

### 附加图（广泛生成）

* *⚠️ 关键：在所有文档中广泛使用 scientific-schematics 和 generate-image。**

 每个文档都应该有丰富的插图。随意生成图形 - 如有疑问，请添加视觉效果。

* *最低图形要求：**

|文件类型 |最低 |推荐 |
|--------------|---------|------------|
|研究论文| 5 | 6-8 |
|文献评论| 4 | 5-7 |
|市场研究| 20 | 25-30 |
|演示 | 1/幻灯片| 1-2/幻灯片|
|海报| 6 | 8-10 |
|补助金 | 4 | 5-7 |
|临床报告| 3 | 4-6 |

* *广泛使用 scientific-schematics 绘制技术图表：**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

- 研究设计和方法流程图（CONSORT、PRISMA、STROBE）
- 概念框架图
- 实验工作流程插图
- 数据分析流程图
- 生物途径或机制图
- 系统架构可视化
- 神经网络架构
- 决策树、算法流程图
- 比较矩阵、时间线图
- 任何受益于原理图的技术概念可视化

* *广泛使用generate-image来呈现视觉内容：**
```bash
python scripts/generate_image.py "your image description" -o figures/output.png
```

- 概念的真实感插图
- 医学/解剖插图
- 环境/生态场景
- 设备和实验室设置可视化
- 艺术可视化、信息图表
- 封面图像、标题图形
- 产品模型、原型可视化
- 任何增强理解或参与的视觉效果

人工智能将自动：
- 创建具有适当格式的出版质量图像
- 通过多个审查和完善迭代
- 确保可访问性（色盲友好，高对比度）
- 将输出保存在图形/目录中

* *当有疑问时，生成图形：**
- 复杂概念→生成原理图
- 数据讨论→生成可视化
- 过程描述→生成图形流程图
- 比较→生成比较图
- 读者受益→生成视觉

详细指导请参考scientific-schematics和generate-image技能文档。

- --

## 核心功能

### 1. 稿件结构和组织

* *IMRAD 格式**：通过大多数科学学科使用的标准引言、方法、结果和讨论结构来指导论文。这包括：
- **简介**：建立研究背景，找出差距，陈述目标
- **方法**：详细研究设计、人群、程序和分析方法
- **结果**：客观地呈现研究结果，无需解释
- **讨论**：解释结果，承认局限性，提出未来方向

有关IMRAD结构的详细指导，参考 `references/imrad_structure.md`.

* *替代结构**：支持学科特定格式，包括：
- 评论文章（叙述性、系统性、范围界定）
- 病例报告和病例系列
- 荟萃分析和汇总分析
- 理论/建模论文
- 方法论文和协议

### 2. 具体章节写作指导

* *摘要写作**：撰写简洁、独立的摘要（100-250 字），以体现论文的目的、方法、结果和结论。支持结构化摘要（带有标记部分）和非结构化单段落格式。

* *引言开发**：建立引人注目的引言：
- 确定研究问题的重要性
- 系统地回顾相关文献
- 识别知识差距或争议
- 陈述明确的研究问题或假设
- 解释研究的新颖性和意义

* *方法文档**：通过以下方式确保重现性：
- 详细的参与者/样本描述
- 清晰的程序文档
- 有依据的统计方法
- 设备和材料规格
- 道德批准和同意声明

* *结果呈现**：呈现结果：
- 从主要结果到次要结果的逻辑流程
- 与图形和表格的整合
- 效果大小的统计显着性
- 客观报告，无需解释

* *讨论构建**：通过以下方式综合结果：
- 将结果与研究问题联系起来
- 与现有文献比较
- 诚实地承认局限性
- 提出机制解释
- 提出实际意义和未来研究

### 3.引文和参考文献管理

跨学科正确应用引文风格。综合风格指南，请参阅 `references/citation_styles.md`.

* *主要引用风格：**
- **AMA（美国医学会）**：编号上标引用，医学中常见
- **温哥华**：方括号内编号引用，生物医学标准
- **APA（美国心理学会） Association)**：作者日期文本引用，常见于社会科学
- **芝加哥**：注释-参考书目或作者日期，人文和科学
- **IEEE**：编号方括号，工程和计算机科学

* *最佳实践：**
- 尽可能引用主要来源
- 包括最近的文献（活跃领域最近 5-10 年）
- 平衡介绍和讨论中的引文分布
- 对照原始来源验证所有引文
- 使用参考管理软件（Zotero、Mendeley、EndNote）

### 4. 图表

创建有效的数据可视化以增强理解。有关详细的最佳实践，请参阅 `references/figures_tables.md`.

* *何时使用表格与图形：**
- **表格**：精确的数值数据、复杂的数据集、需要精确值的多个变量
- **图形**：最直观地理解趋势、模式、关系、比较

* *设计原则：**
- 使每个表格/图形具有完整的说明文字
- 在所有显示项中使用一致的格式和术语
- 用单位标记所有轴、列和行
- 包括样本大小（n）和统计注释
- 遵循“每1000个字一个表格/图形”指南
- 避免在文本、表格和图形之间重复信息

* *常见图形类型：**
- 条形图：比较离散类别
- 折线图：显示随时间变化的趋势
- 散点图：显示相关性
- 箱形图：显示分布和异常值
- 热图：可视化矩阵和模式

### 5. 按研究类型划分的报告指南

通过遵循既定报告标准确保完整性和透明度。有关全面的指南详细信息，请参阅 `references/reporting_guidelines.md`.

* *关键指南：**
- **CONSORT**：随机对照试验
- **STROBE**：观察性研究（队列、病例对照、横断面）
- **PRISMA**：系统评价和荟萃分析
- **STARD**：诊断准确性研究
- **TRIPOD**：预测模型研究
- **ARRIVE**：动物研究
- **CARE**：病例报告
- **SQUIRE**：质量改进研究
- **SPIRIT**：临床研究方案试验
- **干杯**：经济评估

每个指南提供检查表，确保报告所有关键方法要素。

### 6. 写作原则和风格

应用基本的科学写作原则。有关详细指导，请参阅 `references/writing_principles.md`。

* *清晰度**：
- 使用精确、明确的语言
- 首次使用时定义技术术语和缩写
- 保持段落内和段落之间的逻辑流程
- 在适当时使用主动语态以保持清晰

* *简洁**：
- 消除冗余单词和短语
- 倾向于较短的句子（平均 15-20 个单词）
- 删除不必要的限定符
- 严格遵守字数限制

  * *准确性**：
- 以适当的精度报告准确值
- 使用一致的术语贯穿
- 区分观察和解释
- 适当地承认不确定性

* *客观性**：
- 不带偏见地呈现结果
- 避免夸大发现或影响
- 承认相互矛盾的证据
- 保持专业、中立语气

### 7. 写作过程：从大纲到完整段落

* *关键：始终写完整段落，切勿在科学论文中提交要点。**

科学论文必须以完整、流畅的散文形式撰写。使用这种两阶段方法进行有效写作：

* *阶段 1：创建带有关键点的章节大纲**

开始新章节时：
1. 使用research-lookup技能收集相关文献和数据
2. 创建带有要点标记的结构化大纲：
  - 呈现的主要论点或发现
  - 引用的关键研究
  - 包括的数据点和统计数据
  - 逻辑流程和组织
3. 这些要点充当脚手架 - 它们不是最终的手稿

* *示例大纲（简介部分）：**
```
- Background: AI in drug discovery gaining traction
  * Cite recent reviews (Smith 2023, Jones 2024)
  * Traditional methods are slow and expensive
- Gap: Limited application to rare diseases
  * Only 2 prior studies (Lee 2022, Chen 2023)
  * Small datasets remain a challenge
- Our approach: Transfer learning from common diseases
  * Novel architecture combining X and Y
- Study objectives: Validate on 3 rare disease datasets
```

* *第二阶段：将关键点转换为完整段落**

大纲完成后，将每个要点扩展为适当的散文：

1. **将要点转换成完整的句子**，包含主语、动词和宾语
2. **在句子和想法之间添加过渡**（但是，此外，相反，随后）
3. **在句子中自然地整合引文**，而不是像列表
4那样。 **使用上下文和解释进行扩展**，要点省略
5. **确保每段中从一个句子到下一个句子的逻辑流畅**
6. **改变句子结构**以保持读者参与度

* *转换为散文的示例：**

```
Artificial intelligence approaches have gained significant traction in drug discovery 
pipelines over the past decade (Smith, 2023; Jones, 2024). While these computational 
methods show promise for accelerating the identification of therapeutic candidates, 
traditional experimental approaches remain slow and resource-intensive, often requiring 
years of laboratory work and substantial financial investment. However, the application 
of AI to rare diseases has been limited, with only two prior studies demonstrating 
proof-of-concept results (Lee, 2022; Chen, 2023). The primary obstacle has been the 
scarcity of training data for conditions affecting small patient populations. 

To address this challenge, we developed a transfer learning approach that leverages 
knowledge from well-characterized common diseases to predict therapeutic targets for 
rare conditions. Our novel neural architecture combines convolutional layers for 
molecular feature extraction with attention mechanisms for protein-ligand interaction 
modeling. The objective of this study was to validate our approach across three 
independent rare disease datasets, assessing both predictive accuracy and biological 
interpretability of the results.
```

* *大纲和最终文本之间的主要区别：**

|概要（规划阶段）|最终手稿 |
|----------------------------------------|--------------------|
|要点和片段|完整的句子和段落|
|电报|带有上下文的完整解释 |
|引文列表 |融入散文的引文|
|缩写的想法|发展了带有过渡的论证 |
|只为您的眼睛|对于出版和同行评审 |

* *要避免的常见错误：**

- ❌ **永远不要**在最终手稿中留下要点
- ❌ **永远不要**提交段落应为的列表
- ❌ **不要**在结果或讨论部分中使用编号或项目符号列表（研究等特定情况除外）假设或纳入标准）
- ❌ **不要**写句子片段或不完整的想法
- ✅ **做**只在方法中使用偶尔的列表（例如，纳入/排除标准、材料列表）
- ✅ **做**确保每个部分都像连贯的散文一样流动
- ✅ **做**大声朗读段落以检查自然流

* *当列表可接受时（有限情况）：**

列表仅可在特定上下文中出现在科学论文中：
- **方法**：纳入/排除标准、材料和试剂、参与者特征
- **补充材料**：扩展方案、设备列表、详细参数
- **绝不出现**：摘要、简介、结果、讨论、结论

* *摘要格式规则：**
- ❌ **绝不**使用带标签的部分（背景：、方法：、结果：、结论：）
- ✅ **始终**以自然过渡的流畅段落书写
- 例外：如果期刊在作者指南中明确要求，则仅使用结构化格式

* *与研究查找集成：**

The research-lookup 技能对于第 1 阶段（创建轮廓）至关重要：
1. 使用research-lookup
2 搜索相关论文。提取主要发现、方法和数据
3. 将调查结果组织为大纲中的要点
4. 然后在第 2 阶段将大纲转换为完整段落

这两个阶段的过程可确保您：
- 系统地收集和组织信息
- 在写作前创建逻辑结构
- 创作精美的、可发表的散文
- 保持对叙述流程的关注

### 8. 专业报告格式（非期刊文档）

对于研究报告、技术报告、白皮书和其他非期刊手稿的专业文档，请使用 `scientific_report.sty` LaTeX 风格包以获得精美、专业的外观。

* *何时使用专业报告格式：**
- 研究报告和技术报告
- 白皮书和政策简介
- 拨款报告和进度报告
- 行业报告和技术文档
- 内部研究摘要
- 可行性研究和项目可交付成果

* *何时不使用（使用特定于地点的格式）：**
- 期刊手稿 → 使用 `venue-templates` 技能 
- 会议论文 → 使用 `venue-templates` 技能
- 学术论文 → 使用机构模板

* *`scientific_report.sty` 样式包提供：**

|特色|描述|
|---------|-------------|
|版式| Helvetica 字体系列具有现代、专业的外观 |
|配色方案|专业蓝色、绿色和强调色|
|盒子环境 |彩色框显示主要发现、方法、建议、局限性|
|桌子|交替行颜色，专业标题|
|数字|一致的字幕格式 |
|科学命令| p 值、效应大小、置信区间的快捷方式 |

* *内容组织框环境：**

```latex
% Key findings (blue) - for major discoveries
\begin{keyfindings}[Title]
Content with key findings and statistics.
\end{keyfindings}

% Methodology (green) - for methods highlights
\begin{methodology}[Study Design]
Description of methods and procedures.
\end{methodology}

% Recommendations (purple) - for action items
\begin{recommendations}[Clinical Implications]
\begin{enumerate}
    \item Specific recommendation 1
    \item Specific recommendation 2
\end{enumerate}
\end{recommendations}

% Limitations (orange) - for caveats and cautions
\begin{limitations}[Study Limitations]
Description of limitations and their implications.
\end{limitations}
```

* *专业表格格式：**

```latex
\begin{table}[htbp]
\centering
\caption{Results Summary}
\begin{tabular}{@{}lccc@{}}
\toprule
\textbf{Variable} & \textbf{Treatment} & \textbf{Control} & \textbf{p} \\
\midrule
Outcome 1 & \meansd{42.5}{8.3} & \meansd{35.2}{7.9} & <.001\sigthree \\
\rowcolor{tablealt} Outcome 2 & \meansd{3.8}{1.2} & \meansd{3.1}{1.1} & .012\sigone \\
Outcome 3 & \meansd{18.2}{4.5} & \meansd{17.8}{4.2} & .58\signs \\
\bottomrule
\end{tabular}

{\small \siglegend}
\end{table}
```

* *科学记数法命令：**

|命令 |输出|用途 |
|---------|--------|---------|
| `\pvalue{0.023}` | *p* = 0.023 | P 值 |
| `\psig{< 0.001}` | **p* = < 0.001** |显着 p 值（粗体）|
| `\CI{0.45}{0.72}` | 95% CI [0.45, 0.72] |置信区间|
| `\effectsize{d}{0.75}` | d = 0.75 |效果大小|
| `\samplesize{250}` | *n* = 250 |样本大小|
| `\meansd{42.5}{8.3}` | 42.5±8.3|均值 SD |
| `\sigone`、`\sigtwo`、`\sigthree` | *、**、*** |意义星 |

* *入门：**

```latex
\documentclass[11pt,letterpaper]{report}
\usepackage{scientific_report}

\begin{document}
\makereporttitle
    {Report Title}
    {Subtitle}
    {Author Name}
    {Institution}
    {Date}

% Your content with professional formatting
\end{document}
```

* *编译**：使用 XeLaTeX 或 LuaLaTeX 进行正确的 Helvetica 字体渲染：
```bash
xelatex report.tex
```

 有关完整文档，请参阅to:
- `assets/scientific_report.sty`: 样式包
- `assets/scientific_report_template.tex`: 完整模板示例
- `assets/REPORT_FORMATTING_GUIDE.md`: 快速参考指南
- `references/professional_report_formatting.md`: 综合格式指南

### 9. 期刊特定格式化

根据期刊要求调整稿件：
- 遵循作者的结构、长度和格式指南
- 应用期刊特定的引文样式
- 符合图形/表格规范（分辨率、文件格式、尺寸）
- 包括所需的声明（资金、利益冲突、数据可用性、道德批准）
- 遵守每个部分的字数限制
- 格式根据提供的模板要求

### 10. 特定领域的语言和术语

调整语言、术语和惯例以匹配特定的科学学科。每个领域都建立了词汇表、首选措辞和特定领域的惯例，以表明专业知识并确保目标受众的清晰度。

* *识别特定领域的语言惯例：**
- 回顾目标期刊中最近的高影响力论文中使用的术语
- 注意特定领域的缩写、单位和符号系统
- 识别首选术语（例如，“参与者”与“受试者”、“化合物”与“药物”、“样本”与“样品”）
- 观察通常如何描述方法、生物体或技术

* *生物医学和临床科学：**
- 使用精确的解剖学和临床术语（例如，不使用“心肌梗死”）正式写作中的“心脏病”）
- 遵循标准化疾病命名法（ICD、DSM、SNOMED-CT）
- 首先使用通用名称指定药物名称，如果需要，在括号中指定品牌名称
- 使用“患者”进行临床研究，使用“参与者”进行社区研究
- 遵循人类基因组变异协会 (HGVS)遗传变异的命名法
- 用标准单位报告实验室值（大多数国际期刊中的SI单位）

* *分子生物学和遗传学：**
- 基因符号使用斜体（例如，*TP53*），蛋白质使用常规字体（例如，p53）
- 遵循物种特异性基因命名法（人类大写：*BRCA1*；小鼠句子大小写：*Brca1*）
- 在第一次提及时完整指定生物体名称，然后使用接受的名称缩写（例如，*大肠杆菌*，然后 *大肠杆菌*）
- 使用标准遗传符号（例如，+/+、+/-、-/- 表示基因型）
- 采用分子技术的既定术语（例如，“定量 PCR”或“qPCR”，而不是“实时” PCR")

* *化学和制药科学：**
- 遵循 IUPAC 化合物命名法
- 对新化合物使用系统名称，对众所周知的物质使用通用名称
- 使用标准符号指定化学结构（例如，SMILES、InChI 用于数据库）
- 使用适当的单位报告浓度（mM、μM、 nM 或 % w/v、v/v)
- 使用公认的反应命名法描述合成路线
- 使用与字段定义一致的术语，如“生物利用度”、“药代动力学”、“IC50”

* *生态和环境科学：**
- 使用物种的二项式命名法（斜体字：*Homo）智人*)
- 在相关时在第一个物种提及时指定分类权威
- 采用标准化栖息地和生态系统分类
- 对生态指标使用一致的术语（例如“物种丰富度”、“香农多样性指数”）
- 使用现场标准术语描述采样方法（例如“横断面”、“样带”、“样带”） “quadrat”，“标记-重新捕获”）

* *物理与工程：**
- 一致遵循 SI 单位，除非现场惯例另有规定 
- 使用物理量的标准符号（标量与矢量、张量）
- 使用现象的既定术语（例如，“量子纠缠”、“层流”）
- 指定设备的型号和制造商相关
- 使用符合现场标准的数学符号（例如，ℏ表示简化的普朗克常数）

* *神经科学：**
- 使用标准化的大脑区域命名法（例如，参考艾伦脑图谱等地图集）
- 使用已建立的立体定位系统指定大脑区域的坐标
- 遵循神经术语约定（例如，正式写作中的“动作电位”而不是“尖峰”）
- 根据测量方法适当使用“神经活动”、“神经元放电”、“大脑激活”
- 描述具有适当特异性的记录技术（例如“全细胞膜片钳”、“细胞外记录”）

* *社会和行为科学：**
- 在适当的时候使用以人为本的语言（例如，“精神分裂症患者”而不是“精神分裂症患者”）
- 采用标准化的心理结构和经过验证的评估名称
- 遵循 APA 指南以减少语言偏见
- 使用既定术语指定理论框架
- 使用人类研究的“参与者”而不是“受试者”

* *一般原则：**

* *匹配受众专业知识：**
- 对于专业期刊：自由使用特定领域的术语，仅定义高度专业化或新颖的术语
- 对于具有广泛影响力的期刊（例如*自然*、*科学*）：定义更多技术术语，为专业概念提供上下文
- 对于跨学科受众：平衡精度与可访问性，在第一次使用时定义术语

* *战略性地定义技术术语：**
- 在首次使用时定义缩写：“信使 RNA (mRNA)”
- 在为更广泛的受众写作时提供专业技术的简要说明
- 避免过度定义目标受众熟知的术语（表示不熟悉该领域）
- 如果有大量专业术语，则创建一个术语表不可避免的

* *保持一致性：**
- 始终对同一概念使用相同的术语（不要在“药物”、“药物”和“药物”之间交替使用）
- 遵循一致的缩写系统（在第一次定义后决定“PCR”或“聚合酶链式反应”）
- 始终应用相同的命名系统（特别是对于基因、物种、化学品）

* *避免字段混合错误：**
- 不要使用基础科学的临床术语（例如，不要称小鼠为“患者”）
- 避免使用口语或过于笼统的术语来代替精确的字段术语
- 不要在确保正确的情况下从相邻字段导入术语用法

* *验证术语用法：**
- 查阅特定领域的风格指南和命名法资源
- 检查目标期刊最近论文中术语的使用方式
- 使用特定领域的数据库和本体（例如，基因本体、MeSH 术语）
- 不确定时，引用关键参考文献建立术语

### 11. 要避免的常见陷阱

* *首要拒绝原因：**
1. 统计数据描述不恰当、不完整或不充分
2. 对结果的过度解释或无支持的结论
3. 影响重现性的方法描述不佳
4. 小的、有偏见的或不适当的样本
5. 写作质量差或文本难以理解
6. 文献综述或背景不充分
7. 不清楚或设计不当的图表和表格
8. 未能遵守报告准则

* *写作质量问题：**
- 时态混合不当（方法/结果使用过去时，既定事实使用现在时）
- 过多的行话或未定义的缩写词
- 破坏逻辑流程的段落中断
- 各节之间缺少过渡
- 符号不一致或术语

## 稿件开发工作流程

* *第1阶段：规划**
1. 确定目标期刊和审稿作者指南
2. 确定适用的报告指南（CONSORT、STROBE 等）
3. 概要稿件结构（通常是IMRAD）
4. 计划图表作为论文的主干

* *第二阶段：起草**（每个部分使用两阶段写作过程）
1. 从数字和表格（核心数据故事）
2开始。对于下面的每个部分，请遵循两个阶段的过程：
 - **第一**：使用研究查找使用项目符号点创建大纲
  - **第二**：使用流畅的散文将项目符号点转换为完整段落
3. 编写方法（通常最容易首先起草）
4. 结果草案（客观描述数字/表格）
5. 撰写讨论（解释调查结果）
6. 写引言（设置研究问题）
7. 工艺摘要（综合完整故事）
8. 创建标题（简洁和描述性）

* *记住**：要点仅用于计划 - 最终稿件必须是完整的段落。

* *第 3 阶段：修订**
1. 检查 
2 中的逻辑流程和“红线”。验证术语和符号
3 的一致性。确保图/表不言自明
4. 确认遵守报告准则
5. 验证所有引文是否准确且格式正确
6. 检查每个部分的字数
7. 语法、拼写和清晰度校对

* *阶段 4：最终准备**
1. 格式按期刊要求
2. 准备补充材料
3. 撰写突出重要性的求职信
4. 完成提交清单
5. 收集所有必需的陈述和表格

## 与其他科学技能的集成

此技能可以有效地与：
- **数据分析技能**：用于生成报告结果
- **统计分析**：用于确定适当的统计演示
- **文献综述技能**：用于情境化研究
- **图形创建工具**：用于开发出版质量的可视化
- **Venue-templates 技能**：针对特定地点的写作风格和格式（期刊手稿）
- **scientific_report.sty**：针对专业报告、白皮书和技术文档

### 专业报告与期刊手稿

* *选择正确的格式做法：**

|文件类型 |格式化方式 |
|------------------------|------------------------|
|期刊手稿|使用`venue-templates`技能|
|会议论文|使用`venue-templates`技能|
|研究报告|使用`scientific_report.sty`（此技能）|
|白皮书 |使用`scientific_report.sty`（此技能）|
|技术报告|使用`scientific_report.sty`（此技能）|
|拨款报告|使用 `scientific_report.sty`（此技能） |

### 特定场所写作风格

* *在为特定场所写作之前，请参阅 venue-templates 技能以获取写作风格指南：**

不同的地点有截然不同的写作期望：
- **自然/科学**：易理解、故事驱动、广泛意义
- **细胞出版社**：机制深度、图形摘要、亮点
- **医学期刊（NEJM、Lancet）**：结构化摘要、证据语言
- **机器学习会议（NeurIPS、ICML）**：贡献项目符号、消融研究
- **CS 会议（CHI、ACL）**：特定领域约定

venue-templates 技能提供：
- `venue_writing_styles.md`：大师风格比较
- 特定场地指南：`nature_science_style.md`、 `cell_press_style.md`、`medical_journal_styles.md`、`ml_conference_style.md`、`cs_conference_style.md`
- `reviewer_expectations.md`：审稿人在每个地点寻找什么

* *工作流程**：首先将此技能用于一般科学写作原则（IMRAD、清晰度、引文），然后咨询 venue-templates 

## 参考资料

此技能包括涵盖科学写作特定方面的综合参考文件：

- `references/imrad_structure.md`：IMRAD 格式和特定部分内容的详细指南
- `references/citation_styles.md`：完整的引文风格指南（APA、AMA、温哥华、芝加哥、 IEEE)
- `references/figures_tables.md`：创建有效数据可视化的最佳实践
- `references/reporting_guidelines.md`：特定于研究的报告标准和清单
- `references/writing_principles.md`：有效科学传播的核心原则
- `references/professional_report_formatting.md`：专业报告样式指南`scientific_report.sty`

## 资产

此技能包括用于专业报告格式的 LaTeX 样式包和模板：

- `assets/scientific_report.sty`：带有 Helvetica 字体、彩色框和有吸引力的表格的专业 LaTeX 样式包
- `assets/scientific_report_template.tex`：展示所有样式的完整报告模板特点
- `assets/REPORT_FORMATTING_GUIDE.md`：样式包快速参考指南

* *`scientific_report.sty` 的主要特点：**
- 现代、专业外观的 Helvetica 字体系列
- 专业配色方案（蓝色、绿色、橙色、紫色）
- 盒子环境：`keyfindings`、`methodology`、`resultsbox`、`recommendations`、 `limitations`、`criticalnotice`、`definition`、`executivesummary`、`hypothesis`
  - 具有交替行颜色和专业标题的表格
  - p 值、效应大小、置信区间的科学记数法命令
  - 专业标题和页脚

* *对于特定地点的写作风格**（语气、声音、摘要格式、审稿人期望），请参阅 **venue-templates** 技能，该技能为 Nature/Science、Cell Press、医学期刊、ML 会议和 CS 会议提供全面的风格指南。

 在从事科学写作的特定方面时根据需要加载这些参考资料。
