<!-- 来源：https://github.com/SuperiorByteWorks-LLC/agent-project |许可证：Apache-2.0 |作者：Clayton Young / Superior Byte Works, LLC (Boreal Bytes) -->

# 组合复杂图表集

> **返回[风格指南](../mermaid_style_guide.md)** — 该文件介绍了如何组合多种图表类型来全面记录复杂系统。

* *目的：** 单个图表捕获单个视角。真实的文档通常需要多种图表类型一起工作——链接到详细序列图的概述流程图、与显示实体生命周期的状态机配对的 ER 模式、由架构前/后视图补充的甘特时间线。该文件教您何时以及如何构建最清晰的图表。

- --

## 何时构建多个图表

|您正在记录的内容 |图解组合|为什么它有效 |
| ------------------------ | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
|完整的系统架构| C4 上下文 + 架构 + 顺序（关键流程） |利益相关者的上下文、操作的基础设施、开发人员的序列 |
| API设计文档| ER（数据模型）+序列（请求流）+状态（实体生命周期）|数据库团队的架构、后端的交互、业务逻辑的状态 |
|功能规格|流程图（快乐路径）+序列（服务交互）+用户旅程（UX）| PM的流程、工程师的实施、设计的经验|
|移民项目|甘特图（时间线）+架构（之前/之后）+流程图（迁移过程）|领导安排、基础设施拓扑、迁移团队步骤 |
|入职文档 |用户旅程 + 流程图（设置步骤）+ 顺序（第一次 API 调用）|产品体验地图、新员工清单、开发人员技术演练 |
|事件响应 |状态（警报生命周期）+序列（升级流程）+流程图（决策树）|待命状态跟踪、管理沟通、响应者分类 |

- --

## 模式 1：概述 + 详细信息

* *何时使用：** 您需要大局和细节。领导看全局；工程师深入细节。

概览图显示了高级阶段或组件。一个或多个详细图放大显示内部交互的特定阶段。

### 概述 — 发布管道

```mermaid
flowchart LR
    accTitle: Release Pipeline Overview
    accDescr: High-level four-phase release pipeline from code commit through build, staging, and production deployment

    subgraph source ["📥 Source"]
        commit[📝 Code commit] --> pr_review[🔍 PR review]
    end

    subgraph build ["🔧 Build"]
        compile[⚙️ Compile] --> test[🧪 Test suite]
        test --> scan[🔐 Security scan]
    end

    subgraph staging ["🚀 Staging"]
        deploy_stg[☁️ Deploy staging] --> smoke[🧪 Smoke tests]
        smoke --> approval{👤 Approved?}
    end

    subgraph production ["✅ Production"]
        canary[🚀 Canary **5%**] --> rollout[🚀 Full **rollout**]
        rollout --> monitor[📊 Monitor metrics]
    end

    source --> build
    build --> staging
    approval -->|Yes| production
    approval -->|No| source

    classDef phase_start fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e3a5f
    classDef phase_test fill:#fef9c3,stroke:#ca8a04,stroke-width:2px,color:#713f12
    classDef phase_deploy fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d

    class commit,pr_review,compile phase_start
    class test,scan,smoke,approval phase_test
    class deploy_stg,canary,rollout,monitor phase_deploy
```

_生产部署阶段涉及多个服务交互。请参阅下面的金丝雀推出过程的详细序列。_

### 详细信息 — 金丝雀部署序列

```mermaid
sequenceDiagram
    accTitle: Canary Deployment Service Interactions
    accDescr: Detailed sequence showing how the CI server orchestrates a canary deployment through the container registry, Kubernetes cluster, and monitoring stack with automated rollback on failure

    participant ci as ⚙️ CI Server
    participant registry as 📦 Container Registry
    participant k8s as ☁️ Kubernetes
    participant monitor as 📊 Monitoring
    participant oncall as 👤 On-Call Engineer

    ci->>registry: 📤 Push tagged image
    registry-->>ci: ✅ Image stored

    ci->>k8s: 🚀 Deploy canary (5% traffic)
    k8s-->>ci: ✅ Canary pods running

    ci->>monitor: 📊 Start canary analysis
    Note over monitor: ⏰ Observe for 15 minutes

    loop 📊 Every 60 seconds
        monitor->>k8s: 🔍 Query error rate
        k8s-->>monitor: 📊 Metrics response
    end

    alt ✅ Error rate below threshold
        monitor-->>ci: ✅ Canary healthy
        ci->>k8s: 🚀 Promote to 100%
        k8s-->>ci: ✅ Full rollout complete
        ci->>monitor: 📊 Continue monitoring
    else ❌ Error rate above threshold
        monitor-->>ci: ❌ Canary failing
        ci->>k8s: 🔄 Rollback to previous
        k8s-->>ci: ✅ Rollback complete
        ci->>oncall: ⚠️ Alert: canary failed
        Note over oncall: 📋 Investigate root cause
    end
```

### 这些如何连接

- **概述流程图**显示了具有子图到子图连接的完整管道 — 领导层阅读此内容以了解发布过程
- **详细序列**从生产子图中放大到“Canary 5% → Full rollout”，显示工程师将调试的实际服务交互
- **命名一致** - “Canary”和“Monitor Metrics”出现在两个图中，在概述和细节之间建立了清晰的桥梁

- --

## 模式2：多视角文档

* *何时使用：**相同的系统需求为不同的受众（数据库团队、后端工程师和产品经理）记录同一功能。

此示例从三个角度记录了 **用户身份验证** 功能。

### 数据模型 — 用于数据库团队

```mermaid
erDiagram
    accTitle: Authentication Data Model
    accDescr: Five-entity schema for user authentication covering users, sessions, refresh tokens, login attempts, and MFA devices with cardinality relationships

    USER ||--o{ SESSION : "has"
    USER ||--o{ REFRESH_TOKEN : "owns"
    USER ||--o{ LOGIN_ATTEMPT : "produces"
    USER ||--o{ MFA_DEVICE : "registers"
    SESSION ||--|| REFRESH_TOKEN : "paired with"

    USER {
        uuid id PK "🔑 Primary key"
        string email "📧 Unique login"
        string password_hash "🔐 Bcrypt hash"
        boolean mfa_enabled "🔒 MFA flag"
        timestamp last_login "⏰ Last active"
    }

    SESSION {
        uuid id PK "🔑 Primary key"
        uuid user_id FK "👤 Session owner"
        string ip_address "🌐 Client IP"
        string user_agent "📋 Browser info"
        timestamp expires_at "⏰ Expiration"
    }

    REFRESH_TOKEN {
        uuid id PK "🔑 Primary key"
        uuid user_id FK "👤 Token owner"
        uuid session_id FK "🔗 Paired session"
        string token_hash "🔐 Hashed token"
        boolean revoked "❌ Revoked flag"
        timestamp expires_at "⏰ Expiration"
    }

    LOGIN_ATTEMPT {
        uuid id PK "🔑 Primary key"
        uuid user_id FK "👤 Attempting user"
        string ip_address "🌐 Source IP"
        boolean success "✅ Outcome"
        string failure_reason "⚠️ Why failed"
        timestamp attempted_at "⏰ Attempt time"
    }

    MFA_DEVICE {
        uuid id PK "🔑 Primary key"
        uuid user_id FK "👤 Device owner"
        string device_type "📱 TOTP or WebAuthn"
        string secret_hash "🔐 Encrypted secret"
        boolean verified "✅ Setup complete"
        timestamp registered_at "⏰ Registered"
    }
```

### 身份验证流程 — 用于后端team

```mermaid
sequenceDiagram
    accTitle: Login Flow with MFA
    accDescr: Step-by-step authentication sequence showing credential validation, conditional MFA challenge, token issuance, and failure handling between browser, API, auth service, and database

    participant B as 👤 Browser
    participant API as 🌐 API Gateway
    participant Auth as 🔐 Auth Service
    participant DB as 💾 Database

    B->>API: 📤 POST /login (email, password)
    API->>Auth: 🔐 Validate credentials
    Auth->>DB: 🔍 Fetch user by email
    DB-->>Auth: 👤 User record

    Auth->>Auth: 🔐 Verify password hash

    alt ❌ Invalid password
        Auth->>DB: 📝 Log failed attempt
        Auth-->>API: ❌ 401 Unauthorized
        API-->>B: ❌ Invalid credentials
    else ✅ Password valid
        alt 🔒 MFA enabled
            Auth-->>API: ⚠️ 202 MFA required
            API-->>B: 📱 Show MFA prompt

            B->>API: 📤 POST /login/mfa (code)
            API->>Auth: 🔐 Verify MFA code
            Auth->>DB: 🔍 Fetch MFA device
            DB-->>Auth: 📱 Device record
            Auth->>Auth: 🔐 Validate TOTP

            alt ❌ Invalid code
                Auth-->>API: ❌ 401 Invalid code
                API-->>B: ❌ Try again
            else ✅ Code valid
                Auth->>DB: 📝 Create session + tokens
                Auth-->>API: ✅ 200 + tokens
                API-->>B: ✅ Set cookies + redirect
            end
        else 🔓 No MFA
            Auth->>DB: 📝 Create session + tokens
            Auth-->>API: ✅ 200 + tokens
            API-->>B: ✅ Set cookies + redirect
        end
    end
```

### 登录体验 — 针对产品团队

```mermaid
journey
    accTitle: Login Experience Journey Map
    accDescr: User satisfaction scores across the sign-in experience for password-only users and MFA users showing friction points in the multi-factor flow

    title 👤 Login Experience
    section 🔐 Sign In
        Navigate to login          : 4 : User
        Enter email and password   : 3 : User
        Click sign in button       : 4 : User
    section 📱 MFA Challenge
        Receive MFA prompt         : 3 : MFA User
        Open authenticator app     : 2 : MFA User
        Enter 6-digit code         : 2 : MFA User
        Handle expired code        : 1 : MFA User
    section ✅ Post-Login
        Land on dashboard          : 5 : User
        See personalized content   : 5 : User
        Resume previous session    : 4 : User
```

### 这些如何连接

- **相同的实体，不同的视图** — “用户”、“会话”、“MFA 设备”作为表格出现在 ER 图中，按照参与者/操作的顺序，在旅程中作为体验接触点
- **每个受众都获得可操作的信息** — 数据库团队看到索引和基数，后端团队看到 API 合同和错误代码，产品团队看到满意度分数和摩擦点
- **旅程揭示了序列隐藏**——序列图显示 MFA 作为一个干净的条件分支，但旅程图显示它实际上是 UX 中最糟糕的部分（得分 1-2）。这促使产品决定投资 WebAuthn/passkeys

- --

## 模式 3：架构之前/之后

* *何时使用：** 利益相关者需要查看当前状态、目标状态并了解转换的迁移文档。

### 当前状态 — Monolith

```mermaid
flowchart TB
    accTitle: Current State Monolith Architecture
    accDescr: Single Rails monolith handling all traffic through one server connected to one database showing the scaling bottleneck

    client([👤 All traffic]) --> mono[🖥️ Rails **Monolith**]
    mono --> db[(💾 Single PostgreSQL)]
    mono --> jobs[⏰ Background **jobs**]
    jobs --> db

    classDef bottleneck fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#7f1d1d
    classDef neutral fill:#f3f4f6,stroke:#6b7280,stroke-width:2px,color:#1f2937

    class mono,db bottleneck
    class client,jobs neutral
```

> ⚠️ **问题：** 单一数据库是瓶颈。单体应用无法水平扩展。部署 = 完全重新启动。

### 目标状态 — 微服务

```mermaid
flowchart TB
    accTitle: Target State Microservices Architecture
    accDescr: Decomposed microservices architecture with API gateway routing to independent services each with their own data store and a shared message queue for async communication

    client([👤 All traffic]) --> gw[🌐 API **Gateway**]

    subgraph services ["⚙️ Services"]
        user_svc[👤 User Service]
        order_svc[📋 Order Service]
        product_svc[📦 Product Service]
    end

    subgraph data ["💾 Data Stores"]
        user_db[(💾 Users DB)]
        order_db[(💾 Orders DB)]
        product_db[(💾 Products DB)]
    end

    gw --> user_svc
    gw --> order_svc
    gw --> product_svc

    user_svc --> user_db
    order_svc --> order_db
    product_svc --> product_db

    order_svc --> mq[📥 Message Queue]
    mq --> user_svc
    mq --> product_svc

    classDef gateway fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#3b0764
    classDef service fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e3a5f
    classDef datastore fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d
    classDef infra fill:#fef9c3,stroke:#ca8a04,stroke-width:2px,color:#713f12

    class gw gateway
    class user_svc,order_svc,product_svc service
    class user_db,order_db,product_db datastore
    class mq infra
```

> ✅ **结果：** 每个服务独立扩展。每个服务数据库消除了共享瓶颈。异步消息传递解耦服务依赖关系。

### 这些如何连接

- **相同​​的布局，不同的复杂性** - 两个图都使用 `flowchart TB`，因此结构转换在视觉上是显而易见的。整体架构有 4 个节点；目标是带有子图的 11 个节点。
- **颜色讲述故事** — 整体在瓶颈组件上使用红色（危险）。目标使用蓝色/绿色/紫色来显示健康、差异化的组件。
- **Prose 连接图表** — ⚠️ 问题标注和 ✅ 结果标注解释_为什么_架构发生变化，而不仅仅是_发生变化。

- --

## 文档中的链接图

在真实文档中编写图表时，请遵循以下做法：

|实践|示例|
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **使用标题作为锚点** | `See [Authentication Flow](#authentication-flow-for-backend-team) for the full login sequence` |
| **参考特定节点** | “概述中的 **API 网关** 连接到下面详细介绍的服务” |
| **一致的命名** |相同的实体 = 每个图中的名称相同（用户服务，不是一个图中的“用户 Svc”，另一个图中的“用户 API”）|
| **相邻放置** |将相关图表保留在连续的部分中，不要分散在文档中 |
| **桥接散文** |图表之间的一句话解释了它们如何连接：“下面的序列从上面的管道放大到部署阶段”|
| **受众标签** |标记部分：“### 数据模型 — _数据库团队_”，以便读者跳到他们的视图 |

- --

## 选择您的组合策略

```mermaid
flowchart TB
    accTitle: Diagram Composition Decision Tree
    accDescr: Decision flowchart for choosing between single diagram, overview plus detail, multi-perspective, or before-after composition strategies based on audience and documentation needs

    start([📋 What are you documenting?]) --> audience{👥 Multiple audiences?}

    audience -->|Yes| perspectives[📐 Multi-Perspective]
    audience -->|No| depth{📏 Need both summary and detail?}

    depth -->|Yes| overview[🔍 Overview + Detail]
    depth -->|No| change{🔄 Showing a change over time?}

    change -->|Yes| before_after[⚡ Before / After]
    change -->|No| single[📊 Single diagram is fine]

    classDef decision fill:#fef9c3,stroke:#ca8a04,stroke-width:2px,color:#713f12
    classDef result fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e3a5f
    classDef start_style fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#3b0764

    class audience,depth,change decision
    class perspectives,overview,before_after,single result
    class start start_style
```
