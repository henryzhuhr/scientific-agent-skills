# GNN 可解释性 — 完整参考

PyG 提供 `torch_geometric.explain` 用于解释 GNN 预测。该模块包括统一的 `Explainer` 接口、多种解释算法、可视化和评估指标。

## 解释器接口

`Explainer` 类是中心入口点。配置为：
1. 一个解释**算法**（GNNExplainer、PGExplainer、CaptumExplainer等）
2. **解释类型**（`"model"` - 解释模型预测，或 `"phenomenon"` - 解释数据集模式）
3. **掩模类型** — 解释输入的哪些部分（节点、边、特征）
4. **后处理** — 如何阈值掩码（top-k、硬等）

```python
from torch_geometric.explain import Explainer, GNNExplainer

explainer = Explainer(
    model=model,
    algorithm=GNNExplainer(epochs=200),
    explanation_type='model',          # 'model' or 'phenomenon'
    node_mask_type='attributes',       # 'object', 'common_attributes', 'attributes', or None
    edge_mask_type='object',           # 'object' or None
    model_config=dict(
        mode='multiclass_classification',  # 'binary_classification', 'multiclass_classification', 'regression'
        task_level='node',                  # 'node', 'edge', 'graph'
        return_type='log_probs',            # 'log_probs', 'probs', 'raw'
    ),
)
```

* *掩码类型说明：**
- `'object'`：每个节点/边一个掩码值（哪些节点/边重要？）
- `'attributes'`：每个节点特征维度一个掩码值（哪些特征）重要吗？）
- `'common_attributes'`：所有节点共享相同的特征掩码
- `None`：不生成此掩码类型

## 生成解释

### 节点分类

```python
# Explain prediction for node at index 10
explanation = explainer(data.x, data.edge_index, index=10)

print(explanation.node_mask)   # [num_nodes, num_features] — importance per feature per node
print(explanation.edge_mask)   # [num_edges] — importance per edge
```

### 图分类

```python
explainer = Explainer(
    model=model,
    algorithm=GNNExplainer(epochs=200),
    explanation_type='model',
    edge_mask_type='object',
    model_config=dict(
        mode='multiclass_classification',
        task_level='graph',
        return_type='raw',
    ),
)

explanation = explainer(data.x, data.edge_index)
```

## 可视化

```python
# Visualize which features are most important (bar chart)
explanation.visualize_feature_importance(top_k=10)
# Saves to 'feature_importance.png' by default, or pass path=

# Visualize the important subgraph
explanation.visualize_graph()
# Saves to 'graph.png' by default, or pass path=
```

## 可用算法

### GNNExplainer

通过优化学习软掩模。适用于节点和图形级任务。使用最广泛的算法。

```python
from torch_geometric.explain import GNNExplainer

algorithm = GNNExplainer(epochs=200, lr=0.01)
```

### PGExplainer

A 参数（经过训练的）解释器 — 学习生成边缘掩模的神经网络。使用前必须进行训练，然后推广到新图表。仅支持边缘掩码（无节点掩码）。

```python
from torch_geometric.explain import PGExplainer

explainer = Explainer(
    model=model,
    algorithm=PGExplainer(epochs=30, lr=0.003),
    explanation_type='phenomenon',     # PGExplainer explains phenomena
    edge_mask_type='object',
    model_config=dict(
        mode='regression',
        task_level='graph',
        return_type='raw',
    ),
    threshold_config=dict(threshold_type='topk', value=10),
)

# Train the explainer first
for epoch in range(30):
    for batch in loader:
        loss = explainer.algorithm.train(
            epoch, model, batch.x, batch.edge_index, target=batch.target
        )

# Then explain
explanation = explainer(data.x, data.edge_index)
```

### CaptumExplainer

包装 [Captum](https://captum.ai/)库，允许访问基于梯度的归因方法。适用于同构图和异构图。

```python
from torch_geometric.explain import CaptumExplainer

# Supports: 'IntegratedGradients', 'Saliency', 'Deconvolution',
#           'ShapleyValueSampling', 'GuidedBackprop', etc.
algorithm = CaptumExplainer('IntegratedGradients')
```

需要`pip install captum`（或`uv add captum`）。

### AttentionExplainer

使用基于注意力的 GNN（GATConv、TransformerConv）的注意力权重作为边缘解释。无需训练 - 只需读取现有的注意力分数。

```python
from torch_geometric.explain import AttentionExplainer

algorithm = AttentionExplainer()
```

## 异构图解释

对于异构模型，解释器返回带有每种类型掩码的`HeteroExplanation`：

```python
from torch_geometric.explain import Explainer, CaptumExplainer

explainer = Explainer(
    model=hetero_model,
    algorithm=CaptumExplainer('IntegratedGradients'),
    explanation_type='model',
    node_mask_type='attributes',
    edge_mask_type='object',
    model_config=dict(
        mode='multiclass_classification',
        task_level='node',
        return_type='probs',
    ),
)

hetero_explanation = explainer(
    data.x_dict,
    data.edge_index_dict,
    index=torch.tensor([1, 3]),
)

# Access per-type masks
hetero_explanation.node_mask_dict    # {'paper': tensor, 'author': tensor, ...}
hetero_explanation.edge_mask_dict    # {('paper','cites','paper'): tensor, ...}
```

## 评估指标

```python
from torch_geometric.explain import unfaithfulness, fidelity, characterization_score

# Unfaithfulness: how much does the explanation change the prediction?
# Lower is better (0 = perfectly faithful)
score = unfaithfulness(explainer, explanation)

# Fidelity: measures explanation quality via positive/negative fidelity
pos_fidelity, neg_fidelity = fidelity(explainer, explanation)

# Characterization score: combined metric
char_score = characterization_score(pos_fidelity, neg_fidelity)
```

## 后处理掩码

控制原始掩码值如何转换为最终解释：

```python
explainer = Explainer(
    ...,
    threshold_config=dict(
        threshold_type='topk',    # 'topk', 'hard', or None
        value=10,                  # Top-10 edges for 'topk', threshold value for 'hard'
    ),
)
```

- `'topk'`：仅保留前k个得分最高的元素
- `'hard'`：二进制阈值 — 保留 `value` 以上的元素
- `None`：返回原始连续掩码值
