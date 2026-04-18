# 心率变异性 (HRV)分析

## 概述

心率变异性 (HRV)反映连续心跳之间时间间隔的变化，为了解自主神经系统调节、心血管健康和心理状态提供见解。 NeuroKit2 提供跨时间、频率和非线性域的全面 HRV 分析。

## 主要功能

### hrv()

跨所有域一次性计算所有可用的 HRV 指数。

```python
hrv_indices = nk.hrv(peaks, sampling_rate=1000, show=False)
```

* *输入：**
- `peaks`：具有 `'ECG_R_Peaks'` 键或 R 峰值索引数组的字典
- `sampling_rate`：以 Hz 为单位的信号采样率

* *返回：**
- 具有来自所有域的 HRV 索引的数据帧：
  - 时域指标
  - 频域功率谱
  - 非线性复杂度措施

* *这是一个方便的包装**，结合了：
- `hrv_time()`
- `hrv_frequency()`
- `hrv_nonlinear()`

## 时域分析

### hrv_time()

根据心跳间隔 (IBI)计算时域 HRV 指标。

```python
hrv_time = nk.hrv_time(peaks, sampling_rate=1000)
```

### 关键指标

* *基本间隔统计：**
- `HRV_MeanNN`：NN 间隔的平均值(ms)
- `HRV_SDNN`：NN 间隔的标准差 (ms)
  - 反映总 HRV，捕获所有循环分量
  - 短期需要 ≥5 分钟，长期需要 ≥24 小时
- `HRV_RMSSD`：连续差值的均方根(ms)
  - 高频变异性，反映副交感神经活动
  - 录音较短，更稳定

* *连续差异测量：**
- `HRV_SDSD`：连续差异的标准差 (ms)
  - 与 RMSSD 类似，与副交感神经活动相关
- `HRV_pNN50`：连续 NN 间隔差异 > 50 毫秒的百分比
  - 副交感神经指标，在某些情况下可能不敏感群体
- `HRV_pNN20`：连续 NN 间隔差异 >20ms 的百分比
  - pNN50

 更敏感的替代方案**范围测量：**
- `HRV_MinNN`、`HRV_MaxNN`：最小和最大 NN 间隔 (ms)
- `HRV_CVNN`：变异系数 (SDNN/MeanNN)
  - 归一化测量，可用于跨受试者比较
- `HRV_CVSD`：连续差异的变异系数 (RMSSD/MeanNN)

* *基于中值的统计：**
- `HRV_MedianNN`：中值NN 间隔 (ms)
  - 对异常值具有鲁棒性
- `HRV_MadNN`：NN 间隔的中值绝对偏差
  - 鲁棒离散度测量
- `HRV_MCVNN`：基于中值的变异系数

* *高级time-domain:**
- `HRV_IQRNN`：NN 间隔的四分位数范围
- `HRV_pNN10`、`HRV_pNN25`、`HRV_pNN40`：附加百分位阈值
- `HRV_TINN`：NN 间隔的三角插值直方图
- `HRV_HTI`：HRV 三角指数（总 NN 间隔/直方图高度）

### 记录持续时间要求
- **超短（< 5 分钟）**：RMSSD、pNN50 最可靠
- **短期（5 分钟）**：临床使用标准，所有时域有效
- **长期（24 小时）**：SDNN 解释所需，捕获昼夜节律

## 频域分析

### hrv_Frequency()

使用频谱分析跨频段的 HRV 功率分析。

```python
hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000, ulf=(0, 0.0033), vlf=(0.0033, 0.04),
                            lf=(0.04, 0.15), hf=(0.15, 0.4), vhf=(0.4, 0.5),
                            psd_method='welch', normalize=True)
```

### 频段

* *超低频 (ULF)：0-0.0033 Hz**
- 需要 ≥24 小时记录
- 昼夜节律、体温调节
- 缓慢代谢过程

* *极低频 (VLF)：0.0033-0.04 Hz**
- 需要 ≥5 分钟记录
- 体温调节、激素波动
- 肾素-血管紧张素系统、外周血管舒缩活动

* *低频 (LF)：0.04-0.15 Hz**
- 混合交感神经和副交感神经影响
- 压力感受器反射活动
- 血压调节（10秒节律）

* *高频（HF）：0.15-0.4 Hz**
- 副交感神经（迷走神经）活动
- 呼吸性窦性心律失常
- 与呼吸同步（呼吸频率）范围）

* *甚高频 (VHF)：0.4-0.5 Hz**
- 很少使用，可能反映测量噪声
- 需要仔细解释

### 关键指标

* *绝对功率（ms²）：**
- `HRV_ULF`、`HRV_VLF`、`HRV_LF`、`HRV_HF`、`HRV_VHF`：各频段功率
- `HRV_TP`：总功率（NN间隔的方差）
- `HRV_LFHF`：低频/高频比（交感迷走神经平衡）

* *标准化功率：**
- `HRV_LFn`：低频功率/(LF + HF) - 标准化 LF
- `HRV_HFn`：高频功率/(LF + HF) - 标准化 HF
- `HRV_LnHF`：自然HF 对数（对数正态分布）

* *峰值频率：**
- `HRV_LFpeak`、`HRV_HFpeak`：每个频段中最大功率的频率
- 用于识别主振荡

### 功率谱密度方法

* *Welch 方法（默认）：**
```python
hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000, psd_method='welch')
```
- 具有重叠的加窗 FFT
- 更平滑的频谱，减少方差
- 适用于标准 HRV 分析

* *Lomb-Scargle周期图：**
```python
hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000, psd_method='lomb')
```
- 处理不均匀采样的数据
- 无需插值
- 更适合噪声或包含伪影的数据

* *多锥度方法：**
```python
hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000, psd_method='multitapers')
```
- 卓越的光谱估计
- 以最小偏差减少方差
- 计算密集型

* *Burg 自回归：**
```python
hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000, psd_method='burg', order=16)
```
- 参数方法
- 定义明确的平滑光谱Peaks
- 需要顺序选择

### 解释指南

* *LF/HF 比率：**
- 传统上解释为交感迷走神经平衡
- **警告**：最近的证据质疑这种解释
- LF 反映了交感神经和副交感神经影响
- 上下文相关：受控呼吸影响 HF

* *HF 功率：**
- 可靠的副交感神经指标
- 随休息、放松、深呼吸而增加
- 随压力、焦虑、交感神经激活而减少

* *记录要求：**
- **最低**：低频/高频估计 60 秒
- **推荐**：短期 HRV 2-5 分钟 
- **最佳**：每个工作组标准 5 分钟
- **长期**：ULF 分析 24 小时

## 非线性域分析

### hrv_nonlinear()

计算反映自主动态的复杂性、熵和分形度量。

```python
hrv_nonlinear = nk.hrv_nonlinear(peaks, sampling_rate=1000)
```

### 庞加莱图指数

* *庞加莱图**：NN(i+1) vs NN(i)散点图几何

- `HRV_SD1`：垂直于同一线的标准差 (ms)
  - 短期 HRV，快速逐搏变异性
  - 反映副交感神经活动
  - 在数学上与 RMSSD 相关：SD1 ≈ RMSSD/√2

- `HRV_SD2`：沿同一线的标准差 (ms)
  - 长期 HRV，缓慢变异
  - 反映交感神经和副交感神经活动
  - 与 SDNN

- 相关 `HRV_SD1SD2`：比率 SD1/SD2
  - 短期和长期之间的平衡变异性
  - <1：主要为长期变异性

- `HRV_SD2SD1`：比率 SD2/SD1
  - SD1SD2

- `HRV_S`：椭圆面积 (π × SD1 × SD2)
  - 总 HRV 幅度

- `HRV_CSI`：心脏交感神经指数 (SD2/SD1)
  - 建议的交感神经指数 

- `HRV_CVI`：心脏迷走神经指数 (log10(SD1 × SD2))
  - 建议的副交感神经指数 

- `HRV_CSI_Modified`：修改后的 CSI (SD2²/(SD1 × SD2))

### 心率不对称

分析心率加速和减速对 HRV 的影响是否不同。

- `HRV_GI`：Guzik 指数 - 短期变异性的不对称性
- `HRV_SI`：坡度指数 - 长期变化的不对称性
- `HRV_AI`：面积指数 - 整体不对称性
- `HRV_PI`：Porta 指数 - 减速度百分比
- `HRV_C1d`、`HRV_C2d`：减速度贡献
- `HRV_C1a`、`HRV_C2a`：加速贡献
- `HRV_SD1d`、`HRV_SD1a`：减速/加速的庞加莱SD1
- `HRV_SD2d`、`HRV_SD2a`：用于减速/加速的庞加莱 SD2

* *解释：**
- 健康个体：存在不对称性（更多/更大的减速）
- 临床人群：减少不对称性
- 反映加速与减速的差异自主控制

### 熵测量

* *近似熵（ApEn）：**
- `HRV_ApEn`：规律性度量，较低=更规律/可预测
- 对数据长度、阶数m、容差敏感r

* *样本熵（SampEn）：**
- `HRV_SampEn`：改进的 ApEn，更少依赖于数据长度
- 与短记录更一致
- 较低的值 = 更规则的模式

* *多尺度熵 (MSE)：**
- `HRV_MSE`：跨多个时间尺度的复杂性
- 区分真正的复杂性来自随机性

* *模糊熵：**
- `HRV_FuzzyEn`：用于模式匹配的模糊隶属函数
- 短数据更稳定

* *香农熵：**
- `HRV_ShanEn`：信息论随机性measure

### 分形测量

* *去趋势波动分析 (DFA)：**
- `HRV_DFA_alpha1`：短期分形标度指数（4-11 次）
  - α1 > 1：相关性，心脏病时减少
  - α1 ≈ 1：粉红噪声，健康
  - α1 < 0.5：反相关

- `HRV_DFA_alpha2`：长期分形标度指数（>11 次）
  - 反映长期相关性

- `HRV_DFA_alpha1alpha2`：比率 α1/α2

* * 相关维度：**
- `HRV_CorDim`：相空间中吸引子的维数
- 表示系统复杂性

* *Higuchi分形维数：**
- `HRV_HFD`：复杂性和自相似性
- 较高的值=更复杂，不规则

* *彼得罗分形维度：**
- `HRV_PFD`：替代复杂性度量
- 计算效率

* *Katz 分形维度：**
- `HRV_KFD`：波形复杂性

### 心率碎片

量化异常短期

- `HRV_PIP`：拐点百分比
  - 正常：~50%，碎片：>70% 
- `HRV_IALS`：加速/减速段的逆平均长度
- `HRV_PSS`：短节段（<3 次心跳）的百分比
- `HRV_PAS`：交替节段中 NN 间隔的百分比

* *临床相关性：**
- 与心血管风险相关的碎片化增加
- 超越传统 HRV 指标的独立预测因子

### 其他非线性指标

- `HRV_Hurst`：赫斯特指数（长程依赖性）
- `HRV_LZC`：Lempel-Ziv 复杂度（算法复杂度）
- `HRV_MFDFA`：多重分形 DFA 指数

## 专业 HRV功能

### hrv_rsa()

呼吸性窦性心律失常 - 通过呼吸调节心率。

```python
rsa = nk.hrv_rsa(peaks, rsp_signal, sampling_rate=1000, method='porges1980')
```

* *方法：**
- `'porges1980'`：Porges-Bohrer 方法（呼吸频率附近的带通滤波 HR）
- `'harrison2021'`：峰谷 RSA（每次呼吸的最大-最小 HR）周期）

* *要求：**
- 心电图和呼吸信号
- 同步定时
- 至少几个呼吸周期

* *返回：**
- `RSA`：RSA幅度（心跳/分钟或类似单位，具体取决于方法）

### hrv_rqa()

循环量化分析 - 来自相空间重建的非线性动力学。

```python
rqa = nk.hrv_rqa(peaks, sampling_rate=1000)
```

* *指标：**
- `RQA_RR`：循环率 - 系统可预测性
- `RQA_DET`：确定性 -形成线的重复点的百分比
- `RQA_LMean`、`RQA_LMax`：平均和最大对角线长度
- `RQA_ENTR`：线长度的香农熵 - 复杂性
- `RQA_LAM`：层流 - 陷入特定状态的系统
- `RQA_TT`：捕获时间 - 层流状态下的持续时间

* *用例：**
- 检测生理状态的转变
- 评估系统确定性与随机性

## 间隔处理

### Intervals_process()

Preprocess HRV 分析之前的 RR 间隔。

```python
processed_intervals = nk.intervals_process(rr_intervals, interpolate=False,
                                           interpolate_sampling_rate=1000)
```

* *操作：**
- 删除生理上不合理的间隔
- 可选：插值到定期采样
- 可选：去趋势以删除缓慢趋势

* *使用案例：**
- 使用预先提取的 RR 间隔时
- 从外部设备清洁间隔
- 为频域分析准备数据

### Intervals_to_peaks()

将间隔数据（RR、NN）转换为 HRV 峰值指数分析。

```python
peaks_dict = nk.intervals_to_peaks(rr_intervals, sampling_rate=1000)
```

* *用例：**
- 从外部 HRV 设备导入数据
- 使用商业系统的间隔数据
- 在间隔和峰值表示之间转换

## 实际注意事项

### 最小记录持续时间

|分析|最短持续时间 |最佳持续时间|
|----------|------------------|------------------|
| RMSSD，pNN50 | 30 秒 | 5 分钟 |
| SDNN | 5 分钟 | 5 分钟（短），24 小时（长）|
|低频、高频功率 | 2 分钟 | 5 分钟 |
|甚低频功率| 5 分钟 | 10+ 分钟 |
|超低频电源| 24 小时 | 24 小时 |
|非线性（ApEn、SampEn）| 100-300 次 | 500+ 节拍 |
| DFA | 300 次 | 1000+ 节拍 |

### 工件管理

* *预处理：**
```python
# Detect R-peaks with artifact correction
peaks, info = nk.ecg_peaks(cleaned_ecg, sampling_rate=1000, correct_artifacts=True)

# Or manually process intervals
processed = nk.intervals_process(rr_intervals, interpolate=False)
```

* *质量检查：**
- 转速图的目视检查（NN 间隔随时间变化）
- 识别生理上不可信的间隔（<300 毫秒）或 >2000 ms)
- 检查突然跳跃或丢失的节拍
- 在分析前评估信号质量

### 标准化和比较

* *工作组标准 (1996)：**
- 短期 5 分钟录音
- 仰卧、控制呼吸建议
- 24 小时进行长期评估

* *标准化：**
- 考虑年龄、性别、健身水平影响
- 一天中的时间和昼夜节律影响
- 身体位置（仰卧与站立）
- 呼吸频率和深度

* *个体间变异：**
- HRV 具有较大的受试者间变异
- 受试者内变化更容易解释
- 首选基线比较

## 临床和研究应用

* *心血管健康：**
- HRV 降低：HRV 降低的危险因素心脏事件
- SDNN、DFA alpha1：预后指标
- MI后监测

* *心理状态：**
- 焦虑/压力：HRV降低（尤其是RMSSD、HF）
- 抑郁：自主神经平衡改变
- PTSD：碎片化指数

* *运动表现：**
- 通过每日RMSSD监测训练负荷ZXXQNL41QXZ-过度训练：HRV降低ZXXQNL42QXZ-恢复评估

* *神经科学：**
- 情绪调节研究
- 认知负荷评估
- 脑心轴研究

* *衰老：**
- HRV 随着年龄的增长而降低
- 复杂性测量值下降
- 需要基线参考

## 参考文献

- 欧洲心脏病学会的工作组。 （1996）。心率变异性：测量标准、生理解释和临床应用。循环，93(5), 1043-1065.
- Shaffer, F. 和 Ginsberg, J. P. (2017)。心率变异性指标和规范概述。公共卫生前沿，5, 258.
- Peng, C. K.、Havlin, S.、Stanley, H. E. 和 Goldberger, A. L. (1995)。非平稳心跳时间序列中缩放指数和交叉现象的量化。混沌，5(1), 82-87.
- Guzik, P.、Piskorski, J.、Krauze, T.、Wykretowicz, A. 和 Wysocki, H. (2006)。 RR 间隔庞加莱图的心率不对称性。生物医学技术/生物医学工程，51(4), 272-275.
- Costa, M.、Goldberger, A. L. 和 Peng, C. K. (2005)。生物信号的多尺度熵分析。物理审查E, 71(2), 021906.
