# UMAP API 参考

## UMAP 类

`umap.UMAP(n_neighbors=15, n_components=2, metric='euclidean', n_epochs=None, learning_rate=1.0, init='spectral', min_dist=0.1, spread=1.0, low_memory=True, set_op_mix_ratio=1.0, local_connectivity=1.0, repulsion_strength=1.0, negative_sample_rate=5, transform_queue_size=4.0, a=None, b=None, random_state=None, metric_kwds=None, angular_rp_forest=False, target_n_neighbors=-1, target_metric='categorical', target_metric_kwds=None, target_weight=0.5, transform_seed=42, transform_mode='embedding', force_approximation_algorithm=False, verbose=False, unique=False, densmap=False, dens_lambda=2.0, dens_frac=0.3, dens_var_shift=0.1, output_dens=False, disconnection_distance=None, precomputed_knn=(None, None, None))`

 查找近似数据底层流形的低维嵌入。

### 核心参数

#### n_neighbors (int, default: 15)
用于流形的局部邻域的大小近似值。较大的值会产生更多的流形全局视图，而较小的值会保留更多的局部结构。一般在2到100的范围内。

* *调整指导：**
- 使用2-5表示非常局部的结构
- 使用10-20表示平衡的局部/全局结构（典型）
- 使用50-200表示全局结构

#### n_components（int，默认值： 2)
嵌入空间的尺寸。与 t-SNE 不同，UMAP 随着嵌入维度的增加而扩展良好。

* *常用值：**
- 2-3：可视化
- 5-10：聚类预处理
- 10-100：下游 ML

#### 指标（str 或可调用，默认： 'euclidean')
要使用的距离度量。接受：
- scipy.spatial.distance 中的任何度量
- sklearn.metrics 中的任何度量
- 自定义可调用距离函数（必须使用 Numba 编译）

* *常用度量：**
- `'euclidean'`：标准欧几里德距离（默认）
- `'manhattan'`：L1 距离
- `'cosine'`：余弦距离（适用于文本/文档向量）
- `'correlation'`：相关距离
- `'hamming'`：汉明距离（适用于二进制）数据）
- `'jaccard'`：杰卡德距离（对于二进制/设置数据）
- `'dice'`：骰子距离
- `'canberra'`：堪培拉距离
- `'braycurtis'`：Bray-Curtis距离
- `'chebyshev'`：切比雪夫距离
- `'minkowski'`：明可夫斯基距离（用metric_kwds指定p）
- `'precomputed'`：使用预先计算的距离矩阵

#### min_dist (float, 默认: 0.1)
E 嵌入点之间的有效最小距离。控制点堆积在一起的紧密程度。较小的值会导致更密集的嵌入。

* *调整指导：**
- 使用0.0进行聚类应用
- 使用0.1-0.3进行可视化（平衡）
- 使用0.5-0.99进行松散结构保存

#### 传播（浮动，默认： 1.0)
嵌入点的有效比例。与 `min_dist` 结合使用来控制聚集嵌入与分散嵌入。确定簇在嵌入空间中的分布情况。

### 训练参数

#### n_epochs（int，默认值：无）
训练纪元数。如果没有，则根据数据集大小自动确定（通常为 200-500 epoch）。

* *手动调整：**
- 较小的数据集可能需要 500+ epochs
- 较大的数据集可能会与 200 epochs 收敛
- 更多的 epochs = 更好的优化但更慢Training

#### learning_rate（浮点数，默认值：1.0）
SGD优化器的初始学习率。较高的值会导致更快的收敛，但可能会超出最佳解决方案。

#### init（str或np.ndarray，默认：'spectral'）
嵌入的初始化方法：
- `'spectral'`：使用光谱嵌入（默认，通常是最好的）
- `'random'`：随机初始化
- `'pca'`：使用PCA
初始化- numpy数组：自定义初始化（形状：（n_samples，n_components））

### 高级结构参数

#### local_connectivity（int，默认值： 1.0)
假设本地连接的最近邻居的数量。值越高，连接的流形越多。

#### set_op_mix_ratio (float, default: 1.0)
构造模糊集并集时并集和交集之间的插值。值 1.0 使用纯并集，0.0 使用纯交集。

#### repulsion_strength (float, default: 1.0)
低维嵌入优化中应用于负样本的权重。较高的值将嵌入点进一步分开。

#### negative_sample_rate（int，默认值：5）
每个正样本选择的负样本数。较高的值会导致点之间更大的排斥和更多的分散嵌入，但会增加计算成本。

### 监督学习参数

#### target_n_neighbors（int，默认值：-1）
构造目标单纯形集时使用的最近邻的数量。如果为-1，则使用n_neighbors值。

#### target_metric（str，默认值：'categorical'）
目标值（标签）的距离度量：
- `'categorical'`：用于分类任务
- 用于回归任务的任何其他度量

#### target_weight（float，默认值： 0.5)
应用于目标信息与数据结构的权重。范围 0.0 到 1.0：
- 0.0：纯无监督嵌入（忽略标签）
- 0.5：平衡（默认）
- 1.0：纯监督嵌入（仅考虑标签）

### 变换参数

#### transform_queue_size (float, 默认值: 4.0)
用于变换操作的最近邻搜索队列的大小。较大的值可以提高变换精度，但会增加内存使用量和计算时间。

#### transform_seed（int，默认值：42）
变换操作的随机种子。确保变换结果的再现性。

#### transform_mode (str, default: 'embedding')
变换新数据的方法：
- `'embedding'`：标准方法（默认）
- `'graph'`：使用最近邻图

### 性能参数

#### low_memory (bool, 默认: True)
是否使用内存高效的实现。仅当内存不受限制并且您想要更快的性能时才设置为 False。

#### verbose (bool, default: False)
拟合过程中是否打印进度消息。

#### unique (bool, default: False)
是否只考虑唯一的数据点。如果您知道数据包含许多重复项，请设置为 True 以提高性能。

#### force_approximation_algorithm（bool，默认值：False）
即使对于小型数据集，也强制使用近似最近邻搜索。可以提高大型数据集上的性能。

#### angular_rp_forest (bool, default: False)
是否使用角度随机投影森林进行最近邻搜索。可以提高高维度归一化数据的性能。

### DensMAP 参数

DensMAP 是保留局部密度信息的变体。

#### densmap (bool, 默认: False)
是否使用 DensMAP 算法而不是标准 UMAP。除拓扑结构外，还保留局部密度。

#### dens_lambda (float，默认值：2.0)
DensMAP 优化中密度保留项的权重。较高的值强调密度保留。

#### dens_frac（浮点型，默认值：0.3）
用于 DensMAP 中密度估计的数据集的分数。

#### dens_var_shift（浮点型，默认值：0.1）
用于 DensMAP 中密度估计的正则化参数。

#### output_dens (bool, 默认值: False)
除了嵌入之外是否输出局部密度估计。结果存储在 `rad_orig_` 和 `rad_emb_` 属性中。

### 其他参数

#### 一个（浮点型，默认值：无）
控制嵌入的参数。如果为 None，则根据 min_dist 和 spread 自动确定。

#### b (float，默认值：None)
控制嵌入的参数。如果无，则根据 min_dist 和 spread 自动确定。

#### random_state（int、RandomState 实例或 None，默认值：None）
用于再现性的随机状态。设置为整数以获得可重现的结果。

#### metric_kwds（字典，默认值：无）
距离度量的附加关键字参数。

#### disconnection_distance（浮点型，默认值：无）
考虑断开点的距离阈值。如果没有，则使用图中的最大距离。

#### precompulated_knn（元组，默认：（None，None，None））
预计算k-最近邻为（knn_indices，knn_dists，knn_search_index）。对于重用昂贵的计算非常有用。

## 方法

### fit(X, y=None)
将 UMAP 模型拟合到数据。

* *参数：**
- `X`：类似数组，形状 (n_samples, n_features) - 训练data
- `y`：类数组，形状（n_samples，），可选 - 监督降维的目标值

* *返回：**
- `self`：拟合的 UMAP 对象

* *属性集：**
- `embedding_`：训练数据的嵌入表示
- `graph_`：流形的模糊单纯集逼近
- `_raw_data`：训练数据的副本
- `_small_data`：数据集是否被视为小
- `_metric_kwds`：处理后的指标关键字参数
- `_n_neighbors`：实际使用的n_neighbors
- `_initial_alpha`：初始学习率
- `_a`，`_b`：曲线参数

### fit_transform(X, y=None)
拟合模型并返回嵌入表示。

* *参数：**
- `X`：类似数组，形状 (n_samples, n_features) - 训练数据
- `y`：类似数组，形状(n_samples,), 可选 - 监督降维的目标值

* *返回：**
- `X_new`: array, shape (n_samples, n_components) - 嵌入数据

### transform(X)
将新数据转换到现有嵌入空间中。

* *参数：**
- `X`：类似数组，形状（n_samples，n_features） - 要转换的新数据

  * *返回：**
- `X_new`：数组，形状（n_samples，n_components） - 新数据的嵌入表示

  * *重要注意：**
- 调用transform之前必须先拟合模型
- 变换质量取决于训练和测试分布之间的相似性
- 对于显着不同的数据分布，考虑参数化UMAP

### inverse_transform(X)
将数据从嵌入空间变换回原始数据space.

* *参数：**
- `X`：类似数组，形状（n_samples，n_components）-嵌入数据点

* *返回：**
- `X_new`：数组，形状（n_samples，n_features）-原始重建数据space

* *重要说明：**
- 计算成本较高的操作
- 在训练嵌入的凸包之外效果不佳
- 重建质量因区域而异

### update(X)
使用新数据更新模型。允许增量拟合。

* *参数：**
- `X`：类似数组，形状（n_samples，n_features）-要合并的新数据

* *返回：**
- `self`：更新的UMAP对象

* *注：**实验特征，可能不会保留批量训练的所有属性。

## Attributes

### embedding_
array, shape (n_samples, n_components) - 训练数据的嵌入表示。

### graph_
scipy.sparse.csr_matrix - 的加权邻接矩阵流形的模糊单纯形集逼近。

### _raw_data
array - 原始训练数据的副本。

### _sparse_data
bool - 训练数据是否稀疏。

### _small_data
bool - 数据集是否稀疏被认为很小（对小数据集使用不同的算法）。

### _input_hash
str - 用于缓存目的的输入数据的哈希值。

### _knn_indices
array - 每个训练点的 k 个最近邻的索引。

### _knn_dists
array - 每个训练点到 k 个最近邻的距离。

### _rp_forest
list - 用于近似最近邻的随机投影森林search.

## ParametricUMAP Class

`umap.ParametricUMAP(encoder=None, decoder=None, parametric_reconstruction=False, autoencoder_loss=False, reconstruction_validation=None, dims=None, batch_size=None, n_training_epochs=1, loss_report_frequency=10, optimizer=None, keras_fit_kwargs={}, **kwargs)`

使用神经网络学习嵌入函数的参数化UMAP。

#### 附加参数（除了UMAP）

#### 编码器（tensorflow.keras.Model，默认：None）
Keras模型用于编码数据到嵌入。如果为 None，则使用默认的 3 层架构，每层有 100 个神经元。

#### 解码器（tensorflow.keras.Model，默认值：None）
Keras 模型，用于将嵌入解码回数据空间。仅当parametric_reconstruction=True时使用。

#### parametric_reconstruction (bool, default: False)
是否使用参数化重建。需要解码器模型。

#### autoencoder_loss (bool, 默认: False)
是否在优化中包含重建损失。需要解码器模型。

#### reconstruction_validation（元组，默认：None）
训练期间用于监视重建损失的验证数据（X_val，y_val）。

#### dims（元组，默认：None）
编码器网络的输入维度。如果提供自定义编码器，则需要。

#### batch_size（int，默认值：None）
用于神经网络训练的批量大小。如果没有，则自动确定。 

#### n_training_epochs (int，默认值：1)
神经网络的训练纪元数。更多纪元可以提高质量，但会增加训练时间。

#### loss_report_Frequency（int，默认值：10）
训练期间报告损失的频率。

#### 优化器（tensorflow.keras.optimizers.Optimizer，默认值：None）
用于训练的Keras优化器。如果没有，则使用带有learning_rate参数的Adam。

#### keras_fit_kwargs (dict, default: {})
传递给 Keras fit()方法的附加关键字参数。

### 方法

与 UMAP 类相同，但 transform()和 inverse_transform()使用学习的神经网络进行更快的推理。

## 实用函数

### umap.nearest_neighbors(X, n_neighbors, metric, metric_kwds={}, angular=False, random_state=None)
计算数据的k近邻。

* *返回：** (knn_indices, knn_dists, rp_forest)

### umap.fuzzy_simplicial_set(X, n_neighbors, random_state, metric, metric_kwds={}, knn_indices=None, knn_dists=None, angular=False, set_op_mix_ratio=1.0, local_connectivity=1.0, apply_set_operations=True, verbose=False, return_dists=None)
构造数据的模糊单纯集表示。

* *返回：** 模糊单纯集作为稀疏矩阵

### umap.simplicial_set_embedding(data, graph, n_components, initial_alpha, a, b, gamma, negative_sample_rate, n_epochs, init, random_state, metric, metric_kwds, densmap, densmap_kwds、output_dens、output_metric、output_metric_kwds、euclidean_output、parallel=False、verbose=False)
执行优化以找到低维嵌入。

* *返回：**嵌入数组

### umap.find_ab_params(spread, min_dist)
Fit a, b params for the UMAP curve from spread and min_dist.

* *Returns:** (a, b) tuple

## AlignedUMAP Class

`umap.AlignedUMAP(n_neighbors=15, n_components=2, metric='euclidean', alignment_regularisation=1e-2, alignment_window_size=3, **kwargs)`

UMAP变体用于对齐多个相关datasets.

#### 附加参数

#### alignment_regularization（float，默认：1e-2）
数据集之间对齐正则化的强度。

#### alignment_window_size（int，默认：3）
要对齐的相邻数据集的数量。

### 方法

#### fit(X)
将模型拟合到多个数据集。

* *参数：**
- `X`：数组列表-要对齐的数据集列表

* *返回：**
- `self`：拟合型号

### 属性

#### embeddings_
数组列表 - 对齐嵌入列表，每个输入数据集一个。

## 用法示例

#### 所有常用参数的基本用法

```python
import umap

# Standard 2D visualization embedding
reducer = umap.UMAP(
    n_neighbors=15,          # Balance local/global structure
    n_components=2,          # Output dimensions
    metric='euclidean',      # Distance metric
    min_dist=0.1,           # Minimum distance between points
    spread=1.0,             # Scale of embedded points
    random_state=42,        # Reproducibility
    n_epochs=200,           # Training iterations (None = auto)
    learning_rate=1.0,      # SGD learning rate
    init='spectral',        # Initialization method
    low_memory=True,        # Memory-efficient mode
    verbose=True            # Print progress
)

embedding = reducer.fit_transform(data)
```

### 受监督学习

```python
# Train with labels for class separation
reducer = umap.UMAP(
    n_neighbors=15,
    target_weight=0.5,           # Balance data structure vs labels
    target_metric='categorical',  # Metric for labels
    random_state=42
)

embedding = reducer.fit_transform(data, y=labels)
```

### 聚类预处理

```python
# Optimized for clustering
reducer = umap.UMAP(
    n_neighbors=30,      # More global structure
    min_dist=0.0,        # Allow tight packing
    n_components=10,     # Higher dimensions for density
    metric='euclidean',
    random_state=42
)

embedding = reducer.fit_transform(data)
```

### 自定义距离度量

```python
from numba import njit

@njit()
def custom_distance(x, y):
    """Custom distance function (must be Numba-compatible)"""
    result = 0.0
    for i in range(x.shape[0]):
        result += abs(x[i] - y[i])
    return result

reducer = umap.UMAP(metric=custom_distance)
embedding = reducer.fit_transform(data)
```

### 带有自定义的参数化UMAP架构

```python
import tensorflow as tf
from umap.parametric_umap import ParametricUMAP

# Define custom encoder
encoder = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(input_dim,)),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(2)  # Output dimension
])

# Define decoder for reconstruction
decoder = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(2,)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(input_dim)
])

# Train parametric UMAP with autoencoder
embedder = ParametricUMAP(
    encoder=encoder,
    decoder=decoder,
    dims=(input_dim,),
    parametric_reconstruction=True,
    autoencoder_loss=True,
    n_training_epochs=10,
    batch_size=128,
    n_neighbors=15,
    min_dist=0.1,
    random_state=42
)

embedding = embedder.fit_transform(data)
new_embedding = embedder.transform(new_data)
reconstructed = embedder.inverse_transform(embedding)
```

### 用于密度保存的 DensMAP

```python
# Preserve local density information
reducer = umap.UMAP(
    densmap=True,           # Enable DensMAP
    dens_lambda=2.0,       # Weight of density preservation
    dens_frac=0.3,         # Fraction for density estimation
    output_dens=True,      # Output density estimates
    n_neighbors=15,
    min_dist=0.1,
    random_state=42
)

embedding = reducer.fit_transform(data)

# Access density estimates
original_density = reducer.rad_orig_  # Density in original space
embedded_density = reducer.rad_emb_   # Density in embedded space
```

### 用于时间序列的对齐 UMAP

```python
from umap import AlignedUMAP

# Multiple related datasets (e.g., different time points)
datasets = [day1_data, day2_data, day3_data, day4_data]

# Align embeddings
mapper = AlignedUMAP(
    n_neighbors=15,
    alignment_regularisation=1e-2,  # Alignment strength
    alignment_window_size=2,        # Align with adjacent datasets
    n_components=2,
    random_state=42
)

mapper.fit(datasets)

# Access aligned embeddings
aligned_embeddings = mapper.embeddings_
# aligned_embeddings[0] is day1 embedding
# aligned_embeddings[1] is day2 embedding, etc.
```
