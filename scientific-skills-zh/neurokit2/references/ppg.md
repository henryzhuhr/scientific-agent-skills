# 光电体积描记法 (PPG)分析

## 概述

光电体积描记法 (PPG)使用光学传感器测量微血管组织中的血容量变化。 PPG 广泛应用于可穿戴设备、脉搏血氧计和临床监护仪，用于心率、脉搏特征和心血管评估。

## 主处理管道

### ppg_process()

自动化 PPG 信号处理管道。

```python
signals, info = nk.ppg_process(ppg_signal, sampling_rate=100, method='elgendi')
```

* *管道步骤：**
1. 信号清洗（过滤）
2. 收缩峰值检测
3. 心率计算
4. 信号质量评估

* *返回：**
- `signals`：数据帧包含：
  - `PPG_Clean`：过滤后的PPG信号
  - `PPG_Peaks`：收缩峰值标记
  - `PPG_Rate`：瞬时心脏速率 (BPM)
  - `PPG_Quality`：信号质量指示器
- `info`：具有峰值索引和参数的字典

* *方法：**
- `'elgendi'`：Elgendi 等人。 (2013)算法（默认，稳健）
- `'nabian2018'`：Nabian 等人。 (2018)approach

## 预处理函数

### ppg_clean()

准备用于峰检测的原始PPG信号。

```python
cleaned_ppg = nk.ppg_clean(ppg_signal, sampling_rate=100, method='elgendi')
```

* *方法：**

* *1。 Elgendi（默认）：**
- 巴特沃斯带通滤波器 (0.5-8 Hz)
- 消除基线漂移和高频噪声
- 针对峰值检测可靠性进行优化

* *2。 Nabian2018：**
- 替代滤波方法
- 不同的频率特性

* *PPG信号特性：**
- **收缩峰值**：快速上冲，尖峰（心脏射血）
- **重搏切迹**：二级峰值（主动脉瓣）闭合）
- **基线**：由于呼吸、运动、灌注而缓慢漂移

### ppg_peaks()

检测PPG信号中的收缩峰。

```python
peaks, info = nk.ppg_peaks(cleaned_ppg, sampling_rate=100, method='elgendi',
                           correct_artifacts=False)
```

* *方法：**
- `'elgendi'`：具有动态阈值的两个移动平均线
- `'bishop'`：Bishop 算法
- `'nabian2018'`：Nabian 方法
- `'scipy'`：简单的 scipy 峰值检测

  * *伪影校正：**
  - 设置 `correct_artifacts=True` 进行生理合理性检查
  - 根据节拍间间隔异常值删除虚假峰值

  * *返回：**
  - 字典`'PPG_Peaks'` 包含峰值指数的键

* *典型的心跳间隔：**
- 成人静息：600-1200 ms (50-100 BPM)
- 运动员：可以更长（心动过缓）
- 压力/锻炼：更短（<600） ms, >100 BPM)

### ppg_findpeaks()

通过算法比较进行低电平峰值检测。

```python
peaks_dict = nk.ppg_findpeaks(cleaned_ppg, sampling_rate=100, method='elgendi')
```

* *用例：**
- 自定义参数调整
- 算法测试
- 研究方法开发

## 分析函数

### ppg_analyze()

自动选择事件相关或区间相关分析。

```python
analysis = nk.ppg_analyze(signals, sampling_rate=100)
```

* *模式选择：**
- 持续时间<10秒→事件相关
- 持续时间 ≥ 10 秒 → 间隔相关

### ppg_eventlated()

分析 PPG 对离散事件/刺激的响应。

```python
results = nk.ppg_eventrelated(epochs)
```

* *计算指标（每轮）：**
- `PPG_Rate_Baseline`：事件前的心率
- `PPG_Rate_Min/Max`：时期内的最小/最大心率
- 跨时期时间窗口的心率动态

* *用例：**
- 对情绪刺激的心血管反应
- 认知负荷评估
- 应激反应范例

### ppg_intervallated()

分析扩展的PPG记录。

```python
results = nk.ppg_intervalrelated(signals, sampling_rate=100)
```

* *计算指标：**
- `PPG_Rate_Mean`：平均心率速率
- 心率变异性 (HRV)指标
  - 委托给 `hrv()` 功能
  - 时间、频率和非线性域

* *记录持续时间：**
- 最小值：基本心率 60 秒
- HRV 分析：2-5 分钟推荐

* *使用案例：**
- 静息状态心血管评估
- 可穿戴设备数据分析
- 长期心率监测

## 质量评估

### ppg_quality()

评估信号质量和可靠性。

```python
quality = nk.ppg_quality(ppg_signal, sampling_rate=100, method='averageQRS')
```

* *方法：**

* *1。平均QRS（默认）：**
- 模板匹配方法
- 将每个脉冲与平均模板相关联
- 每节拍返回0-1 的质量分数
- 阈值：>0.6 = 可接受的质量

* *2。相异性：**
- 形貌相异性测量
- 检测形态变化

* * 使用案例：**
- 识别损坏的片段
- 在分析前过滤低质量数据
- 验证峰值检测精度

* * 共同质量问题：**
- 运动伪影：突然的信号变化
- 传感器接触不良：低振幅、噪声
- 血管收缩：信号振幅降低（寒冷、压力）

## 实用功能

### ppg_segment()

提取单个脉冲以进行形态学分析分析。

```python
pulses = nk.ppg_segment(cleaned_ppg, peaks, sampling_rate=100)
```

* *返回：**
- 脉冲时期的字典，每个时期以收缩峰值为中心
- 启用脉冲间比较
- 跨条件的形态分析

* *使用案例：**
- 脉搏波分析
- 动脉僵硬度代理
- 血管老化评估

### ppg_methods()

中使用的文档预处理方法Analysis.

```python
methods_info = nk.ppg_methods(method='elgendi')
```

* *返回：**
- 记录处理管道的字符串
- 对于出版物中的方法部分很有用

## 模拟和可视化

### ppg_simulate()

生成合成PPG信号测试。

```python
synthetic_ppg = nk.ppg_simulate(duration=60, sampling_rate=100, heart_rate=70,
                                noise=0.1, random_state=42)
```

* *参数：**
- `heart_rate`：平均 BPM（默认：70）
- `heart_rate_std`：HRV 幅度
- `noise`：高斯噪声level
- `random_state`：再现性种子

* *用例：**
- 算法验证
- 参数优化
- 教育演示

### ppg_plot()

可视化处理的PPG信号.

```python
nk.ppg_plot(signals, info, static=True)
```

* *显示：**
- 原始和清洁的 PPG 信号
- 检测到的收缩峰值
- 瞬时心率轨迹
- 信号质量指标

## 实际注意事项

### 采样率建议
- **最小**：20 Hz（基本心率）
- **标准**：50-100 Hz（大多数可穿戴设备）
- **高分辨率**：200-500 Hz（研究、脉搏波分析）
- **过高**：>1000 Hz（对于PPG)

### 记录持续时间
- **心率**：≥10 秒（几次心跳）
- **HRV 分析**：最少 2-5 分钟
- **长期监测**：数小时到数天（可穿戴设备）

### 传感器放置

* *常见部位：**
- **指尖**：信号质量最高，最常见
- **耳垂**：运动伪影较少，临床使用
- **手腕**：可穿戴设备（智能手表）
- **前额**：反射模式，医疗监测

* *透射率与反射率：**
- **透射率**：光穿过组织（指尖、耳垂）
  - 更高的信号质量
  - 更少的运动伪影
- **反射率**：从组织（手腕、前额）反射的光
  - 更容易受到噪音
  - 方便可穿戴设备

### 常见问题和解决方案

* *低信号幅度：**
- 灌注不良：温暖双手，增加血流量
- 传感器接触：调整放置，清洁皮肤
- 血管收缩：环境温度，压力

* *运动伪影：**
- 可穿戴设备中的主要问题
- 自适应过滤、基于加速度计的校正
- 模板匹配、异常值拒绝

* * 基线漂移：**
- 呼吸调制（正常）
- 运动或压力变化
- 高通过滤或去除趋势

* *丢失峰值：**
- 低质量信号：检查传感器接触
- 算法参数：调整阈值
- 尝试替代检测方法

### 最佳实践

* *标准工作流程：**
```python
# 1. Clean signal
cleaned = nk.ppg_clean(ppg_raw, sampling_rate=100, method='elgendi')

# 2. Detect peaks with artifact correction
peaks, info = nk.ppg_peaks(cleaned, sampling_rate=100, correct_artifacts=True)

# 3. Assess quality
quality = nk.ppg_quality(cleaned, sampling_rate=100)

# 4. Comprehensive processing (alternative)
signals, info = nk.ppg_process(ppg_raw, sampling_rate=100)

# 5. Analyze
analysis = nk.ppg_analyze(signals, sampling_rate=100)
```

* *PPG 的 HRV：**
```python
# Process PPG signal
signals, info = nk.ppg_process(ppg_raw, sampling_rate=100)

# Extract peaks and compute HRV
hrv_indices = nk.hrv(info['PPG_Peaks'], sampling_rate=100)

# PPG-derived HRV is valid but may differ slightly from ECG-derived HRV
# Differences due to pulse arrival time, vascular properties
```

## 临床和研究应用

* *可穿戴健康监测：**
- 消费者智能手表和健身追踪器
- 连续心率监测
- 睡眠跟踪和活动评估

* *临床监测：**
- 脉搏血氧饱和度（SpO2+心率）
- 围手术期监测
- 重症监护心率评估

* *心血管评估：**
- 脉搏波分析
- 动脉僵硬度代理（脉冲到达时间）
- 血管老化指数

* *自主功能：**
- 来自PPG的HRV（PPG-HRV）
- 压力和恢复监测
- 精神负荷评估

* *远程患者监护：**
- 远程医疗应用
- 家庭健康追踪
- 慢性病管理

* *情感计算：**
- 生理信号情感识别
- 用户体验研究
- 人机交互

## PPG与ECG

* *PPG的优点：**
- 非侵入性，无电极
- 方便长期监测
- 低成本，可小型化
- 适合可穿戴设备

* *PPG的缺点：**
- 更容易运动伪影
- 灌注不良时信号质量较低
- 心脏脉冲到达时间延迟
- 无法评估心电活动

* *HRV 比较：**
- PPG-HRV 通常对时/频域有效
- 由于脉冲传输时间变异性可能略有不同
- ECG 首选用于临床 HRV（如果可用）
- PPG 可用于研究和消费者应用

## 解释指南

* *来自 PPG 的心率：**
- 与 ECG 衍生心率的解释相同
- 轻微延迟（脉冲到达时间）对于速率计算可忽略不计
- 运动伪影更常见：用信号质量进行验证

* *脉冲幅度：**
- 反映外周灌注
- 增加：血管舒张、温暖
- 减少：血管收缩、寒冷、压力、接触不良

* *脉冲形态：**
- 收缩期峰值：心脏射血
- 重搏切迹：主动脉瓣关闭，动脉顺应性
- 老化/僵硬：较早、更突出的重搏切迹

## 参考文献

- Elgendi, M. (2012)。指尖光电体积描记图信号的分析。当前心脏病学评论，8(1), 14-25.
- Elgendi, M.、Norton, I.、Brearley, M.、Abbott, D. 和 Schuurmans, D. (2013)。热带条件下应急响应人员测量的加速光电体积描记图中的收缩峰值检测。 PloS 一，8(10)，e76585.
- Allen, J. (2007)。光电体积描记法及其在临床生理测量中的应用。生理测量，28(3)，R1.
- Tamura, T.、Maeda, Y.、Sekine, M. 和 Yoshida, M. (2014)。可穿戴光电体积描记传感器——过去和现在。电子，3(2), 282-302.
