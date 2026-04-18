# Matplotlib 绘图类型指南

matplotlib 中不同绘图类型的综合指南，包含示例和用例。

## 1. 线图

* *用例：** 时间序列、连续数据、趋势、函数可视化

### 基本线图绘图
```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, linewidth=2, label='Data')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.legend()
```

### 多行
```python
ax.plot(x, y1, label='Dataset 1', linewidth=2)
ax.plot(x, y2, label='Dataset 2', linewidth=2, linestyle='--')
ax.plot(x, y3, label='Dataset 3', linewidth=2, linestyle=':')
ax.legend()
```

### 带标记的行
```python
ax.plot(x, y, marker='o', markersize=8, linestyle='-',
        linewidth=2, markerfacecolor='red', markeredgecolor='black')
```

### 步骤Plot
```python
ax.step(x, y, where='mid', linewidth=2, label='Step function')
# where options: 'pre', 'post', 'mid'
```

### 误差线
```python
ax.errorbar(x, y, yerr=error, fmt='o-', linewidth=2,
            capsize=5, capthick=2, label='With uncertainty')
```

## 2. 散点图

* *用例：** 相关性、变量之间的关系、聚类、异常值

### 基本散点图
```python
ax.scatter(x, y, s=50, alpha=0.6)
```

### 大小和颜色的散点图
```python
scatter = ax.scatter(x, y, s=sizes*100, c=colors,
                     cmap='viridis', alpha=0.6, edgecolors='black')
plt.colorbar(scatter, ax=ax, label='Color variable')
```

### 分类散点图
```python
for category in categories:
    mask = data['category'] == category
    ax.scatter(data[mask]['x'], data[mask]['y'],
               label=category, s=50, alpha=0.7)
ax.legend()
```

## 3. 条形图图表

* *使用案例：**分类比较、离散数据、计数

### 垂直条形图
```python
ax.bar(categories, values, color='steelblue',
       edgecolor='black', linewidth=1.5)
ax.set_ylabel('Values')
```

### 水平条形图
```python
ax.barh(categories, values, color='coral',
        edgecolor='black', linewidth=1.5)
ax.set_xlabel('Values')
```

### 分组条形图图表
```python
x = np.arange(len(categories))
width = 0.35

ax.bar(x - width/2, values1, width, label='Group 1')
ax.bar(x + width/2, values2, width, label='Group 2')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
```

### 堆叠条形图
```python
ax.bar(categories, values1, label='Part 1')
ax.bar(categories, values2, bottom=values1, label='Part 2')
ax.bar(categories, values3, bottom=values1+values2, label='Part 3')
ax.legend()
```

### 带误差条的条形图
```python
ax.bar(categories, values, yerr=errors, capsize=5,
       color='steelblue', edgecolor='black')
```

### 带误差条的条形图模式
```python
bars1 = ax.bar(x - width/2, values1, width, label='Group 1',
               color='white', edgecolor='black', hatch='//')
bars2 = ax.bar(x + width/2, values2, width, label='Group 2',
               color='white', edgecolor='black', hatch='\\\\')
```

## 4.直方图

* *用例：**分布、频率分析

### 基本直方图
```python
ax.hist(data, bins=30, edgecolor='black', alpha=0.7)
ax.set_xlabel('Value')
ax.set_ylabel('Frequency')
```

### 多重重叠直方图
```python
ax.hist(data1, bins=30, alpha=0.5, label='Dataset 1')
ax.hist(data2, bins=30, alpha=0.5, label='Dataset 2')
ax.legend()
```

### 标准化直方图（密度）
```python
ax.hist(data, bins=30, density=True, alpha=0.7,
        edgecolor='black', label='Empirical')

# Overlay theoretical distribution
from scipy.stats import norm
x = np.linspace(data.min(), data.max(), 100)
ax.plot(x, norm.pdf(x, data.mean(), data.std()),
        'r-', linewidth=2, label='Normal fit')
ax.legend()
```

### 2D 直方图（Hexbin）
```python
hexbin = ax.hexbin(x, y, gridsize=30, cmap='Blues')
plt.colorbar(hexbin, ax=ax, label='Counts')
```

### 2D直方图 (hist2d)
```python
h = ax.hist2d(x, y, bins=30, cmap='Blues')
plt.colorbar(h[3], ax=ax, label='Counts')
```

## 5. 箱形图和小提琴图

* *用例：** 统计分布、异常值检测、比较分布

### 箱形图Plot
```python
ax.boxplot([data1, data2, data3],
           labels=['Group A', 'Group B', 'Group C'],
           showmeans=True, meanline=True)
ax.set_ylabel('Values')
```

### 水平箱形图
```python
ax.boxplot([data1, data2, data3], vert=False,
           labels=['Group A', 'Group B', 'Group C'])
ax.set_xlabel('Values')
```

### 小提琴图
```python
parts = ax.violinplot([data1, data2, data3],
                      positions=[1, 2, 3],
                      showmeans=True, showmedians=True)
ax.set_xticks([1, 2, 3])
ax.set_xticklabels(['Group A', 'Group B', 'Group C'])
```

## 6. 热图

* *使用案例：** 矩阵数据、相关性、强度图

### 基本热图
```python
im = ax.imshow(matrix, cmap='coolwarm', aspect='auto')
plt.colorbar(im, ax=ax, label='Values')
ax.set_xlabel('X')
ax.set_ylabel('Y')
```

### 带注释的热图
```python
im = ax.imshow(matrix, cmap='coolwarm')
plt.colorbar(im, ax=ax)

# Add text annotations
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        text = ax.text(j, i, f'{matrix[i, j]:.2f}',
                       ha='center', va='center', color='black')
```

### 相关性矩阵
```python
corr = data.corr()
im = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)
plt.colorbar(im, ax=ax, label='Correlation')

# Set tick labels
ax.set_xticks(range(len(corr)))
ax.set_yticks(range(len(corr)))
ax.set_xticklabels(corr.columns, rotation=45, ha='right')
ax.set_yticklabels(corr.columns)
```

## 7. 等高线图

* *用例：** 2D 平面上的 3D 数据、地形、函数可视化

### 等高线
```python
contour = ax.contour(X, Y, Z, levels=10, cmap='viridis')
ax.clabel(contour, inline=True, fontsize=8)
plt.colorbar(contour, ax=ax)
```

### 填充轮廓
```python
contourf = ax.contourf(X, Y, Z, levels=20, cmap='viridis')
plt.colorbar(contourf, ax=ax)
```

### 组合轮廓
```python
contourf = ax.contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.8)
contour = ax.contour(X, Y, Z, levels=10, colors='black',
                     linewidths=0.5, alpha=0.4)
ax.clabel(contour, inline=True, fontsize=8)
plt.colorbar(contourf, ax=ax)
```

## 8.饼图

* *用例：** 比例、百分比（谨慎使用）

### 基本饼图
```python
ax.pie(sizes, labels=labels, autopct='%1.1f%%',
       startangle=90, colors=colors)
ax.axis('equal')  # Equal aspect ratio ensures circular pie
```

### 分解饼图
```python
explode = (0.1, 0, 0, 0)  # Explode first slice
ax.pie(sizes, explode=explode, labels=labels,
       autopct='%1.1f%%', shadow=True, startangle=90)
ax.axis('equal')
```

### 甜甜圈Chart
```python
ax.pie(sizes, labels=labels, autopct='%1.1f%%',
       wedgeprops=dict(width=0.5), startangle=90)
ax.axis('equal')
```

## 9. 极坐标图

* *用例：** 循环数据、定向数据、雷达图

### 基本极坐标图
```python
theta = np.linspace(0, 2*np.pi, 100)
r = np.abs(np.sin(2*theta))

ax = plt.subplot(111, projection='polar')
ax.plot(theta, r, linewidth=2)
```

### 雷达图表
```python
categories = ['A', 'B', 'C', 'D', 'E']
values = [4, 3, 5, 2, 4]

# Add first value to the end to close the polygon
angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
values_closed = np.concatenate((values, [values[0]]))
angles_closed = np.concatenate((angles, [angles[0]]))

ax = plt.subplot(111, projection='polar')
ax.plot(angles_closed, values_closed, 'o-', linewidth=2)
ax.fill(angles_closed, values_closed, alpha=0.25)
ax.set_xticks(angles)
ax.set_xticklabels(categories)
```

## 10.流图和箭袋图

* *用例：**矢量场，流可视化

### 箭袋图（矢量场）
```python
ax.quiver(X, Y, U, V, alpha=0.8)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_aspect('equal')
```

### 流Plot
```python
ax.streamplot(X, Y, U, V, density=1.5, color='k', linewidth=1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_aspect('equal')
```

## 11. 填充Between

* *用例：** 不确定性边界、置信区间、曲线下面积

### 填充两条曲线之间
```python
ax.plot(x, y, 'k-', linewidth=2, label='Mean')
ax.fill_between(x, y - std, y + std, alpha=0.3,
                label='±1 std dev')
ax.legend()
```

### 填充Between with条件
```python
ax.plot(x, y1, label='Line 1')
ax.plot(x, y2, label='Line 2')
ax.fill_between(x, y1, y2, where=(y2 >= y1),
                alpha=0.3, label='y2 > y1', interpolate=True)
ax.legend()
```

## 12. 3D 绘图

* *用例：** 三维数据可视化

### 3D 散点图
```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(x, y, z, c=colors, cmap='viridis',
                     marker='o', s=50)
plt.colorbar(scatter, ax=ax)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
```

### 3D 曲面Plot
```python
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis',
                       edgecolor='none', alpha=0.9)
plt.colorbar(surf, ax=ax)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
```

### 3D 线框
```python
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(X, Y, Z, color='black', linewidth=0.5)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
```

### 3D 轮廓
```python
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.contour(X, Y, Z, levels=15, cmap='viridis')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
```

## 13. 专业化图

### 茎图
```python
ax.stem(x, y, linefmt='C0-', markerfmt='C0o', basefmt='k-')
ax.set_xlabel('X')
ax.set_ylabel('Y')
```

### 填充多边形
```python
vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
from matplotlib.patches import Polygon
polygon = Polygon(vertices, closed=True, edgecolor='black',
                  facecolor='lightblue', alpha=0.5)
ax.add_patch(polygon)
ax.set_xlim(-0.5, 1.5)
ax.set_ylim(-0.5, 1.5)
```

### 楼梯图
```python
ax.stairs(values, edges, fill=True, alpha=0.5)
```

### Broken Barh（甘特式）
```python
ax.broken_barh([(10, 50), (100, 20), (130, 10)], (10, 9),
               facecolors='tab:blue')
ax.broken_barh([(10, 20), (50, 50), (120, 30)], (20, 9),
               facecolors='tab:orange')
ax.set_ylim(5, 35)
ax.set_xlim(0, 200)
ax.set_xlabel('Time')
ax.set_yticks([15, 25])
ax.set_yticklabels(['Task 1', 'Task 2'])
```

## 14. 时间序列图

### 基本时间序列
```python
import pandas as pd
import matplotlib.dates as mdates

ax.plot(dates, values, linewidth=2)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
plt.xticks(rotation=45)
ax.set_xlabel('Date')
ax.set_ylabel('Value')
```

### 带阴影的时间序列地区
```python
ax.plot(dates, values, linewidth=2)
# Shade weekends or specific periods
ax.axvspan(start_date, end_date, alpha=0.2, color='gray')
```

## 地块选择指南

|数据类型 |推荐剧情|替代选项|
|---------|------------------|------------------------|
|单一连续变量|直方图，KDE |箱线图、小提琴图 |
|两个连续变量 |散点图| Hexbin，2D 直方图 |
|时间序列|线图 |面积图、阶梯图 |
|分类与连续 |条形图、箱线图|小提琴情节、条形情节 |
|两个分类变量 |热图 |分组条形图|
|三个连续变量| 3D 散点、轮廓 |颜色编码散点 |
|比例|条形图|饼图（谨慎使用）|
|分布比较 |箱线图、小提琴图|叠加直方图|
|相关矩阵|热图 |集群热图|
|矢量场|箭袋图、流图 | - |
|函数可视化|线图、等高线图 | 3D曲面|
