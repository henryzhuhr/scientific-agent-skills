# NCBI GEO（基因表达综合），通过电子实用程序

## 基本 URL

|目的|网址 |
|---|---|
|电子公用事业 | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/` |
| GEO直接查询| `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi` |

## 重要提示：数据库名称为 `gds`

GEO 的 Entrez 数据库为 `gds`（不是 `geo`）。它包含所有 GEO 记录类型：GDS 数据集、GSE 系列、GPL 平台、GSM 样本。在搜索词中使用 `[ETYP]` 按类型过滤。

## 关键端点

### eSearch — 搜索 GEO

```
GET /esearch.fcgi?db=gds&term={query}&retmode=json&retmax={n}
```

 参数：
- `db=gds`（必需）
- `term` — 带字段标签的搜索查询
- `retmax` — 最大结果（默认 20）
- `retstart` — 分页偏移量
- `retmode=json` — 获取 JSON 响应
- `usehistory=y` — 在服务器端存储结果用于大型查询
- `api_key` — NCBI API 密钥（可选，提高速率限制）

#### 条目类型过滤器 (`[ETYP]`)
- `gds[ETYP]` — 策划的 GEO 数据集
- `gse[ETYP]` — GEO 系列（大多数常见，默认使用）
- `gpl[ETYP]` — 平台
- `gsm[ETYP]` — 样本

#### 其他字段标签
- `[Organism]` — 例如`"Homo sapiens"[Organism]`
- `[PDAT]` — 出版日期
- `[Title]` — 标题搜索
- 布尔值：`AND`、`OR`、`NOT` （大写）

示例 — 人类癌症 GSE 系列：
```
/esearch.fcgi?db=gds&term=cancer+AND+gse[ETYP]+AND+"Homo+sapiens"[Organism]&retmax=10&retmode=json
```

响应：
```json
{
  "esearchresult": {
    "count": "15432",
    "retmax": "10",
    "idlist": ["200012345", "200067890"],
    "querytranslation": "cancer AND gse[ETYP]"
  }
}
```

返回的 ID 是数字 UID（不是登录号）。对于 GSE 记录：UID = 200000000 + GSE_number.

### eSummary — 获取 UID

的元数据```
GET /esummary.fcgi?db=gds&id={uid_list}&retmode=json
```

 每条记录的关键响应字段：
- `Accession` — 例如"GSE12345"
- `title`、`summary`
- `taxon` — 有机体
- `entrytype` — "GDS"、"GSE"、"GPL"、"GSM"
- `gdstype` — 例如“按数组进行表达分析”
- `n_samples` — 样本计数
- `pubmedids` — 链接的 PubMed ID
- `PDAT` — 出版日期
- `Samples` — 样本对象数组
- `FTPLink` — 数据下载路径

示例：
```
/esummary.fcgi?db=gds&id=200012345&retmode=json
```

### GEO 直接查询 — 按入录的全记录

```
GET https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={accession}&form={format}&view={detail}
```

参数：
- `acc` — GEO 登录（GSE12345、GDS1234、GPL570、GSM12345）
- `targ` — `self`、`gsm`（样品）、`gpl`（平台）、`gse` （系列）
- `form` — `text`（软格式）、`xml` (MINIML)、`html`
- `view` — `quick`、`brief`、 `full`、`data`

示例 — SOFT 中的系列元数据：
```
acc.cgi?acc=GSE53757&targ=self&form=text&view=brief
```

注意：acc.cgi 不返回 JSON。使用 eSearch + eSummary 获取 JSON 结果。当您需要完整的 SOFT/MINIML 记录时，请使用 acc.cgi。

### eLink — 与其他 NCBI 数据库的交叉引用

```
GET /elink.fcgi?dbfrom=gds&db=pubmed&id={uid}&retmode=json
```

## 实用工作流程

对于大多数查询，请使用此两步方法：

1. **eSearch** 查找与查询
2 匹配的UID。 **eSummary** 获取这些 UID 的元数据

这为您提供了整个 JSON。

## 重要说明

 - GDS 记录大部分被冻结 - NCBI 停止策划新的 GDS。使用 `gse[ETYP]` 获得全面的结果。
  - eFetch 对 `gds` 数据库的支持有限。使用 eSummary 获取元数据，或使用 acc.cgi 获取完整记录。
- URL 将空格编码为 `+`，将引号编码为 `%22`.

## 速率限制

- **没有 API 密钥**：3 个请求/秒
- **有 API 密钥**：10 个请求/秒（在 ncbi.nlm.nih.gov/account/settings 上免费注册）
- 包含 `&email=user@example.com` 作为礼貌 
- 对于大型结果集，请使用历史记录服务器（`usehistory=y` 然后通过`WebEnv` 和 `query_key` 至 eSummary)
