# SHAP 解释器参考

本文档提供有关所有 SHAP 解释器类、其参数、方法以及何时使用每种类型的全面信息。

## 概述

SHAP 为不同模型类型提供专门的解释器，每个模型都针对特定架构进行了优化。一般`shap.Explainer`类会根据模型类型自动选择合适的算法。

## 核心解释器类

### shap.Explainer（自动选择器）

* *目的**：通过选择最合适的解释器，自动使用Shapley值来解释任何机器学习模型或Python函数algorithm.

* *构造函数参数**：
- `model`：要解释的模型（函数或模型对象）
- `masker`：用于特征操作的背景数据或掩码对象
- `algorithm`：可选覆盖以强制特定解释器类型
- `output_names`：模型输出的名称
- `feature_names`：输入特征的名称

* *何时使用**：不确定使用哪个解释器时的默认选择；根据模型类型自动选择最佳算法。

### TreeExplainer

* *目的**：使用 Tree SHAP 算法快速准确地计算基于树的集成模型的 SHAP 值。

* *构造函数参数**：
- `model`：基于树的模型（XGBoost、LightGBM、CatBoost、PySpark或scikit-learn树） 
- `data`：用于特征集成的后台数据集（可选与tree_path_dependent） 
- `feature_perturbation`：如何处理依赖features
  - `"interventional"`：需要后台数据；遵循因果推理规则
  - `"tree_path_dependent"`：无需背景数据；每个叶子使用训练示例
  - `"auto"`：如果提供数据，则默认为干预，否则为tree_path_dependent
- `model_output`：解释什么模型输出
  - `"raw"`：标准模型输出（默认）
  - `"probability"`：概率转换输出
  - `"log_loss"`：损失函数的自然对数
  - 自定义方法名称，如`"predict_proba"`
- `feature_names`：可选特征命名

  * *支持的模型**：
- XGBoost (xgboost.XGBClassifier, xgboost.XGBRegressor, xgboost.Booster)
- LightGBM (lightgbm.LGBMClassifier, lightgbm.LGBMRegressor, lightgbm.Booster)
- CatBoost (catboost.CatBoostClassifier, catboost.CatBoostRegressor)
- PySpark MLlib 树模型
- scikit-learn（DecisionTreeClassifier、DecisionTreeRegressor、RandomForestClassifier、RandomForestRegressor、ExtraTreesClassifier、ExtraTreesRegressor、GradientBoostingClassifier、GradientBoostingRegressor）

* *关键方法**：
- `shap_values(X)`：计算样本的 SHAP 值；返回数组，其中每行代表特征属性
- `shap_interaction_values(X)`：估计特征对之间的交互效果；提供具有主效应和成对相互作用的矩阵
- `explain_row(row)`：用​​详细的归因信息解释各个行

* *何时使用**：
- 所有基于树的模型的主要选择
- 当需要精确的 SHAP 值（而不是近似值）时 
- 当计算速度对于大型数据集很重要时 
- 对于随机森林、梯度提升或XGBoost

* *示例**：
```python
import shap
import xgboost

# Train model
model = xgboost.XGBClassifier().fit(X_train, y_train)

# Create explainer
explainer = shap.TreeExplainer(model)

# Compute SHAP values
shap_values = explainer.shap_values(X_test)

# Compute interaction values
shap_interaction = explainer.shap_interaction_values(X_test)
```

### DeepExplainer

* *用途**：使用 DeepLIFT 算法的增强版近似深度学习模型的 SHAP 值。

* *构造函数参数**：
- `model`：依赖于框架的规范
  - **TensorFlow**：（input_tensor，output_tensor）的元组，其中输出是单维的
  - **PyTorch**：`nn.Module`对象或`(model, layer)`的元组，用于特定于层的解释
- `data`：用于特征集成的后台数据集
  - **TensorFlow**：numpy 数组或 pandas DataFrames
  - **PyTorch**：火炬张量
  - **推荐大小**：100-1000 个样本（不是完整的训练集）以平衡准确性和计算成本
- `session`（仅限 TensorFlow）：可选会话对象；如果没有，则自动检测
- `learning_phase_flags`：用于在推理过程中处理批量规范/丢失的自定义学习阶段张量

  * *支持的框架**：
- **TensorFlow **：完全支持，包括Keras模型
- **PyTorch **：与nn.Module完全集成架构

* *关键方法**：
- `shap_values(X)`：返回应用于数据的模型的近似SHAP值 X
- `explain_row(row)`：解释具有属性值和预期输出的单行
- `save(file)` / `load(file)`：解释器对象的序列化支持
- `supports_model_with_masker(model, masker)`：模型类型的兼容性检查器

* *何时使用**：
- 用于 TensorFlow 或 PyTorch 中的深度神经网络
- 使用卷积神经网络 (CNN)时
- 用于循环神经网络 (RNN)和转换器 
- 当深度学习架构需要特定于模型的解释时

* *关键设计功能**：
 的方差期望估计值大约为 1/√N，其中 N 是背景样本的数量，从而实现准确性与效率的权衡。

* *示例**：
```python
import shap
import tensorflow as tf

# Assume model is a Keras model
model = tf.keras.models.load_model('my_model.h5')

# Select background samples (subset of training data)
background = X_train[:100]

# Create explainer
explainer = shap.DeepExplainer(model, background)

# Compute SHAP values
shap_values = explainer.shap_values(X_test[:10])
```

### KernelExplainer

* *目的**：使用内核进行与模型无关的 SHAP 值计算SHAP 加权线性回归方法。

* *构造函数参数**：
- `model`：采用样本矩阵并返回模型输出的函数或模型对象
- `data`：用于模拟缺失的背景数据集（numpy 数组、pandas DataFrame 或稀疏矩阵） features
- `feature_names`：可选的功能名称列表；如果可用，自动从 DataFrame 列名称派生
- `link`：特征重要性和模型输出之间的连接函数
  - `"identity"`：直接关系（默认）
  - `"logit"`：对于概率输出

* *关键方法**：
- `shap_values(X, **kwargs)`：计算样本预测的 SHAP 值
  - `nsamples`：每个预测的评估计数（“自动”或整数）；较高的值减少方差
  - `l1_reg`：特征选择正则化（“num_features（int）”，“aic”，“bic”或float）
  - 返回每行总和为模型输出与预期值之间的差值的数组
- `explain_row(row)`：解释具有归因值和预期的单个预测value
- `save(file)` / `load(file)`：保留并恢复解释器对象

* *何时使用**：
- 对于无法使用专门解释器的黑盒模型
- 使用自定义预测函数时
- 对于任何模型类型（神经网络、SVM、集成方法等）
- 当需要与模型无关的解释时
- **注意**：比专门解释器慢；仅当不存在专门选项时使用

* *示例**：
```python
import shap
from sklearn.svm import SVC

# Train model
model = SVC(probability=True).fit(X_train, y_train)

# Create prediction function
predict_fn = lambda x: model.predict_proba(x)[:, 1]

# Select background samples
background = shap.sample(X_train, 100)

# Create explainer
explainer = shap.KernelExplainer(predict_fn, background)

# Compute SHAP values (may be slow)
shap_values = explainer.shap_values(X_test[:10])
```

### LinearExplainer

* *目的**：解释特征相关性的线性模型的专用解释器。

* *构造函数参数**：
- `model`：线性（系数、截距）的模型或元组 
- `masker`：特征相关性的背景数据
- `feature_perturbation`：如何处理特征相关性
  - `"interventional"`：假设特征独立性
  - `"correlation_dependent"`：特征的说明相关性

* *支持的模型**：
- scikit-learn 线性模型（LinearRegression、LogisticRegression、Ridge、Lasso、ElasticNet）
- 具有系数和截距的自定义线性模型

* *何时使用**：
- 用于线性回归和逻辑回归模型
- 当特征相关性对于解释准确性很重要时
- 当需要极快的解释时
- 对于GLM和其他线性模型类型

* *示例**：
```python
import shap
from sklearn.linear_model import LogisticRegression

# Train model
model = LogisticRegression().fit(X_train, y_train)

# Create explainer
explainer = shap.LinearExplainer(model, X_train)

# Compute SHAP values
shap_values = explainer.shap_values(X_test)
```

### GradientExplainer

* *用途**：使用预期梯度来近似神经网络的 SHAP 值。

* *构造函数参数**：
- `model`：深度学习模型（TensorFlow 或 PyTorch）
- `data`：背景样本积分
- `batch_size`：梯度计算的批量大小
- `local_smoothing`：为平滑添加的噪声量（默认0）

* *何时使用**：
- 作为神经网络DeepExplainer的替代品
- 当基于梯度的解释时优选
- 适用于梯度信息可用的可微分模型

* *示例**：
```python
import shap
import torch

# Assume model is a PyTorch model
model = torch.load('model.pt')

# Select background samples
background = X_train[:100]

# Create explainer
explainer = shap.GradientExplainer(model, background)

# Compute SHAP values
shap_values = explainer.shap_values(X_test[:10])
```

### PermutationExplainer

* *目的**：通过迭代输入的排列来近似Shapley值。

* *构造函数参数**：
- `model`：预测函数
- `masker`：背景数据或掩蔽对象
- `max_evals`：每个样本的最大模型评估数量

* *何时使用**：
- 当需要精确的Shapley值但没有专门的解释器时
- 对于排列是的小特征集tractable
- 作为 KernelExplainer 的更准确替代品（但速度较慢）

* *示例**：
```python
import shap

# Create explainer
explainer = shap.PermutationExplainer(model.predict, X_train)

# Compute SHAP values
shap_values = explainer.shap_values(X_test[:10])
```

## 解释器选择指南

* *用于选择解释器的决策树**：

1. **您的模型是基于树的吗？**（XGBoost、LightGBM、CatBoost、随机森林等）
  - 是 → 使用 `TreeExplainer`（快速且准确）
  - 否 → 继续步骤 2

2. **您的模型是深度神经网络吗？**（TensorFlow、PyTorch、Keras）
  - 是 → 使用 `DeepExplainer` 或 `GradientExplainer`
  - 否 → 继续执行步骤 3

3. **您的模型是线性的吗？**（线性/逻辑回归，GLM）
  - 是 → 使用 `LinearExplainer`（极快）
  - 否 → 继续步骤 4

4. **您需要与模型无关的解释吗？**
  - 是→使用`KernelExplainer`（速度较慢，但​​适用于任何模型）
  - 如果计算预算允许且需要高精度→使用`PermutationExplainer`

5. **不确定或想要自动选择？**
  - 使用 `shap.Explainer`（自动选择最佳算法）

## 解释器之间的通用参数

* *背景数据/掩码**：
- 目的：表示建立基线期望的“典型”输入
- 大小建议：50-1000样本（复杂模型更多）
- 选择：来自训练数据或kmeans选择的代表的随机样本

* *特征名称**：
- 从pandas DataFrames自动提取
- 可以为numpy数组手动指定
- 对于绘图可解释性很重要

* *模型输出规范**：
- 原始模型输出与转换输出（概率，对数赔率）
- 对于正确解释至关重要SHAP 值
- 示例：对于 XGBoost 分类器，SHAP 解释逻辑转换之前的边际输出（对数赔率）

## 性能注意事项

* *速度排名**（最快到最慢）：
1. `LinearExplainer` - 几乎瞬时
2. `TreeExplainer` - 速度非常快，扩展性良好
3. `DeepExplainer` - 快速神经网络
4. `GradientExplainer` - 快速神经网络
5. `KernelExplainer` - 慢，仅在必要时使用
6. `PermutationExplainer` - 非常慢，但对于小型功能集来说最准确

* *内存注意事项**：
- `TreeExplainer`：内存开销低
- `DeepExplainer`：内存与背景样本大小成正比
- `KernelExplainer`：对于大型功能集可能是内存密集型的背景数据集
- 对于大型数据集：使用批处理或样本子集

## 解释器输出：解释对象

所有解释器返回包含以下内容的`shap.Explanation` 对象：
- `values`：SHAP 值（numpy 数组）
- `base_values`：预期模型输出（基线）
- `data`：原始特征值
- `feature_names`：特征名称

解释对象支持：
- 切片：`explanation[0]`为第一个样本
- 数组操作：与numpy操作兼容
- 直接绘图：可以传递给绘图函数
