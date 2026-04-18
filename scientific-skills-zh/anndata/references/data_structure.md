# AnnData 对象结构

AnnData 对象存储带有关联注释的数据矩阵，为管理实验数据和元数据提供灵活的框架。

## 核心组件

### X (Data Matrix)
形状为 (n_obs, n_vars)存储实验的主数据矩阵测量值。

```python
import anndata as ad
import numpy as np

# Create with dense array
adata = ad.AnnData(X=np.random.rand(100, 2000))

# Create with sparse matrix (recommended for large, sparse data)
from scipy.sparse import csr_matrix
sparse_data = csr_matrix(np.random.rand(100, 2000))
adata = ad.AnnData(X=sparse_data)
```

访问数据：
```python
# Full matrix (caution with large datasets)
full_data = adata.X

# Single observation
obs_data = adata.X[0, :]

# Single variable across all observations
var_data = adata.X[:, 0]
```

### obs（观察注释）
DataFrame存储有关观察（行）的元数据。每行对应于 X.

```python
import pandas as pd

# Create AnnData with observation metadata
obs_df = pd.DataFrame({
    'cell_type': ['T cell', 'B cell', 'Monocyte'],
    'treatment': ['control', 'treated', 'control'],
    'timepoint': [0, 24, 24]
}, index=['cell_1', 'cell_2', 'cell_3'])

adata = ad.AnnData(X=np.random.rand(3, 100), obs=obs_df)

# Access observation metadata
print(adata.obs['cell_type'])
print(adata.obs.loc['cell_1'])
```

### var (Variable Annotations)
DataFrame 中的一个观察，存储有关变量（列）的元数据。每行对应于 X.

```python
# Create AnnData with variable metadata
var_df = pd.DataFrame({
    'gene_name': ['ACTB', 'GAPDH', 'TP53'],
    'chromosome': ['7', '12', '17'],
    'highly_variable': [True, False, True]
}, index=['ENSG00001', 'ENSG00002', 'ENSG00003'])

adata = ad.AnnData(X=np.random.rand(100, 3), var=var_df)

# Access variable metadata
print(adata.var['gene_name'])
print(adata.var.loc['ENSG00001'])
```

### 层（替代数据表示）中的一个变量 
字典，存储与 X.

 维度相同的替代矩阵```python
# Store raw counts, normalized data, and scaled data
adata = ad.AnnData(X=np.random.rand(100, 2000))
adata.layers['raw_counts'] = np.random.randint(0, 100, (100, 2000))
adata.layers['normalized'] = adata.X / np.sum(adata.X, axis=1, keepdims=True)
adata.layers['scaled'] = (adata.X - adata.X.mean()) / adata.X.std()

# Access layers
raw_data = adata.layers['raw_counts']
normalized_data = adata.layers['normalized']
```

公共层使用：
- `raw_counts`：归一化前的原始计数数据
- `normalized`：对数归一化或TPM值
- `scaled`：用于分析的Z评分值
- `imputed`：插补后的数据

### obsm（多维观测注释）
存储与观测对齐的多维数组的字典。

```python
# Store PCA coordinates and UMAP embeddings
adata.obsm['X_pca'] = np.random.rand(100, 50)  # 50 principal components
adata.obsm['X_umap'] = np.random.rand(100, 2)  # 2D UMAP coordinates
adata.obsm['X_tsne'] = np.random.rand(100, 2)  # 2D t-SNE coordinates

# Access embeddings
pca_coords = adata.obsm['X_pca']
umap_coords = adata.obsm['X_umap']
```

常见的obsm用途：
- `X_pca`：主成分坐标
- `X_umap`：UMAP嵌入坐标
- `X_tsne`：t-SNE嵌入坐标
- `X_diffmap`：扩散图坐标
- `protein_expression`：蛋白质丰度测量(CITE-seq)

### varm (多维变量注释)
存储与变量对齐的多维数组的字典。

```python
# Store PCA loadings
adata.varm['PCs'] = np.random.rand(2000, 50)  # Loadings for 50 components
adata.varm['gene_modules'] = np.random.rand(2000, 10)  # Gene module scores

# Access loadings
pc_loadings = adata.varm['PCs']
```

常见的varm用途：
- `PCs`：主成分载荷
- `gene_modules`：基因共表达模块分配

### obsp（成对观察关系）
字典，存储表示观察值之间关系的稀疏矩阵。

```python
from scipy.sparse import csr_matrix

# Store k-nearest neighbor graph
n_obs = 100
knn_graph = csr_matrix(np.random.rand(n_obs, n_obs) > 0.95)
adata.obsp['connectivities'] = knn_graph
adata.obsp['distances'] = csr_matrix(np.random.rand(n_obs, n_obs))

# Access graphs
knn_connections = adata.obsp['connectivities']
distances = adata.obsp['distances']
```

常见的obsp用途：
- `connectivities`：细胞-细胞邻域图
- `distances`：之间的成对距离cells

### varp（成对变量关系）
存储表示变量之间关系的稀疏矩阵的字典。

```python
# Store gene-gene correlation matrix
n_vars = 2000
gene_corr = csr_matrix(np.random.rand(n_vars, n_vars) > 0.99)
adata.varp['correlations'] = gene_corr

# Access correlations
gene_correlations = adata.varp['correlations']
```

### uns（非结构化注释）
存储任意非结构化的字典元数据.

```python
# Store analysis parameters and results
adata.uns['experiment_date'] = '2025-11-03'
adata.uns['pca'] = {
    'variance_ratio': [0.15, 0.10, 0.08],
    'params': {'n_comps': 50}
}
adata.uns['neighbors'] = {
    'params': {'n_neighbors': 15, 'method': 'umap'},
    'connectivities_key': 'connectivities'
}

# Access unstructured data
exp_date = adata.uns['experiment_date']
pca_params = adata.uns['pca']['params']
```

常见用途：
- 分析参数和设置
- 用于绘图的调色板
- 聚类信息
- 工具特定元数据

### raw（原始数据）快照）
可选属性，在过滤之前保留原始数据矩阵和变量注释。

```python
# Create AnnData and store raw state
adata = ad.AnnData(X=np.random.rand(100, 5000))
adata.var['gene_name'] = [f'Gene_{i}' for i in range(5000)]

# Store raw state before filtering
adata.raw = adata.copy()

# Filter to highly variable genes
highly_variable_mask = np.random.rand(5000) > 0.5
adata = adata[:, highly_variable_mask]

# Access original data
original_matrix = adata.raw.X
original_var = adata.raw.var
```

##对象属性

```python
# Dimensions
n_observations = adata.n_obs
n_variables = adata.n_vars
shape = adata.shape  # (n_obs, n_vars)

# Index information
obs_names = adata.obs_names  # Observation identifiers
var_names = adata.var_names  # Variable identifiers

# Storage mode
is_view = adata.is_view  # True if this is a view of another object
is_backed = adata.isbacked  # True if backed by on-disk storage
filename = adata.filename  # Path to backing file (if backed)
```

##创建AnnData对象

### 来自数组和 DataFrames
```python
import anndata as ad
import numpy as np
import pandas as pd

# Minimal creation
X = np.random.rand(100, 2000)
adata = ad.AnnData(X)

# With metadata
obs = pd.DataFrame({'cell_type': ['A', 'B'] * 50}, index=[f'cell_{i}' for i in range(100)])
var = pd.DataFrame({'gene_name': [f'Gene_{i}' for i in range(2000)]}, index=[f'ENSG{i:05d}' for i in range(2000)])
adata = ad.AnnData(X=X, obs=obs, var=var)

# With all components
adata = ad.AnnData(
    X=X,
    obs=obs,
    var=var,
    layers={'raw': np.random.randint(0, 100, (100, 2000))},
    obsm={'X_pca': np.random.rand(100, 50)},
    uns={'experiment': 'test'}
)
```

### 来自 DataFrame
```python
# Create from pandas DataFrame (genes as columns, cells as rows)
df = pd.DataFrame(
    np.random.rand(100, 50),
    columns=[f'Gene_{i}' for i in range(50)],
    index=[f'Cell_{i}' for i in range(100)]
)
adata = ad.AnnData(df)
```

## 数据访问模式

### 向量提取
```python
# Get observation annotation as array
cell_types = adata.obs_vector('cell_type')

# Get variable values across observations
gene_expression = adata.obs_vector('ACTB')  # If ACTB is in var_names

# Get variable annotation as array
gene_names = adata.var_vector('gene_name')
```

###子集
```python
# By index
subset = adata[0:10, 0:100]  # First 10 obs, first 100 vars

# By name
subset = adata[['cell_1', 'cell_2'], ['ACTB', 'GAPDH']]

# By boolean mask
high_count_cells = adata.obs['total_counts'] > 1000
subset = adata[high_count_cells, :]

# By observation metadata
t_cells = adata[adata.obs['cell_type'] == 'T cell']
```

## 内存注意事项

AnnData 结构旨在提高内存效率：
- 稀疏矩阵减少稀疏数据的内存
- 视图尽可能避免复制数据
- 支持模式可以处理大于RAM
-分类注释减少离散值的内存

```python
# Convert strings to categoricals (more memory efficient)
adata.obs['cell_type'] = adata.obs['cell_type'].astype('category')
adata.strings_to_categoricals()

# Check if object is a view (doesn't own data)
if adata.is_view:
    adata = adata.copy()  # Create independent copy
```
