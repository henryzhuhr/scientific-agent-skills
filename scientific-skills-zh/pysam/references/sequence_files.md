# 使用序列文件 (FASTA/FASTQ)

## FASTA 文件

### 概述

Pysam 提供 `FastaFile` 类，用于对 FASTA 参考序列进行索引随机访问。 FASTA 文件在使用前必须用 `samtools faidx` 建立索引。

### Opening FASTA Files

```python
import pysam

# Open indexed FASTA file
fasta = pysam.FastaFile("reference.fasta")

# Automatically looks for reference.fasta.fai index
```

### 创建 FASTA Index

```python
# Create index using pysam
pysam.faidx("reference.fasta")

# Or using samtools command
pysam.samtools.faidx("reference.fasta")
```

 这将创建随机所需的 `.fai` 索引文件access.

### FastaFile 属性

```python
fasta = pysam.FastaFile("reference.fasta")

# List of reference sequences
references = fasta.references
print(f"References: {references}")

# Get lengths
lengths = fasta.lengths
print(f"Lengths: {lengths}")

# Get specific sequence length
chr1_length = fasta.get_reference_length("chr1")
```

### 获取序列

#### 按区域获取

使用**0 基础，半开放**坐标：

```python
# Fetch specific region
sequence = fasta.fetch("chr1", 1000, 2000)
print(f"Sequence: {sequence}")  # Returns 1000 bases

# Fetch entire chromosome
chr1_seq = fasta.fetch("chr1")

# Fetch using region string (1-based)
sequence = fasta.fetch(region="chr1:1001-2000")
```

* *重要：**数字参数使用基于 0 的坐标，区域字符串使用基于 1 的坐标（samtools 约定）。

#### 常见用例

```python
# Get sequence at variant position
def get_variant_context(fasta, chrom, pos, window=10):
    """Get sequence context around a variant position (1-based)."""
    start = max(0, pos - window - 1)  # Convert to 0-based
    end = pos + window
    return fasta.fetch(chrom, start, end)

# Get sequence for gene coordinates
def get_gene_sequence(fasta, chrom, start, end, strand):
    """Get gene sequence with strand awareness."""
    seq = fasta.fetch(chrom, start, end)

    if strand == "-":
        # Reverse complement
        complement = str.maketrans("ATGCatgc", "TACGtacg")
        seq = seq.translate(complement)[::-1]

    return seq

# Check reference allele
def check_ref_allele(fasta, chrom, pos, expected_ref):
    """Verify reference allele at position (1-based pos)."""
    actual = fasta.fetch(chrom, pos-1, pos)  # Convert to 0-based
    return actual.upper() == expected_ref.upper()
```

### 提取多个区域

```python
# Extract multiple regions efficiently
regions = [
    ("chr1", 1000, 2000),
    ("chr1", 5000, 6000),
    ("chr2", 10000, 11000)
]

sequences = {}
for chrom, start, end in regions:
    seq_id = f"{chrom}:{start}-{end}"
    sequences[seq_id] = fasta.fetch(chrom, start, end)
```

### 使用模糊碱基

FASTA 文件可能包含 IUPAC 模糊代码：

- N = 任何碱基
- R = A 或 G（嘌呤）
- Y = C 或 T (嘧啶)
- S = G 或 C (强)
- W = A 或 T (弱)
- K = G 或 T (酮)
- M = A 或 C (氨基)
- B = C、G 或 T（非 A）
- D = A、G 或T（非 C）
- H = A、C 或 T（非 G）
- V = A、C 或 G（非 T）

```python
# Handle ambiguous bases
def count_ambiguous(sequence):
    """Count non-ATGC bases."""
    return sum(1 for base in sequence.upper() if base not in "ATGC")

# Remove regions with too many Ns
def has_quality_sequence(fasta, chrom, start, end, max_n_frac=0.1):
    """Check if region has acceptable N content."""
    seq = fasta.fetch(chrom, start, end)
    n_count = seq.upper().count('N')
    return (n_count / len(seq)) <= max_n_frac
```

## FASTQ 文件

### 概述

Pysam 提供 `FastxFile`（或`FastqFile`）用于读取包含带有质量分数的原始测序读数的 FASTQ 文件。 FASTQ 文件不支持随机访问 - 仅顺序读取。

### 打开 FASTQ 文件

```python
import pysam

# Open FASTQ file
fastq = pysam.FastxFile("reads.fastq")

# Works with compressed files
fastq_gz = pysam.FastxFile("reads.fastq.gz")
```

### 读取 FASTQ 记录

```python
fastq = pysam.FastxFile("reads.fastq")

for read in fastq:
    print(f"Name: {read.name}")
    print(f"Sequence: {read.sequence}")
    print(f"Quality: {read.quality}")
    print(f"Comment: {read.comment}")  # Optional header comment
```

* *FastqProxy 属性：**
- `name` - 读取标识符（无 @ 前缀）
- `sequence` - DNA/RNA 序列
- `quality` - ASCII 编码的质量字符串
- `comment` - 标题行中的可选注释
- `get_quality_array()` - 将质量字符串转换为数值数组

### 质量得分转换

```python
# Convert quality string to numeric values
for read in fastq:
    qual_array = read.get_quality_array()
    mean_quality = sum(qual_array) / len(qual_array)
    print(f"{read.name}: mean Q = {mean_quality:.1f}")
```

质量分数按 Phred 缩放（通常为 Phred+33 编码）：
- Q = -10 * log10(P_error)
- ASCII 33 ('!') = Q0
- ASCII 43 ('+') = Q10
- ASCII 63 ('?') = Q30

### 常用 FASTQ 处理工作流程

#### 质量过滤

```python
def filter_by_quality(input_fastq, output_fastq, min_mean_quality=20):
    """Filter reads by mean quality score."""
    with pysam.FastxFile(input_fastq) as infile:
        with open(output_fastq, 'w') as outfile:
            for read in infile:
                qual_array = read.get_quality_array()
                mean_q = sum(qual_array) / len(qual_array)

                if mean_q >= min_mean_quality:
                    # Write in FASTQ format
                    outfile.write(f"@{read.name}\n")
                    outfile.write(f"{read.sequence}\n")
                    outfile.write("+\n")
                    outfile.write(f"{read.quality}\n")
```

#### 长度过滤

```python
def filter_by_length(input_fastq, output_fastq, min_length=50):
    """Filter reads by minimum length."""
    with pysam.FastxFile(input_fastq) as infile:
        with open(output_fastq, 'w') as outfile:
            kept = 0
            for read in infile:
                if len(read.sequence) >= min_length:
                    outfile.write(f"@{read.name}\n")
                    outfile.write(f"{read.sequence}\n")
                    outfile.write("+\n")
                    outfile.write(f"{read.quality}\n")
                    kept += 1
    print(f"Kept {kept} reads")
```

#### 计算质量统计数据

```python
def calculate_fastq_stats(fastq_file):
    """Calculate basic statistics for FASTQ file."""
    total_reads = 0
    total_bases = 0
    quality_sum = 0

    with pysam.FastxFile(fastq_file) as fastq:
        for read in fastq:
            total_reads += 1
            read_length = len(read.sequence)
            total_bases += read_length

            qual_array = read.get_quality_array()
            quality_sum += sum(qual_array)

    return {
        "total_reads": total_reads,
        "total_bases": total_bases,
        "mean_read_length": total_bases / total_reads if total_reads > 0 else 0,
        "mean_quality": quality_sum / total_bases if total_bases > 0 else 0
    }
```

#### 按名称提取读取

```python
def extract_reads_by_name(fastq_file, read_names, output_file):
    """Extract specific reads by name."""
    read_set = set(read_names)

    with pysam.FastxFile(fastq_file) as infile:
        with open(output_file, 'w') as outfile:
            for read in infile:
                if read.name in read_set:
                    outfile.write(f"@{read.name}\n")
                    outfile.write(f"{read.sequence}\n")
                    outfile.write("+\n")
                    outfile.write(f"{read.quality}\n")
```

#### 将 FASTQ 转换为 FASTA

```python
def fastq_to_fasta(fastq_file, fasta_file):
    """Convert FASTQ to FASTA (discards quality scores)."""
    with pysam.FastxFile(fastq_file) as infile:
        with open(fasta_file, 'w') as outfile:
            for read in infile:
                outfile.write(f">{read.name}\n")
                outfile.write(f"{read.sequence}\n")
```

#### 子样本FASTQ

```python
import random

def subsample_fastq(input_fastq, output_fastq, fraction=0.1, seed=42):
    """Randomly subsample reads from FASTQ file."""
    random.seed(seed)

    with pysam.FastxFile(input_fastq) as infile:
        with open(output_fastq, 'w') as outfile:
            for read in infile:
                if random.random() < fraction:
                    outfile.write(f"@{read.name}\n")
                    outfile.write(f"{read.sequence}\n")
                    outfile.write("+\n")
                    outfile.write(f"{read.quality}\n")
```

## Tabix 索引文件

### 概述

Pysam 提供 `TabixFile` 用于访问 tabix 索引的基因组数据文件（BED、GFF、GTF、通用制表符分隔）。

### 打开 Tabix文件

```python
import pysam

# Open tabix-indexed file
tabix = pysam.TabixFile("annotations.bed.gz")

# File must be bgzip-compressed and tabix-indexed
```

### 创建 Tabix 索引

```python
# Index a file
pysam.tabix_index("annotations.bed", preset="bed", force=True)
# Creates annotations.bed.gz and annotations.bed.gz.tbi

# Presets available: bed, gff, vcf
```

### 获取记录

```python
tabix = pysam.TabixFile("annotations.bed.gz")

# Fetch region
for row in tabix.fetch("chr1", 1000000, 2000000):
    print(row)  # Returns tab-delimited string

# Parse with specific parser
for row in tabix.fetch("chr1", 1000000, 2000000, parser=pysam.asBed()):
    print(f"Interval: {row.contig}:{row.start}-{row.end}")

# Available parsers: asBed(), asGTF(), asVCF(), asTuple()
```

### 使用 BED文件

```python
bed = pysam.TabixFile("regions.bed.gz")

# Access BED fields by name
for interval in bed.fetch("chr1", 1000000, 2000000, parser=pysam.asBed()):
    print(f"Region: {interval.contig}:{interval.start}-{interval.end}")
    print(f"Name: {interval.name}")
    print(f"Score: {interval.score}")
    print(f"Strand: {interval.strand}")
```

### 使用GTF/GFF 文件

```python
gtf = pysam.TabixFile("annotations.gtf.gz")

# Access GTF fields
for feature in gtf.fetch("chr1", 1000000, 2000000, parser=pysam.asGTF()):
    print(f"Feature: {feature.feature}")
    print(f"Gene: {feature.gene_id}")
    print(f"Transcript: {feature.transcript_id}")
    print(f"Coordinates: {feature.start}-{feature.end}")
```

## 性能提示

### FASTA
1. **始终使用索引 FASTA** 文件（使用 samtools faidx 创建 .fai）
2. **提取多个区域时的批量获取操作**
3. **将频繁访问的序列缓存在内存中
4. **使用适当的窗口大小**以避免加载过多的序列数据

### FASTQ
1. **流处理** - FASTQ 文件按顺序读取，动态处理 
2. **使用压缩的FASTQ.gz*​​以节省磁盘空间（pysam透明处理）
3. **避免将整个文件**加载到内存中——逐个读取
4. **对于大文件**，请考虑使用文件分割进行并行处理

### Tabix
1. **始终在区域查询之前使用 bgzip 和 tabix-index** 文件
2. **创建索引时使用适当的预设**
3. **为命名字段访问指定解析器**
4. **对同一文件进行批量查询**以避免重新打开

## 常见陷阱

1. **FASTA坐标系：** fetch()使用从0开始的坐标，区域字符串使用从1开始的
2. **缺少索引：** FASTA 随机访问需要 .fai 索引文件
3. **仅限 FASTQ 顺序：** 无法在 FASTQ
4 上执行随机访问或基于区域的查询。 **质量编码：**除非另有说明，否则假设 Phred+33 
5. **Tabix 压缩：** 必须使用 bgzip，而不是常规 gzip，用于 tabix 索引 
6. **解析器要求：** TabixFile 需要显式解析器来访问命名字段
7. **区分大小写：** FASTA 序列保留大小写 — 使用 .upper()或 .lower()进行一致比较
