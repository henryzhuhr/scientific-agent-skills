# SHAP 可视化参考

本文档提供了有关所有 SHAP 绘图函数、其参数、用例以及可视化模型解释的最佳实践的全面信息。

## 概述

SHAP 提供了多种可视化工具，用于解释单个和全局级别的模型预测。每种绘图类型在理解特征重要性、交互作用和预测机制方面都有特定的用途。

## 绘图类型

### 瀑布图

* *目的**：显示各个预测的说明，显示每个特征如何将预测从基线（预期值）移向最终预测。

* *功能**： `shap.plots.waterfall(explanation, max_display=10, show=True)`

* *关键参数**：
- `explanation`：解释对象中的单行（不是多个样本）
- `max_display`：要显示的特征数量（默认值：10）；影响较小的特征折叠成单个“其他特征”术语
- `show`：是否立即显示绘图

* *视觉元素**：
- **X轴**：显示SHAP值（对预测的贡献）
- **起点**：模型的预期值（基线）
- **特征贡献**：红色条（正）或蓝色条（负）显示每个特征如何移动预测
- **特征值**：以灰色显示在特征名称左侧
- **终点**：最终模型预测

* *何时使用**：
- 解释中的各个预测详细信息
- 了解哪些功能推动了特定决策
- 传达单个实例的模型行为（例如贷款拒绝、诊断）
- 调试意外预测

* *重要说明**：
- 对于 XGBoost 分类器，预测以对数赔率单位进行解释（逻辑变换之前的保证金输出）
- SHAP 值总和为基线和最终预测之间的差异（可加性属性）
- 使用散点图和瀑布图来探索多个模型之间的模式样本

* *示例**：
```python
import shap

# Compute SHAP values
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

# Plot waterfall for first prediction
shap.plots.waterfall(shap_values[0])

# Show more features
shap.plots.waterfall(shap_values[0], max_display=20)
```

### Beeswarm Plots

* *目的**：主要特征如何影响整个数据集中模型输出的信息密集摘要，将特征重要性与值分布相结合。

* *函数**： `shap.plots.beeswarm(shap_values, max_display=10, order=Explanation.abs.mean(0), color=None, show=True)`

* *关键参数**：
- `shap_values`：包含多个样本的解释对象
- `max_display`：要显示的特征数量（默认：10）
- `order`：如何对特征进行排名
  - `Explanation.abs.mean(0)`：平均绝对 SHAP 值（默认）
  - `Explanation.abs.max(0)`：最大绝对值（突出显示异常值影响）
- `color`：matplotlib 颜色图；默认为红蓝方案
- `show`：是否立即显示绘图

* *视觉元素**：
- **Y轴**：按重要性排名的特征
- **X轴**：SHAP值（对模型输出的影响）
- **每个点**：数据集中的单个实例
- **点位置 (X)**：SHAP 值大小
- **点颜色**：原始特征值（红色 = 高，蓝色 = 低）
- **点聚类**：显示影响的密度/分布

  * *何时使用**：
- 总结整个数据集中的特征重要性
- 了解平均和个体特征影响
- 识别特征值模式及其影响
- 比较跨特征的全局模型行为
- 检测非线性关系（例如，较高年龄→较低收入可能性）

* *实用变体**：
```python
# Standard beeswarm plot
shap.plots.beeswarm(shap_values)

# Show more features
shap.plots.beeswarm(shap_values, max_display=20)

# Order by maximum absolute values (highlight outliers)
shap.plots.beeswarm(shap_values, order=shap_values.abs.max(0))

# Plot absolute SHAP values with fixed coloring
shap.plots.beeswarm(shap_values.abs, color="shap_red")

# Custom matplotlib colormap
shap.plots.beeswarm(shap_values, color=plt.cm.viridis)
```

### 条形图

* *目的**：将特征重要性显示为平均绝对 SHAP 值，提供全局特征影响的清晰、简单的可视化。

* *功能**：`shap.plots.bar(shap_values, max_display=10, clustering=None, clustering_cutoff=0.5, show=True)`

* *关键参数**：
- `shap_values`：解释对象（可以是单个实例、全局或群组）
- `max_display`：要显示的最大特征/条数
- `clustering`：来自 `shap.utils.hclust`
- `clustering_cutoff` 的可选层次聚类对象：显示聚类结构的阈值（0-1，默认值：0.5）

* *绘图类型**：

#### 全局条形图
显示所有样本的整体特征重要性。重要性计算为平均绝对 SHAP 值。

```python
# Global feature importance
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)
shap.plots.bar(shap_values)
```

#### 局部条形图
显示单个实例的 SHAP 值，其中特征值以灰色显示。

```python
# Single prediction explanation
shap.plots.bar(shap_values[0])
```

#### 群组条形图绘图
通过传递解释对象的字典来比较子组之间的特征重要性。

```python
# Compare cohorts
cohorts = {
    "Group A": shap_values[mask_A],
    "Group B": shap_values[mask_B]
}
shap.plots.bar(cohorts)
```

* *特征聚类**：
使用基于模型的聚类识别冗余特征（比基于相关性更准确） 

```python
# Add feature clustering
clustering = shap.utils.hclust(X_train, y_train)
shap.plots.bar(shap_values, clustering=clustering)

# Adjust clustering display threshold
shap.plots.bar(shap_values, clustering=clustering, clustering_cutoff=0.3)
```

* *何时使用**：
- 全局特征重要性的快速概述
- 跨群组或模型比较特征重要性
- 识别冗余或相关特征
- 干净、简单的演示可视化

### 强制图

* *目的**：附加力可视化显示特征如何将预测从基线推高（红色）或降低（蓝色）。

* *功能**：`shap.plots.force(base_value, shap_values, features, feature_names=None, out_names=None, link="identity", matplotlib=False, show=True)`

* *关键参数**：
- `base_value`：期望值（基线预测）
- `shap_values`：样本的 SHAP 值 
- `features`：样本的特征值 
- `feature_names`：可选特征名称
- `link`：变换函数（“identity”或"logit")
- `matplotlib`：使用 matplotlib 后端（默认：交互式 JavaScript）

* *视觉元素**：
- **基线**：开始预测（预期值）
- **红色箭头**：将预测推高的特征
- **蓝色箭头**：将预测推低的特征
- **最终值**：结果预测

* *交互特征**（JavaScript 模式）：
- 悬停查看详细特征信息
- 多个样本创建堆叠可视化
- 可以旋转不同的视角

* *何时使用**：
- 预测的交互式探索
- 同时可视化多个预测
- 需要交互元素的演示
- 了解预测组合lance

* *示例**：
```python
# Single prediction force plot
shap.plots.force(
    shap_values.base_values[0],
    shap_values.values[0],
    X_test.iloc[0],
    matplotlib=True
)

# Multiple predictions (interactive)
shap.plots.force(
    shap_values.base_values,
    shap_values.values,
    X_test
)
```

### 散点图（相关图）

* *目的**：显示特征值与其SHAP值之间的关系，揭示特征值如何影响预测。

* *功能**： `shap.plots.scatter(shap_values, color=None, hist=True, alpha=1, show=True)`

* *关键参数**：
- `shap_values`：解释对象，可以指定带下标的特征（例如，`shap_values[:, "Age"]`） 
- `color`：用于着色点的特征（字符串名称或解释）对象）
- `hist`：在 y 轴上显示特征值的直方图
- `alpha`：点透明度（对于密集图有用）

* *视觉元素**：
- **X轴**：特征值
- **Y轴**： SHAP 值（对预测的影响）
- **点颜色**：另一个特征的值（用于交互检测）
- **直方图**：特征值的分布

* *何时使用**：
- 理解特征预测关系
- 检测非线性效应
- 识别特征交互
- 验证或发现模型行为中的模式
- 从瀑布图中探索反直觉的预测

* *交互检测**：
通过另一个特征的颜色点来揭示交互。

```python
# Basic dependence plot
shap.plots.scatter(shap_values[:, "Age"])

# Color by another feature to show interactions
shap.plots.scatter(shap_values[:, "Age"], color=shap_values[:, "Education"])

# Multiple features in one plot
shap.plots.scatter(shap_values[:, ["Age", "Education", "Hours-per-week"]])

# Increase transparency for dense data
shap.plots.scatter(shap_values[:, "Age"], alpha=0.5)
```

### 热图地块

* *用途**：同时可视化多个样本的SHAP值，显示跨实例的特征影响。

* *功能**：`shap.plots.heatmap(shap_values, instance_order=None, feature_values=None, max_display=10, show=True)`

* *关键参数**：
- `shap_values`：解释对象
- `instance_order`：如何订购实例（可以是自定义排序的说明对象）
- `feature_values`：悬停时显示特征值
- `max_display`：要显示的最大特征

* *视觉元素**：
- **行**：单个实例/样本
- **列**：特征
- **单元格颜色**：SHAP 值（红色 = 正值，蓝色 = 负值）
- **强度**：影响大小

* *何时使用**：
- 比较多个实例之间的解释
- 识别功能影响中的模式
- 了解哪些功能在不同实例中差异最大预测
- 检测具有相似解释模式的子组或簇

* *示例**：
```python
# Basic heatmap
shap.plots.heatmap(shap_values)

# Order instances by model output
shap.plots.heatmap(shap_values, instance_order=shap_values.sum(1))

# Show specific subset
shap.plots.heatmap(shap_values[:100])
```

### 小提琴图

* *目的**：与蜂群图类似，但使用小提琴（内核密度）可视化而不是单独的dots.

* *功能**：`shap.plots.violin(shap_values, features=None, feature_names=None, max_display=10, show=True)`

* *何时使用**：
- 当数据集非常大时替代蜂群
- 强调各个点的分布密度
- 更清晰的可视化演示文稿

* *示例**：
```python
shap.plots.violin(shap_values)
```

### 决策图

* *目的**：通过累积SHAP值显示预测路径，对于多类分类特别有用。

* *功能**： `shap.plots.decision(base_value, shap_values, features, feature_names=None, feature_order="importance", highlight=None, link="identity", show=True)`

* *关键参数**：
- `base_value`：期望值
- `shap_values`：样本的SHAP值
- `features`：特征值
- `feature_order`：如何排序特征（“重要性”或列表）
- `highlight`：要突出显示的样本索引
- `link`：转换函数

* *何时使用**：
- 多类分类解释
- 了解累积特征效应
- 比较样本之间的预测路径
- 识别预测分歧的位置

* *示例**：
```python
# Decision plot for multiple predictions
shap.plots.decision(
    shap_values.base_values,
    shap_values.values,
    X_test,
    feature_names=X_test.columns.tolist()
)

# Highlight specific instances
shap.plots.decision(
    shap_values.base_values,
    shap_values.values,
    X_test,
    highlight=[0, 5, 10]
)
```

## 绘图选择Guide

* *对于个人预测**：
- **瀑布**：最适合详细、顺序的解释
- **强制**：适合交互式探索
- **酒吧（本地）**：简单、干净的单预测重要性

* *用于全局理解**：
- **Beeswarm**：具有价值的信息密集摘要分布
- **Bar（全局）**：干净、简单的重要性排名
- **Violin**：以分布为中心的beeswarm替代品

* *对于特征关系**：
- **散点**：了解特征预测关系和交互
- **热图**：比较多个模式实例

* *对于多个样本**：
- **热图**：SHAP 值的网格视图
- **强制（堆叠）**：交互式多样本可视化
- **决策**：多类问题的预测路径

* *对于队列比较**：
- **条形（群组）**：特征重要性的清晰比较
- **多个蜂群**：并排分布比较

## 可视化最佳实践

* *1。开始全局，然后走向本地**：
- 从蜂群图或条形图开始了解全局模式
- 深入了解特定实例或功能的瀑布图或散点图

* *2。使用多种绘图类型**：
- 不同的绘图揭示不同的见解
- 组合瀑布（个体）+散点（关系）+蜂群（全局）

* *3。调整 max_display**：
- 默认 (10)适合演示
- 增加 (20-30)用于详细分析
- 考虑对冗余特征进行聚类

* *4.有意义的颜色**：
- 对 SHAP 值使用默认的红蓝色（红色 = 正，蓝色 = 负）
- 通过交互特征绘制颜色散点图
- 特定域的自定义颜色图

* *5。考虑受众**：
- 技术受众：Beeswarm、分散图、热图
- 非技术受众：瀑布图、条形图、力图
- 交互式演示：使用 JavaScript 进行力图

* *6。保存高质量图形**：
```python
import matplotlib.pyplot as plt

# Create plot
shap.plots.beeswarm(shap_values, show=False)

# Save with high DPI
plt.savefig('shap_plot.png', dpi=300, bbox_inches='tight')
plt.close()
```

* *7。处理大型数据集**：
- 用于可视化的样本子集（例如，`shap_values[:1000]`）
- 对于非常大的数据集使用小提琴而不是蜂群
- 调整具有许多点的散点图的alpha

## 常见模式和工作流程

* *模式1：完整模型说明**
```python
# 1. Global importance
shap.plots.beeswarm(shap_values)

# 2. Top feature relationships
for feature in top_features:
    shap.plots.scatter(shap_values[:, feature])

# 3. Example predictions
for i in interesting_indices:
    shap.plots.waterfall(shap_values[i])
```

* *模式2：模型比较**
```python
# Compute SHAP for multiple models
shap_model1 = explainer1(X_test)
shap_model2 = explainer2(X_test)

# Compare feature importance
shap.plots.bar({
    "Model 1": shap_model1,
    "Model 2": shap_model2
})
```

* *模式3：子组分析**
```python
# Define cohorts
male_mask = X_test['Sex'] == 'Male'
female_mask = X_test['Sex'] == 'Female'

# Compare cohorts
shap.plots.bar({
    "Male": shap_values[male_mask],
    "Female": shap_values[female_mask]
})

# Separate beeswarm plots
shap.plots.beeswarm(shap_values[male_mask])
shap.plots.beeswarm(shap_values[female_mask])
```

* *模式4：调试预测**
```python
# Identify outliers or errors
errors = (model.predict(X_test) != y_test)
error_indices = np.where(errors)[0]

# Explain errors
for idx in error_indices[:5]:
    print(f"Sample {idx}:")
    shap.plots.waterfall(shap_values[idx])

    # Explore key features
    shap.plots.scatter(shap_values[:, "Key_Feature"])
```

## 与笔记本和报告集成

* *Jupyter 笔记本**：
- 交互式力图无缝工作
- 使用 `show=True`（默认）进行内联显示
- 与降价解释

* *静态报告**：
- 使用matplotlib后端绘制力图
- 以编程方式保存图形
- 为了清晰起见，更喜欢瀑布图和条形图

* *Web应用程序**：
- 将力图导出为HTML
- 使用 shap.save_html()进行交互式可视化
- 考虑按需生成绘图

## 可视化故障排除

* *问题**：绘图不显示
- **解决方案**：确保 matplotlib 后端设置正确；如果需要，请使用 `plt.show()`

* *问题**：太多特征使绘图混乱
- **解决方案**：减少 `max_display` 参数或使用特征聚类

* *问题**：颜色反转或混淆
- **解决方案**：检查模型输出类型（概率与概率） log-odds）并使用适当的链接函数

* *问题**：大型数据集绘制缓慢
- **解决方案**：数据样本子集；使用 `shap_values[:1000]` 进行可视化

* *问题**：要素名称缺失
- **解决方案**：确保要素名称位于解释对象中或显式传递给绘图函数
