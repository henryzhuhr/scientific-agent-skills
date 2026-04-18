# NCBI 蛋白质 API 参考

## 概述
蛋白质序列记录（RefSeq、GenBank、UniProt 导入）可通过 NCBI 电子实用程序使用 `db=protein`.

## 基本 URL
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

## 身份验证
- **API 密钥** （推荐）：在 https://www.ncbi.nlm.nih.gov/account/ 注册并附加 `&api_key=YOUR_KEY`.
  - 没有密钥：3 个请求/秒。含密钥：10次请求/秒。
- 提供`tool`和`email`参数进行识别。

## 关键端点

### 1. ESearch -- 搜索蛋白质记录
```
GET esearch.fcgi?db=protein&term=QUERY&retmax=N&retmode=json
```
|参数 |描述 |
|--------|--------------|
| `term` |搜索查询（Entrez 语法）。字段：`[Protein Name]`、`[Organism]`、`[Accession]`、`[Gene Name]` |
| `retmax` |返回的最大 ID（默认 20，最大 100000）|
| `retstart` |分页偏移 |
| `usehistory` | `y` 将结果存储在服务器上（与大型集合一起使用） |

* *示例 -- 搜索人胰岛素：**
```
GET esearch.fcgi?db=protein&term=insulin+AND+homo+sapiens[Organism]&retmax=5&retmode=json
```
 响应 (JSON):
```json
{
  "esearchresult": {
    "count": "1523",
    "retmax": "5",
    "idlist": ["116734704", "AAA59172.1", "NP_000198.1", ...],
    "querytranslation": "insulin AND \"Homo sapiens\"[Organism]"
  }
}
```

### 2. EFetch -- 检索蛋白质记录
```
GET efetch.fcgi?db=protein&id=IDS&rettype=TYPE&retmode=MODE
```
|重新输入 |旋转模式 |输出 |
|---------|---------|--------|
| `fasta` | `text` | FASTA序列|
| `gp` | `text` | GenPept 平面锉刀 |
| `gp` | `xml` | GenPept XML (INSDSeq) |
| `acc` | `text` |入藏列表|
| `seqid` | `text` | SeqID列表|
| `ft` | `text` |特征表 |

* *示例 -- 获取 NP_000198.1（人胰岛素）的 FASTA：**
```
GET efetch.fcgi?db=protein&id=NP_000198.1&rettype=fasta&retmode=text
```
 响应：
```
>NP_000198.1 insulin preproprotein [Homo sapiens]
MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAED
LQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN
```

* *示例 -- 获取多个 GenPept XML IDs:**
```
GET efetch.fcgi?db=protein&id=NP_000198.1,NP_001278826.1&rettype=gp&retmode=xml
```

### 3. ESummary -- 简要记录摘要
```
GET esummary.fcgi?db=protein&id=IDS&retmode=json
```
返回：入藏、标题、有机体、长度、分类、创建/更新日期。

### 4. ELink -- 查找相关记录
```
GET elink.fcgi?dbfrom=protein&db=gene&id=NP_000198.1
```
将蛋白质与基因、核苷酸、结构、分类学等链接。

## 常见搜索模式
```
# By accession
term=NP_000198.1[Accession]

# By gene name + organism
term=BRCA1[Gene Name] AND human[Organism]

# RefSeq only
term=insulin AND srcdb_refseq[Properties]

# By sequence length range
term=100:500[Sequence Length] AND kinase[Protein Name]
```

## 速率限制
- 无 API 密钥：3 个请求/秒
- 有 API 密钥：10 个请求/秒
- 大批量下载：使用 `usehistory=y` `WebEnv`/`query_key`，然后分块获取 500
