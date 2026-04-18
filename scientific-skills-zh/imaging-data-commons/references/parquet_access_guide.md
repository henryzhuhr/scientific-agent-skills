# IDC

直接 Parquet 访问指南**测试使用：** idc-index-data 23.10.1、DuckDB 1.x

 所有 idc-index 元数据表都作为 Parquet 文件发布到具有不受限制的 CORS 访问的公共 GCS 存储桶。这可以在不安装 idc-index 的情况下使用 DuckDB 或 pandas 进行元数据查询 - 对于快速探索或 pip install 不可用的环境非常有用。

* *限制：** 下载帮助程序 (`download_from_selection()`)、查看器 URL (`get_viewer_URL()`)和引文生成需要 idc-index 客户端，并且无法从原始 Parquet 文件中获得。

## 何时使用此功能指南

当您需要时加载本指南：
- 在不安装idc-index的情况下查询IDC元数据
- 针对最新索引文件运行临时DuckDB查询
- 访问`volume_geometry_index`或`rtstruct_index`进行几何验证或RT结构查询

用于完整的API访问（下载，查看器，引用），使用主 SKILL.md.

## URL Pattern

```
https://storage.googleapis.com/idc-index-data-artifacts/current/release_artifacts/{filename}.parquet
```

`current/` 中记录的 idc-index 始终解析为最新数据版本。要固定到特定版本，请将 `current` 替换为数据版本号（例如，`23.10.1`）。

## 可用文件

|文件 |大概尺寸 |描述 |
|------|------------------|-------------|
| `idc_index.parquet` | 〜70 MB |主索引（所有DICOM系列元数据）|
| `volume_geometry_index.parquet` | 〜5 MB | CT/MR/PT 系列的 3D 几何验证 |
| `rtstruct_index.parquet` | 〜2 MB | RT 结构集 ROI 元数据 |
| `seg_index.parquet` | 〜6 MB | DICOM 分割交叉引用 |
| `sm_index.parquet` | 〜2 MB |载玻片显微镜系列元数据|
| `contrast_index.parquet` | 〜1 MB |造影剂元数据 |
| `ann_index.parquet` | 〜0.2 MB |显微镜注释系列元数据|
| `ann_group_index.parquet` | ~0.5 MB |注释组元数据|
| `collections_index.parquet` | — |集合级元数据|
| `analysis_results_index.parquet` | — |派生数据集元数据|
| `clinical_index.parquet` | 〜0.2 MB |临床数据列词典|
| `prior_versions_index.parquet` | — |之前 IDC 版本的系列 |

* *注意：** 主索引文件名为 `idc_index.parquet`，而不是 `index.parquet`。在 SQL 查询中使用别名引用它（例如，`FROM read_parquet(...) AS index`）。

## 先决条件

```bash
pip install duckdb
# or: uv add duckdb
```

DuckDB 使用 HTTP 范围请求直接从 HTTPS URL 读取 Parquet — 不需要 GCS 客户端库或身份验证。

## 基本查询

```python
import duckdb

BASE = "https://storage.googleapis.com/idc-index-data-artifacts/current/release_artifacts"

# Discover modalities and series counts
duckdb.sql(f"""
    SELECT Modality, COUNT(*) as series_count, ROUND(SUM(series_size_MB)/1000, 1) as size_GB
    FROM read_parquet('{BASE}/idc_index.parquet')
    GROUP BY Modality
    ORDER BY series_count DESC
""").df()

# Collections with CT data, ordered by size
duckdb.sql(f"""
    SELECT collection_id,
           COUNT(DISTINCT PatientID) as patients,
           COUNT(*) as series,
           ROUND(SUM(series_size_MB)/1000, 1) as size_GB
    FROM read_parquet('{BASE}/idc_index.parquet')
    WHERE Modality = 'CT'
    GROUP BY collection_id
    ORDER BY size_GB DESC
    LIMIT 10
""").df()
```

## 体积几何验证

`volume_geometry_index`涵盖单帧CT、MR和PT系列。每行都有方向、间距、尺寸和切片位置的布尔检查，以及复合 `regularly_spaced_3d_volume` 标志。

```python
import duckdb

BASE = "https://storage.googleapis.com/idc-index-data-artifacts/current/release_artifacts"

# CT series that form a valid 3D volume (can be loaded without resampling)
duckdb.sql(f"""
    SELECT i.collection_id, i.SeriesInstanceUID, i.BodyPartExamined,
           v.obliquity_degrees, v.regularly_spaced_3d_volume
    FROM read_parquet('{BASE}/idc_index.parquet') i
    JOIN read_parquet('{BASE}/volume_geometry_index.parquet') v
        ON i.SeriesInstanceUID = v.SeriesInstanceUID
    WHERE i.Modality = 'CT'
      AND v.regularly_spaced_3d_volume = TRUE
    LIMIT 10
""").df()

# Fraction of 3D-valid series per collection and modality
duckdb.sql(f"""
    SELECT i.collection_id, i.Modality,
           COUNT(*) as total,
           SUM(CASE WHEN v.regularly_spaced_3d_volume THEN 1 ELSE 0 END) as valid_3d,
           ROUND(100.0 * SUM(CASE WHEN v.regularly_spaced_3d_volume THEN 1 ELSE 0 END) / COUNT(*), 1) as pct_valid
    FROM read_parquet('{BASE}/idc_index.parquet') i
    JOIN read_parquet('{BASE}/volume_geometry_index.parquet') v
        ON i.SeriesInstanceUID = v.SeriesInstanceUID
    WHERE i.Modality IN ('CT', 'MR', 'PT')
    GROUP BY i.collection_id, i.Modality
    ORDER BY total DESC
    LIMIT 10
""").df()
```

 `volume_geometry_index`:

 中的关键列|专栏 |类型 |说明 |
|--------|------|-------------|
| `SeriesInstanceUID` |字符串 |连接键|
| `single_orientation` |布尔 |所有实例共享相同的 ImageOrientationPatient |
| `orthogonal_orientation` |布尔 |方向余弦正交|
| `unique_slice_positions` |布尔 |没有重复或重叠的切片 |
| `consistent_pixel_spacing` |布尔 |所有实例共享相同的 PixelSpacing |
| `consistent_image_dimensions` |布尔 |所有实例共享相同的行和列 |
| `uniform_slice_spacing` |布尔 |连续切片之间的间距恒定 |
| `obliquity_degrees` |浮动|切片法线与最近的基轴之间的角度（0 = 纯轴向/矢状/冠状）|
| `regularly_spaced_3d_volume` |布尔 |复合：如果所有检查都通过，则为 TRUE |

## RT 结构集

`rtstruct_index` 每个 RTSTRUCT 系列具有聚合 ROI 元数据的一行。

```python
import duckdb

BASE = "https://storage.googleapis.com/idc-index-data-artifacts/current/release_artifacts"

# RTSTRUCT series with ROI details
duckdb.sql(f"""
    SELECT i.collection_id, i.SeriesInstanceUID,
           r.total_rois, r.ROINames, r.RTROIInterpretedTypes,
           r.referenced_SeriesInstanceUID
    FROM read_parquet('{BASE}/idc_index.parquet') i
    JOIN read_parquet('{BASE}/rtstruct_index.parquet') r
        ON i.SeriesInstanceUID = r.SeriesInstanceUID
    WHERE i.Modality = 'RTSTRUCT'
    LIMIT 5
""").df()

# Collections with the most RTSTRUCT series
duckdb.sql(f"""
    SELECT i.collection_id,
           COUNT(*) as rtstruct_series,
           ROUND(AVG(r.total_rois), 1) as avg_rois_per_struct
    FROM read_parquet('{BASE}/idc_index.parquet') i
    JOIN read_parquet('{BASE}/rtstruct_index.parquet') r
        ON i.SeriesInstanceUID = r.SeriesInstanceUID
    GROUP BY i.collection_id
    ORDER BY rtstruct_series DESC
    LIMIT 10
""").df()
```

 `rtstruct_index`:

| 中的关键列专栏 |类型 |描述 |
|--------|------|-------------|
| `SeriesInstanceUID` |字符串 |连接键（RTSTRUCT系列）|
| `total_rois` |整数|结构集中的 ROI 数量 |
| `ROINames` |字符串（数组）|不同的 ROI 名称（例如 `["GTV", "Heart", "PTV"]`）|
| `ROIGenerationAlgorithms` |字符串（数组）|不同的生成算法（例如，`["AUTOMATIC", "MANUAL"]`）|
| `RTROIInterpretedTypes` |字符串（数组）|不同的 ROI 类型（例如 `["GTV", "ORGAN", "PTV"]`）|
| `referenced_SeriesInstanceUID` |字符串 |引用的源图像系列的 SeriesInstanceUID |

## 固定到特定版本

```python
import duckdb

# Use a specific data release instead of 'current'
VERSION = "23.10.1"
BASE = f"https://storage.googleapis.com/idc-index-data-artifacts/{VERSION}/release_artifacts"

duckdb.sql(f"SELECT COUNT(*) FROM read_parquet('{BASE}/idc_index.parquet')").df()
```

## 资源

- idc-index-data 版本：https://github.com/ImagingDataCommons/idc-index-data/releases
- idc-index 文档： https://idc-index.readthedocs.io/
  - IDC 门户：https://portal.imaging.datacommons.cancer.gov/
