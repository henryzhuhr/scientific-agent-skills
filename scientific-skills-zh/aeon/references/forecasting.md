# 时间序列预测

Aeon 提供了用于预测未来时间序列值的预测算法。

## Naive 和 Baseline 方法

用于比较的简单预测策略：

- `NaiveForecaster` - 多种策略：最后值、平均值、季节朴素
  - 参数：`strategy` ("last", "mean", "seasonal"), `sp` (季节性时段)
  - **使用时机**：建立基线或简单模式

## 统计模型

经典时间序列预测方法：

### ARIMA
- `ARIMA` - 自回归综合移动Average
  - 参数：`p`（AR 阶）、`d`（差分）、`q`（MA 阶）
  - **使用时**：线性模式、平稳或差分平稳序列

### 指数平滑
- `ETS` - 误差趋势季节分解
  - 参数：`error`、`trend`、`seasonal` 类型
  - **使用时间**：存在趋势和季节性模式

### 阈值自回归
- `TAR` - 用于状态切换的阈值自回归模型
- `AutoTAR` - 自动阈值发现
  - **使用时间**：系列在不同状态下表现出不同的行为

### Theta 方法
- `Theta` -经典 Theta 预测
  - 参数：`theta`、`weights` 用于分解
  - **使用时间**：需要简单但有效的基线

### 时变参数
- `TVP` - 带卡尔曼的时变参数模型过滤
  - **使用时**：参数随时间变化

## 深度学习预测器

复杂时间模式的神经网络：

- `TCNForecaster` - 时间卷积网络
  - 大感受野的扩张卷积
  - **何时使用**：长序列，需要非循环架构

- `DeepARNetwork` - 使用RNN进行概率预测
  - 提供预测间隔
  - **使用当**：需要概率预测，不确定性量化

## 基于回归的预测

将回归应用于滞后特征：

- `RegressionForecaster` - 包装回归器进行预测
  - 参数：`window_length`，`horizon`
  - **使用时间**：想要使用任何回归器作为预测器

## 快速入门

```python
from aeon.forecasting.naive import NaiveForecaster
from aeon.forecasting.arima import ARIMA
import numpy as np

# Create time series
y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Naive baseline
naive = NaiveForecaster(strategy="last")
naive.fit(y)
forecast_naive = naive.predict(fh=[1, 2, 3])

# ARIMA model
arima = ARIMA(order=(1, 1, 1))
arima.fit(y)
forecast_arima = arima.predict(fh=[1, 2, 3])
```

## 预测范围

预测范围（`fh`）指定未来时间点预测：

```python
# Relative horizon (next 3 steps)
fh = [1, 2, 3]

# Absolute horizon (specific time indices)
from aeon.forecasting.base import ForecastingHorizon
fh = ForecastingHorizon([11, 12, 13], is_relative=False)
```

## 型号选择

- **基线**：采用季节性策略的 NaiveForecaster
- **线性模式**：ARIMA
- **趋势 + 季节性**：ETS
- **制度变化**：TAR、AutoTAR
- **复杂模式**：TCNForecaster
- **概率**： DeepARNetwork
- **长序列**：TCNForecaster
- **短序列**：ARIMA、ETS

## 评估指标

使用标准预测指标：

```python
from aeon.performance_metrics.forecasting import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error
)

# Calculate error
mae = mean_absolute_error(y_true, y_pred)
mse = mean_squared_error(y_true, y_pred)
mape = mean_absolute_percentage_error(y_true, y_pred)
```

## 外生变量

许多预测器支持外生特征：

```python
# Train with exogenous variables
forecaster.fit(y, X=X_train)

# Predict requires future exogenous values
y_pred = forecaster.predict(fh=[1, 2, 3], X=X_test)
```

## 基类

- `BaseForecaster` - 所有预测器的抽象基础
- `BaseDeepForecaster` - 深度学习预测器的基础

扩展这些以实现自定义预测算法。
