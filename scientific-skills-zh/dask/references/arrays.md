# Dask Arrays

## 概述

Dask Array 使用阻塞算法实现 NumPy 的 ndarray 接口。它协调排列成网格的许多 NumPy 数组，以便能够利用跨多个核心的并行性对大于可用内存的数据集进行计算。

## 核心概念

A Dask 数组分为块（块）：
 - 每个块都是一个常规的 NumPy 数组
  - 操作应用于每个块并行
- 自动组合结果
- 启用核外计算（数据大于RAM）

## 关键功能

### Dask 数组支持什么

* *数学运算**：
- 算术运算（+、-、*、 /)
- 标量函数（指数、对数、三角函数）
- 逐元素运算

* *归约**：
- `sum()`、`mean()`、`std()`、 `var()`
- 沿指定轴的缩减
- `min()`、`max()`、`argmin()`、`argmax()`

* *线性代数**：
- 张量收缩
- 点产品和矩阵乘法
- 一些分解（SVD，QR）

* *数据操作**：
- 转置
- 切片（标准和花式索引）
- 重塑
- 串联和堆叠

* *数组协议**：
- 通用函数（ufunc）
- 用于互操作性的NumPy协议

## 何时使用Dask数组

* *使用Dask数组何时**：
- 数组超出可用RAM
- 计算可以跨块并行化
- 使用NumPy风格的数值运算
- 需要将NumPy代码扩展到更大的数据集

* *坚持使用NumPy当**：
- 数组适合内存中
- 操作需要数据的全局视图
- 使用专门的Dask
 中不可用的功能 - 仅使用 NumPy 性能就足够了

## 重要限制

Dask 数组故意不实现某些 NumPy 功能：

* *未实现**：
- 大多数`np.linalg`函数（仅提供基本操作）
- 难以并行化的操作（如完全排序）
- 内存效率低下的操作（转换为列表，通过循环迭代）
- 许多专用函数（由社区需求驱动）

* *解决方法**：对于不受支持的情况操作，请考虑将 `map_blocks` 与自定义 NumPy 代码结合使用。

## 创建 Dask 数组

### 来自 NumPy 数组
```python
import dask.array as da
import numpy as np

# Create from NumPy array with specified chunks
x = np.arange(10000)
dx = da.from_array(x, chunks=1000)  # Creates 10 chunks of 1000 elements each
```

### 随机数组
```python
# Create random array with specified chunks
x = da.random.random((10000, 10000), chunks=(1000, 1000))

# Other random functions
x = da.random.normal(10, 0.1, size=(10000, 10000), chunks=(1000, 1000))
```

### 零、一和空
```python
# Create arrays filled with constants
zeros = da.zeros((10000, 10000), chunks=(1000, 1000))
ones = da.ones((10000, 10000), chunks=(1000, 1000))
empty = da.empty((10000, 10000), chunks=(1000, 1000))
```

### 来自函数
```python
# Create array from function
def create_block(block_id):
    return np.random.random((1000, 1000)) * block_id[0]

x = da.from_delayed(
    [[dask.delayed(create_block)((i, j)) for j in range(10)] for i in range(10)],
    shape=(10000, 10000),
    dtype=float
)
```

### 来自磁盘
```python
# Load from HDF5
import h5py
f = h5py.File('myfile.hdf5', mode='r')
x = da.from_array(f['/data'], chunks=(1000, 1000))

# Load from Zarr
import zarr
z = zarr.open('myfile.zarr', mode='r')
x = da.from_array(z, chunks=(1000, 1000))
```

## 常用运算

### 算术运算
```python
import dask.array as da

x = da.random.random((10000, 10000), chunks=(1000, 1000))
y = da.random.random((10000, 10000), chunks=(1000, 1000))

# Element-wise operations (lazy)
z = x + y
z = x * y
z = da.exp(x)
z = da.log(y)

# Compute result
result = z.compute()
```

### 缩减
```python
# Reductions along axes
total = x.sum().compute()
mean = x.mean().compute()
std = x.std().compute()

# Reduction along specific axis
row_means = x.mean(axis=1).compute()
col_sums = x.sum(axis=0).compute()
```

### 切片和索引
```python
# Standard slicing (returns Dask Array)
subset = x[1000:5000, 2000:8000]

# Fancy indexing
indices = [0, 5, 10, 15]
selected = x[indices, :]

# Boolean indexing
mask = x > 0.5
filtered = x[mask]
```

### 矩阵运算
```python
# Matrix multiplication
A = da.random.random((10000, 5000), chunks=(1000, 1000))
B = da.random.random((5000, 8000), chunks=(1000, 1000))
C = da.matmul(A, B)
result = C.compute()

# Dot product
dot_product = da.dot(A, B)

# Transpose
AT = A.T
```

### 线性代数
```python
# SVD (Singular Value Decomposition)
U, s, Vt = da.linalg.svd(A)
U_computed, s_computed, Vt_computed = dask.compute(U, s, Vt)

# QR decomposition
Q, R = da.linalg.qr(A)
Q_computed, R_computed = dask.compute(Q, R)

# Note: Only some linalg operations are available
```

### 整形和操作
```python
# Reshape
x = da.random.random((10000, 10000), chunks=(1000, 1000))
reshaped = x.reshape(5000, 20000)

# Transpose
transposed = x.T

# Concatenate
x1 = da.random.random((5000, 10000), chunks=(1000, 1000))
x2 = da.random.random((5000, 10000), chunks=(1000, 1000))
combined = da.concatenate([x1, x2], axis=0)

# Stack
stacked = da.stack([x1, x2], axis=0)
```

## 分块策略

分块对于Dask阵列性能至关重要。

### 块大小指南

* *好的块大小**：
- 每个块：~10-100 MB （压缩）
- 数字数据每块约 100 万个元素
- 并行性和开销之间的平衡

* *计算示例**：
```python
# For float64 data (8 bytes per element)
# Target 100 MB chunks: 100 MB / 8 bytes = 12.5M elements

# For 2D array (10000, 10000):
x = da.random.random((10000, 10000), chunks=(1000, 1000))  # ~8 MB per chunk
```

### 查看块结构
```python
# Check chunks
print(x.chunks)  # ((1000, 1000, ...), (1000, 1000, ...))

# Number of chunks
print(x.npartitions)

# Chunk sizes in bytes
print(x.nbytes / x.npartitions)
```

### 重新分块
```python
# Change chunk sizes
x = da.random.random((10000, 10000), chunks=(500, 500))
x_rechunked = x.rechunk((2000, 2000))

# Rechunk specific dimension
x_rechunked = x.rechunk({0: 2000, 1: 'auto'})
```

## 使用map_blocks的自定义操作

对于Dask中不可用的操作，请使用`map_blocks`:

```python
import dask.array as da
import numpy as np

def custom_function(block):
    # Apply custom NumPy operation
    return np.fft.fft2(block)

x = da.random.random((10000, 10000), chunks=(1000, 1000))
result = da.map_blocks(custom_function, x, dtype=x.dtype)

# Compute
output = result.compute()
```

### 具有不同输出形状的map_blocks
```python
def reduction_function(block):
    # Returns scalar for each block
    return np.array([block.mean()])

result = da.map_blocks(
    reduction_function,
    x,
    dtype='float64',
    drop_axis=[0, 1],  # Output has no axes from input
    new_axis=0,        # Output has new axis
    chunks=(1,)        # One element per block
)
```

## 延迟评估和计算

### 延迟操作
```python
# All operations are lazy (instant, no computation)
x = da.random.random((10000, 10000), chunks=(1000, 1000))
y = x + 100
z = y.mean(axis=0)
result = z * 2

# Nothing computed yet, just task graph built
```

### 触发计算
```python
# Compute single result
final = result.compute()

# Compute multiple results efficiently
result1, result2 = dask.compute(operation1, operation2)
```

### 保存在内存中
```python
# Keep intermediate results in memory
x_cached = x.persist()

# Reuse cached results
y1 = (x_cached + 10).compute()
y2 = (x_cached * 2).compute()
```

## 保存结果

### 到NumPy
```python
# Convert to NumPy (loads all in memory)
numpy_array = dask_array.compute()
```

### 到磁盘
```python
# Save to HDF5
import h5py
with h5py.File('output.hdf5', mode='w') as f:
    dset = f.create_dataset('/data', shape=x.shape, dtype=x.dtype)
    da.store(x, dset)

# Save to Zarr
import zarr
z = zarr.open('output.zarr', mode='w', shape=x.shape, dtype=x.dtype, chunks=x.chunks)
da.store(x, z)
```

## 性能注意事项

### 高效操作
- 按元素操作：非常高效
- 可并行操作的减少：高效
- 沿块边界切片：高效
- 具有良好块对齐的矩阵操作：高效

### 昂贵的操作
- 跨多个块切片：需要数据运动
- 需要全局排序的操作：没有得到很好的支持
- 极其不规则的访问模式：性能较差
- 块对齐较差的操作：需要重新分块

### 优化提示

* *1。选择合适的块尺寸**
```python
# Aim for balanced chunks
# Good: ~100 MB per chunk
x = da.random.random((100000, 10000), chunks=(10000, 10000))
```

* *2。对齐操作块**
```python
# Make sure chunks align for operations
x = da.random.random((10000, 10000), chunks=(1000, 1000))
y = da.random.random((10000, 10000), chunks=(1000, 1000))  # Aligned
z = x + y  # Efficient
```

* *3。使用适当的调度程序**
```python
# Arrays work well with threaded scheduler (default)
# Shared memory access is efficient
result = x.compute()  # Uses threads by default
```

* *4。最小化数据传输**
```python
# Better: Compute on each chunk, then transfer results
means = x.mean(axis=1).compute()  # Transfers less data

# Worse: Transfer all data then compute
x_numpy = x.compute()
means = x_numpy.mean(axis=1)  # Transfers more data
```

## 常见模式

### 图像处理
```python
import dask.array as da

# Load large image stack
images = da.from_zarr('images.zarr')

# Apply filtering
def apply_gaussian(block):
    from scipy.ndimage import gaussian_filter
    return gaussian_filter(block, sigma=2)

filtered = da.map_blocks(apply_gaussian, images, dtype=images.dtype)

# Compute statistics
mean_intensity = filtered.mean().compute()
```

### 科学计算
```python
# Large-scale numerical simulation
x = da.random.random((100000, 100000), chunks=(10000, 10000))

# Apply iterative computation
for i in range(num_iterations):
    x = da.exp(-x) * da.sin(x)
    x = x.persist()  # Keep in memory for next iteration

# Final result
result = x.compute()
```

### 数据分析
```python
# Load large dataset
data = da.from_zarr('measurements.zarr')

# Compute statistics
mean = data.mean(axis=0)
std = data.std(axis=0)
normalized = (data - mean) / std

# Save normalized data
da.to_zarr(normalized, 'normalized.zarr')
```

## 与其他工具集成

### XArray
```python
import xarray as xr
import dask.array as da

# XArray wraps Dask arrays with labeled dimensions
data = da.random.random((1000, 2000, 3000), chunks=(100, 200, 300))
dataset = xr.DataArray(
    data,
    dims=['time', 'y', 'x'],
    coords={'time': range(1000), 'y': range(2000), 'x': range(3000)}
)
```

### Scikit-learn（通过Dask-ML)
```python
# Some scikit-learn compatible operations
from dask_ml.preprocessing import StandardScaler

X = da.random.random((10000, 100), chunks=(1000, 100))
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

## 调试技巧

### 可视化任务图
```python
# Visualize computation graph (for small arrays)
x = da.random.random((100, 100), chunks=(10, 10))
y = x + 1
y.visualize(filename='graph.png')
```

### 检查数组属性
```python
# Inspect before computing
print(f"Shape: {x.shape}")
print(f"Dtype: {x.dtype}")
print(f"Chunks: {x.chunks}")
print(f"Number of tasks: {len(x.__dask_graph__())}")
```

### 首先在小型阵列上进行测试
```python
# Test logic on small array
small_x = da.random.random((100, 100), chunks=(50, 50))
result_small = computation(small_x).compute()

# Validate, then scale
large_x = da.random.random((100000, 100000), chunks=(10000, 10000))
result_large = computation(large_x).compute()
```
