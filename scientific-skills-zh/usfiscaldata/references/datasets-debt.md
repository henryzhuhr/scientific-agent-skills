# 债务数据集 — 美国财政部财政数据

## 对 Penny 的债务

* *端点：** `/v2/accounting/od/debt_to_penny` 
* *频率：** 每日 
* *日期范围：** 1993 年 4 月 1 日至今

 跟踪每个企业未偿付的确切公共债务总额day.

* *关键字段：**
|领域 |类型 |描述 |
|--------|------|-------------|
| `record_date` |日期 |记录日期|
| `debt_held_public_amt` |货币 |公众持有的债务|
| `intragov_hold_amt` |货币 |政府内部持股|
| `tot_pub_debt_out_amt` |货币 | **未偿公共债务总额** |

```python
# Current national debt
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny",
    params={"sort": "-record_date", "page[size]": 1}
)
latest = resp.json()["data"][0]
print(f"As of {latest['record_date']}: ${float(latest['tot_pub_debt_out_amt']):,.2f}")

# Debt over the last year
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny",
    params={
        "fields": "record_date,tot_pub_debt_out_amt",
        "filter": "record_date:gte:2024-01-01",
        "sort": "-record_date"
    }
)
df = pd.DataFrame(resp.json()["data"])
df["tot_pub_debt_out_amt"] = df["tot_pub_debt_out_amt"].astype(float)
```

## 历史未偿债务

* *端点：** `/v2/accounting/od/historical_debt_outstanding` 
* *频率：**每年 
* *日期范围：** 1790 年至今

 的年度记录美国国债可追溯到共和国成立之初。

* *关键字段：**
|领域 |类型 |描述|
|--------|------|-------------|
| `record_date` |日期 |年终日期|
| `debt_outstanding_amt` |货币 |未偿债务总额 |

```python
# Full historical debt series
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/historical_debt_outstanding",
    params={"sort": "-record_date", "page[size]": 10000}
)
df = pd.DataFrame(resp.json()["data"])
```

## 联邦债务表

* *端点：** `/v1/accounting/od/schedules_fed_debt` 
* *频率：**每月 
* *日期范围：** 2005 年 10 月至今

 联邦债务每月细目按安全类型和组件。

* *关键字段：**
|领域 |类型 |描述 |
|--------|------|-------------|
| `record_date` |日期 |月底日期 |
| `security_type_desc` |字符串 |安全类型|
| `security_class_desc` |字符串 |安全等级|
| `debt_outstanding_amt` |货币 |未偿债务 |

## 按日划分的联邦债务明细表

* *端点：** `/v1/accounting/od/schedules_fed_debt_daily` 
* *频率：** 每日 
* *日期范围：** 2006 年 9 月至今

 每日版联邦债务明细表，包含两个数据表。

## 财政部应收账款报告 (TROR)

* *端点：** `/v2/debt/tror` 
* *频率：** 每季度 
* *日期范围：** 2016 年 12 月至今

联邦机构合规性和应收账款数据。还包括：
- `/v2/debt/tror/data_act_compliance` — 120 天拖欠债务转介合规报告

* *关键字段：**
|领域 |类型 |描述 |
|--------|------|-------------|
| `record_date` |日期 |季度结束日期 |
| `funding_type_desc` |字符串 |资金类型|
| `total_receivables_delinquent_amt` |货币 |拖欠金额 |

```python
# TROR data, sorted by funding type
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/debt/tror",
    params={"sort": "funding_type_id"}
)
```

## 减少公共债务的捐赠

* *终点：** `/v2/accounting/od/gift_contributions` 
* *频率：** 每月 
* *日期范围：** 1996 年 9 月至目前

记录公众为减少国债自愿捐款。

## 未偿公共债务利息支出

* *端点：** `/v2/accounting/od/interest_expense` 
* *频率：**每月
* *日期范围：**2010年5月至目前

按证券类型细分的每月利息费用。

* *关键字段：**
|领域 |类型 |描述|
|--------|------|-------------|
| `record_date` |日期 |月结束日期|
| `security_type_desc` |字符串 |安全型|
| `expense_net_amt` |货币 |净利息支出|
| `expense_gross_amt` |货币 |总利息支出 |

```python
# Get total interest expense by month
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/interest_expense",
    params={
        "fields": "record_date,expense_net_amt",
        "filter": "record_date:gte:2020-01-01",
        "sort": "-record_date"
    }
)
df = pd.DataFrame(resp.json()["data"])
df["expense_net_amt"] = df["expense_net_amt"].astype(float)
```

## 国家失业基金预付款（第 XII 章）

* *端点：** `/v2/accounting/od/title_xii` 
* *频率：** 每日 
* *日期范围：** 2016 年 10 月至目前

各州和地区从联邦失业信托基金借款。

* *关键字段：**
|领域 |类型 |描述 |
|--------|------|-------------|
| `record_date` |日期 |记录日期|
| `state_nm` |字符串 |州名|
| `debt_outstanding_amt` |货币 |未付预付款金额|
