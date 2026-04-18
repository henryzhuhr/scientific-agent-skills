---
name: zarr-python
description: 用于云存储的分块 N 维阵列。压缩数组、并行 I/O、S3/GCS 集成、NumPy/Dask/Xarray 兼容，适用于大规模科学计算管道。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Zarr Python

## 概述

Zarr 是一个 Python 库，用于通过分块和压缩来存储大型 N 维数组。应用此技能可实现高效的并行 I/O、云原生工作流程以及与 NumPy、Dask 和 Xarray 的无缝集成。

## 快速入门

### 安装

```bash
uv pip install zarr
```

 需要 Python 3.11+。如需云存储支持，请安装附加软件包：
```python
uv pip install s3fs  # For S3
uv pip install gcsfs  # For Google Cloud Storage
```

### 基本阵列创建

```python
import zarr
import numpy as np

# Create a 2D array with chunking and compression
z = zarr.create_array(
    store="data/my_array.zarr",
    shape=(10000, 10000),
    chunks=(1000, 1000),
    dtype="f4"
)

# Write data using NumPy-style indexing
z[:, :] = np.random.random((10000, 10000))

# Read data
data = z[0:100, 0:100]  # Returns NumPy array
```

## 核心操作

### 创建阵列

Zarr为阵列提供了多种便捷功能创建：

```python
# Create empty array
z = zarr.zeros(shape=(10000, 10000), chunks=(1000, 1000), dtype='f4',
               store='data.zarr')

# Create filled arrays
z = zarr.ones((5000, 5000), chunks=(500, 500))
z = zarr.full((1000, 1000), fill_value=42, chunks=(100, 100))

# Create from existing data
data = np.arange(10000).reshape(100, 100)
z = zarr.array(data, chunks=(10, 10), store='data.zarr')

# Create like another array
z2 = zarr.zeros_like(z)  # Matches shape, chunks, dtype of z
```

### 打开现有数组

```python
# Open array (read/write mode by default)
z = zarr.open_array('data.zarr', mode='r+')

# Read-only mode
z = zarr.open_array('data.zarr', mode='r')

# The open() function auto-detects arrays vs groups
z = zarr.open('data.zarr')  # Returns Array or Group
```

### 读写数据

Zarr数组支持NumPy-like索引：

```python
# Write entire array
z[:] = 42

# Write slices
z[0, :] = np.arange(100)
z[10:20, 50:60] = np.random.random((10, 10))

# Read data (returns NumPy array)
data = z[0:100, 0:100]
row = z[5, :]

# Advanced indexing
z.vindex[[0, 5, 10], [2, 8, 15]]  # Coordinate indexing
z.oindex[0:10, [5, 10, 15]]       # Orthogonal indexing
z.blocks[0, 0]                     # Block/chunk indexing
```

### 调整大小和追加

```python
# Resize array
z.resize(15000, 15000)  # Expands or shrinks dimensions

# Append data along an axis
z.append(np.random.random((1000, 10000)), axis=0)  # Adds rows
```

## 分块策略

分块对于性能至关重要。根据访问模式选择块大小和形状。

### 块大小指南

- **最小块大小**：建议使用 1 MB 以获得最佳性能
- **平衡**：更大的块 = 更少的元数据操作；较小的块 = 更好的并行访问
- **内存考虑**：压缩期间整个块必须适合内存

```python
# Configure chunk size (aim for ~1MB per chunk)
# For float32 data: 1MB = 262,144 elements = 512×512 array
z = zarr.zeros(
    shape=(10000, 10000),
    chunks=(512, 512),  # ~1MB chunks
    dtype='f4'
)
```

### 将块与访问模式对齐

* *关键**：块形状根据数据的存储方式极大地影响性能

```python
# If accessing rows frequently (first dimension)
z = zarr.zeros((10000, 10000), chunks=(10, 10000))  # Chunk spans columns

# If accessing columns frequently (second dimension)
z = zarr.zeros((10000, 10000), chunks=(10000, 10))  # Chunk spans rows

# For mixed access patterns (balanced approach)
z = zarr.zeros((10000, 10000), chunks=(1000, 1000))  # Square chunks
```

* *性能示例**：对于（200, 200, 200）数组，沿第一维读取：
- 使用块（1, 200, 200）：~107ms
- 使用块（200, 200, 1): ~1.65ms (快65倍！)

### 大规模存储分片

当数组有数百万个小块时，使用分片将块分组为更大的存储对象：

```python
from zarr.codecs import ShardingCodec, BytesCodec
from zarr.codecs.blosc import BloscCodec

# Create array with sharding
z = zarr.create_array(
    store='data.zarr',
    shape=(100000, 100000),
    chunks=(100, 100),  # Small chunks for access
    shards=(1000, 1000),  # Groups 100 chunks per shard
    dtype='f4'
)
```

* *好处**：
- 减少文件系统开销来自数百万个小文件
- 提高云存储性能（更少的对象请求）
- 防止文件系统块大小浪费

* *重要**：写入之前，整个分片必须适合内存。

## 压缩

Zarr 对每个块应用压缩，以减少存储，同时保持快速访问。

### 配置压缩

```python
from zarr.codecs.blosc import BloscCodec
from zarr.codecs import GzipCodec, ZstdCodec

# Default: Blosc with Zstandard
z = zarr.zeros((1000, 1000), chunks=(100, 100))  # Uses default compression

# Configure Blosc codec
z = zarr.create_array(
    store='data.zarr',
    shape=(1000, 1000),
    chunks=(100, 100),
    dtype='f4',
    codecs=[BloscCodec(cname='zstd', clevel=5, shuffle='shuffle')]
)

# Available Blosc compressors: 'blosclz', 'lz4', 'lz4hc', 'snappy', 'zlib', 'zstd'

# Use Gzip compression
z = zarr.create_array(
    store='data.zarr',
    shape=(1000, 1000),
    chunks=(100, 100),
    dtype='f4',
    codecs=[GzipCodec(level=6)]
)

# Disable compression
z = zarr.create_array(
    store='data.zarr',
    shape=(1000, 1000),
    chunks=(100, 100),
    dtype='f4',
    codecs=[BytesCodec()]  # No compression
)
```

### 压缩性能提示

- **Blosc** （默认）：快速压缩/解压缩，适合交互式工作负载
- **Zstandard**：更好的压缩比，比 LZ4
 稍慢- **Gzip**：最大压缩，性能较慢
- **LZ4**：最快压缩，较低比率
- **随机播放**：启用随机播放过滤器以更好地压缩数字data

```python
# Optimal for numeric scientific data
codecs=[BloscCodec(cname='zstd', clevel=5, shuffle='shuffle')]

# Optimal for speed
codecs=[BloscCodec(cname='lz4', clevel=1)]

# Optimal for compression ratio
codecs=[GzipCodec(level=9)]
```

## 存储后端

Zarr 通过灵活的存储接口支持多个存储后端。

### 本地文件系统（默认）

```python
from zarr.storage import LocalStore

# Explicit store creation
store = LocalStore('data/my_array.zarr')
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))

# Or use string path (creates LocalStore automatically)
z = zarr.open_array('data/my_array.zarr', mode='w', shape=(1000, 1000),
                    chunks=(100, 100))
```

### 内存中存储

```python
from zarr.storage import MemoryStore

# Create in-memory store
store = MemoryStore()
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))

# Data exists only in memory, not persisted
```

### ZIP文件存储

```python
from zarr.storage import ZipStore

# Write to ZIP file
store = ZipStore('data.zip', mode='w')
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
z[:] = np.random.random((1000, 1000))
store.close()  # IMPORTANT: Must close ZipStore

# Read from ZIP file
store = ZipStore('data.zip', mode='r')
z = zarr.open_array(store=store)
data = z[:]
store.close()
```

### 云存储（S3，GCS）

```python
import s3fs
import zarr

# S3 storage
s3 = s3fs.S3FileSystem(anon=False)  # Use credentials
store = s3fs.S3Map(root='my-bucket/path/to/array.zarr', s3=s3)
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
z[:] = data

# Google Cloud Storage
import gcsfs
gcs = gcsfs.GCSFileSystem(project='my-project')
store = gcsfs.GCSMap(root='my-bucket/path/to/array.zarr', gcs=gcs)
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
```

* *云存储最佳实践**：
  - 使用整合的元数据来减少延迟：`zarr.consolidate_metadata(store)`
  - 将块大小与云对象大小对齐（通常最佳为 5-100 MB）
  - 使用 Dask 为大规模数据启用并行写入
  - 考虑分片以减少分片数量对象

## 组和层次结构

组按层次结构组织多个数组，类似于目录或HDF5组。

### 创建和使用组

```python
# Create root group
root = zarr.group(store='data/hierarchy.zarr')

# Create sub-groups
temperature = root.create_group('temperature')
precipitation = root.create_group('precipitation')

# Create arrays within groups
temp_array = temperature.create_array(
    name='t2m',
    shape=(365, 720, 1440),
    chunks=(1, 720, 1440),
    dtype='f4'
)

precip_array = precipitation.create_array(
    name='prcp',
    shape=(365, 720, 1440),
    chunks=(1, 720, 1440),
    dtype='f4'
)

# Access using paths
array = root['temperature/t2m']

# Visualize hierarchy
print(root.tree())
# Output:
# /
#  ├── temperature
#  │   └── t2m (365, 720, 1440) f4
#  └── precipitation
#      └── prcp (365, 720, 1440) f4
```

### H5py兼容的API

Zarr提供了h5py兼容熟悉 HDF5 用户的界面：

```python
# Create group with h5py-style methods
root = zarr.group('data.zarr')
dataset = root.create_dataset('my_data', shape=(1000, 1000), chunks=(100, 100),
                              dtype='f4')

# Access like h5py
grp = root.require_group('subgroup')
arr = grp.require_dataset('array', shape=(500, 500), chunks=(50, 50), dtype='i4')
```

## 属性和元数据

使用属性将自定义元数据附加到数组和组：

```python
# Add attributes to array
z = zarr.zeros((1000, 1000), chunks=(100, 100))
z.attrs['description'] = 'Temperature data in Kelvin'
z.attrs['units'] = 'K'
z.attrs['created'] = '2024-01-15'
z.attrs['processing_version'] = 2.1

# Attributes are stored as JSON
print(z.attrs['units'])  # Output: K

# Add attributes to groups
root = zarr.group('data.zarr')
root.attrs['project'] = 'Climate Analysis'
root.attrs['institution'] = 'Research Institute'

# Attributes persist with the array/group
z2 = zarr.open('data.zarr')
print(z2.attrs['description'])
```

* *重要**：属性必须是 JSON 可序列化的（字符串、数字、列表、字典、布尔值、空）。

## 与 NumPy、Dask 和 Xarray 集成

### NumPy 集成

Zarr 数组实现 NumPy 数组接口：

```python
import numpy as np
import zarr

z = zarr.zeros((1000, 1000), chunks=(100, 100))

# Use NumPy functions directly
result = np.sum(z, axis=0)  # NumPy operates on Zarr array
mean = np.mean(z[:100, :100])

# Convert to NumPy array
numpy_array = z[:]  # Loads entire array into memory
```

### Dask 集成

Dask 在 Zarr 数组上提供惰性并行计算：

```python
import dask.array as da
import zarr

# Create large Zarr array
z = zarr.open('data.zarr', mode='w', shape=(100000, 100000),
              chunks=(1000, 1000), dtype='f4')

# Load as Dask array (lazy, no data loaded)
dask_array = da.from_zarr('data.zarr')

# Perform computations (parallel, out-of-core)
result = dask_array.mean(axis=0).compute()  # Parallel computation

# Write Dask array to Zarr
large_array = da.random.random((100000, 100000), chunks=(1000, 1000))
da.to_zarr(large_array, 'output.zarr')
```

* *优点**：
- 处理大于内存的数据集
- 跨块自动并行计算
- 具有分块存储的高效 I/O

### Xarray集成

Xarray 提供带有 Zarr 后端的标记多维数组：

```python
import xarray as xr
import zarr

# Open Zarr store as Xarray Dataset (lazy loading)
ds = xr.open_zarr('data.zarr')

# Dataset includes coordinates and metadata
print(ds)

# Access variables
temperature = ds['temperature']

# Perform labeled operations
subset = ds.sel(time='2024-01', lat=slice(30, 60))

# Write Xarray Dataset to Zarr
ds.to_zarr('output.zarr')

# Create from scratch with coordinates
ds = xr.Dataset(
    {
        'temperature': (['time', 'lat', 'lon'], data),
        'precipitation': (['time', 'lat', 'lon'], data2)
    },
    coords={
        'time': pd.date_range('2024-01-01', periods=365),
        'lat': np.arange(-90, 91, 1),
        'lon': np.arange(-180, 180, 1)
    }
)
ds.to_zarr('climate_data.zarr')
```

* *优点**：
- 命名维度和坐标
- 基于标签的索引和选择
- 与 pandas 集成时间序列
- 气候/地理空间科学家熟悉的类似 NetCDF 的界面

## 并行计算和同步

### 线程安全操作

```python
from zarr import ThreadSynchronizer
import zarr

# For multi-threaded writes
synchronizer = ThreadSynchronizer()
z = zarr.open_array('data.zarr', mode='r+', shape=(10000, 10000),
                    chunks=(1000, 1000), synchronizer=synchronizer)

# Safe for concurrent writes from multiple threads
# (when writes don't span chunk boundaries)
```

### 过程安全操作

```python
from zarr import ProcessSynchronizer
import zarr

# For multi-process writes
synchronizer = ProcessSynchronizer('sync_data.sync')
z = zarr.open_array('data.zarr', mode='r+', shape=(10000, 10000),
                    chunks=(1000, 1000), synchronizer=synchronizer)

# Safe for concurrent writes from multiple processes
```

* *注意**：
- 并发读取不需要同步
- 仅可能跨越块边界的写入需要同步
- 写入单独块的每个进程/线程不需要同步

## 合并元数据

对于具有多个阵列的分层存储，将元数据合并到单个文件中以减少 I/O 操作：

```python
import zarr

# After creating arrays/groups
root = zarr.group('data.zarr')
# ... create multiple arrays/groups ...

# Consolidate metadata
zarr.consolidate_metadata('data.zarr')

# Open with consolidated metadata (faster, especially on cloud storage)
root = zarr.open_consolidated('data.zarr')
```

* *优点**：
- 将元数据读取操作从 N（每个阵列一个）减少到 1
- 对于云存储至关重要（减少延迟）
- 加快 `tree()` 操作和组遍历

* *注意事项**：
- 如果数组更新而不重新整合，元数据可能会过时
- 不适合频繁更新的数据集
- 多写入器场景可能不一致内容为

## 性能优化

#### 最佳性能检查表

1. **块大小**：每个块的目标为 1-10 MB
 ```python
 # 对于 float32：1MB = 262,144 个元素
chunks = (512, 512) # 512×512×4 字节 = ~1MB
 ```

2. **块形状**：与访问模式对齐
 ```python
 # 行式访问 → 块跨越列：(小，大)
 # 列式访问 → 块跨越行：(大，小)
 # 随机访问 → 平衡：(中，中)
```

3. **压缩**：根据工作负载选择
 ```python
 # 交互式/快速：BloscCodec(cname='lz4')
 # 平衡：BloscCodec(cname='zstd', clevel=5)
 # 最大压缩：GzipCodec(level=9)
``

4. **存储后端**：与环境匹配
 ```python
 # 本地：LocalStore（默认）
 # 云：具有统一元数据的 S3Map/GCSMap
 # 临时：MemoryStore
```

5. **分片**：用于大规模数据集
 ```python
 # 当你有数百万个小块时
shards=(10*chunk_size, 10*chunk_size)
 ```

6. **并行 I/O**：使用 Dask 进行大型操作
 ```python
 import dask.array as da
 dask_array = da.from_zarr('data.zarr')
 result = dask_array.compute(scheduler='threads', num_workers=8)
 ```

### 分析和调试

```python
# Print detailed array information
print(z.info)

# Output includes:
# - Type, shape, chunks, dtype
# - Compression codec and level
# - Storage size (compressed vs uncompressed)
# - Storage location

# Check storage size
print(f"Compressed size: {z.nbytes_stored / 1e6:.2f} MB")
print(f"Uncompressed size: {z.nbytes / 1e6:.2f} MB")
print(f"Compression ratio: {z.nbytes / z.nbytes_stored:.2f}x")
```

## 常见模式和最佳实践

### 模式：时间序列数据

```python
# Store time series with time as first dimension
# This allows efficient appending of new time steps
z = zarr.open('timeseries.zarr', mode='a',
              shape=(0, 720, 1440),  # Start with 0 time steps
              chunks=(1, 720, 1440),  # One time step per chunk
              dtype='f4')

# Append new time steps
new_data = np.random.random((1, 720, 1440))
z.append(new_data, axis=0)
```

### 模式：大型矩阵操作

```python
import dask.array as da

# Create large matrix in Zarr
z = zarr.open('matrix.zarr', mode='w',
              shape=(100000, 100000),
              chunks=(1000, 1000),
              dtype='f8')

# Use Dask for parallel computation
dask_z = da.from_zarr('matrix.zarr')
result = (dask_z @ dask_z.T).compute()  # Parallel matrix multiply
```

### 模式：云原生工作流

```python
import s3fs
import zarr

# Write to S3
s3 = s3fs.S3FileSystem()
store = s3fs.S3Map(root='s3://my-bucket/data.zarr', s3=s3)

# Create array with appropriate chunking for cloud
z = zarr.open_array(store=store, mode='w',
                    shape=(10000, 10000),
                    chunks=(500, 500),  # ~1MB chunks
                    dtype='f4')
z[:] = data

# Consolidate metadata for faster reads
zarr.consolidate_metadata(store)

# Read from S3 (anywhere, anytime)
store_read = s3fs.S3Map(root='s3://my-bucket/data.zarr', s3=s3)
z_read = zarr.open_consolidated(store_read)
subset = z_read[0:100, 0:100]
```

### 模式：格式转换

```python
# HDF5 to Zarr
import h5py
import zarr

with h5py.File('data.h5', 'r') as h5:
    dataset = h5['dataset_name']
    z = zarr.array(dataset[:],
                   chunks=(1000, 1000),
                   store='data.zarr')

# NumPy to Zarr
import numpy as np
data = np.load('data.npy')
z = zarr.array(data, chunks='auto', store='data.zarr')

# Zarr to NetCDF (via Xarray)
import xarray as xr
ds = xr.open_zarr('data.zarr')
ds.to_netcdf('data.nc')
```

## 常见问题和解决方案

### 问题：性能缓慢

* *诊断**：检查块大小和对齐
```python
print(z.chunks)  # Are chunks appropriate size?
print(z.info)    # Check compression ratio
```

* *解决方案**：
- 将块大小增加到 1-10 MB
- 将块与访问模式对齐
- 尝试不同的压缩编解码器
- 使用Dask进行并行操作

### 问题：内存使用率高

* *原因**：将整个数组或大块加载到内存中

* *解决方案**：
```python
# Don't load entire array
# Bad: data = z[:]
# Good: Process in chunks
for i in range(0, z.shape[0], 1000):
    chunk = z[i:i+1000, :]
    process(chunk)

# Or use Dask for automatic chunking
import dask.array as da
dask_z = da.from_zarr('data.zarr')
result = dask_z.mean().compute()  # Processes in chunks
```

### 问题：云存储延迟

* *解决方案**：
```python
# 1. Consolidate metadata
zarr.consolidate_metadata(store)
z = zarr.open_consolidated(store)

# 2. Use appropriate chunk sizes (5-100 MB for cloud)
chunks = (2000, 2000)  # Larger chunks for cloud

# 3. Enable sharding
shards = (10000, 10000)  # Groups many chunks
```

### 问题：并发写入冲突

* *解决方案**：使用同步器或确保非重叠写入
```python
from zarr import ProcessSynchronizer

sync = ProcessSynchronizer('sync.sync')
z = zarr.open_array('data.zarr', mode='r+', synchronizer=sync)

# Or design workflow so each process writes to separate chunks
```

## 其他资源

有关详细的API文档、高级用法和最新更新：

- **官方文档**：https://zarr.readthedocs.io/
- **Zarr规范**： https://zarr-specs.readthedocs.io/
- **GitHub 存储库**：https://github.com/zarr-developers/zarr-python
- **社区聊天**：https://gitter.im/zarr-developers/community

* *相关库**：
- **Xarray**：https://docs.xarray.dev/ （标记数组）
- **Dask**：https://docs.dask.org/ （并行计算）
- **NumCodecs**：https://numcodecs.readthedocs.io/ （压缩编解码器）
