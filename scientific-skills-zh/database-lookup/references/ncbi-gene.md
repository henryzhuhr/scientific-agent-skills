# NCBI Gene (E-utilities)

## 基本 URL
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

## Auth
API 密钥可选，但建议使用。无密钥：3 请求/秒。使用密钥：10 个请求/秒。
 来自 https://www.ncbi.nlm.nih.gov/account/settings/
 的免费密钥传递为：`&api_key=YOUR_KEY`

## 关键端点

### eSearch — 搜索基因ID
```
GET /esearch.fcgi?db=gene&term={query}&retmode=json&retmax={n}
```

参数：
- `db=gene`（必填）
- `term` — 搜索查询（例如 `BRCA1[gene]+AND+human[orgn]`）
- `retmode=json`
- `retmax` — 最大结果（默认 20）
- `retstart` — 分页偏移量

E示例：
```
/esearch.fcgi?db=gene&term=BRCA1[gene]+AND+human[orgn]&retmode=json&retmax=5
```

### eSummary — 获取基因元数据
```
GET /esummary.fcgi?db=gene&id={gene_ids}&retmode=json
```

关键响应字段：`name`、`description`、`chromosome`、`maplocation`、`otheraliases`、`nomenclaturesymbol`、 `organism`

示例：
```
/esummary.fcgi?db=gene&id=672&retmode=json
```

### eFetch — 完整基因记录（仅限 XML/文本，无 JSON）
```
GET /efetch.fcgi?db=gene&id={gene_ids}&rettype=gene_table&retmode=text
```

### eLink — 跨数据库链接（基因到通路、PubMed、 OMIM)
```
GET /elink.fcgi?dbfrom=gene&db={target_db}&id={gene_id}&retmode=json
```

目标数据库：`biosystems`（通路）、`pubmed`、`omim`、`nuccore`、`protein`

示例 — 基因路径：
```
/elink.fcgi?dbfrom=gene&db=biosystems&id=672&retmode=json
```

## 速率限制
- 不带 API 密钥：3 个请求/秒
- 使用 API 密钥：10 个请求/秒
- 对于批量：使用 `usehistory=y` 与 eSearch，然后通过 `query_key` 检索和`WebEnv`
