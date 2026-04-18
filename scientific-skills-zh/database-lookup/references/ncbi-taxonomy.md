# NCBI 分类 API 参考

## 概述
NCBI 数据库中所有生物的分类数据（名称、谱系、等级）。可通过电子实用程序使用 `db=taxonomy`.

## 基本 URL
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

## 身份验证
- **API 密钥**（推荐）：附加 `&api_key=YOUR_KEY`（在 ncbi.nlm.nih.gov/account 注册）。
- 不带键：3 请求/秒。包含密钥：10 个请求/秒。
- 提供 `tool` 和 `email` 参数。

## 关键端点

### 1. ESearch -- 按名称搜索分类
```
GET esearch.fcgi?db=taxonomy&term=QUERY&retmode=json
```
|参数 |描述 |
|--------|--------------|
| `term` |生物名称、俗名或出租车。字段：`[Scientific Name]`、`[Common Name]`、`[All Names]`、`[Rank]` |
| `retmax` |返回的最大 ID（默认 20）|

* *示例 -- 按学名搜索：**
```
GET esearch.fcgi?db=taxonomy&term=Homo+sapiens[Scientific Name]&retmode=json
```
响应:
```json
{
  "esearchresult": {
    "count": "1",
    "idlist": ["9606"]
  }
}
```

* *示例 -- 按常见搜索name:**
```
GET esearch.fcgi?db=taxonomy&term=dog[Common Name]&retmode=json
```

### 2. EFetch -- 检索完整的分类记录
```
GET efetch.fcgi?db=taxonomy&id=TAXIDS&retmode=xml
```
注意：分类EFetch 仅支持 XML 输出。

* *示例 -- 获取人类分类（taxid 9606):**
```
GET efetch.fcgi?db=taxonomy&id=9606&retmode=xml
```
响应（缩写 XML）:
```xml
<TaxaSet>
  <Taxon>
    <TaxId>9606</TaxId>
    <ScientificName>Homo sapiens</ScientificName>
    <OtherNames>
      <CommonName>human</CommonName>
    </OtherNames>
    <Rank>species</Rank>
    <Division>Primates</Division>
    <GeneticCode><GCId>1</GCId><GCName>Standard</GCName></GeneticCode>
    <MitoGeneticCode><MGCId>2</MGCId><MGCName>Vertebrate Mitochondrial</MGCName></MitoGeneticCode>
    <Lineage>cellular organisms; Eukaryota; Opisthokonta; Metazoa; ... ; Hominidae; Homo</Lineage>
    <LineageEx>
      <Taxon><TaxId>131567</TaxId><ScientificName>cellular organisms</ScientificName><Rank>no rank</Rank></Taxon>
      <Taxon><TaxId>2759</TaxId><ScientificName>Eukaryota</ScientificName><Rank>superkingdom</Rank></Taxon>
      <!-- ... each ancestor node ... -->
    </LineageEx>
  </Taxon>
</TaxaSet>
```

### 3. ESummary -- 简要分类摘要
```
GET esummary.fcgi?db=taxonomy&id=TAXIDS&retmode=json
```
**示例 -- 多个类群：**
```
GET esummary.fcgi?db=taxonomy&id=9606,10090,7227&retmode=json
```
响应包括：`ScientificName`、`CommonName`、`Rank`、`Division`、`TaxId`、`Genus`、`Species`.

### 4. ELink -- 交叉链接分类到其他数据库
```
GET elink.fcgi?dbfrom=taxonomy&db=protein&id=9606&term=insulin
```
查找给定出租车的所有蛋白质记录，可以选择按关键字过滤。

## 常见搜索模式
```
# All species under a genus
term=Drosophila[Next Level] AND species[Rank]

# Search by taxid directly
term=txid9606[Organism:exp]

# By rank
term=Mammalia[Scientific Name] AND class[Rank]

# Subtree search (all descendants)
term=txid9606[Organism:exp]
```

## 有用的交叉引用
|链接 |描述 |
|------|--------------|
| `taxonomy_protein` |分类单元的所有蛋白质 |
| `taxonomy_gene` |分类单元的所有基因 |
| `taxonomy_nuccore` |分类单元的所有核苷酸记录|
| `taxonomy_genome` |分类单元的基因组组装 |

## 速率限制
- 不带 API 密钥：3 个请求/秒
- 使用 API 密钥：10 个请求/秒
- EFetch 在一次调用中支持多个出租车（以逗号分隔）
