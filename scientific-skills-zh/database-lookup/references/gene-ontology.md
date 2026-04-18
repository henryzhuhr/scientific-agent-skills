# 基因本体 (GO) API 参考

## 基本 URL
- **QuickGO（EBI，推荐）**：`https://www.ebi.ac.uk/QuickGO/services` — 最可靠的端点
- **GO API**：`https://api.geneontology.org/api` — 可能返回 403；使用 QuickGO 作为后备
- **AmiGO / GOlr（基于 Solr）**：`http://golr-aux.geneontology.org/solr`

## 身份验证
无需。所有端点都是公共的。

## 速率限制
没有发布的硬限制。 QuickGO 建议合理使用。

- --

## GO API (api.geneontology.org)

### 1. GO 术语查找
```
GET https://api.geneontology.org/api/ontology/term/{go_id}
```
示例：
```
GET https://api.geneontology.org/api/ontology/term/GO%3A0008150
```
返回包含术语名称、定义、命名空间（biological_process / 

### 2. 基因/蛋白质注释（生物实体）
```
GET https://api.geneontology.org/api/bioentity/gene/{gene_id}/function
```
示例 — UniProt 蛋白质的 GO 注释：
```
GET https://api.geneontology.org/api/bioentity/gene/UniProtKB%3AP04637/function
```
 返回带有证据代码、限定符的 GO 注释，参考文献。

### 3. GO 术语注释的基因
```
GET https://api.geneontology.org/api/bioentity/function/{go_id}/genes
```
示例：
```
GET https://api.geneontology.org/api/bioentity/function/GO%3A0006915/genes?rows=20
```
返回用该 GO 术语注释的基因/蛋白质。

### 4. 搜索实体
```
GET https://api.geneontology.org/api/search/entity/{query}
```
示例：
```
GET https://api.geneontology.org/api/search/entity/apoptosis?rows=10
```

### 5.本体祖先/后代
```
GET https://api.geneontology.org/api/ontology/term/{go_id}/graph
```

- --

## QuickGO API（EBI - 推荐用于强大的注释查询）

### 1. GO 术语详细信息
```
GET https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{go_ids}
```
示例：
```
GET https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/GO:0008150
```
接受逗号分隔的 ID（最多 25 个）。

### 2. 搜索注释
```
GET https://www.ebi.ac.uk/QuickGO/services/annotation/search?geneProductId={uniprot_id}
```
示例 — TP53 的注释：
```
GET https://www.ebi.ac.uk/QuickGO/services/annotation/search?geneProductId=P04637&limit=25
```

### 3. GO Term 的注释
```
GET https://www.ebi.ac.uk/QuickGO/services/annotation/search?goId=GO:0006915&taxonId=9606&limit=25
```

### 4. 过滤注释证据
```
GET https://www.ebi.ac.uk/QuickGO/services/annotation/search?geneProductId=P04637&goUsage=descendants&evidenceCode=ECO:0000269&limit=25
```

### 5. GO Term 子项
```
GET https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/GO:0008150/children
```

### 6. GO Term 祖先（图表）
```
GET https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/GO:0006915/ancestors?relations=is_a,part_of
```

### 7. 搜索 GO Term按名称
```
GET https://www.ebi.ac.uk/QuickGO/services/ontology/go/search?query=apoptosis&limit=10
```

## QuickGO注释搜索参数
|参数|描述|
|---------|--------------|
| `geneProductId` | UniProt 登记号（例如 P04637）|
| `goId` | GO 术语（例如 GO:0006915）|
| `goUsage` | `exact` 或 `descendants`（包括子术语）|
| `taxonId` | NCBI 分类 ID（9606 = 人类）|
| `evidenceCode` | ECO 代码（例如 ECO:0000269 = 实验性）|
| `aspect` | `biological_process`、`molecular_function`、`cellular_component` |
| `limit` |每页结果（最多 100 条）|
| `page` |页码（从 1 开始）|

## QuickGO 响应格式
```json
{
  "numberOfHits": 1234,
  "results": [
    {
      "geneProductId": "P04637",
      "symbol": "TP53",
      "goId": "GO:0006915",
      "goName": "apoptotic process",
      "evidenceCode": "ECO:0000269",
      "goAspect": "biological_process",
      "taxonId": 9606,
      "reference": "PMID:12345678",
      "assignedBy": "UniProt"
    }
  ]
}
```

## 注释
- QuickGO (EBI)通常对于注释查询来说更稳健且有更好的文档记录。
- GO API (geneontology.org)更适合本体结构traversal.
- GO ID 在路径中使用时必须进行 URL 编码（例如，`GO%3A0008150` 表示 `GO:0008150`）。
- 三个 GO 命名空间：biological_process (BP)、molecules_function (MF)、cellular_component (CC)。
- 证据代码：IDA（直接测定）、 IMP（突变表型）、IGI（遗传相互作用）、IEA（电子注释）等
