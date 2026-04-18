# 连接 AnnData 对象

沿观察值或变量轴组合多个 AnnData 对象。

## 基本连接

### 沿观察值连接（堆栈单元格/样本）
```python
import anndata as ad
import numpy as np

# Create multiple AnnData objects
adata1 = ad.AnnData(X=np.random.rand(100, 50))
adata2 = ad.AnnData(X=np.random.rand(150, 50))
adata3 = ad.AnnData(X=np.random.rand(200, 50))

# Concatenate along observations (axis=0, default)
adata_combined = ad.concat([adata1, adata2, adata3], axis=0)

print(adata_combined.shape)  # (450, 50)
```

### 沿变量连接（堆栈）基因/特征)
```python
# Create objects with same observations, different variables
adata1 = ad.AnnData(X=np.random.rand(100, 50))
adata2 = ad.AnnData(X=np.random.rand(100, 30))
adata3 = ad.AnnData(X=np.random.rand(100, 70))

# Concatenate along variables (axis=1)
adata_combined = ad.concat([adata1, adata2, adata3], axis=1)

print(adata_combined.shape)  # (100, 150)
```

## 连接类型

### 内连接(交集)
仅保留所有对象中存在的变量/观察结果。

```python
import pandas as pd

# Create objects with different variables
adata1 = ad.AnnData(
    X=np.random.rand(100, 50),
    var=pd.DataFrame(index=[f'Gene_{i}' for i in range(50)])
)
adata2 = ad.AnnData(
    X=np.random.rand(150, 60),
    var=pd.DataFrame(index=[f'Gene_{i}' for i in range(10, 70)])
)

# Inner join: only genes 10-49 are kept (overlap)
adata_inner = ad.concat([adata1, adata2], join='inner')
print(adata_inner.n_vars)  # 40 genes (overlap)
```

### 外连接(并集)
Keep所有变量/观察值，填充缺失值。

```python
# Outer join: all genes are kept
adata_outer = ad.concat([adata1, adata2], join='outer')
print(adata_outer.n_vars)  # 70 genes (union)

# Missing values are filled with appropriate defaults:
# - 0 for sparse matrices
# - NaN for dense matrices
```

### 填充外连接的值
```python
# Specify fill value for missing data
adata_filled = ad.concat([adata1, adata2], join='outer', fill_value=0)
```

## 跟踪数据源

### 添加批次labels
```python
# Label which object each observation came from
adata_combined = ad.concat(
    [adata1, adata2, adata3],
    label='batch',  # Column name for labels
    keys=['batch1', 'batch2', 'batch3']  # Labels for each object
)

print(adata_combined.obs['batch'].value_counts())
# batch1    100
# batch2    150
# batch3    200
```

### 自动批量标签
```python
# If keys not provided, uses integer indices
adata_combined = ad.concat(
    [adata1, adata2, adata3],
    label='dataset'
)
# dataset column contains: 0, 1, 2
```

## 合并策略

使用 `merge` 参数控制如何组合来自不同对象的元数据。

### merge=None （默认为 None）观察）
排除非串联轴上的元数据。

```python
# When concatenating observations, var metadata must match
adata1.var['gene_type'] = 'protein_coding'
adata2.var['gene_type'] = 'protein_coding'

# var is kept only if identical across all objects
adata_combined = ad.concat([adata1, adata2], merge=None)
```

### merge='same'
保留所有对象中相同的元数据。

```python
adata1.var['chromosome'] = ['chr1'] * 25 + ['chr2'] * 25
adata2.var['chromosome'] = ['chr1'] * 25 + ['chr2'] * 25
adata1.var['type'] = 'protein_coding'
adata2.var['type'] = 'lncRNA'  # Different

# 'chromosome' is kept (same), 'type' is excluded (different)
adata_combined = ad.concat([adata1, adata2], merge='same')
```

### merge='unique'
保留每个键只有一个的元数据列value.

```python
adata1.var['gene_id'] = [f'ENSG{i:05d}' for i in range(50)]
adata2.var['gene_id'] = [f'ENSG{i:05d}' for i in range(50)]

# gene_id is kept (unique values for each key)
adata_combined = ad.concat([adata1, adata2], merge='unique')
```

### merge='first'
从包含每个键的第一个对象中获取值。

```python
adata1.var['description'] = ['Desc1'] * 50
adata2.var['description'] = ['Desc2'] * 50

# Uses descriptions from adata1
adata_combined = ad.concat([adata1, adata2], merge='first')
```

### merge='only'
保留仅出现在一个中的元数据object.

```python
adata1.var['adata1_specific'] = [1] * 50
adata2.var['adata2_specific'] = [2] * 50

# Both metadata columns are kept
adata_combined = ad.concat([adata1, adata2], merge='only')
```

## 处理索引冲突

### 使索引唯一
```python
import pandas as pd

# Create objects with overlapping observation names
adata1 = ad.AnnData(
    X=np.random.rand(3, 10),
    obs=pd.DataFrame(index=['cell_1', 'cell_2', 'cell_3'])
)
adata2 = ad.AnnData(
    X=np.random.rand(3, 10),
    obs=pd.DataFrame(index=['cell_1', 'cell_2', 'cell_3'])
)

# Make indices unique by appending batch keys
adata_combined = ad.concat(
    [adata1, adata2],
    label='batch',
    keys=['batch1', 'batch2'],
    index_unique='_'  # Separator for making indices unique
)

print(adata_combined.obs_names)
# ['cell_1_batch1', 'cell_2_batch1', 'cell_3_batch1',
#  'cell_1_batch2', 'cell_2_batch2', 'cell_3_batch2']
```

## 连接层

```python
# Objects with layers
adata1 = ad.AnnData(X=np.random.rand(100, 50))
adata1.layers['normalized'] = np.random.rand(100, 50)
adata1.layers['scaled'] = np.random.rand(100, 50)

adata2 = ad.AnnData(X=np.random.rand(150, 50))
adata2.layers['normalized'] = np.random.rand(150, 50)
adata2.layers['scaled'] = np.random.rand(150, 50)

# Layers are concatenated automatically if present in all objects
adata_combined = ad.concat([adata1, adata2])

print(adata_combined.layers.keys())
# dict_keys(['normalized', 'scaled'])
```

## 连接多维注释

### obsm/varm
```python
# Objects with embeddings
adata1.obsm['X_pca'] = np.random.rand(100, 50)
adata2.obsm['X_pca'] = np.random.rand(150, 50)

# obsm is concatenated along observation axis
adata_combined = ad.concat([adata1, adata2])
print(adata_combined.obsm['X_pca'].shape)  # (250, 50)
```

### obsp/varp（成对注释）
```python
from scipy.sparse import csr_matrix

# Pairwise matrices
adata1.obsp['connectivities'] = csr_matrix((100, 100))
adata2.obsp['connectivities'] = csr_matrix((150, 150))

# By default, obsp is NOT concatenated (set pairwise=True to include)
adata_combined = ad.concat([adata1, adata2])
# adata_combined.obsp is empty

# Include pairwise data (creates block diagonal matrix)
adata_combined = ad.concat([adata1, adata2], pairwise=True)
print(adata_combined.obsp['connectivities'].shape)  # (250, 250)
```

## 连接uns （非结构化）

非结构化元数据递归合并：

```python
adata1.uns['experiment'] = {'date': '2025-01-01', 'batch': 'A'}
adata2.uns['experiment'] = {'date': '2025-01-01', 'batch': 'B'}

# Using merge='unique' for uns
adata_combined = ad.concat([adata1, adata2], uns_merge='unique')
# 'date' is kept (same value), 'batch' might be excluded (different values)
```

## 延迟连接（AnnCollection）

对于非常大的数据集，使用不加载所有数据的延迟连接data:

```python
from anndata.experimental import AnnCollection

# Create collection from file paths (doesn't load data)
files = ['data1.h5ad', 'data2.h5ad', 'data3.h5ad']
collection = AnnCollection(
    files,
    join_obs='outer',
    join_vars='inner',
    label='dataset',
    keys=['dataset1', 'dataset2', 'dataset3']
)

# Access data lazily
print(collection.n_obs)  # Total observations
print(collection.obs.head())  # Metadata loaded, not X

# Convert to regular AnnData when needed (loads all data)
adata = collection.to_adata()
```

### 使用 AnnCollection
```python
# Subset without loading data
subset = collection[collection.obs['cell_type'] == 'T cell']

# Iterate through datasets
for adata in collection:
    print(adata.shape)

# Access specific dataset
first_dataset = collection[0]
```

## 磁盘上的串联

对于内存太大的数据集，请直接在磁盘上连接：

```python
from anndata.experimental import concat_on_disk

# Concatenate without loading into memory
concat_on_disk(
    ['data1.h5ad', 'data2.h5ad', 'data3.h5ad'],
    'combined.h5ad',
    join='outer'
)

# Load result in backed mode
adata = ad.read_h5ad('combined.h5ad', backed='r')
```

## 常见连接模式

### 合并技术复制
```python
# Multiple runs of the same samples
replicates = [adata_run1, adata_run2, adata_run3]
adata_combined = ad.concat(
    replicates,
    label='technical_replicate',
    keys=['rep1', 'rep2', 'rep3'],
    join='inner'  # Keep only genes measured in all runs
)
```

### 合并来自的批次实验
```python
# Different experimental batches
batches = [adata_batch1, adata_batch2, adata_batch3]
adata_combined = ad.concat(
    batches,
    label='batch',
    keys=['batch1', 'batch2', 'batch3'],
    join='outer'  # Keep all genes
)

# Later: apply batch correction
```

### 合并多模态数据
```python
# Different measurement modalities (e.g., RNA + protein)
adata_rna = ad.AnnData(X=np.random.rand(100, 2000))
adata_protein = ad.AnnData(X=np.random.rand(100, 50))

# Concatenate along variables to combine modalities
adata_multimodal = ad.concat([adata_rna, adata_protein], axis=1)

# Add labels to distinguish modalities
adata_multimodal.var['modality'] = ['RNA'] * 2000 + ['protein'] * 50
```

## 最佳实践

1. **连接前检查兼容性**
```python
# Verify shapes are compatible
print([adata.n_vars for adata in [adata1, adata2, adata3]])

# Check variable names match
print([set(adata.var_names) for adata in [adata1, adata2, adata3]])
```

2. **使用适当的连接类型** 
- `inner`：当您需要在所有样本中使用相同的特征时（最严格） 
- `outer`：当您想要保留所有特征（最包容）时 

3. **跟踪数据源**
 始终使用 `label` 和 `keys` 来跟踪哪些观测值来自哪个数据集。

4. **考虑内存使用**
  - 对于大型数据集，使用 `AnnCollection` 或 `concat_on_disk`
  - 考虑结果的支持模式

5. **处理批次效应**
串联组合数据，但不纠正批次效应。串联后应用批量校正：
```python
# After concatenation, apply batch correction
import scanpy as sc
sc.pp.combat(adata_combined, key='batch')
```

6. **验证结果**
```python
# Check dimensions
print(adata_combined.shape)

# Check batch distribution
print(adata_combined.obs['batch'].value_counts())

# Verify metadata integrity
print(adata_combined.var.head())
print(adata_combined.obs.head())
```
