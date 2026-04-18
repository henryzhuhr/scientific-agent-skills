# 模型选择和评估参考

## 概述

使用scikit-learn的模型选择工具评估模型、调整超参数和选择最佳模型的综合指南。

## 训练测试分割

### 基本分割

```python
from sklearn.model_selection import train_test_split

# Basic split (default 75/25)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# With stratification (preserves class distribution)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)

# Three-way split (train/val/test)
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
```

## 交叉验证

### 交叉验证策略

* *KFold**
- 标准 k 折交叉验证
- 将数据拆分为 k 个连续折叠
```python
from sklearn.model_selection import KFold

kf = KFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, val_idx in kf.split(X):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
```

* *StratifiedKFold**
- 保留类每个折叠中的分布
- 用于不平衡分类
```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, val_idx in skf.split(X, y):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
```

* *TimeSeriesSplit**
- 用于时间序列数据
- 尊重时间order
```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
for train_idx, val_idx in tscv.split(X):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
```

* *GroupKFold**
- 确保来自同一组的样本不会出现在训练和验证中
- 当样本不独立时使用
```python
from sklearn.model_selection import GroupKFold

gkf = GroupKFold(n_splits=5)
for train_idx, val_idx in gkf.split(X, y, groups=group_ids):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
```

* *LeaveOneOut (LOO)**
- 每个样本用作验证集一次
- 用于非常小的数据集
- 计算成本昂贵
```python
from sklearn.model_selection import LeaveOneOut

loo = LeaveOneOut()
for train_idx, val_idx in loo.split(X):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
```

### 交叉验证函数

* *cross_val_score**
- 评估使用交叉验证的模型
- 返回分数数组
```python
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print(f"Scores: {scores}")
print(f"Mean: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
```

* *cross_validate**
- 比cross_val_score更全面
- 可以返回多个指标和拟合times
```python
from sklearn.model_selection import cross_validate

model = RandomForestClassifier(n_estimators=100, random_state=42)
cv_results = cross_validate(
    model, X, y, cv=5,
    scoring=['accuracy', 'precision', 'recall', 'f1'],
    return_train_score=True,
    return_estimator=True  # Returns fitted estimators
)

print(f"Test accuracy: {cv_results['test_accuracy'].mean():.3f}")
print(f"Test precision: {cv_results['test_precision'].mean():.3f}")
print(f"Fit time: {cv_results['fit_time'].mean():.3f}s")
```

* *cross_val_predict**
- 获取每个样本在验证集中时的预测
- 用于分析错误
```python
from sklearn.model_selection import cross_val_predict

model = RandomForestClassifier(n_estimators=100, random_state=42)
y_pred = cross_val_predict(model, X, y, cv=5)

# Now can analyze predictions vs actual
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y, y_pred)
```

## 超参数调整

### 网格搜索

* *GridSearchCV**
- 对参数网格进行详尽搜索
- 测试所有组合
```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

model = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(
    model, param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,  # Use all CPU cores
    verbose=1
)

grid_search.fit(X_train, y_train)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best cross-validation score: {grid_search.best_score_:.3f}")
print(f"Test score: {grid_search.score(X_test, y_test):.3f}")

# Access best model
best_model = grid_search.best_estimator_

# View all results
import pandas as pd
results_df = pd.DataFrame(grid_search.cv_results_)
```

### 随机搜索

* *RandomizedSearchCV**
- 从参数中采样随机组合分布
- 对于大型搜索空间更有效
```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

param_distributions = {
    'n_estimators': randint(50, 300),
    'max_depth': [5, 10, 15, 20, None],
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'max_features': uniform(0.1, 0.9)  # Continuous distribution
}

model = RandomForestClassifier(random_state=42)
random_search = RandomizedSearchCV(
    model, param_distributions,
    n_iter=100,  # Number of parameter settings sampled
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    verbose=1,
    random_state=42
)

random_search.fit(X_train, y_train)

print(f"Best parameters: {random_search.best_params_}")
print(f"Best score: {random_search.best_score_:.3f}")
```

### 连续减半

* *HalvingGridSearchCV / HalvingRandomSearchCV**
- 使用连续减半迭代地选择最佳候选者
- 比详尽更有效搜索
```python
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingGridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200, 300],
    'max_depth': [5, 10, 15, 20, None],
    'min_samples_split': [2, 5, 10, 20]
}

model = RandomForestClassifier(random_state=42)
halving_search = HalvingGridSearchCV(
    model, param_grid,
    cv=5,
    factor=3,  # Proportion of candidates eliminated in each iteration
    resource='n_samples',  # Can also use 'n_estimators' for ensembles
    max_resources='auto',
    random_state=42
)

halving_search.fit(X_train, y_train)
print(f"Best parameters: {halving_search.best_params_}")
```

## 分类指标

### 基本指标

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    balanced_accuracy_score, matthews_corrcoef
)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')  # For multiclass
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')
balanced_acc = balanced_accuracy_score(y_test, y_pred)  # Good for imbalanced data
mcc = matthews_corrcoef(y_test, y_pred)  # Matthews correlation coefficient

print(f"Accuracy: {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1-score: {f1:.3f}")
print(f"Balanced Accuracy: {balanced_acc:.3f}")
print(f"MCC: {mcc:.3f}")
```

### 分类报告

```python
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred, target_names=class_names))
```

### 混淆矩阵

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(cmap='Blues')
plt.show()
```

### ROC和AUC

```python
from sklearn.metrics import roc_auc_score, roc_curve, RocCurveDisplay

# Binary classification
y_proba = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_proba)
print(f"ROC AUC: {auc:.3f}")

# Plot ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=auc).plot()

# Multiclass (one-vs-rest)
auc_ovr = roc_auc_score(y_test, y_proba_multi, multi_class='ovr')
```

### 精确召回曲线

```python
from sklearn.metrics import precision_recall_curve, PrecisionRecallDisplay
from sklearn.metrics import average_precision_score

precision, recall, thresholds = precision_recall_curve(y_test, y_proba)
ap = average_precision_score(y_test, y_proba)

disp = PrecisionRecallDisplay(precision=precision, recall=recall, average_precision=ap)
disp.plot()
```

### 对数损失

```python
from sklearn.metrics import log_loss

y_proba = model.predict_proba(X_test)
logloss = log_loss(y_test, y_proba)
print(f"Log Loss: {logloss:.3f}")
```

## 回归指标

```python
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    mean_absolute_percentage_error, median_absolute_error
)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)
median_ae = median_absolute_error(y_test, y_pred)

print(f"MSE: {mse:.3f}")
print(f"RMSE: {rmse:.3f}")
print(f"MAE: {mae:.3f}")
print(f"R² Score: {r2:.3f}")
print(f"MAPE: {mape:.3f}")
print(f"Median AE: {median_ae:.3f}")
```

## 聚类指标

### 带接地真相标签

```python
from sklearn.metrics import (
    adjusted_rand_score, normalized_mutual_info_score,
    adjusted_mutual_info_score, fowlkes_mallows_score,
    homogeneity_score, completeness_score, v_measure_score
)

ari = adjusted_rand_score(y_true, y_pred)
nmi = normalized_mutual_info_score(y_true, y_pred)
ami = adjusted_mutual_info_score(y_true, y_pred)
fmi = fowlkes_mallows_score(y_true, y_pred)
homogeneity = homogeneity_score(y_true, y_pred)
completeness = completeness_score(y_true, y_pred)
v_measure = v_measure_score(y_true, y_pred)
```

### 没有地面真相

```python
from sklearn.metrics import (
    silhouette_score, calinski_harabasz_score, davies_bouldin_score
)

silhouette = silhouette_score(X, labels)  # [-1, 1], higher better
ch_score = calinski_harabasz_score(X, labels)  # Higher better
db_score = davies_bouldin_score(X, labels)  # Lower better
```

## 自定义评分

### 使用make_scorer

```python
from sklearn.metrics import make_scorer

def custom_metric(y_true, y_pred):
    # Your custom logic
    return score

custom_scorer = make_scorer(custom_metric, greater_is_better=True)

# Use in cross-validation or grid search
scores = cross_val_score(model, X, y, cv=5, scoring=custom_scorer)
```

### 多个网格搜索中的指标

```python
from sklearn.model_selection import GridSearchCV

scoring = {
    'accuracy': 'accuracy',
    'precision': 'precision_weighted',
    'recall': 'recall_weighted',
    'f1': 'f1_weighted'
}

grid_search = GridSearchCV(
    model, param_grid,
    cv=5,
    scoring=scoring,
    refit='f1',  # Refit on best f1 score
    return_train_score=True
)

grid_search.fit(X_train, y_train)
```

## 验证曲线

### 学习曲线

```python
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
import numpy as np

train_sizes, train_scores, val_scores = learning_curve(
    model, X, y,
    cv=5,
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring='accuracy',
    n_jobs=-1
)

train_mean = train_scores.mean(axis=1)
train_std = train_scores.std(axis=1)
val_mean = val_scores.mean(axis=1)
val_std = val_scores.std(axis=1)

plt.figure(figsize=(10, 6))
plt.plot(train_sizes, train_mean, label='Training score')
plt.plot(train_sizes, val_mean, label='Validation score')
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1)
plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1)
plt.xlabel('Training Set Size')
plt.ylabel('Score')
plt.title('Learning Curve')
plt.legend()
plt.grid(True)
```

### 验证Curve

```python
from sklearn.model_selection import validation_curve

param_range = [1, 10, 50, 100, 200, 500]
train_scores, val_scores = validation_curve(
    model, X, y,
    param_name='n_estimators',
    param_range=param_range,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)

train_mean = train_scores.mean(axis=1)
val_mean = val_scores.mean(axis=1)

plt.figure(figsize=(10, 6))
plt.plot(param_range, train_mean, label='Training score')
plt.plot(param_range, val_mean, label='Validation score')
plt.xlabel('n_estimators')
plt.ylabel('Score')
plt.title('Validation Curve')
plt.legend()
plt.grid(True)
```

## 模型持久性

### 保存和加载模型

```python
import joblib

# Save model
joblib.dump(model, 'model.pkl')

# Load model
loaded_model = joblib.load('model.pkl')

# Also works with pipelines
joblib.dump(pipeline, 'pipeline.pkl')
```

### 使用pickle

```python
import pickle

# Save
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Load
with open('model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)
```

## 不平衡数据策略

### 类加权

```python
from sklearn.ensemble import RandomForestClassifier

# Automatically balance classes
model = RandomForestClassifier(class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Custom weights
class_weights = {0: 1, 1: 10}  # Give class 1 more weight
model = RandomForestClassifier(class_weight=class_weights, random_state=42)
```

### 重采样（使用不平衡学习）

```python
# Install: uv pip install imbalanced-learn
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline

# SMOTE oversampling
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Combined approach
pipeline = ImbPipeline([
    ('over', SMOTE(sampling_strategy=0.5)),
    ('under', RandomUnderSampler(sampling_strategy=0.8)),
    ('model', RandomForestClassifier())
])
```

## 最佳实践

### 分层分割
始终使用分层分割进行分类：
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
```

### 适当的指标
- **平衡数据**：准确率、F1-score
- **不平衡数据**：精度、召回率、F1-score、ROC AUC，平衡精度
- **成本敏感**：使用成本定义自定义评分器
- **排名**：ROC AUC，平均精度

### 交叉验证
- 在大多数情况下使用 5 或 10 倍 CV
- 使用 StratifiedKFold分类
- 对时间序列使用TimeSeriesSplit
- 对样本进行分组时使用GroupKFold

### 嵌套交叉验证
用于调整时无偏的性能估计：
```python
from sklearn.model_selection import cross_val_score, GridSearchCV

# Inner loop: hyperparameter tuning
grid_search = GridSearchCV(model, param_grid, cv=5)

# Outer loop: performance estimation
scores = cross_val_score(grid_search, X, y, cv=5)
print(f"Nested CV score: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
```
