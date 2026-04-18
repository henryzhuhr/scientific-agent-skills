# GWAS Catalog (EBI)

## Base URL
```
https://www.ebi.ac.uk/gwas/rest/api
```

## Auth
No API key required.

## 注意：响应使用带有 `_links` 和 `_embedded` 密钥的 HAL+JSON 格式。

## 密钥端点

|端点|描述 |
|----------|--------------|
| `/studies/{accession}` |单一研究（例如 GCST001633）|
| `/studies/search/findByPubmedId?pubmedId={id}` | PubMed ID 研究 |
| `/singleNucleotidePolymorphisms/{rsId}` | SNP详细信息|
| `/singleNucleotidePolymorphisms/{rsId}/associations` | SNP 关联 |
| `/singleNucleotidePolymorphisms/search/findByRsId?rsId={rsId}` |按 rsID 搜索 |
| `/associations` |列出协会 |
| `/associations/{id}` |单联|
| `/efoTraits` |列出 EFO 性状 |
| `/efoTraits/search/findByEfoTrait?trait={name}` |搜索特征 |

## 分页
`?page=0&size=20`（零索引，最大~500）

## 调用示例
```
# Get a study
https://www.ebi.ac.uk/gwas/rest/api/studies/GCST001633

# Associations for a SNP
https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/rs7329174/associations

# Search traits
https://www.ebi.ac.uk/gwas/rest/api/efoTraits/search/findByEfoTrait?trait=diabetes&page=0&size=5
```

## 响应格式
HAL+JSON。结果为 `_embedded.studies[]` 或 `_embedded.associations[]`。关键字段：`pvalue`、`riskFrequency`、`orPerCopyNum`、`betaNum`.

## 速率限制
没有公布的限制。通过 FTP 获取批量数据：ftp.ebi.ac.uk/pub/databases/gwas/
