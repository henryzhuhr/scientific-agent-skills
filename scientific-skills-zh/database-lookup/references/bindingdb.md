# BindingDB REST API

## 基本 URL
```
https://bindingdb.org/rest/
https://bindingdb.org/axis2/services/BDBService/
```

## Auth
不需要 API 密钥。完全开放、免费。

## 响应格式
默认为XML。将 `&response=application/json` 附加到 JSON 的任何端点。

## 关键端点

|端点|描述 |
|----------|--------------|
| `/rest/getLigandsByUniprot` |单一蛋白质靶标的配体|
| `/rest/getLigandsByUniprots` |多个蛋白质靶标的配体|
| `/rest/getLigandsByPDBs` |按 PDB 结构 ID 划分的配体 |
| `/rest/getTargetByCompound` |化合物的靶标（SMILES 相似性） |

## 端点详细信息

### 获取单个靶标的配体
```
GET https://bindingdb.org/rest/getLigandsByUniprot?uniprot={UNIPROT_ID};{IC50_cutoff_nM}&response=application/json
```
- `uniprot` — UniProt ID，后跟 `;` 和 nM
 中的亲和力截止值 - 返回单体 ID、SMILES、亲和力类型(IC50, Ki, Kd)和值
- 如果未找到 UniProt ID，则返回空字符串

示例：
```
https://bindingdb.org/rest/getLigandsByUniprot?uniprot=P35355;100&response=application/json
```

### 获取多个目标的配体
```
GET https://bindingdb.org/rest/getLigandsByUniprots?uniprot={IDs}&cutoff={nM}&response=application/json
```
- `uniprot` — 逗号分隔UniProt IDs
- `cutoff` — nM
 中的亲和力截止值 - 如果没有匹配的 ID

E，则返回空字符串示例：
```
https://bindingdb.org/rest/getLigandsByUniprots?uniprot=P00176,P00183&cutoff=10000&response=application/json
```

### 通过 PDB 获取配体结构
```
GET https://bindingdb.org/rest/getLigandsByPDBs?pdb={PDBs}&cutoff={nM}&identity={percent}&response=application/json
```
- `pdb` — 逗号分隔的 PDB ID
- `cutoff` — nM
- `identity` 中的亲和力截止值 — 序列同一性截止值（百分比，例如92)

示例：
```
https://bindingdb.org/rest/getLigandsByPDBs?pdb=1Q0L,3ANM&cutoff=100&identity=92&response=application/json
```

### 查找化合物的目标（相似性搜索）
```
GET https://bindingdb.org/rest/getTargetByCompound?smiles={SMILES}&cutoff={similarity}&response=application/json
```
- `smiles` — 化合物 SMILES（必须进行 URL 编码）
- `cutoff` — Tanimoto 相似性截止值（十进制，例如 0.85）
  - 返回相似的化合物及其蛋白质靶标和亲和力 

E 示例：
```
https://bindingdb.org/rest/getTargetByCompound?smiles=CCC%5BN%2B%5D%28C%29%28C%29CCn1nncc1COc1cc%28%3DO%29n%28C%29c2ccccc12&cutoff=0.85&response=application/json
```

## 速率限制 
无记录限制。出于礼貌，将请求保持在每秒约 1 个。

## 注释
- API 表面很小（4 个端点），但专注于结合亲和力数据
- 对于化合物名称搜索，首先通过 PubChem 解析为 SMILES，然后使用 `getTargetByCompound`
- 对于批量数据访问，请使用可下载的 TSV/SDF 文件https://www.bindingdb.org/bind/chemsearch/marvin/Download.jsp
- 包含约 320 万个结合测量结果，约 140 万种化合物和约 11.4K 个目标
