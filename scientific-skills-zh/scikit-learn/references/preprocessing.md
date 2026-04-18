# 数据预处理与特征工程参考

## 概述

数据预处理将原始数据转换为适合机器学习模型的格式。这包括缩放、编码、处理缺失值和特征工程。

## 特征缩放和归一化

### StandardScaler

* *StandardScaler (`sklearn.preprocessing.StandardScaler`)**
- 将特征标准化为零均值和单位方差
- 公式：z = (x - 均值) / std
- 使用当：特征具有不同尺度时，算法假设数据呈正态分布
- 需要：SVM、KNN、神经网络、PCA、正则化线性回归
- 示例：
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Use same parameters as training

# Access learned parameters
print(f"Mean: {scaler.mean_}")
print(f"Std: {scaler.scale_}")
```

### MinMaxScaler

* *MinMaxScaler (`sklearn.preprocessing.MinMaxScaler`)**
- 将特征缩放到给定范围（默认 [0, 1]）
- 公式：X_scaled = (X - X.min) / (X.max - X.min)
- 何时使用：需要有界值，数据非正态分布
- 敏感离群值
- 示例：
```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))
X_scaled = scaler.fit_transform(X_train)

# Custom range
scaler = MinMaxScaler(feature_range=(-1, 1))
X_scaled = scaler.fit_transform(X_train)
```

### RobustScaler

* *RobustScaler (`sklearn.preprocessing.RobustScaler`)**
- 使用中位数和四分位距 (IQR)进行缩放 
- 公式：X_scaled = （X - 中位数）/ IQR
- 在以下情况下使用：数据包含异常值
- 对异常值具有鲁棒性
- 示例：
```python
from sklearn.preprocessing import RobustScaler

scaler = RobustScaler()
X_scaled = scaler.fit_transform(X_train)
```

### 标准化器

* *标准化器(`sklearn.preprocessing.Normalizer`)**
- 将样本单独归一化为单位范数
- 常用范数：'l1'、'l2'、'max' 
- 何时使用：需要独立归一化每个样本（例如文本特征）
- 示例：
```python
from sklearn.preprocessing import Normalizer

normalizer = Normalizer(norm='l2')  # Euclidean norm
X_normalized = normalizer.fit_transform(X)
```

### MaxAbsScaler

* *MaxAbsScaler (`sklearn.preprocessing.MaxAbsScaler`)**
- 按最大绝对值缩放
- 范围：[-1, 1]
- 不移动/居中数据（保留稀疏性）
- 在以下情况下使用：数据已居中或稀疏
- 示例：
```python
from sklearn.preprocessing import MaxAbsScaler

scaler = MaxAbsScaler()
X_scaled = scaler.fit_transform(X_sparse)
```

## 编码分类变量

### OneHotEncoder

* *OneHotEncoder (`sklearn.preprocessing.OneHotEncoder`)**
- 为每个类别创建二进制列
- 用于以下情况：标称类别（无顺序）、基于树的模型或线性模型
- 示例：
```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
X_encoded = encoder.fit_transform(X_categorical)

# Get feature names
feature_names = encoder.get_feature_names_out(['color', 'size'])

# Handle unknown categories during transform
X_test_encoded = encoder.transform(X_test_categorical)
```

### OrdinalEncoder

* *OrdinalEncoder (`sklearn.preprocessing.OrdinalEncoder`)**
- 将类别编码为整数
- 用于以下情况：序数类别（有序）或基于树的模型
- 示例：
```python
from sklearn.preprocessing import OrdinalEncoder

# Natural ordering
encoder = OrdinalEncoder()
X_encoded = encoder.fit_transform(X_categorical)

# Custom ordering
encoder = OrdinalEncoder(categories=[['small', 'medium', 'large']])
X_encoded = encoder.fit_transform(X_categorical)
```

### LabelEncoder

* *LabelEncoder (`sklearn.preprocessing.LabelEncoder`)**
- 将目标标签 (y)编码为整数
- 用于：目标变量编码
- 示例：
```python
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Decode back
y_decoded = le.inverse_transform(y_encoded)
print(f"Classes: {le.classes_}")
```

### 目标编码（使用category_encoders)

```python
# Install: uv pip install category-encoders
from category_encoders import TargetEncoder

encoder = TargetEncoder()
X_train_encoded = encoder.fit_transform(X_train_categorical, y_train)
X_test_encoded = encoder.transform(X_test_categorical)
```

## 非线性变换

### 幂变换

* *PowerTransformer**
- 使数据更像高斯
- 方法：'yeo-johnson'（适用于负数）值），'box-cox'（仅正）
- 在以下情况下使用：数据倾斜，算法假设正常
- 示例：
```python
from sklearn.preprocessing import PowerTransformer

# Yeo-Johnson (handles negative values)
pt = PowerTransformer(method='yeo-johnson', standardize=True)
X_transformed = pt.fit_transform(X)

# Box-Cox (positive values only)
pt = PowerTransformer(method='box-cox', standardize=True)
X_transformed = pt.fit_transform(X)
```

### 分位数变换

* *QuantileTransformer**
- 转换要遵循的特征均匀或正态分布
- 对异常值具有鲁棒性
- 用于以下情况：想要减少异常值影响
- 示例：
```python
from sklearn.preprocessing import QuantileTransformer

# Transform to uniform distribution
qt = QuantileTransformer(output_distribution='uniform', random_state=42)
X_transformed = qt.fit_transform(X)

# Transform to normal distribution
qt = QuantileTransformer(output_distribution='normal', random_state=42)
X_transformed = qt.fit_transform(X)
```

### 日志变换

```python
import numpy as np

# Log1p (log(1 + x)) - handles zeros
X_log = np.log1p(X)

# Or use FunctionTransformer
from sklearn.preprocessing import FunctionTransformer

log_transformer = FunctionTransformer(np.log1p, inverse_func=np.expm1)
X_log = log_transformer.fit_transform(X)
```

## 缺失值Imputation

### SimpleImputer

* *SimpleImputer (`sklearn.impute.SimpleImputer`)**
- 基本插补策略
- 策略：'mean'、'median'、'most_frequent'、'constant'
- 示例：
```python
from sklearn.impute import SimpleImputer

# For numerical features
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# For categorical features
imputer = SimpleImputer(strategy='most_frequent')
X_imputed = imputer.fit_transform(X_categorical)

# Fill with constant
imputer = SimpleImputer(strategy='constant', fill_value=0)
X_imputed = imputer.fit_transform(X)
```

### Iterative Imputer

* *IterativeImputer**
- 将每个具有缺失值的特征建模为其他特征的函数
- 比 SimpleImputer
 更复杂示例：
```python
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

imputer = IterativeImputer(max_iter=10, random_state=42)
X_imputed = imputer.fit_transform(X)
```

### KNN Imputer

* *KNNImputer**
- 使用 k 最近邻进行估算
- 用于以下情况：特征相关 
- 示例：
```python
from sklearn.impute import KNNImputer

imputer = KNNImputer(n_neighbors=5)
X_imputed = imputer.fit_transform(X)
```

## 特征工程

### 多项式特征

* *多项式特征**
- 创建多项式和交互特征
- 何时使用：需要线性模型的非线性特征
- 示例：
```python
from sklearn.preprocessing import PolynomialFeatures

# Degree 2: includes x1, x2, x1^2, x2^2, x1*x2
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

# Get feature names
feature_names = poly.get_feature_names_out(['x1', 'x2'])

# Only interactions (no powers)
poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_interactions = poly.fit_transform(X)
```

### 分箱/离散化

* *KBinsDiscretizer**
- 将连续特征分箱为离散间隔
- 策略：'uniform'、'quantile'、'kmeans'
- 编码：'onehot'、'ordinal'、'onehot-dense'
- 示例：
```python
from sklearn.preprocessing import KBinsDiscretizer

# Equal-width bins
binner = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='uniform')
X_binned = binner.fit_transform(X)

# Equal-frequency bins (quantile-based)
binner = KBinsDiscretizer(n_bins=5, encode='onehot', strategy='quantile')
X_binned = binner.fit_transform(X)
```

### 二值化

* *二值化器**
- 根据阈值将特征转换为二进制（0 或 1）
- 示例：
```python
from sklearn.preprocessing import Binarizer

binarizer = Binarizer(threshold=0.5)
X_binary = binarizer.fit_transform(X)
```

### 样条功能

* *SplineTransformer**
- 创建样条基函数
- 用于捕获非线性关系
- 示例：
```python
from sklearn.preprocessing import SplineTransformer

spline = SplineTransformer(n_knots=5, degree=3)
X_splines = spline.fit_transform(X)
```

## 文本特征提取

### CountVectorizer

* *CountVectorizer (`sklearn.feature_extraction.text.CountVectorizer`)**
- 将文本转换为标记计数矩阵
- 用于：词袋表示
- 示例：
```python
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(
    max_features=5000,  # Keep top 5000 features
    min_df=2,  # Ignore terms appearing in < 2 documents
    max_df=0.8,  # Ignore terms appearing in > 80% documents
    ngram_range=(1, 2)  # Unigrams and bigrams
)

X_counts = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names_out()
```

### TfidfVectorizer

* *TfidfVectorizer**
- TF-IDF（词频-逆文档频率）转换
- 对于大多数任务优于 CountVectorizer
- 示例：
```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    max_features=5000,
    min_df=2,
    max_df=0.8,
    ngram_range=(1, 2),
    stop_words='english'  # Remove English stop words
)

X_tfidf = vectorizer.fit_transform(documents)
```

### HashingVectorizer

* *HashingVectorizer**
- 使用哈希技巧提高内存效率
- 不需要拟合，无法反向变换
- 使用时：词汇量非常大，流数据
- 示例：
```python
from sklearn.feature_extraction.text import HashingVectorizer

vectorizer = HashingVectorizer(n_features=2**18)
X_hashed = vectorizer.transform(documents)  # No fit needed
```

## 特征选择

### 过滤方法

* *方差阈值**
- 删除低方差特征
- 示例：
```python
from sklearn.feature_selection import VarianceThreshold

selector = VarianceThreshold(threshold=0.01)
X_selected = selector.fit_transform(X)
```

* *SelectKBest / SelectPercentile**
- 基于统计选择特征测试
- 测试：f_classif、chi2、mutual_info_classif
- 示例：
```python
from sklearn.feature_selection import SelectKBest, f_classif

# Select top 10 features
selector = SelectKBest(score_func=f_classif, k=10)
X_selected = selector.fit_transform(X_train, y_train)

# Get selected feature indices
selected_indices = selector.get_support(indices=True)
```

### 包装方法

* *递归特征消除 (RFE)**
- 递归删除features
- 使用模型特征重要性
- 示例：
```python
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)
rfe = RFE(estimator=model, n_features_to_select=10, step=1)
X_selected = rfe.fit_transform(X_train, y_train)

# Get selected features
selected_features = rfe.support_
feature_ranking = rfe.ranking_
```

* *RFECV（带交叉验证）**
- 带有交叉验证的RFE以找到最佳特征数量
- 示例：
```python
from sklearn.feature_selection import RFECV

model = RandomForestClassifier(n_estimators=100, random_state=42)
rfecv = RFECV(estimator=model, cv=5, scoring='accuracy')
X_selected = rfecv.fit_transform(X_train, y_train)

print(f"Optimal number of features: {rfecv.n_features_}")
```

### 嵌入式方法

* *SelectFromModel**
- 根据模型系数/重要性选择特征
- 适用于：线性模型 (L1)、基于树的模型
- 示例：
```python
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)
selector = SelectFromModel(model, threshold='median')
selector.fit(X_train, y_train)
X_selected = selector.transform(X_train)

# Get selected features
selected_features = selector.get_support()
```

* *基于 L1 的特征选择**
```python
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel

model = LogisticRegression(penalty='l1', solver='liblinear', C=0.1)
selector = SelectFromModel(model)
selector.fit(X_train, y_train)
X_selected = selector.transform(X_train)
```

## 处理异常值

### IQR 方法

```python
import numpy as np

Q1 = np.percentile(X, 25, axis=0)
Q3 = np.percentile(X, 75, axis=0)
IQR = Q3 - Q1

# Define outlier boundaries
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Remove outliers
mask = np.all((X >= lower_bound) & (X <= upper_bound), axis=1)
X_no_outliers = X[mask]
```

### Winsorization

```python
from scipy.stats import mstats

# Clip outliers at 5th and 95th percentiles
X_winsorized = mstats.winsorize(X, limits=[0.05, 0.05], axis=0)
```

## 自定义Transformers

### 使用 FunctionTransformer

```python
from sklearn.preprocessing import FunctionTransformer
import numpy as np

def log_transform(X):
    return np.log1p(X)

transformer = FunctionTransformer(log_transform, inverse_func=np.expm1)
X_transformed = transformer.fit_transform(X)
```

### 创建自定义 Transformer

```python
from sklearn.base import BaseEstimator, TransformerMixin

class CustomTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, parameter=1):
        self.parameter = parameter

    def fit(self, X, y=None):
        # Learn parameters from X if needed
        return self

    def transform(self, X):
        # Transform X
        return X * self.parameter

transformer = CustomTransformer(parameter=2)
X_transformed = transformer.fit_transform(X)
```

## 最佳实践

### 仅适合训练数据
始终适合transformers 仅适用于训练数据：
```python
# Correct
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Wrong - causes data leakage
scaler = StandardScaler()
X_all_scaled = scaler.fit_transform(np.vstack([X_train, X_test]))
```

### 使用 Pipelines
将预处理与模型相结合：
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])

pipeline.fit(X_train, y_train)
```

### 分别处理分类和数值
使用列转换器：
```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

numeric_features = ['age', 'income']
categorical_features = ['gender', 'occupation']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ]
)

X_transformed = preprocessor.fit_transform(X)
```

### 算法特定要求

* *需要缩放：**
- SVM、KNN、神经网络
- PCA、带正则化的线性/Logistic 回归
- K-Means聚类

* *不需要缩放：**
- 基于树的模型（决策树、随机森林、梯度提升）
- 朴素贝叶斯

* *编码要求：**
- 线性模型、SVM、KNN：标称特征的 One-hot 编码
- 基于树的模型：可以直接处理序数编码
