# Protocols API

## 概述

Protocols API 是protocols.io 的核心功能，支持从创建到发布的完整协议生命周期。这包括搜索、创建、更新、管理步骤、处理材料、添加书签和生成 PDF。

## 基本 URL

所有协议端点都使用基本 URL：`https://protocols.io/api/v3`

## 内容格式参数

许多端点支持 `content_format` 参数来指定如何返回内容：

- `json`：Draft.js JSON 格式（默认）
- `html`：HTML 格式
- `markdown`：Markdown 格式

包含此作为查询参数：`?content_format=html`

## 列表和搜索操作

### 列表协议

通过过滤和分页检索协议。

* *端点：** `GET /protocols`

* *查询参数：**
- `filter`：过滤器类型
  - `public`：仅限公共协议
  - `private`：您的私有协议
  - `shared`：与您共享的协议
  - `user_public`：其他用户的公共协议
- `key`：协议标题、描述和内容中的搜索关键字
- `order_field`：排序字段（`activity`、`created_on`、`modified_on`、`name`、`id`）
- `order_dir`：排序方向（`desc`、`asc`）
- `page_size`：每页结果数（默认：10，最大：50）
- `page_id`：分页页码（从 0 开始）
- `fields`：要返回的以逗号分隔的字段列表
- `content_format`：内容格式(`json`, `html`, `markdown`)

* *请求示例：**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://protocols.io/api/v3/protocols?filter=public&key=CRISPR&page_size=20&content_format=html"
```

### 按 DOI

搜索协议通过 DOI 检索协议。

* *端点：** `GET /protocols/{doi}`

* *路径参数：**
- `doi`：协议 DOI（例如 `dx.doi.org/10.17504/protocols.io.xxxxx`）

## 检索协议详细信息

### 通过 ID

获取协议**端点：** `GET /protocols/{protocol_id}`

* *路径参数：**
- `protocol_id`：协议唯一标识符

  * *查询参数：**
- `content_format`：内容格式（`json`、`html`、`markdown`）

* *响应包括：**
- 协议元数据（标题、作者、描述、DOI）
- 所有协议步骤及内容
- 材料和试剂
- 指南和警告
- 版本信息
- 出版状态

## 创建和更新协议

### 创建新协议协议

* *端点：** `POST /protocols`

* *请求体参数：**
- `title`（必填）：协议标题
- `description`：协议描述
- `tags`：标签数组字符串
- `vendor_name`：供应商/公司名称
- `vendor_link`：供应商网站URL
- `warning`：警告或安全消息
- `guidelines`：使用指南
- `manuscript_citation`：相关手稿的引用
- `link`：相关资源的外部链接

* *示例请求：**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "CRISPR Gene Editing Protocol",
    "description": "Comprehensive protocol for CRISPR-Cas9 mediated gene editing",
    "tags": ["CRISPR", "gene editing", "molecular biology"]
  }' \
  "https://protocols.io/api/v3/protocols"
```

### 更新协议

* *端点：** `PATCH /protocols/{protocol_id}`

* *路径参数：**
- `protocol_id`：协议的唯一标识符

* *请求体**：与创建相同的参数，均为可选

## 协议步骤管理

### 创建协议步骤

* *端点：** `POST /protocols/{protocol_id}/steps`

* *请求正文参数：**
- `title`（必填）：步骤标题
- `description`：步骤描述（HTML、Markdown 或 Draft.js JSON）
- `duration`：步骤持续时间秒
- `temperature`：温度设置
- `components`：使用的材料/试剂阵列
- `software`：所需的软件或工具
- `commands`：执行的命令
- `expected_result`：预期结果描述

* *示例请求：**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Prepare sgRNA",
    "description": "Design and synthesize single guide RNA (sgRNA) targeting your gene of interest",
    "duration": 3600,
    "temperature": 25
  }' \
  "https://protocols.io/api/v3/protocols/12345/steps"
```

### 更新协议步骤

* *端点：** `PATCH /protocols/{protocol_id}/steps/{step_id}`

* *参数**：与创建步骤相同，全部可选

### 删除协议步骤

* *端点：** `DELETE /protocols/{protocol_id}/steps/{step_id}`

### 重新排序步骤

* *端点：** `POST /protocols/{protocol_id}/steps/reorder`

* *请求正文：**
- `step_order`：按所需顺序排列的步骤 ID 数组

## 材料和试剂

### 获取协议材料

检索某个实验中使用的所有材料和试剂协议.

* *端点：** `GET /protocols/{protocol_id}/materials`

* *响应包括：**
- 试剂名称和描述
- 目录号
- 供应商信息
- 浓度和数量
- 产品链接页面

## 发布和DOI

### 发布协议

发布DOI并使协议公开可用。

* *端点：**`POST /protocols/{protocol_id}/publish`

* *请求正文参数：**
- `version_notes`：此中的更改说明版本
- `publish_type`：发布类型
  - `new`：首次发布
  - `update`：更新现有已发布协议

* *重要说明：**
- 一旦发布，协议将获得永久DOI
- 无法删除已发布的协议，只能使用新版本进行更新
- 已发布的协议可公开访问

* *示例请求：**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "version_notes": "Initial publication",
    "publish_type": "new"
  }' \
  "https://protocols.io/api/v3/protocols/12345/publish"
```

## 书签

### 添加书签

将协议添加到您的用于快速访问的书签。

* *端点：** `POST /protocols/{protocol_id}/bookmarks`

### 删除书签

* *端点：** `DELETE /protocols/{protocol_id}/bookmarks`

### 列出书签协议

* *端点：** `GET /bookmarks`

## PDF Export

### 生成协议 PDF

生成协议的格式化 PDF 版本。

* *端点：** `GET /view/{protocol_uri}.pdf`

* *查询参数：**
- `compact`：设置为 `1` 以获得无大间距的紧凑视图

* *速率限制：**
- 登录用户：每分钟 5 个请求
- 未签名用户：每分钟 3 个请求分钟

* *示例：**
```
https://protocols.io/api/v3/view/crispr-protocol-abc123.pdf?compact=1
```

## 常见用例

### 1. 导入现有协议

导入并使用现有协议：

1. 使用关键字或DOI
2搜索协议。使用 `/protocols/{protocol_id}`
3 检索完整的协议详细信息。提取步骤、材料和元数据供本地使用

### 2. 从头开始​​创建新协议

创建新协议：

1. 创建带有标题和描述的协议：`POST /protocols`
2. 依次添加步骤：`POST /protocols/{id}/steps`
3. 查看并测试协议
4. 准备好后发布：`POST /protocols/{id}/publish`

### 3.更新已发布的协议

更新已发布的协议：

1. 检索当前版本：`GET /protocols/{protocol_id}`
2. 进行必要的更新：`PATCH /protocols/{protocol_id}`
3. 根据需要更新或添加步骤
4. 发布新版本：`POST /protocols/{protocol_id}/publish` 和 `publish_type: "update"`

### 4.克隆和修改协议

创建现有协议的修改版本：

1. 检索原始协议详细信息
2. 使用修改后的元数据创建新协议
3. 复制并修改原始
4的步骤。发布为新协议

## 错误处理

常见错误响应：

- `400 Bad Request`：参数或请求格式无效
- `401 Unauthorized`：访问令牌缺失或无效
- `403 Forbidden`：权限不足操作
- `404 Not Found`：未找到协议或资源
- `429 Too Many Requests`：超出速率限制
- `500 Internal Server Error`：服务器端错误

为`429`和`500`实现具有指数退避的重试逻辑错误.
