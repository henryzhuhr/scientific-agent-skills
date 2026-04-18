# 开放目标平台 API

## 基本 URL

* *GraphQL API（主要，推荐）：**
```
https://api.platform.opentargets.org/api/v4/graphql
```

* *重要：** GraphQL 端点需要使用 `Content-Type: application/json` 的 HTTP POST。 WebFetch（仅限 GET）将不起作用 — 通过 shell 使用 `curl`：
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"query":"{ target(ensemblId: \"ENSG00000157764\") { approvedSymbol approvedName } }"}' \
  https://api.platform.opentargets.org/api/v4/graphql
```

* *REST API（更简单的查询）：**
```
https://api.platform.opentargets.org/api/v4
```

## 身份验证

无需 API 密钥。所有端点都是公共的。

## GraphQL API

所有 GraphQL 查询都作为 POST 请求发送到 GraphQL 端点。

```
POST https://api.platform.opentargets.org/api/v4/graphql
Content-Type: application/json

{
  "query": "...",
  "variables": { ... }
}
```

### 1. 目标信息（由 Ensembl Gene 提供） ID)

```graphql
query TargetInfo($ensemblId: String!) {
  target(ensemblId: $ensemblId) {
    id
    approvedSymbol
    approvedName
    biotype
    proteinIds {
      id
      source
    }
    tractability {
      label
      modality
      value
    }
    safetyLiabilities {
      event
      effects {
        direction
        dosing
      }
    }
    pathways {
      pathway
      pathwayId
    }
    functionDescriptions
    subcellularLocations {
      location
    }
  }
}
```

* *变量：** `{ "ensemblId": "ENSG00000141510" }`

* *URL 示例（简单查询也支持 GET）：**
```
https://api.platform.opentargets.org/api/v4/graphql?query={target(ensemblId:"ENSG00000141510"){id approvedSymbol approvedName biotype functionDescriptions}}
```

- --

### 2. 疾病信息（通过 EFO ID)

```graphql
query DiseaseInfo($efoId: String!) {
  disease(efoId: $efoId) {
    id
    name
    description
    therapeuticAreas {
      id
      name
    }
    synonyms {
      terms
    }
  }
}
```

* *变量：** `{ "efoId": "EFO_0000311" }`（癌症）

* *URL 示例：**
```
https://api.platform.opentargets.org/api/v4/graphql?query={disease(efoId:"EFO_0000311"){id name description therapeuticAreas{id name}}}
```

- --

### 3. 目标疾病关联

```graphql
query Associations($ensemblId: String!, $page: Pagination!) {
  target(ensemblId: $ensemblId) {
    approvedSymbol
    associatedDiseases(page: $page) {
      count
      rows {
        disease {
          id
          name
        }
        score
        datasourceScores {
          id
          score
        }
      }
    }
  }
}
```

* *变量：**
```json
{
  "ensemblId": "ENSG00000141510",
  "page": { "index": 0, "size": 10 }
}
```

* *URL示例：**
```
https://api.platform.opentargets.org/api/v4/graphql?query={target(ensemblId:"ENSG00000141510"){approvedSymbol associatedDiseases(page:{index:0,size:5}){count rows{disease{id name}score}}}}
```

- --

### 4.疾病-目标关联（从疾病方面）

```graphql
query DiseaseAssociations($efoId: String!, $page: Pagination!) {
  disease(efoId: $efoId) {
    name
    associatedTargets(page: $page) {
      count
      rows {
        target {
          id
          approvedSymbol
        }
        score
        datasourceScores {
          id
          score
        }
      }
    }
  }
}
```

* *变量：**
```json
{
  "efoId": "EFO_0000311",
  "page": { "index": 0, "size": 10 }
}
```

- --

### 5. 目标疾病的证据pair

```graphql
query Evidence($ensemblId: String!, $efoId: String!, $size: Int!) {
  disease(efoId: $efoId) {
    evidences(ensemblIds: [$ensemblId], size: $size) {
      count
      rows {
        id
        score
        datasourceId
        datatypeId
        literature
        diseaseFromSource
        targetFromSourceId
        resourceScore
        urls {
          niceName
          url
        }
      }
    }
  }
}
```

* *变量：**
```json
{
  "ensemblId": "ENSG00000141510",
  "efoId": "EFO_0000311",
  "size": 10
}
```

- --

### 6.药物/分子信息

```graphql
query DrugInfo($chemblId: String!) {
  drug(chemblId: $chemblId) {
    id
    name
    drugType
    maximumClinicalTrialPhase
    hasBeenWithdrawn
    mechanismsOfAction {
      rows {
        mechanismOfAction
        targets {
          id
          approvedSymbol
        }
      }
    }
    indications {
      rows {
        disease {
          id
          name
        }
        maxPhaseForIndication
      }
    }
    linkedDiseases {
      count
      rows {
        id
        name
      }
    }
    linkedTargets {
      count
      rows {
        id
        approvedSymbol
      }
    }
  }
}
```

* *变量：** `{ "chemblId": "CHEMBL25" }`（阿司匹林）

* *URL 示例：**
```
https://api.platform.opentargets.org/api/v4/graphql?query={drug(chemblId:"CHEMBL25"){id name drugType maximumClinicalTrialPhase mechanismsOfAction{rows{mechanismOfAction targets{id approvedSymbol}}}}}
```

- --

### 7. 跨目标、疾病和药物

```graphql
query Search($queryString: String!, $entityNames: [String!], $page: Pagination!) {
  search(queryString: $queryString, entityNames: $entityNames, page: $page) {
    total
    hits {
      id
      entity
      name
      description
      score
    }
  }
}
```

* *变量：**
```json
{
  "queryString": "BRAF melanoma",
  "entityNames": ["target", "disease", "drug"],
  "page": { "index": 0, "size": 10 }
}
```

* *URL示例：**
```
https://api.platform.opentargets.org/api/v4/graphql?query={search(queryString:"BRAF",entityNames:["target"],page:{index:0,size:5}){total hits{id entity name description}}}
```

- --

### 8. 已知药物对于目标

```graphql
query KnownDrugs($ensemblId: String!, $size: Int!) {
  target(ensemblId: $ensemblId) {
    approvedSymbol
    knownDrugs(size: $size) {
      count
      rows {
        drug {
          id
          name
          drugType
          maximumClinicalTrialPhase
        }
        disease {
          id
          name
        }
        phase
        status
        mechanismOfAction
        urls {
          niceName
          url
        }
      }
    }
  }
}
```

* *变量：**
```json
{
  "ensemblId": "ENSG00000157764",
  "size": 10
}
```

(ENSG00000157764 = BRAF)

- --

### 9. 可处理性（成药性）

包含在目标查询中（参见上面的端点1）。方式包括：
- `SM`（小分子）
- `AB`（抗体）
- `PR`（PROTAC）
- `OC`（其他）临床）

- --

## REST API端点

这些是常见操作的更简单的替代方案。

### 搜索

```
GET /api/v4/search?q={query}&page=0&size=10
```

* *示例：**
```
https://api.platform.opentargets.org/api/v4/search?q=TP53&size=5
```

* *响应：**
```json
{
  "total": 15,
  "data": [
    {
      "id": "ENSG00000141510",
      "entity": "target",
      "name": "TP53",
      "description": "Cellular tumor antigen p53",
      "score": 142.5
    }
  ]
}
```

- --

## 密钥标识符

|实体|身份证格式|示例 |
|---------|------------|---------|
|目标|整体基因 ID | `ENSG00000141510` (TP53) |
|疾病 | EFO/Mondo/HP/Orphanet | `EFO_0000311`（癌症），`MONDO_0007254` |
|药品 | ChEMBL ID | `CHEMBL25`（阿司匹林）|

## 数据源 ID（用于过滤证据）

- `ot_genetics_portal` -- 开放目标遗传学
- `eva` -- ClinVar（通过 EVA）
- `cancer_gene_census` -- COSMIC 癌症基因普查
- `chembl` -- ChEMBL（临床试验）
- `europepmc` -- 文献挖掘
- `expression_atlas` -- 表达图谱
- `gene2phenotype` -- Gene2Phenotype
- `genomics_england` -- Genomics England PanelApp
- `intogen` -- IntOGen（癌症驱动因素）
- `ot_crispr` -- 开放目标 CRISPR 筛选
- `progeny` -- PROGENy（通路活性）
- `reactome` -- 反应组途径
- `slapenrich` -- SLAPenrich
- `sysbio` -- 系统生物学
- `uniprot_literature` -- UniProt 文献

## 分页

GraphQL 使用`page: { index: Int, size: Int }`（从 0 开始的索引）。
REST 使用 `page` 和 `size` 查询参数。

## 速率限制

 - 不需要 API 密钥。
  - 适用公平使用速率限制。无硬发布限制。
- 对于批量数据，请使用开放目标数据下载（GCS/FTP 上的 Parquet 文件）而不是 API。
- 尊重 HTTP 429 和 `Retry-After` 标头。

## 错误格式

GraphQL错误：
```json
{
  "errors": [
    {
      "message": "Variable '$ensemblId' expected value of type 'String!' but got: null",
      "locations": [{"line": 1, "column": 7}]
    }
  ]
}
```

REST 错误返回带有 JSON 错误体的适当 HTTP 状态代码。

## Tips

- 使用 GraphQL API 实现最大灵活性 - 仅请求您需要的字段。
- GraphQL 的 GET 方法适用于简单查询，但对于带有变量的复杂查询则需要 POST。
- 组合目标 + 疾病查询以获得与证据细分的关联分数。
- 在关联查询中使用 `datasourceScores` 以查看哪些证据源贡献最大。
- 开放目标平台`https://platform.opentargets.org` 的 Web UI 有一个用于测试查询的 GraphQL 游乐场。
