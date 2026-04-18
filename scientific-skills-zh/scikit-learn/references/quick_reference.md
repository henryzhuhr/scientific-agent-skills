# Scikit-learn 快速参考

## 常用导入模式

```python
# Core scikit-learn
import sklearn

# Data splitting and cross-validation
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV

# Preprocessing
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# Feature selection
from sklearn.feature_selection import SelectKBest, RFE

# Supervised learning
from sklearn.linear_model import LogisticRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier

# Unsupervised learning
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA, NMF

# Metrics
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, r2_score, confusion_matrix, classification_report
)

# Pipeline
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer

# Utilities
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

## 安装

```bash
# Using uv (recommended)
uv pip install scikit-learn

# Optional dependencies
uv pip install scikit-learn[plots]  # For plotting utilities
uv pip install pandas numpy matplotlib seaborn  # Common companions
```

## 快速工作流程模板

### 分类管道

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Preprocess
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
```

### 回归管道

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Preprocess and train
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = GradientBoostingRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
print(f"RMSE: {mean_squared_error(y_test, y_pred, squared=False):.3f}")
print(f"R² Score: {r2_score(y_test, y_pred):.3f}")
```

### 交叉验证

```python
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"CV Accuracy: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
```

### 混合数据的完整管道类型

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

# Define feature types
numeric_features = ['age', 'income']
categorical_features = ['gender', 'occupation']

# Create preprocessing pipelines
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine transformers
preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# Full pipeline
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Fit and predict
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

### 超参数调优

```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

model = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(
    model, param_grid, cv=5, scoring='accuracy', n_jobs=-1
)

grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.3f}")

# Use best model
best_model = grid_search.best_estimator_
```

## 常见模式

### 加载数据

```python
# From scikit-learn datasets
from sklearn.datasets import load_iris, load_digits, make_classification

# Built-in datasets
iris = load_iris()
X, y = iris.data, iris.target

# Synthetic data
X, y = make_classification(
    n_samples=1000, n_features=20, n_classes=2, random_state=42
)

# From pandas
import pandas as pd
df = pd.read_csv('data.csv')
X = df.drop('target', axis=1)
y = df['target']
```

### 处理不平衡数据

```python
from sklearn.ensemble import RandomForestClassifier

# Use class_weight parameter
model = RandomForestClassifier(class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Or use appropriate metrics
from sklearn.metrics import balanced_accuracy_score, f1_score
print(f"Balanced Accuracy: {balanced_accuracy_score(y_test, y_pred):.3f}")
print(f"F1 Score: {f1_score(y_test, y_pred):.3f}")
```

### 特征重要性

```python
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Get feature importances
importances = pd.DataFrame({
    'feature': feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(importances.head(10))
```

### 聚类

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Scale data first
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X_scaled)

# Evaluate
from sklearn.metrics import silhouette_score
score = silhouette_score(X_scaled, labels)
print(f"Silhouette Score: {score:.3f}")
```

### 维度减少

```python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Fit PCA
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

# Plot
plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y, cmap='viridis')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title(f'PCA (explained variance: {pca.explained_variance_ratio_.sum():.2%})')
```

### 模型持久性

```python
import joblib

# Save model
joblib.dump(model, 'model.pkl')

# Load model
loaded_model = joblib.load('model.pkl')
predictions = loaded_model.predict(X_new)
```

## 常见问题和解决方案

### 数据泄漏
```python
# WRONG: Fitting scaler on all data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test = train_test_split(X_scaled)

# RIGHT: Fit on training data only
X_train, X_test = train_test_split(X)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# BEST: Use Pipeline
from sklearn.pipeline import Pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
pipeline.fit(X_train, y_train)  # No leakage!
```

### 分类的分层分割
```python
# Always use stratify for classification
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```

### 随机状态的再现性
```python
# Set random_state for reproducibility
model = RandomForestClassifier(n_estimators=100, random_state=42)
```

### 处理未知类别
```python
# Use handle_unknown='ignore' for OneHotEncoder
encoder = OneHotEncoder(handle_unknown='ignore')
```

### 特征名称管道
```python
# Get feature names after transformation
preprocessor.fit(X_train)
feature_names = preprocessor.get_feature_names_out()
```

## 备忘单：算法选择

### 分类

|问题 |算法|何时使用 |
|---------|------------|------------|
|二元/多类 |逻辑回归 |快速基线，可解释性|
|二元/多类 |随机森林|默认良好，稳健|
|二元/多类 |梯度提升|最佳精度，愿意调|
|二元/多类 |支持向量机|数据小，边界复杂|
|二元/多类 |朴素贝叶斯 |文本分类，快速|
|高尺寸 |线性 SVM 或 Logistic |文本，多种特征 |

### 回归

|问题 |算法|何时使用 |
|---------|------------|------------|
|持续目标|线性回归|快速基线，可解释性|
|持续目标|山脊/套索|需要正则化|
|持续目标|随机森林|良好的默认，非线性|
|持续目标|梯度提升|最佳精度|
|持续目标| SVR |小数据，非线性|

### 聚类

|问题 |算法|何时使用 |
|---------|------------|-------------|
|已知 K，球形 | K 均值 |快速、简单 |
|未知 K，任意形状 |数据库扫描 |存在噪音/异常值 |
|层级结构|集聚 |需要树状图 |
|软聚类|高斯混合 |概率估计 |

### 降维

|问题 |算法|何时使用 |
|---------|------------|-------------|
|线性减速 |主成分分析|方差解释|
|可视化| t-SNE | 2D/3D 绘图 |
|非负数据| NMF |图片、文字|
|稀疏数据|截断SVD |文本、推荐系统 |

## 性能提示

### 加速训练
```python
# Use n_jobs=-1 for parallel processing
model = RandomForestClassifier(n_estimators=100, n_jobs=-1)

# Use warm_start for incremental learning
model = RandomForestClassifier(n_estimators=100, warm_start=True)
model.fit(X, y)
model.n_estimators += 50
model.fit(X, y)  # Adds 50 more trees

# Use partial_fit for online learning
from sklearn.linear_model import SGDClassifier
model = SGDClassifier()
for X_batch, y_batch in batches:
    model.partial_fit(X_batch, y_batch, classes=np.unique(y))
```

### 内存效率
```python
# Use sparse matrices
from scipy.sparse import csr_matrix
X_sparse = csr_matrix(X)

# Use MiniBatchKMeans for large data
from sklearn.cluster import MiniBatchKMeans
model = MiniBatchKMeans(n_clusters=8, batch_size=100)
```

## 版本查看

```python
import sklearn
print(f"scikit-learn version: {sklearn.__version__}")
```

## 有用资源

 - 官方文档：https://scikit-learn.org/stable/
  - 用户指南：https://scikit-learn.org/stable/user_guide.html
  - API参考： https://scikit-learn.org/stable/api/index.html
  - 示例：https://scikit-learn.org/stable/auto_examples/index.html
  - 教程：https://scikit-learn.org/stable/tutorial/index.html
