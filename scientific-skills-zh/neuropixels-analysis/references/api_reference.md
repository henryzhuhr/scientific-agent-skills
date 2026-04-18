# API参考

按模块组织的neuropixels_analysis函数的快速参考。

## 核心模块

### load_recording

```python
npa.load_recording(
    path: str,
    format: str = 'auto',  # 'spikeglx', 'openephys', 'nwb'
    stream_id: str = None,  # e.g., 'imec0.ap'
) -> Recording
```

从各种格式加载神经像素记录。

### run_pipeline

```python
npa.run_pipeline(
    recording: Recording,
    output_dir: str,
    sorter: str = 'kilosort4',
    preprocess: bool = True,
    correct_motion: bool = True,
    postprocess: bool = True,
    curate: bool = True,
    curation_method: str = 'allen',
) -> dict
```

运行完整的分析管道。返回包含所有结果的字典。

## 预处理模块

### preprocess

```python
npa.preprocess(
    recording: Recording,
    freq_min: float = 300,
    freq_max: float = 6000,
    phase_shift: bool = True,
    common_ref: bool = True,
    bad_channel_detection: bool = True,
) -> Recording
```

应用标准预处理链。

### detector_bad_channels

```python
npa.detect_bad_channels(
    recording: Recording,
    method: str = 'coherence+psd',
    **kwargs,
) -> list
```

检测并返回不良通道列表IDs.

### apply_filters

```python
npa.apply_filters(
    recording: Recording,
    freq_min: float = 300,
    freq_max: float = 6000,
    filter_type: str = 'bandpass',
) -> Recording
```

应用频率滤波器。

### common_reference

```python
npa.common_reference(
    recording: Recording,
    operator: str = 'median',
    reference: str = 'global',
) -> Recording
```

应用公共参考(CMR/CAR)。

## 运动模块

### check_drift

```python
npa.check_drift(
    recording: Recording,
    plot: bool = True,
    output: str = None,
) -> dict
```

检查记录是否有漂移。返回漂移统计数据。

### estimate_motion

```python
npa.estimate_motion(
    recording: Recording,
    preset: str = 'kilosort_like',
    **kwargs,
) -> dict
```

E估计运动而不应用校正。

### Correct_motion

```python
npa.correct_motion(
    recording: Recording,
    preset: str = 'nonrigid_accurate',
    folder: str = None,
    **kwargs,
) -> Recording
```

应用运动

* *预设：**
- `'kilosort_like'`：快速、刚性校正
- `'nonrigid_accurate'`：较慢，更适合严重漂移
- `'nonrigid_fast_and_accurate'`：平衡选项

## 排序模块

### run_sorting

```python
npa.run_sorting(
    recording: Recording,
    sorter: str = 'kilosort4',
    output_folder: str = None,
    sorter_params: dict = None,
    **kwargs,
) -> Sorting
```

运行尖峰排序器。

* *支持的排序器：**
- `'kilosort4'`：基于GPU，推荐
- `'kilosort3'`：传统，需要MATLAB
- `'spykingcircus2'`：基于CPU的替代方案
- `'mountainsort5'`：快速，适合短时间录音

### compare_sorters

```python
npa.compare_sorters(
    sortings: list,
    delta_time: float = 0.4,  # ms
    match_score: float = 0.5,
) -> Comparison
```

比较多个排序器的结果。

## 后处理模块

### create_analyzer

```python
npa.create_analyzer(
    sorting: Sorting,
    recording: Recording,
    output_folder: str = None,
    sparse: bool = True,
) -> SortingAnalyzer
```

创建用于后处理的SortingAnalyzer。

### postprocess

```python
npa.postprocess(
    sorting: Sorting,
    recording: Recording,
    output_folder: str = None,
    compute_all: bool = True,
    n_jobs: int = -1,
) -> tuple[SortingAnalyzer, DataFrame]
```

完整后处理。返回（分析器，指标）。

### compute_quality_metrics

```python
npa.compute_quality_metrics(
    analyzer: SortingAnalyzer,
    metric_names: list = None,  # None = all
    **kwargs,
) -> DataFrame
```

计算所有单位的质量指标。

* *可用指标：**
- `snr`：信噪比
- `isi_violations_ratio`：ISI违规
- `presence_ratio`：记录存在
- `amplitude_cutoff`：幅度分布截止
- `firing_rate`：平均发射率
- `amplitude_cv`：振幅变异系数
- `sliding_rp_violation`：滑动窗难熔违规
- `d_prime`：隔离质量
- `nearest_neighbor`：最近邻重叠

## 管理模块

### curate

```python
npa.curate(
    metrics: DataFrame,
    method: str = 'allen',  # 'allen', 'ibl', 'strict', 'custom'
    **thresholds,
) -> dict
```

应用自动管理。返回 {unit_id: label}。

### auto_classify

```python
npa.auto_classify(
    metrics: DataFrame,
    snr_threshold: float = 5.0,
    isi_threshold: float = 0.01,
    presence_threshold: float = 0.9,
) -> dict
```

根据自定义阈值对单位进行分类。

### filter_units

```python
npa.filter_units(
    sorting: Sorting,
    labels: dict,
    keep: list = ['good'],
) -> Sorting
```

过滤排序以仅保留指定的labels.

## AI Curation Module

### generate_unit_report

```python
npa.generate_unit_report(
    analyzer: SortingAnalyzer,
    unit_id: int,
    output_dir: str = None,
    figsize: tuple = (16, 12),
) -> dict
```

生成用于AI分析的可视化报告。

返回：
- `'image_path'`：保存图形的路径
- `'image_base64'`：Base64 编码图像
- `'metrics'`：质量指标 dict
- `'unit_id'`：单元 ID

### analyze_unit_visually

```python
npa.analyze_unit_visually(
    analyzer: SortingAnalyzer,
    unit_id: int,
    api_client: Any = None,
    model: str = 'claude-opus-4.5',
    task: str = 'quality_assessment',
    custom_prompt: str = None,
) -> dict
```

 使用视觉语言分析单元model.

* *任务：**
- `'quality_assessment'`：分类为好/mua/噪音
- `'merge_candidate'`：检查单位是否应该合并
- `'drift_assessment'`：评估运动/漂移

### batch_visual_curation

```python
npa.batch_visual_curation(
    analyzer: SortingAnalyzer,
    unit_ids: list = None,
    api_client: Any = None,
    model: str = 'claude-opus-4.5',
    output_dir: str = None,
    progress_callback: callable = None,
) -> dict
```

在多个单元上运行视觉管理。

### CurationSession

```python
session = npa.CurationSession.create(
    analyzer: SortingAnalyzer,
    output_dir: str,
    session_id: str = None,
    unit_ids: list = None,
    sort_by_confidence: bool = True,
)

# Navigation
session.current_unit() -> UnitCuration
session.next_unit() -> UnitCuration
session.prev_unit() -> UnitCuration
session.go_to_unit(unit_id: int) -> UnitCuration

# Decisions
session.set_decision(unit_id, decision, notes='')
session.set_ai_classification(unit_id, classification)

# Export
session.get_final_labels() -> dict
session.export_decisions(output_path) -> DataFrame
session.get_summary() -> dict

# Persistence
session.save()
session = npa.CurationSession.load(session_dir)
```

## 可视化模块

### plot_drift

```python
npa.plot_drift(
    recording: Recording,
    motion: dict = None,
    output: str = None,
    figsize: tuple = (12, 8),
)
```

绘制漂移/运动图。

### plot_quality_metrics

```python
npa.plot_quality_metrics(
    analyzer: SortingAnalyzer,
    metrics: DataFrame = None,
    output: str = None,
)
```

绘制质量指标概述。

### plot_unit_summary

```python
npa.plot_unit_summary(
    analyzer: SortingAnalyzer,
    unit_id: int,
    output: str = None,
)
```

绘制综合单元摘要。

## SpikeInterface集成

所有neuropixels_analysis函数都与SpikeInterface对象一起使用：

```python
import spikeinterface.full as si
import neuropixels_analysis as npa

# SpikeInterface recording works with npa functions
recording = si.read_spikeglx('/path/')
rec = npa.preprocess(recording)

# Access SpikeInterface directly for advanced usage
rec_filtered = si.bandpass_filter(recording, freq_min=300, freq_max=6000)
```

## 通用参数

### 录制参数
- `freq_min`：高通截止 (Hz)
- `freq_max`：低通截止 (Hz)
- `n_jobs`：并行作业（-1 = 所有内核）

### 排序参数
- `output_folder`：保存结果的位置
- `sorter_params`：排序器特定参数的字典

### 质量指标阈值
- `snr_threshold`：SNR截止（通常为5）
- `isi_threshold`：ISI 违规截止（通常为 0.01）
- `presence_threshold`：存在比截止（通常为 0.9）
