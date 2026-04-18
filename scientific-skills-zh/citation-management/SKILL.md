---
name: citation-management
description: 学术研究的综合引文管理。在 Google Scholar 和 PubMed 中搜索论文、提取准确的元数据、验证引文并生成格式正确的 BibTeX 条目。当您需要查找论文、验证引文信息、将 DOI 转换为 BibTeX 或确保科学写作中的参考准确性时，应该使用此技能。
allowed-tools: Read Write Edit Bash
license: MIT License
metadata:
    skill-author: K-Dense Inc.
---

# 引文管理

## 概述

在整个研究和写作过程中系统地管理引文。该技能提供了搜索学术数据库（Google Scholar、PubMed）、从多个来源（CrossRef、PubMed、arXiv）提取准确元数据、验证引文信息以及生成格式正确的 BibTeX 条目的工具和策略。

 对于保持引文准确性、避免参考错误和确保可重复研究至关重要。与 literature-review 技能无缝集成，实现全面的研究工作流程。

## 何时使用此技能

在以下情况下使用此技能：
- 在 Google Scholar 或 PubMed 上搜索特定论文
- 将 DOI、PMID 或 arXiv ID 转换为正确格式的 BibTeX
- 提取引文的完整元数据（作者、标题、期刊、年份等）
- 验证现有引文的准确性
- 清理和格式化 BibTeX 文件
- 查找特定领域中被高度引用的论文
- 验证引文信息是否与实际出版物相匹配
- 为手稿或文章建立参考书目论文
- 检查重复引文
- 确保一致的引文格式

## 科学示意图的视觉增强

* *使用此技能创建文档时，始终考虑添加科学图表和示意图以增强视觉传达。**

如果您的文档尚未包含示意图或图表：
- 使用 **scientific-schematics** 技能生成人工智能驱动的出版质量图表
- 用自然语言简单描述您想要的图表
- Nano Banana Pro 将自动生成、审查和完善原理图

* *对于新文档：**默认情况下应生成科学原理图，以直观地表示文本中描述的关键概念、工作流程、架构或关系。

* *如何生成原理图：**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

AI将自动：
- 创建具有适当格式的出版质量图像
- 通过多个审查和完善迭代
- 确保可访问性（色盲友好，高对比度）
- 将输出保存在图形/目录中

* *何时添加原理图：**
- 引文工作流程图
- 文献检索方法流程图
- 参考管理系统架构
- 引文风格决策树
- 数据库集成图
- 任何受益于可视化的复杂概念

有关创建原理图的详细指导，请参阅scientific-schematics 技能文档。

- --

## 核心工作流程

引文管理遵循系统化流程：

### 阶段1：论文发现和搜索

* *目标**：使用学术搜索引擎查找相关论文。

#### 谷歌学术搜索

谷歌学术搜索提供最全面的跨学科覆盖。

* *基本搜索**：
```bash
# Search for papers on a topic
python scripts/search_google_scholar.py "CRISPR gene editing" \
  --limit 50 \
  --output results.json

# Search with year filter
python scripts/search_google_scholar.py "machine learning protein folding" \
  --year-start 2020 \
  --year-end 2024 \
  --limit 100 \
  --output ml_proteins.json
```

* *高级搜索策略**（参见 `references/google_scholar_search.md`）：
- 对精确短语使用引号：`"deep learning"`
- 按作者搜索：`author:LeCun`
- 在标题中搜索：`intitle:"neural networks"`
- 排除术语： `machine learning -survey`
- 使用排序选项查找高被引论文
- 按日期范围过滤以获取最近的工作

* *最佳实践**：
- 使用特定的、有针对性的搜索词
- 包括关键技术术语和首字母缩略词
- 按近年来过滤快速移动字段
- 检查“引用者”以查找开创性论文
- 导出热门结果以供进一步分析

#### PubMed 搜索

PubMed 专门研究生物医学和生命科学文献（35+ 百万次引用）。

* *基本搜索**：
```bash
# Search PubMed
python scripts/search_pubmed.py "Alzheimer's disease treatment" \
  --limit 100 \
  --output alzheimers.json

# Search with MeSH terms and filters
python scripts/search_pubmed.py \
  --query '"Alzheimer Disease"[MeSH] AND "Drug Therapy"[MeSH]' \
  --date-start 2020 \
  --date-end 2024 \
  --publication-types "Clinical Trial,Review" \
  --output alzheimers_trials.json
```

* *高级 PubMed 查询**（参见 `references/pubmed_search.md`）：
- 使用 MeSH 术语：`"Diabetes Mellitus"[MeSH]`
- 字段标签：`"cancer"[Title]`， `"Smith J"[Author]`
- 布尔运算符：`AND`、`OR`、`NOT`
- 日期过滤器：`2020:2024[Publication Date]`
- 发布类型：`"Review"[Publication Type]`
- 与 E-utilities API 结合使用自动化

* *最佳实践**：
- 使用 MeSH 浏览器查找正确的受控词汇
- 首先在 PubMed 高级搜索生成器中构建复杂查询
- 使用 OR
 包含多个同义词- 检索 PMID 以轻松元数据提取
- 导出到 JSON 或直接导出到BibTeX

### 第 2 阶段：元数据提取

* *目标**：将论文标识符（DOI、PMID、arXiv ID）转换为完整、准确的元数据。

#### 快速 DOI 到 BibTeX 转换

对于单个 DOI，请使用快速转换工具：

```bash
# Convert single DOI
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2

# Convert multiple DOIs from a file
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib

# Different output formats
python scripts/doi_to_bibtex.py 10.1038/nature12345 --format json
```

#### 综合元数据提取

对于 DOI、PMID、arXiv ID 或 URL：

```bash
# Extract from DOI
python scripts/extract_metadata.py --doi 10.1038/s41586-021-03819-2

# Extract from PMID
python scripts/extract_metadata.py --pmid 34265844

# Extract from arXiv ID
python scripts/extract_metadata.py --arxiv 2103.14030

# Extract from URL
python scripts/extract_metadata.py --url "https://www.nature.com/articles/s41586-021-03819-2"

# Batch extraction from file (mixed identifiers)
python scripts/extract_metadata.py --input identifiers.txt --output citations.bib
```

* *元数据源**（请参阅`references/metadata_extraction.md`）：

1. **CrossRef API**：DOIs 的主要来源
  - 期刊文章的综合元数据
  - 出版商提供的信息
  - 包括作者、标题、期刊、卷、页数、日期
  - 免费，无需 API 密钥

2. **PubMed 电子实用程序**：生物医学文献
  - 官方 NCBI 元数据
  - 包括 MeSH 术语、摘要
  - PMID 和 PMCID 标识符
  - 免费，推荐用于高容量的 API 密钥

3. **arXiv API**：物理、数学、CS、q-bio 中的预印本
  - 预印本的完整元数据
  - 版本跟踪
  - 作者关系
  - 免费、开放访问

4. **DataCite API**：研究数据集、软件和其他资源
  - 非传统学术成果的元数据
  - 数据集和代码的 DOI
  - 免费访问

* *提取内容**：
- **必填字段**：作者、标题、年份
- **期刊文章**：期刊、卷、编号、页数、DOI
- **书籍**：出版商、ISBN、版本
- **会议论文**：书名、会议地点、页数
- **预印本**：存储库（arXiv，bioRxiv），预印本 ID
- **附加**：摘要、关键字、URL

### 第 3 阶段：BibTeX 格式化

* *目标**：生成干净、格式正确的 BibTeX 条目。

#### 了解 BibTeX 条目类型

完整信息请参阅 `references/bibtex_formatting.md` guide.

* *常见条目类型**：
- `@article`：期刊文章（最常见）
- `@book`：书籍
- `@inproceedings`：会议论文
- `@incollection`：书籍章节
- `@phdthesis`：论文
- `@misc`：预印本、软件、数据集

* *按类型划分的必填字段**：

```bibtex
@article{citationkey,
  author  = {Last1, First1 and Last2, First2},
  title   = {Article Title},
  journal = {Journal Name},
  year    = {2024},
  volume  = {10},
  number  = {3},
  pages   = {123--145},
  doi     = {10.1234/example}
}

@inproceedings{citationkey,
  author    = {Last, First},
  title     = {Paper Title},
  booktitle = {Conference Name},
  year      = {2024},
  pages     = {1--10}
}

@book{citationkey,
  author    = {Last, First},
  title     = {Book Title},
  publisher = {Publisher Name},
  year      = {2024}
}
```

#### 格式化和清理

使用用于标准化 BibTeX 文件的格式化程序：

```bash
# Format and clean BibTeX file
python scripts/format_bibtex.py references.bib \
  --output formatted_references.bib

# Sort entries by citation key
python scripts/format_bibtex.py references.bib \
  --sort key \
  --output sorted_references.bib

# Sort by year (newest first)
python scripts/format_bibtex.py references.bib \
  --sort year \
  --descending \
  --output sorted_references.bib

# Remove duplicates
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --output clean_references.bib

# Validate and report issues
python scripts/format_bibtex.py references.bib \
  --validate \
  --report validation_report.txt
```

* *格式化操作**：
- 标准化字段顺序
- 一致的缩进和间距
- 标题中正确的大写（受 {} 保护）
- 标准化作者姓名格式
- 一致的引文关键字格式
- 删除不必要的字段
- 修复常见错误（缺少逗号、大括号）

### 第 4 阶段：引文验证

* *目标**：验证所有引文是否准确且完整。

#### 综合验证

```bash
# Validate BibTeX file
python scripts/validate_citations.py references.bib

# Validate and fix common issues
python scripts/validate_citations.py references.bib \
  --auto-fix \
  --output validated_references.bib

# Generate detailed validation report
python scripts/validate_citations.py references.bib \
  --report validation_report.json \
  --verbose
```

* *验证检查**（参见`references/citation_validation.md`）：

1. **DOI 验证**：
  - DOI 通过 doi.org 正确解析
  - BibTeX 和 CrossRef
 之间的元数据匹配 - 没有损坏或无效的 DOIs

2. **必填字段**：
  - 条目类型的所有必填字段
  - 无空或缺失的关键信息
  - 作者姓名格式正确

3. **数据一致性**：
  - 年份有效（4位数字，合理范围）
  - 数量/数量为数字
  - 页面格式正确（例如，123--145）
  - URL可访问

4. **重复检测**：
  - 多次使用相同的 DOI
  - 相似的标题（可能重复）
  - 相同的作者/年份/标题组合

5. **格式合规性**：
  - 有效的 BibTeX 语法
  - 正确的大括号和引号
  - 引文键是唯一的
  - 正确处理特殊字符

  * *验证输出**：
```json
{
  "total_entries": 150,
  "valid_entries": 145,
  "errors": [
    {
      "citation_key": "Smith2023",
      "error_type": "missing_field",
      "field": "journal",
      "severity": "high"
    },
    {
      "citation_key": "Jones2022",
      "error_type": "invalid_doi",
      "doi": "10.1234/broken",
      "severity": "high"
    }
  ],
  "warnings": [
    {
      "citation_key": "Brown2021",
      "warning_type": "possible_duplicate",
      "duplicate_of": "Brown2021a",
      "severity": "medium"
    }
  ]
}
```

### 第 5 阶段：集成与写作工作流程

#### 为手稿构建参考文献

创建参考书目的完整工作流程：

```bash
# 1. Search for papers on your topic
python scripts/search_pubmed.py \
  '"CRISPR-Cas Systems"[MeSH] AND "Gene Editing"[MeSH]' \
  --date-start 2020 \
  --limit 200 \
  --output crispr_papers.json

# 2. Extract DOIs from search results and convert to BibTeX
python scripts/extract_metadata.py \
  --input crispr_papers.json \
  --output crispr_refs.bib

# 3. Add specific papers by DOI
python scripts/doi_to_bibtex.py 10.1038/nature12345 >> crispr_refs.bib
python scripts/doi_to_bibtex.py 10.1126/science.abcd1234 >> crispr_refs.bib

# 4. Format and clean the BibTeX file
python scripts/format_bibtex.py crispr_refs.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output references.bib

# 5. Validate all citations
python scripts/validate_citations.py references.bib \
  --auto-fix \
  --report validation.json \
  --output final_references.bib

# 6. Review validation report and fix any remaining issues
cat validation.json

# 7. Use in your LaTeX document
# \bibliography{final_references}
```

#### 与文献复习技能集成

此技能补充了`literature-review`技能：

* *文献复习技能** → 系统检索与综合
* *引文管理技能** → 技术引文处理

* *组合工作流程**：
1. 使用`literature-review`进行全面的多数据库搜索
2. 使用 `citation-management` 提取并验证所有引文 
3. 使用 `literature-review` 来综合主题 
4 的发现。使用 `citation-management` 验证最终参考书目准确性

```bash
# After completing literature review
# Verify all citations in the review document
python scripts/validate_citations.py my_review_references.bib --report review_validation.json

# Format for specific citation style if needed
python scripts/format_bibtex.py my_review_references.bib \
  --style nature \
  --output formatted_refs.bib
```

## 搜索策略

### Google Scholar 最佳实践

* *查找具有影响力的论文**（关键）：

 始终根据引用对论文进行优先级排序计数、场地质量和作者声誉：

* *引用计数阈值：**
|纸时代|引文|分类|
|---------|------------------------|----------------|
| 0-3岁| 20+ |值得注意|
| 0-3岁| 100+ |极具影响力|
| 3-7年| 100+ |重要|
| 3-7年| 500+ |地标纸|
| 7 年以上 | 500+ |开创性工作|
| 7 年以上 | 1000+ |基础 |

* *场地质量等级：**
- **第 1 级（首选）：** Nature、Science、Cell、NEJM、Lancet、JAMA、PNAS
- **第 2 级（高优先级）：** 影响因子 >10，顶级会议（NeurIPS、ICML、ICLR）
- **第 3 级（良好）：** 专业期刊 (IF 5-10)
- **第 4 级（谨慎）：** 影响较小的同行评审场所

* *作者声誉指标：**
- h 指数 >40
- 高级研究人员在第 1 级场所发表多篇出版物
- 受认可机构的领导力
- 奖项和编辑职位

* *高影响力论文的搜索策略：**
- 按引用计数排序（引用最多的在前）
- 查找来自一级期刊的评论文章以了解概述
- 检查“引用者”以进行影响评估和最近的后续工作
- 使用引文警报来跟踪新的引用关键论文
- 使用`source:Nature`或`source:Science`
按顶级地点过滤-使用`author:LastName`

* *高级操作员**搜索已知领域领导者的论文**（完整列表在`references/google_scholar_search.md`):
```
"exact phrase"           # Exact phrase matching
author:lastname          # Search by author
intitle:keyword          # Search in title only
source:journal           # Search specific journal
-exclude                 # Exclude terms
OR                       # Alternative terms
2020..2024              # Year range
```

* *搜索示例**:
```
# Find recent reviews on a topic
"CRISPR" intitle:review 2023..2024

# Find papers by specific author on topic
author:Church "synthetic biology"

# Find highly cited foundational work
"deep learning" 2012..2015 sort:citations

# Exclude surveys and focus on methods
"protein folding" -survey -review intitle:method
```

### PubMed 最佳实践

* *使用 MeSH 术语**:
MeSH（医学主题）标题）提供受控词汇以进行精确搜索。

1. **在 https://meshb.nlm.nih.gov/search
2 查找 MeSH 术语**。 **在查询中使用**：`"Diabetes Mellitus, Type 2"[MeSH]`
3. **与关键字结合**以实现全面覆盖

* *字段标签**：
```
[Title]              # Search in title only
[Title/Abstract]     # Search in title or abstract
[Author]             # Search by author name
[Journal]            # Search specific journal
[Publication Date]   # Date range
[Publication Type]   # Article type
[MeSH]              # MeSH term
```

* *构建复杂查询**：
```bash
# Clinical trials on diabetes treatment published recently
"Diabetes Mellitus, Type 2"[MeSH] AND "Drug Therapy"[MeSH] 
AND "Clinical Trial"[Publication Type] AND 2020:2024[Publication Date]

# Reviews on CRISPR in specific journal
"CRISPR-Cas Systems"[MeSH] AND "Nature"[Journal] AND "Review"[Publication Type]

# Specific author's recent work
"Smith AB"[Author] AND cancer[Title/Abstract] AND 2022:2024[Publication Date]
```

* *用于自动化的E-utilities**：
脚本使用NCBI E-utilities API用于编程访问：
- **ESearch**：搜索和检索 PMID
- **EFetch**：检索完整元数据
- **ESummary**：获取摘要信息
- **ELink**：查找相关文章

有关完整 API，请参阅 `references/pubmed_search.md`文档.

## 工具和脚本

### search_google_scholar.py

搜索 Google 学术搜索并导出结果。

* *功能**：
- 带速率限制的自动搜索
- 分页支持
- 年份范围过滤
- 导出到 JSON 或 BibTeX
- 引用计数信息

* *用法**：
```bash
# Basic search
python scripts/search_google_scholar.py "quantum computing"

# Advanced search with filters
python scripts/search_google_scholar.py "quantum computing" \
  --year-start 2020 \
  --year-end 2024 \
  --limit 100 \
  --sort-by citations \
  --output quantum_papers.json

# Export directly to BibTeX
python scripts/search_google_scholar.py "machine learning" \
  --limit 50 \
  --format bibtex \
  --output ml_papers.bib
```

### search_pubmed.py

使用电子实用程序API搜索PubMed。

* *功能**：
- 复杂查询支持（MeSH、字段标签、布尔）
- 日期范围过滤
- 出版物类型过滤
- 使用元数据批量检索
- 导出到JSON或BibTeX

* *用法**：
```bash
# Simple keyword search
python scripts/search_pubmed.py "CRISPR gene editing"

# Complex query with filters
python scripts/search_pubmed.py \
  --query '"CRISPR-Cas Systems"[MeSH] AND "therapeutic"[Title/Abstract]' \
  --date-start 2020-01-01 \
  --date-end 2024-12-31 \
  --publication-types "Clinical Trial,Review" \
  --limit 200 \
  --output crispr_therapeutic.json

# Export to BibTeX
python scripts/search_pubmed.py "Alzheimer's disease" \
  --limit 100 \
  --format bibtex \
  --output alzheimers.bib
```

### extract_metadata.py

从论文中提取完整的元数据标识符。

* *功能**：
- 支持 DOI、PMID、arXiv ID、URL
- 查询 CrossRef、PubMed、arXiv API
- 处理多种标识符类型
- 批量处理
- 多个输出格式

* *用法**：
```bash
# Single DOI
python scripts/extract_metadata.py --doi 10.1038/s41586-021-03819-2

# Single PMID
python scripts/extract_metadata.py --pmid 34265844

# Single arXiv ID
python scripts/extract_metadata.py --arxiv 2103.14030

# From URL
python scripts/extract_metadata.py \
  --url "https://www.nature.com/articles/s41586-021-03819-2"

# Batch processing (file with one identifier per line)
python scripts/extract_metadata.py \
  --input paper_ids.txt \
  --output references.bib

# Different output formats
python scripts/extract_metadata.py \
  --doi 10.1038/nature12345 \
  --format json  # or bibtex, yaml
```

### validate_itations.py

验证BibTeX条目的准确性和完整性。

* *功能**：
- 通过doi.org和DOI验证CrossRef
- 必填字段检查
- 重复检测
- 格式验证
- 自动修复常见问题
- 详细报告

* *用法**：
```bash
# Basic validation
python scripts/validate_citations.py references.bib

# With auto-fix
python scripts/validate_citations.py references.bib \
  --auto-fix \
  --output fixed_references.bib

# Detailed validation report
python scripts/validate_citations.py references.bib \
  --report validation_report.json \
  --verbose

# Only check DOIs
python scripts/validate_citations.py references.bib \
  --check-dois-only
```

### format_bibtex.py

格式化和清理BibTeX文件。

* *功能**：
- 标准化格式化
- 对条目进行排序（按键、年份、作者）
- 删除重复项
- 验证语法
- 修复常见问题错误
- 强制执行引文键约定

* *用法**：
```bash
# Basic formatting
python scripts/format_bibtex.py references.bib

# Sort by year (newest first)
python scripts/format_bibtex.py references.bib \
  --sort year \
  --descending \
  --output sorted_refs.bib

# Remove duplicates
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --output clean_refs.bib

# Complete cleanup
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --sort year \
  --validate \
  --auto-fix \
  --output final_refs.bib
```

### doi_to_bibtex.py

快速 DOI 到 BibTeX 转换。

* *功能**：
- 快速单个DOI转换
- 批量处理
- 多种输出格式
- 剪贴板支持

* *用法**：
```bash
# Single DOI
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2

# Multiple DOIs
python scripts/doi_to_bibtex.py \
  10.1038/nature12345 \
  10.1126/science.abc1234 \
  10.1016/j.cell.2023.01.001

# From file (one DOI per line)
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib

# Copy to clipboard
python scripts/doi_to_bibtex.py 10.1038/nature12345 --clipboard
```

## 最佳实践

### 搜索策略

1. **从广泛开始，然后缩小**：
  - 从一般术语开始了解该领域
  - 使用特定关键字和过滤器进行细化
  - 使用同义词和相关术语

2. **使用多个来源**：
  - Google Scholar 用于全面覆盖 
  - PubMed 用于生物医学焦点 
  - arXiv 用于预印本 
  - 合并结果以获得完整性

3. **利用引用**：
  - 检查开创性论文的“被引用”
  - 回顾关键论文的参考文献
  - 使用引用网络发现相关工作

4. **记录您的搜索**：
  - 保存搜索查询和日期
  - 记录结果数量
  - 记下应用的任何过滤器或限制

### 元数据提取

1. **如果可用，请始终使用 DOI**：
  - 最可靠的标识符
  - 出版物的永久链接
  - 通过 CrossRef

2 的最佳元数据源。 **验证提取的元数据**：
 - 检查作者姓名是否正确
  - 验证期刊/会议名称
  - 确认出版年份
  - 验证页码和卷

3. **处理边缘情况**：
  - 预印本：包括存储库和 ID
  - 稍后发布的预印本：使用已发布的版本
  - 会议论文：包括会议名称和地点
  - 书籍章节：包括书名和编辑

4. **保持一致性**：
  - 使用一致的作者姓名格式
  - 标准化期刊缩写
  - 使用相同的DOI格式（首选URL）

### BibTeX Quality

1. **遵循约定**：
  - 使用有意义的引用键（FirstAuthor2024 关键字）
  - 使用 {}
 保护标题中的大写 - 使用 -- 表示页面范围（不是单破折号）
 - 包括所有现代出版物的 DOI 字段

2. **保持干净**：
  - 删除不必要的字段
  - 没有冗余信息
  - 一致的格式
  - 定期验证语法

3. **系统地组织**：
  - 按年份或主题排序
  - 将相关论文分组
  - 对不同的项目使用单独的文件
  - 仔细合并以避免重复

### 验证

1. **尽早且经常验证**：
  - 添加引用时检查引文
  - 提交前验证完整的参考书目
  - 在任何手动编辑后重新验证

2. **及时修复问题**：
  - 损坏的 DOI：查找正确的标识符
  - 缺失字段：从原始来源提取
  - 重复：选择最佳版本，删除其他版本
  - 格式错误：安全时使用自动修复

3. **手动审查关键引用**：
  - 验证正确引用的关键论文
  - 检查作者姓名是否与出版物匹配
  - 确认页码和卷
  - 确保URL是最新的

## 要避免的常见陷阱

1. **单一来源偏差**：仅使用 Google Scholar 或 PubMed
  - **解决方案**：搜索多个数据库以全面覆盖 

2. **盲目接受元数据**：不验证提取的信息
  - **解决方案**：根据原始来源抽查提取的元数据

3. **忽略 DOI 错误**：参考书目中损坏或不正确的 DOI
  - **解决方案**：在最终提交之前运行验证

4. **格式不一致**：混合引用键样式，格式化
  - **解决方案**：使用format_bibtex.py标准化

5. **重复条目**：同一篇论文使用不同的键多次引用
  - **解决方案**：在验证中使用重复检测

6. **缺少必填字段**：BibTeX 条目不完整
  - **解决方案**：验证并确保所有必填字段均存在

7. **过时的预印本**：出版版本存在时引用预印本
  - **解决方案**：检查预印本是否已发布，更新到期刊版本

8. **特殊字符问题**：由于字符
而导致 LaTeX 编译损坏 - **解决方案**：在 BibTeX

 中使用正确的转义或 Unicode9. **提交前不验证**：提交时出现引用错误
 - **解决方案**：始终将验证作为最终检查

10. **手动 BibTeX 条目**：手动键入条目
  - **解决方案**：始终使用脚本从元数据源中提取

## 示例工作流程

### 示例 1：为论文构建参考书目

```bash
# Step 1: Find key papers on your topic
python scripts/search_google_scholar.py "transformer neural networks" \
  --year-start 2017 \
  --limit 50 \
  --output transformers_gs.json

python scripts/search_pubmed.py "deep learning medical imaging" \
  --date-start 2020 \
  --limit 50 \
  --output medical_dl_pm.json

# Step 2: Extract metadata from search results
python scripts/extract_metadata.py \
  --input transformers_gs.json \
  --output transformers.bib

python scripts/extract_metadata.py \
  --input medical_dl_pm.json \
  --output medical.bib

# Step 3: Add specific papers you already know
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2 >> specific.bib
python scripts/doi_to_bibtex.py 10.1126/science.aam9317 >> specific.bib

# Step 4: Combine all BibTeX files
cat transformers.bib medical.bib specific.bib > combined.bib

# Step 5: Format and deduplicate
python scripts/format_bibtex.py combined.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output formatted.bib

# Step 6: Validate
python scripts/validate_citations.py formatted.bib \
  --auto-fix \
  --report validation.json \
  --output final_references.bib

# Step 7: Review any issues
cat validation.json | grep -A 3 '"errors"'

# Step 8: Use in LaTeX
# \bibliography{final_references}
```

### 示例 2：转换列表DOIs

```bash
# You have a text file with DOIs (one per line)
# dois.txt contains:
# 10.1038/s41586-021-03819-2
# 10.1126/science.aam9317
# 10.1016/j.cell.2023.01.001

# Convert all to BibTeX
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib

# Validate the result
python scripts/validate_citations.py references.bib --verbose
```

### 示例 3：清理现有 BibTeX 文件

```bash
# You have a messy BibTeX file from various sources
# Clean it up systematically

# Step 1: Format and standardize
python scripts/format_bibtex.py messy_references.bib \
  --output step1_formatted.bib

# Step 2: Remove duplicates
python scripts/format_bibtex.py step1_formatted.bib \
  --deduplicate \
  --output step2_deduplicated.bib

# Step 3: Validate and auto-fix
python scripts/validate_citations.py step2_deduplicated.bib \
  --auto-fix \
  --output step3_validated.bib

# Step 4: Sort by year
python scripts/format_bibtex.py step3_validated.bib \
  --sort year \
  --descending \
  --output clean_references.bib

# Step 5: Final validation report
python scripts/validate_citations.py clean_references.bib \
  --report final_validation.json \
  --verbose

# Review report
cat final_validation.json
```

### 示例 4：查找并引用开创性论文

```bash
# Find highly cited papers on a topic
python scripts/search_google_scholar.py "AlphaFold protein structure" \
  --year-start 2020 \
  --year-end 2024 \
  --sort-by citations \
  --limit 20 \
  --output alphafold_seminal.json

# Extract the top 10 by citation count
# (script will have included citation counts in JSON)

# Convert to BibTeX
python scripts/extract_metadata.py \
  --input alphafold_seminal.json \
  --output alphafold_refs.bib

# The BibTeX file now contains the most influential papers
```

## 与其他集成技能

### 文献综述技能

* *引文管理**为**文献综述**提供技术基础设施：

- **文献综述**：多数据库系统检索和综合
- **引文管理**：元数据提取和验证

* *组合工作流程**：
1. 使用 literature-review 进行系统搜索方法 
2. 使用 citation-management 提取并验证引文
3. 使用 literature-review 综合结果 
4. 使用 citation-management 确保参考书目准确性

### 科学写作技巧

* *引文管理**确保**科学写作**的准确参考：

- 导出经过验证的 BibTeX 以用于 LaTeX 手稿
- 验证引文是否符合出版标准
- 根据期刊设置参考文献格式要求

### 场地模板技能

* *引文管理**与**场地模板**配合使用，以提交准备好的稿件：

- 不同的场地需要不同的引文样式
- 生成格式正确的参考文献
- 验证引文是否满足场地要求

## 资源

### 捆绑资源

* *参考文献**（在 `references/` 中）：
- `google_scholar_search.md`：完整的 Google 学术搜索指南
- `pubmed_search.md`：PubMed 和 E-utilities API 文档
- `metadata_extraction.md`：元数据源和字段要求
- `citation_validation.md`：验证标准和质量检查
- `bibtex_formatting.md`：BibTeX条目类型和格式规则

* *脚本**（在`scripts/`中）：
- `search_google_scholar.py`：Google学术搜索自动化
- `search_pubmed.py`：PubMed 电子实用程序 API 客户端
- `extract_metadata.py`：通用元数据提取器
- `validate_citations.py`：引文验证和验证
- `format_bibtex.py`：BibTeX 格式化程序和清理程序
- `doi_to_bibtex.py`：快速 DOI 到 BibTeX 转换器

* *资产**（在 `assets/` 中）：
- `bibtex_template.bib`：所有类型的 BibTeX 条目示例
- `citation_checklist.md`：质量保证清单

### 外部资源

* *搜索引擎**：
- Google Scholar：https://scholar.google.com/
- PubMed：https://pubmed.ncbi.nlm.nih.gov/
- PubMed 高级搜索： https://pubmed.ncbi.nlm.nih.gov/advanced/

* *元数据 API**：
- CrossRef API：https://api.crossref.org/
- PubMed 电子实用程序：https://www.ncbi.nlm.nih.gov/books/NBK25501/
- arXiv API：https://arxiv.org/help/api/
- DataCite API：https://api.datacite.org/

* *工具和验证器**：
- MeSH 浏览器：https://meshb.nlm.nih.gov/search
- DOI 解析器：https://doi.org/
- BibTeX 格式：http://www.bibtex.org/Format/

* *引文样式**：
- BibTeX 文档：http://www.bibtex.org/
- LaTeX 书目管理：https://www.overleaf.com/learn/latex/Bibliography_management

## 依赖项

### 必需的Python包

```bash
# Core dependencies
pip install requests  # HTTP requests for APIs
pip install bibtexparser  # BibTeX parsing and formatting
pip install biopython  # PubMed E-utilities access

# Optional (for Google Scholar)
pip install scholarly  # Google Scholar API wrapper
# or
pip install selenium  # For more robust Scholar scraping
```

### 可选工具

```bash
# For advanced validation
pip install crossref-commons  # Enhanced CrossRef API access
pip install pylatexenc  # LaTeX special character handling
```

## 总结

citation-management技能提供：

1. **Google Scholar 和 PubMed
2 的全面搜索功能**。 **从 DOI、PMID、arXiv ID、URLs
3 中自动提取元数据**。 **引文验证**带有 DOI 验证和完整性检查
4. **BibTeX 格式化** 使用标准化和清理工具
5. **质量保证**通过验证和报告
6. **与科学写作工作流程集成**
7. **可重复性** 通过记录的检索和提取方法

使用此技能在整个研究中保持准确、完整的引用，并确保可发表的参考书目。
