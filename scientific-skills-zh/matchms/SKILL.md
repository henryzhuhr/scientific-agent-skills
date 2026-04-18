---
name: matchms
description: 代谢组学的光谱相似性和化合物鉴定。用于比较质谱、计算相似性分数（余弦、修正余弦）以及从谱库中识别未知化合物。最适合代谢物鉴定、光谱匹配、库搜索。对于完整的 LC-MS/MS 蛋白质组学流程，请使用 pyopenms。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# Matchms

## 概述

Matchms 是一个用于质谱数据处理和分析的开源 Python 库。从各种格式导入谱图，标准化元数据，过滤峰，计算谱图相似性，并构建可重复的分析工作流程。

## 核心功能

### 1. 导入和导出质谱数据

从多种文件格式加载谱图并导出处理后的数据：

```python
from matchms.importing import load_from_mgf, load_from_mzml, load_from_msp, load_from_json
from matchms.exporting import save_as_mgf, save_as_msp, save_as_json

# Import spectra
spectra = list(load_from_mgf("spectra.mgf"))
spectra = list(load_from_mzml("data.mzML"))
spectra = list(load_from_msp("library.msp"))

# Export processed spectra
save_as_mgf(spectra, "output.mgf")
save_as_json(spectra, "output.json")
```

* *支持格式：**
- mzML 和 mzXML（原始质谱格式）
- MGF（Mascot 通用格式）
- MSP（谱库格式）
- JSON（GNPS 兼容）
- 代谢组学-USI 参考文献
- Pickle（Python）序列化）

有关详细的导入/导出文档，请参阅 `references/importing_exporting.md`.

### 2. 频谱过滤和处理

应用全面的过滤器来标准化元数据并细化峰值数据：

```python
from matchms.filtering import default_filters, normalize_intensities
from matchms.filtering import select_by_relative_intensity, require_minimum_number_of_peaks

# Apply default metadata harmonization filters
spectrum = default_filters(spectrum)

# Normalize peak intensities
spectrum = normalize_intensities(spectrum)

# Filter peaks by relative intensity
spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01, intensity_to=1.0)

# Require minimum peaks
spectrum = require_minimum_number_of_peaks(spectrum, n_required=5)
```

* *过滤器类别：**
- **元数据处理**：协调化合物名称、派生化学结构、标准化加合物、纠正电荷
- **峰过滤**：标准化强度、按 m/z 或强度选择、删除前体峰
- **质量控制**：需要最小峰、验证前体 m/z、确保元数据完整性
- **化学注释**：添加指纹、派生在ChI/SMILES中，修复结构不匹配

Matchms提供40+过滤器。有关完整的滤波器参考，请参阅 `references/filtering.md`.

### 3. 计算光谱相似度

使用各种相似性度量比较光谱：

```python
from matchms import calculate_scores
from matchms.similarity import CosineGreedy, ModifiedCosine, CosineHungarian

# Calculate cosine similarity (fast, greedy algorithm)
scores = calculate_scores(references=library_spectra,
                         queries=query_spectra,
                         similarity_function=CosineGreedy())

# Calculate modified cosine (accounts for precursor m/z differences)
scores = calculate_scores(references=library_spectra,
                         queries=query_spectra,
                         similarity_function=ModifiedCosine(tolerance=0.1))

# Get best matches
best_matches = scores.scores_by_query(query_spectra[0], sort=True)[:10]
```

* *可用的相似性函数：**
- **CosineGreedy/CosineHungarian**：具有不同匹配算法的基于峰值的余弦相似性
- **ModifiedCosine**：考虑前体质量差异的余弦相似性
- **NeutralLossesCosine**：基于中性损失的相似性模式
- **FingerprintSimilarity**：使用指纹的分子结构相似性
- **MetadataMatch**：比较用户定义的元数据字段
- **PrecursorMzMatch/ParentMassMatch**：基于简单质量的过滤

有关详细的相似性函数文档，请参阅`references/similarity.md`.

### 4. 构建处理管道

创建可重复的多步骤分析工作流程：

```python
from matchms import SpectrumProcessor
from matchms.filtering import default_filters, normalize_intensities
from matchms.filtering import select_by_relative_intensity, remove_peaks_around_precursor_mz

# Define a processing pipeline
processor = SpectrumProcessor([
    default_filters,
    normalize_intensities,
    lambda s: select_by_relative_intensity(s, intensity_from=0.01),
    lambda s: remove_peaks_around_precursor_mz(s, mz_tolerance=17)
])

# Apply to all spectra
processed_spectra = [processor(s) for s in spectra]
```

### 5. 使用光谱对象

核心 `Spectrum` 类包含质谱数据：

```python
from matchms import Spectrum
import numpy as np

# Create a spectrum
mz = np.array([100.0, 150.0, 200.0, 250.0])
intensities = np.array([0.1, 0.5, 0.9, 0.3])
metadata = {"precursor_mz": 250.5, "ionmode": "positive"}

spectrum = Spectrum(mz=mz, intensities=intensities, metadata=metadata)

# Access spectrum properties
print(spectrum.peaks.mz)           # m/z values
print(spectrum.peaks.intensities)  # Intensity values
print(spectrum.get("precursor_mz")) # Metadata field

# Visualize spectra
spectrum.plot()
spectrum.plot_against(reference_spectrum)
```

### 6. 元数据管理

标准化和协调谱图元数据：

```python
# Metadata is automatically harmonized
spectrum.set("Precursor_mz", 250.5)  # Gets harmonized to lowercase key
print(spectrum.get("precursor_mz"))   # Returns 250.5

# Derive chemical information
from matchms.filtering import derive_inchi_from_smiles, derive_inchikey_from_inchi
from matchms.filtering import add_fingerprint

spectrum = derive_inchi_from_smiles(spectrum)
spectrum = derive_inchikey_from_inchi(spectrum)
spectrum = add_fingerprint(spectrum, fingerprint_type="morgan", nbits=2048)
```

## 常见工作流程

对于典型的质谱分析工作流程，包括：
- 加载和预处理谱库
- 将未知谱与参考谱进行匹配
- 质量过滤和数据清理
- 大规模相似性比较
- 基于网络的谱聚类

 详细示例请参阅`references/workflows.md`。

## 安装

```bash
uv pip install matchms
```

用于分子结构处理（SMILES、InChI）：
```bash
uv pip install matchms[chemistry]
```

## 参考文档

详细参考文档在`references/`目录：
- `filtering.md` - 带有描述的完整过滤函数参考
- `similarity.md` - 所有相似性指标以及何时使用它们
- `importing_exporting.md` - 文件格式详细信息和I/O操作
- `workflows.md` - 常见分析模式和示例

根据需要加载这些参考资料以获取有关特定的详细信息matchms 功能。
