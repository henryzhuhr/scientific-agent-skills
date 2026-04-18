# Datamol 片段和支架参考

## 支架模块 (`datamol.scaffold`)

支架代表分子的核心结构，可用于识别结构家族和分析构效关系 (SAR)。

### Murcko Scaffolds

#### `dm.to_scaffold_murcko(mol)`
提取Bemis-Murcko支架（分子框架）。
- **方法**：去除侧链、固定环系统和接头
- **返回**：代表支架的分子对象
- **用例**：识别化合物系列的核心结构
- **示例**：
 ```python
 mol = dm.to_mol("c1ccc(cc1)CCN") # 苯乙胺
 脚手架 = dm.to_scaffold_murcko(mol)
scaffold_smiles = dm.to_smiles(scaffold)
 # 返回: 'c1ccccc1CC' (苯环 + 乙基连接体)
```

* *支架分析工作流程**:
```python
# Extract scaffolds from compound library
scaffolds = [dm.to_scaffold_murcko(mol) for mol in mols]
scaffold_smiles = [dm.to_smiles(s) for s in scaffolds]

# Count scaffold frequency
from collections import Counter
scaffold_counts = Counter(scaffold_smiles)
most_common = scaffold_counts.most_common(10)
```

### Fuzzy支架

#### `dm.scaffold.fuzzy_scaffolding(mol, ...)`
生成具有必须出现在核心中的可执行组的模糊支架。
- **目的**：允许指定功能组的更灵活的支架定义
- **用例**：超出Murcko规则的自定义支架定义

### 应用

* *基于支架的分割**（用于ML模型验证）：
```python
# Group compounds by scaffold
scaffold_to_mols = {}
for mol, scaffold in zip(mols, scaffolds):
    smi = dm.to_smiles(scaffold)
    if smi not in scaffold_to_mols:
        scaffold_to_mols[smi] = []
    scaffold_to_mols[smi].append(mol)

# Ensure train/test sets have different scaffolds
```

* *SAR分析**：
```python
# Group by scaffold and analyze activity
for scaffold_smi, molecules in scaffold_to_mols.items():
    activities = [get_activity(mol) for mol in molecules]
    print(f"Scaffold: {scaffold_smi}, Mean activity: {np.mean(activities)}")
```

- --

## 片段模块(`datamol.fragment`)

分子碎裂根据化学规则将分子打碎成更小的碎片，可用于基于片段的药物设计和子结构分析。

### BRICS Fragmentation

#### `dm.fragment.brics(mol, ...)`
使用BRICS（打破逆合成有趣的化学子结构）的片段分子。
- **方法**：基于16种化学上有意义的键类型进行剖析
- **考虑**：考虑化学环境和周围的子结构
- **返回**：片段集SMILES strings
- **用例**：逆合成分析，基于片段的设计
- **示例**：
 ```python
 mol = dm.to_mol("c1ccccc1CCN")
 Fragments = dm.fragment.brics(mol)
 # 返回片段如：'[1*]CCN'、'[1*]c1ccccc1'等。
 # [1*]表示附着点
```

### RECAP Fragmentation

#### `dm.fragment.recap(mol, ...)`
使用 RECAP 的片段分子（逆合成组合分析程序）。
- **方法**：基于 11 种预定义键类型进行剖析
- **规则**：
  - 完整保留小于 5 个碳的烷基
  - 保留环状键
- **返回**：片段 SMILES 集strings
- **用例**：组合库设计
- **示例**：
 ```python
 mol = dm.to_mol("CCCCCc1ccccc1")
fragments = dm.fragment.recap(mol)
 ```

### MMPA 片段

#### `dm.fragment.mmpa_frag(mol, ...)`
用于匹配分子对分析的片段。
- **目的**：生成适合识别分子对的片段
- **用例**：分析微小的结构变化如何影响properties
- **示例**:
 ```python
fragments = dm.fragment.mmpa_frag(mol)
 # 用于查找通过单次变换不同的分子对
```

### 方法比较

|方法|债券类型 |保存周期|最适合|
|--------|------------------------|--------------------|----------|
|金砖国家 | 16 | 16是的 |逆合成分析、片段重组|
|回顾 | 11 | 11是的 |组合文库设计|
| MMPA |变量|取决于 |构效关系分析 |

### 片段工作流程

```python
import datamol as dm

# 1. Fragment a molecule
mol = dm.to_mol("CC(=O)Oc1ccccc1C(=O)O")  # Aspirin
brics_frags = dm.fragment.brics(mol)
recap_frags = dm.fragment.recap(mol)

# 2. Analyze fragment frequency across library
all_fragments = []
for mol in molecule_library:
    frags = dm.fragment.brics(mol)
    all_fragments.extend(frags)

# 3. Identify common fragments
from collections import Counter
fragment_counts = Counter(all_fragments)
common_fragments = fragment_counts.most_common(20)

# 4. Convert fragments back to molecules (remove attachment points)
def clean_fragment(frag_smiles):
    # Remove [1*], [2*], etc. attachment point markers
    clean = frag_smiles.replace('[1*]', '[H]')
    return dm.to_mol(clean)
```

### 高级：基于片段的虚拟筛选

```python
# Build fragment library from known actives
active_fragments = set()
for active_mol in active_compounds:
    frags = dm.fragment.brics(active_mol)
    active_fragments.update(frags)

# Screen compounds for presence of active fragments
def score_by_fragments(mol, fragment_set):
    mol_frags = dm.fragment.brics(mol)
    overlap = mol_frags.intersection(fragment_set)
    return len(overlap) / len(mol_frags)

# Score screening library
scores = [score_by_fragments(mol, active_fragments) for mol in screening_lib]
```

### 关键概念

- **附着点**：用 [1*]标记， [2*]等片段SMILES
- **逆合成**：断裂模拟合成断开
- **化学意义**：在典型的合成键处发生断裂
- **重组**：理论上片段可以重新组合成有效分子
