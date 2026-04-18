---
name: open-notebook
description: Google NotebookLM 的自托管开源替代方案，用于人工智能驱动的研究和文档分析。在将研究材料组织到笔记本中、摄取不同的内容源（PDF、视频、音频、网页、Office 文档）、生成 AI 驱动的笔记和摘要、根据研究创建多扬声器播客、使用上下文感知 AI 与文档聊天、使用全文和矢量搜索跨材料搜索或运行自定义内容转换时使用。支持超过 16 个人工智能提供商，包括 OpenAI、Anthropic、Google、Ollama、Groq 和 Mistral，通过自托管提供完整的数据隐私。
license: MIT
metadata:
    skill-author: K-Dense Inc.
---

# Open Notebook

## 概述

Open Notebook 是 Google NotebookLM 的开源、自托管替代品，使研究人员能够组织材料、生成人工智能驱动的见解、创建播客以及与其文档进行上下文感知对话，同时保持完整的数据隐私。

 与 Google 的 Notebook LM 不同，后者在企业之外没有公开可用的 API版本中，Open Notebook 提供了全面的 REST API，支持 16 个以上的 AI 提供程序，并完全在您自己的基础设施上运行。

* * 相对于 NotebookLM 的主要优势：**
  - 用于编程访问和自动化的完整 REST API
  - 可选择 16 个以上的 AI 提供程序（未锁定到 Google 模型）
  - 具有 1-4 个可自定义扬声器的多扬声器播客生成（与 1 个可自定义扬声器相比） 2人限制）
- 通过自托管完成数据主权
- 开源且完全可扩展（MIT许可证）

* *存储库：** https://github.com/lfnovo/open-notebook

## 快速入门

### 先决条件

- Docker桌面安装
- 至少一个AI提供商的API密钥（或用于免费本地推理的本地Ollama）

### 安装

使用Docker Compose部署打开笔记本：

```bash
# Download the docker-compose file
curl -o docker-compose.yml https://raw.githubusercontent.com/lfnovo/open-notebook/main/docker-compose.yml

# Set the required encryption key
export OPEN_NOTEBOOK_ENCRYPTION_KEY="your-secret-key-here"

# Launch the services
docker-compose up -d
```

访问应用程序：
- **前端UI：** http://localhost:8502
- **REST API:** http://localhost:5055
- **API 文档：** http://localhost:5055/docs

### 配置 AI Provider

启动后，配置至少一个 AI Provider：

1. 导航到 UI
2 中的 **设置 > API 密钥**。添加您的首选提供商（OpenAI、Anthropic 等）
3 的凭据。测试连接并发现可用型号
4. 注册模型以供跨平台使用

或通过REST API进行配置：

```python
import requests

BASE_URL = "http://localhost:5055/api"

# Add a credential for an AI provider
response = requests.post(f"{BASE_URL}/credentials", json={
    "provider": "openai",
    "name": "My OpenAI Key",
    "api_key": "sk-..."
})
credential = response.json()

# Discover available models
response = requests.post(
    f"{BASE_URL}/credentials/{credential['id']}/discover"
)
discovered = response.json()

# Register discovered models
requests.post(
    f"{BASE_URL}/credentials/{credential['id']}/register-models",
    json={"model_ids": [m["id"] for m in discovered["models"]]}
)
```

## 核心功能

### 笔记本
将研究组织到单独的笔记本中，每个笔记本包含源、注释和聊天会话。

```python
import requests

BASE_URL = "http://localhost:5055/api"

# Create a notebook
response = requests.post(f"{BASE_URL}/notebooks", json={
    "name": "Cancer Genomics Research",
    "description": "Literature review on tumor mutational burden"
})
notebook = response.json()
notebook_id = notebook["id"]
```

### 来源
摄取多种内容类型，包括 PDF、视频、音频文件、网页和 Office 文档。处理源以进行全文和矢量搜索。

```python
# Add a web URL source
response = requests.post(f"{BASE_URL}/sources", data={
    "url": "https://arxiv.org/abs/2301.00001",
    "notebook_id": notebook_id,
    "process_async": "true"
})
source = response.json()

# Upload a PDF file
with open("paper.pdf", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/sources",
        data={"notebook_id": notebook_id},
        files={"file": ("paper.pdf", f, "application/pdf")}
    )
```

### 注释
创建和管理与笔记本相关的注释（人工或人工智能生成）。

```python
# Create a human note
response = requests.post(f"{BASE_URL}/notes", json={
    "title": "Key Findings",
    "content": "TMB correlates with immunotherapy response in NSCLC...",
    "note_type": "human",
    "notebook_id": notebook_id
})
```

### 上下文感知聊天
使用引用的人工智能与您的研究材料聊天来源。

```python
# Create a chat session
session = requests.post(f"{BASE_URL}/chat/sessions", json={
    "notebook_id": notebook_id,
    "title": "TMB Discussion"
}).json()

# Send a message with context from sources
response = requests.post(f"{BASE_URL}/chat/execute", json={
    "session_id": session["id"],
    "message": "What are the key biomarkers for immunotherapy response?",
    "context": {"include_sources": True, "include_notes": True}
})
```

### 搜索
使用全文或矢量（语义）搜索在所有材料中搜索。

```python
# Vector search across the knowledge base
results = requests.post(f"{BASE_URL}/search", json={
    "query": "tumor mutational burden immunotherapy",
    "search_type": "vector",
    "limit": 10
}).json()

# Ask a question with AI-powered answer
answer = requests.post(f"{BASE_URL}/search/ask/simple", json={
    "query": "How does TMB predict checkpoint inhibitor response?"
}).json()
```

### 播客生成
从研究材料中生成专业的多扬声器播客，具有 1-4 个功能可定制的扬声器。

```python
# Generate a podcast episode
job = requests.post(f"{BASE_URL}/podcasts/generate", json={
    "notebook_id": notebook_id,
    "episode_profile_id": episode_profile_id,
    "speaker_profile_ids": [speaker1_id, speaker2_id]
}).json()

# Check generation status
status = requests.get(f"{BASE_URL}/podcasts/jobs/{job['job_id']}").json()

# Download audio when ready
audio = requests.get(
    f"{BASE_URL}/podcasts/episodes/{status['episode_id']}/audio"
)
```

### 内容转换
对内容应用自定义 AI 驱动的转换，以进行摘要、提取和分析。

```python
# Create a custom transformation
transform = requests.post(f"{BASE_URL}/transformations", json={
    "name": "extract_methods",
    "title": "Extract Methods",
    "description": "Extract methodology details from papers",
    "prompt": "Extract and summarize the methodology section...",
    "apply_default": False
}).json()

# Execute transformation on text
result = requests.post(f"{BASE_URL}/transformations/execute", json={
    "transformation_id": transform["id"],
    "input_text": "...",
    "model_id": "model_id_here"
}).json()
```

## 支持的 AI 提供商

Open Notebook 支持超过 16 个 AI 提供商通过世界语库：

|供应商|法学硕士 |嵌入 |语音转文本 |文字转语音 |
|---------|-----|------------|----------------|----------------|
|开放人工智能 |是的 |是的 |是的 |是 |
|人择 |是的 |没有 |没有 |否|
|谷歌GenAI |是的 |是的 |没有 |是 |
|顶点人工智能 |是的 |是的 |没有 |是 |
|奥拉玛 |是的 |是的 |没有 |否|
|格罗克 |是的 |没有 |是的 |否|
|米斯特拉尔|是的 |是的 |没有 |否|
| Azure 开放人工智能 |是的 |是的 |没有 |否|
|深度搜索|是的 |没有 |没有 |否|
| xAI |是的 |没有 |没有 |否|
|开放路由器 |是的 |没有 |没有 |否|
|十一实验室 |没有 |没有 |是的 |是 |
|困惑|是的 |没有 |没有 |否|
|航程|没有 |是的 |没有 |否 |

## 环境变量

Docker部署的关键配置变量：

|变量|描述 |默认|
|----------|-------------|---------|
| `OPEN_NOTEBOOK_ENCRYPTION_KEY` | **必需。** 用于加密存储的凭据的密钥 |无 |
| `SURREAL_URL` | SurrealDB 连接 URL | `ws://surrealdb:8000/rpc` |
| `SURREAL_NAMESPACE` |数据库命名空间| `open_notebook` |
| `SURREAL_DATABASE` |数据库名称| `open_notebook` |
| `OPEN_NOTEBOOK_PASSWORD` | UI 的可选密码保护 |无 |

## API 参考

REST API 在 `http://localhost:5055/api` 上提供，交互式文档位于 `/docs`。

 核心端点组：
- `/api/notebooks` - 笔记本 CRUD 和源关联
- `/api/sources` - 源摄取，处理和检索
- `/api/notes` - 笔记管理
- `/api/chat/sessions` - 聊天会话管理
- `/api/chat/execute` - 聊天消息执行
- `/api/search` - 全文和矢量搜索
- `/api/podcasts` - 播客生成和管理
- `/api/transformations` - 内容转换管道
- `/api/models` - AI 模型配置和发现
- `/api/credentials` - 提供商凭证管理

有关所有端点和请求/响应的完整 API 参考格式，请参见 `references/api_reference.md`.

## 架构

Open Notebook 使用现代堆栈：
- **后端：** 带 FastAPI 的 Python 
- **数据库：** SurrealDB（文档 + 关系型）
- **AI 集成：** LangChain 与世界语多提供商库
- **前端：** Next.js 与 React
- **部署：** Docker Compose 与持久卷

## 重要说明

- Open Notebook 需要 Docker 进行部署
- 必须至少配置一个 AI 提供程序才能使 AI 功能正常工作
- 如需无需 API 成本的免费本地推理，请使用Ollama
  - `OPEN_NOTEBOOK_ENCRYPTION_KEY` 必须在首次启动之前设置，并在重新启动后保持一致
  - 所有数据都本地存储在 Docker 卷中，以实现完整的数据主权