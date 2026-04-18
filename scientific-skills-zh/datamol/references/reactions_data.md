# Datamol 反应和数据模块参考

## 反应模块 (`datamol.reactions`)

反应模块支持使用 SMARTS 反应模式以编程方式应用化学转化。

### 应用化学反应

#### `dm.reactions.apply_reaction(rxn, reactants, as_smiles=False, sanitize=True, single_product_group=True, rm_attach=True, product_index=0)`
对反应物应用化学反应molecular.
- **参数**：
  - `rxn`：反应对象（来自 SMARTS 模式）
  - `reactants`：反应物分子元组
  - `as_smiles`：返回 SMILES 字符串（True）或分子对象（False）
  - `sanitize`：消毒产品分子
  - `single_product_group`：返回单个产品（True）或所有产品组（False）
  - `rm_attach`：删除附着点标记
  - `product_index`：从反应中返回哪种产品
- **返回**：产品分子或 SMILES
- **示例**：
 ```python
 from rdkit import Chem

 # 定义反应：醇 + 羧酸 → 酯
rxn = Chem.rdChemReactions.ReactionFromSmarts(
 '[C:1][OH:2].[C:3](=[O:4])[OH:5]>>[C:1][O:2][C:3](=[O:4])'
 )

 # 适用于反应物
醇 = dm.to_mol("CCO")
 酸 = dm.to_mol("CC(=O)O")
 Product = dm.reactions.apply_reaction(rxn, (alcohol,acid))
 ```

### 创建反应

反应通常是使用 SMARTS 模式创建的RDKit:
```python
from rdkit.Chem import rdChemReactions

# Reaction pattern: [reactant1].[reactant2]>>[product]
rxn = rdChemReactions.ReactionFromSmarts(
    '[1*][*:1].[1*][*:2]>>[*:1][*:2]'
)
```

### 验证功能

该模块包括以下功能：
- **检查分子是否是反应物**：验证分子是否与反应物模式匹配
- **验证反应**：检查反应是否综合合理
- **处理反应文件**：从文件或数据库加载反应

### 常见反应模式

* *酰胺形成**：
```python
# Amine + carboxylic acid → amide
amide_rxn = rdChemReactions.ReactionFromSmarts(
    '[N:1].[C:2](=[O:3])[OH]>>[N:1][C:2](=[O:3])'
)
```

* *Suzuki偶联**：
```python
# Aryl halide + boronic acid → biaryl
suzuki_rxn = rdChemReactions.ReactionFromSmarts(
    '[c:1][Br].[c:2][B]([OH])[OH]>>[c:1][c:2]'
)
```

* *官能团转换**:
```python
# Alcohol → ester
esterification = rdChemReactions.ReactionFromSmarts(
    '[C:1][OH:2].[C:3](=[O:4])[Cl]>>[C:1][O:2][C:3](=[O:4])'
)
```

### 工作流程示例

```python
import datamol as dm
from rdkit.Chem import rdChemReactions

# 1. Define reaction
rxn_smarts = '[C:1](=[O:2])[OH:3]>>[C:1](=[O:2])[Cl:3]'  # Acid → acid chloride
rxn = rdChemReactions.ReactionFromSmarts(rxn_smarts)

# 2. Apply to molecule library
acids = [dm.to_mol(smi) for smi in acid_smiles_list]
acid_chlorides = []

for acid in acids:
    try:
        product = dm.reactions.apply_reaction(
            rxn,
            (acid,),  # Single reactant as tuple
            sanitize=True
        )
        acid_chlorides.append(product)
    except Exception as e:
        print(f"Reaction failed: {e}")

# 3. Validate products
valid_products = [p for p in acid_chlorides if p is not None]
```

### 关键概念

- **SMARTS**：SMiles ARbitrary 目标规范 - 反应的模式语言
- **原子映射**：像 [C:1]这样的数字通过反应保留原子身份
- **附着点**：[1*]表示通用连接点
- **反应验证**：并非所有 SMARTS 反应都是化学反应合理

- --

## 数据模块（`datamol.data`）

该数据模块提供了对用于测试和学习的精选分子数据集的便捷访问。

### 可用数据集

#### `dm.data.cdk2(as_df=True, mol_column='mol')`
RDKit CDK2数据集-激酶抑制剂data.
- **参数**：
  - `as_df`：返回为数据帧（True）或分子列表（False）
  - `mol_column`：分子列的名称
- **返回**：具有分子结构和活性数据的数据集
- **用例**：小数据集算法测试
- **示例**：
 ```python
 cdk2_df = dm.data.cdk2(as_df=True)
 print(cdk2_df.shape)
 print(cdk2_df.columns)
 ```

#### `dm.data.freesolv()`
FreeSolv 数据集 - 实验和计算的水合自由能。
- **内容**：642 个分子，其中：
  - IUPAC 名称
  - SMILES 字符串
  - 实验水合自由能值
  - 计算值
- **警告**：“仅用作教学和测试目的的玩具数据集”
- **不适合**：基准测试或生产模型训练
- **示例**：
 ```python
 freesolv_df = dm.data.freesolv()
 # 列：iupac、smiles、expt (kcal/mol)、calc (kcal/mol)
```

#### `dm.data.solubility(as_df=True, mol_column='mol')`
RDKit 溶解度数据集，包含训练/测试分割。
- **内容**：水具有预定义分割的溶解度数据
- **列**：包括具有“训练”或“测试”值的“分割”列
- **用例**：使用正确的训练/测试分离来测试 ML 工作流程
- **示例**：
 ```python
 sol_df = dm.data.solubility(as_df=True)

# 分割成train/test
train_df = sol_df[sol_df['split'] == 'train']
 test_df = sol_df[sol_df['split'] == 'test']

 # 用于模型开发
X_train = dm.to_fp(train_df[mol_column])
 y_train = train_df['solubility']
 ```

### 使用指南

* *用于测试和教程**：
```python
# Quick dataset for testing code
df = dm.data.cdk2()
mols = df['mol'].tolist()

# Test descriptor calculation
descriptors_df = dm.descriptors.batch_compute_many_descriptors(mols)

# Test clustering
clusters = dm.cluster_mols(mols, cutoff=0.3)
```

* *用于学习工作流程**：
```python
# Complete ML pipeline example
sol_df = dm.data.solubility()

# Preprocessing
train = sol_df[sol_df['split'] == 'train']
test = sol_df[sol_df['split'] == 'test']

# Featurization
X_train = dm.to_fp(train['mol'])
X_test = dm.to_fp(test['mol'])

# Model training (example)
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(X_train, train['solubility'])
predictions = model.predict(X_test)
```

### 重要说明

- **玩具数据集**：设计用于教学目的，而非生产用途
- **小尺寸**：适合快速测试的化合物数量有限
- **预处理**：数据已清理并formatted
- **引文**：如果发布

### 最佳实践

1，请检查数据集文档是否有正确的归属。 **仅用于开发**：不要从玩具数据集
2 中得出科学结论。 **验证真实数据**：始终在实际项目数据
3上测试生产代码。 **正确归属**：如果在出版物中使用，请引用原始数据源
4. **了解限制**：了解每个数据集的范围和质量
