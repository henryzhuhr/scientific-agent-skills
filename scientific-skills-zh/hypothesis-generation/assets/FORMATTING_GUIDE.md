# 假设生成报告 - 格式化快速参考

## 概述

本指南提供了使用假设生成LaTeX 模板和样式包的快速参考。完整文档请参见 `SKILL.md`.

## 快速入门

```latex
% !TEX program = xelatex
\documentclass[11pt,letterpaper]{article}
\usepackage{hypothesis_generation}
\usepackage{natbib}

\title{Your Phenomenon Name}
\begin{document}
\maketitle
% Your content
\end{document}
```

* *编译：** 使用 XeLaTeX 或 LuaLaTeX 获得最佳结果
```bash
xelatex your_document.tex
bibtex your_document
xelatex your_document.tex
xelatex your_document.tex
```

## 配色方案参考

### 假设颜色
- **假设 1**：深蓝色 (RGB: 0, 102, 153) - 用于第一个假设
- **假设 2**：森林绿 (RGB: 0, 128, 96) - 用于第二个假设
- **假设 3**：皇家紫色 (RGB: 102, 51, 153) - 用于第三个假设
- **假设 4**：青色（RGB：0, 128, 128） - 用于第四个假设（如果需要）
- **假设 5**：焦橙色（RGB：204, 85, 0） - 用于第五个假设（如果需要）

### 实用程序颜色
- **预测**：琥珀色 (RGB: 255, 191, 0) - 用于可测试的预测
- **证据**：浅蓝色 (RGB: 102, 178, 204) - 用于支持证据
- **比较**：钢灰色 (RGB: 108, 117, 125) - 用于关键比较
- **限制**：珊瑚红（RGB：220、53、69） - 用于限制/挑战

## 自定义框环境

### 1. 执行摘要框

```latex
\begin{summarybox}[Executive Summary]
  Content here
\end{summarybox}
```

* *用于：**文档开头的高级概述

- --

### 2. 假设框（5 个变体）

```latex
\begin{hypothesisbox1}[Hypothesis 1: Title]
  \textbf{Mechanistic Explanation:}
  [2-3 paragraphs explaining HOW and WHY]
  
  \textbf{Key Supporting Evidence:}
  \begin{itemize}
    \item Evidence point 1 \citep{ref1}
    \item Evidence point 2 \citep{ref2}
  \end{itemize}
  
  \textbf{Core Assumptions:}
  \begin{enumerate}
    \item Assumption 1
    \item Assumption 2
  \end{enumerate}
\end{hypothesisbox1}
```

* *可用框：** `hypothesisbox1`、`hypothesisbox2`、`hypothesisbox3`、`hypothesisbox4`、 `hypothesisbox5`

* *用于：** 呈现每个相互竞争的假设及其机制、证据和假设

* *4页正文的最佳实践：**
- 仅将机械解释保留在1-2个简短段落（最多6-10个句子）
- 包括2-3个最重要的证据点和引文
- 列出1-2个最关键的假设
- 确保每个假设真正不同
- 所有详细解释请访问附录 A
- **在每个假设框前使用 `\newpage` 以防止溢出**
- 每个完整的假设框应≤0.6 页

- --

### 3. 预测框

```latex
\begin{predictionbox}[Predictions: Hypothesis 1]
  \textbf{Prediction 1.1:} [Specific prediction]
  \begin{itemize}
    \item \textbf{Conditions:} When/where this applies
    \item \textbf{Expected Outcome:} Specific measurable result
    \item \textbf{Falsification:} What would disprove it
  \end{itemize}
\end{predictionbox}
```

* *用于：** 从每个假设导出的可测试预测假设

* *4页正文的最佳实践：**
- 尽可能进行具体和定量的预测
- 明确说明预测应成立的条件
- 始终指定证伪标准
- 正文中每个假设仅包含1-2个最关键的预测
- 其他预测请访问附录

- --

### 4.证据框

```latex
\begin{evidencebox}[Supporting Evidence]
  Content discussing supporting evidence
\end{evidencebox}
```

* *用于：**突出显示关键支持证据或文献综合

* *最佳实践：**
- 在正文中谨慎使用（详细证据见附录） A)
- 包括所有证据的引用
- 关注最令人信服的证据

- --

### 5. 比较框

```latex
\begin{comparisonbox}[H1 vs. H2: Key Distinction]
  \textbf{Fundamental Difference:}
  [Description of core difference]
  
  \textbf{Discriminating Experiment:}
  [Description of experiment]
  
  \textbf{Outcome Interpretation:}
  \begin{itemize}
    \item \textbf{If [Result A]:} H1 supported
    \item \textbf{If [Result B]:} H2 supported
  \end{itemize}
\end{comparisonbox}
```

* *用于：** 解释如何区分相互竞争的假设

* *最佳实践：**
- 关注基本机制差异
- 提出清晰、可行的判别实验
- 指定具体结果解释
- 对所有主要假设对进行比较

- --

### 6. 限制Box

```latex
\begin{limitationbox}[Limitations \& Challenges]
  Discussion of limitations
\end{limitationbox}
```

* *用于：**突出重要的限制或挑战

* *最佳实践：**
- 当限制特别重要时使用
- 诚实地面对挑战
- 建议如何限制可能地址

- --

## 文档结构

### 正文（最多4页 - 高度简洁）

1. **执行摘要**（0.5-1页）
  - 使用`summarybox`
  - 简要现象概述
  - 在每个句子中列出所有假设
  - 推荐方法

2. **竞争假设**（2-2.5页）
  - 使用`hypothesisbox1`、`hypothesisbox2`等。
  - 每个假设一框
  - 简要机制解释（1-2段）+基本证据（2-3分）+关键假设（1-2）
  - 目标：3-5假设
  - 保持高度简洁 - 详细信息参见附录

3. **可测试的预测**（0.5-1 页）
  - 对每个假设使用 `predictionbox`
  - 仅每个假设 1-2 个最关键的预测
  - 非常简短 - 附录中的完整预测

4. **关键比较**（0.5-1 页）
  - 仅使用 `comparisonbox` 进行最高优先级比较
  - 展示如何区分顶级假设
  - 附录中的其他比较

  * *正文总数：最多 4 页 - 对此处的内容非常有选择性**

### 附录（全面、详细）

* *附录A：综合文献综述**
- 详细背景（广泛引用）
- 当前理解
- 每个假设的证据（详细）
- 相互矛盾的发现
- 知识差距
- **目标：40-60+引用**

* *附录B：详细实验设计**
- 每个假设的完整方案
- 方法、对照、样本量
- 统计方法
- 可行性评估
- 时间表和资源要求

* *附录C：质量评估**
- 详细评估表
- 优势和劣势分析
- 比较评分
- 建议

* *附录D：补充证据**
- 类似机制
- 初步数据
- 理论框架
- 历史背景

* *参考文献**
- **目标：总共50+ 参考文献**

## 引文最佳实践

### 在正文中
- 引用 15-20 篇关键论文
- 使用 `\citep{author2023}` 进行括号引用
- 使用 `\citet{author2023}` 进行文本引用
- 重点关注最重要/最新的证据

### 在附录
- 总共引用40-60多篇论文
- 全面覆盖相关文献
- 包括评论、初步研究、理论论文
- 引用每一个主张和证据

### 引用密度指南
- 主要假设框：每个框2-3次引用（最重要）仅）
- 正文总数：最多 10-15 次引用（保持简洁）
- 附录 A 文献部分：每小节 8-15 次引用
- 实验设计：方法/先例 2-5 次引用
- 质量评估：评估标准所需的引用
- 总计文档：超过 50 次引用（绝大多数在附录中）

## 表格

### 专业表格格式

```latex
\begin{hypotable}{Caption}
\begin{tabular}{|l|l|l|}
\hline
\tableheadercolor
\textcolor{white}{\textbf{Header 1}} & \textcolor{white}{\textbf{Header 2}} \\
\hline
Data row 1 & Data \\
\hline
\tablerowcolor  % Alternating gray background
Data row 2 & Data \\
\hline
\end{tabular}
\caption{Your caption}
\end{hypotable}
```

* *最佳实践：**
- 使用 `\tableheadercolor` 作为标题行
- 备用`\tablerowcolor` 用于表格 >3 行
- 保持表格可读（不要太宽）
- 用于质量评估、比较

## 常见格式模式

### 假设部分模式

```latex
% Use \newpage before hypothesis box to prevent overflow
\newpage
\subsection*{Hypothesis N: [Concise Title]}

\begin{hypothesisboxN}[Hypothesis N: [Title]]

\textbf{Mechanistic Explanation:}

[1-2 brief paragraphs of explanation - 6-10 sentences max]

\vspace{0.3cm}

\textbf{Key Supporting Evidence:}
\begin{itemize}
  \item [Evidence 1] \citep{ref1}
  \item [Evidence 2] \citep{ref2}
  \item [Evidence 3] \citep{ref3}
\end{itemize}

\vspace{0.3cm}

\textbf{Core Assumptions:}
\begin{enumerate}
  \item [Assumption 1]
  \item [Assumption 2]
\end{enumerate}

\end{hypothesisboxN}

\vspace{0.5cm}
```

* *注：** `\newpage` 之前的假设框确保它从新页面开始，防止溢出。当盒子包含大量内容时，这一点尤其重要。

### 预测部分模式

```latex
\subsection*{Predictions from Hypothesis N}

\begin{predictionbox}[Predictions: Hypothesis N]

\textbf{Prediction N.1:} [Statement]
\begin{itemize}
  \item \textbf{Conditions:} [Conditions]
  \item \textbf{Expected Outcome:} [Outcome]
  \item \textbf{Falsification:} [Falsification]
\end{itemize}

\vspace{0.2cm}

\textbf{Prediction N.2:} [Statement]
[... continue ...]

\end{predictionbox}
```

### 比较部分模式

```latex
\subsection*{Distinguishing Hypothesis X vs. Hypothesis Y}

\begin{comparisonbox}[HX vs. HY: Key Distinction]

\textbf{Fundamental Difference:}

[Description of core difference]

\vspace{0.3cm}

\textbf{Discriminating Experiment:}

[Experiment description]

\vspace{0.3cm}

\textbf{Outcome Interpretation:}
\begin{itemize}
  \item \textbf{If [Result A]:} HX supported
  \item \textbf{If [Result B]:} HY supported
  \item \textbf{If [Result C]:} Both/neither supported
\end{itemize}

\end{comparisonbox}
```

## 间距和布局

### 垂直间距
- `\vspace{0.3cm}` - 框内元素之间
- `\vspace{0.5cm}` - 主要部分或框之间
- `\vspace{1cm}` - 标题之后，主要内容之前

### 分页符和溢出预防

* *关键：防止内容溢出**

LaTeX 框（tcolorbox 环境）不会自动跨页分隔。超出剩余页面空间的内容将溢出并导致格式问题。请遵循以下准则：

1. **长框之前的策略性分页符：**
```latex
\newpage  % Start on fresh page if box will be long
\begin{hypothesisbox1}[Hypothesis 1: Title]
  % Substantial content here
\end{hypothesisbox1}
```

2. **监控框内容长度：**
  - 每个假设框最多应≤0.7页
  - 如果机制解释+证据+假设超过~0.6页，内容太长
  - 解决方案：将详细内容移至附录，仅在主文本框中保留要点

3. **何时使用 `\newpage`：**
  - 在具有 >3 个小节或 >15 行内容的任何假设框之前 
  - 在具有大量实验描述的比较框之前 
  - 在主要附录部分之间 
  - 如果在开始新框之前当前页面上剩余的页数少于 0.6 页

4. **正文内容长度指南：**
  - 执行摘要框：最大 0.5-0.8 页 
  - 每个假设框：最大 0.4-0.6 页 
  - 每个预测框：最大 0.3-0.5 页 
  - 每个比较框：最大 0.4-0.6 页 

5. **分解长内容：**
 ```latex
 % GOOD：带有分页符的简洁正文
 \newpage
 \begin{hypothesisbox1}[假设1：简短标题]
 \textbf{机制说明：}
 1-2 段（6-10 句）简要概述。
 
 \textbf{关键支持证据：}
 \begin{itemize}
 \item 证据 1 \citep{ref1}
 \item 证据2 \citep{ref2}
 \end{itemize}
 
 \textbf{核心假设：}
 \begin{枚举}
 \item 假设 1
 \end{枚举}
 
 详细机制和综合证据参见附录A。
 \end{hypothesisbox1}
 ```

```latex
 % BAD：内容过长，会溢出
 \begin{hypothesisbox1}[假设 1]
 \subsection{非常长的部分}
 多个段落...
 \subsection{另一个长部分}
 更多段落...
 \subsection{更多内容}
 [内容继续超出页面边界 → 溢出！]
 \end{hypothesisbox1}
 ```

6。 **分页命令：**
 - `\newpage` - 强制新页（在长框之前推荐）
 - `\clearpage` - 强制新页并刷新浮动（在附录之前使用）

### 节间距
 已由样式包处理，但您可以调整：
```latex
\vspace{0.5cm}  % Add extra space if needed
```

##故障排除

###常见问题

**问题：“找不到文件假设_生成.sty”**
-解决方案：确保.sty文件与.tex文件位于同一目录中，或者在LaTeX中path

**问题：盒子没有颜色**
-解决方案：使用XeLaTeX或LuaLaTeX编译，而不是pdfLaTeX
-命令：`xelatex yourfile.tex`

**问题：引文显示为[？] **
-解决方案：之后运行bibtex第一个 xelatex 编译
```bash
xelatex yourfile.tex
bibtex yourfile
xelatex yourfile.tex
xelatex yourfile.tex
```

**问题：找不到字体**
-解决方案：如果未安装自定义字体，请注释掉 .sty 文件中的字体行
-要注释的行：`\setmainfont{...}` 和`\setsansfont{...}`

**问题：框标题与内容重叠**
-解决方案：在标题后使用 `\vspace{0.3cm}` 添加更多垂直空间

**问题：表格太宽**
-解决方案：在表格之前使用 `\small` 或 `\footnotesize`，或使用`p{width}`立柱规格

**问题：内容溢出页面**
- **原因：** 框（tcolorbox 环境）太长，无法容纳剩余页面空间
- **解决方案 1：** 在框前添加 `\newpage` 以在新页面上启动它
- **解决方案 2：** 减少框内容 - 将详细信息移至附录
- **解决方案3：**将内容分成多个较小的盒子
- **预防：**将每个假设框最多控制在0.4-0.6页；在内容丰富的方框前大量使用 `\newpage`

**问题：正文超过 4 页**
- **原因：** 方框包含太多详细信息
- **解决方案：** 积极将内容移至附录 - 主文本框应仅包含：
 - 简要机制概述 (1-2段落）
 - 2-3 个关键证据要点
 - 1-2 个核心假设
 - 所有详细解释、附加证据和全面讨论都包含在附录中 A

### 软件包要求

确保安装这些软件包：
- `tcolorbox`（带有`most` 选项)
- `xcolor`
- `fontspec` (用于 XeLaTeX/LuaLaTeX)
- `fancyhdr`
- `titlesec`
- `enumitem`
- `booktabs`
- `natbib`

安装缺少的软件包：
```bash
# For TeX Live
tlmgr install tcolorbox xcolor fontspec fancyhdr titlesec enumitem booktabs natbib

# For MiKTeX (Windows)
# Use MiKTeX Package Manager GUI
```

##风格一致性提示

1。 **颜色使用**
 - 整个文档中的每个假设始终使用相同的颜色
 - H1 = 蓝色，H2 = 绿色，H3 = 紫色等。
 - 不要为相同的假设混合颜色

2。 **框用法**
 - 正文：假设框、预测框、比较框
 - 附录：可以根据需要使用证据框、限制框
 - 不要过度使用框——为关键内容保留

3。 **引文样式**
 - 始终保持一致的引文格式
 - 大多数引文使用`\citep{}`
 - 对多个引文进行分组：`\citep{ref1, ref2, ref3}`

4. **假设编号**
 - 一致地对假设进行编号（H1、H2、H3 等）
 - 在预测中使用相同的编号（H1 的 P1.1、P1.2）
 - 在比较中使用相同的编号（H1 与 H2）

5。 **语言**
 - 精确而具体
 - 避免模糊的语言（“可能”、“可能”、“可能”）
 - 尽可能使用主动语态
 - 在可行的情况下进行定量预测

##快速检查表

在最终确定文档之前：

- [ ]标题页面有现象名称
- [ ] **正文最多4页** 
- [ ]执行摘要简洁（0.5-1页）
- [ ]每个假设在其自己的彩色框中
- [ ]提出3-5个假设（不多）
- [ ]每个假设都有简短的机制解释（1-2 段）
- [ ]每个假设都有 2-3 个最重要的证据点并带有引文
- [ ]每个假设有 1-2 个最关键的假设
- [ ]每个假设有 1-2 个关键预测的预测框
- [ ]正文中的优先级比较框（其他在附录）
- [ ]确定的优先实验
- [ ] **在长框之前使用分页符（`\newpage`）以防止溢出**
- [ ] **没有内容溢出页面边界（仔细检查PDF）**
- [ ] **每个假设框≤0.6页（如果更长，详情移至附录）**
- [ ]附录 A 有全面的文献综述和详细证据 
- [ ]附录 B 有详细的实验方案 
- [ ]附录 C 有质量评估表 
- [ ]附录 D 有补充证据 
- [ ]正文引用 10-15 次（选择性）
- [ ]完整文档中总共有 50 多个引用
- [ ]所有方框都使用正确的颜色
- [ ]文档编译没有错误
- [ ]参考文献格式正确
- [ ] **编译后的PDF 目视检查是否有溢出问题**

## 示例最小文档

```latex
% !TEX program = xelatex
\documentclass[11pt,letterpaper]{article}
\usepackage{hypothesis_generation}
\usepackage{natbib}

\title{Role of X in Y}

\begin{document}
\maketitle

\section*{Executive Summary}
\begin{summarybox}[Executive Summary]
Brief overview of phenomenon and hypotheses.
\end{summarybox}

\section{Competing Hypotheses}

% Use \newpage before each hypothesis box to prevent overflow
\newpage
\subsection*{Hypothesis 1: Title}
\begin{hypothesisbox1}[Hypothesis 1: Title]
\textbf{Mechanistic Explanation:}
Brief explanation in 1-2 paragraphs.

\textbf{Key Supporting Evidence:}
\begin{itemize}
  \item Evidence point \citep{ref1}
\end{itemize}
\end{hypothesisbox1}

\newpage
\subsection*{Hypothesis 2: Title}
\begin{hypothesisbox2}[Hypothesis 2: Title]
\textbf{Mechanistic Explanation:}
Brief explanation in 1-2 paragraphs.

\textbf{Key Supporting Evidence:}
\begin{itemize}
  \item Evidence point \citep{ref2}
\end{itemize}
\end{hypothesisbox2}

\section{Testable Predictions}

\subsection*{Predictions from Hypothesis 1}
\begin{predictionbox}[Predictions: Hypothesis 1]
Predictions here.
\end{predictionbox}

\section{Critical Comparisons}

\subsection*{H1 vs. H2}
\begin{comparisonbox}[H1 vs. H2]
Comparison here.
\end{comparisonbox}

% Force new page before appendices
\appendix
\newpage
\appendixsection{Appendix A: Literature Review}
Detailed literature review here.

\newpage
\bibliographystyle{plainnat}
\bibliography{references}

\end{document}
```

* *要点：**
- `\newpage` 在每个假设框之前使用，以确保它们从新页面开始
- 这可以防止内容溢出问题
- 主文本框保持简洁（1-2 段 + 要点）
- 详细内容参见附录

## 其他资源

- 请参阅`hypothesis_report_template.tex`了解完整的注释模板
- 请参阅`SKILL.md`了解工作流程和方法指南
- 请参阅`references/hypothesis_quality_criteria.md`了解评估框架
- 请参阅`references/experimental_design_patterns.md`了解设计指导
  - 请参阅 treatment-plans 技能以获取其他 LaTeX 样式示例
