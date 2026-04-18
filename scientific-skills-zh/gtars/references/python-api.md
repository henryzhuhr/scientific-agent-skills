# Python API参考

gtars Python绑定的综合参考。

## 安装

```bash
# Install gtars Python package
uv pip install gtars

# Or with pip
pip install gtars
```

## 核心类

### RegionSet

管理基因组集合间隔：

```python
import gtars

# Create from BED file
regions = gtars.RegionSet.from_bed("regions.bed")

# Create from coordinates
regions = gtars.RegionSet([
    ("chr1", 1000, 2000),
    ("chr1", 3000, 4000),
    ("chr2", 5000, 6000)
])

# Access regions
for region in regions:
    print(f"{region.chromosome}:{region.start}-{region.end}")

# Get region count
num_regions = len(regions)

# Get total coverage
total_coverage = regions.total_coverage()
```

### 区域操作

对区域集执行操作：

```python
# Sort regions
sorted_regions = regions.sort()

# Merge overlapping regions
merged = regions.merge()

# Filter by size
large_regions = regions.filter_by_size(min_size=1000)

# Filter by chromosome
chr1_regions = regions.filter_by_chromosome("chr1")
```

### 设置操作

对基因组执行设置操作区域：

```python
# Load two region sets
set_a = gtars.RegionSet.from_bed("set_a.bed")
set_b = gtars.RegionSet.from_bed("set_b.bed")

# Union
union = set_a.union(set_b)

# Intersection
intersection = set_a.intersect(set_b)

# Difference
difference = set_a.subtract(set_b)

# Symmetric difference
sym_diff = set_a.symmetric_difference(set_b)
```

## 数据导出

### 写入BED文件

将区域导出为BED格式：

```python
# Write to BED file
regions.to_bed("output.bed")

# Write with scores
regions.to_bed("output.bed", scores=score_array)

# Write with names
regions.to_bed("output.bed", names=name_list)
```

### 格式转换

之间转换格式：

```python
# BED to JSON
regions = gtars.RegionSet.from_bed("input.bed")
regions.to_json("output.json")

# JSON to BED
regions = gtars.RegionSet.from_json("input.json")
regions.to_bed("output.bed")
```

## NumPy 集成

与 NumPy 数组无缝集成：

```python
import numpy as np

# Export to NumPy arrays
starts = regions.starts_array()  # NumPy array of start positions
ends = regions.ends_array()      # NumPy array of end positions
sizes = regions.sizes_array()    # NumPy array of region sizes

# Create from NumPy arrays
chromosomes = ["chr1"] * len(starts)
regions = gtars.RegionSet.from_arrays(chromosomes, starts, ends)
```

## 并行处理

利用大型并行处理数据集：

```python
# Enable parallel processing
regions = gtars.RegionSet.from_bed("large_file.bed", parallel=True)

# Parallel operations
result = regions.parallel_apply(custom_function)
```

## 内存管理

E大型数据集的高效内存使用：

```python
# Stream large BED files
for chunk in gtars.RegionSet.stream_bed("large_file.bed", chunk_size=10000):
    process_chunk(chunk)

# Memory-mapped mode
regions = gtars.RegionSet.from_bed("large_file.bed", mmap=True)
```

## 错误处理

Handle common错误：

```python
try:
    regions = gtars.RegionSet.from_bed("file.bed")
except gtars.FileNotFoundError:
    print("File not found")
except gtars.InvalidFormatError as e:
    print(f"Invalid BED format: {e}")
except gtars.ParseError as e:
    print(f"Parse error at line {e.line}: {e.message}")
```

## 配置

配置gtars行为：

```python
# Set global options
gtars.set_option("parallel.threads", 4)
gtars.set_option("memory.limit", "4GB")
gtars.set_option("warnings.strict", True)

# Context manager for temporary options
with gtars.option_context("parallel.threads", 8):
    # Use 8 threads for this block
    regions = gtars.RegionSet.from_bed("large_file.bed", parallel=True)
```

## 日志记录

启用日志记录调试：

```python
import logging

# Enable gtars logging
gtars.set_log_level("DEBUG")

# Or use Python logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("gtars")
```

## 性能提示

- 对大型数据集使用并行处理
- 为非常大的文件启用内存映射模式
- 尽可能流数据以减少内存使用
- 适用时在操作之前对区域进行预排序
- 使用用于数值计算的 NumPy 数组
- 缓存经常访问的数据
