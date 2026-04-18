# 世界卫生组织全球卫生观察站 (GHO) API 参考

## 概述
世界卫生组织全球卫生观察站 (GHO) OData API 提供对 194 个世界卫生组织成员国的健康统计数据的访问。它涵盖了 2000 多个指标，包括预期寿命、疾病负担、死亡率、免疫覆盖率、卫生人力、空气污染、水/卫生设施以及可持续发展目标 (SDG)健康指标。

## 基本 URL
```
https://ghoapi.azureedge.net/api
```

## 身份验证
* *无需 API 密钥。** API 完全开放， free.

## 速率限制
- 没有记录正式的速率限制。
- API 通过 Azure CDN 提供服务，并能很好地处理中等负载。
- 尊重自动请求；建议每秒 1-2 个。

- --

## 关键端点

API 遵循 OData v4 协议。标准 OData 查询参数工作：`$filter`、`$select`、`$orderby`、`$top`、`$skip`、`$count`.

### 1. 列出全部指标

```
GET /Indicator
```

* *示例：**
```
https://ghoapi.azureedge.net/api/Indicator
```

* *响应：**
```json
{
  "@odata.context": "...",
  "value": [
    {
      "IndicatorCode": "WHOSIS_000001",
      "IndicatorName": "Life expectancy at birth (years)",
      "Language": "EN"
    },
    {
      "IndicatorCode": "WHOSIS_000002",
      "IndicatorName": "Healthy life expectancy (HALE) at birth (years)",
      "Language": "EN"
    },
    {
      "IndicatorCode": "WHS4_100",
      "IndicatorName": "Measles (MCV1) immunization coverage among 1-year-olds (%)",
      "Language": "EN"
    }
  ]
}
```

### 2. 获取特定数据指标

```
GET /{IndicatorCode}
```

* *示例（出生时预期寿命）：**
```
https://ghoapi.azureedge.net/api/WHOSIS_000001
```

* *响应：**
```json
{
  "@odata.context": "...",
  "value": [
    {
      "Id": 12345,
      "IndicatorCode": "WHOSIS_000001",
      "SpatialDim": "USA",
      "SpatialDimType": "COUNTRY",
      "TimeDim": 2019,
      "TimeDimType": "YEAR",
      "Dim1": "SEX",
      "Dim1Type": "BTSX",
      "Dim2": null,
      "Dim2Type": null,
      "Dim3": null,
      "Dim3Type": null,
      "DataSourceDim": null,
      "Value": "78.5",
      "NumericValue": 78.5,
      "Low": 78.2,
      "High": 78.8,
      "Comments": "",
      "Date": "2024-01-15T00:00:00+00:00",
      "TimeDimensionValue": "2019",
      "TimeDimensionBegin": "2019-01-01T00:00:00+00:00",
      "TimeDimensionEnd": "2019-12-31T00:00:00+00:00"
    }
  ]
}
```

### 3. 按国家过滤

使用OData `$filter` 按国家/地区 (SpatialDim)限制结果。

* *示例（仅限美国的预期寿命）：**
```
https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDim eq 'USA'
```

* *示例（多个国家/地区的预期寿命）：**
```
https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDim eq 'USA' or SpatialDim eq 'GBR' or SpatialDim eq 'JPN'
```

### 4. 按年份筛选

* *示例（2019 年预期寿命）：**
```
https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=TimeDim eq 2019
```

* *示例（自 2015 年以来美国的预期寿命）：**
```
https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDim eq 'USA' and TimeDim ge 2015
```

### 5. 筛选性别/维度

* *示例（预期寿命，男女，美国，2015 年以上）：**
```
https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDim eq 'USA' and TimeDim ge 2015 and Dim1 eq 'BTSX'
```

Dim1 性别值：`BTSX`（男女）、`MLE`（男性）、`FMLE` (女).

### 6.分页与限制

* *示例（前 10 个结果）：**
```
https://ghoapi.azureedge.net/api/WHOSIS_000001?$top=10
```

 * *示例（跳过前 100 个，获取下 50 个）：**
```
https://ghoapi.azureedge.net/api/WHOSIS_000001?$top=50&$skip=100
```

### 7. 选择特定字段

```
https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDim eq 'USA'&$select=SpatialDim,TimeDim,NumericValue,Dim1
```

### 8. 订单结果

```
https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDim eq 'USA'&$orderby=TimeDim desc
```

### 9. 列出维度值

```
GET /DIMENSION/{DimensionType}/DimensionValues
```

* *示例（列出所有国家）：**
```
https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues
```

* *示例（列出所有地区）：**
```
https://ghoapi.azureedge.net/api/DIMENSION/REGION/DimensionValues
```

* *示例（列出性别维度值）：**
```
https://ghoapi.azureedge.net/api/DIMENSION/SEX/DimensionValues
```

- --

## 通用指标代码

### 预期寿命和死亡率
|代码|描述 |
|------|--------------|
| `WHOSIS_000001` |出生时预期寿命（岁）|
| `WHOSIS_000002` |出生时健康预期寿命（HALE）（岁）|
| `WHOSIS_000004` |新生儿死亡率（每1000名活产儿）|
| `MDG_0000000001` |婴儿死亡率（每1000名活产婴儿）|
| `MDG_0000000007` |五岁以下儿童死亡率（每 1000 名活产婴儿）|
| `MORT_MATERNALNUM` |孕产妇死亡人数|
| `MDG_0000000026` |孕产妇死亡率（每10万活产儿）|
| `NCDMORT3070` | 30-70 岁之间死于非传染性疾病的概率 |
| `LIFE_0000000029` |成人死亡率（死亡概率15-60） |

### 传染病
|代码|描述 |
|------|--------------|
| `WHS3_49` | HIV 感染率（占 15-49 岁人口的百分比）|
| `MDG_0000000029` |结核病发病率（每10万人）|
| `MALARIA_EST_INCIDENCE` |疟疾发病率（每 1000 名高危人群）|
| `WHS3_62` |新发艾滋病毒感染人数（每 1000 名未感染人口）|

### 免疫
|代码|描述 |
|------|-------------|
| `WHS4_100` |麻疹 (MCV1)免疫接种（1 岁儿童的百分比）|
| `WHS4_117` | DTP3 免疫接种（1 岁儿童的百分比）|
| `WHS4_129` |乙型肝炎 (HepB3)免疫 (%) |
| `WHS4_543` |脊髓灰质炎 (Pol3)免疫接种（1 岁儿童的百分比）|

### 非传染性疾病和危险因素
|代码|描述|
|------|-------------|
| `NCD_BMI_30A` |肥胖患病率（BMI >= 30），年龄标准化 |
| `NCD_HYP_PREVALENCE_A` |血压升高的患病率|
| `NCD_GLUC_04` |糖尿病患病率（占人口百分比）|
| `M_Est_smk_curr_std` |当前吸烟流行率|
| `SA_0000001462` |人均酒精消费总量（升）|

### 卫生系统
|代码|描述 |
|------|--------------|
| `HWF_0001` |医生（每万人）|
| `HWF_0006` |护理和助产人员（每万人）|
| `WHS7_104` |医院床位（每万人）|
| `GHED_CHE_pc_US_SHA2011` |当前人均卫生支出（美元）|
| `UHC_INDEX_REPORTED` |全民健康覆盖服务覆盖指数|

### 环境健康
|代码|描述 |
|------|--------------|
| `SDGPM25` | PM2.5空气污染，年平均暴露量（ug/m3）|
| `WSH_SANITATION_SAFELY_MANAGED` |安全管理的卫生服务 (%) |
| `WSH_WATER_SAFELY_MANAGED` |安全管理的饮用水服务 (%) |

- --

## 国家/地区代码 (ISO 3166-1 alpha-3)

GHO API 对 `SpatialDim` 字段中的国家/地区使用 **ISO 3 字母代码**。

`USA`（美国）， `GBR`（英国）、`DEU`（德国）、`FRA`（法国）、`JPN`（日本）、`CHN`（中国）、`IND`（印度）、`BRA`（巴西）、`ZAF`（南方）非洲）、`NGA`（尼日利亚）、`AUS`（澳大利亚）、`CAN`（加拿大）、`KOR`（韩国）、`MEX`（墨西哥）、`RUS`（俄罗斯联邦）

世卫组织区域：`AFR`（非洲）、`AMR`（美洲）、`SEAR`（东南亚）、`EUR`（欧洲）、`EMR`（东地中海）、`WPR`（西太平洋）、`GLOBAL` （全局）

- --

## 响应格式
所有响应均为 JSON，遵循 OData v4 约定：

```json
{
  "@odata.context": "https://ghoapi.azureedge.net/api/$metadata#...",
  "value": [
    { ... observation object ... },
    { ... observation object ... }
  ]
}
```

 每个观察中的关键字段：
- `SpatialDim`：国家/地区代码 (ISO alpha-3)
- `TimeDim`：年份（整数）
- `NumericValue`：数值数据值（浮点或空）
- `Value`：值的字符串表示形式
- `Low` / `High`：置信区间边界（当可用）
- `Dim1`：第一个附加维度（通常是性别：`BTSX`、`MLE`、`FMLE`）
- `Dim2`、`Dim3`：附加维度（年龄组等）

## 注释
 - API 使用 OData v4 语法。过滤运算符：`eq`、`ne`、`gt`、`ge`、`lt`、`le`、`and`、`or`、`not`。字符串值必须用单引号括起来。
- 并非所有指标都包含所有国家或年份的数据。在构建相关工作流程之前检查数据可用性。
- `NumericValue` 优于 `Value` 进行数值分析； `Value` 是一个字符串，可能包含限定符。
- 许多指标按性别 (`Dim1`)和/或年龄组 (`Dim2`)分类。使用维度值端点发现有效代码。
- 数据可能有多年滞后，特别是对于低收入国家。
- `Low` 和 `High` 字段提供来自 WHO 估计过程的不确定性区间（并非所有指标都有这些）。
- 对于批量探索，GHO 数据门户 https://www.who.int/data/gho 提供用于查找指示器代码的可浏览界面。
