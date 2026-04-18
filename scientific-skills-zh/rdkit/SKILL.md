---
name: rdkit
description: 用于细粒度分子控制的化学信息学工具包。 SMILES/SDF 解析、描述符（MW、LogP、TPSA）、指纹、子结构搜索、2D/3D 生成、相似性、反应。对于具有更简单界面的标准工作流程，请使用 datamol（RDKit 的包装器）。使用 rdkit 进行高级控制、自定义清理、专用算法。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# RDKit 化学信息学工具包

## 概述

RDKit 是一个综合性化学信息学库，提供用于分子分析和操作的 Python API。该技能为读/写分子结构、计算描述符、指纹识别、子结构搜索、化学反应、2D/3D 坐标生成和分子可视化提供指导。使用此技能进行药物发现、计算化学和化学信息学研究任务。

## 核心功能

### 1. 分子 I/O 和创建

* *阅读分子：**

 读取各种格式的分子结构：

```python
from rdkit import Chem

# From SMILES strings
mol = Chem.MolFromSmiles('Cc1ccccc1')  # Returns Mol object or None

# From MOL files
mol = Chem.MolFromMolFile('path/to/file.mol')

# From MOL blocks (string data)
mol = Chem.MolFromMolBlock(mol_block_string)

# From InChI
mol = Chem.MolFromInchi('InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H')
```

* *写作分子：**

将分子转换为文本表示形式：

```python
# To canonical SMILES
smiles = Chem.MolToSmiles(mol)

# To MOL block
mol_block = Chem.MolToMolBlock(mol)

# To InChI
inchi = Chem.MolToInchi(mol)
```

* *批处理：**

要处理多个分子，请使用供应商/写入器对象：

```python
# Read SDF files
suppl = Chem.SDMolSupplier('molecules.sdf')
for mol in suppl:
    if mol is not None:  # Check for parsing errors
        # Process molecule
        pass

# Read SMILES files
suppl = Chem.SmilesMolSupplier('molecules.smi', titleLine=False)

# For large files or compressed data
with gzip.open('molecules.sdf.gz') as f:
    suppl = Chem.ForwardSDMolSupplier(f)
    for mol in suppl:
        # Process molecule
        pass

# Multithreaded processing for large datasets
suppl = Chem.MultithreadedSDMolSupplier('molecules.sdf')

# Write molecules to SDF
writer = Chem.SDWriter('output.sdf')
for mol in molecules:
    writer.write(mol)
writer.close()
```

* *重要注意：**
- 所有 `MolFrom*` 函数在失败时返回 `None`，并显示错误消息
- 在处理分子之前始终检查 `None`
- 分子在导入时自动净化（验证化合价，感知芳香性）

### 2. 分子净化和验证

RDKit在解析过程中自动清理分子，执行13个步骤，包括化合价检查、芳香性感知和手性分配。

* *清理控制：**

```python
# Disable automatic sanitization
mol = Chem.MolFromSmiles('C1=CC=CC=C1', sanitize=False)

# Manual sanitization
Chem.SanitizeMol(mol)

# Detect problems before sanitization
problems = Chem.DetectChemistryProblems(mol)
for problem in problems:
    print(problem.GetType(), problem.Message())

# Partial sanitization (skip specific steps)
from rdkit.Chem import rdMolStandardize
Chem.SanitizeMol(mol, sanitizeOps=Chem.SANITIZE_ALL ^ Chem.SANITIZE_PROPERTIES)
```

* *常见清理问题：**
- 具有超过最大化合价的原子允许将引发异常
- 无效的芳环将导致kekulization错误
- 如果没有明确的说明，自由基电子可能无法正确分配

### 3.分子分析和性质

* *访问分子结构：**

```python
# Iterate atoms and bonds
for atom in mol.GetAtoms():
    print(atom.GetSymbol(), atom.GetIdx(), atom.GetDegree())

for bond in mol.GetBonds():
    print(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx(), bond.GetBondType())

# Ring information
ring_info = mol.GetRingInfo()
ring_info.NumRings()
ring_info.AtomRings()  # Returns tuples of atom indices

# Check if atom is in ring
atom = mol.GetAtomWithIdx(0)
atom.IsInRing()
atom.IsInRingSize(6)  # Check for 6-membered rings

# Find smallest set of smallest rings (SSSR)
from rdkit.Chem import GetSymmSSSR
rings = GetSymmSSSR(mol)
```

* *立体化学：**

```python
# Find chiral centers
from rdkit.Chem import FindMolChiralCenters
chiral_centers = FindMolChiralCenters(mol, includeUnassigned=True)
# Returns list of (atom_idx, chirality) tuples

# Assign stereochemistry from 3D coordinates
from rdkit.Chem import AssignStereochemistryFrom3D
AssignStereochemistryFrom3D(mol)

# Check bond stereochemistry
bond = mol.GetBondWithIdx(0)
stereo = bond.GetStereo()  # STEREONONE, STEREOZ, STEREOE, etc.
```

* *片段分析：**

```python
# Get disconnected fragments
frags = Chem.GetMolFrags(mol, asMols=True)

# Fragment on specific bonds
from rdkit.Chem import FragmentOnBonds
frag_mol = FragmentOnBonds(mol, [bond_idx1, bond_idx2])

# Count ring systems
from rdkit.Chem.Scaffolds import MurckoScaffold
scaffold = MurckoScaffold.GetScaffoldForMol(mol)
```

### 4. 分子描述符和属性

* *基本描述符：**

```python
from rdkit.Chem import Descriptors

# Molecular weight
mw = Descriptors.MolWt(mol)
exact_mw = Descriptors.ExactMolWt(mol)

# LogP (lipophilicity)
logp = Descriptors.MolLogP(mol)

# Topological polar surface area
tpsa = Descriptors.TPSA(mol)

# Number of hydrogen bond donors/acceptors
hbd = Descriptors.NumHDonors(mol)
hba = Descriptors.NumHAcceptors(mol)

# Number of rotatable bonds
rot_bonds = Descriptors.NumRotatableBonds(mol)

# Number of aromatic rings
aromatic_rings = Descriptors.NumAromaticRings(mol)
```

* *批次描述符计算：**

```python
# Calculate all descriptors at once
all_descriptors = Descriptors.CalcMolDescriptors(mol)
# Returns dictionary: {'MolWt': 180.16, 'MolLogP': 1.23, ...}

# Get list of available descriptor names
descriptor_names = [desc[0] for desc in Descriptors._descList]
```

* *Lipinski 的五法则：**

```python
# Check drug-likeness
mw = Descriptors.MolWt(mol) <= 500
logp = Descriptors.MolLogP(mol) <= 5
hbd = Descriptors.NumHDonors(mol) <= 5
hba = Descriptors.NumHAcceptors(mol) <= 10

is_drug_like = mw and logp and hbd and hba
```

### 5. 指纹和分子相似性

* *指纹类型：**

```python
from rdkit.Chem import rdFingerprintGenerator
from rdkit.Chem import MACCSkeys

# RDKit topological fingerprint
rdk_gen = rdFingerprintGenerator.GetRDKitFPGenerator(minPath=1, maxPath=7, fpSize=2048)
fp = rdk_gen.GetFingerprint(mol)

# Morgan fingerprints (circular fingerprints, similar to ECFP)
# Modern API using rdFingerprintGenerator
morgan_gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
fp = morgan_gen.GetFingerprint(mol)
# Count-based fingerprint
fp_count = morgan_gen.GetCountFingerprint(mol)

# MACCS keys (166-bit structural key)
fp = MACCSkeys.GenMACCSKeys(mol)

# Atom pair fingerprints
ap_gen = rdFingerprintGenerator.GetAtomPairGenerator()
fp = ap_gen.GetFingerprint(mol)

# Topological torsion fingerprints
tt_gen = rdFingerprintGenerator.GetTopologicalTorsionGenerator()
fp = tt_gen.GetFingerprint(mol)

# Avalon fingerprints (if available)
from rdkit.Avalon import pyAvalonTools
fp = pyAvalonTools.GetAvalonFP(mol)
```

* *相似度计算：**

```python
from rdkit import DataStructs
from rdkit.Chem import rdFingerprintGenerator

# Generate fingerprints using generator
mfpgen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
fp1 = mfpgen.GetFingerprint(mol1)
fp2 = mfpgen.GetFingerprint(mol2)

# Calculate Tanimoto similarity
similarity = DataStructs.TanimotoSimilarity(fp1, fp2)

# Calculate similarity for multiple molecules
fps = [mfpgen.GetFingerprint(m) for m in [mol2, mol3, mol4]]
similarities = DataStructs.BulkTanimotoSimilarity(fp1, fps)

# Other similarity metrics
dice = DataStructs.DiceSimilarity(fp1, fp2)
cosine = DataStructs.CosineSimilarity(fp1, fp2)
```

* *聚类和多样性：**

```python
# Butina clustering based on fingerprint similarity
from rdkit.ML.Cluster import Butina

# Calculate distance matrix
dists = []
mfpgen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
fps = [mfpgen.GetFingerprint(mol) for mol in mols]
for i in range(len(fps)):
    sims = DataStructs.BulkTanimotoSimilarity(fps[i], fps[:i])
    dists.extend([1-sim for sim in sims])

# Cluster with distance cutoff
clusters = Butina.ClusterData(dists, len(fps), distThresh=0.3, isDistData=True)
```

### 6. 子结构搜索和SMARTS

* *基本子结构匹配：**

```python
# Define query using SMARTS
query = Chem.MolFromSmarts('[#6]1:[#6]:[#6]:[#6]:[#6]:[#6]:1')  # Benzene ring

# Check if molecule contains substructure
has_match = mol.HasSubstructMatch(query)

# Get all matches (returns tuple of tuples with atom indices)
matches = mol.GetSubstructMatches(query)

# Get only first match
match = mol.GetSubstructMatch(query)
```

* *常见 SMARTS 模式：**

```python
# Primary alcohols
primary_alcohol = Chem.MolFromSmarts('[CH2][OH1]')

# Carboxylic acids
carboxylic_acid = Chem.MolFromSmarts('C(=O)[OH]')

# Amides
amide = Chem.MolFromSmarts('C(=O)N')

# Aromatic heterocycles
aromatic_n = Chem.MolFromSmarts('[nR]')  # Aromatic nitrogen in ring

# Macrocycles (rings > 12 atoms)
macrocycle = Chem.MolFromSmarts('[r{12-}]')
```

* *匹配规则：**
- 查询中未指定的属性匹配中的任何值target
- 除非明确指定，否则氢将被忽略
- 带电查询原子不会匹配不带电的目标原子
- 芳香族查询原子不会匹配脂肪族目标原子（除非查询是通用的）

### 7. 化学反应

* *反应SMARTS：**

```python
from rdkit.Chem import AllChem

# Define reaction using SMARTS: reactants >> products
rxn = AllChem.ReactionFromSmarts('[C:1]=[O:2]>>[C:1][O:2]')  # Ketone reduction

# Apply reaction to molecules
reactants = (mol1,)
products = rxn.RunReactants(reactants)

# Products is tuple of tuples (one tuple per product set)
for product_set in products:
    for product in product_set:
        # Sanitize product
        Chem.SanitizeMol(product)
```

* *反应特征：**
- 原子映射保留反应物和产物之间的特定原子
- 产物中的虚拟原子被相应的反应物原子取代
- “任何”键继承反应物的键序
- 手性除非明确更改，否则保留

* *反应相似性：**

```python
# Generate reaction fingerprints
fp = AllChem.CreateDifferenceFingerprintForReaction(rxn)

# Compare reactions
similarity = DataStructs.TanimotoSimilarity(fp1, fp2)
```

### 8. 2D 和 3D 坐标生成

* *2D 坐标生成：**

```python
from rdkit.Chem import AllChem

# Generate 2D coordinates for depiction
AllChem.Compute2DCoords(mol)

# Align molecule to template structure
template = Chem.MolFromSmiles('c1ccccc1')
AllChem.Compute2DCoords(template)
AllChem.GenerateDepictionMatching2DStructure(mol, template)
```

* *3D 坐标生成和构象：**

```python
# Generate single 3D conformer using ETKDG
AllChem.EmbedMolecule(mol, randomSeed=42)

# Generate multiple conformers
conf_ids = AllChem.EmbedMultipleConfs(mol, numConfs=10, randomSeed=42)

# Optimize geometry with force field
AllChem.UFFOptimizeMolecule(mol)  # UFF force field
AllChem.MMFFOptimizeMolecule(mol)  # MMFF94 force field

# Optimize all conformers
for conf_id in conf_ids:
    AllChem.MMFFOptimizeMolecule(mol, confId=conf_id)

# Calculate RMSD between conformers
from rdkit.Chem import AllChem
rms = AllChem.GetConformerRMS(mol, conf_id1, conf_id2)

# Align molecules
AllChem.AlignMol(probe_mol, ref_mol)
```

* *约束嵌入：**

```python
# Embed with part of molecule constrained to specific coordinates
AllChem.ConstrainedEmbed(mol, core_mol)
```

### 9. 分子可视化

* *基本绘图：**

```python
from rdkit.Chem import Draw

# Draw single molecule to PIL image
img = Draw.MolToImage(mol, size=(300, 300))
img.save('molecule.png')

# Draw to file directly
Draw.MolToFile(mol, 'molecule.png')

# Draw multiple molecules in grid
mols = [mol1, mol2, mol3, mol4]
img = Draw.MolsToGridImage(mols, molsPerRow=2, subImgSize=(200, 200))
```

* *突出显示子结构：**

```python
# Highlight substructure match
query = Chem.MolFromSmarts('c1ccccc1')
match = mol.GetSubstructMatch(query)

img = Draw.MolToImage(mol, highlightAtoms=match)

# Custom highlight colors
highlight_colors = {atom_idx: (1, 0, 0) for atom_idx in match}  # Red
img = Draw.MolToImage(mol, highlightAtoms=match,
                      highlightAtomColors=highlight_colors)
```

* *自定义可视化：**

```python
from rdkit.Chem.Draw import rdMolDraw2D

# Create drawer with custom options
drawer = rdMolDraw2D.MolDraw2DCairo(300, 300)
opts = drawer.drawOptions()

# Customize options
opts.addAtomIndices = True
opts.addStereoAnnotation = True
opts.bondLineWidth = 2

# Draw molecule
drawer.DrawMolecule(mol)
drawer.FinishDrawing()

# Save to file
with open('molecule.png', 'wb') as f:
    f.write(drawer.GetDrawingText())
```

* *Jupyter Notebook集成：**

```python
# Enable inline display in Jupyter
from rdkit.Chem.Draw import IPythonConsole

# Customize default display
IPythonConsole.ipython_useSVG = True  # Use SVG instead of PNG
IPythonConsole.molSize = (300, 300)   # Default size

# Molecules now display automatically
mol  # Shows molecule image
```

* *可视化指纹位：**

```python
# Show what molecular features a fingerprint bit represents
from rdkit.Chem import Draw

# For Morgan fingerprints
bit_info = {}
fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, bitInfo=bit_info)

# Draw environment for specific bit
img = Draw.DrawMorganBit(mol, bit_id, bit_info)
```

### 10.分子修饰

* *添加/删除氢：**

```python
# Add explicit hydrogens
mol_h = Chem.AddHs(mol)

# Remove explicit hydrogens
mol = Chem.RemoveHs(mol_h)
```

* *Kekulization 和芳香性：**

```python
# Convert aromatic bonds to alternating single/double
Chem.Kekulize(mol)

# Set aromaticity
Chem.SetAromaticity(mol)
```

* *替换子结构：**

```python
# Replace substructure with another structure
query = Chem.MolFromSmarts('c1ccccc1')  # Benzene
replacement = Chem.MolFromSmiles('C1CCCCC1')  # Cyclohexane

new_mol = Chem.ReplaceSubstructs(mol, query, replacement)[0]
```

* *中和费用：**

```python
# Remove formal charges by adding/removing hydrogens
from rdkit.Chem.MolStandardize import rdMolStandardize

# Using Uncharger
uncharger = rdMolStandardize.Uncharger()
mol_neutral = uncharger.uncharge(mol)
```

### 11. 使用分子哈希和标准化

* *分子哈希：**

```python
from rdkit.Chem import rdMolHash

# Generate Murcko scaffold hash
scaffold_hash = rdMolHash.MolHash(mol, rdMolHash.HashFunction.MurckoScaffold)

# Canonical SMILES hash
canonical_hash = rdMolHash.MolHash(mol, rdMolHash.HashFunction.CanonicalSmiles)

# Regioisomer hash (ignores stereochemistry)
regio_hash = rdMolHash.MolHash(mol, rdMolHash.HashFunction.Regioisomer)
```

* *随机微笑：**

```python
# Generate random SMILES representations (for data augmentation)
from rdkit.Chem import MolToRandomSmilesVect

random_smiles = MolToRandomSmilesVect(mol, numSmiles=10, randomSeed=42)
```

### 12. 药效团和 3D 特征

* *药效团特征：**

```python
from rdkit.Chem import ChemicalFeatures
from rdkit import RDConfig
import os

# Load feature factory
fdef_path = os.path.join(RDConfig.RDDataDir, 'BaseFeatures.fdef')
factory = ChemicalFeatures.BuildFeatureFactory(fdef_path)

# Get pharmacophore features
features = factory.GetFeaturesForMol(mol)

for feat in features:
    print(feat.GetFamily(), feat.GetType(), feat.GetAtomIds())
```

## 常见工作流程

### 药物相似性分析

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

def analyze_druglikeness(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    # Calculate Lipinski descriptors
    results = {
        'MW': Descriptors.MolWt(mol),
        'LogP': Descriptors.MolLogP(mol),
        'HBD': Descriptors.NumHDonors(mol),
        'HBA': Descriptors.NumHAcceptors(mol),
        'TPSA': Descriptors.TPSA(mol),
        'RotBonds': Descriptors.NumRotatableBonds(mol)
    }

    # Check Lipinski's Rule of Five
    results['Lipinski'] = (
        results['MW'] <= 500 and
        results['LogP'] <= 5 and
        results['HBD'] <= 5 and
        results['HBA'] <= 10
    )

    return results
```

### 相似性筛选

```python
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs

def similarity_screen(query_smiles, database_smiles, threshold=0.7):
    query_mol = Chem.MolFromSmiles(query_smiles)
    query_fp = AllChem.GetMorganFingerprintAsBitVect(query_mol, 2)

    hits = []
    for idx, smiles in enumerate(database_smiles):
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2)
            sim = DataStructs.TanimotoSimilarity(query_fp, fp)
            if sim >= threshold:
                hits.append((idx, smiles, sim))

    return sorted(hits, key=lambda x: x[2], reverse=True)
```

### 子结构过滤

```python
from rdkit import Chem

def filter_by_substructure(smiles_list, pattern_smarts):
    query = Chem.MolFromSmarts(pattern_smarts)

    hits = []
    for smiles in smiles_list:
        mol = Chem.MolFromSmiles(smiles)
        if mol and mol.HasSubstructMatch(query):
            hits.append(smiles)

    return hits
```

## 最佳实践

### 错误处理

解析分子时始终检查`None`：

```python
mol = Chem.MolFromSmiles(smiles)
if mol is None:
    print(f"Failed to parse: {smiles}")
    continue
```

### 性能优化

* *使用二进制格式存储：**

```python
import pickle

# Pickle molecules for fast loading
with open('molecules.pkl', 'wb') as f:
    pickle.dump(mols, f)

# Load pickled molecules (much faster than reparsing)
with open('molecules.pkl', 'rb') as f:
    mols = pickle.load(f)
```

* *使用批量操作：**

```python
# Calculate fingerprints for all molecules at once
fps = [AllChem.GetMorganFingerprintAsBitVect(mol, 2) for mol in mols]

# Use bulk similarity calculations
similarities = DataStructs.BulkTanimotoSimilarity(fps[0], fps[1:])
```

### 线程安全

RDKit 操作通常是线程安全的：
- 分子 I/O（SMILES、mol块）
- 坐标生成
- 指纹和描述符
- 子结构搜索
- 反应
- 绘图

* *不是线程安全的：**并发访问时的MolSuppliers。

### 内存管理

对于大数据集：

```python
# Use ForwardSDMolSupplier to avoid loading entire file
with open('large.sdf') as f:
    suppl = Chem.ForwardSDMolSupplier(f)
    for mol in suppl:
        # Process one molecule at a time
        pass

# Use MultithreadedSDMolSupplier for parallel processing
suppl = Chem.MultithreadedSDMolSupplier('large.sdf', numWriterThreads=4)
```

## 常见陷阱

1. **忘记检查 None：** 解析 
2 后始终验证分子。 **清理失败：** 使用`DetectChemistryProblems()`调试
3. **缺少氢：** 在计算依赖于氢的属性时使用 `AddHs()`
4. **2D 与 3D：** 在可视化或 3D 分析之前生成适当的坐标
5. **SMARTS 匹配规则：** 请记住，未指定的属性会匹配任何内容
6. **MolSuppliers 的线程安全性：** 不要跨线程共享供应商对象

## 资源

### 参考资料/

此技能包括详细的 API 参考文档：

- `api_reference.md` - 按功能组织的 RDKit 模块、函数和类的综合列表
- `descriptors_reference.md` - 可用分子描述符的完整列表及描述
- `smarts_patterns.md` - 功能组和结构特征的常见 SMARTS 模式

在需要特定 API 详细信息、参数信息或模式示例时加载这些参考。

### 脚本/

常见 RDKit 工作流程的示例脚本：

- `molecular_properties.py` - 计算全面的分子特性和描述符
- `similarity_search.py` - 执行基于指纹的相似性筛选
- `substructure_filter.py` - 按子结构模式过滤分子

这些脚本可以直接执行或用作自定义工作流程的模板。
