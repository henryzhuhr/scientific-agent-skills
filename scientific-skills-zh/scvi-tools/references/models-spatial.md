# 空间转录组学模型

本文档涵盖了用于分析scvi-tools中空间解析转录组学数据的模型。

## DestVI（使用变分推理对空间转录组学进行解卷积）

* *目的**：使用单细胞参考数据对空间转录组学进行多分辨率解卷积。

* *关键特点**：
- 估计每个空间位置的细胞类型比例
- 使用单细胞RNA-seq参考进行解卷积
- 多分辨率方法（全局和局部模式）
- 考虑空间相关性
- 提供不确定性量化

* *何时使用**：
- 对 Visium 或类似的空间转录组进行反卷积
- 拥有带有细胞类型标签的 scRNA-seq 参考数据
- 想要将细胞类型映射到空间位置
- 对细胞类型的空间组织感兴趣
- 需要细胞类型丰度的概率估计

* *数据要求**：
- **空间数据**：Visium 或类似的基于点的测量（目标数据）
- **单细胞参考**：带有细胞类型注释的 scRNA-seq
- 两个数据集应共享基因

* *基本用法**：
```python
import scvi

# Step 1: Train scVI on single-cell reference
scvi.model.SCVI.setup_anndata(sc_adata, layer="counts")
sc_model = scvi.model.SCVI(sc_adata)
sc_model.train()

# Step 2: Setup spatial data
scvi.model.DESTVI.setup_anndata(
    spatial_adata,
    layer="counts"
)

# Step 3: Train DestVI using reference
model = scvi.model.DESTVI.from_rna_model(
    spatial_adata,
    sc_model,
    cell_type_key="cell_type"  # Cell type labels in reference
)
model.train(max_epochs=2500)

# Step 4: Get cell type proportions
proportions = model.get_proportions()
spatial_adata.obsm["proportions"] = proportions

# Step 5: Get cell type-specific expression
# Expression of genes specific to each cell type at each spot
ct_expression = model.get_scale_for_ct("T cells")
```

* *密钥参数**：
- `amortization`：摊销策略（“两者”、“潜在”、“比例”）
- `n_latent`：潜在维度（继承自scVI模型）

* *输出**：
- `get_proportions()`：细胞类型每个点的比例
- `get_scale_for_ct(cell_type)`：细胞类型特异性表达模式
- `get_gamma()`：比例特异性基因表达缩放

* *可视化**：
```python
import scanpy as sc
import matplotlib.pyplot as plt

# Visualize specific cell type proportions spatially
sc.pl.spatial(
    spatial_adata,
    color="T cells",  # If proportions added to .obs
    spot_size=150
)

# Or use obsm directly
for ct in cell_types:
    plt.figure()
    sc.pl.spatial(
        spatial_adata,
        color=spatial_adata.obsm["proportions"][ct],
        title=f"{ct} proportions"
    )
```

## Sterescope

* *目的**：使用概率建模进行空间转录组学的细胞类型反卷积。

* *主要特征**：
- 基于参考的反卷积
- 细胞类型比例的概率框架
- 与各种空间技术配合使用
- 处理基因选择和归一化

* *何时使用**：
- 与DestVI类似，但方法更简单
- 通过参考对空间数据进行解卷积
- 基本解卷积的更快替代方案

* *基本用法**：
```python
scvi.model.STEREOSCOPE.setup_anndata(
    sc_adata,
    labels_key="cell_type",
    layer="counts"
)

# Train on reference
ref_model = scvi.model.STEREOSCOPE(sc_adata)
ref_model.train()

# Setup spatial data
scvi.model.STEREOSCOPE.setup_anndata(spatial_adata, layer="counts")

# Transfer to spatial
spatial_model = scvi.model.STEREOSCOPE.from_reference_model(
    spatial_adata,
    ref_model
)
spatial_model.train()

# Get proportions
proportions = spatial_model.get_proportions()
```

## Tangram

* *目的**：空间映射和将单细胞数据整合到空间位置。

* *主要功能**：
- 将单细胞映射到空间坐标
- 了解单细胞和空间数据之间的最佳传输
- 空间位置的基因插补
- 细胞类型映射

* *何时使用**：
- 映射来自scRNA-seq 到空间位置
- 在空间数据中导入未测量的基因
- 以单细胞分辨率理解空间组织
- 整合scRNA-seq 和空间转录组学

* *数据要求**：
- 带注释的单细胞RNA-seq 数据
- 空间转录组学data
- 模式之间共享基因

* *基本用法**：
```python
import tangram as tg

# Map cells to spatial locations
ad_map = tg.map_cells_to_space(
    adata_sc=sc_adata,
    adata_sp=spatial_adata,
    mode="cells",  # or "clusters" for cell type mapping
    density_prior="rna_count_based"
)

# Get mapping matrix (cells × spots)
mapping = ad_map.X

# Project cell annotations to space
tg.project_cell_annotations(
    ad_map,
    spatial_adata,
    annotation="cell_type"
)

# Impute genes in spatial data
genes_to_impute = ["CD3D", "CD8A", "CD4"]
tg.project_genes(ad_map, spatial_adata, genes=genes_to_impute)
```

* *可视化**：
```python
# Visualize cell type mapping
sc.pl.spatial(
    spatial_adata,
    color="cell_type_projected",
    spot_size=100
)
```

## gimVI（高斯恒等式多重vi插补）

* *目的**：空间和单细胞数据之间的跨模态插补。

* *关键特征**：
- 空间和单细胞数据的联合模型
- 插补空间数据中缺失的基因
- 启用跨数据集查询
- 学习共享表示

* *何时使用**：
- 导入空间数据中未测量的基因
- 空间和单细胞数据集的联合分析
- 模态之间的映射

* *基本用法**：
```python
# Combine datasets
combined_adata = sc.concat([sc_adata, spatial_adata])

scvi.model.GIMVI.setup_anndata(
    combined_adata,
    layer="counts"
)

model = scvi.model.GIMVI(combined_adata)
model.train()

# Impute genes in spatial data
imputed = model.get_imputed_values(spatial_indices)
```

## scVIVA（空间变分自动编码器的变化）

* *目的**：分析空间数据中的细胞-环境关系。

* *主要特征**：
- 对细胞邻域和环境进行建模
- 识别与环境相关的基因表达
- 解释空间相关性结构
- 细胞间相互作用分析

* *何时使用**：
- 了解空间环境如何影响细胞
- 识别利基特异性基因程序
- 细胞与细胞相互作用研究
- 微环境分析

* *数据要求**：
- 具有坐标的空间转录组学
- 细胞类型注释（可选）

* *基本用法**：
```python
scvi.model.SCVIVA.setup_anndata(
    spatial_adata,
    layer="counts",
    spatial_key="spatial"  # Coordinates in .obsm
)

model = scvi.model.SCVIVA(spatial_adata)
model.train()

# Get environment representations
env_latent = model.get_environment_representation()

# Identify environment-associated genes
env_genes = model.get_environment_specific_genes()
```

## ResolVI

* *目的**：通过分辨率感知建模解决空间转录组噪声。

* *主要功能**：
- 考虑空间分辨率影响
- 降噪空间数据
- 多尺度分析
- 提高下游分析质量

* *何时使用**：
- 有噪声的空间数据
- 多空间分辨率
- 分析前需要去噪
- 改善数据质量

* *基本用法**：
```python
scvi.model.RESOLVI.setup_anndata(
    spatial_adata,
    layer="counts",
    spatial_key="spatial"
)

model = scvi.model.RESOLVI(spatial_adata)
model.train()

# Get denoised expression
denoised = model.get_denoised_expression()
```

## 空间转录组学的模型选择

### DestVI
* *选择何时**：
- 需要详细解卷积时参考
- 有高质量scRNA-seq 参考
- 想要多分辨率分析
- 需要不确定性定量

* *最适合**：Visium、基于点的技术

### 立体镜
* *何时选择**：
- 需要更简单、更快的解卷积
- 基本细胞类型比例估计
- 有限的计算资源

* *最适合**：快速反卷积任务

### 七巧板
* *何时选择**：
- 想要单细胞分辨率映射
- 需要估算许多基因
- 对细胞感兴趣定位
- 首选最佳运输方法

* *最适合**：详细的空间映射

### gimVI
* *何时选择**：
- 需要双向插补
- 空间和单细胞的联合建模
- 跨数据集查询

* *最适合**：积分和插补

### scVIVA
* *选择何时**：
- 对细胞环境感兴趣
- 细胞与细胞相互作用分析
- 邻里效应

* *最适合**：微环境研究

### ResolVI
* *选择何时**：
- 数据质量是一个问题
- 需要去噪
- 多尺度分析

* *最适合**：噪声数据预处理

## 完整工作流程：空间反卷积DestVI

```python
import scvi
import scanpy as sc
import squidpy as sq

# ===== Part 1: Prepare single-cell reference =====
# Load and process scRNA-seq reference
sc_adata = sc.read_h5ad("reference_scrna.h5ad")

# QC and filtering
sc.pp.filter_genes(sc_adata, min_cells=10)
sc.pp.highly_variable_genes(sc_adata, n_top_genes=4000)

# Train scVI on reference
scvi.model.SCVI.setup_anndata(
    sc_adata,
    layer="counts",
    batch_key="batch"
)

sc_model = scvi.model.SCVI(sc_adata)
sc_model.train(max_epochs=400)

# ===== Part 2: Load spatial data =====
spatial_adata = sc.read_visium("path/to/visium")
spatial_adata.var_names_make_unique()

# QC spatial data
sc.pp.filter_genes(spatial_adata, min_cells=10)

# ===== Part 3: Run DestVI =====
scvi.model.DESTVI.setup_anndata(
    spatial_adata,
    layer="counts"
)

destvi_model = scvi.model.DESTVI.from_rna_model(
    spatial_adata,
    sc_model,
    cell_type_key="cell_type"
)

destvi_model.train(max_epochs=2500)

# ===== Part 4: Extract results =====
# Get proportions
proportions = destvi_model.get_proportions()
spatial_adata.obsm["proportions"] = proportions

# Add proportions to .obs for easy plotting
for i, ct in enumerate(sc_model.adata.obs["cell_type"].cat.categories):
    spatial_adata.obs[f"prop_{ct}"] = proportions[:, i]

# ===== Part 5: Visualization =====
# Plot specific cell types
cell_types = ["T cells", "B cells", "Macrophages"]

for ct in cell_types:
    sc.pl.spatial(
        spatial_adata,
        color=f"prop_{ct}",
        title=f"{ct} proportions",
        spot_size=150,
        cmap="viridis"
    )

# ===== Part 6: Spatial analysis =====
# Compute spatial neighbors
sq.gr.spatial_neighbors(spatial_adata)

# Spatial autocorrelation of cell types
for ct in cell_types:
    sq.gr.spatial_autocorr(
        spatial_adata,
        attr="obs",
        mode="moran",
        genes=[f"prop_{ct}"]
    )

# ===== Part 7: Save results =====
destvi_model.save("destvi_model")
spatial_adata.write("spatial_deconvolved.h5ad")
```

## 空间分析最佳实践

1. **参考质量**：使用高质量、注释良好的 scRNA-seq 参考 
2. **基因重叠**：确保参考和空间
3之间有足够的共享基因。 **空间坐标**：在`.obsm["spatial"]`
4中正确注册空间坐标。 **验证**：使用已知的标记基因来验证反卷积
5. **可视化**：始终在空间上可视化结果以检查生物学合理性
6. **细胞类型粒度**：考虑适当的细胞类型分辨率
7. **计算资源**：空间模型可能会占用大量内存
8. **质量控制**：分析前过滤低质量斑点
