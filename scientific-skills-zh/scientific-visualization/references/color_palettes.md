# 科学调色板和指南

## 概述

科学可视化中的颜色选择对于可访问性、清晰度和准确的数据表示至关重要。本参考提供色盲友好调色板和颜色使用的最佳实践。

## 色盲友好调色板

### Okabe-Ito 调色板（推荐用于类别）

Okabe-Ito 调色板经过专门设计，可让具有各种颜色形式的人区分

```python
# Okabe-Ito colors (RGB values)
okabe_ito = {
    'orange': '#E69F00',      # RGB: (230, 159, 0)
    'sky_blue': '#56B4E9',    # RGB: (86, 180, 233)
    'bluish_green': '#009E73', # RGB: (0, 158, 115)
    'yellow': '#F0E442',      # RGB: (240, 228, 66)
    'blue': '#0072B2',        # RGB: (0, 114, 178)
    'vermillion': '#D55E00',  # RGB: (213, 94, 0)
    'reddish_purple': '#CC79A7', # RGB: (204, 121, 167)
    'black': '#000000'        # RGB: (0, 0, 0)
}
```

* *Matplotlib中的用法:**
```python
import matplotlib.pyplot as plt

colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
          '#0072B2', '#D55E00', '#CC79A7', '#000000']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
```

* *Seaborn中的用法:**
```python
import seaborn as sns

okabe_ito_palette = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
                      '#0072B2', '#D55E00', '#CC79A7']
sns.set_palette(okabe_ito_palette)
```

* *中的用法情节：**
```python
import plotly.graph_objects as go

okabe_ito_plotly = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
                     '#0072B2', '#D55E00', '#CC79A7']
fig = go.Figure()
# Apply to discrete color scale
```

### Wong Palette（类别的替代）

Bang Wong（自然方法）的另一个优秀的色盲友好调色板。

```python
wong_palette = {
    'black': '#000000',
    'orange': '#E69F00',
    'sky_blue': '#56B4E9',
    'green': '#009E73',
    'yellow': '#F0E442',
    'blue': '#0072B2',
    'vermillion': '#D55E00',
    'purple': '#CC79A7'
}
```

### Paul Tol Palettes

Paul Tol针对不同的使用场景设计了多个经过科学优化的调色板。

* *明亮调色板（最多7个类别）：**
```python
tol_bright = ['#4477AA', '#EE6677', '#228833', '#CCBB44',
              '#66CCEE', '#AA3377', '#BBBBBB']
```

* *静音调色板（最多9个类别）：**
```python
tol_muted = ['#332288', '#88CCEE', '#44AA99', '#117733',
             '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499']
```

* *高对比度（3个类别）仅）：**
```python
tol_high_contrast = ['#004488', '#DDAA33', '#BB5566']
```

## 顺序颜色图（连续数据）

顺序颜色图用单一色调表示从低值到高值的数据。

### 感知均匀颜色图

这些颜色图在整个颜色上具有统一的感知变化scale.

* *Viridis（Matplotlib 中的默认值）：**
- 色盲友好
- 灰度打印效果良好
- 感知制服
```python
plt.imshow(data, cmap='viridis')
```

* *Cividis：**
- 针对色盲观众进行了优化
- 专为绿色盲/红色盲设计
```python
plt.imshow(data, cmap='cividis')
```

* *等离子，地狱， Magma:**
- 感知上统一的 viridis 替代品
- 适合不同的审美偏好
```python
plt.imshow(data, cmap='plasma')
```

### 何时使用序列地图
- 显示强度的热图
- 地理海拔数据
- 概率分布
- 任何单变量连续数据（低→高）

## 发散颜色图（负到正）

发散颜色图具有中性中间颜色，在极端处具有两种对比色。

### 色盲安全发散贴图

* *RdYlBu （红-黄-蓝）：**
```python
plt.imshow(data, cmap='RdYlBu_r')  # _r reverses: blue (low) to red (high)
```

* *PuOr（紫-橙色）：**
- 非常适合色盲观众
```python
plt.imshow(data, cmap='PuOr')
```

* *BrBG（棕-蓝-绿）：**
- 良好色盲可访问性
```python
plt.imshow(data, cmap='BrBG')
```

### 避免这些发散的地图
- **RdGn（红-绿）**：红-绿色盲有问题
- **RdYlGn（红-黄-绿）**：同样的问题

### 何时使用发散图
- 相关矩阵
- 变化/差异数据（正与负）
- 与中心值的偏差
- 温度异常

## 特殊用途调色板

### 对于基因组学/生物信息学

* *序列类型识别：**
```python
# DNA/RNA bases
nucleotide_colors = {
    'A': '#00CC00',  # Green
    'C': '#0000CC',  # Blue
    'G': '#FFB300',  # Orange
    'T': '#CC0000',  # Red
    'U': '#CC0000'   # Red (RNA)
}
```

* *基因表达：**
- 使用顺序颜色图（viridis、YlOrRd）表示表达水平
- 使用发散颜色图（RdBu）表示log2折叠更改

### 用于显微镜

* *荧光通道：**
```python
# Traditional fluorophore colors (use with caution)
fluorophore_colors = {
    'DAPI': '#0000FF',      # Blue - DNA
    'GFP': '#00FF00',       # Green (problematic for colorblind)
    'RFP': '#FF0000',       # Red
    'Cy5': '#FF00FF'        # Magenta
}

# Colorblind-friendly alternatives
fluorophore_alt = {
    'Channel1': '#0072B2',  # Blue
    'Channel2': '#E69F00',  # Orange (instead of green)
    'Channel3': '#D55E00',  # Vermillion
    'Channel4': '#CC79A7'   # Magenta
}
```

## 颜色使用最佳实践

### 分类数据（定性配色方案）

* *执行：**
- 使用不同的， Okabe-Ito 或 Wong 调色板中的饱和颜色
- 一个图中最多限制 7-8 个类别
- 对各个图中的相同类别使用一致的颜色
- 当单独的颜色可能不够时添加图案/标记

* *不要：**
- 使用红色/绿色组合
- 使用彩虹（喷射）类别的颜色图
- 使用难以区分的相似色调

### 连续数据（顺序/发散方案）

* *Do:**
- 使用感知均匀的颜色图（viridis、plasma、cividis）
- 当数据具有有意义的中心时选择发散图point
- 包括带标记刻度的颜色条
- 测试灰度外观

* *不要：**
- 使用彩虹（喷射）颜色图-感知上不均匀
- 使用红绿发散图
- 在热图上省略颜色条

## 色盲可访问性测试

### 在线模拟器
- **Coblis**： https://www.color-blindness.com/coblis-color-blindness-simulator/
- **Color Oracle**：适用于 Windows/Mac/Linux 的免费下载工具
- **Sim Daltonism**：Mac 应用程序

### 色觉缺陷的类型
- **绿盲**（约 5% 的男性）：无法区分绿色
- **红色盲**（约2%的男性）：无法区分红色
- **蓝色盲**（<1%）：无法区分蓝色（罕见）

### Python工具
```python
# Using colorspacious to simulate colorblind vision
from colorspacious import cspace_convert

def simulate_deuteranopia(image_rgb):
    from colorspacious import cspace_convert
    # Convert to colorblind simulation
    # (Implementation would require colorspacious library)
    pass
```

## 实现示例

### 设置全局Matplotlib 样式
```python
import matplotlib.pyplot as plt
import matplotlib as mpl

# Set Okabe-Ito as default color cycle
okabe_ito_colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
                     '#0072B2', '#D55E00', '#CC79A7']
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=okabe_ito_colors)

# Set default colormap to viridis
mpl.rcParams['image.cmap'] = 'viridis'
```

### Seaborn 与自定义调色板
```python
import seaborn as sns

# Set Paul Tol muted palette
tol_muted = ['#332288', '#88CCEE', '#44AA99', '#117733',
             '#999933', '#DDCC77', '#CC6677', '#882255', '#AA4499']
sns.set_palette(tol_muted)

# For heatmaps
sns.heatmap(data, cmap='viridis', annot=True)
```

### 绘制离散颜色
```python
import plotly.express as px

# Use Okabe-Ito for categorical data
okabe_ito_plotly = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
                     '#0072B2', '#D55E00', '#CC79A7']

fig = px.scatter(df, x='x', y='y', color='category',
                 color_discrete_sequence=okabe_ito_plotly)
```

## 灰度兼容性

所有图形都应保持可解释的灰度。通过转换为灰度进行测试：

```python
# Convert figure to grayscale for testing
fig.savefig('figure_gray.png', dpi=300, colormap='gray')
```

* *灰度兼容策略：**
1. 使用不同的线型（实线、虚线、点线）
2. 使用不同的标记形状（圆形、正方形、三角形）
3. 将剖面线图案添加到bars
4. 确保颜色之间有足够的亮度对比度

## 色彩空间

### RGB 与 CMYK
- **RGB**（红、绿、蓝）：用于数字/屏幕显示
- **CMYK**（青色、品红色、黄色、黑色）：用于打印

* *重要：** 打印时的颜色与屏幕上的颜色不同。准备打印时：
1. 转换为 CMYK 色彩空间
2. 检查 CMYK 预览中的颜色外观
3. 确保保持足够的对比度

### Matplotlib 色彩空间
```python
# Save for print (CMYK)
# Note: Direct CMYK support limited; use PDF and let publisher convert
fig.savefig('figure.pdf', dpi=300)

# For RGB (digital)
fig.savefig('figure.png', dpi=300)
```

## 常见错误

1. **使用jet/rainbow色彩图**：感知上不均匀；避免
2. **红绿组合**：约 8% 的男性无法区分 
3. **颜色太多**：超过7-8个就变得难以区分
4. **颜色含义不一致**：数字 
5 中相同的颜色应表示相同的内容。 **缺少颜色条**：始终包含连续数据
6. **低对比度**：确保颜色足够不同
7. **仅依靠颜色**：添加纹理、图案或标记

## 资源

- **ColorBrewer**：http://colorbrewer2.org/ - 通过色盲安全选项选择调色板
- **Paul Tol 的调色板**：https://personal.sron.nl/~pault/
- **Okabe-Ito 调色板起源**： “颜色通用设计”（Okabe & Ito，2008）
- **Matplotlib 颜色图**：https://matplotlib.org/stable/tutorials/colors/colormaps.html
- **Seaborn 调色板**： https://seaborn.pydata.org/tutorial/color_palettes.html
