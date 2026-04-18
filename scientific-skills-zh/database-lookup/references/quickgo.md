# QuickGO（EBI GO 注释浏览器）

## 基本 URL
```
https://www.ebi.ac.uk/QuickGO/services/
```

## 身份验证
无需身份验证。

## 关键端点

|端点|描述 |
|----------|-------------|
| `/ontology/go/terms/{goId}` | GO术语详情|
| `/ontology/go/terms/{goId}/children` |儿童条款|
| `/ontology/go/terms/{goId}/ancestors` |祖先术语|
| `/ontology/go/search?query={term}` |按关键字搜索GO术语|
| `/annotation/search` |按基因/分类单元/GO 术语搜索注释 |

## 注释搜索参数
- `goId` — GO 术语（例如 GO:0003723）
- `taxonId` — NCBI 分类（例如人类 9606）
- `geneProductId` — UniProt 登录 
- `evidence` — 证据代码（例如 ECO:0000269）
- `aspect` — 生物过程、分子功能、细胞成分
- `limit`、`page` — pagination

## 调用示例
```
# GO term details
https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/GO:0003723

# Human annotations for RNA binding
https://www.ebi.ac.uk/QuickGO/services/annotation/search?goId=GO:0003723&taxonId=9606&limit=10

# Search terms by keyword
https://www.ebi.ac.uk/QuickGO/services/ontology/go/search?query=apoptosis&limit=5
```

## 响应格式
JSON。注释：带有基因产物、GO 术语、证据、限定符的分页结果。

## 速率限制
EBI 合理使用政策。对大型结果集使用下载端点。
