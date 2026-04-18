# 科学文档的专业报告格式

本参考指南涵盖科学报告、技术文档和白皮书的专业格式。使用 `scientific_report.sty` LaTeX 样式包实现一致、专业的输出。

- --

## 何时使用专业报告格式

### 使用此样式：

- **研究报告** - 内部和外部研究摘要
- **技术报告** - 详细的技术文档和分析
- **白皮书** - 立场文件和思想领导文件
- **拨款报告** - 进度报告和最终拨款报告
- **政策简报** - 基于研究的政策建议
- **行业报告** - 面向行业受众的技术报告
- **内部研究摘要** - 团队和利益相关者沟通
- **可行性研究** - 技术和研究可行性评估
- **项目文档** - 研究项目可交付成果

### 不要使用此样式：

- **期刊手稿** → 使用 `venue-templates` 技能进行期刊特定格式设置
- **会议论文** → 使用 `venue-templates` 技能进行会议要求
- **学术论文/学位论文** → 使用机构模板
- **同行评审的提交** → 遵循期刊作者指南

* *关键区别**：专业报告格式优先考虑一般读者的视觉吸引力和可读性，而期刊稿件必须遵循严格的出版商要求。

- --

## 概述science_report.sty

`scientific_report.sty`包提供：

|特色|描述|
|---------|-------------|
|版式| Helvetica 字体系列具有现代、专业的外观 |
|配色方案|协调的蓝色、绿色、橙色和紫色|
|盒子环境 |用于组织内容类型的彩色框|
|桌子|专业造型交替行|
|数字|一致的字幕格式|
|页眉/页脚|专业页眉和页脚|
|科学命令| p 值、效应大小、统计的快捷方式 |

### 基本文档设置

```latex
\documentclass[11pt,letterpaper]{report}
\usepackage{scientific_report}

\begin{document}
% Your content here
\end{document}
```

* *编译**：使用 XeLaTeX 或 LuaLaTeX 获得正确的 Helvetica 字体渲染：
```bash
xelatex document.tex
```

- --

## 内容组织的盒子环境

### 目的和用途

彩色盒子帮助读者快速识别不同类型的内容。有策略地使用它们来突出显示重要信息。

### 可用的盒子环境

|环境 |颜色 |用途 |
|-------------|--------|---------|
| `keyfindings` |蓝色|主要发现、发现、关键要点|
| `methodology` |绿色|方法、程序、研究设计|
| `resultsbox` |蓝绿色|统计结果、数据亮点|
| `recommendations` |紫色|建议、行动项目、影响|
| `limitations` |橙色|限制、注意事项、警告 |
| `criticalnotice` |红色|重要警告、安全注意事项|
| `definition` |灰色|定义、注释、补充信息 |
| `executivesummary` |蓝色（阴影）|执行摘要|
| `hypothesis` |浅蓝色 |研究假设|

### 关键发现框

用于重大发现和重要发现：

```latex
\begin{keyfindings}[Research Highlights]
Our analysis revealed three significant findings:
\begin{enumerate}
    \item Treatment A was 40% more effective than control (\pvalue{0.001})
    \item Effect sizes were clinically meaningful (\effectsize{d}{0.82})
    \item Benefits persisted at 12-month follow-up
\end{enumerate}
\end{keyfindings}
```

* *最佳实践：**
- 谨慎使用（每章最多1-3个）
- 保留真正重要的内容研究结果
- 包括具体数字和统计数据
- 写得简洁

### 方法框

用于突出显示方法和程序：

```latex
\begin{methodology}[Study Design]
This double-blind, randomized controlled trial employed a 2×2 factorial
design. Participants (\samplesize{450}) were randomized to one of four
conditions: (1) Treatment A, (2) Treatment B, (3) Combined A+B, or
(4) Placebo control.
\end{methodology}
```

* *最佳实践：**
- 总结关键方法学特征
- 在方法部分的开头使用
- 包括样本大小和设计类型
- 保持技术性但易于理解

### 结果Box

用于突出显示特定统计结果：

```latex
\begin{resultsbox}[Primary Outcome Analysis]
Mixed-effects regression revealed a significant treatment × time
interaction, \effectsize{F(3, 446)}{8.72}, \psig{< 0.001},
$\eta^2_p$ = 0.055, indicating differential improvement across
treatment conditions over the study period.
\end{resultsbox}
```

* *最佳实践：**
- 报告完整的统计信息
- 使用科学记数法命令
- 包括效果大小和 p 值
- 每个主要一个框分析

### 建议框

用于建议和影响：

```latex
\begin{recommendations}[Clinical Practice Guidelines]
Based on our findings, we recommend:
\begin{enumerate}
    \item \textbf{Primary recommendation:} Implement screening protocol
        for high-risk populations.
    \item \textbf{Secondary recommendation:} Adjust treatment intensity
        based on baseline severity scores.
    \item \textbf{Monitoring:} Reassess at 3-month intervals.
\end{enumerate}
\end{recommendations}
```

* *最佳实践：**
- 提出具体且可操作的建议
- 使用清晰的标签确定优先级
- 链接到支持证据
- 包括实施指南

### 限制框

用于限制、警告和警告：

```latex
\begin{limitations}[Study Limitations]
Several limitations should be considered:
\begin{itemize}
    \item \textbf{Sample:} Participants were recruited from academic
        medical centers, limiting generalizability to community settings.
    \item \textbf{Design:} The observational design precludes causal
        inference about treatment effects.
    \item \textbf{Attrition:} 15% dropout rate may introduce bias.
\end{itemize}
\end{limitations}
```

* *最佳实践：**
- 诚实和彻底
- 解释每个的含义限制
- 建议未来的研究如何解决限制
- 不要过度限定结果

### 重要通知框

用于重要警告或安全信息：

```latex
\begin{criticalnotice}[Safety Warning]
\textbf{Contraindication:} This intervention is contraindicated for
patients with [condition]. Monitor for [adverse effects] and discontinue
immediately if [symptoms] occur. Report serious adverse events to [contact].
\end{criticalnotice}
```

* *最佳实践：**
- 真正保留关键信息
- 清晰直接
- 包括要采取的具体行动
- 提供相关的联系信息

### 定义框

用于定义和解释性注释：

```latex
\begin{definition}[Effect Size]
An \textbf{effect size} is a quantitative measure of the magnitude of a
phenomenon. Unlike significance tests, effect sizes are independent of
sample size and allow comparison across studies. Common measures include
Cohen's \textit{d} for mean differences and Pearson's \textit{r} for
correlations.
\end{definition}
```

* *最佳实践：**
- 首次使用时定义技术术语
- 保持定义简洁
- 包含实用解释指导
- 使用适合受众的术语

- --

## 专业表格格式

### 设计原则

1. **外观整洁**：使用`booktabs`规则（`\toprule`、`\midrule`、`\bottomrule`）
2. **交替行**：将 `\rowcolor{tablealt}` 应用于每隔一行 
3. **清晰的标题**：用于列标识的粗体标题
4. **适当的精度**：将统计数据报告到适当的小数位
5. **完整信息**：包括样本量、单位和注释

### 标准数据表

```latex
\begin{table}[htbp]
\centering
\caption{Demographic Characteristics by Treatment Group}
\label{tab:demographics}
\begin{tabular}{@{}lcc@{}}
\toprule
\textbf{Characteristic} & \textbf{Treatment} & \textbf{Control} \\
 & (\samplesize{225}) & (\samplesize{225}) \\
\midrule
Age, years, \meansd{M}{SD} & \meansd{42.3}{12.5} & \meansd{43.1}{11.8} \\
\rowcolor{tablealt} Female, n (\%) & 128 (56.9) & 121 (53.8) \\
Education, years, \meansd{M}{SD} & \meansd{14.2}{2.8} & \meansd{14.5}{2.6} \\
\rowcolor{tablealt} Baseline score, \meansd{M}{SD} & \meansd{52.4}{15.3} & \meansd{51.8}{14.9} \\
\bottomrule
\end{tabular}
\figurenote{No significant differences between groups at baseline (all \textit{p} > .10).}
\end{table}
```

### 带显着性指标的结果表

```latex
\begin{table}[htbp]
\centering
\caption{Treatment Effects on Primary and Secondary Outcomes}
\label{tab:results}
\begin{tabular}{@{}lcccc@{}}
\toprule
\textbf{Outcome} & \textbf{Treatment} & \textbf{Control} & \textbf{Effect} & \textbf{p} \\
 & \meansd{M}{SD} & \meansd{M}{SD} & \textbf{(d)} & \\
\midrule
Primary outcome & \meansd{68.4}{14.2} & \meansd{54.1}{15.8} & 0.95\sigthree & <.001 \\
\rowcolor{tablealt} Secondary A & \meansd{4.2}{1.1} & \meansd{3.5}{1.2} & 0.61\sigtwo & .003 \\
Secondary B & \meansd{22.8}{5.4} & \meansd{21.2}{5.1} & 0.31\sigone & .042 \\
\rowcolor{tablealt} Secondary C & \meansd{8.9}{2.3} & \meansd{8.5}{2.4} & 0.17\signs & .285 \\
\bottomrule
\end{tabular}

\vspace{0.5em}
{\small \siglegend}
\end{table}
```

### 质量对照表评级

```latex
\begin{table}[htbp]
\centering
\caption{Evidence Summary by Study}
\label{tab:evidence}
\begin{tabular}{@{}llccc@{}}
\toprule
\textbf{Study} & \textbf{Design} & \textbf{N} & \textbf{Quality} & \textbf{Evidence} \\
\midrule
Smith et al. (2024) & RCT & 450 & \qualityhigh & \evidencestrong \\
\rowcolor{tablealt} Jones et al. (2023) & Cohort & 1,250 & \qualitymedium & \evidencemoderate \\
Chen et al. (2023) & Case-control & 320 & \qualitymedium & \evidencemoderate \\
\rowcolor{tablealt} Lee et al. (2022) & Cross-sectional & 890 & \qualitylow & \evidenceweak \\
\bottomrule
\end{tabular}
\end{table}
```

- --

## 图形和标题样式

### 标题格式

样式包自动格式化标题：
- 蓝色、粗体图形标签
- 灰色描述性text
- 带边距居中对齐

### 标准图

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{../figures/results_comparison.png}
\caption{Comparison of Outcome Scores by Treatment Condition and Time Point}
\label{fig:results}
\end{figure}
```

### 带来源属性的图

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.85\textwidth]{../figures/trend_analysis.png}
\caption{Trends in Key Metrics Over the Study Period}
\figuresource{Study data collected January--December 2024}
\label{fig:trends}
\end{figure}
```

### 带说明的图注意

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.8\textwidth]{../figures/conceptual_model.png}
\caption{Conceptual Model of Hypothesized Relationships}
\figurenote{Solid arrows indicate primary pathways; dashed arrows indicate moderated relationships. Numbers represent standardized coefficients.}
\label{fig:model}
\end{figure}
```

- --

## 调色板和视觉层次

### 颜色使用指南

|颜色 |用于 |避免使用 |
|--------|---------|-----------------|
|原色蓝|标题，重要发现|警告、注意|
|科学绿色|方法，积极的结果|阴性结果|
|橙色|注意事项、限制 |积极的发现|
|红色|严重警告|日常内容|
|紫色|推荐 |结果、方法|
|灰色|定义、注释 |主要发现 |

### 视觉层次结构

1. **执行摘要框**（阴影效果） - 最突出的
2. **彩色内容框** - 关键内容
3 高度突出。 **带有颜色的表格** - 数据
4 中等突出。 **正文** - 标准突出部分
5. **定义框** - 补充信息的显着性较低

### 可访问性注意事项

- 调色板的设计旨在区分常见的色觉缺陷
- 所有盒子都有颜色和结构指示符（边框、背景）
- 文本保持足够的对比度
- 不要仅依靠颜色来传达含义

- --

## 版式指南

### 字体规格

|元素|字体|尺寸|颜色 |
|---------|------|-----|--------|
|正文 |黑体 | 11点|深灰色 (#424242) |
|章节标题 | Helvetica 粗体 |巨大|原蓝色 (#003366) |
|章节标题 | Helvetica 粗体 |大|原蓝色 (#003366) |
|小节| Helvetica 粗体 |大|二次蓝 (#4A90E2) |
|小小节| Helvetica 粗体 |正常尺寸 |深灰色 (#424242) |

### 间距

- 行间距：1.15（为了可读性）
- 段落间距：段落之间 0.5em
- 页边距：所有边 1 英寸

### 最佳版式做法

1. **一致性**：对相似元素使用相同的格式
2. **层次结构**：使用视觉权重来表示重要性
3. **可读性**：足够的间距和对比度
4. **专业**：避免混合字体或过多格式

- --

## 科学计数法命令参考

### 统计报告

|命令 |输出|何时使用 |
|---------|--------|-------------|
| `\pvalue{0.023}` | *p* = 0.023 |报告 p 值 |
| `\psig{< 0.001}` | ***p*** = < 0.001 |显着 p 值（粗体）|
| `\CI{0.45}{0.72}` | 95% CI [0.45, 0.72] |置信区间|
| `\effectsize{d}{0.75}` | d = 0.75 |效果大小|
| `\samplesize{250}` | *n* = 250 |样本大小|
| `\meansd{42.5}{8.3}` | 42.5±8.3|平均值与 SD |

### 显着性指标

|命令 |输出|含义 |
|---------|--------|---------|
| `\sigone` | * | p < 0.05 |
| `\sigtwo` | ** | p < 0.01 |
| `\sigthree` | *** | p < 0.001 |
| `\signs` | ns |不显着|
| `\siglegend` |完整传奇 |表脚注 |

### 质量和证据评级

|命令 |输出|含义 |
|---------|--------|---------|
| `\qualityhigh` | **高**（绿色）|高品质|
| `\qualitymedium` | **中**（橙色）|质量中等|
| `\qualitylow` | **低**（红色）|低质量|
| `\evidencestrong` | **强**（绿色）|有力证据|
| `\evidencemoderate` | **中等**（橙色）|中等证据|
| `\evidenceweak` | **弱**（红色） |证据不足 |

### 趋势指标

|命令 |符号|含义 |
|---------|--------|---------|
| `\trendup` | ▲（绿色）|上升趋势|
| `\trenddown` | ▼（红色）|下降趋势|
| `\trendflat` | →（灰色）|稳定/无变化 |

- --

## 完整的 LaTeX 示例

### 执行摘要示例

```latex
\chapter*{Executive Summary}
\addcontentsline{toc}{chapter}{Executive Summary}

\begin{executivesummary}[Report Highlights]
This report presents findings from a comprehensive study of [topic]
involving \samplesize{450} participants across 12 research sites.
The research addressed [key question] using [methodology].
\end{executivesummary}

\subsection*{Key Findings}

\begin{keyfindings}
\begin{enumerate}
    \item The primary intervention demonstrated a large effect
          (\effectsize{d}{0.82}, \psig{< 0.001}).
    \item Benefits were maintained at 12-month follow-up.
    \item Cost-effectiveness analysis supports implementation.
\end{enumerate}
\end{keyfindings}

\subsection*{Recommendations}

\begin{recommendations}
Based on these findings, we recommend:
\begin{enumerate}
    \item Implement the intervention in [settings].
    \item Train practitioners using the standardized protocol.
    \item Monitor outcomes using the validated measures.
\end{enumerate}
\end{recommendations}
```

### 方法部分示例

```latex
\chapter{Methods}

\begin{methodology}[Study Overview]
This randomized controlled trial employed a parallel-group design with
1:1 allocation to intervention or control conditions. The study was
conducted across 12 sites between January 2023 and December 2024.
\end{methodology}

\section{Participants}

A total of \samplesize{450} participants were enrolled. Eligibility
criteria were:

\begin{itemize}
    \item Age 18--65 years
    \item Diagnosis of [condition] per [criteria]
    \item No contraindications to [intervention]
\end{itemize}

Table~\ref{tab:participants} presents participant characteristics.

\begin{limitations}[Recruitment Challenges]
Recruitment was slower than anticipated due to [reasons]. The final
sample was 10% below target, which may affect statistical power for
secondary analyses.
\end{limitations}
```

### 结果部分示例

```latex
\chapter{Results}

\section{Primary Outcome}

\begin{resultsbox}[Primary Analysis]
Mixed-effects regression revealed a significant treatment effect,
\effectsize{F(1, 448)}{42.18}, \psig{< 0.001}, with a large effect
size (\effectsize{d}{0.82}). The treatment group showed significantly
greater improvement (\meansd{16.4}{5.2} points) compared to control
(\meansd{8.1}{4.8} points).
\end{resultsbox}

Figure~\ref{fig:primary} illustrates the treatment effects over time.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{../figures/primary_outcome.png}
\caption{Primary Outcome Scores by Treatment Group and Time Point}
\figurenote{Error bars represent 95\% confidence intervals.}
\label{fig:primary}
\end{figure}

\section{Secondary Outcomes}

Results for secondary outcomes are presented in Table~\ref{tab:secondary}.
```

### 讨论部分示例

```latex
\chapter{Discussion}

\section{Summary of Findings}

\begin{keyfindings}[Main Conclusions]
\begin{enumerate}
    \item The intervention was highly effective (primary hypothesis
          \highlight{supported})
    \item Effects were clinically meaningful and durable
    \item Evidence strength: \evidencestrong
\end{enumerate}
\end{keyfindings}

\section{Limitations}

\begin{limitations}
Several limitations warrant consideration:
\begin{itemize}
    \item The sample was predominantly [demographic], limiting
          generalizability.
    \item Attrition was higher in the control group (18\% vs. 12\%).
    \item Self-report measures may be subject to response bias.
\end{itemize}
\end{limitations}

\section{Implications}

\begin{recommendations}[Research Implications]
\begin{enumerate}
    \item Replicate in diverse populations
    \item Investigate mechanisms of change
    \item Test implementation strategies
\end{enumerate}
\end{recommendations}

\begin{recommendations}[Practice Implications]
\begin{enumerate}
    \item Adopt the intervention in [settings]
    \item Train providers using standardized protocols
    \item Monitor fidelity and outcomes
\end{enumerate}
\end{recommendations}
```

- --

## 清单：专业报告质量

在最终确定报告之前，请验证：

### 格式
- [ ]使用`scientific_report.sty`包
- [ ]使用XeLaTeX或LuaLaTeX
- [ ] Helvetica字体正确渲染
- [ ]颜色正确显示

### 内容组织
- [ ]执行摘要已呈现并完整
- [ ]方框中突出显示的主要发现
- [ ]明确描述的方法
- [ ]结果采用统计数据正确格式化
- [ ]承认的局限性
- [ ]建议具体且可操作

### 表格
- [ ]所有表格都有标题和标签
- [ ]应用交替行颜色
- [ ]显着性指标解释
- [ ]数字格式一致

### 图
- [ ]所有图都有标题和标签
- [ ]适当来源 
- [ ]分辨率足以打印 (300 DPI)
- [ ]文本中引用

### 统计报告
- [ ]适当报告的 P 值
- [ ]包括效应大小
- [ ]置信区间，其中相关
- [ ]规定样本大小

### 专业外观
- [ ]始终保持一致的格式
- [ ]无孤立标题或寡头
- [ ]在适当位置分页符
- [ ]参考文献完整且formatted

- --

## 资源

### 本技能中的文件

- `assets/scientific_report.sty` - LaTeX 样式包
- `assets/scientific_report_template.tex` - 完整报告模板
- `assets/REPORT_FORMATTING_GUIDE.md` - 快速参考指南

### 相关技能

- `venue-templates` - 用于期刊手稿和会议论文
- `scientific-schematics` - 用于生成图表和图形
- `generate-image` - 用于创建插图和图形

### 外部资源

- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX) - 一般 LaTeX 参考
- [Booktabs 包文档](https://ctan.org/pkg/booktabs) - 专业表格样式
- [tcolorbox 包文档](https://ctan.org/pkg/tcolorbox) - 彩色框环境
