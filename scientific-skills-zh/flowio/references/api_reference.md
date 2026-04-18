# FlowIO API 参考

## 概述

FlowIO 是一个用于读写流式细胞术标准 (FCS)文件的 Python 库。它支持 FCS 版本 2.0、3.0 和 3.1，具有最小的依赖性。

## 安装

```bash
pip install flowio
```

 支持 Python 3.9 及更高版本。

## 核心类

### FlowData

使用 FCS 的主要类files.

#### 构造函数

```python
FlowData(fcs_file,
         ignore_offset_error=False,
         ignore_offset_discrepancy=False,
         use_header_offsets=False,
         only_text=False,
         nextdata_offset=None,
         null_channel_list=None)
```

* *参数：**
- `fcs_file`：文件路径（str）、路径对象或文件句柄
- `ignore_offset_error`（bool）：忽略偏移错误（默认： False)
- `ignore_offset_discrepancy` (bool)：忽略 HEADER 和 TEXT 部分之间的偏移差异（默认值：False）
- `use_header_offsets` (bool)：使用 HEADER 部分偏移量而不是 TEXT 部分（默认值：False）
- `only_text` (bool)：仅解析TEXT段，跳过DATA和ANALYSIS（默认：False）
- `nextdata_offset`（int）：读取多数据集文件的字节偏移
- `null_channel_list`（list）：要排除的空通道的PnN标签列表

#### 属性

* *文件信息：**
- `name`：FCS 文件的名称
- `file_size`：文件大小（以字节为单位）
- `version`：FCS 版本（例如，'3.0'、'3.1'）
- `header`：包含HEADER段信息的字典
- `data_type`：数据格式类型（'I'，'F'，'D'，'A'）

* *通道信息：**
- `channel_count`：数据集中的通道数
- `channels`：将通道编号映射到通道信息的字典
- `pnn_labels`：PnN（短通道名称）标签列表
- `pns_labels`：PnS（描述性染色名称）标签列表
- `pnr_values`：每个通道的PnR（范围）值列表通道
- `fluoro_indices`：荧光通道索引列表
- `scatter_indices`：散射通道索引列表
- `time_index`：时间通道索引（或无）
- `null_channels`：空通道列表指数

* *事件数据：**
- `event_count`：数据集中的事件数（行）
- `events`：原始事件数据（字节）

  * *元数据：**
- `text`：TEXT 段键值对字典
- `analysis`：ANALYSIS 段键值对字典（如果存在）

#### 方法

##### as_array()

```python
as_array(preprocess=True)
```

 以 2-D NumPy 数组形式返回事件数据。

* *参数：**
- `preprocess`（布尔）：应用增益、对数和时间缩放变换（默认值：True）

* *返回：**
- 形状为（event_count， channel_count)

* *示例:**
```python
flow_data = FlowData('sample.fcs')
events_array = flow_data.as_array()  # Preprocessed data
raw_array = flow_data.as_array(preprocess=False)  # Raw data
```

##### write_fcs()

```python
write_fcs(filename, metadata=None)
```

将 FlowData 实例导出为新的 FCS file.

* *参数：**
- `filename` (str): 输出文件路径
- `metadata` (dict): 可选的TEXT段关键字字典添加/更新

* *示例：**
```python
flow_data = FlowData('sample.fcs')
flow_data.write_fcs('output.fcs', metadata={'$SRC': 'Modified data'})
```

* *注意：**导出为带有单精度浮点数据的FCS 3.1。

## 实用函数

### read_multiple_data_sets()

```python
read_multiple_data_sets(fcs_file,
                        ignore_offset_error=False,
                        ignore_offset_discrepancy=False,
                        use_header_offsets=False)
```

从包含多个数据集的FCS文件中读取所有数据集。

* *参数：**
- 与FlowData构造函数相同（除了`nextdata_offset`)

* *返回：**
- FlowData 实例列表，每个数据集一个 

* *示例：**
```python
from flowio import read_multiple_data_sets

datasets = read_multiple_data_sets('multi_dataset.fcs')
print(f"Found {len(datasets)} datasets")
for i, dataset in enumerate(datasets):
    print(f"Dataset {i}: {dataset.event_count} events")
```

### create_fcs()

```python
create_fcs(filename,
           event_data,
           channel_names,
           opt_channel_names=None,
           metadata=None)
```

从事件数据创建一个新的FCS文件。

* *参数：**
- `filename` (str): 输出文件路径
- `event_data` (ndarray): 2-D NumPy事件数据数组（行=事件，列=通道）
- `channel_names`（列表）：PnN（短）通道名称列表
- `opt_channel_names`（列表）：PnS（描述性）通道名称的可选列表
- `metadata`（字典）：TEXT段的可选字典关键字

* *示例：**
```python
import numpy as np
from flowio import create_fcs

# Create synthetic data
events = np.random.rand(10000, 5)
channels = ['FSC-A', 'SSC-A', 'FL1-A', 'FL2-A', 'Time']
opt_channels = ['Forward Scatter', 'Side Scatter', 'FITC', 'PE', 'Time']

create_fcs('synthetic.fcs',
           events,
           channels,
           opt_channel_names=opt_channels,
           metadata={'$SRC': 'Synthetic data'})
```

## 异常类

### FlowIOWarning

非严重问题的通用警告类。

### PnEWarning

创建 FCS 文件期间 PnE 值无效时引发警告。

### FlowIOException

FlowIO 错误的基本异常类。

### FCSParsingError

在解析 FCS 文件时出现问题时引发。

### DataOffsetDiscrepancyError

Raished当 HEADER 和 TEXT 部分为数据段提供不同的字节偏移量时。

* *解决方法：** 创建 FlowData 实例时使用 `ignore_offset_discrepancy=True` 参数。

### MultipleDataSetsError

在尝试使用标准 FlowData 构造函数读取包含多个数据集的文件时引发。

* *解决方案：** 使用 `read_multiple_data_sets()` 函数

## FCS 文件结构参考

FCS 文件由四个段组成：

1. **HEADER**：包含FCS版本和其他段
2的字节位置。 **TEXT**：键值元数据对（分隔格式）
3. **数据**：原始事件数据（二进制、浮点或 ASCII）
4. **ANALYSIS**（可选）：数据处理结果

### 通用文本段关键字

- `$BEGINDATA`、`$ENDDATA`：DATA 段的字节偏移
- `$BEGINANALYSIS`、`$ENDANALYSIS`：ANALYSIS 的字节偏移段
- `$BYTEORD`：字节顺序（小端为1,2,3,4；大端为4,3,2,1）
- `$DATATYPE`：数据类型（'I'=整数，'F'=浮点，'D'=双精度，'A'=ASCII）
- `$MODE`：数据模式（'L'=列表模式，最常见） 
- `$NEXTDATA`：到下一个数据集的偏移量（如果是单个数据集，则为 0） 
- `$PAR`：参数数量（通道） 
- `$TOT`：参数总数events
- `PnN`：参数 n
- `PnS`：参数 n
- `PnR` 的描述性染色名称：参数 n
- 的范围（最大值） `PnE`：参数 n 的放大指数（格式： "a,b" 其中值 = a * 10^(b*x))
- `PnG`：参数 n

## 通道类型

的放大增益FlowIO自动对通道进行分类：

- **散射通道**：FSC（前向散射）、SSC（侧向散射） 
- **荧光通道**：FL1、FL2、FITC、PE等 
- **时间通道**：通常标记为“时间”

访问索引via：
- `flow_data.scatter_indices`
- `flow_data.fluoro_indices`
- `flow_data.time_index`

## 数据预处理

调用`as_array(preprocess=True)`时，FlowIO适用：

1. **增益缩放**：乘以 PnG 值
2. **对数变换**：如果存在
3，则应用PnE指数变换。 **时间缩放**：将时间值转换为适当的单位

要访问原始的、未处理的数据：`as_array(preprocess=False)`

## 最佳实践

1. **内存效率**：仅需要元数据时使用`only_text=True`
2. **错误处理**：将文件操作包装在 FCSParsingError
3 的 try- except 块中。 **多数据集文件**：如果不确定数据集计数
4，请始终使用`read_multiple_data_sets()`。 **偏移问题**：如果遇到偏移错误，请尝试 `ignore_offset_discrepancy=True`
5. **通道选择**：在解析过程中使用 null_channel_list 排除不需要的通道

## 与 FlowKit 集成

对于高级流式细胞术分析（包括补偿、门控和 GatingML 支持），请考虑将 FlowKit 库与 FlowIO 一起使用。 FlowKit 提供了构建在 FlowIO 的文件解析功能之上的更高级别的抽象。

## 示例工作流程

### 基本文件读取

```python
from flowio import FlowData

# Read FCS file
flow = FlowData('experiment.fcs')

# Print basic info
print(f"Version: {flow.version}")
print(f"Events: {flow.event_count}")
print(f"Channels: {flow.channel_count}")
print(f"Channel names: {flow.pnn_labels}")

# Get event data
events = flow.as_array()
print(f"Data shape: {events.shape}")
```

### 元数据提取

```python
from flowio import FlowData

flow = FlowData('sample.fcs', only_text=True)

# Access metadata
print(f"Acquisition date: {flow.text.get('$DATE', 'N/A')}")
print(f"Instrument: {flow.text.get('$CYT', 'N/A')}")

# Channel information
for i, (pnn, pns) in enumerate(zip(flow.pnn_labels, flow.pns_labels)):
    print(f"Channel {i}: {pnn} ({pns})")
```

### 创建新的FCS 文件

```python
import numpy as np
from flowio import create_fcs

# Generate or process data
data = np.random.rand(5000, 3) * 1000

# Define channels
channels = ['FSC-A', 'SSC-A', 'FL1-A']
stains = ['Forward Scatter', 'Side Scatter', 'GFP']

# Create FCS file
create_fcs('output.fcs',
           data,
           channels,
           opt_channel_names=stains,
           metadata={
               '$SRC': 'Python script',
               '$DATE': '19-OCT-2025'
           })
```

### 处理多数据集文件

```python
from flowio import read_multiple_data_sets

# Read all datasets
datasets = read_multiple_data_sets('multi.fcs')

# Process each dataset
for i, dataset in enumerate(datasets):
    print(f"\nDataset {i}:")
    print(f"  Events: {dataset.event_count}")
    print(f"  Channels: {dataset.pnn_labels}")

    # Get data array
    events = dataset.as_array()
    mean_values = events.mean(axis=0)
    print(f"  Mean values: {mean_values}")
```

### 修改和再导出

```python
from flowio import FlowData

# Read original file
flow = FlowData('original.fcs')

# Get event data
events = flow.as_array(preprocess=False)

# Modify data (example: apply custom transformation)
events[:, 0] = events[:, 0] * 1.5  # Scale first channel

# Note: Currently, FlowIO doesn't support direct modification of event data
# For modifications, use create_fcs() instead:
from flowio import create_fcs

create_fcs('modified.fcs',
           events,
           flow.pnn_labels,
           opt_channel_names=flow.pns_labels,
           metadata=flow.text)
```
