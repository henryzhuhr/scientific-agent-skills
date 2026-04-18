# 堆积操作

## 概述

polars-bio 提供了 `pb.depth()` 函数，用于计算 BAM/CRAM 文件中每个碱基或每个块的读取深度。它使用 CIGAR 感知深度计算来准确地解释插入、删除和剪辑。默认返回 **LazyFrame**。

## pb.depth()

从对齐文件中计算读取深度。

### 基本用法

```python
import polars_bio as pb

# Compute depth across entire BAM file (returns LazyFrame)
depth_lf = pb.depth("aligned.bam")
depth_df = depth_lf.collect()

# Get DataFrame directly
depth_df = pb.depth("aligned.bam", output_type="polars.DataFrame")
```

### 参数

|参数|类型 |默认|描述 |
|-----------|------|---------|------------|
| `path` | STR |必填| BAM 或 CRAM 文件的路径 |
| `filter_flag` |整数 | `1796` | SAM 标志过滤器（默认排除未映射、次要、重复、QC 失败）|
| `min_mapping_quality` |整数 | `0` |包含读取的最低映射质量 |
| `binary_cigar` |布尔 | `True` |使用二进制 CIGAR 进行更快的处理 |
| `dense_mode` | STR | `"auto"` |密集输出模式|
| `use_zero_based` |布尔 | `None` |坐标系（无=使用全局设置）|
| `per_base` |布尔 | `False` |每碱基深度（真）与块深度（假）|
| `output_type` | STR | `"polars.LazyFrame"` |输出格式：`"polars.LazyFrame"`、`"polars.DataFrame"`、`"pandas.DataFrame"` |

### 输出架构（块模式，默认）

当 `per_base=False`（默认）时，具有相同深度的相邻位置被分组为块：

|专栏 |类型 |描述|
|--------|------|-------------|
| `contig` |字符串|染色体/重叠群名称 |
| `pos_start` | Int64 |块起始位置|
| `pos_end` | Int64 |块结束位置|
| `coverage` |整数16 |读取深度 |

### 输出架构（Per-Base 模式）

当 `per_base=True` 时，每个位置单独报告：

|专栏 |类型 |说明 |
|--------|------|-------------|
| `contig` |字符串|染色体/重叠群名称 |
| `pos` | Int64 |位置|
| `coverage` |整数16 |位置 |

### filter_flag

的读取深度默认 `filter_flag=1796` 排除具有以下 SAM 标志的读取：
- 4：未映射 
- 256：二次比对 
- 512：失败 QC
- 1024：PCR/光学重复

### CIGAR感知计算

`pb.depth()`正确处理CIGAR操作：
- **M/X/=**（匹配/不匹配）：计为覆盖范围
- **D**（删除）：计为覆盖范围（读取跨越删除）
- **N**（跳过区域）：不计算（例如，剪接比对）
- **I**（插入）：在参考位置不计算
- **S/H**（软/硬剪切）：不计算

## 示例

### 全基因组深度

```python
import polars_bio as pb
import polars as pl

# Compute depth genome-wide (block mode)
depth = pb.depth("sample.bam", output_type="polars.DataFrame")

# Summary statistics
depth.select(
    pl.col("coverage").cast(pl.Int64).mean().alias("mean_depth"),
    pl.col("coverage").cast(pl.Int64).median().alias("median_depth"),
    pl.col("coverage").cast(pl.Int64).max().alias("max_depth"),
)
```

### 每碱基深度

```python
import polars_bio as pb

# Per-base depth (one row per position)
depth = pb.depth("sample.bam", per_base=True, output_type="polars.DataFrame")
```

### 带质量过滤器的深度

```python
import polars_bio as pb

# Only count well-mapped reads
depth = pb.depth(
    "sample.bam",
    min_mapping_quality=20,
    output_type="polars.DataFrame",
)
```

### 自定义标志Filter

```python
import polars_bio as pb

# Only exclude unmapped (4) and duplicate (1024) reads
depth = pb.depth(
    "sample.bam",
    filter_flag=4 + 1024,
    output_type="polars.DataFrame",
)
```

## 与区间运算集成

深度结果可与 polars-bio 区间运算一起使用。请注意，深度输出使用 `contig`/`pos_start`/`pos_end` 列名称，因此请使用 `cols` 参数来映射它们：

```python
import polars_bio as pb
import polars as pl

# Compute depth
depth = pb.depth("sample.bam", output_type="polars.DataFrame")

# Rename columns to match interval operation conventions
depth_intervals = depth.rename({
    "contig": "chrom",
    "pos_start": "start",
    "pos_end": "end",
})

# Find regions with adequate coverage
adequate = depth_intervals.filter(pl.col("coverage") >= 30)

# Merge adjacent adequate-coverage blocks
merged = pb.merge(adequate, output_type="polars.DataFrame")

# Find gaps in coverage (complement)
genome = pl.DataFrame({
    "chrom": ["chr1"],
    "start": [0],
    "end": [248956422],
})
gaps = pb.complement(adequate, view_df=genome, output_type="polars.DataFrame")
```

### 使用 cols 参数而不是重命名

```python
import polars_bio as pb

depth = pb.depth("sample.bam", output_type="polars.DataFrame")
targets = pb.read_bed("targets.bed")

# Use cols1 to specify depth column names
overlapping = pb.overlap(
    depth, targets,
    cols1=["contig", "pos_start", "pos_end"],
    output_type="polars.DataFrame",
)
```
