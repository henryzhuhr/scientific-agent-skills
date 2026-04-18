# 广义线性模型 (GLM)参考

本文档提供了 statsmodels 中广义线性模型的全面指导，包括族、链接函数和应用程序。

## 概述

GLM 通过：
1 将线性回归扩展到非正态响应分布。 **分布族**：指定响应
2 的条件分布。 **链接函数**：将线性预测变量转换为均值
3 的尺度。 **方差函数**：将方差与均值相关

* *一般形式**：g(μ) = Xβ，其中 g 是链接函数，μ = E(Y|X)

## 何时使用 GLM

- **二元结果**：逻辑回归（具有 logit 链接的二项式族）
- **计数数据**：泊松或负二项式回归
- **正连续数据**：伽马或逆高斯
- **非正态分布**：当违反OLS假设时
- **链接函数**：需要预测变量和响应尺度之间的非线性关系

## 分布族

### 二项式系列

用于二元结果（0/1）或比例（k/n）。

* *何时使用：**
- 二元分类
- 成功/失败结果
- 比例或比率

* *常用链接：**
- Logit（默认）： log(μ/(1-μ))
- 概率：Φ⁻1(μ)
- 对数：log(μ)

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Binary logistic regression
model = sm.GLM(y, X, family=sm.families.Binomial())
results = model.fit()

# Formula API
results = smf.glm('success ~ x1 + x2', data=df,
                  family=sm.families.Binomial()).fit()

# Access predictions (probabilities)
probs = results.predict(X_new)

# Classification (0.5 threshold)
predictions = (probs > 0.5).astype(int)
```

* *解释：**
```python
import numpy as np

# Odds ratios (for logit link)
odds_ratios = np.exp(results.params)
print("Odds ratios:", odds_ratios)

# For 1-unit increase in x, odds multiply by exp(beta)
```

### 泊松系列

用于计数数据（非负整数）。

* *何时使用：**
- 计数结果（事件数量）
- 罕见事件
- 速率建模（带偏移）

* *常用链接：**
- 日志（默认）： log(μ)
- 身份：μ
- 平方：√μ

```python
# Poisson regression
model = sm.GLM(y, X, family=sm.families.Poisson())
results = model.fit()

# With exposure/offset for rates
# If modeling rate = counts/exposure
model = sm.GLM(y, X, family=sm.families.Poisson(),
               offset=np.log(exposure))
results = model.fit()

# Interpretation: exp(beta) = multiplicative effect on expected count
import numpy as np
rate_ratios = np.exp(results.params)
print("Rate ratios:", rate_ratios)
```

* *过度分散检查：**
```python
# Deviance / df should be ~1 for Poisson
overdispersion = results.deviance / results.df_resid
print(f"Overdispersion: {overdispersion}")

# If >> 1, consider Negative Binomial
if overdispersion > 1.5:
    print("Consider Negative Binomial model for overdispersion")
```

### 负二项式族

用于过度分散计数data.

* *何时使用：**
- 计数方差 > 平均值的数据
- 零过多或方差较大
- 泊松模型显示过度分散

```python
# Negative Binomial GLM
model = sm.GLM(y, X, family=sm.families.NegativeBinomial())
results = model.fit()

# Alternative: use discrete choice model with alpha estimation
from statsmodels.discrete.discrete_model import NegativeBinomial
nb_model = NegativeBinomial(y, X)
nb_results = nb_model.fit()

print(f"Dispersion parameter alpha: {nb_results.params[-1]}")
```

### 高斯族

相当于 OLS，但通过 IRLS（迭代重新加权最小二乘法）拟合。

* *何时使用：**
- 希望 GLM 框架保持一致性
- 需要强大的标准误差
- 与其他 GLM 比较

* *常见链接：**
- 身份（默认）： μ
- 对数：log(μ)
- 逆：1/μ

```python
# Gaussian GLM (equivalent to OLS)
model = sm.GLM(y, X, family=sm.families.Gaussian())
results = model.fit()

# Verify equivalence with OLS
ols_results = sm.OLS(y, X).fit()
print("Parameters close:", np.allclose(results.params, ols_results.params))
```

### Gamma 系列

用于正连续数据，通常右偏。

* *何时使用：**
- 积极结果（保险索赔、生存）次）
- 右偏分布
- 方差与平均值成正比²

* *常用链接：**
- 逆（默认）：1/μ
- 对数：log(μ)
- 身份： μ

```python
# Gamma regression (common for cost data)
model = sm.GLM(y, X, family=sm.families.Gamma())
results = model.fit()

# Log link often preferred for interpretation
model = sm.GLM(y, X, family=sm.families.Gamma(link=sm.families.links.Log()))
results = model.fit()

# With log link, exp(beta) = multiplicative effect
import numpy as np
effects = np.exp(results.params)
```

### 逆高斯族

适用于具有特定方差结构的正连续数据。

* *何时使用：**
- 正偏结果
- 方差与均值成比例³
- 替代Gamma

* *常用链接：**
- 平方反比（默认）：1/μ²
- Log：log(μ)

```python
model = sm.GLM(y, X, family=sm.families.InverseGaussian())
results = model.fit()
```

### Tweedie Family

涵盖多个分布的灵活系列。

* *何时使用：**
- 保险索赔（零和连续的混合）
- 半连续数据
- 需要灵活的方差函数

* *特殊情况（幂参数p）：**
- p=0：正常
- p=1：泊松
- p=2：Gamma
- p=3：逆高斯
- 1<p<2：复合泊松伽玛（保险常见）

```python
# Tweedie with power=1.5
model = sm.GLM(y, X, family=sm.families.Tweedie(link=sm.families.links.Log(),
                                                 var_power=1.5))
results = model.fit()
```

## 链接函数

链接函数将线性预测器连接到response.

### 可用链接

```python
from statsmodels.genmod import families

# Identity: g(μ) = μ
link = families.links.Identity()

# Log: g(μ) = log(μ)
link = families.links.Log()

# Logit: g(μ) = log(μ/(1-μ))
link = families.links.Logit()

# Probit: g(μ) = Φ⁻¹(μ)
link = families.links.Probit()

# Complementary log-log: g(μ) = log(-log(1-μ))
link = families.links.CLogLog()

# Inverse: g(μ) = 1/μ
link = families.links.InversePower()

# Inverse squared: g(μ) = 1/μ²
link = families.links.InverseSquared()

# Square root: g(μ) = √μ
link = families.links.Sqrt()

# Power: g(μ) = μ^p
link = families.links.Power(power=2)
```

### 选择链接函数

* *规范链接**（每个系列默认）：
- 二项式 → Logit
- 泊松 → Log
- 伽玛 →逆
- 高斯→恒等式
- 逆高斯→逆平方

* *何时使用非规范：**
- **与二项式的日志链接**：风险比而不是优势比
- **恒等链接**：直接累加效应（合理时）
- **Probit vs Logit**：类似结果，基于字段的偏好
- **CLogLog**：不对称关系，生存中常见分析

```python
# Example: Risk ratios with log-binomial model
model = sm.GLM(y, X, family=sm.families.Binomial(link=sm.families.links.Log()))
results = model.fit()

# exp(beta) now gives risk ratios, not odds ratios
risk_ratios = np.exp(results.params)
```

## 模型拟合和结果

### 基本工作流程

```python
import statsmodels.api as sm

# Add constant
X = sm.add_constant(X_data)

# Specify family and link
family = sm.families.Poisson(link=sm.families.links.Log())

# Fit model using IRLS
model = sm.GLM(y, X, family=family)
results = model.fit()

# Summary
print(results.summary())
```

### 结果属性

```python
# Parameters and inference
results.params              # Coefficients
results.bse                 # Standard errors
results.tvalues            # Z-statistics
results.pvalues            # P-values
results.conf_int()         # Confidence intervals

# Predictions
results.fittedvalues       # Fitted values (μ)
results.predict(X_new)     # Predictions for new data

# Model fit statistics
results.aic                # Akaike Information Criterion
results.bic                # Bayesian Information Criterion
results.deviance           # Deviance
results.null_deviance      # Null model deviance
results.pearson_chi2       # Pearson chi-squared statistic
results.df_resid           # Residual degrees of freedom
results.llf                # Log-likelihood

# Residuals
results.resid_response     # Response residuals (y - μ)
results.resid_pearson      # Pearson residuals
results.resid_deviance     # Deviance residuals
results.resid_anscombe     # Anscombe residuals
results.resid_working      # Working residuals
```

### 伪R-squared

```python
# McFadden's pseudo R-squared
pseudo_r2 = 1 - (results.deviance / results.null_deviance)
print(f"Pseudo R²: {pseudo_r2:.4f}")

# Adjusted pseudo R-squared
n = len(y)
k = len(results.params)
adj_pseudo_r2 = 1 - ((n-1)/(n-k)) * (results.deviance / results.null_deviance)
print(f"Adjusted Pseudo R²: {adj_pseudo_r2:.4f}")
```

## 诊断

### 拟合优度

```python
# Deviance should be approximately χ² with df_resid degrees of freedom
from scipy import stats

deviance_pval = 1 - stats.chi2.cdf(results.deviance, results.df_resid)
print(f"Deviance test p-value: {deviance_pval}")

# Pearson chi-squared test
pearson_pval = 1 - stats.chi2.cdf(results.pearson_chi2, results.df_resid)
print(f"Pearson chi² test p-value: {pearson_pval}")

# Check for overdispersion/underdispersion
dispersion = results.pearson_chi2 / results.df_resid
print(f"Dispersion: {dispersion}")
# Should be ~1; >1 suggests overdispersion, <1 underdispersion
```

### 残差分析

```python
import matplotlib.pyplot as plt

# Deviance residuals vs fitted
plt.figure(figsize=(10, 6))
plt.scatter(results.fittedvalues, results.resid_deviance, alpha=0.5)
plt.xlabel('Fitted values')
plt.ylabel('Deviance residuals')
plt.axhline(y=0, color='r', linestyle='--')
plt.title('Deviance Residuals vs Fitted')
plt.show()

# Q-Q plot of deviance residuals
from statsmodels.graphics.gofplots import qqplot
qqplot(results.resid_deviance, line='s')
plt.title('Q-Q Plot of Deviance Residuals')
plt.show()

# For binary outcomes: binned residual plot
if isinstance(results.model.family, sm.families.Binomial):
    from statsmodels.graphics.gofplots import qqplot
    # Group predictions and compute average residuals
    # (custom implementation needed)
    pass
```

### 影响和离群值

```python
from statsmodels.stats.outliers_influence import GLMInfluence

influence = GLMInfluence(results)

# Leverage
leverage = influence.hat_matrix_diag

# Cook's distance
cooks_d = influence.cooks_distance[0]

# DFFITS
dffits = influence.dffits[0]

# Find influential observations
influential = np.where(cooks_d > 4/len(y))[0]
print(f"Influential observations: {influential}")
```

## 假设检验

```python
# Wald test for single parameter (automatically in summary)

# Likelihood ratio test for nested models
# Fit reduced model
model_reduced = sm.GLM(y, X_reduced, family=family).fit()
model_full = sm.GLM(y, X_full, family=family).fit()

# LR statistic
lr_stat = 2 * (model_full.llf - model_reduced.llf)
df = model_full.df_model - model_reduced.df_model

from scipy import stats
lr_pval = 1 - stats.chi2.cdf(lr_stat, df)
print(f"LR test p-value: {lr_pval}")

# Wald test for multiple parameters
# Test beta_1 = beta_2 = 0
R = [[0, 1, 0, 0], [0, 0, 1, 0]]
wald_test = results.wald_test(R)
print(wald_test)
```

## 稳健标准误差

```python
# Heteroscedasticity-robust (sandwich estimator)
results_robust = results.get_robustcov_results(cov_type='HC0')

# Cluster-robust
results_cluster = results.get_robustcov_results(cov_type='cluster',
                                                groups=cluster_ids)

# Compare standard errors
print("Regular SE:", results.bse)
print("Robust SE:", results_robust.bse)
```

## 模型比较

```python
# AIC/BIC for non-nested models
models = [model1_results, model2_results, model3_results]
for i, res in enumerate(models, 1):
    print(f"Model {i}: AIC={res.aic:.2f}, BIC={res.bic:.2f}")

# Likelihood ratio test for nested models (as shown above)

# Cross-validation for predictive performance
from sklearn.model_selection import KFold
from sklearn.metrics import log_loss

kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = []

for train_idx, val_idx in kf.split(X):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]

    model_cv = sm.GLM(y_train, X_train, family=family).fit()
    pred_probs = model_cv.predict(X_val)

    score = log_loss(y_val, pred_probs)
    cv_scores.append(score)

print(f"CV Log Loss: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")
```

## 预测

```python
# Point predictions
predictions = results.predict(X_new)

# For classification: get probabilities and convert
if isinstance(family, sm.families.Binomial):
    probs = predictions
    class_predictions = (probs > 0.5).astype(int)

# For counts: predictions are expected counts
if isinstance(family, sm.families.Poisson):
    expected_counts = predictions

# Prediction intervals via bootstrap
n_boot = 1000
boot_preds = np.zeros((n_boot, len(X_new)))

for i in range(n_boot):
    # Bootstrap resample
    boot_idx = np.random.choice(len(y), size=len(y), replace=True)
    X_boot, y_boot = X[boot_idx], y[boot_idx]

    # Fit and predict
    boot_model = sm.GLM(y_boot, X_boot, family=family).fit()
    boot_preds[i] = boot_model.predict(X_new)

# 95% prediction intervals
pred_lower = np.percentile(boot_preds, 2.5, axis=0)
pred_upper = np.percentile(boot_preds, 97.5, axis=0)
```

## 常见应用

### 逻辑回归（二元分类）

```python
import statsmodels.api as sm

# Fit logistic regression
X = sm.add_constant(X_data)
model = sm.GLM(y, X, family=sm.families.Binomial())
results = model.fit()

# Odds ratios
odds_ratios = np.exp(results.params)
odds_ci = np.exp(results.conf_int())

# Classification metrics
from sklearn.metrics import classification_report, roc_auc_score

probs = results.predict(X)
predictions = (probs > 0.5).astype(int)

print(classification_report(y, predictions))
print(f"AUC: {roc_auc_score(y, probs):.4f}")

# ROC curve
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

fpr, tpr, thresholds = roc_curve(y, probs)
plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()
```

### 泊松回归（计数数据）

```python
# Fit Poisson model
X = sm.add_constant(X_data)
model = sm.GLM(y_counts, X, family=sm.families.Poisson())
results = model.fit()

# Rate ratios
rate_ratios = np.exp(results.params)
print("Rate ratios:", rate_ratios)

# Check overdispersion
dispersion = results.pearson_chi2 / results.df_resid
if dispersion > 1.5:
    print(f"Overdispersion detected ({dispersion:.2f}). Consider Negative Binomial.")
```

### 伽玛回归（成本/持续时间数据）

```python
# Fit Gamma model with log link
X = sm.add_constant(X_data)
model = sm.GLM(y_cost, X,
               family=sm.families.Gamma(link=sm.families.links.Log()))
results = model.fit()

# Multiplicative effects
effects = np.exp(results.params)
print("Multiplicative effects on mean:", effects)
```

## 最佳实践

1. **检查分布假设**：绘制响应
2 的直方图和Q-Q 图。 **验证链接功能**：使用规范链接，除非有理由不使用
3. **检查残差**：偏差残差应近似正常 
4. **过度分散测试**：特别适用于泊松模型
5. **适当使用偏移量**：对于不同曝光度的速率建模
6. **考虑稳健的SE**：当方差假设有问题时
7. **比较模型**：使用AIC/BIC进行非嵌套，LR测试用于嵌套
8. **按原始比例解释**：变换系数（例如，对数链接的 exp）
9. **检查有影响的观察结果**：使用库克距离
10. **验证预测**：使用交叉验证或保留集

## 常见陷阱

1. **忘记添加常量**：无截距项
2. **使用错误的系列**：检查响应
3的分布。 **忽略过度离散**：使用负二项式代替 Poisson
4. **误解系数**：记住链接函数变换
5. **不检查收敛**：IRLS 可能不会收敛；检查警告
6. **逻辑上完全分离**：某些类别完美预测结果
7. **使用具有有限结果的身份链接**：可以预测有效范围之外的
8. **将模型与不同样本进行比较**：使用相同的观察结果
9. **忘记速率模型中的偏移量**：必须使用 log(exposure)作为偏移量
10. **不考虑替代方案**：混合模型，复杂数据的零膨胀
