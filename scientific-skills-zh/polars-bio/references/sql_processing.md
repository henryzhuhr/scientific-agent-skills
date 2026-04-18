# SQL 数据处理

## 概述

polars-bio 集成了 Apache DataFusion 的 SQL 引擎，支持对生物信息学文件和 Polars DataFrame 进行 SQL 查询。将文件注册为表并使用标准 SQL 语法查询它们。所有查询都会返回 **LazyFrame** — 调用 `.collect()` 来实现结果。

## 注册函数

将生物信息学文件注册为 SQL 表。 **路径是第一个参数**，名称是可选关键字：

```python
import polars_bio as pb

# Register various file formats (path first, name= keyword)
pb.register_vcf("samples.vcf.gz", name="variants")
pb.register_bed("target_regions.bed", name="regions")
pb.register_bam("aligned.bam", name="alignments")
pb.register_cram("aligned.cram", name="cram_alignments")
pb.register_gff("genes.gff3", name="annotations")
pb.register_gtf("genes.gtf", name="gtf_annotations")
pb.register_fastq("sample.fastq.gz", name="reads")
pb.register_sam("alignments.sam", name="sam_alignments")
pb.register_pairs("contacts.pairs", name="hic_contacts")
```

### 参数

所有`register_*`函数共享这些参数：

|参数|类型 |默认|描述 |
|-----------|------|---------|------------|
| `path` | STR |必需（第一个位置）|文件路径（本地或云）|
| `name` | STR | `None` | SQL 查询的表名称（如果省略则自动生成）|
| `chunk_size` |整数 | `64` |用于读取的块大小|
| `concurrent_fetches` |整数 | `8` |并发云获取|
| `allow_anonymous` |布尔 | `True` |允许匿名云访问|
| `max_retries` |整数 | `5` |云重试次数|
| `timeout` |整数 | `300` |云超时（以秒为单位）|
| `enable_request_payer` |布尔 | `False` |请求者支付云|
| `compression_type` | STR | `"auto"` |压缩类型 |

 某些寄存器函数具有附加的特定于格式的参数（例如，`register_vcf` 上的 `info_fields`）。

* *注意：** `register_fasta` 不存在。使用 `scan_fasta` + `from_polars` 作为解决方法。

## from_polars

将现有的 Polars DataFrame 注册为 SQL 可查询表：

```python
import polars as pl
import polars_bio as pb

df = pl.DataFrame({
    "chrom": ["chr1", "chr1", "chr2"],
    "start": [100, 500, 200],
    "end":   [200, 600, 400],
    "name":  ["peak1", "peak2", "peak3"],
})

pb.from_polars("my_peaks", df)

# Now query with SQL
result = pb.sql("SELECT * FROM my_peaks WHERE chrom = 'chr1'").collect()
```

* *重要：** `register_view`接受 SQL 查询字符串，而不是 DataFrame。使用`from_polars`注册DataFrames。

## register_view

从查询字符串创建SQL视图：

```python
import polars_bio as pb

# Create a view from a SQL query
pb.register_view("chr1_variants", "SELECT * FROM variants WHERE chrom = 'chr1'")

# Query the view
result = pb.sql("SELECT * FROM chr1_variants WHERE qual > 30").collect()
```

### 参数

|参数|类型 |描述 |
|-----------|------|-------------|
| `name` | STR |查看名称 |
| `query` | STR |定义视图的 SQL 查询字符串 |

## pb.sql()

使用 DataFusion SQL 语法执行 SQL 查询。 **返回 LazyFrame** — 调用 `.collect()` 获取 DataFrame.

```python
import polars_bio as pb

# Simple query
result = pb.sql("SELECT chrom, start, end FROM regions WHERE chrom = 'chr1'").collect()

# Aggregation
result = pb.sql("""
    SELECT chrom, COUNT(*) as variant_count, AVG(qual) as avg_qual
    FROM variants
    GROUP BY chrom
    ORDER BY variant_count DESC
""").collect()

# Join tables
result = pb.sql("""
    SELECT v.chrom, v.start, v.end, v.ref, v.alt, r.name
    FROM variants v
    JOIN regions r ON v.chrom = r.chrom
        AND v.start >= r.start
        AND v.end <= r.end
""").collect()
```

## DataFusion SQL 语法

polars-bio 使用 Apache DataFusion 的 SQL 方言。主要功能：

### 过滤

```sql
SELECT * FROM variants WHERE qual > 30 AND filter = 'PASS'
```

### 聚合

```sql
SELECT chrom, COUNT(*) as n, MIN(start) as min_pos, MAX(end) as max_pos
FROM regions
GROUP BY chrom
HAVING COUNT(*) > 100
```

### 窗口函数

```sql
SELECT chrom, start, end,
    ROW_NUMBER() OVER (PARTITION BY chrom ORDER BY start) as row_num,
    LAG(end) OVER (PARTITION BY chrom ORDER BY start) as prev_end
FROM regions
```

### 子查询

```sql
SELECT * FROM variants
WHERE chrom IN (SELECT DISTINCT chrom FROM regions)
```

### 通用表表达式（CTE）

```sql
WITH filtered_variants AS (
    SELECT * FROM variants WHERE qual > 30
),
chr1_regions AS (
    SELECT * FROM regions WHERE chrom = 'chr1'
)
SELECT f.chrom, f.start, f.ref, f.alt
FROM filtered_variants f
JOIN chr1_regions r ON f.start BETWEEN r.start AND r.end
```

## 将SQL与间隔操作相结合

SQL查询返回可直接与polars-bio间隔一起使用的LazyFrame操作：

```python
import polars_bio as pb

# Register files
pb.register_vcf("samples.vcf.gz", name="variants")
pb.register_bed("target_regions.bed", name="targets")

# SQL to filter (returns LazyFrame)
high_qual = pb.sql("SELECT chrom, start, end FROM variants WHERE qual > 30").collect()
targets = pb.sql("SELECT chrom, start, end FROM targets WHERE chrom = 'chr1'").collect()

# Interval operation on SQL results
overlapping = pb.overlap(high_qual, targets).collect()
```

## 示例工作流程

### 变异密度分析

```python
import polars_bio as pb

pb.register_vcf("cohort.vcf.gz", name="variants")
pb.register_bed("genome_windows_1mb.bed", name="windows")

# Count variants per window using SQL
result = pb.sql("""
    SELECT w.chrom, w.start, w.end, COUNT(v.start) as variant_count
    FROM windows w
    LEFT JOIN variants v ON w.chrom = v.chrom
        AND v.start >= w.start
        AND v.start < w.end
    GROUP BY w.chrom, w.start, w.end
    ORDER BY variant_count DESC
""").collect()
```

### 基因注释查找

```python
import polars_bio as pb

pb.register_gff("gencode.gff3", name="genes")

# Find all protein-coding genes on chromosome 1
coding_genes = pb.sql("""
    SELECT chrom, start, end, attributes
    FROM genes
    WHERE type = 'gene'
        AND chrom = 'chr1'
        AND attributes LIKE '%protein_coding%'
    ORDER BY start
""").collect()
```
