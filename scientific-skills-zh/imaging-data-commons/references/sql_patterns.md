# IDC 的 SQL 查询模式

* *测试使用：** idc-index 0.11.14（IDC 数据版本 v23）

使用 IDC 数据时常见 SQL 查询模式的快速参考。有关上下文的详细示例，请参阅主 SKILL.md 中的“核心功能”部分。

## 何时使用本指南

当您需要快速参考 SQL 模式时加载本指南：
- 发现可用的过滤器值（模式、身体部位、制造商）
- 跨集合查找注释和分段
- 查询载玻片显微镜检查和注释数据
- 下载前估计下载大小
- 将成像数据链接到临床数据
- 按 3D 体积几何有效性过滤 (volume_geometry_index)
- 查找 RT 结构集系列和 ROI 元数据 (rtstruct_index)

有关表模式、DataFrame 访问和连接列引用，请参阅`references/index_tables_guide.md`.

## 先决条件

```bash
pip install --upgrade idc-index
```

```python
from idc_index import IDCClient
client = IDCClient()
```

## 发现可用的过滤器值

```python
# What modalities exist?
client.sql_query("SELECT DISTINCT Modality FROM index")

# What body parts for a specific modality?
client.sql_query("""
    SELECT DISTINCT BodyPartExamined, COUNT(*) as n
    FROM index WHERE Modality = 'CT' AND BodyPartExamined IS NOT NULL
    GROUP BY BodyPartExamined ORDER BY n DESC
""")

# What manufacturers for MR?
client.sql_query("""
    SELECT DISTINCT Manufacturer, COUNT(*) as n
    FROM index WHERE Modality = 'MR'
    GROUP BY Manufacturer ORDER BY n DESC
""")
```

## 查找注释和Segmentations

* *注意：**并非所有图像衍生对象都属于分析结果集合。一些注释与原始图像一起存放。使用 DICOM Modality 或 SOPClassUID 查找所有派生对象，无论集合类型如何。

```python
# Find ALL segmentations and structure sets by DICOM Modality
# SEG = DICOM Segmentation, RTSTRUCT = Radiotherapy Structure Set
client.sql_query("""
    SELECT collection_id, Modality, COUNT(*) as series_count
    FROM index
    WHERE Modality IN ('SEG', 'RTSTRUCT')
    GROUP BY collection_id, Modality
    ORDER BY series_count DESC
""")

# Find segmentations for a specific collection (includes non-analysis-result items)
client.sql_query("""
    SELECT SeriesInstanceUID, SeriesDescription, analysis_result_id
    FROM index
    WHERE collection_id = 'tcga_luad' AND Modality = 'SEG'
""")

# List analysis result collections (curated derived datasets)
client.fetch_index("analysis_results_index")
client.sql_query("""
    SELECT analysis_result_id, analysis_result_title, Collections, Modalities
    FROM analysis_results_index
""")

# Find analysis results for a specific source collection
client.sql_query("""
    SELECT analysis_result_id, analysis_result_title
    FROM analysis_results_index
    WHERE Collections LIKE '%tcga_luad%'
""")

# Use seg_index for detailed DICOM Segmentation metadata
client.fetch_index("seg_index")

# Get segmentation statistics by algorithm
client.sql_query("""
    SELECT AlgorithmName, AlgorithmType, COUNT(*) as seg_count
    FROM seg_index
    WHERE AlgorithmName IS NOT NULL
    GROUP BY AlgorithmName, AlgorithmType
    ORDER BY seg_count DESC
    LIMIT 10
""")

# Find segmentations for specific source images (e.g., chest CT)
client.sql_query("""
    SELECT
        s.SeriesInstanceUID as seg_series,
        s.AlgorithmName,
        s.total_segments,
        s.segmented_SeriesInstanceUID as source_series
    FROM seg_index s
    JOIN index src ON s.segmented_SeriesInstanceUID = src.SeriesInstanceUID
    WHERE src.Modality = 'CT' AND src.BodyPartExamined = 'CHEST'
    LIMIT 10
""")

# Find TotalSegmentator results with source image context
client.sql_query("""
    SELECT
        seg_info.collection_id,
        COUNT(DISTINCT s.SeriesInstanceUID) as seg_count,
        SUM(s.total_segments) as total_segments
    FROM seg_index s
    JOIN index seg_info ON s.SeriesInstanceUID = seg_info.SeriesInstanceUID
    WHERE s.AlgorithmName LIKE '%TotalSegmentator%'
    GROUP BY seg_info.collection_id
    ORDER BY seg_count DESC
""")

# Use ann_index and ann_group_index for Microscopy Bulk Simple Annotations
# ann_group_index has AnnotationGroupLabel, GraphicType, NumberOfAnnotations, AlgorithmName
client.fetch_index("ann_index")
client.fetch_index("ann_group_index")
client.sql_query("""
    SELECT g.AnnotationGroupLabel, g.GraphicType, g.NumberOfAnnotations, i.collection_id
    FROM ann_group_index g
    JOIN ann_index a ON g.SeriesInstanceUID = a.SeriesInstanceUID
    JOIN index i ON a.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE g.AlgorithmName IS NOT NULL
    LIMIT 10
""")
# See references/digital_pathology_guide.md for AnnotationGroupLabel filtering, SM+ANN joins, and more
```

## 查询载玻片显微镜和注释数据

使用 `sm_index` 获取载玻片显微镜元数据，使用 `ann_index`/`ann_group_index` 获取载玻片上的注释（DICOM ANN对象）。按 `AnnotationGroupLabel` 过滤注释组，以按名称查找注释。

```python
client.fetch_index("sm_index")
client.fetch_index("ann_index")
client.fetch_index("ann_group_index")

# Example: find annotation groups by label within a collection
client.sql_query("""
    SELECT g.AnnotationGroupLabel, g.GraphicType, g.NumberOfAnnotations
    FROM ann_group_index g
    JOIN index i ON g.SeriesInstanceUID = i.SeriesInstanceUID
    WHERE i.collection_id = 'your_collection_id'
      AND LOWER(g.AnnotationGroupLabel) LIKE '%keyword%'
""")
```

有关 SM 查询、ANN 过滤模式、SM+ANN 交叉引用和连接示例，请参阅 `references/digital_pathology_guide.md`。

## 估计下载Size

```python
# Size for specific criteria
client.sql_query("""
    SELECT SUM(series_size_MB) as total_mb, COUNT(*) as series_count
    FROM index
    WHERE collection_id = 'nlst' AND Modality = 'CT'
""")
```

## 临床数据链接

```python
client.fetch_index("clinical_index")

# Find collections with clinical data and their tables
client.sql_query("""
    SELECT collection_id, table_name, COUNT(DISTINCT column_label) as columns
    FROM clinical_index
    GROUP BY collection_id, table_name
    ORDER BY collection_id
""")
```

请参阅 `references/clinical_data_guide.md` 了解完整模式，包括值映射和患者队列选择。

## 故障排除

* *问题：**查询返回错误“找不到表”
- **原因：**查询前未获取索引
- **解决方案：**使用主 ZXQINLINE8QX

 以外的表之前调用 `client.fetch_index("table_name")` **问题：** LIKE 模式与预期结果不匹配
- **原因：**区分大小写或空白
- **解决方案：** 使用 `LOWER(column)` 进行不区分大小写的匹配，使用 `TRIM()` 进行空白

* *问题：** JOIN 返回的行数比预期少
- **原因：** 连接列中存在 NULL 值或没有匹配的记录
- **解决方案：** 使用 `LEFT JOIN`包含不匹配的行，使用 `IS NOT NULL`

## 体积几何验证

`volume_geometry_index` 来检查 NULL，涵盖单帧 CT、MR 和 PT 系列。查询前先获取

```python
client.fetch_index("volume_geometry_index")

# Series that form a regularly-spaced 3D volume (no resampling needed)
client.sql_query("""
    SELECT i.collection_id, i.SeriesInstanceUID, i.BodyPartExamined,
           v.obliquity_degrees
    FROM index i
    JOIN volume_geometry_index v ON i.SeriesInstanceUID = v.SeriesInstanceUID
    WHERE i.Modality = 'CT'
      AND v.regularly_spaced_3d_volume = TRUE
    LIMIT 10
""")

# Fraction of 3D-valid CT per collection
client.sql_query("""
    SELECT i.collection_id,
           COUNT(*) as total_ct,
           SUM(CASE WHEN v.regularly_spaced_3d_volume THEN 1 ELSE 0 END) as valid_3d,
           ROUND(100.0 * SUM(CASE WHEN v.regularly_spaced_3d_volume THEN 1 ELSE 0 END) / COUNT(*), 1) as pct_valid
    FROM index i
    JOIN volume_geometry_index v ON i.SeriesInstanceUID = v.SeriesInstanceUID
    WHERE i.Modality = 'CT'
    GROUP BY i.collection_id
    ORDER BY total_ct DESC
    LIMIT 10
""")
```

关键列：`regularly_spaced_3d_volume`（复合标志）、`obliquity_degrees`（0 =纯轴向/矢状/冠状），加上单独的布尔检查：`single_orientation`、`orthogonal_orientation`、 `unique_slice_positions`、`consistent_pixel_spacing`、`consistent_image_dimensions`、`uniform_slice_spacing`.

## RT 结构集

`rtstruct_index` 每个 RTSTRUCT 系列有一行。数组列（`ROINames`、`ROIGenerationAlgorithms`、`RTROIInterpretedTypes`）存储为字符串。

```python
client.fetch_index("rtstruct_index")

# RTSTRUCT series with ROI counts and names
client.sql_query("""
    SELECT i.collection_id, i.SeriesInstanceUID,
           r.total_rois, r.ROINames, r.RTROIInterpretedTypes,
           r.referenced_SeriesInstanceUID
    FROM index i
    JOIN rtstruct_index r ON i.SeriesInstanceUID = r.SeriesInstanceUID
    LIMIT 10
""")

# Collections with the most RTSTRUCT series
client.sql_query("""
    SELECT i.collection_id,
           COUNT(*) as rtstruct_series,
           ROUND(AVG(r.total_rois), 1) as avg_rois
    FROM index i
    JOIN rtstruct_index r ON i.SeriesInstanceUID = r.SeriesInstanceUID
    GROUP BY i.collection_id
    ORDER BY rtstruct_series DESC
    LIMIT 10
""")

# Find source CT series for a given RTSTRUCT
client.sql_query("""
    SELECT r.SeriesInstanceUID as rtstruct_uid,
           r.total_rois, r.ROINames,
           src.SeriesInstanceUID as source_ct_uid,
           src.collection_id, src.BodyPartExamined
    FROM rtstruct_index r
    JOIN index src ON r.referenced_SeriesInstanceUID = src.SeriesInstanceUID
    LIMIT 10
""")
```

## 资源

- `references/index_tables_guide.md` 用于表模式、DataFrame 访问和连接列引用
- `references/clinical_data_guide.md` 用于临床数据模式和值映射
- `references/digital_pathology_guide.md` 用于病理特定查询
- `references/bigquery_guide.md` 用于需要完整 DICOM 元数据的高级查询
- `references/parquet_access_guide.md` 用于直接 Parquet 查询，无需安装 idc-index
