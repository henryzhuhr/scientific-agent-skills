# Transformations

Aeon 提供了广泛的转换功能，用于从时间序列数据进行预处理、特征提取和表示学习。

## 转换类型

Aeon 区分：
- **CollectionTransformers**：转换多个时间序列（集合）
- **SeriesTransformers**：转换单个时间系列

## 集合变形金刚

#### 基于卷积的特征提取

使用随机内核快速、可扩展的特征生成：

- `RocketTransformer` - 随机卷积内核
- `MiniRocketTransformer` - 速度简化的ROCKET
- `MultiRocketTransformer` - 增强型 ROCKET 变体
- `HydraTransformer` - 多分辨率扩张卷积
- `MultiRocketHydraTransformer` - 组合 ROCKET 和 Hydra
- `ROCKETGPU` - GPU 加速变体

* *何时使用**：需要快速、可扩展的功能

### 统计特征提取

基于时间序列特征的领域无关特征：

- `Catch22` - 22个规范时间序列特征
- `TSFresh` - 全面的自动化特征提取（100+特征）
- `TSFreshRelevant` - 通过相关性过滤进行特征提取
- `SevenNumberSummary` - 描述性统计（均值、标准差、分位数）

* *何时使用**：需要可解释的特征、与领域无关的方法或提供传统的 ML。

### 基于字典表示形式

离散表示的符号近似：

- `SAX` - 符号聚合近似
- `PAA` - 分段聚合近似
- `SFA` - 符号傅立叶近似值
- `SFAFast` - 优化的SFA
- `SFAWhole` - 整个系列上的SFA（无窗口）
- `BORF` - Bag-of-Receptive-Fields

* *何时使用**：需要离散/符号表示、降维、可解释性.

### 基于 Shapelet 的特征

判别式子序列提取：

- `RandomShapeletTransform` - 随机判别 shapelet
- `RandomDilatedShapeletTransform` - 用于多尺度的扩张 shapelet
- `SAST` - 可扩展且准确的子序列Transform
- `RSAST` - 随机 SAST

* *使用时机**：需要可解释的判别模式、相位不变特征。

### Interval-Based Features

时间间隔的统计摘要：

- `RandomIntervals` - 来自随机的特征间隔
- `SupervisedIntervals` - 监督区间选择
- `QUANTTransformer` - 基于分位数的区间特征

* *使用时间**：预测模式本地化到特定窗口。

### 预处理转换

数据准备和标准化：

- `MinMaxScaler` - 缩放到 [0, 1]范围
- `Normalizer` - Z 归一化（零均值，单位方差）
- `Centerer` - 中心到零均值
- `SimpleImputer` - 填充缺失值
- `DownsampleTransformer` - 降低时间分辨率
- `Tabularizer` - 将时间序列转换为表格格式

* *何时使用**：需要标准化、缺失值处理、格式转换。

### 专业变换

高级分析方法：

- `MatrixProfile` - 计算距离剖面以进行模式发现
- `DWTTransformer` - 离散小波变换
- `AutocorrelationFunctionTransformer` - ACF 计算
- `Dobin` - 使用邻居的基于距离的离群值
- `SignatureTransformer` - 路径签名方法
- `PLATransformer` - 分段线性逼近

### 类不平衡处理

- `ADASYN` - 自适应合成采样
- `SMOTE` - 合成少数过采样
- `OHIT` - 高度不平衡时间序列的过采样

* *使用时间**：具有不平衡类别的分类。

### 管道构成

- `CollectionTransformerPipeline` - 链式多个变压器

## 系列转换器

转换单个时间序列（例如，用于预测中的预处理）。

### 统计分析

- `AutoCorrelationSeriesTransformer` - 自相关
- `StatsModelsACF` - 使用 statsmodels
- `StatsModelsPACF` 的 ACF - 部分自相关

### 平滑和过滤

- `ExponentialSmoothing` - 指数加权移动平均
- `MovingAverage` - 简单或加权移动平均
- `SavitzkyGolayFilter` - 多项式平滑
- `GaussianFilter` - 高斯核平滑
- `BKFilter` - Baxter-King 带通滤波器
- `DiscreteFourierApproximation` - 基于傅立叶的滤波

* *使用时**：需要降噪、趋势提取或频率滤波。

### 维度缩减

- `PCASeriesTransformer` - 主成分分析
- `PlASeriesTransformer` - 分段线性逼近

### 变换

- `BoxCoxTransformer` - 方差稳定化
- `LogTransformer` -对数缩放
- `ClaSPTransformer` - 分类分数概况

### 管道构成

- `SeriesTransformerPipeline` - 链式串联变压器

## 快速入门：特征提取

```python
from aeon.transformations.collection.convolution_based import RocketTransformer
from aeon.classification.sklearn import RotationForest
from aeon.datasets import load_classification

# Load data
X_train, y_train = load_classification("GunPoint", split="train")
X_test, y_test = load_classification("GunPoint", split="test")

# Extract ROCKET features
rocket = RocketTransformer()
X_train_features = rocket.fit_transform(X_train)
X_test_features = rocket.transform(X_test)

# Use with any sklearn classifier
clf = RotationForest()
clf.fit(X_train_features, y_train)
accuracy = clf.score(X_test_features, y_test)
```

## 快速入门：预处理管道

```python
from aeon.transformations.collection import (
    MinMaxScaler,
    SimpleImputer,
    CollectionTransformerPipeline
)

# Build preprocessing pipeline
pipeline = CollectionTransformerPipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', MinMaxScaler())
])

X_transformed = pipeline.fit_transform(X_train)
```

## 快速入门：系列平滑

```python
from aeon.transformations.series import MovingAverage

# Smooth individual time series
smoother = MovingAverage(window_size=5)
y_smoothed = smoother.fit_transform(y)
```

## 算法选择

### 用于特征提取：
- **速度+性能**： MiniRocketTransformer
- **可解释性**：Catch22、TSFresh
- **降维**：PAA、SAX、PCA
- **判别模式**：Shapelet 变换
- **综合功能**：TSFresh（运行时间更长）

### 对于预处理：
- **标准化**：标准化器、MinMaxScaler
- **平滑**：移动平均、SavitzkyGolayFilter
- **缺失值**：SimpleImputer
- **频率分析**：DWTTransformer、傅立叶方法

### 对于符号表示形式：
- **快速逼近**：PAA
- **基于字母**：SAX
- **基于频率**：SFA、SFAFast

## 最佳实践

1. **仅适合训练数据**：避免数据泄漏
 ```python
 Transformer.fit(X_train)
 X_train_tf = Transformer.transform(X_train)
 X_test_tf = Transformer.transform(X_test)
 ```

2. **管道组成**：复杂工作流程的transformers链
```python
 pipeline = CollectionTransformerPipeline([
('imputer', SimpleImputer()),
('scaler', Normalizer()),
('features', RocketTransformer())
 ])
``

3. **特征选择**：TSFresh可以生成很多特征；考虑选择
 ```python
 from sklearn.feature_selection import SelectKBest
 选择器 = SelectKBest(k=100)
 X_selected = 选择器.fit_transform(X_features, y)
 ```

4. **内存注意事项**：大型数据集上的一些 transformers 内存密集型
  - 使用 MiniRocket 而不是 ROCKET 来提高速度
  - 考虑对很长的系列进行下采样
  - 使用 ROCKETGPU 进行 GPU 加速

5. **领域知识**：选择匹配域的变换：
  - 周期性数据：基于傅立叶的方法
  - 噪声数据：平滑滤波器
  - 尖峰检测：小波变换
