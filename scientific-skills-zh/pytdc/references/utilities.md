# TDC 实用程序和数据函数

本文档提供了有关TDC 数据处理、评估和实用函数的综合文档。

## 概述

TDC 提供的实用程序分为四个主要类别：
1. **数据集分割** - 训练/验证/测试分区策略
2. **模型评估** - 标准化性能指标
3. **数据处理** - 分子转换、过滤和转化
4. **实体检索** - 数据库查询和转换

## 1. 数据集拆分

数据集拆分对于评估模型泛化能力至关重要。 TDC 提供多种专为治疗性 ML 设计的拆分策略。

### 基本拆分用法

```python
from tdc.single_pred import ADME

data = ADME(name='Caco2_Wang')

# Get split with default parameters
split = data.get_split()
# Returns: {'train': DataFrame, 'valid': DataFrame, 'test': DataFrame}

# Customize split parameters
split = data.get_split(
    method='scaffold',
    seed=42,
    frac=[0.7, 0.1, 0.2]
)
```

### 拆分方法

#### 随机拆分
数据随机洗牌 - 适用于一般 ML 

```python
split = data.get_split(method='random', seed=1)
```

* *何时使用：**
- 基线模型评估
- 当化学/时间结构不重要时
- 快速原型制作

* *不推荐用于：**
- 现实药物发现场景
- 评估对新化学物质的泛化

#### 支架拆分
基于分子支架（Bemis-Murcko支架）的拆分-确保测试分子在结构上与训练不同。

```python
split = data.get_split(method='scaffold', seed=1)
```

* *何时使用：**
- 默认为大多数单一预测任务
- 评估对新化学系列的泛化
- 现实的药物发现场景

* *工作原理：**
1. 从每个分子 
2 中提取 Bemis-Murcko 支架。通过支架
3对分子进行分组。将脚手架分配给训练/有效/测试集
4. 确保测试分子具有看不见的支架

#### 冷分裂（DTI/DDI任务）
对于多实例预测，冷分裂确保测试集包含看不见的药物、靶标或两者。

* *冷药物分裂：**
```python
from tdc.multi_pred import DTI
data = DTI(name='BindingDB_Kd')
split = data.get_split(method='cold_drug', seed=1)
```
-测试集包含在过程中未看到的药物训练
- 评估新化合物的泛化

* *冷目标分割：**
```python
split = data.get_split(method='cold_target', seed=1)
```
-测试集包含训练期间未看到的目标
- 评估对新蛋白质的泛化

* *冷药物-目标分割：**
```python
split = data.get_split(method='cold_drug_target', seed=1)
```
-测试集包含新的药物-目标对
- 最具挑战性的评估场景

#### Temporal Split
对于具有时间信息的数据集 - 确保测试数据来自较晚的时间点。

```python
split = data.get_split(method='temporal', seed=1)
```

* *何时使用：**
- 带有时间戳的数据集
- 模拟前瞻性预测
- 临床试验结果预测

### 自定义分割分数

```python
# 80% train, 10% valid, 10% test
split = data.get_split(method='scaffold', frac=[0.8, 0.1, 0.1])

# 70% train, 15% valid, 15% test
split = data.get_split(method='scaffold', frac=[0.7, 0.15, 0.15])
```

### 分层分割

对于具有不平衡标签的分类任务：

```python
split = data.get_split(method='scaffold', stratified=True)
```

在训练/有效/测试中保持标签分布2. 模型评估

TDC 为不同任务类型提供标准化评估指标。

### 评估器基本用法

```python
from tdc import Evaluator

# Initialize evaluator
evaluator = Evaluator(name='ROC-AUC')

# Evaluate predictions
score = evaluator(y_true, y_pred)
```

### 分类指标

#### ROC-AUC
接收器操作特性 -曲线下面积

```python
evaluator = Evaluator(name='ROC-AUC')
score = evaluator(y_true, y_pred_proba)
```

* *最适合：**
- 二元分类
- 不平衡数据集
- 整体判别能力

* *范围：** 0-1（越高越好，0.5 为随机）

#### PR-AUC
曲线下精确回忆区域

```python
evaluator = Evaluator(name='PR-AUC')
score = evaluator(y_true, y_pred_proba)
```

* *最适合：**
- 高度不平衡的数据集
- 当正类很少时
- 补充ROC-AUC

* *范围：** 0-1（越高越好）

#### F1 分数
精度和召回率的调和平均值

```python
evaluator = Evaluator(name='F1')
score = evaluator(y_true, y_pred_binary)
```

* *最适合：**
- 精度和召回率之间的平衡召回
- 多类分类

* *范围：** 0-1（越高越好）

#### 准确度
正确预测的分数

```python
evaluator = Evaluator(name='Accuracy')
score = evaluator(y_true, y_pred_binary)
```

* *最适合：**
- 平衡数据集
- 简单基线指标

* *不推荐用于：**不平衡数据集

#### Cohen's Kappa
预测和真实情况之间的协议，考虑机会

```python
evaluator = Evaluator(name='Kappa')
score = evaluator(y_true, y_pred_binary)
```

* *范围：** -1到1（更高更好，0 是随机的）

### 回归指标

#### RMSE - 均方根误差
```python
evaluator = Evaluator(name='RMSE')
score = evaluator(y_true, y_pred)
```

* *最适合：**
- 连续预测
- 严重惩罚大误差

* *范围：** 0-∞（越低越好）

#### MAE - 平均绝对值错误
```python
evaluator = Evaluator(name='MAE')
score = evaluator(y_true, y_pred)
```

* *最适合：**
- 连续预测
- 比RMSEZXXQNL10QXZ对异常值更稳健**范围：**0-∞（越低越好）

#### R² - 系数测定
```python
evaluator = Evaluator(name='R2')
score = evaluator(y_true, y_pred)
```

* *最适合：**
- 模型解释的方差
- 比较不同模型

* *范围：**-∞到1（越高越好，1是完美的）

#### MSE - 均方误差
```python
evaluator = Evaluator(name='MSE')
score = evaluator(y_true, y_pred)
```

* *范围：** 0-∞（越低越好）

### 排名指标

#### Spearman Correlation
Rank 相关性系数

```python
evaluator = Evaluator(name='Spearman')
score = evaluator(y_true, y_pred)
```

* *最适合：**
- 排名任务
- 非线性关系
- 序数数据

* *范围：** -1 到 1（越高越好）

#### Pearson相关性
线性相关系数

```python
evaluator = Evaluator(name='Pearson')
score = evaluator(y_true, y_pred)
```

* *最适合：**
- 线性关系
- 连续数据

* *范围：** -1到1（越高越好）

### 多标签分类

```python
evaluator = Evaluator(name='Micro-F1')
score = evaluator(y_true_multilabel, y_pred_multilabel)
```

可用：`Micro-F1`、`Macro-F1`、`Micro-AUPR`、`Macro-AUPR`

### 基准组评估

对于基准组，评估需要多个种子：

```python
from tdc.benchmark_group import admet_group

group = admet_group(path='data/')
benchmark = group.get('Caco2_Wang')

# Predictions must be dict with seeds as keys
predictions = {}
for seed in [1, 2, 3, 4, 5]:
    # Train model and predict
    predictions[seed] = model_predictions

# Evaluate with mean and std across seeds
results = group.evaluate(predictions)
print(results)  # {'Caco2_Wang': [mean_score, std_score]}
```

## 3.数据处理

TDC提供11个全面的数据处理实用程序。

### 分子格式转换

~15个分子之间的转换

```python
from tdc.chem_utils import MolConvert

# SMILES to PyTorch Geometric
converter = MolConvert(src='SMILES', dst='PyG')
pyg_graph = converter('CC(C)Cc1ccc(cc1)C(C)C(O)=O')

# SMILES to DGL
converter = MolConvert(src='SMILES', dst='DGL')
dgl_graph = converter('CC(C)Cc1ccc(cc1)C(C)C(O)=O')

# SMILES to Morgan Fingerprint (ECFP)
converter = MolConvert(src='SMILES', dst='ECFP')
fingerprint = converter('CC(C)Cc1ccc(cc1)C(C)C(O)=O')
```

* *可用格式：**
- **文本**：微笑、自拍、InChI
- **指纹**：ECFP (摩根)、MACCS、RDKit、AtomPair、拓扑扭转
- **图**：PyG (PyTorch Geometric)、DGL (Deep Graph Library)
- **3D**：Graph3D、库仑矩阵、距离矩阵

* *批量转换：**
```python
converter = MolConvert(src='SMILES', dst='PyG')
graphs = converter(['SMILES1', 'SMILES2', 'SMILES3'])
```

### 分子过滤器

使用精心设计的化学规则去除非药物分子。

```python
from tdc.chem_utils import MolFilter

# Initialize filter with rules
mol_filter = MolFilter(
    rules=['PAINS', 'BMS'],  # Chemical filter rules
    property_filters_dict={
        'MW': (150, 500),      # Molecular weight range
        'LogP': (-0.4, 5.6),   # Lipophilicity range
        'HBD': (0, 5),         # H-bond donors
        'HBA': (0, 10)         # H-bond acceptors
    }
)

# Filter molecules
filtered_smiles = mol_filter(smiles_list)
```

* *可用的过滤器规则：**
- `PAINS` - 泛检测干扰化合物
- `BMS` - Bristol-Myers Squibb HTS 甲板过滤器
- `Glaxo` - GlaxoSmithKline过滤器
- `Dundee` - University of Dundee 过滤器
- `Inpharmatica` - Inpharmatica 过滤器
- `LINT` - Pfizer LINT 过滤器

### 标签分布可视化

```python
# Visualize label distribution
data.label_distribution()

# Print statistics
data.print_stats()
```

显示直方图并计算连续标签的平均值、中位数、标准差。

### 标签二值化

使用阈值将连续标签转换为二进制。

```python
from tdc.utils import binarize

# Binarize with threshold
binary_labels = binarize(y_continuous, threshold=5.0, order='ascending')
# order='ascending': values >= threshold become 1
# order='descending': values <= threshold become 1
```

### 标签单位转换

测量之间的转换单位.

```python
from tdc.chem_utils import label_transform

# Convert nM to pKd
y_pkd = label_transform(y_nM, from_unit='nM', to_unit='p')

# Convert μM to nM
y_nM = label_transform(y_uM, from_unit='uM', to_unit='nM')
```

* *可用转换：**
- 结合亲和力：nM、μM、pKd、pKi、pIC50
- 对数转换
- 自然对数转换

### 标签含义

获取标签的可解释描述。

```python
# Get label mapping
label_map = data.get_label_map(name='DrugBank')
print(label_map)
# {0: 'No interaction', 1: 'Increased effect', 2: 'Decreased effect', ...}
```

### 数据平衡

通过过采样/欠采样处理类不平衡。

```python
from tdc.utils import balance

# Oversample minority class
X_balanced, y_balanced = balance(X, y, method='oversample')

# Undersample majority class
X_balanced, y_balanced = balance(X, y, method='undersample')
```

### 对的图形转换数据

将配对数据转换为图形表示。

```python
from tdc.utils import create_graph_from_pairs

# Create graph from drug-drug pairs
graph = create_graph_from_pairs(
    pairs=ddi_pairs,  # [(drug1, drug2, label), ...]
    format='edge_list'  # or 'PyG', 'DGL'
)
```

### 负采样

为二进制任务生成负样本。

```python
from tdc.utils import negative_sample

# Generate negative samples for DTI
negative_pairs = negative_sample(
    positive_pairs=known_interactions,
    all_drugs=drug_list,
    all_targets=target_list,
    ratio=1.0  # Negative:positive ratio
)
```

* *用例：**
- 药物目标相互作用预测
- 药物-药物相互作用任务
- 创建平衡数据集

### 实体检索

数据库标识符之间转换。

#### PubChem CID到SMILES
```python
from tdc.utils import cid2smiles

smiles = cid2smiles(2244)  # Aspirin
# Returns: 'CC(=O)Oc1ccccc1C(=O)O'
```

#### UniProt ID 转氨基酸序列
```python
from tdc.utils import uniprot2seq

sequence = uniprot2seq('P12345')
# Returns: 'MVKVYAPASS...'
```

#### 批量检索
```python
# Multiple CIDs
smiles_list = [cid2smiles(cid) for cid in [2244, 5090, 6323]]

# Multiple UniProt IDs
sequences = [uniprot2seq(uid) for uid in ['P12345', 'Q9Y5S9']]
```

## 4. 高级实用程序

### 检索数据集名称

```python
from tdc.utils import retrieve_dataset_names

# Get all datasets for a task
adme_datasets = retrieve_dataset_names('ADME')
dti_datasets = retrieve_dataset_names('DTI')
tox_datasets = retrieve_dataset_names('Tox')

print(f"ADME datasets: {adme_datasets}")
```

### 模糊搜索

TDC支持数据集名称的模糊匹配：

```python
from tdc.single_pred import ADME

# These all work (typo-tolerant)
data = ADME(name='Caco2_Wang')
data = ADME(name='caco2_wang')
data = ADME(name='Caco2')  # Partial match
```

### 数据格式选项

```python
# Pandas DataFrame (default)
df = data.get_data(format='df')

# Dictionary
data_dict = data.get_data(format='dict')

# DeepPurpose format (for DeepPurpose library)
dp_format = data.get_data(format='DeepPurpose')

# PyG/DGL graphs (if applicable)
graphs = data.get_data(format='PyG')
```

### 数据加载实用程序

```python
from tdc.utils import create_fold

# Create cross-validation folds
folds = create_fold(data, fold=5, seed=42)
# Returns list of (train_idx, test_idx) tuples

# Iterate through folds
for i, (train_idx, test_idx) in enumerate(folds):
    train_data = data.iloc[train_idx]
    test_data = data.iloc[test_idx]
    # Train and evaluate
```

## 常用工作流程

### 工作流程 1：完整数据管道

```python
from tdc.single_pred import ADME
from tdc import Evaluator
from tdc.chem_utils import MolConvert, MolFilter

# 1. Load data
data = ADME(name='Caco2_Wang')

# 2. Filter molecules
mol_filter = MolFilter(rules=['PAINS'])
filtered_data = data.get_data()
filtered_data = filtered_data[
    filtered_data['Drug'].apply(lambda x: mol_filter([x]))
]

# 3. Split data
split = data.get_split(method='scaffold', seed=42)
train, valid, test = split['train'], split['valid'], split['test']

# 4. Convert to graph representations
converter = MolConvert(src='SMILES', dst='PyG')
train_graphs = converter(train['Drug'].tolist())

# 5. Train model (user implements)
# model.fit(train_graphs, train['Y'])

# 6. Evaluate
evaluator = Evaluator(name='MAE')
# score = evaluator(test['Y'], predictions)
```

### 工作流程 2：多任务学习准备工作

```python
from tdc.benchmark_group import admet_group
from tdc.chem_utils import MolConvert

# Load benchmark group
group = admet_group(path='data/')

# Get multiple datasets
datasets = ['Caco2_Wang', 'HIA_Hou', 'Bioavailability_Ma']
all_data = {}

for dataset_name in datasets:
    benchmark = group.get(dataset_name)
    all_data[dataset_name] = benchmark

# Prepare for multi-task learning
converter = MolConvert(src='SMILES', dst='ECFP')
# Process each dataset...
```

### 工作流程 3：DTI 冷分裂评估

```python
from tdc.multi_pred import DTI
from tdc import Evaluator

# Load DTI data
data = DTI(name='BindingDB_Kd')

# Cold drug split
split = data.get_split(method='cold_drug', seed=42)
train, test = split['train'], split['test']

# Verify no drug overlap
train_drugs = set(train['Drug_ID'])
test_drugs = set(test['Drug_ID'])
assert len(train_drugs & test_drugs) == 0, "Drug leakage detected!"

# Train and evaluate
# model.fit(train)
evaluator = Evaluator(name='RMSE')
# score = evaluator(test['Y'], predictions)
```

## 最佳实践

1. **始终使用有意义的分割** - 使用支架或冷分割进行实际评估
2. **多个种子** - 使用多个种子进行实验以获得可靠的结果
3. **适当的指标** - 选择与您的任务和数据集特征相匹配的指标
4. **数据过滤** - 在训练
5之前删除PAINS和非药物分子。 **格式转换** - 将分子转换为适合您的模型 
6 的格式。 **批处理** - 使用批处理操作以提高大型数据集的效率

## 性能提示

- 以批处理模式转换分子以加快处理速度
- 缓存转换后的表示形式以避免重新计算
- 为您的框架使用适当的数据格式（PyG、DGL 等）
- 在管道中尽早过滤数据以减少计算

## 参考文献

- TDC 文档：https://tdc.readthedocs.io
- 数据函数：https://tdcommons.ai/fct_overview/
- 评估指标：https://tdcommons.ai/functions/model_eval/
- 数据拆分： https://tdcommons.ai/functions/data_split/
