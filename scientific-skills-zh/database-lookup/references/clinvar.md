# ClinVar API 参考

## 基本 URL
- **NCBI 电子实用程序**：`https://eutils.ncbi.nlm.nih.gov/entrez/eutils`
- **ClinVar Web API (VCV)**：`https://www.ncbi.nlm.nih.gov/clinvar`
- **NCBI 变异服务**：`https://api.ncbi.nlm.nih.gov/variation/v0`

## 身份验证
- 电子实用程序：不需要密钥，但**强烈推荐**。在 https://www.ncbi.nlm.nih.gov/account/ 注册以获得 `api_key`.
  - 没有密钥：3 个请求/秒。使用密钥：10 个请求/秒。
- 将 `&api_key=YOUR_KEY` 附加到所有电子公用事业请求。

## 速率限制
- 不使用 API 密钥：3 个请求/秒
- 使用 API 密钥：10 个请求/秒

## 关键端点

### 1. 搜索 ClinVar (esearch)
```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term={query}&retmode=json
```
 示例 — 搜索 BRCA1 致病变异：
```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=BRCA1[gene]+AND+pathogenic[clinical_significance]&retmode=json&retmax=10
```
 返回 JSON，其中包含 ClinVar 变异 ID 的 `idlist`。

### 2. 获取 ClinVar 记录（摘要）
```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id={id_list}&retmode=json
```
示例：
```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=37088,37087&retmode=json
```
返回包含临床意义、变异名称、基因、条件、审核状态的 JSON。

### 3. 全记录（efetch）
```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=clinvar&id={id}&rettype=vcv&is_variationid&retmode=xml
```
注：ClinVar efetch 返回 **仅 XML**（无 JSON）用于 efetch）。

### 4. 变异服务 API — SPDI/HGVS 查找
```
GET https://api.ncbi.nlm.nih.gov/variation/v0/spdi/{spdi_expression}/clinvar
GET https://api.ncbi.nlm.nih.gov/variation/v0/hgvs/{hgvs_expression}/clinvar
```
示例：
```
GET https://api.ncbi.nlm.nih.gov/variation/v0/hgvs/NM_007294.4%3Ac.5266dupC/clinvar
```

### 5. ClinVar VCV/RCV 直接访问
```
GET https://www.ncbi.nlm.nih.gov/clinvar/variation/{variation_id}/?redir=vcv
```
此返回HTML。对于编程访问，请使用电子实用程序或变异服务 API。

## 有用的搜索限定符
- `[gene]` — 基因符号（例如，`BRCA1[gene]`）
- `[clinical_significance]` — 致病性、可能致病性、良性、 certain_significance
- `[molecular_consequence]` — 错义、无义、移码等。 
- `[review_status]` — 标准提供的单一提交者、专家小组审核等。 
- `[condition]` — 疾病名称

## 响应格式
- esearch/esummary：JSON（使用 `retmode=json`）
- efetch：仅用于 ClinVar
 的 XML- 变异服务：JSON

## 摘要响应关键字段
```json
{
  "result": {
    "37088": {
      "uid": "37088",
      "title": "NM_007294.4(BRCA1):c.5266dupC (p.Gln1756Profs*74)",
      "clinical_significance": { "description": "Pathogenic" },
      "genes": [{"symbol": "BRCA1", "geneid": 672}],
      "variation_set": [...],
      "trait_set": [{"trait_name": "Hereditary breast and ovarian cancer syndrome"}]
    }
  }
}
```

## 注释
- 结合 esearch + esummary 进行搜索然后获取工作流程。
- 对于批量下载，请使用 ClinVar FTP：https://ftp.ncbi.nlm.nih.gov/pub/clinvar/
