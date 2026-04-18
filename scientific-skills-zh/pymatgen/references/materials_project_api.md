# 材料项目 API 参考

此参考记录了如何通过 pymatgen 的 API 集成访问和使用材料项目数据库。

## 概述

材料项目是计算材料属性的综合数据库，包含数十万种无机晶体和分子的数据。 API 通过 `MPRester` 客户端提供对这些数据的编程访问。

## 安装和设置

Materials Project API 客户端现在位于单独的包中：

```bash
pip install mp-api
```

### 获取 API 密钥

1. 访问 https://next-gen.materialsproject.org/
2. 创建帐户或登录
3. 导航到您的仪表板/设置
4. 生成 API 密钥
5. 将其存储为环境变量：

```bash
export MP_API_KEY="your_api_key_here"
```

或添加到您的shell配置文件中（~/.bashrc、~/.zshrc等）

## 基本用法

### 初始化

```python
from mp_api.client import MPRester

# Using environment variable (recommended)
with MPRester() as mpr:
    # Perform queries
    pass

# Or explicitly pass API key
with MPRester("your_api_key_here") as mpr:
    # Perform queries
    pass
```

* *重要**：始终使用 `with` 上下文管理器以确保会话正确关闭。

## 查询材料数据

### 按公式搜索

```python
with MPRester() as mpr:
    # Get all materials with formula
    materials = mpr.materials.summary.search(formula="Fe2O3")

    for mat in materials:
        print(f"Material ID: {mat.material_id}")
        print(f"Formula: {mat.formula_pretty}")
        print(f"Energy above hull: {mat.energy_above_hull} eV/atom")
        print(f"Band gap: {mat.band_gap} eV")
        print()
```

### 按材料 ID 搜索

```python
with MPRester() as mpr:
    # Get specific material
    material = mpr.materials.summary.search(material_ids=["mp-149"])[0]

    print(f"Formula: {material.formula_pretty}")
    print(f"Space group: {material.symmetry.symbol}")
    print(f"Density: {material.density} g/cm³")
```

### 按化学搜索系统

```python
with MPRester() as mpr:
    # Get all materials in Fe-O system
    materials = mpr.materials.summary.search(chemsys="Fe-O")

    # Get materials in ternary system
    materials = mpr.materials.summary.search(chemsys="Li-Fe-O")
```

### 按元素搜索

```python
with MPRester() as mpr:
    # Materials containing Fe and O
    materials = mpr.materials.summary.search(elements=["Fe", "O"])

    # Materials containing ONLY Fe and O (excluding others)
    materials = mpr.materials.summary.search(
        elements=["Fe", "O"],
        exclude_elements=True
    )
```

## 获取结构

### 从材质ID

```python
with MPRester() as mpr:
    # Get structure
    structure = mpr.get_structure_by_material_id("mp-149")

    # Get multiple structures
    structures = mpr.get_structures(["mp-149", "mp-510", "mp-19017"])
```

### 所有结构公式

```python
with MPRester() as mpr:
    # Get all Fe2O3 structures
    materials = mpr.materials.summary.search(formula="Fe2O3")

    for mat in materials:
        structure = mpr.get_structure_by_material_id(mat.material_id)
        print(f"{mat.material_id}: {structure.get_space_group_info()}")
```

## 高级查询

### 属性过滤

```python
with MPRester() as mpr:
    # Materials with specific property ranges
    materials = mpr.materials.summary.search(
        chemsys="Li-Fe-O",
        energy_above_hull=(0, 0.05),  # Stable or near-stable
        band_gap=(1.0, 3.0),           # Semiconducting
    )

    # Magnetic materials
    materials = mpr.materials.summary.search(
        elements=["Fe"],
        is_magnetic=True
    )

    # Metals only
    materials = mpr.materials.summary.search(
        chemsys="Fe-Ni",
        is_metal=True
    )
```

### 排序和限制

```python
with MPRester() as mpr:
    # Get most stable materials
    materials = mpr.materials.summary.search(
        chemsys="Li-Fe-O",
        sort_fields=["energy_above_hull"],
        num_chunks=1,
        chunk_size=10  # Limit to 10 results
    )
```

## 电子结构数据

### 能带结构

```python
with MPRester() as mpr:
    # Get band structure
    bs = mpr.get_bandstructure_by_material_id("mp-149")

    # Analyze band structure
    if bs:
        print(f"Band gap: {bs.get_band_gap()}")
        print(f"Is metal: {bs.is_metal()}")
        print(f"Direct gap: {bs.get_band_gap()['direct']}")

        # Plot
        from pymatgen.electronic_structure.plotter import BSPlotter
        plotter = BSPlotter(bs)
        plotter.show()
```

### 态密度

```python
with MPRester() as mpr:
    # Get DOS
    dos = mpr.get_dos_by_material_id("mp-149")

    if dos:
        # Get band gap from DOS
        gap = dos.get_gap()
        print(f"Band gap from DOS: {gap} eV")

        # Plot DOS
        from pymatgen.electronic_structure.plotter import DosPlotter
        plotter = DosPlotter()
        plotter.add_dos("Total DOS", dos)
        plotter.show()
```

### 费米面

```python
with MPRester() as mpr:
    # Get electronic structure data for Fermi surface
    bs = mpr.get_bandstructure_by_material_id("mp-149", line_mode=False)
```

## 热力学数据

### 相图构造

```python
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter

with MPRester() as mpr:
    # Get entries for phase diagram
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")

    # Build phase diagram
    pd = PhaseDiagram(entries)

    # Plot
    plotter = PDPlotter(pd)
    plotter.show()
```

### 普贝图

```python
from pymatgen.analysis.pourbaix_diagram import PourbaixDiagram, PourbaixPlotter

with MPRester() as mpr:
    # Get entries for Pourbaix diagram
    entries = mpr.get_pourbaix_entries(["Fe"])

    # Build Pourbaix diagram
    pb = PourbaixDiagram(entries)

    # Plot
    plotter = PourbaixPlotter(pb)
    plotter.show()
```

### 形成能

```python
with MPRester() as mpr:
    materials = mpr.materials.summary.search(material_ids=["mp-149"])

    for mat in materials:
        print(f"Formation energy: {mat.formation_energy_per_atom} eV/atom")
        print(f"Energy above hull: {mat.energy_above_hull} eV/atom")
```

## 弹性和力学属性

```python
with MPRester() as mpr:
    # Search for materials with elastic data
    materials = mpr.materials.elasticity.search(
        chemsys="Fe-O",
        bulk_modulus_vrh=(100, 300)  # GPa
    )

    for mat in materials:
        print(f"{mat.material_id}: K = {mat.bulk_modulus_vrh} GPa")
```

## 介电属性

```python
with MPRester() as mpr:
    # Get dielectric data
    materials = mpr.materials.dielectric.search(
        material_ids=["mp-149"]
    )

    for mat in materials:
        print(f"Dielectric constant: {mat.e_electronic}")
        print(f"Refractive index: {mat.n}")
```

## 压电属性

```python
with MPRester() as mpr:
    # Get piezoelectric materials
    materials = mpr.materials.piezoelectric.search(
        piezoelectric_modulus=(1, 100)
    )
```

## 表面属性

```python
with MPRester() as mpr:
    # Get surface data
    surfaces = mpr.materials.surface_properties.search(
        material_ids=["mp-149"]
    )
```

## 分子数据（对于分子材料）

```python
with MPRester() as mpr:
    # Search molecules
    molecules = mpr.molecules.summary.search(
        formula="H2O"
    )

    for mol in molecules:
        print(f"Molecule ID: {mol.molecule_id}")
        print(f"Formula: {mol.formula_pretty}")
```

## 批量数据下载

### 下载材料的所有数据

```python
with MPRester() as mpr:
    # Get comprehensive data
    materials = mpr.materials.summary.search(
        material_ids=["mp-149"],
        fields=[
            "material_id",
            "formula_pretty",
            "structure",
            "energy_above_hull",
            "band_gap",
            "density",
            "symmetry",
            "elasticity",
            "magnetic_ordering"
        ]
    )
```

## 出处和计算详细信息

```python
with MPRester() as mpr:
    # Get calculation details
    materials = mpr.materials.summary.search(
        material_ids=["mp-149"],
        fields=["material_id", "origins"]
    )

    for mat in materials:
        print(f"Origins: {mat.origins}")
```

## 使用条目

### 热力学分析的计算条目

```python
with MPRester() as mpr:
    # Get entries (includes energy and composition)
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")

    # Entries can be used directly in phase diagram analysis
    from pymatgen.analysis.phase_diagram import PhaseDiagram
    pd = PhaseDiagram(entries)

    # Check stability
    for entry in entries[:5]:
        e_above_hull = pd.get_e_above_hull(entry)
        print(f"{entry.composition.reduced_formula}: {e_above_hull:.3f} eV/atom")
```

## 速率限制和最佳实践

### 速率限制

Materials Project API 具有速率限制，以确保合理使用：
- 注意请求频率
- 尽可能使用批量查询
- 在本地缓存结果以进行重复分析

### 高效查询

```python
# Bad: Multiple separate queries
with MPRester() as mpr:
    for mp_id in ["mp-149", "mp-510", "mp-19017"]:
        struct = mpr.get_structure_by_material_id(mp_id)  # 3 API calls

# Good: Single batch query
with MPRester() as mpr:
    structs = mpr.get_structures(["mp-149", "mp-510", "mp-19017"])  # 1 API call
```

### 缓存结果

```python
import json

# Save results for later use
with MPRester() as mpr:
    materials = mpr.materials.summary.search(chemsys="Li-Fe-O")

    # Save to file
    with open("li_fe_o_materials.json", "w") as f:
        json.dump([mat.dict() for mat in materials], f)

# Load cached results
with open("li_fe_o_materials.json", "r") as f:
    cached_data = json.load(f)
```

## 错误处理

```python
from mp_api.client.core.client import MPRestError

try:
    with MPRester() as mpr:
        materials = mpr.materials.summary.search(material_ids=["invalid-id"])
except MPRestError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 常见用例

### 寻找稳定化合物

```python
with MPRester() as mpr:
    # Get all stable compounds in a chemical system
    materials = mpr.materials.summary.search(
        chemsys="Li-Fe-O",
        energy_above_hull=(0, 0.001)  # Essentially on convex hull
    )

    print(f"Found {len(materials)} stable compounds")
    for mat in materials:
        print(f"  {mat.formula_pretty} ({mat.material_id})")
```

### 电池材料筛选

```python
with MPRester() as mpr:
    # Screen for potential cathode materials
    materials = mpr.materials.summary.search(
        elements=["Li"],  # Must contain Li
        energy_above_hull=(0, 0.05),  # Near stable
        band_gap=(0, 0.5),  # Metallic or small gap
    )

    print(f"Found {len(materials)} potential cathode materials")
```

### 寻找具有特定晶体结构的材料

```python
with MPRester() as mpr:
    # Find materials with specific space group
    materials = mpr.materials.summary.search(
        chemsys="Fe-O",
        spacegroup_number=167  # R-3c (corundum structure)
    )
```

## 与其他Pymatgen功能集成

从材料项目检索到的所有数据都可以直接用于pymatgen的分析工具：

```python
with MPRester() as mpr:
    # Get structure
    struct = mpr.get_structure_by_material_id("mp-149")

    # Use with pymatgen analysis
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    sga = SpacegroupAnalyzer(struct)

    # Generate surfaces
    from pymatgen.core.surface import SlabGenerator
    slabgen = SlabGenerator(struct, (1,0,0), 10, 10)
    slabs = slabgen.get_slabs()

    # Phase diagram analysis
    entries = mpr.get_entries_in_chemsys(struct.composition.chemical_system)
    from pymatgen.analysis.phase_diagram import PhaseDiagram
    pd = PhaseDiagram(entries)
```

## 其他资源

- **API 文档**：https://docs.materialsproject.org/
- **材料项目网站**：https://next-gen.materialsproject.org/
- **GitHub**： https://github.com/materialsproject/api
- **论坛**：https://matsci.org/

## 最佳实践摘要

1. **始终使用上下文管理器**：使用 `with MPRester() as mpr:`
2. **将 API 密钥存储为环境变量**：切勿对 API 密钥
3 进行硬编码。 **批量查询**：尽可能一次请求多个项目
4. **缓存结果**：将常用数据保存在本地
5. **处理错误**：将 API 调用包装在 try- except 块中 
6. **具体**：使用过滤器来限制结果并减少数据传输
7. **检查数据可用性**：并非所有材料的所有属性都可用
