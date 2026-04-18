---
name: gget
description: "对 20 多个生物信息学数据库进行快速 CLI/Python 查询。用于快速查找：基因信息、BLAST 搜索、AlphaFold 结构、富集分析。最适合交互式探索、简单查询。对于批处理或高级 BLAST，请使用 biopython；对于多数据库 Python 工作流程，请使用 bioservices。"
license: BSD-2-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# gget

## 概述

gget 是一个命令行生物信息学工具和 Python 包，提供对 20 多个基因组数据库和分析方法的统一访问。通过一致的界面查询基因信息、序列分析、蛋白质结构、表达数据和疾病关联。所有 gget 模块都可以用作命令行工具和 Python 函数。

* *重要**：gget 查询的数据库不断更新，有时会更改其结构。 gget模块每两周自动测试一次，并在必要时更新以匹配新的数据库结构。

## 安装

在干净的虚拟环境中安装gget以避免冲突：

```bash
# Using uv (recommended)
uv uv pip install gget

# Or using pip
uv pip install --upgrade gget

# In Python/Jupyter
import gget
```

## 快速入门

所有人的基本使用模式模块：

```bash
# Command-line
gget <module> [arguments] [options]

# Python
gget.module(arguments, options)
```

大多数模块返回：
- **命令行**：JSON（默认）或带有 `-csv` 标志的 CSV
- **Python**：DataFrame 或字典

 模块之间的通用标志：
- `-o/--out`：将结果保存到文件
- `-q/--quiet`：抑制进度信息
- `-csv`：返回CSV格式（仅限命令行）

## 模块类别

### 1.参考和基因信息

#### gget ref - 参考基因组下载

检索 Ensembl 参考基因组的下载链接和元数据。

* *参数**：
- `species`：Genus_species 格式（例如“homo_sapiens”、“mus_musculus”）。快捷方式：“人类”、“鼠标”
- `-w/--which`：指定返回类型（gtf、cdna、dna、cds、cdrna、pep）。默认值：全部
- `-r/--release`：Ensembl 版本号（默认值：最新）
- `-l/--list_species`：列出可用的脊椎动物物种
- `-liv/--list_iv_species`：列出可用的无脊椎动物物种
- `-ftp`：仅返回 FTP链接
- `-d/--download`：下载文件（需要curl）

* *示例**：
```bash
# List available species
gget ref --list_species

# Get all reference files for human
gget ref homo_sapiens

# Download only GTF annotation for mouse
gget ref -w gtf -d mouse
```

```python
# Python
gget.ref("homo_sapiens")
gget.ref("mus_musculus", which="gtf", download=True)
```

#### gget搜索-基因搜索

按名称或描述跨物种定位基因。

* *参数**：
- `searchwords`：一个或多个搜索词（不区分大小写）
- `-s/--species`：目标物种（例如，“homo_sapiens”、“mouse”）
- `-r/--release`：Ensembl 版本号
- `-t/--id_type`：返回“基因”（默认）或“转录本” 
- `-ao/--andor`：“或”（默认）查找任何搜索词； 'and' 需要 ALL
- `-l/--limit`：返回的最大结果

* *返回**：ensembl_id、gene_name、ensembl_description、ext_ref_description、biotype、 URL

* *示例**：
```bash
# Search for GABA-related genes in human
gget search -s human gaba gamma-aminobutyric

# Find specific gene, require all terms
gget search -s mouse -ao and pax7 transcription
```

```python
# Python
gget.search(["gaba", "gamma-aminobutyric"], species="homo_sapiens")
```

#### gget 信息 - 基因/转录信息

从 Ensembl、UniProt 和NCBI.

* *参数**：
- `ens_ids`：一个或多个 Ensembl ID（还支持 WormBase、Flybase ID）。限制：~1000 个 ID
- `-n/--ncbi`：禁用 NCBI 数据检索
- `-u/--uniprot`：禁用 UniProt 数据检索
- `-pdb`：包括 PDB 标识符（增加运行时间）

* *返回**：UniProt ID， NCBI 基因 ID、主要基因名称、同义词、蛋白质名称、描述、生物型、规范转录本

* *示例**：
```bash
# Get info for multiple genes
gget info ENSG00000034713 ENSG00000104853 ENSG00000170296

# Include PDB IDs
gget info ENSG00000034713 -pdb
```

```python
# Python
gget.info(["ENSG00000034713", "ENSG00000104853"], pdb=True)
```

#### gget seq - 序列检索

获取基因和转录本的核苷酸或氨基酸序列。

* *参数**：
- `ens_ids`：一个或多个Ensembl标识符
- `-t/--translate`：获取氨基酸序列而不是核苷酸
- `-iso/--isoforms`：返回所有转录本变体（仅基因 ID）

* *返回**：FASTA 格式序列

* *示例**：
```bash
# Get nucleotide sequences
gget seq ENSG00000034713 ENSG00000104853

# Get all protein isoforms
gget seq -t -iso ENSG00000034713
```

```python
# Python
gget.seq(["ENSG00000034713"], translate=True, isoforms=True)
```

### 2. 序列分析&比对

#### gget BLAST - BLAST 根据标准数据库搜索

BLAST 核苷酸或氨基酸序列。

* *参数**：
- `sequence`：FASTA/.txt 文件的序列字符串或路径
- `-p/--program`：blastn、blastp、blastx、tblastn、tblastx（自动检测）
- `-db/--database`：
  - 核苷酸： nt、refseq_rna、pdbnt
  - 蛋白质：nr、swissprot、pdbaa、refseq_ Protein
- `-l/--limit`：最大命中数（默认值：50）
- `-e/--expect`：E 值截止值（默认值： 10.0)
- `-lcf/--low_comp_filt`：启用低复杂度过滤
- `-mbo/--megablast_off`：禁用 MegaBLAST (blastn仅）

* *示例**：
```bash
# BLAST protein sequence
gget blast MKWMFKEDHSLEHRCVESAKIRAKYPDRVPVIVEKVSGSQIVDIDKRKYLVPSDITVAQFMWIIRKRIQLPSEKAIFLFVDKTVPQSR

# BLAST from file with specific database
gget blast sequence.fasta -db swissprot -l 10
```

```python
# Python
gget.blast("MKWMFK...", database="swissprot", limit=10)
```

#### gget blat - BLAT 搜索

使用 UCSC 定位序列的基因组位置BLAT.

* *参数**：
- `sequence`：FASTA/.txt 文件的序列字符串或路径
- `-st/--seqtype`：'DNA'、'蛋白质'、'translated%20RNA'、'translated%20DNA' （自动检测）
- `-a/--assembly`：目标组装（默认：“人类”/hg38；选项：“鼠标”/mm39、“斑马雀”/taeGut2等）

* *返回**：基因组、查询大小、比对位置、匹配、不匹配、比对百分比

* *示例**：
```bash
# Find genomic location in human
gget blat ATCGATCGATCGATCG

# Search in different assembly
gget blat -a mm39 ATCGATCGATCGATCG
```

```python
# Python
gget.blat("ATCGATCGATCGATCG", assembly="mouse")
```

#### gget 肌肉 - 多序列比对

使用比对多个核苷酸或氨基酸序列Muscle5.

* *参数**：
- `fasta`：FASTA/.txt 文件的序列或路径
- `-s5/--super5`：使用 Super5 算法更快地处理（大型数据集）

* *返回**：ClustalW 格式的对齐序列或对齐的 FASTA (.afa)

* *示例**：
```bash
# Align sequences from file
gget muscle sequences.fasta -o aligned.afa

# Use Super5 for large dataset
gget muscle large_dataset.fasta -s5
```

```python
# Python
gget.muscle("sequences.fasta", save=True)
```

#### gget 钻石 - 局部序列比对

使用以下命令执行快速局部蛋白质或翻译 DNA 比对钻石.

* *参数**：
- 查询：序列（字符串/列表）或 FASTA 文件路径 
- `--reference`：参考序列（字符串/列表）或 FASTA 文件路径（必填） 
- `--sensitivity`：快速、中敏感、敏感、更敏感、非常敏感（默认），超敏感
- `--threads`：CPU线程（默认：1）
- `--diamond_db`：保存数据库以供重复使用
- `--translated`：启用核苷酸到氨基酸比对

* *返回**：同一性百分比、序列长度、匹配位置、缺口开口、E值、位分数

* *示例**：
```bash
# Align against reference
gget diamond GGETISAWESQME -ref reference.fasta --threads 4

# Save database for reuse
gget diamond query.fasta -ref ref.fasta --diamond_db my_db.dmnd
```

```python
# Python
gget.diamond("GGETISAWESQME", reference="reference.fasta", threads=4)
```

### 3. 结构和蛋白质分析

#### gget pdb - 蛋白质结构

查询 RCSB 蛋白质数据库的结构和元数据.

* *参数**：
- `pdb_id`：PDB 标识符（例如，'7S7U'）
- `-r/--resource`：数据类型（pdb、entry、pubmed、程序集、实体类型）
- `-i/--identifier`：程序集、实体或链 ID

* *返回**：PDB 格式（结构）或 JSON（元数据）

* *示例**：
```bash
# Download PDB structure
gget pdb 7S7U -o 7S7U.pdb

# Get metadata
gget pdb 7S7U -r entry
```

```python
# Python
gget.pdb("7S7U", save=True)
```

#### gget alphafold - 蛋白质结构预测

使用简化的AlphaFold2预测3D蛋白质结构。

* *需要设置**：
```bash
# Install OpenMM first
uv pip install openmm

# Then setup AlphaFold
gget setup alphafold
```

* *参数**：
- `sequence`：氨基酸序列（字符串）、多个序列（列表）或FASTA文件。多个序列触发多聚体建模
- `-mr/--multimer_recycles`：回收迭代（默认：3；建议20次以确保准确性）
- `-mfm/--multimer_for_monomer`：将多聚体模型应用于单个蛋白质
- `-r/--relax`：顶级模型的AMBER松弛
- `plot`：仅限 Python；生成交互式 3D 可视化（默认值：True）
- `show_sidechains`：仅限 Python；包含侧链（默认：True）

* *返回**：PDB结构文件，JSON对齐错误数据，可选3D可视化

* *示例**：
```bash
# Predict single protein structure
gget alphafold MKWMFKEDHSLEHRCVESAKIRAKYPDRVPVIVEKVSGSQIVDIDKRKYLVPSDITVAQFMWIIRKRIQLPSEKAIFLFVDKTVPQSR

# Predict multimer with higher accuracy
gget alphafold sequence1.fasta -mr 20 -r
```

```python
# Python with visualization
gget.alphafold("MKWMFK...", plot=True, show_sidechains=True)

# Multimer prediction
gget.alphafold(["sequence1", "sequence2"], multimer_recycles=20)
```

#### gget elm -真核线性基序

预测蛋白质序列中的真核线性基序。

* *需要设置**：
```bash
gget setup elm
```

* *参数**：
- `sequence`：氨基酸序列或UniProt Acc
- `-u/--uniprot`：表示序列是UniProt Acc
- `-e/--expand`：包括蛋白质名称、生物体、参考文献
- `-s/--sensitivity`：DIAMOND 比对灵敏度（默认值：“非常敏感”）
- `-t/--threads`：线程数（默认值：1）

* *返回**：两个输出：
1. **ortholog_df**：来自直系同源蛋白
2的线性基序。 **regex_df**：在输入序列中直接匹配的基序

* *示例**：
```bash
# Predict motifs from sequence
gget elm LIAQSIGQASFV -o results

# Use UniProt accession with expanded info
gget elm --uniprot Q02410 -e
```

```python
# Python
ortholog_df, regex_df = gget.elm("LIAQSIGQASFV")
```

### 4.表达和疾病数据

#### gget archs4 - 基因相关性和组织表达

查询ARCHS4数据库以获取相关基因或组织表达数据。

* *参数**：
- `gene`：基因符号或Ensembl ID（带有`--ensembl`标志）
- `-w/--which`：'相关'（默认，返回100）最相关的基因）或“组织”（表达图谱）
- `-s/--species`：“人类”（默认）或“小鼠”（仅限组织数据）
- `-e/--ensembl`：输入是 Ensembl ID

  * *返回**：
- **相关模式**：基因符号， Pearson 相关系数
- **组织模式**：组织标识符，最小/Q1/中值/Q3/最大表达值

* *示例**：
```bash
# Get correlated genes
gget archs4 ACE2

# Get tissue expression
gget archs4 -w tissue ACE2
```

```python
# Python
gget.archs4("ACE2", which="tissue")
```

#### gget cellxgene -单细胞 RNA-seq 数据

Query CZ CELLxGENE 发现单细胞数据普查。

* *需要设置**：
```bash
gget setup cellxgene
```

 * *参数**：
- `--gene` (-g)：基因名称或 Ensembl ID（区分大小写！“PAX7”表示人类，“Pax7”表示小鼠）
- `--tissue`：组织类型 
- `--cell_type`：特定细胞类型 
- `--species` (-s)：“homo_sapiens”（默认）或“mus_musculus”
- `--census_version` (-cv)：版本（“稳定”、“最新”或日期）
- `--ensembl` (-e)：使用 Ensembl ID
- `--meta_only` (-mo)：仅返回元数据
- 其他过滤器：疾病、发育阶段、性别、测定、数据集 ID、供体 ID、种族、悬浮类型

* *返回**：具有计数矩阵和元数据（或仅元数据数据帧）的 AnnData 对象

* *示例**：
```bash
# Get single-cell data for specific genes and cell types
gget cellxgene --gene ACE2 ABCA1 --tissue lung --cell_type "mucus secreting cell" -o lung_data.h5ad

# Metadata only
gget cellxgene --gene PAX7 --tissue muscle --meta_only -o metadata.csv
```

```python
# Python
adata = gget.cellxgene(gene=["ACE2", "ABCA1"], tissue="lung", cell_type="mucus secreting cell")
```

#### gget丰富器 - 丰富分析

执行使用Enrichr.

* *参数**：
- `genes`：基因符号或Ensembl ID
- `-db/--database`：参考数据库（支持快捷方式：'pathway'，'transcription'，'ontology'，'diseases_drugs'， 'celltypes')
- `-s/--species`：人类（默认）、小鼠、苍蝇、酵母、蠕虫、鱼
- `-bkg_l/--background_list`：用于比较的背景基因
- `-ko/--kegg_out`：保存带有突出显示基因的KEGG通路图像
- `plot`：仅限 Python；生成图形结果

* *数据库快捷方式**：
- 'pathway' → KEGG_2021_Human
- 'transcription' → ChEA_2016
- 'ontology' → GO_Biological_Process_2021
- “疾病_药物”→ GWAS_Catalog_2019
- “细胞类型”→ PanglaoDB_Augmented_2021

* *示例**：
```bash
# Enrichment analysis for ontology
gget enrichr -db ontology ACE2 AGT AGTR1

# Save KEGG pathways
gget enrichr -db pathway ACE2 AGT AGTR1 -ko ./kegg_images/
```

```python
# Python with plot
gget.enrichr(["ACE2", "AGT", "AGTR1"], database="ontology", plot=True)
```

#### gget bgee - Orthology & Expression

检索直系同源和基因表达数据Bgee数据库。

* *参数**：
- `ens_id`：Ensembl基因ID或NCBI基因ID（对于非Ensembl物种）。 `type=expression`
- `-t/--type` 时支持多个 ID：“orthologs”（默认）或“expression”

* *返回**：
- **直系同源模式**：将跨物种的基因与ID、名称、分类信息进行匹配
- **表达模式**：解剖实体、置信度分数、表达status

* *示例**：
```bash
# Get orthologs
gget bgee ENSG00000169194

# Get expression data
gget bgee ENSG00000169194 -t expression

# Multiple genes
gget bgee ENSBTAG00000047356 ENSBTAG00000018317 -t expression
```

```python
# Python
gget.bgee("ENSG00000169194", type="orthologs")
```

#### gget opentargets - 疾病与药物协会

从检索疾病和药物关联OpenTargets.

* *参数**：
- Ensembl 基因 ID（必填）
- `-r/--resource`：疾病（默认）、药物、易处理性、药物遗传学、表达、depmap、相互作用
- `-l/--limit`：上限结果计数
- 过滤器参数（因资源而异）：
  - 药物：`--filter_disease`
  - 药物遗传学：`--filter_drug`
  - 表达/depmap：`--filter_tissue`、`--filter_anat_sys`、`--filter_organ`
  - 相互作用： `--filter_protein_a`、`--filter_protein_b`、`--filter_gene_b`

* *示例**：
```bash
# Get associated diseases
gget opentargets ENSG00000169194 -r diseases -l 5

# Get associated drugs
gget opentargets ENSG00000169194 -r drugs -l 10

# Get tissue expression
gget opentargets ENSG00000169194 -r expression --filter_tissue brain
```

```python
# Python
gget.opentargets("ENSG00000169194", resource="diseases", limit=5)
```

#### gget cbio - cBioPortal Cancer Genomics

使用 cBioPortal 数据绘制癌症基因组热图。

* *两个子命令**：

* *搜索** - 查找研究 ID：
```bash
gget cbio search breast lung
```

* *图** - 生成热图：

* *参数**：
- `-s/--study_ids`：以空格分隔的 cBioPortal 研究 ID（必需）
- `-g/--genes`：以空格分隔的基因名称或 Ensembl ID（必需）
- `-st/--stratification`：列组织数据（tissue、cancer_type、cancer_type_detailed、study_id、sample）
- `-vt/--variation_type`：数据类型（mutation_occurrences、cna_nonbinary、sv_occurrences、cna_occurrences、Consequence）
- `-f/--filter`：按列值过滤（例如， 'study_id:msk_impact_2017')
- `-dd/--data_dir`：缓存目录（默认：./gget_cbio_cache）
- `-fd/--figure_dir`：输出目录（默认：./gget_cbio_figures）
- `-dpi`：分辨率（默认值：100）
- `-sh/--show`：在窗口中显示绘图
- `-nc/--no_confirm`：跳过下载确认

* *示例**：
```bash
# Search for studies
gget cbio search esophag ovary

# Create heatmap
gget cbio plot -s msk_impact_2017 -g AKT1 ALK BRAF -st tissue -vt mutation_occurrences
```

```python
# Python
gget.cbio_search(["esophag", "ovary"])
gget.cbio_plot(["msk_impact_2017"], ["AKT1", "ALK"], stratification="tissue")
```

#### gget cosmic - COSMIC 数据库

搜索 COSMIC（癌症体细胞突变目录）数据库。

* *重要**：商业用途需支付许可费。需要 COSMIC 帐户凭据。

* *参数**：
- `searchterm`：基因名称、Ensembl ID、突变符号或样本 ID
- `-ctp/--cosmic_tsv_path`：下载的 COSMIC TSV 文件的路径（查询时需要）
- `-l/--limit`：最大结果（默认值：100）

* *数据库下载标志**：
- `-d/--download_cosmic`：激活下载模式
- `-gm/--gget_mutate`：为gget mutate创建版本
- `-cp/--cosmic_project`：数据库类型（cancer、census、cell_line、抗性、基因组筛选、目标筛选）
- `-cv/--cosmic_version`：COSMIC 版本
- `-gv/--grch_version`：人类参考基因组（37 或 38）
- `--email`、`--password`：COSMIC凭证

* *示例**：
```bash
# First download database
gget cosmic -d --email user@example.com --password xxx -cp cancer

# Then query
gget cosmic EGFR -ctp cosmic_data.tsv -l 10
```

```python
# Python
gget.cosmic("EGFR", cosmic_tsv_path="cosmic_data.tsv", limit=10)
```

### 5. 其他工具

#### gget mutate - 生成突变序列

生成突变核苷酸序列来自突变注释。

* *参数**：
- `sequences`：FASTA 文件路径或直接序列输入（字符串/列表）
- `-m/--mutations`：带有突变数据的 CSV/TSV 文件或 DataFrame（必需）
- `-mc/--mut_column`：突变列名称（默认值：'mutation'）
- `-sic/--seq_id_column`：序列 ID 列（默认值：'seq_ID'）
- `-mic/--mut_id_column`：突变 ID 列
- `-k/--k`：侧翼序列的长度（默认值：30）核苷酸）

* *返回**：FASTA格式的突变序列

* *示例**：
```bash
# Single mutation
gget mutate ATCGCTAAGCT -m "c.4G>T"

# Multiple sequences with mutations from file
gget mutate sequences.fasta -m mutations.csv -o mutated.fasta
```

```python
# Python
import pandas as pd
mutations_df = pd.DataFrame({"seq_ID": ["seq1"], "mutation": ["c.4G>T"]})
gget.mutate(["ATCGCTAAGCT"], mutations=mutations_df)
```

#### gget gpt - OpenAI Text Generation

使用 OpenAI 的 API 生成自然语言文本。

* *需要设置**：
```bash
gget setup gpt
```

* *重要**：免费套餐仅限帐户创建后 3 个月。设置每月计费限额。

* *参数**：
- `prompt`：生成的文本输入（必填）
- `api_key`：OpenAI认证（必填）
- 模型配置：温度、top_p、max_tokens、频率_惩罚、存在_惩罚
- 默认模型： gpt-3.5-turbo (可配置)

* *示例**:
```bash
gget gpt "Explain CRISPR" --api_key your_key_here
```

```python
# Python
gget.gpt("Explain CRISPR", api_key="your_key_here")
```

#### gget 设置 - 安装依赖项

安装/下载特定的第三方依赖项module.

* *参数**：
- `module`：需要依赖安装的模块名称
- `-o/--out`：输出文件夹路径（仅限elm模块）

* *需要设置的模块**：
- `alphafold` - 下载约4GB模型参数
- `cellxgene` - 安装cellxgene-census（可能不支持最新的Python）
- `elm` - 下载本地ELM数据库
- `gpt` - 配置OpenAI集成

* *示例**：
```bash
# Setup AlphaFold
gget setup alphafold

# Setup ELM with custom directory
gget setup elm -o /path/to/elm_data
```

```python
# Python
gget.setup("alphafold")
```

## 常用工作流程

### 工作流程1：基因发现到序列分析

查找并分析兴趣：

```python
# 1. Search for genes
results = gget.search(["GABA", "receptor"], species="homo_sapiens")

# 2. Get detailed information
gene_ids = results["ensembl_id"].tolist()
info = gget.info(gene_ids[:5])

# 3. Retrieve sequences
sequences = gget.seq(gene_ids[:5], translate=True)
```

### 工作流程 2：序列比对和结构

比对序列并预测结构：

```python
# 1. Align multiple sequences
alignment = gget.muscle("sequences.fasta")

# 2. Find similar sequences
blast_results = gget.blast(my_sequence, database="swissprot", limit=10)

# 3. Predict structure
structure = gget.alphafold(my_sequence, plot=True)

# 4. Find linear motifs
ortholog_df, regex_df = gget.elm(my_sequence)
```

### 工作流程 3：基因表达和富集

分析表达模式和功能富集：

```python
# 1. Get tissue expression
tissue_expr = gget.archs4("ACE2", which="tissue")

# 2. Find correlated genes
correlated = gget.archs4("ACE2", which="correlation")

# 3. Get single-cell data
adata = gget.cellxgene(gene=["ACE2"], tissue="lung", cell_type="epithelial cell")

# 4. Perform enrichment analysis
gene_list = correlated["gene_symbol"].tolist()[:50]
enrichment = gget.enrichr(gene_list, database="ontology", plot=True)
```

### 工作流程 4：疾病和药物分析

研究疾病关联和治疗靶点：

```python
# 1. Search for genes
genes = gget.search(["breast cancer"], species="homo_sapiens")

# 2. Get disease associations
diseases = gget.opentargets("ENSG00000169194", resource="diseases")

# 3. Get drug associations
drugs = gget.opentargets("ENSG00000169194", resource="drugs")

# 4. Query cancer genomics data
study_ids = gget.cbio_search(["breast"])
gget.cbio_plot(study_ids[:2], ["BRCA1", "BRCA2"], stratification="cancer_type")

# 5. Search COSMIC for mutations
cosmic_results = gget.cosmic("BRCA1", cosmic_tsv_path="cosmic.tsv")
```

### 工作流程 5：比较基因组学

比较不同蛋白之间的蛋白质物种：

```python
# 1. Get orthologs
orthologs = gget.bgee("ENSG00000169194", type="orthologs")

# 2. Get sequences for comparison
human_seq = gget.seq("ENSG00000169194", translate=True)
mouse_seq = gget.seq("ENSMUSG00000026091", translate=True)

# 3. Align sequences
alignment = gget.muscle([human_seq, mouse_seq])

# 4. Compare structures
human_structure = gget.pdb("7S7U")
mouse_structure = gget.alphafold(mouse_seq)
```

### 工作流程 6：构建参考指数

为下游分析准备参考数据（例如 kallisto|bustools）：

```bash
# 1. List available species
gget ref --list_species

# 2. Download reference files
gget ref -w gtf -w cdna -d homo_sapiens

# 3. Build kallisto index
kallisto index -i transcriptome.idx transcriptome.fasta

# 4. Download genome for alignment
gget ref -w dna -d homo_sapiens
```

## 最佳实践

### 数据检索
- 使用 `--limit` 控制大型查询的结果大小
- 使用 `-o/--out` 保存结果以实现可重复性
- 检查数据库版本/版本以确保分析之间的一致性
- 在生产脚本中使用 `--quiet` 来减少输出

### 序列分析
- 对于BLAST/BLAT，从默认参数开始，然后调整灵敏度
- 将`gget diamond`与`--threads`结合使用以实现更快的局部比对
- 使用`--diamond_db`保存DIAMOND数据库以进行重复查询
- 对于多个序列比对，对大型数据集使用 `-s5/--super5`

### 表达和疾病数据
- 基因符号在 cellxgene 中区分大小写（例如，'PAX7' 与 'Pax7'）
- 在首次使用 alphafold、cellxgene、elm 之前运行 `gget setup`， gpt
- 对于富集分析，使用数据库快捷方式以方便
- 使用 `-dd` 缓存 cBioPortal 数据以避免重复下载

### 结构预测
- AlphaFold 多聚体预测：使用 `-mr 20` 获得更高的准确性
- 使用`-r` 最终结构的 AMBER 松弛标志
- 使用 `plot=True`
 在 Python 中可视化结果-在运行 AlphaFold 预测之前先检查 PDB 数据库

### 错误处理
- 数据库结构更改；定期更新 gget： `uv pip install --upgrade gget`
- 使用 gget 信息一次处理最多约 1000 个 Ensembl ID
- 对于大规模分析，对 API 查询实施速率限制
- 使用虚拟环境以避免依赖冲突

## 输出格式

### 命令行
- 默认：JSON
- CSV：添加 `-csv` 标志
- FASTA：gget seq，gget mutate
- PDB：gget pdb、gget alphafold
- PNG：gget cbio 图

### Python
- 默认：DataFrame 或字典
- JSON：添加 `json=True` 参数
- 保存到文件：添加 `save=True`或指定 `out="filename"`
- AnnData: gget cellxgene

## 资源

该技能包括详细模块信息的参考文档：

### 参考/
- `module_reference.md` - 所有模块的综合参数参考
- `database_info.md` - 有关查询数据库及其更新频率的信息
- `workflows.md` - 扩展工作流示例和使用案例 

 如需更多帮助：
 - 官方文档：https://pachterlab.github.io/gget/
  - GitHub 问题：https://github.com/pachterlab/gget/issues
  - 引用：Luebbert, L. & Pachter, L. (2023)。使用 gget 高效查询基因组参考数据库。生物信息学。 https://doi.org/10.1093/bioinformatics/btac836
