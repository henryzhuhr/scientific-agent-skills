# USPTO 公共 API

## 1. PatentsView API（主要专利检索）

建议使用较新的基于 Elasticsearch 的 API。

### 基本 URL

```
https://search.patentsview.org/api/v1/
```

* *需要 API 密钥** — 在 `https://patentsview.org/apis/keyrequest`

 处注册作为查询传递参数：`?api_key=YOUR_KEY`

### 关键端点

#### 搜索专利
```
GET or POST /patent/
```

查询参数`q`接受JSON查询对象。

运算符：`_eq`、`_neq`、 `_gt`、`_gte`、`_lt`、`_lte`、`_begins`、`_contains`、`_text_any`、`_text_all`、`_text_phrase`、`_and`、`_or`、 `_not`

参数：
- `q` — JSON 查询
- `f` — 要返回的字段（JSON 数组）
- `o` — 选项：`{"size": 25}` for分页
- `s` — 排序：`[{"patent_date": "desc"}]`

#### 按关键字搜索
```
GET /patent/?q={"_text_any":{"patent_abstract":"autonomous vehicle"}}&f=["patent_id","patent_title","patent_date"]&o={"size":5}&api_key=KEY
```

#### 按发明人搜索
```
GET /patent/?q={"inventors.inventor_name_last":"Tesla"}&f=["patent_id","patent_title","patent_date"]&api_key=KEY
```

#### 按受让人
```
GET /patent/?q={"assignees.assignee_organization":"Google LLC"}&f=["patent_id","patent_title","patent_date","assignees"]&api_key=KEY
```

#### 按专利号查找
```
GET /patent/{patent_number}/?api_key=KEY
```

#### 其他实体端点
```
/inventor/
/assignee/
/cpc_group/
```

### 响应结构

```json
{
  "patents": [
    {
      "patent_id": "11234567",
      "patent_title": "...",
      "patent_date": "2022-03-15",
      "patent_abstract": "...",
      "assignees": [{"assignee_organization": "..."}],
      "inventors": [{"inventor_name_first": "...", "inventor_name_last": "..."}]
    }
  ],
  "count": 1,
  "total_hits": 8923
}
```

### 速率限制

~每个 API 密钥每分钟 45 个请求。

### 重要提示

用户必须拥有此端点的 PatentsView API 密钥。如果他们没有，请告知他们需要在 `https://patentsview.org/apis/keyrequest` 注册。从 `.env` 加载密钥为 `PATENTSVIEW_API_KEY`.

 * *注意：** `api.patentsview.org` 的旧版 API 已停用（返回 410 Gone）。仅上述新 API 有效。

## 3. PEDS — 专利审查数据系统

* *URL**：`https://ped.uspto.gov/api/queries`

* *方法**：POST

用于专利审查数据（申请状态、申请日期、审查员）信息）。

```json
{
  "searchText": "applicationNumberText:16123456",
  "fl": "*",
  "mm": "100%",
  "df": "patentTitle",
  "facet": "false",
  "sort": "applId asc",
  "start": 0
}
```

不需要 API 密钥，但速率受到严重限制。可用性可能不可靠。

## 4. TSDR — 商标状态和文档检索

用于按序列号或注册号进行商标查找（不是全文搜索）。

```
GET https://tsdr.uspto.gov/documentxml/status/{serial_number}
GET https://tsdr.uspto.gov/documentxml/status/rn{registration_number}
```

返回包含标记详细信息、状态、所有者、商品/服务、起诉历史记录的 XML。

无 API 密钥。速率有限。无 JSON 端点 — 响应为 XML.

## 5. 限制

- **没有用于商标全文搜索的公共 REST API**（TESS 仅限 Web）
- PatentsView 新 API 需要注册 API 密钥
- PEDS 可用性不一致
- TSDR 需要已经知道序列/注册号
