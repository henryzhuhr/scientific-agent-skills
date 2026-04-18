# Polars 数据转换

Polars 中联接、串联和整形操作的综合指南。

## Joins

Joins 基于公共列组合来自多个 DataFrame 的数据。

### 基本联接类型

* *内联接（交集）：**
```python
# Keep only matching rows from both DataFrames
result = df1.join(df2, on="id", how="inner")
```

* *左连接（所有左侧+从右侧匹配）：**
```python
# Keep all rows from left, add matching rows from right
result = df1.join(df2, on="id", how="left")
```

* *外连接（联合）：**
```python
# Keep all rows from both DataFrames
result = df1.join(df2, on="id", how="outer")
```

* *交叉连接（笛卡尔）产品）：**
```python
# Every row from left with every row from right
result = df1.join(df2, how="cross")
```

* *半连接（左过滤）：**
```python
# Keep only left rows that have a match in right
result = df1.join(df2, on="id", how="semi")
```

* *反连接（左非匹配）：**
```python
# Keep only left rows that DON'T have a match in right
result = df1.join(df2, on="id", how="anti")
```

### 连接语法变体

* *单列连接：**
```python
df1.join(df2, on="id")
```

* *多列连接：**
```python
df1.join(df2, on=["id", "date"])
```

* *不同列名称：**
```python
df1.join(df2, left_on="user_id", right_on="id")
```

* *多个不同的列：**
```python
df1.join(
    df2,
    left_on=["user_id", "date"],
    right_on=["id", "timestamp"]
)
```

### 后缀处理

当两个 DataFrame 都有同名的列时（除了 join键）：

```python
# Add suffixes to distinguish columns
result = df1.join(df2, on="id", suffix="_right")

# Results in: value, value_right (if both had "value" column)
```

### 连接示例

* *示例 1：客户订单**
```python
customers = pl.DataFrame({
    "customer_id": [1, 2, 3, 4],
    "name": ["Alice", "Bob", "Charlie", "David"]
})

orders = pl.DataFrame({
    "order_id": [101, 102, 103],
    "customer_id": [1, 2, 1],
    "amount": [100, 200, 150]
})

# Inner join - only customers with orders
result = customers.join(orders, on="customer_id", how="inner")

# Left join - all customers, even without orders
result = customers.join(orders, on="customer_id", how="left")
```

* *示例 2：时间序列data**
```python
prices = pl.DataFrame({
    "date": ["2023-01-01", "2023-01-02", "2023-01-03"],
    "stock": ["AAPL", "AAPL", "AAPL"],
    "price": [150, 152, 151]
})

volumes = pl.DataFrame({
    "date": ["2023-01-01", "2023-01-02"],
    "stock": ["AAPL", "AAPL"],
    "volume": [1000000, 1100000]
})

result = prices.join(
    volumes,
    on=["date", "stock"],
    how="left"
)
```

### Asof Joins (Nearest Match)

对于时间序列数据，连接到最近的时间戳：

```python
# Join to nearest earlier timestamp
quotes = pl.DataFrame({
    "timestamp": [1, 2, 3, 4, 5],
    "stock": ["A", "A", "A", "A", "A"],
    "quote": [100, 101, 102, 103, 104]
})

trades = pl.DataFrame({
    "timestamp": [1.5, 3.5, 4.2],
    "stock": ["A", "A", "A"],
    "trade": [50, 75, 100]
})

result = trades.join_asof(
    quotes,
    on="timestamp",
    by="stock",
    strategy="backward"  # or "forward", "nearest"
)
```

## Concatenation

Concatenation stacks DataFrames 

### 垂直串联（堆栈行）

```python
df1 = pl.DataFrame({"a": [1, 2], "b": [3, 4]})
df2 = pl.DataFrame({"a": [5, 6], "b": [7, 8]})

# Stack rows
result = pl.concat([df1, df2], how="vertical")
# Result: 4 rows, same columns
```

* *处理不匹配的模式：**
```python
df1 = pl.DataFrame({"a": [1, 2], "b": [3, 4]})
df2 = pl.DataFrame({"a": [5, 6], "c": [7, 8]})

# Diagonal concat - fills missing columns with nulls
result = pl.concat([df1, df2], how="diagonal")
# Result: columns a, b, c (with nulls where not present)
```

### 水平串联（堆栈）列）

```python
df1 = pl.DataFrame({"a": [1, 2, 3]})
df2 = pl.DataFrame({"b": [4, 5, 6]})

# Stack columns
result = pl.concat([df1, df2], how="horizontal")
# Result: 3 rows, columns a and b
```

* *注意：**水平连接需要相同的行数。

### 连接选项

```python
# Rechunk after concatenation (better performance for subsequent operations)
result = pl.concat([df1, df2], rechunk=True)

# Parallel execution
result = pl.concat([df1, df2], parallel=True)
```

### 用例

* *组合多个数据来源：**
```python
# Read multiple files and concatenate
files = ["data_2023.csv", "data_2024.csv", "data_2025.csv"]
dfs = [pl.read_csv(f) for f in files]
combined = pl.concat(dfs, how="vertical")
```

* *添加计算列：**
```python
base = pl.DataFrame({"value": [1, 2, 3]})
computed = pl.DataFrame({"doubled": [2, 4, 6]})
result = pl.concat([base, computed], how="horizontal")
```

## 旋转（宽格式）

将唯一值从一列转换为多列。

### 基本枢轴

```python
df = pl.DataFrame({
    "date": ["2023-01", "2023-01", "2023-02", "2023-02"],
    "product": ["A", "B", "A", "B"],
    "sales": [100, 150, 120, 160]
})

# Pivot: products become columns
pivoted = df.pivot(
    values="sales",
    index="date",
    columns="product"
)
# Result:
# date     | A   | B
# 2023-01  | 100 | 150
# 2023-02  | 120 | 160
```

### 带有聚合的枢轴

，当存在重复组合时，聚合：

```python
df = pl.DataFrame({
    "date": ["2023-01", "2023-01", "2023-01"],
    "product": ["A", "A", "B"],
    "sales": [100, 110, 150]
})

# Aggregate duplicates
pivoted = df.pivot(
    values="sales",
    index="date",
    columns="product",
    aggregate_function="sum"  # or "mean", "max", "min", etc.
)
```

### 多重索引列

```python
df = pl.DataFrame({
    "region": ["North", "North", "South", "South"],
    "date": ["2023-01", "2023-01", "2023-01", "2023-01"],
    "product": ["A", "B", "A", "B"],
    "sales": [100, 150, 120, 160]
})

pivoted = df.pivot(
    values="sales",
    index=["region", "date"],
    columns="product"
)
```

## 取消旋转/熔化（长格式）

将多个列转换为行（与旋转相反）。

### 基本逆透视

```python
df = pl.DataFrame({
    "date": ["2023-01", "2023-02"],
    "product_A": [100, 120],
    "product_B": [150, 160]
})

# Unpivot: convert columns to rows
unpivoted = df.unpivot(
    index="date",
    on=["product_A", "product_B"]
)
# Result:
# date     | variable   | value
# 2023-01  | product_A  | 100
# 2023-01  | product_B  | 150
# 2023-02  | product_A  | 120
# 2023-02  | product_B  | 160
```

### 自定义列名称

```python
unpivoted = df.unpivot(
    index="date",
    on=["product_A", "product_B"],
    variable_name="product",
    value_name="sales"
)
```

### 按模式逆透视

```python
# Unpivot all columns matching pattern
df = pl.DataFrame({
    "id": [1, 2],
    "sales_Q1": [100, 200],
    "sales_Q2": [150, 250],
    "sales_Q3": [120, 220],
    "revenue_Q1": [1000, 2000]
})

# Unpivot all sales columns
unpivoted = df.unpivot(
    index="id",
    on=pl.col("^sales_.*$")
)
```

## 爆炸（取消嵌套）列表）

将列表列转换为多行。

### 基本分解

```python
df = pl.DataFrame({
    "id": [1, 2],
    "values": [[1, 2, 3], [4, 5]]
})

# Explode list into rows
exploded = df.explode("values")
# Result:
# id | values
# 1  | 1
# 1  | 2
# 1  | 3
# 2  | 4
# 2  | 5
```

### 多列分解

```python
df = pl.DataFrame({
    "id": [1, 2],
    "letters": [["a", "b"], ["c", "d"]],
    "numbers": [[1, 2], [3, 4]]
})

# Explode multiple columns (must be same length)
exploded = df.explode("letters", "numbers")
```

## 转置

交换行和列：

```python
df = pl.DataFrame({
    "metric": ["sales", "costs", "profit"],
    "Q1": [100, 60, 40],
    "Q2": [150, 80, 70]
})

# Transpose
transposed = df.transpose(
    include_header=True,
    header_name="quarter",
    column_names="metric"
)
# Result: quarters as rows, metrics as columns
```

## 重塑模式

### 模式 1：从宽到长到宽

```python
# Start wide
wide = pl.DataFrame({
    "id": [1, 2],
    "A": [10, 20],
    "B": [30, 40]
})

# To long
long = wide.unpivot(index="id", on=["A", "B"])

# Back to wide (maybe with transformations)
wide_again = long.pivot(values="value", index="id", columns="variable")
```

### 模式 2：嵌套到Flat

```python
# Nested data
df = pl.DataFrame({
    "user": [1, 2],
    "purchases": [
        [{"item": "A", "qty": 2}, {"item": "B", "qty": 1}],
        [{"item": "C", "qty": 3}]
    ]
})

# Explode and unnest
flat = (
    df.explode("purchases")
    .unnest("purchases")
)
```

### 模式 3：聚合到数据透视

```python
# Raw data
sales = pl.DataFrame({
    "date": ["2023-01", "2023-01", "2023-02"],
    "product": ["A", "B", "A"],
    "sales": [100, 150, 120]
})

# Aggregate then pivot
result = (
    sales
    .group_by("date", "product")
    .agg(pl.col("sales").sum())
    .pivot(values="sales", index="date", columns="product")
)
```

## 高级转换

### 有条件重塑

```python
# Pivot only certain values
df.filter(pl.col("year") >= 2020).pivot(...)

# Unpivot with filtering
df.unpivot(index="id", on=pl.col("^sales.*$"))
```

### 多级转换

```python
# Complex reshaping pipeline
result = (
    df
    .unpivot(index="id", on=pl.col("^Q[0-9]_.*$"))
    .with_columns(
        quarter=pl.col("variable").str.extract(r"Q([0-9])", 1),
        metric=pl.col("variable").str.extract(r"Q[0-9]_(.*)", 1)
    )
    .drop("variable")
    .pivot(values="value", index=["id", "quarter"], columns="metric")
)
```

## 性能注意事项

### 连接性能

```python
# 1. Join on indexed/sorted columns when possible
df1_sorted = df1.sort("id")
df2_sorted = df2.sort("id")
result = df1_sorted.join(df2_sorted, on="id")

# 2. Use appropriate join type
# semi/anti are faster than inner+filter
matches = df1.join(df2, on="id", how="semi")  # Better than filtering after inner join

# 3. Filter before joining
df1_filtered = df1.filter(pl.col("active"))
result = df1_filtered.join(df2, on="id")  # Smaller join
```

### 连接性能

```python
# 1. Rechunk after concatenation
result = pl.concat(dfs, rechunk=True)

# 2. Use lazy mode for large concatenations
lf1 = pl.scan_parquet("file1.parquet")
lf2 = pl.scan_parquet("file2.parquet")
result = pl.concat([lf1, lf2]).collect()
```

### 枢轴性能

```python
# 1. Filter before pivoting
pivoted = df.filter(pl.col("year") == 2023).pivot(...)

# 2. Specify aggregate function explicitly
pivoted = df.pivot(..., aggregate_function="first")  # Faster than "sum" if only one value
```

## 常见用例

### 时间序列对齐

```python
# Align two time series with different timestamps
ts1.join_asof(ts2, on="timestamp", strategy="backward")
```

### 功能工程

```python
# Create lag features
df.with_columns(
    pl.col("value").shift(1).over("user_id").alias("prev_value"),
    pl.col("value").shift(2).over("user_id").alias("prev_prev_value")
)
```

### 数据反规范化

```python
# Combine normalized tables
orders.join(customers, on="customer_id").join(products, on="product_id")
```

### 报告生成

```python
# Pivot for reporting
sales.pivot(values="amount", index="month", columns="product")
```
