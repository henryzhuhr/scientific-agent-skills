# 世界银行开放数据 API

## 基本 URL

```
https://api.worldbank.org/v2
```

## 身份验证

* *无需 API 密钥。** API 完全开放。

## 关键端点

### 1. 获取国家/地区的指标数据
```
GET /country/{country_code}/indicator/{indicator_code}
```
|参数|必填 |描述 |
|-----------|----------|--------------------------------------------------------|
|格式|没有 | `json`、`xml`（默认）、`jsonP` |
|日期 |没有 |年份范围：`2010:2023`，单年份：`2020` |
|页 |没有 |页码（默认1）|
|每页 |没有 |每页结果（默认 50，最大 32500）|
|机读签证 |没有 |最新值：最近数据点的数量 |
|填补缺口|没有 | `Y` 用最新值填补空白|
|频率|没有 | `M`（每月）、`Q`（每季）、`Y`（每年）|
|来源 |没有 |源 ID 号 |

 示例（美国 GDP，2015-2023 年）：
```
https://api.worldbank.org/v2/country/US/indicator/NY.GDP.MKTP.CD?format=json&date=2015:2023
```

 示例（最近 5 个值）：
```
https://api.worldbank.org/v2/country/US/indicator/NY.GDP.MKTP.CD?format=json&MRV=5
```

### 2. 获取多个指标数据国家
```
GET /country/{code1};{code2};{code3}/indicator/{indicator_code}
```
示例：
```
https://api.worldbank.org/v2/country/US;GB;CN;IN/indicator/SP.POP.TOTL?format=json&date=2020:2023
```

### 3. 获取所有国家的指标数据
```
GET /country/all/indicator/{indicator_code}
```
示例：
```
https://api.worldbank.org/v2/country/all/indicator/SI.POV.DDAY?format=json&date=2020&per_page=300
```

### 4. 获取指标数据按地区/收入组
```
GET /country/{aggregate_code}/indicator/{indicator_code}
```
聚合代码：`EAS`（东亚）、`ECS`（欧洲和中亚）、`LIC`（低收入）、`HIC`（高收入）、`WLD`（世界）、等

示例：
```
https://api.worldbank.org/v2/country/WLD/indicator/NY.GDP.MKTP.CD?format=json&date=2020:2023
```

### 5. 列出所有国家/地区
```
GET /country
```
示例：
```
https://api.worldbank.org/v2/country?format=json&per_page=300
```

### 6. 获取国家/地区信息
```
GET /country/{country_code}
```
示例：
```
https://api.worldbank.org/v2/country/US?format=json
```

### 7. 列出所有指标
```
GET /indicator
```
示例：
```
https://api.worldbank.org/v2/indicator?format=json&per_page=100
```

### 8. 搜索指标
```
GET /indicator
```
直接在URL路径中使用查询字符串或按主题/来源过滤。

按主题：
```
https://api.worldbank.org/v2/topic/3/indicator?format=json
```

按来源：
```
https://api.worldbank.org/v2/source/2/indicator?format=json&per_page=50
```

### 9. 列表主题
```
GET /topic
```
示例：
```
https://api.worldbank.org/v2/topic?format=json
```

### 10. 列出源
```
GET /source
```
示例：
```
https://api.worldbank.org/v2/source?format=json
```

## 常用指标代码

|指标代码|说明 |
|------------------------------------------------|----------------------------------------------------------------|
|纽约.GDP.MKTP.CD | GDP（现价美元）|
| NY.GDP.MKTP.KD.ZG | GDP增长（年百分比）|
|纽约.GDP.PCAP.CD |人均GDP（现价美元）|
| NY.GDP.PCAP.PP.CD |人均 GDP，购买力平价（现价国际美元）|
| SP.POP.TOTL |总人口|
| SP.POP.GROW |人口增长（年百分比）|
| SP.DYN.LE00.IN |出生时预期寿命（岁）|
| SP.DYN.TFRT.IN |生育率（每个女性的生育数）|
| SL.UEM.TOTL.ZS |失业率（占劳动力总数的百分比）|
| FP.CPI.TOTL.ZG |通货膨胀，消费者价格（年度百分比）|
| SI.POV.DDAY |贫困人数为 2.15 美元/天（占人口的百分比）|
| SI.POV.基尼|基尼指数|
| BX.KLT.DINV.CD.WD |外国直接投资净流入（国际收支平衡，美元）|
| NE.EXP.GNFS.ZS |商品和服务出口（占 GDP 的百分比）|
| EN.ATM.CO2E.PC |二氧化碳排放量（人均吨）|
| SE.ADT.LITR.ZS |成人识字率（15 岁以上的百分比）|
| SH.XPD.CHEX.PC.CD |当前人均卫生支出（美元）|
| IT.NET.USER.ZS |使用互联网的个人（占人口的百分比） |

## 通用国家/地区代码 (ISO 3166-1 alpha-2)

`US`（美国）、`GB`（英国）、`CN`（中国）、`IN`（印度）、`JP`（日本）、`DE`（德国）、`FR`（法国）、`BR`（巴西）、 `ZA`（南非）、`NG`（尼日利亚）、`AU`（澳大利亚）、`CA`（加拿大）

## 响应格式

* *重要：** JSON 响应作为 **二元素数组** 返回。第一个元素是分页元数据；第二个是数据数组。

### 指标观测值
```json
[
  {
    "page": 1,
    "pages": 1,
    "per_page": 50,
    "total": 9,
    "sourceid": "2",
    "lastupdated": "2024-03-28"
  },
  [
    {
      "indicator": {
        "id": "NY.GDP.MKTP.CD",
        "value": "GDP (current US$)"
      },
      "country": {
        "id": "US",
        "value": "United States"
      },
      "countryiso3code": "USA",
      "date": "2023",
      "value": 27360935000000,
      "unit": "",
      "obs_status": "",
      "decimal": 0
    },
    {
      "indicator": { "id": "NY.GDP.MKTP.CD", "value": "GDP (current US$)" },
      "country": { "id": "US", "value": "United States" },
      "countryiso3code": "USA",
      "date": "2022",
      "value": 25462700000000,
      "unit": "",
      "obs_status": "",
      "decimal": 0
    }
  ]
]
```

注：当该年数据不可用时，`value` 为 `null`。

### 国家信息
```json
[
  { "page": 1, "pages": 1, "per_page": 50, "total": 1 },
  [
    {
      "id": "US",
      "iso2Code": "US",
      "name": "United States",
      "region": { "id": "NAC", "iso2code": "XU", "value": "North America" },
      "adminregion": { "id": "", "iso2code": "", "value": "" },
      "incomeLevel": { "id": "HIC", "iso2code": "XD", "value": "High income" },
      "lendingType": { "id": "LNX", "iso2code": "XX", "value": "Not classified" },
      "capitalCity": "Washington D.C.",
      "longitude": "-77.032",
      "latitude": "38.8895"
    }
  ]
]
```

## 汇率限制

 - 未发布正式的速率限制； API 是开放且慷慨的。
- 对于批量下载，请使用 `per_page=32500` 来最大程度地减少请求。
- 请尊重：自动化脚本每秒 1-2 个请求。
- 对于非常大的数据集，请考虑世界银行批量下载工具。

## 注释

- 始终包括`format=json` -- 默认为 XML。
- 默认按 **降序** 日期顺序返回结果。
- `null` 值常见于近年来（数据尚未发布）或覆盖稀疏的指标。
- 分页：检查元数据中的 `pages`；迭代 `page=1`、`page=2` 等。
  - 国家/地区代码在 URL 路径中遵循 ISO 3166-1 alpha-2（2 个字母）。响应还包括 `countryiso3code`.
