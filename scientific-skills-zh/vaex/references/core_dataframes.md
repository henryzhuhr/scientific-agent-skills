# 核心 DataFrames 和数据加载

此参考内容涵盖 Vaex DataFrame 基础知识、从各种来源加载数据以及了解 DataFrame 结构。

## DataFrame 基础知识

A Vaex DataFrame 是处理大型表格数据集的中央数据结构。与 pandas 不同，Vaex DataFrames：
- 使用**延迟评估** - 直到需要时才执行操作
- 工作**非核心** - 数据不需要适合 RAM
- 支持**虚拟列** - 没有内存开销的计算列
- 通过优化的 C++ 启用**每秒十亿行**处理后端

## 打开现有文件

### 主要方法：`vaex.open()`

最常见的加载数据方式：

```python
import vaex

# Works with multiple formats
df = vaex.open('data.hdf5')     # HDF5 (recommended)
df = vaex.open('data.arrow')    # Apache Arrow (recommended)
df = vaex.open('data.parquet')  # Parquet
df = vaex.open('data.csv')      # CSV (slower for large files)
df = vaex.open('data.fits')     # FITS (astronomy)

# Can open multiple files as one DataFrame
df = vaex.open('data_*.hdf5')   # Wildcards supported
```

* *关键特征：**
- **HDF5/Arrow即时** - 内存映射文件，无需加载time
- **处理大型 CSV** - 自动对大型 CSV 文件进行分块
- **立即返回** - 延迟计算意味着在需要之前不进行计算

### 格式特定加载器

```python
# CSV with options
df = vaex.from_csv(
    'large_file.csv',
    chunk_size=5_000_000,      # Process in chunks
    convert=True,               # Convert to HDF5 automatically
    copy_index=False            # Don't copy pandas index if present
)

# Apache Arrow
df = vaex.open('data.arrow')    # Native support, very fast

# HDF5 (optimal format)
df = vaex.open('data.hdf5')     # Instant loading via memory mapping
```

## 从其他源创建数据帧

### 来自 Pandas

```python
import pandas as pd
import vaex

# Convert pandas DataFrame
pdf = pd.read_csv('data.csv')
df = vaex.from_pandas(pdf, copy_index=False)

# Warning: This loads entire pandas DataFrame into memory
# For large data, prefer vaex.from_csv() directly
```

### 来自 NumPy 数组

```python
import numpy as np
import vaex

# Single array
x = np.random.rand(1_000_000)
df = vaex.from_arrays(x=x)

# Multiple arrays
x = np.random.rand(1_000_000)
y = np.random.rand(1_000_000)
df = vaex.from_arrays(x=x, y=y)
```

### 来自字典

```python
import vaex

# Dictionary of lists/arrays
data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000]
}
df = vaex.from_dict(data)
```

### 来自箭头表

```python
import pyarrow as pa
import vaex

# From Arrow Table
arrow_table = pa.table({
    'x': [1, 2, 3],
    'y': [4, 5, 6]
})
df = vaex.from_arrow_table(arrow_table)
```

## 示例数据集

Vaex 提供用于测试的内置示例数据集：

```python
import vaex

# NYC taxi dataset (~1GB, 11 million rows)
df = vaex.example()

# Smaller datasets
df = vaex.datasets.titanic()
df = vaex.datasets.iris()
```

## 检查数据帧

### 基本信息

```python
# Display first and last rows
print(df)

# Shape (rows, columns)
print(df.shape)  # Returns (row_count, column_count)
print(len(df))   # Row count

# Column names
print(df.columns)
print(df.column_names)

# Data types
print(df.dtypes)

# Memory usage (for materialized columns)
df.byte_size()
```

### 统计汇总

```python
# Quick statistics for all numeric columns
df.describe()

# Single column statistics
df.x.mean()
df.x.std()
df.x.min()
df.x.max()
df.x.sum()
df.x.count()

# Quantiles
df.x.quantile(0.5)   # Median
df.x.quantile([0.25, 0.5, 0.75])  # Multiple quantiles
```

### 查看数据

```python
# First/last rows (returns pandas DataFrame)
df.head(10)
df.tail(10)

# Random sample
df.sample(n=100)

# Convert to pandas (careful with large data!)
pdf = df.to_pandas_df()

# Convert specific columns only
pdf = df[['x', 'y']].to_pandas_df()
```

## 数据帧结构

### 列

```python
# Access columns as expressions
x_column = df.x
y_column = df['y']

# Column operations return expressions (lazy)
sum_column = df.x + df.y    # Not computed yet

# List all columns
print(df.get_column_names())

# Check column types
print(df.dtypes)

# Virtual vs materialized columns
print(df.get_column_names(virtual=False))  # Materialized only
print(df.get_column_names(virtual=True))   # All columns
```

### 行

```python
# Row count
row_count = len(df)
row_count = df.count()

# Single row (returns dict)
row = df.row(0)
print(row['column_name'])

# Note: Iterating over rows is NOT recommended in Vaex
# Use vectorized operations instead
```

## 使用表达式

表达式是Vaex 表示尚未执行的计算的方式Yet:

```python
# Create expressions (no computation)
expr = df.x ** 2 + df.y

# Expressions can be used in many contexts
mean_of_expr = expr.mean()          # Still lazy
df['new_col'] = expr                # Virtual column
filtered = df[expr > 10]            # Selection

# Force evaluation
result = expr.values  # Returns NumPy array (use carefully!)
```

## 数据帧操作

### 复制

```python
# Shallow copy (shares data)
df_copy = df.copy()

# Deep copy (independent data)
df_deep = df.copy(deep=True)
```

### 修剪/切片

```python
# Select row range
df_subset = df[1000:2000]      # Rows 1000-2000
df_subset = df[:1000]          # First 1000 rows
df_subset = df[-1000:]         # Last 1000 rows

# Note: This creates a view, not a copy (efficient)
```

### 连接

```python
# Vertical concatenation (combine rows)
df_combined = vaex.concat([df1, df2, df3])

# Horizontal concatenation (combine columns)
# Use join or simply assign columns
df['new_col'] = other_df.some_column
```

## 最佳实践

1. **首选 HDF5 或 Arrow 格式** - 即时加载，最佳性能
2. **将大型 CSV 转换为 HDF5** - 一次性转换以供重复使用
3. **避免在大数据上使用 `.to_pandas_df()`** - 违背 Vaex 的目的 
4. **使用表达式而不是 `.values`** - 保持操作惰性 
5. **检查数据类型** - 确保数字列不是字符串类型
6. **使用虚拟列** - 派生数据零内存开销

## 常见模式

### 模式：一次性 CSV 到 HDF5 转换

```python
# Initial conversion (do once)
df = vaex.from_csv('large_data.csv', convert='large_data.hdf5')

# Future loads (instant)
df = vaex.open('large_data.hdf5')
```

### 模式：检查大型数据集

```python
import vaex

df = vaex.open('large_file.hdf5')

# Quick overview
print(df)                    # First/last rows
print(df.shape)             # Dimensions
print(df.describe())        # Statistics

# Sample for detailed inspection
sample = df.sample(1000).to_pandas_df()
print(sample.head())
```

### 模式：加载多个文件

```python
# Load multiple files as one DataFrame
df = vaex.open('data_part*.hdf5')

# Or explicitly concatenate
df1 = vaex.open('data_2020.hdf5')
df2 = vaex.open('data_2021.hdf5')
df_all = vaex.concat([df1, df2])
```

## 常见问题和解决方案

### 问题：CSV 加载速度慢

```python
# Solution: Convert to HDF5 first
df = vaex.from_csv('large.csv', convert='large.hdf5')
# Future loads: df = vaex.open('large.hdf5')
```

### 问题：列显示为字符串类型

```python
# Check type
print(df.dtypes)

# Convert to numeric (creates virtual column)
df['age_numeric'] = df.age.astype('int64')
```

### 问题：小型操作内存不足

```python
# Likely using .values or .to_pandas_df()
# Solution: Use lazy operations

# Bad (loads into memory)
array = df.x.values

# Good (stays lazy)
mean = df.x.mean()
filtered = df[df.x > 10]
```

## 相关资源

- 有关数据操作和过滤：请参阅`data_processing.md`
- 有关性能优化：请参阅`performance.md`
  - 有关文件格式详细信息：请参阅 `io_operations.md`
