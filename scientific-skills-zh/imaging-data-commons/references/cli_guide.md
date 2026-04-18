# idc-index 命令行界面指南

`idc-index` 软件包提供了从 NCI Imaging Data Commons 下载 DICOM 数据的命令行工具，无需编写 Python 代码。

## 安装

```bash
pip install --upgrade idc-index
```

 安装后，`idc` 命令可在您的计算机中使用。终端.

## 可用命令

|命令 |用途 |
|---------|---------|
| `idc download` |自动检测输入类型的通用下载|
| `idc download-from-manifest` |从清单文件下载并进行验证和进度跟踪 |
| `idc download-from-selection` |具有多个条件的基于过滤器的下载 |

- --

## idc download

智能解释输入的通用下载命令。它确定输入是否对应于清单文件路径或标识符列表（collection_id、PatientID、StudyInstanceUID、SeriesInstanceUID、crdc_series_uuid）。选项 |描述|
|--------|-------------|
| `--download-dir` |目标目录（默认：当前目录）|
| `--dir-template` |目录层次结构模板（默认：`%collection_id/%PatientID/%StudyInstanceUID/%Modality_%SeriesInstanceUID`）|
| `--log-level` |详细程度：调试、信息、警告、错误、严重 |

### 目录模板变量

在 `--dir-template` 中使用这些变量来组织下载：

- `%collection_id` - 集合标识符
- `%PatientID` - 患者标识符
- `%StudyInstanceUID` - 研究 UID
- `%SeriesInstanceUID` - 系列 UID
- `%Modality` - 成像模式（CT、MR、PT、等）

* *示例：**

```bash
# Flat structure (all files in one directory)
idc download rider_pilot --download-dir ./data --dir-template ""

# Simplified hierarchy
idc download rider_pilot --download-dir ./data --dir-template "%collection_id/%PatientID/%Modality"
```

- --

## idc download-from-manifest

专门用于从具有内置验证、进度跟踪和恢复功能的清单文件下载。

### 用法

```bash
# Basic download from manifest
idc download-from-manifest --manifest-file cohort.txt --download-dir ./data

# With progress bar and validation
idc download-from-manifest --manifest-file cohort.txt --download-dir ./data --show-progress-bar

# Resume interrupted download with s5cmd sync
idc download-from-manifest --manifest-file cohort.txt --download-dir ./data --use-s5cmd-sync
```

### 选项

|选项 |说明|
|--------|-------------|
| `--manifest-file` | **必需。** 包含 S3 URL |
| 的清单文件路径`--download-dir` | **必填。** 目标目录 |
| `--validate-manifest` |下载前验证清单（默认启用）|
| `--show-progress-bar` |显示下载进度|
| `--use-s5cmd-sync` |启用可断点下载 - 跳过已下载的文件 |
| `--quiet` |抑制子进程输出 |
| `--dir-template` |目录层次结构模板|
| `--log-level` |记录详细程度 |

### 清单文件格式

清单文件包含 S3 URL，每行一个：

```
s3://idc-open-data/cb09464a-c5cc-4428-9339-d7fa87cfe837/*
s3://idc-open-data/88f3990d-bdef-49cd-9b2b-4787767240f2/*
```

* *如何获取清单文件：**

1. **IDC 门户**：将队列选择导出为清单
2. **Python查询**：从SQL结果生成

```python
from idc_index import IDCClient

client = IDCClient()
results = client.sql_query("""
    SELECT series_aws_url
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
""")

with open('ct_manifest.txt', 'w') as f:
    for url in results['series_aws_url']:
        f.write(url + '\n')
```

- --

## idc download-from-selection

使用过滤条件下载数据。过滤器按顺序应用。

### 用法

```bash
# Download by collection
idc download-from-selection --collection-id rider_pilot --download-dir ./data

# Download specific series
idc download-from-selection --series-instance-uid "1.3.6.1.4.1.9328.50.1.69736" --download-dir ./data

# Multiple filters
idc download-from-selection --collection-id nlst --patient-id "100004" --download-dir ./data

# Dry run - see what would be downloaded without actually downloading
idc download-from-selection --collection-id tcga_luad --dry-run --download-dir ./data
```

### 选项

|选项 |描述|
|--------|-------------|
| `--download-dir` | **必填。** 目标目录 |
| `--collection-id` |按集合标识符过滤 |
| `--patient-id` |按患者标识符过滤|
| `--study-instance-uid` |按研究 UID 过滤 |
| `--series-instance-uid` |按系列 UID 过滤 |
| `--crdc-series-uuid` |按 CRDC UUID |
| 过滤`--dry-run` |无需下载即可计算队列大小|
| `--show-progress-bar` |显示下载进度|
| `--use-s5cmd-sync` |启用断点续传下载|
| `--dir-template` |目录层次结构模板 |

### 试运行大小估计

在提交之前使用 `--dry-run` 估计下载大小：

```bash
idc download-from-selection --collection-id nlst --dry-run --download-dir ./data
```

这显示：
- 匹配过滤器的系列数
- 总下载量size
- 未下载任何文件

- --

## 常用工作流程

### 1. 下载用于测试的小型集合

```bash
# rider_pilot is ~1GB - good for testing
idc download rider_pilot --download-dir ./test_data
```

### 2. 带进度和恢复的大型数据集

```bash
# Use s5cmd sync for large downloads - can resume if interrupted
idc download-from-selection \
    --collection-id nlst \
    --download-dir ./nlst_data \
    --show-progress-bar \
    --use-s5cmd-sync
```

### 3. 下载前估算大小

```bash
# Check size first
idc download-from-selection --collection-id tcga_luad --dry-run --download-dir ./data

# Then download if size is acceptable
idc download-from-selection --collection-id tcga_luad --download-dir ./data
```

### 4. 通过Python + 下载特定模态CLI

```python
# First, query for series UIDs in Python
from idc_index import IDCClient

client = IDCClient()
results = client.sql_query("""
    SELECT SeriesInstanceUID
    FROM index
    WHERE collection_id = 'nlst'
      AND Modality = 'CT'
      AND BodyPartExamined = 'CHEST'
    LIMIT 50
""")

# Save to manifest
results['SeriesInstanceUID'].to_csv('my_series.csv', index=False, header=False)
```

```bash
# Then download via CLI
idc download my_series.csv --download-dir ./lung_ct
```

- --

## 内置安全功能

CLI 包括多个安全功能：

- **磁盘空间检查**：在开始下载之前验证足够的空间
- **清单验证**：验证默认清单文件格式
- **进度跟踪**：用于监控大下载的可选进度条
- **恢复功能**：使用`--use-s5cmd-sync`继续中断的下载

- --

## 故障排除

### 下载中断

使用`--use-s5cmd-sync`恢复：

```bash
idc download-from-manifest --manifest-file cohort.txt --download-dir ./data --use-s5cmd-sync
```

### 连接超时

对于不稳定的网络，使用Python小批量下载，生成多个清单，然后顺序下载。

- --

## 另请参阅

- [idc-index文档](https://idc-index.readthedocs.io/)
- [IDC 门户](https://portal.imaging.datacommons.cancer.gov/) - 交互式队列建设
- [IDC 教程](https://github.com/ImagingDataCommons/IDC-Tutorials)
