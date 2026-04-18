# PyHealth 数据预处理和处理器

## 概述

PyHealth 提供全面的数据处理实用程序，将原始医疗保健数据转换为模型就绪格式。处理器处理特征提取、序列处理、信号转换和标签准备。

## 处理器基类

所有处理器继承自`Processor`，具有标准接口：

* *关键方法：**
- `__call__()`：转换输入数据
- `get_input_info()`：返回处理后的输入schema
- `get_output_info()`：返回处理后的输出 schema

## 核心处理器类型

### 特征处理器

* *特征处理器** (`FeatureProcessor`)
- 特征提取的基类
- 处理词汇构建
- 嵌入准备
- 特征编码

* *常用操作：**
- 医疗代码标记化
- 分类编码
- 特征标准化
- 缺失值处理

* *用法：**
```python
from pyhealth.data import FeatureProcessor

processor = FeatureProcessor(
    vocabulary="diagnoses",
    min_freq=5,  # Minimum code frequency
    max_vocab_size=10000
)

processed_features = processor(raw_features)
```

### 序列处理器

* *序列处理器** (`SequenceProcessor`)
- 处理顺序临床事件
- 时间顺序保存
- 序列填充/截断
- 时间间隙编码

* *主要特性：**
- 变长序列处理
- 时间特征提取
- 序列统计计算

* *参数：**
- `max_seq_length`：最大序列长度（如果较长，则截断）
- `padding`：填充策略（“前”或“后”） 
- `truncating`：截断策略（“前”或“后”） "post")

* *用法：**
```python
from pyhealth.data import SequenceProcessor

processor = SequenceProcessor(
    max_seq_length=100,
    padding="post",
    truncating="post"
)

# Process diagnosis sequences
processed_seq = processor(diagnosis_sequences)
```

* *NestedSequenceProcessor** (`NestedSequenceProcessor`)
- 处理分层序列（例如，包含事件的访问）
- 两级处理（访问级和访问级）事件级）
- 保留嵌套结构

* *用例：**
- EHR 访问包含多个事件
- 多级时间建模
- 分层注意力型号

* *结构：**
```python
# Input: [[visit1_events], [visit2_events], ...]
# Output: Processed nested sequences with proper padding
```

### 数字数据处理器

* *NestedFloatsProcessor** (`NestedFloatsProcessor`)
- 处理嵌套数值数组
- 实验室值、生命体征、测量值
- 多级数值特征

* * 操作：**
- 标准化
- 标准化
- 缺失值imputation
- 异常值处理

* *用法：**
```python
from pyhealth.data import NestedFloatsProcessor

processor = NestedFloatsProcessor(
    normalization="z-score",  # or "min-max"
    fill_missing="mean"  # imputation strategy
)

processed_labs = processor(lab_values)
```

* *TensorProcessor** (`TensorProcessor`)
- 将数据转换为 PyTorch 张量
- 类型处理（long、float、等）
- 设备放置（CPU/GPU）

* *参数：**
- `dtype`：张量数据类型
- `device`：计算设备

### 时序处理器

* *时序处理器** (`TimeseriesProcessor`)
- 处理带有时间戳的时态数据
- 时间间隙计算
- 时态特征工程
- 不规则采样处理

* *提取的特征：**
- 自上一个事件以来的时间
- 到下一个事件的时间事件
- 事件频率
- 时间模式

* *用法：**
```python
from pyhealth.data import TimeseriesProcessor

processor = TimeseriesProcessor(
    time_unit="hour",  # "day", "hour", "minute"
    compute_gaps=True,
    compute_frequency=True
)

processed_ts = processor(timestamps, events)
```

* *信号处理器** (`SignalProcessor`)
- 生理信号处理
- EEG, ECG、PPG 信号
- 滤波和预处理

* *操作：**
- 带通滤波
- 伪影去除
- 分割
- 特征提取（频率、幅度）

* *用法：**
```python
from pyhealth.data import SignalProcessor

processor = SignalProcessor(
    sampling_rate=256,  # Hz
    bandpass_filter=(0.5, 50),  # Hz range
    segment_length=30  # seconds
)

processed_signal = processor(raw_eeg_signal)
```

### 图像处理器

* *图像处理器** (`ImageProcessor`)
- 医学图像预处理
- 标准化和调整大小
- 增强支持
- 格式标准化

* *操作：**
- 调整为标准尺寸
- 归一化（平均值/标准差）
- 加窗（用于CT/MRI）
- 数据增强

* *用法：**
```python
from pyhealth.data import ImageProcessor

processor = ImageProcessor(
    image_size=(224, 224),
    normalization="imagenet",  # or custom mean/std
    augmentation=True
)

processed_image = processor(raw_image)
```

## 标签处理器

### 二进制分类

* *二进制标签处理器** (`BinaryLabelProcessor`)
- 二进制分类标签(0/1)
- 处理正/负类
- 不平衡的类权重

* *用法：**
```python
from pyhealth.data import BinaryLabelProcessor

processor = BinaryLabelProcessor(
    positive_class=1,
    class_weight="balanced"
)

processed_labels = processor(raw_labels)
```

### 多类分类

* *多类标签处理器** (`MultiClassLabelProcessor`)
- 多类分类(互斥类)
- 标签编码
- 类平衡

* *参数：**
- `num_classes`：类数
- `class_weight`：加权策略

* *用法：**
```python
from pyhealth.data import MultiClassLabelProcessor

processor = MultiClassLabelProcessor(
    num_classes=5,  # e.g., sleep stages: W, N1, N2, N3, REM
    class_weight="balanced"
)

processed_labels = processor(raw_labels)
```

### 多标签分类

* *多标签处理器** (`MultiLabelProcessor`)
- 多标签分类（每个样本多个标签）
- 每个标签的二进制编码
- 标签共现处理

* *用例：**
- 药物推荐（多个药物）
- ICD 编码（多个）诊断）
- 合并症预测

* *用法：**
```python
from pyhealth.data import MultiLabelProcessor

processor = MultiLabelProcessor(
    num_labels=100,  # total possible labels
    threshold=0.5  # prediction threshold
)

processed_labels = processor(raw_label_sets)
```

### 回归

* *回归标签处理器** (`RegressionLabelProcessor`)
- 连续值预测
- 目标缩放和标准化
- 异常值处理

* *用例：**
- 停留时间预测
- 实验室值预测
- 风险评分估计

* *用法：**
```python
from pyhealth.data import RegressionLabelProcessor

processor = RegressionLabelProcessor(
    normalization="z-score",  # or "min-max"
    clip_outliers=True,
    outlier_std=3  # clip at 3 standard deviations
)

processed_targets = processor(raw_values)
```

## 专用处理器

### 文本处理

* *文本处理器** (`TextProcessor`)
- 临床文本预处理
- 标记化
- 词汇构建
- 序列编码

* *操作：**
- 小写
- 标点符号删除
- 医学缩写处理
- 令牌频率过滤

* *用法：**
```python
from pyhealth.data import TextProcessor

processor = TextProcessor(
    tokenizer="word",  # or "sentencepiece", "bpe"
    lowercase=True,
    max_vocab_size=50000,
    min_freq=5
)

processed_text = processor(clinical_notes)
```

### 特定于模型的处理器

* *StageNetProcessor** (`StageNetProcessor`)
- StageNet 模型的专门预处理
- 基于块的序列处理
- 阶段感知特征提取

* *用法：**
```python
from pyhealth.data import StageNetProcessor

processor = StageNetProcessor(
    chunk_size=128,
    num_stages=3
)

processed_data = processor(sequential_data)
```

* *StageNetTensorProcessor** (`StageNetTensorProcessor`)
- StageNet 的张量转换
- 正确的批处理和padding
- 阶段掩模生成

### 原始数据处理

* *RawProcessor** (`RawProcessor`)
- 最小预处理
- 预处理数据的传递
- 自定义预处理场景

* *用法：**
```python
from pyhealth.data import RawProcessor

processor = RawProcessor()
processed_data = processor(data)  # Minimal transformation
```

## 样本级处理

* *样本处理器** (`SampleProcessor`)
- 处理完整样本（输入+输出）
- 协调多个处理器
- 端到端预处理管道

* *工作流程：**
1. 将输入处理器应用于功能
2. 将输出处理器应用于标签
3. 组合成模型就绪样本

* *用法：**
```python
from pyhealth.data import SampleProcessor

processor = SampleProcessor(
    input_processors={
        "diagnoses": SequenceProcessor(max_seq_length=50),
        "medications": SequenceProcessor(max_seq_length=30),
        "labs": NestedFloatsProcessor(normalization="z-score")
    },
    output_processor=BinaryLabelProcessor()
)

processed_sample = processor(raw_sample)
```

## 数据集级处理

* *数据集处理器** (`DatasetProcessor`)
- 处理整个数据集
- 批处理
- 并行处理支持
- 缓存以提高效率

* *操作：**
- 将处理器应用于所有样本
- 从数据集生成词汇
- 计算数据集统计数据
- 保存处理后的数据数据

* *用法：**
```python
from pyhealth.data import DatasetProcessor

processor = DatasetProcessor(
    sample_processor=sample_processor,
    num_workers=4,  # parallel processing
    cache_dir="/path/to/cache"
)

processed_dataset = processor(raw_dataset)
```

## 常见预处理工作流程

### 工作流程 1：EHR 死亡率预测

```python
from pyhealth.data import (
    SequenceProcessor,
    BinaryLabelProcessor,
    SampleProcessor
)

# Define processors
input_processors = {
    "diagnoses": SequenceProcessor(max_seq_length=50),
    "medications": SequenceProcessor(max_seq_length=30),
    "procedures": SequenceProcessor(max_seq_length=20)
}

output_processor = BinaryLabelProcessor(class_weight="balanced")

# Combine into sample processor
sample_processor = SampleProcessor(
    input_processors=input_processors,
    output_processor=output_processor
)

# Process dataset
processed_samples = [sample_processor(s) for s in raw_samples]
```

### 工作流程 2：睡眠分期EEG

```python
from pyhealth.data import (
    SignalProcessor,
    MultiClassLabelProcessor,
    SampleProcessor
)

# Signal preprocessing
signal_processor = SignalProcessor(
    sampling_rate=100,
    bandpass_filter=(0.3, 35),  # EEG frequency range
    segment_length=30  # 30-second epochs
)

# Label processing
label_processor = MultiClassLabelProcessor(
    num_classes=5,  # W, N1, N2, N3, REM
    class_weight="balanced"
)

# Combine
sample_processor = SampleProcessor(
    input_processors={"signal": signal_processor},
    output_processor=label_processor
)
```

### 工作流程 3：药物推荐

```python
from pyhealth.data import (
    SequenceProcessor,
    MultiLabelProcessor,
    SampleProcessor
)

# Input processing
input_processors = {
    "diagnoses": SequenceProcessor(max_seq_length=50),
    "previous_medications": SequenceProcessor(max_seq_length=40)
}

# Multi-label output (multiple drugs)
output_processor = MultiLabelProcessor(
    num_labels=150,  # number of possible drugs
    threshold=0.5
)

sample_processor = SampleProcessor(
    input_processors=input_processors,
    output_processor=output_processor
)
```

### 工作流程 4：住院时间预测

```python
from pyhealth.data import (
    SequenceProcessor,
    NestedFloatsProcessor,
    RegressionLabelProcessor,
    SampleProcessor
)

# Process different feature types
input_processors = {
    "diagnoses": SequenceProcessor(max_seq_length=30),
    "procedures": SequenceProcessor(max_seq_length=20),
    "labs": NestedFloatsProcessor(
        normalization="z-score",
        fill_missing="mean"
    )
}

# Regression target
output_processor = RegressionLabelProcessor(
    normalization="log",  # log-transform LOS
    clip_outliers=True
)

sample_processor = SampleProcessor(
    input_processors=input_processors,
    output_processor=output_processor
)
```

## 最佳实践

### 序列处理

1. **选择适当的 max_seq_length**：上下文和计算之间的平衡
  - 短序列（20-50）：快速，上下文较少
  - 中序列（50-100）：良好平衡
  - 长序列（100+）：更多上下文，较慢

2. **截断策略**：
  - “后”：保留最近的事件（建议用于临床预测）
  - “前”：保留最早的事件

3. **填充策略**：
  - “post”：在末尾填充（标准）
  - “pre”：在开始处填充

### 特征编码

1. **词汇量**：限制频繁代码
  - `min_freq=5`：包括出现≥5次的代码
  - `max_vocab_size=10000`：总词汇量上限

2. **处理罕见代码**：分组为“未知”类别

3. **缺失值**：
  - 插补（平均值、中位数、前向填充）
  - 指示变量
  - 特殊标记

### 标准化

1. **数字特征**：始终归一化
  - Z 分数：标准缩放（平均值 = 0，std = 1）
  - 最小-最大：范围缩放 [0, 1]

2. **仅计算训练集的统计数据**：防止数据泄漏

3. **对验证/测试集应用相同的归一化**

### 类不平衡

1. **使用类别权重**：`class_weight="balanced"`

2. **考虑过采样**：对于非常罕见的阳性病例

3. **使用适当的指标进行评估**：AUROC、AUPRC、F1

### 性能优化

1. **缓存处理后的数据**：保存预处理结果

2. **并行处理**：对DataLoader

3使用`num_workers`。 **批量处理**：一次处理多个样品

4. **特征选择**：删除低信息特征

### 验证

1. **检查加工形状**：确保尺寸正确

2. **验证值范围**：归一化后

3. **检查样品**：手动检查处理后的数据

4. **监控内存使用情况**：特别适用于大型数据集

## 故障排除

### 常见问题

* *内存错误：**
- 减少`max_seq_length`
- 使用较小的批次
- 分块处理数据
- 启用缓存到磁盘

* *处理速度慢：**
- 启用并行处理（`num_workers`）
- 缓存预处理数据
- 降低特征维度
- 使用更高效的数据类型

* *形状不匹配：**
- 检查序列长度
- 验证填充配置
- 确保一致的处理器设置

* *NaN 值：**
- 显式处理缺失数据
- 检查标准化参数
- 验证插补策略

* *类不平衡：**
- 使用类加权
- 考虑过采样
- 调整决策阈值
- 使用适当的评估指标
