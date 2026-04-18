# Monarch Initiative API

## 基本 URL
```
https://api.monarchinitiative.org/v3/api
```

## Auth
无需 API 密钥。

## 关键端点

|端点|描述 |
|----------|-------------|
| `/search?q={query}` |跨所有实体的文本搜索 |
| `/autocomplete?q={prefix}` |自动完成实体名称 |
| `/entity/{id}` |实体详细信息（基因、疾病、表型）|
| `/entity/{id}/associations` |实体的关联 |
| `/entity/{id}/associations?category={cat}` |过滤关联 |

## 实体 ID 前缀
- `MONDO:` — 疾病（例如 `MONDO:0007947`）
- `HP:` — 表型（例如 `HP:0001250`）
- `HGNC:` —基因（例如 `HGNC:3603`）
- `NCBIGene:` — 基因（例如 `NCBIGene:7157`）

## 关联类别
`biolink:GeneToPhenotypicFeatureAssociation`、`biolink:DiseaseToPhenotypicFeatureAssociation`、`biolink:GeneToDiseaseAssociation`

## 调用示例
```
# Search for Marfan syndrome
https://api.monarchinitiative.org/v3/api/search?q=Marfan+syndrome&limit=5

# Entity details for a disease
https://api.monarchinitiative.org/v3/api/entity/MONDO:0007947

# Gene-to-phenotype for FBN1
https://api.monarchinitiative.org/v3/api/entity/HGNC:3603/associations?category=biolink:GeneToPhenotypicFeatureAssociation&limit=10
```

## 响应格式
JSON。搜索：`items[]` 与 `id`、`name`、`category`。关联：`items[]` 与 `subject`、`predicate`、`object`、`publications`.

## 速率限制
没有发布的限制。讲道理吧。
