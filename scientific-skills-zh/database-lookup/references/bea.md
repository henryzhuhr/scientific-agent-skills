# BEA（经济分析局）API参考

## 概述
经济分析局API提供对美国经济账户数据的访问，包括GDP（国民收入和产品账户——NIPA）、个人收入、国际贸易、行业账户和地区经济数据。结构为具有数据集特定参数的单个端点。

## 基本 URL
```
https://apps.bea.gov/api/data
```

## 身份验证
- **API 密钥：必需。** 在 https://apps.bea.gov/API/signup/
 注册 - 作为查询参数传递： `&UserID=YOUR_API_KEY`

## 速率限制
- **每个 API 密钥每分钟 100 个请求**。
- **每个 API 密钥每分钟 100 MB 数据**。
- **每分钟 30 个错误** -- 超出会触发临时锁定。
- 每日和每月限制尚未正式发布，但 BEA 可能会大力限制use.

## 常用参数（所有请求）
|参数|类型 |必填 |描述 |
|---------|--------|---------|-------------|
| `UserID` |字符串|是的 |您的 BEA API 密钥。 |
| `method` |字符串|是的 | API 方法（见下文）。 |
| `ResultFormat` |字符串|没有 | `JSON`（默认）或 `XML`。 |

- --

## 方法

### 1. GetDataSetList
列出所有可用数据集。

#### `GET /api/data?method=GetDataSetList&UserID=YOUR_KEY&ResultFormat=JSON`

* *示例：**
```
https://apps.bea.gov/api/data?method=GetDataSetList&UserID=YOUR_KEY&ResultFormat=JSON
```

* *响应：**
```json
{
  "BEAAPI": {
    "Request": {
      "RequestParam": [
        {"ParameterName": "METHOD", "ParameterValue": "GETDATASETLIST"},
        {"ParameterName": "RESULTFORMAT", "ParameterValue": "JSON"}
      ]
    },
    "Results": {
      "Dataset": [
        {"DatasetName": "NIPA", "DatasetDescription": "Standard NIPA tables"},
        {"DatasetName": "NIUnderlyingDetail", "DatasetDescription": "National Income and Product Accounts Underlying Detail"},
        {"DatasetName": "MNE", "DatasetDescription": "Multinational Enterprises"},
        {"DatasetName": "FixedAssets", "DatasetDescription": "Fixed Assets"},
        {"DatasetName": "ITA", "DatasetDescription": "International Transactions"},
        {"DatasetName": "IIP", "DatasetDescription": "International Investment Position"},
        {"DatasetName": "GDPbyIndustry", "DatasetDescription": "GDP by Industry"},
        {"DatasetName": "Regional", "DatasetDescription": "Regional data"},
        {"DatasetName": "UnderlyingGDPbyIndustry", "DatasetDescription": "Underlying GDP by Industry"},
        {"DatasetName": "InputOutput", "DatasetDescription": "Input-Output Statistics"}
      ]
    }
  }
}
```

- --

### 2. GetParameterList
列出特定的参数dataset.

#### `GET /api/data?method=GetParameterList&DatasetName={dataset}&UserID=YOUR_KEY&ResultFormat=JSON`

* *示例：**
```
https://apps.bea.gov/api/data?method=GetParameterList&DatasetName=NIPA&UserID=YOUR_KEY&ResultFormat=JSON
```

* *响应：**
```json
{
  "BEAAPI": {
    "Results": {
      "Parameter": [
        {
          "ParameterName": "TableName",
          "ParameterDataType": "string",
          "ParameterDescription": "The standard NIPA table identifier",
          "ParameterIsRequiredFlag": "1",
          "ParameterDefaultValue": ""
        },
        {
          "ParameterName": "Frequency",
          "ParameterDataType": "string",
          "ParameterDescription": "A - Annual, Q - Quarterly, M - Monthly",
          "ParameterIsRequiredFlag": "1",
          "ParameterDefaultValue": ""
        },
        {
          "ParameterName": "Year",
          "ParameterDataType": "string",
          "ParameterDescription": "List of year(s) of data to retrieve",
          "ParameterIsRequiredFlag": "1",
          "ParameterDefaultValue": ""
        }
      ]
    }
  }
}
```

- --

### 3. GetParameterValues
列出参数的有效值。

#### `GET /api/data?method=GetParameterValues&DatasetName={dataset}&ParameterName={param}&UserID=YOUR_KEY&ResultFormat=JSON`

* *示例（列出 NIPA 表）：**
```
https://apps.bea.gov/api/data?method=GetParameterValues&DatasetName=NIPA&ParameterName=TableName&UserID=YOUR_KEY&ResultFormat=JSON
```

* *响应（略）：**
```json
{
  "BEAAPI": {
    "Results": {
      "ParamValue": [
        {"TableName": "T10101", "Description": "Table 1.1.1. Percent Change From Preceding Period in Real Gross Domestic Product"},
        {"TableName": "T10106", "Description": "Table 1.1.6. Real Gross Domestic Product, Chained Dollars"},
        {"TableName": "T10105", "Description": "Table 1.1.5. Gross Domestic Product"},
        {"TableName": "T20100", "Description": "Table 2.1. Personal Income and Its Disposition"},
        {"TableName": "T30100", "Description": "Table 3.1. Government Current Receipts and Expenditures"}
      ]
    }
  }
}
```

- --

### 4. GetData
主要数据检索方法。参数因数据集而异。

#### `GET /api/data?method=GetData&DatasetName={dataset}&{params}&UserID=YOUR_KEY&ResultFormat=JSON`

- --

## 数据集特定参数和示例

### A. NIPA（国民收入和产品账户）

* *参数：**
|参数|类型 |必填 |描述 |
|------------|--------|---------|-------------|
| `TableName`|字符串|是的 | NIPA 表标识符（例如 `T10101`）。 |
| `Frequency`|字符串|是的 | `A`（年度）、`Q`（季度）、`M`（每月）。 |
| `Year` |字符串|是的 |以逗号分隔的年份，或 `ALL` 或 `X` 表示最新年份。 |

* *示例（实际 GDP 百分比变化，季度，2022-2024 年）：**
```
https://apps.bea.gov/api/data?method=GetData&DatasetName=NIPA&TableName=T10101&Frequency=Q&Year=2022,2023,2024&UserID=YOUR_KEY&ResultFormat=JSON
```

* *示例（GDP 水平，年度，所有年）：**
```
https://apps.bea.gov/api/data?method=GetData&DatasetName=NIPA&TableName=T10105&Frequency=A&Year=ALL&UserID=YOUR_KEY&ResultFormat=JSON
```

* *响应：**
```json
{
  "BEAAPI": {
    "Request": { ... },
    "Results": {
      "Statistic": "NIPA Table",
      "UTCProductionTime": "2024-11-01T13:00:00.000",
      "Dimensions": [
        {"Name": "TableName", "DataType": "string", "IsValue": "0"},
        {"Name": "SeriesCode", "DataType": "string", "IsValue": "0"},
        {"Name": "LineNumber", "DataType": "numeric", "IsValue": "0"},
        {"Name": "LineDescription", "DataType": "string", "IsValue": "0"},
        {"Name": "TimePeriod", "DataType": "string", "IsValue": "0"},
        {"Name": "METRIC_NAME", "DataType": "string", "IsValue": "0"},
        {"Name": "CL_UNIT", "DataType": "string", "IsValue": "0"},
        {"Name": "UNIT_MULT", "DataType": "numeric", "IsValue": "0"},
        {"Name": "DataValue", "DataType": "numeric", "IsValue": "1"}
      ],
      "Data": [
        {
          "TableName": "T10101",
          "SeriesCode": "A191RL",
          "LineNumber": "1",
          "LineDescription": "Gross domestic product",
          "TimePeriod": "2022Q1",
          "METRIC_NAME": "Fisher Quantity Index",
          "CL_UNIT": "Percent change",
          "UNIT_MULT": "0",
          "DataValue": "-1.6",
          "NoteRef": "T10101"
        },
        {
          "TableName": "T10101",
          "SeriesCode": "A191RL",
          "LineNumber": "1",
          "LineDescription": "Gross domestic product",
          "TimePeriod": "2022Q2",
          "CL_UNIT": "Percent change",
          "DataValue": "-0.6"
        }
      ],
      "Notes": [
        {"NoteRef": "T10101", "NoteText": "Table 1.1.1. Percent Change From Preceding Period..."}
      ]
    }
  }
}
```

- --

### B. 区域（州、县、MSA 数据）

* *参数：**
|参数|类型 |必填 |描述 |
|--------------|--------|---------|--------------|
| `TableName` |字符串|是的 |区域表（例如，`CAGDP1` 按州划分的 GDP）。 |
| `LineCode` |整数 |是的 |表中的行号（指定数据系列）。 |
| `GeoFips` |字符串|是的 | FIPS 代码：`STATE`（所有州）、`COUNTY`（所有县）、`MSA`（所有 MSA）或特定 FIPS（例如，加利福尼亚州为 `06000`）。 |
| `Year` |字符串|是的 |逗号分隔的年份或 `ALL` 或 `LAST5`。 |

* *常用区域表：**
|表|描述 |
|--------|--------------|
| `CAGDP1` |按州划分的 GDP 汇总 |
| `CAGDP2` |按州分列的 GDP |
| `CAGDP9` |各州实际 GDP |
| `CAINC1` |按州划分的个人收入汇总|
| `CAINC4` |各州个人收入和就业|
| `CAINC5N` |按州类型划分的个人收入|
| `SAINC1` |国家个人年收入|
| `SQINC1` |国家季度个人收入|

* *示例（按州划分的 GDP，所有州，2020-2023 年）：**
```
https://apps.bea.gov/api/data?method=GetData&DatasetName=Regional&TableName=CAGDP1&LineCode=1&GeoFips=STATE&Year=2020,2021,2022,2023&UserID=YOUR_KEY&ResultFormat=JSON
```

 * *示例（个人收入加利福尼亚州）：**
```
https://apps.bea.gov/api/data?method=GetData&DatasetName=Regional&TableName=CAINC1&LineCode=1&GeoFips=06000&Year=LAST5&UserID=YOUR_KEY&ResultFormat=JSON
```

* *回复：**
```json
{
  "BEAAPI": {
    "Results": {
      "Data": [
        {
          "GeoFips": "06000",
          "GeoName": "California",
          "Code": "CAINC1-1",
          "TimePeriod": "2023",
          "CL_UNIT": "Thousands of dollars",
          "UNIT_MULT": "3",
          "DataValue": "3,220,965,123"
        }
      ]
    }
  }
}
```

- --

### C. ITA（国际交易账户/贸易）

* *参数：**
|参数|类型 |必填 |描述 |
|------------|--------|---------|------------|
| `Indicator` |字符串|是的 |指标代码（例如，货物余额为 `BalGds`）。 |
| `AreaOrCountry` |字符串|是的 |国家代码：`AllCountries`、`China`、`Japan`等，或`All`。 |
| `Frequency` |字符串|是的 | `A`、`Q`、`M`。 |
| `Year` |字符串|是的 |以逗号分隔的年份或 `ALL`。 |

* *常用ITA指标：**
|代码|描述 |
|------|--------------|
| `BalGds` |货物余额|
| `BalServ` |服务平衡|
| `BalGdsServ` |商品和服务余额|
| `BalCurAcct` |经常账户余额|
| `ExpGds` |出口货物|
| `ImpGds` |进口货物|
| `ExpServ` |服务出口|
| `ImpServ` |服务进口 |

* *示例（美国对华货物贸易差额，季度）：**
```
https://apps.bea.gov/api/data?method=GetData&DatasetName=ITA&Indicator=BalGds&AreaOrCountry=China&Frequency=Q&Year=2022,2023,2024&UserID=YOUR_KEY&ResultFormat=JSON
```

- --

### D. GDPbyIndustry

* *参数：**
|参数|类型 |必填 |描述 |
|-------------|--------|---------|-------------|
| `TableID` |整数 |是的 |表号 (1-15)。 |
| `Industry` |字符串|是的 |行业代码：`ALL`，或特定的（例如农业的 `11`）。 |
| `Frequency` |字符串|是的 | `A` 或 `Q`。 |
| `Year` |字符串|是的 |以逗号分隔的年份或 `ALL`。 |

* *常用表 ID：**
|身份证 |描述|
|----|-------------|
| 1 |工业增加值|
| 5 |工业增加值占 GDP 的百分比 |
| 6 |工业实际增加值|
| 7 |按行业划分的实际增加值百分比变化 |

* *示例（所有行业增加值，年度）：**
```
https://apps.bea.gov/api/data?method=GetData&DatasetName=GDPbyIndustry&TableID=1&Industry=ALL&Frequency=A&Year=2020,2021,2022,2023&UserID=YOUR_KEY&ResultFormat=JSON
```

- --

### E. IIP（国际投资头寸）

* *参数：**
|参数|类型 |必填 |描述 |
|----------------|--------|---------|------------|
| `TypeOfInvestment` |字符串|是的 | `ALL`、`FinAssetsExclFinDeriv`等|
| `Component` |字符串|是的 | `ALL` 或特定组件。 |
| `Frequency` |字符串|是的 | `A` 或 `Q`。 |
| `Year` |字符串|是的 |以逗号分隔的年份或 `ALL`。 |

* *示例：**
```
https://apps.bea.gov/api/data?method=GetData&DatasetName=IIP&TypeOfInvestment=ALL&Component=ALL&Frequency=A&Year=2020,2021,2022,2023&UserID=YOUR_KEY&ResultFormat=JSON
```

- --

### F.固定资产

* *参数：**
|参数|类型 |必填 |描述 |
|------------|--------|---------|-------------|
| `TableName`|字符串|是的 |固定资产表ID。 |
| `Year` |字符串|是的 |以逗号分隔的年份或 `ALL`。 |

* *示例：**
```
https://apps.bea.gov/api/data?method=GetData&DatasetName=FixedAssets&TableName=FAAt101&Year=ALL&UserID=YOUR_KEY&ResultFormat=JSON
```

- --

## 关键 NIPA 表参考

|表名 |描述|
|-----------|--------------|
| `T10101` |实际 GDP 变化百分比 |
| `T10105` | GDP（现价美元）|
| `T10106` |实际GDP（环比2017年美元）|
| `T10107` | GDP价格指数（百分比变化）|
| `T10110` | GDP物价平减指数|
| `T20100` |个人收入及其处置|
| `T20301` |个人消费支出按类型|
| `T20600` |个人收入和支出|
| `T30100` |政府经常性收入和支出|
| `T40100` |国民账户中的对外交易|
| `T50100` |按部门划分的储蓄和投资|
| `T50105` |储蓄和投资（实际）|
| `T60100` |企业利润|
| `T70100` |按主要产品类型划分的 GDP |
| `T11000` |实际GDP，扩展细节|
| `T11200` |对GDP增长的贡献|

## GeoFips参考（常用）
| FIPS |状态 |
|------|--------|
| `00000` |美国|
| `01000` |阿拉巴马州|
| `06000` |加利福尼亚州|
| `12000` |佛罗里达州|
| `36000` |纽约|
| `48000` |德克萨斯州|
| `STATE` |所有州|
| `COUNTY` |所有县|
| `MSA` |所有大都市统计区域|

## Notes
- 响应中的 DataValue 是一个字符串，有时带有逗号（例如，`"3,220,965,123"`）。通过删除逗号进行解析。
- `Year=X` 仅返回最近可用的一年。
- `Year=LAST5` 返回最近 5 年。
- 对于 NIPA 表，结果包含每个表的多个行项目（不同的 GDP 组成部分有不同的行号）。
- `GetParameterValues`方法对于发现每个数据集的有效表名称、行代码和指标代码至关重要。
- BEA 还在 https://apps.bea.gov/iTable/ 提供批量下载文件以供交互使用。
- 季度数据使用格式的时间段 `2024Q1`、`2024Q2` 等。
- 除非另有说明，所有货币价值均以美元为单位指定。单位在 `CL_UNIT` 和 `UNIT_MULT` 字段中指示。
