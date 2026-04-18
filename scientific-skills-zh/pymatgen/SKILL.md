---
name: pymatgen
description: 材料科学工具包。晶体结构（CIF、POSCAR）、相图、能带结构、DOS、材料项目集成、格式转换，用于计算材料科学。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Pymatgen - Python 材料基因组学

## 概述

Pymatgen 是一个用于材料分析的综合 Python 库，为材料项目提供支持。创建、分析和操纵晶体结构和分子，计算相图和热力学性质，分析电子结构（能带结构，DOS），生成表面和界面，并访问材料项目的计算材料数据库。支持来自各种计算代码的 100 多种文件格式。

## 何时使用此技能

此技能应在以下情况下使用：
- 在材料科学中处理晶体结构或分子系统
- 在结构文件格式（CIF、POSCAR、XYZ 等）之间进行转换
- 分析对称性、空间群或配位环境
- 计算相图或评估热力学稳定性
- 分析电子结构数据（带隙、DOS、能带结构）
- 生成表面、板或研究界面
- 以编程方式访问材料项目数据库
- 设置高通量计算工作流程
- 分析扩散、磁性或机械特性
- 使用 VASP、高斯、量子 ESPRESSO 或其他计算代码

## 快速入门指南

### 安装

```bash
# Core pymatgen
uv pip install pymatgen

# With Materials Project API access
uv pip install pymatgen mp-api

# Optional dependencies for extended functionality
uv pip install pymatgen[analysis]  # Additional analysis tools
uv pip install pymatgen[vis]       # Visualization tools
```

### 基本结构操作

```python
from pymatgen.core import Structure, Lattice

# Read structure from file (automatic format detection)
struct = Structure.from_file("POSCAR")

# Create structure from scratch
lattice = Lattice.cubic(3.84)
struct = Structure(lattice, ["Si", "Si"], [[0,0,0], [0.25,0.25,0.25]])

# Write to different format
struct.to(filename="structure.cif")

# Basic properties
print(f"Formula: {struct.composition.reduced_formula}")
print(f"Space group: {struct.get_space_group_info()}")
print(f"Density: {struct.density:.2f} g/cm³")
```

### 材料项目集成

```bash
# Set up API key
export MP_API_KEY="your_api_key_here"
```

```python
from mp_api.client import MPRester

with MPRester() as mpr:
    # Get structure by material ID
    struct = mpr.get_structure_by_material_id("mp-149")

    # Search for materials
    materials = mpr.materials.summary.search(
        formula="Fe2O3",
        energy_above_hull=(0, 0.05)
    )
```

## 核心功能

### 1. 结构创建和操作

使用各种方法和方法创建结构执行转换。

* *来自文件：**
```python
# Automatic format detection
struct = Structure.from_file("structure.cif")
struct = Structure.from_file("POSCAR")
mol = Molecule.from_file("molecule.xyz")
```

* *从头开始：**
```python
from pymatgen.core import Structure, Lattice

# Using lattice parameters
lattice = Lattice.from_parameters(a=3.84, b=3.84, c=3.84,
                                  alpha=120, beta=90, gamma=60)
coords = [[0, 0, 0], [0.75, 0.5, 0.75]]
struct = Structure(lattice, ["Si", "Si"], coords)

# From space group
struct = Structure.from_spacegroup(
    "Fm-3m",
    Lattice.cubic(3.5),
    ["Si"],
    [[0, 0, 0]]
)
```

* *转换：**
```python
from pymatgen.transformations.standard_transformations import (
    SupercellTransformation,
    SubstitutionTransformation,
    PrimitiveCellTransformation
)

# Create supercell
trans = SupercellTransformation([[2,0,0],[0,2,0],[0,0,2]])
supercell = trans.apply_transformation(struct)

# Substitute elements
trans = SubstitutionTransformation({"Fe": "Mn"})
new_struct = trans.apply_transformation(struct)

# Get primitive cell
trans = PrimitiveCellTransformation()
primitive = trans.apply_transformation(struct)
```

* *参考：**参见`references/core_classes.md` 用于结构、晶格、分子和相关类的综合文档。

### 2. 文件格式转换

通过自动格式检测在 100 多种文件格式之间进行转换。

* *使用便捷方法：**
```python
# Read any format
struct = Structure.from_file("input_file")

# Write to any format
struct.to(filename="output.cif")
struct.to(filename="POSCAR")
struct.to(filename="output.xyz")
```

* *使用转换脚本：**
```bash
# Single file conversion
python scripts/structure_converter.py POSCAR structure.cif

# Batch conversion
python scripts/structure_converter.py *.cif --output-dir ./poscar_files --format poscar
```

* *参考：**有关所有支持的格式和代码的详细文档，请参阅 `references/io_formats.md` Integrations.

### 3. 结构分析和对称性

分析结构的对称性、配位性和其他属性。

* *对称性分析：**
```python
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

sga = SpacegroupAnalyzer(struct)

# Get space group information
print(f"Space group: {sga.get_space_group_symbol()}")
print(f"Number: {sga.get_space_group_number()}")
print(f"Crystal system: {sga.get_crystal_system()}")

# Get conventional/primitive cells
conventional = sga.get_conventional_standard_structure()
primitive = sga.get_primitive_standard_structure()
```

* *配位环境：**
```python
from pymatgen.analysis.local_env import CrystalNN

cnn = CrystalNN()
neighbors = cnn.get_nn_info(struct, n=0)  # Neighbors of site 0

print(f"Coordination number: {len(neighbors)}")
for neighbor in neighbors:
    site = struct[neighbor['site_index']]
    print(f"  {site.species_string} at {neighbor['weight']:.3f} Å")
```

* *使用分析脚本：**
```bash
# Comprehensive analysis
python scripts/structure_analyzer.py POSCAR --symmetry --neighbors

# Export results
python scripts/structure_analyzer.py structure.cif --symmetry --export json
```

* *参考：**有关所有分析功能的详细文档，请参阅 `references/analysis_modules.md`。

### 4. 相图和热力学

构建相图并分析热力学稳定性。

* *相图构建：**
```python
from mp_api.client import MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter

# Get entries from Materials Project
with MPRester() as mpr:
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")

# Build phase diagram
pd = PhaseDiagram(entries)

# Check stability
from pymatgen.core import Composition
comp = Composition("LiFeO2")

# Find entry for composition
for entry in entries:
    if entry.composition.reduced_formula == comp.reduced_formula:
        e_above_hull = pd.get_e_above_hull(entry)
        print(f"Energy above hull: {e_above_hull:.4f} eV/atom")

        if e_above_hull > 0.001:
            # Get decomposition
            decomp = pd.get_decomposition(comp)
            print("Decomposes to:", decomp)

# Plot
plotter = PDPlotter(pd)
plotter.show()
```

* *使用相图脚本：**
```bash
# Generate phase diagram
python scripts/phase_diagram_generator.py Li-Fe-O --output li_fe_o.png

# Analyze specific composition
python scripts/phase_diagram_generator.py Li-Fe-O --analyze "LiFeO2" --show
```

* *参考：**参见`references/analysis_modules.md`（相图部分）和 `references/transformations_workflows.md`（工作流程 2）了解详细示例。

### 5. 电子结构分析

分析能带结构、态密度和电子特性。

* *能带结构：**
```python
from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import BSPlotter

# Read from VASP calculation
vasprun = Vasprun("vasprun.xml")
bs = vasprun.get_band_structure()

# Analyze
band_gap = bs.get_band_gap()
print(f"Band gap: {band_gap['energy']:.3f} eV")
print(f"Direct: {band_gap['direct']}")
print(f"Is metal: {bs.is_metal()}")

# Plot
plotter = BSPlotter(bs)
plotter.save_plot("band_structure.png")
```

* *态密度：**
```python
from pymatgen.electronic_structure.plotter import DosPlotter

dos = vasprun.complete_dos

# Get element-projected DOS
element_dos = dos.get_element_dos()
for element, element_dos_obj in element_dos.items():
    print(f"{element}: {element_dos_obj.get_gap():.3f} eV")

# Plot
plotter = DosPlotter()
plotter.add_dos("Total DOS", dos)
plotter.show()
```

* *参考：**参见`references/analysis_modules.md`（电子结构部分）和`references/io_formats.md`（VASP部分）。

### 6. 表面和界面分析

生成板，分析表面并研究界面。

* *板生成：**
```python
from pymatgen.core.surface import SlabGenerator

# Generate slabs for specific Miller index
slabgen = SlabGenerator(
    struct,
    miller_index=(1, 1, 1),
    min_slab_size=10.0,      # Å
    min_vacuum_size=10.0,    # Å
    center_slab=True
)

slabs = slabgen.get_slabs()

# Write slabs
for i, slab in enumerate(slabs):
    slab.to(filename=f"slab_{i}.cif")
```

* *Wulff形状构造：**
```python
from pymatgen.analysis.wulff import WulffShape

# Define surface energies
surface_energies = {
    (1, 0, 0): 1.0,
    (1, 1, 0): 1.1,
    (1, 1, 1): 0.9,
}

wulff = WulffShape(struct.lattice, surface_energies)
print(f"Surface area: {wulff.surface_area:.2f} Ų")
print(f"Volume: {wulff.volume:.2f} ų")

wulff.show()
```

* *吸附位点发现：**
```python
from pymatgen.analysis.adsorption import AdsorbateSiteFinder
from pymatgen.core import Molecule

asf = AdsorbateSiteFinder(slab)

# Find sites
ads_sites = asf.find_adsorption_sites()
print(f"On-top sites: {len(ads_sites['ontop'])}")
print(f"Bridge sites: {len(ads_sites['bridge'])}")
print(f"Hollow sites: {len(ads_sites['hollow'])}")

# Add adsorbate
adsorbate = Molecule("O", [[0, 0, 0]])
ads_struct = asf.add_adsorbate(adsorbate, ads_sites["ontop"][0])
```

* *参考：**参见`references/analysis_modules.md`（表面和界面部分）和`references/transformations_workflows.md`（工作流程3和9）。

### 7.材料项目数据库访问

以编程方式访问材料项目数据库.

* *设置：**
1. 从 https://next-gen.materialsproject.org/
2 获取 API 密钥。设置环境变量：`export MP_API_KEY="your_key_here"`

* *搜索并检索：**
```python
from mp_api.client import MPRester

with MPRester() as mpr:
    # Search by formula
    materials = mpr.materials.summary.search(formula="Fe2O3")

    # Search by chemical system
    materials = mpr.materials.summary.search(chemsys="Li-Fe-O")

    # Filter by properties
    materials = mpr.materials.summary.search(
        chemsys="Li-Fe-O",
        energy_above_hull=(0, 0.05),  # Stable/metastable
        band_gap=(1.0, 3.0)            # Semiconducting
    )

    # Get structure
    struct = mpr.get_structure_by_material_id("mp-149")

    # Get band structure
    bs = mpr.get_bandstructure_by_material_id("mp-149")

    # Get entries for phase diagram
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")
```

* *参考：**参见`references/materials_project_api.md`了解全面的API文档和示例。

### 8.计算工作流程设置

设置各种电子结构代码的计算。

* *VASP输入生成：**
```python
from pymatgen.io.vasp.sets import MPRelaxSet, MPStaticSet, MPNonSCFSet

# Relaxation
relax = MPRelaxSet(struct)
relax.write_input("./relax_calc")

# Static calculation
static = MPStaticSet(struct)
static.write_input("./static_calc")

# Band structure (non-self-consistent)
nscf = MPNonSCFSet(struct, mode="line")
nscf.write_input("./bandstructure_calc")

# Custom parameters
custom = MPRelaxSet(struct, user_incar_settings={"ENCUT": 600})
custom.write_input("./custom_calc")
```

* *其他代码：**
```python
# Gaussian
from pymatgen.io.gaussian import GaussianInput

gin = GaussianInput(
    mol,
    functional="B3LYP",
    basis_set="6-31G(d)",
    route_parameters={"Opt": None}
)
gin.write_file("input.gjf")

# Quantum ESPRESSO
from pymatgen.io.pwscf import PWInput

pwin = PWInput(struct, control={"calculation": "scf"})
pwin.write_file("pw.in")
```

* *参考：**参见`references/io_formats.md`（电子结构代码I/O部分）和`references/transformations_workflows.md`工作流程示例。

### 9. 高级分析

* *衍射图案：**
```python
from pymatgen.analysis.diffraction.xrd import XRDCalculator

xrd = XRDCalculator()
pattern = xrd.get_pattern(struct)

# Get peaks
for peak in pattern.hkls:
    print(f"2θ = {peak['2theta']:.2f}°, hkl = {peak['hkl']}")

pattern.plot()
```

* *弹性性能：**
```python
from pymatgen.analysis.elasticity import ElasticTensor

# From elastic tensor matrix
elastic_tensor = ElasticTensor.from_voigt(matrix)

print(f"Bulk modulus: {elastic_tensor.k_voigt:.1f} GPa")
print(f"Shear modulus: {elastic_tensor.g_voigt:.1f} GPa")
print(f"Young's modulus: {elastic_tensor.y_mod:.1f} GPa")
```

* *磁性订购：**
```python
from pymatgen.transformations.advanced_transformations import MagOrderingTransformation

# Enumerate magnetic orderings
trans = MagOrderingTransformation({"Fe": 5.0})
mag_structs = trans.apply_transformation(struct, return_ranked_list=True)

# Get lowest energy magnetic structure
lowest_energy_struct = mag_structs[0]['structure']
```

* *参考：**参见`references/analysis_modules.md`综合分析模块文档。

## 捆绑资源

### 脚本(`scripts/`)

常见的可执行Python脚本任务：

- **`structure_converter.py`**：结构文件格式之间的转换
  - 支持批量转换和自动格式检测
  - 用法：`python scripts/structure_converter.py POSCAR structure.cif`

- **`structure_analyzer.py`**：全面的结构分析
  - 对称性、协调性、晶格参数、距离矩阵
  - 用法：`python scripts/structure_analyzer.py structure.cif --symmetry --neighbors`

- **`phase_diagram_generator.py`**：从Materials Project生成相图
  - 稳定性分析和热力学性质
  - 用法：`python scripts/phase_diagram_generator.py Li-Fe-O --analyze "LiFeO2"`

所有脚本都包含详细帮助： `python scripts/script_name.py --help`

### 参考文献 (`references/`)

根据需要加载到上下文中的综合文档：

- **`core_classes.md`**：元素、结构、晶格、分子、组合类
- **`io_formats.md`**：文件格式支持和代码集成（VASP、高斯等）
- **`analysis_modules.md`**：相图、表面、电子结构、对称性
- **`materials_project_api.md`**：完整材料项目 API 指南
- **`transformations_workflows.md`**：转换框架和通用工作流程

 当需要有关特定模块或工作流程的详细信息时加载参考。

## 常用工作流程

### 高通量结构生成

```python
from pymatgen.transformations.standard_transformations import SubstitutionTransformation
from pymatgen.io.vasp.sets import MPRelaxSet

# Generate doped structures
base_struct = Structure.from_file("POSCAR")
dopants = ["Mn", "Co", "Ni", "Cu"]

for dopant in dopants:
    trans = SubstitutionTransformation({"Fe": dopant})
    doped_struct = trans.apply_transformation(base_struct)

    # Generate VASP inputs
    vasp_input = MPRelaxSet(doped_struct)
    vasp_input.write_input(f"./calcs/Fe_{dopant}")
```

### 能带结构计算工作流程

```python
# 1. Relaxation
relax = MPRelaxSet(struct)
relax.write_input("./1_relax")

# 2. Static (after relaxation)
relaxed = Structure.from_file("1_relax/CONTCAR")
static = MPStaticSet(relaxed)
static.write_input("./2_static")

# 3. Band structure (non-self-consistent)
nscf = MPNonSCFSet(relaxed, mode="line")
nscf.write_input("./3_bandstructure")

# 4. Analysis
from pymatgen.io.vasp import Vasprun
vasprun = Vasprun("3_bandstructure/vasprun.xml")
bs = vasprun.get_band_structure()
bs.get_band_gap()
```

### 表面能计算

```python
# 1. Get bulk energy
bulk_vasprun = Vasprun("bulk/vasprun.xml")
bulk_E_per_atom = bulk_vasprun.final_energy / len(bulk)

# 2. Generate and calculate slabs
slabgen = SlabGenerator(bulk, (1,1,1), 10, 15)
slab = slabgen.get_slabs()[0]

MPRelaxSet(slab).write_input("./slab_calc")

# 3. Calculate surface energy (after calculation)
slab_vasprun = Vasprun("slab_calc/vasprun.xml")
E_surf = (slab_vasprun.final_energy - len(slab) * bulk_E_per_atom) / (2 * slab.surface_area)
E_surf *= 16.021766  # Convert eV/Ų to J/m²
```

* *更多工作流程：**请参阅`references/transformations_workflows.md`了解10个详细的工作流程示例。

## 最佳实践

### 结构处理

1. **使用自动格式检测**：`Structure.from_file()` 可处理大多数格式
2. **首选不可变结构**：当结构不应更改时使用 `IStructure`
3. **检查对称性**：使用 `SpacegroupAnalyzer` 还原为原始单元 
4. **验证结构**：检查重叠原子或不合理的键长

### 文件 I/O

1. **使用便捷方法**：`from_file()`和`to()`优先为
2. **明确指定格式**：自动检测失败时
3. **处理异常**：将文件 I/O 包装在 try- except 块中 
4. **使用序列化**：`as_dict()`/`from_dict()` 用于版本安全存储

### 材料项目 API

1. **使用上下文管理器**：始终使用 `with MPRester() as mpr:`
2. **批量查询**：一次请求多个项目
3. **缓存结果**：将常用数据保存在本地
4. **有效过滤**：使用属性过滤器减少数据传输

### 计算工作流程

1. **使用输入集**：优先使用 `MPRelaxSet`、`MPStaticSet`，而不是手动 INCAR
2. **检查收敛**：始终验证计算收敛
3. **跟踪转换**：使用 `TransformedStructure` 作为来源 
4. **组织计算**：使用清晰的目录结构

### 性能

1. **减少对称性**：尽可能使用原始细胞
2. **限制邻居搜索**：指定合理的截止半径
3. **使用适当的方法**：不同的分析工具具有不同的速度/精度权衡
4. **尽可能并行化**：许多操作可以并行化

## 单位和约定

Pymatgen 在全文中使用原子单位：
- **长度**：埃 (Å)
- **能量**：电子伏特 (eV)
- **角度**：度 (°)
- **磁矩**：玻尔磁子(μB)
- **时间**：飞秒 (fs)

 在需要时使用 `pymatgen.core.units` 转换单位。

## 与其他工具集成

Pymatgen 与：
- **ASE**（原子仿真环境）
- **Phonopy** 无缝集成（声子计算）
- **BoltzTraP**（输运属性）
- **Atomate/Fireworks**（工作流程管理）
- **AiiDA**（来源跟踪）
- **Zeo++**（孔隙分析）
- **OpenBabel**（分子）转换）

## 故障排除

* *导入错误**：安装缺少的依赖项
```bash
uv pip install pymatgen[analysis,vis]
```

* *找不到API密钥**：设置MP_API_KEY环境变量
```bash
export MP_API_KEY="your_key_here"
```

* *结构读取失败**：检查文件格式和语法
```python
# Try explicit format specification
struct = Structure.from_file("file.txt", fmt="cif")
```

* *对称分析失败**：结构可能存在数值精度问题
```python
# Increase tolerance
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
sga = SpacegroupAnalyzer(struct, symprec=0.1)
```

## 其他资源

- **文档**：https://pymatgen.org/
- **材料项目**： https://materialsproject.org/
- **GitHub**：https://github.com/materialsproject/pymatgen
- **论坛**：https://matsci.org/
- **示例笔记本**：https://matgenb.materialsvirtuallab.org/

## 版本说明

此技能专为pymatgen 2024.x 及更高版本。对于材料项目 API，请使用 `mp-api` 包（与旧版 `pymatgen.ext.matproj` 分开）。

 要求：
- Python 3.10 或更高版本
- pymatgen >= 2023.x
- mp-api（用于材料项目）接入）
