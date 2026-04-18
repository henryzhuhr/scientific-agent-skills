# dbSNP API 参考

## 概述
SNP 和变体数据。可通过两个 API 访问：用于搜索/元数据的 NCBI 电子实用程序 (`db=snp`)，以及用于详细变体注释的 NCBI 变体服务 REST API。

## 基本 URL
```
E-utilities:  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
Variation API: https://api.ncbi.nlm.nih.gov/variation/v0/
```

## 身份验证
- **电子实用程序**：推荐 API 密钥（`&api_key=KEY`）。不使用密钥时为 3 请求/秒，使用密钥时为 10 请求/秒。
- **变体 API**：无需身份验证。适用速率限制（未记录；请尊重，约 1-2 请求/秒）。

- --

## 电子公用事业端点 (db=snp)

### 1. ESearch — 搜索 SNP
```
GET esearch.fcgi?db=snp&term=QUERY&retmax=N&retmode=json
```

* *示例 — 搜索 BRCA1 中的 SNP基因：**
```
GET esearch.fcgi?db=snp&term=BRCA1[Gene Name] AND homo sapiens[Organism]&retmax=5&retmode=json
```
响应：
```json
{
  "esearchresult": {
    "count": "12847",
    "idlist": ["80357713", "80357508", ...]
  }
}
```
注意：返回的 ID 是不带“rs”前缀的 rs 编号。

### 2. ESummary -- SNP 摘要
```
GET esummary.fcgi?db=snp&id=IDS&retmode=json
```

* *示例 -- 获取摘要rs334（镰状细胞变体）：**
```
GET esummary.fcgi?db=snp&id=334&retmode=json
```
响应包括：`snp_id`、`chr`、`chrpos`、`genes`、`clinical_significance`、`global_mafs`、`docsum`.

### 3. EFetch -- 获取 SNP 详细信息（仅限 XML）
```
GET efetch.fcgi?db=snp&id=IDS&rettype=json&retmode=text
```
注意：dbSNP 的 EFetch 返回带有 `rettype=json` 的 JSON。还支持带有 `retmode=xml`.

- --

## 变体服务 API

### 的 XML 1. 通过 rsID
```
GET /variation/v0/refsnp/{rsid}
```

* *示例：**
```
GET https://api.ncbi.nlm.nih.gov/variation/v0/refsnp/334
```
Response (JSON,缩写):
```json
{
  "refsnp_id": "334",
  "create_date": "2000/09/19",
  "primary_snapshot_data": {
    "placements_with_allele": [...],
    "allele_annotations": [...],
    "support": [...]
  },
  "present_obs_movements": [
    {
      "component_ids": [{"type": "clinvar", "value": "..."}],
      "observation": {
        "seq_id": "NC_000011.10",
        "position": 5227002,
        "deleted_sequence": "T",
        "inserted_sequence": "A"
      }
    }
  ]
}
```

### 2. 通过 SPDI 表示法查找变体
```
GET /variation/v0/spdi/{spdi}/rsids
```
SPDI 格式： `SeqID:Position:Deletion:Insertion`

* *示例：**
```
GET https://api.ncbi.nlm.nih.gov/variation/v0/spdi/NC_000011.10:5227002:T:A/rsids
```

### 3. 查找变体HGVS
```
GET /variation/v0/hgvs/{hgvs}/contextuals
```

* *示例：**
```
GET https://api.ncbi.nlm.nih.gov/variation/v0/hgvs/NC_000011.10:g.5227003T>A/contextuals
```

### 4. 批量 rsID 查找（POST）
```
POST /variation/v0/refsnp/batch
Content-Type: application/json

{"refsnp_ids": ["334", "1805007", "7412"]}
```

## 常用电子公用事业搜索模式
```
# By rs number
term=334[RS ID]

# Clinical significance
term=pathogenic[Clinical Significance] AND BRCA1[Gene Name]

# By chromosome position (GRCh38)
term=11[Chromosome] AND 5227002:5227002[Base Position]

# By variant type
term=missense[Function Class] AND TP53[Gene Name]

# By global minor allele frequency
term=0.01:0.05[Global MAF]
```

## 速率限制
- 电子实用程序：3请求/秒（无密钥），10请求/秒（有密钥）
- 变化服务API：无发布限制；建议 1-2 请求/秒
