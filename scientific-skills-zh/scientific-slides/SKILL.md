---
name: scientific-slides
description: 为研究演讲构建幻灯片和演示文稿。使用它来制作 PowerPoint 幻灯片、会议演示、研讨会演讲、研究演示、论文答辩幻灯片或任何科学演讲。提供幻灯片结构、设计模板、计时指导和视觉验证。适用于 PowerPoint 和 LaTeX Beamer。
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 科学幻灯片

## 概述

科学演示是交流研究、分享发现以及与学术和专业受众互动的重要媒介。该技能为创建有效的科学演示提供了全面的指导，从结构和内容开发到视觉设计和交付准备。

* *重点**：会议、研讨会、答辩和专业演讲的口头演示。

* *关键设计理念**：科学演示应该具有视觉吸引力并有研究支持。不惜一切代价避免使用枯燥、文字较多的幻灯片。伟大的科学演示结合了：
- **引人注目的视觉效果**：高质量的图形、图像、图表（不仅仅是要点）
- **研究背景**：正确引用 research-lookup 建立可信度
- **最小文本**：要点作为提示，您口头提供解释
- **专业设计**：现代配色方案、强烈的视觉层次、宽敞的空白
- **故事驱动**：清晰的叙事弧，而不仅仅是数据转储

  * *记住**：无聊的演示=被遗忘的科学。通过适当的引用使您的幻灯片在视觉上令人难忘，同时保持科学严谨性。

## 何时使用此技能

此技能应在以下情况下使用：
- 准备会议演示（5-20分钟）
- 开展学术研讨会（45-60分钟）
- 创建论文或论文答辩演示文稿
- 设计资助推介演示文稿
- 准备期刊俱乐部演示文稿
- 在机构或公司进行研究讲座
- 关于科学主题的教学或教程演示

## 使用 Nano Banana Pro 生成幻灯片

* *此技能使用 Nano Banana Pro AI 生成令人惊叹的演示文稿幻灯片自动。**

根据输出格式，有两种工作流程：

### 默认工作流程：PDF 幻灯片（推荐）

使用 Nano Banana Pro 将每张幻灯片生成完整图像，然后组合成 PDF。这会产生视觉上最令人惊叹的结果。

* *工作原理：**
1. **计划幻灯片**：为每张幻灯片创建详细计划（标题、要点、视觉元素）
2. **生成幻灯片**：为每张幻灯片调用 Nano Banana Pro 以创建完整的幻灯片图像
3. **组合到 PDF**：将幻灯片图像组装到单个 PDF 演示文稿中

* *步骤 1：规划每张幻灯片**

在生成之前，为您的演示文稿创建详细计划：

```markdown
# Presentation Plan: Introduction to Machine Learning

## Slide 1: Title Slide
- Title: "Machine Learning: From Theory to Practice"
- Subtitle: "AI Conference 2025"
- Speaker: Dr. Jane Smith, University of XYZ
- Visual: Modern abstract neural network background

## Slide 2: Introduction
- Title: "Why Machine Learning Matters"
- Key points: Industry adoption, breakthrough applications, future potential
- Visual: Icons showing different ML applications (healthcare, finance, robotics)

## Slide 3: Core Concepts
- Title: "The Three Types of Learning"
- Content: Supervised, Unsupervised, Reinforcement
- Visual: Three-part diagram showing each type with examples

... (continue for all slides)
```

* *步骤 2：生成每张幻灯片**

使用用于创建每张幻灯片的 `generate_slide_image.py` 脚本。

* *关键：格式一致性协议**

为了确保演示文稿中所有幻灯片的统一格式：

1. **在演示文稿开始时定义格式目标**，并将其包含在每个提示中：
  - 配色方案（例如，“深蓝色背景，白色文本，金色强调”）
  - 版式风格（例如，“粗体无衬线标题，干净的正文文本”）
  - 视觉风格（例如，“简约、专业、企业美学”）
  - 布局方法（例如，“大量空白，左对齐内容”）

2. **使用 `--attach`:
 生成后续幻灯片时，始终附加上一张幻灯片** - 这允许 Nano Banana Pro 查看并匹配现有样式
 - 在整个甲板上创建视觉连续性
  - 确保颜色、字体和设计语言一致

3. **默认作者是“K-Dense”**除非指定其他名称

4. **直接在提示中包含引文**，对于引用研究的幻灯片：
  - 在提示文本中添加引文，以便它们出现在生成的幻灯片上
  - 使用格式：“包含引文：（作者等人，年份）”或“显示参考文献：作者等人，年份”
  - 对于多个引用，请在提示中全部列出
  - 引文应以小文本形式出现在幻灯片底部或相关内容附近

5. **附加结果幻灯片的现有图形/数据**（对于数据驱动的演示至关重要）：
  - 创建有关结果的幻灯片时，始终检查以下位置中的现有图形：
  - 工作目录（例如，`figures/`、`results/`、`plots/`、 `images/`)
  - 用户提供的输入文件或目录
  - 与演示相关的任何数据可视化、图表或图形
  - 使用 `--attach` 包含这些数字，以便 Nano Banana Pro 可以合并它们：
  - 附加结果幻灯片的实际数据图形/图表
  - 附加相关的方法幻灯片的图表
  - 为标题幻灯片附加徽标或机构图像
  - 附加数据图时，在提示中描述您想要的内容：
  - “创建一张幻灯片，展示所附结果图表，突出显示关键发现”
  - “围绕此附图构建幻灯片，添加标题和项目符号点解释数据”
  - “合并将所附图表放入带有解释的结果幻灯片中“
  - **生成结果幻灯片之前**：列出工作目录中的文件以查找相关图表
  - 可以附加多个图表：`--attach fig1.png --attach fig2.png`

  * *具有格式一致性、引文和图表附件的示例：**

```bash
# Title slide (first slide - establishes the style)
python scripts/generate_slide_image.py "Title slide for presentation: 'Machine Learning: From Theory to Practice'. Subtitle: 'AI Conference 2025'. Speaker: K-Dense. FORMATTING GOAL: Dark blue background (#1a237e), white text, gold accents (#ffc107), minimal design, sans-serif fonts, generous margins, no decorative elements." -o slides/01_title.png

# Content slide with citations (attach previous slide for consistency)
python scripts/generate_slide_image.py "Presentation slide titled 'Why Machine Learning Matters'. Three key points with simple icons: 1) Industry adoption, 2) Breakthrough applications, 3) Future potential. CITATIONS: Include at bottom in small text: (LeCun et al., 2015; Goodfellow et al., 2016). FORMATTING GOAL: Match attached slide style - dark blue background, white text, gold accents, minimal professional design, no visual clutter." -o slides/02_intro.png --attach slides/01_title.png

# Background slide with multiple citations
python scripts/generate_slide_image.py "Presentation slide titled 'Deep Learning Revolution'. Key milestones: ImageNet breakthrough (2012), transformer architecture (2017), GPT models (2018-present). CITATIONS: Show references at bottom: (Krizhevsky et al., 2012; Vaswani et al., 2017; Brown et al., 2020). FORMATTING GOAL: Match attached slide style exactly - same colors, fonts, minimal design." -o slides/03_background.png --attach slides/02_intro.png

# RESULTS SLIDE - Attach actual data figure from working directory
# First, check what figures exist: ls figures/ or ls results/
python scripts/generate_slide_image.py "Presentation slide titled 'Model Performance Results'. Create a slide presenting the attached accuracy chart. Key findings to highlight: 1) 95% accuracy achieved, 2) Outperforms baseline by 12%, 3) Consistent across test sets. CITATIONS: Include at bottom: (Our results, 2025). FORMATTING GOAL: Match attached slide style exactly." -o slides/04_results.png --attach slides/03_background.png --attach figures/accuracy_chart.png

# RESULTS SLIDE - Multiple figures comparison
python scripts/generate_slide_image.py "Presentation slide titled 'Before vs After Comparison'. Build a side-by-side comparison slide using the two attached figures. Left: baseline results, Right: our improved results. Add brief labels explaining the improvement. FORMATTING GOAL: Match attached slide style exactly." -o slides/05_comparison.png --attach slides/04_results.png --attach figures/baseline.png --attach figures/improved.png

# METHODOLOGY SLIDE - Attach existing diagram
python scripts/generate_slide_image.py "Presentation slide titled 'System Architecture'. Present the attached architecture diagram with brief explanatory bullet points: 1) Input processing, 2) Model inference, 3) Output generation. FORMATTING GOAL: Match attached slide style exactly." -o slides/06_architecture.png --attach slides/05_comparison.png --attach diagrams/system_architecture.png
```

* *重要：在创建结果幻灯片之前，请始终：**
1. 列出工作目录中的文件：`ls -la figures/` 或 `ls -la results/`
2. 检查用户提供的目录中的相关数字
3. 附上应出现在幻灯片上的所有相关数字
4. 描述 Nano Banana Pro 应如何合并附图

* *提示模板：**

在每个提示中包含这些元素（根据需要自定义）：
```
[Slide content description]
CITATIONS: Include at bottom: (Author1 et al., Year; Author2 et al., Year)
FORMATTING GOAL: [Background color], [text color], [accent color], minimal professional design, no decorative elements, consistent with attached slide style.
```

* *步骤 3：组合到PDF**

```bash
# Combine all slides into a PDF presentation
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf
```

### PPT 工作流程：生成视觉效果的 PowerPoint

创建 PowerPoint 演示文稿时，使用 Nano Banana Pro 为每张幻灯片生成图像和图形，然后使用 PPTX 技能单独添加文本。

* *如何实现作品：**
1. **规划幻灯片**：为每张幻灯片 
2 创建内容计划。 **生成视觉效果**：使用带有 `--visual-only` 标志的 Nano Banana Pro 为幻灯片 
3 创建图像。 **构建 PPTX**：使用 PPTX 技能（html2pptx 或基于模板）创建带有生成的视觉效果和单独文本的幻灯片

* *步骤 1：为每张幻灯片生成视觉效果**

```bash
# Generate a figure for the introduction slide
python scripts/generate_slide_image.py "Professional illustration showing machine learning applications: healthcare diagnosis, financial analysis, autonomous vehicles, and robotics. Modern flat design, colorful icons on white background." -o figures/ml_applications.png --visual-only

# Generate a diagram for the methods slide
python scripts/generate_slide_image.py "Neural network architecture diagram showing input layer, three hidden layers, and output layer. Clean, technical style with node connections. Blue and gray color scheme." -o figures/neural_network.png --visual-only

# Generate a conceptual graphic for results
python scripts/generate_slide_image.py "Before and after comparison showing improvement: left side shows cluttered data, right side shows organized insights. Arrow connecting them. Professional business style." -o figures/results_visual.png --visual-only
```

* *步骤 2：使用 PPTX 构建 PowerPoint技能**

使用 PPTX 技能的 html2pptx 工作流程创建幻灯片，其中包括：
- 从步骤 1 生成的图像
- 单独添加标题和正文文本
- 专业布局和格式设置

请参阅 `scientific-skills-zh/pptx/SKILL.md` 了解完整的 PPTX 创建Documentation.

- --

## Nano Banana Pro 脚本参考

### generate_slide_image.py

使用 Nano Banana Pro AI.

 生成演示幻灯片或视觉效果```bash
# Full slide (default) - generates complete slide as image
python scripts/generate_slide_image.py "slide description" -o output.png

# Visual only - generates just the image/figure for embedding in PPT
python scripts/generate_slide_image.py "visual description" -o output.png --visual-only

# With reference images attached (Nano Banana Pro will see these)
python scripts/generate_slide_image.py "Create a slide explaining this chart" -o slide.png --attach chart.png
python scripts/generate_slide_image.py "Combine these into a comparison slide" -o compare.png --attach before.png --attach after.png
```

* *选项：**
- `-o, --output`：输出文件路径（必需）
- `--attach IMAGE`：附加图像文件作为生成上下文（可以多次使用）
- `--visual-only`：仅生成视觉/图形，而不是完整的Slide
- `--iterations`：最大细化迭代（默认值：2）
- `--api-key`：OpenRouter API密钥（或设置OPENROUTER_API_KEY环境变量）
- `-v, --verbose`：详细输出

* *附加参考图片：**

当您希望 Nano Banana Pro 将现有图像作为上下文查看时，请使用 `--attach`：
- “创建有关此数据的幻灯片”+附加数据图表
- “使用此徽标制作标题幻灯片”+附加徽标
- “将这些数字合并到一张幻灯片中”+附加多个图像
- “说明该图在幻灯片中”+附加图表

* *环境设置：**
```bash
export OPENROUTER_API_KEY='your_api_key_here'
# Get key at: https://openrouter.ai/keys
```

### slips_to_pdf.py

将多个幻灯片图像合并为一个PDF.

```bash
# Combine PNG files
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf

# Combine specific files in order
python scripts/slides_to_pdf.py title.png intro.png methods.png -o talk.pdf

# From directory (sorted by filename)
python scripts/slides_to_pdf.py slides/ -o presentation.pdf
```

* *选项：**
- `-o, --output`：输出PDF路径（必填）
- `--dpi`：PDF分辨率（默认： 150)
- `-v, --verbose`：详细输出

* *提示：** 使用数字命名幻灯片以确保正确排序：`01_title.png`、`02_intro.png` 等。

- --

## 幻灯片生成的提示写入

### 完整幻灯片提示（PDF 工作流程）

对于完整的幻灯片，包括：
1. **幻灯片类型**：标题幻灯片、内容幻灯片、图表幻灯片等。
2. **标题**：幻灯片标题文本
3. **内容**：要点、项目符号或描述
4. **视觉元素**：包含哪些图像、图标或图形
5. **设计风格**：配色方案、情绪、审美

* *提示示例：**

```
Title slide:
"Title slide for a medical research presentation. Title: 'Advances in Cancer Immunotherapy'. Subtitle: 'Clinical Trial Results 2024'. Professional medical theme with subtle DNA helix in background. Navy blue and white color scheme."

Content slide:
"Presentation slide titled 'Key Findings'. Three bullet points: 1) 40% improvement in response rate, 2) Reduced side effects, 3) Extended survival outcomes. Include relevant medical icons. Clean, professional design with green and white colors."

Diagram slide:
"Presentation slide showing the research methodology. Title: 'Study Design'. Flowchart showing: Patient Screening → Randomization → Treatment Groups (A, B, Control) → Follow-up → Analysis. CONSORT-style flow diagram. Professional academic style."
```

### 仅视觉提示（PPT 工作流程）

对于要嵌入 PowerPoint 的图像，重点关注视觉元素仅：

```
"Flowchart showing machine learning pipeline: Data Collection → Preprocessing → Model Training → Validation → Deployment. Clean technical style, blue and gray colors."

"Conceptual illustration of cloud computing with servers, data flow, and connected devices. Modern flat design, suitable for business presentation."

"Scientific diagram of cell division process showing mitosis phases. Educational style with labels, colorblind-friendly colors."
```

- --

## 科学原理图的视觉增强

除了幻灯片生成之外，还可以使用 **scientific-schematics** 技能绘制技术图表：

* *何时使用 scientific-schematics：**
- 复杂的技术图表（电路图、化学结构）
- 论文出版质量的图表（质量阈值较高）
- 需要科学准确性审核的图表

* *如何生成原理图：**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

有关创建原理图的详细指导，请参阅 scientific-schematics 技能文档。

- --

## 核心功能

### 1. 演示结构和组织

构建具有清晰的叙述流程和针对不同上下文的适当结构的演示。详细指导请参考`references/presentation_structure.md`.

* *宇宙故事篇**：
1. **挂钩**：吸引注意力（30-60 秒）
2. **上下文**：确定重要性（谈话的 5-10%）
3. **问题/差距**：识别未知内容（谈话的 5-10%）
4. **方法**：解释你的解决方案（占谈话的 15-25%）
5. **结果**：呈现主要发现（占讨论的 40-50%）
6. **含义**：讨论含义（占谈话的 15-20%）
7. **结束**：令人难忘的结论（1-2分钟）

* *演讲特定结构**：
- **会议演讲（15分钟）**：聚焦1-2个关键发现，最少的方法
- **学术研讨会（45分钟）**：全面覆盖，详细方法，多项研究
- **论文答辩（60 分钟）**：完整的论文概述，涵盖所有研究
- **资助推介（15 分钟）**：强调重要性、可行性和影响力
- **期刊俱乐部（30 分钟）**：对已发表作品的批判性分析

### 2. 幻灯片设计原则

创建专业、可读且易于理解的幻灯片，以增强理解。有关完整的设计指南，请参阅 `references/slide_design_principles.md`.

* *反模式：避免干燥、文本过多的演示**

❌ **是什么让演示文稿枯燥易忘：**
- 文字墙（每张幻灯片超过 6 个项目符号）
- 小字体（<24pt 正文）
- 仅白色背景上的黑色文本（没有视觉兴趣）
- 没有图像或图形（仅项目符号点）
- 没有任何内容的通用模板定制
- 密集的、段落式的要点
- 缺少研究背景（无引用）
- 所有幻灯片看起来都一样（重复）

✅ **什么使演示文稿引人入胜且令人难忘：**
- 高质量的视觉效果占主导地位（数字、照片、图表、图标）
- 大而清晰的文本作为强调（不是主要内容）
- 现代、有目的的配色方案（不是默认主题）
- 慷慨的空白（幻灯片呼吸）
- 研究支持的上下文（来自 research-lookup 的正确引用）
- 幻灯片布局的多样性（并非全部）项目符号列表）
- 具有视觉锚点的故事驱动流程
- 专业、精美的外观

* *核心设计原则**：

* *视觉优先方法**（关键）：
- 从视觉效果（图形、图像、图表）开始，添加文本作为支持
- 每张幻灯片都应具有强大的视觉效果元素（图形、图表、照片、图表）
- 文本解释或补充视觉效果，而不是取代它们
- 思考：“我如何展示这一点，而不仅仅是讲述它？”
- 目标：60-70% 视觉内容，30-40% 文本

* *简单且具有影响力**：
- 一个主要想法每张幻灯片
- 最小文本（3-4 个项目符号，每个优选 4-6 个单词）
- 大量空白（幻灯片的 40-50%）
- 清晰的视觉焦点
- 大胆、自信的设计选择

* *参与的版式**：
- 无衬线字体（Arial、Calibri、Helvetica）
- 大字体：正文文本为 24-28 磅（不小于 18 磅）
- 幻灯片标题为 36-44 磅（加粗）
- 高对比度（最小 4.5:1，首选 7:1）
- 使用尺寸来体现层次结构，而不仅仅是重量

* *影响颜色**：
- 现代调色板（不是默认的蓝色/灰色）
- 考虑您的主题：生物技术？充满活力的色彩。物理？光滑的深色。健康？暖色调。
- 有限的调色板（总共 3-5 种颜色）
- 高对比度组合
- 色盲安全（避免红绿组合）
- 有目的地使用颜色（不是装饰）

* *视觉兴趣布局**：
- 变化布局（并非所有项目符号列表）
- 使用两栏布局（文本+图形）
- 关键结果的完整幻灯片图形
- 不对称构图（比居中更有趣）
- 焦点的三分法则
- 一致但不重复

### 3.幻灯片的数据可视化

适应科学图形演示上下文。有关详细指导，请参阅 `references/data_visualization_slides.md`。

* *与期刊数据的主要区别**：
- 简化，不要复制
- 较大的字体（最小 18-24pt）
- 更少的面板（跨幻灯片分割）
- 直接标记（不是图例）
- 通过颜色和大小进行强调
- 复杂数据的渐进式披露

* *可视化最佳实践**：
- **条形图**：比较离散类别
- **折线图**：趋势和轨迹
- **散点图**：关系和相关性
- **热图**：矩阵数据和模式
- **网络图**：关系和连接

* *要避免的常见错误**：
- 微小字体（<18pt）
- 一张幻灯片上的面板太多
- 复杂图例
- 对比度不足
- 布局混乱

### 4. 特定演讲指导

不同的演示上下文需要不同的方法。有关每种类型的综合指导，请参阅 `references/talk_types_guide.md`.

* *会议演讲**（10-20 分钟）：
- 结构：简要介绍→最少方法→关键结果→快速结论
- 重点：仅 1-2 个主要发现
- 风格：参与、快节奏、令人难忘的
- 目标：产生兴趣、建立人际网络、获得邀请

* *学术研讨会**（45-60 分钟）：
- 结构：全面覆盖，详细方法
- 重点：多项发现，分析深度
- 风格：学术、互动、讨论导向
- 目标：展示专业知识、获取反馈、协作

* *论文答辩** (45-60分钟）：
- 结构：完整的论文概述，所有研究
- 重点：展示掌握和独立思考
- 风格：正式、全面、为审讯做好准备
- 目标：通过考试，捍卫研究决策

* * 资助推介**（10-20 分钟）：
- 结构：问题→ 意义 → 方法 → 可行性 → 影响
- 重点：创新、初步数据、团队资格
- 风格：有说服力，注重结果和影响
- 目标：确保资金、证明可行性

* *期刊俱乐部**（20-45 分钟）：
- 结构：背景→方法→结果→关键分析
- 重点：理解和批评已发表的作品
- 风格：教育性、批判性、促进讨论
- 目标：学习、批评、讨论影响

### 5. 实施选项

#### Nano Banana Pro PDF（默认 -推荐）

* *最适合**：视觉震撼的幻灯片、快速创建、非技术受众

* *这是默认和推荐的方法。**使用 AI 将每张幻灯片生成为完整图像。

* *工作流程**：
1. 规划每张幻灯片（标题、内容、视觉元素）
2. 使用 `generate_slide_image.py`
3 生成每张幻灯片。与 `slides_to_pdf.py`

```bash
# Generate slides
python scripts/generate_slide_image.py "Title: Introduction..." -o slides/01.png
python scripts/generate_slide_image.py "Title: Methods..." -o slides/02.png

# Combine to PDF
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf
```

 组合成 PDF**优点**：
- 最视觉上令人印象深刻的结果
- 快速创建（描述和生成）
- 无需设计技能
- 一致、专业外观
- 适合一般观众

* *最适合**：
- 会议演讲
- 商业演示
- 一般科学演讲
- 推介演示

#### 通过PPTX 进行PowerPoint 技能

* *最适合**：可编辑幻灯片、自定义设计、基于模板的工作流程

* *参考**：请参阅 `scientific-skills-zh/pptx/SKILL.md` 以获取完整文档

使用 Nano Banana Pro 和 `--visual-only` 生成图像，然后使用文本构建 PPTX。

* *关键资源**：
- `assets/powerpoint_design_guide.md`：完整的 PowerPoint 设计指南
- PPTX 技能的 `html2pptx.md`：程序化创建工作流程
- PPTX 技能的脚本：`rearrange.py`、`inventory.py`、`replace.py`、 `thumbnail.py`

* *工作流程**：
1. 使用 `generate_slide_image.py --visual-only`
2 生成视觉效果。设计 HTML 幻灯片（用于编程）或使用模板
3. 使用 html2pptx 或模板编辑
4 创建演示文稿。添加生成的图像和文本内容
5. 生成缩略图以进行视觉验证
6. 基于目视检查进行迭代

* *优点**：
- 可编辑幻灯片（稍后可以修改文本）
- 复杂的动画和过渡
- 交互元素
- 公司模板兼容性

#### LaTeX Beamer

* *最适合**：数学内容，一致的格式，版本控制

* *参考**：完整文档请参见`references/beamer_guide.md`

* *可用模板**：
- `assets/beamer_template_conference.tex`：15分钟的会议演讲
- `assets/beamer_template_seminar.tex`：45分钟的学术研讨会
- `assets/beamer_template_defense.tex`：论文答辩

* *工作流程**：
1. 选择合适的模板
2. 自定义主题和颜色
3. 添加内容（LaTeX 原生：方程、代码、算法）
4. 编译为 PDF
5. 转换为图像进行视觉验证

* *优点**：
- 美丽的数学和方程
- 一致、专业的外观
- 版本控制友好（纯文本）
- 非常适合算法和代码
- 可重现和编程

### 6. 视觉审查以及迭代

通过目视检查实施迭代改进。完整工作流程请参考`references/visual_review_workflow.md`.

* *视觉验证工作流程**：

* *步骤 1：生成 PDF**（如果还没有 PDF）
- PowerPoint：导出为 PDF
- Beamer：编译 LaTeX 源

* *步骤 2：转换为图像**
```bash
# Using the pdf_to_images script
python scripts/pdf_to_images.py presentation.pdf review/slide --dpi 150

# Or use pptx skill's thumbnail tool
python scientific-skills-zh/pptx/scripts/thumbnail.py presentation.pptx review/thumb
```

* *步骤 3：系统化检查**

检查每张幻灯片是否有：
- **文本溢出**：文本在边缘处被切断
- **元素重叠**：文本与图像或其他文本重叠
- **字体大小**：文本太小（<18pt）
- **对比度**：文本与背景之间对比度不足
- **布局问题**：错位、间距不佳
- **视觉质量**：像素化图像、渲染不佳

* *步骤 4：文档问题**

创建问题日志：
```
Slide # | Issue Type | Description | Priority
- -------|-----------|-------------|----------
3       | Text overflow | Bullet 4 extends beyond box | High
7       | Overlap | Figure overlaps with caption | High
12      | Font size | Axis labels too small | Medium
```

* *步骤 5：应用修复**

对源进行更正文件：
- PowerPoint：编辑文本框，调整元素大小
- Beamer：调整 LaTeX 代码，重新编译

* *步骤 6：重新验证**

 重复步骤 1-5，直到不再存在严重问题。

* *停止标准**：
- 无文本溢出
- 没有不适当的重叠
- 所有文本可读（≥18pt 等效）
- 足够的对比度（≥4.5:1）
- 专业外观

### 7. 时间和节奏

确保演示适合分配的时间。有关全面的计时指导，请参阅 `assets/timing_guidelines.md`。

* *每分钟一张幻灯片规则**：
- 一般指南：每分钟约 1 张幻灯片
- 复杂幻灯片调整（2-3 分钟）
- 简单幻灯片调整（15-30 秒）

* *时间分配**：
- 介绍：15-20%
- 方法：15-20%
- 结果：40-50%（大多数时间）
- 讨论：15-20%
- 结论：5%

* *实践要求**：
- 5分钟演讲：练习5-7次
- 15分钟演讲：练习3-5次
- 45分钟演讲：练习3-4次
- 防御：练习4-6次

* *计时检查点**：

For 15分钟演讲：
- 3-4分钟：结束介绍
- 7-8分钟：结果中途
- 12-13分钟：开始结论

* *紧急策略**：
- 落后：跳过备份幻灯片（提前准备）
- 领先：扩展示例，稍慢
- 永远不要跳过结论

### 8. 验证和质量保证

* *自动化验证**：
```bash
# Validate slide count, timing, file size
python scripts/validate_presentation.py presentation.pdf --duration 15

# Generates report on:
# - Slide count vs. recommended range
# - File size warnings
# - Slide dimensions
# - Font size issues (PowerPoint)
# - Compilation success (Beamer)
```

 * *手动验证清单**：
- [ ]适合持续时间的幻灯片计数
- [ ]幻灯片标题完整（姓名、所属单位、日期）
- [ ]清晰的叙述流程
- [ ]每个主要想法Slide
- [ ]字体大小 ≥18pt（最好是 24pt+）
- [ ]高对比度颜色
- [ ]图形大且可读
- [ ]无文本溢出或元素重叠
- [ ]始终保持一致的设计
- [ ]幻灯片编号present
- [ ]最终幻灯片上的联系信息
- [ ]准备好的备份幻灯片
- [ ]在投影仪上测试（如果可能）

## 演示文稿开发工作流程

### 第 1 阶段：规划（创建幻灯片之前）

* *定义上下文**：
1. 什么类型的谈话？ （会议、研讨会、答辩等）
2. 多长时间？ （持续时间以分钟为单位）
3. 观众是谁？ （专科、普通、混合）
4. 场地是什么？ （房间大小、A/V 设置、虚拟/现场）
5. 之后会发生什么？ （问答、讨论、交流）

* *研究与文献综述**（使用research-lookup技巧）：
1. **搜索背景文献**：查找 5-10 篇建立背景 
2 的关键论文。 **识别知识差距**：使用 research-lookup 查找未知内容 
3. **查找比较研究**：查找具有类似方法或结果的论文
4. **收集支持性引文**：收集支持您的解释的论文
5. **构建参考列表**：为幻灯片
6 创建.bib 文件或引文列表。 **注意要引用的关键发现**：记录具体结果以参考

* *制定内容大纲**：
1. 识别 1-3 个核心消息
2. 选择主要发现来展示 
3. 选择基本数字（对于 15 分钟的演讲，通常为 3-6 个）
4. 用适当的引文规划叙述弧
5. 按部分分配时间

* *15分钟演讲大纲示例**：
```
1. Title (30 sec)
2. Hook: Compelling problem (60 sec) [Cite 1-2 papers via research-lookup]
3. Background (90 sec) [Cite 3-4 key papers establishing context]
4. Research question (45 sec) [Cite papers showing gap]
5. Methods overview (2 min)
6-8. Main result 1 (3 min, 3 slides)
9-10. Main result 2 (2 min, 2 slides)
11-12. Result 3 or validation (2 min, 2 slides)
13-14. Discussion and implications (2 min) [Compare to 2-3 prior studies]
15. Conclusions (45 sec)
16. Acknowledgments (15 sec)

NOTE: Use research-lookup to find papers for background (slides 2-4) 
and discussion (slides 13-14) BEFORE creating slides.
```

### 阶段2：设计和创建

* *选择实施方法**：

* *选项A：PowerPoint（通过PPTX）技能）**
1. 读取 `assets/powerpoint_design_guide.md`
2. 读取 `scientific-skills-zh/pptx/SKILL.md`
3. 选择方法（编程或基于模板）
4. 创建具有一致设计的母版幻灯片
5. 按照大纲 

* *选项 B：LaTeX Beamer**
1 构建演示文稿。读取 `references/beamer_guide.md`
2. 从`assets/`
3中选择合适的模板。自定义主题和颜色
4. 在 LaTeX
5 中写入内容。编译为 PDF

* *设计注意事项**（使其具有视觉吸引力）：
- **选择现代调色板**：匹配您的主题（生物技术=充满活力，物理=时尚，健康=温暖）
  - 使用 pptx 技能的调色板示例（青色和珊瑚色，大胆红色，深紫色和祖母绿，等）
  - 不仅仅是默认的蓝色/灰色主题
  - 3-5种高对比度颜色
  - **选择干净的字体**：无衬线，大尺寸（24pt +正文）
  - **规划视觉元素**：每张幻灯片有哪些图像，图表，图标？
  - **创建不同的布局**：混合全图、两列、文本覆盖（并非全部项目符号）
- **设计部分分隔线**：用醒目的图形进行视觉破坏
- **规划动画/构建**：控制复杂幻灯片的信息流
- **添加视觉兴趣**：背景图像、色块、形状、图标

### 第 3 阶段：内容开发

* *填充幻灯片**（视觉优先策略）：
1. **从视觉效果开始**：为每个关键点规划哪些图形、图像、图表
2. **广泛使用 research-lookup**：查找 8-15 篇论文以进行正确引用
3. **首先创建视觉主干**：添加所有图形、图表、图像、图表
4. **添加最少的文本作为支持**：项目符号补充视觉效果，不要替换它们
5. **设计部分分隔线**：图像或图形（不仅仅是文本）
6 的视觉破坏。 **波兰语标题/结束语**：具有视觉冲击力，包括联系信息
7. **添加过渡/构建**：控制信息流

* *视觉内容要求**（使幻灯片引人入胜）：
- **图像**：使用高质量照片、插图、概念图形
- **图标**：概念的视觉表示（非装饰）
- **图表**：流程图、原理图、流程图表
- **数字**：带有大标签的简化研究图表（18-24pt）
- **图表**：带有清晰消息的清晰数据可视化
- **图形**：视觉隐喻、概念插图
- **色块**：使用彩色形状以视觉方式组织内容
- 目标：每张幻灯片至少有 1-2 个强烈的视觉元素

* *科学内容**（研究支持）：
- **引文**：广泛使用 research-lookup 查找相关论文
  - 简介：引用 3-5 篇论文建立背景和差距
  - 背景：以视觉方式显示关键的先前工作（不仅仅是引用）
  - 讨论：引用 3-5 篇论文与您的进行比较结果
  - 使用作者年份格式（Smith 等人，2023）以提高可读性
  - 引用建立可信度和科学严谨性
- **图**：从论文简化，大标签（最小 18-24 点）
- **方程**：大，清晰，解释每个术语（使用谨慎地）
- **表格**：最小，突出显示关键比较（不是数据转储）
- **代码/算法**：使用语法突出显示，保持简短

* *文本指南**（少即是多）：
- 要点，从不段落
- 每张幻灯片 3-4 个项目符号（最多 6 个）如果必要）
- 每个项目符号 4-6 个单词（短于 6×6 规则）
- 粗体关键术语
- 文本是支持角色，视觉效果是星星
- 使用构建来控制节奏

### 第 4 阶段：视觉验证

* *生成图片**：
```bash
# Convert PDF to images
python scripts/pdf_to_images.py presentation.pdf review/slides

# Or create thumbnail grid
python scientific-skills-zh/pptx/scripts/thumbnail.py presentation.pptx review/grid
```

* *系统审查**：
1. 查看每张幻灯片图像
2. 检查问题清单
3. 幻灯片编号 
4 的文档问题。从远处测试可读性（以 50% 大小查看）

* *需要修复的常见问题**：
- 文本超出边界
- 图形与文本重叠
- 字体太小
- 对比度较差
- 错位

* *迭代**：
1. 修复 source
2 中已发现的问题。重新生成 PDF/演示文稿
3. 再次转换为图像
4. 重新检查
5. 重复直到干净

### 阶段5：练习和精炼

* *练习时间表**：
- 运行1：粗稿（将运行很长时间）
- 运行2：平滑过渡
- 运行3：精确计时
- 运行4：决赛Polish
- 运行 5+：维护（前一天，早上）

* *练习内容**：
- 与计时器充分交谈
- 困难的解释
- 部分之间的转换
- 打开和关闭（直到完美）
- 预期问题

* * 基于实践的细化**：
- 如果运行则剪切幻灯片over
- 如果不清楚则展开解释
- 调整措辞以使其清晰
- 标记时间检查点
- 准备备份幻灯片

### 第六阶段：最终准备

* *技术检查**：
- []保存多个副本（笔记本电脑、云、 USB)
- [ ]适用于演示计算机
- [ ]提供适配器/电缆
- [ ]备份 PDF 版本
- [ ]使用投影仪进行测试（如果可能）

* *内容最终**：
- [ ]无拼写错误或错误
- [ ]所有数字高质量
- [ ]幻灯片编号正确
- [ ]最后幻灯片上的联系信息
- [ ]备份幻灯片准备好

  * *交付准备**：
- [ ]准备好的注释（如果使用）
- [ ]计时器/电话就绪
- [ ]可用水
- [ ]名片/讲义
- [ ]熟悉材料（3+种实践）

## 与其他技能的集成

* *研究查找**（对于科学演示至关重要）：
- **背景开发**：搜索文献构建介绍上下文
- **引文收集**：查找在演讲中引用的关键论文
- **差距识别**：识别未知的内容以激励研究
- **之前的工作比较**：查找论文以将您的结果与
- **支持证据**：找到支持您的解释的文献
- **问题准备**：查找可能为问答回复提供信息的论文
- **在开发任何科学演示时始终使用research-lookup**，以确保正确的上下文和引用

* *科学写作**：
- 将论文内容转换为演示文稿格式
- 提取关键发现并简化
- 使用相同的图形（但重新设计用于幻灯片）
- 保持术语一致

* *PPTX 技能**：
- 用于 PowerPoint 创建和编辑
- 利用脚本进行模板工作流程
- 使用缩略图生成进行验证
- 参考 html2pptx 用于编程创建

* *数据可视化**：
- 创建适合演示文稿的内容数字
- 简化复杂的可视化
- 确保从远处看的可读性
- 使用渐进式披露

## 要避免的常见陷阱

### 内容错误

* * 干燥、无聊的演示**（必须避免）：
- 问题：文本过多没有视觉兴趣的幻灯片，缺少研究背景
- 标志：所有要点，没有图像，默认模板，没有引用
- 解决方案：
- 使用research-lookup找到8-15篇可信背景的论文
- 向每张幻灯片添加高质量的视觉效果（图形，照片，图表，图标）
  - 选择反映您主题的现代调色板
  - 改变幻灯片布局（并非所有项目符号列表）
  - 用视觉效果讲故事，谨慎使用文本

  * *内容太多**：
  - 问题：尝试包含纸质内容
  - 解决方案：重点关注 1-2 个关键发现简短的演讲，直观地展示

* *文本太多**：
- 问题：幻灯片上的完整段落，密集的要点，逐字阅读
- 解决方案：3-4个项目符号，每个项目符号4-6个单词，让视觉效果传达信息

* *缺少研究背景**：
- 问题：没有引用，没有声明支持，定位不明确
- 解决方案：使用research-lookup查找论文，在介绍中引用3-5，在讨论中引用3-5

* *叙事不佳**：
- 问题：在主题之间跳转，没有清晰的故事，没有流程
- 解决方案：遵循故事弧，使用视觉过渡，维护线程

* *冲破结果**：
- 问题：简短的方法，简短的结果，长时间的讨论
- 解决方案：花费40-50%的时间在结果上，直观地显示数据

### 设计错误

* *通用，默认外观**：
- 问题：使用默认的 PowerPoint/Beamer 主题，无需自定义，看起来过时
- 解决方案：选择现代调色板，自定义字体/布局，添加视觉个性

* *文本重，视觉效果差**：
- 问题：所有要点幻灯片，没有图像或图形，看起来很无聊at
- 解决方案：在每张幻灯片中添加图形、照片、图表、图标，使视觉上变得有趣

* *小字体**：
- 问题：正文 <18pt，从后面看不懂，看起来不专业
- 解决方案：正文 24-28pt（不仅仅是最低 18pt），36-44pt标题

* *低对比度**：
- 问题：浅色背景上的浅文本，可见性差，难以阅读
- 解决方案：高对比度（首选7:1，不仅仅是4.5:1最低），使用对比度检查器进行测试

* *杂乱的幻灯片**：
- 问题：元素太多，没有空白，压倒性的
- 解决方案：每张幻灯片一个想法，40-50%的空白，宽敞的间距

* *格式不一致**：
- 问题：幻灯片之间的字体、颜色、布局不同，看起来很业余
- 解决方案：使用主幻灯片，维护设计系统，专业一致性

* *视觉缺失层次结构**：
- 问题：一切大小和颜色相同，没有重点，焦点不清晰
- 解决方案：大小差异（标题大，正文中），强调颜色，焦点清晰

### 时间错误

* *不练习**：
- 问题：第一次通过是在演示
- 解决方案：用定时器练习至少3次

* *没有时间检查点**：
- 问题：直到太晚才意识到落后
- 解决方案：设置3-4个检查点，全程监控

* *超时**：
- 问题：非常不专业，削减进入Q&A
- 解决方案：练习精确时间，准备B计划（幻灯片可跳过）

* *跳过结论**：
- 问题：时间不够，匆忙完成或跳过结局
- 解决方案：永远不要跳过结论，而是剪切前面的内容

## 工具和脚本

### Nano Banana Pro 脚本

* *generate_slide_image.py** - 生成幻灯片或视觉效果AI:
```bash
# Full slide (for PDF workflow)
python scripts/generate_slide_image.py "Title: Introduction\nContent: Key points" -o slide.png

# Visual only (for PPT workflow)
python scripts/generate_slide_image.py "Diagram description" -o figure.png --visual-only

# Options:
# -o, --output       Output file path (required)
# --visual-only      Generate just the visual, not complete slide
# --iterations N     Max refinement iterations (default: 2)
# -v, --verbose      Verbose output
```

* *slides_to_pdf.py** - 将幻灯片图像合并到 PDF:
```bash
# From glob pattern
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf

# From directory (sorted by filename)
python scripts/slides_to_pdf.py slides/ -o presentation.pdf

# Options:
# -o, --output    Output PDF path (required)
# --dpi N         PDF resolution (default: 150)
# -v, --verbose   Verbose output
```

### 验证脚本

* *validate_presentation.py**:
```bash
python scripts/validate_presentation.py presentation.pdf --duration 15

# Checks:
# - Slide count vs. recommended range
# - File size warnings
# - Slide dimensions
# - Font sizes (PowerPoint)
# - Compilation (Beamer)
```

* *pdf_to_images.py**:
```bash
python scripts/pdf_to_images.py presentation.pdf output/slide --dpi 150

# Converts PDF to images for visual inspection
# Supports: JPG, PNG
# Adjustable DPI
# Page range selection
```

### PPTX技能脚本

From `scientific-skills-zh/pptx/scripts/`:
- `thumbnail.py`：创建缩略图网格
- `rearrange.py`：复制幻灯片并重新排序
- `inventory.py`：提取文本内容
- `replace.py`：更新文本以编程方式

### 外部工具

* *推荐**：
- PDF 查看器：用于审阅演示文稿
- 颜色对比度检查器：WebAIM 对比度检查器
- 色盲模拟器：Coblis
- 计时器应用程序：用于练习会话
- 屏幕录像机：用于自我审查

## 参考文件

特定方面的综合指南：

- **`references/presentation_structure.md`**：所有谈话类型的详细结构、时间分配、开/关策略、过渡技术
- **`references/slide_design_principles.md`**：版式、颜色理论、布局、可访问性、视觉层次结构、设计工作流程
- **`references/data_visualization_slides.md`**：简化图形、图表类型、渐进式披露、常见错误、娱乐工作流程
- **`references/talk_types_guide.md`**：针对会议、研讨会、答辩、资助、期刊俱乐部的具体指导，并附示例
- **`references/beamer_guide.md`**：完整LaTeX Beamer 文档、主题、定制、高级功能、编译
- **`references/visual_review_workflow.md`**：PDF 到图像转换、系统检查、问题文档、迭代改进

## 资产

### 模板

- **`assets/beamer_template_conference.tex`**：15分钟会议演讲模板
- **`assets/beamer_template_seminar.tex`**：45分钟学术研讨会模板
- **`assets/beamer_template_defense.tex`**：论文答辩模板

### 指南

- **`assets/powerpoint_design_guide.md`**：完整的PowerPoint设计和实施指南
- **`assets/timing_guidelines.md`**：综合计时、节奏和练习策略

## 快速入门指南

### 用于15分钟的会议演讲（PDF工作流程 - 推荐）

1. **研究与计划**（45 分钟）：
  - **使用 research-lookup** 查找 8-12 篇相关论文进行引用
  - 构建参考列表（背景、比较研究）
  - 概述内容（简介 → 方法 → 2-3 个关键结果 → 结论）
  - **为每张幻灯片创建详细计划**（标题、要点、视觉元素）
  - 目标 15-18 张幻灯片

2. **使用 Nano Banana Pro 生成幻灯片**（1-2 小时）：
 
  * *重要：使用一致的格式，附加以前的幻灯片，并包含引用！**
 
 ```bash
 # 幻灯片标题（建立样式 - 默认作者：K-Dense）
python script/generate_slide_image.py “标题幻灯片：‘您的研究标题’。会议名称，K-Dense。格式目标：[您的配色方案]，简约的专业设计，无装饰元素，干净且企业化。” -o Slides/01_title.png
 
 # 带引文的介绍幻灯片（为了保持一致性，附上之前的内容）
python script/generate_slide_image.py "标题为“为什么这很重要”的幻灯片。带有简单图标的三个关键点。引文：包括在底部：（Smith 等人，2023 年；Jones 等人，2024 年）。格式设置目标：完全匹配附加的幻灯片样式。” -o Slides/02_intro.png --attach slips/01_title.png
 
 # 继续每张幻灯片（始终附加上一张幻灯片，包括相关的引用）
python script/generate_slide_image.py "标题为“方法”的幻灯片。关键方法论点。引文：（基于 Chen 等人，2022 年）。格式设置目标：完全匹配附加的幻灯片样式。” -o幻灯片/03_methods.png --attach幻灯片/02_intro.png
 
 # 合并为PDF
python脚本/slides_to_pdf.py幻灯片/*.png -o演示文稿.pdf
``

3. **审阅和迭代**（30 分钟）：
  - 打开 PDF 并审阅每张幻灯片
  - 重新生成任何需要改进的幻灯片
  - 重新组合为 PDF

4. **练习**（2-3小时）：
  - 使用计时器练习3-5次
  - 目标为13-14分钟（留出缓冲区）
  - 自己录音，观看回放
  - **准备问题**（使用research-lookup来预测）

5. **最终确定**（30 分钟）：
  - 如果需要，生成备份/附录幻灯片
  - 保存多个副本
  - 在演示计算机上测试

总时间：约 5-6 小时人工智能生成的高质量演示文稿

### 替代方案：PowerPoint 工作流程

如果您需要可编辑幻灯片（例如，用于公司模板）：

1. **计划幻灯片**如上
2. **使用 `--visual-only` 标志生成视觉效果**：
 ```bash
 python script/generate_slide_image.py "图表描述" -ofigures/fig1.png --visual-only
 ```
3. **使用 PPTX 技能和生成的图像 
4 构建 PPTX**。 **使用 PPTX 工作流程单独添加文本**

有关完整的 PowerPoint 工作流程，请参阅 `scientific-skills-zh/pptx/SKILL.md`。

## 摘要：关键原则

1. **视觉优先设计**：每张幻灯片都需要强大的视觉元素（图形、图像、图表） - 避免纯文本幻灯片
2. **研究支持**：使用 research-lookup 查找 8-15 篇论文，在介绍中引用 3-5 篇论文，在讨论中引用 3-5 篇论文
3. **现代美学**：选择当代调色板匹配主题，而不是默认主题
4. **最小文本**：3-4 个项目符号，每个项目符号 4-6 个单词（24-28pt 字体），让视觉效果讲述故事
5. **结构**：跟随故事情节，在结果上花费 40-50%
6. **高对比度**：专业外观首选 7:1
7. **多种布局**：混合全图、两列、视觉叠加（并非所有项目符号）
8. **计时**：练习 3-5 次，每分钟约 1 张幻灯片，切勿跳过结论
9. **验证**：目视检查工作流程以捕获溢出和重叠
10. **留白**：40-50% 的幻灯片留有视觉呼吸空间

* *记住**：
- **无聊 = 被遗忘**：枯燥、文字较多的幻灯片无法传达您的科学知识
- **视觉 + 研究 = 影响力**：将引人注目的视觉效果与研究支持的背景相结合
- **您是演示文稿，幻灯片是视觉支持**：它们应该增强而不是取代你的谈话
