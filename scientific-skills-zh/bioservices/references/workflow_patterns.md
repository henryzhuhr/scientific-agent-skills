# BioServices：常见工作流程模式

本文档描述了使用 BioServices.

## 目录

1 常见生物信息学任务的详细多步骤工作流程。 [完整的蛋白质分析管道](#complete-蛋白质分析-管道)
2. [路径发现和网络分析](#pathway-discovery-and-network-analysis)
3. [复合多数据库搜索](#compound-multi-database-search)
4. [批量标识符转换](#batch-identifier-conversion)
5. [基因功能注释](#gene-function-annotation)
6. [蛋白质相互作用网络构建](# Protein-interaction-network-construction)
7. [多生物体比较分析](#multi-organism-comparative-analysis)

- --

## 完整的蛋白质分析流程

* *目标：**给定蛋白质名称，检索序列，查找同源物，识别途径，并发现相互作用。

* *示例：**分析人类ZAP70蛋白

### 步骤 1：UniProt 搜索和标识符检索

```python
from bioservices import UniProt

u = UniProt(verbose=False)

# Search for protein by name
query = "ZAP70_HUMAN"
results = u.search(query, frmt="tab", columns="id,genes,organism,length")

# Parse results
lines = results.strip().split("\n")
if len(lines) > 1:
    header = lines[0]
    data = lines[1].split("\t")
    uniprot_id = data[0]  # e.g., P43403
    gene_names = data[1]   # e.g., ZAP70

print(f"UniProt ID: {uniprot_id}")
print(f"Gene names: {gene_names}")
```

* *输出：**
- UniProt 登录号：P43403
- 基因名称：ZAP70

### 步骤 2：序列检索

```python
# Retrieve FASTA sequence
sequence = u.retrieve(uniprot_id, frmt="fasta")
print(sequence)

# Extract just the sequence string (remove header)
seq_lines = sequence.split("\n")
sequence_only = "".join(seq_lines[1:])  # Skip FASTA header
```

* *输出：** FASTA 格式的完整蛋白质序列

### 步骤3：BLAST 相似性搜索

```python
from bioservices import NCBIblast
import time

s = NCBIblast(verbose=False)

# Submit BLAST job
jobid = s.run(
    program="blastp",
    sequence=sequence_only,
    stype="protein",
    database="uniprotkb",
    email="your.email@example.com"
)

print(f"BLAST Job ID: {jobid}")

# Wait for completion
while True:
    status = s.getStatus(jobid)
    print(f"Status: {status}")
    if status == "FINISHED":
        break
    elif status == "ERROR":
        print("BLAST job failed")
        break
    time.sleep(5)

# Retrieve results
if status == "FINISHED":
    blast_results = s.getResult(jobid, "out")
    print(blast_results[:500])  # Print first 500 characters
```

* *输出：** 显示相似蛋白质的BLAST 比对结果

### 步骤4: KEGG 通路发现

```python
from bioservices import KEGG

k = KEGG()

# Get KEGG gene ID from UniProt mapping
kegg_mapping = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query=uniprot_id)
print(f"KEGG mapping: {kegg_mapping}")

# Extract KEGG gene ID (e.g., hsa:7535)
if kegg_mapping:
    kegg_gene_id = kegg_mapping[uniprot_id][0] if uniprot_id in kegg_mapping else None

    if kegg_gene_id:
        # Find pathways containing this gene
        organism = kegg_gene_id.split(":")[0]  # e.g., "hsa"
        gene_id = kegg_gene_id.split(":")[1]   # e.g., "7535"

        pathways = k.get_pathway_by_gene(gene_id, organism)
        print(f"Found {len(pathways)} pathways:")

        # Get pathway names
        for pathway_id in pathways:
            pathway_info = k.get(pathway_id)
            # Parse NAME line
            for line in pathway_info.split("\n"):
                if line.startswith("NAME"):
                    pathway_name = line.replace("NAME", "").strip()
                    print(f"  {pathway_id}: {pathway_name}")
                    break
```

* *输出:**
- 路径:hsa04064 - NF-kappa B 信号通路
- 路径:hsa04650 - 自然杀伤细胞介导的细胞毒性
- 路径:hsa04660 - T 细胞受体信号通路
- 路径：hsa04662 - B 细胞受体信号通路

### 步骤 5：蛋白质-蛋白质相互作用

```python
from bioservices import PSICQUIC

p = PSICQUIC()

# Query MINT database for human (taxid:9606) interactions
query = f"ZAP70 AND species:9606"
interactions = p.query("mint", query)

# Parse PSI-MI TAB format results
if interactions:
    interaction_lines = interactions.strip().split("\n")
    print(f"Found {len(interaction_lines)} interactions")

    # Print first few interactions
    for line in interaction_lines[:5]:
        fields = line.split("\t")
        protein_a = fields[0]
        protein_b = fields[1]
        interaction_type = fields[11]
        print(f"  {protein_a} - {protein_b}: {interaction_type}")
```

 * *输出：** 与 ZAP70

 相互作用的蛋白质列表### 步骤 6：基因本体注释

```python
from bioservices import QuickGO

g = QuickGO()

# Get GO annotations for protein
annotations = g.Annotation(protein=uniprot_id, format="tsv")

if annotations:
    # Parse TSV results
    lines = annotations.strip().split("\n")
    print(f"Found {len(lines)-1} GO annotations")

    # Display first few annotations
    for line in lines[1:6]:  # Skip header
        fields = line.split("\t")
        go_id = fields[6]
        go_term = fields[7]
        go_aspect = fields[8]
        print(f"  {go_id}: {go_term} [{go_aspect}]")
```

* *输出：** 注释ZAP70函数、过程和位置的GO术语

### 完整管道摘要

* *输入：**蛋白质名称（例如“ZAP70_HUMAN”）

  * *输出：**
1. UniProt 登录号和基因名称
2. 蛋白质序列(FASTA)
3. 相似蛋白（BLAST结果）
4. 生物途径（KEGG）
5. 互动伙伴（PSICQUIC）
6. 功能注释（GO 术语）

* *脚本：** `scripts/protein_analysis_workflow.py` 自动化整个流程。

- --

## 通路发现和网络分析

* *目标：** 分析生物体的所有通路并提取蛋白质相互作用网络。

* *示例：** 人类 (hsa)通路分析

### 步骤 1：获取生物体的所有路径

```python
from bioservices import KEGG

k = KEGG()
k.organism = "hsa"

# Get all pathway IDs
pathway_ids = k.pathwayIds
print(f"Found {len(pathway_ids)} pathways for {k.organism}")

# Display first few
for pid in pathway_ids[:10]:
    print(f"  {pid}")
```

* *输出：** ~300 条人类路径列表

### 步骤 2：解析路径相互作用

```python
# Analyze specific pathway
pathway_id = "hsa04660"  # T cell receptor signaling

# Get KGML data
kgml_data = k.parse_kgml_pathway(pathway_id)

# Extract entries (genes/proteins)
entries = kgml_data['entries']
print(f"Pathway contains {len(entries)} entries")

# Extract relations (interactions)
relations = kgml_data['relations']
print(f"Found {len(relations)} relations")

# Analyze relation types
relation_types = {}
for rel in relations:
    rel_type = rel.get('name', 'unknown')
    relation_types[rel_type] = relation_types.get(rel_type, 0) + 1

print("\nRelation type distribution:")
for rel_type, count in sorted(relation_types.items()):
    print(f"  {rel_type}: {count}")
```

* *输出：**
- 条目计数（途径中的基因/蛋白质）
- 关系计数（相互作用）
- 相互作用类型的分布（激活、抑制、结合等）

### 步骤3：提取蛋白质-蛋白质相互作用

```python
# Filter for specific interaction types
pprel_interactions = [
    rel for rel in relations
    if rel.get('link') == 'PPrel'  # Protein-protein relation
]

print(f"Found {len(pprel_interactions)} protein-protein interactions")

# Extract interaction details
for rel in pprel_interactions[:10]:
    entry1 = rel['entry1']
    entry2 = rel['entry2']
    interaction_type = rel.get('name', 'unknown')

    print(f"  {entry1} -> {entry2}: {interaction_type}")
```

* *输出：** 与类型的定向蛋白质-蛋白质相互作用

### 步骤 4：转换为网络格式 (SIF)

```python
# Get Simple Interaction Format (filters for key interactions)
sif_data = k.pathway2sif(pathway_id)

# SIF format: source, interaction_type, target
print("\nSimple Interaction Format:")
for interaction in sif_data[:10]:
    print(f"  {interaction}")
```

* *输出：** 适用于 Cytoscape 或的网络边缘NetworkX

### 步骤 5：所有路径的批量分析

```python
import pandas as pd

# Analyze all pathways (this takes time!)
all_results = []

for pathway_id in pathway_ids[:50]:  # Limit for example
    try:
        kgml = k.parse_kgml_pathway(pathway_id)

        result = {
            'pathway_id': pathway_id,
            'num_entries': len(kgml.get('entries', [])),
            'num_relations': len(kgml.get('relations', []))
        }

        all_results.append(result)

    except Exception as e:
        print(f"Error parsing {pathway_id}: {e}")

# Create DataFrame
df = pd.DataFrame(all_results)
print(df.describe())

# Find largest pathways
print("\nLargest pathways:")
print(df.nlargest(10, 'num_entries')[['pathway_id', 'num_entries', 'num_relations']])
```

* *输出：** 路径大小和相互作用密度的统计摘要

* *脚本：** `scripts/pathway_analysis.py` 通过导出实现此工作流程options.

- --

## 化合物多数据库搜索

* *目标：** 按名称搜索化合物并检索 KEGG、ChEBI 和 ChEMBL 中的标识符。

* *示例：** 格尔德霉素（抗生素）

### 步骤 1：搜索 KEGG 化合物数据库

```python
from bioservices import KEGG

k = KEGG()

# Search by compound name
compound_name = "Geldanamycin"
results = k.find("compound", compound_name)

print(f"KEGG search results for '{compound_name}':")
print(results)

# Extract compound ID
if results:
    lines = results.strip().split("\n")
    if lines:
        kegg_id = lines[0].split("\t")[0]  # e.g., cpd:C11222
        kegg_id_clean = kegg_id.replace("cpd:", "")  # C11222
        print(f"\nKEGG Compound ID: {kegg_id_clean}")
```

* *输出：** KEGG ID（例如，C11222）

### 步骤2：通过数据库链接获取KEGG条目

```python
# Retrieve compound entry
compound_entry = k.get(kegg_id)

# Parse entry for database links
chebi_id = None
for line in compound_entry.split("\n"):
    if "ChEBI:" in line:
        # Extract ChEBI ID
        parts = line.split("ChEBI:")
        if len(parts) > 1:
            chebi_id = parts[1].strip().split()[0]
            print(f"ChEBI ID: {chebi_id}")
            break

# Display entry snippet
print("\nKEGG Entry (first 500 chars):")
print(compound_entry[:500])
```

* *输出：** ChEBI ID（例如， 5292)和化合物信息

### 步骤 3：通过 UniChem

```python
from bioservices import UniChem

u = UniChem()

# Convert KEGG → ChEMBL
try:
    chembl_id = u.get_compound_id_from_kegg(kegg_id_clean)
    print(f"ChEMBL ID: {chembl_id}")
except Exception as e:
    print(f"UniChem lookup failed: {e}")
    chembl_id = None
```

 * *输出：** ChEMBL ID（例如 CHEMBL278315）

 交叉引用 ChEMBL### 步骤 4：检索详细信息

```python
# Get ChEBI information
if chebi_id:
    from bioservices import ChEBI
    c = ChEBI()

    try:
        chebi_entity = c.getCompleteEntity(f"CHEBI:{chebi_id}")
        print(f"\nChEBI Formula: {chebi_entity.Formulae}")
        print(f"ChEBI Name: {chebi_entity.chebiAsciiName}")
    except Exception as e:
        print(f"ChEBI lookup failed: {e}")

# Get ChEMBL information
if chembl_id:
    from bioservices import ChEMBL
    chembl = ChEMBL()

    try:
        chembl_compound = chembl.get_compound_by_chemblId(chembl_id)
        print(f"\nChEMBL Molecular Weight: {chembl_compound['molecule_properties']['full_mwt']}")
        print(f"ChEMBL SMILES: {chembl_compound['molecule_structures']['canonical_smiles']}")
    except Exception as e:
        print(f"ChEMBL lookup failed: {e}")
```

* *输出：** 来自多个数据库的化学性质

### 完整化合物工作流程摘要

* *输入：** 化合物名称（例如“Geldanamycin”）

* *输出：**
- KEGG ID：C11222
- ChEBI ID：5292
- ChEMBL ID：CHEMBL278315
- 化学式
- 分子量
- SMILES结构

* *脚本：**`scripts/compound_cross_reference.py`自动执行此操作工作流程.

- --

## 批量标识符转换

* *目标：**高效地在数据库之间转换多个标识符。

### 批量UniProt → KEGG Mapping

```python
from bioservices import UniProt

u = UniProt()

# List of UniProt IDs
uniprot_ids = ["P43403", "P04637", "P53779", "Q9Y6K9"]

# Batch mapping (comma-separated)
query_string = ",".join(uniprot_ids)
results = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query=query_string)

print("UniProt → KEGG mapping:")
for uniprot_id, kegg_ids in results.items():
    print(f"  {uniprot_id} → {kegg_ids}")
```

* *输出：**将每个UniProt ID映射到KEGG基因的字典IDs

### 批量文件处理

```python
import csv

# Read identifiers from file
def read_ids_from_file(filename):
    with open(filename, 'r') as f:
        ids = [line.strip() for line in f if line.strip()]
    return ids

# Process in chunks (API limits)
def batch_convert(ids, from_db, to_db, chunk_size=100):
    u = UniProt()
    all_results = {}

    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i+chunk_size]
        query = ",".join(chunk)

        try:
            results = u.mapping(fr=from_db, to=to_db, query=query)
            all_results.update(results)
            print(f"Processed {min(i+chunk_size, len(ids))}/{len(ids)}")
        except Exception as e:
            print(f"Error processing chunk {i}: {e}")

    return all_results

# Write results to CSV
def write_mapping_to_csv(mapping, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Source_ID', 'Target_IDs'])

        for source_id, target_ids in mapping.items():
            target_str = ";".join(target_ids) if target_ids else "No mapping"
            writer.writerow([source_id, target_str])

# Example usage
input_ids = read_ids_from_file("uniprot_ids.txt")
mapping = batch_convert(input_ids, "UniProtKB_AC-ID", "KEGG", chunk_size=50)
write_mapping_to_csv(mapping, "uniprot_to_kegg_mapping.csv")
```

* *脚本：** `scripts/batch_id_converter.py`提供命令行批量转换。

- --

## 基因功能注释

* *目标：**检索一个基因的全面功能信息基因.

### 工作流程

```python
from bioservices import UniProt, KEGG, QuickGO

# Gene of interest
gene_symbol = "TP53"

# 1. Find UniProt entry
u = UniProt()
search_results = u.search(f"gene:{gene_symbol} AND organism:9606",
                          frmt="tab",
                          columns="id,genes,protein names")

# Extract UniProt ID
lines = search_results.strip().split("\n")
if len(lines) > 1:
    uniprot_id = lines[1].split("\t")[0]
    protein_name = lines[1].split("\t")[2]
    print(f"Protein: {protein_name}")
    print(f"UniProt ID: {uniprot_id}")

# 2. Get KEGG pathways
kegg_mapping = u.mapping(fr="UniProtKB_AC-ID", to="KEGG", query=uniprot_id)
if uniprot_id in kegg_mapping:
    kegg_id = kegg_mapping[uniprot_id][0]

    k = KEGG()
    organism, gene_id = kegg_id.split(":")
    pathways = k.get_pathway_by_gene(gene_id, organism)

    print(f"\nPathways ({len(pathways)}):")
    for pathway_id in pathways[:5]:
        print(f"  {pathway_id}")

# 3. Get GO annotations
g = QuickGO()
go_annotations = g.Annotation(protein=uniprot_id, format="tsv")

if go_annotations:
    lines = go_annotations.strip().split("\n")
    print(f"\nGO Annotations ({len(lines)-1} total):")

    # Group by aspect
    aspects = {"P": [], "F": [], "C": []}
    for line in lines[1:]:
        fields = line.split("\t")
        go_aspect = fields[8]  # P, F, or C
        go_term = fields[7]
        aspects[go_aspect].append(go_term)

    print(f"  Biological Process: {len(aspects['P'])} terms")
    print(f"  Molecular Function: {len(aspects['F'])} terms")
    print(f"  Cellular Component: {len(aspects['C'])} terms")

# 4. Get protein sequence features
full_entry = u.retrieve(uniprot_id, frmt="txt")
print("\nProtein Features:")
for line in full_entry.split("\n"):
    if line.startswith("FT   DOMAIN"):
        print(f"  {line}")
```

* *输出：**全面注释，包括名称、通路、GO术语和特征。

- --

## 蛋白质相互作用网络构建

* *目标：**为一组基因构建蛋白质-蛋白质相互作用网络蛋白质。

### 工作流程

```python
from bioservices import PSICQUIC
import networkx as nx

# Proteins of interest
proteins = ["ZAP70", "LCK", "LAT", "SLP76", "PLCg1"]

# Initialize PSICQUIC
p = PSICQUIC()

# Build network
G = nx.Graph()

for protein in proteins:
    # Query for human interactions
    query = f"{protein} AND species:9606"

    try:
        results = p.query("intact", query)

        if results:
            lines = results.strip().split("\n")

            for line in lines:
                fields = line.split("\t")
                # Extract protein names (simplified)
                protein_a = fields[4].split(":")[1] if ":" in fields[4] else fields[4]
                protein_b = fields[5].split(":")[1] if ":" in fields[5] else fields[5]

                # Add edge
                G.add_edge(protein_a, protein_b)

    except Exception as e:
        print(f"Error querying {protein}: {e}")

print(f"Network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Analyze network
print("\nNode degrees:")
for node in proteins:
    if node in G:
        print(f"  {node}: {G.degree(node)} interactions")

# Export for visualization
nx.write_gml(G, "protein_network.gml")
print("\nNetwork exported to protein_network.gml")
```

* *输出：** NetworkX 图以 GML 格式导出，用于 Cytoscape 可视化。

- --

## 多生物体比较分析

* *目标：** 比较多个生物体中的通路或基因存在有机体.

### 工作流程

```python
from bioservices import KEGG

k = KEGG()

# Organisms to compare
organisms = ["hsa", "mmu", "dme", "sce"]  # Human, mouse, fly, yeast
organism_names = {
    "hsa": "Human",
    "mmu": "Mouse",
    "dme": "Fly",
    "sce": "Yeast"
}

# Pathway of interest
pathway_name = "cell cycle"

print(f"Searching for '{pathway_name}' pathway across organisms:\n")

for org in organisms:
    k.organism = org

    # Search pathways
    results = k.lookfor_pathway(pathway_name)

    print(f"{organism_names[org]} ({org}):")
    if results:
        for pathway in results[:3]:  # Show first 3
            print(f"  {pathway}")
    else:
        print("  No matches found")
    print()
```

* *输出：**跨有机体的路径存在/不存在。

- --

## 工作流程最佳实践

### 1.错误处理

始终包装服务调用：
```python
try:
    result = service.method(params)
    if result:
        # Process
        pass
except Exception as e:
    print(f"Error: {e}")
```

### 2. 速率限制

为批处理添加延迟：
```python
import time

for item in items:
    result = service.query(item)
    time.sleep(0.5)  # 500ms delay
```

### 3. 结果验证

检查是否为空或意外结果：
```python
if result and len(result) > 0:
    # Process
    pass
else:
    print("No results returned")
```

### 4. 进度报告

对于长工作流程：
```python
total = len(items)
for i, item in enumerate(items):
    # Process item
    if (i + 1) % 10 == 0:
        print(f"Processed {i+1}/{total}")
```

### 5. 数据导出

保存中间结果结果：
```python
import json

with open("results.json", "w") as f:
    json.dump(results, f, indent=2)
```

- --

## 与其他工具集成

### BioPython Integration

```python
from bioservices import UniProt
from Bio import SeqIO
from io import StringIO

u = UniProt()
fasta_data = u.retrieve("P43403", "fasta")

# Parse with BioPython
fasta_io = StringIO(fasta_data)
record = SeqIO.read(fasta_io, "fasta")

print(f"Sequence length: {len(record.seq)}")
print(f"Description: {record.description}")
```

### Pandas Integration

```python
from bioservices import UniProt
import pandas as pd
from io import StringIO

u = UniProt()
results = u.search("zap70", frmt="tab", columns="id,genes,length,organism")

# Load into DataFrame
df = pd.read_csv(StringIO(results), sep="\t")
print(df.head())
print(df.describe())
```

### NetworkX Integration

参见上面的蛋白质相互作用网络构建。

- --

完整工作示例，请参阅 `scripts/` 目录中的脚本。
