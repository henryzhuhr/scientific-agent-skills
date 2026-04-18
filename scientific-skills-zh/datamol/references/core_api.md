# Datamol 核心 API 参考

本文档涵盖了 datamol 命名空间中可用的主要函数。

## 分子创建和转换

### `to_mol(mol, ...)`
将 SMILES 字符串或其他分子表示形式转换为 RDKit 分子objects.
- **参数**：接受SMILES字符串、InChI或其他分子格式
- **返回**：`rdkit.Chem.Mol`对象
- **常用**：`mol = dm.to_mol("CCO")`

### `from_inchi(inchi)`
将InChI字符串转换为分子对象.

### `from_smarts(smarts)`
将SMARTS图案转换为分子对象。

### `from_selfies(selfies)`
将SELFIES字符串转换为分子对象。

### `copy_mol(mol)`
创建分子对象的副本以避免修改原来的。

## 分子导出

### `to_smiles(mol, ...)`
将分子对象转换为SMILES字符串。
- **常用参数**：`canonical=True`、`isomeric=True`

### `to_inchi(mol, ...)`
将分子转换为 InChI 字符串表示形式。

### `to_inchikey(mol)`
将分子转换为 InChI 密钥（固定长度哈希）。

### `to_smarts(mol)`
将分子转换为 SMARTS pattern.

### `to_selfies(mol)`
将分子转换为SELFIES（自引用嵌入字符串）格式。

## 消毒和标准化

### `sanitize_mol(mol, ...)`
RDKit消毒的增强版本
- **目的**：修复常见分子结构问题
- **返回**：已消毒的分子，如果消毒失败则无

### `standardize_mol(mol, disconnect_metals=False, normalize=True, reionize=True, ...)`
应用全面的标准化程序，包括：
- 金属断开连接
- 标准化（电荷校正）
- 再电离
- 片段处理（最大片段选择）

### `standardize_smiles(smiles, ...)`
将SMILES标准化过程直接应用于SMILES字符串。

### `fix_mol(mol)`
尝试自动修复分子结构问题。

### `fix_valence(mol)`
纠正分子结构中的价态错误。

## 分子属性

### `reorder_atoms(mol, ...)`
无论原始 SMILES 表示如何，确保同一分子的原子排序一致。
- **目的**：保持可重现的特征生成

### `remove_hs(mol, ...)`
从分子结构中去除氢原子。

### `add_hs(mol, ...)`
在分子结构中添加明确的氢原子。

## 指纹和相似性

### `to_fp(mol, fp_type='ecfp', ...)`
生成分子指纹用于相似性计算。
- **指纹类型**：
  - `'ecfp'` - 扩展连接指纹（摩根）
  - `'fcfp'` - 功能连接指纹
  - `'maccs'` - MACCS密钥
  - `'topological'` - 拓扑指纹
  - `'atompair'` - 原子对指纹
- **常用参数**：`n_bits`、`radius`
- **返回**： Numpy 数组或 RDKit 指纹对象

### `pdist(mols, ...)`
计算列表中所有分子之间的成对 Tanimoto 距离。
- **支持**：通过 `n_jobs` 参数进行并行处理
- **返回**：距离矩阵

### `cdist(mols1, mols2, ...)`
计算两组分子之间的Tanimoto距离。

## 聚类和多样性

### `cluster_mols(mols, cutoff=0.2, feature_fn=None, n_jobs=1)`
使用Butina聚类算法聚类分子。
- **参数**：
  - `cutoff`：距离阈值（默认 0.2）
  - `feature_fn`：分子特征的自定义函数
  - `n_jobs`：并行化（所有核心为-1）
- **重要**：构建完整距离矩阵 - 适合对于~1000个结构，不适用于10,000+
- **返回**：簇列表（每个簇是分子索引列表）

### `pick_diverse(mols, npick, ...)`
根据指纹多样性选择不同的分子子集。

### `pick_centroids(mols, npick, ...)`
Select代表簇的质心分子。

## 图形操作

### `to_graph(mol)`
将分子转换为图形表示以进行基于图形的分析。

### `get_all_path_between(mol, start, end)`
查找分子结构中两个原子之间的所有路径。

## 数据框架集成

### `to_df(mols, smiles_column='smiles', mol_column='mol')`
将分子列表转换为pandas DataFrame。

### `from_df(df, smiles_column='smiles', mol_column='mol')`
将pandas DataFrame转换为分子列表。
