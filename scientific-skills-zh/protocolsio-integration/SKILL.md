---
name: protocolsio-integration
description: 与 Protocols.io API 集成，用于管理科学协议。当使用protocols.io搜索、创建、更新或发布协议时，应该使用此技能；管理方案步骤和材料；处理讨论和评论；整理工作空间；上传和管理文件；或将protocols.io 功能集成到工作流程中。适用于协议发现、协作协议开发、实验跟踪、实验室协议管理和科学文档。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Protocols.io 集成

## 概述

Protocols.io 是一个用于开发、共享和管理科学协议的综合平台。此技能提供与protocols.io API v3的完整集成，支持以编程方式访问协议、工作区、讨论、文件管理和协作功能。

## 何时使用此技能

在以下任何场景中使用protocols.io时使用此技能：

- **协议发现**：通过关键字、DOI或类别搜索现有协议
- **协议管理**：创建、更新或发布科学协议
- **步骤管理**：添加、编辑或组织协议步骤和程序
- **协作开发**：与团队成员就共享协议进行合作
- **工作区组织**：管理实验室或机构协议存储库
- **讨论和反馈**：添加或响应协议注释
- **文件管理**：将数据文件、图像或文档上传到协议
- **实验跟踪**：记录协议执行和结果
- **数据导出**：备份或迁移协议集合
- **集成项目**：构建与协议交互的工具。io

## 核心功能

此技能提供跨五个主要功能的全面指导区域：

### 1. 身份验证和访问

使用访问令牌和 OAuth 流程管理 API 身份验证。包括客户端访问令牌（用于个人内容）和 OAuth 令牌（用于多用户应用程序）。

* *关键操作：**
- 生成 OAuth 流程的授权链接
- 交换访问令牌的授权代码
- 刷新过期的令牌
- 管理速率限制和权限

* *参考：**阅读`references/authentication.md`了解详细的身份验证过程、OAuth实现和安全最佳实践。

### 2.协议操作

从创建到发布的完整协议生命周期管理。

* *关键操作：**
- 通过关键字、过滤器或DOI
搜索和发现协议-检索所有协议的详细协议信息步骤
- 使用元数据和标签创建新协议
- 更新协议信息和设置
- 管理协议步骤（创建、更新、删除、重新排序）
- 处理协议材料和试剂
- 通过DOI发行发布协议
- 为快速访问添加书签协议
- 生成协议PDFs

* *参考：**阅读 `references/protocols_api.md` 以获取全面的协议管理指南，包括 API 端点、参数、常见工作流程和示例。

### 3. 讨论与协作

通过评论和讨论启用社区参与。

* *关键操作：**
- 查看协议级别和步骤级评论
- 创建新评论和线索回复
- 编辑或删除您自己的评论
- 分析讨论模式和反馈
- 回复用户问题和问题

* *参考：** 阅读 `references/discussions.md` 以进行讨论管理、评论线索和协作工作流程。

### 4. 工作空间管理

使用基于角色的权限组织团队工作空间内的协议。

* *关键操作：**
- 列出和访问用户工作空间
- 检索工作空间详细信息和成员列表
- 请求访问或加入工作空间
- 列出工作区特定协议
- 在工作区中创建协议
- 管理工作区权限和协作

* *参考：** 阅读 `references/workspaces.md` 了解工作区组织、权限管理和团队协作模式。

### 5. 文件操作

上传、组织和管理与协议关联的文件。

* *关键操作：**
- 搜索工作区文件和文件夹
- 上传带有元数据和标签的文件
- 下载文件并验证上传
- 将文件组织到文件夹层次结构中
- 更新文件元数据
- 删除和恢复文件
- 管理存储和组织

* *参考：**阅读`references/file_manager.md`了解文件上传过程、组织策略和存储管理。

### 6.附加功能

补充功能，包括配置文件、通知和导出。

* *关键操作：**
- 管理用户配置文件和设置
- 查询最近发布的协议
- 创建和跟踪实验记录
- 接收和管理通知
- 导出组织数据进行存档

* *参考：**阅读`references/additional_features.md`以进行配置文件管理、发布发现、实验跟踪和数据导出。

## 获取开始

### 步骤1：身份验证设置

在使用任何protocols.io API功能之前：

1. 获取访问令牌（CLIENT_ACCESS_TOKEN 或 OAUTH_ACCESS_TOKEN）
2. 详细认证流程请阅读`references/authentication.md`
3. 安全地存储令牌
4. 在所有请求中包含以下内容：`Authorization: Bearer YOUR_TOKEN`

### 步骤 2：确定您的用例

确定哪个功能领域可以满足您的需求：

- **使用协议？** → 阅读 `references/protocols_api.md`
- **管理团队协议？** → 阅读`references/workspaces.md`
- **处理评论/反馈？** → 阅读 `references/discussions.md`
- **上传文件/数据？** → 阅读 `references/file_manager.md`
- **跟踪实验或配置文件？** → 阅读 `references/additional_features.md`

### 步骤 3：实施集成

遵循相关参考文件中的指导：

- 每个参考都包含详细的端点文档
- 指定了 API 参数和请求/响应格式
- 提供了常见用例和工作流程以及示例
- 包括最佳实践和错误处理指南

## 基本 URL 和请求格式

所有 API 请求都使用基本 URL URL：
```
https://protocols.io/api/v3
```

所有请求都需要授权标头：
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

大多数端点支持带有 `Content-Type: application/json`.

## 内容格式选项的 JSON 请求/响应格式

许多端点支持`content_format` 参数控制如何返回协议内容：

- `json`：Draft.js JSON 格式（默认）
- `html`：HTML 格式
- `markdown`：Markdown 格式

 作为查询参数包含： `?content_format=html`

## 速率限制

请注意 API 速率限制：

- **标准端点**：每个用户每分钟 100 个请求
- **PDF 端点**：5 个请求/分钟（登录）、3 个请求/分钟（无符号）

对速率限制错误（HTTP 429）实施指数退避。

## 常见工作流程

### 工作流程1：导入和分析协议

从protocols.io分析现有协议：

1. **搜索**：使用`GET /protocols`配合关键字查找相关协议
2. **检索**：使用 `GET /protocols/{protocol_id}`
3 获取完整详细信息。 **提取**：解析步骤、材料和元数据以进行分析
4. **评论讨论**：查看 `GET /protocols/{id}/comments` 的用户反馈 
5. **导出**：如果需要离线参考，则生成 PDF

  * *参考文件**：`protocols_api.md`、`discussions.md`

### 工作流程 2：创建和发布协议

创建新协议并使用 DOI 发布：

1. **身份验证**：确保您具有有效的访问令牌（请参阅 `authentication.md`）
2. **创建**：使用`POST /protocols`，标题和描述为
3. **添加步骤**：对于每个步骤，使用 `POST /protocols/{id}/steps`
4. **添加材料**：记录步骤组件
5中的试剂。 **审核**：验证所有内容是否完整且准确
6. **发布**：使用 `POST /protocols/{id}/publish`

 发布 DOI **参考文件**：`protocols_api.md`、`authentication.md`

### 工作流程 3：协作实验室工作空间

设置团队协议管理：

1. **创建/加入工作区**：访问或请求工作区成员资格（请参阅 `workspaces.md`）
2. **组织结构**：为实验室协议创建文件夹层次结构（请参阅 `file_manager.md`）
3. **创建协议**：使用 `POST /workspaces/{id}/protocols` 作为团队协议 
4. **上传文件**：添加实验数据和图片
5. **启用讨论**：团队成员可以发表评论并提供反馈
6. **跟踪实验**：使用实验记录记录协议执行

* *参考文件**：`workspaces.md`、`file_manager.md`、`protocols_api.md`、`discussions.md`、`additional_features.md`

### 工作流程4：实验文档

用于跟踪协议执行和结果：

1. **执行协议**：在实验室
2中执行协议。 **上传数据**：使用文件管理器API上传结果（参见`file_manager.md`）
3. **创建记录**：使用`POST /protocols/{id}/runs`
4进行文档执行。 **链接文件**：参考实验记录
5中上传的数据文件。 **注意修改**：记录任何协议偏差或优化
6. **分析**：审查多次运行以进行重现性评估

  * *参考文件**：`additional_features.md`、`file_manager.md`、`protocols_api.md`

### 工作流程5：协议发现和引用

在研究中查找和引用协议：

1. **搜索**：使用`GET /publications`
2查询已发布的协议。 **过滤器**：对相关协议使用类别和关键字过滤器
3. **评论**：阅读协议详细信息和社区评论
4. **书签**：使用`POST /protocols/{id}/bookmarks`
5保存有用的协议。 **引用**：在出版物中使用协议 DOI（正确归属）
6. **导出PDF**：生成格式化的PDF供离线参考

* *参考文件**：`protocols_api.md`、`additional_features.md`

## Python请求示例

### 基本协议搜索

```python
import requests

token = "YOUR_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

# Search for CRISPR protocols
response = requests.get(
    "https://protocols.io/api/v3/protocols",
    headers=headers,
    params={
        "filter": "public",
        "key": "CRISPR",
        "page_size": 10,
        "content_format": "html"
    }
)

protocols = response.json()
for protocol in protocols["items"]:
    print(f"{protocol['title']} - {protocol['doi']}")
```

### 创建新协议

```python
import requests

token = "YOUR_ACCESS_TOKEN"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Create protocol
data = {
    "title": "CRISPR-Cas9 Gene Editing Protocol",
    "description": "Comprehensive protocol for CRISPR gene editing",
    "tags": ["CRISPR", "gene editing", "molecular biology"]
}

response = requests.post(
    "https://protocols.io/api/v3/protocols",
    headers=headers,
    json=data
)

protocol_id = response.json()["item"]["id"]
print(f"Created protocol: {protocol_id}")
```

### 上传文件到工作空间

```python
import requests

token = "YOUR_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

# Upload file
with open("data.csv", "rb") as f:
    files = {"file": f}
    data = {
        "folder_id": "root",
        "description": "Experimental results",
        "tags": "experiment,data,2025"
    }

    response = requests.post(
        "https://protocols.io/api/v3/workspaces/12345/files/upload",
        headers=headers,
        files=files,
        data=data
    )

file_id = response.json()["item"]["id"]
print(f"Uploaded file: {file_id}")
```

## 错误处理

为API请求实现强大的错误处理：

```python
import requests
import time

def make_request_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit
                retry_after = int(response.headers.get('Retry-After', 60))
                time.sleep(retry_after)
                continue
            elif response.status_code >= 500:  # Server error
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)

    raise Exception("Max retries exceeded")
```

## 参考文件

根据您的任务加载适当的参考文件：

- **`authentication.md`**：OAuth 流程、令牌管理、速率限制
- **`protocols_api.md`**：协议 CRUD、步骤、材料、发布、PDF
- **`discussions.md`**：评论、回复、协作
- **`workspaces.md`**：团队工作空间、权限、组织
- **`file_manager.md`**：文件上传、文件夹、存储管理
- **`additional_features.md`**：个人资料、出版物、实验、通知

要加载参考文件，请从特定功能需要时的 `references/` 目录。

## 最佳实践

1. **身份验证**：安全地存储令牌，绝不在代码或版本控制中
2. **速率限制**：实施指数退避并遵守速率限制
3. **错误处理**：适当处理所有 HTTP 错误代码
4. **数据验证**：在 API 调用之前验证输入
5. **文档**：彻底记录协议步骤
6. **协作**：使用评论和讨论进行团队沟通
7. **组织**：保持一致的命名和标记约定
8. **版本控制**：进行更新时跟踪协议版本
9. **归属**：使用 DOIs
10 正确引用协议。 **备份**：定期导出重要协议和工作区数据

## 其他资源

- **官方API文档**：https://apidoc.protocols.io/
- **Protocols.io平台**：https://www.protocols.io/
- **支持**：联系protocols.io支持获取API访问和技术支持问题
- **社区**：与protocols.io社区合作以获得最佳实践

## 故障排除

* *身份验证问题：**
- 验证令牌是否有效且未过期
- 检查授权标头格式：`Bearer YOUR_TOKEN`
- 确保适当的令牌类型（客户端与OAUTH)

* *速率限制：**
- 对 429 个错误实施指数退避 
- 监控请求频率
- 考虑缓存频繁请求

* *权限错误：**
- 验证工作区/协议访问权限
- 检查用户角色工作区
- 确保未经许可访问时协议不是私有的

* *文件上传失败：**
- 根据工作区限制检查文件大小
- 验证文件类型是否受支持
- 确保多部分/表单数据编码正确

有关详细的故障排除指南，请参阅涵盖每个功能的特定参考文件面积.
