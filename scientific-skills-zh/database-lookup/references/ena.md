# 欧洲核苷酸档案 (ENA) API 参考

## 概述
ENA 是欧洲的主要核苷酸序列存储库，与 NCBI GenBank 和 DDBJ 一起属于国际核苷酸序列数据库协作 (INSDC)的一部分。它存储原始测序读数、组装序列、基因组组装和相关元数据。 ENA 为不同的访问模式提供了五个互补的 API。

## 1. ENA Portal API（高级搜索）

### 基本 URL
```
https://www.ebi.ac.uk/ena/portal/api
```

 无需身份验证。所有端点都是公共的。

### 关键端点

#### 搜索记录
```
GET /search?result={result_type}&query={query}&fields={fields}&limit={N}&format={format}
```

|参数|类型 |描述|
|---------|------|----------|
| `result` |字符串| **必需。** 要搜索的数据类型。请参阅下面的结果类型。 |
| `query` |字符串|使用 ENA 查询语法搜索查询。 |
| `fields` |字符串|要返回的以逗号分隔的字段列表。使用 `/returnFields` 查看每个结果类型的可用字段。 |
| `limit` |整数 |返回的最大结果数（默认 100000）。 |
| `offset` |整数 |分页偏移。 |
| `format` |字符串| `json`（默认）、`tsv`。 |

* *查询语法：**
```
tax_id=9606 AND description="*hemoglobin*"
tax_id=9606 AND library_strategy="RNA-Seq"
accession="PRJEB40665"
scientific_name="Escherichia coli" AND dataclass="STD"
country="United Kingdom" AND first_public>2024-01-01
```

运算符：`=`、`!=`、`>`、`<`、`>=`、`<=`。使用`AND`、`OR`、`NOT`。通配符：`*`。将值用双引号括起来。

* *示例 -- 搜索人类 RNA-Seq 运行：**
```
https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=tax_id%3D9606%20AND%20library_strategy%3D%22RNA-Seq%22&fields=run_accession,experiment_accession,sample_accession,study_accession,instrument_platform,library_strategy,read_count,base_count&limit=5&format=json
```

* *示例 -- 搜索核苷酸序列有机体：**
```
https://www.ebi.ac.uk/ena/portal/api/search?result=sequence&query=tax_id%3D9606%20AND%20description%3D%22*hemoglobin*%22&fields=accession,description,tax_id,scientific_name,base_count&limit=5&format=json
```

* *响应：**
```json
[
  {
    "accession": "AA126503",
    "description": "zk94h05.s1 Soares_pregnant_uterus_NbHPU Homo sapiens cDNA clone ...",
    "tax_id": "9606"
  }
]
```

#### 计数记录
```
GET /count?result={result_type}&query={query}
```

返回一个普通整数count.

* *示例：**
```
https://www.ebi.ac.uk/ena/portal/api/count?result=read_run&query=tax_id%3D9606%20AND%20library_strategy%3D%22RNA-Seq%22
```

#### 列出可用的结果类型
```
GET /results?format=json
```

#### 列出结果类型的可搜索字段
```
GET /searchFields?result={result_type}
```

#### 列表结果类型的可返回字段
```
GET /returnFields?result={result_type}
```

### 结果类型

|结果类型 |描述|
|-------------|--------------|
| `sequence` |核苷酸序列|
| `coding` |编码序列 (CDS) |
| `noncoding` |非编码序列|
| `read_run` |原始测序读取（运行）|
| `read_experiment` |测序实验|
| `read_study` |原始读取研究|
| `analysis` |分析|
| `analysis_study` |分析研究|
| `assembly` |基因组组装 |
| `sample` |样品|
| `study` |研究|
| `taxon` |分类学分类|
| `wgs_set` |基因组组装重叠群集 (WGS) |
| `tsa_set` |转录组组装重叠群集 (TSA) |
| `tls_set` |目标位点研究重叠群集 (TLS) |

- --

## 2. ENA 浏览器 API（记录检索）

### 基本 URL
```
https://www.ebi.ac.uk/ena/browser/api
```

 使用此功能可按登录号直接检索记录。

### 密钥端点

#### 以 XML 格式检索记录
```
GET /xml/{accession}
```

* *示例：**
```
https://www.ebi.ac.uk/ena/browser/api/xml/PRJEB40665
https://www.ebi.ac.uk/ena/browser/api/xml/SRR12345678
https://www.ebi.ac.uk/ena/browser/api/xml/ERS1234567
```

#### 在 EMBL 平面文件中检索记录格式
```
GET /embl/{accession}
```

* *示例：**
```
https://www.ebi.ac.uk/ena/browser/api/embl/AY585947
```

支持`?lineLimit=N`截断长记录。

#### 在FASTA中检索序列格式
```
GET /fasta/{accession}
```

* *示例：**
```
https://www.ebi.ac.uk/ena/browser/api/fasta/AY585947
```

### 响应格式

|端点|格式|使用案例|
|----------|--------|----------|
| `/xml/{accession}` | XML |用于研究、样品、实验、运行的完整结构化元数据 |
| `/embl/{accession}` | EMBL 平面文件 |具有特征的注释序列 |
| `/fasta/{accession}` |法斯塔 |原始核苷酸/蛋白质序列 |

### 登录类型

|前缀|实体|示例 |
|--------|--------|---------|
| `PRJEB` / `PRJNA` / `PRJDB` |研究/项目| `PRJEB40665` |
| `ERX` / `SRX` / `DRX` |实验| `ERX1234567` |
| `ERS` / `SRS` / `DRS` |样品| `ERS1234567` |
| `ERR` / `SRR` / `DRR` |运行| `ERR1234567` |
| `GCA` |基因组组装| `GCA_000001405.29` |
|标准 INSDC |序列| `AY585947`、`M10051` |

- --

## 3. ENA 分类 REST API

### 基本 URL
```
https://www.ebi.ac.uk/ena/taxonomy/rest
```

### 关键端点

#### 按分类查找ID
```
GET /tax-id/{taxId}
```

* *示例：**
```
https://www.ebi.ac.uk/ena/taxonomy/rest/tax-id/9606
```

* *响应：**
```json
{
  "taxId": 9606,
  "scientificName": "Homo sapiens",
  "commonName": "human",
  "formalName": true,
  "rank": "species",
  "division": "HUM",
  "lineage": "Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; ...; Homo; ",
  "geneticCode": "1",
  "mitochondrialGeneticCode": "2",
  "submittable": true,
  "binomial": true,
  "metagenome": false,
  "otherNames": [
    {"nameClass": "authority", "name": "Linnaeus, 1758"},
    {"nameClass": "genbank common name", "name": "human"}
  ]
}
```

#### 按科学搜索名称
```
GET /scientific-name/{name}
```

* *示例：**
```
https://www.ebi.ac.uk/ena/taxonomy/rest/scientific-name/Homo%20sapiens
```

返回匹配分类记录的数组。

#### 按常见搜索名称
```
GET /any-name/{name}
```

* *示例：**
```
https://www.ebi.ac.uk/ena/taxonomy/rest/any-name/human
```

#### 建议名称（自动完成）
```
GET /suggest-for-submission/{partialName}
```

* *示例：**
```
https://www.ebi.ac.uk/ena/taxonomy/rest/suggest-for-submission/Homo%20sap
```

- --

## 4. ENA 交叉参考服务

### 基础URL
```
https://www.ebi.ac.uk/ena/xref/rest
```

检索 ENA 记录和外部数据库（UniProt、PDB、PubMed 等）之间的链接。

### 关键端点

#### 搜索交叉引用加入
```
GET /json/search?accession={accession}
```

|参数|类型 |描述|
|---------|------|----------|
| `accession` |字符串| ENA 加入以查找交叉引用。 |
| `source` |字符串|按源数据库过滤（例如，`UniProtKB`）。 |
| `target` |字符串|按目标类型过滤。 |
| `limit` |整数 |最大结果。 |
| `offset` |整数 |分页偏移。 |

* *示例：**
```
https://www.ebi.ac.uk/ena/xref/rest/json/search?accession=A00145
```

* *响应：**
```json
[
  {
    "Source": "EuropePMC",
    "Source Primary Accession": "PMC12345",
    "Source Secondary Accession": "",
    "Source URL": "https://europepmc.org/...",
    "Source Secondary URL": "",
    "Target": "sequence",
    "Target Primary Accession": "A00145",
    "Target Secondary Accession": "",
    "Target URL": "https://www.ebi.ac.uk/ena/...",
    "Has Inferred": "N",
    "Inferred From": ""
  }
]
```

- --

## 5. CRAM 参考注册表

### 基础URL
```
https://www.ebi.ac.uk/ena/cram
```

检索 CRAM 文件压缩中使用的参考序列。

### 关键端点

#### 通过 MD5 校验和查找
```
GET /md5/{md5}
```

* *示例：**
```
https://www.ebi.ac.uk/ena/cram/md5/b1eba5b6e4440e22e1e02f7e0febd2da
```

#### 通过 SHA1 校验和查找
```
GET /sha1/{sha1}
```

 返回 FASTA 中的参考序列format.

- --

## 常见搜索模式

```
# All RNA-Seq runs for a species
result=read_run&query=tax_id=9606 AND library_strategy="RNA-Seq"

# WGS assemblies for an organism
result=assembly&query=tax_id=562 AND assembly_type="primary metagenome"

# Sequences by study accession
result=sequence&query=study_accession="PRJEB40665"

# Samples from a country with collection date
result=sample&query=country="Germany" AND collection_date>=2024-01-01

# Coding sequences for a gene keyword
result=coding&query=description="*BRCA1*" AND tax_id=9606

# Count available datasets
/count?result=read_run&query=tax_id=9606

# Get metadata fields available for a result type
/returnFields?result=read_run
/searchFields?result=read_run
```

## 速率限制

- 无需身份验证
- 没有正式发布的速率限制，但要礼貌：避免超过〜5个并发请求
- 大型结果集：使用用于分页的 `limit` 和 `offset`
- 对于批量下载序列数据（FASTQ 等），请使用 ENA 的 FTP/Aspera 服务而不是 REST API

## Tips

- **ENA vs SRA**：ENA 和 NCBI SRA 互相镜像对方的数据（两者都是INSDC 成员）。 ENA 登记号 (ERR/ERX/ERS/PRJEB)和 NCBI 登记号 (SRR/SRX/SRS/PRJNA)交叉引用。使用具有您需要的查询功能的 API。
- **用于搜索的门户 API、用于检索的浏览器 API**：当您需要使用过滤器搜索多个记录时，请使用门户 API。当您有特定登录并需要完整记录时，请使用浏览器 API。
- **JSON 与 XML**：门户 API 返回 JSON 或 TSV。浏览器 API 主要返回 XML、EMBL 或 FASTA。
- **字段发现**：始终检查 `/returnFields?result={type}` 和 `/searchFields?result={type}` 以查看每种结果类型可用的内容 - 结果类型之间的字段不同。
- **交叉引用**：使用外部引用服务查找从 ENA 记录到 UniProt、PDB、PubMed 等的链接数据库.
