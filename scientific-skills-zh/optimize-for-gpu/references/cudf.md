# cuDF Reference

cuDF 是一个 GPU DataFrame 库，它提供了一个类似 pandas 的 API，用于完全在 GPU 上加载、连接、聚合、过滤和操作表格数据。它是 NVIDIA RAPIDS 生态系统的一部分，基于 Apache Arrow 列式内存格式构建。

> **完整文档：** https://docs.rapids.ai/api/cudf/stable/

## 目录

1. [安装和设置](#installation-and-setup)
2. [两种使用模式](#two-usage-modes)
3. [cudf.pandas加速器模式](#cudfpandas-accelerator-mode)
4. [核心API：DataFrame和系列](#core-api)
5. [IO操作](#io-操作)
6. [分组操作](#groupby-操作)
7. [字符串操作](#string-operations)
8. [用户定义函数 (UDF)](#user-definition-functions)
9. [缺失数据处理](#missing-data-handling)
10. [数据类型](#data-types)
11. [内存管理](#内存管理)
12. [互操作性](#互操作性)
13. [带有 Dask-cuDF 的多 GPU](#multi-gpu-with-dask-cudf)
14. [性能优化](#性能优化)
15. [与 pandas 的主要区别](#key-differences-from-pandas)
16. [常见迁移模式](#common-migration-patterns)

- --

## 安装和设置

在所有安装说明、文档字符串、注释和错误中始终使用 `uv add`（切勿使用 `pip install` 或 `conda install`） messages.

```bash
uv add --extra-index-url=https://pypi.nvidia.com cudf-cu12    # For CUDA 12.x
```

Verify:
```python
import cudf
print(cudf.Series([1, 2, 3]))  # Should print a GPU series
```

- --

## 两种使用模式

cuDF提供了两种加速pandas代码的方法：

### 1. cudf.pandas （零代码更改）
自动加速 pandas 的直接替换。对于不支持的操作，回退到 CPU。最适合：快速加速现有代码、混合代码库、原型设计。

### 2.直接cuDF API
将`import pandas`替换为`import cudf`。最大性能，无代理开销，但需要使代码适应 cuDF 的 API（与 pandas 有一些行为差异）。最适合：生产管道、最高性能、新的 GPU 优先代码。

- --

## cudf.pandas 加速器模式

从 pandas 到 GPU 的最快路径 — 无需更改代码。

### 激活

```python
# Jupyter/IPython (MUST be before any pandas import)
%load_ext cudf.pandas
import pandas as pd  # Now GPU-accelerated

# Command line
# python -m cudf.pandas your_script.py
# python -m cudf.pandas --profile your_script.py  # With profiling

# Programmatic
import cudf.pandas
cudf.pandas.install()
import pandas as pd  # Now GPU-accelerated
```

* *关键：** 如果 pandas 已导入在会话中，您必须重新启动内核/进程。

### 工作原理

- `import pandas` 返回包装 cuDF 和 pandas 的代理模块。
- 首先在 GPU (cuDF)上尝试每个操作。如果失败，它会自动回退到 CPU (pandas)。
- 仅在必要时才在 GPU 和 CPU 之间进行数据传输。
- 默认情况下使用托管内存 — 可以处理大于 GPU 内存的数据集。
- 目前通过了 **93% 的 pandas 187,000 多个单元测试**。

### 分析 GPU 与 CPU执行

```python
%%cudf.pandas.profile        # Shows GPU vs CPU operation breakdown per cell
%%cudf.pandas.line_profile   # Per-line GPU/CPU timing
```

### 访问底层对象

```python
proxy_df.as_gpu_object()  # Get the cuDF DataFrame directly
proxy_df.as_cpu_object()  # Get the pandas DataFrame directly
```

注意：提取底层对象后，自动回退将停止工作。

### 兼容的第三方库
cuGraph、cuML、 Hvplot、Holoview、Ibis、NumPy、Matplotlib、Plotly、PyTorch、Seaborn、Scikit-Learn、SciPy、TensorFlow、XGBoost.

* *不兼容：** Joblib。对于分布式工作，请改用 Dask-cuDF。

### 限制

- 连接操作不能保证 pandas 的行排序（为了性能）。
- 不能在同一会话中将 `import cudf` 与 cudf.pandas 一起使用。
- Pickled 对象在常规 pandas 和cudf.pandas.
- 代理数组子类 `numpy.ndarray`，这可能会导致急切的设备到主机传输。
- 强制仅使用 CPU：设置 `CUDF_PANDAS_FALLBACK_MODE=1`.

- --

## 核心 API

### 创建 DataFrames 和系列

```python
import cudf

# From dict
df = cudf.DataFrame({"a": [1, 2, 3], "b": [4.0, 5.0, 6.0], "c": ["x", "y", "z"]})

# From pandas
import pandas as pd
gdf = cudf.DataFrame.from_pandas(pd.DataFrame({"a": [1, 2, 3]}))
# or
gdf = cudf.DataFrame(pandas_df)

# Series
s = cudf.Series([1, 2, 3, None, 5])

# Back to pandas
pdf = gdf.to_pandas()
```

### 常用操作（与pandas相同）

```python
df.head(10)
df.tail(5)
df.describe()
df.info()
df.dtypes
df.columns
df.shape

# Selection
df["a"]                     # Column → Series
df[["a", "b"]]             # Multiple columns → DataFrame
df.loc[2:5, ["a", "b"]]   # Label-based indexing
df.iloc[0:3]               # Integer-based indexing

# Filtering
df[df["a"] > 2]
df.query("a > 2 and b < 6")  # Supports @var for local variables

# Sorting
df.sort_values("a", ascending=False)
df.sort_index()

# Missing data
df.fillna(0)
df.dropna()
df.isna()

# Aggregations
df["a"].sum()
df["a"].mean()
df["a"].std()
df["a"].value_counts()

# Transforms
df["a"].clip(lower=1, upper=5)
df["a"].apply(lambda x: x * 2)  # JIT-compiled

# Combining
cudf.concat([df1, df2])
df1.merge(df2, on="key")
df1.merge(df2, on="key", how="left")  # left, right, inner, outer

# Arrow interop (zero-copy)
arrow_table = df.to_arrow()
df = cudf.DataFrame.from_arrow(arrow_table)
```

- --

## IO 操作

GPU 加速的文件读取和写入 — 对于大文件，通常比 pandas 快得多。

### Parquet（建议提高性能）

```python
# Read
df = cudf.read_parquet("data.parquet")
df = cudf.read_parquet("data.parquet", columns=["a", "b"])  # Read only specific columns

# Write
df.to_parquet("output.parquet")

# Metadata inspection (without loading data)
cudf.io.parquet.read_parquet_metadata("data.parquet")

# Incremental writing
writer = cudf.io.parquet.ParquetDatasetWriter("output_dir/", partition_cols=["year"])
writer.write_table(df)
writer.close()
```

### CSV

```python
df = cudf.read_csv("data.csv")
df = cudf.read_csv("data.csv", usecols=["a", "b"], dtype={"a": "int32"})
df.to_csv("output.csv", index=False)
```

### JSON

```python
df = cudf.read_json("data.json")
df = cudf.read_json("data.json", lines=True)  # JSON Lines format
df.to_json("output.json")
```

### ORC

```python
df = cudf.read_orc("data.orc")
df.to_orc("output.orc")
```

### 其他格式

|格式|阅读 |写| GPU 加速 |
|--------|------|--------|-----------------|
|阿夫罗 | `cudf.read_avro()` |不适用 |是（只读）|
|文字| `cudf.read_text()` |不适用 |是（只读）|
| HDF5 | `cudf.read_hdf()` | `df.to_hdf()` |否（使用 pandas）|
|羽毛| `cudf.read_feather()` | `df.to_feather()` |否（使用 pandas）|

* *首选 Parquet 而不是 CSV** — 柱状格式在 GPU 上读取速度更快，支持谓词下推，并且压缩效果良好。

- --

## GroupBy 操作

### 基本 GroupBy

```python
df.groupby("category").sum()
df.groupby(["category", "subcategory"]).mean()
df.groupby("category").agg({"value": "sum", "count": "max"})
df.groupby("category").agg({"value": ["sum", "min", "max"], "count": "mean"})
```

### 支持聚合

* *通用：** `count`、`size`、`nunique`、`nth`、`collect`、`unique`
* *数字：** `sum`、 `mean`、`var`、`std`、`median`、`idxmin`、`idxmax`、`min`、`max`、`quantile`
* *专业：** `corr`、`cov`

### GroupBy Transform

```python
df.groupby("category").transform("max")  # Broadcasts result to match group size
```

### GroupBy Apply

```python
df.groupby("category").apply(lambda x: x.max() - x.min())
```

* *警告：** Apply 按组顺序运行该函数 — 对于许多小数据来说可能会很慢组。尽可能使用矢量化聚合。

### JIT-Compiled GroupBy（用户定义聚合）

```python
def custom_agg(df):
    return df["value"].max() - df["value"].min() / 2

result = df.groupby("category").apply(custom_agg, engine="jit")
```

JIT 限制：无空值，仅 int32/64 和 float32/64，无法返回新列。

### 重要：排序Behaviour

cuDF 默认使用 `sort=False` （与默认排序的 pandas 不同）。要匹配 pandas：
```python
df.groupby("category", sort=True).sum()
# Or globally:
cudf.set_option("mode.pandas_compatible", True)
```

- --

## 字符串操作

cuDF 通过 `.str` 访问器提供 GPU 加速的字符串操作 - 与pandas.

```python
s = cudf.Series(["Hello World", "foo bar", "RAPIDS GPU", None])

# Case
s.str.lower()
s.str.upper()
s.str.title()
s.str.capitalize()

# Pattern matching
s.str.contains("World")
s.str.startswith("Hello")
s.str.endswith("GPU")
s.str.match(r"^[A-Z]")

# Extraction and replacement
s.str.extract(r"(\w+)\s(\w+)")
s.str.replace("World", "GPU")
s.str.slice(0, 5)

# Splitting and joining
s.str.split(" ")
s.str.cat(sep=", ")

# Info
s.str.len()
s.str.isalpha()
s.str.isdigit()

# cuDF-exclusive operations (not in pandas)
s.str.normalize_spaces()   # Collapse whitespace
s.str.tokenize()           # Tokenize strings
s.str.ngrams(2)            # Generate n-grams
s.str.edit_distance(other) # Levenshtein distance
s.str.url_encode()
s.str.url_decode()
```

- --

## 用户定义函数

### Series.apply() — JIT 编译

```python
s = cudf.Series([1, 2, 3, 4, 5])

def square_plus_one(x):
    return x ** 2 + 1

s.apply(square_plus_one)  # Compiled to GPU kernel via Numba
```

With 参数：
```python
def add_constant(x, c):
    return x + c

s.apply(add_constant, args=(42,))
```

### DataFrame.apply() — 逐行(axis=1)

```python
def row_func(row):
    return row["a"] + row["b"] * 2

df.apply(row_func, axis=1)  # Access columns by name via dict-like syntax
```

### UDF 中的空值处理

空值自动传播：
```python
s = cudf.Series([1, cudf.NA, 3])
def f(x):
    return x + 1
s.apply(f)  # Returns [2, <NA>, 4]
```

 显式空值检查：
```python
def f(x):
    if x is cudf.NA:
        return 0
    return x + 1
```

### 字符串UDFs

UDF 内的字符串操作支持：`==`、`!=`、`>=`、`<=`、`startswith()`、`endswith()`、`find()`、`rfind()`、 `count()`、`in`、`strip/lstrip/rstrip()`、`upper/lower()`、`replace()`、`+`（串联）、`len()`、布尔检查。

对于创建中间字符串的字符串 UDF，分配堆：
```python
from cudf.core.udf.utils import set_malloc_heap_size
set_malloc_heap_size(int(2e9))  # 2 GB
```

### 滚动窗口 UDFs

```python
import math

s = cudf.Series([16, 25, 36, 49, 64, 81], dtype="float64")

def max_sqrt(window):
    result = 0
    for val in window:
        result = max(result, math.sqrt(val))
    return result

s.rolling(window=3, min_periods=3).apply(max_sqrt)
```

* *限制：** 滚动 UDF 不支持空值。

### cuDF 上的自定义 Numba CUDA 内核列

为了获得最大程度的控制，请编写直接在cuDF列上操作的CUDA内核：

```python
from numba import cuda

@cuda.jit
def gpu_multiply(in_col, out_col, multiplier):
    i = cuda.grid(1)
    if i < in_col.size:
        out_col[i] = in_col[i] * multiplier

df["result"] = 0.0
gpu_multiply.forall(len(df))(df["a"], df["result"], 10.0)
```

### UDF限制

- 仅数字非十进制类型具有完全支持；字符串具有部分支持。
- 不支持 `**kwargs`。
- UDF 中未实现按位操作。
- GroupBy JIT：无空值，仅 int32/64 和 float32/64，无法返回新列。
- 滚动 UDF：无空值support.

- --

## 缺失数据处理

- 缺失值是 `<NA>`（不是 NaN）- cuDF 使用单独的 null 掩码，而不是 NaN 标记。
- 所有 dtypes 都是可以为 null 的（包括整数 - 对于缺失的 int 没有浮点强制）。
- 插入整数列的 `np.nan` 变为 `<NA>`，无需转换为浮点数。

```python
s = cudf.Series([1, None, 3, None, 5])

s.isna()                # Boolean mask
s.notna()
s.fillna(0)             # Fill with scalar
s.fillna({"a": 0, "b": 1})  # Fill with dict (per-column)
s.dropna()

# Aggregations skip NA by default
s.sum()                 # skipna=True (default)
s.sum(skipna=False)     # Propagates NA

# GroupBy excludes NA groups by default
df.groupby("a", dropna=False).sum()  # Include NA groups
```

- --

## 数据类型

|类别 |类型 |
|----------|--------|
|整数 | `int8`、`int16`、`int32`、`int64`、`uint32`、`uint64` |
|浮动| `float32`、`float64` |
|日期时间 | `datetime64[s/ms/us/ns]` |
|时间三角洲 | `timedelta[s/ms/us/ns]` |
|分类| `CategoricalDtype` |
|字符串| `object` / `string` |
|十进制| `Decimal32Dtype`、`Decimal64Dtype`、`Decimal128Dtype` |
|列表 | `ListDtype`（嵌套列表）|
|结构| `StructDtype`（类似字典）|

所有类型均可为空。列表列具有 `.list` 访问器（`get()`、`len()`、`contains()`、`sort_values()`、`unique()`、`concat()`）。结构列有一个 `.struct` 访问器（`field()`、`explode()`）。

* *没有用于任意 Python 对象的 `object` dtype** — `object` dtype 仅存储字符串。

- --

## 内存管理

### RMM（RAPIDS Memory Manager）

cuDF使用RMM进行GPU内存分配。根据您的工作负载进行配置：

```python
import rmm

# Pool allocator (recommended for production — avoids per-allocation cudaMalloc overhead)
pool = rmm.mr.PoolMemoryResource(
    rmm.mr.CudaMemoryResource(),
    initial_pool_size="1GiB",
    maximum_pool_size="4GiB"
)
rmm.mr.set_current_device_resource(pool)

# Managed memory (allows datasets larger than GPU memory)
rmm.mr.set_current_device_resource(rmm.mr.ManagedMemoryResource())

# Managed + pool (best of both)
pool = rmm.mr.PoolMemoryResource(
    rmm.mr.ManagedMemoryResource(),
    initial_pool_size="1GiB"
)
rmm.mr.set_current_device_resource(pool)
```

### 将 CuPy 和 Numba 与 RMM

结合使用 cuDF 与 CuPy 或 Numba 时，对齐同一分配器上的所有库以避免内存碎片：

```python
# CuPy
from rmm.allocators.cupy import rmm_cupy_allocator
import cupy
cupy.cuda.set_allocator(rmm_cupy_allocator)

# Numba
from rmm.allocators.numba import RMMNumbaManager
from numba import cuda
cuda.set_memory_manager(RMMNumbaManager)
```

### Copy-on-Write

```python
cudf.set_option("copy_on_write", True)
# or: export CUDF_COPY_ON_WRITE=1
```

Slices、`.head()`、浅拷贝和视图生成方法共享内存，直到其中之一被修改。显着减少具有许多派生 DataFrame 的工作流程的内存使用量。

### 内存分析

```python
rmm.statistics.enable_statistics()
stats = rmm.statistics.get_statistics()
# Returns: current_bytes, current_count, peak_bytes, peak_count, total_bytes, total_count
```

- --

## 互操作性

### CuPy （零拷贝）

```python
import cupy as cp

# cuDF → CuPy
arr = df.to_cupy()             # DataFrame → 2D CuPy array
arr = cp.asarray(df["col"])    # Series → 1D CuPy array
arr = df["col"].values         # Series → 1D CuPy array

# CuPy → cuDF
df = cudf.DataFrame(cupy_2d_array)
s = cudf.Series(cupy_1d_array)

# Via DLPack
df = cudf.from_dlpack(cupy_array.__dlpack__())
```

### 箭头（零拷贝）

```python
arrow_table = df.to_arrow()
df = cudf.DataFrame.from_arrow(arrow_table)
```

### RAPIDS Ecosystem

- **cuML:** 直接接受 cuDF DataFrames 用于 ML pipelines.
- **cuGraph：** 接受 cuDF 数据帧进行图形分析。
- **Dask-cuDF：** 分布式 GPU 数据帧（见下文）。

### CUDA 阵列接口

cuDF 系列公开 `__cuda_array_interface__`，用于与任何兼容库（CuPy、Numba、PyTorch 等）进行零拷贝共享。

- --

## 带有 Dask-cuDF

的多 GPU 适用于大于单个 GPU 内存的数据集，或多 GPU并行性：

```python
import dask_cudf
from dask.distributed import Client
from dask_cuda import LocalCUDACluster

# One worker per GPU
cluster = LocalCUDACluster()
client = Client(cluster)

# From files
ddf = dask_cudf.read_csv("path/*.csv")
ddf = dask_cudf.read_parquet("path/")

# From cuDF DataFrame
ddf = dask_cudf.from_cudf(df, npartitions=16)

# Operations (lazy — call .compute() to execute)
result = ddf.groupby("a").sum().compute()

# Persist in GPU memory for repeated access
ddf = ddf.persist()
```

 与cuDF的主要区别：不支持`.iloc`，必须调用`.compute()`来实现，未实现转置。

- --

## 性能优化

1. **从 cudf.pandas 开始**最容易采用 - 零代码更改、自动 GPU/CPU 回退。

2. **切换到直接 cuDF API 以获得最大性能** — 避免代理开销和回退复制成本。

3. **优先选择 Parquet 而不是 CSV** — 柱状格式、更快的 GPU 读取、谓词下推、更好的压缩。

4. **通过 RMM 使用池分配器** — 避免每次分配 `cudaMalloc` 开销。

5. **启用写时复制** — `cudf.set_option("copy_on_write", True)` 减少切片和视图的内存。

6. **将数据整形为长**（更多行，更少列）- GPU 在行上并行。

7. **从不迭代** — 仅使用矢量化运算。 `for row in df.iterrows()`违背了GPU加速的目的。

8. **最小数据集大小：** GPU 可以处理 **10,000-100,000+ 行**。较小的数据集在 CPU.

9 上可能会更快。 **使用向量化字符串操作**（`.str.` 访问器）而不是按行字符串 UDFs.

10. **使用 CuPy 进行逐行数学**，cuDF 本身不支持。

11. **使用 Numba CUDA 内核**进行复杂的逐元素操作。

12. **在同一 RMM 分配器上对齐所有 RAPIDS 库**以避免内存碎片。

13. **对于分布式工作负载**，使用 Dask-cuDF 和 `persist()` 将数据保存在 GPU 内存上。

- --

## 与 pandas

1 的主要区别。默认情况下，**结果排序是不确定的**（groupby、连接等）。使用`sort=True`或`cudf.set_option("mode.pandas_compatible", True)`.

2. **所有类型均可为 null。** 缺失值为 `<NA>`，而不是 NaN。缺少值的整数列保持整数（无浮点强制）。

3. **无迭代。** 不支持 `for val in series`。如果必须迭代，请先转换为pandas。

4. **需要唯一的列名称。**没有重复的列名称。

5. **没有任意Python对象。** `object` dtype仅存储字符串。

6. **`.apply()` 使用 Numba JIT。** UDF 内部仅支持 Python 的子集 — 没有任意 Python 对象，没有外部库调用。

7. **由于 GPU 并行操作顺序不同，浮点结果可能略有不同**。使用基于公差的比较。

8. **GroupBy 默认为 `sort=False`**（pandas 默认为 `sort=True`）.

9. **没有 ExtensionDtype 支持** from pandas.

- --

## 常见迁移模式

### 模式 1：零努力 (cudf.pandas)
```python
%load_ext cudf.pandas
import pandas as pd
# Everything else stays exactly the same
```

### 模式 2：直接导入Swap
```python
# Before
import pandas as pd
df = pd.read_csv("data.csv")
result = df.groupby("col").mean()

# After
import cudf
df = cudf.read_csv("data.csv")
result = df.groupby("col").mean()
```

### 模式 3：用矢量化 Ops 替换迭代
```python
# Before (pandas — slow even on CPU)
for idx, row in df.iterrows():
    df.at[idx, "c"] = row["a"] + row["b"]

# After (cuDF)
df["c"] = df["a"] + df["b"]
```

### 模式 4：用 Vectorized
```python
# Before
df["result"] = df.apply(lambda row: row["a"] ** 2 + row["b"], axis=1)

# After (vectorized — much faster)
df["result"] = df["a"] ** 2 + df["b"]
```

### 模式替换 apply() 5：GPU 处理，CPU 位于边界
```python
# Load and process on GPU
gdf = cudf.read_parquet("data.parquet")
result = gdf.groupby("key").agg({"val": "sum"})

# Convert to pandas only when needed (plotting, export, etc.)
pdf = result.to_pandas()
pdf.plot()
```

### 模式 6：CuPy 用于不支持的数学
```python
import cupy as cp

# Convert to CuPy for operations cuDF doesn't support
arr = df[["x", "y", "z"]].to_cupy()
norms = cp.linalg.norm(arr, axis=1)
df["norm"] = cudf.Series(norms)
```

- --

## 配置

```python
cudf.set_option("copy_on_write", True)            # Enable copy-on-write
cudf.set_option("mode.pandas_compatible", True)    # Match pandas behavior
cudf.describe_option()                             # List all options
```

|环境变量|用途|
|--------------------|----------|
| `CUDF_COPY_ON_WRITE=1` |启用写时复制 |
| `CUDF_PANDAS_RMM_MODE` |控制 cudf.pandas 的内存分配器 |
| `CUDF_PANDAS_FALLBACK_MODE=1` |在 cudf.pandas 中强制仅执行 CPU |
