---
name: umap-learn
description: UMAP 降维。针对高维数据的 2D/3D 可视化、聚类预处理 (HDBSCAN)、监督/参数 UMAP 的快速非线性流形学习。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# UMAP-Learn

## 概述

UMAP（统一流形逼近和投影）是一种用于可视化和一般非线性降维的降维技术。应用此技能可实现快速、可扩展的嵌入，从而保留本地和全局结构、监督学习和聚类预处理。

## 快速入门

### 安装

```bash
uv pip install umap-learn
```

### 基本用法

UMAP 遵循 scikit-learn 约定，可用作t-SNE 或 PCA.

```python
import umap
from sklearn.preprocessing import StandardScaler

# Prepare data (standardization is essential)
scaled_data = StandardScaler().fit_transform(data)

# Method 1: Single step (fit and transform)
embedding = umap.UMAP().fit_transform(scaled_data)

# Method 2: Separate steps (for reusing trained model)
reducer = umap.UMAP(random_state=42)
reducer.fit(scaled_data)
embedding = reducer.embedding_  # Access the trained embedding
```

* *关键预处理要求：** 在应用 UMAP 之前始终将特征标准化为可比较的尺度，以确保各个维度的权重相等。

### 典型工作流程

```python
import umap
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# 1. Preprocess data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(raw_data)

# 2. Create and fit UMAP
reducer = umap.UMAP(
    n_neighbors=15,
    min_dist=0.1,
    n_components=2,
    metric='euclidean',
    random_state=42
)
embedding = reducer.fit_transform(scaled_data)

# 3. Visualize
plt.scatter(embedding[:, 0], embedding[:, 1], c=labels, cmap='Spectral', s=5)
plt.colorbar()
plt.title('UMAP Embedding')
plt.show()
```

## 参数调优Guide

UMAP 有四个控制嵌入行为的主要参数。了解这些对于有效使用至关重要。

### n_neighbors（默认值：15）

* *用途：**平衡嵌入中的局部结构与全局结构。

* *工作原理：**控制学习流形结构时 UMAP 检查的局部邻域的大小。

* *效果值：**
- **低值 (2-5)：** 强调精细的局部细节，但可能将数据分段为断开连接的组件
- **中值 (15-20)：** 局部结构和全局关系的平衡视图（推荐起点）
- **高值 (50-200)：** 优先考虑广泛的拓扑结构，但会牺牲细粒度细节

* *建议：**从15开始，根据结果进行调整。增加以获得更多全局结构，减少以获得更多局部细节。

### min_dist（默认值：0.1）

* *用途：**控制低维空间中点簇的紧密程度。

* *工作原理：**设置输出表示中允许点之间的最小距离。

* *按值影响：**
- **低值 (0.0-0.1)：** 创建对聚类有用的聚集嵌入；揭示精细的拓扑细节
- **高值 (0.5-0.99)：** 防止紧密堆积；强调局部结构上的广泛拓扑保存

* *建议：** 使用 0.0 用于聚类应用，0.1-0.3 用于可视化，0.5+ 用于松散结构。

### n_components（默认值：2）

* *用途：** 确定嵌入输出空间的维度。

* *关键特征：** 不同于t-SNE、UMAP 在嵌入维度上可以很好地扩展，从而能够在可视化之外使用。

* *常见用途：**
- **2-3 维度：** 可视化
- **5-10 维度：** 聚类预处理（比 2D 更好地保留密度）
- **10-50 维度：** 下游 ML 的特征工程models

* *建议：** 使用 2 进行可视化，使用 5-10 进行聚类，对于 ML 管道使用更高的值。

### 度量（默认值：'euclidean'）

* *用途：**指定如何计算输入数据点之间的距离。

* *支持的度量：**
- **Minkowski变体：** euclidean、manhattan、chebyshev
- **空间指标：** canberra、braycurtis、haversine
- **相关性指标：** 余弦、相关性（适用于文本/文档嵌入）
- **二进制数据指标：** hamming、jaccard、dice、russellrao、 kulsinski, rogerstanimoto, sokalmichener, sokalsneath, yule
- **自定义指标：** 通过 Numba

 用户定义的距离函数 **建议：** 对数字数据使用欧几里德，对文本/文档向量使用余弦，对二进制数据使用汉明。

### 参数调优示例

```python
# For visualization with emphasis on local structure
umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, metric='euclidean')

# For clustering preprocessing
umap.UMAP(n_neighbors=30, min_dist=0.0, n_components=10, metric='euclidean')

# For document embeddings
umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, metric='cosine')

# For preserving global structure
umap.UMAP(n_neighbors=100, min_dist=0.5, n_components=2, metric='euclidean')
```

## 监督和半监督降维

UMAP支持合并标签信息来指导嵌入过程，在保留内部结构的同时实现类分离。

### 监督UMAP

拟合时通过 `y` 参数传递目标标签：

```python
# Supervised dimension reduction
embedding = umap.UMAP().fit_transform(data, y=labels)
```

* *主要优点：**
- 实现清晰分离的类
- 保留每个类内的内部结构
- 维护类之间的全局关系

* *何时使用：** 当您已标记数据并想要分离已知的类，同时保持有意义的点嵌入。

### 半监督UMAP

对于部分标签，按照scikit-learn约定使用`-1`标记未标记的点：

```python
# Create semi-supervised labels
semi_labels = labels.copy()
semi_labels[unlabeled_indices] = -1

# Fit with partial labels
embedding = umap.UMAP().fit_transform(data, y=semi_labels)
```

* *何时使用：**当标签成本昂贵或数据多于标签时

### 使用 UMAP 进行度量学习

在标记数据上训练监督嵌入，然后应用于新的未标记数据：

```python
# Train on labeled data
mapper = umap.UMAP().fit(train_data, train_labels)

# Transform unlabeled test data
test_embedding = mapper.transform(test_data)

# Use as feature engineering for downstream classifier
from sklearn.svm import SVC
clf = SVC().fit(mapper.embedding_, train_labels)
predictions = clf.predict(test_embedding)
```

* *何时使用：** 用于机器学习管道中的监督特征工程。

## UMAP for聚类

UMAP 可作为基于密度的聚类算法（如 HDBSCAN）的有效预处理，克服维数灾难。

### 聚类最佳实践

* *关键原则：**为聚类和可视化配置不同的 UMAP。

* *推荐参数：**
- **n_neighbors:** 增加到~30（默认 15 太局部，可以创建人工细粒度簇）
- **min_dist：** 设置为 0.0（在簇内密集填充点以获得更清晰的边界）
- **n_components：** 使用 5-10 维度（保持性能，同时提高密度保留与 2D 相比）

### 聚类工作流程

```python
import umap
import hdbscan
from sklearn.preprocessing import StandardScaler

# 1. Preprocess data
scaled_data = StandardScaler().fit_transform(data)

# 2. UMAP with clustering-optimized parameters
reducer = umap.UMAP(
    n_neighbors=30,
    min_dist=0.0,
    n_components=10,  # Higher than 2 for better density preservation
    metric='euclidean',
    random_state=42
)
embedding = reducer.fit_transform(scaled_data)

# 3. Apply HDBSCAN clustering
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=15,
    min_samples=5,
    metric='euclidean'
)
labels = clusterer.fit_predict(embedding)

# 4. Evaluate
from sklearn.metrics import adjusted_rand_score
score = adjusted_rand_score(true_labels, labels)
print(f"Adjusted Rand Score: {score:.3f}")
print(f"Number of clusters: {len(set(labels)) - (1 if -1 in labels else 0)}")
print(f"Noise points: {sum(labels == -1)}")
```

### 聚类后可视化

```python
# Create 2D embedding for visualization (separate from clustering)
vis_reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, random_state=42)
vis_embedding = vis_reducer.fit_transform(scaled_data)

# Plot with cluster labels
import matplotlib.pyplot as plt
plt.scatter(vis_embedding[:, 0], vis_embedding[:, 1], c=labels, cmap='Spectral', s=5)
plt.colorbar()
plt.title('UMAP Visualization with HDBSCAN Clusters')
plt.show()
```

* *重要警告：** UMAP 不能完全保留密度，并且可以创建人工聚类划分。始终验证和探索生成的集群。

## 转换新数据

UMAP 通过其 `transform()` 方法实现新数据的预处理，允许经过训练的模型将未见过的数据投影到学习的嵌入空间中。

### 基本转换用法

```python
# Train on training data
trans = umap.UMAP(n_neighbors=15, random_state=42).fit(X_train)

# Transform test data
test_embedding = trans.transform(X_test)
```

### 与机器学习管道集成

```python
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import umap

# Split data
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)

# Preprocess
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train UMAP
reducer = umap.UMAP(n_components=10, random_state=42)
X_train_embedded = reducer.fit_transform(X_train_scaled)
X_test_embedded = reducer.transform(X_test_scaled)

# Train classifier on embeddings
clf = SVC()
clf.fit(X_train_embedded, y_train)
accuracy = clf.score(X_test_embedded, y_test)
print(f"Test accuracy: {accuracy:.3f}")
```

### 重要注意事项

* *数据一致性：**变换方法假设高维空间中的整体分布在训练数据和测试数据之间是一致的。当此假设失败时，请考虑使用参数化 UMAP。

* *性能：** 转换操作非常高效（通常 <1 秒），但由于 Numba JIT 编译，初始调用可能会更慢。

* *Scikit-learn 兼容性：** UMAP 遵循标准 sklearn 约定，并在管道：

XQBLOCK11QXZ
## 高级功能

### 参数化UMAP

参数化UMAP用学习的神经网络映射函数替换直接嵌入优化。

* *与标准UMAP的主要区别：**
- 使用TensorFlow/Keras训练编码器网络
- 实现新数据的高效转换
- 支持通过解码器网络重建（逆变换）
- 允许自定义架构（用于图像的CNN，用于序列的RNN）

* *安装：**
```bash
uv pip install umap-learn[parametric_umap]
# Requires TensorFlow 2.x
```

* *基本用法：**
```python
from umap.parametric_umap import ParametricUMAP

# Default architecture (3-layer 100-neuron fully-connected network)
embedder = ParametricUMAP()
embedding = embedder.fit_transform(data)

# Transform new data efficiently
new_embedding = embedder.transform(new_data)
```

* *自定义架构：**
```python
import tensorflow as tf

# Define custom encoder
encoder = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(input_dim,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(2)  # Output dimension
])

embedder = ParametricUMAP(encoder=encoder, dims=(input_dim,))
embedding = embedder.fit_transform(data)
```

* *何时使用Parametric UMAP：**
- 训练后需要对新数据进行高效变换
- 需要重建能力（逆
- 希望将 UMAP 与自动编码器结合起来
- 受益于专用架构的复杂数据类型（图像、序列）

* *何时使用标准 UMAP：**
- 需要简单和快速的原型设计
- 数据集很小，计算效率并不重要
- 未来数据不需要学习变换

### 逆变换

逆变换可以从低维嵌入重建高维数据。

* *基本用法：**
```python
reducer = umap.UMAP()
embedding = reducer.fit_transform(data)

# Reconstruct high-dimensional data from embedding coordinates
reconstructed = reducer.inverse_transform(embedding)
```

* *重要限制：**
- 计算量大的操作
- 在凸包之外效果不佳嵌入
- 簇之间有间隙的区域的准确度降低

* *用例：**
- 了解嵌入数据的结构
- 可视化簇之间的平滑过渡
- 探索数据点之间的插值
- 在嵌入中生成合成样本space

* *示例：探索嵌入空间：**
```python
import numpy as np

# Create grid of points in embedding space
x = np.linspace(embedding[:, 0].min(), embedding[:, 0].max(), 10)
y = np.linspace(embedding[:, 1].min(), embedding[:, 1].max(), 10)
xx, yy = np.meshgrid(x, y)
grid_points = np.c_[xx.ravel(), yy.ravel()]

# Reconstruct samples from grid
reconstructed_samples = reducer.inverse_transform(grid_points)
```

### AlignedUMAP

用于分析时间或相关数据集（例如，时间序列实验、批处理）数据）：

```python
from umap import AlignedUMAP

# List of related datasets
datasets = [day1_data, day2_data, day3_data]

# Create aligned embeddings
mapper = AlignedUMAP().fit(datasets)
aligned_embeddings = mapper.embeddings_  # List of embeddings
```

* *何时使用：**比较相关数据集之间的嵌入，同时保持一致的坐标系。

## 再现性

为了确保可再现的结果，请始终设置`random_state`参数：

```python
reducer = umap.UMAP(random_state=42)
```

UMAP 使用随机优化，因此在没有固定随机状态的运行之间结果会略有不同。

## 常见问题和解决方案

* *问题：** 断开的组件或碎片集群
- **解决方案：** 增加 `n_neighbors` 以强调更全局结构

* *问题：**聚类过于分散或分离不好
- **解决方案：**减少`min_dist`以允许更紧密的包装

* *问题：**聚类结果较差
- **解决方案：**使用聚类特定参数（n_neighbors=30，min_dist=0.0， n_components=5-10)

* *问题：**转换结果与训练明显不同
- **解决方案：**确保测试数据分布与训练匹配，或使用参数化 UMAP

* *问题：**大型数据集上性能缓慢
- **解决方案：**设置 `low_memory=True`（默认），或考虑使用降维PCA第一

* *问题：**所有点折叠成单个簇
- **解决方案：**检查数据预处理（确保适当缩放），增加`min_dist`

## 资源

### 参考文献/

包含详细的API文档：
- `api_reference.md`：完整的UMAP类参数和methods

当需要详细参数信息或高级方法使用时加载这些参考。
