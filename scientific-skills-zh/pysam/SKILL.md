---
name: pysam
description: 基因组文件工具包。读/写 SAM/BAM/CRAM 比对、VCF/BCF 变体、FASTA/FASTQ 序列、提取区域、计算覆盖率，用于 NGS 数据处理流程。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Pysam

## 概述

Pysam 是一个用于读取、操作和写入基因组数据集的 Python 模块。使用 htslib 的 Pythonic 接口读取/写入 SAM/BAM/CRAM 比对文件、VCF/BCF 变体文件和 FASTA/FASTQ 序列。查询tabix索引文件，执行覆盖率堆积分析，并执行samtools/bcftools命令。

## 何时使用此技能

此技能应在以下情况下使用：
- 使用测序比对文件（BAM/CRAM）
- 分析遗传变异（VCF/BCF）
- 提取参考序列或基因区域
- 处理原始测序数据（FASTQ）
- 计算覆盖度或读取深度
- 实施生物信息学分析流程
- 测序数据的质量控制
- 变异调用和注释工作流程

## 快速入门

### 安装
```bash
uv pip install pysam
```

### 基本示例

* *读取对齐文件：**
```python
import pysam

# Open BAM file and fetch reads in region
samfile = pysam.AlignmentFile("example.bam", "rb")
for read in samfile.fetch("chr1", 1000, 2000):
    print(f"{read.query_name}: {read.reference_start}")
samfile.close()
```

* *读取变体文件：**
```python
# Open VCF file and iterate variants
vcf = pysam.VariantFile("variants.vcf")
for variant in vcf:
    print(f"{variant.chrom}:{variant.pos} {variant.ref}>{variant.alts}")
vcf.close()
```

* *查询参考序列：**
```python
# Open FASTA and extract sequence
fasta = pysam.FastaFile("reference.fasta")
sequence = fasta.fetch("chr1", 1000, 2000)
print(sequence)
fasta.close()
```

## 核心功能

### 1. 比对文件操作（SAM/BAM/CRAM）

使用 `AlignmentFile` 类来处理比对测序读数。这适用于分析映射结果、计算覆盖率、提取读数或质量控制。

* *常见操作：**
- 打开并读取BAM/SAM/CRAM文件
- 从特定基因组区域获取读数
- 通过映射质量、标志或其他标准过滤读数
- 写入过滤或修改比对
- 计算覆盖率统计数据
- 执行堆积分析（逐个碱基覆盖率）
- 访问读取序列、质量分数和比对信息

* *参考：** 请参阅 `references/alignment_files.md` 了解有关以下内容的详细文档：
- 打开和读取对齐文件
- AlignedSegment 属性和方法
- 使用 `fetch()`
- 基于区域的获取 `fetch()`
- 覆盖率的堆积分析 
- 编写和创建 BAM文件
- 坐标系和索引
- 性能优化技巧

### 2. 变体文件操作(VCF/BCF)

使用`VariantFile` 类处理来自变体调用管道的遗传变体。适用于变异分析、过滤、注释或群体遗传学。

* *常用操作：**
- 读写VCF/BCF文件
- 查询特定区域的变异
- 获取变异信息（位置、等位基因、质量）
- 提取样本的基因型数据
- 过滤变异质量、等位基因频率或其他标准
- 使用附加信息注释变体
- 子集样本或区域

* *参考：** 有关详细文档，请参阅 `references/variant_files.md`：
- 打开和读取变体文件
- 变体记录属性和方法
- 访问INFO 和 FORMAT 字段
- 使用基因型和样本
- 创建和写入 VCF 文件
- 过滤和子集变体
- 多样本 VCF 操作

### 3. 序列文件操作 (FASTA/FASTQ)

使用 `FastaFile`用于随机访问参考序列，`FastxFile` 用于读取原始测序数据。这适用于提取基因序列、根据参考验证变异或处理原始读数。

* *常见操作：**
- 通过基因组坐标查询参考序列
- 提取感兴趣的基因或区域的序列
- 读取具有质量分数的FASTQ文件
- 验证变异参考等位基因
- 计算序列统计
- 按质量或长度过滤读数
- 在FASTA和FASTQ格式之间转换

* *参考：** 有关详细文档，请参阅 `references/sequence_files.md`：
- FASTA 文件访问和索引
- 按区域提取序列
- 处理基因的反向互补
- 顺序读取 FASTQ 文件
- 质量得分转换和过滤
- 使用 tabix 索引文件（BED、 GTF, GFF)
- 常见序列处理模式

### 4. 集成生物信息学工作流程

Pysam 擅长集成多种文件类型以进行全面的基因组分析。常见工作流程结合了比对文件、变体文件和参考序列。

* *常见工作流程：**
- 计算特定区域的覆盖统计数据
- 根据比对的读数验证变体
- 用覆盖信息注释变体
- 提取变体位置周围的序列
- 根据多个过滤比对或变体标准
- 生成可视化覆盖率轨迹
- 跨多种数据类型的质量控制

* *参考：** 有关详细示例，请参阅`references/common_workflows.md`：
- 质量控制工作流程（BAM 统计、参考一致性）
- 覆盖率分析（每个碱基覆盖率、低覆盖率检测）
- 变异分析（注释、通过读取支持进行过滤）
- 序列提取（变异上下文、基因序列）
- 读取过滤和子集
- 集成模式（BAM+VCF、VCF+BED 等）
- 复杂工作流程的性能优化

## Key概念

### 坐标系

* *关键：** Pysam 使用 **从 0 开始的半开**坐标（Python 约定）：
- 起始位置是从 0 开始的（第一个基数是位置 0）
- 结束位置是独占的（不包括在范围内）
- 区域1000-2000 包括碱基 1000-1999（总共 1000 个碱基）

* *例外：** `fetch()` 中的区域字符串遵循 samtools 约定（从 1 开始）：
```python
samfile.fetch("chr1", 999, 2000)      # 0-based: positions 999-1999
samfile.fetch("chr1:1000-2000")       # 1-based string: positions 1000-2000
```

 * *VCF 文件：** 在文件格式中使用从 1 开始的坐标，但 `VariantRecord.start` 是从 0 开始的。

### 索引要求

随机访问特定基因组区域需要索引文件：
- **BAM 文件**：需要 `.bai` 索引（使用 `pysam.index()` 创建）
- **CRAM 文件**：需要 `.crai` 索引
- **FASTA 文件**：需要 `.fai` 索引（使用`pysam.faidx()`)
- **VCF.gz 文件**：需要 `.tbi` tabix 索引（使用 `pysam.tabix_index()` 创建）
- **BCF 文件**：需要 `.csi` 索引

 如果没有索引，请使用 `fetch(until_eof=True)` 进行顺序

### 文件模式

打开文件时指定格式：
- `"rb"` - 读取BAM（二进制）
- `"r"` - 读取SAM（文本）
- `"rc"` - 读取CRAM
- `"wb"` - 写入 BAM
- `"w"` - 写入 SAM
- `"wc"` - 写入 CRAM

### 性能注意事项

1. **始终使用索引文件**进行随机访问操作
2. **使用`pileup()`进行按列分析**而不是重复的获取操作
3. **使用`count()`进行计数**而不是手动迭代计数
4. **分析独立基因组区域
5时并行处理区域**。 **明确关闭文件**以释放资源
6. **使用`until_eof=True`**进行顺序处理，无需索引
7. **除非必要，否则避免使用多个迭代器**（如果需要，请使用 `multiple_iterators=True`）

## 常见陷阱

1. **坐标混淆：** 记住不同上下文中基于 0 的系统与基于 1 的系统
2. **缺少索引：** 许多操作需要索引文件 - 首先创建它们
3. **部分重叠：** `fetch()` 返回读取重叠区域边界，而不仅仅是那些完全包含的 
4. **迭代器范围：** 保持堆积迭代器引用处于活动状态，以避免“迭代器完成后访问 PileupProxy”错误
5. **质量分数编辑：**更改`query_sequence`后无法就地修改`query_qualities`——先创建一个副本
6. **流限制：** 流仅支持 stdin/stdout，而不支持任意 Python 文件对象
7. **线程安全：**虽然GIL在I/O期间被释放，但全面的线程安全尚未得到充分验证

## 命令行工具

Pysam提供对samtools和bcftools命令的访问：

```python
# Sort BAM file
pysam.samtools.sort("-o", "sorted.bam", "input.bam")

# Index BAM
pysam.samtools.index("sorted.bam")

# View specific region
pysam.samtools.view("-b", "-o", "region.bam", "input.bam", "chr1:1000-2000")

# BCF tools
pysam.bcftools.view("-O", "z", "-o", "output.vcf.gz", "input.vcf")
```

* *错误处理：**
```python
try:
    pysam.samtools.sort("-o", "output.bam", "input.bam")
except pysam.SamtoolsError as e:
    print(f"Error: {e}")
```

## 资源

### 引用/

每个主要功能的详细文档：

- **alignment_files.md** - SAM / BAM / CRAM操作的完整指南，包括AlignmentFile类，AlignedSegment属性，获取操作，堆积分析和编写对齐

- **variant_files.md** - VCF/BCF 操作的完整指南，包括 VariantFile 类、VariantRecord 属性、基因型处理、INFO/FORMAT 字段和多样本操作

- **sequence_files.md** - FASTA/FASTQ 操作的完整指南，包括 FastaFile 和 FastxFile 类、序列提取、质量评分处理和 tabix 索引文件访问

- **common_workflows.md** - 结合多种文件类型的集成生物信息学工作流程的实际示例，包括质量控制、覆盖分析、变异验证和序列提取

## 获取帮助

有关具体操作的详细信息，请参阅相应的参考文档：

- 使用 BAM 文件或计算覆盖率 → `alignment_files.md`
- 分析变异或基因型 → `variant_files.md`
- 提取序列或处理 FASTQ → `sequence_files.md`
- 集成多种文件类型的复杂工作流程 → `common_workflows.md`

官方文档：https://pysam.readthedocs.io/
