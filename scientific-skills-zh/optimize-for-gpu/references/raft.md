# RAFT (pylibraft)参考

RAFT（可重用加速函数和工具）是用于机器学习和信息检索的 GPU 加速构建块的 RAPIDS 库。它提供了低级原语——稀疏特征求解器、设备内存管理、随机图生成和多 GPU 通信——而 cuML 和 cuGraph 等高级库都是基于这些原语构建的。当您需要这些基元时，可以直接使用 `pylibraft`，而无需使用完整的 ML 框架。

> **完整文档：** https://docs.rapids.ai/api/raft/stable/
> **注意：** 向量搜索和聚类算法已迁移到 [cuVS](https://github.com/rapidsai/cuvs)。使用cuVS进行最近邻搜索，而不是RAFT。

## 目录

1. [安装和设置](#installation-and-setup)
2. [核心概念](#core-concepts)
3. [设备内存管理](#device-memory-management)
4. [稀疏特征值问题](#sparse-eigenvalue-problems)
5. [随机图生成](#random-graph- Generation)
6. [带有 raft-dask 的多节点多 GPU](#multi-node-multi-gpu-with-raft-dask)
7. [互操作性](#互操作性)
8. [性能提示](#performance-tips)
9. [常见陷阱](#common-pitfalls)

- --

## 安装和设置

在所有安装说明、文档字符串、注释和错误中始终使用 `uv add`（切勿使用 `pip install` 或 `conda install`） messages.

```bash
# pylibraft (core library)
uv add --extra-index-url=https://pypi.nvidia.com pylibraft-cu12   # For CUDA 12.x

# raft-dask (multi-node multi-GPU support, optional)
uv add --extra-index-url=https://pypi.nvidia.com raft-dask-cu12   # For CUDA 12.x
```

Verify:
```python
import pylibraft
from pylibraft.common import DeviceResources
handle = DeviceResources()
handle.sync()
print("pylibraft is working")
```

- --

## 核心概念

### DeviceResources（CUDA资源句柄）

`DeviceResources`管理昂贵的资源CUDA 资源（流、流池、cuBLAS/cuSOLVER 的库句柄）。创建一个并在多个 RAFT 调用中重复使用它，以避免重复分配开销。

默认情况下，```python
from pylibraft.common import DeviceResources, Stream

# Default stream
handle = DeviceResources()

# Custom stream
stream = Stream()
handle = DeviceResources(stream)

# With a CuPy stream
import cupy
cupy_stream = cupy.cuda.Stream()
handle = DeviceResources(stream=cupy_stream.ptr)

# Always sync before reading results
handle.sync()
```

RAFT 函数是异步的 - 它们立即返回并在 GPU 上继续工作。在访问 CPU 上的输出数据之前，必须调用 `handle.sync()`。如果不传递 `handle`，RAFT 会在内部分配临时资源并在返回之前进行同步（方便，但重复调用会较慢）。

### Stream

A 围绕 `cudaStream_t` 的薄包装器，用于排序 GPU 操作：

```python
from pylibraft.common import Stream

stream = Stream()
stream.sync()                  # Synchronize all work on this stream
ptr = stream.get_ptr()         # Get the raw cudaStream_t pointer (uintptr_t)
```

- --

## 设备内存管理

### device_ndarray

`device_ndarray`是RAFT的轻量级GPU数组类型。它实现了 `__cuda_array_interface__`，使其可与 CuPy、Numba、PyTorch 和其他 GPU 库互操作。

```python
from pylibraft.common import device_ndarray
import numpy as np

# Allocate empty GPU array
gpu_arr = device_ndarray.empty((1000, 50), dtype=np.float32)

# From a NumPy array (copies data to GPU)
cpu_data = np.random.rand(1000, 50).astype(np.float32)
gpu_arr = device_ndarray(cpu_data)

# Back to NumPy (copies data to CPU)
result = gpu_arr.copy_to_host()

# Properties
print(gpu_arr.shape)          # (1000, 50)
print(gpu_arr.dtype)          # float32
print(gpu_arr.c_contiguous)   # True (row-major)
print(gpu_arr.f_contiguous)   # False
```

### 配置输出类型

您可以配置所有 RAFT 计算 API 以返回 CuPy 数组或 PyTorch 张量，而不是返回 CuPy 数组或 PyTorch 张量`device_ndarray`:

```python
import pylibraft.config

pylibraft.config.set_output_as("cupy")    # All APIs return cupy arrays
pylibraft.config.set_output_as("torch")   # All APIs return torch tensors

# Custom conversion
pylibraft.config.set_output_as(lambda arr: arr.copy_to_host())  # Return numpy
```

- --

## 稀疏特征值问题

### eigsh — 稀疏对称特征值分解

GPU 加速的 Lanczos 方法，用于查找特征值/特征向量大型稀疏对称矩阵。 `scipy.sparse.linalg.eigsh`.

```python
import cupy as cp
import cupyx.scipy.sparse as sp
from pylibraft.sparse.linalg import eigsh
from pylibraft.common import DeviceResources

# Create a sparse symmetric matrix (CSR format)
n = 10000
density = 0.01
A = sp.random(n, n, density=density, dtype=cp.float32, format='csr')
A = A + A.T  # Make symmetric

# Find 6 largest eigenvalues
handle = DeviceResources()
eigenvalues, eigenvectors = eigsh(A, k=6, which='LM', handle=handle)
handle.sync()

print(f"Eigenvalues shape: {eigenvalues.shape}")      # (6,)
print(f"Eigenvectors shape: {eigenvectors.shape}")     # (10000, 6)
```

* *参数：**
- `A` — 稀疏对称 CSR 矩阵 (`cupyx.scipy.sparse.csr_matrix`)
- `k` — 特征值数量计算（默认值：6）。必须是 `1 <= k < n`
- `which` — 哪些特征值：
  - `'LM'`：幅度最大（默认）
  - `'LA'`：最大代数
  - `'SA'`：最小algebraic
  - `'SM'`：幅度最小
- `v0` — 起始向量（可选，如果无则随机）
- `ncv` — Lanczos 向量的数量。必须为 `k + 1 < ncv < n`
- `maxiter` — 最大迭代次数
- `tol` — 收敛容差（0 = 机器精度）
- `seed` — 用于再现性的随机种子
- `handle` —可选配`DeviceResources`手柄

* *何时使用：** 谱方法（谱聚类、图划分、类似 PageRank 的计算）、稀疏数据的降维、大型稀疏哈密顿量的物理模拟、结构分析（振动模式）。

- --

## 随机图生成

### rmat — R-MAT 图生成

使用递归矩阵生成随机图(R-MAT)模型，通常用于对具有真实结构（幂律度分布、社区结构）的图算法进行基准测试。

```python
import cupy as cp
from pylibraft.random import rmat
from pylibraft.common import DeviceResources

n_edges = 100000
r_scale = 16          # log2 of source node count (2^16 = 65536 nodes)
c_scale = 16          # log2 of destination node count
theta_len = max(r_scale, c_scale) * 4

# Output: edge list as (src, dst) pairs
out = cp.empty((n_edges, 2), dtype=cp.int32)
# Probability distribution at each R-MAT level
theta = cp.random.random_sample(theta_len, dtype=cp.float32)

handle = DeviceResources()
rmat(out, theta, r_scale, c_scale, seed=42, handle=handle)
handle.sync()

print(f"Generated {n_edges} edges")
print(f"Edge list shape: {out.shape}")       # (100000, 2)
print(f"Sample edges:\n{out[:5].get()}")     # First 5 edges on CPU
```

* *何时使用：** 对图算法进行基准测试，生成合成社交/网络图，大规模测试图处理管道。

- --

## 多节点多 GPU raft-dask

`raft-dask` 提供了一个 `Comms` 类，用于管理 Dask 集群中工作线程之间的 NCCL 和 UCX 通信。这是 RAPIDS 中分布式 GPU 计算的基础。

```python
from dask_cuda import LocalCUDACluster
from dask.distributed import Client
from raft_dask.common import Comms, local_handle

# Set up a local multi-GPU Dask cluster
cluster = LocalCUDACluster()
client = Client(cluster)

def run_on_gpu(sessionId):
    handle = local_handle(sessionId)
    # Use handle with RAFT or cuML algorithms
    return "done"

# Initialize multi-GPU communication
comms = Comms(client=client)
comms.init()

# Submit work to each GPU worker
futures = [
    client.submit(run_on_gpu, comms.sessionId, workers=[w], pure=False)
    for w in comms.worker_addresses
]

# Wait for results
from dask.distributed import wait
wait(futures, timeout=60)

# Clean up
comms.destroy()
client.close()
cluster.close()
```

* *通信参数：**
- `comms_p2p` (bool) — 启用 UCX 点对点通信（默认值：False）。为需要直接 GPU 到 GPU 传输的算法启用。 
- `client` — Dask 分布式客户端
- `verbose` (bool) — 启用详细日志记录
- `streams_per_handle` (int) — 每个 CUDA 流的数量handle

- --

## 互操作性

RAFT 的 `device_ndarray` 实现了 `__cuda_array_interface__`，从而实现与其他 GPU 库的零拷贝共享：

```python
import cupy as cp
import torch
from pylibraft.common import device_ndarray

# pylibraft -> CuPy (zero-copy)
raft_arr = device_ndarray(np.random.rand(100).astype(np.float32))
cupy_arr = cp.asarray(raft_arr)

# pylibraft -> PyTorch (zero-copy)
torch_tensor = torch.as_tensor(raft_arr, device='cuda')

# CuPy -> pylibraft (pass directly — RAFT APIs accept __cuda_array_interface__)
cupy_data = cp.random.rand(100, 50, dtype=cp.float32)
# Can pass cupy_data directly to pylibraft functions like eigsh()

# pylibraft -> NumPy (copy)
numpy_arr = raft_arr.copy_to_host()
```

RAFT 函数接受任何实现 `__cuda_array_interface__` 的对象作为输入 — 您不需要先转换为`device_ndarray`。这意味着 CuPy 数组、Numba 设备数组、PyTorch CUDA 张量和 cuDF 列都可以直接工作。

- --

## 性能提示

1. **重用 DeviceResources。** 创建 `DeviceResources` 会分配 CUDA 库句柄（cuBLAS、cuSOLVER）。创建一次，传递给所有调用。

2. **批量同步。** RAFT 调用是异步的。在调用 `handle.sync()` 之前对多个操作进行排队，而不是在每个操作之后同步。

3. **使用 float32。** float32 的 GPU 吞吐量比 float64 高 2-32 倍。仅当精度需要时才使用 float64。

4. **预分配输出。** 许多 RAFT 函数接受 `out` 参数。预分配避免了重复的GPU内存分配。

5. **将数据保留在 GPU 上。** RAFT 通过 `__cuda_array_interface__` 与 CuPy、cuDF 和 cuML 进行互操作。在库之间直接传递 GPU 数组，而不是通过 CPU 往返。

- --

## 常见陷阱

- **忘记同步。** RAFT 操作是异步的。在不调用 `handle.sync()` 的情况下读取结果会给出未定义/陈旧的数据。如果省略 `handle` 参数，RAFT 会在内部同步（安全但速度较慢）。

- **使用 RAFT 进行向量搜索。**向量搜索（k-NN、IVFPQ、CAGRA 等）已迁移到 [cuVS](https://github.com/rapidsai/cuvs)。 RAFT 不再维护这些算法。

- **错误的稀疏格式。** `eigsh()` 需要 `cupyx.scipy.sparse.csr_matrix`。其他稀疏格式（COO、CSC）必须首先转换。

- **带有 eigsh 的非对称矩阵。** `eigsh` 仅适用于实数对称/埃尔米特矩阵。对于一般特征值问题，您需要不同的求解器。

- **dtype 不匹配。** RAFT 函数对 dtypes 很挑剔。显式使用 `float32` 或 `float64` — 不要依赖隐式转换。
