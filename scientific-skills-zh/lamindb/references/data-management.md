# LaminDB 数据管理

本文档涵盖了 LaminDB 中的查询、搜索、过滤和流式传输数据，以及组织和访问数据集的最佳实践。

## 注册表概述

查看可用注册表及其内容：

```python
import lamindb as ln

# View all registries across modules
ln.view()

# View latest 100 artifacts
ln.Artifact.to_dataframe()

# View other registries
ln.Transform.to_dataframe()
ln.Run.to_dataframe()
ln.User.to_dataframe()
```

## 快速查找Access

对于记录少于 100k 的注册表，`Lookup` 对象可实现方便的自动完成：

```python
# Create lookup
records = ln.Record.lookup()

# Access by name (auto-complete enabled in IDEs)
experiment_1 = records.experiment_1
sample_a = records.sample_a

# Works with biological ontologies too
import bionty as bt
cell_types = bt.CellType.lookup()
t_cell = cell_types.t_cell
```

## 检索单个记录

### 使用 get()

精确检索一条记录（如果为零或多个则出错） matches):

```python
# By UID
artifact = ln.Artifact.get("aRt1Fact0uid000")

# By field
artifact = ln.Artifact.get(key="data/experiment.h5ad")
user = ln.User.get(handle="researcher123")

# By ontology ID (for bionty)
cell_type = bt.CellType.get(ontology_id="CL:0000084")
```

#### 使用one()和one_or_none()

```python
# Get exactly one from QuerySet (errors if 0 or >1)
artifact = ln.Artifact.filter(key="data.csv").one()

# Get one or None (errors if >1)
artifact = ln.Artifact.filter(key="maybe_data.csv").one_or_none()

# Get first match
artifact = ln.Artifact.filter(suffix=".h5ad").first()
```

## 过滤数据

`filter()`方法返回一个QuerySet，以便灵活检索：

```python
# Basic filtering
artifacts = ln.Artifact.filter(suffix=".h5ad")
artifacts.to_dataframe()

# Multiple conditions (AND logic)
artifacts = ln.Artifact.filter(
    suffix=".h5ad",
    created_by=user
)

# Comparison operators
ln.Artifact.filter(size__gt=1e6).to_dataframe()           # Greater than
ln.Artifact.filter(size__gte=1e6).to_dataframe()          # Greater than or equal
ln.Artifact.filter(size__lt=1e9).to_dataframe()           # Less than
ln.Artifact.filter(size__lte=1e9).to_dataframe()          # Less than or equal

# Range queries
ln.Artifact.filter(size__gte=1e6, size__lte=1e9).to_dataframe()
```

## 文本和字符串查询

```python
# Exact match
ln.Artifact.filter(description="Experiment 1").to_dataframe()

# Contains (case-sensitive)
ln.Artifact.filter(description__contains="RNA").to_dataframe()

# Case-insensitive contains
ln.Artifact.filter(description__icontains="rna").to_dataframe()

# Starts with
ln.Artifact.filter(key__startswith="experiments/").to_dataframe()

# Ends with
ln.Artifact.filter(key__endswith=".csv").to_dataframe()

# IN list
ln.Artifact.filter(suffix__in=[".h5ad", ".csv", ".parquet"]).to_dataframe()
```

## 基于特征的查询

通过注释特征查询工件：

```python
# Filter by feature value
ln.Artifact.filter(cell_type="T cell").to_dataframe()
ln.Artifact.filter(treatment="DMSO").to_dataframe()

# Include features in output
ln.Artifact.filter(treatment="DMSO").to_dataframe(include="features")

# Nested dictionary access
ln.Artifact.filter(study_metadata__assay="RNA-seq").to_dataframe()
ln.Artifact.filter(study_metadata__detail1="123").to_dataframe()

# Check annotation status
ln.Artifact.filter(cell_type__isnull=False).to_dataframe()  # Has annotation
ln.Artifact.filter(treatment__isnull=True).to_dataframe()    # Missing annotation
```

## 遍历相关注册表

Django的双下划线语法可以实现跨相关表的查询：

```python
# Find artifacts by creator handle
ln.Artifact.filter(created_by__handle="researcher123").to_dataframe()
ln.Artifact.filter(created_by__handle__startswith="test").to_dataframe()

# Find artifacts by transform name
ln.Artifact.filter(transform__name="preprocess.py").to_dataframe()

# Find artifacts measuring specific genes
ln.Artifact.filter(feature_sets__genes__symbol="CD8A").to_dataframe()
ln.Artifact.filter(feature_sets__genes__ensembl_gene_id="ENSG00000153563").to_dataframe()

# Find runs with specific parameters
ln.Run.filter(params__learning_rate=0.01).to_dataframe()
ln.Run.filter(params__downsample=True).to_dataframe()

# Find artifacts from specific project
project = ln.Project.get(name="Cancer Study")
ln.Artifact.filter(projects=project).to_dataframe()
```

## 排序结果

```python
# Order by field (ascending)
ln.Artifact.filter(suffix=".h5ad").order_by("created_at").to_dataframe()

# Order descending
ln.Artifact.filter(suffix=".h5ad").order_by("-created_at").to_dataframe()

# Multiple order fields
ln.Artifact.order_by("-created_at", "size").to_dataframe()
```

## 高级逻辑查询

### OR Logic

```python
from lamindb import Q

# OR condition
artifacts = ln.Artifact.filter(
    Q(suffix=".jpg") | Q(suffix=".png")
).to_dataframe()

# Complex OR with multiple conditions
artifacts = ln.Artifact.filter(
    Q(suffix=".h5ad", size__gt=1e6) | Q(suffix=".csv", size__lt=1e3)
).to_dataframe()
```

### NOT Logic

```python
# Exclude condition
artifacts = ln.Artifact.filter(
    ~Q(suffix=".tmp")
).to_dataframe()

# Complex exclusion
artifacts = ln.Artifact.filter(
    ~Q(created_by__handle="testuser")
).to_dataframe()
```

### 组合 AND、OR、NOT

```python
# Complex query
artifacts = ln.Artifact.filter(
    (Q(suffix=".h5ad") | Q(suffix=".csv")) &
    Q(size__gt=1e6) &
    ~Q(created_by__handle__startswith="test")
).to_dataframe()
```

## 搜索功能

全文搜索注册表字段：

```python
# Basic search
ln.Artifact.search("iris").to_dataframe()
ln.User.search("smith").to_dataframe()

# Search in specific registry
bt.CellType.search("T cell").to_dataframe()
bt.Gene.search("CD8").to_dataframe()
```

## 使用查询集

查询集是惰性的 - 它们在评估之前不会访问数据库：

```python
# Create query (no database hit)
qs = ln.Artifact.filter(suffix=".h5ad")

# Evaluate in different ways
df = qs.to_dataframe()        # As pandas DataFrame
list_records = list(qs)       # As Python list
count = qs.count()            # Count only
exists = qs.exists()          # Boolean check

# Iteration
for artifact in qs:
    print(artifact.key, artifact.size)

# Slicing
first_10 = qs[:10]
next_10 = qs[10:20]
```

## 链接过滤器

```python
# Build query incrementally
qs = ln.Artifact.filter(suffix=".h5ad")
qs = qs.filter(size__gt=1e6)
qs = qs.filter(created_at__year=2025)
qs = qs.order_by("-created_at")

# Execute
results = qs.to_dataframe()
```

## 流式传输大型数据集

对于太大而无法放入内存的数据集，请使用流式访问：

### 流式传输文件

```python
# Open file stream
artifact = ln.Artifact.get(key="large_file.csv")

with artifact.open() as f:
    # Read in chunks
    chunk = f.read(10000)  # Read 10KB
    # Process chunk
```

### 数组切片

对于基于数组的格式（Zarr、HDF5、AnnData）：

```python
# Get backing file without loading
artifact = ln.Artifact.get(key="large_data.h5ad")
adata = artifact.backed()  # Returns backed AnnData

# Slice specific portions
subset = adata[:1000, :]  # First 1000 cells
genes_of_interest = adata[:, ["CD4", "CD8A", "CD8B"]]

# Stream batches
for i in range(0, adata.n_obs, 1000):
    batch = adata[i:i+1000, :]
    # Process batch
```

### 迭代器访问

```python
# Process large collections incrementally
artifacts = ln.Artifact.filter(suffix=".fastq.gz")

for artifact in artifacts.iterator(chunk_size=10):
    # Process 10 at a time
    path = artifact.cache()
    # Analyze file
```

## 聚合和统计

```python
# Count records
ln.Artifact.filter(suffix=".h5ad").count()

# Distinct values
ln.Artifact.values_list("suffix", flat=True).distinct()

# Aggregation (requires Django ORM knowledge)
from django.db.models import Sum, Avg, Max, Min

# Total size of all artifacts
ln.Artifact.aggregate(Sum("size"))

# Average artifact size by suffix
ln.Artifact.values("suffix").annotate(avg_size=Avg("size"))
```

## 缓存和性能

```python
# Check cache location
ln.settings.cache_dir

# Configure cache
lamin cache set /path/to/cache

# Clear cache for specific artifact
artifact.delete_cache()

# Get cached path (downloads if needed)
path = artifact.cache()

# Check if cached
if artifact.is_cached():
    path = artifact.cache()
```

## 用键组织数据

构建键的最佳实践：

```python
# Hierarchical organization
ln.Artifact("data.h5ad", key="project/experiment/batch1/data.h5ad").save()
ln.Artifact("data.h5ad", key="scrna/2025/oct/sample_001.h5ad").save()

# Browse by prefix
ln.Artifact.filter(key__startswith="scrna/2025/oct/").to_dataframe()

# Version in key (alternative to built-in versioning)
ln.Artifact("data.h5ad", key="data/processed/v1/final.h5ad").save()
ln.Artifact("data.h5ad", key="data/processed/v2/final.h5ad").save()
```

## 集合

将相关工件分组到集合中：

```python
# Create collection
collection = ln.Collection(
    [artifact1, artifact2, artifact3],
    name="scRNA-seq batch 1-3",
    description="Complete dataset across three batches"
).save()

# Access collection members
for artifact in collection.artifacts:
    print(artifact.key)

# Query collections
ln.Collection.filter(name__contains="batch").to_dataframe()
```

## 最佳实践

1. **加载前使用过滤器**：在访问文件内容之前查询元数据
2. **利用查询集**：针对复杂条件逐步构建查询
3. **流式传输大文件**：不必要时不要将整个数据集加载到内存中
4. **分层结构键**：使浏览和过滤更容易
5. **使用搜索进行发现**：当您不知道确切的字段值时
6. **策略性缓存**：根据存储容量
7配置缓存位置。 **索引特征**：预先定义特征以实现基于特征的高效查询
8. **使用集合**：对数据集级操作的相关工件进行分组
9. **订单结果**：按创建日期或其他字段排序，以便检索一致
10. **检查是否存在**：使用`exists()`或`one_or_none()`以避免错误

## 常见查询模式

```python
# Recent artifacts
ln.Artifact.order_by("-created_at")[:10].to_dataframe()

# My artifacts
me = ln.setup.settings.user
ln.Artifact.filter(created_by=me).to_dataframe()

# Large files
ln.Artifact.filter(size__gt=1e9).order_by("-size").to_dataframe()

# This month's data
from datetime import datetime
ln.Artifact.filter(
    created_at__year=2025,
    created_at__month=10
).to_dataframe()

# Validated datasets with specific features
ln.Artifact.filter(
    is_valid=True,
    cell_type__isnull=False
).to_dataframe(include="features")
```
