# 元数据提取指南

使用各种 API 和服务从 DOI、PMID、arXiv ID 和 URL 中提取准确的引文元数据的综合指南。

## 概述

准确的元数据对于正确的引文至关重要。本指南涵盖：
- 识别论文标识符（DOI、PMID、arXiv ID）
- 查询元数据 API（CrossRef、PubMed、arXiv、DataCite）
- 按条目类型所需的 BibTeX 字段
- 处理边缘情况和特殊情况
- 验证提取的内容元数据

## 论文标识符

### DOI（数字对象标识符）

* *格式**：`10.XXXX/suffix`

* *示例**：
```
10.1038/s41586-021-03819-2    # Nature article
10.1126/science.aam9317       # Science article
10.1016/j.cell.2023.01.001    # Cell article
10.1371/journal.pone.0123456  # PLOS ONE article
```

* *属性**：
- 永久标识符
- 元数据最可靠
- 解析到当前位置
- 发布者指定的

* *哪里可以找到**：
- 文章首页
- 文章网页
- CrossRef，Google Scholar， PubMed
- 通常在出版商网站上突出显示

### PMID (PubMed ID)

* *格式**：8 位数字（通常）

* *示例**：
```
34265844
28445112
35476778
```

* *属性**：
- 特定于PubMed数据库
- 仅限生物医学文献
- 由NCBI分配ZXXQNL31QXZ-永久标识符

* *哪里可以找到**：
- PubMed 搜索结果
- PubMed 上的文章页面
- 经常出现在文章中 PDF 页脚
- PMC (PubMed Central)页面

### PMCID (PubMed Central) ID)

* *格式**：PMC 后跟数字

* *示例**：
```
PMC8287551
PMC7456789
```

* *属性**：
- PMC 中的免费全文文章
- PubMed 文章的子集
- 开放获取或作者手稿

### arXiv ID

* *格式**：YYMM.NNNNN 或存档/YYMMNNN

* *示例**：
```
2103.14030        # New format (since 2007)
2401.12345        # 2024 submission
arXiv:hep-th/9901001  # Old format
```

* *属性**：
- 预印本（不是同行评审）
- 物理、数学、CS、q-bio 等。
- 版本跟踪（v1、v2 等）
- 免费、开放访问

* *在哪里找到**：
- arXiv.org
- 之前经常引用出版物
- 论文PDF标题

### 其他标识符

* *ISBN**（书籍）：
```
978-0-12-345678-9
0-123-45678-9
```

* *arXiv类别**：
```
cs.LG    # Computer Science - Machine Learning
q-bio.QM # Quantitative Biology - Quantitative Methods
math.ST  # Mathematics - Statistics
```

## 元数据 API

### CrossRef API

* *DOI 的主要来源** - 期刊文章最全面的元数据。

* *基本 URL**：`https://api.crossref.org/works/`

* *不需要 API 密钥**，但推荐礼貌池：
- 将电子邮件添加到用户代理
- 变得更好service
- 无速率限制

#### 基本 DOI 查询

* *请求**：
```
GET https://api.crossref.org/works/10.1038/s41586-021-03819-2
```

* *响应**（简化）：
```json
{
  "message": {
    "DOI": "10.1038/s41586-021-03819-2",
    "title": ["Article title here"],
    "author": [
      {"given": "John", "family": "Smith"},
      {"given": "Jane", "family": "Doe"}
    ],
    "container-title": ["Nature"],
    "volume": "595",
    "issue": "7865",
    "page": "123-128",
    "published-print": {"date-parts": [[2021, 7, 1]]},
    "publisher": "Springer Nature",
    "type": "journal-article",
    "ISSN": ["0028-0836"]
  }
}
```

#### 字段可用

* *始终存在**：
- `DOI`：数字对象标识符
- `title`：文章标题（数组）
- `type`：内容类型（期刊文章、书籍章节等）

* *通常当前**：
- `author`：作者对象数组
- `container-title`：期刊/书籍标题
- `published-print`或`published-online`：出版日期
- `volume`，`issue`， `page`：出版物详细信息
- `publisher`：出版商名称

* *有时存在**：
- `abstract`：文章摘要
- `subject`：主题类别
- `ISSN`：期刊 ISSN
- `ISBN`：书籍 ISBN
- `reference`：参考文献列表
- `is-referenced-by-count`：引用计数

#### 内容类型

CrossRef `type` 字段值：
- `journal-article`：期刊文章
- `book-chapter`：书籍章节
- `book`：书籍
- `proceedings-article`：会议论文
- `posted-content`：预印本
- `dataset`：研究数据集
- `report`：技术报告
- `dissertation`：论文/论文

### PubMed 电子实用程序API

* *专门用于生物医学文献** - 使用 MeSH 术语策划元数据。

* *基本 URL**：`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

* *推荐 API 密钥**（免费）：
- 更高的速率限制
- 更好的性能

#### PMID元数据

* *步骤 1：Efetch 获取完整记录**

```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?
  db=pubmed&
  id=34265844&
  retmode=xml&
  api_key=YOUR_KEY
```

* *响应**：具有全面元数据的 XML

* *步骤 2：解析 XML**

 关键字段：
```xml
<PubmedArticle>
  <MedlineCitation>
    <PMID>34265844</PMID>
    <Article>
      <ArticleTitle>Title here</ArticleTitle>
      <AuthorList>
        <Author><LastName>Smith</LastName><ForeName>John</ForeName></Author>
      </AuthorList>
      <Journal>
        <Title>Nature</Title>
        <JournalIssue>
          <Volume>595</Volume>
          <Issue>7865</Issue>
          <PubDate><Year>2021</Year></PubDate>
        </JournalIssue>
      </Journal>
      <Pagination><MedlinePgn>123-128</MedlinePgn></Pagination>
      <Abstract><AbstractText>Abstract text here</AbstractText></Abstract>
    </Article>
  </MedlineCitation>
  <PubmedData>
    <ArticleIdList>
      <ArticleId IdType="doi">10.1038/s41586-021-03819-2</ArticleId>
      <ArticleId IdType="pmc">PMC8287551</ArticleId>
    </ArticleIdList>
  </PubmedData>
</PubmedArticle>
```

#### 唯一PubMed Fields

* *MeSH 术语**：受控词汇
```xml
<MeshHeadingList>
  <MeshHeading>
    <DescriptorName UI="D003920">Diabetes Mellitus</DescriptorName>
  </MeshHeading>
</MeshHeadingList>
```

* *出版物类型**：
```xml
<PublicationTypeList>
  <PublicationType UI="D016428">Journal Article</PublicationType>
  <PublicationType UI="D016449">Randomized Controlled Trial</PublicationType>
</PublicationTypeList>
```

* *拨款信息**：
```xml
<GrantList>
  <Grant>
    <GrantID>R01-123456</GrantID>
    <Agency>NIAID NIH HHS</Agency>
    <Country>United States</Country>
  </Grant>
</GrantList>
```

### arXiv API

* *物理、数学、CS、q-bio 预印本** - 免费、开放获取。

* *基本 URL**：`http://export.arxiv.org/api/query`

* *不需要 API 密钥**

#### arXiv ID元数据

* *请求**：
```
GET http://export.arxiv.org/api/query?id_list=2103.14030
```

* *响应**：Atom XML

```xml
<entry>
  <id>http://arxiv.org/abs/2103.14030v2</id>
  <title>Highly accurate protein structure prediction with AlphaFold</title>
  <author><name>John Jumper</name></author>
  <author><name>Richard Evans</name></author>
  <published>2021-03-26T17:47:17Z</published>
  <updated>2021-07-01T16:51:46Z</updated>
  <summary>Abstract text here...</summary>
  <arxiv:doi>10.1038/s41586-021-03819-2</arxiv:doi>
  <category term="q-bio.BM" scheme="http://arxiv.org/schemas/atom"/>
  <category term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
</entry>
```

#### 关键字段

- `id`：arXiv URL
- `title`：预印本标题
- `author`：作者列表
- `published`：第一版本日期
- `updated`：最新版本日期
- `summary`：摘要
- `arxiv:doi`：DOI（如果已发布）
- `arxiv:journal_ref`：期刊参考（如果已发布）
- `category`：arXiv 类别

#### 版本跟踪

arXiv 跟踪版本：
- `v1`：初始提交
- `v2`、`v3` 等：修订

* *始终检查**是否已在期刊中发表预印本（如果可用，请使用 DOI）。

### DataCite API

* *研究数据集、软件、其他输出** -为非传统学术著作分配 DOI。

* *基本 URL**：`https://api.datacite.org/dois/`

* *与 CrossRef** 类似，但适用于数据集、软件、代码等。

* *请求**：
```
GET https://api.datacite.org/dois/10.5281/zenodo.1234567
```

* *响应**：带有元数据的 JSON数据集/软件

## 必填 BibTeX 字段

### @article（期刊文章）

* *必填**：
- `author`：作者姓名
- `title`：文章标题
- `journal`：期刊名称
- `year`：出版年份

* *可选但推荐**：
- `volume`：卷号
- `number`：发行号
- `pages`：页面范围（例如，123--145）
- `doi`：数字对象标识符
- `url`：URL（如果没有） DOI
- `month`：出版物月

* *示例**：
```bibtex
@article{Smith2024,
  author  = {Smith, John and Doe, Jane},
  title   = {Novel Approach to Protein Folding},
  journal = {Nature},
  year    = {2024},
  volume  = {625},
  number  = {8001},
  pages   = {123--145},
  doi     = {10.1038/nature12345}
}
```

### @book（书籍）

* *必填**：
- `author` 或 `editor`：作者或编辑 
- `title`：书名
- `publisher`：出版商名称
- `year`：出版物年

* *可选但推荐**：
- `edition`：版本号（如果不是第一个）
- `address`：发布者位置
- `isbn`：ISBN
- `url`： URL
- `series`：系列名称

* *示例**：
```bibtex
@book{Kumar2021,
  author    = {Kumar, Vinay and Abbas, Abul K. and Aster, Jon C.},
  title     = {Robbins and Cotran Pathologic Basis of Disease},
  publisher = {Elsevier},
  year      = {2021},
  edition   = {10},
  isbn      = {978-0-323-53113-9}
}
```

### @inproceedings（会议论文）

* *必填**：
- `author`：作者名称
- `title`：论文标题
- `booktitle`：会议/论文集名称
- `year`：年份

* *可选但推荐**：
- `pages`：页面范围
- `organization`：组织机构
- `publisher`：发布者
- `address`：会议地点
- `month`：会议月份
- `doi`：DOI如果可用

* *示例**：
```bibtex
@inproceedings{Vaswani2017,
  author    = {Vaswani, Ashish and Shazeer, Noam and others},
  title     = {Attention is All You Need},
  booktitle = {Advances in Neural Information Processing Systems},
  year      = {2017},
  pages     = {5998--6008},
  volume    = {30}
}
```

### @incollection（图书章节）

* *必填**：
- `author`：章节作者
- `title`：章节title
- `booktitle`：书名
- `publisher`：出版商名称
- `year`：出版年份

* *可选但推荐**：
- `editor`：书籍编辑者
- `pages`：章节页码范围
- `chapter`：章节编号
- `edition`：版本
- `address`：出版商位置

* *示例**：
```bibtex
@incollection{Brown2020,
  author    = {Brown, Peter O. and Botstein, David},
  title     = {Exploring the New World of the Genome with {DNA} Microarrays},
  booktitle = {DNA Microarrays: A Molecular Cloning Manual},
  editor    = {Eisen, Michael B. and Brown, Patrick O.},
  publisher = {Cold Spring Harbor Laboratory Press},
  year      = {2020},
  pages     = {1--45}
}
```

### @phdthesis（论文）

* *必填**：
- `author`：作者姓名
- `title`：论文标题
- `school`：机构
- `year`：年份

* *可选**：
- `type`：类型（例如“博士论文”）
- `address`：机构位置
- `month`：月份
- `url`：URL

  * *示例**：
```bibtex
@phdthesis{Johnson2023,
  author = {Johnson, Mary L.},
  title  = {Novel Approaches to Cancer Immunotherapy},
  school = {Stanford University},
  year   = {2023},
  type   = {{PhD} dissertation}
}
```

### @misc（预印本，软件，数据集）

* *必填**：
- `author`：作者
- `title`：标题
- `year`：年份

* *对于预印本，添加**：
- `howpublished`：存储库（例如“bioRxiv”）
- `doi`：预印本 DOI
- `note`：预印本 ID

  * *示例（预印本）**：
```bibtex
@misc{Zhang2024,
  author       = {Zhang, Yi and Chen, Li and Wang, Hui},
  title        = {Novel Therapeutic Targets in Alzheimer's Disease},
  year         = {2024},
  howpublished = {bioRxiv},
  doi          = {10.1101/2024.01.001},
  note         = {Preprint}
}
```

* *示例（软件）**：
```bibtex
@misc{AlphaFold2021,
  author       = {DeepMind},
  title        = {{AlphaFold} Protein Structure Database},
  year         = {2021},
  howpublished = {Software},
  url          = {https://alphafold.ebi.ac.uk/},
  doi          = {10.5281/zenodo.5123456}
}
```

## 提取工作流程

### 来自 DOI

* *最佳实践** - 最可靠来源：

```bash
# Single DOI
python scripts/extract_metadata.py --doi 10.1038/s41586-021-03819-2

# Multiple DOIs
python scripts/extract_metadata.py \
  --doi 10.1038/nature12345 \
  --doi 10.1126/science.abc1234 \
  --output refs.bib
```

* *过程**：
1. 使用 DOI
2 查询 CrossRef API。解析 JSON 响应
3. 提取所需字段
4. 确定条目类型（@article、@book 等）
5. 格式为 BibTeX
6. 验证完整性

### 来自 PMID

* *对于生物医学文献**：

```bash
# Single PMID
python scripts/extract_metadata.py --pmid 34265844

# Multiple PMIDs
python scripts/extract_metadata.py \
  --pmid 34265844 \
  --pmid 28445112 \
  --output refs.bib
```

* *过程**：
1. 使用 PMID
2 查询 PubMed EFetch。解析 XML 响应
3. 提取包括 MeSH 术语 
4 的元数据。检查响应中的 DOI 
5. 如果 DOI 存在，可选择查询 CrossRef 以获取其他元数据
6. 格式为 BibTeX

### 来自 arXiv ID

* *用于预印本**：

```bash
python scripts/extract_metadata.py --arxiv 2103.14030
```

* *过程**：
1. 使用 ID
2 查询 arXiv API。解析 Atom XML 响应
3. 检查已发布版本（响应中的 DOI）
4. 如果已发布：使用 DOI 和 CrossRef
5. 如果未发布：使用预印本元数据
6. 格式为@misc，带有预印本注释

* *重要**：始终检查预印本是否已发布！

### 来自URL

* *当您只有URL**时：

```bash
python scripts/extract_metadata.py \
  --url "https://www.nature.com/articles/s41586-021-03819-2"
```

* *处理**：
1. 解析 URL 以提取标识符 
2. 识别类型（DOI、PMID、arXiv）
3. 从 URL
4 中提取标识符。查询相应的API
5. 格式为 BibTeX

* *URL 模式**：
```
# DOI URLs
https://doi.org/10.1038/nature12345
https://dx.doi.org/10.1126/science.abc123
https://www.nature.com/articles/s41586-021-03819-2

# PubMed URLs
https://pubmed.ncbi.nlm.nih.gov/34265844/
https://www.ncbi.nlm.nih.gov/pubmed/34265844

# arXiv URLs
https://arxiv.org/abs/2103.14030
https://arxiv.org/pdf/2103.14030.pdf
```

### 批处理

* *来自具有混合标识符的文件**：

```bash
# Create file with one identifier per line
# identifiers.txt:
#   10.1038/nature12345
#   34265844
#   2103.14030
#   https://doi.org/10.1126/science.abc123

python scripts/extract_metadata.py \
  --input identifiers.txt \
  --output references.bib
```

* *处理**：
- 脚本自动检测标识符类型
- 查询适当的API
- 将所有内容合并到单个BibTeX文件中
- 优雅地处理错误

## 特殊情况和边缘情况

### 预印本稍后发布

* *问题**：引用预印本，但现在是期刊版本可用.

* *解**：
1. 检查 arXiv 元数据中的 DOI 字段
2. 如果存在 DOI，请使用已发布的版本 
3. 更新对期刊文章 
4 的引用。如果需要，请在评论中注明预印本版本

* *示例**：
```bibtex
% Originally: arXiv:2103.14030
% Published as:
@article{Jumper2021,
  author  = {Jumper, John and Evans, Richard and others},
  title   = {Highly Accurate Protein Structure Prediction with {AlphaFold}},
  journal = {Nature},
  year    = {2021},
  volume  = {596},
  pages   = {583--589},
  doi     = {10.1038/s41586-021-03819-2}
}
```

### 多个作者（等）

* *问题**：许多作者（10+）。

* *BibTeX实践**：
- 包括所有作者，如果<10
- 使用“和其他”表示 10+
- 或列出所有（期刊有所不同）

* *示例**：
```bibtex
@article{LargeCollaboration2024,
  author = {First, Author and Second, Author and Third, Author and others},
  ...
}
```

### 作者姓名变体

* *问题**：作者以不同名称发表格式。

* *标准化**：
```
# Common variations
John Smith
John A. Smith
John Andrew Smith
J. A. Smith
Smith, J.
Smith, J. A.

# BibTeX format (recommended)
author = {Smith, John A.}
```

* *提取首选项**：
1. 如果可用，请使用全名 
2. 如果可用，请包括中间名首字母 
3. 格式：最后，第一个中间

### 没有可用的DOI

* *问题**：没有DOI的较旧论文或书籍。

* *解决方案**：
1. 如果可用，请使用 PMID（生物医学）
2. 书籍使用 ISBN 
3. 使用 URL 获取稳定源 
4. 包括完整的出版物详细信息

* *示例**：
```bibtex
@article{OldPaper1995,
  author  = {Author, Name},
  title   = {Title Here},
  journal = {Journal Name},
  year    = {1995},
  volume  = {123},
  pages   = {45--67},
  url     = {https://stable-url-here},
  note    = {PMID: 12345678}
}
```

### 会议论文与期刊文章

* *问题**：在两者中发表的相同工作。

* *最佳实践**：
- 如果两者都引用期刊版本可用
- 期刊版本已存档
- 会议版本的时效性

* *如果引用会议**：
```bibtex
@inproceedings{Smith2024conf,
  author    = {Smith, John},
  title     = {Title},
  booktitle = {Proceedings of NeurIPS 2024},
  year      = {2024}
}
```

* *如果引用期刊**：
```bibtex
@article{Smith2024journal,
  author  = {Smith, John},
  title   = {Title},
  journal = {Journal of Machine Learning Research},
  year    = {2024}
}
```

### 书籍章节vs 编辑收藏

* *正确提取**：
- 章节：使用 `@incollection`
- 整本书：使用 `@book`
- 书籍编辑：在 `editor` 字段中列出
- 章节作者：在中列出`author` 字段

### 数据集和软件

* *使用@misc** 与适当的字段：

```bibtex
@misc{DatasetName2024,
  author       = {Author, Name},
  title        = {Dataset Title},
  year         = {2024},
  howpublished = {Zenodo},
  doi          = {10.5281/zenodo.123456},
  note         = {Version 1.2}
}
```

## 提取后验证

始终验证提取的元数据：

```bash
python scripts/validate_citations.py extracted_refs.bib
```

* *检查**：
- 存在所有必填字段
- DOI 正确解析
- 作者姓名格式一致
- 年份合理（4 位数字）
- 期刊/出版商名称正确的
- 页面范围使用--不是-
- 正确处理特殊字符

## 最佳实践

### 1. 在可用时首选 DOI

DO 提供：
- 永久标识符
- 最佳元数据源
- 发布者验证的信息
- 可解析链接

### 2. 验证自动提取元数据

抽查：
- 作者姓名匹配出版物
- 标题匹配（包括大小写）
- 年份正确
- 期刊名称完整

### 3. 处理特殊字符

* *LaTeX 特殊字符**：
- 保护大写：`{AlphaFold}`
- 处理重音符号：`M{\"u}ller` 或使用 Unicode
- 化学式：`H$_2$O` 或 `\ce{H2O}`

### 4. 使用一致的引文关键字

* *约定**： `FirstAuthorYEARkeyword`
```
Smith2024protein
Doe2023machine
Johnson2024cancer
```

### 5. 包含现代论文的 DOI

~2000 年之后发表的所有论文均应包含 DOI：
```bibtex
doi = {10.1038/nature12345}
```

### 6. 文档来源

，对于非标准来源，添加注释：
```bibtex
note = {Preprint, not peer-reviewed}
note = {Technical report}
note = {Dataset accompanying [citation]}
```

## 总结

元数据提取工作流程：

1. **识别**：确定标识符类型（DOI、PMID、arXiv、URL）
2. **查询**：使用适当的 API（CrossRef、PubMed、arXiv）
3. **提取**：解析所需字段的响应
4. **格式**：创建格式正确的 BibTeX 条目
5. **验证**：检查完整性和准确性
6. **验证**：抽查关键引文

* *使用脚本**进行自动化：
- `extract_metadata.py`：通用提取器
- `doi_to_bibtex.py`：快速DOI转换
- `validate_citations.py`：验证准确性

* *始终在最终提交之前验证**提取的元数据！
