# gnomAD（基因组聚合数据库）API 参考

## 概述
gnomAD 聚合外显子组和基因组测序数据，以提供不同人群的等位基因频率
 和变异注释。

## API 类型：GraphQL
- **端点**：`https://gnomad.broadinstitute.org/api`
- **方法**：POST JSON 正文包含 GraphQL 查询
- **Auth**：不需要（公共，未经身份验证）
- **响应格式**：JSON（具有 GraphQL 结构的 `data` 包装器）

## 键查询

### 按变体 ID 进行变体查找
变体 ID 使用格式： `{chrom}-{pos}-{ref}-{alt}`（GRCh37 或 GRCh38）.

```
POST https://gnomad.broadinstitute.org/api
Content-Type: application/json

{
  "query": "{ variant(variantId: \"1-55516888-G-A\", dataset: gnomad_r4) { variant_id rsids chrom pos ref alt exome { ac an af } genome { ac an af } } }"
}
```

### 基因查找
```json
{
  "query": "{ gene(gene_symbol: \"BRCA1\", reference_genome: GRCh38) { gene_id symbol chrom start stop strand } }"
}
```

### 基因中的变异
```json
{
  "query": "{ gene(gene_symbol: \"PCSK9\", reference_genome: GRCh38) { variants(dataset: gnomad_r4) { variant_id consequence rsids exome { ac an af } genome { ac an af } } } }"
}
```

### 区域中的变体
```json
{
  "query": "{ region(chrom: \"1\", start: 55505222, stop: 55530526, reference_genome: GRCh38) { variants(dataset: gnomad_r4) { variant_id rsids consequence exome { ac af } genome { ac af } } } }"
}
```

### 转录本查找
```json
{
  "query": "{ transcript(transcript_id: \"ENST00000357654\", reference_genome: GRCh38) { transcript_id gene_id chrom start stop strand } }"
}
```

## 数据集值
- `gnomad_r4` -- gnomAD v4（GRCh38，最新主要版本）
- `gnomad_r3` -- gnomAD v3.1.2（GRCh38，仅限基因组）
- `gnomad_r2_1` -- gnomAD v2.1.1（GRCh37，外显子组 + 基因组）

## 群体频率字段
`exome` 或 `genome` 对象内，特定人群的频率可通过 
`populations { id ac an af }` 获得，其中 `id` 值包括：`afr`、`amr`、`asj`、`eas`、
`fin`、`mid`、 `nfe`、`oth`、`sas`.

## 响应示例（变体）
```json
{
  "data": {
    "variant": {
      "variant_id": "1-55516888-G-A",
      "rsids": ["rs11591147"],
      "chrom": "1",
      "pos": 55516888,
      "ref": "G",
      "alt": "A",
      "exome": { "ac": 1234, "an": 250000, "af": 0.004936 },
      "genome": { "ac": 456, "an": 150000, "af": 0.00304 }
    }
  }
}
```

## 速率限制
- 没有发布速率限制，但激进的查询将受到限制
- 使用合理的请求节奏（建议约 1 请求/秒）
  - 对于批量下载，请使用 Google Cloud 上的 gnomAD 的 Hail 表或下载 VCFs

## Notes
- GraphQL 模式没有单独进行版本控制；它跟踪 gnomad Web 界面
- 使用 gnomad.broadinstitute.org 上的浏览器网络检查器来发现 
 其他查询字段和结构
- 结构变体 (SV)具有单独的查询结构 (`structural_variant`)
- 约束指标（pLI、LOEUF）可通过以下方式在基因查询上使用`gnomad_constraint`
