# RDKit 的常见 SMARTS 模式

本文档提供了 RDKit 中用于子结构搜索的常用 SMARTS 模式的集合。

## 官能团

### 醇类

```python
# Primary alcohol
'[CH2][OH1]'

# Secondary alcohol
'[CH1]([OH1])[CH3,CH2]'

# Tertiary alcohol
'[C]([OH1])([C])([C])[C]'

# Any alcohol
'[OH1][C]'

# Phenol
'c[OH1]'
```

### 醛类和酮类

```python
# Aldehyde
'[CH1](=O)'

# Ketone
'[C](=O)[C]'

# Any carbonyl
'[C](=O)'
```

### 羧酸及其衍生物

```python
# Carboxylic acid
'C(=O)[OH1]'
'[CX3](=O)[OX2H1]'  # More specific

# Ester
'C(=O)O[C]'
'[CX3](=O)[OX2][C]'  # More specific

# Amide
'C(=O)N'
'[CX3](=O)[NX3]'  # More specific

# Acyl chloride
'C(=O)Cl'

# Anhydride
'C(=O)OC(=O)'
```

### 胺类

```python
# Primary amine
'[NH2][C]'

# Secondary amine
'[NH1]([C])[C]'

# Tertiary amine
'[N]([C])([C])[C]'

# Aromatic amine (aniline)
'c[NH2]'

# Any amine
'[NX3]'
```

### 醚类

```python
# Aliphatic ether
'[C][O][C]'

# Aromatic ether
'c[O][C,c]'
```

### 卤化物

```python
# Alkyl halide
'[C][F,Cl,Br,I]'

# Aryl halide
'c[F,Cl,Br,I]'

# Specific halides
'[C]F'  # Fluoride
'[C]Cl'  # Chloride
'[C]Br'  # Bromide
'[C]I'  # Iodide
```

### 腈类和硝基类

```python
# Nitrile
'C#N'

# Nitro group
'[N+](=O)[O-]'

# Nitro on aromatic
'c[N+](=O)[O-]'
```

### 硫醇类和硫化物

```python
# Thiol
'[C][SH1]'

# Sulfide
'[C][S][C]'

# Disulfide
'[C][S][S][C]'

# Sulfoxide
'[C][S](=O)[C]'

# Sulfone
'[C][S](=O)(=O)[C]'
```

## 环系统

### 简单环

```python
# Benzene ring
'c1ccccc1'
'[#6]1:[#6]:[#6]:[#6]:[#6]:[#6]:1'  # Explicit atoms

# Cyclohexane
'C1CCCCC1'

# Cyclopentane
'C1CCCC1'

# Any 3-membered ring
'[r3]'

# Any 4-membered ring
'[r4]'

# Any 5-membered ring
'[r5]'

# Any 6-membered ring
'[r6]'

# Any 7-membered ring
'[r7]'
```

### 芳香环

```python
# Aromatic carbon in ring
'[cR]'

# Aromatic nitrogen in ring (pyridine, etc.)
'[nR]'

# Aromatic oxygen in ring (furan, etc.)
'[oR]'

# Aromatic sulfur in ring (thiophene, etc.)
'[sR]'

# Any aromatic ring
'a1aaaaa1'
```

### 杂环

```python
# Pyridine
'n1ccccc1'

# Pyrrole
'n1cccc1'

# Furan
'o1cccc1'

# Thiophene
's1cccc1'

# Imidazole
'n1cncc1'

# Pyrimidine
'n1cnccc1'

# Thiazole
'n1ccsc1'

# Oxazole
'n1ccoc1'
```

### 熔环

```python
# Naphthalene
'c1ccc2ccccc2c1'

# Indole
'c1ccc2[nH]ccc2c1'

# Quinoline
'n1cccc2ccccc12'

# Benzimidazole
'c1ccc2[nH]cnc2c1'

# Purine
'n1cnc2ncnc2c1'
```

### 大环

```python
# Rings with 8 or more atoms
'[r{8-}]'

# Rings with 9-15 atoms
'[r{9-15}]'

# Rings with more than 12 atoms (macrocycles)
'[r{12-}]'
```

## 具体结构特征

### 脂肪族与芳香族

```python
# Aliphatic carbon
'[C]'

# Aromatic carbon
'[c]'

# Aliphatic carbon in ring
'[CR]'

# Aromatic carbon (alternative)
'[cR]'
```

### 立体化学

```python
# Tetrahedral center with clockwise chirality
'[C@]'

# Tetrahedral center with counterclockwise chirality
'[C@@]'

# Any chiral center
'[C@,C@@]'

# E double bond
'C/C=C/C'

# Z double bond
'C/C=C\\C'
```

### 杂交

```python
# SP hybridization (triple bond)
'[CX2]'

# SP2 hybridization (double bond or aromatic)
'[CX3]'

# SP3 hybridization (single bonds)
'[CX4]'
```

### 电荷

```python
# Positive charge
'[+]'

# Negative charge
'[-]'

# Specific charge
'[+1]'
'[-1]'
'[+2]'

# Positively charged nitrogen
'[N+]'

# Negatively charged oxygen
'[O-]'

# Carboxylate anion
'C(=O)[O-]'

# Ammonium cation
'[N+]([C])([C])([C])[C]'
```

## 药效团特征

### 氢键供体

```python
# Hydroxyl
'[OH]'

# Amine
'[NH,NH2]'

# Amide NH
'[N][C](=O)'

# Any H-bond donor
'[OH,NH,NH2,NH3+]'
```

### 氢键受体

```python
# Carbonyl oxygen
'[O]=[C,S,P]'

# Ether oxygen
'[OX2]'

# Ester oxygen
'C(=O)[O]'

# Nitrogen acceptor
'[N;!H0]'

# Any H-bond acceptor
'[O,N]'
```

### 疏水基团

```python
# Alkyl chain (4+ carbons)
'CCCC'

# Branched alkyl
'C(C)(C)C'

# Aromatic rings (hydrophobic)
'c1ccccc1'
```

### 芳香族相互作用

```python
# Benzene for pi-pi stacking
'c1ccccc1'

# Heterocycle for pi-pi
'[a]1[a][a][a][a][a]1'

# Any aromatic ring
'[aR]'
```

## 药物样片段

### Lipinski片段

```python
# Aromatic ring with substituents
'c1cc(*)ccc1'

# Aliphatic chain
'CCCC'

# Ether linkage
'[C][O][C]'

# Amine (basic center)
'[N]([C])([C])'
```

### 通用脚手架

```python
# Benzamide
'c1ccccc1C(=O)N'

# Sulfonamide
'S(=O)(=O)N'

# Urea
'[N][C](=O)[N]'

# Guanidine
'[N]C(=[N])[N]'

# Phosphate
'P(=O)([O-])([O-])[O-]'
```

### 特权结构

```python
# Biphenyl
'c1ccccc1-c2ccccc2'

# Benzopyran
'c1ccc2OCCCc2c1'

# Piperazine
'N1CCNCC1'

# Piperidine
'N1CCCCC1'

# Morpholine
'N1CCOCC1'
```

## 反应组

### 亲电试剂

```python
# Acyl chloride
'C(=O)Cl'

# Alkyl halide
'[C][Cl,Br,I]'

# Epoxide
'C1OC1'

# Michael acceptor
'C=C[C](=O)'
```

### 亲核试剂

```python
# Primary amine
'[NH2][C]'

# Thiol
'[SH][C]'

# Alcohol
'[OH][C]'
```

## 毒性警报 (PAINS)

```python
# Rhodanine
'S1C(=O)NC(=S)C1'

# Catechol
'c1ccc(O)c(O)c1'

# Quinone
'O=C1C=CC(=O)C=C1'

# Hydroquinone
'OC1=CC=C(O)C=C1'

# Alkyl halide (reactive)
'[C][I,Br]'

# Michael acceptor (reactive)
'C=CC(=O)[C,N]'
```

## 金属绑定

```python
# Carboxylate (metal chelator)
'C(=O)[O-]'

# Hydroxamic acid
'C(=O)N[OH]'

# Catechol (iron chelator)
'c1c(O)c(O)ccc1'

# Thiol (metal binding)
'[SH]'

# Histidine-like (metal binding)
'c1ncnc1'
```

## 大小和复杂性过滤器

```python
# Long aliphatic chains (>6 carbons)
'CCCCCCC'

# Highly branched (quaternary carbon)
'C(C)(C)(C)C'

# Multiple rings
'[R]~[R]'  # Two rings connected

# Spiro center
'[C]12[C][C][C]1[C][C]2'
```

## 特殊模式

### 原子计数

```python
# Any atom
'[*]'

# Heavy atom (not H)
'[!H]'

# Carbon
'[C,c]'

# Heteroatom
'[!C;!H]'

# Halogen
'[F,Cl,Br,I]'
```

### 键类型

```python
# Single bond
'C-C'

# Double bond
'C=C'

# Triple bond
'C#C'

# Aromatic bond
'c:c'

# Any bond
'C~C'
```

### 环成员资格

```python
# In any ring
'[R]'

# Not in ring
'[!R]'

# In exactly one ring
'[R1]'

# In exactly two rings
'[R2]'

# Ring bond
'[R]~[R]'
```

### 度数和连接性

```python
# Total degree 1 (terminal atom)
'[D1]'

# Total degree 2 (chain)
'[D2]'

# Total degree 3 (branch point)
'[D3]'

# Total degree 4 (highly branched)
'[D4]'

# Connected to exactly 2 carbons
'[C]([C])[C]'
```

## 用法示例

```python
from rdkit import Chem

# Create SMARTS query
pattern = Chem.MolFromSmarts('[CH2][OH1]')  # Primary alcohol

# Search molecule
mol = Chem.MolFromSmiles('CCO')
matches = mol.GetSubstructMatches(pattern)

# Multiple patterns
patterns = {
    'alcohol': '[OH1][C]',
    'amine': '[NH2,NH1][C]',
    'carboxylic_acid': 'C(=O)[OH1]'
}

# Check for functional groups
for name, smarts in patterns.items():
    query = Chem.MolFromSmarts(smarts)
    if mol.HasSubstructMatch(query):
        print(f"Found {name}")
```

## SMARTS

编写技巧1. **需要时具体化：** 使用原子属性 [CX3]，而不仅仅是 [C]
2. **为了清楚起见，请使用括号：** [C]与 C（芳香族）
3 不同。 **考虑芳香性：**小写字母（c、n、o）是芳香性
4. **检查环成员身份：** [R]表示环内，[!R]表示非环
5. **使用递归 SMARTS：** $(...)用于复杂模式
6. **测试模​​式：** 始终在已知分子 
7 上验证 SMARTS。 **从简单开始：**逐步构建复杂模式

## 常见 SMARTS 语法

- `[C]` - 脂肪族碳
- `[c]` - 芳香族碳
- `[CX4]` - 具有 4 个连接的碳 (sp3)
- `[CX3]` - Carbon with 3 connections (sp2)
- `[CX2]` - Carbon with 2 connections (sp)
- `[CH3]` - Methyl group
- `[R]` - In ring
- `[r6]` - In 6-membered ring
- `[r{5-7}]` - In 5, 6, or 7-membered ring
- `[D2]` - Degree 2 (2 neighbors)
- `[+]` - Positive charge
- `[-]` - Negative电荷
- `[!C]` - 非碳
- `[#6]` - 原子序数为6的元素（碳）
- `~` - 任何键类型
- `-` - 单键
- `=` - Double bond
- `#` - Triple bond
- `:` - Aromatic bond
- `@` - Clockwise chirality
- `@@` - Counter-clockwise手性
