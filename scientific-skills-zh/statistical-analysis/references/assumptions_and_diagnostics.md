# 统计假设和诊断程序

本文件提供有关检查和验证各种分析的统计假设的全面指导。

## 一般原则

1. **在解释测试结果之前始终检查假设**
2. **使用多种诊断方法**（目视+形式测试）
3. **考虑稳健性**：某些测试在某些条件下对于违规行为具有稳健性
4. **在分析报告中记录所有假设检查**
5. **报告违规行为并采取补救措施**

## 测试中的常见假设

### 1. 观察的独立性

 * *含义**：每个观察都是独立的； 

* *如何检查**：
- 审查研究设计和数据收集程序
- 对于时间序列：检查自相关性（ACF/PACF 图、Durbin-Watson 检验）
- 对于聚类数据：考虑类内相关性 (ICC)

* *如果出现这种情况该怎么办违反**：
- 对聚类/分层数据使用混合效应模型
- 对时间相关数据使用时间序列方法
- 对相关数据使用广义估计方程（GEE）

* *严重严重性**：高-违规会严重夸大I类数据误差

- --

### 2. 正态性

* *含义**：数据或残差遵循正态（高斯）分布。

* *需要时**：
- t 检验（适用于小样本；每组 n > 30 时稳健）
- 方差分析（适用于小样本）样本；每组 n > 30 时稳健）
- 线性回归（对于残差）
- 一些相关性测试（皮尔逊）

* *如何检查**：

* *视觉方法**（主要）：
- Q-Q（分位数-分位数）图：点应落在对角线上line
- 具有正态曲线叠加的直方图
- 核密度图

* *正式测试**（次要）：
- Shapiro-Wilk 测试（建议 n < 50）
- Kolmogorov-Smirnov 测试
- Anderson-Darling 测试

* *Python 实现**：
```python
from scipy import stats
import matplotlib.pyplot as plt

# Shapiro-Wilk test
statistic, p_value = stats.shapiro(data)

# Q-Q plot
stats.probplot(data, dist="norm", plot=plt)
```

* *解释指导**：
- 对于 n < 30：目视和形式测试都很重要
- 对于 30 ≤ n < 100：目视检查为主，形式测试次要
- 对于 n ≥ 100：形式测试过于敏感；依靠目视检查
- 寻找严重偏斜、离群值或双峰

* *如果违反怎么办**：
- **轻度违规**（轻微偏斜）：如果每组 n > 30，则继续
- **中度违规**：使用非参数替代方案（Mann-Whitney、Mann-Whitney、 Kruskal-Wallis, Wilcoxon)
- **严重违规**：
  - 转换数据（对数、平方根、Box-Cox）
  - 使用非参数方法
  - 使用稳健的回归方法
  - 考虑引导

  * *严重严重性**：中- 参数检验对于具有足够样本量的轻度违规通常具有鲁棒性

- --

### 3. 方差齐性（Homoscedasticity）

* *含义**：组间或预测变量范围内的方差相等。

* *需要时**：
- 独立样本t-test
- ANOVA
- 线性回归（残差恒定方差）

* *如何检查**：

* *视觉方法**（主要）：
- 按组划分的箱线图（用于 t 检验/方差分析）
- 残差与拟合值图（用于回归） - 应显示随机散点
- 尺度位置图（标准化残差与拟合的平方根）

* *正式测试**（次要）：
- Levene 测试（对非正态性稳健）
- Bartlett 测试（对非正态性敏感，不推荐）
- Brown-Forsythe 检验（基于中位数的 Levene 版本）
- Breusch-Pagan 检验（用于回归）

* *Python 实现**：
```python
from scipy import stats
import pingouin as pg

# Levene's test
statistic, p_value = stats.levene(group1, group2, group3)

# For regression
# Breusch-Pagan test
from statsmodels.stats.diagnostic import het_breuschpagan
_, p_value, _, _ = het_breuschpagan(residuals, exog)
```

* *解释指导**：
- 方差比（最大/分钟）< 2-3：一般可接受
- 对于方差分析：如果组大小相等，测试是稳健的
- 对于回归：在残差图中查找漏斗模式

* *做什么如果违反**：
- **t-test**：使用 Welch 的 t 检验（不假设方差相等）
- **ANOVA**：使用 Welch 的 ANOVA 或 Brown-Forsythe ANOVA
- **回归**：
  - 变换因变量（对数、平方根）
  - 使用加权最小二乘法 (WLS)
  - 使用稳健的标准误差 (HC3)
  - 使用具有适当方差函数的广义线性模型 (GLM)

* *严重程度**：中 - 使用相同的样本量进行测试可以保持稳健

- --

## 测试特定假设

### T 检验

* *假设**：
1. 观察的独立性
2. 正态性（每组进行独立t检验；差异进行配对t检验）
3. 方差齐性（仅限独立 t 检验）

* *诊断工作流程**：
```python
import scipy.stats as stats
import pingouin as pg

# Check normality for each group
stats.shapiro(group1)
stats.shapiro(group2)

# Check homogeneity of variance
stats.levene(group1, group2)

# If assumptions violated:
# Option 1: Welch's t-test (unequal variances)
pg.ttest(group1, group2, correction=False)  # Welch's

# Option 2: Non-parametric alternative
pg.mwu(group1, group2)  # Mann-Whitney U
```

- --

### ANOVA

* *假设**：
1. 组内和组间观察的独立性
2. 每组的正态性为
3. 组间方差同质性

* *其他注意事项**：
- 对于重复测量方差分析：球形度假设（莫奇利检验）

* *诊断工作流程**：
```python
import pingouin as pg

# Check normality per group
for group in df['group'].unique():
    data = df[df['group'] == group]['value']
    stats.shapiro(data)

# Check homogeneity of variance
pg.homoscedasticity(df, dv='value', group='group')

# For repeated measures: Check sphericity
# Automatically tested in pingouin's rm_anova
```

* *如果违反球形度该怎么办**（重复措施）：
- Greenhouse-Geisser 校正 (ε < 0.75)
- Huynh-Feldt 校正 (ε > 0.75)
- 使用多元方法 (MANOVA)

- --

### 线性回归

* *假设**：
1. **线性**：X和Y之间的关系是线性的
2. **独立性**：残差是独立的
3. **同方差性**：残差 
4 的恒定方差。 **正态性**：残差呈正态分布
5. **无多重共线性**：预测变量不高度相关（多元回归）

* *诊断工作流程**：

* *1。线性**：
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Scatter plots of Y vs each X
# Residuals vs. fitted values (should be randomly scattered)
plt.scatter(fitted_values, residuals)
plt.axhline(y=0, color='r', linestyle='--')
```

* *2。独立**：
```python
from statsmodels.stats.stattools import durbin_watson

# Durbin-Watson test (for time series)
dw_statistic = durbin_watson(residuals)
# Values between 1.5-2.5 suggest independence
```

* *3。同方差**：
```python
# Breusch-Pagan test
from statsmodels.stats.diagnostic import het_breuschpagan
_, p_value, _, _ = het_breuschpagan(residuals, exog)

# Visual: Scale-location plot
plt.scatter(fitted_values, np.sqrt(np.abs(std_residuals)))
```

* *4。残差正态性**：
```python
# Q-Q plot of residuals
stats.probplot(residuals, dist="norm", plot=plt)

# Shapiro-Wilk test
stats.shapiro(residuals)
```

* *5。多重共线性**：
```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Calculate VIF for each predictor
vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

# VIF > 10 indicates severe multicollinearity
# VIF > 5 indicates moderate multicollinearity
```

* *违反怎么办**：
- **非线性**：添加多项式项，使用GAM，或变换变量
- **异方差**：变换Y，使用WLS，使用鲁棒SE
- **非正态残差**：变换 Y，使用稳健方法，检查异常值
- **多重共线性**：删除相关预测变量，使用 PCA，岭回归

- --

### 逻辑回归

* *假设**：
1. **独立性**：观察结果是独立的
2. **线性**：对数赔率和连续预测变量 
3 之间的线性关系。 **没有完美的多重共线性**：预测变量不完全相关
4. **大样本量**：每个预测因子至少 10-20 个事件

* *诊断工作流程**：

* *1。 logit的线性**：
```python
# Box-Tidwell test: Add interaction with log of continuous predictor
# If interaction is significant, linearity violated
```

* *2。多重共线性**：
```python
# Use VIF as in linear regression
```

* *3。有影响力的观察**：
```python
# Cook's distance, DFBetas, leverage
from statsmodels.stats.outliers_influence import OLSInfluence

influence = OLSInfluence(model)
cooks_d = influence.cooks_distance
```

* *4。模型拟合**：
```python
# Hosmer-Lemeshow test
# Pseudo R-squared
# Classification metrics (accuracy, AUC-ROC)
```

- --

## 异常值检测

* *方法**：
1. **视觉**：箱线图、散点图
2. **统计**：
  - Z 分数：|z| > 3 建议离群值
  - IQR 方法：值 < Q1 - 1.5×IQR 或 > Q3 + 1.5×IQR
  - 使用中值绝对偏差（对离群值稳健）修改后的 Z 分数

* *对于回归**：
- **杠杆**：高杠杆点（帽子值）
- **影响**：库克距离 > 4/n 建议影响点
- **离群值**：学生化残差 > ±3

* *做什么**：
1. 调查数据输入错误
2. 考虑异常值是否是有效的观测结果
3. 报告敏感性分析（有和没有异常值的结果）
4. 如果异常值合法，则使用稳健的方法

- --

## 样本大小注意事项

### 最小样本大小（经验规则）

- **T 检验**：每组 n ≥ 30，对于非正态性的稳健性
- **方差分析**：每组 n ≥ 30
- **相关性**：n ≥ 30 以获得足够的功效
- **简单回归**：n ≥ 50
- **多元回归**：每组 n ≥ 10-20预测变量（至少 10 + k 个预测变量）
- **逻辑回归**：每个预测变量 n ≥ 10-20 个事件

### 小样本注意事项

对于小样本：
- 假设变得更加关键
- 在可用时使用精确检验（Fisher 精确、精确逻辑回归）
- 考虑非参数替代方案
- 使用排列测试或引导方法
- 解释保守

- --

## 报告假设检查

报告分析时，包括：

1. **检查的假设声明**：列出所有测试的假设
2. **使用的方法**：描述所使用的视觉和形式测试
3. **诊断测试结果**：报告测试统计数据和 p 值
4. **评估**：说明是否满足或违反假设
5. **采取的措施**：如果违反，请描述补救措施（转换、替代测试、稳健方法）

* *报告声明示例**：
> “使用 Shapiro-Wilk 检验和 Q-Q 图评估正常性。A 组（W = 0.97，p = .18）和 B 组（W = 0.96，p = .12）的数据显示没有显着性使用 Levene 检验评估方差齐性，该检验不显着 (F(1, 58) = 1.23，p = .27），表明组间方差相等，因此满足独立样本 t 检验的假设。
