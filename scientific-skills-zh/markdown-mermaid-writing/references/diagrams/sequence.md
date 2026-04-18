<!-- 来源：https://github.com/SuperiorByteWorks-LLC/agent-project |许可证：Apache-2.0 |作者：Clayton Young / Superior Byte Works, LLC (Boreal Bytes) -->

# 序列图

> **返回[样式指南](../mermaid_style_guide.md)** — 首先阅读样式指南以了解表情符号、颜色和可访问性规则。

* *语法关键字：** `sequenceDiagram`
* *最适合：** API 交互、时间流、多参与者通信、请求/响应模式
* *何时不使用：** 简单线性过程（使用 [Flowchart](flowchart.md)）、静态关系（使用 [Class](class.md)或 [ER](er.md)）

- --

## 示例图

```mermaid
sequenceDiagram
    accTitle: OAuth 2.0 Authorization Code Flow
    accDescr: Step-by-step OAuth flow between user browser, app server, and identity provider showing the token exchange and error path

    participant U as 👤 User Browser
    participant A as 🖥️ App Server
    participant I as 🔐 Identity Provider

    U->>A: Click Sign in
    A-->>U: Redirect to IdP

    U->>I: Enter credentials
    I->>I: 🔍 Validate credentials

    alt ✅ Valid credentials
        I-->>U: Redirect with auth code
        U->>A: Send auth code
        A->>I: Exchange code for token
        I-->>A: 🔐 Access + refresh token
        A-->>U: ✅ Set session cookie
        Note over U,A: 🔒 User is now authenticated
    else ❌ Invalid credentials
        I-->>U: ⚠️ Show error message
    end
```

- --

## 提示

- 限制为 **4–5 名参与者** — 更多则变得不可读
- 实线箭头 (`->>`)表示请求，虚线 (`-->>`)表示响应
- 使用`alt/else/end` 用于条件分支
- 使用 `Note over X,Y:` 进行带有表情符号的上下文注释
- 使用 `par/end` 进行并行操作
- 使用 `loop/end` 进行重复交互
- **消息文本**中的表情符号非常有助于状态清晰（✅， ❌, ⚠️, 🔐)

## 常见模式

* *并行调用：**

```
par 📥 Fetch user
    A->>B: GET /user
and 📥 Fetch orders
    A->>C: GET /orders
end
```

* *循环：**

```
loop ⏰ Every 30 seconds
    A->>B: Health check
    B-->>A: ✅ 200 OK
end
```

- --

## 模板

```mermaid
sequenceDiagram
    accTitle: Your Title Here
    accDescr: Describe the interaction between participants and what the sequence demonstrates

    participant A as 👤 Actor
    participant B as 🖥️ System
    participant C as 💾 Database

    A->>B: 📤 Request action
    B->>C: 🔍 Query data
    C-->>B: 📥 Return results
    B-->>A: ✅ Deliver response
```

- --

## 复杂示例

A 微服务结账流程，有 6 个参与者分组在 `box` 区域。显示并行调用、条件分支、`break` 的错误处理、重试逻辑和上下文注释 - 用于复杂序列的完整工具包。

```mermaid
sequenceDiagram
    accTitle: Microservices Checkout Flow
    accDescr: Multi-service checkout sequence showing parallel inventory and payment processing, error recovery with retries, and async notification dispatch across client, gateway, and backend service layers

    box rgb(237,233,254) 🌐 Client Layer
        participant browser as 👤 Browser
    end

    box rgb(219,234,254) 🖥️ API Layer
        participant gw as 🌐 API Gateway
        participant order as 📋 Order Service
    end

    box rgb(220,252,231) ⚙️ Backend Services
        participant inventory as 📦 Inventory
        participant payment as 💰 Payment
        participant notify as 📤 Notifications
    end

    browser->>gw: 🛒 Submit checkout
    gw->>gw: 🔐 Validate JWT token
    gw->>order: 📋 Create order

    Note over order: 📊 Order status: PENDING

    par ⚡ Parallel validation
        order->>inventory: 📦 Reserve items
        inventory-->>order: ✅ Items reserved
    and
        order->>payment: 💰 Authorize card
        payment-->>order: ✅ Payment authorized
    end

    alt ✅ Both succeeded
        order->>payment: 💰 Capture payment
        payment-->>order: ✅ Payment captured
        order->>inventory: 📦 Confirm reservation

        Note over order: 📊 Order status: CONFIRMED

        par 📤 Async notifications
            order->>notify: 📧 Send confirmation email
        and
            order->>notify: 📱 Send push notification
        end

        order-->>gw: ✅ Order confirmed
        gw-->>browser: ✅ Show confirmation page

    else ❌ Inventory unavailable
        order->>payment: 🔄 Void authorization
        order-->>gw: ⚠️ Items out of stock
        gw-->>browser: ⚠️ Show stock error

    else ❌ Payment declined
        order->>inventory: 🔄 Release reservation

        loop 🔄 Retry up to 2 times
            order->>payment: 💰 Retry authorization
            payment-->>order: ❌ Still declined
        end

        order-->>gw: ❌ Payment failed
        gw-->>browser: ❌ Show payment error
    end
```

### 为什么有效

- **`box` 分组** 按架构层对参与者进行集群 - 读者可以立即看到哪些服务是面向客户的，哪些服务是后端的 
- **`par` 块** 显示同时发生的并行库存 + 付款检查，这就是真正的结帐系统如何提高性能
- **嵌套的 `alt`/`else`** 涵盖了幸福的道路和两个不同的失败模式，每种模式都有适当的清理（无效身份验证，释放保留）
- **`loop` 用于重试逻辑** 显示付款重试模式，而不会扰乱快乐路径
- **消息中的表情符号**使扫描速度更快 - 📦用于库存，💰用于付款，✅/❌用于结果
