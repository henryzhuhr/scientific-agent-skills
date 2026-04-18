# HPO（人类表型本体）

## 基本 URL
```
https://ontology.jax.org/api/hp
```

## Auth
无需 API 密钥。

## 重要提示：HP ID 中的 URL 编码冒号 — `HP:0001250` 变为 `HP%3A0001250`

## 密钥端点

|端点|描述 |
|----------|--------------|
| `/hpo/search?q={query}&max={n}` |按名称搜索 HPO 术语 |
| `/hpo/term/{id}` |条款详情|
| `/hpo/term/{id}/genes` |与表型相关的基因|
| `/hpo/term/{id}/diseases` |与表型相关的疾病|
| `/hpo/term/{id}/children` |层次结构中的子项 |
| `/hpo/term/{id}/parents` |父条款|
| `/hpo/gene/{gene_id}` |基因表型 (Entrez ID) |
| `/hpo/disease/{disease_id}` |疾病表型 (OMIM/ORPHA) |

## 调用示例
```
# Search for "seizure"
https://ontology.jax.org/api/hp/hpo/search?q=seizure&max=5

# Term details for Seizure
https://ontology.jax.org/api/hp/hpo/term/HP%3A0001250

# Genes associated with Seizure
https://ontology.jax.org/api/hp/hpo/term/HP%3A0001250/genes

# Diseases for Seizure
https://ontology.jax.org/api/hp/hpo/term/HP%3A0001250/diseases

# Phenotypes for SCN1A (Entrez 6323)
https://ontology.jax.org/api/hp/hpo/gene/6323
```

## 响应格式
JSON。条款：`id`、`name`、`definition`、`synonyms`。基因关联：`genes[]` 与 `geneId`、`geneSymbol`。疾病：`diseases[]` 与 `diseaseId`、`diseaseName`.

## 速率限制
没有公布的限制。批量注释文件位于 https://hpo.jax.org/data/annotations
