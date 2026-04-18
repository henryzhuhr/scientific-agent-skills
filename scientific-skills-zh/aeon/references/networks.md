# Deep Learning Networks

Aeon 提供专为时间序列任务设计的神经网络架构。这些网络用作分类、回归、聚类和预测的构建块。

## 核心网络架构

### 卷积网络

* *FCNNetwork** - 全卷积网络
- 具有批量标准化的三个卷积块
- 用于降维的全局平均池化
- **何时使用**：需要简单而有效的 CNN 基线

* *ResNetNetwork** - 残差网络
- 具有跳跃连接的残差块
- 防止深度网络中梯度消失
- **使用时机**：需要深度网络，训练稳定性很重要

* *InceptionNetwork** - Inception 模块
- 多尺度特征提取使用并行卷积
- 不同的内核大小捕获不同尺度的模式
- **使用时**：模式存在于多个时间尺度

* *TimeCNNNetwork** - 标准 CNN
- 基本卷积架构
- **使用时间**：简单的 CNN 足够，可解释性有价值

* *不相交CNN网络** - 单独的路径
- 不相交的卷积路径
- **使用时间**：需要不同的特征提取策略

* *DCNNNetwork** - 扩张CNN
- 大感受野的扩张卷积
- **使用时机**：没有很多层的长程依赖

### 循环网络

* *RecurrentNetwork** - RNN/LSTM/GRU
- 可配置的单元类型（RNN、LSTM、GRU）
- 顺序网络时间依赖性建模
- **使用时机**：顺序依赖性关键，可变长度系列

### 时间卷积网络

* *TCNNetwork** - 时间卷积网络
- 扩张因果卷积
- 无复发的大感受野
- **使用时**：长序列，需要可并行架构

### 多层感知器

* *MLPNetwork** - 基本前馈
- 简单的全连接层
- 在处理前展平时间序列
- **使用时机**：需要基线、计算限制或简单模式

## 基于编码器的架构

专为表示学习和聚类而设计的网络。

### 自动编码器变体

* *EncoderNetwork** - 通用编码器
- 灵活的编码器结构
- **何时使用**：需要自定义编码

* *AEFCNNetwork** - 基于FCN的自动编码器
- 全卷积编码器-解码器
- **何时使用**：需要卷积表示学习

* *AEResNetNetwork** - ResNet 自动编码器
- 编码器-解码器中的剩余块
- **使用时**：具有跳过连接的深度自动编码

* *AEDCNNNetwork** - 扩张的CNN自动编码器
- 用于压缩的扩张卷积
- **使用当**：自动编码器中需要大的感受野

* *AEDRNNNetwork** - 扩张的 RNN 自动编码器
- 扩张的循环连接
- **使用时间**：具有远程依赖性的顺序模式

* *AEBiGRUNetwork** - 双向 GRU
- 双向循环编码
- **使用时间**：来自两个方向的上下文有帮助的

* *AEAttentionBiGRUNetwork** - Attention + BiGRU
- BiGRU输出上的注意机制
- **何时使用**：需要关注重要的时间步骤

## 专业架构

* *LITENetwork** - 轻量级Inception Time Ensemble
- 基于高效的inception架构
- 用于多元序列的 LITEMV 变体
- **何时使用**：需要高性能的效率

* *DeepARNetwork** - 概率预测
- 用于预测的自回归 RNN
- 生成概率预测
- **何时使用**：需要预测不确定性量化

## 与估计器一起使用

网络通常在估计器中使用，而不是直接使用：

```python
from aeon.classification.deep_learning import FCNClassifier
from aeon.regression.deep_learning import ResNetRegressor
from aeon.clustering.deep_learning import AEFCNClusterer

# Classification with FCN
clf = FCNClassifier(n_epochs=100, batch_size=16)
clf.fit(X_train, y_train)

# Regression with ResNet
reg = ResNetRegressor(n_epochs=100)
reg.fit(X_train, y_train)

# Clustering with autoencoder
clusterer = AEFCNClusterer(n_clusters=3, n_epochs=100)
labels = clusterer.fit_predict(X_train)
```

## 自定义网络配置

许多网络接受配置参数：

```python
# Configure FCN layers
clf = FCNClassifier(
    n_epochs=200,
    batch_size=32,
    kernel_size=[7, 5, 3],  # Kernel sizes for each layer
    n_filters=[128, 256, 128],  # Filters per layer
    learning_rate=0.001
)
```

## 基类

- `BaseDeepLearningNetwork` - 所有网络的抽象基类
- `BaseDeepRegressor` - 基类用于深度回归
- `BaseDeepClassifier` - 深度分类的基础
- `BaseDeepForecaster` - 深度预测的基础

扩展这些以实现自定义架构。

## 训练注意事项

### 超参数

关键超参数调整：

- `n_epochs` - 训练迭代（50-200 典型）
- `batch_size` - 每批次样本（16-64 典型）
- `learning_rate` - 步长（0.0001-0.01）
- 网络特定：层，过滤器、内核大小

### 回调

许多网络支持用于训练监控的回调：

```python
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

clf = FCNClassifier(
    n_epochs=200,
    callbacks=[
        EarlyStopping(patience=20, restore_best_weights=True),
        ReduceLROnPlateau(patience=10, factor=0.5)
    ]
)
```

### GPU 加速

深度学习网络受益于GPU：

```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Use first GPU

# Networks automatically use GPU if available
clf = InceptionTimeClassifier(n_epochs=100)
clf.fit(X_train, y_train)
```

## 架构选择

### 按任务：

* *分类**：InceptionNetwork、ResNetNetwork、FCNNetwork
* *回归**：InceptionNetwork、ResNetNetwork、TCNNetwork
* *预测**：TCNNetwork、DeepARNetwork、RecurrentNetwork
* *聚类**：AEFCNNetwork、AEResNetNetwork、AEAttentionBiGRUNetwork

### 按数据特征：

* *长序列**：TCNNetwork、DCNNNetwork（扩张卷积）
* *短序列**：MLPNetwork、FCNNetwork
* *多元**：InceptionNetwork、FCNNetwork、LITENetwork
* *可变长度**：带掩码的RecurrentNetwork
* *多尺度模式**： InceptionNetwork

### 按计算资源：

* *有限计算**：MLPNetwork、LITENetwork
* *中等计算**：FCNNetwork、TimeCNNNetwork
* *可用高计算**：InceptionNetwork、ResNetNetwork
* *可用 GPU**：任何深度网络（主要加速）

## 最佳实践

#### 1.数据准备

标准化输入数据：

```python
from aeon.transformations.collection import Normalizer

normalizer = Normalizer()
X_train_norm = normalizer.fit_transform(X_train)
X_test_norm = normalizer.transform(X_test)
```

### 2. 训练/验证拆分

使用验证集进行早期停止：

```python
from sklearn.model_selection import train_test_split

X_train_fit, X_val, y_train_fit, y_val = train_test_split(
    X_train, y_train, test_size=0.2, stratify=y_train
)

clf = FCNClassifier(n_epochs=200)
clf.fit(X_train_fit, y_train_fit, validation_data=(X_val, y_val))
```

### 3. 启动 Simple

先从较简单的架构开始，然后再从复杂的架构开始：

1. 首先尝试 MLPNetwork 或 FCNNetwork
2. 如果不够，可以尝试ResNetNetwork或InceptionNetwork
3. 如果单个模型不足，请考虑集成

### 4.超参数调优

使用网格搜索或随机搜索：

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_epochs': [100, 200],
    'batch_size': [16, 32],
    'learning_rate': [0.001, 0.0001]
}

clf = FCNClassifier()
grid = GridSearchCV(clf, param_grid, cv=3)
grid.fit(X_train, y_train)
```

### 5.正则化

防止过拟合：
- 使用dropout（如果网络支持）
- 提前停止
- 数据增强（如果有）
- 降低模型复杂度

### 6.再现性

设置随机种子：

```python
import numpy as np
import random
import tensorflow as tf

seed = 42
np.random.seed(seed)
random.seed(seed)
tf.random.set_seed(seed)
```
