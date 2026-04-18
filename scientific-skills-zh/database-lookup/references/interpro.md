# InterPro API 参考

## 基本 URL
```
https://www.ebi.ac.uk/interpro/api
```

## 身份验证
不需要。完全公开的API。

## 速率限制
没有发布的硬限制。 EBI 一般指导：合理，对大型数据集使用批量下载。

## 响应格式默认为 
JSON。某些端点明确支持 `?format=json`。

## 关键端点

### 1. 条目查找（按加入）
```
GET https://www.ebi.ac.uk/interpro/api/entry/interpro/{accession}
```
E示例：
```
GET https://www.ebi.ac.uk/interpro/api/entry/interpro/IPR000504
```
 返回包含条目名称、类型（系列/域/站点/等）、描述、GO 术语、文献的 JSON references.

### 2. 按成员数据库进行条目查找
```
GET https://www.ebi.ac.uk/interpro/api/entry/pfam/{pfam_accession}
GET https://www.ebi.ac.uk/interpro/api/entry/smart/{smart_accession}
GET https://www.ebi.ac.uk/interpro/api/entry/prosite/{prosite_accession}
```
E示例：
```
GET https://www.ebi.ac.uk/interpro/api/entry/pfam/PF00076
```

### 3. 搜索/列表条目
```
GET https://www.ebi.ac.uk/interpro/api/entry/interpro?search={query}
```
E示例：
```
GET https://www.ebi.ac.uk/interpro/api/entry/interpro?search=kinase
```
返回匹配的InterPro条目的分页列表。

### 4. 蛋白质注释 — 获取a的InterPro条目Protein
```
GET https://www.ebi.ac.uk/interpro/api/entry/interpro/protein/uniprot/{uniprot_accession}
```
示例：
```
GET https://www.ebi.ac.uk/interpro/api/entry/interpro/protein/uniprot/P12345
```
返回注释该蛋白质的所有 InterPro 条目。

### 5. 具有给定条目的蛋白质
```
GET https://www.ebi.ac.uk/interpro/api/protein/uniprot/entry/interpro/{accession}
```
示例：
```
GET https://www.ebi.ac.uk/interpro/api/protein/uniprot/entry/interpro/IPR000504
```
返回用该条目注释的 UniProt 蛋白质的分页列表。

### 6. 结构映射
```
GET https://www.ebi.ac.uk/interpro/api/structure/pdb/entry/interpro/{accession}
```
E示例：
```
GET https://www.ebi.ac.uk/interpro/api/structure/pdb/entry/interpro/IPR000504
```

### 7. 按类型分类的条目过滤器
```
GET https://www.ebi.ac.uk/interpro/api/entry/interpro?type=domain
GET https://www.ebi.ac.uk/interpro/api/entry/interpro?type=family
GET https://www.ebi.ac.uk/interpro/api/entry/interpro?type=homologous_superfamily
```

### 8.分类交叉引用
```
GET https://www.ebi.ac.uk/interpro/api/taxonomy/uniprot/entry/interpro/{accession}
```

## 分页
响应包括`next`和`previous` URLs：
```json
{
  "count": 1234,
  "next": "https://www.ebi.ac.uk/interpro/api/entry/interpro?cursor=...&page_size=20",
  "previous": null,
  "results": [...]
}
```
使用`?page_size=N`控制页面大小（默认20）。

## 条目响应关键字段
```json
{
  "metadata": {
    "accession": "IPR000504",
    "name": "RNA recognition motif domain",
    "type": "domain",
    "source_database": "interpro",
    "member_databases": {"pfam": {"PF00076": "RRM_1"}},
    "go_terms": [{"identifier": "GO:0003723", "name": "RNA binding"}],
    "description": ["<p>The RNA recognition motif...</p>"]
  }
}
```

## 注释
- API遵循可组合的URL模式：组合实体类型（条目，蛋白质， 
- 成员数据库：pfam、smart、prosite、prints、panther、cdd、hamap、tigrfam、pirsf、sfld、ncbifam.
