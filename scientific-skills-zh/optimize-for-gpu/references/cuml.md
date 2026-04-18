# cuML Reference

cuML 是 RAPIDS 生态系统中 NVIDIA GPU 加速的机器学习库。它为 50 多种算法提供与 scikit-learn 兼容的 API，平均性能提高 10-50 倍，其中一些算法（HDBSCAN、t-SNE、UMAP、KNN）可实现 60-600 倍的加速。它遵循 sklearn 中熟悉的拟合/预测/变换模式。

> **完整文档：** https://docs.rapids.ai/api/cuml/stable/

## 目录

1. [安装和设置](#installation-and-setup)
2. [两种使用模式](#two-usage-modes)
3. [cuml.accel加速器模式](#cumlaccel-accelerator-mode)
4. [直接 cuML API](#direct-cuml-api)
5. [算法目录](#algorithm-catalog)
6. [输入/输出类型处理](#inputoutput-type-handling)
7. [预处理](#preprocessing)
8. [特征提取](#feature-extraction)
9. [模型选择和调整](#model-selection-and-tuning)
10. [森林推理库（FIL）](#forest-inference-library)
11. [带有 Dask 的多 GPU](#multi-gpu-with-dask)
12. [模型序列化](#model-serialization)
13. [内存管理](#内存管理)
14. [性能优化](#性能优化)
15. [互操作性](#互操作性)
16. [与 sklearn 的主要区别](#key-differences-from-sklearn)
17. [常见迁移模式](#common-migration-patterns)

- --

## 安装和设置

在所有安装说明、文档字符串、注释和错误中始终使用 `uv add`（切勿使用 `pip install` 或 `conda install`） messages.

```bash
uv add --extra-index-url=https://pypi.nvidia.com cuml-cu12    # For CUDA 12.x
```

* *平台：**仅限 Linux 和 WSL2（无本机 macOS 或 Windows）。
* *要求：** scikit-learn >= 1.4，具有 CUDA 12.x 的 NVIDIA GPU支持.

验证：
```python
import cuml
print(cuml.__version__)

from cuml.datasets import make_blobs
X, y = make_blobs(n_samples=1000, n_features=10)
print(f"Generated {X.shape[0]} samples on GPU")
```

- --

## 两种使用模式

### 1. cuml.accel（零代码更改）
透明地拦截 sklearn、umap-learn 和 hdbscan 调用并将它们路由到 GPU。对于不支持的操作，回退到 CPU。最适合：快速加速现有 sklearn 代码、混合代码库、原型设计。

### 2. 直接 cuML API
将 `from sklearn` 替换为 `from cuml`。最大性能，对 GPU 执行的显式控制。最适合：生产管道、最高性能、新的 GPU 优先代码。

- --

## cuml.accel 加速器模式

从 sklearn 到 GPU 的最快路径 - 无需更改代码。类似于 Pandas 的 `cudf.pandas`。

### 激活

```python
# Jupyter/IPython (MUST be the first cell, before any sklearn import)
%load_ext cuml.accel

import sklearn  # Now GPU-accelerated
from sklearn.cluster import KMeans  # Runs on GPU transparently
```

```bash
# Command line
python -m cuml.accel script.py
python -m cuml.accel -v script.py     # With info logging
python -m cuml.accel -vv script.py    # With debug logging
```

```python
# Programmatic (call BEFORE importing sklearn)
import cuml
cuml.accel.install()

from sklearn.cluster import KMeans  # Now GPU-accelerated
```

```bash
# Environment variable
CUML_ACCEL_ENABLED=1 python script.py
```

### 如何操作Works

- 拦截 sklearn/umap-learn/hdbscan 导入并用 GPU 版本替换估计器。
- 如果 GPU 不支持某个操作，它会默默地回退到 CPU sklearn。
- 默认使用托管内存 — 主机 RAM 增强 GPU VRAM。
- 在下腌制的模型cuml.accel 在非 GPU 环境中作为标准 sklearn 对象加载。
- 跨 sklearn、umap-learn 和 hdbscan 加速 30 多种算法。
- 与 scikit-learn 版本 1.4-1.7 兼容。

### 已知回退触发器（在 CPU 上运行）相反）

- 稀疏输入数据（大多数算法）
- 可调用参数（例如，用于 KMeans 的可调用 `init`）
- 某些参数值：用于 PCA 的 `n_components="mle"`、用于线性模型的 `positive=True`、热启动
- 不支持的邻居距离度量算法
- 随机森林的多输出目标
- 字符串/对象数据类型-必须首先使用LabelEncoder进行预编码

### 数值精度

GPU结果在数值上是等效的，但由于并行降序，浮点精度级别可能有所不同。通过分数（准确度、R2 等）而不是原始系数值来比较模型质量。

- --

## 直接 cuML API

将 sklearn 导入替换为 cuml 导入。 API 是相同的 — fit/predict/transform。

```python
from cuml.cluster import DBSCAN
from cuml.datasets import make_blobs

# Create data directly on GPU
X, y = make_blobs(n_samples=100_000, centers=5, n_features=10, random_state=42)

# Fit — runs on GPU
model = DBSCAN(eps=1.0, min_samples=5)
model.fit(X)
print(model.labels_)
```

```python
from cuml import LinearRegression
from cuml.datasets import make_regression
from cuml.model_selection import train_test_split

X, y = make_regression(n_samples=100_000, n_features=50, noise=0.1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
score = model.score(X_test, y_test)
print(f"R2 score: {score:.4f}")
```

- --

## 算法目录

### 聚类

| CUML | sklearn 等效项 |多GPU |
|------|--------------------|------------------------|
| `cuml.KMeans` | `sklearn.cluster.KMeans` |是 |
| `cuml.DBSCAN` | `sklearn.cluster.DBSCAN` |是 |
| `cuml.AgglomerativeClustering` | `sklearn.cluster.AgglomerativeClustering` |否|
| `cuml.cluster.hdbscan.HDBSCAN` | `hdbscan.HDBSCAN` |否|
| `cuml.cluster.SpectralClustering` | `sklearn.cluster.SpectralClustering` |否 |

### 回归

| CUML | sklearn 等效项 |多GPU |
|------|--------------------|----------|
| `cuml.LinearRegression` | `sklearn.linear_model.LinearRegression` |是 |
| `cuml.Ridge` | `sklearn.linear_model.Ridge` |是 |
| `cuml.Lasso` | `sklearn.linear_model.Lasso` |是 |
| `cuml.ElasticNet` | `sklearn.linear_model.ElasticNet` |是 |
| `cuml.SVR` | `sklearn.svm.SVR` |否|
| `cuml.KernelRidge` | `sklearn.kernel_ridge.KernelRidge` |否|
| `cuml.ensemble.RandomForestRegressor` | `sklearn.ensemble.RandomForestRegressor` |是 |
| `cuml.MBSGDRegressor` | `sklearn.linear_model.SGDRegressor` |否|

### 分类

| CUML | sklearn 等效项 |多GPU |
|------|--------------------|------------------------|
| `cuml.LogisticRegression` | `sklearn.linear_model.LogisticRegression` |否|
| `cuml.ensemble.RandomForestClassifier` | `sklearn.ensemble.RandomForestClassifier` |是 |
| `cuml.svm.SVC` | `sklearn.svm.SVC` |否|
| `cuml.svm.LinearSVC` | `sklearn.svm.LinearSVC` |否|
| `cuml.naive_bayes.GaussianNB` | `sklearn.naive_bayes.GaussianNB` |否|
| `cuml.naive_bayes.MultinomialNB` | `sklearn.naive_bayes.MultinomialNB` |是 |
| `cuml.naive_bayes.BernoulliNB` | `sklearn.naive_bayes.BernoulliNB` |否|
| `cuml.naive_bayes.CategoricalNB` | `sklearn.naive_bayes.CategoricalNB` |否|
| `cuml.naive_bayes.ComplementNB` | `sklearn.naive_bayes.ComplementNB` |否|
| `cuml.neighbors.KNeighborsClassifier` | `sklearn.neighbors.KNeighborsClassifier` |是 |
| `cuml.neighbors.KNeighborsRegressor` | `sklearn.neighbors.KNeighborsRegressor` |是 |
| `cuml.MBSGDClassifier` | `sklearn.linear_model.SGDClassifier` |否|
| `cuml.multiclass.OneVsOneClassifier` | `sklearn.multiclass.OneVsOneClassifier` |否|
| `cuml.multiclass.OneVsRestClassifier` | `sklearn.multiclass.OneVsRestClassifier` |否 |

### 降维与流形学习

| CUML | sklearn/图书馆等效项 |多GPU |
|-----|----------------------------|-----------|
| `cuml.PCA` | `sklearn.decomposition.PCA` |是 |
| `cuml.IncrementalPCA` | `sklearn.decomposition.IncrementalPCA` |否|
| `cuml.TruncatedSVD` | `sklearn.decomposition.TruncatedSVD` |是 |
| `cuml.UMAP` | `umap.UMAP` |是（推论）|
| `cuml.TSNE` | `sklearn.manifold.TSNE` |否|
| `cuml.random_projection.GaussianRandomProjection` | `sklearn.random_projection.GaussianRandomProjection` |否|
| `cuml.random_projection.SparseRandomProjection` | `sklearn.random_projection.SparseRandomProjection` |否 |

### 最近邻居

| CUML | sklearn 等效项 |多GPU |
|------|--------------------|---------|
| `cuml.neighbors.NearestNeighbors` | `sklearn.neighbors.NearestNeighbors` |是 |
| `cuml.neighbors.KNeighborsClassifier` | `sklearn.neighbors.KNeighborsClassifier` |是 |
| `cuml.neighbors.KNeighborsRegressor` | `sklearn.neighbors.KNeighborsRegressor` |是 |
| `cuml.neighbors.KernelDensity` | `sklearn.neighbors.KernelDensity` |否 |

### 时间序列

| CUML |描述 |
|------|--------------|
| `cuml.ExponentialSmoothing` | Holt-Winters 指数平滑 |
| `cuml.tsa.ARIMA` | ARIMA/SARIMA 模型（批量 - 同时适合多个系列）|
| `cuml.tsa.auto_arima.AutoARIMA` |自动 ARIMA 订单选择 |

### 指标（GPU 加速）

* *回归：** `r2_score`、`mean_squared_error`、`mean_absolute_error`、`mean_squared_log_error`、`median_absolute_error`

* *分类：** `accuracy_score`、`log_loss`、`roc_auc_score`、`precision_recall_curve`、`confusion_matrix`

* *聚类：** `adjusted_rand_score`、`silhouette_score`、`silhouette_samples`、`homogeneity_score`、 `completeness_score`、`v_measure_score`、`mutual_info_score`

* *其他：** `trustworthiness`、`pairwise_distances`、`pairwise_kernels`

### 型号解释

| CUML |描述 |
|------|--------------|
| `cuml.explainer.KernelExplainer` | SHAP 内核解释器 |
| `cuml.explainer.PermutationExplainer` | SHAP 排列解释器 |
| `cuml.explainer.TreeExplainer` | SHAP 树解释器 |

- --

## 输入/输出类型处理

### 支持的输入类型

cuML 接受：NumPy 数组、CuPy 数组、cuDF DataFrames/Series、pandas DataFrames/Series、Numba 设备数组、PyTorch 张量（通过`__cuda_array_interface__`).

NumPy 和 pandas 输入会自动传输到 GPU。为了获得最佳性能，请传递 CuPy 数组或 cuDF DataFrame 以避免传输。

### 控制输出类型

```python
import cuml

# Global setting
cuml.set_global_output_type('cupy')  # Options: 'input', 'cupy', 'numpy', 'cudf', 'pandas'

# Context manager
with cuml.using_output_type('cudf'):
    result = model.predict(X)  # Returns cudf Series

# Per-estimator
model = cuml.KMeans(output_type='cupy')
```

* *性能排名**（最快到最慢的输出类型）：
1. `cupy` — 无主机传输，最高效
2. `cudf` — 某些形状的轻微开销
3. `numpy` / `pandas` — 设备到主机的传输成本

* *最佳实践：** 使用 `cupy` 或 `cudf` 获取中间结果。仅在最后转换为 `numpy`/`pandas` 以进行可视化或导出。

- --

## 预处理

cuML 提供所有常见 sklearn 预处理器的 GPU 加速版本。

### 缩放器和变压器

```python
from cuml.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from cuml.preprocessing import Normalizer, PowerTransformer, QuantileTransformer
from cuml.preprocessing import Binarizer, PolynomialFeatures, KBinsDiscretizer

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

### 编码器

```python
from cuml.preprocessing import LabelEncoder, OneHotEncoder, LabelBinarizer, TargetEncoder

le = LabelEncoder()
y_encoded = le.fit_transform(y)

ohe = OneHotEncoder(sparse_output=False)
X_encoded = ohe.fit_transform(X_categorical)
```

### 输入器

```python
from cuml.preprocessing import SimpleImputer, MissingIndicator

imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)
```

### 管道和组成

```python
from cuml.compose import ColumnTransformer, make_column_transformer
from cuml.preprocessing import StandardScaler, OneHotEncoder

preprocessor = make_column_transformer(
    (StandardScaler(), ['age', 'income']),
    (OneHotEncoder(), ['category', 'region']),
)
X_processed = preprocessor.fit_transform(df)
```

### 预处理函数

`scale()`、`minmax_scale()`、`maxabs_scale()`、`robust_scale()`、`normalize()`、`binarize()`、 `add_dummy_feature()`、`label_binarize()`

- --

## 特征提取

```python
from cuml.feature_extraction.text import TfidfVectorizer, CountVectorizer, HashingVectorizer

tfidf = TfidfVectorizer(max_features=10000)
X_tfidf = tfidf.fit_transform(corpus)
```

- --

## 模型选择和调优

### 训练/测试Split

```python
from cuml.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

### 交叉验证

```python
from cuml.model_selection import KFold

kf = KFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, test_idx in kf.split(X):
    X_train, X_test = X[train_idx], X[test_idx]
    # ...
```

### 超参数调整

对于GPU高效的超参数搜索，请使用dask-ml的GridSearchCV/RandomizedSearchCV而不是sklearn的 - sklearn 的版本导致每倍 CPU-GPU 数据传输过多。

```python
from dask_ml.model_selection import RandomizedSearchCV
from cuml.ensemble import RandomForestClassifier

param_distributions = {
    'max_depth': [8, 12, 16, 20],
    'n_estimators': [100, 200, 500],
    'max_features': [0.5, 0.75, 1.0],
}

search = RandomizedSearchCV(
    RandomForestClassifier(),
    param_distributions,
    n_iter=25,
    cv=5,
    random_state=42,
)
search.fit(X_train, y_train)
print(f"Best score: {search.best_score_:.4f}")
print(f"Best params: {search.best_params_}")
```

### 数据集生成器

```python
from cuml.datasets import make_blobs, make_classification, make_regression

X, y = make_blobs(n_samples=100_000, centers=5, n_features=20, random_state=42)
X, y = make_classification(n_samples=100_000, n_features=50, n_informative=25)
X, y = make_regression(n_samples=100_000, n_features=50, noise=0.1)
```

- --

## 森林推理库

FIL 提供高性能 GPU 推理在任何框架中训练的基于树的模型 - 比 sklearn 推理快 80 倍以上。

```python
from cuml.fil import ForestInference

# Load from XGBoost, LightGBM, or sklearn saved models
fil_model = ForestInference.load("xgboost_model.ubj", is_classifier=True)

# Optional: optimize for specific batch size
fil_model.optimize()

# Predict (80x+ faster than sklearn)
predictions = fil_model.predict(X_test)
probas = fil_model.predict_proba(X_test)
```

* *支持：** XGBoost、LightGBM、sklearn 随机森林、任何 Treelite 兼容模型。

 当您的模型已经在 CPU 上训练并且希望在不使用 CPU 的情况下加速推理时，这尤其有价值再训练.

- --

## 带 Dask 的多 GPU

对于单个 GPU 来说太大的数据集或当您想要使用多个 GPU 时。

```python
from dask.distributed import Client
from dask_cuda import LocalCUDACluster

# One Dask worker per GPU
cluster = LocalCUDACluster(
    rmm_pool_size="12GB",
    enable_cudf_spill=True,
)
client = Client(cluster)

# Create distributed data
from cuml.dask.datasets import make_blobs
X, y = make_blobs(
    n_samples=1_000_000,
    n_features=20,
    centers=5,
    n_parts=len(client.scheduler_info()['workers']) * 2,  # 2 partitions per worker
)

# Use Dask estimator
from cuml.dask.cluster import KMeans
kmeans = KMeans(n_clusters=5)
kmeans.fit(X)
labels = kmeans.predict(X)

# Convert to single-GPU model for serialization
single_model = kmeans.get_combined_model()

client.close()
cluster.close()
```

### 可用的多 GPU 估计器 (`cuml.dask`)

- **聚类：** KMeans， DBSCAN
- **线性模型：** LinearRegression、Ridge、Lasso、ElasticNet
- **集成：** RandomForestClassifier、RandomForestRegressor
- **分解：** PCA、TruncatedSVD
- **流形：** UMAP（仅限推理）
- **邻居：** 最近邻居、KNeighborsClassifier、KNeighborsRegressor
- **朴素贝叶斯：** 多项式NB
- **预处理：** LabelEncoder、LabelBinarizer、OneHotEncoder

- --

## 模型序列化

```python
import pickle

# Save cuML model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f, protocol=5)

# Load cuML model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
```

- 在cuml.accel下训练的模型可以在非GPU环境中作为标准sklearn对象进行pickle和加载。
- Dask分布式模型必须首先转换：`single_model = dask_model.get_combined_model()`.
- joblib也适用于序列化。

- --

## 内存管理

### RMM（RAPIDS内存管理器）

```python
import rmm

# Pre-allocate a memory pool for faster allocation
rmm.reinitialize(pool_allocator=True, initial_pool_size=2**32)  # 4 GB pool
```

### 与cuDF和CuPy对齐

当将cuML与cuDF和CuPy一起使用时，将所有库对齐在同一个RMM上分配器：

```python
import rmm
from rmm.allocators.cupy import rmm_cupy_allocator
import cupy
cupy.cuda.set_allocator(rmm_cupy_allocator)
```

### cuml.accel Memory

cuml.accel 默认使用托管内存（主机 RAM 增强 GPU VRAM）。如果遇到速度减慢的情况，请使用 `--disable-uvm` 标志禁用。托管内存在 WSL2 上或外部配置 RMM 时不起作用。

### 最佳实践

- 在精度允许的情况下使用 float32 而不是 float64 — 内存减半，吞吐量加倍。
- 在整个管道中将数据保留在 GPU 上 — 避免 NumPy/pandas 往返。
- 对于大于 GPU 内存的数据集：使用Dask 多 GPU 或块处理。
- 预分配 RMM 池以避免碎片。

- --

## 性能优化

### 算法的预期加速

|类别 |典型加速比|备注|
|----------|----------------|------|
| HDBSCAN、t-SNE、UMAP | 60-300x |复杂算法受益最多|
| KNN |高达 600 倍 |随着数据大小 |
| 大幅扩展KMeans、随机森林 | 15-80 倍 | RF：20-45x 单 GPU |
| FIL 推理 | 80x+ |从任何框架进行树模型推理|
|线性模型、PCA、岭 | 2-10 倍 |更简单的算法，更低但一致的增益 |

### 关键优化技巧

1. **使用 float32。** GPU float32 吞吐量比 float64 高 2-32 倍。大多数机器学习算法不需要双精度。

2. **将数据保存在 GPU 上。** 传递 CuPy 数组或 cuDF DataFrame。每个 NumPy/pandas 转换都会触发设备-主机传输。

3. **更大的数据集 = 更大的加速。** GPU 并行优势随着数据大小的增加而增长。至少约 10K 行才能看到好处。

4. **宽数据优势更多。** 128-512 个特征比 8-16 个特征获得更高的加速。

5. **第一次调用有 JIT 开销。** 后续调用的基准，而不是第一次。

6. **使用 RMM 池。** 预分配的内存池比原始 cudaMalloc.

7 快 1000 倍。 **使用 dask-ml 进行超参数调整，**而不是 sklearn 的 GridSearchCV — 它避免了过多的 CPU-GPU 传输。

8. **使用 FIL 进行树模型推理。** 即使模型是在 CPU（XGBoost、LightGBM、sklearn RF）上训练的，FIL 也能提供 80 倍以上的推理加速。

- --

## 互操作性

- **cuDF：** 零拷贝输入。 cuDF DataFrames 被所有估计器直接接受。
- **CuPy:** 通过 `__cuda_array_interface__` 进行零拷贝。最有效的中间格式。
- **NumPy/pandas：** 接受作为输入（自动传输到 GPU）。输出类型可配置。
- **PyTorch：** 通过数组接口接受的张量。
- **sklearn：** API 兼容。型号可互换。 cuml.accel 用于透明加速。
- **XGBoost/LightGBM:** FIL 为外部训练的树模型提供 GPU 推理。
- **Dask:** 通过 `cuml.dask` 模块提供本机分布式支持。

### 端到端 RAPIDS管道

```python
import cudf
import cuml
from cuml.preprocessing import StandardScaler
from cuml.ensemble import RandomForestClassifier
from cuml.model_selection import train_test_split

# Load data on GPU
df = cudf.read_parquet("data.parquet")
X = df.drop("target", axis=1)
y = df["target"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Preprocess
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train
model = RandomForestClassifier(n_estimators=100, max_depth=16)
model.fit(X_train, y_train)

# Evaluate
score = model.score(X_test, y_test)
print(f"Accuracy: {score:.4f}")
```

所有这些都完全在GPU上运行——从Parquet读取到模型评估——CPU-GPU传输为零。

- --

## 与sklearn

1的主要区别。 **平台：** 仅 Linux 和 WSL2。没有本机 macOS 或 Windows。

2. **稀疏数据：** 大多数 cuML 算法不支持稀疏矩阵。在 cuml.accel 下，稀疏输入回落到 CPU.

3. **字符串数据：** 必须预先编码为数字。 estimators.

4 中没有本机字符串列支持。 **多输出：** 随机森林不支持。

5. **热启动：** 大多数算法不支持。

6. **忽略一些 sklearn 参数：** `n_jobs`（GPU 处理并行性）、`positive=True`、特定求解器选择。

7. **数值精度：** 结果质量相同，但在浮点级别可能有所不同。比较分数，而不是原始系数。

8. **内存：** 受 GPU VRAM 限制（通常为 8-80 GB）。对于较大的数据集，请使用托管内存或 Dask。

9. **缺少拟合属性：** 一些 sklearn 属性未在 cuml.accel 下计算（例如 HDBSCAN `exemplars_`、LinearRegression `rank_`）。

- --

## 常见迁移模式

### 模式 1：零努力(cuml.accel)

```python
# Add one line at top of notebook:
%load_ext cuml.accel

from sklearn.cluster import KMeans  # Now GPU-accelerated
from sklearn.decomposition import PCA  # Now GPU-accelerated
# Everything else stays exactly the same
```

### 模式 2：直接导入交换

```python
# Before
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# After
from cuml.ensemble import RandomForestClassifier
from cuml.preprocessing import StandardScaler
from cuml.model_selection import train_test_split
```

### 模式 3：完整 RAPIDS 管道 (cuDF + cuML)

```python
import cudf
from cuml.preprocessing import StandardScaler, LabelEncoder
from cuml.ensemble import RandomForestClassifier
from cuml.model_selection import train_test_split

# Load and preprocess entirely on GPU
df = cudf.read_parquet("data.parquet")
le = LabelEncoder()
df["category_encoded"] = le.fit_transform(df["category"])

X = df[["feature1", "feature2", "category_encoded"]].to_cupy()
y = df["target"].to_cupy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=200, max_depth=16)
model.fit(X_train, y_train)
print(f"Accuracy: {model.score(X_test, y_test):.4f}")
```

### 模式 4：CPU 训练模型的 GPU 推理

```python
from cuml.fil import ForestInference

# Load XGBoost/LightGBM/sklearn model for 80x+ faster inference
fil_model = ForestInference.load("my_xgboost_model.ubj", is_classifier=True)
predictions = fil_model.predict(X_test)
```
