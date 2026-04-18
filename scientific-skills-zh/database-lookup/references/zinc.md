# ZINC 数据库 API

## 基本 URL

```
https://zinc.docking.org
```

## Auth

无需 API 密钥。完全开放公共API。

## URL模式

资源遵循统一模式，文件扩展名指定格式：

```
/{resource}.{format}
/{resource}/{id}.{format}
/{resource}/subsets/{subset}.{format}
```

支持格式：`.json`、`.csv`、`.txt`、`.smi`、 `.sdf`、`.mol2`、`.xml`、`.png`

字段选择（仅返回特定字段）：
```
/{resource}.json:field1+field2+field3
```

## 关键端点

### ZINC的物质查找ID
```
GET /substances/ZINC000000000053.json
```

### 按名称搜索
```
GET /substances.json?preferred_name=aspirin
```

### 按 InChIKey 搜索
```
GET /substances.json?inchikey=BSYNRYMUTXBXSQ-UHFFFAOYSA-N
```

### 按分子搜索公式
```
GET /substances.json?mol_formula=C9H8O4
```

### 子结构搜索(SMILES)
```
GET /substances.json?sub_id-matches=c1ccccc1&count=10
```

### 子结构搜索(SMARTS)
```
GET /substances.json?sub_id-matches-sma=[ND1]&count=10
```

### 相似性搜索(Tanimoto, ECFP4指纹）

阈值（例如，40 = 40%）是参数名称的一部分。值可以是 SMILES 或 ZINC ID 号。
```
GET /substances/?ecfp4_fp-tanimoto-40=c1ccccc1O
GET /substances/?ecfp4_fp-tanimoto-70=ZINC000000000053
```

### 浏览子集

按可购买性、药物状态、反应性或来源过滤：
```
GET /substances/subsets/fda.json              # FDA-approved drugs
GET /substances/subsets/in-stock.json         # In-stock compounds
GET /substances/subsets/metabolites.json      # Metabolites
GET /substances/subsets/fda+in-stock.json     # Combine subsets with +
```

 关键子集：
- **可购买性**：`in-stock`、`on-demand`、`for-sale`、`bb`（积木）
- **药品状态**：`fda`、`world`、`in-trials`、`in-man`、 `in-vivo`、`in-vitro`
- **原点**：`biogenic`、`metabolites`、`natural-products`、`endogenous`
- **反应性**：`anodyne`、`clean`、 `standard`、`reactive`

### 基因靶标物质
```
GET /genes/ACHE/substances.json?count=10
```

### 产品目录
```
GET /catalogs.json                            # List all vendor catalogs
GET /catalogs/cmcd/substances.json            # Substances in a catalog
```

### 2D 结构图像 (300x300) PNG)
```
GET /substances/ZINC000000000053.png
```

### 分子格式转换
```
GET /apps/mol/convert?from=CC(=O)Oc1ccccc1C(=O)O&to=inchikey
```
 以纯文本形式返回 InChIKey。支持 SMILES、InChI 和 InChIKey 之间的转换。

### 批量解析 (POST)

一次解析多个名称、ZINC ID 或 SMILES：
```
POST /substances/resolved/
Content-Type: application/x-www-form-urlencoded

paste=aspirin%0Aibuprofen%0AZINC000000000053&identifiers=y&structures=y&names=y&output_format=json
```

## 查询参数

### 分页
- `count=N` — 每页结果（在大型集合上谨慎使用 `count=all`）
- `page=N` — 页码（1 索引）

### 排序
- `sort=mwt` — 升序field
- `sort=-mwt` — 降序（前缀为 `-`）
- `sort=no` — 禁用排序以加快批量查询速度

### 属性过滤器（比较运算符）
- `mwt-le=500` — 分子量 <= 500
- `logp-ge=2` — LogP >= 2
- `hbd-le=5` — H 键供体 <= 5
- 运算符：`-le` (<=)、`-ge` (>=)、`-lt` (<)、 `-gt` (>)、`-eq` (=)

### 可搜索物质属性

分子属性：`mwt`、`logp`、`hba`、`hbd`、`tpsa`、 `rb`（可旋转键）、`num_rings`、`num_aromatic_rings`、`num_heavy_atoms`、`num_chiral_centers`、`fractioncsp3`

标识符：`zinc_id`、`smiles`、`inchikey`、 `mol_formula`、`preferred_name`、`cas_numbers`

状态：`purchasable`、`reactive`、`bb`（构建块）

## 调用示例

### 获取属性化合物
```
GET /substances/ZINC000000000053.json:zinc_id+smiles+mwt+logp+hba+hbd+tpsa+mol_formula+preferred_name
```

### 按分子量排序的FDA药物
```
GET /substances/subsets/fda.json:zinc_id+preferred_name+mwt?sort=mwt&count=10
```

### 类药化合物（Lipinski过滤器）
```
GET /substances/subsets/for-sale.json?mwt-le=500&logp-le=5&hbd-le=5&hba-le=10&count=20
```

### 查找针对特定目标的化合物gene
```
GET /genes/EGFR/substances.json:zinc_id+preferred_name+smiles?count=10
```

## 响应格式

```json
[
  {
    "zinc_id": "ZINC000000000053",
    "smiles": "CC(=O)Oc1ccccc1C(=O)O",
    "preferred_name": "aspirin",
    "mwt": 180.159,
    "logp": 1.31,
    "hba": 3,
    "hbd": 1,
    "tpsa": 63,
    "mol_formula": "C9H8O4",
    "inchikey": "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
    "purchasable": 5
  }
]
```

响应是 JSON 数组。单记录查找（按 ZINC ID）返回 JSON 对象。

## 速率限制

没有记录的速率限制。 API 是公共资助的 (NIH NIGMS GM71896)。请尊重：
- 使用 `count=` 限制结果大小
- 使用 `sort=no` 进行更快的批量查询
- 相似性和子结构搜索的计算成本很高 - 预计响应较慢
- 避免在大型结果集上使用 `count=all`

## 特殊注释

- ZINC 包含 **2+ 十亿** 市售化合物 — 始终使用 `count=` 来限制结果
- ZINC ID 的格式为 `ZINC000000000053`（“ZINC”后填充 15 位零）
- `.smi` 格式返回 SMILES 字符串，对化学信息学管道很有用 
- `.sdf` 格式返回适合对接软件的 3D 结构
- 子集可与 `+` 组合（例如，`fda+in-stock` = FDA 批准且有库存）
- 对于虚拟筛选工作流程，使用批次 (`/tranches/`)按分子量进行分区， LogP
