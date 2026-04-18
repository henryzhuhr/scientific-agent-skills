# 常用工作流程和最佳实践

本文档涵盖了 scvi-tools.

## 标准分析工作流程

### 1. 数据加载和准备

```python
import scvi
import scanpy as sc
import numpy as np

# Load data (AnnData format required)
adata = sc.read_h5ad("data.h5ad")
# Or load from other formats
# adata = sc.read_10x_mtx("filtered_feature_bc_matrix/")
# adata = sc.read_csv("counts.csv")

# Basic QC metrics
sc.pp.calculate_qc_metrics(adata, inplace=True)
adata.var['mt'] = adata.var_names.str.startswith('MT-')
sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], inplace=True)
```

### 2. 质量的常见工作流程、最佳实践和高级使用模式Control

```python
# Filter cells
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_cells(adata, max_genes=5000)

# Filter genes
sc.pp.filter_genes(adata, min_cells=3)

# Filter by mitochondrial content
adata = adata[adata.obs['pct_counts_mt'] < 20, :]

# Remove doublets (optional, before training)
sc.external.pp.scrublet(adata)
adata = adata[~adata.obs['predicted_doublet'], :]
```

### 3. scvi-tools的预处理

```python
# IMPORTANT: scvi-tools needs RAW counts
# If you've already normalized, use the raw layer or reload data

# Save raw counts if not already available
if 'counts' not in adata.layers:
    adata.layers['counts'] = adata.X.copy()

# Feature selection (optional but recommended)
sc.pp.highly_variable_genes(
    adata,
    n_top_genes=4000,
    subset=False,  # Keep all genes, just mark HVGs
    batch_key="batch"  # If multiple batches
)

# Filter to HVGs (optional)
# adata = adata[:, adata.var['highly_variable']]
```

### 4. 使用scvi-tools注册数据

```python
# Setup AnnData for scvi-tools
scvi.model.SCVI.setup_anndata(
    adata,
    layer="counts",  # Use raw counts
    batch_key="batch",  # Technical batches
    categorical_covariate_keys=["donor", "condition"],
    continuous_covariate_keys=["percent_mito", "n_counts"]
)

# Check registration
adata.uns['_scvi']['summary_stats']
```

### 5. 模型训练

```python
# Create model
model = scvi.model.SCVI(
    adata,
    n_latent=30,  # Latent dimensions
    n_layers=2,   # Network depth
    n_hidden=128, # Hidden layer size
    dropout_rate=0.1,
    gene_likelihood="zinb"  # zero-inflated negative binomial
)

# Train model
model.train(
    max_epochs=400,
    batch_size=128,
    train_size=0.9,
    early_stopping=True,
    check_val_every_n_epoch=10
)

# View training history
train_history = model.history["elbo_train"]
val_history = model.history["elbo_validation"]
```

### 6. 提取结果

```python
# Get latent representation
latent = model.get_latent_representation()
adata.obsm["X_scVI"] = latent

# Get normalized expression
normalized = model.get_normalized_expression(
    adata,
    library_size=1e4,
    n_samples=25  # Monte Carlo samples
)
adata.layers["scvi_normalized"] = normalized
```

### 7. 下游分析

```python
# Clustering on scVI latent space
sc.pp.neighbors(adata, use_rep="X_scVI", n_neighbors=15)
sc.tl.umap(adata, min_dist=0.3)
sc.tl.leiden(adata, resolution=0.8, key_added="leiden")

# Visualization
sc.pl.umap(adata, color=["leiden", "batch", "cell_type"])

# Differential expression
de_results = model.differential_expression(
    groupby="leiden",
    group1="0",
    group2="1",
    mode="change",
    delta=0.25
)
```

### 8. 模型持久性

```python
# Save model
model_dir = "./scvi_model/"
model.save(model_dir, overwrite=True)

# Save AnnData with results
adata.write("analyzed_data.h5ad")

# Load model later
model = scvi.model.SCVI.load(model_dir, adata=adata)
```

## 超参数调整

### 关键超参数

* *架构**：
- `n_latent`：潜在空间维度（10-50）
  - 对于复杂、异构而言较大数据集
  - 对于简单数据集较小或防止过度拟合
- `n_layers`：隐藏层数量 (1-3)
  - 用于复杂数据的更多层，但收益递减
- `n_hidden`：每个隐藏层的节点 (64-256)
  - 缩放数据集大小和复杂性

* *训练**：
- `max_epochs`：训练迭代（200-500）
  - 使用早期停止来防止过度拟合
- `batch_size`：每批样本（64-256）
  - 对于大数据集较大，较小对于有限的内存
- `lr`：学习率（默认为0.001，通常很好）

* *特定于模型**：
- `gene_likelihood`：分布（“zinb”，“nb”，“poisson”）
  - “zinb”用于稀疏数据零膨胀
  - “nb”表示稀疏数据
- `dispersion`：基因或基因批次特定
  - “基因”表示简单，“基因批次”表示复杂批次效应

### 超参数搜索示例

```python
from scvi.model import SCVI

# Define search space
latent_dims = [10, 20, 30]
n_layers_options = [1, 2]

best_score = float('-inf')
best_params = None

for n_latent in latent_dims:
    for n_layers in n_layers_options:
        model = SCVI(
            adata,
            n_latent=n_latent,
            n_layers=n_layers
        )
        model.train(max_epochs=200)

        # Evaluate on validation set
        val_elbo = model.history["elbo_validation"][-1]

        if val_elbo > best_score:
            best_score = val_elbo
            best_params = {"n_latent": n_latent, "n_layers": n_layers}

print(f"Best params: {best_params}")
```

### 使用Optuna进行超参数优化

```python
import optuna

def objective(trial):
    n_latent = trial.suggest_int("n_latent", 10, 50)
    n_layers = trial.suggest_int("n_layers", 1, 3)
    n_hidden = trial.suggest_categorical("n_hidden", [64, 128, 256])

    model = scvi.model.SCVI(
        adata,
        n_latent=n_latent,
        n_layers=n_layers,
        n_hidden=n_hidden
    )

    model.train(max_epochs=200, early_stopping=True)
    return model.history["elbo_validation"][-1]

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=20)

print(f"Best parameters: {study.best_params}")
```

## GPU加速

### 启用GPU训练

```python
# Automatic GPU detection
model = scvi.model.SCVI(adata)
model.train(accelerator="auto")  # Uses GPU if available

# Force GPU
model.train(accelerator="gpu")

# Multi-GPU
model.train(accelerator="gpu", devices=2)

# Check if GPU is being used
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")
```

### GPU内存管理

```python
# Reduce batch size if OOM
model.train(batch_size=64)  # Instead of default 128

# Mixed precision training (saves memory)
model.train(precision=16)

# Clear cache between runs
import torch
torch.cuda.empty_cache()
```

## 批量集成策略

### 策略1：简单批量密钥

```python
# For standard batch correction
scvi.model.SCVI.setup_anndata(adata, batch_key="batch")
model = scvi.model.SCVI(adata)
```

### 策略2：多个协变量

```python
# Correct for multiple technical factors
scvi.model.SCVI.setup_anndata(
    adata,
    batch_key="sequencing_batch",
    categorical_covariate_keys=["donor", "tissue"],
    continuous_covariate_keys=["percent_mito"]
)
```

### 策略 3：分层批次

```python
# When batches have hierarchical structure
# E.g., samples within studies
adata.obs["batch_hierarchy"] = (
    adata.obs["study"].astype(str) + "_" +
    adata.obs["sample"].astype(str)
)

scvi.model.SCVI.setup_anndata(adata, batch_key="batch_hierarchy")
```

## 参考映射 (scArches)

### 训练参考模型

```python
# Train on reference dataset
scvi.model.SCVI.setup_anndata(ref_adata, batch_key="batch")
ref_model = scvi.model.SCVI(ref_adata)
ref_model.train()

# Save reference
ref_model.save("reference_model")
```

### 将查询映射到参考

```python
# Load reference
ref_model = scvi.model.SCVI.load("reference_model", adata=ref_adata)

# Setup query with same parameters
scvi.model.SCVI.setup_anndata(query_adata, batch_key="batch")

# Transfer learning
query_model = scvi.model.SCVI.load_query_data(
    query_adata,
    "reference_model"
)

# Fine-tune on query (optional)
query_model.train(max_epochs=200)

# Get query embeddings
query_latent = query_model.get_latent_representation()

# Transfer labels using KNN
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=15)
knn.fit(ref_model.get_latent_representation(), ref_adata.obs["cell_type"])
query_adata.obs["predicted_cell_type"] = knn.predict(query_latent)
```

## 模型缩小

减少模型大小以加快推理速度：

```python
# Train full model
model = scvi.model.SCVI(adata)
model.train()

# Minify for deployment
minified = model.minify_adata(adata)

# Save minified version
minified.write("minified_data.h5ad")
model.save("minified_model")

# Load and use (much faster)
mini_model = scvi.model.SCVI.load("minified_model", adata=minified)
```

## 内存高效数据加载

### 使用AnnDataLoader

```python
from scvi.data import AnnDataLoader

# For very large datasets
dataloader = AnnDataLoader(
    adata,
    batch_size=128,
    shuffle=True,
    drop_last=False
)

# Custom training loop (advanced)
for batch in dataloader:
    # Process batch
    pass
```

### 使用支持的 AnnData

```python
# For data too large for memory
adata = sc.read_h5ad("huge_dataset.h5ad", backed='r')

# scvi-tools works with backed mode
scvi.model.SCVI.setup_anndata(adata)
model = scvi.model.SCVI(adata)
model.train()
```

## 模型解释

### 特征重要性SHAP

```python
import shap

# Get SHAP values for interpretability
explainer = shap.DeepExplainer(model.module, background_data)
shap_values = explainer.shap_values(test_data)

# Visualize
shap.summary_plot(shap_values, feature_names=adata.var_names)
```

### 基因相关性分析

```python
# Get gene-gene correlation matrix
correlation = model.get_feature_correlation_matrix(
    adata,
    transform_batch="batch1"
)

# Visualize top correlated genes
import seaborn as sns
sns.heatmap(correlation[:50, :50], cmap="coolwarm")
```

## 常见问题排查

### 问题：训练期间NaN损失

* *原因**：
- 学习率太高
- 非标准化输入（必须使用原始计数）
- 数据质量问题

* *解决方案**：
```python
# Reduce learning rate
model.train(lr=0.0001)

# Check data
assert adata.X.min() >= 0  # No negative values
assert np.isnan(adata.X).sum() == 0  # No NaNs

# Use more stable likelihood
model = scvi.model.SCVI(adata, gene_likelihood="nb")
```

### 问题：批次不佳更正

* *解决方案**：
```python
# Increase batch effect modeling
model = scvi.model.SCVI(
    adata,
    encode_covariates=True,  # Encode batch in encoder
    deeply_inject_covariates=False
)

# Or try opposite
model = scvi.model.SCVI(adata, deeply_inject_covariates=True)

# Use more latent dimensions
model = scvi.model.SCVI(adata, n_latent=50)
```

### 问题：模型未训练（ELBO未减少）

* *解决方案**：
```python
# Increase learning rate
model.train(lr=0.005)

# Increase network capacity
model = scvi.model.SCVI(adata, n_hidden=256, n_layers=2)

# Train longer
model.train(max_epochs=500)
```

### 问题：内存不足(OOM)

* *解决方案**：
```python
# Reduce batch size
model.train(batch_size=64)

# Use mixed precision
model.train(precision=16)

# Reduce model size
model = scvi.model.SCVI(adata, n_latent=10, n_hidden=64)

# Use backed AnnData
adata = sc.read_h5ad("data.h5ad", backed='r')
```

## 性能基准测试

```python
import time

# Time training
start = time.time()
model.train(max_epochs=400)
training_time = time.time() - start
print(f"Training time: {training_time:.2f}s")

# Time inference
start = time.time()
latent = model.get_latent_representation()
inference_time = time.time() - start
print(f"Inference time: {inference_time:.2f}s")

# Memory usage
import psutil
import os
process = psutil.Process(os.getpid())
memory_gb = process.memory_info().rss / 1024**3
print(f"Memory usage: {memory_gb:.2f} GB")
```

## 最佳实践总结

1. **始终使用原始计数**：切勿在 scvi-tools
2 之前进行日志标准化。 **特征选择**：使用高度可变的基因来提高效率
3. **批量校正**：注册所有已知的技术协变量
4. **提前停止**：使用验证集防止过度拟合
5. **模型保存**：始终保存经过训练的模型
6. **GPU 使用**：使用 GPU 处理大型数据集（>10k 个单元）
7. **超参数调整**：从默认值开始，根据需要进行调整
8. **验证**：目视检查批次校正（UMAP 按批次着色）
9. **文档**：跟踪预处理步骤
10. **再现性**：设置随机种子（`scvi.settings.seed = 0`）
