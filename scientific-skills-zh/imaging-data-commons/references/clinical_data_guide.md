# IDC

临床数据指南**测试使用：** idc-index 0.11.7（IDC 数据版本 v23）

 临床数据（人口统计、诊断、治疗、实验室测试、分期）伴随着许多 IDC 影像收集。本指南介绍了如何使用 `idc-index`.

## 何时使用本指南

在需要时使用本指南：
- 查找可用于集合的临床元数据
- 按临床标准（例如，癌症分期、治疗史）筛选患者
- 将临床属性与影像数据连接起来队列选择
- 理解和解码临床表中的编码值

有关基本临床数据访问，请参阅主SKILL.md中的“临床数据访问”部分。本指南提供了详细的工作流程和高级模式。

## 先决条件

```bash
pip install --upgrade idc-index
```

无需 BigQuery 凭据 - 临床数据与 `idc-index` 打包在一起。

## 了解 IDC 中的临床数据

### 什么是临床数据？

临床数据指的是医学图像附带的非影像信息：
- 患者人口统计（年龄、性别、种族）
- 临床病史（诊断、手术、治疗）
- 实验室测试和病理结果
- 癌症分期（临床和病理）
- 治疗结果

### 数据组织

IDC中的临床数据来自数据提交者提供的特定集合的电子表格。 IDC 将这些解析为可通过 `idc-index`.

 访问的可查询表**重要特征：**
- 临床数据在集合之间**不协调**（术语和格式有所不同）
- 并非所有集合都有临床数据（首先检查可用性）
- 所有数据都是**匿名** - `dicom_patient_id`成像链接

### 临床索引表

`clinical_index` 用作所有可用临床数据的字典/目录：

|专栏 |目的|用于 |
|--------|---------|---------|
| `collection_id` |集合标识符|按集合过滤|
| `table_name` |完整的 BigQuery 表参考 | BigQuery 查询（如果需要）|
| `short_table_name` |简称| `get_clinical_table()`方法|
| `column` |表中的列名 |选择数据列|
| `column_label` |人类可读的描述 |搜索概念 |
| `values` |观察到的列的属性值 |解释编码值 |

### `values` 列

`values` 列包含 `column` 字段中定义的列的观察属性值数组。每个条目都有：
- **option_code**：在该列中观察到的实际值
- **option_description**：该值的人类可读描述（如果可用，则来自数据字典，否则为 `None`）

 对于 ACRIN 集合，值描述来自提供的数据字典。对于其他集合，它们是通过检查实际数据值得出的。

* *注意：** 对于具有 >20 个唯一值的列，为简单起见，`values` 数组留空 (`[]`)。

## 核心工作流程

### 步骤 1：获取临床Index

```python
from idc_index import IDCClient

client = IDCClient()
client.fetch_index('clinical_index')

# View available columns
print(client.clinical_index.columns.tolist())
```

### 步骤 2：发现可用临床数据

```python
# List all collections with clinical data
collections_with_clinical = client.clinical_index["collection_id"].unique().tolist()
print(f"{len(collections_with_clinical)} collections have clinical data")

# Find clinical attributes for a specific collection
nlst_columns = client.clinical_index[client.clinical_index['collection_id']=='nlst']
nlst_columns[['short_table_name', 'column', 'column_label', 'values']]
```

### 步骤 3：搜索特定属性

```python
# Search by keyword in column_label (case-insensitive)
stage_attrs = client.clinical_index[
    client.clinical_index["column_label"].str.contains("[Ss]tage", na=False)
]
stage_attrs[["collection_id", "short_table_name", "column", "column_label"]]
```

### 步骤 4：加载临床数据表

```python
# Load table using short_table_name
nlst_canc_df = client.get_clinical_table("nlst_canc")

# Examine structure
print(f"Rows: {len(nlst_canc_df)}, Columns: {len(nlst_canc_df.columns)}")
nlst_canc_df.head()
```

### 步骤5：将编码值映射到描述

许多临床属性使用编码值。 `clinical_index` 中的 `values` 列包含一组观察值及其描述（如果可用）。

```python
# Get the clinical_index rows for NLST
nlst_clinical_columns = client.clinical_index[client.clinical_index['collection_id']=='nlst']

# Get observed values for a specific column
# Filter to the row for 'clinical_stag' and extract the values array
clinical_stag_values = nlst_clinical_columns[
    nlst_clinical_columns['column']=='clinical_stag'
]['values'].values[0]

# View the observed values and their descriptions
print(clinical_stag_values)
# Output: array([{'option_code': '.M', 'option_description': 'Missing'},
#                {'option_code': '110', 'option_description': 'Stage IA'},
#                {'option_code': '120', 'option_description': 'Stage IB'}, ...])

# Create mapping dictionary from codes to descriptions
mapping_dict = {item['option_code']: item['option_description'] for item in clinical_stag_values}

# Apply to DataFrame - convert column to string first for consistent matching
nlst_canc_df['clinical_stag_meaning'] = nlst_canc_df['clinical_stag'].astype(str).map(mapping_dict)
```

### 步骤 6：与影像数据连接

`dicom_patient_id` 列将临床数据与影像联系起来。它与成像索引中的 `PatientID` 列匹配。

```python
# Pandas merge approach
import pandas as pd

# Get NLST CT imaging data
nlst_imaging = client.index[(client.index['collection_id']=='nlst') & (client.index['Modality']=='CT')]

# Join with clinical data
merged = pd.merge(
    nlst_imaging[['PatientID', 'StudyInstanceUID']].drop_duplicates(),
    nlst_canc_df[['dicom_patient_id', 'clinical_stag', 'clinical_stag_meaning']],
    left_on='PatientID',
    right_on='dicom_patient_id',
    how='inner'
)
```

```python
# SQL join approach
# Clinical tables loaded via get_clinical_table() are not automatically
# registered in DuckDB. Register the DataFrame manually before joining.
nlst_canc_df = client.get_clinical_table("nlst_canc")
client._duckdb_conn.register("nlst_canc", nlst_canc_df)

query = """
SELECT
  index.PatientID,
  index.StudyInstanceUID,
  index.Modality,
  nlst_canc.clinical_stag
FROM index
JOIN nlst_canc ON index.PatientID = nlst_canc.dicom_patient_id
WHERE index.collection_id = 'nlst' AND index.Modality = 'CT'
"""
results = client.sql_query(query)
```

## 常见用例

### 使用案例 1：按癌症分期选择患者

```python
from idc_index import IDCClient
import pandas as pd

client = IDCClient()
client.fetch_index('clinical_index')

# Load clinical table
nlst_canc = client.get_clinical_table("nlst_canc")

# Select Stage IV patients (code '400')
stage_iv_patients = nlst_canc[nlst_canc['clinical_stag'] == '400']['dicom_patient_id']

# Get CT imaging studies for these patients
stage_iv_studies = pd.merge(
    client.index[(client.index['collection_id']=='nlst') & (client.index['Modality']=='CT')],
    stage_iv_patients,
    left_on='PatientID',
    right_on='dicom_patient_id',
    how='inner'
)['StudyInstanceUID'].drop_duplicates()

print(f"Found {len(stage_iv_studies)} CT studies for Stage IV patients")
```

### 使用案例 2：查找具有特定临床属性的集合

```python
# Find collections with chemotherapy information
chemo_collections = client.clinical_index[
    client.clinical_index["column_label"].str.contains("[Cc]hemotherapy", na=False)
]["collection_id"].unique()

print(f"Collections with chemotherapy data: {list(chemo_collections)}")
```

### 使用案例 3：检查临床观察值属性

```python
# Find what values have been observed for a specific attribute
chemotherapy_rows = client.clinical_index[
    (client.clinical_index["collection_id"] == "hcc_tace_seg") &
    (client.clinical_index["column"] == "chemotherapy")
]

# Get the observed values array
values_list = chemotherapy_rows["values"].tolist()
print(values_list)
# Output: [[{'option_code': 'Cisplastin', 'option_description': None},
#           {'option_code': 'Cisplatin, Mitomycin-C', 'option_description': None}, ...]]
```

### 用例4：为选定患者生成查看器URL

```python
import random

# Get studies for a sample Stage IV patient
sample_patient = stage_iv_patients.iloc[0]
studies = client.index[client.index['PatientID'] == sample_patient]['StudyInstanceUID'].unique()

# Generate viewer URL
if len(studies) > 0:
    viewer_url = client.get_viewer_URL(studyInstanceUID=studies[0])
    print(viewer_url)
```

## 关键概念

### 列与column_label

- **列**：用于从表中选择数据（编程）访问）
- **column_label**：用于搜索/理解数据的含义（人类可读）

一些集合（如`c4kc_kits`）具有相同的列和column_label。其他（如 ACRIN 集合）具有神秘的列名称，但有描述性标签。

### option_code 与 option_description

`values` 数组包含观察到的属性值：
- **option_code**：在列中观察到的实际值（您过滤的内容）
- **option_description**：人类可读的描述（如果可用，则来自数据字典，否则为 `None`）

### dicom_ Patient_id

每个临床表都包含 `dicom_patient_id`，它与成像索引中的 `PatientID` 列相匹配。这是连接临床和影像数据的关键。

## 故障排除

### 问题：找不到临床表

* *原因：**使用了错误的表名或集合不存在表

* *解决方案：**首先查询clinical_index以查找可用的表：
```python
client.clinical_index[client.clinical_index['collection_id']=='your_collection']['short_table_name'].unique()
```

### 问题：空值数组

* *原因：** 当列具有 >20 个唯一值时，`values` 数组留空

* *解决方案：** 加载临床表并检查唯一值直接：
```python
clinical_df = client.get_clinical_table("table_name")
clinical_df['column_name'].unique()
```

### 问题：编码值不在映射中

* *原因：** 字典中可能缺少某些值（例如，空字符串、`.M` 等特殊代码表示缺少）

* *解决方案：** 优雅地处理未映射的值：
```python
df['meaning'] = df['code'].astype(str).map(mapping_dict).fillna('Unknown/Missing')
```

### 问题：加入时没有匹配的患者

 * *原因：** 临床数据可能包括没有图像的患者，反之亦然

  * *解决方案：** 之前验证患者重叠加入：
```python
imaging_patients = set(client.index[client.index['collection_id']=='nlst']['PatientID'].unique())
clinical_patients = set(clinical_df['dicom_patient_id'].unique())
overlap = imaging_patients & clinical_patients
print(f"Patients with both imaging and clinical data: {len(overlap)}")
```

## 资源

* *IDC 文档：**
- [临床数据组织](https://learn.canceridc.dev/data/organization-of-data/clinical) - IDC
- [临床数据]中临床数据的组织方式仪表板](https://datastudio.google.com/u/0/reporting/04cf5976-4ea0-4fee-a749-8bfd162f2e87/page/p_s7mk6eybqc) - 可用临床数据的可视化摘要
- [idc-index Clinical_index文档](https://idc-index.readthedocs.io/en/latest/column_descriptions.html#clinical-index)

* *相关指南：**
- `bigquery_guide.md` - 通过 BigQuery 进行高级临床查询
- Main SKILL.md - 核心 IDC 工作流程

* *IDC教程：**
- [clinical_data_intro.ipynb](https://github.com/ImagingDataCommons/IDC-Tutorials/blob/master/notebooks/advanced_topics/clinical_data_intro.ipynb)
- [exploring_clinical_data.ipynb](https://github.com/ImagingDataCommons/IDC-Tutorials/blob/master/notebooks/getting_started/exploring_clinical_data.ipynb)
- [nlst_clinical_data.ipynb](https://github.com/ImagingDataCommons/IDC-Tutorials/blob/master/notebooks/collections_demos/nlst_clinical_data.ipynb)
