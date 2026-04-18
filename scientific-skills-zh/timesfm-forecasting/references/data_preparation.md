# TimesFM

## 的数据准备输入格式

TimesFM 接受**一维 numpy 数组**列表。每个数组代表一个
单变量时间序列。

```python
inputs = [
    np.array([1.0, 2.0, 3.0, 4.0, 5.0]),       # Series 1
    np.array([10.0, 20.0, 15.0, 25.0]),          # Series 2 (different length)
    np.array([100.0, 110.0, 105.0, 115.0, 120.0, 130.0]),  # Series 3
]
```

### 关键属性

- **变量长度**：同一批次中的序列可以有不同的长度
- **浮点值**：使用`np.float32`或`np.float64`
- **仅限 1-D**：每个数组必须是一维（不是 2-D 矩阵行）
- **NaN 处理**：前导 NaN 被去除；内部 NaN 线性插值

## 从通用格式加载

### CSV — 单系列（长格式）

```python
import pandas as pd
import numpy as np

df = pd.read_csv("data.csv", parse_dates=["date"])
values = df["value"].values.astype(np.float32)
inputs = [values]
```

### CSV — 多系列（宽格式）

```python
df = pd.read_csv("data.csv", parse_dates=["date"], index_col="date")
inputs = [df[col].dropna().values.astype(np.float32) for col in df.columns]
```

### CSV —带 ID 列的长格式

```python
df = pd.read_csv("data.csv", parse_dates=["date"])
inputs = []
for series_id, group in df.groupby("series_id"):
    values = group.sort_values("date")["value"].values.astype(np.float32)
    inputs.append(values)
```

### Pandas DataFrame

```python
# Single column
inputs = [df["temperature"].values.astype(np.float32)]

# Multiple columns
inputs = [df[col].dropna().values.astype(np.float32) for col in numeric_cols]
```

### Numpy Arrays

```python
# 2-D array (rows = series, cols = time steps)
data = np.load("timeseries.npy")  # shape (N, T)
inputs = [data[i] for i in range(data.shape[0])]

# Or from 1-D
inputs = [np.sin(np.linspace(0, 10, 200))]
```

### Excel

```python
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
inputs = [df[col].dropna().values.astype(np.float32) for col in df.select_dtypes(include=[np.number]).columns]
```

### Parquet

```python
df = pd.read_parquet("data.parquet")
inputs = [df[col].dropna().values.astype(np.float32) for col in df.select_dtypes(include=[np.number]).columns]
```

### JSON

```python
import json

with open("data.json") as f:
    data = json.load(f)

# Assumes {"series_name": [values...], ...}
inputs = [np.array(values, dtype=np.float32) for values in data.values()]
```

## NaN Handling

TimesFM 处理 NaN 值自动：

### 前导 NaNs

在输入模型之前剥离：

```python
# Input:  [NaN, NaN, 1.0, 2.0, 3.0]
# Actual: [1.0, 2.0, 3.0]
```

### 内部 NaNs

线性插值：

```python
# Input:  [1.0, NaN, 3.0, NaN, NaN, 6.0]
# Actual: [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
```

### 尾随NaNs

* *未处理** — 在传递给模型之前删除它们：

```python
values = df["value"].values.astype(np.float32)
# Remove trailing NaNs
while len(values) > 0 and np.isnan(values[-1]):
    values = values[:-1]
inputs = [values]
```

### 最佳实践

```python
def clean_series(arr: np.ndarray) -> np.ndarray:
    """Clean a time series for TimesFM input."""
    arr = np.asarray(arr, dtype=np.float32)
    # Remove trailing NaNs
    while len(arr) > 0 and np.isnan(arr[-1]):
        arr = arr[:-1]
    # Replace inf with NaN (will be interpolated)
    arr[np.isinf(arr)] = np.nan
    return arr

inputs = [clean_series(df[col].values) for col in cols]
```

## 上下文长度注意事项

|上下文长度 |使用案例|备注|
| -------------- | -------- | ----- |
| 64–256 |快速原型制作|最少的上下文，快速|
| 256–512 | 256–512每日数据，~1 年 |平衡性好|
| 512–1024 |每日数据，~2-3 年 |标准生产|
| 1024–4096 |每小时数据、每周模式 |更多背景 = 更好 |
| 4096–16384 |高频、长模式| TimesFM 2.5 最大值 |

* * 经验法则**：提供至少 3-5 个主导模式 
 的完整周期（例如，对于每日数据的每周季节性，提供至少 21-35 天）。

## 协变量 (XReg)

TimesFM 2.5 通过`forecast_with_covariates()` API.

### 协变量类型

|类型 |描述 |示例|
| ---- | ----------- | --------|
| **动态数值** |时变数值特征 |温度、价格、促销花费|
| **动态分类** |时变分类特征 |星期几、假日标志 |
| **静态分类** |固定每个系列的功能|商店 ID、地区、产品类别 |

### 准备协变量

每个系列的每个协变量的长度必须为 `context + horizon`：

```python
import numpy as np

context_len = 100   # length of historical data
horizon = 24        # forecast horizon
total_len = context_len + horizon

# Dynamic numerical: temperature forecast for each series
temp = [
    np.random.randn(total_len).astype(np.float32),  # Series 1
    np.random.randn(total_len).astype(np.float32),  # Series 2
]

# Dynamic categorical: day of week (0-6) for each series
dow = [
    np.tile(np.arange(7), total_len // 7 + 1)[:total_len],  # Series 1
    np.tile(np.arange(7), total_len // 7 + 1)[:total_len],  # Series 2
]

# Static categorical: one label per series
regions = ["east", "west"]

# Forecast with covariates
point, quantiles = model.forecast_with_covariates(
    inputs=[values1, values2],
    dynamic_numerical_covariates={"temperature": temp},
    dynamic_categorical_covariates={"day_of_week": dow},
    static_categorical_covariates={"region": regions},
    xreg_mode="xreg + timesfm",
)
```

### XReg 模式

|模式|描述 |
| ---- | ----------- |
| `"xreg + timesfm"` |首先处理协变量，然后与 TimesFM 预测 |
| 相结合`"timesfm + xreg"` | TimesFM 首先预测，然后通过协变量进行调整 |

## 常见数据问题

### 问题：系列太短

TimesFM 需要至少 1 个数据点，但更多上下文 = 更好的预测。

```python
MIN_LENGTH = 32  # Practical minimum for meaningful forecasts

inputs = [
    arr for arr in raw_inputs
    if len(arr[~np.isnan(arr)]) >= MIN_LENGTH
]
```

### 问题：具有常数的系列值

常量序列可能会产生 NaN 或零宽度预测区间：

```python
for i, arr in enumerate(inputs):
    if np.std(arr[~np.isnan(arr)]) < 1e-10:
        print(f"⚠️ Series {i} is constant — forecast will be flat")
```

### 问题：极端离群值

即使进行归一化，大离群值也会破坏预测的稳定性：

```python
def clip_outliers(arr: np.ndarray, n_sigma: float = 5.0) -> np.ndarray:
    """Clip values beyond n_sigma standard deviations."""
    mu = np.nanmean(arr)
    sigma = np.nanstd(arr)
    if sigma > 0:
        arr = np.clip(arr, mu - n_sigma * sigma, mu + n_sigma * sigma)
    return arr
```

### 问题：批量混合频率

TimesFM独立处理每个系列，因此您可以混合频率：

```python
inputs = [
    daily_sales,      # 365 points
    weekly_revenue,   # 52 points
    monthly_users,    # 24 points
]
# All forecasted in one batch — TimesFM handles different lengths
point, q = model.forecast(horizon=12, inputs=inputs)
```

但是，`horizon`是共享的。如果每个系列需要不同的视野，
在单独的调用中进行预测。
