# DisGeNET（基因疾病关联）

## 基本 URL
```
https://www.disgenet.org/api
```

## Auth
* * 需要 API 密钥。** 在 disgenet.org 注册，然后进行身份验证：
```bash
curl -X POST https://www.disgenet.org/api/auth/ \
  -d 'email=you@example.com&password=yourpassword'
# Returns: {"token": "abc123..."}
```
传递为：`Authorization: Bearer <token>`

从以下位置加载令牌`.env` 为 `DISGENET_API_KEY`.

## 关键端点

|端点|描述 |
|----------|--------------|
| `/gda/gene/{gene_id}` |基因-疾病关联（NCBI 基因 ID）|
| `/gda/disease/{disease_id}` |基因疾病关联 (UMLS CUI) |
| `/gda/evidences/gene/{gene_id}` |证据级数据|
| `/vda/gene/{gene_id}` |基因变异与疾病的关联 |
| `/vda/variant/{rsid}` |变异疾病关联 (dbSNP rsID) |

## 参数
- `source` — `CURATED`、`BEFREE`、`ALL`
- `min_score` — GDA 分数阈值(0-1)
- `min_ei` — 证据索引阈值
- `format` — `json` 或 `tsv`
- `limit`、`offset` — 分页

## 示例呼叫
```
# Gene-disease for TP53 (gene ID 7157)
/gda/gene/7157?source=CURATED&min_score=0.3&limit=10&format=json

# Disease-gene for Breast Cancer (UMLS CUI C0006142)
/gda/disease/C0006142?limit=10

# Variant-disease for rs1042522
/vda/variant/rs1042522
```

## 速率限制
免费学术层：〜每天几百个请求。提供付费等级。

## 免费替代方案
如果没有 API 密钥：使用 **开放目标** 进行疾病基因关联。
