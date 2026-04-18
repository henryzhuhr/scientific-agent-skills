# 图像加载和格式

## 概述

PathML 为从 160 多种专有医学成像格式加载整个幻灯片图像 (WSI)提供全面支持。该框架通过统一的幻灯片类和接口抽象出供应商特定的复杂性，从而能够跨不同文件格式无缝访问图像金字塔、元数据和感兴趣区域。

## 支持的格式

PathML 支持以下幻灯片格式：

### 明场显微镜格式
- **Aperio SVS** (`.svs`) - Leica Biosystems
- **滨松 NDPI** (`.ndpi`) - 滨松光子学 
- **徕卡 SCN** (`.scn`) - 徕卡 Biosystems
- **蔡司 ZVI** (`.zvi`) - 卡尔蔡司
- **3DHISTECH** (`.mrxs`) - 3DHISTECH Ltd.
- **Ventana BIF** (`.bif`) - Roche Ventana
- **通用平铺 TIFF** (`.tif`、`.tiff`)

### 医学成像标准
- **DICOM** (`.dcm`) - 医学数字成像和通信
- **OME-TIFF** (`.ome.tif`、`.ome.tiff`) - 开放显微镜环境

### 多参数成像
- **CODEX** - 空间蛋白质组学成像
- **Vectra** (`.qptiff`) - 多重免疫荧光
- **MERFISH** - 多重抗误差 FISH

PathML 利用 OpenSlide 和其他专用库自动处理格式特定的细微差别。

## 用于加载图像的核心类

### SlideData

`SlideData` 是 PathML 中表示整个幻灯片图像的基础类。

* *从文件加载：**
```python
from pathml.core import SlideData

# Load a whole-slide image
wsi = SlideData.from_slide("path/to/slide.svs")

# Load with specific backend
wsi = SlideData.from_slide("path/to/slide.svs", backend="openslide")

# Load from OME-TIFF
wsi = SlideData.from_slide("path/to/slide.ome.tiff", backend="bioformats")
```

* *关键属性：**
- `wsi.slide` - 后端幻灯片对象（OpenSlide、BioFormats 等）
- `wsi.tiles` - 图像图块集合
- `wsi.metadata` - 幻灯片元数据字典
- `wsi.level_dimensions` - 图像金字塔级别尺寸
- `wsi.level_downsamples` - 每个金字塔的下采样因子级别

* *方法：**
- `wsi.generate_tiles()` - 从幻灯片生成图块
- `wsi.read_region()` - 读取给定级别的特定区域
- `wsi.get_thumbnail()` - 获取缩略图

### SlideType

`SlideType` 是一个定义支持的幻灯片后端的枚举：

```python
from pathml.core import SlideType

# Available backends
SlideType.OPENSLIDE  # For most WSI formats (SVS, NDPI, etc.)
SlideType.BIOFORMATS  # For OME-TIFF and other formats
SlideType.DICOM  # For DICOM WSI
SlideType.VectraQPTIFF  # For Vectra multiplex IF
```

### 专用幻灯片类

PathML 为特定成像提供专用幻灯片类模式：

* *CODEXSlide：**
```python
from pathml.core import CODEXSlide

# Load CODEX spatial proteomics data
codex_slide = CODEXSlide(
    path="path/to/codex_dir",
    stain="IF",  # Immunofluorescence
    backend="bioformats"
)
```

* *VectraSlide：**
```python
from pathml.core import types

# Load Vectra multiplex IF data
vectra_slide = SlideData.from_slide(
    "path/to/vectra.qptiff",
    backend=SlideType.VectraQPTIFF
)
```

* *多参数Slide：**
```python
from pathml.core import MultiparametricSlide

# Generic multiparametric imaging
mp_slide = MultiparametricSlide(path="path/to/multiparametric_data")
```

## 加载策略

### 基于图块的加载

对于大型 WSI 文件，基于图块的加载可实现内存高效处理：

```python
from pathml.core import SlideData

# Load slide
wsi = SlideData.from_slide("path/to/slide.svs")

# Generate tiles at specific magnification level
wsi.generate_tiles(
    level=0,  # Pyramid level (0 = highest resolution)
    tile_size=256,  # Tile dimensions in pixels
    stride=256,  # Spacing between tiles (256 = no overlap)
    pad=False  # Whether to pad edge tiles
)

# Iterate over tiles
for tile in wsi.tiles:
    image = tile.image  # numpy array
    coords = tile.coords  # (x, y) coordinates
    # Process tile...
```

* *重叠图块：**
```python
# Generate tiles with 50% overlap
wsi.generate_tiles(
    level=0,
    tile_size=256,
    stride=128  # 50% overlap
)
```

### 基于区域加载

直接提取特定的感兴趣区域：

```python
# Read region at specific location and level
region = wsi.read_region(
    location=(10000, 15000),  # (x, y) in level 0 coordinates
    level=1,  # Pyramid level
    size=(512, 512)  # Width, height in pixels
)

# Returns numpy array
```

### 金字塔级别选择

整个幻灯片图像存储在多分辨率金字塔中。根据所需的放大倍率选择适当的级别：

```python
# Inspect available levels
print(wsi.level_dimensions)  # [(width0, height0), (width1, height1), ...]
print(wsi.level_downsamples)  # [1.0, 4.0, 16.0, ...]

# Load at lower resolution for faster processing
wsi.generate_tiles(level=2, tile_size=256)  # Use level 2 (16x downsampled)
```

* *常见金字塔级别：**
- 级别 0：全分辨率（例如，40 倍放大倍率）
- 级别 1：4 倍下采样（例如，10 倍）放大）
- 级别 2：16 倍下采样（例如，2.5 倍放大倍率）
- 级别 3：64 倍下采样（缩略图）

### 缩略图加载

生成低分辨率缩略图以实现可视化和质量control:

```python
# Get thumbnail
thumbnail = wsi.get_thumbnail(size=(1024, 1024))

# Display with matplotlib
import matplotlib.pyplot as plt
plt.imshow(thumbnail)
plt.axis('off')
plt.show()
```

## 使用SlideDataset批量加载

使用`SlideDataset`高效处理多个幻灯片：

```python
from pathml.core import SlideDataset
import glob

# Create dataset from multiple slides
slide_paths = glob.glob("data/*.svs")
dataset = SlideDataset(
    slide_paths,
    tile_size=256,
    stride=256,
    level=0
)

# Iterate over all tiles from all slides
for tile in dataset:
    image = tile.image
    slide_id = tile.slide_id
    # Process tile...
```

* *带预处理管道：**
```python
from pathml.preprocessing import Pipeline, StainNormalizationHE

# Create pipeline
pipeline = Pipeline([
    StainNormalizationHE(target='normalize')
])

# Apply to entire dataset
dataset = SlideDataset(slide_paths)
dataset.run(pipeline, distributed=True, n_workers=8)
```

## 元数据访问

提取幻灯片元数据，包括采集参数、放大倍数和供应商特定信息：

```python
# Access metadata
metadata = wsi.metadata

# Common metadata fields
print(metadata.get('openslide.objective-power'))  # Magnification
print(metadata.get('openslide.mpp-x'))  # Microns per pixel X
print(metadata.get('openslide.mpp-y'))  # Microns per pixel Y
print(metadata.get('openslide.vendor'))  # Scanner vendor

# Slide dimensions
print(wsi.level_dimensions[0])  # (width, height) at level 0
```

## 使用DICOM幻灯片

PathML通过专门的支持DICOM WSI处理：

```python
from pathml.core import SlideData, SlideType

# Load DICOM WSI
dicom_slide = SlideData.from_slide(
    "path/to/slide.dcm",
    backend=SlideType.DICOM
)

# DICOM-specific metadata
print(dicom_slide.metadata.get('PatientID'))
print(dicom_slide.metadata.get('StudyDate'))
```

## 使用 OME-TIFF

OME-TIFF 为多维成像提供开放标准：

```python
from pathml.core import SlideData

# Load OME-TIFF
ome_slide = SlideData.from_slide(
    "path/to/slide.ome.tiff",
    backend="bioformats"
)

# Access channel information for multi-channel images
n_channels = ome_slide.shape[2]  # Number of channels
```

## 性能注意事项

### 内存管理

对于大型 WSI 文件（通常 >1GB），使用基于图块的加载以避免内存耗尽：

```python
# Efficient: Tile-based processing
wsi.generate_tiles(level=1, tile_size=256)
for tile in wsi.tiles:
    process_tile(tile)  # Process one tile at a time

# Inefficient: Loading entire slide into memory
full_image = wsi.read_region((0, 0), level=0, wsi.level_dimensions[0])  # May crash
```

### 分布式处理

使用 Dask 跨多个工作线程进行并行处理：

```python
from pathml.core import SlideDataset
from dask.distributed import Client

# Start Dask client
client = Client(n_workers=8, threads_per_worker=2)

# Process dataset in parallel
dataset = SlideDataset(slide_paths)
dataset.run(pipeline, distributed=True, client=client)
```

### 级别选择

通过选择适当的金字塔级别来平衡分辨率和性能：

- **级别 0：** 用于需要最大细节的最终分析
- **级别 1-2：** 用于大多数预处理和模型训练
- **级别 3+：** 用于缩略图、质量控制和快速探索

## 常见问题和解决方案

* *问题：幻灯片无法加载**
- 验证是否支持文件格式
- 检查文件权限和路径
- 尝试不同的后端：`backend="bioformats"`或`backend="openslide"`

* *问题：内存不足错误**
- 使用基于图块的加载而不是全幻灯片加载
- 在较低金字塔级别进行处理（例如，level=1或level=2）
- 减少tile_size参数
- 使用Dask启用分布式处理

* *问题：幻灯片之间的颜色不一致**
- 应用染色归一化预处理（请参阅`preprocessing.md`)
- 检查扫描仪元数据以获取校准信息
- 在预处理管道中使用 `StainNormalizationHE` 转换

* *问题：元数据丢失或不正确**
- 不同供应商将元数据存储在不同位置
- 使用 `wsi.metadata` 检查可用的元数据字段
- 某些格式可能具有有限的元数据支持

## 最佳实践

1. **处理前始终检查金字塔结构**：检查 `level_dimensions` 和 `level_downsamples` 以了解可用的分辨率

2. **使用适当的金字塔级别**：大多数任务在 1-2 级进行处理；保留0级用于最终高分辨率分析

3. **具有重叠的平铺**用于分割任务：使用 stride <tile_size 以避免边缘伪影

4. **验证放大倍数一致性**：组合不同来源的幻灯片时检查 `openslide.objective-power` 元数据

5. **处理供应商特定格式**：对多参数数据使用专用幻灯片类（CODEXSlide、VectraSlide）

6. **实施质量控制**：在处理之前生成缩略图并检查伪影

7. **对大型数据集使用分布式处理**：利用 Dask 跨多个工作线程进行并行处理

## 示例工作流程

### 加载和检查新幻灯片

```python
from pathml.core import SlideData
import matplotlib.pyplot as plt

# Load slide
wsi = SlideData.from_slide("path/to/slide.svs")

# Inspect properties
print(f"Dimensions: {wsi.level_dimensions}")
print(f"Downsamples: {wsi.level_downsamples}")
print(f"Magnification: {wsi.metadata.get('openslide.objective-power')}")

# Generate thumbnail for QC
thumbnail = wsi.get_thumbnail(size=(1024, 1024))
plt.imshow(thumbnail)
plt.title(f"Slide: {wsi.name}")
plt.axis('off')
plt.show()
```

### 处理多个幻灯片

```python
from pathml.core import SlideDataset
from pathml.preprocessing import Pipeline, TissueDetectionHE
import glob

# Find all slides
slide_paths = glob.glob("data/slides/*.svs")

# Create pipeline
pipeline = Pipeline([TissueDetectionHE()])

# Process all slides
dataset = SlideDataset(
    slide_paths,
    tile_size=512,
    stride=512,
    level=1
)

# Run pipeline with distributed processing
dataset.run(pipeline, distributed=True, n_workers=8)

# Save processed data
dataset.to_hdf5("processed_dataset.h5")
```

### 加载 CODEX 多参数数据

```python
from pathml.core import CODEXSlide
from pathml.preprocessing import Pipeline, CollapseRunsCODEX, SegmentMIF

# Load CODEX slide
codex = CODEXSlide("path/to/codex_dir", stain="IF")

# Create CODEX-specific pipeline
pipeline = Pipeline([
    CollapseRunsCODEX(z_slice=2),  # Select z-slice
    SegmentMIF(
        nuclear_channel='DAPI',
        cytoplasm_channel='CD45',
        model='mesmer'
    )
])

# Process
pipeline.run(codex)
```

## 其他资源

- **PathML 文档：** https://pathml.readthedocs.io/
- **OpenSlide：** https://openslide.org/（WSI 格式的底层库）
- **Bio-Formats：** https://www.openmicroscopy.org/bio-formats/（替代后端）
- **DICOM 标准：** https://www.dicomstandard.org/
