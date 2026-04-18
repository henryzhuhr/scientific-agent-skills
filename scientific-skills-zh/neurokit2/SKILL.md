---
name: neurokit2
description: 用于分析生理数据的综合生物信号处理工具包，包括 ECG、EEG、EDA、RSP、PPG、EMG 和 EOG 信号。在处理心血管信号、大脑活动、皮肤电反应、呼吸模式、肌肉活动或眼球运动时使用此技能。适用于心率变异性分析、事件相关电位、复杂性测量、自主神经系统评估、心理生理学研究和多模态生理信号集成。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# NeuroKit2

## 概述

NeuroKit2 是一个用于处理和分析生理信号（生物信号）的综合 Python 工具包。使用此技能处理心血管、神经、自主、呼吸和肌肉信号，以进行心理生理学研究、临床应用和人机交互研究。

## 何时使用此技能

在处理以下内容时应用此技能：
- **心脏信号**：ECG、PPG、心率变异性 (HRV)、脉冲分析
- **脑信号**：EEG 频带、微观状态、复杂性、源定位
- **自主信号**：皮肤电活动 (EDA/GSR)、皮肤电导反应 (SCR)
- **呼吸信号**：呼吸频率、呼吸变异性 (RRV)、每次呼吸量 
- **肌肉信号**：肌电图振幅、肌肉激活检测
- **眼动追踪**：EOG、眨眼检测和分析
- **多模态集成**：同时处理多个生理信号
- **复杂性分析**：熵测量、分形维数、非线性动力学

## 核心功能

### 1.心脏信号处理（ECG/PPG）

处理心电图和光电容积描记信号以进行心血管分析。详细工作流程参见`references/ecg_cardiac.md`。

* *主要工作流程：**
- 心电图处理流程：清洗→R峰检测→勾画→质量评估
- 跨时间、频率和非线性域的HRV分析
- PPG脉搏分析和质量评估
- 心电衍生呼吸提取

* *关键功能：**
```python
import neurokit2 as nk

# Complete ECG processing pipeline
signals, info = nk.ecg_process(ecg_signal, sampling_rate=1000)

# Analyze ECG data (event-related or interval-related)
analysis = nk.ecg_analyze(signals, sampling_rate=1000)

# Comprehensive HRV analysis
hrv = nk.hrv(peaks, sampling_rate=1000)  # Time, frequency, nonlinear domains
```

### 2.心率变异性分析

根据心脏信号计算综合HRV指标。有关所有指数和特定领域分析，请参阅 `references/hrv.md`。

* *支持的域：**
- **时域**：SDNN、RMSSD、pNN50、SDSD 和派生指标
- **频域**：ULF、VLF、LF、HF、VHF 功率和比率
- **非线性域**：庞加莱图 (SD1/SD2)、熵度量、分形尺寸
- **专业**：呼吸性窦性心律失常（RSA）、复发定量分析（RQA）

* *关键功能：**
```python
# All HRV indices at once
hrv_indices = nk.hrv(peaks, sampling_rate=1000)

# Domain-specific analysis
hrv_time = nk.hrv_time(peaks)
hrv_freq = nk.hrv_frequency(peaks, sampling_rate=1000)
hrv_nonlinear = nk.hrv_nonlinear(peaks, sampling_rate=1000)
hrv_rsa = nk.hrv_rsa(peaks, rsp_signal, sampling_rate=1000)
```

### 3.脑信号分析（EEG）

分析脑电图信号的频率功率、复杂性和微观状态模式。有关详细工作流程和 MNE 集成，请参阅 `references/eeg.md`。

* *主要功能：**
- 频段功率分析（Delta、Theta、Alpha、Beta、Gamma）
- 信道质量评估和重新参考
- 源定位（sLORETA、MNE）
- 微观状态分段和转换动力学
- 全局场功率和相异性测量

* *关键功能：**
```python
# Power analysis across frequency bands
power = nk.eeg_power(eeg_data, sampling_rate=250, channels=['Fz', 'Cz', 'Pz'])

# Microstate analysis
microstates = nk.microstates_segment(eeg_data, n_microstates=4, method='kmod')
static = nk.microstates_static(microstates)
dynamic = nk.microstates_dynamic(microstates)
```

### 4. 皮电活动 (EDA)

处理皮肤电导信号以进行自主神经系统评估。详细工作流程参见`references/eda.md`。

* *主要工作流程：**
- 信号分解为强直和相位分量
- 皮肤电导反应（SCR）检测和分析
- 交感神经系统指数计算
- 自相关和变点检测

* *关键功能：**
```python
# Complete EDA processing
signals, info = nk.eda_process(eda_signal, sampling_rate=100)

# Analyze EDA data
analysis = nk.eda_analyze(signals, sampling_rate=100)

# Sympathetic nervous system activity
sympathetic = nk.eda_sympathetic(signals, sampling_rate=100)
```

### 5.呼吸信号处理(RSP)

分析呼吸模式和呼吸变异性。有关详细工作流程，请参阅 `references/rsp.md`。

* *主要功能：**
- 呼吸频率计算和变异性分析
- 呼吸幅度和对称性评估
- 每次呼吸量（fMRI 应用）
- 呼吸幅度变异性(RAV)

* *主要功能：**
```python
# Complete RSP processing
signals, info = nk.rsp_process(rsp_signal, sampling_rate=100)

# Respiratory rate variability
rrv = nk.rsp_rrv(signals, sampling_rate=100)

# Respiratory volume per time
rvt = nk.rsp_rvt(signals, sampling_rate=100)
```

### 6.肌电图(EMG)

处理肌肉活动信号以进行激活检测和幅度分析。工作流程请参见 `references/emg.md`。

* *关键功能：**
```python
# Complete EMG processing
signals, info = nk.emg_process(emg_signal, sampling_rate=1000)

# Muscle activation detection
activation = nk.emg_activation(signals, sampling_rate=1000, method='threshold')
```

### 7. 眼电图 (EOG)

分析眼球运动和眨眼模式。工作流程参见`references/eog.md`。

* *关键功能：**
```python
# Complete EOG processing
signals, info = nk.eog_process(eog_signal, sampling_rate=500)

# Extract blink features
features = nk.eog_features(signals, sampling_rate=500)
```

### 8.通用信号处理

对任何信号应用滤波、分解和变换操作。 

* *关键操作：**
- 滤波（低通、高通、带通、带阻）
- 分解（EMD、SSA、小波）
- 峰值检测和校正
- 功率谱密度估计
- 信号插值和重采样
- 自相关和同步分析

* *关键功能：**
```python
# Filtering
filtered = nk.signal_filter(signal, sampling_rate=1000, lowcut=0.5, highcut=40)

# Peak detection
peaks = nk.signal_findpeaks(signal)

# Power spectral density
psd = nk.signal_psd(signal, sampling_rate=1000)
```

### 9.复杂性和熵分析

计算非线性动力学、分形维数和信息论度量。请参阅 `references/complexity.md` 了解所有可用指标。

* *可用度量：**
- **熵**：香农、近似、样本、排列、光谱、模糊、多尺度
- **分形维数**：Katz、Higuchi、Petrosian、Sevcik、相关维数
- **非线性动力学**：Lyapunov指数、Lempel-Ziv复杂度、递推量化
- **DFA**：去趋势波动分析、多重分形DFA
- **信息论**：Fisher信息、互信息

* *关键功能：**
```python
# Multiple complexity metrics at once
complexity_indices = nk.complexity(signal, sampling_rate=1000)

# Specific measures
apen = nk.entropy_approximate(signal)
dfa = nk.fractal_dfa(signal)
lyap = nk.complexity_lyapunov(signal, sampling_rate=1000)
```

### 10.事件相关分析

围绕刺激事件创建纪元并分析生理反应。请参阅 `references/epochs_events.md` 了解工作流程。

* *主要功能：**
- 从事件标记创建纪元
- 事件相关平均和可视化
- 基线校正选项
- 带置信区间的总平均计算

* *关键功能：**
```python
# Find events in signal
events = nk.events_find(trigger_signal, threshold=0.5)

# Create epochs around events
epochs = nk.epochs_create(signals, events, sampling_rate=1000,
                          epochs_start=-0.5, epochs_end=2.0)

# Average across epochs
grand_average = nk.epochs_average(epochs)
```

### 11.多信号集成

同时处理多个生理信号并统一输出。有关集成工作流程，请参阅 `references/bio_module.md`。

* *关键功能：**
```python
# Process multiple signals at once
bio_signals, bio_info = nk.bio_process(
    ecg=ecg_signal,
    rsp=rsp_signal,
    eda=eda_signal,
    emg=emg_signal,
    sampling_rate=1000
)

# Analyze all processed signals
bio_analysis = nk.bio_analyze(bio_signals, sampling_rate=1000)
```

## 分析模式

NeuroKit2 根据数据持续时间自动在两种分析模式之间进行选择：

* *事件相关分析**（< 10 秒）：
- 分析刺激锁定反应
- 基于纪元的分割
- 适合离散试验的实验范式

* *间隔相关分析**（≥ 10 秒）：
- 表征长时间内的生理模式
- 静息状态或连续活动
- 适合基线测量和长期测量监控

大部分`*_analyze()`功能自动选择合适的模式。

## 安装

```bash
uv pip install neurokit2
```

开发版本：
```bash
uv pip install https://github.com/neuropsychology/NeuroKit/zipball/dev
```

## 常用工作流程

### 快速开始：心电图分析
```python
import neurokit2 as nk

# Load example data
ecg = nk.ecg_simulate(duration=60, sampling_rate=1000)

# Process ECG
signals, info = nk.ecg_process(ecg, sampling_rate=1000)

# Analyze HRV
hrv = nk.hrv(info['ECG_R_Peaks'], sampling_rate=1000)

# Visualize
nk.ecg_plot(signals, info)
```

### 多模态分析
```python
# Process multiple signals
bio_signals, bio_info = nk.bio_process(
    ecg=ecg_signal,
    rsp=rsp_signal,
    eda=eda_signal,
    sampling_rate=1000
)

# Analyze all signals
results = nk.bio_analyze(bio_signals, sampling_rate=1000)
```

### 事件相关电位
```python
# Find events
events = nk.events_find(trigger_channel, threshold=0.5)

# Create epochs
epochs = nk.epochs_create(processed_signals, events,
                          sampling_rate=1000,
                          epochs_start=-0.5, epochs_end=2.0)

# Event-related analysis for each signal type
ecg_epochs = nk.ecg_eventrelated(epochs)
eda_epochs = nk.eda_eventrelated(epochs)
```

## 参考文献

This技能包括按信号类型和分析方法组织的综合参考文档：

- **ecg_cardiac.md**：ECG/PPG 处理、R 峰检测、描绘、质量评估
- **hrv.md**：所有领域的心率变异性指数
- **eeg.md**：EEG 分析、频段、微状态、源定位
- **eda.md**：皮电活动处理和 SCR分析
- **rsp.md**：呼吸信号处理和变异性
- **ppg.md**：光电容积描记信号分析
- **emg.md**：肌电图处理和激活检测
- **eog.md**：眼电图和眨眼分析
- **signal_processing.md**：常规信号实用程序和转换
- **complexity.md**：熵、分形和非线性测量
- **epochs_events.md**：事件相关分析和纪元创建
- **bio_module.md**：多信号集成工作流程

根据需要使用读取工具加载特定参考文件以访问详细的函数文档和parameters.

## 其他资源

 - 官方文档：https://neuropsychology.github.io/NeuroKit/
  - GitHub 存储库：https://github.com/neuropsychology/NeuroKit
  - 出版物：Makowski 等人。 （2021）。 NeuroKit2：用​​于神经生理信号处理的 Python 工具箱。行为研究方法。 https://doi.org/10.3758/s13428-020-01516-y
