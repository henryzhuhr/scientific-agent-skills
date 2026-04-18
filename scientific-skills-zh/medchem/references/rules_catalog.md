# Medchem 规则和过滤器目录

medchem.

## 目录中所有可用药物化学规则、结构警报和过滤器的综合目录

1. [药物相似规则](#drug-likeness-rules)
2. [先导相似规则](#lead-likeness-rules)
3. [片段规则](#fragment-rules)
4. [CNS规则](#cns-rules)
5. [结构警报过滤器](#structural-alert-filters)
6. [化学基团模式](#chemical-group-patterns)

- --

## 药物相似规则

### 五法则 (Lipinski)

* *参考：** Lipinski 等人，Adv Drug Deliv Rev (1997) 23:3-25

* *目的：**预测口服生物利用度

* *标准：**
- 分子量 ≤ 500 Da
- LogP ≤ 5
- 氢键供体 ≤ 5
- 氢键受体 ≤ 10

* *用法：**
```python
mc.rules.basic_rules.rule_of_five(mol)
```

* *注释：**
- 药物发现中最广泛使用的过滤器之一
- 大约 90% 的口服活性药物符合这些规则
- 存在例外，特别是对于天然产物和抗生素

- --

### Veber规则

* *参考：** Veber et al., J Med Chem (2002) 45:2615-2623

* *目的：** 口服的附加标准生物利用度

* *标准：**
- 可旋转键 ≤ 10
- 拓扑极性表面积 (TPSA) ≤ 140 

* *用法：**
```python
mc.rules.basic_rules.rule_of_veber(mol)
```

* *注释：**
- 补充五的规则
- TPSA 与细胞通透性相关
- 可旋转键影响分子灵活性

- --

### 药物规则

* *目的：**组合药物相似性评估

* *标准：**
- 通过五规则
- 通过Veber规则
- 不包含PAINS子结构

* *用法：**
```python
mc.rules.basic_rules.rule_of_drug(mol)
```

- --

### REOS（快速消除泔水）

* *参考：** Walters & Murcko, Adv Drug Deliv Rev (2002) 54:255-271

* *目的：**过滤掉不太可能是药物的化合物

* *标准：**
- 分子量：200-500 Da
- LogP：-5 至 5
- 氢键供体：0-5
- 氢键受体： 0-10

* *用法：**
```python
mc.rules.basic_rules.rule_of_reos(mol)
```

- --

### 金三角

* *参考：** Johnson et al., J Med Chem (2009) 52:5487-5500

* *用途：**平衡亲脂性和分子量

* *标准：**
- 200 ≤ MW ≤ 50 × LogP + 400
- LogP: -2 至5

* *用法：**
```python
mc.rules.basic_rules.golden_triangle(mol)
```

* *注释：**
- 定义最佳理化空间
- 视觉表示类似于 MW 与 LogP 图上的三角形

- --

## 引线相似性规则

### Oprea 规则

* *参考：** Oprea 等人，J Chem Inf Comput Sci (2001) 41:1308-1315

* *目的：** 识别用于优化的先导化合物

* *标准：**
- 分子量： 200-350 Da
- LogP：-2 至 4
- 可旋转键 ≤ 7
- 环数 ≤ 4

* *用法：**
```python
mc.rules.basic_rules.rule_of_oprea(mol)
```

* *原理：** 铅化合物应具有“空间”优化过程中生长”

- --

### 类铅规则（软）

* *目的：** 允许类铅标准

* *标准：**
- 分子量：250-450 Da
- LogP：-3 至4
- 可旋转键 ≤ 10

* *用途：**
```python
mc.rules.basic_rules.rule_of_leadlike_soft(mol)
```

- --

### 类引线规则（严格）

* *用途：** 限制性类引线标准

* *标准：**
- 分子量：200-350 Da
- LogP：-2 至 3.5
- 可旋转键 ≤ 7
- 环数： 1-3

* *用法：**
```python
mc.rules.basic_rules.rule_of_leadlike_strict(mol)
```

- --

## 片段规则

### 三规则

* *参考：** Congreve 等人，Drug Discov Today (2003) 8:876-877

* *目的：**筛选用于基于片段的药物发现的片段库

* *标准：**
- 分子量 ≤ 300 Da
- LogP ≤ 3
- 氢键供体 ≤ 3
- 氢键受主 ≤ 3
- 可旋转键 ≤ 3
- 极性表面积 ≤ 60 Ų

* *用途：**
```python
mc.rules.basic_rules.rule_of_three(mol)
```

* *注释：**
- 片段在生长过程中长成引线优化
- 更低的复杂度允许更多的起点

- --

## CNS规则

### CNS

的规则**用途：**中枢神经系统药物相似性

* *标准：**
- 分子量 ≤ 450 Da
- LogP：-1 至 5
- 氢键供体 ≤ 2
- TPSA ≤ 90 

* *用法：**
```python
mc.rules.basic_rules.rule_of_cns(mol)
```

* *基本原理：**
- 血脑屏障穿透需要特定属性
- 较低的 TPSA 和 HBD 计数可提高 BBB 通透性
- 严格约束反映 CNS挑战

- --

## 结构警报过滤器

### PAINS（泛测定干扰化合物）

* *参考：** Baell & Holloway, J Med Chem (2010) 53:2719-2740

* *目的：** 识别干扰化合物分析

* *类别：**
- 儿茶酚
- 醌类
- 绕丹宁
- 羟基苯腙
- 烷基/芳基醛
- 迈克尔受体（特定模式）

* *用法：**
```python
mc.rules.basic_rules.pains_filter(mol)
# Returns True if NO PAINS found
```

* *注释：**
- PAINS 化合物通过非特异性机制在多种测定中显示活性
- 筛选活动中常见的假阳性
- 应在先导中优先考虑选择

- --

### 常见警报过滤器

* *来源：**源自ChEMBL管理和药物化学文献

* *目的：**标记常见有问题的结构模式

* *警报类别：**
1. **反应基团**
  - 环氧化物
  - 氮丙啶
  - 酰基卤
  - 异氰酸酯

2. **代谢负担**
  - 肼
  - 硫脲
  - 苯胺（某些模式）

3. **聚合器**
  - 聚芳烃系统
  - 长脂肪链

4. **毒基团**
  - 硝基芳香族化合物
  - 芳香族氮氧化物
  - 某些杂环化合物

* *用法：**
```python
alert_filter = mc.structural.CommonAlertsFilters()
has_alerts, details = alert_filter.check_mol(mol)
```

* *返回格式：**
```python
{
    "has_alerts": True,
    "alert_details": ["reactive_epoxide", "metabolic_hydrazine"],
    "num_alerts": 2
}
```

- --

### NIBR Filters

* *来源：**诺华生物医学研究院

* *用途：**工业药物化学过滤规则

* *功能：**
- 根据诺华经验开发的专有过滤器组
- 平衡药物相似性与实用药物化学
- 包括结构警报和属性过滤器

* *用法：**
```python
nibr_filter = mc.structural.NIBRFilters()
results = nibr_filter(mols=mol_list, n_jobs=-1)
```

* *返回格式：**布尔列表（True =通过）

- --

### Lilly 过失过滤器

* *参考：** 基于 Eli Lilly 药物化学规则

* *来源：** 18 年来积累的 275 个结构模式

* *目的：** 识别测定干扰和问题功能

* *机制：**
- 每个匹配的模式都会增加缺点
- 超过100个缺点的分子会被拒绝
- 一些模式会增加10-50个缺点，其他则会增加100+（立即拒绝）

* *缺点类别：**

1. **高缺点（> 50）：**
  - 已知有毒基团
  - 高反应性官能团
  - 强金属螯合剂

2. **中度过失（20-50）：**
  - 代谢负担
  - 易于聚集的结构
  - 频繁击球手

3. **低过分（5-20）：**
  - 次要问题
  - 上下文相关问题

  * *用法：**
```python
lilly_filter = mc.structural.LillyDemeritsFilters()
results = lilly_filter(mols=mol_list, n_jobs=-1)
```

* *返回格式：**
```python
{
    "demerits": 35,
    "passes": True,  # (demerits ≤ 100)
    "matched_patterns": [
        {"pattern": "phenolic_ester", "demerits": 20},
        {"pattern": "aniline_derivative", "demerits": 15}
    ]
}
```

- --

## 化学基团模式

### 铰链结合物

* *目的：** 识别激酶铰链结合基序

* *常见模式：**
- 氨基吡啶类
- 氨基嘧啶类
- 吲唑类
- 苯并咪唑类

* *用途：**
```python
group = mc.groups.ChemicalGroup(groups=["hinge_binders"])
has_hinge = group.has_match(mol_list)
```

* *应用：** 激酶抑制剂设计

- --

### 磷酸盐结合剂

* *用途：**识别磷酸盐结合基团

* *常见模式：**
- 特定几何形状的碱性胺
- 胍基团
- 精氨酸mimetics

* *用途：**
```python
group = mc.groups.ChemicalGroup(groups=["phosphate_binders"])
```

* *应用：**激酶抑制剂、磷酸酶抑制剂

- --

### 迈克尔受体

* *用途：**识别亲电迈克尔受体基团

* *常见模式：**
- α,β-不饱和羰基
- α,β-不饱和腈
- 乙烯基砜
- 丙烯酰胺

* *用法：**
```python
group = mc.groups.ChemicalGroup(groups=["michael_acceptors"])
```

* *注释：**
- 可能是共价抑制剂所需要的
- 在筛选中通常标记为反应性警报

- --

### 反应性基团

* *目的：** 识别一般反应性功能

* *常见模式：**
- 环氧化物
- 氮丙啶
- 酰基卤
- 异氰酸酯
- 磺酰基氯化物

* *用法：**
```python
group = mc.groups.ChemicalGroup(groups=["reactive_groups"])
```

- --

## 自定义 SMARTS 模式

使用定义自定义结构模式SMARTS：

```python
custom_patterns = {
    "my_warhead": "[C;H0](=O)C(F)(F)F",  # Trifluoromethyl ketone
    "my_scaffold": "c1ccc2c(c1)ncc(n2)N",  # Aminobenzimidazole
}

group = mc.groups.ChemicalGroup(
    groups=["hinge_binders"],
    custom_smarts=custom_patterns
)
```

- --

## 过滤器选择指南

### 初始筛选（高通量）

推荐过滤器：
- 五法则
- PAINS过滤器
- 通用警报（允许设置）

```python
rfilter = mc.rules.RuleFilters(rule_list=["rule_of_five", "pains_filter"])
alert_filter = mc.structural.CommonAlertsFilters()
```

- --

### Hit-to-Lead

推荐过滤器：
- Oprea或Leadlike规则（软）
- NIBR过滤器
- Lilly缺点

```python
rfilter = mc.rules.RuleFilters(rule_list=["rule_of_oprea"])
nibr_filter = mc.structural.NIBRFilters()
lilly_filter = mc.structural.LillyDemeritsFilters()
```

- --

### 先导化合物优化

推荐过滤器：
- 药物规则
- 先导化合物（严格）
- 完整结构警报分析
- 复杂性过滤器

```python
rfilter = mc.rules.RuleFilters(rule_list=["rule_of_drug", "rule_of_leadlike_strict"])
alert_filter = mc.structural.CommonAlertsFilters()
complexity_filter = mc.complexity.ComplexityFilter(max_complexity=400)
```

- --

### CNS 目标

推荐过滤器：
- CNS 规则
- 减少 PAINS 标准（以 CNS 为重点）
- BBB 渗透性约束

```python
rfilter = mc.rules.RuleFilters(rule_list=["rule_of_cns"])
constraints = mc.constraints.Constraints(
    tpsa_max=90,
    hbd_max=2,
    mw_range=(300, 450)
)
```

- --

### 基于片段的药物发现

推荐过滤器：
- 三法则
- 最小复杂度
- 基本反应基团check

```python
rfilter = mc.rules.RuleFilters(rule_list=["rule_of_three"])
complexity_filter = mc.complexity.ComplexityFilter(max_complexity=250)
```

- --

## 重要注意事项

### 误报和漏报

* *过滤器是指导原则，而不是绝对值：**

1. **误报**（标记为好药）：
  - 约 10% 的上市药物不符合五规则
  - 天然产品经常违反标准规则
  - 前药故意违反规则
  - 抗生素和抗病毒药物经常不合规

2. **假阴性**（不良化合物通过）：
  - 通过过滤器并不能保证成功
  - 未捕获特定目标的问题
  - 未完全预测体内属性

### 上下文特定应用

 * *不同的上下文需要不同的标准：**

- **目标类别：**激酶 vs GPCR vs 离子通道具有不同的最佳空间
- **形态：** 小分子 vs PROTAC vs 分子胶
- **给药途径：** 口服 vs IV vs 局部 
- **疾病领域：** CNS vs 肿瘤学 vs 传染病
- **阶段：** 筛选 vs命中领先与领先优化

#### 机器学习的补充

现代方法将规则与ML相结合：

```python
# Rule-based pre-filtering
rule_results = mc.rules.RuleFilters(rule_list=["rule_of_five"])(mols)
filtered_mols = [mol for mol, r in zip(mols, rule_results) if r["passes"]]

# ML model scoring on filtered set
ml_scores = ml_model.predict(filtered_mols)

# Combined decision
final_candidates = [
    mol for mol, score in zip(filtered_mols, ml_scores)
    if score > threshold
]
```

- --

## 参考文献

1. 利平斯基 CA 等人。高级药物传递修订版 (1997) 23:3-25
2. Veber DF 等人。医学化学杂志 (2002) 45:2615-2623
3. Oprea TI 等人。 J Chem Inf Comput Sci (2001) 41:1308-1315
4. 康格里夫 M 等人。今日药物发现 (2003) 8:876-877
5. 贝尔 JB 和霍洛威 GA。医学化学杂志（2010）53：2719-2740
6. 约翰逊 TW 等人。医学化学杂志（2009）52：5487-5500
7. 沃尔特斯·WP 和穆尔科·马萨诸塞州。高级药物交付修订版 (2002) 54:255-271
8. Hann MM 和 Oprea TI。当前化学生物学观点 (2004) 8:255-263
9. 里什顿总经理。今日药物发现 (1997) 2:382-384
