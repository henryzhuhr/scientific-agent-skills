# DrugBank API

## 重要提示：DrugBank 的完整 API 是商业化的（需要付费许可证）

* *药物数据的免费替代品：**
- **ChEMBL** — 广泛的生物活性数据，免费 API
- **PubChem** — 免费化合物数据
- **OpenFDA** — 药物标签、不良事件
- **DGIdb** (https://dgidb.org/api) — 药物-基因相互作用，免费

## 基本 URL（付费 API）
```
https://api.drugbank.com/v1
```

## 需要 Auth
API 密钥：`Authorization: Bearer <api_key>`

## 关键端点（付费 API）

|端点|描述 |
|----------|-------------|
| `/drugs/{drugbank_id}` |通过 DrugBank ID |
| 获取药物`/drugs?q={query}` |搜索药品|
| `/drugs/{id}/interactions` |药物间相互作用|
| `/drugs/{id}/targets` |药物靶点|
| `/drugs/{id}/enzymes` |代谢酶|
| `/drugs/{id}/pathways` |相关途径|
| `/drugs/{id}/adverse_effects` |不良反应|
| `/drug_interactions?drugbank_id={id1},{id2}` |检查具体相互作用 |

## 调用示例
```
GET /drugs/DB00945  (aspirin)
GET /drugs?q=aspirin
GET /drugs/DB00945/interactions
GET /drugs/DB00945/targets
```

## 响应格式
```json
{
  "drugbank_id": "DB00945",
  "name": "Acetylsalicylic acid",
  "cas_number": "50-78-2",
  "groups": ["approved"],
  "targets": [{"name": "Prostaglandin G/H synthase 1", "uniprot_id": "P23219", "gene_name": "PTGS1", "actions": ["inhibitor"]}],
  "external_ids": {"chembl": "CHEMBL25", "pubchem_compound": "2244"}
}
```

## 免费访问选项
- **DrugBank 开放数据**：约 2,500 种 FDA 批准的药物以 XML/CSV 形式下载https://go.drugbank.com/releases/latest
- **学术许可证**：免费用于非商业用途，提供数据下载（非API）
