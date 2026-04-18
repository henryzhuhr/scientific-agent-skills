# Matplotlib 样式指南

matplotlib 可视化样式和自定义的综合指南。

## 颜色图

### 颜色图类别

* *1.感知均匀顺序**
最适合从低值到高值进行的有序数据。
- `viridis`（默认，色盲友好）
- `plasma`
- `inferno`
- `magma`
- `cividis`（针对色盲观众优化）

* *用法：**
```python
im = ax.imshow(data, cmap='viridis')
scatter = ax.scatter(x, y, c=values, cmap='plasma')
```

* *2。顺序**
有序数据的传统颜色图。
- `Blues`、`Greens`、`Reds`、`Oranges`、`Purples`
- `YlOrBr`、`YlOrRd`、 `OrRd`、`PuRd`
- `BuPu`、`GnBu`、`PuBu`、`YlGnBu`

* *3。发散**
最适合具有有意义的中心点（例如零、平均值）的数据。
- `coolwarm`（蓝到红）
- `RdBu`（红-蓝）
- `RdYlBu` （红黄蓝）
- `RdYlGn` （红黄绿）
- `PiYG`、`PRGn`、`BrBG`、`PuOr`、 `RdGy`

* *用法：**
```python
# Center colormap at zero
im = ax.imshow(data, cmap='coolwarm', vmin=-1, vmax=1)
```

* *4。定性**
最适合无固有排序的分类/标称数据。
- `tab10`（10 种不同颜色）
- `tab20`（20 种不同颜色）
- `Set1`、`Set2`、 `Set3`
- `Pastel1`, `Pastel2`
- `Dark2`, `Accent`, `Paired`

* *用法：**
```python
colors = plt.cm.tab10(np.linspace(0, 1, n_categories))
for i, category in enumerate(categories):
    ax.plot(x, y[i], color=colors[i], label=category)
```

* *5.循环**
最适合循环数据（例如相位、角度）。
- `twilight`
- `twilight_shifted`
- `hsv`

### 色彩图最佳实践

1. **避免 `jet` 颜色图** - 感知上不统一，具有误导性
2. **使用感知均匀的颜色图** - `viridis`、`plasma`、`cividis`
3. **考虑色盲用户** - 使用 `viridis`、`cividis`，或使用色盲模拟器 
4 进行测试。 **将颜色图与数据类型匹配**：
 - 顺序：增加/减少数据
  - 发散：具有有意义的中心的数据
  - 定性：类别
5. **反向颜色图** - 添加 `_r` 后缀：`viridis_r`、`coolwarm_r`

### 创建自定义颜色图

```python
from matplotlib.colors import LinearSegmentedColormap

# From color list
colors = ['blue', 'white', 'red']
n_bins = 100
cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)

# From RGB values
colors = [(0, 0, 1), (1, 1, 1), (1, 0, 0)]  # RGB tuples
cmap = LinearSegmentedColormap.from_list('custom', colors)

# Use the custom colormap
ax.imshow(data, cmap=cmap)
```

### 离散颜色图

```python
import matplotlib.colors as mcolors

# Create discrete colormap from continuous
cmap = plt.cm.viridis
bounds = np.linspace(0, 10, 11)
norm = mcolors.BoundaryNorm(bounds, cmap.N)
im = ax.imshow(data, cmap=cmap, norm=norm)
```

## 样式表

### 使用内置样式

```python
# List available styles
print(plt.style.available)

# Apply a style
plt.style.use('seaborn-v0_8-darkgrid')

# Apply multiple styles (later styles override earlier ones)
plt.style.use(['seaborn-v0_8-whitegrid', 'seaborn-v0_8-poster'])

# Temporarily use a style
with plt.style.context('ggplot'):
    fig, ax = plt.subplots()
    ax.plot(x, y)
```

### 流行内置样式

- `default` - Matplotlib's默认样式
- `classic` - 经典matplotlib外观（2.0之前）
- `seaborn-v0_8-*` - Seaborn风格的样式
  - `seaborn-v0_8-darkgrid`、`seaborn-v0_8-whitegrid`
  - `seaborn-v0_8-dark`、`seaborn-v0_8-white`
  - `seaborn-v0_8-ticks`、`seaborn-v0_8-poster`、`seaborn-v0_8-talk`
- `ggplot` - ggplot2 风格
- `bmh` - 贝叶斯方法对于黑客 style
- `fivethirtyeight` - FiveThirtyEight style
- `grayscale` - 灰度 style

### 创建自定义样式表

创建一个名为的文件`custom_style.mplstyle`:

```
# custom_style.mplstyle

# Figure
figure.figsize: 10, 6
figure.dpi: 100
figure.facecolor: white

# Font
font.family: sans-serif
font.sans-serif: Arial, Helvetica
font.size: 12

# Axes
axes.labelsize: 14
axes.titlesize: 16
axes.facecolor: white
axes.edgecolor: black
axes.linewidth: 1.5
axes.grid: True
axes.axisbelow: True

# Grid
grid.color: gray
grid.linestyle: --
grid.linewidth: 0.5
grid.alpha: 0.3

# Lines
lines.linewidth: 2
lines.markersize: 8

# Ticks
xtick.labelsize: 10
ytick.labelsize: 10
xtick.direction: in
ytick.direction: in
xtick.major.size: 6
ytick.major.size: 6
xtick.minor.size: 3
ytick.minor.size: 3

# Legend
legend.fontsize: 12
legend.frameon: True
legend.framealpha: 0.8
legend.fancybox: True

# Savefig
savefig.dpi: 300
savefig.bbox: tight
savefig.facecolor: white
```

加载使用：
```python
plt.style.use('path/to/custom_style.mplstyle')
```

## rcParams配置

### 全局配置

```python
import matplotlib.pyplot as plt

# Configure globally
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14

# Or update multiple at once
plt.rcParams.update({
    'figure.figsize': (10, 6),
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'lines.linewidth': 2
})
```

### 临时配置

```python
# Context manager for temporary changes
with plt.rc_context({'font.size': 14, 'lines.linewidth': 2.5}):
    fig, ax = plt.subplots()
    ax.plot(x, y)
```

### 常用rcParams

* *图形设置：**
```python
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['figure.edgecolor'] = 'white'
plt.rcParams['figure.autolayout'] = False
plt.rcParams['figure.constrained_layout.use'] = True
```

* *字体设置：**
```python
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'normal'
```

* *轴设置：**
```python
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['axes.grid'] = True
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelweight'] = 'normal'
plt.rcParams['axes.spines.top'] = True
plt.rcParams['axes.spines.right'] = True
```

* *线设置：**
```python
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['lines.linestyle'] = '-'
plt.rcParams['lines.marker'] = 'None'
plt.rcParams['lines.markersize'] = 6
```

* *保存设置：**
```python
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.format'] = 'png'
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.1
plt.rcParams['savefig.transparent'] = False
```

## 调色板

### 命名颜色集

```python
# Tableau colors
tableau_colors = plt.cm.tab10.colors

# CSS4 colors (subset)
css_colors = ['steelblue', 'coral', 'teal', 'goldenrod', 'crimson']

# Manual definition
custom_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
```

### 颜色循环

```python
# Set default color cycle
from cycler import cycler
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
plt.rcParams['axes.prop_cycle'] = cycler(color=colors)

# Or combine color and line style
plt.rcParams['axes.prop_cycle'] = cycler(color=colors) + cycler(linestyle=['-', '--', ':', '-.'])
```

### 调色板Generation

```python
# Evenly spaced colors from colormap
n_colors = 5
colors = plt.cm.viridis(np.linspace(0, 1, n_colors))

# Use in plot
for i, (x, y) in enumerate(data):
    ax.plot(x, y, color=colors[i])
```

## Typography

### 字体配置

```python
# Set font family
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']

# Or sans-serif
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']

# Or monospace
plt.rcParams['font.family'] = 'monospace'
plt.rcParams['font.monospace'] = ['Courier New', 'DejaVu Sans Mono']
```

### 文本中的字体属性

```python
from matplotlib import font_manager

# Specify font properties
ax.text(x, y, 'Text',
        fontsize=14,
        fontweight='bold',  # 'normal', 'bold', 'heavy', 'light'
        fontstyle='italic',  # 'normal', 'italic', 'oblique'
        fontfamily='serif')

# Use specific font file
prop = font_manager.FontProperties(fname='path/to/font.ttf')
ax.text(x, y, 'Text', fontproperties=prop)
```

### 数学Text

```python
# LaTeX-style math
ax.set_title(r'$\alpha > \beta$')
ax.set_xlabel(r'$\mu \pm \sigma$')
ax.text(x, y, r'$\int_0^\infty e^{-x} dx = 1$')

# Subscripts and superscripts
ax.set_ylabel(r'$y = x^2 + 2x + 1$')
ax.text(x, y, r'$x_1, x_2, \ldots, x_n$')

# Greek letters
ax.text(x, y, r'$\alpha, \beta, \gamma, \delta, \epsilon$')
```

### 使用 Full LaTeX

```python
# Enable full LaTeX rendering (requires LaTeX installation)
plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

ax.set_title(r'\textbf{Bold Title}')
ax.set_xlabel(r'Time $t$ (s)')
```

## 脊椎和网格

### 脊椎定制

```python
# Hide specific spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Move spine position
ax.spines['left'].set_position(('outward', 10))
ax.spines['bottom'].set_position(('data', 0))

# Change spine color and width
ax.spines['left'].set_color('red')
ax.spines['bottom'].set_linewidth(2)
```

### 网格定制

```python
# Basic grid
ax.grid(True)

# Customized grid
ax.grid(True, which='major', linestyle='--', linewidth=0.8, alpha=0.3)
ax.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.2)

# Grid for specific axis
ax.grid(True, axis='x')  # Only vertical lines
ax.grid(True, axis='y')  # Only horizontal lines

# Grid behind or in front of data
ax.set_axisbelow(True)  # Grid behind data
```

## 图例自定义

### 图例定位

```python
# Location strings
ax.legend(loc='best')  # Automatic best position
ax.legend(loc='upper right')
ax.legend(loc='upper left')
ax.legend(loc='lower right')
ax.legend(loc='lower left')
ax.legend(loc='center')
ax.legend(loc='upper center')
ax.legend(loc='lower center')
ax.legend(loc='center left')
ax.legend(loc='center right')

# Precise positioning (bbox_to_anchor)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Outside plot area
ax.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)  # Below plot
```

### 图例样式

```python
ax.legend(
    fontsize=12,
    frameon=True,           # Show frame
    framealpha=0.9,         # Frame transparency
    fancybox=True,          # Rounded corners
    shadow=True,            # Shadow effect
    ncol=2,                 # Number of columns
    title='Legend Title',   # Legend title
    title_fontsize=14,      # Title font size
    edgecolor='black',      # Frame edge color
    facecolor='white'       # Frame background color
)
```

### 自定义图例条目

```python
from matplotlib.lines import Line2D

# Create custom legend handles
custom_lines = [Line2D([0], [0], color='red', lw=2),
                Line2D([0], [0], color='blue', lw=2, linestyle='--'),
                Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10)]

ax.legend(custom_lines, ['Label 1', 'Label 2', 'Label 3'])
```

## 布局和间距

### 约束布局

```python
# Preferred method (automatic adjustment)
fig, axes = plt.subplots(2, 2, constrained_layout=True)
```

### 紧密布局

```python
# Alternative method
fig, axes = plt.subplots(2, 2)
plt.tight_layout(pad=1.5, h_pad=2.0, w_pad=2.0)
```

### 手动调整

```python
# Fine-grained control
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1,
                    hspace=0.3, wspace=0.4)
```

## 专业出版物样式

出版物质量人物的配置示例：

```python
# Publication style configuration
plt.rcParams.update({
    # Figure
    'figure.figsize': (8, 6),
    'figure.dpi': 100,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,

    # Font
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica'],
    'font.size': 11,

    # Axes
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'axes.linewidth': 1.5,
    'axes.grid': False,
    'axes.spines.top': False,
    'axes.spines.right': False,

    # Lines
    'lines.linewidth': 2,
    'lines.markersize': 8,

    # Ticks
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'xtick.major.size': 6,
    'ytick.major.size': 6,
    'xtick.major.width': 1.5,
    'ytick.major.width': 1.5,
    'xtick.direction': 'in',
    'ytick.direction': 'in',

    # Legend
    'legend.fontsize': 10,
    'legend.frameon': True,
    'legend.framealpha': 1.0,
    'legend.edgecolor': 'black'
})
```

## 深色主题

```python
# Dark background style
plt.style.use('dark_background')

# Or manual configuration
plt.rcParams.update({
    'figure.facecolor': '#1e1e1e',
    'axes.facecolor': '#1e1e1e',
    'axes.edgecolor': 'white',
    'axes.labelcolor': 'white',
    'text.color': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'grid.color': 'gray',
    'legend.facecolor': '#1e1e1e',
    'legend.edgecolor': 'white'
})
```

## 颜色可访问性

### 色盲友好调色板

```python
# Use colorblind-friendly colormaps
colorblind_friendly = ['viridis', 'plasma', 'cividis']

# Colorblind-friendly discrete colors
cb_colors = ['#0173B2', '#DE8F05', '#029E73', '#CC78BC',
             '#CA9161', '#949494', '#ECE133', '#56B4E9']

# Test with simulation tools or use these validated palettes
```

### 高对比度

```python
# Ensure sufficient contrast
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2
```
