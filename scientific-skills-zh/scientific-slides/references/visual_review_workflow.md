# 演示文稿的视觉审核工作流程

## 概述

视觉审核是演示文稿的关键质量保证步骤，允许您在演示之前识别并修复布局问题、文本溢出、元素重叠和设计问题。本指南涵盖将演示文稿转换为图像、系统性目视检查、常见问题和迭代改进策略。

## ⚠️ 关键规则：切勿直接阅读 PDF 演示文稿

* *强制：始终首先将演示文稿 PDF 转换为图像，然后查看图像。**

### 为什么要遵守此规则存在

- **缓冲区溢出预防**：演示文稿PDF（尤其是多幻灯片甲板）在直接读取时会导致“JSON消息超出最大缓冲区大小”错误
- **视觉准确性**：图像准确地显示观众将看到的内容，包括渲染问题
- **性能**：基于图像的审查比PDF文本提取更快、更可靠
- **一致性**：确保所有演示文稿的统一审核流程

### 演示文稿唯一正确的工作流程

1. ✅ 从 PowerPoint/Beamer 源 
2 生成 PDF。 ✅ **使用 pdf_to_images.py 脚本
3 将 PDF 转换为图像**。 ✅ **系统地查看图像文件**
4. ✅ 按幻灯片编号 
5 记录问题。 ✅ 修复源文件中的问题
6. ✅ 重新生成 PDF 并重复 

### 不要做什么

- ❌ 切勿在演示文稿 PDF 上使用 read_file 工具
- ❌ 切勿尝试将 PDF 幻灯片作为文本阅读
- ❌ 切勿跳过图像转换步骤
- ❌永远不要假设PDF“足够小”，可以直接阅读

* *如果您正在审阅演示文稿但尚未转换为图像，请先停止并转换。**

## 为什么视觉审阅很重要

### Source 中看不见的常见问题

* *LaTeX Beamer 问题**：
- 文本框中的文本溢出
- 重叠元素（图像上的方程式）
- 换行不良
- 图形超出幻灯片边界
- 实际分辨率下的字体大小问题

* *PowerPoint 问题**：
- 文本被形状或形状截断幻灯片边缘
- 图像与文本重叠
- 幻灯片之间的间距不一致
- 色彩渲染差异
- 字体替换问题

* *投影问题**：
- 内容在笔记本电脑上可见，但在投影时被切断
- 颜色在投影仪上看起来不同
- 低对比度元素变得不可见
- 小细节消失

### 视觉审阅的好处

- **及早发现布局错误**：在打印或演示之前修复
- **验证可读性**：确保文本足够大且对比度高
- **检查一致性**：发现幻灯片之间的不一致
- **测试可访问性**：验证颜色对比度和清晰度
- **验证设计**：确保专业外观

## 转换：PDF到图像

### 方法1：使用pdf_to_images.py脚本（推荐）

* *不需要外部依赖**：
脚本使用PyMuPDF，a独立的Python库 - 不需要poppler或其他系统软件。

* *安装**：
```bash
# PyMuPDF is included as a project dependency
pip install pymupdf
```

* *基本转换**：
```bash
# Convert all slides to JPEG images
python skills/scientific-slides/scripts/pdf_to_images.py presentation.pdf slide --dpi 150

# Creates: slide-001.jpg, slide-002.jpg, slide-003.jpg, ...
```

* *高分辨率转换**:
```bash
# Higher quality for detailed inspection (300 DPI)
python skills/scientific-slides/scripts/pdf_to_images.py presentation.pdf slide --dpi 300

# PNG format (lossless, larger files)
python skills/scientific-slides/scripts/pdf_to_images.py presentation.pdf slide --dpi 150 --format png
```

* *转换特定幻灯片**:
```bash
# Slides 5-10 only
python skills/scientific-slides/scripts/pdf_to_images.py presentation.pdf slide --dpi 150 --first 5 --last 10

# Single slide
python skills/scientific-slides/scripts/pdf_to_images.py presentation.pdf slide --dpi 150 --first 3 --last 3
```

* *输出选项**:
```bash
# Different output directory
python skills/scientific-slides/scripts/pdf_to_images.py presentation.pdf review/slide --dpi 150

# Custom naming
python skills/scientific-slides/scripts/pdf_to_images.py presentation.pdf output/presentation --dpi 150
```

### 方法2：使用PowerPoint缩略图脚本

对于PowerPoint演示文稿，使用pptx技能的缩略图工具：

```bash
# Create thumbnail grid
python scripts/thumbnail.py presentation.pptx output --cols 4

# Individual slides
python scripts/thumbnail.py presentation.pptx slides/slide --individual
```

* *优点**：
- 针对PowerPoint文件进行优化
- 可以创建概览网格
- 手柄.pptx格式直接
- 可自定义布局

### 方法3：使用ImageMagick

* *安装**：
```bash
# Ubuntu/Debian
sudo apt-get install imagemagick

# macOS
brew install imagemagick
```

* *转换**：
```bash
# Convert PDF to images
convert -density 150 presentation.pdf slide.jpg

# Higher quality
convert -density 300 presentation.pdf slide.jpg

# Specific format
convert -density 150 presentation.pdf slide.png
```

### 方法4：使用Python（编程）

```python
import fitz  # PyMuPDF

# Open PDF
doc = fitz.open('presentation.pdf')

# Convert each page to image
zoom = 200 / 72  # 200 DPI (72 is base DPI)
matrix = fitz.Matrix(zoom, zoom)

for i, page in enumerate(doc, start=1):
    pixmap = page.get_pixmap(matrix=matrix)
    pixmap.save(f'slide-{i:03d}.jpg', output='jpeg')

doc.close()
```

* *安装 PyMuPDF**:
```bash
pip install pymupdf
# No external dependencies needed!
```

## 系统性目视检查

### 检查工作流程

* *第 1 步：概览通行证**
- 快速查看所有幻灯片
- 整体注释一致性
- 识别明显有问题的幻灯片
- 创建需要详细审查的幻灯片列表

* *步骤2：详细检查**
- 仔细审查每张标记的幻灯片
- 检查问题清单（如下）
- 用幻灯片编号记录具体问题
- 记录所需的内容修复

* *步骤 3：跨幻灯片比较**
- 检查相似幻灯片之间的一致性
- 验证均匀的间距和对齐
- 确保字体大小一致
- 检查配色方案一致性

* *步骤4：距离测试**
- 以缩小的尺寸查看图像（模拟）投影）
- 从 ~6 英尺处检查可读性
- 验证关键元素是否可见
- 测试主要信息是否清晰

### 问题检查表

查看每张幻灯片是否存在这些常见问题：

#### 文本问题

* *溢出和截断**：
- [ ]文本在幻灯片边缘被截断
- [ ]文本延伸到文本框之外
- [ ]方程进入边距
- [ ]说明文字在底部被截断
- [ ]项目符号点延伸到外部边界

* *可读性**：
- [ ]字体太小（最小 18pt 可见）
- [ ]对比度差（文本与背景）
- [ ]行间距不足
- [ ]文本太靠近幻灯片边缘
- [ ]重叠行文本

#### 元素重叠

* *文本重叠**：
- [ ]文本与图像重叠
- [ ]文本与形状重叠
- [ ]多个文本框重叠
- [ ]标签与数据点重叠
- [ ]标题重叠与内容

* *视觉元素重叠**：
- [ ]图像重叠
- [ ]形状不适当地重叠
- [ ]数字延伸到边距
- [ ]图例与绘图重叠
- [ ]水印模糊内容

#### 布局和间距

* *对齐问题**：
- [ ]文本框未对齐
- [ ]边距不均匀
- [ ]元素定位不一致
- [ ]标题偏离中心
- [ ]项目符号点未对齐

  * *间距问题**：
- [ ]内容狭窄（空白不足）
- [ ]空白空间过多（幻灯片区域使用不当）
- [ ]元素之间的间距不一致
- [ ]多列布局中间隙不均匀
- [ ]内容分布不良

#### 颜色和颜色对比度

* *可见性**：
- [ ]对比度不足（文本与背景）
- [ ]颜色太相似（难以区分）
- [ ]繁忙背景上的文本
- [ ]浅色背景上的浅色文本
- [ ]深色上的深色文本背景

* *一致性**：
- [ ]幻灯片之间的配色方案不一致
- [ ]意外的颜色变化
- [ ]冲突的颜色组合
- [ ]数据可视化的颜色选择不佳

#### 图形和图形

* *质量**：
- [ ]像素化或模糊的图像
- [ ]低分辨率图形
- [ ]纵横比扭曲
- [ ]屏幕截图质量差
- [ ]锯齿状边缘图形

* *布局**：
- [ ]数字太小难以阅读
- [ ]轴标签太小
- [ ]图例文本难以辨认
- [ ]没有解释的复杂数字
- [ ]数字未居中或对齐

#### 技术问题

* *渲染**：
- [ ]缺少字体（已替换）
- [ ]未显示特殊字符
- [ ]方程渲染不正确
- [ ]图像损坏或文件丢失
- [ ]颜色不正确（RGB 与CMYK)

* *一致性**：
- [ ]幻灯片编号不正确或缺失
- [ ]页脚/页眉不一致
- [ ]导航元素损坏
- [ ]超链接不起作用（如果进行交互测试）

## 文档模板

### 问题日志格式

创建跟踪所有问题的电子表格或文档：

```
Slide # | Issue Category | Description | Severity | Status
--------|---------------|-------------|----------|--------
3       | Text Overflow | Bullet point 4 extends beyond box | High | Fixed
7       | Element Overlap | Figure overlaps with caption | High | Fixed
12      | Font Size | Axis labels too small | Medium | Fixed
15      | Alignment | Title not centered | Low | Fixed
22      | Contrast | Yellow text on white background | High | Fixed
```

* *严重级别**：
- **严重**：使幻灯片无法使用或不专业
- **高**：显着影响可读性或外观
- **中**：明显但不妨碍理解
- **低**：轻微修饰issues

### 示例问题文档

* *良好的文档**：
```
Slide 8: Text Overflow Issue
- Description: Last bullet point "...implementation details" 
  extends ~0.5 inches beyond right margin of text box
- Cause: Bullet text too long for available width
- Fix: Reduce text to "...implementation" or increase box width
- Verification: Check neighboring slides for similar issue
```

* *较差的文档**：
```
Slide 8: text problem
- Fix: make smaller
```

## 常见问题和解决方案

### 问题1：文本溢出

* *问题**：文本超出边界

* *识别**：
- 可见文本在边缘被切断
- 文本进入边距
- 部分字符可见

* *解决方案**：

* *LaTeX Beamer**:
```latex
% Reduce text
\begin{frame}{Title}
  \begin{itemize}
    \item Shorten this long bullet point
    % or
    \item Use abbreviations or acronyms
    % or
    \item<alert@1> Split into multiple bullets
  \end{itemize}
\end{frame}

% Adjust margins
\newgeometry{margin=1.5cm}
\begin{frame}
  Content with wider margins
\end{frame}
\restoregeometry

% Smaller font for specific element
{\small
  Long text that needs to fit
}
```

* *PowerPoint**:
- 减小该元素的字体大小
- 缩短文本内容
- 增加文本框大小
- 使用文本框自动调整选项（谨慎）
- 拆分为多个幻灯片

### 问题 2：元素重叠

* *问题**：元素不恰当地重叠

* *识别**：
- 文本被图像遮挡
- 形状覆盖文本
- 数字重叠

* *解决方案**：

* *LaTeX Beamer**：
```latex
% Use columns for better separation
\begin{columns}
  \begin{column}{0.5\textwidth}
    Text content
  \end{column}
  \begin{column}{0.5\textwidth}
    \includegraphics[width=\textwidth]{figure.pdf}
  \end{column}
\end{columns}

% Add spacing
\vspace{0.5cm}

% Adjust figure size
\includegraphics[width=0.7\textwidth]{figure.pdf}
```

* *PowerPoint**：
- 使用对齐参考线重新定位
- 减少元素大小
- 使用两列布局
- 向后/向前发送元素（分层）
- 增加元素之间的间距

### 问题3：对比度差

* *问题**：文本由于颜色选择而难以阅读

* *识别**：
- 需要眯着眼睛才能阅读文本
- 文本淡入背景
- 颜色太相似

* *解决方案**：

* *LaTeX Beamer**：
```latex
% Increase contrast
\setbeamercolor{frametitle}{fg=black,bg=white}
\setbeamercolor{normal text}{fg=black,bg=white}

% Use darker colors
\definecolor{darkblue}{RGB}{0,50,100}
\setbeamercolor{structure}{fg=darkblue}

% Test in grayscale
\usepackage{xcolor}
\selectcolormodel{gray}  % Temporarily for testing
```

* *PowerPoint**：
- 选择高对比度颜色组合
- 在浅色背景上使用深色文本反之亦然
- 避免文本采用粉彩
- 使用 WebAIM 对比度检查器进行测试
- 如果需要，添加文本背景框

### 问题 4：微小字体

 * *问题**：文本太小，无法从远处阅读

* *识别**：
- 无法读取 3 英尺外的文本
- 正常查看时轴标签消失
- 字幕难以辨认

* *解决方案**：

* *LaTeX Beamer**：
```latex
% Increase base font size
\documentclass[14pt]{beamer}  % Instead of 11pt default

% Recreate figures with larger fonts
% In matplotlib:
plt.rcParams['font.size'] = 18
plt.rcParams['axes.labelsize'] = 20

% In R/ggplot2:
theme_set(theme_minimal(base_size = 16))
```

* *PowerPoint**：
- 正文最小 18 点，首选 24 点
- 使用较大标签重新创建图形
- 使用直接标签而不是图例
- 简化复杂图形
- 分割密集内容多张幻灯片

### 问题 5：未对齐

* *问题**：元素未正确对齐

* *标识**：
- 边距不均匀
- 标题位于不同位置
- 不规则间距

* *解决方案**：

* *LaTeX Beamer**：
```latex
% Use consistent templates
\setbeamertemplate{frametitle}[default][center]

% Align columns at top
\begin{columns}[T]  % T = top alignment
  \begin{column}{0.5\textwidth}
    Content
  \end{column}
  \begin{column}{0.5\textwidth}
    Content
  \end{column}
\end{columns}

% Center figures
\begin{center}
  \includegraphics[width=0.8\textwidth]{figure.pdf}
\end{center}
```

* *PowerPoint**：
- 使用对齐工具（左对齐/居中/右对齐）
- 启用网格线和参考线
- 使用对齐grid
- 均匀分布对象
- 创建布局一致的母版幻灯片

## 迭代改进过程

### 工作流程周期

```
1. Generate PDF
    ↓
2. Convert to images
    ↓
3. Systematic visual inspection
    ↓
4. Document issues
    ↓
5. Prioritize fixes
    ↓
6. Apply corrections to source
    ↓
7. Regenerate PDF
    ↓
8. Re-inspect (go to step 2)
    ↓
9. Complete when no critical issues remain
```

### 优先级策略

* *立即修复**（块演示文稿）：
- 文本溢出，导致内容不可读
- 关键元素重叠，模糊数据
- 图形损坏或内容丢失
- 对比度严重较差

* *呈现前修复**：
- 字体太小
- 中等对齐问题
- 间距不一致
- 中等对比度问题

* *如果时间允许则修复**：
- 轻微错位
- 小间距不一致
- 外观改进
- 非关键颜色调整

### 停止标准

* *最低标准**：
- [ ]无文本溢出或截断
- [ ]没有元素重叠模糊内容
- [ ]所有文本至少以18pt 等效可读
- [ ]足够对比度（最小比例为 4.5:1）
- [ ]图形和图像显示正确
- [ ]幻灯片结构一致

* *理想标准**：
- [ ]整体专业外观
- [ ]一致的对齐和间距
- [ ]高对比度（7:1 比例）
- [ ]最佳字体大小（24pt+）
- [ ]精美的视觉设计
- [ ]零布局问题

## 自动检测策略

### 用于文本溢出检测的Python脚本

```python
from PIL import Image
import numpy as np

def detect_edge_content(image_path, threshold=10):
    """
    Detect if content extends too close to slide edges.
    Returns True if potential overflow detected.
    """
    img = Image.open(image_path).convert('L')  # Grayscale
    arr = np.array(img)
    
    # Check edges (10 pixel border)
    left_edge = arr[:, :threshold]
    right_edge = arr[:, -threshold:]
    top_edge = arr[:threshold, :]
    bottom_edge = arr[-threshold:, :]
    
    # Look for non-white pixels (content)
    white_threshold = 240
    
    issues = []
    if np.any(left_edge < white_threshold):
        issues.append("Left edge")
    if np.any(right_edge < white_threshold):
        issues.append("Right edge")
    if np.any(top_edge < white_threshold):
        issues.append("Top edge")
    if np.any(bottom_edge < white_threshold):
        issues.append("Bottom edge")
    
    return issues

# Usage
for slide_num in range(1, 26):
    issues = detect_edge_content(f'slide-{slide_num}.jpg')
    if issues:
        print(f"Slide {slide_num}: Content near {', '.join(issues)}")
```

### 对比度检查

```python
from PIL import Image
import numpy as np

def check_contrast(image_path):
    """
    Estimate contrast ratio in image.
    Simple version: compare lightest and darkest regions.
    """
    img = Image.open(image_path).convert('L')
    arr = np.array(img)
    
    # Get brightness values
    bright = np.percentile(arr, 95)
    dark = np.percentile(arr, 5)
    
    # Rough contrast ratio
    contrast = (bright + 0.05) / (dark + 0.05)
    
    if contrast < 4.5:
        return f"Low contrast: {contrast:.1f}:1 (minimum 4.5:1)"
    return f"OK: {contrast:.1f}:1"

# Usage
for slide_num in range(1, 26):
    result = check_contrast(f'slide-{slide_num}.jpg')
    print(f"Slide {slide_num}: {result}")
```

## 手动审查最佳实践

### 审查环境

* *设置**：
- 大显示器或双显示器
- 良好的照明（不太亮，不太暗）
- 无干扰的环境
- 具有缩放功能的图像查看器
- 用于跟踪问题的记事本或电子表格

* *查看选项**：
- 以 100% 查看以进行细节检查
- 以 50% 查看以模拟距离
- 按顺序查看以检查一致性
- 并排比较相似的幻灯片

### 复习提示

* *新鲜的眼睛**：
- 休息一下每 15-20 张幻灯片
- 在一天的不同时间进行审核
- 让同事进行审核
- 第二天回来进行最终检查

* *系统方法**：
- 按顺序审核（幻灯片 1 → 结束）
- 一次专注于一种问题类型time
- 使用清单确保彻底性
- 随手记录，而不是凭记忆

* *常见监督**：
- 备份幻灯片（也查看这些！）
- 标题幻灯片（第一印象很重要）
- 致谢幻灯片（通常）忘记了）
- 最后一张幻灯片（在问答过程中可见）

## 工具和资源

### 推荐软件

* *PDF到图像转换**：
- **PyMuPDF**（Python）：快速，无外部依赖（推荐）
- **pdf_to_images.py 脚本**：易于 CLI 使用的包装器
- **ImageMagick**：灵活，多种选项（可选）

* *图像查看**：
- **IrfanView** (Windows)：快速，多种格式
- **预览** (macOS)：内置，简单
- **Eye GNOME** (Linux)：轻量级
- **XnView**：跨平台、批量操作

* *问题跟踪**：
- **电子表格**（Excel、Google Sheets）：简单、灵活
- **Markdown 文件**：版本控制友好
- **问题跟踪器**（GitHub、Jira）：如果团队协作
- **清单应用程序**：用于移动审阅

### 对比Checkers

- **WebAIM 对比度检查器**：https://webaim.org/resources/contrastchecker/
- **颜色对比度分析器**：桌面应用程序
- **Chrome DevTools**：内置对比度检查

### 色盲模拟器

- **Coblis**：https://www.color-blindness.com/coblis-color-blindness-simulator/
- **Color Oracle**：免费桌面应用程序
- **Photoshop/GIMP**：内置色盲滤镜

## 摘要清单

在最终确定您的产品之前演示文稿：

* *转换**：
- [ ] PDF 转换为足够分辨率的图像 (150-300 DPI)
- [ ]转换的所有幻灯片（包括备份幻灯片）
- [ ]保存在组织目录中的图像

* *Visual检查**：
- [ ]系统地审查所有幻灯片
- [ ]为每张幻灯片完成问题清单
- [ ]用幻灯片编号记录的问题
- [ ]分配给每个问题的严重性

  * *问题解决**：
- [ ]关键问题已修复
- [ ]已解决高优先级问题
- [ ]已更新源文件（不仅仅是PDF）
- [ ]重新生成并重新检查

  * *最终验证**：
- [ ]无文本溢出或截断
- [ ]没有不适当的元素重叠
- [ ]整体对比度充足
- [ ]一致的布局和间距
- [ ]专业外观
- [ ]准备投影或分发

  * *测试**：
- [ ]在投影仪上测试，如果可能
- [ ]从房间后面观看距离
- [ ]在各种照明条件下检查
- [ ]已保存备份副本
