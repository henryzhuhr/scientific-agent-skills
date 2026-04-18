# Ensembl REST API

## Base URL

```
https://rest.ensembl.org
```

对于Ensembl Genomes（植物，真菌，细菌，原生生物，后生动物）：
```
https://rest.ensembl.org
```
（相同的基础；Ensembl Genomes已合并到主要REST中API.)

对于 GRCh37 (hg19)存档：
```
https://grch37.rest.ensembl.org
```

## 身份验证

无需 API 密钥。所有端点都是公共的。

## 公共标头

所有请求应包括：
```
Content-Type: application/json
```

API使用内容协商。将 `?content-type=application/json` 附加到 GET 请求，或设置 `Accept` 标头。

## 关键端点

### 1. 通过符号查找基因

```
GET /lookup/symbol/{species}/{symbol}?content-type=application/json
```

|参数|类型 |描述|
|------------|--------|-------------|
| `species` |字符串| **必填。** 物种名称（例如，`homo_sapiens`、`mus_musculus`）。 |
| `symbol` |字符串| **必填。** 基因符号（例如，`TP53`、`BRCA1`）。 |
| `expand` |整数 |设置为 `1` 以包括转录本、翻译、外显子。 |

* *示例：**
```
https://rest.ensembl.org/lookup/symbol/homo_sapiens/TP53?content-type=application/json
https://rest.ensembl.org/lookup/symbol/homo_sapiens/BRCA1?content-type=application/json;expand=1
```

* *响应：**
```json
{
  "id": "ENSG00000141510",
  "display_name": "TP53",
  "description": "tumor protein p53 [Source:HGNC Symbol;Acc:HGNC:11998]",
  "species": "homo_sapiens",
  "object_type": "Gene",
  "biotype": "protein_coding",
  "assembly_name": "GRCh38",
  "seq_region_name": "17",
  "start": 7661779,
  "end": 7687538,
  "strand": -1,
  "source": "ensembl_havana",
  "logic_name": "ensembl_havana_gene_homo_sapiens",
  "version": 16,
  "Transcript": [...]
}
```

- --

### 2. Ensembl 查找基因/特征ID

```
GET /lookup/id/{id}?content-type=application/json
```

|参数|类型 |描述|
|---------|--------|-------------|
| `id` |字符串| **必填。** Ensembl 稳定 ID（基因、转录本、蛋白质、外显子）。 |
| `expand` |整数 |设置为 `1` 以包含子对象（基因的转录本等）。 |
| `db_type` |字符串|数据库类型：`core`、`otherfeatures`、`cdna`、`rnaseq`。 |

* *示例：**
```
https://rest.ensembl.org/lookup/id/ENSG00000141510?content-type=application/json;expand=1
https://rest.ensembl.org/lookup/id/ENST00000269305?content-type=application/json
https://rest.ensembl.org/lookup/id/ENSP00000269305?content-type=application/json
```

- --

### 3. 批量查找（POST，最多 1000 个 ID）

```
POST /lookup/id
Content-Type: application/json

{ "ids": ["ENSG00000141510", "ENSG00000012048", "ENSG00000157764"] }
```

* *响应示例：** 返回由ID:
```json
{
  "ENSG00000141510": {
    "id": "ENSG00000141510",
    "display_name": "TP53",
    ...
  },
  "ENSG00000012048": { ... }
}
```

- --

### 4.序列检索

```
GET /sequence/id/{id}?content-type=application/json
```

|参数|类型 |描述 |
|--------------|--------|-------------|
| `id` |字符串| Ensembl 稳定 ID（基因、转录物或蛋白质）。 |
| `type` |字符串| `genomic`、`cdna`、`cds`、`protein`。默认值因对象类型而异。 |
| `format` |字符串| `json` 或 `fasta`。 |
| `expand_3prime` |整数 |将 3' 末端扩展 N 个碱基。 |
| `expand_5prime` |整数 |将 5' 末端扩展 N 个碱基。 |
| `mask` |字符串| `soft`（小写重复）或 `hard`（N 掩码重复）。 |

* *示例：**

 蛋白质序列：
```
https://rest.ensembl.org/sequence/id/ENSP00000269305?content-type=application/json
```

CDS 序列：
```
https://rest.ensembl.org/sequence/id/ENST00000269305?type=cds&content-type=application/json
```

 基因组序列侧翼：
```
https://rest.ensembl.org/sequence/id/ENSG00000141510?type=genomic&expand_5prime=1000&expand_3prime=500&content-type=application/json
```

FASTA 格式：
```
https://rest.ensembl.org/sequence/id/ENSP00000269305?content-type=text/x-fasta
```

* *响应（JSON）：**
```json
{
  "id": "ENSP00000269305",
  "seq": "MEEPQSDPSVEPPLSQETFSDL...",
  "molecule": "protein",
  "desc": "chromosome:GRCh38:17:7661779:7687538:-1"
}
```

- --

### 5. 序列Region

```
GET /sequence/region/{species}/{region}?content-type=application/json
```

区域格式：`chromosome:start..end`或`chromosome:start..end:strand`

* *示例：**
```
https://rest.ensembl.org/sequence/region/homo_sapiens/17:7661779..7662000:1?content-type=application/json
```

- --

### 6. 变体注释（VEP - 变异效应预测器）

* *按 HGVS 表示法：**
```
GET /vep/{species}/hgvs/{hgvs_notation}?content-type=application/json
```

* *示例：**
```
https://rest.ensembl.org/vep/homo_sapiens/hgvs/ENST00000269305.9:c.817C>T?content-type=application/json
https://rest.ensembl.org/vep/homo_sapiens/hgvs/17:g.7674220G>A?content-type=application/json
```

* *按基因组区域：**
```
GET /vep/{species}/region/{region}/{allele}?content-type=application/json
```

* *示例：**
```
https://rest.ensembl.org/vep/homo_sapiens/region/17:7674220-7674220:1/A?content-type=application/json
```

* *通过rsID:**
```
GET /vep/{species}/id/{rsid}?content-type=application/json
```

* *示例:**
```
https://rest.ensembl.org/vep/homo_sapiens/id/rs699?content-type=application/json
```

* *VEP 响应:**
```json
[
  {
    "input": "17:g.7674220G>A",
    "assembly_name": "GRCh38",
    "seq_region_name": "17",
    "start": 7674220,
    "end": 7674220,
    "strand": 1,
    "allele_string": "G/A",
    "most_severe_consequence": "missense_variant",
    "transcript_consequences": [
      {
        "gene_id": "ENSG00000141510",
        "gene_symbol": "TP53",
        "transcript_id": "ENST00000269305",
        "biotype": "protein_coding",
        "consequence_terms": ["missense_variant"],
        "impact": "MODERATE",
        "amino_acids": "R/H",
        "codons": "cGc/cAc",
        "protein_start": 248,
        "polyphen_prediction": "probably_damaging",
        "polyphen_score": 1.0,
        "sift_prediction": "deleterious",
        "sift_score": 0.0,
        "cadd_phred": 35.0
      }
    ],
    "colocated_variants": [
      {
        "id": "rs28934578",
        "frequencies": { ... },
        "clin_sig": ["pathogenic"]
      }
    ]
  }
]
```

* *批量 VEP（POST，最多 200 个）变体）：**
```
POST /vep/homo_sapiens/region
Content-Type: application/json

{ "variants": ["17 7674220 7674220 G/A 1", "7 140753336 140753336 A/T 1"] }
```

- --

### 7. 变体（已知变体rsID)

```
GET /variation/{species}/{rsid}?content-type=application/json
```

* *示例：**
```
https://rest.ensembl.org/variation/homo_sapiens/rs699?content-type=application/json
```

* *响应：**
```json
{
  "name": "rs699",
  "source": "Variants (including SNPs and indels) imported from dbSNP",
  "mappings": [
    {
      "seq_region_name": "1",
      "start": 230710048,
      "end": 230710048,
      "strand": 1,
      "allele_string": "A/G",
      "assembly_name": "GRCh38",
      "location": "1:230710048-230710048"
    }
  ],
  "MAF": 0.35,
  "minor_allele": "G",
  "clinical_significance": [],
  "synonyms": [],
  "ancestral_allele": "A"
}
```

- --

### 8. 重叠/功能区域

```
GET /overlap/region/{species}/{region}?feature={type}&content-type=application/json
```

|参数|类型 |描述|
|------------|--------|-------------|
| `region` |字符串|格式：`chr:start-end`。 |
| `feature` |字符串|以下一项或多项：`gene`、`transcript`、`cds`、`exon`、`repeat`、`simple`、`misc`、`variation`、`somatic_variation`、`structural_variation`、 `regulatory`、`motif`、`chipseq`、`constrained`。可以重复多个参数。 |

* *示例 -- 获取某个区域内的所有基因：**
```
https://rest.ensembl.org/overlap/region/homo_sapiens/17:7660000-7690000?feature=gene&content-type=application/json
```

 * *示例 -- 获取调控特征：**
```
https://rest.ensembl.org/overlap/region/homo_sapiens/17:7660000-7690000?feature=regulatory&content-type=application/json
```

- --

### 9. 交叉引用（外部引用）

```
GET /xrefs/id/{id}?content-type=application/json
```

* *示例：**
```
https://rest.ensembl.org/xrefs/id/ENSG00000141510?content-type=application/json
```

返回外部数据库的链接（HGNC、UniProt、NCBI Gene、RefSeq、等）。

* *响应：**
```json
[
  {
    "primary_id": "11998",
    "display_id": "TP53",
    "dbname": "HGNC",
    "db_display_name": "HGNC Symbol"
  },
  {
    "primary_id": "P04637",
    "display_id": "P53_HUMAN",
    "dbname": "Uniprot/SWISSPROT"
  },
  {
    "primary_id": "7157",
    "display_id": "TP53",
    "dbname": "EntrezGene"
  }
]
```

* *Xrefs符号：**
```
GET /xrefs/symbol/{species}/{symbol}?content-type=application/json
```

* *示例：**
```
https://rest.ensembl.org/xrefs/symbol/homo_sapiens/TP53?content-type=application/json
```

- --

### 10.比较基因组学——同源性

```
GET /homology/id/{id}?content-type=application/json
```

|参数|类型 |描述 |
|--------------|--------|------------|
| `id` |字符串|整体基因 ID。 |
| `type` |字符串| `orthologues`、`paralogues`、`projections`、`all`。 |
| `target_species` |字符串|过滤到特定物种（例如，`mus_musculus`）。 |
| `target_taxon` |整数 |过滤至 NCBI 分类单元 ID。 |
| `sequence` |字符串| `none`、`cdna`、`protein`。包括比对序列。 |

* *示例 -- 获取人类 TP53 的小鼠直系同源物：**
```
https://rest.ensembl.org/homology/id/ENSG00000141510?type=orthologues&target_species=mus_musculus&content-type=application/json
```

* *响应：**
```json
{
  "data": [
    {
      "id": "ENSG00000141510",
      "homologies": [
        {
          "type": "ortholog_one2one",
          "target": {
            "id": "ENSMUSG00000059552",
            "species": "mus_musculus",
            "protein_id": "ENSMUSP00000073359",
            "perc_id": 77.8,
            "perc_pos": 86.0
          },
          "source": {
            "id": "ENSG00000141510",
            "species": "homo_sapiens",
            "protein_id": "ENSP00000269305"
          },
          "method_link_type": "ENSEMBL_ORTHOLOGUES",
          "dn_ds": 0.15
        }
      ]
    }
  ]
}
```

* *同源性符号：**
```
GET /homology/symbol/{species}/{symbol}?content-type=application/json
```

* *示例：**
```
https://rest.ensembl.org/homology/symbol/homo_sapiens/TP53?type=orthologues&target_species=mus_musculus&content-type=application/json
```

- --

### 11. 监管功能

```
GET /regulatory/species/{species}/id/{id}?content-type=application/json
```

* *示例：**
```
https://rest.ensembl.org/regulatory/species/homo_sapiens/id/ENSR00000000163?content-type=application/json
```

- --

### 12. 物种信息

```
GET /info/species?content-type=application/json
```

返回所有可用的物种并进行组装info.

- --

### 13. 组装信息

```
GET /info/assembly/{species}?content-type=application/json
```

* *示例：**
```
https://rest.ensembl.org/info/assembly/homo_sapiens?content-type=application/json
```

返回染色体名称、长度、程序集名称（GRCh38）、坐标系等。

- --

### 14. 表型基因

```
GET /phenotype/gene/{species}/{gene}?content-type=application/json
```

* *示例：**
```
https://rest.ensembl.org/phenotype/gene/homo_sapiens/TP53?content-type=application/json
```

- --

### 15. LD（连锁不平衡）

```
GET /ld/{species}/pairwise/{rsid1}/{rsid2}?population_name={pop}&content-type=application/json
```

* *示例：**
```
https://rest.ensembl.org/ld/homo_sapiens/pairwise/rs699/rs4762?population_name=1000GENOMES:phase_3:CEU&content-type=application/json
```

- --

## 常见物种名称

|物种 | API名称 |
|---------|----------|
|人类 | `homo_sapiens` |
|鼠标| `mus_musculus` |
|老鼠 | `rattus_norvegicus` |
|斑马鱼 | `danio_rerio` |
|果蝇| `drosophila_melanogaster` |
|鸡 | `gallus_gallus` |
|狗 | `canis_lupus_familiaris` |
|猪| `sus_scrofa` |

## 速率限制

- **一般用户每秒 15 个请求**（无 API 密钥）。
- 如果您注册 API 密钥（可选），可能会提供更高的限制。
- 超出限制的请求会通过 `Retry-After` 接收 HTTP 429 header.
- 批量端点 (POST)计数为单个请求 - 使用它们来减少调用计数。
- `/lookup/id` 的每批 POST 最多 1000 个 ID。
- VEP 的每批 POST 最多 200 个变体。
- 返回速率限制标头： `X-RateLimit-Limit`、`X-RateLimit-Remaining`、`X-RateLimit-Reset`.

## 错误格式

```json
{
  "error": "ID 'ENSG999' not found"
}
```

HTTP 400 表示错误请求，404 表示未找到，429 表示速率限制，503 表示服务不可用。

## 提示

- 始终将`?content-type=application/json`附加到GET请求（或设置Accept标头）——默认为XML/HTML。
- 如果需要hg19坐标，请使用GRCh37基本URL（`grch37.rest.ensembl.org`）。
- `/lookup/symbol`端点是从基因符号到Ensembl的最快方式ID.
- 对于VEP，HGVS端点对于单一变体最方便；区域 POST 端点最适合批处理。
- 将 `/xrefs/id` 与基因 ID 组合以交叉引用 UniProt、NCBI Gene、HGNC 和其他数据库。
