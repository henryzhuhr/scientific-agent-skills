---
name: shap
description: 使用 SHAP (SHapley Additive exPlanations)建立模型的可解释性和可解释性。在解释机器学习模型预测、计算特征重要性、生成 SHAP 图（瀑布图、蜂群图、条形图、散点图、力图、热图）、调试模型、分析模型偏差或公平性、比较模型或实现可解释的 AI 时，请使用此技能。适用于基于树的模型（XGBoost、LightGBM、随机森林）、深度学习（TensorFlow、PyTorch）、线性模型和任何黑盒模型。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# SHAP（SHapley Additive exPlanations）

## 概述

SHAP 是一种使用合作博弈论中的 Shapley 值来解释机器学习模型输出的统一方法。该技能为以下方面提供全面的指导：

- 计算任何模型类型的SHAP值
- 创建可视化以了解特征重要性
- 调试和验证模型行为
- 分析公平性和偏差
- 在生产中实现可解释的AI

SHAP适用于所有模型类型：基于树的模型（XGBoost、LightGBM、CatBoost、随机森林）、深度学习模型（TensorFlow、PyTorch、Keras）、线性模型和黑盒模型。

## 何时使用此技能

* *当用户询问时触发此技能**：
- “解释哪些特征在我的模型中最重要”
- “生成SHAP绘图”（瀑布图、蜂群图、条形图、散点图、力图、热图等）
- “为什么我的模型做出此预测？”
- “计算模型的 SHAP 值”
- “使用 SHAP 可视化特征重要性”
- “调试模型的行为”或“验证我的模型”
- “检查我的模型是否存在偏差”或“分析公平性”
- “比较模型之间的特征重要性”
- “实现可解释的人工智能”或“向我的模型添加解释”
- “了解特征交互”
- “创建模型解释仪表板”

## 快速入门指南

### 步骤1：选择正确的解释器

* *决策树**：

1. **基于树的模型？**（XGBoost、LightGBM、CatBoost、随机森林、梯度提升）
  - 使用 `shap.TreeExplainer`（快速、精确）

2. **深度神经网络？**（TensorFlow、PyTorch、Keras、CNN、RNN、Transformers）
  - 使用 `shap.DeepExplainer` 或 `shap.GradientExplainer`

3. **线性模型？**（线性/逻辑回归，GLM）
  - 使用 `shap.LinearExplainer`（极快）

4. **任何其他模型？**（SVM、自定义函数、黑盒模型）
  - 使用 `shap.KernelExplainer`（与模型无关但速度较慢）

5. **不确定？**
  - 使用 `shap.Explainer`（自动选择最佳算法）

* *有关所有解释器类型的详细信息，请参阅 `references/explainers.md`。**

### 步骤 2：计算 SHAP 值

```python
import shap

# Example with tree-based model (XGBoost)
import xgboost as xgb

# Train model
model = xgb.XGBClassifier().fit(X_train, y_train)

# Create explainer
explainer = shap.TreeExplainer(model)

# Compute SHAP values
shap_values = explainer(X_test)

# The shap_values object contains:
# - values: SHAP values (feature attributions)
# - base_values: Expected model output (baseline)
# - data: Original feature values
```

### 步骤3：可视化结果

* *用于全局理解**（整个数据集）：
```python
# Beeswarm plot - shows feature importance with value distributions
shap.plots.beeswarm(shap_values, max_display=15)

# Bar plot - clean summary of feature importance
shap.plots.bar(shap_values)
```

* *用于个人预测**：
```python
# Waterfall plot - detailed breakdown of single prediction
shap.plots.waterfall(shap_values[0])

# Force plot - additive force visualization
shap.plots.force(shap_values[0])
```

* *用于特征关系**：
```python
# Scatter plot - feature-prediction relationship
shap.plots.scatter(shap_values[:, "Feature_Name"])

# Colored by another feature to show interactions
shap.plots.scatter(shap_values[:, "Age"], color=shap_values[:, "Education"])
```

* *有关所有绘图类型的综合指南，请参阅 `references/plots.md`。**

## 核心工作流程

此技能支持多种常见工作流程。选择与当前任务匹配的工作流程。

### 工作流程 1：基本模型讲解

* *目标**：了解驱动模型预测的因素

* *步骤**：
1. 训练模型并创建适当的解释器
2. 计算测试集 
3 的 SHAP 值。生成全局重要性图（蜂群或条形图）
4. 检查顶部特征关系（散点图）
5. 解释具体预测（瀑布图）

* *示例**：
```python
# Step 1-2: Setup
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

# Step 3: Global importance
shap.plots.beeswarm(shap_values)

# Step 4: Feature relationships
shap.plots.scatter(shap_values[:, "Most_Important_Feature"])

# Step 5: Individual explanation
shap.plots.waterfall(shap_values[0])
```

### 工作流程2：模型调试

* *目标**：识别并修复模型问题

* *步骤**：
1. 计算 SHAP 值 
2. 识别预测错误
3. 解释错误分类的样本
4. 检查意外的特征重要性（数据泄漏）
5. 验证特征关系是否有意义
6. 检查功能交互

* *请参阅`references/workflows.md`了解详细的调试工作流程。**

### 工作流程3：功能工程

* *目标**：使用SHAP见解来改进功能

* *步骤**：
1. 计算基线模型 
2 的 SHAP 值。识别非线性关系（候选变换）
3. 识别特征交互（交互项的候选）
4. 工程师新功能
5. 重新训练并比较 SHAP 值 
6. 验证改进

* *请参阅 `references/workflows.md` 了解详细的特征工程工作流程。**

### 工作流程 4：模型比较

* *目标**：比较多个模型以选择最佳可解释选项

* *步骤**：
1. 训练多个模型
2. 计算每个 
3 的 SHAP 值。比较全局特征重要性
4. 检查特征排名的一致性
5. 分析模型 
6 的具体预测。根据准确性、可解释性和一致性进行选择

* *请参阅 `references/workflows.md` 了解详细的模型比较工作流程。**

### 工作流程 5：公平性和偏差分析

* *目标**：检测和分析跨人口统计群体的模型偏差

* *步骤**：
1. 识别受保护的属性（性别、种族、年龄等）
2. 计算 SHAP 值 
3. 比较各组的特征重要性
4. 检查受保护属性SHAP重要性
5. 识别代理特征
6. 如果发现偏差，请实施缓解策略

* *请参阅`references/workflows.md`了解详细的公平性分析工作流程。**

### 工作流程6：生产部署

* *目标**：将SHAP解释集成到生产系统中

* *步骤**：
1. 训练并保存模型
2. 创建并保存解释器
3. 搭建解释服务
4. 使用解释创建用于预测的 API 端点
5. 实现缓存和优化
6. 监控说明质量

* *请参阅 `references/workflows.md` 了解详细的生产部署工作流程。**

## 关键概念

### SHAP 值

* *定义**：SHAP 值量化每个特征对预测的贡献，以与预期模型输出的偏差来衡量（基线）。

* *属性**：
- **可加性**：SHAP 值总和为预测与基线之间的差异
- **公平性**：基于博弈论中的 Shapley 值
- **一致性**：如果某个功能变得更重要，则其 SHAP 值增加

* *解释**：
- 正 SHAP 值 → 特征将预测推高 
- 负 SHAP 值 → 特征将预测推低 
- 幅度 → 特征影响强度 
- SHAP 值的总和 → 总预测变化基线

* *示例**：
```
Baseline (expected value): 0.30
Feature contributions (SHAP values):
  Age: +0.15
  Income: +0.10
  Education: -0.05
Final prediction: 0.30 + 0.15 + 0.10 - 0.05 = 0.50
```

### 背景数据/基线

* *目的**：表示建立基线期望的“典型”输入

* *选择**：
- 来自训练数据的随机样本（50-1000）样本）
- 或使用kmeans选择代表性样本
- 对于DeepExplainer/KernelExplainer：100-1000个样本平衡精度和速度

* *影响**：基线影响SHAP值大小但不影响相对重要性

### 模型输出类型

* *关键考虑因素**：了解模型输出的内容

- **原始输出**：用于回归或树边距
- **概率**：用于分类概率
- **对数赔率**：用于逻辑回归（在sigmoid之前）

* *示例**：XGBoost分类器解释边距默认情况下输出（对数赔率）。要解释概率，请在 TreeExplainer 中使用 `model_output="probability"`。

## 常见模式

### 模式 1：完整模型分析

```python
# 1. Setup
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

# 2. Global importance
shap.plots.beeswarm(shap_values)
shap.plots.bar(shap_values)

# 3. Top feature relationships
top_features = X_test.columns[np.abs(shap_values.values).mean(0).argsort()[-5:]]
for feature in top_features:
    shap.plots.scatter(shap_values[:, feature])

# 4. Example predictions
for i in range(5):
    shap.plots.waterfall(shap_values[i])
```

### 模式 2：群组比较

```python
# Define cohorts
cohort1_mask = X_test['Group'] == 'A'
cohort2_mask = X_test['Group'] == 'B'

# Compare feature importance
shap.plots.bar({
    "Group A": shap_values[cohort1_mask],
    "Group B": shap_values[cohort2_mask]
})
```

### 模式3：调试错误

```python
# Find errors
errors = model.predict(X_test) != y_test
error_indices = np.where(errors)[0]

# Explain errors
for idx in error_indices[:5]:
    print(f"Sample {idx}:")
    shap.plots.waterfall(shap_values[idx])

    # Investigate key features
    shap.plots.scatter(shap_values[:, "Suspicious_Feature"])
```

## 性能优化

### 速度注意事项

* *解释器速度**（最快到最慢）：
1. `LinearExplainer` - Nearly instantaneous
2. `TreeExplainer` - 非常快
3. `DeepExplainer` - Fast for neural networks
4. `GradientExplainer` - Fast for neural networks
5. `KernelExplainer` - Slow (use only when necessary)
6. `PermutationExplainer` - 非常慢但准确

### 优化策略

* *对于大型数据集**：
```python
# Compute SHAP for subset
shap_values = explainer(X_test[:1000])

# Or use batching
batch_size = 100
all_shap_values = []
for i in range(0, len(X_test), batch_size):
    batch_shap = explainer(X_test[i:i+batch_size])
    all_shap_values.append(batch_shap)
```

* *对于可视化**：
```python
# Sample subset for plots
shap.plots.beeswarm(shap_values[:1000])

# Adjust transparency for dense plots
shap.plots.scatter(shap_values[:, "Feature"], alpha=0.3)
```

* *对于 Production**:
```python
# Cache explainer
import joblib
joblib.dump(explainer, 'explainer.pkl')
explainer = joblib.load('explainer.pkl')

# Pre-compute for batch predictions
# Only compute top N features for API responses
```

## Troubleshooting

### 问题：错误的解释器选择
* *问题**：对树模型使用 KernelExplainer（缓慢且不必要）
* *解决方案**：对于基于树的模型始终使用 TreeExplainer

### 问题：背景数据不足
* *问题**：DeepExplainer/KernelExplainer 背景太少样本
* *解决方案**：使用100-1000个代表性样本

### 问题：令人困惑的单位
* *问题**：将对数赔率解释为概率
* *解决方案**：检查模型输出类型；了解值是概率、对数赔率还是原始输出

### 问题：绘图不显示
* *问题**：Matplotlib 后端问题
* *解决方案**：确保后端设置正确；如果需要，请使用 `plt.show()`

### 问题：太多特征使绘图混乱
* *问题**：默认 max_display=10 可能太多或太少
* *解决方案**：调整 `max_display` 参数或使用特征聚类

### 问题：慢计算
* *问题**：为非常大的数据集计算SHAP
* *解决方案**：采样子集，使用批处理，或确保使用专门的解释器（不是KernelExplainer）

## 与其他工具集成

### Jupyter Notebooks
- 交互式力图工作无缝
- 使用`show=True`（默认）进行内联绘图显示
- 与Markdown结合进行叙述解释

### MLflow /实验跟踪
```python
import mlflow

with mlflow.start_run():
    # Train model
    model = train_model(X_train, y_train)

    # Compute SHAP
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_test)

    # Log plots
    shap.plots.beeswarm(shap_values, show=False)
    mlflow.log_figure(plt.gcf(), "shap_beeswarm.png")
    plt.close()

    # Log feature importance metrics
    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
    for feature, importance in zip(X_test.columns, mean_abs_shap):
        mlflow.log_metric(f"shap_{feature}", importance)
```

### 生产API
```python
class ExplanationService:
    def __init__(self, model_path, explainer_path):
        self.model = joblib.load(model_path)
        self.explainer = joblib.load(explainer_path)

    def predict_with_explanation(self, X):
        prediction = self.model.predict(X)
        shap_values = self.explainer(X)

        return {
            'prediction': prediction[0],
            'base_value': shap_values.base_values[0],
            'feature_contributions': dict(zip(X.columns, shap_values.values[0]))
        }
```

## 参考文档

此技能包括按主题组织的综合参考文档：

### references/explainers.md
所有解释器类的完整指南：
- `TreeExplainer` - 基于树的模型的快速、准确的解释
- `DeepExplainer` - 深度学习模型（TensorFlow、PyTorch）
- `KernelExplainer` - 模型无关（适用于任何模型）
- `LinearExplainer` - 线性模型的快速解释
- `GradientExplainer` - 基于梯度的神经网络
- `PermutationExplainer` - 对于任何模型精确但缓慢

包括：构造函数参数、方法、支持的模型、何时使用、示例、性能注意事项.

### 引用/图.md
综合可视化指南：
- **瀑布图** - 个体预测细分
- **蜂群图** - 值分布的全局重要性
- **条形图** - 清晰的特征重要性摘要
- **散点图** -特征预测关系和交互
- **力图** - 交互式附加力可视化
- **热图** - 多样本比较网格
- **小提琴图** - 以分布为中心的替代方案
- **决策图** - 多类预测路径

包括：参数、用例、示例、最佳实践、图选择指南。

### 参考/工作流程.md
详细工作流程和最佳实践：
- 基本模型讲解工作流程
- 模型调试与验证
- 特征工程指导
- 模型比较与选择
- 公平与偏差分析
- 深度学习模型讲解
- 生产部署
- 时间序列模型讲解
- 常见陷阱和解决方案
- 高级技术
- MLOps 集成

 包括：分步说明、代码示例、决策标准、故障排除.

### 参考文献/theory.md
理论基础：
- 来自博弈论的Shapley值
- 数学公式和属性
- 与其他解释方法（LIME、DeepLIFT等）的连接
- SHAP计算算法（Tree SHAP、Kernel） SHAP等）
- 条件期望和基线选择
- 解释SHAP值
- 交互值
- 理论限制和考虑

包括：数学基础、证明、比较、高级主题。

## 用法指南

* *何时加载参考文件**：
- 当用户需要有关特定解释器类型或参数的详细信息时加载`explainers.md`
- 当用户需要详细的可视化指导或探索绘图选项时加载`plots.md`
- 当用户具有复杂的多步骤任务（调试、公平性）时加载`workflows.md` 
- 当用户询问理论基础、Shapley 值或数学细节时加载 `theory.md`

* *默认方法**（不加载参考）：
- 使用此 SKILL.md 进行基本解释和快速入门
- 提供标准工作流程和通用模式
- 参考文件如果需要更多详细信息，可以使用

* *加载参考**：
```python
# To load reference files, use the Read tool with appropriate file path:
# /path/to/shap/references/explainers.md
# /path/to/shap/references/plots.md
# /path/to/shap/references/workflows.md
# /path/to/shap/references/theory.md
```

## 最佳实践摘要

1. **选择正确的解释器**：尽可能使用专门的解释器（TreeExplainer、DeepExplainer、LinearExplainer）；除非必要，否则避免使用 KernelExplainer

2. **从全局开始，然后转向本地**：从蜂群图/条形图开始进行整体了解，然后深入研究瀑布图/散点图以了解详细信息

3. **使用多种可视化**：不同的图揭示不同的见解；结合全局（蜂群）+局部（瀑布）+关系（分散）视图

4. **选择适当的背景数据**：使用训练数据中的50-1000个代表性样本

5. **了解模型输出单位**：了解是否解释概率、对数赔率或原始输出

6. **使用领域知识进行验证**：SHAP 显示模型行为；使用领域专业知识来解释和验证

7. **优化性能**：用于可视化的示例子集、大型数据集的批处理、生产中的缓存解释器

8. **检查数据泄漏**：意外的高特征重要性可能表明数据质量问题

9. **考虑特征相关性**：使用 TreeExplainer 的相关性感知选项或特征聚类来获取冗余特征 

10. **记住SHAP显示关联，而不是因果关系**：使用领域知识进行因果解释

## 安装

```bash
# Basic installation
uv pip install shap

# With visualization dependencies
uv pip install shap matplotlib

# Latest version
uv pip install -U shap
```

* *依赖项**：numpy，pandas，scikit-learn，matplotlib，scipy

* *可选**： xgboost、lightgbm、tensorflow、torch（取决于模型类型）

## 其他资源

- **官方文档**：https://shap.readthedocs.io/
- **GitHub 存储库**：https://github.com/slundberg/shap
- **原始论文**：Lundberg & Lee (2017) - “解释模型预测的统一方法”
- **《自然 MI 论文》**：Lundberg 等人。 （2020）-“通过可解释的树木人工智能从局部解释到全局理解”

此技能提供了 SHAP 的全面覆盖，以实现跨所有用例和模型类型的模型可解释性。
