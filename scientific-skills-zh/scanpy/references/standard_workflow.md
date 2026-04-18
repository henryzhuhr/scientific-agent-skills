# 单细胞分析的标准 Scanpy 工作流程

本文档概述了使用 scanpy 分析单细胞 RNA-seq 数据的标准工作流程。

## 完整分析流程

### 1. 数据加载和初始设置

```python
import scanpy as sc
import pandas as pd
import numpy as np

# Configure scanpy settings
sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
sc.settings.set_figure_params(dpi=80, facecolor='white')

# Load data (various formats)
adata = sc.read_10x_mtx('path/to/data/')  # For 10X data
# adata = sc.read_h5ad('path/to/data.h5ad')  # For h5ad format
# adata = sc.read_csv('path/to/data.csv')  # For CSV format
```

### 2. 质量控制（QC）

```python
# Calculate QC metrics
sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)

# Common filtering thresholds (adjust based on dataset)
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)

# Remove cells with high mitochondrial content
adata = adata[adata.obs.pct_counts_mt < 5, :]

# Visualize QC metrics
sc.pl.violin(adata, ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'],
             jitter=0.4, multi_panel=True)
sc.pl.scatter(adata, x='total_counts', y='pct_counts_mt')
sc.pl.scatter(adata, x='total_counts', y='n_genes_by_counts')
```

### 3. 归一化

```python
# Normalize to 10,000 counts per cell
sc.pp.normalize_total(adata, target_sum=1e4)

# Log-transform the data
sc.pp.log1p(adata)

# Store normalized data in raw for later use
adata.raw = adata
```

### 4. 特征选择

```python
# Identify highly variable genes
sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)

# Visualize highly variable genes
sc.pl.highly_variable_genes(adata)

# Subset to highly variable genes
adata = adata[:, adata.var.highly_variable]
```

### 5. 缩放和缩放回归

```python
# Regress out effects of total counts per cell and percent mitochondrial genes
sc.pp.regress_out(adata, ['total_counts', 'pct_counts_mt'])

# Scale data to unit variance and zero mean
sc.pp.scale(adata, max_value=10)
```

### 6.降维

```python
# Principal Component Analysis (PCA)
sc.tl.pca(adata, svd_solver='arpack')

# Visualize PCA results
sc.pl.pca(adata, color='CST3')
sc.pl.pca_variance_ratio(adata, log=True)

# Computing neighborhood graph
sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)

# UMAP for visualization
sc.tl.umap(adata)

# t-SNE (alternative to UMAP)
# sc.tl.tsne(adata)
```

### 7.聚类

```python
# Leiden clustering (recommended)
sc.tl.leiden(adata, resolution=0.5)

# Alternative: Louvain clustering
# sc.tl.louvain(adata, resolution=0.5)

# Visualize clustering results
sc.pl.umap(adata, color=['leiden'], legend_loc='on data')
```

### 8.标记基因识别

```python
# Find marker genes for each cluster
sc.tl.rank_genes_groups(adata, 'leiden', method='wilcoxon')

# Visualize top marker genes
sc.pl.rank_genes_groups(adata, n_genes=25, sharey=False)

# Get marker gene dataframe
marker_genes = sc.get.rank_genes_groups_df(adata, group='0')

# Visualize specific markers
sc.pl.umap(adata, color=['leiden', 'CST3', 'NKG7'])
```

### 9. 单元类型注释

```python
# Manual annotation based on marker genes
cluster_annotations = {
    '0': 'CD4 T cells',
    '1': 'CD14+ Monocytes',
    '2': 'B cells',
    '3': 'CD8 T cells',
    # ... add more annotations
}
adata.obs['cell_type'] = adata.obs['leiden'].map(cluster_annotations)

# Visualize annotated cell types
sc.pl.umap(adata, color='cell_type', legend_loc='on data')
```

### 10. 保存结果

```python
# Save the processed AnnData object
adata.write('results/processed_data.h5ad')

# Export results to CSV
adata.obs.to_csv('results/cell_metadata.csv')
adata.var.to_csv('results/gene_metadata.csv')
```

## 附加分析选项

### 轨迹推理

```python
# PAGA (Partition-based graph abstraction)
sc.tl.paga(adata, groups='leiden')
sc.pl.paga(adata, color=['leiden'])

# Diffusion pseudotime (DPT)
adata.uns['iroot'] = np.flatnonzero(adata.obs['leiden'] == '0')[0]
sc.tl.dpt(adata)
sc.pl.umap(adata, color=['dpt_pseudotime'])
```

### 条件之间的差异表达

```python
# Compare conditions within a cell type
sc.tl.rank_genes_groups(adata, groupby='condition', groups=['treated'],
                         reference='control', method='wilcoxon')
sc.pl.rank_genes_groups(adata, groups=['treated'])
```

### 基因集评分

```python
# Score cells for gene set expression
gene_set = ['CD3D', 'CD3E', 'CD3G']
sc.tl.score_genes(adata, gene_set, score_name='T_cell_score')
sc.pl.umap(adata, color='T_cell_score')
```

## 常用参数调整

- **QC阈值**：`min_genes`、`min_cells`、`pct_counts_mt` - 取决于数据集质量
- **标准化目标**：通常为 1e4，但可以调整
- **HVG 参数**：影响特征选择严格性
- **PCA 组件**：检查方差比图以确定最佳值number
- **聚类分辨率**：值越高，聚类越多（通常为 0.4-1.2）
- **n_neighbors**：影响 UMAP 和聚类的粒度（通常为 10-30）

## 最佳实践

1. 在过滤之前始终可视化 QC 指标
2. 标准化前保存原始计数 (`adata.raw = adata`)
3. 使用Leiden代替Louvain进行聚类（效率更高）
4. 尝试多种聚类分辨率以找到最佳粒度
5. 使用已知标记基因
6 验证细胞类型注释。保存关键步骤的中间结果
