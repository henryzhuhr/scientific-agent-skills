# SIMBAD 天文数据库 (CDS Strasbourg)

## 基本 URL

* *TAP 端点（推荐）：**
```
https://simbad.cds.unistra.fr/simbad/sim-tap/sync
```

* *旧脚本接口：**
```
https://simbad.cds.unistra.fr/simbad/sim-script
```

* *简单查询端点：**
```
https://simbad.cds.unistra.fr/simbad/sim-id
https://simbad.cds.unistra.fr/simbad/sim-coo
```

## 身份验证

无需 API 密钥。所有端点都是公共的。

## 关键端点

### 1. TAP 查询（ADQL — 建议以编程方式使用）

```
GET /simbad/sim-tap/sync?request=doQuery&lang=adql&format={format}&query={ADQL}
```

|参数|类型 |描述|
|---------|--------|-------------|
| `request` |字符串| `doQuery` |
| `lang` |字符串| `adql` |
| `format` |字符串| `json`、`votable`、`csv`、`tsv`。 |
| `query` |字符串| **必需。** ADQL 查询。 |

* *示例 — 按名称查找对象：**
```
https://simbad.cds.unistra.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=json&query=SELECT basic.OID, ra, dec, main_id, otype FROM basic JOIN ident ON oid = ident.oidref WHERE id = 'M31'
```

* *示例 — 圆锥搜索（坐标 5 弧分内的对象）：**
```
https://simbad.cds.unistra.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=json&query=SELECT TOP 50 main_id, ra, dec, otype FROM basic WHERE CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', 10.684, 41.269, 0.083)) = 1
```
 注意：CIRCLE 中的半径以度为单位（5 弧分 = 0.083） deg).

* *示例 — 按类型划分的对象（例如，所有脉冲星）：**
```
https://simbad.cds.unistra.fr/simbad/sim-tap/sync?request=doQuery&lang=adql&format=json&query=SELECT TOP 100 main_id, ra, dec, otype FROM basic WHERE otype = 'Pulsar'
```

### 2. 标识符查询（简单查找）

```
GET /simbad/sim-id?Ident={name}&output.format=votable
```

|参数|类型 |描述 |
|------------------|--------|-------------|
| `Ident` |字符串| **必填。** 对象名称（例如，`M31`、`Sirius`、`NGC 1275`）。 |
| `output.format` |字符串| `votable`、`html`。 |

* *示例：**
```
https://simbad.cds.unistra.fr/simbad/sim-id?Ident=M31&output.format=votable
```

### 3、坐标查询

```
GET /simbad/sim-coo?Coord={coords}&Radius={radius}&Radius.unit={unit}&output.format=votable
```

|参数|类型 |描述 |
|----------------|--------|-------------|
| `Coord` |字符串| **必填。** 坐标，例如 `10.684 +41.269` 或 `00 42 44 +41 16 09`。 |
| `Radius` |浮动|搜索半径。默认值：2。|
| `Radius.unit` |字符串| `arcmin`、`arcsec`、`deg`。默认值：`arcmin`。 |
| `output.format`|字符串| `votable`、`html`。 |

* *示例：**
```
https://simbad.cds.unistra.fr/simbad/sim-coo?Coord=10.684+%2B41.269&Radius=5&Radius.unit=arcmin&output.format=votable
```

### 4.脚本接口（用于多命令查询）

```
POST /simbad/sim-script
Content-Type: application/x-www-form-urlencoded
script=format+object+"%MAIN_ID+|+%RA+|+%DEC+|+%OTYPE"\nquery+id+M31
```

## 关键TAP表

|表|描述 |
|-----------------|------------------------|
| `basic` |核心数据：坐标、main_id、物体类型。 |
| `ident` |对象的所有已知标识符。 |
| `flux` |通量/幅度测量。 |
| `mesVelocities` |径向速度测量。 |
| `mesDistance` |距离测量。 |
| `otypedef` |对象类型定义/标签。 |
| `allfluxes` |所有通量数据均已加入。 |

## 常见对象类型 (otype)

`Star`、`Galaxy`、`Pulsar`、`QSO`、`Nebula`、`GlobCluster`、`RadioSource`、`X-raySource`、 `SNRemnant`

## 响应格式 (TAP JSON)

```json
{
  "metadata": [
    {"name": "main_id", "datatype": "char"},
    {"name": "ra", "datatype": "double"},
    {"name": "dec", "datatype": "double"}
  ],
  "data": [
    ["M 31", 10.6847, 41.2687]
  ]
}
```

## 速率限制

没有记录正式的速率限制。 SIMBAD 要求自动化脚本在查询之间包含合理的延迟。非常大的 TAP 查询可能会超时；使用 `TOP N` 限制结果或在 `/simbad/sim-tap/async`.
 切换到异步 TAP
