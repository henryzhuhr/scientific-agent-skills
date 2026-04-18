# PubChem PUG REST API

## 基本 URL

```
https://pubchem.ncbi.nlm.nih.gov/rest/pug
```

## URL 模式

```
/{domain}/{namespace}/{identifiers}/{operation}/{output}
```

- **域名**：`compound`、`substance`、`assay`
- **命名空间**：`cid`、`name`、`smiles`、`inchi`、`inchikey`、`fastformula`
- **操作**：`record`、`property`、`synonyms`、 `description`、`cids`、`xrefs`
- **输出**：`JSON`、`XML`、`CSV`、`TXT`、`SDF`、 `PNG`

## 关键端点

### 按名称搜索
```
GET /compound/name/{name}/JSON
```
示例： `/compound/name/aspirin/JSON`

### 按 CID 搜索
```
GET /compound/cid/{cid}/JSON
```
示例： `/compound/cid/2244/JSON`

多个CID：`/compound/cid/2244,5988,3672/JSON`

### 按SMILES搜索
```
GET /compound/smiles/{smiles}/JSON
```
对于带有特殊字符的SMILES，请使用POST：
```
POST /compound/smiles/JSON
Content-Type: application/x-www-form-urlencoded
smiles=CC(=O)OC1=CC=CC=C1C(=O)O
```

### 按SMILES搜索InChIKey
```
GET /compound/inchikey/{inchikey}/JSON
```

### 按 InChI 搜索（仅限 POST — InChI 字符串对于 URL 来说太长）
```
POST /compound/inchi/JSON
Content-Type: application/x-www-form-urlencoded
inchi=InChI=1S/C9H8O4/...
```

### 按分子式搜索
```
GET /compound/fastformula/{formula}/JSON
```
 示例： `/compound/fastformula/C9H8O4/JSON`

### 属性检索
```
GET /compound/{namespace}/{id}/property/{property_list}/JSON
```
属性以逗号分隔。可用属性：

`MolecularFormula`、`MolecularWeight`、`CanonicalSMILES`、`IsomericSMILES`、`InChI`、`InChIKey`、`IUPACName`、`XLogP`、`ExactMass`、 `MonoisotopicMass`、`TPSA`、`Complexity`、`Charge`、`HBondDonorCount`、`HBondAcceptorCount`、`RotatableBondCount`、`HeavyAtomCount`、 `CID`

示例：
```
/compound/cid/2244/property/MolecularFormula,MolecularWeight,CanonicalSMILES,IUPACName/JSON
```

响应：
```json
{
  "PropertyTable": {
    "Properties": [
      {
        "CID": 2244,
        "MolecularFormula": "C9H8O4",
        "MolecularWeight": 180.16,
        "IUPACName": "2-acetyloxybenzoic acid",
        "CanonicalSMILES": "CC(=O)OC1=CC=CC=C1C(O)=O"
      }
    ]
  }
}
```

### 同义词查找
```
GET /compound/{namespace}/{id}/synonyms/JSON
```

### 复合说明
```
GET /compound/cid/{cid}/description/JSON
```

### 从名称中获取 CID
```
GET /compound/name/{name}/cids/JSON
```

### 交叉引用（专利、注册 ID）
```
GET /compound/cid/{cid}/xrefs/PatentID/JSON
GET /compound/cid/{cid}/xrefs/RegistryID/JSON
```

### 相似性搜索（POST、返回异步检索的列表键）
```
POST /compound/fastsimilarity_2d/smiles/cids/JSON
smiles=CC(=O)OC1=CC=CC=C1C(=O)O&Threshold=90
```

### 2D 结构图像
```
GET /compound/cid/{cid}/PNG
GET /compound/cid/{cid}/PNG?image_size=300x300
```

## 速率限制

- 最大**每秒 5 个请求**
- 最大 **每分钟 400 个请求**
- 带逗号的批量 CID（每个 GET 最多 100 个，每个 POST 约 10,000 个）
- 节流错误返回 `PUGREST.ServerBusy` 故障代码

## 错误格式

```json
{
  "Fault": {
    "Code": "PUGREST.NotFound",
    "Message": "No CID found",
    "Details": ["..."]
  }
}
```
