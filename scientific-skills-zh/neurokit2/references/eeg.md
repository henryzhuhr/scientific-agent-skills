# EEG 分析和微观状态

## 概述

分析脑电图 (EEG)信号以进行频带功率、通道质量评估、源定位和微观状态识别。 NeuroKit2 与 MNE-Python 集成，实现全面的 EEG 处理工作流程。

## 核心 EEG 功能

### eeg_power()

计算指定通道的标准频段功率。

```python
power = nk.eeg_power(eeg_data, sampling_rate=250, channels=['Fz', 'Cz', 'Pz'],
                     frequency_bands={'Delta': (0.5, 4),
                                     'Theta': (4, 8),
                                     'Alpha': (8, 13),
                                     'Beta': (13, 30),
                                     'Gamma': (30, 45)})
```

* *标准频段：**
- **Delta (0.5-4 Hz)**：深度睡眠，无意识过程
- **Theta (4-8 Hz)**：困倦、冥想、记忆编码
- **Alpha (8-13 Hz)**：放松清醒，闭眼
- **Beta (13-30 Hz)**：积极思考、专注、焦虑
- **Gamma (30-45 Hz)**：认知处理、绑定

* *返回：**
- 每个通道的功率值×频带组合的DataFrame
- 列：`Channel_Band`（例如，'Fz_Alpha'，'Cz_Beta'）

* *使用病例：**
- 静息状态分析
- 认知状态分类
- 睡眠分期
- 冥想或神经反馈监测

### eeg_badchannels()

使用统计异常值识别有问题的通道检测。

```python
bad_channels = nk.eeg_badchannels(eeg_data, sampling_rate=250, bad_threshold=2)
```

* *检测方法：**
- 跨通道的标准差异常值
- 与其他通道的相关性
- 平坦或死通道
- 超标的通道噪声

* *参数：**
- `bad_threshold`：异常值检测的 Z 分数阈值（默认值：2）

* *返回：**
- 识别为有问题的通道名称列表

* *用例：**
- 之前的质量控制分析
- 自动坏通道剔除
- 插值或排除决策

### eeg_rereference()

重新表达相对于不同参考点的电压测量。

```python
rereferenced = nk.eeg_rereference(eeg_data, reference='average', robust=False)
```

* *参考类型：**
- `'average'`：平均参考（所有电极的平均值）
- `'REST'`：参考电极标准化技术
- `'bipolar'`：电极对之间的差异记录
- 特定通道名称：使用单电极作为参考

* *常用参考：**
- **平均参考**：最常见于高密度脑电图
- **相连乳突**：传统临床脑电图
- **顶点 (Cz)**：有时用于 ERP 研究
- **休息**：近似无穷大参考

* *返回：**
- 重新引用的EEG数据

### eeg_gfp()

计算全局场功率-每次所有电极的标准差point.

```python
gfp = nk.eeg_gfp(eeg_data)
```

* *解释：**
- 高GFP：跨区域强、同步的大脑活动
- 低GFP：弱或不同步的活动
- GFP峰：稳定地形的点，用于微状态检测

* *使用案例：**
- 识别稳定地形模式的周期
- 选择微观状态分析的时间点
- 事件相关电位 (ERP)可视化

### eeg_diss()

测量电场之间的地形差异配置。

```python
dissimilarity = nk.eeg_diss(eeg_data1, eeg_data2, method='gfp')
```

* *方法：**
- 基于GFP：归一化差异
- 空间相关性
- 余弦距离

* *用例：**
- 比较之间的地形条件
- 微态转变分析
- 模板匹配

## 源定位

### eeg_source()

执行源重建以从头皮记录估计大脑水平活动。

```python
sources = nk.eeg_source(eeg_data, method='sLORETA')
```

* *方法：**
- `'sLORETA'`：标准化低分辨率电磁断层扫描
  - 点源零定位误差
  - 良好的空间分辨率
- `'MNE'`：最小范数估计
  - 快速，完善的
  - 偏向于表面来源
- `'dSPM'`：动态统计参数映射
  - 标准化MNE
- `'eLORETA'`：精确LORETA
  - 改进的本地化精度

* *要求：**
- 正演模型（前导场矩阵）
- 共同配准电极位置
- 头部模型（边界元或球形）

* *返回：**
- 源空间活动估计

### eeg_source_extract()

从特定大脑解剖区域提取活动。

```python
regional_activity = nk.eeg_source_extract(sources, regions=['PFC', 'MTL', 'Parietal'])
```

* *区域选项：**
- 标准图集：Desikan-Killiany、Destrieux、AAL
- 自定义 ROI
- Brodmann 区域

* *返回：**
- 每个区域的时间序列
- 体素的平均或主成分

* *用例：**
- 感兴趣区域分析
- 功能连接
- 源级统计数据

## 微状态分析

微状态是稳定大脑拓扑的短暂（80-120毫秒）周期，代表协调的神经网络。通常有 4-7 个具有不同功能的微状态类别（通常标记为 A、B、C、D）。

### microstates_segment()

使用聚类算法识别和提取微状态。

```python
microstates = nk.microstates_segment(eeg_data, n_microstates=4, sampling_rate=250,
                                      method='kmod', normalize=True)
```

* *方法：**
- `'kmod'` （默认）：针对 EEG 地形优化的修改 k 均值
  - 极性不变聚类
  - 微观状态文献中最常见
- `'kmeans'`：标准 k 均值聚类
- `'kmedoids'`：K 中心点（对于异常值）
- `'pca'`：主成分分析
- `'ica'`：独立成分分析
- `'aahc'`：雾化和凝聚层次聚类

* *参数：**
- `n_microstates`：微状态类的数量（通常为 4-7）
- `normalize`：标准化拓扑（推荐：True）
- `n_inits`：随机初始化的数量（增加稳定性）

* *返回：**
- 字典：
  - `'maps'`：微状态模板拓扑
  - `'labels'`：每个时间点的微状态标签
  - `'gfp'`：全局场功率
  - `'gev'`：全局解释方差

### microstates_findnumber()

E估计最佳微状态数。

```python
optimal_k = nk.microstates_findnumber(eeg_data, show=True)
```

* *标准：**
- **全局解释方差(GEV)**：方差百分比解释
  - 肘部法：在GEV曲线中找到“膝盖”
  - 通常实现70-80％GEV
  - **Krzanowski-Lai（KL）标准**：平衡拟合和简约的统计测量
  - 最大KL表示最佳k

* *典型范围：** 4-7个微状态
- 4个微状态：经典A、B、C、D状态
- 5-7个微状态：更细粒度的分解

### microstates_classify()

根据前后和左右通道重新排序微状态value.

```python
classified = nk.microstates_classify(microstates)
```

* *用途：**
- 标准化受试者之间的微状态标签
- 匹配传统的A、B、C、D拓扑：
  - **A**：左-右方向，顶枕
  - **B**：右-左方向，额颞
  - **C**：前后方向，额中央
  - **D**：额中央，前后（C 的逆）

* *返回：**
- 重新排序的微状态图和标签

### microstates_clean()

预处理脑电图数据以进行微状态提取。

```python
cleaned_eeg = nk.microstates_clean(eeg_data, sampling_rate=250)
```

* *预处理步骤：**
- 带通滤波（通常为2-20 Hz）
- 伪影抑制
- 不良通道插值
- 重新引用平均值

* *基本原理：**
- 微观状态反映大规模网络活动
- 高频和低频伪影会扭曲拓扑

### microstates_peaks()

识别微观状态的 GFP 峰

```python
peak_indices = nk.microstates_peaks(eeg_data, sampling_rate=250)
```

* *目的：**
- 通常在 GFP 峰值处分析的微观状态
- 峰值代表最大、稳定的地形活动的时刻
- 降低计算负载和噪声敏感性

* * 返回：**
- 的指数GFP 局部最大值

### microstates_static()

计算各个微状态的时间属性。

```python
static_metrics = nk.microstates_static(microstates)
```

* *指标：**
- **持续时间 (ms)**：每个微状态花费的平均时间
  - 典型： 80-120 ms
  - 反映稳定性和持久性
- **出现次数（每秒）**：微状态出现的频率
  - 进入每个状态的频率
- **覆盖率（%）**：每个微状态总时间的百分比
  - 相对dominance
- **全局解释方差 (GEV)**：每个类解释的方差
  - 模板拟合质量

  * *返回：**
  - 包含每个微状态类指标的数据帧

  * *解释：**
  - 持续时间的变化：改变的网络稳定性
- 发生变化：转变状态动态
- 覆盖范围变化：特定网络的主导地位

### microstates_dynamic()

分析之间的过渡模式microstates.

```python
dynamic_metrics = nk.microstates_dynamic(microstates)
```

* *指标：**
- **转换矩阵**：从状态 i 转换到状态 j
  - 揭示优先序列
- **转换速率**：总体转换频率
  - 更高的速率：更快切换
- **熵**：转换的随机性
  - 高熵：不可预测的切换
  - 低熵：刻板序列
- **马尔可夫测试**：转换是否依赖于历史？

  * *返回：**
  - 具有转换的字典统计

* *用例：**
- 识别临床人群中的异常微状态序列
- 网络动态和灵活性
- 状态相关信息处理

### microstates_plot()

可视化微状态拓扑和时间course.

```python
nk.microstates_plot(microstates, eeg_data)
```

* *显示：**
- 每个微状态类别的地形图
- 带有微状态标签的 GFP 迹线
- 显示状态序列的转换图
- 统计摘要

## MNE 集成实用程序

### mne_data()

从MNE-Python访问示例数据集。

```python
raw = nk.mne_data(dataset='sample', directory=None)
```

* *可用数据集：**
- `'sample'`：多模态（MEG/EEG）示例
- `'ssvep'`：稳态视觉诱发电位
- `'eegbci'`：运动想象BCI数据集

### mne_to_df() / mne_to_dict()

将MNE对象转换为NeuroKit兼容格式。

```python
df = nk.mne_to_df(raw)
data_dict = nk.mne_to_dict(epochs)
```

* *用例：**
- 在 NeuroKit2 中处理 MNE 处理的数据
- 在分析格式之间进行转换

### mne_channel_add() / mne_channel_extract()

管理 MNE 中的各个通道对象。

```python
# Extract specific channels
subset = nk.mne_channel_extract(raw, ['Fz', 'Cz', 'Pz'])

# Add derived channels
raw_with_eog = nk.mne_channel_add(raw, new_channel_data, ch_name='EOG')
```

### mne_crop()

按时间或样本修剪记录。

```python
cropped = nk.mne_crop(raw, tmin=10, tmax=100)
```

### mne_templateMRI()

为源提供模板解剖定位。

```python
subjects_dir = nk.mne_templateMRI()
```

* *用例：**
- 无需单独MRI的源分析
- 组级源定位
- fsaverage模板brain

### eeg_simulate()

生成合成EEG信号

```python
synthetic_eeg = nk.eeg_simulate(duration=60, sampling_rate=250, n_channels=32)
```

## 实际注意事项

### 采样率建议
- **最小值**：基本功率分析为 100 Hz
- **标准**：大多数应用为 250-500 Hz
- **高分辨率**：1000+ Hz 用于详细的时间动态

### 记录持续时间
- **功率分析**：稳定估计≥2 分钟
- **微观状态**：≥2-5 分钟，首选更长
- **静息状态**：典型3-10 分钟
- **与事件相关**：取决于试验次数（每个条件≥30 次试验）

### 伪影管理
- **眨眼**：使用 ICA 或回归去除
- **肌肉伪影**：高通滤波器（≥1 Hz）或手动拒绝
- **不良通道**：分析前检测和插值
- **线路噪声**：50/60 Hz 陷波滤波器

### 最佳实践

* *功效分析：**
```python
# 1. Clean data
cleaned = nk.signal_filter(eeg_data, sampling_rate=250, lowcut=0.5, highcut=45)

# 2. Identify and interpolate bad channels
bad = nk.eeg_badchannels(cleaned, sampling_rate=250)
# Interpolate bad channels using MNE

# 3. Re-reference
rereferenced = nk.eeg_rereference(cleaned, reference='average')

# 4. Compute power
power = nk.eeg_power(rereferenced, sampling_rate=250, channels=channel_list)
```

* *微观状态工作流程：**
```python
# 1. Preprocess
cleaned = nk.microstates_clean(eeg_data, sampling_rate=250)

# 2. Determine optimal number of states
optimal_k = nk.microstates_findnumber(cleaned, show=True)

# 3. Segment microstates
microstates = nk.microstates_segment(cleaned, n_microstates=optimal_k,
                                     sampling_rate=250, method='kmod')

# 4. Classify to standard labels
microstates = nk.microstates_classify(microstates)

# 5. Compute temporal metrics
static = nk.microstates_static(microstates)
dynamic = nk.microstates_dynamic(microstates)

# 6. Visualize
nk.microstates_plot(microstates, cleaned)
```

## 临床和研究应用

* *认知神经科学：**
- 注意力、工作记忆、执行力功能
- 语言处理
- 感觉知觉

* *临床人群：**
- 癫痫：癫痫发作检测、定位
- 阿尔茨海默病：脑电图减慢，微观状态改变
- 精神分裂症：微观状态改变，尤其是状态C
- ADHD：θ/β 比值增加
- 抑郁：额叶 α 不对称

* *意识研究：**
- 麻醉监测
- 意识障碍
- 睡眠分期

* *神经反馈：**
- 实时频段训练
- 放松的 Alpha 增强
- 焦点的 Beta 增强

## 参考文献

- Michel, C. M., & Koenig, T. (2018)。脑电图微状态作为研究全脑神经元网络时间动态的工具：综述。神经影像，180, 577-593.
- Pascual-Marqui, R. D.、Michel, C. M. 和 Lehmann, D. (1995)。将脑电活动分割为微观状态：模型估计和验证。 IEEE 生物医学工程汇刊，42(7), 658-665.
- Gramfort, A.、Luessi, M.、Larson, E.、Engemann, D. A.、Strohmeier, D.、Brodbeck, C.、... & Hämäläinen, M. (2013)。使用 MNE-Python 进行脑磁图和脑电图数据分析。神经科学前沿，7, 267.
