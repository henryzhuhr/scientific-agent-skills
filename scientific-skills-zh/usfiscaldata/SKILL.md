---
name: usfiscaldata
description: 查询美国财政部财政数据 API 以获取联邦金融数据，包括国债、政府支出、收入、利率、汇率和储蓄债券。无需 API 密钥即可访问 54 个数据集和 182 个数据表。在处理美国联邦财政数据、国债跟踪（便士债务）、每日国债报表、月度国债报表、国债拍卖、国债利率、外汇汇率、储蓄债券或任何美国政府财务统计数据时使用。
license: MIT
metadata:
    skill-author: K-Dense Inc.
---

# 美国财政部财政数据API

免费，美国财政部开放REST API，用于获取联邦金融数据。无需 API 密钥或注册。

* *基本 URL：** `https://api.fiscaldata.treasury.gov/services/api/fiscal_service`

## 快速入门

```python
import requests
import pandas as pd

BASE_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"

# Get the current national debt (Debt to the Penny)
resp = requests.get(f"{BASE_URL}/v2/accounting/od/debt_to_penny", params={
    "sort": "-record_date",
    "page[size]": 1
})
data = resp.json()["data"][0]
print(f"Total public debt as of {data['record_date']}: ${float(data['tot_pub_debt_out_amt']):,.0f}")
```

```python
# Get Treasury exchange rates for recent quarters
resp = requests.get(f"{BASE_URL}/v1/accounting/od/rates_of_exchange", params={
    "fields": "country_currency_desc,exchange_rate,record_date",
    "filter": "record_date:gte:2024-01-01",
    "sort": "-record_date",
    "page[size]": 100
})
df = pd.DataFrame(resp.json()["data"])
```

## 身份验证

无需。 API完全开放、免费。

## 核心参数

|参数|示例|描述 |
|---------|---------|------------|
| `fields=` | `fields=record_date,tot_pub_debt_out_amt` |选择特定列|
| `filter=` | `filter=record_date:gte:2024-01-01` |过滤记录|
| `sort=` | `sort=-record_date` |排序（前缀 `-` 表示降序）|
| `format=` | `format=json` |输出格式：`json`、`csv`、`xml` |
| `page[size]=` | `page[size]=100` |每页记录数（默认100）|
| `page[number]=` | `page[number]=2` |页面索引（从1开始）|

* *过滤运算符：** `lt`、`lte`、`gt`、`gte`、`eq`、`in`

```python
# Multiple filters separated by comma
"filter=country_currency_desc:in:(Canada-Dollar,Mexico-Peso),record_date:gte:2024-01-01"
```

## 关键数据集和端点

### Debt

|数据集 |端点|频率 |
|---------|---------|-----------|
|欠一分钱| `/v2/accounting/od/debt_to_penny` |每日|
|历史未偿债务| `/v2/accounting/od/historical_debt_outstanding` |年度|
|联邦债务表| `/v1/accounting/od/schedules_fed_debt` |每月 |

### 每日和每月报表

|数据集 |端点|频率 |
|---------|---------|------------|
| DTS 运营现金余额 | `/v1/accounting/dts/operating_cash_balance` |每日|
| DTS 存取款 | `/v1/accounting/dts/deposits_withdrawals_operating_cash` |每日|
|每月财务报表 (MTS) | `/v1/accounting/mts/mts_table_1`（16桌） |每月 |

### 利率和汇率

|数据集 |端点|频率 |
|---------|---------|------------|
|国债平均利率| `/v2/accounting/od/avg_interest_rates` |每月|
|财政部报告汇率| `/v1/accounting/od/rates_of_exchange` |季刊|
|公共债务利息支出| `/v2/accounting/od/interest_expense` |每月 |

### 证券及拍卖

|数据集 |端点|频率 |
|---------|---------|------------|
|国债拍卖数据| `/v1/accounting/od/auctions_query` |根据需要|
|国库券即将拍卖 | `/v1/accounting/od/upcoming_auctions` |根据需要|
|平均利率| `/v2/accounting/od/avg_interest_rates` |每月|

### 储蓄国债

|数据集 |端点|频率 |
|---------|---------|-----------|
| I 债券利率 | `/v2/accounting/od/i_bond_interest_rates` |半年度|
|美国国债储蓄债券：发行、赎回和到期日 | `/v1/accounting/od/sb_issues_redemptions` |每月 |

## 响应结构

```json
{
  "data": [...],
  "meta": {
    "count": 100,
    "total-count": 3790,
    "total-pages": 38,
    "labels": {"field_name": "Human Readable Label"},
    "dataTypes": {"field_name": "STRING|NUMBER|DATE|CURRENCY"},
    "dataFormats": {"field_name": "String|10.2|YYYY-MM-DD"}
  },
  "links": {"self": "...", "first": "...", "prev": null, "next": "...", "last": "..."}
}
```

* *注意：** 所有值均以字符串形式返回。根据需要进行转换（例如，`float()`、`pd.to_datetime()`）。空值显示为字符串 `"null"`.

## 常见模式

### 将所有页面加载到 DataFrame

```python
def fetch_all_pages(endpoint, params=None):
    params = params or {}
    params["page[size]"] = 10000  # max size to minimize requests
    resp = requests.get(f"{BASE_URL}{endpoint}", params=params)
    result = resp.json()
    df = pd.DataFrame(result["data"])
    return df
```

### 聚合（自动求和）

Omitting 分组字段触发自动聚合：

```python
# Sum all deposits/withdrawals by record_date and transaction type
resp = requests.get(f"{BASE_URL}/v1/accounting/dts/deposits_withdrawals_operating_cash", params={
    "fields": "record_date,transaction_type,transaction_today_amt"
})
```

## 参考文件

- **[api-basics.md](references/api-basics.md)** — URL 结构、HTTP 方法、版本控制、数据类型
- **[parameters.md](references/parameters.md)** — 所有带有详细示例和边缘情况的参数
- **[datasets-debt.md](references/datasets-debt.md)** — 债务数据集：便士债务、历史债务、联邦债务表、TROR
- **[datasets-fiscal.md](references/datasets-fiscal.md)** — 每日财务报表、每月财务报表、收入、支出
- **[datasets-interest-rates.md](references/datasets-interest-rates.md)** — 平均利息利率、汇率、TIPS/CPI、认证利率
- **[datasets-securities.md](references/datasets-securities.md)** — 国债拍卖、储蓄债券、SLGS、回购
- **[response-format.md](references/response-format.md)** — 响应对象、错误处理、分页、响应codes
- **[examples.md](references/examples.md)** — 常见用例的 Python、R 和 pandas 代码示例
