# 质量指标参考

使用 SpikeInterface 指标和 Allen/IBL 标准进行单元质量评估的综合指南。

## 概述

质量指标评估排序单元的三个方面：

|类别 |问题 |关键指标|
|---------|----------|------------|
| **污染**（I 型）|尖峰是来自多个神经元吗？ | ISI 违规，SNR |
| **完整性**（类型 II）|我们是否缺少尖峰？ |振幅截止、存在比|
| **稳定性** |随着时间的推移，单位是否稳定？ |漂移指标，振幅 CV |

## 计算质量指标

```python
import spikeinterface.full as si

# Create analyzer with computed waveforms
analyzer = si.create_sorting_analyzer(sorting, recording, sparse=True)
analyzer.compute('random_spikes', max_spikes_per_unit=500)
analyzer.compute('waveforms', ms_before=1.5, ms_after=2.0)
analyzer.compute('templates')
analyzer.compute('noise_levels')
analyzer.compute('spike_amplitudes')
analyzer.compute('principal_components', n_components=5)

# Compute all quality metrics
analyzer.compute('quality_metrics')

# Or compute specific metrics
analyzer.compute('quality_metrics', metric_names=[
    'firing_rate', 'snr', 'isi_violations_ratio',
    'presence_ratio', 'amplitude_cutoff'
])

# Get results
qm = analyzer.get_extension('quality_metrics').get_data()
print(qm.columns.tolist())  # Available metrics
```

## 指标定义和阈值

#### 污染指标

#### ISI 违规比率
违反不应期的尖峰分数。所有神经元都有约 1.5 毫秒的不应期。

```python
# Compute with custom refractory period
analyzer.compute('quality_metrics',
                 metric_names=['isi_violations_ratio'],
                 isi_threshold_ms=1.5,
                 min_isi_ms=0.0)
```

|价值|释义 |
|------|---------------|
| < 0.01 |优秀（隔离良好的单机）|
| 0.01 - 0.1 |良好（轻微污染）|
| 0.1 - 0.5 | 0.1 - 0.5中等（可能有多单位活动）|
| > 0.5 |差（可能是多单元）|

* *参考：** Hill 等人。 (2011) J Neurosci 31:8699-8705

#### 信噪比 (SNR)
峰值波形幅度与背景噪声的比率。

```python
analyzer.compute('quality_metrics', metric_names=['snr'])
```

|价值|解读 |
|------|---------------|
| > 10 |优秀|
| 5 - 10 | 5 - 10好|
| 2 - 5 | 2 - 5可接受|
| < 2 |较差（可能是噪声） |

#### 隔离距离
到 PCA 空间中最近簇的马哈拉诺比斯距离。

```python
analyzer.compute('quality_metrics',
                 metric_names=['isolation_distance'],
                 n_neighbors=4)
```

|价值|解读|
|------|---------------|
| > 50 |隔离良好|
| 20 - 50 | 20 - 50中度隔离|
| < 20 |隔离不良|

#### L-ratio
基于马氏距离的污染测量。

|价值|释义|
|------|---------------|
| < 0.05 |隔离良好|
| 0.05 - 0.1 |可接受|
| > 0.1 |污染|

#### D-prime
单元和最近邻之间的可区分性。

|价值|解释|
|------|---------------|
| > 8 |优异的分离度|
| 5 - 8 | 5 - 8分离效果好|
| < 5 |分离差 |

### 完整性指标

#### 振幅截止值
E 估计低于检测阈值的尖峰分数。

```python
analyzer.compute('quality_metrics',
                 metric_names=['amplitude_cutoff'],
                 peak_sign='neg')  # 'neg', 'pos', or 'both'
```

|价值|释义 |
|------|---------------|
| < 0.01 |优秀（接近完成）|
| 0.01 - 0.1 |好|
| 0.1 - 0.2 |中等（一些错过了峰值）|
| > 0.2 |差（许多错过的尖峰） |

* *对于精确的时序分析：** 使用 < 0.01

#### 存在率 
检测到的尖峰的记录时间分数。

```python
analyzer.compute('quality_metrics',
                 metric_names=['presence_ratio'],
                 bin_duration_s=60)  # 1-minute bins
```

|价值|解读|
|------|---------------|
| > 0.99 |优秀|
| 0.9 - 0.99 | 0.9 - 0.99好|
| 0.8 - 0.9 |可接受|
| < 0.8 |单位可能已漂移 |

### 稳定性指标

#### 漂移指标
测量单位随时间的移动。

```python
analyzer.compute('quality_metrics',
                 metric_names=['drift_ptp', 'drift_std', 'drift_mad'])
```

|公制|描述 |物超所值|
|--------|-------------|------------|
| `drift_ptp` |峰间漂移 (μm) | < 40 |
| `drift_std` |漂移标准差| < 10 |
| `drift_mad` |中位绝对偏差| < 10 |

#### 振幅 CV
尖峰振幅的变异系数。

|价值|释义 |
|------|---------------|
| < 0.25 |非常稳定|
| 0.25 - 0.5 | 0.25 - 0.5可接受|
| > 0.5 |不稳定（漂移或污染） |

### 集群质量指标

#### Silhouette 分数
集群凝聚力与分离（-1 到 1）。

|价值|解读|
|------|---------------|
| > 0.5 |明确定义的集群|
| 0.25 - 0.5 | 0.25 - 0.5中等|
| < 0.25 |重叠集群 |

#### 最近邻度量

```python
analyzer.compute('quality_metrics',
                 metric_names=['nn_hit_rate', 'nn_miss_rate'],
                 n_neighbors=4)
```

|公制|描述 |物超所值|
|--------|-------------|------------|
| `nn_hit_rate` |具有相同单位邻居的尖峰分数 | > 0.9 |
| `nn_miss_rate` |与其他单位邻居的尖峰分数 | < 0.1 |

## 标准过滤标准

### Allen Institute 默认值

```python
# Allen Visual Coding / Behavior defaults
allen_query = """
    presence_ratio > 0.95 and
    isi_violations_ratio < 0.5 and
    amplitude_cutoff < 0.1
"""
good_units = qm.query(allen_query).index.tolist()
```

### IBL 标准

```python
# IBL reproducible ephys criteria
ibl_query = """
    presence_ratio > 0.9 and
    isi_violations_ratio < 0.1 and
    amplitude_cutoff < 0.1 and
    firing_rate > 0.1
"""
good_units = qm.query(ibl_query).index.tolist()
```

### 严格单单元条件

```python
# For precise timing / spike-timing analyses
strict_query = """
    snr > 5 and
    presence_ratio > 0.99 and
    isi_violations_ratio < 0.01 and
    amplitude_cutoff < 0.01 and
    isolation_distance > 20 and
    drift_ptp < 40
"""
single_units = qm.query(strict_query).index.tolist()
```

### 多单元活动 (MUA)

```python
# Include multi-unit activity
mua_query = """
    snr > 2 and
    presence_ratio > 0.5 and
    isi_violations_ratio < 1.0
"""
all_units = qm.query(mua_query).index.tolist()
```

## 可视化

### 质量指标摘要

```python
# Plot all metrics
si.plot_quality_metrics(analyzer)
```

### 个体指标分布

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

metrics = ['snr', 'isi_violations_ratio', 'presence_ratio',
           'amplitude_cutoff', 'firing_rate', 'drift_ptp']

for ax, metric in zip(axes.flat, metrics):
    ax.hist(qm[metric].dropna(), bins=50, edgecolor='black')
    ax.set_xlabel(metric)
    ax.set_ylabel('Count')
    # Add threshold line
    if metric == 'snr':
        ax.axvline(5, color='r', linestyle='--', label='threshold')
    elif metric == 'isi_violations_ratio':
        ax.axvline(0.01, color='r', linestyle='--')
    elif metric == 'presence_ratio':
        ax.axvline(0.9, color='r', linestyle='--')

plt.tight_layout()
```

### 单位质量摘要

```python
# Comprehensive unit summary plot
si.plot_unit_summary(analyzer, unit_id=0)
```

### 质量与发射率

```python
fig, ax = plt.subplots()
scatter = ax.scatter(qm['firing_rate'], qm['snr'],
                     c=qm['isi_violations_ratio'],
                     cmap='RdYlGn_r', alpha=0.6)
ax.set_xlabel('Firing Rate (Hz)')
ax.set_ylabel('SNR')
plt.colorbar(scatter, label='ISI Violations')
ax.set_xscale('log')
```

## 计算所有指标Once

```python
# Full quality metrics computation
all_metric_names = [
    # Firing properties
    'firing_rate', 'presence_ratio',
    # Waveform
    'snr', 'amplitude_cutoff', 'amplitude_cv_median', 'amplitude_cv_range',
    # ISI
    'isi_violations_ratio', 'isi_violations_count',
    # Drift
    'drift_ptp', 'drift_std', 'drift_mad',
    # Isolation (require PCA)
    'isolation_distance', 'l_ratio', 'd_prime',
    # Nearest neighbor (require PCA)
    'nn_hit_rate', 'nn_miss_rate',
    # Cluster quality
    'silhouette_score',
    # Synchrony
    'sync_spike_2', 'sync_spike_4', 'sync_spike_8',
]

# Compute PCA first (required for some metrics)
analyzer.compute('principal_components', n_components=5)

# Compute metrics
analyzer.compute('quality_metrics', metric_names=all_metric_names)
qm = analyzer.get_extension('quality_metrics').get_data()

# Save to CSV
qm.to_csv('quality_metrics.csv')
```

## 自定义指标

```python
from spikeinterface.qualitymetrics import compute_firing_rates, compute_snrs

# Compute individual metrics
firing_rates = compute_firing_rates(sorting)
snrs = compute_snrs(analyzer)

# Add custom metric to DataFrame
qm['custom_score'] = qm['snr'] * qm['presence_ratio'] / (qm['isi_violations_ratio'] + 0.001)
```

## 参考文献

- [SpikeInterface质量指标](https://spikeinterface.readthedocs.io/en/latest/modules/qualitymetrics.html)
- [艾伦研究所 ecephys_quality_metrics](https://allensdk.readthedocs.io/en/latest/_static/examples/nb/ecephys_quality_metrics.html)
- Hill 等人。 (2011)“细胞外信号尖峰分选的质量指标”
- Siegle 等人。 (2021)“小鼠视觉系统中尖峰的调查揭示了功能层次”
