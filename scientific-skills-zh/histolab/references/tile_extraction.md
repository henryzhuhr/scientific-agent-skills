# 平铺提取

## 概述

平铺提取是从大型整个幻灯片图像中裁剪更小、可管理区域的过程。 Histolab提供三种主要的提取策略，每种策略适合不同的分析需求。所有切片器共享通用参数，并提供预览和提取切片的方法。

## 通用参数

所有切片器类都接受这些参数：

```python
tile_size: tuple = (512, 512)           # Tile dimensions in pixels (width, height)
level: int = 0                          # Pyramid level for extraction (0=highest resolution)
check_tissue: bool = True               # Filter tiles by tissue content
tissue_percent: float = 80.0            # Minimum tissue coverage (0-100)
pixel_overlap: int = 0                  # Overlap between adjacent tiles (GridTiler only)
prefix: str = ""                        # Prefix for saved tile filenames
suffix: str = ".png"                    # File extension for saved tiles
extraction_mask: BinaryMask = BiggestTissueBoxMask()  # Mask defining extraction region
```

## RandomTiler

* *用途：**从组织中提取固定数量的随机定位的切片Regions.

```python
from histolab.tiler import RandomTiler

random_tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=100,                # Number of random tiles to extract
    level=0,
    seed=42,                    # Random seed for reproducibility
    check_tissue=True,
    tissue_percent=80.0
)

# Extract tiles
random_tiler.extract(slide, extraction_mask=TissueMask())
```

* *关键参数：**
- `n_tiles`：要提取的随机图块数量
- `seed`：用于可重现图块选择的随机种子
- `max_iter`：查找有效图块的最大尝试次数（默认） 1000)

* *用例：**
- 幻灯片内容的探索性分析
- 对训练数据的不同区域进行采样
- 组织特征的快速评估
- 从多个幻灯片创建平衡的数据集

* *优点：**
- 计算高效
- 适合对不同组织形态进行采样
- 可通过种子参数重现
- 快速执行

* *限制：**
- 可能会错过罕见的组织模式
- 无法保证覆盖范围
- 随机分布可能无法捕获结构化特征

## GridTiler

* *用途：**按照网格图案在组织区域系统地提取图块。

```python
from histolab.tiler import GridTiler

grid_tiler = GridTiler(
    tile_size=(512, 512),
    level=0,
    check_tissue=True,
    tissue_percent=80.0,
    pixel_overlap=0             # Overlap in pixels between adjacent tiles
)

# Extract tiles
grid_tiler.extract(slide)
```

* *关键参数：**
- `pixel_overlap`：相邻图块之间重叠像素的数量
  - `pixel_overlap=0`：非重叠图块
  - `pixel_overlap=128`：每侧 128 像素重叠
  - 可用于滑动窗口方法

  * *使用案例：**
  - 全面的幻灯片覆盖
  - 需要位置信息的空间分析
  - 图像从图块重建
- 语义分割任务
- 基于区域的分析

* *优点：**
- 完整的组织覆盖
- 保留空间关系
- 可预测的图块位置
- 适合整个幻灯片分析

* *局限性：**
- 大型幻灯片的计算密集型
- 可能会生成许多背景重的图块（通过`check_tissue`)
- 更大的输出数据集

* *网格图案：**
```
[Tile 1][Tile 2][Tile 3]
[Tile 4][Tile 5][Tile 6]
[Tile 7][Tile 8][Tile 9]
```

与`pixel_overlap=64`:
```
[Tile 1-overlap-Tile 2-overlap-Tile 3]
[    overlap       overlap       overlap]
[Tile 4-overlap-Tile 5-overlap-Tile 6]
```

## ScoreTiler

* *用途：**根据自定义评分函数提取排名靠前的图块。

```python
from histolab.tiler import ScoreTiler
from histolab.scorer import NucleiScorer

score_tiler = ScoreTiler(
    tile_size=(512, 512),
    n_tiles=50,                 # Number of top-scoring tiles to extract
    level=0,
    scorer=NucleiScorer(),      # Scoring function
    check_tissue=True
)

# Extract top-scoring tiles
score_tiler.extract(slide)
```

* *关键参数：**
- `n_tiles`：要提取的排名靠前的图块数量
- `scorer`：评分函数（例如，`NucleiScorer`、`CellularityScorer`、自定义评分器）

* *用例：**
- 提取信息最多的区域
- 优先考虑具有特定特征（细胞核、细胞等）的图块 
- 基于质量的图块选择
- 专注于诊断相关领域
- 训练数据管理

* *优点：**
- 专注于信息最丰富的图块
- 减少数据集大小，同时保持质量
- 可使用不同的评分器进行定制
- 有效针对目标分析

* *限制：**
- 比RandomTiler慢（必须对所有候选图块进行评分）
- 任务需要适当的评分者
- 可能会错过低分但相关的区域

## 可用评分者

### NucleiScorer

根据原子核检测和密度对图块进行评分。

```python
from histolab.scorer import NucleiScorer

nuclei_scorer = NucleiScorer()
```

* *工作原理：**
1. 将图块转换为灰度
2. 应用阈值检测细胞核 
3. 计算类核结构
4. 根据细胞核密度分配分数

* *最适合：**
- 细胞丰富的组织区域
- 肿瘤检测
- 有丝分裂分析
- 细胞含量高的区域

### CellularityScorer

根据整体细胞对图块进行评分content.

```python
from histolab.scorer import CellularityScorer

cellularity_scorer = CellularityScorer()
```

* *最适合：**
- 识别细胞与基质区域
- 肿瘤细胞结构评估
- 将密集组织区域与稀疏组织区域分开

### 自定义评分器

根据特定需求创建自定义评分函数：

```python
from histolab.scorer import Scorer
import numpy as np

class ColorVarianceScorer(Scorer):
    def __call__(self, tile):
        """Score tiles based on color variance."""
        tile_array = np.array(tile.image)
        # Calculate color variance
        variance = np.var(tile_array, axis=(0, 1)).sum()
        return variance

# Use custom scorer
variance_scorer = ColorVarianceScorer()
score_tiler = ScoreTiler(
    tile_size=(512, 512),
    n_tiles=30,
    scorer=variance_scorer
)
```

## 使用locate_tiles()进行图块预览

在提取之前预览图块位置以验证图块配置：

```python
# Preview random tile locations
random_tiler.locate_tiles(
    slide=slide,
    extraction_mask=TissueMask(),
    n_tiles=20  # Number of tiles to preview (for RandomTiler)
)
```

这将显示带有指示图块的彩色矩形的幻灯片缩略图Positions.

## 提取工作流程

### 基本提取

```python
from histolab.slide import Slide
from histolab.tiler import RandomTiler

# Load slide
slide = Slide("slide.svs", processed_path="output/tiles/")

# Configure tiler
tiler = RandomTiler(
    tile_size=(512, 512),
    n_tiles=100,
    level=0,
    seed=42
)

# Extract tiles (saved to processed_path)
tiler.extract(slide)
```

### 使用日志记录提取

```python
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

# Extract tiles with progress information
tiler.extract(slide)
# Output: INFO: Tile 1/100 saved...
# Output: INFO: Tile 2/100 saved...
```

### 使用日志提取报告

```python
# Generate CSV report with tile information
score_tiler = ScoreTiler(
    tile_size=(512, 512),
    n_tiles=50,
    scorer=NucleiScorer()
)

# Extract and save report
score_tiler.extract(slide, report_path="tiles_report.csv")

# Report contains: tile name, coordinates, score, tissue percentage
```

报告格式：
```csv
tile_name,x_coord,y_coord,level,score,tissue_percent
tile_001.png,10240,5120,0,0.89,95.2
tile_002.png,15360,7680,0,0.85,91.7
...
```

## 高级提取模式

### 多级提取

以不同放大倍数提取图块级别：

```python
# High resolution tiles (level 0)
high_res_tiler = RandomTiler(tile_size=(512, 512), n_tiles=50, level=0)
high_res_tiler.extract(slide)

# Medium resolution tiles (level 1)
med_res_tiler = RandomTiler(tile_size=(512, 512), n_tiles=50, level=1)
med_res_tiler.extract(slide)

# Low resolution tiles (level 2)
low_res_tiler = RandomTiler(tile_size=(512, 512), n_tiles=50, level=2)
low_res_tiler.extract(slide)
```

### 分层提取

从同一位置以多个比例提取：

```python
# Extract random locations at level 0
random_tiler_l0 = RandomTiler(
    tile_size=(512, 512),
    n_tiles=30,
    level=0,
    seed=42,
    prefix="level0_"
)
random_tiler_l0.extract(slide)

# Extract same locations at level 1 (use same seed)
random_tiler_l1 = RandomTiler(
    tile_size=(512, 512),
    n_tiles=30,
    level=1,
    seed=42,
    prefix="level1_"
)
random_tiler_l1.extract(slide)
```

### 自定义平铺过滤

在之后应用附加过滤提取：

```python
from PIL import Image
import numpy as np
from pathlib import Path

def filter_blurry_tiles(tile_dir, threshold=100):
    """Remove blurry tiles using Laplacian variance."""
    for tile_path in Path(tile_dir).glob("*.png"):
        img = Image.open(tile_path)
        gray = np.array(img.convert('L'))
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

        if laplacian_var < threshold:
            tile_path.unlink()  # Remove blurry tile
            print(f"Removed blurry tile: {tile_path.name}")

# Use after extraction
tiler.extract(slide)
filter_blurry_tiles("output/tiles/")
```

## 最佳实践

1. **提取前预览**：始终使用 `locate_tiles()` 验证图块放置 
2. **使用适当的级别**：将提取级别与分析分辨率要求相匹配
3. **设置组织百分比阈值**：根据染色和组织类型进行调整（典型值为 70-90%）
4. **选择正确的tiler**：
  - 用于采样和探索的RandomTiler
  - 用于全面覆盖的GridTiler
  - 用于有针对性的、质量驱动的提取的ScoreTiler
5. **启用日志记录**：监控大型数据集
6的提取进度。 **使用种子实现再现性**：在 RandomTiler
7 中设置随机种子。 **考虑存储**：GridTiler 可以为每个幻灯片生成数千个图块
8. **验证图块质量**：检查提取的图块是否存在伪影、模糊或焦点问题

## 性能优化

1. **在适当的级别提取**：较低级别（1、2）提取速度更快
2. **调整组织百分比**：较高的阈值会减少无效的平铺尝试
3. **使用 BiggestTissueBoxMask**：对于单个组织切片 
4，比 TissueMask 更快。 **限制 n_tiles**：对于 RandomTiler 和 ScoreTiler
5. **使用pixel_overlap=0**：对于非重叠的GridTiler提取

## 故障排除

### 问题：未提取图块
* *解决方案：**
- 降低`tissue_percent`阈值
- 验证幻灯片包含组织（检查缩略图）
- 确保extraction_mask捕获组织Regions
- 检查tile_size 是否适合幻灯片分辨率

### 问题：提取了许多背景图块
* *解决方案：**
- 启用`check_tissue=True`
- 增加`tissue_percent` 阈值
- 使用适当的掩模（TissueMask 与TissueMask） BiggestTissueBoxMask)

### 问题：提取非常慢
* *解决方案：**
- 在较低金字塔级别提取（级别=1 或 2）
- 减少 RandomTiler/ScoreTiler 的 `n_tiles`
- 使用 RandomTiler 而不是 GridTiler采样
- 使用BiggestTissueBoxMask而不是TissueMask

### 问题：图块重叠太多(GridTiler)
* *解决方案：**
- 为非重叠图块设置`pixel_overlap=0`
- 减少`pixel_overlap`值
