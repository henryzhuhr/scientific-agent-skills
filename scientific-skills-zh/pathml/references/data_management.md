# 数据管理和存储

## 概述

PathML 通过 HDF5 存储、切片管理策略和优化的批处理工作流程提供高效的数据管理解决方案，用于处理大规模病理数据集。该框架能够以针对机器学习管道和下游分析优化的格式无缝存储和检索图像、掩模、特征和元数据。

## HDF5 集成

HDF5（分层数据格式）是处理后的 PathML 数据的主要存储格式，提供：
- 高效压缩和分块存储
- 对数据子集的快速随机访问data
- 支持任意大的数据集
- 异构数据类型的分层组织
- 跨平台兼容性

### 保存到HDF5

* *单张幻灯片：**
```python
from pathml.core import SlideData

# Load and process slide
wsi = SlideData.from_slide("slide.svs")
wsi.generate_tiles(level=1, tile_size=256, stride=256)

# Run preprocessing pipeline
pipeline.run(wsi)

# Save to HDF5
wsi.to_hdf5("processed_slide.h5")
```

* *多张幻灯片(SlideDataset):**
```python
from pathml.core import SlideDataset
import glob

# Create dataset
slide_paths = glob.glob("data/*.svs")
dataset = SlideDataset(slide_paths, tile_size=256, stride=256, level=1)

# Process
dataset.run(pipeline, distributed=True, n_workers=8)

# Save entire dataset
dataset.to_hdf5("processed_dataset.h5")
```

### HDF5 文件结构

PathML HDF5 文件按层次结构组织：

```
processed_dataset.h5
├── slide_0/
│   ├── metadata/
│   │   ├── name
│   │   ├── level
│   │   ├── dimensions
│   │   └── ...
│   ├── tiles/
│   │   ├── tile_0/
│   │   │   ├── image  (H, W, C) array
│   │   │   ├── coords  (x, y)
│   │   │   └── masks/
│   │   │       ├── tissue
│   │   │       ├── nucleus
│   │   │       └── ...
│   │   ├── tile_1/
│   │   └── ...
│   └── features/
│       ├── tile_features  (n_tiles, n_features)
│       └── feature_names
├── slide_1/
└── ...
```

### 从 HDF5

加载**加载整个幻灯片：**
```python
from pathml.core import SlideData

# Load from HDF5
wsi = SlideData.from_hdf5("processed_slide.h5")

# Access tiles
for tile in wsi.tiles:
    image = tile.image
    masks = tile.masks
    # Process tile...
```

* *加载特定图块：**
```python
# Load only tiles at specific indices
tile_indices = [0, 10, 20, 30]
tiles = wsi.load_tiles_from_hdf5("processed_slide.h5", indices=tile_indices)

for tile in tiles:
    # Process subset...
    pass
```

* *内存映射访问：**
```python
import h5py

# Open HDF5 file without loading into memory
with h5py.File("processed_dataset.h5", 'r') as f:
    # Access specific data
    tile_0_image = f['slide_0/tiles/tile_0/image'][:]
    tissue_mask = f['slide_0/tiles/tile_0/masks/tissue'][:]

    # Iterate through tiles efficiently
    for tile_key in f['slide_0/tiles'].keys():
        tile_image = f[f'slide_0/tiles/{tile_key}/image'][:]
        # Process without loading all tiles...
```

## 图块管理

#### 图块生成策略

* *无重叠的固定尺寸图块：**
```python
wsi.generate_tiles(
    level=1,
    tile_size=256,
    stride=256,  # stride = tile_size → no overlap
    pad=False  # Don't pad edge tiles
)
```
- **用例：**基于图块的标准处理、分类
- **优点：**简单、无冗余、快速处理
- **缺点：**图块边界处的边缘效应

* *重叠切片：**
```python
wsi.generate_tiles(
    level=1,
    tile_size=256,
    stride=128,  # 50% overlap
    pad=False
)
```
- **用例：** 分割、检测（减少边界伪影）
- **优点：** 更好的边界处理，更平滑的拼接
- **缺点：** 更多切片，冗余计算

* *基于组织的自适应切片内容：**
```python
from pathml.utils import adaptive_tile_generation

# Generate tiles only in tissue regions
wsi.generate_tiles(level=1, tile_size=256, stride=256)

# Filter to keep only tiles with sufficient tissue
tissue_tiles = []
for tile in wsi.tiles:
    if tile.masks.get('tissue') is not None:
        tissue_coverage = tile.masks['tissue'].sum() / (tile_size**2)
        if tissue_coverage > 0.5:  # Keep tiles with >50% tissue
            tissue_tiles.append(tile)

wsi.tiles = tissue_tiles
```
- **用例：** 稀疏组织样本，效率
- **优点：** 减少背景图块的处理
- **缺点：** 需要组织检测预处理步骤

### 图块拼接

从处理过的图块重建完整幻灯片：

```python
from pathml.utils import stitch_tiles

# Process tiles
for tile in wsi.tiles:
    tile.prediction = model.predict(tile.image)

# Stitch predictions back to full resolution
full_prediction_map = stitch_tiles(
    wsi.tiles,
    output_shape=wsi.level_dimensions[1],  # Use level 1 dimensions
    tile_size=256,
    stride=256,
    method='average'  # 'average', 'max', or 'first'
)

# Visualize
import matplotlib.pyplot as plt
plt.figure(figsize=(15, 15))
plt.imshow(full_prediction_map)
plt.title('Stitched Prediction Map')
plt.axis('off')
plt.show()
```

* *拼接方法：**
- `'average'`：平均重叠区域（平滑过渡）
- `'max'`：重叠区域中的最大值
- `'first'`：保留第一个图块的值（无混合）
- `'weighted'`：平滑边界的距离加权混合

### 图块缓存

缓存经常访问的图块以加快迭代速度：

```python
from pathml.utils import TileCache

# Create cache
cache = TileCache(max_size_gb=10)

# Cache tiles during first iteration
for i, tile in enumerate(wsi.tiles):
    cache.add(f'tile_{i}', tile.image)
    # Process tile...

# Subsequent iterations use cached data
for i in range(len(wsi.tiles)):
    cached_image = cache.get(f'tile_{i}')
    # Fast access...
```

## 数据集组织

### 大型目录结构项目

以一致的结构组织病理项目：

```
project/
├── raw_slides/
│   ├── cohort1/
│   │   ├── slide001.svs
│   │   ├── slide002.svs
│   │   └── ...
│   └── cohort2/
│       └── ...
├── processed/
│   ├── cohort1/
│   │   ├── slide001.h5
│   │   ├── slide002.h5
│   │   └── ...
│   └── cohort2/
│       └── ...
├── features/
│   ├── cohort1_features.h5
│   └── cohort2_features.h5
├── models/
│   ├── hovernet_checkpoint.pth
│   └── classifier.onnx
├── results/
│   ├── predictions/
│   ├── visualizations/
│   └── metrics.csv
└── metadata/
    ├── clinical_data.csv
    └── slide_manifest.csv
```

### 元数据管理

存储幻灯片级别和队列级别元数据：

```python
import pandas as pd

# Slide manifest
manifest = pd.DataFrame({
    'slide_id': ['slide001', 'slide002', 'slide003'],
    'path': ['raw_slides/cohort1/slide001.svs', ...],
    'cohort': ['cohort1', 'cohort1', 'cohort2'],
    'tissue_type': ['breast', 'breast', 'lung'],
    'scanner': ['Aperio', 'Hamamatsu', 'Aperio'],
    'magnification': [40, 40, 20],
    'staining': ['H&E', 'H&E', 'H&E']
})

manifest.to_csv('metadata/slide_manifest.csv', index=False)

# Clinical data
clinical = pd.DataFrame({
    'slide_id': ['slide001', 'slide002', 'slide003'],
    'patient_id': ['P001', 'P002', 'P003'],
    'age': [55, 62, 48],
    'diagnosis': ['invasive', 'in_situ', 'invasive'],
    'stage': ['II', 'I', 'III'],
    'outcome': ['favorable', 'favorable', 'poor']
})

clinical.to_csv('metadata/clinical_data.csv', index=False)

# Load and merge
manifest = pd.read_csv('metadata/slide_manifest.csv')
clinical = pd.read_csv('metadata/clinical_data.csv')
data = manifest.merge(clinical, on='slide_id')
```

## 批处理策略

### 顺序处理

一次处理一张幻灯片（节省内存）：

```python
import glob
from pathml.core import SlideData
from pathml.preprocessing import Pipeline

slide_paths = glob.glob('raw_slides/**/*.svs', recursive=True)

for slide_path in slide_paths:
    # Load slide
    wsi = SlideData.from_slide(slide_path)
    wsi.generate_tiles(level=1, tile_size=256, stride=256)

    # Process
    pipeline.run(wsi)

    # Save
    output_path = slide_path.replace('raw_slides', 'processed').replace('.svs', '.h5')
    wsi.to_hdf5(output_path)

    print(f"Processed: {slide_path}")
```

### 使用 Dask 进行并行处理

在中处理多张幻灯片并行：

```python
from pathml.core import SlideDataset
from dask.distributed import Client, LocalCluster
from pathml.preprocessing import Pipeline

# Start Dask cluster
cluster = LocalCluster(
    n_workers=8,
    threads_per_worker=2,
    memory_limit='8GB',
    dashboard_address=':8787'  # View progress at localhost:8787
)
client = Client(cluster)

# Create dataset
slide_paths = glob.glob('raw_slides/**/*.svs', recursive=True)
dataset = SlideDataset(slide_paths, tile_size=256, stride=256, level=1)

# Distribute processing
dataset.run(
    pipeline,
    distributed=True,
    client=client,
    scheduler='distributed'
)

# Save results
for i, slide in enumerate(dataset):
    output_path = slide_paths[i].replace('raw_slides', 'processed').replace('.svs', '.h5')
    slide.to_hdf5(output_path)

client.close()
cluster.close()
```

#### 使用作业数组进行批处理

对于HPC集群（SLURM，PBS）：

```python
# submit_jobs.py
import os
import glob

slide_paths = glob.glob('raw_slides/**/*.svs', recursive=True)

# Write slide list
with open('slide_list.txt', 'w') as f:
    for path in slide_paths:
        f.write(path + '\n')

# Create SLURM job script
slurm_script = """#!/bin/bash
#SBATCH --array=1-{n_slides}
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=4:00:00
#SBATCH --output=logs/slide_%A_%a.out

# Get slide path for this array task
SLIDE_PATH=$(sed -n "${{SLURM_ARRAY_TASK_ID}}p" slide_list.txt)

# Run processing
python process_slide.py --slide_path $SLIDE_PATH
""".format(n_slides=len(slide_paths))

with open('submit_jobs.sh', 'w') as f:
    f.write(slurm_script)

# Submit: sbatch submit_jobs.sh
```

```python
# process_slide.py
import argparse
from pathml.core import SlideData
from pathml.preprocessing import Pipeline

parser = argparse.ArgumentParser()
parser.add_argument('--slide_path', type=str, required=True)
args = parser.parse_args()

# Load and process
wsi = SlideData.from_slide(args.slide_path)
wsi.generate_tiles(level=1, tile_size=256, stride=256)

pipeline = Pipeline([...])
pipeline.run(wsi)

# Save
output_path = args.slide_path.replace('raw_slides', 'processed').replace('.svs', '.h5')
wsi.to_hdf5(output_path)

print(f"Processed: {args.slide_path}")
```

## 特征提取和存储

### 提取特征

```python
from pathml.core import SlideData
import torch
import numpy as np

# Load pre-trained model for feature extraction
model = torch.load('models/feature_extractor.pth')
model.eval()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Load processed slide
wsi = SlideData.from_hdf5('processed/slide001.h5')

# Extract features for each tile
features = []
coords = []

for tile in wsi.tiles:
    # Preprocess tile
    tile_tensor = torch.from_numpy(tile.image).permute(2, 0, 1).unsqueeze(0).float()
    tile_tensor = tile_tensor.to(device)

    # Extract features
    with torch.no_grad():
        feature_vec = model(tile_tensor).cpu().numpy().flatten()

    features.append(feature_vec)
    coords.append(tile.coords)

features = np.array(features)  # Shape: (n_tiles, feature_dim)
coords = np.array(coords)  # Shape: (n_tiles, 2)
```

### 将特征存储在HDF5

```python
import h5py

# Save features
with h5py.File('features/slide001_features.h5', 'w') as f:
    f.create_dataset('features', data=features, compression='gzip')
    f.create_dataset('coords', data=coords)
    f.attrs['feature_dim'] = features.shape[1]
    f.attrs['num_tiles'] = features.shape[0]
    f.attrs['model'] = 'resnet50'

# Load features
with h5py.File('features/slide001_features.h5', 'r') as f:
    features = f['features'][:]
    coords = f['coords'][:]
    feature_dim = f.attrs['feature_dim']
```

### 多幻灯片的特征数据库

```python
# Create consolidated feature database
import h5py
import glob

feature_files = glob.glob('features/*_features.h5')

with h5py.File('features/all_features.h5', 'w') as out_f:
    for i, feature_file in enumerate(feature_files):
        slide_name = feature_file.split('/')[-1].replace('_features.h5', '')

        with h5py.File(feature_file, 'r') as in_f:
            features = in_f['features'][:]
            coords = in_f['coords'][:]

            # Store in consolidated file
            grp = out_f.create_group(f'slide_{i}')
            grp.create_dataset('features', data=features, compression='gzip')
            grp.create_dataset('coords', data=coords)
            grp.attrs['slide_name'] = slide_name

# Query features from all slides
with h5py.File('features/all_features.h5', 'r') as f:
    for slide_key in f.keys():
        slide_name = f[slide_key].attrs['slide_name']
        features = f[f'{slide_key}/features'][:]
        # Process...
```

## 数据版本控制

### 使用 DVC 进行版本控制

使用数据版本控制 (DVC)进行大型数据集管理：

```bash
# Initialize DVC
dvc init

# Add data directory
dvc add raw_slides/
dvc add processed/

# Commit to git
git add raw_slides.dvc processed.dvc .gitignore
git commit -m "Add raw and processed slides"

# Push data to remote storage (S3, GCS, etc.)
dvc remote add -d storage s3://my-bucket/pathml-data
dvc push

# Pull data on another machine
git pull
dvc pull
```

### 校验和和验证

验证数据完整性：

```python
import hashlib
import pandas as pd

def compute_checksum(file_path):
    """Compute MD5 checksum of file."""
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Create checksum manifest
slide_paths = glob.glob('raw_slides/**/*.svs', recursive=True)
checksums = []

for slide_path in slide_paths:
    checksum = compute_checksum(slide_path)
    checksums.append({
        'path': slide_path,
        'checksum': checksum,
        'size_mb': os.path.getsize(slide_path) / 1e6
    })

checksum_df = pd.DataFrame(checksums)
checksum_df.to_csv('metadata/checksums.csv', index=False)

# Validate files
def validate_files(manifest_path):
    manifest = pd.read_csv(manifest_path)
    for _, row in manifest.iterrows():
        current_checksum = compute_checksum(row['path'])
        if current_checksum != row['checksum']:
            print(f"ERROR: Checksum mismatch for {row['path']}")
        else:
            print(f"OK: {row['path']}")

validate_files('metadata/checksums.csv')
```

## 性能优化

### 压缩设置

针对速度与大小优化 HDF5 压缩：

```python
import h5py

# Fast compression (less CPU, larger files)
with h5py.File('output.h5', 'w') as f:
    f.create_dataset(
        'images',
        data=images,
        compression='gzip',
        compression_opts=1  # Level 1-9, lower = faster
    )

# Maximum compression (more CPU, smaller files)
with h5py.File('output.h5', 'w') as f:
    f.create_dataset(
        'images',
        data=images,
        compression='gzip',
        compression_opts=9
    )

# Balanced (recommended)
with h5py.File('output.h5', 'w') as f:
    f.create_dataset(
        'images',
        data=images,
        compression='gzip',
        compression_opts=4,
        chunks=True  # Enable chunking for better I/O
    )
```

### 分块策略

优化分块存储以进行访问模式：

```python
# For tile-based access (access one tile at a time)
with h5py.File('tiles.h5', 'w') as f:
    f.create_dataset(
        'tiles',
        shape=(n_tiles, 256, 256, 3),
        dtype='uint8',
        chunks=(1, 256, 256, 3),  # One tile per chunk
        compression='gzip'
    )

# For channel-based access (access all tiles for one channel)
with h5py.File('tiles.h5', 'w') as f:
    f.create_dataset(
        'tiles',
        shape=(n_tiles, 256, 256, 3),
        dtype='uint8',
        chunks=(n_tiles, 256, 256, 1),  # All tiles for one channel
        compression='gzip'
    )
```

### 内存映射数组

对大型数组使用内存映射：

```python
import numpy as np

# Save as memory-mapped file
features_mmap = np.memmap(
    'features/features.mmap',
    dtype='float32',
    mode='w+',
    shape=(n_tiles, feature_dim)
)

# Populate
for i, tile in enumerate(wsi.tiles):
    features_mmap[i] = extract_features(tile)

# Flush to disk
features_mmap.flush()

# Load without reading into memory
features_mmap = np.memmap(
    'features/features.mmap',
    dtype='float32',
    mode='r',
    shape=(n_tiles, feature_dim)
)

# Access subset efficiently
subset = features_mmap[1000:2000]  # Only loads requested rows
```

## 最佳实践

1. **使用 HDF5 处理数据：** 将预处理的图块和要素保存到 HDF5，以便快速访问

2. **分离原始数据和处理后的数据：**将原始幻灯片与处理后的输出分开

3. **维护元数据：** 跟踪载玻片出处、处理参数和临床注释

4. **实施校验和：**验证数据完整性，尤其是在传输

5之后。 **版本数据集：** 使用 DVC 或类似工具对大型数据集进行版本控制

6. **优化存储：** 平衡压缩级别与 I/O 性能

7. **按队列组织：** 为了清楚起见，按研究队列构建目录

8. **定期备份：** 将数据和元数据备份到远程存储

9. **文档处理：** 保留处理步骤、参数和版本的日志

10. **监控磁盘使用情况：**随着数据集增长跟踪存储消耗

## 常见问题和解决方案

* *问题：HDF5文件非常大**
- 增加压缩级别：`compression_opts=9`
- 仅存储必要的数据（避免冗余副本）
- 使用适当的数据类型（图像使用uint8，图像使用uint8） float64)

* *问题：HDF5 读/写速度慢**
- 优化访问模式的块大小
- 降低压缩级别以获得更快的 I/OZXXQNL16QXZ- 使用 SSD 存储而不是 HDD
- 使用 MPI

 启用并行 HDF5 **问题：磁盘不足空间**
- 处理后删除中间文件
- 压缩非活动数据集
- 将旧数据移至存档存储
- 使用云存储存储访问较少的数据

* *问题：数据损坏或丢失**
- 实施定期备份
- 使用RAID冗余
- 传输后验证校验和
- 使用版本控制(DVC)

## 其他资源

- **HDF5 文档：** https://www.hdfgroup.org/solutions/hdf5/
- **h5py:** https://docs.h5py.org/
- **DVC（数据版本控制）：** https://dvc.org/
- **Dask：** https://docs.dask.org/
- **PathML 数据管理 API：** https://pathml.readthedocs.io/en/latest/api_data_reference.html
