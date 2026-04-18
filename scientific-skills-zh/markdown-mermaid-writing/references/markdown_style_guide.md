<!-- 来源：https://github.com/SuperiorByteWorks-LLC/agent-project |许可证：Apache-2.0 |作者：Clayton Young / Superior Byte Works, LLC (Boreal Bytes) -->

# Markdown 风格指南

> **对于 AI 代理：** 阅读此文件以了解所有核心格式规则。创建任何 Markdown 文档时，请遵循这些约定以获得一致、专业的输出。当您的文档类型存在模板时，请从它开始 - 请参阅[模板](#templates).
>
> **对于人类：** 本指南确保项目中的每个 Markdown 文档都是干净的、可扫描的、引用良好的，并且在 GitHub 上呈现精美的。从您的 `AGENTS.md` 或贡献指南中引用它。

* *目标平台：** GitHub Markdown（问题、PR、讨论、Wiki、`.md` 文件）
* *设计目标：** 清晰、专业的文档，通过一致的结构、有意义的格式、正确的引用和策略性使用来有效地进行沟通图。

- --

## 代理快速入门

1. **识别文档类型** → 检查[模板](#templates)是否存在
2. **首先是结构** → 标题层次结构，然后是内容
3. **应用本指南中的格式** → 标题、文本、列表、表格、图像、链接
4. **添加引文** → 所有声明和来源的脚注参考
5. **考虑图表** → [美人鱼图](mermaid_style_guide.md)会比文本更好地传达这一点吗？
6. **添加可折叠部分** → 用于补充细节、演讲者注释或冗长的上下文
7. **验证** → 运行[质量检查表](#quality-checklist)

- --

## 核心原则

| ＃|原理|规则|
| --- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1 | **在他们提问之前先回答** |预测读者的问题并在线解决它们。一份优秀的文档能够在疑虑形成时解决它们——读者读完时不会有挥之不去的“但是……呢？”                            |
| 2 | **可先扫描** |读者在阅读之前先浏览一下。使用标题、粗体和列表使结构一目了然。                                                                                    |
| 3 | **引用所有内容** |每个声明、统计数据或外部引用都会有一个带有完整 URL 的脚注引用。没有孤儿索赔。                                                                                  |
| 4 | **文字墙上的图表** |如果概念涉及流程、关系或结构，请在文本旁边使用[美人鱼图](mermaid_style_guide.md)。                                                               |
| 5 | **信息丰富** |不要隐藏细节——将它们暴露出来。使用可折叠部分来实现深度而不混乱，但永远不要省略信息，因为“他们可能不需要它”。如果相关，请包含它。 |
| 6 | **结构一致** |每个文档中具有相同的标题层次结构、相同的格式模式、相同的表情符号位置。|
| 7 | **每节一个想法** |每个标题应涵盖一个主题。如果您要涵盖两个想法，请分成两个标题。                                                                                                |
| 8 | **专业但平易近人** |格式干净，没有杂乱，没有装饰噪音，但不生硬或学院派。像高级工程师向同事解释一样写作。                                                       |

- --

## 🗂️ 一切都是代码

一切都是代码。 PR、问题、看板 - 它们都是存储库中的 Markdown 文件，而不是平台数据库中捕获的数据。

### 为什么这很重要

- **便携式** - GitHub → GitLab → Gitea → 任何地方。您的项目管理数据不会被任何供应商锁定。切换平台和您的问题、PR 记录和看板 — 它们只是文件。
- **AI 原生** — 代理可以通过本地文件访问来读取每个问题、PR 记录和看板。没有 API 令牌、没有速率限制、没有特定于平台的查询。 `grep` 每次都击败 `gh api`。
- **可审核** — 项目管理变更与代码变更经过相同的 PR 审核流程。每次董事会更新，每个问题状态更改 - 都在 git 历史记录中，带有属性和时间戳。

### 它是如何工作的

|什么 |它住在哪里| GitHub 做什么 |
| -------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **拉取请求** | `docs/project/pr/pr-NNNNNNNN-short-description.md` | GitHub PR 是一个细指针——人们去那里评论差异、批准和观看 CI。文件中记录了更改的内容、原因以及学到的内容。 |
| **问题** | `docs/project/issues/issue-NNNNNNNN-short-description.md` | GitHub Issues 是一个通知和评论层。文件中包含错误报告、功能请求、调查日志和解决方案。                            |
| **看板** | `docs/project/kanban/{scope}-{id}-short-description.md` |无需外部板工具。修改您分支中的董事会，将其与您的 PR 合并。董事会随着代码库的发展而发展。                                        |
| **决策记录** | `docs/decisions/NNN-{slug}.md` |根本没有在 GitHub 中进行跟踪——纯粹是 repo-native。                                                                                                                 |

### 规则

> 📌 **不要在 GitHub 的 UI 中捕获应在文件中捕获的信息。** 在 GitHub 中批准 PR。观看 GitHub 中的 CI。在 GitHub 中发表评论。但实际内容——描述、调查、决定——存在于提交的文件中。如果值得写下来，就值得提交。

### 跟踪文档的模板

- [拉取请求记录](markdown_templates/pull_request.md) — PR 描述就是这个文件
- [问题记录](markdown_templates/issue.md) — 作为存储库文件的错误报告和功能请求
- [看板](markdown_templates/kanban.md) — 与代码合并的冲刺/项目板

See [文件约定](#file-conventions-for-tracked-documents)用于目录结构和命名。

- --

## 文档结构

### 标题和元数据

每个文档都以一个 H1 标题开头，后跟一个简短的上下文行和一个分隔符：

```markdown
# Document Title Here

_Brief context — project name, date, or purpose in one line_

---
```

- **一个 H1每个文档** — 不再是
- 斜体上下文行 — 该文档是什么、何时以及为谁
- 水平规则将元数据与内容分开

### 标题层次结构

|水平|语法 |使用 |每个文档的最大数量|
| -----| ---------------- | ----------------------- | ------------------- |
| H1 | `# Title` |文档标题 | **1**（正好一个）|
| H2 | `## Section` |主要栏目| 4–10 |
| H3 | `### Topic` |章节内的主题 |每半小时 2–5 |
| H4 | `#### Subtopic` |需要时的副主题 |每 H3 2–4 |
| H5+ |切勿使用| — | 0 |

* *规则：**

- **永远不要跳过关卡** — 不要从 H2 跳到 H4
- **H2 标题中的表情符号** — 每个 H2 一个表情符号，开头：`## 📋 Project Overview`
- **H3/H4 中没有表情符号** — 保留小标题clean
- **句子大小写** — `## 📋 Project overview` 不是 `## 📋 Project Overview`（例外：专有名词）
- **描述性标题** — `### Authentication flow` 不是 `### Details`

- --

## 文本格式

### 粗体、斜体、代码

|格式|语法 |何时使用 |示例|
| ---------- | ------------ | -------------------------------------------------------- | ----------------------------------- |
| **粗体** | `**text**` |关键术语、重要概念、重点 | **主数据库** 处理写入 |
| _斜体_ | `*text*` |定义、标题、微妙的强调|该过程称为_sharding_ |
| `Code` | `` `text` `` | Technical terms, commands, file names, values | Run `npm install` 安装 |
| ~~罢工~~ | `~~text~~` |已弃用的内容、更正 | ~~旧方法~~被 v2 取代 |

* *规则：**

- **谨慎粗体** — 如果一切都是粗体，则没有任何内容是粗体。每段最多 2–3 个粗体术语。
- **不要组合**粗体和斜体 (`***text***`) — 选择一个
- **任何技术代码** — 文件名 (`README.md`)、命令 (`git push`)、配置值 (`true`)、环境变量(`NODE_ENV`)
- **切勿将整个句子加粗** — 将句子中的关键词加粗

### 块引号

使用块引号进行定义、标注和重要说明：

```markdown
> **Definition:** A _load balancer_ distributes incoming network traffic
> across multiple servers to ensure no single server bears too much demand.
```

用于警告和标注：

```markdown
> ⚠️ **Warning:** This operation is destructive and cannot be undone.

> 💡 **Tip:** Use `--dry-run` to preview changes before applying.

> 📌 **Note:** This requires admin permissions on the repository.
```

- 带表情符号的前缀 + 用于键入标注的粗体标签
- 将块引用保持在 1–3 行
- 不要嵌套块引用 (`>>`)

- --

## 列表

### 何时使用每种类型

|列表类型 |语法 |当|
|时使用--------- | ------------ | ----------------------------------------------------- |
|子弹 | `- item` |项目没有固有顺序 |
|编号| `1. step` |步骤必须按顺序进行|
|复选框 | `- [ ] item` |跟踪完成情况（议程、清单）|

### 格式规则

- **一致的缩进** - 子项有 2 个空格（某些渲染器使用 4 个；选择一个，坚持使用）
- **并行结构** - 列表中的每个项目应具有相同的语法形式
- **末尾没有句号**，除非项目是完整的句子
- **保持项目简洁** - 如果项目符号需要段落，它应该是一个小节，而不是
- **最大嵌套深度：2级** - 如果您需要第三级，请重组

```markdown
✅ Good — parallel structure, concise:

- Configure the database connection
- Run the migration scripts
- Verify the schema changes

❌ Bad — mixed structure, verbose:

- You need to configure the database
- Migration scripts
- After that, you should verify that the schema looks correct
```

- --

## 链接和引用

### 内联links

```markdown
See the [Mermaid Style Guide](mermaid_style_guide.md) for diagram conventions.
```

- **有意义的链接文本** — `[Mermaid Style Guide]` 不是 `[click here]` 或 `[link]`
- **内部链接的相对路径** — `[Guide](./README.md)` 不是绝对 URL
- **完整 URL**对于外部链接 — 始终为 `https://`

### 脚注引用

* *每项声明、统计数据或对外部工作的引用都必须有脚注引用。** 这对于可信度来说是不可协商的。

```markdown
Markdown was created by John Gruber in 2004 as a lightweight
markup language designed for readability[^1]. GitHub adopted
Mermaid diagram support in February 2022[^2].

[^1]: Gruber, J. (2004). "Markdown." _Daring Fireball_. https://daringfireball.net/projects/markdown/

[^2]: GitHub Blog. (2022). "Include diagrams in your Markdown files with Mermaid." https://github.blog/2022-02-14-include-diagrams-markdown-files-mermaid/
```

* *引用格式：**

```
[^N]: Author/Org. (Year). "Title." *Publication*. https://full-url
```

* *规则：**

- **按顺序编号** — `[^1]`、`[^2]`、`[^3]` 按出现顺序
- **始终包含完整 URL** — 读者必须能够访问source
- **将所有脚注分组在文档底部** - 在 `## References` 部分下或在最后
- **每个外部声明都需要一个** - 统计、引用、方法、提到的工具
- **内部项目链接不需要脚注** - 使用内联链接代替

### 参考样式链接（用于重复） URL)

当相同的 URL 多次出现时，使用引用样式的链接来保持文本简洁：

```markdown
The [official docs][mermaid-docs] cover all diagram types.
See [Mermaid documentation][mermaid-docs] for the full syntax.

[mermaid-docs]: https://mermaid.js.org/ 'Mermaid Documentation'
```

- --

## 图像和图形

### 放置和语法

```markdown
![Descriptive alt text for screen readers](images/architecture_overview.png)
_Figure 1: System architecture showing the three-tier deployment model_
```

* *规则：**

- **与内容内嵌** — 将图像放在相关的位置，而不是单独的“图像”部分
- **描述性替代文本** — `![Three-tier architecture diagram]` 不是 `![image]` 或 `![screenshot]`
- **下面的斜体标题** — `*Figure N: What this image shows*`
- **按顺序对数字进行编号** — 图 1、图 2 等，如果多个图像
- **相对路径** — `images/file.png` 不是绝对路径
- **合理的文件大小** — 压缩 PNG，尽可能使用 SVG

### 图像命名约定

```
{document-slug}_{description}.{ext}

Examples:
  auth_flow_overview.png
  deployment_architecture.svg
  api_response_example.png
```

### 何时不使用image

如果内容可以表达为**美人鱼图**，则优于静态图像：

|场景|使用|
| -------------------------- | ------------------------------------------ |
|架构图|美人鱼`flowchart`或`architecture-beta` |
|序列/交互|美人鱼`sequenceDiagram` |
|数据模型|美人鱼`erDiagram` |
|时间轴 |美人鱼`timeline`或`gantt` |
|用户界面截图|图片（美人鱼做不到）|
|照片/真实世界图像|图片|
|复杂数据可视化|图片或美人鱼 `xychart-beta` |

 有关图表类型选择和样式的信息，请参阅[美人鱼风格指南](mermaid_style_guide.md)。

- --

## 表格

### 何时使用表格

- **结构化比较** — 功能、选项、权衡
- **参考数据** — 配置值、API 参数、状态代码
- **时间表和矩阵** — 时间表、责任分配

### 何时不使用表格

- **叙述内容** — 使用段落代替
- **简单列表** — 使用项目符号
- **超过 5 列** — 在移动设备上变得不可读；重组

### 格式化

```markdown
| Feature | Free Tier | Pro Tier | Enterprise |
| ------- | --------- | -------- | ---------- |
| Users   | 5         | 50       | Unlimited  |
| Storage | 1 GB      | 100 GB   | Custom     |
| Support | Community | Email    | Dedicated  |
```

* *规则：**

- **始终为标题行** — 无无标题表
- **左对齐文本列** — `|---|`（默认）
- **右对齐数字列** — `|---:|`（适当时）
- **简洁的单元格内容** — 每个单元格 1-5 个单词。如果您需要更多，这不是表格问题
- **粗体关键列** - 第一列或读者首先扫描的列
- **列内格式一致** - 不要混合句子和片段

- --

## 代码块

### 内联代码

使用反引号进行技术散文中的术语：

```markdown
Run `git status` to check for uncommitted changes.
The `NODE_ENV` variable controls the runtime environment.
```

### 防护代码块

始终指定语法突出显示的语言：

````markdown
```python
defcalculate_average(values: list[float]) -> float:
 """返回值列表的算术平均值。"""
 返回 sum(values) / len(values)
```
````

* *规则：**

- **始终包含语言标识符** — ` ```python `， ` ```bash `、` ```json ` 等 
- **使用 ` ```text ` 进行纯输出** — 不是 ` ``` `语言
- **保持块集中** — 显示相关片段，而不是整个文件
- **如果需要上下文，添加注释** — `# Configure the database connection` 位于块的顶部

- --

## 可折叠部分

使用 HTML `<details>` 来补充不应包含的内容混乱主要流程 - 演讲者注释、实现细节、详细日志或可选的深入研究。

```markdown
<details>
<summary><strong>💬 Speaker Notes</strong></summary>

- Key talking point one
- Transition to next topic
- **Bold** emphasis works inside details
- [Links](https://example.com) work too

</details>

---
```

* *规则：**

- **默认折叠** - `<details>` 标签自动折叠
- **描述性摘要** - `<strong>💬 Speaker Notes</strong>` 或 `<strong>📋 Implementation Details</strong>`
- **`<summary>` 标签后的空行** - markdown 需要在块内渲染
- **始终跟随`---`** - 每个 `</details>` 后面的水平线用于视觉分离
- **任何降价都可以在里面** - 项目符号、粗体、链接、代码块、表格

### 常见可折叠模式

|摘要标签|用于 |
| -------------------- | ------------------------------------------------ |
| 💬 **演讲者笔记** |演示谈话要点、时间安排、过渡 |
| 📋 **详细信息** |扩展解释，详细上下文 |
| 🔧 **实施** |技术细节、代码示例、配置 |
| 📊 **原始数据** |完整输出、日志、数据表|
| 💡 **背景** |有帮助但不是必需的上下文|

- --

## 水平规则

使用`---`（三个连字符）进行视觉分离：

```markdown
---
```

* *何时使用：**

- **每次之后`</details>` 块** — 强制，创建清晰的分隔
- **在标题/元数据之后** — 将文档标题与内容分开
- **在主要部分之间** — 当单独的 H2 标题无法创建足够的视觉分隔时
- **在脚注/引用之前** — 将内容与引文列表分开

* *何时不这样做使用：**

- 在每个段落之间（太忙）
- 在同一 H2 内的 H3 子部分之间（使用空格代替）

- --

## 批准的表情符号集

每个 H2 标题在开头有一个表情符号。在正文中谨慎使用，仅用于标注和强调。

### 章节标题

|表情符号 |用于|
| -----| -------------------------------------- |
| 📋 |概述、摘要、议程、清单 |
| 🎯 |目标、目的、成果、目标|
| 📚 |内容、文档、主体|
| 🔗 |资源、参考资料、链接 |
| 📍 |议程、导航、当前位置 |
| 🏠 |家政、物流、公告|
| ✍️ |任务、分配、行动项 |

### 状态和结果

|表情符号 |含义|
| -----| ------------------------------------------------ |
| ✅ |成功、完整、正确、批准|
| ❌ |失败、不正确、回避、拒绝|
| ⚠️ |警告、小心、重要通知|
| 💡 |提示、见解、想法、最佳实践|
| 📌 |重要，关键，记住|
| 🚫 |禁止、不做、封杀 |

### 技术及流程

|表情符号 |含义|
| -----| --------------------------------- |
| ⚙️ |配置、设置、流程|
| 🔧 |工具、实用程序、设置|
| 🔍 |分析、调查、回顾|
| 📊 |数据、指标、分析 |
| 📈 |成长、趋势、改进|
| 🔄 |循环、刷新、迭代|
| ⚡ |性能、速度、快速行动|
| 🔐 |安全、认证、隐私|
| 🌐 | Web、API、网络、全球 |
| 💾 |存储、数据库、持久化|
| 📦 |打包、工件、部署 |

### 人员和协作

|表情符号 |含义|
| -----| ----------------------------------- |
| 👤 |用户、个人、个体|
| 👥 |团队、团体、协作|
| 💬 |讨论、评论、演讲者笔记 |
| 🎓 |学习、教育、知识|
| 🤔 |问题、考虑、反思|

### 表情符号规则

1. **每个 H2 标题一个**位于开头 — `## 📋 Overview`
2. **H3/H4 中没有** — 保持小标题干净
3. **正文中的内容较少** — 仅适用于标注 (`> ⚠️ **Warning:**`)和关键标记 
4. **绝不在**：标题 (H1)、代码块、链接文本、表格数据单元格
5. **没有装饰性表情符号** — 🎉 💯 🔥 🎊 💥 ✨ 添加噪音，没有意义
6. **一致性** — 相同的表情符号 = 项目中所有文档的相同含义

- --

## 美人鱼图集成

* *每当内容描述流程、结构、关系或流程时，请考虑美人鱼图是否比单独的散文更好地传达它。** 图表和文本在一起比单独使用更有效。

### 何时添加图

* *任何时候你的文本描述流程、结构、关系、时间或比较，都有一个美人鱼图可以更好地传达它。**扫描下表以确定正确的类型，然后遵循此工作流程：

1. **首先阅读 [美人鱼风格指南](mermaid_style_guide.md)** — 表情符号、调色板、可访问性、复杂性管理
2. **然后打开具体类型文件** — exemplar、tips、template、complex example

|您的内容描述了... |添加... |键入文件 |
| ---------------------------------------------------------------- | ------------------------ | --------------------------------------------------- |
|流程、工作流程、决策逻辑中的步骤 | **流程图** | [流程图.md](mermaid_diagrams/流程图.md) |
|谁与谁交谈以及何时交谈（API 调用、消息）| **序列图** | [sequence.md](mermaid_diagrams/sequence.md) |
|类层次结构、类型关系、接口 | **类图** | [class.md](mermaid_diagrams/class.md) |
|状态转换、实体生命周期、状态机 | **状态图** | [state.md](mermaid_diagrams/state.md) |
|数据库架构、数据模型、实体关系 | **ER图** | [er.md](mermaid_diagrams/er.md) |
|项目时间表、路线图、任务依赖关系 | **甘特图** | [gantt.md](mermaid_diagrams/gantt.md) |
|整体的部分、比例、分布| **饼图** | [pie.md](mermaid_diagrams/pie.md) |
| Git 分支策略、合并/发布流程 | **Git 图表** | [git_graph.md](mermaid_diagrams/git_graph.md) |
|概念层次、头脑风暴、主题图| **思维导图** | [mindmap.md](mermaid_diagrams/mindmap.md) |
|按时间顺序排列的事件、里程碑、历史 | **时间表** | [时间线.md](mermaid_diagrams/timeline.md) |
|用户体验、满意度评分、旅程 | **用户旅程** | [user_journey.md](mermaid_diagrams/user_journey.md) |
|二-轴比较、优先级矩阵 | **象限图** | [象限.md](mermaid_diagrams/象限.md) |
|需求可追溯性、合规性映射 | **需求图** | [要求.md](mermaid_diagrams/要求.md) |
|不同缩放级别的系统架构| **C4图** | [c4.md](mermaid_diagrams/c4.md) |
|流量大小、资源分配、预算 | **桑基图** | [sankey.md](mermaid_diagrams/sankey.md) |
|数字趋势、条形图、折线图 | **XY 图表** | [xy_chart.md](mermaid_diagrams/xy_chart.md) |
|组件布局、空间排列、层次| **框图** | [block.md](mermaid_diagrams/block.md) |
|工作项跟踪、状态板、任务栏 | **看板** | [kanban.md](mermaid_diagrams/kanban.md) |
|二进制协议布局、数据包格式| **数据包图** | [数据包.md](mermaid_diagrams/数据包.md) |
|云基础设施、服务拓扑、网络 | **架构图** | [架构.md](mermaid_diagrams/architecture.md) |
|多维度对比、技巧、雷达分析 | **雷达图** | [雷达.md](mermaid_diagrams/radar.md) |
|层级比例、预算细目| **树形图** | [treemap.md](mermaid_diagrams/treemap.md) |

> 💡 **选择正确的类型，而不是简单的类型。** 不要默认使用流程图来处理所有事情 - 对于按时间顺序排列的事件，时间线比流程图更好，序列图更适合服务交互，ER 图更适合数据模型。扫描上表并将您的内容与最具体的类型相匹配。 **如果你发现自己正在写一段描述视觉概念的段落，请停下来并用图表表示它。**

### 如何集成

将图表**与相关文本**放在一起**，而不是放在单独的部分中：

````markdown
### Authentication Flow

The login process validates credentials, checks MFA status,
and issues session tokens. Failed attempts are logged for
security monitoring.

‎```mermaid
sequenceDiagram
accTitle: Login Authentication Flow
accDescr: User login sequence through API and auth service

    participant U as 👤 User
    participant A as 🌐 API
    participant S as 🔐 Auth Service

    U->>A: POST /login
    A->>S: Validate credentials
    S-->>A: ✅ Token issued
    A-->>U: 200 OK + session

‎```

The token expires after 24 hours. See [Authentication flow](#authentication-flow)
for refresh token details.
````

* *始终遵循[美人鱼风格指南](mermaid_style_guide.md)**进行图表样式 -表情符号、颜色类别、辅助功能 (`accTitle`/`accDescr`)和特定于类型的约定。

- --

## 空白和间距

- **段落之间的空行** — 始终
- **标题前后的空行** — 始终
- **空行代码块之前和之后** — 总是
- **块引用之前和之后的空行** — 总是
- **列表项之间没有空行** — 保持列表紧密
- **没有尾随空格** — 干净的行结尾
- **文件末尾有一个空行** — 标准约定
- **不超过一个连续空行** —两个空行 = 太多空间

- --

## 质量检查表

### 结构

- [ ]恰好一个 H1 标题
- [ ]标题层次结构正确（H1 → H2 → H3 → H4，无跳过）
- [ ]每个 H2 恰好有一个开头的表情符号
- [ ] H3 和 H4 没有表情符号
- [ ]标题元数据之后和每个 `</details>` 块之后的水平规则

### 内容

- [ ]每个外部声明都有脚注引用
- [ ]所有脚注都有完整的URLs
- [ ]所有链接均已测试且正常工作
- [ ]有意义的链接文本（无“单击此处”）
- [ ]粗体用于关键术语，而不是整个句子
- [ ]所有技术术语的代码格式

### 视觉元素

- [ ]图像具有描述性替代文本
- [ ]图像具有斜体图形标题
- [ ]与相关内容内联放置的图像（不在单独的部分中）
- [ ]表格具有标题行和一致的格式
- [ ]在适用的情况下考虑美人鱼图（使用`accTitle`/`accDescr`)

### 可折叠部分

- [ ] `<details>` 块具有描述性 `<summary>` 标签
- [ ] `<summary>` 标签后的空行（用于降价渲染）
- [ ]每个 `</details>` 块后的水平规则 `---`
- [ ]折叠内的内容正确渲染 

### Polish

- [ ]无拼写或语法错误 
- [ ]一致的空白（无尾随空格，无双空格）
- [ ]列表中的并行语法结构
- [ ]在 GitHub 明暗模式下正确渲染

- --

## 模板

模板为常见文档类型提供预构建的结构。复制模板，填写内容，然后按照此样式指南进行格式化。每个模板都强制执行上述原则 - 引文、图表、可折叠深度和自我回答结构。

|文件类型 |模板|最适合|
| ------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
|演示/简报 | [演示.md](markdown_templates/演示.md) |幻灯片式文档，包含演讲者笔记、结构化部分和视觉流程 |
|研究论文/分析 | [research_paper.md](markdown_templates/research_paper.md) |数据驱动分析、文献综述、方法论+大量引用的发现|
|项目文档| [project_documentation.md](markdown_templates/project_documentation.md) |软件/产品文档 — 架构、入门、API 参考、贡献指南 |
|决策记录（ADR/RFC）| [decision_record.md](markdown_templates/decision_record.md) |记录做出决定的原因 - 背景、评估的选项、结果、后果 |
|操作方法/教程指南 | [how_to_guide.md](markdown_templates/how_to_guide.md) |包含先决条件、验证步骤和故障排除的分步说明 |
|状态报告/执行简介| [status_report.md](markdown_templates/status_report.md) |为领导层和利益相关者提供进度更新、风险总结、所需决策 |
|拉取请求记录 | [pull_request.md](markdown_templates/pull_request.md)| PR 文档，包含变更清单、测试证据、回滚计划和审核说明 |
|问题记录 | [问题.md](markdown_templates/问题.md) |错误报告（重现步骤、根本原因）和功能请求（验收标准、用户故事）|
|看板| [kanban.md](markdown_templates/kanban.md) |使用可视板、WIP 限制、指标和阻止的项目跟踪 Sprint/发布/项目工作 |

### 跟踪文档的文件约定

某些模板生成的文档会随着时间的推移而累积。使用这些目录约定：

|文件类型 |目录 |命名模式 |示例|
| ---------------- | ---------------------- | ------------------------------------------- | --------------------------------------------------------------------------- |
|拉请求 | `docs/project/pr/` | `pr-NNNNNNNN-short-description.md` | `docs/project/pr/pr-00000123-fix-auth-timeout.md` |
|问题 | `docs/project/issues/` | `issue-NNNNNNNN-short-description.md` | `docs/project/issues/issue-00000456-add-export-filter.md` |
|看板| `docs/project/kanban/` | `{scope}-{identifier}-short-description.md` | `docs/project/kanban/sprint-2026-w07-agentic-template-modernization.md` |
|决策记录| `docs/decisions/` | `NNN-{slug}.md` | `docs/decisions/001-use-postgresql.md` |
|状态报告| `docs/status/` | `status-{date}.md` | `docs/status/status-2026-02-14.md` |

### 选择模板

- **向人们演示？** → 演示
- **发布分析或研究？** → 研究论文
- **记录代码库或产品？** → 项目文档
- **记录您选择 X 而不是 Y 的原因？** → 决策记录
- **教某人如何做某事？** → 操作指南
- **更新领导进度？** → 状态报告
- **为后代记录PR？** → 拉取请求记录
- **跟踪错误或请求功能？** → 问题记录
- **管理工作项冲刺或项目？** → 看板
- **这些都不适合？** → 直接从本风格指南的规则开始 - 不需要模板

- --

## 常见错误

### ❌ 每个标题多个表情符号

```markdown
## 📚📊📈 Content Topics ← Too many
```

✅修复：每个 H2

 一个表情符号```markdown
## 📚 Content topics
```

### ❌ 缺少引用

```markdown
Studies show 73% of developers prefer Markdown. ← Where's the source?
```

✅ 修复：添加脚注

```markdown
Studies show 73% of developers prefer Markdown[^1].

[^1]: Stack Overflow. (2024). "Developer Survey Results." https://survey.stackoverflow.co/2024
```

### ❌ 没有文字墙结构

```markdown
The system handles authentication by first checking the JWT token
validity, then verifying the user exists in the database, then
checking their permissions against the requested resource...
```

✅ 修复：使用列表、标题或图表

```markdown
### Authentication flow

1. Validate JWT token signature and expiration
2. Verify user exists in the database
3. Check user permissions against the requested resource
```

### ❌ 单独部分中的图像

```markdown
## Content

[paragraphs of text]

## Screenshots

[all images grouped here] ← Disconnected from context
```

✅ 修复：将图像内联放置在其中相关

### ❌可折叠部分后没有水平线

```markdown
</details>
### Next Topic  ← Runs together visually
```

✅ 修复：始终在之后添加`---` `</details>`

```markdown
</details>

- --

### Next topic ← Clear separation
```

- --

## 资源

- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/) · [美人鱼风格指南](mermaid_style_guide.md) · [GitHub Basic格式](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
