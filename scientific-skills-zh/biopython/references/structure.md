# 使用 Bio.PDB

进行结构生物信息学## 概述

Bio.PDB 提供了用于处理来自 PDB 和 mmCIF 文件的大分子 3D 结构的工具。该模块使用SMCRA（Structure/Model/Chain/Residue/Atom）架构来分层表示蛋白质结构。

## SMCRA Architecture

Bio.PDB模块分层组织结构：

```
Structure
  └── Model       (multiple models for NMR structures)
      └── Chain   (e.g., chain A, B, C)
          └── Residue  (amino acids, nucleotides, heteroatoms)
              └── Atom (individual atoms)
```

## 解析结构文件

### PDB格式

```python
from Bio.PDB import PDBParser

# Create parser
parser = PDBParser(QUIET=True)  # QUIET=True suppresses warnings

# Parse structure
structure = parser.get_structure("1crn", "1crn.pdb")

# Access basic information
print(f"Structure ID: {structure.id}")
print(f"Number of models: {len(structure)}")
```

### mmCIF 格式

mmCIF 格式更现代，可以更好地处理大型结构：

```python
from Bio.PDB import MMCIFParser

# Create parser
parser = MMCIFParser(QUIET=True)

# Parse structure
structure = parser.get_structure("1crn", "1crn.cif")
```

### 从 PDB 下载

```python
from Bio.PDB import PDBList

# Create PDB list object
pdbl = PDBList()

# Download PDB file
pdbl.retrieve_pdb_file("1CRN", file_format="pdb", pdir="structures/")

# Download mmCIF file
pdbl.retrieve_pdb_file("1CRN", file_format="mmCif", pdir="structures/")

# Download obsolete structure
pdbl.retrieve_pdb_file("1CRN", obsolete=True, pdir="structures/")
```

## 导航结构层次

### 访问模型

```python
# Get first model
model = structure[0]

# Iterate through all models
for model in structure:
    print(f"Model {model.id}")
```

### 访问链

```python
# Get specific chain
chain = model["A"]

# Iterate through all chains
for chain in model:
    print(f"Chain {chain.id}")
```

### 访问残基

```python
# Iterate through residues in a chain
for residue in chain:
    print(f"Residue: {residue.resname} {residue.id[1]}")

# Get specific residue by ID
# Residue ID is tuple: (hetfield, sequence_id, insertion_code)
residue = chain[(" ", 10, " ")]  # Standard amino acid at position 10
```

### 访问原子

```python
# Iterate through atoms in a residue
for atom in residue:
    print(f"Atom: {atom.name}, Coordinates: {atom.coord}")

# Get specific atom
ca_atom = residue["CA"]  # Alpha carbon
print(f"CA coordinates: {ca_atom.coord}")
```

### 替代访问模式

```python
# Direct access through hierarchy
atom = structure[0]["A"][10]["CA"]

# Get all atoms
atoms = list(structure.get_atoms())
print(f"Total atoms: {len(atoms)}")

# Get all residues
residues = list(structure.get_residues())

# Get all chains
chains = list(structure.get_chains())
```

## 使用原子坐标

### 访问坐标

```python
# Get atom coordinates
coord = atom.coord
print(f"X: {coord[0]}, Y: {coord[1]}, Z: {coord[2]}")

# Get B-factor (temperature factor)
b_factor = atom.bfactor

# Get occupancy
occupancy = atom.occupancy

# Get element
element = atom.element
```

### 计算距离

```python
from Bio.PDB import Vector

# Calculate distance between two atoms
atom1 = residue1["CA"]
atom2 = residue2["CA"]

distance = atom1 - atom2  # Returns distance in Angstroms
print(f"Distance: {distance:.2f} Å")
```

### 计算角度

```python
from Bio.PDB.vectors import calc_angle

# Calculate angle between three atoms
angle = calc_angle(
    atom1.get_vector(),
    atom2.get_vector(),
    atom3.get_vector()
)
print(f"Angle: {angle:.2f} radians")
```

### 计算二面角

```python
from Bio.PDB.vectors import calc_dihedral

# Calculate dihedral angle between four atoms
dihedral = calc_dihedral(
    atom1.get_vector(),
    atom2.get_vector(),
    atom3.get_vector(),
    atom4.get_vector()
)
print(f"Dihedral: {dihedral:.2f} radians")
```

## 结构分析

### 二级结构(DSSP)

DSSP 将二级结构分配给蛋白质结构：

```python
from Bio.PDB import DSSP, PDBParser

# Parse structure
parser = PDBParser()
structure = parser.get_structure("1crn", "1crn.pdb")

# Run DSSP (requires DSSP executable installed)
model = structure[0]
dssp = DSSP(model, "1crn.pdb")

# Access results
for residue_key in dssp:
    dssp_data = dssp[residue_key]
    residue_id = residue_key[1]
    ss = dssp_data[2]  # Secondary structure code
    phi = dssp_data[4]  # Phi angle
    psi = dssp_data[5]  # Psi angle
    print(f"Residue {residue_id}: {ss}, φ={phi:.1f}°, ψ={psi:.1f}°")
```

 二级结构代码：
- `H` - Alpha 螺旋
- `B` - Beta 桥
- `E` - 绞线
- `G` - 3-10螺旋
- `I` - Pi螺旋
- `T` - 转弯
- `S` - 弯曲
- `-` - 线圈/环

### 溶剂可及性 (DSSP)

```python
# Get relative solvent accessibility
for residue_key in dssp:
    acc = dssp[residue_key][3]  # Relative accessibility
    print(f"Residue {residue_key[1]}: {acc:.2f} relative accessibility")
```

### 邻居搜索

有效查找附近的原子：

```python
from Bio.PDB import NeighborSearch

# Get all atoms
atoms = list(structure.get_atoms())

# Create neighbor search object
ns = NeighborSearch(atoms)

# Find atoms within radius
center_atom = structure[0]["A"][10]["CA"]
nearby_atoms = ns.search(center_atom.coord, 5.0)  # 5 Å radius
print(f"Found {len(nearby_atoms)} atoms within 5 Å")

# Find residues within radius
nearby_residues = ns.search(center_atom.coord, 5.0, level="R")

# Find chains within radius
nearby_chains = ns.search(center_atom.coord, 10.0, level="C")
```

### 地图

```python
def calculate_contact_map(chain, distance_threshold=8.0):
    """Calculate residue-residue contact map."""
    residues = list(chain.get_residues())
    n = len(residues)
    contact_map = [[0] * n for _ in range(n)]

    for i, res1 in enumerate(residues):
        for j, res2 in enumerate(residues):
            if i < j:
                # Get CA atoms
                if res1.has_id("CA") and res2.has_id("CA"):
                    dist = res1["CA"] - res2["CA"]
                    if dist < distance_threshold:
                        contact_map[i][j] = 1
                        contact_map[j][i] = 1

    return contact_map
```

## 结构质量评估

### Ramachandran 绘图数据

```python
from Bio.PDB import Polypeptide

def get_phi_psi(structure):
    """Extract phi and psi angles for Ramachandran plot."""
    phi_psi = []

    for model in structure:
        for chain in model:
            polypeptides = Polypeptide.PPBuilder().build_peptides(chain)
            for poly in polypeptides:
                angles = poly.get_phi_psi_list()
                for residue, (phi, psi) in zip(poly, angles):
                    if phi and psi:  # Skip None values
                        phi_psi.append((residue.resname, phi, psi))

    return phi_psi
```

### 检查缺失原子

```python
def check_missing_atoms(structure):
    """Identify residues with missing atoms."""
    missing = []

    for residue in structure.get_residues():
        if residue.id[0] == " ":  # Standard amino acid
            resname = residue.resname

            # Expected backbone atoms
            expected = ["N", "CA", "C", "O"]

            for atom_name in expected:
                if not residue.has_id(atom_name):
                    missing.append((residue.full_id, atom_name))

    return missing
```

## 结构操作

### 选择特定原子

```python
from Bio.PDB import Select

class CASelect(Select):
    """Select only CA atoms."""
    def accept_atom(self, atom):
        return atom.name == "CA"

class ChainASelect(Select):
    """Select only chain A."""
    def accept_chain(self, chain):
        return chain.id == "A"

# Use with PDBIO
from Bio.PDB import PDBIO

io = PDBIO()
io.set_structure(structure)
io.save("ca_only.pdb", CASelect())
io.save("chain_a.pdb", ChainASelect())
```

### 变换结构

```python
import numpy as np

# Rotate structure
from Bio.PDB.vectors import rotaxis

# Define rotation axis and angle
axis = Vector(1, 0, 0)  # X-axis
angle = np.pi / 4  # 45 degrees

# Create rotation matrix
rotation = rotaxis(angle, axis)

# Apply rotation to all atoms
for atom in structure.get_atoms():
    atom.transform(rotation, Vector(0, 0, 0))
```

### 叠加结构

```python
from Bio.PDB import Superimposer, PDBParser

# Parse two structures
parser = PDBParser()
structure1 = parser.get_structure("ref", "reference.pdb")
structure2 = parser.get_structure("mov", "mobile.pdb")

# Get CA atoms from both structures
ref_atoms = [atom for atom in structure1.get_atoms() if atom.name == "CA"]
mov_atoms = [atom for atom in structure2.get_atoms() if atom.name == "CA"]

# Superimpose
super_imposer = Superimposer()
super_imposer.set_atoms(ref_atoms, mov_atoms)

# Apply transformation
super_imposer.apply(structure2.get_atoms())

# Get RMSD
rmsd = super_imposer.rms
print(f"RMSD: {rmsd:.2f} Å")

# Save superimposed structure
from Bio.PDB import PDBIO
io = PDBIO()
io.set_structure(structure2)
io.save("superimposed.pdb")
```

## 写入结构文件

### 保存PDB文件

```python
from Bio.PDB import PDBIO

io = PDBIO()
io.set_structure(structure)
io.save("output.pdb")
```

### 保存 mmCIF 文件

```python
from Bio.PDB import MMCIFIO

io = MMCIFIO()
io.set_structure(structure)
io.save("output.cif")
```

## 结构中的序列

### 提取序列

```python
from Bio.PDB import Polypeptide

# Get polypeptides from structure
ppb = Polypeptide.PPBuilder()

for model in structure:
    for chain in model:
        for pp in ppb.build_peptides(chain):
            sequence = pp.get_sequence()
            print(f"Chain {chain.id}: {sequence}")
```

### 映射到FASTA

```python
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

# Extract sequences and create FASTA
records = []
ppb = Polypeptide.PPBuilder()

for model in structure:
    for chain in model:
        for pp in ppb.build_peptides(chain):
            seq_record = SeqRecord(
                pp.get_sequence(),
                id=f"{structure.id}_{chain.id}",
                description=f"Chain {chain.id}"
            )
            records.append(seq_record)

SeqIO.write(records, "structure_sequences.fasta", "fasta")
```

## 最佳实践

1. **对大型结构和现代数据使用 mmCIF**
2. **设置 QUIET=True** 以抑制解析器警告
3. **分析前检查缺失的原子**
4. **使用 NeighborSearch** 进行高效的空间查询
5. **使用 DSSP 或 Ramachandran 分析
6 验证结构质量**。 **适当处理多个模型**（NMR 结构）
7. **注意杂原子** - 它们具有不同的残基 ID
8. **使用选择类**来输出目标结构
9. **本地缓存下载的结构**
10. **考虑替代构象** - 一些残基具有多个位置

## 常见用例

### 计算结构之间的RMSD

```python
from Bio.PDB import PDBParser, Superimposer

parser = PDBParser()
structure1 = parser.get_structure("s1", "structure1.pdb")
structure2 = parser.get_structure("s2", "structure2.pdb")

# Get CA atoms
atoms1 = [atom for atom in structure1[0]["A"].get_atoms() if atom.name == "CA"]
atoms2 = [atom for atom in structure2[0]["A"].get_atoms() if atom.name == "CA"]

# Ensure same number of atoms
min_len = min(len(atoms1), len(atoms2))
atoms1 = atoms1[:min_len]
atoms2 = atoms2[:min_len]

# Calculate RMSD
sup = Superimposer()
sup.set_atoms(atoms1, atoms2)
print(f"RMSD: {sup.rms:.3f} Å")
```

### 查找结合位点残基

```python
def find_binding_site(structure, ligand_chain, ligand_res_id, distance=5.0):
    """Find residues near a ligand."""
    from Bio.PDB import NeighborSearch

    # Get ligand atoms
    ligand = structure[0][ligand_chain][ligand_res_id]
    ligand_atoms = list(ligand.get_atoms())

    # Get all protein atoms
    protein_atoms = []
    for chain in structure[0]:
        if chain.id != ligand_chain:
            for residue in chain:
                if residue.id[0] == " ":  # Standard residue
                    protein_atoms.extend(residue.get_atoms())

    # Find nearby atoms
    ns = NeighborSearch(protein_atoms)
    binding_site = set()

    for ligand_atom in ligand_atoms:
        nearby = ns.search(ligand_atom.coord, distance, level="R")
        binding_site.update(nearby)

    return list(binding_site)
```

### 计算中心质量

```python
import numpy as np

def center_of_mass(entity):
    """Calculate center of mass for structure entity."""
    masses = []
    coords = []

    # Atomic masses (simplified)
    mass_dict = {"C": 12.0, "N": 14.0, "O": 16.0, "S": 32.0}

    for atom in entity.get_atoms():
        mass = mass_dict.get(atom.element, 12.0)
        masses.append(mass)
        coords.append(atom.coord)

    masses = np.array(masses)
    coords = np.array(coords)

    com = np.sum(coords * masses[:, np.newaxis], axis=0) / np.sum(masses)
    return com
```
