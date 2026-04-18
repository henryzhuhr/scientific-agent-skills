# 打开笔记本 API 参考

## 基本 URL

```
http://localhost:5055/api
```

 交互式 API 文档可在 `http://localhost:5055/docs` (Swagger UI)和 `http://localhost:5055/redoc` (ReDoc)中找到。

## 身份验证

如果配置了 `OPEN_NOTEBOOK_PASSWORD`，请在请求中包含密码。以下路由不参与认证：`/`、`/health`、`/docs`、`/openapi.json`、`/redoc`、`/api/auth/status`、`/api/config`.

- --

## 笔记本

### 列表笔记本

```
GET /api/notebooks
```

* *查询参数：**
|参数|类型 |描述|
|---------|------|----------|
| `archived` |布尔 |按存档状态过滤|
| `order_by` |字符串|排序字段（默认：`updated_at`）|

* *响应：**带有`source_count`和`note_count`.

的笔记本对象数组###创建笔记本

```
POST /api/notebooks
```

* *请求正文：**
```json
{
  "name": "My Research",
  "description": "Optional description"
}
```

### 获取笔记本

```
GET /api/notebooks/{notebook_id}
```

### 更新笔记本

```
PUT /api/notebooks/{notebook_id}
```

* *请求正文：**
```json
{
  "name": "Updated Name",
  "description": "Updated description",
  "archived": false
}
```

### 删除笔记本

```
DELETE /api/notebooks/{notebook_id}
```

* *查询参数：**
|参数|类型 |描述|
|---------|------|----------|
| `delete_sources` |布尔 |同时删除独占源（默认值： false） |

### 删除预览

```
GET /api/notebooks/{notebook_id}/delete-preview
```

返回受删除影响的注释和源的计数。

### 将源链接到笔记本

```
POST /api/notebooks/{notebook_id}/sources/{source_id}
```

 关联源的幂等操作

### 从笔记本中取消链接源

```
DELETE /api/notebooks/{notebook_id}/sources/{source_id}
```

- --

## 源

### 列出源

```
GET /api/sources
```

* *查询参数：**
|参数|类型 |描述|
|---------|------|----------|
| `notebook_id` |字符串|按笔记本筛选 |
| `limit` |整数 |结果数 |
| `offset` |整数 |分页偏移|
| `order_by` |字符串|排序字段 |

### 创建源

```
POST /api/sources
```

接受文件上传的多部分表单数据或URL/文本源的JSON。

* *表单参数：**
|参数|类型 |描述 |
|-----------|------|-------------|
| `file` |文件|上传文件（PDF、DOCX、音频、视频）|
| `url` |字符串|要摄取的网址 |
| `text` |字符串|原始文本内容|
| `notebook_id` |字符串|关联笔记本|
| `process_async` |布尔 |异步处理（默认值：true） |

### 创建源 (JSON)

```
POST /api/sources/json
```

 用于源创建的基于 JSON 的旧端点。

### 获取源

```
GET /api/sources/{source_id}
```

### 获取源Status

```
GET /api/sources/{source_id}/status
```

轮询异步摄取源的处理状态。

### 更新源

```
PUT /api/sources/{source_id}
```

* *请求正文：**
```json
{
  "title": "Updated Title",
  "topic": "Updated topic"
}
```

### 删除源

```
DELETE /api/sources/{source_id}
```

### 下载源文件

```
GET /api/sources/{source_id}/download
```

返回原来上传的文件。

### 检查源文件

```
HEAD /api/sources/{source_id}/download
```

### 重试失败的源

```
POST /api/sources/{source_id}/retry
```

重新排队处理失败的源。

### 获取源见解

```
GET /api/sources/{source_id}/insights
```

检索 AI 生成的源见解。

- --

## 注释

### 列表注释

```
GET /api/notes
```

* *查询参数：**
|参数|类型 |描述|
|---------|------|----------|
| `notebook_id` |字符串|按笔记本过滤|

### 创建注释

```
POST /api/notes
```

* *请求正文：**
```json
{
  "title": "My Note",
  "content": "Note content...",
  "note_type": "human",
  "notebook_id": "notebook:abc123"
}
```

`note_type`必须是`"human"`或`"ai"`。没有标题的AI笔记会自动生成标题。

### 获取笔记

```
GET /api/notes/{note_id}
```

### 更新笔记

```
PUT /api/notes/{note_id}
```

* *请求正文：**
```json
{
  "title": "Updated Title",
  "content": "Updated content",
  "note_type": "human"
}
```

### 删除备注

```
DELETE /api/notes/{note_id}
```

- --

## 聊天

### 列表会话

```
GET /api/chat/sessions
```

* *查询参数：**
|参数|类型 |描述|
|---------|------|----------|
| `notebook_id` |字符串|按笔记本过滤 |

### 创建会话

```
POST /api/chat/sessions
```

* *请求正文：**
```json
{
  "notebook_id": "notebook:abc123",
  "title": "Discussion Topic",
  "model_override": "optional_model_id"
}
```

### 获取会话

```
GET /api/chat/sessions/{session_id}
```

返回带有消息历史记录的会话详细信息。

### 更新会话

```
PUT /api/chat/sessions/{session_id}
```

### 删除会话

```
DELETE /api/chat/sessions/{session_id}
```

### 执行聊天

```
POST /api/chat/execute
```

* *请求正文：**
```json
{
  "session_id": "chat_session:abc123",
  "message": "Your question here",
  "context": {
    "include_sources": true,
    "include_notes": true
  },
  "model_override": "optional_model_id"
}
```

### 构建上下文

```
POST /api/chat/context
```

从聊天会话的源和注释构建上下文数据。

- --

## 搜索

### 搜索知识Base

```
POST /api/search
```

* *请求正文：**
```json
{
  "query": "search terms",
  "search_type": "vector",
  "limit": 10,
  "source_ids": [],
  "note_ids": [],
  "min_similarity": 0.7
}
```

`search_type`可以是`"vector"`（需要嵌入模型）或`"text"`（关键字

### 使用流式询问

```
POST /api/search/ask
```

返回服务器发送的事件，并根据知识库内容由人工智能生成答案。

### 询问简单

```
POST /api/search/ask/simple
```

返回完整的非流式版本response.

- --

## Podcasts

### 生成 Podcast

```
POST /api/podcasts/generate
```

* *请求正文：**
```json
{
  "notebook_id": "notebook:abc123",
  "episode_profile_id": "episode_profile:xyz",
  "speaker_profile_ids": ["speaker:a", "speaker:b"]
}
```

 返回用于跟踪的 `job_id` 

### 获取作业状态

```
GET /api/podcasts/jobs/{job_id}
```

### 列出剧集

```
GET /api/podcasts/episodes
```

### 获取剧集

```
GET /api/podcasts/episodes/{episode_id}
```

### 获取剧集Audio

```
GET /api/podcasts/episodes/{episode_id}/audio
```

流式传输播客音频文件。

### 重试失败的剧集

```
POST /api/podcasts/episodes/{episode_id}/retry
```

### 删除Episode

```
DELETE /api/podcasts/episodes/{episode_id}
```

- --

## 转换

### 列表转换

```
GET /api/transformations
```

### 创建转换

```
POST /api/transformations
```

* *请求正文：**
```json
{
  "name": "summarize",
  "title": "Summarize Content",
  "description": "Generate a concise summary",
  "prompt": "Summarize the following text...",
  "apply_default": false
}
```

### 执行转换

```
POST /api/transformations/execute
```

* *请求正文：**
```json
{
  "transformation_id": "transformation:abc",
  "input_text": "Text to transform...",
  "model_id": "model:xyz"
}
```

### 获取默认提示

```
GET /api/transformations/default-prompt
```

### 更新默认提示

```
PUT /api/transformations/default-prompt
```

### 获取变换

```
GET /api/transformations/{transformation_id}
```

### 更新变换

```
PUT /api/transformations/{transformation_id}
```

### 删除变换

```
DELETE /api/transformations/{transformation_id}
```

- --

## 型号

### 列出型号

```
GET /api/models
```

* *查询参数：**
|参数|类型 |描述|
|---------|------|----------|
| `model_type` |字符串|按类型过滤（llm、嵌入、stt、tts） |

### 创建模型

```
POST /api/models
```

### 删除模型

```
DELETE /api/models/{model_id}
```

### 测试模型

```
POST /api/models/{model_id}/test
```

### 获取默认模型

```
GET /api/models/defaults
```

返回默认模型分配七个服务槽：聊天、转换、嵌入、语音转文本、文本转语音、播客和摘要。

### 更新默认模型

```
PUT /api/models/defaults
```

### 获取提供程序

```
GET /api/models/providers
```

### 发现模型

```
GET /api/models/discover/{provider}
```

### 同步模型（单一提供商）

```
POST /api/models/sync/{provider}
```

### 同步所有模型

```
POST /api/models/sync
```

### 自动分配默认值

```
POST /api/models/auto-assign
```

使用提供商优先级排名自动填充空的默认模型槽位。

### 获取模型计数

```
GET /api/models/count/{provider}
```

### 获取模型提供商

```
GET /api/models/by-provider/{provider}
```

- --

## 凭证

### 获取状态

```
GET /api/credentials/status
```

### 获取环境状态

```
GET /api/credentials/env-status
```

### 列出凭证

```
GET /api/credentials
```

* *查询参数：**
|参数|类型 |描述|
|---------|------|----------|
| `provider` |字符串|按提供商过滤 |

### 按提供商列出

```
GET /api/credentials/by-provider/{provider}
```

### 创建凭证

```
POST /api/credentials
```

* *请求正文：**
```json
{
  "provider": "openai",
  "name": "My OpenAI Key",
  "api_key": "sk-...",
  "base_url": null
}
```

### 获取凭证

```
GET /api/credentials/{credential_id}
```

注意：API密钥值永远不会返回。

### 更新凭证

```
PUT /api/credentials/{credential_id}
```

### 删除Credential

```
DELETE /api/credentials/{credential_id}
```

### 测试 Credential

```
POST /api/credentials/{credential_id}/test
```

### 通过 Credential 发现模型

```
POST /api/credentials/{credential_id}/discover
```

### 通过以下方式注册模型凭证

```
POST /api/credentials/{credential_id}/register-models
```

- --

## 错误响应

API 返回带有 JSON 错误主体的标准 HTTP 状态代码：

|状态 |含义 |
|--------|---------|
| 400 |输入无效 |
| 401 | 401需要身份验证|
| 404 | 404找不到资源|
| 422 | 422配置错误|
| 429 | 429限价|
| 500 | 500内部服务器错误|
| 502 | 502外部服务错误|

* *错误响应格式：**
```json
{
  "detail": "Description of the error"
}
```
