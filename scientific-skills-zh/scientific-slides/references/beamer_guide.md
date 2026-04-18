# LaTeX Beamer 科学演示指南

## 概述

Beamer 是一个 LaTeX 文档类，用于创建具有专业、一致格式的演示文稿。它特别适合包含方程、代码、算法和引文的科学演示。本指南涵盖了有效科学演讲的 Beamer 基础知识、主题、定制和高级功能。

## 为什么使用 Beamer？

### 优点

* *专业品质**：
- 一致、抛光的外观
- 漂亮的版式（尤其是数学）
- 出版质量输出
- 专业主题和模板

* *科学内容**：
- 本机方程支持（LaTeX 数学）
- 具有语法突出显示的代码列表
- 算法环境
- 参考书目集成
- 交叉引用

* *可重复性**：
- 纯文本源（版本控制友好）
- 编程图形生成
- 跨演示文稿的一致样式
- 易于维护和更新

* *效率**：
- 跨演示文稿重用内容演示文稿
- 模板一次，永远使用
- 自动化元素（页码、导航）
- 无需手动格式化

### 缺点

* *学习曲线**：
- 需要LaTeX 知识
- 编译time
- 调试可能具有挑战性
- 比PowerPoint更少所见即所得

* *灵活性**：
- 复杂的自定义布局需要努力
- 图像编辑需要外部工具
- PowerPoint中的一些设计元素更容易
- 动画更多有限

* *协作**：
- 对于非LaTeX用户来说不理想
- 可能存在版本冲突
- 需要LaTeX安装

## 基本Beamer文档结构

### 最小示例

```latex
\documentclass{beamer}

% Theme
\usetheme{Madrid}
\usecolortheme{beaver}

% Title information
\title{Your Presentation Title}
\subtitle{Optional Subtitle}
\author{Your Name}
\institute{Your Institution}
\date{\today}

\begin{document}

% Title slide
\begin{frame}
  \titlepage
\end{frame}

% Content slide
\begin{frame}{Slide Title}
  Content goes here
\end{frame}

\end{document}
```

### 基本包

```latex
\documentclass{beamer}

% Encoding and fonts
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

% Graphics
\usepackage{graphicx}
\graphicspath{{./figures/}}

% Math
\usepackage{amsmath, amssymb, amsthm}

% Tables
\usepackage{booktabs}
\usepackage{multirow}

% Colors
\usepackage{xcolor}

% Algorithms
\usepackage{algorithm}
\usepackage{algorithmic}

% Code listings
\usepackage{listings}

% Citations
\usepackage[style=authoryear,backend=biber]{biblatex}
\addbibresource{references.bib}
```

### 框架基础知识

```latex
% Basic frame
\begin{frame}{Title}
  Content
\end{frame}

% Frame with subtitle
\begin{frame}{Title}{Subtitle}
  Content
\end{frame}

% Frame without title
\begin{frame}
  Content
\end{frame}

% Fragile frame (for verbatim/code)
\begin{frame}[fragile]{Code Example}
  \begin{verbatim}
  def hello():
      print("Hello")
  \end{verbatim}
\end{frame}

% Plain frame (no header/footer)
\begin{frame}[plain]
  Full slide content
\end{frame}
```

## 主题和外观

### 演示主题

Beamer 包括许多控制整体布局的内置主题：

* *经典主题**：
```latex
\usetheme{Berlin}      % Sections in header
\usetheme{Copenhagen}  % Minimal, clean
\usetheme{Madrid}      % Professional, rounded
\usetheme{Boadilla}    % Simple footer
\usetheme{AnnArbor}    % Vertical navigation
```

* *现代主题**：
```latex
\usetheme{CambridgeUS}  % Blue theme
\usetheme{Singapore}    % Minimalist
\usetheme{Rochester}    % Very minimal
\usetheme{Antibes}      % Tree navigation
```

* *科学流行**：
```latex
% Clean and minimal
\usetheme{default}
\usetheme{Copenhagen}

% Professional with navigation
\usetheme{Madrid}
\usetheme{Berlin}

% Traditional academic
\usetheme{Pittsburgh}
\usetheme{Boadilla}
```

### 颜色主题

```latex
% Blue themes
\usecolortheme{default}      % Blue
\usecolortheme{dolphin}      % Cyan-blue
\usecolortheme{seagull}      % Grayscale

% Warm themes
\usecolortheme{beaver}       % Red/brown
\usecolortheme{rose}         % Pink/red

% Nature themes
\usecolortheme{orchid}       % Purple
\usecolortheme{crane}        % Orange/yellow

% Professional
\usecolortheme{albatross}    % Gray/blue
```

### 字体主题

```latex
\usefonttheme{default}              % Standard
\usefonttheme{serif}                % Serif fonts
\usefonttheme{structurebold}        % Bold structure
\usefonttheme{structureitalicserif} % Italic serif
\usefonttheme{professionalfonts}    % Professional fonts
```

### 自定义颜色

```latex
% Define custom colors
\definecolor{myblue}{RGB}{0,115,178}
\definecolor{myred}{RGB}{214,40,40}

% Apply to theme elements
\setbeamercolor{structure}{fg=myblue}
\setbeamercolor{title}{fg=myred}
\setbeamercolor{frametitle}{fg=myblue,bg=white}
\setbeamercolor{block title}{fg=white,bg=myblue}
```

### 最小自定义主题

```latex
% Remove navigation symbols
\setbeamertemplate{navigation symbols}{}

% Page numbers
\setbeamertemplate{footline}[frame number]

% Simple itemize
\setbeamertemplate{itemize items}[circle]

% Clean blocks
\setbeamertemplate{blocks}[rounded][shadow=false]

% Colors
\setbeamercolor{structure}{fg=blue!70!black}
\setbeamercolor{title}{fg=black}
\setbeamercolor{frametitle}{fg=blue!70!black}
```

## 内容元素

### 列表

* *逐项**：
```latex
\begin{frame}{Bullet Points}
  \begin{itemize}
    \item First point
    \item Second point
      \begin{itemize}
        \item Nested point
      \end{itemize}
    \item Third point
  \end{itemize}
\end{frame}
```

* *枚举**：
```latex
\begin{frame}{Numbered List}
  \begin{enumerate}
    \item First item
    \item Second item
    \item Third item
  \end{enumerate}
\end{frame}
```

* *描述**：
```latex
\begin{frame}{Definitions}
  \begin{description}
    \item[Term 1] Definition of term 1
    \item[Term 2] Definition of term 2
  \end{description}
\end{frame}
```

### 列

```latex
\begin{frame}{Two Column Layout}
  \begin{columns}
    
    % Left column
    \begin{column}{0.5\textwidth}
      \begin{itemize}
        \item Point 1
        \item Point 2
      \end{itemize}
    \end{column}
    
    % Right column
    \begin{column}{0.5\textwidth}
      \includegraphics[width=\textwidth]{figure.png}
    \end{column}
    
  \end{columns}
\end{frame}
```

* *三列布局**：
```latex
\begin{columns}[T] % Align at top
  \begin{column}{0.32\textwidth}
    Content A
  \end{column}
  \begin{column}{0.32\textwidth}
    Content B
  \end{column}
  \begin{column}{0.32\textwidth}
    Content C
  \end{column}
\end{columns}
```

### 数字

```latex
\begin{frame}{Figure Example}
  \begin{figure}
    \centering
    \includegraphics[width=0.8\textwidth]{figure.pdf}
    \caption{Figure caption text}
  \end{figure}
\end{frame}
```

* *并排数字**：
```latex
\begin{frame}{Comparison}
  \begin{columns}
    \begin{column}{0.5\textwidth}
      \includegraphics[width=\textwidth]{fig1.pdf}
      \caption{Condition A}
    \end{column}
    \begin{column}{0.5\textwidth}
      \includegraphics[width=\textwidth]{fig2.pdf}
      \caption{Condition B}
    \end{column}
  \end{columns}
\end{frame}
```

* *子数字**：
```latex
\usepackage{subcaption}

\begin{frame}{Multiple Panels}
  \begin{figure}
    \centering
    \begin{subfigure}{0.45\textwidth}
      \includegraphics[width=\textwidth]{fig1.pdf}
      \caption{Panel A}
    \end{subfigure}
    \hfill
    \begin{subfigure}{0.45\textwidth}
      \includegraphics[width=\textwidth]{fig2.pdf}
      \caption{Panel B}
    \end{subfigure}
    \caption{Overall figure caption}
  \end{figure}
\end{frame}
```

### 表格

```latex
\begin{frame}{Table Example}
  \begin{table}
    \centering
    \begin{tabular}{lcc}
      \toprule
      Method & Accuracy & Time \\
      \midrule
      Method A & 0.85 & 10s \\
      Method B & 0.92 & 25s \\
      Method C & 0.88 & 15s \\
      \bottomrule
    \end{tabular}
    \caption{Performance comparison}
  \end{table}
\end{frame}
```

### 块

* *标准块**：
```latex
\begin{frame}{Block Examples}
  
  % Standard block
  \begin{block}{Block Title}
    Block content goes here
  \end{block}
  
  % Alert block (red)
  \begin{alertblock}{Important}
    Warning or important information
  \end{alertblock}
  
  % Example block (green)
  \begin{exampleblock}{Example}
    Example content
  \end{exampleblock}
  
\end{frame}
```

* *定理环境**：
```latex
\begin{frame}{Mathematical Results}
  
  \begin{theorem}
    Statement of theorem
  \end{theorem}
  
  \begin{proof}
    Proof goes here
  \end{proof}
  
  \begin{definition}
    Definition text
  \end{definition}
  
  \begin{lemma}
    Lemma statement
  \end{lemma}
  
\end{frame}
```

## 叠加和动画

### 渐进式披露\pause

```latex
\begin{frame}{Revealing Content}
  First point appears immediately
  
  \pause
  
  Second point appears on click
  
  \pause
  
  Third point appears on another click
\end{frame}
```

### 覆盖规范

* *使用覆盖逐项列出**：
```latex
\begin{frame}{Sequential Bullets}
  \begin{itemize}
    \item<1-> Appears on slide 1 and stays
    \item<2-> Appears on slide 2 and stays
    \item<3-> Appears on slide 3 and stays
  \end{itemize}
\end{frame}
```

* *替代语法**：
```latex
\begin{frame}{Sequential Bullets}
  \begin{itemize}[<+->]  % Automatically sequential
    \item First point
    \item Second point
    \item Third point
  \end{itemize}
\end{frame}
```

### 使用叠加层突出显示

* *特定幻灯片上的警报**：
```latex
\begin{frame}{Highlighting}
  \begin{itemize}
    \item Normal text
    \item<2-| alert@2> Text highlighted on slide 2
    \item Normal text
  \end{itemize}
\end{frame}
```

* *临时外观**：
```latex
\begin{frame}{Appearing and Disappearing}
  Appears on all slides
  
  \only<2>{Only visible on slide 2}
  
  \uncover<3->{Appears on slide 3 and stays}
  
  \visible<4->{Also appears on slide 4, but reserves space}
\end{frame}
```

### 构建复杂图形

```latex
\begin{frame}{Building a Figure}
  \begin{tikzpicture}
    % Base elements (always visible)
    \draw (0,0) rectangle (4,3);
    
    % Add on slide 2+
    \draw<2-> (1,1) circle (0.5);
    
    % Add on slide 3+
    \draw<3->[->, thick] (2,1.5) -- (3,2);
    
    % Highlight on slide 4
    \node<4>[red,thick] at (2,1.5) {Result};
  \end{tikzpicture}
\end{frame}
```

## 数学内容

### 方程

* *内联数学**:
```latex
\begin{frame}{Inline Math}
  The equation $E = mc^2$ is famous.
  
  We can also write $\alpha + \beta = \gamma$.
\end{frame}
```

* *显示数学**:
```latex
\begin{frame}{Display Equations}
  Single equation:
  \begin{equation}
    f(x) = \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
  \end{equation}
  
  Multiple equations:
  \begin{align}
    E &= mc^2 \\
    F &= ma \\
    V &= IR
  \end{align}
\end{frame}
```

* *方程数组**:
```latex
\begin{frame}{Equation System}
  \begin{equation}
    \begin{cases}
      \dot{x} = f(x,y) \\
      \dot{y} = g(x,y)
    \end{cases}
  \end{equation}
\end{frame}
```

### 矩阵

```latex
\begin{frame}{Matrix Example}
  \begin{equation}
    A = \begin{bmatrix}
      a_{11} & a_{12} & a_{13} \\
      a_{21} & a_{22} & a_{23} \\
      a_{31} & a_{32} & a_{33}
    \end{bmatrix}
  \end{equation}
\end{frame}
```

## 代码和算法

### 代码列表

```latex
\begin{frame}[fragile]{Python Code}
  \begin{lstlisting}[language=Python]
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
  \end{lstlisting}
\end{frame}
```

* *自定义代码样式**：
```latex
\lstset{
  language=Python,
  basicstyle=\ttfamily\small,
  keywordstyle=\color{blue},
  commentstyle=\color{green!60!black},
  stringstyle=\color{orange},
  numbers=left,
  numberstyle=\tiny,
  frame=single,
  breaklines=true
}

\begin{frame}[fragile]{Styled Code}
  \begin{lstlisting}
  # This is a comment
  def hello(name):
      """Greet someone"""
      print(f"Hello, {name}")
  \end{lstlisting}
\end{frame}
```

### 算法

```latex
\begin{frame}{Algorithm Example}
  \begin{algorithm}[H]
    \caption{Quicksort}
    \begin{algorithmic}[1]
      \REQUIRE Array $A$, indices $low$, $high$
      \ENSURE Sorted array
      \IF{$low < high$}
        \STATE $pivot \gets partition(A, low, high)$
        \STATE $quicksort(A, low, pivot-1)$
        \STATE $quicksort(A, pivot+1, high)$
      \ENDIF
    \end{algorithmic}
  \end{algorithm}
\end{frame}
```

## 引文和参考书目

### 内联引文

```latex
\begin{frame}{Background}
  Previous work \cite{smith2020} showed that...
  
  Multiple studies \cite{jones2019,brown2021} have found...
  
  According to \textcite{davis2022}, the method works by...
\end{frame}
```

### 参考书目幻灯片

```latex
% At end of presentation
\begin{frame}[allowframebreaks]{References}
  \printbibliography
\end{frame}
```

### 自定义参考书目样式

```latex
% In preamble
\usepackage[style=authoryear,maxbibnames=2,maxcitenames=2]{biblatex}
\addbibresource{references.bib}

% Smaller font for references
\renewcommand*{\bibfont}{\scriptsize}
```

## 高级功能

### 部分组织

```latex
\section{Introduction}
\begin{frame}{Introduction}
  Content
\end{frame}

\section{Methods}
\begin{frame}{Methods}
  Content
\end{frame}

% Automatic outline
\begin{frame}{Outline}
  \tableofcontents
\end{frame}

% Outline at each section
\AtBeginSection{
  \begin{frame}{Outline}
    \tableofcontents[currentsection]
  \end{frame}
}
```

### 备份幻灯片

```latex
% Main presentation ends
\begin{frame}{Thank You}
  Questions?
\end{frame}

% Backup slides (not counted in numbering)
\appendix

\begin{frame}{Extra Data}
  Additional analysis for questions
\end{frame}

\begin{frame}{Detailed Methods}
  More methodological details
\end{frame}
```

### 超链接

```latex
% Define labels
\begin{frame}{Main Result}
  \label{mainresult}
  This is the main finding.
\end{frame}

% Link to labeled frame
\begin{frame}{Reference}
  As shown in the \hyperlink{mainresult}{main result}...
\end{frame}

% External links
\begin{frame}{Resources}
  Visit \url{https://example.com} for more information.
  
  \href{https://github.com/user/repo}{GitHub Repository}
\end{frame}
```

### QR代码

```latex
\usepackage{qrcode}

\begin{frame}{Scan for Paper}
  \begin{center}
    \qrcode[height=3cm]{https://doi.org/10.1234/paper}
    
    \vspace{0.5cm}
    Scan for full paper
  \end{center}
\end{frame}
```

### 多媒体

```latex
\usepackage{multimedia}

\begin{frame}{Video}
  \movie[width=8cm,height=6cm]{Click to play}{video.mp4}
\end{frame}
```

* *注意**：多媒体支持因PDF 查看器而异。

## TikZ Graphics

### 基本形状

```latex
\usepackage{tikz}

\begin{frame}{TikZ Example}
  \begin{tikzpicture}
    % Rectangle
    \draw (0,0) rectangle (2,1);
    
    % Circle
    \draw (3,0.5) circle (0.5);
    
    % Line with arrow
    \draw[->, thick] (0,0) -- (3,2);
    
    % Node with text
    \node at (1.5,2) {Label};
  \end{tikzpicture}
\end{frame}
```

### 流程图

```latex
\usetikzlibrary{shapes,arrows,positioning}

\begin{frame}{Workflow}
  \begin{tikzpicture}[node distance=2cm]
    \node[rectangle,draw] (start) {Start};
    \node[rectangle,draw,right=of start] (process) {Process};
    \node[rectangle,draw,right=of process] (end) {End};
    
    \draw[->,thick] (start) -- (process);
    \draw[->,thick] (process) -- (end);
  \end{tikzpicture}
\end{frame}
```

### 绘图

```latex
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}

\begin{frame}{Data Plot}
  \begin{tikzpicture}
    \begin{axis}[
      xlabel={$x$},
      ylabel={$y$},
      width=8cm,
      height=6cm
    ]
    \addplot[blue,thick] coordinates {
      (0,0) (1,1) (2,4) (3,9)
    };
    \addplot[red,dashed] {x};
    \end{axis}
  \end{tikzpicture}
\end{frame}
```

## 编译

### 基本编译

```bash
# Standard compilation
pdflatex presentation.tex

# With bibliography
pdflatex presentation.tex
biber presentation
pdflatex presentation.tex
pdflatex presentation.tex
```

### 现代编译（推荐）

```bash
# Using latexmk (automated)
latexmk -pdf presentation.tex

# With continuous preview
latexmk -pdf -pvc presentation.tex
```

### 编译选项

```bash
# Faster compilation (draft mode)
pdflatex -draftmode presentation.tex

# Specific engine
lualatex presentation.tex    # Better Unicode support
xelatex presentation.tex     # System fonts

# Output directory
pdflatex -output-directory=build presentation.tex
```

## 讲义和注释

### 创建讲义

```latex
% In preamble
\documentclass[handout]{beamer}

% This removes overlays and creates one frame per slide
```

### 演讲者注释

```latex
\usepackage{pgfpages}
\setbeameroption{show notes on second screen=right}

\begin{frame}{Slide Title}
  Slide content visible to audience
  
  \note{
    These notes are visible only to speaker:
    - Remember to emphasize X
    - Mention collaboration with Y
    - Expect question about Z
  }
\end{frame}
```

### 带注释的讲义

```latex
\documentclass[handout]{beamer}
\usepackage{pgfpages}
\pgfpagesuselayout{2 on 1}[a4paper,border shrink=5mm]
```

## 最佳实践

### 这样做的

- ✅ 始终使用一致的主题
- ✅ 保持方程简单而大
- ✅ 使用渐进式披露（\暂停，覆盖）
- ✅ 包含帧编号
- ✅ 对图形使用矢量图形（PDF）
- ✅ 尽早测试编译并且经常
- ✅ 使用有意义的章节名称
- ✅ 在附录中保留备份幻灯片

### 不要使用

- ❌ 不要使用太多不同的字体或颜色
- ❌ 不要用密集的文本填充幻灯片
- ❌ 不要使用小字体大小
- ❌ 不要包含复杂的动画（有限支持）
- ❌ 不要忘记代码的脆弱框架
- ❌ 不要不一致地混合主题
- ❌ 不要忽略编译警告

## 故障排除

### 常见问题

* *缺少易碎品**：
```
Error: Verbatim environment in frame
Solution: Add [fragile] option to frame
```

* *软件包冲突**：
```
Error: Option clash for package X
Solution: Load package in preamble only once
```

* *图像不存在找到**：
```
Error: File `figure.pdf' not found
Solution: Check path, use \graphicspath, ensure file exists
```

* *叠加问题**：
```
Problem: Overlays not working as expected
Solution: Check syntax <n-> vs <n-m>, test incremental builds
```

### 调试技巧

```latex
% Show frame labels
\usepackage[notref,notcite]{showkeys}

% Draft mode (faster, shows boxes)
\documentclass[draft]{beamer}

% Verbose error messages
\errorcontextlines=999
```

## 模板和示例

### 最小工作示例

请参阅 `assets/beamer_template_conference.tex`，了解完整的、可定制的会议演讲模板。

### 资源

- Beamer 用户指南：`texdoc beamer`
- 主题库：https://deic.uab.cat/~iblanes/beamer_gallery/
- TikZ 示例：https://texample.net/tikz/

## 摘要

Beamer 擅长：
- 数学内容
- 一致的专业格式
- 可复制的演示文稿
- 版本控制
- 引用和交叉引用

在以下情况下选择 Beamer：
- 演示文稿包含重要的数学/方程
- 您重视版本控制和纯文本
- 一致的样式优先 
- 您对 LaTeX

 感到满意在以下情况下考虑使用 PowerPoint：
- 需要大量自定义图形
- 与非 LaTeX 用户协作
- 需要复杂动画
- 需要快速原型设计
