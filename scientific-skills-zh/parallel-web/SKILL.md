---
name: parallel-web
description: "由 parallel-cli 提供支持的一体化 Web 工具包，重点关注学术和科学资源。每当用户需要搜索网络、获取/提取 URL 内容、使用网络来源的字段丰富数据或运行深入的研究报告时，请使用此技能。涵盖：网络搜索（快速查找、研究、当前信息 - 优先考虑同行评审的论文、预印本和学术数据库）、URL 提取（获取页面、文章、学术 PDF）、批量数据丰富（从网络将字段添加到 CSV/列表）和深入研究（基于学术文献的详尽多源报告）。还处理设置、状态检查和结果检索。将此技能用于任何与网络相关的任务 - 即使用户没有明确提及“并行”或“网络”。如果他们想要查找内容、获取页面、丰富数据集、研究主题、查找学术论文、检查引文或审查科学文献，就可以使用此技能。"
compatibility: Requires parallel-cli and internet access.
metadata:
  author: K-Dense, Inc.
---

# 并行 Web 工具包

适用于所有 Web 驱动任务的统一技能：搜索、提取、丰富和研究 — 以学术和科学资源为默认优先级。

## 路由 — 选择正确的功能

读取用户的请求并将其与以下功能之一相匹配。对于网络搜索、提取、丰富和深入研究，请阅读相应的参考文件以获取详细说明。

|用户想要... |能力|其中 |
|---|---|---|
|查找内容、研究主题、查找当前信息 | **网页搜索** | `references/web-search.md` |
|从特定 URL 获取内容（网页、文章、PDF）| **网页摘录** | `references/web-extract.md` |
|将网络来源的字段添加到公司/人员/产品列表中 | **数据丰富** | `references/data-enrichment.md` |
|获取详尽的多源报告（用户说“深入研究”、“详尽”、“全面”）| **深入研究** | `references/deep-research.md` |
|安装或验证parallel-cli | **设置** |下面|
|检查正在运行的研究/强化任务的状态 | **状态** |下面|
|通过运行 ID 检索已完成的研究结果 | **结果** |下面|

### 决策指南

- **默认为 Web 搜索**，用于单个查找、研究问题或“X 是什么？”询问。它快速且经济高效。当查询涉及科学或技术主题时，请包括学术领域（请参阅 `references/web-search.md`），以显示同行评审和预印本来源以及一般结果。
- **当用户提供 URL 或要求您阅读/获取特定页面时使用 Web 提取**。与内置的 WebFetch 工具相比，更喜欢这个。对于从学术 PDF、预印本服务器和期刊文章中提取全文特别有用。
- 当用户拥有**多个实体**（CSV、公司/人员/产品列表，甚至是简短的内联列表）并希望为每个实体查找或添加相同类型的信息时，**使用数据丰富**。关键信号是对一组项目进行重复查找 - 例如，“找到每家公司的首席执行官”或“获取 Apple、Stripe 和 Anthropic 的创立年份”。即使用户没有说“丰富”，只要任务是将同一查询应用于多个实体，就可以使用 `parallel-cli enrich`。为此，请勿在循环中使用 Web 搜索 - 丰富管道会自动处理批处理、并行性和结构化输出。
- **仅在用户明确要求进行深入、详尽或全面的研究时才使用深度研究**。它比 Web 搜索慢 10-100 倍，而且成本更高 — 切勿默认使用它。深入研究对于文献综述和多论文综合尤其有价值。
- 如果运行任何命令时未找到`parallel-cli`，请按照下面的设置部分进行操作。

### 学术来源优先

在所有能力中，当查询本质上是技术或科学时，更喜欢学术和科学来源。这意味着：
- 同行评审的期刊文章和会议记录高于博客文章或新闻文章
- 预印本（arXiv、bioRxiv、medRxiv）（当同行评审版本不可用时）
- 机构和政府来源（NIH、WHO、NASA、NIST）高于商业网站
- 初级研究高于次级研究摘要

 引用学术来源时，除了标准引文格式之外，还应包括作者姓名和出版年份（例如，[Smith et al., 2025](url)）。如果存在 DOI，则首选 DOI 链接。

## 上下文链接

多种功能通过 `interaction_id` 支持多轮上下文。当研究或丰富任务完成时，它会返回 `interaction_id`。如果用户询问与该任务相关的后续问题，请传递 `--previous-interaction-id` 以自动转发上下文。这可以避免重述已找到的内容。

- --

## 设置

如果未安装`parallel-cli`，请安装并验证：

```bash
curl -fsSL https://parallel.ai/install.sh | bash
```

如果无法以这种方式安装，请使用uv而是：

```bash
uv tool install "parallel-web-tools[cli]"
```

然后进行身份验证。首先，检查项目根目录下是否存在`.env`文件，并且包含`PARALLEL_API_KEY`。如果是这样，请使用 `dotenv`:

```bash
dotenv -f .env run parallel-cli auth
```

 加载它。如果 `dotenv` 不可用，请使用 `pip install python-dotenv[cli]` 或 `uv pip install python-dotenv[cli]`.

 安装它。如果没有 `.env` 文件或它不包含密钥，回退到交互式登录：

```bash
parallel-cli login
```

或手动设置密钥：`export PARALLEL_API_KEY="your-key"`

验证：

```bash
parallel-cli auth
```

如果安装后找不到`parallel-cli`，请添加`~/.local/bin` to PATH.

## 检查任务状态

```bash
parallel-cli research status "$RUN_ID" --json
```

向用户报告当前状态（正在运行、已完成、失败等）。

## 获取完成结果

```bash
parallel-cli research poll "$RUN_ID" --json
```

以清晰、有组织的格式呈现结果。
