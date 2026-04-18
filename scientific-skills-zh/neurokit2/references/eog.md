# 眼电图 (EOG)分析

## 概述

眼电图 (EOG)通过检测眼睛位置变化产生的电位差来测量眼球运动和眨眼。 EOG用于睡眠研究、注意力研究、阅读分析和EEG伪影校正。

## 主处理管道

### eog_process()

自动化EOG信号处理管道。

```python
signals, info = nk.eog_process(eog_signal, sampling_rate=500, method='neurokit')
```

* *管道步骤：**
1. 信号清洗（过滤）
2. 眨眼检测
3. 眨眼率计算

* *返回：**
- `signals`：数据帧包含：
  - `EOG_Clean`：过滤的EOG信号
  - `EOG_Blinks`：二进制眨眼标记（0/1）
  - `EOG_Rate`：瞬时眨眼率（眨眼/分钟）
- `info`：带有眨眼索引和参数的字典

* *方法：**
- `'neurokit'`：NeuroKit2 优化方法（默认）
- `'agarwal2019'`：Agarwal 等人。 (2019)算法
- `'mne'`：MNE-Python 方法
- `'brainstorm'`：头脑风暴工具箱方法
- `'kong1998'`：Kong 等人。 (1998)方法

## 预处理函数

### eog_clean()

为眨眼检测准备原始EOG信号。

```python
cleaned_eog = nk.eog_clean(eog_signal, sampling_rate=500, method='neurokit')
```

* *方法：**
- `'neurokit'`：巴特沃斯滤波优化EOG
- `'agarwal2019'`：替代过滤
- `'mne'`：MNE-Python 预处理
- `'brainstorm'`：头脑风暴法
- `'kong1998'`：Kong 方法

* *典型滤波：**
- 低通：10-20 Hz（消除高频噪声）
- 高通：0.1-1 Hz（消除直流漂移）
- 保留眨眼波形（典型持续时间 100-400 ms）

* *EOG 信号特性：**
- **闪烁**：大振幅、定型波形（200-400 ms）
- **眼跳**：快速阶梯状偏转（20-80 ms）
- **平滑追踪**：缓慢斜坡状变化
- **基线**：眼睛注视时稳定

## 闪烁检测

### eog_peaks()

检测EOG信号中的眨眼情况。

```python
blinks, info = nk.eog_peaks(cleaned_eog, sampling_rate=500, method='neurokit',
                            threshold=0.33)
```

* *方法：**
- `'neurokit'`：幅度和持续时间标准（默认）
- `'mne'`：MNE-Python 眨眼检测
- `'brainstorm'`：头脑风暴方法
- `'blinker'`：BLINKER 算法（Kleifges 等人，2017）

* *关键参数：**
- `threshold`：幅度阈值（最大幅度的分数）
  - 典型：0.2-0.5
  - 较低：更敏感（可能包括错误）正值）
  - 更高：更保守（可能会错过小眨眼）

* *返回：**
- 包含眨眼峰值指数的 `'EOG_Blinks'` 键的字典

* *眨眼特征：**
- **频率**：15-20 次眨眼/分钟（休息时，舒适）
- **持续时间**：100-400 ms（平均约 200 ms）
- **振幅**：随电极放置和个体因素而变化
- **波形**：双相或三相

### eog_findpeaks()

低级眨眼检测

```python
blinks_dict = nk.eog_findpeaks(cleaned_eog, sampling_rate=500, method='neurokit')
```

* *用例：**
- 自定义参数调优
- 算法比较
- 研究方法开发

## 特征提取

### eog_features()

提取各个眨眼的特征。

```python
features = nk.eog_features(signals, sampling_rate=500)
```

* *计算的特征：**
- **振幅速度比 (AVR)**：峰值速度/振幅
  - 区分眨眼与伪影
- **眨眼幅度比**：眨眼幅度的一致性
- **持续时间指标**：眨眼持续时间统计（平均值，SD）
- **峰值幅度**：最大偏转
- **峰值速度**：最大变化率

* *用例：**
- 眨眼质量评估
- 困倦检测（困倦时眨眼持续时间增加）
- 神经学评估（疾病中眨眼动态的改变）

### eog_rate()

计算眨眼频率（每次眨眼次数）分钟）。

```python
blink_rate = nk.eog_rate(blinks, sampling_rate=500, desired_length=None)
```

* *方法：**
- 计算眨眼间间隔
- 转换为每分钟眨眼次数
- 插值以匹配信号长度

* *典型眨眼频率：**
- **休息**：15-20 次眨眼/分钟
- **阅读/视觉任务**：5-10 次眨眼/分钟（抑制）
- **对话**：20-30 次眨眼/分钟
- **压力/干眼**：>30眨眼/分钟
- **困倦**：可变，眨眼时间较长

## 分析功能

### eog_analyze()

自动选择事件相关或间隔相关分析。

```python
analysis = nk.eog_analyze(signals, sampling_rate=500)
```

* *模式选择：**
- 持续时间< 10 秒 → 事件相关
- 持续时间 ≥ 10 秒 → 间隔相关

### eog_eventlated()

分析与特定事件相关的眨眼模式。

```python
results = nk.eog_eventrelated(epochs)
```

* *计算的指标（每个周期）：**
- `EOG_Blinks_N`：时期内的眨眼次数
- `EOG_Rate_Mean`：平均眨眼率
- `EOG_Blink_Presence`：二进制（发生任何眨眼）
- 跨时期眨眼的时间分布

* *用例：**
- 眨眼锁定 ERP 污染评估
- 刺激期间的注意力和参与度
- 视觉任务难度（在要求较高的任务期间抑制眨眼）
- 刺激偏移后自发眨眼

### eog_intervallated()

分析长时间的眨眼模式period.

```python
results = nk.eog_intervalrelated(signals, sampling_rate=500)
```

* *计算指标：**
- `EOG_Blinks_N`：眨眼总数
- `EOG_Rate_Mean`：平均眨眼率（眨眼/分钟）
- `EOG_Rate_SD`：眨眼率
- `EOG_Duration_Mean`：平均眨眼持续时间（如果有）
- `EOG_Amplitude_Mean`：平均眨眼幅度（如果有）

* *使用案例：**
- 静息状态眨眼模式
- 困倦或疲劳监测（增加持续时间）
- 持续注意力任务（抑制率）
- 干眼评估（增加率，不完全眨眼）

## 模拟和可视化

### eog_plot（）

可视化处理的EOG信号和检测到的眨眼。

```python
nk.eog_plot(signals, info)
```

* *显示：**
- 原始和清洁的 EOG 信号
- 检测到的眨眼标记
- 眨眼率时间进程

## 实际注意事项

### 采样率建议
- **最低**：100 Hz（基本眨眼检测）
- **标准**：250-500 Hz（研究应用）
- **高分辨率**：1000 Hz（详细波形分析、眼跳）
- **睡眠研究**：典型值 200-250 Hz

### 记录持续时间
- **眨眼检测**：任何持续时间（≥1 次眨眼）
- **眨眼率估计**：稳定估计≥60 秒
- **事件相关**：取决于范例（每次试验的秒数）
- **睡眠 EOG**：小时（完整）夜间）

### 电极放置

* *标准配置：**

* *水平 EOG (HEOG)：**
- 两个电极：左右眼外眦（外眼角）
- 测量水平眼球运动（扫视、平滑追踪）
- 双极记录（左 - 右）

* *垂直 EOG (VEOG)：**
- 两个电极：一只眼睛上方和下方（通常为右侧）
- 测量垂直眼球运动和眨眼
- 双极记录（上方 - 下方）

* *睡眠 EOG：**
- 经常轻微使用不同位置（太阳穴区域）
- E1：左眼外眦外侧 1 cm、下方 1 cm 
- E2：右眼外眦外侧 1 cm、上方 1 cm 
- 捕获水平和垂直运动

* *EEG 污染去除：**
- 额电极（Fp1、 Fp2)可用作 EOG 代理
- EEG 预处理中常见的基于 ICA 的 EOG 伪影去除

### 常见问题和解决方案

* *电极问题：**
- 接触不良：低振幅、噪声
- 皮肤准备：清洁、轻微磨损
- 导电凝胶：确保良好接触

* *伪影：**
- 肌肉活动（尤其是额肌）：高频噪声
- 运动：电缆伪影、头部运动
- 电噪声：50/60 Hz 嗡嗡声（正确接地）

* * 饱和度：**
- 较大的眼跳可能饱和放大器
- 调整增益或电压范围
- 低分辨率系统中更常见

### 最佳实践

* *标准工作流程：**
```python
# 1. Clean signal
cleaned = nk.eog_clean(eog_raw, sampling_rate=500, method='neurokit')

# 2. Detect blinks
blinks, info = nk.eog_peaks(cleaned, sampling_rate=500, method='neurokit')

# 3. Extract features
features = nk.eog_features(signals, sampling_rate=500)

# 4. Comprehensive processing (alternative)
signals, info = nk.eog_process(eog_raw, sampling_rate=500)

# 5. Analyze
analysis = nk.eog_analyze(signals, sampling_rate=500)
```

* *EEG 伪影校正工作流程：**
```python
# Option 1: Regression-based removal
# Identify EOG components from cleaned EOG signal
# Regress out EOG from EEG channels

# Option 2: ICA-based removal (preferred)
# 1. Run ICA on EEG data including EOG channels
# 2. Identify ICA components correlated with EOG
# 3. Remove EOG components from EEG data
# NeuroKit2 integrates with MNE for this workflow
```

## 临床和研究应用

* *EEG 伪影校正：**
- 闪烁污染额叶 EEG 通道
- ICA 或回归方法消除 EOG 伪影
- 对于 ERP 研究至关重要

* *睡眠分期：**
- REM 睡眠期间快速眼球运动 (REM)
- 睡意期间缓慢滚动眼球运动
- 睡眠开始和阶段转换

* *注意力和认知负载：**
- 在要求较高的任务期间抑制眨眼频率
- 在任务边界处闪烁集群（自然断点）
- 自发眨眼作为注意力转移的指示器

* *疲劳和睡意监测：**
- 困倦时眨眼持续时间增加
- 眼睑变慢闭合
- 部分或不完全眨眼
- 驾驶员监控应用

* *阅读和视觉处理：**
- 阅读期间抑制眨眼
- 扫视期间眼球运动（行变化）
- 疲劳对阅读效率的影响

* * 神经学疾病：**
- **帕金森病**：自发眨眼率降低
- **精神分裂症**：眨眼率增加
- **抽动秽语综合征**：过度眨眼（抽动）
- **干眼综合征**：眨眼次数增加、不完全

* *情感和社交认知：**
- 社交互动中的眨眼同步
- 眨眼频率的情绪调节
- ERP 中的眨眼相关电位

* * 人机交互：**
- 视线跟踪预处理
- 注意力监控
- 用户参与评估

## 可使用EOG检测的眼动类型

* *闪烁：**
- 大幅度，短暂持续时间（100-400毫秒）
- NeuroKit2主焦点
- 垂直EOG最敏感

* *眼跳：**
- 快速、弹道式眼球运动（20-80 ms）
- 阶梯状电压偏转
- 水平或垂直
- 需要更高的采样率进行详细分析

* *平滑追踪：**
- 缓慢跟踪移动物体
- 斜坡状电压变化
- 振幅低于眼跳

* *固定：**
- 稳定凝视
- 基线 EOG，振荡小
- 持续时间变化（200-600 毫秒）阅读中的典型）

* *注意：** 详细的扫视/注视分析通常需要眼动追踪（红外、基于视频）。 EOG 对于眨眼和粗眼动很有用。

## 解释指南

* *眨眼频率：**
- **正常休息**：15-20 次眨眼/分钟
- **<10 次眨眼/分钟**：视觉任务参与度、注意力
- **>30 次眨眼/分钟**：压力、干燥眼睛、疲劳
- **上下文相关**：任务要求、照明、屏幕使用

* *眨眼持续时间：**
- **正常**：100-400毫秒（平均~200毫秒）
- **延长**：困倦、疲劳（>500毫秒）
- **短**：正常警觉性

* *眨眼幅度：**
- 因电极放置和个体而异
- 受试者内比较最可靠
- 不完全眨眼：幅度减小（干眼、疲劳）

* * 时间模式：**
- **集群眨眼**：之间的转换任务或认知状态
- **抑制眨眼**：主动视觉处理，持续注意力
- **刺激后眨眼**：完成视觉处理后

## 参考文献

- Kleifges, K.、Bigdely-Shamlo, N.、Kerick, S.E. 和 Robbins, K.A. (2017)。 BLINKER：从脑电图中自动提取眼部指数，实现大规模分析。神经科学前沿，11, 12.
- Agarwal, M., & Sivakumar, R. (2019)。眨眼：一种全自动无监督算法，用于脑电图信号中的眨眼检测。 2019 年第 57 届阿勒顿通信、控制和计算年度会议（第 1113-1121 页）。 IEEE.
- Kong, X., & Wilson, G. F. (1998)。一种新的基于 EOG 的眨眼检测算法。行为研究方法、仪器和计算机，30(4), 713-719.
- Schleicher, R.、Galley, N.、Briest, S. 和 Galley, L. (2008)。睡意警告中眨眼和扫视作为疲劳指标：看起来很累吗？人体工程学，51(7), 982-1010.
