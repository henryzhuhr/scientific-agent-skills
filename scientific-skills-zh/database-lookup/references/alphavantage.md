# Alpha Vantage API 参考

## 概述
Alpha Vantage 提供免费的 API，用于实时和历史股票价格、外汇汇率、加密货币数据、技术指标和基本数据（收益、资产负债表、损益表）。涵盖全球股票、ETF、共同基金和商品。

## 基本 URL
```
https://www.alphavantage.co/query
```

 所有请求都使用带有 `function` 参数的单个端点来选择数据类型。

## 身份验证
- **API 密钥：必需。** 在以下位置获取免费密钥https://www.alphavantage.co/support/#api-key
- 作为查询参数传递：`&apikey=YOUR_KEY`

## 速率限制
- **免费套餐：** 每天 25 个请求。每分钟 5 次调用（截至 2024 年末；之前为 5 次/分钟 + 500 次/天）。
- **高级层**可用于更高的限制（30、75、150+ 次调用/分钟）。
- 超出限制会返回礼貌的 JSON 消息，而不是错误代码。

- --

## 密钥端点（通过`function`参数）

### 1.股票时间序列

#### 日内
```
GET /query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={key}
```
|参数|必填 |值|
|---------|---------|--------|
| `symbol` |是的 |股票代码（例如，`AAPL`、`MSFT`）|
| `interval` |是的 | `1min`、`5min`、`15min`、`30min`、`60min` |
| `outputsize` |没有 | `compact`（最后100点，默认）或`full`（完整历史）|
| `adjusted` |没有 | `true`（默认）或 `false` |
| `datatype` |没有 | `json`（默认）或 `csv` |

* *示例：**
```
https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&apikey=YOUR_KEY
```

#### 每日
```
GET /query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=YOUR_KEY
```

#### 每日（调整为分割/股息）
```
GET /query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=AAPL&outputsize=full&apikey=YOUR_KEY
```

#### 每周/每月
```
GET /query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=AAPL&apikey=YOUR_KEY
GET /query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=AAPL&apikey=YOUR_KEY
```

* *响应（每日）：**
```json
{
  "Meta Data": {
    "1. Information": "Daily Prices (open, high, low, close) and Volumes",
    "2. Symbol": "AAPL",
    "3. Last Refreshed": "2024-11-01",
    "4. Output Size": "Compact",
    "5. Time Zone": "US/Eastern"
  },
  "Time Series (Daily)": {
    "2024-11-01": {
      "1. open": "228.6900",
      "2. high": "229.8600",
      "3. low": "225.8200",
      "4. close": "228.5200",
      "5. volume": "50423432"
    },
    "2024-10-31": {
      "1. open": "229.3400",
      "2. high": "230.2000",
      "3. low": "226.3700",
      "4. close": "227.5500",
      "5. volume": "51235678"
    }
  }
}
```

- --

### 2.股票搜索（代码查找）
```
GET /query?function=SYMBOL_SEARCH&keywords={query}&apikey={key}
```

* *示例：**
```
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=microsoft&apikey=YOUR_KEY
```

* *回复：**
```json
{
  "bestMatches": [
    {
      "1. symbol": "MSFT",
      "2. name": "Microsoft Corporation",
      "3. type": "Equity",
      "4. region": "United States",
      "5. marketOpen": "09:30",
      "6. marketClose": "16:00",
      "7. timezone": "UTC-04",
      "8. currency": "USD",
      "9. matchScore": "1.0000"
    }
  ]
}
```

- --

### 3. 全球报价（实时价格）
```
GET /query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=YOUR_KEY
```

 返回单个交易品种的最新价格、交易量、变化、变化百分比。

- --

### 4. 外汇（FX）汇率

#### 实时交易汇率
```
GET /query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=EUR&apikey=YOUR_KEY
```

#### FX时间序列
```
GET /query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&apikey=YOUR_KEY
GET /query?function=FX_WEEKLY&from_symbol=EUR&to_symbol=USD&apikey=YOUR_KEY
GET /query?function=FX_MONTHLY&from_symbol=EUR&to_symbol=USD&apikey=YOUR_KEY
GET /query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=5min&apikey=YOUR_KEY
```

- --

#### 5.加密货币

#### 实时兑换汇率
```
GET /query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey=YOUR_KEY
```

#### 加密时间系列
```
GET /query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey=YOUR_KEY
GET /query?function=DIGITAL_CURRENCY_WEEKLY&symbol=BTC&market=USD&apikey=YOUR_KEY
GET /query?function=DIGITAL_CURRENCY_MONTHLY&symbol=BTC&market=USD&apikey=YOUR_KEY
```

- --

### 6.技术指标
```
GET /query?function={INDICATOR}&symbol={symbol}&interval={interval}&time_period={n}&series_type={type}&apikey={key}
```

|参数|必填 |描述|
|---------|----------|----------|
| `function` |是的 |指标名称（见下表）|
| `symbol` |是的 |股票代码 |
| `interval` |是的 | `1min`、`5min`、`15min`、`30min`、`60min`、`daily`、`weekly`、`monthly` |
| `time_period` |是* |用于计算的数据点数量（例如，RSI 为 14）|
| `series_type` |是* | `close`、`open`、`high`、`low` |

* 大多数指标需要；有些（如 MACD、BBANDS）有附加参数。

* *常用指标功能：**
`SMA`、`EMA`、`WMA`、`DEMA`、`TEMA`、`VWAP`、 `RSI`、`MACD`、`STOCH`、`ADX`、`CCI`、`AROON`、`BBANDS`、`AD`、`OBV`、`ATR`、 `WILLR`、`MOM`

* *示例 -- RSI（14 天）：**
```
https://www.alphavantage.co/query?function=RSI&symbol=AAPL&interval=daily&time_period=14&series_type=close&apikey=YOUR_KEY
```

* *示例 -- MACD：**
```
https://www.alphavantage.co/query?function=MACD&symbol=AAPL&interval=daily&series_type=close&apikey=YOUR_KEY
```

- --

### 7.基本数据

#### 公司概况
```
GET /query?function=OVERVIEW&symbol=AAPL&apikey=YOUR_KEY
```
回报：市值、市盈率、每股收益、股息收益率、52周高/低、行业、描述和~60其他fields.

#### 损益表
```
GET /query?function=INCOME_STATEMENT&symbol=AAPL&apikey=YOUR_KEY
```

#### 资产负债表
```
GET /query?function=BALANCE_SHEET&symbol=AAPL&apikey=YOUR_KEY
```

#### 现金流量
```
GET /query?function=CASH_FLOW&symbol=AAPL&apikey=YOUR_KEY
```

#### 收益
```
GET /query?function=EARNINGS&symbol=AAPL&apikey=YOUR_KEY
```

返回年度和季度收益（EPS、预计EPS、惊喜）。

- --

### 8. 商品和经济指标
```
GET /query?function=WTI&interval=monthly&apikey=YOUR_KEY
GET /query?function=BRENT&interval=monthly&apikey=YOUR_KEY
GET /query?function=NATURAL_GAS&interval=monthly&apikey=YOUR_KEY
GET /query?function=COPPER&interval=monthly&apikey=YOUR_KEY
GET /query?function=ALUMINUM&interval=monthly&apikey=YOUR_KEY
GET /query?function=WHEAT&interval=monthly&apikey=YOUR_KEY
GET /query?function=CORN&interval=monthly&apikey=YOUR_KEY
GET /query?function=COTTON&interval=monthly&apikey=YOUR_KEY
GET /query?function=SUGAR&interval=monthly&apikey=YOUR_KEY
GET /query?function=COFFEE&interval=monthly&apikey=YOUR_KEY
```

E经济指标：
```
GET /query?function=REAL_GDP&interval=quarterly&apikey=YOUR_KEY
GET /query?function=CPI&interval=monthly&apikey=YOUR_KEY
GET /query?function=INFLATION&apikey=YOUR_KEY
GET /query?function=RETAIL_SALES&apikey=YOUR_KEY
GET /query?function=UNEMPLOYMENT&apikey=YOUR_KEY
GET /query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey=YOUR_KEY
GET /query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey=YOUR_KEY
```

- --

## 备注
- 所有值均以 JSON 中的字符串形式返回。
- JSON 键使用编号前缀（例如，`"1. open"`、`"2. high"`）。
- 时间序列数据由日期/时间戳字符串而不是数组键入。
- 当速率受限时，API返回：`{"Note": "Thank you for using Alpha Vantage! ..."}`
- 对于`outputsize=full`，每日数据回溯20+年。
  - `datatype=csv` 选项为任何端点返回更简单的 CSV 输出。
  - 免费套餐非常严格（25/天）。对于生产用途，建议使用高级密钥。
