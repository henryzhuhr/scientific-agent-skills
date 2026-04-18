# 文件 I/O 和数据格式

## 概述

PyOpenMS 支持多种质谱文件格式的读写。本指南涵盖文件处理策略和特定于格式的操作。

## 支持的格式

### 质谱数据格式

- **mzML**：基于标准 XML 的质谱数据格式
- **mzXML**：早期基于 XML 的格式
- **mzData**：XML 格式（已弃用，但已弃用）支持）

### 标识格式

- **idXML**：OpenMS 本机标识格式
- **mzIdentML**：标识数据的标准 XML 格式
- **pepXML**：X！串联格式
- **protXML**：蛋白质识别格式

### 特征和定量格式

- **featureXML**：检测到的特征的OpenMS 格式
- **consensusXML**：跨样本的共有特征的格式
- **mzTab**：制表符分隔的格式报告

### 序列和文库格式

- **FASTA**：蛋白质/肽序列
- **TraML**：目标实验的转换列表

## 读取mzML 文件

### 内存加载

将整个文件加载到内存中（适合较小的文件）文件）：

```python
import pyopenms as ms

# Create experiment container
exp = ms.MSExperiment()

# Load file
ms.MzMLFile().load("sample.mzML", exp)

# Access data
print(f"Spectra: {exp.getNrSpectra()}")
print(f"Chromatograms: {exp.getNrChromatograms()}")
```

### 索引访问

E 大文件的高效随机访问：

```python
# Create indexed access
indexed_mzml = ms.IndexedMzMLFileLoader()
indexed_mzml.load("large_file.mzML")

# Get specific spectrum by index
spec = indexed_mzml.getSpectrumById(100)

# Access by native ID
spec = indexed_mzml.getSpectrumByNativeId("scan=5000")
```

### 流式访问

非常大的内存高效处理文件：

```python
# Define consumer function
class SpectrumProcessor(ms.MSExperimentConsumer):
    def __init__(self):
        super().__init__()
        self.count = 0

    def consumeSpectrum(self, spec):
        # Process spectrum
        if spec.getMSLevel() == 2:
            self.count += 1

# Stream file
consumer = SpectrumProcessor()
ms.MzMLFile().transform("large.mzML", consumer)
print(f"Processed {consumer.count} MS2 spectra")
```

### 缓存访问

内存使用和速度之间的平衡：

```python
# Use on-disk caching
options = ms.CachedmzML()
options.setMetaDataOnly(False)

exp = ms.MSExperiment()
ms.CachedmzMLHandler().load("sample.mzML", exp, options)
```

## 写入mzML文件

### 基本写入

```python
# Create or modify experiment
exp = ms.MSExperiment()
# ... add spectra ...

# Write to file
ms.MzMLFile().store("output.mzML", exp)
```

### 压缩选项

```python
# Configure compression
file_handler = ms.MzMLFile()

options = ms.PeakFileOptions()
options.setCompression(True)  # Enable compression
file_handler.setOptions(options)

file_handler.store("compressed.mzML", exp)
```

## 读取标识数据

### idXML格式

```python
# Load identification results
protein_ids = []
peptide_ids = []

ms.IdXMLFile().load("identifications.idXML", protein_ids, peptide_ids)

# Access peptide identifications
for peptide_id in peptide_ids:
    print(f"RT: {peptide_id.getRT()}")
    print(f"MZ: {peptide_id.getMZ()}")

    # Get peptide hits
    for hit in peptide_id.getHits():
        print(f"  Sequence: {hit.getSequence().toString()}")
        print(f"  Score: {hit.getScore()}")
        print(f"  Charge: {hit.getCharge()}")
```

### mzIdentML格式

```python
# Read mzIdentML
protein_ids = []
peptide_ids = []

ms.MzIdentMLFile().load("results.mzid", protein_ids, peptide_ids)
```

### pepXML 格式

```python
# Load pepXML
protein_ids = []
peptide_ids = []

ms.PepXMLFile().load("results.pep.xml", protein_ids, peptide_ids)
```

## 读取特征数据

### featureXML

```python
# Load features
feature_map = ms.FeatureMap()
ms.FeatureXMLFile().load("features.featureXML", feature_map)

# Access features
for feature in feature_map:
    print(f"RT: {feature.getRT()}")
    print(f"MZ: {feature.getMZ()}")
    print(f"Intensity: {feature.getIntensity()}")
    print(f"Quality: {feature.getOverallQuality()}")
```

### 共识XML

```python
# Load consensus features
consensus_map = ms.ConsensusMap()
ms.ConsensusXMLFile().load("consensus.consensusXML", consensus_map)

# Access consensus features
for consensus_feature in consensus_map:
    print(f"RT: {consensus_feature.getRT()}")
    print(f"MZ: {consensus_feature.getMZ()}")

    # Get feature handles (sub-features from different maps)
    for handle in consensus_feature.getFeatureList():
        map_index = handle.getMapIndex()
        intensity = handle.getIntensity()
        print(f"  Map {map_index}: {intensity}")
```

## 读取FASTA文件

```python
# Load protein sequences
fasta_entries = []
ms.FASTAFile().load("database.fasta", fasta_entries)

for entry in fasta_entries:
    print(f"Identifier: {entry.identifier}")
    print(f"Description: {entry.description}")
    print(f"Sequence: {entry.sequence}")
```

## 读取TraML文件

```python
# Load transition lists for targeted experiments
targeted_exp = ms.TargetedExperiment()
ms.TraMLFile().load("transitions.TraML", targeted_exp)

# Access transitions
for transition in targeted_exp.getTransitions():
    print(f"Precursor MZ: {transition.getPrecursorMZ()}")
    print(f"Product MZ: {transition.getProductMZ()}")
```

## 写入mzTab文件

```python
# Create mzTab for reporting
mztab = ms.MzTab()

# Add metadata
metadata = mztab.getMetaData()
metadata.mz_tab_version.set("1.0.0")
metadata.title.set("Proteomics Analysis Results")

# Add protein data
protein_section = mztab.getProteinSectionRows()
# ... populate protein data ...

# Write to file
ms.MzTabFile().store("report.mzTab", mztab)
```

## 格式转换

### mzXML 到 mzML

```python
# Read mzXML
exp = ms.MSExperiment()
ms.MzXMLFile().load("data.mzXML", exp)

# Write as mzML
ms.MzMLFile().store("data.mzML", exp)
```

### 从 mzML

```python
# Load experiment
exp = ms.MSExperiment()
ms.MzMLFile().load("data.mzML", exp)

# Extract specific chromatogram
for chrom in exp.getChromatograms():
    if chrom.getNativeID() == "TIC":
        rt, intensity = chrom.get_peaks()
        print(f"TIC has {len(rt)} data points")
```

## 文件元数据

### 访问 mzML 元数据

```python
# Load file
exp = ms.MSExperiment()
ms.MzMLFile().load("sample.mzML", exp)

# Get experimental settings
exp_settings = exp.getExperimentalSettings()

# Instrument info
instrument = exp_settings.getInstrument()
print(f"Instrument: {instrument.getName()}")
print(f"Model: {instrument.getModel()}")

# Sample info
sample = exp_settings.getSample()
print(f"Sample name: {sample.getName()}")

# Source files
for source_file in exp_settings.getSourceFiles():
    print(f"Source: {source_file.getNameOfFile()}")
```

## 最佳实践

### 内存中提取色谱图管理

对于大文件：
1. 使用索引或流式访问而不是完全内存加载
2. 以块的形式处理数据
3. 不再需要时清除数据结构

```python
# Good for large files
indexed_mzml = ms.IndexedMzMLFileLoader()
indexed_mzml.load("huge_file.mzML")

# Process spectra one at a time
for i in range(indexed_mzml.getNrSpectra()):
    spec = indexed_mzml.getSpectrumById(i)
    # Process spectrum
    # Spectrum automatically cleaned up after processing
```

### 错误处理

```python
try:
    exp = ms.MSExperiment()
    ms.MzMLFile().load("data.mzML", exp)
except Exception as e:
    print(f"Failed to load file: {e}")
```

### 文件验证

```python
# Check if file exists and is readable
import os

if os.path.exists("data.mzML") and os.path.isfile("data.mzML"):
    exp = ms.MSExperiment()
    ms.MzMLFile().load("data.mzML", exp)
else:
    print("File not found")
```
