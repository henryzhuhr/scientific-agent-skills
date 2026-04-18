# Pandas 到 Polars 迁移指南

本指南帮助您从 pandas 迁移到 Polars，具有全面的操作映射和关键差异。

## 核心概念差异

### 1. 无索引系统

* *Pandas：** 使用基于行的索引system
```python
df.loc[0, "column"]
df.iloc[0:5]
df.set_index("id")
```

* *Polars:** 仅使用整数位置
```python
df[0, "column"]  # Row position, column name
df[0:5]  # Row slice
# No set_index equivalent - use group_by instead
```

### 2. 内存格式

* *Pandas:** 面向行的 NumPy 数组
* *Polars:**列式 Apache Arrow 格式

* *含义：**
- Polars 列操作速度更快
- Polars 使用更少的内存
- Polars 具有更好的数据共享能力

### 3.并行化

* *Pandas：** 主要是单线程（需要 Dask 才能并行）
* *Polars：** 默认情况下使用 Rust 的并发性进行并行

### 4. 惰性求值

* *Pandas：** 仅渴望评估
* *Polars:** 带有查询优化的 eager (DataFrame)和惰性 (LazyFrame)

### 5. 类型严格性

* *Pandas:** 允许静默类型转换
* *Polars:** 严格键入，显式强制转换必填

* *示例：**
```python
# Pandas: Silently converts to float
pd_df["int_col"] = [1, 2, None, 4]  # dtype: float64

# Polars: Keeps as integer with null
pl_df = pl.DataFrame({"int_col": [1, 2, None, 4]})  # dtype: Int64
```

## 操作映射

### 数据选择

|运营|熊猫 | Polars |
|-----------|--------|--------|
|选择列| `df["col"]` 或 `df.col` | `df.select("col")` 或 `df["col"]` |
|选择多个 | `df[["a", "b"]]` | `df.select("a", "b")` |
|按位置选择| `df.iloc[:, 0:3]` | `df.select(pl.col(df.columns[0:3]))` |
|按条件选择| `df[df["age"] > 25]` | `df.filter(pl.col("age") > 25)` |

### 数据过滤

|运营|熊猫 | Polars |
|-----------|--------|--------|
|单一条件 | `df[df["age"] > 25]` | `df.filter(pl.col("age") > 25)` |
|多种条件| `df[(df["age"] > 25) & (df["city"] == "NY")]` | `df.filter(pl.col("age") > 25, pl.col("city") == "NY")` |
|查询方式 | `df.query("age > 25")` | `df.filter(pl.col("age") > 25)` |
|伊辛 | `df[df["city"].isin(["NY", "LA"])]` | `df.filter(pl.col("city").is_in(["NY", "LA"]))` |
|伊斯纳 | `df[df["value"].isna()]` | `df.filter(pl.col("value").is_null())` |
|不娜| `df[df["value"].notna()]` | `df.filter(pl.col("value").is_not_null())` |

### 添加/修改列

|运营|熊猫 | Polars |
|------------|--------|--------|
|添加栏目| `df["new"] = df["old"] * 2` | `df.with_columns(new=pl.col("old") * 2)` |
|多栏 | `df.assign(a=..., b=...)` | `df.with_columns(a=..., b=...)` |
|条件栏 | `np.where(condition, a, b)` | `pl.when(condition).then(a).otherwise(b)` |

* *重要区别 - 并行执行：**

```python
# Pandas: Sequential (lambda sees previous results)
df.assign(
    a=lambda df_: df_.value * 10,
    b=lambda df_: df_.value * 100
)

# Polars: Parallel (all computed together)
df.with_columns(
    a=pl.col("value") * 10,
    b=pl.col("value") * 100
)
```

### 分组和聚合

|运营|熊猫 | Polars |
|------------|--------|--------|
|分组依据 | `df.groupby("col")` | `df.group_by("col")` |
|聚合单| `df.groupby("col")["val"].mean()` | `df.group_by("col").agg(pl.col("val").mean())` |
|聚合多个 | `df.groupby("col").agg({"val": ["mean", "sum"]})` | `df.group_by("col").agg(pl.col("val").mean(), pl.col("val").sum())` |
|尺寸| `df.groupby("col").size()` | `df.group_by("col").agg(pl.len())` |
|计数 | `df.groupby("col").count()` | `df.group_by("col").agg(pl.col("*").count())` |

### 窗口函数

|运营|熊猫 | Polars |
|-----------|--------|--------|
|转变| `df.groupby("col").transform("mean")` | `df.with_columns(pl.col("val").mean().over("col"))` |
|排名| `df.groupby("col")["val"].rank()` | `df.with_columns(pl.col("val").rank().over("col"))` |
|班次| `df.groupby("col")["val"].shift(1)` | `df.with_columns(pl.col("val").shift(1).over("col"))` |
|累积 | `df.groupby("col")["val"].cumsum()` | `df.with_columns(pl.col("val").cum_sum().over("col"))` |

### 加入

|运营|熊猫 | Polars |
|-----------|--------|--------|
|内连接 | `df1.merge(df2, on="id")` | `df1.join(df2, on="id", how="inner")` |
|左连接 | `df1.merge(df2, on="id", how="left")` | `df1.join(df2, on="id", how="left")` |
|不同的键| `df1.merge(df2, left_on="a", right_on="b")` | `df1.join(df2, left_on="a", right_on="b")` |

### 连接

|运营|熊猫 | Polars |
|-----------|--------|--------|
|垂直| `pd.concat([df1, df2], axis=0)` | `pl.concat([df1, df2], how="vertical")` |
|卧式| `pd.concat([df1, df2], axis=1)` | `pl.concat([df1, df2], how="horizontal")` |

### 排序

|运营|熊猫 | Polars |
|-----------|--------|--------|
|按列排序 | `df.sort_values("col")` | `df.sort("col")` |
|降序| `df.sort_values("col", ascending=False)` | `df.sort("col", descending=True)` |
|多栏 | `df.sort_values(["a", "b"])` | `df.sort("a", "b")` |

### 重塑

|运营|熊猫 | Polars |
|-----------|--------|--------|
|枢轴| `df.pivot(index="a", columns="b", values="c")` | `df.pivot(values="c", index="a", columns="b")` |
|融化| `df.melt(id_vars="id")` | `df.unpivot(index="id")` |

### I/O 操作

|运营|熊猫 | Polars |
|------------|--------|--------|
|读取 CSV | `pd.read_csv("file.csv")` | `pl.read_csv("file.csv")` 或 `pl.scan_csv()` |
|写入 CSV | `df.to_csv("file.csv")` | `df.write_csv("file.csv")` |
|阅读镶木地板 | `pd.read_parquet("file.parquet")` | `pl.read_parquet("file.parquet")` |
|写实木复合地板| `df.to_parquet("file.parquet")` | `df.write_parquet("file.parquet")` |
|阅读 Excel | `pd.read_excel("file.xlsx")` | `pl.read_excel("file.xlsx")` |

### 字符串操作

|运营|熊猫 | Polars |
|------------|--------|--------|
|上层| `df["col"].str.upper()` | `df.select(pl.col("col").str.to_uppercase())` |
|降低| `df["col"].str.lower()` | `df.select(pl.col("col").str.to_lowercase())` |
|包含 | `df["col"].str.contains("pattern")` | `df.filter(pl.col("col").str.contains("pattern"))` |
|更换| `df["col"].str.replace("old", "new")` | `df.select(pl.col("col").str.replace("old", "new"))` |
|分裂| `df["col"].str.split(" ")` | `df.select(pl.col("col").str.split(" "))` |

### 日期时间操作

|运营|熊猫 | Polars |
|-----------|--------|--------|
|解析日期 | `pd.to_datetime(df["col"])` | `df.select(pl.col("col").str.strptime(pl.Date, "%Y-%m-%d"))` |
|年份| `df["date"].dt.year` | `df.select(pl.col("date").dt.year())` |
|月 | `df["date"].dt.month` | `df.select(pl.col("date").dt.month())` |
|日 | `df["date"].dt.day` | `df.select(pl.col("date").dt.day())` |

### 缺失数据

|运营|熊猫 | Polars |
|-----------|--------|--------|
|删除空值 | `df.dropna()` | `df.drop_nulls()` |
|填充空值 | `df.fillna(0)` | `df.fill_null(0)` |
|检查空 | `df["col"].isna()` | `df.select(pl.col("col").is_null())` |
|前向填充 | `df.fillna(method="ffill")` | `df.select(pl.col("col").fill_null(strategy="forward"))` |

### 其他操作

|运营|熊猫 | Polars |
|-----------|--------|--------|
|独特的价值观| `df["col"].unique()` | `df["col"].unique()` |
|价值很重要| `df["col"].value_counts()` | `df["col"].value_counts()` |
|描述| `df.describe()` | `df.describe()` |
|样品| `df.sample(n=100)` | `df.sample(n=100)` |
|头| `df.head()` | `df.head()` |
|尾巴| `df.tail()` | `df.tail()` |

## 常见迁移模式

### 模式 1：链式迁移操作

* *Pandas:**
```python
result = (df
    .assign(new_col=lambda x: x["old_col"] * 2)
    .query("new_col > 10")
    .groupby("category")
    .agg({"value": "sum"})
    .reset_index()
)
```

* *Polars:**
```python
result = (df
    .with_columns(new_col=pl.col("old_col") * 2)
    .filter(pl.col("new_col") > 10)
    .group_by("category")
    .agg(pl.col("value").sum())
)
# No reset_index needed - Polars doesn't have index
```

### 模式 2：应用函数

* *Pandas:**
```python
# Avoid in Polars - breaks parallelization
df["result"] = df["value"].apply(lambda x: x * 2)
```

* *Polars:**
```python
# Use expressions instead
df = df.with_columns(result=pl.col("value") * 2)

# If custom function needed
df = df.with_columns(
    result=pl.col("value").map_elements(lambda x: x * 2, return_dtype=pl.Float64)
)
```

### 模式 3：条件列创建

* *Pandas:**
```python
df["category"] = np.where(
    df["value"] > 100,
    "high",
    np.where(df["value"] > 50, "medium", "low")
)
```

* *Polars:**
```python
df = df.with_columns(
    category=pl.when(pl.col("value") > 100)
        .then("high")
        .when(pl.col("value") > 50)
        .then("medium")
        .otherwise("low")
)
```

### 模式4：组变换

* *Pandas:**
```python
df["group_mean"] = df.groupby("category")["value"].transform("mean")
```

* *Polars:**
```python
df = df.with_columns(
    group_mean=pl.col("value").mean().over("category")
)
```

### 模式 5：多个聚合

* *Pandas:**
```python
result = df.groupby("category").agg({
    "value": ["mean", "sum", "count"],
    "price": ["min", "max"]
})
```

* *Polars:**
```python
result = df.group_by("category").agg(
    pl.col("value").mean().alias("value_mean"),
    pl.col("value").sum().alias("value_sum"),
    pl.col("value").count().alias("value_count"),
    pl.col("price").min().alias("price_min"),
    pl.col("price").max().alias("price_max")
)
```

## 要避免的性能反模式

### 反模式1：顺序管道操作

* *差（禁用并行化）：**
```python
df = df.pipe(function1).pipe(function2).pipe(function3)
```

* *好（启用并行化）：**
```python
df = df.with_columns(
    function1_result(),
    function2_result(),
    function3_result()
)
```

### 反模式 2：热中的 Python 函数路径

* *坏：**
```python
df = df.with_columns(
    result=pl.col("value").map_elements(lambda x: x * 2)
)
```

* *好：**
```python
df = df.with_columns(result=pl.col("value") * 2)
```

### 反模式 3：使用急切读取大数据文件

* *坏：**
```python
df = pl.read_csv("large_file.csv")
result = df.filter(pl.col("age") > 25).select("name", "age")
```

* *好：**
```python
lf = pl.scan_csv("large_file.csv")
result = lf.filter(pl.col("age") > 25).select("name", "age").collect()
```

### 反模式 4：行迭代

* *差：**
```python
for row in df.iter_rows():
    # Process row
    pass
```

* *好：**
```python
# Use vectorized operations
df = df.with_columns(
    # Vectorized computation
)
```

## 迁移检查表

当从pandas迁移到Polars：

1. **删除索引操作** - 使用整数位置或group_by
2. **用表达式替换 apply/map** - 使用 Polars 本机操作 
3. **更新列分配** - 使用 `with_columns()` 而不是直接分配 
4. **将 groupby.transform 更改为 .over()** - 窗口函数的工作方式不同
5. **更新字符串操作** - 使用 `.str.to_uppercase()` 而不是 `.str.upper()`
6. **添加显式类型转换** - Polars 不会默默地转换类型
7. **考虑延迟评估** - 对于大数据，使用 `scan_*` 而不是 `read_*`
8. **更新聚合语法** - Polars
9 中更明确。 **删除reset_index调用** - Polars
10中不需要。 **更新条件逻辑** - 使用`when().then().otherwise()`模式

## 兼容层

对于逐步迁移，您可以使用这两个库：

```python
import pandas as pd
import polars as pl

# Convert pandas to Polars
pl_df = pl.from_pandas(pd_df)

# Convert Polars to pandas
pd_df = pl_df.to_pandas()

# Use Arrow for zero-copy (when possible)
pl_df = pl.from_arrow(pd_df)
pd_df = pl_df.to_arrow().to_pandas()
```

## 何时坚持使用Pandas

在以下情况下考虑使用 pandas：
- 处理需要复杂索引操作的时间序列
- 需要广泛的生态系统支持（某些库仅支持 pandas）
- 团队缺乏 Rust/Polars 专业知识
- 数据很小，性能并不重要
- 使用高级 pandas 功能，而无需 Polars 等效项

## 当切换到 Polars

在以下情况下切换到 Polars：
- 性能至关重要
- 处理大型数据集 (>1GB)
- 需要延迟计算和查询优化
- 想要更好的类型安全性
- 默认情况下需要并行执行
- 启动新的项目
