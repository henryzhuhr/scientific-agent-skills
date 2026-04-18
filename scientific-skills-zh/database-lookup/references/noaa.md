# NOAA 气候数据在线 (CDO) API 参考

## 基本 URL
```
https://www.ncdc.noaa.gov/cdo-web/api/v2
```

## 身份验证
- **API 令牌：必需。** 在 https://www.ncdc.noaa.gov/cdo-web/token
 请求免费令牌 - 作为 HTTP 标头传递： `Token: YOUR_TOKEN`

## 速率限制
- **每个令牌每秒 5 个请求**。
- 每个令牌每天 **10,000 个请求**。
- 查询限制为 **每个请求 1,000 个结果**（使用 `offset` 进行分页）。
- 日期范围限制为 **1 `/data` 端点的每个请求年**。

## 通用参数（适用于大多数端点）
|参数|类型 |必填 |默认|描述|
|-------------|--------|---------|---------|-------------|
| `datasetid` |字符串|变化 | - |数据集 ID（例如 `GHCND`、`GSOM`）。 |
| `datatypeid` |字符串|没有 | - |数据类型过滤器（例如 `TMAX`、`PRCP`）。 |
| `locationid` |字符串|没有 | - |位置 ID（例如 `FIPS:37`、`ZIP:28801`、`CITY:US390029`）。 |
| `stationid` |字符串|没有 | - |站 ID（例如 `GHCND:USW00013874`）。 |
| `startdate` |字符串|变化 | - | ISO 日期 `YYYY-MM-DD`。 |
| `enddate` |字符串|变化 | - | ISO 日期 `YYYY-MM-DD`。 |
| `units` |字符串|没有 | `standard` | `standard` 或 `metric`。 |
| `limit` |整数 |没有 | 25 | 25每页结果（最多 1000 个）。 |
| `offset` |整数 |没有 | 1 |分页偏移量（从 1 开始）。 |
| `sortfield` |字符串|没有 | - |排序依据的字段（例如 `date`、`name`）。 |
| `sortorder` |字符串|没有 | `asc` | `asc` 或 `desc`。 |

- --

## 关键端点

### 1. 数据（观测值）
```
GET /data
```
 返回实际观测数据。这是主要数据检索端点。

* *必需参数：** `datasetid`、`startdate`、`enddate`.

* *示例 -- 每日最高温度站：**
```bash
curl -H "Token: YOUR_TOKEN" \
  "https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMAX&stationid=GHCND:USW00013874&startdate=2024-01-01&enddate=2024-01-31&units=metric&limit=31"
```

* *响应：**
```json
{
  "metadata": {
    "resultset": {
      "offset": 1,
      "count": 31,
      "limit": 31
    }
  },
  "results": [
    {
      "date": "2024-01-01T00:00:00",
      "datatype": "TMAX",
      "station": "GHCND:USW00013874",
      "attributes": ",,W,2400",
      "value": 12.2
    },
    {
      "date": "2024-01-02T00:00:00",
      "datatype": "TMAX",
      "station": "GHCND:USW00013874",
      "attributes": ",,W,2400",
      "value": 8.9
    }
  ]
}
```
注意：当`units=standard`时，GHCND温度值以十分之一摄氏度为单位。对于`units=metric`，它们被转换为摄氏度。

### 2.数据集
```
GET /datasets
GET /datasets/{id}
```
列出可用数据集或获取一个数据集的详细信息。

* *示例：**
```bash
curl -H "Token: YOUR_TOKEN" \
  "https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets?limit=10"
```

* *关键数据集 ID：**
|身份证 |名称 |描述 |
|----------|------|------------|
| `GHCND` |每日总结 |全球每日站点观测（TMAX、TMIN、PRCP、SNOW 等）|
| `GSOM` |本月全球摘要 |每月总计|
| `GSOY` |年度全球总结|年度总量|
| `NORMAL_DLY` |气候常态日报 | 30年日常正常值|
| `NORMAL_MLY` |气候常态月刊| 30年月均值|
| `PRECIP_15` | 15 分钟降水 |次小时降水量|
| `PRECIP_HLY` |每小时降水量 |每小时降水量 |

### 3. 数据类型
```
GET /datatypes
GET /datatypes/{id}
```
列出可用的数据类型，可选择按数据集过滤。

* *示例：**
```bash
curl -H "Token: YOUR_TOKEN" \
  "https://www.ncdc.noaa.gov/cdo-web/api/v2/datatypes?datasetid=GHCND&limit=50"
```

* *常见 GHCND 数据类型：**
|身份证 |描述 |
|--------|-------------|
| `TMAX` |最高温度|
| `TMIN` |最低温度|
| `TAVG` |平均气温|
| `PRCP` |降水|
| `SNOW` |降雪|
| `SNWD` |积雪深度|
| `AWND` |平均风速|
| `WSF2` |最快 2 分钟风速 |

### 4. 气象站
```
GET /stations
GET /stations/{id}
```
查找气象站，可以选择按位置、数据集或范围进行筛选。

* *附加参数：**
|参数|类型 |描述|
|------------|--------|-------------|
| `extent` |字符串|边界框：`south_lat,west_lon,north_lat,east_lon`。 |

* *示例 -- 北卡罗来纳州阿什维尔附近的站点，提供每日数据：**
```bash
curl -H "Token: YOUR_TOKEN" \
  "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations?datasetid=GHCND&locationid=ZIP:28801&limit=10"
```

* *响应：**
```json
{
  "metadata": {"resultset": {"offset": 1, "count": 5, "limit": 10}},
  "results": [
    {
      "elevation": 661.1,
      "mindate": "1893-01-01",
      "maxdate": "2024-11-15",
      "latitude": 35.5951,
      "name": "ASHEVILLE REGIONAL AIRPORT, NC US",
      "datacoverage": 1,
      "id": "GHCND:USW00013874",
      "elevationUnit": "METERS",
      "longitude": -82.5572
    }
  ]
}
```

### 5. 位置和位置类别
```
GET /locations
GET /locations/{id}
GET /locationcategories
GET /locationcategories/{id}
```
浏览位置层次结构（国家、州、城市、邮政编码、气候区域）。

* *示例：**
```bash
curl -H "Token: YOUR_TOKEN" \
  "https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?locationcategoryid=ST&limit=52"
```

位置类别 ID：`CITY`、`CLIM_DIV`、`CLIM_REG`、`CNTRY`、 `CNTY`、`HYD_ACC`、`HYD_CAT`、`HYD_REG`、`HYD_SUB`、`ST`、`ZIP`.

- --

## 工作流程：查找和查询数据

1. **查找数据集：** `GET /datasets` 列出可用数据集。
2. **查找车站：** `GET /stations?datasetid=GHCND&locationid=ZIP:28801` 查找附近的车站。
3. **检查可用数据类型：** `GET /datatypes?datasetid=GHCND&stationid=GHCND:USW00013874`.
4. **查询数据：** `GET /data?datasetid=GHCND&stationid=GHCND:USW00013874&datatypeid=TMAX,TMIN&startdate=2024-01-01&enddate=2024-12-31&units=metric&limit=1000`.

## 注释
 - `/data` 端点对每个请求强制执行 **1 年最大日期范围**。对于多年查询，请进行顺序请求。
- 分页：`offset` 从 1 开始。循环直到元数据中的 `offset + limit > count`。
- 站点 ID 包含数据集前缀（例如 `GHCND:USW00013874`）。
- 数据结果中的 `attributes` 字段包含质量标志（以逗号分隔）。请参阅数据集文档以了解标志含义。
- 令牌位于标头中，而不是作为查询参数。
