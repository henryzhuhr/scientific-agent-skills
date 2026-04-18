# Open Notebook 架构

## 系统概述

Open Notebook 被构建为一个现代 Python Web 应用程序，前端和后端之间有明确的分离，使用 Docker 进行部署。

```
┌─────────────────────────────────────────────────────┐
│                   Docker Compose                    │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │   Next.js    │  │   FastAPI    │  │ SurrealDB │  │
│  │   Frontend   │──│   Backend    │──│           │  │
│  │  (port 8502) │  │  (port 5055) │  │ (port 8K) │  │
│  └──────────────┘  └──────────────┘  └───────────┘  │
│                          │                          │
│                    ┌─────┴─────┐                    │
│                    │ LangChain │                    │
│                    │ Esperanto │                    │
│                    └─────┬─────┘                    │
│                          │                          │
│              ┌───────────┼───────────┐              │
│              │           │           │              │
│          ┌───┴───┐   ┌───┴───┐   ┌───┴───┐          │
│          │OpenAI │   │Claude │   │Ollama │  ...     │
│          └───────┘   └───────┘   └───────┘          │
└─────────────────────────────────────────────────────┘
```

## 核心组件

### FastAPI 后端

REST API 使用 FastAPI 构建并组织成路由器：

- **20 个路由模块**，涵盖笔记本、源、笔记、聊天、搜索、播客、转换、模型、凭证、嵌入、设置等
- 异步/等待非阻塞 I/O
- 用于请求/响应验证的 Pydantic 模型
- 自定义异常处理程序将域错误映射到 HTTP 状态代码
- 用于跨源访问的 CORS 中间件
- 可选的密码身份验证中间件

### SurrealDB

SurrealDB 用作主数据存储，提供文档和关系功能：

- **用于笔记本、源、注释、转换和模型的文档存储**
- **笔记本源关联的关系参考**
- **跨索引内容的全文搜索**
- **RocksDB** 用于磁盘上持久存储的后端
- 架构迁移在应用程序启动时自动运行

### LangChain 集成

AI 功能由 LangChain 与世界语多提供商提供支持库：

- **LangGraph** 管理聊天会话的对话状态
- **嵌入模型** 跨内容的强大矢量搜索
- **LLM 链** 驱动转换、注释生成和播客脚本
- **提示模板** 存储在 `prompts/` 目录中

### 世界语多提供商库

E世界语为16个以上人工智能提供商提供统一接口：

- 摘要特定于提供程序的 API 差异
- 支持 LLM、嵌入、语音转文本和文本转语音功能
- 处理凭证管理和模型发现
- 无需更改代码即可实现运行时提供程序切换

### Next.js 前端

用户界面是使用以下代码构建的 React 应用程序Next.js:

- 桌面和平板电脑使用的响应式设计
- 聊天和处理状态的实时更新
- 带进度跟踪的文件上传
- 播客剧集的音频播放器

## 数据流

### 源摄取

```
Upload/URL → Source Record Created → Processing Queue
                                         │
                              ┌──────────┼──────────┐
                              ▼          ▼          ▼
                          Text       Embedding   Metadata
                        Extraction   Generation  Extraction
                              │          │          │
                              └──────────┼──────────┘
                                         ▼
                                  Source Updated
                                  (searchable)
```

### 聊天执行

```
User Message → Build Context (sources + notes)
                    │
                    ▼
              LangGraph State Machine
                    │
                    ├─ Retrieve relevant context
                    ├─ Format prompt with citations
                    └─ Stream LLM response
                         │
                         ▼
                   Response with
                   source citations
```

### 播客生成

```
Notebook Content → Episode Profile → Script Generation (LLM)
                                          │
                                          ▼
                                    Speaker Assignment
                                          │
                                          ▼
                                    Text-to-Speech
                                    (per segment)
                                          │
                                          ▼
                                    Audio Assembly
                                          │
                                          ▼
                                    Episode Record
                                    + Audio File
```

## 关键设计决策

1. **默认多提供商**：不锁定任何单一AI提供商，实现成本优化和能力匹配
2. **异步处理**：长时间运行的操作（源摄取、播客生成）与状态轮询
3 异步运行。 **自托管数据**：所有数据都保留在用户的基础设施上，并具有加密凭证存储
4. **REST-first API**：每个 UI 操作均由自动化 API 端点支持 
5. **Docker-native**：专为具有持久卷的容器化部署而设计

## 文件结构

```
open-notebook/
├── api/               # FastAPI REST API
│   ├── main.py        # App setup, middleware, routers
│   ├── routers/       # Route handlers (20 modules)
│   ├── models.py      # Pydantic request/response models
│   └── auth.py        # Authentication middleware
├── open_notebook/     # Core library
│   ├── ai/            # AI integration (LangChain, Esperanto)
│   ├── database/      # SurrealDB operations
│   ├── domain/        # Domain models and business logic
│   ├── graphs/        # LangGraph chat and processing graphs
│   ├── podcasts/      # Podcast generation pipeline
│   └── utils/         # Shared utilities
├── frontend/          # Next.js React application
├── prompts/           # AI prompt templates
├── tests/             # Test suite
└── docker-compose.yml # Deployment configuration
```
