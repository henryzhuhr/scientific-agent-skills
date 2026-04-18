# 使用 Bio.Seq 和 Bio.SeqIO

进行序列处理## 概述

Bio.Seq 通过专门的方法为生物序列提供了 `Seq` 对象，而 Bio.SeqIO 则提供了用于跨多种格式读取、写入和转换序列文件的统一接口。

## Seq 对象

### 创建序列

```python
from Bio.Seq import Seq

# Create a basic sequence
my_seq = Seq("AGTACACTGGT")

# Sequences support string-like operations
print(len(my_seq))  # Length
print(my_seq[0:5])  # Slicing
```

### 核心序列操作

```python
# Complement and reverse complement
complement = my_seq.complement()
rev_comp = my_seq.reverse_complement()

# Transcription (DNA to RNA)
rna = my_seq.transcribe()

# Translation (to protein)
protein = my_seq.translate()

# Back-transcription (RNA to DNA)
dna = rna_seq.back_transcribe()
```

### 序列方法

- `complement()` - 返回互补链
- `reverse_complement()` - 返回反向补体
- `transcribe()` - DNA到RNA转录
- `back_transcribe()` - RNA到DNA转换
- `translate()` - 翻译为蛋白质序列
- `translate(table=N)` - 使用特定遗传密码表
- `translate(to_stop=True)` - 在第一个停止 codon

## Bio.SeqIO：序列文件 I/O

### 核心功能

* *Bio.SeqIO.parse()**：作为 `SeqRecord` 迭代器读取序列文件的主要主力objects.

```python
from Bio import SeqIO

# Parse a FASTA file
for record in SeqIO.parse("sequences.fasta", "fasta"):
    print(record.id)
    print(record.seq)
    print(len(record))
```

* *Bio.SeqIO.read()**：对于单记录文件（验证是否存在一条记录）。

```python
record = SeqIO.read("single.fasta", "fasta")
```

* *Bio.SeqIO.write()**：将SeqRecord对象输出到files.

```python
# Write records to file
count = SeqIO.write(seq_records, "output.fasta", "fasta")
print(f"Wrote {count} records")
```

* *Bio.SeqIO.convert()**：简化格式转换。

```python
# Convert between formats
count = SeqIO.convert("input.gbk", "genbank", "output.fasta", "fasta")
```

### 支持的文件格式

常见格式包括：
- **fasta** - FASTA格式
- **fastq** - FASTQ 格式（带质量分数）
- **genbank** 或 **gb** - GenBank 格式
- **embl** - EMBL 格式
- **swiss** - SwissProt 格式
- **fasta-2line** - FASTA 上有序列line
- **制表符** - 简单制表符分隔格式

### SeqRecord 对象

`SeqRecord` 对象将序列数据与注释结合起来：

```python
record.id          # Primary identifier
record.name        # Short name
record.description # Description line
record.seq         # The actual sequence (Seq object)
record.annotations # Dictionary of additional info
record.features    # List of SeqFeature objects
record.letter_annotations  # Per-letter annotations (e.g., quality scores)
```

### 修改记录

```python
# Modify record attributes
record.id = "new_id"
record.description = "New description"

# Extract subsequences
sub_record = record[10:30]  # Slicing preserves annotations

# Modify sequence
record.seq = record.seq.reverse_complement()
```

## 处理大文件

### 内存高效解析

使用迭代器避免将整个文件加载到内存中：

```python
# Good for large files
for record in SeqIO.parse("large_file.fasta", "fasta"):
    if len(record.seq) > 1000:
        print(record.id)
```

### 基于字典接入

随机接入的三种方式：

* *1. Bio.SeqIO.to_dict()** - 将所有记录加载到内存中：

```python
seq_dict = SeqIO.to_dict(SeqIO.parse("sequences.fasta", "fasta"))
record = seq_dict["sequence_id"]
```

* *2。 Bio.SeqIO.index()** - 延迟加载字典（内存高效）：

```python
seq_index = SeqIO.index("sequences.fasta", "fasta")
record = seq_index["sequence_id"]
seq_index.close()
```

* *3。 Bio.SeqIO.index_db()** - 基于 SQLite 的超大文件索引：

```python
seq_index = SeqIO.index_db("index.idx", "sequences.fasta", "fasta")
record = seq_index["sequence_id"]
seq_index.close()
```

### 用于高性能的低级解析器

对于高通量测序数据，请使用返回元组的低级解析器而不是对象：

```python
from Bio.SeqIO.FastaIO import SimpleFastaParser

with open("sequences.fasta") as handle:
    for title, sequence in SimpleFastaParser(handle):
        print(title, len(sequence))

from Bio.SeqIO.QualityIO import FastqGeneralIterator

with open("reads.fastq") as handle:
    for title, sequence, quality in FastqGeneralIterator(handle):
        print(title)
```

## 压缩文件

Bio.SeqIO自动处理压缩文件：

```python
# Works with gzip compression
for record in SeqIO.parse("sequences.fasta.gz", "fasta"):
    print(record.id)

# BGZF format for random access
from Bio import bgzf
with bgzf.open("sequences.fasta.bgz", "r") as handle:
    records = SeqIO.parse(handle, "fasta")
```

## 数据提取模式

### 提取特定信息

```python
# Get all IDs
ids = [record.id for record in SeqIO.parse("file.fasta", "fasta")]

# Get sequences above length threshold
long_seqs = [record for record in SeqIO.parse("file.fasta", "fasta")
             if len(record.seq) > 500]

# Extract organism from GenBank
for record in SeqIO.parse("file.gbk", "genbank"):
    organism = record.annotations.get("organism", "Unknown")
    print(f"{record.id}: {organism}")
```

### 过滤和写入

```python
# Filter sequences by criteria
long_sequences = (record for record in SeqIO.parse("input.fasta", "fasta")
                  if len(record) > 500)
SeqIO.write(long_sequences, "filtered.fasta", "fasta")
```

## 最佳实践

1. **对大文件使用迭代器**，而不是将所有内容加载到内存中
2. **优先使用index()**来重复随机访问大文件
3. **对于数百万条记录或多文件场景使用index_db()**
4. **当速度至关重要时，对高吞吐量数据使用低级解析器**
5. **下载一次，本地重复使用**而不是重复网络访问
6. **显式关闭索引文件**或使用上下文管理器
7. **在使用 SeqIO.write()
8 写入之前验证输入**。 **使用适当的格式字符串** - 始终小写（例如，“fasta”，而不是“FASTA”）

## 常见用例

### 格式转换

```python
# GenBank to FASTA
SeqIO.convert("input.gbk", "genbank", "output.fasta", "fasta")

# Multiple format conversion
for fmt in ["fasta", "genbank", "embl"]:
    SeqIO.convert("input.fasta", "fasta", f"output.{fmt}", fmt)
```

### 质量过滤(FASTQ)

```python
from Bio import SeqIO

good_reads = (record for record in SeqIO.parse("reads.fastq", "fastq")
              if min(record.letter_annotations["phred_quality"]) >= 20)
count = SeqIO.write(good_reads, "filtered.fastq", "fastq")
```

### 序列统计

```python
from Bio.SeqUtils import gc_fraction

for record in SeqIO.parse("sequences.fasta", "fasta"):
    gc = gc_fraction(record.seq)
    print(f"{record.id}: GC={gc:.2%}, Length={len(record)}")
```

### 以编程方式创建记录

```python
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

# Create a new record
new_record = SeqRecord(
    Seq("ATGCGATCGATCG"),
    id="seq001",
    name="MySequence",
    description="Test sequence"
)

# Write to file
SeqIO.write([new_record], "new.fasta", "fasta")
```
