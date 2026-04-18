---
name: lamindb
description: 在使用 LaminDB 时应使用此技能，LaminDB 是一个生物学开源数据框架，使数据可查询、可追踪、可重现且公平。在管理生物数据集（scRNA-seq、空间、流式细胞术等）、跟踪计算工作流程、使用生物本体整理和验证数据、构建数据湖房或确保生物研究中的数据沿袭和可重复性时使用。涵盖数据管理、注释、本体（基因、细胞类型、疾病、组织）、模式验证、与工作流程管理器（Nextflow、Snakemake）和 MLOps 平台（W&B、MLflow）的集成以及部署策略。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# LaminDB

## 概述

LaminDB 是一个生物学开源数据框架，旨在使数据可查询、可追踪、可再现和 FAIR（可查找、可访问、可互操作、可重用）。它提供了一个统一的平台，通过单个 Python API 将 Lakehouse 架构、谱系跟踪、特征存储、生物本体、LIMS（实验室信息管理系统）和 ELN（电子实验室笔记本）功能结合在一起。

* *核心价值主张：**
- **可查询性**：按元数据、特征和本体术语搜索和过滤数据集
- **可追溯性**：从原始数据自动进行谱系跟踪从数据到结果的分析
- **再现性**：数据、代码和环境的版本控制
- **公平合规性**：使用生物本体进行标准化注释

## 何时使用此技能

在以下情况下使用此技能：

- **管理生物数据集**：scRNA-seq、bulk RNA-seq、空间转录组学、流式细胞术细胞计数、多模式数据、EHR 数据
- **跟踪计算工作流程**：笔记本、脚本、管道执行（Nextflow、Snakemake、Redun）
- **整理和验证数据**：模式验证、标准化、基于本体的注释
- **使用生物本体**：基因、蛋白质、细胞类型、组织、疾病、途径（通过Bionty)
- **构建数据 Lakehouse**：跨多个数据集的统一查询接口
- **确保可重复性**：自动版本控制、沿袭跟踪、环境捕获
- **集成 ML 管道**：连接权重和偏差、MLflow、HuggingFace、scVI-tools
- **部署数据基础设施**：设置本地或基于云的数据管理系统
- **数据集协作**：使用标准化元数据共享精选的带注释的数据

## 核心功能

LaminDB 提供了六个互连的功能区域，每个功能区域都详细记录在参考文件夹中。

### 1. 核心概念和数据沿袭

* *核心实体：**
- **工件**：版本化数据集（DataFrame、AnnData、Parquet、Zarr 等）
- **记录**：实验实体（样本、扰动、仪器）
- **运行和转换**：计算谱系跟踪（哪些代码生成哪些数据）
- **功能**：用于注释和查询的键入元数据字段

  * *关键工作流程：**
- 从文件或Python创建和版本工件对象
- 使用`ln.track()`和`ln.finish()`
跟踪笔记本/脚本执行-使用类型化特征注释工件
- 使用`artifact.view_lineage()`
可视化数据沿袭图-按出处查询（查找特定的所有输出）代码/输入）

* *参考：** `references/core-concepts.md` - 阅读此内容以获取有关工件、记录、运行、转换、功能、版本控制和沿袭跟踪的详细信息。

### 2. 数据管理和查询

* *查询功能：**
- 注册表探索和查找自动完成
- 使用`get()`、`one()`、`one_or_none()`
进行单记录检索-使用比较运算符进行过滤（`__gt`、`__lte`、`__contains`、`__startswith`）
- 基于特征的查询（通过带注释的元数据查询）
- 使用双下划线语法进行跨注册表遍历
- 跨注册表全文搜索
- 使用 Q 对象进行高级逻辑查询（AND、OR、NOT）
- 流式传输大型数据集而不加载到内存中

* *Key工作流程：**
- 使用过滤器和排序浏览工件
- 按功能、创建日期、创建者、大小等查询。
- 以块或数组切片流式传输大型文件
- 使用分层键组织数据
- 将工件分组到集合中

* *参考：** `references/data-management.md` - 阅读此内容以获取全面的查询模式、过滤示例、流策略和数据组织最佳实践。

### 3.注释和验证

* *管理过程：**
1. **验证**：确认数据集与所需模式
2匹配。 **标准化**：修复拼写错误，将同义词映射到规范术语
3. **注释**：将数据集链接到元数据实体以实现可查询性

* *模式类型：**
- **灵活模式**：仅验证已知列，允许附加元数据
- **所需最少模式**：指定基本列，允许额外
- **严格模式**：对结构和值的完全控制

  * *支持的数据类型：**
- DataFrames（Parquet、CSV）
- AnnData（单细胞基因组学）
- MuData（多模式）
- SpatialData（空间转录组学）
- TileDB-SOMA（可扩展）数组）

* *关键工作流程：**
- 定义数据验证的特征和模式
- 使用 `DataFrameCurator` 或 `AnnDataCurator` 进行验证
- 使用 `.cat.standardize()`
 标准化值 - 映射到本体`.cat.add_ontology()`
- 使用模式链接保存精选工件
- 按功能查询经过验证的数据集

* *参考：** `references/annotation-validation.md` - 阅读本文以了解详细的精选工作流程、模式设计模式、处理验证错误和最佳实践。

### 4. 生物学本体

* *可用本体（通过Bionty）：**
- 基因（Ensembl）、蛋白质（UniProt）
- 细胞类型（CL）、细胞系（CLO）
- 组织（Uberon）、疾病（Mondo、DOID）
- 表型(HPO)、途径 (GO)
- 实验因素 (EFO)、发育阶段
- 生物体 (NCBItaxon)、药物 (DrugBank)

* *关键工作流程：**
- 使用 `bt.CellType.import_source()`
 导入公共本体 - 使用关键字或精确匹配搜索本体
- 使用同义词映射标准化术语
- 探索层次关系（父母、子女、祖先）
- 根据本体术语验证数据
- 注释数据集包含本体记录
- 创建自定义术语和层次结构
- 处理多生物体上下文（人类、小鼠等）

* *参考：** `references/ontologies.md` - 阅读此内容以了解全面的本体操作、标准化策略、层次结构导航和注释工作流程。

### 5. 集成

* *工作流程经理：**
- Nextflow：跟踪管道流程和输出
- Snakemake：集成到 Snakemake 规则中
- Redun：与 Redun 任务跟踪相结合

* *MLOps 平台：**
- 权重和偏差：将实验与数据工件链接起来
- MLflow：跟踪模型和实验
- HuggingFace：跟踪模型微调
- scVI-tools：单细胞分析工作流程

* *存储系统：**
- 本地文件系统、AWS S3、Google Cloud Storage
- S3 兼容（MinIO、Cloudflare） R2)
- HTTP/HTTPS 端点（只读）
- HuggingFace 数据集

* *数组存储：**
- TileDB-SOMA（支持 cellxgene）
- 用于 Parquet 上 SQL 查询的 DuckDB文件

* *可视化：**
- 用于交互式空间/单细胞可视化的 Vitessce

* *版本控制：**
- 用于源代码跟踪的 Git 集成

* *参考：** `references/integrations.md` - 阅读此内容以了解第三方的集成模式、代码示例和故障排除systems.

### 6. 设置和部署

* *安装：**
- 基本：`uv pip install lamindb`
- 带有附加功能：`uv pip install 'lamindb[gcp,zarr,fcs]'`
- 模块：bionty、wetlab、clinical

* *实例类型：**
- 本地SQLite（开发）
- 云存储+SQLite（小团队）
- 云存储+PostgreSQL（生产）

* *存储选项：**
- 本地文件系统
- 具有可配置区域和权限的 AWS S3
- Google Cloud Storage
- S3 兼容端点（MinIO、Cloudflare R2）

* *配置：**
- 云文件的缓存管理
- 多用户系统配置
- Git 存储库同步
- 环境变量

* *部署模式：**
- 本地开发 → 云生产迁移
- 多区域部署
- 与个人实例共享存储

* *参考：** `references/setup-deployment.md` - 阅读此内容以了解详细安装，配置、存储设置、数据库管理、安全最佳实践和故障排除。

## 常见用例工作流程

### 用例 1：使用本体验证进行单细胞 RNA-seq 分析

```python
import lamindb as ln
import bionty as bt
import anndata as ad

# Start tracking
ln.track(params={"analysis": "scRNA-seq QC and annotation"})

# Import cell type ontology
bt.CellType.import_source()

# Load data
adata = ad.read_h5ad("raw_counts.h5ad")

# Validate and standardize cell types
adata.obs["cell_type"] = bt.CellType.standardize(adata.obs["cell_type"])

# Curate with schema
curator = ln.curators.AnnDataCurator(adata, schema)
curator.validate()
artifact = curator.save_artifact(key="scrna/validated.h5ad")

# Link ontology annotations
cell_types = bt.CellType.from_values(adata.obs.cell_type)
artifact.feature_sets.add_ontology(cell_types)

ln.finish()
```

### 用例 2：构建可查询数据Lakehouse

```python
import lamindb as ln

# Register multiple experiments
for i, file in enumerate(data_files):
    artifact = ln.Artifact.from_anndata(
        ad.read_h5ad(file),
        key=f"scrna/batch_{i}.h5ad",
        description=f"scRNA-seq batch {i}"
    ).save()

    # Annotate with features
    artifact.features.add_values({
        "batch": i,
        "tissue": tissues[i],
        "condition": conditions[i]
    })

# Query across all experiments
immune_datasets = ln.Artifact.filter(
    key__startswith="scrna/",
    tissue="PBMC",
    condition="treated"
).to_dataframe()

# Load specific datasets
for artifact in immune_datasets:
    adata = artifact.load()
    # Analyze
```

### 用例 3：具有 W&B 集成的 ML 管道

```python
import lamindb as ln
import wandb

# Initialize both systems
wandb.init(project="drug-response", name="exp-42")
ln.track(params={"model": "random_forest", "n_estimators": 100})

# Load training data from LaminDB
train_artifact = ln.Artifact.get(key="datasets/train.parquet")
train_data = train_artifact.load()

# Train model
model = train_model(train_data)

# Log to W&B
wandb.log({"accuracy": 0.95})

# Save model in LaminDB with W&B linkage
import joblib
joblib.dump(model, "model.pkl")
model_artifact = ln.Artifact("model.pkl", key="models/exp-42.pkl").save()
model_artifact.features.add_values({"wandb_run_id": wandb.run.id})

ln.finish()
wandb.finish()
```

### 用例 4：Nextflow 管道集成

```python
# In Nextflow process script
import lamindb as ln

ln.track()

# Load input artifact
input_artifact = ln.Artifact.get(key="raw/batch_${batch_id}.fastq.gz")
input_path = input_artifact.cache()

# Process (alignment, quantification, etc.)
# ... Nextflow process logic ...

# Save output
output_artifact = ln.Artifact(
    "counts.csv",
    key="processed/batch_${batch_id}_counts.csv"
).save()

ln.finish()
```

## 入门检查清单

要开始有效使用LaminDB：

1. **安装和设置** (`references/setup-deployment.md`)
  - 安装 LaminDB 和所需的附加组件
  - 使用 `lamin login`
 进行身份验证 - 使用 `lamin init --storage ...`

2 初始化实例。 **学习核心概念** (`references/core-concepts.md`)
 - 了解工件、记录、运行、转换
  - 练习创建和检索工件
  - 在工作流程中实施 `ln.track()` 和 `ln.finish()`

3. **掌握查询** (`references/data-management.md`)
  - 练习过滤和搜索注册表
  - 学习基于特征的查询
  - 实验流式传输大文件

4. **设置验证** (`references/annotation-validation.md`)
  - 定义与研究领域相关的功能
  - 为数据类型创建模式
  - 实践管理工作流程

5. **集成本体** (`references/ontologies.md`)
  - 导入相关生物本体（基因、细胞类型等）
  - 验证现有注释
  - 使用本体术语标准化元数据

6. **连接工具** (`references/integrations.md`)
  - 与现有工作流程管理器集成
  - 链接用于实验跟踪的 ML 平台
  - 配置云存储和计算

## 关键原则

使用 LaminDB:

1 时请遵循这些原则。 **跟踪一切**：在每次分析开始时使用 `ln.track()` 进行自动谱系捕获 

2. **尽早验证**：在广泛分析之前定义模式并验证数据

3. **使用本体**：利用公共生物本体进行标准化注释

4. **使用键组织**：按层次结构构建工件键（例如，`project/experiment/batch/file.h5ad`）

5. **先查询元数据**：在加载大文件之前进行过滤和搜索

6. **版本，不要重复**：使用内置版本控制而不是创建新密钥进行修改

7. **使用特征进行注释**：为可查询元数据定义类型化特征

8. **彻底记录**：添加对工件、模式和转换的描述

9. **利用沿袭**：使用 `view_lineage()` 了解数据来源 

10. **启动本地，扩展云**：使用 SQLite 进行本地开发，使用 PostgreSQL 部署到云

## 参考文件

此技能包括按功能组织的综合参考文档：

- **`references/core-concepts.md`** - 工件、记录、运行、转换、功能、版本控制、沿袭
- **`references/data-management.md`** - 查询、过滤、搜索、流式传输、组织数据
- **`references/annotation-validation.md`** - 架构设计、管理工作流程、验证策略
- **`references/ontologies.md`** - 生物本体管理、标准化、层次结构
- **`references/integrations.md`** - 工作流程管理器、MLOps 平台、存储系统、工具
- **`references/setup-deployment.md`** - 安装、配置、部署、故障排除

根据具体情况阅读相关参考文件手头任务所需的 LaminDB 功能。

## 其他资源

- **官方文档**：https://docs.lamin.ai
- **API 参考**：https://docs.lamin.ai/api
- **GitHub 存储库**：https://github.com/laminlabs/lamindb
- **教程**：https://docs.lamin.ai/tutorial
  - **常见问题解答**：https://docs.lamin.ai/faq
