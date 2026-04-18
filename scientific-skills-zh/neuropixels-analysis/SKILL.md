---
name: neuropixels-analysis
description: Neuropixels 神经记录分析。加载 SpikeGLX/OpenEphys 数据、预处理、运动校正、Kilosort4 尖峰排序、质量指标、Allen/IBL 管理、AI 辅助视觉分析，适用于 Neuropixels 1.0/2.0 细胞外电生理学。当处理神经记录、尖峰排序、细胞外电生理学时，或者当用户提到 Neuropixels、SpikeGLX、Open Ephys、Kilosort、质量指标或单位管理时使用。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Neuropixels 数据分析

## 概述

使用 SpikeInterface、艾伦研究所和国际脑实验室 (IBL)的当前最佳实践来分析 Neuropixels 高密度神经记录的综合工具包。支持从原始数据到可发布的精选单元的完整工作流程。

## 何时使用此技能

此技能应在以下情况下使用：
- 使用 Neuropixels 记录（.ap.bin、.lf.bin、.meta 文件）
- 从 SpikeGLX、Open Ephys 或 NWB 格式加载数据
- 预处理神经记录（过滤、CAR、坏通道检测）
- 检测和纠正记录中的运动/漂移
- 运行尖峰排序（Kilosort4、SpykingCircus2、Mountainsort5）
- 计算质量指标（SNR、ISI 违规、存在比）
- 使用 Allen/IBL 管理单元标准
- 创建神经数据的可视化
- 将结果导出到Phy 或NWB

## 支持的硬件和格式

|探针|电极|频道 | Notes |
|-------|-----------|----------|-------|
|神经像素1.0 | 960 | 960 384 | 384需要相移校正|
| Neuropixels 2.0（单）| 1280 | 1280 384 | 384更密集的几何形状|
| Neuropixels 2.0（4 柄）| 5120| 384 | 384多区域录音|

|格式|扩展| Reader |
|--------|-----------|--------|
|斯派克GLX | `.ap.bin`、`.lf.bin`、`.meta` | `si.read_spikeglx()` |
|打开 Ephys | `.continuous`、`.oebin` | `si.read_openephys()` |
|新世界银行 | `.nwb` | `si.read_nwb()` |

## 快速入门

### 基本导入和设置

```python
import spikeinterface.full as si
import neuropixels_analysis as npa

# Configure parallel processing
job_kwargs = dict(n_jobs=-1, chunk_duration='1s', progress_bar=True)
```

### 加载数据

```python
# SpikeGLX (most common)
recording = si.read_spikeglx('/path/to/data', stream_id='imec0.ap')

# Open Ephys (common for many labs)
recording = si.read_openephys('/path/to/Record_Node_101/')

# Check available streams
streams, ids = si.get_neo_streams('spikeglx', '/path/to/data')
print(streams)  # ['imec0.ap', 'imec0.lf', 'nidq']

# For testing with subset of data
recording = recording.frame_slice(0, int(60 * recording.get_sampling_frequency()))
```

### 完整管道（一）命令）

```python
# Run full analysis pipeline
results = npa.run_pipeline(
    recording,
    output_dir='output/',
    sorter='kilosort4',
    curation_method='allen',
)

# Access results
sorting = results['sorting']
metrics = results['metrics']
labels = results['labels']
```

## 标准分析工作流程

### 1. 预处理

```python
# Recommended preprocessing chain
rec = si.highpass_filter(recording, freq_min=400)
rec = si.phase_shift(rec)  # Required for Neuropixels 1.0
bad_ids, _ = si.detect_bad_channels(rec)
rec = rec.remove_channels(bad_ids)
rec = si.common_reference(rec, operator='median')

# Or use our wrapper
rec = npa.preprocess(recording)
```

### 2. 检查并纠正漂移

```python
# Check for drift (always do this!)
motion_info = npa.estimate_motion(rec, preset='kilosort_like')
npa.plot_drift(rec, motion_info, output='drift_map.png')

# Apply correction if needed
if motion_info['motion'].max() > 10:  # microns
    rec = npa.correct_motion(rec, preset='nonrigid_accurate')
```

### 3. Spike Sorting

```python
# Kilosort4 (recommended, requires GPU)
sorting = si.run_sorter('kilosort4', rec, folder='ks4_output')

# CPU alternatives
sorting = si.run_sorter('tridesclous2', rec, folder='tdc2_output')
sorting = si.run_sorter('spykingcircus2', rec, folder='sc2_output')
sorting = si.run_sorter('mountainsort5', rec, folder='ms5_output')

# Check available sorters
print(si.installed_sorters())
```

### 4. Postprocessing

```python
# Create analyzer and compute all extensions
analyzer = si.create_sorting_analyzer(sorting, rec, sparse=True)

analyzer.compute('random_spikes', max_spikes_per_unit=500)
analyzer.compute('waveforms', ms_before=1.0, ms_after=2.0)
analyzer.compute('templates', operators=['average', 'std'])
analyzer.compute('spike_amplitudes')
analyzer.compute('correlograms', window_ms=50.0, bin_ms=1.0)
analyzer.compute('unit_locations', method='monopolar_triangulation')
analyzer.compute('quality_metrics')

metrics = analyzer.get_extension('quality_metrics').get_data()
```

### 5. Curation

```python
# Allen Institute criteria (conservative)
good_units = metrics.query("""
    presence_ratio > 0.9 and
    isi_violations_ratio < 0.5 and
    amplitude_cutoff < 0.1
""").index.tolist()

# Or use automated curation
labels = npa.curate(metrics, method='allen')  # 'allen', 'ibl', 'strict'
```

### 6. AI 辅助管理（针对不确定单位）

当将此技能与 Claude Code 结合使用时，Claude 可以直接分析波形图并提供专家管理决策。对于编程 API 访问：

```python
from anthropic import Anthropic

# Setup API client
client = Anthropic()

# Analyze uncertain units visually
uncertain = metrics.query('snr > 3 and snr < 8').index.tolist()

for unit_id in uncertain:
    result = npa.analyze_unit_visually(analyzer, unit_id, api_client=client)
    print(f"Unit {unit_id}: {result['classification']}")
    print(f"  Reasoning: {result['reasoning'][:100]}...")
```

* *Claude 代码集成**：在 Claude 代码中运行时，要求 Claude 直接检查波形/相关图 - 无需 API 设置。

### 7. 生成分析报告

```python
# Generate comprehensive HTML report with visualizations
report_dir = npa.generate_analysis_report(results, 'output/')
# Opens report.html with summary stats, figures, and unit table

# Print formatted summary to console
npa.print_analysis_summary(results)
```

### 8. 导出结果

```python
# Export to Phy for manual review
si.export_to_phy(analyzer, output_folder='phy_export/',
                 compute_pc_features=True, compute_amplitudes=True)

# Export to NWB
from spikeinterface.exporters import export_to_nwb
export_to_nwb(rec, sorting, 'output.nwb')

# Save quality metrics
metrics.to_csv('quality_metrics.csv')
```

## 常见陷阱和最佳实践

1. **在尖峰分选之前始终检查漂移** - 漂移 > 10μm 会显着影响质量
2. **对 Neuropixels 1.0 探针使用phase_shift**（2.0 不需要）
3. **保存预处理数据**以避免重新计算 - 使用 `rec.save(folder='preprocessed/')`
4. **使用 GPU** Kilosort4 - 它比 CPU 替代品 
5 快 10-50 倍。 **手动审查不确定的单位** - 自动管理是一个起点
6. **将指标与人工智能相结合** - 对明确案例使用指标，对边界单元使用人工智能
7. **记录您的阈值** - 不同的分析可能需要不同的标准
8. **导出到 Phy** 对于关键实验 - 人工监督很有价值

## 调整的关键参数

### 预处理
- `freq_min`：高通截止（典型值 300-400 Hz）
- `detect_threshold`：坏通道检测灵敏度

### 运动修正
- `preset`：“kilosort_like”（快速）或“nonrigid_accurate”（对于严重漂移更好）

### Spike Sorting（Kilosort4）
- `batch_size`：每批样本（默认30000）
- `nblocks`：漂移块数量（长记录时增加）
- `Th_learned`：检测阈值（较低 = 更多尖峰）

### 质量指标
- `snr_threshold`：信噪比截止（典型值为 3-5）
- `isi_violations_ratio`：耐火违规（0.01-0.5）
- `presence_ratio`：记录覆盖范围（0.5-0.95）

## 捆绑资源

### scripts/preprocess_recording.py
自动预处理脚本：
```bash
python scripts/preprocess_recording.py /path/to/data --output preprocessed/
```

### scripts/run_sorting.py
运行尖峰排序：
```bash
python scripts/run_sorting.py preprocessed/ --sorter kilosort4 --output sorting/
```

### 脚本/compute_metrics.py
计算质量指标并应用管理：
```bash
python scripts/compute_metrics.py sorting/ preprocessed/ --output metrics/ --curation allen
```

### 脚本/export_to_phy.py
导出到Phy进行手动管理：
```bash
python scripts/export_to_phy.py metrics/analyzer --output phy_export/
```

### assets/analysis_template.py
完整的分析模板。复制并自定义：
```bash
cp assets/analysis_template.py my_analysis.py
# Edit parameters and run
python my_analysis.py
```

### references/standard_workflow.md
详细的分步工作流程以及每个阶段的说明。

### references/api_reference.md
按模块组织的快速功能参考。

### references/plotting_guide.md
出版质量图形的综合可视化指南。

## 详细参考指南

|主题 |参考 |
|-------|-----------|
|完整的工作流程 | [参考文献/standard_workflow.md](参考文献/standard_workflow.md) |
| API参考| [参考文献/api_reference.md](参考文献/api_reference.md) |
|绘图指南 | [参考文献/plotting_guide.md](参考文献/plotting_guide.md) |
|预处理 | [参考文献/PREPROCESSING.md](参考文献/PREPROCESSING.md) |
|穗排序 | [参考文献/SPIKE_SORTING.md](参考文献/SPIKE_SORTING.md) |
|运动校正| [参考文献/MOTION_CORRECTION.md](参考文献/MOTION_CORRECTION.md) |
|质量指标| [参考文献/QUALITY_METRICS.md](参考文献/QUALITY_METRICS.md) |
|自动管理| [参考文献/AUTOMATED_CURATION.md](参考文献/AUTOMATED_CURATION.md) |
|人工智能辅助策展 | [参考文献/AI_CURATION.md](参考文献/AI_CURATION.md) |
|波形分析| [references/ANALYSIS.md](references/ANALYSIS.md) |

## 安装

```bash
# Core packages
pip install spikeinterface[full] probeinterface neo

# Spike sorters
pip install kilosort          # Kilosort4 (GPU required)
pip install spykingcircus     # SpykingCircus2 (CPU)
pip install mountainsort5     # Mountainsort5 (CPU)

# Our toolkit
pip install neuropixels-analysis

# Optional: AI curation
pip install anthropic

# Optional: IBL tools
pip install ibl-neuropixel ibllib
```

## 项目结构

```
project/
├── raw_data/
│   └── recording_g0/
│       └── recording_g0_imec0/
│           ├── recording_g0_t0.imec0.ap.bin
│           └── recording_g0_t0.imec0.ap.meta
├── preprocessed/           # Saved preprocessed recording
├── motion/                 # Motion estimation results
├── sorting_output/         # Spike sorter output
├── analyzer/               # SortingAnalyzer (waveforms, metrics)
├── phy_export/             # For manual curation
├── ai_curation/            # AI analysis reports
└── results/
    ├── quality_metrics.csv
    ├── curation_labels.json
    └── output.nwb
```

## 其他资源

- **SpikeInterface 文档**：https://spikeinterface.readthedocs.io/
- **Neuropixels 教程**：https://spikeinterface.readthedocs.io/en/stable/how_to/analyze_neuropixels.html
- **Kilosort4 GitHub**：https://github.com/MouseLand/Kilosort
- **IBL Neuropixel 工具**：https://github.com/int-brain-lab/ibl-neuropixel
- **Allen Institute ecephys**：https://github.com/AllenInstitute/ecephys_spike_sorting
- **Bombcell（自动 QC）**：https://github.com/Julie-Fabre/bombcell
- **SpikeAgent （人工智能策展）**：https://github.com/SpikeAgent/SpikeAgent
