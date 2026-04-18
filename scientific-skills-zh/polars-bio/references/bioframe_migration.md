# 从 Bioframe 迁移到 Polars-bio

## 概述

polars-bio 是 Bioframe 核心间隔操作的直接替代品，在现实世界的基因组基准上提供 6.5-38 倍的加速。主要区别是：Polars DataFrames 而不是 pandas、Rust/DataFusion 后端而不是纯 Python、对大型基因组的流支持以及默认返回 LazyFrame。

## 操作映射

|生物框架| polars-bio |注释 |
|----------|------------|--------|
| `bioframe.overlap(df1, df2)` | `pb.overlap(df1, df2)` |返回 LazyFrame； `.collect()` for DataFrame |
| `bioframe.closest(df1, df2)` | `pb.nearest(df1, df2)` |更名；使用 `k`、`overlap`、`distance` 参数 |
| `bioframe.count_overlaps(df1, df2)` | `pb.count_overlaps(df1, df2)` |默认后缀不同：`("", "_")` 与 bioframe 的 |
| `bioframe.merge(df)` | `pb.merge(df)` |输出包括 `n_intervals` 列 |
| `bioframe.cluster(df)` | `pb.cluster(df)` |输出列：`cluster`、`cluster_start`、`cluster_end` |
| `bioframe.coverage(df1, df2)` | `pb.coverage(df1, df2)` |两个库中的双输入 |
| `bioframe.complement(df, chromsizes)` | `pb.complement(df, view_df=genome)` |基因组作为数据帧，而不是系列 |
| `bioframe.subtract(df1, df2)` | `pb.subtract(df1, df2)` |相同语义 |

## 主要 API 差异

### 数据帧：pandas 与 Polars

* *bioframe（pandas）：**
```python
import bioframe
import pandas as pd

df1 = pd.DataFrame({
    "chrom": ["chr1", "chr1"],
    "start": [1, 10],
    "end":   [5, 20],
})

result = bioframe.overlap(df1, df2)
# result is a pandas DataFrame
result["start_1"]  # pandas column access
```

* *polars-bio (Polars):**
```python
import polars_bio as pb
import polars as pl

df1 = pl.DataFrame({
    "chrom": ["chr1", "chr1"],
    "start": [1, 10],
    "end":   [5, 20],
})

result = pb.overlap(df1, df2)  # Returns LazyFrame
result_df = result.collect()   # Materialize to DataFrame
result_df.select("start_1")   # Polars column access
```

### 返回类型：默认为 LazyFrame

所有 polars-bio 操作默认返回 **LazyFrame**。使用 `.collect()` 或 `output_type="polars.DataFrame"`:

```python
# bioframe: always returns DataFrame
result = bioframe.overlap(df1, df2)

# polars-bio: returns LazyFrame, collect for DataFrame
result_lf = pb.overlap(df1, df2)
result_df = result_lf.collect()

# Or get DataFrame directly
result_df = pb.overlap(df1, df2, output_type="polars.DataFrame")
```

### 基因组/Chromsizes

* *生物框架：**
```python
chromsizes = bioframe.fetch_chromsizes("hg38")  # Returns pandas Series
complement = bioframe.complement(df, chromsizes)
```

* *polars-bio：**
```python
genome = pl.DataFrame({
    "chrom": ["chr1", "chr2"],
    "start": [0, 0],
    "end":   [248956422, 242193529],
})
complement = pb.complement(df, view_df=genome)
```

### 最接近

* *bioframe:**
```python
result = bioframe.closest(df1, df2)
```

* *polars-bio:**
```python
# Basic nearest
result = pb.nearest(df1, df2)

# Find k nearest neighbors
result = pb.nearest(df1, df2, k=3)

# Exclude overlapping intervals
result = pb.nearest(df1, df2, overlap=False)

# Without distance column
result = pb.nearest(df1, df2, distance=False)
```

### 方法链接（仅限 polars-bio）

polars-bio 添加了一个**LazyFrame** 上的 `.pb` 访问器用于方法链接：

```python
# bioframe: sequential function calls
merged = bioframe.merge(bioframe.overlap(df1, df2))

# polars-bio: fluent pipeline (must use LazyFrame)
# Note: overlap adds suffixes, so rename before merge
merged = (
    df1.lazy()
    .pb.overlap(df2)
    .select(
        pl.col("chrom_1").alias("chrom"),
        pl.col("start_1").alias("start"),
        pl.col("end_1").alias("end"),
    )
    .pb.merge()
    .collect()
)
```

## 性能比较

真实世界基因组数据集的基准（来自 polars-bio 论文，生物信息学 2025）：

|运营|生物框架| polars-bio |加速比|
|------------|---------|------------|---------|
|重叠| 1.0 倍 | 6.5 倍 | 6.5x |
|最近的| 1.0 倍 | 38x | 38x |
|合并| 1.0 倍 | 8.2 倍 | 8.2x |
|报道 | 1.0 倍 | 12 倍 | 12x |

 加速来自：
- 基于 Rust 的区间树实现
- Apache DataFusion 查询引擎
- Apache Arrow 列式内存格式
- 并行执行（配置后）
- 流/核外支持

## 迁移代码示例

### 示例1：基本重叠管道

* *之前（bioframe）：**
```python
import bioframe
import pandas as pd

df1 = pd.read_csv("peaks.bed", sep="\t", names=["chrom", "start", "end"])
df2 = pd.read_csv("genes.bed", sep="\t", names=["chrom", "start", "end", "name"])

overlaps = bioframe.overlap(df1, df2, suffixes=("_peak", "_gene"))
filtered = overlaps[overlaps["start_gene"] > 10000]
merged = bioframe.merge(filtered[["chrom_peak", "start_peak", "end_peak"]]
    .rename(columns={"chrom_peak": "chrom", "start_peak": "start", "end_peak": "end"}))
```

* *之后（polars-bio）：**
```python
import polars_bio as pb
import polars as pl

df1 = pb.read_bed("peaks.bed")
df2 = pb.read_bed("genes.bed")

overlaps = pb.overlap(df1, df2, suffixes=("_peak", "_gene"), output_type="polars.DataFrame")
filtered = overlaps.filter(pl.col("start_gene") > 10000)
merged = pb.merge(
    filtered.select(
        pl.col("chrom_peak").alias("chrom"),
        pl.col("start_peak").alias("start"),
        pl.col("end_peak").alias("end"),
    ),
    output_type="polars.DataFrame",
)
```

### 示例2：大规模Streaming

* *之前（bioframe） - 仅限于内存中：**
```python
import bioframe
import pandas as pd

# Must load entire file into memory
df1 = pd.read_csv("huge_intervals.bed", sep="\t", names=["chrom", "start", "end"])
result = bioframe.merge(df1)  # Memory-bound
```

 * *之后（polars-bio） - 流式传输：**
```python
import polars_bio as pb

# Lazy scan, streaming execution
lf = pb.scan_bed("huge_intervals.bed")
result = pb.merge(lf).collect(streaming=True)
```

## pandas兼容模式

For渐进迁移，安装 pandas 支持：

```bash
pip install polars-bio[pandas]
```

这可以实现 pandas 和 Polars 数据帧之间的转换：

```python
import polars_bio as pb
import polars as pl

# Convert pandas DataFrame to Polars for polars-bio
polars_df = pl.from_pandas(pandas_df)
result = pb.overlap(polars_df, other_df).collect()

# Convert back to pandas if needed
pandas_result = result.to_pandas()

# Or request pandas output directly
pandas_result = pb.overlap(polars_df, other_df, output_type="pandas.DataFrame")
```

## 迁移检查表

1. 将 `import bioframe` 替换为 `import polars_bio as pb`
2. 将 `import pandas as pd` 替换为 `import polars as pl`
3. 将 DataFrame 创建从 `pd.DataFrame` 转换为 `pl.DataFrame`
4. 将 `bioframe.closest` 替换为 `pb.nearest`
5. 操作后添加`.collect()`（默认返回LazyFrame）
6. 将列访问从 `df["col"]` 更新为 `df.select("col")` 或 `pl.col("col")`
7. 将 pandas 过滤 `df[df["col"] > x]` 替换为 `df.filter(pl.col("col") > x)`
8. 使用 `chrom`、`start`、`end` 将铬尺寸从系列更新为 DataFrame；传递为 `view_df=`
9. 添加 `pb.set_option("datafusion.execution.target_partitions", N)` 以实现并行度 
10. 将 BED 文件的 `pd.read_csv` 替换为 `pb.read_bed` 或 `pb.scan_bed`
11. 注意 `cluster` 输出列是 `cluster`（不是 `cluster_id`），加上 `cluster_start`、`cluster_end`
12. 注：`merge` 输出包括 `n_intervals` 列 
