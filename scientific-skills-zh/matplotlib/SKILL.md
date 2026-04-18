---
name: matplotlib
description: 用于完全定制的低级绘图库。当您需要对每个绘图元素进行细粒度控制、创建新颖的绘图类型或与特定的科学工作流程集成时使用。导出为 PNG/PDF/SVG 以便发布。对于快速统计图，请使用 seaborn；对于交互式绘图，请使用plotly；对于具有期刊样式的可供出版的多面板图形，请使用 scientific-visualization。
license: https://github.com/matplotlib/matplotlib/tree/main/LICENSE
metadata:
    skill-author: K-Dense Inc.
---

# Matplotlib

## 概述

Matplotlib 是 Python 的基础可视化库，用于创建静态、动画和交互式绘图。此技能提供有效使用 matplotlib 的指导，涵盖 pyplot 接口（MATLAB 样式）和面向对象的 API（图/轴），以及创建出版物质量可视化的最佳实践。

## 何时使用此技能

此技能应在以下情况下使用：
- 创建任何类型的绘图或图表（折线图、散点图、条形图、直方图、热图、轮廓等）
- 生成科学或统计可视化
- 自定义绘图外观（颜色、样式、标签、图例）
- 使用子图创建多面板图形
- 将可视化导出为各种格式（PNG、PDF、SVG等）
- 构建交互式绘图或动画
- 使用 3D 可视化
- 将绘图集成到 Jupyter 笔记本或 GUI 应用程序中

## 核心概念

### Matplotlib 层次结构

Matplotlib 使用对象的层次结构：

1. **图** - 所有绘图元素
2 的顶级容器。 **轴** - 显示数据的实际绘图区域（一个图形可以包含多个轴）
3. **艺术家** - 图形上可见的所有内容（线条、文本、刻度线等）
4. **轴** - 处理刻度和标签的数轴对象（x 轴、y 轴）

### 两个接口

* *1。 pyplot 接口（隐式，MATLAB 风格）**
```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()
```
- 方便快速、简单的绘图
- 自动维护状态
- 适合交互式工作和简单脚本

* *2。面向对象的接口（显式）**
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4])
ax.set_ylabel('some numbers')
plt.show()
```
- **推荐用于大多数用例**
- 对图形和轴进行更明确的控制
- 更适合具有多个子图的复杂图形
- 更易于维护和调试

## 常见工作流程

### 1. 基本绘图

* *单图工作流程：**
```python
import matplotlib.pyplot as plt
import numpy as np

# Create figure and axes (OO interface - RECOMMENDED)
fig, ax = plt.subplots(figsize=(10, 6))

# Generate and plot data
x = np.linspace(0, 2*np.pi, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')

# Customize
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Trigonometric Functions')
ax.legend()
ax.grid(True, alpha=0.3)

# Save and/or display
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.show()
```

### 2. 多个子图

* *创建子图布局：**
```python
# Method 1: Regular grid
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].plot(x, y1)
axes[0, 1].scatter(x, y2)
axes[1, 0].bar(categories, values)
axes[1, 1].hist(data, bins=30)

# Method 2: Mosaic layout (more flexible)
fig, axes = plt.subplot_mosaic([['left', 'right_top'],
                                 ['left', 'right_bottom']],
                                figsize=(10, 8))
axes['left'].plot(x, y)
axes['right_top'].scatter(x, y)
axes['right_bottom'].hist(data)

# Method 3: GridSpec (maximum control)
from matplotlib.gridspec import GridSpec
fig = plt.figure(figsize=(12, 8))
gs = GridSpec(3, 3, figure=fig)
ax1 = fig.add_subplot(gs[0, :])  # Top row, all columns
ax2 = fig.add_subplot(gs[1:, 0])  # Bottom two rows, first column
ax3 = fig.add_subplot(gs[1:, 1:])  # Bottom two rows, last two columns
```

### 3. 绘图类型和用例

* *线图** - 时间序列，连续数据、趋势
```python
ax.plot(x, y, linewidth=2, linestyle='--', marker='o', color='blue')
```

* *散点图** - 变量之间的关系、相关性
```python
ax.scatter(x, y, s=sizes, c=colors, alpha=0.6, cmap='viridis')
```

* *条形图** - 分类比较
```python
ax.bar(categories, values, color='steelblue', edgecolor='black')
# For horizontal bars:
ax.barh(categories, values)
```

* *直方图** -分布
```python
ax.hist(data, bins=30, edgecolor='black', alpha=0.7)
```

* *热图** - 矩阵数据、相关性
```python
im = ax.imshow(matrix, cmap='coolwarm', aspect='auto')
plt.colorbar(im, ax=ax)
```

* *等值线图** - 2D 平面上的 3D 数据
```python
contour = ax.contour(X, Y, Z, levels=10)
ax.clabel(contour, inline=True, fontsize=8)
```

* *箱线图** -统计分布
```python
ax.boxplot([data1, data2, data3], labels=['A', 'B', 'C'])
```

* *小提琴图** - 分布密度
```python
ax.violinplot([data1, data2, data3], positions=[1, 2, 3])
```

有关全面的绘图类型示例和变体，请参阅 `references/plot_types.md`.

### 4. 样式和样式定制

* *颜色指定方法：**
- 命名颜色：`'red'`、`'blue'`、`'steelblue'`
- 十六进制代码：`'#FF5733'`
- RGB 元组：`(0.1, 0.2, 0.3)`
- 颜色图：`cmap='viridis'`、`cmap='plasma'`、`cmap='coolwarm'`

* *使用样式表：**
```python
plt.style.use('seaborn-v0_8-darkgrid')  # Apply predefined style
# Available styles: 'ggplot', 'bmh', 'fivethirtyeight', etc.
print(plt.style.available)  # List all available styles
```

* *自定义rcParams:**
```python
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.titlesize'] = 18
```

* *文本和注释:**
```python
ax.text(x, y, 'annotation', fontsize=12, ha='center')
ax.annotate('important point', xy=(x, y), xytext=(x+1, y+1),
            arrowprops=dict(arrowstyle='->', color='red'))
```

有关详细的样式选项和颜色图指南，请参阅 `references/styling_guide.md`.

### 5. 保存人物

* *导出为各种格式：**
```python
# High-resolution PNG for presentations/papers
plt.savefig('figure.png', dpi=300, bbox_inches='tight', facecolor='white')

# Vector format for publications (scalable)
plt.savefig('figure.pdf', bbox_inches='tight')
plt.savefig('figure.svg', bbox_inches='tight')

# Transparent background
plt.savefig('figure.png', dpi=300, bbox_inches='tight', transparent=True)
```

* *重要参数：**
- `dpi`：分辨率（出版物300，网页150，屏幕72）
- `bbox_inches='tight'`：删除多余的空白
- `facecolor='white'`：确保白色背景（对于透明主题有用）
- `transparent=True`：透明背景

### 6. 使用 3D Plots

```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Surface plot
ax.plot_surface(X, Y, Z, cmap='viridis')

# 3D scatter
ax.scatter(x, y, z, c=colors, marker='o')

# 3D line plot
ax.plot(x, y, z, linewidth=2)

# Labels
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
```

## 最佳实践

### 1. 接口选择
- **生产代码使用面向对象的接口**（fig, ax = plt.subplots()）
- 保留pyplot接口仅用于快速交互探索
- 始终显式创建图形，而不是依赖隐式状态

### 2. 图尺寸和 DPI
- 在创建时设置图尺寸：`fig, ax = plt.subplots(figsize=(10, 6))`
- 对输出介质使用适当的 DPI：
  - 屏幕/笔记本：72-100 dpi
  - 网页：150 dpi
  - 打印/出版物：300 dpi

### 3. 布局管理
- 使用 `constrained_layout=True` 或 `tight_layout()` 防止元素重叠
- 建议使用 `fig, ax = plt.subplots(constrained_layout=True)` 自动间距

### 4. 颜色图选择
- **顺序**（viridis、plasma、 inferno）：具有一致进展的有序数据
- **发散**（coolwarm，RdBu）：具有有意义的中心点（例如零）的数据
- **定性**（tab10，Set3）：分类/标称数据
- 避免彩虹色图（jet） - 它们不是感知上的uniform

### 5. 辅助功能
- 使用色盲友好的颜色图（viridis、cividis）
- 除了颜色之外还为条形图添加图案/阴影线
- 确保元素之间有足够的对比度
- 包括描述性标签和图例

### 6.性能
- 对于大型数据集，在绘图调用中使用 `rasterized=True` 来减小文件大小
- 在绘图之前使用适当的数据缩减（例如，下采样密集时间序列）
- 对于动画，使用位图传输以获得更好的性能

### 7. 代码组织
```python
# Good practice: Clear structure
def create_analysis_plot(data, title):
    """Create standardized analysis plot."""
    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

    # Plot data
    ax.plot(data['x'], data['y'], linewidth=2)

    # Customize
    ax.set_xlabel('X Axis Label', fontsize=12)
    ax.set_ylabel('Y Axis Label', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    return fig, ax

# Use the function
fig, ax = create_analysis_plot(my_data, 'My Analysis')
plt.savefig('analysis.png', dpi=300, bbox_inches='tight')
```

## 快速参考脚本

此技能包括`scripts/`目录中的帮助程序脚本：

### `plot_template.py`
模板脚本通过最佳实践演示各种绘图类型。以此作为创建新可视化的起点。

* *用法：**
```bash
python scripts/plot_template.py
```

### `style_configurator.py`
交互式实用程序，用于配置 matplotlib 样式首选项并生成自定义样式Sheets.

* *用法：**
```bash
python scripts/style_configurator.py
```

## 详细参考

详细信息请查阅参考文档：

- **`references/plot_types.md`** - 包含代码示例和用例的完整绘图类型目录
- **`references/styling_guide.md`** - 详细的样式选项、颜色图和自定义
- **`references/api_reference.md`** - 核心类和方法参考
- **`references/common_issues.md`** - 常见问题的故障排除指南问题

## 与其他工具集成

Matplotlib 与以下工具集成良好：
- **NumPy/Pandas** - 从数组和 DataFrame 直接绘图
- **Seaborn** - 基于 matplotlib 构建的高级统计可视化
- **Jupyter** - 使用交互式绘图`%matplotlib inline` 或 `%matplotlib widget`
- **GUI 框架** - 嵌入 Tkinter、Qt、wxPython 应用程序

## 常见问题

1. **重叠元素**：使用 `constrained_layout=True` 或 `tight_layout()`
2. **状态混乱**：使用OO接口避免pyplot状态机问题
3. **许多图形存在内存问题**：使用 `plt.close(fig)`
4 显式关闭图形。 **字体警告**：使用 `plt.rcParams['font.sans-serif']`
5 安装字体或抑制警告。 **DPI 混淆**：请记住，figsize 的单位是英寸，而不是像素：`pixels = dpi * inches`

## 其他资源

- 官方文档：https://matplotlib.org/
- 图库：https://matplotlib.org/stable/gallery/index.html
- 备忘单： https://matplotlib.org/cheatsheets/
  - 教程：https://matplotlib.org/stable/tutorials/index.html
