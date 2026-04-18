# LaminDB 注释和验证

本文档涵盖了 LaminDB 中的数据管理、验证、模式管理和注释最佳实践。

## 概述

LaminDB 的管理流程通过三个基本步骤确保数据集经过验证和可查询：

1. **验证**：确认数据集与所需模式
2匹配。 **标准化**：修复拼写错误和映射同义词
3等不一致问题。 **注释**：将数据集链接到元数据实体以实现可查询性

## 模式设计

模式定义预期的数据结构、类型和验证规则。 LaminDB 支持三种主要模式方法：

### 1. 灵活模式

仅验证与功能注册表名称匹配的列，允许附加元数据：

```python
import lamindb as ln

# Create flexible schema
schema = ln.Schema(
    name="valid_features",
    itype=ln.Feature  # Validates against Feature registry
).save()

# Any column matching a Feature name will be validated
# Additional columns are permitted but not validated
```

### 2. 最少所需模式

指定基本列，同时允许额外的列元数据：

```python
# Define required features
required_features = [
    ln.Feature.get(name="cell_type"),
    ln.Feature.get(name="tissue"),
    ln.Feature.get(name="donor_id")
]

# Create schema with required features
schema = ln.Schema(
    name="minimal_immune_schema",
    features=required_features,
    flexible=True  # Allows additional columns
).save()
```

### 3. 严格架构

强制完全控制数据结构：

```python
# Define all allowed features
all_features = [
    ln.Feature.get(name="cell_type"),
    ln.Feature.get(name="tissue"),
    ln.Feature.get(name="donor_id"),
    ln.Feature.get(name="disease")
]

# Create strict schema
schema = ln.Schema(
    name="strict_immune_schema",
    features=all_features,
    flexible=False  # No additional columns allowed
).save()
```

## 数据帧管理工作流程

典型的管理过程涉及六个关键步骤：

### 步骤 1-2：加载数据并建立注册表

```python
import pandas as pd
import lamindb as ln

# Load data
df = pd.read_csv("experiment.csv")

# Define and save features
ln.Feature(name="cell_type", dtype=str).save()
ln.Feature(name="tissue", dtype=str).save()
ln.Feature(name="gene_count", dtype=int).save()
ln.Feature(name="experiment_date", dtype="date").save()

# Populate valid values (if using controlled vocabulary)
import bionty as bt
bt.CellType.import_source()
bt.Tissue.import_source()
```

### 步骤 3：创建架构

```python
# Link features to schema
features = [
    ln.Feature.get(name="cell_type"),
    ln.Feature.get(name="tissue"),
    ln.Feature.get(name="gene_count"),
    ln.Feature.get(name="experiment_date")
]

schema = ln.Schema(
    name="experiment_schema",
    features=features,
    flexible=True
).save()
```

### 步骤 4：初始化 Curator 和验证

```python
# Initialize curator
curator = ln.curators.DataFrameCurator(df, schema)

# Validate dataset
validation = curator.validate()

# Check validation results
if validation:
    print("✓ Validation passed")
else:
    print("✗ Validation failed")
    curator.non_validated  # See problematic fields
```

### 步骤 5：修复验证问题

#### 标准化值

```python
# Fix typos and synonyms in categorical columns
curator.cat.standardize("cell_type")
curator.cat.standardize("tissue")

# View standardization mapping
curator.cat.inspect_standardize("cell_type")
```

#### 映射到本体

```python
# Map values to ontology terms
curator.cat.add_ontology("cell_type", bt.CellType)
curator.cat.add_ontology("tissue", bt.Tissue)

# Look up public ontologies for unmapped terms
curator.cat.lookup(public=True).cell_type  # Interactive lookup
```

#### 添加新术语

```python
# Add new valid terms to registry
curator.cat.add_new_from("cell_type")

# Or manually create records
new_cell_type = bt.CellType(name="my_novel_cell_type").save()
```

#### 重命名列

```python
# Rename columns to match feature names
df = df.rename(columns={"celltype": "cell_type"})

# Re-initialize curator with fixed DataFrame
curator = ln.curators.DataFrameCurator(df, schema)
```

### 第6步：保存精选Artifact

```python
# Save with schema linkage
artifact = curator.save_artifact(
    key="experiments/curated_data.parquet",
    description="Validated and annotated experimental data"
)

# Verify artifact has schema
artifact.schema  # Returns the schema object
artifact.describe()  # Shows validation status
```

## AnnData Curation

对于像AnnData这样的复合结构，使用“槽”来验证不同的组件：

### 定义AnnData Schemas

```python
# Create schemas for different slots
obs_schema = ln.Schema(
    name="cell_metadata",
    features=[
        ln.Feature.get(name="cell_type"),
        ln.Feature.get(name="tissue"),
        ln.Feature.get(name="donor_id")
    ]
).save()

var_schema = ln.Schema(
    name="gene_ids",
    features=[ln.Feature.get(name="ensembl_gene_id")]
).save()

# Create composite AnnData schema
anndata_schema = ln.Schema(
    name="scrna_schema",
    otype="AnnData",
    slots={
        "obs": obs_schema,
        "var.T": var_schema  # .T indicates transposition
    }
).save()
```

### 管理 AnnData 对象

```python
import anndata as ad

# Load AnnData
adata = ad.read_h5ad("data.h5ad")

# Initialize curator
curator = ln.curators.AnnDataCurator(adata, anndata_schema)

# Validate all slots
validation = curator.validate()

# Fix issues by slot
curator.cat.standardize("obs", "cell_type")
curator.cat.add_ontology("obs", "cell_type", bt.CellType)
curator.cat.standardize("var.T", "ensembl_gene_id")

# Save curated artifact
artifact = curator.save_artifact(
    key="scrna/validated_data.h5ad",
    description="Curated single-cell RNA-seq data"
)
```

## MuData Curation

MuData 通过特定于模态的方式支持多模态数据插槽：

```python
# Define schemas for each modality
rna_obs_schema = ln.Schema(name="rna_obs_schema", features=[...]).save()
protein_obs_schema = ln.Schema(name="protein_obs_schema", features=[...]).save()

# Create MuData schema
mudata_schema = ln.Schema(
    name="multimodal_schema",
    otype="MuData",
    slots={
        "rna:obs": rna_obs_schema,
        "protein:obs": protein_obs_schema
    }
).save()

# Curate
curator = ln.curators.MuDataCurator(mdata, mudata_schema)
curator.validate()
```

## SpatialData Curation

对于空间转录组数据：

```python
# Define spatial schema
spatial_schema = ln.Schema(
    name="spatial_schema",
    otype="SpatialData",
    slots={
        "tables:cell_metadata.obs": cell_schema,
        "attrs:bio": bio_metadata_schema
    }
).save()

# Curate
curator = ln.curators.SpatialDataCurator(sdata, spatial_schema)
curator.validate()
```

## TileDB-SOMA Curation

对于可扩展的数组支持的数据：

```python
# Define SOMA schema
soma_schema = ln.Schema(
    name="soma_schema",
    otype="tiledbsoma",
    slots={
        "obs": obs_schema,
        "ms:RNA.T": var_schema  # measurement:modality.T
    }
).save()

# Curate
curator = ln.curators.TileDBSOMACurator(soma_exp, soma_schema)
curator.validate()
```

## 功能验证

### 数据类型验证

```python
# Define typed features
ln.Feature(name="age", dtype=int).save()
ln.Feature(name="weight", dtype=float).save()
ln.Feature(name="is_treated", dtype=bool).save()
ln.Feature(name="collection_date", dtype="date").save()

# Coerce types during validation
ln.Feature(name="age_str", dtype=int, coerce_dtype=True).save()  # Auto-convert strings to int
```

### 值验证

```python
# Validate against allowed values
cell_type_feature = ln.Feature(name="cell_type", dtype=str).save()

# Link to registry for controlled vocabulary
cell_type_feature.link_to_registry(bt.CellType)

# Now validation checks against CellType registry
curator = ln.curators.DataFrameCurator(df, schema)
curator.validate()  # Errors if cell_type values not in registry
```

## 标准化策略

### 使用公共本体

```python
# Look up standardized terms from public sources
curator.cat.lookup(public=True).cell_type

# Returns auto-complete object with public ontology terms
# User can select correct term interactively
```

### 同义词映射

```python
# Add synonyms to records
t_cell = bt.CellType.get(name="T cell")
t_cell.add_synonym("T lymphocyte")
t_cell.add_synonym("T-cell")

# Now standardization maps synonyms automatically
curator.cat.standardize("cell_type")
# "T lymphocyte" → "T cell"
# "T-cell" → "T cell"
```

### 自定义标准化

```python
# Manual mapping
mapping = {
    "TCell": "T cell",
    "t cell": "T cell",
    "T-cells": "T cell"
}

# Apply mapping
df["cell_type"] = df["cell_type"].map(lambda x: mapping.get(x, x))
```

## 处理验证错误

### 常见问题和解决方案

* *问题：列不在架构中**
```python
# Solution 1: Rename column
df = df.rename(columns={"old_name": "feature_name"})

# Solution 2: Add feature to schema
new_feature = ln.Feature(name="new_column", dtype=str).save()
schema.features.add(new_feature)
```

* *问题：无效值**
```python
# Solution 1: Standardize
curator.cat.standardize("column_name")

# Solution 2: Add new valid values
curator.cat.add_new_from("column_name")

# Solution 3: Map to ontology
curator.cat.add_ontology("column_name", bt.Registry)
```

* *问题：数据类型不匹配**
```python
# Solution 1: Convert data type
df["column"] = df["column"].astype(int)

# Solution 2: Enable coercion in feature
feature = ln.Feature.get(name="column")
feature.coerce_dtype = True
feature.save()
```

## 架构版本控制

架构可以像其他记录一样进行版本控制：

```python
# Create initial schema
schema_v1 = ln.Schema(name="experiment_schema", features=[...]).save()

# Update schema with new features
schema_v2 = ln.Schema(
    name="experiment_schema",
    features=[...],  # Updated list
    version="2"
).save()

# Link artifacts to specific schema versions
artifact.schema = schema_v2
artifact.save()
```

## 查询验证数据

一旦数据被验证和注释，它就变成可查询：

```python
# Find all validated artifacts
ln.Artifact.filter(is_valid=True).to_dataframe()

# Find artifacts with specific schema
ln.Artifact.filter(schema=schema).to_dataframe()

# Query by annotated features
ln.Artifact.filter(cell_type="T cell", tissue="blood").to_dataframe()

# Include features in results
ln.Artifact.filter(is_valid=True).to_dataframe(include="features")
```

## 最佳实践

1. **首先定义功能**：在 curation
2 之前创建功能注册表。 **使用公共本体**：利用 bt.lookup(public=True)进行标准化
3. **开始灵活**：首先使用灵活的模式，随着理解的增长而收紧
4. **文档槽**：在复合模式
5中明确指定转置（.T）。 **尽早标准化**：在验证之前修复拼写错误和同义词
6. **增量验证**：分别检查每个插槽的复合结构
7. **版本架构**：跟踪架构随时间的变化
8. **添加同义词**：注册常见变体以简化未来的管理
9. **谨慎强制类型**：仅在 safe
10 时启用 dtype 强制。 **样本测试**：在完整数据集管理之前验证小子集

## 高级：自定义验证器

创建自定义验证逻辑：

```python
def validate_gene_expression(df):
    """Custom validator for gene expression values."""
    # Check non-negative
    if (df < 0).any().any():
        return False, "Negative expression values found"

    # Check reasonable range
    if (df > 1e6).any().any():
        return False, "Unreasonably high expression values"

    return True, "Valid"

# Apply during curation
is_valid, message = validate_gene_expression(df)
if not is_valid:
    print(f"Validation failed: {message}")
```

## 跟踪管理来源

```python
# Curated artifacts track curation lineage
ln.track()  # Start tracking

# Perform curation
curator = ln.curators.DataFrameCurator(df, schema)
curator.validate()
curator.cat.standardize("cell_type")
artifact = curator.save_artifact(key="curated.parquet")

ln.finish()  # Complete tracking

# View curation lineage
artifact.run.describe()  # Shows curation transform
artifact.view_lineage()  # Visualizes curation process
```
