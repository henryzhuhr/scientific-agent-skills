# USGS API 参考（地震灾害 + 水务）

## A 部分：地震灾害计划

### 基本 URL
```
https://earthquake.usgs.gov/fdsnws/event/1
```

### 身份验证
* *不需要。** 完全公开，无需 API 密钥。

### 比率限制
 - 没有记录的每用户速率限制，但 USGS 要求用户限制自动查询以避免服务过载。
  - 返回非常大结果集（> 20,000 个事件）的请求将被拒绝。使用分页或缩小查询范围。

### 关键端点

#### 1. 查询地震
```
GET /query
```
 返回匹配搜索条件的地震事件。这是主要终点。

* *参数：**
|参数|类型 |必填 |默认 |描述 |
|--------------|--------|---------|------------|-------------|
| `format` |字符串|没有 | `quakeml` | `geojson`、`csv`、`quakeml`、`text`、`kml`。 JSON 使用 `geojson`。 |
| `starttime` |字符串|没有 | （现在 - 30 天）| ISO8601 日期，例如`2024-01-01`。 |
| `endtime` |字符串|没有 | （现在）| ISO8601 日期。 |
| `minmagnitude`|浮动|没有 | - |最小震级（例如 `4.5`）。 |
| `maxmagnitude`|浮动|没有 | - |最大幅度。 |
| `mindepth` |浮动|没有 | - |最小深度（公里）。 |
| `maxdepth` |浮动|没有 | - |最大深度（公里）。 |
| `latitude` |浮动|没有 | - |圆搜索的中心纬度（-90 到 90）。 |
| `longitude` |浮动|没有 | - |圆搜索的中心经度（-180 到 180）。 |
| `maxradiuskm`|浮动|没有 | - |最大半径（以公里为单位）（带纬度/经度）。 |
| `minlatitude`|浮动|没有 | - |边界框南边缘。 |
| `maxlatitude`|浮动|没有 | - |边界框北边缘。 |
| `minlongitude`|浮动|没有 | - |边界框西边缘。 |
| `maxlongitude`|浮动|没有 | - |边界框东边。 |
| `limit` |整数 |没有 | - |返回的最大事件数（最多 20000 个）。 |
| `offset` |整数 |没有 | 1 |分页偏移量（从 1 开始）。 |
| `orderby` |字符串|没有 | `time` | `time`、`time-asc`、`magnitude`、`magnitude-asc`。 |
| `alertlevel` |字符串|没有 | - |寻呼机警报：`green`、`yellow`、`orange`、`red`。 |
| `eventtype` |字符串|没有 | - |例如`earthquake`、`quarry blast`。 |

* *示例 -- 某个地区发生重大地震：**
```
https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2024-01-01&endtime=2024-12-31&minmagnitude=5.0&minlatitude=30&maxlatitude=45&minlongitude=-125&maxlongitude=-110&orderby=magnitude
```

* *GeoJSON 响应：**
```json
{
  "type": "FeatureCollection",
  "metadata": {
    "generated": 1700000000000,
    "url": "https://earthquake.usgs.gov/fdsnws/event/1/query?...",
    "title": "USGS Earthquakes",
    "status": 200,
    "api": "1.14.1",
    "count": 42
  },
  "features": [
    {
      "type": "Feature",
      "properties": {
        "mag": 6.2,
        "place": "15 km NNE of Ridgecrest, CA",
        "time": 1700000000000,
        "updated": 1700100000000,
        "tz": null,
        "url": "https://earthquake.usgs.gov/earthquakes/eventpage/ci00000001",
        "detail": "https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=ci00000001&format=geojson",
        "felt": 1500,
        "cdi": 7.1,
        "mmi": 6.5,
        "alert": "yellow",
        "status": "reviewed",
        "tsunami": 0,
        "sig": 800,
        "net": "ci",
        "code": "00000001",
        "type": "earthquake",
        "title": "M 6.2 - 15 km NNE of Ridgecrest, CA"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [-117.5, 35.8, 10.5]
      },
      "id": "ci00000001"
    }
  ]
}
```
注意：`geometry.coordinates` 是 `[longitude, latitude, depth_km]`.

#### 2. 事件详细信息
```
GET /query?eventid={EVENTID}&format=geojson
```
返回单个事件的详细信息，包括力矩张量、震源机制和附近城市。

#### 3.事件计数
```
GET /count
```
与`/query`参数相同，仅返回匹配事件的计数。用于在查询前检查结果大小。

* *示例：**
```
https://earthquake.usgs.gov/fdsnws/event/1/count?starttime=2024-01-01&endtime=2024-12-31&minmagnitude=4.5
```

#### 4. 实时源（无参数）
每分钟/5 分钟/15 分钟/小时更新一次的预构建 GeoJSON 源：
```
https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson
https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.geojson
https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson
https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson
```
模式： `{significance}_{timeperiod}.geojson`，其中重要性为 `significant`、`4.5`、`2.5`、`1.0`、`all`，时间周期为 `hour`、`day`、`week`， `month`.

- --

## B 部分：供水服务

### 基本 URL
```
https://waterservices.usgs.gov/nwis
```

### 身份验证
* *不需要。** 完全公开，无需 API 密钥。

### 费率限制
 - 没有严格的每用户限制，但 USGS 建议限制自动请求。大型查询可能会超时。

### 关键端点

#### 1. 瞬时值（实时数据）
```
GET /iv/
```
 返回最近的传感器读数（通常为 15 分钟间隔）。

* *参数：**
|参数|类型 |必填 |默认|说明 |
|----------------|--------|---------|---------|-------------|
| `format` |字符串|没有 | `wml` | `json`、`xml`、`wml,1.1`、`wml,2.0`、`rdb`。 JSON 使用 `json`。 |
| `sites` |字符串|条件。    | - |以逗号分隔的 USGS 站点编号（例如 `01646500`）。 |
| `stateCd` |字符串|条件。    | - | 2 个字母的州代码（例如 `NY`）。 |
| `huc` |字符串|条件。    | - |水文单位代码。 |
| `bBox` |字符串|条件。    | - |边界框：`west,south,east,north`（十进制）。 |
| `countyCd` |字符串|条件。    | - | 5 位 FIPS 县代码。 |
| `parameterCd` |字符串|没有 | `00060` |参数代码。 `00060`=水流，`00065`=标高，`00010`=水温。 |
| `period` |字符串|没有 | - | ISO8601 持续时间，例如`P7D`（过去 7 天）。 |
| `startDT` |字符串|没有 | - |开始日期时间 (ISO8601)。 |
| `endDT` |字符串|没有 | - |结束日期时间 (ISO8601)。 |
| `siteType` |字符串|没有 | - |例如`ST`（溪流）、`GW`（地下水）、`LK`（湖泊）。 |
| `siteStatus` |字符串|没有 | `all` | `active`、`inactive`、`all`。 |

 至少需要一个位置参数（`sites`、`stateCd`、`huc`、`bBox` 或 `countyCd`）。

* *示例 -- 站点的实时流：**
```
https://waterservices.usgs.gov/nwis/iv/?format=json&sites=01646500&parameterCd=00060&period=P1D
```

* *JSON 响应（缩写）：**
```json
{
  "name": "ns1:timeSeriesResponseType",
  "declaredType": "org.cuahsi.waterml.TimeSeriesResponseType",
  "value": {
    "timeSeries": [
      {
        "sourceInfo": {
          "siteName": "Potomac River near Wash, DC Little Falls Pump Sta",
          "siteCode": [{"value": "01646500", "agencyCode": "USGS"}],
          "geoLocation": {
            "geogLocation": {"latitude": 38.94977778, "longitude": -77.12763889}
          }
        },
        "variable": {
          "variableCode": [{"value": "00060"}],
          "variableName": "Streamflow, ft&#179;/s",
          "unit": {"unitCode": "ft3/s"}
        },
        "values": [
          {
            "value": [
              {"value": "5280", "dateTime": "2024-01-15T00:00:00.000-05:00"},
              {"value": "5310", "dateTime": "2024-01-15T00:15:00.000-05:00"}
            ]
          }
        ]
      }
    ]
  }
}
```

#### 2. 每日值（历史值）聚合）
```
GET /dv/
```
 返回每日统计值（平均值、最大值、最小值）。与`/iv/`.

相同的位置参数**附加参数：**
|参数|类型 |描述 |
|-----------|--------|-------------|
| `statCd` |字符串|统计代码：`00001`=max、`00002`=min、`00003`=mean、`00006`=sum。默认`00003`。 |

* *示例 -- 日平均流量，1 年：**
```
https://waterservices.usgs.gov/nwis/dv/?format=json&sites=01646500&parameterCd=00060&statCd=00003&startDT=2023-01-01&endDT=2023-12-31
```

#### 3. 站点信息
```
GET /site/
```
 返回有关监控站点的元数据。适用相同的位置参数。

* *示例 - 弗吉尼亚州的活动流站点：**
```
https://waterservices.usgs.gov/nwis/site/?format=rdb&stateCd=VA&siteType=ST&siteStatus=active&hasDataTypeCd=iv
```

#### 4. 统计数据（预计算）
```
GET /stat/
```
 返回每日值的预计算统计数据（百分位数、平均值、中位数），可用于将当前状况与历史数据进行比较

* *示例：**
```
https://waterservices.usgs.gov/nwis/stat/?format=rdb&sites=01646500&parameterCd=00060&statReportType=daily&statTypeCd=mean,p05,p25,p50,p75,p95
```

### 常用参数代码
|代码|描述 |
|---------|--------------|
| `00060` |流量/流量 (ft3/s) |
| `00065` |标距高度（英尺）|
| `00010` |水温（℃）|
| `00045` |降水量（中）|
| `00400` | pH值|
| `00300` |溶解氧（mg/L）|
| `00095` |比电导（uS/cm）|
| `72019` |地表以下地下水位深度（英尺）|

## 注释
- 地震 API 返回坐标为 `[lon, lat, depth]`（注意：经度在前）。
- 水服务 JSON 将数据包装在类似于 WaterML 的详细结构中。 `rdb`（制表符分隔）格式对于表格数据来说更简单。
  - USGS 站点编号对于地表水通常为 8 位数字，对于地下水为 15 位。
  - 两个 API 都是免费、公开的，并且不需要身份验证。
