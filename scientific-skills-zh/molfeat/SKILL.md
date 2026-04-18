---
name: molfeat
description: ML 的分子特征化（100 多个特征化器）。 ECFP、MACCS、描述符、预训练模型 (ChemBERTa)、将 SMILES 转换为特征，用于 QSAR 和分子 ML。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# Molfeat - 分子特征化中心

## 概述

Molfeat 是一个用于分子特征化的综合 Python 库，它统一了 100 多个预先训练的嵌入和手工制作的特征化器。将化学结构（SMILES 字符串或 RDKit 分子）转换为机器学习任务的数值表示，包括 QSAR 建模、虚拟筛选、相似性搜索和深度学习应用。具有快速并行处理、scikit-learn 兼容 transformers 和内置缓存的特点。

## 何时使用此技能

此技能应在处理以下内容时使用：
- **分子机器学习**：构建 QSAR/QSPR 模型、属性预测
- **虚拟筛选**：对生物的化合物库进行排名活动
- **相似性搜索**：查找结构相似的分子
- **化学空间分析**：聚类、可视化、降维
- **深度学习**：在分子数据上训练神经网络
- **特征化管道**：将SMILES转换为ML就绪表示
- **化学信息学**：任何需要分子特征提取的任务

## 安装

```bash
uv pip install molfeat

# With all optional dependencies
uv pip install "molfeat[all]"
```

* *特定特征器的可选依赖项：**
- `molfeat[dgl]` - GNN模型（GIN变体）
- `molfeat[graphormer]` - Graphhormer模型
- `molfeat[transformer]` - ChemBERTa、ChemGPT、MolT5
- `molfeat[fcd]` - FCD 描述符
- `molfeat[map4]` - MAP4 指纹

## 核心概念

Molfeat 将特征化组织为三个层次类：

### 1. 计算器 (`molfeat.calc`)

将单个分子转换为特征向量的可调用对象。接受 RDKit `Chem.Mol` 对象或 SMILES 字符串。

* *使用计算器：**
- 单分子特征化
- 自定义处理循环
- 直接特征计算

* *示例：**
```python
from molfeat.calc import FPCalculator

calc = FPCalculator("ecfp", radius=3, fpSize=2048)
features = calc("CCO")  # Returns numpy array (2048,)
```

### 2. Transformers (`molfeat.trans`)

Scikit-learn 兼容 transformers，包装计算器以进行并行化批处理。

* *使用 transformers用于：**
- 分子数据集的批量特征化
- 与 scikit-learn 管道集成
- 并行处理（自动 CPU 使用）

* *示例：**
```python
from molfeat.trans import MoleculeTransformer
from molfeat.calc import FPCalculator

transformer = MoleculeTransformer(FPCalculator("ecfp"), n_jobs=-1)
features = transformer(smiles_list)  # Parallel processing
```

### 3. 预训练 Transformers (`molfeat.trans.pretrained`)

专门用于具有批量推理和缓存功能的深度学习模型的transformers。

* *使用预训练的transformers用于：**
- 最先进的分子嵌入
- 大型化学品的迁移学习数据集
- 深度学习特征提取

* *示例：**
```python
from molfeat.trans.pretrained import PretrainedMolTransformer

transformer = PretrainedMolTransformer("ChemBERTa-77M-MLM", n_jobs=-1)
embeddings = transformer(smiles_list)  # Deep learning embeddings
```

## 快速启动工作流程

### 基本特征化

```python
import datamol as dm
from molfeat.calc import FPCalculator
from molfeat.trans import MoleculeTransformer

# Load molecular data
smiles = ["CCO", "CC(=O)O", "c1ccccc1", "CC(C)O"]

# Create calculator and transformer
calc = FPCalculator("ecfp", radius=3)
transformer = MoleculeTransformer(calc, n_jobs=-1)

# Featurize molecules
features = transformer(smiles)
print(f"Shape: {features.shape}")  # (4, 2048)
```

### 保存和加载配置

```python
# Save featurizer configuration for reproducibility
transformer.to_state_yaml_file("featurizer_config.yml")

# Reload exact configuration
loaded = MoleculeTransformer.from_state_yaml_file("featurizer_config.yml")
```

### 优雅地处理错误

```python
# Process dataset with potentially invalid SMILES
transformer = MoleculeTransformer(
    calc,
    n_jobs=-1,
    ignore_errors=True,  # Continue on failures
    verbose=True          # Log error details
)

features = transformer(smiles_with_errors)
# Returns None for failed molecules
```

## 选择正确的特征器

### 对于传统机器学习（RF、SVM、XGBoost）

* *从指纹：**
```python
# ECFP - Most popular, general-purpose
FPCalculator("ecfp", radius=3, fpSize=2048)

# MACCS - Fast, good for scaffold hopping
FPCalculator("maccs")

# MAP4 - Efficient for large-scale screening
FPCalculator("map4")
```

* *对于可解释模型：**
```python
# RDKit 2D descriptors (200+ named properties)
from molfeat.calc import RDKitDescriptors2D
RDKitDescriptors2D()

# Mordred (1800+ comprehensive descriptors)
from molfeat.calc import MordredDescriptors
MordredDescriptors()
```

* *组合多个特征器：**
```python
from molfeat.trans import FeatConcat

concat = FeatConcat([
    FPCalculator("maccs"),      # 167 dimensions
    FPCalculator("ecfp")         # 2048 dimensions
])  # Result: 2215-dimensional combined features
```

### 对于深度学习

* *基于变压器的嵌入：**
```python
# ChemBERTa - Pre-trained on 77M PubChem compounds
PretrainedMolTransformer("ChemBERTa-77M-MLM")

# ChemGPT - Autoregressive language model
PretrainedMolTransformer("ChemGPT-1.2B")
```

* *图神经网络：**
```python
# GIN models with different pre-training objectives
PretrainedMolTransformer("gin-supervised-masking")
PretrainedMolTransformer("gin-supervised-infomax")

# Graphormer for quantum chemistry
PretrainedMolTransformer("Graphormer-pcqm4mv2")
```

### 为了相似性搜索

```python
# ECFP - General purpose, most widely used
FPCalculator("ecfp")

# MACCS - Fast, scaffold-based similarity
FPCalculator("maccs")

# MAP4 - Efficient for large databases
FPCalculator("map4")

# USR/USRCAT - 3D shape similarity
from molfeat.calc import USRDescriptors
USRDescriptors()
```

### 基于药效基团的方法

```python
# FCFP - Functional group based
FPCalculator("fcfp")

# CATS - Pharmacophore pair distributions
from molfeat.calc import CATSCalculator
CATSCalculator(mode="2D")

# Gobbi - Explicit pharmacophore features
FPCalculator("gobbi2D")
```

## 常见工作流程

### 构建QSAR型号

```python
from molfeat.trans import MoleculeTransformer
from molfeat.calc import FPCalculator
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

# Featurize molecules
transformer = MoleculeTransformer(FPCalculator("ecfp"), n_jobs=-1)
X = transformer(smiles_train)

# Train model
model = RandomForestRegressor(n_estimators=100)
scores = cross_val_score(model, X, y_train, cv=5)
print(f"R² = {scores.mean():.3f}")

# Save configuration for deployment
transformer.to_state_yaml_file("production_featurizer.yml")
```

### 虚拟筛选管道

```python
from sklearn.ensemble import RandomForestClassifier

# Train on known actives/inactives
transformer = MoleculeTransformer(FPCalculator("ecfp"), n_jobs=-1)
X_train = transformer(train_smiles)
clf = RandomForestClassifier(n_estimators=500)
clf.fit(X_train, train_labels)

# Screen large library
X_screen = transformer(screening_library)  # e.g., 1M compounds
predictions = clf.predict_proba(X_screen)[:, 1]

# Rank and select top hits
top_indices = predictions.argsort()[::-1][:1000]
top_hits = [screening_library[i] for i in top_indices]
```

### 相似性搜索

```python
from sklearn.metrics.pairwise import cosine_similarity

# Query molecule
calc = FPCalculator("ecfp")
query_fp = calc(query_smiles).reshape(1, -1)

# Database fingerprints
transformer = MoleculeTransformer(calc, n_jobs=-1)
database_fps = transformer(database_smiles)

# Compute similarity
similarities = cosine_similarity(query_fp, database_fps)[0]
top_similar = similarities.argsort()[-10:][::-1]
```

### Scikit-learn 管道集成

```python
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# Create end-to-end pipeline
pipeline = Pipeline([
    ('featurizer', MoleculeTransformer(FPCalculator("ecfp"), n_jobs=-1)),
    ('classifier', RandomForestClassifier(n_estimators=100))
])

# Train and predict directly on SMILES
pipeline.fit(smiles_train, y_train)
predictions = pipeline.predict(smiles_test)
```

### 比较多个特征器

```python
featurizers = {
    'ECFP': FPCalculator("ecfp"),
    'MACCS': FPCalculator("maccs"),
    'Descriptors': RDKitDescriptors2D(),
    'ChemBERTa': PretrainedMolTransformer("ChemBERTa-77M-MLM")
}

results = {}
for name, feat in featurizers.items():
    transformer = MoleculeTransformer(feat, n_jobs=-1)
    X = transformer(smiles)
    # Evaluate with your ML model
    score = evaluate_model(X, y)
    results[name] = score
```

## 发现可用的特征器

使用ModelStore探索所有可用的特征器featurizers:

```python
from molfeat.store.modelstore import ModelStore

store = ModelStore()

# List all available models
all_models = store.available_models
print(f"Total featurizers: {len(all_models)}")

# Search for specific models
chemberta_models = store.search(name="ChemBERTa")
for model in chemberta_models:
    print(f"- {model.name}: {model.description}")

# Get usage information
model_card = store.search(name="ChemBERTa-77M-MLM")[0]
model_card.usage()  # Display usage examples

# Load model
transformer = store.load("ChemBERTa-77M-MLM")
```

## 高级功能

### 自定义预处理

```python
class CustomTransformer(MoleculeTransformer):
    def preprocess(self, mol):
        """Custom preprocessing pipeline"""
        if isinstance(mol, str):
            mol = dm.to_mol(mol)
        mol = dm.standardize_mol(mol)
        mol = dm.remove_salts(mol)
        return mol

transformer = CustomTransformer(FPCalculator("ecfp"), n_jobs=-1)
```

### 批量处理大型数据集

```python
def featurize_in_chunks(smiles_list, transformer, chunk_size=10000):
    """Process large datasets in chunks to manage memory"""
    all_features = []
    for i in range(0, len(smiles_list), chunk_size):
        chunk = smiles_list[i:i+chunk_size]
        features = transformer(chunk)
        all_features.append(features)
    return np.vstack(all_features)
```

### 缓存昂贵的嵌入

```python
import pickle

cache_file = "embeddings_cache.pkl"
transformer = PretrainedMolTransformer("ChemBERTa-77M-MLM", n_jobs=-1)

try:
    with open(cache_file, "rb") as f:
        embeddings = pickle.load(f)
except FileNotFoundError:
    embeddings = transformer(smiles_list)
    with open(cache_file, "wb") as f:
        pickle.dump(embeddings, f)
```

## 性能提示

1. **使用并行化**：设置 `n_jobs=-1` 以利用所有 CPU 核心 
2. **批处理**：一次处理多个分子而不是循环
3. **选择合适的特征器**：指纹比深度学习模型
4更快。 **缓存预训练模型**：利用内置缓存进行重复使用
5. **使用float32**：精度允许时设置`dtype=np.float32`
6. **高效处理错误**：对大型数据集使用 `ignore_errors=True`

## 常用特征器参考

* *常用特征器快速参考：**

|特征化器 |类型 |尺寸|速度|使用案例|
|------------|-----|------------|--------|----------|
| `ecfp` |指纹| 2048 | 2048快|通用|
| `maccs` |指纹| 167 | 167非常快|支架相似度|
| `desc2D` |描述符| 200+ |快|可解释模型|
| `mordred` |描述符| 1800+ |中等|综合功能|
| `map4` |指纹| 1024 | 1024快|大型筛选|
| `ChemBERTa-77M-MLM` |深度学习 | 768 | 768慢* |迁移学习|
| `gin-supervised-masking` | GNN |变量|慢* |基于图的模型|

* 第一次运行很慢；后续运行受益于缓存

## 资源

此技能包括全面的参考文档：

### 引用/api_reference.md
完整的API文档涵盖：
- `molfeat.calc` - 所有计算器类和参数
- `molfeat.trans` - Transformer 类和方法
- `molfeat.store` - ModelStore 使用
- 常见模式和集成示例
- 性能优化技巧

* *何时加载：** 实现特定计算器、了解变压器参数或与scikit-learn/PyTorch 集成时的参考。

### references/available_featurizers.md
按类别组织的所有 100 多个特征器的综合目录：
- 基于 Transformer 的语言模型（ChemBERTa、ChemGPT）
- 图神经网络（GIN、Graphormer）
- 分子描述符（RDKit、 Mordred)
- 指纹（ECFP、MACCS、MAP4 和 15+ 其他）
- 药效团描述符（CATS、Gobbi）
- 形状描述符（USR、ElectroShape）
- 基于支架的描述符

* *何时加载：** 选择最佳特征化器时的参考

* *搜索提示：** 使用 grep 查找特定特征器类型：
```bash
grep -i "chembert" references/available_featurizers.md
grep -i "pharmacophore" references/available_featurizers.md
```

### 引用/示例.md
常见场景的实用代码示例：
- 安装和快速入门
- 计算器和转换器示例
- 预训练模型使用
- Scikit-learn 和 PyTorch 集成
- 虚拟筛选工作流程
- QSAR 模型构建
- 相似性搜索
- 故障排除和最佳实践

* *何时加载：**实现特定工作流程、故障排除问题或学习 molfeat 模式时的参考。

## 故障排除

### 无效分子
启用错误处理以跳过无效 SMILES：
```python
transformer = MoleculeTransformer(
    calc,
    ignore_errors=True,
    verbose=True
)
```

### 大内存问题数据集
对> 100K分子的数据集进行分块处理或使用流式处理方法。

### 预训练模型依赖项
某些模型需要额外的包。安装特定附加功能：
```bash
uv pip install "molfeat[transformer]"  # For ChemBERTa/ChemGPT
uv pip install "molfeat[dgl]"          # For GIN models
```

### 再现性
保存准确的配置和文档版本：
```python
transformer.to_state_yaml_file("config.yml")
import molfeat
print(f"molfeat version: {molfeat.__version__}")
```

## 其他资源

- **官方文档**：https://molfeat-docs.datamol.io/
- **GitHub 存储库**：https://github.com/datamol-io/molfeat
- **PyPI 包**：https://pypi.org/project/molfeat/
- **教程**： https://portal.valencelabs.com/datamol/post/types-of-featurizers-b1e8HHrbFMkbun6
