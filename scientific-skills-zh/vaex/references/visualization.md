# 数据可视化

此参考涵盖了 Vaex 的可视化功能，用于创建大型数据集的绘图、热图和交互式可视化。

## 概述

Vaex 擅长通过高效的分箱和聚合来可视化具有数十亿行的数据集。可视化系统直接处理大数据，无需采样，提供整个数据集的准确表示。

* *主要功能：**
- 交互式可视化十亿行数据集
- 无需采样-使用所有数据
- 自动分箱和聚合
- 与matplotlib集成
- 交互式小部件Jupyter

## 基本绘图

### 1D 直方图

```python
import vaex
import matplotlib.pyplot as plt

df = vaex.open('data.hdf5')

# Simple histogram
df.plot1d(df.age)

# With customization
df.plot1d(df.age,
          limits=[0, 100],
          shape=50,              # Number of bins
          figsize=(10, 6),
          xlabel='Age',
          ylabel='Count')

plt.show()
```

### 2D 密度图（热图）

```python
# Basic 2D plot
df.plot(df.x, df.y)

# With limits
df.plot(df.x, df.y, limits=[[0, 10], [0, 10]])

# Auto limits using percentiles
df.plot(df.x, df.y, limits='99.7%')  # 3-sigma limits

# Customize shape (resolution)
df.plot(df.x, df.y, shape=(512, 512))

# Logarithmic color scale
df.plot(df.x, df.y, f='log')
```

### 散点图（小）数据)

```python
# For smaller datasets or samples
df_sample = df.sample(n=1000)

df_sample.scatter(df_sample.x, df_sample.y,
                  alpha=0.5,
                  s=10)  # Point size

plt.show()
```

## 高级可视化选项

### 色阶和标准化

```python
# Linear scale (default)
df.plot(df.x, df.y, f='identity')

# Logarithmic scale
df.plot(df.x, df.y, f='log')
df.plot(df.x, df.y, f='log10')

# Square root scale
df.plot(df.x, df.y, f='sqrt')

# Custom colormap
df.plot(df.x, df.y, colormap='viridis')
df.plot(df.x, df.y, colormap='plasma')
df.plot(df.x, df.y, colormap='hot')
```

### 限制和范围

```python
# Manual limits
df.plot(df.x, df.y, limits=[[xmin, xmax], [ymin, ymax]])

# Percentile-based limits
df.plot(df.x, df.y, limits='99.7%')  # 3-sigma
df.plot(df.x, df.y, limits='95%')
df.plot(df.x, df.y, limits='minmax')  # Full range

# Mixed limits
df.plot(df.x, df.y, limits=[[0, 100], 'minmax'])
```

### 分辨率Control

```python
# Higher resolution (more bins)
df.plot(df.x, df.y, shape=(1024, 1024))

# Lower resolution (faster)
df.plot(df.x, df.y, shape=(128, 128))

# Different resolutions per axis
df.plot(df.x, df.y, shape=(512, 256))
```

## 统计可视化

### 可视化聚合

```python
# Mean on a grid
df.plot(df.x, df.y, what=df.z.mean(),
        limits=[[0, 10], [0, 10]],
        shape=(100, 100),
        colormap='viridis')

# Standard deviation
df.plot(df.x, df.y, what=df.z.std())

# Sum
df.plot(df.x, df.y, what=df.z.sum())

# Count (default)
df.plot(df.x, df.y, what='count')
```

### 多重统计

```python
# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Count
df.plot(df.x, df.y, what='count',
        ax=axes[0, 0], show=False)
axes[0, 0].set_title('Count')

# Mean
df.plot(df.x, df.y, what=df.z.mean(),
        ax=axes[0, 1], show=False)
axes[0, 1].set_title('Mean of z')

# Std
df.plot(df.x, df.y, what=df.z.std(),
        ax=axes[1, 0], show=False)
axes[1, 0].set_title('Std of z')

# Min
df.plot(df.x, df.y, what=df.z.min(),
        ax=axes[1, 1], show=False)
axes[1, 1].set_title('Min of z')

plt.tight_layout()
plt.show()
```

## 使用选择

同时可视化不同的数据段：

```python
import vaex
import matplotlib.pyplot as plt

df = vaex.open('data.hdf5')

# Create selections
df.select(df.category == 'A', name='group_a')
df.select(df.category == 'B', name='group_b')

# Plot both selections
df.plot1d(df.value, selection='group_a', label='Group A')
df.plot1d(df.value, selection='group_b', label='Group B')
plt.legend()
plt.show()

# 2D plot with selection
df.plot(df.x, df.y, selection='group_a')
```

### 叠加多个选择

```python
# Create base plot
fig, ax = plt.subplots(figsize=(10, 8))

# Plot each selection with different colors
df.plot(df.x, df.y, selection='group_a',
        ax=ax, show=False, colormap='Reds', alpha=0.5)
df.plot(df.x, df.y, selection='group_b',
        ax=ax, show=False, colormap='Blues', alpha=0.5)

ax.set_title('Overlaid Selections')
plt.show()
```

## 子图和布局

### 创建多个绘图

```python
import matplotlib.pyplot as plt

# Create subplot grid
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Plot different variables
variables = ['x', 'y', 'z', 'a', 'b', 'c']
for idx, var in enumerate(variables):
    row = idx // 3
    col = idx % 3
    df.plot1d(df[var], ax=axes[row, col], show=False)
    axes[row, col].set_title(f'Distribution of {var}')

plt.tight_layout()
plt.show()
```

### 分面绘图

```python
# Plot by category
categories = df.category.unique()

fig, axes = plt.subplots(1, len(categories), figsize=(15, 5))

for idx, cat in enumerate(categories):
    df_cat = df[df.category == cat]
    df_cat.plot(df_cat.x, df_cat.y,
                ax=axes[idx], show=False)
    axes[idx].set_title(f'Category {cat}')

plt.tight_layout()
plt.show()
```

## 交互式小部件 (Jupyter)

在 Jupyter 笔记本中创建交互式可视化：

### 选择Widget

```python
# Interactive selection
df.widget.selection_expression()
```

### 直方图Widget

```python
# Interactive histogram with selection
df.plot_widget(df.x, df.y)
```

### 散点Widget

```python
# Interactive scatter plot
df.scatter_widget(df.x, df.y)
```

## 自定义

### 样式绘图

```python
import matplotlib.pyplot as plt

# Create plot with custom styling
fig, ax = plt.subplots(figsize=(12, 8))

df.plot(df.x, df.y,
        limits='99%',
        shape=(256, 256),
        colormap='plasma',
        ax=ax,
        show=False)

# Customize axes
ax.set_xlabel('X Variable', fontsize=14, fontweight='bold')
ax.set_ylabel('Y Variable', fontsize=14, fontweight='bold')
ax.set_title('Custom Density Plot', fontsize=16, fontweight='bold')
ax.grid(alpha=0.3)

# Add colorbar
plt.colorbar(ax.collections[0], ax=ax, label='Density')

plt.tight_layout()
plt.show()
```

### 图形大小和 DPI

```python
# High-resolution plot
df.plot(df.x, df.y,
        figsize=(12, 10),
        dpi=300)
```

## 专业可视化

### Hexbin图

```python
# Alternative to heatmap using hexagonal bins
plt.figure(figsize=(10, 8))
plt.hexbin(df.x.values[:100000], df.y.values[:100000],
           gridsize=50, cmap='viridis')
plt.colorbar(label='Count')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
```

### 等值线图

```python
import numpy as np

# Get 2D histogram data
counts = df.count(binby=[df.x, df.y],
                  limits=[[0, 10], [0, 10]],
                  shape=(100, 100))

# Create contour plot
x = np.linspace(0, 10, 100)
y = np.linspace(0, 10, 100)
plt.contourf(x, y, counts.T, levels=20, cmap='viridis')
plt.colorbar(label='Count')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Contour Plot')
plt.show()
```

### 矢量场叠加

```python
# Compute mean vectors on grid
mean_vx = df.mean(df.vx, binby=[df.x, df.y],
                  limits=[[0, 10], [0, 10]],
                  shape=(20, 20))
mean_vy = df.mean(df.vy, binby=[df.x, df.y],
                  limits=[[0, 10], [0, 10]],
                  shape=(20, 20))

# Create grid
x = np.linspace(0, 10, 20)
y = np.linspace(0, 10, 20)
X, Y = np.meshgrid(x, y)

# Plot
fig, ax = plt.subplots(figsize=(10, 8))

# Base heatmap
df.plot(df.x, df.y, ax=ax, show=False)

# Vector overlay
ax.quiver(X, Y, mean_vx.T, mean_vy.T, alpha=0.7, color='white')

plt.show()
```

## 性能注意事项

### 优化大型可视化

```python
# For very large datasets, reduce shape
df.plot(df.x, df.y, shape=(256, 256))  # Fast

# For publication quality
df.plot(df.x, df.y, shape=(1024, 1024))  # Higher quality

# Balance quality and performance
df.plot(df.x, df.y, shape=(512, 512))  # Good balance
```

### 缓存可视化数据

```python
# Compute once, plot multiple times
counts = df.count(binby=[df.x, df.y],
                  limits=[[0, 10], [0, 10]],
                  shape=(512, 512))

# Use in different plots
plt.figure()
plt.imshow(counts.T, origin='lower', cmap='viridis')
plt.colorbar()
plt.show()

plt.figure()
plt.imshow(np.log10(counts.T + 1), origin='lower', cmap='plasma')
plt.colorbar()
plt.show()
```

## 导出并保存

### 保存图形

```python
# Save as PNG
df.plot(df.x, df.y)
plt.savefig('plot.png', dpi=300, bbox_inches='tight')

# Save as PDF (vector)
plt.savefig('plot.pdf', bbox_inches='tight')

# Save as SVG
plt.savefig('plot.svg', bbox_inches='tight')
```

### 批量绘图

```python
# Generate multiple plots
variables = ['x', 'y', 'z']

for var in variables:
    plt.figure(figsize=(10, 6))
    df.plot1d(df[var])
    plt.title(f'Distribution of {var}')
    plt.savefig(f'plot_{var}.png', dpi=300, bbox_inches='tight')
    plt.close()
```

## 常见模式

### 模式：探索性数据分析

```python
import matplotlib.pyplot as plt

# Create comprehensive visualization
fig = plt.figure(figsize=(16, 12))

# 1D histograms
ax1 = plt.subplot(3, 3, 1)
df.plot1d(df.x, ax=ax1, show=False)
ax1.set_title('X Distribution')

ax2 = plt.subplot(3, 3, 2)
df.plot1d(df.y, ax=ax2, show=False)
ax2.set_title('Y Distribution')

ax3 = plt.subplot(3, 3, 3)
df.plot1d(df.z, ax=ax3, show=False)
ax3.set_title('Z Distribution')

# 2D plots
ax4 = plt.subplot(3, 3, 4)
df.plot(df.x, df.y, ax=ax4, show=False)
ax4.set_title('X vs Y')

ax5 = plt.subplot(3, 3, 5)
df.plot(df.x, df.z, ax=ax5, show=False)
ax5.set_title('X vs Z')

ax6 = plt.subplot(3, 3, 6)
df.plot(df.y, df.z, ax=ax6, show=False)
ax6.set_title('Y vs Z')

# Statistics on grids
ax7 = plt.subplot(3, 3, 7)
df.plot(df.x, df.y, what=df.z.mean(), ax=ax7, show=False)
ax7.set_title('Mean Z on X-Y grid')

plt.tight_layout()
plt.savefig('eda_summary.png', dpi=300, bbox_inches='tight')
plt.show()
```

### 模式：跨组比较

```python
# Compare distributions by category
categories = df.category.unique()

fig, axes = plt.subplots(len(categories), 2,
                         figsize=(12, 4 * len(categories)))

for idx, cat in enumerate(categories):
    df.select(df.category == cat, name=f'cat_{cat}')

    # 1D histogram
    df.plot1d(df.value, selection=f'cat_{cat}',
              ax=axes[idx, 0], show=False)
    axes[idx, 0].set_title(f'Category {cat} - Distribution')

    # 2D plot
    df.plot(df.x, df.y, selection=f'cat_{cat}',
            ax=axes[idx, 1], show=False)
    axes[idx, 1].set_title(f'Category {cat} - X vs Y')

plt.tight_layout()
plt.show()
```

### 模式：时间序列可视化

```python
# Aggregate by time bins
df['year'] = df.timestamp.dt.year
df['month'] = df.timestamp.dt.month

# Plot time series
monthly_sales = df.groupby(['year', 'month']).agg({'sales': 'sum'})

plt.figure(figsize=(14, 6))
plt.plot(range(len(monthly_sales)), monthly_sales['sales'])
plt.xlabel('Time Period')
plt.ylabel('Sales')
plt.title('Sales Over Time')
plt.grid(alpha=0.3)
plt.show()
```

## 与其他集成库

### 交互性绘图

```python
import plotly.graph_objects as go

# Get data from Vaex
counts = df.count(binby=[df.x, df.y], shape=(100, 100))

# Create plotly figure
fig = go.Figure(data=go.Heatmap(z=counts.T))
fig.update_layout(title='Interactive Heatmap')
fig.show()
```

### Seaborn 样式

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Use seaborn styling
sns.set_style('darkgrid')
sns.set_palette('husl')

df.plot1d(df.value)
plt.show()
```

## 最佳实践

1. **使用适当的形状** - 平衡分辨率和性能（256-512 用于探索，1024+ 用于发布）
2. **应用合理的限制** - 使用基于百分位数的限制（“99%”、“99.7%”）来处理异常值
3. **明智地选择色标** - 对数标度适用于大范围计数，线性适用于统一数据
4. **利用选择** - 比较子集而不创建新的 DataFrames
5. **缓存聚合** - 如果创建多个相似的图
6，则计算一次。 **使用矢量格式进行发布** - 对于可缩放图形，另存为 PDF 或 SVG 
7. **避免采样** - Vaex 可视化使用所有数据，无需采样

## 故障排除

### 问题：空图或稀疏图

```python
# Problem: Limits don't match data range
df.plot(df.x, df.y, limits=[[0, 10], [0, 10]])

# Solution: Use automatic limits
df.plot(df.x, df.y, limits='minmax')
df.plot(df.x, df.y, limits='99%')
```

### 问题：绘图太Slow

```python
# Problem: Too high resolution
df.plot(df.x, df.y, shape=(2048, 2048))

# Solution: Reduce shape
df.plot(df.x, df.y, shape=(512, 512))
```

### 问题：看不到低密度区域

```python
# Problem: Linear scale overwhelmed by high-density areas
df.plot(df.x, df.y, f='identity')

# Solution: Use logarithmic scale
df.plot(df.x, df.y, f='log')
```

## 相关资源

- 有关数据聚合：请参阅 `data_processing.md`
- 有关性能优化：请参阅`performance.md`
  - 有关 DataFrame 基础知识：请参阅 `core_dataframes.md`
