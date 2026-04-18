# IDC

的 BigQuery 指南**测试使用：** IDC 数据版本 v23

 对于大多数查询和下载，请使用 `idc-index`（请参阅 main SKILL.md）。本指南涵盖了需要完整 DICOM 元数据或复杂联接的高级用例的 BigQuery。

## 先决条件

* *要求：**
1. 谷歌帐户
2. 已启用计费功能的 Google Cloud 项目（前 1 TB/月免费）
3. `google-cloud-bigquery` Python 包或 BigQuery 控制台访问

* *身份验证设置：**
```bash
# Install Google Cloud SDK, then:
gcloud auth application-default login
```

## 何时使用 BigQuery

在需要时使用 BigQuery 而不是 `idc-index`：
- 完整的 DICOM 元数据（所有 4000 多个标签，而不仅仅是idc-index 中的 ~50)
- 跨临床数据表的复杂连接
- DICOM 序列属性（嵌套结构）
- 查询不在 idc-index 迷你索引中的字段
- 私有 DICOM 元素（OtherElements 列中的供应商特定标签）
- **来自每个段的详细信息DICOM 分段对象** — `idc-index` `seg_index` 提供系列级元数据，但不提供单个分段解剖代码；使用 `segmentations` BigQuery 表按结构名称查询
- **来自 DICOM SR 的定量测量** — 放射组学特征（体积、直径、形状描述符），无需下载和解析 SR 文件；无 idc-index 等效项
- **来自 DICOM SR 的定性测量** — 编码评估（恶性程度、纹理、边缘），无需解析 SR 文件；无 idc-index 等效项

## 在 BigQuery 中访问 IDC

### 数据集结构

所有 IDC 表均位于 `bigquery-public-data` BigQuery 项目中。

* *当前版本（建议探索）：**
- `bigquery-public-data.idc_current.*`
- `bigquery-public-data.idc_current_clinical.*`

* *版本化数据集（建议用于再现性）：**

- `bigquery-public-data.idc_v{IDC version}.*`
- `bigquery-public-data.idc_v{IDC version}_clinical.*`

 始终使用版本化数据集以实现可再现性研究！

## 关键表

### dicom_all
连接完整 DICOM 元数据与 IDC 特定列（collection_id、gcs_url、许可证）的主表。包含 `dicom_metadata` 中的所有 DICOM 标签以及集合和管理元数据。请参阅 [dicom_all.sql](https://github.com/ImagingDataCommons/etl_flow/blob/master/bq/generate_tables_and_views/衍生_表/BQ_Table_Building/衍生_data_views/sql/dicom_all.sql)了解确切的推导。

```sql
SELECT 
  collection_id,
  PatientID,
  StudyInstanceUID, 
  SeriesInstanceUID,
  Modality,
  BodyPartExamined,
  SeriesDescription,
  gcs_url,
  license_short_name
FROM `bigquery-public-data.idc_current.dicom_all`
WHERE Modality = 'CT'
  AND BodyPartExamined = 'CHEST'
LIMIT 10
```

### 派生表

这些表源自 DICOM 对象（分段和结构化报告），并且**在 idc-index 中没有等效项**。使用它们来查询每个分段的解剖结构、放射组学特征和定性评估，而无需下载 DICOM 文件。

* *分段** — DICOM SEG 对象中每个分段一行。让您可以按解剖结构名称或 DICOM 编码概念进行搜索。 `idc-index` `seg_index` 提供系列级元数据；该表提供了每个段的详细信息。

* *measurement_groups** — 每个 SR TID1500 测量组一行。用于定量和定性测量的父分组；将测量链接到分段和源图像。

* *定量测量** — SR TID1500 组中每个数字测量一行。包含从 DICOM SR 提取的放射组学特征（体积、直径、形状描述符、纹理），无需下载或解析 SR 文件。

* *定性_测量** — SR TID1500 组中每个编码评估一行。包含使用编码概念值的评估结果（恶性可能性、纹理、边缘类型）。

有关模式、列描述和查询示例，请参阅下面的[派生表：详细文档](#衍生表详细文档)部分。

### 集合元数据

* *original_collections_metadata** - 集合级别说明

```sql
SELECT
  collection_id,
  CancerTypes,
  TumorLocations,
  Subjects,
  src.source_doi,
  src.ImageTypes,
  src.license.license_short_name
FROM `bigquery-public-data.idc_current.original_collections_metadata`,
UNNEST(Sources) AS src
WHERE CancerTypes LIKE '%Lung%'
```

## 常见查询模式

### 按条件查找集合

```sql
SELECT 
  collection_id,
  COUNT(DISTINCT PatientID) as patient_count,
  COUNT(DISTINCT SeriesInstanceUID) as series_count,
  ARRAY_AGG(DISTINCT Modality) as modalities
FROM `bigquery-public-data.idc_current.dicom_all`
WHERE BodyPartExamined LIKE '%BRAIN%'
GROUP BY collection_id
HAVING patient_count > 50
ORDER BY patient_count DESC
```

### 获取下载 URL

```sql
SELECT
  SeriesInstanceUID,
  gcs_url
FROM `bigquery-public-data.idc_current.dicom_all`
WHERE collection_id = 'rider_pilot'
  AND Modality = 'CT'
```

### 查找具有多个的研究模态

```sql
SELECT
  StudyInstanceUID,
  ARRAY_AGG(DISTINCT Modality) as modalities,
  COUNT(DISTINCT SeriesInstanceUID) as series_count
FROM `bigquery-public-data.idc_current.dicom_all`
GROUP BY StudyInstanceUID
HAVING ARRAY_LENGTH(ARRAY_AGG(DISTINCT Modality)) > 1
LIMIT 100
```

### 许可证过滤

```sql
SELECT
  collection_id,
  license_short_name,
  COUNT(*) as instance_count
FROM `bigquery-public-data.idc_current.dicom_all`
WHERE license_short_name = 'CC BY 4.0'
GROUP BY collection_id, license_short_name
```

### 使用源图像查找分段

```sql
SELECT
  src.collection_id,
  seg.SeriesInstanceUID as seg_series,
  seg.SegmentedPropertyType,
  src.SeriesInstanceUID as source_series,
  src.Modality as source_modality
FROM `bigquery-public-data.idc_current.segmentations` seg
JOIN `bigquery-public-data.idc_current.dicom_all` src
  ON seg.segmented_SeriesInstanceUID = src.SeriesInstanceUID
WHERE src.collection_id = 'qin_prostate_repeatability'
LIMIT 10
```

## 派生表：详细文档

### 分段

DICOM 分段 (SEG)对象中每个分段一行。与 `idc-index` `seg_index`（每个 SEG 系列一行）不同，此表单独公开每个标记区域，以便您可以按解剖结构或查找类型进行搜索。

* *关键列：**

|专栏 |类型 |描述|
|--------|------|-------------|
| `SeriesInstanceUID` |字符串 | SEG系列UID|
| `SOPInstanceUID` |字符串 | SEG实例UID |
| `PatientID` |字符串 |患者标识符|
| `StudyInstanceUID` |字符串 |学习UID |
| `SegmentNumber` |整数| SEG内的段索引（从1开始）|
| `SegmentedPropertyCategory` |记录|编码类别（例如“解剖结构”、“形态改变结构”）|
| `SegmentedPropertyType` |记录 |具体结构（例如“肝脏”、“肾脏”、“肿瘤”）|
| `AnatomicRegion` |记录 |可选的解剖区域修改器|
| `SegmentAlgorithmType` |字符串 |自动、半自动或手动|
| `SegmentAlgorithmName` |字符串（重复）|算法名称数组（例如，[“TotalSegmentator”]）|
| `TrackingUID` |字符串 |将段链接到 SR 测量|
| `TrackingID` |字符串 |人类可读的跟踪标签|
| `segmented_SeriesInstanceUID` |字符串 |源图像系列 UID — 加入 `dicom_all` 获取集合/模态 |
| `viewer_url` |字符串 | SEG |

`SegmentedPropertyCategory` 和 `SegmentedPropertyType` 的直接 IDC 查看器链接是带有子字段 `CodeValue`、`CodingSchemeDesignator` 和 `CodeMeaning` 的 RECORD 类型。使用 `.CodeMeaning` 进行人类可读的过滤。

* *idc-index 间隙：** idc-index 中的 `seg_index` 具有 `total_segments`、`AlgorithmName` 和聚合代码，但不公开每行的各个段解剖结构。当您需要查找包含特定结构的 SEG 系列（例如，具有“肝脏”片段的所有系列）时，请使用此 BigQuery 表。

* *发现跨 IDC 分段的结构：**

```sql
SELECT
  SegmentedPropertyCategory.CodeMeaning AS category,
  SegmentedPropertyType.CodeMeaning AS structure,
  SegmentAlgorithmType,
  COUNT(DISTINCT SeriesInstanceUID) AS seg_series_count
FROM `bigquery-public-data.idc_current.segmentations`
GROUP BY 1, 2, 3
ORDER BY seg_series_count DESC
LIMIT 20
```

* *查找包含特定结构的所有 SEG 系列以及源图像上下文：**

```sql
SELECT
  seg.SeriesInstanceUID AS seg_series,
  seg.SegmentNumber,
  seg.SegmentedPropertyType.CodeMeaning AS structure,
  seg.SegmentAlgorithmType,
  seg.SegmentAlgorithmName,
  img.collection_id,
  img.PatientID,
  img.Modality,
  seg.viewer_url
FROM `bigquery-public-data.idc_current.segmentations` seg
JOIN `bigquery-public-data.idc_current.dicom_all` img
  ON seg.segmented_SeriesInstanceUID = img.SeriesInstanceUID
WHERE seg.SegmentedPropertyType.CodeMeaning = 'Liver'
  AND seg.SegmentAlgorithmType = 'AUTOMATIC'
LIMIT 20
```

* *查找集合中存在的所有分段类型：**

```sql
SELECT
  seg.SegmentedPropertyType.CodeMeaning AS structure,
  seg.SegmentAlgorithmType,
  COUNT(DISTINCT seg.SeriesInstanceUID) AS seg_series_count
FROM `bigquery-public-data.idc_current.segmentations` seg
JOIN `bigquery-public-data.idc_current.dicom_all` img
  ON seg.segmented_SeriesInstanceUID = img.SeriesInstanceUID
WHERE img.collection_id = 'nlst'
GROUP BY 1, 2
ORDER BY seg_series_count DESC
```

* *使用 TrackingUID 将分段链接到 SR 测量：**

```sql
-- Find segments that have corresponding SR measurements
SELECT
  seg.SeriesInstanceUID AS seg_series,
  seg.SegmentNumber,
  seg.SegmentedPropertyType.CodeMeaning AS structure,
  qm.Quantity.CodeMeaning AS measurement,
  ROUND(CAST(qm.Value AS FLOAT64), 2) AS value,
  qm.Units.CodeMeaning AS units
FROM `bigquery-public-data.idc_current.segmentations` seg
JOIN `bigquery-public-data.idc_current.quantitative_measurements` qm
  ON seg.SeriesInstanceUID = qm.segmentationSeriesUID
  AND seg.SegmentNumber = qm.segmentationSegmentNumber
WHERE seg.SegmentedPropertyType.CodeMeaning = 'Neoplasm'
  AND qm.Quantity.CodeMeaning = 'Volume from Voxel Summation'
LIMIT 10
```

- --

### Quantity_measurements

DICOM SR TID1500 测量报告中每个数字测量一行。包含放射组学特征（形状、强度、纹理）和临床测量（体积、直径、SUV）。这些测量值是从 SR 中预先提取的 - 无需下载或 DICOM 解析。

* *没有等效的 idc 索引。**此表只能通过 BigQuery 访问。

* *关键列：**

|专栏 |类型 |说明 |
|--------|------|-------------|
| `SOPInstanceUID` |字符串 | SR实例UID |
| `SeriesInstanceUID` |字符串 | SR系列UID — 加入`dicom_all`进行采集/模态|
| `SeriesDescription` |字符串 | SR 系列描述（例如“TotalSegmentator(v1.5.6)形状测量”）|
| `PatientID` |字符串 |患者标识符|
| `measurementGroup_number` |整数| SR 内的组索引（从 0 开始）；与 `measurement_groups` 和 `qualitative_measurements` |
| 连接密钥`Quantity` |记录 |测量的内容 — `CodeValue`、`CodingSchemeDesignator`、`CodeMeaning`（例如“体素求和的体积”）|
| `Value` |数字|数值测量值|
| `Units` |记录 |单位 — `CodeMeaning`（例如“立方毫米”、“无单位”、“亨斯菲尔德单位”）|
| `derivationModifier` |记录 |该值是如何得出的（例如“平均值”、“最小值”、“最大值”）|
| `lateralityModifier` |记录 |偏侧限定符|
| `finding` |记录 |测量了什么结果 - `CodeMeaning`（例如“结节”、“器官”、“解剖结构”）|
| `findingSite` |记录 |发现的位置 — `CodeMeaning`（例如“肝脏”、“食道”、“肺”）|
| `trackingIdentifier` |字符串 |人类可读的跟踪标签（例如“结节 1”、“测量组 26”）|
| `trackingUniqueIdentifier` |字符串 |跟踪 UID — 链接回 `segmentations.TrackingUID` |
| `segmentationInstanceUID` |字符串 |引用的SEG对象的SOPInstanceUID|
| `segmentationSeriesUID` |字符串 |引用的SEG对象的SeriesInstanceUID |
| `segmentationSegmentNumber` |整数| SEG 内的段号 — 连接到 `segmentations.SegmentNumber` |
| `sourceSegmentedSeriesUID` |字符串 |源图像系列 - 加入 `dicom_all.SeriesInstanceUID` |

* *发现可用的测量类型：**

```sql
SELECT
  Quantity.CodeMeaning AS measurement,
  Units.CodeMeaning AS units,
  COUNT(*) AS measurement_count,
  COUNT(DISTINCT SeriesInstanceUID) AS sr_series_count
FROM `bigquery-public-data.idc_current.quantitative_measurements`
GROUP BY 1, 2
ORDER BY measurement_count DESC
LIMIT 20
```

* *查询特定结构的测量结果（例如，跨集合的肝脏体积）：**

```sql
SELECT
  qm.PatientID,
  ROUND(CAST(qm.Value AS FLOAT64) / 1000, 1) AS volume_cm3,
  img.collection_id,
  qm.segmentationSeriesUID
FROM `bigquery-public-data.idc_current.quantitative_measurements` qm
JOIN `bigquery-public-data.idc_current.dicom_all` img
  ON qm.sourceSegmentedSeriesUID = img.SeriesInstanceUID
WHERE qm.Quantity.CodeMeaning = 'Volume from Voxel Summation'
  AND qm.findingSite.CodeMeaning = 'Liver'
ORDER BY volume_cm3 DESC
LIMIT 20
```

* *检索特定患者的所有测量结果并发现：**

```sql
SELECT
  qm.measurementGroup_number,
  qm.finding.CodeMeaning AS finding,
  qm.findingSite.CodeMeaning AS finding_site,
  qm.lateralityModifier.CodeMeaning AS laterality,
  qm.Quantity.CodeMeaning AS feature,
  ROUND(CAST(qm.Value AS FLOAT64), 3) AS value,
  qm.Units.CodeMeaning AS units
FROM `bigquery-public-data.idc_current.quantitative_measurements` qm
WHERE qm.PatientID = 'LIDC-IDRI-0001'
  AND qm.finding.CodeMeaning = 'Nodule'
ORDER BY qm.measurementGroup_number, qm.Quantity.CodeMeaning
```

- --

### 定性_测量

DICOM SR TID1500 测量报告中每个编码评估一行。这些记录使用编码概念对（例如，数量=“恶性”、值=“5 中的 4（中度可疑癌症）”）来评估特征，而不是数值。

* *没有等效的 idc 索引。**此表只能通过 BigQuery 访问。

* *关键列：**

|专栏 |类型 |描述|
|--------|------|-------------|
| `SOPInstanceUID` |字符串 | SR实例UID |
| `SeriesInstanceUID` |字符串 | SR系列UID — 加入`dicom_all`进行采集/模态|
| `PatientID` |字符串 |患者标识符|
| `measurementGroup_number` |整数| SR 中的组索引 — 使用 `quantitative_measurements` |
| 的连接键`Quantity` |记录 |评估内容 — `CodeMeaning`（例如“恶性肿瘤”、“钙化”、“纹理”）|
| `Value` |记录 |编码答案 — `CodeMeaning`（例如，“5 分之 4（中度可疑癌症）”）|
| `finding` |记录 |评估了什么发现 - `CodeMeaning`（例如“结节”）|
| `findingSite` |记录 |解剖部位 — `CodeMeaning`（例如“肺”）|
| `trackingIdentifier` |字符串 |人类可读的跟踪标签|
| `segmentationInstanceUID` |字符串 |引用的SEG对象的SOPInstanceUID|
| `segmentationSeriesUID` |字符串 |引用的SEG对象的SeriesInstanceUID |
| `segmentationSegmentNumber` |整数|引用的 SEG |
| 内的段号`sourceSegmentedSeriesUID` |字符串 |源图像系列 - 加入 `dicom_all.SeriesInstanceUID` |

* *发现可用的定性特征及其值：**

```sql
SELECT
  Quantity.CodeMeaning AS feature,
  Value.CodeMeaning AS assessed_value,
  finding.CodeMeaning AS finding,
  COUNT(*) AS count
FROM `bigquery-public-data.idc_current.qualitative_measurements`
GROUP BY 1, 2, 3
ORDER BY count DESC
LIMIT 20
```

* *查找具有特定恶性肿瘤的所有结节评级：**

```sql
SELECT
  qm.PatientID,
  qm.trackingIdentifier AS nodule_id,
  qm.Value.CodeMeaning AS malignancy_rating,
  img.collection_id
FROM `bigquery-public-data.idc_current.qualitative_measurements` qm
JOIN `bigquery-public-data.idc_current.dicom_all` img
  ON qm.SeriesInstanceUID = img.SeriesInstanceUID
WHERE qm.Quantity.CodeMeaning = 'Malignancy'
  AND qm.Value.CodeMeaning LIKE '%Suspicious%'
ORDER BY qm.PatientID
LIMIT 20
```

- --

### measurement_groups

TID1500 测量组的父表。每一行代表 SR 中的一个测量组，参考分割和源图像，但没有单独的测量值。当您需要枚举组或检查跟踪的内容时，无需提取所有测量值，请使用此表。

* *关键列：** `SOPInstanceUID`、`SeriesInstanceUID`、`PatientID`、`measurementGroup_number`、`trackingIdentifier`、`trackingUniqueIdentifier`、`finding`、 `findingSite`、`segmentationInstanceUID`、`segmentationSeriesUID`、`segmentationSegmentNumber`、`sourceSegmentedSeriesUID`、`contentSequence`（原始SR内容序列）。

在大多数工作流程中，直接使用连接`quantitative_measurements`和`qualitative_measurements` `SOPInstanceUID` + `measurementGroup_number` 而不是通过 `measurement_groups`.

- --

### 结合定量和定性测量

需要两个表的主要用例：将同一发现的数字特征（体积、直径）与编码评估（恶性程度、纹理）相关联。加入 `SOPInstanceUID` + `measurementGroup_number`.

* *示例：LIDC-IDRI 肺结节分析 - 具有体积和直径的恶性评级：**

```sql
SELECT
  qual.PatientID,
  qual.trackingIdentifier AS nodule_id,
  qual.Value.CodeMeaning AS malignancy_rating,
  ROUND(CAST(vol.Value AS FLOAT64), 1) AS volume_mm3,
  ROUND(CAST(diam.Value AS FLOAT64), 1) AS diameter_mm
FROM `bigquery-public-data.idc_current.qualitative_measurements` qual
JOIN `bigquery-public-data.idc_current.quantitative_measurements` vol
  ON qual.SOPInstanceUID = vol.SOPInstanceUID
  AND qual.measurementGroup_number = vol.measurementGroup_number
JOIN `bigquery-public-data.idc_current.quantitative_measurements` diam
  ON qual.SOPInstanceUID = diam.SOPInstanceUID
  AND qual.measurementGroup_number = diam.measurementGroup_number
WHERE qual.Quantity.CodeMeaning = 'Malignancy'
  AND vol.Quantity.CodeMeaning = 'Volume'
  AND diam.Quantity.CodeMeaning = 'Diameter'
ORDER BY qual.PatientID, qual.trackingIdentifier
LIMIT 20
```

* *加入所有三个派生表以获得完整段context:**

```sql
SELECT
  seg.SegmentedPropertyType.CodeMeaning AS structure,
  qual.Quantity.CodeMeaning AS qualitative_feature,
  qual.Value.CodeMeaning AS qualitative_value,
  qm.Quantity.CodeMeaning AS quantitative_feature,
  ROUND(CAST(qm.Value AS FLOAT64), 3) AS numeric_value,
  qm.Units.CodeMeaning AS units,
  img.collection_id
FROM `bigquery-public-data.idc_current.segmentations` seg
JOIN `bigquery-public-data.idc_current.qualitative_measurements` qual
  ON seg.SeriesInstanceUID = qual.segmentationSeriesUID
  AND seg.SegmentNumber = qual.segmentationSegmentNumber
JOIN `bigquery-public-data.idc_current.quantitative_measurements` qm
  ON qual.SOPInstanceUID = qm.SOPInstanceUID
  AND qual.measurementGroup_number = qm.measurementGroup_number
JOIN `bigquery-public-data.idc_current.dicom_all` img
  ON seg.segmented_SeriesInstanceUID = img.SeriesInstanceUID
WHERE seg.SegmentedPropertyType.CodeMeaning = 'Neoplasm'
LIMIT 10
```

## 私有 DICOM 元素

私有 DICOM 元素是 DICOM 标准中未定义的供应商特定属性。它们通常包含对于图像解释和分析至关重要的基本采集参数（如扩散 b 值、梯度方向或扫描仪特定设置）。

### 了解私有元素

* *私有元素如何工作：**
- 私有元素使用奇数组编号（例如，0019、0043、2001）
- 每个供应商在位置（gggg，0010-00FF）使用私有创建者标识符保留256个元素的块
- 例如，GE在以下位置使用私有创建者“GEMS_PARM_01” (0043,0010)保留元素 (0043,1000-10FF)

* *标准与私有标签：** 某些参数以两种形式存在：
|参数|标准标签|通用电气|西门子|飞利浦|
|---------|-------------|-----|---------|---------|
|扩散 b 值 | (0018,9087) | (0043,1039) | (0019,100C) | (2001,1003) |
|私人创作者| - | GEMS_PARM_01 |西门子 CSA 接头 |飞利浦成像 |

 较旧的扫描仪通常仅填充私有标签；较新的扫描仪可能使用标准标签。始终检查两者。

* *私有元素的挑战：**
- 需要制造商 DICOM 一致性声明来解释
- 标签含义可能会在软件版本之间发生变化
- 可能会在 HIPAA 合规性去识别过程中被删除
- 值编码不同（字符串与数字，不同单位）

### 访问 BigQuery 中的私有元素

私有元素作为具有 `Tag` 和 `Data` 字段的结构数组存储在 `dicom_all` 的 `OtherElements` 列中。

* *标记表示法：** DICOM 表示法(0043,1039)变为 BigQuery 格式 `Tag_00431039`.

### 私有元素查询模式

#### 发现可用的私有标签

列出集合的所有非空私有标签：

```sql
SELECT
  other_elements.Tag,
  COUNT(*) AS instance_count,
  ARRAY_AGG(DISTINCT other_elements.Data[SAFE_OFFSET(0)] IGNORE NULLS LIMIT 5) AS sample_values
FROM `bigquery-public-data.idc_current.dicom_all`,
  UNNEST(OtherElements) AS other_elements
WHERE collection_id = 'qin_prostate_repeatability'
  AND Modality = 'MR'
  AND ARRAY_LENGTH(other_elements.Data) > 0
  AND other_elements.Data[SAFE_OFFSET(0)] IS NOT NULL
  AND other_elements.Data[SAFE_OFFSET(0)] != ''
GROUP BY other_elements.Tag
ORDER BY instance_count DESC
```

对于特定系列：

```sql
SELECT
  other_elements.Tag,
  ARRAY_AGG(DISTINCT other_elements.Data[SAFE_OFFSET(0)] IGNORE NULLS) AS values
FROM `bigquery-public-data.idc_current.dicom_all`,
  UNNEST(OtherElements) AS other_elements
WHERE SeriesInstanceUID = '1.3.6.1.4.1.14519.5.2.1.7311.5101.206828891270520544417996275680'
  AND ARRAY_LENGTH(other_elements.Data) > 0
  AND other_elements.Data[SAFE_OFFSET(0)] IS NOT NULL
  AND other_elements.Data[SAFE_OFFSET(0)] != ''
GROUP BY other_elements.Tag
```

 要识别标签的私有创建者，请在同一组中查找保留元素。例如，如果您找到 `Tag_00431039`，则私有创建者位于 `Tag_00430010`（保留组 0043 中的块 10xx 的标签）。

#### 识别设备制造商

确定生成数据的设备以找到正确的 DICOM 一致性声明：

```sql
SELECT DISTINCT Manufacturer, ManufacturerModelName
FROM `bigquery-public-data.idc_current.dicom_all`
WHERE collection_id = 'qin_prostate_repeatability'
  AND Modality = 'MR'
```

#### 访问私有元素值

使用 `UNNEST` 访问各个私有元素：

```sql
SELECT
  SeriesInstanceUID,
  SeriesDescription,
  other_elements.Data[SAFE_OFFSET(0)] AS b_value
FROM `bigquery-public-data.idc_current.dicom_all`,
  UNNEST(OtherElements) AS other_elements
WHERE collection_id = 'qin_prostate_repeatability'
  AND other_elements.Tag = 'Tag_00431039'
LIMIT 10
```

#### 聚合值系列

收集一系列切片中的所有唯一值：

```sql
SELECT
  SeriesInstanceUID,
  ANY_VALUE(SeriesDescription) AS SeriesDescription,
  ARRAY_AGG(DISTINCT other_elements.Data[SAFE_OFFSET(0)]) AS b_values
FROM `bigquery-public-data.idc_current.dicom_all`,
  UNNEST(OtherElements) AS other_elements
WHERE collection_id = 'qin_prostate_repeatability'
  AND other_elements.Tag = 'Tag_00431039'
GROUP BY SeriesInstanceUID
```

#### 组合标准和私有过滤器

使用标准 DICOM 属性和私有元素值进行过滤：

```sql
SELECT
  PatientID,
  SeriesInstanceUID,
  ANY_VALUE(SeriesDescription) AS SeriesDescription,
  ARRAY_AGG(DISTINCT other_elements.Data[SAFE_OFFSET(0)]) AS b_values,
  COUNT(DISTINCT SOPInstanceUID) AS n_slices
FROM `bigquery-public-data.idc_current.dicom_all`,
  UNNEST(OtherElements) AS other_elements
WHERE collection_id = 'qin_prostate_repeatability'
  AND Modality = 'MR'
  AND other_elements.Tag = 'Tag_00431039'
  AND ImageType[SAFE_OFFSET(0)] = 'ORIGINAL'
  AND other_elements.Data[SAFE_OFFSET(0)] = '1400'
GROUP BY PatientID, SeriesInstanceUID
ORDER BY PatientID
```

#### 交叉收集分析

调查所有IDC集合中私有标签的使用情况：

```sql
SELECT
  collection_id,
  ARRAY_TO_STRING(ARRAY_AGG(DISTINCT other_elements.Data[SAFE_OFFSET(0)] IGNORE NULLS), ', ') AS values_found,
  ARRAY_AGG(DISTINCT Manufacturer IGNORE NULLS) AS manufacturers
FROM `bigquery-public-data.idc_current.dicom_all`,
  UNNEST(OtherElements) AS other_elements
WHERE other_elements.Tag = 'Tag_00431039'
  AND other_elements.Data[SAFE_OFFSET(0)] IS NOT NULL
  AND other_elements.Data[SAFE_OFFSET(0)] != ''
GROUP BY collection_id
ORDER BY collection_id
```

### 工作流程：查找和使用私有标签

1. **使用上面的发现查询 
2 在您的集合中发现可用的私有标签**。 **确定制造商**以了解要查阅哪个一致性声明
3. **从制造商的网站查找 DICOM 一致性声明**（请参阅下面的资源）
4. **在一致性声明中搜索您需要的参数（例如“b_value”、“gradient”），以了解每个标签包含的内容
5. **将标签转换为 BigQuery 格式：** (g​​ggg,eeee) → `Tag_ggggeeee`
6. **在 IDC 查看器中直观地查询和验证**结果

### 数据质量说明

- 某些集合显示不切实际的值（例如，b 值“1000000600”），表明编码问题或不同的约定
- IDC 数据已去标识化；包含 PHI 的私有标签可能已被删除或修改
- 相同的标签在不同软件版本中可能具有不同的含义
- 在大规模分析之前始终使用 [IDC 查看器](https://viewer.imaging.datacommons.cancer.gov/)直观地验证查询结果

### 私有元素资源

* *制造商 DICOM 一致性声明：**
- [GE Healthcare MR](https://www.gehealthcare.com/products/interoperability/dicom/Magnetic-resonance-imaging-dicom-conformance-statements)
- [Siemens MR](https://www.siemens-healthineers.com/services/it-standards/dicom-conformance-statements-magnet-resonance)
- [西门子 CT](https://www.siemens-healthineers.com/services/it-standards/dicom-conformance-statements-compulated-tomography)

* *DICOM标准：**
- [第 5 部分第 7.8 节 - 私有数据元素](https://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_7.8.html)
- [第 15 部分附录 E - 去标识化配置文件](https://dicom.nema.org/medical/dicom/current/output/chtml/part15/chapter_e.html)

* *社区资源：**
- [NAMIC Wiki: DWI/DTI DICOM](https://www.na-mic.org/wiki/NAMIC_Wiki:DTI:DICOM_for_DWI_and_DTI) - 扩散的全面供应商比较Imaging
- [StandardizeBValue](https://github.com/nslay/StandardizeBValue) - 将供应商 b 值提取到标准标签的工具

## 将查询结果与 idc-index 结合使用 

将 BigQuery 与 idc-index 结合起来进行复杂查询以进行下载（无需 GCP 身份验证）下载）：

```python
from google.cloud import bigquery
from idc_index import IDCClient

# Initialize BigQuery client
# Requires: pip install google-cloud-bigquery
# Auth: gcloud auth application-default login
# Project: needed for billing even on public datasets (free tier applies)
bq_client = bigquery.Client(project="your-gcp-project-id")

# Query for series with specific criteria
query = """
SELECT DISTINCT SeriesInstanceUID
FROM `bigquery-public-data.idc_current.dicom_all`
WHERE collection_id = 'tcga_luad'
  AND Modality = 'CT'
  AND Manufacturer = 'GE MEDICAL SYSTEMS'
LIMIT 100
"""

df = bq_client.query(query).to_dataframe()
print(f"Found {len(df)} GE CT series")

# Download with idc-index (no GCP auth required)
idc_client = IDCClient()
idc_client.download_from_selection(
    seriesInstanceUID=list(df['SeriesInstanceUID'].values),
    downloadDir="./tcga_luad_thin_ct"
)
```

## 成本和优化

* *定价：** 每 TB 扫描 5 美元（前 1 TB/月免费）。大多数用户停留在免费套餐内。

* *最大限度地减少扫描的数据：**
- 仅选择需要的列（不是 `SELECT *`）
- 使用 `WHERE` 子句尽早过滤
- 测试时使用 `LIMIT`
- 使用尽可能使用 `dicom_all` 而不是 `dicom_metadata`（较小）
- 在 BQ 控制台中预览查询（免费，显示要扫描的字节）

* *运行前检查成本：**
```python
query_job = client.query(query, job_config=bigquery.QueryJobConfig(dry_run=True))
print(f"Query will scan {query_job.total_bytes_processed / 1e9:.2f} GB")
```

* *使用物化表：** IDC 提供两种视图(`table_name_view`)和物化表(`table_name`)。始终使用物化表（更快，成本更低）。

## 临床数据

临床数据位于具有特定于集合的表的单独数据集中。通过 `idc-index` 提供的所有临床数据也可以在 BigQuery 中获得，具有相同的内容和结构。当您需要本地 `idc-index` 表无法实现的复杂跨集合查询或联接时，请使用 BigQuery。

* *数据集：**
- `bigquery-public-data.idc_current_clinical` - 当前版本（用于探索）
- `bigquery-public-data.idc_v{version}_clinical` - 版本化数据集（用于重现性）

目前有约 130 个临床表，代表约 70 个集合。并非所有集合都有临床数据（从 IDC v11 开始）。

### 临床表命名

大多数集合使用单个表：`<collection_id>_clinical`

* *例外：** ACRIN 集合针对不同的数据类型使用多个表（例如，`acrin_6698_A0`、`acrin_6698_A1`、等）。

### 元数据表

两个元数据表可帮助导航临床数据：

* *table_metadata** - 集合级别信息：
```sql
SELECT
  collection_id,
  table_name,
  table_description
FROM `bigquery-public-data.idc_current_clinical.table_metadata`
WHERE collection_id = 'nlst'
```

* *column_metadata** - 具有值的属性级别详细信息映射：
```sql
SELECT
  collection_id,
  table_name,
  column,
  column_label,
  data_type,
  values
FROM `bigquery-public-data.idc_current_clinical.column_metadata`
WHERE collection_id = 'nlst'
  AND column_label LIKE '%stage%'
```

`values` 字段包含观察到的属性值及其描述（与 `idc-index` 临床索引中的相同）。

### 常见临床查询

* *列出可用的临床表：**
```sql
SELECT table_name
FROM `bigquery-public-data.idc_current_clinical.INFORMATION_SCHEMA.TABLES`
WHERE table_name NOT IN ('table_metadata', 'column_metadata')
```

* *查找具有特定临床属性的集合：**
```sql
SELECT DISTINCT collection_id, table_name, column, column_label
FROM `bigquery-public-data.idc_current_clinical.column_metadata`
WHERE LOWER(column_label) LIKE '%chemotherapy%'
```

* *查询集合的临床数据：**
```sql
-- Example: NLST cancer staging data
SELECT
  dicom_patient_id,
  clinical_stag,
  path_stag,
  de_stag
FROM `bigquery-public-data.idc_current_clinical.nlst_canc`
WHERE clinical_stag IS NOT NULL
LIMIT 10
```

* *加入临床与成像数据：**
```sql
SELECT
  d.PatientID,
  d.StudyInstanceUID,
  d.Modality,
  c.clinical_stag,
  c.path_stag
FROM `bigquery-public-data.idc_current.dicom_all` d
JOIN `bigquery-public-data.idc_current_clinical.nlst_canc` c
  ON d.PatientID = c.dicom_patient_id
WHERE d.collection_id = 'nlst'
  AND d.Modality = 'CT'
  AND c.clinical_stag = '400'  -- Stage IV
LIMIT 20
```

* *跨集合临床检索：**
```sql
-- Find all collections with staging information
SELECT
  cm.collection_id,
  cm.table_name,
  cm.column,
  cm.column_label
FROM `bigquery-public-data.idc_current_clinical.column_metadata` cm
WHERE LOWER(cm.column_label) LIKE '%stage%'
ORDER BY cm.collection_id
```

### 关键列：dicom_patent_id

每个临床表都包含`dicom_patient_id`，与DICOM匹配成像表中的 `PatientID` 属性。这是临床和影像数据之间的连接键。

* *注意：** 临床表模式因集合而异。始终首先检查可用列：
```sql
SELECT column_name, data_type
FROM `bigquery-public-data.idc_current_clinical.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'nlst_canc'
```

有关使用 `idc-index` 的详细工作流程，请参阅 `references/clinical_data_guide.md`，该工作流程无需 BigQuery 身份验证即可提供相同的临床数据。

## 重要说明

- 表是只读的（公共数据集）
- 之间的架构更改IDC 版本
- 使用版本化数据集以实现再现性
- 某些 DICOM 序列 >15 级深度未提取
- 非常大的序列 (>1MB)可能会被截断
- 使用前始终检查数据许可证

## 常见错误

* *问题：必须计费已启用**
- 原因：BigQuery 需要支持计费的 GCP 项目
- 解决方案：在 Google Cloud Console 中启用计费或改用 idc-index 迷你索引

* *问题：查询超出资源限制**
- 原因：查询扫描的数据过多或过于复杂
- 解决方案：添加更具体的 WHERE 过滤器，使用 LIMIT，分成较小的查询

* *问题：未找到列**
- 原因：字段名称拼写错误或不在所选表中
- 解决方案：首先使用 `INFORMATION_SCHEMA.COLUMNS`

 检查表架构**问题：权限被拒绝**
- 原因：未通过 Google 身份验证Cloud
- 解决方案：运行 `gcloud auth application-default login` 或设置 GOOGLE_APPLICATION_CREDENTIALS

## 资源

- [了解 BigQuery DICOM 架构](https://docs.cloud.google.com/healthcare-api/docs/how-tos/dicom-bigquery-schema)
- [BigQuery 查询语法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax)
- [Kaggle SQL 简介](https://www.kaggle.com/learn/intro-to-sql)
- [IDC 的 BigQuery 查询示例数据](https://github.com/ImagingDataCommons/idc-bigquery-cookbook)
