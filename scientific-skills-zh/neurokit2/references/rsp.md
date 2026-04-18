# 呼吸信号处理

## 概述

NeuroKit2 中的呼吸信号处理可以分析呼吸模式、呼吸频率、幅度和变异性。呼吸与心脏活动（呼吸性窦性心律失常）、情绪状态和认知过程密切相关。

## 主处理管道

### rsp_process()

通过峰/谷检测和特征提取自动处理呼吸信号。

```python
signals, info = nk.rsp_process(rsp_signal, sampling_rate=100, method='khodadad2018')
```

* *管道步骤：**
1. 信号净化（去噪、滤波）
2. 峰值（呼气）和谷值（吸气）检测
3. 呼吸频率计算
4. 幅度计算
5. 相位确定（吸气/呼气）
6. 每次呼吸量 (RVT)

* *返回：**
- `signals`：数据帧包含：
  - `RSP_Clean`：过滤后的呼吸信号
  - `RSP_Peaks`、`RSP_Troughs`：极值标记
  - `RSP_Rate`：瞬时呼吸频率（呼吸/分钟）
  - `RSP_Amplitude`：呼吸幅度
  - `RSP_Phase`：吸气 (0)与呼气 (1)
  - `RSP_Phase_Completion`：阶段完成百分比 (0-1)
  - `RSP_RVT`：每次呼吸量
- `info`：具有峰/谷指数的字典

* *方法：**
- `'khodadad2018'`：Khodadad 等人。算法（默认，稳健）
- `'biosppy'`：基于BioSPPy的处理（替代）

## 预处理函数

### rsp_clean()

去除噪音并平滑呼吸signal.

```python
cleaned_rsp = nk.rsp_clean(rsp_signal, sampling_rate=100, method='khodadad2018')
```

* *方法：**

* *1。 Khodadad2018（默认）：**
- 巴特沃斯低通滤波器
- 去除高频噪声
- 保留呼吸波形

* *2。 BioSPPy：**
- 替代过滤方法
- 与Khodadad

类似的性能**3。 Hampel 滤波器：**
```python
cleaned_rsp = nk.rsp_clean(rsp_signal, sampling_rate=100, method='hampel')
```
- 基于中值的异常值去除
- 对伪影和尖峰具有鲁棒性
- 保留尖锐过渡

* *典型呼吸频率：**
- 成人休息时：12-20 次呼吸/分钟 (0.2-0.33 Hz)
- 儿童：更快的频率
- 运动期间：高达 40-60 次呼吸/分钟

### rsp_peaks()

识别吸入槽

```python
peaks, info = nk.rsp_peaks(cleaned_rsp, sampling_rate=100, method='khodadad2018')
```

* *检测方法：**
- `'khodadad2018'`：针对干净信号进行优化
- `'biosppy'`：替代方法
- `'scipy'`：基于简单的 scipy检测

* *返回：**
- 字典包含：
  - `RSP_Peaks`：呼气峰指数（最大点）
  - `RSP_Troughs`：吸气波谷指数（最小点）

* *呼吸周期定义：**
- **吸气**：波谷 → 波峰（气流流入，胸部/腹部膨胀）
- **呼气**：波峰 → 波谷（气流流出，胸部/腹部收缩）

### rsp_findpeaks()

多种算法的低电平峰值检测options.

```python
peaks_dict = nk.rsp_findpeaks(cleaned_rsp, sampling_rate=100, method='scipy')
```

* *方法：**
- `'scipy'`：Scipy 的 find_peaks
- 自定义基于阈值的算法

* *用例：**
- 微调峰值检测
- 自定义参数调整
- 算法比较

### rsp_fixpeaks()

纠正检测到的峰/谷异常（例如，遗漏或错误） 

```python
corrected_peaks = nk.rsp_fixpeaks(peaks, sampling_rate=100)
```

* *更正：**
- 删除生理上不合理的间隔
- 插入缺失的峰
- 删除与伪影相关的假峰

## 特征提取函数

### rsp_rate()

计算瞬时呼吸频率（每分钟呼吸次数）。

```python
rate = nk.rsp_rate(peaks, sampling_rate=100, desired_length=None)
```

* *方法：**
- 根据峰/谷时间计算呼吸间隔
- 转换为每分钟呼吸次数(BPM)
- 插值匹配信号长度

* *典型值：**
- 成人静息：12-20 BPM
- 缓慢呼吸：<10 BPM（冥想、放松）
- 快速呼吸：>25 BPM（运动、焦虑）

### rsp_amplitude()

计算呼吸幅度（峰谷差）。

```python
amplitude = nk.rsp_amplitude(cleaned_rsp, peaks)
```

* *解释：**
- 较大振幅：更深呼吸（潮气量增加）
- 较小振幅：浅呼吸
- 可变振幅：不规则呼吸模式

* *临床相关性：**
- 减小振幅：限制性肺病、胸壁刚性
- 振幅增加：代偿性过度通气

### rsp_phase()

确定吸气/呼气阶段和完成百分比。

```python
phase, completion = nk.rsp_phase(cleaned_rsp, peaks, sampling_rate=100)
```

* *返回：**
- `RSP_Phase`：二进制（0 = 吸气， 1 = 到期）
- `RSP_Phase_Completion`：连续 0-1 指示阶段进展

* *用例：**
- 呼吸门控刺激呈现
- 锁相平均
- 呼吸-心脏耦合分析

### rsp_symmetry()

分析呼吸对称模式（峰谷平衡、上升衰减时序）。

```python
symmetry = nk.rsp_symmetry(cleaned_rsp, peaks)
```

* *指标：**
- 峰谷对称性：峰和谷的间距是否相等？
- 上升-衰减对称：吸气时间等于呼气时间吗？

* *解释：**
- 对称：正常、轻松呼吸
- 不对称：费力呼吸、气道阻塞

## 高级分析功能

### rsp_rrv()

呼吸频率变异性- 类似于心率变异性。

```python
rrv_indices = nk.rsp_rrv(peaks, sampling_rate=100)
```

* *时域指标：**
- `RRV_SDBB`：呼吸间隔的标准差
- `RRV_RMSSD`：连续差异的均方根
- `RRV_MeanBB`：平均呼吸间隔

* *频域指标：**
- 频段功率（如果适用）

* *解释：**
- 较高RRV：灵活、自适应呼吸控制
- 较低RRV：刚性、受限呼吸
- RRV 改变：焦虑、呼吸系统疾病、自主神经功能障碍

* *记录持续时间：**
- 最短：2-3 分钟
- 最佳：稳定估计需要 5-10 分钟

### rsp_rvt()

每次呼吸量 - fMRI混淆回归器.

```python
rvt = nk.rsp_rvt(cleaned_rsp, peaks, sampling_rate=100)
```

* *计算：**
- 呼吸信号的导数
- 捕获体积变化率
- 与 BOLD 信号波动相关

* *用例：**
- fMRI 伪影校正
- 神经影像预处理
- 呼吸混杂回归

* *参考：**
- Birn, R. M., et al. （2008）。在功能磁共振成像中将呼吸变化相关的波动与神经元活动相关的波动分开。 NeuroImage, 31(4), 1536-1548.

### rsp_rav()

呼吸振幅变异指数。

```python
rav = nk.rsp_rav(amplitude, sampling_rate=100)
```

* *指标：**
- 的标准偏差振幅
- 变异系数
- 振幅范围

* *解释：**
- 高RAV：不规则深度（叹息、觉醒变化）
- 低RAV：稳定、受控呼吸

## 分析功能

### rsp_analyze()

自动选择事件相关或间隔相关分析。

```python
analysis = nk.rsp_analyze(signals, sampling_rate=100)
```

* *模式选择：**
- 持续时间<10秒→事件相关
- 持续时间≥10秒→间隔相关

### rsp_eventlated()

分析对特定事件/刺激的呼吸反应。

```python
results = nk.rsp_eventrelated(epochs)
```

* *计算指标（每个时期）：**
- `RSP_Rate_Mean`：时期内的平均呼吸频率
- `RSP_Rate_Min/Max`：最小/最大速率
- `RSP_Amplitude_Mean`：平均呼吸深度
- `RSP_Phase`：事件发生时的呼吸相
- 跨时期的速率和幅度动态

* *用例：**
- 呼吸变化情绪刺激期间
- 任务事件前的预期呼吸
- 屏气或过度换气范式

### rsp_intervallated()

分析扩展呼吸记录。

```python
results = nk.rsp_intervalrelated(signals, sampling_rate=100)
```

* *计算指标：**
- `RSP_Rate_Mean`：平均呼吸频率
- `RSP_Rate_SD`：速率变异性
- `RSP_Amplitude_Mean`：平均呼吸深度
- RRV指数（如果有足够的数据）
- RAV指数

* *记录持续时间：**
- 最低：60 秒
- 最佳：5-10 分钟

* *使用案例：**
- 静息状态呼吸模式
- 基线呼吸评估
- 压力或放松监测

## 模拟和可视化

### rsp_simulate()

生成用于测试的合成呼吸信号。

```python
synthetic_rsp = nk.rsp_simulate(duration=60, sampling_rate=100, respiratory_rate=15,
                                method='sinusoidal', noise=0.1, random_state=42)
```

* *方法：**
- `'sinusoidal'`：简单正弦振荡（快速）
- `'breathmetrics'`：高级真实呼吸模型（更慢，更准确）

* *参数：**
- `respiratory_rate`：每分钟呼吸次数（默认：15）
- `noise`：高斯噪声水平
- `random_state`：种子重现性

* *用例：**
- 算法验证
- 参数调整
- 教育演示

### rsp_plot()

可视化处理的呼吸signal.

```python
nk.rsp_plot(signals, info, static=True)
```

* *显示：**
- 原始和清洁的呼吸信号
- 检测到的波峰和波谷
- 瞬时呼吸频率
- 相位标记

* *交互模式：**设置`static=False` 用于绘图可视化

## 实际注意事项

### 采样率建议
- **最小值**：10 Hz（足以进行速率估计）
- **标准**：50-100 Hz（研究级）
- **高分辨率**：1000 Hz（通常不必要，过采样）

### 记录持续时间
- **速率估计**：≥10 秒（几次呼吸）
- **RRV 分析**：≥2-3 分钟
- **静息状态**：5-10 分钟
- **昼夜节律模式**：几小时到几天

### 信号采集方法

* *应变计/压电带：**
- 胸部或腹部扩张
- 最常见
- 舒适，非侵入式

* *热敏电阻/热电偶：**
- 鼻/口腔气流温度
- 直接气流测量
- 可以侵入式

* *二氧化碳图：**
- 呼气末二氧化碳测量
- 黄金标准生理学
- 昂贵的临床环境

* *阻抗呼吸描记术：**
- 源自心电图电极
- 方便多模式记录
- 不如专用传感器精确

### 常见问题和解决方案

* *不规则呼吸：**
- 清醒、休息时正常
- 叹息，打哈欠、言语、吞咽导致变异性
- 将伪影或模型排除为事件

* *浅呼吸：**
- 低信号幅度
- 检查传感器位置和密封性
- 如果可用则增加增益

* *运动伪影：**
- 尖峰或不连续性
- 最大限度地减少参与者的移动
- 使用强大的峰值检测（Hampel 滤波器）

* * 说话/咳嗽：**
- 扰乱自然呼吸模式
- 注释并从分析中排除
- 或模型作为单独的事件类型

### 最佳实践

* *标准工作流程：**
```python
# 1. Clean signal
cleaned = nk.rsp_clean(rsp_raw, sampling_rate=100, method='khodadad2018')

# 2. Detect peaks/troughs
peaks, info = nk.rsp_peaks(cleaned, sampling_rate=100)

# 3. Extract features
rate = nk.rsp_rate(peaks, sampling_rate=100, desired_length=len(cleaned))
amplitude = nk.rsp_amplitude(cleaned, peaks)
phase = nk.rsp_phase(cleaned, peaks, sampling_rate=100)

# 4. Comprehensive processing (alternative)
signals, info = nk.rsp_process(rsp_raw, sampling_rate=100)

# 5. Analyze
analysis = nk.rsp_analyze(signals, sampling_rate=100)
```

* *呼吸-心脏一体化：**
```python
# Process both signals
ecg_signals, ecg_info = nk.ecg_process(ecg, sampling_rate=1000)
rsp_signals, rsp_info = nk.rsp_process(rsp, sampling_rate=100)

# Respiratory sinus arrhythmia (RSA)
rsa = nk.hrv_rsa(ecg_info['ECG_R_Peaks'], rsp_signals['RSP_Clean'], sampling_rate=1000)

# Or use bio_process for multi-signal integration
bio_signals, bio_info = nk.bio_process(ecg=ecg, rsp=rsp, sampling_rate=1000)
```

## 临床和研究应用

* *心理生理学：**
- 情绪和唤醒（压力期间快速、浅呼吸）
- 放松干预（缓慢、深呼吸）
- 呼吸生物反馈

* *焦虑和惊恐障碍：**
- 惊恐发作时过度换气
- 改变呼吸模式
- 呼吸再训练治疗有效性

* *睡眠药物：**
- 睡眠呼吸暂停检测
- 呼吸模式异常
- 睡眠阶段相关

* *心肺耦合：**
- 呼吸性窦性心律失常（通过呼吸调节HRV）
- 心肺相互作用
- 自主神经系统评估

* *神经影像：**
- fMRI伪影校正（RVT回归器）
- BOLD信号混淆去除
- 呼吸相关的大脑活动

* *冥想和正念：**
- 呼吸意识训练
- 缓慢呼吸练习（共振频率~6次呼吸/分钟）
- 放松的生理标志

* *运动表现：**
- 呼吸效率
- 训练适应
- 恢复监测

## 解释指南

* *呼吸频率：**
- **正常**：12-20 BPM（成人休息时）
- **慢**： <10 BPM（放松、冥想、睡眠）
- **快速**：>25 BPM（运动、焦虑、疼痛、发烧）

* *呼吸幅度：**
- 静息时潮气量通常为 400-600 mL
- 深呼吸：2-3 L
- 浅呼吸： <300 mL

* *呼吸模式：**
- **正常**：平滑、规则的正弦曲线
- **Cheyne-Stokes**：渐强-渐弱伴呼吸暂停（临床病理）
- **共济失调**：完全不规则（脑干）病变）

## 参考文献

- Khodadad, D.、Nordebo, S.、Müller, B.、Waldmann, A.、Yerworth, R.、Becher, T., ... & Bayford, R. (2018)。超声成像组织替代品的综述。医学与生物学超声，44(9), 1807-1823.
- Grossman, P., & Taylor, E. W. (2007)。了解呼吸性窦性心律失常：与心脏迷走神经张力、进化和生物行为功能的关系。生物心理学，74(2), 263-285.
- Birn, R. M.、Diamond, J. B.、Smith, M. A. 和 Bandettini, P. A. (2006)。在功能磁共振成像中将呼吸变化相关的波动与神经元活动相关的波动分开。神经影像, 31(4), 1536-1548.
