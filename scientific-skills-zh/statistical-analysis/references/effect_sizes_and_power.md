# 效应量和功效分析

本文件提供了计算、解释和报告效应量以及为研究计划进行功效分析的指导。

## 为什么效应量很重要

1. **统计显着性≠实际显着性**：p 值仅表明效应是否存在，而不表明效应有多大
2. **依赖于样本大小**：对于大样本，微不足道的影响变得“显着”
3. **解释**：效应大小提供了幅度和实际重要性
4. **荟萃分析**：效应大小能够合并跨研究的结果
5. **功效分析**：确定样本量所需

* *黄金法则**：始终报告效应大小以及 p 值。

- --

## 按分析类型划分的效应大小

### T 检验和均值差

#### Cohen d（标准化平均值）差异）

* *公式**：
- 独立组：d = (M₁ - M2)/SD_pooled
- 配对组：d = M_diff / SD_diff

* *解释**（Cohen，1988）：
- 小：|d| = 0.20
- 中：|d| = 0.50
- 大：|d| = 0.80

* *上下文相关的解释**：
- 在教育中：d = 0.40 是成功干预的典型
- 在心理学中：d = 0.40 被认为是有意义的
- 在医学中：小的效应量可能具有临床重要意义

* *Python计算**:
```python
import pingouin as pg
import numpy as np

# Independent t-test with effect size
result = pg.ttest(group1, group2, correction=False)
cohens_d = result['cohen-d'].values[0]

# Manual calculation
mean_diff = np.mean(group1) - np.mean(group2)
pooled_std = np.sqrt((np.var(group1, ddof=1) + np.var(group2, ddof=1)) / 2)
cohens_d = mean_diff / pooled_std

# Paired t-test
result = pg.ttest(pre, post, paired=True)
cohens_d = result['cohen-d'].values[0]
```

* *d 的置信区间**:
```python
from pingouin import compute_effsize_from_t

d, ci = compute_effsize_from_t(t_statistic, nx=n1, ny=n2, eftype='cohen')
```

- --

#### Hedges' g (Bias-Corrected d)

* *为什么使用它**：Cohen 的 d 有轻微向上小样本偏差 (n < 20)

* *公式**：g = d × Correction_factor，其中 Correction_factor = 1 - 3/(4df - 1)

* *Python 计算**：
```python
result = pg.ttest(group1, group2, correction=False)
hedges_g = result['hedges'].values[0]
```

* *当 **：
- 样本量较小时使用 Hedges' g （每组 n < 20）
- 进行荟萃分析（荟萃分析中的标准）

- --

#### Glass's Δ (Delta)

* *何时使用**：当一组是具有已知变异性的对照时

* *公式**：Δ = (M₁ - M2) / SD_control

* *使用案例**：
- 临床试验（使用对照组 SD）
- 当治疗影响变异性时

- --

### ANOVA

#### Eta 平方 (η²)

* *它是什么度量**：由因子 

 解释的总方差比例**公式**： η² = SS_effect / SS_total

* *解释**：
- 小： η² = 0.01（方差的 1%）
- 中： η² = 0.06（方差的 6%）
- 大： η² = 0.14（14% 方差）

* *限制**：多个因素存在偏差（总和 > 1.0）

* *Python 计算**：
```python
import pingouin as pg

# One-way ANOVA
aov = pg.anova(dv='value', between='group', data=df)
eta_squared = aov['SS'][0] / aov['SS'].sum()

# Or use pingouin directly
aov = pg.anova(dv='value', between='group', data=df, detailed=True)
eta_squared = aov['np2'][0]  # Note: pingouin reports partial eta-squared
```

- --

#### 部分 Eta 平方(η²_p)

* *测量的内容**：由因子解释的方差比例，排除其他因素

* *公式**： η²_p = SS_effect / (SS_effect + SS_error)

* *解释**：与 η²

 相同的基准**何时使用**：多因子方差分析（阶乘标准）设计）

* *Python计算**：
```python
aov = pg.anova(dv='value', between=['factor1', 'factor2'], data=df)
# pingouin reports partial eta-squared by default
partial_eta_sq = aov['np2']
```

- --

#### 欧米伽平方（ω²）

* *它测量什么**：群体方差的较少偏差估计解释

* *为什么使用它**：η²高估了效应大小； ω² 提供更好的总体估计

* *公式**： ω² = (SS_effect - df_effect × MS_error) / (SS_total + MS_error)

* *解释**：与 η² 相同的基准，但通常较小的值

* *Python计算**：
```python
def omega_squared(aov_table):
    ss_effect = aov_table.loc[0, 'SS']
    ss_total = aov_table['SS'].sum()
    ms_error = aov_table.loc[aov_table.index[-1], 'MS']  # Residual MS
    df_effect = aov_table.loc[0, 'DF']

    omega_sq = (ss_effect - df_effect * ms_error) / (ss_total + ms_error)
    return omega_sq
```

- --

#### Cohen's f

* *它测量什么**：方差分析的效应大小（类似于Cohen's d）

* *公式**：f = √(η² / (1 - η²))

* *解释**：
- 小：f = 0.10
- 中：f = 0.25
- 大：f = 0.40

* *Python计算**：
```python
eta_squared = 0.06  # From ANOVA
cohens_f = np.sqrt(eta_squared / (1 - eta_squared))
```

* *用于功效分析**：ANOVA功效计算所需

- --

### 相关性

#### Pearson's r / Spearman's ρ

* *解释**：
- 小：|r| = 0.10
- 中：|r| = 0.30
- 大：|r| = 0.50

* *重要说明**：
- r² = 决定系数（解释方差比例）
- r = 0.30 表示 9% 共享方差 (0.30² = 0.09)
- 考虑方向（正/负）和上下文

* *Python计算**：
```python
import pingouin as pg

# Pearson correlation with CI
result = pg.corr(x, y, method='pearson')
r = result['r'].values[0]
ci = [result['CI95%'][0][0], result['CI95%'][0][1]]

# Spearman correlation
result = pg.corr(x, y, method='spearman')
rho = result['r'].values[0]
```

- --

### 回归

#### R²（决定系数）

* *它测量什么**：模型解释的Y中方差的比例

* *解释**：
- 小：R² = 0.02
- 中：R2 = 0.13
- 大：R2 = 0.26

* *上下文相关**：
- 物理科学：R2 > 0.90 预期
- 社会科学：R2 > 0.30 视为良好
- 行为预测：R² > 0.10可能有意义

* *Python计算**：
```python
from sklearn.metrics import r2_score
from statsmodels.api import OLS

# Using statsmodels
model = OLS(y, X).fit()
r_squared = model.rsquared
adjusted_r_squared = model.rsquared_adj

# Manual
r_squared = 1 - (SS_residual / SS_total)
```

- --

#### 调整后的R²

* *为什么用**：R²在添加预测变量时人为增加；调整后的 R² 会惩罚模型复杂性

* *公式**：R²_adj = 1 - (1 - R²) × (n - 1) / (n - k - 1)

* *何时使用**：始终与 R² 一起报告多元回归

- --

#### 标准化回归系数(β)

* *它测量什么**：预测变量的一 SD 变化对结果的影响（以 SD 单位表示）

* *解释**：与 Cohen 的 d
 类似 - 小：|β| = 0.10
- 中：|β| = 0.30
- 大：|β| = 0.50

* *Python 计算**：
```python
from scipy import stats

# Standardize variables first
X_std = (X - X.mean()) / X.std()
y_std = (y - y.mean()) / y.std()

model = OLS(y_std, X_std).fit()
beta = model.params
```

- --

#### f²（科恩回归的 f 平方）

* *测量的内容**：单个预测变量或模型比较的效果大小

* *公式**：f² = R2_AB - R2_A / (1 - R2_AB)

其中：
- R2_AB = R2（带预测器的完整模型）
- R2_A = R2（不带预测器的简化模型）

* *解释**：
- 小：f2 = 0.02
- 中：f² = 0.15
- 大：f² = 0.35

* *Python 计算**：
```python
# Compare two nested models
model_full = OLS(y, X_full).fit()
model_reduced = OLS(y, X_reduced).fit()

r2_full = model_full.rsquared
r2_reduced = model_reduced.rsquared

f_squared = (r2_full - r2_reduced) / (1 - r2_full)
```

- --

### 分类数据分析

#### Cramér 的 V

* *它测量什么**：χ2 测试的关联强度（适用于任何表格大小）

* *公式**：V = √(χ2/(n × (k - 1)))

其中 k = min(行、列)

* *解释**（对于 k > 2）：
- 小：V = 0.07
- 中：V = 0.21
- 大：V = 0.35

* *对于 2×2 表**：使用 phi 系数 (φ)

* *Python计算**：
```python
from scipy.stats.contingency import association

# Cramér's V
cramers_v = association(contingency_table, method='cramer')

# Phi coefficient (for 2x2)
phi = association(contingency_table, method='pearson')
```

- --

#### 优势比（OR）和风险比（RR）

* *对于2×2列联表**：

|           |结果 + |结果 - |
|-----------|-----------|-----------|
|暴露|一个 | b |
|未曝光 | c | d |

* *优势比**：OR = (a/b) / (c/d) = ad / bc

* *解释**：
- OR = 1：无关联
- OR > 1：正相关（优势增加）
- OR < 1：负相关（降低赔率）
- OR = 2：赔率的两倍
- OR = 0.5：赔率的一半

* *风险比**：RR = (a/(a+b)) / (c/(c+d))

* *何时使用**：
- 队列研究：使用 RR（更多可解释）
- 病例对照研究：使用OR（RR不可用）
- 逻辑回归：OR是自然输出

* *Python计算**：
```python
import statsmodels.api as sm

# From contingency table
odds_ratio = (a * d) / (b * c)

# Confidence interval
table = np.array([[a, b], [c, d]])
oddsratio, pvalue = stats.fisher_exact(table)

# From logistic regression
model = sm.Logit(y, X).fit()
odds_ratios = np.exp(model.params)  # Exponentiate coefficients
ci = np.exp(model.conf_int())  # Exponentiate CIs
```

- --

### 贝叶斯效应大小

#### 贝叶斯因子(BF)

* *它测量什么**：替代假设与原假设的证据比率

* *解释**：
- BF₁₀ = 1：H₁ 和 H₀ 的证据相同 
- BF₁₀ = 3：H₁ 的可能性是 H₀ 的 3 倍（中等）证据）
- BF₁₀ = 10：H₁ 的可能性是 H₀ 的 10 倍（强有力的证据）
- BF₁₀ = 100：H₁ 的可能性是 H₀ 的 100 倍（决定性证据）
- BF₁₀ = 0.33： H₀ 的可能性是 H₁
- BF₁₀ = 0.10 的 3 倍：H₀ 的可能性是 H₁

 的 10 倍**分类** (Jeffreys, 1961)：
- 1-3：轶事证据
- 3-10：中等证据
- 10-30：强有力的证据
- 30-100：非常有力的证据
- >100：决定性证据

* *Python计算**：
```python
import pingouin as pg

# Bayesian t-test
result = pg.ttest(group1, group2, correction=False)
# Note: pingouin doesn't include BF; use other packages

# Using JASP or BayesFactor (R) via rpy2
# Or implement using numerical integration
```

- --

## Power分析

### 概念

* *统计功效**：检测到效果（如果存在）的概率 (1 - β)

* *常规标准**：
- 功效 = 0.80（检测效果的概率为 80%）
- α = 0.05（5% I 类误差）率）

* *四个相互关联的参数**（给定 3 个，可以求解第 4 个）：
1. 样本大小 (n)
2. 效应大小（d、f等）
3. 显着性水平(α)
4. 功效（1 - β）

- --

### 先验功效分析（规划）

* *目的**：在研究之前确定所需的样本量

* *步骤**：
1. 指定预期效果大小（来自文献、试验数据或最小有意义的效果）
2. 设置 α 水平（通常为 0.05）
3. 设置所需功率（通常为 0.80）
4. 计算所需的 n

* *Python 实现**：
```python
from statsmodels.stats.power import (
    tt_ind_solve_power,
    zt_ind_solve_power,
    FTestAnovaPower,
    NormalIndPower
)

# T-test power analysis
n_required = tt_ind_solve_power(
    effect_size=0.5,  # Cohen's d
    alpha=0.05,
    power=0.80,
    ratio=1.0,  # Equal group sizes
    alternative='two-sided'
)

# ANOVA power analysis
anova_power = FTestAnovaPower()
n_per_group = anova_power.solve_power(
    effect_size=0.25,  # Cohen's f
    ngroups=3,
    alpha=0.05,
    power=0.80
)

# Correlation power analysis
from pingouin import power_corr
n_required = power_corr(r=0.30, power=0.80, alpha=0.05)
```

- --

### 事后功耗分析（研究后）

* *⚠️ 注意**：事后功耗是有争议的，通常不推荐

* *为什么它有问题**：
- 观察到的功效是p值的直接函数
- 如果p> 0.05，功效始终很低
- 除了p值之外不提供其他信息
- 可能会产生误导

* *何时可以接受**：
- 未来的研究计划研究
- 使用多项研究（不仅仅是您自己的）的效应量
- 明确的目标是复制的样本量

* *更好的替代方案**：
- 报告效应量的置信区间
- 进行敏感性分析
- 报告最小可检测效应size

- --

### 敏感性分析

* *目的**：确定给定研究参数的最小可检测效应大小

* *何时使用**：研究完成后，了解研究的能力

* *Python实施**：
```python
# What effect size could we detect with n=50 per group?
detectable_effect = tt_ind_solve_power(
    effect_size=None,  # Solve for this
    nobs1=50,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)

print(f"With n=50 per group, we could detect d ≥ {detectable_effect:.2f}")
```

- --

## 报告效果大小

### APA风格指南

* *T-测试示例**：
> “A组（M = 75.2，SD = 8.5）得分显着高于B组（M = 68.3, SD = 9.2), t(98) = 3.82, p < .001, d = 0.77, 95% CI [0.36, 1.18]。"

* *方差分析示例**:
> "治疗条件对测试分数有显着的主效应，F(2, 87) = 8.45， p < .001，η²p = .16 使用 Tukey 的 HSD 进行事后比较发现...“

。**相关示例**：
> “学习时间和考试成绩之间存在中度正相关，r(148) = .42, p < .001, 95% CI [.27, .55]。”

* *回归示例**：
> “回归模型显着预测考试成绩，F(3, 146) = 45.2, p < .001，R² = .48。学习时间 (β = .52，p < .001)和之前的 GPA (β = .31，p < .001)是显着的预测因子。"

* *贝叶斯示例**：
> "贝叶斯独立样本 t 检验为组间差异提供了强有力的证据，BF₁₀ = 23.5，表明 H₁ 下的数据可能性是 H₀ 下的 23.5 倍。“

- --

## 效应大小陷阱

1. **不要只依赖基准**：背景很重要；小影响也可能有意义
2. **报告置信区间**：CI 显示效应大小估计的精度
3. **区分统计意义与实际意义**：大 n 可以使微不足道的影响变得“显着”
4. **考虑成本效益**：如果干预成本较低，即使很小的影响也可能很有价值
5. **多种结果**：效果大小因结果而异；报告全部
6. **不要挑选**：报告所有计划分析的效果
7. **发表偏差**：发表的效果常常被高估

- --

## 快速参考表

|分析|效应大小|小|中等|大|
|----------|-------------|--------|--------|------|
| T 检验 |科恩的 d | 0.20 | 0.20 0.50 | 0.50 0.80 |
|方差分析 | η², ω² | 0.01 | 0.01 0.06 | 0.06 0.14 |
|方差分析 |科恩的 f | 0.10 | 0.10 0.25 | 0.25 0.40 |
|相关性| r, ρ | 0.10 | 0.10 0.30 | 0.30 0.50 |
|回归 | R²| 0.02 | 0.02 0.13 | 0.13 0.26 |
|回归 | f² | 0.02 | 0.02 0.15 | 0.15 0.35 |
|卡方|克拉梅尔的 V | 0.07 | 0.07 0.21 | 0.21 0.35 |
|卡方 (2×2) | φ | 0.10 | 0.10 0.30 | 0.30 0.50 |

- --

## 资源

- 科恩，J. (1988)。 *行为科学的统计功效分析*（第二版）
- Lakens, D. (2013)。计算和报告效应大小
- Ellis, P. D. (2010)。 *效应大小基本指南*
