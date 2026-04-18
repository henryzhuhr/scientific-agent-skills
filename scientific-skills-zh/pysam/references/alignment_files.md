# 使用比对文件（SAM/BAM/CRAM）

## 概述

Pysam 提供 `AlignmentFile` 类，用于读写包含比对序列数据的 SAM/BAM/CRAM 格式文件。 BAM/CRAM 文件支持通过索引进行压缩和随机访问。

## 打开对齐文件

通过模式限定符指定格式：
- `"rb"` - 读取 BAM（二进制）
- `"r"` - 读取 SAM（文本）
- `"rc"` -读取 CRAM（压缩）
- `"wb"` - 写入 BAM
- `"w"` - 写入 SAM
- `"wc"` - 写入 CRAM

```python
import pysam

# Reading
samfile = pysam.AlignmentFile("example.bam", "rb")

# Writing (requires template or header)
outfile = pysam.AlignmentFile("output.bam", "wb", template=samfile)
```

### 流处理

使用`"-"` 作为 stdin/stdout 操作的文件名：

```python
# Read from stdin
infile = pysam.AlignmentFile('-', 'rb')

# Write to stdout
outfile = pysam.AlignmentFile('-', 'w', template=infile)
```

* *重要：** Pysam 不支持从真正的 Python 文件对象读取/写入 - 仅支持 stdin/stdout 流。

## AlignmentFile Properties

* *标头信息：**
- `references` - 染色体/重叠群名称列表
- `lengths` - 每个参考的相应长度
- `header` - 作为字典的完整标头

```python
samfile = pysam.AlignmentFile("example.bam", "rb")
print(f"References: {samfile.references}")
print(f"Lengths: {samfile.lengths}")
```

## 阅读Reads

### fetch() - 基于区域的检索

使用**基于0的坐标**检索读取重叠的指定基因组区域。

```python
# Fetch specific region
for read in samfile.fetch("chr1", 1000, 2000):
    print(read.query_name, read.reference_start)

# Fetch entire contig
for read in samfile.fetch("chr1"):
    print(read.query_name)

# Fetch without index (sequential read)
for read in samfile.fetch(until_eof=True):
    print(read.query_name)
```

* *重要说明：**
- 需要索引（.bai/.crai）进行随机access
- 返回与区域**重叠**的读取（可能超出边界）
- 对非索引文件或顺序读取使用`until_eof=True`
- 默认情况下，仅返回映射读取
- 对于未映射读取，使用`fetch("*")`或`until_eof=True`

### 多个迭代器

当在同一文件上使用多个迭代器时：

```python
samfile = pysam.AlignmentFile("example.bam", "rb", multiple_iterators=True)
iter1 = samfile.fetch("chr1", 1000, 2000)
iter2 = samfile.fetch("chr2", 5000, 6000)
```

 如果没有 `multiple_iterators=True`，新的 fetch()调用会重新定位文件指针并中断现有迭代器。

### count() - 计数区域中的读取次数

```python
# Count all reads
num_reads = samfile.count("chr1", 1000, 2000)

# Count with quality filter
num_quality_reads = samfile.count("chr1", 1000, 2000, quality=20)
```

### count_coverage() - 每个碱基覆盖率

返回四个数组（A、C、G、T），每个碱基覆盖率：

```python
coverage = samfile.count_coverage("chr1", 1000, 2000)
a_counts, c_counts, g_counts, t_counts = coverage
```

## AlignedSegment 对象

E 每次读取都表示为具有以下关键属性的 `AlignedSegment` 对象：

### 读取信息
- `query_name` - 读取名称/ID
- `query_sequence` - 读取序列（碱基）
- `query_qualities` - 碱基质量分数（ASCII 编码）
- `query_length` - 读取长度

### 映射信息
- `reference_name` - 染色体/重叠群名称
- `reference_start` - 起始位置（从 0 开始，包含）
- `reference_end` - 结束位置（从 0 开始，不包含）
- `mapping_quality` - MAPQ 分数
- `cigarstring` - CIGAR 字符串（例如， "100M")
- `cigartuples` - CIGAR 作为（操作、长度）元组列表

* *重要：** `cigartuples` 格式与 SAM 规范不同。操作均为整数：
- 0 = M（匹配/不匹配）
- 1 = I（插入）
- 2 = D（删除）
- 3 = N（跳过参考）
- 4 = S（软剪辑）
- 5 = H（硬剪辑）裁剪）
- 6 = P（填充）
- 7 = =（序列匹配）
- 8 = X（序列不匹配）

### 标志和状态
- `flag` - SAM 标志为整数
- `is_paired` - 是否配对读取？
- `is_proper_pair` - 是否以正确的配对方式读取？
- `is_unmapped` - 是否读取未映射？
- `mate_is_unmapped` - 配对是否未映射？
- `is_reverse` - 在反向链上读取吗？
- `mate_is_reverse` - 在反向链上配对吗？
- `is_read1` - 这是读取 1 吗？
- `is_read2` - 这是读取 2 吗？
- `is_secondary` -是否是辅助对齐？
- `is_qcfail` - QC 读取是否失败？
- `is_duplicate` - 是否读取重复内容？
- `is_supplementary` - 是否是补充对齐？

### 标签和可选字段
- `get_tag(tag)` - 获取可选字段的值
- `set_tag(tag, value)` - 设置可选字段
- `has_tag(tag)` - 检查标签是否存在
- `get_tags()` - 获取所有标签作为列表tuples

```python
for read in samfile.fetch("chr1", 1000, 2000):
    if read.has_tag("NM"):
        edit_distance = read.get_tag("NM")
        print(f"{read.query_name}: NM={edit_distance}")
```

## 写入对齐文件

### 创建标头

```python
header = {
    'HD': {'VN': '1.0'},
    'SQ': [
        {'LN': 1575, 'SN': 'chr1'},
        {'LN': 1584, 'SN': 'chr2'}
    ]
}

outfile = pysam.AlignmentFile("output.bam", "wb", header=header)
```

### 创建AlignedSegment对象

```python
# Create new read
a = pysam.AlignedSegment()
a.query_name = "read001"
a.query_sequence = "AGCTTAGCTAGCTACCTATATCTTGGTCTTGGCCG"
a.flag = 0
a.reference_id = 0  # Index into header['SQ']
a.reference_start = 100
a.mapping_quality = 20
a.cigar = [(0, 35)]  # 35M
a.query_qualities = pysam.qualitystring_to_array("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")

# Write to file
outfile.write(a)
```

### 格式之间的转换

```python
# BAM to SAM
infile = pysam.AlignmentFile("input.bam", "rb")
outfile = pysam.AlignmentFile("output.sam", "w", template=infile)
for read in infile:
    outfile.write(read)
infile.close()
outfile.close()
```

## 堆积分析

`pileup()` 方法提供跨区域的**列**（逐位置）分析区域：

```python
for pileupcolumn in samfile.pileup("chr1", 1000, 2000):
    print(f"Position {pileupcolumn.pos}: coverage = {pileupcolumn.nsegments}")

    for pileupread in pileupcolumn.pileups:
        if not pileupread.is_del and not pileupread.is_refskip:
            # Query position is the position in the read
            base = pileupread.alignment.query_sequence[pileupread.query_position]
            print(f"  {pileupread.alignment.query_name}: {base}")
```

* *关键属性：**
- `pileupcolumn.pos` - 基于0的参考位置
- `pileupcolumn.nsegments` - 覆盖位置的读取数
- `pileupread.alignment` - 对齐的段object
- `pileupread.query_position` - 读取中的位置（无删除）
- `pileupread.is_del` - 这是删除吗？
- `pileupread.is_refskip` - 这是引用跳过（CIGAR 中的 N）吗？

  * *重要：** 保持迭代器引用处于活动状态。当迭代器过早超出范围时，会出现“迭代器完成后访问 PileupProxy ”错误。

## 坐标系

* *严重：** Pysam 使用 **从 0 开始的半开**坐标（Python 约定）：
- `reference_start` 是从 0 开始的（第一个基是0)
- `reference_end` 是独占的（不包含在范围内）
- 1000-2000 的区域包括基数 1000-1999

* *例外：** `fetch()` 和 `pileup()` 中的区域字符串遵循 samtools 约定（基于1）：
```python
# These are equivalent:
samfile.fetch("chr1", 999, 2000)  # Python style: 0-based
samfile.fetch("chr1:1000-2000")   # samtools style: 1-based
```

## 索引

创建BAM索引：
```python
pysam.index("example.bam")
```

或使用命令行界面：
```python
pysam.samtools.index("example.bam")
```

## 性能提示

1. **重复查询特定区域时使用索引访问**
2. **使用`pileup()`进行按列分析**而不是重复的获取操作
3. **使用 `fetch(until_eof=True)` 顺序读取**非索引文件 
4. **避免多个迭代器**除非必要（性能成本）
5. **使用`count()`进行简单计数**而不是手动迭代计数

## 常见陷阱

1. **部分重叠：** `fetch()` 返回重叠区域边界的读数 - 如果需要精确边界，则实施显式过滤
2. **质量分数编辑：**修改`query_sequence`后无法就地编辑`query_qualities`。先创建一个副本：`quals = read.query_qualities`
3. **缺少索引：**没有`until_eof=True`的`fetch()`需要索引文件
4. **线程安全性：**虽然pysam在I/O期间释放GIL，但全面的线程安全性尚未得到充分验证
5. **迭代器范围：** 保持堆积迭代器引用处于活动状态，以避免“迭代器完成后访问 PileupProxy”错误
