# FRED（美联储经济数据）API 参考

## 概述
FRED API 由圣路易斯联邦储备银行提供，可访问来自 100 多个来源的超过 800,000 个经济时间序列。涵盖 GDP、就业、通货膨胀、利率、货币供应、贸易、住房等。

## 基本 URL
```
https://api.stlouisfed.org/fred
```

## 身份验证
- **API 密钥：必需。** 在 https://fred.stlouisfed.org/docs/api/api_key.html
- 通过查询参数：`&api_key=YOUR_KEY`

## 速率限制
- **每个 API 密钥每分钟 120 个请求**。
- 没有记录每日限制，但过度使用可能会触发限制。

## 常用参数（适用于大多数端点）
|参数|类型 |必填 |默认|描述 |
|----------------|--------|---------|---------|-------------|
| `api_key` |字符串|是的 | - |您的 FRED API 密钥。 |
| `file_type` |字符串|没有 | `xml` |响应格式：`xml` 或 `json`。 |
| `realtime_start` |字符串|没有 |今天|实时周期 `YYYY-MM-DD` 开始。 |
| `realtime_end` |字符串|没有 |今天|实时周期结束 `YYYY-MM-DD`。 |

- --

## 关键端点

### 1. 系列观测值（时间序列数据）

#### `GET /fred/series/observations`
返回经济时间序列的数据值。

* *参数：**
|参数|类型 |必填 |默认 |描述 |
|--------------------|--------|---------|----------------|-------------|
| `series_id` |字符串|是的 | - | FRED 系列 ID（例如 `GDP`、`UNRATE`、`CPIAUCSL`）。 |
| `observation_start`|字符串|没有 | `1776-07-04` |开始日期 `YYYY-MM-DD`。 |
| `observation_end` |字符串|没有 | `9999-12-31` |结束日期 `YYYY-MM-DD`。 |
| `units` |字符串|没有 | `lin` |数据转换：`lin`（水平）、`chg`（变化）、`ch1`（与去年同期相比的变化）、`pch`（百分比变化）、`pc1`（与去年同期相比的百分比变化）、`pca`（复合年度百分比变化）、`cch`（连续复合）变化率）、`cca`（连续复合年率）、`log`（自然对数）。 |
| `frequency` |字符串|没有 | （本地）|聚合频率：`d`、`w`、`bw`、`m`、`q`、`sa`、`a`（每日到每年）。 |
| `aggregation_method` |字符串|没有 | `avg` | `avg`、`sum`、`eop`（期末）。 |
| `sort_order` |字符串|没有 | `asc` | `asc` 或 `desc`。 |
| `limit` |整数 |没有 | 100000 |返回的最大观测值（最大 100000）。 |
| `offset` |整数 |没有 | 0 |分页偏移。 |

* *示例：**
```
https://api.stlouisfed.org/fred/series/observations?series_id=GDP&api_key=YOUR_KEY&file_type=json&observation_start=2020-01-01&observation_end=2024-12-31&units=pch&frequency=q
```

* *响应：**
```json
{
  "realtime_start": "2024-11-01",
  "realtime_end": "2024-11-01",
  "observation_start": "2020-01-01",
  "observation_end": "2024-12-31",
  "units": "Percent Change",
  "output_type": 1,
  "file_type": "json",
  "order_by": "observation_date",
  "sort_order": "asc",
  "count": 20,
  "offset": 0,
  "limit": 100000,
  "observations": [
    {
      "realtime_start": "2024-11-01",
      "realtime_end": "2024-11-01",
      "date": "2020-01-01",
      "value": "-1.3"
    },
    {
      "realtime_start": "2024-11-01",
      "realtime_end": "2024-11-01",
      "date": "2020-04-01",
      "value": "-8.4"
    }
  ]
}
```

注意：`value` 始终是字符串。缺失值显示为 `"."`.

- --

### 2. 系列信息（元数据）

#### `GET /fred/series`
返回系列的元数据。

* *参数：**
|参数|类型 |必填 |描述 |
|------------|--------|---------|-------------|
| `series_id`|字符串|是的 | FRED 系列 ID。 |

* *示例：**
```
https://api.stlouisfed.org/fred/series?series_id=UNRATE&api_key=YOUR_KEY&file_type=json
```

* *响应：**
```json
{
  "realtime_start": "2024-11-01",
  "realtime_end": "2024-11-01",
  "seriess": [
    {
      "id": "UNRATE",
      "title": "Unemployment Rate",
      "observation_start": "1948-01-01",
      "observation_end": "2024-10-01",
      "frequency": "Monthly",
      "frequency_short": "M",
      "units": "Percent",
      "units_short": "%",
      "seasonal_adjustment": "Seasonally Adjusted",
      "seasonal_adjustment_short": "SA",
      "last_updated": "2024-11-01 07:41:02-05",
      "popularity": 95,
      "notes": "The unemployment rate represents..."
    }
  ]
}
```

- --

### 3.系列搜索

#### `GET /fred/series/search`
搜索系列通过关键字。

* *参数：**
|参数|类型 |必填 |默认|描述 |
|----------------|--------|----------|----------------|-------------|
| `search_text` |字符串|是的 | - |要搜索的关键字。 |
| `search_type` |字符串|没有 | `full_text` | `full_text` 或 `series_id`。 |
| `order_by` |字符串|没有 | `search_rank` | `search_rank`、`series_id`、`title`、`units`、`frequency`、`seasonal_adjustment`、`realtime_start`、`realtime_end`、`last_updated`、`observation_start`、 `observation_end`、`popularity`、`group_popularity`。 |
| `sort_order` |字符串|没有 | `asc` | `asc` 或 `desc`。 |
| `limit` |整数 |没有 | 1000 | 1000最大结果（最多 1000 个）。 |
| `offset` |整数 |没有 | 0 |分页偏移。 |
| `filter_variable` |字符串|没有 | - | `frequency`、`units`、`seasonal_adjustment`。 |
| `filter_value` |字符串|没有 | - |要过滤的值（例如，`Monthly`）。 |
| `tag_names` |字符串|没有 | - |要过滤的以分号分隔的标签（例如，`gdp;quarterly`）。 |

* *示例：**
```
https://api.stlouisfed.org/fred/series/search?search_text=consumer+price+index&api_key=YOUR_KEY&file_type=json&limit=5
```

* *响应：**
```json
{
  "realtime_start": "2024-11-01",
  "realtime_end": "2024-11-01",
  "order_by": "search_rank",
  "sort_order": "asc",
  "count": 1256,
  "offset": 0,
  "limit": 5,
  "seriess": [
    {
      "id": "CPIAUCSL",
      "title": "Consumer Price Index for All Urban Consumers: All Items in U.S. City Average",
      "observation_start": "1947-01-01",
      "observation_end": "2024-09-01",
      "frequency": "Monthly",
      "units": "Index 1982-1984=100",
      "seasonal_adjustment": "Seasonally Adjusted",
      "popularity": 95
    }
  ]
}
```

- --

### 4. 类别查找

#### `GET /fred/category`
获取特定类别的信息。

* *参数：**
|参数|类型 |必填 |描述 |
|-------------|------|---------|-------------|
| `category_id`|整数 |是的 |类别 ID（0 = 根）。 |

* *示例：**
```
https://api.stlouisfed.org/fred/category?category_id=0&api_key=YOUR_KEY&file_type=json
```

#### `GET /fred/category/children`
获取子类别。

* *示例：**
```
https://api.stlouisfed.org/fred/category/children?category_id=0&api_key=YOUR_KEY&file_type=json
```

#### `GET /fred/category/series`
获取某个类别中的所有系列。

* *参数：**
|参数|类型 |必填 |描述|
|-------------|------|----------|--------------|
| `category_id`|整数 |是的 |类别 ID。 |
| `limit` |整数 |没有 |最大结果（最多 1000 个）。 |
| `offset` |整数 |没有 |分页偏移。 |

* *示例：**
```
https://api.stlouisfed.org/fred/category/series?category_id=125&api_key=YOUR_KEY&file_type=json
```

- --

### 5.发布

#### `GET /fred/releases`
获取所有经济数据

* *示例：**
```
https://api.stlouisfed.org/fred/releases?api_key=YOUR_KEY&file_type=json
```

#### `GET /fred/release/series`
获取特定版本中的所有系列。

* *参数：**
|参数|类型 |必填 |描述|
|------------|------|---------|--------------|
| `release_id`|整数 |是的 |发布ID。 |

* *示例：**
```
https://api.stlouisfed.org/fred/release/series?release_id=53&api_key=YOUR_KEY&file_type=json
```

- --

### 6.标签

#### `GET /fred/tags`
获取所有标签及其使用频率。

#### `GET /fred/series/search/tags`
获取系列搜索匹配的标签。

* *示例：**
```
https://api.stlouisfed.org/fred/series/search/tags?series_search_text=mortgage+rate&api_key=YOUR_KEY&file_type=json
```

- --

## 常用系列ID

|系列 ID |描述 |
|--------------|--------------|
| `GDP` |国内生产总值（季度，十亿美元）|
| `GDPC1` |实际GDP（环比2017年美元）|
| `A191RL1Q225SBEA` |实际GDP增长率（年化季度）|
| `UNRATE` |失业率（月度，%）|
| `PAYEMS` |非农就业总额（月度，千）|
| `CPIAUCSL` |所有城镇消费者CPI（月度，指数）|
| `CPILFESL` |核心CPI（不包括食品和能源）|
| `PCEPI` | PCE价格指数|
| `PCEPILFE` |核心PCE价格指数|
| `FEDFUNDS` |联邦基金有效利率（月度，%）|
| `DFF` |联邦基金有效利率（每日）|
| `DGS10` | 10 年期国债固定到期利率（每日）|
| `DGS2` | 2 年期国债利率（每日）|
| `T10Y2Y` | 10年-2年国债利差|
| `MORTGAGE30US` | 30年期固定抵押贷款利率（每周）|
| `M2SL` | M2货币存量（每月）|
| `HOUST` |新屋开工量（月，千）|
| `RSAFS` |零售额（每月，百万美元）|
| `INDPRO` |工业生产指数|
| `UMCSENT` |密歇根大学消费者信心|
| `SP500` |标准普尔 500 指数（每日）|
| `VIXCLS` | CBOE 波动率指数（每日）|
| `DEXUSEU` |美元/欧元汇率（每日）|
| `DCOILWTICO`| WTI原油价格（每日）|
| `BOPGSTB` |贸易差额（每月，百万美元）|
| `GFDEBTN` |联邦债务公共债务总额 |

## 注释
- 实时周期：FRED 支持复古数据。 `realtime_start`/`realtime_end` 参数可让您检索特定时间点已知的数据（对于分析数据修订很有用）。
  - 用于转换的 `units` 参数非常强大 - 它避免了必须在客户端计算百分比变化。
  - 值以字符串形式返回； `"."` 表示缺失/不可用。
  - 对于 FRED 批量数据，他们在 `https://api.stlouisfed.org/geofred/` 上提供了用于地理/区域数据的下载 API。
