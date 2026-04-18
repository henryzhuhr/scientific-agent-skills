# Unpaywall API

Unpaywall 告诉您学术文章是否存在合法、免费的副本。给定 DOI，它会返回开放访问状态、PDF 链接和位置详细信息。

## 基本 URL

```
https://api.unpaywall.org/v2
```

## 身份验证

No API 密钥。您必须包含您的**电子邮件地址**作为查询参数：`?email=you@example.com`

* *重要：**使用真实的电子邮件地址。 Unpaywall 拒绝占位符电子邮件，如带有 HTTP 422.

## 的占位符电子邮件 `test@example.com`## 速率限制

每天 100,000 次调用。如需更频繁的使用，请下载数据库快照。

## 关键端点

### 1. DOI 查找

```
GET /v2/{doi}?email=you@example.com
```

* *示例：**
```
https://api.unpaywall.org/v2/10.1038/nature12373?email=you@example.com
```

### 2. 搜索（不可靠）

```
GET /v2/search?query={text}&email=you@example.com
```

* *警告：** 截至 2026 年 3 月，搜索端点已返回 HTTP 500 错误。它可能已弃用或间歇性损坏。使用 DOI 查找——首先通过 PubMed/OpenAlex/Semantic Sc​​holar 查找论文，然后检查每个 DOI 的 OA 状态。

|参数|描述|
|---------|--------------|
| `query` |搜索文本。支持引用短语、`OR`、`-` 否定 |
| `is_oa` | `true` 或 `false` -- 按 OA 状态过滤 |
| `page` |页码（1 索引），每页 50 个结果 |

## 响应格式

### DOI 查找响应
```json
{
  "doi": "10.1038/nature12373",
  "doi_url": "https://doi.org/10.1038/nature12373",
  "title": "Nanometre-scale thermometry in a living cell",
  "year": 2013,
  "published_date": "2013-07-31",
  "genre": "journal-article",
  "publisher": "Springer Nature",
  "is_oa": true,
  "oa_status": "green",
  "best_oa_location": {
    "url": "https://dash.harvard.edu/bitstream/1/...",
    "url_for_pdf": "https://dash.harvard.edu/bitstream/1/...pdf",
    "url_for_landing_page": "https://dash.harvard.edu/handle/...",
    "host_type": "repository",
    "version": "acceptedVersion",
    "license": "cc-by",
    "is_best": true,
    "oa_date": "2016-01-01"
  },
  "first_oa_location": {...},
  "oa_locations": [...],
  "has_repository_copy": true,
  "journal_name": "Nature",
  "journal_issns": "0028-0836,1476-4687",
  "journal_issn_l": "0028-0836",
  "journal_is_oa": false,
  "journal_is_in_doaj": false,
  "z_authors": [
    {"raw_author_name": "G. Kucsko", "author_position": "first"},
    {"raw_author_name": "P. C. Maurer", "author_position": "middle"}
  ]
}
```

### OA 状态值
|状态 |含义 |
|--------|---------|
| `gold` |发表于完全OA期刊|
| `hybrid` |订阅期刊中的 OA（出版商托管）|
| `bronze` |在出版商网站上免费阅读，但没有 OA 许可证 |
| `green` |可通过存储库（例如机构、预印本）|
| 获取`closed` |找不到免费的正版副本 |

### OA 位置字段
|领域 |描述 |
|-------|--------------|
| `url` |最佳 URL（PDF 如果可用，否则登录页面）|
| `url_for_pdf` |直接 PDF URL（如果没有 PDF，则为 null）|
| `url_for_landing_page` |登陆页面网址|
| `host_type` | `publisher` 或 `repository` |
| `version` | `submittedVersion`、`acceptedVersion`、`publishedVersion` |
| `license` |例如，`cc-by`、`cc-by-nc`、`implied-oa` 或 null |
| `is_best` |这是否是`best_oa_location`|
| `oa_date` |当首次在此位置可用时|

### 搜索响应
```json
{
  "results": [
    {
      "response": {...},
      "score": 42.5,
      "snippet": "...text with <b>highlighted</b> matches..."
    }
  ]
}
```

## 典型工作流程

1. 您有来自 PubMed、Crossref 或其他来源的 DOI 
2. 使用 DOI
3 致电 Unpaywall。检查 `is_oa` - 如果为 true，则使用 `best_oa_location.url_for_pdf` 获取免费 PDF
4. 检查`oa_status`了解它是什么类型的OA
5. 如果关闭，`oa_locations`将为空——文章需要订阅
