# CORE API

CORE 聚合了来自全球 15,000 多个存储库的开放获取研究。它为超过 3700 万篇文章提供**全文**，为超过 36800 万篇论文提供元数据。

## 基本 URL

```
https://api.core.ac.uk/v3
```

* *重要：** GET 搜索路径需要 **尾部斜杠**（例如，`/v3/search/works/` 不是 `/v3/search/works`）。

## Authentication

- **标头：** `Authorization: Bearer YOUR_API_KEY`
- **查询参数：** `?api_key=YOUR_API_KEY`
- 注册地址：https://core.ac.uk/services/api

* *没有身份验证：** 基本元数据查询有效，但全文不可用（返回“不适用于公共 API”）用户”）。

## 速率限制（基于代币）

|用户类型 |每日代币 |每分钟最大|
|---------|-------------|----------------|
|未经验证 | 100/天 | 10次​​/分钟|
|注册个人| 1,000/天 | 25/分钟|
|注册学术| 5,000/天 | 10/分钟 |

 简单查询需要 1 个代币。下载和滚动分页需要 3-5 个代币。

## 关键端点

### 1. 搜索作品

```
GET /v3/search/works/?q={query}&limit={n}&offset={n}
```

|参数|默认|描述 |
|---------|---------|------------|
| `q` |必填|搜索查询（支持字段查找、布尔运算符）|
| `limit` | 10 | 10每页结果（最多 100 条）|
| `offset` | 0 |分页偏移|
| `scroll` |假 |为 >10,000 个结果启用滚动分页 |
| `sort` |相关性 | `relevance` 或 `recency` |

* *POST 替代**（对于复杂查询）：
```
POST /v3/search/works
Content-Type: application/json

{"q": "machine learning", "limit": 10, "offset": 0}
```

* *示例：**
```
https://api.core.ac.uk/v3/search/works/?q=CRISPR+gene+therapy&limit=10
```

### 2. 查询语言

|操作员|示例|描述 |
|----------|---------|------------|
|和| `title:"AI" AND authors:"Smith"` |两种情况|
|或 | `title:"AI" OR fullText:"Deep Learning"` |任一条件|
|分组| `(title:"AI" OR title:"ML") AND yearPublished>"2020"` |优先级|
|现场查找| `title:"Machine Learning"` |搜索特定领域 |
|范围 | `yearPublished>2018` |数值比较|
|存在 | `_exists_:fullText` |字段必须存在|
|短语 | `title:"Attention is all you need"` |精确短语 |

* *可搜索字段：** `abstract`、`arxivId`、`authors`、`contributors`、`createdDate`、`dataProviders`、`depositedDate`、`documentType`、`doi`、 `fullText`、`id`、`language`、`license`、`oai`、`title`、`yearPublished`

### 3. 通过以下方式获取工作ID

```
GET /v3/works/{id}
```

`id` 是核心工作 ID（整数）。示例：`/v3/works/267312`

### 4. 通过 ID

```
GET /v3/outputs/{id}
```

### 获取输出 5. 下载全文

```
GET /v3/outputs/{id}/download
```

 返回二进制 PDF。需要身份验证。

```
GET /v3/works/tei/{id}
```

返回 TEI XML 格式。

### 6. 搜索输出

```
GET /v3/search/outputs/?q={query}&limit={n}&offset={n}
```

按 DOI 搜索：`q=doi:10.1038/nature12373`

## 响应格式

### 搜索响应
```json
{
  "totalHits": 2281337,
  "limit": 10,
  "offset": 0,
  "scrollId": null,
  "results": [...]
}
```

### 工作对象（关键字段）
```json
{
  "id": 8848131,
  "title": "Attention Is All You Need",
  "authors": [{"name": "Ashish Vaswani"}, ...],
  "abstract": "The dominant sequence...",
  "doi": "10.48550/arXiv.1706.03762",
  "arxivId": "1706.03762",
  "yearPublished": 2017,
  "downloadUrl": "https://core.ac.uk/download/...",
  "fullText": "Full text content (when authenticated)...",
  "language": {"code": "en", "name": "English"},
  "documentType": "research",
  "citationCount": 145678,
  "dataProviders": [{"name": "arXiv"}],
  "links": [{"type": "download", "url": "..."}]
}
```

## 分页

- **标准：** `offset` + `limit` （最多 10,000 个结果）
- **滚动：** 设置 `scroll=true`。响应包括 `scrollId`。在后续请求分页超过 10,000 时使用（花费更多令牌）。

## 错误处理

在重负载下，API 可能会返回部分分片失败消息。这些都是暂时的——短暂等待后重试。
