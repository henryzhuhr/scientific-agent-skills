# UniProt REST API

## 基本 URL

```
https://rest.uniprot.org
```

## 身份验证

无需 API 密钥。所有端点都是公共的。

## 关键端点

### 1.搜索蛋白质

```
GET /uniprotkb/search
```

* *参数：**

|参数|类型 |描述 |
|-----------|--------|-------------|
| `query` |字符串| **必需。** 使用 UniProt 查询语法（字段：值对、布尔运算符）搜索查询。 |
| `format` |字符串| `json`（默认）、`tsv`、`fasta`、`xml`、`list`、`xlsx`、`obo` |
| `fields` |字符串|要返回的以逗号分隔的列列表。关键字段：`accession`、`id`、`protein_name`、`gene_names`、`organism_name`、`organism_id`、`length`、`sequence`、`cc_function`、`go_id`、 `go`、`xref_pdb`、`reviewed`、`ec`、`cc_subcellular_location`、`ft_domain`、`lineage` |
| `size` |整数 |每页结果（最多 500 个，默认 25）|
| `cursor` |字符串|分页游标（在`Link`响应头中返回）|
| `sort` |字符串|对字段和方向进行排序，例如`gene asc`、`length desc`、`annotation_score desc` |

* *调用示例：**

搜索已审查的人类 TP53：
```
https://rest.uniprot.org/uniprotkb/search?query=(gene:TP53) AND (organism_id:9606) AND (reviewed:true)&format=json&fields=accession,protein_name,gene_names,organism_name,length,cc_function&size=10
```

 按蛋白质名称搜索关键词：
```
https://rest.uniprot.org/uniprotkb/search?query=(protein_name:insulin) AND (reviewed:true)&format=json&size=5
```

 按 EC 编号搜索（酶分类）：
```
https://rest.uniprot.org/uniprotkb/search?query=(ec:2.7.11.1) AND (organism_id:9606)&format=json&size=25
```

 按基因本体搜索：
```
https://rest.uniprot.org/uniprotkb/search?query=(go:0006915) AND (organism_id:9606) AND (reviewed:true)&format=json&size=25
```

* *响应(JSON):**
```json
{
  "results": [
    {
      "entryType": "UniProtKB reviewed (Swiss-Prot)",
      "primaryAccession": "P04637",
      "uniProtkbId": "P53_HUMAN",
      "organism": {
        "scientificName": "Homo sapiens",
        "taxonId": 9606
      },
      "proteinDescription": {
        "recommendedName": {
          "fullName": { "value": "Cellular tumor antigen p53" }
        }
      },
      "genes": [
        {
          "geneName": { "value": "TP53" },
          "synonyms": [{ "value": "P53" }]
        }
      ],
      "sequence": {
        "value": "MEEPQSDP...",
        "length": 393,
        "molWeight": 43653,
        "crc64": "..."
      },
      "comments": [...],
      "features": [...],
      "references": [...]
    }
  ]
}
```

* *分页:** `Link` 响应标头包含带有光标参数的下一页 URL。 

- --

### 2. 通过访问获取单个条目

```
GET /uniprotkb/{accession}
```

* *参数：**

|参数|类型 |说明|
|------------|--------|-------------|
| `format` |字符串| `json`、`tsv`、`fasta`、`xml`、`gff` |

* *调用示例：**

```
https://rest.uniprot.org/uniprotkb/P04637?format=json
https://rest.uniprot.org/uniprotkb/P04637.fasta
```

- --

### 3. FASTA 序列检索

将`.fasta`附加到登录中或使用`format=fasta`：

```
https://rest.uniprot.org/uniprotkb/P04637.fasta
```

从搜索中批量FASTA：
```
https://rest.uniprot.org/uniprotkb/search?query=(gene:BRCA1) AND (organism_id:9606) AND (reviewed:true)&format=fasta
```

- --

### 4. ID映射（ID类型之间转换）

ID映射是一个两步异步过程。

* *步骤1：提交作业**
```
POST /idmapping/run
Content-Type: application/x-www-form-urlencoded

from={dbFrom}&to={dbTo}&ids={comma-separated-ids}
```

常用`from`/`to`数据库名称：
- `UniProtKB_AC-ID` (UniProt 登录)
- `Gene_Name`
- `GeneID` (NCBI 基因/Entrez 基因)
- `Ensembl`、`Ensembl_Genomes`
- `RefSeq_Protein`
- `PDB`
- `ChEMBL`
- `EMBL-GenBank-DDBJ`
- `STRING`

返回：
```json
{ "jobId": "abc123def456" }
```

* *步骤 2：投票并检索结果**
```
GET /idmapping/status/{jobId}
```
完成后，重定向到：
```
GET /idmapping/results/{jobId}?format=json&size=500
```

* *示例：**

将 Ensembl 基因 ID 映射到 UniProt 种质：
```
POST /idmapping/run
from=Ensembl&to=UniProtKB_AC-ID&ids=ENSG00000141510,ENSG00000012048
```

Map UniProt 转 PDB：
```
POST /idmapping/run
from=UniProtKB_AC-ID&to=PDB&ids=P04637,P38398
```

* *响应（结果）：**
```json
{
  "results": [
    {
      "from": "ENSG00000141510",
      "to": {
        "primaryAccession": "P04637",
        "uniProtkbId": "P53_HUMAN",
        ...
      }
    }
  ]
}
```

- --

### 5. UniRef（集群序列）

```
GET /uniref/search?query={query}&format=json
GET /uniref/{id}
```

集群 ID：`UniRef100_P04637`、`UniRef90_P04637`、`UniRef50_P04637`

- --

### 6. UniParc（序列存档）

```
GET /uniparc/search?query={query}&format=json
GET /uniparc/{upi}
```

- --

### 7. 蛋白质组

```
GET /proteomes/search?query=(organism_id:9606)&format=json
GET /proteomes/{upid}
```

示例 — 人类参考proteome:
```
https://rest.uniprot.org/proteomes/UP000005640?format=json
```

- --

### 8. Taxonomy

```
GET /taxonomy/search?query={query}&format=json
GET /taxonomy/{taxonId}
```

- --

## 查询语法

UniProt 搜索查询支持带有布尔值的 field:value 语法运营商：

- `(gene:TP53)` -- 基因名称
- `(organism_id:9606)` -- NCBI 分类 ID（9606 = 人类，10090 = 小鼠）
- `(organism_name:"Homo sapiens")` -- 生物名称
- `(reviewed:true)` -- 仅 Swiss-Prot（手动）已审查）
- `(protein_name:kinase)` -- 蛋白质名称包含关键字
- `(ec:2.7.11.1)` -- 酶分类
- `(go:0006915)` -- 基因本体术语ID
- `(xref:pdb-P04637)` -- 交叉引用
- `(length:[100 TO 300])` -- 序列长度范围
- `(cc_disease:cancer)` -- 疾病涉及情况
- `(ft_domain:SH2)` -- 结构域注释
- `(cc_subcellular_location:nucleus)` -- 亚细胞位置
- `(date_modified:[2024-01-01 TO *])` -- 修饰日期

与`AND`组合， `OR`，`NOT`：
```
(gene:BRCA1) AND (organism_id:9606) AND (reviewed:true)
```

## 速率限制

- 没有硬发布的速率限制，但过多的请求将被限制。
- 使用分页（`size` + `cursor`）进行批处理结果。
- 批量 ID 映射作业，而不是一次查找。
- 对于大型下载，请使用流式传输端点或 FTP 站点。
- 如果收到 HTTP 429，请尊重 `Retry-After` 标头。

## 错误格式

```json
{
  "url": "https://rest.uniprot.org/...",
  "messages": ["Error message here"]
}
```

HTTP 400表示错误查询，404表示未找到，429表示速率限制，500表示服务器错误。
