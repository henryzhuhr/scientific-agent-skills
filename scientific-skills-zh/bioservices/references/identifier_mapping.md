# BioServices：标识符映射指南

本文档提供了有关使用BioServices.

## 目录

1在不同生物数据库之间转换标识符的全面信息。 [概述](#overview)
2. [UniProt 映射服务](#uniprot-mapping-service)
3. [UniChem 化合物图谱](#unichem-compound-mapping)
4. [KEGG 标识符转换](#kegg-identifier-conversions)
5. [常见映射模式](#common-mapping-patterns)
6. [疑难解答](#troubleshooting)

- --

## 概述

生物数据库使用不同的标识符系统。交叉引用需要这些系统之间的映射。 BioServices提供了多种方式：

1. **UniProt Mapping**：全面的蛋白质/基因 ID 转换
2. **UniChem**：化合物 ID 映射 
3. **KEGG**：条目
4中的内置交叉引用。 **PICR**：蛋白质标识符交叉引用服务

- --

## UniProt 映射服务

UniProt 映射服务是最全面的蛋白质和基因标识符转换工具。

### 基本用法

```python
from bioservices import UniProt

u = UniProt()

# Map single ID
result = u.mapping(
    fr="UniProtKB_AC-ID",    # Source database
    to="KEGG",                # Target database
    query="P43403"            # Identifier to convert
)

print(result)
# Output: {'P43403': ['hsa:7535']}
```

### 批量映射

```python
# Map multiple IDs (comma-separated)
ids = ["P43403", "P04637", "P53779"]
result = u.mapping(
    fr="UniProtKB_AC-ID",
    to="KEGG",
    query=",".join(ids)
)

for uniprot_id, kegg_ids in result.items():
    print(f"{uniprot_id} → {kegg_ids}")
```

### 支持的数据库对

UniProt 支持 100 多个数据库对之间的映射。关键包括：

#### 蛋白质/基因数据库

|源格式|代码|目标格式|代码|
|----------------|-----|---------------|-----|
| UniProtKB AC/ID | `UniProtKB_AC-ID` |凯格 | `KEGG` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` |合奏 | `Ensembl` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` |整体蛋白质| `Ensembl_Protein` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` |合奏成绩单| `Ensembl_Transcript` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | RefSeq 蛋白质 | `RefSeq_Protein` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | RefSeq 核苷酸 | `RefSeq_Nucleotide` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | GeneID (Entrez) | `GeneID` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | HGNC | `HGNC` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` |华大智造 | `MGI` |
|凯格 | `KEGG` | UniProtKB | `UniProtKB` |
|合奏 | `Ensembl` | UniProtKB | `UniProtKB` |
|基因ID | `GeneID` | UniProtKB | `UniProtKB` |

#### 结构数据库

|来源 |代码|目标|代码|
|--------|-----|--------|-----|
| UniProtKB AC/ID | `UniProtKB_AC-ID` | PDB| `PDB` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` |普法姆| `Pfam` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` | InterPro | `InterPro` |
| PDB| `PDB` | UniProtKB | `UniProtKB` |

#### 表达与蛋白质组学

|来源 |代码|目标|代码|
|--------|-----|--------|-----|
| UniProtKB AC/ID | `UniProtKB_AC-ID` |骄傲| `PRIDE` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` |蛋白质组学数据库 | `ProteomicsDB` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` |帕克斯数据库 | `PaxDb` |

#### 特定生物体

|来源 |代码|目标|代码|
|--------|-----|--------|-----|
| UniProtKB AC/ID | `UniProtKB_AC-ID` |飞行基地 | `FlyBase` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` |蠕虫基地 | `WormBase` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` |新元 | `SGD` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` |泽芬| `ZFIN` |

#### 其他有用的映射

|来源 |代码|目标|代码|
|--------|-----|--------|-----|
| UniProtKB AC/ID | `UniProtKB_AC-ID` |去 | `GO` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` |反应组 | `Reactome` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` |字符串 | `STRING` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` |生物网格| `BioGRID` |
| UniProtKB AC/ID | `UniProtKB_AC-ID` |大都会建筑事务所 | `OMA` |

### 数据库代码完整列表

要获取完整的最新列表：

```python
from bioservices import UniProt

u = UniProt()

# This information is in the UniProt REST API documentation
# Common patterns:
# - Source databases typically end in source database name
# - UniProtKB uses "UniProtKB_AC-ID" or "UniProtKB"
# - Most other databases use their standard abbreviation
```

### 通用数据库代码参考

* *基因/蛋白质标识符：**
- `UniProtKB_AC-ID`：UniProt 登录号/ID
- `UniProtKB`：UniProt 登录号
- `KEGG`：KEGG 基因 ID（例如 hsa：7535）
- `GeneID`：NCBI 基因 (Entrez) IDs
- `Ensembl`：Ensembl 基因 IDs
- `Ensembl_Protein`：Ensembl 蛋白 IDs
- `Ensembl_Transcript`：Ensembl 转录本 IDs
- `RefSeq_Protein`：RefSeq 蛋白 IDs (NP_)
- `RefSeq_Nucleotide`：RefSeq 核苷酸 ID (NM_)

* *基因命名法：**
- `HGNC`：人类基因命名法委员会
- `MGI`：小鼠基因组信息学
- `RGD`：大鼠基因组数据库
- `SGD`：酵母菌基因组数据库
- `FlyBase`：果蝇数据库
- `WormBase`：线虫数据库
- `ZFIN`：斑马鱼数据库

* *结构：**
- `PDB`：蛋白质数据库
- `Pfam`：蛋白质家族
- `InterPro`：蛋白质结构域
- `SUPFAM`：超家族
- `PROSITE`：蛋白质基序

* *途径和网络：**
- `Reactome`：反应组途径
- `BioCyc`：BioCyc途径
- `PathwayCommons`：共用途径
- `STRING`：蛋白质-蛋白质网络
- `BioGRID`：交互数据库

### 映射示例

#### UniProt → KEGG

```python
from bioservices import UniProt

u = UniProt()

# Single mapping
result = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query="P43403")
print(result)  # {'P43403': ['hsa:7535']}
```

#### KEGG → UniProt

```python
# Reverse mapping
result = u.mapping(fr="KEGG", to="UniProtKB", query="hsa:7535")
print(result)  # {'hsa:7535': ['P43403']}
```

#### UniProt → Ensembl

```python
# To Ensembl gene IDs
result = u.mapping(fr="UniProtKB_AC-ID", to="Ensembl", query="P43403")
print(result)  # {'P43403': ['ENSG00000115085']}

# To Ensembl protein IDs
result = u.mapping(fr="UniProtKB_AC-ID", to="Ensembl_Protein", query="P43403")
print(result)  # {'P43403': ['ENSP00000381359']}
```

#### UniProt → PDB

```python
# Find 3D structures
result = u.mapping(fr="UniProtKB_AC-ID", to="PDB", query="P04637")
print(result)  # {'P04637': ['1A1U', '1AIE', '1C26', ...]}
```

#### UniProt → RefSeq

```python
# Get RefSeq protein IDs
result = u.mapping(fr="UniProtKB_AC-ID", to="RefSeq_Protein", query="P43403")
print(result)  # {'P43403': ['NP_001070.2']}
```

#### 基因名称 → UniProt（通过搜索，然后映射）

```python
# First search for gene
search_result = u.search("gene:ZAP70 AND organism:9606", frmt="tab", columns="id")
lines = search_result.strip().split("\n")
if len(lines) > 1:
    uniprot_id = lines[1].split("\t")[0]

    # Then map to other databases
    kegg_id = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query=uniprot_id)
    print(kegg_id)
```

- --

## UniChem 化合物映射

UniChem 专门从事跨数据库映射化学化合物标识符。

### 源数据库 ID

|来源ID |数据库|
|---------|----------|
| 1 | ChEMBL |
| 2 |药物银行|
| 3 | PDB |
| 4 | IUPHAR/BPS 药理学指南 |
| 5 | PubChem |
| 6 |凯格|
| 7 |车比 |
| 8 | NIH 临床收藏|
| 14 | 14 FDA/SRS |
| 22 | 22 PubChem |

### 基本用法

```python
from bioservices import UniChem

u = UniChem()

# Get ChEMBL ID from KEGG compound ID
chembl_id = u.get_compound_id_from_kegg("C11222")
print(chembl_id)  # CHEMBL278315
```

### 所有化合物 ID

```python
# Get all identifiers for a compound
# src_compound_id: compound ID, src_id: source database ID
all_ids = u.get_all_compound_ids("CHEMBL278315", src_id=1)  # 1 = ChEMBL

for mapping in all_ids:
    src_name = mapping['src_name']
    src_compound_id = mapping['src_compound_id']
    print(f"{src_name}: {src_compound_id}")
```

### 特定数据库转换

```python
# Convert between specific databases
# from_src_id=6 (KEGG), to_src_id=1 (ChEMBL)
result = u.get_src_compound_ids("C11222", from_src_id=6, to_src_id=1)
print(result)
```

### 常见化合物映射

#### KEGG → ChEMBL

```python
u = UniChem()
chembl_id = u.get_compound_id_from_kegg("C00031")  # D-Glucose
print(f"ChEMBL: {chembl_id}")
```

#### ChEMBL → PubChem

```python
result = u.get_src_compound_ids("CHEMBL278315", from_src_id=1, to_src_id=22)
if result:
    pubchem_id = result[0]['src_compound_id']
    print(f"PubChem: {pubchem_id}")
```

#### ChEBI → DrugBank

```python
result = u.get_src_compound_ids("5292", from_src_id=7, to_src_id=2)
if result:
    drugbank_id = result[0]['src_compound_id']
    print(f"DrugBank: {drugbank_id}")
```

- --

## KEGG 标识符转换

KEGG 条目包含可以通过解析提取的交叉引用。

### 从 KEGG 提取数据库链接条目

```python
from bioservices import KEGG

k = KEGG()

# Get compound entry
entry = k.get("cpd:C11222")

# Parse for specific database
chebi_id = None
uniprot_ids = []

for line in entry.split("\n"):
    if "ChEBI:" in line:
        # Extract ChEBI ID
        parts = line.split("ChEBI:")
        if len(parts) > 1:
            chebi_id = parts[1].strip().split()[0]

# For genes/proteins
gene_entry = k.get("hsa:7535")
for line in gene_entry.split("\n"):
    if line.startswith("            "):  # Database links section
        if "UniProt:" in line:
            parts = line.split("UniProt:")
            if len(parts) > 1:
                uniprot_id = parts[1].strip()
                uniprot_ids.append(uniprot_id)
```

### KEGG 基因 ID 组件

KEGG 基因 ID 的格式为 `organism:gene_id`:

```python
kegg_id = "hsa:7535"
organism, gene_id = kegg_id.split(":")

print(f"Organism: {organism}")  # hsa (human)
print(f"Gene ID: {gene_id}")    # 7535
```

### KEGG 路径基因

```python
k = KEGG()

# Get pathway entry
pathway = k.get("path:hsa04660")

# Parse for gene list
genes = []
in_gene_section = False

for line in pathway.split("\n"):
    if line.startswith("GENE"):
        in_gene_section = True

    if in_gene_section:
        if line.startswith(" " * 12):  # Gene line
            parts = line.strip().split()
            if parts:
                gene_id = parts[0]
                genes.append(f"hsa:{gene_id}")
        elif not line.startswith(" "):
            break

print(f"Found {len(genes)} genes")
```

- --

## 常见映射模式

### 模式1：基因符号→多个数据库ID

```python
from bioservices import UniProt

def gene_symbol_to_ids(gene_symbol, organism="9606"):
    """Convert gene symbol to multiple database IDs."""
    u = UniProt()

    # Search for gene
    query = f"gene:{gene_symbol} AND organism:{organism}"
    result = u.search(query, frmt="tab", columns="id")

    lines = result.strip().split("\n")
    if len(lines) < 2:
        return None

    uniprot_id = lines[1].split("\t")[0]

    # Map to multiple databases
    ids = {
        'uniprot': uniprot_id,
        'kegg': u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query=uniprot_id),
        'ensembl': u.mapping(fr="UniProtKB_AC-ID", to="Ensembl", query=uniprot_id),
        'refseq': u.mapping(fr="UniProtKB_AC-ID", to="RefSeq_Protein", query=uniprot_id),
        'pdb': u.mapping(fr="UniProtKB_AC-ID", to="PDB", query=uniprot_id)
    }

    return ids

# Usage
ids = gene_symbol_to_ids("ZAP70")
print(ids)
```

### 模式2：化合物名称→所有数据库IDs

```python
from bioservices import KEGG, UniChem, ChEBI

def compound_name_to_ids(compound_name):
    """Search compound and get all database IDs."""
    k = KEGG()

    # Search KEGG
    results = k.find("compound", compound_name)
    if not results:
        return None

    # Extract KEGG ID
    kegg_id = results.strip().split("\n")[0].split("\t")[0].replace("cpd:", "")

    # Get KEGG entry for ChEBI
    entry = k.get(f"cpd:{kegg_id}")
    chebi_id = None
    for line in entry.split("\n"):
        if "ChEBI:" in line:
            parts = line.split("ChEBI:")
            if len(parts) > 1:
                chebi_id = parts[1].strip().split()[0]
                break

    # Get ChEMBL from UniChem
    u = UniChem()
    try:
        chembl_id = u.get_compound_id_from_kegg(kegg_id)
    except:
        chembl_id = None

    return {
        'kegg': kegg_id,
        'chebi': chebi_id,
        'chembl': chembl_id
    }

# Usage
ids = compound_name_to_ids("Geldanamycin")
print(ids)
```

### 模式 3：带错误处理的批量 ID 转换

```python
from bioservices import UniProt

def safe_batch_mapping(ids, from_db, to_db, chunk_size=100):
    """Safely map IDs with error handling and chunking."""
    u = UniProt()
    all_results = {}

    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i+chunk_size]
        query = ",".join(chunk)

        try:
            results = u.mapping(fr=from_db, to=to_db, query=query)
            all_results.update(results)
            print(f"✓ Processed {min(i+chunk_size, len(ids))}/{len(ids)}")

        except Exception as e:
            print(f"✗ Error at chunk {i}: {e}")

            # Try individual IDs in failed chunk
            for single_id in chunk:
                try:
                    result = u.mapping(fr=from_db, to=to_db, query=single_id)
                    all_results.update(result)
                except:
                    all_results[single_id] = None

    return all_results

# Usage
uniprot_ids = ["P43403", "P04637", "P53779", "INVALID123"]
mapping = safe_batch_mapping(uniprot_ids, "UniProtKB_AC-ID", "KEGG")
```

### 模式 4：多跳映射

有时需要通过中间映射数据库：

```python
from bioservices import UniProt

def multi_hop_mapping(gene_symbol, organism="9606"):
    """Gene symbol → UniProt → KEGG → Pathways."""
    u = UniProt()
    k = KEGG()

    # Step 1: Gene symbol → UniProt
    query = f"gene:{gene_symbol} AND organism:{organism}"
    result = u.search(query, frmt="tab", columns="id")

    lines = result.strip().split("\n")
    if len(lines) < 2:
        return None

    uniprot_id = lines[1].split("\t")[0]

    # Step 2: UniProt → KEGG
    kegg_mapping = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query=uniprot_id)
    if not kegg_mapping or uniprot_id not in kegg_mapping:
        return None

    kegg_id = kegg_mapping[uniprot_id][0]

    # Step 3: KEGG → Pathways
    organism_code, gene_id = kegg_id.split(":")
    pathways = k.get_pathway_by_gene(gene_id, organism_code)

    return {
        'gene': gene_symbol,
        'uniprot': uniprot_id,
        'kegg': kegg_id,
        'pathways': pathways
    }

# Usage
result = multi_hop_mapping("TP53")
print(result)
```

- --

## 故障排除

### 问题1：未找到映射

* *症状：**映射返回空或 None

* *解决方案：**
1. 验证源 ID 是否存在于源数据库
2 中。检查数据库代码拼写
3. 尝试反向映射
4. 某些ID可能在所有数据库中都没有映射

```python
result = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query="P43403")

if not result or 'P43403' not in result:
    print("No mapping found. Try:")
    print("1. Verify ID exists: u.search('P43403')")
    print("2. Check if protein has KEGG annotation")
```

### 问题2：批量ID太多

* *症状：**批量映射失败或超时

* *解决方案：**分割成更小的chunks

```python
def chunked_mapping(ids, from_db, to_db, chunk_size=50):
    all_results = {}

    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i+chunk_size]
        result = u.mapping(fr=from_db, to=to_db, query=",".join(chunk))
        all_results.update(result)

    return all_results
```

### 问题 3：多个目标 ID

* *症状：** 一个源 ID 映射到多个目标 ID

* *解决方案：** 处理为列表

```python
result = u.mapping(fr="UniProtKB_AC-ID", to="PDB", query="P04637")
# Result: {'P04637': ['1A1U', '1AIE', '1C26', ...]}

pdb_ids = result['P04637']
print(f"Found {len(pdb_ids)} PDB structures")

for pdb_id in pdb_ids:
    print(f"  {pdb_id}")
```

### 问题 4：有机体歧义

* *症状：** 基因符号映射到多个生物体

* *解决方案：** 始终在搜索中指定生物体

```python
# Bad: Ambiguous
result = u.search("gene:TP53")  # Many organisms have TP53

# Good: Specific
result = u.search("gene:TP53 AND organism:9606")  # Human only
```

### 问题 5：已弃用的 ID

* *症状：** 旧数据库 ID 不支持地图

* *解决方案：**先更新到当前ID

```python
# Check if ID is current
entry = u.retrieve("P43403", frmt="txt")

# Look for secondary accessions
for line in entry.split("\n"):
    if line.startswith("AC"):
        print(line)  # Shows primary and secondary accessions
```

- --

## 最佳实践

1. **在批处理之前始终验证输入**
2. **优雅地处理无/空结果**
3. **对大型 ID 列表使用分块**（每个块 50-100）
4. **重复查询的缓存结果**
5. **尽可能指定生物体**以避免歧义
6. **记录批处理中的失败**以便稍后重试
7. **在大批量之间添加延迟**以遵守 API 限制

```python
import time

def polite_batch_mapping(ids, from_db, to_db):
    """Batch mapping with rate limiting."""
    results = {}

    for i in range(0, len(ids), 50):
        chunk = ids[i:i+50]
        result = u.mapping(fr=from_db, to=to_db, query=",".join(chunk))
        results.update(result)

        time.sleep(0.5)  # Be nice to the API

    return results
```

- --

有关完整的工作示例，请参阅：
- `scripts/batch_id_converter.py`：命令行批量转换工具
- `workflow_patterns.md`：集成到更大的批量中工作流程
