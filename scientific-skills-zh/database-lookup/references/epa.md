# EPA Envirofacts API 参考

## 基本 URL
```
https://data.epa.gov/efservice
```

注意：旧 URL `https://enviro.epa.gov/enviro/efservice` 可能会重定向。使用上面的当前基本 URL。

## 身份验证
* *不需要。** 完全公开，不需要 API 密钥。

## 速率限制
- 没有记录的每用户速率限制。
- 大型结果集可能会超时。使用行限制和分页。

## URL Pattern
Envirofacts 使用基于 RESTful URL 的查询模式：
```
https://data.epa.gov/efservice/{table}/{column}/{operator}/{value}/.../rows/{start}:{end}/{format}
```

- **{table}**：数据库表名称（例如 `TRI_FACILITY`、`AQS_SITES`）。
- **{column}/{operator}/{value}**：过滤条件，链接在URL路径中。
- **运算符**：`=`（隐式，只需使用`/{column}/{value}`），`>`，`<`，`!=`，`BEGINNING`（开头）， `CONTAINING`.
- **rows/{start}:{end}**：分页的行范围（从0开始）。
- **{格式}**：`JSON`、`XML`、`CSV`、`EXCEL`。作为最后一个路径段附加。

* *多个过滤器**在 URL 路径中按顺序链接。

- --

## 关键数据库和表

### 1. 有毒物质释放清单 (TRI)

跟踪工业设施中有毒化学品的释放。

* *关键表格：**
|表|描述 |
|--------|--------------|
| `TRI_FACILITY` |设施信息（名称、地址、坐标）。 |
| `TRI_REPORTING_FORM` |年度报告表数据。 |
| `TRI_RELEASE_QTY` |介质（空气、水、陆地）的释放量。 |
| `TRI_TRANSFER_QTY` |异地转移的数量。 |
| `TRI_CHEM_INFO` |化学信息。 |

* *示例 - 北卡罗来纳州的 TRI 设施：**
```
https://data.epa.gov/efservice/TRI_FACILITY/STATE_ABBR/NC/rows/0:9/JSON
```

* *响应：**
```json
[
  {
    "TRI_FACILITY_ID": "27601MPLNT501WE",
    "FACILITY_NAME": "EXAMPLE MANUFACTURING PLANT",
    "STREET_ADDRESS": "501 WEST MAIN ST",
    "CITY_NAME": "RALEIGH",
    "COUNTY_NAME": "WAKE",
    "STATE_ABBR": "NC",
    "ZIP_CODE": "27601",
    "LATITUDE": 35.7796,
    "LONGITUDE": -78.6382,
    "FEDERAL_FACILITY_FLAG": "NO",
    "INDUSTRY_SECTOR_CODE": "325",
    "PRIMARY_SIC_CODE": "2819",
    "PRIMARY_NAICS_CODE": "325180"
  }
]
```

* *示例 - 某个州特定化学品的 TRI 释放(2022):**
```
https://data.epa.gov/efservice/TRI_RELEASE_QTY/STATE_ABBR/TX/REPORTING_YEAR/2022/CHEM_NAME/CONTAINING/BENZENE/rows/0:24/JSON
```

### 2.空气质量系统(AQS)

来自国家监测网的空气质量监测数据。

* *关键表：**
|表|描述 |
|-------|--------------|
| `AQS_SITES` |监控站点元数据。 |
| `AQS_MONITORS` |监视器级信息（测量的参数）。 |
| `AQS_ANNUAL_SUMMARY` |每个监视器的年度汇总统计数据。 |
| `AQS_DAILY_SUMMARY` |每日总结观察。 |

* *示例 -- 加利福尼亚州的 AQS 监测点：**
```
https://data.epa.gov/efservice/AQS_SITES/STATE_CODE/06/rows/0:9/JSON
```

 * *示例 -- 某个县的年度臭氧汇总：**
```
https://data.epa.gov/efservice/AQS_ANNUAL_SUMMARY/STATE_CODE/06/COUNTY_CODE/037/PARAMETER_CODE/44201/rows/0:9/JSON
```

 * *常用 AQS 参数代码：**
|代码|污染物|
|--------|-----------|
| `44201` |臭氧|
| `42401` | SO2 |
| `42101` |二氧化碳|
| `42602` | NO2 |
| `81102` | PM10 |
| `88101` | PM2.5（FRM）|
| `88502` | PM2.5（非FRM）|
| `14129` |铅 (Pb) |

### 3. 设施注册服务 (FRS)

EPA 监管设施的中央注册。

* *关键表：**
|表|描述 |
|--------|--------------|
| `FRS_FACILITY_SITE` |设施位置和标识符。 |
| `FRS_PROGRAM_FACILITY` |将设施与 EPA 计划联系起来。 |
| `FRS_NAICS` |设施的 NAICS 代码。 |
| `FRS_SIC` |设施的 SIC 代码。 |

* *示例 -- 按邮政编码列出的 EPA 监管设施：**
```
https://data.epa.gov/efservice/FRS_FACILITY_SITE/POSTAL_CODE/90210/rows/0:9/JSON
```

### 4. 安全饮用水 (SDWIS)

公共饮用水系统数据。

* *关键表格：**
|表|描述 |
|--------|--------------|
| `WATER_SYSTEM` |水系统信息。 |
| `VIOLATION` |饮用水违法行为。 |
| `LCR_SAMPLE_RESULT` |铅和铜规则示例结果。 |

* *示例 -- 某个州的饮用水违规：**
```
https://data.epa.gov/efservice/VIOLATION/PWSID/BEGINNING/OH/rows/0:19/JSON
```

### 5. 温室气体报告 (GHG)

设施级温室气体排放数据。

* *关键表格：**
|表|描述 |
|--------|-------------|
| `PUB_DIM_FACILITY` |温室气体报告设施信息。 |
| `PUB_FACTS_SECTOR_GHG_EMISSION` |按部门划分的排放量。 |

* *示例 -- 某个州的温室气体设施：**
```
https://data.epa.gov/efservice/PUB_DIM_FACILITY/STATE/TX/rows/0:9/JSON
```

- --

## 查询模式

### 使用运算符过滤
```
# Exact match (implicit =)
/TABLE/COLUMN/VALUE/JSON

# Greater than
/TABLE/COLUMN/>/VALUE/JSON

# Less than
/TABLE/COLUMN/</VALUE/JSON

# Not equal
/TABLE/COLUMN/!=/VALUE/JSON

# Starts with
/TABLE/COLUMN/BEGINNING/VALUE/JSON

# Contains
/TABLE/COLUMN/CONTAINING/VALUE/JSON
```

### 组合过滤器
链多个列/值对：
```
/TABLE/COLUMN1/VALUE1/COLUMN2/VALUE2/JSON
```

### 分页
使用`rows/{start}:{end}`（从0开始，包含）：
```
/TABLE/rows/0:99/JSON       # First 100 rows
/TABLE/rows/100:199/JSON    # Next 100 rows
```
默认不带`rows`：返回前10,000行。

### 输出格式
附加格式作为最后一个路径分段：
```
/TABLE/.../JSON
/TABLE/.../XML
/TABLE/.../CSV
/TABLE/.../EXCEL
```

- --

## AQS 数据 API（单独系统）

对于更精细的空气质量数据，EPA 还提供了 AQS 数据 API，网址为：
```
https://aqs.epa.gov/data/api
```

- **需要：** 免费帐户https://aqs.epa.gov/data/api/signup?email=YOUR_EMAIL
- **Auth:** 将 `email` 和 `key` 作为查询参数传递。
- 关键端点：`/dailyData/byState`、`/annualData/byState`、`/sampleData/bySite`、 `/monitors/byState`.

* *示例：**
```
https://aqs.epa.gov/data/api/dailyData/byState?email=YOUR_EMAIL&key=YOUR_KEY&param=44201&bdate=20240101&edate=20240131&state=06
```

## 注释
 - URL 中的表和列名称不区分大小写。
  - Envirofacts API 返回表的所有列；您不能选择特定列。
- 要跨表连接数据，您必须发出单独的请求并使用共享键连接客户端（例如`TRI_FACILITY_ID`、`REGISTRY_ID`）。
- 某些表非常大。始终使用 `rows/` 来限制结果和分页。
- EPA 数据更新因计划而异：TRI 为年度，AQS 为每日/年度，SDWIS 为季度。
