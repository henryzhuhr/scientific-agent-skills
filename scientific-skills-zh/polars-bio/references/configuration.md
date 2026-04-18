# 配置

## 概述

polars-bio使用基于`set_option`和`get_option`的全局配置系统来控制执行行为、坐标系、并行度和流模式。

## set_option / get_option

```python
import polars_bio as pb

# Set a configuration option
pb.set_option("datafusion.execution.target_partitions", 8)

# Get current value
value = pb.get_option("datafusion.execution.target_partitions")
```

## 并行性

### DataFusion Target Partitions

控制并行执行分区的数量。默认为 1（单线程）。

```python
import os
import polars_bio as pb

# Use all available CPU cores
pb.set_option("datafusion.execution.target_partitions", os.cpu_count())

# Set specific number of partitions
pb.set_option("datafusion.execution.target_partitions", 8)
```

* *何时增加并行度：**
- 处理大文件 (>1GB)
- 在数百万个间隔上运行间隔操作
- 批量处理多个染色体

* *何时保持默认值(1):**
- 小数据集
- 内存受限环境
- 调试（确定性执行）

## 坐标系

polars-bio 默认为基于 1 的坐标（标准基因组约定）。

### 全局坐标System

```python
import polars_bio as pb

# Switch to 0-based half-open coordinates
pb.set_option("coordinate_system", "0-based")

# Switch back to 1-based (default)
pb.set_option("coordinate_system", "1-based")

# Check current setting
print(pb.get_option("coordinate_system"))
```

### 通过 I/O 函数覆盖每个文件

I/O 函数接受 `use_zero_based` 以在生成的 DataFrame 上设置坐标元数据：

```python
# Read with explicit 0-based metadata
df = pb.read_bed("regions.bed", use_zero_based=True)
```

* *注意：** 间隔操作（重叠、最近等）执行**不**接受`use_zero_based`。它们从 DataFrame 中读取坐标元数据，该元数据由 I/O 函数或全局选项设置。使用手动构建的 DataFrame 时，polars-bio 会警告丢失元数据并回退到全局设置。

### 在手动 DataFrame 上设置元数据

```python
import polars_bio as pb

# Set coordinate metadata on a manually created DataFrame
pb.set_source_metadata(df, format="bed", path="")
```

### 文件格式约定

|格式|原生坐标系 | polars-bio 转换|
|--------|--------------------------|----------------------|
|床 | 0基础半开放|读取时转换为配置系统 |
| VCF| 1 为基础 |读取时转换为配置系统 |
| GFF/GTF | 1 为基础 |读取时转换为配置系统 |
| BAM/SAM |从 0 开始 |读取时转换为配置系统 |

## 流执行模式

polars-bio 支持两种核外处理的流模式：

### DataFusion Streaming

对于间隔操作默认启用。通过DataFusion执行引擎批量处理数据。

```python
# DataFusion streaming is automatic for interval operations
result = pb.overlap(lf1, lf2)  # Streams if inputs are LazyFrames
```

### Polars Streaming

使用Polars的原生流进行后处理操作：

```python
# Collect with Polars streaming
result = lf.collect(streaming=True)
```

### 组合两者都是

```python
import polars_bio as pb

# Scan files lazily (DataFusion streaming for I/O)
lf1 = pb.scan_bed("large1.bed")
lf2 = pb.scan_bed("large2.bed")

# Interval operation (DataFusion streaming)
result_lf = pb.overlap(lf1, lf2)

# Collect with Polars streaming for final materialization
result = result_lf.collect(streaming=True)
```

## Logging

控制调试日志的详细程度：

```python
import polars_bio as pb

# Set log level
pb.set_loglevel("debug")   # Detailed execution info
pb.set_loglevel("info")    # Standard messages
pb.set_loglevel("warn")    # Warnings only (default)
```

* *注意：**只有`"debug"`、`"info"`和`"warn"`是有效日志level.

## 元数据管理

polars-bio 将坐标系和源元数据附加到 I/O 函数生成的 DataFrame 上。该元数据由区间操作用来确定坐标系。

```python
import polars_bio as pb

# Inspect metadata on a DataFrame
metadata = pb.get_metadata(df)

# Print metadata summary
pb.print_metadata_summary(df)

# Print metadata as JSON
pb.print_metadata_json(df)

# Set metadata on a manually created DataFrame
pb.set_source_metadata(df, format="bed", path="regions.bed")

# Register a DataFrame as a SQL table
pb.from_polars("my_table", df)
```

## 完整配置参考

|选项 |默认|描述 |
|--------|---------|------------|
| `datafusion.execution.target_partitions` | `1` |并行执行分区数量|
| `coordinate_system` | `"1-based"` |默认坐标系（`"0-based"` 或 `"1-based"`）|
