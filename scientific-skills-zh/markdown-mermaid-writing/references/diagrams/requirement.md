<!-- 来源：https://github.com/SuperiorByteWorks-LLC/agent-project |许可证：Apache-2.0 |作者：Clayton Young / Superior Byte Works, LLC (Boreal Bytes) -->

# 需求图

> **返回[风格指南](../mermaid_style_guide.md)** — 首先阅读风格指南了解表情符号、颜色和可访问性规则。

* *语法关键字：** `requirementDiagram`
* *最适合：**系统需求可追溯性、合规性映射、正式需求工程
* *何时不使用：**非正式任务跟踪（使用 [Kanban](kanban.md)）、一般关系（使用 [ER](er.md)）

- --

## 示例图

```mermaid
requirementDiagram

    requirement high_availability {
        id: 1
        text: System shall maintain 99.9 percent uptime
        risk: high
        verifymethod: test
    }

    requirement data_encryption {
        id: 2
        text: All data at rest shall be AES-256 encrypted
        risk: medium
        verifymethod: inspection
    }

    requirement session_timeout {
        id: 3
        text: Sessions expire after 30 minutes idle
        risk: low
        verifymethod: test
    }

    element auth_service {
        type: service
        docref: auth-service-v2
    }

    element crypto_module {
        type: module
        docref: crypto-lib-v3
    }

    auth_service - satisfies -> high_availability
    auth_service - satisfies -> session_timeout
    crypto_module - satisfies -> data_encryption
```

- --

## 提示

- 每个需求需要：`id`、`text`、`risk`、`verifymethod`
- **`id` 必须是数字** — 使用`id: 1`、`id: 2`等（`REQ-001`等破折号会导致解析错误）
- 风险级别：`low`、`medium`、`high`（全部小写）
- 验证方法：`analysis`、 `inspection`、`test`、`demonstration`（全部小写）
- 使用`element`设计满足要求的组件
- 关系类型：`- satisfies ->`、`- traces ->`、`- contains ->`、 `- derives ->`、`- refines ->`、`- copies ->`
- 遵守每个图表的 **3–5 要求**
- 避免文本字段中的特殊字符 - 拼写出符号（例如，“99.9%”而不是“99.9%”）
- 在内部使用 4 个空格缩进`{ }` 块

- --

## 模板

```mermaid
requirementDiagram

    requirement your_requirement {
        id: 1
        text: The requirement statement here
        risk: medium
        verifymethod: test
    }

    element your_component {
        type: service
        docref: component-ref
    }

    your_component - satisfies -> your_requirement
```
