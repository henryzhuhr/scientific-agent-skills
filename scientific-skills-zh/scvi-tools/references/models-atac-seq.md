# ATAC-seq 和染色质可及性模型

本文档涵盖了用于分析 scvi-tools 中的单细胞 ATAC-seq 和染色质可及性数据的模型。

## PeakVI

* *目的**：使用峰值计数分析和整合单细胞 ATAC-seq 数据。

* *Key功能**：
- 专为 scATAC-seq 峰值数据设计的变分自动编码器
- 学习染色质可及性的低维表示
- 跨样本执行批量校正
- 启用差异可及性测试
- 集成多个ATAC-seq数据集

* *何时使用**：
- 分析 scATAC-seq 峰值计数矩阵
- 整合多个 ATAC-seq 实验
- 染色质可及性数据的批量校正
- ATAC-seq 的降维
- 细胞类型或条件之间的差异可及性分析

* *数据要求**：
- 峰计数矩阵（细胞×峰）
- 峰可访问性的二进制或计数数据
- 批次/样品注释（可选，用于批次校正）

* *基本用法**：
```python
import scvi

# Prepare data (peaks should be in adata.X)
# Optional: filter peaks
sc.pp.filter_genes(adata, min_cells=3)

# Setup data
scvi.model.PEAKVI.setup_anndata(
    adata,
    batch_key="batch"
)

# Train model
model = scvi.model.PEAKVI(adata)
model.train()

# Get latent representation (batch-corrected)
latent = model.get_latent_representation()
adata.obsm["X_PeakVI"] = latent

# Differential accessibility
da_results = model.differential_accessibility(
    groupby="cell_type",
    group1="TypeA",
    group2="TypeB"
)
```

* *密钥参数**：
- `n_latent`：潜在空间的维数（默认：10）
- `n_hidden`：每个隐藏层的节点数（默认：128）
- `n_layers`：隐藏层的数量（默认：1）
- `region_factors`：是否学习区域特定因素（默认：True）
- `latent_distribution`：潜在空间的分布（“正常”或“ln”）

* *输出**：
- `get_latent_representation()`：细胞的低维嵌入
- `get_accessibility_estimates()`：归一化可及性值
- `differential_accessibility()`：差分峰的统计测试
- `get_region_factors()`：峰特定缩放因子

* *最佳实践**：
1. 滤除低质量峰（存在于极少数细胞中）
2. 如果集成多个样品，请包括批次信息
3. 使用潜在表示进行聚类和 UMAP 可视化
4. 对于技术变化较大的数据集，请考虑使用 `region_factors=True`
5. 将潜在嵌入存储在 `adata.obsm` 中，以便使用 scanpy

## PoissonVI

* *目的**：scATAC-seq 片段计数的定量分析（比峰值计数更详细）。

* *主要功能**：
- 直接对片段计数进行建模（不仅仅是峰值）存在/不存在）
- 计数数据的泊松分布
- 捕获可访问性的定量差异
- 启用染色质状态的细粒度分析

* *何时使用**：
- 分析片段级ATAC-seq数据
- 需要定量可访问性测量
- 比二进制峰调用更高分辨率的分析
- 研究染色质可及性的逐渐变化

* *数据要求**：
- 片段计数矩阵（细胞×基因组区域）
- 计数数据（非二进制）

* *基本用法**：
```python
scvi.model.POISSONVI.setup_anndata(
    adata,
    batch_key="batch"
)

model = scvi.model.POISSONVI(adata)
model.train()

# Get results
latent = model.get_latent_representation()
accessibility = model.get_accessibility_estimates()
```

* *与 PeakVI 的主要区别**：
- **PeakVI**：最适合标准峰计数矩阵，速度更快
- **PoissonVI**：最适合定量片段计数，更详细

* *何时选择 PoissonVI PeakVI**:
- 使用片段计数而不是称为峰
- 需要捕获定量差异
- 拥有高质量、高覆盖率的数据
- 对微妙的可访问性变化感兴趣

## scBasset

* *目的**：具有可解释性的 scATAC-seq 分析的深度学习方法和基序分析。

* *主要特点**：
- 用于基于序列的分析的卷积神经网络 (CNN)架构
- 对原始 DNA 序列进行建模，而不仅仅是峰值计数
- 实现基序发现和转录因子 (TF)结合预测
- 提供可解释的特征重要性
- 执行批量校正

* *何时使用**：
- 想要纳入DNA序列信息
- 对TF基序分析感兴趣
- 需要可解释的模型（哪些序列驱动可访问性）
- 分析调控元件和TF结合位点
- 仅根据序列预测可访问性

* *数据要求**：
- 峰序列（从基因组中提取）
- 峰可及性矩阵
- 基因组参考（用于序列提取）

* *基本用法**：
```python
# scBasset requires sequence information
# First, extract sequences for peaks
from scbasset import utils
sequences = utils.fetch_sequences(adata, genome="hg38")

# Setup and train
scvi.model.SCBASSET.setup_anndata(
    adata,
    batch_key="batch"
)

model = scvi.model.SCBASSET(adata, sequences=sequences)
model.train()

# Get latent representation
latent = model.get_latent_representation()

# Interpret model: which sequences/motifs are important
importance_scores = model.get_feature_importance()
```

* *关键参数**：
- `n_latent`：潜在空间维度
- `conv_layers`：卷积层数
- `n_filters`：每个卷积层的滤波器数量
- `filter_size`：卷积滤波器的大小

* *高级功能**：
- **计算机模拟诱变**：预测序列变化如何影响可访问性
- **基序富集**：识别可访问区域中富集的 TF 基序
- **批量校正**：与其他 scvi-tools 模型类似
- **迁移学习**：在新数据集上微调

* *可解释性工具**：
```python
# Get importance scores for sequences
importance = model.get_sequence_importance(region_indices=[0, 1, 2])

# Predict accessibility for new sequences
predictions = model.predict_accessibility(new_sequences)
```

## ATAC-seq的模型选择

### PeakVI
* *何时选择**：
- 标准 scATAC-seq 分析工作流程
- 具有峰值计数矩阵（最常见的格式）
- 需要快速、高效的批量校正
- 想要简单的差分可访问性
- 优先考虑计算效率

* *优点**：
- 快速训练和推理
- 经过验证的scATAC-seq记录
- 与scanpy轻松集成工作流程
- 稳健批量校正

### PoissonVI
* *选择何时**：
- 拥有片段级计数数据
- 需要定量可及性测量
- 对细微差异感兴趣
- 拥有高覆盖率、高质量数据

* *优点**：
- 更详细的定量信息
- 更好的梯度变化
- 适当的计数统计模型

### scBasset
* *何时选择**：
- 想要合并DNA序列
- 需要生物学解释（基序、TF）
- 对监管感兴趣机制
- 拥有用于 CNN 训练的计算资源
- 想要对新序列进行预测能力

* *优点**：
- 基于序列，可生物学解释
- 内置基序和TF 分析
- 预测建模功能
- 计算机模拟扰动实验

## 工作流程示例：完整 ATAC-seq 分析

```python
import scvi
import scanpy as sc

# 1. Load and preprocess ATAC-seq data
adata = sc.read_h5ad("atac_data.h5ad")

# 2. Filter low-quality peaks
sc.pp.filter_genes(adata, min_cells=10)

# 3. Setup and train PeakVI
scvi.model.PEAKVI.setup_anndata(
    adata,
    batch_key="sample"
)

model = scvi.model.PEAKVI(adata, n_latent=20)
model.train(max_epochs=400)

# 4. Extract latent representation
latent = model.get_latent_representation()
adata.obsm["X_PeakVI"] = latent

# 5. Downstream analysis
sc.pp.neighbors(adata, use_rep="X_PeakVI")
sc.tl.umap(adata)
sc.tl.leiden(adata, key_added="clusters")

# 6. Differential accessibility
da_results = model.differential_accessibility(
    groupby="clusters",
    group1="0",
    group2="1"
)

# 7. Save model
model.save("peakvi_model")
```

## 与基因表达整合 (RNA+ATAC)

对于配对多模态数据（来自相同细胞的 RNA+ATAC），请使用 **MultiVI**相反：

```python
# For 10x Multiome or similar paired data
scvi.model.MULTIVI.setup_anndata(
    adata,
    batch_key="sample",
    modality_key="modality"  # "RNA" or "ATAC"
)

model = scvi.model.MULTIVI(adata)
model.train()

# Get joint latent space
latent = model.get_latent_representation()
```

有关多模态集成的更多详细信息，请参阅 `models-multimodal.md`。

## ATAC-seq 分析的最佳实践

1. **质量控制**：
  - 过滤峰值计数非常低或非常高的细胞
  - 删除极少数细胞中存在的峰值
  - 如果需要，过滤线粒体和性染色体峰值

2. **批量校正**：
  - 如果集成多个样本，则始终包含 `batch_key`
  - 考虑技术协变量（测序深度、TSS 富集）

3. **特征选择**：
  - 与RNA-seq不同，经常使用所有峰
  - 考虑过滤非常罕见的峰以提高效率

4. **潜在维度**：
  - 根据数据集复杂性从 `n_latent=10-30` 开始
  - 更多异构数据集的更大值

5. **下游分析**：
  - 使用潜在表示进行聚类和可视化
  - 将峰链接到基因以进行调控分析
  - 对簇特定峰

6 进行基序富集。 **计算注意事项**：
 - ATAC-seq 矩阵通常非常大（许多峰值）
  - 考虑对初始探索进行下采样峰值
  - 对大型数据集使用 GPU 加速
