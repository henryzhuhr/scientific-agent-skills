# 时间序列分析参考

本文档提供了statsmodels中时间序列模型的全面指导，包括ARIMA、状态空间模型、VAR、指数平滑和预测方法。

## 概述

Statsmodels提供了广泛的时间序列功能：
- **单变量模型**：AR、ARIMA、SARIMAX、指数平滑
- **多元模型**：VAR、VARMAX、动态因子模型
- **状态空间框架**：自定义模型、卡尔曼滤波
- **诊断工具**：ACF、PACF、平稳性检验、残差分析
- **预测**：点预测和预测区间

## 单变量时间序列模型

### AutoReg（AR模型）

自回归模型：当前值取决于过去的值。

* *何时使用：**
- 单变量时间序列
- 过去的值预测未来
- 平稳序列

* *模型**：yₜ = c + φ₁yₜ₋₁ + φ2yₜ₋2 + ... + φₚyₜ₋ₚ + εₜ

```python
from statsmodels.tsa.ar_model import AutoReg
import pandas as pd

# Fit AR(p) model
model = AutoReg(y, lags=5)  # AR(5)
results = model.fit()

print(results.summary())
```

* *具有外生回归量：**
```python
# AR with exogenous variables (ARX)
model = AutoReg(y, lags=5, exog=X_exog)
results = model.fit()
```

* *季节性 AR：**
```python
# Seasonal lags (e.g., monthly data with yearly seasonality)
model = AutoReg(y, lags=12, seasonal=True)
results = model.fit()
```

### ARIMA（自回归积分移动平均）

组合 AR、差分 (I)和 MA 分量。

* *何时使用：**
- 非平稳时间序列（需要差分）
- 过去的值和错误预测未来
- 许多时间序列的灵活模型

* *模型**：ARIMA（p，d，q）
- p：AR阶数（滞后）
- d：差分阶数（实现平稳性）
- q：MA阶数（滞后预测误差）

```python
from statsmodels.tsa.arima.model import ARIMA

# Fit ARIMA(p,d,q)
model = ARIMA(y, order=(1, 1, 1))  # ARIMA(1,1,1)
results = model.fit()

print(results.summary())
```

* *选择p、d、q：**

1. **确定d（差阶）**：
```python
from statsmodels.tsa.stattools import adfuller

# ADF test for stationarity
def check_stationarity(series):
    result = adfuller(series)
    print(f"ADF Statistic: {result[0]:.4f}")
    print(f"p-value: {result[1]:.4f}")
    if result[1] <= 0.05:
        print("Series is stationary")
        return True
    else:
        print("Series is non-stationary, needs differencing")
        return False

# Test original series
if not check_stationarity(y):
    # Difference once
    y_diff = y.diff().dropna()
    if not check_stationarity(y_diff):
        # Difference again
        y_diff2 = y_diff.diff().dropna()
        check_stationarity(y_diff2)
```

2. **确定 p 和 q (ACF/PACF)**：
```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

# After differencing to stationarity
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# ACF: helps determine q (MA order)
plot_acf(y_stationary, lags=40, ax=ax1)
ax1.set_title('Autocorrelation Function (ACF)')

# PACF: helps determine p (AR order)
plot_pacf(y_stationary, lags=40, ax=ax2)
ax2.set_title('Partial Autocorrelation Function (PACF)')

plt.tight_layout()
plt.show()

# Rules of thumb:
# - PACF cuts off at lag p → AR(p)
# - ACF cuts off at lag q → MA(q)
# - Both decay → ARMA(p,q)
```

3. **模型选择 (AIC/BIC)**：
```python
# Grid search for best (p,q) given d
import numpy as np

best_aic = np.inf
best_order = None

for p in range(5):
    for q in range(5):
        try:
            model = ARIMA(y, order=(p, d, q))
            results = model.fit()
            if results.aic < best_aic:
                best_aic = results.aic
                best_order = (p, d, q)
        except:
            continue

print(f"Best order: {best_order} with AIC: {best_aic:.2f}")
```

### SARIMAX（具有外生变量的季节性 ARIMA）

使用季节性和外生回归量扩展 ARIMA。

* *何时使用：**
- 季节性模式（每月、每月、季度数据）
- 外部变量影响系列
- 最灵活的单变量模型

* *模型**：SARIMAX(p,d,q)(P,D,Q,s)
- (p,d,q)：非季节性 ARIMA
- (P,D,Q,s)：周期为 s

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Seasonal ARIMA for monthly data (s=12)
model = SARIMAX(y,
                order=(1, 1, 1),           # (p,d,q)
                seasonal_order=(1, 1, 1, 12))  # (P,D,Q,s)
results = model.fit()

print(results.summary())
```

 的季节性 ARIMA**具有外生性变量：**
```python
# SARIMAX with external predictors
model = SARIMAX(y,
                exog=X_exog,
                order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 12))
results = model.fit()
```

* *示例：具有趋势和季节性的月销售额**
```python
# Typical for monthly data: (p,d,q)(P,D,Q,12)
# Start with (1,1,1)(1,1,1,12) or (0,1,1)(0,1,1,12)

model = SARIMAX(monthly_sales,
                order=(0, 1, 1),
                seasonal_order=(0, 1, 1, 12),
                enforce_stationarity=False,
                enforce_invertibility=False)
results = model.fit()
```

### 指数平滑

过去观察值的加权平均值，权重呈指数递减。

* *何时使用：**
- 简单、可解释的预测
- 存在趋势和/或季节性
- 无需明确的模型规范

* *类型：**
- 简单指数平滑：无趋势，无季节性
- 霍尔特方法：有趋势
- Holt-Winters：具有趋势和季节性

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Simple exponential smoothing
model = ExponentialSmoothing(y, trend=None, seasonal=None)
results = model.fit()

# Holt's method (with trend)
model = ExponentialSmoothing(y, trend='add', seasonal=None)
results = model.fit()

# Holt-Winters (trend + seasonality)
model = ExponentialSmoothing(y,
                            trend='add',           # 'add' or 'mul'
                            seasonal='add',        # 'add' or 'mul'
                            seasonal_periods=12)   # e.g., 12 for monthly
results = model.fit()

print(results.summary())
```

* *加法与乘法：**
```python
# Additive: constant seasonal variation
# yₜ = Level + Trend + Seasonal + Error

# Multiplicative: proportional seasonal variation
# yₜ = Level × Trend × Seasonal × Error

# Choose based on data:
# - Additive: seasonal variation constant over time
# - Multiplicative: seasonal variation increases with level
```

* *创新状态空间（ETS）：**
```python
from statsmodels.tsa.exponential_smoothing.ets import ETSModel

# More robust, state space formulation
model = ETSModel(y,
                error='add',           # 'add' or 'mul'
                trend='add',           # 'add', 'mul', or None
                seasonal='add',        # 'add', 'mul', or None
                seasonal_periods=12)
results = model.fit()
```

## 多元时间序列

### VAR（向量自回归）

方程组，其中每个变量取决于所有变量的过去值。

* *何时使用：**
- 多个相互关联的时间序列
- 双向关系
- 格兰杰因果关系测试

* *模型**：每个变量在所有变量上都是 AR：
- y₁ₜ = c₁ + φ₁₁y₁ₜ₋₁ + φ₁ς y2ₜ₋₁ + ... + ε₁ₜ
- y2ₜ = c2 + φ2₁y₁ₜ₋₁ + φ22y2ₜ₋₁ + ... + ε2ₜ

```python
from statsmodels.tsa.api import VAR
import pandas as pd

# Data should be DataFrame with multiple columns
# Each column is a time series
df_multivariate = pd.DataFrame({'series1': y1, 'series2': y2, 'series3': y3})

# Fit VAR
model = VAR(df_multivariate)

# Select lag order using AIC/BIC
lag_order_results = model.select_order(maxlags=15)
print(lag_order_results.summary())

# Fit with optimal lags
results = model.fit(maxlags=5, ic='aic')
print(results.summary())
```

* *格兰杰因果关系检验：**
```python
# Test if series1 Granger-causes series2
from statsmodels.tsa.stattools import grangercausalitytests

# Requires 2D array [series2, series1]
test_data = df_multivariate[['series2', 'series1']]

# Test up to max_lag
max_lag = 5
results = grangercausalitytests(test_data, max_lag, verbose=True)

# P-values for each lag
for lag in range(1, max_lag + 1):
    p_value = results[lag][0]['ssr_ftest'][1]
    print(f"Lag {lag}: p-value = {p_value:.4f}")
```

* *脉冲响应函数 (IRF)：**
```python
# Trace effect of shock through system
irf = results.irf(10)  # 10 periods ahead

# Plot IRFs
irf.plot(orth=True)  # Orthogonalized (Cholesky decomposition)
plt.show()

# Cumulative effects
irf.plot_cum_effects(orth=True)
plt.show()
```

* *预测误差方差分解：**
```python
# Contribution of each variable to forecast error variance
fevd = results.fevd(10)  # 10 periods ahead
fevd.plot()
plt.show()
```

### VARMAX（具有移动平均和外生变量的 VAR）

使用 MA 分量和外部扩展 VAR回归器。

* *何时使用：**
- VAR 不足（需要 MA 组件）
- 外部变量影响系统
- 更灵活的多元模型

```python
from statsmodels.tsa.statespace.varmax import VARMAX

# VARMAX(p, q) with exogenous variables
model = VARMAX(df_multivariate,
               order=(1, 1),        # (p, q)
               exog=X_exog)
results = model.fit()

print(results.summary())
```

## 状态空间模型

自定义时间序列的灵活框架模型.

* *何时使用：**
- 自定义模型规范
- 未观察到的分量
- 卡尔曼滤波/平滑
- 缺失数据

```python
from statsmodels.tsa.statespace.mlemodel import MLEModel

# Extend MLEModel for custom state space models
# Example: Local level model (random walk + noise)
```

* *动态因子型号：**
```python
from statsmodels.tsa.statespace.dynamic_factor import DynamicFactor

# Extract common factors from multiple time series
model = DynamicFactor(df_multivariate,
                      k_factors=2,          # Number of factors
                      factor_order=2)       # AR order of factors
results = model.fit()

# Estimated factors
factors = results.factors.filtered
```

## 预测

### 点预测

```python
# ARIMA forecasting
model = ARIMA(y, order=(1, 1, 1))
results = model.fit()

# Forecast h steps ahead
h = 10
forecast = results.forecast(steps=h)

# With exogenous variables (SARIMAX)
model = SARIMAX(y, exog=X, order=(1, 1, 1))
results = model.fit()

# Need future exogenous values
forecast = results.forecast(steps=h, exog=X_future)
```

### 预测区间

```python
# Get forecast with confidence intervals
forecast_obj = results.get_forecast(steps=h)
forecast_df = forecast_obj.summary_frame()

print(forecast_df)
# Contains: mean, mean_se, mean_ci_lower, mean_ci_upper

# Extract components
forecast_mean = forecast_df['mean']
forecast_ci_lower = forecast_df['mean_ci_lower']
forecast_ci_upper = forecast_df['mean_ci_upper']

# Plot
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(y.index, y, label='Historical')
plt.plot(forecast_df.index, forecast_mean, label='Forecast', color='red')
plt.fill_between(forecast_df.index,
                 forecast_ci_lower,
                 forecast_ci_upper,
                 alpha=0.3, color='red', label='95% CI')
plt.legend()
plt.title('Forecast with Prediction Intervals')
plt.show()
```

### 动态与静态预测

```python
# Static (one-step-ahead, using actual values)
static_forecast = results.get_prediction(start=split_point, end=len(y)-1)

# Dynamic (multi-step, using predicted values)
dynamic_forecast = results.get_prediction(start=split_point,
                                          end=len(y)-1,
                                          dynamic=True)

# Plot comparison
fig, ax = plt.subplots(figsize=(12, 6))
y.plot(ax=ax, label='Actual')
static_forecast.predicted_mean.plot(ax=ax, label='Static forecast')
dynamic_forecast.predicted_mean.plot(ax=ax, label='Dynamic forecast')
ax.legend()
plt.show()
```

## 诊断测试

### 平稳性测试

```python
from statsmodels.tsa.stattools import adfuller, kpss

# Augmented Dickey-Fuller (ADF) test
# H0: unit root (non-stationary)
adf_result = adfuller(y, autolag='AIC')
print(f"ADF Statistic: {adf_result[0]:.4f}")
print(f"p-value: {adf_result[1]:.4f}")
if adf_result[1] <= 0.05:
    print("Reject H0: Series is stationary")
else:
    print("Fail to reject H0: Series is non-stationary")

# KPSS test
# H0: stationary (opposite of ADF)
kpss_result = kpss(y, regression='c', nlags='auto')
print(f"KPSS Statistic: {kpss_result[0]:.4f}")
print(f"p-value: {kpss_result[1]:.4f}")
if kpss_result[1] <= 0.05:
    print("Reject H0: Series is non-stationary")
else:
    print("Fail to reject H0: Series is stationary")
```

### 剩余诊断

```python
# Ljung-Box test for autocorrelation in residuals
from statsmodels.stats.diagnostic import acorr_ljungbox

lb_test = acorr_ljungbox(results.resid, lags=10, return_df=True)
print(lb_test)
# P-values > 0.05 indicate no significant autocorrelation (good)

# Plot residual diagnostics
results.plot_diagnostics(figsize=(12, 8))
plt.show()

# Components:
# 1. Standardized residuals over time
# 2. Histogram + KDE of residuals
# 3. Q-Q plot for normality
# 4. Correlogram (ACF of residuals)
```

### 异方差测试

```python
from statsmodels.stats.diagnostic import het_arch

# ARCH test for heteroskedasticity
arch_test = het_arch(results.resid, nlags=10)
print(f"ARCH test statistic: {arch_test[0]:.4f}")
print(f"p-value: {arch_test[1]:.4f}")

# If significant, consider GARCH model
```

## 季节性分解

```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Decompose into trend, seasonal, residual
decomposition = seasonal_decompose(y,
                                   model='additive',  # or 'multiplicative'
                                   period=12)         # seasonal period

# Plot components
fig = decomposition.plot()
fig.set_size_inches(12, 8)
plt.show()

# Access components
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# STL decomposition (more robust)
from statsmodels.tsa.seasonal import STL

stl = STL(y, seasonal=13)  # seasonal must be odd
stl_result = stl.fit()

fig = stl_result.plot()
plt.show()
```

## 模型评估

### 样本内指标

```python
# From results object
print(f"AIC: {results.aic:.2f}")
print(f"BIC: {results.bic:.2f}")
print(f"Log-likelihood: {results.llf:.2f}")

# MSE on training data
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(y, results.fittedvalues)
rmse = np.sqrt(mse)
print(f"RMSE: {rmse:.4f}")

# MAE
from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(y, results.fittedvalues)
print(f"MAE: {mae:.4f}")
```

### 样本外指标评估

```python
# Train-test split for time series (no shuffle!)
train_size = int(0.8 * len(y))
y_train = y[:train_size]
y_test = y[train_size:]

# Fit on training data
model = ARIMA(y_train, order=(1, 1, 1))
results = model.fit()

# Forecast test period
forecast = results.forecast(steps=len(y_test))

# Metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error

rmse = np.sqrt(mean_squared_error(y_test, forecast))
mae = mean_absolute_error(y_test, forecast)
mape = np.mean(np.abs((y_test - forecast) / y_test)) * 100

print(f"Test RMSE: {rmse:.4f}")
print(f"Test MAE: {mae:.4f}")
print(f"Test MAPE: {mape:.2f}%")
```

### 滚动预测

```python
# More realistic evaluation: rolling one-step-ahead forecasts
forecasts = []

for t in range(len(y_test)):
    # Refit or update with new observation
    y_current = y[:train_size + t]
    model = ARIMA(y_current, order=(1, 1, 1))
    fit = model.fit()

    # One-step forecast
    fc = fit.forecast(steps=1)[0]
    forecasts.append(fc)

forecasts = np.array(forecasts)

rmse = np.sqrt(mean_squared_error(y_test, forecasts))
print(f"Rolling forecast RMSE: {rmse:.4f}")
```

### 交叉验证

```python
# Time series cross-validation (expanding window)
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
rmse_scores = []

for train_idx, test_idx in tscv.split(y):
    y_train_cv = y.iloc[train_idx]
    y_test_cv = y.iloc[test_idx]

    model = ARIMA(y_train_cv, order=(1, 1, 1))
    results = model.fit()

    forecast = results.forecast(steps=len(test_idx))
    rmse = np.sqrt(mean_squared_error(y_test_cv, forecast))
    rmse_scores.append(rmse)

print(f"CV RMSE: {np.mean(rmse_scores):.4f} ± {np.std(rmse_scores):.4f}")
```

## 高级主题

### ARDL（自回归）分布式滞后)

桥接单变量和多变量时间序列。

```python
from statsmodels.tsa.ardl import ARDL

# ARDL(p, q) model
# y depends on its own lags and lags of X
model = ARDL(y, lags=2, exog=X, exog_lags=2)
results = model.fit()
```

### 纠错模型

用于协积分序列。

```python
from statsmodels.tsa.vector_ar.vecm import coint_johansen

# Test for cointegration
johansen_test = coint_johansen(df_multivariate, det_order=0, k_ar_diff=1)

# Fit VECM if cointegrated
from statsmodels.tsa.vector_ar.vecm import VECM

model = VECM(df_multivariate, k_ar_diff=1, coint_rank=1)
results = model.fit()
```

### 状态切换型号

用于结构断裂和政权变化。

```python
from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression

# Markov switching model
model = MarkovRegression(y, k_regimes=2, order=1)
results = model.fit()

# Smoothed probabilities of regimes
regime_probs = results.smoothed_marginal_probabilities
```

## 最佳实践

1. **检查平稳性**：如果需要差异，请使用 ADF/KPSS 测试 
2 进行验证。 **绘制数据**：在建模之前始终可视化
3. **识别季节性**：使用适当的季节性模型（SARIMAX、Holt-Winters）
4. **模型选择**：使用AIC/BIC和样本外验证
5. **残差诊断**：检查自相关、正态性、异方差
6. **预测评估**：使用滚动预测和适当的时间序列CV
7. **避免过度拟合**：更喜欢更简单的模型，使用信息标准
8. **文档假设**：注意任何数据转换（对数、差分）
9. **预测区间**：始终提供不确定性估计
10. **定期改装**：新数据到达时更新模型

## 常见陷阱

1. **不检查平稳性**：在非平稳数据
2上拟合ARIMA。 **数据泄漏**：在转换中使用未来数据
3. **错误的季节周期**：S=4 表示季度，S=12 表示每月
4. **过度拟合**：相对于data
5的参数太多。 **忽略残差自相关**：模型不充分
6. **使用不适当的指标**：MAPE 因零或负数而失败 
7. **不处理缺失数据**：影响模型估计
8. **外推外生变量**：需要 SARIMAX
9 的未来 X 值。 **令人困惑的静态与动态预测**：对于多步骤
10，动态更加现实。 **不验证预测**：始终检查样本外的表现
