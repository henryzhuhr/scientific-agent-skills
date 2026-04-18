# Medchem API参考

所有medchem模块和功能的综合参考。

## 模块：medchem.rules

### 类：RuleFilters

基于多种药物化学的过滤分子Rules.

* *构造函数：**
```python
RuleFilters(rule_list: List[str])
```

* *参数：**
- `rule_list`：要应用的规则名称列表。请参阅下面的可用规则。

* *方法：**

```python
__call__(mols: List[Chem.Mol], n_jobs: int = 1, progress: bool = False) -> Dict
```
- `mols`：RDKit 分子对象列表
- `n_jobs`：并行作业数（-1 使用所有核心）
- `progress`：显示进度bar
- **返回**：包含每个规则结果的字典

* *示例：**
```python
rfilter = mc.rules.RuleFilters(rule_list=["rule_of_five", "rule_of_cns"])
results = rfilter(mols=mol_list, n_jobs=-1, progress=True)
```

### 模块：medchem.rules.basic_rules

可应用于单个规则的单独规则函数分子.

#### rule_of_ Five()

```python
rule_of_five(mol: Union[str, Chem.Mol]) -> bool
```

Lipinski 口服生物利用度的五法则。

* *标准：**
- 分子量 ≤ 500 Da
- LogP ≤ 5
- H-键供体 ≤ 5
- H-键受体 ≤ 10

* *参数：**
- `mol`：SMILES 字符串或 RDKit 分子对象

  * *返回：** 如果分子通过所有测试，则为 True criteria

#### rule_of_third()

```python
rule_of_three(mol: Union[str, Chem.Mol]) -> bool
```

片段筛选文库的三规则。

* *标准：**
- 分子量 ≤ 300 Da
- LogP ≤ 3
- 氢键供体 ≤ 3
- 氢键受体 ≤ 3
- 可旋转键 ≤ 3
- 极性表面积 ≤ 60 Ų

#### rule_of_oprea()

```python
rule_of_oprea(mol: Union[str, Chem.Mol]) -> bool
```

Oprea 用于命中先导优化的类先导标准。

* *标准：**
- 分子量：200-350 Da
- LogP：-2 至 4
- 可旋转键 ≤ 7
- 环 ≤ 4

#### rule_of_cns()

```python
rule_of_cns(mol: Union[str, Chem.Mol]) -> bool
```

CNS 药物相似规则。

* *标准：**
- 分子量 ≤ 450 Da
- LogP：-1 至 5
- H 键供体 ≤ 2
- TPSA ≤ 90 Ų

#### rule_of_leadlike_soft()

```python
rule_of_leadlike_soft(mol: Union[str, Chem.Mol]) -> bool
```

 软铅类标准（更多

* *标准：**
- 分子量：250-450 Da
- LogP：-3 至 4
- 可旋转键 ≤ 10

#### rule_of_leadlike_strict()

```python
rule_of_leadlike_strict(mol: Union[str, Chem.Mol]) -> bool
```

严格的类铅标准（更具限制性）。

* *标准：**
- 分子量：200-350 Da
- LogP：-2 至 3.5
- 可旋转键 ≤ 7
- 环： 1-3

#### rule_of_veber()

```python
rule_of_veber(mol: Union[str, Chem.Mol]) -> bool
```

Veber 的口服生物利用度规则。

* *标准：**
- 可旋转键 ≤ 10
- TPSA ≤ 140 Ų

#### rule_of_reos()

```python
rule_of_reos(mol: Union[str, Chem.Mol]) -> bool
```

快速消除泔水(REOS)过滤器。

* *标准：**
- 分子量：200-500 Da
- LogP：-5至5
- 氢键供体：0-5
- 氢键受体：0-10

#### rule_of_drug()

```python
rule_of_drug(mol: Union[str, Chem.Mol]) -> bool
```

组合药物相似性criteria.

* *标准：**
- 通过五的规则
- 通过 Veber 规则
- 无 PAINS 子结构

#### Golden_triangle()

```python
golden_triangle(mol: Union[str, Chem.Mol]) -> bool
```

 药物相似性金三角Balance.

* *标准：**
- 200 ≤ MW ≤ 50×LogP + 400
- LogP：-2 至 5

#### pains_filter()

```python
pains_filter(mol: Union[str, Chem.Mol]) -> bool
```

Pan 检测干扰化合物 (PAINS)过滤器。

* *返回：** 如果分子不包含 PAINS 子结构则为真 

- --

## 模块：medchem.structural

### 类：CommonAlertsFilters

用于源自 ChEMBL 和的常见结构警报的过滤器文献.

* *构造函数：**
```python
CommonAlertsFilters()
```

* *方法：**

```python
__call__(mols: List[Chem.Mol], n_jobs: int = 1, progress: bool = False) -> List[Dict]
```

将常见警报过滤器应用于分子列表。

* *返回：**具有以下内容的词典列表键：
- `has_alerts`：指示分子是否有警报的布尔值
- `alert_details`：匹配警报模式的列表
- `num_alerts`：找到的警报数量

```python
check_mol(mol: Chem.Mol) -> Tuple[bool, List[str]]
```

检查单个分子的结构alerts.

* *返回：** (has_alerts, list_of_alert_names)

### 的元组类：NIBRFilters

Novartis NIBR 药物化学过滤器.

* *构造函数：**
```python
NIBRFilters()
```

* *方法：**

```python
__call__(mols: List[Chem.Mol], n_jobs: int = 1, progress: bool = False) -> List[bool]
```

将NIBR过滤器应用于分子。

* *返回：**布尔值列表（如果分子为True通过）

### 类：LillyDemeritsFilters

Eli Lilly 的基于过失的结构警报系统（275 条规则）。

* *构造函数：**
```python
LillyDemeritsFilters()
```

* *方法：**

```python
__call__(mols: List[Chem.Mol], n_jobs: int = 1, progress: bool = False) -> List[Dict]
```

计算分子的Lilly缺点。

* *返回：**包含键的字典列表：
- `demerits`：总计过失分数
- `passes`：布尔值（如果过失≤100则为真）
- `matched_patterns`：带分数的匹配模式列表

- --

## 模块：medchem.function

通用的高级功能API操作。

### nibr_filter()

```python
nibr_filter(mols: List[Chem.Mol], n_jobs: int = 1) -> List[bool]
```

使用功能API应用NIBR过滤器。

* *参数：**
- `mols`：分子列表
- `n_jobs`：并行化级别

* *返回：** 通过/失败布尔值列表

### common_alerts_filter()

```python
common_alerts_filter(mols: List[Chem.Mol], n_jobs: int = 1) -> List[Dict]
```

使用功能API应用常见警报过滤器。

* *返回：** 结果列表dictionaries

### lilly_demerits_filter()

```python
lilly_demerits_filter(mols: List[Chem.Mol], n_jobs: int = 1) -> List[Dict]
```

使用功能 API 计算 Lilly 过失。

- --

## 模块：medchem.groups

### 类： ChemicalGroup

检测分子中的特定化学基团。

* *构造函数：**
```python
ChemicalGroup(groups: List[str], custom_smarts: Optional[Dict[str, str]] = None)
```

* *参数：**
- `groups`：预定义基团名称列表
- `custom_smarts`：字典映射自定义基团名称至 SMARTS 模式

* *预定义组：**
- `"hinge_binders"`：激酶铰链结合基序
- `"phosphate_binders"`：磷酸盐结合基团
- `"michael_acceptors"`：迈克尔受体亲电子体
- `"reactive_groups"`：一般反应性功能

* *方法：**

```python
has_match(mols: List[Chem.Mol]) -> List[bool]
```

检查分子是否包含任何指定基团。

```python
get_matches(mol: Chem.Mol) -> Dict[str, List[Tuple]]
```

获取单个的详细匹配信息分子.

* *返回：**将组名称映射到原子索引列表的字典

```python
get_all_matches(mols: List[Chem.Mol]) -> List[Dict]
```

获取所有分子的匹配信息。

* *示例：**
```python
group = mc.groups.ChemicalGroup(groups=["hinge_binders", "phosphate_binders"])
matches = group.get_all_matches(mol_list)
```

- --

## 模块： medchem.catalogs

### 类：NamedCatalogs

访问精选化学品目录。

* *可用目录：**
- `"functional_groups"`：常用官能团
- `"protecting_groups"`：保护基结构
- `"reagents"`：常用试剂
- `"fragments"`：标准片段

* *用法：**
```python
catalog = mc.catalogs.NamedCatalogs.get("functional_groups")
matches = catalog.get_matches(mol)
```

- --

## 模块：medchem.complexity

计算分子复杂性度量。

### calculate_complexity()

```python
calculate_complexity(mol: Chem.Mol, method: str = "bertz") -> float
```

计算分子的复杂度分数。

* *参数：**
- `mol`：RDKit分子
- `method`：复杂度度量("bertz", "whitlock", "barone")

* *返回：** 复杂度分数（越高=越复杂）

### 类：ComplexityFilter

按复杂度过滤分子Threshold.

* *构造函数：**
```python
ComplexityFilter(max_complexity: float, method: str = "bertz")
```

* *方法：**

```python
__call__(mols: List[Chem.Mol], n_jobs: int = 1) -> List[bool]
```

过滤超过复杂度阈值的分子。

- --

## 模块： medchem.constraints

### 类：Constraints

应用自定义的基于属性的约束。

* *构造函数：**
```python
Constraints(
    mw_range: Optional[Tuple[float, float]] = None,
    logp_range: Optional[Tuple[float, float]] = None,
    tpsa_max: Optional[float] = None,
    tpsa_range: Optional[Tuple[float, float]] = None,
    hbd_max: Optional[int] = None,
    hba_max: Optional[int] = None,
    rotatable_bonds_max: Optional[int] = None,
    rings_range: Optional[Tuple[int, int]] = None,
    aromatic_rings_max: Optional[int] = None,
)
```

* *参数：**所有参数都是可选的。仅指定所需的约束。

* *方法：**

```python
__call__(mols: List[Chem.Mol], n_jobs: int = 1) -> List[Dict]
```

将约束应用于分子。

* *返回：**带有键的字典列表：
- `passes`：指示是否所有约束都通过的布尔值
- `violations`：失败的约束名称列表

* *示例：**
```python
constraints = mc.constraints.Constraints(
    mw_range=(200, 500),
    logp_range=(-2, 5),
    tpsa_max=140
)
results = constraints(mols=mol_list, n_jobs=-1)
```

- --

## 模块：medchem.query

复杂过滤的查询语言。

### parse()

```python
parse(query: str) -> Query
```

 将 medchem 查询字符串解析为 Query 对象。

* *查询语法：**
- 运算符：`AND`、`OR`、 `NOT`
- 比较：`<`、`>`、`<=`、`>=`、`==`、`!=`
- 属性：`complexity`、 `lilly_demerits`、`mw`、`logp`、`tpsa`
- 规则：`rule_of_five`、`rule_of_cns`等
- 过滤器：`common_alerts`、`nibr_filter`、 `pains_filter`

* *查询示例：**
```python
"rule_of_five AND NOT common_alerts"
"rule_of_cns AND complexity < 400"
"mw > 200 AND mw < 500 AND logp < 5"
"(rule_of_five OR rule_of_oprea) AND NOT pains_filter"
```

### 类：查询

* *方法：**

```python
apply(mols: List[Chem.Mol], n_jobs: int = 1) -> List[bool]
```

将解析的查询应用于分子。

* *示例：**
```python
query = mc.query.parse("rule_of_five AND NOT common_alerts")
results = query.apply(mols=mol_list, n_jobs=-1)
passing_mols = [mol for mol, passes in zip(mol_list, results) if passes]
```

- --

## 模块：medchem.utils

用于处理分子的实用函数。

### batch_process()

```python
batch_process(
    mols: List[Chem.Mol],
    func: Callable,
    n_jobs: int = 1,
    progress: bool = False,
    batch_size: Optional[int] = None
) -> List
```

并行批量处理分子。

* *参数：**
- `mols`：分子列表
- `func`：应用于每个分子的函数
- `n_jobs`：并行工作人员数量
- `progress`：显示进度条
- `batch_size`：处理批次的大小

### standardize_mol()

```python
standardize_mol(mol: Chem.Mol) -> Chem.Mol
```

标准化分子表示（消毒、中和电荷等）。

- --

## 常见模式

### 模式：并行处理

所有过滤器都支持并行化：

```python
# Use all CPU cores
results = filter_object(mols=mol_list, n_jobs=-1, progress=True)

# Use specific number of cores
results = filter_object(mols=mol_list, n_jobs=4, progress=True)
```

### 模式：组合多个过滤器

```python
import medchem as mc

# Apply multiple filters
rule_filter = mc.rules.RuleFilters(rule_list=["rule_of_five"])
alert_filter = mc.structural.CommonAlertsFilters()
lilly_filter = mc.structural.LillyDemeritsFilters()

# Get results
rule_results = rule_filter(mols=mol_list, n_jobs=-1)
alert_results = alert_filter(mols=mol_list, n_jobs=-1)
lilly_results = lilly_filter(mols=mol_list, n_jobs=-1)

# Combine criteria
passing_mols = [
    mol for i, mol in enumerate(mol_list)
    if rule_results[i]["passes"]
    and not alert_results[i]["has_alerts"]
    and lilly_results[i]["passes"]
]
```

### 模式：使用数据帧

```python
import pandas as pd
import datamol as dm
import medchem as mc

# Load data
df = pd.read_csv("molecules.csv")
df["mol"] = df["smiles"].apply(dm.to_mol)

# Apply filters
rfilter = mc.rules.RuleFilters(rule_list=["rule_of_five", "rule_of_cns"])
results = rfilter(mols=df["mol"].tolist(), n_jobs=-1)

# Add results to dataframe
df["passes_ro5"] = [r["rule_of_five"] for r in results]
df["passes_cns"] = [r["rule_of_cns"] for r in results]

# Filter dataframe
filtered_df = df[df["passes_ro5"] & df["passes_cns"]]
```
