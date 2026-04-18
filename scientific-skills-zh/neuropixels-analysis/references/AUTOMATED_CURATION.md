# 自动管理参考

使用 Bombcell、UnitRefine 和其他工具进行自动尖峰排序管理的指南。

## 为什么自动管理？

手动管理是：
- **慢**：每次记录会话的小时数
- **主观**：评估者间变异性
- **不可再现**：难以标准化

自动化工具提供一致、可再现的质量分类。

## 可用工具

|工具|分类|语言 |集成|
|------|----------------|---------|--------------|
| **炸弹细胞** | 4 级（单/多/噪声/非体细胞）| Python/MATLAB | Spike接口，物理|
| **单位精炼** |基于机器学习 |蟒蛇 |尖峰接口|
| **SpikeInterface QM** |基于阈值的|蟒蛇 |原生|
| **单位匹配** |跨会话跟踪 | Python/MATLAB | Kilosort，Bombcell |

## Bombcell

### 概述

Bombcell 将单位分为 4 类：
1. **单个体细胞单位** - 隔离良好的单个神经元
2. **多单元活动 (MUA)** - 混合神经元信号
3. **噪声** - 非神经伪影
4. **非体细胞** - 轴突或树突信号

### 安装

```bash
# Python
pip install bombcell

# Or development version
git clone https://github.com/Julie-Fabre/bombcell.git
cd bombcell/py_bombcell
pip install -e .
```

### 基本用法 (Python)

```python
import bombcell as bc

# Load sorted data (Kilosort output)
kilosort_folder = '/path/to/kilosort/output'
raw_data_path = '/path/to/recording.ap.bin'

# Run Bombcell
results = bc.run_bombcell(
    kilosort_folder,
    raw_data_path,
    sample_rate=30000,
    n_channels=384
)

# Get classifications
unit_labels = results['unit_labels']
# 'good' = single unit, 'mua' = multi-unit, 'noise' = noise
```

### 与集成SpikeInterface

```python
import spikeinterface.full as si

# After spike sorting
sorting = si.run_sorter('kilosort4', recording, output_folder='ks4/')

# Create analyzer and compute required extensions
analyzer = si.create_sorting_analyzer(sorting, recording, sparse=True)
analyzer.compute('waveforms')
analyzer.compute('templates')
analyzer.compute('spike_amplitudes')

# Export to Phy format (Bombcell can read this)
si.export_to_phy(analyzer, output_folder='phy_export/')

# Run Bombcell on Phy export
import bombcell as bc
results = bc.run_bombcell_phy('phy_export/')
```

### Bombcell Metrics

Bombcell 计算分类的具体指标：

|公制|描述 |用于|
|--------|-------------|----------|
| `peak_trough_ratio` |波形形状|躯体与非躯体|
| `spatial_decay` |跨通道幅度 |噪音检测|
| `refractory_period_violations` | ISI 违规行为 |单与多|
| `presence_ratio` |时间稳定性 |单位质量|
| `waveform_duration` |峰谷时间|单元格类型 |

### 自定义阈值

```python
# Customize classification thresholds
custom_params = {
    'isi_threshold': 0.01,          # ISI violation threshold
    'presence_threshold': 0.9,       # Minimum presence ratio
    'amplitude_threshold': 20,       # Minimum amplitude (μV)
    'spatial_decay_threshold': 40,   # Spatial decay (μm)
}

results = bc.run_bombcell(
    kilosort_folder,
    raw_data_path,
    **custom_params
)
```

## SpikeInterface 自动管理

### 基于阈值的管理

```python
# Compute quality metrics
analyzer.compute('quality_metrics')
qm = analyzer.get_extension('quality_metrics').get_data()

# Define curation function
def auto_curate(qm):
    labels = {}
    for unit_id in qm.index:
        row = qm.loc[unit_id]

        # Classification logic
        if row['snr'] < 2 or row['presence_ratio'] < 0.5:
            labels[unit_id] = 'noise'
        elif row['isi_violations_ratio'] > 0.1:
            labels[unit_id] = 'mua'
        elif (row['snr'] > 5 and
              row['isi_violations_ratio'] < 0.01 and
              row['presence_ratio'] > 0.9):
            labels[unit_id] = 'good'
        else:
            labels[unit_id] = 'unsorted'

    return labels

unit_labels = auto_curate(qm)

# Filter by label
good_unit_ids = [u for u, l in unit_labels.items() if l == 'good']
sorting_curated = sorting.select_units(good_unit_ids)
```

### 使用 SpikeInterface 管理模块

```python
from spikeinterface.curation import (
    CurationSorting,
    MergeUnitsSorting,
    SplitUnitSorting
)

# Wrap sorting for curation
curation = CurationSorting(sorting)

# Remove noise units
noise_units = qm[qm['snr'] < 2].index.tolist()
curation.remove_units(noise_units)

# Merge similar units (based on template similarity)
analyzer.compute('template_similarity')
similarity = analyzer.get_extension('template_similarity').get_data()

# Find highly similar pairs
import numpy as np
threshold = 0.9
similar_pairs = np.argwhere(similarity > threshold)
# Merge pairs (careful - requires manual review)

# Get curated sorting
sorting_curated = curation.to_sorting()
```

## UnitMatch：跨会话跟踪

在记录日内跟踪相同的神经元。

### 安装

```bash
pip install unitmatch
# Or from source
git clone https://github.com/EnnyvanBeest/UnitMatch.git
```

### 用法

```python
# After running Bombcell on multiple sessions
session_folders = [
    '/path/to/session1/kilosort/',
    '/path/to/session2/kilosort/',
    '/path/to/session3/kilosort/',
]

from unitmatch import UnitMatch

# Run UnitMatch
um = UnitMatch(session_folders)
um.run()

# Get matching results
matches = um.get_matches()
# Returns DataFrame with unit IDs matched across sessions

# Assign unique IDs
unique_ids = um.get_unique_ids()
```

### 与集成工作流程

```python
# Typical workflow:
# 1. Spike sort each session
# 2. Run Bombcell for quality control
# 3. Run UnitMatch for cross-session tracking

# Session 1
sorting1 = si.run_sorter('kilosort4', rec1, output_folder='session1/ks4/')
# Run Bombcell
labels1 = bc.run_bombcell('session1/ks4/', raw1_path)

# Session 2
sorting2 = si.run_sorter('kilosort4', rec2, output_folder='session2/ks4/')
labels2 = bc.run_bombcell('session2/ks4/', raw2_path)

# Track units across sessions
um = UnitMatch(['session1/ks4/', 'session2/ks4/'])
matches = um.get_matches()
```

## 半自动化工作流程

结合自动和手动管理：

```python
# Step 1: Automated classification
analyzer.compute('quality_metrics')
qm = analyzer.get_extension('quality_metrics').get_data()

# Auto-label obvious cases
auto_labels = {}
for unit_id in qm.index:
    row = qm.loc[unit_id]
    if row['snr'] < 1.5:
        auto_labels[unit_id] = 'noise'
    elif row['snr'] > 8 and row['isi_violations_ratio'] < 0.005:
        auto_labels[unit_id] = 'good'
    else:
        auto_labels[unit_id] = 'needs_review'

# Step 2: Export uncertain units for manual review
needs_review = [u for u, l in auto_labels.items() if l == 'needs_review']

# Export only uncertain units to Phy
sorting_review = sorting.select_units(needs_review)
analyzer_review = si.create_sorting_analyzer(sorting_review, recording)
analyzer_review.compute('waveforms')
analyzer_review.compute('templates')
si.export_to_phy(analyzer_review, output_folder='phy_review/')

# Manual review in Phy: phy template-gui phy_review/params.py

# Step 3: Load manual labels and merge
manual_labels = si.read_phy('phy_review/').get_property('quality')
# Combine auto + manual labels for final result
```

## 方法比较

|方法|优点 |缺点 |
|--------|------|------|
| **手册（物理）** |黄金标准，灵活 |慢，主观|
| **SpikeInterface QM** |快速、可重复 |仅简单阈值|
| **炸弹细胞** |多类别、经过验证 |需要波形提取|
| **单位精炼** |基于机器学习，从数据中学习 |需要训练数据 |

## 最佳实践

1. **始终可视化** - 不要盲目相信自动化结果
2. **文档阈值** - 记录使用的确切参数
3. **验证** - 在子集
4 上比较自动与手动。 **保守一点** - 如有疑问，请排除单位 
5. **报告方法** - 在出版物中包含管理标准

## 管道示例

```python
def curate_sorting(sorting, recording, output_dir):
    """Complete curation pipeline."""

    # Create analyzer
    analyzer = si.create_sorting_analyzer(sorting, recording, sparse=True,
                                          folder=f'{output_dir}/analyzer')

    # Compute required extensions
    analyzer.compute('random_spikes', max_spikes_per_unit=500)
    analyzer.compute('waveforms')
    analyzer.compute('templates')
    analyzer.compute('noise_levels')
    analyzer.compute('spike_amplitudes')
    analyzer.compute('quality_metrics')

    qm = analyzer.get_extension('quality_metrics').get_data()

    # Auto-classify
    labels = {}
    for unit_id in qm.index:
        row = qm.loc[unit_id]

        if row['snr'] < 2:
            labels[unit_id] = 'noise'
        elif row['isi_violations_ratio'] > 0.1 or row['presence_ratio'] < 0.8:
            labels[unit_id] = 'mua'
        elif (row['snr'] > 5 and
              row['isi_violations_ratio'] < 0.01 and
              row['presence_ratio'] > 0.9 and
              row['amplitude_cutoff'] < 0.1):
            labels[unit_id] = 'good'
        else:
            labels[unit_id] = 'unsorted'

    # Summary
    from collections import Counter
    print("Classification summary:")
    print(Counter(labels.values()))

    # Save labels
    import json
    with open(f'{output_dir}/unit_labels.json', 'w') as f:
        json.dump(labels, f)

    # Return good units
    good_ids = [u for u, l in labels.items() if l == 'good']
    return sorting.select_units(good_ids), labels

# Usage
sorting_curated, labels = curate_sorting(sorting, recording, 'output/')
```

## 参考文献

- [Bombcell GitHub](https://github.com/Julie-Fabre/bombcell)
- [UnitMatch GitHub](https://github.com/EnnyvanBeest/UnitMatch)
- [SpikeInterface Curation](https://spikeinterface.readthedocs.io/en/stable/modules/curation.html)
- Fabre 等人。 (2023)“Bombcell：自动管理和细胞分类”
- van Beest 等人。 (2024)“UnitMatch：用高密度探针追踪神经元”
