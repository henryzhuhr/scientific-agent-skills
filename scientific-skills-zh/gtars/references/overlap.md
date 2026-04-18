# 重叠检测和 IGD

重叠模块使用集成基因组数据库 (IGD)数据结构提供基因组间隔之间的高效重叠检测。

## IGD 索引

IGD（集成基因组数据库）是用于快速基因组间隔查询和重叠检测的专用数据结构。

### 构建 IGD 索引

从基因组区域创建索引文件：

```python
import gtars

# Build IGD index from BED file
igd = gtars.igd.build_index("regions.bed")

# Save index for reuse
igd.save("regions.igd")

# Load existing index
igd = gtars.igd.load_index("regions.igd")
```

#### 查询重叠

高效查找重叠区域：

```python
# Query a single region
overlaps = igd.query("chr1", 1000, 2000)

# Query multiple regions
results = []
for chrom, start, end in query_regions:
    overlaps = igd.query(chrom, start, end)
    results.append(overlaps)

# Get overlap counts only
count = igd.count_overlaps("chr1", 1000, 2000)
```

## CLI用法

重叠器命令行工具提供重叠检测：

```bash
# Find overlaps between two BED files
gtars overlaprs query --index regions.bed --query query_regions.bed

# Count overlaps
gtars overlaprs count --index regions.bed --query query_regions.bed

# Output overlapping regions
gtars overlaprs overlap --index regions.bed --query query_regions.bed --output overlaps.bed
```

### IGD CLI 命令

构建和查询 IGD 索引：

```bash
# Build IGD index
gtars igd build --input regions.bed --output regions.igd

# Query IGD index
gtars igd query --index regions.igd --region "chr1:1000-2000"

# Batch query from file
gtars igd query --index regions.igd --query-file queries.bed --output results.bed
```

## Python API

### 重叠检测

计算区域之间的重叠集合：

```python
import gtars

# Load two region sets
set_a = gtars.RegionSet.from_bed("regions_a.bed")
set_b = gtars.RegionSet.from_bed("regions_b.bed")

# Find overlaps
overlaps = set_a.overlap(set_b)

# Get regions from A that overlap with B
overlapping_a = set_a.filter_overlapping(set_b)

# Get regions from A that don't overlap with B
non_overlapping_a = set_a.filter_non_overlapping(set_b)
```

### 重叠统计

计算重叠指标：

```python
# Count overlaps
overlap_count = set_a.count_overlaps(set_b)

# Calculate overlap fraction
overlap_fraction = set_a.overlap_fraction(set_b)

# Get overlap coverage
coverage = set_a.overlap_coverage(set_b)
```

## 性能特征

IGD提供高效查询：
- **索引构建**：O(n log n)其中 n 是区域数量
- **查询时间**：O(k + log n)，其中 k 是重叠数量
- **内存效率**：基因组间隔的紧凑表示

## 使用案例

### 调节元素分析

识别基因组之间的重叠特征：

```python
# Find transcription factor binding sites overlapping promoters
tfbs = gtars.RegionSet.from_bed("chip_seq_peaks.bed")
promoters = gtars.RegionSet.from_bed("promoters.bed")

overlapping_tfbs = tfbs.filter_overlapping(promoters)
print(f"Found {len(overlapping_tfbs)} TFBS in promoters")
```

### 变体注释

对具有重叠特征的变体进行注释：

```python
# Check which variants overlap with coding regions
variants = gtars.RegionSet.from_bed("variants.bed")
cds = gtars.RegionSet.from_bed("coding_sequences.bed")

coding_variants = variants.filter_overlapping(cds)
```

### 染色质状态分析

比较染色质状态样品：

```python
# Find regions with consistent chromatin states
sample1 = gtars.RegionSet.from_bed("sample1_peaks.bed")
sample2 = gtars.RegionSet.from_bed("sample2_peaks.bed")

consistent_regions = sample1.overlap(sample2)
```
