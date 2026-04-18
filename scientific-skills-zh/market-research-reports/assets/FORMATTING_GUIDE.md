# 市场研究报告格式指南

使用`market_research.sty`样式包的快速参考。

## 调色板

### 原色
|颜色名称 | RGB |十六进制 |用法 |
|------------|-----|-----|--------|
| `primaryblue` | (0, 51, 102) | `#003366` |标头、标题、链接 |
| `secondaryblue` | (51, 102, 153) | `#336699` |小节，次要元素|
| `lightblue` | (173、216、230) | `#ADD8E6` |关键洞察框背景|
| `accentblue` | (0, 120, 215) | `#0078D7` |重点突出，机会框 |

### 次要颜色
|颜色名称 | RGB |十六进制 |用法 |
|------------|-----|-----|--------|
| `accentgreen` | (0, 128, 96) | `#008060` |市场数据框，积极指标|
| `lightgreen` | (200, 230, 201) | `#C8E6C9` |行情数据框背景|
| `warningorange` | (255, 140, 0) | `#FF8C00` |风险框、警告|
| `alertred` | (198, 40, 40) | `#C62828` |重大风险|
| `recommendpurple` | (103, 58, 183) | `#673AB7` |推荐盒子|

### 中性色
|颜色名称 | RGB |十六进制 |用法 |
|------------|-----|-----|--------|
| `darkgray` | (66, 66, 66) | `#424242` |正文|
| `mediumgray` | (117, 117, 117) | `#757575` |辅助文字|
| `lightgray` | (240, 240, 240) | `#F0F0F0` |背景、标注框|
| `tablealt` | (245, 247, 250) | `#F5F7FA` |交替表行 |

- --

## 框环境

### 关键洞察框（蓝色）
用于主要发现、见解和重要发现。

```latex
\begin{keyinsightbox}[Custom Title]
The market is projected to grow at 15.3% CAGR through 2030, driven by
increasing enterprise adoption and favorable regulatory conditions.
\end{keyinsightbox}
```

### 市场数据框（绿色）
用于市场统计、指标、 

```latex
\begin{marketdatabox}[Market Snapshot]
\begin{itemize}
    \item \textbf{Market Size (2024):} \marketsize{45.2 billion}
    \item \textbf{Projected Size (2030):} \marketsize{98.7 billion}
    \item \textbf{CAGR:} \growthrate{15.3}
\end{itemize}
\end{marketdatabox}
```

### 风险框（橙色/警告）
用于风险因素、警告和注意事项。

```latex
\begin{riskbox}[Market Risk]
Regulatory changes in the European Union could impact 40% of market
participants within the next 18 months.
\end{riskbox}
```

### 严重风险框（红色）
用于高严重性或严重性风险.

```latex
\begin{criticalriskbox}[Critical: Supply Chain Disruption]
A major supply chain disruption could result in 6-12 month delays
and 30% cost increases.
\end{criticalriskbox}
```

### 推荐框（紫色）
用于战略建议和行动项目。

```latex
\begin{recommendationbox}[Strategic Recommendation]
\begin{enumerate}
    \item Prioritize market entry in Asia-Pacific region
    \item Develop strategic partnerships with local distributors
    \item Invest in localization of product offerings
\end{enumerate}
\end{recommendationbox}
```

### 标注框（灰色）
用于定义、注释和补充信息。

```latex
\begin{calloutbox}[Definition: TAM]
Total Addressable Market (TAM) represents the total revenue opportunity
available if 100% market share was achieved.
\end{calloutbox}
```

### 执行摘要框
执行摘要突出显示的特殊样式。

```latex
\begin{executivesummarybox}[Executive Summary]
Key findings and highlights of the report...
\end{executivesummarybox}
```

### 机会框（青色/口音蓝色）
代表机会和积极结果。

```latex
\begin{opportunitybox}[Growth Opportunity]
The Asia-Pacific market represents a \$15 billion opportunity
growing at 22% CAGR.
\end{opportunitybox}
```

### 框架框
用于战略分析框架。

```latex
% SWOT Analysis
\begin{swotbox}[SWOT Analysis Summary]
Content...
\end{swotbox}

% Porter's Five Forces
\begin{porterbox}[Porter's Five Forces Analysis]
Content...
\end{porterbox}
```

- --

## 重要报价

用于突出显示重要统计数据或报价。

```latex
\begin{pullquote}
"The convergence of AI and healthcare represents a \$199 billion
opportunity by 2034."
\end{pullquote}
```

- --

## 统计框

用于突出显示关键统计数据（按 3 行使用）。

```latex
\begin{center}
\statbox{\$45.2B}{Market Size 2024}
\statbox{15.3\%}{CAGR 2024-2030}
\statbox{23\%}{Market Leader Share}
\end{center}
```

- --

## 自定义命令

### 突出显示文本
```latex
\highlight{Important text}  % Blue bold
```

### 市场规模格式
```latex
\marketsize{45.2 billion}   % Outputs: $45.2 billion in green
```

### 增长率格式
```latex
\growthrate{15.3}           % Outputs: 15.3% in green
```

### 风险指标
```latex
\riskhigh{}     % Outputs: HIGH in red
\riskmedium{}   % Outputs: MEDIUM in orange
\risklow{}      % Outputs: LOW in green
```

### 评级星级 (1-5)
```latex
\rating{4}      % Outputs: ★★★★☆
```

### 趋势指标
```latex
\trendup{}      % Green up triangle
\trenddown{}    % Red down triangle
\trendflat{}    % Gray right arrow
```

- --

## 表格式设置

### 具有交替行的标准表格
```latex
\begin{table}[htbp]
\centering
\caption{Market Size by Region}
\begin{tabular}{@{}lrrr@{}}
\toprule
\textbf{Region} & \textbf{Size} & \textbf{Share} & \textbf{CAGR} \\
\midrule
North America & \$18.2B & 40.3\% & 12.5\% \\
\rowcolor{tablealt} Europe & \$12.1B & 26.8\% & 14.2\% \\
Asia-Pacific & \$10.5B & 23.2\% & 18.7\% \\
\rowcolor{tablealt} Rest of World & \$4.4B & 9.7\% & 11.3\% \\
\midrule
\textbf{Total} & \textbf{\$45.2B} & \textbf{100\%} & \textbf{15.3\%} \\
\bottomrule
\end{tabular}
\label{tab:regional}
\end{table}
```

### 带有趋势指标的表格
```latex
\begin{tabular}{@{}lrrl@{}}
\toprule
\textbf{Company} & \textbf{Revenue} & \textbf{Share} & \textbf{Trend} \\
\midrule
Company A & \$5.2B & 15.3\% & \trendup{} +12\% \\
Company B & \$4.8B & 14.1\% & \trenddown{} -3\% \\
Company C & \$4.2B & 12.4\% & \trendflat{} +1\% \\
\bottomrule
\end{tabular}
```

- --

## 图形格式设置

### 标准图
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{../figures/market_growth.png}
\caption{Market Growth Trajectory (2020-2030)}
\label{fig:growth}
\end{figure}
```

### 带来源属性的图
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.85\textwidth]{../figures/market_share.png}
\caption{Market Share Distribution (2024)}
\figuresource{Company annual reports, industry analysis}
\label{fig:market_share}
\end{figure}
```

- --

## 列表格式

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

### 嵌套列表
```latex
\begin{itemize}
    \item Main point
    \begin{itemize}
        \item Sub-point A
        \item Sub-point B
    \end{itemize}
    \item Another main point
\end{itemize}
```

- --

## 标题页

### 使用自定义标题命令
```latex
\makemarketreporttitle
    {Market Title}              % Report title
    {Subtitle Here}             % Subtitle
    {../figures/cover.png}      % Hero image (leave empty for no image)
    {January 2025}              % Date
    {Market Intelligence Team}  % Author/prepared by
```

### 手册标题页
完整手册标题页代码请参阅模板。

- --

## 附录章节

```latex
\appendix

\chapter{Methodology}

\appendixsection{Data Sources}
Content that appears in table of contents...
```

- --

## 常见模式

### 市场快照部分
```latex
\begin{marketdatabox}[Market Snapshot]
\begin{itemize}
    \item \textbf{Current Market Size:} \marketsize{45.2 billion}
    \item \textbf{Projected Size (2030):} \marketsize{98.7 billion}
    \item \textbf{CAGR:} \growthrate{15.3}
    \item \textbf{Largest Segment:} Enterprise (42\% share)
    \item \textbf{Fastest Growing Region:} APAC (\growthrate{22.1} CAGR)
\end{itemize}
\end{marketdatabox}
```

### 风险登记册摘要
```latex
\begin{table}[htbp]
\centering
\caption{Risk Assessment Summary}
\begin{tabular}{@{}llccl@{}}
\toprule
\textbf{Risk} & \textbf{Category} & \textbf{Prob.} & \textbf{Impact} & \textbf{Rating} \\
\midrule
Market disruption & Market & High & High & \riskhigh{} \\
\rowcolor{tablealt} Regulatory change & Regulatory & Med & High & \riskhigh{} \\
New entrant & Competitive & Med & Med & \riskmedium{} \\
\rowcolor{tablealt} Tech obsolescence & Technology & Low & High & \riskmedium{} \\
Currency fluctuation & Financial & Med & Low & \risklow{} \\
\bottomrule
\end{tabular}
\end{table}
```

#### 竞争比较表
```latex
\begin{table}[htbp]
\centering
\caption{Competitive Comparison}
\begin{tabular}{@{}lccccc@{}}
\toprule
\textbf{Factor} & \textbf{Co. A} & \textbf{Co. B} & \textbf{Co. C} & \textbf{Co. D} \\
\midrule
Market Share & \rating{5} & \rating{4} & \rating{3} & \rating{2} \\
\rowcolor{tablealt} Product Quality & \rating{4} & \rating{5} & \rating{3} & \rating{4} \\
Price Competitiveness & \rating{3} & \rating{3} & \rating{5} & \rating{4} \\
\rowcolor{tablealt} Innovation & \rating{5} & \rating{4} & \rating{2} & \rating{3} \\
Customer Service & \rating{4} & \rating{4} & \rating{4} & \rating{5} \\
\bottomrule
\end{tabular}
\end{table}
```

- --

## 故障排除

### 框溢出
如果框内容溢出页面，请分成多个框或使用分页符：
```latex
\newpage
\begin{keyinsightbox}[Continued...]
```

### 图形放置
使用`[htbp]`进行灵活放置，或使用`[H]`（需要`float`包）进行精确放置放置：
```latex
\begin{figure}[H]  % Requires \usepackage{float}
```

### 表太宽
使用`\resizebox`或`adjustbox`：
```latex
\resizebox{\textwidth}{!}{
\begin{tabular}{...}
...
\end{tabular}
}
```

### 颜色不出现
确保`xcolor`包装加载了`[table]`选项（已包含在样式文件中）。

- --

## 编译

使用XeLaTeX编译以获得最佳结果：
```bash
xelatex report.tex
bibtex report
xelatex report.tex
xelatex report.tex
```

或使用乳胶：
```bash
latexmk -xelatex report.tex
```
