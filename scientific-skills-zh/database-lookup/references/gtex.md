# GTEx（基因型-组织表达）API 参考

## 概述
GTEx 对死后捐赠者的人体组织中的基因表达水平进行分类，
enabling 研究组织特异性基因调控和 eQTL。

## 基本 URL
`https://gtexportal.org/api/v2`

## Auth
不需要（公共，未经身份验证）。

## 响应格式
JSON。大多数端点返回分页结果，其结构为：
```json
{
  "data": [ ... ],
  "paging_info": {
    "numberOfPages": 10,
    "page": 0,
    "maxItemsPerPage": 250
  }
}
```

## 分页参数（大多数端点通用）
- `page` -- 0索引页码（默认值：0）
- `itemsPerPage` -- 每页结果（默认值：250，最大： 250)

## 关键端点

### 基因表达（组织中位数）
```
GET /expression/medianGeneExpression?gencodeId=ENSG00000139618.17&datasetId=gtex_v8
```
 参数：
- `gencodeId` -- 版本化 Ensembl 基因 ID（必需）
- `datasetId` -- `gtex_v8`（必需）
- `tissueSiteDetailId` -- 过滤到特定组织（可选）

 返回该基因每个组织的 TPM 中位数。

### 基因表达（全部，针对组织）
```
GET /expression/medianGeneExpression?tissueSiteDetailId=Liver&datasetId=gtex_v8
```

### 单组织eQTLs
```
GET /association/singleTissueEqtl?gencodeId=ENSG00000139618.17&tissueSiteDetailId=Whole_Blood&datasetId=gtex_v8
```
参数：
- `gencodeId` -- 版本化 Ensembl 基因 ID（必填）
- `tissueSiteDetailId` -- 组织 ID（必填）
- `datasetId` -- `gtex_v8` （必填）

### 多组织eQTLs
```
GET /association/multiTissueEqtl?gencodeId=ENSG00000139618.17&datasetId=gtex_v8
```

### 基因搜索
```
GET /reference/gene?geneId=BRCA2&gencodeVersion=v26&genomeBuild=GRCh38/hg38
```
参数：
- `geneId` --基因符号或Ensembl ID
- `gencodeVersion` -- `v26` for GTEx v8
- `genomeBuild` -- `GRCh38/hg38`

### 列出组织
```
GET /dataset/tissueSiteDetail?datasetId=gtex_v8
```
 返回所有组织部位详细信息 ID、名称、颜色、样本计数。

### 外显子表达
```
GET /expression/medianExonExpression?gencodeId=ENSG00000139618.17&datasetId=gtex_v8
```

### 转录本表达
```
GET /expression/medianTranscriptExpression?gencodeId=ENSG00000139618.17&datasetId=gtex_v8
```

### 组织中表达最高的基因
```
GET /expression/topExpressedGene?tissueSiteDetailId=Brain_Cortex&datasetId=gtex_v8&filterMtGene=true
```

### 位置变异（二元）
```
GET /association/dyneqtl?variantId=chr1_1000000_A_G_b38&gencodeId=ENSG00000139618.17&tissueSiteDetailId=Whole_Blood&datasetId=gtex_v8
```

## 组织 ID 示例
准确使用下划线分隔的名称：
- `Whole_Blood`、`Liver`、`Brain_Cortex`、 `Heart_Left_Ventricle`
- `Muscle_Skeletal`、`Adipose_Subcutaneous`、`Lung`、`Skin_Sun_Exposed_Lower_leg`

## 示例响应（中值基因表达）
```json
{
  "data": [
    {
      "datasetId": "gtex_v8",
      "gencodeId": "ENSG00000139618.17",
      "geneSymbol": "BRCA2",
      "median": 4.523,
      "tissueSiteDetailId": "Whole_Blood",
      "unit": "TPM"
    },
    {
      "datasetId": "gtex_v8",
      "gencodeId": "ENSG00000139618.17",
      "geneSymbol": "BRCA2",
      "median": 12.87,
      "tissueSiteDetailId": "Testis",
      "unit": "TPM"
    }
  ],
  "paging_info": { "numberOfPages": 1, "page": 0, "maxItemsPerPage": 250 }
}
```

## 速率限制
- 未发布速率限制
- 建议合理的请求节奏（~1-2 请求/秒）
- 对于批量分析，请从 GTEx 门户下载页面下载完整数据集

## 注：
- GTEx v8 是主要数据集；始终指定 `datasetId=gtex_v8`
- 基因 ID 必须是版本化的 GENCODE ID（例如，ENSG00000139618.17）
- 使用基因搜索端点将符号解析为版本化的 GENCODE ID
- `gencodeVersion=v26` 对应于 GTEx v8
