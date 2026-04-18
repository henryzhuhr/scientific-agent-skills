# 信号处理

## 概述

PyOpenMS 提供处理原始质谱数据的算法，包括平滑、滤波、取峰、质心、归一化和反卷积。

## 算法模式

大多数信号处理算法遵循标准模式：

```python
import pyopenms as ms

# 1. Create algorithm instance
algo = ms.AlgorithmName()

# 2. Get and modify parameters
params = algo.getParameters()
params.setValue("parameter_name", value)
algo.setParameters(params)

# 3. Apply to data
algo.filterExperiment(exp)  # or filterSpectrum(spec)
```

## 平滑

### 高斯滤波器

应用高斯平滑来降低噪声：

```python
# Create Gaussian filter
gaussian = ms.GaussFilter()

# Configure parameters
params = gaussian.getParameters()
params.setValue("gaussian_width", 0.2)  # Width in m/z or RT units
params.setValue("ppm_tolerance", 10.0)  # For m/z dimension
params.setValue("use_ppm_tolerance", "true")
gaussian.setParameters(params)

# Apply to experiment
gaussian.filterExperiment(exp)

# Or apply to single spectrum
spec = exp.getSpectrum(0)
gaussian.filterSpectrum(spec)
```

### Savitzky-Golay 滤波器

保留峰值的多项式平滑形状：

```python
# Create Savitzky-Golay filter
sg_filter = ms.SavitzkyGolayFilter()

# Configure parameters
params = sg_filter.getParameters()
params.setValue("frame_length", 11)  # Window size (must be odd)
params.setValue("polynomial_order", 4)  # Polynomial degree
sg_filter.setParameters(params)

# Apply smoothing
sg_filter.filterExperiment(exp)
```

## 峰值拾取和质心

### 峰值拾取器高分辨率

检测高分辨率数据中的峰值：

```python
# Create peak picker
peak_picker = ms.PeakPickerHiRes()

# Configure parameters
params = peak_picker.getParameters()
params.setValue("signal_to_noise", 3.0)  # S/N threshold
params.setValue("spacing_difference", 1.5)  # Minimum peak spacing
peak_picker.setParameters(params)

# Pick peaks
exp_picked = ms.MSExperiment()
peak_picker.pickExperiment(exp, exp_picked)
```

### CWT

Continuation 的峰值拾取器基于小波变换的峰值拾取：

```python
# Create CWT peak picker
cwt_picker = ms.PeakPickerCWT()

# Configure parameters
params = cwt_picker.getParameters()
params.setValue("signal_to_noise", 1.0)
params.setValue("peak_width", 0.15)  # Expected peak width
cwt_picker.setParameters(params)

# Pick peaks
cwt_picker.pickExperiment(exp, exp_picked)
```

## 归一化

### 归一化器

归一化光谱内的峰值强度：

```python
# Create normalizer
normalizer = ms.Normalizer()

# Configure normalization method
params = normalizer.getParameters()
params.setValue("method", "to_one")  # Options: "to_one", "to_TIC"
normalizer.setParameters(params)

# Apply normalization
normalizer.filterExperiment(exp)
```

## 峰值过滤

### 阈值Mower

删除低于强度阈值的峰值：

```python
# Create threshold filter
mower = ms.ThresholdMower()

# Configure threshold
params = mower.getParameters()
params.setValue("threshold", 1000.0)  # Absolute intensity threshold
mower.setParameters(params)

# Apply filter
mower.filterExperiment(exp)
```

### Window Mower

仅保留滑动窗口中的最高峰值：

```python
# Create window mower
window_mower = ms.WindowMower()

# Configure parameters
params = window_mower.getParameters()
params.setValue("windowsize", 50.0)  # Window size in m/z
params.setValue("peakcount", 2)  # Keep top N peaks per window
window_mower.setParameters(params)

# Apply filter
window_mower.filterExperiment(exp)
```

### N 个最大峰值

仅保留N 个最强烈的峰：

```python
# Create N largest filter
n_largest = ms.NLargest()

# Configure parameters
params = n_largest.getParameters()
params.setValue("n", 200)  # Keep 200 most intense peaks
n_largest.setParameters(params)

# Apply filter
n_largest.filterExperiment(exp)
```

## 基线降低

### 形态滤波器

使用形态操作删除基线：

```python
# Create morphological filter
morph_filter = ms.MorphologicalFilter()

# Configure parameters
params = morph_filter.getParameters()
params.setValue("struc_elem_length", 3.0)  # Structuring element size
params.setValue("method", "tophat")  # Method: "tophat", "bothat", "erosion", "dilation"
morph_filter.setParameters(params)

# Apply filter
morph_filter.filterExperiment(exp)
```

## 谱图合并

### 谱图合并

将多个光谱合并为一个：

```python
# Create merger
merger = ms.SpectraMerger()

# Configure parameters
params = merger.getParameters()
params.setValue("average_gaussian:spectrum_type", "profile")
params.setValue("average_gaussian:rt_FWHM", 5.0)  # RT window
merger.setParameters(params)

# Merge spectra
merger.mergeSpectraBlockWise(exp)
```

## 解卷积

### 电荷解卷积

确定电荷态并转换为中性质量：

```python
# Create feature deconvoluter
deconvoluter = ms.FeatureDeconvolution()

# Configure parameters
params = deconvoluter.getParameters()
params.setValue("charge_min", 1)
params.setValue("charge_max", 4)
params.setValue("potential_charge_states", "1,2,3,4")
deconvoluter.setParameters(params)

# Apply deconvolution
feature_map_out = ms.FeatureMap()
deconvoluter.compute(exp, feature_map, feature_map_out, ms.ConsensusMap())
```

### 同位素解卷积

删除同位素模式：

```python
# Create isotope wavelet transform
isotope_wavelet = ms.IsotopeWaveletTransform()

# Configure parameters
params = isotope_wavelet.getParameters()
params.setValue("max_charge", 3)
params.setValue("intensity_threshold", 10.0)
isotope_wavelet.setParameters(params)

# Apply transformation
isotope_wavelet.transform(exp)
```

## 保留时间对齐

### 图谱对齐

在多次运行中对齐保留时间：

```python
# Create map aligner
aligner = ms.MapAlignmentAlgorithmPoseClustering()

# Load multiple experiments
exp1 = ms.MSExperiment()
exp2 = ms.MSExperiment()
ms.MzMLFile().load("run1.mzML", exp1)
ms.MzMLFile().load("run2.mzML", exp2)

# Create reference
reference = ms.MSExperiment()

# Align experiments
transformations = []
aligner.align(exp1, exp2, transformations)

# Apply transformation
transformer = ms.MapAlignmentTransformer()
transformer.transformRetentionTimes(exp2, transformations[0])
```

## 质量校准

### 内部校准

使用已知参考质量校准质量轴：

```python
# Create internal calibration
calibration = ms.InternalCalibration()

# Set reference masses
reference_masses = [500.0, 1000.0, 1500.0]  # Known m/z values

# Calibrate
calibration.calibrate(exp, reference_masses)
```

## 质量控制

### 谱图统计

计算质量指标：

```python
# Get spectrum
spec = exp.getSpectrum(0)

# Calculate statistics
mz, intensity = spec.get_peaks()

# Total ion current
tic = sum(intensity)

# Base peak
base_peak_intensity = max(intensity)
base_peak_mz = mz[intensity.argmax()]

print(f"TIC: {tic}")
print(f"Base peak: {base_peak_mz} m/z at {base_peak_intensity}")
```

## 频谱预处理管道

### 完整预处理示例

```python
import pyopenms as ms

def preprocess_experiment(input_file, output_file):
    """Complete preprocessing pipeline."""

    # Load data
    exp = ms.MSExperiment()
    ms.MzMLFile().load(input_file, exp)

    # 1. Smooth with Gaussian filter
    gaussian = ms.GaussFilter()
    gaussian.filterExperiment(exp)

    # 2. Pick peaks
    picker = ms.PeakPickerHiRes()
    exp_picked = ms.MSExperiment()
    picker.pickExperiment(exp, exp_picked)

    # 3. Normalize intensities
    normalizer = ms.Normalizer()
    params = normalizer.getParameters()
    params.setValue("method", "to_TIC")
    normalizer.setParameters(params)
    normalizer.filterExperiment(exp_picked)

    # 4. Filter low-intensity peaks
    mower = ms.ThresholdMower()
    params = mower.getParameters()
    params.setValue("threshold", 10.0)
    mower.setParameters(params)
    mower.filterExperiment(exp_picked)

    # Save processed data
    ms.MzMLFile().store(output_file, exp_picked)

    return exp_picked

# Run pipeline
exp_processed = preprocess_experiment("raw_data.mzML", "processed_data.mzML")
```

## 最佳实践

### 参数优化

在代表性数据上测试参数：

```python
# Try different Gaussian widths
widths = [0.1, 0.2, 0.5]

for width in widths:
    exp_test = ms.MSExperiment()
    ms.MzMLFile().load("test_data.mzML", exp_test)

    gaussian = ms.GaussFilter()
    params = gaussian.getParameters()
    params.setValue("gaussian_width", width)
    gaussian.setParameters(params)
    gaussian.filterExperiment(exp_test)

    # Evaluate quality
    # ... add evaluation code ...
```

### 保留原始数据

保留原始数据比较：

```python
# Load original
exp_original = ms.MSExperiment()
ms.MzMLFile().load("data.mzML", exp_original)

# Create copy for processing
exp_processed = ms.MSExperiment(exp_original)

# Process copy
gaussian = ms.GaussFilter()
gaussian.filterExperiment(exp_processed)

# Original remains unchanged
```

### Profile vs Centroid Data

处理前检查数据类型：

```python
# Check if spectrum is centroided
spec = exp.getSpectrum(0)

if spec.isSorted():
    # Likely centroided
    print("Centroid data")
else:
    # Likely profile
    print("Profile data - apply peak picking")
```
