# NASA 系外行星档案 API

## 基本 URL

```
https://exoplanetarchive.ipac.caltech.edu
```

## 身份验证

无需 API 密钥。所有端点都是公共的。

## 关键端点

### 1. TAP 服务（推荐 — 当前方法）

```
GET /TAP/sync?query={ADQL}&format={format}
```

|参数|类型 |描述|
|------------|--------|-------------|
| `query` |字符串| **必需。** ADQL 查询。 |
| `format` |字符串| `json`、`csv`、`votable`、`tsv`、`ipac`。默认值：`votable`。 |

* *示例 - 已确认的行星，具有关键参数：**
```
https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=SELECT pl_name,hostname,sy_dist,pl_orbper,pl_rade,pl_bmasse,disc_year,discoverymethod FROM ps WHERE default_flag=1 ORDER BY disc_year DESC&format=json
```

 * *示例 - 位于宜居带的行星（粗略估计）：**
```
https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=SELECT TOP 50 pl_name,hostname,pl_orbsmax,st_teff,pl_rade FROM ps WHERE default_flag=1 AND pl_orbsmax BETWEEN 0.8 AND 1.5 AND st_teff BETWEEN 4000 AND 7000&format=json
```

 * *示例 - 发现的行星TESS:**
```
https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=SELECT pl_name,pl_rade,pl_orbper,disc_year FROM ps WHERE default_flag=1 AND disc_facility='Transiting Exoplanet Survey Satellite (TESS)'&format=json
```

* *示例 - 通过发现方法计算行星：**
```
https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=SELECT discoverymethod, COUNT(*) as cnt FROM ps WHERE default_flag=1 GROUP BY discoverymethod ORDER BY cnt DESC&format=json
```

### 2. 旧版 API（较旧，仍然功能）

```
GET /cgi-bin/nstedAPI/nph-nstedAPI?table={table}&format={format}&where={conditions}&select={columns}
```

* *示例：**
```
https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=ps&select=pl_name,pl_orbper,pl_rade&where=disc_year=2023&format=json
```

注意：旧版 API 已弃用，转而使用 TAP。将 TAP 用于新应用。

## 关键 TAP 表

|表|描述 |
|--------|-------------|
| `ps` | **行星系统** — 每个行星每个参考一行。使用 `default_flag=1` 作为默认/最佳参数集。 |
| `pscomppars` | **行星系统复合参数** — 每个行星一行，具有来自多个参考的最佳拟合值。 |
| `stellarhosts` |主星的恒星属性。 |
| `td` |时间序列数据（传输曲线、RV 曲线）。 |
| `keplernames` |开普勒感兴趣对象交叉引用。 |
| `k2names` | K2 活动交叉引用。 |
| `toi` | TESS 感兴趣的对象。 |

## 关键列（ps 表）

|专栏 |描述 |
|------------------|------------------------|
| `pl_name` |行星名称（例如“Kepler-22 b”）。 |
| `hostname` |主持人明星名字。 |
| `default_flag` | 1 = 该行星的默认参数设置。 |
| `disc_year` |发现年。 |
| `discoverymethod` | `Transit`、`Radial Velocity`、`Imaging`、`Microlensing`等|
| `pl_orbper` |轨道周期（天）。 |
| `pl_orbsmax` |半长轴 (AU)。 |
| `pl_rade` |行星半径（地球半径）。 |
| `pl_bmasse` |行星质量（地球质量）。 |
| `pl_eqt` |平衡温度（K）。 |
| `sy_dist` |到系统的距离（秒差距）。 |
| `st_teff` |恒星有效温度（K）。 |
| `st_rad` |恒星半径（太阳半径）。 |
| `st_mass` |恒星质量（太阳质量）。 |
| `disc_facility` |发现设施名称。 |

## 响应格式 (TAP JSON)

```json
{
  "metadata": [
    {"name": "pl_name", "datatype": "char"},
    {"name": "pl_orbper", "datatype": "double"}
  ],
  "data": [
    ["Kepler-22 b", 289.8623]
  ]
}
```

## 速率限制

无需 API 密钥或身份验证。没有记录正式的速率限制，但存档要求用户避免过多的自动查询。结果集太大可能会导致超时；在 ADQL 中使用 `TOP N` 或使用 `OFFSET` 和 `MAXREC` 进行分页。

 对于非常大的下载，请使用批量下载界面：
```
https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS
```
