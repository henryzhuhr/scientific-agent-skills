# 基因组区间运算

## 概述

polars-bio 为基因组区间运算提供了8个核心运算。所有操作都适用于包含基因组间隔的 Polars DataFrame 或 LazyFrame（默认情况下，列：`chrom`、`start`、`end`），并默认返回 **LazyFrame**。通过`output_type="polars.DataFrame"`以获得渴望的结果。

## 操作摘要

|运营|输入 |描述|
|------------|--------|-------------|
| `overlap` |两个数据框 |查找重叠间隔对 |
| `count_overlaps` |两个数据框 |计算第一组中每个间隔的重叠 |
| `nearest` |两个数据框 |查找两组之间最近的间隔 |
| `merge` |一个数据框 |合并重叠/预定间隔 |
| `cluster` |一个数据框 |将集群 ID 分配给重叠间隔 |
| `coverage` |两个数据框 |计算每个时间间隔的覆盖计数 |
| `complement` |一个 DataFrame + 基因组 |查找间隔之间的间隙 |
| `subtract` |两个数据框 |删除重叠部分|

## 重叠

查找两个DataFrame之间的重叠间隔对。

### 功能API

```python
import polars as pl
import polars_bio as pb

df1 = pl.DataFrame({
    "chrom": ["chr1", "chr1", "chr1"],
    "start": [1, 5, 22],
    "end":   [6, 9, 30],
})

df2 = pl.DataFrame({
    "chrom": ["chr1", "chr1"],
    "start": [3, 25],
    "end":   [8, 28],
})

# Returns LazyFrame by default
result_lf = pb.overlap(df1, df2, suffixes=("_1", "_2"))
result_df = result_lf.collect()

# Or get DataFrame directly
result_df = pb.overlap(df1, df2, suffixes=("_1", "_2"), output_type="polars.DataFrame")
```

### 方法链接API（LazyFrame）仅)

```python
result = df1.lazy().pb.overlap(df2, suffixes=("_1", "_2")).collect()
```

### 参数

|参数|类型 |默认|描述 |
|-----------|------|---------|------------|
| `df1` |数据帧/LazyFrame/str |必填|第一个（探测）间隔集 |
| `df2` |数据帧/LazyFrame/str |必填|第二个（构建）间隔设置 |
| `suffixes` |元组[str, str] | `("_1", "_2")` |重叠列名称的后缀 |
| `on_cols` |列表[str] | `None` |要加入的其他列（基因组坐标之外）|
| `cols1` |列表[str] | `["chrom", "start", "end"]` | df1 |
| 中的列名称`cols2` |列表[str] | `["chrom", "start", "end"]` | df2 |
| 中的列名称`algorithm` | STR | `"Coitrees"` |区间算法|
| `low_memory` |布尔 | `False` |低内存模式|
| `output_type` | STR | `"polars.LazyFrame"` |输出格式：`"polars.LazyFrame"`、`"polars.DataFrame"`、`"pandas.DataFrame"` |
| `projection_pushdown` |布尔 | `True` |启用投影下推优化 |

### 输出架构

从两个输入返回应用了后缀的列：
- `chrom_1`、`start_1`、`end_1`（来自 df1）
- `chrom_2`、 `start_2`、`end_2`（来自 df2）
- 来自 df1 和 df2

 的任何其他列

 列 dtypes 对于 chrom 为 `String`，对于开始/结束为 `Int64`。

## count_overlaps

计算 df1 中每个区间与 df2 的重叠区间数。

```python
# Functional
counts = pb.count_overlaps(df1, df2)

# Method-chaining (LazyFrame)
counts = df1.lazy().pb.count_overlaps(df2)
```

### 参数

|参数|类型 |默认|描述 |
|-----------|------|---------|------------|
| `df1` |数据帧/LazyFrame/str |必填|查询间隔设置|
| `df2` |数据帧/LazyFrame/str |必填|目标间隔设定|
| `suffixes` |元组[str, str] | `("", "_")` |列名称的后缀 |
| `cols1` |列表[str] | `["chrom", "start", "end"]` | df1 |
| 中的列名称`cols2` |列表[str] | `["chrom", "start", "end"]` | df2 |
| 中的列名称`on_cols` |列表[str] | `None` |附加连接列|
| `output_type` | STR | `"polars.LazyFrame"` |输出格式|
| `naive_query` |布尔 | `True` |使用朴素查询策略|
| `projection_pushdown` |布尔 | `True` |启用投影下推 |

### 输出架构

返回 df1 列以及附加的 `count` 列 (Int64)。

## 最近的

在 df2 中查找每个间隔的最近间隔df1.

```python
# Find nearest (default: k=1, any direction)
nearest = pb.nearest(df1, df2, output_type="polars.DataFrame")

# Find k nearest
nearest = pb.nearest(df1, df2, k=3)

# Exclude overlapping intervals from results
nearest = pb.nearest(df1, df2, overlap=False)

# Without distance column
nearest = pb.nearest(df1, df2, distance=False)
```

### 参数

|参数|类型 |默认|描述 |
|-----------|------|---------|------------|
| `df1` |数据帧/LazyFrame/str |必填|查询间隔设置|
| `df2` |数据帧/LazyFrame/str |必填|目标间隔设定|
| `suffixes` |元组[str, str] | `("_1", "_2")` |列名称的后缀 |
| `on_cols` |列表[str] | `None` |附加连接列|
| `cols1` |列表[str] | `["chrom", "start", "end"]` | df1 |
| 中的列名称`cols2` |列表[str] | `["chrom", "start", "end"]` | df2 |
| 中的列名称`k` |整数 | `1` |要查找的最近邻居的数量|
| `overlap` |布尔 | `True` |在结果中包含重叠间隔 |
| `distance` |布尔 | `True` |在输出中包含距离列 |
| `output_type` | STR | `"polars.LazyFrame"` |输出格式|
| `projection_pushdown` |布尔 | `True` |启用投影下推 |

### 输出架构

返回两个 DataFrame（带后缀）的列以及 `distance` 列 (Int64)，其中包含到最近间隔的距离（如果重叠则为 0）。如果 `distance=False`.

## merge

Merge 单个 DataFrame 内的重叠和预订间隔，则省略距离列。

```python
import polars as pl
import polars_bio as pb

df = pl.DataFrame({
    "chrom": ["chr1", "chr1", "chr1", "chr2"],
    "start": [1, 4, 20, 1],
    "end":   [6, 9, 30, 10],
})

# Functional
merged = pb.merge(df, output_type="polars.DataFrame")

# Method-chaining (LazyFrame)
merged = df.lazy().pb.merge().collect()

# Merge intervals within a minimum distance
merged = pb.merge(df, min_dist=10)
```

### 参数

|参数|类型 |默认|描述 |
|-----------|------|---------|------------|
| `df` |数据帧/LazyFrame/str |必填|设置合并的间隔 |
| `min_dist` |整数 | `0` |要合并的间隔之间的最小距离（0 = 必须重叠或被书封）|
| `cols` |列表[str] | `["chrom", "start", "end"]` |列名称 |
| `on_cols` |列表[str] | `None` |附加分组列|
| `output_type` | STR | `"polars.LazyFrame"` |输出格式|
| `projection_pushdown` |布尔 | `True` |启用投影下推 |

### 输出架构

|专栏 |类型 |描述 |
|--------|------|-------------|
| `chrom` |字符串|染色体|
| `start` | Int64 |合并区间开始|
| `end` | Int64 |合并区间结束|
| `n_intervals` | Int64 |合并的间隔数 |

## cluster

将簇 ID 分配给重叠间隔。重叠的间隔被分配相同的簇ID。

```python
# Functional
clustered = pb.cluster(df, output_type="polars.DataFrame")

# Method-chaining (LazyFrame)
clustered = df.lazy().pb.cluster().collect()

# With minimum distance
clustered = pb.cluster(df, min_dist=5)
```

### 参数|类型 |默认|描述|
|---------|------|---------|----------|
| `df` |数据帧/LazyFrame/str |必填|间隔设定|
| `min_dist` |整数 | `0` |聚类的最小距离|
| `cols` |列表[str] | `["chrom", "start", "end"]` |列名称|
| `output_type` | STR | `"polars.LazyFrame"` |输出格式|
| `projection_pushdown` |布尔 | `True` |启用投影下推 |

### 输出架构

返回原始列加上：

|专栏 |类型 |描述 |
|--------|------|-------------|
| `cluster` | Int64 |簇ID（同一簇内的间隔重叠）|
| `cluster_start` | Int64 |集群范围的开始 |
| `cluster_end` | Int64 |集群范围结束 |

## 覆盖范围

计算每个时间间隔的覆盖计数。这是一个**双输入**操作：对于 df1 中的每个间隔，计算 df2 中的覆盖范围。

```python
# Functional
cov = pb.coverage(df1, df2, output_type="polars.DataFrame")

# Method-chaining (LazyFrame)
cov = df1.lazy().pb.coverage(df2).collect()
```

### 参数|类型 |默认|描述 |
|-----------|------|---------|------------|
| `df1` |数据帧/LazyFrame/str |必填|查询间隔|
| `df2` |数据帧/LazyFrame/str |必填|覆盖源区间|
| `suffixes` |元组[str, str] | `("_1", "_2")` |列名称的后缀 |
| `on_cols` |列表[str] | `None` |附加连接列|
| `cols1` |列表[str] | `["chrom", "start", "end"]` | df1 |
| 中的列名称`cols2` |列表[str] | `["chrom", "start", "end"]` | df2 |
| 中的列名称`output_type` | STR | `"polars.LazyFrame"` |输出格式|
| `projection_pushdown` |布尔 | `True` |启用投影下推 |

### 输出架构

从 df1 返回列加上 `coverage` 列 (Int64)。

## 补足 

查找基因组内间隔之间的间隙。需要指定染色体大小的基因组定义。

```python
import polars as pl
import polars_bio as pb

df = pl.DataFrame({
    "chrom": ["chr1", "chr1"],
    "start": [100, 500],
    "end":   [200, 600],
})

genome = pl.DataFrame({
    "chrom": ["chr1"],
    "start": [0],
    "end":   [1000],
})

# Functional
gaps = pb.complement(df, view_df=genome, output_type="polars.DataFrame")

# Method-chaining (LazyFrame)
gaps = df.lazy().pb.complement(genome).collect()
```

### 参数

|参数|类型 |默认|描述|
|---------|------|---------|----------|
| `df` |数据帧/LazyFrame/str |必填|间隔设定|
| `view_df` |数据帧/LazyFrame | `None` |带有 chrom、开始、结束定义染色体范围的基因组 |
| `cols` |列表[str] | `["chrom", "start", "end"]` | df |
| 中的列名称`view_cols` |列表[str] | `None` | view_df |
| 中的列名称`output_type` | STR | `"polars.LazyFrame"` |输出格式|
| `projection_pushdown` |布尔 | `True` |启用投影下推 |

### 输出架构

返回一个 DataFrame，其中 `chrom` (String)、`start` (Int64)、`end` (Int64)列表示间隔之间的间隙。

## 减去

删除 df1 中与间隔重叠的间隔部分df2.

```python
# Functional
result = pb.subtract(df1, df2, output_type="polars.DataFrame")

# Method-chaining (LazyFrame)
result = df1.lazy().pb.subtract(df2).collect()
```

### 参数

|参数|类型 |默认|描述 |
|-----------|------|---------|-------------|
| `df1` |数据帧/LazyFrame/str |必填|从 |
| 中减去的间隔`df2` |数据帧/LazyFrame/str |必填|减去|
|的间隔`cols1` |列表[str] | `["chrom", "start", "end"]` | df1 |
| 中的列名称`cols2` |列表[str] | `["chrom", "start", "end"]` | df2 |
| 中的列名称`output_type` | STR | `"polars.LazyFrame"` |输出格式|
| `projection_pushdown` |布尔 | `True` |启用投影下推 |

### 输出架构

返回 `chrom` (String)、`start` (Int64)、`end` (Int64)，表示减法后 df1 区间的剩余部分。

## 性能注意事项

### 探针构建架构

双输入操作（`overlap`、`nearest`、`count_overlaps`、`coverage`、`subtract`）使用探针构建连接：
- **探针**（第一个） DataFrame)：逐行迭代
- **构建**（第二个DataFrame）：索引到区间树中以进行快速查找

为了获得最佳性能，将**较大** DataFrame 作为探针（第一个参数）传递，将**较小** DataFrame 作为构建（第二个参数）传递。

### 并行性

默认情况下， polars-bio 使用单个执行分区。对于大型数据集，启用并行执行：

```python
import os
import polars_bio as pb

pb.set_option("datafusion.execution.target_partitions", os.cpu_count())
```

### 流式执行

DataFusion流式传输默认启用用于间隔操作。数据批量处理，支持大于可用RAM的数据集的核外计算。

### 何时使用延迟评估

使用 `scan_*` 函数和延迟 DataFrame 用于：
- 文件大于可用 RAM
- 仅需要结果子集时
- 可以优化中间结果的管道操作

```python
# Lazy pipeline
lf1 = pb.scan_bed("large1.bed")
lf2 = pb.scan_bed("large2.bed")
result = pb.overlap(lf1, lf2).collect()
```
