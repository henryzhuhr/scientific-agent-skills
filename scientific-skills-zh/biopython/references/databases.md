# 使用 Bio.Entrez

## 进行数据库访问## 概述

Bio.Entrez 提供对 NCBI 的 Entrez 数据库的编程访问，包括 PubMed、GenBank、基因、蛋白质、核苷酸等。它处理 API 调用、速率限制和数据解析的所有复杂性。

## 设置和配置

### 电子邮件地址（必需）

NCBI 需要电子邮件地址来跟踪使用情况并在出现问题时联系用户：

```python
from Bio import Entrez

# Always set your email
Entrez.email = "your.email@example.com"
```

### API 密钥（推荐）

使用 API key 将速率限制从每秒 3 个请求增加到 10 个请求：

```python
# Get API key from: https://www.ncbi.nlm.nih.gov/account/settings/
Entrez.api_key = "your_api_key_here"
```

### 速率限制

Biopython 自动遵守 NCBI 速率限制：
- **没有 API 密钥**：每秒 3 个请求
- **使用 API 密钥**：每个 10 个请求第二个

模块会自动处理此问题，因此您不需要在请求之间添加延迟。

## Core Entrez Functions

### EInfo - 数据库信息

获取有关可用数据库及其统计信息的信息：

```python
# List all databases
handle = Entrez.einfo()
result = Entrez.read(handle)
print(result["DbList"])

# Get information about a specific database
handle = Entrez.einfo(db="pubmed")
result = Entrez.read(handle)
print(result["DbInfo"]["Description"])
print(result["DbInfo"]["Count"])  # Number of records
```

### ESearch - 搜索数据库

搜索记录并检索其 ID：

```python
# Search PubMed
handle = Entrez.esearch(db="pubmed", term="biopython")
result = Entrez.read(handle)
handle.close()

id_list = result["IdList"]
count = result["Count"]
print(f"Found {count} results")
print(f"Retrieved IDs: {id_list}")
```

### 高级 ESearch 参数

```python
# Search with additional parameters
handle = Entrez.esearch(
    db="pubmed",
    term="biopython[Title]",
    retmax=100,           # Return up to 100 IDs
    sort="relevance",     # Sort by relevance
    reldate=365,          # Only results from last year
    datetype="pdat"       # Use publication date
)
result = Entrez.read(handle)
handle.close()
```

### ESummary - 获取记录摘要

检索列表的摘要信息ID：

```python
# Get summaries for multiple records
handle = Entrez.esummary(db="pubmed", id="19304878,18606172")
results = Entrez.read(handle)
handle.close()

for record in results:
    print(f"Title: {record['Title']}")
    print(f"Authors: {record['AuthorList']}")
    print(f"Journal: {record['Source']}")
    print()
```

### EFetch - 检索全记录

获取各种格式的完整记录：

```python
# Fetch a GenBank record
handle = Entrez.efetch(db="nucleotide", id="EU490707", rettype="gb", retmode="text")
record_text = handle.read()
handle.close()

# Parse with SeqIO
from Bio import SeqIO
handle = Entrez.efetch(db="nucleotide", id="EU490707", rettype="gb", retmode="text")
record = SeqIO.read(handle, "genbank")
handle.close()
print(record.description)
```

### EFetch 返回类型

不同数据库支持不同的返回类型：

* *核苷酸/蛋白质：**
- `rettype="fasta"` - FASTA 格式
- `rettype="gb"` 或 `"genbank"` - GenBank 格式
- `rettype="gp"` - GenPept 格式（蛋白质）

* *PubMed：**
- `rettype="medline"` - MEDLINE 格式
- `rettype="abstract"` - 摘要文本

* *常见模式：**
- `retmode="text"` - 纯文本
- `retmode="xml"` - XML 格式

### ELink - 查找相关记录

查找不同数据库中记录之间的链接：

```python
# Find protein records linked to a nucleotide record
handle = Entrez.elink(dbfrom="nucleotide", db="protein", id="EU490707")
result = Entrez.read(handle)
handle.close()

# Extract linked IDs
for linkset in result[0]["LinkSetDb"]:
    if linkset["LinkName"] == "nucleotide_protein":
        protein_ids = [link["Id"] for link in linkset["Link"]]
        print(f"Linked protein IDs: {protein_ids}")
```

### EPost - 上传 ID 列表

将大型 ID 列表上传到服务器以供以后使用：

```python
# Post IDs to server
id_list = ["19304878", "18606172", "16403221"]
handle = Entrez.epost(db="pubmed", id=",".join(id_list))
result = Entrez.read(handle)
handle.close()

# Get query_key and WebEnv for later use
query_key = result["QueryKey"]
webenv = result["WebEnv"]

# Use in subsequent queries
handle = Entrez.efetch(
    db="pubmed",
    query_key=query_key,
    WebEnv=webenv,
    rettype="medline",
    retmode="text"
)
```

### EGQuery - 全局查询

一次在所有 Entrez 数据库中搜索：

```python
handle = Entrez.egquery(term="biopython")
result = Entrez.read(handle)
handle.close()

for row in result["eGQueryResult"]:
    print(f"{row['DbName']}: {row['Count']} results")
```

### ESpell - 拼写建议

获取搜索的拼写建议条款：

```python
handle = Entrez.espell(db="pubmed", term="biopythn")
result = Entrez.read(handle)
handle.close()

print(f"Original: {result['Query']}")
print(f"Suggestion: {result['CorrectedQuery']}")
```

## 使用不同的数据库

### PubMed

```python
# Search for articles
handle = Entrez.esearch(db="pubmed", term="cancer genomics", retmax=10)
result = Entrez.read(handle)
handle.close()

# Fetch abstracts
handle = Entrez.efetch(
    db="pubmed",
    id=result["IdList"],
    rettype="medline",
    retmode="text"
)
records = handle.read()
handle.close()
print(records)
```

### GenBank / 核苷酸

```python
# Search for sequences
handle = Entrez.esearch(db="nucleotide", term="Cypripedioideae[Orgn] AND matK[Gene]")
result = Entrez.read(handle)
handle.close()

# Fetch sequences
if result["IdList"]:
    handle = Entrez.efetch(
        db="nucleotide",
        id=result["IdList"][:5],
        rettype="fasta",
        retmode="text"
    )
    sequences = handle.read()
    handle.close()
```

### Protein

```python
# Search for protein sequences
handle = Entrez.esearch(db="protein", term="human insulin")
result = Entrez.read(handle)
handle.close()

# Fetch protein records
from Bio import SeqIO
handle = Entrez.efetch(
    db="protein",
    id=result["IdList"][:5],
    rettype="gp",
    retmode="text"
)
records = SeqIO.parse(handle, "genbank")
for record in records:
    print(f"{record.id}: {record.description}")
handle.close()
```

### Gene

```python
# Search for gene records
handle = Entrez.esearch(db="gene", term="BRCA1[Gene] AND human[Organism]")
result = Entrez.read(handle)
handle.close()

# Get gene information
handle = Entrez.efetch(db="gene", id=result["IdList"][0], retmode="xml")
record = Entrez.read(handle)
handle.close()
```

### 分类

```python
# Search for organism
handle = Entrez.esearch(db="taxonomy", term="Homo sapiens")
result = Entrez.read(handle)
handle.close()

# Fetch taxonomic information
handle = Entrez.efetch(db="taxonomy", id=result["IdList"][0], retmode="xml")
records = Entrez.read(handle)
handle.close()

for record in records:
    print(f"TaxID: {record['TaxId']}")
    print(f"Scientific Name: {record['ScientificName']}")
    print(f"Lineage: {record['Lineage']}")
```

## 解析 Entrez 结果

### 读取 XML结果

```python
# Most results can be parsed with Entrez.read()
handle = Entrez.efetch(db="pubmed", id="19304878", retmode="xml")
records = Entrez.read(handle)
handle.close()

# Access parsed data
article = records['PubmedArticle'][0]['MedlineCitation']['Article']
print(article['ArticleTitle'])
```

### 处理大型结果集

```python
# Batch processing for large searches
search_term = "cancer[Title]"
handle = Entrez.esearch(db="pubmed", term=search_term, retmax=0)
result = Entrez.read(handle)
handle.close()

total_count = int(result["Count"])
batch_size = 500

for start in range(0, total_count, batch_size):
    # Fetch batch
    handle = Entrez.esearch(
        db="pubmed",
        term=search_term,
        retstart=start,
        retmax=batch_size
    )
    result = Entrez.read(handle)
    handle.close()

    # Process IDs
    id_list = result["IdList"]
    print(f"Processing IDs {start} to {start + len(id_list)}")
```

## 高级模式

### 使用 WebEnv 搜索历史记录

```python
# Perform search and store on server
handle = Entrez.esearch(
    db="pubmed",
    term="biopython",
    usehistory="y"
)
result = Entrez.read(handle)
handle.close()

webenv = result["WebEnv"]
query_key = result["QueryKey"]
count = int(result["Count"])

# Fetch results in batches using history
batch_size = 100
for start in range(0, count, batch_size):
    handle = Entrez.efetch(
        db="pubmed",
        retstart=start,
        retmax=batch_size,
        rettype="medline",
        retmode="text",
        webenv=webenv,
        query_key=query_key
    )
    data = handle.read()
    handle.close()
    # Process data
```

### 组合搜索

```python
# Use boolean operators
complex_search = "(cancer[Title]) AND (genomics[Title]) AND 2020:2025[PDAT]"
handle = Entrez.esearch(db="pubmed", term=complex_search, retmax=100)
result = Entrez.read(handle)
handle.close()
```

## 最佳实践

1. **始终设置 Entrez.email** - NCBI
2 需要。 **使用 API 密钥**以获得更高的速率限制（10 请求/秒 vs 3 请求/秒）
3. **阅读后释放资源
4，关闭句柄**。 **批量大请求** - 使用 retstart 和 retmax 进行分页
5. **使用 WebEnv 进行大量下载** - 将结果存储在服务器
6 上。 **本地缓存** - 下载一次并保存以避免重复请求
7. **优雅地处理错误** - 可能会出现网络问题和 API 限制
8. **尊重 NCBI 指南** - 不要淹没服务
9. **使用适当的rettype** - 选择符合您需求的格式
10. **仔细解析 XML** - 结构因数据库和记录类型而异

## 错误处理

```python
from urllib.error import HTTPError
from Bio import Entrez

Entrez.email = "your.email@example.com"

try:
    handle = Entrez.efetch(db="nucleotide", id="invalid_id", rettype="gb")
    record = handle.read()
    handle.close()
except HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}")
except Exception as e:
    print(f"Error: {e}")
```

## 常见用例

### 下载 GenBank 记录

```python
from Bio import Entrez, SeqIO

Entrez.email = "your.email@example.com"

# List of accession numbers
accessions = ["EU490707", "EU490708", "EU490709"]

for acc in accessions:
    handle = Entrez.efetch(db="nucleotide", id=acc, rettype="gb", retmode="text")
    record = SeqIO.read(handle, "genbank")
    handle.close()

    # Save to file
    SeqIO.write(record, f"{acc}.gb", "genbank")
```

### 搜索和下载论文

```python
# Search PubMed
handle = Entrez.esearch(db="pubmed", term="machine learning bioinformatics", retmax=20)
result = Entrez.read(handle)
handle.close()

# Get details
handle = Entrez.efetch(db="pubmed", id=result["IdList"], retmode="xml")
papers = Entrez.read(handle)
handle.close()

# Extract information
for paper in papers['PubmedArticle']:
    article = paper['MedlineCitation']['Article']
    print(f"Title: {article['ArticleTitle']}")
    print(f"Journal: {article['Journal']['Title']}")
    print()
```

### 查找相关序列

```python
# Start with one sequence
handle = Entrez.efetch(db="nucleotide", id="EU490707", rettype="gb", retmode="text")
record = SeqIO.read(handle, "genbank")
handle.close()

# Find similar sequences
handle = Entrez.elink(dbfrom="nucleotide", db="nucleotide", id="EU490707")
result = Entrez.read(handle)
handle.close()

# Get related IDs
related_ids = []
for linkset in result[0]["LinkSetDb"]:
    for link in linkset["Link"]:
        related_ids.append(link["Id"])
```
