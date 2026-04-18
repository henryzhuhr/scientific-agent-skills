<!-- 来源：https://github.com/SuperiorByteWorks-LLC/agent-project |许可证：Apache-2.0 |作者：Clayton Young / Superior Byte Works, LLC (Boreal Bytes) -->

# 操作方法/教程指南模板

> **返回 [Markdown 样式指南](../markdown_style_guide.md)** — 首先阅读样式指南以了解格式、引用和表情符号规则。

* *将此模板用于：** 分步教程、操作方法指南、入门演练、操作手册、设置说明或任何主要工作是教某人做某事的文档。旨在让读者第一次尝试就成功。

* *主要功能：**验证命令的先决条件、每个阶段预期输出的编号步骤、“验证它是否有效”检查点、常见故障的故障排除部分以及“下一步是什么”路径。

* *理念：**如果读者遇到困难，操作指南就会失败。每一步都应该是可验证的——读者应该能够在进入下一个步骤之前确认他们做得正确。预测他们会想知道“这有效吗？”的确切时刻。并在那里设置一个检查点。包括他们实际看到的错误消息，而不仅仅是快乐的路径。

- --

## 如何使用

1. 将此文件复制到您的项目
2. 将所有 `[bracketed placeholders]` 替换为您的内容 
3. **从头开始亲自测试指南** - 在干净的机器上遵循每一步。如果您跳过此步骤，则该指南有 bugs.
4. 添加 [美人鱼图](../mermaid_style_guide.md)以获取流程概述、决策点或架构上下文
5. 在每个验证步骤中包含实际输出（经过修剪）——不要只是说“您应该看到输出”

- --

## 模板

该行下面的所有内容都是模板。从这里复制：

- --

# [操作方法：具体任务说明]

_[预计时间：N 分钟] · [难度：初级/中级/高级] · [最后验证：日期]_

- --

## 📋 概述

### 您将完成什么

[一段：读者在本指南结束时将构建、配置或实现的内容。具体一点。]

### 您将学到什么

- [技能或概念 1]
- [技能或概念 2]
- [技能或概念 3]

### 流程概述

```mermaid
flowchart LR
    accTitle: Tutorial Process Overview
    accDescr: High-level steps from prerequisites through setup, configuration, and verification

    prereqs([📋 Prerequisites]) --> setup[🔧 Setup]
    setup --> configure[⚙️ Configure]
    configure --> build[📦 Build]
    build --> verify[✅ Verify]

    classDef done fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d
    class verify done
```

- --

## 📋先决条件

在开始之前，请确保您拥有：

|要求 |版本 |使用 | 进行验证安装链接|
| ---------------- | ----------- | -------------------- | ------------------------------------------------ |
| [工具/运行时] | ≥ [版本] | `[command] --version` | [安装指南](https://example.com) |
| [依赖] | ≥ [版本] | `[command] --version` | [安装指南](https://example.com) |
| [帐户/访问] | — | [如何验证] | [注册](https://example.com) |

* *验证所有先决条件：**

```bash
# Run each command — all should succeed before proceeding
[command1] --version    # Expected: [version] or higher
[command2] --version    # Expected: [version] or higher
```

> ⚠️ **不要跳过此步骤。**如果未正确安装[特定先决条件]，第 3 步将失败。

- --

## 🔧步骤

### 步骤 1：[操作动词 — 设置/创建/配置/安装]

[简要上下文：为什么此步骤是必要的 — 一句话。]

```bash
[command to run]
```

* *预期输出：**

```
[What the terminal should show — include actual output, trimmed if long]
```

> 💡 **提示：** [有关此步骤的有用上下文 - 常见变化、在不同操作系统上该怎么做等]

- --

### 步骤 2：[动作动词]

[简介上下文。]

```bash
[command to run]
```

* *预期输出：**

```
[What you should see]
```

* *如果您在此处看到错误**，请检查：

- [最常见原因和修复]
- [第二个最常见原因和修复]

- --

### 步骤 3：[动作动词]

[简要上下文。]

[如果此步骤涉及编辑文件，则显示确切内容：]

```yaml
# config/[filename]
[key]: [value]
[key]: [value]

# [Comment explaining what this section does]
[key]:
  [nested_key]: [value]
  [nested_key]: [value]
```

> 📌 **重要：** [关键细节关于这个配置——如果你弄错了会发生什么]

- --

### 步骤 4：[动作动词]

[简要上下文。]

```bash
[command to run]
```

* *预期输出：**

```
[What you should see]
```

- --

### 步骤 5： [动作动词 - 这应该是最终动作]

[简要上下文。]

```bash
[final command]
```

- --

## ✅ 验证它是否有效

运行这些检查以确认一切正常：

|检查 |命令|预期结果|
| --------- | ----------- | ------------------------- |
| [检查1] | `[command]` | [成功是什么样的] |
| [检查2] | `[command]` | [成功是什么样的] |
| [检查3] | `[command]` | [成功是什么样的] |

* *所有检查都通过？** 你就完成了。跳转到 [下一步](#-whats-next)。

* *出现故障？** 请参阅下面的[疑难解答](#-troubleshooting)。

- --

## 🔧 疑难解答

### "[读者将看到的确切错误消息]"

* *原因：** [触发此错误的原因 - 具体]

* *修复：**

```bash
[exact commands to resolve]
```

* *验证修复：**

```bash
[command to confirm the error is resolved]
```

- --

### “[另一个常见错误消息]“

 * *原因：** [什么触发此]

  * *修复：**

1. [步骤1]
2. [步骤2]
3. 重新运行失败的步骤

- --

### “[第三个常见问题 - 可能不是错误消息，而是症状]”

* *原因：** [导致此行为的原因]

* *修复：**

[使用命令的解决方案]

- --

### 仍然卡住？

- **搜索现有问题：** [docs/project/issues/](../../docs/project/issues/)
- **寻求帮助：** [docs/project/kanban/](../../docs/project/kanban/)
- **提交错误：** [问题template](../../docs/project/issues/issue-00000001-agentic-documentation-system.md)

- --

## 🚀 接下来做什么

现在您已经完成了本指南：

- **[下一个教程]** — [它涵盖的内容以及您下一步想要这样做的原因](../workflow_guide.md)
- **[参考文档]** — [在哪里学习完整的功能集](../markdown_style_guide.md)
- **[高级主题]** — [深入了解当您准备](../operational_readiness.md)

<详细信息>
<摘要><strong>📋快速参考卡</strong></summary>

本指南中的关键命令和值以供将来参考：

|行动|命令|
| -------------- | ----------- |
| [开始] | `[command]` |
| [停止] | `[command]` |
| [查看状态] | `[command]` |
| [查看日志] | `[command]` |
| [重置] | `[command]` |

</details>

- --

## 🔗 参考资料

- [官方文档](https://example.com) — [哪个部分最相关]
- [源存储库](https://github.com/SuperiorByteWorks-LLC) — [针对 bug报告和贡献]

- --

_最后验证：[日期]，[操作系统/平台版本]·由[团队/作者]维护_
