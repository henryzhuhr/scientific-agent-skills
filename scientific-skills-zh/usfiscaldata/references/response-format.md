# 响应格式 — 美国财政部财政数据 API

## 响应结构 (JSON)

```json
{
  "data": [
    {
      "record_date": "2024-03-31",
      "tot_pub_debt_out_amt": "34589629941.12"
    }
  ],
  "meta": {
    "count": 100,
    "labels": {
      "record_date": "Record Date",
      "tot_pub_debt_out_amt": "Total Public Debt Outstanding"
    },
    "dataTypes": {
      "record_date": "DATE",
      "tot_pub_debt_out_amt": "CURRENCY"
    },
    "dataFormats": {
      "record_date": "YYYY-MM-DD",
      "tot_pub_debt_out_amt": "10.2"
    },
    "total-count": 3790,
    "total-pages": 38
  },
  "links": {
    "self": "&page%5Bnumber%5D=1&page%5Bsize%5D=100",
    "first": "&page%5Bnumber%5D=1&page%5Bsize%5D=100",
    "prev": null,
    "next": "&page%5Bnumber%5D=2&page%5Bsize%5D=100",
    "last": "&page%5Bnumber%5D=38&page%5Bsize%5D=100"
  }
}
```

## `meta` Object

|领域 |描述 |
|-------|--------------|
| `count` |此响应页中的记录数 |
| `total-count` |与查询匹配的总记录数（所有页）|
| `total-pages` |当前页面大小下可用的总页数|
| `labels` |人类可读的列标签 |
| `dataTypes` |逻辑数据类型：`STRING`、`NUMBER`、`DATE`、`CURRENCY`、`INTEGER`、`PERCENTAGE` |
| `dataFormats` |格式提示：`YYYY-MM-DD`、`10.2`（10 位数字，2 位小数）、`String` |

## `links` 对象

使用 `links` 对象以编程方式导航分页：

|领域 |值 |
|-------|--------|
| `self` |当前页查询参数|
| `first` |首页|
| `prev` |上一页（如果在第一页则为空）|
| `next` |下一页（如果在最后一页则为空）|
| `last` |最后一页|

## `data` 对象

行对象的数组。所有值都是 **字符串**，无论逻辑类型如何。

## 响应代码

|代码|含义 |
|------|---------|
| 200 | 200 OK — 成功 GET |
| 304 | 304未修改 — 缓存响应 |
| 400 |错误请求 — URL 格式错误或参数无效 |
| 403 | 403禁止 — 无效的 API 密钥（不适用；无需密钥）|
| 404 | 404未找到 — 端点不存在 |
| 405 | 405不允许的方法 — 非 GET 请求 |
| 429 | 429请求过多 — 速率受限 |
| 500 | 500内部服务器错误 |

## 错误对象

发生错误时，响应中包含错误对象，而不是 `data`：

```json
{
  "error": "Invalid Query Param",
  "message": "Invalid query parameter 'sorts' with value '[-record_date]'. For more information please see the documentation."
}
```

```python
resp = requests.get(url, params=params)
result = resp.json()

if "error" in result:
    print(f"API Error: {result['error']}")
    print(f"Message: {result['message']}")
elif resp.status_code != 200:
    print(f"HTTP {resp.status_code}: {resp.text}")
else:
    data = result["data"]
```

## 常见错误原因

- `fields=` 参数中的字段名称无效
- 过滤器运算符无效（使用 `eq`、`gte`、`lte`、`gt`、`lt`、`in`）
- 日期格式错误（必须是`YYYY-MM-DD`)
- 在 URL 中使用 `/v1/` 访问 v2 端点
- `sort` 字段在端点中不可用

## 解析响应

```python
import requests
import pandas as pd

def api_to_dataframe(endpoint, params=None):
    """Fetch API data and return a typed DataFrame."""
    base = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"
    resp = requests.get(f"{base}{endpoint}", params=params)
    resp.raise_for_status()
    result = resp.json()
    
    df = pd.DataFrame(result["data"])
    meta = result["meta"]
    
    # Apply type conversions using metadata
    for col, dtype in meta["dataTypes"].items():
        if col not in df.columns:
            continue
        if dtype in ("NUMBER", "CURRENCY", "PERCENTAGE"):
            df[col] = pd.to_numeric(df[col].replace("null", None), errors="coerce")
        elif dtype == "DATE":
            df[col] = pd.to_datetime(df[col].replace("null", None), errors="coerce")
        elif dtype == "INTEGER":
            df[col] = pd.to_numeric(df[col].replace("null", None), errors="coerce").astype("Int64")
    
    return df, meta

# Usage
df, meta = api_to_dataframe(
    "/v2/accounting/od/debt_to_penny",
    params={"sort": "-record_date", "page[size]": 30}
)
print(f"Total records available: {meta['total-count']}")
print(df[["record_date", "tot_pub_debt_out_amt"]].head())
```

## CSV 格式响应

当指定`format=csv`时，响应正文为纯CSV文本（不是JSON）：

```python
import io

resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny",
    params={"format": "csv", "sort": "-record_date", "page[size]": 100}
)
df = pd.read_csv(io.StringIO(resp.text))
```

## XML格式响应

当指定`format=xml`时，响应正文为XML：

```python
import xml.etree.ElementTree as ET

resp = requests.get(
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny",
    params={"format": "xml", "page[size]": 10}
)
root = ET.fromstring(resp.text)
```
