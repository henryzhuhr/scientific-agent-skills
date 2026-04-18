# RCSB 蛋白质数据库 (PDB) API 参考

## 基本 URL
- **数据 API**：`https://data.rcsb.org/rest/v1`
- **搜索 API**：`https://search.rcsb.org/rcsbsearch/v2/query`
- **GraphQL**：`https://data.rcsb.org/graphql`
- **文件**： `https://files.rcsb.org`

## 身份验证
无需。完全公开的API。

## 速率限制
没有发布硬限制；要有礼貌（每秒几个请求）。可通过 FTP 进行批量下载。

## 关键端点

### 1. 条目查找（数据 API）
```
GET https://data.rcsb.org/rest/v1/core/entry/{entry_id}
```
E 示例：
```
GET https://data.rcsb.org/rest/v1/core/entry/4HHB
```
 返回包含分辨率、方法、沉积日期、标题、作者等的 JSON。

### 2. 聚合物实体（链级信息）
```
GET https://data.rcsb.org/rest/v1/core/polymer_entity/{entry_id}/{entity_id}
```
示例：
```
GET https://data.rcsb.org/rest/v1/core/polymer_entity/4HHB/1
```

### 3. 程序集信息
```
GET https://data.rcsb.org/rest/v1/core/assembly/{entry_id}/{assembly_id}
```

### 4. 全文和属性搜索（搜索） API)
```
POST https://search.rcsb.org/rcsbsearch/v2/query
Content-Type: application/json
```
示例 — 按 UniProt 登录号搜索：
```json
{
  "query": {
    "type": "terminal",
    "service": "text",
    "parameters": {
      "attribute": "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession",
      "operator": "exact_match",
      "value": "P69905"
    }
  },
  "return_type": "entry"
}
```

### 5. 序列搜索（搜索 API）
```json
{
  "query": {
    "type": "terminal",
    "service": "sequence",
    "parameters": {
      "evalue_cutoff": 0.1,
      "identity_cutoff": 0.9,
      "sequence_type": "protein",
      "value": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH"
    }
  },
  "return_type": "polymer_entity"
}
```

### 6. 结构相似性搜索
```json
{
  "query": {
    "type": "terminal",
    "service": "structure",
    "parameters": {
      "value": {"entry_id": "4HHB", "assembly_id": "1"},
      "operator": "strict_shape_match"
    }
  },
  "return_type": "assembly"
}
```

### 7. 下载结构文件
```
GET https://files.rcsb.org/download/{entry_id}.cif
GET https://files.rcsb.org/download/{entry_id}.pdb
```

### 8. GraphQL 查询
```
POST https://data.rcsb.org/graphql
```
Body示例：
```json
{
  "query": "{ entry(entry_id: \"4HHB\") { rcsb_entry_info { resolution_combined } struct { title } } }"
}
```

## 响应格式
所有 REST/搜索端点都返回 JSON。文件下载返回 PDB/mmCIF 文本。

## 有用的 `return_type` 搜索值
- `entry` — PDB ID
- `polymer_entity` — 实体级结果（例如 4HHB_1）
- `assembly` — 生物组装结果

## 注释
- 搜索 API 使用带有 JSON 查询 DSL 的 POST。通过 `"type": "group"` 和 `"logical_operator": "and"/"or"`.
 组合查询 - 通过 `"request_options": {"paginate": {"start": 0, "rows": 25}}`.
 进行分页
