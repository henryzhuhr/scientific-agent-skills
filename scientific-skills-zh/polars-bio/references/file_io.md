# 生物信息学文件 I/O

## 概述

polars-bio 提供常见生物信息学格式的 `read_*`、`scan_*`、`write_*` 和 `sink_*` 函数。 `read_*` 将数据急切地加载到 DataFrame 中，而 `scan_*` 创建一个 LazyFrame 用于流/核外处理。 `write_*` 从 DataFrame/LazyFrame 写入并返回行计数，而 `sink_*` 从 LazyFrame 进行流式传输。

## 支持的格式

|格式|阅读 |扫描|注册 (SQL) |写|水槽 |
|--------|-----|------|------------------|--------|------|
|床 | `read_bed` | `scan_bed` | `register_bed` | — | — |
| VCF| `read_vcf` | `scan_vcf` | `register_vcf` | `write_vcf` | `sink_vcf` |
|巴姆| `read_bam` | `scan_bam` | `register_bam` | `write_bam` | `sink_bam` |
|补习班 | `read_cram` | `scan_cram` | `register_cram` | `write_cram` | `sink_cram` |
| GFF | `read_gff` | `scan_gff` | `register_gff` | — | — |
| GTF | `read_gtf` | `scan_gtf` | `register_gtf` | — | — |
|法斯塔 | `read_fasta` | `scan_fasta` | — | — | — |
|快问 | `read_fastq` | `scan_fastq` | `register_fastq` | `write_fastq` | `sink_fastq` |
|萨姆 | `read_sam` | `scan_sam` | `register_sam` | `write_sam` | `sink_sam` |
| Hi-C 对 | `read_pairs` | `scan_pairs` | `register_pairs` | — | — |
|通用表| `read_table` | `scan_table` | — | — | — |

## 常见云/IO 参数

所有 `read_*` 和 `scan_*` 函数共享这些参数（而不是单个 `storage_options` 字典）：

|参数|类型 |默认|描述 |
|-----------|------|---------|------------|
| `path` | STR |必填|文件路径（本地、S3、GCS、Azure）|
| `chunk_size` |整数 | `8` |并行读取的块数|
| `concurrent_fetches` |整数 | `1` |云存储并发获取数量|
| `allow_anonymous` |布尔 | `True` |允许匿名访问云存储|
| `enable_request_payer` |布尔 | `False` |启用云存储请求者付费 |
| `max_retries` |整数 | `5` |云操作的最大重试次数 |
| `timeout` |整数 | `300` |云操作超时（以秒为单位）|
| `compression_type` | STR | `"auto"` |压缩类型（从扩展自动检测）|
| `projection_pushdown` |布尔 | `True` |启用投影下推优化|
| `use_zero_based` |布尔 | `None` |设置坐标系元数据（无=使用全局设置）|

并非所有函数都支持所有参数。 SAM 函数缺少云参数。 FASTA/FASTQ缺少`predicate_pushdown`.

## BED格式

### read_bed / scan_bed

读取BED文件。自动检测色谱柱（BED3 到 BED12）。 BED文件使用从0开始的半开坐标； polars-bio 自动附加坐标元数据。

```python
import polars_bio as pb

# Eager read
df = pb.read_bed("regions.bed")

# Lazy scan
lf = pb.scan_bed("regions.bed")
```

### 列架构 (BED3)

|专栏 |类型 |描述|
|--------|------|-------------|
| `chrom` |字符串|染色体名称 |
| `start` | Int64 |起始位置|
| `end` | Int64 |结束位置|

扩展BED字段（自动检测）添加：`name`、`score`、`strand`、`thickStart`、`thickEnd`、`itemRgb`、`blockCount`、`blockSizes`、 `blockStarts`.

## VCF格式

### read_vcf / scan_vcf

读取VCF/BCF文件。支持`.vcf`、`.vcf.gz`、`.bcf`.

```python
import polars_bio as pb

# Read VCF
df = pb.read_vcf("variants.vcf.gz")

# Read with specific INFO and FORMAT fields extracted as columns
df = pb.read_vcf("variants.vcf.gz", info_fields=["AF", "DP"], format_fields=["GT", "GQ"])

# Read specific samples
df = pb.read_vcf("variants.vcf.gz", samples=["SAMPLE1", "SAMPLE2"])
```

### 附加参数

|参数|类型 |默认|描述 |
|-----------|------|---------|------------|
| `info_fields` |列表[str] | `None` |要提取为列的 INFO 字段 |
| `format_fields` |列表[str] | `None` |要提取为列的格式字段 |
| `samples` |列表[str] | `None` |样品包括|
| `predicate_pushdown` |布尔 | `True` |启用谓词下推 |

### 列架构

|专栏 |类型 |描述|
|--------|------|-------------|
| `chrom` |字符串|染色体|
| `start` | UInt32 |起始位置 |
| `end` | UInt32 |结束位置|
| `id` |字符串|变体 ID |
| `ref` |字符串|参考等位基因|
| `alt` |字符串|替代等位基因 |
| `qual` |浮点32 |质量得分|
| `filter` |字符串|过滤器状态|
| `info` |字符串| INFO 字段（原始，除非指定 `info_fields`）|

### write_vcf / sink_vcf

```python
import polars_bio as pb

# Write DataFrame to VCF
rows_written = pb.write_vcf(df, "output.vcf")

# Stream LazyFrame to VCF
pb.sink_vcf(lf, "output.vcf")
```

## BAM 格式

### read_bam / scan_bam

从 BAM 文件中读取对齐的测序读数。需要 `.bai` 索引文件。

```python
import polars_bio as pb

# Read BAM
df = pb.read_bam("aligned.bam")

# Scan BAM (streaming)
lf = pb.scan_bam("aligned.bam")

# Read with specific tags
df = pb.read_bam("aligned.bam", tag_fields=["NM", "MD"])
```

### 附加参数

|参数|类型 |默认|描述 |
|---------|------|---------|-------------|
| `tag_fields` |列表[str] | `None` |要提取为列的 SAM 标签 |
| `predicate_pushdown` |布尔 | `True` |启用谓词下推|
| `infer_tag_types` |布尔 | `True` |从数据推断标签列类型|
| `infer_tag_sample_size` |整数 | `100` |用于类型推断的采样记录数 |
| `tag_type_hints` |列表[str] | `None` |标签的显式类型提示 |

### 列架构

|专栏 |类型 |说明 |
|--------|------|-------------|
| `chrom` |字符串|参考序列名称|
| `start` | Int64 |对齐起始位置|
| `end` | Int64 |对准结束位置|
| `name` |字符串|读取名称|
| `flags` | UInt32 | SAM 标志 |
| `mapping_quality` | UInt32 |测绘质量|
| `cigar` |字符串|雪茄绳|
| `sequence` |字符串|读取序列|
| `quality_scores` |字符串|基础质量线|
| `mate_chrom` |字符串|配合参考名称|
| `mate_start` | Int64 |配合起始位置|
| `template_length` | Int64 |模板长度 |

### write_bam / sink_bam

```python
rows_written = pb.write_bam(df, "output.bam")
rows_written = pb.write_bam(df, "output.bam", sort_on_write=True)

pb.sink_bam(lf, "output.bam")
pb.sink_bam(lf, "output.bam", sort_on_write=True)
```

## CRAM 格式

### read_cram / scan_cram

CRAM 文件具有与 BAM **独立的功能**。需要参考FASTA和`.crai`索引。

```python
import polars_bio as pb

# Read CRAM (reference required)
df = pb.read_cram("aligned.cram", reference_path="reference.fasta")

# Scan CRAM (streaming)
lf = pb.scan_cram("aligned.cram", reference_path="reference.fasta")
```

与BAM相同的附加参数和列模式，加上：

|参数|类型 |默认|描述 |
|---------|------|---------|------------|
| `reference_path` | STR | `None` |参考FASTA的路径 |

### write_cram / sink_cram

```python
rows_written = pb.write_cram(df, "output.cram", reference_path="reference.fasta")
pb.sink_cram(lf, "output.cram", reference_path="reference.fasta")
```

## GFF/GTF Format

### read_gff / scan_gff / read_gtf / scan_gtf

GFF3和GTF有单独的

```python
import polars_bio as pb

# Read GFF3
df = pb.read_gff("annotations.gff3")

# Read GTF
df = pb.read_gtf("genes.gtf")

# Extract specific attributes as columns
df = pb.read_gff("annotations.gff3", attr_fields=["gene_id", "gene_name"])
```

### 附加参数

|参数|类型 |默认|描述|
|---------|------|---------|----------|
| `attr_fields` |列表[str] | `None` |要提取为列的属性字段 |
| `predicate_pushdown` |布尔 | `True` |启用谓词下推 |

### 列架构

|专栏 |类型 |说明 |
|--------|------|-------------|
| `chrom` |字符串|序列名称|
| `source` |字符串|特征来源|
| `type` |字符串|特征类型（基因、外显子等）|
| `start` | Int64 |起始位置 |
| `end` | Int64 |结束位置 |
| `score` |浮点32 |分数|
| `strand` |字符串|绞线 (+/-/.) |
| `phase` | UInt32 |相位（0/1/2）|
| `attributes` |字符串|属性字符串 |

## FASTA 格式

### read_fasta / scan_fasta

从 FASTA 文件中读取参考序列。

```python
import polars_bio as pb

df = pb.read_fasta("reference.fasta")
```

### 列架构

|专栏 |类型 |描述|
|--------|------|-------------|
| `name` |字符串|序列名称|
| `description` |字符串|说明行|
| `sequence` |字符串|核苷酸序列 |

## FASTQ 格式

### read_fastq / scan_fastq

读取带有质量分数的原始测序读数。

```python
import polars_bio as pb

df = pb.read_fastq("reads.fastq.gz")
```

### 列架构

|专栏 |类型 |描述|
|--------|------|-------------|
| `name` |字符串|读取名称 |
| `description` |字符串|说明行|
| `sequence` |字符串|核苷酸序列|
| `quality` |字符串|质量字符串（Phred+33 编码）|

### write_fastq / sink_fastq

```python
rows_written = pb.write_fastq(df, "output.fastq")
pb.sink_fastq(lf, "output.fastq")
```

## SAM 格式

### read_sam / scan_sam

读取文本格式对齐文件。与 BAM 相同的列架构。无云参数。

```python
import polars_bio as pb

df = pb.read_sam("alignments.sam")
```

### 附加参数

|参数|类型 |默认|描述 |
|---------|------|---------|------------|
| `tag_fields` |列表[str] | `None` |要提取的 SAM 标签 |
| `infer_tag_types` |布尔 | `True` |推断标签类型 |
| `infer_tag_sample_size` |整数 | `100` |用于推理的样本大小 |
| `tag_type_hints` |列表[str] | `None` |显式类型提示 |

### write_sam / sink_sam

```python
rows_written = pb.write_sam(df, "output.sam")
pb.sink_sam(lf, "output.sam", sort_on_write=True)
```

## Hi-C Pairs

### read_pairs / scan_pairs

读取 Hi-Cpairs 格式文件以获取染色质接触数据。

```python
import polars_bio as pb

df = pb.read_pairs("contacts.pairs")
lf = pb.scan_pairs("contacts.pairs")
```

### Column架构

|专栏 |类型 |描述|
|--------|------|-------------|
| `readID` |字符串|读取标识符|
| `chrom1` |字符串|第一次接触染色体 |
| `pos1` | Int32 |首次接触位置|
| `chrom2` |字符串|第二接触染色体|
| `pos2` | Int32 |第二个触点位置|
| `strand1` |字符串|第一次接触链 |
| `strand2` |字符串|第二个联系人 |

## 通用表读取器

### read_table / scan_table

使用自定义架构读取制表符分隔的文件。对于非标准格式或与bioframe兼容的表很有用。

```python
import polars_bio as pb

df = pb.read_table("custom.tsv", schema={"chrom": str, "start": int, "end": int, "name": str})
lf = pb.scan_table("custom.tsv", schema={"chrom": str, "start": int, "end": int})
```

## 云存储

所有`read_*`和`scan_*`函数都通过单独的参数支持云存储：

### Amazon S3

```python
df = pb.read_bed(
    "s3://bucket/regions.bed",
    allow_anonymous=False,
    max_retries=10,
    timeout=600,
)
```

### Google Cloud Storage

```python
df = pb.read_vcf("gs://bucket/variants.vcf.gz", allow_anonymous=True)
```

### Azure Blob Storage

```python
df = pb.read_bam("az://container/aligned.bam", allow_anonymous=False)
```

* *注意：** 对于经过身份验证的访问，请通过环境变量或云 SDK 配置来配置凭据（例如，`AWS_ACCESS_KEY_ID`、`GOOGLE_APPLICATION_CREDENTIALS`）。

## 压缩支持

polars-bio 透明地处理压缩文件：

|压缩|扩展|并行减压|
|-------------|-----------|------------------------|
|广州邮编 | `.gz` |否|
| BGZF | `.gz`（带BGZF块）|是 |
|未压缩 | （无）| N/A |

* *建议：** 对于大文件使用 BGZF 压缩（例如，使用 `bgzip` 创建）。 BGZF支持并行块解压缩，与普通GZIP相比显着提高读取性能。

## 描述功能

无需完全读取即可检查文件结构：

```python
import polars_bio as pb

# Describe file schemas and metadata
schema_df = pb.describe_vcf("samples.vcf.gz")
schema_df = pb.describe_bam("aligned.bam")
schema_df = pb.describe_sam("alignments.sam")
schema_df = pb.describe_cram("aligned.cram", reference_path="ref.fasta")
```
