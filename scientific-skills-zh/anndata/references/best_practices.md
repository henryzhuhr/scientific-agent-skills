# 最佳实践

高效且有效地使用AnnData.

## 内存管理

### 对稀疏数据使用稀疏矩阵
```python
import numpy as np
from scipy.sparse import csr_matrix
import anndata as ad

# Check data sparsity
data = np.random.rand(1000, 2000)
sparsity = 1 - np.count_nonzero(data) / data.size
print(f"Sparsity: {sparsity:.2%}")

# Convert to sparse if >50% zeros
if sparsity > 0.5:
    adata = ad.AnnData(X=csr_matrix(data))
else:
    adata = ad.AnnData(X=data)

# Benefits: 10-100x memory reduction for sparse genomics data
```

### 将字符串转换为分类
```python
# Inefficient: string columns use lots of memory
adata.obs['cell_type'] = ['Type_A', 'Type_B', 'Type_C'] * 333 + ['Type_A']

# Efficient: convert to categorical
adata.obs['cell_type'] = adata.obs['cell_type'].astype('category')

# Convert all string columns
adata.strings_to_categoricals()

# Benefits: 10-50x memory reduction for repeated strings
```

### 对大型数据集使用支持模式
```python
# Don't load entire dataset into memory
adata = ad.read_h5ad('large_dataset.h5ad', backed='r')

# Work with metadata
filtered = adata[adata.obs['quality'] > 0.8]

# Load only filtered subset
adata_subset = filtered.to_memory()

# Benefits: Work with datasets larger than RAM
```

## 视图与副本

### 了解视图
```python
# Subsetting creates a view by default
subset = adata[0:100, :]
print(subset.is_view)  # True

# Views don't copy data (memory efficient)
# But modifications can affect original

# Check if object is a view
if adata.is_view:
    adata = adata.copy()  # Make independent
```

### 何时使用视图
```python
# Good: Read-only operations on subsets
mean_expr = adata[adata.obs['cell_type'] == 'T cell'].X.mean()

# Good: Temporary analysis
temp_subset = adata[:100, :]
result = analyze(temp_subset.X)
```

### 何时使用副本
```python
# Create independent copy for modifications
adata_filtered = adata[keep_cells, :].copy()

# Safe to modify without affecting original
adata_filtered.obs['new_column'] = values

# Always copy when:
# - Storing subset for later use
# - Modifying subset data
# - Passing to function that modifies data
```

## 数据存储最佳实践

### 选择正确的格式

* *H5AD (HDF5) - 默认选择**
```python
adata.write_h5ad('data.h5ad', compression='gzip')
```
- 快速随机访问
- 支持备份模式
- 良好的压缩
- 最适合：大多数用例

* *Zarr - 云和并行访问**
```python
adata.write_zarr('data.zarr', chunks=(100, 100))
```
- 非常适合云存储（S3、 GCS)
- 支持并行 I/O
- 良好的压缩
- 最适合：大型数据集、云工作流程、并行处理

* *CSV - 互操作性**
```python
adata.write_csvs('output_dir/')
```
- 人类可读
- 与所有工具兼容
- 文件大小大，速度慢
- 最适合：与非Python 工具、小数据集共享

### 优化文件size
```python
# Before saving, optimize:

# 1. Convert to sparse if appropriate
from scipy.sparse import csr_matrix, issparse
if not issparse(adata.X):
    density = np.count_nonzero(adata.X) / adata.X.size
    if density < 0.5:
        adata.X = csr_matrix(adata.X)

# 2. Convert strings to categoricals
adata.strings_to_categoricals()

# 3. Use compression
adata.write_h5ad('data.h5ad', compression='gzip', compression_opts=9)

# Typical results: 5-20x file size reduction
```

## 支持模式策略

### 只读分析
```python
# Open in read-only backed mode
adata = ad.read_h5ad('data.h5ad', backed='r')

# Perform filtering without loading data
high_quality = adata[adata.obs['quality_score'] > 0.8]

# Load only filtered data
adata_filtered = high_quality.to_memory()
```

### 读写修改
```python
# Open in read-write backed mode
adata = ad.read_h5ad('data.h5ad', backed='r+')

# Modify metadata (written to disk)
adata.obs['new_annotation'] = values

# X remains on disk, modifications saved immediately
```

### 分块处理
```python
# Process large dataset in chunks
adata = ad.read_h5ad('huge_dataset.h5ad', backed='r')

results = []
chunk_size = 1000

for i in range(0, adata.n_obs, chunk_size):
    chunk = adata[i:i+chunk_size, :].to_memory()
    result = process(chunk)
    results.append(result)

final_result = combine(results)
```

## 性能优化

### 取子集性能
```python
# Fast: Boolean indexing with arrays
mask = np.array(adata.obs['quality'] > 0.5)
subset = adata[mask, :]

# Slow: Boolean indexing with Series (creates view chain)
subset = adata[adata.obs['quality'] > 0.5, :]

# Fastest: Integer indices
indices = np.where(adata.obs['quality'] > 0.5)[0]
subset = adata[indices, :]
```

### 避免重复取子
```python
# Inefficient: Multiple subset operations
for cell_type in ['A', 'B', 'C']:
    subset = adata[adata.obs['cell_type'] == cell_type]
    process(subset)

# Efficient: Group and process
groups = adata.obs.groupby('cell_type').groups
for cell_type, indices in groups.items():
    subset = adata[indices, :]
    process(subset)
```

### 对大数据使用分块操作矩阵
```python
# Process X in chunks
for chunk in adata.chunked_X(chunk_size=1000):
    result = compute(chunk)

# More memory efficient than loading full X
```

## 使用原始数据

### 在过滤之前存储原始数据
```python
# Original data with all genes
adata = ad.AnnData(X=counts)

# Store raw before filtering
adata.raw = adata.copy()

# Filter to highly variable genes
adata = adata[:, adata.var['highly_variable']]

# Later: access original data
original_expression = adata.raw.X
all_genes = adata.raw.var_names
```

### 何时使用原始数据
```python
# Use raw for:
# - Differential expression on filtered genes
# - Visualization of specific genes not in filtered set
# - Accessing original counts after normalization

# Access raw data
if adata.raw is not None:
    gene_expr = adata.raw[:, 'GENE_NAME'].X
else:
    gene_expr = adata[:, 'GENE_NAME'].X
```

## 元数据管理

### 命名约定
```python
# Consistent naming improves usability

# Observation metadata (obs):
# - cell_id, sample_id
# - cell_type, tissue, condition
# - n_genes, n_counts, percent_mito
# - cluster, leiden, louvain

# Variable metadata (var):
# - gene_id, gene_name
# - highly_variable, n_cells
# - mean_expression, dispersion

# Embeddings (obsm):
# - X_pca, X_umap, X_tsne
# - X_diffmap, X_draw_graph_fr

# Follow conventions from scanpy/scverse ecosystem
```

### 文档元数据
```python
# Store metadata descriptions in uns
adata.uns['metadata_descriptions'] = {
    'cell_type': 'Cell type annotation from automated clustering',
    'quality_score': 'QC score from scrublet (0-1, higher is better)',
    'batch': 'Experimental batch identifier'
}

# Store processing history
adata.uns['processing_steps'] = [
    'Raw counts loaded from 10X',
    'Filtered: n_genes > 200, n_counts < 50000',
    'Normalized to 10000 counts per cell',
    'Log transformed'
]
```

## 再现性

### 设置随机seeds
```python
import numpy as np

# Set seed for reproducible results
np.random.seed(42)

# Document in uns
adata.uns['random_seed'] = 42
```

### 存储参数
```python
# Store analysis parameters in uns
adata.uns['pca'] = {
    'n_comps': 50,
    'svd_solver': 'arpack',
    'random_state': 42
}

adata.uns['neighbors'] = {
    'n_neighbors': 15,
    'n_pcs': 50,
    'metric': 'euclidean',
    'method': 'umap'
}
```

### 版本跟踪
```python
import anndata
import scanpy
import numpy

# Store versions
adata.uns['versions'] = {
    'anndata': anndata.__version__,
    'scanpy': scanpy.__version__,
    'numpy': numpy.__version__,
    'python': sys.version
}
```

## 错误处理

### 检查数据有效性
```python
# Verify dimensions
assert adata.n_obs == len(adata.obs)
assert adata.n_vars == len(adata.var)
assert adata.X.shape == (adata.n_obs, adata.n_vars)

# Check for NaN values
has_nan = np.isnan(adata.X.data).any() if issparse(adata.X) else np.isnan(adata.X).any()
if has_nan:
    print("Warning: Data contains NaN values")

# Check for negative values (if counts expected)
has_negative = (adata.X.data < 0).any() if issparse(adata.X) else (adata.X < 0).any()
if has_negative:
    print("Warning: Data contains negative values")
```

### 验证元数据
```python
# Check for missing values
missing_obs = adata.obs.isnull().sum()
if missing_obs.any():
    print("Missing values in obs:")
    print(missing_obs[missing_obs > 0])

# Verify indices are unique
assert adata.obs_names.is_unique, "Observation names not unique"
assert adata.var_names.is_unique, "Variable names not unique"

# Check metadata alignment
assert len(adata.obs) == adata.n_obs
assert len(adata.var) == adata.n_vars
```

## 与其他工具集成

### Scanpy 集成
```python
import scanpy as sc

# AnnData is native format for scanpy
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata)
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)
```

### Pandas 集成
```python
import pandas as pd

# Convert to DataFrame
df = adata.to_df()

# Create from DataFrame
adata = ad.AnnData(df)

# Work with metadata as DataFrames
adata.obs = adata.obs.merge(external_metadata, left_index=True, right_index=True)
```

### PyTorch 集成
```python
from anndata.experimental import AnnLoader

# Create PyTorch DataLoader
dataloader = AnnLoader(adata, batch_size=128, shuffle=True)

# Iterate in training loop
for batch in dataloader:
    X = batch.X
    # Train model on batch
```

## 常见陷阱

### 陷阱 1：修改views
```python
# Wrong: Modifying view can affect original
subset = adata[:100, :]
subset.X = new_data  # May modify adata.X!

# Correct: Copy before modifying
subset = adata[:100, :].copy()
subset.X = new_data  # Independent copy
```

### 陷阱 2：索引未对齐
```python
# Wrong: Assuming order matches
external_data = pd.read_csv('data.csv')
adata.obs['new_col'] = external_data['values']  # May misalign!

# Correct: Align on index
adata.obs['new_col'] = external_data.set_index('cell_id').loc[adata.obs_names, 'values']
```

### 陷阱 3：混合稀疏和密集
```python
# Wrong: Converting sparse to dense uses huge memory
result = adata.X + 1  # Converts sparse to dense!

# Correct: Use sparse operations
from scipy.sparse import issparse
if issparse(adata.X):
    result = adata.X.copy()
    result.data += 1
```

### 陷阱 4：不处理视图
```python
# Wrong: Assuming subset is independent
subset = adata[mask, :]
del adata  # subset may become invalid!

# Correct: Copy when needed
subset = adata[mask, :].copy()
del adata  # subset remains valid
```

### 陷阱5：忽略内存限制
```python
# Wrong: Loading huge dataset into memory
adata = ad.read_h5ad('100GB_file.h5ad')  # OOM error!

# Correct: Use backed mode
adata = ad.read_h5ad('100GB_file.h5ad', backed='r')
subset = adata[adata.obs['keep']].to_memory()
```

## 工作流程示例

完整的最佳实践工作流程：

```python
import anndata as ad
import numpy as np
from scipy.sparse import csr_matrix

# 1. Load with backed mode if large
adata = ad.read_h5ad('data.h5ad', backed='r')

# 2. Quick metadata check without loading data
print(f"Dataset: {adata.n_obs} cells × {adata.n_vars} genes")

# 3. Filter based on metadata
high_quality = adata[adata.obs['quality_score'] > 0.8]

# 4. Load filtered subset to memory
adata = high_quality.to_memory()

# 5. Convert to optimal storage types
adata.strings_to_categoricals()
if not issparse(adata.X):
    density = np.count_nonzero(adata.X) / adata.X.size
    if density < 0.5:
        adata.X = csr_matrix(adata.X)

# 6. Store raw before filtering genes
adata.raw = adata.copy()

# 7. Filter to highly variable genes
adata = adata[:, adata.var['highly_variable']].copy()

# 8. Document processing
adata.uns['processing'] = {
    'filtered': 'quality_score > 0.8',
    'n_hvg': adata.n_vars,
    'date': '2025-11-03'
}

# 9. Save optimized
adata.write_h5ad('processed.h5ad', compression='gzip')
```
