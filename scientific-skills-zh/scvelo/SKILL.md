---
name: scvelo
description: 使用 scVelo 进行 RNA 速度分析。根据未剪接/剪接 mRNA 动力学估计细胞状态转变，推断轨迹方向，计算潜伏时间，并识别单细胞 RNA-seq 数据中的驱动基因。补充了用于轨迹推断的 Scanpy/scVI 工具。
license: BSD-3-Clause
metadata:
    skill-author: Kuan-lin Huang
---

# scVelo — RNA 速度分析

## 概述

scVelo 是用于单细胞 RNA-seq 数据中 RNA 速度分析的领先 Python 软件包。它通过对 mRNA 剪接动力学建模来推断细胞状态转变——使用未剪接（前 mRNA）与剪接（成熟 mRNA）丰度的比率来确定每个细胞中基因是否上调或下调。这允许重建发育轨迹并识别细胞命运决定，而无需时间过程数据。

* *安装：** `pip install scvelo`

* *关键资源：**
- 文档：https://scvelo.readthedocs.io/
- GitHub：https://github.com/theislab/scvelo
- 论文：卑尔根等人。 （2020）自然生物技术。 PMID：32747759

## 何时使用此技能

在以下情况下使用scVelo：

- **从快照数据推断轨迹**：确定细胞分化的方向
- **细胞命运预测**：识别祖细胞及其下游命运
- **驱动程序基因识别**：找到动态最能解释观察到的轨迹的基因
- **发育生物学**：造血、神经发生、上皮间质转化模型
- **潜伏时间估计**：沿着剪接动力学衍生的伪时间对细胞进行排序
- **对Scanpy的补充**：向UMAP添加方向信息embeddings

## 先决条件

scVelo 需要 **未剪接** 和 **剪接** RNA 的计数矩阵。这些由：
1 生成。 **STARsolo** 或 **kallisto|bustools** 具有 `lamanno` 模式 
2. **速度** CLI：`velocyto run10x` / `velocyto run`
3. **alevin-fry** / **simpleaf** 具有拼接/未拼接输出

数据存储在 `AnnData` 对象中，其中包含 `layers["spliced"]` 和 `layers["unspliced"]`.

## 标准 RNA 速度工作流程

### 1. 设置和数据加载

```python
import scvelo as scv
import scanpy as sc
import numpy as np
import matplotlib.pyplot as plt

# Configure settings
scv.settings.verbosity = 3       # Show computation steps
scv.settings.presenter_view = True
scv.settings.set_figure_params('scvelo')

# Load data (AnnData with spliced/unspliced layers)
# Option A: Load from loom (velocyto output)
adata = scv.read("cellranger_output.loom", cache=True)

# Option B: Merge velocyto loom with Scanpy-processed AnnData
adata_processed = sc.read_h5ad("processed.h5ad")  # Has UMAP, clusters
adata_velocity = scv.read("velocyto.loom")
adata = scv.utils.merge(adata_processed, adata_velocity)

# Verify layers
print(adata)
# obs × var: N × G
# layers: 'spliced', 'unspliced' (required)
# obsm['X_umap'] (required for visualization)
```

### 2.预处理

```python
# Filter and normalize (follows Scanpy conventions)
scv.pp.filter_and_normalize(
    adata,
    min_shared_counts=20,   # Minimum counts in spliced+unspliced
    n_top_genes=2000        # Top highly variable genes
)

# Compute first and second order moments (means and variances)
# knn_connectivities must be computed first
sc.pp.neighbors(adata, n_neighbors=30, n_pcs=30)
scv.pp.moments(
    adata,
    n_pcs=30,
    n_neighbors=30
)
```

### 3. 速度估计 — 随机模型

随机模型速度快，适合探索性分析：

```python
# Stochastic velocity (faster, less accurate)
scv.tl.velocity(adata, mode='stochastic')
scv.tl.velocity_graph(adata)

# Visualize
scv.pl.velocity_embedding_stream(
    adata,
    basis='umap',
    color='leiden',
    title="RNA Velocity (Stochastic)"
)
```

### 4. 速度估计 — 动态模型（推荐）

动态模型完全拟合剪接动力学，更准确：

```python
# Recover dynamics (computationally intensive; ~10-30 min for 10K cells)
scv.tl.recover_dynamics(adata, n_jobs=4)

# Compute velocity from dynamical model
scv.tl.velocity(adata, mode='dynamical')
scv.tl.velocity_graph(adata)
```

### 5. 潜伏时间

动态模型可以计算共享潜伏时间（伪时间）：

```python
# Compute latent time
scv.tl.latent_time(adata)

# Visualize latent time on UMAP
scv.pl.scatter(
    adata,
    color='latent_time',
    color_map='gnuplot',
    size=80,
    title='Latent time'
)

# Identify top genes ordered by latent time
top_genes = adata.var['fit_likelihood'].sort_values(ascending=False).index[:300]
scv.pl.heatmap(
    adata,
    var_names=top_genes,
    sortby='latent_time',
    col_color='leiden',
    n_convolve=100
)
```

### 6. 驱动基因分析

```python
# Identify genes with highest velocity fit
scv.tl.rank_velocity_genes(adata, groupby='leiden', min_corr=0.3)
df = scv.DataFrame(adata.uns['rank_velocity_genes']['names'])
print(df.head(10))

# Speed and coherence
scv.tl.velocity_confidence(adata)
scv.pl.scatter(
    adata,
    c=['velocity_length', 'velocity_confidence'],
    cmap='coolwarm',
    perc=[5, 95]
)

# Phase portraits for specific genes
scv.pl.velocity(adata, ['Cpe', 'Gnao1', 'Ins2'],
               ncols=3, figsize=(16, 4))
```

### 7. 速度箭头和伪时间

```python
# Arrow plot on UMAP
scv.pl.velocity_embedding(
    adata,
    arrow_length=3,
    arrow_size=2,
    color='leiden',
    basis='umap'
)

# Stream plot (cleaner visualization)
scv.pl.velocity_embedding_stream(
    adata,
    basis='umap',
    color='leiden',
    smooth=0.8,
    min_mass=4
)

# Velocity pseudotime (alternative to latent time)
scv.tl.velocity_pseudotime(adata)
scv.pl.scatter(adata, color='velocity_pseudotime', cmap='gnuplot')
```

### 8. PAGA 轨迹图

```python
# PAGA graph with velocity-informed transitions
scv.tl.paga(adata, groups='leiden')
df = scv.get_df(adata, 'paga/transitions_confidence', precision=2).T
df.style.background_gradient(cmap='Blues').format('{:.2g}')

# Plot PAGA with velocity
scv.pl.paga(
    adata,
    basis='umap',
    size=50,
    alpha=0.1,
    min_edge_width=2,
    node_size_scale=1.5
)
```

## 完整工作流程脚本

```python
import scvelo as scv
import scanpy as sc

def run_rna_velocity(adata, n_top_genes=2000, mode='dynamical', n_jobs=4):
    """
    Complete RNA velocity workflow.

    Args:
        adata: AnnData with 'spliced' and 'unspliced' layers, UMAP in obsm
        n_top_genes: Number of top HVGs for velocity
        mode: 'stochastic' (fast) or 'dynamical' (accurate)
        n_jobs: Parallel jobs for dynamical model

    Returns:
        Processed AnnData with velocity information
    """
    scv.settings.verbosity = 2

    # 1. Preprocessing
    scv.pp.filter_and_normalize(adata, min_shared_counts=20, n_top_genes=n_top_genes)

    if 'neighbors' not in adata.uns:
        sc.pp.neighbors(adata, n_neighbors=30)

    scv.pp.moments(adata, n_pcs=30, n_neighbors=30)

    # 2. Velocity estimation
    if mode == 'dynamical':
        scv.tl.recover_dynamics(adata, n_jobs=n_jobs)

    scv.tl.velocity(adata, mode=mode)
    scv.tl.velocity_graph(adata)

    # 3. Downstream analyses
    if mode == 'dynamical':
        scv.tl.latent_time(adata)
        scv.tl.rank_velocity_genes(adata, groupby='leiden', min_corr=0.3)

    scv.tl.velocity_confidence(adata)
    scv.tl.velocity_pseudotime(adata)

    return adata
```

## AnnData中的关键输出字段

运行工作流后，添加以下字段：

|地点 |关键|描述 |
|----------|-----|-------------|
| `adata.layers` | `velocity` |每个细胞每个基因的RNA速度|
| `adata.layers` | `fit_t` |每个细胞每个基因的拟合潜伏时间 |
| `adata.obsm` | `velocity_umap` | UMAP 上的二维速度矢量 |
| `adata.obs` | `velocity_pseudotime` |速度伪时间|
| `adata.obs` | `latent_time` |动力学模型的潜伏时间|
| `adata.obs` | `velocity_length` |每个单元的速度|
| `adata.obs` | `velocity_confidence` |每个单元格的置信度得分 |
| `adata.var` | `fit_likelihood` |基因级模型拟合质量|
| `adata.var` | `fit_alpha` |转录率|
| `adata.var` | `fit_beta` |拼接率|
| `adata.var` | `fit_gamma` |降解率|
| `adata.uns` | `velocity_graph` |细胞-细胞转移概率矩阵 |

## 速度模型比较

|型号|速度|准确度|何时使用 |
|-------|--------|---------|--------------|
| `stochastic` |快|中等|探索性；大型数据集|
| `deterministic` |中等|中等|简单线性动力学|
| `dynamical` |慢|高|出版质量；识别驱动基因 |

## 最佳实践

- **从随机模式开始**进行探索；切换到动态进行最终分析
- **需要未拼接读数的良好覆盖**：短读数（< 100 bp）可能会错过内含子覆盖
- **最少2,000个细胞**：RNA速度在细胞较少时有噪音
- **速度应该一致**：箭头应遵循已知的生物学；随机性表明存在问题
- **k-NN 带宽很重要**：邻居太少 → 速度有噪声；太多 → 过度平滑
- **健全性检查**：根细胞（祖细胞）应该具有高标记基因的未剪接/剪接比率
- **动态模型需要不同的动力学状态**：最适合清晰的分化过程

## 故障排除

|问题 |解决方案 |
|---------|---------|
|未拼接层缺失 |重新运行 velocity 或使用 STARsolo 与 `--soloFeatures Gene Velocyto` |
|速度基因很少|下`min_shared_counts`；检查测序深度|
|随机外观的箭头 |尝试不同的`n_neighbors`或速度模型|
|动态内存错误|设置`n_jobs=1`；减少`n_top_genes` |
|到处都是负速度|检查拼接/未拼接层是否未交换 |

## 其他资源

- **scVelo 文档**：https://scvelo.readthedocs.io/
- **教程笔记本**：https://scvelo.readthedocs.io/tutorials/
- **GitHub**：https://github.com/theislab/scvelo
- **论文**：Bergen V 等人。 （2020）自然生物技术。 PMID：32747759
- **velocyto**（预处理）：http://velocyto.org/
- **CellRank**（命运预测，扩展scVelo）：https://cellrank.readthedocs.io/
- **dynamo**（代谢标记替代方案）： https://dynamo-release.readthedocs.io/
