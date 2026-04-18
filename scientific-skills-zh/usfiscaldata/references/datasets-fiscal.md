# 财政报表数据集——美国财政部财政数据

## 每日财政报表(DTS)

DTS数据集有**9个数据表**，全部位于`/v1/accounting/dts/`下。每日更新（工作日）。

* *日期范围：** 2005 年 10 月至今

### DTS 表

|表|端点|描述 |
|-------|---------|------------|
|经营现金余额| `/v1/accounting/dts/operating_cash_balance` |国库一般账户余额|
|存款和取款 | `/v1/accounting/dts/deposits_withdrawals_operating_cash` | TGA 的变更 |
|公共债务交易| `/v1/accounting/dts/public_debt_transactions` |证券的发行和赎回|
|公共债务调整| `/v1/accounting/dts/adjustment_public_debt_transactions_cash_basis` |收付实现制调整|
|债务受限制| `/v1/accounting/dts/debt_subject_to_limit` |债务与法定限额|
|机构间税收转移| `/v1/accounting/dts/inter_agency_tax_transfers` |政府内部税收转移|
|联邦税存款| `/v1/accounting/dts/federal_tax_deposits` |缴税活动|
|短期现金投资| `/v1/accounting/dts/short_term_cash_investments` |现金投资活动|
|已发放所得税退税 | `/v1/accounting/dts/income_tax_refunds_issued` |退税开具|

### 常见DTS字段

|领域 |类型 |描述 |
|--------|------|-------------|
| `record_date` |日期 |营业日期|
| `account_type` |字符串 |账户/余额类型|
| `open_today_bal` |货币 |期初余额|
| `open_month_bal` |货币 |期初余额|
| `open_fiscal_year_bal` |货币 |期初会计年度余额|
| `close_today_bal` |货币 |期末余额|
| `transaction_today_amt` |货币 |今日成交金额|
| `transaction_mtd_amt` |货币 |本月至今金额 |
| `transaction_fytd_amt` |货币 |财政年度至今金额 |

```python
# Get current Treasury General Account (TGA) balance
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance",
    params={"sort": "-record_date", "page[size]": 5}
)
for row in resp.json()["data"]:
    print(f"{row['record_date']}: ${float(row['close_today_bal']):,.0f}M (closing balance)")

# Get deposits and withdrawals for a specific period
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/deposits_withdrawals_operating_cash",
    params={
        "filter": "record_date:gte:2024-01-01,record_date:lte:2024-01-31",
        "sort": "record_date",
        "page[size]": 1000
    }
)
```

### 聚合示例 (DTS)

```python
# Get sum of today's transaction amounts by transaction type
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/deposits_withdrawals_operating_cash",
    params={
        "fields": "record_date,transaction_type,transaction_today_amt",
        "filter": "record_date:eq:2024-01-15"
    }
)
```

- --

## 月度财务报表 (MTS)

MTS 数据集有 **16 个数据表**，全部位于`/v1/accounting/mts/`。每月更新。

* *日期范围：** 1980 年 10 月至今

### MTS 表

|表|端点|说明 |
|--------|----------|------------|
| MTS 表 1 | `/v1/accounting/mts/mts_table_1` |收入和支出汇总|
| MTS 表 2 | `/v1/accounting/mts/mts_table_2` |收据来源 |
| MTS 表 3 | `/v1/accounting/mts/mts_table_3` |按功能划分的支出 |
| MTS 表 4 | `/v1/accounting/mts/mts_table_4` |按机构支出 |
| MTS 表 5 | `/v1/accounting/mts/mts_table_5` |按类别支出|
| MTS 表 6 | `/v1/accounting/mts/mts_table_6` |融资方式|
| MTS 表 7 | `/v1/accounting/mts/mts_table_7` |按来源划分的收款（季度）|
| MTS 表 8 | `/v1/accounting/mts/mts_table_8` |按功能划分的支出（季度）|
| MTS 表 9 | `/v1/accounting/mts/mts_table_9` |收据：比较总结|
| MTS 表 10 | `/v1/accounting/mts/mts_table_10` |支出：比较摘要|
| MTS 表 11 | `/v1/accounting/mts/mts_table_11` |收据补充详细信息|
| MTS 表 12 | `/v1/accounting/mts/mts_table_12` |支出补充详细信息|
| MTS 表 13 | `/v1/accounting/mts/mts_table_13` |联邦借款和债务|
| MTS 表 14 | `/v1/accounting/mts/mts_table_14` |融资方式：联邦|
| MTS 表 15 | `/v1/accounting/mts/mts_table_15` |联邦信托基金摘要|
| MTS 表 16 | `/v1/accounting/mts/mts_table_16` |融资方式：预算外 |

### 通用 MTS 字段

|领域 |类型 |描述 |
|--------|------|-------------|
| `record_date` |日期 |月结束日期|
| `record_fiscal_year` |字符串 |财政年度（10 月至 9 月）|
| `record_fiscal_quarter` |字符串 |财政季度 (1–4) |
| `classification_desc` |字符串 |行项目描述 |
| `classification_id` |字符串 |行项目代码 |
| `parent_id` |字符串 |父分类ID |
| `current_month_gross_rcpt_amt` |货币 |当月总收入|
| `current_fytd_gross_rcpt_amt` |货币 |财政年度迄今总收入|
| `prior_fytd_gross_rcpt_amt` |货币 |上一财年至今 |

```python
# MTS Table 1: Summary of receipts and outlays
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_1",
    params={
        "filter": "record_fiscal_year:eq:2024",
        "sort": "record_date"
    }
)
df = pd.DataFrame(resp.json()["data"])

# MTS Table 9: Get line 120 (Total Receipts) for most recent period
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_9",
    params={
        "filter": "line_code_nbr:eq:120",
        "sort": "-record_date",
        "page[size]": 1
    }
)
```

- --

## 美国政府税收

* *端点：** `/v1/accounting/od/rev_collections` 
* *频率：** 每日 
* *日期范围：** 2004 年 10 月赠送

每日税收和非税收入征收。

- --

## 美国政府财务报告

* *端点：**（8个表）
* *频率：**年度
* *日期范围：**1995年9月至今（2024财年最新）

年度经审计的财务报表。包括：
- 资产负债表
- 净成本表
- 运营报表
- 净头寸变动表

- --

## 每月国库支出

* *频率：** 每月 
* *日期范围：** 十月2013 年至今

 每月联邦支出数据。

- --

## 按部门划分的收据

* *端点：** `/v2/accounting/od/receipts_by_dept` 
* *频率：** 年度 
* *日期范围：** 2015 年 9 月至目前

按部门划分的联邦收入年度明细。

- --

## 国库管理账户

* *频率：**季度 
* *日期范围：** 2022年12月至今（3个数据表）

国库管理信托和特别基金账户data.

- --

## 财政部公报

* *频率：**季度 
* *日期范围：** 2021年3月至今（13张表）

季度财务报告，涵盖政府财政、公共债务、储蓄债券等。

* *端点前缀：** `/v1/accounting/od/treasury_bulletin_`
