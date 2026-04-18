# LaminDB 集成

本文档涵盖了 LaminDB 与工作流管理器、MLOps 平台、可视化工具和其他第三方系统的集成。

## 概述

LaminDB 支持跨数据存储、计算工作流、机器学习平台和可视化工具的广泛集成，从而能够无缝融入现有的数据科学和生物信息学pipelines.

## 数据存储集成

### 本地文件系统

```python
import lamindb as ln

# Initialize with local storage
lamin init --storage ./mydata

# Save artifacts to local storage
artifact = ln.Artifact("data.csv", key="local/data.csv").save()

# Load from local storage
data = artifact.load()
```

### AWS S3

```python
# Initialize with S3 storage
lamin init --storage s3://my-bucket/path \
  --db postgresql://user:pwd@host:port/db

# Artifacts automatically sync to S3
artifact = ln.Artifact("data.csv", key="experiments/data.csv").save()

# Transparent S3 access
data = artifact.load()  # Downloads from S3 if not cached
```

### S3 兼容服务

支持 MinIO、Cloudflare R2 等S3 兼容端点：

```python
# Initialize with custom S3 endpoint
lamin init --storage 's3://bucket?endpoint_url=http://minio.example.com:9000'

# Configure credentials
export AWS_ACCESS_KEY_ID=minioadmin
export AWS_SECRET_ACCESS_KEY=minioadmin
```

### Google Cloud Storage

```python
# Install GCP extras
pip install 'lamindb[gcp]'

# Initialize with GCS
lamin init --storage gs://my-bucket/path \
  --db postgresql://user:pwd@host:port/db

# Artifacts sync to GCS
artifact = ln.Artifact("data.csv", key="experiments/data.csv").save()
```

### HTTP/HTTPS（只读）

```python
# Access remote files without copying
artifact = ln.Artifact(
    "https://example.com/data.csv",
    key="remote/data.csv"
).save()

# Stream remote content
with artifact.open() as f:
    data = f.read()
```

### HuggingFace数据集

```python
# Access HuggingFace datasets
from datasets import load_dataset

dataset = load_dataset("squad", split="train")

# Register as LaminDB artifact
artifact = ln.Artifact.from_dataframe(
    dataset.to_pandas(),
    key="hf/squad_train.parquet",
    description="SQuAD training data from HuggingFace"
).save()
```

## Workflow Manager 集成

### Nextflow

跟踪 Nextflow 管道执行和输出：

```python
# In your Nextflow process script
import lamindb as ln

# Initialize tracking
ln.track()

# Your Nextflow process logic
input_artifact = ln.Artifact.get(key="${input_key}")
data = input_artifact.load()

# Process data
result = process_data(data)

# Save output
output_artifact = ln.Artifact.from_dataframe(
    result,
    key="${output_key}"
).save()

ln.finish()
```

* *Nextflow 配置示例：**
```nextflow
process ANALYZE {
    input:
    val input_key

    output:
    path "result.csv"

    script:
    """
    #!/usr/bin/env python
    import lamindb as ln
    ln.track()
    artifact = ln.Artifact.get(key="${input_key}")
    # Process and save
    ln.finish()
    """
}
```

### Snakemake

将 LaminDB 集成到 Snakemake 工作流程中：

```python
# In Snakemake rule
rule process_data:
    input:
        "data/input.csv"
    output:
        "data/output.csv"
    run:
        import lamindb as ln

        ln.track()

        # Load input artifact
        artifact = ln.Artifact.get(key="inputs/data.csv")
        data = artifact.load()

        # Process
        result = analyze(data)

        # Save output
        result.to_csv(output[0])
        ln.Artifact(output[0], key="outputs/result.csv").save()

        ln.finish()
```

### Redun

Track Redun 任务执行：

```python
from redun import task
import lamindb as ln

@task()
@ln.tracked()
def process_dataset(input_key: str, output_key: str):
    """Redun task with LaminDB tracking."""
    # Load input
    artifact = ln.Artifact.get(key=input_key)
    data = artifact.load()

    # Process
    result = transform(data)

    # Save output
    ln.Artifact.from_dataframe(result, key=output_key).save()

    return output_key

# Redun automatically tracks lineage alongside LaminDB
```

## MLOps 平台集成

### 权重和偏差 (W&B)

将 W&B 实验跟踪与 LaminDB 数据管理相结合：

```python
import wandb
import lamindb as ln

# Initialize both
wandb.init(project="my-project", name="experiment-1")
ln.track(params={"learning_rate": 0.01, "batch_size": 32})

# Load training data
train_artifact = ln.Artifact.get(key="datasets/train.parquet")
train_data = train_artifact.load()

# Train model
model = train_model(train_data)

# Log to W&B
wandb.log({"accuracy": 0.95, "loss": 0.05})

# Save model in LaminDB
import joblib
joblib.dump(model, "model.pkl")
model_artifact = ln.Artifact(
    "model.pkl",
    key="models/experiment-1.pkl",
    description=f"Model from W&B run {wandb.run.id}"
).save()

# Link W&B run ID
model_artifact.features.add_values({"wandb_run_id": wandb.run.id})

ln.finish()
wandb.finish()
```

### MLflow

将MLflow模型跟踪与LaminDB集成：

```python
import mlflow
import lamindb as ln

# Start runs
mlflow.start_run()
ln.track()

# Log parameters to both
params = {"max_depth": 5, "n_estimators": 100}
mlflow.log_params(params)
ln.context.params = params

# Load data from LaminDB
data_artifact = ln.Artifact.get(key="datasets/features.parquet")
X = data_artifact.load()

# Train and log model
model = train_model(X)
mlflow.sklearn.log_model(model, "model")

# Save to LaminDB
import joblib
joblib.dump(model, "model.pkl")
model_artifact = ln.Artifact(
    "model.pkl",
    key=f"models/{mlflow.active_run().info.run_id}.pkl"
).save()

mlflow.end_run()
ln.finish()
```

### HuggingFace Transformers

跟踪模型微调LaminDB:

```python
from transformers import Trainer, TrainingArguments
import lamindb as ln

ln.track(params={"model": "bert-base", "epochs": 3})

# Load training data
train_artifact = ln.Artifact.get(key="datasets/train_tokenized.parquet")
train_dataset = train_artifact.load()

# Configure trainer
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

# Train
trainer.train()

# Save model to LaminDB
trainer.save_model("./model")
model_artifact = ln.Artifact(
    "./model",
    key="models/bert_finetuned",
    description="BERT fine-tuned on custom dataset"
).save()

ln.finish()
```

### scVI-tools

使用 scVI 和 LaminDB:

```python
import scvi
import lamindb as ln

ln.track()

# Load data
adata_artifact = ln.Artifact.get(key="scrna/raw_counts.h5ad")
adata = adata_artifact.load()

# Setup scVI
scvi.model.SCVI.setup_anndata(adata, layer="counts")

# Train model
model = scvi.model.SCVI(adata)
model.train()

# Save latent representation
adata.obsm["X_scvi"] = model.get_latent_representation()

# Save results
result_artifact = ln.Artifact.from_anndata(
    adata,
    key="scrna/scvi_latent.h5ad",
    description="scVI latent representation"
).save()

ln.finish()
```

## 数组存储集成

### TileDB-SOMA

可扩展的数组存储，支持cellxgene：

```python
import tiledbsoma as soma
import lamindb as ln

# Create SOMA experiment
uri = "tiledb://my-namespace/experiment"

with soma.Experiment.create(uri) as exp:
    # Add measurements
    exp.add_new_collection("RNA")

    # Register in LaminDB
    artifact = ln.Artifact(
        uri,
        key="cellxgene/experiment.soma",
        description="TileDB-SOMA experiment"
    ).save()

# Query with SOMA
with soma.Experiment.open(uri) as exp:
    obs = exp.obs.read().to_pandas()
```

### DuckDB

使用DuckDB查询工件：

```python
import duckdb
import lamindb as ln

# Get artifact
artifact = ln.Artifact.get(key="datasets/large_data.parquet")

# Query with DuckDB (without loading full file)
path = artifact.cache()
result = duckdb.query(f"""
    SELECT cell_type, COUNT(*) as count
    FROM read_parquet('{path}')
    GROUP BY cell_type
    ORDER BY count DESC
""").to_df()

# Save query result
result_artifact = ln.Artifact.from_dataframe(
    result,
    key="analysis/cell_type_counts.parquet"
).save()
```

## 可视化集成

### Vitessce

创建交互式可视化：

```python
from vitessce import VitessceConfig
import lamindb as ln

# Load spatial data
artifact = ln.Artifact.get(key="spatial/visium_slide.h5ad")
adata = artifact.load()

# Create Vitessce configuration
vc = VitessceConfig.from_object(adata)

# Save configuration
import json
config_file = "vitessce_config.json"
with open(config_file, "w") as f:
    json.dump(vc.to_dict(), f)

# Register configuration
config_artifact = ln.Artifact(
    config_file,
    key="visualizations/spatial_config.json",
    description="Vitessce visualization config"
).save()
```

## 架构模块集成

### Bionty（生物本体）

```python
import bionty as bt

# Import biological ontologies
bt.CellType.import_source()
bt.Gene.import_source(organism="human")

# Use in data curation
cell_types = bt.CellType.from_values(adata.obs.cell_type)
```

### WetLab

跟踪湿实验室实验：

```python
# Install wetlab module
pip install 'lamindb[wetlab]'

# Use wetlab registries
import lamindb_wetlab as wetlab

# Track experiments, samples, protocols
experiment = wetlab.Experiment(name="RNA-seq batch 1").save()
```

### 临床数据 (OMOP)

```python
# Install clinical module
pip install 'lamindb[clinical]'

# Use OMOP common data model
import lamindb_clinical as clinical

# Track clinical data
patient = clinical.Patient(patient_id="P001").save()
```

## Git 集成

### 与 Git 存储库同步

```python
# Configure git sync
export LAMINDB_SYNC_GIT_REPO=https://github.com/user/repo.git

# Or programmatically
ln.settings.sync_git_repo = "https://github.com/user/repo.git"

# Set development directory
lamin settings set dev-dir .

# Scripts tracked with git commits
ln.track()  # Automatically captures git commit hash
# ... your code ...
ln.finish()

# View git information
transform = ln.Transform.get(name="analysis.py")
transform.source_code  # Shows code at git commit
transform.hash        # Git commit hash
```

## 企业集成

### Benchling

与 Benchling 注册表同步（需要团队/企业） plan):

```python
# Configure Benchling connection (contact LaminDB team)
# Syncs schemas and data from Benchling registries

# Access synced Benchling data
# Details available through enterprise support
```

## 自定义集成模式

### REST API 集成

```python
import requests
import lamindb as ln

ln.track()

# Fetch from API
response = requests.get("https://api.example.com/data")
data = response.json()

# Convert to DataFrame
import pandas as pd
df = pd.DataFrame(data)

# Save to LaminDB
artifact = ln.Artifact.from_dataframe(
    df,
    key="api/fetched_data.parquet",
    description="Data fetched from external API"
).save()

artifact.features.add_values({"api_url": response.url})

ln.finish()
```

### 数据库集成

```python
import sqlalchemy as sa
import lamindb as ln

ln.track()

# Connect to external database
engine = sa.create_engine("postgresql://user:pwd@host:port/db")

# Query data
query = "SELECT * FROM experiments WHERE date > '2025-01-01'"
df = pd.read_sql(query, engine)

# Save to LaminDB
artifact = ln.Artifact.from_dataframe(
    df,
    key="external_db/experiments_2025.parquet",
    description="Experiments from external database"
).save()

ln.finish()
```

## 羊角面包元数据

使用Croissant元数据格式导出数据集：

```python
# Create artifact with rich metadata
artifact = ln.Artifact.from_dataframe(
    df,
    key="datasets/published_data.parquet",
    description="Published dataset with Croissant metadata"
).save()

# Export Croissant metadata (requires additional configuration)
# Enables dataset discovery and interoperability
```

## 集成最佳实践

1. **一致跟踪**：在所有集成工作流程
2中使用`ln.track()`。 **链接 ID**：将外部系统 ID（W&B 运行 ID、MLflow 实验 ID）存储为 features
3. **集中数据**：使用 LaminDB 作为数据工件 
4 的单一事实来源。 **同步参数**：将参数记录到 LaminDB 和 ML 平台
5. **版本在一起**：将代码（git）、数据（LaminDB）和实验（ML平台）保存在sync
6中。 **策略性缓存**：为云存储
7配置适当的缓存位置。 **使用功能集**：将 Bionty 的本体术语链接到工件 
8. **文档集成**：添加解释集成上下文
9 的描述。 **增量测试**：首先验证与小数据集的集成
10. **监控沿袭**：使用 `view_lineage()` 确保集成跟踪正常工作

## 常见问题故障排除

* *问题：找不到 S3 凭据**
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

* *问题：GCS 身份验证失败**
```bash
gcloud auth application-default login
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

* *问题：Git 同步不起作用**
```bash
# Ensure git repo is set
lamin settings get sync-git-repo

# Ensure you're in git repo
git status

# Commit changes before tracking
git add .
git commit -m "Update analysis"
ln.track()
```

* *问题：MLflow 工件未同步**
```python
# Save explicitly to both systems
mlflow.log_artifact("model.pkl")
ln.Artifact("model.pkl", key="models/model.pkl").save()
```
