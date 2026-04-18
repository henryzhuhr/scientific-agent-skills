---
name: pyopenms
description: 完整的质谱分析平台。用于蛋白质组学工作流程，包括检测、肽鉴定、蛋白质定量和复杂的 LC-MS/MS 流程。支持广泛的文件格式和算法。最适合蛋白质组学、全面的 MS 数据处理。对于简单的光谱比较和代谢物 ID，请使用 matchms。
license: 3 clause BSD license
metadata:
    skill-author: K-Dense Inc.
---

# PyOpenMS

## 概述

PyOpenMS 提供与 OpenMS 库的 Python 绑定以进行计算质谱分析，从而能够分析蛋白质组学和代谢组学数据。用于处理质谱文件格式、处理光谱数据、检测特征、识别肽/蛋白质以及执行定量分析。

## 安装

使用uv安装：

```bash
uv uv pip install pyopenms
```

验证安装：

```python
import pyopenms
print(pyopenms.__version__)
```

## 核心功能

PyOpenMS 将功能组织到以下领域：

### 1. 文件 I/O 和数据格式

处理质谱文件格式并在表示形式之间进行转换。

* *支持的格式**：mzML、mzXML、TraML、mzTab、FASTA、pepXML、protXML、mzIdentML、 featureXML、consensusXML、idXML

基本文件读取：

```python
import pyopenms as ms

# Read mzML file
exp = ms.MSExperiment()
ms.MzMLFile().load("data.mzML", exp)

# Access spectra
for spectrum in exp:
    mz, intensity = spectrum.get_peaks()
    print(f"Spectrum: {len(mz)} peaks")
```

* *详细文件处理**：参见`references/file_io.md`

### 2.信号处理

通过平滑、滤波、质心化等处理原始光谱数据

基础谱图处理：

```python
# Smooth spectrum with Gaussian filter
gaussian = ms.GaussFilter()
params = gaussian.getParameters()
params.setValue("gaussian_width", 0.1)
gaussian.setParameters(params)
gaussian.filterExperiment(exp)
```

* *算法详情**：参见`references/signal_processing.md`

### 3.特征检测

跨谱图和样本检测并链接特征以进行定量

```python
# Detect features
ff = ms.FeatureFinder()
ff.run("centroided", exp, features, params, ms.FeatureMap())
```

* *完整工作流程**：参见`references/feature_detection.md`

### 4.肽和蛋白质识别

与搜索引擎集成并处理识别结果。

* *支持的引擎**：Comet、Mascot、MSGFPlus、XTandem、 OMSSA、Myrimatch

基本鉴定工作流程：

```python
# Load identification data
protein_ids = []
peptide_ids = []
ms.IdXMLFile().load("identifications.idXML", protein_ids, peptide_ids)

# Apply FDR filtering
fdr = ms.FalseDiscoveryRate()
fdr.apply(peptide_ids)
```

* *详细工作流程**：参见`references/identification.md`

### 5.代谢组学分析

执行非靶向代谢组学预处理和

典型工作流程：
1. 加载并处理原始数据
2. 检测特征
3. 对齐样品 
4 的保留时间。将特征链接到共识图
5. 使用化合物数据库进行注释

* *有关完整的代谢组学工作流程**：请参阅 `references/metabolomics.md`

## 数据结构

PyOpenMS 使用以下主要对象：

- **MSExperiment**：光谱和色谱图的收集
- **MSSpectrum**：具有 m/z 和强度对的单一质谱
- **MSChromatogram**：色谱图
- **功能**：检测到的色谱峰及其质量指标
- **FeatureMap**：特征集合
- **PeptideIdentification**：肽搜索结果
- **ProteinIdentification**：蛋白质搜索结果

* *详细文档**：参见`references/data_structures.md`

## 常见工作流程

### 快速入门：加载和探索数据

```python
import pyopenms as ms

# Load mzML file
exp = ms.MSExperiment()
ms.MzMLFile().load("sample.mzML", exp)

# Get basic statistics
print(f"Number of spectra: {exp.getNrSpectra()}")
print(f"Number of chromatograms: {exp.getNrChromatograms()}")

# Examine first spectrum
spec = exp.getSpectrum(0)
print(f"MS level: {spec.getMSLevel()}")
print(f"Retention time: {spec.getRT()}")
mz, intensity = spec.get_peaks()
print(f"Peaks: {len(mz)}")
```

### 参数管理

大多数算法都使用参数系统：

```python
# Get algorithm parameters
algo = ms.GaussFilter()
params = algo.getParameters()

# View available parameters
for param in params.keys():
    print(f"{param}: {params.getValue(param)}")

# Modify parameters
params.setValue("gaussian_width", 0.2)
algo.setParameters(params)
```

### 导出到Pandas

将数据转换为pandas DataFrames分析：

```python
import pyopenms as ms
import pandas as pd

# Load feature map
fm = ms.FeatureMap()
ms.FeatureXMLFile().load("features.featureXML", fm)

# Convert to DataFrame
df = fm.get_df()
print(df.head())
```

## 与其他工具集成

PyOpenMS 与以下集成：
- **Pandas**：将数据导出到 DataFrames
- **NumPy**：使用峰值数组
- **Scikit-learn**：机器学习MS数据
- **Matplotlib/Seaborn**：可视化
- **R**：通过rpy2桥

## 资源

- **官方文档**：https://pyopenms.readthedocs.io
- **OpenMS文档**：https://www.openms.org
- **GitHub**：https://github.com/OpenMS/OpenMS

## 参考文献

- `references/file_io.md` - 综合文件格式处理
- `references/signal_processing.md` - 信号处理算法
- `references/feature_detection.md` - 特征检测和链接
- `references/identification.md` - 肽和蛋白质鉴定
- `references/metabolomics.md` - 代谢组学特定工作流程
- `references/data_structures.md` - 核心对象和数据结构
