---
name: exploratory-data-analysis
description: 对 200 多种文件格式的科学数据文件执行全面的探索性数据分析。在分析任何科学数据文件以了解其结构、内容、质量和特征时，应使用此技能。自动检测文件类型并生成详细的降价报告，其中包含特定格式的分析、质量指标和下游分析建议。涵盖化学、生物信息学、显微镜、光谱学、蛋白质组学、代谢组学和一般科学数据格式。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 探索性数据分析

## 概述

对跨多个领域的科学数据文件执行全面的探索性数据分析 (EDA)。该技能提供自动文件类型检测、特定格式分析、数据质量评估，并生成适合文档和下游分析规划的详细 Markdown 报告。

* *关键功能：**
- 自动检测和分析 200 多种科学文件格式
- 全面的特定格式元数据提取
- 数据质量和完整性评估
- 统计摘要和分布
- 可视化建议
- 下游分析建议
- Markdown 报告生成

## 何时使用此技能

在以下情况下使用此技能：
- 用户提供用于分析的科学数据文件的路径
- 用户要求“探索”、“分析”或“总结”数据文件
- 用户想要了解科学数据的结构和内容
- 用户在分析之前需要数据集的综合报告
- 用户想要评估数据质量或完整性
- 用户询问文件适合哪种类型的分析

## 支持的文件类别

该技能具有全面的覆盖范围科学文件格式分为六大类：

### 1.化学和分子格式（60 多个扩展）
结构文件、计算化学输出、分子动力学轨迹和化学数据库。

* *文件类型包括：** `.pdb`、`.cif`、`.mol`、 `.mol2`、`.sdf`、`.xyz`、`.smi`、`.gro`、`.log`、`.fchk`、`.cube`、`.dcd`、`.xtc`、`.trr`、 `.prmtop`、`.psf`等。

* *参考文件：** `references/chemistry_molecular_formats.md`

### 2.生物信息学和基因组学格式（50+扩展）
序列数据、比对、注释、变异和表达数据。

* *文件类型包括：** `.fasta`、`.fastq`、`.sam`、`.bam`、`.vcf`、 `.bed`、`.gff`、`.gtf`、`.bigwig`、`.h5ad`、`.loom`、`.counts`、`.mtx` 等。

* *参考文件：** `references/bioinformatics_genomics_formats.md`

### 3. 显微镜和成像格式（45+ 扩展）
显微镜图像、医学成像、全玻片成像和电子显微镜。

* *文件类型包括：** `.tif`、`.nd2`、`.lif`、 `.czi`、`.ims`、`.dcm`、`.nii`、`.mrc`、`.dm3`、`.vsi`、`.svs`、`.ome.tiff`等。

* *参考文件：** `references/microscopy_imaging_formats.md`

### 4.光谱和分析化学格式（35+扩展）
NMR、质谱、IR/Raman、UV-Vis、X射线、色谱和其他分析技术。

* *文件类型包括：** `.fid`、`.mzML`、 `.mzXML`、`.raw`、`.mgf`、`.spc`、`.jdx`、`.xy`、`.cif`（晶体学）、`.wdf` 等。

* *参考文件：** `references/spectroscopy_analytical_formats.md`

### 5.蛋白质组学和代谢组学格式（30+扩展）
质谱蛋白质组学、代谢组学、脂质组学和多组学数据。

* *文件类型包括：** `.mzML`、`.pepXML`、`.protXML`、 `.mzid`、`.mzTab`、`.sky`、`.mgf`、`.msp`、`.h5ad` 等。

* *参考文件：** `references/proteomics_metabolomics_formats.md`

### 6. 通用科学数据格式（30+扩展）
数组、表格、分层数据、压缩档案和常见科学格式。

* *文件类型包括：** `.npy`、`.npz`、`.csv`、`.xlsx`、`.json`、`.hdf5`、`.zarr`、`.parquet`、`.mat`、`.fits`、 `.nc`、`.xml`等。

* *参考文件：** `references/general_scientific_formats.md`

## 工作流程

### 第一步：文件类型检测

当用户提供文件路径时，首先识别文件类型：

1. 提取文件扩展名
2. 在相应的参考文件 
3 中查找扩展名。识别文件类别和格式描述
4. 加载格式特定信息

* *示例：**
```
User: "Analyze data.fastq"
→ Extension: .fastq
→ Category: bioinformatics_genomics
→ Format: FASTQ Format (sequence data with quality scores)
→ Reference: references/bioinformatics_genomics_formats.md
```

### 步骤2：加载格式特定信息

根据文件类型，阅读相应的参考文件来了解：
- **典型数据：** 这种格式包含什么样的数据
- **用例：** 此格式的常见应用
- **Python 库：** 如何在 Python 中读取文件
- **EDA 方法：** 哪些分析适合此数据类型

 在参考文件中搜索特定扩展名（例如，在 `bioinformatics_genomics_formats.md` 中搜索“### .fastq”）。

### 步骤3：执行数据分析

使用`scripts/eda_analyzer.py`脚本或实现自定义分析：

* *选项A：使用分析器脚本**
```python
# The script automatically:
# 1. Detects file type
# 2. Loads reference information
# 3. Performs format-specific analysis
# 4. Generates markdown report

python scripts/eda_analyzer.py <filepath> [output.md]
```

* *选项B：对话中的自定义分析**
根据参考文件中的格式信息，执行适当的分析分析：

对于表格数据（CSV、TSV、Excel）：
- 使用 pandas 加载
- 检查维度、数据类型
- 分析缺失值
- 计算汇总统计数据
- 识别异常值
- 检查重复项

对于序列数据（FASTA、FASTQ）：
- 计数序列
- 分析长度分布
- 计算GC 含量
- 评估质量分数（FASTQ）

对于图像（TIFF、ND2、CZI）：
- 检查尺寸（X、Y、Z、C、T）
- 分析位深度和值范围
- 提取元数据（通道、时间戳、空间校准）
- 计算强度统计数据

 对于数组（NPY、HDF5）：
- 检查形状和值维度
- 分析数据类型
- 计算统计摘要
- 检查缺失/无效值

### 步骤4：生成综合报告

创建包含以下部分的Markdown 报告：

#### 必需部分：
1. **标题和元数据**
  - 文件名和时间戳
  - 文件大小和位置

2. **基本信息**
  - 文件属性
  - 格式识别

3. **文件类型详细信息**
  - 参考中的格式描述
  - 典型数据内容
  - 常见用例
  - 用于读取

4的Python库。 **数据分析**
 - 结构和尺寸
  - 统计摘要
  - 质量评估
  - 数据特征

5. **主要发现**
  - 值得注意的模式
  - 潜在问题
  - 质量指标

6. **建议**
  - 预处理步骤
  - 适当的分析
  - 工具和方法
  - 可视化方法

#### 模板位置
使用`assets/report_template.md`作为报告结构的指南。

### 步骤5：保存报告

使用描述性文件名保存Markdown报告：
- 模式：`{original_filename}_eda_report.md`
- 示例：`experiment_data.fastq` → `experiment_data_eda_report.md`

## 详细格式参考

每个参考文件包含数十种文件类型的全面信息。要查找有关特定格式的信息：

1. 从扩展名
2 中识别类别。阅读相应的参考文件
3. 搜索与扩展名匹配的节标题（例如“### .pdb”）
4. 提取格式信息

### 参考文件结构

每个格式条目包括：
- **描述：** 格式是什么
- **典型数据：** 它包含什么
- **用例：** 常见应用
- **Python 库：** 如何阅读它（带有代码示例）
- **EDA 方法：** 要执行的具体分析

* *示例查找：**
```markdown
### .pdb - Protein Data Bank
**Description:** Standard format for 3D structures of biological macromolecules
**Typical Data:** Atomic coordinates, residue information, secondary structure
**Use Cases:** Protein structure analysis, molecular visualization, docking
**Python Libraries:**
- `Biopython`: `Bio.PDB`
- `MDAnalysis`: `MDAnalysis.Universe('file.pdb')`
**EDA Approach:**
- Structure validation (bond lengths, angles)
- B-factor distribution
- Missing residues detection
- Ramachandran plots
```

## 最佳实践

### 阅读参考文件

参考文件很大（每个10,000+字）。要有效地使用它们：

1. **按扩展名搜索：** 使用grep查找具体格式
 ```python
 import re
 with open('references/chemistry_molecular_formats.md', 'r') as f:
 content = f.read()
 pattern = r'### \.pdb[^#]*?(?=###|\Z)'
 match = re.search(模式, 内容, re.IGNORECASE | re.DOTALL)
 ```

2. **提取相关部分：** 不必要时不要将整个参考文件加载到上下文中

3. **缓存格式信息：** 如果分析同一类型的多个文件，请重复使用格式信息

### 数据分析

1. **大文件样本：** 对于具有数百万条记录的文件，分析代表性样本
2. **优雅地处理错误：**许多科学格式需要特定的库；提供清晰的安装说明
3. **验证元数据：**交叉检查元数据一致性（例如，规定维度与实际数据）
4. **考虑数据来源：**记下仪器、软件版本、处理步骤

### 报告生成

1. **全面：** 包括下游分析
2的所有相关信息。 **具体一点：** 根据文件类型
3提供具体建议。 **具有可操作性：** 建议具体的后续步骤和工具
4. **包括代码示例：** 展示如何加载和使用数据

## 示例

### 示例 1：分析 FASTQ 文件

```python
# User provides: "Analyze reads.fastq"

# 1. Detect file type
extension = '.fastq'
category = 'bioinformatics_genomics'

# 2. Read reference info
# Search references/bioinformatics_genomics_formats.md for "### .fastq"

# 3. Perform analysis
from Bio import SeqIO
sequences = list(SeqIO.parse('reads.fastq', 'fastq'))
# Calculate: read count, length distribution, quality scores, GC content

# 4. Generate report
# Include: format description, analysis results, QC recommendations

# 5. Save as: reads_eda_report.md
```

### 示例 2：分析 CSV 数据集

```python
# User provides: "Explore experiment_results.csv"

# 1. Detect: .csv → general_scientific

# 2. Load reference for CSV format

# 3. Analyze
import pandas as pd
df = pd.read_csv('experiment_results.csv')
# Dimensions, dtypes, missing values, statistics, correlations

# 4. Generate report with:
# - Data structure
# - Missing value patterns
# - Statistical summaries
# - Correlation matrix
# - Outlier detection results

# 5. Save report
```

### 示例 3：分析显微镜数据

```python
# User provides: "Analyze cells.nd2"

# 1. Detect: .nd2 → microscopy_imaging (Nikon format)

# 2. Read reference for ND2 format
# Learn: multi-dimensional (XYZCT), requires nd2reader

# 3. Analyze
from nd2reader import ND2Reader
with ND2Reader('cells.nd2') as images:
    # Extract: dimensions, channels, timepoints, metadata
    # Calculate: intensity statistics, frame info

# 4. Generate report with:
# - Image dimensions (XY, Z-stacks, time, channels)
# - Channel wavelengths
# - Pixel size and calibration
# - Recommendations for image analysis

# 5. Save report
```

## 故障排除

### 缺少库

许多科学格式需要专门的库：

* *问题：** 尝试读取文件

* *解决方案：**提供清晰的安装说明
```python
try:
    from Bio import SeqIO
except ImportError:
    print("Install Biopython: uv pip install biopython")
```

按类别常见要求：
- **生物信息学：** `biopython`、`pysam`、`pyBigWig`
- **化学：** `rdkit`、`mdanalysis`、`cclib`
- **显微镜检查：** `tifffile`、`nd2reader`、`aicsimageio`、`pydicom`
- **光谱检查：** `nmrglue`、 `pymzml`、`pyteomics`
- **常规：** `pandas`、`numpy`、`h5py`、`scipy`

### 未知文件类型

如果文件扩展名不在参考文献：

1. 向用户询问文件格式
2. 检查它是否是供应商特定的变体
3. 尝试基于文件结构（文本与二进制）
4 进行通用分析。提供一般建议

### 大文件

对于非常大的文件：

1. 使用抽样策略（前N条记录）
2. 使用内存映射访问（适用于 HDF5、NPY）
3. 分块处理（对于 CSV、FASTQ）
4. 根据样本提供估算

## 脚本用法

`scripts/eda_analyzer.py`可以直接使用：

```bash
# Basic usage
python scripts/eda_analyzer.py data.csv

# Specify output file
python scripts/eda_analyzer.py data.csv output_report.md

# The script will:
# 1. Auto-detect file type
# 2. Load format references
# 3. Perform appropriate analysis
# 4. Generate markdown report
```

该脚本支持许多常见格式的自动分析，但对话中的自定义分析提供了更大的灵活性和特定领域的见解。

## 高级用法

### 多文件分析

分析多个相关文件时：
1. 对每个文件 
2 执行单独的 EDA。创建总结比较报告
3. 确定关系和依赖关系
4. 建议整合策略

### 质量控制

用于数据质量评估：
1. 检查格式合规性
2. 验证元数据一致性
3. 评估完整性
4. 识别异常值和异常值
5. 与预期范围/分布比较

### 预处理建议

根据数据特征，推荐：
1. 标准化策略
2. 缺失值插补
3. 异常值处理
4. 批量修正
5. 格式转换

## 资源

### 脚本/
- `eda_analyzer.py`：可直接运行或导入的综合分析脚本

### 参考文献/
- `chemistry_molecular_formats.md`：60+化学/分子文件格式
- `bioinformatics_genomics_formats.md`：50+生物信息学格式
- `microscopy_imaging_formats.md`：45+成像格式
- `spectroscopy_analytical_formats.md`：35+光谱格式
- `proteomics_metabolomics_formats.md`：30+组学格式
- `general_scientific_formats.md`：30多种通用格式

### asset/
- `report_template.md`：EDA报告的综合Markdown模板
