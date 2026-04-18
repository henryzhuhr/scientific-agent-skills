---
name: anndata
description: 单细胞分析中带注释矩阵的数据结构。在处理 .h5ad 文件或与 scverse 生态系统集成时使用。这是数据格式技巧——对于分析工作流程使用scanpy；对于概率模型，使用 scvi-tools；对于人口规模查询，请使用 cellxgene-census。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# AnnData

## 概述

AnnData 是一个 Python 包，用于处理带注释的数据矩阵、存储实验测量值 (X)以及观测元数据 (obs)、变量元数据 (var)和多维注释（obsm、varm、obsp、varp、uns）。它最初是通过 Scanpy 为单细胞基因组学设计的，现在可作为任何需要高效存储、操作和分析的注释数据的通用框架。

## 何时使用此技能

在以下情况下使用此技能：
- 创建、读取或写入 AnnData 对象
- 使用 h5ad、zarr 或其他基因组学数据格式
- 执行单细胞RNA-seq 分析
- 使用稀疏矩阵或支持模式管理大型数据集
- 连接多个数据集或实验批次
- 子集化、过滤或转换注释数据
- 与scanpy 集成， scvi-tools，或其他scverse生态系统工具

## 安装

```bash
uv pip install anndata

# With optional dependencies
uv pip install anndata[dev,test,doc]
```

## 快速入门

### 创建AnnData 对象
```python
import anndata as ad
import numpy as np
import pandas as pd

# Minimal creation
X = np.random.rand(100, 2000)  # 100 cells × 2000 genes
adata = ad.AnnData(X)

# With metadata
obs = pd.DataFrame({
    'cell_type': ['T cell', 'B cell'] * 50,
    'sample': ['A', 'B'] * 50
}, index=[f'cell_{i}' for i in range(100)])

var = pd.DataFrame({
    'gene_name': [f'Gene_{i}' for i in range(2000)]
}, index=[f'ENSG{i:05d}' for i in range(2000)])

adata = ad.AnnData(X=X, obs=obs, var=var)
```

### 读取数据
```python
# Read h5ad file
adata = ad.read_h5ad('data.h5ad')

# Read with backed mode (for large files)
adata = ad.read_h5ad('large_data.h5ad', backed='r')

# Read other formats
adata = ad.read_csv('data.csv')
adata = ad.read_loom('data.loom')
adata = ad.read_10x_h5('filtered_feature_bc_matrix.h5')
```

### 写入数据
```python
# Write h5ad file
adata.write_h5ad('output.h5ad')

# Write with compression
adata.write_h5ad('output.h5ad', compression='gzip')

# Write other formats
adata.write_zarr('output.zarr')
adata.write_csvs('output_dir/')
```

### 基本操作
```python
# Subset by conditions
t_cells = adata[adata.obs['cell_type'] == 'T cell']

# Subset by indices
subset = adata[0:50, 0:100]

# Add metadata
adata.obs['quality_score'] = np.random.rand(adata.n_obs)
adata.var['highly_variable'] = np.random.rand(adata.n_vars) > 0.8

# Access dimensions
print(f"{adata.n_obs} observations × {adata.n_vars} variables")
```

## 核心能力

### 1.数据结构

了解AnnData对象结构包括X、obs、var、layers、obsm、varm、 obsp、varp、uns 和 raw 组件。

* *请参阅**：`references/data_structure.md` 了解有关以下内容的全面信息：
- 核心组件（X、obs、var、layers、obsm、varm、obsp、varp、uns、raw）
- 从各种来源创建 AnnData 对象
- 访问和操作数据组件
- 内存高效实践

### 2. 输入/输出操作

以各种格式读写数据，支持压缩、备份模式和云存储。

* *参见**：`references/io_operations.md`，了解有关以下内容的详细信息：
- 本机格式（h5ad、zarr）
- 替代格式（CSV、MTX、Loom、10X、Excel）
- 大型数据集的支持模式
- 远程数据访问
- 格式转换
- 性能优化

常用命令：
```python
# Read/write h5ad
adata = ad.read_h5ad('data.h5ad', backed='r')
adata.write_h5ad('output.h5ad', compression='gzip')

# Read 10X data
adata = ad.read_10x_h5('filtered_feature_bc_matrix.h5')

# Read MTX format
adata = ad.read_mtx('matrix.mtx').T
```

### 3.串联

使用灵活的连接策略沿着观测值或变量组合多个AnnData对象。

* *参见**：`references/concatenation.md`全面覆盖：
- 基本串联（对于观察，axis=0，对于变量，axis=1）
- 连接类型（内部、外部）
- 合并策略（相同、唯一、第一个、仅）
- 带标签的跟踪数据源
- 延迟串联 (AnnCollection)
- 大型磁盘串联数据集

常用命令：
```python
# Concatenate observations (combine samples)
adata = ad.concat(
    [adata1, adata2, adata3],
    axis=0,
    join='inner',
    label='batch',
    keys=['batch1', 'batch2', 'batch3']
)

# Concatenate variables (combine modalities)
adata = ad.concat([adata_rna, adata_protein], axis=1)

# Lazy concatenation
from anndata.experimental import AnnCollection
collection = AnnCollection(
    ['data1.h5ad', 'data2.h5ad'],
    join_obs='outer',
    label='dataset'
)
```

### 4.数据操作

高效地转换、子集、过滤和重新组织数据。

* *参见**：`references/manipulation.md`，了解有关以下内容的详细指导：
- 子集（按索引、名称、布尔掩码、元数据条件）
- 转置
- 复制（完整副本与视图）
- 重命名（观察、变量、类别）
- 类型转换（字符串到分类，稀疏/密集）
- 添加/删除数据组件
- 重新排序
- 质量控制过滤

 常用命令：
```python
# Subset by metadata
filtered = adata[adata.obs['quality_score'] > 0.8]
hv_genes = adata[:, adata.var['highly_variable']]

# Transpose
adata_T = adata.T

# Copy vs view
view = adata[0:100, :]  # View (lightweight reference)
copy = adata[0:100, :].copy()  # Independent copy

# Convert strings to categoricals
adata.strings_to_categoricals()
```

### 5. 最佳实践

遵循内存效率、性能和性能方面的推荐模式

* *请参阅**：`references/best_practices.md` 了解以下方面的指南：
- 内存管理（稀疏矩阵、分类、支持模式）
- 视图与副本
- 数据存储优化
- 性能优化
- 使用原始数据data
- 元数据管理
- 再现性
- 错误处理
- 与其他工具集成
- 常见陷阱和解决方案

主要建议：
```python
# Use sparse matrices for sparse data
from scipy.sparse import csr_matrix
adata.X = csr_matrix(adata.X)

# Convert strings to categoricals
adata.strings_to_categoricals()

# Use backed mode for large files
adata = ad.read_h5ad('large.h5ad', backed='r')

# Store raw before filtering
adata.raw = adata.copy()
adata = adata[:, adata.var['highly_variable']]
```

## 与Scverse 集成生态系统

AnnData 作为 scverse 生态系统的基础数据结构：

### Scanpy（单细胞分析）
```python
import scanpy as sc

# Preprocessing
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)

# Dimensionality reduction
sc.pp.pca(adata, n_comps=50)
sc.pp.neighbors(adata, n_neighbors=15)
sc.tl.umap(adata)
sc.tl.leiden(adata)

# Visualization
sc.pl.umap(adata, color=['cell_type', 'leiden'])
```

### Muon（多模态数据）
```python
import muon as mu

# Combine RNA and protein data
mdata = mu.MuData({'rna': adata_rna, 'protein': adata_protein})
```

### PyTorch集成
```python
from anndata.experimental import AnnLoader

# Create DataLoader for deep learning
dataloader = AnnLoader(adata, batch_size=128, shuffle=True)

for batch in dataloader:
    X = batch.X
    # Train model
```

## 常用工作流程

### 单细胞RNA测序分析
```python
import anndata as ad
import scanpy as sc

# 1. Load data
adata = ad.read_10x_h5('filtered_feature_bc_matrix.h5')

# 2. Quality control
adata.obs['n_genes'] = (adata.X > 0).sum(axis=1)
adata.obs['n_counts'] = adata.X.sum(axis=1)
adata = adata[adata.obs['n_genes'] > 200]
adata = adata[adata.obs['n_counts'] < 50000]

# 3. Store raw
adata.raw = adata.copy()

# 4. Normalize and filter
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var['highly_variable']]

# 5. Save processed data
adata.write_h5ad('processed.h5ad')
```

### 批量集成
```python
# Load multiple batches
adata1 = ad.read_h5ad('batch1.h5ad')
adata2 = ad.read_h5ad('batch2.h5ad')
adata3 = ad.read_h5ad('batch3.h5ad')

# Concatenate with batch labels
adata = ad.concat(
    [adata1, adata2, adata3],
    label='batch',
    keys=['batch1', 'batch2', 'batch3'],
    join='inner'
)

# Apply batch correction
import scanpy as sc
sc.pp.combat(adata, key='batch')

# Continue analysis
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)
```

### 使用大型数据集
```python
# Open in backed mode
adata = ad.read_h5ad('100GB_dataset.h5ad', backed='r')

# Filter based on metadata (no data loading)
high_quality = adata[adata.obs['quality_score'] > 0.8]

# Load filtered subset
adata_subset = high_quality.to_memory()

# Process subset
process(adata_subset)

# Or process in chunks
chunk_size = 1000
for i in range(0, adata.n_obs, chunk_size):
    chunk = adata[i:i+chunk_size, :].to_memory()
    process(chunk)
```

## 故障排除

### 内存不足错误
使用支持模式或转换为稀疏矩阵：
```python
# Backed mode
adata = ad.read_h5ad('file.h5ad', backed='r')

# Sparse matrices
from scipy.sparse import csr_matrix
adata.X = csr_matrix(adata.X)
```

### 文件读取速度慢
使用压缩和适当的格式：
```python
# Optimize for storage
adata.strings_to_categoricals()
adata.write_h5ad('file.h5ad', compression='gzip')

# Use Zarr for cloud storage
adata.write_zarr('file.zarr', chunks=(1000, 1000))
```

### 索引对齐问题
始终对齐索引上的外部数据：
```python
# Wrong
adata.obs['new_col'] = external_data['values']

# Correct
adata.obs['new_col'] = external_data.set_index('cell_id').loc[adata.obs_names, 'values']
```

## 其他资源

- **官方文档**： https://anndata.readthedocs.io/
- **Scanpy 教程**：https://scanpy.readthedocs.io/
- **Scverse 生态系统**：https://scverse.org/
- **GitHub 存储库**：https://github.com/scverse/anndata
