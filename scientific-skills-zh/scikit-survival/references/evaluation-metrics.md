# 生存模型的评估指标

## 概述

E 评估生存模型需要考虑审查数据的专门指标。 scikit-survival 提供了三个主要类别的指标：
1. 一致性指数（C-指数）
2. 时间依赖性 ROC 和 AUC
3. Brier 评分

## 一致性指数（C 指数）

### 测量内容

一致性指数测量预测风险评分与观察到的事件时间之间的等级相关性。它表示对于随机一对受试者，模型正确排序其生存时间的概率。

* *范围**：0 到 1
- 0.5 = 随机预测
- 1.0 = 完美一致性
- 典型良好表现：0.7-0.8

### 两个实现

#### Harrell's C-index (concordance_index_censored)

传统的估计器，更简单但有局限性。

* *何时使用：**
- 低审查率 (< 40%)
- 开发过程中快速评估
- 比较同一数据集上的模型

* *限制：**
- 随着高审查率变得越来越有偏见
- 高估了从大约49%审查开始的性能

```python
from sksurv.metrics import concordance_index_censored

# Compute Harrell's C-index
result = concordance_index_censored(y_test['event'], y_test['time'], risk_scores)
c_index = result[0]
print(f"Harrell's C-index: {c_index:.3f}")
```

#### Uno的C指数(concordance_index_ipcw)

审查加权逆概率 (IPCW)估计器，可纠正审查偏差。

* *何时使用：**
- 中到高审查率 (> 40%)
- 需要无偏估计 
- 比较不同数据集的模型
- 发布结果（更稳健）

* *优点：**
- 即使在高审查的情况下也保持稳定
- 更可靠的估计
- 偏差较小

```python
from sksurv.metrics import concordance_index_ipcw

# Compute Uno's C-index
# Requires training data for IPCW calculation
c_index, concordant, discordant, tied_risk = concordance_index_ipcw(
    y_train, y_test, risk_scores
)
print(f"Uno's C-index: {c_index:.3f}")
```

### 在 Harrell 和 Uno 之间进行选择

* *在以下情况下使用 Uno 的 C 指数：**
- 审查率 > 40%
- 需要最准确的估计
- 比较不同研究的模型
- 出版研究

* *在以下情况下使用 Harrell 的 C 指数：**
- 低审查率
- 开发过程中的快速模型比较
- 计算效率至关重要

### 示例比较

```python
from sksurv.metrics import concordance_index_censored, concordance_index_ipcw

# Harrell's C-index
harrell = concordance_index_censored(y_test['event'], y_test['time'], risk_scores)[0]

# Uno's C-index
uno = concordance_index_ipcw(y_train, y_test, risk_scores)[0]

print(f"Harrell's C-index: {harrell:.3f}")
print(f"Uno's C-index: {uno:.3f}")
```

## 时间相关的 ROC 和 AUC

### 它测量什么

时间相关的 AUC 评估特定时间点的模型辨别力。它将在时间 *t* 经历事件的受试者与没有经历事件的受试者区分开来。

* *问题回答**：“模型预测谁在时间 t 时将发生事件的效果如何？”

### 何时使用

- 预测特定时间窗口内的事件发生
- 在特定时间点（例如 5 年）的临床决策生存）
- 想要评估不同时间范围内的表现
- 需要区分和计时信息

### 关键功能：cumulative_dynamic_auc

```python
from sksurv.metrics import cumulative_dynamic_auc

# Define evaluation times
times = [365, 730, 1095, 1460, 1825]  # 1, 2, 3, 4, 5 years

# Compute time-dependent AUC
auc, mean_auc = cumulative_dynamic_auc(
    y_train, y_test, risk_scores, times
)

# Plot AUC over time
import matplotlib.pyplot as plt
plt.plot(times, auc, marker='o')
plt.xlabel('Time (days)')
plt.ylabel('Time-dependent AUC')
plt.title('Model Discrimination Over Time')
plt.show()

print(f"Mean AUC: {mean_auc:.3f}")
```

### 解释

- **时间t**的AUC：概率模型正确地对具有以下特征的受试者进行排名：按时间 t 列出的事件 
- **随时间变化的 AUC**：表示模型性能随时间范围的变化
- **平均 AUC**：所有时间点上歧视的总体摘要

### 示例：比较模型

```python
# Compare two models
auc1, mean_auc1 = cumulative_dynamic_auc(y_train, y_test, risk_scores1, times)
auc2, mean_auc2 = cumulative_dynamic_auc(y_train, y_test, risk_scores2, times)

plt.plot(times, auc1, marker='o', label='Model 1')
plt.plot(times, auc2, marker='s', label='Model 2')
plt.xlabel('Time (days)')
plt.ylabel('Time-dependent AUC')
plt.legend()
plt.show()
```

## Brier Score

### 测量内容

Brier 分数通过审查将均方误差扩展到生存数据。它测量区分度（排名）和校准（预测概率的准确性）。

* *公式**：**(1/n) Σ (S(t|x_i) - I(T_i > t))²**

，其中 S(t|x_i)是受试者 i 在时间 t 的预测生存概率。

* *范围**：0 到1
- 0 = 完美预测
- 越低越好
- 典型良好性能：< 0.2

### 何时使用

- 需要校准评估（不仅仅是排名）
- 想要评估预测概率，而不仅仅是风险分数
- 比较模型输出生存函数
- 需要概率估计的临床应用

### 关键功能

#### brier_score：单个时间点

```python
from sksurv.metrics import brier_score

# Compute Brier score at specific time
time_point = 1825  # 5 years
surv_probs = model.predict_survival_function(X_test)
# Extract survival probability at time_point for each subject
surv_at_t = [fn(time_point) for fn in surv_probs]

bs = brier_score(y_train, y_test, surv_at_t, time_point)[1]
print(f"Brier score at {time_point} days: {bs:.3f}")
```

#### Integrated_brier_score：跨时间摘要

```python
from sksurv.metrics import integrated_brier_score

# Compute integrated Brier score
times = [365, 730, 1095, 1460, 1825]
surv_probs = model.predict_survival_function(X_test)

ibs = integrated_brier_score(y_train, y_test, surv_probs, times)
print(f"Integrated Brier Score: {ibs:.3f}")
```

### 解释

- **时间 t** 时的 Brier 分数**：预期平方差时间 t
- **综合 Brier 评分**：Brier 评分的加权平均值
- **较低的值 = 更好的预测**

### 与空模型的比较

始终与基线进行比较（例如， Kaplan-Meier):

```python
from sksurv.nonparametric import kaplan_meier_estimator

# Compute Kaplan-Meier baseline
time_km, surv_km = kaplan_meier_estimator(y_train['event'], y_train['time'])

# Predict with KM for each test subject
surv_km_test = [surv_km[time_km <= time_point][-1] if any(time_km <= time_point) else 1.0
                for _ in range(len(X_test))]

bs_km = brier_score(y_train, y_test, surv_km_test, time_point)[1]
bs_model = brier_score(y_train, y_test, surv_at_t, time_point)[1]

print(f"Kaplan-Meier Brier Score: {bs_km:.3f}")
print(f"Model Brier Score: {bs_model:.3f}")
print(f"Improvement: {(bs_km - bs_model) / bs_km * 100:.1f}%")
```

## 使用指标进行交叉验证

### 一致性指数评分器

```python
from sklearn.model_selection import cross_val_score
from sksurv.metrics import as_concordance_index_ipcw_scorer

# Create scorer
scorer = as_concordance_index_ipcw_scorer()

# Perform cross-validation
scores = cross_val_score(model, X, y, cv=5, scoring=scorer)
print(f"Mean C-index: {scores.mean():.3f} (±{scores.std():.3f})")
```

### 综合 Brier 评分Scorer

```python
from sksurv.metrics import as_integrated_brier_score_scorer

# Define time points for evaluation
times = np.percentile(y['time'][y['event']], [25, 50, 75])

# Create scorer
scorer = as_integrated_brier_score_scorer(times)

# Perform cross-validation
scores = cross_val_score(model, X, y, cv=5, scoring=scorer)
print(f"Mean IBS: {scores.mean():.3f} (±{scores.std():.3f})")
```

## 使用GridSearch进行模型选择CV

```python
from sklearn.model_selection import GridSearchCV
from sksurv.ensemble import RandomSurvivalForest
from sksurv.metrics import as_concordance_index_ipcw_scorer

# Define parameter grid
param_grid = {
    'n_estimators': [100, 200, 300],
    'min_samples_split': [10, 20, 30],
    'max_depth': [None, 10, 20]
}

# Create scorer
scorer = as_concordance_index_ipcw_scorer()

# Perform grid search
cv = GridSearchCV(
    RandomSurvivalForest(random_state=42),
    param_grid,
    scoring=scorer,
    cv=5,
    n_jobs=-1
)
cv.fit(X, y)

print(f"Best parameters: {cv.best_params_}")
print(f"Best C-index: {cv.best_score_:.3f}")
```

## 综合模型评估

### 推荐的评估管道

```python
from sksurv.metrics import (
    concordance_index_censored,
    concordance_index_ipcw,
    cumulative_dynamic_auc,
    integrated_brier_score
)

def evaluate_survival_model(model, X_train, X_test, y_train, y_test):
    """Comprehensive evaluation of survival model"""

    # Get predictions
    risk_scores = model.predict(X_test)
    surv_funcs = model.predict_survival_function(X_test)

    # 1. Concordance Index (both versions)
    c_harrell = concordance_index_censored(y_test['event'], y_test['time'], risk_scores)[0]
    c_uno = concordance_index_ipcw(y_train, y_test, risk_scores)[0]

    # 2. Time-dependent AUC
    times = np.percentile(y_test['time'][y_test['event']], [25, 50, 75])
    auc, mean_auc = cumulative_dynamic_auc(y_train, y_test, risk_scores, times)

    # 3. Integrated Brier Score
    ibs = integrated_brier_score(y_train, y_test, surv_funcs, times)

    # Print results
    print("=" * 50)
    print("Model Evaluation Results")
    print("=" * 50)
    print(f"Harrell's C-index:  {c_harrell:.3f}")
    print(f"Uno's C-index:      {c_uno:.3f}")
    print(f"Mean AUC:           {mean_auc:.3f}")
    print(f"Integrated Brier:   {ibs:.3f}")
    print("=" * 50)

    return {
        'c_harrell': c_harrell,
        'c_uno': c_uno,
        'mean_auc': mean_auc,
        'ibs': ibs,
        'time_auc': dict(zip(times, auc))
    }

# Use the evaluation function
results = evaluate_survival_model(model, X_train, X_test, y_train, y_test)
```

## 选择正确的指标

### 决策指南

* *在以下情况下使用C指数（Uno's）：**
- 主要目标是排名/歧视
- 不需要校准概率
- 标准生存分析设置
- 最常见的选择

* *使用时间相关AUC 何时：**
- 需要在特定时间点进行区分 
- 特定范围内的临床决策 
- 想要了解性能随时间的变化情况 

* * 使用 Brier 评分时：**
- 需要校准概率估计 
- 区分和校准都很重要 
- 需要临床决策概率
- 想要综合评估

* *最佳实践**：报告多个指标以进行综合评估。至少报告：
- Uno 的 C 指数（歧视）
- 综合 Brier 评分（歧视 + 校准）
- 临床相关时间点的时间依赖性 AUC 
