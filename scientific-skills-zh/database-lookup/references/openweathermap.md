# OpenWeatherMap API 参考

## 基本 URL
```
https://api.openweathermap.org
```

## 身份验证
- **API 密钥：必需。** 在 https://home.openweathermap.org/users/sign_up
 注册免费密钥 - 作为查询参数传递： `&appid=YOUR_KEY`
- 免费套餐密钥在注册后几小时内激活。

## 速率限制（免费套餐）
- **每分钟 60 次调用**（某些端点每天 1,000 次调用）。
- **当前天气、5 天天气预报、地理编码：** 免费提供tier.
- **一次通话 3.0：** 需要订阅（每天 1,000 次免费通话，需使用信用卡存档）。
- **历史数据、空气污染历史：** 需要扩展范围的付费计划。

- --

## 关键端点

### 1. 当前天气
```
GET /data/2.5/weather
```

* *参数：**
|参数|类型 |必填 |默认|描述|
|---------|--------|---------|----------|-------------|
| `q` |字符串|条件。    | - |城市名称，可选地带有州/国家：`London`、`London,GB`、`Portland,OR,US`。 |
| `lat` |浮动|条件。    | - |纬度（与 `lon` 一起使用）。 |
| `lon` |浮动|条件。    | - |经度（与 `lat` 一起使用）。 |
| `id` |整数 |条件。    | - |城市 ID（来自 OWM 城市列表）。 |
| `zip` |字符串|条件。    | - |国家/地区邮政编码：`90210,US`、`SW1,GB`。 |
| `units` |字符串|没有 | `standard` | `standard`（开尔文）、`metric`（摄氏度）、`imperial`（华氏度）。 |
| `lang` |字符串|没有 | `en` |描述的语言代码。 |
| `appid` |字符串|是的 | - | API 密钥。 |

 需要一个位置参数（`q`、`lat`+`lon`、`id` 或 `zip`）。

* *示例：**
```
https://api.openweathermap.org/data/2.5/weather?lat=40.7128&lon=-74.0060&units=metric&appid=YOUR_KEY
```

* *响应：**
```json
{
  "coord": {"lon": -74.006, "lat": 40.7128},
  "weather": [
    {
      "id": 800,
      "main": "Clear",
      "description": "clear sky",
      "icon": "01d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 22.5,
    "feels_like": 21.8,
    "temp_min": 20.1,
    "temp_max": 24.3,
    "pressure": 1013,
    "humidity": 55,
    "sea_level": 1013,
    "grnd_level": 1010
  },
  "visibility": 10000,
  "wind": {"speed": 3.6, "deg": 220, "gust": 5.1},
  "clouds": {"all": 0},
  "dt": 1700000000,
  "sys": {
    "country": "US",
    "sunrise": 1699960000,
    "sunset": 1699996000
  },
  "timezone": -18000,
  "id": 5128581,
  "name": "New York",
  "cod": 200
}
```

### 2. 5天/3小时预测（免费）
```
GET /data/2.5/forecast
```
以3小时为间隔返回5天的预测数据（40个数据）点）。与当前天气相同的位置参数。

* *附加参数：**
|参数|类型 |描述|
|-----------|------|-------------|
| `cnt` |整数 |返回的 3 小时步数（最多 40）。 |

* *示例：**
```
https://api.openweathermap.org/data/2.5/forecast?q=London,GB&units=metric&cnt=8&appid=YOUR_KEY
```

* *响应：**
```json
{
  "cod": "200",
  "message": 0,
  "cnt": 8,
  "list": [
    {
      "dt": 1700000000,
      "main": {
        "temp": 10.5,
        "feels_like": 8.2,
        "temp_min": 9.8,
        "temp_max": 10.5,
        "pressure": 1020,
        "humidity": 80
      },
      "weather": [{"id": 802, "main": "Clouds", "description": "scattered clouds", "icon": "03d"}],
      "clouds": {"all": 40},
      "wind": {"speed": 4.1, "deg": 250},
      "visibility": 10000,
      "pop": 0.2,
      "dt_txt": "2024-01-15 12:00:00"
    }
  ],
  "city": {
    "id": 2643743,
    "name": "London",
    "coord": {"lat": 51.5085, "lon": -0.1257},
    "country": "GB",
    "population": 1000000,
    "timezone": 0,
    "sunrise": 1699950000,
    "sunset": 1699982000
  }
}
```
`pop` 是降水概率（0.0 到 1.0）。

### 3.地理编码
```
GET /geo/1.0/direct
GET /geo/1.0/reverse
GET /geo/1.0/zip
```

* *直接地理编码（城市名称到坐标）：**
```
https://api.openweathermap.org/geo/1.0/direct?q=London,GB&limit=5&appid=YOUR_KEY
```
返回`{name, lat, lon, country, state}`.

的数组**反向地理编码（坐标到城市） name):**
```
https://api.openweathermap.org/geo/1.0/reverse?lat=51.5085&lon=-0.1257&limit=1&appid=YOUR_KEY
```

* *邮政编码地理编码:**
```
https://api.openweathermap.org/geo/1.0/zip?zip=90210,US&appid=YOUR_KEY
```

### 4. One Call API 3.0（需要订阅）
```
GET /data/3.0/onecall
```
返回当前、每分钟（1小时）、每小时的综合端点（48小时）、每日（8天）、一次调用提醒。

* *参数：**
|参数|类型 |必填 |描述 |
|---------|--------|---------|-------------|
| `lat` |浮动|是的 |纬度。 |
| `lon` |浮动|是的 |经度。 |
| `exclude` |字符串|没有 |要排除的逗号分隔部分：`current`、`minutely`、`hourly`、`daily`、`alerts`。 |
| `units` |字符串|没有 | `standard`、`metric`、`imperial`。 |
| `appid` |字符串|是的 | API 密钥。 |

* *示例：**
```
https://api.openweathermap.org/data/3.0/onecall?lat=40.7128&lon=-74.006&exclude=minutely,alerts&units=metric&appid=YOUR_KEY
```

### 5. 空气污染
```
GET /data/2.5/air_pollution
GET /data/2.5/air_pollution/forecast
GET /data/2.5/air_pollution/history
```

* *参数：** `lat`、`lon`、 `appid`（必填）。对于历史记录：`start` 和 `end`（Unix 时间戳）。

* *示例：**
```
https://api.openweathermap.org/data/2.5/air_pollution?lat=40.7128&lon=-74.006&appid=YOUR_KEY
```

* *响应：**
```json
{
  "coord": {"lon": -74.006, "lat": 40.7128},
  "list": [
    {
      "main": {"aqi": 2},
      "components": {
        "co": 230.31,
        "no": 0.5,
        "no2": 15.0,
        "o3": 68.0,
        "so2": 2.5,
        "pm2_5": 8.1,
        "pm10": 12.3,
        "nh3": 1.0
      },
      "dt": 1700000000
    }
  ]
}
```
AQI 等级：1=良好、2=一般、3=中等、 4=差，5=非常差。成分单位为ug/m3.

- --

## 天气状况代码
|范围 |类别|
|---------|----------|
| 2xx |雷雨|
| 3xx |毛毛雨|
| 5xx |雨 |
| 6xx |雪|
| 7xx |大气（雾、雾、霾）|
| 800 |清除|
| 80 倍 |云 |

天气图标：`https://openweathermap.org/img/wn/{icon}@2x.png`

## 免费套餐与付费套餐
|端点|免费|订阅 |
|---------|------|------------|
|当前天气 |是的 |是 |
| 5 天/3 小时预报 |是的 |是 |
|地理编码 |是的 |是 |
|空气污染（当前）|是的 |是 |
|一通3.0 | 1000/天（需要信用卡）|是 |
|历史天气 |没有 |是 |
| 16 天每日预报 |没有 |是 |
| 30 天气候预报 |没有 |是 |

## 备注
- 所有时间戳（`dt`、`sunrise`、`sunset`）均为 **Unix 纪元秒 (UTC)**。
- `timezone` 字段以秒为单位相对于 UTC 的偏移量（例如 -18000 = UTC-5).
- 默认温度单位为开尔文。始终指定 `units=metric` 或 `units=imperial`。
  - 城市名称查询 (`q=`)可能不明确。首选 `lat`+`lon` 以获得精确度，如果需要，请首先使用地理编码。
- 天气图标 URL 模式：`https://openweathermap.org/img/wn/{icon}@2x.png`（例如，`01d` 表示晴天）。
- 错误响应返回 `{"cod": 401, "message": "Invalid API key"}` 或类似内容。
