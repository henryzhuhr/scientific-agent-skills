# ChEBI（具有生物意义的化学实体）API 参考

## 基本 URL
- **OLS（本体查找服务）API**：`https://www.ebi.ac.uk/ols4/api`
- **ChEBI Web 服务 (SOAP)**：`https://www.ebi.ac.uk/webservices/chebi/2.0/test`（仅限 SOAP/XML）
- **ChEBI LibChebi REST （有限）**：`https://www.ebi.ac.uk/chebi`

## 的实体页面身份验证
无需。所有端点都是公共的。

## 速率限制
没有发布的硬限制。 EBI 一般指南：合理使用。

## 重要提示
ChEBI 的主要 Web 服务是 **基于 SOAP** (XML)，而不是 REST。对于 REST 风格的 JSON 访问，请使用 **EBI OLS4 API**，它将 ChEBI 作为本体进行索引。

- --

## OLS4 API 端点（推荐用于 REST/JSON）

### 1. 搜索 ChEBI术语
```
GET https://www.ebi.ac.uk/ols4/api/search?q={query}&ontology=chebi
```
示例：
```
GET https://www.ebi.ac.uk/ols4/api/search?q=aspirin&ontology=chebi
```
返回包含匹配ChEBI术语、ID、定义、同义词的JSON。

### 2. 按ChEBI查找ID
```
GET https://www.ebi.ac.uk/ols4/api/ontologies/chebi/terms?iri=http://purl.obolibrary.org/obo/CHEBI_{id}
```
示例：
```
GET https://www.ebi.ac.uk/ols4/api/ontologies/chebi/terms?iri=http://purl.obolibrary.org/obo/CHEBI_15365
```
返回完整术语详细信息：名称、定义、同义词、外部参照、关系。

### 3. 通过简写形式获取术语
```
GET https://www.ebi.ac.uk/ols4/api/ontologies/chebi/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FCHEBI_{id}
```
（双编码 IRI路径。)

### 4. 术语层次结构 — 父级
```
GET https://www.ebi.ac.uk/ols4/api/ontologies/chebi/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FCHEBI_{id}/parents
```

### 5. 术语层次结构 — 子级
```
GET https://www.ebi.ac.uk/ols4/api/ontologies/chebi/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FCHEBI_{id}/children
```

### 6. 本体元数据
```
GET https://www.ebi.ac.uk/ols4/api/ontologies/chebi
```

## OLS 搜索响应格式
```json
{
  "response": {
    "numFound": 5,
    "docs": [
      {
        "id": "chebi:15365",
        "iri": "http://purl.obolibrary.org/obo/CHEBI_15365",
        "label": "aspirin",
        "description": ["A member of the class of benzoic acids..."],
        "short_form": "CHEBI_15365",
        "obo_id": "CHEBI:15365",
        "ontology_name": "chebi",
        "type": "class"
      }
    ]
  }
}
```

## ChEBI SOAP Web 服务（替代）
如果您需要化学特定数据（分子式、质量、结构、InChI），请使用 SOAP服务：
- WSDL：`https://www.ebi.ac.uk/webservices/chebi/2.0/webservice?wsdl`
- 操作：`getCompleteEntity`、`getLiteEntity`、`getStructureSearch`、`getOntologyChildren`、`getOntologyParents`
- 仅返回 XML。

 的 SOAP 请求示例`getCompleteEntity`:
```xml
<soapenv:Body>
  <chebi:getCompleteEntity>
    <chebi:chebiId>CHEBI:15365</chebi:chebiId>
  </chebi:getCompleteEntity>
</soapenv:Body>
```
返回：公式、质量、电荷、InChI、InChIKey、SMILES、同义词、数据库链接、本体父/子。

## 注释
- 对于编程 REST 访问，OLS4 是最简单的路径。
- 对于化学结构搜索（通过 InChI、SMILES、子结构），需要 SOAP 服务。
- ChEBI ID 是数字（例如 15365），但在 OBO 中引用为“CHEBI:15365”格式。
- PubChem 和 UniChem 可以将 ChEBI ID 交叉引用到其他化学数据库。
