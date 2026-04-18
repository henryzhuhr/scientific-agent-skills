# Molfeat API 参考

## 核心模块

Molfeat 被组织成几个关键模块，提供分子特征化的不同方面：

- **`molfeat.store`** - 管理模型加载、列表和注册
- **`molfeat.calc`** - 提供单分子计算器featurization
- **`molfeat.trans`** - 提供 scikit-learn 兼容的 transformers 用于批处理
- **`molfeat.utils`** - 用于数据处理的实用函数
- **`molfeat.viz`** - 分子可视化工具features

- --

## molfeat.calc - 计算器

计算器是将单个分子转换为特征向量的可调用对象。它们接受 RDKit `Chem.Mol` 对象或 SMILES 字符串作为输入。

### SerializedCalculator（基类）

所有计算器的基本抽象类。子类化时，必须实现：
- `__call__()` - 特征化所需的方法
- `__len__()` - 可选，返回输出长度
- `columns` - 可选属性，返回特征名称
- `batch_compute()` - 可选，用于高效批处理处理

* *状态管理方法：**
- `to_state_json()` - 将计算器状态保存为 JSON
- `to_state_yaml()` - 将计算器状态保存为 YAML
- `from_state_dict()` - 从状态字典加载计算器
- `to_state_dict()` - 导出计算器状态为字典

### FPCalculator

计算分子指纹。支持 15 种以上指纹方法。

* *支持的指纹类型：**

* *结构指纹：**
- `ecfp` - 扩展连接指纹（圆形）
- `fcfp` - 功能级指纹
- `rdkit` - RDKit 拓扑指纹
- `maccs` - MACCS 密钥（166 位结构密钥）
- `avalon` - Avalon 指纹
- `pattern` - 模式指纹
- `layered` - 分层指纹

* *基于原子的指纹：**
- `atompair` - 原子对指纹
- `atompair-count` - 计数的原子对
- `topological` - 拓扑扭转指纹
- `topological-count` - 计数的拓扑扭转

* *专用指纹：**
- `map4` - 最多 4 个键的 MinHashed 原子对指纹
- `secfp` - SMILES 扩展连接指纹
- `erg` - 扩展简化图
- `estate` - 电拓扑状态指数

* *参数：**
- `method` (str) - 指纹类型名称
- `radius` (int) - 圆形指纹的半径（默认值：3）
- `fpSize` (int) -指纹大小（默认：2048）
- `includeChirality` (bool) - 包含手性信息
- `counting` (bool) - 使用计数向量而不是二进制

* *用法：**
```python
from molfeat.calc import FPCalculator

# Create fingerprint calculator
calc = FPCalculator("ecfp", radius=3, fpSize=2048)

# Compute fingerprint for single molecule
fp = calc("CCO")  # Returns numpy array

# Get fingerprint length
length = len(calc)  # 2048

# Get feature names
names = calc.columns
```

* *通用指纹尺寸：**
- MACCS：167 尺寸
- ECFP（默认）：2048 尺寸
- MAP4（默认）：1024 尺寸

### 描述符计算器

* *RDKitDescriptors2D**
 计算使用 RDKit.

```python
from molfeat.calc import RDKitDescriptors2D

calc = RDKitDescriptors2D()
descriptors = calc("CCO")  # Returns 200+ descriptors
```

* *RDKitDescriptors3D**
 计算 3D 分子描述符（需要构象异构体生成）。

* *MordredDescriptors**
 计算超过 1800 个分子描述符使用Mordred.

```python
from molfeat.calc import MordredDescriptors

calc = MordredDescriptors()
descriptors = calc("CCO")
```

### 药效计算器

* *Pharmacophore2D**
RDKit的2D药效团指纹生成。

* *Pharmacophore3D**
来自多个的一致药效团指纹

* *CATS计算器**
计算化学高级模板搜索（CATS）描述符 - 药效团点对分布。

* *参数：**
- `mode` - “2D”或“3D”距离计算
- `dist_bins` -对分布的距离箱
- `scale` - 缩放模式：“raw”、“num”或“count”

```python
from molfeat.calc import CATSCalculator

calc = CATSCalculator(mode="2D", scale="raw")
cats = calc("CCO")  # Returns 21 descriptors by default
```

### 形状描述符

* *USRDescriptors**
超快形状识别描述符（多个变体）。

* *ElectroShapeDescriptors**
结合形状、手性和静电的静电形状描述符。

### 基于图形计算器

* *ScaffoldKey计算器**
计算40多种基于支架的分子属性。

* *Atom计算器**
图神经网络的原子级特征化。

* *BondCalculator**
图神经网络的债券级特征化networks.

### 实用函数

* *get_calculator()**
按名称实例化计算器的工厂函数。

```python
from molfeat.calc import get_calculator

# Instantiate any calculator by name
calc = get_calculator("ecfp", radius=3)
calc = get_calculator("maccs")
calc = get_calculator("desc2D")
```

针对不支持的情况提高`ValueError` featurizers.

- --

## molfeat.trans - Transformers

Transformers 将计算器包装到完整的特征化管道中以进行批处理。

### MoleculeTransformer

Scikit-learn 批量分子兼容变压器featurization.

* *关键参数：**
- `featurizer` - 要使用的计算器或特征器
- `n_jobs` (int) - 并行作业数量（所有内核为-1）
- `dtype` - 输出数据类型（numpy float32/64，火炬张量)
- `verbose` (bool) - 启用详细日志记录
- `ignore_errors` (bool) - 失败时继续（失败的分子返回 None）

* *基本方法：**
- `transform(mols)` - 处理批次并返回表示
- `_transform(mol)` - 处理单个分子特征化
- `__call__(mols)` - 围绕transform()的便捷包装器
- `preprocess(mol)` - 准备输入分子（不自动应用）
- `to_state_yaml_file(path)` - 保存变压器配置
- `from_state_yaml_file(path)` - 负载变压器配置

* *用法：**
```python
from molfeat.calc import FPCalculator
from molfeat.trans import MoleculeTransformer
import datamol as dm

# Load molecules
smiles = dm.data.freesolv().sample(100).smiles.values

# Create transformer
calc = FPCalculator("ecfp")
transformer = MoleculeTransformer(calc, n_jobs=-1)

# Featurize batch
features = transformer(smiles)  # Returns numpy array (100, 2048)

# Save configuration
transformer.to_state_yaml_file("ecfp_config.yml")

# Reload
transformer = MoleculeTransformer.from_state_yaml_file("ecfp_config.yml")
```

* *性能：**对642个分子进行的测试显示，与单线程处理相比，使用4个并行作业可实现3.4倍的加速。

### FeatConcat

将多个特征化器连接成统一的表示。

```python
from molfeat.trans import FeatConcat
from molfeat.calc import FPCalculator

# Combine multiple fingerprints
concat = FeatConcat([
    FPCalculator("maccs"),      # 167 dimensions
    FPCalculator("ecfp")         # 2048 dimensions
])

# Result: 2167-dimensional features
transformer = MoleculeTransformer(concat, n_jobs=-1)
features = transformer(smiles)
```

### PretrainedMolTransformer

`MoleculeTransformer` 的子类，用于预训练深度学习模型。

* *独特功能：**
- `_embed()` - 神经网络的批量推理
- `_convert()` - 将 SMILES/分子转换为模型兼容的格式
  - 用于语言模型的 SELFIES 字符串
  - 用于图形神经网络的 DGL 图
  - 用于高效的集成缓存系统storage

* *用法：**
```python
from molfeat.trans.pretrained import PretrainedMolTransformer

# Load pretrained model
transformer = PretrainedMolTransformer("ChemBERTa-77M-MLM", n_jobs=-1)

# Generate embeddings
embeddings = transformer(smiles)
```

### PrecompulatedMolTransformer

用于缓存/预计算功能的变压器。

- --

## molfeat.store - 模型 Store

管理特征器发现、加载和注册。

### ModelStore

用于访问可用特征器的中央集线器。

* *关键方法：**
- `available_models` - 列出所有可用特征器的属性
- `search(name=None, **kwargs)` - 搜索特定特征器featurizers
- `load(name, **kwargs)` - 按名称加载特征器
- `register(name, card)` - 注册自定义特征器

* *用法：**
```python
from molfeat.store.modelstore import ModelStore

# Initialize store
store = ModelStore()

# List all available models
all_models = store.available_models
print(f"Found {len(all_models)} featurizers")

# Search for specific model
results = store.search(name="ChemBERTa-77M-MLM")
if results:
    model_card = results[0]

    # View usage information
    model_card.usage()

    # Load the model
    transformer = model_card.load()

# Direct loading
transformer = store.load("ChemBERTa-77M-MLM")
```

* *ModelCard属性：**
- `name` - 模型标识符
- `description` - 模型描述
- `version` - 模型版本
- `authors` - 模型作者
- `tags` -分类标签
- `usage()` - 显示使用示例
- `load(**kwargs)` - 加载模型

- --

## 常见模式

### 错误处理

```python
# Enable error tolerance
featurizer = MoleculeTransformer(
    calc,
    n_jobs=-1,
    verbose=True,
    ignore_errors=True
)

# Failed molecules return None
features = featurizer(smiles_with_errors)
```

### 数据类型控制

```python
# NumPy float32 (default)
features = transformer(smiles, enforce_dtype=True)

# PyTorch tensors
import torch
transformer = MoleculeTransformer(calc, dtype=torch.float32)
features = transformer(smiles)
```

### 持久性和再现性

```python
# Save transformer state
transformer.to_state_yaml_file("config.yml")
transformer.to_state_json_file("config.json")

# Load from saved state
transformer = MoleculeTransformer.from_state_yaml_file("config.yml")
transformer = MoleculeTransformer.from_state_json_file("config.json")
```

### 预处理

```python
# Manual preprocessing
mol = transformer.preprocess("CCO")

# Transform with preprocessing
features = transformer.transform(smiles_list)
```

- --

## 集成示例

### Scikit-learn 管道

```python
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from molfeat.trans import MoleculeTransformer
from molfeat.calc import FPCalculator

# Create pipeline
pipeline = Pipeline([
    ('featurizer', MoleculeTransformer(FPCalculator("ecfp"))),
    ('classifier', RandomForestClassifier())
])

# Fit and predict
pipeline.fit(smiles_train, y_train)
predictions = pipeline.predict(smiles_test)
```

### PyTorch 集成

```python
import torch
from torch.utils.data import Dataset, DataLoader
from molfeat.trans import MoleculeTransformer

class MoleculeDataset(Dataset):
    def __init__(self, smiles, labels, transformer):
        self.smiles = smiles
        self.labels = labels
        self.transformer = transformer

    def __len__(self):
        return len(self.smiles)

    def __getitem__(self, idx):
        features = self.transformer(self.smiles[idx])
        return torch.tensor(features), torch.tensor(self.labels[idx])

# Create dataset and dataloader
transformer = MoleculeTransformer(FPCalculator("ecfp"))
dataset = MoleculeDataset(smiles, labels, transformer)
loader = DataLoader(dataset, batch_size=32)
```

- --

## 性能提示

1. **并行化**：使用`n_jobs=-1`来利用所有CPU核心
2. **批处理**：一次处理多个分子而不是循环
3. **缓存**：利用预训练模型 
4 的内置缓存。 **数据类型**：当精度允许
5时，使用float32而不是float64。 **错误处理**：为具有潜在无效分子的大型数据集设置 `ignore_errors=True`
