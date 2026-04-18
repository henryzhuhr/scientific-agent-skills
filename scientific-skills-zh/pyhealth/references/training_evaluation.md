# PyHealth 训练、评估和可解释性

## 概述

PyHealth 提供用于训练模型、评估预测、确保模型可靠性和解释临床应用结果的综合工具。

## 训练器类

### 核心功能

`Trainer` 类管理完整的模型训练和评估工作流程PyTorch 集成。

* *初始化：**
```python
from pyhealth.trainer import Trainer

trainer = Trainer(
    model=model,  # PyHealth or PyTorch model
    device="cuda",  # or "cpu"
)
```

### 训练

* *train()方法**

 通过全面的监控和检查点训练模型。

* *参数：**
- `train_dataloader`：训练数据加载器
- `val_dataloader`：验证数据加载器（可选）
- `test_dataloader`：测试数据加载器（可选）
- `epochs`：训练周期数
- `optimizer`：优化器实例或class
- `learning_rate`：学习率（默认：1e-3）
- `weight_decay`：L2 正则化（默认：0）
- `max_grad_norm`：梯度裁剪阈值
- `monitor`：要监控的指标（例如， "pr_auc_score")
- `monitor_criterion`：“max”或“min” 
- `save_path`：检查点保存目录

* *用法：**
```python
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    test_dataloader=test_loader,
    epochs=50,
    optimizer=torch.optim.Adam,
    learning_rate=1e-3,
    weight_decay=1e-5,
    max_grad_norm=5.0,
    monitor="pr_auc_score",
    monitor_criterion="max",
    save_path="./checkpoints"
)
```

* *训练特点：**

1. **自动检查点**：根据监控的指标

2保存最佳模型。 **提前停止**：如果没有改善则停止训练

3. **梯度剪切**：防止梯度爆炸

4. **进度跟踪**：显示训练进度和指标

5. **多GPU支持**：自动设备放置

### Inference

* *inference()方法**

对数据集执行预测。

* *参数：**
- `dataloader`：用于推理的数据加载器
- `additional_outputs`：要返回的附加输出列表
- `return_patient_ids`：返回患者标识符

* *用法：**
```python
predictions = trainer.inference(
    dataloader=test_loader,
    additional_outputs=["attention_weights", "embeddings"],
    return_patient_ids=True
)
```

 * *返回：**
- `y_pred`：模型预测
- `y_true`：地面真实标签
- `patient_ids`：患者标识符（如果请求）
- 附加输出（如果指定）

### 评估

* *evaluate()方法**

 计算综合评估指标。

* *参数：**
- `dataloader`：用于评估的数据加载器
- `metrics`：度量函数列表

* *用法：**
```python
from pyhealth.metrics import binary_metrics_fn

results = trainer.evaluate(
    dataloader=test_loader,
    metrics=["accuracy", "pr_auc_score", "roc_auc_score", "f1_score"]
)

print(results)
# Output: {'accuracy': 0.85, 'pr_auc_score': 0.78, 'roc_auc_score': 0.82, 'f1_score': 0.73}
```

### 检查点管理

* *save()方法**
```python
trainer.save("./models/best_model.pt")
```

* *load()方法**
```python
trainer.load("./models/best_model.pt")
```

## 评估指标

### 二元分类指标

* *可用指标：**
- `accuracy`：总体准确度
- `precision`：阳性预测值
- `recall`：灵敏度/真阳性率
- `f1_score`：F1分数（精度和召回率的调和平均值）
- `roc_auc_score`：ROC曲线下的面积
- `pr_auc_score`：精度-召回率下的面积曲线
- `cohen_kappa`：评估者间可靠性

* *用法：**
```python
from pyhealth.metrics import binary_metrics_fn

# Comprehensive binary metrics
metrics = binary_metrics_fn(
    y_true=labels,
    y_pred=predictions,
    metrics=["accuracy", "f1_score", "pr_auc_score", "roc_auc_score"]
)
```

* *阈值选择：**
```python
# Default threshold: 0.5
predictions_binary = (predictions > 0.5).astype(int)

# Optimal threshold by F1
from sklearn.metrics import f1_score
thresholds = np.arange(0.1, 0.9, 0.05)
f1_scores = [f1_score(y_true, (y_pred > t).astype(int)) for t in thresholds]
optimal_threshold = thresholds[np.argmax(f1_scores)]
```

* *最佳实践：**
- **使用AUROC**：整体模型判别
- **使用AUPRC**：特别针对不平衡类
- **使用F1**：平衡精度和召回率
- **报告置信区间**：Bootstrap重采样

### 多类分类指标

* *可用指标：**
- `accuracy`：总体准确度
- `macro_f1`：跨类别的未加权平均F1
- `micro_f1`：全局F1（总TP，FP， FN)
- `weighted_f1`：按类别频率加权平均 F1
- `cohen_kappa`：多类别 kappa

* *用法：**
```python
from pyhealth.metrics import multiclass_metrics_fn

metrics = multiclass_metrics_fn(
    y_true=labels,
    y_pred=predictions,
    metrics=["accuracy", "macro_f1", "weighted_f1"]
)
```

* *每类别指标：**
```python
from sklearn.metrics import classification_report

print(classification_report(y_true, y_pred,
    target_names=["Wake", "N1", "N2", "N3", "REM"]))
```

* *混淆矩阵：**
```python
from sklearn.metrics import confusion_matrix
import seaborn as sns

cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm, annot=True, fmt='d')
```

### 多标签分类指标

* *可用指标：**
- `jaccard_score`：并集的交集
- `hamming_loss`：不正确标签的比例
- `example_f1`：每个示例的F1（微观平均）
- `label_f1`：每个标签的F1（宏观）平均）

* *用法：**
```python
from pyhealth.metrics import multilabel_metrics_fn

# y_pred: [n_samples, n_labels] binary matrix
metrics = multilabel_metrics_fn(
    y_true=label_matrix,
    y_pred=pred_matrix,
    metrics=["jaccard_score", "example_f1", "label_f1"]
)
```

* *药物推荐指标：**
```python
# Jaccard similarity (intersection/union)
jaccard = len(set(true_drugs) & set(pred_drugs)) / len(set(true_drugs) | set(pred_drugs))

# Precision@k: Precision for top-k predictions
def precision_at_k(y_true, y_pred, k=10):
    top_k_pred = y_pred.argsort()[-k:]
    return len(set(y_true) & set(top_k_pred)) / k
```

### 回归指标

* *可用指标：**
- `mean_absolute_error`：平均绝对误差
- `mean_squared_error`：平均平方误差
- `root_mean_squared_error`：RMSE
- `r2_score`：系数判定

* *用法：**
```python
from pyhealth.metrics import regression_metrics_fn

metrics = regression_metrics_fn(
    y_true=true_values,
    y_pred=predictions,
    metrics=["mae", "rmse", "r2"]
)
```

* *百分比误差指标：**
```python
# Mean Absolute Percentage Error
mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# Median Absolute Percentage Error (robust to outliers)
medape = np.median(np.abs((y_true - y_pred) / y_true)) * 100
```

### 公平指标

* *目的：**评估跨人口统计的模型偏差groups

* *可用指标：**
- `demographic_parity`：阳性预测率相等
- `equalized_odds`：组间 TPR 和 FPR 相等
- `equal_opportunity`：组间 TPR 相等
- `predictive_parity`：组间相等 PPV

* *用法：**
```python
from pyhealth.metrics import fairness_metrics_fn

fairness_results = fairness_metrics_fn(
    y_true=labels,
    y_pred=predictions,
    sensitive_attributes=demographics,  # e.g., race, gender
    metrics=["demographic_parity", "equalized_odds"]
)
```

* *示例：**
```python
# Evaluate fairness across gender
male_mask = (demographics == "male")
female_mask = (demographics == "female")

male_tpr = recall_score(y_true[male_mask], y_pred[male_mask])
female_tpr = recall_score(y_true[female_mask], y_pred[female_mask])

tpr_disparity = abs(male_tpr - female_tpr)
print(f"TPR disparity: {tpr_disparity:.3f}")
```

## 校准和不确定度量化

### 模型校准

* *目的：**确保预测概率与实际频率匹配

* *校准图：**
```python
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt

fraction_of_positives, mean_predicted_value = calibration_curve(
    y_true, y_prob, n_bins=10
)

plt.plot(mean_predicted_value, fraction_of_positives, marker='o')
plt.plot([0, 1], [0, 1], linestyle='--', label='Perfect calibration')
plt.xlabel('Mean predicted probability')
plt.ylabel('Fraction of positives')
plt.legend()
```

* *预期校准误差（ECE）：**
```python
def expected_calibration_error(y_true, y_prob, n_bins=10):
    """Compute ECE"""
    bins = np.linspace(0, 1, n_bins + 1)
    bin_indices = np.digitize(y_prob, bins) - 1

    ece = 0
    for i in range(n_bins):
        mask = bin_indices == i
        if mask.sum() > 0:
            bin_accuracy = y_true[mask].mean()
            bin_confidence = y_prob[mask].mean()
            ece += mask.sum() / len(y_true) * abs(bin_accuracy - bin_confidence)

    return ece
```

* *校准方法：**

1. **Platt 缩放**：验证预测 
```python
from sklearn.linear_model import LogisticRegression

calibrator = LogisticRegression()
calibrator.fit(val_predictions.reshape(-1, 1), val_labels)
calibrated_probs = calibrator.predict_proba(test_predictions.reshape(-1, 1))[:, 1]
```

2 的逻辑回归。 **等渗回归**：非参数校准
```python
from sklearn.isotonic import IsotonicRegression

calibrator = IsotonicRegression(out_of_bounds='clip')
calibrator.fit(val_predictions, val_labels)
calibrated_probs = calibrator.predict(test_predictions)
```

3. **温度缩放**：在softmax之前缩放logits
```python
def find_temperature(logits, labels):
    """Find optimal temperature parameter"""
    from scipy.optimize import minimize

    def nll(temp):
        scaled_logits = logits / temp
        probs = torch.softmax(scaled_logits, dim=1)
        return F.cross_entropy(probs, labels).item()

    result = minimize(nll, x0=1.0, method='BFGS')
    return result.x[0]

temperature = find_temperature(val_logits, val_labels)
calibrated_logits = test_logits / temperature
```

### 不确定性量化

* *保形预测：**

提供有保证的预测集覆盖率。

* *用法：**
```python
from pyhealth.metrics import prediction_set_metrics_fn

# Calibrate on validation set
scores = 1 - val_predictions[np.arange(len(val_labels)), val_labels]
quantile_level = np.quantile(scores, 0.9)  # 90% coverage

# Generate prediction sets on test set
prediction_sets = test_predictions > (1 - quantile_level)

# Evaluate
metrics = prediction_set_metrics_fn(
    y_true=test_labels,
    prediction_sets=prediction_sets,
    metrics=["coverage", "average_size"]
)
```

* *蒙特卡洛辍学：**

E通过推理时的辍学估计不确定性。

```python
def predict_with_uncertainty(model, dataloader, num_samples=20):
    """Predict with uncertainty using MC dropout"""
    model.train()  # Keep dropout active

    predictions = []
    for _ in range(num_samples):
        batch_preds = []
        for batch in dataloader:
            with torch.no_grad():
                output = model(batch)
                batch_preds.append(output)
        predictions.append(torch.cat(batch_preds))

    predictions = torch.stack(predictions)
    mean_pred = predictions.mean(dim=0)
    std_pred = predictions.std(dim=0)  # Uncertainty

    return mean_pred, std_pred
```

* *Ensemble不确定性：**

```python
# Train multiple models
models = [train_model(seed=i) for i in range(5)]

# Predict with ensemble
ensemble_preds = []
for model in models:
    pred = model.predict(test_data)
    ensemble_preds.append(pred)

mean_pred = np.mean(ensemble_preds, axis=0)
std_pred = np.std(ensemble_preds, axis=0)  # Uncertainty
```

## 可解释性

### 注意力可视化

* *对于 Transformer 和 RETAIN 模型：**

```python
# Get attention weights during inference
outputs = trainer.inference(
    test_loader,
    additional_outputs=["attention_weights"]
)

attention = outputs["attention_weights"]

# Visualize attention for sample
import matplotlib.pyplot as plt
import seaborn as sns

sample_idx = 0
sample_attention = attention[sample_idx]  # [seq_length, seq_length]

sns.heatmap(sample_attention, cmap='viridis')
plt.xlabel('Key Position')
plt.ylabel('Query Position')
plt.title('Attention Weights')
plt.show()
```

* *RETAIN解读：**

```python
# RETAIN provides visit-level and feature-level attention
visit_attention = outputs["visit_attention"]  # Which visits are important
feature_attention = outputs["feature_attention"]  # Which features are important

# Find most influential visit
most_important_visit = visit_attention[sample_idx].argmax()

# Find most influential features in that visit
important_features = feature_attention[sample_idx, most_important_visit].argsort()[-10:]
```

### 功能重要性

* *排列重要性：**

```python
from sklearn.inspection import permutation_importance

def get_predictions(model, X):
    return model.predict(X)

result = permutation_importance(
    model, X_test, y_test,
    n_repeats=10,
    scoring='roc_auc'
)

# Sort features by importance
indices = result.importances_mean.argsort()[::-1]
for i in indices[:10]:
    print(f"{feature_names[i]}: {result.importances_mean[i]:.3f}")
```

* *SHAP 值：**

```python
import shap

# Create explainer
explainer = shap.DeepExplainer(model, train_data)

# Compute SHAP values
shap_values = explainer.shap_values(test_data)

# Visualize
shap.summary_plot(shap_values, test_data, feature_names=feature_names)
```

### ChEFER（临床健康事件特征提取和排名）

* *PyHealth的可解释性工具：**

```python
from pyhealth.explain import ChEFER

explainer = ChEFER(model=model, dataset=test_dataset)

# Get feature importance for prediction
importance_scores = explainer.explain(
    patient_id="patient_123",
    visit_id="visit_456"
)

# Visualize top features
explainer.plot_importance(importance_scores, top_k=20)
```

## 完整的训练管道示例

```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.datasets import split_by_patient, get_dataloader
from pyhealth.models import Transformer
from pyhealth.trainer import Trainer
from pyhealth.metrics import binary_metrics_fn

# 1. Load and prepare data
dataset = MIMIC4Dataset(root="/path/to/mimic4")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)

# 2. Split data
train_data, val_data, test_data = split_by_patient(
    sample_dataset, ratios=[0.7, 0.1, 0.2], seed=42
)

# 3. Create data loaders
train_loader = get_dataloader(train_data, batch_size=64, shuffle=True)
val_loader = get_dataloader(val_data, batch_size=64, shuffle=False)
test_loader = get_dataloader(test_data, batch_size=64, shuffle=False)

# 4. Initialize model
model = Transformer(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "procedures", "medications"],
    mode="binary",
    embedding_dim=128,
    num_heads=8,
    num_layers=3,
    dropout=0.3
)

# 5. Train model
trainer = Trainer(model=model, device="cuda")
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    optimizer=torch.optim.Adam,
    learning_rate=1e-3,
    weight_decay=1e-5,
    monitor="pr_auc_score",
    monitor_criterion="max",
    save_path="./checkpoints/mortality_model"
)

# 6. Evaluate on test set
test_results = trainer.evaluate(
    test_loader,
    metrics=["accuracy", "precision", "recall", "f1_score",
             "roc_auc_score", "pr_auc_score"]
)

print("Test Results:")
for metric, value in test_results.items():
    print(f"{metric}: {value:.4f}")

# 7. Get predictions for analysis
predictions = trainer.inference(test_loader, return_patient_ids=True)
y_pred, y_true, patient_ids = predictions

# 8. Calibration analysis
from sklearn.calibration import calibration_curve

fraction_pos, mean_pred = calibration_curve(y_true, y_pred, n_bins=10)
ece = expected_calibration_error(y_true, y_pred)
print(f"Expected Calibration Error: {ece:.4f}")

# 9. Save final model
trainer.save("./models/mortality_transformer_final.pt")
```

## 最佳实践

### 训练

1. **监控多个指标**：跟踪损失和特定于任务的指标
2. **使用验证集**：通过提前停止
3来防止过度拟合。 **梯度裁剪**：稳定训练（max_grad_norm=5.0）
4. **学习率调度**：在平台
5上减少LR。 **检查点最佳模型**：根据验证性能保存

### 评估

1. **使用适合任务的指标**：AUROC/AUPRC 用于二进制，宏 F1 用于不平衡的多类
2. **报告置信区间**：引导或交叉验证
3. **分层评估**：按子组
4报告指标。 **临床指标**：包括临床相关阈值
5. **公平评估**：跨人口统计群体进行评估

### 部署

1. **校准预测**：确保概率可靠
2. **量化不确定性**：提供置信度估计
3. **监控性能**：跟踪生产中的指标
4. **处理分布变化**：检测数据何时变化
5. **可解释性**：为预测提供解释
