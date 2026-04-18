# GRN 推理算法

Arboreto 提供了两种基因调控网络（GRN）推理算法，均基于多元回归方法。

## 算法概述

两种算法都遵循相同的推理策略：
1. 对于数据集中的每个目标基因，训练回归模型
2. 确定模型 
3 中最重要的功能（潜在的调节器）。将这些特征作为具有重要性分数的候选调节器发出

，关键区别在于**计算效率**和底层回归方法。

## GRNBoost2（推荐）

* *目的**：使用梯度提升对大规模数据集进行快速GRN推理。

### 何时使用
- **大型数据集**：数以万计的观察结果（例如，单细胞 RNA-seq）
- **时间受限的分析**：需要比 GENIE3
 更快的结果- **默认选择**：GRNBoost2 是旗舰算法，推荐用于大多数用例

### 技术详细信息
- **方法**：具有早期停止正则化的随机梯度提升
- **性能**：在大型数据集上比 GENIE3 快得多
- **输出**：与 GENIE3 格式相同（TF-目标-重要性三元组）

### 用法
```python
from arboreto.algo import grnboost2

network = grnboost2(
    expression_data=expression_matrix,
    tf_names=tf_names,
    seed=42  # For reproducibility
)
```

### 参数
```python
grnboost2(
    expression_data,           # Required: pandas DataFrame or numpy array
    gene_names=None,           # Required for numpy arrays
    tf_names='all',            # List of TF names or 'all'
    verbose=False,             # Print progress messages
    client_or_address='local', # Dask client or scheduler address
    seed=None                  # Random seed for reproducibility
)
```

## GENIE3

* *用途**：基于经典随机森林的GRN推理，作为概念蓝图。

### 何时使用
- **较小的数据集**：当数据集大小允许更长的计算时
- **比较研究**：与已发布的GENIE3结果进行比较时
- **验证**：验证GRNBoost2结果

### 技术细节
- **方法**：随机森林或额外树回归
- **基础**：原始多元回归GRN推理策略
- **权衡**：计算成本更高但完善

### 用法
```python
from arboreto.algo import genie3

network = genie3(
    expression_data=expression_matrix,
    tf_names=tf_names,
    seed=42
)
```

### 参数
```python
genie3(
    expression_data,           # Required: pandas DataFrame or numpy array
    gene_names=None,           # Required for numpy arrays
    tf_names='all',            # List of TF names or 'all'
    verbose=False,             # Print progress messages
    client_or_address='local', # Dask client or scheduler address
    seed=None                  # Random seed for reproducibility
)
```

## 算法对比

|特色| GRNBoost2 |精灵3 |
|---------|------------|--------|
| **速度** |快速（针对大数据进行了优化）|较慢|
| **方法** |梯度提升|随机森林|
| **最适合** |大规模数据（10k+ 观测值）|中小型数据集|
| **输出格式** |相同 |同|
| **推理策略** |多元回归 |多元回归|
| **推荐** |是（默认选择）|用于比较/验证 |

## 高级：自定义回归器参数

对于高级用户，传递自定义 scikit-learn 回归器参数：

```python
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

# Custom GRNBoost2 parameters
custom_grnboost2 = grnboost2(
    expression_data=expression_matrix,
    regressor_type='GBM',
    regressor_kwargs={
        'n_estimators': 100,
        'max_depth': 5,
        'learning_rate': 0.1
    }
)

# Custom GENIE3 parameters
custom_genie3 = genie3(
    expression_data=expression_matrix,
    regressor_type='RF',
    regressor_kwargs={
        'n_estimators': 1000,
        'max_features': 'sqrt'
    }
)
```

## 选择正确的算法

* *决策指南**：

1. **从 GRNBoost2 开始** - 它速度更快，可以更好地处理大型数据集
2. **使用 GENIE3 if**：
  - 与现有 GENIE3 出版物进行比较
  - 数据集为中小型 
  - 验证 GRNBoost2 结果

 两种算法都产生具有相同输出格式的可比较的调节网络，使它们可以互换用于大多数分析。
