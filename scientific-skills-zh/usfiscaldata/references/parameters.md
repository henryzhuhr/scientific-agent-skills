# 查询参数 — 美国财政部财政数据 API

所有参数都是可选的。将它们与 URL 查询字符串中的 `&` 组合。

## `fields=` — 选择列

仅返回指定字段。接受以逗号分隔的字段名称列表。

```
?fields=record_date,tot_pub_debt_out_amt
?fields=country_currency_desc,exchange_rate,record_date
```

- 如果省略，则返回所有字段
- 无效的字段名称会导致错误
- 省略某些字段可以触发**自动聚合**（见下文）

### 聚合/自动求和

当`fields=` 参数排除一些非数字字段，API 自动按剩余字段进行分组并对数值求和。

```python
# Returns sum of transaction amounts grouped by record_date and transaction_type
params = {
    "fields": "record_date,transaction_type,transaction_today_amt"
}
```

## `filter=` — 过滤记录

按字段值缩小结果范围。多个字段过滤器**在单个 `filter=` 参数中以逗号分隔**。

### 过滤器语法

```
filter=<field>:<operator>:<value>
filter=<field>:<operator>:<value>,<field>:<operator>:<value>
```

### 运算符

|操作员|意义|示例 |
|----------|---------|---------|
| `eq` |等于 | `filter=record_date:eq:2024-03-31` |
| `lt` |小于| `filter=exchange_rate:lt:1.5` |
| `lte` |小于或等于 | `filter=record_date:lte:2024-12-31` |
| `gt` |大于 | `filter=record_fiscal_year:gt:2010` |
| `gte` |大于或等于| `filter=record_date:gte:2024-01-01` |
| `in` |包含在套装中 | `filter=country_currency_desc:in:(Canada-Dollar,Mexico-Peso)` |

### 日期过滤器

使用 `YYYY-MM-DD` 格式的日期：

```
filter=record_date:gte:2024-01-01
filter=record_date:gte:2023-01-01,record_date:lte:2023-12-31
```

### 多字段过滤器

```
filter=country_currency_desc:in:(Canada-Dollar,Mexico-Peso),record_date:gte:2024-01-01
```

### 通用过滤器字段

大多数端点具有以下标准日期字段：
- `record_date` — 记录日期 (YYYY-MM-DD)
- `record_fiscal_year` — 会计年度（例如，`2024`）
- `record_fiscal_quarter` — 财政季度 (1-4)
- `record_calendar_year` — 日历年
- `record_calendar_month` — 日历月 (01-12)

## `sort=` — 对结果进行排序

按一个或多个字段排序。前缀 `-` 为降序。

```
?sort=-record_date           # Most recent first
?sort=record_date            # Oldest first
?sort=-record_fiscal_year,-record_fiscal_quarter  # Nested sort
```

* *默认：** 按第一列排序（通常为 `record_date` 升序）。

## `format=` — 输出格式

```
?format=json    # Default
?format=csv     # Comma-separated values
?format=xml     # XML
```

使用 CSV 或 XML 格式时，响应是原始文件内容而不是 JSON。`format=`## `page[size]=` 和 `page[number]=` — 分页

控制每页有多少条记录以及显示哪一页return.

```
?page[size]=100&page[number]=1    # Default (100 records, page 1)
?page[size]=10000                  # Large page to reduce requests
?page[number]=5&page[size]=50     # 50 records starting at page 5
```

- 默认页面大小：**100**
- 默认页码：**1**
- 在响应中使用 `meta.total-pages` 来了解存在多少页
- 使用 `meta.total-count` 获取总记录数

### Fetch所有记录

```python
import requests
import pandas as pd

def fetch_all(endpoint, params=None):
    """Fetch all pages and return as DataFrame."""
    params = dict(params or {})
    params["page[size]"] = 10000
    params["page[number]"] = 1
    
    base = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"
    all_data = []
    
    while True:
        resp = requests.get(f"{base}{endpoint}", params=params)
        result = resp.json()
        all_data.extend(result["data"])
        
        meta = result["meta"]
        if params["page[number]"] >= meta["total-pages"]:
            break
        params["page[number]"] += 1
    
    return pd.DataFrame(all_data)
```

## 组合参数

```python
params = {
    "fields": "country_currency_desc,exchange_rate,record_date",
    "filter": "country_currency_desc:in:(Canada-Dollar,Euro),record_date:gte:2020-01-01",
    "sort": "-record_date",
    "format": "json",
    "page[size]": 100,
    "page[number]": 1
}
resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/rates_of_exchange",
    params=params
)
```
