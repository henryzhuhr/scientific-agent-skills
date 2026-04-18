# Dask DataFrames

## 概述

Dask DataFrames 通过在多个 pandas DataFrame 之间分配工作来实现大型表格数据的并行处理。正如文档中所描述的，“Dask DataFrames是许多pandas DataFrames的集合”，具有相同的API，使得从pandas的过渡变得简单。

## 核心概念

A Dask DataFrame沿着索引分为多个pandas DataFrames（分区）：
- 每个分区都是一个常规的pandas DataFrame
- 操作并行应用于每个分区
- 自动组合结果

## 关键功能

### 规模
- 在笔记本电脑上处理 100 GiB
- 在集群上处理 100 TiB
- 处理超出可用的数据集RAM

### 兼容性
- 实现大部分 pandas API
- 从 pandas 代码轻松过渡
- 与熟悉的操作一起使用

## 何时使用 Dask DataFrames

* *使用 Dask当**：
- 数据集超出可用RAM
- 计算需要大量时间，而pandas优化没有帮助
- 需要从原型（pandas）扩展到生产（更大的数据）
- 处理应一起处理的多个文件

* *坚持使用Pandas当**：
- 数据轻松装入内存
- 计算在亚秒内完成
- 无需自定义`.apply()` 函数的简单操作
- 迭代开发和探索

## 读取数据

Dask 镜像pandas 读取语法，并添加了对多个文件的支持：

### Single文件
```python
import dask.dataframe as dd

# Read single file
ddf = dd.read_csv('data.csv')
ddf = dd.read_parquet('data.parquet')
```

### 多个文件
```python
# Read multiple files using glob patterns
ddf = dd.read_csv('data/*.csv')
ddf = dd.read_parquet('s3://mybucket/data/*.parquet')

# Read with path structure
ddf = dd.read_parquet('data/year=*/month=*/day=*.parquet')
```

### 优化
```python
# Specify columns to read (reduces memory)
ddf = dd.read_parquet('data.parquet', columns=['col1', 'col2'])

# Control partitioning
ddf = dd.read_csv('data.csv', blocksize='64MB')  # Creates 64MB partitions
```

## 常用操作

所有操作都是惰性的，直到`.compute()`为称为。

### 过滤
```python
# Same as pandas
filtered = ddf[ddf['column'] > 100]
filtered = ddf.query('column > 100')
```

### 列操作
```python
# Add columns
ddf['new_column'] = ddf['col1'] + ddf['col2']

# Select columns
subset = ddf[['col1', 'col2', 'col3']]

# Drop columns
ddf = ddf.drop(columns=['unnecessary_col'])
```

### 聚合
```python
# Standard aggregations work as expected
mean = ddf['column'].mean().compute()
sum_total = ddf['column'].sum().compute()
counts = ddf['category'].value_counts().compute()
```

### GroupBy
```python
# GroupBy operations (may require shuffle)
grouped = ddf.groupby('category')['value'].mean().compute()

# Multiple aggregations
agg_result = ddf.groupby('category').agg({
    'value': ['mean', 'sum', 'count'],
    'amount': 'sum'
}).compute()
```

### 联接和合并
```python
# Merge DataFrames
merged = dd.merge(ddf1, ddf2, on='key', how='left')

# Join on index
joined = ddf1.join(ddf2, on='key')
```

### 排序
```python
# Sorting (expensive operation, requires data movement)
sorted_ddf = ddf.sort_values('column')
result = sorted_ddf.compute()
```

## 自定义操作

### 应用函数

* *到分区（高效）**：
```python
# Apply function to entire partitions
def custom_partition_function(partition_df):
    # partition_df is a pandas DataFrame
    return partition_df.assign(new_col=partition_df['col1'] * 2)

ddf = ddf.map_partitions(custom_partition_function)
```

* *到行（效率较低）**：
```python
# Apply to each row (creates many tasks)
ddf['result'] = ddf.apply(lambda row: custom_function(row), axis=1, meta=('result', 'float'))
```

* *注意**：始终优先选择 `map_partitions` 而不是按行 `apply` 以获得更好的效果

### 元参数

当Dask无法推断输出结构时，指定`meta`参数：
```python
# For apply operations
ddf['new'] = ddf.apply(func, axis=1, meta=('new', 'float64'))

# For map_partitions
ddf = ddf.map_partitions(func, meta=pd.DataFrame({
    'col1': pd.Series(dtype='float64'),
    'col2': pd.Series(dtype='int64')
}))
```

## 惰性求值和计算

### 惰性操作
```python
# These operations are lazy (instant, no computation)
filtered = ddf[ddf['value'] > 100]
aggregated = filtered.groupby('category').mean()
final = aggregated[aggregated['value'] < 500]

# Nothing has computed yet
```

### 触发计算
```python
# Compute single result
result = final.compute()

# Compute multiple results efficiently
result1, result2, result3 = dask.compute(
    operation1,
    operation2,
    operation3
)
```

### 持久化到内存
```python
# Keep results in distributed memory for reuse
ddf_cached = ddf.persist()

# Now multiple operations on ddf_cached won't recompute
result1 = ddf_cached.mean().compute()
result2 = ddf_cached.sum().compute()
```

## 索引管理

### 设置Index
```python
# Set index (required for efficient joins and certain operations)
ddf = ddf.set_index('timestamp', sorted=True)
```

### 索引属性
- 排序索引可以实现高效的过滤和连接
- 索引决定分区
- 某些操作在适当的索引下性能更好

## 写入结果

### 到文件
```python
# Write to multiple files (one per partition)
ddf.to_parquet('output/data.parquet')
ddf.to_csv('output/data-*.csv')

# Write to single file (forces computation and concatenation)
ddf.compute().to_csv('output/single_file.csv')
```

### 到内存（Pandas）
```python
# Convert to pandas (loads all data in memory)
pdf = ddf.compute()
```

## 性能注意事项

### 高效操作
- 列选择和过滤：非常高效
- 简单聚合（总和、平均值、计数）：高效
- 分区上的按行操作：使用 `map_partitions`

### 昂贵的操作
- 排序：需要跨工作人员进行数据洗牌
- 包含多个组的 GroupBy：可能需要洗牌
- 复杂联接：取决于数据distribution
- 按行应用：创建多个任务

### 优化技巧

* *1.尽早选择列**
```python
# Better: Read only needed columns
ddf = dd.read_parquet('data.parquet', columns=['col1', 'col2'])
```

* *2。在 GroupBy 之前过滤**
```python
# Better: Reduce data before expensive operations
result = ddf[ddf['year'] == 2024].groupby('category').sum().compute()
```

* *3。使用高效的文件格式**
```python
# Use Parquet instead of CSV for better performance
ddf.to_parquet('data.parquet')  # Faster, smaller, columnar
```

* *4。适当重新分区**
```python
# If partitions are too small
ddf = ddf.repartition(npartitions=10)

# If partitions are too large
ddf = ddf.repartition(partition_size='100MB')
```

## 常见模式

### ETL管道
```python
import dask.dataframe as dd

# Read data
ddf = dd.read_csv('raw_data/*.csv')

# Transform
ddf = ddf[ddf['status'] == 'valid']
ddf['amount'] = ddf['amount'].astype('float64')
ddf = ddf.dropna(subset=['important_col'])

# Aggregate
summary = ddf.groupby('category').agg({
    'amount': ['sum', 'mean'],
    'quantity': 'count'
})

# Write results
summary.to_parquet('output/summary.parquet')
```

### 时间序列分析
```python
# Read time series data
ddf = dd.read_parquet('timeseries/*.parquet')

# Set timestamp index
ddf = ddf.set_index('timestamp', sorted=True)

# Resample (if available in Dask version)
hourly = ddf.resample('1H').mean()

# Compute statistics
result = hourly.compute()
```

### 合并多个文件
```python
# Read multiple files as single DataFrame
ddf = dd.read_csv('data/2024-*.csv')

# Process combined data
result = ddf.groupby('category')['value'].sum().compute()
```

## 与 Pandas 的限制和差异

### 并非所有 Pandas 功能都可用
中未实现某些 pandas 操作Dask:
- 一些字符串方法
- 某些窗口函数
- 一些专门的统计函数

### 分区事项
- 分区内的操作是高效的
- 跨分区操作可能会很昂贵
- 基于索引的操作受益于排序索引

### 惰性评估
- 操作直到`.compute()`
- 需要了解计算才执行触发器
- 不计算就无法检查中间结果

## 调试提示

### 检查分区
```python
# Get number of partitions
print(ddf.npartitions)

# Compute single partition
first_partition = ddf.get_partition(0).compute()

# View first few rows (computes first partition)
print(ddf.head())
```

### 验证小数据上的操作
```python
# Test on small sample first
sample = ddf.head(1000)
# Validate logic works
# Then scale to full dataset
result = ddf.compute()
```

### 检查D类型
```python
# Verify data types are correct
print(ddf.dtypes)
```
