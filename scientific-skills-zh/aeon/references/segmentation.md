# 时间序列分割

Aeon 提供了将时间序列分割成具有不同特征的区域的算法，识别变化点和边界。

## 分割算法

### 二进制分割
- `BinSegmenter` - 递归二进制分割
  - 在最显着变化处迭代分割序列点
  - 参数：`n_segments`、`cost_function`
  - **使用时间**：已知段数，分层结构

### Classification-Based
- `ClaSPSegmenter` - 分类分数配置文件
  - 使用分类性能来识别边界
  - 发现分类区分邻居的分段
  - **使用时**：分段具有不同的时间模式

### 基于快速模式
- `FLUSSSegmenter` - 快速低成本单能语义分段
  - 使用弧交叉的高效语义分段
  - 基于矩阵profile
  - **使用时间**：大型时间序列，需要速度和模式发现

### 信息论
- `InformationGainSegmenter` - 信息增益最大化
  - 查找最大化信息增益的边界
  - **使用时间**：段之间的统计差异

### 高斯建模
- `GreedyGaussianSegmenter` - 贪婪高斯近似
  - 将分段建模为高斯分布
  - 增量添加变化点
  - **使用时间**：分段遵循高斯分布

### 分层聚合
- `EAggloSegmenter` - 自下而上的合并方法
  - 通过聚合估计变化点
  - **何时使用**：需要分层分割结构

### 隐藏马尔可夫模型
- `HMMSegmenter` - 带有维特比的HMM解码
  - 基于概率状态的分割
  - **使用时**：分段表示隐藏状态

### Dimensionality-Based
- `HidalgoSegmenter` - 异构内在维度算法
  - 检测局部维度的变化
  - **使用时**：分段之间的维度变化

### Baseline
- `RandomSegmenter` - 随机变化点Generation
  - **使用时**：需要零假设基线

## 快速入门

```python
from aeon.segmentation import ClaSPSegmenter
import numpy as np

# Create time series with regime changes
y = np.concatenate([
    np.sin(np.linspace(0, 10, 100)),      # Segment 1
    np.cos(np.linspace(0, 10, 100)),      # Segment 2
    np.sin(2 * np.linspace(0, 10, 100))   # Segment 3
])

# Segment the series
segmenter = ClaSPSegmenter()
change_points = segmenter.fit_predict(y)

print(f"Detected change points: {change_points}")
```

## 输出格式

分段器返回变化点索引：

```python
# change_points = [100, 200]  # Boundaries between segments
# This divides series into: [0:100], [100:200], [200:end]
```

## 算法选择

- **速度优先**：FLUSSSegmenter、BinSegmenter
- **精度优先**：ClaSPSegmenter、HMMSegmenter
- **已知段计数**：带 n_segments 参数的 BinSegmenter
- **未知段计数**：ClaSPSegmenter、 InformationGainSegmenter
- **模式变化**：FLUSSSegmenter、ClaSPSegmenter
- **统计变化**：InformationGainSegmenter、GreedyGaussianSegmenter
- **状态转换**：HMMSegmenter

## 常用案例

### 状态变化检测
识别时间序列行为何时发生根本性变化：

```python
from aeon.segmentation import InformationGainSegmenter

segmenter = InformationGainSegmenter(k=3)  # Up to 3 change points
change_points = segmenter.fit_predict(stock_prices)
```

### 活动分段
将传感器数据分段为活动：

```python
from aeon.segmentation import ClaSPSegmenter

segmenter = ClaSPSegmenter()
boundaries = segmenter.fit_predict(accelerometer_data)
```

### 季节边界检测
查找时间序列中的季节过渡：

```python
from aeon.segmentation import HMMSegmenter

segmenter = HMMSegmenter(n_states=4)  # 4 seasons
segments = segmenter.fit_predict(temperature_data)
```

## 评估指标

使用分割质量指标：

```python
from aeon.benchmarking.metrics.segmentation import (
    count_error,
    hausdorff_error
)

# Count error: difference in number of change points
count_err = count_error(y_true, y_pred)

# Hausdorff: maximum distance between predicted and true points
hausdorff_err = hausdorff_error(y_true, y_pred)
```

## 最佳实践

1. **标准化数据**：确保变化检测不受scale
2支配。 **选择适当的指标**：不同的算法优化不同的标准
3. **验证段**：可视化以验证有意义的边界
4. **处理噪声**：在分割之前考虑平滑
5. **领域知识**：如果已知
6，则使用预期的段计数。 **参数调整**：调整灵敏度参数（阈值、惩罚）

## 可视化

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 4))
plt.plot(y, label='Time Series')
for cp in change_points:
    plt.axvline(cp, color='r', linestyle='--', label='Change Point')
plt.legend()
plt.show()
```
