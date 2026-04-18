# 运动/漂移校正参考

急性探针插入期间的机械漂移是 Neuropixels 记录的主要挑战。本指南涵盖了运动伪影的检测、估计和校正。

## 为什么运动校正很重要

- Neuropixels 探头在记录期间可以漂移 10-100+ μm
- 未校正的漂移导致：
  - 单位在记录中出现/消失
  - 波形幅度变化
  - 不正确的尖峰单元分配
  - 单位产量降低

## 检测：排序前检查

* *在运行尖峰排序之前始终可视化漂移！**

```python
import spikeinterface.full as si
from spikeinterface.sortingcomponents.peak_detection import detect_peaks
from spikeinterface.sortingcomponents.peak_localization import localize_peaks

# Preprocess first (don't whiten - affects peak localization)
rec = si.highpass_filter(recording, freq_min=400.)
rec = si.common_reference(rec, operator='median', reference='global')

# Detect peaks
noise_levels = si.get_noise_levels(rec, return_in_uV=False)
peaks = detect_peaks(
    rec,
    method='locally_exclusive',
    noise_levels=noise_levels,
    detect_threshold=5,
    radius_um=50.,
    n_jobs=8,
    chunk_duration='1s',
    progress_bar=True
)

# Localize peaks
peak_locations = localize_peaks(
    rec, peaks,
    method='center_of_mass',
    n_jobs=8,
    chunk_duration='1s'
)

# Visualize drift
si.plot_drift_raster_map(
    peaks=peaks,
    peak_locations=peak_locations,
    recording=rec,
    clim=(-200, 0)  # Adjust color limits
)
```

### 解释漂移图

|图案|解读|动作 |
|---------|----------------|--------|
|水平带，稳定|无明显漂移|跳过修正|
|对角带（慢）|逐渐沉降漂移|使用运动校正|
|快速跳跃|大脑脉动或运动|使用非刚性校正|
|混乱的图案|严重不稳定|考虑丢弃片段 |

## 运动校正方法

### 快速校正（建议开始）

```python
# Simple one-liner with preset
rec_corrected = si.correct_motion(
    recording=rec,
    preset='nonrigid_fast_and_accurate'
)
```

### 可用预设

|预设|速度|准确度|最适合|
|--------|--------|---------|----------|
| `rigid_fast` |快|低|快速检查，漂移小|
| `kilosort_like` |中等|好 | Kilosort 兼容结果 |
| `nonrigid_accurate` |慢|高|出版物品质|
| `nonrigid_fast_and_accurate` |中等|高| **推荐默认** |
| `dredge` |慢|最高|最佳结果，复杂漂移|
| `dredge_fast` |中等|高|计算量较少的 DREDge |

### 完全控制管道

```python
from spikeinterface.sortingcomponents.motion import (
    estimate_motion,
    interpolate_motion
)

# Step 1: Estimate motion
motion, temporal_bins, spatial_bins = estimate_motion(
    rec,
    peaks,
    peak_locations,
    method='decentralized',
    direction='y',
    rigid=False,          # Non-rigid for Neuropixels
    win_step_um=50,       # Spatial window step
    win_sigma_um=150,     # Spatial smoothing
    bin_s=2.0,            # Temporal bin size
    progress_bar=True
)

# Step 2: Visualize motion estimate
si.plot_motion(
    motion,
    temporal_bins,
    spatial_bins,
    recording=rec
)

# Step 3: Apply correction via interpolation
rec_corrected = interpolate_motion(
    recording=rec,
    motion=motion,
    temporal_bins=temporal_bins,
    spatial_bins=spatial_bins,
    border_mode='force_extrapolate'
)
```

### 保存运动估计

```python
# Save for later use
import numpy as np
np.savez('motion_estimate.npz',
         motion=motion,
         temporal_bins=temporal_bins,
         spatial_bins=spatial_bins)

# Load later
data = np.load('motion_estimate.npz')
motion = data['motion']
temporal_bins = data['temporal_bins']
spatial_bins = data['spatial_bins']
```

## DREDge：最先进的方法

DREDge（电生理学的分散注册） Data）是目前性能最好的运动校正方法。

### 使用DREDge Preset

```python
# AP-band motion estimation
rec_corrected = si.correct_motion(rec, preset='dredge')

# Or compute explicitly
motion, motion_info = si.compute_motion(
    rec,
    preset='dredge',
    output_motion_info=True,
    folder='motion_output/',
    **job_kwargs
)
```

### 基于 LFP 的运动估计

对于非常快的漂移或 AP 频段估计失败时：

```python
# Load LFP stream
lfp = si.read_spikeglx('/path/to/data', stream_name='imec0.lf')

# Estimate motion from LFP (faster, handles rapid drift)
motion_lfp, motion_info = si.compute_motion(
    lfp,
    preset='dredge_lfp',
    output_motion_info=True
)

# Apply to AP recording
rec_corrected = interpolate_motion(
    recording=rec,  # AP recording
    motion=motion_lfp,
    temporal_bins=motion_info['temporal_bins'],
    spatial_bins=motion_info['spatial_bins']
)
```

## 与尖峰排序集成

### 选项 1：预校正（推荐）

```python
# Correct before sorting
rec_corrected = si.correct_motion(rec, preset='nonrigid_fast_and_accurate')

# Save corrected recording
rec_corrected = rec_corrected.save(folder='preprocessed_motion_corrected/',
                                    format='binary', n_jobs=8)

# Run spike sorting on corrected data
sorting = si.run_sorter('kilosort4', rec_corrected, output_folder='ks4/')
```

### 选项 2：让 Kilosort 处理它

Kilosort 2.5+ 具有内置漂移校正：

```python
sorting = si.run_sorter(
    'kilosort4',
    rec,  # Not motion corrected
    output_folder='ks4/',
    nblocks=5,  # Non-rigid blocks for drift correction
    do_correction=True  # Enable Kilosort's drift correction
)
```

### 选项 3：事后校正

```python
# Sort first
sorting = si.run_sorter('kilosort4', rec, output_folder='ks4/')

# Then estimate motion from sorted spikes
# (More accurate as it uses actual spike times)
from spikeinterface.sortingcomponents.motion import estimate_motion_from_sorting

motion = estimate_motion_from_sorting(sorting, rec)
```

## 参数深入

### 峰值检测

```python
peaks = detect_peaks(
    rec,
    method='locally_exclusive',  # Best for dense probes
    noise_levels=noise_levels,
    detect_threshold=5,          # Lower = more peaks (noisier estimate)
    radius_um=50.,               # Exclusion radius
    exclude_sweep_ms=0.1,        # Temporal exclusion
)
```

### 运动估计

```python
motion = estimate_motion(
    rec, peaks, peak_locations,
    method='decentralized',      # 'decentralized' or 'iterative_template'
    direction='y',               # Along probe axis
    rigid=False,                 # False for non-rigid
    bin_s=2.0,                   # Temporal resolution (seconds)
    win_step_um=50,              # Spatial window step
    win_sigma_um=150,            # Spatial smoothing sigma
    margin_um=0,                 # Margin at probe edges
    win_scale_um=150,            # Window scale for weights
)
```

## 故障排除

### 校正过度（波浪图案）

```python
# Increase temporal smoothing
motion = estimate_motion(..., bin_s=5.0)  # Larger bins

# Or use rigid correction for small drift
motion = estimate_motion(..., rigid=True)
```

### 校正不足（仍存在漂移）

```python
# Decrease spatial window for finer non-rigid estimate
motion = estimate_motion(..., win_step_um=25, win_sigma_um=75)

# Use more peaks
peaks = detect_peaks(..., detect_threshold=4)  # Lower threshold
```

### 边缘工件

```python
rec_corrected = interpolate_motion(
    rec, motion, temporal_bins, spatial_bins,
    border_mode='force_extrapolate',  # or 'remove_channels'
    spatial_interpolation_method='kriging'
)
```

## 验证

校正后，重新可视化确认：

```python
# Re-detect peaks on corrected recording
peaks_corrected = detect_peaks(rec_corrected, ...)
peak_locations_corrected = localize_peaks(rec_corrected, peaks_corrected, ...)

# Plot before/after comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Before
si.plot_drift_raster_map(peaks, peak_locations, rec, ax=axes[0])
axes[0].set_title('Before Correction')

# After
si.plot_drift_raster_map(peaks_corrected, peak_locations_corrected,
                         rec_corrected, ax=axes[1])
axes[1].set_title('After Correction')
```

## 参考文献

- 【SpikeInterface运动校正文档](https://spikeinterface.readthedocs.io/en/stable/modules/motion_ Correction.html)
- [处理漂移教程](https://spikeinterface.readthedocs.io/en/stable/how_to/handle_drift.html)
- [DREDge GitHub](https://github.com/evarol/DREDge)
- Windolf 等人。 (2023)“DREDge：高密度细胞外记录的稳健运动校正”
