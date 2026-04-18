---
name: gtars
description: 用于 Rust 与 Python 绑定的基因组区间分析的高性能工具包。在处理基因组区域、BED 文件、覆盖轨迹、重叠检测、ML 模型标记化或计算基因组学和机器学习应用程序中的片段分析时使用。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Gtars：Rust 中的基因组工具和算法

## 概述

Gtars 是一个高性能 Rust 工具包，用于操作、分析和处理基因组区间数据。它提供了用于重叠检测、覆盖分析、机器学习标记化和参考序列管理的专用工具。

在处理以下内容时使用此技能：
- 基因组间隔文件（BED格式）
- 基因组区域之间的重叠检测
- 覆盖轨迹生成（WIG、BigWig）
- 基因组ML预处理和标记化
- 单细胞基因组学中的片段分析
- 参考序列检索和验证

## 安装

### Python 安装

安装gtars Python 绑定：

```bash
uv uv pip install gtars
```

### CLI安装

安装命令行工具（需要Rust/Cargo）：

```bash
# Install with all features
cargo install gtars-cli --features "uniwig overlaprs igd bbcache scoring fragsplit"

# Or install specific features only
cargo install gtars-cli --features "uniwig overlaprs"
```

### Rust Library

添加到Rust项目的Cargo.toml：

```toml
[dependencies]
gtars = { version = "0.1", features = ["tokenizers", "overlaprs"] }
```

## 核心功能

Gtars被组织成专门的模块，每个模块专注于特定的基因组分析任务：

### 1.重叠检测和 IGD 索引

使用集成基因组数据库 (IGD)数据结构高效检测基因组区间之间的重叠。

* *何时使用：**
- 查找重叠的调控元件
- 变体注释
- 比较ChIP-seq峰
- 识别共享基因组特征

* *简单示例：**
```python
import gtars

# Build IGD index and query overlaps
igd = gtars.igd.build_index("regions.bed")
overlaps = igd.query("chr1", 1000, 2000)
```

有关全面的重叠检测文档，请参阅`references/overlap.md`。

### 2.覆盖跟踪Generation

使用uniwig模块从测序数据生成覆盖轨迹。

* *何时使用：**
- ATAC-seq可访问性配置文件
- ChIP-seq覆盖可视化
- RNA-seq读取覆盖
- 差异覆盖分析

* *快速示例：**
```bash
# Generate BigWig coverage track
gtars uniwig generate --input fragments.bed --output coverage.bw --format bigwig
```

 有关详细的覆盖率分析工作流程，请参阅 `references/coverage.md`。

### 3. 基因组标记化

将基因组区域转换为机器学习应用的离散标记，特别是基因组数据上的深度学习模型。

* *何时使用：**
- 基因组ML模型的预处理
- 与geniml库集成
- 创建位置编码
- 在基因组序列上训练变压器模型

* *快速示例：**
```python
from gtars.tokenizers import TreeTokenizer

tokenizer = TreeTokenizer.from_bed_file("training_regions.bed")
token = tokenizer.tokenize("chr1", 1000, 2000)
```

有关标记化文档，请参阅 `references/tokenizers.md`。

### 4. 参考序列管理

H按照 GA4GH refget 协议处理参考基因组序列并计算摘要。

* *何时使用：**
- 验证参考基因组完整性
- 提取特定基因组序列
- 计算序列消化
- 交叉参考比较

* *简单示例：**
```python
# Load reference and extract sequences
store = gtars.RefgetStore.from_fasta("hg38.fa")
sequence = store.get_subsequence("chr1", 1000, 2000)
```

参考序列操作参见`references/refget.md`。

### 5.片段处理

分割和分析片段文件，对单细胞基因组数据特别有用。

* *何时使用：**
- 处理单细胞ATAC-seq数据
- 通过细胞条形码分割片段
- 基于簇的片段分析
- 片段质量control

* *简单示例：**
```bash
# Split fragments by clusters
gtars fragsplit cluster-split --input fragments.tsv --clusters clusters.txt --output-dir ./by_cluster/
```

有关片段处理命令，请参阅 `references/cli.md`。

### 6. 片段评分

评分片段与参考数据集的重叠。

* *何时使用：**
- 评估片段富集
- 比较实验数据与参考
- 质量指标计算
- 跨样本批量评分

* *简单示例：**
```bash
# Score fragments against reference
gtars scoring score --fragments fragments.bed --reference reference.bed --output scores.txt
```

## 常见工作流程

### 工作流程 1：峰重叠分析

识别重叠的基因组特征：

```python
import gtars

# Load two region sets
peaks = gtars.RegionSet.from_bed("chip_peaks.bed")
promoters = gtars.RegionSet.from_bed("promoters.bed")

# Find overlaps
overlapping_peaks = peaks.filter_overlapping(promoters)

# Export results
overlapping_peaks.to_bed("peaks_in_promoters.bed")
```

### 工作流程 2：覆盖追踪管道

生成覆盖追踪可视化：

```bash
# Step 1: Generate coverage
gtars uniwig generate --input atac_fragments.bed --output coverage.wig --resolution 10

# Step 2: Convert to BigWig for genome browsers
gtars uniwig generate --input atac_fragments.bed --output coverage.bw --format bigwig
```

### 工作流程 3：ML 预处理

为机器学习准备基因组数据：

```python
from gtars.tokenizers import TreeTokenizer
import gtars

# Step 1: Load training regions
regions = gtars.RegionSet.from_bed("training_peaks.bed")

# Step 2: Create tokenizer
tokenizer = TreeTokenizer.from_bed_file("training_peaks.bed")

# Step 3: Tokenize regions
tokens = [tokenizer.tokenize(r.chromosome, r.start, r.end) for r in regions]

# Step 4: Use tokens in ML pipeline
# (integrate with geniml or custom models)
```

## Python 与 CLI 用法

* *在以下情况下使用 Python API：**
- 与分析管道集成
- 需要编程控制
- 使用 NumPy/Pandas
- 构建自定义工作流程

* *在以下情况下使用 CLI：**
- 快速一次性分析
- Shell脚本
- 批量处理文件
- 原型工作流程

## 参考文档

全面的模块文档：

- **`references/python-api.md`** - 包含RegionSet 操作、NumPy 集成和数据导出的完整Python API 参考
- **`references/overlap.md`** - IGD 索引、重叠检测和设置操作
- **`references/coverage.md`** - 使用 uniwig
- **`references/tokenizers.md`** - ML 应用的基因组标记化
- **`references/refget.md`** - 参考序列管理和摘要
- 生成覆盖轨迹**`references/cli.md`** - 命令行界面完整参考

## 与 geniml

Gtars 集成作为 geniml Python 包的基础，为机器学习工作流程提供核心基因组间隔操作。在处理 geniml 相关任务时，使用 gtars 进行数据预处理和标记化。

## 性能特征

- **原生 Rust 性能**：内存开销低的快速执行
- **并行处理**：大型数据集的多线程操作
- **内存效率**：流式传输和内存映射文件支持
- **零复制操作**：NumPy 集成与最少的数据复制

## 数据格式

Gtars 适用于标准基因组格式：

- **BED**：基因组间隔（3 列或扩展）
- **WIG/BigWig**：覆盖范围Track
- **FASTA**：参考序列
- **片段 TSV**：带有条形码的单细胞片段文件

## 错误处理和调试

启用详细日志记录故障排除：

```python
import gtars

# Enable debug logging
gtars.set_log_level("DEBUG")
```

```bash
# CLI verbose mode
gtars --verbose <command>
```
