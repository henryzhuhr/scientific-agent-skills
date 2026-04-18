# 单细胞 RNA-seq 模型

本文档涵盖了 scvi-tools 中分析单细胞 RNA 测序数据的核心模型。

## scVI (Single-Cell Variational Inference)

* *目的**：scRNA-seq 数据的无监督分析、降维和批量校正。

* *Key特征**：
- 基于变分自动编码器（VAE）的深度生成模型
- 学习捕获生物变异的低维潜在表示
- 自动校正批次效应和技术协变量
- 启用标准化基因表达估计
- 支持差异表达分析

* *何时用途**：
- scRNA-seq 数据集的初步探索和降维
- 整合多个批次或研究
- 生成批次校正的表达矩阵
- 执行概率差异表达分析

* *基本用法**：
```python
import scvi

# Setup data
scvi.model.SCVI.setup_anndata(
    adata,
    layer="counts",
    batch_key="batch"
)

# Train model
model = scvi.model.SCVI(adata, n_latent=30)
model.train()

# Extract results
latent = model.get_latent_representation()
normalized = model.get_normalized_expression()
```

* *关键参数**：
- `n_latent`：潜在空间的维数（默认：10）
- `n_layers`：隐藏层的数量（默认：1）
- `n_hidden`：每个隐藏层的节点数（默认值：128）
- `dropout_rate`：神经网络的丢失率（默认值：0.1）
- `dispersion`：基因特异性或细胞特异性分散（“基因”或“基因批次”）
- `gene_likelihood`：数据分布（“zinb”、“nb”、“poisson”）

* *输出**：
- `get_latent_representation()`：批量校正的低维嵌入
- `get_normalized_expression()`：去噪、标准化表达值
- `differential_expression()`：组间概率DE测试
- `get_feature_correlation_matrix()`：基因-基因相关性估计

## scANVI（使用变分推理的单细胞注释）

* *目的**：使用标记和未标记细胞进行半监督细胞类型注释和整合。

* *主要功能**：
- 使用细胞类型标签扩展 scVI
- 利用部分标记的数据集进行注释传输
- 同时执行批量校正和细胞类型预测
- 启用查询到参考映射

* *何时使用**：
- 使用参考标签注释新数据集
- 从注释良好的数据集到未标记数据集的迁移学习
- 标记和未标记细胞的联合分析
- 构建具有不确定性量化的细胞类型分类器

* *基本用法**：
```python
# Option 1: Train from scratch
scvi.model.SCANVI.setup_anndata(
    adata,
    layer="counts",
    batch_key="batch",
    labels_key="cell_type",
    unlabeled_category="Unknown"
)
model = scvi.model.SCANVI(adata)
model.train()

# Option 2: Initialize from pretrained scVI
scvi_model = scvi.model.SCVI(adata)
scvi_model.train()
scanvi_model = scvi.model.SCANVI.from_scvi_model(
    scvi_model,
    unlabeled_category="Unknown"
)
scanvi_model.train()

# Predict cell types
predictions = scanvi_model.predict()
```

* *关键参数**：
- `labels_key`：`adata.obs` 中包含细胞类型标签的列
- `unlabeled_category`：没有注释的细胞标签
- 所有 scVI 参数也可用

* *输出**：
- `predict()`：所有细胞的类型预测cells
- `predict_proba()`：预测概率
- `get_latent_representation()`：细胞类型感知潜在空间

## AUTOZI

* *目的**：scRNA-seq数据中零膨胀基因的自动识别和建模。

* *关键特点**：
- 区分生物零和技术性脱落
- 了解哪些基因表现出零膨胀
- 提供基因特定的零膨胀概率
- 通过考虑脱落来改进下游分析

* *何时使用**：
- 检测哪些基因是零膨胀受技术丢失的影响
- 改进稀疏数据集的插补和归一化
- 了解数据中零膨胀的程度

* *基本用法**：
```python
scvi.model.AUTOZI.setup_anndata(adata, layer="counts")
model = scvi.model.AUTOZI(adata)
model.train()

# Get zero-inflation probabilities per gene
zi_probs = model.get_alphas_betas()
```

## VeloVI

* *目的**：使用变分法进行RNA速度分析inference.

* *主要特点**：
- 剪接和未剪接 RNA 计数的联合建模
- RNA 速度的概率估计
- 考虑技术噪声和批次效应
- 为速度估计提供不确定性量化

* *何时使用**：
- 推断细胞动力学和分化轨迹
- 分析剪接/未剪接计数数据
- 带批量校正的 RNA 速度分析

* *基本用法**：
```python
import scvelo as scv

# Prepare velocity data
scv.pp.filter_and_normalize(adata)
scv.pp.moments(adata)

# Train VeloVI
scvi.model.VELOVI.setup_anndata(adata, spliced_layer="Ms", unspliced_layer="Mu")
model = scvi.model.VELOVI(adata)
model.train()

# Get velocity estimates
latent_time = model.get_latent_time()
velocities = model.get_velocity()
```

## 对比VI

* *目的**：从背景生物变异中分离出扰动特异性变异。

* *主要特征**：
- 将共享变异（跨条件下常见）与目标特异性变异分开
- 可用于扰动研究（药物治疗、遗传扰动）
- 识别条件特异性基因程序
- 能够发现治疗特异性效果

* *何时使用**：
- 分析扰动实验（药物筛选、CRISPR 等）
- 识别对治疗有特异性反应的基因
- 将治疗效果与背景变化分开
- 比较对照与扰动条件

* *基本用法**：
```python
scvi.model.CONTRASTIVEVI.setup_anndata(
    adata,
    layer="counts",
    batch_key="batch",
    categorical_covariate_keys=["condition"]  # control vs treated
)

model = scvi.model.CONTRASTIVEVI(
    adata,
    n_latent=10,        # Shared variation
    n_latent_target=5   # Target-specific variation
)
model.train()

# Extract representations
shared = model.get_latent_representation(representation="shared")
target_specific = model.get_latent_representation(representation="target")
```

## CellAssign

* *目的**：使用已知标记基因进行基于标记的细胞类型注释。

* *主要特征**：
- 使用细胞标记基因的先验知识types
- 细胞类型的概率分配
- 处理标记基因重叠和模糊性
- 提供不确定性的软分配

* *何时使用**：
- 使用已知标记基因注释细胞
- 利用现有的生物学知识进行分类
- 有标记基因列表但没有参考数据集的情况

* *基本用法**：
```python
# Create marker gene matrix (cell types x genes)
marker_gene_mat = pd.DataFrame({
    "CD4 T cells": [1, 1, 0, 0],  # CD3D, CD4, CD8A, CD19
    "CD8 T cells": [1, 0, 1, 0],
    "B cells": [0, 0, 0, 1]
}, index=["CD3D", "CD4", "CD8A", "CD19"])

scvi.model.CELLASSIGN.setup_anndata(adata, layer="counts")
model = scvi.model.CELLASSIGN(adata, marker_gene_mat)
model.train()

predictions = model.predict()
```

## Solo（双联体检测）

* *目的**：识别scRNA-seq数据中的双联体（包含两个或多个细胞的细胞）。

* *关键功能**：
- 使用 scVI 嵌入进行半监督双峰检测
- 模拟人工双峰进行训练
- 提供双峰概率分数
- 可应用于任何 scVI 模型

* *何时使用**：
- scRNA-seq 数据集的质量控制
- 在下游分析之前去除双峰
- 评估数据中的双峰率

* *基本用法**：
```python
# Train scVI model first
scvi.model.SCVI.setup_anndata(adata, layer="counts")
scvi_model = scvi.model.SCVI(adata)
scvi_model.train()

# Train Solo for doublet detection
solo_model = scvi.external.SOLO.from_scvi_model(scvi_model)
solo_model.train()

# Predict doublets
predictions = solo_model.predict()
doublet_scores = predictions["doublet"]
adata.obs["doublet_score"] = doublet_scores
```

## 摊销LDA（主题建模）

* *目的**：使用潜在狄利克雷分配对基因表达进行主题建模。

* *关键特征**：
- 发现基因表达程序（主题）
- 用于可扩展性的摊销变分推理
- 每个单元格都是主题的混合
- 每个主题都是基因

* *何时使用**：
- 发现基因程序或表达模块
- 了解表达的组成结构
- 替代降维方法
- 表达模式的可解释分解

* *基本用法**：
```python
scvi.model.AMORTIZEDLDA.setup_anndata(adata, layer="counts")
model = scvi.model.AMORTIZEDLDA(adata, n_topics=10)
model.train()

# Get topic compositions per cell
topic_proportions = model.get_latent_representation()

# Get gene loadings per topic
topic_gene_loadings = model.get_topic_distribution()
```

## 模型选择指南

* *选择scVI，当**：
- 从无监督分析开始
- 需要批量校正和集成
- 想要标准化表达和DE分析

* *选择scANVI当**：
- 有一些标记细胞用于训练
- 需要细胞类型注释
- 想要将标签从引用转移到查询

* *选择AUTOZI当**：
- 担心技术退出
- 需要识别零膨胀基因
- 工作数据集非常稀疏

* *当**时选择VeloVI：
- 有拼接/未拼接计数数据
- 对细胞动力学感兴趣
- 需要批量校正的RNA速度

* *当**时选择对比VI：
- 分析扰动实验
- 需要分离治疗效果
- 想要识别特定条件的程序

* *选择CellAssign，当**：
- 有可用的标记基因列表
- 想要基于概率标记的注释
- 没有可用的参考数据集

* *选择Solo当**：
- 需要双峰检测
- 已经使用scVI进行分析
- 想要概率双峰分数
