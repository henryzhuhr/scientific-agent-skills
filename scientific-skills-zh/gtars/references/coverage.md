# 使用 Uniwig

进行覆盖分析 Uniwig 模块从测序数据生成覆盖轨迹，提供基因组间隔到覆盖概况的高效转换。

## 覆盖轨迹生成

从 BED 文件创建覆盖轨迹：

```python
import gtars

# Generate coverage from BED file
coverage = gtars.uniwig.coverage_from_bed("fragments.bed")

# Generate coverage with specific resolution
coverage = gtars.uniwig.coverage_from_bed("fragments.bed", resolution=10)

# Generate strand-specific coverage
fwd_coverage = gtars.uniwig.coverage_from_bed("fragments.bed", strand="+")
rev_coverage = gtars.uniwig.coverage_from_bed("fragments.bed", strand="-")
```

## CLI 用法

从命令生成覆盖轨迹line:

```bash
# Generate coverage track
gtars uniwig generate --input fragments.bed --output coverage.wig

# Specify resolution
gtars uniwig generate --input fragments.bed --output coverage.wig --resolution 10

# Generate BigWig format
gtars uniwig generate --input fragments.bed --output coverage.bw --format bigwig

# Strand-specific coverage
gtars uniwig generate --input fragments.bed --output forward.wig --strand +
gtars uniwig generate --input fragments.bed --output reverse.wig --strand -
```

## 使用覆盖率数据

### 访问覆盖率值

查询特定位置的覆盖率：

```python
# Get coverage at position
cov = coverage.get_coverage("chr1", 1000)

# Get coverage over range
cov_array = coverage.get_coverage_range("chr1", 1000, 2000)

# Get coverage statistics
mean_cov = coverage.mean_coverage("chr1", 1000, 2000)
max_cov = coverage.max_coverage("chr1", 1000, 2000)
```

### 覆盖率操作

对覆盖率执行操作曲目：

```python
# Normalize coverage
normalized = coverage.normalize()

# Smooth coverage
smoothed = coverage.smooth(window_size=10)

# Combine coverage tracks
combined = coverage1.add(coverage2)

# Compute coverage difference
diff = coverage1.subtract(coverage2)
```

## 输出格式

Uniwig 支持多种输出格式：

### WIG 格式

标准摆动格式：
```
fixedStep chrom=chr1 start=1000 step=1
12
15
18
22
...
```

### BigWig格式

用于高效存储和访问的二进制格式：
```bash
# Generate BigWig
gtars uniwig generate --input fragments.bed --output coverage.bw --format bigwig
```

### BedGraph格式

用于变量覆盖的灵活格式：
```
chr1    1000    1001    12
chr1    1001    1002    15
chr1    1002    1003    18
```

## 用例

### ATAC-seq分析

生成染色质可及性特征：

```python
# Generate ATAC-seq coverage
atac_fragments = gtars.RegionSet.from_bed("atac_fragments.bed")
coverage = gtars.uniwig.coverage_from_bed("atac_fragments.bed", resolution=1)

# Identify accessible regions
peaks = coverage.call_peaks(threshold=10)
```

### ChIP-seq Peak Visualization

为 ChIP-seq 数据创建覆盖轨迹：

```bash
# Generate coverage for visualization
gtars uniwig generate --input chip_seq_fragments.bed \
                      --output chip_coverage.bw \
                      --format bigwig
```

### RNA-seq覆盖率

计算RNA-seq的读取覆盖率：

```python
# Generate strand-specific RNA-seq coverage
fwd = gtars.uniwig.coverage_from_bed("rnaseq.bed", strand="+")
rev = gtars.uniwig.coverage_from_bed("rnaseq.bed", strand="-")

# Export for IGV
fwd.to_bigwig("rnaseq_fwd.bw")
rev.to_bigwig("rnaseq_rev.bw")
```

### 差异覆盖率分析

比较样本之间的覆盖率：

```python
# Generate coverage for two samples
control = gtars.uniwig.coverage_from_bed("control.bed")
treatment = gtars.uniwig.coverage_from_bed("treatment.bed")

# Compute fold change
fold_change = treatment.divide(control)

# Find differential regions
diff_regions = fold_change.find_regions(threshold=2.0)
```

## 性能优化

- 对数据使用适当的分辨率scale
- 建议用于大型数据集的 BigWig 格式
- 可用于多个染色体的并行处理
- 适用于大文件的内存高效流
