# Datamol I/O 模块参考

`datamol.io` 模块为多种格式的分子数据提供全面的文件处理。

## 读取分子文件

### `dm.read_sdf(filename, sanitize=True, remove_hs=True, as_df=True, mol_column='mol', ...)`
读取结构数据文件 (SDF)格式。
- **参数**：
  - `filename`：SDF文件的路径（通过fsspec支持本地和远程路径）
  - `sanitize`：对分子应用消毒
  - `remove_hs`：删除显式氢
  - `as_df`：返回为DataFrame（True）或列表分子（False）
  - `mol_column`：DataFrame中分子列的名称
  - `n_jobs`：启用并行处理
- **返回**：DataFrame或分子列表
- **示例**：`df = dm.read_sdf("compounds.sdf")`

### `dm.read_smi(filename, smiles_column='smiles', mol_column='mol', as_df=True, ...)`
读取SMILES文件（默认以空格分隔）。
- **通用格式**：SMILES后跟分子ID/名称
- **示例**：`df = dm.read_smi("molecules.smi")`

### `dm.read_csv(filename, smiles_column='smiles', mol_column=None, ...)`
读取CSV文件具有可选的自动 SMILES 到分子转换。
- **参数**：
  - `smiles_column`：包含 SMILES 字符串的列
  - `mol_column`：如果指定，则从 SMILES 列创建分子对象
- **示例**： `df = dm.read_csv("data.csv", smiles_column="SMILES", mol_column="mol")`

### `dm.read_excel(filename, sheet_name=0, smiles_column='smiles', mol_column=None, ...)`
使用分子处理读取Excel文件。
- **参数**：
  - `sheet_name`：要读取的工作表（索引或名称）
  - 其他参数类似于`read_csv`
- **示例**：`df = dm.read_excel("compounds.xlsx", sheet_name="Sheet1")`

### `dm.read_molblock(molblock, sanitize=True, remove_hs=True)`
解析MOL块字符串（分子结构文本表示）。

### `dm.read_mol2file(filename, sanitize=True, remove_hs=True, cleanupSubstructures=True)`
读取Mol2格式文件.

### `dm.read_pdbfile(filename, sanitize=True, remove_hs=True, proximityBonding=True)`
读取蛋白质数据库（PDB）格式文件。

### `dm.read_pdbblock(pdbblock, sanitize=True, remove_hs=True, proximityBonding=True)`
解析PDB块字符串。

### `dm.open_df(filename, ...)`
通用数据帧阅读器 - 自动检测格式。
- **支持的格式**：CSV、Excel、Parquet、JSON、SDF
- **示例**：`df = dm.open_df("data.csv")` 或 `df = dm.open_df("molecules.sdf")`

## 写入分子文件

### `dm.to_sdf(mols, filename, mol_column=None, ...)`
将分子写入SDF文件。
- **输入类型**：
  - 分子列表
  - 分子列数据框
  - 分子序列
- **参数**：
  - `mol_column`：如果输入为 DataFrame
- **示例**:
 ```python
 dm.to_sdf(mols, "output.sdf")
 # 或来自 DataFrame
dm.to_sdf(df, "output.sdf", mol_column="mol")
 ```

### `dm.to_smi(mols, filename, mol_column=None, ...)`
将分子写入 SMILES 文件并进行可选验证。
- **格式**：带有可选分子名称/ID 的 SMILES 字符串

### `dm.to_xlsx(df, filename, mol_columns=None, ...)`
将带有渲染分子图像的 DataFrame 导出到 Excel。
- **参数**：
  - `mol_columns`：包含要渲染为图像的分子的列
- **特殊功能**：自动将分子渲染为 Excel 单元格中的图像
- **示例**： `dm.to_xlsx(df, "molecules.xlsx", mol_columns=["mol"])`

### `dm.to_molblock(mol, ...)`
将分子转换为MOL块字符串。

### `dm.to_pdbblock(mol, ...)`
将分子转换为PDB块字符串。

### `dm.save_df(df, filename, ...)`
以多种格式保存 DataFrame（CSV、Excel、Parquet、JSON）。

## 远程文件支持

所有 I/O 功能通过 fsspec 集成支持远程文件路径：
- **支持的协议**：S3 (AWS)、GCS (Google Cloud)、Azure、 HTTP/HTTPS
- **示例**：
 ```python
 dm.read_sdf("s3://bucket/compounds.sdf")
 dm.read_csv("https://example.com/data.csv")
 ```

## 跨函数的关键参数

- **`sanitize`**：应用分子清理（默认：True）
- **`remove_hs`**：删除显式氢（默认：True）
- **`as_df`**：返回DataFrame与列表（默认：对于大多数函数为True）
- **`n_jobs`**：启用并行处理（无 = 所有核心，1 = 顺序）
- **`mol_column`**：DataFrames 中分子列的名称
- **`smiles_column`**：DataFrames 中 SMILES 列的名称
