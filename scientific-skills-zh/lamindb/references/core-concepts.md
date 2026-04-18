# LaminDB 核心概念

本文档涵盖了 LaminDB 的基本概念和构建块：工件、记录、运行、转换、特征和数据沿袭跟踪。

## Artifacts

Artifacts 表示各种格式的数据集（DataFrames、AnnData、SpatialData、实木复合地板、扎尔等）。它们用作 LaminDB.

### 创建和保存工件

* *来自文件：**
```python
import lamindb as ln

# Save a file as artifact
ln.Artifact("sample.fasta", key="sample.fasta").save()

# With description
artifact = ln.Artifact(
    "data/analysis.h5ad",
    key="experiments/scrna_batch1.h5ad",
    description="Single-cell RNA-seq batch 1"
).save()
```

* *来自数据帧：**
```python
import pandas as pd

df = pd.read_csv("data.csv")
artifact = ln.Artifact.from_dataframe(
    df,
    key="datasets/processed_data.parquet",
    description="Processed experimental data"
).save()
```

* *来自AnnData:**
```python
import anndata as ad

adata = ad.read_h5ad("data.h5ad")
artifact = ln.Artifact.from_anndata(
    adata,
    key="scrna/experiment1.h5ad",
    description="scRNA-seq data with QC"
).save()
```

### 检索工件

```python
# By key
artifact = ln.Artifact.get(key="sample.fasta")

# By UID
artifact = ln.Artifact.get("aRt1Fact0uid000")

# By filter
artifact = ln.Artifact.filter(suffix=".h5ad").first()
```

### 访问工件内容

```python
# Get cached local path
local_path = artifact.cache()

# Load into memory
data = artifact.load()  # Returns DataFrame, AnnData, etc.

# Streaming access (for large files)
with artifact.open() as f:
    # Read incrementally
    chunk = f.read(1000)
```

### 工件元数据

```python
# View all metadata
artifact.describe()

# Access specific metadata
artifact.size          # File size in bytes
artifact.suffix        # File extension
artifact.created_at    # Timestamp
artifact.created_by    # User who created it
artifact.run          # Associated run
artifact.transform    # Associated transform
artifact.version      # Version string
```

## 记录

记录表示实验实体：样本、扰动、仪器、细胞系和任何其他元数据实体。它们通过类型定义支持分层关系。

### 创建记录

```python
# Define a type
sample_type = ln.Record(name="Sample", is_type=True).save()

# Create instances of that type
ln.Record(name="P53mutant1", type=sample_type).save()
ln.Record(name="P53mutant2", type=sample_type).save()
ln.Record(name="WT-control", type=sample_type).save()
```

### 搜索记录

```python
# Text search
ln.Record.search("p53").to_dataframe()

# Filter by fields
ln.Record.filter(type=sample_type).to_dataframe()

# Get specific record
record = ln.Record.get(name="P53mutant1")
```

### 分层关系

```python
# Establish parent-child relationships
parent_record = ln.Record.get(name="P53mutant1")
child_record = ln.Record(name="P53mutant1-replicate1", type=sample_type).save()
child_record.parents.add(parent_record)

# Query relationships
parent_record.children.to_dataframe()
child_record.parents.to_dataframe()
```

## 运行和转换

这些捕获计算谱系。 **Transform** 表示可重用的分析步骤（笔记本、脚本或函数），而 **Run** 记录特定的执行实例。

### 基本跟踪工作流程

```python
import lamindb as ln

# Start tracking (beginning of notebook/script)
ln.track()

# Your analysis code
data = ln.Artifact.get(key="input.csv").load()
# ... perform analysis ...
result.to_csv("output.csv")
artifact = ln.Artifact("output.csv", key="output.csv").save()

# Finish tracking (end of notebook/script)
ln.finish()
```

### 使用参数进行跟踪

```python
ln.track(params={
    "learning_rate": 0.01,
    "batch_size": 32,
    "epochs": 100,
    "downsample": True
})

# Query runs by parameters
ln.Run.filter(params__learning_rate=0.01).to_dataframe()
ln.Run.filter(params__downsample=True).to_dataframe()
```

### 使用参数进行跟踪项目

```python
# Associate with project
ln.track(project="Cancer Drug Screen 2025")

# Query by project
project = ln.Project.get(name="Cancer Drug Screen 2025")
ln.Artifact.filter(projects=project).to_dataframe()
ln.Run.filter(project=project).to_dataframe()
```

### 函数级跟踪

使用 `@ln.tracked()` 装饰器进行细粒度沿袭：

```python
@ln.tracked()
def preprocess_data(input_key: str, output_key: str, normalize: bool = True) -> None:
    """Preprocess raw data and save result."""
    # Load input (automatically tracked)
    artifact = ln.Artifact.get(key=input_key)
    data = artifact.load()

    # Process
    if normalize:
        data = (data - data.mean()) / data.std()

    # Save output (automatically tracked)
    ln.Artifact.from_dataframe(data, key=output_key).save()

# Each call creates a separate Transform and Run
preprocess_data("raw/batch1.csv", "processed/batch1.csv", normalize=True)
preprocess_data("raw/batch2.csv", "processed/batch2.csv", normalize=False)
```

### 访问沿袭信息

```python
# From artifact to run
artifact = ln.Artifact.get(key="output.csv")
run = artifact.run
transform = run.transform

# View details
run.describe()          # Run metadata
transform.describe()    # Transform metadata

# Access inputs
run.inputs.to_dataframe()

# Visualize lineage graph
artifact.view_lineage()
```

## 功能

功能定义用于验证和查询的类型化元数据字段。它们支持结构化注释和搜索。

### 定义特征

```python
from datetime import date

# Numeric feature
ln.Feature(name="gc_content", dtype=float).save()
ln.Feature(name="read_count", dtype=int).save()

# Date feature
ln.Feature(name="experiment_date", dtype=date).save()

# Categorical feature
ln.Feature(name="cell_type", dtype=str).save()
ln.Feature(name="treatment", dtype=str).save()
```

### 使用特征注释工件

```python
# Single values
artifact.features.add_values({
    "gc_content": 0.55,
    "experiment_date": "2025-10-31"
})

# Using feature registry records
gc_content_feature = ln.Feature.get(name="gc_content")
artifact.features.add(gc_content_feature)
```

### 查询功能

```python
# Filter by feature value
ln.Artifact.filter(gc_content=0.55).to_dataframe()
ln.Artifact.filter(experiment_date="2025-10-31").to_dataframe()

# Comparison operators
ln.Artifact.filter(read_count__gt=1000000).to_dataframe()
ln.Artifact.filter(gc_content__gte=0.5, gc_content__lte=0.6).to_dataframe()

# Check for presence of annotation
ln.Artifact.filter(cell_type__isnull=False).to_dataframe()

# Include features in output
ln.Artifact.filter(treatment="DMSO").to_dataframe(include="features")
```

### 嵌套字典功能

对于存储为字典的复杂元数据：

```python
# Access nested values
ln.Artifact.filter(study_metadata__detail1="123").to_dataframe()
ln.Artifact.filter(study_metadata__assay__type="RNA-seq").to_dataframe()
```

## 数据沿袭跟踪

LaminDB 自动捕获执行上下文以及数据、代码和运行之间的关系。

### 跟踪内容

- **源代码**：脚本/笔记本内容和 git commit
- **环境**：Python 包和版本
- **输入工件**：执行期间加载的数据
- **输出工件**：执行过程中创建的数据
- **执行元数据**：时间戳、用户、参数
- **计算依赖**：转换关系

### 查看谱系

```python
# Visualize full lineage graph
artifact.view_lineage()

# View captured metadata
artifact.describe()

# Access related entities
artifact.run              # The run that created it
artifact.run.transform    # The transform (code) used
artifact.run.inputs       # Input artifacts
artifact.run.report       # Execution report
```

### 查询Lineage

```python
# Find all outputs from a transform
transform = ln.Transform.get(name="preprocessing.py")
ln.Artifact.filter(transform=transform).to_dataframe()

# Find all artifacts from a specific user
user = ln.User.get(handle="researcher123")
ln.Artifact.filter(created_by=user).to_dataframe()

# Find artifacts using specific inputs
input_artifact = ln.Artifact.get(key="raw/data.csv")
runs = ln.Run.filter(inputs=input_artifact)
ln.Artifact.filter(run__in=runs).to_dataframe()
```

## 版本控制

LaminDB 在源数据或代码更改时自动管理工件版本控制。

### 自动版本控制

```python
# First version
artifact_v1 = ln.Artifact("data.csv", key="experiment/data.csv").save()

# Modify and save again - creates new version
# (modify data.csv)
artifact_v2 = ln.Artifact("data.csv", key="experiment/data.csv").save()
```

### 使用版本

```python
# Get latest version (default)
artifact = ln.Artifact.get(key="experiment/data.csv")

# View all versions
artifact.versions.to_dataframe()

# Get specific version
artifact_v1 = artifact.versions.filter(version="1").first()

# Compare versions
v1_data = artifact_v1.load()
v2_data = artifact.load()
```

## 最佳实践

1. **使用有意义的键**：按层次结构键（例如，`project/experiment/sample.h5ad`）
2. **添加描述**：帮助未来的用户了解工件内容
3. **一致跟踪**：在每次分析开始时调用 `ln.track()`
4. **预先定义特征**：在注释
5之前创建特征注册表。 **使用类型化特征**：指定数据类型以更好地验证
6. **利用版本控制**：不要为微小的更改创建新密钥
7. **文档转换**：将文档字符串添加到跟踪的函数
8. **设置项目**：将相关工作分组，以便于组织和访问控制
9. **高效查询**：在加载大型数据集
10之前使用过滤器。 **可视化谱系**：使用`view_lineage()`了解数据来源
