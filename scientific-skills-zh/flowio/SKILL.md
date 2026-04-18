---
name: flowio
description: 解析 FCS（流式细胞术标准）文件 v2.0-3.1。将事件提取为 NumPy 数组，读取元数据/通道，转换为 CSV/DataFrame，用于流式细胞术数据预处理。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# FlowIO：流式细胞术标准文件处理程序

## 概述

FlowIO 是一个轻量级 Python 库，用于读写流式细胞术标准 (FCS)文件。解析 FCS 元数据、提取事件数据并创建具有最小依赖性的新 FCS 文件。该库支持 FCS 版本 2.0、3.0 和 3.1，使其成为后端服务、数据管道和基本细胞计数文件操作的理想选择。

## 何时使用此技能

此技能应在以下情况下使用：

- 需要解析或元数据提取的 FCS 文件
- 需要转换为 NumPy 的流式细胞术数据阵列
- 需要导出为FCS 格式的事件数据
- 需要分离的多数据集FCS 文件
- 通道信息提取（散射、荧光、时间）
- 细胞计数文件验证或检查
- 高级分析前的预处理工作流程

* *相关工具：** 对于包括补偿在内的高级流式细胞术分析，门控和 FlowJo/GatingML 支持，推荐 FlowKit 库作为 FlowIO.

## 安装

```bash
uv pip install flowio
```

 需要 Python 3.9 或更高版本。

## 快速入门

### 基本文件读取

```python
from flowio import FlowData

# Read FCS file
flow_data = FlowData('experiment.fcs')

# Access basic information
print(f"FCS Version: {flow_data.version}")
print(f"Events: {flow_data.event_count}")
print(f"Channels: {flow_data.pnn_labels}")

# Get event data as NumPy array
events = flow_data.as_array()  # Shape: (events, channels)
```

### 创建FCS 文件

```python
import numpy as np
from flowio import create_fcs

# Prepare data
data = np.array([[100, 200, 50], [150, 180, 60]])  # 2 events, 3 channels
channels = ['FSC-A', 'SSC-A', 'FL1-A']

# Create FCS file
create_fcs('output.fcs', data, channels)
```

## 核心工作流程

### 读取和解析FCS 文件

FlowData 类提供读取FCS 的主要接口files.

* *标准读取：**

```python
from flowio import FlowData

# Basic reading
flow = FlowData('sample.fcs')

# Access attributes
version = flow.version              # '3.0', '3.1', etc.
event_count = flow.event_count      # Number of events
channel_count = flow.channel_count  # Number of channels
pnn_labels = flow.pnn_labels        # Short channel names
pns_labels = flow.pns_labels        # Descriptive stain names

# Get event data
events = flow.as_array()            # Preprocessed (gain, log scaling applied)
raw_events = flow.as_array(preprocess=False)  # Raw data
```

* *高效内存元数据读取：**

仅需要元数据（无事件数据）时：

```python
# Only parse TEXT segment, skip DATA and ANALYSIS
flow = FlowData('sample.fcs', only_text=True)

# Access metadata
metadata = flow.text  # Dictionary of TEXT segment keywords
print(metadata.get('$DATE'))  # Acquisition date
print(metadata.get('$CYT'))   # Instrument name
```

* *处理有问题文件：**

一些FCS文件存在偏移差异或错误：

```python
# Ignore offset discrepancies between HEADER and TEXT sections
flow = FlowData('problematic.fcs', ignore_offset_discrepancy=True)

# Use HEADER offsets instead of TEXT offsets
flow = FlowData('problematic.fcs', use_header_offsets=True)

# Ignore offset errors entirely
flow = FlowData('problematic.fcs', ignore_offset_error=True)
```

* *排除空通道：**

```python
# Exclude specific channels during parsing
flow = FlowData('sample.fcs', null_channel_list=['Time', 'Null'])
```

### 提取元数据和通道信息

FCS文件在TEXT中包含丰富的元数据segment.

* *常用元数据关键字：**

```python
flow = FlowData('sample.fcs')

# File-level metadata
text_dict = flow.text
acquisition_date = text_dict.get('$DATE', 'Unknown')
instrument = text_dict.get('$CYT', 'Unknown')
data_type = flow.data_type  # 'I', 'F', 'D', 'A'

# Channel metadata
for i in range(flow.channel_count):
    pnn = flow.pnn_labels[i]      # Short name (e.g., 'FSC-A')
    pns = flow.pns_labels[i]      # Descriptive name (e.g., 'Forward Scatter')
    pnr = flow.pnr_values[i]      # Range/max value
    print(f"Channel {i}: {pnn} ({pns}), Range: {pnr}")
```

* *通道类型标识：**

FlowIO自动对通道进行分类：

```python
# Get indices by channel type
scatter_idx = flow.scatter_indices    # [0, 1] for FSC, SSC
fluoro_idx = flow.fluoro_indices      # [2, 3, 4] for FL channels
time_idx = flow.time_index            # Index of time channel (or None)

# Access specific channel types
events = flow.as_array()
scatter_data = events[:, scatter_idx]
fluorescence_data = events[:, fluoro_idx]
```

* *分析段：**

如果存在，访问处理结果：

```python
if flow.analysis:
    analysis_keywords = flow.analysis  # Dictionary of ANALYSIS keywords
    print(analysis_keywords)
```

### 创建新的FCS文件

从NumPy数组或其他数据源生成FCS文件。

* *基本创建：**

```python
import numpy as np
from flowio import create_fcs

# Create event data (rows=events, columns=channels)
events = np.random.rand(10000, 5) * 1000

# Define channel names
channel_names = ['FSC-A', 'SSC-A', 'FL1-A', 'FL2-A', 'Time']

# Create FCS file
create_fcs('output.fcs', events, channel_names)
```

* *具有描述性通道名称：**

```python
# Add optional descriptive names (PnS)
channel_names = ['FSC-A', 'SSC-A', 'FL1-A', 'FL2-A', 'Time']
descriptive_names = ['Forward Scatter', 'Side Scatter', 'FITC', 'PE', 'Time']

create_fcs('output.fcs',
           events,
           channel_names,
           opt_channel_names=descriptive_names)
```

* *具有自定义元数据：**

```python
# Add TEXT segment metadata
metadata = {
    '$SRC': 'Python script',
    '$DATE': '19-OCT-2025',
    '$CYT': 'Synthetic Instrument',
    '$INST': 'Laboratory A'
}

create_fcs('output.fcs',
           events,
           channel_names,
           opt_channel_names=descriptive_names,
           metadata=metadata)
```

* *注意：** FlowIO 导出为 FCS 3.1 单精度浮点数据。

### 导出修改数据

修改现有的FCS文件并重新导出它们。

* *方法1：使用write_fcs()方法：**

```python
from flowio import FlowData

# Read original file
flow = FlowData('original.fcs')

# Write with updated metadata
flow.write_fcs('modified.fcs', metadata={'$SRC': 'Modified data'})
```

* *方法2：提取、修改和重新创建：**

用于修改事件数据：

```python
from flowio import FlowData, create_fcs

# Read and extract data
flow = FlowData('original.fcs')
events = flow.as_array(preprocess=False)

# Modify event data
events[:, 0] = events[:, 0] * 1.5  # Scale first channel

# Create new FCS file with modified data
create_fcs('modified.fcs',
           events,
           flow.pnn_labels,
           opt_channel_names=flow.pns_labels,
           metadata=flow.text)
```

### 处理多数据集FCS文件

某些FCS文件在单个文件中包含多个数据集。

* *检测多数据集文件：**

```python
from flowio import FlowData, MultipleDataSetsError

try:
    flow = FlowData('sample.fcs')
except MultipleDataSetsError:
    print("File contains multiple datasets")
    # Use read_multiple_data_sets() instead
```

* *读取所有数据集：**

```python
from flowio import read_multiple_data_sets

# Read all datasets from file
datasets = read_multiple_data_sets('multi_dataset.fcs')

print(f"Found {len(datasets)} datasets")

# Process each dataset
for i, dataset in enumerate(datasets):
    print(f"\nDataset {i}:")
    print(f"  Events: {dataset.event_count}")
    print(f"  Channels: {dataset.pnn_labels}")

    # Get event data for this dataset
    events = dataset.as_array()
    print(f"  Shape: {events.shape}")
    print(f"  Mean values: {events.mean(axis=0)}")
```

* *读取特定数据集：**

```python
from flowio import FlowData

# Read first dataset (nextdata_offset=0)
first_dataset = FlowData('multi.fcs', nextdata_offset=0)

# Read second dataset using NEXTDATA offset from first
next_offset = int(first_dataset.text['$NEXTDATA'])
if next_offset > 0:
    second_dataset = FlowData('multi.fcs', nextdata_offset=next_offset)
```

## 数据预处理

FlowIO 在 `preprocess=True`.

* *预处理步骤：**

1 时应用标准 FCS 预处理转换。 **增益缩放：** 将值乘以 PnG（增益）关键字 
2. **对数变换：** 如果存在 
，则应用 PnE 指数变换 - 公式：`value = a * 10^(b * raw_value)`，其中 PnE = "a,b"
3. **时间缩放：**将时间值转换为适当的单位

* *控制预处理：**

```python
# Preprocessed data (default)
preprocessed = flow.as_array(preprocess=True)

# Raw data (no transformations)
raw = flow.as_array(preprocess=False)
```

## 错误处理

H适当处理常见的FlowIO异常。

```python
from flowio import (
    FlowData,
    FCSParsingError,
    DataOffsetDiscrepancyError,
    MultipleDataSetsError
)

try:
    flow = FlowData('sample.fcs')
    events = flow.as_array()

except FCSParsingError as e:
    print(f"Failed to parse FCS file: {e}")
    # Try with relaxed parsing
    flow = FlowData('sample.fcs', ignore_offset_error=True)

except DataOffsetDiscrepancyError as e:
    print(f"Offset discrepancy detected: {e}")
    # Use ignore_offset_discrepancy parameter
    flow = FlowData('sample.fcs', ignore_offset_discrepancy=True)

except MultipleDataSetsError as e:
    print(f"Multiple datasets detected: {e}")
    # Use read_multiple_data_sets instead
    from flowio import read_multiple_data_sets
    datasets = read_multiple_data_sets('sample.fcs')

except Exception as e:
    print(f"Unexpected error: {e}")
```

## 常见用途案例

### 检查FCS文件内容

快速探索FCS文件结构：

```python
from flowio import FlowData

flow = FlowData('unknown.fcs')

print("=" * 50)
print(f"File: {flow.name}")
print(f"Version: {flow.version}")
print(f"Size: {flow.file_size:,} bytes")
print("=" * 50)

print(f"\nEvents: {flow.event_count:,}")
print(f"Channels: {flow.channel_count}")

print("\nChannel Information:")
for i, (pnn, pns) in enumerate(zip(flow.pnn_labels, flow.pns_labels)):
    ch_type = "scatter" if i in flow.scatter_indices else \
              "fluoro" if i in flow.fluoro_indices else \
              "time" if i == flow.time_index else "other"
    print(f"  [{i}] {pnn:10s} | {pns:30s} | {ch_type}")

print("\nKey Metadata:")
for key in ['$DATE', '$BTIM', '$ETIM', '$CYT', '$INST', '$SRC']:
    value = flow.text.get(key, 'N/A')
    print(f"  {key:15s}: {value}")
```

### 批量处理多个文件

处理FCS的一个目录文件：

```python
from pathlib import Path
from flowio import FlowData
import pandas as pd

# Find all FCS files
fcs_files = list(Path('data/').glob('*.fcs'))

# Extract summary information
summaries = []
for fcs_path in fcs_files:
    try:
        flow = FlowData(str(fcs_path), only_text=True)
        summaries.append({
            'filename': fcs_path.name,
            'version': flow.version,
            'events': flow.event_count,
            'channels': flow.channel_count,
            'date': flow.text.get('$DATE', 'N/A')
        })
    except Exception as e:
        print(f"Error processing {fcs_path.name}: {e}")

# Create summary DataFrame
df = pd.DataFrame(summaries)
print(df)
```

### 将 FCS 转换为 CSV

将事件数据导出为 CSV 格式：

```python
from flowio import FlowData
import pandas as pd

# Read FCS file
flow = FlowData('sample.fcs')

# Convert to DataFrame
df = pd.DataFrame(
    flow.as_array(),
    columns=flow.pnn_labels
)

# Add metadata as attributes
df.attrs['fcs_version'] = flow.version
df.attrs['instrument'] = flow.text.get('$CYT', 'Unknown')

# Export to CSV
df.to_csv('output.csv', index=False)
print(f"Exported {len(df)} events to CSV")
```

### 过滤事件并重新导出

应用过滤器并保存过滤后的内容数据：

```python
from flowio import FlowData, create_fcs
import numpy as np

# Read original file
flow = FlowData('sample.fcs')
events = flow.as_array(preprocess=False)

# Apply filtering (example: threshold on first channel)
fsc_idx = 0
threshold = 500
mask = events[:, fsc_idx] > threshold
filtered_events = events[mask]

print(f"Original events: {len(events)}")
print(f"Filtered events: {len(filtered_events)}")

# Create new FCS file with filtered data
create_fcs('filtered.fcs',
           filtered_events,
           flow.pnn_labels,
           opt_channel_names=flow.pns_labels,
           metadata={**flow.text, '$SRC': 'Filtered data'})
```

### 提取特定通道

提取并处理特定通道：

```python
from flowio import FlowData
import numpy as np

flow = FlowData('sample.fcs')
events = flow.as_array()

# Extract fluorescence channels only
fluoro_indices = flow.fluoro_indices
fluoro_data = events[:, fluoro_indices]
fluoro_names = [flow.pnn_labels[i] for i in fluoro_indices]

print(f"Fluorescence channels: {fluoro_names}")
print(f"Shape: {fluoro_data.shape}")

# Calculate statistics per channel
for i, name in enumerate(fluoro_names):
    channel_data = fluoro_data[:, i]
    print(f"\n{name}:")
    print(f"  Mean: {channel_data.mean():.2f}")
    print(f"  Median: {np.median(channel_data):.2f}")
    print(f"  Std Dev: {channel_data.std():.2f}")
```

## 最佳实践

1. **内存效率：** 当不需要事件数据时使用`only_text=True`
2. **错误处理：** 将文件操作包装在 try- except 块中以获得健壮的代码
3. **多数据集检测：** 检查 MultipleDataSetsError 并使用适当的函数 
4. **预处理控制：**根据分析需要显式设置`preprocess`参数
5. **偏移问题：** 如果解析失败，请尝试`ignore_offset_discrepancy=True`参数
6. **通道验证：** 在处理
7 之前验证通道计数和名称是否符合预期。 **元数据保留：**修改文件时，保留原始TEXT段关键字

## 高级主题

### 了解FCS文件结构

FCS文件由四个段组成：

1. **HEADER：** FCS 版本和其他段的字节偏移
2. **文本：** 键值元数据对（分隔符分隔）
3. **数据：** 原始事件数据（二进制/浮点/ASCII 格式）
4. **ANALYSIS**（可选）：数据处理结果

通过 FlowData 属性访问这些段：
- `flow.header` - HEADER 段
- `flow.text` - TEXT 段关键字
- `flow.events` - DATA 段（以字节为单位）
- `flow.analysis` - ANALYSIS 段关键字（如果存在）

### 详细 API 参考

有关包括所有参数、方法、异常和 FCS 关键字参考的综合 API 文档，请查阅详细参考文件：

* *阅读：** `references/api_reference.md`

 参考包括：
- 完整的 FlowData 类文档
- 所有实用函数（read_multiple_data_sets、create_fcs）
- 异常类和处理
- FCS 文件结构详细信息
- 常见 TEXT 段关键字
- 扩展示例工作流程

 在处理复杂的 FCS 操作或遇到异常文件格式时，加载此参考详细指导。

## 集成说明

* *NumPy 数组：** 所有事件数据均以 NumPy ndarrays 形式返回，形状为（事件、通道）

* *Pandas DataFrames：** 轻松转换为 DataFrames 进行分析：
```python
import pandas as pd
df = pd.DataFrame(flow.as_array(), columns=flow.pnn_labels)
```

 * *FlowKit 集成：** 对于高级分析（补偿、门控、FlowJo 支持），请使用基于其构建的 FlowKit 库FlowIO 的解析能力

* *Web 应用程序：** FlowIO 的最小依赖性使其非常适合处理 FCS 上传的 Web 后端服务

## 故障排除

* *问题：**“偏移差异错误”
* *解决方案：**使用 `ignore_offset_discrepancy=True`参数

* *问题：**“多个数据集错误”
* *解决方案：**使用`read_multiple_data_sets()`函数而不是FlowData构造函数

* *问题：**大文件内存不足
* *解决方案：**使用`only_text=True`进行仅元数据操作，或处理中的事件chunks

* *问题：**意外的通道计数
* *解决方案：**检查空通道；使用`null_channel_list`参数排除它们

* *问题：**无法就地修改事件数据
* *解决方案：** FlowIO不支持直接修改；提取数据，修改，然后使用 `create_fcs()` 保存

## 总结

FlowIO 为流式细胞术工作流程提供基本的 FCS 文件处理功能。用它来解析、元数据提取和文件创建。对于简单的文件操作和数据提取，FlowIO 就足够了。对于包括补偿和门控在内的复杂分析，可与 FlowKit 或其他专用工具集成。
