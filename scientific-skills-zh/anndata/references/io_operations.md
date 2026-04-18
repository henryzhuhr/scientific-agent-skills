# 输入/输出操作

AnnData 提供全面的 I/O 功能，用于读写各种格式的数据。

## 原生格式

### H5AD（基于 HDF5）
AnnData 对象推荐的原生格式，提供高效存储和快速访问。

#### 编写 H5AD文件
```python
import anndata as ad

# Write to file
adata.write_h5ad('data.h5ad')

# Write with compression
adata.write_h5ad('data.h5ad', compression='gzip')

# Write with specific compression level (0-9, higher = more compression)
adata.write_h5ad('data.h5ad', compression='gzip', compression_opts=9)
```

#### 读取H5AD文件
```python
# Read entire file into memory
adata = ad.read_h5ad('data.h5ad')

# Read in backed mode (lazy loading for large files)
adata = ad.read_h5ad('data.h5ad', backed='r')  # Read-only
adata = ad.read_h5ad('data.h5ad', backed='r+')  # Read-write

# Backed mode enables working with datasets larger than RAM
# Only accessed data is loaded into memory
```

#### 支持模式操作
```python
# Open in backed mode
adata = ad.read_h5ad('large_dataset.h5ad', backed='r')

# Access metadata without loading X into memory
print(adata.obs.head())
print(adata.var.head())

# Subset operations create views
subset = adata[:100, :500]  # View, no data loaded

# Load specific data into memory
X_subset = subset.X[:]  # Now loads this subset

# Convert entire backed object to memory
adata_memory = adata.to_memory()
```

### Zarr
H分层数组存储格式，针对云存储和并行进行了优化I/O.

#### 写入 Zarr
```python
# Write to Zarr store
adata.write_zarr('data.zarr')

# Write with specific chunks (important for performance)
adata.write_zarr('data.zarr', chunks=(100, 100))
```

#### 读取 Zarr
```python
# Read Zarr store
adata = ad.read_zarr('data.zarr')
```

#### 远程 Zarr 访问
```python
import fsspec

# Access Zarr from S3
store = fsspec.get_mapper('s3://bucket-name/data.zarr')
adata = ad.read_zarr(store)

# Access Zarr from URL
store = fsspec.get_mapper('https://example.com/data.zarr')
adata = ad.read_zarr(store)
```

## 替代输入格式

### CSV/TSV
```python
# Read CSV (genes as columns, cells as rows)
adata = ad.read_csv('data.csv')

# Read with custom delimiter
adata = ad.read_csv('data.tsv', delimiter='\t')

# Specify that first column is row names
adata = ad.read_csv('data.csv', first_column_names=True)
```

### Excel
```python
# Read Excel file
adata = ad.read_excel('data.xlsx')

# Read specific sheet
adata = ad.read_excel('data.xlsx', sheet='Sheet1')
```

### Matrix Market (MTX)
基因组学中稀疏矩阵的常用格式。

```python
# Read MTX with associated files
# Requires: matrix.mtx, genes.tsv, barcodes.tsv
adata = ad.read_mtx('matrix.mtx')

# Read with custom gene and barcode files
adata = ad.read_mtx(
    'matrix.mtx',
    var_names='genes.tsv',
    obs_names='barcodes.tsv'
)

# Transpose if needed (MTX often has genes as rows)
adata = adata.T
```

### 10X 基因组格式
```python
# Read 10X h5 format
adata = ad.read_10x_h5('filtered_feature_bc_matrix.h5')

# Read 10X MTX directory
adata = ad.read_10x_mtx('filtered_feature_bc_matrix/')

# Specify genome if multiple present
adata = ad.read_10x_h5('data.h5', genome='GRCh38')
```

### Loom
```python
# Read Loom file
adata = ad.read_loom('data.loom')

# Read with specific observation and variable annotations
adata = ad.read_loom(
    'data.loom',
    obs_names='CellID',
    var_names='Gene'
)
```

### 文本文件
```python
# Read generic text file
adata = ad.read_text('data.txt', delimiter='\t')

# Read with custom parameters
adata = ad.read_text(
    'data.txt',
    delimiter=',',
    first_column_names=True,
    dtype='float32'
)
```

### UMI工具
```python
# Read UMI tools format
adata = ad.read_umi_tools('counts.tsv')
```

### HDF5（通用）
```python
# Read from HDF5 file (not h5ad format)
adata = ad.read_hdf('data.h5', key='dataset')
```

## 替代输出格式

### CSV
```python
# Write to CSV files (creates multiple files)
adata.write_csvs('output_dir/')

# This creates:
# - output_dir/X.csv (expression matrix)
# - output_dir/obs.csv (observation annotations)
# - output_dir/var.csv (variable annotations)
# - output_dir/uns.csv (unstructured annotations, if possible)

# Skip certain components
adata.write_csvs('output_dir/', skip_data=True)  # Skip X matrix
```

### Loom
```python
# Write to Loom format
adata.write_loom('output.loom')
```

## 读取特定元素

为了进行细粒度控制，从存储中读取特定元素：

```python
from anndata import read_elem

# Read just observation annotations
obs = read_elem('data.h5ad/obs')

# Read specific layer
layer = read_elem('data.h5ad/layers/normalized')

# Read unstructured data element
params = read_elem('data.h5ad/uns/pca_params')
```

## 写入特定元素

```python
from anndata import write_elem
import h5py

# Write element to existing file
with h5py.File('data.h5ad', 'a') as f:
    write_elem(f, 'new_layer', adata.X.copy())
```

## 延迟操作

对于非常大的数据集，使用延迟读取以避免加载整个数据集：

```python
from anndata.experimental import read_elem_lazy

# Lazy read (returns dask array or similar)
X_lazy = read_elem_lazy('large_data.h5ad/X')

# Compute only when needed
subset = X_lazy[:100, :100].compute()
```

## 常见I/O模式

### 格式之间的转换
```python
# MTX to H5AD
adata = ad.read_mtx('matrix.mtx').T
adata.write_h5ad('data.h5ad')

# CSV to H5AD
adata = ad.read_csv('data.csv')
adata.write_h5ad('data.h5ad')

# H5AD to Zarr
adata = ad.read_h5ad('data.h5ad')
adata.write_zarr('data.zarr')
```

### 加载元数据而不data
```python
# Backed mode allows inspecting metadata without loading X
adata = ad.read_h5ad('large_file.h5ad', backed='r')
print(f"Dataset contains {adata.n_obs} observations and {adata.n_vars} variables")
print(adata.obs.columns)
print(adata.var.columns)
# X is not loaded into memory
```

### 追加到现有文件
```python
# Open in read-write mode
adata = ad.read_h5ad('data.h5ad', backed='r+')

# Modify metadata
adata.obs['new_column'] = values

# Changes are written to disk
```

### 从URL下载
```python
import anndata as ad

# Read directly from URL (for h5ad files)
url = 'https://example.com/data.h5ad'
adata = ad.read_h5ad(url, backed='r')  # Streaming access

# For other formats, download first
import urllib.request
urllib.request.urlretrieve(url, 'local_file.h5ad')
adata = ad.read_h5ad('local_file.h5ad')
```

## 性能提示

### Reading
- 对于只需要查询的大文件使用 `backed='r'`
- 如果需要修改元数据而不加载所有数据，则使用 `backed='r+'`
- H5AD 格式通常对于随机访问最快
- Zarr 更适合云存储和并行访问
- 考虑存储压缩，但注意它可能会减慢速度读取

### 写入
 - 使用压缩进行长期存储：`compression='gzip'` 或`compression='lzf'`
  - LZF 压缩速度更快，但压缩量小于GZIP
  - 对于Zarr，根据访问模式调整块大小：
  - 用于顺序读取的更大块
  - 用于随机访问的较小块
  - 在写入之前将字符串列转换为分类（较小的文件）

### 内存管理
```python
# Convert strings to categoricals (reduces file size and memory)
adata.strings_to_categoricals()
adata.write_h5ad('data.h5ad')

# Use sparse matrices for sparse data
from scipy.sparse import csr_matrix
if isinstance(adata.X, np.ndarray):
    density = np.count_nonzero(adata.X) / adata.X.size
    if density < 0.5:  # If more than 50% zeros
        adata.X = csr_matrix(adata.X)
```

## 处理大型数据集

### 策略 1：支持模式
```python
# Work with dataset larger than RAM
adata = ad.read_h5ad('100GB_file.h5ad', backed='r')

# Filter based on metadata (fast, no data loading)
filtered = adata[adata.obs['quality_score'] > 0.8]

# Load filtered subset into memory
adata_memory = filtered.to_memory()
```

### 策略 2：分块处理
```python
# Process data in chunks
adata = ad.read_h5ad('large_file.h5ad', backed='r')

chunk_size = 1000
results = []

for i in range(0, adata.n_obs, chunk_size):
    chunk = adata[i:i+chunk_size, :].to_memory()
    # Process chunk
    result = process(chunk)
    results.append(result)
```

### 策略 3：使用 AnnCollection
```python
from anndata.experimental import AnnCollection

# Create collection without loading data
adatas = [f'dataset_{i}.h5ad' for i in range(10)]
collection = AnnCollection(
    adatas,
    join_obs='inner',
    join_vars='inner'
)

# Process collection lazily
# Data is loaded only when accessed
```

## 常见问题和解决方案

### 问题：读取时内存不足
* *解决方案**：使用备份模式或分块读取
```python
adata = ad.read_h5ad('file.h5ad', backed='r')
```

### 问题：从云存储读取速度慢
* *解决方案**：使用 Zarr 格式并适当使用chunking
```python
adata.write_zarr('data.zarr', chunks=(1000, 1000))
```

### 问题：大文件大小
* *解决方案**：使用压缩并转换为稀疏/分类
```python
adata.strings_to_categoricals()
from scipy.sparse import csr_matrix
adata.X = csr_matrix(adata.X)
adata.write_h5ad('compressed.h5ad', compression='gzip')
```

### 问题：无法修改支持的对象
* *解决方案**：加载到内存或打开在“r+”模式下
```python
# Option 1: Load to memory
adata = adata.to_memory()

# Option 2: Open in read-write mode
adata = ad.read_h5ad('file.h5ad', backed='r+')
```
