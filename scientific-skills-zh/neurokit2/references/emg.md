# 肌电图 (EMG)分析

## 概述

肌电图 (EMG)测量骨骼肌在收缩过程中产生的电活动。 NeuroKit2中的肌电分析侧重于振幅估计、肌肉激活检测以及心理生理学和运动控制研究的时间动力学。

## 主处理管道

### emg_process()

自动化肌电信号处理管道。

```python
signals, info = nk.emg_process(emg_signal, sampling_rate=1000)
```

* *管道步骤：**
1. 信号清理（高通滤波、去趋势）
2. 幅度包络提取
3. 肌肉激活检测
4. 起始和偏移识别

* *返回：**
- `signals`：数据帧包含：
  - `EMG_Clean`：滤波后的EMG信号
  - `EMG_Amplitude`：线性包络（平滑整流信号）
  - `EMG_Activity`：二元激活指示符 (0/1)
  - `EMG_Onsets`：激活起始标记
  - `EMG_Offsets`：激活偏移标记
- `info`：包含激活参数的字典

* *典型工作流程：**
- 处理原始肌电图 → 提取振幅 → 检测激活 → 分析特征

## 预处理函数

### emg_clean()

应用过滤以消除噪声并准备振幅提取。

```python
cleaned_emg = nk.emg_clean(emg_signal, sampling_rate=1000)
```

* *过滤方法 (BioSPPy)方法）：**
- 四阶巴特沃斯高通滤波器（100 Hz）
- 消除低频运动伪影和基线漂移
- 消除直流偏移
- 信号去趋势

* *基本原理：**
- EMG 频率内容：20-500 Hz （主频率：50-150 Hz）
- 100 Hz 高通隔离肌肉活动
- 消除心电图污染（尤其是躯干肌肉）
- 消除运动伪影（<20 Hz）

* *EMG 信号特征：**
- 期间的随机、零均值振荡收缩
- 更高的振幅=更强的收缩
- 原始肌电图：正向和负向偏转

## 特征提取

### emg_amplitude()

计算代表肌肉收缩强度的线性包络。

```python
amplitude = nk.emg_amplitude(cleaned_emg, sampling_rate=1000)
```

* *方法：**
1. 全波整流（绝对值）
2. 低通滤波（平滑包络）
3. 下采样（可选）

* *线性包络：**
- 跟随 EMG 幅度调制的平滑曲线
- 表示肌肉力量/激活水平
- 适合进一步分析（激活检测、积分）

* *典型平滑：**
- 低通滤波器：10-20 Hz cutoff
- 移动平均值：50-200 ms 窗口
- 平衡：响应性与平滑性

## 激活检测

### emg_activation()

检测肌肉激活的周期（起始和终止）偏移量）。

```python
activity, info = nk.emg_activation(emg_amplitude, sampling_rate=1000, method='threshold',
                                   threshold='auto', duration_min=0.05)
```

* *方法：**

* *1。基于阈值（默认）：**
```python
activity = nk.emg_activation(amplitude, method='threshold', threshold='auto')
```
- 将幅度与阈值进行比较
- `threshold='auto'`：基于信号统计自动（例如平均值 + 1 SD）
- `threshold=0.1`：手动绝对阈值
- 简单、快速、广泛使用

* *2。高斯混合模型（GMM）：**
```python
activity = nk.emg_activation(amplitude, method='mixture', n_clusters=2)
```
-无监督聚类：主动与休息
- 适应信号特征
- 对变化基线更稳健

* *3。变化点检测：**
```python
activity = nk.emg_activation(amplitude, method='changepoint')
```
- 检测信号属性中的突变
- 识别激活/停用点
- 对于复杂的时间模式很有用

* *4。双峰性（Silva 等人，2013）：**
```python
activity = nk.emg_activation(amplitude, method='bimodal')
```
- 双峰分布测试（主动与休息）
- 确定最佳分离阈值
- 统计原理

* *关键参数：**
- `duration_min`：最小激活持续时间（秒）
  - 过滤短暂的虚假激活
  - 典型：50-100 ms
- `threshold`：激活阈值（取决于方法）

* *返回：**
- `activity`：二进制数组（0 = 休息， 1 = 活动)
- `info`：带有起始/偏移索引的字典

* *激活指标：**
- **起始**：从休息到活动的转换
- **偏移**：从活动到休息的转换
- **持续时间**：起始和偏移之间的时间
- **突发**：连续激活的单周期

## 分析功能

### emg_analyze()

自动选择事件相关或间隔相关分析。

```python
analysis = nk.emg_analyze(signals, sampling_rate=1000)
```

* *模式选择：**
- 持续时间<10秒→事件相关
- 持续时间≥10秒→间隔相关

### emg_eventlated()

分析肌电图对离散事件/刺激的响应。

```python
results = nk.emg_eventrelated(epochs)
```

* *计算指标（每个时期）：**
- `EMG_Activation`：激活的存在（二进制）
- `EMG_Amplitude_Mean`：历元期间的平均振幅
- `EMG_Amplitude_Max`：峰值振幅
- `EMG_Bursts`：激活突发数
- `EMG_Onset_Latency`：从事件到首次激活的时间（如果适用）

* *使用病例：**
- 惊吓反应（眼轮匝肌肌电图）
- 情绪刺激期间的面部肌电图（皱眉肌、颧肌）
- 运动反应延迟
- 肌肉反应范式

### emg_intervallated()

分析扩展 EMG 记录。

```python
results = nk.emg_intervalrelated(signals, sampling_rate=1000)
```

* *计算指标：**
- `EMG_Bursts_N`：激活突发总数
- `EMG_Amplitude_Mean`：整个过程的平均振幅间隔
- `EMG_Activation_Duration`：处于活动状态的总时间
- `EMG_Rest_Duration`：处于休息状态的总时间

* *用例：**
- 静息肌张力评估
- 慢性疼痛或压力相关的肌肉活动
- 持续期间的疲劳监测任务
- 姿势肌肉评估

## 模拟和可视化

### emg_simulate()

生成用于测试的合成肌电信号。

```python
synthetic_emg = nk.emg_simulate(duration=10, sampling_rate=1000, burst_number=3,
                                noise=0.1, random_state=42)
```

* *参数：**
- `burst_number`：要包含的激活突发数量
- `noise`：背景噪声水平
- `random_state`：再现性种子

* *生成的特征：**
- 突发期间的随机 EMG 振荡
- 真实频率内容
- 可变突发定时和幅度

* *用例：**
- 算法验证
- 检测参数调整
- 教育演示

### emg_plot()

可视化处理的 EMG 信号。

```python
nk.emg_plot(signals, info, static=True)
```

* *显示：**
- 原始和清洁的 EMG 信号
- 幅度包络
- 检测到的激活周期
- 起始/偏移标记

* *交互模式：** 设置 `static=False` 用于绘图可视化

## 实际注意事项

### 采样率建议
- **最小值**：500 Hz（奈奎斯特用于 250 Hz 上限频率）
- **标准**： 1000 Hz（大多数研究应用）
- **高分辨率**：2000-4000 Hz（详细的运动单元研究）
- **表面肌电图**：典型值 1000-2000 Hz
- **肌内肌电图**：单电机 10,000+ Hz单位

### 记录持续时间
- **与事件相关**：取决于范例（例如，每次试验 2-5 秒）
- **持续收缩**：秒到分钟
- **疲劳研究**：分钟到小时
- **慢性监测**：天（可穿戴式EMG)

### 电极放置

* *表面肌电图（最常见）：**
- 双极配置（肌肉腹部上的两个电极）
- 电中性部位（骨）上的参考/接地电极
- 皮肤准备：清洁、磨损、降低阻抗
- 电极间距离：10-20 毫米（SENIAM 标准）

* *肌肉特定指南：**
- 遵循 SENIAM（用于肌肉非侵入性评估的表面肌电图）建议
- 收缩时触诊肌肉以定位腹部
- 将电极与肌纤维方向对齐

* *心理生理学中的常见肌肉：**
- **皱眉肌**：皱眉，负面影响（眉毛上方）
- **颧大肌**：微笑，正面影响（脸颊）
- **眼轮匝肌**：惊吓反应，恐惧（眼睛周围）
- **咬肌**：下巴咬紧牙关、压力（下颌肌肉）
- **斜方肌**：肩部紧张、压力（上背部）
- **额肌**：前额紧张、意外

### 信号质量问题

* *ECG 污染：**
- 常见于躯干和近端肌肉
- 高通滤波(>100 Hz)通常足够
- 如果持续：模板减法，ICA

* *运动伪影：**
- 低频干扰
- 电极电缆运动
- 固定电极，尽量减少电缆运动

* *电极问题：**
- 接触不良：高阻抗，低振幅
- 出汗：振幅逐渐增加，不稳定
- 头发：清洁或剃须区域

* *串扰：**
- 相邻肌肉活动出血记录
- 小心的电极放置
- 小电极间距离

### 最佳实践

* *标准工作流程：**
```python
# 1. Clean signal (high-pass filter, detrend)
cleaned = nk.emg_clean(emg_raw, sampling_rate=1000)

# 2. Extract amplitude envelope
amplitude = nk.emg_amplitude(cleaned, sampling_rate=1000)

# 3. Detect activation periods
activity, info = nk.emg_activation(amplitude, sampling_rate=1000,
                                   method='threshold', threshold='auto')

# 4. Comprehensive processing (alternative)
signals, info = nk.emg_process(emg_raw, sampling_rate=1000)

# 5. Analyze
analysis = nk.emg_analyze(signals, sampling_rate=1000)
```

* *标准化：**
```python
# Maximum voluntary contraction (MVC) normalization
mvc_amplitude = np.max(mvc_emg_amplitude)  # From separate MVC trial
normalized_emg = (amplitude / mvc_amplitude) * 100  # Express as % MVC

# Common in ergonomics, exercise physiology
# Allows comparison across individuals and sessions
```

## 临床和研究应用

* *心理生理学：**
- **面部EMG**：情绪效价（微笑与皱眉）
- **惊吓反应**：恐惧、惊讶、防御反应
- **压力**：慢性肌肉紧张（斜方肌、咬肌）

* *运动控制和康复：**
- 步态分析
- 运动障碍（震颤、肌张力障碍）
- 中风康复（肌肉重新激活）
- 假肢控制（肌电）

* *人体工程学和职业健康：**
- 与工作相关的肌肉骨骼疾病
- 姿势评估
- 重复劳损受伤风险

* *运动科学：**
- 运动期间的肌肉激活模式
- 疲劳评估（中频偏移）
- 训练优化

* *生物反馈：**
- 放松训练（降低肌肉张力）
- 神经肌肉再教育
- 慢性疼痛管理

* *睡眠药物：**
- 快速眼动睡眠肌张力下降的下巴肌电图
- 周期性肢体运动
- 磨牙症（牙齿）研磨）

## 高级肌电图分析（超越NeuroKit2基本功能）

* *频域：**
- 疲劳期间的中频偏移
- 功率谱分析
- 需要更长的段（每个分析窗口≥1秒）

* *运动单元识别：**
- 肌内肌电图
- 尖峰检测和分类
- 发射率分析
- 需要高采样率（10+ kHz）

* *肌肉协调：**
- 协同收缩指数
- 协同作用分析
- 多肌肉整合

## 解释指南

* *振幅（线性包络）：**
- 较高的振幅≈较强的收缩（不完全线性）
- 与力的关系：S形，受多种因素影响
- 受试者内比较最多可靠

* *激活阈值：**
- 自动阈值：方便但可通过视觉验证
- 手动阈值：非标准肌肉可能需要
- 静息基线：应接近零（如果不是，检查电极）

* *突发特性：**
- **相**：短暂突发（惊吓、快速运动）
- **强直**：持续激活（姿势、持续握力）
- **节奏**：重复爆发（震颤、行走）

## 参考文献

- Fridlund, A. J. 和 Cacioppo, J. T. (1986)。人体肌电图研究指南。心理生理学，23(5), 567-589.
- Hermens, H. J.、Freriks, B.、Disselhorst-Klug, C. 和 Rau, G. (2000)。制定 SEMG 传感器和传感器放置程序的建议。肌电图和运动学杂志，10(5), 361-374.
- Silva, H.、Scherer, R.、Sousa, J. 和 Londral, A. (2013)。致力于提高肌电图接口的稳定性。口腔康复杂志，40(6), 456-465.
- Tassinary, L. G.、Cacioppo, J. T. 和 Vanman, E. J. (2017)。骨骼运动系统：表面肌电图。见《心理生理学手册》（第 267-299 页）。剑桥大学出版社.
