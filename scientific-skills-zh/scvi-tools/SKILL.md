---
name: scvi-tools
description: 单细胞组学的深度生成模型。当您需要概率批量校正 (scVI)、迁移学习、不确定性差异表达或多模态积分（TOTALVI、MultiVI）时使用。最适合高级建模、批量效果、多模式数据。对于标准分析管道，请使用 scanpy。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# scvi-tools

## 概述

scvi-tools 是一个用于单细胞基因组学概率模型的综合 Python 框架。它基于 PyTorch 和 PyTorch Lightning 构建，提供使用变分推理的深度生成模型，用于分析不同的单细胞数据模态。

## 何时使用此技能

在以下情况下使用此技能：
- 分析单细胞 RNA-seq 数据（降维、批量校正、集成）
- 使用单细胞 ATAC-seq 或染色质可及性数据
- 整合多模态数据（CITE-seq、多组、配对/未配对数据集）
- 分析空间转录组数据（反卷积、空间映射）
- 对单细胞数据执行差异表达分析
- 进行细胞类型注释或迁移学习任务
- 使用专门的单细胞模态（甲基化、细胞计数、RNA 速度）
- 构建用于单细胞分析的自定义概率模型

## 核心功能

scvi-tools 提供按数据模态组织的模型：

### 1. 单细胞 RNA 序列分析
用于表达分析、批量校正和集成的核心模型。参见`references/models-scrna-seq.md`：
- **scVI**：无监督降维和批量校正
- **scANVI**：半监督细胞类型注释和集成
- **AUTOZI**：零膨胀检测和建模
- **VeloVI**：RNA速度分析
- **contrastiveVI**：扰动效应隔离

### 2.染色质可及性（ATAC-seq）
用于分析单细胞染色质数据的模型。请参阅 `references/models-atac-seq.md` 了解：
- **PeakVI**：基于峰的 ATAC-seq 分析和集成
- **PoissonVI**：定量片段计数建模
- **scBasset**：采用基序分析的深度学习方法

### 3.多模态&多组学集成
多种数据类型联合分析。请参阅 `references/models-multimodal.md`：
- **totalVI**：CITE-seq 蛋白质和 RNA 联合建模
- **MultiVI**：配对和未配对的多组学整合
- **MrVI**：多分辨率交叉样本分析

### 4. 空间转录组学
空间解析转录组学分析。参见`references/models-spatial.md`：
- **DestVI**：多分辨率空间解卷积
- **立体镜**：细胞类型解卷积
- **七巧板**：空间映射和集成
- **scVIVA**：细胞-环境关系分析

### 5. 专业化模态
额外的专业分析工具。请参阅 `references/models-specialized.md` 了解：
- **MmethylVI/MmethylANVI**：单细胞甲基化分析
- **CytoVI**：流式/质谱流式细胞仪批量校正
- **Solo**：双联体检测
- **CellAssign**：基于标记的细胞类型注释

## 典型工作流程

所有scvi-tools模型都遵循一致的API模式：

```python
# 1. Load and preprocess data (AnnData format)
import scvi
import scanpy as sc

adata = scvi.data.heart_cell_atlas_subsampled()
sc.pp.filter_genes(adata, min_counts=3)
sc.pp.highly_variable_genes(adata, n_top_genes=1200)

# 2. Register data with model (specify layers, covariates)
scvi.model.SCVI.setup_anndata(
    adata,
    layer="counts",  # Use raw counts, not log-normalized
    batch_key="batch",
    categorical_covariate_keys=["donor"],
    continuous_covariate_keys=["percent_mito"]
)

# 3. Create and train model
model = scvi.model.SCVI(adata)
model.train()

# 4. Extract latent representations and normalized values
latent = model.get_latent_representation()
normalized = model.get_normalized_expression(library_size=1e4)

# 5. Store in AnnData for downstream analysis
adata.obsm["X_scVI"] = latent
adata.layers["scvi_normalized"] = normalized

# 6. Downstream analysis with scanpy
sc.pp.neighbors(adata, use_rep="X_scVI")
sc.tl.umap(adata)
sc.tl.leiden(adata)
```

* *关键设计原则：**
- **需要原始计数**：模型期望非标准化计数数据以获得最佳性能
- **统一API**：所有模型之间的一致接口（设置→训练→ 
- **Ann以数据为中心**：与scanpy生态系统无缝集成
- **GPU加速**：自动利用可用GPU
- **批量校正**：通过协变量注册处理技术变异

## 常见分析任务

### 差异表达式
使用学习到的生成模型进行概率DE分析：

```python
de_results = model.differential_expression(
    groupby="cell_type",
    group1="TypeA",
    group2="TypeB",
    mode="change",  # Use composite hypothesis testing
    delta=0.25      # Minimum effect size threshold
)
```

有关详细方法和解释，请参见`references/differential-expression.md`。

### 模型持久性
保存并加载训练好的模型模型：

```python
# Save model
model.save("./model_directory", overwrite=True)

# Load model
model = scvi.model.SCVI.load("./model_directory", adata=adata)
```

### 批量校正和集成
跨批次或研究集成数据集：

```python
# Register batch information
scvi.model.SCVI.setup_anndata(adata, batch_key="study")

# Model automatically learns batch-corrected representations
model = scvi.model.SCVI(adata)
model.train()
latent = model.get_latent_representation()  # Batch-corrected
```

## 理论基础

scvi-tools 构建于：
- **变分推理**：可扩展贝叶斯推理的近似后验分布
- **深度生成模型**：学习复杂数据分布的 VAE 架构
- **摊销推理**：用于跨单元高效学习的共享神经网络
- **概率建模**：有原则的不确定性量化和统计测试

有关数学框架的详细背景，请参阅 `references/theoretical-foundations.md`。

## 其他资源

- **工作流程**：`references/workflows.md` 包含常见工作流程、最佳实践、超参数调整和 GPU 优化
- **模型参考**：每个模型类别的详细文档`references/`目录
- **官方文档**：https://docs.scvi-tools.org/en/stable/
- **教程**：https://docs.scvi-tools.org/en/stable/tutorials/index.html
- **API参考**： https://docs.scvi-tools.org/en/stable/api/index.html

## 安装

```bash
uv pip install scvi-tools
# For GPU support
uv pip install scvi-tools[cuda]
```

## 最佳实践

1. **使用原始计数**：始终向模型 
2 提供非标准化计数数据。 **过滤基因**：在分析前删除低计数基因（例如，`min_counts=3`）
3. **注册协变量**：在`setup_anndata`
4中包括已知的技术因素（批次、供体等）。 **特征选择**：使用高度可变的基因来提高性能
5. **模型保存**：始终保存经过训练的模型，以避免重新训练
6. **GPU 使用**：为大型数据集启用 GPU 加速 (`accelerator="gpu"`)
7. **Scanpy 集成**：将输出存储在 AnnData 对象中以供下游分析
