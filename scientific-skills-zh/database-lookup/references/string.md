# STRING REST API

## 基本 URL

```
https://string-db.org/api
```

## URL 模式

```
/api/{output_format}/{method}
```

- **输出格式**：`json`、`tsv`、`tsv-no-header`、 `image`、`svg`（并非所有端点的所有格式）
- **方法**：端点名称（见下文）

## 身份验证

无需 API 密钥。所有端点都是公共的。

## 关键端点

### 1. 解析蛋白质标识符

将蛋白质名称/标识符映射到 STRING 内部 ID。始终首先执行此操作以获取规范的 STRING ID。

```
GET /api/json/resolve?identifier={query}&species={taxid}
```

|参数|类型 |描述 |
|-------------|--------|-------------|
| `identifier` |字符串| **必填。** 蛋白质名称、基因符号或外部 ID。 |
| `species` |整数 | NCBI 分类 ID（9606 = 人类，10090 = 小鼠）。建议避免歧义。 |

* *示例：**
```
https://string-db.org/api/json/resolve?identifier=TP53&species=9606
```

* *响应：**
```json
[
  {
    "stringId": "9606.ENSP00000269305",
    "preferredName": "TP53",
    "ncbiTaxonId": 9606,
    "taxonName": "Homo sapiens",
    "annotation": "Cellular tumor antigen p53; ..."
  }
]
```

- --

### 2. 获取交互伙伴（网络）

```
GET /api/json/interaction_partners?identifiers={proteins}&species={taxid}
```

|参数|类型 |描述 |
|--------------------|--------|-------------|
| `identifiers` |字符串| **必填。** 蛋白质名称。使用 `%0d`（换行符）分隔多个。 |
| `species` |整数 | NCBI 分类 ID。 |
| `limit` |整数 |返回的相互作用伙伴的最大数量（每个输入蛋白质）。 |
| `required_score` |整数 |最低综合分数（0-1000）。默认值：400。常见阈值：400（中）、700（高）、900（最高）。 |
| `network_type` |字符串| `functional`（默认，所有关联）或 `physical`（仅限物理绑定）。 |

* *示例：**
```
https://string-db.org/api/json/interaction_partners?identifiers=TP53&species=9606&limit=10&required_score=900
```

* *响应：**
```json
[
  {
    "stringId_A": "9606.ENSP00000269305",
    "stringId_B": "9606.ENSP00000261842",
    "preferredName_A": "TP53",
    "preferredName_B": "MDM2",
    "ncbiTaxonId": 9606,
    "score": 0.999,
    "nscore": 0,
    "fscore": 0,
    "pscore": 0,
    "ascore": 0.93,
    "escore": 0.994,
    "dscore": 0.9,
    "tscore": 0.981
  }
]
```

评分通道：`nscore`（邻域）、`fscore`（融合）、`pscore`（系统发育共现）、 `ascore`（共表达）、`escore`（实验）、`dscore`（数据库/策划）、`tscore`（文本挖掘）。

- --

### 3.获取一组之间的网络交互蛋白质

```
GET /api/json/network?identifiers={proteins}&species={taxid}
```

|参数|类型 |描述 |
|------------------|--------|-------------|
| `identifiers` |字符串| **必需。** 蛋白质名称由 `%0d`（换行编码）分隔。 |
| `species` |整数 | NCBI 分类 ID。 |
| `required_score` |整数 |最低综合分数（0-1000）。 |
| `network_type` |字符串| `functional` 或 `physical`。 |
| `add_nodes` |整数 |要添加的额外交互者的数量（扩展网络）。 |

* *示例 - 一组蛋白质之间的网络：**
```
https://string-db.org/api/json/network?identifiers=TP53%0dBRCA1%0dATM%0dCHEK2%0dMDM2&species=9606&required_score=700
```

返回输入集之间的所有成对相互作用。

- --

### 4. 网络image

```
GET /api/image/network?identifiers={proteins}&species={taxid}
GET /api/svg/network?identifiers={proteins}&species={taxid}
```

返回交互网络的PNG图像或SVG。

* *示例：**
```
https://string-db.org/api/image/network?identifiers=TP53%0dBRCA1%0dMDM2&species=9606
```

- --

### 5.功能富集分析

执行基因对一组蛋白质进行本体论、KEGG 通路等富集分析。

```
GET /api/json/enrichment?identifiers={proteins}&species={taxid}
```

|参数|类型 |描述 |
|--------------|--------|------------|
| `identifiers` |字符串| **必需。** 以换行符分隔的 (`%0d`)蛋白质名称。 |
| `species` |整数 | NCBI 分类 ID。 |

* *示例：**
```
https://string-db.org/api/json/enrichment?identifiers=TP53%0dBRCA1%0dATM%0dCHEK2%0dCDK2%0dCDKN1A&species=9606
```

* *回复：**
```json
[
  {
    "category": "Process",
    "term": "GO:0006974",
    "description": "cellular response to DNA damage stimulus",
    "number_of_genes": 6,
    "number_of_genes_in_background": 781,
    "ncbiTaxonId": 9606,
    "inputGenes": "TP53,BRCA1,ATM,CHEK2,CDK2,CDKN1A",
    "preferredNames": "TP53,BRCA1,ATM,CHEK2,CDK2,CDKN1A",
    "p_value": 1.2e-12,
    "fdr": 5.6e-10
  }
]
```

类别包括：`Process`（GO 生物过程）、`Function`（GO 分子功能）、`Component`（GO 细胞）组件）、`KEGG`、`Pfam`、`InterPro`、`SMART`、`Keyword`（UniProt）、`Reactome`、`WikiPathways`、`HPO`（人类表型） Ontology).

- --

### 6.获取蛋白质注释/信息

```
GET /api/json/get_string_ids?identifiers={proteins}&species={taxid}
```

将任意名称映射到带有注释的STRING ID text.

* *示例：**
```
https://string-db.org/api/json/get_string_ids?identifiers=CDK2%0dp53&species=9606
```

* *响应：**
```json
[
  {
    "queryIndex": 0,
    "queryItem": "CDK2",
    "stringId": "9606.ENSP00000266970",
    "ncbiTaxonId": 9606,
    "taxonName": "Homo sapiens",
    "preferredName": "CDK2",
    "annotation": "Cyclin-dependent kinase 2; ..."
  }
]
```

- --

### 7. 在另一个中获取同源/最佳命中品种

```
GET /api/json/homology?identifiers={proteins}&species={taxid}&species_b={taxid_b}
```

|参数|类型 |描述 |
|------------|-----|------------|
| `identifiers` |字符串|来源蛋白质。 |
| `species` |整数 |源种。 |
| `species_b` |整数 |同源物查找的目标物种。 |

* *示例：**
```
https://string-db.org/api/json/homology?identifiers=TP53&species=9606&species_b=10090
```

- --

### 8. PPI 丰富（我的集合比预期？）

```
GET /api/json/ppi_enrichment?identifiers={proteins}&species={taxid}
```

* *示例：**
```
https://string-db.org/api/json/ppi_enrichment?identifiers=TP53%0dBRCA1%0dATM%0dCHEK2&species=9606
```

* *响应：**
```json
[
  {
    "number_of_nodes": 4,
    "number_of_edges": 6,
    "average_node_degree": 3.0,
    "local_clustering_coefficient": 1.0,
    "expected_number_of_edges": 1,
    "p_value": 0.000123
  }
]
```

- --

## 常见物种分类ID

|物种 |分类单元 ID |
|------|----------|
|智人（人类）| 9606 |
|小家鼠（小鼠）| 10090 |
|褐家鼠（大鼠）| 10116 |
|果蝇（果蝇）|第7227章酿酒酵母（酵母）|第4932章秀丽隐杆线虫（蠕虫）|第6239章斑马鱼 | Danio rerio 7955 |
|大肠杆菌 K12 | 511145 |
|拟南芥|第3702章- 没有发布硬速率限制，但 API 旨在以中等速率进行编程访问。
- 建议：**每秒最多 1 个请求**。
- 对于大规模数据下载，请改用 STRING 网站上的平面文件下载。
- 如果发送太多请求，可能会收到 HTTP 429 或临时阻止。
- 强烈建议每个请求使用多个标识符

## 错误处理

 - 对于格式错误的请求，返回 HTTP 400。
  - 如果找不到匹配的蛋白质，则返回 HTTP 404。
  - 如果查询有效但没有返回结果，则空 JSON 数组 `[]`（例如，上面没有交互）阈值）。
  - 尽可能包含 `species` 参数，以避免不明确的标识符解析。
