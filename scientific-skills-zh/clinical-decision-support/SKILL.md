---
name: clinical-decision-support
description: 为制药和临床研究环境生成专业的临床决策支持 (CDS)文件，包括患者队列分析（根据结果进行生物标志物分层）和治疗推荐报告（带有决策算法的循证指南）。支持 GRADE 证据分级、统计分析（风险比、生存曲线、瀑布图）、生物标志物集成和法规遵从性。输出针对药物开发、临床研究和证据合成进行优化的可发布 LaTeX/PDF 格式。
allowed-tools: Read Write Edit Bash
license: MIT License
metadata:
    skill-author: K-Dense Inc.
---

# 临床决策支持文档

## 说明

为制药公司、临床研究人员和医疗决策者生成专业的临床决策支持（CDS）文档。该技能专门研究为治疗策略和药物开发提供信息的分析性循证文档：

1. **患者队列分析** - 生物标志物分层组分析与统计结果比较
2. **治疗建议报告** - 具有 GRADE 分级和决策算法的循证临床指南

所有文档均生成为可出版的 LaTeX/PDF 文件，并针对药物研究、监管提交和临床指南制定进行了优化。

* *注意：** 对于床边的个体患者治疗计划，请改用 `treatment-plans` 技能。该技能侧重于药物/研究环境的组级分析和证据综合。

* *写作风格：**对于针对医学期刊的可出版文档，请参阅**venue-templates**技能的`medical_journal_styles.md`，以获取有关结构化摘要、证据语言和 CONSORT/STROBE 合规性的指导。

## 功能

### 文档类型

* *患者队列分析**
- 基于生物标志物的患者分层（分子亚型、基因表达、IHC）
- 分子亚型分类（例如，GBM 间充质免疫活性与原神经、乳腺癌亚型）
- 统计分析的结果指标（OS、 PFS、ORR、DOR、DCR)
- 亚组之间的统计比较（风险比、p 值、95% CI）
- 使用 Kaplan-Meier 曲线和对数秩检验进行生存分析
- 疗效表和瀑布图
- 比较有效性分析
- 药物队列报告（试验亚组，真实世界证据）

* *治疗推荐报告**
- 针对特定疾病状态的循证治疗指南
- 推荐强度分级（GRADE系统：1A、1B、2A、2B、2C）
- 证据质量评估（高、中、低、极低）
- TikZ的治疗算法流程图图表
- 基于生物标志物的治疗线测序
- 具有临床和分子标准的决策途径
- 制药策略文件
- 医学会临床指南制定

### 临床特征

- **生物标志物整合**：基因组改变（突变、CNV、融合）、基因表达特征、IHC标记物、PD-L1 评分
- **统计分析**：风险比、p 值、置信区间、生存曲线、Cox 回归、对数秩检验
- **证据分级**：GRADE 系统 (1A/1B/2A/2B/2C)、牛津 CEBM 水平、证据质量评估
- **临床术语**： SNOMED-CT、LOINC、正确的医学命名法、试验命名法
- **合规性**：HIPAA 去标识、保密标头、ICH-GCP 对齐
- **专业格式**：紧凑的 0.5 英寸边距、颜色编码建议、可出版、适合监管提交

## 制药和研究用途案例

此技能专为制药和临床研究应用而设计：

* *药物开发**
- **2/3期试验分析**：生物标志物分层功效和安全性分析
- **亚组分析**：显示患者亚组治疗效果的森林图
- **同伴诊断开发**：将生物标志物与药物反应联系起来
- **监管提交**：带有证据摘要的 IND/NDA 文件

* *医疗事务**
- **KOL 教育材料**：针对思想领袖的循证治疗算法
- **医疗策略文件**：竞争格局和定位策略
- **顾问委员会材料**：队列分析和治疗推荐框架
- **出版规划**：供同行评审的手稿分析期刊

* *临床指南**
- **指南制定**：采用专业协会GRADE方法进行证据合成
- **共识建议**：多利益相关者治疗算法开发
- **实践标准**：基于生物标志物的治疗选择标准
- **质量衡量**：基于证据的表现指标

* *真实世界证据**
- **RWE 队列研究**：根据 EMR 数据对患者队列进行回顾性分析
- **比较有效性**：现实环境中的头对头治疗比较
- **结果研究**：临床实践中的长期生存和安全性
- **健康经济学**：按生物标志物子组进行成本效益分析

## 何时使用

当您需要时使用此技能：

- **分析患者队列**，按生物标志物、分子亚型或临床特征分层
- **生成治疗推荐报告**，并提供临床指南或药物策略的证据分级
- **通过统计分析（生存率、缓解率、风险比）比较患者亚组之间的结果** 
- **制作药物研究文件**，用于药物开发、临床试验或监管提交内容
- **使用GRADE证据分级和决策算法制定临床实践指南**
- **在人群水平（而非个体患者）记录生物标志物引导的治疗选择** 
- **从多个试验或真实世界数据源合成证据**
- **创建临床决策算法**以及治疗排序流程图

* *不要使用此技能：**
- 个体患者治疗计划（使用 `treatment-plans` 技能）
- 床边临床护理文件（使用 `treatment-plans` 技能）
- 简单的患者特定治疗方案（使用 `treatment-plans` 技能）

## 通过科学原理图增强视觉效果

* *⚠️强制性：每份临床决策支持文档必须包含至少 1-2 个使用 scientific-schematics 技能的 AI 生成的图形。**

 这不是可选的。临床决策文件需要清晰的视觉算法。在最终确定任何文件之前：
1. 至少生成一个示意图或图表（例如，临床决策算法、治疗途径或生物标志物分层树）
2. 对于队列分析：包括患者流程图
3. 对于治疗建议：包括决策流程图

* *如何生成图形：**
- 使用 **scientific-schematics** 技能生成人工智能驱动的出版物质量图表
- 用自然语言简单描述您想要的图表
- Nano Banana Pro 将自动生成、审查和完善原理图

* *如何生成原理图：**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

人工智能将自动：
- 创建具有适当格式的出版质量图像
- 通过多次迭代进行审查和完善
- 确保可访问性（色盲友好，高对比度）
- 将输出保存在图形/目录中

* *何时添加示意图：**
- 临床决策算法流程图
- 治疗途径图
- 生物标志物分层树
- 患者队列流程图（CONSORT 式）
- 生存曲线可视化
- 分子机制图
- 任何复杂概念受益于可视化的

有关创建原理图的详细指导，请参阅scientific-schematics技能文档。

- --

## 文档结构

* *关键要求：所有临床决策支持文档必须以第1页的完整执行摘要开始，该摘要在任何目录或详细信息之前跨越整个第一页**

### 第 1 页执行摘要结构

每个 CDS 文档的首页应仅包含包含以下组件的执行摘要：

* *必需的元素（全部位于第 1 页）：**
1. **文档标题和类型**
  - 主标题（例如，“生物标志物分层队列分析”或“循证治疗建议”）
  - 带有疾病状态和焦点的副标题
 
2. **报告信息框**（使用彩色tcolorbox）
  - 文档类型和目的
  - 分析/报告日期
  - 疾病状态和患者群体
  - 作者/机构（如果适用）
  - 分析框架或方法
 
3. **主要结果框**（使用 tcolorbox 的 3-5 个彩色框）
  - **主要结果**（蓝色框）：主要功效/结果发现
  - **生物标志物见解**（绿色框）：关键分子亚型发现
  - **临床影响**（黄色/橙色框）：可操作的治疗影响
  - **统计摘要**（灰色框）：危险比、p 值、关键统计数据
  - **安全亮点**（红色框，如果适用）：严重不良事件或警告

  * *视觉要求：**
  - 使用 `\thispagestyle{empty}` 从第 1 页删除页码
  - 所有内容必须适合第 1 页（之前） `\newpage`)
- 使用具有不同颜色的彩色 tcolorbox 环境实现视觉层次结构
- 框应可扫描并突出显示最关键的信息
- 使用项目符号，而不是叙述性段落
- 在目录或详细部分之前使用 `\newpage` 结束第 1 页 

* *第一页 LaTeX 结构示例：**
```latex
\maketitle
\thispagestyle{empty}

% Report Information Box
\begin{tcolorbox}[colback=blue!5!white, colframe=blue!75!black, title=Report Information]
\textbf{Document Type:} Patient Cohort Analysis\\
\textbf{Disease State:} HER2-Positive Metastatic Breast Cancer\\
\textbf{Analysis Date:} \today\\
\textbf{Population:} 60 patients, biomarker-stratified by HR status
\end{tcolorbox}

\vspace{0.3cm}

% Key Finding #1: Primary Results
\begin{tcolorbox}[colback=blue!5!white, colframe=blue!75!black, title=Primary Efficacy Results]
\begin{itemize}
    \item Overall ORR: 72\% (95\% CI: 59-83\%)
    \item Median PFS: 18.5 months (95\% CI: 14.2-22.8)
    \item Median OS: 35.2 months (95\% CI: 28.1-NR)
\end{itemize}
\end{tcolorbox}

\vspace{0.3cm}

% Key Finding #2: Biomarker Insights
\begin{tcolorbox}[colback=green!5!white, colframe=green!75!black, title=Biomarker Stratification Findings]
\begin{itemize}
    \item HR+/HER2+: ORR 68\%, median PFS 16.2 months
    \item HR-/HER2+: ORR 78\%, median PFS 22.1 months
    \item HR status significantly associated with outcomes (p=0.041)
\end{itemize}
\end{tcolorbox}

\vspace{0.3cm}

% Key Finding #3: Clinical Implications
\begin{tcolorbox}[colback=orange!5!white, colframe=orange!75!black, title=Clinical Recommendations]
\begin{itemize}
    \item Strong efficacy observed regardless of HR status (Grade 1A)
    \item HR-/HER2+ patients showed numerically superior outcomes
    \item Treatment recommended for all HER2+ MBC patients
\end{itemize}
\end{tcolorbox}

\newpage
\tableofcontents  % TOC on page 2
\newpage  % Detailed content starts page 3
```

### 患者队列分析（详细部分 - 第 3 页+）
- **队列特征**：人口统计、基线特征、患者选择标准
- **生物标志物分层**：分子亚型、基因组改变、IHC概况
- **治疗暴露**：按亚组接受的治疗、剂量、治疗持续时间
- **结果分析**：缓解率（ORR、DCR）、生存数据（OS、PFS）、DOR
- **统计方法**：Kaplan-Meier 生存曲线、风险比、对数秩检验、Cox 回归
- **亚组比较**：生物标志物分层功效、森林图、统计显着性
- **安全性**：按亚组、剂量调整、停药划分的不良事件
- **临床建议**：基于生物标志物概况的治疗影响
- **图**：瀑布图、游泳者图、生存曲线、森林图
- **表格**：人口统计表、生物标志物频率、按亚组划分的结果

### 治疗建议报告（详细部分 - 第 3 页+）

* *第 1 页治疗建议执行摘要应包括：**
1. **报告信息框**：疾病状态、指南版本/日期、目标人群
2. **关键建议框**（绿色）：按治疗方案 
3 划分的前 3-5 级建议。 **生物标记决策标准框**（蓝色）：影响治疗选择的关键分子标记
4. **证据摘要框**（灰色）：支持建议的主要试验（例如，KEYNOTE-189、FLAURA）
5. **关键监控盒**（橙色/红色）：基本安全监控要求

* *详细部分（第 3 页+）：**
- **临床背景**：疾病状态、流行病学、当前治疗前景
- **目标人群**：患者特征、生物标志物标准、分期
- **证据审查**：系统文献综合、指南摘要、试验数据
- **治疗选项**：具有以下机制的可用疗法行动
- **证据分级**：每个建议的等级评估（1A、1B、2A、2B、2C）
- **按线推荐**：一线、二线、后续治疗
- **生物标志物引导选择**：基于分子谱的决策标准
- **治疗算法**：显示决策路径的 TikZ 流程图
- **监测方案**：安全性评估、疗效监测、剂量修改
- **特殊人群**：老年人、肾/肝损伤、合并症
- **参考文献**：包含试验名称和引文的完整参考书目

## 输出格式

* *强制首页要求：**
- **第1页**：带有3-5个彩色tcolorbox元素的整页执行摘要
- **第2页**：目录（可选）
- **第3页+**：包含方法、结果、图形的详细部分，表格

* *文档规格：**
- **主要**：LaTeX/PDF，边距为 0.5 英寸，用于紧凑、数据密集的演示
- **长度**：通常为 5-15 页（1 页执行摘要 + 4-14 页详细内容）
- **样式**：可出版，医药级，适合监管提交
- **第一页**：始终是跨越整个第1页的完整执行摘要（请参阅文档结构部分）

* *视觉元素：**
- **颜色**：
  - 第 1 页框：蓝色=数据/信息，绿色=生物标志物/建议，黄色/橙色=临床意义，红色=警告
  - 推荐框（绿色=强烈推荐，黄色=有条件，蓝色=需要研究）
  - 生物标志物分层（颜色编码分子）亚型）
  - 统计显着性（颜色编码的 p 值、风险比）
- **表格**：
  - 具有基线特征的人口统计数据
  - 按亚组划分的生物标志物频率
  - 结果表（按分子亚型划分的 ORR、PFS、OS、DOR）
  - 不良按队列划分的事件
  - 带有GRADE评级的证据汇总表
- **数字**：
  - 带有对数秩p值和风险数表的Kaplan-Meier生存曲线
  - 显示患者最佳反应的瀑布图
  - 具有置信区间的亚组分析的森林图
  - TikZ 决策算法流程图
  - 个体患者时间线的游泳图
- **统计**：95% CI 的风险比、p 值、中位生存时间、里程碑生存率
- **合规性**：根据 HIPAA 安全港进行去识别、专有数据的保密声明

## 集成

此技能与以下功能集成：
- **scientific-writing**：引文管理、统计报告、证据合成
- **clinical-reports**：医学术语、HIPAA 合规性、监管文档
- **scientific-schematics**：用于决策算法和治疗的 TikZ 流程图路径
- **treatment-plans**：队列衍生见解的个体患者应用（双向）

## Treatment-Plans Skill

的关键区别**临床决策支持（本技能）：**
- **受众**：制药公司、临床研究人员、指南委员会、医疗事务
- **范围**：人群水平分析、证据综合、指南制定
- **重点**：生物标志物分层、统计比较、证据分级
- **输出**：多页分析文件（通常 5-15 页）包含大量图表 
- **使用案例**：药物开发、监管提交、临床实践指南、医疗策略
- **示例**：“通过激素受体状态分析 60 名 HER2+ 乳腺癌患者的生存结果”

* *Treatment-Plans 技能：**
- **受众**：临床医生、患者、护理团队
- **范围**：个体患者护理计划
- **重点**：SMART 目标、针对患者的干预措施、监测计划
- **输出**：简明的 1-4 页可操作护理计划
- **使用案例**：床边临床护理、EMR 文档、以患者为中心的规划
- **示例**：“为新诊断的 2 型糖尿病的 55 岁患者制定治疗计划”

* * 何时使用：**
- 使用 **clinical-decision-support** 用于：队列分析、生物标志物分层研究、治疗指南制定、药物策略文件
- 使用 **treatment-plans** 用于：个体患者护理计划、针对特定患者的治疗方案、床边临床文件

## 使用示例

### 患者队列分析

* *示例 1：NSCLC 生物标志物分层**
```
> Analyze a cohort of 45 NSCLC patients stratified by PD-L1 expression (<1%, 1-49%, ≥50%) 
> receiving pembrolizumab. Include outcomes: ORR, median PFS, median OS with hazard ratios 
> comparing PD-L1 ≥50% vs <50%. Generate Kaplan-Meier curves and waterfall plot.
```

* *示例 2：GBM 分子亚型分析**
```
> Generate cohort analysis for 30 GBM patients classified into Cluster 1 (Mesenchymal-Immune-Active) 
> and Cluster 2 (Proneural) molecular subtypes. Compare outcomes including median OS, 6-month PFS rate, 
> and response to TMZ+bevacizumab. Include biomarker profile table and statistical comparison.
```

* *示例3：乳腺癌HER2队列**
```
> Analyze 60 HER2-positive metastatic breast cancer patients treated with trastuzumab-deruxtecan, 
> stratified by prior trastuzumab exposure (yes/no). Include ORR, DOR, median PFS with forest plot 
> showing subgroup analyses by hormone receptor status, brain metastases, and number of prior lines.
```

### 治疗建议报告

* *示例 1：HER2+ 转移性乳腺癌指南**
```
> Create evidence-based treatment recommendations for HER2-positive metastatic breast cancer including 
> biomarker-guided therapy selection. Use GRADE system to grade recommendations for first-line 
> (trastuzumab+pertuzumab+taxane), second-line (trastuzumab-deruxtecan), and third-line options. 
> Include decision algorithm flowchart based on brain metastases, hormone receptor status, and prior therapies.
```

* *示例 2：晚期 NSCLC 治疗算法**
```
> Generate treatment recommendation report for advanced NSCLC based on PD-L1 expression, EGFR mutation, 
> ALK rearrangement, and performance status. Include GRADE-graded recommendations for each molecular subtype, 
> TikZ flowchart for biomarker-directed therapy selection, and evidence tables from KEYNOTE-189, FLAURA, 
> and CheckMate-227 trials.
```

* *示例 3：多发性骨髓瘤治疗方案测序**
```
> Create treatment algorithm for newly diagnosed multiple myeloma through relapsed/refractory setting. 
> Include GRADE recommendations for transplant-eligible vs ineligible, high-risk cytogenetics considerations, 
> and sequencing of daratumumab, carfilzomib, and CAR-T therapy. Provide flowchart showing decision points 
> at each line of therapy.
```

## 主要功能

### 生物标志物分类
- 基因组：突变、CNV、基因融合
- 表达：RNA-seq、IHC 评分
- 分子亚型：疾病特异性分类
- 临床可操作性：治疗选择指导

### 结果指标
- 生存期：OS（总生存期）、PFS（无进展生存期）
- 缓解：ORR（客观缓解率）、DOR（缓解持续时间）、DCR（疾病控制）率）
- 质量：ECOG 表现状态、症状负担
- 安全性：不良事件、剂量调整

### 统计方法
- 生存分析：Kaplan-Meier 曲线、对数秩检验
- 组比较：t 检验、卡方检验、Fisher 检验精确
- 效应大小：风险比、比值比为 95% CI
- 显着性：p 值、多重测试校正

### 证据分级

* *GRADE 系统**
- **1A**：强烈推荐，高质量证据
- **1B**：强推荐，中等质量证据 
- **2A**：弱推荐，高质量证据
- **2B**：弱推荐，中等质量证据
- **2C**：弱推荐，低质量证据

* *推荐强度**
- **强**：效益明显大于风险
- **有条件**：存在权衡，患者价值很重要
- **研究**：证据不足，需要临床试验

## 最佳实践

### 用于队列分析

1. **患者选择透明度**：清楚记录纳入/排除标准、患者流程和排除原因
2. **生物标志物清晰度**：指定检测方法、平台（例如 FoundationOne、Caris）、切点和验证状态
3. **统计严谨性**：
  - 报告具有 95% 置信区间的风险比，而不仅仅是 p 值
  - 包括生存分析的中位随访时间
  - 指定使用的统计检验（对数秩、Cox 回归、Fisher 精确）
  - 适当时考虑多重比较
4. **结果定义**：使用标准标准：
  - 反应：RECIST 1.1，免疫治疗的 iRECIST 
  - 不良事件：CTCAE 版本 5.0
  - 性能状态：ECOG 或 Karnofsky
5. **生存数据呈现**：
  - 中位 OS/PFS，CI 为 95% 
  - 标志性生存率（6 个月、12 个月、24 个月）
  - Kaplan-Meier 曲线下方的风险表中的数字
  - 审查清楚地表明了 
6. **子组分析**：预先指定子组；明确标记探索性分析与预先计划的分析
7. **数据完整性**：报告缺失数据及其处理方式

### 对于治疗建议报告

1. **证据分级透明度**：
  - 一致使用 GRADE 系统（1A、1B、2A、2B、2C）
  - 记录每个等级的基本原理
  - 明确说明证据质量（高、中、低、极低）
2. **综合证据审查**：
  - 包括 3 期随机试验作为主要证据
  - 补充新兴疗法的 2 期数据
  - 注意真实世界证据和荟萃分析
  - 引用试验名称（例如 KEYNOTE-189、CheckMate-227）
3. **生物标志物指导建议**：
  - 将特定生物标志物与治疗建议联系起来
  - 指定测试方法和经过验证的测定
  - 包括伴随诊断的 FDA/EMA 批准状态
4. **临床可操作性**：每项建议都应有明确的实施指南
5. **决策算法清晰度**：TikZ 流程图应该明确，具有明确的是/否决策点
6. **特殊人群**：解决老年人、肾/肝损伤、怀孕、药物相互作用
7. **监控指南**：指定安全实验室、成像和频率
8. **更新频率**：定期更新的日期建议和计划

### 一般最佳实践

1. **首页执行摘要（强制）**：
  - 始终在第 1 页上创建涵盖整个第一页的完整执行摘要
  - 使用 3-5 个彩色 tcolorbox 元素突出显示关键发现
  - 第 1 页上没有目录或详细部分
  - 使用 `\thispagestyle{empty}` 并以`\newpage`
  - 这是最重要的页面 - 应该在 60 秒内可扫描 
2. **去识别化**：在生成文档之前删除所有 18 个 HIPAA 标识符（安全港方法）
3. **监管合规性**：包括专有药品数据的保密声明
4. **出版就绪格式**：使用 0.5 英寸边距、专业字体、颜色编码部分 
5. **再现性**：记录所有统计方法以启用复制
6. **利益冲突**：在适用时披露制药资金或关系
7. **视觉层次结构**：一致使用彩色框（蓝色=数据，绿色=生物标志物，黄色/橙色=建议，红色=警告）

## 参考文献

请参阅`references/`目录以获取有关以下内容的详细指导：
- 患者队列分析和分层方法
- 治疗建议开发
- 临床决策算法
- 生物标志物分类和解释
- 结果分析和统计方法
- 证据合成和分级系统

## 模板

请参阅`assets/` LaTeX 模板目录：
- `cohort_analysis_template.tex` - 具有统计比较的生物标志物分层患者队列分析
- `treatment_recommendation_template.tex` - 具有 GRADE 分级的循证临床实践指南
- `clinical_pathway_template.tex` - 用于治疗测序的 TikZ 决策算法流程图
- `biomarker_report_template.tex` - 分子亚型分类和基因组概况报告

* *模板功能：**
- 0.5 英寸边距，紧凑演示
- 颜色编码推荐框
- 人口统计、生物标志物、结果的专业表格
- 对 Kaplan-Meier 曲线、瀑布图、森林图的内置支持
- GRADE 证据分级表
- 药品文档的机密标题

## 脚本

请参阅 `scripts/` 目录以获取分析和可视化工具：
- `generate_survival_analysis.py` - 使用对数秩检验、风险比、95% 生成 Kaplan-Meier 曲线 CI
- `create_waterfall_plot.py` - 队列的最佳响应可视化分析
- `create_forest_plot.py` - 具有置信区间的亚组分析可视化
- `create_cohort_tables.py` - 人口统计、生物标志物频率和结果表
- `build_decision_tree.py` - 用于治疗算法的TikZ流程图生成
- `biomarker_classifier.py` - 患者按分子亚型分层算法
- `calculate_statistics.py` - 风险比、Cox 回归、对数秩检验、Fisher's 精确
- `validate_cds_document.py` - 质量和合规性检查（HIPAA、统计报告标准）
- `grade_evidence.py` - 用于治疗的自动 GRADE 评估助手建议
