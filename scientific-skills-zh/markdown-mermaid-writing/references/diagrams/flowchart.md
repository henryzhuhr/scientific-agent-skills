<!-- 来源：https://github.com/SuperiorByteWorks-LLC/agent-project |许可证：Apache-2.0 |作者：Clayton Young / Superior Byte Works, LLC (Boreal Bytes) -->

# Flowchart

> **返回[样式指南](../mermaid_style_guide.md)** — 首先阅读样式指南以了解表情符号、颜色和可访问性规则。

* *语法关键字：** `flowchart`
* *最适合：**顺序流程、工作流程、决策逻辑、故障排除树
* *何时不使用：**参与者之间的复杂时序（使用[Sequence](sequence.md)）、状态机（使用[State](state.md)）

- --

## 示例图

```mermaid
flowchart TB
    accTitle: Feature Development Lifecycle
    accDescr: End-to-end feature flow from idea through design, build, test, review, and release with a revision loop on failed reviews

    idea([💡 Feature idea]) --> spec[📋 Write spec]
    spec --> design[🎨 Design solution]
    design --> build[🔧 Implement]
    build --> test[🧪 Run tests]
    test --> review{🔍 Review passed?}
    review -->|Yes| release[🚀 Release to prod]
    review -->|No| revise[✏️ Revise code]
    revise --> test
    release --> monitor([📊 Monitor metrics])

    classDef start fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#3b0764
    classDef process fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e3a5f
    classDef decision fill:#fef9c3,stroke:#ca8a04,stroke-width:2px,color:#713f12
    classDef success fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d

    class idea,monitor start
    class spec,design,build,test,revise process
    class review decision
    class release success
```

- --

## 提示

- 使用`TB`（从上到下）表示流程，`LR`（从左到右）表示管道
- 圆角矩形`([text])`表示开始/结束，菱形`{text}` 用于决策
- 最多 10 个节点 — 将较大的流拆分为“第 1 阶段”/“第 2 阶段”图表
- 每个图表最多 3 个决策点
- 边缘标签应为 1–4 个字：`-->|Yes|`、`-->|All green|`
- 使用`classDef` 用于 **语义** 着色 — 琥珀色为决策，绿色为成功，蓝色为行动

## 子图模式

当您需要分组阶段时：

```mermaid
flowchart TB
    accTitle: CI/CD Pipeline Stages
    accDescr: Three-stage pipeline grouping code quality checks, testing, and deployment into distinct phases

    trigger([⚡ Push to main])

    subgraph quality ["🔍 Code Quality"]
        lint[📝 Lint code] --> format[⚙️ Check formatting]
    end

    subgraph testing ["🧪 Testing"]
        unit[🧪 Unit tests] --> integration[🔗 Integration tests]
    end

    subgraph deploy ["🚀 Deployment"]
        build[📦 Build artifacts] --> ship[☁️ Deploy to staging]
    end

    trigger --> quality
    quality --> testing
    testing --> deploy
    deploy --> done([✅ Pipeline complete])

    classDef trigger_style fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#3b0764
    classDef success fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d

    class trigger trigger_style
    class done success
```

- --

## 模板

```mermaid
flowchart TB
    accTitle: Your Title Here (3-8 words)
    accDescr: One or two sentences explaining what this diagram shows and what insight the reader gains

    start([🏁 Starting point]) --> step1[⚙️ First action]
    step1 --> decision{🔍 Check condition?}
    decision -->|Yes| step2[✅ Positive path]
    decision -->|No| step3[🔧 Alternative path]
    step2 --> done([🏁 Complete])
    step3 --> done
```

- --

## 复杂示例

A 20+节点电子商务订单管道组织成5个子图，每个子图代表一个处理阶段。子图通过内部节点连接，决策点将订单路由到异常处理，颜色类一目了然地区分阶段。

```mermaid
flowchart TB
    accTitle: E-Commerce Order Processing Pipeline
    accDescr: Full order lifecycle from intake through fulfillment, shipping, and notification with exception handling paths for payment failures, stockouts, and delivery issues

    order_in([📥 New order]) --> validate_pay{💰 Payment valid?}

    subgraph intake ["📥 Order Intake"]
        validate_pay -->|Yes| check_fraud{🔐 Fraud check}
        validate_pay -->|No| pay_fail[❌ Payment **declined**]
        check_fraud -->|Clear| check_stock{📦 In stock?}
        check_fraud -->|Flagged| manual_review[🔍 Manual **review**]
        manual_review --> check_stock
    end

    subgraph fulfill ["📦 Fulfillment"]
        pick[📋 **Pick** items] --> pack[📦 Pack order]
        pack --> label[🏷️ Generate **shipping** label]
    end

    subgraph ship ["🚚 Shipping"]
        handoff[🚚 Carrier **handoff**] --> transit[📍 In transit]
        transit --> deliver{✅ Delivered?}
    end

    subgraph notify ["📤 Notifications"]
        confirm_email[📧 Order **confirmed**]
        ship_update[📧 Shipping **update**]
        deliver_email[📧 Delivery **confirmed**]
    end

    subgraph exception ["⚠️ Exception Handling"]
        pay_fail --> retry_pay[🔄 Retry payment]
        retry_pay --> validate_pay
        out_of_stock[📦 **Backorder** created]
        deliver_fail[🔄 **Reattempt** delivery]
    end

    check_stock -->|Yes| pick
    check_stock -->|No| out_of_stock
    label --> handoff
    deliver -->|Yes| deliver_email
    deliver -->|No| deliver_fail
    deliver_fail --> transit

    check_stock -->|Yes| confirm_email
    handoff --> ship_update
    deliver_email --> complete([✅ Order **complete**])

    classDef intake_style fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e3a5f
    classDef fulfill_style fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#3b0764
    classDef ship_style fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d
    classDef warn_style fill:#fef9c3,stroke:#ca8a04,stroke-width:2px,color:#713f12
    classDef danger_style fill:#fee2e2,stroke:#dc2626,stroke-width:2px,color:#7f1d1d

    class validate_pay,check_fraud,check_stock,manual_review intake_style
    class pick,pack,label fulfill_style
    class handoff,transit,deliver ship_style
    class confirm_email,ship_update,deliver_email warn_style
    class pay_fail,retry_pay,out_of_stock,deliver_fail danger_style
```

### 为什么会起作用

- **5 个子图映射到实际业务阶段** - 接收、履行、运输、通知和异常是运营团队实际考虑订单的方式
  - **异常处理是它自己的子图** - 不分散在各个阶段。代理和读者可以在一处看到所有故障路径
- **颜色类别强化结构** - 蓝色表示摄入，紫色表示履行，绿色表示运输，琥珀色表示通知，红色表示例外。即使不阅读标签，颜色模式也会告诉您正在查看哪个阶段
- **子图之间的决策路线** - 菱形（`{Payment valid?}`、`{In stock?}`、`{Delivered?}`）是流程分支的点，每个分支都通向一个明确标记的目的地
