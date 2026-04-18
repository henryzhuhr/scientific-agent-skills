# Cox 比例风险模型

## 概述

Cox 比例风险模型是将协变量与事件时间相关联的半参数模型。个体 *i* 的风险函数表示为：

* *h_i(t) = h_0(t) × exp(β^T x_i)**

 其中：
- h_0(t)是基线风险函数（未指定）
- β 是系数向量
- x_i 是个体的协变量向量*i*

关键假设是两个个体之间的风险比随着时间的推移是恒定的（比例风险）。

## CoxPHSurvivalAnalysis

用于生存分析的基本Cox比例风险模型。

### 何时使用
- 带有审查数据的标准生存分析
- 需要可解释系数（对数风险比）
- 比例风险假设成立
- 数据集具有相对较少的特征

### 关键参数
- `alpha`：正则化参数（默认值：0，无正则化）
- `ties`：处理绑定事件时间的方法（'breslow' 或 'efron'）
- `n_iter`：优化的最大迭代次数

### 示例用法
```python
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.datasets import load_gbsg2

# Load data
X, y = load_gbsg2()

# Fit Cox model
estimator = CoxPHSurvivalAnalysis()
estimator.fit(X, y)

# Get coefficients (log hazard ratios)
coefficients = estimator.coef_

# Predict risk scores
risk_scores = estimator.predict(X)
```

## CoxnetSurvivalAnalysis

Cox 模型，具有用于特征选择和弹性网络惩罚的正则化。

### 何时使用
- 高维数据（许多特征）
- 需要自动特征选择
- 想要处理多重共线性
- 需要稀疏模型

### 惩罚类型
- **岭（L2）**： alpha_min_ratio=1.0, l1_ratio=0
  - 缩小所有系数
  - 当所有特征都相关时很好

- **Lasso (L1)**: l1_ratio=1.0
  - 执行特征选择（将系数设置为零）
  - 适合稀疏models

- **弹性网络**：0 < l1_ratio < 1
  - L1和L2
的组合 - 平衡特征选择和分组

### 关键参数
- `l1_ratio`：L1和L2惩罚之间的平衡（0=Ridge，1=Lasso）
- `alpha_min_ratio`：正则化路径中最小与最大惩罚的比率
- `n_alphas`：沿正则化路径的alpha数量
- `fit_baseline_model`：是否拟合未惩罚基线模型

### 用法示例
```python
from sksurv.linear_model import CoxnetSurvivalAnalysis

# Fit with elastic net penalty
estimator = CoxnetSurvivalAnalysis(l1_ratio=0.5, alpha_min_ratio=0.01)
estimator.fit(X, y)

# Access regularization path
alphas = estimator.alphas_
coefficients_path = estimator.coef_path_

# Predict with specific alpha
risk_scores = estimator.predict(X, alpha=0.1)
```

### Alpha选择的交叉验证
```python
from sklearn.model_selection import GridSearchCV
from sksurv.metrics import concordance_index_censored

# Define parameter grid
param_grid = {'l1_ratio': [0.1, 0.5, 0.9],
              'alpha_min_ratio': [0.01, 0.001]}

# Grid search with C-index
cv = GridSearchCV(CoxnetSurvivalAnalysis(),
                  param_grid,
                  scoring='concordance_index_ipcw',
                  cv=5)
cv.fit(X, y)

# Best parameters
best_params = cv.best_params_
```

## IPCRidge

审查加权岭回归的逆概率

### 何时使用
- 优先选择加速失效时间 (AFT)框架而不是比例风险
- 需要对特征如何加速/减速生存时间进行建模
- 高审查率
- 希望使用岭罚分进行正则化

### 与 Cox 的主要区别模型 
AFT 模型假设特征将生存时间乘以常数因子，而不是乘以危险率。模型直接预测对数生存时间。

### 使用示例
```python
from sksurv.linear_model import IPCRidge

# Fit IPCRidge model
estimator = IPCRidge(alpha=1.0)
estimator.fit(X, y)

# Predict log survival time
log_time = estimator.predict(X)
```

## 模型比较和选择

### 在模型之间进行选择

* *在以下情况下使用 CoxPHSurvivalAnalysis：**
- 中小数量的特征
- 想要可解释的风险比
- 标准生存分析设置

* *在以下情况下使用Coxnet生存分析：**
- 高维数据(p >> n)
- 需要特征选择
- 想要识别重要的预测因子
- 存在多重共线性

* *在以下情况下使用 IPCRidge：**
- AFT 框架更合适
- 高审查率
- 想要直接对时间建模而不是危险

### 检查比例风险假设

应验证比例风险假设使用：
- Schoenfeld 残差
- 对数生存图
- 统计测试（在生命线等其他软件包中可用）

如果违反，请考虑：
- 通过违反协变量进行分层
- 时变系数
- 替代模型（AFT、参数模型）

## 解释

### Cox 模型系数
- 正系数：危险增加（生存期较短）
- 负系数：风险降低（生存期更长）
- 协变量增加一个单位的风险比 = exp(β)
- 示例：β=0.693 → HR=2.0（风险加倍）

### 风险评分
- 较高的风险评分 = 较高的事件风险 = 较短的预期生存期
- 风险评分是相对的；使用生存函数进行绝对预测
