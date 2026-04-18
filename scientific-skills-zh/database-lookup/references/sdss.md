# SDSS SkyServer API

## 基本 URL

```
https://skyserver.sdss.org/dr18/SkyServerWS
```

 将 `dr18` 替换为所需的数据发布（例如，`dr17`、`dr16`）。

## 身份验证

无需 API 密钥。所有端点都是公共的。

## 关键端点

### 1. SQL搜索（CasJobs风格的自由格式SQL）

```
GET /SearchTools/SqlSearch
```

|参数|类型 |描述 |
|-----------|--------|-------------|
| `cmd` |字符串| **必需。** 针对 SDSS CasJobs 架构的 SQL 查询。 |
| `format` |字符串| `json`、`xml`、`csv`、`html`、`votable`。默认值：`html`。 |

* *示例 — 查询 10 个星系：**
```
https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch?cmd=SELECT TOP 10 objid,ra,dec,u,g,r,i,z FROM PhotoObj WHERE type=3&format=json
```

 类型代码：`3` = 星系，`6` = 恒星.

* *响应(JSON):**
```json
[
  {"Rows": [
    {"objid": 1237645941825863680, "ra": 195.123, "dec": 2.456, "u": 22.1, "g": 20.8, "r": 19.5, "i": 19.1, "z": 18.9}
  ]}
]
```

### 2.径向搜索

```
GET /SearchTools/RadialSearch
```

|参数|类型 |描述 |
|--------------|--------|------------|
| `ra` |浮动| **必填。** 赤经（度）。 |
| `dec` |浮动| **必填。** 赤纬（度）。 |
| `radius` |浮动|搜索半径（以弧分为单位）。默认值：1。|
| `format` |字符串| `json`、`xml`、`csv`。 |
| `limit` |整数 |最大结果。 |
| `objtype` |字符串|过滤器：`star`、`galaxy`，或全部留空。 |

* *示例 — RA=180、Dec=+0.5 2 弧分以内的对象：**
```
https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/RadialSearch?ra=180&dec=0.5&radius=2&format=json&limit=10
```

### 3. 矩形搜索

```
GET /SearchTools/RectangularSearch
```

|参数|类型 |描述|
|------------|--------|-------------|
| `min_ra` |浮动|最小 RA（度）。 |
| `max_ra` |浮动|最大 RA（度）。 |
| `min_dec` |浮动|最小十二月（度）。 |
| `max_dec` |浮动|最大减速度（度）。 |
| `format` |字符串| `json`、`xml`、`csv`。 |
| `limit` |整数 |最大结果。 |

### 4. 通过 ObjID

```
GET /SearchTools/SqlSearch?cmd=SELECT * FROM PhotoObj WHERE objid={objid}&format=json
```

### 进行对象查找 5. 通过 Plate-MJD-Fiber

```
GET /SearchTools/SqlSearch?cmd=SELECT * FROM SpecObj WHERE plate={plate} AND mjd={mjd} AND fiberid={fiberid}&format=json
```

### 进行光谱搜索 6. 图像剪切服务

```
GET /ImgCutout/getjpeg
```

|参数|类型 |描述|
|---------|--------|-------------|
| `ra` |浮动| **必填。** RA（度）。 |
| `dec` |浮动| **必填。** 十二月（度）。 |
| `scale` |浮动|弧秒/像素。默认值：0.396127。 |
| `width` |整数 |图像宽度（以像素为单位）。默认值：512。|
| `height` |整数 |图像高度（以像素为单位）。默认值：512。|

* *示例：**
```
https://skyserver.sdss.org/dr18/SkyServerWS/ImgCutout/getjpeg?ra=180.0&dec=0.5&scale=0.4&width=256&height=256
```

返回 JPEG 图像数据。

### 7. 频谱图/数据

Spectrum FITS 文件可以从科学档案馆检索服务器：
```
https://data.sdss.org/sas/dr18/spectro/sdss/redux/{run2d}/spectra/{plate}/spec-{plate}-{mjd}-{fiberid}.fits
```

## 重要的SQL表

|表|描述 |
|-------------|--------------|
| `PhotoObj` |光度测量（位置、幅度）。 |
| `SpecObj` |光谱测量（红移、分类）。 |
| `Galaxy` | PhotoObj 的视图已过滤为星系。 |
| `Star` | PhotoObj 的视图已过滤为星星。 |

## 速率限制

没有正式记录的速率限制。返回非常大结果集的查询可能会超时。在 SQL 查询中使用 `TOP N` 来限制结果。对于批量数据，请使用 CasJobs (https://skyserver.sdss.org/CasJobs/)和免费帐户。
