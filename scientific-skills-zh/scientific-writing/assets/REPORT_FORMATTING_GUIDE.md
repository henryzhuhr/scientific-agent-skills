# 科学报告格式指南

使用`scientific_report.sty`样式包的快速参考。

## 概述

`scientific_report.sty`包为科学报告、技术文档和白皮书提供专业的格式设置。它具有：

- **Helvetica 字体系列**，打造干净、现代的外观
- **专业配色方案**，具有蓝色、绿色和强调色
- **彩色框环境**，用于组织不同类型的内容
- **有吸引力的表格**，具有交替的行颜色和专业标题
- **科学记数法命令** p 值、效果大小和统计数据
- **专业页眉和页脚**，带有自动部分标题

- --

## 调色板

### 原色（蓝色）

|颜色名称 | RGB |十六进制 |用法 |
|------------|-----|-----|--------|
| `primaryblue` | (0, 51, 102) | `#003366` |标头、标题、主要元素 |
| `secondaryblue` | (74, 144, 226) | `#4A90E2` |小节、二级标题 |
| `lightblue` | (220, 235, 252) | `#DCEBFC` |主要调查结果框背景|
| `accentblue` | (0, 120, 215) | `#0078D7` |重点突出、假设框 |

### 科学颜色（绿色）

|颜色名称 | RGB |十六进制 |用法 |
|------------|-----|-----|--------|
| `sciencegreen` | (0, 168, 150) | `#00A896` |方法框，积极的发现|
| `lightgreen` | (220, 245, 240) | `#DCF5F0` |方法论框背景|
| `darkgreen` | (0, 128, 96) | `#008060` |结果框，强有力的证据 |

### 警告颜色（橙色/红色）

|颜色名称 | RGB |十六进制 |用法 |
|------------|-----|-----|--------|
| `cautionorange` | (255, 140, 66) | `#FF8C42` |限制、警告、注意事项|
| `lightorange` | (255, 243, 224) | `#FFF3E0` |限制框背景|
| `criticalred` | (198, 40, 40) | `#C62828` |重要通知、警报|
| `lightred` | (255, 235, 238) | `#FFEBEE` |重要通知背景 |

### 推荐颜色

|颜色名称 | RGB |十六进制 |用法 |
|------------|-----|-----|--------|
| `recommendpurple` | (103, 58, 183) | `#673AB7` |推荐框|
| `lightpurple` | (237, 231, 246) | `#EDE7F6` |推荐框背景|

### 中性色

|颜色名称 | RGB |十六进制 |用法 |
|------------|-----|-----|--------|
| `darkgray` | (66, 66, 66) | `#424242` |正文|
| `mediumgray` | (117, 117, 117) | `#757575` |辅助文本，定义|
| `lightgray` | (245, 245, 245) | `#F5F5F5` |背景、定义框|
| `tablealt` | (248, 250, 252) | `#F8FAFC` |交替表行|

- --

## 框环境

### 关键发现框（蓝色）

用于主要发现、发现和重要结果。

```latex
\begin{keyfindings}[Custom Title]
This study found that treatment A significantly outperformed
treatment B (\pvalue{0.001}, \effectsize{d}{0.75}).
\end{keyfindings}
```

### 方法框（绿色）

用于方法、程序和研究设计亮点。

```latex
\begin{methodology}[Study Design]
This randomized controlled trial employed a 2×2 factorial design
with pre-post measurements and 6-month follow-up.
\end{methodology}
```

### 结果框（蓝-绿）

用于突出显示具体结果和统计结果。

```latex
\begin{resultsbox}[Primary Outcome]
Analysis revealed a significant main effect, F(2, 147) = 12.45,
\psig{< 0.001}, $\eta^2$ = 0.145.
\end{resultsbox}
```

### 建议框（紫色）

用于建议、影响和行动项目。

```latex
\begin{recommendations}[Clinical Implications]
\begin{enumerate}
    \item Implement screening protocol for high-risk patients
    \item Adjust treatment dosage based on biomarker levels
    \item Monitor patients at 3-month intervals
\end{enumerate}
\end{recommendations}
```

### 限制框（橙色）

用于限制、警告和警告。

```latex
\begin{limitations}[Study Limitations]
\begin{itemize}
    \item Sample limited to urban populations
    \item Cross-sectional design precludes causal inference
    \item Self-report measures may introduce bias
\end{itemize}
\end{limitations}
```

### 重要通知框（红色）

用于严重警告、重要通知或安全信息。

```latex
\begin{criticalnotice}[Safety Warning]
Patients with contraindication X should not receive this treatment.
Consult specialist before proceeding.
\end{criticalnotice}
```

### 定义框（灰色）

用于定义、注释和补充信息。

```latex
\begin{definition}[Key Term]
\textbf{Effect size} refers to a quantitative measure of the
magnitude of a phenomenon, independent of sample size.
\end{definition}
```

### 执行摘要框（特殊）

用于增强样式和阴影效果的执行摘要。

```latex
\begin{executivesummary}[Report Overview]
This report presents findings from a comprehensive analysis
of [topic]. Key findings indicate that...
\end{executivesummary}
```

### 假设框（浅蓝色）

用于陈述研究假设。

```latex
\begin{hypothesis}[Primary Hypothesis]
We hypothesize that intervention X will significantly improve
outcome Y compared to control conditions.
\end{hypothesis}
```

- --

## 重要报价

用于突出显示重要的报价或陈述。

```latex
\begin{pullquote}
"These findings represent a paradigm shift in our understanding
of the underlying mechanisms."
\end{pullquote}
```

- --

## 统计框

用于突出显示关键统计数据（在行中使用共 3).

```latex
\begin{center}
\statbox{n = 500}{Participants}
\statbox{p < 0.001}{Significance}
\statbox{d = 0.75}{Effect Size}
\end{center}
```

- --

## 科学记数法命令

### P 值

```latex
\pvalue{0.023}          % Outputs: p = 0.023
\psig{< 0.001}          % Outputs: p = < 0.001 (bold for significant)
```

### 置信度间隔

```latex
\CI{0.45}{0.72}         % Outputs: 95% CI [0.45, 0.72]
```

### 效果大小

```latex
\effectsize{d}{0.75}    % Outputs: d = 0.75
\effectsize{r}{0.42}    % Outputs: r = 0.42
\effectsize{F(2, 97)}{12.45}  % Outputs: F(2, 97) = 12.45
```

### 样本大小

```latex
\samplesize{250}        % Outputs: n = 250
```

### 标准平均值偏差

```latex
\meansd{42.5}{8.3}      % Outputs: 42.5 ± 8.3
```

### 显着性指标（对于表格）

```latex
Result\sigone           % * for p < 0.05
Result\sigtwo           % ** for p < 0.01
Result\sigthree         % *** for p < 0.001
Result\signs            % ns for not significant

% Legend for table footnotes:
\siglegend              % Outputs: *p < 0.05; **p < 0.01; ***p < 0.001; ns not significant
```

### 质量/证据指标

```latex
\qualityhigh            % HIGH (green)
\qualitymedium          % MEDIUM (orange)
\qualitylow             % LOW (red)

\evidencestrong         % Strong (green)
\evidencemoderate       % Moderate (orange)
\evidenceweak           % Weak (red)
```

### 趋势指标

```latex
\trendup                % Green up triangle ▲
\trenddown              % Red down triangle ▼
\trendflat              % Gray right arrow →
```

### 文本突出显示

```latex
\highlight{important text}  % Blue bold text
```

- --

## 表格格式

### 带交替的标准表格行

```latex
\begin{table}[htbp]
\centering
\caption{Descriptive Statistics by Group}
\label{tab:descriptives}
\begin{tabular}{@{}lccc@{}}
\toprule
\textbf{Variable} & \textbf{Group A} & \textbf{Group B} & \textbf{p} \\
\midrule
Age (years) & \meansd{42.5}{8.3} & \meansd{43.1}{7.9} & .58 \\
\rowcolor{tablealt} Score 1 & \meansd{15.2}{3.4} & \meansd{18.7}{4.1} & <.001\sigthree \\
Score 2 & \meansd{22.8}{5.1} & \meansd{23.4}{4.8} & .42 \\
\rowcolor{tablealt} Score 3 & \meansd{8.9}{2.2} & \meansd{7.2}{2.5} & .003\sigtwo \\
\bottomrule
\end{tabular}

\vspace{0.5em}
{\small \siglegend}
\end{table}
```

### 包含质量指标的表格

```latex
\begin{tabular}{@{}llcc@{}}
\toprule
\textbf{Study} & \textbf{Design} & \textbf{Quality} & \textbf{Evidence} \\
\midrule
Smith et al. (2023) & RCT & \qualityhigh & \evidencestrong \\
\rowcolor{tablealt} Jones et al. (2022) & Cohort & \qualitymedium & \evidencemoderate \\
Lee et al. (2021) & Cross-sectional & \qualitylow & \evidenceweak \\
\bottomrule
\end{tabular}
```

### 包含趋势指标的表格

```latex
\begin{tabular}{@{}lrrl@{}}
\toprule
\textbf{Metric} & \textbf{Baseline} & \textbf{Follow-up} & \textbf{Change} \\
\midrule
Score A & 42.5 & 58.3 & \trendup +37\% \\
\rowcolor{tablealt} Score B & 18.2 & 15.1 & \trenddown -17\% \\
Score C & 7.8 & 7.9 & \trendflat +1\% \\
\bottomrule
\end{tabular}
```

- --

## 图格式

### 标准图

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{../figures/results_chart.png}
\caption{Comparison of Outcome Scores Across Treatment Conditions}
\label{fig:results}
\end{figure}
```

### 带有来源属性的图

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.85\textwidth]{../figures/data_visualization.png}
\caption{Distribution of Participant Responses by Category}
\figuresource{Study data, collected January-March 2024}
\label{fig:distribution}
\end{figure}
```

### 带有来源的图注

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.8\textwidth]{../figures/model_diagram.png}
\caption{Conceptual Model of Proposed Relationships}
\figurenote{Solid arrows indicate direct effects; dashed arrows indicate moderated effects.}
\label{fig:model}
\end{figure}
```

- --

## 标题页

### 标准标题页

```latex
\makereporttitle
    {Research Report Title}              % Title
    {A Comprehensive Analysis}           % Subtitle
    {Author Name, PhD}                   % Author(s)
    {Research Institution}               % Institution
    {January 2025}                        % Date
```

### 带封面的标题页图片

```latex
\makereporttitlewithimage
    {Research Report Title}              % Title
    {A Comprehensive Analysis}           % Subtitle
    {../figures/cover_image.png}         % Image path
    {Author Name, PhD}                   % Author(s)
    {Research Institution}               % Institution
    {January 2025}                        % Date
```

- --

## 列表格式

列表自动使用蓝色项目符号/数字。

### 项目符号列表

```latex
\begin{itemize}
    \item First item with automatic blue bullet
    \item Second item
    \item Third item
\end{itemize}
```

### 编号列表

```latex
\begin{enumerate}
    \item First item with blue number
    \item Second item
    \item Third item
\end{enumerate}
```

- --

## 附录部分

```latex
\appendix

\chapter{Supplementary Materials}

\appendixsection{Additional Tables}
% Content appears in table of contents

\appendixsection{Instruments}
% Additional appendix content
```

- --

## 编译

使用XeLaTeX或LuaLaTeX编译以获得最佳字体渲染：

```bash
# Using XeLaTeX
xelatex report.tex
bibtex report        # If using BibTeX
xelatex report.tex
xelatex report.tex

# Using latexmk (recommended)
latexmk -xelatex report.tex

# Using LuaLaTeX
lualatex report.tex
```

- --

## 常见模式

### 结果部分示例

```latex
\section{Primary Outcomes}

\begin{resultsbox}[Main Finding]
The intervention group showed significantly higher scores than
the control group, \effectsize{t(98)}{3.45}, \psig{< 0.001},
\effectsize{d}{0.69}, \CI{0.42}{0.96}.
\end{resultsbox}

Table~\ref{tab:outcomes} presents the complete results for all
outcome measures.

\begin{table}[htbp]
\centering
\caption{Outcome Measures by Treatment Condition}
\label{tab:outcomes}
\begin{tabular}{@{}lcccc@{}}
\toprule
\textbf{Measure} & \textbf{Control} & \textbf{Treatment} & \textbf{d} & \textbf{p} \\
\midrule
Primary & \meansd{42.1}{8.2} & \meansd{51.3}{9.1} & 0.69\sigthree & <.001 \\
\rowcolor{tablealt} Secondary & \meansd{3.2}{1.1} & \meansd{4.1}{1.3} & 0.52\sigtwo & .004 \\
Tertiary & \meansd{18.5}{4.2} & \meansd{19.2}{4.5} & 0.16\signs & .328 \\
\bottomrule
\end{tabular}
\end{table}
```

### 讨论部分示例

```latex
\section{Interpretation of Findings}

\begin{keyfindings}[Summary]
\begin{enumerate}
    \item Primary hypothesis \highlight{supported} with large effect
    \item Secondary hypothesis partially supported
    \item Evidence quality: \evidencestrong
\end{enumerate}
\end{keyfindings}

\begin{limitations}
This study has several limitations that should be considered...
\end{limitations}

\begin{recommendations}[Future Research]
Future studies should address the following:
\begin{enumerate}
    \item Replicate findings in diverse populations
    \item Extend follow-up period to assess long-term effects
    \item Investigate moderating variables
\end{enumerate}
\end{recommendations}
```

- --

## 故障排除

### 盒子溢出
如果盒子内容溢出页面：
```latex
\newpage
\begin{keyfindings}[Continued...]
```

### 图形放置
使用`[htbp]`进行灵活放置，或使用`[H]`（需要`float`封装）进行放置精确：
```latex
\usepackage{float}
\begin{figure}[H]
```

### 表格太宽
使用`\resizebox`或减小字体大小：
```latex
\resizebox{\textwidth}{!}{
\begin{tabular}{...}
...
\end{tabular}
}
```

### 字体问题
如果Helvetica未渲染，请确保您使用的是XeLaTeX或LuaLaTeX:
```bash
xelatex report.tex   # NOT pdflatex
```

- --

## 快速参考卡

|目的|命令/环境 |
|---------|------------------------|
|主要发现| `\begin{keyfindings}...\end{keyfindings}` |
|方法 | `\begin{methodology}...\end{methodology}` |
|结果 | `\begin{resultsbox}...\end{resultsbox}` |
|推荐| `\begin{recommendations}...\end{recommendations}` |
|限制| `\begin{limitations}...\end{limitations}` |
|警告| `\begin{criticalnotice}...\end{criticalnotice}` |
|定义 | `\begin{definition}...\end{definition}` |
|执行摘要| `\begin{executivesummary}...\end{executivesummary}` |
|假设| `\begin{hypothesis}...\end{hypothesis}` |
| P 值 | `\pvalue{0.05}` 或 `\psig{< 0.001}` |
|效应大小| `\effectsize{d}{0.75}` |
|样本量| `\samplesize{250}` |
|平均值±标准差| `\meansd{42.5}{8.3}` |
| CI | `\CI{0.38}{0.72}` |
|亮点| `\highlight{text}` |
|替代行| `\rowcolor{tablealt}` |
|意义 | `\sigone`、`\sigtwo`、`\sigthree`、`\signs` |
