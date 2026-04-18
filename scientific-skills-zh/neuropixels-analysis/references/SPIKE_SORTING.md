# Spike Sorting Reference

Spike Sorting Neuropixels 数据的综合指南。

## 可用排序器

|分拣机 |需要 GPU |速度|品质 |最适合 |
|--------|----------------|--------|---------|----------|
| **千排序4** |是（CUDA）|快|优秀|生产使用|
| **千排序3** |是（CUDA）|快|非常好 |旧版兼容性 |
| **Kilosort2.5** |是（CUDA）|快|好 |旧管道|
| **间谍马戏团2** |没有 |中等|好 |仅 CPU 系统 |
| **山排序5** |没有 |中等|好 |小录音|
| **特里斯克劳斯2** |没有 |中等|好 |交互式排序|

## Kilosort4（推荐）

### 安装
```bash
pip install kilosort
```

### 基本用法
```python
import spikeinterface.full as si

# Run Kilosort4
sorting = si.run_sorter(
    'kilosort4',
    recording,
    output_folder='ks4_output',
    verbose=True
)

print(f"Found {len(sorting.unit_ids)} units")
```

### 自定义参数
```python
sorting = si.run_sorter(
    'kilosort4',
    recording,
    output_folder='ks4_output',
    # Detection
    Th_universal=9,        # Spike detection threshold
    Th_learned=8,          # Learned threshold
    # Templates
    dmin=15,               # Min vertical distance between templates (um)
    dminx=12,              # Min horizontal distance (um)
    nblocks=5,             # Number of non-rigid blocks
    # Clustering
    max_channel_distance=None,  # Max distance for template channel
    # Output
    do_CAR=False,          # Skip CAR (done in preprocessing)
    skip_kilosort_preprocessing=True,
    save_extra_kwargs=True
)
```

### Kilosort4完整参数
```python
# Get all available parameters
params = si.get_default_sorter_params('kilosort4')
print(params)

# Key parameters:
ks4_params = {
    # Detection
    'Th_universal': 9,      # Universal threshold for spike detection
    'Th_learned': 8,        # Threshold for learned templates
    'spkTh': -6,            # Spike threshold during extraction

    # Clustering
    'dmin': 15,             # Min distance between clusters (um)
    'dminx': 12,            # Min horizontal distance (um)
    'nblocks': 5,           # Blocks for non-rigid drift correction

    # Templates
    'n_templates': 6,       # Number of universal templates per group
    'nt': 61,               # Number of time samples in template

    # Performance
    'batch_size': 60000,    # Batch size in samples
    'nfilt_factor': 8,      # Factor for number of filters
}
```

## Kilosort3

### 用法
```python
sorting = si.run_sorter(
    'kilosort3',
    recording,
    output_folder='ks3_output',
    # Key parameters
    detect_threshold=6,
    projection_threshold=[9, 9],
    preclust_threshold=8,
    car=False,  # CAR done in preprocessing
    freq_min=300,
)
```

## SpykingCircus2 （仅CPU）

### 安装
```bash
pip install spykingcircus
```

### 使用
```python
sorting = si.run_sorter(
    'spykingcircus2',
    recording,
    output_folder='sc2_output',
    # Parameters
    detect_threshold=5,
    selection_method='all',
)
```

## Mountainsort5（仅CPU）

### 安装
```bash
pip install mountainsort5
```

### 用法
```python
sorting = si.run_sorter(
    'mountainsort5',
    recording,
    output_folder='ms5_output',
    # Parameters
    detect_threshold=5.0,
    scheme='2',  # '1', '2', or '3'
)
```

## 运行多个排序器

### 比较排序器
```python
# Run multiple sorters
sorting_ks4 = si.run_sorter('kilosort4', recording, output_folder='ks4/')
sorting_sc2 = si.run_sorter('spykingcircus2', recording, output_folder='sc2/')
sorting_ms5 = si.run_sorter('mountainsort5', recording, output_folder='ms5/')

# Compare results
comparison = si.compare_multiple_sorters(
    [sorting_ks4, sorting_sc2, sorting_ms5],
    name_list=['KS4', 'SC2', 'MS5']
)

# Get agreement scores
agreement = comparison.get_agreement_sorting()
```

### Ensemble排序
```python
# Create consensus sorting
sorting_ensemble = si.create_ensemble_sorting(
    [sorting_ks4, sorting_sc2, sorting_ms5],
    voting_method='agreement',
    min_agreement=2  # Unit must be found by at least 2 sorters
)
```

## 在Docker/Singularity中排序

### 使用Docker
```python
sorting = si.run_sorter(
    'kilosort3',
    recording,
    output_folder='ks3_docker/',
    docker_image='spikeinterface/kilosort3-compiled-base:latest',
    verbose=True
)
```

### 使用Singularity
```python
sorting = si.run_sorter(
    'kilosort3',
    recording,
    output_folder='ks3_singularity/',
    singularity_image='/path/to/kilosort3.sif',
    verbose=True
)
```

## 长录音策略

### 连接录音
```python
# Multiple recording files
recordings = [
    si.read_spikeglx(f'/path/to/recording_{i}', stream_id='imec0.ap')
    for i in range(3)
]

# Concatenate
recording_concat = si.concatenate_recordings(recordings)

# Sort
sorting = si.run_sorter('kilosort4', recording_concat, output_folder='ks4/')

# Split back by original recording
sortings_split = si.split_sorting(sorting, recording_concat)
```

### 按片段排序
```python
# For very long recordings, sort segments separately
from pathlib import Path

segments_output = Path('sorting_segments')
sortings = []

for i, segment in enumerate(recording.split_by_times([0, 3600, 7200, 10800])):
    sorting_seg = si.run_sorter(
        'kilosort4',
        segment,
        output_folder=segments_output / f'segment_{i}'
    )
    sortings.append(sorting_seg)
```

## 排序后管理

### 手动管理Phy
```python
# Export to Phy format
analyzer = si.create_sorting_analyzer(sorting, recording)
analyzer.compute(['random_spikes', 'waveforms', 'templates'])
si.export_to_phy(analyzer, output_folder='phy_export/')

# Open Phy
# Run in terminal: phy template-gui phy_export/params.py
```

### 加载 Phy Curation
```python
# After manual curation in Phy
sorting_curated = si.read_phy('phy_export/')

# Or apply Phy labels
sorting_curated = si.apply_phy_curation(sorting, 'phy_export/')
```

### 自动管理
```python
# Remove units below quality threshold
analyzer = si.create_sorting_analyzer(sorting, recording)
analyzer.compute('quality_metrics')

qm = analyzer.get_extension('quality_metrics').get_data()

# Define quality criteria
query = "(snr > 5) & (isi_violations_ratio < 0.01) & (presence_ratio > 0.9)"
good_unit_ids = qm.query(query).index.tolist()

sorting_clean = sorting.select_units(good_unit_ids)
print(f"Kept {len(good_unit_ids)}/{len(sorting.unit_ids)} units")
```

## 排序指标

### 检查排序器输出
```python
# Basic stats
print(f"Units found: {len(sorting.unit_ids)}")
print(f"Total spikes: {sorting.get_total_num_spikes()}")

# Per-unit spike counts
for unit_id in sorting.unit_ids[:10]:
    n_spikes = len(sorting.get_unit_spike_train(unit_id))
    print(f"Unit {unit_id}: {n_spikes} spikes")
```

### 发射率
```python
# Compute firing rates
duration = recording.get_total_duration()
for unit_id in sorting.unit_ids:
    n_spikes = len(sorting.get_unit_spike_train(unit_id))
    fr = n_spikes / duration
    print(f"Unit {unit_id}: {fr:.2f} Hz")
```

## 故障排除

### 常见问题

* *GPU 之外内存**
```python
# Reduce batch size
sorting = si.run_sorter(
    'kilosort4',
    recording,
    output_folder='ks4/',
    batch_size=30000  # Smaller batch
)
```

* *找到的单元太少**
```python
# Lower detection threshold
sorting = si.run_sorter(
    'kilosort4',
    recording,
    output_folder='ks4/',
    Th_universal=7,  # Lower from default 9
    Th_learned=6
)
```

* *单元太多（过度分割）**
```python
# Increase minimum distance between templates
sorting = si.run_sorter(
    'kilosort4',
    recording,
    output_folder='ks4/',
    dmin=20,   # Increase from 15
    dminx=16   # Increase from 12
)
```

* *检查GPU可用性**
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0)}")
```
