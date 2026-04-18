# 命令行界面

Gtars 为直接从终端进行基因组区间分析提供了全面的 CLI。

## 安装

```bash
# Install with all features
cargo install gtars-cli --features "uniwig overlaprs igd bbcache scoring fragsplit"

# Install specific features only
cargo install gtars-cli --features "uniwig overlaprs"
```

## 全局选项

```bash
# Display help
gtars --help

# Show version
gtars --version

# Verbose output
gtars --verbose <command>

# Quiet mode
gtars --quiet <command>
```

## IGD 命令

构建和查询重叠的IGD 索引检测：

```bash
# Build IGD index
gtars igd build --input regions.bed --output regions.igd

# Query single region
gtars igd query --index regions.igd --region "chr1:1000-2000"

# Query from file
gtars igd query --index regions.igd --query-file queries.bed --output results.bed

# Count overlaps
gtars igd count --index regions.igd --query-file queries.bed
```

## 重叠命令

计算基因组区域集之间的重叠：

```bash
# Find overlapping regions
gtars overlaprs overlap --set-a regions_a.bed --set-b regions_b.bed --output overlaps.bed

# Count overlaps
gtars overlaprs count --set-a regions_a.bed --set-b regions_b.bed

# Filter regions by overlap
gtars overlaprs filter --input regions.bed --filter overlapping.bed --output filtered.bed

# Subtract regions
gtars overlaprs subtract --set-a regions_a.bed --set-b regions_b.bed --output difference.bed
```

## Uniwig 命令

从基因组生成覆盖轨迹间隔：

```bash
# Generate coverage track
gtars uniwig generate --input fragments.bed --output coverage.wig

# Specify resolution
gtars uniwig generate --input fragments.bed --output coverage.wig --resolution 10

# Generate BigWig
gtars uniwig generate --input fragments.bed --output coverage.bw --format bigwig

# Strand-specific coverage
gtars uniwig generate --input fragments.bed --output forward.wig --strand +
```

## BBCache 命令

从 BEDbase.org 缓存和管理 BED 文件：

```bash
# Cache BED file from bedbase
gtars bbcache fetch --id <bedbase_id> --output cached.bed

# List cached files
gtars bbcache list

# Clear cache
gtars bbcache clear

# Update cache
gtars bbcache update
```

## 评分命令

Score 片段与参考重叠数据集：

```bash
# Score fragments
gtars scoring score --fragments fragments.bed --reference reference.bed --output scores.txt

# Batch scoring
gtars scoring batch --fragments-dir ./fragments/ --reference reference.bed --output-dir ./scores/

# Score with weights
gtars scoring score --fragments fragments.bed --reference reference.bed --weights weights.txt --output scores.txt
```

## FragSplit 命令

按细胞条形码或簇分割片段文件：

```bash
# Split by barcode
gtars fragsplit split --input fragments.tsv --barcodes barcodes.txt --output-dir ./split/

# Split by clusters
gtars fragsplit cluster-split --input fragments.tsv --clusters clusters.txt --output-dir ./clustered/

# Filter fragments
gtars fragsplit filter --input fragments.tsv --min-fragments 100 --output filtered.tsv
```

## 常见工作流程

### 工作流程 1：重叠分析管道

```bash
# Step 1: Build IGD index for reference
gtars igd build --input reference_regions.bed --output reference.igd

# Step 2: Query with experimental data
gtars igd query --index reference.igd --query-file experimental.bed --output overlaps.bed

# Step 3: Generate statistics
gtars overlaprs count --set-a experimental.bed --set-b reference_regions.bed
```

### 工作流程2：覆盖轨迹生成

```bash
# Step 1: Generate coverage
gtars uniwig generate --input fragments.bed --output coverage.wig --resolution 10

# Step 2: Convert to BigWig
gtars uniwig generate --input fragments.bed --output coverage.bw --format bigwig
```

### 工作流程3：片段处理

```bash
# Step 1: Filter fragments
gtars fragsplit filter --input raw_fragments.tsv --min-fragments 100 --output filtered.tsv

# Step 2: Split by clusters
gtars fragsplit cluster-split --input filtered.tsv --clusters clusters.txt --output-dir ./by_cluster/

# Step 3: Score against reference
gtars scoring batch --fragments-dir ./by_cluster/ --reference reference.bed --output-dir ./scores/
```

## 输入/输出格式

### BED 格式
标准 3 列或扩展 BED 格式：
```
chr1    1000    2000
chr1    3000    4000
chr2    5000    6000
```

### 片段格式 (TSV)
单单元格制表符分隔格式片段：
```
chr1    1000    2000    BARCODE1
chr1    3000    4000    BARCODE2
chr2    5000    6000    BARCODE1
```

### WIG 格式
覆盖轨道的摆动格式：
```
fixedStep chrom=chr1 start=1000 step=10
12
15
18
```

## 性能选项

```bash
# Set thread count
gtars --threads 8 <command>

# Memory limit
gtars --memory-limit 4G <command>

# Buffer size
gtars --buffer-size 10000 <command>
```

## 错误搬运

```bash
# Continue on errors
gtars --continue-on-error <command>

# Strict mode (fail on warnings)
gtars --strict <command>

# Log to file
gtars --log-file output.log <command>
```
