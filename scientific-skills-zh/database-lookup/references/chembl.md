# ChEMBL REST API

## 基本 URL
```
https://www.ebi.ac.uk/chembl/api/data
```

## Auth
无需 API 密钥。完全开放、免费。

## 关键端点

|端点|描述 |
|----------|-------------|
| `/molecule/{chembl_id}` |通过 ChEMBL ID |
| 获取分子`/molecule/search?q={query}` |自由文本分子搜索|
| `/target/{chembl_id}` |通过 ChEMBL ID |
| 获取目标`/target/search?q={query}` |自由文本目标搜索|
| `/activity?molecule_chembl_id={id}` |分子的活性 |
| `/activity?target_chembl_id={id}` |目标活动|
| `/mechanism?molecule_chembl_id={id}` |作用机制|
| `/drug_indication?molecule_chembl_id={id}` |药品适应症|
| `/similarity/{smiles}/{threshold}` |相似性搜索（阈值40-100）|
| `/substructure/{smiles}` |子结构搜索 |

## 常用参数

- `format=json` — 响应格式（默认 json）
- `limit` — 每页结果（默认 20，最大 1000）
- `offset` — 分页偏移量
- `order_by` — 排序字段（前缀 `-` 表示降序）
- `only` — 仅返回指定字段（以逗号分隔）

### 过滤运算符（附加到字段名称）
`__exact`、`__icontains`、 `__gt`、`__gte`、`__lt`、`__lte`、`__in`、`__isnull`、`__startswith`、`__range`、`__regex`

## 示例调用

```
# Get molecule by ID
/molecule/CHEMBL25.json

# Search molecules by name
/molecule/search?q=aspirin&format=json

# Activities for a target with potency filter
/activity?target_chembl_id=CHEMBL240&pchembl_value__gte=6&format=json&limit=100

# Similarity search (80% threshold)
/similarity/CC(%3DO)Oc1ccccc1C(%3DO)O/80.json

# Approved drugs only
/molecule?max_phase=4&format=json

# Mechanism of action
/mechanism?molecule_chembl_id=CHEMBL25&format=json
```

## 响应格式（分子）
```json
{
  "page_meta": {"limit": 20, "offset": 0, "total_count": 150},
  "molecules": [{
    "molecule_chembl_id": "CHEMBL25",
    "pref_name": "ASPIRIN",
    "max_phase": 4,
    "molecule_properties": {
      "full_mwt": 180.16, "full_molformula": "C9H8O4",
      "alogp": 1.31, "hba": 3, "hbd": 1, "psa": 63.60
    },
    "molecule_structures": {
      "canonical_smiles": "CC(=O)Oc1ccccc1C(=O)O",
      "standard_inchi_key": "BSYNRYMUTXBXSQ-UHFFFAOYSA-N"
    }
  }]
}
```

## 速率限制
没有严格限制。保持在约 10 请求/秒以下。无需授权。
