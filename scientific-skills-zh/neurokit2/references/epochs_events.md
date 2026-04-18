# 时代和事件相关分析

## 概述

事件相关分析检查对特定刺激或事件的时间锁定的生理反应。 NeuroKit2 提供用于所有信号类型的事件检测、纪元创建、平均和事件相关特征提取的工具。

## 事件检测

### events_find()

根据阈值交叉或阈值自动检测信号中的事件/触发

```python
events = nk.events_find(event_channel, threshold=0.5, threshold_keep='above',
                        duration_min=1, inter_min=0)
```

* *参数：**
- `threshold`：检测阈值
- `threshold_keep`：`'above'`或`'below'`阈值
- `duration_min`：最小事件持续时间（样本）要保留
- `inter_min`：事件之间的最小间隔（样本）

* *返回：**
- 字典：
  - `'onset'`：事件开始索引
  - `'offset'`：事件偏移索引（如果适用）
  - `'duration'`：事件持续时间
  - `'label'`：事件标签（如果有多个事件类型）

* *常见用例：**

* *来自实验的TTL触发器：**
```python
# Trigger channel: 0V baseline, 5V pulses during events
events = nk.events_find(trigger_channel, threshold=2.5, threshold_keep='above')
```

* *按钮按：**
```python
# Detect when button signal goes high
button_events = nk.events_find(button_signal, threshold=0.5, threshold_keep='above',
                               duration_min=10)  # Debounce
```

* *状态更改：**
```python
# Detect periods above/below threshold
high_arousal = nk.events_find(eda_signal, threshold='auto', duration_min=100)
```

### events_plot()

可视化事件时序相对于信号.

```python
nk.events_plot(events, signal)
```

* *显示：**
- 信号跟踪
- 事件标记（垂直线或阴影区域）
- 事件标签

* *用例：**
- 验证事件检测准确性
- 检查事件的时间分布
- epoch 之前的质量控制

## Epoch 创建

### epochs_create()

围绕事件创建数据epoch（片段），用于事件相关分析。

```python
epochs = nk.epochs_create(data, events, sampling_rate=1000,
                          epochs_start=-0.5, epochs_end=2.0,
                          event_labels=None, event_conditions=None,
                          baseline_correction=False)
```

* *参数：**
- `data`：带有信号或单个信号的 DataFrame
- `events`：来自 `events_find()`
- `sampling_rate` 的事件索引或字典(Hz)
- `epochs_start`：相对于事件的开始时间（秒，负 = 之前）
- `epochs_end`：相对于事件的结束时间（秒，正 = 之后）
- `event_labels`：每个事件的标签列表（可选）
- `event_conditions`：每个事件的条件名称列表（可选）
- `baseline_correction`：如果为真，则从每个时期减去基线平均值

* *返回：**
- 数据帧字典，每个时期一个
- 每个数据帧包含与事件相关的时间的信号数据（事件开始时索引= 0）
- 包括`'Label'` 和 `'Condition'` 列（如果提供）

* *典型纪元窗口：**
- **视觉 ERP**：-0.2 至 1.0 秒（200 毫秒基线，刺激后 1 秒）
- **心脏定向**：-1.0 至 10 秒（捕获预期和响应）
- **EMG 惊吓**：-0.1 至 0.5 秒（短暂响应）
- **EDA SCR**：-1.0 至 10 秒（1-3 秒延迟，缓慢恢复）

### 事件标签和条件

按类型和实验组织事件条件：

```python
# Example: Emotional picture experiment
event_times = [1000, 2500, 4200, 5800]  # Event onsets in samples
event_labels = ['trial1', 'trial2', 'trial3', 'trial4']
event_conditions = ['positive', 'negative', 'positive', 'neutral']

epochs = nk.epochs_create(signals, events=event_times, sampling_rate=1000,
                          epochs_start=-1, epochs_end=5,
                          event_labels=event_labels,
                          event_conditions=event_conditions)
```

* *访问纪元：**
```python
# Epoch by number
epoch_1 = epochs['1']

# Filter by condition
positive_epochs = {k: v for k, v in epochs.items() if v['Condition'][0] == 'positive'}
```

### 基线校正

从纪元中删除刺激前基线以隔离事件相关的变化：

* *自动（纪元期间）创建）：**
```python
epochs = nk.epochs_create(data, events, sampling_rate=1000,
                          epochs_start=-0.5, epochs_end=2.0,
                          baseline_correction=True)  # Subtracts mean of entire baseline
```

* *手动（纪元创建后）：**
```python
# Subtract baseline period mean
baseline_start = -0.5  # seconds
baseline_end = 0.0     # seconds

for key, epoch in epochs.items():
    baseline_mask = (epoch.index >= baseline_start) & (epoch.index < baseline_end)
    baseline_mean = epoch[baseline_mask].mean()
    epochs[key] = epoch - baseline_mean
```

* *何时基线正确：**
- **ERP**：始终（隔离与事件相关的更改）
- **心脏/EDA**：通常（消除个体间基线差异）
- **绝对测量**：有时不需要（例如，分析绝对幅度）

## 历元分析和可视化

### epochs_plot()

可视化个体或平均历元。

```python
nk.epochs_plot(epochs, column='ECG_Rate', condition=None, show=True)
```

* *参数：**
- `column`：要绘制哪个信号列
- `condition`：仅绘制特定条件（可选）

  * *显示：**
- 单个历元轨迹（半透明）
- 跨时期的平均值（粗线）
- 可选：阴影误差（SEM或SD）

* *用例：**
- 可视化事件相关响应
- 比较条件
- 识别异常时期

### epochs_average()

通过统计数据计算跨纪元的总平均值。

```python
average_epochs = nk.epochs_average(epochs, output='dict')
```

* *参数：**
- `output`：`'dict'`（默认）或`'df'` (DataFrame)

* *返回：**
- 字典或 DataFrame 包含：
  - `'Mean'`：每个时间点跨历元的平均值
  - `'SD'`：标准偏差
  - `'SE'`：标准误差平均值
  - `'CI_lower'`、`'CI_upper'`：95% 置信区间

* *用例：**
- 计算事件相关电位 (ERP)
- 总平均心脏/EDA/EMG 反应
- 组级别分析

* *特定条件平均：**
```python
# Separate averages by condition
positive_epochs = {k: v for k, v in epochs.items() if v['Condition'][0] == 'positive'}
negative_epochs = {k: v for k, v in epochs.items() if v['Condition'][0] == 'negative'}

avg_positive = nk.epochs_average(positive_epochs)
avg_negative = nk.epochs_average(negative_epochs)
```

### epochs_to_df()

将epochs字典转换为统一DataFrame.

```python
epochs_df = nk.epochs_to_df(epochs)
```

* *返回：**
- 所有时期堆叠的单个DataFrame
- 包括`'Epoch'`、`'Time'`、`'Label'`、`'Condition'` columns
- 促进使用 pandas/seaborn 进行统计分析和绘图

* *用例：**
- 为混合效应模型准备数据
- 使用seaborn/plotly 绘图
- 导出到 R 或统计软件

### epochs_to_array()

将纪元转换为3D NumPy数组。

```python
epochs_array = nk.epochs_to_array(epochs, column='ECG_Rate')
```

* *返回：**
- 3D数组：(n_epochs, n_timepoints, n_columns)

* *使用案例：**
- 机器学习输入（划时代的功能）
- 基于自定义数组的分析
- 数组数据的统计测试

## 信号特定事件相关分析

NeuroKit2 为每种信号类型提供专门的事件相关分析：

### ECG 事件相关
```python
ecg_epochs = nk.epochs_create(ecg_signals, events, sampling_rate=1000,
                              epochs_start=-1, epochs_end=10)
ecg_results = nk.ecg_eventrelated(ecg_epochs)
```

* *计算指标：**
- `ECG_Rate_Baseline`：事件前的心率
- `ECG_Rate_Min/Max`：时期内的最小/最大心率
- `ECG_Phase_*`：心动阶段事件发生时
- 跨时间窗口的速率动态

### EDA 事件相关
```python
eda_epochs = nk.epochs_create(eda_signals, events, sampling_rate=100,
                              epochs_start=-1, epochs_end=10)
eda_results = nk.eda_eventrelated(eda_epochs)
```

* *计算指标：**
- `EDA_SCR`：SCR 的存在（二进制）
- `SCR_Amplitude`：最大值SCR 幅度
- `SCR_Latency`： SCR 开始时间
- `SCR_RiseTime`、`SCR_RecoveryTime`
- `EDA_Tonic`： 平均强直水平

### RSP事件相关
```python
rsp_epochs = nk.epochs_create(rsp_signals, events, sampling_rate=100,
                              epochs_start=-0.5, epochs_end=5)
rsp_results = nk.rsp_eventrelated(rsp_epochs)
```

* *计算指标：**
- `RSP_Rate_Mean`：平均呼吸频率
- `RSP_Amplitude_Mean`：平均呼吸深度
- `RSP_Phase`：呼吸阶段事件
- 速率/振幅动态

### EMG 事件相关
```python
emg_epochs = nk.epochs_create(emg_signals, events, sampling_rate=1000,
                              epochs_start=-0.1, epochs_end=1.0)
emg_results = nk.emg_eventrelated(emg_epochs)
```

* *计算指标：**
- `EMG_Activation`：激活的存在
- `EMG_Amplitude_Mean/Max`：振幅统计信息
- `EMG_Onset_Latency`：激活开始时间
- `EMG_Bursts`：激活突发数量

### EOG 事件相关
```python
eog_epochs = nk.epochs_create(eog_signals, events, sampling_rate=500,
                              epochs_start=-0.5, epochs_end=2.0)
eog_results = nk.eog_eventrelated(eog_epochs)
```

* *计算指标：**
- `EOG_Blinks_N`：时期内的眨眼次数
- `EOG_Rate_Mean`：眨眼率
- 时间眨眼分布

### PPG 事件相关
```python
ppg_epochs = nk.epochs_create(ppg_signals, events, sampling_rate=100,
                              epochs_start=-1, epochs_end=10)
ppg_results = nk.ppg_eventrelated(ppg_epochs)
```

* *计算指标：**
- 与 ECG 类似：速率动态、相位信息

## 实用工作流程

### 完整的事件相关分析管道

```python
import neurokit2 as nk

# 1. Process physiological signals
ecg_signals, ecg_info = nk.ecg_process(ecg, sampling_rate=1000)
eda_signals, eda_info = nk.eda_process(eda, sampling_rate=100)

# 2. Align sampling rates if needed
eda_signals_resampled = nk.signal_resample(eda_signals, sampling_rate=100,
                                           desired_sampling_rate=1000)

# 3. Merge signals into single DataFrame
signals = pd.concat([ecg_signals, eda_signals_resampled], axis=1)

# 4. Detect events
events = nk.events_find(trigger_channel, threshold=0.5)

# 5. Add event labels and conditions
event_labels = ['trial1', 'trial2', 'trial3', ...]
event_conditions = ['condition_A', 'condition_B', 'condition_A', ...]

# 6. Create epochs
epochs = nk.epochs_create(signals, events, sampling_rate=1000,
                          epochs_start=-1.0, epochs_end=5.0,
                          event_labels=event_labels,
                          event_conditions=event_conditions,
                          baseline_correction=True)

# 7. Signal-specific event-related analysis
ecg_results = nk.ecg_eventrelated(epochs)
eda_results = nk.eda_eventrelated(epochs)

# 8. Merge results
results = pd.merge(ecg_results, eda_results, left_index=True, right_index=True)

# 9. Statistical analysis by condition
results['Condition'] = event_conditions
condition_comparison = results.groupby('Condition').mean()
```

### 处理多个事件类型

```python
# Different event types with different markers
event_type1 = nk.events_find(trigger_ch1, threshold=0.5)
event_type2 = nk.events_find(trigger_ch2, threshold=0.5)

# Combine events with labels
all_events = np.concatenate([event_type1['onset'], event_type2['onset']])
event_labels = ['type1'] * len(event_type1['onset']) + ['type2'] * len(event_type2['onset'])

# Sort by time
sort_idx = np.argsort(all_events)
all_events = all_events[sort_idx]
event_labels = [event_labels[i] for i in sort_idx]

# Create epochs
epochs = nk.epochs_create(signals, all_events, sampling_rate=1000,
                          epochs_start=-0.5, epochs_end=3.0,
                          event_labels=event_labels)

# Separate by type
type1_epochs = {k: v for k, v in epochs.items() if v['Label'][0] == 'type1'}
type2_epochs = {k: v for k, v in epochs.items() if v['Label'][0] == 'type2'}
```

### 质量控制和伪影剔除

```python
# Remove epochs with excessive noise or artifacts
clean_epochs = {}
for key, epoch in epochs.items():
    # Example: reject if EDA amplitude too high (movement artifact)
    if epoch['EDA_Phasic'].abs().max() < 5.0:  # Threshold
        # Example: reject if heart rate change too large (invalid)
        if epoch['ECG_Rate'].max() - epoch['ECG_Rate'].min() < 50:
            clean_epochs[key] = epoch

print(f"Kept {len(clean_epochs)}/{len(epochs)} epochs")

# Analyze clean epochs
results = nk.ecg_eventrelated(clean_epochs)
```

## 统计注意事项

### 样本大小
- **ERP/平均**：每个条件 20-30 次以上试验最小值
- **单独试验分析**：混合效应模型处理可变试验计数
- **组比较**：功效分析的试验数据

### 时间窗口选择
- **先验假设**：根据文献预先注册时间窗口
- **探索性**：使用完整纪元，正确进行多重比较
- **避免**：根据观测数据选择窗口（循环）

### 基线周期
- 应该没有预期效果
- 稳定估计的足够持续时间（典型值500-1000毫秒）
- 快速动态更短（例如，惊吓：100毫秒足够）

### 条件比较
- 受试者内设计的重复测量方差分析
- 不平衡的混合效应模型数据
- 非参数比较的排列检验
- 多重比较的正确性（时间点/信号）

## 常见应用

* *认知心理学：**
- P300 ERP分析
- 错误相关的消极性(ERN)
- 注意眨眼
- 工作记忆负荷效应

* *情感神经科学：**
- 情感图片观看（EDA、HR、面部肌电图）
- 恐惧调节（HR 减速、SCR）
- 效价/唤醒尺寸

* *临床研究：**
- 惊吓反应（眼轮匝肌肌电图）
- 定向反应（心率减速）
- 预期和预测误差

* *心理生理学：**
- 心脏防御反应
- 定向反射与防御反射
- 情绪期间的呼吸变化

* *人机交互：**
- 事件期间的用户参与
- 惊喜/违反期望
- 任务事件期间的认知负荷

## 参考文献

- 拉克，S.J. (2014)。事件相关电位技术简介（第二版）。麻省理工学院出版社。
- Bradley, M. M., & Lang, P. J. (2000)。测量情绪：行为、感觉和生理。载于 R. D. Lane 和 L. Nadel（主编），《情感认知神经科学》（第 242-276 页）。牛津大学出版社。
- Boucsein, W. (2012)。皮肤电活动（第二版）。 Springer.
- Gratton, G.、Coles, M. G. 和 Donchin, E. (1983)。一种离线去除眼部伪影的新方法脑电图与临床神经生理学, 55(4), 468-484.
