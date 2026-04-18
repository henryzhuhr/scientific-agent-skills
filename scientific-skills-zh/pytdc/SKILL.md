---
name: pytdc
description: 治疗数据共享。 AI 就绪药物发现数据集（ADME、毒性、DTI）、基准、支架分割、分子预言，用于治疗性 ML 和药理学预测。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# PyTDC（治疗数据共享）

## 概述

PyTDC 是一个开放科学平台，为药物发现和开发提供 AI 就绪数据集和基准。通过标准化评估指标和有意义的数据分割访问涵盖整个治疗流程的精选数据集，这些数据集分为三类：单实例预测（分子/蛋白质属性）、多实例预测（药物-靶点相互作用，DDI）和生成（分子生成、逆合成）。

## 何时使用此技能

此技能应在以下情况下使用：
- 使用药物发现或治疗性机器学习数据集
- 在标准化制药任务上对机器学习模型进行基准测试
- 预测分子特性（ADME、毒性、生物活性）
- 预测药物-靶标或药物-药物相互作用
- 生成具有所需特性的新型分子
- 通过适当的训练/测试拆分（支架、 Cold-split)
- 使用分子预言机进行属性优化

## 安装和设置

使用 pip 安装 PyTDC:

```bash
uv pip install PyTDC
```

 升级到最新版本：

```bash
uv pip install PyTDC --upgrade
```

核心依赖（自动安装）：
- numpy、pandas、tqdm、seaborn、scikit_learn、fuzzywuzzy

根据特定功能的需要自动安装其他软件包。

## Quick开始

访问任何TDC数据集的基本模式遵循以下结构：

```python
from tdc.<problem> import <Task>
data = <Task>(name='<Dataset>')
split = data.get_split(method='scaffold', seed=1, frac=[0.7, 0.1, 0.2])
df = data.get_data(format='df')
```

其中：
- `<problem>`：`single_pred`、`multi_pred`或`generation`
之一`<Task>`：特定任务类别（例如 ADME、DTI、MolGen）
- `<Dataset>`：该任务中的数据集名称

* *示例 - 加载 ADME 数据：**

```python
from tdc.single_pred import ADME
data = ADME(name='Caco2_Wang')
split = data.get_split(method='scaffold')
# Returns dict with 'train', 'valid', 'test' DataFrames
```

## 单实例预测任务

单实例预测涉及预测单个生物医学实体（分子、蛋白质等）的特性。

### 可用任务类别

#### 1. ADME（吸收、分布、代谢、排泄）

预测药物分子的药代动力学特性。

```python
from tdc.single_pred import ADME
data = ADME(name='Caco2_Wang')  # Intestinal permeability
# Other datasets: HIA_Hou, Bioavailability_Ma, Lipophilicity_AstraZeneca, etc.
```

* *常用ADME数据集：**
- Caco2 - 肠道通透性
- HIA -人体肠道吸收
- 生物利用度-口服生物利用度
- 亲脂性-辛醇-水分配系数
- 溶解度-水溶解度
- BBB-血脑屏障渗透
- CYP-细胞色素P450代谢

#### 2.毒性（Tox）

预测化合物的毒性和不良反应。

```python
from tdc.single_pred import Tox
data = Tox(name='hERG')  # Cardiotoxicity
# Other datasets: AMES, DILI, Carcinogens_Lagunin, etc.
```

* *常见毒性数据集：**
- hERG - 心脏毒性
- AMES - 致突变性
- DILI - 药物诱导的肝脏损伤
- 致癌物 - 致癌性
- ClinTox - 临床试验毒性

#### 3. HTS（高通量筛选）

根据筛选数据预测生物活性。

```python
from tdc.single_pred import HTS
data = HTS(name='SARSCoV2_Vitro_Touret')
```

#### 4. QM（量子）力学）

分子的量子力学性质。

```python
from tdc.single_pred import QM
data = QM(name='QM7')
```

#### 5.其他单一预测任务

- **产量**：化学反应产量预测
- **表位**：生物制剂的表位预测
- **开发**：发育阶段预测
- **CRISPROutcome**：基因编辑结果预测

### 数据格式

单一预测数据集通常返回包含以下列的DataFrame：
- `Drug_ID` 或`Compound_ID`：唯一标识符
- `Drug` 或`X`：SMILES 字符串或分子表示
- `Y`：目标标签（连续或二进制）

## 多实例预测任务

多实例预测涉及预测多个生物医学实体之间相互作用的属性。

### 可用任务类别

#### 1. DTI（药物-靶标相互作用）

预测药物与蛋白质靶标之间的结合亲和力。

```python
from tdc.multi_pred import DTI
data = DTI(name='BindingDB_Kd')
split = data.get_split()
```

* *可用数据集：**
- BindingDB_Kd - 解离常数（52,284 对）
- BindingDB_IC50 - 半最大抑制浓度（991,486 对）
- BindingDB_Ki - 抑制常数(375,032 对)
- DAVIS, KIBA - 激酶结合数据集

* *数据格式：** Drug_ID, Target_ID, Drug (SMILES), Target (序列), Y (结合亲和力)

#### 2. DDI (药物-药物相互作用)

预测药物之间的相互作用pairs.

```python
from tdc.multi_pred import DDI
data = DDI(name='DrugBank')
split = data.get_split()
```

多类分类任务预测交互类型。数据集包含 191,808 个 DDI 对和 1,706 种药物。

#### 3. PPI（蛋白质-蛋白质相互作用）

预测蛋白质-蛋白质相互作用。

```python
from tdc.multi_pred import PPI
data = PPI(name='HuRI')
```

#### 4. 其他多重预测任务

- **GDA**：基因-疾病关联
- **DrugRes**：耐药性预测
- **DrugSyn**：药物协同作用预测
- **PeptideMHC**：肽-MHC结合
- **AntibodyAff**：抗体亲和力预测
- **MTI**： miRNA-靶标相互作用
- **催化剂**：催化剂预测
- **试验结果**：临床试验结果预测

## 生成任务

生成任务涉及创建具有所需特性的新型生物医学实体。

### 1. 分子生成(MolGen)

生成具有所需化学性质的多样化新颖分子。

```python
from tdc.generation import MolGen
data = MolGen(name='ChEMBL_V29')
split = data.get_split()
```

 与预言机一起使用以优化特定属性：

```python
from tdc import Oracle
oracle = Oracle(name='GSK3B')
score = oracle('CC(C)Cc1ccc(cc1)C(C)C(O)=O')  # Evaluate SMILES
```

有关所有可用的预言机，请参阅 `references/oracles.md`函数。

### 2. 逆合成 (RetroSyn)

预测合成目标分子所需的反应物。

```python
from tdc.generation import RetroSyn
data = RetroSyn(name='USPTO')
split = data.get_split()
```

 数据集包含来自 USPTO 数据库的 1,939,253 个反应。

### 3. 配对分子Generation

生成分子对（例如前药-药物对）。

```python
from tdc.generation import PairMolGen
data = PairMolGen(name='Prodrug')
```

详细的预言机文档和分子生成工作流程，请参阅`references/oracles.md`和`scripts/molecular_generation.py`。

## 基准组

基准组为系统模型评估提供相关数据集的精选集合。

### ADMET 基准组

```python
from tdc.benchmark_group import admet_group
group = admet_group(path='data/')

# Get benchmark datasets
benchmark = group.get('Caco2_Wang')
predictions = {}

for seed in [1, 2, 3, 4, 5]:
    train, valid = benchmark['train'], benchmark['valid']
    # Train model here
    predictions[seed] = model.predict(benchmark['test'])

# Evaluate with required 5 seeds
results = group.evaluate(predictions)
```

* *ADMET 组包括 22 个数据集**，涵盖吸收、分布、代谢、排泄和毒性。

### 其他基准组

可用的基准组包括集合：
- ADMET 属性
- 药物-靶点相互作用
- 药物组合预测
- 以及更多专门的治疗任务

有关基准评估工作流程，请参阅`scripts/benchmark_evaluation.py`.

## 数据功能

TDC 提供了分为四个部分的综合数据处理实用程序categories.

### 1.数据集分割

使用各种策略检索训练/验证/测试分区：

```python
# Scaffold split (default for most tasks)
split = data.get_split(method='scaffold', seed=1, frac=[0.7, 0.1, 0.2])

# Random split
split = data.get_split(method='random', seed=42, frac=[0.8, 0.1, 0.1])

# Cold split (for DTI/DDI tasks)
split = data.get_split(method='cold_drug', seed=1)  # Unseen drugs in test
split = data.get_split(method='cold_target', seed=1)  # Unseen targets in test
```

* *可用的分割策略：**
- `random`：随机洗牌
- `scaffold`：基于支架（用于化学多样性）
- `cold_drug`、`cold_target`、`cold_drug_target`：用于 DTI 任务
- `temporal`：时间数据集的基于时间的分割

### 2. 模型评估

使用标准化指标进行评估：

```python
from tdc import Evaluator

# For binary classification
evaluator = Evaluator(name='ROC-AUC')
score = evaluator(y_true, y_pred)

# For regression
evaluator = Evaluator(name='RMSE')
score = evaluator(y_true, y_pred)
```

* *可用指标：** ROC-AUC、PR-AUC、F1、Accuracy、RMSE、MAE、R2、Spearman、Pearson等。

### 3.数据处理

TDC提供11个关键处理实用程序：

```python
from tdc.chem_utils import MolConvert

# Molecule format conversion
converter = MolConvert(src='SMILES', dst='PyG')
pyg_graph = converter('CC(C)Cc1ccc(cc1)C(C)C(O)=O')
```

* *处理实用程序包括：**
- 分子格式转换（SMILES、SELFIES、PyG、DGL、ECFP等）
- 分子过滤器（PAINS、药物相似性）
- 标签二值化和单位转换
- 数据平衡（过采样/欠采样）
- 对数据的负采样
- 图形转换
- 实体检索（CID 到 SMILES，UniProt 到序列）

 有关综合实用程序文档，请参阅 `references/utilities.md`.

### 4.分子生成预言机

TDC提供了17+预言机函数用于分子优化：

```python
from tdc import Oracle

# Single oracle
oracle = Oracle(name='DRD2')
score = oracle('CC(C)Cc1ccc(cc1)C(C)C(O)=O')

# Multiple oracles
oracle = Oracle(name='JNK3')
scores = oracle(['SMILES1', 'SMILES2', 'SMILES3'])
```

完整的预言机文档，请参见`references/oracles.md`.

## 高级功能

### 检索可用数据集

```python
from tdc.utils import retrieve_dataset_names

# Get all ADME datasets
adme_datasets = retrieve_dataset_names('ADME')

# Get all DTI datasets
dti_datasets = retrieve_dataset_names('DTI')
```

### 标签转换

```python
# Get label mapping
label_map = data.get_label_map(name='DrugBank')

# Convert labels
from tdc.chem_utils import label_transform
transformed = label_transform(y, from_unit='nM', to_unit='p')
```

### 数据库查询

```python
from tdc.utils import cid2smiles, uniprot2seq

# Convert PubChem CID to SMILES
smiles = cid2smiles(2244)

# Convert UniProt ID to amino acid sequence
sequence = uniprot2seq('P12345')
```

## 常见工作流程

### 工作流程 1：训练单个预测模型

请参阅 `scripts/load_and_split_data.py` 了解完整示例：

```python
from tdc.single_pred import ADME
from tdc import Evaluator

# Load data
data = ADME(name='Caco2_Wang')
split = data.get_split(method='scaffold', seed=42)

train, valid, test = split['train'], split['valid'], split['test']

# Train model (user implements)
# model.fit(train['Drug'], train['Y'])

# Evaluate
evaluator = Evaluator(name='MAE')
# score = evaluator(test['Y'], predictions)
```

### 工作流程 2：基准评估

请参阅 `scripts/benchmark_evaluation.py` 了解具有多个种子和正确评估的完整示例协议.

### 工作流程 3：使用 Oracle 进行分子生成

有关使用 Oracle 函数进行目标定向生成的示例，请参阅 `scripts/molecular_generation.py`。

## 资源

此技能包括常见 TDC 工作流程的捆绑资源：

### 脚本/

- `load_and_split_data.py`：用于使用各种策略加载和分割 TDC 数据集的模板
- `benchmark_evaluation.py`：用于使用适当的 5 种子协议运行基准组评估的模板
- `molecular_generation.py`：使用预言函数进行分子生成的模板

### 参考文献/

- `datasets.md`：按任务类型组织的所有可用数据集的综合目录
- `oracles.md`：所有17+分子生成预言机的完整文档
- `utilities.md`：数据处理、分割和评估实用程序的详细指南

## 其他资源

- **官方网站**： https://tdcommons.ai
- **文档**：https://tdc.readthedocs.io
- **GitHub**：https://github.com/mims-harvard/TDC
- **论文**：NeurIPS 2021 - “治疗数据共享：用于药物发现和治疗的机器学习数据集和任务开发“
