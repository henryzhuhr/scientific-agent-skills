# 离散选择模型参考

本文档提供了有关statsmodels中离散选择模型的全面指导，包括二元、多项、计数和序数模型。

## 概述

离散选择模型处理的结果为：
- **二元**：0/1，成功/失败
- **多项式**：多个无序类别
- **序数**：有序类别
- **计数**：非负整数

所有模型都使用最大似然估计并假设独立同分布。错误。

## 二元模型

### Logit（逻辑回归）

对二元结果使用逻辑分布。

* *何时使用：**
- 二元分类（是/否，成功/失败）
- 二元概率估计结果
- 可解释的比值比

* *模型**：P(Y=1|X) = 1 / (1 + exp(-Xβ))

```python
import statsmodels.api as sm
from statsmodels.discrete.discrete_model import Logit

# Prepare data
X = sm.add_constant(X_data)

# Fit model
model = Logit(y, X)
results = model.fit()

print(results.summary())
```

* *解释：**
```python
import numpy as np

# Odds ratios
odds_ratios = np.exp(results.params)
print("Odds ratios:", odds_ratios)

# For 1-unit increase in X, odds multiply by exp(β)
# OR > 1: increases odds of success
# OR < 1: decreases odds of success
# OR = 1: no effect

# Confidence intervals for odds ratios
odds_ci = np.exp(results.conf_int())
print("Odds ratio 95% CI:")
print(odds_ci)
```

* *边际效果：**
```python
# Average marginal effects (AME)
marginal_effects = results.get_margeff(at='mean')
print(marginal_effects.summary())

# Marginal effects at means (MEM)
marginal_effects_mem = results.get_margeff(at='mean', method='dydx')

# Marginal effects at representative values
marginal_effects_custom = results.get_margeff(at='mean',
                                              atexog={'x1': 1, 'x2': 5})
```

* *预测：**
```python
# Predicted probabilities
probs = results.predict(X)

# Binary predictions (0.5 threshold)
predictions = (probs > 0.5).astype(int)

# Custom threshold
threshold = 0.3
predictions_custom = (probs > threshold).astype(int)

# For new data
X_new = sm.add_constant(X_new_data)
new_probs = results.predict(X_new)
```

* *模型评估：**
```python
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score, roc_curve)

# Classification report
print(classification_report(y, predictions))

# Confusion matrix
print(confusion_matrix(y, predictions))

# AUC-ROC
auc = roc_auc_score(y, probs)
print(f"AUC: {auc:.4f}")

# Pseudo R-squared
print(f"McFadden's Pseudo R²: {results.prsquared:.4f}")
```

### Probit

对二进制使用正态分布结果。

* *何时使用：**
- 二元结果
- 更喜欢正态分布假设
- 字段约定（计量经济学经常使用概率）

* *模型**：P(Y=1|X) = Φ(Xβ)，其中 Φ 是标准正态分布CDF

```python
from statsmodels.discrete.discrete_model import Probit

model = Probit(y, X)
results = model.fit()

print(results.summary())
```

* *与Logit比较：**
- Probit和Logit通常给出相似的结果
- Probit：对称，基于正态分布
- Logit：尾部稍重，更容易解释（优势比）
- 系数不可直接比较（尺度差异）

```python
# Marginal effects are comparable
logit_me = logit_results.get_margeff().margeff
probit_me = probit_results.get_margeff().margeff

print("Logit marginal effects:", logit_me)
print("Probit marginal effects:", probit_me)
```

## 多项模型

### MNLogit（多项Logit）

用于具有3个以上类别的无序分类结果。

* *何时使用：**
- 多个无序类别（例如，运输方式、品牌选择）
- 类别之间没有自然排序
- 需要每个类别的概率

* *模型**： P(Y=j|X) = exp(Xβⱼ) / Σₖ exp(Xβₖ)

```python
from statsmodels.discrete.discrete_model import MNLogit

# y should be integers 0, 1, 2, ... for categories
model = MNLogit(y, X)
results = model.fit()

print(results.summary())
```

* *解释：**
```python
# One category is reference (usually category 0)
# Coefficients represent log-odds relative to reference

# For category j vs reference:
# exp(β_j) = odds ratio of category j vs reference

# Predicted probabilities for each category
probs = results.predict(X)  # Shape: (n_samples, n_categories)

# Most likely category
predicted_categories = probs.argmax(axis=1)
```

* *相对风险比：**
```python
# Exponentiate coefficients for relative risk ratios
import numpy as np
import pandas as pd

# Get parameter names and values
params_df = pd.DataFrame({
    'coef': results.params,
    'RRR': np.exp(results.params)
})
print(params_df)
```

### Conditional Logit

对于替代品具有特征的选择模型。

* *何时使用：**
- 替代特定回归量（因选择而异）
- 具有选择的面板数据
- 离散选择实验

```python
from statsmodels.discrete.conditional_models import ConditionalLogit

# Data structure: long format with choice indicator
model = ConditionalLogit(y_choice, X_alternatives, groups=individual_id)
results = model.fit()
```

## 计数模型

### 泊松

计数的标准模型data.

* *何时使用：**
- 计数结果（事件、发生次数）
- 罕见事件
- 均值 ≈ 方差

* *模型**： P(Y=k|X) = exp(-λ) λᵏ / k!，其中 log(λ) = Xβ

```python
from statsmodels.discrete.count_model import Poisson

model = Poisson(y_counts, X)
results = model.fit()

print(results.summary())
```

* *解释：**
```python
# Rate ratios (incident rate ratios)
rate_ratios = np.exp(results.params)
print("Rate ratios:", rate_ratios)

# For 1-unit increase in X, expected count multiplies by exp(β)
```

* *检查过度分散：**
```python
# Mean and variance should be similar for Poisson
print(f"Mean: {y_counts.mean():.2f}")
print(f"Variance: {y_counts.var():.2f}")

# Formal test
from statsmodels.stats.stattools import durbin_watson

# Overdispersion if variance >> mean
# Rule of thumb: variance/mean > 1.5 suggests overdispersion
overdispersion_ratio = y_counts.var() / y_counts.mean()
print(f"Variance/Mean: {overdispersion_ratio:.2f}")

if overdispersion_ratio > 1.5:
    print("Consider Negative Binomial model")
```

* *带偏移（对于率）：**
```python
# When modeling rates with varying exposure
# log(λ) = log(exposure) + Xβ

model = Poisson(y_counts, X, offset=np.log(exposure))
results = model.fit()
```

### 负二项式

对于过度分散的计数数据（方差 > 均值）。

* *何时使用：**
- 计数具有过度分散的数据
- 过多方差未解释泊松
- 计数异质性

* *模型**：添加色散参数α以解决过度色散

```python
from statsmodels.discrete.count_model import NegativeBinomial

model = NegativeBinomial(y_counts, X)
results = model.fit()

print(results.summary())
print(f"Dispersion parameter alpha: {results.params['alpha']:.4f}")
```

* *与泊松比较：**
```python
# Fit both models
poisson_results = Poisson(y_counts, X).fit()
nb_results = NegativeBinomial(y_counts, X).fit()

# AIC comparison (lower is better)
print(f"Poisson AIC: {poisson_results.aic:.2f}")
print(f"Negative Binomial AIC: {nb_results.aic:.2f}")

# Likelihood ratio test (if NB is better)
from scipy import stats
lr_stat = 2 * (nb_results.llf - poisson_results.llf)
lr_pval = 1 - stats.chi2.cdf(lr_stat, df=1)  # 1 extra parameter (alpha)
print(f"LR test p-value: {lr_pval:.4f}")

if lr_pval < 0.05:
    print("Negative Binomial significantly better")
```

### 零膨胀型号

用于带有多余零的计数数据。

* *何时使用：**
- 比泊松/NB
预期的零更多-两个过程：一个用于零，一个用于计数
- 示例：看医生的次数，保险索赔

* *型号：**
- ZeroInflatedPoisson (ZIP)
- ZeroInflatedNegativeBinomialP (ZINB)

```python
from statsmodels.discrete.count_model import (ZeroInflatedPoisson,
                                               ZeroInflatedNegativeBinomialP)

# ZIP model
zip_model = ZeroInflatedPoisson(y_counts, X, exog_infl=X_inflation)
zip_results = zip_model.fit()

# ZINB model (for overdispersion + excess zeros)
zinb_model = ZeroInflatedNegativeBinomialP(y_counts, X, exog_infl=X_inflation)
zinb_results = zinb_model.fit()

print(zip_results.summary())
```

* *两个部分型号：**
```python
# 1. Inflation model: P(Y=0 due to inflation)
# 2. Count model: distribution of counts

# Predicted probabilities of inflation
inflation_probs = zip_results.predict(X, which='prob')

# Predicted counts
predicted_counts = zip_results.predict(X, which='mean')
```

### 跨栏模型

两阶段模型：是否有计数，然后是多少。

* *何时使用：**
- 多余的零
- 零与正的不同过程计数
- 零在结构上不同于正值

```python
from statsmodels.discrete.count_model import HurdleCountModel

# Specify count distribution and zero inflation
model = HurdleCountModel(y_counts, X,
                         exog_infl=X_hurdle,
                         dist='poisson')  # or 'negbin'
results = model.fit()

print(results.summary())
```

## 序数模型

### 有序Logit/Probit

用于有序分类结果。

* *何时使用：**
- 有序类别（例如，低/中/高，评级 1-5）
- 自然排序很重要
- 想要尊重序数结构

* *模型**：有割点的累积概率模型

```python
from statsmodels.miscmodels.ordinal_model import OrderedModel

# y should be ordered integers: 0, 1, 2, ...
model = OrderedModel(y_ordered, X, distr='logit')  # or 'probit'
results = model.fit(method='bfgs')

print(results.summary())
```

* *解释：**
```python
# Cutpoints (thresholds between categories)
cutpoints = results.params[-n_categories+1:]
print("Cutpoints:", cutpoints)

# Coefficients
coefficients = results.params[:-n_categories+1]
print("Coefficients:", coefficients)

# Predicted probabilities for each category
probs = results.predict(X)  # Shape: (n_samples, n_categories)

# Most likely category
predicted_categories = probs.argmax(axis=1)
```

* *比例赔率假设：**
```python
# Test if coefficients are same across cutpoints
# (Brant test - implement manually or check residuals)

# Check: model each cutpoint separately and compare coefficients
```

## 模型诊断

### 拟合优度

```python
# Pseudo R-squared (McFadden)
print(f"Pseudo R²: {results.prsquared:.4f}")

# AIC/BIC for model comparison
print(f"AIC: {results.aic:.2f}")
print(f"BIC: {results.bic:.2f}")

# Log-likelihood
print(f"Log-likelihood: {results.llf:.2f}")

# Likelihood ratio test vs null model
lr_stat = 2 * (results.llf - results.llnull)
from scipy import stats
lr_pval = 1 - stats.chi2.cdf(lr_stat, results.df_model)
print(f"LR test p-value: {lr_pval}")
```

### 分类指标（二进制）

```python
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score)

# Predictions
probs = results.predict(X)
predictions = (probs > 0.5).astype(int)

# Metrics
print(f"Accuracy: {accuracy_score(y, predictions):.4f}")
print(f"Precision: {precision_score(y, predictions):.4f}")
print(f"Recall: {recall_score(y, predictions):.4f}")
print(f"F1: {f1_score(y, predictions):.4f}")
print(f"AUC: {roc_auc_score(y, probs):.4f}")
```

### 分类指标（多项）

```python
from sklearn.metrics import accuracy_score, classification_report, log_loss

# Predicted categories
probs = results.predict(X)
predictions = probs.argmax(axis=1)

# Accuracy
accuracy = accuracy_score(y, predictions)
print(f"Accuracy: {accuracy:.4f}")

# Classification report
print(classification_report(y, predictions))

# Log loss
logloss = log_loss(y, probs)
print(f"Log Loss: {logloss:.4f}")
```

### 计数模型诊断

```python
# Observed vs predicted frequencies
observed = pd.Series(y_counts).value_counts().sort_index()
predicted = results.predict(X)
predicted_counts = pd.Series(np.round(predicted)).value_counts().sort_index()

# Compare distributions
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
observed.plot(kind='bar', alpha=0.5, label='Observed', ax=ax)
predicted_counts.plot(kind='bar', alpha=0.5, label='Predicted', ax=ax)
ax.legend()
ax.set_xlabel('Count')
ax.set_ylabel('Frequency')
plt.show()

# Rootogram (better visualization)
from statsmodels.graphics.agreement import mean_diff_plot
# Custom rootogram implementation needed
```

### 影响和异常值

```python
# Standardized residuals
std_resid = (y - results.predict(X)) / np.sqrt(results.predict(X))

# Check for outliers (|std_resid| > 2)
outliers = np.where(np.abs(std_resid) > 2)[0]
print(f"Number of outliers: {len(outliers)}")

# Leverage (hat values) - for logit/probit
# from statsmodels.stats.outliers_influence
```

## 假设测试

```python
# Single parameter test (automatic in summary)

# Multiple parameters: Wald test
# Test H0: β₁ = β₂ = 0
R = [[0, 1, 0, 0], [0, 0, 1, 0]]
wald_test = results.wald_test(R)
print(wald_test)

# Likelihood ratio test for nested models
model_reduced = Logit(y, X_reduced).fit()
model_full = Logit(y, X_full).fit()

lr_stat = 2 * (model_full.llf - model_reduced.llf)
df = model_full.df_model - model_reduced.df_model
from scipy import stats
lr_pval = 1 - stats.chi2.cdf(lr_stat, df)
print(f"LR test p-value: {lr_pval:.4f}")
```

## 模型选择和比较

```python
# Fit multiple models
models = {
    'Logit': Logit(y, X).fit(),
    'Probit': Probit(y, X).fit(),
    # Add more models
}

# Compare AIC/BIC
comparison = pd.DataFrame({
    'AIC': {name: model.aic for name, model in models.items()},
    'BIC': {name: model.bic for name, model in models.items()},
    'Pseudo R²': {name: model.prsquared for name, model in models.items()}
})
print(comparison.sort_values('AIC'))

# Cross-validation for predictive performance
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression

# Use sklearn wrapper or manual CV
```

## 公式API

使用R式公式更容易指定。

```python
import statsmodels.formula.api as smf

# Logit with formula
formula = 'y ~ x1 + x2 + C(category) + x1:x2'
results = smf.logit(formula, data=df).fit()

# MNLogit with formula
results = smf.mnlogit(formula, data=df).fit()

# Poisson with formula
results = smf.poisson(formula, data=df).fit()

# Negative Binomial with formula
results = smf.negativebinomial(formula, data=df).fit()
```

## 通用应用

### 二元分类（营销响应）

```python
# Predict customer purchase probability
X = sm.add_constant(customer_features)
model = Logit(purchased, X)
results = model.fit()

# Targeting: select top 20% likely to purchase
probs = results.predict(X)
top_20_pct_idx = np.argsort(probs)[-int(0.2*len(probs)):]
```

### 多项选择（运输模式）

```python
# Predict transportation mode choice
model = MNLogit(mode_choice, X)
results = model.fit()

# Predicted mode for new commuter
new_commuter = sm.add_constant(new_features)
mode_probs = results.predict(new_commuter)
predicted_mode = mode_probs.argmax(axis=1)
```

### 计数数据（医生数量）访问次数）

```python
# Model healthcare utilization
model = NegativeBinomial(num_visits, X)
results = model.fit()

# Expected visits for new patient
expected_visits = results.predict(new_patient_X)
```

### 零膨胀（保险理赔）

```python
# Many people have zero claims
# Zero-inflation: some never claim
# Count process: those who might claim

zip_model = ZeroInflatedPoisson(claims, X_count, exog_infl=X_inflation)
results = zip_model.fit()

# P(never file claim)
never_claim_prob = results.predict(X, which='prob-zero')

# Expected claims
expected_claims = results.predict(X, which='mean')
```

## 最佳实践

1. **检查数据类型**：确保响应与模型（二进制、计数、类别）
2 匹配。 **添加常量**：始终使用 `sm.add_constant()` 除非不需要截取 
3. **缩放连续预测器**：为了更好的收敛和解释
4. **检查收敛**：查找收敛警告
5. **使用公式 API**：用于分类变量和交互
6. **边际效应**：报告边际效应，而不仅仅是系数
7. **模型比较**：使用AIC/BIC和交叉验证
8. **验证**：预测模型
9的保留集或交叉验证。 **检查过度分散**：对于计数模型，测试泊松假设
10. **考虑替代方案**：零通货膨胀、超额零的障碍模型

## 常见陷阱

1. **忘记常数**：无截距项
2. **完美分离**：Logit/probit 可能不会收敛
3. **使用具有过度离散的泊松**：检查并使用负二项式
4. **误解系数**：记住它们是对数赔率/对数尺度
5. **不检查收敛**：优化可能会默默失败
6. **分布错误**：将模型与数据类型（二进制/计数/分类）
7 匹配。 **忽略多余的零**：适当时使用 ZIP/ZINB
8. **不验证预测**：始终检查样本外性能
9. **比较非嵌套模型**：使用 AIC/BIC，而不是似然比检验 
10. **序数为名义**：对有序类别使用 OrderedModel
