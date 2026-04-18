# 相似性搜索

Aeon 提供了在时间序列内和跨时间序列查找相似模式的工具，包括子序列搜索、基序发现和近似最近邻。

## 子序列最近邻 (SNN)

查找时间序列内最相似的子序列。

### MASS 算法
- `MassSNN` - Mueen 的相似性搜索算法
  - 相似性的快速归一化互相关 
  - 有效计算距离剖面
  - **使用时**：需要精确的最近邻距离，大系列

### 基于 STOMP 的 Motif Discovery
- `StompMotif` -发现重复出现的模式（基序）
  - 查找前 k 个最相似的子序列对
  - 基于矩阵轮廓计算
  - **使用时**：想要发现重复的模式

### Brute Force Baseline
- `DummySNN` - 穷举距离计算
  - 计算所有成对距离
  - **使用时**：小系列，需要精确基线

## 集合级搜索

跨集合查找相似的时间序列。

### 近似最近邻（ANN）
- `RandomProjectionIndexANN` -局部敏感散列
  - 使用具有余弦相似度的随机投影
  - 为快速近似搜索构建索引
  - **使用时机**：大型集合，速度比精确性更重要

## 快速入门：Motif Discovery

```python
from aeon.similarity_search import StompMotif
import numpy as np

# Create time series with repeated patterns
pattern = np.sin(np.linspace(0, 2*np.pi, 50))
y = np.concatenate([
    pattern + np.random.normal(0, 0.1, 50),
    np.random.normal(0, 1, 100),
    pattern + np.random.normal(0, 0.1, 50),
    np.random.normal(0, 1, 100)
])

# Find top-3 motifs
motif_finder = StompMotif(window_size=50, k=3)
motifs = motif_finder.fit_predict(y)

# motifs contains indices of motif occurrences
for i, (idx1, idx2) in enumerate(motifs):
    print(f"Motif {i+1} at positions {idx1} and {idx2}")
```

## 快速入门：子序列搜索

```python
from aeon.similarity_search import MassSNN
import numpy as np

# Time series to search within
y = np.sin(np.linspace(0, 20, 500))

# Query subsequence
query = np.sin(np.linspace(0, 2, 50))

# Find nearest subsequences
searcher = MassSNN()
distances = searcher.fit_transform(y, query)

# Find best match
best_match_idx = np.argmin(distances)
print(f"Best match at index {best_match_idx}")
```

## 快速入门：集合上的近似NN

```python
from aeon.similarity_search import RandomProjectionIndexANN
from aeon.datasets import load_classification

# Load time series collection
X_train, _ = load_classification("GunPoint", split="train")

# Build index
ann = RandomProjectionIndexANN(n_projections=8, n_bits=4)
ann.fit(X_train)

# Find approximate nearest neighbors
query = X_train[0]
neighbors, distances = ann.kneighbors(query, k=5)
```

## 矩阵配置文件

矩阵配置文件是许多相似性搜索任务的基本数据结构：

- **距离配置文件**：距离对所有子序列的查询
- **矩阵轮廓**：每个子序列到任何其他子序列的最小距离
- **主题**：具有最小距离的一对子序列
- **不和谐**：具有最大最小距离的子序列（异常）

```python
from aeon.similarity_search import StompMotif

# Compute matrix profile and find motifs/discords
mp = StompMotif(window_size=50)
mp.fit(y)

# Access matrix profile
profile = mp.matrix_profile_
profile_indices = mp.matrix_profile_index_

# Find discords (anomalies)
discord_idx = np.argmax(profile)
```

## 算法选择

- **精确子序列搜索**：MassSNN
- **Motif发现**：StompMotif
- **异常检测**：矩阵轮廓（参见anomaly_detection.md）
- **快速近似搜索**： RandomProjectionIndexANN
- **小数据**：精确结果的 DummySNN

## 用例

### 模式匹配
查找长序列中出现模式的位置：

```python
# Find heartbeat pattern in ECG data
searcher = MassSNN()
distances = searcher.fit_transform(ecg_data, heartbeat_pattern)
occurrences = np.where(distances < threshold)[0]
```

### Motif Discovery
Identify重复出现的模式：

```python
# Find repeated behavioral patterns
motif_finder = StompMotif(window_size=100, k=5)
motifs = motif_finder.fit_predict(activity_data)
```

### 时间序列检索
在数据库中查找相似的时间序列：

```python
# Build searchable index
ann = RandomProjectionIndexANN()
ann.fit(time_series_database)

# Query for similar series
neighbors = ann.kneighbors(query_series, k=10)
```

## 最佳实践

1. **窗口大小**：子序列方法的关键参数
  - 太小：捕获噪声
  - 太大：错过细粒度模式
  - 经验法则：系列长度的10-20%

2. **归一化**：大多数方法假设 z 归一化子序列
  - 处理幅度变化
  - 关注形状相似性

3. **距离度量**：针对不同需求的不同度量
  - 欧几里德：快速、基于形状的
  - DTW：处理时间扭曲
  - 余弦：尺度不变

4. **排除区域**：对于主题发现，排除琐碎的匹配
  - 通常设置为0.5-1.0 × window_size
  - 防止发现重叠的出现

5. **性能**：
  - MASS 是 O(n log n)与 O(n²)强力
  - ANN 以准确性换取速度
  - GPU 加速可用于某些方法
