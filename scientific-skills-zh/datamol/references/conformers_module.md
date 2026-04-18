# Datamol Conformers Module Reference

`datamol.conformers`模块提供用于生成和分析3D分子构象的工具。

## Conformer Generation

### `dm.conformers.generate(mol, n_confs=None, rms_cutoff=None, minimize_energy=True, method='ETKDGv3', add_hs=True, ...)`
生成3D分子构象。
- **参数**：
  - `mol`：输入分子
  - `n_confs`：要生成的构象异构体数量（如果没有，则根据可旋转键自动确定）
  - `rms_cutoff`：用于过滤相似构象异构体（删除重复项）的RMS阈值（以Ångströms为单位）
  - `minimize_energy`：应用 UFF 能量最小化（默认：True）
  - `method`：嵌入方法 - 选项：
  - `'ETDG'` - 实验扭转距离几何
  - `'ETKDG'` - ETDG 与附加基础知识
  - `'ETKDGv2'` - 增强版本 2
  - `'ETKDGv3'` - 增强版本 3（默认，推荐）
  - `add_hs`：嵌入前添加氢（默认：True，对质量至关重要）
  - `random_seed`：设置为重现性
- **返回**：具有嵌入构象异构体的分子
- **示例**：
 ```python
 mol = dm.to_mol("CCO")
 mol_3d = dm.conformers.generate(mol, n_confs=10, rms_cutoff=0.5)
 conformers = mol_3d.GetConformers() # 访问所有conformers
 ```

## Conformer Clustering

### `dm.conformers.cluster(mol, rms_cutoff=1.0, already_aligned=False, centroids=False)`
按RMS距离对conformer进行分组。
- **参数**：
  - `rms_cutoff`：以Ångströms为单位的聚类阈值（默认值：1.0）
  - `already_aligned`：构象异构体是否预对齐
  - `centroids`：返回质心构象异构体（True）或聚类组（False）
- **返回**：簇信息或质心构象
- **用例**：识别不同的构象家族

### `dm.conformers.return_centroids(mol, conf_clusters, centroids=True)`
从簇中提取代表性构象异构体。
- **参数**：
  - `conf_clusters`：`cluster()`
 中的簇索引序列 - `centroids`：返回单个分子（True）或分子列表（假）
- **返回**：质心构象异构体

## 构象分析

### `dm.conformers.rmsd(mol)`
计算所有构象异构体的成对RMSD矩阵。
- **要求**：至少2个构象异构体
- **返回**：NxN矩阵RMSD 值
- **用例**：量化构象异构体多样性

### `dm.conformers.sasa(mol, n_jobs=1, ...)`
使用 FreeSASA 计算溶剂可及表面积 (SASA)。
- **参数**：
  - `n_jobs`：多个并行化conformers
- **返回**：SASA 值数组（每个符合者一个）
- **存储**：作为属性存储在每个符合者中的值 `'rdkit_free_sasa'`
- **示例**：
 ```python
 sasa_values = dm.conformers.sasa(mol_3d)
 # 或者从conformer属性访问
conf = mol_3d.GetConformer(0)
 sasa = conf.GetDoubleProp('rdkit_free_sasa')
 ```

## 低级Conformer操作

### `dm.conformers.center_of_mass(mol, conf_id=-1, use_atoms=True, round_coord=None)`
计算分子中心。
- **参数**：
  - `conf_id`：构象指数（-1为第一构象）
  - `use_atoms`：使用原子质量（真）或几何中心（假）
  - `round_coord`：舍入的十进制精度
- **返回**：中心的3D坐标
- **用例**：居中分子以进行可视化或对齐

### `dm.conformers.get_coords(mol, conf_id=-1)`
从a中检索原子坐标conformer.
- **返回**：原子位置的 Nx3 numpy 数组
- **示例**：
 ```python
 位置 = dm.conformers.get_coords(mol_3d, conf_id=0)
 # Positions.shape: (num_atoms, 3)
```

### `dm.conformers.translate(mol, conf_id=-1, transform_matrix=None)`
使用变换矩阵重新定位构象异构体。
- **修改**：就地操作
- **用例**：对齐或重新定位分子

## 工作流程示例

```python
import datamol as dm

# 1. Create molecule and generate conformers
mol = dm.to_mol("CC(C)CCO")  # Isopentanol
mol_3d = dm.conformers.generate(
    mol,
    n_confs=50,           # Generate 50 initial conformers
    rms_cutoff=0.5,       # Filter similar conformers
    minimize_energy=True   # Minimize energy
)

# 2. Analyze conformers
n_conformers = mol_3d.GetNumConformers()
print(f"Generated {n_conformers} unique conformers")

# 3. Calculate SASA
sasa_values = dm.conformers.sasa(mol_3d)

# 4. Cluster conformers
clusters = dm.conformers.cluster(mol_3d, rms_cutoff=1.0, centroids=False)

# 5. Get representative conformers
centroids = dm.conformers.return_centroids(mol_3d, clusters)

# 6. Access 3D coordinates
coords = dm.conformers.get_coords(mol_3d, conf_id=0)
```

## 关键概念

- **距离几何**：根据连通性信息生成 3D 结构的方法
- **ETKDG**：使用实验扭转角偏好和其他化学知识
- **RMS 截止**：较低的值=更独特的构象异构体；较高的值 = 更少、更明显的构象异构体
- **能量最小化**：将结构松弛到最近的局部能量最小值
- **氢**：对于精确的 3D 几何形状至关重要 - 始终在嵌入过程中包含 
