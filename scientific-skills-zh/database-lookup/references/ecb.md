# ECB 统计数据仓库 (SDW) REST API 参考

## 概述
ECB SDW API 提供对欧洲央行统计数据的访问：汇率、货币总量、利率、国际收支、银行统计数据等。它遵循 SDMX（统计数据和元数据交换）RESTful Web 服务标准。

## 基本 URL
```
https://data-api.ecb.europa.eu/service
```

 注意：旧 URL `https://sdw-wsrest.ecb.europa.eu/service` 仍然有效，但以上是当前端点。

## 身份验证
* *不需要 API 密钥。** API 完全开放，并且public.

## 速率限制
- 未发布正式的速率限制。
- ECB 要求用户尊重：避免过多的并行请求。
- 对于批量下载，使用压缩响应 (`Accept-Encoding: gzip`)。

## 通用标头
|标题 |价值|描述 |
|--------|--------|-------------|
| `Accept` | `application/vnd.sdmx.data+json;version=2.0.0` | JSON格式（推荐）|
| `Accept` | `application/vnd.sdmx.data+csv` | CSV格式|
| `Accept` | `application/vnd.sdmx.data+xml` | SDMX-ML XML（默认）|
| `Accept-Encoding` | `gzip` |压缩响应 |

- --

## 关键端点

### 1. 获取数据（时间序列）

```
GET /data/{flowRef}/{key}?{parameters}
```

|组件|描述|
|---------|--------------|
| `flowRef` |数据流 ID（例如，`EXR` 表示汇率，`BSI` 表示资产负债表项目）|
| `key` |点分隔的尺寸值。使用 `+` 进行 OR，`.` 跳过维度（通配符）。 |

* *查询参数：**
|参数|必填 |描述 |
|-----------|---------|------------|
| `startPeriod` |没有 |开始日期：`YYYY`、`YYYY-MM` 或 `YYYY-MM-DD` |
| `endPeriod` |没有 |结束日期：相同格式|
| `updatedAfter` |没有 | ISO 8601 时间戳；仅返回此时间之后更新的数据|
| `detail` |没有 | `full`（默认）、`dataonly`、`serieskeysonly`、`nodata` |
| `firstNObservations` |没有 |仅返回每个系列的前 N ​​个观测值 |
| `lastNObservations` |没有 |仅返回每个系列的最后 N 个观测值 |
| `dimensionAtObservation` |没有 |通常为 `TIME_PERIOD`（默认）|

* *汇率密钥结构（EXR 数据流）：**
`{frequency}.{currency}.{currency_denom}.{exr_type}.{exr_suffix}`

|职位|尺寸|常用值 |
|---------|------------|----------------|
| 1 |频率| `D`（每日）、`M`（每月）、`A`（每年）|
| 2 |货币 | `USD`、`GBP`、`JPY`、`CHF`、`CNY`等|
| 3 |货币分母 | `EUR`（通常）|
| 4 |汇率类型 | `SP00`（现货）、`EN00`（平均）|
| 5 |汇率后缀| `A`（平均）、`E`（期末）|

* *示例 -- 每日美元/欧元即期汇率，2024 年：**
```
GET https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?startPeriod=2024-01-01&endPeriod=2024-12-31
Accept: application/vnd.sdmx.data+json;version=2.0.0
```

* *示例 -- 过去 12 个月的每月英镑和日元兑欧元观察结果：**
```
GET https://data-api.ecb.europa.eu/service/data/EXR/M.GBP+JPY.EUR.SP00.A?lastNObservations=12
Accept: application/vnd.sdmx.data+json;version=2.0.0
```

* *示例 -- 特定日期的所有每日汇率（通配符）：**
```
GET https://data-api.ecb.europa.eu/service/data/EXR/D..EUR.SP00.A?startPeriod=2024-06-01&endPeriod=2024-06-01
Accept: application/vnd.sdmx.data+json;version=2.0.0
```

* *JSON 响应结构 (SDMX-JSON v2.0):**
```json
{
  "meta": { "schema": "...", "id": "...", "prepared": "2024-11-01T12:00:00Z" },
  "data": {
    "dataSets": [
      {
        "action": "Information",
        "series": {
          "0": {
            "attributes": [0, 0, ...],
            "observations": {
              "0": [1.0856],
              "1": [1.0791],
              "2": [1.0834]
            }
          }
        }
      }
    ],
    "structures": [
      {
        "dimensions": {
          "series": [...],
          "observation": [
            {
              "id": "TIME_PERIOD",
              "values": [
                {"id": "2024-01-02", "name": "2024-01-02"},
                {"id": "2024-01-03", "name": "2024-01-03"}
              ]
            }
          ]
        }
      }
    ]
  }
}
```

注意：观察值是索引数组。将观测索引与 `structures.dimensions.observation`.

 中的 `TIME_PERIOD` 值进行匹配**CSV 响应**（更易于解析）：
```
Accept: application/vnd.sdmx.data+csv
```
 返回标准 CSV，其中包含以下列：`DATAFLOW`、`FREQ`、`CURRENCY`、`CURRENCY_DENOM`、`EXR_TYPE`、`EXR_SUFFIX`、`TIME_PERIOD`、 `OBS_VALUE`等

- --

### 2.获取数据流定义（可用数据集）

```
GET /dataflow/{agencyID}/{resourceID}/{version}
```

* *示例 -- 列出所有ECB数据流：**
```
GET https://data-api.ecb.europa.eu/service/dataflow/ECB
Accept: application/vnd.sdmx.structure+json;version=2.0.0
```

* *示例-- 获取 EXR 数据流定义：**
```
GET https://data-api.ecb.europa.eu/service/dataflow/ECB/EXR
Accept: application/vnd.sdmx.structure+json;version=2.0.0
```

- --

### 3. 获取数据结构定义（维度 &代码）

```
GET /datastructure/{agencyID}/{resourceID}/{version}?references=children
```

* *示例：**
```
GET https://data-api.ecb.europa.eu/service/datastructure/ECB/ECB_EXR1?references=children
Accept: application/vnd.sdmx.structure+json;version=2.0.0
```

这将返回所有维度、其代码列表和允许的值 - 对于构造有效键至关重要。

- --

## 通用数据流ID

|数据流 |描述 |
|----------|-------------|
| `EXR` |汇率|
| `BSI` |资产负债表项目（货币金融机构）|
| `MIR` | MFI利率|
| `ILM` |内部流动性管理|
| `SEC` |证券发行统计|
| `BOP` |国际收支|
| `STP` |结构性财务指标|
| `CBD` |综合银行数据|
| `ICP` |消费者价格指数（HICP）|
| `FM` |金融市场数据|
| `YC` |产量曲线数据 |

## 注释
- SDMX-JSON 格式很详细。为了更简单的解析，请使用 `Accept: application/vnd.sdmx.data+csv`.
  - 当维度未知时，将其留空（例如，`D..EUR.SP00.A`）以获取该维度的所有值。
  - 使用 `+` 请求一个维度的多个值（例如， `USD+GBP`).
- `detail=dataonly` 参数省略属性并减少响应大小。
- 历史数据可用性因数据流而异；汇率回到1999年（欧元介绍）。
