# 美联储经济数据 (FRED) API

## 基本 URL

```
https://api.stlouisfed.org/fred
```

## 身份验证

* * 需要 API 密钥。** 在 https://fred.stlouisfed.org/docs/api/api_key.html 注册 

 作为查询参数传递： `&api_key=YOUR_KEY`

## 关键端点

### 获取系列（元数据）
```
GET /series
```
|参数|必填 |描述 |
|-------------|----------|------------------------------------|
|系列_id |是的 | FRED 系列 ID（例如 `FEDFUNDS`）|
| api_key |是的 |您的 API 密钥 |
|文件类型 |没有 | `json`（默认）、`xml` |

示例：
```
https://api.stlouisfed.org/fred/series?series_id=FEDFUNDS&api_key=YOUR_KEY&file_type=json
```

### 获取系列观测值（实际数据点）
```
GET /series/observations
```
|参数|必填 |描述 |
|--------------------------------|------------------------|--------------------------------------------------------|
|系列_id |是的 | FRED系列ID |
| api_key |是的 |您的 API 密钥 |
|文件类型 |没有 | `json`、`xml` |
|观察开始 |没有 | `YYYY-MM-DD` 开始日期 |
|观察结束 |没有 | `YYYY-MM-DD` 结束日期 |
|单位 |没有 | `lin`（级别）、`chg`、`ch1`、`pch`、`pc1`、`pca`、`cch`、`cca`、`log` |
|频率|没有 | `d`、`w`、`bw`、`m`、`q`、`sa`、`a`（每日到每年）|
|聚合方法|没有 | `avg`、`sum`、`eop` |
|排序顺序 |没有 | `asc`（默认），`desc` |
|限制|没有 |最大观测值（默认 100000）|
|偏移|没有 |分页偏移 |

示例：
```
https://api.stlouisfed.org/fred/series/observations?series_id=FEDFUNDS&api_key=YOUR_KEY&file_type=json&observation_start=2023-01-01&observation_end=2024-01-01
```

### 搜索系列
```
GET /series/search
```
|参数|必填 |描述 |
|-------------|----------|------------------------------------------------------------------------|
|搜索文本 |是的 |搜索关键词|
| api_key |是的 |您的 API 密钥 |
|文件类型 |没有 | `json`、`xml` |
|搜索类型 |没有 | `full_text`（默认）、`series_id` |
|限制|没有 |最大结果（默认 1000）|
|偏移|没有 |分页偏移|
|订购依据 |没有 | `search_rank`、`series_id`、`title`、`units`、`frequency`、`seasonal_adjustment`、`realtime_start`、`realtime_end`、`last_updated`、`observation_start`、 `observation_end`、`popularity`、`group_popularity` |
|标签名称 |没有 |分号分隔的标记过滤器 |

示例：
```
https://api.stlouisfed.org/fred/series/search?search_text=monetary+base&api_key=YOUR_KEY&file_type=json&limit=10
```

### 获取系列的类别
```
GET /series/categories
```
示例：
```
https://api.stlouisfed.org/fred/series/categories?series_id=FEDFUNDS&api_key=YOUR_KEY&file_type=json
```

### 浏览类别
```
GET /category
GET /category/children
GET /category/series
```
示例（根类别）：
```
https://api.stlouisfed.org/fred/category?category_id=0&api_key=YOUR_KEY&file_type=json
```

### 获取版本
```
GET /releases
GET /release/series
```
示例：
```
https://api.stlouisfed.org/fred/release/series?release_id=10&api_key=YOUR_KEY&file_type=json
```

### 获取标签
```
GET /tags
GET /series/tags
```

## 常见系列 ID

|系列 ID |描述|
|----------|--------------------------------------------------------|
|联邦基金|联邦基金有效利率|
| DFF |联邦基金利率（每日）|
| DGS10 | 10年期国债固定到期利率|
| DGS2 | 2年期国债固定到期利率|
| M2SL | M2货币库存|
| CPIAUCSL |居民消费价格指数（所有城市）|
|取消评级 |失业率|
|国内生产总值|国内生产总值|
| GDPC1 |实际GDP |
| A191RL1Q225SBEA |实际GDP增长率（季度）|
|付款|非农就业总额|
| T10Y2Y | 10年-2年国债利差|
|抵押贷款30美元| 30年期固定抵押贷款利率|
| DTWEXBGS |贸易加权美元指数|
|博格姆库 |货币基础（总计）|
|沃克 |美联储总资产 |

## 响应格式

### 系列元数据 (`/series`)
```json
{
  "realtime_start": "2024-01-01",
  "realtime_end": "2024-01-01",
  "seriess": [
    {
      "id": "FEDFUNDS",
      "realtime_start": "2024-01-01",
      "realtime_end": "2024-01-01",
      "title": "Federal Funds Effective Rate",
      "observation_start": "1954-07-01",
      "observation_end": "2024-01-01",
      "frequency": "Monthly",
      "frequency_short": "M",
      "units": "Percent",
      "units_short": "%",
      "seasonal_adjustment": "Not Seasonally Adjusted",
      "seasonal_adjustment_short": "NSA",
      "last_updated": "2024-02-01 15:51:07-06",
      "popularity": 95,
      "notes": "..."
    }
  ]
}
```

### 观察(`/series/observations`)
```json
{
  "realtime_start": "2024-01-01",
  "realtime_end": "2024-01-01",
  "observation_start": "2023-01-01",
  "observation_end": "2024-01-01",
  "units": "lin",
  "output_type": 1,
  "file_type": "json",
  "order_by": "observation_date",
  "sort_order": "asc",
  "count": 12,
  "offset": 0,
  "limit": 100000,
  "observations": [
    {
      "realtime_start": "2024-01-01",
      "realtime_end": "2024-01-01",
      "date": "2023-01-01",
      "value": "4.33"
    }
  ]
}
```

注意：`value` 始终是字符串。缺失数据显示为 `"."`.

### 搜索结果 (`/series/search`)
```json
{
  "realtime_start": "...",
  "realtime_end": "...",
  "order_by": "search_rank",
  "sort_order": "desc",
  "count": 500,
  "offset": 0,
  "limit": 1000,
  "seriess": [
    {
      "id": "BOGMBASE",
      "title": "Monetary Base; Total",
      "frequency": "Bi-Weekly",
      "units": "Millions of Dollars",
      "popularity": 72,
      "notes": "..."
    }
  ]
}
```

## 速率限制

- **每个 API 密钥每分钟 120 个请求**。
- 没有记录每日限制，但可能会过度使用throttled.
- 响应不包含速率限制标头；实现客户端限流。
