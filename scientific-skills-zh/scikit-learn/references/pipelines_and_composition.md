# 管道和复合估计器参考

## 概述

管道将多个处理步骤链接到单个估计器中，防止数据泄漏并简化代码。它们支持可重复的工作流程以及与交叉验证和超参数调整的无缝集成。

## 管道基础知识

### 创建管道

* *管道 (`sklearn.pipeline.Pipeline`)**
- 具有最终估计器的 transformers 链 
- 所有中间步骤都必须具有fit_transform()
- 最终步骤可以是任何估计器（变压器、分类器、回归器、聚类器）
- 示例：
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=10)),
    ('classifier', LogisticRegression())
])

# Fit the entire pipeline
pipeline.fit(X_train, y_train)

# Predict using the pipeline
y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)
```

### 使用 make_pipeline

* *make_pipeline**
- 自动生成步骤的便捷构造函数名称
- 示例：
```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

pipeline = make_pipeline(
    StandardScaler(),
    PCA(n_components=10),
    SVC(kernel='rbf')
)

pipeline.fit(X_train, y_train)
```

## 访问管道组件

### 访问步骤

```python
# By index
scaler = pipeline.steps[0][1]

# By name
scaler = pipeline.named_steps['scaler']
pca = pipeline.named_steps['pca']

# Using indexing syntax
scaler = pipeline['scaler']
pca = pipeline['pca']

# Get all step names
print(pipeline.named_steps.keys())
```

### 设置参数

```python
# Set parameters using double underscore notation
pipeline.set_params(
    pca__n_components=15,
    classifier__C=0.1
)

# Or during creation
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=10)),
    ('classifier', LogisticRegression(C=1.0))
])
```

### 访问属性

```python
# Access fitted attributes
pca_components = pipeline.named_steps['pca'].components_
explained_variance = pipeline.named_steps['pca'].explained_variance_ratio_

# Access intermediate transformations
X_scaled = pipeline.named_steps['scaler'].transform(X_test)
X_pca = pipeline.named_steps['pca'].transform(X_scaled)
```

## 使用管道进行超参数调整

### 使用管道进行网格搜索

```python
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', SVC())
])

param_grid = {
    'classifier__C': [0.1, 1, 10, 100],
    'classifier__gamma': ['scale', 'auto', 0.001, 0.01],
    'classifier__kernel': ['rbf', 'linear']
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.3f}")
```

### 调整多个管道步骤

```python
param_grid = {
    # PCA parameters
    'pca__n_components': [5, 10, 20, 50],

    # Classifier parameters
    'classifier__C': [0.1, 1, 10],
    'classifier__kernel': ['rbf', 'linear']
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5)
grid_search.fit(X_train, y_train)
```

## ColumnTransformer

### 基本用法

* *ColumnTransformer (`sklearn.compose.ColumnTransformer`)**
- 对不同列应用不同的预处理
- 防止数据泄漏交叉验证
- 示例：
```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# Define column groups
numeric_features = ['age', 'income', 'hours_per_week']
categorical_features = ['gender', 'occupation', 'native_country']

# Create preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'  # Keep other columns unchanged
)

X_transformed = preprocessor.fit_transform(X)
```

### 使用管道步骤

```python
from sklearn.pipeline import Pipeline

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Full pipeline with model
full_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression())
])

full_pipeline.fit(X_train, y_train)
```

### 使用make_column_transformer

```python
from sklearn.compose import make_column_transformer

preprocessor = make_column_transformer(
    (StandardScaler(), numeric_features),
    (OneHotEncoder(), categorical_features),
    remainder='passthrough'
)
```

### 列选择

```python
# By column names (if X is DataFrame)
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), ['age', 'income']),
    ('cat', OneHotEncoder(), ['gender', 'occupation'])
])

# By column indices
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), [0, 1, 2]),
    ('cat', OneHotEncoder(), [3, 4])
])

# By boolean mask
numeric_mask = [True, True, True, False, False]
categorical_mask = [False, False, False, True, True]

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_mask),
    ('cat', OneHotEncoder(), categorical_mask)
])

# By callable
def is_numeric(X):
    return X.select_dtypes(include=['number']).columns.tolist()

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), is_numeric)
])
```

### 获取特征名称

```python
# Get output feature names
feature_names = preprocessor.get_feature_names_out()

# After fitting
preprocessor.fit(X_train)
output_features = preprocessor.get_feature_names_out()
print(f"Input features: {X_train.columns.tolist()}")
print(f"Output features: {output_features}")
```

### 剩余处理

```python
# Drop unspecified columns (default)
preprocessor = ColumnTransformer([...], remainder='drop')

# Pass through unchanged
preprocessor = ColumnTransformer([...], remainder='passthrough')

# Apply transformer to remaining columns
preprocessor = ColumnTransformer([...], remainder=StandardScaler())
```

## FeatureUnion

### 基本用法

* *FeatureUnion(`sklearn.pipeline.FeatureUnion`)**
- 连接多个变压器的结果
- Transformers应用于并行
- 示例：
```python
from sklearn.pipeline import FeatureUnion
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest

# Combine PCA and feature selection
feature_union = FeatureUnion([
    ('pca', PCA(n_components=10)),
    ('select_best', SelectKBest(k=20))
])

X_combined = feature_union.fit_transform(X_train, y_train)
print(f"Combined features: {X_combined.shape[1]}")  # 10 + 20 = 30
```

### 带管道

```python
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, TruncatedSVD

# Create feature union
feature_union = FeatureUnion([
    ('pca', PCA(n_components=10)),
    ('svd', TruncatedSVD(n_components=10))
])

# Full pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('features', feature_union),
    ('classifier', LogisticRegression())
])

pipeline.fit(X_train, y_train)
```

### 加权特征联盟

```python
# Apply weights to transformers
feature_union = FeatureUnion(
    transformer_list=[
        ('pca', PCA(n_components=10)),
        ('select_best', SelectKBest(k=20))
    ],
    transformer_weights={
        'pca': 2.0,  # Give PCA features double weight
        'select_best': 1.0
    }
)
```

## 高级管道模式

### 缓存管道步骤

```python
from sklearn.pipeline import Pipeline
from tempfile import mkdtemp
from shutil import rmtree

# Cache intermediate results
cachedir = mkdtemp()
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=50)),
    ('classifier', LogisticRegression())
], memory=cachedir)

pipeline.fit(X_train, y_train)

# Clean up cache
rmtree(cachedir)
```

### 嵌套管道

```python
from sklearn.pipeline import Pipeline

# Inner pipeline for text processing
text_pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer())
])

# Outer pipeline combining text and numeric features
full_pipeline = Pipeline([
    ('features', FeatureUnion([
        ('text', text_pipeline),
        ('numeric', StandardScaler())
    ])),
    ('classifier', LogisticRegression())
])
```

### 中的自定义Transformers管道

```python
from sklearn.base import BaseEstimator, TransformerMixin

class TextLengthExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [[len(text)] for text in X]

pipeline = Pipeline([
    ('length', TextLengthExtractor()),
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])
```

### 切片管道

```python
# Get sub-pipeline
sub_pipeline = pipeline[:2]  # First two steps

# Get specific range
middle_steps = pipeline[1:3]
```

## TransformedTargetRegressor

### 基本用法

* *TransformedTargetRegressor**
- 在拟合之前转换目标变量
- 自动逆变换预测
- 示例：
```python
from sklearn.compose import TransformedTargetRegressor
from sklearn.preprocessing import QuantileTransformer
from sklearn.linear_model import LinearRegression

model = TransformedTargetRegressor(
    regressor=LinearRegression(),
    transformer=QuantileTransformer(output_distribution='normal')
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)  # Automatically inverse-transformed
```

### 带函数

```python
import numpy as np

model = TransformedTargetRegressor(
    regressor=LinearRegression(),
    func=np.log1p,
    inverse_func=np.expm1
)

model.fit(X_train, y_train)
```

## 完整示例：端到端管道

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

# Define feature types
numeric_features = ['age', 'income', 'hours_per_week']
categorical_features = ['gender', 'occupation', 'education']

# Numeric preprocessing pipeline
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Categorical preprocessing pipeline
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Combine preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Full pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('pca', PCA(n_components=0.95)),  # Keep 95% variance
    ('classifier', RandomForestClassifier(random_state=42))
])

# Hyperparameter tuning
param_grid = {
    'preprocessor__num__imputer__strategy': ['mean', 'median'],
    'pca__n_components': [0.90, 0.95, 0.99],
    'classifier__n_estimators': [100, 200],
    'classifier__max_depth': [10, 20, None]
}

grid_search = GridSearchCV(
    pipeline, param_grid,
    cv=5, scoring='accuracy',
    n_jobs=-1, verbose=1
)

grid_search.fit(X_train, y_train)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV score: {grid_search.best_score_:.3f}")
print(f"Test score: {grid_search.score(X_test, y_test):.3f}")

# Make predictions
best_pipeline = grid_search.best_estimator_
y_pred = best_pipeline.predict(X_test)
y_proba = best_pipeline.predict_proba(X_test)
```

## 可视化

### 显示管道

```python
# In Jupyter notebooks, pipelines display as diagrams
from sklearn import set_config
set_config(display='diagram')

pipeline  # Displays visual diagram
```

### 文本表示

```python
# Print pipeline structure
print(pipeline)

# Get detailed parameters
print(pipeline.get_params())
```

## 最佳实践

### 始终使用管道
- 防止数据泄漏
- 确保训练和数据之间的一致性预测
- 使代码更易于维护
- 启用简单的超参数调整

### 正确的管道构造
```python
# Good: Preprocessing inside pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
pipeline.fit(X_train, y_train)

# Bad: Preprocessing outside pipeline (can cause leakage)
X_train_scaled = StandardScaler().fit_transform(X_train)
model = LogisticRegression()
model.fit(X_train_scaled, y_train)
```

### 对混合数据使用ColumnTransformer
当您同时拥有数值和分类数据时，始终使用ColumnTransformer功能：
```python
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_features),
    ('cat', OneHotEncoder(), categorical_features)
])
```

### 有意义地命名您的步骤
```python
# Good
pipeline = Pipeline([
    ('imputer', SimpleImputer()),
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=10)),
    ('rf_classifier', RandomForestClassifier())
])

# Bad
pipeline = Pipeline([
    ('step1', SimpleImputer()),
    ('step2', StandardScaler()),
    ('step3', PCA(n_components=10)),
    ('step4', RandomForestClassifier())
])
```

### 缓存昂贵的转换
对于重复拟合（例如，在网格搜索期间），缓存昂贵步骤：
```python
from tempfile import mkdtemp

cachedir = mkdtemp()
pipeline = Pipeline([
    ('expensive_preprocessing', ExpensiveTransformer()),
    ('classifier', LogisticRegression())
], memory=cachedir)
```

### 测试管道兼容性
确保所有步骤兼容：
- 所有中间步骤必须有fit()和transform()
- 最终步骤需要fit()和predict()（或transform()）
- 使用set_output(transform='pandas') for DataFrame 输出
```python
pipeline.set_output(transform='pandas')
X_transformed = pipeline.transform(X)  # Returns DataFrame
```
