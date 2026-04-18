# PMC (PubMed Central)

PMC 是生物医学和生命科学文章的**全文存档**。它与 PubMed 是分开的——PubMed 有引文/摘要，PMC 有全文。并非所有 PubMed 文章都在 PMC 中，反之亦然。

## PMC 的电子实用程序

### 基本 URL

```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

 与 PubMed 相同的电子实用程序，但使用 `db=pmc`.

### eSearch -- 搜索PMC

```
GET /esearch.fcgi?db=pmc&term={query}&retmode=json
```

与 PubMed eSearch 的参数相同。返回 PMC UID（数字，例如 `13033346`）。您需要在前面添加“PMC”才能获取 PMCID（例如 `PMC13033346`）。

### eFetch -- 获取全文 XML

```
GET /efetch.fcgi?db=pmc&id={pmcid}&retmode=xml
```

|重新输入 |旋转模式 |返回 |
|---------|---------|---------|
| *（省略）* | `xml` | **全文 JATS XML**（正文、图表、参考文献）|
| `medline` | `text` | MEDLINE 格式 |

* *示例：**
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=7029759&retmode=xml
```

XML 使用 JATS（期刊文章标签套件）格式：
- `<front>` -- 期刊元数据、文章元数据、作者信息
- `<body>` -- 完整文章文本`<sec>` 部分、`<p>` 段落、`<fig>` 数字
- `<back>` -- `<ref-list>` 以及所有引用

 仅传递数字 ID（不是“PMC7029759”，只是“7029759”）。

## BioC API -- 结构化全文

以结构化段落格式获取全文的另一种方法。

### 基本 URL

```
https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/
```

### 端点

```
GET /BioC_{format}/{id}/{encoding}
```

|参数|值|
|---------|--------|
| `format` | `json` 或 `xml` |
| `id` | PMID（例如，`17299597`）或 PMCID（例如，`PMC7029759`）|
| `encoding` | `unicode` 或 `ascii` |

* *示例：**
```
https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC7029759/unicode
```

* *响应结构 (JSON)：**
```json
{
  "source": "PMC",
  "documents": [{
    "id": "PMC7029759",
    "infons": {"license": "...", "doi": "..."},
    "passages": [
      {
        "offset": 0,
        "infons": {"section_type": "TITLE"},
        "text": "Article title..."
      },
      {
        "offset": 42,
        "infons": {"section_type": "ABSTRACT"},
        "text": "Abstract text..."
      },
      {
        "offset": 500,
        "infons": {"section_type": "INTRO"},
        "text": "Introduction text..."
      }
    ]
  }]
}
```

 部分类型：`TITLE`， `ABSTRACT`、`INTRO`、`METHODS`、`RESULTS`、`DISCUSS`、`CONCL`、`REF`、`SUPPL`、`FIG`、`TABLE`

* *覆盖范围：** 来自 PMC 开放获取子集的约 300 万篇文章。

## PMC ID 转换器 API

在 PMID、PMCID、DOI 和稿件 ID 之间进行转换。

### 基本 URL

```
https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/
```

### 参数

|参数|必填 |描述 |
|-----------|---------|------------|
| `ids` |是的 |最多 200 个以逗号分隔的 ID |
| `idtype` |没有 | `pmcid`、`pmid`、`mid`、`doi`（默认：自动检测）|
| `format` |没有 | `json`、`xml`、`csv`（默认：xml）|
| `tool` |推荐|您的应用名称|
| `email` |推荐|您的联系电子邮件 |

* *示例：**
```
https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?ids=PMC7029759&format=json
```

* *回复：**
```json
{
  "status": "ok",
  "records": [{
    "pmcid": "PMC7029759",
    "pmid": "32117569",
    "doi": "10.12688/f1000research.22211.2"
  }]
}
```

 仅返回 PMC 中文章的结果。如果一篇文章在 PubMed 但不在 PMC 中，则不会返回 PMCID。

## 速率限制

|服务 |极限|
|---------|-----|
|电子公用事业（`db=pmc`）|不带钥匙 3/秒，带钥匙 10/秒 |
| BioC API |遵循一般 NCBI 政策（3/秒，无密钥）|
| ID转换器|遵循一般 NCBI 政策 |

 在电子实用程序请求中包含 `tool` 和 `email` 参数。大型批量作业应在高峰时间（周一至周五上午 5 点至晚上 9 点（美国东部时间））之外运行。
