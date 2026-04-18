---
name: labarchive-integration
description: 电子实验室笔记本 API 集成。访问笔记本、管理条目/附件、备份笔记本、与 Protocols.io/Jupyter/REDCap 集成，实现编程式 ELN 工作流程。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# LabArchives 集成

## 概述

LabArchives 是一个用于研究文档和数据管理的电子实验室笔记本平台。访问笔记本、管理条目和附件、生成报告以及通过 REST API 以编程方式与第三方工具集成。

## 何时使用此技能

此技能应在以下情况下使用：
- 使用 LabArchives REST API 实现笔记本自动化
- 以编程方式备份笔记本
- 创建或管理笔记本条目和附件
- 生成站点报告和分析
- 将 LabArchives 与第三方工具（Protocols.io、Jupyter、REDCap）集成
- 自动将数据上传到电子实验室笔记本
- 以编程方式管理用户访问和权限

## 核心功能

### 1. 身份验证和配置

为 LabArchives API 集成设置 API 访问凭据和区域端点。

* *先决条件：**
- 启用 API 访问的企业 LabArchives 许可证
- 来自 LabArchives 管理员的 API 访问密钥 ID 和密码
- 用户身份验证凭据（电子邮件和外部应用程序）密码）

* *配置设置：**

使用`scripts/setup_config.py`脚本创建配置文件：

```bash
python3 scripts/setup_config.py
```

这将创建一个`config.yaml`文件，其中包含以下内容结构：

```yaml
api_url: https://api.labarchives.com/api  # or regional endpoint
access_key_id: YOUR_ACCESS_KEY_ID
access_password: YOUR_ACCESS_PASSWORD
```

* *区域 API 端点：**
- 美国/国际：`https://api.labarchives.com/api`
- 澳大利亚：`https://auapi.labarchives.com/api`
- 英国：`https://ukapi.labarchives.com/api`

有关详细的身份验证说明和故障排除，参考`references/authentication_guide.md`.

### 2.用户信息检索

获取后续API操作所需的用户ID（UID）和访问信息。

* *工作流程：**

1. 使用登录凭证
2调用`users/user_access_info` API方法。解析 XML/JSON 响应以提取用户 ID (UID)
3. 使用UID通过`users/user_info_via_id`

检索详细的用户信息**使用 Python 包装器的示例：**

```python
from labarchivespy.client import Client

# Initialize client
client = Client(api_url, access_key_id, access_password)

# Get user access info
login_params = {'login_or_email': user_email, 'password': auth_token}
response = client.make_call('users', 'user_access_info', params=login_params)

# Extract UID from response
import xml.etree.ElementTree as ET
uid = ET.fromstring(response.content)[0].text

# Get detailed user info
params = {'uid': uid}
user_info = client.make_call('users', 'user_info_via_id', params=params)
```

### 3. 笔记本操作

管理笔记本访问、备份和元数据检索。

* *关键操作：**

- **列出笔记本：** 检索用户可访问的所有笔记本
- **备份笔记本：** 下载包含可选附件的完整笔记本数据
- **获取笔记本 ID：** 检索机构定义的笔记本标识符以与赠款/项目管理系统集成
- **获取笔记本成员：** 列出有权访问特定笔记本的所有用户
- **获取笔记本设置：** 检索笔记本的配置和权限

  * *笔记本备份示例：**

使用`scripts/notebook_operations.py` 脚本：

```bash
# Backup with attachments (default, creates 7z archive)
python3 scripts/notebook_operations.py backup --uid USER_ID --nbid NOTEBOOK_ID

# Backup without attachments, JSON format
python3 scripts/notebook_operations.py backup --uid USER_ID --nbid NOTEBOOK_ID --json --no-attachments
```

* *API 端点格式：**
```
https://<api_url>/notebooks/notebook_backup?uid=<UID>&nbid=<NOTEBOOK_ID>&json=true&no_attachments=false
```

 完整的 API 方法文档，请参阅 `references/api_reference.md`.

### 4. 条目和附件管理

创建、修改和管理笔记本条目和文件附件。

* *条目操作：**
- 在笔记本中创建新条目
- 为现有条目添加注释
- 创建条目零件/组件
- 上传文件附件到条目

* *附件工作流程：**

使用 `scripts/entry_operations.py` 脚本：

```bash
# Upload attachment to an entry
python3 scripts/entry_operations.py upload --uid USER_ID --nbid NOTEBOOK_ID --entry-id ENTRY_ID --file /path/to/file.pdf

# Create a new entry with text content
python3 scripts/entry_operations.py create --uid USER_ID --nbid NOTEBOOK_ID --title "Experiment Results" --content "Results from today's experiment..."
```

* *支持的文件类型：**
- 文档（PDF、DOCX、TXT）
- 图像（PNG、JPG、 TIFF)
- 数据文件（CSV、XLSX、HDF5）
- 科学格式（CIF、MOL、PDB）
- 档案（ZIP、7Z）

### 5. 站点报告和分析

生成有关笔记本使用情况、活动和合规性的机构报告（企业专题）.

* *可用报告：**
- 详细使用情况报告：用户活动指标和参与统计数据
- 详细笔记本报告：笔记本元数据、成员列表和设置
- PDF/离线笔记本生成报告：导出合规跟踪
- 笔记本成员报告：访问控制和协作分析
- 笔记本设置报告：配置和权限审计

* *报告生成：**

```python
# Generate detailed usage report
response = client.make_call('site_reports', 'detailed_usage_report',
                           params={'start_date': '2025-01-01', 'end_date': '2025-10-20'})
```

### 6.第三方集成

LabArchives与众多科学软件平台集成。此技能提供以编程方式利用这些集成的指导。

* *支持的集成：**
- **Protocols.io:** 将协议直接导出到 LabArchives 笔记本
- **GraphPad Prism:** 导出分析和图形（版本 8+）
- **SnapGene:** 直接分子生物学工作流程集成
- **Geneious：** 生物信息学分析导出
- **Jupyter：** 嵌入Jupyter笔记本作为条目
- **REDCap：** 临床数据采集集成
- **Qeios：** 研究发布平台
- **SciSpace：** 文献管理

* *OAuth身份验证：**
LabArchives 现在使用 OAuth 进行所有新集成。旧集成可以使用 API 密钥身份验证。

有关详细的集成设置说明和用例，请参阅 `references/integrations.md`。

## 常见工作流程

### 完整笔记本备份工作流程

1. 认证并获取用户ID
2. 列出所有可访问的笔记本电脑
3. 遍历笔记本并备份每个
4. 使用时间戳元数据存储备份

```bash
# Complete backup script
python3 scripts/notebook_operations.py backup-all --email user@example.edu --password AUTH_TOKEN
```

### 自动数据上传工作流程

1. 使用 LabArchives API
2 进行身份验证。识别目标笔记本电脑和条目
3. 上传实验数据文件
4. 将元数据注释添加到条目
5. 生成活动报告

### 集成工作流程示例（Jupyter → LabArchives）

1. 将 Jupyter Notebook 导出为 HTML 或 PDF
2. 使用entry_operations.py上传到LabArchives
3. 添加带有执行时间戳和环境信息的注释
4. 轻松检索的标签条目

## Python 包安装

安装 `labarchives-py` 包装器以简化 API 访问：

```bash
git clone https://github.com/mcmero/labarchives-py
cd labarchives-py
uv pip install .
```

或者，通过 Python 的 `requests` 库使用直接 HTTP 请求进行自定义实现。

## 最佳做法

1. **速率限制：** 在 API 调用之间实施适当的延迟，以避免限制
2. **错误处理：** 始终将 API 调用包装在带有适当日志记录的 try- except 块中
3. **身份验证安全性：** 将凭据存储在环境变量或安全配置文件中（切勿在代码中）
4. **备份验证：**笔记本备份后，验证文件的完整性和完整性
5. **增量操作：** 对于大型笔记本，使用分页和批处理
6. **区域端点：** 使用正确的区域 API 端点以获得最佳性能

## 故障排除

* *常见问题：**

- **401 未经授权：** 验证访问密钥 ID 和密码是否正确；检查您的帐户是否已启用 API 访问
- **404 未找到：** 确认笔记本 ID (nbid)存在并且用户具有访问权限
- **403 禁止：** 检查请求操作的用户权限
- **空响应：** 确保正确提供所需参数（uid、nbid）
- **附件上传失败：** 验证文件大小限制和格式兼容性

如需更多支持，请通过support@labarchives.com联系LabArchives。

## 资源

此技能包括支持LabArchives API集成的捆绑资源：

### 脚本/

- `setup_config.py`：API 凭据的交互式配置文件生成器
- `notebook_operations.py`：用于列出、备份和管理笔记本的实用程序
- `entry_operations.py`：用于创建条目和上传附件的工具

### 引用/

- `api_reference.md`：综合 API 端点包含参数和示例的文档
- `authentication_guide.md`：详细的身份验证设置和配置说明
- `integrations.md`：第三方集成设置指南和用例
