# 组织掩模

## 概述

组织掩模是识别整个幻灯片图像中的组织区域的二进制表示。它们对于在图块提取过程中过滤掉背景、伪影和非组织区域至关重要。 Histolab 提供了多种掩模类，以满足不同的组织分割需求。

## 掩模类

### BinaryMask

* *用途：** 用于创建自定义二进制掩模的通用基类。

```python
from histolab.masks import BinaryMask

class CustomMask(BinaryMask):
    def _mask(self, obj):
        # Implement custom masking logic
        # Return binary numpy array
        pass
```

* *用例：**
- 自定义组织分割算法
- 区域特定分析（例如，排除注释）
- 与外部分割模型集成

### TissueMask

* *目的：**使用自动过滤器分割载玻片中的所有组织区域。

```python
from histolab.masks import TissueMask

# Create tissue mask
tissue_mask = TissueMask()

# Apply to slide
mask_array = tissue_mask(slide)
```

* *如何实现作品：**
1. 将图像转换为灰度
2. 应用 Otsu 阈值将组织与背景分开 
3. 执行二元扩张以连接附近的组织区域
4. 去除组织区域内的小孔
5. 过滤掉小物体（伪影）

* *返回：**二进制NumPy数组其中：
- `True`（或1）：组织像素
- `False`（或0）：背景像素

* *最适合：**
- 幻灯片具有多个单独的组织切片
- 综合组织分析
- 当所有组织区域都很重要时

### BiggestTissueBoxMask（默认）

* *目的：**识别并返回最大连接组织区域的边界框。

```python
from histolab.masks import BiggestTissueBoxMask

# Create mask for largest tissue region
biggest_mask = BiggestTissueBoxMask()

# Apply to slide
mask_array = biggest_mask(slide)
```

* *如何实现工作原理：**
1. 应用与 TissueMask
2 相同的过滤管道。识别所有连接的组织成分
3. 选择最大的连通分量
4. 返回包含该区域的边界框

* *最适合：**
- 具有单个主要组织切片的载玻片
- 排除小伪影或组织碎片
- 专注于主要组织区域（大多数平铺者的默认值）

## 使用过滤器自定义蒙版

掩模接受用于专门组织检测的自定义过滤器链：

```python
from histolab.masks import TissueMask
from histolab.filters.image_filters import RgbToGrayscale, OtsuThreshold
from histolab.filters.morphological_filters import BinaryDilation, RemoveSmallHoles

# Define custom filter composition
custom_mask = TissueMask(
    filters=[
        RgbToGrayscale(),
        OtsuThreshold(),
        BinaryDilation(disk_size=5),
        RemoveSmallHoles(area_threshold=500)
    ]
)
```

## 可视化掩模

### 使用locate_mask()

```python
from histolab.slide import Slide
from histolab.masks import TissueMask

slide = Slide("slide.svs", processed_path="output/")
mask = TissueMask()

# Visualize mask boundaries on thumbnail
slide.locate_mask(mask)
```

这显示幻灯片缩略图，其中掩模边界以对比色覆盖。

### 手册可视化

```python
import matplotlib.pyplot as plt
from histolab.masks import TissueMask

slide = Slide("slide.svs", processed_path="output/")
tissue_mask = TissueMask()

# Generate mask
mask_array = tissue_mask(slide)

# Plot side by side
fig, axes = plt.subplots(1, 2, figsize=(15, 7))

axes[0].imshow(slide.thumbnail)
axes[0].set_title("Original Slide")
axes[0].axis('off')

axes[1].imshow(mask_array, cmap='gray')
axes[1].set_title("Tissue Mask")
axes[1].axis('off')

plt.show()
```

## 创建自定义矩形掩模

定义特定的感兴趣区域：

```python
from histolab.masks import BinaryMask
import numpy as np

class RectangularMask(BinaryMask):
    def __init__(self, x_start, y_start, width, height):
        self.x_start = x_start
        self.y_start = y_start
        self.width = width
        self.height = height

    def _mask(self, obj):
        # Create mask with specified rectangular region
        thumb = obj.thumbnail
        mask = np.zeros(thumb.shape[:2], dtype=bool)
        mask[self.y_start:self.y_start+self.height,
             self.x_start:self.x_start+self.width] = True
        return mask

# Use custom mask
roi_mask = RectangularMask(x_start=1000, y_start=500, width=2000, height=1500)
```

## 排除注释

病理学幻灯片通常包含笔标记或数字注释。使用自定义遮罩排除它们：

```python
from histolab.masks import TissueMask
from histolab.filters.image_filters import RgbToGrayscale, OtsuThreshold
from histolab.filters.morphological_filters import BinaryDilation

class AnnotationExclusionMask(BinaryMask):
    def _mask(self, obj):
        thumb = obj.thumbnail

        # Convert to HSV to detect pen marks (often blue/green)
        hsv = cv2.cvtColor(np.array(thumb), cv2.COLOR_RGB2HSV)

        # Define color ranges for pen marks
        lower_blue = np.array([100, 50, 50])
        upper_blue = np.array([130, 255, 255])

        # Create mask excluding pen marks
        pen_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Apply standard tissue detection
        tissue_mask = TissueMask()(obj)

        # Combine: keep tissue, exclude pen marks
        final_mask = tissue_mask & ~pen_mask.astype(bool)

        return final_mask
```

## 与平铺提取集成

遮罩通过`extraction_mask`参数与平铺器无缝集成：

```python
from histolab.tiler import RandomTiler
from histolab.masks import TissueMask, BiggestTissueBoxMask

# Use TissueMask to extract from all tissue
random_tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=100,
    level=0,
    extraction_mask=TissueMask()  # Extract from all tissue regions
)

# Or use default BiggestTissueBoxMask
random_tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=100,
    level=0,
    extraction_mask=BiggestTissueBoxMask()  # Default behavior
)
```

## 最佳实践

1. **提取前预览掩模**：使用`locate_mask()`或手动可视化来验证掩模质量
2. **选择合适的面罩类型**：对于多个组织切片使用 `TissueMask`，对于单个主要切片使用 `BiggestTissueBoxMask`
3. **针对特定染色进行定制**：不同的染色（H&E、IHC）可能需要调整阈值参数
4. **处理伪影**：使用自定义滤镜或遮罩排除笔迹、气泡或折叠
5. **在不同的载玻片上进行测试**：验证具有不同质量和伪影的载玻片的掩模性能
6. **考虑计算成本**：`TissueMask` 比 `BiggestTissueBoxMask`

 更全面，但计算量更大##常见问题和解决方案

### 问题：Mask 包含太多背景
* *解决方案：** 调整 Otsu 阈值或增加小物体去除阈值

### 问题：Mask 排除有效组织
* *解决方案：** 降低小物体去除阈值或修改扩张参数

### 问题：多个组织切片，但仅捕获最大的组织
* *解决方案：** 从 `BiggestTissueBoxMask` 切换到 `TissueMask`

### 问题：掩码中包含笔注释
* *解决方案：** 实现自定义注释排除掩码（参见上面的示例）
