# 证券和储蓄债券数据集 — 美国国债财政数据

## 国债拍卖数据

* *端点：** `/v1/accounting/od/auctions_query` 
* *频率：** 根据需要 
* *日期范围：** 1979 年 11 月至今

H国债拍卖的历史数据，包括票据、票据、债券、TIPS 和 FRN。

* *关键字段：**
|领域 |类型 |描述 |
|--------|------|-------------|
| `record_date` |日期 |拍卖日期|
| `security_type` |字符串 |票据、票据、债券、小费、FRN |
| `security_term` |字符串 |例如，“4 周”、“2 年”、“10 年”|
| `cusip` |字符串 | CUSIP 标识符 |
| `offering_amt` |货币 |提供金额|
| `accepted_comp_bid_rate_amt` |百分比|高接受竞争性出价|
| `bid_to_cover_ratio` |数量 |投标覆盖率|
| `total_accepted_amt` |货币 |受理总额|
| `indirect_bid_pct_accepted` |百分比|间接投标人百分比|
| `issue_date` |日期 |发行/结算日期|
| `maturity_date` |日期 |到期日 |

```python
# Get recent 10-year Treasury note auctions
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query",
    params={
        "filter": "security_type:eq:Note,security_term:eq:10-Year",
        "sort": "-record_date",
        "page[size]": 10
    }
)
df = pd.DataFrame(resp.json()["data"])

# Get all auctions in 2024
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query",
    params={
        "filter": "record_date:gte:2024-01-01,record_date:lte:2024-12-31",
        "sort": "-record_date",
        "page[size]": 10000
    }
)
```

## 国债即将拍卖

* *端点：** `/v1/accounting/od/upcoming_auctions` 
* *频率：** 根据需要 
* *日期范围：** 2024 年 3 月至今

 已公布但尚未确定拍卖时间表。

* *关键字段：**
|领域 |类型 |描述 |
|--------|------|-------------|
| `auction_date` |日期 |预定拍卖日期|
| `security_type` |字符串 |安全型|
| `security_term` |字符串 |到期期限|
| `offering_amt` |货币 |公布发行金额 |

```python
# Get upcoming auctions
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/upcoming_auctions",
    params={"sort": "auction_date"}
)
upcoming = pd.DataFrame(resp.json()["data"])
print(upcoming[["auction_date", "security_type", "security_term", "offering_amt"]])
```

## 创纪录的国债拍卖数据

* *频率：** 根据需要

跟踪每种证券类型和期限的拍卖记录（最大、最高利率、最低利率等）。

## 国债回购

* *频率：** 根据需要（2 个数据表） 
* *日期范围：** 2000 年 3 月至今

有关财政部二级市场回购（回购）操作的数据。自该计划于 2024 年重新启动以来一直有效。

- --

## I 债券利率

* *端点：** `/v2/accounting/od/i_bond_interest_rates` 
* *频率：**半年一次（5 月和 11 月） 
* *日期范围：** 1998 年 9 月至目前

系列I储蓄债券的综合利率，包括固定利率和通货膨胀率部分。

* *关键字段：**
|领域 |类型 |描述 |
|--------|------|-------------|
| `effective_date` |日期 |汇率生效日期|
| `announcement_date` |日期 |公告日期|
| `fixed_rate` |百分比|固定利率组件|
| `semiannual_inflation_rate` |百分比|半年CPI-U通胀率|
| `earnings_rate_i_bonds` |百分比|综合综合利率 |

```python
# Current I Bond rates
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/i_bond_interest_rates",
    params={"sort": "-effective_date", "page[size]": 5}
)
df = pd.DataFrame(resp.json()["data"])
latest = df.iloc[0]
print(f"Current I Bond rate: {latest['earnings_rate_i_bonds']}%")
print(f"  Fixed rate: {latest['fixed_rate']}%")
print(f"  Inflation component: {latest['semiannual_inflation_rate']}%")
```

## 美国国库储蓄债券：发行、赎回和到期

* *端点：** `/v1/accounting/od/sb_issues_redemptions`（3 个表） 
* *频率：** 每月 
* *日期范围：** 九月1998年至今

 EE系列、I系列和HH系列储蓄债券未偿还、发行和赎回的月度统计。

* *关键字段：**
|领域 |类型 |描述 |
|--------|------|-------------|
| `record_date` |日期 |月结束日期 |
| `series_cd` |字符串 |邦德系列（EE、I、HH）|
| `issued_amt` |货币 |发行数量|
| `redeemed_amt` |货币 |赎回金额|
| `matured_amt` |货币 |到期金额|
| `outstanding_amt` |货币 |未偿总额 |

## 储蓄债券价值文件

* *频率：** 每半年一次 
* *日期范围：** 1992 年 5 月至今

用于计算当前储蓄债券赎回价值的文件。

## 应计储蓄债券赎回表（已停产）

* *端点：** `/v2/accounting/od/redemption_tables` 
* *频率：** 停产（最后更新于 2022 年） 
* *日期范围：** 1999 年 3 月 – 2023 年 5 月

 历史储蓄债券的每月赎回价值表。

## 储蓄债券出售证券（已停止）

* *频率：**已停止 
* *日期范围：** 1998 年 10 月 – 2022 年 6 月

- --

## 州和地方政府系列 (SLGS)证券

* *端点：** `/v1/accounting/od/slgs_statistics` 
* *频率：**每日 
* *日期范围：** 1998 年 10 月至今 

SLGS 证券流通数据 — 出售给州和地方政府的不可流通特殊目的证券。

## 每月州和地方政府系列 (SLGS)证券计划

* *频率：** 每月 
* *日期范围：** 2014 年 3 月至今 

 SLGS 计划的月度统计。

- --

## 电子证券交易

* *频率：** 每月（8 个数据表） 
* *日期范围：** 2000 年 1 月至今

 TRADES（国库/储备金自动债务录入系统）系统。

- --

## 联邦投资计划

### 基金利息成本
* *频率：** 每月 
* *日期范围：** 2001 年 10 月至今

 政府信托每月利息成本

### 本金未偿
* *频率：** 每月（2 个表） 
* *日期范围：** 2017 年 10 月至今

### 账户报表
* *频率：** 每月（3 个表） 
* *日期范围：** 11 月2011 年至今

- --

## 联邦借款计划

### 分配和交易数据
* *频率：** 每日（2 个表） 
* *日期范围：** 2000 年 9 月至今

### 未投资利息资金
* *频率：**每季度 
* *日期范围：** 2016 年 12 月至今

### 总账余额报告汇总
* *频率：**每月（2 个表） 
* *日期范围：** 2005 年 10 月至今
