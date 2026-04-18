# 代谢组学工作台 REST API

## 基本 URL
```
https://www.metabolomicsworkbench.org/rest/
```

## Auth
无需 API 密钥。完全公开。

## URL结构
```
/rest/{context}/{input_item}/{input_value}/{output_item}
```

上下文：`study`、`compound`、`refmet`、`gene`、`protein`、`moverz`、 `exactmass`

## 关键端点

### 研究背景
| URL 模式 |描述 |
|---|---|
| `/rest/study/study_id/{ST_ID}/summary` |研究摘要元数据|
| `/rest/study/study_id/{ST_ID}/metabolites` |研究中的代谢物|
| `/rest/study/study_id/{ST_ID}/analysis` |分析详情|
| `/rest/study/study_id/{ST_ID}/factors` |实验因素|
| `/rest/study/study_id/{ST_ID}/data` |命名代谢物数据矩阵|
| `/rest/study/study_id/{ST_ID}/species` |品种信息|
| `/rest/study/study_id/{ST_ID}/disease` |疾病信息|
| `/rest/study/study_title/{keyword}/summary` |按标题关键词搜索研究|
| `/rest/study/study_type/{type}/summary` |按研究类型搜索|
| `/rest/study/analysis_id/{AN_ID}/summary` |按分析 ID |

 研究 ID 进行摘要：`ST######`（例如，`ST000001`）。分析 ID：`AN######`.

### 复合上下文
| URL 模式 |描述 |
|---|---|
| `/rest/compound/name/{NAME}/summary` |按名称搜索化合物 |
| `/rest/compound/pubchem_cid/{CID}/summary` |按 PubChem CID 搜索 |
| `/rest/compound/hmdb_id/{HMDB_ID}/summary` |按HMDB ID搜索|
| `/rest/compound/kegg_id/{KEGG_ID}/summary` |按 KEGG ID 搜索 |
| `/rest/compound/inchi_key/{KEY}/summary` |按 InChI 键搜索 |
| `/rest/compound/regno/{REGNO}/classification` |复合分类|
| `/rest/compound/regno/{REGNO}/molfile` | MOL 文件（结构）|

### RefMet（标准化命名法）
| URL 模式 |描述 |
|---|---|
| `/rest/refmet/name/{NAME}/all` |完整 RefMet 记录 |
| `/rest/refmet/match/{NAME}/name` |将名称与标准化 RefMet 名称匹配 |

### 基因/蛋白质上下文
| URL 模式 |描述 |
|---|---|
| `/rest/gene/gene_symbol/{SYMBOL}/all` |按符号显示的基因信息 |
| `/rest/gene/gene_id/{ID}/all` |基因信息由 Entrez ID |
|提供`/rest/protein/uniprot_id/{ID}/all` | UniProt ID 提供的蛋白质 |

### 质量搜索 (MoverZ / ExactMass)
```
/rest/moverz/mz/{MZ_VALUE}/tol/{TOLERANCE}/mode/{pos|neg}
/rest/exactmass/mass/{MASS_VALUE}/tol/{TOLERANCE}
```

## 调用示例

```
# Study summary
https://www.metabolomicsworkbench.org/rest/study/study_id/ST000001/summary

# Metabolites in a study
https://www.metabolomicsworkbench.org/rest/study/study_id/ST000001/metabolites

# Search studies by title
https://www.metabolomicsworkbench.org/rest/study/study_title/diabetes/summary

# Compound by name
https://www.metabolomicsworkbench.org/rest/compound/name/glucose/summary

# Compound by PubChem CID
https://www.metabolomicsworkbench.org/rest/compound/pubchem_cid/5793/summary

# RefMet standardized name match
https://www.metabolomicsworkbench.org/rest/refmet/match/alpha-D-Glucose/name

# m/z search in positive mode
https://www.metabolomicsworkbench.org/rest/moverz/mz/175.0354/tol/0.005/mode/pos

# Exact mass search
https://www.metabolomicsworkbench.org/rest/exactmass/mass/174.0282/tol/0.005
```

## 响应格式
默认为JSON。 `mwtab` 输出返回 MWTab 文本。 `molfile` 返回 MOL/SDF 文本。无分页 — 返回完整结果。

## 速率限制
没有发布的限制。讲道理。批量调用增加0.5-1s延迟。
