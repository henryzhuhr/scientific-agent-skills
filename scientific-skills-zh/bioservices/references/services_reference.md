# BioServices：完整服务参考

本文档提供了BioServices中可用的所有主要服务的综合参考，包括关键方法、参数和用例。

## 蛋白质和基因资源

### UniProt

蛋白质序列和功能信息数据库.

* *初始化：**
```python
from bioservices import UniProt
u = UniProt(verbose=False)
```

* *关键方法：**

- `search(query, frmt="tab", columns=None, limit=None, sort=None, compress=False, include=False, **kwargs)`
  - 灵活查询语法搜索UniProt
  - `frmt`: "tab", "fasta", "xml", "rdf", "gff", "txt"
  - `columns`：逗号分隔列表（例如，“id,genes,organism,length”）
  - 返回：请求格式的字符串

- `retrieve(uniprot_id, frmt="txt")`
  - 检索特定的 UniProt Entry
  - `frmt`：“txt”、“fasta”、“xml”、“rdf”、“gff”
  - 返回：请求格式的条目数据

- `mapping(fr="UniProtKB_AC-ID", to="KEGG", query="P43403")`
  - 在数据库之间转换标识符
  - `fr`/`to`：数据库标识符（参见identifier_mapping.md）
  - `query`：单个ID或逗号分隔列表
  - 返回：将输入映射到输出ID的字典

- `searchUniProtId(pattern, columns="entry name,length,organism", limit=100)`
  - 的便捷方法基于 ID 的搜索
  - 返回：制表符分隔值

* *常用列：** id、条目名称、基因、生物体、蛋白质名称、长度、序列、go-id、ec、途径、交互者

* *用例：**
- BLAST 的蛋白质序列检索
- 功能注释查找
- 跨数据库标识符映射
- 批量蛋白质信息检索

- --

### KEGG（京都基因和基因组百科全书）

代谢途径、基因和生物体数据库.

* *初始化：**
```python
from bioservices import KEGG
k = KEGG()
k.organism = "hsa"  # Set default organism
```

* *关键方法：**

- `list(database)`
  - 列出 KEGG 数据库中的条目
  - `database`: "organism", "pathway", "module", "disease", "drug", "compound"
  - 返回：带有条目的多行字符串

- `find(database, query)`
  - 通过关键字搜索数据库
  - 返回：具有 ID

 的匹配条目列表- `get(entry_id)`
 - 通过 ID
 检索条目 - 支持基因、途径、化合物等。
 - 返回：原始条目文本

- `parse(data)`
  - 将 KEGG 条目解析为字典
  - 返回：具有结构化的字典data

- `lookfor_organism(name)`
  - 按名称模式搜索生物体
  - 返回：匹配生物体代码列表

- `lookfor_pathway(name)`
  - 按名称搜索途径
  - 返回：途径 ID 列表

- `get_pathway_by_gene(gene_id, organism)`
  - 查找包含基因 
 的通路 - 返回：通路 ID 列表 

- `parse_kgml_pathway(pathway_id)`
  - 解析通路 KGML 以进行交互
  - 返回：包含“条目”和“关系”的字典 

- `pathway2sif(pathway_id)`
  - 提取简单交互格式数据
  - 激活/抑制过滤器
  - 返回：交互元组列表

* *生物体代码：**
- hsa：智人
- mmu：Mus musculus
- dme：果蝇
- sce：酿酒酵母
- eco：大肠杆菌

* *用例：**
- 通路分析和可视化
- 基因功能注释
- 代谢网络重建
- 蛋白质-蛋白质相互作用提取

- --

### HGNC（人类基因命名委员会）

官方人类基因命名Authority.

* *初始化：**
```python
from bioservices import HGNC
h = HGNC()
```

* *关键方法：**
- `search(query)`：搜索基因符号/名称
- `fetch(format, query)`：检索基因信息

* *使用案例：**
- 标准化人类基因名称
- 查找官方基因符号

- --

### MyGeneInfo

基因注释和查询服务。

* *初始化：**
```python
from bioservices import MyGeneInfo
m = MyGeneInfo()
```

* *Key方法：**
- `querymany(ids, scopes, fields, species)`：批量基因查询
- `getgene(geneid)`：获取基因注释

* *使用案例：**
- 批量基因注释检索
- 基因ID转换

- --

## 化学化合物资源

### ChEBI (Chemical Entities of Biological Interest)

分子实体词典.

* *初始化：**
```python
from bioservices import ChEBI
c = ChEBI()
```

* *关键方法：**
- `getCompleteEntity(chebi_id)`：完整化合物信息
- `getLiteEntity(chebi_id)`：基本信息
- `getCompleteEntityByList(chebi_ids)`：批量检索

* *使用案例：**
- 小分子信息
- 化学结构数据
- 化合物性质查找

- --

### ChEMBL

生物活性药物样化合物数据库.

* *初始化：**
```python
from bioservices import ChEMBL
c = ChEMBL()
```

* *关键方法：**
- `get_molecule_form(chembl_id)`：化合物详细信息
- `get_target(chembl_id)`：目标信息
- `get_similarity(chembl_id)`：获取给定 
- `get_assays()`：生物测定数据

* *使用案例：**
- 药物发现数据
- 查找类似化合物 
- 生物活性信息
- 目标化合物关系

- --

### UniChem

化学标识符映射服务。

* *初始化：**
```python
from bioservices import UniChem
u = UniChem()
```

* *关键方法：**
- `get_compound_id_from_kegg(kegg_id)`：KEGG → ChEMBL
- `get_all_compound_ids(src_compound_id, src_id)`：获取全部IDs
- `get_src_compound_ids(src_compound_id, from_src_id, to_src_id)`：转换 IDs

* *源 ID：**
- 1：ChEMBL
- 2：DrugBank
- 3：PDB
- 6：KEGG
- 7： ChEBI
- 22：PubChem

* *用例：**
- 跨数据库化合物 ID 映射
- 链接化学数据库

- --

### PubChem

化学化合物数据库NIH.

* *初始化：**
```python
from bioservices import PubChem
p = PubChem()
```

* *关键方法：**
- `get_compounds(identifier, namespace)`：检索化合物
- `get_properties(properties, identifier, namespace)`：获取属性

* *使用案例：**
- 化学结构检索
- 化合物属性信息

- --

## 序列分析工具

### NCBIblast

序列相似性搜索.

* *初始化：**
```python
from bioservices import NCBIblast
s = NCBIblast(verbose=False)
```

* *关键方法：**
- `run(program, sequence, stype, database, email, **params)`
  - 提交BLAST作业
  - `program`: "blastp", "blastn", “blastx”、“tblastn”、“tblastx”
  - `stype`：“蛋白质”或“DNA”
  - `database`：“uniprotkb”、“pdb”、“refseq_蛋白质”等。
  - `email`：需要NCBI
  - 返回：作业 ID

- `getStatus(jobid)`
  - 检查作业状态
  - 返回：“RUNNING”、“FINISHED”、“ERROR”

- `getResult(jobid, result_type)`
  - 检索结果
  - `result_type`：“out”（默认）、“ids”、“xml”

* *重要：** BLAST 作业是异步的。在检索结果之前始终检查状态。

* *用例：**
- 蛋白质同源性搜索
- 序列相似性分析
- 同源性功能注释

- --

## 通路和相互作用资源

### Reactome

Pathway数据库.

* *初始化：**
```python
from bioservices import Reactome
r = Reactome()
```

* *关键方法：**
- `get_pathway_by_id(pathway_id)`：路径详细信息
- `search_pathway(query)`：搜索路径

* *使用案例：**
- 人类通路分析
- 生物过程注释

- --

### PSICQUIC

蛋白质相互作用查询服务（联邦30+ 

* *初始化：**
```python
from bioservices import PSICQUIC
s = PSICQUIC()
```

* *关键方法：**
- `query(database, query_string)`
  - 查询具体交互数据库
  - 返回：PSI-MI TAB 格式

- `activeDBs`
  - 属性列表可用数据库
  - 返回：数据库名称列表

* *可用数据库：** MINT、IntAct、BioGRID、DIP、InnateDB、MatrixDB、MPIDB、UniProt 和 30 多个

* *查询语法：** 支持 AND、OR、species过滤器
- 示例：“ZAP70 AND物种：9606”

* *用例：**
- 蛋白质-蛋白质相互作用发现
- 网络分析
- 相互作用组映射

- --

### IntactComplex

蛋白质复合物数据库。

* *初始化：**
```python
from bioservices import IntactComplex
i = IntactComplex()
```

* *关键方法：**
- `search(query)`：搜索复合物
- `details(complex_ac)`：复合物详情

* *使用案例：**
- 蛋白质复合物组成
- 多蛋白质组装分析

- --

### OmniPath

整合信号通路数据库.

* *初始化：**
```python
from bioservices import OmniPath
o = OmniPath()
```

* *关键方法：**
- `interactions(datasets, organisms)`：获取交互
- `ptms(datasets, organisms)`：翻译后修改

* *使用案例：**
- 细胞信号分析
- 调控网络映射

- --

## 基因本体

### QuickGO

基因本体注释服务。

* *初始化：**
```python
from bioservices import QuickGO
g = QuickGO()
```

* *关键方法：**
- `Term(go_id, frmt="obo")`
  - 检索GO术语信息
  - 返回：术语定义和元数据

- `Annotation(protein=None, goid=None, format="tsv")`
  - 获取 GO 注释
  - 返回：按请求格式的注释

* *GO 类别：**
- 生物过程 (BP)
- 分子功能 (MF)
- 细胞成分 (CC)

* *使用案例：**
- 功能注释
- 富集分析
- GO术语查找

- --

## 基因组资源

### BioMart

基因组数据挖掘工具data.

* *初始化：**
```python
from bioservices import BioMart
b = BioMart()
```

* *关键方法：**
- `datasets(dataset)`：列出可用数据集
- `attributes(dataset)`：列出属性
- `query(query_xml)`：执行BioMart查询

* *用例：**
- 批量基因组数据检索
- 自定义基因组注释
- SNP信息

- --

### ArrayExpress

基因表达数据库.

* *初始化：**
```python
from bioservices import ArrayExpress
a = ArrayExpress()
```

* *关键方法：**
- `queryExperiments(keywords)`：搜索实验
- `retrieveExperiment(accession)`：获取实验数据

* *使用案例：**
- 基因表达数据
- 微阵列分析
- RNA-seq 数据检索

- --

### ENA (欧洲核苷酸档案)

核苷酸序列数据库.

* *初始化：**
```python
from bioservices import ENA
e = ENA()
```

* *关键方法：**
- `search_data(query)`：搜索序列
- `retrieve_data(accession)`：检索序列

* *使用案例：**
- 核苷酸序列检索
- 基因组组装获取

- --

## 结构生物学

### PDB（蛋白质数据库）

3D 蛋白质结构数据库.

* *初始化：**
```python
from bioservices import PDB
p = PDB()
```

* *关键方法：**
- `get_file(pdb_id, file_format)`：下载结构文件
- `search(query)`：搜索结构

* *文件格式：** pdb、cif、 xml

* *用例：**
- 3D 结构检索
- 基于结构的分析
- PyMOL 可视化

- --

### Pfam

蛋白质家族数据库.

* *初始化：**
```python
from bioservices import Pfam
p = Pfam()
```

* *关键方法：**
- `searchSequence(sequence)`：按顺序查找域
- `getPfamEntry(pfam_id)`：域信息

* *用例：**
- 蛋白质结构域识别
- 家族分类
- 功能基序发现

- --

## 专业资源

### BioModels

系统生物学模型repository.

* *初始化：**
```python
from bioservices import BioModels
b = BioModels()
```

* *关键方法：**
- `get_model_by_id(model_id)`：检索SBML模型

* *用例：**
- 系统生物学建模
- SBML模型检索

- --

### COG (Clusters of Orthologous Genes)

直系同源基因分类。

* *初始化:**
```python
from bioservices import COG
c = COG()
```

* *用例:**
- Orthology分析
- 功能分类

- --

### BiGG Models

代谢网络模型。

* *初始化：**
```python
from bioservices import BiGG
b = BiGG()
```

* *关键方法：**
- `list_models()`：可用型号
- `get_model(model_id)`：型号详细信息

* *使用案例：**
- 代谢网络分析
- 通量平衡分析

- --

## 一般模式

### 错误处理

所有服务可能会抛出异常。将调用包装在try- except中：

```python
try:
    result = service.method(params)
    if result:
        # Process result
        pass
except Exception as e:
    print(f"Error: {e}")
```

### Verbosity Control

大多数服务支持`verbose`参数：
```python
service = Service(verbose=False)  # Suppress HTTP logs
```

### Rate Limiting

服务有超时和速率限制：
```python
service.TIMEOUT = 30  # Adjust timeout
service.DELAY = 1     # Delay between requests (if supported)
```

### 输出格式

常用格式参数：
- `frmt`: "xml", "json", "tab", "txt", "fasta" 
- `format`: 服务特定变体

### 缓存

一些服务缓存结果：
```python
service.CACHE = True  # Enable caching
service.clear_cache()  # Clear cache
```

## 其他资源

有关详细的API文档：
- 官方文档：https://bioservices.readthedocs.io/
- 从main链接的各个服务文档page
- 源代码：https://github.com/coelaer/bioservices
