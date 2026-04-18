# SEC EDGAR API 参考

## 概述
SEC 的电子数据收集、分析和检索系统。提供对公司文件、公司数据和 XBRL 财务数据的免费访问。不需要 API 密钥，但必须提供用于识别您身份的用户代理标头。

## 基本 URL
- **EFTS（全文搜索）：** `https://efts.sec.gov/LATEST`
- **公司/文件数据：** `https://data.sec.gov`
- **EDGAR 网站/档案：** `https://www.sec.gov`
- **XBRL API：** `https://data.sec.gov/api/xbrl`

## 身份验证
- **API 密钥：** 不需要。
- **用户代理标头：** 每个请求都需要。必须包含公司/个人名称和电子邮件。
 ```
 用户代理：MyCompany admin@mycompany.com
 ```
 没有正确用户代理的请求将被阻止 (403)。

## 速率限制
- **每个源每秒 10 个请求** IP.
  - 超过此值会导致基于 IP 的临时限制 (HTTP 429)。
  - SEC 要求用户在可能的情况下在市场时间之外（晚上 9:00 - 东部时间上午 6:00）发出请求以进行批量下载。

- --

## 关键端点

### 1.全文检索 (EFTS)

#### `GET https://efts.sec.gov/LATEST/search-index`
搜索所有 EDGAR 文件的全文。

* *参数：**
|参数|类型 |必填 |说明 |
|-------------|--------|---------|------------|
| `q` |字符串|是的 |搜索查询文本。支持布尔运算符（`AND`、`OR`、`NOT`）、引号中的精确短语。 |
| `dateRange` |字符串|没有 | `custom` 启用日期过滤。 |
| `startdt` |字符串|没有 |开始日期 `YYYY-MM-DD`。 |
| `enddt` |字符串|没有 |结束日期 `YYYY-MM-DD`。 |
| `forms` |字符串|没有 |以逗号分隔的表单类型，例如`10-K,10-Q,8-K`。 |
| `from` |整数 |没有 |分页偏移量（默认 0）。 |
| `size` |整数 |没有 |每页结果（默认 10 个，最大值各不相同）。 |

* *示例：**
```
https://efts.sec.gov/LATEST/search-index?q=%22artificial+intelligence%22&forms=10-K&startdt=2024-01-01&enddt=2024-12-31
```

* *响应：**
```json
{
  "hits": {
    "hits": [
      {
        "_id": "0001234567-24-000123:filing.htm",
        "_source": {
          "file_date": "2024-03-15",
          "display_date_filed": "2024-03-15",
          "entity_name": "EXAMPLE CORP",
          "file_num": "001-12345",
          "form_type": "10-K",
          "file_description": "Annual report",
          "period_of_report": "2023-12-31"
        }
      }
    ],
    "total": { "value": 150 }
  }
}
```

### 2. EDGAR 全文搜索（首选较新端点）

#### `GET https://efts.sec.gov/LATEST/search-index`（也可访问如下）

#### `GET https://efts.sec.gov/LATEST/search-index?q=...`

注意：EDGAR全文搜索也已在更简单的URL下公开：

#### `GET https://efts.sec.gov/LATEST/search-index`

以上是规范端点。一些文档还引用了相同后端的 EDGAR 搜索 UI。

- --

### 3. 公司股票代码和 CIK 查找

#### `GET https://www.sec.gov/cgi-bin/browse-edgar`
Legacy EDGAR 公司搜索。

* *参数：**
|参数|类型 |必填 |描述 |
|-----------|--------|---------|-------------|
| `company` |字符串|没有 |公司名称搜索。 |
| `CIK` |字符串|没有 | CIK 编号或股票代码。 |
| `type` |字符串|没有 |归档型过滤器（例如，`10-K`）。 |
| `dateb` |字符串|没有 |提交日期为 `YYYY-MM-DD` 之前。 |
| `owner` |字符串|没有 | `include`、`exclude` 或 `only`。 |
| `count` |整数 |没有 |结果数（最多 100）。 |
| `action` |字符串|是的 | `getcompany` 用于公司搜索。 |
| `output` |字符串|没有 | `atom` 用于 XML/Atom 提要。 |

* *示例：**
```
https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=AAPL&type=10-K&dateb=&owner=include&count=10&output=atom
```

#### `GET https://www.sec.gov/files/company_tickers.json`
返回所有公司代码到 CIK 的 JSON 映射数字。

* *回复：**
```json
{
  "0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."},
  "1": {"cik_str": 789019, "ticker": "MSFT", "title": "MICROSOFT CORP"},
  ...
}
```

#### `GET https://www.sec.gov/files/company_tickers_exchange.json`
包括每个代码的交换信息。

- --

### 4. 公司备案和提交

#### `GET https://data.sec.gov/submissions/CIK{cik_padded}.json`
返回给定 CIK 的公司元数据和最近提交的文件（以零填充到 10）数字）。

* *示例：**
```
https://data.sec.gov/submissions/CIK0000320193.json
```

* *响应：**
```json
{
  "cik": "320193",
  "entityType": "operating",
  "sic": "3571",
  "sicDescription": "Electronic Computers",
  "name": "Apple Inc.",
  "tickers": ["AAPL"],
  "exchanges": ["Nasdaq"],
  "filings": {
    "recent": {
      "accessionNumber": ["0000320193-24-000123", ...],
      "filingDate": ["2024-11-01", ...],
      "reportDate": ["2024-09-28", ...],
      "form": ["10-K", ...],
      "primaryDocument": ["aapl-20240928.htm", ...],
      "primaryDocDescription": ["10-K", ...]
    },
    "files": [
      {"name": "CIK0000320193-submissions-001.json", "filingCount": 1000}
    ]
  }
}
```

`filings.recent` 对象包含最新的约 1000 个申请。较旧的归档位于 `filings.files` 引用的单独分页文件中。

- --

### 5. 公司概念（XBRL 数据）

#### `GET https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/{taxonomy}/{tag}.json`
返回公司报告的所有值中特定 XBRL 标签的所有值文件.

* *路径参数：**
|参数|描述|
|------------|-------------|
| `cik` |零填充 CIK（10 位数字）。 |
| `taxonomy` | XBRL 分类：`us-gaap`、`ifrs-full`、`dei`、`srt`。 |
| `tag` | XBRL 概念标签，例如 `Revenue`、`Assets`、`AccountsPayableCurrent`。 |

* *示例：**
```
https://data.sec.gov/api/xbrl/companyconcept/CIK0000320193/us-gaap/Revenue.json
```

* *响应：**
```json
{
  "cik": 320193,
  "taxonomy": "us-gaap",
  "tag": "Revenue",
  "label": "Revenue",
  "description": "Amount of revenue recognized...",
  "entityName": "Apple Inc.",
  "units": {
    "USD": [
      {
        "start": "2023-10-01",
        "end": "2024-09-28",
        "val": 391035000000,
        "accn": "0000320193-24-000123",
        "fy": 2024,
        "fp": "FY",
        "form": "10-K",
        "filed": "2024-11-01"
      }
    ]
  }
}
```

- --

### 6. 公司情况（一家公司的所有 XBRL）

#### `GET https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json`
返回公司在所有申请中报告的所有 XBRL 概念。

* *示例：**
```
https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json
```

* *响应：**与 companyconcept 结构相同，但所有标签都嵌套在 `facts.us-gaap`、`facts.dei` 下，等。

```json
{
  "cik": 320193,
  "entityName": "Apple Inc.",
  "facts": {
    "dei": {
      "EntityCommonStockSharesOutstanding": { "units": { "shares": [...] } }
    },
    "us-gaap": {
      "Revenue": { "units": { "USD": [...] } },
      "Assets": { "units": { "USD": [...] } }
    }
  }
}
```

- --

### 7. 框架（一段时间内的跨公司 XBRL）

#### `GET https://data.sec.gov/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period}.json`
返回给定报告的所有公司的特定 XBRL 概念值period.

* *路径参数：**
|参数|描述|
|------------|-------------|
| `taxonomy` | `us-gaap`、`ifrs-full`、`dei`、`srt`。 |
| `tag` | XBRL 标签，例如 `Assets`。 |
| `unit` | `USD`、`shares`、`pure`等|
| `period` |即时：`CY2023Q4I`；持续时间：`CY2023`、`CY2023Q1`。 |

* *期间格式：**
- `CY2023` = 2023 日历年（全年持续时间）
- `CY2023Q1` = 2023 年第一季度持续时间
- `CY2023Q4I` = 2023 年第四季度末即时（资产负债表）项）

* *示例：**
```
https://data.sec.gov/api/xbrl/frames/us-gaap/Assets/USD/CY2023Q4I.json
```

* *响应：**
```json
{
  "taxonomy": "us-gaap",
  "tag": "Assets",
  "ccp": "CY2023Q4I",
  "uom": "USD",
  "label": "Assets",
  "description": "Sum of the carrying amounts...",
  "pts": 8500,
  "data": [
    {"accn": "0000320193-24-000123", "cik": 320193, "entityName": "Apple Inc.", "loc": "US-CA", "end": "2023-12-30", "val": 352583000000}
  ]
}
```

- --

### 8. 归档档案（直接文档访问）

#### `GET https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number_no_dashes}/{filename}`
直接访问任何归档文件。

* *示例：**
```
https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm
```

URL中的入藏号格式去掉破折号：`0000320193-24-000123`变为`000032019324000123`.

- --

## 常用XBRL标签参考
|标签 |描述|
|-----|-------------|
| `Revenue` / `Revenues` |总收入|
| `NetIncomeLoss` |净利润|
| `Assets` |总资产|
| `Liabilities` |负债总额|
| `StockholdersEquity` |总权益|
| `EarningsPerShareBasic` |基本EPS |
| `EarningsPerShareDiluted` |稀释每股收益|
| `OperatingIncomeLoss` |营业收入|
| `CashAndCashEquivalentsAtCarryingValue` |现金及等价物|
| `LongTermDebt` |长期债务|
| `CommonStockSharesOutstanding` |流通股 |

## 备注
- `data.sec.gov` URL 中的 CIK 编号必须以零填充至 10 位数字。
- EFTS 全文搜索索引文件的文本内容，而不是 XBRL 数据。
- 对于批量下载，SEC 在以下位置提供索引文件： `https://www.sec.gov/Archives/edgar/full-index/`.
- 除非另有说明，所有响应均为 JSON。归档文档可以是 HTML、XML 或纯文本。
