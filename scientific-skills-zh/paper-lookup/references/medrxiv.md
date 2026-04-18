# medRxiv API

medRxiv 是健康科学的预印本服务器。该API与bioRxiv的API相同——相同的端点，相同的响应格式——只需使用`medrxiv`作为服务器参数。

* *重要：**与bioRxiv一样，**没有关键字搜索**。使用 Semantic Sc​​holar、OpenAlex 或 PubMed 对 medRxiv 内容进行关键字搜索。

## 基本 URL

```
https://api.biorxiv.org
```

（与 bioRxiv 相同的基本 URL - 服务器在路径中指定。）

## 身份验证

不需要。完全公开的API.

## 关键端点

### 1.内容详细信息--按日期范围浏览

```
GET /details/medrxiv/{interval}/{cursor}/{format}
```

|参数|价值观 |描述|
|---------|--------|-------------|
| `interval` | `YYYY-MM-DD/YYYY-MM-DD` |日期范围（含）|
| | `N`（整数）| N 最新预印本 |
| | `Nd`（整数+“d”）|最近N天|
| `cursor` |整数（默认`0`）|分页偏移（每页 100）|
| `format` | `json`（默认）、`xml` |响应格式 |

可选：`?category=cardiovascular%20medicine`（对空格使用 URL 编码）

* *示例：**
```
https://api.biorxiv.org/details/medrxiv/2024-01-01/2024-01-31/0
https://api.biorxiv.org/details/medrxiv/5
https://api.biorxiv.org/details/medrxiv/10d
```

### 2. 内容详细信息 -- DOI查找

```
GET /details/medrxiv/{doi}/na/{format}
```

* *示例：**
```
https://api.biorxiv.org/details/medrxiv/10.1101/2021.04.29.21256344/na/json
```

### 3. 已发表文章链接

```
GET /pubs/medrxiv/{interval}/{cursor}
GET /pubs/medrxiv/{doi}/na
```

将预印本链接到其已发表的期刊版本。接受预印本 DOI 和已发布的 DOI。

## 响应格式

与 bioRxiv 相同：

```json
{
  "messages": [{
    "status": "ok",
    "count": 100,
    "total": "502",
    "cursor": 0
  }],
  "collection": [{
    "title": "Paper title...",
    "authors": "Surname, A.; Surname, B.",
    "author_corresponding": "Full Name",
    "author_corresponding_institution": "Institution",
    "doi": "10.1101/2021.04.29.21256344",
    "date": "2021-05-03",
    "version": "1",
    "type": "PUBLISHAHEADOFPRINT",
    "license": "cc_by_nc_nd",
    "category": "cardiovascular medicine",
    "abstract": "Full abstract text...",
    "published": "10.1371/journal.pone.0256482",
    "server": "medRxiv"
  }]
}
```

## 分页

每页 100 个结果。使用 `cursor` 参数进行分页。

## 速率限制

没有记录的速率限制。无需身份验证。

## 分类

`addiction-medicine`、`allergy-and-immunology`、`anesthesia`、`cardiovascular-medicine`、`dentistry-and-oral-medicine`、`dermatology`、`emergency-medicine`、`endocrinology`、`epidemiology`、`forensic-medicine`、 `gastroenterology`、`genetic-and-genomic-medicine`、`geriatric-medicine`、`health-economics`、`health-informatics`、`health-policy`、`health-systems-and-quality-improvement`、`hematology`、`hiv-aids`、`infectious-diseases`、 `intensive-care-and-critical-care-medicine`、`medical-education`、`medical-ethics`、`nephrology`、`neurology`、`nursing`、`nutrition`、`obstetrics-and-gynecology`、`occupational-and-environmental-health`、`oncology`、 `ophthalmology`、`orthopedics`、`otolaryngology`、`pain-medicine`、`palliative-medicine`、`pathology`、`pediatrics`、`pharmacology-and-therapeutics`、`primary-care-research`、`psychiatry-and-clinical-psychology`、 `public-and-global-health`、`radiology-and-imaging`、`rehabilitation-medicine-and-physical-therapy`、`respiratory-medicine`、`rheumatology`、`sexual-and-reproductive-health`、`sports-medicine`、`surgery`、`toxicology`、`transplantation`、 `urology`
