# Polars 核心概念

## 表达式

表达式是Polars API 的基础。它们是可组合的单元，描述数据转换而不立即执行它们。

### 什么是表达式？

表达式描述数据的转换。它仅在特定上下文中具体化（执行）：
- `select()` - 选择和转换列
- `with_columns()` - 添加或修改列
- `filter()` - 过滤行
- `group_by().agg()` - 聚合数据

### 表达式语法

* *基本列参考：**
```python
pl.col("column_name")
```

* *计算表达式：**
```python
# Arithmetic
pl.col("height") * 2
pl.col("price") + pl.col("tax")

# With alias
(pl.col("weight") / (pl.col("height") ** 2)).alias("bmi")

# Method chaining
pl.col("name").str.to_uppercase().str.slice(0, 3)
```

### 表达式上下文

* *选择上下文：**
```python
df.select(
    "name",  # Simple column name
    pl.col("age"),  # Expression
    (pl.col("age") * 12).alias("age_in_months")  # Computed expression
)
```

* *With_columns 上下文：**
```python
df.with_columns(
    age_doubled=pl.col("age") * 2,
    name_upper=pl.col("name").str.to_uppercase()
)
```

* *过滤器上下文：**
```python
df.filter(
    pl.col("age") > 25,
    pl.col("city").is_in(["NY", "LA", "SF"])
)
```

* *Group_by上下文：**
```python
df.group_by("department").agg(
    pl.col("salary").mean(),
    pl.col("employee_id").count()
)
```

### 表达式扩展

一次对多个列应用操作：

* *所有列：**
```python
df.select(pl.all() * 2)
```

* *模式匹配：**
```python
# All columns ending with "_value"
df.select(pl.col("^.*_value$") * 100)

# All numeric columns
df.select(pl.col(pl.NUMERIC_DTYPES) + 1)
```

* *排除模式：**
```python
df.select(pl.all().exclude("id", "name"))
```

### 表达式组成

表达式可存储和重用：

```python
# Define reusable expressions
age_expression = pl.col("age") * 12
name_expression = pl.col("name").str.to_uppercase()

# Use in multiple contexts
df.select(age_expression, name_expression)
df.with_columns(age_months=age_expression)
```

## 数据类型

Polars 拥有基于 Apache Arrow 的严格类型系统。

### 核心数据类型

* *数字：**
- `Int8`、`Int16`、`Int32`、`Int64` - 有符号整数
- `UInt8`、`UInt16`、`UInt32`、`UInt64` - 无符号整数
- `Float32`、`Float64` - 浮点数

* *文本：**
- `Utf8` / `String` - UTF-8 编码字符串
- `Categorical` - 分类字符串（低基数）
- `Enum` - 固定字符串值集

* *时间：**
- `Date` - 日历日期（无time)
- `Datetime` - 带有可选时区的日期和时间
- `Time` - 一天中的时间
- `Duration` - 持续时间/差异

* *布尔值：**
- `Boolean` -真/假值

* *嵌套：**
- `List` - 可变长度列表
- `Array` - 固定长度数组
- `Struct` - 嵌套记录结构

  * *其他：**
- `Binary` - 二进制data
- `Object` - Python 对象（避免在生产中）
- `Null` - Null 类型

### 类型转换

在类型之间显式转换：

```python
# Cast to different type
df.select(
    pl.col("age").cast(pl.Float64),
    pl.col("date_string").str.strptime(pl.Date, "%Y-%m-%d"),
    pl.col("id").cast(pl.Utf8)
)
```

### Null处理

Polars 在所有类型中使用一致的空值处理：

* *检查空值：**
```python
df.filter(pl.col("value").is_null())
df.filter(pl.col("value").is_not_null())
```

* *填充空值：**
```python
pl.col("value").fill_null(0)
pl.col("value").fill_null(strategy="forward")
pl.col("value").fill_null(strategy="backward")
pl.col("value").fill_null(strategy="mean")
```

* *删除nulls:**
```python
df.drop_nulls()  # Drop any row with nulls
df.drop_nulls(subset=["col1", "col2"])  # Drop rows with nulls in specific columns
```

### 分类数据

对低基数的字符串列使用分类类型（重复值）：

```python
# Cast to categorical
df.with_columns(
    pl.col("category").cast(pl.Categorical)
)

# Benefits:
# - Reduced memory usage
# - Faster grouping and joining
# - Maintains order information
```

## Lazy vs Eagervaluation

Polars 支持两种执行模式：eager（DataFrame）和lazy（LazyFrame）。

### Eagervaluation（DataFrame）

操作立即执行：

```python
import polars as pl

# DataFrame operations execute right away
df = pl.read_csv("data.csv")  # Reads file immediately
result = df.filter(pl.col("age") > 25)  # Filters immediately
final = result.select("name", "age")  # Selects immediately
```

* *何时使用eager：**
- 适合内存的小数据集
- 交互式探索笔记本
- 简单的一次性操作
- 需要立即反馈

### 延迟计算（LazyFrame）

操作构建查询计划，在执行前进行优化：

```python
import polars as pl

# LazyFrame operations build a query plan
lf = pl.scan_csv("data.csv")  # Doesn't read yet
lf2 = lf.filter(pl.col("age") > 25)  # Adds to plan
lf3 = lf2.select("name", "age")  # Adds to plan
df = lf3.collect()  # NOW executes optimized plan
```

* *何时使用延迟：**
- Large数据集
- 复杂查询管道
- 仅需要数据子集
- 性能至关重要
- 需要流

### 查询优化

Polars 自动优化延迟查询：

* *谓词下推：**
 过滤操作推送到可能时的数据源：
```python
# Only reads rows where age > 25 from CSV
lf = pl.scan_csv("data.csv")
result = lf.filter(pl.col("age") > 25).collect()
```

* *投影下推：**
仅从数据源读取所需的列：
```python
# Only reads "name" and "age" columns from CSV
lf = pl.scan_csv("data.csv")
result = lf.select("name", "age").collect()
```

* *查询计划检查：**
```python
# View the optimized query plan
lf = pl.scan_csv("data.csv")
result = lf.filter(pl.col("age") > 25).select("name", "age")
print(result.explain())  # Shows optimized plan
```

### 流模式

处理大于内存的数据：

```python
# Enable streaming for very large datasets
lf = pl.scan_csv("very_large.csv")
result = lf.filter(pl.col("age") > 25).collect(streaming=True)
```

* *流的好处：**
- 处理大于RAM的数据
- 更低的峰值内存用法
- 基于块的处理
- 自动内存管理

* *流限制：**
- 并非所有操作都支持流
- 对于小数据可能会更慢
- 某些操作需要具体化整个数据集

### 在Eager和Lazy之间转换

* *Eager到Lazy：**
```python
df = pl.read_csv("data.csv")
lf = df.lazy()  # Convert to LazyFrame
```

* *Lazy到Eager：**
```python
lf = pl.scan_csv("data.csv")
df = lf.collect()  # Execute and return DataFrame
```

## 内存格式

Polars 使用 Apache Arrow 列式内存格式：

* *优点：**
- 与其他 Arrow 库共享零拷贝数据
- 高效的列式操作
- SIMD向量化
- 减少内存开销
- 快速序列化

* *含义：**
- 数据按列存储，而不是按行
- 列操作非常快
- 随机行访问比pandas慢
- 最适合分析工作负载

## 并行化

Polars 使用 Rust 的并发性自动并行化操作：

* *并行化的内容：**
- 组内的聚合
- 窗口函数
- 大多数表达式计算
- 文件读取（多个文件）
- 连接操作

* *并行化应避免的事项：**
- Python 用户定义函数 (UDF)
- `.map_elements()`
- 顺序 `.pipe()` 链

* *最佳做法：**
```python
# Good: Stays in expression API (parallelized)
df.with_columns(
    pl.col("value") * 10,
    pl.col("value").log(),
    pl.col("value").sqrt()
)

# Bad: Uses Python function (sequential)
df.with_columns(
    pl.col("value").map_elements(lambda x: x * 10)
)
```

## 严格类型系统

Polars 强制执行严格类型：

* *无静默转换：**
```python
# This will error - can't mix types
# df.with_columns(pl.col("int_col") + "string")

# Must cast explicitly
df.with_columns(
    pl.col("int_col").cast(pl.Utf8) + "_suffix"
)
```

* *优点：**
- 防止静默bugs
- 可预测的行为
- 更好的性能
- 更清晰的代码意图

* *整数空值：**
与pandas不同，整数列可以有空值而不转换为浮点数：
```python
# In pandas: Int column with null becomes Float
# In polars: Int column with null stays Int (with null values)
df = pl.DataFrame({"int_col": [1, 2, None, 4]})
# dtype: Int64 (not Float64)
```
