# scVelo 速度模型参考

## 数学框架

RNA 速度基于转录的动力学模型：

```
dx_s/dt = β·x_u - γ·x_s   (spliced dynamics)
dx_u/dt = α(t) - β·x_u    (unspliced dynamics)
```

 其中：
- `x_s`：剪接的 mRNA 丰度
- `x_u`：未剪接（前 mRNA）丰度
- `α(t)`：转录率（随时间变化）
- `β`：剪接率
- `γ`：降解率

* *速度**定义为： `v = dx_s/dt = β·x_u - γ·x_s`

- **v > 0**：基因正在上调（在稳态下未剪接比预期更多）
- **v < 0**：基因正在下调（未剪接比预期更少）

## 模型比较

### 稳态（Velocyto，原始）

- 假设常数 α（转录率）
- 在稳态细胞上使用线性回归拟合 γ
- **限制**：需要可识别的稳态；假设恒定转录

```python
# Use with scVelo for backward compatibility
scv.tl.velocity(adata, mode='steady_state')
```

### 随机模型 (scVelo v1)

- 使用方差/协方差项扩展稳态
- 模拟 mRNA 计数中的细胞间变异
- 对噪声的鲁棒性比稳态

```python
scv.tl.velocity(adata, mode='stochastic')
```

### 动态模型（scVelo v2，推荐）

- 联合估计所有动力学速率（α、β、γ）和细胞特异性潜伏时间
- 不假设稳态
- 识别诱导与抑制Phase
- 计算每个基因的拟合可能性（质量测量）

```python
scv.tl.recover_dynamics(adata, n_jobs=4)
scv.tl.velocity(adata, mode='dynamical')
```

* *由动力学模型识别的动力学状态：**

|状态|描述 |
|--------|--------------|
|感应| α > 0，x_u 增加 |
|稳态开启| α > 0，恒定高表达|
|镇压| α = 0，x_u 递减 |
|稳态关闭| α = 0，恒定低表达 |

## 速度图

速度图根据细胞与相邻细胞状态的速度相似性来连接细胞：

```python
scv.tl.velocity_graph(adata)
# Stored in adata.uns['velocity_graph']
# Entry [i,j] = probability that cell i transitions to cell j
```

* *参数：**
- `n_neighbors`：考虑的邻居数量
- `sqrt_transform`：对数据应用 sqrt 变换（默认值：拼接时为 False） 
- `approx`：使用近似最近邻搜索（对于大型数据更快）数据集）

## 潜伏时间解释

每个基因的潜伏时间 τ ∈ [0, 1]代表：
- τ = 0：基因处于诱导开始状态
- τ = 0.5：基因处于诱导峰值（对于一个完整的周期）
- τ = 1：基因已恢复到稳态off

* *共享潜伏时间**是通过取所有速度基因的平均值并按 fit_likelihood 加权来计算的。

## 质量指标

### 基因级别
- `fit_likelihood`：动态模型的拟合优度（0-1；更高=更好）
  - 用于过滤驱动程序基因：`adata.var[adata.var['fit_likelihood'] > 0.1]`
- `fit_alpha`：诱导过程中的转录率
- `fit_gamma`：mRNA降解率
- `fit_r2`：动力学拟合的R²

### 细胞水平
- `velocity_length`：速度矢量的大小（单元速度）
- `velocity_confidence`：速度与相邻单元的相干性（0-1）

### 数据集级别
```python
# Check overall velocity quality
scv.pl.proportions(adata)  # Ratio of spliced/unspliced per cell
scv.pl.velocity_confidence(adata, groupby='leiden')
```

## 参数调优指南

|参数|功能|默认|何时更改|
|---------|----------|---------|----------------|
| `min_shared_counts` |过滤基因| 20 |增加深度测序；浅层减少|
| `n_top_genes` | HVG选择| 2000 | 2000复杂数据集的增加|
| `n_neighbors` | kNN 图 | 30|小数据集减少；增加噪音 |
| `n_pcs` | PCA尺寸| 30|与碎石图中的肘部匹配 |
| `t_max_rank` |潜伏时间约束 |无 |设置已知的发育方向 |

## 与其他工具集成

### CellRank（命运预测）

```python
import cellrank as cr
from cellrank.kernels import VelocityKernel, ConnectivityKernel

# Combine velocity and connectivity kernels
vk = VelocityKernel(adata).compute_transition_matrix()
ck = ConnectivityKernel(adata).compute_transition_matrix()
combined = 0.8 * vk + 0.2 * ck

# Compute macrostates (terminal and initial states)
g = cr.estimators.GPCCA(combined)
g.compute_macrostates(n_states=4, cluster_key='leiden')
g.plot_macrostates(which="all")

# Compute fate probabilities
g.compute_fate_probabilities()
g.plot_fate_probabilities()
```

### Scanpy 集成

scVelo 与 Scanpy 原生配合使用AnnData:

```python
import scanpy as sc
import scvelo as scv

# Run standard Scanpy pipeline first
sc.pp.normalize_total(adata)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata)
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)
sc.tl.leiden(adata)

# Then add velocity on top
scv.pp.moments(adata)
scv.tl.recover_dynamics(adata)
scv.tl.velocity(adata, mode='dynamical')
scv.tl.velocity_graph(adata)
scv.tl.latent_time(adata)
```
