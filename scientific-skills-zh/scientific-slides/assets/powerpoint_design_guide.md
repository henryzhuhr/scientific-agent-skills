# 科学演示文稿的 PowerPoint 设计指南

## 概述

本指南提供了使用 PowerPoint 创建专业科学演示文稿的全面说明，重点是与 ZX​​QTERM1QXZ 技能集成以进行程序化创建和科学内容的最佳实践。

* *关键**：避免枯燥、文本较多的演示文稿。科学幻灯片应该是：
- **视觉吸引力**：每张幻灯片上都有高质量的图像、图形、图表
- **研究支持**：引用research-lookup以提高可信度（最少8-15篇论文）
- **现代设计**：现代调色板，而不是默认主题
- **最小文本**：3-4每个项目符号有 4-6 个单词，视觉效果会说话
- **专业润色**：一致但多样的布局，宽敞的空白

* *反模式警告**：白色背景上黑色文本的全项目符号幻灯片 = 立即无聊和被遗忘的科学。

## 使用 PPTX 技能

### 参考

有关PowerPoint创建的完整技术文档，请参考：
- **主要文档**：`document-skills/pptx/SKILL.md`
- **HTML到PowerPoint工作流程**：详细参见`pptx/html2pptx.md`
- **OOXML编辑**：用于`pptx/ooxml.md`

### 中的高级编辑二PowerPoint 创建方法

#### 1. 程序化创建 (html2pptx)

* *最适合**：使用自定义设计和数据可视化从头开始创建演示文稿。

* *工作流程**：
1. 完整读取`document-skills/pptx/SKILL.md`
2. 以 HTML 格式设计具有适当尺寸的幻灯片（16:9 为 720pt × 405pt）
3. 使用`html2pptx()`函数
4创建JavaScript文件。使用 PptxGenJS API
5 添加图表和表格。生成缩略图并进行视觉验证
6. 基于目视检查进行迭代

* *示例结构**：
```javascript
const pptx = new PptxGenJS();

// Add title slide
const slide1 = pptx.addSlide();
slide1.addText("Your Title", {
  x: 1, y: 2, w: 8, h: 1,
  fontSize: 44, bold: true, align: "center"
});

// Add content slide with figure
const slide2 = pptx.addSlide();
slide2.addText("Results", { x: 0.5, y: 0.5, fontSize: 32 });
slide2.addImage({ path: "figure.png", x: 1, y: 1.5, w: 8, h: 4 });

pptx.writeFile({ fileName: "presentation.pptx" });
```

#### 2.基于模板的创建

* *最适合**：使用现有的 PowerPoint 模板或编辑现有的演示文稿。

* *工作流程**：
1. 从 template.pptx
2 开始。使用 `scripts/rearrange.py` 复制/重新排序幻灯片 
3. 使用`scripts/inventory.py`提取文本
4. 生成替换文本 JSON
5. 使用`scripts/replace.py`更新内容
6. 使用缩略图网格进行验证

* *关键脚本**：
- `rearrange.py`：复制和重新排序幻灯片
- `inventory.py`：提取所有文本形状
- `replace.py`：应用文本替换
- `thumbnail.py`：视觉验证

## 科学演示的设计原则

### 1.布局和结构

* *幻灯片母版设置**：
- 创建一致的母版幻灯片
- 定义4-5种布局类型（标题、内容、图形、两栏、关闭）
- 设置默认字体、颜色和间距
- 包括徽标和页脚的占位符

* *标准布局**：

* *标题幻灯片**：
```
┌─────────────────────────┐
│                         │
│   Presentation Title    │
│   Your Name             │
│   Institution           │
│   Date / Conference     │
│                         │
└─────────────────────────┘
```

* *内容幻灯片**：
```
┌─────────────────────────┐
│ Slide Title             │
├─────────────────────────┤
│ • Bullet point 1        │
│ • Bullet point 2        │
│ • Bullet point 3        │
│                         │
│ [Optional figure]       │
└─────────────────────────┘
```

* *两柱幻灯片**：
```
┌─────────────────────────┐
│ Slide Title             │
├───────────┬─────────────┤
│           │             │
│  Text     │   Figure    │
│  Content  │   or        │
│           │   Data      │
└───────────┴─────────────┘
```

* *全图幻灯片**：
```
┌─────────────────────────┐
│ Figure Title (small)    │
├─────────────────────────┤
│                         │
│    Large Figure or      │
│    Visualization        │
│                         │
└─────────────────────────┘
```

### 2.版式

* *字体选择**：
- **主要**：无衬线字体（Arial、Calibri、Helvetica）
- **替代**：Verdana、Tahoma、Trebuchet MS
- **避免**：衬线字体（在屏幕上难以阅读）、装饰性字体

* *字体大小**：
- 幻灯片标题：44-54pt
- 幻灯片标题：32-40pt
- 正文：24-28pt（最小 18pt）
- 说明文字： 16-20pt
- 页脚：10-12pt

* *文本格式**：
- **粗体**：用于强调（谨慎使用）
- **颜色**：用于突出显示（一致的含义）
- **大小**：用于层次结构
- **对齐**：正文靠左，标题居中

* *6×6 规则**：
- 每张幻灯片最多 6 个项目符号点
- 每个项目符号最多 6 个单词
- 更好：3-4 个项目符号，每个项目符号 4-8 个单词

### 3. 配色方案

* *选择颜色**：

考虑您的主题和受众：
- **学术/专业**：海军蓝、灰色、白色，带有最小的口音
- **生物医学**：蓝色和绿色色调（避免红绿组合）
- **技术**：现代颜色（青色、橙色、紫色）
- **临床**：保守（蓝色、灰色、柔和）绿色）

* *示例调色板**：

* *经典科学**：
- 背景：白色 (#FFFFFF)
- 标题：海军蓝 (#1C3D5A)
- 文本：深灰色 (#2D3748)
- 口音：橙色(#E67E22)

* *现代研究**：
- 背景：浅灰色 (#F7FAFC)
- 标题：青色 (#0A9396)
- 文本：木炭色 (#2C2C2C)
- 口音：珊瑚色(#EE6C4D)

* *高对比度**（适用于大型场地）：
- 背景：白色 (#FFFFFF)
- 标题：黑色 (#000000)
- 文本：深灰色 (#1A1A1A)
- 强调色：亮蓝色(#0066CC)

* *辅助功能指南**：
- 最小对比度：4.5:1（正文）
- 首选对比度：7:1（AAA 标准）
- 避免红绿组合（8% 的男性是色盲）
- 除颜色外还使用图案或形状数据

### 4. 视觉元素

* *图形和图像**：
- **分辨率**：打印最小 300 DPI，投影 150 DPI
- **格式**：用于屏幕截图的 PNG，用于矢量图形的 PDF/SVG
- **大小**：足够大，可以从背面读取room
- **放置**：居中或使用两栏布局

* *数据可视化**：
- **从日志数字简化**（更少的面板，更大的文本）
- **字体大小**：轴标签为18-24pt
- **线宽**：2-4pt厚度
- **颜色**：高对比度，色盲安全
- **标签**：直接标记优先于图例

* *图标和形状**：
- 用于视觉兴趣和组织
- 一致的风格（全部轮廓或全部填充）
- 尺寸适当（不要太大或太大）小）
- 限制颜色（匹配主题）

### 5.动画和过渡

* *何时使用**：
- ✅ 逐步披露要点
- ✅ 逐步构建复杂的图形
- ✅ 强调关键发现
- ✅ 显示流程步骤

* *何时避免**：
- ❌ 装饰或娱乐
- ❌ 每一个幻灯片
- ❌ 分散注意力的效果（飞入、弹跳、旋转）

* *推荐动画**：
- **出现**：干净、专业
- **淡入淡出**：微妙过渡
- **擦拭**：定向显示
- **持续时间**：快速（0.2-0.3 秒）
- **触发**：单击时（非自动）

* *幻灯片过渡**：
- 在整个过程中使用一致的过渡（或无）
- 推荐：无、淡入淡出或推送
- 避免：3D 旋转、复杂效果
- 持续时间：非常快速（0.3-0.5 秒）

## 使用 PPTX 技能创建演示文稿

### 设计优先工作流程

* *步骤 0：根据主题选择现代调色板**

* *关键**：选择反映主题的颜色，而不是通用默认值。

* *基于主题调色板示例：**
- **生物技术/生命科学**：青色 (#0A9396)、珊瑚色 (#EE6C4D)、奶油色 (#F4F1DE)
- **神经科学/脑研究**：深紫色 (#722880)、洋红色 (#D72D51)、白色
- **机器学习/AI**：粗红色 (#E74C3C)、橙色 (#F39C12)、深灰色 (#2C2C2C)
- **物理/工程**：海军蓝 (#1C3D5A)、橙色 (#E67E22)、浅灰色 (#F7FAFC)
- **医学/保健**：青色(#5EA8A7)、珊瑚色 (#FE4447)、白色 (#FFFFFF)
- **环境科学**：鼠尾草 (#87A96B)、赤土陶土 (#E07A5F)、奶油色 (#F4F1DE)

在 pptx 技能 SKILL.md 中查看完整调色板选项（行76-94).

* *步骤 1：规划设计系统**（使用现代调色板）
```javascript
// Define design constants with MODERN colors (not defaults)
const DESIGN = {
  colors: {
    primary: "0A9396",    // Teal (modern, engaging)
    accent: "EE6C4D",     // Coral (attention-grabbing)
    text: "2C2C2C",       // Charcoal (readable)
    background: "FFFFFF"  // White (clean)
  },
  fonts: {
    title: { size: 40, bold: true, face: "Arial" },
    heading: { size: 28, bold: true, face: "Arial" },
    body: { size: 24, face: "Arial" },
    caption: { size: 16, face: "Arial" }
  },
  layout: {
    margin: 0.5,
    titleY: 0.5,
    contentY: 1.5
  }
};
```

* *步骤 2：创建可重用函数**
```javascript
function addTitleSlide(pptx, title, subtitle, author) {
  const slide = pptx.addSlide();
  slide.background = { color: DESIGN.colors.primary };
  
  slide.addText(title, {
    x: 1, y: 2, w: 8, h: 1,
    fontSize: 44, bold: true, color: "FFFFFF",
    align: "center"
  });
  
  slide.addText(subtitle, {
    x: 1, y: 3.2, w: 8, h: 0.5,
    fontSize: 24, color: "FFFFFF",
    align: "center"
  });
  
  slide.addText(author, {
    x: 1, y: 4, w: 8, h: 0.4,
    fontSize: 18, color: "FFFFFF",
    align: "center"
  });
  
  return slide;
}

function addContentSlide(pptx, title, bullets) {
  const slide = pptx.addSlide();
  
  slide.addText(title, {
    x: DESIGN.layout.margin,
    y: DESIGN.layout.titleY,
    w: 9,
    h: 0.5,
    ...DESIGN.fonts.heading,
    color: DESIGN.colors.primary
  });
  
  slide.addText(bullets, {
    x: DESIGN.layout.margin,
    y: DESIGN.layout.contentY,
    w: 9,
    h: 3,
    ...DESIGN.fonts.body,
    bullet: true
  });
  
  return slide;
}
```

 * *步骤 3：构建演示文稿**（视觉优先）方法）
```javascript
const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_16x9";

// Title slide with background image or color block
const titleSlide = pptx.addSlide();
titleSlide.background = { color: DESIGN.colors.primary }; // Bold color background
addTitleSlide(
  pptx,
  "Research Title",
  "Subtitle or Conference Name",
  "Your Name • Institution • Date"
);

// Introduction with image/icon
const introSlide = pptx.addSlide();
introSlide.addImage({
  path: "concept_image.png",  // Visual representation of concept
  x: 5, y: 1.5, w: 4, h: 3
});
introSlide.addText("Background", { x: 0.5, y: 0.5, fontSize: 36, bold: true });
introSlide.addText([
  "Key context point 1 (AuthorA, 2023)",
  "Key context point 2 (AuthorB, 2022)",
  "Research gap identified (AuthorC, 2021)"
], {
  x: 0.5, y: 1.5, w: 4, h: 2,
  fontSize: 24, bullet: true
});

// Results slide - FIGURE DOMINATES
const resultsSlide = pptx.addSlide();
resultsSlide.addText("Main Finding", { x: 0.5, y: 0.5, fontSize: 32, bold: true });
resultsSlide.addImage({
  path: "results_figure.png",  // Large, clear figure
  x: 0.5, y: 1.5, w: 9, h: 4   // Nearly full slide
});
// Minimal text annotation only
resultsSlide.addText("34% improvement (p < 0.001)", {
  x: 7, y: 1, fontSize: 20, color: DESIGN.colors.accent, bold: true
});

// Save
pptx.writeFile({ fileName: "presentation.pptx" });
```

* *干演示的主要变化：**
- 标题幻灯片使用粗体背景颜色（不是纯白色）
- 简介包括相关图像（不仅仅是项目符号）
- 结果幻灯片以图形为主（不是文本为主）
- 研究项目符号中包含的引文context
- 文本最少且具有支持性，视觉效果是主要的

### 添加科学内容

* *方程**（如images):
```javascript
// Render equation as PNG first (using LaTeX or online tool)
// Then add to slide
slide.addImage({
  path: "equation.png",
  x: 2, y: 3, w: 6, h: 1
});
```

* *表格**:
```javascript
slide.addTable([
  [
    { text: "Method", options: { bold: true } },
    { text: "Accuracy", options: { bold: true } },
    { text: "Time (s)", options: { bold: true } }
  ],
  ["Method A", "0.85", "10"],
  ["Method B", "0.92", "25"],
  ["Method C", "0.88", "15"]
], {
  x: 2, y: 2, w: 6,
  fontSize: 20,
  border: { pt: 1, color: "888888" },
  fill: { color: "F5F5F5" }
});
```

* *图表**:
```javascript
// Bar chart
slide.addChart(pptx.ChartType.bar, [
  {
    name: "Control",
    labels: ["Metric 1", "Metric 2", "Metric 3"],
    values: [45, 67, 82]
  },
  {
    name: "Treatment",
    labels: ["Metric 1", "Metric 2", "Metric 3"],
    values: [52, 78, 91]
  }
], {
  x: 1, y: 1.5, w: 8, h: 4,
  chartColors: [DESIGN.colors.primary, DESIGN.colors.accent],
  showTitle: false,
  showLegend: true,
  fontSize: 18
});
```

## 可视化验证工作流程

### 生成缩略图

创建演示文稿后：

```bash
# Create thumbnail grid for quick review
python scripts/thumbnail.py presentation.pptx review/thumbnails --cols 4

# Or for individual slides
python scripts/thumbnail.py presentation.pptx review/slide
```

### 检查清单

对于每张幻灯片，检查：
- [ ]文本可读（未切断或太小）
- [ ]无元素重叠
- [ ]一致的颜色和字体
- [ ]足够的空白
- [ ]数字清晰且尺寸正确
- [ ]对齐正确

### 常见问题

* *文本溢出**：
- 减少字体大小或文本长度
- 增加文本框大小
- 拆分为多张幻灯片

* *元素重叠**：
- 使用两列布局
- 减小元素大小
- 调整定位

* *对比度较差**：
- 选择较高对比度的颜色
- 使用浅色背景上的深色文本
- 使用对比度检查器进行测试

## 模板和示例

#### 从模板开始

如果您有现有模板：

1. **提取模板结构**：
```bash
python scripts/inventory.py template.pptx inventory.json
```

2. **创建缩略图网格**：
```bash
python scripts/thumbnail.py template.pptx template_review
```

3. **分析布局**并记录要使用

4的幻灯片。 **重新排列幻灯片**：
```bash
python scripts/rearrange.py template.pptx working.pptx 0,5,5,12,18,22
```

5. **替换内容**：
```bash
python scripts/replace.py working.pptx replacements.json output.pptx
```

## 最佳实践摘要

### 要做的事情（使演示文稿引人入胜）

- ✅ 使用 research-lookup 查找 8-15 篇论文进行引用
- ✅ 为每张幻灯片添加高质量的视觉效果（图形、图像、图表、图标）
- ✅ 选择反映您主题的现代调色板（不是默认值）
- ✅ 保持文本最少（3-4 个项目符号，4-6 个单词）每个）
- ✅ 使用大字体（24-28pt 正文，36-44pt 标题）
- ✅ 改变幻灯片布局（全图、两列、视觉叠加）
- ✅ 保持高对比度（首选 7:1）
- ✅ 充足的空白（40-50% 的空白）幻灯片）
- ✅ 在介绍和讨论中引用论文（建立可信度）
- ✅ 从远处测试可读性
- ✅ 在演示前进行视觉验证

### 不要做的事情（避免枯燥的演示）

- ❌ 不要创建纯文本幻灯片（向每个幻灯片添加视觉效果）幻灯片）
- ❌ 不要使用未更改的默认主题（根据您的主题进行自定义）
- ❌ 不要使用所有要点幻灯片（不同布局）
- ❌ 不要跳过 research-lookup（演示文稿也需要引用）
- ❌ 不要塞入太多文字一张幻灯片
- ❌不要使用小字体（正文<24pt）
- ❌不要仅仅依赖颜色
- ❌不要使用复杂的动画
- ❌不要混合太多字体样式
- ❌不要忽略可访问性
- ❌ 不要跳过视觉验证

## 可访问性注意事项

* *颜色对比度**：
- 使用 WebAIM 对比度检查器
- 普通文本的最低 4.5:1
- 最佳可读性的首选 7:1

* *颜色失明**：
- 使用Coblis模拟器进行测试
- 使用带有颜色的图案/形状
- 避免红绿组合

* *可读性**：
- 仅无衬线字体
- 最小18pt，优先24pt+
- 清晰的视觉层次
- 足够的间距

## 与其他技能集成

* *与科学写作**：
- 将纸质内容转换为幻灯片
- 简化密集文本
- 提取关键发现
- 创建视觉摘要

* *通过数据可视化**：
- 简化期刊数据
- 使用更大的标签重新创建
- 使用渐进式披露
- 强调关键结果

* *通过研究查找**：
- 查找相关论文
- 提取关键引文
- 构建背景context
- 用证据支持主张

## 资源

* *PowerPoint 教程**：
- Microsoft PowerPoint 文档
- PowerPoint 设计模板
- 科学演示示例

* *设计工具**：
- 调色板生成器(Coolors.co)
- 对比度检查器 (WebAIM)
- 图标库（名词项目）
- 图像编辑（PowerPoint 内置、外部工具）

* *PPTX 技能文档**：
- `document-skills/pptx/SKILL.md`：主要文档
- `document-skills/pptx/html2pptx.md`：HTML 到 PPTX 工作流程
- `document-skills/pptx/ooxml.md`：高级编辑
- `document-skills/pptx/scripts/`：实用脚本

## 快速参考

### 常用幻灯片尺寸

- **16:9 宽高比**：10" × 5.625" (720pt × 405pt)
- **4:3 宽高比**：10" × 7.5" (720pt × 540pt)

### 测量单位

- PowerPoint 使用英寸
- 72 点 = 1英寸
- 距左上角的位置（x，y）
- 宽度和高度的尺寸（w，h）

### 字体尺寸指南

|元素|最低 |推荐|
|---------|---------|-------------|
|标题幻灯片 | 40 分 | 44-54pt |
|幻灯片标题 | 28点| 32-40pt |
|正文 | 18点| 24-28点|
|标题| 14点| 16-20点|
|页脚| 10分| 10-12pt |

### 颜色使用

- **背景**：白色或非常浅的颜色
- **文本**：浅色上的深色（黑色/深灰色），或深色上的白色
- **强调色**：一种或两种强调色 max
- **数据**：色盲安全调色板（蓝色/橙色）

## 故障排除

* *问题**：文本显示被切断
- **解决方案**：增大文本框大小或减小字体大小

* *问题**：数字模糊
- **解决方案**：使用更高分辨率的图像（300 DPI）

* *问题**：投影时颜色看起来不同
- **解决方案**：事先用投影仪测试，使用高对比度

* *问题**：文件太大
- **解决方案**：压缩图像，降低图像分辨率

  * *问题**：动画不起作用
- **解决方案**：检查PowerPoint版本兼容性

## 结论

有效的科学PowerPoint演示需要：
1. 清晰、简单的设计
2. 可读文本（24pt+正文）
3. 高品质人物
4. 一致格式
5. 视觉验证
6. 可访问性注意事项

 使用 pptx 技能进行编程创建和视觉审核工作流程，以在演示之前确保专业质量。
