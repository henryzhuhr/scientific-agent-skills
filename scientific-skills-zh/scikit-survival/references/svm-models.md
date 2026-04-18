# 生存支持向量机

## 概述

生存支持向量机 (SVM)将传统的 SVM 框架应用于审查数据的生存分析。他们优化了鼓励正确排序生存时间的排名目标。

### 用于生存分析的核心思想

SVM 学习产生风险评分的函数 f(x)，其中优化确保生存时间较短的受试者比生存时间较长的受试者获得更高的风险分数。

## 何时使用生存 SVM

* *适用于：**
- 中等规模的数据集（通常有 100-10,000 个样本）
- 需要非线性决策边界（内核 SVM）
- 需要基于边际的正则化学习
- 具有明确定义的特征空间

* *不适合：**
- 非常大的数据集（>100,000 个样本）-集成方法可能更快
- 需要可解释的系数-使用Cox模型代替
- 需要生存函数估计-使用随机生存森林
- 非常高维的数据-使用正则化Cox或梯度提升

## 模型类型

### FastSurvivalSVM

线性生存使用坐标下降对速度进行优化的 SVM。

* *何时使用：**
- 预期的线性关系
- 速度很重要的大型数据集
- 想要快速训练和预测

* *关键参数：**
- `alpha`：正则化参数（默认值： 1.0)
  - 更高 = 更多正则化
- `rank_ratio`：排名和回归之间的权衡（默认：1.0）
- `max_iter`：最大迭代次数（默认：20）
- `tol`：停止标准的容差（默认： 1e-5)

```python
from sksurv.svm import FastSurvivalSVM

# Fit linear survival SVM
estimator = FastSurvivalSVM(alpha=1.0, max_iter=100, tol=1e-5, random_state=42)
estimator.fit(X, y)

# Predict risk scores
risk_scores = estimator.predict(X_test)
```

### FastKernelSurvivalSVM

用于非线性关系的内核生存 SVM。

* *何时使用：**
- 特征和生存之间的非线性关系
- 中型数据集
- 可以承受更长的训练时间以获得更好的性能

* *内核选项：**
- `'linear'`：线性内核，相当于 FastSurvivalSVM
- `'poly'`：多项式内核
- `'rbf'`：径向基函数（高斯）内核 - 最常见
- `'sigmoid'`：Sigmoid kernel
- 自定义核函数

* *关键参数：**
- `alpha`：正则化参数（默认：1.0）
- `kernel`：核函数（默认：'rbf'）
- `gamma`：rbf、poly、 sigmoid
- `degree`：多项式核的次数
- `coef0`：poly 和 sigmoid 的独立项
- `rank_ratio`：权衡参数（默认值：1.0）
- `max_iter`：最大值迭代次数（默认值：20）

```python
from sksurv.svm import FastKernelSurvivalSVM

# Fit RBF kernel survival SVM
estimator = FastKernelSurvivalSVM(
    alpha=1.0,
    kernel='rbf',
    gamma='scale',
    max_iter=50,
    random_state=42
)
estimator.fit(X, y)

# Predict risk scores
risk_scores = estimator.predict(X_test)
```

### HingeLossSurvivalSVM

使用铰链损失的生存SVM，与分类SVM更相似。

* *何时使用：**
- 希望铰链损失而不是平方铰链
- 所需的稀疏解决方案
- 与分类SVM类似的行为

* *关键参数：**
- `alpha`：正则化参数
- `fit_intercept`：是否拟合截距项（默认值： False)

```python
from sksurv.svm import HingeLossSurvivalSVM

# Fit hinge loss SVM
estimator = HingeLossSurvivalSVM(alpha=1.0, fit_intercept=False, random_state=42)
estimator.fit(X, y)

# Predict risk scores
risk_scores = estimator.predict(X_test)
```

### NaiveSurvivalSVM

使用二次规划的生存 SVM 的原始公式。

* *何时使用：**
- 小数据集
- 研究/基准测试目的
- 其他方法不收敛

* *限制：**
- 比快速变体慢
- 可扩展性较差

```python
from sksurv.svm import NaiveSurvivalSVM

# Fit naive SVM (slower)
estimator = NaiveSurvivalSVM(alpha=1.0, random_state=42)
estimator.fit(X, y)

# Predict
risk_scores = estimator.predict(X_test)
```

### MinlipSurvivalAnalysis

使用最小化Lipschitz常数方法进行生存分析。

* *何时使用：**
- 想要不同的优化目标
- 研究应用
- 标准生存SVM的替代品

```python
from sksurv.svm import MinlipSurvivalAnalysis

# Fit Minlip model
estimator = MinlipSurvivalAnalysis(alpha=1.0, random_state=42)
estimator.fit(X, y)

# Predict
risk_scores = estimator.predict(X_test)
```

## 超参数调整

### 调整Alpha （正则化）

```python
from sklearn.model_selection import GridSearchCV
from sksurv.metrics import as_concordance_index_ipcw_scorer

# Define parameter grid
param_grid = {
    'alpha': [0.1, 0.5, 1.0, 5.0, 10.0, 50.0]
}

# Grid search
cv = GridSearchCV(
    FastSurvivalSVM(),
    param_grid,
    scoring=as_concordance_index_ipcw_scorer(),
    cv=5,
    n_jobs=-1
)
cv.fit(X, y)

print(f"Best alpha: {cv.best_params_['alpha']}")
print(f"Best C-index: {cv.best_score_:.3f}")
```

### 调整内核参数

```python
from sklearn.model_selection import GridSearchCV

# Define parameter grid for kernel SVM
param_grid = {
    'alpha': [0.1, 1.0, 10.0],
    'gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 1.0]
}

# Grid search
cv = GridSearchCV(
    FastKernelSurvivalSVM(kernel='rbf'),
    param_grid,
    scoring=as_concordance_index_ipcw_scorer(),
    cv=5,
    n_jobs=-1
)
cv.fit(X, y)

print(f"Best parameters: {cv.best_params_}")
print(f"Best C-index: {cv.best_score_:.3f}")
```

## Clinical Kernel Transform

### ClinicalKernelTransform

将临床特征与分子数据相结合的特殊内核，以改进医疗应用中的预测。

* *用例：**
- 同时具有临床变量（年龄、分期等）和高维分子数据（基因表达、基因组学）
- 临床特征应具有不同的权重
- 想要集成异构数据类型

* *关键参数：**
- `fit_once`：是否一次拟合内核或在交叉验证期间重新拟合（默认值：False）
- 临床特征应与分子特征分开传递

```python
from sksurv.kernels import ClinicalKernelTransform
from sksurv.svm import FastKernelSurvivalSVM
from sklearn.pipeline import make_pipeline

# Separate clinical and molecular features
clinical_features = ['age', 'stage', 'grade']
X_clinical = X[clinical_features]
X_molecular = X.drop(clinical_features, axis=1)

# Create pipeline with clinical kernel
estimator = make_pipeline(
    ClinicalKernelTransform(),
    FastKernelSurvivalSVM()
)

# Fit model
# ClinicalKernelTransform expects tuple (clinical, molecular)
X_combined = list(zip(X_clinical.values, X_molecular.values))
estimator.fit(X_combined, y)
```

## 实际示例

### 示例1：线性SVM与交叉验证

```python
from sksurv.svm import FastSurvivalSVM
from sklearn.model_selection import cross_val_score
from sksurv.metrics import as_concordance_index_ipcw_scorer
from sklearn.preprocessing import StandardScaler

# Standardize features (important for SVMs!)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Create model
svm = FastSurvivalSVM(alpha=1.0, max_iter=100, random_state=42)

# Cross-validation
scores = cross_val_score(
    svm, X_scaled, y,
    cv=5,
    scoring=as_concordance_index_ipcw_scorer(),
    n_jobs=-1
)

print(f"Mean C-index: {scores.mean():.3f} (±{scores.std():.3f})")
```

### 示例 2：具有不同内核的内核 SVM

```python
from sksurv.svm import FastKernelSurvivalSVM
from sklearn.model_selection import train_test_split
from sksurv.metrics import concordance_index_ipcw

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Compare different kernels
kernels = ['linear', 'poly', 'rbf', 'sigmoid']
results = {}

for kernel in kernels:
    # Fit model
    svm = FastKernelSurvivalSVM(kernel=kernel, alpha=1.0, random_state=42)
    svm.fit(X_train_scaled, y_train)

    # Predict
    risk_scores = svm.predict(X_test_scaled)

    # Evaluate
    c_index = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
    results[kernel] = c_index

    print(f"{kernel:10s}: C-index = {c_index:.3f}")

# Best kernel
best_kernel = max(results, key=results.get)
print(f"\nBest kernel: {best_kernel} (C-index = {results[best_kernel]:.3f})")
```

### 示例 3：具有超参数调优的完整流水线

```python
from sksurv.svm import FastKernelSurvivalSVM
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sksurv.metrics import as_concordance_index_ipcw_scorer

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('svm', FastKernelSurvivalSVM(kernel='rbf'))
])

# Define parameter grid
param_grid = {
    'svm__alpha': [0.1, 1.0, 10.0],
    'svm__gamma': ['scale', 0.01, 0.1, 1.0]
}

# Grid search
cv = GridSearchCV(
    pipeline,
    param_grid,
    scoring=as_concordance_index_ipcw_scorer(),
    cv=5,
    n_jobs=-1,
    verbose=1
)
cv.fit(X_train, y_train)

# Best model
best_model = cv.best_estimator_
print(f"Best parameters: {cv.best_params_}")
print(f"Best CV C-index: {cv.best_score_:.3f}")

# Evaluate on test set
risk_scores = best_model.predict(X_test)
c_index = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
print(f"Test C-index: {c_index:.3f}")
```

## 重要注意事项

### 特征缩放

* *关键**：在使用 SVM 之前始终标准化特征！

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### 计算复杂度

- **FastSurvivalSVM**：每次迭代 O(n × p) - fast
- **FastKernelSurvivalSVM**：O(n² × p) - 较慢，二次缩放
- **NaiveSurvivalSVM**：O(n³) - 对于大型数据集非常慢

对于大型数据集（> 10,000 个样本），首选：
- FastSurvivalSVM （线性）
- 梯度提升
- 随机生存森林

### 当 SVM 可能不是最佳选择时

- **非常大的数据集**：集成方法更快
- **需要生存函数**：使用随机生存森林或 Cox 模型
- **需要可解释性**：使用Cox模型
- **非常高的维度**：使用惩罚Cox（Coxnet）或带有特征选择的梯度提升

## 模型选择指南

|型号|速度|非线性|可扩展性|可解释性|
|-----|--------|---------------|--------------|------------------|
|快速生存SVM |快|没有 |高|中|
| FastKernelSurvivalSVM | FastKernelSurvivalSVM | FastKernelSurvivalSVM中等|是的 |中等|低|
| HingeLossSurvivalSVM | 铰链损失生存SVM快|没有 |高|中|
|朴素生存SVM |慢|没有 |低|中等 |

* *一般建议：**
- 从 **FastSurvivalSVM** 开始作为基线
- 如果预期非线性，尝试使用 RBF **FastKernelSurvivalSVM**
- 使用网格搜索来调整 alpha 和 gamma
- 始终标准化特征
- 与随机比较生存森林和梯度提升
