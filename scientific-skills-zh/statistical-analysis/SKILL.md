---
name: statistical-analysis
description: 通过测试选择和报告指导统计分析。当您需要帮助为您的数据选择适当的测试、假设检查、功效分析和 APA 格式的结果时使用。最适合学术研究报告、考试选择指导。要以编程方式实现特定模型，请使用 statsmodels。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 统计分析

## 概述

统计分析是检验假设和量化关系的系统过程。通过假设检查和 APA 报告进行假设检验（t 检验、方差分析、卡方）、回归、相关性和贝叶斯分析。将此技能应用于学术研究。

## 何时使用此技能

此技能应在以下情况下使用：
- 进行统计假设检验（t 检验、方差分析、卡方）
- 执行回归或相关分析
- 运行贝叶斯统计分析
- 检查统计假设和诊断
- 计算效应大小并进行功效分析
- 以APA 格式报告统计结果
- 分析研究实验或观察数据

- --

## 核心功能

### 1. 测试选择和规划
- 根据以下条件选择适当的统计测试研究问题和数据特征
- 进行先验功效分析以确定所需的样本量
- 计划分析策略，包括多重比较校正

### 2. 假设检查
- 在运行测试之前自动验证所有相关假设
- 提供诊断可视化（Q-Q 图、残差图、方框图）图）
- 在违反假设时建议采取补救措施

### 3. 统计测试
- 假设检验：t 检验、方差分析、卡方、非参数替代
- 回归：线性、多重、逻辑、带诊断
- 相关性： Pearson、Spearman，带置信区间
- 贝叶斯替代方案：贝叶斯 t 检验、方差分析、贝叶斯因子回归

### 4. 效应大小和解释
- 计算和解释所有分析的适当效应大小
- 为效应估计提供置信区间
- 区分实际意义统计

### 5. 专业报告
- 生成 APA 风格的统计报告
- 创建可供发布的图形和表格
- 提供所有所需统计数据的完整解释

- --

## 工作流程决策树

使用此决策树来确定您的分析路径：

```
START
│
├─ Need to SELECT a statistical test?
│  └─ YES → See "Test Selection Guide"
│  └─ NO → Continue
│
├─ Ready to check ASSUMPTIONS?
│  └─ YES → See "Assumption Checking"
│  └─ NO → Continue
│
├─ Ready to run ANALYSIS?
│  └─ YES → See "Running Statistical Tests"
│  └─ NO → Continue
│
└─ Need to REPORT results?
   └─ YES → See "Reporting Results"
```

- --

## 测试选择指南

### 快速参考：选择正确的测试

使用 `references/test_selection_guide.md` 进行全面指导。快速参考：

* *比较两组：**
- 独立、连续、正态 → 独立 t 检验 
- 独立、连续、非正态 → Mann-Whitney U 检验 
- 配对、连续、正态 → 配对 t 检验
- 配对、连续、非正态 → Wilcoxon符号秩检验
- 二元结果→卡方或费舍尔精确检验

* *比较3个以上组：**
- 独立、连续、正态→单向方差分析
- 独立、连续、非正态→克鲁斯卡尔-沃利斯检验
- 配对、连续、正态→重复测量ANOVA
- 配对、连续、非正态 → Friedman 检验

* *关系：**
- 两个连续变量 → Pearson（正态）或 Spearman 相关（非正态）
- 具有预测变量的连续结果 → 线性回归
- 具有预测变量的二元结果 → 逻辑回归

* *贝叶斯替代方案：**
所有测试都有贝叶斯版本，提供：
- 有关假设的直接概率陈述
- 贝叶斯因子量化证据
- 支持原假设的能力
- 参见`references/bayesian_statistics.md`

- --

## 假设检查

### 系统假设验证

* *在解释测试结果之前始终检查假设。**

使用提供的`scripts/assumption_checks.py`模块进行自动检查：

```python
from scripts.assumption_checks import comprehensive_assumption_check

# Comprehensive check with visualizations
results = comprehensive_assumption_check(
    data=df,
    value_col='score',
    group_col='group',  # Optional: for group comparisons
    alpha=0.05
)
```

这执行：
1. **异常值检测**（IQR 和 z 分数方法）
2. **正态性检验**（Shapiro-Wilk 检验 + Q-Q 图）
3. **方差同质性**（Levene 检验 + 箱线图）
4. **解释和建议**

### 单独假设检查

对于有针对性的检查，请使用单独函数：

```python
from scripts.assumption_checks import (
    check_normality,
    check_normality_per_group,
    check_homogeneity_of_variance,
    check_linearity,
    detect_outliers
)

# Example: Check normality with visualization
result = check_normality(
    data=df['score'],
    name='Test Score',
    alpha=0.05,
    plot=True
)
print(result['interpretation'])
print(result['recommendation'])
```

### 违反假设时该怎么办

* *违反正态性：**
- 轻度违反 + 每组 n > 30 → 继续使用参数检验（稳健）
- 中度违规 → 使用非参数替代方案
- 严重违规 → 转换数据或使用非参数检验

* *违反方差齐性：**
- 对于 t 检验 → 使用 Welch 的 t 检验
- 对于方差分析 → 使用Welch 方差分析或 Brown-Forsythe ANOVA
- 对于回归 → 使用稳健标准误差或加权最小二乘

* *违反线性（回归）：**
- 添加多项式项
- 变换变量
- 使用非线性模型或 GAM

参见`references/assumptions_and_diagnostics.md` 用于全面指导。

- --

## 运行统计测试

### Python 库

用于统计分析的主要库：
- **scipy.stats**：核心统计测试
- **statsmodels**：高级回归和诊断
- **pingouin**：具有效应大小的用户友好统计测试
- **pymc**：贝叶斯统计建模
- **arviz**：贝叶斯可视化和诊断

### 示例分析

#### 完整的T 测试报告

```python
import pingouin as pg
import numpy as np

# Run independent t-test
result = pg.ttest(group_a, group_b, correction='auto')

# Extract results
t_stat = result['T'].values[0]
df = result['dof'].values[0]
p_value = result['p-val'].values[0]
cohens_d = result['cohen-d'].values[0]
ci_lower = result['CI95%'].values[0][0]
ci_upper = result['CI95%'].values[0][1]

# Report
print(f"t({df:.0f}) = {t_stat:.2f}, p = {p_value:.3f}")
print(f"Cohen's d = {cohens_d:.2f}, 95% CI [{ci_lower:.2f}, {ci_upper:.2f}]")
```

#### 带事后测试的方差分析

```python
import pingouin as pg

# One-way ANOVA
aov = pg.anova(dv='score', between='group', data=df, detailed=True)
print(aov)

# If significant, conduct post-hoc tests
if aov['p-unc'].values[0] < 0.05:
    posthoc = pg.pairwise_tukey(dv='score', between='group', data=df)
    print(posthoc)

# Effect size
eta_squared = aov['np2'].values[0]  # Partial eta-squared
print(f"Partial η² = {eta_squared:.3f}")
```

#### 带诊断的线性回归

```python
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Fit model
X = sm.add_constant(X_predictors)  # Add intercept
model = sm.OLS(y, X).fit()

# Summary
print(model.summary())

# Check multicollinearity (VIF)
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)

# Check assumptions
residuals = model.resid
fitted = model.fittedvalues

# Residual plots
import matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Residuals vs fitted
axes[0, 0].scatter(fitted, residuals, alpha=0.6)
axes[0, 0].axhline(y=0, color='r', linestyle='--')
axes[0, 0].set_xlabel('Fitted values')
axes[0, 0].set_ylabel('Residuals')
axes[0, 0].set_title('Residuals vs Fitted')

# Q-Q plot
from scipy import stats
stats.probplot(residuals, dist="norm", plot=axes[0, 1])
axes[0, 1].set_title('Normal Q-Q')

# Scale-Location
axes[1, 0].scatter(fitted, np.sqrt(np.abs(residuals / residuals.std())), alpha=0.6)
axes[1, 0].set_xlabel('Fitted values')
axes[1, 0].set_ylabel('√|Standardized residuals|')
axes[1, 0].set_title('Scale-Location')

# Residuals histogram
axes[1, 1].hist(residuals, bins=20, edgecolor='black', alpha=0.7)
axes[1, 1].set_xlabel('Residuals')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title('Histogram of Residuals')

plt.tight_layout()
plt.show()
```

#### 贝叶斯T-Test

```python
import pymc as pm
import arviz as az
import numpy as np

with pm.Model() as model:
    # Priors
    mu1 = pm.Normal('mu_group1', mu=0, sigma=10)
    mu2 = pm.Normal('mu_group2', mu=0, sigma=10)
    sigma = pm.HalfNormal('sigma', sigma=10)

    # Likelihood
    y1 = pm.Normal('y1', mu=mu1, sigma=sigma, observed=group_a)
    y2 = pm.Normal('y2', mu=mu2, sigma=sigma, observed=group_b)

    # Derived quantity
    diff = pm.Deterministic('difference', mu1 - mu2)

    # Sample
    trace = pm.sample(2000, tune=1000, return_inferencedata=True)

# Summarize
print(az.summary(trace, var_names=['difference']))

# Probability that group1 > group2
prob_greater = np.mean(trace.posterior['difference'].values > 0)
print(f"P(μ₁ > μ₂ | data) = {prob_greater:.3f}")

# Plot posterior
az.plot_posterior(trace, var_names=['difference'], ref_val=0)
```

- --

## 效应大小

### 始终计算效应大小

* *效应大小量化幅度，而 p 值仅指示效应的存在。**

 有关全面信息，请参阅 `references/effect_sizes_and_power.md`指导.

### 快速参考：常见效应大小

|测试|效应大小|小|中等|大|
|------|-------------|--------|--------|--------|
| T 检验 |科恩的 d | 0.20 | 0.20 0.50 | 0.50 0.80 |
|方差分析 | η²_p | 0.01 | 0.01 0.06 | 0.06 0.14 |
|相关性| r | 0.10 | 0.10 0.30 | 0.30 0.50 |
|回归 | R²| 0.02 | 0.02 0.13 | 0.13 0.26 |
|卡方|克拉梅尔的 V | 0.07 | 0.07 0.21 | 0.21 0.35 |

* *重要**：基准是指南。上下文很重要！

### 计算效应大小

大多数效应大小由 pingouin 自动计算：

```python
# T-test returns Cohen's d
result = pg.ttest(x, y)
d = result['cohen-d'].values[0]

# ANOVA returns partial eta-squared
aov = pg.anova(dv='score', between='group', data=df)
eta_p2 = aov['np2'].values[0]

# Correlation: r is already an effect size
corr = pg.corr(x, y)
r = corr['r'].values[0]
```

### 效应大小的置信区间

始终报告要显示的 CI precision：

```python
from pingouin import compute_effsize_from_t

# For t-test
d, ci = compute_effsize_from_t(
    t_statistic,
    nx=len(group1),
    ny=len(group2),
    eftype='cohen'
)
print(f"d = {d:.2f}, 95% CI [{ci[0]:.2f}, {ci[1]:.2f}]")
```

- --

## 功效分析

### 先验功效分析（研究计划）

在数据收集之前确定所需的样本量：

```python
from statsmodels.stats.power import (
    tt_ind_solve_power,
    FTestAnovaPower
)

# T-test: What n is needed to detect d = 0.5?
n_required = tt_ind_solve_power(
    effect_size=0.5,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)
print(f"Required n per group: {n_required:.0f}")

# ANOVA: What n is needed to detect f = 0.25?
anova_power = FTestAnovaPower()
n_per_group = anova_power.solve_power(
    effect_size=0.25,
    ngroups=3,
    alpha=0.05,
    power=0.80
)
print(f"Required n per group: {n_per_group:.0f}")
```

### 敏感性分析（研究后）

确定您可以检测到的效应大小：

```python
# With n=50 per group, what effect could we detect?
detectable_d = tt_ind_solve_power(
    effect_size=None,  # Solve for this
    nobs1=50,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)
print(f"Study could detect d ≥ {detectable_d:.2f}")
```

* *注意**：一般不建议进行事后功效分析（研究后计算功效）。请改用敏感性分析。

请参阅 `references/effect_sizes_and_power.md` 了解详细指导。

- --

## 报告结果

### APA 风格统计报告

遵循 `references/reporting_standards.md` 中的指南。

### 基本报告元件

1. **描述性统计**：所有组/变量
2的M、SD、n。 **检验统计数据**：检验名称、统计量、df、精确 p 值
3. **效果大小**：置信区间为 
4. **假设检查**：进行了哪些测试、结果、采取的操作
5. **所有计划分析**：包括非显着性结果

### 示例报告模板

#### 独立 T 检验

```
Group A (n = 48, M = 75.2, SD = 8.5) scored significantly higher than
Group B (n = 52, M = 68.3, SD = 9.2), t(98) = 3.82, p < .001, d = 0.77,
95% CI [0.36, 1.18], two-tailed. Assumptions of normality (Shapiro-Wilk:
Group A W = 0.97, p = .18; Group B W = 0.96, p = .12) and homogeneity
of variance (Levene's F(1, 98) = 1.23, p = .27) were satisfied.
```

#### 单向方差分析 

```
A one-way ANOVA revealed a significant main effect of treatment condition
on test scores, F(2, 147) = 8.45, p < .001, η²_p = .10. Post hoc
comparisons using Tukey's HSD indicated that Condition A (M = 78.2,
SD = 7.3) scored significantly higher than Condition B (M = 71.5,
SD = 8.1, p = .002, d = 0.87) and Condition C (M = 70.1, SD = 7.9,
p < .001, d = 1.07). Conditions B and C did not differ significantly
(p = .52, d = 0.18).
```

#### 多重回归

```
Multiple linear regression was conducted to predict exam scores from
study hours, prior GPA, and attendance. The overall model was significant,
F(3, 146) = 45.2, p < .001, R² = .48, adjusted R² = .47. Study hours
(B = 1.80, SE = 0.31, β = .35, t = 5.78, p < .001, 95% CI [1.18, 2.42])
and prior GPA (B = 8.52, SE = 1.95, β = .28, t = 4.37, p < .001,
95% CI [4.66, 12.38]) were significant predictors, while attendance was
not (B = 0.15, SE = 0.12, β = .08, t = 1.25, p = .21, 95% CI [-0.09, 0.39]).
Multicollinearity was not a concern (all VIF < 1.5).
```

#### 贝叶斯分析

```
A Bayesian independent samples t-test was conducted using weakly
informative priors (Normal(0, 1) for mean difference). The posterior
distribution indicated that Group A scored higher than Group B
(M_diff = 6.8, 95% credible interval [3.2, 10.4]). The Bayes Factor
BF₁₀ = 45.3 provided very strong evidence for a difference between
groups, with a 99.8% posterior probability that Group A's mean exceeded
Group B's mean. Convergence diagnostics were satisfactory (all R̂ < 1.01,
ESS > 1000).
```

- --

## 贝叶斯统计

### 何时使用贝叶斯方法

在以下情况下考虑贝叶斯方法：
- 您有要合并的先验信息
- 您需要有关假设的直接概率陈述
- 样本量较小或计划连续数据收集
- 您需要量化原假设的证据
- 模型很复杂（分层、缺失数据）

参见`references/bayesian_statistics.md` 用于全面指导：
- 贝叶斯定理和解释
- 先验规范（信息性、弱信息性、非信息性）
- 使用贝叶斯因子进行贝叶斯假设检验
- 可信区间与置信区间
- 贝叶斯 t 检验、方差分析、回归和分层模型
- 模型收敛检查和后验预测检查

### 主要优点

1. **直观解释**：“根据数据，该参数有 95% 的概率位于该区间内”
2. **无效的证据**：可以量化对无效的支持
3. **灵活**：无 p-hacking 问题；可以在数据到达时对其进行分析
4. **不确定性量化**：全后验分布

- --

## 资源

本技能包含综合参考资料：

### 参考资料目录

- **test_selection_guide.md**：选择适当统计检验的决策树
- **assections_and_diagnostics.md**：检查和处理假设违规的详细指南
- **effect_sizes_and_power.md**：计算、解释和报告效应大小；进行功效分析
- **bayesian_statistics.md**：贝叶斯分析方法完整指南
- **reporting_standards.md**：带有示例的APA风格报告指南

### 脚本目录

- **assume_checks.py**：使用可视化进行自动假设检查
  - `comprehensive_assumption_check()`：完整工作流程
  - `check_normality()`：使用Q-Q图进行正态性测试
  - `check_homogeneity_of_variance()`：使用箱线图进行Levene检验
  - `check_linearity()`：回归线性检查
  - `detect_outliers()`：IQR 和 z 分数异常值检测

- --

## 最佳实践

1. **预注册分析**尽可能区分验证性和探索性
2. **在解释结果之前始终检查假设**
3. **报告效果大小**，置信区间为 
4. **报告所有计划的分析**包括非显着结果
5. **区分统计意义和实际意义**
6. **分析前后的数据可视化**
7. **检查诊断**回归/方差分析（残差图、VIF 等）
8. **进行敏感性分析**以评估稳健性
9. **共享数据和代码**以实现可重复性
10. **对违规、转换和决策保持透明**

- --

## 要避免的常见陷阱

1. **P-hacking**：在某些事情变得重要之前不要测试多种方法
2. **HARKing**：不要将探索性发现作为证实性的
3. **忽略假设**：检查它们并报告违规情况
4. **混淆显着性与重要性**：p < .05 ≠ 有意义的效果
5. **不报告效应大小**：对于解释至关重要
6. **精选结果**：报告所有计划分析
7. **误解 p 值**：它们不是假设为真的概率 
8. **多重比较**：在适当的情况下纠正系列错误
9. **忽略缺失数据**：了解机制（MCAR、MAR、MNAR）
10. **过度解释非显着性结果**：缺乏证据≠缺乏证据

- --

## 入门清单

开始统计分析时：

- [ ]定义研究问题和假设
- [ ]确定适当的统计检验（使用test_selection_guide.md）
- [ ]进行功效分析以确定样本大小
- [ ]加载并检查数据
- [ ]检查缺失数据和异常值
- [ ]使用验证假设假设_checks.py
- [ ]运行主要分析
- [ ]使用置信区间计算效应大小
- [ ]如果需要，进行事后测试（带修正）
- [ ]创建可视化
- [ ]按照reporting_standards.md
- [ ]进行敏感性分析分析
- [ ]共享数据和代码

- --

## 支持和进一步阅读

有关以下问题：
- **测试选择**：参见references/test_selection_guide.md
- **假设**：参见references/assurations_and_diagnostics.md
- **效果大小**：参见references/effect_sizes_and_power.md
- **贝叶斯方法**：参见references/bayesian_statistics.md
- **报告**：参见references/reporting_standards.md

* *Key教科书**：
- Cohen, J. (1988)。 *行为科学的统计功效分析*
- Field, A. (2013)。 *使用 IBM SPSS Statistics 发现统计数据*
  - Gelman, A., & Hill, J. (2006)。 *使用回归和多级/分层模型进行数据分析*
- Kruschke, J. K. (2014)。 *进行贝叶斯数据分析*

* *在线资源**：
- APA 风格指南：https://apastyle.apa.org/
- 统计咨询：交叉验证 (stats.stackexchange.com)
