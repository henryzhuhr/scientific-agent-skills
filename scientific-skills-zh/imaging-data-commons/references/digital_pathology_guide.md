# IDC数字病理学指南

* *测试使用：** IDC数据版本v23，idc-index 0.11.10

对于一般IDC查询和下载，请使用`idc-index`（参见main SKILL.md）。本指南涵盖了 IDC 中数字病理学背景下的载玻片显微镜 (SM)成像、显微镜批量简单注释 (ANN)和分割 (SEG)。

## 数字病理学索引表

五个专门索引表提供精选元数据，无需 BigQuery：

|表|行粒度|描述 |
|-------|--------------------|----------|
| `sm_index` | 1 行 = 1 SM 系列 |载玻片显微镜系列元数据：容器/载玻片 ID、组织类型、解剖结构、诊断、镜头倍率、像素间距、图像尺寸 |
| `sm_instance_index` | 1 行 = 1 个 SM 实例 |单个幻灯片图像的实例级 (SOPInstanceUID)元数据 |
| `seg_index` | 1 行 = 1 SEG 系列 | DICOM 分段元数据：算法、分段计数、源系列参考。用于放射学和病理学 — 按源模态过滤以查找特定于病理学的分割 |
| `ann_index` | 1 行 = 1 ANN 系列 |显微镜批量简单注释系列元数据；包括链接到带注释的幻灯片 |
| 的 `referenced_SeriesInstanceUID` `ann_group_index` | 1 行 = 1 个注释组 |注解组明细：`AnnotationGroupLabel`、`GraphicType`、`NumberOfAnnotations`、`AlgorithmName`，属性代码|

均需要`client.fetch_index("table_name")`才可查询。使用 `client.indices_overview` 以编程方式检查列模式。

## 幻灯片显微镜查询

### 基本 SM 元数据

```python
from idc_index import IDCClient
client = IDCClient()

# sm_index has detailed metadata; join with index for collection_id
client.fetch_index("sm_index")
client.sql_query("""
    SELECT i.collection_id, COUNT(*) as slides,
           MIN(s.min_PixelSpacing_2sf) as min_resolution
    FROM sm_index s
    JOIN index i ON s.SeriesInstanceUID = i.SeriesInstanceUID
    GROUP BY i.collection_id
    ORDER BY slides DESC
""")
```

### 查找具有特定属性的 SM 系列

```python
# Find high-resolution slides with specific objective lens power
client.fetch_index("sm_index")
client.sql_query("""
    SELECT
        i.collection_id,
        i.PatientID,
        s.ObjectiveLensPower,
        s.min_PixelSpacing_2sf
    FROM sm_index s
    JOIN index i ON s.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE s.ObjectiveLensPower >= 40
    ORDER BY s.min_PixelSpacing_2sf
    LIMIT 20
""")
```

### 按样本过滤制剂

`sm_index` 包括染色、嵌入和固定元数据。这些列是**数组**（例如，H&E 的 `[hematoxylin stain, water soluble eosin stain]`）— 使用 `array_to_string()` 和 `LIKE` 或 `list_contains()` 进行过滤。

```python
# Find H&E-stained slides in a collection
client.fetch_index("sm_index")
client.sql_query("""
    SELECT
        i.PatientID,
        s.staining_usingSubstance_CodeMeaning as staining,
        s.embeddingMedium_CodeMeaning as embedding,
        s.tissueFixative_CodeMeaning as fixative
    FROM sm_index s
    JOIN index i ON s.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE i.collection_id = 'tcga_brca'
      AND array_to_string(s.staining_usingSubstance_CodeMeaning, ', ') LIKE '%hematoxylin%'
    LIMIT 10
""")
```

```python
# Compare FFPE vs frozen slides across collections
client.sql_query("""
    SELECT
        i.collection_id,
        s.embeddingMedium_CodeMeaning as embedding,
        COUNT(*) as slide_count
    FROM sm_index s
    JOIN index i ON s.SeriesInstanceUID = i.SeriesInstanceUID
    GROUP BY i.collection_id, embedding
    ORDER BY i.collection_id, slide_count DESC
""")
```

## 识别肿瘤与正常幻灯片

`sm_index`表提供两种识别组织类型的方法：

|专栏 |使用案例|
|--------|----------|
| `primaryAnatomicStructureModifier_CodeMeaning` |来自 DICOM 标本元数据的结构化组织类型（例如，`Neoplasm, Primary`、`Normal`、`Tumor`、`Neoplasm, Metastatic`）。适用于所有包含 SM 数据的集合。 |
| `ContainerIdentifier` |载玻片/容器标识符。对于 TCGA 集合，包含 [TCGA 条形码](https://docs.gdc.cancer.gov/Encyclopedia/pages/TCGA_Barcode/)，其中[样本类型代码](https://gdc.cancer.gov/resources-tcga-users/tcga-code-tables/sample-type-codes)（位置 14-15）编码组织来源： `01`-`09` = 肿瘤，`10`-`19` = 正常。 |

### 使用结构化组织类型元数据

```python
from idc_index import IDCClient
client = IDCClient()
client.fetch_index("sm_index")

# Discover tissue type values across all SM data
client.sql_query("""
    SELECT
        s.primaryAnatomicStructureModifier_CodeMeaning as tissue_type,
        COUNT(*) as slide_count
    FROM sm_index s
    WHERE s.primaryAnatomicStructureModifier_CodeMeaning IS NOT NULL
    GROUP BY tissue_type
    ORDER BY slide_count DESC
""")
```

#### 示例：TCGA-BRCA

```python
# Tissue type breakdown for TCGA-BRCA
client.sql_query("""
    SELECT
        s.primaryAnatomicStructureModifier_CodeMeaning as tissue_type,
        COUNT(*) as slide_count,
        COUNT(DISTINCT i.PatientID) as patient_count
    FROM sm_index s
    JOIN index i ON s.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE i.collection_id = 'tcga_brca'
    GROUP BY tissue_type
    ORDER BY slide_count DESC
""")
# Returns: Neoplasm, Primary (2704 slides), Normal (399 slides)
```

### 使用 TCGA 条形码（仅限 TCGA 集合）

对于 TCGA 集合，肿瘤与正常切片`ContainerIdentifier` 包含载玻片条形码（例如，`TCGA-E9-A3X8-01A-03-TSC`）。提取样本类型代码以对组织进行分类：

```python
# Parse sample type from TCGA barcode
client.sql_query("""
    SELECT
        SUBSTRING(SPLIT_PART(s.ContainerIdentifier, '-', 4), 1, 2) as sample_type_code,
        s.primaryAnatomicStructureModifier_CodeMeaning as tissue_type,
        COUNT(*) as slide_count
    FROM sm_index s
    JOIN index i ON s.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE i.collection_id = 'tcga_brca'
    GROUP BY sample_type_code, tissue_type
    ORDER BY sample_type_code
""")
# Returns: 01 → Neoplasm, Primary (2704), 06 → None (8), 11 → Normal (399)
```

条形码方法可捕获结构化元数据为 NULL 的情况（例如，`06` = TCGA-BRCA 中的转移性载玻片具有 `primaryAnatomicStructureModifier_CodeMeaning` = NULL）。

## 注释查询(ANN)

DICOM 显微镜批量简单注释（模态 = 'ANN'）是**载玻片显微镜图像上的注释。它们出现在`ann_index`（系列级）和`ann_group_index`（组级详细信息）中。每个 ANN 系列均引用其通过 `referenced_SeriesInstanceUID`.

### 基本注释发现

注释的幻灯片```python
# Find annotation series and their referenced images
client.fetch_index("ann_index")
client.fetch_index("ann_group_index")

client.sql_query("""
    SELECT
        a.SeriesInstanceUID as ann_series,
        a.AnnotationCoordinateType,
        a.referenced_SeriesInstanceUID as source_series
    FROM ann_index a
    LIMIT 10
""")
```

### 注释组统计

```python
# Get annotation group details (graphic types, counts, algorithms)
client.sql_query("""
    SELECT
        GraphicType,
        SUM(NumberOfAnnotations) as total_annotations,
        COUNT(*) as group_count
    FROM ann_group_index
    GROUP BY GraphicType
    ORDER BY total_annotations DESC
""")
```

### 使用源幻灯片上下文查找注释

```python
# Find annotations with their source slide microscopy context
client.sql_query("""
    SELECT
        i.collection_id,
        g.GraphicType,
        g.AnnotationPropertyType_CodeMeaning,
        g.AlgorithmName,
        g.NumberOfAnnotations
    FROM ann_group_index g
    JOIN ann_index a ON g.SeriesInstanceUID = a.SeriesInstanceUID
    JOIN index i ON a.referenced_SeriesInstanceUID = i.SeriesInstanceUID
    WHERE g.AlgorithmName IS NOT NULL
    LIMIT 10
""")
```

## 幻灯片显微镜上的分段

DICOM 分段（模态 = 'SEG'）用于放射学（例如 CT 上的器官分割）和病理学（例如整个幻灯片图像上的组织区域分割）。使用 `seg_index.segmented_SeriesInstanceUID` 查找源系列，然后按源模态过滤以隔离病理分割。

```python
# Find segmentations whose source is a slide microscopy image
client.fetch_index("seg_index")
client.fetch_index("sm_index")
client.sql_query("""
    SELECT
        seg.SeriesInstanceUID as seg_series,
        seg.AlgorithmName,
        seg.total_segments,
        src.collection_id,
        src.Modality as source_modality
    FROM seg_index seg
    JOIN index src ON seg.segmented_SeriesInstanceUID = src.SeriesInstanceUID
    WHERE src.Modality = 'SM'
    LIMIT 20
""")
```

## 查找预先计算的分析结果

IDC 托管由 `analysis_result_id` 在主目录中识别的派生数据集（细胞核分割、TIL 图、AI 注释） `index`表。使用 `analysis_results_index` 来发现可用于病理学的内容。

```python
from idc_index import IDCClient
client = IDCClient()
client.fetch_index("analysis_results_index")

# Find analysis results that include pathology annotations or segmentations
client.sql_query("""
    SELECT
        ar.analysis_result_id,
        ar.analysis_result_title,
        ar.Modalities,
        ar.Subjects,
        ar.Collections
    FROM analysis_results_index ar
    WHERE ar.Modalities LIKE '%ANN%' OR ar.Modalities LIKE '%SEG%'
    ORDER BY ar.Subjects DESC
""")
```

### 查找特定幻灯片的分析结果

```python
# Find all derived data (annotations, segmentations) for TCGA-BRCA slides
client.fetch_index("ann_index")
client.sql_query("""
    SELECT
        i.analysis_result_id,
        i.PatientID,
        a.referenced_SeriesInstanceUID as source_slide,
        g.AnnotationGroupLabel,
        g.NumberOfAnnotations,
        g.AlgorithmName
    FROM ann_group_index g
    JOIN ann_index a ON g.SeriesInstanceUID = a.SeriesInstanceUID
    JOIN index i ON a.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE i.collection_id = 'tcga_brca'
    LIMIT 10
""")
```

 注释对象还可以包含存储在其中的每个注释**测量**（例如，细胞核面积、偏心率） DICOM 文件。这些不在索引表中 - 使用 [highdicom](https://github.com/ImagingDataCommons/highdicom) (`ann.get_annotation_groups()`、`group.get_measurements()`)下载后提取它们。请参阅 [microscopy_dicom_ann_intro](https://github.com/ImagingDataCommons/IDC-Tutorials/blob/master/notebooks/pathomics/microscopy_dicom_ann_intro.ipynb)教程，了解包括空间分析和细胞结构计算的工作示例。

## 按 AnnotationGroupLabel

`AnnotationGroupLabel` 过滤是按名称或语义内容查找注释组的最直接的列。使用 `LIKE` 和通配符进行文本搜索。

### 简单标签过滤

```python
# Find annotation groups by label (e.g., groups mentioning "blast")
client.fetch_index("ann_group_index")
client.sql_query("""
    SELECT
        g.SeriesInstanceUID,
        g.AnnotationGroupLabel,
        g.GraphicType,
        g.NumberOfAnnotations,
        g.AlgorithmName
    FROM ann_group_index g
    WHERE LOWER(g.AnnotationGroupLabel) LIKE '%blast%'
    ORDER BY g.NumberOfAnnotations DESC
""")
```

### 带有集合上下文的标签过滤

```python
# Find annotation groups matching a label within a specific collection
client.fetch_index("ann_index")
client.fetch_index("ann_group_index")
client.sql_query("""
    SELECT
        i.collection_id,
        g.AnnotationGroupLabel,
        g.GraphicType,
        g.NumberOfAnnotations,
        g.AnnotationPropertyType_CodeMeaning
    FROM ann_group_index g
    JOIN ann_index a ON g.SeriesInstanceUID = a.SeriesInstanceUID
    JOIN index i ON a.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE i.collection_id = 'your_collection_id'
      AND LOWER(g.AnnotationGroupLabel) LIKE '%keyword%'
    ORDER BY g.NumberOfAnnotations DESC
""")
```

## 载玻片显微镜注释（SM + ANN）交叉参考）

在查找与载玻片显微镜数据相关的注释时，请同时使用 SM 和 ANN 表。 `ann_index.referenced_SeriesInstanceUID` 将每个注释系列链接到其源幻灯片。

```python
# Find slide microscopy images and their annotations in a collection
client.fetch_index("sm_index")
client.fetch_index("ann_index")
client.fetch_index("ann_group_index")
client.sql_query("""
    SELECT
        i.collection_id,
        s.ObjectiveLensPower,
        g.AnnotationGroupLabel,
        g.NumberOfAnnotations,
        g.GraphicType
    FROM ann_group_index g
    JOIN ann_index a ON g.SeriesInstanceUID = a.SeriesInstanceUID
    JOIN sm_index s ON a.referenced_SeriesInstanceUID = s.SeriesInstanceUID
    JOIN index i ON a.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE i.collection_id = 'your_collection_id'
    ORDER BY g.NumberOfAnnotations DESC
""")
```

## 连接模式

### SM 连接（带有集合上下文的幻灯片显微镜详细信息）

```python
client.fetch_index("sm_index")
result = client.sql_query("""
    SELECT i.collection_id, i.PatientID, s.ObjectiveLensPower, s.min_PixelSpacing_2sf
    FROM index i
    JOIN sm_index s ON i.SeriesInstanceUID = s.SeriesInstanceUID
    LIMIT 10
""")
```

### ANN 连接（带有集合的注释组） context)

```python
client.fetch_index("ann_index")
client.fetch_index("ann_group_index")
result = client.sql_query("""
    SELECT
        i.collection_id,
        g.AnnotationGroupLabel,
        g.GraphicType,
        g.NumberOfAnnotations,
        a.referenced_SeriesInstanceUID as source_series
    FROM ann_group_index g
    JOIN ann_index a ON g.SeriesInstanceUID = a.SeriesInstanceUID
    JOIN index i ON a.SeriesInstanceUID = i.SeriesInstanceUID
    LIMIT 10
""")
```

## 相关工具

以下工具适用于数字病理工作流程的 DICOM 格式：

* *Python 库：**
- [highdicom](https://github.com/ImagingDataCommons/highdicom) - Python 的高级 DICOM 抽象。创建和读取 DICOM 分段 (SEG)、结构化报告 (SR)以及病理学和放射学参数图。由 IDC.
- [wsidicom](https://github.com/imi-bigpicture/wsidicom)开发 - 用于读取 DICOM WSI 数据集的 Python 包。将元数据解析为易于使用的数据类，以进行整个幻灯片图像分析。
- [TIA-Toolbox](https://github.com/TissueImageAnalytics/tiatoolbox) - 通过 `DICOMWSIReader` 提供 DICOM 支持的端到端计算病理学库。提供图块提取、特征提取和预训练深度学习模型。
- [EZ-WSI-DICOMweb](https://github.com/GoogleCloudPlatform/EZ-WSI-DICOMweb) - 通过 DICOMweb 从 DICOM 整个幻灯片图像中提取图像补丁。专为具有云 DICOM 商店的 AI/ML 工作流程而设计。

* *查看器：**
- [Slim](https://github.com/ImagingDataCommons/slim) - 基于 Web 的 DICOM 幻灯片显微镜查看器和注释工具。通过 DICOMweb 支持明场和多重免疫荧光成像。由IDC开发。
- [QuPath](https://qupath.github.io/) - 用于整个幻灯片图像分析的跨平台开源软件。通过 Bio-Formats 和 OpenSlide (v0.4.0+)支持 DICOM WSI。

* *转换：**
- [dicom_wsi](https://github.com/Steven-N-Hart/dicom_wsi) - 用于将专有 WSI 格式转换为 DICOM 兼容文件的 Python 实现。
