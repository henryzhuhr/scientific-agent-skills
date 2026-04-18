# 用于生存分析的集成模型

## 随机生存森林

### 概述

随机生存森林将随机森林算法扩展到使用删失数据进行生存分析。他们在引导样本和聚合预测上构建多个决策树。

### 他们如何工作

1. **引导采样**：每棵树都建立在训练数据
2的不同引导样本上。 **特征随机性**：在每个节点，仅考虑特征的随机子集来进行分割
3. **生存函数估计**：在终端节点，Kaplan-Meier 和 Nelson-Aalen 估计器计算生存函数
4. **集成聚合**：最终预测所有树的平均生存函数

### 何时使用

- 特征和生存之间复杂的非线性关系
- 不需要对函数形式进行假设
- 希望通过最小的调整获得稳健的预测
- 需要特征重要性估计
- 有足够的样本量（通常n> 100)

### 关键参数

- `n_estimators`：树木数量（默认：100）
  - 更多树木=更稳定的预测，但速度更慢
  - 典型范围：100-1000

- `max_depth`：最大深度trees
  - 控制树的复杂性
  - None = 节点扩展直到pure或min_samples_split

- `min_samples_split`：分割节点的最小样本（默认值：6）
  - 较大的值=更多正则化

- `min_samples_leaf`：叶节点的最小样本（默认值： 3)
  - 防止对小群体的过度拟合

- `max_features`：每次分割时要考虑的特征数量
  - 'sqrt'：sqrt(n_features) - 良好的默认值
  - 'log2'：log2(n_features)
  - None：全部features

- `n_jobs`：并行作业数量（-1 使用所有处理器）

### 用法示例

```python
from sksurv.ensemble import RandomSurvivalForest
from sksurv.datasets import load_breast_cancer

# Load data
X, y = load_breast_cancer()

# Fit Random Survival Forest
rsf = RandomSurvivalForest(n_estimators=1000,
                           min_samples_split=10,
                           min_samples_leaf=15,
                           max_features="sqrt",
                           n_jobs=-1,
                           random_state=42)
rsf.fit(X, y)

# Predict risk scores
risk_scores = rsf.predict(X)

# Predict survival functions
surv_funcs = rsf.predict_survival_function(X)

# Predict cumulative hazard functions
chf_funcs = rsf.predict_cumulative_hazard_function(X)
```

### 功能重要性

* *重要**：基于分裂杂质的内置特征重要性对于生存数据来说并不可靠。请改用基于排列的特征重要性。

```python
from sklearn.inspection import permutation_importance
from sksurv.metrics import concordance_index_censored

# Define scoring function
def score_survival_model(model, X, y):
    prediction = model.predict(X)
    result = concordance_index_censored(y['event'], y['time'], prediction)
    return result[0]

# Compute permutation importance
perm_importance = permutation_importance(
    rsf, X, y,
    n_repeats=10,
    random_state=42,
    scoring=score_survival_model
)

# Get feature importance
feature_importance = perm_importance.importances_mean
```

## 梯度提升生存分析

### 概述

梯度提升通过顺序添加弱学习器来纠正先前学习器的错误来构建集成。模型为： **f(x) = Σ β_m g(x; θ_m)**

### 模型类型

#### GradientBoostingSurvivalAnalysis

使用回归树作为基础学习器。可以捕获复杂的非线性关系。

* *何时使用：**
- 需要对复杂的非线性关系进行建模
- 想要高预测性能
- 有足够的数据以避免过度拟合
- 可以仔细调整超参数

#### ComponentwiseGradientBoostingSurvivalAnalysis

使用分量最小二乘作为基础学习器。通过自动特征选择生成线性模型。

* *何时使用：**
- 想要可解释的线性模型
- 需要自动特征选择（如Lasso）
- 拥有高维数据
- 更喜欢稀疏模型

### 损失函数

#### Cox 的部分似然（默认）

维护比例风险框架，但用加性集成模型替换线性模型。

* *适用于：**
- 标准生存分析设置
- 当比例风险合理时
- 大多数用例

#### 加速故障时间(AFT)

假设特征以恒定因子加速或减慢生存时间。损失函数：**(1/n) Σ ω_i (log y_i - f(x_i))²**

* *适用于：**
- AFT 框架优于比例风险 
- 想要直接对时间建模
- 需要解释对生存时间的影响

### 正则化策略

防止过拟合的三大技术：

1. **Learning Rate** (`learning_rate < 1`)
   - Shrinks contribution of each base learner
   - Smaller values need more iterations but better generalization
   - Typical range: 0.01 - 0.1

2. **Dropout** (`dropout_rate > 0`)
  - 在训练期间随机删除以前的学习者
  - 强制学习者变得更加稳健
  - 典型范围：0.01 - 0.2

3. **Subsampling** (`subsample < 1`)
   - Uses random subset of data for each iteration
   - Adds randomness and reduces overfitting
   - Typical range: 0.5 - 0.9

* *Recommendation**: Combine small learning rate with early stopping for best performance.

### Key Parameters

- `loss`: Loss function ('coxph' or 'ipcwls')
- `learning_rate`: Shrinks contribution of each tree (default: 0.1)
- `n_estimators`: Number of boosting iterations (default: 100)
- `subsample`：每次迭代的样本分数（默认值：1.0）
- `dropout_rate`：学习者的辍学率（默认值：0.0）
- `max_depth`：树的最大深度（默认值：3）
- `min_samples_split`: Minimum samples to split node (default: 2)
- `min_samples_leaf`: Minimum samples at leaf (default: 1)
- `max_features`: Features to consider at each split

### Example用法

```python
from sksurv.ensemble import GradientBoostingSurvivalAnalysis
from sklearn.model_selection import train_test_split

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit gradient boosting model
gbs = GradientBoostingSurvivalAnalysis(
    loss='coxph',
    learning_rate=0.05,
    n_estimators=200,
    subsample=0.8,
    dropout_rate=0.1,
    max_depth=3,
    random_state=42
)
gbs.fit(X_train, y_train)

# Predict risk scores
risk_scores = gbs.predict(X_test)

# Predict survival functions
surv_funcs = gbs.predict_survival_function(X_test)

# Predict cumulative hazard functions
chf_funcs = gbs.predict_cumulative_hazard_function(X_test)
```

### 提前停止

使用验证集防止过拟合：

```python
from sklearn.model_selection import train_test_split

# Create train/validation split
X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Fit with early stopping
gbs = GradientBoostingSurvivalAnalysis(
    n_estimators=1000,
    learning_rate=0.01,
    max_depth=3,
    validation_fraction=0.2,
    n_iter_no_change=10,
    random_state=42
)
gbs.fit(X_tr, y_tr)

# Number of iterations used
print(f"Used {gbs.n_estimators_} iterations")
```

### 超参数调优

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'subsample': [0.8, 1.0]
}

cv = GridSearchCV(
    GradientBoostingSurvivalAnalysis(),
    param_grid,
    scoring='concordance_index_ipcw',
    cv=5,
    n_jobs=-1
)
cv.fit(X, y)

best_model = cv.best_estimator_
```

## ComponentwiseGradientBoostingSurvivalAnalysis

### Overview

Uses component-wise least squares, producing sparse linear models with automatic feature selection similar to Lasso.

### When to Use

- Want interpretable linear model
- Need automatic feature selection
- Have high-dimensional data with many irrelevant features
- Prefer coefficient-based interpretation

### Example Usage

```python
from sksurv.ensemble import ComponentwiseGradientBoostingSurvivalAnalysis

# Fit componentwise boosting
cgbs = ComponentwiseGradientBoostingSurvivalAnalysis(
    loss='coxph',
    learning_rate=0.1,
    n_estimators=100
)
cgbs.fit(X, y)

# Get selected features and coefficients
coef = cgbs.coef_
selected_features = [i for i, c in enumerate(coef) if c != 0]
```

## ExtraSurvivalTrees

极其随机的生存树 - 与随机生存森林类似，但在分割选择中具有额外的随机性。

### 何时使用

 - 想要比随机生存森林更多的正则化
  - 数据有限
  - 需要更快的训练

 ### 关键区别

它不是为选定的特征找到最佳分割，而是随机选择分割点， adding more diversity to the ensemble.

```python
from sksurv.ensemble import ExtraSurvivalTrees

est = ExtraSurvivalTrees(n_estimators=100, random_state=42)
est.fit(X, y)
```

## Model Comparison

|型号|复杂性 |可解释性|性能| Speed |
|-------|-----------|------------------|-------------|-------|
|随机生存森林 |中等|低|高|中号|
|梯度提升生存分析 |高|低|最高|慢|
| ComponentwiseGradientBoosting 生存分析 |低|高|中等|快|
|额外生存树 |中等|低|中高|快速 |

* *一般建议：**
- **最佳整体性能**：带有调整的 GradientBoostingSurvivalAnalysis
- **最佳平衡**：RandomSurvivalForest
- **最佳可解释性**：ComponentwiseGradientBoostingSurvivalAnalysis
- **最快训练**：ExtraSurvivalTrees
