# PyMC 分布参考

此参考提供了 PyMC 中可用的概率分布的综合目录，按类别组织。在构建贝叶斯模型时，使用此选项为先验和似然性选择适当的分布。

## 连续分布

连续分布定义实值域上的概率密度。

### 常见连续分布

* *`pm.Normal(name, mu, sigma)`**
- 正态（高斯）分布
- 参数：`mu`（均值）、`sigma`（标准差）
- 支持：(-∞, ∞)
- 常见用途：无界参数的默认先验、具有加性噪声的连续数据的似然

* *`pm.HalfNormal(name, sigma)`**
- 半正态分布（正一半正常）
- 参数：`sigma`（标准差）
- 支持：[0, ∞)
- 常见用途：尺度/标准差参数先验 

* *`pm.Uniform(name, lower, upper)`**
- 均匀分布
- 参数： `lower`、`upper`（边界）
- 支持：[下、上]
- 常见用途：当参数必须有界时提供弱信息先验

* *`pm.Beta(name, alpha, beta)`**
- Beta 分布
- 参数： `alpha`、`beta`（形状参数）
- 支持：[0, 1]
- 常见用途：概率和比例先验

* *`pm.Gamma(name, alpha, beta)`**
- 伽玛分布
- 参数： `alpha`（形状）、`beta`（速率）
- 支持：(0, ∞)
- 常见用途：正参数先验、速率参数

* *`pm.Exponential(name, lam)`**
- 指数分布
- 参数： `lam`（速率参数）
- 支持：[0, ∞)
- 常见用途：比例参数优先、等待时间

* *`pm.LogNormal(name, mu, sigma)`**
- 对数正态分布
- 参数：`mu`、 `sigma`（基础法线参数）
- 支持：(0, ∞)
- 常见用途：具有乘法效应的正参数先验

* *`pm.StudentT(name, nu, mu, sigma)`**
- 学生的 t 分布
- 参数：`nu`（自由度）、`mu`（位置）、`sigma`（尺度）
- 支持：(-∞, ∞)
- 常见用途：抗离群模型的正态稳健替代

* *`pm.Cauchy(name, alpha, beta)`**
- 柯西分布
- 参数：`alpha`（位置），`beta`（尺度）
- 支持：（-∞，∞）
- 常见用途：重尾替代到正态

### 专业连续分布

* *`pm.Laplace(name, mu, b)`** - 拉普拉斯（双指数）分布

* *`pm.AsymmetricLaplace(name, kappa, mu, b)`** - 非对称拉普拉斯分布

* *`pm.InverseGamma(name, alpha, beta)`** - 逆伽玛distribution

* *`pm.Weibull(name, alpha, beta)`** - 用于可靠性分析的威布尔分布

* *`pm.Logistic(name, mu, s)`** - Logistic 分布

* *`pm.LogitNormal(name, mu, sigma)`** - (0,1)支持的 Logit 正态分布

* *`pm.Pareto(name, alpha, m)`** - 帕累托分布幂律现象

* *`pm.ChiSquared(name, nu)`** - 卡方分布

* *`pm.ExGaussian(name, mu, sigma, nu)`** - 指数修正高斯

* *`pm.VonMises(name, mu, kappa)`** - Von Mises（圆形正态）分布

* *`pm.SkewNormal(name, mu, sigma, alpha)`** -偏斜正态分布

* *`pm.Triangular(name, lower, c, upper)`** - 三角分布

* *`pm.Gumbel(name, mu, beta)`** - 极值的Gumbel分布

* *`pm.Rice(name, nu, sigma)`** - 莱斯（莱斯）分布

* *`pm.Moyal(name, mu, sigma)`** - Moyal distribution

* *`pm.Kumaraswamy(name, a, b)`** - Kumaraswamy 分布（测试版替代方案）

* *`pm.Interpolated(name, x_points, pdf_points)`** - 插值的自定义分布

## 离散分布

离散分布定义整数值域上的概率。

### 常见离散分布

* *`pm.Bernoulli(name, p)`**
- 伯努利分布（二元结果）
- 参数：`p`（成功概率）
- 支持：{0, 1}
- 常见用途：二元分类、硬币翻转

* *`pm.Binomial(name, n, p)`**
- 二项分布
- 参数：`n`（试验次数）、`p`（成功概率）
- 支持：{0, 1, ..., n}
- 常见用途：固定的成功次数Trials

* *`pm.Poisson(name, mu)`**
- 泊松分布
- 参数：`mu`（速率参数）
- 支持：{0, 1, 2, ...}
- 常见用途：计数数据、速率、出现次数

* *`pm.Categorical(name, p)`**
- 分类分布
- 参数：`p`（概率向量）
- 支持：{0, 1, ..., K-1}
- 常见用途：多类分类

* *`pm.DiscreteUniform(name, lower, upper)`**
- 离散均匀分布
- 参数：`lower`、`upper`（边界）
- 支持：{lower, ..., upper}
- 常见用途：有限先验统一整数

* *`pm.NegativeBinomial(name, mu, alpha)`**
- 负二项分布
- 参数：`mu`（均值）、`alpha`（离散）
- 支持：{0, 1, 2, ...}
- 常见用途：过分散计数数据

* *`pm.Geometric(name, p)`**
- 几何分布
- 参数：`p`（成功概率）
- 支持：{0, 1, 2, ...}
- 常见用途：第一次之前的失败次数success

### 专业离散分布

* *`pm.BetaBinomial(name, alpha, beta, n)`** - Beta 二项式（过度分散二项式）

* *`pm.HyperGeometric(name, N, k, n)`** - 超几何分布

* *`pm.DiscreteWeibull(name, q, beta)`** - 离散威布尔distribution

* *`pm.OrderedLogistic(name, eta, cutpoints)`** - 序数数据的有序逻辑

* *`pm.OrderedProbit(name, eta, cutpoints)`** - 序数数据的有序概率

## 多元分布

多元分布定义向量值随机变量的联合概率分布。

### 常见多元分布

* *`pm.MvNormal(name, mu, cov)`**
- 多元正态分布
- 参数：`mu`（均值向量）、`cov`（协方差矩阵）
- 常见用途：相关连续变量、高斯过程

* *`pm.Dirichlet(name, a)`**
- 狄利克雷分布
- 参数：`a`（浓度参数）
- 支持：单纯形（总和为 1）
- 常见用途：概率向量先验、主题建模

* *`pm.Multinomial(name, n, p)`**
- 多项分布
- 参数：`n`（试验次数）、`p`（概率向量）
- 常见用途：对多个数据进行计数类别

* *`pm.MvStudentT(name, nu, mu, cov)`**
- 多元学生 t 分布
- 参数：`nu`（自由度）、`mu`（位置）、`cov`（尺度矩阵）
- 常见用途：鲁棒多元建模

### 专业多元分布

* *`pm.LKJCorr(name, n, eta)`** - LKJ 相关矩阵先验（对于相关矩阵）

* *`pm.LKJCholeskyCov(name, n, eta, sd_dist)`** - 使用 Cholesky 分解的 LKJ 先验

* *`pm.Wishart(name, nu, V)`** - Wishart 分布（对于协方差）矩阵）

* *`pm.InverseWishart(name, nu, V)`** - 逆 Wishart 分布

* *`pm.MatrixNormal(name, mu, rowcov, colcov)`** - 矩阵正态分布

* *`pm.KroneckerNormal(name, mu, covs, sigma)`** - 克罗内克结构正态

* *`pm.CAR(name, mu, W, alpha, tau)`** - 条件自回归(spatial)

* *`pm.ICAR(name, W, sigma)`** - 内在条件自回归 (spatial)

## 混合分布

混合分布结合了多个分量分布。

* *`pm.Mixture(name, w, comp_dists)`**
- 一般混合distribution
- 参数：`w`（权重）、`comp_dists`（分量分布）
- 常见用途：聚类、多模态数据

* *`pm.NormalMixture(name, w, mu, sigma)`**
- 正态分布的混合
- 常见用途：高斯聚类

### 零膨胀和跨栏模型

* *`pm.ZeroInflatedPoisson(name, psi, mu)`** - 计数数据中有多余的零

* *`pm.ZeroInflatedBinomial(name, psi, n, p)`** - 零膨胀二项式

* *`pm.ZeroInflatedNegativeBinomial(name, psi, mu, alpha)`** - 零膨胀负值binomial

* *`pm.HurdlePoisson(name, psi, mu)`** - 跨栏泊松（两部分模型）

* *`pm.HurdleGamma(name, psi, alpha, beta)`** - 跨栏 gamma

* *`pm.HurdleLogNormal(name, psi, mu, sigma)`** - 跨栏对数正态

## 时间序列分布

专为时态数据和顺序建模而设计的分布。

* *`pm.AR(name, rho, sigma, init_dist)`**
- 自回归过程
- 参数：`rho`（AR系数），`sigma`（创新标准）， `init_dist`（初始分布）
- 常见用途：时间序列建模、顺序数据

* *`pm.GaussianRandomWalk(name, mu, sigma, init_dist)`**
- 高斯随机游走
- 参数：`mu`（漂移）、`sigma`（步长）、 `init_dist`（初始值）
- 常见用途：累积过程、随机游走先验

* *`pm.MvGaussianRandomWalk(name, mu, cov, init_dist)`**
- 多元高斯随机游走

* *`pm.GARCH11(name, omega, alpha_1, beta_1)`**
- GARCH(1,1)波动率模型
- 常见用途：金融时间序列、波动率建模

* *`pm.EulerMaruyama(name, dt, sde_fn, sde_pars, init_dist)`**
- 通过欧拉-丸山离散化的随机微分方程
- 常见用途：连续时间过程

## 特殊分布

* *`pm.Deterministic(name, var)`**
- 确定性变换（不是随机变量）
- 用于从其他变量导出的计算量

* *`pm.Potential(name, logp)`**
- 添加任意对数概率贡献
- 用于自定义似然分量或约束

* *`pm.Flat(name)`**
- 不适当的平坦先验（恒定密度）
- 谨慎使用；可能会导致采样问题

* *`pm.HalfFlat(name)`**
- 正实数上不正确的平坦先验
- 谨慎使用；可能会导致采样问题

## 分布修饰符

* *`pm.Truncated(name, dist, lower, upper)`**
- 将任何分布截断到指定的边界

* *`pm.Censored(name, dist, lower, upper)`**
- 处理审查的观察结果（观察到的边界，不精确）值）

* *`pm.CustomDist(name, ..., logp, random)`**
- 使用用户指定的对数概率和随机采样函数定义自定义分布

* *`pm.Simulator(name, fn, params, ...)`**
- 通过模拟自定义分布（用于无似然推理）

## 用法提示

### 选择先验

1. **尺度参数**（σ，τ）：使用`HalfNormal`、`HalfCauchy`、`Exponential`或`Gamma`
2. **概率**：使用 `Beta` 或 `Uniform(0, 1)`
3. **无界参数**：使用`Normal`或`StudentT`（为了稳健性）
4. **正参数**：使用 `LogNormal`、`Gamma` 或 `Exponential`
5. **相关矩阵**：使用 `LKJCorr`
6. **计数数据**：使用 `Poisson` 或 `NegativeBinomial`（用于过度分散）

### 形状广播

PyMC 发行版支持 NumPy 风格的广播。使用 `shape` 参数创建随机变量的向量或数组：

```python
# Vector of 5 independent normals
beta = pm.Normal('beta', mu=0, sigma=1, shape=5)

# 3x4 matrix of independent gammas
tau = pm.Gamma('tau', alpha=2, beta=1, shape=(3, 4))
```

### 使用命名维度的暗淡 

代替形状，使用 `dims` 以获得更易读的模型：

```python
with pm.Model(coords={'predictors': ['age', 'income', 'education']}) as model:
    beta = pm.Normal('beta', mu=0, sigma=1, dims='predictors')
```
