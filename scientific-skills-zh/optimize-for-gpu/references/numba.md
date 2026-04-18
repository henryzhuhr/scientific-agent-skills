# Numba CUDA 参考

Numba 将 Python 直接编译为 CUDA 内核，让您可以完全控制 GPU 线程、块、共享内存和同步。当您的算法需要无法表示为标准数组操作的自定义 GPU 逻辑时，请使用 Numba。

> **完整文档：** https://numba.readthedocs.io/en/stable/cuda/index.html

## 目录

1. [安装和设置](#installation-and-setup)
2. [核心概念：内核、线程、块、网格](#core-concepts)
3. [编写 CUDA 内核](#writing-cuda-kernels)
4. [螺纹定位](#螺纹定位)
5. [内存管理](#内存管理)
6. [共享内存](#shared-memory)
7. [设备功能](#device-functions)
8. [原子操作](#atomic-operations)
9. [GPU Ufuncs：@vectorize 和 @guvectorize](#gpu-ufuncs)
10. [GPU 缩减](#gpu-reductions)
11. [流和异步操作](#streams)
12. [随机数生成](#random-number- Generation)
13. [合作团体](#cooperative-groups)
14. [科学计算的常见模式](#common-patterns)
15. [性能优化](#性能优化)
16. [调试](#debugging)
17. [互操作性](#互操作性)
18. [常见陷阱](#common-pitfalls)

- --

## 安装和设置

在所有安装说明、文档字符串、注释和错误中始终使用 `uv add`（切勿使用 `pip install` 或 `conda install`） messages.

```bash
uv add numba numba-cuda
```

`numba-cuda` 包是积极维护的 NVIDIA 实现。它在 `numba.cuda` 命名空间下实现功能 - 与旧的内置目标相比，无需更改代码。

* *要求：** CUDA 工具包 >= 11.2，计算能力 >= 5.0 的 GPU（Maxwell 或更新版本）。

```python
from numba import cuda

# Verify GPU is available
print(cuda.is_available())   # True if CUDA works
cuda.detect()                # Prints GPU details
```

- --

## 核心概念

CUDA 在层次结构中组织并行执行：

```
Grid (of blocks) → Blocks (of threads) → Threads
```

- **线程**：最小的执行单元。每个都运行您的内核函数。
- **块**：一组可以共享快速片上内存并相互同步的线程。每个块最多 1024 个线程。
- **Grid**：内核启动的所有块的集合。

A **kernel** 是一个在 GPU 上运行的函数，从 CPU 启动。 **设备函数**在 GPU 上运行，但从其他 GPU 代码（而不是从 CPU）调用。

- --

## 编写 CUDA 内核

### @cuda.jit 装饰器

```python
from numba import cuda

@cuda.jit
def my_kernel(input_array, output_array):
    i = cuda.grid(1)                    # Get this thread's global index
    if i < input_array.size:            # Bounds check — ALWAYS do this
        output_array[i] = input_array[i] * 2.0
```

* *@cuda.jit 的关键参数：**

|参数|用途|
|---------|---------|
| `device=True` |使其成为设备函数（只能从 GPU 调用，可以返回值）|
| `fastmath=True` |启用快速数学运算（float32 上的快速 sqrt、除法、FMA、trig/exp/log 近似）。当不需要 IEEE-754 严格性时使用 |
| `max_registers=N` |限制每个线程的寄存器以增加占用|
| `cache=True` |将编译后的内核缓存到磁盘|
| `debug=True` |启用异常检查（慢 - 仅用于调试，与 `opt=False` 配对）|
| `lineinfo=True` |用于分析的源行信息，无需完全调试开销 |

### 启动内核

```python
import numpy as np
from numba import cuda

data = np.random.rand(1_000_000).astype(np.float32)
out = np.zeros_like(data)

# Transfer to GPU
d_data = cuda.to_device(data)
d_out = cuda.device_array_like(out)

# Calculate launch configuration
threads_per_block = 256
blocks_per_grid = (data.size + threads_per_block - 1) // threads_per_block

# Launch
my_kernel[blocks_per_grid, threads_per_block](d_data, d_out)

# Get results back
result = d_out.copy_to_host()
```

* *启动语法：** `kernel[grid_dim, block_dim, stream, dynamic_shared_mem_bytes](...args)`

第 3 个和第 4 个参数是可选的（流和动态共享内存大小以字节为单位）。

### 2D启动配置

```python
@cuda.jit
def kernel_2d(matrix, output):
    x, y = cuda.grid(2)
    if x < matrix.shape[0] and y < matrix.shape[1]:
        output[x, y] = matrix[x, y] * 2.0

threads = (16, 16)
blocks = (
    (matrix.shape[0] + threads[0] - 1) // threads[0],
    (matrix.shape[1] + threads[1] - 1) // threads[1],
)
kernel_2d[blocks, threads](d_matrix, d_output)
```

### 方便：1D

```python
# Automatically computes grid dimensions for 1D
my_kernel.forall(len(data))(d_data, d_out)
```

### 内核的关键规则

1 的.forall()。 **内核不能返回值。** 所有输出必须写入作为参数传递的数组。
2. **始终检查数组边界。** 如果 grid_size > array_size，越界线程会默默地损坏内存。
3. **内核启动是异步的。** 在CPU上读取结果之前使用`cuda.synchronize()`。

- --

## 线程定位

### Intrinsics

|内在|描述|
|-----------|--------------|
| `cuda.threadIdx.x/y/z` |其块内的线程索引 |
| `cuda.blockIdx.x/y/z` |网格内的块索引 |
| `cuda.blockDim.x/y/z` |每块线程数|
| `cuda.gridDim.x/y/z` |网格中的块|
| `cuda.grid(ndim)` |整个网格中的绝对位置（1D→整数，2D/3D→元组）|
| `cuda.gridsize(ndim)` |整个网格中的线程总数 |

### Grid-Stride 循环模式

对于处理大于网格的数据，请使用 grid-stride 循环。这将网格大小与问题大小分离，对于重用 RNG 状态至关重要。

```python
@cuda.jit
def process_large(data, out):
    start = cuda.grid(1)
    stride = cuda.gridsize(1)
    for i in range(start, data.shape[0], stride):
        out[i] = data[i] * 2.0
```

- --

## 内存管理

### 数据传输

```python
# Host → Device
d_array = cuda.to_device(numpy_array)                    # Synchronous copy
d_array = cuda.to_device(numpy_array, stream=stream)     # Async copy

# Allocate on device (no copy)
d_array = cuda.device_array(shape=(1000,), dtype=np.float32)
d_array = cuda.device_array_like(numpy_array)

# Device → Host
host_array = d_array.copy_to_host()                      # New array
d_array.copy_to_host(existing_array)                     # Into pre-allocated
d_array.copy_to_host(stream=stream)                      # Async
```

### 内存类型

|类型 |应用程序接口 |使用案例 |
|-----|-----|----------|
| **设备** | `cuda.device_array()`、`cuda.to_device()` |标准GPU显存|
| **固定** | `cuda.pinned_array()`、`cuda.pinned()` 上下文管理器 |页锁定主机内存 — 更快的传输 |
| **映射** | `cuda.mapped_array()` |可从主机和设备|
|访问**管理** | `cuda.managed_array()` |统一内存 — 在主机/设备之间自动迁移（推荐 Linux/x86）|
| **常数** | `cuda.const.array_like(arr)` |只读、缓存、从主机设置 |

### 用于快速传输的固定内存

```python
# Allocate pinned host memory (page-locked — faster PCI-e transfers)
with cuda.pinned(host_array):
    d_array = cuda.to_device(host_array, stream=stream)
    # Transfer is faster because the OS can't page this memory out

# Or allocate directly
pinned = cuda.pinned_array(shape=(1000,), dtype=np.float32)
```

### 释放控制

```python
with cuda.defer_cleanup():
    # All GPU deallocation deferred here — avoids implicit synchronization
    # Use this in performance-critical sections
    run_many_kernels()
# Cleanup happens here
```

- --

## 共享内存

共享内存速度很快在块内共享片上存储器（数十 TB/s 带宽）。它是高性能内核的关键——用它来缓存块中多个线程将访问的数据。

### 静态共享内存（大小在编译时已知）

```python
from numba import cuda, float32

@cuda.jit
def kernel_with_shared(data, output):
    # Allocate shared memory — visible to all threads in this block
    shared = cuda.shared.array(256, dtype=float32)

    tid = cuda.threadIdx.x
    i = cuda.grid(1)

    # Each thread loads one element into shared memory
    if i < data.size:
        shared[tid] = data[i]

    # BARRIER: wait for ALL threads in block to finish loading
    cuda.syncthreads()

    # Now safe to read any element in shared[]
    if i < data.size and tid > 0:
        output[i] = shared[tid] + shared[tid - 1]
```

### 动态共享内存（大小设置为launch)

```python
@cuda.jit
def kernel_dynamic_shared(data):
    # size=0 means "use dynamic shared memory"
    dyn = cuda.shared.array(0, dtype=float32)
    tid = cuda.threadIdx.x
    dyn[tid] = data[cuda.grid(1)]
    cuda.syncthreads()
    # ...

# Specify size at launch (4th parameter = bytes)
kernel_dynamic_shared[blocks, threads, stream, 1024](data)  # 1024 bytes of shared mem
```

* *重要：**同一内核别名中的所有 `cuda.shared.array(0, ...)` 调用同一内存区域。要使用多个动态共享数组，请手动获取不相交的切片。

### 本地内存（每线程暂存器）

```python
@cuda.jit
def kernel_with_local(data):
    # Each thread gets its own private array
    local_buf = cuda.local.array(10, dtype=float32)
    i = cuda.grid(1)
    for j in range(10):
        local_buf[j] = data[i * 10 + j]
    # Process local_buf...
```

- --

## 设备函数

设备函数在GPU上运行，并从内核或其他设备函数中调用。与内核不同，它们**可以返回值**。

```python
@cuda.jit(device=True)
def compute_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

@cuda.jit
def kernel(points, distances):
    i = cuda.grid(1)
    if i < points.shape[0] - 1:
        distances[i] = compute_distance(
            points[i, 0], points[i, 1],
            points[i+1, 0], points[i+1, 1]
        )
```

* *交叉编译注意：**用`@numba.jit`（CPU JIT）装饰的函数也可以从CUDA内核调用 - 对于在CPU和GPU代码路径之间共享逻辑很有用。

- --

## 原子Operations

Atomics 确保共享数据的线程安全更新。全部返回**旧**值。

```python
cuda.atomic.add(array, index, value)       # +=   (int32, float32, float64)
cuda.atomic.sub(array, index, value)       # -=   (int32, float32, float64)
cuda.atomic.max(array, index, value)       # max  (int/uint 32/64, float 32/64)
cuda.atomic.min(array, index, value)       # min  (same types)
cuda.atomic.nanmax(array, index, value)    # max ignoring NaN
cuda.atomic.nanmin(array, index, value)    # min ignoring NaN
cuda.atomic.and_(array, index, value)      # &=   (int/uint 32/64)
cuda.atomic.or_(array, index, value)       # |=   (int/uint 32/64)
cuda.atomic.xor(array, index, value)       # ^=   (int/uint 32/64)
cuda.atomic.exch(array, index, value)      # exchange
cuda.atomic.cas(array, index, old, value)  # compare-and-swap
```

多维索引通过元组工作：`cuda.atomic.add(result, (row, col), value)`

### 示例：Histogram

```python
@cuda.jit
def histogram(data, bins):
    i = cuda.grid(1)
    if i < data.size:
        bin_idx = int(data[i] * len(bins))
        if 0 <= bin_idx < len(bins):
            cuda.atomic.add(bins, bin_idx, 1)
```

- --

## GPU Ufuncs

### @vectorize — GPU 上的逐元素运算

在 GPU 上运行逐元素运算的最简单方法。编写一个标量函数，Numba 自动在数组上广播它。

```python
from numba import vectorize, float32, float64
import math

@vectorize([float32(float32, float32),
            float64(float64, float64)],
           target='cuda')
def gpu_hypot(x, y):
    return math.sqrt(x**2 + y**2)

# Usage — just call it like a NumPy ufunc
result = gpu_hypot(array_x, array_y)

# Pass device arrays to avoid transfers
d_x = cuda.to_device(x)
d_y = cuda.to_device(y)
d_result = gpu_hypot(d_x, d_y)
```

### @guvectorize — 广义 Ufuncs

用于子数组（不仅仅是标量）上的操作。使用 NumPy 的广义 ufunc 签名。

```python
from numba import guvectorize, float32

@guvectorize([float32[:,:], float32[:,:], float32[:,:]],
             '(m,n),(n,p)->(m,p)', target='cuda')
def gpu_matmul(A, B, C):
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            total = 0.0
            for k in range(A.shape[1]):
                total += A[i, k] * B[k, j]
            C[i, j] = total
```

- --

## GPU 缩减

```python
from numba import cuda

# Define reduction operation
sum_reduce = cuda.reduce(lambda a, b: a + b)

# Use it
result = sum_reduce(array)                    # Full reduction
result = sum_reduce(array, init=0)            # With initial value
sum_reduce(array, res=device_result)          # Write to device array (no D→H copy)
sum_reduce(array, stream=stream)              # Async
```

自定义减少：

```python
@cuda.reduce
def max_reduce(a, b):
    return a if a > b else b

maximum = max_reduce(data_array)
```

- --

## Streams

Streams 启用数据传输的重叠计算并同时运行多个内核。

```python
stream = cuda.stream()

# Async transfer → kernel → transfer back
d_data = cuda.to_device(host_data, stream=stream)
my_kernel[blocks, threads, stream](d_data, d_out)
result = d_out.copy_to_host(stream=stream)
stream.synchronize()  # Wait for everything on this stream

# Context manager that auto-synchronizes
with stream.auto_synchronize():
    d_data = cuda.to_device(host_data, stream=stream)
    my_kernel[blocks, threads, stream](d_data, d_out)
    result = d_out.copy_to_host(stream=stream)
# Synchronizes here automatically
```

### 管道模式（重叠传输和计算）

```python
stream1 = cuda.stream()
stream2 = cuda.stream()

# Chunk 1: transfer on stream1
d_chunk1 = cuda.to_device(data[:half], stream=stream1)
# Chunk 2: transfer on stream2 (overlaps with stream1 transfer)
d_chunk2 = cuda.to_device(data[half:], stream=stream2)

# Process chunk1 on stream1
kernel[blocks, threads, stream1](d_chunk1, d_out1)
# Process chunk2 on stream2 (overlaps with stream1 compute)
kernel[blocks, threads, stream2](d_chunk2, d_out2)

cuda.synchronize()  # Wait for all streams
```

- --

## 随机数生成

Numba使用xoroshiro128+算法提供GPU原生随机数生成。

```python
from numba import cuda
from numba.cuda.random import (
    create_xoroshiro128p_states,
    xoroshiro128p_uniform_float32,
    xoroshiro128p_uniform_float64,
    xoroshiro128p_normal_float32,
    xoroshiro128p_normal_float64,
)

# Create RNG states — one per thread
n_threads = 256 * 128
rng_states = create_xoroshiro128p_states(n_threads, seed=42)

@cuda.jit
def monte_carlo_pi(rng_states, iterations, out):
    gid = cuda.grid(1)
    if gid < out.size:
        inside = 0
        for _ in range(iterations):
            x = xoroshiro128p_uniform_float32(rng_states, gid)
            y = xoroshiro128p_uniform_float32(rng_states, gid)
            if x**2 + y**2 <= 1.0:
                inside += 1
        out[gid] = inside / iterations * 4.0

monte_carlo_pi[128, 256](rng_states, 10000, d_out)
```

* *提示：** RNG状态消耗与线程成比例的内存计数。使用网格跨步循环来限制大问题所需的状态数量。

- --

## 协作组

用于需要在网格中的所有块之间同步（不仅仅是在单个块内）的算法。

```python
@cuda.jit
def iterative_kernel(M):
    col = cuda.grid(1)
    g = cuda.cg.this_grid()  # Get grid group

    for row in range(1, M.shape[0]):
        M[row, col] = M[row - 1, col] + 1
        g.sync()  # Global barrier — all blocks wait here

# Query max grid size for cooperative launch
overload = iterative_kernel.overloads[signature]
max_blocks = overload.max_cooperative_grid_blocks(block_dim)
```

当`g.sync()`为检测到。网格不得超过`max_cooperative_grid_blocks()`.

- --

## 常见图案

### 共享内存的平铺矩阵乘法

这是共享内存优化的典型示例 - A 和 B 的平铺加载到快速共享内存中以减少缓慢的全局内存访问。

```python
from numba import cuda, float32
import numpy as np

TPB = 16  # Tile/block size

@cuda.jit
def matmul_shared(A, B, C):
    sA = cuda.shared.array((TPB, TPB), dtype=float32)
    sB = cuda.shared.array((TPB, TPB), dtype=float32)

    x, y = cuda.grid(2)
    tx, ty = cuda.threadIdx.x, cuda.threadIdx.y

    tmp = float32(0.0)
    for tile in range(cuda.gridDim.x):
        # Load tile into shared memory (with bounds check)
        col = tx + tile * TPB
        row = ty + tile * TPB
        sA[ty, tx] = A[y, col] if (y < A.shape[0] and col < A.shape[1]) else 0
        sB[ty, tx] = B[row, x] if (x < B.shape[1] and row < B.shape[0]) else 0
        cuda.syncthreads()

        # Compute partial dot product from this tile
        for k in range(TPB):
            tmp += sA[ty, k] * sB[k, tx]
        cuda.syncthreads()

    if y < C.shape[0] and x < C.shape[1]:
        C[y, x] = tmp
```

### 并行前缀和（扫描）

```python
@cuda.jit
def inclusive_scan(data, output):
    shared = cuda.shared.array(256, dtype=float32)
    tid = cuda.threadIdx.x
    i = cuda.grid(1)

    shared[tid] = data[i] if i < data.size else 0
    cuda.syncthreads()

    # Up-sweep
    offset = 1
    while offset < cuda.blockDim.x:
        if tid >= offset:
            shared[tid] += shared[tid - offset]
        offset *= 2
        cuda.syncthreads()

    if i < data.size:
        output[i] = shared[tid]
```

### 共享内存减少

```python
@cuda.jit
def block_reduce_sum(data, partial_sums):
    shared = cuda.shared.array(256, dtype=float32)
    tid = cuda.threadIdx.x
    i = cuda.grid(1)

    shared[tid] = data[i] if i < data.size else 0.0
    cuda.syncthreads()

    # Tree reduction in shared memory
    s = cuda.blockDim.x // 2
    while s > 0:
        if tid < s:
            shared[tid] += shared[tid + s]
        s //= 2
        cuda.syncthreads()

    # Thread 0 of each block writes the block's sum
    if tid == 0:
        partial_sums[cuda.blockIdx.x] = shared[0]
```

### 模板/邻居访问模式

```python
@cuda.jit
def stencil_1d(data, output, radius):
    shared = cuda.shared.array(288, dtype=float32)  # blockDim + 2*radius
    tid = cuda.threadIdx.x
    i = cuda.grid(1)

    # Load center + halo into shared memory
    shared[tid + radius] = data[i] if i < data.size else 0
    if tid < radius:
        shared[tid] = data[i - radius] if i >= radius else 0
        shared[tid + cuda.blockDim.x + radius] = (
            data[i + cuda.blockDim.x] if i + cuda.blockDim.x < data.size else 0
        )
    cuda.syncthreads()

    if i < data.size:
        total = float32(0.0)
        for j in range(-radius, radius + 1):
            total += shared[tid + radius + j]
        output[i] = total / (2 * radius + 1)
```

- --

## 性能优化

### GPU 特定提示

1. **最大限度地减少主机设备传输。** 使用 `cuda.to_device()` 并跨多个内核调用将数据保留在 GPU 上。与 GPU 内存带宽（~900+ GB/s）相比，每次 PCI-e 传输都很昂贵（~12 GB/s）。

2. **使用共享内存**来存储块中跨线程重用的数据。共享内存带宽比全局内存高约 10-100 倍。

3. **合并内存访问。**相邻线程（连续的 `threadIdx.x`）应访问相邻的内存位置。这使得硬件可以将访问组合成更少的宽事务。

4. **选择占用的块大小。** 1D 为 128-256 线程/块，2D 为 (16,16)或 (32,32)。线程太少，GPU 利用率不足；太多可能会限制每个线程的寄存器/共享内存。

5. **当不需要 IEEE-754 严格性时，使用 `fastmath=True`**。为 float32.

6 启用 FMA、快速 sqrt/除法和更快的 trig/exp/log。 **在精度允许的情况下，优先选择 float32 而不是 float64**。 GPU float32 吞吐量要高出 2 倍到 32 倍，具体取决于 GPU（消费类 GPU 严重惩罚 float64）。

7. **使用流**将数据传输与计算重叠。

8. **在性能关键部分使用 `cuda.defer_cleanup()`** 来防止内存释放的隐式同步。

9. **当占用成为瓶颈时，使用 `max_registers` 参数限制寄存器使用**。

10. **使用网格步长循环**将网格大小与问题大小分离并提高灵活性。

### 不该做的事情

 - 不要在内核内部使用 Python 对象、字符串或动态内存分配 - Numba CUDA 支持受限的 Python 子集。
  - 不要将 `syncthreads()` 放在不同的分支内 - 如果块中的线程通过屏障采用不同的路径，则行为未定义（死锁或损坏）。
  - 不要在读取 CPU 上的结果之前忘记 `cuda.synchronize()` - 内核启动是异步的。
  - 不要启动数据大小很小的内核 - 内核启动开销 (~5-20us)在小型数组中占主导地位。

- --

## 调试

### CUDA 模拟器

在 CPU 上运行 CUDA 代码进行调试 - 支持内核内部的 `print()` 和 `pdb`。

```bash
export NUMBA_ENABLE_CUDASIM=1
python your_script.py
```

 模拟器一次运行一个块内核，每个 CUDA 线程生成一个线程。支持共享/本地/常量内存、原子和 `syncthreads()`.

### 调试特定线程

```python
@cuda.jit
def debug_kernel(data, out):
    i = cuda.grid(1)
    if cuda.threadIdx.x == 0 and cuda.blockIdx.x == 0:
        # Only thread (0,0) hits the debugger
        from pdb import set_trace; set_trace()
    if i < data.size:
        out[i] = data[i] * 2
```

### 设备上调试模式

```python
@cuda.jit(debug=True, opt=False)
def kernel_debug(data):
    # Enables CUDA exception checking — much slower but catches errors
    ...
```

- --

## 互操作性

Numba 支持 **CUDA 数组接口**（版本 3） - 任何公开 `__cuda_array_interface__` 的对象都可以通过零拷贝直接传递到 Numba 内核。

### CuPy

```python
import cupy as cp
from numba import cuda

@cuda.jit
def add_kernel(x, y, out):
    i = cuda.grid(1)
    if i < x.shape[0]:
        out[i] = x[i] + y[i]

# CuPy arrays work directly — zero copy
a = cp.arange(1000, dtype=cp.float32)
b = cp.ones(1000, dtype=cp.float32)
out = cp.zeros(1000, dtype=cp.float32)
add_kernel[4, 256](a, b, out)
```

### 使用 PyTorch

```python
import torch
from numba import cuda

t = torch.cuda.FloatTensor([1, 2, 3])
d_array = cuda.as_cuda_array(t)  # Zero-copy Numba view of PyTorch tensor
```

### 检查 GPU 阵列

```python
cuda.is_cuda_array(obj)       # True if obj has __cuda_array_interface__
cuda.as_cuda_array(obj)       # Wrap as Numba device array (zero copy)
```

* *兼容的库：** CuPy、PyTorch、 JAX、PyCUDA、RAPIDS（cuDF、cuML）、PyArrow、mpi4py、NVIDIA DALI。

- --

## 常见陷阱

1. **忘记边界检查。** 如果 `blocks * threads > array_size`，越界线程会默默地损坏内存。始终：`if i < array.size`.

2. **尝试从内核返回值。**内核无法返回 - 而是写入输出数组。返回值被默默丢弃。

3. **隐式同步传输。** 将主机 (NumPy)数组直接传递到内核会触发同步回拷。使用显式 `cuda.to_device()` / `copy_to_host()`.

4. **对于静态分配，共享内存大小必须是编译时常量**。使用动态共享内存（大小=0）来确定运行时的大小。

5. **动态共享内存别名。**同一内核中的所有 `cuda.shared.array(0, ...)` 共享相同的内存。手动切片多个阵列。

6. **发散分支中的 `syncthreads()`。** 块中的所有线程必须到达相同的 `syncthreads()` 调用。发散路径 → 未定义行为。

7. **原子操作类型限制。** `atomic.add` 支持 int32、float32、float64。位原子仅适用于整数类型。

8. **忘记 `cuda.synchronize()`。** 内核启动是异步的。在同步之前读取主机端结果会提供陈旧/不完整的数据。

9. **内核中不支持的 Python 功能。** 无动态分配、无 Python 对象、无字符串操作、无异常（除非调试模式）。坚持使用数字类型和 math.

10. **在消费类 GPU 上使用 float64。** 消费类 NVIDIA GPU (GeForce)严重限制了 float64 吞吐量（通常是 float32 的 1/32）。除非需要精度，否则使用 float32。
