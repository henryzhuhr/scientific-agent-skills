---
name: seaborn
description: 与 pandas 集成的统计可视化。用于快速探索分布、关系以及与有吸引力的默认值的分类比较。最适合箱线图、小提琴图、配对图、热图。基于 matplotlib 构建。对于交互式绘图，请使用plotly；对于发布样式，请使用 scientific-visualization。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# Seaborn 统计可视化

## 概述

Seaborn 是一个Python 可视化库，用于创建出版质量的统计图形。使用此技能以最少的代码进行面向数据集的绘图、多变量分析、自动统计估计和复杂的多面板图形。

## 设计理念

Seaborn 遵循以下核心原则：

1. **面向数据集**：直接使用 DataFrame 和命名变量，而不是抽象坐标
2. **语义映射**：自动将数据值转换为视觉属性（颜色、大小、样式）
3. **统计意识**：内置聚合、误差估计和置信区间
4. **审美默认设置**：开箱即用的可出版主题和调色板
5. **Matplotlib 集成**：在需要时完全兼容 matplotlib 定制

## 快速入门

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load example dataset
df = sns.load_dataset('tips')

# Create a simple visualization
sns.scatterplot(data=df, x='total_bill', y='tip', hue='day')
plt.show()
```

## 核心绘图接口

### 函数接口（传统）

函数接口提供按可视化类型组织的专门绘图功能。每个类别都有**轴级**函数（绘制到单轴）和**图形级**函数（通过分面管理整个图形）。

* *何时使用：**
- 快速探索性分析
- 单一用途可视化
- 当您需要特定的绘图类型时

### 对象接口（现代）

`seaborn.objects` 接口提供了类似于 ggplot2 的声明式、可组合 API。通过链接方法来指定数据映射、标记、转换和比例来构建可视化。

* *何时使用：**
- 复杂分层可视化
- 当您需要对转换进行细粒度控制时
- 构建自定义绘图类型
- 编程绘图Generation

```python
from seaborn import objects as so

# Declarative syntax
(
    so.Plot(data=df, x='total_bill', y='tip')
    .add(so.Dot(), color='day')
    .add(so.Line(), so.PolyFit())
)
```

## 按类别绘制函数

### 关系图（变量之间的关系）

* *用于：** 探索两个或多个变量如何相互关联

- `scatterplot()` - 将单个观察结果显示为点
- `lineplot()` - 显示趋势和变化（自动聚合和计算 CI）
- `relplot()` - 具有自动分面功能的图形级界面

  * *关键参数：**
- `x`、`y` - 主变量
- `hue` - 附加分类/连续变量的颜色编码
- `size` - 点/线尺寸编码
- `style` - 标记/线样式编码
- `col`、`row` - 分为多个子图（仅限图形级别）

```python
# Scatter with multiple semantic mappings
sns.scatterplot(data=df, x='total_bill', y='tip',
                hue='time', size='size', style='sex')

# Line plot with confidence intervals
sns.lineplot(data=timeseries, x='date', y='value', hue='category')

# Faceted relational plot
sns.relplot(data=df, x='total_bill', y='tip',
            col='time', row='sex', hue='smoker', kind='scatter')
```

### 分布图（单变量和双变量分布）

* *用于：**了解数据传播、形状和概率密度

- `histplot()` - 基于条形的频率分布，具有灵活的分箱
- `kdeplot()` - 使用高斯核进行平滑密度估计
- `ecdfplot()` - 经验累积分布（无需调整参数）
- `rugplot()` - 个体观察刻度线
- `displot()` - 单变量和双变量分布的图形级界面
- `jointplot()` - 边缘分布的双变量图
- `pairplot()` - 数据集中的成对关系矩阵

* *Key参数：**
- `x`、`y` - 变量（y 对于单变量可选）
- `hue` - 按类别单独分布
- `stat` - 归一化：“计数”、“频率”、“概率”、 “密度”
- `bins` / `binwidth` - 直方图分箱控制
- `bw_adjust` - KDE 带宽乘数（更高 = 更平滑）
- `fill` - 曲线下填充区域
- `multiple` - 如何处理色调：“layer”、“stack”、“dodge”、“fill”

```python
# Histogram with density normalization
sns.histplot(data=df, x='total_bill', hue='time',
             stat='density', multiple='stack')

# Bivariate KDE with contours
sns.kdeplot(data=df, x='total_bill', y='tip',
            fill=True, levels=5, thresh=0.1)

# Joint plot with marginals
sns.jointplot(data=df, x='total_bill', y='tip',
              kind='scatter', hue='time')

# Pairwise relationships
sns.pairplot(data=df, hue='species', corner=True)
```

### 分类图（跨类别比较）

* *用于：**比较离散类别的分布或统计数据

* *分类散点图：**
- `stripplot()` - 带抖动的点以显示所有观测结果
- `swarmplot()` - 非重叠点（蜂群算法）

* *分布比较：**
- `boxplot()` - 四分位数和离群值
- `violinplot()` - KDE + 四分位数信息
- `boxenplot()` - 针对较大数据集的增强箱线图

* *统计估计：**
- `barplot()` - 具有置信区间的平均值/合计
- `pointplot()` - 带连接线的点估计
- `countplot()` - 每个类别的观测值计数

* *图形级别：**
- `catplot()` - 多面分类图（集） `kind` 参数）

* *关键参数：**
- `x`、`y` - 变量（通常是分类变量）
- `hue` - 附加分类分组
- `order`、 `hue_order` - 控制类别排序
- `dodge` - 并排单独的色调级别
- `orient` - “v”（垂直）或“h”（水平）
- `kind` - catplot 的绘图类型：“strip”， "swarm", "box", "violin", "bar", "point"

```python
# Swarm plot showing all points
sns.swarmplot(data=df, x='day', y='total_bill', hue='sex')

# Violin plot with split for comparison
sns.violinplot(data=df, x='day', y='total_bill',
               hue='sex', split=True)

# Bar plot with error bars
sns.barplot(data=df, x='day', y='total_bill',
            hue='sex', estimator='mean', errorbar='ci')

# Faceted categorical plot
sns.catplot(data=df, x='day', y='total_bill',
            col='time', kind='box')
```

### 回归图（线性关系）

* *用途：** 可视化线性回归和残差

- `regplot()` - 使用散点 + 拟合的轴级回归图line
- `lmplot()` - 具有分面支持的图形级别
- `residplot()` - 用于评估模型拟合的残差图

* *关键参数：**
- `x`、`y` - 变量regress
- `order` - 多项式回归阶数
- `logistic` - 拟合逻辑回归
- `robust` - 使用稳健回归（对异常值不太敏感）
- `ci` - 置信区间宽度（默认） 95)
- `scatter_kws`、`line_kws` - 自定义散点和线条属性

```python
# Simple linear regression
sns.regplot(data=df, x='total_bill', y='tip')

# Polynomial regression with faceting
sns.lmplot(data=df, x='total_bill', y='tip',
           col='time', order=2, ci=95)

# Check residuals
sns.residplot(data=df, x='total_bill', y='tip')
```

### 矩阵图（矩形数据）

* *用于：** 可视化矩阵、相关性和网格结构数据

- `heatmap()` - 带注释的颜色编码矩阵
- `clustermap()` - 分层集群heatmap

* *关键参数：**
- `data` - 2D矩形数据集（DataFrame或数组）
- `annot` - 在单元格中显示值
- `fmt` - 注释的格式字符串（例如，“.2f”）
- `cmap` - 颜色图名称
- `center` - 颜色图中心的值（用于发散颜色图）
- `vmin`、`vmax` - 颜色比例限制
- `square` - 强制方形单元格
- `linewidths` - 单元格之间的间隙

```python
# Correlation heatmap
corr = df.corr()
sns.heatmap(corr, annot=True, fmt='.2f',
            cmap='coolwarm', center=0, square=True)

# Clustered heatmap
sns.clustermap(data, cmap='viridis',
               standard_scale=1, figsize=(10, 10))
```

## 多图网格

Seaborn 提供用于创建复杂的多面板图形的网格对象：

### FacetGrid

根据分类变量创建子图。通过图形级函数（`relplot`、`displot`、`catplot`）调用时最有用，但可直接用于自定义绘图。

```python
g = sns.FacetGrid(df, col='time', row='sex', hue='smoker')
g.map(sns.scatterplot, 'total_bill', 'tip')
g.add_legend()
```

### PairGrid

显示a中所有变量之间的成对关系dataset.

```python
g = sns.PairGrid(df, hue='species')
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
g.map_diag(sns.histplot)
g.add_legend()
```

### JointGrid

将二元图与边际分布结合起来。

```python
g = sns.JointGrid(data=df, x='total_bill', y='tip')
g.plot_joint(sns.scatterplot)
g.plot_marginals(sns.histplot)
```

## 图级函数与轴级函数

理解这种区别对于有效seaborn 用法：

### 轴级函数
- 绘制到单个 matplotlib `Axes` 对象
- 轻松集成到复杂的 matplotlib 图形中
- 接受 `ax=` 参数以实现精确放置
- 返回`Axes`对象
- 示例：`scatterplot`、`histplot`、`boxplot`、`regplot`、`heatmap`

* *何时使用：**
- 构建自定义多绘图布局
- 组合不同的绘图类型
- 需要matplotlib级别控制
- 与现有的matplotlib代码集成

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
sns.scatterplot(data=df, x='x', y='y', ax=axes[0, 0])
sns.histplot(data=df, x='x', ax=axes[0, 1])
sns.boxplot(data=df, x='cat', y='y', ax=axes[1, 0])
sns.kdeplot(data=df, x='x', y='y', ax=axes[1, 1])
```

### 图形级函数
- 管理整个图形，包括所有子图
- 通过 `col` 和 `row` 参数进行内置分面 
- 返回 `FacetGrid`、`JointGrid` 或`PairGrid` 对象
- 使用 `height` 和 `aspect` 调整大小（每个子图）
- 无法放置在现有图形中
- 示例：`relplot`、`displot`、`catplot`、 `lmplot`、`jointplot`、`pairplot`

* *何时使用：**
- 分面可视化（小倍数）
- 快速探索性分析
- 一致的多面板布局
- 不需要与其他图结合类型

```python
# Automatic faceting
sns.relplot(data=df, x='x', y='y', col='category', row='group',
            hue='type', height=3, aspect=1.2)
```

## 数据结构要求

### 长格式数据（首选）

E每个变量是一列，每个观察是一行。这种“整洁”的格式提供了最大的灵活性：

```python
# Long-form structure
   subject  condition  measurement
0        1    control         10.5
1        1  treatment         12.3
2        2    control          9.8
3        2  treatment         13.1
```

* *优点：**
- 与所有seaborn函数一起使用
- 轻松将变量重新映射到可视属性
- 支持任意复杂性
- DataFrame自然操作

### 宽格式数据

变量分布在列中。对于简单的矩形数据很有用：

```python
# Wide-form structure
   control  treatment
0     10.5       12.3
1      9.8       13.1
```

* *用例：**
- 简单时间序列
- 相关矩阵
- 热图
- 数组数据的快速绘图

* *将宽范围转换为long:**
```python
df_long = df.melt(var_name='condition', value_name='measurement')
```

## 调色板

Seaborn 为不同数据类型提供精心设计的调色板：

### 定性调色板（分类数据）

通过色调变化区分类别：
- `"deep"` - 默认，鲜艳的色彩
- `"muted"` - 较柔和，饱和度较低
- `"pastel"` - 浅色，去饱和
- `"bright"` - 高度饱和
- `"dark"` - 深色值
- `"colorblind"` - 对于色觉缺陷来说是安全的

```python
sns.set_palette("colorblind")
sns.color_palette("Set2")
```

### 顺序调色板（有序数据）

显示从低值到高值的进度：
- `"rocket"`、`"mako"` - 宽亮度范围（适用于热图）
- `"flare"`、`"crest"` - 限制亮度（适用于点/线）
- `"viridis"`， `"magma"`、`"plasma"` - Matplotlib 感知均匀

```python
sns.heatmap(data, cmap='rocket')
sns.kdeplot(data=df, x='x', y='y', cmap='mako', fill=True)
```

### 发散调色板（中心数据）

E 强调与中点的偏差：
- `"vlag"` - 蓝色到红色
- `"icefire"` - 蓝色到橙色
- `"coolwarm"` - 冷色到暖色
- `"Spectral"` - 彩虹发散

```python
sns.heatmap(correlation_matrix, cmap='vlag', center=0)
```

### 定制调色板

```python
# Create custom palette
custom = sns.color_palette("husl", 8)

# Light to dark gradient
palette = sns.light_palette("seagreen", as_cmap=True)

# Diverging palette from hues
palette = sns.diverging_palette(250, 10, as_cmap=True)
```

## 主题和美学

### 设置主题

`set_theme()`控制整体外观：

```python
# Set complete theme
sns.set_theme(style='whitegrid', palette='pastel', font='sans-serif')

# Reset to defaults
sns.set_theme()
```

### 样式

控制背景和网格外观：
- `"darkgrid"` - 灰色背景，带白色网格（默认）
- `"whitegrid"` - 白色背景，带灰色网格
- `"dark"` - 灰色背景，无网格
- `"white"` - 白色背景，无网格
- `"ticks"` - 带轴刻度的白色背景

```python
sns.set_style("whitegrid")

# Remove spines
sns.despine(left=False, bottom=False, offset=10, trim=True)

# Temporary style
with sns.axes_style("white"):
    sns.scatterplot(data=df, x='x', y='y')
```

### 上下文

针对不同用例的缩放元素：
- `"paper"` - 最小（默认）
- `"notebook"` - 稍大
- `"talk"` - 演示幻灯片
- `"poster"` - 大格式

```python
sns.set_context("talk", font_scale=1.2)

# Temporary context
with sns.plotting_context("poster"):
    sns.barplot(data=df, x='category', y='value')
```

## 最佳实践

### 1. 数据准备

始终使用具有有意义的列名称的结构良好的DataFrame：

```python
# Good: Named columns in DataFrame
df = pd.DataFrame({'bill': bills, 'tip': tips, 'day': days})
sns.scatterplot(data=df, x='bill', y='tip', hue='day')

# Avoid: Unnamed arrays
sns.scatterplot(x=x_array, y=y_array)  # Loses axis labels
```

### 2. 选择正确的绘图类型

* *连续x，连续y：** `scatterplot`， `lineplot`、`kdeplot`、`regplot`
* *连续x、分类y：** `violinplot`、`boxplot`、`stripplot`、`swarmplot`
* *一个连续变量：** `histplot`、`kdeplot`、`ecdfplot`
  * *相关性/矩阵：** `heatmap`、`clustermap`
  * *成对关系：** `pairplot`、 `jointplot`

### 3. 使用图形级函数进行分面

```python
# Instead of manual subplot creation
sns.relplot(data=df, x='x', y='y', col='category', col_wrap=3)

# Not: Creating subplots manually for simple faceting
```

### 4. 利用语义映射

使用 `hue`、`size` 和 `style` 来编码附加内容维度：

```python
sns.scatterplot(data=df, x='x', y='y',
                hue='category',      # Color by category
                size='importance',    # Size by continuous variable
                style='type')         # Marker style by type
```

### 5. 控制统计估计

许多函数自动计算统计数据。了解并定制：

```python
# Lineplot computes mean and 95% CI by default
sns.lineplot(data=df, x='time', y='value',
             errorbar='sd')  # Use standard deviation instead

# Barplot computes mean by default
sns.barplot(data=df, x='category', y='value',
            estimator='median',  # Use median instead
            errorbar=('ci', 95))  # Bootstrapped CI
```

### 6.与Matplotlib结合

Seaborn与matplotlib无缝集成进行微调：

```python
ax = sns.scatterplot(data=df, x='x', y='y')
ax.set(xlabel='Custom X Label', ylabel='Custom Y Label',
       title='Custom Title')
ax.axhline(y=0, color='r', linestyle='--')
plt.tight_layout()
```

### 7.保存高质量图

```python
fig = sns.relplot(data=df, x='x', y='y', col='group')
fig.savefig('figure.png', dpi=300, bbox_inches='tight')
fig.savefig('figure.pdf')  # Vector format for publications
```

## 常见模式

### 探索性数据分析

```python
# Quick overview of all relationships
sns.pairplot(data=df, hue='target', corner=True)

# Distribution exploration
sns.displot(data=df, x='variable', hue='group',
            kind='kde', fill=True, col='category')

# Correlation analysis
corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
```

### 出版质量图

```python
sns.set_theme(style='ticks', context='paper', font_scale=1.1)

g = sns.catplot(data=df, x='treatment', y='response',
                col='cell_line', kind='box', height=3, aspect=1.2)
g.set_axis_labels('Treatment Condition', 'Response (μM)')
g.set_titles('{col_name}')
sns.despine(trim=True)

g.savefig('figure.pdf', dpi=300, bbox_inches='tight')
```

### 复杂多面板图

```python
# Using matplotlib subplots with seaborn
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

sns.scatterplot(data=df, x='x1', y='y', hue='group', ax=axes[0, 0])
sns.histplot(data=df, x='x1', hue='group', ax=axes[0, 1])
sns.violinplot(data=df, x='group', y='y', ax=axes[1, 0])
sns.heatmap(df.pivot_table(values='y', index='x1', columns='x2'),
            ax=axes[1, 1], cmap='viridis')

plt.tight_layout()
```

### 带置信带的时间序列

```python
# Lineplot automatically aggregates and shows CI
sns.lineplot(data=timeseries, x='date', y='measurement',
             hue='sensor', style='location', errorbar='sd')

# For more control
g = sns.relplot(data=timeseries, x='date', y='measurement',
                col='location', hue='sensor', kind='line',
                height=4, aspect=1.5, errorbar=('ci', 95))
g.set_axis_labels('Date', 'Measurement (units)')
```

## 故障排除

### 问题：图例位于绘图区域之外

默认情况下，图形级函数将图例放置在外部。要移入内部：

```python
g = sns.relplot(data=df, x='x', y='y', hue='category')
g._legend.set_bbox_to_anchor((0.9, 0.5))  # Adjust position
```

### 问题：重叠标签

```python
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
```

### 问题：图形太小

对于图形级别函数：
```python
sns.relplot(data=df, x='x', y='y', height=6, aspect=1.5)
```

对于轴级函数：
```python
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x='x', y='y', ax=ax)
```

### 问题：颜色不够鲜明

```python
# Use a different palette
sns.set_palette("bright")

# Or specify number of colors
palette = sns.color_palette("husl", n_colors=len(df['category'].unique()))
sns.scatterplot(data=df, x='x', y='y', hue='category', palette=palette)
```

### 问题：KDE 太平滑或Jagged

```python
# Adjust bandwidth
sns.kdeplot(data=df, x='x', bw_adjust=0.5)  # Less smooth
sns.kdeplot(data=df, x='x', bw_adjust=2)    # More smooth
```

## 资源

此技能包括用于更深入探索的参考资料：

### 参考资料/

- `function_reference.md` - 所有 seaborn 函数及其参数和示例的综合列表
- `objects_interface.md` - 现代 seaborn.objects API 的详细指南
- `examples.md` - 不同分析场景的常见用例和代码模式

根据需要加载详细函数签名、高级参数或具体示例的参考文件。
