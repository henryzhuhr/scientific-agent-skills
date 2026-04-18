# Zarr Python Quick Reference

此参考提供了常用 Zarr 函数、参数和模式的简明概述，以便在开发过程中快速查找。

## 数组创建函数

### `zarr.zeros()` / `zarr.ones()` / `zarr.empty()`
```python
zarr.zeros(shape, chunks=None, dtype='f8', store=None, compressor='default',
           fill_value=0, order='C', filters=None)
```
创建用零填充的数组， 

* *关键参数：**
- `shape`：定义数组维度的元组（例如，`(1000, 1000)`）
- `chunks`：定义块维度的元组（例如，`(100, 100)`），或 `None` 表示无chunking
- `dtype`：NumPy 数据类型（例如，`'f4'`、`'i8'`、`'bool'`）
- `store`：存储位置（字符串路径、存储对象或用于内存的 `None`）
- `compressor`：压缩编解码器或`None`无压缩

### `zarr.create_array()` / `zarr.create()`
```python
zarr.create_array(store, shape, chunks, dtype='f8', compressor='default',
                  fill_value=0, order='C', filters=None, overwrite=False)
```
创建一个对所有参数进行显式控制的新数组。

### `zarr.array()`
```python
zarr.array(data, chunks=None, dtype=None, compressor='default', store=None)
```
从现有数据（NumPy数组、列表等）创建数组。

* *示例：**
```python
import numpy as np
data = np.random.random((1000, 1000))
z = zarr.array(data, chunks=(100, 100), store='data.zarr')
```

### `zarr.open_array()` / `zarr.open()`
```python
zarr.open_array(store, mode='a', shape=None, chunks=None, dtype=None,
                compressor='default', fill_value=0)
```
打开现有阵列或创建新阵列。

* *模式选项：**
- `'r'`：只读
- `'r+'`：读写，文件必须存在
- `'a'`：读写，不存在则创建（默认）
- `'w'`：新建，存在则覆盖
- `'w-'`：新建，存在则失败

## 存储类

### LocalStore （默认）
```python
from zarr.storage import LocalStore

store = LocalStore('path/to/data.zarr')
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
```

### MemoryStore
```python
from zarr.storage import MemoryStore

store = MemoryStore()  # Data only in memory
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
```

### ZipStore
```python
from zarr.storage import ZipStore

# Write
store = ZipStore('data.zip', mode='w')
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
z[:] = data
store.close()  # MUST close

# Read
store = ZipStore('data.zip', mode='r')
z = zarr.open_array(store=store)
data = z[:]
store.close()
```

### 云存储(S3/GCS)
```python
# S3
import s3fs
s3 = s3fs.S3FileSystem(anon=False)
store = s3fs.S3Map(root='bucket/path/data.zarr', s3=s3)

# GCS
import gcsfs
gcs = gcsfs.GCSFileSystem(project='my-project')
store = gcsfs.GCSMap(root='bucket/path/data.zarr', gcs=gcs)
```

## 压缩编解码器

### Blosc 编解码器（默认）
```python
from zarr.codecs.blosc import BloscCodec

codec = BloscCodec(
    cname='zstd',      # Compressor: 'blosclz', 'lz4', 'lz4hc', 'snappy', 'zlib', 'zstd'
    clevel=5,          # Compression level: 0-9
    shuffle='shuffle'  # Shuffle filter: 'noshuffle', 'shuffle', 'bitshuffle'
)

z = zarr.create_array(store='data.zarr', shape=(1000, 1000), chunks=(100, 100),
                      dtype='f4', codecs=[codec])
```

* *Blosc 压缩器特性：**
- `'lz4'`：最快压缩，较低比率
- `'zstd'`：平衡（默认），良好的比率和速度
- `'zlib'`：兼容性好，性能适中
- `'lz4hc'`：比lz4好，速度慢
- `'snappy'`：速度快，比例适中
- `'blosclz'`：Blosc默认的

### 其他编解码器
```python
from zarr.codecs import GzipCodec, ZstdCodec, BytesCodec

# Gzip compression (maximum ratio, slower)
GzipCodec(level=6)  # Level 0-9

# Zstandard compression
ZstdCodec(level=3)  # Level 1-22

# No compression
BytesCodec()
```

## 数组索引和选择

### 基本索引（NumPy 样式）
```python
z = zarr.zeros((1000, 1000), chunks=(100, 100))

# Read
row = z[0, :]           # Single row
col = z[:, 0]           # Single column
block = z[10:20, 50:60] # Slice
element = z[5, 10]      # Single element

# Write
z[0, :] = 42
z[10:20, 50:60] = np.random.random((10, 10))
```

### 高级索引
```python
# Coordinate indexing (point selection)
z.vindex[[0, 5, 10], [2, 8, 15]]  # Specific coordinates

# Orthogonal indexing (outer product)
z.oindex[0:10, [5, 10, 15]]  # Rows 0-9, columns 5, 10, 15

# Block/chunk indexing
z.blocks[0, 0]  # First chunk
z.blocks[0:2, 0:2]  # First four chunks
```

## 组和层次结构

### 创建组
```python
# Create root group
root = zarr.group(store='data.zarr')

# Create nested groups
grp1 = root.create_group('group1')
grp2 = grp1.create_group('subgroup')

# Create arrays in groups
arr = grp1.create_array(name='data', shape=(1000, 1000),
                        chunks=(100, 100), dtype='f4')

# Access by path
arr2 = root['group1/data']
```

### 组方法
```python
root = zarr.group('data.zarr')

# h5py-compatible methods
dataset = root.create_dataset('data', shape=(1000, 1000), chunks=(100, 100))
subgrp = root.require_group('subgroup')  # Create if doesn't exist

# Visualize structure
print(root.tree())

# List contents
print(list(root.keys()))
print(list(root.groups()))
print(list(root.arrays()))
```

## 数组属性和元数据

### 使用属性
```python
z = zarr.zeros((1000, 1000), chunks=(100, 100))

# Set attributes
z.attrs['units'] = 'meters'
z.attrs['description'] = 'Temperature data'
z.attrs['created'] = '2024-01-15'
z.attrs['version'] = 1.2
z.attrs['tags'] = ['climate', 'temperature']

# Read attributes
print(z.attrs['units'])
print(dict(z.attrs))  # All attributes as dict

# Update/delete
z.attrs['version'] = 2.0
del z.attrs['tags']
```

* *注意：** 属性必须是 JSON 可序列化的。

## 数组属性和方法

### 属性
```python
z = zarr.zeros((1000, 1000), chunks=(100, 100), dtype='f4')

z.shape          # (1000, 1000)
z.chunks         # (100, 100)
z.dtype          # dtype('float32')
z.size           # 1000000
z.nbytes         # 4000000 (uncompressed size in bytes)
z.nbytes_stored  # Actual compressed size on disk
z.nchunks        # 100 (number of chunks)
z.cdata_shape    # Shape in terms of chunks: (10, 10)
```

### 方法
```python
# Information
print(z.info)  # Detailed information about array
print(z.info_items())  # Info as list of tuples

# Resizing
z.resize(1500, 1500)  # Change dimensions

# Appending
z.append(new_data, axis=0)  # Add data along axis

# Copying
z2 = z.copy(store='new_location.zarr')
```

## 分块指南

### 块大小计算
```python
# For float32 (4 bytes per element):
# 1 MB = 262,144 elements
# 10 MB = 2,621,440 elements

# Examples for 1 MB chunks:
(512, 512)      # For 2D: 512 × 512 × 4 = 1,048,576 bytes
(128, 128, 128) # For 3D: 128 × 128 × 128 × 4 = 8,388,608 bytes ≈ 8 MB
(64, 256, 256)  # For 3D: 64 × 256 × 256 × 4 = 16,777,216 bytes ≈ 16 MB
```

### 分块策略访问模式

* *时间序列（沿第一维顺序访问）：**
```python
chunks=(1, 720, 1440)  # One time step per chunk
```

* *行式访问：**
```python
chunks=(10, 10000)  # Small rows, span columns
```

* *列式访问访问：**
```python
chunks=(10000, 10)  # Span rows, small columns
```

* *随机访问：**
```python
chunks=(500, 500)  # Balanced square chunks
```

* *3D体积数据：**
```python
chunks=(64, 64, 64)  # Cubic chunks for isotropic access
```

## 集成API

### NumPy 集成
```python
import numpy as np

z = zarr.zeros((1000, 1000), chunks=(100, 100))

# Use NumPy functions
result = np.sum(z, axis=0)
mean = np.mean(z)
std = np.std(z)

# Convert to NumPy
arr = z[:]  # Loads entire array into memory
```

### Dask 集成
```python
import dask.array as da

# Load Zarr as Dask array
dask_array = da.from_zarr('data.zarr')

# Compute operations in parallel
result = dask_array.mean(axis=0).compute()

# Write Dask array to Zarr
large_array = da.random.random((100000, 100000), chunks=(1000, 1000))
da.to_zarr(large_array, 'output.zarr')
```

### Xarray 集成
```python
import xarray as xr

# Open Zarr as Xarray Dataset
ds = xr.open_zarr('data.zarr')

# Write Xarray to Zarr
ds.to_zarr('output.zarr')

# Create with coordinates
ds = xr.Dataset(
    {'temperature': (['time', 'lat', 'lon'], data)},
    coords={
        'time': pd.date_range('2024-01-01', periods=365),
        'lat': np.arange(-90, 91, 1),
        'lon': np.arange(-180, 180, 1)
    }
)
ds.to_zarr('climate.zarr')
```

## 并行计算

### 同步器
```python
from zarr import ThreadSynchronizer, ProcessSynchronizer

# Multi-threaded writes
sync = ThreadSynchronizer()
z = zarr.open_array('data.zarr', mode='r+', synchronizer=sync)

# Multi-process writes
sync = ProcessSynchronizer('sync.sync')
z = zarr.open_array('data.zarr', mode='r+', synchronizer=sync)
```

* *注意：**仅需要同步：
- 可能跨越块边界的并发写入
- 读取不需要（始终安全）
- 如果每个进程写入单独的数据则不需要chunks

## 元数据整合

```python
# Consolidate metadata (after creating all arrays/groups)
zarr.consolidate_metadata('data.zarr')

# Open with consolidated metadata (faster, especially on cloud)
root = zarr.open_consolidated('data.zarr')
```

* *优点：**
- 将 I/O 从 N 次操作减少到 1
- 对于云存储至关重要（减少延迟）
- 加快层次结构遍历

* *注意事项：**
- 如果数据更新，可能会变得过时
- 修改后重新合并
- 不适用于频繁更新的数据集

## 常见模式

### 数据不断增长的时间序列
```python
# Start with empty first dimension
z = zarr.open('timeseries.zarr', mode='a',
              shape=(0, 720, 1440),
              chunks=(1, 720, 1440),
              dtype='f4')

# Append new time steps
for new_timestep in data_stream:
    z.append(new_timestep, axis=0)
```

### 处理大型数组在块中
```python
z = zarr.open('large_data.zarr', mode='r')

# Process without loading entire array
for i in range(0, z.shape[0], 1000):
    chunk = z[i:i+1000, :]
    result = process(chunk)
    save(result)
```

### 格式转换管道
```python
# HDF5 → Zarr
import h5py
with h5py.File('data.h5', 'r') as h5:
    z = zarr.array(h5['dataset'][:], chunks=(1000, 1000), store='data.zarr')

# Zarr → NumPy file
z = zarr.open('data.zarr', mode='r')
np.save('data.npy', z[:])

# Zarr → NetCDF (via Xarray)
ds = xr.open_zarr('data.zarr')
ds.to_netcdf('data.nc')
```

## 性能优化快速检查表

1. **块大小**：每个块 1-10 MB
2. **块形状**：与访问模式
3对齐。 **压缩**：
 - 快速：`BloscCodec(cname='lz4', clevel=1)`
  - 平衡：`BloscCodec(cname='zstd', clevel=5)`
  - 最大：`GzipCodec(level=9)`
4. **云存储**：
  - 更大的块（5-100 MB）
  - 合并元数据
  - 考虑分片
5. **并行I/O**：对于大型操作使用Dask
6. **内存**：分块处理，不要加载整个数组

## 调试和分析

```python
z = zarr.open('data.zarr', mode='r')

# Detailed information
print(z.info)

# Size statistics
print(f"Uncompressed: {z.nbytes / 1e6:.2f} MB")
print(f"Compressed: {z.nbytes_stored / 1e6:.2f} MB")
print(f"Ratio: {z.nbytes / z.nbytes_stored:.1f}x")

# Chunk information
print(f"Chunks: {z.chunks}")
print(f"Number of chunks: {z.nchunks}")
print(f"Chunk grid: {z.cdata_shape}")
```

## 常见数据类型

```python
# Integers
'i1', 'i2', 'i4', 'i8'  # Signed: 8, 16, 32, 64-bit
'u1', 'u2', 'u4', 'u8'  # Unsigned: 8, 16, 32, 64-bit

# Floats
'f2', 'f4', 'f8'  # 16, 32, 64-bit (half, single, double precision)

# Others
'bool'     # Boolean
'c8', 'c16'  # Complex: 64, 128-bit
'S10'      # Fixed-length string (10 bytes)
'U10'      # Unicode string (10 characters)
```

## 版本兼容性

Zarr-Python版本3.x同时支持：
- **Zarr v2格式**：传统格式，广泛兼容
- **Zarr v3格式**：带分片的新格式，改进元数据

检查格式版本：
```python
# Zarr automatically detects format version
z = zarr.open('data.zarr', mode='r')
# Format info available in metadata
```

## 错误搬运

```python
try:
    z = zarr.open_array('data.zarr', mode='r')
except zarr.errors.PathNotFoundError:
    print("Array does not exist")
except zarr.errors.ReadOnlyError:
    print("Cannot write to read-only array")
except Exception as e:
    print(f"Unexpected error: {e}")
```
