# API 基础知识 — 美国财政部财政数据

## 概述

- RESTful API — 仅接受 HTTP GET 请求
- 默认返回 JSON（也可以是 CSV、XML）
- 无 API 密钥，无需身份验证，无需注册
- 开放数据，免费用于商业和非商业用途
- 当前版本：v1 和 v2（检查每个数据集的页面适用哪个版本）

## URL 结构

```
BASE URL + ENDPOINT + PARAMETERS

Base URL:  https://api.fiscaldata.treasury.gov/services/api/fiscal_service
Endpoint:  /v2/accounting/od/debt_to_penny
Params:    ?fields=record_date,tot_pub_debt_out_amt&sort=-record_date&page[size]=5

Full URL:
https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny?fields=record_date,tot_pub_debt_out_amt&sort=-record_date&page[size]=5
```

- 端点组件使用小写+下划线
- 端点名称为单数

## API 版本控制

- **v1**：早期数据集（DTS、 MTS，一些债务表）
- **v2**：较新或更新的数据集（对 Penny 的债务、TROR、平均利率）
- 检查 `fiscaldata.treasury.gov/datasets/` 上的特定数据集页面以确认版本

## 数据类型

响应中的所有字段值都是 **字符串**（带引号），无论其逻辑如何型号.

|逻辑类型 |数据类型值 |示例值 |如何转换 |
|---|---|---|---|
|字符串| `STRING` | `"Canada-Dollar"` |无需转换|
|数量 | `NUMBER` | `"36123456789012.34"` | `float(value)` |
|日期 | `DATE` | `"2024-03-31"` | `pd.to_datetime(value)` |
|货币 | `CURRENCY` | `"1234567.89"` | `float(value)` |
|整数 | `INTEGER` | `"42"` | `int(value)` |
|百分比 | `PERCENTAGE` | `"4.25"` | `float(value)` |

* *空值**显示为字符串 `"null"`（不是 Python `None` 或 JSON `null`）。

```python
# Safe numeric conversion handling nulls
def safe_float(val):
    return float(val) if val and val != "null" else None
```

## HTTP 方法

- **仅 GET 是支持**
- POST、PUT、DELETE 返回 HTTP 405

## 速率限制

- 速率受限时返回 HTTP 429
- 没有记录的固定速率限制；对批量请求实施回退重试

```python
import time
import requests

def get_with_retry(url, params, retries=3):
    for attempt in range(retries):
        resp = requests.get(url, params=params)
        if resp.status_code == 429:
            time.sleep(2 ** attempt)
            continue
        resp.raise_for_status()
        return resp.json()
    raise Exception("Rate limited after retries")
```

## 缓存

- 可以为缓存响应返回HTTP 304（未修改）
- 可以安全地缓存响应；大多数数据集每天、每月或每季度更新

## 数据注册表

[财政服务数据注册表](https://fiscal.treasury.gov/data-registry/index.html)包含联邦政府数据的字段定义、权威来源、数据类型和格式。
