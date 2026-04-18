---
name: vaex
description: 使用此技能来处理和分析超出可用 RAM 的大型表格数据集（数十亿行）。 Vaex 擅长核外 DataFrame 操作、惰性求值、快速聚合、大数据的高效可视化以及大型数据集的机器学习。当用户需要处理大型 CSV/HDF5/Arrow/Parquet 文件、对海量数据集执行快速统计、创建大数据可视化或构建不适合内存的 ML 管道时适用。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Vaex

## 概述

Vaex 是一个高性能 Python 库，专为惰性、核外 DataFrame 设计，用于处理和可视化太大而无法放入 RAM 的表格数据集。 Vaex 每秒可以处理超过十亿行，从而能够对数十亿行的数据集进行交互式数据探索和分析。

## 何时使用此技能

在以下情况下使用 Vaex：
- 处理大于可用 RAM（千兆字节到太字节）的表格数据集
- 对大规模数据执行快速统计聚合数据集
- 创建大型数据集的可视化和热图
- 在大数据上构建机器学习管道
- 数据格式之间的转换（CSV、HDF5、Arrow、Parquet）
- 需要惰性评估和虚拟列以避免内存开销
- 处理天文数据、金融时间序列或其他大规模科学数据datasets

## 核心功能

Vaex 提供了六个主要功能领域，每个领域都在参考目录中详细记录：

### 1. 数据帧和数据加载

从各种来源加载并创建 Vaex 数据帧，包括文件（HDF5、CSV、Arrow、Parquet）、pandas DataFrames、NumPy数组和字典。参考`references/core_dataframes.md`的内容：
- 高效打开大文件
- 从pandas/NumPy/Arrow转换
- 使用示例数据集
- 理解DataFrame结构

### 2.数据处理和操作

执行过滤，创建虚拟列，使用表达式，并聚合数据，而无需将所有内容加载到内存中。参考 `references/data_processing.md` 的内容：
- 筛选和选择
- 虚拟列和表达式
- Groupby 操作和聚合
- 字符串操作和日期时间处理
- 处理缺失数据

### 3. 性能和优化

利用 Vaex 的惰性求值、缓存策略和内存高效操作。参考 `references/performance.md` 的内容：
- 了解惰性求值
- 使用 `delay=True` 进行批处理操作
- 在需要时具体化列
- 缓存策略
- 异步操作

### 4. 数据可视化

创建大型数据集的交互式可视化包括热图、直方图和散点图。参考 `references/visualization.md`：
- 创建 1D 和 2D 绘图
- 热图可视化
- 使用选择
- 自定义绘图和子图

### 5. 机器学习集成

使用 transformers 构建 ML 管道，编码器，以及与 scikit-learn、XGBoost 和其他框架的集成。参考`references/machine_learning.md`的：
- 特征缩放和编码
- PCA和降维
- K-均值聚类
- 与scikit-learn/XGBoost/CatBoost集成
- 模型序列化和部署

### 6. I/O操作

以最佳性能高效地读取和写入各种格式的数据。参考 `references/io_operations.md` 的内容：
- 文件格式建议
- 导出策略
- 使用 Apache Arrow
- 大文件的 CSV 处理
- 服务器和远程数据访问

## 快速启动模式

对于大多数 Vaex 任务，请遵循以下模式：

```python
import vaex

# 1. Open or create DataFrame
df = vaex.open('large_file.hdf5')  # or .csv, .arrow, .parquet
# OR
df = vaex.from_pandas(pandas_df)

# 2. Explore the data
print(df)  # Shows first/last rows and column info
df.describe()  # Statistical summary

# 3. Create virtual columns (no memory overhead)
df['new_column'] = df.x ** 2 + df.y

# 4. Filter with selections
df_filtered = df[df.age > 25]

# 5. Compute statistics (fast, lazy evaluation)
mean_val = df.x.mean()
stats = df.groupby('category').agg({'value': 'sum'})

# 6. Visualize
df.plot1d(df.x, limits=[0, 100])
df.plot(df.x, df.y, limits='99.7%')

# 7. Export if needed
df.export_hdf5('output.hdf5')
```

## 使用参考

参考文件包含有关每个功能区域的详细信息。根据特定任务将引用加载到上下文中：

- **基本操作**：从 `references/core_dataframes.md` 和 `references/data_processing.md`
- **性能问题**：检查 `references/performance.md`
- **可视化任务**：使用 `references/visualization.md`
- **ML管道**：参考 `references/machine_learning.md`
- **文件 I/O**：参考 `references/io_operations.md`

## 最佳实践

1. **使用 HDF5 或 Apache Arrow 格式**，以实现大型数据集 
2 的最佳性能。 **利用虚拟列**而不是具体化数据来节省内存
3. **批量操作**在执行多个计算时使用`delay=True`
4. **导出为高效格式**，而不是将数据保存在 CSV
5 中。 **使用表达式**进行复杂计算，无需中间存储
6. **使用 `df.stat()`** 进行分析，了解内存使用情况并优化操作

## 常见模式

### 模式：将大型 CSV 转换为 HDF5
```python
import vaex

# Open large CSV (processes in chunks automatically)
df = vaex.from_csv('large_file.csv')

# Export to HDF5 for faster future access
df.export_hdf5('large_file.hdf5')

# Future loads are instant
df = vaex.open('large_file.hdf5')
```

### 模式：高效聚合
```python
# Use delay=True to batch multiple operations
mean_x = df.x.mean(delay=True)
std_y = df.y.std(delay=True)
sum_z = df.z.sum(delay=True)

# Execute all at once
results = vaex.execute([mean_x, std_y, sum_z])
```

### 模式：特征工程的虚拟列
```python
# No memory overhead - computed on the fly
df['age_squared'] = df.age ** 2
df['full_name'] = df.first_name + ' ' + df.last_name
df['is_adult'] = df.age >= 18
```

## 资源

此技能包括 `references/` 目录中的参考文档：

- `core_dataframes.md` -数据帧创建、加载和基本结构
- `data_processing.md` - 过滤、表达式、聚合和转换
- `performance.md` - 优化策略和惰性评估
- `visualization.md` - 绘图和交互式可视化
- `machine_learning.md` - ML管道和模型集成
- `io_operations.md` - 文件格式和数据导入/导出
