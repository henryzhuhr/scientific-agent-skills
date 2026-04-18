# LaTeX 研究海报生成技能

使用 LaTeX 为会议和学术演示创建专业的、可发表的研究海报。

## 概述

此技能为使用三个主要 LaTeX 软件包创建研究海报提供全面指导：
- **beamerposter**：传统学术海报，熟悉的 Beamer 语法
- **tikzposter**：采用 TikZ 集成的现代、多彩设计
- **baposter**：具有自动定位功能的结构化多栏布局

## 快速入门

### 1. 选择模板

在 `assets/` 中浏览模板：
- `beamerposter_template.tex` - 经典学术风格
- `tikzposter_template.tex` - 现代、多彩的设计
- `baposter_template.tex` - 结构化多列布局

### 2.自定义内容

根据您的研究编辑模板：
- 标题、作者、从属关系
- 简介、方法、结果、结论
- 用图像替换占位符数字
- 更新参考文献和致谢

### 3. 配置整页

海报应以最小边距覆盖整个页面：

```latex
% beamerposter - full page setup
\documentclass[final,t]{beamer}
\usepackage[size=a0,scale=1.4,orientation=portrait]{beamerposter}
\setbeamersize{text margin left=5mm, text margin right=5mm}
\usepackage[margin=10mm]{geometry}

% tikzposter - full page setup
\documentclass[25pt,a0paper,portrait,margin=10mm,innermargin=15mm]{tikzposter}

% baposter - full page setup
\documentclass[a0paper,portrait,fontscale=0.285]{baposter}
```

### 4.编译

```bash
pdflatex poster.tex

# Or for better font support:
lualatex poster.tex
xelatex poster.tex
```

### 5.审查PDF质量

* *打印前必备！**

```bash
# Run automated checks
./scripts/review_poster.sh poster.pdf

# Manual verification (see checklist below)
```

## 主要功能

### 全页覆盖

全部配置为最大化内容区域的模板：
- 最小外边距 (5-15 毫米)
- 列之间的最佳间距 (15-20 毫米)
- 适当的块填充以提高可读性
- 无浪费的空白区域

### PDF 质量控制

* *自动检查**（`review_poster.sh`）：
- 页面大小验证
- 字体嵌入检查
- 图像分辨率分析
- 文件大小优化

* *手动验证** (`assets/poster_quality_checklist.md`):
- 100% 缩放时的目视检查
- 缩小比例打印测试 (25%)
- 版式和间距审查
- 内容完整性检查

### 设计原则

所有模板均遵循循证海报设计：
- **版式**：72pt+标题，48-72pt标题，24-36pt正文
- **颜色**：高对比度（≥4.5:1），色盲友好调色板
- **布局**：清晰的视觉层次，逻辑流程
- **内容**：最多300-800字，40-50%视觉内容

## 常见海报尺寸

模板支持所有标准尺寸：

|尺寸|尺寸|配置|
|------|------------|---------------|
| A0 | 841 × 1189 毫米 | `size=a0` 或 `a0paper` |
| A1 | 594 × 841 毫米 | `size=a1` 或 `a1paper` |
| 36×48 英寸 | 914 × 1219 毫米 | 自定义页面尺寸 |
| 42×56 英寸 | 1067 × 1422 毫米 |自定义页面尺寸|

## 文档

#### 参考指南

* *综合文档**（在`references/`中）：

1. **`latex_poster_packages.md`**（746行）
  - beamerposter、tikzposter、baposter的详细比较
  - 特定于包的语法和示例
  - 优点、限制、最佳用例
  - 主题和颜色定制
  - 编译提示和故障排除

2. **`poster_design_principles.md`**（807 行）
  - 视觉层次结构和空白
  - 版式：字体选择、大小、可读性
  - 颜色理论：方案、对比度、可访问性
  - 色盲友好调色板
  - 图标、图形和视觉elements
  - 要避免的常见设计错误

3. **`poster_layout_design.md`**（650+行）
  - 网格系统（2、3、4列布局）
  - 视觉流和阅读模式
  - 空间组织策略
  - 空白管理
  - 块和盒设计
  - 布局模式研究型

4. **`poster_content_guide.md`**（900+ 行）
  - 内容策略（3-5 分钟规则）
  - 按部分的文字预算
  - 视觉与文本比率（40-50% 视觉）
  - 特定部分的写作指导
  - 图形整合和标题
  - 从纸张到海报改编

### 工具和资产

* *脚本**（在`scripts/`中）：
- `review_poster.sh`：自动PDF质量检查
  - 页面大小验证
  - 字体嵌入检查
  - 图像分辨率分析
  - 文件大小评估

* *清单**（在`assets/`中）：
- `poster_quality_checklist.md`：综合预打印清单
  - 预编译检查
  - PDF质量验证
  - 目视检查项目
  - 辅助功能检查
  - 同行评审指南
  - 最终打印清单

* *模板**（在`assets/`中）：
- `beamerposter_template.tex`：完整工作模板
- `tikzposter_template.tex`：完整工作模板
- `baposter_template.tex`：完整工作模板

## 工作流程

### 推荐海报创作流程

* *1。规划**（LaTeX 之前）
- 确定会议要求（大小、方向）
- 确定要突出显示的 3-5 个关键结果
- 创建图形 (300+ DPI)
- 起草 300-800 字内容大纲

* *2。模板选择**
- 根据需求选择套餐：
  - **beamerposter**：传统会议、机构品牌
  - **tikzposter**：现代会议、创意领域
  - **baposter**：多节海报、结构化布局

* *3.内容集成**
- 复制模板并自定义
- 替换占位符文本
- 添加图形并确保高分辨率
- 配置颜色以匹配品牌

* *4。编译和审查**
- 编译为 PDF
- 运行 `review_poster.sh` 进行自动检查
- 以 100% 缩放进行视觉审查
- 对照 `poster_quality_checklist.md`

* *5。测试打印**
- **关键步骤！** 以 25% 比例打印
- A0 → A4 纸，36×48" → 信纸
- 从 2-3 英尺处查看（模拟完整海报的 8-12 英尺）
- 验证可读性和颜色

* *6。修订**
- 修复发现的任何问题
- 仔细校对（错误被放大！）
- 获取同事反馈
- 最终编译

* *7.打印**
- 验证页面尺寸：`pdfinfo poster.pdf`
- 检查嵌入的字体：`pdffonts poster.pdf`
- 在截止日期前 2-3 天发送到专业打印机
- 保留备份副本

## 故障排除

### 大白色页边距

* *问题**：海报边缘周围的空白过多

* *解决方案**：
```latex
% beamerposter
\setbeamersize{text margin left=5mm, text margin right=5mm}
\usepackage[margin=10mm]{geometry}

% tikzposter
\documentclass[..., margin=5mm, innermargin=10mm]{tikzposter}

% baposter
\documentclass[a0paper, margin=5mm]{baposter}
```

### 内容剪切

* *问题**：文本或图形超出页面

* *解决方案**：
- 检查总宽度：列+ 间距 + 边距 = pagewidth
- 减少列宽或间距
- 使用可见页面边界进行调试：
```latex
\usepackage{eso-pic}
\AddToShipoutPictureBG{
  \AtPageLowerLeft{
    \put(0,0){\framebox(\LenToUnit{\paperwidth},\LenToUnit{\paperheight}){}}
  }
}
```

### 模糊图像

* *问题**：像素化或低质量数字

* *解决方案**：
- 尽可能使用矢量图形（PDF、SVG）
- 光栅图像：最终打印尺寸至少 300 DPI
- 对于 A0 宽度 (33.1")：最小 300 DPI = 9930 像素
- 检查： `pdfimages -list poster.pdf`

### 未嵌入字体

* *问题**：打印机因缺少字体而拒绝 PDF

* *解决方案**：
```bash
# Recompile with embedded fonts
pdflatex -dEmbedAllFonts=true poster.tex

# Verify embedding
pdffonts poster.pdf
# All fonts should show "yes" in "emb" column
```

### 文件太大

* *问题**：PDF超出电子邮件大小限制（>50MB）

* *解决方案**：
```bash
# Compress for digital sharing
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
   -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=poster_compressed.pdf poster.pdf

# Keep original uncompressed version for printing
```

## 要避免的常见错误

### 内容
- ❌文本太多（>1000）字）
- ❌ 字体太小（<24pt 正文）
- ❌ 没有明确的主要信息
- ✅ 300-800 个单词，30pt+ 正文，1-3 个关键发现

### 设计
- ❌ 色彩对比度差(<4.5:1)
- ❌ 红绿颜色组合（色盲问题）
- ❌ 布局杂乱，没有空白
- ✅ 高对比度，易于使用的颜色，宽敞的间距

### 技术
- ❌ 错误的海报尺寸
- ❌ 低分辨率图像 (<300 DPI)
- ❌ 未嵌入字体
- ✅ 验证规格、高分辨率图像、嵌入字体

## 封装比较

选择正确封装的快速参考：

|特色|投影海报 | tikz海报 |巴海报|
|---------|----------------|------------|----------|
| **学习曲线** |简单（Beamer 用户）|中等|中等|
| **美学** |传统|现代|专业|
| **定制** |中等|高 (TikZ) |结构化|
| **编译速度** |快|慢一点 |快-中|
| **最适合** |学术会议 |创意设计|多栏布局 |

* *推荐**：
- 初次海报制作：**beamerposter**（熟悉、简单）
- 现代会议：**tikzposter**（美观、灵活）
- 复杂布局：**baposter**（自动定位）

## 示例用法

### 在科学作家CLI中

```
> Create a research poster for NeurIPS conference on transformer attention

The assistant will:
1. Ask about poster size and orientation
2. Generate complete LaTeX poster with your content
3. Configure for full page coverage
4. Provide compilation instructions
5. Run quality checks on generated PDF
```

### 手动创建

```bash
# 1. Copy template
cp assets/tikzposter_template.tex my_poster.tex

# 2. Edit content
vim my_poster.tex

# 3. Compile
pdflatex my_poster.tex

# 4. Review
./scripts/review_poster.sh my_poster.pdf

# 5. Test print at 25% scale
# (A0 on A4 paper)

# 6. Final printing
```

## 成功提示

### 内容策略
1. **一条主要信息**：观众应该记住的一件事是什么？
2. **3-5 个关键人物**：视觉内容占主导地位
3. **300-800字**：少即是多
4. **要点**：比段落更易于浏览

### 设计策略
1. **高对比度**：暗色亮色或亮色暗色
2. **大字体**：30pt+ 正文文本，以便从远处阅读 
3. **空白**：海报的 30-40% 应为空
4. **视觉层次**：大小显着变化（标题3×正文）

### 技术策略
1. **尽早测试**：最终打印 
2 之前以 25% 比例打印。 **矢量图形**：尽可能使用 PDF/SVG
3. **验证规格**：检查页面大小、字体、分辨率
4. **获取反馈**：打印前请同事查看

## 其他资源

### 在线工具
- **颜色对比度检查器**：https://webaim.org/resources/contrastchecker/
- **色盲模拟器**： https://www.color-blindness.com/coblis-color-blindness-simulator/
- **调色板生成器**：https://coolors.co/

### LaTeX Packages
- `beamerposter`：为海报大小的文档扩展 Beamer
- `tikzposter`：使用 Tik 创建现代海报Z
- `baposter`：基于框的自动海报布局
- `qrcode`：在中生成 QR 代码LaTeX
- `graphicx`：包括图像
- `tcolorbox`：彩色框和框架

### 进一步阅读
- `references/`目录中的所有参考文档
- `assets/poster_quality_checklist.md`
中的质量检查表- `references/latex_poster_packages.md`

## 中的软件包比较支持 

对于问题或疑问：
- 查看 `references/`
 中的参考文档- 检查上面的故障排除部分 
- 运行自动审核：`./scripts/review_poster.sh`
- 使用质量检查表： `assets/poster_quality_checklist.md`

## 版本

LaTeX Poster Skill v1.0
兼容：beamerposter、tikzposter、baposter
最后更新：2025年1月
