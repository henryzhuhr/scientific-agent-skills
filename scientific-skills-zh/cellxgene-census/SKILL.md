---
name: cellxgene-census
description: 以编程方式查询 CELLxGENE 普查（61M+ 单元）。当您需要来自最大的精选单细胞图谱的跨组织、疾病或细胞类型的表达数据时使用。最适合人口规模查询、参考图集比较。要分析您自己的数据，请使用 scanpy 或 scvi-tools。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# CZ CELLxGENE Census

## 概述

CZ CELLxGENE Census 提供对来自 CZ CELLxGENE Discover 的全面、版本化标准化单细胞基因组数据集合的编程访问。这项技能可以对数千个数据集中的数百万个细胞进行高效查询和分析。

人口普查包括：
- **来自人类和小鼠的 61+ 百万个细胞**
- **标准化元数据**（细胞类型、组织、疾病、供体）
- **原始基因表达**矩阵
- **预先计算的嵌入**和统计
- **与PyTorch、scanpy和其他分析工具集成**

## 何时使用此技能

应在以下情况下使用此技能：
- 按细胞类型、组织或疾病查询单细胞表达数据
- 探索可用的单细胞数据集和元数据
- 在单细胞数据上训练机器学习模型
- 执行大规模跨数据集分析
- 将人口普查数据与 scanpy 集成或其他分析框架
- 跨数百万个单元计算统计数据
- 访问预先计算的嵌入或模型预测

## 安装和设置

安装人口普查API：
```bash
uv pip install cellxgene-census
```

对于机器学习工作流程，安装额外的依赖项：
```bash
uv pip install cellxgene-census[experimental]
```

## 核心工作流程模式

### 1. 打开人口普查

始终使用上下文管理器以确保正确的资源清理：

```python
import cellxgene_census

# Open latest stable version
with cellxgene_census.open_soma() as census:
    # Work with census data

# Open specific version for reproducibility
with cellxgene_census.open_soma(census_version="2023-07-25") as census:
    # Work with census data
```

* *Key要点：**
- 使用上下文管理器（`with` 语句）进行自动清理
- 指定 `census_version` 进行可重现分析
- 默认打开最新的“稳定”版本

### 2. 探索人口普查信息

在查询表达式数据之前，探索可用的数据集和元数据。

* *访问摘要信息：**
```python
# Get summary statistics
summary = census["census_info"]["summary"].read().concat().to_pandas()
print(f"Total cells: {summary['total_cell_count'][0]}")

# Get all datasets
datasets = census["census_info"]["datasets"].read().concat().to_pandas()

# Filter datasets by criteria
covid_datasets = datasets[datasets["disease"].str.contains("COVID", na=False)]
```

* *查询单元格元数据以了解可用数据：**
```python
# Get unique cell types in a tissue
cell_metadata = cellxgene_census.get_obs(
    census,
    "homo_sapiens",
    value_filter="tissue_general == 'brain' and is_primary_data == True",
    column_names=["cell_type"]
)
unique_cell_types = cell_metadata["cell_type"].unique()
print(f"Found {len(unique_cell_types)} cell types in brain")

# Count cells by tissue
tissue_counts = cell_metadata.groupby("tissue_general").size()
```

* *重要：**始终过滤用于 `is_primary_data == True` 以避免计算重复单元格，除非专门分析重复项。

### 3. 查询表达式数据（小到中规模）

对于返回适合内存的 < 100k 单元格的查询，请使用 `get_anndata()`:

```python
# Basic query with cell type and tissue filters
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",  # or "Mus musculus"
    obs_value_filter="cell_type == 'B cell' and tissue_general == 'lung' and is_primary_data == True",
    obs_column_names=["assay", "disease", "sex", "donor_id"],
)

# Query specific genes with multiple filters
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    var_value_filter="feature_name in ['CD4', 'CD8A', 'CD19', 'FOXP3']",
    obs_value_filter="cell_type == 'T cell' and disease == 'COVID-19' and is_primary_data == True",
    obs_column_names=["cell_type", "tissue_general", "donor_id"],
)
```

* *过滤器语法：**
- 使用 `obs_value_filter` 进行细胞过滤
- 使用 `var_value_filter` 进行基因过滤
- 将条件与 `and`、`or`
 组合使用 `in` 进行多个值： `tissue in ['lung', 'liver']`
- 使用`obs_column_names`

仅选择需要的列**单独获取元数据：**
```python
# Query cell metadata
cell_metadata = cellxgene_census.get_obs(
    census, "homo_sapiens",
    value_filter="disease == 'COVID-19' and is_primary_data == True",
    column_names=["cell_type", "tissue_general", "donor_id"]
)

# Query gene metadata
gene_metadata = cellxgene_census.get_var(
    census, "homo_sapiens",
    value_filter="feature_name in ['CD4', 'CD8A']",
    column_names=["feature_id", "feature_name", "feature_length"]
)
```

### 4.大规模查询（核外处理）

对于超出可用 RAM 的查询，请使用 `axis_query()` 进行迭代处理：

```python
import tiledbsoma as soma

# Create axis query
query = census["census_data"]["homo_sapiens"].axis_query(
    measurement_name="RNA",
    obs_query=soma.AxisQuery(
        value_filter="tissue_general == 'brain' and is_primary_data == True"
    ),
    var_query=soma.AxisQuery(
        value_filter="feature_name in ['FOXP2', 'TBR1', 'SATB2']"
    )
)

# Iterate through expression matrix in chunks
iterator = query.X("raw").tables()
for batch in iterator:
    # batch is a pyarrow.Table with columns:
    # - soma_data: expression value
    # - soma_dim_0: cell (obs) coordinate
    # - soma_dim_1: gene (var) coordinate
    process_batch(batch)
```

* *计算增量统计信息：**
```python
# Example: Calculate mean expression
n_observations = 0
sum_values = 0.0

iterator = query.X("raw").tables()
for batch in iterator:
    values = batch["soma_data"].to_numpy()
    n_observations += len(values)
    sum_values += values.sum()

mean_expression = sum_values / n_observations
```

### 5. 使用 PyTorch 进行机器学习

对于训练模型，请使用实验性 PyTorch集成：

```python
from cellxgene_census.experimental.ml import experiment_dataloader

with cellxgene_census.open_soma() as census:
    # Create dataloader
    dataloader = experiment_dataloader(
        census["census_data"]["homo_sapiens"],
        measurement_name="RNA",
        X_name="raw",
        obs_value_filter="tissue_general == 'liver' and is_primary_data == True",
        obs_column_names=["cell_type"],
        batch_size=128,
        shuffle=True,
    )

    # Training loop
    for epoch in range(num_epochs):
        for batch in dataloader:
            X = batch["X"]  # Gene expression tensor
            labels = batch["obs"]["cell_type"]  # Cell type labels

            # Forward pass
            outputs = model(X)
            loss = criterion(outputs, labels)

            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
```

* *训练/测试拆分：**
```python
from cellxgene_census.experimental.ml import ExperimentDataset

# Create dataset from experiment
dataset = ExperimentDataset(
    experiment_axis_query,
    layer_name="raw",
    obs_column_names=["cell_type"],
    batch_size=128,
)

# Split into train and test
train_dataset, test_dataset = dataset.random_split(
    split=[0.8, 0.2],
    seed=42
)
```

### 6. 与 Scanpy 集成

将人口普查数据与 scanpy 无缝集成工作流程：

```python
import scanpy as sc

# Load data from Census
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="cell_type == 'neuron' and tissue_general == 'cortex' and is_primary_data == True",
)

# Standard scanpy workflow
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)

# Dimensionality reduction
sc.pp.pca(adata, n_comps=50)
sc.pp.neighbors(adata)
sc.tl.umap(adata)

# Visualization
sc.pl.umap(adata, color=["cell_type", "tissue", "disease"])
```

### 7. 多数据集集成

查询并集成多个数据集：

```python
# Strategy 1: Query multiple tissues separately
tissues = ["lung", "liver", "kidney"]
adatas = []

for tissue in tissues:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter=f"tissue_general == '{tissue}' and is_primary_data == True",
    )
    adata.obs["tissue"] = tissue
    adatas.append(adata)

# Concatenate
combined = adatas[0].concatenate(adatas[1:])

# Strategy 2: Query multiple datasets directly
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="tissue_general in ['lung', 'liver', 'kidney'] and is_primary_data == True",
)
```

## 关键概念和最佳实践

### 始终过滤主要数据
除非分析重复项，否则始终在查询中包含 `is_primary_data == True` 以避免多次计算单元格：
```python
obs_value_filter="cell_type == 'B cell' and is_primary_data == True"
```

### 指定人口普查版本以实现再现性
始终在生产中指定人口普查版本分析：
```python
census = cellxgene_census.open_soma(census_version="2023-07-25")
```

### 在加载之前估计查询大小
对于大型查询，首先检查单元格数量以避免内存问题：
```python
# Get cell count
metadata = cellxgene_census.get_obs(
    census, "homo_sapiens",
    value_filter="tissue_general == 'brain' and is_primary_data == True",
    column_names=["soma_joinid"]
)
n_cells = len(metadata)
print(f"Query will return {n_cells:,} cells")

# If too large (>100k), use out-of-core processing
```

### 使用tissue_general进行更广泛的分组
The `tissue_general` 字段提供比 `tissue` 更粗略的类别，对于跨组织分析很有用：
```python
# Broader grouping
obs_value_filter="tissue_general == 'immune system'"

# Specific tissue
obs_value_filter="tissue == 'peripheral blood mononuclear cell'"
```

### 仅选择需要的列
通过仅指定所需的元数据来最小化数据传输列：
```python
obs_column_names=["cell_type", "tissue_general", "disease"]  # Not all columns
```

### 检查特定基因查询的数据集是否存在
分析特定基因时，验证哪些数据集测量了它们：
```python
presence = cellxgene_census.get_presence_matrix(
    census,
    "homo_sapiens",
    var_value_filter="feature_name in ['CD4', 'CD8A']"
)
```

### 两步工作流程：探索然后查询
首先探索元数据去理解可用数据，则查询表达式：
```python
# Step 1: Explore what's available
metadata = cellxgene_census.get_obs(
    census, "homo_sapiens",
    value_filter="disease == 'COVID-19' and is_primary_data == True",
    column_names=["cell_type", "tissue_general"]
)
print(metadata.value_counts())

# Step 2: Query based on findings
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="disease == 'COVID-19' and cell_type == 'T cell' and is_primary_data == True",
)
```

## 可用元数据字段

### 细胞元数据（obs）
过滤关键字段：
- `cell_type`、`cell_type_ontology_term_id`
- `tissue`、`tissue_general`、`tissue_ontology_term_id`
- `disease`、`disease_ontology_term_id`
- `assay`、`assay_ontology_term_id`
- `donor_id`、`sex`、`self_reported_ethnicity`
- `development_stage`、 `development_stage_ontology_term_id`
- `dataset_id`
- `is_primary_data`（布尔值：True = 唯一细胞）

### 基因元数据 (var)
- `feature_id`（Ensembl 基因 ID，例如， “ENSG00000161798”）
- `feature_name`（基因符号，例如“FOXP2”）
- `feature_length`（碱基对的基因长度）

## 参考文档

该技能包含详细的参考文档：

### references/census_schema.md
的综合文档：
- 人口普查数据结构和组织
- 所有可用的元数据字段
- 值过滤器语法和运算符
- SOMA 对象类型
- 数据包含标准

* *何时阅读：** 当您需要详细的架构信息、元数据字段的完整列表或复杂的过滤器语法时。

### 引用/common_patterns.md
的示例和模式：
- 探索性查询（仅限元数据）
- 中小型查询（AnnData）
- 大型查询（核外处理）
- PyTorch 集成
- Scanpy 集成工作流程
- 多数据集集成
- 最佳实践和常见陷阱

* *何时阅读：** 在实现特定查询模式、查找代码示例或排除常见问题时。

## 常用案例

### 用例 1：探索组织中的细胞类型
```python
with cellxgene_census.open_soma() as census:
    cells = cellxgene_census.get_obs(
        census, "homo_sapiens",
        value_filter="tissue_general == 'lung' and is_primary_data == True",
        column_names=["cell_type"]
    )
    print(cells["cell_type"].value_counts())
```

### 用例 2：查询标记基因表达
```python
with cellxgene_census.open_soma() as census:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        var_value_filter="feature_name in ['CD4', 'CD8A', 'CD19']",
        obs_value_filter="cell_type in ['T cell', 'B cell'] and is_primary_data == True",
    )
```

### 用例 3：训练细胞类型分类器
```python
from cellxgene_census.experimental.ml import experiment_dataloader

with cellxgene_census.open_soma() as census:
    dataloader = experiment_dataloader(
        census["census_data"]["homo_sapiens"],
        measurement_name="RNA",
        X_name="raw",
        obs_value_filter="is_primary_data == True",
        obs_column_names=["cell_type"],
        batch_size=128,
        shuffle=True,
    )

    # Train model
    for epoch in range(epochs):
        for batch in dataloader:
            # Training logic
            pass
```

### 用例4：跨组织分析
```python
with cellxgene_census.open_soma() as census:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter="cell_type == 'macrophage' and tissue_general in ['lung', 'liver', 'brain'] and is_primary_data == True",
    )

    # Analyze macrophage differences across tissues
    sc.tl.rank_genes_groups(adata, groupby="tissue_general")
```

## 故障排除

### 查询返回太多单元格
- 添加更多特定过滤器以缩小范围
- 使用 `tissue` 而不是 `tissue_general` 以获得更细的粒度
- 如果已知，则按特定 `dataset_id` 过滤
- 对于大型查询切换到核外处理

### 内存错误
- 使用更严格的过滤器减少查询范围
- 使用 `var_value_filter`
 选择更少的基因- 使用 `axis_query()`
- 批量处理数据

### 结果中的重复单元格
- 始终包含过滤器中的 `is_primary_data == True`
- 检查是否有意跨多个数据集查询

### Gene Not Found
- 验证基因名称拼写（区分大小写）
- 尝试使用 `feature_id` 而不是 `feature_name`
- 检查数据集存在矩阵，查看基因是否被测量
- 一些基因可能在普查构建期间被过滤

### 版本不一致
- 始终明确指定 `census_version`
- 在所有分析中使用相同版本
- 检查发行说明以了解特定于版本的更改
