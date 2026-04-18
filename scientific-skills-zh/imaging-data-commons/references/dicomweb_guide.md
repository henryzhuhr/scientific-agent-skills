# IDC

IDC 的 DICOMweb 指南通过 Google Cloud Healthcare API DICOM 存储提供 DICOMweb 访问。本指南涵盖了实施细节和使用模式。

## 何时使用 DICOMweb

在需要时使用 DICOMweb：
- 与 PACS 系统或 DICOMweb 兼容工具集成
- 流式传输元数据，无需下载完整文件
- 构建自定义查看器或 Web 应用程序
- 使用现有 DICOMweb 客户端库（OHIF、dicomweb-client 等）

 对于大多数用例，`idc-index` 更简单，建议使用。当您特别需要 DICOMweb 协议时，请使用 DICOMweb。

## 端点

### 公共代理（无身份验证）

```
https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb
```

- **100% 数据覆盖率** - 包含来自所有存储桶的所有 IDC 数据
- 指向最新的 IDC 版本自动
- **在新的 IDC 版本上立即更新**
- 每 IP 每日配额（适合测试和适度使用）
- 无需身份验证
- 只读访问
- 注意：URL 中的“仅查看者无下载”是旧命名，没有任何功能意义

### Google Healthcare API （需要身份验证）

```
https://healthcare.googleapis.com/v1/projects/nci-idc-data/locations/us-central1/datasets/idc/dicomStores/idc-store-v{VERSION}/dicomWeb
```

 将 `{VERSION}` 替换为 IDC 版本号。要查找当前版本：

```python
from idc_index import IDCClient
client = IDCClient()
print(client.get_idc_version())  # e.g., "23" for v23
```

- **~96% 数据覆盖率** - 仅复制 `idc-open-data` 存储桶中的数据（其他存储桶中缺少约 4%）
- **更新 1-2 周后** IDC 发布
- 需要身份验证并提供更高版本配额
- 更好的性能（无代理路由）
- 每个版本都有一个新版本存储

请参阅下面的[内容覆盖差异](#content-coverage-differences)和[身份验证](#authentication-for-google-healthcare-api)部分。

## 内容覆盖差异

* *重要提示：** 两个 DICOMweb 端点具有不同的数据覆盖范围。 IDC 公共代理包含比经过身份验证的 Google Healthcare 端点更多的数据。

### 覆盖范围摘要

|端点|覆盖范围|缺失数据|
|---------|----------|-------------|
| **IDC 公共代理** | 100% |无 |
| **谷歌医疗保健API** | 〜96% | ~4%（两个存储桶未复制）|

### Google Healthcare 缺少什么？

Google Healthcare DICOM 存储**仅复制来自 `idc-open-data` S3 存储桶的数据**。它不包括来自两个附加存储桶的数据：

- `idc-open-data-cr`
- `idc-open-data-two`

 这些缺失的存储桶通常每个包含数千个系列，约占 IDC 数据总量的 4%。具体计数因 IDC 版本而异。

 有关存储桶组织、文件结构和直接访问方法的详细信息，请参阅 `cloud_storage_guide.md`。

### 更新时机

- **IDC 公共代理**：新 IDC 版本发布时立即更新
- **Google Healthcare**：每个新 IDC 版本后 1-2 周更新版本

在版本之间，两个端点都保持最新。 1-2 周的延迟仅发生在新 IDC 版本发布后的过渡期内。

* *来自 IDC 文档的警告：** *“Google 托管的 DICOM 存储可能不包含最新版本的 IDC 数据！”* - 在新版本发布后的几周内进行检查。

### 选择正确的端点

* *使用 IDC 公共代理何时：**
- 您需要完整的数据覆盖 (100%)
- 新版本发布后您需要立即获得绝对最新的数据
- 您不想设置 GCP 身份验证
- 您的使用量符合每个 IP 配额（可以通过 support@canceridc.dev 请求增加）
- 您正在访问载玻片显微镜图像逐帧

* *在以下情况下使用 Google Healthcare API：**
- 约 4% 的缺失数据不会影响您的使用案例
- 您需要更高的配额以进行大量使用
- 您需要更好的性能（直接访问，无代理路由）

### 检查您的数据可用性

在选择端点之前，请验证您的数据是否可能丢失存储桶：

```python
from idc_index import IDCClient

client = IDCClient()

# Check which buckets contain your collection's data
results = client.sql_query("""
    SELECT series_aws_url, COUNT(*) as series_count
    FROM index
    WHERE collection_id = 'your_collection_id'
    GROUP BY series_aws_url
""")

print(results)

# Look for URLs containing 'idc-open-data-cr' or 'idc-open-data-two'
# If present, that data won't be available in Google Healthcare endpoint
```

## 实施详细信息

IDC DICOMweb 通过 Google Cloud Healthcare API DICOM 商店提供。该实施遵循 DICOM PS3.18 Web 服务，具有 [Google Healthcare DICOM 一致性声明](https://docs.cloud.google.com/healthcare-api/docs/dicom)中记录的特定特征。

### 支持的操作

|服务 |描述 |支持 |
|---------|-------------|------------|
| QIDO-RS |搜索 DICOM 对象 |是 |
| WADO-RS |检索 DICOM 对象和元数据 |是 |
| STOW-RS |存储 DICOM 对象 |否（IDC 为只读）|

* *不支持：** URI 服务、工作列表服务、非患者实例服务、功能事务

### 可搜索 DICOM 标签 (QIDO-RS)

该实现支持一组有限的可搜索标签：

|水平|可搜索标签 |
|--------------------|-----------------|
|学习| StudyInstanceUID、患者姓名、患者 ID、登录号、参考医生姓名、研究日期 |
|系列|所有研究标签 + SeriesInstanceUID、模态 |
|实例|所有系列标签 + SOPInstanceUID |

* *重要：** 仅支持精确匹配，除了：
- StudyDate：支持范围查询
- PatientName：支持模糊匹配

### 查询限制

- 最大结果：研究/系列搜索 5,000 个；实例为 50,000
- 最大偏移量：1,000,000
- 大于 ~1 MB 的 DICOM 序列标签不会在元数据中返回（而是提供 BulkDataURI）

## 代码示例

所有示例都使用公共代理端点。有关对 Google Healthcare 进行身份验证的访问，请参阅[身份验证部分](#authentication-for-google-healthcare-api)。

### 使用 idc-index 查找 UID

使用 `idc-index` 发现数据，然后使用 DICOMweb 进行元数据访问：

```python
from idc_index import IDCClient

client = IDCClient()

# Find studies of interest
results = client.sql_query("""
    SELECT StudyInstanceUID, SeriesInstanceUID, PatientID, Modality
    FROM index
    WHERE collection_id = 'tcga_luad' AND Modality = 'CT'
    LIMIT 5
""")

# Use these UIDs with DICOMweb
study_uid = results.iloc[0]['StudyInstanceUID']
series_uid = results.iloc[0]['SeriesInstanceUID']
print(f"Study: {study_uid}")
print(f"Series: {series_uid}")
```

### QIDO-RS：按 UID

```python
import requests

base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"

# Search for a specific study
study_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.307623500513044641407722230440"
response = requests.get(
    f"{base_url}/studies",
    params={"StudyInstanceUID": study_uid},
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    studies = response.json()
    print(f"Found {len(studies)} study")
```

### 搜索 QIDO-RS：列出研究中的系列

```python
import requests

base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"
study_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.307623500513044641407722230440"

response = requests.get(
    f"{base_url}/studies/{study_uid}/series",
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    series_list = response.json()
    for series in series_list:
        # DICOM tags are returned as hex codes
        series_uid = series.get("0020000E", {}).get("Value", [None])[0]
        modality = series.get("00080060", {}).get("Value", [None])[0]
        description = series.get("0008103E", {}).get("Value", [""])[0]
        print(f"{modality}: {description}")
```

### QIDO-RS：列出系列中的实例

```python
import requests

base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"
study_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.307623500513044641407722230440"
series_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.217441095430480124587725641302"

response = requests.get(
    f"{base_url}/studies/{study_uid}/series/{series_uid}/instances",
    params={"limit": 10},
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    instances = response.json()
    print(f"Found {len(instances)} instances")
    for inst in instances[:3]:
        sop_uid = inst.get("00080018", {}).get("Value", [None])[0]
        print(f"  SOPInstanceUID: {sop_uid}")
```

### WADO-RS：检索系列元数据

```python
import requests

base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"
study_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.307623500513044641407722230440"
series_uid = "1.3.6.1.4.1.14519.5.2.1.6450.9002.217441095430480124587725641302"

response = requests.get(
    f"{base_url}/studies/{study_uid}/series/{series_uid}/metadata",
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    instances = response.json()
    print(f"Retrieved metadata for {len(instances)} instances")

    # Extract image dimensions from first instance
    if instances:
        inst = instances[0]
        rows = inst.get("00280010", {}).get("Value", [None])[0]
        cols = inst.get("00280011", {}).get("Value", [None])[0]
        print(f"Image dimensions: {rows} x {cols}")
```

### 组合工作流程：idc-index 发现 + DICOMweb 元数据

```python
from idc_index import IDCClient
import requests

# Use idc-index for efficient discovery
idc = IDCClient()
results = idc.sql_query("""
    SELECT StudyInstanceUID, SeriesInstanceUID, Modality, SeriesDescription
    FROM index
    WHERE collection_id = 'nlst' AND Modality = 'CT'
    LIMIT 1
""")

study_uid = results.iloc[0]['StudyInstanceUID']
series_uid = results.iloc[0]['SeriesInstanceUID']
print(f"Found: {results.iloc[0]['SeriesDescription']}")

# Use DICOMweb to stream metadata without downloading files
base_url = "https://proxy.imaging.datacommons.cancer.gov/current/viewer-only-no-downloads-see-tinyurl-dot-com-slash-3j3d9jyp/dicomWeb"

response = requests.get(
    f"{base_url}/studies/{study_uid}/series/{series_uid}/metadata",
    headers={"Accept": "application/dicom+json"}
)

if response.status_code == 200:
    metadata = response.json()
    print(f"Retrieved metadata for {len(metadata)} instances without downloading files")
```

## 常见 DICOM 标签参考

DICOMweb 以十六进制代码形式返回标签。常用标签：

|标签 |名称 |描述 |
|-----|------|-------------|
| 00080018 | SOP实例UID |唯一实例标识符|
| 00080020 |学习日期 |研究进行日期 |
| 00080060 |模态 |成像方式（CT、MR、PT 等）|
| 0008103E |系列描述|系列说明|
| 00100020 |患者 ID |患者标识符|
| 0020000D |研究实例UID |独特的研究标识符|
| 0020000E |系列实例UID |唯一系列标识符|
| 00280010 |行|图像高度（以像素为单位）|
| 00280011 |专栏 |图像宽度（以像素为单位）|

## Google Healthcare API 的身份验证

要使用具有更高配额的 Google Healthcare 端点：

```python
from google.auth import default
from google.auth.transport.requests import Request
import requests

# Get credentials (requires gcloud auth)
credentials, project = default()
credentials.refresh(Request())

# Build authenticated request
base_url = "https://healthcare.googleapis.com/v1/projects/nci-idc-data/locations/us-central1/datasets/idc/dicomStores/idc-store-v23/dicomWeb"

response = requests.get(
    f"{base_url}/studies",
    params={"limit": 5},
    headers={
        "Authorization": f"Bearer {credentials.token}",
        "Accept": "application/dicom+json"
    }
)
```

 * *先决条件：**
1. 安装了 Google Cloud SDK (`gcloud`)
2. 已认证：`gcloud auth application-default login`
3. 帐户有权访问公共 Google Cloud 数据集

## 故障排除

### 问题：搜索查询出现 400 错误请求
- **原因：** 使用不受支持的搜索参数。该实现仅支持用于过滤的特定 DICOM 标签。
- **解决方案：** 使用基于 UID 的查询（StudyInstanceUID、SeriesInstanceUID）。要按模态或其他属性进行过滤，请先使用 `idc-index` 发现 UID，然后使用特定 UID 查询 DICOMweb。

### 问题：403 Forbidden on Google Healthcare Endpoint
- **原因：** 缺少身份验证或权限不足
- **解决方案：** 运行 `gcloud auth application-default login` 并确保您的帐户已access

### 问题：429 请求过多
- **原因：** 超出速率限制
- **解决方案：** 在请求之间添加延迟，减少 `limit` 值，或使用经过身份验证的端点以获得更高的配额

### 问题：204 没有有效 UID 的内容
- **原因：** UID 可能来自当前数据中不存在的旧 IDC 版本，或者数据位于 Google Healthcare 未复制的存储桶中
- **解决方案：**
  - 首先使用 `idc-index` 查询验证 UID 是否存在
  - 检查数据是否位于 `idc-open-data-cr` 或 `idc-open-data-two` 存储桶中（在 Google Healthcare 中不可用）端点）
  - 切换到 IDC 公共代理以获得 100% 覆盖率
  - 在新版本发布期间，Google Healthcare 可能会落后 1-2 周

### 问题：大型元数据响应解析缓慢
- **原因：** 具有许多实例的系列返回大型 JSON
- **解决方案：** 使用 `limit`实例查询上的参数，或通过 SOPInstanceUID

### 查询特定实例问题：响应缺少预期属性
- **原因：** 大于 ~1 MB 的 DICOM 序列被排除在元数据响应中
- **解决方案：** 如果需要所有属性，请使用 WADO-RS 实例检索来检索完整的 DICOM 实例

## 资源

* *IDC 文档：**
- [IDC DICOM 商店](https://learn.canceridc.dev/data/organization-of-data/dicom-stores) - 数据覆盖范围和存储桶详细信息
- [IDC DICOMweb 访问](https://learn.canceridc.dev/data/downloading-data/dicomweb-access) - 端点使用和差异
- [IDC 代理政策](https://learn.canceridc.dev/portal/proxy-policy) - 配额政策和使用限制
- [IDC 用户指南](https://learn.canceridc.dev/) - 完整文档

* *DICOMweb 标准和工具：**
- [Google Healthcare DICOM 一致性声明](https://docs.cloud.google.com/healthcare-api/docs/dicom)
- [DICOMweb 标准](https://www.dicomstandard.org/using/dicomweb)
- [dicomweb-client Python 库](https://dicomweb-client.readthedocs.io/)

* *相关指南：**
- `cloud_storage_guide.md` - 直接存储桶访问、文件组织、CRDC UUID 和版本控制
  - `bigquery_guide.md` - 具有完整 DICOM 属性的高级元数据查询
