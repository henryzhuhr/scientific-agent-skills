# 复杂性和熵分析

## 概述

复杂性度量量化时间序列信号的不规则性、不可预测性和多尺度结构。 NeuroKit2 提供全面的熵、分形维数和非线性动力学测量，用于评估生理信号复杂性。

## 主要功能

### Complexity()

同时计算多个复杂性指标以进行探索性分析。

```python
complexity_indices = nk.complexity(signal, sampling_rate=1000, show=False)
```

* *返回：**
- DataFrame具有跨类别的众多复杂性度量：
  - 熵指数
  - 分形维数
  - 非线性动力学度量
  - 信息论度量

* *用例：**
- 探索性分析以识别相关度量
- 综合信号表征
- 跨信号的比较研究

## 参数优化

在计算复杂性度量之前，应确定最佳嵌入参数：

### Complexity_delay()

确定相空间的最佳时间延迟(τ) 

```python
optimal_tau = nk.complexity_delay(signal, delay_max=100, method='fraser1986', show=False)
```

* *方法：**
- `'fraser1986'`：互信息第一最小值
- `'theiler1990'`：自相关第一过零
- `'casdagli1991'`：曹氏方法

* *用途：**熵中的嵌入延迟，吸引子重建

### complexity_dimension()

确定最佳嵌入维度(m)。

```python
optimal_m = nk.complexity_dimension(signal, delay=None, dimension_max=20,
                                    method='afn', show=False)
```

* *方法：**
- `'afn'`：平均虚假最近邻
- `'fnn'`：虚假最近邻
- `'correlation'`：相关维数饱和度

* *用途：**熵计算、相空间重建

### Complexity_tolerance()

确定熵度量的最佳容差 (r)。

```python
optimal_r = nk.complexity_tolerance(signal, method='sd', show=False)
```

* *方法：**
- `'sd'`：基于标准差（0.1-0.25 × SD 典型值）
- `'maxApEn'`：最大化ApEn
- `'recurrence'`：基于复发率

* *用于：**近似熵，样本熵

### Complexity_k()

确定 Higuchi 分形维数的最佳 k 参数。

```python
optimal_k = nk.complexity_k(signal, k_max=20, show=False)
```

* *用于：** Higuchi 分形维数计算

## 熵测量

熵量化随机性、不可预测性和信息content.

### entropy_shannon()

香农熵 - 经典信息论测度。

```python
shannon_entropy = nk.entropy_shannon(signal)
```

* *解释：**
- 较高：更随机，不太可预测
- 较低：更规则，可预测
- 单位：比特（信息）

* *用例：**
- 一般随机性评估
- 信息内容
- 信号不规则性

### entropy_approximate()

近似熵 (ApEn) - 的规律性Patterns.

```python
apen = nk.entropy_approximate(signal, delay=1, dimension=2, tolerance='sd')
```

* *参数：**
- `delay`：时间延迟（τ）
- `dimension`：嵌入维度（m）
- `tolerance`：相似度阈值(r)

* *解释：**
- 较低的 ApEn：更规则、自相似的模式 
- 较高的 ApEn：更复杂、不规则 
- 对信号长度敏感（建议≥100-300 点）

* *生理应用：**
- HRV：降低心脏病中的 ApEn
- EEG：神经系统疾病中的 ApEn 发生改变

### entropy_sample()

样本熵 (SampEn) - 改进的 ApEn.

```python
sampen = nk.entropy_sample(signal, delay=1, dimension=2, tolerance='sd')
```

* * 相对于 ApEn 的优点：**
- 较少依赖于信号长度
- 记录间更加一致
- 无自匹配偏差

* *解释：**
- 与ApEn 相同但更可靠
- 在大多数应用中首选

* *典型值：**
- HRV：0.5-2.5 （上下文相关）
- EEG：0.3-1.5

### entropy_multiscale()

多尺度熵（MSE）-跨时间尺度的复杂性。

```python
mse = nk.entropy_multiscale(signal, scale=20, dimension=2, tolerance='sd',
                            method='MSEn', show=False)
```

* *方法：**
- `'MSEn'`：多尺度样本熵
- `'MSApEn'`：多尺度近似熵
- `'CMSE'`：复合多尺度熵
- `'RCMSE'`：精炼复合多尺度熵

* *解释：**
- 不同粗粒度尺度下的熵
- 健康/复杂系统：跨多个尺度的高熵
- 患病/简单系统：熵降低，尤其是在较大尺度上

* *用例：**
- 区分真实复杂性和复杂性随机性
- 白噪声：跨尺度恒定
- 粉红噪声/复杂性：跨尺度的结构化变化

### entropy_fuzzy()

模糊熵-使用模糊隶属度函数.

```python
fuzzen = nk.entropy_fuzzy(signal, delay=1, dimension=2, tolerance='sd', r=0.2)
```

* *优点：**
- 对于噪声信号更稳定
- 模式匹配的模糊边界
- 对于短信号更好的性能

### entropy_permutation()

Permutation Entropy - 基于序数模式。

```python
perment = nk.entropy_permutation(signal, delay=1, dimension=3)
```

* *方法：**
- 将信号编码为序数模式（排列）
- 计算模式频率
- 对噪声和噪声具有鲁棒性非平稳性

* *解释：**
- 较低：更规则的序数结构
- 较高：更随机的排序

* *用例：**
- 脑电图分析
- 麻醉深度监测
- 快速计算

### entropy_spectral()

频谱熵 - 基于功率谱。

```python
spec_ent = nk.entropy_spectral(signal, sampling_rate=1000, bands=None)
```

* *方法：**
- 功率谱的归一化香农熵
- 量化频率分布规律性

* *解释：**
- 0：单频（纯音）
- 1：白噪声（平坦频谱）

* *使用案例：**
- 脑电图：频谱分布随状态变化
- 麻醉监测

### entropy_svd()

奇异值分解熵.

```python
svd_ent = nk.entropy_svd(signal, delay=1, dimension=2)
```

* *方法：**
- 轨迹矩阵上的SVD
- 奇异值分布熵

* *用例：**
- 吸引子复杂度
- 确定性与随机动力学

### entropy_ Differential()

差分熵-香农熵的连续模拟。

```python
diff_ent = nk.entropy_differential(signal)
```

* *用于：**连续概率分布

### 其他熵措施

* *Tsallis 熵：**
```python
tsallis = nk.entropy_tsallis(signal, q=2)
```
- 参数为 q
- q=1 的广义熵减少为香农熵 

* *Rényi 熵：**
```python
renyi = nk.entropy_renyi(signal, alpha=2)
```
- 参数为 α

 的广义熵**其他专用熵：**
- `entropy_attention()`：注意力熵
- `entropy_grid()`：基于网格的熵
- `entropy_increment()`：增量熵
- `entropy_slope()`：斜率熵
- `entropy_dispersion()`：色散熵
- `entropy_symbolicdynamic()`：符号动力学熵
- `entropy_range()`：范围熵
- `entropy_phase()`：相熵
- `entropy_quadratic()`， `entropy_cumulative_residual()`、`entropy_rate()`：专门变体

## 分形维数测量

分形维数表征自相似性和粗糙度。

### fractal_katz()

Katz 分形维数 - 波形

```python
kfd = nk.fractal_katz(signal)
```

* *解释：**
- 1：直线
- >1：增加粗糙度和复杂度
- 典型范围：1.0-2.0

* *优点：**
- 简单、快速计算
- 无参数调整

### fractal_higuchi()

Higuchi分形维数-自相似性。

```python
hfd = nk.fractal_higuchi(signal, k_max=10)
```

* *方法：**
- 构造k个新时间序列原文
- 根据长度尺度关系估计维度

* *解释：**
- 较高的HFD：更复杂、不规则
- 较低的HFD：更平滑、更规则

* *用例：**
- 脑电图复杂度
- HRV分析
- 癫痫检测

### fractal_petrosian()

Petrosian 分形维数 - 快速估计。

```python
pfd = nk.fractal_petrosian(signal)
```

* *优点：**
- 快速计算
- 直接计算（无曲线）拟合)

### fractal_sevcik()

Sevcik 分形维数 - 归一化波形复杂度。

```python
sfd = nk.fractal_sevcik(signal)
```

### fractal_nld()

归一化长度密度 - 基于曲线长度measure.

```python
nld = nk.fractal_nld(signal)
```

### fractal_psdslope()

功率谱密度斜率 - 频域分形测量.

```python
slope = nk.fractal_psdslope(signal, sampling_rate=1000)
```

* *方法：**
- 对数功率谱的线性拟合
- 斜率 β 与分形维数相关

* *解释：**
- β ≈ 0：白噪声（随机）
- β ≈ -1：粉红噪声（1/f，复）
- β ≈ -2：布朗噪声（布朗运动）

### fractal_hurst()

Hurst 指数 - 长程依赖。

```python
hurst = nk.fractal_hurst(signal, show=False)
```

* *解释：**
- H < 0.5：反持久（均值回归）
- H = 0.5：随机游走（白噪声）
- H > 0.5：持久（趋势、长记忆）

* *用例：**
- 评估长期相关性
- 金融时间序列
- HRV分析

### fractal_correlation()

相关维数 - 吸引子维数。

```python
corr_dim = nk.fractal_correlation(signal, delay=1, dimension=10, radius=64)
```

* *方法：**
- Grassberger-Procaccia算法
- 估计同相吸引子维数space

* *解释：**
- 低维：确定性、低维混沌
- 高维：高维混沌或噪声

### fractal_dfa()

去趋势波动分析-缩放exponent.

```python
dfa_alpha = nk.fractal_dfa(signal, multifractal=False, q=2, show=False)
```

* *解释：**
- α < 0.5：反相关
- α = 0.5：不相关（白噪声）
- α = 1.0：1/f 噪声（粉红噪声，健康）复杂性）
- α = 1.5：布朗噪声
- α > 1.0：持续的长程相关性

* *HRV应用：**
- α1（短期，4-11次心跳）：反映自主调节
- α2（长期，>11） beats)：长程相关性
- 减少 α1：心脏病理学

### fractal_mfdfa()

Multifractal DFA - 多尺度分形属性。

```python
mfdfa_results = nk.fractal_mfdfa(signal, q=None, show=False)
```

* *方法：**
- 扩展 DFA到多个 q 阶
- 表征多重分形谱

* *返回：**
- 广义赫斯特指数 h(q)
- 多重分形谱 f(α)
- 宽度表示多重分形强度

* *使用案例：**
- 检测多重分形结构
- 健康与疾病中的 HRV 多重分形
- EEG 多尺度动力学

### fractal_tmf()

多重分形非线性 - 与单分形的偏差。

```python
tmf = nk.fractal_tmf(signal)
```

* *解释：**
- 量化与简单缩放的偏差
- 更高：更多多重分形结构

### fractal_密度()

密度分形Dimension.

```python
density_fd = nk.fractal_density(signal)
```

### fractal_linelength()

线长度 - 总变化测量。

```python
linelength = nk.fractal_linelength(signal)
```

* *用例：**
- 简单复杂性代理
- 脑电图癫痫发作检测

## 非线性动力学

### 复杂度_lyapunov()

最大李雅普诺夫指数-混沌和发散。

```python
lyap = nk.complexity_lyapunov(signal, delay=None, dimension=None,
                              sampling_rate=1000, show=False)
```

* *解释：**
- λ < 0: 稳定固定点
- λ = 0：周期轨道
- λ > 0：混沌（附近轨迹呈指数发散）

* *用例：**
- 检测生理信号中的混沌
- HRV：正李亚普诺夫表明非线性动力学
- EEG：癫痫检测（癫痫发作前减少 λ）

### 复杂性_lempelziv()

Lempel-Ziv 复杂性 - 算法复杂性。

```python
lz = nk.complexity_lempelziv(signal, symbolize='median')
```

* *方法：**
- 计算不同模式的数量
- 粗粒度随机性测量

* *解释：**
- 较低：重复、可预测的模式
- 较高：多样化、不可预测的模式

* *用例：**
- 脑电图：意识水平、麻醉
- HRV：自主神经复杂性

### Complexity_rqa()

循环量化分析 - 相空间循环。

```python
rqa_indices = nk.complexity_rqa(signal, delay=1, dimension=3, tolerance='sd')
```

* *指标：**
- **循环率 (RR)**：循环状态的百分比
- **确定性 (DET)**：循环点的百分比在线中
- **层流 (LAM)**：垂直结构的百分比（层流状态）
- **捕获时间 (TT)**：平均垂直线长度
- **最长对角线/垂直**：系统可预测性
- **熵 (ENTR)**：线长度的香农熵分布

* *解释：**
- 高DET：确定性动力学
- 高LAM：系统陷入特定状态
- 低RR：随机、非循环动力学

* *用例：**
- 检测系统动力学中的转变
- 生理状态变化
- 非线性时间序列分析

### Complexity_hjorth()

Hjorth 参数 - 时域复杂性.

```python
hjorth = nk.complexity_hjorth(signal)
```

* *指标：**
- **活动性**：信号的方差
- **移动性**：导数与信号的标准差的比例
- **复杂性**：移动性随导数的变化

* *使用案例：**
- EEG 特征提取
- 癫痫检测
- 信号表征

### 复杂性_去相关（）

去相关时间 - 内存period.

```python
decorr_time = nk.complexity_decorrelation(signal, show=False)
```

* *解释：**
- 自相关降至阈值以下的时间滞后
- 较短：快速波动，短记忆
- 较长：缓慢波动，长记忆

### Complexity_relativeroughness()

相对粗糙度 - 平滑度度量。

```python
roughness = nk.complexity_relativeroughness(signal)
```

## 信息论

### Fisher_information()

Fisher 信息 - 度量order.

```python
fisher = nk.fisher_information(signal, delay=1, dimension=2)
```

* *解释：**
- 高：有序、结构化
- 低：无序、随机

* *用例：**
- 与香农熵结合（Fisher-Shannon 平面）
- 表征系统复杂性

### Fishershannon_information()

Fisher-Shannon信息产品.

```python
fs = nk.fishershannon_information(signal)
```

* *方法：**
- Fisher信息和香农熵的乘积
- 表征有序无序Balance

### mutual_information()

互信息 - 变量之间共享信息。

```python
mi = nk.mutual_information(signal1, signal2, method='knn')
```

* *方法：**
- `'knn'`：k最近邻（非参数）
- `'kernel'`：核密度估计
- `'binning'`：基于直方图的

* *用例：**
- 信号之间的耦合
- 特征选择
- 非线性依赖

## 实用注意事项

### 信号长度要求

|测量 |最小长度|最佳长度 |
|---------|---------------|----------------|
|香农熵 | 50 | 50 200+ |
| ApEn、SampEn | 100-300 | 500-1000 |
|多尺度熵 | 500 | 500每刻度 1000+ |
| DFA | 500 | 500 1000+ |
|李亚普诺夫| 1000 | 1000 5000+ |
|相关维度| 1000 | 1000 5000+ |

### 参数选择

* *一般准则：**
- 首先使用参数优化函数
- 或使用常规默认值：
  - 延迟 (τ)：HRV 为 1，EEG 自相关第一最小值 
  - 尺寸 (m)：2-3典型
  - 公差(r)：0.2 × SD 通用

* *灵敏度：**
- 结果可以是参数敏感的
- 报告使用的参数
- 考虑灵敏度分析

### 归一化和预处理

* *标准化：**
- 许多测量对信号幅度敏感
- 通常建议进行 Z 分数归一化
- 可能需要去除趋势

* * 平稳性：**
- 某些测量假定平稳性
- 检查统计测试（例如，ADF 测试）
- 分段非平稳信号

### 解释

* *上下文相关：**
- 没有通用的“好”或“坏”复杂性
- 比较受试者内或组之间
- 考虑生理学上下文

* *复杂性与随机性：**
- 最大熵≠最大复杂性
- 真实复杂性：结构化变异性
- 白噪声：高熵但低复杂性（MSE区分）

## 应用

* *心血管：**
- HRV复杂性：心脏病、衰老减少
- DFA α1：MI

 后的预后标志物**神经科学：**
- EEG 复杂性：意识、麻醉深度
- 熵：阿尔茨海默病、癫痫、睡眠阶段
- 排列熵：麻醉监测

* *心理学：**
- 抑郁、焦虑中的复杂性损失
- 压力下规律性增加

* *老化：**
- 跨系统老化的“复杂性损失”
- 降低多尺度复杂性

* *关键转变：**
- 状态转变前的复杂性变化
- 预警信号（关键减速）

## 参考文献

- Pincus, S. M. (1991)。近似熵作为系统复杂性的度量。 《美国国家科学院院刊》，88(6), 2297-2301.
- Richman, J. S. 和 Moorman, J. R. (2000)。使用近似熵和样本熵进行生理时间序列分析。美国生理学杂志 - 心脏和循环生理学，278(6)，H2039-H2049.
- Peng，C. K. 等。 （1995）。非平稳心跳时间序列中缩放指数和交叉现象的量化。混沌，5(1), 82-87.
- Costa, M.、Goldberger, A. L. 和 Peng, C. K. (2005)。生物信号的多尺度熵分析。物理评论 E, 71(2), 021906.
- Grassberger, P., & Procaccia, I. (1983)。测量奇异吸引子的奇异程度。物理学 D：非线性现象，9(1-2), 189-208.
