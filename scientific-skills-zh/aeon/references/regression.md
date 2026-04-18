# 时间序列回归

Aeon 提供跨 9 个类别的时间序列回归器，用于从时间序列预测连续值。

## 基于卷积的回归器

应用卷积核进行特征提取：

- `HydraRegressor` - 多分辨率扩张卷积
- `RocketRegressor` - 随机卷积核
- `MiniRocketRegressor` - 简化的ROCKET以提高速度
- `MultiRocketRegressor` - 组合的ROCKET变体
- `MultiRocketHydraRegressor` - 合并ROCKET和Hydra方法

* *何时使用**：需要具有强大基线性能的快速回归。

## 深度学习回归器

用于端到端时间回归的神经架构：

- `FCNRegressor` - 全卷积网络
- `ResNetRegressor` - 具有跳跃连接的残差块
- `InceptionTimeRegressor` - 多尺度初始模块
- `TimeCNNRegressor` - 标准CNN架构
- `RecurrentRegressor` - RNN/LSTM/GRU 变体
- `MLPRegressor` - 多层感知器
- `EncoderRegressor` - 通用编码器包装器
- `LITERegressor` - 轻量级起始时间集合
- `DisjointCNNRegressor` - 专用CNN架构

* *使用时机**：大型数据集、复杂模式或需要特征学习。

## 基于距离的回归器

k-具有时间距离度量的最近邻：

- `KNeighborsTimeSeriesRegressor` - k-NN with DTW、LCSS、ERP或其他距离

* *使用时机**：小型数据集，局部相似性模式，或可解释的预测。

## 基于特征的回归器

在回归之前提取统计特征：

- `Catch22Regressor` - 22个规范时间序列特征
- `FreshPRINCERegressor` - 组合多个特征提取器的管道
- `SummaryRegressor` - 汇总统计特征
- `TSFreshRegressor` - 自动tsfresh特征提取

* *使用时**：需要

## 混合回归器

组合多种方法：

- `RISTRegressor` - 随机区间-Shapelet 变换

* *使用时机**：从组合区间和 shapelet 方法中受益。

## 基于区间的方法回归器

从时间间隔中提取特征：

- `CanonicalIntervalForestRegressor` - 带决策树的随机间隔
- `DrCIFRegressor` - 多样化表示 CIF
- `TimeSeriesForestRegressor` - 随机间隔集合
- `RandomIntervalRegressor` - 基于简单区间的方法
- `RandomIntervalSpectralEnsembleRegressor` - 谱区间特征
- `QUANTRegressor` - 基于分位数的区间特征

* *使用时间**：预测模式出现在特定时间窗口中。

## 基于 Shapelet 的回归器

使用判别子序列进行预测：

- `RDSTRegressor` - 随机扩张 Shapelet 变换

* *使用时间**：需要相不变判别模式。

## 组成工具

构建自定义回归管道：

- `RegressorPipeline` - 带有回归器的transformers链
- `RegressorEnsemble` - 具有可学习权重的加权集成
- `SklearnRegressorWrapper` - 根据时间调整sklearn回归器系列

## 实用工具

- `DummyRegressor` - 基线策略（均值、中位数）
- `BaseRegressor` - 自定义回归器的抽象基础
- `BaseDeepRegressor` - 深度学习回归器的基础

## 快速开始

```python
from aeon.regression.convolution_based import RocketRegressor
from aeon.datasets import load_regression

# Load data
X_train, y_train = load_regression("Covid3Month", split="train")
X_test, y_test = load_regression("Covid3Month", split="test")

# Train and predict
reg = RocketRegressor()
reg.fit(X_train, y_train)
predictions = reg.predict(X_test)
```

## 算法选择

- **速度优先**：MiniRocketRegressor
- **精度优先**：InceptionTimeRegressor、MultiRocketHydraRegressor
- **可解释性**：Catch22Regressor、SummaryRegressor
- **小数据**：KNeighborsTimeSeriesRegressor
- **大数据**：深度学习回归器，ROCKET 变体
- **间隔模式**：DrCIFRegressor、CanonicalIntervalForestRegressor
