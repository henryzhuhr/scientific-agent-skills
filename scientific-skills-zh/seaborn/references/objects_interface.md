# Seaborn 对象接口

`seaborn.objects` 接口提供了一个现代的声明式 API，用于通过组合构建可视化。本指南涵盖了 seaborn 0.12+ 中引入的完整对象接口。

## 核心概念

对象接口将**您想要显示的内容**（数据和映射）与**如何显示它**（标记、统计数据和移动）分开。通过以下方式构建绘图：

1. 使用数据和美学映射 
2 创建 `Plot` 对象。使用 `.add()` 组合标记和统计变换 
3 添加图层。定制`.scale()`、`.label()`、`.limit()`、`.theme()`等
4. 使用`.show()`或`.save()`

进行渲染##基本用法

```python
from seaborn import objects as so
import pandas as pd

# Create plot with data and mappings
p = so.Plot(data=df, x='x_var', y='y_var')

# Add mark (visual representation)
p = p.add(so.Dot())

# Display (automatic in Jupyter)
p.show()
```

## 绘图类

`Plot`类是对象接口的基础。

### 初始化

```python
so.Plot(data=None, x=None, y=None, color=None, alpha=None,
        fill=None, fillalpha=None, fillcolor=None, marker=None,
        pointsize=None, stroke=None, text=None, **variables)
```

* *参数：**
- `data` - 数据帧或数据向量字典
- `x, y` - 位置变量
- `color` - 颜色变量编码
- `alpha` - 透明度变量
- `marker` - 标记形状变量
- `pointsize` - 点大小变量
- `stroke` - 线宽变量
- `text` - 文本标签变量
- `**variables` - 使用属性名称的附加映射

* *示例：**
```python
# Basic mapping
so.Plot(df, x='total_bill', y='tip')

# Multiple mappings
so.Plot(df, x='total_bill', y='tip', color='day', pointsize='size')

# All variables in Plot
p = so.Plot(df, x='x', y='y', color='cat')
p.add(so.Dot())  # Uses all mappings

# Some variables in add()
p = so.Plot(df, x='x', y='y')
p.add(so.Dot(), color='cat')  # Only this layer uses color
```

### 方法

#### add()

使用标记向绘图添加一个图层和可选的统计/移动。

```python
Plot.add(mark, *transforms, orient=None, legend=True, data=None,
         **variables)
```

* *参数：**
- `mark` - 标记定义视觉表示的对象
- `*transforms` - 用于数据转换的统计和/或移动对象
- `orient` - “x”、“y”或“v”/“h”表示方向
- `legend` - 包含在图例中（真/假）
- `data` - 覆盖该层的数据
- `**variables` - 覆盖或添加变量映射

* *示例：**
```python
# Simple mark
p.add(so.Dot())

# Mark with stat
p.add(so.Line(), so.PolyFit(order=2))

# Mark with multiple transforms
p.add(so.Bar(), so.Agg(), so.Dodge())

# Layer-specific mappings
p.add(so.Dot(), color='category')
p.add(so.Line(), so.Agg(), color='category')

# Layer-specific data
p.add(so.Dot())
p.add(so.Line(), data=summary_df)
```

#### facet()

从分类变量创建子图。

```python
Plot.facet(col=None, row=None, order=None, wrap=None)
```

* *参数：**
- `col` - 列面的变量
- `row` - 行面的变量
- `order` - 带面的字典订单（键：变量名称）
- `wrap` - 在这么多列之后换行

* *示例：**
```python
p.facet(col='time', row='sex')
p.facet(col='category', wrap=3)
p.facet(col='day', order={'day': ['Thur', 'Fri', 'Sat', 'Sun']})
```

#### pair()

为多个创建成对子图变量.

```python
Plot.pair(x=None, y=None, wrap=None, cross=True)
```

* *参数：**
- `x` - x 轴配对的变量
- `y` - y 轴配对的变量（如果没有，则使用x）
- `wrap` - 在这么多列之后换行
- `cross` - 包括所有 x/y 组合（相对于仅对角线）

* *示例：**
```python
# Pairs of all variables
p = so.Plot(df).pair(x=['a', 'b', 'c'])
p.add(so.Dot())

# Rectangular grid
p = so.Plot(df).pair(x=['a', 'b'], y=['c', 'd'])
p.add(so.Dot(), alpha=0.5)
```

#### scale()

自定义数据如何映射到视觉properties.

```python
Plot.scale(**scales)
```

* *参数：**带有属性名称和Scale对象的关键字参数

* *示例：**
```python
p.scale(
    x=so.Continuous().tick(every=5),
    y=so.Continuous().label(like='{x:.1f}'),
    color=so.Nominal(['#1f77b4', '#ff7f0e', '#2ca02c']),
    pointsize=(5, 10)  # Shorthand for range
)
```

#### limit()

设置轴limit.

```python
Plot.limit(x=None, y=None)
```

* *参数：**
- `x` - x 轴的（最小值，最大值）的元组
- `y` - 的（最小值，最大值）的元组y-axis

* *示例：**
```python
p.limit(x=(0, 100), y=(0, 50))
```

#### label()

设置轴标签和标题。

```python
Plot.label(x=None, y=None, color=None, title=None, **labels)
```

* *参数：** 带有属性名称和标签的关键字参数strings

* *示例：**
```python
p.label(
    x='Total Bill ($)',
    y='Tip Amount ($)',
    color='Day of Week',
    title='Restaurant Tips Analysis'
)
```

#### 主题()

应用matplotlib样式设置。

```python
Plot.theme(config, **kwargs)
```

* *参数：**
- `config` - rcParams 字典或 seaborn 主题字典
- `**kwargs` - 单个 rcParams

* *示例：**
```python
# Seaborn theme
p.theme({**sns.axes_style('whitegrid'), **sns.plotting_context('talk')})

# Custom rcParams
p.theme({'axes.facecolor': 'white', 'axes.grid': True})

# Individual parameters
p.theme(axes_facecolor='white', font_scale=1.2)
```

#### 布局()

Configure子图布局。

```python
Plot.layout(size=None, extent=None, engine=None)
```

* *参数：**
- `size` - （宽度，高度）以英寸为单位
- `extent` - 子图的（左、下、右、上）
- `engine` - “紧”、“约束”或无

* *示例：**
```python
p.layout(size=(10, 6), engine='constrained')
```

#### share()

控制跨面共享轴。

```python
Plot.share(x=None, y=None)
```

* *参数：**
- `x` - 共享 x 轴：True、False 或“col”/“row” 
- `y` - 共享 y 轴：True、False 或"col"/"row"

* *示例：**
```python
p.share(x=True, y=False)  # Share x across all, independent y
p.share(x='col')  # Share x within columns only
```

#### on()

在现有 matplotlib 图形或轴上绘图。

```python
Plot.on(target)
```

* *参数：**
- `target` - matplotlib 图形或轴对象

* *示例：**
```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(10, 10))
so.Plot(df, x='x', y='y').add(so.Dot()).on(axes[0, 0])
so.Plot(df, x='x', y='z').add(so.Line()).on(axes[0, 1])
```

#### show()

渲染并显示plot.

```python
Plot.show(**kwargs)
```

* *参数：**传递给`matplotlib.pyplot.show()`

#### save()

将绘图保存到file.

```python
Plot.save(filename, **kwargs)
```

* *参数：**
- `filename` - 输出文件名
- `**kwargs` - 传递到`matplotlib.figure.Figure.savefig()`

* *示例：**
```python
p.save('plot.png', dpi=300, bbox_inches='tight')
p.save('plot.pdf')
```

## 标记对象

标记定义数据的可视化表示方式。

### Dot

个人的点/标记观测值.

```python
so.Dot(artist_kws=None, **kwargs)
```

* *属性：**
- `color` - 填充颜色
- `alpha` - 透明度
- `fillcolor` - 替代颜色属性
- `fillalpha` - 替代 alpha 属性
- `edgecolor` - 边缘颜色
- `edgealpha` - 边缘透明度
- `edgewidth` - 边缘线宽度
- `marker` - 标记样式
- `pointsize` - 标记尺寸
- `stroke` - 边缘宽度

* *示例：**
```python
so.Plot(df, x='x', y='y').add(so.Dot(color='blue', pointsize=10))
so.Plot(df, x='x', y='y', color='cat').add(so.Dot(alpha=0.5))
```

### Line

连接线观测值.

```python
so.Line(artist_kws=None, **kwargs)
```

* *属性：**
- `color` - 线条颜色
- `alpha` - 透明度
- `linewidth` - 线宽
- `linestyle` - 线条样式（“-”、“--”、“-.”、“:”）
- `marker` - 数据点处的标记
- `pointsize` - 标记尺寸
- `edgecolor` - 标记边缘颜色
- `edgewidth` - 标记边缘宽度

* *示例：**
```python
so.Plot(df, x='x', y='y').add(so.Line())
so.Plot(df, x='x', y='y', color='cat').add(so.Line(linewidth=2))
```

### 路径

与线类似，但按数据顺序连接点（不按 x 排序）。

```python
so.Path(artist_kws=None, **kwargs)
```

属性相同如`Line`.

* *示例：**
```python
# For trajectories, loops, etc.
so.Plot(trajectory_df, x='x', y='y').add(so.Path())
```

### Bar

矩形条.

```python
so.Bar(artist_kws=None, **kwargs)
```

* *属性：**
- `color` - 填充颜色
- `alpha` - 透明度
- `edgecolor` - 边缘颜色
- `edgealpha` - 边缘透明度
- `edgewidth` - 边缘线宽度
- `width` - 条形宽度（数据单位）

* *示例：**
```python
so.Plot(df, x='category', y='value').add(so.Bar())
so.Plot(df, x='x', y='y').add(so.Bar(color='#1f77b4', width=0.5))
```

### 条形

多个条形（用于有错误的聚合数据） 

```python
so.Bars(artist_kws=None, **kwargs)
```

属性与`Bar`相同。与 `Agg()` 或 `Est()` stats 一起使用。

* *示例：**
```python
so.Plot(df, x='category', y='value').add(so.Bars(), so.Agg())
```

### Area

线与线之间的填充区域基线.

```python
so.Area(artist_kws=None, **kwargs)
```

* *属性：**
- `color` - 填充颜色
- `alpha` - 透明度
- `edgecolor` - 边缘颜色
- `edgealpha` - 边缘透明度
- `edgewidth` - 边缘线宽度
- `baseline` - 基线值（默认：0）

* *示例：**
```python
so.Plot(df, x='x', y='y').add(so.Area(alpha=0.3))
so.Plot(df, x='x', y='y', color='cat').add(so.Area())
```

### Band

两条线之间的填充带（用于范围/间隔）。

```python
so.Band(artist_kws=None, **kwargs)
```

属性与`Area`相同。需要 `ymin` 和 `ymax` 映射或与 `Est()` stat.

 一起使用**示例：**
```python
so.Plot(df, x='x', ymin='lower', ymax='upper').add(so.Band())
so.Plot(df, x='x', y='y').add(so.Band(), so.Est())
```

### Range

Line 在端点处带有标记（对于

```python
so.Range(artist_kws=None, **kwargs)
```

* *属性：**
- `color` - 线条和标记颜色
- `alpha` - 透明度
- `linewidth` - 线条宽度
- `marker` - 端点处的标记样式
- `pointsize` - 标记尺寸
- `edgewidth` - 标记边缘宽度

* *示例：**
```python
so.Plot(df, x='x', y='y').add(so.Range(), so.Est())
```

### Dash

水平/垂直短线（用于分布标记）。

```python
so.Dash(artist_kws=None, **kwargs)
```

* *属性：**
- `color` - 线条颜色
- `alpha` - 透明度
- `linewidth` - 线条宽度
- `width` - 虚线长度（数据单位）

* *示例：**
```python
so.Plot(df, x='category', y='value').add(so.Dash())
```

### Text

数据点处的文本标签。

```python
so.Text(artist_kws=None, **kwargs)
```

* *属性：**
- `color` - 文本颜色
- `alpha` - 透明度
- `fontsize` - 字体大小
- `halign` - 水平对齐： "left", "center", "right"
- `valign` - 垂直对齐方式：“bottom”、“center”、“top”
- `offset` - 从点 

 的 (x, y)偏移需要 `text` mapping.

* *示例：**
```python
so.Plot(df, x='x', y='y', text='label').add(so.Text())
so.Plot(df, x='x', y='y', text='value').add(so.Text(fontsize=10, offset=(0, 5)))
```

## Stat Objects

Stats 在渲染之前转换数据。用`.add()`.

### Agg

按组聚合观察值组成。

```python
so.Agg(func='mean')
```

* *参数：**
- `func` - 聚合函数：“mean”、“median”、 "sum"、"min"、"max"、"count" 或 callable

* *示例：**
```python
so.Plot(df, x='category', y='value').add(so.Bar(), so.Agg('mean'))
so.Plot(df, x='x', y='y', color='group').add(so.Line(), so.Agg('median'))
```

### Est

E 估计有误差的集中趋势间隔.

```python
so.Est(func='mean', errorbar=('ci', 95), n_boot=1000, seed=None)
```

* *参数：**
- `func` - 估计器：“mean”、“median”、“sum”或可调用
- `errorbar` - 错误表示：
  - `("ci", level)` - 通过 bootstrap 得出的置信区间
  - `("pi", level)` - 百分位数区间
  - `("se", scale)` - 按因子缩放的标准误差
  - `"sd"` - 标准差
- `n_boot` - Bootstrap 迭代
- `seed` - 随机种子

* *示例：**
```python
so.Plot(df, x='category', y='value').add(so.Bar(), so.Est())
so.Plot(df, x='x', y='y').add(so.Line(), so.Est(errorbar='sd'))
so.Plot(df, x='x', y='y').add(so.Line(), so.Est(errorbar=('ci', 95)))
so.Plot(df, x='x', y='y').add(so.Band(), so.Est())
```

### Hist

Bin 观测值和count/aggregate.

```python
so.Hist(stat='count', bins='auto', binwidth=None, binrange=None,
        common_norm=True, common_bins=True, cumulative=False)
```

* *参数：**
- `stat` - “计数”、“密度”、“概率”、“百分比”、“频率”
- `bins` - 箱数、箱方法或边
- `binwidth` - 箱的宽度
- `binrange` - 分箱的（最小，最大）范围
- `common_norm` - 跨组一起标准化
- `common_bins` - 对所有组使用相同的箱groups
- `cumulative` - 累积直方图

* *示例：**
```python
so.Plot(df, x='value').add(so.Bars(), so.Hist())
so.Plot(df, x='value').add(so.Bars(), so.Hist(bins=20, stat='density'))
so.Plot(df, x='value', color='group').add(so.Area(), so.Hist(cumulative=True))
```

### KDE

核密度估计。

```python
so.KDE(bw_method='scott', bw_adjust=1, gridsize=200,
       cut=3, cumulative=False)
```

* *参数：**
- `bw_method` - 带宽方法：“scott”、“silverman”或标量
- `bw_adjust` - 带宽乘数
- `gridsize` - 密度分辨率曲线
- `cut` - 超出数据范围的扩展（以带宽为单位）
- `cumulative` - 累积密度

* *示例：**
```python
so.Plot(df, x='value').add(so.Line(), so.KDE())
so.Plot(df, x='value', color='group').add(so.Area(alpha=0.5), so.KDE())
so.Plot(df, x='x', y='y').add(so.Line(), so.KDE(bw_adjust=0.5))
```

### Count

Count group.

```python
so.Count()
```

* *示例：**
```python
so.Plot(df, x='category').add(so.Bar(), so.Count())
```

### PolyFit

多项式回归fit.

```python
so.PolyFit(order=1)
```

* *参数：**
- `order` - 多项式阶数（1 = 线性，2 = 二次，等）

* *示例：**
```python
so.Plot(df, x='x', y='y').add(so.Dot())
so.Plot(df, x='x', y='y').add(so.Line(), so.PolyFit(order=2))
```

### Perc

计算百分位数。

```python
so.Perc(k=5, method='linear')
```

* *参数：**
- `k` - 百分位间隔数
- `method` - 插值方法

* *示例：**
```python
so.Plot(df, x='x', y='y').add(so.Band(), so.Perc())
```

## 移动对象

移动调整位置以解决重叠或创建特定的位置布局.

### Dodge

并排移动位置。

```python
so.Dodge(empty='keep', gap=0)
```

* *参数：**
- `empty` - 如何处理空组：“keep”、“drop”、“fill”
- `gap` - 躲避元素之间的间隙（比例）

* *示例：**
```python
so.Plot(df, x='category', y='value', color='group').add(so.Bar(), so.Dodge())
so.Plot(df, x='cat', y='val', color='hue').add(so.Dot(), so.Dodge(gap=0.1))
```

### Stack

堆叠标记

```python
so.Stack()
```

* *示例：**
```python
so.Plot(df, x='x', y='y', color='category').add(so.Bar(), so.Stack())
so.Plot(df, x='x', y='y', color='group').add(so.Area(), so.Stack())
```

### Jitter

添加随机噪声

```python
so.Jitter(width=None, height=None, seed=None)
```

* *参数：**
- `width` - x 方向抖动（数据单位或比例）
- `height` - y 方向抖动
- `seed` -随机种子

* *示例：**
```python
so.Plot(df, x='category', y='value').add(so.Dot(), so.Jitter())
so.Plot(df, x='cat', y='val').add(so.Dot(), so.Jitter(width=0.2))
```

### Shift

按恒定量平移位置。

```python
so.Shift(x=0, y=0)
```

* *参数：**
- `x` - x 方向移动（数据单位）
- `y` - y 方向移动

* *示例：**
```python
so.Plot(df, x='x', y='y').add(so.Dot(), so.Shift(x=1))
```

### Norm

标准化值。

```python
so.Norm(func='max', where=None, by=None, percent=False)
```

* *参数：**
- `func` - 标准化：“max”、“sum”、“area”或可调用
- `where` - 适用于哪个轴：“x”、“y”或无
- `by` - 对单独标准化的变量进行分组
- `percent` - 显示为百分比

* *示例：**
```python
so.Plot(df, x='x', y='y', color='group').add(so.Area(), so.Norm())
```

## 缩放对象

缩放控制数据值如何映射到视觉属性。

### 连续

用于数值数据。

```python
so.Continuous(values=None, norm=None, trans=None)
```

* *方法：**
- `.tick(at=None, every=None, between=None, minor=None)` - 配置刻度
- `.label(like=None, base=None, unit=None)` - 格式标签

* *参数：**
- `values` - 显式值范围（最小值、最大值）
- `norm` - 归一化函数
- `trans` - 转换：“log”、“sqrt”、“symlog”、“logit”、 “pow10”，或可调用

* *示例：**
```python
p.scale(
    x=so.Continuous().tick(every=10),
    y=so.Continuous(trans='log').tick(at=[1, 10, 100]),
    color=so.Continuous(values=(0, 1)),
    pointsize=(5, 20)  # Shorthand for Continuous range
)
```

### 标称

用于分类数据。

```python
so.Nominal(values=None, order=None)
```

* *参数：**
- `values` - 显式值（例如颜色、标记）
- `order` - 类别顺序

* *示例：**
```python
p.scale(
    color=so.Nominal(['#1f77b4', '#ff7f0e', '#2ca02c']),
    marker=so.Nominal(['o', 's', '^']),
    x=so.Nominal(order=['Low', 'Medium', 'High'])
)
```

### Temporal

对于日期时间data.

```python
so.Temporal(values=None, trans=None)
```

* *方法：**
- `.tick(every=None, between=None)` - 配置刻度
- `.label(concise=False)` - 格式标签

* *示例：**
```python
p.scale(x=so.Temporal().tick(every=('month', 1)).label(concise=True))
```

## 完整示例

### 带统计信息的分层图

```python
(
    so.Plot(df, x='total_bill', y='tip', color='time')
    .add(so.Dot(), alpha=0.5)
    .add(so.Line(), so.PolyFit(order=2))
    .scale(color=so.Nominal(['#1f77b4', '#ff7f0e']))
    .label(x='Total Bill ($)', y='Tip ($)', title='Tips Analysis')
    .theme({**sns.axes_style('whitegrid')})
)
```

### 多面分布

```python
(
    so.Plot(df, x='measurement', color='treatment')
    .facet(col='timepoint', wrap=3)
    .add(so.Area(alpha=0.5), so.KDE())
    .add(so.Dot(), so.Jitter(width=0.1), y=0)
    .scale(x=so.Continuous().tick(every=5))
    .label(x='Measurement (units)', title='Treatment Effects Over Time')
    .share(x=True, y=False)
)
```

### 分组条形图

```python
(
    so.Plot(df, x='category', y='value', color='group')
    .add(so.Bar(), so.Agg('mean'), so.Dodge())
    .add(so.Range(), so.Est(errorbar='se'), so.Dodge())
    .scale(color=so.Nominal(order=['A', 'B', 'C']))
    .label(y='Mean Value', title='Comparison by Category and Group')
)
```

### 复杂多层

```python
(
    so.Plot(df, x='date', y='value')
    .add(so.Dot(color='gray', pointsize=3), alpha=0.3)
    .add(so.Line(color='blue', linewidth=2), so.Agg('mean'))
    .add(so.Band(color='blue', alpha=0.2), so.Est(errorbar=('ci', 95)))
    .facet(col='sensor', row='location')
    .scale(
        x=so.Temporal().label(concise=True),
        y=so.Continuous().tick(every=10)
    )
    .label(
        x='Date',
        y='Measurement',
        title='Sensor Measurements by Location'
    )
    .layout(size=(12, 8), engine='constrained')
)
```

## 从函数接口迁移

### 散点图

* *函数接口：**
```python
sns.scatterplot(data=df, x='x', y='y', hue='category', size='value')
```

* *对象接口：**
```python
so.Plot(df, x='x', y='y', color='category', pointsize='value').add(so.Dot())
```

### 带有CI

* *函数的线图接口：**
```python
sns.lineplot(data=df, x='time', y='measurement', hue='group', errorbar='ci')
```

* *对象接口：**
```python
(
    so.Plot(df, x='time', y='measurement', color='group')
    .add(so.Line(), so.Est())
)
```

### 直方图

* *函数接口：**
```python
sns.histplot(data=df, x='value', hue='category', stat='density', kde=True)
```

* *对象接口：**
```python
(
    so.Plot(df, x='value', color='category')
    .add(so.Bars(), so.Hist(stat='density'))
    .add(so.Line(), so.KDE())
)
```

### 带误差线的条形图

* *函数接口：**
```python
sns.barplot(data=df, x='category', y='value', hue='group', errorbar='ci')
```

* *对象界面：**
```python
(
    so.Plot(df, x='category', y='value', color='group')
    .add(so.Bar(), so.Agg(), so.Dodge())
    .add(so.Range(), so.Est(), so.Dodge())
)
```

## 提示和最佳实践

1. **方法链接**：每个方法返回一个新的 Plot 对象，实现流畅的链接
2. **图层组合**：组合多个`.add()`调用来叠加不同的标记
3. **变换顺序**：在`.add(mark, stat, move)`中，先统计，然后移动
4. **变量优先级**：特定于层的映射覆盖地块级映射
5. **缩放快捷键**：使用元组进行简单范围：`color=(min, max)` 与全尺寸对象
6. **Jupyter 渲染**：返回时自动渲染图；使用`.show()`，否则使用
7. **节省**：使用`.save()`而不是`plt.savefig()`进行正确处理
8. **Matplotlib 访问**：使用 `.on(ax)` 与 matplotlib 人物 
 集成
