---
name: pptx-posters
description: 使用 HTML/CSS 创建可导出到 PDF 或 PPTX 的研究海报。仅当用户明确请求 PowerPoint/PPTX 海报格式时才使用此技能。对于标准研究海报，请改用 latex-posters。这项技能提供了具有响应式布局和轻松视觉集成的现代基于网络的海报设计。
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# PPTX 研究海报（基于 HTML）

## 概述

* *⚠️ 仅当用户明确请求 PPTX/POWERPOINT 海报格式时才使用此技能。**

 对于标准研究海报，请使用 **latex-posters** 技能，该技能提供更好的排版控制，是学术会议的默认设置。

此技能使用 HTML/CSS 创建研究海报，然后可以将其导出到 PDF 或转换为 PowerPoint 格式。基于网络的方法提供：
- 现代、响应式布局
- 轻松集成人工智能生成的视觉效果
- 在浏览器中快速迭代和预览
- 通过浏览器打印功能导出到PDF
- 如果特别需要则转换为PPTX

## 何时使用此技能

* *仅在以下情况下使用此技能：**
- 用户明确请求“PPTX 海报”、“PowerPoint 海报”或“PPT 海报”
- 用户特别请求基于 HTML 的海报
- 用户需要在创建后在 PowerPoint 中编辑海报
- LaTeX 不可用或用户请求非 LaTeX解决方案

* *不要在以下情况下使用此技能：**
- 用户请求“海报”但未指定格式 → 使用 Latex-posters
- 用户请求“研究海报”或“会议海报”→ 使用 Latex-海报
- 用户提及 LaTeX、tikzposter、beamerposter 或 baposter → 使用Latex-posters

## AI 驱动的视觉元素生成

* *标准工作流程：在创建 HTML 海报之前使用 AI 生成所有主要视觉元素。**

这是创建视觉上引人注目的海报的推荐方法：
1. 规划所需的所有视觉元素（英雄图像、简介、方法、结果、结论）
2. 使用 scientific-schematics 或 Nano Banana Pro
3 生成每个元素。在 HTML 模板
4 中组装生成的图像。在视觉效果周围添加文本内容

* *目标：海报区域的60-70%应该是AI生成的视觉效果，30-40%是文本。**

- --

### 关键：海报大小字体要求

* *⚠️ AI 生成的可视化中的所有文本必须是海报可读的。**

 生成海报图形时，您必须在每个提示中包含字体大小规范。海报图形是从 4-6 英尺远处观看的，因此文本必须很大。

* *每个海报图形的强制提示要求：**

```
POSTER FORMAT REQUIREMENTS (STRICTLY ENFORCE):
- ABSOLUTE MAXIMUM 3-4 elements per graphic (3 is ideal)
- ABSOLUTE MAXIMUM 10 words total in the entire graphic
- NO complex workflows with 5+ steps (split into 2-3 simple graphics instead)
- NO multi-level nested diagrams (flatten to single level)
- NO case studies with multiple sub-sections (one key point per case)
- ALL text GIANT BOLD (80pt+ for labels, 120pt+ for key numbers)
- High contrast ONLY (dark on white OR white on dark, NO gradients with text)
- MANDATORY 50% white space minimum (half the graphic should be empty)
- Thick lines only (5px+ minimum), large icons (200px+ minimum)
- ONE SINGLE MESSAGE per graphic (not 3 related messages)
```

* *⚠️ 生成之前：检查您的提示并计算元素**
- 如果您的描述有 5 个以上项目 → 停止。拆分为多个图形
  - 如果您的工作流程有 5 个以上阶段 → 停止。仅显示 3-4 个高级步骤
- 如果您的比较有 4 个以上方法 → 停止。仅显示前 3 个或我们与最佳基线

* *示例 - 错误（7 阶段工作流程）：**
```bash
# ❌ Creates tiny unreadable text
python scripts/generate_schematic.py "Drug discovery workflow: Stage 1 Target ID, Stage 2 Synthesis, Stage 3 Screening, Stage 4 Lead Opt, Stage 5 Validation, Stage 6 Clinical Trial, Stage 7 FDA Approval with metrics." -o figures/workflow.png
```

 * *示例 - 正确（3 个大型阶段）：**
```bash
# ✅ Same content, simplified to readable poster format
python scripts/generate_schematic.py "POSTER FORMAT for A0. ULTRA-SIMPLE 3-box workflow: 'DISCOVER' → 'VALIDATE' → 'APPROVE'. Each word in GIANT bold (120pt+). Thick arrows (10px). 60% white space. ONLY these 3 words. NO substeps. Readable from 12 feet." -o figures/workflow_simple.png
```

- --

### 重要：防止内容溢出

* *⚠️ 海报不得在边缘截断文本或内容。**

* *预防规则：**

* *1。限制内容部分（最多 5-6 个部分）：**
```
✅ GOOD - 5 sections with room to breathe:
   - Title/Header
   - Introduction/Problem
   - Methods
   - Results (1-2 key findings)
   - Conclusions

❌ BAD - 8+ sections crammed together
```

* *2。字数限制：**
- **每节**：最多 50-100 个字
- **海报总数**：最多 300-800 个字 
- **如果您有更多内容**：剪切或制作讲义

- --

## 核心功能

### 1. HTML/CSS 海报设计

HTML 模板（`assets/poster_html_template.html`）提供：
- 固定海报尺寸（36×48 英寸 = 2592×3456 pt）
- 具有渐变样式的专业标题
- 三列内容布局
- 具有现代风格的基于块的部分
- 带有参考和联系信息的页脚

### 2.海报结构

* *标准布局：**
```
┌─────────────────────────────────────────┐
│  HEADER: Title, Authors, Hero Image     │
├─────────────┬─────────────┬─────────────┤
│ Introduction│   Results   │  Discussion │
│             │             │             │
│   Methods   │   (charts)  │ Conclusions │
│             │             │             │
│  (diagram)  │   (data)    │   (summary) │
├─────────────┴─────────────┴─────────────┤
│  FOOTER: References & Contact Info      │
└─────────────────────────────────────────┘
```

### 3.视觉集成

每个部分应突出显示AI 生成的视觉效果：

* *英雄图片（标题）：**
```html
<img src="figures/hero.png" class="hero-image">
```

* *部分图形：**
```html
<div class="block">
  <h2 class="block-title">Methods</h2>
  <div class="block-content">
    <img src="figures/workflow.png" class="block-image">
    <ul>
      <li>Brief methodology point</li>
    </ul>
  </div>
</div>
```

### 4. 生成视觉元素

* *在创建 HTML 之前，生成所有视觉元素元素：**

```bash
# Create figures directory
mkdir -p figures

# Hero image - SIMPLE, impactful
python scripts/generate_schematic.py "POSTER FORMAT for A0. Hero banner: '[TOPIC]' in HUGE text (120pt+). Dark blue gradient background. ONE iconic visual. Minimal text. Readable from 15 feet." -o figures/hero.png

# Introduction visual - ONLY 3 elements
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE visual with ONLY 3 icons: [icon1] → [icon2] → [icon3]. ONE word labels (80pt+). 50% white space. Readable from 8 feet." -o figures/intro.png

# Methods flowchart - ONLY 4 steps
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE flowchart with ONLY 4 boxes: STEP1 → STEP2 → STEP3 → STEP4. GIANT labels (100pt+). Thick arrows. 50% white space. NO sub-steps." -o figures/workflow.png

# Results visualization - ONLY 3 bars
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE bar chart with ONLY 3 bars: BASELINE (70%), EXISTING (85%), OURS (95%). GIANT percentages ON bars (120pt+). NO axis, NO legend. 50% white space." -o figures/results.png

# Conclusions - EXACTLY 3 key findings
python scripts/generate_schematic.py "POSTER FORMAT for A0. EXACTLY 3 cards: '95%' (150pt) 'ACCURACY' (60pt), '2X' (150pt) 'FASTER' (60pt), checkmark 'READY' (60pt). 50% white space. NO other text." -o figures/conclusions.png
```

- --

## PPTX 海报创建的工作流程

### 第 1 阶段：规划

1. **确认明确请求 PPTX**
2. **确定海报要求：**
  - 尺寸：36×48 英寸（最常见）或 A0
  - 方向：纵向（最常见）
3. **制定内容大纲：**
  - 确定 1-3 条核心信息
  - 规划 3-5 个视觉元素
  - 起草最小文本（总共 300-800 个字）

### 第 2 阶段：生成视觉元素（AI 驱动）

 * *关键：使用 MINIMAL 生成简单的图形内容。**

```bash
mkdir -p figures

# Generate each element with POSTER FORMAT specifications
# (See examples in Section 4 above)
```

### 第 3 阶段：创建 HTML 海报

1. **复制模板：**
 ```bash
 cp Skills/pptx-posters/assets/poster_html_template.html poster.html
 ```

2. **更新内容：**
  - 替换占位符标题和作者
  - 插入AI生成的图像
  - 添加最少的支持文本
  - 更新参考和联系信息

3. **在浏览器中预览：**
 ```bash
 open poster.html # macOS
 # or
xdg-open poster.html # Linux
 ```

### 第 4 阶段：导出为 PDF

* *浏览器打印方法：**
1. 在 Chrome 或 Firefox
2 中打开 poster.html。打印（Cmd/Ctrl + P）
3. 选择“另存为PDF”
4. 设置纸张尺寸以匹配海报尺寸
5. 删除边距
6. 启用“背景图形”

* *命令行（如果 Chrome 可用）：**
```bash
# Chrome headless PDF export
google-chrome --headless --print-to-pdf=poster.pdf \
  --print-to-pdf-no-header \
  --no-margins \
  poster.html
```

### 第 5 阶段：转换为 PPTX（如果需要）

* *选项 1：PDF 到 PPTX转换**
```bash
# Using LibreOffice
libreoffice --headless --convert-to pptx poster.pdf

# Or use online converters for simple cases
```

* *选项2：使用python-pptx直接创建PPTX**
```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
prs.slide_width = Inches(48)
prs.slide_height = Inches(36)

slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

# Add images from figures/
slide.shapes.add_picture("figures/hero.png", Inches(0), Inches(0), width=Inches(48))
# ... add other elements

prs.save("poster.pptx")
```

- --

## HTML模板结构

提供的模板(`assets/poster_html_template.html`)包括：

### 用于自定义的 CSS 变量

```css
/* Poster dimensions */
body {
  width: 2592pt;   /* 36 inches */
  height: 3456pt;  /* 48 inches */
}

/* Color scheme - customize these */
.header {
  background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 50%, #3182ce 100%);
}

/* Typography */
.poster-title { font-size: 108pt; }
.authors { font-size: 48pt; }
.block-title { font-size: 52pt; }
.block-content { font-size: 34pt; }
```

### 关键类

|班级 |目的|字体大小 |
|--------|---------|-----------|
| `.poster-title` |主标题| 108pt |
| `.authors` |作者姓名 | 48点|
| `.affiliations` |机构 | 38点|
| `.block-title` |节标题 | 52点|
| `.block-content` |正文 | 34点|
| `.key-finding` |突出显示框 | 36pt |

- --

## 质量检查表

### 步骤 0：生成前审核（强制）

* *对于每个计划图形，验证：**
- [ ]可以用 3-4 项或更少的内容进行描述？ （不是 5+）
- [ ]这是一个简单的工作流程（3-4 个步骤，而不是 7+）？
- [ ]可以用 10 个字或更少的文字描述所有文本吗？
- [ ]它传达一条消息（不是多个）吗？

* *拒绝这些模式：**
- ❌ “7阶段工作流程”→简化为“3个大型阶段”
- ❌“多个案例研究”→每个图形一个案例
- ❌“2015-2024年度时间表”→“只有3个关键年”
- ❌“比较6种方法”→“只有2：我们的与best"

### 步骤 2b：生成后审核（强制）

* *对于每个生成的 25% 缩放图：**

* *✅ 通过标准（全部必须为真）：**
- [ ]可以清楚地阅读所有文本
- [ ]计数：3-4 个元素或less
- [ ]空白：50%+ 空
- [ ] 2 秒内理解
- [ ]不是复杂的 5+ 阶段工作流程
- [ ]不是多个嵌套部分

* *❌ 失败标准（如果有的话重新生成）：**
- [ ]文本小/难以阅读 → 重新生成“150pt+”
- [ ]超过 4 个元素 → 重新生成“仅 3 个元素”
- [ ]小于 50% 空白 → 重新生成“60% 空白”
- [ ]复杂多级 → 分割为 2-3图形
- [ ]多个案例狭窄 → 分割成单独的图形

### 导出后

- [ ] 4 个边缘中的任何一个都没有内容被切断（仔细检查）
- [ ]所有图像正确显示
- [ ]颜色按预期渲染
- [ ]文本可读25% 比例
- [ ]图形看起来很简单（不像复杂的 7 阶段工作流程）

- --

## 要避免的常见陷阱

* *AI 生成的图形错误：**
- ❌ 元素过多（10+ 项）→ 最多保持 3-5 
- ❌ 文本太小 → 在提示中指定“GIANT (100pt+)”
- ❌ 无空白 → 添加“50% 空白”每个提示
- ❌ 复杂流程图（8 个以上步骤） → 限制为 4-5 个步骤

* *HTML/导出错误：**
- ❌ 内容超出海报尺寸 → 检查浏览器中的溢出
- ❌ PDF 中缺少背景图形 → 在打印设置中启用
- ❌ 错误PDF 中的纸张尺寸 → 完全匹配海报尺寸
- ❌ 低分辨率图像 → 使用最低 300 DPI

* *内容错误：**
- ❌ 文本太多（超过 1000 个单词） → 剪切为 300-800 个单词
- ❌ 章节太多 (7+) → 合并为 5-6
- ❌ 没有清晰的视觉层次 → 突出关键发现

- --

## 与其他技能集成

此技能适用于：
- **科学原理图**：生成所有海报图和流程图
- **生成图像/纳米香蕉Pro**：创建风格化图形和英雄图像
- **LaTeX 海报**：海报创建的默认技能（除非 PPTX 明确要求，否则使用此技能）

- --

## 模板资源

在 `assets/` 目录中可用：

- `poster_html_template.html`：主要HTML海报模板（36×48英寸）
- `poster_quality_checklist.md`：提交前验证清单

## 参考文献

可在`references/`目录中找到：

- `poster_content_guide.md`：内容组织和写作指南
- `poster_design_principles.md`：版式、色彩理论和视觉层次
- `poster_layout_design.md`：布局原则和网格系统
