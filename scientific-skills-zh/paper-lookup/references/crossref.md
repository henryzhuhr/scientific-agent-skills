# Crossref API

Crossref 是学术内容的 DOI 注册机构。它提供超过 1.5 亿篇作品的元数据，包括期刊文章、书籍、会议论文、数据集和预印本。

## 基本 URL

```
https://api.crossref.org
```

## 身份验证

无需。添加 `mailto=you@example.com` 进入 **礼貌池**（2 倍更快的速率限制）。

## 速率限制

|泳池|评分 |并发 |
|------|------|-------------|
|公开（无邮寄地址）| 5 请求/秒 | 1个并发|
|有礼貌（有mailto）| 10 请求/秒 | 3 个并发 |

HTTP 429 = 暂时阻塞。

## 关键端点

### 1. 搜索作品

```
GET /works?query={text}&rows={n}&mailto=you@example.com
```

|参数|默认|描述 |
|---------|---------|------------|
| `query` | --|跨所有领域的自由文本搜索|
| `query.author` | --|搜索作者姓名|
| `query.bibliographic` | --|搜索标题、作者、ISSN、年份 |
| `query.affiliation` | --|搜索附属机构 |
| `query.container-title` | --|检索期刊名称|
| `filter` | --|逗号分隔的 `name:value` 对 |
| `sort` | `score` | `score`、`published`、`issued`、`deposited`、`updated`、`is-referenced-by-count`、`references-count` |
| `order` | `desc` | `asc` 或 `desc` |
| `rows` | 20 |每页结果（最多 1000）|
| `offset` | 0 |跳过 N 个结果（最多 10,000 个）|
| `cursor` | --|使用 `*` 进行基于游标的深度分页 |
| `select` | --|返回 |
| 的逗号分隔字段名称`facet` | --|面数，例如`type-name:10` |
| `sample` | --|返回 N 个随机项（最多 100 个） |

* *示例：**
```
https://api.crossref.org/works?query=CRISPR+gene+therapy&filter=from-pub-date:2024-01-01,type:journal-article,has-abstract:true&rows=5&sort=published&order=desc&mailto=you@example.com
```

### 2. 通过 DOI

```
GET /works/{doi}?mailto=you@example.com
```

URL 获取工作 - 对 DOI 进行编码：`10.1038/nature12373` 变为`10.1038%2Fnature12373`

* *示例：**
```
https://api.crossref.org/works/10.1038%2Fnature12373?mailto=you@example.com
```

### 3. 期刊

```
GET /journals?query={name}&rows={n}
GET /journals/{issn}
GET /journals/{issn}/works?query={text}&rows={n}
```

### 4. 资助者

```
GET /funders?query={name}
GET /funders/{id}
GET /funders/{id}/works?rows={n}
```

资助者 ID 来自资助者注册表（例如 NSF 的 `100000001`）。

### 5. 成员（发布者）

```
GET /members?query={name}
GET /members/{id}/works?rows={n}
```

## 关键过滤器

### 日期过滤器（接受`YYYY`、`YYYY-MM`、`YYYY-MM-DD`)
|过滤|描述 |
|--------|-------------|
| `from-pub-date` / `until-pub-date` |出版日期|
| `from-print-pub-date` / `until-print-pub-date` |打印出版日期|
| `from-online-pub-date` / `until-online-pub-date` |网上发表日期|
| `from-posted-date` / `until-posted-date` |发布日期（预印本）|

### 布尔过滤器
|过滤|描述|
|--------|-------------|
| `has-abstract` |有摘要|
| `has-orcid` |具有 ORCID ID |
| `has-funder` |有资助者信息 |
| `has-full-text` |有全文链接|
| `has-references` |有参考清单|
| `has-license` |有许可证信息 |

### 值过滤器
|过滤|描述|
|--------|-------------|
| `type` | `journal-article`、`posted-content`、`book-chapter`、`proceedings-article`等|
| `issn` |期刊ISSN |
| `doi` |具体DOI |
| `orcid` |贡献者 ORCID |
| `funder` |资助者注册 ID |
| `member` |交叉引用会员ID |
| `prefix` | DOI 前缀 |
| `license.url` |许可证网址|
| `update-type` | `correction`, `retraction` |

* *语法：** `filter=name1:value1,name2:value2`

## 分页

### 基于偏移量（最大 10,000）
```
/works?query=cancer&rows=100&offset=200
```

### 基于光标（无限制）
1. 第一个请求：`?cursor=*&rows=100`
2. 响应包括 `next-cursor`
3. 下一个请求：`?cursor={next-cursor-value}&rows=100`
4. 游标在 5 分钟后过期

## 响应格式

### 列表响应
```json
{
  "status": "ok",
  "message-type": "work-list",
  "message": {
    "total-results": 2779116,
    "items-per-page": 20,
    "next-cursor": "...",
    "items": [...]
  }
}
```

### 工作对象（关键字段）
```json
{
  "DOI": "10.1038/nature12373",
  "title": ["Nanometre-scale thermometry in a living cell"],
  "author": [{"given": "G.", "family": "Kucsko", "sequence": "first"}],
  "publisher": "Springer Science and Business Media LLC",
  "type": "journal-article",
  "published": {"date-parts": [[2013, 7, 31]]},
  "container-title": ["Nature"],
  "ISSN": ["0028-0836", "1476-4687"],
  "volume": "500",
  "issue": "7460",
  "page": "54-58",
  "is-referenced-by-count": 1745,
  "references-count": 30,
  "abstract": "<p>Abstract text with HTML tags...</p>",
  "license": [{"URL": "...", "content-version": "vor"}],
  "link": [{"URL": "...", "content-type": "application/pdf"}],
  "reference": [{"key": "...", "doi-asserted-by": "crossref", "DOI": "..."}],
  "subject": ["Multidisciplinary"],
  "language": "en"
}
```

 注：`title` 和`container-title` 是数组。 `published.date-parts` 是 `[[year, month, day]]`。摘要可能包含 HTML 标签。
