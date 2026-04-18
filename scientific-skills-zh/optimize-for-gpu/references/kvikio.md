# KvikIO 参考 — 高性能 GPU 文件 IO

KvikIO 是一个用于高性能文件 IO 的 Python 和 C++ 库。它提供了与 NVIDIA cuFile 的绑定，支持 GPUDirect Storage (GDS)——直接在存储和 GPU 内存之间读写数据，完全绕过 CPU 内存。当 GDS 不可用时，KvikIO 会优雅地回退到 POSIX IO，同时仍然无缝处理主机和设备数据。

KvikIO 是 RAPIDS 生态系统的一部分，并与 CuPy、cuDF、Numba 和其他 GPU 库进行互操作。

## 目录

1. [安装](#安装)
2. [何时使用 KvikIO](#when-to-use-kvikio)
3. [CuFile — 本地文件 IO](#cufile--local-file-io)
4. [远程文件 — S3、HTTP、WebHDFS](#remotefile--s3-http-webhdfs)
5. [Zarr 集成](#zarr-integration)
6. [内存映射文件](#内存映射文件)
7. [运行时设置](#runtime-settings)
8. [性能优化](#性能优化)
9. [互操作性](#互操作性)
10. [常见模式](#common-patterns)
11. [常见陷阱](#common-pitfalls)

- --

## 安装

```bash
# CUDA 12.x
uv add kvikio-cu12

# CUDA 13.x
uv add kvikio-cu13

# For Zarr support (optional)
uv add zarr
```

验证安装：

```python
import kvikio
# Check if GDS is available
import kvikio.cufile_driver
print(kvikio.cufile_driver.get("is_gds_available"))  # True if GDS is set up
```

- --

## 何时使用克维克IO

在以下情况下使用 KvikIO：
- **将大型二进制数据直接加载到 GPU** — 避免标准 `open()` 或 NumPy 的 `fromfile()` 所需的 CPU 内存复制
- **将 GPU 数组写入磁盘** — 直接从设备内存保存，无需先复制到主机
- **从远程存储读取（S3、HTTP、 WebHDFS）写入 GPU 内存** — 跳过主机内存分段步骤
- **在 GPU 上使用 Zarr 阵列** — GDSStore 后端将块直接读取到 CuPy 数组
- **IO 是瓶颈** — GDS 可以实现接近原始 NVMe 带宽（每个驱动器 6-7 GB/s），而标准 IO 则在 CPU 内存带宽上达到顶峰
- **重叠IO 和计算** — 非阻塞读/写让您可以通过 GPU 计算管道加载数据

KvikIO 不太适合以下情况：
- 数据很小 (< 1 MB) — 内核启动和 GDS 开销占主导地位
- 您正在读取结构化格式（CSV、Parquet、JSON） — 使用 cuDF，它有自己的优化读取器
- 您只需要主机内存 —标准Python IO更简单

- --

## CuFile — 本地文件 IO

`kvikio.CuFile` 是本地文件IO的主要接口。它取代了用于 GPU 工作负载的 Python `open()`。

### 基本用法

```python
import cupy as cp
import kvikio

# Write a GPU array to disk
a = cp.arange(1_000_000, dtype=cp.float32)
with kvikio.CuFile("data.bin", "w") as f:
    f.write(a)

# Read it back
b = cp.empty(1_000_000, dtype=cp.float32)
with kvikio.CuFile("data.bin", "r") as f:
    f.read(b)

assert cp.all(a == b)
```

### API 方法

|方法|封锁|描述 |
|--------|---------|------------|
| `read(buf, size, file_offset)` |是的 |读入设备或主机缓冲区|
| `write(buf, size, file_offset)` |是的 |从设备或主机缓冲区写入|
| `pread(buf, size, file_offset)` |没有 |非阻塞并行读取，返回`IOFuture` |
| `pwrite(buf, size, file_offset)` |没有 |非阻塞并行写入，返回`IOFuture` |
| `raw_read(buf, size, file_offset)` |是的 |低级单线程读取（仅限设备）|
| `raw_write(buf, size, file_offset)` |是的 |低级单线程写入（仅限设备）|
| `raw_read_async(buf, stream, size, file_offset)` |没有 | CUDA 流异步读取（仅限设备）|
| `raw_write_async(buf, stream, size, file_offset)` |没有 | CUDA 流异步写入（仅限设备）|

文件模式：`"r"`（读）、`"w"`（写/截断）、`"a"`（追加）、`"+"`（读+写）。

### 带有Futures的非阻塞IO

`pread`和`pwrite`拆分操作进入线程池中执行的任务并返回 `IOFuture`:

```python
import cupy as cp
import kvikio

data = cp.empty(10_000_000, dtype=cp.float32)

with kvikio.CuFile("data.bin", "r") as f:
    # Launch two non-blocking reads for different sections
    future1 = f.pread(data[:5_000_000])
    future2 = f.pread(data[5_000_000:], file_offset=5_000_000 * 4)

    # Do other work while IO happens...

    # Wait for completion
    bytes_read1 = future1.get()
    bytes_read2 = future2.get()
```

### 部分读取和写入

```python
import cupy as cp
import kvikio

# Read only a portion of a file
buf = cp.empty(1000, dtype=cp.float32)
with kvikio.CuFile("data.bin", "r") as f:
    # Read 1000 floats starting at byte offset 4000
    f.read(buf, size=4000, file_offset=4000)
```

### 主机内存支持

KvikIO 透明地处理主机内存 - 无需特殊 API需要：

```python
import numpy as np
import kvikio

# Write from host memory
a = np.arange(1_000_000, dtype=np.float32)
with kvikio.CuFile("data.bin", "w") as f:
    f.write(a)

# Read into host memory
b = np.empty_like(a)
with kvikio.CuFile("data.bin", "r") as f:
    f.read(b)
```

### GDS 对齐

GDS 最适合页面对齐 IO。 GPU页面大小为4 KiB（4096字节）：
- **文件偏移**：应该是4096
的倍数- **传输大小**：应该是4096

KvikIO正确处理未对齐的IO，但将其分为对齐和未对齐的部分，因此对齐的IO将是

- --

## RemoteFile — S3、HTTP、WebHDFS

`kvikio.RemoteFile` 将远程文件直接读取到 GPU 或主机内存中。

### HTTP/HTTPS

```python
import cupy as cp
import kvikio

buf = cp.empty(1_000_000, dtype=cp.float32)
with kvikio.RemoteFile.open_http("https://example.com/data.bin") as f:
    print(f.nbytes())  # File size
    f.read(buf)
```

### AWS S3

```python
import cupy as cp
import kvikio

# Using bucket + object name (requires AWS env vars or explicit credentials)
with kvikio.RemoteFile.open_s3("my-bucket", "data/file.bin") as f:
    buf = cp.empty(f.nbytes(), dtype=cp.uint8)
    f.read(buf)

# Using S3 URL
with kvikio.RemoteFile.open_s3_url("s3://my-bucket/data/file.bin") as f:
    buf = cp.empty(f.nbytes(), dtype=cp.uint8)
    f.read(buf)

# Public S3 (no credentials needed)
with kvikio.RemoteFile.open_s3_public("s3://public-bucket/data.bin") as f:
    buf = cp.empty(f.nbytes(), dtype=cp.uint8)
    f.read(buf)

# Presigned URL
with kvikio.RemoteFile.open_s3_presigned_url(presigned_url) as f:
    buf = cp.empty(f.nbytes(), dtype=cp.uint8)
    f.read(buf)
```

AWS 凭证来自环境变量（`AWS_DEFAULT_REGION`、`AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY`），或者可以作为关键字参数传递。

### 自动检测端点Type

```python
import kvikio

# KvikIO figures out the protocol from the URL
with kvikio.RemoteFile.open("s3://bucket/object") as f:
    ...

with kvikio.RemoteFile.open("https://example.com/file.bin") as f:
    ...
```

### WebHDFS

```python
import kvikio

with kvikio.RemoteFile.open_webhdfs("http://namenode:9870/path/to/file") as f:
    buf = cp.empty(f.nbytes(), dtype=cp.uint8)
    f.read(buf)
```

### 主机内存与 RemoteFile

RemoteFile 读入主机内存就像轻松：

```python
import numpy as np
import kvikio

with kvikio.RemoteFile.open_http("https://example.com/data.bin") as f:
    buf = np.empty(f.nbytes(), dtype=np.uint8)
    f.read(buf)
```

- --

## Zarr Integration

KvikIO 为 Zarr（版本 3.x）提供 GPU 存储后端。这使得可以通过 GDS 在 GPU 内存中直接读取和写入分块 N 维数组。

```python
import zarr
from kvikio.zarr import GDSStore

# Enable GPU support in Zarr
zarr.config.enable_gpu()

# Create a GDS-backed store
store = GDSStore(root="data.zarr")

# Create and write a Zarr array (data stays on GPU)
z = zarr.create_array(
    store=store,
    shape=(1000, 1000),
    chunks=(100, 100),
    dtype="float32",
    overwrite=True,
)

# Reading returns CuPy arrays
chunk = z[:100, :100]  # Returns cupy.ndarray
```

Zarr + KvikIO 对于以下用途很有用：
- 气候/天气数据（大型多维数组）
- 生物信息学（基因组数组）
- 使用的任何工作负载需要GPU处理的分块数组

除了kvikio之外还需要：`uv add zarr`。

- --

## 内存映射文件

`kvikio.mmap.Mmap`提供内存映射文件访问，同时支持主机和设备目的地：

```python
from kvikio.mmap import Mmap
import cupy as cp

# Map a file for reading
with Mmap("data.bin", flags="r") as m:
    print(m.file_size())

    # Sequential read into device memory
    buf = cp.empty(1000, dtype=cp.float32)
    m.read(buf, size=4000, offset=0)

    # Parallel read (returns IOFuture)
    future = m.pread(buf, size=4000, offset=0)
    future.get()
```

- --

## 运行时设置

KvikIO 行为通过环境变量或 `kvikio.defaults` API 进行控制。

### 关键设置

|设置|环境变量 |默认|说明 |
|---------|------------|---------|-------------|
|兼容模式| `KVIKIO_COMPAT_MODE` | `AUTO` | `ON`：仅限 POSIX，`OFF`：仅限 GDS，`AUTO`：尝试 GDS，回退 |
|线程池大小| `KVIKIO_NTHREADS` | 1 | `pread`/`pwrite` |
| IO线程数任务规模| `KVIKIO_TASK_SIZE` | 4 MiB |每个并行 IO 任务的最大大小 |
| GDS门槛| `KVIKIO_GDS_THRESHOLD` | 16 KiB |使用 GDS 的最小尺寸（较小的使用 POSIX）|
|反弹缓冲区大小 | `KVIKIO_BOUNCE_BUFFER_SIZE` | 16 MiB | 16 MiB每个线程的中间主机缓冲区大小 |
|直接IO读取| `KVIKIO_AUTO_DIRECT_IO_READ` |关闭 |机会性 O_DIRECT 读取 |
|直接IO写入| `KVIKIO_AUTO_DIRECT_IO_WRITE` |上 |用于写入的机会性 O_DIRECT |

### 编程配置

```python
import kvikio.defaults

# Query settings
print(kvikio.defaults.get("compat_mode"))
print(kvikio.defaults.get("num_threads"))

# Modify settings at runtime
kvikio.defaults.set({"num_threads": 16, "task_size": 8 * 1024 * 1024})

# Enable direct IO for reads
kvikio.defaults.set({"auto_direct_io_read": True})
```

### 兼容模式

当 GDS 不可用时（缺少 `libcufile.so`、在 WSL 中运行、没有 `/run/udev` 的 Docker）， `AUTO` 模式自动回退到 POSIX IO。这意味着 KvikIO 代码可以在任何地方工作 - 当 GDS 可用时它运行得更快。

```python
import kvikio.cufile_driver

# Check if GDS is actually being used
print(kvikio.cufile_driver.get("is_gds_available"))
```

### cuFile 驱动程序配置

```python
import kvikio.cufile_driver

# Query driver properties
print(kvikio.cufile_driver.get("is_gds_available"))
print(kvikio.cufile_driver.get("major_version"))

# Configure settable properties
kvikio.cufile_driver.set("max_device_cache_size", 1024)

# Use as context manager (auto-reverts on exit)
with kvikio.cufile_driver.set({"poll_mode": True}):
    # poll mode active here
    ...
# poll mode reverted
```

- --

## 性能优化

### 1. 增加线程池大小

默认1线程比较保守。对于大文件，增加它：

```python
import kvikio.defaults
kvikio.defaults.set({"num_threads": 16})
```

### 2. 使用非阻塞 IO 进行流水线

通过使用计算与计算重叠 IO `pread`/`pwrite`:

```python
import cupy as cp
import kvikio

# Pipeline: read chunk N while processing chunk N-1
chunk_size = 10_000_000
buf_a = cp.empty(chunk_size, dtype=cp.float32)
buf_b = cp.empty(chunk_size, dtype=cp.float32)

with kvikio.CuFile("large_data.bin", "r") as f:
    # Start first read
    future = f.pread(buf_a)
    future.get()

    for offset in range(chunk_size * 4, file_size, chunk_size * 4):
        # Start next read while processing current
        next_future = f.pread(buf_b, file_offset=offset)

        # Process buf_a on GPU (overlaps with IO)
        result = cp.fft.fft(buf_a)

        next_future.get()
        buf_a, buf_b = buf_b, buf_a  # Swap buffers
```

### 3. 将 IO 与页面边界对齐

GDS 在 4 KiB 对齐偏移量下性能最佳，并且大小：

```python
# Good: aligned offset and size
f.read(buf, size=4096 * 1000, file_offset=4096 * 10)

# Slower: unaligned (KvikIO handles it, but splits into aligned + unaligned parts)
f.read(buf, size=5000, file_offset=100)
```

### 4.启用 Direct IO

对于顺序写入和冷读取，Direct IO（绕过 OS 页缓存）可以提供帮助：

```python
import kvikio.defaults
kvikio.defaults.set({
    "auto_direct_io_read": True,
    "auto_direct_io_write": True,
})
```

### 5. 调整任务和反弹缓冲区大小

对于非常大的文件，增加任务和反弹缓冲区大小：

```python
import kvikio.defaults
kvikio.defaults.set({
    "task_size": 16 * 1024 * 1024,       # 16 MiB per task
    "bounce_buffer_size": 64 * 1024 * 1024,  # 64 MiB bounce buffer
})
```

### 6. 页面缓存实用程序

对于基准测试，清除页面缓存以测量冷读性能：

```python
import kvikio

# Check page cache residency
pages_cached, total_pages = kvikio.get_page_cache_info("data.bin")
print(f"{pages_cached}/{total_pages} pages in cache")

# Clear page cache (requires root or appropriate permissions)
kvikio.clear_page_cache()
```

- --

## 互操作性

### 使用 CuPy

KvikIO 直接读取 CuPy 数组 - 这是最常见的用法：

```python
import cupy as cp
import kvikio

data = cp.empty(1_000_000, dtype=cp.float64)
with kvikio.CuFile("data.bin", "r") as f:
    f.read(data)
# data is now a CuPy array, ready for GPU computation
```

### 使用 Numba CUDA

KvikIO 可与支持 CUDA 数组接口的任何缓冲区配合使用：

```python
from numba import cuda
import kvikio

d_arr = cuda.device_array(1_000_000, dtype="float32")
with kvikio.CuFile("data.bin", "r") as f:
    f.read(d_arr)
```

### 与 cuDF

对于不是表格格式的原始二进制数据，请使用 KvikIO 加载，然后转换：

```python
import cupy as cp
import cudf
import kvikio

# Load raw float array, wrap as cuDF Series
buf = cp.empty(1_000_000, dtype=cp.float32)
with kvikio.CuFile("signal.bin", "r") as f:
    f.read(buf)
signal = cudf.Series(buf)
```

对于表格格式（CSV、Parquet、JSON、ORC），请使用 cuDF 自己的阅读器 - 它们针对这些格式进行了优化。

### 使用 NumPy（主机内存）

KvikIO 无缝处理主机内存：

```python
import numpy as np
import kvikio

arr = np.empty(1_000_000, dtype=np.float32)
with kvikio.CuFile("data.bin", "r") as f:
    f.read(arr)
```

- --

## 常见模式

### 保存和加载GPU模型检查点

```python
import cupy as cp
import kvikio

def save_checkpoint(arrays: dict[str, cp.ndarray], path: str):
    """Save multiple GPU arrays to a single file."""
    with kvikio.CuFile(path, "w") as f:
        offset = 0
        for arr in arrays.values():
            f.write(arr, file_offset=offset)
            offset += arr.nbytes

def load_checkpoint(shapes_dtypes: dict, path: str) -> dict[str, cp.ndarray]:
    """Load GPU arrays from a checkpoint file."""
    arrays = {}
    with kvikio.CuFile(path, "r") as f:
        offset = 0
        for name, (shape, dtype) in shapes_dtypes.items():
            arr = cp.empty(shape, dtype=dtype)
            f.read(arr, file_offset=offset)
            offset += arr.nbytes
            arrays[name] = arr
    return arrays
```

### 将数据从S3流式传输到GPU中处理

```python
import cupy as cp
import kvikio

with kvikio.RemoteFile.open_s3("my-bucket", "large-dataset.bin") as f:
    total_bytes = f.nbytes()
    chunk_size = 100 * 1024 * 1024  # 100 MB chunks
    buf = cp.empty(chunk_size // 4, dtype=cp.float32)

    for offset in range(0, total_bytes, chunk_size):
        size = min(chunk_size, total_bytes - offset)
        f.read(buf[:size // 4], size=size, file_offset=offset)
        # Process chunk on GPU
        result = cp.mean(buf[:size // 4])
```

### 为GPU 工作负载替换Python open()

```python
# Before: CPU-bound file IO
import numpy as np
data = np.fromfile("data.bin", dtype=np.float32)
import cupy as cp
gpu_data = cp.asarray(data)  # Extra copy: disk → CPU → GPU

# After: Direct to GPU
import cupy as cp
import kvikio
gpu_data = cp.empty(1_000_000, dtype=cp.float32)
with kvikio.CuFile("data.bin", "r") as f:
    f.read(gpu_data)  # disk → GPU directly (with GDS)
```

- --

## 常见陷阱

1. **忘记设置线程池大小** — 默认为 1 个线程。对于大文件，`kvikio.defaults.set({"num_threads": 16})`可以显着提高吞吐量。

2. **将 KvikIO 用于结构化格式** — 不要使用 KvikIO 读取 CSV/Parquet/JSON。使用`cudf.read_csv()`、`cudf.read_parquet()`等。KvikIO用于原始二进制数据。

3. **不检查 GDS 可用性** — 代码在没有 GDS 的情况下可以正常工作（回退到 POSIX），但不会获得全部带宽优势。检查`kvikio.cufile_driver.get("is_gds_available")`.

4. **性能关键路径中的未对齐 IO** — 使用 4 KiB 对齐的偏移量和大小以获得最佳 GDS 性能。

5. **不使用上下文管理器** — 始终使用 `with kvikio.CuFile(...)` 以确保文件正确关闭和取消注册。

6. **预期 RemoteFile 写入** — `RemoteFile` 是只读的。要写入远程存储，请先在本地写入，然后通过相应的 SDK（S3 的 boto3 等）上传。

7. **没有 GDS 设置的 Docker** — 在 Docker 中，以只读方式挂载 `/run/udev` (`--volume /run/udev:/run/udev:ro`)以使 GDS 正常工作。否则，KvikIO 会默默地回退到 POSIX.
