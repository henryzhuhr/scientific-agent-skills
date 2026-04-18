# 异常检测

Aeon 提供异常检测方法，用于在序列和集合级别识别时间序列中的异常模式。

## 集合异常检测器

检测集合中的异常时间序列：

- `ClassificationAdapter` - 调整分类器进行异常检测
  - 训练正常数据，标记异常值预测期间
  - **使用时间**：已标记正常数据，需要基于分类的方法

- `OutlierDetectionAdapter` - 包装sklearn异常检测器
  - 与IsolationForest、LOF、OneClassSVM一起使用
  - **使用时间**：想要使用sklearn异常检测器收藏

## 系列异常检测器

检测单个时间序列内的异常点或子序列。

### 基于距离的方法

使用相似性度量来识别异常：

- `CBLOF` - 基于聚类的局部异常值因子
  - 对数据进行聚类，基于聚类识别异常值属性
  - **使用时间**：异常形成稀疏聚类

- `KMeansAD` - 基于K均值的异常检测
  - 到最近聚类中心的距离指示异常
  - **使用时间**：正常模式聚类良好

- `LeftSTAMPi` - 左 STAMP 增量 
  - 用于在线异常检测的矩阵配置文件
  - **使用时**：流数据，需要在线检测

- `STOMP` - 可扩展时间序列有序搜索矩阵配置文件
  - 计算子序列异常的矩阵配置文件
  - **使用when**：不一致发现，主题检测

- `MERLIN` - 基于矩阵轮廓的方法
  - 高效矩阵轮廓计算
  - **使用何时**：大时间序列，需要可扩展性

- `LOF` - 适用于时间序列的局部异常值因子
  - 基于密度的异常值检测
  - **使用时间**：低密度区域中的异常

- `ROCKAD` - 基于ROCKET的半监督检测
  - 使用ROCKET特征进行异常识别
  - **使用时间**：有一些标记数据，需要基于特征的方法

### 基于分布的方法

分析统计分布：

- `COPOD` - 基于 Copula 的异常值检测
  - 模型边际和联合分布
  - **使用时间**：多维时间序列，复杂依赖项

- `DWT_MLEAD` - 离散小波变换多级异常检测
  - 将序列分解为频段
  - **使用时间**：特定频率处的异常

### 基于隔离的方法

使用隔离原则：

- `IsolationForest` - 基于随机森林隔离
  - 异常比正常点更容易隔离
  - **使用何时**：高维数据，对分布没有假设

- `OneClassSVM` - 用于新颖性检测的支持向量机
  - 学习正常数据周围的边界
  - **使用何时**：明确定义的正常区域，需要稳健的边界

- `STRAY` - 流式稳健异常检测
  - 对数据分布变化具有鲁棒性
  - **使用时间**：流式传输数据，分布变化

### 外部库集成

- `PyODAdapter` - 将PyOD库桥接到aeon
  - Access 40+ PyOD异常检测器
  - **何时使用**：需要特定的 PyOD 算法

## 快速入门

```python
from aeon.anomaly_detection import STOMP
import numpy as np

# Create time series with anomaly
y = np.concatenate([
    np.sin(np.linspace(0, 10, 100)),
    [5.0],  # Anomaly spike
    np.sin(np.linspace(10, 20, 100))
])

# Detect anomalies
detector = STOMP(window_size=10)
anomaly_scores = detector.fit_predict(y)

# Higher scores indicate more anomalous points
threshold = np.percentile(anomaly_scores, 95)
anomalies = anomaly_scores > threshold
```

## 点与子序列异常

- **点异常**：单个异常值
  - 使用：COPOD、DWT_MLEAD、 IsolationForest

- **后续异常**（不一致）：异常模式
  - 使用：STOMP、LeftSTAMPi、MERLIN

- **集体异常**：形成异常模式的点组
  - 使用：矩阵轮廓方法，基于聚类的

## 评估指标

异常检测的专用指标：

```python
from aeon.benchmarking.metrics.anomaly_detection import (
    range_precision,
    range_recall,
    range_f_score,
    roc_auc_score
)

# Range-based metrics account for window detection
precision = range_precision(y_true, y_pred, alpha=0.5)
recall = range_recall(y_true, y_pred, alpha=0.5)
f1 = range_f_score(y_true, y_pred, alpha=0.5)
```

## 算法选择

- **速度优先**： KMeansAD、IsolationForest
- **准确性优先**：STOMP、COPOD
- **流数据**：LeftSTAMPi、STRAY
- **不一致发现**：STOMP、MERLIN
- **多维**：COPOD、PyODAdapter
- **半监督**：ROCKAD、OneClassSVM
- **无训练数据**：IsolationForest、STOMP

## 最佳实践

1. **标准化数据**：许多方法对scale
2敏感。 **选择窗口大小**：对于矩阵轮廓方法，窗口大小关键为
3. **设置阈值**：使用基于百分位数或特定于域的阈值
4. **验证结果**：可视化检测以验证意义
5. **处理季节性**：检测前去趋势/去季节化
