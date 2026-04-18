# 美国财政部财政数据 API 参考

## 概述
美国财政部的财政数据 API 提供对联邦金融数据的机器可读访问：国债、国债、利率、收益率曲线、收入、支出等。由财政服务局维护。

## 基本 URL
```
https://api.fiscaldata.treasury.gov/services/api/fiscal_service
```

## 身份验证
* *无需 API 密钥。** API 完全开放和公开。

## 速率限制
- **未发布正式的速率限制。**
- 预计合理使用；没有记录身份验证或限制。
- 对于批量数据，请使用大页面大小的分页。

- --

## 关键端点

### URL 模式
所有数据集端点如下：
```
GET /services/api/fiscal_service/{endpoint}?{parameters}
```

### 通用查询参数（适用于所有端点）
|参数|类型 |描述|
|---------|------|----------|
| `fields` |字符串|要返回的以逗号分隔的字段列表 |
| `filter` |字符串|过滤器表达式：`field:operator:value`（例如，`record_date:gte:2024-01-01`）|
| `sort` |字符串|排序字段：`field` (asc)或 `-field` (desc)；逗号分隔 |
| `page[number]` |整数 |页码（默认1）|
| `page[size]` |整数 |每页结果（默认 100，最大 10000）|
| `format` |字符串| `json`（默认）或 `csv` |

* *过滤运算符：**
`eq`（等于）、`lt`、`lte`、`gt`、`gte`、 `in`（逗号分隔值）

- --

### 1.国债收益率曲线利率（每日）
```
GET /v2/accounting/od/avg_interest_rates
```

* *更好的收益率终点曲线：**
```
GET /v1/accounting/od/rates_of_exchange
```

* *每日国债平价收益率曲线利率：**
注：每日收益率曲线利率发布于 `https://home.treasury.gov/resource-center/data-chart-center/interest-rates/`，并可通过 TreasuryDirect API 获取。通过财政数据进行编程访问：

```
GET /v2/accounting/od/avg_interest_rates
```

* *示例 -- 国债平均利率证券：**
```
https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?filter=record_date:gte:2024-01-01&sort=-record_date&page[size]=100
```

* *回复：**
```json
{
  "data": [
    {
      "record_date": "2024-10-31",
      "security_type_desc": "Treasury Bills",
      "security_desc": "Treasury Bills",
      "avg_interest_rate_amt": "5.223",
      "src_line_nbr": "1",
      "record_fiscal_year": "2025",
      "record_fiscal_quarter": "1",
      "record_calendar_year": "2024",
      "record_calendar_quarter": "4",
      "record_calendar_month": "10",
      "record_calendar_day": "31"
    }
  ],
  "meta": {
    "count": 100,
    "labels": { ... },
    "dataTypes": { ... },
    "dataFormats": { ... },
    "total-count": 1234,
    "total-pages": 13
  },
  "links": {
    "self": "&page%5Bnumber%5D=1&page%5Bsize%5D=100",
    "first": "&page%5Bnumber%5D=1&page%5Bsize%5D=100",
    "prev": null,
    "next": "&page%5Bnumber%5D=2&page%5Bsize%5D=100",
    "last": "&page%5Bnumber%5D=13&page%5Bsize%5D=100"
  }
}
```

- --

### 2. 便士债务（每日国债）
```
GET /v2/accounting/od/debt_to_penny
```

* *示例 -- 自 2024 年以来的债务：**
```
https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny?filter=record_date:gte:2024-01-01&sort=-record_date&page[size]=10
```

* *关键字段：** `record_date`、`tot_pub_debt_out_amt`、 `intragov_hold_amt`、`debt_held_public_amt`

- --

### 3.国债拍卖
```
GET /v1/accounting/od/auctions_query
```

* *示例 -- 最近的国债拍卖：**
```
https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query?filter=security_type:eq:Bill&sort=-auction_date&page[size]=10
```

* *关键字段：** `cusip`、`security_type`、`security_term`、`auction_date`、`issue_date`、`maturity_date`、`high_yield`、`high_discount_rate`、`bid_to_cover_ratio`、 `total_accepted`

- --

### 4. 每月财政报表（收入和支出）
```
GET /v1/accounting/mts/mts_table_5
```

* *示例 -- 联邦收入/支出：**
```
https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_5?filter=record_date:gte:2024-01-01&sort=-record_date&page[size]=50
```

- --

### 5. 联邦支出类别
```
GET /v1/accounting/mts/mts_table_9
```

* *示例：**
```
https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_9?filter=record_date:gte:2024-01-01&sort=-record_date
```

- --

### 6.国库报告汇率
```
GET /v1/accounting/od/rates_of_exchange
```

* *示例 --一季度汇率：**
```
https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/rates_of_exchange?filter=record_date:eq:2024-09-30&page[size]=200
```

* *关键字段：** `country_currency_desc`、`exchange_rate`、`record_date`、`effective_date`

- --

### 7、利息支出债务
```
GET /v2/accounting/od/interest_expense
```

* *示例：**
```
https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/interest_expense?filter=record_fiscal_year:eq:2024&sort=-record_date
```

- --

### 8. 储蓄债券速率
```
GET /v2/accounting/od/sb_value
```

- --

## 通用端点路径

|端点|描述 |
|----------|-------------|
| `v2/accounting/od/debt_to_penny` |每日未偿公共债务总额|
| `v2/accounting/od/avg_interest_rates` |国债平均利率|
| `v1/accounting/od/auctions_query` |国债拍卖结果|
| `v1/accounting/od/rates_of_exchange` |国库报告汇率|
| `v2/accounting/od/interest_expense` |公共债务利息支出|
| `v1/accounting/mts/mts_table_5` |每月财务报表：收入/支出 |
| `v1/accounting/mts/mts_table_9` |月度财务报表：按功能划分的支出 |
| `v2/accounting/od/statement_net_cost` |净成本表|
| `v2/accounting/od/debt_outstanding` |历史未偿债务（年度）|

## 响应格式
所有JSON响应共享相同的信封：
- `data`：结果对象数组
- `meta`：包含`count`、`total-count`、`total-pages`、字段标签和数据类型
- `links`：分页链接（`self`、`first`、`prev`、`next`、`last`）

## 注释
- 所有货币金额均以字符串形式返回以保持精度。
- 日期使用`record_date` 字段中的 `YYYY-MM-DD` 格式。
- `filter` 参数支持链接：`filter=field1:eq:val1,field2:gte:val2`.
- 使用 `fields=` 通过仅请求所需的列来减少响应大小。
- API 文档和数据集浏览器位于： https://fiscaldata.treasury.gov/api-documentation/
- 具体针对国债收益率曲线利率，FRED系列`DGS1`、`DGS2`、`DGS5`、`DGS10`、`DGS30`可能更方便。
