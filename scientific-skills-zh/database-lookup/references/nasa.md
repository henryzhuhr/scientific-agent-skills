# NASA APIs

## 基本 URL

```
https://api.nasa.gov
```

## 身份验证

所有端点都需要作为 `api_key` 查询参数传递的 API 密钥。
- 在以下位置获取免费密钥：https://api.nasa.gov/#signUp
- 演示密钥： `DEMO_KEY`（速率限制：每个 IP 30 个请求/小时，50 个请求/天）
- 注册密钥：1,000 个请求/小时

## 关键端点

### 1. APOD（天文图片）天）

```
GET /planetary/apod
```

* *参数：**

|参数|类型 |描述|
|------------|--------|-------------|
| `api_key` |字符串| **必需。** API 密钥。 |
| `date` |字符串|年-月-日。默认：今天。 |
| `start_date` |字符串|日期范围的开始 (YYYY-MM-DD)。 |
| `end_date` |字符串|日期范围结束 (YYYY-MM-DD)。 |
| `count` |整数 |返回 N 张随机图像（不能与日期/范围组合）。 |
| `thumbs` |布尔 |返回视频条目的缩略图 URL。 |

* *示例：**
```
https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=2024-01-15
```

* *响应 (JSON)：**
```json
{
  "date": "2024-01-15",
  "title": "...",
  "explanation": "...",
  "url": "https://apod.nasa.gov/apod/image/...",
  "hdurl": "https://apod.nasa.gov/apod/image/...",
  "media_type": "image",
  "copyright": "..."
}
```

### 2. NEO — 近地天体（小行星） NeoWs)

```
GET /neo/rest/v1/feed
```

* *参数：**

|参数|类型 |描述|
|--------------|--------|------------|
| `api_key` |字符串| **必填。** |
| `start_date` |字符串|年-月-日。默认：今天。 |
| `end_date` |字符串|年-月-日。自开始起最多 7 天。 |

* *示例：**
```
https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-03&api_key=DEMO_KEY
```

* *按小行星 ID 查找：**
```
GET /neo/rest/v1/neo/{asteroid_id}?api_key=DEMO_KEY
```

* *浏览全部：**
```
GET /neo/rest/v1/neo/browse?api_key=DEMO_KEY
```

* *响应结构：** `near_earth_objects` 按日期键入，每个对象包含 `name`、`nasa_jpl_url`、`estimated_diameter`、`close_approach_data`、`is_potentially_hazardous_asteroid`.

### 的对象数组 3. 火星漫游者照片

```
GET /mars-photos/api/v1/rovers/{rover}/photos
```

流动站：`curiosity`、`opportunity`、`spirit`、`perseverance`

* *参数：**

|参数|类型 |说明|
|------------|--------|-------------|
| `api_key` |字符串| **必填。** |
| `sol` |整数 |火星太阳（白天）。使用 `sol` 或 `earth_date`，不能同时使用两者。 |
| `earth_date` |字符串|年-月-日。 |
| `camera` |字符串|按相机过滤：`FHAZ`、`RHAZ`、`MAST`、`CHEMCAM`、`NAVCAM`等|
| `page` |整数 |每页 25 个结果。 |

* *示例：**
```
https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera=NAVCAM&api_key=DEMO_KEY
```

* *流动站清单（任务元数据）：**
```
GET /mars-photos/api/v1/manifests/{rover}?api_key=DEMO_KEY
```

* *响应：** `photos` 数组，每个包含 `id`， `sol`、`camera`（含 `full_name`）、`img_src`、`earth_date`、`rover`.

## 速率限制

|钥匙类型|每小时限制 |每日限价|
|------------|-------------|------------|
| `DEMO_KEY` | 30/小时 | 50/天|
|注册| 1,000/小时 |无限|

速率限制标头：`X-RateLimit-Limit`、`X-RateLimit-Remaining`.
