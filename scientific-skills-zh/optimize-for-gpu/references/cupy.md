# CuPy Reference

CuPy 是一个兼容 NumPy/SciPy 的数组库，用于 GPU 加速计算。它包含 NVIDIA 的优化库（cuBLAS、cuFFT、cuSOLVER、cuSPARSE、cuRAND），因此标准数组操作已经经过高度调整。大多数 NumPy 代码只需更改导入即可工作。

> **完整文档：** https://docs.cupy.dev/en/stable/

## 目录

1. [安装和设置](#installation-and-setup)
2. [直接替换模式](#the-drop-in-replacement-pattern)
3. [核心API：cupy.ndarray](#core-api)
4. [支持的操作](#supported-operations)
5. [自定义内核](#custom-kernels)
6. [内核融合](#kernel-fusion)
7. [内存管理](#内存管理)
8. [流和异步操作](#streams-and-async-operations)
9. [多 GPU](#multi-gpu)
10. [性能优化](#性能优化)
11. [互操作性](#互操作性)
12. [与 NumPy 的主要区别](#key-differences-from-numpy)
13. [常见陷阱](#common-pitfalls)
14. [环境变量](#environment-variables)

- --

## 安装和设置

在所有安装说明、文档字符串、注释和错误中始终使用 `uv add`（切勿使用 `pip install` 或 `conda install`） messages.

```bash
uv add cupy-cuda12x    # For CUDA 12.x (most common)
```

Verify:
```python
import cupy as cp
print(cp.cuda.runtime.getDeviceCount())  # >= 1 means GPU is available
print(cp.show_config())                  # Full environment info
```

- --

## 直接替换模式

GPU 加速 NumPy 代码的最快方法：更改import.

```python
# Before (CPU)
import numpy as np
a = np.random.rand(10_000_000)
b = np.fft.fft(a)
c = np.sort(b.real)

# After (GPU)
import cupy as cp
a = cp.random.rand(10_000_000)
b = cp.fft.fft(a)
c = cp.sort(b.real)
```

### CPU和GPU之间的数据传输

```python
# NumPy → CuPy (CPU → GPU)
gpu_array = cp.asarray(numpy_array)     # Zero-copy if already on current device
gpu_array = cp.array(numpy_array)       # Always copies

# CuPy → NumPy (GPU → CPU)
cpu_array = cp.asnumpy(gpu_array)       # Copy to CPU
cpu_array = gpu_array.get()             # Same thing
```

### 编写CPU/GPU无关代码

```python
def normalize(x):
    xp = cp.get_array_module(x)  # Returns cupy or numpy depending on input
    return x / xp.linalg.norm(x)

# Works with both NumPy and CuPy arrays
normalize(numpy_array)   # Runs on CPU
normalize(cupy_array)    # Runs on GPU
```

CuPy数组实现`__array_ufunc__`和`__array_function__`，因此当给定 CuPy 数组 (NumPy >= 1.17)时，NumPy 函数可以自动分派到 CuPy。

- --

## 核心 API

`cupy.ndarray` 镜像 `numpy.ndarray` — 相同属性（`shape`、`dtype`、`ndim`、`size`、`strides`、`T`），加上 `device`（阵列所在的 GPU） on).

* *重要：** `cupy.ndarray` 和 `numpy.ndarray` 不可隐式转换。每次转换都会导致主机设备数据传输。

### 数组创建

```python
cp.empty((1000, 1000), dtype=cp.float32)
cp.zeros((1000,), dtype=cp.float64)
cp.ones((512, 512), dtype=cp.float32)
cp.full((100,), fill_value=3.14, dtype=cp.float32)
cp.arange(0, 100, 0.1)
cp.linspace(0, 1, 1000)
cp.eye(100)
cp.random.rand(1000, 1000)                    # Uniform [0, 1)
cp.random.randn(1000, 1000)                   # Standard normal
cp.random.default_rng(42).normal(0, 1, 1000)  # Generator API
```

CuPy 的随机数支持 `dtype` 参数 (float32/float64) — 与始终返回 float64 的 NumPy 不同。当不需要双精度时，使用 `dtype=cp.float32`。

- --

## 支持的操作

CuPy 实现了 NumPy 的大部分和 SciPy 的大部分。所有都是 GPU 加速的。

### 数组数学和按元素运算
`sin`、`cos`、`tan`、`exp`、`log`、`log2`、`log10`、 `sqrt`、`square`、`abs`、`power`、`add`、`subtract`、`multiply`、`divide`、`mod`、`clip`、 `sign`、`ceil`、`floor`、`round`、`maximum`、`minimum`

### 减少
`sum`、`prod`、 `mean`、`std`、`var`、`min`、`max`、`argmin`、`argmax`、`cumsum`、`cumprod`、`any`、 `all`、`nansum`、`nanmean`、`nanstd`、`nanvar`

### 线性代数（`cupy.linalg` — 由 cuBLAS/cuSOLVER 提供支持）
`dot`， `matmul`、`@`操作员、`tensordot`、`einsum`、`inner`、`outer`、`cholesky`、`qr`、`svd`、`eig`、 `eigh`、`eigvalsh`、`norm`、`solve`、`inv`、`pinv`、`lstsq`、`det`、`slogdet`、`matrix_rank`、 `matrix_power`

### FFT (`cupy.fft` — 由 cuFFT 提供支持)
`fft`、`ifft`、`fft2`、`ifft2`、`fftn`、`ifftn`、`rfft`、 `irfft`、`rfft2`、`irfft2`、`rfftn`、`irfftn`、`fftfreq`、`rfftfreq`、`fftshift`、`ifftshift`

### 排序和搜索
`sort`、`argsort`、`partition`、`argpartition`、`argmin`、`argmax`、`where`、`nonzero`、`unique`、 `searchsorted`

### 数组操作
`reshape`、`ravel`、`flatten`、`transpose`、`swapaxes`、`concatenate`、`stack`、 `vstack`、`hstack`、`dstack`、`split`、`hsplit`、`vsplit`、`tile`、`repeat`、`pad`、 `flip`、`fliplr`、`flipud`、`roll`、`rot90`、`broadcast_to`、`expand_dims`、`squeeze`

### 稀疏矩阵(`cupyx.scipy.sparse`)
CSR、CSC、COO 格式。矩阵-向量乘法、矩阵-矩阵乘法、格式之间的转换。由 cuSPARSE 提供支持。

### 信号处理 (`cupyx.scipy.signal`)
卷积、相关、滤波、窗函数。

### 特殊函数 (`cupyx.scipy.special`)
贝塞尔函数、误差函数、伽马函数等。

### 统计
`mean`、`median`、`std`、`var`、`percentile`、`quantile`、`corrcoef`、`cov`、`histogram`、 `bincount`、`digitize`

- --

## 自定义内核

当内置操作不够用时，CuPy 提供了多种编写自定义 GPU 代码的方法，按从最简单到最强大的顺序排列。

### ElementwiseKernel — 自定义 Element-wise Operations

CuPy 自动处理索引和广播。您只需用 C++ 编写每个元素的逻辑即可。

```python
squared_diff = cp.ElementwiseKernel(
    'float32 x, float32 y',   # Input params
    'float32 z',               # Output params
    'z = (x - y) * (x - y)',  # Per-element operation (C++ code)
    'squared_diff'             # Kernel name
)

result = squared_diff(a, b)  # Broadcasting works automatically
```

* *类型通用内核：**使用单字母类型占位符。相同字母 = 相同类型，在调用时从参数解析。

```python
generic_squared_diff = cp.ElementwiseKernel(
    'T x, T y', 'T z',
    'z = (x - y) * (x - y)',
    'generic_squared_diff'
)
# Works with float32, float64, etc. — type inferred from inputs
```

* *原始索引：** 使用 `raw` 前缀以禁用自动索引。使用 `i` 作为循环索引。

```python
# Access neighbors — raw disables auto-indexing so you can index manually
stencil = cp.ElementwiseKernel(
    'raw T x', 'T y',
    'y = (x[i > 0 ? i-1 : 0] + x[i] + x[i < _ind.size()-1 ? i+1 : _ind.size()-1]) / 3',
    'stencil_1d'
)
```

### ReductionKernel — 自定义缩减

四部分缩减：映射每个元素、缩减对、后处理结果。

```python
l2norm = cp.ReductionKernel(
    'T x',           # Input
    'T y',           # Output
    'x * x',         # Map: square each element
    'a + b',         # Reduce: sum pairs (a, b are the binary operands)
    'y = sqrt(a)',   # Post-map: sqrt of final sum
    '0',             # Identity element
    'l2norm'         # Kernel name
)

norm = l2norm(array)        # Full reduction → scalar
norms = l2norm(matrix, axis=1)  # Reduce along axis → vector
```

### RawKernel — 完整 CUDA C/C++

用于完全控制网格、块、共享内存 - 写入原始 CUDA.

```python
kernel_code = r'''
extern "C" __global__
void vector_add(const float* a, const float* b, float* c, int n) {
    int tid = blockDim.x * blockIdx.x + threadIdx.x;
    if (tid < n) {
        c[tid] = a[tid] + b[tid];
    }
}
'''
vector_add = cp.RawKernel(kernel_code, 'vector_add')

n = 1_000_000
a = cp.random.rand(n, dtype=cp.float32)
b = cp.random.rand(n, dtype=cp.float32)
c = cp.zeros(n, dtype=cp.float32)

threads = 256
blocks = (n + threads - 1) // threads
vector_add((blocks,), (threads,), (a, b, c, n))  # (grid, block, args)
```

 * *重要的 RawKernel 警告：**
  - 忽略数组视图/步长 - `matrix.T` 被视为 `matrix`。自己处理步幅。
- 使用 `extern "C"` 防止 C++ 名称修改。
- 对于复数，包括 `<cupy/complex.cuh>`.
- 编译后的二进制文件缓存在 `~/.cupy/kernel_cache`.

* *CuPy dtype 到 CUDA 类型映射：**

| CuPy dtype | CUDA类型 |
|-----------|-----------|
| `float16` | `half` |
| `float32` | `float` |
| `float64` | `double` |
| `int32` | `int` |
| `int64` | `long long` |
| `complex64` | `complex<float>` |
| `complex128` | `complex<double>` |

### RawModule — 大型 CUDA 代码库

对于多内核 CUDA 文件或预编译的二进制文件：

```python
module = cp.RawModule(code=cuda_source)       # From source string
module = cp.RawModule(path='kernels.cu')      # From file
module = cp.RawModule(path='kernels.cubin')   # From precompiled

kernel = module.get_function('my_kernel')
kernel((blocks,), (threads,), (args...))
```

### JIT 内核 (cupyx.jit.rawkernel) — Python 中的 CUDA 内核语法

使用Python语法而不是C++编写CUDA风格的内核。

```python
@cupyx.jit.rawkernel()
def my_kernel(x, y, size):
    tid = cupyx.jit.grid(1)
    if tid < size:
        y[tid] = x[tid] * 2.0

my_kernel[blocks, threads](x, y, n)
```

可用的JIT原语：
- `cupyx.jit.threadIdx`、`blockIdx`、`blockDim`、 `gridDim`
- `cupyx.jit.grid(ndim)`、`gridsize(ndim)`
- `cupyx.jit.syncthreads()`、`syncwarp()`
- `cupyx.jit.shared_memory(dtype, size)`
- `cupyx.jit.atomic_add/min/max/and/or/xor(array, index, value)`
- 经纱洗牌：`shfl_sync`、`shfl_up_sync`、`shfl_down_sync`、`shfl_xor_sync`

* *限制：** 在 Python REPL 中不起作用（需要源代码访问）。从 .py 文件中使用。

- --

## 内核融合

将多个逐元素操作合并到一个内核启动中 - 消除中间数组并减少内核启动开销。

```python
@cp.fuse()
def fused_op(x, y):
    return cp.sqrt((x - y) ** 2 + 1.0)

# This compiles into ONE kernel instead of multiple
result = fused_op(a, b)
```

* *限制：**仅融合逐元素操作和简单归约操作。不支持 `matmul`、`reshape`、索引等。

- --

## 内存管理

### 内存池（默认行为）

CuPy 默认使用内存池 — 这对于性能至关重要。池缓存释放的 GPU 内存以供重用，避免昂贵的 `cudaMalloc`/`cudaFree` 调用和隐式同步。

* *关键见解：** 当数组超出范围时，内存不会释放给操作系统 - 它会返回到池中。这是预期的行为（在 `nvidia-smi` 中显示为仍分配）。

```python
mempool = cp.get_default_memory_pool()
mempool.used_bytes()        # Currently allocated by CuPy arrays
mempool.total_bytes()       # Total held by pool (including free blocks)
mempool.free_all_blocks()   # Release all unused memory back to OS

pinned_mempool = cp.get_default_pinned_memory_pool()
pinned_mempool.free_all_blocks()
```

### 限制 GPU 内存

```python
mempool = cp.get_default_memory_pool()
with cp.cuda.Device(0):
    mempool.set_limit(size=4 * 1024**3)  # 4 GiB limit for GPU 0
```

 或者通过环境变量（之前设置） `import cupy`):
```bash
export CUPY_GPU_MEMORY_LIMIT="50%"     # Percentage of total GPU memory
export CUPY_GPU_MEMORY_LIMIT="4294967296"  # Bytes
```

### 托管（统一）内存

数据在CPU和GPU之间自动迁移。当数据不适合 GPU 内存时很有用。

```python
cp.cuda.set_allocator(cp.cuda.MemoryPool(cp.cuda.malloc_managed).malloc)
```

### 用于快速传输的固定内存

```python
# High-level API
pinned_array = cupyx.empty_pinned((1000,), dtype=np.float32)
pinned_array = cupyx.zeros_pinned((1000,), dtype=np.float32)

# These are NumPy arrays backed by page-locked memory — transfers to GPU are faster
```

### 禁用池

```python
cp.cuda.set_allocator(None)                    # Disable device pool
cp.cuda.set_pinned_memory_allocator(None)      # Disable pinned pool
```

必须在之前完成任何 CuPy 操作。

### 使用 RMM（RAPIDS 内存管理器）

当将 CuPy 与 cuDF/RAPIDS 一起使用时，在单个分配器上对齐：

```python
import rmm
rmm.reinitialize(pool_allocator=True)
cp.cuda.set_allocator(rmm.rmm_cupy_allocator)
```

- --

## 流和异步操作

Streams 支持重叠计算

```python
stream = cp.cuda.Stream()

# Context manager style
with stream:
    d_data = cp.asarray(host_data)     # H→D transfer on this stream
    result = cp.sum(d_data)            # Kernel on this stream
# Operations enqueued but may not be complete here

stream.synchronize()  # Wait for all operations on this stream
```

### 多个重叠流

```python
s1 = cp.cuda.Stream()
s2 = cp.cuda.Stream()

with s1:
    d_a = cp.asarray(data_a)
    result_a = cp.fft.fft(d_a)

with s2:
    d_b = cp.asarray(data_b)  # Overlaps with s1's FFT
    result_b = cp.fft.fft(d_b)

cp.cuda.Device().synchronize()  # Wait for all streams
```

### 计时事件

```python
start = cp.cuda.Event()
end = cp.cuda.Event()

start.record()
# ... GPU operations ...
end.record()
end.synchronize()

elapsed_ms = cp.cuda.get_elapsed_time(start, end)
```

### 每线程默认值Stream

```bash
export CUPY_CUDA_PER_THREAD_DEFAULT_STREAM=1
```

启用每线程默认流，以在多线程应用程序中实现更好的并发性。

- --

## 多GPU

```python
# Set current device
cp.cuda.Device(0).use()

# Context manager
with cp.cuda.Device(1):
    x = cp.array([1, 2, 3])  # Allocated on GPU 1

# Check which device an array is on
print(x.device)  # Device 1
```

如果 GPU 拓扑支持，跨设备操作可以通过 P2P（点对点）内存访问进行。使用 `cp.asarray()` 在设备之间显式传输数组。

### 每设备内存限制

```python
mempool = cp.get_default_memory_pool()
with cp.cuda.Device(0):
    mempool.set_limit(size=4 * 1024**3)
with cp.cuda.Device(1):
    mempool.set_limit(size=4 * 1024**3)
```

- --

## 性能优化

### 基准测试（关键第一步）

* *切勿使用用于 GPU 代码的 `time.perf_counter()` 或 `%timeit`** — 它们仅测量 CPU 时间，而不测量 GPU 执行时间。 CuPy 操作是异步的。

```python
from cupyx.profiler import benchmark

result = benchmark(my_function, (arg1, arg2), n_repeat=100, n_warmup=10)
print(result)  # Shows CPU and GPU elapsed times with statistics
```

In IPython/Jupyter:
```python
%load_ext cupy
%gpu_timeit my_function(args)
```

### 一次性开销

- **上下文初始化：** 第一次 CuPy 调用可能需要 1-5 秒（CUDA 上下文创建）。这是一次性的。
- **内核 JIT 编译：** 对任何操作的第一次调用都会触发即时内核编译。缓存在`~/.cupy/kernel_cache`中。在 CI/CD 运行中保留此目录。

### CUB 和 cuTENSOR 加速

```bash
# CuPy v11+ uses CUB by default
export CUPY_ACCELERATORS=cub          # CUB only (default)
export CUPY_ACCELERATORS=cub,cutensor # Both (requires cuTENSOR installed)
```

CUB 加速：减少（`sum`、`prod`、`amin`、`amax`、 `argmin`、`argmax`)、包含扫描 (`cumsum`)、直方图、稀疏矩阵向量乘法和 `ReductionKernel`。可以为缩减提供约 100 倍的加速。

cuTENSOR 加速：二进制元素 ufunc、缩减、张量收缩。

### 关键优化策略

1. **与 float64 相比，更喜欢 float32。** 消费类 GPU 的 float32 吞吐量高出 2-32 倍。精度允许时使用`dtype=cp.float32`。

2. **最大限度地减少 CPU-GPU 传输。** 每个 `cp.asnumpy()` / `.get()` 都会触发同步和 PCI-e 传输。尽可能长时间地将数据保留在GPU上。

3. **使用内核融合。** `@cp.fuse()` 将多个元素操作合并到一个内核中，消除了中间数组。

4. **批量操作。** 较少的大型操作胜过许多小型操作（内核启动开销约为每个 5-20us）。

5. **预分配输出数组。** 在ufuncs中使用`out=`参数以避免重复分配：
 ```python
 cp.add(a, b, out=result) # 写入现有数组
 ```

6. **使用就地操作。** `a += b` 避免分配新数组。

7. **使用流**来重叠计算和数据传输。

8. **带有 NVTX 标记的配置文件**，用于 Nsight Systems 分析：
 ```python
 with cupyx.profiler.time_range('my_operation', color_id=0):
 结果 = Heavy_computation()
 ```

### 决策树：哪种内核方法？

1. **可以表示为 NumPy 操作吗？** → 使用内置的 CuPy 函数（开发速度最快，通常性能最佳）
2. **多个链式元素运算？** → 使用 `@cp.fuse()`
3. **通过广播自定义元素？** → 使用 `ElementwiseKernel`
4. **定制减少？** → 使用`ReductionKernel`
5. **需要完整的网格/块/共享内存控制？** → 使用 `RawKernel` 或 `cupyx.jit.rawkernel`
6. **大型 CUDA 代码库？** → 使用 `RawModule`

- --

## 互操作性

CuPy 通过 CUDA 阵列接口和 DLPack 协议与其他 GPU 库进行互操作 — 两者都支持零拷贝数据共享。

### NumPy

```python
# NumPy functions auto-dispatch to CuPy (NumPy >= 1.17)
import numpy as np
result = np.sum(cupy_array)  # Dispatches to CuPy, returns CuPy array
```

### Numba

```python
from numba import cuda

@cuda.jit
def numba_kernel(x, y):
    i = cuda.grid(1)
    if i < x.shape[0]:
        y[i] = x[i] * 2

# CuPy arrays pass directly to Numba kernels — zero copy
a = cp.arange(1000, dtype=cp.float32)
b = cp.zeros_like(a)
numba_kernel[4, 256](a, b)
```

### PyTorch

```python
import torch

# CuPy → PyTorch (zero copy via CUDA Array Interface)
cupy_array = cp.array([1.0, 2.0, 3.0], dtype=cp.float32)
torch_tensor = torch.as_tensor(cupy_array, device='cuda')

# PyTorch → CuPy (zero copy)
cupy_array = cp.asarray(torch_tensor)

# Via DLPack (also zero copy)
cupy_array = cp.from_dlpack(torch_tensor)
torch_tensor = torch.from_dlpack(cupy_array)
```

### cuDF

```python
import cudf

# cuDF → CuPy
arr = df.to_cupy()
arr = cp.asarray(df['column'])

# CuPy → cuDF
df = cudf.DataFrame(cupy_array)
s = cudf.Series(cupy_array)
```

### 原始指针互操作

```python
# Export pointer
ptr = cupy_array.data.ptr  # Raw device pointer as int

# Import foreign pointer
mem = cp.cuda.UnownedMemory(ptr, size_bytes, owner=owner_obj)
memptr = cp.cuda.MemoryPointer(mem, offset=0)
arr = cp.ndarray(shape, dtype, memptr=memptr)
```

- --

## 与 NumPy

的主要差异这些是行为差异，如果您不知道，可能会导致错误他们.

1. **归约返回 0 维数组，而不是标量。** `cp.sum(a)` 返回 0 维 `cupy.ndarray`，而不是 Python 浮点数。这避免了隐式 GPU-CPU 同步。如果需要标量，请使用 `.item()`。

2. **越界索引默默地换行。** NumPy 引发 `IndexError`； CuPy 环绕且没有错误。

3. **赋值中的重复索引未定义。** `a[[0, 0]] = [1, 2]` — NumPy 存储最后一个值； CuPy 存储未定义的值（GPU 竞争条件）。

4. **浮点到整数的转换在边缘处有所不同。** 将负浮点转换为无符号整数或将无穷大转换为整数会得到与 NumPy.

5 不同的结果。 **没有字符串/对象数据类型。** CuPy 仅支持数字类型。没有带有字符串字段的结构化数组。

6. **CuPy ufunc 需要 CuPy 数组。** 与 NumPy ufunc 不同，CuPy ufunc 不接受列表或 NumPy 数组 - 首先转换。

7. **随机种子数组经过哈希处理。** 数组种子产生的熵比 NumPy 的方法少。

- --

## 常见陷阱

1. **使用 CPU 计时器进行测量。** GPU 操作是异步的。 `time.perf_counter()` 仅测量“入队”操作的时间，而不是执行它们的时间。始终使用 `cupyx.profiler.benchmark()`.

2. **不必要的往返。** 每个 `cp.asnumpy()` / `.get()` 都会同步 GPU 并通过 PCI-e 复制数据。重构代码以将数据保留在 GPU.

3 上。 **来自池的“内存泄漏”。**内存池缓存已释放的块。 `nvidia-smi` 将它们显示为已分配。使用`mempool.free_all_blocks()`释放.

4. **首次调用延迟。** CUDA 上下文初始化 + 内核 JIT 编译。基准测试前热身。

5. **混合设备。** 在 GPU 1 上使用 GPU 0 的数组而不进行显式传输可能会失败或速度很慢。

6. **RawKernel 忽略视图。** 传递给 RawKernel 的转置或切片数组被视为原始连续布局。您必须手动处理步幅。

7. **在读取结果之前忘记 `synchronize()`。** 如果将数据传回 CPU 或在非 CuPy 代码中使用它，请确保先完成 GPU。

- --

## 环境变量

|变量|目的|
|----------|---------|
| `CUPY_ACCELERATORS` |后端列表：`cub`、`cutensor`（默认：v11+ 的 `cub`）|
| `CUPY_CACHE_DIR` |内核缓存目录（默认：`~/.cupy/kernel_cache`）|
| `CUPY_GPU_MEMORY_LIMIT` | GPU内存限制（字节或`"50%"`）|
| `CUPY_CACHE_SAVE_CUDA_SOURCE` |设置 `1` 转储内核源以进行分析 |
| `CUPY_CUDA_PER_THREAD_DEFAULT_STREAM` |为每线程默认流设置 `1` |
