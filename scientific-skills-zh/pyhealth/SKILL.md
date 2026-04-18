---
name: pyhealth
description: 全面的医疗保健人工智能工具包，用于使用临床数据开发、测试和部署机器学习模型。在处理电子健康记录 (EHR)、临床预测任务（死亡率、再入院、药物推荐）、医疗编码系统（ICD、NDC、ATC）、生理信号（EEG、ECG）、医疗数据集（MIMIC-III/IV、eICU、OMOP）或为医疗保健应用实施深度学习模型（RETAIN、SafeDrug、Transformer、GNN）时，应使用此技能。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# PyHealth：医疗保健 AI 工具包

## 概述

PyHealth 是一个用于医疗保健 AI 的综合 Python 库，为临床机器学习提供专门的工具、模型和数据集。在开发医疗保健预测模型、处理临床数据、使用医疗编码系统或在医疗保健环境中部署 AI 解决方案时，请使用此技能。

## 何时使用此技能

在以下情况下调用此技能：

- **使用医疗保健数据集**：MIMIC-III、MIMIC-IV、eICU、OMOP、睡眠脑电图数据、医学图像
- **临床预测任务**：死亡率预测、再入院、住院时间、药物推荐
- **医学编码**：ICD-9/10、NDC、RxNorm、ATC 编码系统之间的转换
- **处理临床数据**：顺序事件、生理信号、临床文本、医学图像
- **实施医疗保健模型**：RETAIN、SafeDrug、GAMENet、StageNet、 EHR
 的变压器 - **评估临床模型**：公平性指标、校准、可解释性、不确定性量化

## 核心功能

PyHealth 通过针对医疗保健 AI 优化的模块化 5 阶段管道进行操作：

1. **数据加载**：通过标准化接口
2访问10多个医疗数据集。 **任务定义**：应用 20 多个预定义的临床预测任务或创建自定义任务
3. **模型选择**：从 33 多个模型中进行选择（基线、深度学习、医疗保健特定）
4. **培训**：通过自动检查点、监控和评估
5进行培训。 **部署**：校准、解释和验证临床使用

 * *性能**：医疗数据处理速度比 pandas 快 3 倍

## 快速启动工作流程

```python
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.datasets import split_by_patient, get_dataloader
from pyhealth.models import Transformer
from pyhealth.trainer import Trainer

# 1. Load dataset and set task
dataset = MIMIC4Dataset(root="/path/to/data")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)

# 2. Split data
train, val, test = split_by_patient(sample_dataset, [0.7, 0.1, 0.2])

# 3. Create data loaders
train_loader = get_dataloader(train, batch_size=64, shuffle=True)
val_loader = get_dataloader(val, batch_size=64, shuffle=False)
test_loader = get_dataloader(test, batch_size=64, shuffle=False)

# 4. Initialize and train model
model = Transformer(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "medications"],
    mode="binary",
    embedding_dim=128
)

trainer = Trainer(model=model, device="cuda")
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    monitor="pr_auc_score"
)

# 5. Evaluate
results = trainer.evaluate(test_loader)
```

## 详细文档

该技能包括按功能组织的综合参考文档。根据需要阅读具体参考文件：

### 1.数据集和数据结构

* *文件**：`references/datasets.md`

* *阅读时间：**
- 加载医疗数据集（MIMIC、eICU、OMOP、睡眠脑电图等）
- 了解事件、患者、就诊数据结构
- 处理不同的数据类型（EHR、信号、图像、文本）
- 拆分数据以进行训练/验证/测试
- 使用 SampleDataset 进行特定于任务的格式化

* *关键主题：**
- 核心数据结构（事件、患者、访问）
- 10 多个可用数据集（EHR、生理信号、成像、文本）
- 数据加载和迭代
- 训练/验证/测试分割策略
- 大数据集的性能优化

### 2. 医学编码翻译

* *文件**：`references/medical_coding.md`

* *阅读当：**
- 在医疗编码系统之间进行转换
- 使用诊断代码（ICD-9-CM、ICD-10-CM、CCS）
- 处理药物代码（NDC、RxNorm、ATC）
- 标准化程序代码（ICD-9-PROC、 ICD-10-PROC)
- 将代码分组为临床类别
- 处理分层药物分类

* *关键主题：**
- 用于系统内查找的 InnerMap
- 用于跨系统翻译的 CrossMap
- 支持的编码系统（ICD、NDC、ATC、CCS、 RxNorm)
- 代码标准化和层次结构遍历
- 按治疗类别进行药物分类
- 与数据集集成

### 3.临床预测任务

* *文件**：`references/tasks.md`

* *阅读何时：**
- 定义临床预测目标
- 使用预定义任务（死亡率、再入院、药物推荐）
- 处理 EHR、信号、成像或基于文本的任务
- 创建自定义预测任务
- 为模型设置输入/输出模式
- 应用特定于任务的过滤逻辑

* *关键主题：**
- 20+ 预定义临床任务
- EHR 任务（死亡率、再入院、住院时间、药物推荐）
- 信号任务（睡眠分期、脑电图分析、癫痫检测）
- 影像任务（COVID-19 胸部 X 射线分类）
- 文本任务（医学编码、专业）分类）
- 自定义任务创建模式

### 4. 模型和架构

* *文件**：`references/models.md`

* *阅读时间：**
- 选择临床预测模型
- 了解模型架构和功能
- 在通用和医疗保健专用之间进行选择models
- 实现可解释模型（RETAIN、AdaCare）
- 使用药物推荐（SafeDrug、GAMENet）
- 使用图形神经网络进行医疗保健
- 配置模型超参数

* *关键主题：**
- 33+ 可用models
- 通用：Logistic 回归、MLP、CNN、RNN、Transformer、GNN
- 医疗保健专用：RETAIN、SafeDrug、GAMENet、StageNet、AdaCare
- 按任务类型和数据类型选择模型
- 可解释性注意事项
- 计算要求
- 超参数调优指南

### 5.数据预处理

* *文件**：`references/preprocessing.md`

* *读取时间：**
- 预处理模型的临床数据
- 处理顺序事件和时间序列数据
- 处理生理信号（EEG、ECG）
- 标准化实验室值和生命体征
- 为不同任务类型准备标签
- 构建特征词汇表
- 管理缺失数据和异常值

* *关键主题：**
- 15+ 处理器类型
- 序列处理（填充、截断）
- 信号处理（过滤、分割）
- 特征提取和编码
- 标签处理器（二值、多类、多标签、回归）
- 文本和图像预处理
- 常用预处理工作流程

### 6. 训练和评估

* *文件**：`references/training_evaluation.md`

* *阅读时间：**
- 使用 Trainer 类训练模型
- 评估模型性能
- 计算临床指标
- 评估跨人口统计的模型公平性
- 校准可靠性预测
- 量化预测不确定性
- 解释模型预测
- 为临床部署准备模型

* *关键主题：**
- 训练器类（训练、评估、推理）
- 二元、多类、多标签、回归任务的指标
- 偏差评估的公平性指标
- 校准方法（普拉特缩放、温度）缩放）
- 不确定性量化（保形预测、MC dropout）
- 可解释性工具（注意力可视化、SHAP、ChEFER）
- 完整的训练管道示例

## 安装

```bash
uv pip install pyhealth
```

* *要求：**
- Python ≥ 3.7
- PyTorch ≥ 1.8
- NumPy, pandas, scikit-learn

## 常用案例

### 使用案例1：ICU 死亡率预测

* *目标**：预测重症监护病房的患者死亡率

* *方法：**
1. 加载 MIMIC-IV 数据集 → 读取 `references/datasets.md`
2. 应用死亡率预测任务 → 阅读 `references/tasks.md`
3. 选择可解释模型（RETAIN）→读取`references/models.md`
4. 训练和评估 → 阅读 `references/training_evaluation.md`
5. 解释临床使用的预测 → 阅读 `references/training_evaluation.md`

### 使用案例 2：安全用药建议

* *目标**：推荐药物，同时避免药物相互作用

* *方法：**
1. 加载 EHR 数据集（MIMIC-IV 或 OMOP）→ 读取 `references/datasets.md`
2. 申请药物推荐任务→阅读`references/tasks.md`
3. 使用具有 DDI 约束的 SafeDrug 模型 → 阅读 `references/models.md`
4. 预处理药物代码 → 读取 `references/medical_coding.md`
5. 使用多标签指标进行评估 → 阅读 `references/training_evaluation.md`

### 用例 3：医院再入院预测

* *目标**：识别有 30 天再入院风险的患者

* *方法：**
1. 加载多站点 EHR 数据（eICU 或 OMOP）→ 读取 `references/datasets.md`
2. 应用再入院预测任务 → 阅读 `references/tasks.md`
3. 处理预处理中的类不平衡 → 阅读 `references/preprocessing.md`
4. 火车变压器模型 → 阅读 `references/models.md`
5. 校准预测并评估公平性 → 阅读 `references/training_evaluation.md`

### 用例 4：睡眠障碍诊断

* *目标**：根据 EEG 信号对睡眠阶段进行分类

* *方法：**
1. 加载睡眠脑电图数据集（SleepEDF、SHHS）→读取`references/datasets.md`
2. 应用睡眠分期任务 → 阅读 `references/tasks.md`
3. 预处理脑电图信号（过滤、分割）→读取`references/preprocessing.md`
4. 训练 CNN 或 RNN 模型 → 阅读 `references/models.md`
5. 评估每个阶段的性能 → 阅读 `references/training_evaluation.md`

### 用例 5：医疗代码翻译

* *目标**：跨不同编码系统标准化诊断

* *方法：**
1. 阅读 `references/medical_coding.md` 获取全面指导 
2. 使用 CrossMap 在 ICD-9、ICD-10、CCS
3 之间进行转换。将代码分组为有临床意义的类别
4. 与数据集处理集成

### 用例 6：临床文本到 ICD 编码

* *目标**：从临床记录中自动分配 ICD 代码

* *方法：**
1. 使用临床文本加载 MIMIC-III → 阅读 `references/datasets.md`
2. 应用ICD编码任务→读取`references/tasks.md`
3. 预处理临床文本 → 阅读 `references/preprocessing.md`
4. 使用 TransformersModel (ClinicalBERT) → 阅读 `references/models.md`
5. 使用多标签指标进行评估 → 阅读 `references/training_evaluation.md`

## 最佳实践

### 数据处理

1. **始终按患者拆分**：通过确保没有患者出现在多个拆分中来防止数据泄漏
 ```python
 from pyhealth.datasets import split_by_patent
 train, val, test = split_by_patent(dataset, [0.7, 0.1, 0.2])
 ``

2. **检查数据集统计数据**：在建模之前了解您的数据
 ```python
 print(dataset.stats()) # 患者、访问、事件、代码分布
 ```

3. **使用适当的预处理**：将处理器与数据类型相匹配（请参阅`references/preprocessing.md`）

### 模型开发

1. **从基线开始**：使用简单模型建立基线性能
  - 二元/多类任务的逻辑回归
  - 用于初始深度学习基线的MLP

2. **选择适合任务的模型**：
  - 所需的可解释性 → RETAIN、AdaCare
  - 药物推荐 → SafeDrug、GAMENet
  - 长序列 → Transformer
  - 图形关系 → GNN

3. **监控验证指标**：对任务使用适当的指标并处理类别不平衡
  - 二元分类：AUROC、AUPRC（特别是对于罕见事件）
  - 多类别：宏-F1（用于不平衡）、加权-F1
  - 多标签：Jaccard、示例-F1
  - 回归：MAE、 RMSE

### 临床部署

1. **校准预测**：确保概率可靠（参见 `references/training_evaluation.md`）

2. **评估公平性**：跨人口群体进行评估以检测偏差

3. **量化不确定性**：为预测 

4 提供置信度估计。 **解释预测**：使用注意力权重、SHAP 或 ChEFER 来获得临床信任 

5. **彻底验证**：使用来自不同时间段或地点的保留测试集

## 限制和注意事项

### 数据要求

- **大型数据集**：深度学习模型需要足够的数据（数千名患者）
- **数据质量**：丢失数据和编码错误影响性能
- **时间一致性**：确保训练/测试拆分在需要时遵循时间顺序

### 临床验证

- **外部验证**：对来自不同医院/系统的数据进行测试
- **前瞻性评估**：部署前在真实临床环境中进行验证
- **临床审查**：让临床医生审查预测和解释
- **道德考虑**：解决隐私（HIPAA/GDPR）、公平性和安全性

### 计算资源

- **推荐GPU**：用于高效训练深度学习模型
- **内存要求**：大型数据集可能需要16GB+ RAM
- **存储**：医疗数据集可以是10s-100s的GB

## 故障排除

### 常见问题

* *导入错误数据集**：
- 确保数据集文件已下载且路径正确
- 检查PyHealth版本兼容性

* *内存不足**：
- 减少批量大小
- 减少序列长度（`max_seq_length`）
- 使用梯度累积
- 分块处理数据

* *性能差**：
- 检查类不平衡并使用适当的指标（AUPRC与AUROC）
- 验证预处理（标准化，缺失数据处理）
- 增加模型容量或训练周期
- 检查训练/测试中的数据泄漏split

* *慢速训练**：
- 使用 GPU (`device="cuda"`)
- 增加批量大小（如果内存允许）
- 减少序列长度
- 使用更高效的模型（CNN 与 Transformer）

### 获取帮助

- **文档**：https://pyhealth.readthedocs.io/
- **GitHub问题**：https://github.com/sunlabuiuc/PyHealth/issues
- **教程**：7个核心教程+ 5个在线实用管道

## 示例：完整工作流程

```python
# Complete mortality prediction pipeline
from pyhealth.datasets import MIMIC4Dataset
from pyhealth.tasks import mortality_prediction_mimic4_fn
from pyhealth.datasets import split_by_patient, get_dataloader
from pyhealth.models import RETAIN
from pyhealth.trainer import Trainer

# 1. Load dataset
print("Loading MIMIC-IV dataset...")
dataset = MIMIC4Dataset(root="/data/mimic4")
print(dataset.stats())

# 2. Define task
print("Setting mortality prediction task...")
sample_dataset = dataset.set_task(mortality_prediction_mimic4_fn)
print(f"Generated {len(sample_dataset)} samples")

# 3. Split data (by patient to prevent leakage)
print("Splitting data...")
train_ds, val_ds, test_ds = split_by_patient(
    sample_dataset, ratios=[0.7, 0.1, 0.2], seed=42
)

# 4. Create data loaders
train_loader = get_dataloader(train_ds, batch_size=64, shuffle=True)
val_loader = get_dataloader(val_ds, batch_size=64)
test_loader = get_dataloader(test_ds, batch_size=64)

# 5. Initialize interpretable model
print("Initializing RETAIN model...")
model = RETAIN(
    dataset=sample_dataset,
    feature_keys=["diagnoses", "procedures", "medications"],
    mode="binary",
    embedding_dim=128,
    hidden_dim=128
)

# 6. Train model
print("Training model...")
trainer = Trainer(model=model, device="cuda")
trainer.train(
    train_dataloader=train_loader,
    val_dataloader=val_loader,
    epochs=50,
    optimizer="Adam",
    learning_rate=1e-3,
    weight_decay=1e-5,
    monitor="pr_auc_score",  # Use AUPRC for imbalanced data
    monitor_criterion="max",
    save_path="./checkpoints/mortality_retain"
)

# 7. Evaluate on test set
print("Evaluating on test set...")
test_results = trainer.evaluate(
    test_loader,
    metrics=["accuracy", "precision", "recall", "f1_score",
             "roc_auc_score", "pr_auc_score"]
)

print("\nTest Results:")
for metric, value in test_results.items():
    print(f"  {metric}: {value:.4f}")

# 8. Get predictions with attention for interpretation
predictions = trainer.inference(
    test_loader,
    additional_outputs=["visit_attention", "feature_attention"],
    return_patient_ids=True
)

# 9. Analyze a high-risk patient
high_risk_idx = predictions["y_pred"].argmax()
patient_id = predictions["patient_ids"][high_risk_idx]
visit_attn = predictions["visit_attention"][high_risk_idx]
feature_attn = predictions["feature_attention"][high_risk_idx]

print(f"\nHigh-risk patient: {patient_id}")
print(f"Risk score: {predictions['y_pred'][high_risk_idx]:.3f}")
print(f"Most influential visit: {visit_attn.argmax()}")
print(f"Most important features: {feature_attn[visit_attn.argmax()].argsort()[-5:]}")

# 10. Save model for deployment
trainer.save("./models/mortality_retain_final.pt")
print("\nModel saved successfully!")
```

## 资源

各个组件的详细信息，请参考`references/`目录下的综合参考文件：

- **datasets.md**：数据结构、加载和分割（4,500 个字）
- **medical_coding.md**：代码翻译和标准化（3,800 个字）
- **tasks.md**：临床预测任务和自定义任务创建（4,200 个字）
- **models.md**：模型架构和选择指南（5,100 个字）
- **preprocessing.md**：数据处理器和预处理工作流程（4,600 个字）
- **training_evaluation.md**：训练、指标、校准、可解释性（5,900 个字）

* * 全面的文档**：整个模块化参考文件约 28,000 个字。
