# scEmbed：单细胞嵌入生成

## 概述

scEmbed 在单细胞 ATAC-seq 数据集上训练 Region2Vec 模型，以生成用于聚类和分析的细胞嵌入。它提供了一个无监督机器学习框架，用于表示和分析低维空间中的 scATAC-seq 数据。

## 何时使用

在处理以下内容时使用 scEmbed：
- 需要聚类的单细胞 ATAC-seq (scATAC-seq)数据
- 细胞类型注释任务
- 单细胞降维染色质可及性
- 与 scanpy 工作流程集成以进行下游分析

## 工作流程

### 步骤 1：数据准备

输入数据必须采用 AnnData 格式，且 `.var` 属性包含 `chr`、`start` 和`end` 峰值。

* *从原始数据开始**（barcodes.txt、peaks.bed、matrix.mtx）：

```python
import scanpy as sc
import pandas as pd
import scipy.io
import anndata

# Load data
barcodes = pd.read_csv('barcodes.txt', header=None, names=['barcode'])
peaks = pd.read_csv('peaks.bed', sep='\t', header=None,
                    names=['chr', 'start', 'end'])
matrix = scipy.io.mmread('matrix.mtx').tocsr()

# Create AnnData
adata = anndata.AnnData(X=matrix.T, obs=barcodes, var=peaks)
adata.write('scatac_data.h5ad')
```

### 步骤 2：预标记化

使用 gtars 实用程序将基因组区域转换为标记。这将创建一个包含标记化单元的镶木地板文件，以实现更快的训练：

```python
from geniml.io import tokenize_cells

tokenize_cells(
    adata='scatac_data.h5ad',
    universe_file='universe.bed',
    output='tokenized_cells.parquet'
)
```

* *预标记化的好处：**
- 更快的训练迭代
- 减少内存需求
- 可重复使用标记化数据以进行多次训练

### 步骤3：模型训练

使用标记化数据训练scEmbed模型：

```python
from geniml.scembed import ScEmbed
from geniml.region2vec import Region2VecDataset

# Load tokenized dataset
dataset = Region2VecDataset('tokenized_cells.parquet')

# Initialize and train model
model = ScEmbed(
    embedding_dim=100,
    window_size=5,
    negative_samples=5
)

model.train(
    dataset=dataset,
    epochs=100,
    batch_size=256,
    learning_rate=0.025
)

# Save model
model.save('scembed_model/')
```

### 步骤4：生成单元嵌入

使用训练后的模型生成单元嵌入：

```python
from geniml.scembed import ScEmbed

# Load trained model
model = ScEmbed.from_pretrained('scembed_model/')

# Generate embeddings for AnnData object
embeddings = model.encode(adata)

# Add to AnnData for downstream analysis
adata.obsm['scembed_X'] = embeddings
```

### 步骤5：下游分析

与scanpy集成进行聚类和可视化：

```python
import scanpy as sc

# Use scEmbed embeddings for neighborhood graph
sc.pp.neighbors(adata, use_rep='scembed_X')

# Cluster cells
sc.tl.leiden(adata, resolution=0.5)

# Compute UMAP for visualization
sc.tl.umap(adata)

# Plot results
sc.pl.umap(adata, color='leiden')
```

## 关键参数

### 训练参数

|参数|描述 |典型范围|
|---------|--------------|---------------|
| `embedding_dim` |细胞嵌入的尺寸 | 50 - 200 |
| `window_size` |训练上下文窗口 | 3 - 10 |
| `negative_samples` |负样本数量| 5 - 20 |
| `epochs` |训练纪元 | 50 - 200 |
| `batch_size` |训练批量大小 | 128 - 512 |
| `learning_rate` |初始学习率| 0.01 - 0.05 |

### 标记化参数

- **Universe 文件**：定义基因组词汇的参考 BED 文件
- **重叠阈值**：峰-宇宙匹配的最小重叠（通常为 1e-9）

## 预训练模型

预训练 scEmbed 模型可在拥抱常见参考数据集的脸部。使用以下方式加载它们：

```python
from geniml.scembed import ScEmbed

# Load pre-trained model
model = ScEmbed.from_pretrained('databio/scembed-pbmc-10k')

# Generate embeddings
embeddings = model.encode(adata)
```

## 最佳实践

- **数据质量**：使用过滤后的峰值条形码矩阵，而不是原始计数
- **预标记化**：始终预标记化以提高训练效率
- **参数调整**：调整`embedding_dim` 和基于数据集大小的训练周期 
- **验证**：使用已知的细胞类型标记来验证聚类质量
- **集成**：与 scanpy 结合进行全面的单细胞分析
- **模型共享**：将训练好的模型导出到 Hugging Face 以实现可重复性

## 示例数据集

10x Genomics PBMC 10k 数据集（10,000 个外周血单核细胞）作为标准基准：
- 包含多种免疫细胞类型
- 良好表征的细胞群
- 可从 10x Genomics 网站获取

## 细胞类型注释

聚类后，使用k近邻（KNN）和参考数据集注释细胞类型：

```python
from geniml.scembed import annotate_celltypes

# Annotate using reference
annotations = annotate_celltypes(
    query_adata=adata,
    reference_adata=reference,
    embedding_key='scembed_X',
    k=10
)

adata.obs['cell_type'] = annotations
```

## 输出

scEmbed 生成：
- 低维单元嵌入（存储在 `adata.obsm` 中）
- 训练后的模型文件以供重用
- scanpy 下游分析的兼容格式
- 可选择导出到 Hugging Face 以进行共享
