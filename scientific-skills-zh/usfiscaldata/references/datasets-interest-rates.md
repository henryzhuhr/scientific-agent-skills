# 利率和汇率数据集 — 美国财政部财政数据

## 美国国债平均利率

* *端点：** `/v2/accounting/od/avg_interest_rates` 
* *频率：** 每月 
* *日期范围：** 2001 年 1 月至今

 流通和流通的平均利率非流通国债，按证券类型细分。

* *关键字段：**
|领域 |类型 |描述 |
|--------|------|-------------|
| `record_date` |日期 |月结束日期|
| `security_desc` |字符串 |证券描述（例如“国库券”）|
| `security_type_desc` |字符串 | “适销”或“不可适销”|
| `avg_interest_rate_amt` |百分比|平均利率(%) |

```python
# Get average rates for all marketable securities, most recent month
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates",
    params={
        "filter": "security_type_desc:eq:Marketable",
        "sort": "-record_date",
        "page[size]": 50
    }
)
df = pd.DataFrame(resp.json()["data"])
latest = df[df["record_date"] == df["record_date"].max()]
print(latest[["security_desc", "avg_interest_rate_amt"]])

# Historical rate for a specific security type
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates",
    params={
        "fields": "record_date,avg_interest_rate_amt",
        "filter": "security_desc:eq:Treasury Notes,record_date:gte:2010-01-01",
        "sort": "-record_date"
    }
)
```

* *常用证券说明：**
- `Treasury Bills`
- `Treasury Notes`
- `Treasury Bonds`
- `Treasury Inflation-Protected Securities (TIPS)`
- `Treasury Floating Rate Notes (FRN)`
- `Federal Financing Bank`
- `United States Savings Securities`
- `Government Account Series`
- `Total Marketable`
- `Total Non-marketable`
- `Total Interest-bearing Debt`

- --

## 国库报告汇率

* *端点：** `/v1/accounting/od/rates_of_exchange` 
* *频率：** 每季度 
* *日期范围：** 三月2001 年至今，

 联邦机构用于报告目的的外币官方财政部汇率。每季度更新一次（3月31日、6月30日、9月30日、12月31日）。

* *关键字段：**
|领域 |类型 |描述 |
|--------|------|-------------|
| `record_date` |日期 |季度结束日期 |
| `country` |字符串 |国家名称|
| `currency` |字符串 |货币名称|
| `country_currency_desc` |字符串 |组合“国家/地区货币”（例如“加拿大元”）|
| `exchange_rate` |数量 |每 1 美元的外币单位 |
| `effective_date` |日期 |汇率生效日期 |

```python
# Get all current exchange rates (latest quarter)
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/rates_of_exchange",
    params={"sort": "-record_date", "page[size]": 200}
)
df = pd.DataFrame(resp.json()["data"])
latest_date = df["record_date"].max()
current_rates = df[df["record_date"] == latest_date].copy()
current_rates["exchange_rate"] = current_rates["exchange_rate"].astype(float)
print(current_rates[["country_currency_desc", "exchange_rate"]].to_string())

# Euro rate history
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/rates_of_exchange",
    params={
        "fields": "record_date,exchange_rate",
        "filter": "country_currency_desc:eq:Euro Zone-Euro",
        "sort": "-record_date",
        "page[size]": 100
    }
)
euro_df = pd.DataFrame(resp.json()["data"])
euro_df["exchange_rate"] = euro_df["exchange_rate"].astype(float)
euro_df["record_date"] = pd.to_datetime(euro_df["record_date"])
```

- --

## TIPS 和 CPI 数据

* *端点：** `/v1/accounting/od/tips_cpi_data` 
* *频率：** 每月 
* *日期范围：** 1998 年 4 月至今（2 个数据）表)

通胀保值国库券 (TIPS)参考 CPI 数据和用于计算 TIPS 值的指数比率。

* *关键字段：**
|领域 |类型 |描述 |
|--------|------|-------------|
| `record_date` |日期 |记录日期|
| `index_ratio` |数量 | TIPS调整指数比例|
| `ref_cpi` |数量 |参考CPI值|

- --

## FRN每日指数

* *端点：** `/v1/accounting/od/frn_daily_indexes` 
* *频率：**每日
* *日期范围：** 2024年4月至今

国债浮动利率票据（FRN）的每日指数值。该利率基于 13 周国库券拍卖利率。

- --

## 国债认证利率

四个认证周期，每个周期都有自己的端点集：

### 年度认证
* *频率：**年度
* *日期范围：**2006年10月至今（9个数据表）

### 每月认证 
* *频率：** 每月 
* *日期范围：** 2006 年 10 月至今（6 个数据表）

### 季度认证
* *频率：** 每季度 
* *日期范围：** 2006 年 10 月至目前（4 个数据表）

### 半年度认证
* *频率：** 半年度 
* *日期范围：** 2008 年 1 月至今（1 个数据表）

 这些认证利率用于联邦贷款、融资计划和其他需要官方财政部认证的目的rates.

- --

## 联邦信贷类似到期利率

* *端点：** `/v1/accounting/od/fed_credit_similar_maturity_rates` 
* *频率：** 年度 
* *日期范围：** 1992 年 9 月至今

 用于评估联邦信贷计划（贷款和贷款）的利率

- --

## 历史合格税收抵免债券利率

* *频率：** 每日（已停止） 
* *日期范围：** 2009 年 3 月 – 2018 年 1 月

H 合格税收抵免债券 (QTCB)的历史利率。不再更新。

- --

## 州和地方政府系列 (SLGS)每日利率表

* *端点：** `/v1/accounting/od/slgs_savings_bonds`（2 个表） 
* *频率：** 每日 
* *日期范围：** 1992 年 6 月至今

 州和地方政府系列证券的每日利率，州和地方发行人用于遵守联邦税法套利限制.
