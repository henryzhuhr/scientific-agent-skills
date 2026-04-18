# Semantic Scholar API

Semantic Scholar 通过 AI 支持的功能索引所有学术领域的 2 亿多篇论文：引文上下文、有影响力的引文、TLDR 和论文推荐。

## 基本 URL

```
https://api.semanticscholar.org/graph/v1       (Academic Graph)
https://api.semanticscholar.org/recommendations/v1  (Recommendations)
```

## 身份验证

- **没有密钥：** 共享费率池（经常出现 429 错误）。有效，但不可靠。
- **使用密钥：** 每个密钥 1 请求/秒（根据请求更高）。
- 标头：`x-api-key: YOUR_KEY`
- 获取免费密钥：https://www.semanticscholar.org/product/api#api-key-form

## `fields`参数

几乎每个端点都接受`fields`——要包含的字段的逗号分隔列表（无空格）。没有它，你只能得到 `paperId` + `title`.

* *论文字段：**
`paperId`、`corpusId`、`externalIds`、`url`、`title`、`abstract`、 `venue`、`publicationVenue`、`year`、`referenceCount`、`citationCount`、`influentialCitationCount`、`isOpenAccess`、`openAccessPdf`、`fieldsOfStudy`、`s2FieldsOfStudy`、 `publicationTypes`、`publicationDate`、`journal`、`authors`、`citations`、`references`、`tldr`、`embedding`

* *作者字段：**
`authorId`、`externalIds`、`url`、`name`、`affiliations`、`homepage`、`paperCount`、`citationCount`、`hIndex`、 `papers`

## 纸张 ID 格式

`{paper_id}` 参数接受：
- `649def34f8be52c8b66281af98ae884c09aef38b`（S2 哈希）
- `CorpusId:215416146`
- `DOI:10.1038/s41586-021-03819-2`
- `ARXIV:2005.14165`
- `PMID:19872477`
- `PMCID:2323736`
- `ACL:W12-3903`

## 关键端点

### 1.论文检索（相关性）

```
GET /graph/v1/paper/search?query={text}&fields={fields}&offset={n}&limit={n}
```

|参数|默认|描述 |
|-----------|---------|------------|
| `query` |必填|纯文本搜索|
| `fields` |论文 ID,标题 |逗号分隔 |
| `offset` | 0 |分页开始 |
| `limit` | 100 | 100最多 100 |
| `year` | --| `2019` 或 `2016-2020` |
| `publicationDateOrYear` | --| `YYYY-MM-DD:YYYY-MM-DD` |
| `fieldsOfStudy` | --|例如，`Computer Science,Medicine` |
| `publicationTypes` | --|例如，`JournalArticle,Conference` |
| `openAccessPdf` | --| OA 纸张过滤器 |
| `minCitationCount` | --|最低引用次数|
| `venue` | --|逗号分隔的场所 |

* *最大 1,000 个结果**可通过偏移量访问。

* *示例：**
```
https://api.semanticscholar.org/graph/v1/paper/search?query=CRISPR+gene+therapy&fields=title,year,abstract,citationCount,authors,openAccessPdf&limit=10&year=2023-2024
```

### 2. 论文批量搜索（布尔查询、大结果）集）

```
GET /graph/v1/paper/search/bulk?query={text}&fields={fields}&sort={field}:{order}&token={token}
```

 - 支持布尔运算符：`+`（AND）、`|`（OR）、`-`（NOT）、`"..."`（短语）、`*`（通配符）、 `()`（分组）
- 基于令牌的分页（最多 10M 篇论文）
- 每次调用最多返回 1,000 个
- 可排序：`citationCount:desc`、`publicationDate:desc`、`paperId:asc`

### 3. 论文详情（按 ID）

```
GET /graph/v1/paper/{paper_id}?fields={fields}
```

* *示例：**
```
https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/s41586-021-03819-2?fields=title,year,abstract,citationCount,referenceCount,isOpenAccess,openAccessPdf,authors,tldr
```

* *回复：**
```json
{
  "paperId": "dc32a984b651256a8ec282be52310e6bd33d9815",
  "title": "Highly accurate protein structure prediction with AlphaFold",
  "year": 2021,
  "citationCount": 34260,
  "isOpenAccess": true,
  "openAccessPdf": {"url": "https://...pdf", "status": "HYBRID"},
  "tldr": {"text": "This work develops AlphaFold, a system that..."},
  "authors": [{"authorId": "47921134", "name": "J. Jumper"}, ...]
}
```

### 4. 论文引用

```
GET /graph/v1/paper/{paper_id}/citations?fields={fields}&offset={n}&limit={n}
```

返回引用本文的论文。 `limit` max 1000.

引文专用字段：`contexts`、`intents`、`isInfluential`

### 5.论文参考文献

```
GET /graph/v1/paper/{paper_id}/references?fields={fields}&offset={n}&limit={n}
```

返回本文引用的论文。与引文相同的分页。

### 6.论文标题匹配

```
GET /graph/v1/paper/search/match?query={exact title}&fields={fields}
```

返回与`matchScore`的单个最佳匹配。如果不匹配则为 404。

### 7. 作者搜索

```
GET /graph/v1/author/search?query={name}&fields={fields}&offset={n}&limit={n}
```

### 8. 作者详细信息

```
GET /graph/v1/author/{author_id}?fields={fields}
```

### 9. 作者的论文

```
GET /graph/v1/author/{author_id}/papers?fields={fields}&offset={n}&limit={n}
```

### 10.论文推荐

```
GET /recommendations/v1/papers/forpaper/{paper_id}?fields={fields}&limit={n}&from={pool}
```

`from`：`recent`（默认）或`all-cs`。 `limit`最大500.

### 11. 多论文推荐 (POST)

```
POST /recommendations/v1/papers/
Content-Type: application/json

{
  "positivePaperIds": ["paperId1", "paperId2"],
  "negativePaperIds": ["paperId3"]
}
```

### 12. 论文批量 (POST)

```
POST /graph/v1/paper/batch?fields={fields}
Content-Type: application/json

{"ids": ["DOI:10.1038/nature12373", "ARXIV:2005.14165"]}
```

 每个请求最多 500 个 ID。

## 分页

|端点|每页最大 |最大总数 |方法 |
|----------|-------------|------------|--------|
|相关性搜索 | 100 | 100 1,000 |偏移/下一个|
|批量搜索 | 1,000 | 10,000,000 |代币|
|引文/参考文献| 1,000 |全部 |偏移/下一个|
|作者搜索 | 1,000 | --|偏移/下一个 |

## 出版物类型

`Review`、`JournalArticle`、`CaseReport`、`ClinicalTrial`、`Conference`、`Dataset`、`Editorial`、`LettersAndComments`、 `MetaAnalysis`、`News`、`Study`、`Book`、`BookSection`

## 研究领域

`Computer Science`、`Medicine`、`Chemistry`、 `Biology`、`Materials Science`、`Physics`、`Geology`、`Psychology`、`Art`、`History`、`Geography`、`Sociology`、`Business`、 `Political Science`、`Economics`、`Philosophy`、`Mathematics`、`Engineering`、`Environmental Science`、`Agricultural and Food Sciences`、`Education`、`Law`、 `Linguistics`

## 错误格式

```json
{"message": "Too Many Requests", "code": "429"}
```

HTTP 404 表示未找到，429 表示速率限制。
