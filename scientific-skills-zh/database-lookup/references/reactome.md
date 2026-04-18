# Reactome Content Service REST API

## 基本 URL

```
https://reactome.org/ContentService
```

 无需身份验证。默认为 JSON。

## 关键端点

### 搜索（跨通路、反应、蛋白质的全文）

```
GET /search/query?query={term}
```

 参数：
- `query`（必需）— 搜索词（例如“细胞凋亡”、“TP53”、 "R-HSA-109581")
- `species` — 按物种过滤（例如“智人”）
- `types` — 按类型过滤：`Pathway`、`Reaction`、`Protein`、`Complex`、 `SmallMolecule`
- `cluster` — 布尔值，聚类结果（默认 true）
- `rows` — 页面大小
- `Start row` — 偏移量分页

示例：
```
/search/query?query=apoptosis&species=Homo+sapiens&types=Pathway
```

响应：
```json
{
  "results": [
    {
      "typeName": "Pathway",
      "rows": [
        {
          "dbId": 109581,
          "stId": "R-HSA-109581",
          "name": "Apoptosis",
          "species": ["Homo sapiens"],
          "summation": ["..."]
        }
      ]
    }
  ],
  "found": 42
}
```

### 自动完成
```
GET /search/suggest?query={partial_term}
```

### 的顶级路径物种
```
GET /data/pathways/top/{species}
```
示例：`/data/pathways/top/Homo+sapiens`

### 路径详细信息
```
GET /data/query/{id}
```
其中`{id}`是一个稳定的ID，如`R-HSA-109581`或数字dbId。

### 包含在a中的事件Pathway
```
GET /data/pathway/{id}/containedEvents
```

### 反应的参与者
```
GET /data/event/{id}/participants
```

### 事件的祖先
```
GET /data/event/{id}/ancestors
```

### 将外部 ID 映射到路径（例如 UniProt 到 Reactome）路径）
```
GET /data/mapping/{resource}/{id}/pathways
```
示例 — 查找 TP53 的路径 (UniProt P04637):
```
/data/mapping/UniProt/P04637/pathways
```

### 将外部 ID 映射到反应
```
GET /data/mapping/{resource}/{id}/reactions
```

### 通用实体查找
```
GET /data/query/{id}
```

### 事件的参考实体
```
GET /data/participants/{id}/referenceEntities
```

### 所有物种
```
GET /data/species/all
```

### 物种的事件层次结构（大响应）
```
GET /data/eventsHierarchy/{species}
```

## 稳定ID格式

`R-{species_code}-{number}`

|代码|种类 |
|---|---|
| HSA |智人|
|管理单元|小家鼠|
| RNO |褐家鼠 |
|二甲醚|黑腹果蝇 |
|中电 |线虫 |
|常设委员会 | S. cerevisiae |

## 用于映射的外部资源名称

`UniProt`、`ChEBI`、`ENSEMBL`、`miRBase`、`GeneCards`、`NCBI`

 同一参数的多个值：重复参数（例如`types=Pathway&types=Reaction`）.

## 速率限制

无需 API 密钥。没有发布正式的速率限制，但要合理——避免数百个并发请求。对于批量数据，请使用 Reactome 的可下载转储（MySQL、Neo4j、BioPAX、SBML）。
