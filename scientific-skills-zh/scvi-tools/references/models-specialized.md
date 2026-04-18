# 专用模态模型

本文档涵盖了 scvi-tools 中专用单细胞数据模态的模型。

## MmethylVI / MmethylANVI（甲基化分析）

* *目的**：分析 DNA 甲基化的单细胞亚硫酸氢盐测序 (scBS-seq)数据。

* *Key功能**：
- 以单细胞分辨率模拟甲基化模式
- 处理甲基化数据的稀疏性
- 甲基化实验的批量校正
- 用于细胞类型注释的标签转移（MmethylANVI）

* *何时使用**：
- 分析 scBS-seq 或类似的甲基化数据
- 研究跨细胞类型的DNA甲基化模式
- 跨批次整合甲基化数据
- 基于甲基化概况的细胞类型注释

* *数据要求**：
- 甲基化计数矩阵（甲基化与每个CpG位点的总读数）
- 格式：细胞×具有甲基化比率或计数的 CpG 位点

### MmethylVI（无监督）

* *基本用法**：
```python
import scvi

# Setup methylation data
scvi.model.METHYLVI.setup_anndata(
    adata,
    layer="methylation_counts",  # Methylation data
    batch_key="batch"
)

model = scvi.model.METHYLVI(adata)
model.train()

# Get latent representation
latent = model.get_latent_representation()

# Get normalized methylation values
normalized_meth = model.get_normalized_methylation()
```

### MmethylANVI（半监督细胞类型）

* *基本用法**：
```python
# Setup with cell type labels
scvi.model.METHYLANVI.setup_anndata(
    adata,
    layer="methylation_counts",
    batch_key="batch",
    labels_key="cell_type",
    unlabeled_category="Unknown"
)

model = scvi.model.METHYLANVI(adata)
model.train()

# Predict cell types
predictions = model.predict()
```

* *关键参数**：
- `n_latent`：潜在维度
- `region_factors`：模型区域特异性效应

* *用例**：
- 表观遗传异质性分析
- 通过甲基化鉴定细胞类型
- 与基因表达数据整合（单独分析）
- 差异甲基化分析

## CytoVI（流式和质谱流式细胞仪）

* *目的**：流式细胞仪和质谱仪的批量校正和整合（CyTOF） data.

* *主要功能**：
- 处理基于抗体的蛋白质测量
- 校正细胞计数数据中的批次效应
- 实现跨实验集成
- 专为高维蛋白质面板而设计

* *何时使用**：
- 分析流式细胞术或 CyTOF 数据
- 跨批次整合细胞计数实验
- 蛋白质面板的批次校正
- 交叉研究细胞计数整合

* *数据要求**：
- 蛋白质表达矩阵（细胞×蛋白质）
- 流式细胞术或 CyTOF 测量
- 批次/实验注释

* *基本用法**：
```python
scvi.model.CYTOVI.setup_anndata(
    adata,
    protein_expression_obsm_key="protein_expression",
    batch_key="batch"
)

model = scvi.model.CYTOVI(adata)
model.train()

# Get batch-corrected representation
latent = model.get_latent_representation()

# Get normalized protein values
normalized = model.get_normalized_expression()
```

* *关键参数**：
- `n_latent`：潜在空间维度
- `n_layers`：网络深度

* *典型工作流程**：
```python
import scanpy as sc

# 1. Load cytometry data
adata = sc.read_h5ad("cytof_data.h5ad")

# 2. Train CytoVI
scvi.model.CYTOVI.setup_anndata(
    adata,
    protein_expression_obsm_key="protein",
    batch_key="experiment"
)
model = scvi.model.CYTOVI(adata)
model.train()

# 3. Get batch-corrected values
latent = model.get_latent_representation()
adata.obsm["X_CytoVI"] = latent

# 4. Downstream analysis
sc.pp.neighbors(adata, use_rep="X_CytoVI")
sc.tl.umap(adata)
sc.tl.leiden(adata)

# 5. Visualize batch correction
sc.pl.umap(adata, color=["batch", "leiden"])
```

## SysVI（系统级集成）

* *目的**：强调保留生物变异的批量效应校正。

* *关键特点**：
- 专门的批量集成方法
- 保留生物信号，同时消除技术影响
- 专为大规模集成研究而设计

* *何时使用**：
- 大规模多批次集成
- 需要保留细微的生物变异
- 跨系统的系统级分析许多研究

* *基本用法**：
```python
scvi.model.SYSVI.setup_anndata(
    adata,
    layer="counts",
    batch_key="batch"
)

model = scvi.model.SYSVI(adata)
model.train()

latent = model.get_latent_representation()
```

## 解密（轨迹推断）

* *目的**：单细胞数据的轨迹推断和伪时间分析。

* *关键特征**：
- 学习细胞轨迹和分化路径
- 伪时间估计
- 解释轨迹结构的不确定性
- 与scVI 嵌入兼容

* *何时使用**：
- 研究细胞分化
- 时间过程或发育数据集
- 理解细胞状态转换
- 识别发育中的分支点

* *基本用法**：
```python
# Typically used after scVI for embeddings
scvi_model = scvi.model.SCVI(adata)
scvi_model.train()

# Decipher for trajectory
scvi.model.DECIPHER.setup_anndata(adata)
decipher_model = scvi.model.DECIPHER(adata, scvi_model)
decipher_model.train()

# Get pseudotime
pseudotime = decipher_model.get_pseudotime()
adata.obs["pseudotime"] = pseudotime
```

* *可视化**：
```python
import scanpy as sc

# Plot pseudotime on UMAP
sc.pl.umap(adata, color="pseudotime", cmap="viridis")

# Gene expression along pseudotime
sc.pl.scatter(adata, x="pseudotime", y="gene_of_interest")
```

## peRegLM（峰值调节线性模型）

* *目的**：将染色质可及性与基因表达联系起来进行调控分析。

* *主要特征**：
- 将ATAC-seq峰与基因表达联系起来
- 识别调控关系
- 使用配对的多组数据

* *何时使用**：
- 多组数据（来自相同细胞的 RNA + ATAC）
- 了解基因调控
- 将峰连接到目标基因
- 调控网络构建

* *基本用法**：
```python
# Requires paired RNA + ATAC data
scvi.model.PEREGLM.setup_anndata(
    multiome_adata,
    rna_layer="counts",
    atac_layer="atac_counts"
)

model = scvi.model.PEREGLM(multiome_adata)
model.train()

# Get peak-gene links
peak_gene_links = model.get_regulatory_links()
```

## 模型特定最佳实践

### MmethylVI/MmethylANVI
1. **稀疏性**：甲基化数据本质上是稀疏的；型号占此
2. **CpG 选择**：过滤覆盖率极低的 CpG
3. **生物学解释**：考虑基因组背景（启动子、增强子）
4. **整合**：对于多组学，单独分析然后整合结果

### CytoVI
1. **蛋白质QC**：去除低质量或无信息的蛋白质
2. **补偿**：在分析
3之前确保适当的光谱补偿。 **批量设计**：包括生物和技术复制
4. **对照**：使用对照样品来验证批次校正

### SysVI
1. **样本大小**：专为大规模集成而设计
2. **批次定义**：仔细定义批次结构
3. **生物验证**：验证保留的生物信号

### Decipher
1. **起点**：如果已知
2，则定义轨迹起始单元。 **分支**：指定预期的分支数量
3. **验证**：使用已知标记来验证pseudotime
4. **集成**：与scVI嵌入配合良好

## 与其他模型集成

许多专用模型可以很好地组合使用：

* *甲基化+表达**：
```python
# Analyze separately, then integrate
methylvi_model = scvi.model.METHYLVI(meth_adata)
scvi_model = scvi.model.SCVI(rna_adata)

# Integrate results at analysis level
# E.g., correlate methylation and expression patterns
```

* *细胞计数+ CITE-seq**：
```python
# CytoVI for flow/CyTOF
cyto_model = scvi.model.CYTOVI(cyto_adata)

# totalVI for CITE-seq
cite_model = scvi.model.TOTALVI(cite_adata)

# Compare protein measurements across platforms
```

* *ATAC + RNA（多组）**：
```python
# MultiVI for joint analysis
multivi_model = scvi.model.MULTIVI(multiome_adata)

# peRegLM for regulatory links
pereglm_model = scvi.model.PEREGLM(multiome_adata)
```

## 选择专业模型

### 决策树

1. **什么数据模态？**
  - 甲基化 → MmethylVI/MmethylANVI
  - Flow/CyTOF → CytoVI
  - 轨迹 → Decipher
  - 多批次集成 → SysVI
  - 监管链接 → peRegLM

2. **你们有标签吗？**
  - 有 → MmethylANVI（甲基化）
  - 无 → MmethylVI（甲基化）

3. **您的主要目标是什么？**
  - 批量校正 → CytoVI、SysVI
  - 轨迹/伪时间 → Decipher
  - 峰基因链接 → peRegLM
  - 甲基化模式 → MmethylVI/ANVI

## 示例：完全甲基化分析

```python
import scvi
import scanpy as sc

# 1. Load methylation data
meth_adata = sc.read_h5ad("methylation_data.h5ad")

# 2. QC: filter low-coverage CpG sites
sc.pp.filter_genes(meth_adata, min_cells=10)

# 3. Setup MethylVI
scvi.model.METHYLVI.setup_anndata(
    meth_adata,
    layer="methylation",
    batch_key="batch"
)

# 4. Train model
model = scvi.model.METHYLVI(meth_adata, n_latent=15)
model.train(max_epochs=400)

# 5. Get latent representation
latent = model.get_latent_representation()
meth_adata.obsm["X_MethylVI"] = latent

# 6. Clustering
sc.pp.neighbors(meth_adata, use_rep="X_MethylVI")
sc.tl.umap(meth_adata)
sc.tl.leiden(meth_adata)

# 7. Differential methylation
dm_results = model.differential_methylation(
    groupby="leiden",
    group1="0",
    group2="1"
)

# 8. Save
model.save("methylvi_model")
meth_adata.write("methylation_analyzed.h5ad")
```

## 外部工具集成

一些专用模型可作为外部包：

* *SOLO**（双峰检测）：
```python
from scvi.external import SOLO

solo = SOLO.from_scvi_model(scvi_model)
solo.train()
doublets = solo.predict()
```

* *scArches**（参考映射）：
```python
from scvi.external import SCARCHES

# For transfer learning and query-to-reference mapping
```

这些外部工具针对特定用例扩展了 scvi-tools 功能。

## 汇总表

|型号|数据类型 |主要用途 |监督？ |
|-------|------------|-------------|------------|
|甲基VI |甲基化 |无监督分析 |否|
|甲基ANVI |甲基化 |细胞类型注释|半|
|细胞VI |细胞计数|批量修正 |否|
|系统VI |单链RNA测序|大规模整合 |否|
|破译|单链RNA测序|轨迹推断 |否|
| peRegLM |多组学|峰基因链接|否|
|独奏|单链RNA测序|双峰检测 |半|
