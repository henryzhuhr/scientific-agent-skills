# Google Data Commons API

## 基本 URL

```
https://api.datacommons.org
```

## 身份验证

* *需要 API 密钥。** 从 Google Cloud Console 获取（启用 Data Commons API）。

作为查询参数传递：`&key=YOUR_KEY`

或作为标头： `X-API-Key: YOUR_KEY`

注意：许多端点无需密钥即可轻松使用，但建议使用密钥以实现可靠访问。

## 关键端点

### 1.获取统计值（单次观察）
```
GET /v2/observation
```
|参数|必填 |描述 |
|-------------|----------|------------------------------------------------------------|
|关键|是的 | API密钥|
|实体.dcids |是的 |放置 DCID（例如 `country/USA`、`geoId/06`）|
|变量.dcids|是的 |统计变量 DCID |
|日期 |没有 |具体日期或 `LATEST` |
|选择 |没有 |选择字段：`entity`、`variable`、`date`、`value` |

示例：
```
https://api.datacommons.org/v2/observation?key=YOUR_KEY&entity.dcids=country/USA&variable.dcids=Count_Person&date=LATEST&select=entity&select=variable&select=date&select=value
```

### 2.获取统计时间序列
```
GET /v2/observation
```
使用相同端点但省略 `date` 参数（或设置 `date=''`）以获取完整时间序列。

示例（美国人口时间序列）：
```
https://api.datacommons.org/v2/observation?key=YOUR_KEY&entity.dcids=country/USA&variable.dcids=Count_Person&select=entity&select=variable&select=date&select=value
```

### 3. 节点信息（实体的属性值）
```
GET /v2/node
```
|参数|必填 |描述 |
|---------|----------|----------------------------------------------------|
|关键|是的 | API密钥|
|节点 |是的 |节点 |
| 的 DCID财产 |是的 |属性表达式：`->prop`（出）、`<-prop`（入）|

示例（获取加利福尼亚州的属性）：
```
https://api.datacommons.org/v2/node?key=YOUR_KEY&nodes=geoId/06&property=->*
```

示例（获取地点名称）：
```
https://api.datacommons.org/v2/node?key=YOUR_KEY&nodes=geoId/06&property=->name
```

### 4. SPARQL 查询
```
POST /v2/sparql
```
Content-Type： `application/json`

Body:
```json
{
  "query": "SELECT ?name WHERE { ?state typeOf State . ?state name ?name . ?state containedInPlace country/USA }"
}
```

将 API 密钥作为查询参数或标头传递。

示例 (curl):
```
curl -X POST 'https://api.datacommons.org/v2/sparql?key=YOUR_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"query": "SELECT ?name WHERE { ?place typeOf Country . ?place name ?name } LIMIT 10"}'
```

### 5. 解析实体（将名称/坐标映射到DCID)
```
GET /v2/resolve
```
|参数|必填 |描述 |
|------------|----------|------------------------------------------------|
|关键|是的 | API密钥|
|节点 |是的 |要解析的实体标识符 |
|财产 |是的 | `<-description`（名称查找）或基于坐标的|

示例（按名称解析）：
```
https://api.datacommons.org/v2/resolve?key=YOUR_KEY&nodes=California&property=<-description->dcid
```

### 6. 搜索统计变量
```
GET /v2/variable/search
```
|参数|必填 |描述 |
|---------|----------|------------------------|
|关键|是的 | API密钥|
|查询 |是的 |搜索关键字|

示例：
```
https://api.datacommons.org/v2/variable/search?key=YOUR_KEY&query=unemployment+rate
```

## 常用DCID

### 地点
| DCID |描述 |
|--------------------------------|------------------------|
|国家/美国 |美国|
|国家/英国 |英国|
|国家/中国 |中国|
|地理编号/06 |加利福尼亚州|
| geoId/0667000 |旧金山市|
|地理ID/06085 |圣克拉拉县 |

### 统计变量
| DCID |描述 |
|--------------------------------------------------------|--------------------------------|
|人数 |总人口|
|受雇人数 |就业人员 |
| UnemploymentRate_Person | 失业率失业率|
|人收入中位数 |收入中位数|
|金额_经济活动_国内生产总值_名义 |名义GDP |
| Mean_ConsumerPriceIndex | 平均消费者价格指数消费者价格指数|
|计数_死亡 |死亡人数|
|过去 12 个月内 Count_Person_BelowPovertyLevel |贫困人口|
|中位数年龄人 |中位数年龄 |

## 响应格式

### 观察响应
```json
{
  "byVariable": {
    "Count_Person": {
      "byEntity": {
        "country/USA": {
          "orderedFacets": [
            {
              "facetId": "2176550201",
              "observations": [
                {
                  "date": "2020",
                  "value": 331449281
                },
                {
                  "date": "2021",
                  "value": 331893745
                }
              ]
            }
          ]
        }
      }
    }
  },
  "facets": {
    "2176550201": {
      "importName": "CensusACS5YearSurvey",
      "provenanceUrl": "https://www.census.gov/",
      "measurementMethod": "CensusACS5yrSurvey"
    }
  }
}
```

### 节点响应
```json
{
  "data": {
    "geoId/06": {
      "arcs": {
        "name": {
          "nodes": [
            {
              "value": "California"
            }
          ]
        }
      }
    }
  }
}
```

### SPARQL响应
```json
{
  "header": ["?name"],
  "rows": [
    { "cells": [{ "value": "Alabama" }] },
    { "cells": [{ "value": "Alaska" }] }
  ]
}
```

### 变量搜索响应
```json
{
  "variables": [
    {
      "dcid": "UnemploymentRate_Person",
      "displayName": "Unemployment Rate"
    }
  ]
}
```

## 速率限制

- 没有API密钥：非常有限（大约每分钟几个请求；可能会被阻止）。
- 有API密钥：没有正式发布，但通常很慷慨
- 实施客户端节流（建议 1-2 个请求/秒）。
- 通过 Data Commons 数据下载提供批量数据以进行大规模分析。

## 注释

- V2 API（以 `/v2/` 开头的路径）是当前推荐的版本。
- 较旧V1 端点（`/v1/bulk/observations/series`、`/stat/value` 等）仍然有效，但已弃用。
- DCID = 数据共享标识符。每个实体、统计变量和概念都有唯一的 DCID。
  - 知识图谱包括来自美国人口普查、世界银行、CDC、BLS、FBI 和许多其他来源的数据。
