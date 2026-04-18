# 皮肤电活动 (EDA)分析

## 概述

皮肤电活动 (EDA)也称为皮肤电反应 (GSR)或皮肤电导 (SC)，测量皮肤的电导，反映交感神经系统的唤醒和汗腺活动。 EDA广泛应用于心理生理学、情感计算和测谎。

## 主处理管道

### eda_process()

自动处理返回强直/相分解和SCR特征的原始EDA信号。

```python
signals, info = nk.eda_process(eda_signal, sampling_rate=100, method='neurokit')
```

* *管道步骤：**
1. 信号净化（低通滤波）
2. 强直相分解
3. 皮肤电导反应（SCR）检测
4. SCR 特征提取（起始、峰值、幅度、上升/恢复时间）

* *返回：**
- `signals`：数据帧包含：
  - `EDA_Clean`：滤波信号
  - `EDA_Tonic`：慢变基线
  - `EDA_Phasic`：快速变化的响应
  - `SCR_Onsets`、`SCR_Peaks`、`SCR_Height`：响应标记
  - `SCR_Amplitude`、`SCR_RiseTime`、`SCR_RecoveryTime`：响应特征
- `info`：带有处理参数的字典

* *方法：**
- `'neurokit'`：cvxEDA分解+神经包峰值检测
- `'biosppy'`：中值平滑+biosppy方法

## 预处理功能

### eda_clean()

通过低通滤波去除噪声。

```python
cleaned_eda = nk.eda_clean(eda_signal, sampling_rate=100, method='neurokit')
```

* *方法：**
- `'neurokit'`：低通巴特沃斯滤波器（截止3 Hz）
- `'biosppy'`：低通巴特沃斯滤波器（5 Hz 截止）

* *自动跳过：**
- 如果采样率 < 7 Hz，则跳过清洁（已经是低通）

* *原理：**
- EDA 频率内容通常为 0-3 Hz
- 消除高频噪声和运动伪影
- 保留慢速 SCR（典型上升时间 1-3 秒）

### eda_phasic()

将 EDA 分解为强直（慢基线）和相（快速响应）分量。

```python
tonic, phasic = nk.eda_phasic(eda_cleaned, sampling_rate=100, method='cvxeda')
```

* *方法：**

* *1。 cvxEDA（默认，推荐）：**
```python
tonic, phasic = nk.eda_phasic(eda_cleaned, sampling_rate=100, method='cvxeda')
```
-凸优化方法（Greco et al., 2016）
- 稀疏相驱动模型
- 生理上最准确
- 计算密集但卓越的分解

* *2。中值平滑：**
```python
tonic, phasic = nk.eda_phasic(eda_cleaned, sampling_rate=100, method='smoothmedian')
```
- 具有可配置窗口的中值滤波器
- 快速、简单
- 不如 cvxEDA

 准确**3。高通滤波（Biopac 的 Acqknowledge）：**
```python
tonic, phasic = nk.eda_phasic(eda_cleaned, sampling_rate=100, method='highpass')
```
- 高通滤波器（0.05 Hz）提取相
- 快速计算
- 通过减法导出的补品

* *4。 SparsEDA：**
```python
tonic, phasic = nk.eda_phasic(eda_cleaned, sampling_rate=100, method='sparseda')
```
-稀疏反卷积方法
- 替代优化方法

* *返回：**
- `tonic`：慢变皮肤电导水平（SCL）
- `phasic`：快速皮肤电导反应 (SCR)

* *生理学解释：**
- **补品 (SCL)**：基线唤醒、一般激活、水化
- **阶段性 (SCR)**：事件相关反应、定向、情绪反应

### eda_peaks()

检测皮肤电导反应（SCR）在相分量中。

```python
peaks, info = nk.eda_peaks(eda_phasic, sampling_rate=100, method='neurokit',
                           amplitude_min=0.1)
```

* *方法：**
- `'neurokit'`：针对可靠性进行优化，可配置阈值
- `'gamboa2008'`：Gamboa 算法
- `'kim2004'`：Kim 的方法
- `'vanhalem2020'`：Van Halem 的方法
- `'nabian2018'`：Nabian 的算法

* *关键参数：**
- `amplitude_min`：最小 SCR 幅度（默认值：0.1） µS)
  - 太低：来自噪声的误报
  - 太高：错过小但有效的响应
- `rise_time_max`：最大上升时间（默认值：2 秒）
- `rise_time_min`：最小上升时间（默认值：0.01 秒）

* *返回：**
- 字典包含：
  - `SCR_Onsets`：SCR 开始处的索引
  - `SCR_Peaks`：峰值幅度索引
  - `SCR_Height`：基线上方的峰值高度
  - `SCR_Amplitude`：起始到峰值幅度
  - `SCR_RiseTime`：起始到峰值持续时间
  - `SCR_RecoveryTime`：峰值到恢复持续时间（50% 衰减）

* *SCR 时序约定：**
- **延迟**：刺激后 1-3 秒（典型）
- **上升时间**：0.5-3 秒
- **恢复时间**：2-10 秒（恢复到 50%）
- **最小振幅**：0.01-0.05 µS（检测阈值）

### eda_fixpeaks()

校正检测到的 SCR 峰值（当前

```python
corrected_peaks = nk.eda_fixpeaks(peaks)
```

* *注意：** 由于动态较慢，对 EDA 的重要性不如心脏信号。

## 分析函数

### eda_analyze()

根据数据自动选择适当的分析类型持续时间.

```python
analysis = nk.eda_analyze(signals, sampling_rate=100)
```

* *模式选择：**
- 持续时间 < 10 秒 → `eda_eventrelated()`
- 持续时间 ≥ 10 秒 → `eda_intervalrelated()`

* * 返回：**
- DataFrame具有适合分析模式的 EDA 指标

### eda_eventlated()

分析事件相关响应的刺激锁定 EDA 纪元。

```python
results = nk.eda_eventrelated(epochs)
```

* *计算指标（每个纪元）：**
- `EDA_SCR`： SCR 的存在（二进制：0 或 1）
- `SCR_Amplitude`：时期内的最大 SCR 幅度
- `SCR_Magnitude`：平均相性活动
- `SCR_Peak_Amplitude`：起始到峰值幅度
- `SCR_RiseTime`：从发作到峰值的时间
- `SCR_RecoveryTime`：恢复 50% 的时间
- `SCR_Latency`：从刺激到 SCR 发作的延迟
- `EDA_Tonic`：时期内的平均强直水平

* *典型参数：**
- 历元持续时间：刺激后 0-10 秒
- 基线：刺激前 -1 至 0 秒
- 预期 SCR 延迟：1-3 秒

* *用例：**
- 情绪刺激处理（图像、声音）
- 认知负荷评估（心算）
- 预期和预测错误
- 定向响应

### eda_intervallated()

分析扩展 EDA 记录的整体唤醒和激活模式。

```python
results = nk.eda_intervalrelated(signals, sampling_rate=100)
```

* *计算指标：**
- `SCR_Peaks_N`：检测到的 SCR 数量
- `SCR_Peaks_Amplitude_Mean`：平均 SCR 幅度
- `EDA_Tonic_Mean`、`EDA_Tonic_SD`：补品水平统计
- `EDA_Sympathetic`：交感神经系统指数
- `EDA_SympatheticN`：归一化交感神经指数
- `EDA_Autocorrelation`：时间结构（滞后4秒）
- `EDA_Phasic_*`：平均值、SD、最小值、最大值相分量

* *记录持续时间：**
- **最小值**：10 秒
- **建议**：稳定 SCR 速率需要 60 秒以上
- **交感指数**：需要 ≥64 秒

* *使用案例：**
- 静息状态唤醒评估
- 压力水平监测
- 基线交感神经活动
- 长期情感状态

## 专业分析功能

### eda_sympathetic()

从频段导出交感神经系统活动(0.045-0.25 Hz).

```python
sympathetic = nk.eda_sympathetic(signals, sampling_rate=100, method='posada',
                                  show=False)
```

* *方法：**
- `'posada'`：Posada-Quintero 方法 (2016)
  - 0.045-0.25 Hz 的频谱功率band
  - 针对其他自主措施进行验证
- `'ghiasi'`：Ghiasi 方法 (2018)
  - 基于替代频率的方法

* *要求：**
- **最短持续时间**：64 秒
- 足以满足目标中的频率分辨率带

* *返回：**
- `EDA_Sympathetic`：交感神经指数（绝对）
- `EDA_SympatheticN`：标准化交感神经指数（0-1）

* *解释：**
- 较高值：交感神经增强唤醒
- 反映强直交感神经活动，而不是阶段性反应
- 补充 SCR 分析

* *用例：**
- 压力评估
- 一段时间内的唤醒监测
- 认知负荷测量
- 补充 HRV 以实现自主平衡

### eda_autocor()

计算自相关以评估 EDA 的时间结构signal.

```python
autocorr = nk.eda_autocor(eda_phasic, sampling_rate=100, lag=4)
```

* *参数：**
- `lag`：以秒为单位的时间滞后（默认：4秒）

* *解释：**
- 高自相关：持续、缓慢变化的信号
- 低自相关：快速、不相关的波动
- 反映 SCR 的时间规律性

* *用例：**
- 评估信号质量
- 表征响应模式
- 区分持续与瞬态唤醒

### eda_changepoints()

检测EDA信号均值和方差的突变。

```python
changepoints = nk.eda_changepoints(eda_phasic, penalty=10000, show=False)
```

* *方法：**
- 基于惩罚的分割
- 识别之间的转换状态

* *参数：**
- `penalty`：控制灵敏度（默认：10,000）
  - 更高的惩罚：更少、更稳健的变化点
  - 更低的惩罚：对小变化更敏感

  * *返回：**
- 检测到的索引变化点
- 分段的可选可视化

* *用例：**
- 识别连续监控中的状态转换
- 按唤醒水平分段数据
- 检测实验中的阶段变化
- 自动纪元定义

## 可视化

### eda_plot()

创建处理过的EDA的静态或交互式可视化。

```python
nk.eda_plot(signals, info, static=True)
```

* *显示：**
- 原始和清洁的EDA信号
- 强直和相位分量
- 检测到的 SCR 起始、峰值和恢复
- 交感指数时程（如果计算）

* *交互模式 (`static=False`)：**
- 基于绘图的交互式探索
- 缩放、平移、悬停以了解详细信息
- 导出到图像格式

## 仿真和测试

### eda_simulate()

生成具有可配置参数的合成EDA信号。

```python
synthetic_eda = nk.eda_simulate(duration=10, sampling_rate=100, scr_number=3,
                                noise=0.01, drift=0.01)
```

* *参数：**
- `duration`：信号长度（秒）
- `sampling_rate`：采样频率 (Hz)
- `scr_number`：要包含的 SCR 数量
- `noise`：高斯噪声水平
- `drift`：慢基线漂移幅度
- `random_state`：再现性种子

* *返回：**
- 具有真实SCR形态的合成EDA信号

* *使用案例：**
- 算法测试和验证
- 教育演示
- 方法比较

## 实际考虑

### 采样率建议
- **最小值**：10 Hz（足以用于慢速SCR）
- **标准**：20-100 Hz（大多数商业系统）
- **高分辨率**：1000 Hz（研究级，过采样）

### 记录持续时间
- **SCR 检测**：≥10 秒（取决于刺激）
- **事件相关**：通常为每次 10-20 秒试验
- **间隔相关**：稳定估计≥60秒
- **交感指数**：≥64秒（频率分辨率）

### 电极放置
- **标准部位**：
  - 掌：远端/中指骨（手指）
  - 足底：脚底
- **高密度**：鱼际/小鱼际隆起
- **避免**：多毛皮肤、低汗腺密度区域
- **双边**：左手与右手（通常相似）

### 信号质量问题

* *平坦信号（无变化）：**
- 检查电极接触和凝胶
- 验证在汗腺丰富的区域是否正确放置
- 允许 5-10 分钟的适应期

* * 噪音过多：**
- 运动伪影：最大限度地减少参与者运动
- 电气干扰：检查接地、屏蔽
- 热效应：控制室温

* *基线漂移：**
- 正常：几分钟内缓慢变化
- 过量：电极极化，接触不良
- 解决方案：使用`eda_phasic()`分离强直漂移

* *无反应者：**
- ~5-10% 的人群具有最小的 EDA
- 遗传/生理变异
- 不表示设备故障

### 最佳实践

* *预处理工作流程：**
```python
# 1. Clean signal
cleaned = nk.eda_clean(eda_raw, sampling_rate=100, method='neurokit')

# 2. Decompose tonic/phasic
tonic, phasic = nk.eda_phasic(cleaned, sampling_rate=100, method='cvxeda')

# 3. Detect SCRs
signals, info = nk.eda_peaks(phasic, sampling_rate=100, amplitude_min=0.05)

# 4. Analyze
analysis = nk.eda_analyze(signals, sampling_rate=100)
```

* *与事件相关工作流程：**
```python
# 1. Process signal
signals, info = nk.eda_process(eda_raw, sampling_rate=100)

# 2. Find events
events = nk.events_find(trigger_channel, threshold=0.5)

# 3. Create epochs (-1 to 10 seconds around stimulus)
epochs = nk.epochs_create(signals, events, sampling_rate=100,
                          epochs_start=-1, epochs_end=10)

# 4. Event-related analysis
results = nk.eda_eventrelated(epochs)

# 5. Statistical analysis
# Compare SCR amplitude across conditions
```

## 临床和研究应用

* *情感和情感科学：**
- 情感的唤醒维度（不是效价）
- 情感图片观看
- 音乐诱发的情感
- 恐惧调节

* *认知过程：**
- 精神负荷和努力
- 注意力和警惕性
- 决策和不确定性
- 错误处理

* * 临床人群：**
- 焦虑症：基线升高、夸大响应
- PTSD：恐惧调节、消退缺陷
- 自闭症：非典型唤醒模式
- 精神病：恐惧反应减少

* *应用设置：**
- 测谎（测谎仪）
- 用户体验研究
- 驱动程序监测
- 现实环境中的压力评估

* *神经影像集成：**
- fMRI：EDA与杏仁核、岛叶活动相关
- 脑成像期间的并发记录
- 自主大脑耦合

## 解释指南

* *SCR 幅度：**
- **0.01-0.05 µS**：小但可检测
- **0.05-0.2 µS**：中等响应
- **>0.2 µS**：大响应
- **上下文相关**：标准化受试者内 

* *SCR 频率：**
- **静息**：每分钟 1-3 次 SCR（典型）
- **有压力**：每分钟 >5 次 SCR
- **非特异性 SCR**：自发（无可识别刺激）

* * 补品SCL：**
- **范围**：2-20 µS（个体间差异很大）
- **受试者内部变化**比绝对水平更容易解释
- **增加**：唤醒、压力、认知负荷
- **减少**：放松、习惯

## 参考文献

- Boucsein, W. (2012)。皮肤电活动（第二版）。 Springer Science & Business Media.
- Greco, A.、Valenza, G. 和 Scilingo, E. P. (2016)。 cvxEDA：皮肤电活动处理的凸优化方法。 IEEE 生物医学工程汇刊，63(4), 797-804.
- Posada-Quintero, H. F.、Florian, J. P.、Orjuela-Cañón, A. D.、Aljama-Corrales, T.、Charleston-Villalobos, S. 和 Chon, K. H. (2016)。用于评估交感神经功能的皮肤电活动的功率谱密度分析。生物医学工程年鉴，44(10), 3124-3135.
- Dawson, M. E.、Schell, A. M. 和 Filion, D. L. (2017)。皮肤电系统。见《心理生理学手册》（第 217-243 页）。剑桥大学出版社.
