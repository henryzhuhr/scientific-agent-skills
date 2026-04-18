---
name: scientific-visualization
description: 用于准备发表的人物的元技能。在创建需要多面板布局、重要性注释、错误栏、色盲安全调色板和特定期刊格式（《自然》、《科学》、《细胞》）的期刊提交图表时使用。使用发布样式协调 matplotlib/seaborn/plotly。为了快速探索，请使用 seaborn 或直接使用plotly。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 科学可视化

## 概述

科学可视化将数据转换为清晰、准确的图形以供发布。使用多面板布局、误差线、重要性标记和色盲安全调色板创建日志就绪绘图。使用 matplotlib、seaborn 导出为 PDF/EPS/TIFF，并为手稿绘制图表。

## 何时使用此技能

此技能应在以下情况下使用：
- 为科学手稿创建绘图或可视化
- 为期刊提交准备图表（《自然》、《科学》、《细胞》、《公共科学图书馆》、等）
- 确保图形对色盲者友好且可访问
- 制作具有一致样式的多面板图形
- 以正确的分辨率和格式导出图形
- 遵循特定的出版指南
- 改进现有图形以满足出版标准
- 创建需要在颜色和颜色下工作的图形grayscale

## 快速入门指南

### 基本出版质量图

```python
import matplotlib.pyplot as plt
import numpy as np

# Apply publication style (from scripts/style_presets.py)
from style_presets import apply_publication_style
apply_publication_style('default')

# Create figure with appropriate size (single column = 3.5 inches)
fig, ax = plt.subplots(figsize=(3.5, 2.5))

# Plot data
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')

# Proper labeling with units
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Amplitude (mV)')
ax.legend(frameon=False)

# Remove unnecessary spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Save in publication formats (from scripts/figure_export.py)
from figure_export import save_publication_figure
save_publication_figure(fig, 'figure1', formats=['pdf', 'png'], dpi=300)
```

### 使用预配置样式

使用中的 matplotlib 样式文件应用特定于期刊的样式`assets/`:

```python
import matplotlib.pyplot as plt

# Option 1: Use style file directly
plt.style.use('assets/nature.mplstyle')

# Option 2: Use style_presets.py helper
from style_presets import configure_for_journal
configure_for_journal('nature', figure_width='single')

# Now create figures - they'll automatically match Nature specifications
fig, ax = plt.subplots()
# ... your plotting code ...
```

### Seaborn 快速入门

对于统计图，请使用 seaborn 和发布样式：

```python
import seaborn as sns
import matplotlib.pyplot as plt
from style_presets import apply_publication_style

# Apply publication style
apply_publication_style('default')
sns.set_theme(style='ticks', context='paper', font_scale=1.1)
sns.set_palette('colorblind')

# Create statistical comparison figure
fig, ax = plt.subplots(figsize=(3.5, 3))
sns.boxplot(data=df, x='treatment', y='response', 
            order=['Control', 'Low', 'High'], palette='Set2', ax=ax)
sns.stripplot(data=df, x='treatment', y='response',
              order=['Control', 'Low', 'High'], 
              color='black', alpha=0.3, size=3, ax=ax)
ax.set_ylabel('Response (μM)')
sns.despine()

# Save figure
from figure_export import save_publication_figure
save_publication_figure(fig, 'treatment_comparison', formats=['pdf', 'png'], dpi=300)
```

## 核心原则和最佳实践

### 1. 分辨率和文件格式

* *关键要求**（详见`references/publication_guidelines.md`）：
- **光栅图像**（照片、显微镜）：300-600 DPI
- **线条艺术**（图表、绘图）：600-1200 DPI 或矢量格式
- **矢量格式**（首选）：PDF、EPS、SVG
- **光栅格式**：TIFF、PNG（科学数据绝不使用 JPEG）

* *实现：**
```python
# Use the figure_export.py script for correct settings
from figure_export import save_publication_figure

# Saves in multiple formats with proper DPI
save_publication_figure(fig, 'myfigure', formats=['pdf', 'png'], dpi=300)

# Or save for specific journal requirements
from figure_export import save_for_journal
save_for_journal(fig, 'figure1', journal='nature', figure_type='combination')
```

### 2. 颜色选择 - 色盲辅助功能

* *始终使用色盲友好的调色板**（详见`references/color_palettes.md`）：

* *推荐：Okabe-Ito 调色板**（可区分所有类型的色盲）：
```python
# Option 1: Use assets/color_palettes.py
from color_palettes import OKABE_ITO_LIST, apply_palette
apply_palette('okabe_ito')

# Option 2: Manual specification
okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=okabe_ito)
```

 * *对于热图/连续数据：**
- 使用感知均匀的颜色图：`viridis`、`plasma`、 `cividis`
- 避免红绿发散贴图（使用 `PuOr`、`RdBu`、`BrBG` 代替）
- 切勿使用 `jet` 或 `rainbow` 颜色贴图

* *始终以灰度测试图形**以确保可解释性.

### 3. 排版和文本

* *字体指南**（在 `references/publication_guidelines.md` 中详细介绍）：
- 无衬线字体：Arial、Helvetica、Calibri
- **最终打印尺寸**的最小尺寸：
  - 轴标签：7-9 pt
  - 刻度标签：6-8 pt
  - 面板标签：8-12 pt（粗体）
  - 标签的句子大小写：“时间（小时）”而不是“时间（小时）” 
  - 始终包含单位括号

* *实现：**
```python
# Set fonts globally
import matplotlib as mpl
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.labelsize'] = 9
mpl.rcParams['xtick.labelsize'] = 7
mpl.rcParams['ytick.labelsize'] = 7
```

### 4.图形尺寸

* *期刊特定宽度**（详见`references/journal_requirements.md`）：
- **自然**：单89毫米，双183 mm
- **科学**：单 55 毫米，双 175 毫米
- **单元**：单 85 毫米，双 178 毫米

* *检查图形尺寸合规性：**
```python
from figure_export import check_figure_size

fig = plt.figure(figsize=(3.5, 3))  # 89 mm for Nature
check_figure_size(fig, journal='nature')
```

### 5. 多面板图

* *最佳实践：**
- 用粗体字母标记面板：**A**、**B**、**C**（大多数期刊为大写，Nature 为小写）
- 在所有面板上保持一致的样式
- 尽可能沿边缘对齐面板
- 在面板之间使用足够的空白panel

* *示例实现**（完整代码请参见 `references/matplotlib_examples.md`）：
```python
from string import ascii_uppercase

fig = plt.figure(figsize=(7, 4))
gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.4)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
# ... create other panels ...

# Add panel labels
for i, ax in enumerate([ax1, ax2, ...]):
    ax.text(-0.15, 1.05, ascii_uppercase[i], transform=ax.transAxes,
            fontsize=10, fontweight='bold', va='top')
```

## 常见任务

### 任务 1：创建可发布的线图

完整代码请参见 `references/matplotlib_examples.md` 示例 1代码.

* *关键步骤：**
1. 应用发布样式
2. 为目标期刊
3设置适当的图形大小。使用色盲友好的颜色
4. 添加具有正确表示形式的误差线（SEM、SD 或 CI）
5. 用单位 
6 标记轴。去除不必要的刺
7. 以矢量格式保存

* *使用 seaborn 进行自动置信区间：**
```python
import seaborn as sns
fig, ax = plt.subplots(figsize=(5, 3))
sns.lineplot(data=timeseries, x='time', y='measurement',
             hue='treatment', errorbar=('ci', 95), 
             markers=True, ax=ax)
ax.set_xlabel('Time (hours)')
ax.set_ylabel('Measurement (AU)')
sns.despine()
```

### 任务 2：创建多面板图

完整代码请参见 `references/matplotlib_examples.md` 示例 2。

* *Key步骤：**
1. 使用`GridSpec`进行灵活布局
2. 确保面板之间的样式一致
3. 添加粗体面板标签（A、B、C 等）
4. 对齐相关面板
5. 验证所有文本在最终尺寸下均可读

### 任务 3：使用正确的颜色图创建热图

有关完整代码，请参阅 `references/matplotlib_examples.md` 示例 4。

* *关键步骤：**
1. 使用感知均匀的颜色图（`viridis`、`plasma`、`cividis`）
2. 包括标记的颜色条
3. 对于发散数据，请使用色盲安全发散图（`RdBu_r`、`PuOr`）
4. 为发散地图
5设置适当的中心值。测试灰度外观

* *使用 seaborn 进行相关矩阵：**
```python
import seaborn as sns
fig, ax = plt.subplots(figsize=(5, 4))
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, square=True,
            linewidths=1, cbar_kws={'shrink': 0.8}, ax=ax)
```

### 任务 4：为特定期刊准备图形

* *工作流程：**
1. 检查期刊要求：`references/journal_requirements.md`
2. 为日志配置 matplotlib：
 ```python
 from style_presets import configure_for_journal
 configure_for_journal('nature',figure_width='single')
 ```
3. 创建图形（将自动正确调整大小）
4. 使用期刊规范导出：
 ```python
 fromfigure_export import save_for_journal
 save_for_journal(fig, 'figure1', Journal='nature',figure_type='line_art')
 ```

### 任务 5：修复现有图形以满足发布要求标准

* *检查表方法**（`references/publication_guidelines.md`中的完整检查表）：

1. **检查分辨率**：验证 DPI 是否满足期刊要求
2. **检查文件格式**：绘图使用矢量，图像使用 TIFF/PNG 
3. **检查颜色**：确保色盲友好
4. **检查字体**：最终尺寸最小 6-7 pt，sans-serif
5. **检查标签**：所有轴都标有单位
6. **检查尺寸**：匹配日记帐列宽度
7. **测试灰度**：图可在没有颜色的情况下解释
8. **删除图表垃圾**：没有不必要的网格、3D 效果、阴影

### 任务 6：创建色盲友好的可视化

* *策略：**
1. 使用 `assets/color_palettes.py`
2 认可的调色板。添加冗余编码（线条样式、标记、图案）
3. 使用色盲模拟器
4进行测试。确保灰度兼容性

* *示例：**
```python
from color_palettes import apply_palette
import matplotlib.pyplot as plt

apply_palette('okabe_ito')

# Add redundant encoding beyond color
line_styles = ['-', '--', '-.', ':']
markers = ['o', 's', '^', 'v']

for i, (data, label) in enumerate(datasets):
    plt.plot(x, data, linestyle=line_styles[i % 4],
             marker=markers[i % 4], label=label)
```

## 统计严谨性

* *始终包括：**
- 误差线（SD、SEM 或 CI - 在标题中指定）
- 图中的样本大小 (n)或标题
- 统计显着性标记（*，**，***）
- 可能时的单个数据点（不仅仅是汇总统计）

* *统计示例：**
```python
# Show individual points with summary statistics
ax.scatter(x_jittered, individual_points, alpha=0.4, s=8)
ax.errorbar(x, means, yerr=sems, fmt='o', capsize=3)

# Mark significance
ax.text(1.5, max_y * 1.1, '***', ha='center', fontsize=8)
```

## 使用不同的绘图库

### Matplotlib
- 对发布细节的最大控制权
- 最适合复杂的多面板图形
- 使用提供的样式文件实现一致的格式
- 请参阅`references/matplotlib_examples.md` 以获取更多示例

### Seaborn

Seaborn 为统计图形提供了一个高级的、面向数据集的界面，构建于matplotlib。它擅长用最少的代码创建出版质量的统计可视化，同时保持与 matplotlib 自定义的完全兼容性。

* *科学可视化的主要优势：**
- 自动统计估计和置信区间
- 内置支持多面板图形（分面）
- 默认情况下色盲友好的调色板
- 使用 pandas DataFrames 的面向数据集的 API
- 变量到视觉属性的语义映射

#### 出版快速入门样式

始终先应用 matplotlib 发布样式，然后配置 seaborn:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from style_presets import apply_publication_style

# Apply publication style
apply_publication_style('default')

# Configure seaborn for publication
sns.set_theme(style='ticks', context='paper', font_scale=1.1)
sns.set_palette('colorblind')  # Use colorblind-safe palette

# Create figure
fig, ax = plt.subplots(figsize=(3.5, 2.5))
sns.scatterplot(data=df, x='time', y='response', 
                hue='treatment', style='condition', ax=ax)
sns.despine()  # Remove top and right spines
```

#### 发布的常见绘图类型

* *统计比较：**
```python
# Box plot with individual points for transparency
fig, ax = plt.subplots(figsize=(3.5, 3))
sns.boxplot(data=df, x='treatment', y='response', 
            order=['Control', 'Low', 'High'], palette='Set2', ax=ax)
sns.stripplot(data=df, x='treatment', y='response',
              order=['Control', 'Low', 'High'], 
              color='black', alpha=0.3, size=3, ax=ax)
ax.set_ylabel('Response (μM)')
sns.despine()
```

* *分布分析：**
```python
# Violin plot with split comparison
fig, ax = plt.subplots(figsize=(4, 3))
sns.violinplot(data=df, x='timepoint', y='expression',
               hue='treatment', split=True, inner='quartile', ax=ax)
ax.set_ylabel('Gene Expression (AU)')
sns.despine()
```

* *相关矩阵：**
```python
# Heatmap with proper colormap and annotations
fig, ax = plt.subplots(figsize=(5, 4))
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))  # Show only lower triangle
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, square=True,
            linewidths=1, cbar_kws={'shrink': 0.8}, ax=ax)
plt.tight_layout()
```

* *有置信度的时间序列频段：**
```python
# Line plot with automatic CI calculation
fig, ax = plt.subplots(figsize=(5, 3))
sns.lineplot(data=timeseries, x='time', y='measurement',
             hue='treatment', style='replicate',
             errorbar=('ci', 95), markers=True, dashes=False, ax=ax)
ax.set_xlabel('Time (hours)')
ax.set_ylabel('Measurement (AU)')
sns.despine()
```

#### Seaborn

的多面板图形**使用 FacetGrid 进行自动分面：**
```python
# Create faceted plot
g = sns.relplot(data=df, x='dose', y='response',
                hue='treatment', col='cell_line', row='timepoint',
                kind='line', height=2.5, aspect=1.2,
                errorbar=('ci', 95), markers=True)
g.set_axis_labels('Dose (μM)', 'Response (AU)')
g.set_titles('{row_name} | {col_name}')
sns.despine()

# Save with correct DPI
from figure_export import save_publication_figure
save_publication_figure(g.figure, 'figure_facets', 
                       formats=['pdf', 'png'], dpi=300)
```

* *将 seaborn 与 matplotlib 组合子图：**
```python
# Create custom multi-panel layout
fig, axes = plt.subplots(2, 2, figsize=(7, 6))

# Panel A: Scatter with regression
sns.regplot(data=df, x='predictor', y='response', ax=axes[0, 0])
axes[0, 0].text(-0.15, 1.05, 'A', transform=axes[0, 0].transAxes,
                fontsize=10, fontweight='bold')

# Panel B: Distribution comparison
sns.violinplot(data=df, x='group', y='value', ax=axes[0, 1])
axes[0, 1].text(-0.15, 1.05, 'B', transform=axes[0, 1].transAxes,
                fontsize=10, fontweight='bold')

# Panel C: Heatmap
sns.heatmap(correlation_data, cmap='viridis', ax=axes[1, 0])
axes[1, 0].text(-0.15, 1.05, 'C', transform=axes[1, 0].transAxes,
                fontsize=10, fontweight='bold')

# Panel D: Time series
sns.lineplot(data=timeseries, x='time', y='signal', 
             hue='condition', ax=axes[1, 1])
axes[1, 1].text(-0.15, 1.05, 'D', transform=axes[1, 1].transAxes,
                fontsize=10, fontweight='bold')

plt.tight_layout()
sns.despine()
```

#### 出版物的调色板

Seaborn 包括几个色盲安全调色板：

```python
# Use built-in colorblind palette (recommended)
sns.set_palette('colorblind')

# Or specify custom colorblind-safe colors (Okabe-Ito)
okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
sns.set_palette(okabe_ito)

# For heatmaps and continuous data
sns.heatmap(data, cmap='viridis')  # Perceptually uniform
sns.heatmap(corr, cmap='RdBu_r', center=0)  # Diverging, centered
```

#### 在轴级别和图形级别之间进行选择函数

* *轴级函数**（例如，`scatterplot`、`boxplot`、`heatmap`）：
- 在构建自定义多面板布局时使用
- 接受`ax=`参数以进行精确放置
- 与matplotlib 子图
- 对图形构成进行更多控制

```python
fig, ax = plt.subplots(figsize=(3.5, 2.5))
sns.scatterplot(data=df, x='x', y='y', hue='group', ax=ax)
```

* *图形级函数**（例如，`relplot`、`catplot`、`displot`）：
- 用于自动分面分类变量
- 创建具有一致样式的完整图形
- 非常适合探索性分析
- 使用 `height` 和 `aspect` 调整大小

```python
g = sns.relplot(data=df, x='x', y='y', col='category', kind='scatter')
```

#### 统计严谨性Seaborn

Seaborn 自动计算并显示不确定性：

```python
# Line plot: shows mean ± 95% CI by default
sns.lineplot(data=df, x='time', y='value', hue='treatment',
             errorbar=('ci', 95))  # Can change to 'sd', 'se', etc.

# Bar plot: shows mean with bootstrapped CI
sns.barplot(data=df, x='treatment', y='response',
            errorbar=('ci', 95), capsize=0.1)

# Always specify error type in figure caption:
# "Error bars represent 95% confidence intervals"
```

#### 可供出版的最佳实践 Seaborn 图

1. **始终先设置发布主题：**
 ```python
 sns.set_theme(style='ticks', context='paper', font_scale=1.1)
 ```

2. **使用色盲安全调色板：**
 ```python
 sns.set_palette('colorblind')
 ```

3. **删除不必要的元素：**
 ```python
 sns.despine() # 删除顶部和右侧的刺
 ```

4. **适当控制图形大小：**
 ```python
 # 坐标轴级别：使用 matplotlib Figsize
Fig, ax = plt.subplots(figsize=(3.5, 2.5))
 
 # 图形级别：使用高度和方面
g = sns.relplot(..., 高度=3, 方面=1.2)
 ```

5. **尽可能显示单个数据点：**
 ```python
 sns.boxplot(...) # 摘要统计
 sns.stripplot(..., alpha=0.3) # 单个点
 ```

6. **包含带有单位的正确标签：**
 ```python
 ax.set_xlabel('时间（小时）')
 ax.set_ylabel('表达式 (AU)')
 ```

7. **以正确的分辨率导出：**
 ```python
 fromfigure_export import save_publication_figure
 save_publication_figure(fig, 'figure_name', 
formats=['pdf', 'png'], dpi=300)
 ```

#### 高级 Seaborn 技术

* *用于探索性分析的成对关系：**
```python
# Quick overview of all relationships
g = sns.pairplot(data=df, hue='condition', 
                 vars=['gene1', 'gene2', 'gene3'],
                 corner=True, diag_kind='kde', height=2)
```

* *层次聚类热图：**
```python
# Cluster samples and features
g = sns.clustermap(expression_data, method='ward', 
                   metric='euclidean', z_score=0,
                   cmap='RdBu_r', center=0, 
                   figsize=(10, 8), 
                   row_colors=condition_colors,
                   cbar_kws={'label': 'Z-score'})
```

* *联合带边际分布：**
```python
# Bivariate distribution with context
g = sns.jointplot(data=df, x='gene1', y='gene2',
                  hue='treatment', kind='scatter',
                  height=6, ratio=4, marginal_kws={'kde': True})
```

#### 常见 Seaborn 问题和解决方案

* *问题：图例位于绘图区域之外**
```python
g = sns.relplot(...)
g._legend.set_bbox_to_anchor((0.9, 0.5))
```

* *问题：重叠标签**
```python
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
```

* *问题：最终尺寸的文本太小**
```python
sns.set_context('paper', font_scale=1.2)  # Increase if needed
```

#### 其他资源

有关更详细的seaborn信息，请参阅：
- `scientific-skills-zh/seaborn/SKILL.md` - 综合 seaborn 文档
- `scientific-skills-zh/seaborn/references/examples.md` - 实际用例
- `scientific-skills-zh/seaborn/references/function_reference.md` - 完整的 API 参考
- `scientific-skills-zh/seaborn/references/objects_interface.md` - 现代声明式 API

### Plotly
- 用于探索的交互式图形
- 导出用于发布的静态图像
- 配置发布质量：
```python
fig.update_layout(
    font=dict(family='Arial, sans-serif', size=10),
    plot_bgcolor='white',
    # ... see matplotlib_examples.md Example 8
)
fig.write_image('figure.png', scale=3)  # scale=3 gives ~300 DPI
```

## 资源

### 参考目录

* *根据需要加载这些以获取详细信息：**

- **`publication_guidelines.md`**：综合最佳实践
  - 分辨率和文件格式要求
  - 版式指南
  - 布局和构图规则
  - 统计严谨性要求
  - 完整的出版清单

- **`color_palettes.md`**：颜色使用指南
  - 具有 RGB 值的色盲友好调色板规范
  - 顺序和发散的色彩图建议
  - 可访问性测试程序
  - 领域特定调色板（基因组学、显微镜学）

- **`journal_requirements.md`**：期刊特定规范
  - 技术要求出版商
  - 文件格式和DPI规范
  - 图形尺寸要求
  - 快速参考表

- **`matplotlib_examples.md`**：实用代码示例
  - 10个完整的工作示例
  - 线图、条形图、热图、多面板数字
  - 期刊特定的图形示例
  - 每个库的提示（matplotlib、seaborn、绘图）

### 脚本目录

* *使用这些帮助程序脚本进行自动化：**

- **`figure_export.py`**：导出实用程序
  - `save_publication_figure()`：使用正确的 DPI 以多种格式保存 
  - `save_for_journal()`：自动使用期刊特定要求
  - `check_figure_size()`：验证尺寸是否符合期刊规格
  - 直接运行：`python scripts/figure_export.py`示例

- **`style_presets.py`**：预配置样式
  - `apply_publication_style()`：应用预设样式（默认、自然、科学、细胞）
  - `set_color_palette()`：快速调色板切换
  - `configure_for_journal()`：一命令日记配置
  - 直接运行：`python scripts/style_presets.py` 查看示例

### 资产目录

* *在图中使用这些文件：**

- **`color_palettes.py`**：可导入的颜色定义
  - 所有推荐的调色板作为Python常量
  - `apply_palette()`辅助函数
  - 可以直接导入到笔记本/脚本

- **Matplotlib样式文件**：与`plt.style.use()`
  - `publication.mplstyle`：一般出版物质量
  - `nature.mplstyle`：自然期刊规范
  - `presentation.mplstyle`：海报/幻灯片的较大字体

## 工作流程摘要

* *创建出版物的推荐工作流程数字：**

1. **计划**：确定目标期刊、图形类型和内容
2. **配置**：为journal
应用适当的样式 ```python
 from style_presets import configure_for_journal
 configure_for_journal('nature', 'single')
 ```
3. **创建**：使用正确的标签、颜色、统计信息构建图形
4. **验证**：检查大小、字体、颜色、可访问性
 ```python
 fromfigure_export import check_figure_size
 check_figure_size(fig, Journal='nature')
 ```
5. **导出**：以所需格式保存
 ```python
 fromfigure_export import save_for_journal
 save_for_journal(fig, 'figure1', 'nature', 'combination')
 ```
6. **审查**：在手稿上下文中查看最终尺寸

## 要避免的常见陷阱

1. **字体太小**：以最终尺寸 
2 打印时，文本不可读。 **JPEG 格式**：切勿将 JPEG 用于图形/绘图（创建伪像）
3. **红绿色**：约 8% 的男性无法区分 
4. **低分辨率**：出版物 
5 中的像素化数字。 **缺少单位**：始终用单位 
6 标记轴。 **3D效果**：扭曲感知，完全避免
7. **图表垃圾**：删除不必要的网格线、装饰
8. **截断轴**：从零开始条形图，除非有科学依据
9. **样式不一致**：同一手稿中的各个图形的字体/颜色不同
10. **无误差线**：始终显示不确定性

## 最终检查表

在提交图形之前，请验证：

- [ ]分辨率符合期刊要求（300+ DPI）
- [ ]文件格式正确（绘图矢量，图像TIFF）
- [ ]图尺寸与期刊匹配规格
- [ ]所有文本均以最终尺寸可读（≥6 pt）
- [ ]颜色对色盲友好
- [ ]图形以灰度形式工作
- [ ]所有标有单位的轴
- [ ]误差线在标题中显示并带有定义
- [ ]面板标签存在且一致
- [ ]无图表垃圾或 3D 效果
- [ ]所有图形的字体一致
- [ ]明确标记统计显着性
- [ ]图例清晰完整

 使用此技能可确保科学数据符合最高出版标准，同时保持所有人均可访问读者.
