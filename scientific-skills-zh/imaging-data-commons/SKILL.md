---
name: imaging-data-commons
description: 使用 idc-index 从 NCI Imaging Data Commons 查询和下载公共癌症成像数据。用于访问大规模放射学（CT、MR、PET）和病理学数据集以进行 AI 培训或研究。无需身份验证。按元数据查询、在浏览器中可视化、检查许可证。
license: This skill is provided under the MIT License. IDC data itself has individual licensing (mostly CC-BY, some CC-NC) that must be respected when using the data.
metadata:
    version: 1.4.0
    skill-author: Andrey Fedorov, @fedorov
    idc-index: "0.11.14"
    idc-data-version: "v23"
    repository: https://github.com/ImagingDataCommons/idc-claude-skill
---

# 成像数据共享

## 概述

使用 `idc-index` Python 包从国家癌症研究所成像数据共享 (IDC)查询和下载公共癌症成像数据。数据访问无需身份验证。

* *当前 IDC 数据版本：v23**（始终使用 `IDCClient().get_idc_version()` 进行验证）

* *主要工具：** `idc-index` ([GitHub](https://github.com/imagingdatacommons/idc-index))

* *关键 - 检查软件包版本并根据需要进行升级（运行此工具）第一）：**

```python
import idc_index

REQUIRED_VERSION = "0.11.14"  # Must match metadata.idc-index in this file
installed = idc_index.__version__

if installed < REQUIRED_VERSION:
    print(f"Upgrading idc-index from {installed} to {REQUIRED_VERSION}...")
    import subprocess
    subprocess.run(["pip3", "install", "--upgrade", "--break-system-packages", "idc-index"], check=True)
    print("Upgrade complete. Restart Python to use new version.")
else:
    print(f"idc-index {installed} meets requirement ({REQUIRED_VERSION})")
```

* *验证IDC数据版本并检查当前数据规模：**

```python
from idc_index import IDCClient
client = IDCClient()

# Verify IDC data version (should be "v23")
print(f"IDC data version: {client.get_idc_version()}")

# Get collection count and total series
stats = client.sql_query("""
    SELECT
        COUNT(DISTINCT collection_id) as collections,
        COUNT(DISTINCT analysis_result_id) as analysis_results,
        COUNT(DISTINCT PatientID) as patients,
        COUNT(DISTINCT StudyInstanceUID) as studies,
        COUNT(DISTINCT SeriesInstanceUID) as series,
        SUM(instanceCount) as instances,
        SUM(series_size_MB)/1000000 as size_TB
    FROM index
""")
print(stats)
```

* *核心工作流程：**
1. 查询元数据 → `client.sql_query()`
2. 下载 DICOM 文件 → `client.download_from_selection()`
3. 在浏览器中可视化 → `client.get_viewer_URL(seriesInstanceUID=...)`

## 何时使用此技能

- 查找公开可用的放射学（CT、MR、PET）或病理学（载玻片显微镜）图像
- 按癌症类型、形态、解剖部位或其他元数据选择图像子集
- 从以下位置下载 DICOM 数据IDC
- 在研究或商业应用中使用之前检查数据许可证
- 在没有本地 DICOM 查看器软件的浏览器中可视化医学图像

## 快速导航

* *核心部分（内联）：**
- IDC 数据模型 - 收集和分析结果层次结构
- 索引表 - 可用表和连接模式
- 安装-包设置和版本验证
- 核心功能-基本API模式（查询、下载、可视化、许可、引用、批量）
- 最佳实践-使用指南
- 故障排除-常见问题和解决方案

* *参考指南（按需加载）：**

|指南|何时加载 |
|-------|----------------|
| `index_tables_guide.md` |复杂 JOIN、模式发现、DataFrame 访问 |
| `use_cases.md` |端到端工作流程示例（训练数据集、批量下载）|
| `sql_patterns.md` |用于过滤器发现、注释、大小估计的快速 SQL 模式 |
| `clinical_data_guide.md` |临床/表格数据、成像+临床连接、值映射|
| `cloud_storage_guide.md` |直接 S3/GCS 访问、版本控制、UUID 映射 |
| `dicomweb_guide.md` | DICOMweb 端点、PACS 集成 |
| `digital_pathology_guide.md` |载玻片显微镜 (SM)、注释 (ANN)、病理工作流程 |
| `bigquery_guide.md` |完整的 DICOM 元数据，私有元素（需要 GCP）|
| `cli_guide.md` |命令行工具（`idc download`、清单文件）|
| `parquet_access_guide.md` |通过 GCS 直接 Parquet 查询（无需安装 idc-index）|

## IDC 数据模型

IDC 在标准 DICOM 层次结构之上添加了两个分组级别（患者 → 研究 → 系列 → 实例）：

- **collection_id**：按疾病、模式或研究重点对患者进行分组（例如，`tcga_luad`、 `nlst`）。患者恰好属于一个集合。
- **analysis_result_id**：识别一个或多个原始集合中的派生对象（分割、注释、放射组学特征）。

使用 `collection_id` 查找原始成像数据，可能包括与图像一起存储的注释；使用`analysis_result_id`查找AI生成的或专家注释。

* *查询的关键标识符：**
|标识符 |范围 |用于 |
|------------|--------|---------|
| `collection_id` |数据集分组|按项目/研究过滤 |
| `PatientID` |病人 |按患者对图像进行分组|
| `StudyInstanceUID` | DICOM 研究 |相关系列分组、可视化|
| `SeriesInstanceUID` | DICOM系列|相关系列分组、可视化|

## 索引表

`idc-index`包提供了多个元数据索引表，可以通过SQL或pandas DataFrames访问。

* *完整的索引表文档：**使用https://idc-index.readthedocs.io/en/latest/indices_reference.html快速检查可用的表和列，无需执行任何代码。

* *重要：**使用`client.indices_overview` 获取当前表描述和列模式。这是可用列及其类型的权威来源 - 在编写 SQL 或探索数据结构时始终查询它。

### 可用表

|表|行粒度|已加载 |说明 |
|--------|------------------|--------|-------------|
| `index` | 1 行 = 1 DICOM 系列 |汽车 |所有当前 IDC 数据的主要元数据 |
| `prior_versions_index` | 1 行 = 1 DICOM 系列 |汽车 | IDC 之前版本的系列；用于下载已弃用的数据 |
| `collections_index` | 1 行 = 1 个集合 | fetch_index() | 获取索引集合级元数据和描述 |
| `analysis_results_index` | 1行=1个分析结果集合| fetch_index() | 获取索引有关派生数据集的元数据（注释、分段）|
| `clinical_index` | 1 行 = 1 临床数据列 | fetch_index() | 获取索引将临床表列映射到集合的字典 |
| `sm_index` | 1 行 = 1 个载玻片显微镜系列 | fetch_index() | 获取索引载玻片显微镜（病理学）系列元数据|
| `sm_instance_index` | 1 行 = 1 个载玻片显微镜实例 | fetch_index() | 获取索引用于载玻片显微镜的实例级 (SOPInstanceUID)元数据 |
| `seg_index` | 1 行 = 1 DICOM 分割系列 | fetch_index() | 获取索引分割元数据：算法、分割计数、参考源图像系列|
| `ann_index` | 1 行 = 1 DICOM ANN 系列 | fetch_index() | 获取索引显微镜批量简单注释系列元数据；参考带注释的图像系列|
| `ann_group_index` | 1 行 = 1 个注释组 | fetch_index() | 获取索引详细注释组元数据：图形类型、注释数量、属性代码、算法|
| `contrast_index` | 1 行 = 1 个带有对比信息的系列 | fetch_index() | 获取索引造影剂元数据：造影剂名称、成分、给药途径（CT、MR、PT、XA、RF）|
| `volume_geometry_index` | 1 行 = 1 个 CT/MR/PT 系列 | fetch_index() | 获取索引单帧 CT、MR 和 PT 系列的 3D 体积几何验证；方向、间距、尺寸和切片位置的布尔检查；复合材料 `regularly_spaced_3d_volume` 标志 |
| `rtstruct_index` | 1 行 = 1 个 RTSTRUCT 系列 | fetch_index() | 获取索引RT 结构集元数据：ROI 总数、ROI 名称、生成算法、解释类型和引用的图像系列 UID |

* *Auto** = 实例化`IDCClient()`时自动加载
* *fetch_index()** = 需要`client.fetch_index("table_name")`加载

### 连接表

* *关键列没有显式标记，以下是可以在连接中使用的子集。**

|加入专栏 |桌子|使用案例|
|------------|--------|----------|
| `collection_id` |索引、先前版本索引、集合索引、临床索引 |将系列链接到集合元数据或临床数据 |
| `SeriesInstanceUID` |索引、先前版本索引、sm_index、sm_instance_index |跨表链接系列；连接到载玻片显微镜详细信息|
| `StudyInstanceUID` |索引，先前版本索引 |将当前和历史数据的研究联系起来 |
| `PatientID` |索引，先前版本索引 |将患者与当前和历史数据联系起来|
| `analysis_result_id` |索引，分析结果索引 |将系列链接到分析结果元数据（注释、分段）|
| `source_DOI` |索引，分析结果索引 |通过出版物 DOI |
| 链接`crdc_series_uuid` |索引，先前版本索引 |通过 CRDC 唯一标识符 |
| 链接`Modality` |索引，先前版本索引 |按成像方式过滤|
| `SeriesInstanceUID` |索引、seg_index、ann_index、ann_group_index、contrast_index |将分段/注释/对比系列链接到其索引元数据 |
| `segmented_SeriesInstanceUID` | seg_index → 索引 |将分段链接到其源图像系列（加入 seg_index.segmented_SeriesInstanceUID = index.SeriesInstanceUID）|
| `referenced_SeriesInstanceUID` | ann_index → 索引 |将注释链接到其源图像系列（加入 ann_index.referenced_SeriesInstanceUID = index.SeriesInstanceUID）|
| `SeriesInstanceUID` |索引，体积几何索引 |将系列链接到其 3D 几何验证结果（连接index.SeriesInstanceUID =volume_geometry_index.SeriesInstanceUID）|
| `SeriesInstanceUID` / `referenced_SeriesInstanceUID` |索引，rtstruct_index |将 RTSTRUCT 系列加入其元数据 (index.SeriesInstanceUID = rtstruct_index.SeriesInstanceUID);使用 rtstruct_index.referenced_SeriesInstanceUID 查找源图像系列 |

* *注意：** `Subjects`、`Updated` 和 `Description` 出现在多个表中，但具有不同的含义（计数与标识符、不同的更新上下文）。

有关详细的联接示例、架构发现模式、关键列引用和 DataFrame 访问，请参阅 `references/index_tables_guide.md`。

### 临床数据访问

```python
# Fetch clinical index (also downloads clinical data tables)
client.fetch_index("clinical_index")

# Query clinical index to find available tables and their columns
tables = client.sql_query("SELECT DISTINCT table_name, column_label FROM clinical_index")

# Load a specific clinical table as DataFrame
clinical_df = client.get_clinical_table("table_name")
```

请参阅`references/clinical_data_guide.md`了解详细的工作流程，包括值映射模式以及将临床数据与成像连接。

## 数据访问选项

|方法|需要身份验证 |最适合|
|--------|----------------|----------|
| `idc-index` |没有 |重点查询及下载（推荐）|
|直接实木复合地板 (GCS) |没有 |无需安装idc-index即可快速查询；始终使用最新数据|
| IDC门户 |没有 |互动探索、手动选择、浏览器下载|
| BigQuery |是（GCP 帐户）|复杂查询，完整 DICOM 元数据 |
| DICOMweb 代理 |没有 |通过 DICOMweb API 进行工具集成 |
|云存储（S3/GCS）|没有 |直接文件访问、批量下载、自定义管道 |

* *云存储组织**

IDC 维护 AWS S3 和 Google Cloud Storage 之间镜像的公共云存储桶中的所有 DICOM 文件。文件按 CRDC UUID（而不是 DICOM UID）组织以支持版本控制。

|桶（AWS / GCS）|许可证|内容|
|--------------------|---------|---------|
| `idc-open-data` / `idc-open-data` |无商业限制 | >90% 的 IDC 数据 |
| `idc-open-data-two` / `idc-open-idc1` |无商业限制 |具有潜在头部扫描的集合 |
| `idc-open-data-cr` / `idc-open-cr` |商业用途受限 (CC BY-NC) | ~4% 的数据 |

文件存储为 `<crdc_series_uuid>/<crdc_instance_uuid>.dcm`。通过 AWS CLI、gsutil 或 s5cmd 进行匿名访问是免费的（无出口费用）。使用 S3 URL 索引中的 `series_aws_url` 列； GCS 使用相同的路径结构。

有关存储桶详细信息、访问命令、UUID 映射和版本控制，请参阅 

。

* *DICOMweb 访问**

IDC 数据可通过 DICOMweb 界面（Google Cloud Healthcare API 实现）获取，以便与 PACS 系统和 DICOMweb 兼容工具集成。

|端点|授权 |使用案例|
|----------|------|----------|
|公共代理|没有 |测试、适度查询、每日配额|
|谷歌医疗保健 |是 (GCP) |生产使用，更高配额 |

有关端点 URL、代码示例、支持的操作和实现详细信息，请参阅 `references/dicomweb_guide.md`。

* *直接 Parquet 访问**

所有 idc 索引元数据表都作为 Parquet 文件发布到具有不受限制的 CORS 的公共 GCS 存储桶 (`idc-index-data-artifacts`)。这使得 DuckDB 或 pandas 查询无需安装 idc-index，包括跨表联接以及针对 `volume_geometry_index` 和 `rtstruct_index` 的查询。

有关 URL 模式、可用文件和 DuckDB 查询示例，请参阅 `references/parquet_access_guide.md`。

## 安装和设置

* *必需（对于基本功能）访问）：**
```bash
pip install --upgrade idc-index
```

* *重要：**新的IDC数据发布将始终触发`idc-index`的新版本。安装时始终使用 `--upgrade` 标志，除非为了重现性需要旧版本。

* *重要：** IDC 数据版本 v23 是当前版本。始终验证您的版本：
```python
print(client.get_idc_version())  # Should return "v23"
```
如果您看到旧版本，请升级：`pip install --upgrade idc-index`

* *测试使用：** idc-index 0.11.14（IDC数据版本v23）

* *可选（用于数据）分析）：**
```bash
pip install pandas numpy pydicom
```

## 核心能力

### 1.数据发现与探索

了解 IDC 中可用的影像集合和数据：

```python
from idc_index import IDCClient

client = IDCClient()

# Get summary statistics from primary index
query = """
SELECT
  collection_id,
  COUNT(DISTINCT PatientID) as patients,
  COUNT(DISTINCT SeriesInstanceUID) as series,
  SUM(series_size_MB) as size_mb
FROM index
GROUP BY collection_id
ORDER BY patients DESC
"""
collections_summary = client.sql_query(query)

# For richer collection metadata, use collections_index
client.fetch_index("collections_index")
collections_info = client.sql_query("""
    SELECT collection_id, CancerTypes, TumorLocations, Species, Subjects, SupportingData
    FROM collections_index
""")

# For analysis results (annotations, segmentations), use analysis_results_index
client.fetch_index("analysis_results_index")
analysis_info = client.sql_query("""
    SELECT analysis_result_id, analysis_result_title, Subjects, Collections, Modalities
    FROM analysis_results_index
""")
```

* *`collections_index`** 提供每个集合的精选元数据：癌症类型、肿瘤位置、物种、受试者计数和支持数据类型 - 无需从主索引进行聚合。

* *`analysis_results_index`** 列出派生数据集（AI 分割、专家注释、放射组学特征）及其源集合和模式。

### 2. 使用 SQL 查询元数据

使用 SQL 查询 IDC 迷你索引以查找特定数据集。

* *首先，探索过滤器列的可用值：**
```python
from idc_index import IDCClient

client = IDCClient()

# Check what Modality values exist
modalities = client.sql_query("""
    SELECT DISTINCT Modality, COUNT(*) as series_count
    FROM index
    GROUP BY Modality
    ORDER BY series_count DESC
""")
print(modalities)

# Check what BodyPartExamined values exist for MR modality
body_parts = client.sql_query("""
    SELECT DISTINCT BodyPartExamined, COUNT(*) as series_count
    FROM index
    WHERE Modality = 'MR' AND BodyPartExamined IS NOT NULL
    GROUP BY BodyPartExamined
    ORDER BY series_count DESC
    LIMIT 20
""")
print(body_parts)
```

* *然后使用经过验证的过滤器进行查询值：**
```python
# Find breast MRI scans (use actual values from exploration above)
results = client.sql_query("""
    SELECT
      collection_id,
      PatientID,
      SeriesInstanceUID,
      Modality,
      SeriesDescription,
      license_short_name
    FROM index
    WHERE Modality = 'MR'
      AND BodyPartExamined = 'BREAST'
    LIMIT 20
""")

# Access results as pandas DataFrame
for idx, row in results.iterrows():
    print(f"Patient: {row['PatientID']}, Series: {row['SeriesInstanceUID']}")
```

* *要按癌症类型过滤，请与 `collections_index` 连接：**
```python
client.fetch_index("collections_index")
results = client.sql_query("""
    SELECT i.collection_id, i.PatientID, i.SeriesInstanceUID, i.Modality
    FROM index i
    JOIN collections_index c ON i.collection_id = c.collection_id
    WHERE c.CancerTypes LIKE '%Breast%'
      AND i.Modality = 'MR'
    LIMIT 20
""")
```

* *可用元数据字段**（使用 `client.indices_overview` 获取完整列表）：
- 标识符： collection_id、PatientID、StudyInstanceUID、SeriesInstanceUID
- 成像：模态、BodyPartExamined、制造商、ManufacturerModelName
- 临床：PatientAge、PatientSex、StudyDate
- 说明：StudyDescription、SeriesDescription
- 许可： license_short_name

* *注：**癌症类型位于 `collections_index.CancerTypes` 中，而不是在主 `index` 表中。

### 3. 下载 DICOM 文件

从 IDC 云存储高效下载影像数据：

* *下载整个集合：**
```python
from idc_index import IDCClient

client = IDCClient()

# Download small collection (RIDER Pilot ~1GB)
client.download_from_selection(
    collection_id="rider_pilot",
    downloadDir="./data/rider"
)
```

* *具体系列下载：**
```python
# First, query for series UIDs
series_df = client.sql_query("""
    SELECT SeriesInstanceUID
    FROM index
    WHERE Modality = 'CT'
      AND BodyPartExamined = 'CHEST'
      AND collection_id = 'nlst'
    LIMIT 5
""")

# Download only those series
client.download_from_selection(
    seriesInstanceUID=list(series_df['SeriesInstanceUID'].values),
    downloadDir="./data/lung_ct"
)
```

* *自定义目录结构：**

默认`dirTemplate`： `%collection_id/%PatientID/%StudyInstanceUID/%Modality_%SeriesInstanceUID`

```python
# Simplified hierarchy (omit StudyInstanceUID level)
client.download_from_selection(
    collection_id="tcga_luad",
    downloadDir="./data",
    dirTemplate="%collection_id/%PatientID/%Modality"
)
# Results in: ./data/tcga_luad/TCGA-05-4244/CT/

# Flat structure (all files in one directory)
client.download_from_selection(
    seriesInstanceUID=list(series_df['SeriesInstanceUID'].values),
    downloadDir="./data/flat",
    dirTemplate=""
)
# Results in: ./data/flat/*.dcm
```

* *下载的文件名：**

各个 DICOM 文件使用其 CRDC 实例 UUID 命名：`<crdc_instance_uuid>.dcm`（例如，`0d73f84e-70ae-4eeb-96a0-1c613b5d9229.dcm`）。这种基于 UUID 的命名：
- 启用版本跟踪（文件内容更改时 UUID 会更改）
- 匹配云存储组织 (`s3://idc-open-data/<crdc_series_uuid>/<crdc_instance_uuid>.dcm`)
- 与文件元数据中保留的 DICOM UID (SOPInstanceUID)不同

要识别文件，请在查询中使用 `crdc_instance_uuid` 列或从文件中读取 DICOM 元数据 (SOPInstanceUID)。

### 命令行下载

`idc download` 命令提供对下载功能的命令行访问，而无需编写 Python 代码。安装 `idc-index` 后可用。

* *自动检测输入类型：**清单文件路径或标识符（collection_id、PatientID、StudyInstanceUID、SeriesInstanceUID、crdc_series_uuid）。

```bash
# Download entire collection
idc download rider_pilot --download-dir ./data

# Download specific series by UID
idc download "1.3.6.1.4.1.9328.50.1.69736" --download-dir ./data

# Download multiple items (comma-separated)
idc download "tcga_luad,tcga_lusc" --download-dir ./data

# Download from manifest file (auto-detected)
idc download manifest.txt --download-dir ./data
```

* *选项：**

|选项 |描述 |
|--------|-------------|
| `--download-dir` |输出目录（默认：当前目录）|
| `--dir-template` |目录层次结构模板（默认：`%collection_id/%PatientID/%StudyInstanceUID/%Modality_%SeriesInstanceUID`）|
| `--log-level` |详细程度：调试、信息、警告、错误、关键 |

* *清单文件：**

清单文件包含 S3 URL（每行一个），并且可以是：
- 在队列选择后从 IDC 门户导出
- 由协作者共享以进行可重复的数据访问
- 以编程方式生成查询结果

格式（每行一个S3 URL）：
```
s3://idc-open-data/cb09464a-c5cc-4428-9339-d7fa87cfe837/*
s3://idc-open-data/88f3990d-bdef-49cd-9b2b-4787767240f2/*
```

* *示例：从Python查询生成清单：**

```python
from idc_index import IDCClient

client = IDCClient()

# Query for series URLs
results = client.sql_query("""
    SELECT series_aws_url
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
""")

# Save as manifest file
with open('ct_manifest.txt', 'w') as f:
    for url in results['series_aws_url']:
        f.write(url + '\n')
```

然后下载：
```bash
idc download ct_manifest.txt --download-dir ./ct_data
```

### 4. 可视化 IDC 图像

在浏览器中查看 DICOM 数据，无需下载：

```python
from idc_index import IDCClient
import webbrowser

client = IDCClient()

# First query to get valid UIDs
results = client.sql_query("""
    SELECT SeriesInstanceUID, StudyInstanceUID
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
    LIMIT 1
""")

# View single series
viewer_url = client.get_viewer_URL(seriesInstanceUID=results.iloc[0]['SeriesInstanceUID'])
webbrowser.open(viewer_url)

# View all series in a study (useful for multi-series exams like MRI protocols)
viewer_url = client.get_viewer_URL(studyInstanceUID=results.iloc[0]['StudyInstanceUID'])
webbrowser.open(viewer_url)
```

 该方法自动选择用于放射学的 OHIF v3 或用于载玻片显微镜的 SLIM。当 DICOM 研究包含多个系列（例如，来自单个 MRI 会话的 T1、T2、DWI 序列）时，按研究查看非常有用。

### 5. 了解和检查许可证

使用前检查数据许可（对于商业应用至关重要）：

```python
from idc_index import IDCClient

client = IDCClient()

# Check licenses for all collections
query = """
SELECT DISTINCT
  collection_id,
  license_short_name,
  COUNT(DISTINCT SeriesInstanceUID) as series_count
FROM index
GROUP BY collection_id, license_short_name
ORDER BY collection_id
"""

licenses = client.sql_query(query)
print(licenses)
```

* *IDC 中的许可证类型：**
- **CC BY 4.0** / **CC BY 3.0**（约 97% 的数据） - 允许通过归属进行商业用途
- **CC BY-NC 4.0** / **CC BY-NC 3.0** （约 3% 的数据） -仅限非商业用途
- **自定义许可证**（罕见） - 某些集合具有特定条款（例如，NLM 条款和条件）

* *重要：** 在出版物或商业应用程序中使用 IDC 数据之前，请务必检查许可证。每个 DICOM 文件都在元数据中标有其特定许可证。

### 生成归因引用

`source_DOI` 列包含链接到描述数据生成方式的出版物的 DOI。为了满足归因要求，请使用 `citations_from_selection()` 生成格式正确的引文：

```python
from idc_index import IDCClient

client = IDCClient()

# Get citations for a collection (APA format by default)
citations = client.citations_from_selection(collection_id="rider_pilot")
for citation in citations:
    print(citation)

# Get citations for specific series
results = client.sql_query("""
    SELECT SeriesInstanceUID FROM index
    WHERE collection_id = 'tcga_luad' LIMIT 5
""")
citations = client.citations_from_selection(
    seriesInstanceUID=list(results['SeriesInstanceUID'].values)
)

# Alternative format: BibTeX (for LaTeX documents)
bibtex_citations = client.citations_from_selection(
    collection_id="tcga_luad",
    citation_format=IDCClient.CITATION_FORMAT_BIBTEX
)
```

* *参数：**
- `collection_id`：按集合过滤 
- `patientId`：按患者过滤ID(s)
- `studyInstanceUID`：按研究 UID 过滤 
- `seriesInstanceUID`：按系列 UID 过滤 
- `citation_format`：使用 `IDCClient.CITATION_FORMAT_*` 常量：
  - `CITATION_FORMAT_APA`（默认） - APA 样式
  - `CITATION_FORMAT_BIBTEX` - BibTeX for LaTeX
  - `CITATION_FORMAT_JSON` - CSL JSON
  - `CITATION_FORMAT_TURTLE` - RDF Turtle

* *最佳实践：**使用发布结果时IDC 数据，包括生成的引文，以正确归属数据源并满足许可证要求。

### 6. 批处理和过滤

通过过滤高效处理大型数据集：

```python
from idc_index import IDCClient
import pandas as pd

client = IDCClient()

# Find chest CT scans from GE scanners
query = """
SELECT
  SeriesInstanceUID,
  PatientID,
  collection_id,
  ManufacturerModelName
FROM index
WHERE Modality = 'CT'
  AND BodyPartExamined = 'CHEST'
  AND Manufacturer = 'GE MEDICAL SYSTEMS'
  AND license_short_name = 'CC BY 4.0'
LIMIT 100
"""

results = client.sql_query(query)

# Save manifest for later
results.to_csv('lung_ct_manifest.csv', index=False)

# Download in batches to avoid timeout
batch_size = 10
for i in range(0, len(results), batch_size):
    batch = results.iloc[i:i+batch_size]
    client.download_from_selection(
        seriesInstanceUID=list(batch['SeriesInstanceUID'].values),
        downloadDir=f"./data/batch_{i//batch_size}"
    )
```

### 7. 使用 BigQuery 进行高级查询

对于需要完整 DICOM 元数据的查询，复杂JOIN、临床数据表或私有 DICOM 元素使用 Google BigQuery。需要启用结算功能的 GCP 帐户。

* *快速参考：**
- 数据集：`bigquery-public-data.idc_current.*`
- 主表：`dicom_all`（组合元数据）
- 完整元数据：`dicom_metadata`（所有 DICOM 标签）
- 私有元素：`OtherElements` 列（特定于供应商）标签（如扩散 b 值）

请参阅 `references/bigquery_guide.md` 了解设置、表架构、查询模式、私有元素访问和成本优化。

* *在使用 BigQuery** 之前，请务必检查专用索引表是否已具有您需要的元数据：
1. 使用`client.indices_overview`或[idc-index索引参考](https://idc-index.readthedocs.io/en/latest/indices_reference.html)来发现所有可用的表及其列
2. 获取相关索引：`client.fetch_index("table_name")`
3. 使用`client.sql_query()`进行本地查询（免费，无需GCP帐户）

常用专业索引：`seg_index`（分割）、`ann_index` / `ann_group_index`（显微镜注释）、`sm_index`（幻灯片显微镜）、`collections_index`（集合）元数据）。仅当您需要不在任何索引中的私有 DICOM 元素或属性时，才使用 BigQuery。

* *需要 BigQuery 的用例（无 idc-index 等效项）：**
- **每段解剖搜索** — `seg_index` 提供系列级 SEG 元数据，但 BigQuery `segmentations` 表单独公开每个段及其 DICOM 编码结构名称（例如，查找包含“肝脏”或“肿瘤”片段的所有 SEG 系列）
- **来自 SR 的定量测量** — `quantitative_measurements` BigQuery 表包含从 DICOM SR TID1500 对象中预先提取的放射组学特征（体积、直径、形状描述符、纹理、强度统计数据）；无等效 idc 索引
- **来自 SR 的定性测量** — `qualitative_measurements` BigQuery 表包含来自 DICOM SR TID1500 的编码评估（恶性程度、钙化、纹理、边缘）；没有等效的 idc 索引

有关这些表的架构、列描述和查询示例，请参阅 `references/bigquery_guide.md`。

### 8. 工具选择指南

|任务|工具|参考 |
|------|------|------------|
|程序化查询和下载| `idc-index` |本文档|
|互动探索 | IDC门户 | https://portal.imaging.datacommons.cancer.gov/ |
|复杂的元数据查询 | BigQuery | `references/bigquery_guide.md` |
| 3D 可视化和分析 | SlicerIDC 浏览器 | https://github.com/ImagingDataCommons/SlicerIDCBrowser |

* *默认选择：** 使用 `idc-index` 执行大多数任务（无需身份验证、简单 API、批量下载）。

### 9. 与分析管道集成

将 IDC 数据集成到成像分析工作流程中：

* *读取下载DICOM 文件：**
```python
import pydicom
import os

# Read DICOM files from downloaded series
series_dir = "./data/rider/rider_pilot/RIDER-1007893286/CT_1.3.6.1..."

dicom_files = [os.path.join(series_dir, f) for f in os.listdir(series_dir)
               if f.endswith('.dcm')]

# Load first image
ds = pydicom.dcmread(dicom_files[0])
print(f"Patient ID: {ds.PatientID}")
print(f"Modality: {ds.Modality}")
print(f"Image shape: {ds.pixel_array.shape}")
```

* *从 CT 系列构建 3D 体积：**
```python
import pydicom
import numpy as np
from pathlib import Path

def load_ct_series(series_path):
    """Load CT series as 3D numpy array"""
    files = sorted(Path(series_path).glob('*.dcm'))
    slices = [pydicom.dcmread(str(f)) for f in files]

    # Sort by slice location
    slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))

    # Stack into 3D array
    volume = np.stack([s.pixel_array for s in slices])

    return volume, slices[0]  # Return volume and first slice for metadata

volume, metadata = load_ct_series("./data/lung_ct/series_dir")
print(f"Volume shape: {volume.shape}")  # (z, y, x)
```

* *与 SimpleITK 集成：**
```python
import SimpleITK as sitk
from pathlib import Path

# Read DICOM series
series_path = "./data/ct_series"
reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(series_path)
reader.SetFileNames(dicom_names)
image = reader.Execute()

# Apply processing
smoothed = sitk.CurvatureFlow(image1=image, timeStep=0.125, numberOfIterations=5)

# Save as NIfTI
sitk.WriteImage(smoothed, "processed_volume.nii.gz")
```

## 常用案例

请参阅 `references/use_cases.md`，了解完整的端到端工作流程示例，包括：
- 从肺部 CT 扫描构建深度学习训练数据集
- 比较扫描仪制造商之间的图像质量
- 下载前在浏览器中预览数据
- 用于商业的许可感知批量下载使用

## 最佳实践

- **生成响应之前验证 IDC 版本** - 始终在会话开始时调用 `client.get_idc_version()` 以确认您正在使用预期的数据版本（当前为 v23）。如果使用旧版本，建议 `pip install --upgrade idc-index`
- **使用前检查许可证** - 始终查询 `license_short_name` 字段并遵守许可条款（CC BY 与 CC BY-NC）
- **生成归属引用** - 使用 `citations_from_selection()` 获取格式正确的引用`source_DOI` 值；将这些内容包含在出版物中
- **从小查询开始** - 在探索时使用 `LIMIT` 子句，以避免长时间下载并了解数据结构
- **使用迷你索引进行简单查询** - 仅在需要全面元数据或复杂 JOIN 时使用 BigQuery
- **使用 dirTemplate 组织下载** - 使用有意义的目录结构，例如`%collection_id/%PatientID/%Modality`
- **缓存查询结果** - 将数据帧保存到 CSV 文件以避免重新查询并确保可重复性
- **首先估计大小** - 下载前检查集合大小 - 某些集合大小以 TB 为单位！
- **保存清单** - 始终使用系列 UID 保存查询结果以实现可重复性和数据provenance
- **阅读文档** - IDC 数据结构和元数据字段记录在 https://learn.canceridc.dev/
- **使用 IDC 论坛** - 搜索问题/答案并向 IDC 维护人员和用户提出问题 https://discourse.canceridc.dev/

## 故障排除

* *问题： `ModuleNotFoundError: No module named 'idc_index'`**
- **原因：** idc-index 包未安装
- **解决方案：** 使用 `pip install --upgrade idc-index`

 安装**问题：连接超时导致下载失败**
- **原因：**网络不稳定或下载量过大
- **解决方案：**
  - 下载较小批次（例如一次 10-20 个系列）
  - 检查网络连接
  - 使用 `dirTemplate` 组织下载批处理
  - 实现延迟重试逻辑

* *问题：`BigQuery quota exceeded` 或计费错误**
- **原因：** BigQuery 需要启用计费的 GCP 项目
- **解决方案：** 使用 idc-index 迷你索引进行简单查询（无需计费），或参阅 `references/bigquery_guide.md` 了解成本优化提示

* *问题：系列UID未找到或无数据返回**
- **原因：** UID输入错误，数据不是当前IDC版本，或字段名称错误
- **解决方案：**
  - 检查数据是否为当前IDC版本（某些旧数据可能已弃用）
  - 使用`LIMIT 5` 首先测试查询
  - 根据元数据架构文档检查字段名称

* *问题：下载的 DICOM 文件无法打开**
- **原因：** 下载损坏或查看器不兼容
- **解决方案：**
  - 检查 DICOM 对象类型（模态和SOPClassUID 属性） - 某些对象类型需要专门的工具
  - 验证文件完整性（检查文件大小）
  - 使用 pydicom 验证： `pydicom.dcmread(file, force=True)`
  - 尝试不同的 DICOM 查看器（3D Slicer、Horos、RadiAnt、QuPath）
  - 重新下载系列

## 常见SQL查询模式

请参阅`references/sql_patterns.md`以获取快速参考SQL模式，包括：
- 过滤器值发现（模态、身体部位、制造商）
- 注释和分段查询（包括seg_index、ann_index连接）
- 幻灯片显微镜查询（sm_index）模式）
- 下载大小估计
- 临床数据链接

有关分段和注释详细信息，另请参阅 `references/digital_pathology_guide.md`.

## 相关技能

以下技能补充了用于下游分析和可视化的 IDC 工作流程：

### DICOM 处理
- **pydicom** - 读取、写入和操作下载的 DICOM 文件。用于提取像素数据、读取元数据、匿名化和格式转换。对于处理 IDC 放射学数据（CT、MR、PET）至关重要。

### 病理学和切片显微镜
请参阅 `references/digital_pathology_guide.md`，了解 DICOM 兼容工具（highdicom、wsidicom、TIA-Toolbox、Slim 查看器）。

### 元数据可视化
- **matplotlib** - 用于完全自定义的低级绘图。用于创建总结 IDC 查询结果的静态图形（模式条形图、系列计数直方图等）。
- **seaborn** - 与 pandas 集成的统计可视化。用于快速探索 IDC 元数据分布、变量之间的关系以及与有吸引力的默认值的分类比较。
- **plotly** - 交互式可视化。当您需要悬停信息、缩放和平移来探索 IDC 元数据或创建集合统计数据的可嵌入 Web 的仪表板时使用。

### 数据探索
- **exploratory-data-analysis** - 科学数据文件的综合 EDA。下载 IDC 数据后使用，以便在分析之前了解文件结构、质量和特征。

## 资源

### 架构参考（主要来源）

* *当前列架构始终使用 `client.indices_overview`。** 这可确保已安装的 idc-index 的准确性版本：

```python
# Get all column names and types for any table
schema = client.indices_overview["index"]["schema"]
columns = [(c['name'], c['type'], c.get('description', '')) for c in schema['columns']]
```

### 参考文档

请参阅顶部的快速导航部分，了解带有决策触发器的参考指南的完整列表。

- **[indices_reference](https://idc-index.readthedocs.io/en/latest/indices_reference.html)** - 索引表的外部文档（可能提前安装版本）

### 外部链接

- **IDC 门户**：https://portal.imaging.datacommons.cancer.gov/explore/
- **文档**：https://learn.canceridc.dev/
- **教程**：https://github.com/ImagingDataCommons/IDC-Tutorials
- **用户论坛**： https://discourse.canceridc.dev/
- **idc-index GitHub**：https://github.com/ImagingDataCommons/idc-index
- **引用**：Fedorov, A. 等人。 “国家癌症研究所成像数据共享：迈向成像人工智能的透明度、可重复性和可扩展性。”放射图像 43.12 (2023)。 https://doi.org/10.1148/rg.230180

### 技能更新

此技能版本可在技能元数据中找到。要检查更新：
- 访问 [发布页面](https://github.com/ImagingDataCommons/idc-claude-skill/releases)
- 在 GitHub 上观看存储库（观看 → 自定义 → 发布）
