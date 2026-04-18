# 过滤器和预处理

## 概述

Histolab 提供了一套全面的过滤器，用于预处理整个幻灯片图像和图块。过滤器可应用于图像以进行可视化、质量控制、组织检测和伪影去除。它们是可组合的，可以链接在一起以创建复杂的预处理管道。

## 过滤器类别

### 图像过滤器
色彩空间转换、阈值和强度调整

### 形态过滤器
膨胀、腐蚀、打开和关闭等结构操作

### 组合Filters
用于组合多个滤镜的实用程序

## 图像滤镜

### RgbToGrayscale

将RGB图像转换为灰度。

```python
from histolab.filters.image_filters import RgbToGrayscale

gray_filter = RgbToGrayscale()
gray_image = gray_filter(rgb_image)
```

* *用例：**
- 基于强度的预处理操作
- 简化颜色复杂度
- 形态操作的输入

### RgbToHsv

将RGB转换为HSV（色调、饱和度、值）颜色空间。

```python
from histolab.filters.image_filters import RgbToHsv

hsv_filter = RgbToHsv()
hsv_image = hsv_filter(rgb_image)
```

* *使用案例：**
- 基于颜色的组织分割
- 通过色调检测笔标记
- 将彩色内容与无彩色内容分离

### RgbToHed

将 RGB 转换为 HED（苏木精-曙红-DAB）颜色空间进行染色反卷积。

```python
from histolab.filters.image_filters import RgbToHed

hed_filter = RgbToHed()
hed_image = hed_filter(rgb_image)
```

* *用例：**
- 分离 H&E 染色成分
- 分析细胞核（苏木精）与细胞质（伊红）染色
- 定量染色强度

### OtsuThreshold

应用Otsu的自动阈值方法创建二值图像。

```python
from histolab.filters.image_filters import OtsuThreshold

otsu_filter = OtsuThreshold()
binary_image = otsu_filter(grayscale_image)
```

* *工作原理：**
- 自动确定最佳阈值
- 将前景与背景分开
- 最小化类内方差

* *用例：**
- 组织检测
- 细胞核分割
- 二进制掩模创建

### AdaptiveThreshold

对局部强度变化应用自适应阈值。

```python
from histolab.filters.image_filters import AdaptiveThreshold

adaptive_filter = AdaptiveThreshold(
    block_size=11,      # Size of local neighborhood
    offset=2            # Constant subtracted from mean
)
binary_image = adaptive_filter(grayscale_image)
```

* *用例：**
- 非均匀照明
- 局部对比度增强
- 处理可变染色强度

### 反转

反转图像强度值。

```python
from histolab.filters.image_filters import Invert

invert_filter = Invert()
inverted_image = invert_filter(image)
```

* *使用案例：**
- 某些分割算法的预处理
- 可视化调整

### StretchContrast

通过拉伸强度范围来增强图像对比度。

```python
from histolab.filters.image_filters import StretchContrast

contrast_filter = StretchContrast()
enhanced_image = contrast_filter(image)
```

* *使用案例：**
- 提高低对比度的可见度特征
- 可视化预处理
- 增强微弱结构

### 直方图均衡

E均衡图像直方图以增强对比度。

```python
from histolab.filters.image_filters import HistogramEqualization

hist_eq_filter = HistogramEqualization()
equalized_image = hist_eq_filter(grayscale_image)
```

* *用例：**
- 标准化图像对比
- 揭示隐藏的细节
- 特征提取的预处理

## 形态过滤器

### BinaryDilation

以二进制形式扩展白色区域images.

```python
from histolab.filters.morphological_filters import BinaryDilation

dilation_filter = BinaryDilation(disk_size=5)
dilated_image = dilation_filter(binary_image)
```

* *参数：**
- `disk_size`：结构元素的大小（默认：5）

* *用例：**
- 连接附近的组织区域
- 填充小间隙
- 扩展组织掩模

### BinaryErosion

缩小二值图像中的白色区域。

```python
from histolab.filters.morphological_filters import BinaryErosion

erosion_filter = BinaryErosion(disk_size=5)
eroded_image = erosion_filter(binary_image)
```

* *用例：**
- 去除小突起
- 分离连接对象
- 收缩组织边界

### BinaryOpening

E先腐蚀后膨胀（删除小对象）。

```python
from histolab.filters.morphological_filters import BinaryOpening

opening_filter = BinaryOpening(disk_size=3)
opened_image = opening_filter(binary_image)
```

* *用例：**
- 删除小伪影
- 平滑对象边界
- 降噪

### 二元闭运算

膨胀后腐蚀（填充小孔）。

```python
from histolab.filters.morphological_filters import BinaryClosing

closing_filter = BinaryClosing(disk_size=5)
closed_image = closing_filter(binary_image)
```

* *用例：**
- 填充组织区域中的小孔
- 连接附近对象
- 平滑内部边界

### RemoveSmallObjects

删除小于阈值的连接组件。

```python
from histolab.filters.morphological_filters import RemoveSmallObjects

remove_small_filter = RemoveSmallObjects(
    area_threshold=500  # Minimum area in pixels
)
cleaned_image = remove_small_filter(binary_image)
```

* *用例：**
- 去除灰尘和伪影
- 过滤噪音
- 清洁纸巾面罩

### RemoveSmallHoles

填充小于阈值的孔。

```python
from histolab.filters.morphological_filters import RemoveSmallHoles

fill_holes_filter = RemoveSmallHoles(
    area_threshold=1000  # Maximum hole size to fill
)
filled_image = fill_holes_filter(binary_image)
```

* *用例：**
- 填充组织中的小间隙
- 创建连续的组织区域
- 去除内部伪影

## 滤波器组合

### 链接滤波器

将多个滤波器组合在序列：

```python
from histolab.filters.image_filters import RgbToGrayscale, OtsuThreshold
from histolab.filters.morphological_filters import BinaryDilation, RemoveSmallObjects
from histolab.filters.compositions import Compose

# Create filter pipeline
tissue_detection_pipeline = Compose([
    RgbToGrayscale(),
    OtsuThreshold(),
    BinaryDilation(disk_size=5),
    RemoveSmallHoles(area_threshold=1000),
    RemoveSmallObjects(area_threshold=500)
])

# Apply pipeline
result = tissue_detection_pipeline(rgb_image)
```

### Lambda 过滤器

创建自定义过滤器内联：

```python
from histolab.filters.image_filters import Lambda
import numpy as np

# Custom brightness adjustment
brightness_filter = Lambda(lambda img: np.clip(img * 1.2, 0, 255).astype(np.uint8))

# Custom color channel extraction
red_channel_filter = Lambda(lambda img: img[:, :, 0])
```

## 常见预处理管道

### 标准组织检测

```python
from histolab.filters.compositions import Compose
from histolab.filters.image_filters import RgbToGrayscale, OtsuThreshold
from histolab.filters.morphological_filters import (
    BinaryDilation, RemoveSmallHoles, RemoveSmallObjects
)

tissue_detection = Compose([
    RgbToGrayscale(),
    OtsuThreshold(),
    BinaryDilation(disk_size=5),
    RemoveSmallHoles(area_threshold=1000),
    RemoveSmallObjects(area_threshold=500)
])
```

### 笔痕去除

```python
from histolab.filters.image_filters import RgbToHsv, Lambda
import numpy as np

def remove_pen_marks(hsv_image):
    """Remove blue/green pen markings."""
    h, s, v = hsv_image[:, :, 0], hsv_image[:, :, 1], hsv_image[:, :, 2]
    # Mask for blue/green hues (common pen colors)
    pen_mask = ((h > 0.45) & (h < 0.7) & (s > 0.3))
    # Set pen regions to white
    hsv_image[pen_mask] = [0, 0, 1]
    return hsv_image

pen_removal = Compose([
    RgbToHsv(),
    Lambda(remove_pen_marks)
])
```

### 细胞核增强

```python
from histolab.filters.image_filters import RgbToHed, HistogramEqualization
from histolab.filters.compositions import Compose

nuclei_enhancement = Compose([
    RgbToHed(),
    Lambda(lambda hed: hed[:, :, 0]),  # Extract hematoxylin channel
    HistogramEqualization()
])
```

### 对比度标准化

```python
from histolab.filters.image_filters import StretchContrast, HistogramEqualization

contrast_normalization = Compose([
    RgbToGrayscale(),
    StretchContrast(),
    HistogramEqualization()
])
```

## 将过滤器应用于图块

过滤器可以应用于单个图块：

```python
from histolab.tile import Tile
from histolab.filters.image_filters import RgbToGrayscale

# Load or extract tile
tile = Tile(image=pil_image, coords=(x, y))

# Apply filter
gray_filter = RgbToGrayscale()
filtered_tile = tile.apply_filters(gray_filter)

# Chain multiple filters
from histolab.filters.compositions import Compose
from histolab.filters.image_filters import StretchContrast

filter_chain = Compose([
    RgbToGrayscale(),
    StretchContrast()
])
processed_tile = tile.apply_filters(filter_chain)
```

## 自定义掩模过滤器

将自定义过滤器与组织集成掩码：

```python
from histolab.masks import TissueMask
from histolab.filters.compositions import Compose
from histolab.filters.image_filters import RgbToGrayscale, OtsuThreshold
from histolab.filters.morphological_filters import BinaryDilation

# Custom aggressive tissue detection
aggressive_filters = Compose([
    RgbToGrayscale(),
    OtsuThreshold(),
    BinaryDilation(disk_size=10),  # Larger dilation
    RemoveSmallObjects(area_threshold=5000)  # Remove only large artifacts
])

# Create mask with custom filters
custom_mask = TissueMask(filters=aggressive_filters)
```

## 污点标准化

虽然histolab没有内置污点标准化，但可以使用过滤器进行基本标准化：

```python
from histolab.filters.image_filters import RgbToHed, Lambda
import numpy as np

def normalize_hed(hed_image, target_means=[0.65, 0.70], target_stds=[0.15, 0.13]):
    """Simple H&E normalization."""
    h_channel = hed_image[:, :, 0]
    e_channel = hed_image[:, :, 1]

    # Normalize hematoxylin
    h_normalized = (h_channel - h_channel.mean()) / h_channel.std()
    h_normalized = h_normalized * target_stds[0] + target_means[0]

    # Normalize eosin
    e_normalized = (e_channel - e_channel.mean()) / e_channel.std()
    e_normalized = e_normalized * target_stds[1] + target_means[1]

    hed_image[:, :, 0] = h_normalized
    hed_image[:, :, 1] = e_normalized

    return hed_image

normalization_pipeline = Compose([
    RgbToHed(),
    Lambda(normalize_hed)
    # Convert back to RGB if needed
])
```

## 最佳实践

1. **预览过滤器**：在应用于图块
2 之前，在缩略图上可视化过滤器输出。 **高效链**：按逻辑顺序排列滤波器（例如，阈值处理之前的颜色转换）
3. **调整参数**：调整特定组织
4的阈值和结构元素大小。 **使用组合**：使用`Compose`
5构建可重复使用的过滤管道。 **考虑性能**：复杂的过滤器链会增加处理时间
6. **在不同的载玻片上进行验证**：在不同的扫描仪、染色剂和组织类型
7 上测试过滤器。 **记录自定义过滤器**：清楚地描述自定义管道的用途和参数

## 质量控制过滤器

### 模糊检测

```python
from histolab.filters.image_filters import Lambda
import cv2
import numpy as np

def laplacian_blur_score(gray_image):
    """Calculate Laplacian variance (blur metric)."""
    return cv2.Laplacian(np.array(gray_image), cv2.CV_64F).var()

blur_detector = Lambda(lambda img: laplacian_blur_score(
    RgbToGrayscale()(img)
))
```

### 组织覆盖

```python
from histolab.filters.image_filters import RgbToGrayscale, OtsuThreshold
from histolab.filters.compositions import Compose

def tissue_coverage(image):
    """Calculate percentage of tissue in image."""
    tissue_mask = Compose([
        RgbToGrayscale(),
        OtsuThreshold()
    ])(image)
    return tissue_mask.sum() / tissue_mask.size * 100

coverage_filter = Lambda(tissue_coverage)
```

## 故障排除

### 问题：组织检测错过有效组织
* *解决方案：**
- 减少 `RemoveSmallObjects`
 中的 `area_threshold`- 减少侵蚀/开口盘大小
- 尝试自适应阈值而不是 Otsu

### 问题：包含太多伪影
* *解决方案：**
- 在 `RemoveSmallObjects`
 中增加 `area_threshold`- 添加打开/关闭操作
- 对特定伪影使用自定义的基于颜色的过滤

### 问题：组织边界也如此rough
* *解决方案：**
- 添加 `BinaryClosing` 或 `BinaryOpening` 进行平滑
- 调整磁盘大小以进行形态学操作

### 问题：可变染色质量
* *解决方案：**
- 应用直方图均衡
- 使用自适应阈值
- 实施染色归一化管道
