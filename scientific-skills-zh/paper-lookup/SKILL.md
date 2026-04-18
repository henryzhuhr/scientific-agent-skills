---
name: paper-lookup
description: 通过 REST API 搜索 10 个学术论文数据库，查找研究论文、预印本和学术文章。涵盖 PubMed、PMC（全文）、bioRxiv、medRxiv、arXiv、OpenAlex、Crossref、Semantic Sc​​holar、CORE、Unpaywall。在搜索论文、引文、DOI/PMID 查找、摘要、全文、开放获取、预印本、引文图、作者搜索或任何学术文献查询时使用。在提及任何受支持的数据库或请求（例如“在 X 上查找论文”或“查找此 DOI”）时触发。
metadata:
  skill-author: K-Dense Inc.
---

# 论文查找

您可以通过其 REST API 访问 10 个学术论文数据库。您的工作是找出哪个数据库最适合用户的查询，调用它们并返回结果。

## 核心工作流程

1. **理解查询** -- 用户在寻找什么？ DOI 的具体论文？关于某个主题的论文？作者的出版物？开放获取 PDF？全文？这决定了要命中哪个数据库。

2. **选择数据库** -- 使用下面的数据库选择指南。许多查询受益于访问多个数据库——例如，在 PubMed 中搜索论文，然后检查 Unpaywall 中的开放获取副本。

3. **阅读参考文件** -- 每个数据库在 `references/` 中都有一个参考文件，其中包含端点详细信息、查询格式和示例调用。在进行 API 调用之前，请阅读相关文件。

4. **进行 API 调用** -- 请参阅下面的 **进行 API 调用** 部分，了解要在您的平台上使用哪个 HTTP 获取工具。

5. **返回结果** -- 始终返回：
  - 来自每个数据库的 **原始 JSON**（或为 arXiv 解析的 XML）响应
  - 使用特定端点查询的**数据库列表**
  - 如果查询未返回结果，请明确说明而不是省略它

## 数据库选择指南

匹配用户的意图到正确的数据库。

### 按用例

|用户询问... |主数据库 |还要考虑 |
|---|---|---|
|关于生物医学主题的论文|考研|语义学者，OpenAlex |
|生物医学文章全文 |管理委员会|核心|
|生物学预印本|生物Rxiv |语义学者，OpenAlex |
|健康/医学预印本 | medRxiv |语义学者，OpenAlex |
|物理、数学或计算机科学预印本 | arXiv |语义学者，OpenAlex |
|各领域论文 |开放亚历克斯 |语义学者，Crossref |
| DOI 的一篇具体论文 |交叉参考 | Unpaywall，语义学者|
|开放获取 PDF 论文 |取消付费墙 |核心，PMC |
|引用图（谁引用了谁）|语义学者| OpenAlex |
|作者的出版物 |语义学者| OpenAlex |
|论文推荐|语义学者| -- |
|全文（任何字段）|核心| PMC（仅限生物医学）|
|期刊/出版商元数据 |交叉参考 | OpenAlex |
|资助者信息 |交叉参考 | OpenAlex |
| PMID/PMCID/DOI 之间的转换 | PMC（ID转换器）|交叉参考|
|按日期列出的最近预印本 | BioRxiv、medRxiv | arXiv |

### 跨数据库查询

|用户询问... |要查询的数据库|
|---|---|
|关于论文的一切（元数据+引文+OA）| Crossref + 语义学者 + Unpaywall |
|综合文献检索| PubMed + OpenAlex + 语义学者 |
|查找并阅读论文 | PubMed（查找）+ Unpaywall（OA 链接）+ PMC 或 CORE（全文）|
|预印本及其出版版本 | bioRxiv/medRxiv + Crossref |
|带有引用指标的作者概述 | Semantic Sc​​holar + OpenAlex |

当查询跨越多个需求时（例如，“查找有关 CRISPR 的论文并获取 PDF”），并行查询相关数据库。

## 通用标识符格式

不同的数据库使用不同的标识符系统。如果查询失败，可能是标识符格式错误。

|标识符 |格式|示例|由 |
|---|---|---|---|
| 使用DOI | `10.xxxx/xxxxx` | `10.1038/nature12373` |所有数据库|
| PMID |整数 | `34567890` | PubMed、PMC、语义学者 |
| PMCID | `PMC` + 数字 | `PMC7029759` | PMC，欧洲 PMC |
| arXiv ID | `YYMM.NNNNN` | `2103.15348` | arXiv，语义学者 |
|开放亚历克斯 ID | `W` + 数字 | `W2741809807` | OpenAlex |
|语义学者 ID | 40 个字符的十六进制 | `649def34f8be...` |语义学者|
|奥西德 | `0000-XXXX-XXXX-XXXX` | `0000-0001-6187-6610` | OpenAlex，交叉参考|
|国际标准刊号 | `XXXX-XXXX` | `0028-0836` | Crossref、OpenAlex |

* *交叉引用 ID：** Semantic Sc​​holar 通过前缀接受 DOI、PMID、PMCID 和 arXiv ID（例如，`DOI:10.1038/nature12373`、`PMID:34567890`、`ARXIV:2103.15348`）。 OpenAlex 通过前缀（`doi:10.1038/...`、`pmid:34567890`）接受 DOI 和 PMID。使用 PMC ID 转换器在 PMID、PMCID 和 DOI 之间进行转换。

## API 密钥和 Access

这些数据库大多数都是完全开放的。一些数据库受益于 API 密钥以获得更高的速率限制。

### 需要或受益于 API 密钥的数据库

|数据库|环境变量 |必需的？ |注册 |
|---|---|---|---|
| NCBI（PubMed、PMC）| `NCBI_API_KEY` |否（没有时 3 个请求/秒，有时 10 个请求/秒）| https://www.ncbi.nlm.nih.gov/account/settings/ |
|核心| `CORE_API_KEY` |是的全文 | https://core.ac.uk/services/api |
|语义学者| `S2_API_KEY` |否（无共享池）| https://www.semanticscholar.org/product/api#api-key-form |
|开放亚历克斯 | `OPENALEX_API_KEY` |推荐| https://openalex.org/settings/api |

### 完全开放数据库（无需密钥）

|数据库|备注|
|---|---|
|生物Rxiv / medRxiv |没有身份验证，没有记录的速率限制 |
| arXiv |无身份验证，每 3 秒最多 1 个请求 |
|交叉参考 |没有授权；为礼貌池添加 `mailto` 参数（2x 速率限制）|
|取消付费墙 |没有授权；需要 `email` 参数 |

### 加载 API 密钥

1. **首先检查环境** -- 密钥可能已导出（例如，`$NCBI_API_KEY`）.
2. **回退到`.env`** -- 检查当前工作目录中的`.env`。
3. **不继续**——大多数 API 仍然以较低的速率限制运行。告诉用户缺少哪个密钥以及如何获取它。

## 进行 API 调用

使用您环境的 HTTP 获取工具来调用 REST 端点：

|平台| HTTP 获取工具 |后备 |
|---|---|---|
|克劳德·代码 | `WebFetch` | `curl` 通过 Bash |
|双子座 CLI | `web_fetch` | `curl`过壳|
|风帆冲浪 | `read_url_content` | `curl` 通过终端|
|光标|没有专用的抓取工具| `curl` 通过 `run_terminal_cmd` |
|法典 CLI |没有专用的抓取工具| `curl` 通过 `shell` |
|克莱恩 |没有专用的抓取工具| `curl` via `execute_command` |

如果获取工具失败，请通过任何可用的 shell 工具回退到 `curl`。

### 特殊情况

- **arXiv 返回 Atom XML**，而不是 JSON。解析它或使用`curl`并提取相关字段。如果可用，请考虑通过简单的解析器进行管道传输。
- **PMC eFetch 返回 JATS XML** 以获得全文。这是预期的 - 全文文章采用 XML 格式。
- **Crossref 和 Unpaywall** 受益于包含用于礼貌/快速池的 `mailto` 参数或电子邮件。

### 请求指南

- 对于 **NCBI API**（PubMed、PMC）：无密钥时最多 3 个请求/秒，有密钥时 10 个请求/秒。按顺序发出请求。
- 对于 **arXiv**：每 3 秒最多 1 个请求。请耐心等待。
- 对于 **Crossref**：5 请求/秒（公共），10 请求/秒（与 `mailto` 礼貌池）。
- 对于没有严格限制的其他 API，您可以并行查询多个数据库。
- 如果收到 HTTP 429（速率限制），请稍等一下并重试一次。

### 错误恢复

1. **检查标识符格式** - 使用通用标识符格式表。 PMID 无法在 arXiv 中使用，arXiv ID 无法直接在 PubMed 中使用。
2. **尝试替代标识符** - 如果 DOI 在一个数据库中失败，请尝试使用标题或 PMID。
3. **尝试不同的数据库** - 如果 PubMed 没有返回任何 CS 论文，请尝试 Semantic Sc​​holar 或 OpenAlex.
4. **报告失败** -- 告诉用户哪个数据库失败、错误以及您尝试了什么。

## 输出格式

像这样构建您的响应：

```
## Databases Queried
- **PubMed** -- esearch + esummary for "CRISPR gene therapy"
- **Unpaywall** -- DOI lookup for 10.1038/...

## Results

### PubMed
[raw JSON response or formatted results]

### Unpaywall
[raw JSON response]
```

如果结果非常大，请呈现最相关的部分，并注意有更多数据可用。但默认显示完整的原始 JSON —— 用户要求它。

## 可用数据库

在进行任何 API 调用之前阅读相关参考文件。

### 生物医学文献
|数据库|参考文件|涵盖内容|
|---|---|---|
|考研| `references/pubmed.md` | 37M+ 生物医学引文、摘要、MeSH 术语 |
|管理委员会| `references/pmc.md` | 10M+全文生物医学文章（JATS XML），ID转换|

### 预印本服务器
|数据库|参考文件|涵盖内容 |
|---|---|---|
|生物Rxiv | `references/biorxiv.md` |生物学预印本（按日期/DOI 浏览，无关键字搜索）|
| medRxiv | `references/medrxiv.md` |健康科学预印本（按日期/DOI 浏览，无关键字搜索）|
| arXiv | `references/arxiv.md` |物理、数学、CS、生物学、经济学预印本（关键字搜索、Atom XML）|

### 多学科索引
|数据库|参考文件|涵盖内容 |
|---|---|---|
|开放亚历克斯 | `references/openalex.md` | 2.5亿+作品、作者、机构、主题、引文数据|
|交叉参考 | `references/crossref.md` | 1.5 亿+ DOI 元数据、期刊、资助者、参考文献 |
|语义学者| `references/semantic-scholar.md` | 2 亿多篇论文、引文图、AI 生成的 TLDR、建议 |

### 开放获取和全文
|数据库|参考文件|涵盖内容 |
|---|---|---|
|核心| `references/core.md` |来自全球 OA 存储库的超过 3700 万篇全文 |
|取消付费墙 | `references/unpaywall.md` |任何 DOI 的 OA 状态和 PDF 链接 |
