---
name: polars-bio
description: Polars DataFrame 上的高性能基因组间隔操作和生物信息学文件 I/O。 BED/VCF/BAM/GFF 间隔的重叠、最近、合并、覆盖、补充、减去。流媒体、云原生、更快的 Bioframe 替代方案。
license: https://github.com/biodatageeks/polars-bio/blob/main/LICENSE
metadata:
    skill-author: K-Dense Inc.
---

# Polars-bio

## 概述

polars-bio 是一个用于基因组间隔操作和生物信息学文件 I/O 的高性能 Python 库，基于 Polars、Apache Arrow 和 Apache DataFusion 构建。它提供了一个熟悉的以 DataFrame 为中心的 API，用于区间算术（重叠、最近、合并、覆盖、补、减）和读/写常见生物信息学格式（BED、VCF、BAM、CRAM、GFF/GTF、FASTA、FASTQ）。

 关键价值主张：
- **在真实世界基因组基准上比 Bioframe 快 6-38 倍**
- **流/核外**通过 DataFusion
 支持大型基因组 - **云原生**文件 I/O（S3、GCS、Azure），带谓词下推
- **两种 API 样式**：函数式 (`pb.overlap(df1, df2)`)和方法链接 (`df1.lazy().pb.overlap(df2)`)
- **通过 DataFusion SQL 用于基因组数据的 SQL 接口** engine

## 何时使用此技能

在以下情况下使用此技能：
- 执行基因组间隔操作（重叠、最近、合并、覆盖、补充、减去）
- 读取/写入生物信息学文件格式（BED、VCF、BAM、CRAM、GFF/GTF、FASTA、FASTQ）
- 处理大型基因组不适合内存的数据集（流模式）
- 在基因组数据文件上运行 SQL 查询
- 从 Bioframe 迁移到更快的替代方案
- 从 BAM/CRAM 文件计算读取深度/堆积
- 使用包含基因组间隔的 Polars 数据帧

## 快速开始

### 安装

```bash
pip install polars-bio
# or
uv pip install polars-bio
```

对于pandas兼容性：
```bash
pip install polars-bio[pandas]
```

### 基本重叠示例

```python
import polars as pl
import polars_bio as pb

# Create two interval DataFrames
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

# Functional API (returns LazyFrame by default)
result = pb.overlap(df1, df2)
result_df = result.collect()

# Get a DataFrame directly
result_df = pb.overlap(df1, df2, output_type="polars.DataFrame")

# Method-chaining API (via .pb accessor on LazyFrame)
result = df1.lazy().pb.overlap(df2)
result_df = result.collect()
```

### 读取BED文件

```python
import polars_bio as pb

# Eager read (loads entire file)
df = pb.read_bed("regions.bed")

# Lazy scan (streaming, for large files)
lf = pb.scan_bed("regions.bed")
result = lf.collect()
```

## 核心功能

### 1.基因组区间操作

polars-bio为基因组范围算术提供8个核心区间运算。所有操作都接受带有 `chrom`、`start`、`end` 列（可配置）的 Polars 数据帧。所有操作默认返回 `LazyFrame`（使用 `output_type="polars.DataFrame"` 获得渴望的结果）。

* *操作：**
- `overlap` / `count_overlaps` - 查找或计算两个集合之间的重叠间隔
- `nearest` - 查找最近的间隔（可配置） `k`、`overlap`、`distance` 参数）
- `merge` - 合并集合内的重叠/预订间隔
- `cluster` - 将集群 ID 分配给重叠间隔
- `coverage` - 计算每个间隔覆盖计数（双输入操作）
- `complement` - 查找基因组内间隔之间的间隙
- `subtract` - 删除与另一组重叠的间隔部分

* *示例：**
```python
import polars_bio as pb

# Find overlapping intervals (returns LazyFrame)
result = pb.overlap(df1, df2, suffixes=("_1", "_2"))

# Count overlaps per interval
counts = pb.count_overlaps(df1, df2)

# Merge overlapping intervals
merged = pb.merge(df1)

# Find nearest intervals
nearest = pb.nearest(df1, df2)

# Collect any LazyFrame result to DataFrame
result_df = result.collect()
```

* *参考：**参见`references/interval_operations.md` 有关所有操作、参数、输出模式和性能注意事项的详细文档。

### 2. 生物信息学文件 I/O

使用 `read_*`、`scan_*`、`write_*` 和 `sink_*` 函数读取和写入常见生物信息学格式。支持云存储（S3、GCS、Azure）和压缩（GZIP、BGZF）。

* *支持的格式：**
- **BED** - 基因组区间（`read_bed`、`scan_bed`、`write_*` 通过通用）
- **VCF** - 遗传变异（`read_vcf`、`scan_vcf`、`write_vcf`、 `sink_vcf`)
- **BAM** - 对齐读取 (`read_bam`、`scan_bam`、`write_bam`、`sink_bam`)
- **CRAM** - 压缩对齐 (`read_cram`、`scan_cram`、 `write_cram`, `sink_cram`)
- **GFF** - 基因注释 (`read_gff`, `scan_gff`)
- **GTF** - 基因注释 (`read_gtf`, `scan_gtf`)
- **FASTA** - 参考序列(`read_fasta`、`scan_fasta`)
- **FASTQ** - 测序读取 (`read_fastq`、`scan_fastq`、`write_fastq`、`sink_fastq`)
- **SAM** - 文本比对 (`read_sam`、 `scan_sam`、`write_sam`、`sink_sam`)
- **Hi-C 对** - 染色质接触（`read_pairs`、 `scan_pairs`)

* *示例：**
```python
import polars_bio as pb

# Read VCF file
variants = pb.read_vcf("samples.vcf.gz")

# Lazy scan BAM file (streaming)
alignments = pb.scan_bam("aligned.bam")

# Read GFF annotations
genes = pb.read_gff("annotations.gff3")

# Cloud storage (individual params, not a dict)
df = pb.read_bed("s3://bucket/regions.bed",
                 allow_anonymous=True)
```

* *参考：**有关每种格式的列架构、参数、云存储选项和压缩支持，请参阅 `references/file_io.md`。

### 3. SQL 数据处理

注册生物信息学文件作为表并使用 DataFusion SQL 查询它们。将 SQL 的强大功能与 polars-bio 的基因组感知阅读器相结合。

```python
import polars as pl
import polars_bio as pb

# Register files as SQL tables (path first, name= keyword)
pb.register_vcf("samples.vcf.gz", name="variants")
pb.register_bed("target_regions.bed", name="regions")

# Query with SQL (returns LazyFrame)
result = pb.sql("SELECT chrom, start, end, ref, alt FROM variants WHERE qual > 30")
result_df = result.collect()

# Register a Polars DataFrame as a SQL table
pb.from_polars("my_intervals", df)
result = pb.sql("SELECT * FROM my_intervals WHERE chrom = 'chr1'").collect()
```

* *参考：** 有关寄存器函数、SQL 语法和示例，请参阅 `references/sql_processing.md`。

### 4. 堆积操作

计算每个碱基的读取深度具有 CIGAR 感知深度计算功能的 BAM/CRAM 文件。

```python
import polars_bio as pb

# Compute depth across a BAM file
depth_lf = pb.depth("aligned.bam")
depth_df = depth_lf.collect()

# With quality filter
depth_lf = pb.depth("aligned.bam", min_mapping_quality=20)
```

* *参考：** 请参阅 `references/pileup_operations.md` 了解参数和积分模式。

## 关键概念

### 坐标系

polars-bio 默认为 **基于 1 的**坐标（基因组）公约）。这可以全局更改：

```python
import polars_bio as pb

# Switch to 0-based coordinates
pb.set_option("coordinate_system", "0-based")

# Switch back to 1-based (default)
pb.set_option("coordinate_system", "1-based")
```

I/O 函数还接受 `use_zero_based` 在生成的 DataFrame 上设置坐标元数据：

```python
# Read BED with explicit 0-based metadata
df = pb.read_bed("regions.bed", use_zero_based=True)
```

* *重要：** BED 文件在文件格式中始终是从 0 开始的半开。 polars-bio 在读取 BED 文件时自动处理转换。坐标元数据通过 I/O 函数附加到 DataFrame，并通过操作传播。

### 两种 API 样式

* *功能 API** - 独立函数，显式输入：
```python
result = pb.overlap(df1, df2, suffixes=("_1", "_2"))
merged = pb.merge(df)
```

* *方法链接 API** - 通过 **LazyFrames** 上的 `.pb` 访问器（不是DataFrames):
```python
result = df1.lazy().pb.overlap(df2)
merged = df.lazy().pb.merge()
```

* *重要：** 用于区间操作的 `.pb` 访问器仅在 `LazyFrame` 上可用。在 `DataFrame` 上，`.pb` 仅提供写操作（`write_bam`、`write_vcf` 等）。

 方法链可实现流畅的管道：
```python
# Chain interval operations (note: overlap outputs suffixed columns,
# so rename before merge which expects chrom/start/end)
result = (
    df1.lazy()
    .pb.overlap(df2)
    .filter(pl.col("start_2") > 1000)
    .select(
        pl.col("chrom_1").alias("chrom"),
        pl.col("start_1").alias("start"),
        pl.col("end_1").alias("end"),
    )
    .pb.merge()
    .collect()
)
```

### 探针构建架构

对于两个输入操作（重叠、最近、count_overlaps、覆盖），polars-bio 使用探针构建连接策略：
- **第一个** DataFrame 是 **探针**（迭代）
- **第二个** DataFrame 是 **构建**（索引用于查找）

 为了获得最佳性能，将较大的 DataFrame 作为第一个参数（探针）传递，较小的 DataFrame 传递作为第二个（构建）。

### 列约定

默认情况下，polars-bio 需要名为 `chrom`、`start`、`end` 的列。可以通过列表指定自定义列名称：

```python
result = pb.overlap(
    df1, df2,
    cols1=["chromosome", "begin", "finish"],
    cols2=["chr", "pos_start", "pos_end"],
)
```

### 返回类型和收集结果

所有间隔操作和`pb.sql()`默认返回**LazyFrame**。使用 `.collect()` 实现结果，或传递 `output_type="polars.DataFrame"` 进行急切评估：

```python
# Lazy (default) - collect when needed
result_lf = pb.overlap(df1, df2)
result_df = result_lf.collect()

# Eager - get DataFrame directly
result_df = pb.overlap(df1, df2, output_type="polars.DataFrame")
```

### 流式处理和核外处理

对于大于可用 RAM 的数据集，请使用 `scan_*` 函数和流式执行：

```python
# Scan files lazily
lf = pb.scan_bed("large_intervals.bed")

# Process with streaming
result = lf.collect(streaming=True)
```

DataFusion流默认启用间隔操作，批量处理数据而不将完整数据集加载到内存中。

## 常见陷阱

1. **DataFrame 与 LazyFrame 上的 `.pb` 访问器：** 间隔操作（重叠、合并等）仅适用于 `LazyFrame.pb`。 `DataFrame.pb`只有写方法。在链接间隔 ops.

2 之前使用 `.lazy()` 进行转换。 **LazyFrame 返回：** 所有区间操作和 `pb.sql()` 默认返回 `LazyFrame`。不要忘记 `.collect()` 或使用 `output_type="polars.DataFrame"`.

3. **列名称不匹配：** 默认情况下，polars-bio 需要 `chrom`、`start`、`end`。如果您的列具有不同的名称，请使用 `cols1`/`cols2` 参数（作为列表）。

4. **坐标系元数据：** 手动构建 DataFrame 时（不是通过 `read_*`/`scan_*`），polars-bio 会警告缺少坐标元数据。全局使用`pb.set_option("coordinate_system", "0-based")`，或者使用自动设置元数据的I/O函数。

5. **探测构建顺序很重要：**对于重叠、最近和覆盖，第一个 DataFrame 将针对第二个 DataFrame 进行探测。交换参数会更改左右输出列中出现的间隔，并可能影响性能。

6. **INT32 位置限制：** 基因组位置存储为 32 位整数，将坐标限制为约 21 亿。这对于所有已知的基因组来说已经足够了，但对于自定义坐标空间可能是一个问题。

7. **BAM 索引要求：** `read_bam` 和 `scan_bam` 需要 `.bai` 索引文件以及 BAM。如果缺少，请使用 `samtools index` 创建一个。

8. **默认情况下禁用并行执行：** DataFusion 并行度默认为 1 个分区。对于大型数据集启用：
 ```python
 pb.set_option("datafusion.execution.target_partitions", 8)
 ```

9. **CRAM 具有单独的功能：** 对于 CRAM 文件使用 `read_cram`/`scan_cram`/`register_cram`（不是 `read_bam`）。 CRAM 函数需要 `reference_path` 参数。

## 最佳实践

1. **对于大文件使用 `scan_*`：** 对于大于可用 RAM 的文件，优先选择 `scan_bed`、`scan_vcf` 等，而不是 `read_*`。扫描函数启用流式传输和谓词下推。

2. **为大型数据集配置并行度：**
 ```python
 import os
 pb.set_option("datafusion.execution.target_partitions", os.cpu_count())
 ```

3. **使用 BGZF 压缩：** BGZF 压缩文件（`.bed.gz`、`.vcf.gz`）支持并行块解压缩，明显快于普通 GZIP.

4. **尽早选择列：** 当只需要特定列时，尽早选择它们以减少内存使用：
 ```python
 df = pb.read_vcf("large.vcf.gz").select("chrom", "start", "end", "ref", "alt")
 ```

5. **直接使用云路径：** 直接传递 S3/GCS/Azure URI 来读取/扫描函数，而不是先下载文件：
 ```python
 df = pb.read_bed("s3://my-bucket/regions.bed", allowed_anonymous=True)
 ```

6. **对于单一操作优先使用函数式 API，对于管道使用方法链接：** 使用 `pb.overlap()` 进行一次性操作，在构建多步骤管道时使用 `.lazy().pb.overlap()`。

## 资源

### 参考文献/

每个主要功能的详细文档：

- **interval_operations.md** -所有 8 个区间操作均包含参数、示例、输出模式和性能提示。基因组范围算术的核心参考.

- **file_io.md** - 支持的格式表、每种格式的列模式、云存储配置、压缩支持和通用参数。

- **sql_processing.md** - 注册函数、DataFusion SQL 语法、将 SQL 与间隔操作相结合以及示例查询。

- **pileup_operations.md** - 从 BAM/CRAM 文件、参数和间隔集成进行每基读取深度计算Operations.

- **configuration.md** - 全局设置（并行度、坐标系、流模式）、日志记录和元数据管理。

- **bioframe_migration.md** - 操作映射表、API 差异、性能比较、迁移代码示例和 pandas 兼容模式。
