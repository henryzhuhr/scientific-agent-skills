---
name: datamol
description: RDKit 的 Pythonic 包装器，具有简化的界面和合理的默认值。标准药物发现的首选，包括 SMILES 解析、标准化、描述符、指纹、聚类、3D 构象异构体、并行处理。返回本机 rdkit.Chem.Mol 对象。对于高级控制或自定义参数，直接使用rdkit。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# Datamol 化学信息学技能

## 概述

Datamol 是一个Python 库，它在RDKit 上为分子化学信息学提供了一个轻量级的Pythonic 抽象层。通过合理的默认值、高效的并行化和现代 I/O 功能来简化复杂的分子操作。所有分子对象均为原生 `rdkit.Chem.Mol` 实例，确保与 RDKit 生态系统完全兼容。

* *关键功能**：
- 分子格式转换（SMILES、SELFIES、InChI）
- 结构标准化和清理
- 分子描述符和指纹
- 3D构象异构体生成和分析
- 聚类和多样性选择
- 支架和片段分析
- 化学反应应用
- 可视化和比对
- 并行化批处理
- 通过fsspec的云存储支持

## 安装和设置

指南用户安装 datamol:

```bash
uv pip install datamol
```

* *导入约定**:
```python
import datamol as dm
```

## 核心工作流程

### 1. 基本分子处理

* *从创建分子SMILES**:
```python
import datamol as dm

# Single molecule
mol = dm.to_mol("CCO")  # Ethanol

# From list of SMILES
smiles_list = ["CCO", "c1ccccc1", "CC(=O)O"]
mols = [dm.to_mol(smi) for smi in smiles_list]

# Error handling
mol = dm.to_mol("invalid_smiles")  # Returns None
if mol is None:
    print("Failed to parse SMILES")
```

* *将分子转换为 SMILES**:
```python
# Canonical SMILES
smiles = dm.to_smiles(mol)

# Isomeric SMILES (includes stereochemistry)
smiles = dm.to_smiles(mol, isomeric=True)

# Other formats
inchi = dm.to_inchi(mol)
inchikey = dm.to_inchikey(mol)
selfies = dm.to_selfies(mol)
```

* *标准化和消毒**（始终建议用户提供分子):
```python
# Sanitize molecule
mol = dm.sanitize_mol(mol)

# Full standardization (recommended for datasets)
mol = dm.standardize_mol(
    mol,
    disconnect_metals=True,
    normalize=True,
    reionize=True
)

# For SMILES strings directly
clean_smiles = dm.standardize_smiles(smiles)
```

### 2.读写分子文件

参考`references/io_module.md`全面的I/O文档。

* *读取文件**:
```python
# SDF files (most common in chemistry)
df = dm.read_sdf("compounds.sdf", mol_column='mol')

# SMILES files
df = dm.read_smi("molecules.smi", smiles_column='smiles', mol_column='mol')

# CSV with SMILES column
df = dm.read_csv("data.csv", smiles_column="SMILES", mol_column="mol")

# Excel files
df = dm.read_excel("compounds.xlsx", sheet_name=0, mol_column="mol")

# Universal reader (auto-detects format)
df = dm.open_df("file.sdf")  # Works with .sdf, .csv, .xlsx, .parquet, .json
```

* *写入files**:
```python
# Save as SDF
dm.to_sdf(mols, "output.sdf")
# Or from DataFrame
dm.to_sdf(df, "output.sdf", mol_column="mol")

# Save as SMILES file
dm.to_smi(mols, "output.smi")

# Excel with rendered molecule images
dm.to_xlsx(df, "output.xlsx", mol_columns=["mol"])
```

* *远程文件支持** (S3, GCS, HTTP):
```python
# Read from cloud storage
df = dm.read_sdf("s3://bucket/compounds.sdf")
df = dm.read_csv("https://example.com/data.csv")

# Write to cloud storage
dm.to_sdf(mols, "s3://bucket/output.sdf")
```

### 3. 分子描述符和属性

详细描述符参见`references/descriptors_viz.md` Documentation.

* *计算单个分子的描述符**：
```python
# Get standard descriptor set
descriptors = dm.descriptors.compute_many_descriptors(mol)
# Returns: {'mw': 46.07, 'logp': -0.03, 'hbd': 1, 'hba': 1,
#           'tpsa': 20.23, 'n_aromatic_atoms': 0, ...}
```

* *批量描述符计算**（推荐用于数据集）：
```python
# Compute for all molecules in parallel
desc_df = dm.descriptors.batch_compute_many_descriptors(
    mols,
    n_jobs=-1,      # Use all CPU cores
    progress=True   # Show progress bar
)
```

* *具体描述符**：
```python
# Aromaticity
n_aromatic = dm.descriptors.n_aromatic_atoms(mol)
aromatic_ratio = dm.descriptors.n_aromatic_atoms_proportion(mol)

# Stereochemistry
n_stereo = dm.descriptors.n_stereo_centers(mol)
n_unspec = dm.descriptors.n_stereo_centers_unspecified(mol)

# Flexibility
n_rigid = dm.descriptors.n_rigid_bonds(mol)
```

* *药物相似性过滤（Lipinski五法则）**：
```python
# Filter compounds
def is_druglike(mol):
    desc = dm.descriptors.compute_many_descriptors(mol)
    return (
        desc['mw'] <= 500 and
        desc['logp'] <= 5 and
        desc['hbd'] <= 5 and
        desc['hba'] <= 10
    )

druglike_mols = [mol for mol in mols if is_druglike(mol)]
```

### 4.分子指纹和相似性

* *生成指纹**：
```python
# ECFP (Extended Connectivity Fingerprint, default)
fp = dm.to_fp(mol, fp_type='ecfp', radius=2, n_bits=2048)

# Other fingerprint types
fp_maccs = dm.to_fp(mol, fp_type='maccs')
fp_topological = dm.to_fp(mol, fp_type='topological')
fp_atompair = dm.to_fp(mol, fp_type='atompair')
```

* *相似度计算**：
```python
# Pairwise distances within a set
distance_matrix = dm.pdist(mols, n_jobs=-1)

# Distances between two sets
distances = dm.cdist(query_mols, library_mols, n_jobs=-1)

# Find most similar molecules
from scipy.spatial.distance import squareform
dist_matrix = squareform(dm.pdist(mols))
# Lower distance = higher similarity (Tanimoto distance = 1 - Tanimoto similarity)
```

### 5.聚类和多样性选择

聚类详细信息请参阅`references/core_api.md`。

* *Butina聚类**：
```python
# Cluster molecules by structural similarity
clusters = dm.cluster_mols(
    mols,
    cutoff=0.2,    # Tanimoto distance threshold (0=identical, 1=completely different)
    n_jobs=-1      # Parallel processing
)

# Each cluster is a list of molecule indices
for i, cluster in enumerate(clusters):
    print(f"Cluster {i}: {len(cluster)} molecules")
    cluster_mols = [mols[idx] for idx in cluster]
```

* *重要**：Butina聚类构建全距离矩阵 - 适合~1000个分子，不适用于10,000+。

* *多样性选择**：
```python
# Pick diverse subset
diverse_mols = dm.pick_diverse(
    mols,
    npick=100  # Select 100 diverse molecules
)

# Pick cluster centroids
centroids = dm.pick_centroids(
    mols,
    npick=50   # Select 50 representative molecules
)
```

### 6.支架分析

完整的脚手架文档请参阅`references/fragments_scaffolds.md`。

* *提取Murcko脚手架**：
```python
# Get Bemis-Murcko scaffold (core structure)
scaffold = dm.to_scaffold_murcko(mol)
scaffold_smiles = dm.to_smiles(scaffold)
```

* *基于脚手架的分析**：
```python
# Group compounds by scaffold
from collections import Counter

scaffolds = [dm.to_scaffold_murcko(mol) for mol in mols]
scaffold_smiles = [dm.to_smiles(s) for s in scaffolds]

# Count scaffold frequency
scaffold_counts = Counter(scaffold_smiles)
most_common = scaffold_counts.most_common(10)

# Create scaffold-to-molecules mapping
scaffold_groups = {}
for mol, scaf_smi in zip(mols, scaffold_smiles):
    if scaf_smi not in scaffold_groups:
        scaffold_groups[scaf_smi] = []
    scaffold_groups[scaf_smi].append(mol)
```

* *基于脚手架训练/测试分裂**（针对 ML）：
```python
# Ensure train and test sets have different scaffolds
scaffold_to_mols = {}
for mol, scaf in zip(mols, scaffold_smiles):
    if scaf not in scaffold_to_mols:
        scaffold_to_mols[scaf] = []
    scaffold_to_mols[scaf].append(mol)

# Split scaffolds into train/test
import random
scaffolds = list(scaffold_to_mols.keys())
random.shuffle(scaffolds)
split_idx = int(0.8 * len(scaffolds))
train_scaffolds = scaffolds[:split_idx]
test_scaffolds = scaffolds[split_idx:]

# Get molecules for each split
train_mols = [mol for scaf in train_scaffolds for mol in scaffold_to_mols[scaf]]
test_mols = [mol for scaf in test_scaffolds for mol in scaffold_to_mols[scaf]]
```

### 7. 分子碎片

碎片详细信息请参阅 `references/fragments_scaffolds.md`。

* *BRICS 碎片**（16 键）类型）：
```python
# Fragment molecule
fragments = dm.fragment.brics(mol)
# Returns: set of fragment SMILES with attachment points like '[1*]CCN'
```

* *RECAP碎片**（11种键类型）：
```python
fragments = dm.fragment.recap(mol)
```

* *碎片分析**：
```python
# Find common fragments across compound library
from collections import Counter

all_fragments = []
for mol in mols:
    frags = dm.fragment.brics(mol)
    all_fragments.extend(frags)

fragment_counts = Counter(all_fragments)
common_frags = fragment_counts.most_common(20)

# Fragment-based scoring
def fragment_score(mol, reference_fragments):
    mol_frags = dm.fragment.brics(mol)
    overlap = mol_frags.intersection(reference_fragments)
    return len(overlap) / len(mol_frags) if mol_frags else 0
```

### 8. 3D Conformer生成

详细的一致体文档请参考`references/conformers_module.md`。

* *生成一致体**:
```python
# Generate 3D conformers
mol_3d = dm.conformers.generate(
    mol,
    n_confs=50,           # Number to generate (auto if None)
    rms_cutoff=0.5,       # Filter similar conformers (Ångströms)
    minimize_energy=True,  # Minimize with UFF force field
    method='ETKDGv3'      # Embedding method (recommended)
)

# Access conformers
n_conformers = mol_3d.GetNumConformers()
conf = mol_3d.GetConformer(0)  # Get first conformer
positions = conf.GetPositions()  # Nx3 array of atom coordinates
```

* *一致体聚类**:
```python
# Cluster conformers by RMSD
clusters = dm.conformers.cluster(
    mol_3d,
    rms_cutoff=1.0,
    centroids=False
)

# Get representative conformers
centroids = dm.conformers.return_centroids(mol_3d, clusters)
```

* *SASA计算**:
```python
# Calculate solvent accessible surface area
sasa_values = dm.conformers.sasa(mol_3d, n_jobs=-1)

# Access SASA from conformer properties
conf = mol_3d.GetConformer(0)
sasa = conf.GetDoubleProp('rdkit_free_sasa')
```

### 9. 可视化

可视化文档参见`references/descriptors_viz.md`。

* *基本分子网格**:
```python
# Visualize molecules
dm.viz.to_image(
    mols[:20],
    legends=[dm.to_smiles(m) for m in mols[:20]],
    n_cols=5,
    mol_size=(300, 300)
)

# Save to file
dm.viz.to_image(mols, outfile="molecules.png")

# SVG for publications
dm.viz.to_image(mols, outfile="molecules.svg", use_svg=True)
```

* *对齐可视化**（对于SAR）分析）：
```python
# Align molecules by common substructure
dm.viz.to_image(
    similar_mols,
    align=True,  # Enable MCS alignment
    legends=activity_labels,
    n_cols=4
)
```

* *突出显示子结构**：
```python
# Highlight specific atoms and bonds
dm.viz.to_image(
    mol,
    highlight_atom=[0, 1, 2, 3],  # Atom indices
    highlight_bond=[0, 1, 2]      # Bond indices
)
```

* *构象可视化**：
```python
# Display multiple conformers
dm.viz.conformers(
    mol_3d,
    n_confs=10,
    align_conf=True,
    n_cols=3
)
```

### 10. 化学反应

有关反应文档，请参阅`references/reactions_data.md`。

* *应用反应**：
```python
from rdkit.Chem import rdChemReactions

# Define reaction from SMARTS
rxn_smarts = '[C:1](=[O:2])[OH:3]>>[C:1](=[O:2])[Cl:3]'
rxn = rdChemReactions.ReactionFromSmarts(rxn_smarts)

# Apply to molecule
reactant = dm.to_mol("CC(=O)O")  # Acetic acid
product = dm.reactions.apply_reaction(
    rxn,
    (reactant,),
    sanitize=True
)

# Convert to SMILES
product_smiles = dm.to_smiles(product)
```

* *批量反应应用**：
```python
# Apply reaction to library
products = []
for mol in reactant_mols:
    try:
        prod = dm.reactions.apply_reaction(rxn, (mol,))
        if prod is not None:
            products.append(prod)
    except Exception as e:
        print(f"Reaction failed: {e}")
```

## 并行化

Datamol 包括许多操作的内置并行化。使用 `n_jobs` 参数：
- `n_jobs=1`：顺序（无并行化）
- `n_jobs=-1`：使用所有可用的 CPU 内核
- `n_jobs=4`：使用 4 个内核

* *支持并行化的函数**：
- `dm.read_sdf(..., n_jobs=-1)`
- `dm.descriptors.batch_compute_many_descriptors(..., n_jobs=-1)`
- `dm.cluster_mols(..., n_jobs=-1)`
- `dm.pdist(..., n_jobs=-1)`
- `dm.conformers.sasa(..., n_jobs=-1)`

* *进度条**：许多批处理操作支持`progress=True`参数。

## 常见工作流程和模式

### 完整管道：数据加载→过滤→分析

```python
import datamol as dm
import pandas as pd

# 1. Load molecules
df = dm.read_sdf("compounds.sdf")

# 2. Standardize
df['mol'] = df['mol'].apply(lambda m: dm.standardize_mol(m) if m else None)
df = df[df['mol'].notna()]  # Remove failed molecules

# 3. Compute descriptors
desc_df = dm.descriptors.batch_compute_many_descriptors(
    df['mol'].tolist(),
    n_jobs=-1,
    progress=True
)

# 4. Filter by drug-likeness
druglike = (
    (desc_df['mw'] <= 500) &
    (desc_df['logp'] <= 5) &
    (desc_df['hbd'] <= 5) &
    (desc_df['hba'] <= 10)
)
filtered_df = df[druglike]

# 5. Cluster and select diverse subset
diverse_mols = dm.pick_diverse(
    filtered_df['mol'].tolist(),
    npick=100
)

# 6. Visualize results
dm.viz.to_image(
    diverse_mols,
    legends=[dm.to_smiles(m) for m in diverse_mols],
    outfile="diverse_compounds.png",
    n_cols=10
)
```

### 结构-活性关系（SAR）分析

```python
# Group by scaffold
scaffolds = [dm.to_scaffold_murcko(mol) for mol in mols]
scaffold_smiles = [dm.to_smiles(s) for s in scaffolds]

# Create DataFrame with activities
sar_df = pd.DataFrame({
    'mol': mols,
    'scaffold': scaffold_smiles,
    'activity': activities  # User-provided activity data
})

# Analyze each scaffold series
for scaffold, group in sar_df.groupby('scaffold'):
    if len(group) >= 3:  # Need multiple examples
        print(f"\nScaffold: {scaffold}")
        print(f"Count: {len(group)}")
        print(f"Activity range: {group['activity'].min():.2f} - {group['activity'].max():.2f}")

        # Visualize with activities as legends
        dm.viz.to_image(
            group['mol'].tolist(),
            legends=[f"Activity: {act:.2f}" for act in group['activity']],
            align=True  # Align by common substructure
        )
```

### 虚拟筛选管道

```python
# 1. Generate fingerprints for query and library
query_fps = [dm.to_fp(mol) for mol in query_actives]
library_fps = [dm.to_fp(mol) for mol in library_mols]

# 2. Calculate similarities
from scipy.spatial.distance import cdist
import numpy as np

distances = dm.cdist(query_actives, library_mols, n_jobs=-1)

# 3. Find closest matches (min distance to any query)
min_distances = distances.min(axis=0)
similarities = 1 - min_distances  # Convert distance to similarity

# 4. Rank and select top hits
top_indices = np.argsort(similarities)[::-1][:100]  # Top 100
top_hits = [library_mols[i] for i in top_indices]
top_scores = [similarities[i] for i in top_indices]

# 5. Visualize hits
dm.viz.to_image(
    top_hits[:20],
    legends=[f"Sim: {score:.3f}" for score in top_scores[:20]],
    outfile="screening_hits.png"
)
```

## 参考文档

有关详细的API文档，请查阅这些参考文件：

- **`references/core_api.md`**：核心命名空间函数（转换，标准化、指纹图谱、聚类）
- **`references/io_module.md`**：文件 I/O 操作（读/写 SDF、CSV、Excel、远程文件）
- **`references/conformers_module.md`**：3D 构象异构体生成、聚类、SASA 计算
- **`references/descriptors_viz.md`**：分子描述符和可视化功能
- **`references/fragments_scaffolds.md`**：支架提取，BRICS/RECAP碎片
- **`references/reactions_data.md`**：化学反应和玩具数据集

## 最佳实践

1. **始终从外部来源标准化分子**：
 ```python
 mol = dm.standardize_mol(mol, disconnect_metals=True, normalize=True, reionize=True)
 ```

2. **分子解析后检查 None 值**：
 ```python
 mol = dm.to_mol(smiles)
 if mol is None:
 # 处理无效的 SMILES
```

3. **对大型数据集使用并行处理**：
 ```python
 result = dm.operation(..., n_jobs=-1, Progress=True)
 ```

4. **利用 fsspec** 进行云存储：
 ```python
 df = dm.read_sdf("s3://bucket/compounds.sdf")
 ```

5. **使用适当的指纹**进行​​相似性：
  - ECFP (Morgan)：通用，结构相似性
  - MACCS：快速、较小的特征空间
  - 原子对：考虑原子对和距离

6. **考虑规模限制**：
  - Butina 聚类：~1,000 个分子（全距离矩阵）
  - 对于较大的数据集：使用多样性选择或分层方法

7. **ML 的脚手架拆分**：通过脚手架 

8 确保正确的训练/测试分离。 **可视化 SAR 系列时对齐分子**

## 错误处理

```python
# Safe molecule creation
def safe_to_mol(smiles):
    try:
        mol = dm.to_mol(smiles)
        if mol is not None:
            mol = dm.standardize_mol(mol)
        return mol
    except Exception as e:
        print(f"Failed to process {smiles}: {e}")
        return None

# Safe batch processing
valid_mols = []
for smiles in smiles_list:
    mol = safe_to_mol(smiles)
    if mol is not None:
        valid_mols.append(mol)
```

## 与机器学习集成

```python
# Feature generation
X = np.array([dm.to_fp(mol) for mol in mols])

# Or descriptors
desc_df = dm.descriptors.batch_compute_many_descriptors(mols, n_jobs=-1)
X = desc_df.values

# Train model
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(X, y_target)

# Predict
predictions = model.predict(X_test)
```

## 故障排除

* *问题**：分子解析失败
- **解决方案**：首先使用 `dm.standardize_smiles()` 或尝试 `dm.fix_mol()`

  * *问题**：聚类内存错误
- **解决方案**：使用 `dm.pick_diverse()` 而不是大型集合的完整聚类

  * *问题**：一致异构体生成缓慢
- **解决方案**：减少`n_confs` 或增加 `rms_cutoff` 以生成更少的一致性

* *问题**：远程文件访问失败
- **解决方案**：确保安装了 fsspec 和适当的云提供商库（s3fs、gcsfs 等）

## 其他资源

- **Datamol 文档**：https://docs.datamol.io/
- **RDKit 文档**：https://www.rdkit.org/docs/
- **GitHub 存储库**：https://github.com/datamol-io/datamol
