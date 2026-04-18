# Matplotlib 常见问题和解决方案

常见 matplotlib 问题的故障排除指南。

## 显示和后端问题

### 问题：绘图未显示

* *问题：** `plt.show()` 不显示任何

* *解决方案：**
```python
# 1. Check if backend is properly set (for interactive use)
import matplotlib
print(matplotlib.get_backend())

# 2. Try different backends
matplotlib.use('TkAgg')  # or 'Qt5Agg', 'MacOSX'
import matplotlib.pyplot as plt

# 3. In Jupyter notebooks, use magic command
%matplotlib inline  # Static images
# or
%matplotlib widget  # Interactive plots

# 4. Ensure plt.show() is called
plt.plot([1, 2, 3])
plt.show()
```

### 问题：“运行时错误：主线程不在主循环中”

* *问题：**线程的交互模式问题

* *解决方案：**
```python
# Switch to non-interactive backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Or turn off interactive mode
plt.ioff()
```

### 问题：图形未交互式更新

* *问题：** 更改未反映在交互式窗口中

* *解决方案：**
```python
# Enable interactive mode
plt.ion()

# Draw after each change
plt.plot(x, y)
plt.draw()
plt.pause(0.001)  # Brief pause to update display
```

## 布局和间距问题

### 问题：重叠标签和标题

* *问题：**标签、标题或刻度标签重叠或被切断

* *解决方案：**
```python
# Solution 1: Constrained layout (RECOMMENDED)
fig, ax = plt.subplots(constrained_layout=True)

# Solution 2: Tight layout
fig, ax = plt.subplots()
plt.tight_layout()

# Solution 3: Adjust margins manually
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)

# Solution 4: Save with bbox_inches='tight'
plt.savefig('figure.png', bbox_inches='tight')

# Solution 5: Rotate long tick labels
ax.set_xticklabels(labels, rotation=45, ha='right')
```

### 问题：颜色条影响子图大小

* *问题：** 添加颜色条会缩小plot

* *解决方案：**
```python
# Solution 1: Use constrained layout
fig, ax = plt.subplots(constrained_layout=True)
im = ax.imshow(data)
plt.colorbar(im, ax=ax)

# Solution 2: Manually specify colorbar dimensions
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)

# Solution 3: For multiple subplots, share colorbar
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax in axes:
    im = ax.imshow(data)
fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.95)
```

### 问题：子图太靠近

* *问题：**多个子图重叠

* *解决方案：**
```python
# Solution 1: Use constrained_layout
fig, axes = plt.subplots(2, 2, constrained_layout=True)

# Solution 2: Adjust spacing with subplots_adjust
fig, axes = plt.subplots(2, 2)
plt.subplots_adjust(hspace=0.4, wspace=0.4)

# Solution 3: Specify spacing in tight_layout
plt.tight_layout(h_pad=2.0, w_pad=2.0)
```

## 内存和性能问题

### 问题：多个图形的内存泄漏

* *问题：**创建多个图形时内存使用量增加

* *解决方案：**
```python
# Close figures explicitly
fig, ax = plt.subplots()
ax.plot(x, y)
plt.savefig('plot.png')
plt.close(fig)  # or plt.close('all')

# Clear current figure without closing
plt.clf()

# Clear current axes
plt.cla()
```

### 问题：大文件大小

* *问题：**保存的图形太大Large

* *解决方案：**
```python
# Solution 1: Reduce DPI
plt.savefig('figure.png', dpi=150)  # Instead of 300

# Solution 2: Use rasterization for complex plots
ax.plot(x, y, rasterized=True)

# Solution 3: Use vector format for simple plots
plt.savefig('figure.pdf')  # or .svg

# Solution 4: Compress PNG
plt.savefig('figure.png', dpi=300, optimize=True)
```

### 问题：大型数据集绘图速度缓慢

* *问题：** 绘图时间过长点

* *解决方案：**
```python
# Solution 1: Downsample data
from scipy.signal import decimate
y_downsampled = decimate(y, 10)  # Keep every 10th point

# Solution 2: Use rasterization
ax.plot(x, y, rasterized=True)

# Solution 3: Use line simplification
ax.plot(x, y)
for line in ax.get_lines():
    line.set_rasterized(True)

# Solution 4: For scatter plots, consider hexbin or 2d histogram
ax.hexbin(x, y, gridsize=50, cmap='viridis')
```

## 字体和文本问题

### 问题：字体警告

* *问题：**“findfont：字体系列[...]不找到“

* *解决方案：**
```python
# Solution 1: Use available fonts
from matplotlib.font_manager import findfont, FontProperties
print(findfont(FontProperties(family='sans-serif')))

# Solution 2: Rebuild font cache
import matplotlib.font_manager
matplotlib.font_manager._rebuild()

# Solution 3: Suppress warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Solution 4: Specify fallback fonts
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'sans-serif']
```

### 问题：LaTeX渲染错误

* *问题：**数学文本未渲染正确

* *解决方案：**
```python
# Solution 1: Use raw strings with r prefix
ax.set_xlabel(r'$\alpha$')  # Not '\alpha'

# Solution 2: Escape backslashes in regular strings
ax.set_xlabel('$\\alpha$')

# Solution 3: Disable LaTeX if not installed
plt.rcParams['text.usetex'] = False

# Solution 4: Use mathtext instead of full LaTeX
# Mathtext is always available, no LaTeX installation needed
ax.text(x, y, r'$\int_0^\infty e^{-x} dx$')
```

### 问题：文本被剪切或位于图形之外

* *问题：**标签或注释出现在图形之外bounds

* *解决方案：**
```python
# Solution 1: Use bbox_inches='tight'
plt.savefig('figure.png', bbox_inches='tight')

# Solution 2: Adjust figure bounds
plt.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.15)

# Solution 3: Clip text to axes
ax.text(x, y, 'text', clip_on=True)

# Solution 4: Use constrained_layout
fig, ax = plt.subplots(constrained_layout=True)
```

## 颜色和颜色图问题

### 问题：颜色条与图不匹配

* *问题：**颜色条显示的范围与数据

不同**解决方案：**
```python
# Explicitly set vmin and vmax
im = ax.imshow(data, vmin=0, vmax=1, cmap='viridis')
plt.colorbar(im, ax=ax)

# Or use the same norm for multiple plots
import matplotlib.colors as mcolors
norm = mcolors.Normalize(vmin=data.min(), vmax=data.max())
im1 = ax1.imshow(data1, norm=norm, cmap='viridis')
im2 = ax2.imshow(data2, norm=norm, cmap='viridis')
```

### 问题：颜色看起来错误

* *问题：**中出现意外颜色绘图

* *解决方案：**
```python
# Solution 1: Check color specification format
ax.plot(x, y, color='blue')  # Correct
ax.plot(x, y, color=(0, 0, 1))  # Correct RGB
ax.plot(x, y, color='#0000FF')  # Correct hex

# Solution 2: Verify colormap exists
print(plt.colormaps())  # List available colormaps

# Solution 3: For scatter plots, ensure c shape matches
ax.scatter(x, y, c=colors)  # colors should have same length as x, y

# Solution 4: Check if alpha is set correctly
ax.plot(x, y, alpha=1.0)  # 0=transparent, 1=opaque
```

### 问题：反转颜色图

* *问题：**颜色图方向向后

* *解决方案：**
```python
# Add _r suffix to reverse any colormap
ax.imshow(data, cmap='viridis_r')
```

## 轴和比例问题

### 问题：轴限制不起作用

* *问题：** `set_xlim` 或 `set_ylim` 未生效

* *解决方案：**
```python
# Solution 1: Set after plotting
ax.plot(x, y)
ax.set_xlim(0, 10)
ax.set_ylim(-1, 1)

# Solution 2: Disable autoscaling
ax.autoscale(False)
ax.set_xlim(0, 10)

# Solution 3: Use axis method
ax.axis([xmin, xmax, ymin, ymax])
```

### 问题：对数刻度为零或负数值

* *问题：**使用对数刻度且数据≤ 0

时出现值错误**解决方案：**
```python
# Solution 1: Filter out non-positive values
mask = (data > 0)
ax.plot(x[mask], data[mask])
ax.set_yscale('log')

# Solution 2: Use symlog for data with positive and negative values
ax.set_yscale('symlog')

# Solution 3: Add small offset
ax.plot(x, data + 1e-10)
ax.set_yscale('log')
```

### 问题：日期未正确显示

* *问题：**日期轴显示数字而不是数字日期

* *解决方案：**
```python
import matplotlib.dates as mdates
import pandas as pd

# Convert to datetime if needed
dates = pd.to_datetime(date_strings)

ax.plot(dates, values)

# Format date axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
plt.xticks(rotation=45)
```

## 图例问题

### 问题：图例覆盖数据

* *问题：**图例模糊了重要部分图

* *解决方案：**
```python
# Solution 1: Use 'best' location
ax.legend(loc='best')

# Solution 2: Place outside plot area
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Solution 3: Make legend semi-transparent
ax.legend(framealpha=0.7)

# Solution 4: Put legend below plot
ax.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)
```

### 问题：图例中的项目太多

* *问题：** 图例中包含许多项目条目

* *解决方案：**
```python
# Solution 1: Only label selected items
for i, (x, y) in enumerate(data):
    label = f'Data {i}' if i % 5 == 0 else None
    ax.plot(x, y, label=label)

# Solution 2: Use multiple columns
ax.legend(ncol=3)

# Solution 3: Create custom legend with fewer entries
from matplotlib.lines import Line2D
custom_lines = [Line2D([0], [0], color='r'),
                Line2D([0], [0], color='b')]
ax.legend(custom_lines, ['Category A', 'Category B'])

# Solution 4: Use separate legend figure
fig_leg = plt.figure(figsize=(3, 2))
ax_leg = fig_leg.add_subplot(111)
ax_leg.legend(*ax.get_legend_handles_labels(), loc='center')
ax_leg.axis('off')
```

## 3D 绘图问题

### 问题：3D 绘图看起来平坦

* *问题：** 难以感知 3D 深度绘图

* *解决方案：**
```python
# Solution 1: Adjust viewing angle
ax.view_init(elev=30, azim=45)

# Solution 2: Add gridlines
ax.grid(True)

# Solution 3: Use color for depth
scatter = ax.scatter(x, y, z, c=z, cmap='viridis')

# Solution 4: Rotate interactively (if using interactive backend)
# User can click and drag to rotate
```

### 问题：3D 轴标签被切断

* *问题：** 3D 轴标签出现在外部图

* *解决方案：**
```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z)

# Add padding
fig.tight_layout(pad=3.0)

# Or save with tight bounding box
plt.savefig('3d_plot.png', bbox_inches='tight', pad_inches=0.5)
```

## 图像和颜色条问题

### 问题：图像出现翻转

* *问题：** 图像方向是错误

* *解决方案：**
```python
# Set origin parameter
ax.imshow(img, origin='lower')  # or 'upper' (default)

# Or flip array
ax.imshow(np.flipud(img))
```

### 问题：图像看起来像素化

* *问题：** 缩放时图像出现块状

* *解决方案：**
```python
# Solution 1: Use interpolation
ax.imshow(img, interpolation='bilinear')
# Options: 'nearest', 'bilinear', 'bicubic', 'spline16', 'spline36', etc.

# Solution 2: Increase DPI when saving
plt.savefig('figure.png', dpi=300)

# Solution 3: Use vector format if appropriate
plt.savefig('figure.pdf')
```

## 常见错误和修复

### “TypeError：'AxesSubplot'对象不可下标”

 * *问题：**尝试索引单轴
```python
# Wrong
fig, ax = plt.subplots()
ax[0].plot(x, y)  # Error!

# Correct
fig, ax = plt.subplots()
ax.plot(x, y)
```

### “ValueError：x和y必须具有相同的第一维度”

* *问题：**数据数组长度不匹配
```python
# Check shapes
print(f"x shape: {x.shape}, y shape: {y.shape}")

# Ensure they match
assert len(x) == len(y), "x and y must have same length"
```

### “AttributeError：‘numpy.ndarray’对象没有属性‘plot’”

* *问题：** 在数组上调用绘图而不是轴
```python
# Wrong
data.plot(x, y)

# Correct
ax.plot(x, y)
# or for pandas
data.plot(ax=ax)
```

## 避免问题的最佳实践

1. **始终使用 OO 接口** - 避免使用 pyplot 状态机
 ```python
 Fig, ax = plt.subplots() # Good
 ax.plot(x, y)
 ```

2. **使用 constrained_layout** - 防止重叠问题
 ```python
 Fig, ax = plt.subplots(constrained_layout=True)
 ```

3. **明确关闭数字** - 防止内存泄漏
``python
 plt.close(fig)
``

4. **在创建时设置图形大小** - 比稍后调整大小更好
 ```python
 Fig, ax = plt.subplots(figsize=(10, 6))
 ```

5. **使用原始字符串作为数学文本** - 避免转义问题
 ```python
 ax.set_xlabel(r'$\alpha$')
 ```

6. **绘图前检查数据形状** - 早期捕获大小不匹配
 ```python
 断言 len(x) == len(y)
 ```

7. **使用适当的 DPI** - 打印为 300，网络为 150
 ```python
 plt.savefig('figure.png', dpi=300)
 ```

8. **使用不同后端进行测试** - 如果出现显示问题
 ```python
 import matplotlib
 matplotlib.use('TkAgg')
 ```
