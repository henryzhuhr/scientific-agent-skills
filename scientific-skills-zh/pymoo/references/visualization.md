# Pymoo可视化参考

pymoo中可视化功能的综合参考。

## 概述

Pymoo提供了八种可视化类型用于分析多目标优化结果。所有绘图都包装 matplotlib 并接受标准 matplotlib 关键字参数进行自定义。

## 核心可视化类型

### 1. 散点图
* *用途：** 可视化 2D、3D 或更高维度的目标空间
* *最适合：** 帕累托前沿、解分布、算法比较

* *用法：**
```python
from pymoo.visualization.scatter import Scatter

# 2D scatter plot
plot = Scatter()
plot.add(result.F, color="red", label="Algorithm A")
plot.add(ref_pareto_front, color="black", alpha=0.3, label="True PF")
plot.show()

# 3D scatter plot
plot = Scatter(title="3D Pareto Front")
plot.add(result.F)
plot.show()
```

* *参数：**
- `title`：绘图标题
- `figsize`：图形尺寸元组（宽度，高度）
- `legend`：显示图例（默认：True）
- `labels`：轴标签列表

* *添加方法参数：**
- `color`：颜色规格
- `alpha`：透明度（0-1）
- `s`：标记尺寸
- `marker`：标记样式
- `label`：图例标签

* *N维投影：**
对于> 3个目标，自动创建散点图矩阵

### 2. 平行坐标图(PCP)
* *用途：**比较多个目标的多个解决方案
* *最适合：**多目标问题，比较算法性能

* *机制：**每个垂直轴代表一个目标，线条连接每个目标的目标值解

* *用法：**
```python
from pymoo.visualization.pcp import PCP

plot = PCP()
plot.add(result.F, color="blue", alpha=0.5)
plot.add(reference_set, color="red", alpha=0.8)
plot.show()
```

* *参数：**
- `title`：图标题
- `figsize`：图形尺寸
- `labels`：目标标签
- `bounds`：每个目标的标准化范围（最小，最大）
- `normalize_each_axis`：每个轴标准化为[0,1]（默认值：True）

* *最佳实践：**
- 针对不同目标尺度进行标准化
- 使用透明度进行重叠线
- 为了清晰度限制解决方案的数量（<1000）

### 3. 热图
* *用途：**显示解密度和分布模式
* *最适合：**了解解聚类，识别差距

* *用法：**
```python
from pymoo.visualization.heatmap import Heatmap

plot = Heatmap(title="Solution Density")
plot.add(result.F)
plot.show()
```

* *参数：**
- `bins`：箱数每个维度（默认：20）
- `cmap`：颜色图名称（例如，“viridis”、“plasma”、“hot”）
- `norm`：归一化方法

* *解释：**
- 明亮区域：高溶液密度
- 黑暗区域：很少或没有解决方案
- 揭示分布均匀性

### 4.花瓣图
* *用途：**多个目标的径向表示
* *最适合：**比较各个目标的单个解决方案

* *结构：**每个“花瓣”代表一个目标，长度表示目标值

* *用法：**
```python
from pymoo.visualization.petal import Petal

plot = Petal(title="Solution Comparison", bounds=[min_vals, max_vals])
plot.add(result.F[0], color="blue", label="Solution 1")
plot.add(result.F[1], color="red", label="Solution 2")
plot.show()
```

* *参数：**
- `bounds`：标准化每个目标的[最小值，最大值]
- `labels`：目标名称
- `reverse`：反转特定目标（用于最小化显示）

* *用例：**
- 在几个解决方案之间做出决策
- 向利益相关者呈现权衡

### 5.雷达图
* *目的：**多标准性能配置文件
* *最适合：**比较解特性

* *类似于：**花瓣图，但具有连接的顶点

* *用法：**
```python
from pymoo.visualization.radar import Radar

plot = Radar(bounds=[min_vals, max_vals])
plot.add(solution_A, label="Design A")
plot.add(solution_B, label="Design B")
plot.show()
```

### 6.Radviz
* *用途：**降维可视化
* *最适合：**高维数据探索、模式识别

* *机制：**将高维点投影到2D圆上，尺寸锚定在周长上

* *用法：**
```python
from pymoo.visualization.radviz import Radviz

plot = Radviz(title="High-dimensional Solution Space")
plot.add(result.F, color="blue", s=30)
plot.show()
```

* *参数：**
- `endpoint_style`：锚点可视化
- `labels`：维度标签

* *解释：**
- 锚点附近的点：该维度中的高值
- 中心点：跨维度平衡
- 集群：类似的解决方案

### 7. 星坐标
* *用途：**替代高维可视化
* *最适合：**比较多维数据集

* *机制：**每个维度作为从原点开始的轴，基于点绘制值

* *用法：**
```python
from pymoo.visualization.star_coordinate import StarCoordinate

plot = StarCoordinate()
plot.add(result.F)
plot.show()
```

* *参数：**
- `axis_style`：轴外观
- `axis_extension`：轴长度超出最大值
- `labels`：尺寸标签

### 8.视频/动画
* *用途：**显示一段时间内的优化进度
* *最适合：**了解收敛行为、演示

* *用法：**
```python
from pymoo.visualization.video import Video

# Create animation from algorithm history
anim = Video(result.algorithm)
anim.save("optimization_progress.mp4")
```

* *要求：**
- 算法必须存储历史记录（最小化时使用`save_history=True`）
- 安装用于视频导出的ffmpeg

* *自定义：**
- 帧速率
- 每帧的绘图类型
- 叠加信息（生成、超体积等）

## 高级功能

### 多数据集叠加

所有绘图类型都支持添加多个数据集：

```python
plot = Scatter(title="Algorithm Comparison")
plot.add(nsga2_result.F, color="red", alpha=0.5, label="NSGA-II")
plot.add(nsga3_result.F, color="blue", alpha=0.5, label="NSGA-III")
plot.add(true_pareto_front, color="black", linewidth=2, label="True PF")
plot.show()
```

### 自定义样式

Pass matplotlib kwargs直接：

```python
plot = Scatter(
    title="My Results",
    figsize=(10, 8),
    tight_layout=True
)
plot.add(
    result.F,
    color="red",
    marker="o",
    s=50,
    alpha=0.7,
    edgecolors="black",
    linewidth=0.5
)
```

### 标准化

将目标标准化为[0,1]以进行公平比较：

```python
plot = PCP(normalize_each_axis=True, bounds=[min_bounds, max_bounds])
```

### 保存到文件

保存图而不是显示：

```python
plot = Scatter()
plot.add(result.F)
plot.save("my_plot.png", dpi=300)
```

## 可视化选择指南

* *选择可视化基于：**

|问题类型 |主要情节|次要情节|
|-------------|-------------|----------------|
| 2-目标 |分散|热图|
| 3-目标 | 3D 散点 |平行坐标|
|多目标 (4-10) |平行坐标|拉维兹|
|多目标 (>10) |拉维兹 |星坐标|
|解决方案比较 |花瓣/雷达 |平行坐标|
|算法收敛 |视频 |分散（最终）|
|分布分析|热图 |分散|

* *组合：**
- 散点图 + 热图：总体分布 + 密度
- PCP + 花瓣：种群概览 + 个体解决方案
- 散点图 + 视频：最终结果 + 收敛过程

## 常见可视化工作流程

### 1. 算法比较
```python
from pymoo.visualization.scatter import Scatter

plot = Scatter(title="Algorithm Comparison on ZDT1")
plot.add(ga_result.F, color="blue", label="GA", alpha=0.6)
plot.add(nsga2_result.F, color="red", label="NSGA-II", alpha=0.6)
plot.add(zdt1.pareto_front(), color="black", label="True PF")
plot.show()
```

### 2. 多目标分析
```python
from pymoo.visualization.pcp import PCP

plot = PCP(
    title="5-objective DTLZ2 Results",
    labels=["f1", "f2", "f3", "f4", "f5"],
    normalize_each_axis=True
)
plot.add(result.F, alpha=0.3)
plot.show()
```

### 3. 决策
```python
from pymoo.visualization.petal import Petal

# Compare top 3 solutions
candidates = result.F[:3]

plot = Petal(
    title="Top 3 Solutions",
    bounds=[result.F.min(axis=0), result.F.max(axis=0)],
    labels=["Cost", "Weight", "Efficiency", "Safety"]
)
for i, sol in enumerate(candidates):
    plot.add(sol, label=f"Solution {i+1}")
plot.show()
```

### 4. 收敛可视化
```python
from pymoo.optimize import minimize

# Enable history
result = minimize(
    problem,
    algorithm,
    ('n_gen', 200),
    seed=1,
    save_history=True,
    verbose=False
)

# Create convergence plot
from pymoo.visualization.scatter import Scatter

plot = Scatter(title="Convergence Over Generations")
for gen in [0, 50, 100, 150, 200]:
    F = result.history[gen].opt.get("F")
    plot.add(F, alpha=0.5, label=f"Gen {gen}")
plot.show()
```

## 提示和最佳实践

1. **使用适当的 alpha：** 对于重叠点，请使用 `alpha=0.3-0.7`
2. **标准化目标：**不同的尺度？标准化以获得公平的可视化
3. **标签清晰：** 始终提供有意义的标签和图例
4. **限制数据点：** >10000 点？示例或使用热图
5. **配色方案：** 使用色盲友好的调色板
6. **保存高分辨率：** 使用 `dpi=300` 来发布 
7. **交互式探索：**考虑交互式绘图
8的plotly。 **组合视图：** 显示多个视角进行综合分析
