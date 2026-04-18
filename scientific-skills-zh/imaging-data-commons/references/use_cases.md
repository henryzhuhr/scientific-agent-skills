# IDC

的常见用例**测试使用：** idc-index 0.11.9（IDC 数据版本 v23）

本指南为常见 IDC 用例提供完整的端到端工作流程示例。每个用例都展示了从查询到下载的完整工作流程以及最佳实践。

## 何时使用本指南

在需要时加载本指南：
- 用于训练数据集创建的完整端到端工作流程示例
- 多步骤数据选择和下载工作流程的模式
- 商业用途的许可证感知数据处理示例
- 可视化下载前数据预览的工作流程

有关核心 API 模式（查询、下载、可视化、引用），请参阅主 SKILL.md 中的“核心功能”部分。

## 先决条件

```bash
pip install --upgrade idc-index
```

## 用例 1：查找并下载肺部 CT 扫描进行深度扫描学习

* *目标：**从 NLST 集合中构建肺部 CT 扫描的训练数据集

* *步骤：**
```python
from idc_index import IDCClient

client = IDCClient()

# 1. Query for lung CT scans with specific criteria
query = """
SELECT
  PatientID,
  SeriesInstanceUID,
  SeriesDescription
FROM index
WHERE collection_id = 'nlst'
  AND Modality = 'CT'
  AND BodyPartExamined = 'CHEST'
  AND license_short_name = 'CC BY 4.0'
ORDER BY PatientID
LIMIT 100
"""

results = client.sql_query(query)
print(f"Found {len(results)} series from {results['PatientID'].nunique()} patients")

# 2. Download data organized by patient
client.download_from_selection(
    seriesInstanceUID=list(results['SeriesInstanceUID'].values),
    downloadDir="./training_data",
    dirTemplate="%collection_id/%PatientID/%SeriesInstanceUID"
)

# 3. Save manifest for reproducibility
results.to_csv('training_manifest.csv', index=False)
```

## 用例 2：按制造商查询脑 MRI 进行质量研究

* *目标：**比较不同 MRI 扫描仪的图像质量制造商

* *步骤：**
```python
from idc_index import IDCClient
import pandas as pd

client = IDCClient()

# Query for brain MRI grouped by manufacturer
query = """
SELECT
  Manufacturer,
  ManufacturerModelName,
  COUNT(DISTINCT SeriesInstanceUID) as num_series,
  COUNT(DISTINCT PatientID) as num_patients
FROM index
WHERE Modality = 'MR'
  AND BodyPartExamined LIKE '%BRAIN%'
GROUP BY Manufacturer, ManufacturerModelName
HAVING num_series >= 10
ORDER BY num_series DESC
"""

manufacturers = client.sql_query(query)
print(manufacturers)

# Download sample from each manufacturer for comparison
for _, row in manufacturers.head(3).iterrows():
    mfr = row['Manufacturer']
    model = row['ManufacturerModelName']

    query = f"""
    SELECT SeriesInstanceUID
    FROM index
    WHERE Manufacturer = '{mfr}'
      AND ManufacturerModelName = '{model}'
      AND Modality = 'MR'
      AND BodyPartExamined LIKE '%BRAIN%'
    LIMIT 5
    """

    series = client.sql_query(query)
    client.download_from_selection(
        seriesInstanceUID=list(series['SeriesInstanceUID'].values),
        downloadDir=f"./quality_study/{mfr.replace(' ', '_')}"
    )
```

## 用例3：在不下载的情况下可视化系列

* *目标：**在提交下载之前预览成像数据

```python
from idc_index import IDCClient
import webbrowser

client = IDCClient()

series_list = client.sql_query("""
    SELECT SeriesInstanceUID, PatientID, SeriesDescription
    FROM index
    WHERE collection_id = 'acrin_nsclc_fdg_pet' AND Modality = 'PT'
    LIMIT 10
""")

# Preview each in browser
for _, row in series_list.iterrows():
    viewer_url = client.get_viewer_URL(seriesInstanceUID=row['SeriesInstanceUID'])
    print(f"Patient {row['PatientID']}: {row['SeriesDescription']}")
    print(f"  View at: {viewer_url}")
    # webbrowser.open(viewer_url)  # Uncomment to open automatically
```

有关其他可视化选项，请参阅[IDC门户入门用于 3D Slicer 集成的 [指南](https://learn.canceridc.dev/portal/getting-started)或 [SlicerIDCBrowser](https://github.com/ImagingDataCommons/SlicerIDCBrowser)。

## 使用案例 4：用于商业用途的许可感知批量下载

* *目标：** 仅下载适合商业用途的 CC-BY 许可数据应用程序

* *步骤：**
```python
from idc_index import IDCClient

client = IDCClient()

# Query ONLY for CC BY licensed data (allows commercial use with attribution)
query = """
SELECT
  SeriesInstanceUID,
  collection_id,
  PatientID,
  Modality
FROM index
WHERE license_short_name LIKE 'CC BY%'
  AND license_short_name NOT LIKE '%NC%'
  AND Modality IN ('CT', 'MR')
  AND BodyPartExamined IN ('CHEST', 'BRAIN', 'ABDOMEN')
LIMIT 200
"""

cc_by_data = client.sql_query(query)

print(f"Found {len(cc_by_data)} CC BY licensed series")
print(f"Collections: {cc_by_data['collection_id'].unique()}")

# Download with license verification
client.download_from_selection(
    seriesInstanceUID=list(cc_by_data['SeriesInstanceUID'].values),
    downloadDir="./commercial_dataset",
    dirTemplate="%collection_id/%Modality/%PatientID/%SeriesInstanceUID"
)

# Save license information
cc_by_data.to_csv('commercial_dataset_manifest_CC-BY_ONLY.csv', index=False)
```

## 资源

- 主要 SKILL.md 用于核心 API 模式（查询、下载、可视化）
- `references/clinical_data_guide.md` 用于临床数据集成工作流程
- `references/sql_patterns.md` 用于其他 SQL 查询模式
- `references/index_tables_guide.md` 用于复杂连接模式
