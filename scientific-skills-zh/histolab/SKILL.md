---
name: histolab
description: 轻量级 WSI 切片提取和预处理。用于 H&E 图像的基本载玻片处理组织检测、平铺提取、染色归一化。最适合简单的管道、数据集准备、基于图块的快速分析。对于高级空间蛋白质组学、多重成像或深度学习流程，请使用 pathml。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# Histolab

## 概述

Histolab 是一个用于处理数字病理学中的整个幻灯片图像 (WSI)的 Python 库。它可以自动执行组织检测，从十亿像素图像中提取信息图块，并为深度学习管道准备数据集。该库可处理多种 WSI 格式，实现复杂的组织分割，并提供灵活的切片提取策略。

## 安装

```bash
uv pip install histolab
```

## 快速入门

从整个幻灯片图像中提取切片的基本工作流程：

```python
from histolab.slide import Slide
from histolab.tiler import RandomTiler

# Load slide
slide = Slide("slide.svs", processed_path="output/")

# Configure tiler
tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=100,
    level=0,
    seed=42
)

# Preview tile locations
tiler.locate_tiles(slide, n_tiles=20)

# Extract tiles
tiler.extract(slide)
```

## 核心功能

### 1. 幻灯片管理

加载、检查和处理各种格式的整个幻灯片图像。

* *常用操作：**
- 加载 WSI 文件（SVS、TIFF、NDPI 等）
- 访问幻灯片元数据（尺寸、放大倍数、属性）
- 生成可视化缩略图
- 使用金字塔图像结构
- 提取特定坐标处的区域

* *关键类：** `Slide`

* *参考：** `references/slide_management.md` 包含有关以下内容的全面文档：
- 幻灯片初始化和配置
- 内置样本数据集（前列腺、卵巢、乳房、心脏、肾脏组织）
- 访问幻灯片属性和元数据
- 缩略图生成和可视化
- 使用金字塔级别
- 多幻灯片处理工作流程

* *示例工作流程：**
```python
from histolab.slide import Slide
from histolab.data import prostate_tissue

# Load sample data
prostate_svs, prostate_path = prostate_tissue()

# Initialize slide
slide = Slide(prostate_path, processed_path="output/")

# Inspect properties
print(f"Dimensions: {slide.dimensions}")
print(f"Levels: {slide.levels}")
print(f"Magnification: {slide.properties.get('openslide.objective-power')}")

# Save thumbnail
slide.save_thumbnail()
```

### 2. 组织检测和掩模

自动识别组织区域并过滤背景/伪影。

* *常用操作：**
- 创建二元组织掩模
- 检测最大组织区域
- 排除背景和伪影
- 自定义组织分割
- 删除笔注释

* *关键类：** `TissueMask`、`BiggestTissueBoxMask`、`BinaryMask`

* *参考：** `references/tissue_masks.md` 包含以下内容的综合文档：
- TissueMask：使用自动过滤器分割所有组织区域
- BiggestTissueBoxMask：返回最大组织区域的边界框（默认）
- BinaryMask：自定义掩模实现的基类
- 可视化掩模`locate_mask()`
- 创建自定义矩形和注释排除蒙版
- 蒙版与图块提取集成
- 最佳实践和故障排除

* *示例工作流程：**
```python
from histolab.masks import TissueMask, BiggestTissueBoxMask

# Create tissue mask for all tissue regions
tissue_mask = TissueMask()

# Visualize mask on slide
slide.locate_mask(tissue_mask)

# Get mask array
mask_array = tissue_mask(slide)

# Use largest tissue region (default for most extractors)
biggest_mask = BiggestTissueBoxMask()
```

* *何时使用每个蒙版：**
- `TissueMask`：多个组织切片，综合分析
- `BiggestTissueBoxMask`：单个主要组织切片，排除伪影（默认）
- 自定义`BinaryMask`：特定ROI，排除注释，自定义分割

### 3.平铺提取

使用不同的从大WSI中提取较小的区域策略。

* *三种提取策略：**

* *RandomTiler：**提取固定数量的随机定位的图块
- 最适合：采样不同区域、探索性分析、训练数据
- 关键参数：`n_tiles`、`seed`再现性

* *GridTiler：** 以网格图案系统地跨组织提取图块
- 最适合：完整覆盖、空间分析、重建
- 关键参数：用于滑动窗口的 `pixel_overlap`

* *ScoreTiler：** 根据评分函数提取排名靠前的图块
- 最适合：信息最丰富区域，质量驱动选择
- 关键参数：`scorer`（NucleiScorer、CellularityScorer、自定义）

* *常用参数：**
- `tile_size`：平铺尺寸（例如，(512, 512)）
- `level`：提取的金字塔级别（0 = 最高分辨率）
- `check_tissue`：按组织内容过滤图块
- `tissue_percent`：最小组织覆盖范围（默认 80%）
- `extraction_mask`：定义提取区域的掩模

* *参考：** `references/tile_extraction.md` 包含以下内容的综合文档：
- 每个分块策略的详细说明
- 可用评分器（NucleiScorer、CellularityScorer、自定义）
- 使用 `locate_tiles()`
 进行分块预览- 提取工作流程和报告
- 高级模式（多级、分层提取）
- 性能优化和故障排除

* *示例工作流程：**

```python
from histolab.tiler import RandomTiler, GridTiler, ScoreTiler
from histolab.scorer import NucleiScorer

# Random sampling (fast, diverse)
random_tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=100,
    level=0,
    seed=42,
    check_tissue=True,
    tissue_percent=80.0
)
random_tiler.extract(slide)

# Grid coverage (comprehensive)
grid_tiler = GridTiler(
    tile_size=(512, 512),
    level=0,
    pixel_overlap=0,
    check_tissue=True
)
grid_tiler.extract(slide)

# Score-based selection (most informative)
score_tiler = ScoreTiler(
    tile_size=(512, 512),
    n_tiles=50,
    scorer=NucleiScorer(),
    level=0
)
score_tiler.extract(slide, report_path="tiles_report.csv")
```

* *提取前始终预览：**
```python
# Preview tile locations on thumbnail
tiler.locate_tiles(slide, n_tiles=20)
```

### 4. 过滤器和预处理

应用用于组织检测、质量控制和预处理的图像处理滤波器。

* *滤波器类别：**

* *图像滤波器：**色彩空间转换、阈值处理、对比度增强
- `RgbToGrayscale`、`RgbToHsv`、`RgbToHed`
- `OtsuThreshold`、 `AdaptiveThreshold`
- `StretchContrast`、`HistogramEqualization`

* *形态滤波器：**对二值图像进行结构操作
- `BinaryDilation`、`BinaryErosion`
- `BinaryOpening`、`BinaryClosing`
- `RemoveSmallObjects`、`RemoveSmallHoles`

* *组成：** 将多个过滤器链接在一起
- `Compose`：创建过滤器管道

* *参考：** `references/filters_preprocessing.md` 包含以下内容的综合文档：
- 每种过滤器类型的详细说明
- 过滤器组成和链接
- 常见预处理管道（组织检测、钢笔去除、细胞核增强）
- 将过滤器应用于图块
- 自定义蒙版过滤器
- 质量控制过滤器（模糊）检测、组织覆盖）
- 最佳实践和故障排除

* *工作流程示例：**

```python
from histolab.filters.compositions import Compose
from histolab.filters.image_filters import RgbToGrayscale, OtsuThreshold
from histolab.filters.morphological_filters import (
    BinaryDilation, RemoveSmallHoles, RemoveSmallObjects
)

# Standard tissue detection pipeline
tissue_detection = Compose([
    RgbToGrayscale(),
    OtsuThreshold(),
    BinaryDilation(disk_size=5),
    RemoveSmallHoles(area_threshold=1000),
    RemoveSmallObjects(area_threshold=500)
])

# Use with custom mask
from histolab.masks import TissueMask
custom_mask = TissueMask(filters=tissue_detection)

# Apply filters to tile
from histolab.tile import Tile
filtered_tile = tile.apply_filters(tissue_detection)
```

### 5. 可视化

可视化载玻片、掩模、图块位置和提取质量。

* *常见可视化任务：**
- 显示幻灯片缩略图
- 可视化组织掩模
- 预览图块位置
- 评估图块质量
- 创建报告和数字

* *参考：** `references/visualization.md` 包含有关以下内容的综合文档：
- 幻灯片缩略图显示和保存
- 使用 `locate_mask()`
 进行掩模可视化- 使用 `locate_tiles()`
- 显示提取的图块和马赛克 
- 质量评估（分数分布、顶部 vs底部图块）
- 多幻灯片可视化
- 滤镜效果可视化
- 导出高分辨率图形和 PDF 报告
- Jupyter 笔记本中的交互式可视化

* *示例工作流程：**

```python
import matplotlib.pyplot as plt
from histolab.masks import TissueMask

# Display slide thumbnail
plt.figure(figsize=(10, 10))
plt.imshow(slide.thumbnail)
plt.title(f"Slide: {slide.name}")
plt.axis('off')
plt.show()

# Visualize tissue mask
tissue_mask = TissueMask()
slide.locate_mask(tissue_mask)

# Preview tile locations
tiler = RandomTiler(tile_size=(512, 512), n_tiles=50)
tiler.locate_tiles(slide, n_tiles=20)

# Display extracted tiles in grid
from pathlib import Path
from PIL import Image

tile_paths = list(Path("output/tiles/").glob("*.png"))[:16]
fig, axes = plt.subplots(4, 4, figsize=(12, 12))
axes = axes.ravel()

for idx, tile_path in enumerate(tile_paths):
    tile_img = Image.open(tile_path)
    axes[idx].imshow(tile_img)
    axes[idx].set_title(tile_path.stem, fontsize=8)
    axes[idx].axis('off')

plt.tight_layout()
plt.show()
```

## 典型工作流程

### 工作流程 1：探索性平铺提取

对不同组织区域进行快速采样以进行初始分析。

```python
from histolab.slide import Slide
from histolab.tiler import RandomTiler
import logging

# Enable logging for progress tracking
logging.basicConfig(level=logging.INFO)

# Load slide
slide = Slide("slide.svs", processed_path="output/random_tiles/")

# Inspect slide
print(f"Dimensions: {slide.dimensions}")
print(f"Levels: {slide.levels}")
slide.save_thumbnail()

# Configure random tiler
random_tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=100,
    level=0,
    seed=42,
    check_tissue=True,
    tissue_percent=80.0
)

# Preview locations
random_tiler.locate_tiles(slide, n_tiles=20)

# Extract tiles
random_tiler.extract(slide)
```

### 工作流程 2：综合网格提取

整个载玻片的完整组织覆盖分析。

```python
from histolab.slide import Slide
from histolab.tiler import GridTiler
from histolab.masks import TissueMask

# Load slide
slide = Slide("slide.svs", processed_path="output/grid_tiles/")

# Use TissueMask for all tissue sections
tissue_mask = TissueMask()
slide.locate_mask(tissue_mask)

# Configure grid tiler
grid_tiler = GridTiler(
    tile_size=(512, 512),
    level=1,  # Use level 1 for faster extraction
    pixel_overlap=0,
    check_tissue=True,
    tissue_percent=70.0
)

# Preview grid
grid_tiler.locate_tiles(slide)

# Extract all tiles
grid_tiler.extract(slide, extraction_mask=tissue_mask)
```

### 工作流程 3：质量驱动的图块选择

根据核密度提取信息最丰富的图块。

```python
from histolab.slide import Slide
from histolab.tiler import ScoreTiler
from histolab.scorer import NucleiScorer
import pandas as pd
import matplotlib.pyplot as plt

# Load slide
slide = Slide("slide.svs", processed_path="output/scored_tiles/")

# Configure score tiler
score_tiler = ScoreTiler(
    tile_size=(512, 512),
    n_tiles=50,
    level=0,
    scorer=NucleiScorer(),
    check_tissue=True
)

# Preview top tiles
score_tiler.locate_tiles(slide, n_tiles=15)

# Extract with report
score_tiler.extract(slide, report_path="tiles_report.csv")

# Analyze scores
report_df = pd.read_csv("tiles_report.csv")
plt.hist(report_df['score'], bins=20, edgecolor='black')
plt.xlabel('Tile Score')
plt.ylabel('Frequency')
plt.title('Distribution of Tile Scores')
plt.show()
```

### 工作流程 4：多幻灯片处理管道

处理整个具有一致参数的载玻片集合。

```python
from pathlib import Path
from histolab.slide import Slide
from histolab.tiler import RandomTiler
import logging

logging.basicConfig(level=logging.INFO)

# Configure tiler once
tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=50,
    level=0,
    seed=42,
    check_tissue=True
)

# Process all slides
slide_dir = Path("slides/")
output_base = Path("output/")

for slide_path in slide_dir.glob("*.svs"):
    print(f"\nProcessing: {slide_path.name}")

    # Create slide-specific output directory
    output_dir = output_base / slide_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load and process slide
    slide = Slide(slide_path, processed_path=output_dir)

    # Save thumbnail for review
    slide.save_thumbnail()

    # Extract tiles
    tiler.extract(slide)

    print(f"Completed: {slide_path.name}")
```

### 工作流程 5：自定义组织检测和过滤

处理带有伪影、注释或异常染色的载玻片。

```python
from histolab.slide import Slide
from histolab.masks import TissueMask
from histolab.tiler import RandomTiler
from histolab.filters.compositions import Compose
from histolab.filters.image_filters import RgbToGrayscale, OtsuThreshold
from histolab.filters.morphological_filters import (
    BinaryDilation, RemoveSmallObjects, RemoveSmallHoles
)

# Define custom filter pipeline for aggressive artifact removal
aggressive_filters = Compose([
    RgbToGrayscale(),
    OtsuThreshold(),
    BinaryDilation(disk_size=10),
    RemoveSmallHoles(area_threshold=5000),
    RemoveSmallObjects(area_threshold=3000)  # Remove larger artifacts
])

# Create custom mask
custom_mask = TissueMask(filters=aggressive_filters)

# Load slide and visualize mask
slide = Slide("slide.svs", processed_path="output/")
slide.locate_mask(custom_mask)

# Extract with custom mask
tiler = RandomTiler(tile_size=(512, 512), n_tiles=100)
tiler.extract(slide, extraction_mask=custom_mask)
```

## 最佳实践

### 载玻片加载和检查
1. 在加工 
2 之前务必检查载玻片属性。保存缩略图以便快速查看
3. 检查金字塔层数和尺寸
4. 使用缩略图

### 组织检测
1 验证组织是否存在。在提取
2之前使用`locate_mask()`预览蒙版。多节使用`TissueMask`，单节使用`BiggestTissueBoxMask`
3. 针对特定污渍定制过滤器（H&E 与 IHC）
4. 使用自定义蒙版
5 处理笔注释。在不同的载玻片上测试面罩

### 瓷砖提取
1. **解压前始终使用 `locate_tiles()` 进行预览**
2. 选择合适的tiler：
  - RandomTiler：采样和探索
  - GridTiler：完整覆盖
  - ScoreTiler：质量驱动的选择
3. 设置适当的 `tissue_percent` 阈值（典型值为 70-90%）
4. 在 RandomTiler
5 中使用种子来实现再现性。在适当的金字塔级别提取以获得分析分辨率
6. 为大型数据集启用日志记录

### 性能
1. 以较低级别（1、2）提取以加快处理速度
2. 适当时使用 `BiggestTissueBoxMask` 而不是 `TissueMask`
3. 调整 `tissue_percent` 以减少无效平铺尝试 
4. 初步探索限制`n_tiles`
5. 使用 `pixel_overlap=0` 进行非重叠网格

### 质量控制
1. 验证图块质量（检查模糊、伪影、焦点）
2. 查看 ScoreTiler
3 的分数分布。检查顶部和底部得分瓷砖
4. 监测组织覆盖率统计
5. 如果需要，可以通过其他质量指标过滤提取的图块

## 常见用例

### 训练深度学习模型
- 使用 RandomTiler 在多个幻灯片中提取平衡数据集
- 将 ScoreTiler 与 NucleiScorer 结合使用，重点关注细胞丰富的区域
- 以一致的分辨率（0 级或 1 级）提取1)
- 生成 CSV 报告以跟踪图块元数据

### 整体幻灯片分析
- 使用 GridTiler 进行完整的组织覆盖
- 在多个金字塔级别提取以进行分层分析
- 维护与网格位置的空间关系
- 使用 `pixel_overlap` 进行滑动窗口方法

### 组织表征
- 使用 RandomTiler 对不同区域进行采样
- 使用掩模量化组织覆盖范围
- 使用 HED 分解提取染色特定信息
- 比较载玻片上的组织模式

### 质量评估
- 使用 ScoreTiler 识别最佳焦点区域
- 使用自定义掩模和过滤器检测伪影
- 评估整个载玻片集合的染色质量
- 标记有问题的载玻片以供手动审查

### 数据集管理
- 使用 ScoreTiler 优先考虑信息图块
- 按组织过滤图块百分比
- 生成包含图块分数和元数据的报告
- 跨载玻片和组织类型创建分层数据集

## 故障排除

### 未提取图块
- 较低的`tissue_percent`阈值
- 验证载玻片包含组织（检查缩略图）
- 确保extract_mask 捕获组织区域
- 检查tile_size 是否适合载玻片分辨率

### 许多背景图块
- 启用`check_tissue=True`
- 增加`tissue_percent` 阈值
- 使用适当的掩模（TissueMask 与BiggestTissueBoxMask)
- 自定义掩模过滤器以更好地检测组织

### 提取非常慢
- 在较低金字塔级别提取（级别= 1 或 2）
- 减少 RandomTiler/ScoreTiler 的 `n_tiles`
- 使用 RandomTiler 而不是 GridTiler采样
- 使用BiggestTissueBoxMask代替TissueMask

### 图块有伪影
- 实现自定义注释排除蒙版
- 调整过滤器参数以去除伪影
- 增加小对象去除阈值
- 应用提取后质量过滤

### 载玻片之间的结果不一致
- 对 RandomTiler 使用相同的种子
- 使用预处理过滤器标准化染色
- 根据染色质量调整 `tissue_percent`
- 实施载玻片特定掩模定制

## 资源

此技能包括详细的参考文档`references/`目录：

### references/slide_management.md
加载、检查和处理整个幻灯片图像的综合指南：
- 幻灯片初始化和配置
- 内置示例数据集
- 幻灯片属性和元数据
- 缩略图生成和可视化
- 使用金字塔级别
- 多玻片处理工作流程
- 最佳实践和常见模式

### references/tissue_masks.md
有关组织检测和遮蔽的完整文档：
- TissueMask、BiggestTissueBoxMask、BinaryMask 类
- 组织检测过滤器的工作原理
- 使用过滤器自定义遮罩链
- 可视化蒙版
- 创建自定义矩形和注释排除蒙版
- 与图块提取集成
- 最佳实践和故障排除

### 引用/tile_extraction.md
图块提取策略的详细说明：
- RandomTiler、GridTiler、 ScoreTiler 比较
- 可用评分器（NucleiScorer、CellularityScorer、自定义）
- 通用和特定于策略的参数
- 使用locate_tiles()进行图块预览
- 提取工作流程和 CSV 报告
- 高级模式（多级、分层）
- 性能优化
- 常见问题排查

### references/filters_preprocessing.md
完整滤镜参考和预处理指南：
- 图像滤镜（颜色转换、阈值处理、对比度）
- 形态滤镜（膨胀、腐蚀、开、闭）
- 滤镜组成和链接
- 通用预处理管道
- 将过滤器应用于图块
- 自定义蒙版过滤器
- 质量控制过滤器
- 最佳实践和故障排除

### 引用/可视化.md
综合可视化指南：
- 幻灯片缩略图显示和保存
- 蒙版可视化技术
- 图块位置预览
- 显示提取的图块并创建马赛克
- 质量评估可视化
- 多幻灯片比较
- 过滤器效果可视化
- 导出高分辨率图形和PDF
- Jupyter 笔记本中的交互式可视化

* *使用模式：** 参考文件包含支持本主要技能文档中描述的工作流程的深入信息。根据需要加载特定的参考文件，以获取详细的实施指南、故障排除或高级功能。
