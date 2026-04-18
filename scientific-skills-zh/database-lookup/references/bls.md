# 劳工统计局 (BLS)公共数据 API

## 基本 URL

```
https://api.bls.gov/publicAPI/v2
```

 版本 1（无密钥）：`https://api.bls.gov/publicAPI/v1`

## 身份验证

* *API 密钥可选，但强烈推荐。** 在以下位置注册https://data.bls.gov/registrationEngine/

- **V1（无密钥）：** 限制为 25 个请求/天，10 年日期范围，每个查询 25 个系列。
- **V2（有密钥）：** 500 个请求/天，20 年日期范围，每个查询 50 个系列，加上目录数据和计算。

## 密钥端点

### 1. 获取系列数据（POST -- 主要方法）
```
POST /timeseries/data/
```
Content-Type: `application/json`

* *请求正文:**
```json
{
  "seriesid": ["CUUR0000SA0", "LNS14000000"],
  "startyear": "2020",
  "endyear": "2024",
  "registrationkey": "YOUR_KEY",
  "catalog": true,
  "calculations": true,
  "annualaverage": true,
  "aspects": true
}
```

|领域|必填 | V1 | V2 |描述 |
|------------------|---------|-----|-----|--------------------------------------------------------------------------------|
|系列ID |是的 |是的 |是的 |系列 ID 数组（最多 25 v1 / 50 v2）|
|开始年 |是的 |是的 |是的 | 4 位开始年份 |
|年底|是的 |是的 |是的 | 4 位结束年份 |
|注册码 |没有 |没有 |是的 | API 密钥（v2 功能所需）|
|目录 |没有 |没有 |是的 | `true` 包含系列元数据 |
|计算|没有 |没有 |是的 | `true` 包括净值/百分比变化 |
|年度平均 |没有 |没有 |是的 | `true` 包括年平均值 |
|方面 |没有 |没有 |是的 | `true` 包括脚注和方面 |

### 2. 获取单系列数据（GET -- 方便）
```
GET /timeseries/data/{seriesID}
```
E 示例：
```
https://api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0?registrationkey=YOUR_KEY&startyear=2022&endyear=2024
```

### 3. 最新数据（GET -- 无日期） range)
```
GET /timeseries/data/{seriesID}
```
不带startyear/endyear，返回最近3年。

示例：
```
https://api.bls.gov/publicAPI/v2/timeseries/data/LNS14000000?registrationkey=YOUR_KEY
```

## 通用系列 ID

### 消费者价格指数 (CPI)
|系列 ID |说明 |
|-----------------|----------------------------------------------------------------|
| CUUR0000SA0 | CPI-U 所有项目，美国城市平均，未季节性调整 |
| CUSR0000SA0 | CPI-U 所有项目，美国城市平均，季节性调整 |
| CUUR0000SAF1 | CPI-U 食品，美国城市平均 |
| CUUR0000SETB01 | CPI-U 汽油（所有类型）|
| CUUR0000SAH1 | CPI-U庇护所|
| CUUR0000SAM | CPI-U医疗|

CPI系列ID结构：`CU` + `U/S`（unadj/adj）+ `R/S`（修订）+区号+项目代码

### 就业/失业（当前人口调查）
|系列 ID |描述 |
|-----------------|----------------------------------------------------------------|
| LNS14000000 |失业率（季节性调整后）|
| LNS11000000 |民间劳动力水平|
| LNS12000000 |就业水平|
| LNS13000000 |失业率|
| LNS14000006 |失业率 - 黑人或非裔美国人 |
| LNS14000009 |失业率 - 西班牙裔或拉丁裔 |

### 就业（当前就业统计/非农就业人口）
|系列 ID |描述 |
|-----------------|----------------------------------------------------------------|
| CES0000000001 |非农就业总额（季节性调整）|
| CES0500000003 |平均每小时收入，私人总收入|
| CES0500000002 |平均每周工作时间，私人总时间 |

### 生产者价格指数 (PPI)
|系列 ID |描述 |
|-----------------|----------------------------------------------------------------|
| WPSFD4 | PPI最终需求|
| WPUFD49104 | PPI 最终需求减去食品和能源 |

### 就业成本指数 (ECI)
|系列 ID |描述 |
|-----------------|----------------------------------------------------------------|
| CIU1010000000000A | ECI 总薪酬，所有平民 |

### 职业就业和工资统计 (OEWS)
|系列 ID 图案 |描述 |
|--------------------------------|----------------------------------------------------------------|
| OEUM003342000000011-0000 |示例：特定职业/区域组合|

OEWS系列ID很复杂。使用 BLS 系列 ID 查找器：https://data.bls.gov/cgi-bin/srgate

## 系列 ID 结构

BLS 系列 ID 编码调查、季节调整、区域、行业和项目信息。主要调查前缀：

|前缀|调查|
|--------------------|------------------------------------------------|
| CU |居民消费价格指数|
|闪电 |当前人口调查（劳动力）|
|欧盟CE |当前就业统计|
| WP |生产者价格指数|
| EI |就业成本指数/国民薪酬|
|原厂设备 |职业就业及工资统计|
|洛杉矶 |当地失业统计|
| SM |州和都会区就业 (CES) |
|杰通 |职位空缺和劳动力流动 (JOLTS) |

## 响应格式

### 标准响应
```json
{
  "status": "REQUEST_SUCCEEDED",
  "responseTime": 85,
  "message": [],
  "Results": {
    "series": [
      {
        "seriesID": "CUUR0000SA0",
        "catalog": {
          "series_title": "All items in U.S. city average, all urban consumers, not seasonally adjusted",
          "series_id": "CUUR0000SA0",
          "seasonality": "Not Seasonally Adjusted",
          "survey_name": "Consumer Price Index - All Urban Consumers",
          "survey_abbreviation": "CU",
          "measure_data_type": "All items",
          "area": "U.S. city average",
          "item": "All items"
        },
        "data": [
          {
            "year": "2024",
            "period": "M01",
            "periodName": "January",
            "latest": "true",
            "value": "308.417",
            "footnotes": [{}],
            "calculations": {
              "net_changes": {
                "1": "0.5",
                "3": "1.2",
                "6": "2.1",
                "12": "3.1"
              },
              "pct_changes": {
                "1": "0.2",
                "3": "0.4",
                "6": "0.7",
                "12": "3.1"
              }
            }
          },
          {
            "year": "2023",
            "period": "M12",
            "periodName": "December",
            "value": "306.746",
            "footnotes": [{}]
          }
        ]
      }
    ]
  }
}
```

### 数据对象中的关键字段
- `year`：4 位年份字符串
- `period`：`M01`-`M12`（每月）、`Q01`-`Q05`（每季）、`A01`（每年）、`S01`-`S03`（半年）
- `periodName`：人类可读的周期名称
- `value`：字符串（转换为浮点数以进行计算）
- `latest`：仅在最近观察中的`"true"`
- `calculations`：仅当`calculations: true`在请求（V2）。包含 1、3、6、12 个月跨度的 `net_changes` 和 `pct_changes`。
- `footnotes`：脚注对象数组

### 错误响应
```json
{
  "status": "REQUEST_NOT_PROCESSED",
  "responseTime": 10,
  "message": ["No data available for the given series and date range."],
  "Results": {
    "series": []
  }
}
```

## 速率限制

|特色| V1（无钥匙）| V2（带钥匙） |
|--------------------------------|--------------------------------|--------------------------------|
|每日查询限额| 25 项请求 | 500 个请求 |
|每个查询的系列 | 25 | 25 50 |
|每次查询的年数 | 10 | 10 20 |
|目录数据|没有 |是 |
|计算|没有 |是 |
|年平均值|没有 |是 |
|净值/百分比变化|没有 |是 |

## 注释

- BLS 强烈建议使用 POST 请求进行数据检索。 GET 端点是一个方便的包装器。
- 周期 `M13` 表示年平均值（仅在 `annualaverage: true` 时出现）。
- 所有 `value` 字段都是字符串。缺失的数据通常会被忽略（观察结果根本不会出现）。
- 对于 CPI 百分比变化（通货膨胀率），您可以根据原始指数值计算或使用 V2 `calculations` 功能，该功能提供预先计算的 12 个月百分比变化。
- BLS 网站有一个用于构建 ID 的系列 ID 查找工具： https://data.bls.gov/cgi-bin/srgate
  - 批量数据可在 https://download.bls.gov/pub/time.series/ 下载，按调查前缀组织。
