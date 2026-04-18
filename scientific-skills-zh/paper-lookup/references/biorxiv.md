# bioRxiv API

bioRxiv 是生物学的预印本服务器。 API 提供预印本的元数据，包括标题、作者、摘要、DOI 和出版状态。

* *重要：**bioRxiv API **没有关键字搜索**。它仅支持日期范围浏览和 DOI 查找。对于bioRxiv预印本的关键字搜索，请改用Semantic Sc​​holar、OpenAlex或CORE。

## 基本URL

```
https://api.biorxiv.org
```

## 身份验证

不需要。完全公开API.

## 关键端点

### 1.内容详细信息--按日期范围浏览

```
GET /details/biorxiv/{interval}/{cursor}/{format}
```

|参数|价值观 |描述|
|---------|--------|-------------|
| `interval` | `YYYY-MM-DD/YYYY-MM-DD` |日期范围（含）。保持较小的范围（1-3 天）以避免超时。 |
| | `N`（整数）| N 最新预印本 |
| | `Nd`（整数+“d”）|最近N天|
| `cursor` |整数（默认`0`）|分页偏移（每页 100 个结果）|
| `format` | `json`（默认）、`xml` |响应格式 |

 可选查询参数：`?category=neuroscience`（按类别过滤，空格使用下划线）

* *示例：**
```
https://api.biorxiv.org/details/biorxiv/2024-01-01/2024-01-31/0
https://api.biorxiv.org/details/biorxiv/5
https://api.biorxiv.org/details/biorxiv/10d
https://api.biorxiv.org/details/biorxiv/2024-01-01/2024-01-31?category=neuroscience
```

### 2. 内容详细信息 -- DOI查找

```
GET /details/biorxiv/{doi}/na/{format}
```

* *示例：**
```
https://api.biorxiv.org/details/biorxiv/10.1101/2024.01.16.575895/na/json
```

### 3. 已发表文章链接

```
GET /pubs/biorxiv/{interval}/{cursor}
GET /pubs/biorxiv/{doi}/na
```

将预印本链接到其已发表的期刊版本。接受预印本 DOI 和已发表的 DOI。

### 4. 出版商过滤器

```
GET /publisher/{prefix}/{interval}/{cursor}
```

 查找特定出版商出版的 bioRxiv 论文（按 DOI前缀).

* *示例:**
```
https://api.biorxiv.org/publisher/10.15252/2024-01-01/2024-06-01/0
```

## 响应格式

```json
{
  "messages": [{
    "status": "ok",
    "count": 100,
    "total": "1029",
    "cursor": 0
  }],
  "collection": [{
    "title": "Paper title...",
    "authors": "Surname, A.; Surname, B.",
    "author_corresponding": "Full Name",
    "author_corresponding_institution": "Institution",
    "doi": "10.1101/2024.01.16.575895",
    "date": "2024-01-20",
    "version": "1",
    "type": "new results",
    "license": "cc_no",
    "category": "cancer biology",
    "jatsxml": "https://www.biorxiv.org/content/early/.../source.xml",
    "abstract": "Full abstract text...",
    "published": "10.1158/2159-8290.CD-24-0187",
    "server": "bioRxiv"
  }]
}
```

- 如果尚未在期刊中发表，则 `published` 为 `"NA"`；如果已在期刊中发表，则为已发表的 DOI was.
- `type` 值：`new results`、`confirmatory results`、`contradictory results`

## 分页

所有多结果端点返回**每页 100 个结果**。使用`cursor`进行分页。 `messages` 对象告诉您 `total` 计数。

## 速率限制

没有记录的速率限制。无需身份验证。 

## 分类

`animal-behavior-and-cognition`、`biochemistry`、`bioengineering`、`bioinformatics`、`biophysics`、`cancer-biology`、`cell-biology`、`clinical-trials`、 `developmental-biology`、`ecology`、`epidemiology`、`evolutionary-biology`、`genetics`、`genomics`、`immunology`、`microbiology`、`molecular-biology`、`neuroscience`、 `paleontology`、`pathology`、`pharmacology-and-toxicology`、`physiology`、`plant-biology`、`scientific-communication-and-education`、`synthetic-biology`、`systems-biology`、`zoology`
