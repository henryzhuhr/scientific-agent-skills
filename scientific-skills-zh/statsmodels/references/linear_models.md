# 线性回归模型参考

本文档提供了statsmodels中线性回归模型的详细指导，包括OLS、GLS、WLS、分位数回归和专门变体。

## 核心模型类

### OLS（普通最小二乘）

假设独立、同分布的误差（Σ=I）。最适合具有同方差误差的标准回归。

* *何时使用：**
- 标准回归分析
- 误差是独立的且具有恒定方差
- 无自相关或异方差
- 最常见的起点

* *基本用法：**
```python
import statsmodels.api as sm
import numpy as np

# Prepare data - ALWAYS add constant for intercept
X = sm.add_constant(X_data)  # Adds column of 1s for intercept

# Fit model
model = sm.OLS(y, X)
results = model.fit()

# View results
print(results.summary())
```

* *关键结果属性：**
```python
results.params           # Coefficients
results.bse              # Standard errors
results.tvalues          # T-statistics
results.pvalues          # P-values
results.rsquared         # R-squared
results.rsquared_adj     # Adjusted R-squared
results.fittedvalues     # Fitted values (predictions on training data)
results.resid            # Residuals
results.conf_int()       # Confidence intervals for parameters
```

* *带置信度/预测区间的预测：**
```python
# For in-sample predictions
pred = results.get_prediction(X)
pred_summary = pred.summary_frame()
print(pred_summary)  # Contains mean, std, confidence intervals

# For out-of-sample predictions
X_new = sm.add_constant(X_new_data)
pred_new = results.get_prediction(X_new)
pred_summary = pred_new.summary_frame()

# Access intervals
mean_ci_lower = pred_summary["mean_ci_lower"]
mean_ci_upper = pred_summary["mean_ci_upper"]
obs_ci_lower = pred_summary["obs_ci_lower"]  # Prediction intervals
obs_ci_upper = pred_summary["obs_ci_upper"]
```

* *公式API （R 型）：**
```python
import statsmodels.formula.api as smf

# Automatic handling of categorical variables and interactions
formula = 'y ~ x1 + x2 + C(category) + x1:x2'
results = smf.ols(formula, data=df).fit()
```

### WLS（加权最小二乘）

H处理异方差误差（对角 Σ），其中方差随观测值不同。

* *何时使用：**
- 已知异方差（非恒定误差）方差）
- 不同的观测值具有不同的可靠性
- 权重已知或可以估计

* *用法：**
```python
# If you know the weights (inverse variance)
weights = 1 / error_variance
model = sm.WLS(y, X, weights=weights)
results = model.fit()

# Common weight patterns:
# - 1/variance: when variance is known
# - n_i: sample size for grouped data
# - 1/x: when variance proportional to x
```

* *可行的WLS（估计权重）：**
```python
# Step 1: Fit OLS
ols_results = sm.OLS(y, X).fit()

# Step 2: Model squared residuals to estimate variance
abs_resid = np.abs(ols_results.resid)
variance_model = sm.OLS(np.log(abs_resid**2), X).fit()

# Step 3: Use estimated variance as weights
weights = 1 / np.exp(variance_model.fittedvalues)
wls_results = sm.WLS(y, X, weights=weights).fit()
```

### GLS（广义最小二乘法）

处理任意协方差结构（Σ）。其他回归方法的超类。

* *何时使用：**
- 已知协方差结构
- 相关错误
- 比 WLS

 更通用**用法：**
```python
# Specify covariance structure
# Sigma should be (n x n) covariance matrix
model = sm.GLS(y, X, sigma=Sigma)
results = model.fit()
```

### GLSAR（GLS 与自回归误差)

时间序列数据具有 AR(p)误差的可行广义最小二乘法。

* *何时使用：**
- 具有自相关误差的时间序列回归
- 需要考虑序列相关性
- 误差独立

* *用法：**
```python
# AR(1) errors
model = sm.GLSAR(y, X, rho=1)  # rho=1 for AR(1), rho=2 for AR(2), etc.
results = model.iterative_fit()  # Iteratively estimates AR parameters

print(results.summary())
print(f"Estimated rho: {results.model.rho}")
```

### RLS（递归最小二乘法）

顺序参数估计，对于自适应或在线学习很有用。

* *何时使用：**
- 参数随时间变化
- 在线/流数据
- 希望查看参数演变

* *用法：**
```python
from statsmodels.regression.recursive_ls import RecursiveLS

model = RecursiveLS(y, X)
results = model.fit()

# Access time-varying parameters
params_over_time = results.recursive_coefficients
cusum = results.cusum  # CUSUM statistic for structural breaks
```

### 滚动回归

跨移动窗口计算时变参数的估计

* *何时使用：**
- 参数随时间变化
- 想要检测结构变化
- 具有演变关系的时间序列

* *用法：**
```python
from statsmodels.regression.rolling import RollingOLS, RollingWLS

# Rolling OLS with 60-period window
rolling_model = RollingOLS(y, X, window=60)
rolling_results = rolling_model.fit()

# Extract time-varying parameters
rolling_params = rolling_results.params  # DataFrame with parameters over time
rolling_rsquared = rolling_results.rsquared

# Plot parameter evolution
import matplotlib.pyplot as plt
rolling_params.plot()
plt.title('Time-Varying Coefficients')
plt.show()
```

### 分位数回归

分析条件分位数而不是条件均值。

* *何时使用：**
- 对分位数的兴趣（中位数、第 90 个百分位数等）
- 对异常值具有鲁棒性（中位数回归）
- 分布效应分位数
- 异质效应

* *用法：**
```python
from statsmodels.regression.quantile_regression import QuantReg

# Median regression (50th percentile)
model = QuantReg(y, X)
results_median = model.fit(q=0.5)

# Multiple quantiles
quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]
results_dict = {}
for q in quantiles:
    results_dict[q] = model.fit(q=q)

# Plot quantile-varying effects
import matplotlib.pyplot as plt
coef_dict = {q: res.params for q, res in results_dict.items()}
coef_df = pd.DataFrame(coef_dict).T
coef_df.plot()
plt.xlabel('Quantile')
plt.ylabel('Coefficient')
plt.show()
```

## 混合效应模型

适用于具有随机效应的分层/嵌套数据。

* *何时使用：**
- 聚类/分组数据（学校中的学生、医院中的患者）
- 重复测量
- 需要随机效应来解释分组

* *用法：**
```python
from statsmodels.regression.mixed_linear_model import MixedLM

# Random intercept model
model = MixedLM(y, X, groups=group_ids)
results = model.fit()

# Random intercept and slope
model = MixedLM(y, X, groups=group_ids, exog_re=X_random)
results = model.fit()

print(results.summary())
```

## 诊断和模型评估

### 残差分析

```python
# Basic residual plots
import matplotlib.pyplot as plt

# Residuals vs fitted
plt.scatter(results.fittedvalues, results.resid)
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.axhline(y=0, color='r', linestyle='--')
plt.title('Residuals vs Fitted')
plt.show()

# Q-Q plot for normality
from statsmodels.graphics.gofplots import qqplot
qqplot(results.resid, line='s')
plt.show()

# Histogram of residuals
plt.hist(results.resid, bins=30, edgecolor='black')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Distribution of Residuals')
plt.show()
```

### 规格测试

```python
from statsmodels.stats.diagnostic import het_breuschpagan, het_white
from statsmodels.stats.stattools import durbin_watson, jarque_bera

# Heteroscedasticity tests
lm_stat, lm_pval, f_stat, f_pval = het_breuschpagan(results.resid, X)
print(f"Breusch-Pagan test p-value: {lm_pval}")

# White test
white_test = het_white(results.resid, X)
print(f"White test p-value: {white_test[1]}")

# Autocorrelation
dw_stat = durbin_watson(results.resid)
print(f"Durbin-Watson statistic: {dw_stat}")
# DW ~ 2 indicates no autocorrelation
# DW < 2 suggests positive autocorrelation
# DW > 2 suggests negative autocorrelation

# Normality test
jb_stat, jb_pval, skew, kurtosis = jarque_bera(results.resid)
print(f"Jarque-Bera test p-value: {jb_pval}")
```

### 多重共线性

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Calculate VIF for each variable
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print(vif_data)
# VIF > 10 indicates problematic multicollinearity
# VIF > 5 suggests moderate multicollinearity

# Condition number (from summary)
print(f"Condition number: {results.condition_number}")
# Condition number > 20 suggests multicollinearity
# Condition number > 30 indicates serious problems
```

### 影响统计数据

```python
from statsmodels.stats.outliers_influence import OLSInfluence

influence = results.get_influence()

# Leverage (hat values)
leverage = influence.hat_matrix_diag
# High leverage: > 2*p/n (p=predictors, n=observations)

# Cook's distance
cooks_d = influence.cooks_distance[0]
# Influential if Cook's D > 4/n

# DFFITS
dffits = influence.dffits[0]
# Influential if |DFFITS| > 2*sqrt(p/n)

# Create influence plot
from statsmodels.graphics.regressionplots import influence_plot
fig, ax = plt.subplots(figsize=(12, 8))
influence_plot(results, ax=ax)
plt.show()
```

### 假设检验

```python
# Test single coefficient
# H0: beta_i = 0 (automatically in summary)

# Test multiple restrictions using F-test
# Example: Test beta_1 = beta_2 = 0
R = [[0, 1, 0, 0], [0, 0, 1, 0]]  # Restriction matrix
f_test = results.f_test(R)
print(f_test)

# Formula-based hypothesis testing
f_test = results.f_test("x1 = x2 = 0")
print(f_test)

# Test linear combination: beta_1 + beta_2 = 1
r_matrix = [[0, 1, 1, 0]]
q_matrix = [1]  # RHS value
f_test = results.f_test((r_matrix, q_matrix))
print(f_test)

# Wald test (equivalent to F-test for linear restrictions)
wald_test = results.wald_test(R)
print(wald_test)
```

## 模型比较

```python
# Compare nested models using likelihood ratio test (if using MLE)
from statsmodels.stats.anova import anova_lm

# Fit restricted and unrestricted models
model_restricted = sm.OLS(y, X_restricted).fit()
model_full = sm.OLS(y, X_full).fit()

# ANOVA table for model comparison
anova_results = anova_lm(model_restricted, model_full)
print(anova_results)

# AIC/BIC for non-nested model comparison
print(f"Model 1 AIC: {model1.aic}, BIC: {model1.bic}")
print(f"Model 2 AIC: {model2.aic}, BIC: {model2.bic}")
# Lower AIC/BIC indicates better model
```

## 稳健标准误差

处理异方差或不重新加权的聚类。

```python
# Heteroscedasticity-robust (HC) standard errors
results_hc = results.get_robustcov_results(cov_type='HC0')  # White's
results_hc1 = results.get_robustcov_results(cov_type='HC1')
results_hc2 = results.get_robustcov_results(cov_type='HC2')
results_hc3 = results.get_robustcov_results(cov_type='HC3')  # Most conservative

# Newey-West HAC (Heteroscedasticity and Autocorrelation Consistent)
results_hac = results.get_robustcov_results(cov_type='HAC', maxlags=4)

# Cluster-robust standard errors
results_cluster = results.get_robustcov_results(cov_type='cluster',
                                                groups=cluster_ids)

# View robust results
print(results_hc3.summary())
```

## 最佳实践

1. **始终添加常量**：使用 `sm.add_constant()` 除非您特别想要排除拦截
2. **检查假设**：运行诊断测试（异方差、自相关、正态性）
3. **对分类变量使用公式API**：`smf.ols()` 自动处理分类变量
4. **稳健的标准误差**：当检测到异方差但模型规范正确时使用
5. **模型选择**：非嵌套模型使用AIC/BIC，嵌套模型使用F检验/似然比
6. **异常值和影响**：始终检查库克的距离和杠杆
7. **多重共线性**：解释前检查VIF和条件号
8. **时间序列**：使用 `GLSAR` 或稳健的 HAC 标准误差来处理自相关误差 
9. **分组数据**：考虑混合效应模型或集群稳健标准误差
10. **分位数回归**：用于稳健估计或对分布效应感兴趣时使用

## 常见陷阱

1. **忘记添加常量**：导致无截距模型
2. **忽略异方差**：使用 WLS 或稳健标准误
3. **使用带有自相关误差的 OLS**：使用 GLSAR 或 HAC 标准误差
4. **多重共线性的过度解释**：首先检查VIF
5. **不检查残差**：始终绘制残差与拟合值
6. **使用 t-SNE/PCA 残差**：残差应来自原始空间
7. **令人困惑的预测与置信区间**：预测区间更宽
8. **未正确处理分类变量**：使用公式 API 或手动虚拟编码
9. **比较具有不同样本量的模型**：确保使用相同的观察值
10. **忽略有影响的观察结果**：检查库克距离和 DFFITS
