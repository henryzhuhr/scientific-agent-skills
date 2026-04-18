# IDC

IDC 云存储指南维护在 Google Cloud Storage (GCS)和 AWS S3 之间镜像的公共云存储桶中的所有 DICOM 文件。本指南涵盖存储桶组织、文件结构、访问方法和版本控制。

## 何时使用直接云存储访问

在需要时使用直接存储桶访问：
- 通过并行传输实现最大下载性能
- 与云原生工作流程集成（例如，在云虚拟机上运行分析）
- 从 s5cmd 或等工具进行编程访问gsutil
  - 访问特定文件版本以实现可重复性

 对于大多数用例，`idc-index` 更简单，建议使用 - 它在内部使用 s5cmd 从这些相同的 S3 存储桶下载，自动处理 UUID 查找。当您需要原始文件访问、自定义并行化或构建云原生管道时，请使用直接云存储。

## 存储桶

IDC 根据许可和内容类型跨多个存储桶组织数据。所有存储桶都在 AWS 和 GCS 之间镜像，具有相同的内容和文件路径。

### 存储桶摘要

|目的| AWS S3 存储桶 | GCS 铲斗 |许可证|内容 |
|---------|----------------|------------|---------|---------|
|原始数据| `idc-open-data` | `idc-open-data` |无商业限制 | >90% 的 IDC 数据 |
|头部扫描 | `idc-open-data-two` | `idc-open-idc1` |无商业限制 |可能包含头部成像的集合|
|商业限制| `idc-open-data-cr` | `idc-open-cr` |商业用途受限 (CC BY-NC) | ~4% 的数据 |

* *注意：**
- 所有 AWS 存储桶均位于 AWS 区域中 `us-east-1`
- 在 IDC v19 之前，GCS 使用 `public-datasets-idc`（现已由 `idc-open-data` 取代）
- 头部扫描存储桶的存在是为了未来有关面部成像数据的潜在政策更改
- **重要**使用`idc-index` 获取许可证信息 - 不依赖存储桶名称！ 

### 为什么要使用多个桶？

1. **许可分离**：带有商业用途限制（CC BY-NC）的数据在`idc-open-data-cr` / `idc-open-cr`中隔离，以防止意外商业用途
2. **头部扫描处理**：由 TCIA 标记为可能包含头部扫描的集合位于单独的存储桶 (`idc-open-data-two` / `idc-open-idc1`)中，以实现未来潜在的策略合规性 
3. **历史原因**：存储桶结构随着 IDC 的发展并与不同的云程序合作而演变

## 存储桶内的文件组织

文件是按 CRDC UUID 组织的，而不是 DICOM UID 组织的。这可以实现版本控制，同时保持跨云提供商的一致路径。

### 目录结构

```
<bucket>/
└── <crdc_series_uuid>/
    ├── <crdc_instance_uuid_1>.dcm
    ├── <crdc_instance_uuid_2>.dcm
    └── ...
```

* *示例路径：**
```
s3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/0d73f84e-70ae-4eeb-96a0-1c613b5d9229.dcm
```

- `7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9` = 系列 UUID（文件夹）
- `0d73f84e-70ae-4eeb-96a0-1c613b5d9229.dcm` = 实例 UUID（文件）

### CRDC UUID 与 DICOM UID

|标识符类型|格式|更改时间 |用于|
|-----------------|--------|-------------|---------|
| DICOM UID（例如 SeriesInstanceUID）|数字（例如，`1.3.6.1.4...`）|从不（包含在 DICOM 元数据中）|临床鉴定、DICOMweb查询|
| CRDC UUID（例如 crdc_series_uuid）| UUID（例如，`e127d258-37c2-...`）|内容变更 |文件路径、版本控制、再现性 |

* *关键见解：** 如果系列内容发生更改（添加/删除实例、更正元数据），则单个 DICOM SeriesInstanceUID 可能在 IDC 版本中具有多个 CRDC 系列 UUID。 CRDC UUID 唯一标识数据的特定版本。

### 将 DICOM UID 映射到文件路径

使用 `idc-index` 从 DICOM 标识符获取文件 URL：

```python
from idc_index import IDCClient

client = IDCClient()

# Get all file URLs for a series
series_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.217441095430480124587725641302"
urls = client.get_series_file_URLs(seriesInstanceUID=series_uid)

for url in urls[:3]:
    print(url)
# Returns S3 URLs like: s3://idc-open-data/<crdc_series_uuid>/<crdc_instance_uuid>.dcm
```

 或者直接查询索引获取 URL列：

```python
# Get series-level URL (points to folder)
result = client.sql_query("""
    SELECT SeriesInstanceUID, series_aws_url
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
    LIMIT 3
""")

print(result[['SeriesInstanceUID', 'series_aws_url']])
```

* *索引中的可用 URL 列：**
- `series_aws_url`：系列文件夹的 S3 URL（例如，`s3://idc-open-data/uuid/*`）

GCS URL 遵循相同的路径结构 - 将 `s3://` 替换为`gs://`（例如，`gs://idc-open-data/uuid/*`）。使用 `idc-index` 下载方法时，GCS 访问在内部处理。

## 访问云存储

所有 IDC 存储桶通过与 AWS 开放数据和 Google 公共数据计划合作，支持免费出口（无下载费用）。无需身份验证。

### AWS S3 访问

* *使用 AWS CLI（无需帐户）：**
```bash
# List bucket contents
aws s3 ls --no-sign-request s3://idc-open-data/

# List files in a series folder
aws s3 ls --no-sign-request s3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/

# Download a single file
aws s3 cp --no-sign-request \
    s3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/0d73f84e-70ae-4eeb-96a0-1c613b5d9229.dcm \
    ./local_file.dcm

# Download entire series folder
aws s3 cp --no-sign-request --recursive \
    s3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/ \
    ./series_folder/
```

* *使用 s5cmd（批量下载速度更快）：**
```bash
# Install s5cmd
# macOS: brew install s5cmd
# Linux: download from https://github.com/peak/s5cmd/releases

# Download specific series
s5cmd --no-sign-request cp 's3://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/*' ./local_folder/

# Download from manifest file
s5cmd --no-sign-request run manifest.txt
```

* *s5cmd清单格式：** `s5cmd run` 命令需要每行一个 s5cmd 命令，而不仅仅是 URL：
```
cp s3://idc-open-data/uuid1/instance1.dcm ./local_folder/
cp s3://idc-open-data/uuid1/instance2.dcm ./local_folder/
cp s3://idc-open-data/uuid2/instance3.dcm ./local_folder/
```

IDC 门户以此格式导出清单。以编程方式创建清单时，请使用 `idc-index` 下载方法（在内部处理此问题），而不是手动构建清单。

### GCS Access

* *使用 gsutil:**
```bash
# List bucket contents
gsutil ls gs://idc-open-data/

# Download a series folder
gsutil -m cp -r gs://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/ ./local_folder/
```

* *使用 gcloud 存储（较新版本） CLI):**
```bash
gcloud storage cp -r gs://idc-open-data/7a6b2389-53c6-4c5b-b07f-6d1ed4a3eed9/ ./local_folder/
```

### Python 直接访问

```python
import s3fs
import gcsfs
from idc_index import IDCClient

# First, get a file URL from idc-index
client = IDCClient()
result = client.sql_query("""
    SELECT series_aws_url
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
    LIMIT 1
""")
# series_aws_url is like: s3://idc-open-data/<uuid>/*
series_url = result['series_aws_url'].iloc[0]
series_path = series_url.replace('s3://', '').rstrip('/*')  # e.g., "idc-open-data/<uuid>"

# AWS S3 access
s3 = s3fs.S3FileSystem(anon=True)
files = s3.ls(series_path)
with s3.open(files[0], 'rb') as f:
    data = f.read()

# GCS access (same path structure as AWS)
gcs = gcsfs.GCSFileSystem(token='anon')
files = gcs.ls(series_path)
with gcs.open(files[0], 'rb') as f:
    data = f.read()
```

## 版本控制和可重复性

IDC 每 2-4 个月发布新的数据版本。版本控制系统通过保留所有历史数据来确保可重复性。

### 版本控制的工作原理

1. **快照**：每个IDC版本（v1、v2、...、v23等）代表发布时间
2时所有数据的完整快照。 **基于UUID**：当数据发生变化时，分配新的CRDC UUID；旧的 UUID 仍然可以访问
3. **累计桶**：所有版本共存于同一个桶中——老系列文件夹

* *版本变更场景：**
|更改类型 | DICOM UID | CRDC UUID |效果 |
|-------------|------------|------------|--------|
|新系列已添加 |新 |新 |存储桶中的新文件夹 |
|实例已添加至系列 |相同 |新系列UUID |新建文件夹，实例可能重复|
|元数据已更正 |相同或新 |新 |包含更新文件的新文件夹 |
|系列已删除 |不适用 |不适用 |旧文件夹保留，不在当前索引中 |

* *数据删除警告：** 在极少数情况下（例如，数据所有者请求、PHI 事件），数据可能会从 IDC 中完全删除，包括从所有历史版本中删除。

* *BigQuery 版本化数据集（仅限元数据，不是文件存储）：**

为了查询特定于版本的元数据，BigQuery 提供版本化表。有关详细信息，请参阅 `bigquery_guide.md`。
- `bigquery-public-data.idc_current` — 最新版本的别名
- `bigquery-public-data.idc_v23` — 特定版本（将 23 替换为所需版本）

### 重现以前的分析

确保重现性的最简单方法是保存您在分析时使用的数据的 `crdc_series_uuid` 值：

```python
from idc_index import IDCClient
import json

client = IDCClient()

# Select data for your analysis
selection = client.sql_query("""
    SELECT crdc_series_uuid
    FROM index
    WHERE collection_id = 'tcga_luad'
      AND Modality = 'CT'
    LIMIT 10
""")
series_uuids = list(selection['crdc_series_uuid'])

# Download the data
client.download_from_selection(seriesInstanceUID=series_uuids, downloadDir="./data")

# Save a manifest for reproducibility
manifest = {
    "crdc_series_uuids": series_uuids,
    "download_date": "2024-01-15",
    "idc_version": client.get_idc_version(),
    "description": "CT scans for lung cancer analysis"
}
with open("analysis_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

# Later, reproduce the exact dataset:
with open("analysis_manifest.json") as f:
    manifest = json.load(f)
client.download_from_selection(
    seriesInstanceUID=manifest["crdc_series_uuids"],
    downloadDir="./reproduced_data"
)
```

 由于 `crdc_series_uuid` 标识每个系列的不可变版本，保存这些 UUID 可以保证您以后可以检索完全相同的文件。

## 存储桶、版本和其他访问之间的关系方法

### 数据覆盖率比较

|访问方式|包括桶 |覆盖范围|版本|
|-------------|--------------------|----------|----------|
|直接访问存储桶 |所有 3 个桶 | 100% |所有历史|
| `idc-index` 下载 |所有 3 个桶 | 100% |当前 + 先前版本索引 |
| IDC门户 |所有 3 个桶 | 100% |仅当前|
| DICOMweb 公共代理 |所有 3 个桶 | 100% |仅当前|
|谷歌医疗 DICOM |仅`idc-open-data` | 〜96% |仅当前 |

* *重要：** Google Healthcare API DICOM 存储仅复制来自 `idc-open-data` 的数据。 `idc-open-data-two` 和 `idc-open-data-cr` 中的数据（约占总数的 4%）无法通过 Google Healthcare DICOMweb 端点获得。

## 最佳实践

- **使用 `idc-index` 进行发现**：首先查询元数据，然后访问具有已知 UUID 的存储桶
- **将默认值下载到 AWS存储桶**：如果需要，请求 GCS
- **保存清单**：存储 `series_aws_url` 或 `crdc_series_uuid` 值以实现可重复性
- **检查许可证**：在商业使用之前查询 `license_short_name`； CC-NC数据需要非商业用途
- **使用当前版本除非复制**：`index`表有当前数据；仅使用 `prior_versions_index` 以获得精确的再现性

## 故障排除

### 问题：访问存储桶时“访问被拒绝”
- **原因：** 使用签名请求或错误的存储桶名称
- **解决方案：** 通过 AWS CLI 使用 `--no-sign-request` 标志，或`anon=True` 与 Python 库

### 问题：在预期路径中找不到文件
- **原因：** 使用 DICOM UID 而不是 CRDC UUID，或在较新版本中更改数据
- **解决方案：** 查询 `idc-index` 以获取当前的 `series_aws_url`，或检查`prior_versions_index` 用于历史路径

### 问题：下载的文件与预期的系列不匹配
- **原因：**系列在较新的IDC版本中进行了修订
- **解决方案：** 使用`prior_versions_index`找到您需要的确切版本；比较 `crdc_series_uuid` 值

### 问题：Google Healthcare DICOMweb
- **原因：** Google Healthcare 仅镜像 `idc-open-data` 存储桶（约 96% 的数据）
- **解决方案：** 使用 IDC 公共代理实现 100% 覆盖，或直接访问存储桶

## 资源

* *IDC文档：**
- [文件和元数据](https://learn.canceridc.dev/data/organization-of-data/files-and-metadata) - 存储桶组织详细信息
- [数据版本控制](https://learn.canceridc.dev/data/data-versioning) - 版本控制方案说明
- [解决GUID 和 UUID](https://learn.canceridc.dev/data/organization-of-data/guids-and-uuids) - CRDC UUID 文档
- [直接从云加载](https://learn.canceridc.dev/data/downloading-data/direct-loading) - 云访问的 Python 示例

* *AWS 资源：**
- [AWS Open Data Registry 上的 NCI IDC](https://registry.opendata.aws/nci-imaging-data-commons/) - 存储桶 ARN 和访问信息
- [s5cmd](https://github.com/peak/s5cmd) - 高性能 S3 客户端（由 idc-index 内部使用）
- [AWS CLI S3命令](https://docs.aws.amazon.com/cli/latest/reference/s3/) - 标准 AWS 命令行界面
  - [Boto3 S3 文档](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html) - 适用于 Python 的 AWS 开发工具包

* *Google Cloud 资源：**
- [gsutil 工具](https://cloud.google.com/storage/docs/gsutil) - Google Cloud Storage 命令行工具
- [gcloud storage 命令](https://cloud.google.com/sdk/gcloud/reference/storage) - 现代 GCS CLI（推荐使用 gsutil）
- [Google Cloud Storage Python client](https://cloud.google.com/python/docs/reference/storage/latest) - 适用于 Python 的 GCS SDK

* *相关指南：**
- `dicomweb_guide.md` - DICOMweb API 访问（直接存储桶访问的替代方案）
- `bigquery_guide.md` - 高级元数据查询，包括版本化数据集
