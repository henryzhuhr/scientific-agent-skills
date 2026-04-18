# 美国人口普查局 API 参考

## 概述
美国人口普查局 API 提供对数百个数据集的访问，包括美国社区调查 (ACS)、十年一次的人口普查、经济普查、人口估计等。它是美国人口、社会、经济和住房数据的主要来源。

## 基本 URL
```
https://api.census.gov/data
```

## 身份验证
- **API 密钥：必需（免费）。** 在 https://api.census.gov/data/key_signup.html
- 作为查询参数传递： `&key=YOUR_KEY`
  - 没有密钥的请求被限制为约 500 个/天。使用密钥，限制要高得多。

## 速率限制
- 不使用密钥：每天大约 500 个请求。
- 使用密钥：每个 IP 每天最多 500 个请求是记录的软限制，但实际上密钥授予的数量要多得多。
- 没有记录正式的每分钟速率限制；将自动请求保持在每秒几个。

- --

## 关键数据集和URL模式

一般URL模式是：
```
https://api.census.gov/data/{year}/{dataset}?get={variables}&for={geography}&key=YOUR_KEY
```

### 主要数据集路径

|数据集 |路径段|描述|
|---------|-------------|-------------|
| ACS 5 年详细表 | `acs/acs5` |大多数地区的 5 年估计（2009 年至今）|
| ACS 1 年详细表格 | `acs/acs1` |一年估计，人口超过 65,000 人（2005 年至今）|
| ACS 5 年主题表 | `acs/acs5/subject` |预先计算的主题表|
| ACS 5 年数据概况 | `acs/acs5/profile` |社会/经济/住房概况|
|十年一次的人口普查（2020 年）| `dec/dhc` |人口统计和住房特征|
|十年一次的人口普查（2020 PL）| `dec/pl` |重新划分数据 (PL 94-171) |
|十年一次的人口普查（2010）| `dec/sf1` |摘要文件1 |
|人口估计| `pep/population` |年人口估计|
|经济普查| `ecnbasic` |经济普查（2017、2022）|
|县商业模式| `cbp` |企业设立很重要|
|年度商业调查| `abscs` |业务特征 |

- --

## 关键端点

### 1. ACS 5 年估算（最常见）

```
GET /data/{year}/acs/acs5?get={variables}&for={geography}&key=YOUR_KEY
```

|参数|必填 |描述|
|---------|----------|----------|
| `get` |是的 |逗号分隔的变量名称（例如，`NAME,B01001_001E`）|
| `for` |是的 |目标地理位置（例如，`state:*`、`county:*`、`tract:*`）|
| `in` |有时|子州级别的父地理 |
| `key` |是的 |您的 API 密钥 |

* *示例（所有州的总人口，2022 ACS 5 年）：**
```
https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=state:*&key=YOUR_KEY
```

* *示例（加利福尼亚州所有县的家庭收入中位数）：**
```
https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E&for=county:*&in=state:06&key=YOUR_KEY
```

* *示例（特定区域的种族人口）：**
```
https://api.census.gov/data/2022/acs/acs5?get=NAME,B02001_001E,B02001_002E,B02001_003E&for=tract:000100&in=state:06&in=county:075&key=YOUR_KEY
```

* *响应（JSON 数组，第一行是标题）：**
```json
[
  ["NAME", "B01001_001E", "state"],
  ["Alabama", "5024279", "01"],
  ["Alaska", "733391", "02"],
  ["Arizona", "7151502", "04"]
]
```

### 2. ACS 1 年估算

```
GET /data/{year}/acs/acs1?get={variables}&for={geography}&key=YOUR_KEY
```
与ACS 5年参数相同。仅适用于人口超过 65,000 人的地区。

* *示例（所有州的贫困率）：**
```
https://api.census.gov/data/2022/acs/acs1?get=NAME,B17001_001E,B17001_002E&for=state:*&key=YOUR_KEY
```

### 3. ACS 数据配置文件

```
GET /data/{year}/acs/acs5/profile?get={variables}&for={geography}&key=YOUR_KEY
```
 使用带有预先计算的 `DP` 前缀变量百分比.

* *示例（教育程度概况）：**
```
https://api.census.gov/data/2022/acs/acs5/profile?get=NAME,DP02_0068PE&for=state:*&key=YOUR_KEY
```

### 4. 2020 年十年一次人口普查

```
GET /data/2020/dec/dhc?get={variables}&for={geography}&key=YOUR_KEY
```

* *示例（按州划分的总人口，2020 年）人口普查）：**
```
https://api.census.gov/data/2020/dec/dhc?get=NAME,P1_001N&for=state:*&key=YOUR_KEY
```

### 5. 十年一次的人口普查 2010

```
GET /data/2010/dec/sf1?get={variables}&for={geography}&key=YOUR_KEY
```

* *示例：**
```
https://api.census.gov/data/2010/dec/sf1?get=NAME,P001001&for=state:*&key=YOUR_KEY
```

### 6. 发现可用变量

```
GET /data/{year}/{dataset}/variables.json
```

* *示例：**
```
https://api.census.gov/data/2022/acs/acs5/variables.json
```
返回一个大型 JSON 对象，列出所有可用变量以及标签和概念。

### 7. 发现可用地理

```
GET /data/{year}/{dataset}/geography.json
```

* *示例：**
```
https://api.census.gov/data/2022/acs/acs5/geography.json
```

### 8. 列出可用数据集

```
GET /data.json
```

返回所有可用数据集及其标题、年份和 API端点.

- --

## 地理语法

|水平| `for` 语法 | `in` 要求|
|--------|--------------|-----------------|
|国家| `us:1` 或 `us:*` |无 |
|状态| `state:06` 或 `state:*` |无 |
|县| `county:075` 或 `county:*` | `in=state:06`（全部可选）|
|县分区| `county subdivision:*` | `in=state:XX&in=county:YYY` |
|人口普查单| `tract:*` | `in=state:XX&in=county:YYY` |
|块集团| `block group:*` | `in=state:XX&in=county:YYY&in=tract:ZZZZZZ` |
|地点（城市）| `place:*` | `in=state:XX` |
|都会区 (CBSA) | `metropolitan statistical area/micropolitan statistical area:*` |无 |
|邮政编码选项卡区域 | `zip code tabulation area:*` |无 |

州 FIPS 代码：`01`=AL、`02`=AK、`04`=AZ、`05`=AR、`06`=CA、`08`=CO、`09`=CT、`10`=DE、 `11`=DC、`12`=FL、`13`=GA、`15`=HI、`16`=ID、`17`=IL、`18`=IN、`19`=IA、`20`=KS、 `21`=KY、`22`=LA、`23`=ME、`24`=MD、`25`=MA、`26`=MI、`27`=MN、`28`=MS、`29`=MO、 `30`=MT、`31`=NE、`32`=NV、`33`=NH、`34`=NJ、`35`=NM、`36`=NY、`37`=NC、 `38`=ND、`39`=OH、`40`=OK、`41`=OR、`42`=PA、`44`=RI、`45`=SC、`46`=SD、`47`=TN、 `48`=TX、`49`=UT、`50`=VT、`51`=VA、`53`=WA、`54`=WV、`55`=WI、 `56`=WY

- --

## 常用变量代码

### ACS 详细表（B 表）
|变量|描述|
|----------|-------------|
| `B01001_001E` |总人口|
| `B01002_001E` |中位年龄|
| `B02001_001E` |总计（比赛）|
| `B02001_002E` |白独|
| `B02001_003E` |黑人或非裔美国人 |
| `B03001_003E` |西班牙裔或拉丁裔 |
| `B19013_001E` |家庭收入中位数|
| `B19001_001E` |家庭收入（总计，用于分配）|
| `B25077_001E` |房屋价值中位数 |
| `B25064_001E` |总租金中位数|
| `B17001_001E` |贫困状况（总计）|
| `B17001_002E` |贫困状况（贫困以下）|
| `B15003_022E` |学士学位|
| `B15003_023E` |硕士学位|
| `B15003_025E` |博士学位 |
| `B23025_005E` |失业者（平民劳动力）|
| `B25001_001E` |住房总数|
| `B08301_001E` |上班的交通工具（总计）|

变量命名：`B{table}_{seq}E`用于估计，`B{table}_{seq}M`用于误差幅度。

### ACS数据配置文件变量（DP表）
|变量|描述 |
|----------|-------------|
| `DP02_0068PE` |拥有学士及以上学历的% |
| `DP03_0062E` |家庭收入中位数|
| `DP03_0128PE` |低于贫困线的百分比 |
| `DP04_0089E` |房屋价值中位数|
| `DP05_0001E` |总人口 |

### 2020 年十年 (DHC)
|变量|描述 |
|----------|-------------|
| `P1_001N` |总人口|
| `P1_003N` |白色独|
| `P1_004N` |黑人或非裔美国人 |
| `H1_001N` |住房总数|
| `H1_002N` |已占用住房单元|

- --

## 响应格式
所有数据响应都是**数组的JSON数组**。第一个数组始终是列标题；后续数组是数据行。

```json
[
  ["NAME", "B01001_001E", "B19013_001E", "state", "county"],
  ["Los Angeles County, California", "10014009", "73538", "06", "037"],
  ["San Diego County, California", "3298634", "85750", "06", "073"]
]
```

- 值是字符串（甚至数字）。
- 丢失或不可用的数据可能显示为 `null`、`"-"` 或 `"N"`。
- 注释值：`"-"`（示例案例太少）， `"N"`（不可用）、`"(X)"`（不适用）。

## 备注
- 始终在 `get` 参数中包含 `NAME` 以获得人类可读的地理标签。
- `E` 后缀表示“估计”；使用 `M` 后缀作为误差幅度（例如，`B19013_001M`）。
- 变量发现：浏览 https://api.census.gov/data/{year}/acs/acs5/variables.html 获取可搜索表。
- 对于 ACS，5 年估计覆盖所有地区，但较当前； 1 年仅涵盖较大的地理区域，但时间较近。
- 组端点：`?get=group(B01001)` 检索表组中的所有变量。
