# 专业治疗计划样式 - 快速参考

## 文件位置
`medical_treatment_plan.sty` - 可在资产目录中找到

## 快速入门

```latex
% !TEX program = xelatex
\documentclass[11pt,letterpaper]{article}
\usepackage{medical_treatment_plan}
\usepackage{natbib}

\begin{document}
\maketitle
% Your content
\end{document}
```

## 自定义框环境

### 1. 信息框（蓝色）- 常规信息
```latex
\begin{infobox}[Title]
  Content
\end{infobox}
```
**用于：**临床评估、监测计划、滴定方案

### 2. 警告框（黄色/红色）- 严重警报
```latex
\begin{warningbox}[Title]
  Critical information
\end{warningbox}
```
**用于：** 安全方案、决策点、禁忌症

### 3. 目标框（绿色）- 治疗目标
```latex
\begin{goalbox}[Title]
  Goals and targets
\end{goalbox}
```
**用于：** 智能目标、目标结果、成功指标

### 4. 要点框（浅蓝色）- 亮点
```latex
\begin{keybox}[Title]
  Important highlights
\end{keybox}
```
**用于：** 执行摘要、要点、基本建议

### 5. 应急箱（红色）- 紧急情况信息
```latex
\begin{emergencybox}
  Emergency contacts
\end{emergencybox}
```
**用于：**紧急联系人、紧急协议

### 6. 患者信息框（白色/蓝色）- 人口统计
```latex
\begin{patientinfo}
  Patient information
\end{patientinfo}
```
**用于：** 患者人口统计和基线数据

## 专业表格

```latex
\begin{medtable}{Caption}
\begin{tabular}{|l|l|l|}
\hline
\tableheadercolor
\textcolor{white}{\textbf{Header 1}} & \textcolor{white}{\textbf{Header 2}} \\
\hline
Data row 1 \\
\hline
\tablerowcolor  % Alternating gray
Data row 2 \\
\hline
\end{tabular}
\caption{Table caption}
\end{medtable}
```

## 配色方案

- **主蓝色** (0, 102, 153)：标题、标题
- **次蓝色** (102, 178, 204)：浅色背景
- **强调蓝色** (0, 153, 204)：链接、亮点
- **成功绿色** (0, 153, 76)：目标
- **红色警告** (204, 0, 0)：警告

## 编译

```bash
xelatex document.tex
bibtex document
xelatex document.tex
xelatex document.tex
```

## 最佳实践

1. **将匹配框类型与目的匹配：** 绿色表示目标，红色/黄色表示警告
2. **不要过度使用盒子：** 仅保留重要信息
3. **保持颜色一致性：** 坚持定义的方案
4. **使用空白：** 在主要部分之间添加 `\vspace{0.5cm}`
5. **表格交替行：** 使用 `\tablerowcolor` 提高可读性

## 安装

 * *选项 1：** 将 `assets/medical_treatment_plan.sty` 复制到您的文档目录

* *选项2：**安装到用户TeX目录
```bash
mkdir -p ~/texmf/tex/latex/medical_treatment_plan
cp assets/medical_treatment_plan.sty ~/texmf/tex/latex/medical_treatment_plan/
texhash ~/texmf
```

## 所需包
全部按样式自动加载：
- tcolorbox、tikz、xcolor
- fancyhdr、titlesec、enumitem
- booktabs、longtable、array、 colortbl
- hyperref、natbib、fontspec

## 示例结构

```latex
\maketitle

\section*{Patient Information}
\begin{patientinfo}
  Demographics
\end{patientinfo}

\section{Executive Summary}
\begin{keybox}[Plan Overview]
  Key highlights
\end{keybox}

\section{Treatment Goals}
\begin{goalbox}[SMART Goals]
  Goals list
\end{goalbox}

\section{Medication Plan}
\begin{infobox}[Dosing]
  Instructions
\end{infobox}

\begin{warningbox}[Safety]
  Warnings
\end{warningbox}

\section{Emergency}
\begin{emergencybox}
  Contacts
\end{emergencybox}
```

## 故障排除

* *缺少包：**
```bash
sudo tlmgr install tcolorbox tikz pgf
```

* *不包含特殊字符显示：**
- 使用 XeLaTeX 而不是 PDFLaTeX
- 或使用 LaTeX 命令：`$\checkmark$`、`$\geq$`

* *标题警告：**
- 已在样式文件中设置为 22pt
- 调整如果需要

- --

完整文档，请参阅SKILL.md

中的“专业文档样式”部分
