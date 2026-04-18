# PRIDE Archive REST API 参考

## 概述
PRIDE（蛋白质组学 IDentifications 数据库）位于 EMBL-EBI，提供完整的公共 REST API，用于查询蛋白质组学数据集、蛋白质、肽和光谱。

## 基本 URL
```
https://www.ebi.ac.uk/pride/ws/archive/v2
```
（旧版 v1 也存在，但 v2 已存在）当前）

## 身份验证
- **读取访问无需身份验证**
- 开放并免费使用

## 关键端点

|端点|描述 |
|---|---|
| `GET /projects` |搜索/列出蛋白质组学项目 |
| `GET /projects/{accession}` |通过PXD加入|
|获取特定项目`GET /projects/{accession}/files` |列出项目的文件 |
| `GET /spectra` |搜索光谱|
| `GET /peptideevidences` |搜索肽证据|
| `GET /proteinevidences` |搜索蛋白质证据|
| `GET /stats` |数据库统计 |

## 查询参数
- `keyword` — 自由文本搜索
- `filter` — 特定于字段的过滤器（例如，物种、仪器、修改）
- `pageSize` — 每页结果（默认 10，最多100)
- `page` — 页码（0 索引）
- `sortDirection` — ASC 或 DESC
- `sortFields` — 排序依据的字段

## 示例调用

```bash
# Search projects by keyword
curl "https://www.ebi.ac.uk/pride/ws/archive/v2/projects?keyword=alzheimer&pageSize=5"

# Get a specific project
curl "https://www.ebi.ac.uk/pride/ws/archive/v2/projects/PXD010000"

# List files for a project
curl "https://www.ebi.ac.uk/pride/ws/archive/v2/projects/PXD010000/files?pageSize=10"

# Search by species (human = 9606)
curl "https://www.ebi.ac.uk/pride/ws/archive/v2/projects?filter=organisms_facet==9606&pageSize=5"

# Get database statistics
curl "https://www.ebi.ac.uk/pride/ws/archive/v2/stats"
```

## 响应格式
JSON。示例（项目）：
```json
{
  "accession": "PXD010000",
  "title": "Project title here",
  "projectDescription": "...",
  "organisms": [{"accession": "9606", "name": "Homo sapiens"}],
  "instruments": [{"name": "Q Exactive"}],
  "submissionDate": "2018-05-01",
  "publicationDate": "2018-09-01",
  "numAssays": 12,
  "references": [{"pubmedId": 12345678}]
}
```

## 速率限制
- 没有严格发布的速率限制，但适用标准 EBI 合理使用策略
- 建议：限制为每秒几个请求
- 通过 FTP/Aspera 提供批量数据ftp.pride.ebi.ac.uk
