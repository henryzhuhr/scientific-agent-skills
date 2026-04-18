# Matchms 导入和导出参考

本文档详细介绍了matchms中用于加载和保存质谱数据的所有文件格式支持。

## 导入光谱

Matchms 提供了从各种文件格式加载光谱的专用功能。所有导入函数都会返回生成器，以实现大文件的内存高效处理。

### 常见导入模式

```python
from matchms.importing import load_from_mgf

# Load spectra (returns generator)
spectra_generator = load_from_mgf("spectra.mgf")

# Convert to list for processing
spectra = list(spectra_generator)
```

## 支持的导入格式

### MGF（吉祥物通用格式）

* *函数**：`load_from_mgf(filename, metadata_harmonization=True)`

* *说明**：加载MGF 文件中的光谱，质谱数据交换的通用格式。

* *参数**：
- `filename` (str)：MGF 文件的路径
- `metadata_harmonization`（布尔值，默认=True）：应用自动元数据密钥Harmonization

* *示例**：
```python
from matchms.importing import load_from_mgf

# Load with metadata harmonization
spectra = list(load_from_mgf("data.mgf"))

# Load without harmonization
spectra = list(load_from_mgf("data.mgf", metadata_harmonization=False))
```

* *MGF 格式**：基于文本的格式，带有包含元数据和峰列表的 BEGIN IONS/END IONS 块。

- --

### MSP（NIST 质谱库）格式）

* *功能**：`load_from_msp(filename, metadata_harmonization=True)`

* *说明**：从MSP文件加载光谱，常用于光谱库。

* *参数**：
- `filename`（str）：MSP文件路径
- `metadata_harmonization` （布尔，默认= True）：应用自动元数据协调

* *示例**：
```python
from matchms.importing import load_from_msp

spectra = list(load_from_msp("library.msp"))
```

* *MSP格式**：基于文本的格式，具有名称/MW/注释字段，后跟峰列表。

- --

### mzML（质谱标记）语言）

* *功能**：`load_from_mzml(filename, ms_level=2, metadata_harmonization=True)`

* *描述**：从 mzML 文件加载谱图，这是原始质谱数据基于 XML 的标准格式。

* *参数**：
- `filename`（str）：mzML 文件的路径
- `ms_level`（int，默认 = 2）：要提取的 MS 级别（1 表示 MS1，2 表示 MS2/串联）
- `metadata_harmonization`（布尔值，默认 = True）：应用自动元数据协调

* *示例**：
```python
from matchms.importing import load_from_mzml

# Load MS2 spectra (default)
ms2_spectra = list(load_from_mzml("data.mzML"))

# Load MS1 spectra
ms1_spectra = list(load_from_mzml("data.mzML", ms_level=1))
```

* *mzML格式**：基于XML的标准格式，包含原始仪器数据和丰富的元数据。

- --

### mzXML

* *功能**：`load_from_mzxml(filename, ms_level=2, metadata_harmonization=True)`

* *描述**：从 mzXML 文件加载谱图，这是一种早期基于 XML 的质谱数据格式。

* *参数**：
- `filename` (str)：mzXML 文件的路径
- `ms_level`（int，默认=2）：要提取的 MS 级别
- `metadata_harmonization`（布尔值，默认=True）：应用自动元数据协调

* *示例**：
```python
from matchms.importing import load_from_mzxml

spectra = list(load_from_mzxml("data.mzXML"))
```

* *mzXML 格式**：基于 XML 的格式，是mzML.

- --

### JSON（GNPS 格式）

* *功能**：`load_from_json(filename, metadata_harmonization=True)`

* *说明**：从 JSON 文件加载光谱，特别是 GNPS 兼容的 JSON 格式。

* *参数**：
- `filename` (str)：JSON 文件的路径
- `metadata_harmonization`（布尔值，默认值=True）：应用自动元数据协调

* *示例**：
```python
from matchms.importing import load_from_json

spectra = list(load_from_json("spectra.json"))
```

* *JSON 格式**：具有频谱元数据和峰值的结构化 JSON arrays.

- --

### Pickle（Python 序列化）

* *函数**：`load_from_pickle(filename)`

* *说明**：从pickle 文件加载之前保存的matchms Spectrum 对象。快速加载预处理光谱。

* *参数**：
- `filename`（str）：泡菜文件的路径

* *示例**：
```python
from matchms.importing import load_from_pickle

spectra = list(load_from_pickle("processed_spectra.pkl"))
```

* *用例**：保存和加载预处理光谱以加快后续操作分析。

- --

### USI（通用谱图标识符）

* *功能**：`load_from_usi(usi)`

* *说明**：从代谢组学 USI 参考加载单个谱图。

* *参数**：
- `usi` (str): 通用谱图标识符字符串

* *示例**:
```python
from matchms.importing import load_from_usi

usi = "mzspec:GNPS:TASK-...:spectrum..."
spectrum = load_from_usi(usi)
```

* *USI 格式**: 用于从在线存储库访问谱图的标准化标识符。

- --

## 导出Spectra

Matchms 提供将处理后的光谱保存为各种格式以便共享和存档的功能。

### MGF Export

* *功能**：`save_as_mgf(spectra, filename, write_mode='w')`

* *说明**：将光谱保存为 MGF 格式。

* *参数**：
- `spectra` (list)：要保存的 Spectrum 对象列表
- `filename` (str)：输出文件路径
- `write_mode` (str，default='w')：文件写入模式（'w' 表示写入，'a' 表示附加）

* *示例**：
```python
from matchms.exporting import save_as_mgf

save_as_mgf(processed_spectra, "output.mgf")
```

- --

### MSP Export

* *功能**：`save_as_msp(spectra, filename, write_mode='w')`

* *说明**：将光谱保存到MSP format.

* *参数**:
- `spectra` (list): 要保存的 Spectrum 对象列表
- `filename` (str): 输出文件路径
- `write_mode` (str, default='w'): 文件写入模式

* *示例**：
```python
from matchms.exporting import save_as_msp

save_as_msp(library_spectra, "library.msp")
```

- --

### JSON导出

* *功能**：`save_as_json(spectra, filename, write_mode='w')`

* *描述**：将光谱保存为JSON格式（GNPS 兼容）。

* *参数**：
- `spectra`（列表）：要保存的频谱对象列表
- `filename`（str）：输出文件路径
- `write_mode`（str，默认='w'）：文件写入mode

* *示例**：
```python
from matchms.exporting import save_as_json

save_as_json(spectra, "spectra.json")
```

- --

### Pickle Export

* *功能**：`save_as_pickle(spectra, filename)`

* *说明**：将光谱保存为Python pickle文件。保留所有 Spectrum 属性，加载速度最快。

* *参数**：
- `spectra` (list)：要保存的 Spectrum 对象列表
- `filename` (str)：输出文件路径

* *示例**：
```python
from matchms.exporting import save_as_pickle

save_as_pickle(processed_spectra, "processed.pkl")
```

* *优点**：
- 快速保存和加载
- 保留准确的频谱状态
- 无格式转换开销

* *缺点**：
- 不可读
- Python 特定（不可移植到其他语言）
- Pickle 格式可能不兼容 Python 版本

- --

## 完整的导入/导出工作流程

### 预处理和保存管道

```python
from matchms.importing import load_from_mgf
from matchms.exporting import save_as_mgf, save_as_pickle
from matchms.filtering import default_filters, normalize_intensities
from matchms.filtering import select_by_relative_intensity

# Load raw spectra
spectra = list(load_from_mgf("raw_data.mgf"))

# Process spectra
processed = []
for spectrum in spectra:
    spectrum = default_filters(spectrum)
    spectrum = normalize_intensities(spectrum)
    spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01)
    if spectrum is not None:
        processed.append(spectrum)

# Save processed spectra (MGF for sharing)
save_as_mgf(processed, "processed_data.mgf")

# Save as pickle for fast reloading
save_as_pickle(processed, "processed_data.pkl")
```

### 格式转换

```python
from matchms.importing import load_from_mzml
from matchms.exporting import save_as_mgf, save_as_msp

# Convert mzML to MGF
spectra = list(load_from_mzml("data.mzML", ms_level=2))
save_as_mgf(spectra, "data.mgf")

# Convert to MSP library format
save_as_msp(spectra, "data.msp")
```

### 从多个文件加载

```python
from matchms.importing import load_from_mgf
import glob

# Load all MGF files in directory
all_spectra = []
for mgf_file in glob.glob("data/*.mgf"):
    spectra = list(load_from_mgf(mgf_file))
    all_spectra.extend(spectra)

print(f"Loaded {len(all_spectra)} spectra from multiple files")
```

### 内存高效处理

```python
from matchms.importing import load_from_mgf
from matchms.exporting import save_as_mgf
from matchms.filtering import default_filters, normalize_intensities

# Process large file without loading all into memory
def process_spectrum(spectrum):
    spectrum = default_filters(spectrum)
    spectrum = normalize_intensities(spectrum)
    return spectrum

# Stream processing
with open("output.mgf", 'w') as outfile:
    for spectrum in load_from_mgf("large_file.mgf"):
        processed = process_spectrum(spectrum)
        if processed is not None:
            # Write immediately without storing in memory
            save_as_mgf([processed], outfile, write_mode='a')
```

## 格式选择指南

* *MGF**:
- ✓ 广泛支持
- ✓ 人类可读
- ✓ 适合数据共享
- ✓ 中等文件大小
- 最适合：数据交换、GNPS 上传、发布数据

* *MSP**:
- ✓ 光谱库标准
- ✓ 人类可读
- ✓ 良好的元数据支持
- 最适合：参考库、NIST 格式兼容性

* *JSON**:
- ✓ 结构化格式
- ✓ GNPS 兼容
- ✓ 易于解析以编程方式
- 最适合：Web 应用程序、GNPS 集成、结构化数据

* *Pickle**：
- ✓ 最快保存/加载
- ✓ 保留精确状态
- ✗ 不可移植到其他语言
- ✗ 否人类可读的
- 最适合：中间处理、仅限Python 的工作流程

* *mzML/mzXML**:
- ✓ 原始仪器数据
- ✓ 丰富的元数据
- ✓ 行业标准
- ✗ 大文件大小
- ✗ 解析速度较慢
- 最适合：原始数据归档、多级 MS 数据

## 元数据协调

`metadata_harmonization` 参数（在大多数导入函数中可用）自动标准化元数据键：

```python
# Without harmonization
spectrum = load_from_mgf("data.mgf", metadata_harmonization=False)
# May have: "PRECURSOR_MZ", "Precursor_mz", "precursormz"

# With harmonization (default)
spectrum = load_from_mgf("data.mgf", metadata_harmonization=True)
# Standardized to: "precursor_mz"
```

* *推荐**：保留启用协调（默认），以实现跨不同数据源的一致元数据访问。

## 文件格式规范

有关详细格式规范：
- **MGF**：http://www.matrixscience.com/help/data_file_help.html
- **MSP**： https://chemdata.nist.gov/mass-spc/ms-search/
- **mzML**：http://www.psidev.info/mzML
- **GNPS JSON**：https://gnps.ucsd.edu/

## 进一步阅读

完整的 API文档：
 https://matchms.readthedocs.io/en/latest/api/matchms.importing.html
 https://matchms.readthedocs.io/en/latest/api/matchms.exporting.html
