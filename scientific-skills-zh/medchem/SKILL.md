---
name: medchem
description: 药物化学过滤器。应用药物相似性规则（Lipinski、Veber）、PAINS 过滤器、结构警报、复杂性指标，以进行化合物优先级排序和库过滤。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# Medchem

## 概述

Medchem 是一个用于药物发现工作流程中分子过滤和优先级排序的 Python 库。应用数百个完善的新型分子过滤器、结构警报和药物化学规则，大规模有效地对化合物库进行分类和优先排序。规则和过滤器是特定于上下文的 - 结合领域专业知识用作指南。

## 何时使用此技能

此技能应在以下情况下使用：
- 将药物相似性规则（Lipinski、Veber 等）应用于化合物库
- 通过结构警报或 PAINS 模式过滤分子
- 优先考虑先导化合物优化
- 评估化合物质量和药物化学性质
- 检测反应性或有问题的官能团
- 计算分子复杂性指标

## 安装

```bash
uv pip install medchem
```

## 核心功能

### 1. 药物化学规则

使用`medchem.rules`模块将已建立的药物相似规则应用于分子。

* *可用规则：**
- 五规则(Lipinski)
- Oprea规则
- CNS规则
- 铅状规则(软和严格）
- 三规则
- Reos规则
- 药物规则
- Veber规则
- 金三角
- PAINS过滤器

* *单规则应用：**

```python
import medchem as mc

# Apply Rule of Five to a SMILES string
smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
passes = mc.rules.basic_rules.rule_of_five(smiles)
# Returns: True

# Check specific rules
passes_oprea = mc.rules.basic_rules.rule_of_oprea(smiles)
passes_cns = mc.rules.basic_rules.rule_of_cns(smiles)
```

* *带有规则过滤器的多个规则：**

```python
import datamol as dm
import medchem as mc

# Load molecules
mols = [dm.to_mol(smiles) for smiles in smiles_list]

# Create filter with multiple rules
rfilter = mc.rules.RuleFilters(
    rule_list=[
        "rule_of_five",
        "rule_of_oprea",
        "rule_of_cns",
        "rule_of_leadlike_soft"
    ]
)

# Apply filters with parallelization
results = rfilter(
    mols=mols,
    n_jobs=-1,  # Use all CPU cores
    progress=True
)
```

* *结果格式：**
结果以字典形式返回，其中包含每个规则的通过/失败状态和详细信息。

### 2.结构警报过滤器

使用 `medchem.structural` 模块检测潜在有问题的结构模式。

* *可用过滤器：**

1. **常见警报** - 来自 ChEMBL 管理和文献 
2 的一般结构警报。 **NIBR 过滤器** - 诺华生物医学研究所过滤器套件
3. **Lilly 过失** - Eli Lilly 基于过失的系统（275 条规则，超过 100 个过失的分子被拒绝）

* *常见警报：**

```python
import medchem as mc

# Create filter
alert_filter = mc.structural.CommonAlertsFilters()

# Check single molecule
mol = dm.to_mol("c1ccccc1")
has_alerts, details = alert_filter.check_mol(mol)

# Batch filtering with parallelization
results = alert_filter(
    mols=mol_list,
    n_jobs=-1,
    progress=True
)
```

* *NIBR 过滤器：**

```python
import medchem as mc

# Apply NIBR filters
nibr_filter = mc.structural.NIBRFilters()
results = nibr_filter(mols=mol_list, n_jobs=-1)
```

* *Lilly缺点：**

```python
import medchem as mc

# Calculate Lilly demerits
lilly = mc.structural.LillyDemeritsFilters()
results = lilly(mols=mol_list, n_jobs=-1)

# Each result includes demerit score and whether it passes (≤100 demerits)
```

### 3. 用于高级操作的功能 API

`medchem.functional` 模块为常用工作流程提供便捷的功能。

* *快速过滤：**

```python
import medchem as mc

# Apply NIBR filters to a list
filter_ok = mc.functional.nibr_filter(
    mols=mol_list,
    n_jobs=-1
)

# Apply common alerts
alert_results = mc.functional.common_alerts_filter(
    mols=mol_list,
    n_jobs=-1
)
```

### 4. 化学基团检测

使用`medchem.groups`识别特定化学基团和官能团。

* *可用基团：**
- 铰链结合物
- 磷酸盐结合物
- 迈克尔受体
- 反应基团
- 自定义SMARTS 模式

* *用法：**

```python
import medchem as mc

# Create group detector
group = mc.groups.ChemicalGroup(groups=["hinge_binders"])

# Check for matches
has_matches = group.has_match(mol_list)

# Get detailed match information
matches = group.get_matches(mol)
```

### 5. 命名目录

通过 `medchem.catalogs`.

 访问精选的化学结构集合**可用目录：**
- 功能基团
- 保护基团
- 常用试剂
- 标准片段

* *用法：**

```python
import medchem as mc

# Access named catalogs
catalogs = mc.catalogs.NamedCatalogs

# Use catalog for matching
catalog = catalogs.get("functional_groups")
matches = catalog.get_matches(mol)
```

### 6. 分子复杂性

使用以下方法计算近似合成可及性的复杂性指标`medchem.complexity`.

* *常用指标：**
- Bertz 复杂度
- Whitlock 复杂度
- Barone 复杂度

* *用法：**

```python
import medchem as mc

# Calculate complexity
complexity_score = mc.complexity.calculate_complexity(mol)

# Filter by complexity threshold
complex_filter = mc.complexity.ComplexityFilter(max_complexity=500)
results = complex_filter(mols=mol_list)
```

### 7. 约束过滤

使用`medchem.constraints`.

* *示例约束：**
- 分子量范围
- LogP 边界
- TPSA 限制
- 可旋转键应用基于自定义属性的约束counts

* *用法：**

```python
import medchem as mc

# Define constraints
constraints = mc.constraints.Constraints(
    mw_range=(200, 500),
    logp_range=(-2, 5),
    tpsa_max=140,
    rotatable_bonds_max=10
)

# Apply constraints
results = constraints(mols=mol_list, n_jobs=-1)
```

### 8. Medchem 查询语言

使用专门的查询语言进行复杂的过滤条件。

* *查询示例：**
```
# Molecules passing Ro5 AND not having common alerts
"rule_of_five AND NOT common_alerts"

# CNS-like molecules with low complexity
"rule_of_cns AND complexity < 400"

# Leadlike molecules without Lilly demerits
"rule_of_leadlike AND lilly_demerits == 0"
```

* *用法：**

```python
import medchem as mc

# Parse and apply query
query = mc.query.parse("rule_of_five AND NOT common_alerts")
results = query.apply(mols=mol_list, n_jobs=-1)
```

## 工作流程模式

### 模式 1：化合物库的初始分类

过滤大型化合物集合以识别药物样物质候选人.

```python
import datamol as dm
import medchem as mc
import pandas as pd

# Load compound library
df = pd.read_csv("compounds.csv")
mols = [dm.to_mol(smi) for smi in df["smiles"]]

# Apply primary filters
rule_filter = mc.rules.RuleFilters(rule_list=["rule_of_five", "rule_of_veber"])
rule_results = rule_filter(mols=mols, n_jobs=-1, progress=True)

# Apply structural alerts
alert_filter = mc.structural.CommonAlertsFilters()
alert_results = alert_filter(mols=mols, n_jobs=-1, progress=True)

# Combine results
df["passes_rules"] = rule_results["pass"]
df["has_alerts"] = alert_results["has_alerts"]
df["drug_like"] = df["passes_rules"] & ~df["has_alerts"]

# Save filtered compounds
filtered_df = df[df["drug_like"]]
filtered_df.to_csv("filtered_compounds.csv", index=False)
```

### 模式 2：先导化合物优化过滤

在先导化合物优化过程中应用更严格的标准。

```python
import medchem as mc

# Create comprehensive filter
filters = {
    "rules": mc.rules.RuleFilters(rule_list=["rule_of_leadlike_strict"]),
    "alerts": mc.structural.NIBRFilters(),
    "lilly": mc.structural.LillyDemeritsFilters(),
    "complexity": mc.complexity.ComplexityFilter(max_complexity=400)
}

# Apply all filters
results = {}
for name, filt in filters.items():
    results[name] = filt(mols=candidate_mols, n_jobs=-1)

# Identify compounds passing all filters
passes_all = all(r["pass"] for r in results.values())
```

### 模式 3：识别特定化学基团

查找包含特定官能团或

```python
import medchem as mc

# Create group detector for multiple groups
group_detector = mc.groups.ChemicalGroup(
    groups=["hinge_binders", "phosphate_binders"]
)

# Screen library
matches = group_detector.get_all_matches(mol_list)

# Filter molecules with desired groups
mol_with_groups = [mol for mol, match in zip(mol_list, matches) if match]
```

## 最佳实践

1. **上下文很重要**：不要盲目应用过滤器。了解生物靶标和化学空间。

2. **组合多个过滤器**：结合使用规则、结构警报和领域知识来做出更好的决策。

3. **使用并行化**：对于大型数据集（>1000 个分子），始终使用 `n_jobs=-1` 进行并行处理。

4. **迭代细化**：从广泛的过滤器（Ro5）开始，然后根据需要应用更具体的标准（CNS，铅状）。

5. **文档过滤决策**：跟踪哪些分子被过滤掉以及为什么可重复性。

6. **验证结果**：请记住，上市药物通常无法通过标准过滤器 - 将这些作为指导方针，而不是绝对规则。

7. **考虑前药**：设计为前药的分子可能故意违反标准药物化学规则。

## 资源

### 参考文献/api_guide.md
全面的 API 参考，涵盖所有 medchem 模块，包含详细的函数签名、参数和返回类型。

### references/rules_catalog.md
可用规则、过滤器和警报的完整目录，以及描述、阈值和文献参考。

### scripts/filter_molecules.py
用于批量过滤工作流程的生产就绪脚本。支持多种输入格式（CSV、SDF、SMILES）、可配置的过滤器组合和详细报告。

* *用法：**
```bash
python scripts/filter_molecules.py input.csv --rules rule_of_five,rule_of_cns --alerts nibr --output filtered.csv
```

## 文档

官方文档：https://medchem-docs.datamol.io/
GitHub存储库： https://github.com/datamol-io/medchem
