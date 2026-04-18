# RDKit 分子描述符参考

RDKit 的 `Descriptors` 模块中可用的分子描述符的完整参考。

## 用法

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

mol = Chem.MolFromSmiles('CCO')

# Calculate individual descriptor
mw = Descriptors.MolWt(mol)

# Calculate all descriptors at once
all_desc = Descriptors.CalcMolDescriptors(mol)
```

## 分子量和质量

### MolWt
分子的平均分子量。
```python
Descriptors.MolWt(mol)
```

### ExactMolWt
E 使用同位素组成的精确分子量。
```python
Descriptors.ExactMolWt(mol)
```

### HeavyAtomMolWt
忽略氢的平均分子量。
```python
Descriptors.HeavyAtomMolWt(mol)
```

## 亲脂性

### MolLogP
Wildman-Crippen LogP（辛醇-水分配）系数).
```python
Descriptors.MolLogP(mol)
```

### MolMR
Wildman-Crippen 摩尔折射率.
```python
Descriptors.MolMR(mol)
```

## 极表面积

### TPSA
拓扑极表面积（TPSA）基于片段贡献。
```python
Descriptors.TPSA(mol)
```

### LabuteASA
Labute 的近似表面积（ASA）。
```python
Descriptors.LabuteASA(mol)
```

## 氢键

### NumHDonors
氢键供体数量（N-H 和 O-H）。
```python
Descriptors.NumHDonors(mol)
```

### NumHAcceptors
氢键受体数量（N 和 O）。
```python
Descriptors.NumHAcceptors(mol)
```

### NOCount
N 和 O 原子数量。
```python
Descriptors.NOCount(mol)
```

### NHOHCount
N-H 和 O-H 键数量。
```python
Descriptors.NHOHCount(mol)
```

## 原子计数

### HeavyAtomCount
重原子数（非氢）。
```python
Descriptors.HeavyAtomCount(mol)
```

### NumHeteroatoms
杂原子数（非 C 和非 H）。
```python
Descriptors.NumHeteroatoms(mol)
```

### NumValenceElectrons
价电子总数。
```python
Descriptors.NumValenceElectrons(mol)
```

### NumRadicalElectrons
自由基电子数量。
```python
Descriptors.NumRadicalElectrons(mol)
```

## 环描述符

### RingCount
环数
```python
Descriptors.RingCount(mol)
```

### NumAromaticRings
芳香环数
```python
Descriptors.NumAromaticRings(mol)
```

### NumSaturatedRings
饱和数环.
```python
Descriptors.NumSaturatedRings(mol)
```

### NumAliphaticRings
脂肪族（非芳香族）环的数量。
```python
Descriptors.NumAliphaticRings(mol)
```

### NumAromaticCarbocycles
芳香族碳环的数量（带有
```python
Descriptors.NumAromaticCarbocycles(mol)
```

### NumAromaticHeterocycles
芳香杂环（含杂原子的环）的数量。
```python
Descriptors.NumAromaticHeterocycles(mol)
```

### NumSaturatedCarbocycles
的数量饱和碳环数。
```python
Descriptors.NumSaturatedCarbocycles(mol)
```

### NumSaturatedHeterocycles
饱和杂环数。
```python
Descriptors.NumSaturatedHeterocycles(mol)
```

### NumAliphatic Carbocycles
脂肪族数碳环数.
```python
Descriptors.NumAliphaticCarbocycles(mol)
```

### NumAliphaticHeterocycles
脂肪族杂环数.
```python
Descriptors.NumAliphaticHeterocycles(mol)
```

## 可旋转键

### NumRotatableBonds
可旋转键的数量（柔性）。
```python
Descriptors.NumRotatableBonds(mol)
```

## Aromatic Atoms

### NumAromaticAtoms
芳香族数量原子.
```python
Descriptors.NumAromaticAtoms(mol)
```

## 分数描述符

### FractionCsp3
sp3 杂化的碳分数。
```python
Descriptors.FractionCsp3(mol)
```

## 复杂性描述符

### BertzCT
Bertz复杂性指数。
```python
Descriptors.BertzCT(mol)
```

### Ipc
信息内容（复杂性度量）。
```python
Descriptors.Ipc(mol)
```

## Kappa Shape Indices

分子基于图不变量的形状描述符。

### Kappa1
第一个 kappa 形状索引。
```python
Descriptors.Kappa1(mol)
```

### Kappa2
第二个 kappa 形状index.
```python
Descriptors.Kappa2(mol)
```

### Kappa3
第三个 kappa 形状索引.
```python
Descriptors.Kappa3(mol)
```

## Chi 连通性指数

分子连通性指数。

### Chi0, Chi1, Chi2, Chi3, Chi4
简单 chi 连接指数。
```python
Descriptors.Chi0(mol)
Descriptors.Chi1(mol)
Descriptors.Chi2(mol)
Descriptors.Chi3(mol)
Descriptors.Chi4(mol)
```

### Chi0n, Chi1n, Chi2n, Chi3n, Chi4n
价修改 chi 连接指数.
```python
Descriptors.Chi0n(mol)
Descriptors.Chi1n(mol)
Descriptors.Chi2n(mol)
Descriptors.Chi3n(mol)
Descriptors.Chi4n(mol)
```

### Chi0v、Chi1v、Chi2v、Chi3v、Chi4v
价 chi 连接指数.
```python
Descriptors.Chi0v(mol)
Descriptors.Chi1v(mol)
Descriptors.Chi2v(mol)
Descriptors.Chi3v(mol)
Descriptors.Chi4v(mol)
```

## Hall-Kier Alpha

### HallKierAlpha
Hall-Kier alpha 值（分子灵活性）。
```python
Descriptors.HallKierAlpha(mol)
```

## Balaban 的 J 指数

### BalabanJ
Balaban 的 J 指数（支化）描述符）。
```python
Descriptors.BalabanJ(mol)
```

## EState Indices

电拓扑状态索引。

### MaxEStateIndex
最大E状态值。
```python
Descriptors.MaxEStateIndex(mol)
```

### MinEStateIndex
最小 E 状态值。
```python
Descriptors.MinEStateIndex(mol)
```

### MaxAbsEStateIndex
最大绝对 E 状态值。
```python
Descriptors.MaxAbsEStateIndex(mol)
```

### MinAbsEStateIndex
最小绝对E状态值。
```python
Descriptors.MinAbsEStateIndex(mol)
```

## Partial Charges

### MaxPartialCharge
最大部分charge.
```python
Descriptors.MaxPartialCharge(mol)
```

### MinPartialCharge
最小部分电荷。
```python
Descriptors.MinPartialCharge(mol)
```

### MaxAbsPartialCharge
最大绝对部分电荷charge.
```python
Descriptors.MaxAbsPartialCharge(mol)
```

### MinAbsPartialCharge
最小绝对部分电荷.
```python
Descriptors.MinAbsPartialCharge(mol)
```

## Fingerprint Density

测量分子的密度Fingerprints.

### FpDensityMorgan1
半径处的摩根指纹密度 1.
```python
Descriptors.FpDensityMorgan1(mol)
```

### FpDensityMorgan2
半径处的摩根指纹密度2.
```python
Descriptors.FpDensityMorgan2(mol)
```

### FpDensityMorgan3
半径处的摩根指纹密度 3.
```python
Descriptors.FpDensityMorgan3(mol)
```

## PEOE VSA描述符

轨道电负性部分均衡(PEOE) VSA 描述符。

### PEOE_VSA1 到 PEOE_VSA14
MOE 型描述符，使用部分电荷和表面积贡献。
```python
Descriptors.PEOE_VSA1(mol)
# ... through PEOE_VSA14
```

## SMR VSA 描述符

分子折射率 VSA描述符。

### SMR_VSA1 到 SMR_VSA10
MOE 类型描述符，使用 MR 贡献和表面积。
```python
Descriptors.SMR_VSA1(mol)
# ... through SMR_VSA10
```

## SLogP VSA 描述符

LogP VSA 描述符。

### 使用 LogP 贡献和表面积的 SLogP_VSA1 到 SLogP_VSA12
MOE 类型描述符。
```python
Descriptors.SLogP_VSA1(mol)
# ... through SLogP_VSA12
```

## EState VSA 描述符

### EState_VSA1 到 EState_VSA11
MOE 类型描述符使用E状态指数和表面积。
```python
Descriptors.EState_VSA1(mol)
# ... through EState_VSA11
```

## VSA描述符

范德华表面积描述符。

### VSA_EState1 到 VSA_EState10
EState VSA 描述符。
```python
Descriptors.VSA_EState1(mol)
# ... through VSA_EState10
```

## BCUT 描述符

Burden-CAS-德克萨斯大学特征值描述符。

### BCUT2D_MWHI
按分子量加权的负荷矩阵的最高特征值。
```python
Descriptors.BCUT2D_MWHI(mol)
```

### BCUT2D_MWLOW
按分子加权的负荷矩阵的最低特征值权重.
```python
Descriptors.BCUT2D_MWLOW(mol)
```

### BCUT2D_CHGHI
按部分费用加权的最高特征值。
```python
Descriptors.BCUT2D_CHGHI(mol)
```

### BCUT2D_CHGLO
加权最低特征值
```python
Descriptors.BCUT2D_CHGLO(mol)
```

### BCUT2D_LOGPHI
LogP 加权的最高特征值。
```python
Descriptors.BCUT2D_LOGPHI(mol)
```

### BCUT2D_LOGPLOW
最低特征值按 LogP 加权。
```python
Descriptors.BCUT2D_LOGPLOW(mol)
```

### BCUT2D_MRHI
按摩尔折射率加权的最高特征值。
```python
Descriptors.BCUT2D_MRHI(mol)
```

### BCUT2D_MRLOW
Lowest按摩尔折射率加权的特征值。
```python
Descriptors.BCUT2D_MRLOW(mol)
```

## 自相关描述符

### AUTOCORR2D
2D自相关描述符（如果启用）。
测量空间分布的各种自相关指数属性。

## MQN 描述符

分子量子数 - 42 个简单描述符。

### mqn1 到 mqn42
计数各种分子特征的整数描述符。
```python
# Access via CalcMolDescriptors
desc = Descriptors.CalcMolDescriptors(mol)
mqns = {k: v for k, v in desc.items() if k.startswith('mqn')}
```

## QED

### qed
药物相似性定量估计。
```python
Descriptors.qed(mol)
```

## Lipinski 的五法则

使用 Lipinski 检查药物相似性标准：

```python
def lipinski_rule_of_five(mol):
    mw = Descriptors.MolWt(mol) <= 500
    logp = Descriptors.MolLogP(mol) <= 5
    hbd = Descriptors.NumHDonors(mol) <= 5
    hba = Descriptors.NumHAcceptors(mol) <= 10
    return mw and logp and hbd and hba
```

## 批量描述符计算

一次性计算所有描述符：

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

mol = Chem.MolFromSmiles('CCO')

# Get all descriptors as dictionary
all_descriptors = Descriptors.CalcMolDescriptors(mol)

# Access specific descriptor
mw = all_descriptors['MolWt']
logp = all_descriptors['MolLogP']

# Get list of available descriptor names
from rdkit.Chem import Descriptors
descriptor_names = [desc[0] for desc in Descriptors._descList]
```

## 描述符类别汇总

1. **物理化学**：MolWt、MolLogP、MolMR、TPSA
2. **拓扑**：BertzCT、BalabanJ、Kappa 指数
3. **电子**：部分收费，E状态指数
4. **形状**：Kappa 指数，BCUT 描述符
5. **连接性**：Chi 指数
6. **2D 指纹**：FpDensity 描述符
7. **原子计数**：重原子、杂原子、环
8. **药物相似性**：QED，Lipinski 参数
9. **灵活性**：NumRotatableBonds、HallKierAlpha
10. **表面积**：基于 VSA 的描述符

## 常见用例

### 药物相似性筛选

```python
def screen_druglikeness(mol):
    return {
        'MW': Descriptors.MolWt(mol),
        'LogP': Descriptors.MolLogP(mol),
        'HBD': Descriptors.NumHDonors(mol),
        'HBA': Descriptors.NumHAcceptors(mol),
        'TPSA': Descriptors.TPSA(mol),
        'RotBonds': Descriptors.NumRotatableBonds(mol),
        'AromaticRings': Descriptors.NumAromaticRings(mol),
        'QED': Descriptors.qed(mol)
    }
```

### 类铅过滤

```python
def is_leadlike(mol):
    mw = 250 <= Descriptors.MolWt(mol) <= 350
    logp = Descriptors.MolLogP(mol) <= 3.5
    rot_bonds = Descriptors.NumRotatableBonds(mol) <= 7
    return mw and logp and rot_bonds
```

### 多样性分析

```python
def molecular_complexity(mol):
    return {
        'BertzCT': Descriptors.BertzCT(mol),
        'NumRings': Descriptors.RingCount(mol),
        'NumRotBonds': Descriptors.NumRotatableBonds(mol),
        'FractionCsp3': Descriptors.FractionCsp3(mol),
        'NumAromaticRings': Descriptors.NumAromaticRings(mol)
    }
```

## 提示

1. **对多个描述符使用批量计算**以避免冗余计算
2. **检查“无”** - 某些描述符可能会为无效分子
3 返回“无”。 **机器学习应用程序的描述符标准化**
4. **选择相关描述符** - 并非所有 200 多个描述符都对每个任务 
5 都有用。 **单独考虑3D描述符**（需要3D坐标）
6. **验证范围** - 检查描述符值是否在预期范围内
