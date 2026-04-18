# 后处理和分析参考

排序神经像素数据的质量指标、可视化和分析的综合指南。

## 排序分析器

`SortingAnalyzer`是后处理的中心对象。

### 创建分析器
```python
import spikeinterface.full as si

# Create analyzer
analyzer = si.create_sorting_analyzer(
    sorting,
    recording,
    sparse=True,                    # Use sparse representation
    format='binary_folder',         # Storage format
    folder='analyzer_output'        # Save location
)
```

### 计算扩展
```python
# Compute all standard extensions
analyzer.compute('random_spikes')       # Random spike selection
analyzer.compute('waveforms')           # Extract waveforms
analyzer.compute('templates')           # Compute templates
analyzer.compute('noise_levels')        # Noise estimation
analyzer.compute('principal_components')  # PCA
analyzer.compute('spike_amplitudes')    # Amplitude per spike
analyzer.compute('correlograms')        # Auto/cross correlograms
analyzer.compute('unit_locations')      # Unit locations
analyzer.compute('spike_locations')     # Per-spike locations
analyzer.compute('template_similarity') # Template similarity matrix
analyzer.compute('quality_metrics')     # Quality metrics

# Or compute multiple at once
analyzer.compute([
    'random_spikes', 'waveforms', 'templates', 'noise_levels',
    'principal_components', 'spike_amplitudes', 'correlograms',
    'unit_locations', 'quality_metrics'
])
```

### 保存并加载
```python
# Save
analyzer.save_as(folder='analyzer_saved', format='binary_folder')

# Load
analyzer = si.load_sorting_analyzer('analyzer_saved')
```

## 质量指标

### 计算指标
```python
analyzer.compute('quality_metrics')
qm = analyzer.get_extension('quality_metrics').get_data()
print(qm)
```

### 可用指标

|公制|描述 |良好的价值观|
|--------|-------------|------------|
| `snr` |信噪比 | > 5 |
| `isi_violations_ratio` | ISI违规率| < 0.01 (1%) |
| `isi_violations_count` | ISI 违规计数 |低|
| `presence_ratio` |带有尖峰的记录分数| > 0.9 |
| `firing_rate` |每秒峰值 | 0.1-50赫兹|
| `amplitude_cutoff` |估计错过的峰值| < 0.1 |
| `amplitude_median` |中值尖峰幅度| - |
| `amplitude_cv` |变异系数| < 0.5 |
| `drift_ptp` |峰间漂移 (um) | < 40 |
| `drift_std` |漂移标准差| < 10 |
| `drift_mad` |中位绝对偏差| < 10 |
| `sliding_rp_violation` |滑动不应期| < 0.05 |
| `sync_spike_2` |与其他单位同步 | < 0.5 |
| `isolation_distance` |马哈拉诺比斯距离 | > 20 |
| `l_ratio` | L 比（隔离）| < 0.1 |
| `d_prime` |可辨别性| > 5 |
| `nn_hit_rate` |最近邻命中率| > 0.9 |
| `nn_miss_rate` |最近邻居未命中率| < 0.1 |
| `silhouette_score` |集群剪影| > 0.5 |

### 计算特定指标
```python
analyzer.compute(
    'quality_metrics',
    metric_names=['snr', 'isi_violations_ratio', 'presence_ratio', 'firing_rate']
)
```

### 自定义质量阈值
```python
qm = analyzer.get_extension('quality_metrics').get_data()

# Define quality criteria
quality_criteria = {
    'snr': ('>', 5),
    'isi_violations_ratio': ('<', 0.01),
    'presence_ratio': ('>', 0.9),
    'firing_rate': ('>', 0.1),
    'amplitude_cutoff': ('<', 0.1),
}

# Filter good units
good_units = qm.query(
    "(snr > 5) & (isi_violations_ratio < 0.01) & (presence_ratio > 0.9)"
).index.tolist()

print(f"Good units: {len(good_units)}/{len(qm)}")
```

## 波形和模板

### 提取波形
```python
analyzer.compute('waveforms', ms_before=1.5, ms_after=2.5, max_spikes_per_unit=500)

# Get waveforms for a unit
waveforms = analyzer.get_extension('waveforms').get_waveforms(unit_id=0)
print(f"Shape: {waveforms.shape}")  # (n_spikes, n_samples, n_channels)
```

### 计算模板
```python
analyzer.compute('templates', operators=['average', 'std', 'median'])

# Get template
templates_ext = analyzer.get_extension('templates')
template = templates_ext.get_unit_template(unit_id=0, operator='average')
```

### 模板相似度
```python
analyzer.compute('template_similarity')
sim = analyzer.get_extension('template_similarity').get_data()
# Matrix of cosine similarities between templates
```

## 单元位置

### 计算位置
```python
analyzer.compute('unit_locations', method='monopolar_triangulation')
locations = analyzer.get_extension('unit_locations').get_data()
print(locations)  # x, y coordinates per unit
```

### 峰值位置
```python
analyzer.compute('spike_locations', method='center_of_mass')
spike_locs = analyzer.get_extension('spike_locations').get_data()
```

### 定位方法
- `'center_of_mass'` - 快速，不太准确
- `'monopolar_triangulation'` - 更准确，较慢
- `'grid_convolution'` - 平衡良好

## 相关图

### 自相关图
```python
analyzer.compute('correlograms', window_ms=50, bin_ms=1)
correlograms, bins = analyzer.get_extension('correlograms').get_data()

# correlograms shape: (n_units, n_units, n_bins)
# Auto-correlogram for unit i: correlograms[i, i, :]
# Cross-correlogram units i,j: correlograms[i, j, :]
```

## 可视化

### 探针地图
```python
si.plot_probe_map(recording, with_channel_ids=True)
```

### 单元模板
```python
# All units
si.plot_unit_templates(analyzer)

# Specific units
si.plot_unit_templates(analyzer, unit_ids=[0, 1, 2])
```

### 波形
```python
# Plot waveforms with template
si.plot_unit_waveforms(analyzer, unit_ids=[0])

# Waveform density
si.plot_unit_waveforms_density_map(analyzer, unit_id=0)
```

### 光栅绘图
```python
si.plot_rasters(sorting, time_range=(0, 10))  # First 10 seconds
```

### 振幅
```python
analyzer.compute('spike_amplitudes')
si.plot_amplitudes(analyzer)

# Distribution
si.plot_all_amplitudes_distributions(analyzer)
```

### 相关图
```python
# Auto-correlograms
si.plot_autocorrelograms(analyzer, unit_ids=[0, 1, 2])

# Cross-correlograms
si.plot_crosscorrelograms(analyzer, unit_ids=[0, 1])
```

### 质量指标
```python
# Summary plot
si.plot_quality_metrics(analyzer)

# Specific metric distribution
import matplotlib.pyplot as plt
qm = analyzer.get_extension('quality_metrics').get_data()
plt.hist(qm['snr'], bins=50)
plt.xlabel('SNR')
plt.ylabel('Count')
```

### 探头上的单位位置
```python
si.plot_unit_locations(analyzer)
```

### 漂移地图
```python
si.plot_drift_raster(sorting, recording)
```

### 摘要Plot
```python
# Comprehensive unit summary
si.plot_unit_summary(analyzer, unit_id=0)
```

## LFP 分析

### 加载 LFP 数据
```python
lfp = si.read_spikeglx('/path/to/data', stream_id='imec0.lf')
print(f"LFP: {lfp.get_sampling_frequency()} Hz")
```

### 基本 LFP 处理
```python
# Downsample if needed
lfp_ds = si.resample(lfp, resample_rate=1000)

# Common average reference
lfp_car = si.common_reference(lfp_ds, reference='global', operator='median')
```

### 提取 LFP迹线
```python
import numpy as np

# Get traces (channels x samples)
traces = lfp.get_traces(start_frame=0, end_frame=30000)

# Specific channels
traces = lfp.get_traces(channel_ids=[0, 1, 2])
```

### 光谱分析
```python
from scipy import signal
import matplotlib.pyplot as plt

# Get single channel
trace = lfp.get_traces(channel_ids=[0]).flatten()
fs = lfp.get_sampling_frequency()

# Power spectrum
freqs, psd = signal.welch(trace, fs, nperseg=4096)
plt.semilogy(freqs, psd)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power')
plt.xlim(0, 100)
```

### 频谱图
```python
f, t, Sxx = signal.spectrogram(trace, fs, nperseg=2048, noverlap=1024)
plt.pcolormesh(t, f, 10*np.log10(Sxx), shading='gouraud')
plt.ylabel('Frequency (Hz)')
plt.xlabel('Time (s)')
plt.ylim(0, 100)
plt.colorbar(label='Power (dB)')
```

## 导出格式

### 导出到Phy
```python
si.export_to_phy(
    analyzer,
    output_folder='phy_export',
    compute_pc_features=True,
    compute_amplitudes=True,
    copy_binary=True
)
# Then: phy template-gui phy_export/params.py
```

### 导出到NWB
```python
from spikeinterface.exporters import export_to_nwb

export_to_nwb(
    recording,
    sorting,
    'output.nwb',
    metadata=dict(
        session_description='Neuropixels recording',
        experimenter='Name',
        lab='Lab name',
        institution='Institution'
    )
)
```

### 导出报告
```python
si.export_report(
    analyzer,
    output_folder='report',
    remove_if_exists=True,
    format='html'
)
```

## 完整分析管道

```python
import spikeinterface.full as si

def analyze_sorting(recording, sorting, output_dir):
    """Complete post-processing pipeline."""

    # Create analyzer
    analyzer = si.create_sorting_analyzer(
        sorting, recording,
        sparse=True,
        folder=f'{output_dir}/analyzer'
    )

    # Compute all extensions
    print("Computing extensions...")
    analyzer.compute(['random_spikes', 'waveforms', 'templates', 'noise_levels'])
    analyzer.compute(['principal_components', 'spike_amplitudes'])
    analyzer.compute(['correlograms', 'unit_locations', 'template_similarity'])
    analyzer.compute('quality_metrics')

    # Get quality metrics
    qm = analyzer.get_extension('quality_metrics').get_data()

    # Filter good units
    good_units = qm.query(
        "(snr > 5) & (isi_violations_ratio < 0.01) & (presence_ratio > 0.9)"
    ).index.tolist()

    print(f"Quality filtering: {len(good_units)}/{len(qm)} units passed")

    # Export
    si.export_to_phy(analyzer, f'{output_dir}/phy')
    si.export_report(analyzer, f'{output_dir}/report')

    # Save metrics
    qm.to_csv(f'{output_dir}/quality_metrics.csv')

    return analyzer, qm, good_units

# Usage
analyzer, qm, good_units = analyze_sorting(recording, sorting, 'output/')
```
