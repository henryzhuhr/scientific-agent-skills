# 幻灯片管理

## 概述

`Slide` 类是在 histolab 中处理整个幻灯片图像 (WSI)的主要接口。它提供了加载、检查和处理以各种格式存储的大型组织病理学图像的方法。

## 初始化

```python
from histolab.slide import Slide

# Initialize a slide with a WSI file and output directory
slide = Slide(processed_path="path/to/processed/output",
              slide_path="path/to/slide.svs")
```

* *参数：**
- `slide_path`：整个幻灯片图像文件的路径（支持多种格式：SVS、TIFF、NDPI等）
- `processed_path`：保存处理后的输出（图块、缩略图等）的目录

## 加载示例数据

Histolab提供来自TCGA的内置示例数据集用于测试和演示：

```python
from histolab.data import prostate_tissue, ovarian_tissue, breast_tissue, heart_tissue, kidney_tissue

# Load prostate tissue sample
prostate_svs, prostate_path = prostate_tissue()
slide = Slide(prostate_path, processed_path="output/")
```

可用示例数据集：
- `prostate_tissue()`：前列腺组织样本
- `ovarian_tissue()`：卵巢组织样本
- `breast_tissue()`：乳腺组织样本
- `heart_tissue()`：心脏组织样本
- `kidney_tissue()`：肾脏组织示例

## 关键属性

### 幻灯片尺寸
```python
# Get slide dimensions at level 0 (highest resolution)
width, height = slide.dimensions

# Get dimensions at specific pyramid level
level_dimensions = slide.level_dimensions
# Returns tuple of (width, height) for each level
```

### 放大倍数信息
```python
# Get base magnification (e.g., 40x, 20x)
base_mag = slide.base_mpp  # Microns per pixel at level 0

# Get all available levels
num_levels = slide.levels  # Number of pyramid levels
```

### 幻灯片属性
```python
# Access OpenSlide properties dictionary
properties = slide.properties

# Common properties include:
# - slide.properties['openslide.objective-power']: Objective power
# - slide.properties['openslide.mpp-x']: Microns per pixel in X
# - slide.properties['openslide.mpp-y']: Microns per pixel in Y
# - slide.properties['openslide.vendor']: Scanner vendor
```

## 缩略图生成

```python
# Get thumbnail at specific size
thumbnail = slide.thumbnail

# Save thumbnail to disk
slide.save_thumbnail()  # Saves to processed_path

# Get scaled thumbnail
scaled_thumbnail = slide.scaled_image(scale_factor=32)
```

## 幻灯片可视化

```python
# Display slide thumbnail with matplotlib
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 10))
plt.imshow(slide.thumbnail)
plt.title(f"Slide: {slide.name}")
plt.axis('off')
plt.show()
```

## 提取区域

```python
# Extract region at specific coordinates and level
region = slide.extract_region(
    location=(x, y),  # Top-left coordinates at level 0
    size=(width, height),  # Region size
    level=0  # Pyramid level
)
```

## 使用金字塔级别

WSI 文件使用具有多个分辨率级别的金字塔结构：
- 级别 0：最高分辨率（本机扫描分辨率）
- 级别 1+：逐渐降低分辨率以获得更快的速度访问

```python
# Check available levels
for level in range(slide.levels):
    dims = slide.level_dimensions[level]
    downsample = slide.level_downsamples[level]
    print(f"Level {level}: {dims}, downsample: {downsample}x")
```

## 幻灯片名称和路径

```python
# Get slide filename without extension
slide_name = slide.name

# Get full path to slide file
slide_path = slide.scaled_image
```

## 最佳实践

1. **始终指定processed_pa​​th**：在专用目录
2中组织输出。 **处理前检查尺寸**：大型幻灯片可能会超出内存限制
3. **使用适当的金字塔级别**：在与您的分析分辨率
4匹配的级别提取图块。 **使用缩略图预览**：在繁重处理之前使用缩略图进行快速可视化
5. **监控内存使用情况**：大型幻灯片上的 0 级操作需要大量 RAM

## 常用工作流程

### 载玻片检查工作流程
```python
from histolab.slide import Slide

# Load slide
slide = Slide("slide.svs", processed_path="output/")

# Inspect properties
print(f"Dimensions: {slide.dimensions}")
print(f"Levels: {slide.levels}")
print(f"Magnification: {slide.properties.get('openslide.objective-power', 'N/A')}")

# Save thumbnail for review
slide.save_thumbnail()
```

### 多载玻片处理
```python
import os
from pathlib import Path

slide_dir = Path("slides/")
output_dir = Path("processed/")

for slide_path in slide_dir.glob("*.svs"):
    slide = Slide(slide_path, processed_path=output_dir / slide_path.stem)
    # Process each slide
    print(f"Processing: {slide.name}")
```
