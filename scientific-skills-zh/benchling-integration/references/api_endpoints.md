# Benchling REST API 端点参考

## 基本 URL

所有 API 请求都使用基本 URL 格式：
```
https://{tenant}.benchling.com/api/v2
```

 将 `{tenant}` 替换为您的 Benchling 租户名称。

## API 版本控制

当前 API 版本： `v2` (2025-10-07)

URL路径中指定API版本。 Benchling 在主要版本内保持向后兼容性。

## 身份验证

所有请求都需要通过 HTTP 标头进行身份验证：

* *API 密钥（基本身份验证）：**
```bash
curl -X GET \
  https://your-tenant.benchling.com/api/v2/dna-sequences \
  -u "your_api_key:"
```

* *OAuth 承载Token:**
```bash
curl -X GET \
  https://your-tenant.benchling.com/api/v2/dna-sequences \
  -H "Authorization: Bearer your_access_token"
```

## Common Headers

```
Authorization: Bearer {token}
Content-Type: application/json
Accept: application/json
```

## 响应格式

所有响应都遵循一致的 JSON 结构：

* *Single资源：**
```json
{
  "id": "seq_abc123",
  "name": "My Sequence",
  "bases": "ATCGATCG",
  ...
}
```

* *列表响应：**
```json
{
  "results": [
    {"id": "seq_1", "name": "Sequence 1"},
    {"id": "seq_2", "name": "Sequence 2"}
  ],
  "nextToken": "token_for_next_page"
}
```

## 分页

列表端点支持分页：

* *查询参数：**
- `pageSize`：每页的项目数（默认：50，最大：100）
- `nextToken`：下一页的上一个响应的令牌

* *示例：**
```bash
curl -X GET \
  "https://your-tenant.benchling.com/api/v2/dna-sequences?pageSize=50&nextToken=abc123"
```

## 错误响应

* *格式：**
```json
{
  "error": {
    "type": "NotFoundError",
    "message": "DNA sequence not found",
    "userMessage": "The requested sequence does not exist or you don't have access"
  }
}
```

* *常见状态代码：**
- `200 OK`：成功
- `201 Created`：已创建资源
- `400 Bad Request`：参数无效
- `401 Unauthorized`：凭据丢失或无效
- `403 Forbidden`：权限不足
- `404 Not Found`：资源没有存在
- `422 Unprocessable Entity`：验证错误
- `429 Too Many Requests`：超出速率限制
- `500 Internal Server Error`：服务器错误

## 核心端点

### DNA序列

* *列出DNA序列：**
```http
GET /api/v2/dna-sequences

Query Parameters:
- pageSize: integer (default: 50, max: 100)
- nextToken: string
- folderId: string
- schemaId: string
- name: string (filter by name)
- modifiedAt: string (ISO 8601 date)
```

* *获取 DNA 序列：**
```http
GET /api/v2/dna-sequences/{sequenceId}
```

* *创建 DNA 序列：**
```http
POST /api/v2/dna-sequences

Body:
{
  "name": "My Plasmid",
  "bases": "ATCGATCG",
  "isCircular": true,
  "folderId": "fld_abc123",
  "schemaId": "ts_abc123",
  "fields": {
    "gene_name": {"value": "GFP"},
    "resistance": {"value": "Kanamycin"}
  },
  "entityRegistryId": "src_abc123",  // optional for registration
  "namingStrategy": "NEW_IDS"        // optional for registration
}
```

* *更新 DNA序列：**
```http
PATCH /api/v2/dna-sequences/{sequenceId}

Body:
{
  "name": "Updated Plasmid",
  "fields": {
    "gene_name": {"value": "mCherry"}
  }
}
```

* *存档 DNA 序列：**
```http
POST /api/v2/dna-sequences:archive

Body:
{
  "dnaSequenceIds": ["seq_abc123"],
  "reason": "Deprecated construct"
}
```

### RNA 序列

* *列出 RNA序列：**
```http
GET /api/v2/rna-sequences
```

* *获取RNA序列：**
```http
GET /api/v2/rna-sequences/{sequenceId}
```

* *创建RNA序列：**
```http
POST /api/v2/rna-sequences

Body:
{
  "name": "gRNA-001",
  "bases": "AUCGAUCG",
  "folderId": "fld_abc123",
  "fields": {
    "target_gene": {"value": "TP53"}
  }
}
```

* *更新RNA序列：**
```http
PATCH /api/v2/rna-sequences/{sequenceId}
```

* *存档 RNA 序列：**
```http
POST /api/v2/rna-sequences:archive
```

### 氨基酸（蛋白质）序列

* *列出 AA 序列：**
```http
GET /api/v2/aa-sequences
```

* *获取 AA 序列：**
```http
GET /api/v2/aa-sequences/{sequenceId}
```

* *创建 AA 序列：**
```http
POST /api/v2/aa-sequences

Body:
{
  "name": "GFP Protein",
  "aminoAcids": "MSKGEELFTGVVPILVELDGDVNGHKF",
  "folderId": "fld_abc123"
}
```

### 自定义实体

* *列出自定义实体：**
```http
GET /api/v2/custom-entities

Query Parameters:
- schemaId: string (required to filter by type)
- pageSize: integer
- nextToken: string
```

* *获取自定义实体：**
```http
GET /api/v2/custom-entities/{entityId}
```

* *创建自定义实体：**
```http
POST /api/v2/custom-entities

Body:
{
  "name": "HEK293T-Clone5",
  "schemaId": "ts_cellline_abc",
  "folderId": "fld_abc123",
  "fields": {
    "passage_number": {"value": "15"},
    "mycoplasma_test": {"value": "Negative"}
  }
}
```

* *更新自定义实体：**
```http
PATCH /api/v2/custom-entities/{entityId}

Body:
{
  "fields": {
    "passage_number": {"value": "16"}
  }
}
```

### 混合物

* *列出混合物：**
```http
GET /api/v2/mixtures
```

* *创建混合物：**
```http
POST /api/v2/mixtures

Body:
{
  "name": "LB-Amp Media",
  "folderId": "fld_abc123",
  "schemaId": "ts_mixture_abc",
  "ingredients": [
    {
      "componentEntityId": "ent_lb_base",
      "amount": {"value": "1000", "units": "mL"}
    },
    {
      "componentEntityId": "ent_ampicillin",
      "amount": {"value": "100", "units": "mg"}
    }
  ]
}
```

### 容器

* *列出容器：**
```http
GET /api/v2/containers

Query Parameters:
- parentStorageId: string (filter by location/box)
- schemaId: string
- barcode: string
```

* *获取容器：**
```http
GET /api/v2/containers/{containerId}
```

* *创建容器：**
```http
POST /api/v2/containers

Body:
{
  "name": "Sample-001",
  "schemaId": "cont_schema_abc",
  "barcode": "CONT001",
  "parentStorageId": "box_abc123",
  "fields": {
    "concentration": {"value": "100 ng/μL"},
    "volume": {"value": "50 μL"}
  }
}
```

* *更新集装箱：**
```http
PATCH /api/v2/containers/{containerId}

Body:
{
  "fields": {
    "volume": {"value": "45 μL"}
  }
}
```

* *中转集装箱：**
```http
POST /api/v2/containers:transfer

Body:
{
  "containerIds": ["cont_abc123"],
  "destinationStorageId": "box_xyz789"
}
```

* *签出集装箱：**
```http
POST /api/v2/containers:checkout

Body:
{
  "containerIds": ["cont_abc123"],
  "comment": "Taking to bench"
}
```

* *签入容器：**
```http
POST /api/v2/containers:checkin

Body:
{
  "containerIds": ["cont_abc123"],
  "locationId": "bench_loc_abc"
}
```

### 框

* *列表框：**
```http
GET /api/v2/boxes

Query Parameters:
- parentStorageId: string
- schemaId: string
```

* *获取框：**
```http
GET /api/v2/boxes/{boxId}
```

* *创建框：**
```http
POST /api/v2/boxes

Body:
{
  "name": "Freezer-A-Box-01",
  "schemaId": "box_schema_abc",
  "parentStorageId": "loc_freezer_a",
  "barcode": "BOX001"
}
```

### 位置

* *列出位置：**
```http
GET /api/v2/locations
```

* *获取位置：**
```http
GET /api/v2/locations/{locationId}
```

* *创建位置：**
```http
POST /api/v2/locations

Body:
{
  "name": "Freezer A - Shelf 2",
  "parentStorageId": "loc_freezer_a",
  "barcode": "LOC-A-S2"
}
```

### 板

* *列表板：**
```http
GET /api/v2/plates
```

* *获取板：**
```http
GET /api/v2/plates/{plateId}
```

* *创建板：**
```http
POST /api/v2/plates

Body:
{
  "name": "PCR-Plate-001",
  "schemaId": "plate_schema_abc",
  "barcode": "PLATE001",
  "wells": [
    {"position": "A1", "entityId": "ent_abc"},
    {"position": "A2", "entityId": "ent_xyz"}
  ]
}
```

### 条目（笔记本）

* *列表条目：**
```http
GET /api/v2/entries

Query Parameters:
- folderId: string
- schemaId: string
- modifiedAt: string
```

* *获取条目：**
```http
GET /api/v2/entries/{entryId}
```

* *创建条目：**
```http
POST /api/v2/entries

Body:
{
  "name": "Experiment 2025-10-20",
  "folderId": "fld_abc123",
  "schemaId": "entry_schema_abc",
  "fields": {
    "objective": {"value": "Test gene expression"},
    "date": {"value": "2025-10-20"}
  }
}
```

* *更新条目：**
```http
PATCH /api/v2/entries/{entryId}

Body:
{
  "fields": {
    "results": {"value": "Successful expression"}
  }
}
```

### 工作流任务

* *列出工作流任务：**
```http
GET /api/v2/tasks

Query Parameters:
- workflowId: string
- statusIds: string[] (comma-separated)
- assigneeId: string
```

* *获取任务：**
```http
GET /api/v2/tasks/{taskId}
```

* *创建任务：**
```http
POST /api/v2/tasks

Body:
{
  "name": "PCR Amplification",
  "workflowId": "wf_abc123",
  "assigneeId": "user_abc123",
  "schemaId": "task_schema_abc",
  "fields": {
    "template": {"value": "seq_abc123"},
    "priority": {"value": "High"}
  }
}
```

* *更新任务：**
```http
PATCH /api/v2/tasks/{taskId}

Body:
{
  "statusId": "status_complete_abc",
  "fields": {
    "completion_date": {"value": "2025-10-20"}
  }
}
```

### 文件夹

* *列出文件夹：**
```http
GET /api/v2/folders

Query Parameters:
- projectId: string
- parentFolderId: string
```

* *获取文件夹：**
```http
GET /api/v2/folders/{folderId}
```

* *创建文件夹：**
```http
POST /api/v2/folders

Body:
{
  "name": "2025 Experiments",
  "parentFolderId": "fld_parent_abc",
  "projectId": "proj_abc123"
}
```

### 项目

* *列出项目：**
```http
GET /api/v2/projects
```

* *获取项目：**
```http
GET /api/v2/projects/{projectId}
```

### 用户

* *获取当前用户：**
```http
GET /api/v2/users/me
```

* *列出用户：**
```http
GET /api/v2/users
```

* *获取用户：**
```http
GET /api/v2/users/{userId}
```

### 团队

* *列出团队：**
```http
GET /api/v2/teams
```

* *获取团队：**
```http
GET /api/v2/teams/{teamId}
```

### 架构

* *列出架构：**
```http
GET /api/v2/schemas

Query Parameters:
- entityType: string (e.g., "dna_sequence", "custom_entity")
```

* *获取架构：**
```http
GET /api/v2/schemas/{schemaId}
```

### 注册表

* *列出注册表：**
```http
GET /api/v2/registries
```

* *获取注册表：**
```http
GET /api/v2/registries/{registryId}
```

## 批量操作

### 批量存档

* *存档多个实体：**
```http
POST /api/v2/{entity-type}:archive

Body:
{
  "{entity}Ids": ["id1", "id2", "id3"],
  "reason": "Cleanup"
}
```

### 批量传输

* *传输多个容器：**
```http
POST /api/v2/containers:bulk-transfer

Body:
{
  "transfers": [
    {"containerId": "cont_1", "destinationId": "box_a"},
    {"containerId": "cont_2", "destinationId": "box_b"}
  ]
}
```

## 异步操作

一些操作返回异步的任务ID处理：

* *响应：**
```json
{
  "taskId": "task_abc123"
}
```

* *检查任务状态：**
```http
GET /api/v2/tasks/{taskId}

Response:
{
  "id": "task_abc123",
  "status": "RUNNING", // or "SUCCEEDED", "FAILED"
  "message": "Processing...",
  "response": {...}  // Available when status is SUCCEEDED
}
```

## 字段值格式

自定义架构字段使用特定格式：

* *简单值：**
```json
{
  "field_name": {
    "value": "Field Value"
  }
}
```

* *下拉菜单：**
```json
{
  "dropdown_field": {
    "value": "Option1"  // Must match exact option name
  }
}
```

* *日期：**
```json
{
  "date_field": {
    "value": "2025-10-20"  // Format: YYYY-MM-DD
  }
}
```

* *实体链接：**
```json
{
  "entity_link_field": {
    "value": "seq_abc123"  // Entity ID
  }
}
```

* *数字：**
```json
{
  "numeric_field": {
    "value": "123.45"  // String representation
  }
}
```

## 速率限制

* *限制：**
- 默认：每 10 秒 100 个请求user/app
- 响应中包含的速率限制标头：
  - `X-RateLimit-Limit`：允许的请求总数
  - `X-RateLimit-Remaining`：剩余请求
  - `X-RateLimit-Reset`：限制重置时的Unix时间戳

  * *处理429响应：**
```json
{
  "error": {
    "type": "RateLimitError",
    "message": "Rate limit exceeded",
    "retryAfter": 5  // Seconds to wait
  }
}
```

## 过滤和搜索

* *常用查询参数：**
- `name`：部分名称匹配
- `modifiedAt`：ISO 8601 datetime
- `createdAt`：ISO 8601 datetime
- `schemaId`：过滤器按模式
- `folderId`：按文件夹过滤
- `archived`：布尔值（包括存档项目）

* *示例：**
```bash
curl -X GET \
  "https://tenant.benchling.com/api/v2/dna-sequences?name=plasmid&folderId=fld_abc&archived=false"
```

## 最佳实践

### 请求效率

1. **使用适当的页面大小：**
  - 默认：50 个项目
  - 最大：100 个项目
  - 根据需要调整

2. **服务器端过滤：**
  - 使用查询参数而不是客户端过滤
  - 减少数据传输和处理

3. **批量操作：**
  - 可用时使用批量端点
  - 在一个请求中存档/传输多个项目

### 错误处理

```javascript
// Example error handling
async function fetchSequence(id) {
  try {
    const response = await fetch(
      `https://tenant.benchling.com/api/v2/dna-sequences/${id}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/json'
        }
      }
    );

    if (!response.ok) {
      if (response.status === 429) {
        // Rate limit - retry with backoff
        const retryAfter = response.headers.get('Retry-After');
        await sleep(retryAfter * 1000);
        return fetchSequence(id);
      } else if (response.status === 404) {
        return null;  // Not found
      } else {
        throw new Error(`API error: ${response.status}`);
      }
    }

    return await response.json();
  } catch (error) {
    console.error('Request failed:', error);
    throw error;
  }
}
```

### 分页循环

```javascript
async function getAllSequences() {
  let allSequences = [];
  let nextToken = null;

  do {
    const url = new URL('https://tenant.benchling.com/api/v2/dna-sequences');
    if (nextToken) {
      url.searchParams.set('nextToken', nextToken);
    }
    url.searchParams.set('pageSize', '100');

    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json'
      }
    });

    const data = await response.json();
    allSequences = allSequences.concat(data.results);
    nextToken = data.nextToken;
  } while (nextToken);

  return allSequences;
}
```

## 参考文献

- **API 文档：** https://benchling.com/api/reference
- **交互式 API Explorer：** https://your-tenant.benchling.com/api/reference（需要身份验证）
- **更改日志：** https://docs.benchling.com/changelog
