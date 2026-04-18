---
name: research-lookup
description: 使用parallel-cli 搜索（主要的快速网络搜索）、Parallel Chat API（深度研究）或 Perplexity sonar-pro-search（学术论文搜索）查找当前研究信息。自动将查询路由到最佳后端。用于查找论文、收集研究数据和验证科学信息。
allowed-tools: Read Write Edit Bash
license: MIT license
compatibility: parallel-cli required (primary); PARALLEL_API_KEY and OPENROUTER_API_KEY optional for deep/academic backends
metadata:
    skill-author: K-Dense Inc.
---

# 研究信息查找

## 概述

此技能通过**智能后端路由**提供实时研究信息查找：

- **并行cli搜索**（parallel-web技能）：所有研究查询的**主要和默认后端**。快速、经济高效的网络搜索，并优先考虑学术资源。使用 `parallel-cli search` 和 `--include-domains` 获取学术资源。
- **并行聊天 API**（`core` 模型）：需要扩展综合（60 秒至 5 分钟延迟）的复杂、多源深度研究的辅助后端。仅在明确需要时使用。
- **Perplexity sonar-pro-search**（通过 OpenRouter）：仅用于学术数据库访问至关重要的学术特定论文搜索。

该技能自动检测查询类型并路由到最佳后端。

## 何时使用此技能

在需要时使用此技能：

- **当前研究信息**：最新研究、论文和发现
- **文献验证**：根据当前研究检查事实、统计数据或主张
- **背景研究**：收集科学写作的背景和支持证据
- **引文来源**：查找相关论文和研究以引用
- **技术文档**：查找规范、协议或方法学
- **市场/行业数据**：当前统计数据、趋势、竞争情报
- **近期发展**：新兴趋势、突破、公告

## 科学图表的视觉增强

* *使用此技能创建文档时，请始终考虑添加科学图表和图表以增强视觉传达。**

如果您的文档尚未包含原理图或图表：
- 使用 **scientific-schematics** 技能生成人工智能驱动的出版物质量图表
- 用自然语言简单描述您想要的图表

```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

- --

## 自动后端选择

该技能自动将查询路由到基于内容的最佳后端：

### 路由逻辑

```
Query arrives
    |
    +-- Contains academic keywords? (papers, DOI, journal, peer-reviewed, etc.)
    |       YES --> Perplexity sonar-pro-search (academic search mode)
    |
    +-- Needs deep multi-source synthesis? (user says "deep research", "exhaustive")
    |       YES --> Parallel Chat API (core model, 60s-5min)
    |
    +-- Everything else (general research, market data, technical info, analysis)
            --> parallel-cli search (fast, default)
```

### 默认：并行cli搜索（parallel-web技能）

* *所有标准研究查询的主要后端。**快速、经济高效，并支持学术源优先级排序。

用于科学/技术查询，运行两次搜索以确保学术覆盖：

```bash
# 1. Academic-focused search
parallel-cli search "your research query" -q "keyword1" -q "keyword2" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,semanticscholar.org,biorxiv.org,medrxiv.org,ncbi.nlm.nih.gov,nature.com,science.org,ieee.org,acm.org,springer.com,wiley.com,cell.com,pnas.org,nih.gov" \
  -o sources/research_<topic>-academic.json

# 2. General search (catches non-academic sources)
parallel-cli search "your research query" -q "keyword1" -q "keyword2" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_<topic>-general.json
```

选项：
- `--after-date YYYY-MM-DD`用于时间敏感的查询
- `--include-domains domain1.com,domain2.com`限制特定来源

合并结果，以学术来源为主导。对于非科学查询，单个常规搜索就足够了。

所有其他查询默认路由至此处，包括：

- 一般研究问题
- 市场和行业分析
- 技术信息和文档
- 当前事件和最新动态
- 比较分析
- 统计数据检索
- 事实检查和验证

### 学术关键词（通往 Perplexity 的路径）

包含这些术语的查询将被路由至 Perplexity 以进行学术搜索：

- 论文查找：`find papers`、`find articles`、`research papers on`、 `published studies`
- 引用：`cite`、`citation`、`doi`、`pubmed`、`pmid`
- 学术来源：`peer-reviewed`、`journal article`、 `scholarly`、`arxiv`、`preprint`
- 审阅类型：`systematic review`、`meta-analysis`、`literature search`
- 纸张质量：`foundational papers`、`seminal papers`、 `landmark papers`、`highly cited`

### 深入研究（并行聊天API的路由）

仅当用户明确要求进行深入、详尽或全面的研究时才使用。比并行 cli 搜索慢得多，成本更高。

### 手动覆盖

您可以强制使用特定后端：

```bash
# Force parallel-cli search (fast web search)
parallel-cli search "your query" -q "keyword" --json --max-results 10 -o sources/research_<topic>.json

# Force Parallel Deep Research (slow, exhaustive)
python research_lookup.py "your query" --force-backend parallel

# Force Perplexity academic search
python research_lookup.py "your query" --force-backend perplexity
```

- --

## 核心功能

### 1. 一般研究查询（并行 cli 搜索 —默认）

* *主要后端。**通过 parallel-web 技能进行快速、经济高效的网络搜索，并具有学术来源优先级。

```
Query Examples:
- "Recent advances in CRISPR gene editing 2025"
- "Compare mRNA vaccines vs traditional vaccines for cancer treatment"
- "AI adoption in healthcare industry statistics"
- "Global renewable energy market trends and projections"
- "Explain the mechanism underlying gut microbiome and depression"
```

```bash
# Example: research on CRISPR advances
parallel-cli search "Recent advances in CRISPR gene editing 2025" \
  -q "CRISPR" -q "gene editing" -q "2025" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,nature.com,science.org,cell.com,pnas.org,nih.gov" \
  -o sources/research_crispr_advances-academic.json

parallel-cli search "Recent advances in CRISPR gene editing 2025" \
  -q "CRISPR" -q "gene editing" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_crispr_advances-general.json
```

* *响应包括：**
- 通过搜索内联引用综合发现的结果结果
- 按优先顺序排列的学术来源（同行评审、预印本）
- 具体事实、数字和日期
- 列出按类型分组的所有引用 URL 的来源部分

### 2. 学术论文搜索（Perplexity sonar-pro-search）

* *用于特定于学术的查询。** 优先级学术数据库和同行评审的来源。当查询专门询问论文、引文或 DOIs 时使用。

```
Query Examples:
- "Find papers on transformer attention mechanisms in NeurIPS 2024"
- "Foundational papers on quantum error correction"
- "Systematic review of immunotherapy in non-small cell lung cancer"
- "Cite the original BERT paper and its most influential follow-ups"
- "Published studies on CRISPR off-target effects in clinical trials"
```

* *响应包括：**
- 学术文献的主要发现摘要
- 5-8 个高质量引文，包括作者、标题、期刊、年份、DOIs
- 引文计数和地点等级指标
- 关键统计数据和方法亮点
- 研究差距和未来方向

### 3.深度研究（并行聊天API - 仅根据请求）

* *仅当用户明确请求深入/详尽的研究时使用。**通过聊天API（`core`模型）提供全面的多源综合。 60s-5min 延迟。

```
Query Examples:
- "Deep research on the current state of quantum computing error correction"
- "Exhaustive analysis of mRNA vaccine platforms for cancer immunotherapy"
```

### 4. 技术和方法信息

使用并行-cli 搜索（默认）进行快速查找：

```bash
parallel-cli search "Western blot protocol for protein detection" \
  -q "western blot" -q "protocol" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_western_blot.json
```

### 5. 统计和市场数据

使用Parallel-cli 搜索（默认）当前数据：

```bash
parallel-cli search "Global AI market size and growth projections 2025" \
  -q "AI market" -q "statistics" -q "growth" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --after-date 2024-01-01 \
  -o sources/research_ai_market.json
```

- --

## 纸张质量和受欢迎程度优先 

* *关键**：搜索论文时，始终优先考虑高质量、有影响力的论文。

### 基于引文的排名

|纸时代|引用阈值 |分类|
|---------|--------------------------------|----------------|
| 0-3岁| 20+ 次引用 |值得注意|
| 0-3岁| 100 多次引用 |极具影响力|
| 3-7年| 100 多次引用 |重要|
| 3-7年| 500 多次引用 |地标纸|
| 7 年以上 | 500 多次引用 |开创性工作|
| 7 年以上 | 1000+ 次引用 |基础 |

### 场地质量等级

* *1 级 - 顶级场地**（始终首选）：
- **普通科学**：自然、科学、细胞、PNAS
- **医学**：NEJM、柳叶刀、JAMA、BMJ
- **特定领域**：自然医学、自然生物技术、自然方法
- **顶级 CS/AI**：NeurIPS、ICML、ICLR、ACL、CVPR

* *2 级 - 高影响力专业**（强烈偏好）：
- 影响因子 > 10 的期刊
- 子领域的顶级会议（EMNLP、NAACL、ECCV、 MICCAI)

* *Tier 3 - 受尊重的专业**（相关时包含）：
- 影响因子为 5-10 的期刊

- --

## 技术集成

### 先决条件

```bash
# Primary backend (parallel-cli) - REQUIRED
# Install parallel-cli if not already available:
curl -fsSL https://parallel.ai/install.sh | bash
# Or: uv tool install "parallel-web-tools[cli]"

# Authenticate:
parallel-cli auth
# Or: export PARALLEL_API_KEY="your_parallel_api_key"
```

### 环境变量

```bash
# Primary backend (parallel-cli search) - REQUIRED
export PARALLEL_API_KEY="your_parallel_api_key"

# Deep research backend (Parallel Chat API) - optional, for deep research only
# Uses the same PARALLEL_API_KEY

# Academic search backend (Perplexity) - optional, for academic paper queries
export OPENROUTER_API_KEY="your_openrouter_api_key"
```

### API 规范

* *parallel-cli 搜索（主）：**
- 命令：`parallel-cli search` 和 `--json` 输出
- 延迟：2-10 秒（快速）
- 输出：带有标题、URL、发布日期、摘录的 JSON
- 学术领域：使用 `--include-domains` 获取学术资源
- 保存结果：`-o filename.json` 用于后续和可重复性

* *并行聊天 API（仅限深入研究）：**
- 端点：`https://api.parallel.ai`（兼容 OpenAI SDK）
- 模型：`core`（60s-5 分钟延迟，复杂的多源合成）
- 输出：带有内联引用的 Markdown 文本
- 引用：URL 的研究基础，推理和置信度
- 速率限制：300 req/min
- Python 包：`openai`

* *困惑声纳专业搜索（仅限学术）：**
- 型号：`perplexity/sonar-pro-search`（通过 OpenRouter）
- 搜索模式：学术（优先考虑同行评审的来源）
- 搜索上下文：高（综合研究）
- 响应时间：5-15 秒

### 命令行用法

```bash
# Fast web search via parallel-cli (DEFAULT — recommended) — ALWAYS save to sources/
parallel-cli search "your query" -q "keyword1" -q "keyword2" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_<topic>.json

# Academic-focused search via parallel-cli — ALWAYS save to sources/
parallel-cli search "your query" -q "keyword1" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,semanticscholar.org,biorxiv.org,medrxiv.org,nature.com,science.org,cell.com,pnas.org,nih.gov" \
  -o sources/research_<topic>-academic.json

# Time-sensitive search via parallel-cli
parallel-cli search "your query" -q "keyword" \
  --json --max-results 10 --after-date 2024-01-01 \
  -o sources/research_<topic>.json

# Extract full content from a specific URL (use parallel-web extract)
parallel-cli extract "https://example.com/paper" --json

# Force Parallel Deep Research (slow, exhaustive) — via research_lookup.py
python research_lookup.py "your query" --force-backend parallel -o sources/research_<topic>.md

# Force Perplexity academic search — via research_lookup.py
python research_lookup.py "your query" --force-backend perplexity -o sources/papers_<topic>.md

# Auto-routed via research_lookup.py (legacy) — ALWAYS save to sources/
python research_lookup.py "your query" -o sources/research_YYYYMMDD_HHMMSS_<topic>.md

# Batch queries via research_lookup.py — ALWAYS save to sources/
python research_lookup.py --batch "query 1" "query 2" "query 3" -o sources/batch_research_<topic>.md
```

- --

## 强制：将所有结果保存到来源文件夹

* *每个research-lookup结果必须保存到项目的`sources/`文件夹中。**

这是不可协商的。研究结果的获取成本高昂，且对重现性至关重要。

### 保存规则

|后端| `-o` 标志目标 |文件名模式 |
|---------|------------------|------------------|
|并行 cli 搜索（默认）| `sources/research_<topic>.json` | `research_<brief_topic>.json` 或 `research_<brief_topic>-academic.json` |
|并行深度研究| `sources/research_<topic>.md` | `research_YYYYMMDD_HHMMSS_<brief_topic>.md` |
|困惑（学术）| `sources/papers_<topic>.md` | `papers_YYYYMMDD_HHMMSS_<brief_topic>.md` |
|批量查询 | `sources/batch_<topic>.md` | `batch_research_YYYYMMDD_HHMMSS_<brief_topic>.md` |

### 如何保存

* *关键：每次搜索都必须使用 `-o` 标志将结果保存到 `sources/` 文件夹。**

* *关键：保存的文件必须保留所有引文、源 URL 和DOI。**

```bash
# parallel-cli search (DEFAULT) — save JSON to sources/
parallel-cli search "Recent advances in CRISPR gene editing 2025" \
  -q "CRISPR" -q "gene editing" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,nature.com,science.org,cell.com,pnas.org,nih.gov" \
  -o sources/research_crispr_advances-academic.json

parallel-cli search "Recent advances in CRISPR gene editing 2025" \
  -q "CRISPR" -q "gene editing" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_crispr_advances-general.json

# Academic paper search via Perplexity — save to sources/
python research_lookup.py "Find papers on transformer attention mechanisms in NeurIPS 2024" \
  -o sources/papers_20250217_143500_transformer_attention.md

# Deep research via Parallel Chat API — save to sources/
python research_lookup.py "AI regulation landscape" --force-backend parallel \
  -o sources/research_20250217_144000_ai_regulation.md

# Batch queries — save to sources/
python research_lookup.py --batch "mRNA vaccines efficacy" "mRNA vaccines safety" \
  -o sources/batch_research_20250217_144500_mrna_vaccines.md
```

### 已保存文件中的引文保留

Each 输出格式以不同方式保留引文：

|格式|包含引文 |何时使用 |
|--------------------|--------------------|-------------|
|并行-cli JSON（默认）|完整结果对象：`title`、`url`、`publish_date`、`excerpts` |标准使用 - 结构化、可解析、快速 |
|文本（research_lookup.py）| `Sources (N):` 部分，包含 `[title] (date) + URL` + `Additional References (N):` 以及 DOI 和学术 URL |深入研究/困惑​​——人类可读 |
| JSON（`--json` 通过 Research_lookup.py）|完整引用对象：`url`、`title`、`date`、`snippet`、`doi`、`type` |当您需要来自深入研究的最大引文元数据 |

* *对于并行 CLI 搜索**，保存的 JSON 文件包括：完整搜索结果，包含标题、URL、发布日期和每个结果的内容摘录。
* *对于并行聊天 API 后端**，保存的文件包括：研究报告 + 来源列表（标题、URL）+其他参考文献（DOI、学术 URL）。
* *对于 Perplexity 后端**，保存的文件包括：学术摘要 + 来源列表（标题、日期、URL、片段）+ 其他参考文献（DOI、学术 URL）。

* *在需要时使用 `--json`：**
- 以编程方式解析引文元数据
- 为 BibTeX 生成保留完整的 DOI 和 URL 数据
- 维护结构化引文对象交叉引用

### 为什么要保存所有内容

1. **再现性**：每一次引用和声明都可以追溯到其原始研究来源
2. **上下文窗口恢复**：如果上下文被压缩，则可以重新读取保存的结果，而无需重新查询
3. **审计跟踪**：`sources/` 文件夹准确记录了所有研究信息的收集方式
4. **跨部分重用**：多个部分可以引用相同的已保存研究，而无需重复查询
5. **成本效率**：在进行新的 API 调用之前检查 `sources/` 的现有结果
6. **同行评审支持**：审稿人可以验证支持每个引文的研究

### 在进行新查询之前，首先检查来源

在调用`research_lookup.py`之前，检查相关结果是否已存在：

```bash
ls sources/  # Check existing saved results
```

如果之前的查找涵盖相同的主题，请重新读取保存的文件而不是创建新的文件API调用。

### 记录

保存研究结果时，始终记录：

```
[HH:MM:SS] SAVED: Research lookup to sources/research_20250217_143000_crispr_advances.md (3,800 words, 8 citations)
[HH:MM:SS] SAVED: Paper search to sources/papers_20250217_143500_transformer_attention.md (6 papers found)
```

- --

## 与科学写作集成

此技能通过提供：

1来增强科学写作。 **文献综述支持**：收集当前研究以进行介绍和讨论 - **保存到 `sources/`**
2. **方法验证**：根据当前标准验证协议 — **保存到 `sources/`**
3. **结果情境化**：将结果与最近的类似研究进行比较 - **保存到 `sources/`**
4. **讨论增强**：用最新证据支持论点 - **保存到 `sources/`**
5. **引文管理**：提供格式正确的引文 — **保存到 `sources/`**

## 补充工具

|任务|工具 |
|------|------|
|一般网络搜索（快速）| `parallel-cli search`（内置此技能）|
|以学术为中心的网络搜索 | `parallel-cli search --include-domains`（内置于该技能中）|
| URL内容提取 | `parallel-cli extract`（parallel-web技能）|
|深入研究（详尽）| `research-lookup` 通过并行聊天 API 或 `parallel-web` 深入研究 |
|学术论文检索 | `research-lookup`（自动路由到 Perplexity）|
|谷歌学术搜索 | `citation-management`技能|
|考研搜索 | `citation-management`技能|
| DOI 到 BibTeX | `citation-management`技能|
|元数据验证 | `parallel-cli extract`（parallel-web技能）|

- --

## 错误处理和限制

* *已知限制：**
- parallel-cli搜索：需要安装并验证`parallel-cli`
- 并行聊天API（核心模型）：复杂查询可能需要长达 5 分钟
- 困惑：信息被切断，可能无法访问付费墙后面的全文
- 所有后端：无法访问专有或受限数据库

* *后备行为：**
- 如果未找到 `parallel-cli`，请使用 `curl -fsSL https://parallel.ai/install.sh | bash` 或`uv tool install "parallel-web-tools[cli]"`
- 如果并行 cli 搜索返回的结果不足，则回退到 Perplexity 或并行聊天 API
- 如果所选后端的 API 密钥丢失，则尝试其他后端
- 如果所有后端都失败，则返回结构化错误响应
- 如果初始响应为，则重新表述查询以获得更好的结果不足

- --

## 使用示例

### 示例1：一般研究（并行cli搜索的路由）

* *查询**：“变压器注意机制2025的最新进展”

* *后端**：并行cli搜索（默认，快速）

* *命令**：
```bash
parallel-cli search "Recent advances in transformer attention mechanisms 2025" \
  -q "transformer" -q "attention" -q "2025" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "arxiv.org,semanticscholar.org,nature.com,science.org,ieee.org,acm.org" \
  -o sources/research_transformer_attention-academic.json

parallel-cli search "Recent advances in transformer attention mechanisms 2025" \
  -q "transformer" -q "attention" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/research_transformer_attention-general.json
```

* *响应**：通过学术和一般来源的内联引用综合发现，涵盖最近的论文、关键创新和性能基准。

### 示例 2：学术论文搜索（通往 Perplexity 的路径）

* *查询**：“查找有关临床试验中 CRISPR 脱靶效应的论文”

* *后端**：Perplexity 声纳专业搜索（学术模式）

* *响应**：精心策划的 5-8 篇高影响力论文列表，其中包含完整的引用、DOI、引用计数和场地等级

### 示例 3：比较分析（并行 cli 搜索的路径）

* *查询**：“比较和对比 mRNA 疫苗与用于癌症治疗的传统疫苗”

* *后端**：并行 cli 搜索（默认，快速）

* *响应**：通过内联引用、结构化分析和证据质量从多个网络来源进行综合比较

### 示例 4：市场数据（并行 cli 搜索的路由）

* *查询**：“2025 年医疗统计中的全球人工智能采用”

* *后端**：并行 cli 搜索（默认，快速）

```bash
parallel-cli search "Global AI adoption in healthcare statistics 2025" \
  -q "AI healthcare" -q "adoption statistics" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --after-date 2024-01-01 \
  -o sources/research_ai_healthcare_adoption.json
```

* *响应**：当前市场数据、采用率、增长预测， 

- --

## 摘要

此技能作为智能三后端路由的主要研究界面：

- **并行-cli搜索**（默认）：通过 parallel-web 技能进行快速、经济有效的网络搜索，并进行学术来源优先排序
- **并行聊天API**（`core` 模型）：深入、详尽的多源综合（仅在明确请求时）
- **困惑声纳专业搜索**：仅学术特定论文搜索
- **自动路由**：检测查询类型并路由到最佳后端
- **手动覆盖**：需要时强制任何后端
- **学术优先级**：两种搜索模式确保科学查询的学术来源表面
