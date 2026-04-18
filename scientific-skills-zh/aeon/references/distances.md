# 距离度量

Aeon 提供专门的距离函数来测量时间序列之间的相似性，与 aeon 和 scikit-learn 估计器兼容。

## 距离类别

### 弹性距离

允许序列之间灵活的时间对齐：

* *动态时间扭曲系列：**
- `dtw` - 经典动态时间扭曲
- `ddtw` - 导数 DTW（比较导数）
- `wdtw` - 加权 DTW（按位置惩罚扭曲）
- `wddtw` - 加权导数DTW
- `shape_dtw` - 基于形状 DTW

* *基于编辑：**
- `erp` - 带真实惩罚的编辑距离
- `edr` - 真实序列上的编辑距离
- `lcss` - 最长公共距离子序列
- `twe` - 时间扭曲编辑距离

* *专业化：**
- `msm` - 移动-分割-合并距离
- `adtw` - Amerced DTW
- `sbd` - 基于形状的距离

* *使用时间**：时间序列可能存在时间偏移、速度变化或相位差。

### 锁步距离

逐点比较时间序列而不对齐：

- `euclidean` - 欧几里德距离（L2 范数）
- `manhattan` - 曼哈顿距离（L1）范数）
- `minkowski` - 广义明可夫斯基距离（Lp 范数）
- `squared` - 欧几里德距离平方

* *使用时**：系列已对齐，需要计算速度，或不需要时间扭曲。

## 使用模式

### 计算单距离

```python
from aeon.distances import dtw_distance

# Distance between two time series
distance = dtw_distance(x, y)

# With window constraint (Sakoe-Chiba band)
distance = dtw_distance(x, y, window=0.1)
```

### 成对距离矩阵

```python
from aeon.distances import dtw_pairwise_distance

# All pairwise distances in collection
X = [series1, series2, series3, series4]
distance_matrix = dtw_pairwise_distance(X)

# Cross-collection distances
distance_matrix = dtw_pairwise_distance(X_train, X_test)
```

### 成本矩阵和对齐路径

```python
from aeon.distances import dtw_cost_matrix, dtw_alignment_path

# Get full cost matrix
cost_matrix = dtw_cost_matrix(x, y)

# Get optimal alignment path
path = dtw_alignment_path(x, y)
# Returns indices: [(0,0), (1,1), (2,1), (2,2), ...]
```

### 与估计器

```python
from aeon.classification.distance_based import KNeighborsTimeSeriesClassifier

# Use DTW distance in classifier
clf = KNeighborsTimeSeriesClassifier(
    n_neighbors=5,
    distance="dtw",
    distance_params={"window": 0.2}
)
clf.fit(X_train, y_train)
```

## 距离参数

### 窗口约束

限制扭曲路径偏差（提高速度并防止病理扭曲）：

```python
# Sakoe-Chiba band: window as fraction of series length
dtw_distance(x, y, window=0.1)  # Allow 10% deviation

# Itakura parallelogram: slopes constrain path
dtw_distance(x, y, itakura_max_slope=2.0)
```

### Normalization

控制距离计算之前是否对序列进行z归一化：

```python
# Most elastic distances support normalization
distance = dtw_distance(x, y, normalize=True)
```

### 距离特定参数

```python
# ERP: penalty for gaps
distance = erp_distance(x, y, g=0.5)

# TWE: stiffness and penalty parameters
distance = twe_distance(x, y, nu=0.001, lmbda=1.0)

# LCSS: epsilon threshold for matching
distance = lcss_distance(x, y, epsilon=0.5)
```

## 算法选择

### 按用例：

* *时间错位**：DTW、DDTW、WDTW
* *速度变化**：带窗口的 DTW约束
* *形状相似性**：形状DTW、SBD
* *编辑操作**：ERP、EDR、LCSS
* *导数匹配**：DDTW
* *计算速度**：欧几里德、曼哈顿
* *异常鲁棒性**：曼哈顿、LCSS

### 计算成本：

* *最快**：欧几里德 (O(n))
* *快**：约束 DTW（O(nw)，其中 w 是窗口）
* *中**：完整 DTW (O(n²))
* *慢**：复杂弹性距离（ERP、TWE、 MSM)

## 快速参考表

|距离 |对齐|速度|稳健性|可解释性 |
|---------|------------|--------|------------|--------------------|
|欧几里得|锁步|非常快|低|高|
|大田 |弹性|中等|中等|中|
| DDTW |弹性|中等|高|中|
| WDTW |弹性|中等|中等|中|
|企业资源规划|基于编辑 |慢|高|低|
| LCSS |基于编辑 |慢|非常高 |低|
|形状 DTW |弹性|中等|中等|高|

## 最佳实践

### 1.归一化

大多数距离对比例敏感；适当时标准化：

```python
from aeon.transformations.collection import Normalizer

normalizer = Normalizer()
X_normalized = normalizer.fit_transform(X)
```

### 2. 窗口约束

对于 DTW 变体，使用窗口约束以提高速度和更好的泛化：

```python
# Start with 10-20% window
distance = dtw_distance(x, y, window=0.1)
```

### 3. 系列长度

- 等长必需：大多数锁步距离
- 支持不等长：弹性距离（DTW、ERP等）

### 4.多元系列

大多数距离支持多元时间序列：

```python
# x.shape = (n_channels, n_timepoints)
distance = dtw_distance(x_multivariate, y_multivariate)
```

### 5.性能优化

- 使用numba编译的实现（aeon中默认）
- 如果不需要对齐，请考虑锁步距离
- 使用窗口化DTW而不是完整的DTW
- 预先计算距离矩阵以供重复使用

### 6. 选择正确的距离

```python
# Quick decision tree:
if series_aligned:
    use_distance = "euclidean"
elif need_speed:
    use_distance = "dtw"  # with window constraint
elif temporal_shifts_expected:
    use_distance = "dtw" or "shape_dtw"
elif outliers_present:
    use_distance = "lcss" or "manhattan"
elif derivatives_matter:
    use_distance = "ddtw" or "wddtw"
```

## 与 scikit-learn 集成

Aeon 距离与 sklearn 配合使用估计器：

```python
from sklearn.neighbors import KNeighborsClassifier
from aeon.distances import dtw_pairwise_distance

# Precompute distance matrix
X_train_distances = dtw_pairwise_distance(X_train)

# Use with sklearn
clf = KNeighborsClassifier(metric='precomputed')
clf.fit(X_train_distances, y_train)
```

## 可用距离函数

获取所有可用距离的列表：

```python
from aeon.distances import get_distance_function_names

print(get_distance_function_names())
# ['dtw', 'ddtw', 'wdtw', 'euclidean', 'erp', 'edr', ...]
```

检索特定距离函数：

```python
from aeon.distances import get_distance_function

distance_func = get_distance_function("dtw")
result = distance_func(x, y, window=0.1)
```
