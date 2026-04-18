# 时间序列分类

Aeon 提供 13 类时间序列分类器，具有 scikit-learn 兼容 API。

## 基于卷积的分类器

应用随机卷积变换以实现高效的特征提取：

- `Arsenal` - ROCKET 分类器的集成，具有不同的分类器kernels
- `HydraClassifier` - 带膨胀的多分辨率卷积
- `RocketClassifier` - 带岭回归的随机卷积核
- `MiniRocketClassifier` - 速度的简化 ROCKET 变体
- `MultiRocketClassifier` - 组合多个 ROCKET变种

* *使用时机**：需要在不同数据集上具有强大性能的快速、可扩展分类。

## 深度学习分类器

针对时间序列优化的神经网络架构：

- `FCNClassifier` - 全卷积网络
- `ResNetClassifier` - 具有跳跃连接的残差网络
- `InceptionTimeClassifier` - 多尺度初始模块
- `TimeCNNClassifier` - 时间序列的标准CNN
- `MLPClassifier` - 多层感知器基线
- `EncoderClassifier` - 通用编码器包装器
- `DisjointCNNClassifier` - 以Shapelet为中心建筑

* *使用时机**：可用的大型数据集、需要端到端学习或复杂的时间模式。

## 基于字典的分类器

将时间序列转换为符号表示：

- `BOSSEnsemble` - 带集成投票的 Bag-of-SFA-Symbols
- `TemporalDictionaryEnsemble` - 多种字典方法组合
- `WEASEL` - 用于时间序列分类的Word ExtrAction
- `MrSEQLClassifier` - 多个符号序列学习

* *何时使用**：需要可解释模型、稀疏模式或符号推理。

## 基于距离的分类器

利用专门的时间序列距离指标：

- `KNeighborsTimeSeriesClassifier` - 具有时间距离的 k-NN（DTW、LCSS、ERP 等）
- `ElasticEnsemble` - 组合多个弹性距离测量
- `ProximityForest` - 使用基于距离的分割的树集成

* *使用时**：小型数据集，需要基于相似性的分类或可解释Decisions.

## 基于特征的分类器

在分类前提取统计和签名特征：

- `Catch22Classifier` - 22 个规范时间序列特征
- `TSFreshClassifier` - 通过 tsfresh 自动特征提取
- `SignatureClassifier` - 路径签名转换
- `SummaryClassifier` - 摘要统计提取
- `FreshPRINCEClassifier` - 组合多个特征提取器

* *何时使用**：需要可解释的特征、可用的领域专业知识或特征工程方法。

## 基于间隔的分类器

从随机或监督间隔中提取特征：

- `CanonicalIntervalForestClassifier` - 具有决策树的随机区间特征
- `DrCIFClassifier` - 具有catch22特征的多样化表示CIF
- `TimeSeriesForestClassifier` - 具有汇总统计的随机区间
- `RandomIntervalClassifier` - 基于简单区间的方法
- `RandomIntervalSpectralEnsembleClassifier` - 间隔的光谱特征
- `SupervisedTimeSeriesForest` - 监督间隔选择

  * *使用时间**：判别模式出现在特定时间窗口中。

## 基于Shapelet的分类器

识别判别子序列（shapelet）：

- `ShapeletTransformClassifier` - 发现并使用有判别性 shapelet
- `LearningShapeletClassifier` - 通过梯度下降学习 shapelet
- `SASTClassifier` - 可扩展近似 shapelet 变换
- `RDSTClassifier` - 随机扩张 shapelet 变换

* *使用时**：需要可解释的判别模式或相不变特征。

## 混合分类器

组合多种分类范式：

- `HIVECOTEV1` - 基于变换的集成的分层投票集体（版本1）
- `HIVECOTEV2` - 更新后的增强版本组件

* *使用时间**：需要最大精度，可用计算资源。

## 早期分类

在观察整个时间序列之前进行预测：

- `TEASER` - 两层早期准确序列分类器
- `ProbabilityThresholdEarlyClassifier` - 置信度超过阈值时预测

* *使用时间**：实时决策

## 序数分类

处理有序类标签：

- `OrdinalTDE` - 序数输出的时态字典集合

* *使用时间**：类具有自然排序（例如，严重性级别）。

## 组合工具

构建自定义管道和集成：

- `ClassifierPipeline` - 带有分类器的 transformers 链 
- `WeightedEnsembleClassifier` - 分类器的加权组合
- `SklearnClassifierWrapper` - 针对时间序列调整 sklearn 分类器

## 快速Start

```python
from aeon.classification.convolution_based import RocketClassifier
from aeon.datasets import load_classification

# Load data
X_train, y_train = load_classification("GunPoint", split="train")
X_test, y_test = load_classification("GunPoint", split="test")

# Train and predict
clf = RocketClassifier()
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
```

## 算法选择

- **速度优先**：MiniRocketClassifier、Arsenal
- **精度优先**：HIVECOTEV2、InceptionTimeClassifier
- **可解释性**：ShapeletTransformClassifier、Catch22Classifier
- **小数据**：KNeighborsTimeSeriesClassifier，基于距离的方法
- **大数据**：深度学习分类器，ROCKET变体
