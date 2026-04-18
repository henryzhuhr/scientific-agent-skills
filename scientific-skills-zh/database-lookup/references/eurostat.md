# 欧盟统计局 API 参考

## 概述
E 欧盟统计局是欧盟统计局，为欧盟/欧洲经济区成员国和伙伴国家提供经济、人口、贸易、劳动力、环境等方面的统计数据。 API 遵循 SDMX（统计数据和元数据交换）标准。

## 基本 URL
```
https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1
```

 还存在较旧的 JSON-stat 端点：
```
https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0
```

## 身份验证
* *不需要 API 密钥。** API 完全开放，并且free.

## 速率限制
- 没有记录正式的速率限制。
- 欧盟统计局可能会限制激进的抓取。将自动请求保持在每秒 1-2 个。
- 大型数据集可能会超时；使用过滤器来减少响应大小。

- --

## 关键端点 (SDMX 2.1 API)

### 1. 获取数据集（观察）

```
GET /data/{datasetCode}/{filter}
```

|参数|必填 |描述|
|---------|----------|----------|
| `datasetCode` |是的 |欧盟统计局数据集代码（例如，`nama_10_gdp`、`demo_pjan`）|
| `filter` |没有 |点分隔尺寸过滤器。使用 `+` 表示维度中的多个值，使用 `.` 分隔维度，使用空段表示“全部”。 |

* *查询参数：**
|参数|必填 |描述|
|---------|----------|----------|
| `format` |没有 | `sdmx+json`（默认）、`sdmx+csv`、`sdmx+xml`、`TSV` |
| `startPeriod` |没有 |开始年/季/月：`2015`、`2020-Q1`、`2020-01` |
| `endPeriod` |没有 |年/季/月末|
| `detail` |没有 | `full`（默认）、`dataonly`、`serieskeysonly`、`nodata` |
| `lang` |没有 | `en`（默认）、`fr`、`de` |

* *示例（德国和法国按市场价格计算的 GDP，年度，2018-2023 年）：**
```
https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/nama_10_gdp/A.CP_MEUR.B1GQ.DE+FR?startPeriod=2018&endPeriod=2023
```

 * *示例（按国家/地区划分的总人口，年度）：**
```
https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/demo_pjan/A.NR.T.TOTAL.DE+FR+IT+ES?startPeriod=2015&endPeriod=2023
```

 * *示例（失业率，季节性调整后，每月）：**
```
https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/une_rt_m/M.SA.TOTAL.PC_ACT.T.EA20?startPeriod=2023-01&endPeriod=2024-12
```

* *示例（HICP 通货膨胀，所有项目，每月）：**
```
https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/prc_hicp_mmor/M.RCH_A.CP00.DE+FR+IT?startPeriod=2023-01&endPeriod=2024-06&format=sdmx+json
```

### 2. 将数据集获取为 CSV

将 `?format=sdmx+csv` 附加到任何数据请求，以获得更易于处理的平面 CSV 响应parse.

* *示例：**
```
https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/nama_10_gdp/A.CP_MEUR.B1GQ.DE+FR?startPeriod=2018&endPeriod=2023&format=sdmx+csv
```

### 3.获取数据集结构（维度和代码）列表）

```
GET /datastructure/ESTAT/{datasetCode}
```

* *示例：**
```
https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/datastructure/ESTAT/nama_10_gdp
```

返回尺寸名称、位置和代码列表引用。

### 4. 获取代码列表（尺寸值）

```
GET /codelist/ESTAT/{codelistId}
```

* *示例：**
```
https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/codelist/ESTAT/GEO
```

### 5. 搜索/浏览数据集（数据流）

```
GET /dataflow/ESTAT/all
```

返回所有可用的欧盟统计局数据集。添加 `?detail=allstubs` 以简化列表。

* *示例：**
```
https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/all?detail=allstubs
```

- --

## JSON-stat API（更简单的替代方案）

### 基础URL
```
https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data
```

### 获取数据
```
GET /data/{datasetCode}?{dimension_filters}
```

 维度使用其维度名称作为查询参数传递。

* *示例（DE 的 GDP 和FR):**
```
https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp?geo=DE&geo=FR&unit=CP_MEUR&na_item=B1GQ&freq=A&time=2020&time=2021&time=2022&lang=en
```

* *响应（JSON-stat 格式）:**
```json
{
  "version": "2.0",
  "label": "GDP and main components (output, expenditure and income)",
  "id": ["freq", "unit", "na_item", "geo", "time"],
  "size": [1, 1, 1, 2, 3],
  "dimension": {
    "geo": {
      "label": "Geopolitical entity",
      "category": {
        "index": {"DE": 0, "FR": 1},
        "label": {"DE": "Germany", "FR": "France"}
      }
    },
    "time": {
      "label": "Time",
      "category": {
        "index": {"2020": 0, "2021": 1, "2022": 2}
      }
    }
  },
  "value": {3336010.0, 3601750.0, 3876810.0, 2310420.0, 2500870.0, 2639090.0},
  "status": {}
}
```

值位于平面数组中；使用尺寸大小来重塑。

- --

## 通用数据集代码

|代码|描述|
|------|--------------|
| `nama_10_gdp` | GDP及主要构成|
| `nama_10_pc` |人均GDP|
| `namq_10_gdp` | GDP季度|
| `demo_pjan` | 1 月 1 日人口 |
| `demo_gind` |人口变化（出生、死亡、迁移）|
| `une_rt_m` |失业率（月）|
| `une_rt_a` |失业率（年度）|
| `lfsi_emp_a` |就业率（年度）|
| `prc_hicp_manr` | HICP通货膨胀（年变化率，月度）|
| `prc_hicp_mmor` | HICP通货膨胀（月变化率）|
| `ext_lt_maineu` |按合作伙伴划分的欧盟贸易（主要合作伙伴）|
| `ext_st_27_2020sitc` |国际贸易SITC|
| `bop_c6_q` |国际收支（季度）|
| `gov_10dd_edpt1` |政府赤字/盈余|
| `gov_10a_main` |政府收入、支出及主要总量|
| `sts_inpr_m` |工业生产（月）|
| `tour_occ_nim` |旅游（住宿过夜）|
| `env_air_gge` |温室气体排放|
| `tec00114` | GDP增长率（百分比变化）|
| `tec00118` |政府债务占 GDP 的百分比 |

## 通用国家代码（ISO 2 个字母，欧盟统计局使用大写）

`AT`奥地利、`BE`比利时、`BG`保加利亚、`CY`塞浦路斯、`CZ`捷克、`DE`德国、`DK`丹麦、`EE`爱沙尼亚、`EL`希腊、 `ES`西班牙、`FI`芬兰、`FR`法国、`HR`克罗地亚、`HU`匈牙利、`IE`爱尔兰、`IT`意大利、`LT`立陶宛、`LU`卢森堡、 `LV` 拉脱维亚、`MT` 马耳他、`NL` 荷兰、`PL` 波兰、`PT` 葡萄牙、`RO` 罗马尼亚、`SE` 瑞典、`SI` 斯洛文尼亚、`SK`斯洛伐克

聚合：`EU27_2020`（EU-27）、`EA20`（欧元区20）、`EA19`（欧元区19）、`EEA30_2007`（欧洲经济区）

* *注：**希腊使用`EL`（不Eurostat.

## SDMX JSON 响应格式中的 `GR`)

```json
{
  "header": {
    "id": "...",
    "prepared": "2024-01-15T10:00:00"
  },
  "dataSets": [
    {
      "series": {
        "0:0:0:0": {
          "observations": {
            "0": [3336010.0],
            "1": [3601750.0]
          }
        }
      }
    }
  ],
  "structure": {
    "dimensions": {
      "series": [...],
      "observation": [...]
    }
  }
}
```

 在 SDMX+JSON 中，维度值被编码为整数索引。 `structure.dimensions` 部分将索引映射到代码和标签。这很紧凑，但需要索引查找。

## 注释
- 过滤器路径中的维度顺序取决于数据集结构。始终首先检查 `/datastructure/ESTAT/{code}`。
- 使用 `+` 选择一维中的多个值（例如，`DE+FR+IT`）。
- 将维度段留空（连续点 `..`）以选择所有值。
- CSV 格式建议使用 (`?format=sdmx+csv`)以便更轻松地解析 - 它返回带有标记列的平面行。
  - JSON-stat API 对于快速查询来说更简单，但 SDMX API 更强大和完整。
  - 可以通过浏览主题在 https://ec.europa.eu/eurostat/databrowser/ 找到数据集代码。
  - 可能会出现大型无限制查询出来。始终按国家/地区和时间段过滤。
