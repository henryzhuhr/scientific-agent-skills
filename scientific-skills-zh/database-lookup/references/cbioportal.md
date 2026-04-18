# cBioPortal API

## 基本 URL
```
https://www.cbioportal.org/api
```

## Auth
公共实例没有身份验证。私有/机构实例（例如 `genie.cbioportal.org`）需要通过 `Authorization: Bearer <token>` 标头提供数据访问令牌。

## 通用标头
```
Accept: application/json
Content-Type: application/json
```

## 通用查询参数

大多数列表端点支持这些：

|参数|类型 |描述 |默认 |
|---|---|---|---|
| `projection` |字符串|详细程度：`ID`、`SUMMARY`、`DETAILED`、`META` | `SUMMARY` |
| `pageNumber` |整数 |从零开始的页面索引 | `0` |
| `pageSize` |整数 |每页结果 | `10000000` |
| `sortBy` |字符串|排序依据 | 的属性变化|
| `direction` |字符串| `ASC` 或 `DESC` | `ASC` |

## 关键终点

### 研究

|方法|端点|描述 |
|---|---|---|
|获取 | `/studies` |列出所有癌症研究|
|获取 | `/studies/{studyId}` |获取单个研究|
|发布 | `/studies/fetch` |按 ID 获取多个研究 |

E示例：
```
GET https://www.cbioportal.org/api/studies?projection=SUMMARY&pageSize=10
GET https://www.cbioportal.org/api/studies/brca_tcga
```

响应字段：`studyId`、`name`、`description`、`cancerTypeId`、`pmid`、`citation`、 `allSampleCount`、`referenceGenome`、`publicStudy`、`importDate`

### 癌症类型

|方法|端点|描述 |
|---|---|---|
|获取 | `/cancer-types` |列出所有癌症类型 |
|获取 | `/cancer-types/{cancerTypeId}` |获取一种癌症类型 |

响应字段：`cancerTypeId`、`name`、`shortName`、`dedicatedColor`、`parent`

### 基因

|方法|端点|描述 |
|---|---|---|
|获取 | `/genes` |列出所有基因（分页）|
|获取 | `/genes/{geneId}` |基因由 Hugo 符号或 Entrez ID |
|获取 | `/genes/{geneId}/aliases` |基因别名 |
|发布 | `/genes/fetch` |获取多个基因 |

示例：
```
GET https://www.cbioportal.org/api/genes/TP53
```
响应：`{"entrezGeneId": 7157, "hugoGeneSymbol": "TP53", "type": "protein-coding"}`

### 分子概况

|方法|端点|描述 |
|---|---|---|
|获取 | `/molecular-profiles` |所有研究的所有概况|
|获取 | `/studies/{studyId}/molecular-profiles` |研究中的概况|
|获取 | `/molecular-profiles/{molecularProfileId}` |单型材|

型材类型（`molecularAlterationType`）：`MUTATION_EXTENDED`、`COPY_NUMBER_ALTERATION`、`MRNA_EXPRESSION`、`PROTEIN_LEVEL`、 `METHYLATION`

示例：
```
GET https://www.cbioportal.org/api/studies/brca_tcga/molecular-profiles
```

### 突变

|方法|端点|描述 |
|---|---|---|
|获取 | `/molecular-profiles/{profileId}/mutations` |配置文件中的突变 |
|发布 | `/molecular-profiles/{profileId}/mutations/fetch` |过滤突变查询|
|发布 | `/mutations/fetch` |多配置文件突变获取 |

 GET 参数：
|参数|类型 |描述 |
|---|---|---|
| `sampleListId` |字符串|要查询的示例列表（例如 `brca_tcga_all`）|
| `entrezGeneId` |整数 |按基因过滤|
| `projection` |字符串| `SUMMARY`、`DETAILED`、`ID`、`META` |

示例 — TCGA 乳腺癌中的 TP53 突变：
```
GET https://www.cbioportal.org/api/molecular-profiles/brca_tcga_mutations/mutations?sampleListId=brca_tcga_all&entrezGeneId=7157&projection=DETAILED
```

POST 多基因体获取：
```json
{
  "sampleListId": "brca_tcga_all",
  "entrezGeneIds": [7157, 672]
}
```

响应字段：`entrezGeneId`、`sampleId`、`patientId`、`proteinChange`、`mutationType`、`mutationStatus`、`chr`、 `startPosition`、`endPosition`、`referenceAllele`、`variantAllele`、`variantType`、`ncbiBuild`、`tumorAltCount`、`tumorRefCount`

### 副本编号变更

|方法|端点|描述 |
|---|---|---|
|获取 | `/molecular-profiles/{profileId}/discrete-copy-number` | CNA数据|
|发布 | `/molecular-profiles/{profileId}/discrete-copy-number/fetch` |已过滤的 CNA 查询 |
|发布 | `/discrete-copy-number/fetch` |多谱 CNA 获取 |

### 分子数据（表达、甲基化）

|方法|端点|描述 |
|---|---|---|
|获取 | `/molecular-profiles/{profileId}/molecular-data` |表达/甲基化数据|
|发布 | `/molecular-data/fetch` |多轮廓分子数据获取 |

### 临床数据

|方法|端点|描述 |
|---|---|---|
|获取 | `/studies/{studyId}/clinical-data` |研究的临床数据|
|发布 | `/clinical-data/fetch` |多项研究临床数据|
|获取 | `/studies/{studyId}/clinical-attributes` |可用临床属性 |

 GET 参数：
|参数|类型 |描述 |
|---|---|---|
| `clinicalDataType` |字符串| `PATIENT` 或 `SAMPLE` |
| `attributeId` |字符串|例如`OS_STATUS`、`OS_MONTHS`、`CANCER_TYPE` |

示例：
```
GET https://www.cbioportal.org/api/studies/brca_tcga/clinical-data?clinicalDataType=PATIENT&attributeId=OS_STATUS&projection=SUMMARY
```

### 患者和样本

|方法|端点|描述 |
|---|---|---|
|获取 | `/studies/{studyId}/patients` |研究中的患者|
|获取 | `/studies/{studyId}/samples` |研究中的样本|
|发布 | `/patients/fetch` |多研究患者获取|
|发布 | `/samples/fetch` |多研究样本获取 |

### 样本列表

|方法|端点|描述 |
|---|---|---|
|获取 | `/studies/{studyId}/sample-lists` |预定义样本组|
|获取 | `/sample-lists/{sampleListId}` |单样本列表|

### 基因Panel

|方法|端点|描述 |
|---|---|---|
|获取 | `/gene-panels` |所有基因面板|
|获取 | `/gene-panels/{genePanelId}` |带有基因列表的面板详细信息|
|发布 | `/gene-panel-data/fetch` |哪些面板覆盖哪些样品 |

### 处理

|方法|端点|描述 |
|---|---|---|
|发布 | `/treatments/patient` |患者级治疗数据|
|发布 | `/treatments/sample` |样本级处理数据|

### 系统

|方法|端点|描述 |
|---|---|---|
|获取 | `/health` |服务器健康检查|
|获取 | `/info` |门户版本、数据库模式版本 |

## 典型工作流程

1. **查找研究**：`GET /studies` — 浏览可用的癌症研究，获取 `studyId` 值 
2. **获取分子概况**：`GET /studies/{studyId}/molecular-profiles` — 查找概况 ID（例如 `brca_tcga_mutations`、`brca_tcga_gistic`）
3. **获取样本列表**：`GET /studies/{studyId}/sample-lists` — 查找样本列表 ID（例如 `brca_tcga_all`、`brca_tcga_sequenced`）
4. **查询数据**：使用配置文件 ID 和样本列表 ID 来获取突变、CNA、表达或临床数据

## 速率限制

没有发布的速率限制。要有礼貌——避免多次提出并发请求。对于大量数据需求，cBioPortal 在 https://docs.cbioportal.org/downloads/.

## 提供可下载的数据集 ## Tips

- **研究 ID** 遵循以下模式：`{cancer_type}_{source}`（例如 `brca_tcga`、`luad_tcga`、 `prad_mskcc_2017`)
- **分子谱 ID** 扩展研究 ID：`{studyId}_mutations`、`{studyId}_gistic`、`{studyId}_rna_seq_v2_mrna`
- 使用 `projection=DETAILED` 获得最丰富的响应，包括嵌套对象
- POST `/fetch` 端点用于跨多个研究、基因或样本的批量查询 - 它们是最灵活的查询方式
  - 基因查找接受 Hugo 符号 (`TP53`)和 Entrez ID (`7157`)
  - Swagger UI https://www.cbioportal.org/api/swagger-ui/index.html 以交互方式记录每个端点
