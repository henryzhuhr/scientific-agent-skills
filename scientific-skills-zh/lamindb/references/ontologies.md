# LaminDB 本体管理

本文档介绍了通过 Bionty 插件在 LaminDB 中进行生物本体管理，包括使用标准化生物术语访问、搜索和注释数据。

## 概述

LaminDB 集成了 `bionty` 插件来管理标准化生物本体，从而实现跨研究项目的一致元数据管理和数据注释。 Bionty 提供对 20 多个精选生物本体的访问，涵盖基因、蛋白质、细胞类型、组织、疾病等。

## 可用本体

LaminDB 提供对多个精选本体源的访问：

|登记处 |本体来源|描述 |
|----------|----------------|-------------|
| **基因** |合奏 |跨生物体（人类、小鼠等）的基因 |
| **蛋白质** |尤尼普罗特|蛋白质序列和注释|
| **细胞类型** |细胞本体论（CL）|标准化细胞类型分类|
| **细胞系** |细胞系本体论（CLO）|细胞系注释|
| **纸巾** |乌伯伦 |解剖结构和组织|
| **疾病** |蒙多，DOID |疾病分类|
| **表型** |人类表型本体论（HPO）|表型异常|
| **途径** |基因本体论（GO）|生物途径和过程|
| **实验因素** |实验因素本体论（EFO）|实验变量|
| **发展阶段** |各种|生物体的发育阶段|
| **种族** |汉斯斯特罗 |人类祖先本体|
| **药物** |药物银行|药物化合物|
| **有机体** | NCBI 分类库 |分类 |

## 安装和导入

```python
# Install bionty (included with lamindb)
pip install lamindb

# Import
import lamindb as ln
import bionty as bt
```

## 导入公共本体

使用公共本体源填充您的注册表：

```python
# Import Cell Ontology
bt.CellType.import_source()

# Import organism-specific genes
bt.Gene.import_source(organism="human")
bt.Gene.import_source(organism="mouse")

# Import tissues
bt.Tissue.import_source()

# Import diseases
bt.Disease.import_source(source="mondo")  # Mondo Disease Ontology
bt.Disease.import_source(source="doid")   # Disease Ontology
```

## 搜索和访问记录

### 关键字搜索

```python
# Search cell types
bt.CellType.search("T cell").to_dataframe()
bt.CellType.search("gamma-delta").to_dataframe()

# Search genes
bt.Gene.search("CD8").to_dataframe()
bt.Gene.search("TP53").to_dataframe()

# Search diseases
bt.Disease.search("cancer").to_dataframe()

# Search tissues
bt.Tissue.search("brain").to_dataframe()
```

### 自动完成查找

对于记录数少于 100k 的注册表：

```python
# Create lookup object
cell_types = bt.CellType.lookup()

# Access by name (auto-complete in IDEs)
t_cell = cell_types.t_cell
hsc = cell_types.hematopoietic_stem_cell

# Similarly for other registries
genes = bt.Gene.lookup()
cd8a = genes.cd8a
```

### 精确字段匹配

```python
# By ontology ID
cell_type = bt.CellType.get(ontology_id="CL:0000798")
disease = bt.Disease.get(ontology_id="MONDO:0004992")

# By name
cell_type = bt.CellType.get(name="T cell")
gene = bt.Gene.get(symbol="CD8A")

# By Ensembl ID
gene = bt.Gene.get(ensembl_gene_id="ENSG00000153563")
```

## 本体层次结构

### 探索关系

```python
# Get a cell type
gdt_cell = bt.CellType.get(ontology_id="CL:0000798")  # gamma-delta T cell

# View direct parents
gdt_cell.parents.to_dataframe()

# View all ancestors recursively
ancestors = []
current = gdt_cell
while current.parents.exists():
    parent = current.parents.first()
    ancestors.append(parent)
    current = parent

# View direct children
gdt_cell.children.to_dataframe()

# View all descendants recursively
gdt_cell.query_children().to_dataframe()
```

### 可视化层次结构

```python
# Visualize parent hierarchy
gdt_cell.view_parents()

# Include children in visualization
gdt_cell.view_parents(with_children=True)

# Get all related terms for visualization
t_cell = bt.CellType.get(name="T cell")
t_cell.view_parents(with_children=True)  # Shows T cell subtypes
```

## 标准化和验证数据

### 验证

检查术语是否存在于本体：

```python
# Validate cell types
bt.CellType.validate(["T cell", "B cell", "invalid_cell"])
# Returns: [True, True, False]

# Validate genes
bt.Gene.validate(["CD8A", "TP53", "FAKEGENE"], organism="human")
# Returns: [True, True, False]

# Check which terms are invalid
terms = ["T cell", "fat cell", "neuron", "invalid_term"]
invalid = [t for t, valid in zip(terms, bt.CellType.validate(terms)) if not valid]
print(f"Invalid terms: {invalid}")
```

### 同义词标准化

将非标准术语转换为经过验证的名称：

```python
# Standardize cell type names
bt.CellType.standardize(["fat cell", "blood forming stem cell"])
# Returns: ['adipocyte', 'hematopoietic stem cell']

# Standardize genes
bt.Gene.standardize(["BRCA-1", "p53"], organism="human")
# Returns: ['BRCA1', 'TP53']

# Handle mixed valid/invalid terms
terms = ["T cell", "T lymphocyte", "invalid"]
standardized = bt.CellType.standardize(terms)
# Returns standardized names where possible
```

### 加载经过验证记录

```python
# Load records from values (including synonyms)
records = bt.CellType.from_values(["fat cell", "blood forming stem cell"])

# Returns list of CellType records
for record in records:
    print(record.name, record.ontology_id)

# Use with gene symbols
genes = bt.Gene.from_values(["CD8A", "CD8B"], organism="human")
```

## 注释数据集

### 注释AnnData

```python
import anndata as ad
import lamindb as ln

# Load example data
adata = ad.read_h5ad("data.h5ad")

# Validate and retrieve matching records
cell_types = bt.CellType.from_values(adata.obs.cell_type)

# Create artifact with annotations
artifact = ln.Artifact.from_anndata(
    adata,
    key="scrna/annotated_data.h5ad",
    description="scRNA-seq data with validated cell type annotations"
).save()

# Link ontology records to artifact
artifact.feature_sets.add_ontology(cell_types)
```

### 注释DataFrames

```python
import pandas as pd

# Create DataFrame with biological entities
df = pd.DataFrame({
    "cell_type": ["T cell", "B cell", "NK cell"],
    "tissue": ["blood", "spleen", "liver"],
    "disease": ["healthy", "lymphoma", "healthy"]
})

# Validate and standardize
df["cell_type"] = bt.CellType.standardize(df["cell_type"])
df["tissue"] = bt.Tissue.standardize(df["tissue"])

# Create artifact
artifact = ln.Artifact.from_dataframe(
    df,
    key="metadata/sample_info.parquet"
).save()

# Link ontology records
cell_type_records = bt.CellType.from_values(df["cell_type"])
tissue_records = bt.Tissue.from_values(df["tissue"])

artifact.feature_sets.add_ontology(cell_type_records)
artifact.feature_sets.add_ontology(tissue_records)
```

## 管理自定义术语和层次结构

### 添加自定义术语

```python
# Register new term not in public ontology
my_celltype = bt.CellType(name="my_novel_T_cell_subtype").save()

# Establish parent-child relationship
parent = bt.CellType.get(name="T cell")
my_celltype.parents.add(parent)

# Verify relationship
my_celltype.parents.to_dataframe()
parent.children.to_dataframe()  # Should include my_celltype
```

### 添加同义词

```python
# Add synonyms for standardization
hsc = bt.CellType.get(name="hematopoietic stem cell")
hsc.add_synonym("HSC")
hsc.add_synonym("blood stem cell")
hsc.add_synonym("hematopoietic progenitor")

# Set abbreviation
hsc.set_abbr("HSC")

# Now standardization works with synonyms
bt.CellType.standardize(["HSC", "blood stem cell"])
# Returns: ['hematopoietic stem cell', 'hematopoietic stem cell']
```

### 创建自定义层次结构

```python
# Build custom cell type hierarchy
immune_cell = bt.CellType.get(name="immune cell")

# Add custom subtypes
my_subtype1 = bt.CellType(name="custom_immune_subtype_1").save()
my_subtype2 = bt.CellType(name="custom_immune_subtype_2").save()

# Link to parent
my_subtype1.parents.add(immune_cell)
my_subtype2.parents.add(immune_cell)

# Create sub-subtypes
my_subsubtype = bt.CellType(name="custom_sub_subtype").save()
my_subsubtype.parents.add(my_subtype1)

# Visualize custom hierarchy
immune_cell.view_parents(with_children=True)
```

## 多生物体支持

对于生物体感知注册表，如Gene：

```python
# Set global organism
bt.settings.organism = "human"

# Validate human genes
bt.Gene.validate(["TCF7", "CD8A"], organism="human")

# Load genes for specific organism
human_genes = bt.Gene.from_values(["CD8A", "TP53"], organism="human")
mouse_genes = bt.Gene.from_values(["Cd8a", "Trp53"], organism="mouse")

# Search organism-specific genes
bt.Gene.search("CD8", organism="human").to_dataframe()
bt.Gene.search("Cd8", organism="mouse").to_dataframe()

# Switch organism context
bt.settings.organism = "mouse"
genes = bt.Gene.from_source(symbol="Ap5b1")
```

## 公共本体查找

从公共本体访问术语，无需导入：

```python
# Interactive lookup in public sources
cell_types_public = bt.CellType.lookup(public=True)

# Access public terms
hepatocyte = cell_types_public.hepatocyte

# Import specific term
hepatocyte_local = bt.CellType.from_source(name="hepatocyte")

# Or import by ontology ID
specific_cell = bt.CellType.from_source(ontology_id="CL:0000182")
```

## 版本跟踪

LaminDB自动跟踪本体版本：

```python
# View current source versions
bt.Source.filter(currently_used=True).to_dataframe()

# Check which source a record derives from
cell_type = bt.CellType.get(name="hepatocyte")
cell_type.source  # Returns Source metadata

# View source details
source = cell_type.source
print(source.name)        # e.g., "cl"
print(source.version)     # e.g., "2023-05-18"
print(source.url)         # Ontology URL
```

## 本体集成工作流程

### 工作流程1：验证现有数据

```python
# Load data with biological annotations
adata = ad.read_h5ad("uncurated_data.h5ad")

# Validate cell types
validation = bt.CellType.validate(adata.obs.cell_type)

# Identify invalid terms
invalid_idx = [i for i, v in enumerate(validation) if not v]
invalid_terms = adata.obs.cell_type.iloc[invalid_idx].unique()
print(f"Invalid cell types: {invalid_terms}")

# Fix invalid terms manually or with standardization
adata.obs["cell_type"] = bt.CellType.standardize(adata.obs.cell_type)

# Re-validate
validation = bt.CellType.validate(adata.obs.cell_type)
assert all(validation), "All terms should now be valid"
```

### 工作流程 2：整理和注释

```python
import lamindb as ln

ln.track()  # Start tracking

# Load data
df = pd.read_csv("experimental_data.csv")

# Standardize using ontologies
df["cell_type"] = bt.CellType.standardize(df["cell_type"])
df["tissue"] = bt.Tissue.standardize(df["tissue"])

# Create curated artifact
artifact = ln.Artifact.from_dataframe(
    df,
    key="curated/experiment_2025_10.parquet",
    description="Curated experimental data with ontology-validated annotations"
).save()

# Link ontology records
artifact.feature_sets.add_ontology(bt.CellType.from_values(df["cell_type"]))
artifact.feature_sets.add_ontology(bt.Tissue.from_values(df["tissue"]))

ln.finish()  # Complete tracking
```

### 工作流程 3：跨生物体基因定位

```python
# Get human genes
human_genes = ["CD8A", "CD8B", "TP53"]
human_records = bt.Gene.from_values(human_genes, organism="human")

# Find mouse orthologs (requires external mapping)
# LaminDB doesn't provide built-in ortholog mapping
# Use external tools like Ensembl BioMart or homologene

mouse_orthologs = ["Cd8a", "Cd8b", "Trp53"]
mouse_records = bt.Gene.from_values(mouse_orthologs, organism="mouse")
```

## 查询本体注释数据

```python
# Find all datasets with specific cell type
t_cell = bt.CellType.get(name="T cell")
ln.Artifact.filter(feature_sets__cell_types=t_cell).to_dataframe()

# Find datasets measuring specific genes
cd8a = bt.Gene.get(symbol="CD8A", organism="human")
ln.Artifact.filter(feature_sets__genes=cd8a).to_dataframe()

# Query across ontology hierarchy
# Find all datasets with T cell or T cell subtypes
t_cell_subtypes = t_cell.query_children()
ln.Artifact.filter(
    feature_sets__cell_types__in=t_cell_subtypes
).to_dataframe()
```

## 最佳实践

1. **先导入本体**：在验证
2之前调用`import_source()`。 **使用标准化**：利用同义词映射来处理变体
3. **尽早验证**：在创建工件之前检查条款
4. **设置生物体上下文**：为基因相关查询指定生物体
5. **添加自定义同义词**：在您的域中注册常见变体
6. **使用公共查找**：访问 `lookup(public=True)` 进行术语发现
7. **跟踪版本**：监控本体源版本的可重复性
8. **构建层次结构**：将自定义术语链接到现有本体结构
9. **分层查询**：使用`query_children()`进行全面搜索
10. **文档映射**：跟踪自定义术语添加和关系

## 常见本体操作

```python
# Check if term exists
exists = bt.CellType.filter(name="T cell").exists()

# Count terms in registry
n_cell_types = bt.CellType.filter().count()

# Get all terms with specific parent
immune_cells = bt.CellType.filter(parents__name="immune cell")

# Find orphan terms (no parents)
orphans = bt.CellType.filter(parents__isnull=True)

# Get recently added terms
from datetime import datetime, timedelta
recent = bt.CellType.filter(
    created_at__gte=datetime.now() - timedelta(days=7)
)
```
