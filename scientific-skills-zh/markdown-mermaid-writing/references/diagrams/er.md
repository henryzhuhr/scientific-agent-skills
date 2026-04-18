<!-- 来源：https://github.com/SuperiorByteWorks-LLC/agent-project |许可证：Apache-2.0 |作者：Clayton Young / Superior Byte Works, LLC (Boreal Bytes) -->

# 实体关系 (ER)图

> **返回[样式指南](../mermaid_style_guide.md)** — 首先阅读样式指南以了解表情符号、颜色和可访问性规则。

* *语法关键字：** `erDiagram`
* *最适合：**数据库模式、数据模型、实体关系、API 数据结构
* *何时不使用：**带有方法的类层次结构（使用 [Class](class.md)）、流程（使用 [Flowchart](flowchart.md)）

- --

## 示例图

```mermaid
erDiagram
    accTitle: Project Management Data Model
    accDescr: Entity relationships for a project management system showing teams, projects, tasks, members, and comments with cardinality

    TEAM ||--o{ PROJECT : "owns"
    PROJECT ||--o{ TASK : "contains"
    TASK ||--o{ COMMENT : "has"
    TEAM ||--o{ MEMBER : "includes"
    MEMBER ||--o{ TASK : "assigned to"
    MEMBER ||--o{ COMMENT : "writes"

    TEAM {
        uuid id PK "🔑 Primary key"
        string name "👥 Team name"
        string department "🏢 Department"
    }

    PROJECT {
        uuid id PK "🔑 Primary key"
        uuid team_id FK "🔗 Team reference"
        string title "📋 Project title"
        string status "📊 Current status"
        date deadline "⏰ Due date"
    }

    TASK {
        uuid id PK "🔑 Primary key"
        uuid project_id FK "🔗 Project reference"
        uuid assignee_id FK "👤 Assigned member"
        string title "📝 Task title"
        string priority "⚠️ Priority level"
        string status "📊 Current status"
    }

    MEMBER {
        uuid id PK "🔑 Primary key"
        uuid team_id FK "🔗 Team reference"
        string name "👤 Full name"
        string email "📧 Email address"
        string role "🏷️ Job role"
    }

    COMMENT {
        uuid id PK "🔑 Primary key"
        uuid task_id FK "🔗 Task reference"
        uuid author_id FK "👤 Author reference"
        text body "📝 Comment text"
        timestamp created_at "⏰ Created time"
    }
```

- --

## 提示

- 包括数据类型、`PK`/`FK` 注释以及带有上下文表情符号的**注释字符串**
- 使用清晰的动词短语关系标签：`"owns"`， `"contains"`、`"assigned to"`
- 基数表示法：
  - `||--o{` 一对多
  - `||--||` 一对一
  - `}o--o{` 多对多
  - `o` = 零个或多个，`|` = 恰好一个
- 每个图表限制为 **5–7 个实体** — 按域分割大型模式
- 实体名称：`UPPER_CASE`（SQL 约定）

- --

## 模板

```mermaid
erDiagram
    accTitle: Your Title Here
    accDescr: Describe the data model and key relationships between entities

    ENTITY_A ||--o{ ENTITY_B : "has many"
    ENTITY_B ||--|| ENTITY_C : "belongs to"

    ENTITY_A {
        uuid id PK "🔑 Primary key"
        string name "📝 Display name"
    }

    ENTITY_B {
        uuid id PK "🔑 Primary key"
        uuid entity_a_id FK "🔗 Reference"
        string value "📊 Value field"
    }
```

- --

## 复杂示例

A 多租户 SaaS 平台架构，具有跨越三个域的 10 个实体 - 身份和访问、计费和订阅以及审计和安全。关系显示了从租户隔离到用户权限再到发票生成的完整基数图。

```mermaid
erDiagram
    accTitle: SaaS Multi-Tenant Platform Schema
    accDescr: Ten-entity data model for a multi-tenant SaaS platform covering identity management, role-based access, subscription billing, and audit logging with full cardinality relationships

    TENANT ||--o{ ORGANIZATION : "contains"
    ORGANIZATION ||--o{ USER : "employs"
    ORGANIZATION ||--|| SUBSCRIPTION : "holds"
    USER }o--o{ ROLE : "assigned"
    ROLE ||--o{ PERMISSION : "grants"
    SUBSCRIPTION ||--|| PLAN : "subscribes to"
    SUBSCRIPTION ||--o{ INVOICE : "generates"
    USER ||--o{ AUDIT_LOG : "produces"
    TENANT ||--o{ AUDIT_LOG : "scoped to"
    USER ||--o{ API_KEY : "owns"

    TENANT {
        uuid id PK "🔑 Primary key"
        string name "🏢 Tenant name"
        string subdomain "🌐 Unique subdomain"
        string tier "🏷️ Service tier"
        boolean active "✅ Active status"
        timestamp created_at "⏰ Created time"
    }

    ORGANIZATION {
        uuid id PK "🔑 Primary key"
        uuid tenant_id FK "🔗 Tenant reference"
        string name "👥 Org name"
        string billing_email "📧 Billing contact"
        int seat_count "📊 Licensed seats"
    }

    USER {
        uuid id PK "🔑 Primary key"
        uuid org_id FK "🔗 Organization reference"
        string email "📧 Login email"
        string display_name "👤 Display name"
        string status "📊 Account status"
        timestamp last_login "⏰ Last active"
    }

    ROLE {
        uuid id PK "🔑 Primary key"
        uuid tenant_id FK "🔗 Tenant scope"
        string name "🏷️ Role name"
        string description "📝 Role purpose"
        boolean system_role "🔒 Built-in flag"
    }

    PERMISSION {
        uuid id PK "🔑 Primary key"
        uuid role_id FK "🔗 Role reference"
        string resource "🎯 Target resource"
        string action "⚙️ Allowed action"
        string scope "🔒 Permission scope"
    }

    PLAN {
        uuid id PK "🔑 Primary key"
        string name "🏷️ Plan name"
        int price_cents "💰 Monthly price"
        int seat_limit "👥 Max seats"
        jsonb features "📋 Feature flags"
        boolean active "✅ Available flag"
    }

    SUBSCRIPTION {
        uuid id PK "🔑 Primary key"
        uuid org_id FK "🔗 Organization reference"
        uuid plan_id FK "🔗 Plan reference"
        string status "📊 Sub status"
        date current_period_start "📅 Period start"
        date current_period_end "📅 Period end"
    }

    INVOICE {
        uuid id PK "🔑 Primary key"
        uuid subscription_id FK "🔗 Subscription reference"
        int amount_cents "💰 Total amount"
        string currency "💱 Currency code"
        string status "📊 Payment status"
        timestamp issued_at "⏰ Issue date"
    }

    AUDIT_LOG {
        uuid id PK "🔑 Primary key"
        uuid tenant_id FK "🔗 Tenant scope"
        uuid user_id FK "👤 Acting user"
        string action "⚙️ Action performed"
        string resource_type "🎯 Target type"
        uuid resource_id "🔗 Target ID"
        jsonb metadata "📋 Event details"
        timestamp created_at "⏰ Event time"
    }

    API_KEY {
        uuid id PK "🔑 Primary key"
        uuid user_id FK "👤 Owner"
        string prefix "🏷️ Key prefix"
        string hash "🔐 Hashed secret"
        string name "📝 Key name"
        timestamp expires_at "⏰ Expiration"
        boolean revoked "❌ Revoked flag"
    }
```

### 为什么有效

- **按域组织的 10 个实体** — 身份（租户、组织、用户、角色、权限）、计费（计划、订阅、发票）和安全性（审核日志、API 密钥）。关系线自然地将相关实体聚集在一起。
- **完整基数告诉业务规则** - 组织订阅的 `||--||`（一对一）意味着每个组织一个订阅。 User-Role 的 `}o--o{`（多对多）意味着灵活的 RBAC。每个关系符号都编码一个约束。
- **每个字段都有类型、注释和用途** - 用于模式生成的 PK/FK，用于人工扫描的表情符号注释。开发人员可以阅读此图并直接编写迁移脚本。
