# TCGA / GDC 数据门户 API

## 基本 URL
```
https://api.gdc.cancer.gov
```

## Auth
没有公共数据的身份验证。仅受控访问下载需要令牌。

## 关键端点

所有搜索端点都接受 GET 或 POST（复杂过滤器首选 POST）。

|端点|描述 |
|----------|--------------|
| `/projects` |列出/过滤癌症项目（例如 TCGA-BRCA）|
| `/cases` |搜索病例（患者/样本）|
| `/files` |搜索/过滤文件（BAM、VCF、表达式）|
| `/genes` |搜索基因级数据|
| `/ssms` |搜索简单体细胞突变|
| `/ssm_occurrences` |跨案例突变发生 |
| `/files/{uuid}` |文件元数据（按 UUID |
|） `/data/{uuid}` |按 UUID 下载文件 |

## 过滤语法（POST body）
```json
{
  "filters": {
    "op": "in",
    "content": {"field": "cases.project.project_id", "value": ["TCGA-BRCA"]}
  },
  "fields": "file_id,file_name,data_type",
  "format": "JSON",
  "size": 10
}
```
 运算符：`in`、`=`、`!=`、`>`、`<`、`>=`、 `<=`, `is`, `not`, `and`, `or`

## 调用示例
```
# List projects
https://api.gdc.cancer.gov/projects?size=5&fields=project_id,name,primary_site

# BRCA1 mutations (POST)
curl -X POST https://api.gdc.cancer.gov/ssms \
  -H "Content-Type: application/json" \
  -d '{"filters":{"op":"in","content":{"field":"consequence.transcript.gene.symbol","value":["BRCA1"]}},"fields":"ssm_id,genomic_dna_change","size":5}'

# Cases in TCGA-LUAD
https://api.gdc.cancer.gov/cases?filters=%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22project.project_id%22%2C%22value%22%3A%5B%22TCGA-LUAD%22%5D%7D%7D&size=3&fields=submitter_id,disease_type
```

## 分页
`from` （偏移量）和 `size`（限制，最大 10000）。默认大小为 10。

## 速率限制
对元数据查询没有严格限制。使用 GDC Transfer Tool 进行批量文件下载。
