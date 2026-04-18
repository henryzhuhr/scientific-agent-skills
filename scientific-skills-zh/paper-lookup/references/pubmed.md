# PubMed（NCBI 电子实用程序）

PubMed 提供 3700 万多篇生物医学和生命科学文章的引文、摘要和元数据。它不包含全文 - 为此，请使用 PMC.

## Base URL

```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

## Authentication

- **API 密钥可选** 但推荐。没有：3 请求/秒。包含：10 个请求/秒。
- 传递为：`&api_key=YOUR_KEY`
- 在所有请求中还包括 `&tool=your_app_name&email=your@email.com`。

## 关键端点

### 1. eSearch -- 搜索并获取 PMIDs

```
GET /esearch.fcgi?db=pubmed&term={query}&retmode=json
```

|参数|必填 |默认|描述 |
|---------|---------|---------|-------------|
| `db` |是的 | --| `pubmed` |
| `term` |是的 | --|搜索查询。支持 PubMed 语法：字段标签 `[AU]`、`[TI]`、`[TA]`、`[MH]` (MeSH)、布尔 AND/OR/NOT |
| `retmax` |没有 | 20 |返回的最大 PMID（最大 10,000）|
| `retstart` |没有 | 0 |分页偏移|
| `retmode` |没有 | `xml` | `json` 或 `xml` |
| `rettype` |没有 | `uilist` | `uilist`（ID）或`count`（仅计数）|
| `sort` |没有 | `relevance` | `relevance`、`pub_date`、`Author`、`JournalName` |
| `datetype` |没有 | --| `pdat`（发布）、`mdat`（修改）、`edat`（entrez）|
| `mindate` / `maxdate` |没有 | --|日期范围 `YYYY/MM/DD` |
| `reldate` |没有 | --|过去 N 天的商品 |
| `usehistory` |没有 | --| `y` 存储在历史记录服务器上以获取大型结果集 |

* *示例：**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=CRISPR+gene+therapy&retmode=json&retmax=5&sort=pub_date
```

* *响应：**
```json
{
  "esearchresult": {
    "count": "224107",
    "retmax": "5",
    "retstart": "0",
    "idlist": ["39984857", "39984678", "39984543", "39984210", "39983901"]
  }
}
```

### 2. eSummary -- 获取文档摘要

```
GET /esummary.fcgi?db=pubmed&id={pmids}&retmode=json
```

|参数|必填 |描述 |
|-----------|---------|------------|
| `db` |是的 | `pubmed` |
| `id` |是的 |以逗号分隔的 PMID（最多 10,000）|
| `retmode` |没有 | `json` 或 `xml` |

* *示例：**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=39984857,39984678&retmode=json
```

* *响应字段：** `uid`、`pubdate`、`source`（期刊）、`authors`、 `title`、`volume`、`issue`、`pages`、`fulljournalname`、`elocationid`（DOI）、`articleids`（PMC、DOI等）、`pubtype`、 `pmcrefcount`

### 3. eFetch -- 检索完整记录（摘要、MEDLINE）

```
GET /efetch.fcgi?db=pubmed&id={pmids}&rettype={type}&retmode={mode}
```

|重新输入 |旋转模式 |返回 |
|---------|---------|---------|
| *（省略）* | `xml` |完整的 PubMed XML（引文 + 摘要）|
| `medline` | `text` | MEDLINE 格式 |
| `abstract` | `text` |纯文本摘要|
| `uilist` | `text` | PMID 列表 |

* *示例 -- 获取 XML 形式的摘要：**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=39984857&retmode=xml
```

XML 包含 `<PubmedArticle>` 和 `<MedlineCitation>`（标题、摘要、MeSH 术语、作者）和 `<PubmedData>`（文章 ID、出版物）历史）。

### 4. eLink -- 查找相关文章

```
GET /elink.fcgi?dbfrom=pubmed&db=pubmed&id={pmid}&cmd=neighbor_score&retmode=json
```

返回具有相关性分数的相关 PMID。

## 搜索语法提示

- **字段标签：** `aspirin[TI]`（标题）、`Smith J[AU]`（作者）、 `Nature[TA]`（期刊）、`neoplasms[MH]`（MeSH 标题）
- **布尔值：** `CRISPR AND (therapy OR treatment)`
- **日期范围：** `2020/01/01:2024/12/31[PDAT]`
- **出版物类型：** `review[PT]`， `clinical trial[PT]`
- **生物：** `humans[MH]`、`mice[MH]`

## 速率限制

- **3 个请求/秒** 无 API 密钥
- **10 个请求/秒** 有 API 密钥
- 包括每个请求上的 `tool` 和 `email` 参数
- 大型批量作业应在高峰时间之外运行（周一至周五上午 5 点至晚上 9 点（美国东部时间））

## 错误格式

```json
{"error": "API rate limit exceeded", "count": "11"}
```

HTTP 400 表示错误请求，429 表示速率限制。
