# OpenAlex API

OpenAlex 是一个包含 2.5 亿+学术著作、作者、机构、来源和主题的综合索引。它是该技能中最广泛的多学科数据库。

## 基本 URL

```
https://api.openalex.org
```

## 身份验证

- **推荐 API 密钥**（免费）。在 https://openalex.org/settings/api
 获取一个 - 传递为：`?api_key=YOUR_KEY`
 - 传统礼貌池仍然有效：添加 `?mailto=you@example.com` 以获得更好的速率限制

## 速率限制

 - **100 个请求/秒** max
  - 基于使用情况的定价，每天免费 1 美元津贴
- 按 ID/DOI 进行单个实体查找是免费的（无限制）
- 列表 + 过滤器查询：每个约 0.0001 美元（约 10,000 个/天免费）
- 搜索查询：每个约 0.001 美元（约 1,000 个/天免费）

## 密钥端点

### 1.获取单个作品

```
GET /works/{id}
```

接受多种ID格式：
```
/works/W2741809807                              (OpenAlex ID)
/works/doi:10.7717/peerj.4375                  (DOI)
/works/pmid:29456894                            (PMID)
/works/https://doi.org/10.7717/peerj.4375      (full DOI URL)
```

### 2.搜索作品

```
GET /works?search={query}&per_page={n}&page={n}
```

|参数|默认|描述 |
|---------|---------|------------|
| `search` | --|全文搜索（标题、摘要、全文）。支持布尔值：`AND`、`OR`、`NOT`（大写）|
| `search.exact` | --|无词干|
| `search.semantic` | --| AI 嵌入搜索（测试版，1 个请求/秒，最多 50 个结果）|
| `filter` | --|逗号分隔的 `field:value` 对 |
| `sort` |相关性 | `cited_by_count:desc`、`publication_date:desc`、`relevance_score:desc` |
| `per_page` | 25 | 25每页结果（最多 100 条）|
| `page` | 1 |页码（最大 `page * per_page` = 10,000）|
| `cursor` | --|使用 `*` 进行深度分页首页|
| `select` | --|返回 |
| 的逗号分隔字段`group_by` | --|按字段聚合|

* *高级搜索：**支持通配符(`machin*`)、模糊(`machin~1`)、邻近(`"climate change"~5`)、布尔分组.

* *示例：**
```
https://api.openalex.org/works?search=CRISPR+gene+therapy&filter=from_publication_date:2023-01-01&sort=cited_by_count:desc&per_page=10
```

### 3. 过滤器工作原理

```
GET /works?filter={filters}
```

关键过滤字段：
|过滤|示例|描述 |
|--------|---------|------------|
| `from_publication_date` | `2023-01-01` |发布日期 |
| 之后`to_publication_date` | `2024-12-31` |发布日期 |
| 之前`publication_year` | `2024` |确切年份 |
| `type` | `article` |工作类型|
| `cited_by_count` | `>100` |引用阈值|
| `is_oa` | `true` |仅限开放获取|
| `has_abstract` | `true` |有摘要|
| `authorships.author.id` | `A5048491430` |按作者ID |
| `primary_location.source.id` | `S137773608` |按期刊/来源|
| `institutions.country_code` | `us` |按国家|
| `concepts.id` | `C41008148` |按概念/主题 |
| `doi` | `10.1038/nature12373` |按 DOI |

* * 运算符：** `>`、`<`、`!`（求反）、`|`（过滤器内或）

* *示例：**
```
https://api.openalex.org/works?filter=from_publication_date:2024-01-01,type:article,is_oa:true,cited_by_count:>50
```

### 4.其他实体

```
GET /authors?search={name}
GET /authors/{id}
GET /sources?search={name}          (journals, repositories)
GET /sources/{id}
GET /institutions?search={name}
GET /institutions/{id}
GET /topics/{id}
```

作者和机构接受类似的过滤/排序/分页参数。

### 5.光标分页（适用于> 10,000个结果）

```
GET /works?filter=publication_year:2024&cursor=*&per_page=100
```

响应包括`meta.next_cursor`。在下一个请求中将其作为 `cursor={value}` 传递。 `next_cursor`为空时停止。

## 响应格式

### 工作对象（关键字段）

```json
{
  "id": "https://openalex.org/W2741809807",
  "doi": "https://doi.org/10.7717/peerj.4375",
  "title": "The state of OA",
  "publication_year": 2018,
  "publication_date": "2018-02-13",
  "type": "article",
  "language": "en",
  "is_retracted": false,
  "cited_by_count": 1169,
  "open_access": {
    "is_oa": true,
    "oa_status": "gold",
    "oa_url": "https://doi.org/10.7717/peerj.4375"
  },
  "authorships": [{
    "author": {"id": "https://openalex.org/A5048491430", "display_name": "Heather Piwowar"},
    "institutions": [{"display_name": "Impactstory"}]
  }],
  "primary_location": {
    "source": {"display_name": "PeerJ", "issn_l": "2167-8359"}
  },
  "abstract_inverted_index": {"Despite": [0], "growing": [1], "interest": [2], ...},
  "referenced_works": ["https://openalex.org/W123...", ...],
  "ids": {"openalex": "...", "doi": "...", "pmid": "..."}
}
```

### 摘要倒排索引

摘要存储为`{word: [positions]}`。重构：
```python
def reconstruct(inverted_index):
    positions = {}
    for word, indices in inverted_index.items():
        for idx in indices:
            positions[idx] = word
    return ' '.join(positions[i] for i in sorted(positions.keys()))
```

### 列出响应

```json
{
  "meta": {"count": 3771834, "page": 1, "per_page": 10},
  "results": [...]
}
```

## 错误格式

HTTP 403表示无效API密钥，429表示超出速率限制。错误响应包含消息字段。
