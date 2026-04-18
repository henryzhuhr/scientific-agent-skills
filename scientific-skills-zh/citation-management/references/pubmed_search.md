# PubMed 搜索指南

PubMed 生物医学和生命科学文献搜索综合指南，包括 MeSH 术语、字段标签、高级搜索策略和电子实用程序 API 使用。

## 概述

PubMed 是生物医学文献的首要数据库：
- **覆盖率**：35+ 百万引用
- **范围**：生物医学和生命科学
- **来源**：MEDLINE、生命科学期刊、在线书籍
- **权威**：由国家医学图书馆 (NLM) / NCBI
- **访问**：免费，无需帐户
- **更新**：每日更新引用
- **Curation**：高质量元数据，MeSH 索引

## 基本搜索

### 简单关键字搜索

PubMed 自动将术语映射到 MeSH 并搜索多个字段：

```
diabetes
CRISPR gene editing
Alzheimer's disease treatment
cancer immunotherapy
```

* *自动功能**：
- 自动 MeSH 映射
- 复数/单数变体
- 缩写扩展
- 拼写检查

### 精确短语搜索

使用引号进行精确短语：

```
"CRISPR-Cas9"
"systematic review"
"randomized controlled trial"
"machine learning"
```

## MeSH（医学主题词）

### 什么是 MeSH？

MeSH 是用于索引生物医学文献的受控词汇同义词库：
- **层次结构**：以树结构组织
- **一致的索引**：相同的概念始终以相同的方式标记
- **全面**：涵盖疾病、药物、解剖学、技术等。
- **专业管理**：NLM 索引器分配 MeSH 术语

### 查找 MeSH 术语

* *MeSH 浏览器**： https://meshb.nlm.nih.gov/search

* *示例**：
```
Search: "heart attack"
MeSH term: "Myocardial Infarction"
```

* *在 PubMed**：
1. 使用关键字
2进行搜索。检查左侧边栏中的“MeSH 术语”
3. 选择相关的 MeSH 术语
4. 添加到搜索

### 在搜索中使用 MeSH

* *基本 MeSH 搜索**：
```
"Diabetes Mellitus"[MeSH]
"CRISPR-Cas Systems"[MeSH]
"Alzheimer Disease"[MeSH]
"Neoplasms"[MeSH]
```

 * *带副标题的 MeSH**：
```
"Diabetes Mellitus/drug therapy"[MeSH]
"Neoplasms/genetics"[MeSH]
"Heart Failure/prevention and control"[MeSH]
```

 * *常见副标题**：
- `/drug therapy`：药物治疗
- `/diagnosis`：诊断方面
- `/genetics`：遗传方面
- `/epidemiology`：发生与分布
- `/prevention and control`：预防方法
- `/etiology`：原因
- `/surgery`：手术治疗
- `/metabolism`：代谢方面

### MeSH 爆炸

默认情况下，MeSH 搜索包括较窄的术语（爆炸）：

```
"Neoplasms"[MeSH]
# Includes: Breast Neoplasms, Lung Neoplasms, etc.
```

* *禁用爆炸**（确切术语）仅）：
```
"Neoplasms"[MeSH:NoExp]
```

### MeSH 主要主题

仅在主要关注 MeSH 术语的情况下搜索：

```
"Diabetes Mellitus"[MeSH Major Topic]
# Only papers where diabetes is main topic
```

## 字段标签

字段标签指定要搜索记录的哪一部分。

### 常见字段标签

* *标题和摘要**：
```
cancer[Title]                    # In title only
treatment[Title/Abstract]        # In title or abstract
"machine learning"[Title/Abstract]
```

* *作者**：
```
"Smith J"[Author]
"Doudna JA"[Author]
"Collins FS"[Author]
```

* *作者 - 完整姓名**:
```
"Smith, John"[Full Author Name]
```

* *期刊**:
```
"Nature"[Journal]
"Science"[Journal]
"New England Journal of Medicine"[Journal]
"Nat Commun"[Journal]           # Abbreviated form
```

* *发表日期**:
```
2023[Publication Date]
2020:2024[Publication Date]      # Date range
2023/01/01:2023/12/31[Publication Date]
```

* *日期创建**：
```
2023[Date - Create]              # When added to PubMed
```

* *发布类型**：
```
"Review"[Publication Type]
"Clinical Trial"[Publication Type]
"Meta-Analysis"[Publication Type]
"Randomized Controlled Trial"[Publication Type]
```

* *语言**：
```
English[Language]
French[Language]
```

* *DOI**：
```
10.1038/nature12345[DOI]
```

* *PMID（PubMed） ID)**:
```
12345678[PMID]
```

* *文章 ID**:
```
PMC1234567[PMC]                  # PubMed Central ID
```

### 不太常见但有用的标签

```
humans[MeSH Terms]               # Only human studies
animals[MeSH Terms]              # Only animal studies
"United States"[Place of Publication]
nih[Grant Number]                # NIH-funded research
"Female"[Sex]                    # Female subjects
"Aged, 80 and over"[Age]        # Elderly subjects
```

## 布尔值运算符

将搜索项与布尔逻辑结合起来。

### AND

这两个项必须存在（默认行为）：

```
diabetes AND treatment
"CRISPR-Cas9" AND "gene editing"
cancer AND immunotherapy AND "clinical trial"[Publication Type]
```

### OR

E其中一个项必须是存在：

```
"heart attack" OR "myocardial infarction"
diabetes OR "diabetes mellitus"
CRISPR OR Cas9 OR "gene editing"
```

* *用例**：同义词和相关术语

### NOT

排除术语：

```
cancer NOT review
diabetes NOT animal
"machine learning" NOT "deep learning"
```

* *警告**：可能排除同时提及两者的相关论文terms.

### 组合运算符

使用括号进行复杂逻辑：

```
(diabetes OR "diabetes mellitus") AND (treatment OR therapy)

("CRISPR" OR "gene editing") AND ("therapeutic" OR "therapy") 
  AND 2020:2024[Publication Date]

(cancer OR neoplasm) AND (immunotherapy OR "immune checkpoint inhibitor") 
  AND ("clinical trial"[Publication Type] OR "randomized controlled trial"[Publication Type])
```

## 高级搜索生成器

* *访问**： https://pubmed.ncbi.nlm.nih.gov/advanced/

* *功能**：
- 可视化查询生成器
- 添加多个查询框
- 从下拉列表中选择字段标签
- 与 AND/OR/NOT
- 结合使用结果
- 显示最终查询字符串
- 保存查询

* *工作流程**：
1. 在单独的框中添加搜索词
2. 选择字段标签
3. 选择布尔运算符
4. 预览结果
5. 根据需要精炼
6. 复制最终查询字符串
7. 在脚本中使用或保存

* *构建的示例查询**：
```
#1: "Diabetes Mellitus, Type 2"[MeSH]
#2: "Metformin"[MeSH]
#3: "Clinical Trial"[Publication Type]
#4: 2020:2024[Publication Date]
#5: #1 AND #2 AND #3 AND #4
```

## 过滤器和限制

### 文章类型

```
"Review"[Publication Type]
"Systematic Review"[Publication Type]
"Meta-Analysis"[Publication Type]
"Clinical Trial"[Publication Type]
"Randomized Controlled Trial"[Publication Type]
"Case Reports"[Publication Type]
"Comparative Study"[Publication Type]
```

### 物种

```
humans[MeSH Terms]
mice[MeSH Terms]
rats[MeSH Terms]
```

### 性别

```
"Female"[MeSH Terms]
"Male"[MeSH Terms]
```

### 年龄组

```
"Infant"[MeSH Terms]
"Child"[MeSH Terms]
"Adolescent"[MeSH Terms]
"Adult"[MeSH Terms]
"Aged"[MeSH Terms]
"Aged, 80 and over"[MeSH Terms]
```

### 文本可用性

```
free full text[Filter]           # Free full-text available
```

### 期刊类别

```
"Journal Article"[Publication Type]
```

## 电子实用程序API

NCBI 通过电子实用程序（Entrez 编程实用程序）提供编程访问。

### 概述

* *基本URL**：`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

* *主要工具**：
- **ESearch**：搜索和检索PMID
- **Eetch**：检索完整记录
- **ESummary**：检索文档摘要
- **ELink**：查找相关文章
- **EInfo**：数据库统计

* *不需要 API 密钥**，但推荐用于：
- 更高的速率限制（10/秒 vs 3/秒）
- 更好的性能
- 识别您的项目

* *获取 API 密钥**： https://www.ncbi.nlm.nih.gov/account/

### ESearch - 搜索 PubMed

检索查询的 PMID。

* *端点**：`/esearch.fcgi`

* *参数**：
- `db`：数据库(pubmed)
- `term`：搜索查询
- `retmax`：最大结果（默认 20，最大 10000）
- `retstart`：起始位置（用于分页）
- `sort`：排序顺序（相关性、pub_date、作者）
- `api_key`：您的 API 密钥（可选但推荐）

* *示例URL**：
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?
  db=pubmed&
  term=diabetes+AND+treatment&
  retmax=100&
  retmode=json&
  api_key=YOUR_API_KEY
```

* *响应**：
```json
{
  "esearchresult": {
    "count": "250000",
    "retmax": "100",
    "idlist": ["12345678", "12345679", ...]
  }
}
```

### EFetch - 检索记录

获取 PMID 的完整元数据。

* *端点**： `/efetch.fcgi`

* *参数**：
- `db`：数据库（pubmed）
- `id`：逗号分隔的 PMID
- `retmode`：格式（xml、json、文本）
- `rettype`：类型（摘要、medline、完整）
- `api_key`：您的 API 密钥

* *示例 URL**：
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?
  db=pubmed&
  id=12345678,12345679&
  retmode=xml&
  api_key=YOUR_API_KEY
```

* *响应**：具有完整元数据的 XML，包括：
- 标题
- 作者（具有从属关系）
- 摘要
- 期刊
- 出版日期
- DOI
- PMID, PMCID
- MeSH 术语
- 关键字

### ESummary - 获取摘要

的轻量级替代方案EFetch.

* *示例**：
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?
  db=pubmed&
  id=12345678&
  retmode=json&
  api_key=YOUR_API_KEY
```

* *返回**：没有完整摘要和详细信息的关键元数据。

### ELink - 查找相关文章

查找相关文章或其他链接数据库.

* *示例**：
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?
  dbfrom=pubmed&
  db=pubmed&
  id=12345678&
  linkname=pubmed_pubmed_citedin
```

* *链接类型**：
- `pubmed_pubmed`：相关文章
- `pubmed_pubmed_citedin`：引用本文的论文
- `pubmed_pmc`：PMC全文版本
- `pubmed_protein`：相关蛋白质记录

### 速率限制

* *无API密钥**：
- 每秒3个请求
- 超出则阻止

* *有API密钥**：
- 每秒10个请求
- 更适合编程访问

* *最佳实践**：
```python
import time
time.sleep(0.34)  # ~3 requests/second
# or
time.sleep(0.11)  # ~10 requests/second with API key
```

### API密钥用法

* *获取API密钥**：
1. 创建 NCBI 帐户：https://www.ncbi.nlm.nih.gov/account/
2. 设置 → API 密钥管理
3. 创建新的 API 密钥
4. 复制密钥

* *在请求中使用**：
```
&api_key=YOUR_API_KEY_HERE
```

* *安全存储**：
```bash
# In environment variable
export NCBI_API_KEY="your_key_here"

# In script
import os
api_key = os.getenv('NCBI_API_KEY')
```

## 搜索策略

### 全面系统搜索

用于系统评论和荟萃分析：

```
# 1. Identify key concepts
Concept 1: Diabetes
Concept 2: Treatment
Concept 3: Outcomes

# 2. Find MeSH terms and synonyms
Concept 1: "Diabetes Mellitus"[MeSH] OR diabetes OR diabetic
Concept 2: "Drug Therapy"[MeSH] OR treatment OR therapy OR medication
Concept 3: "Treatment Outcome"[MeSH] OR outcome OR efficacy OR effectiveness

# 3. Combine with AND
("Diabetes Mellitus"[MeSH] OR diabetes OR diabetic) 
  AND ("Drug Therapy"[MeSH] OR treatment OR therapy OR medication)
  AND ("Treatment Outcome"[MeSH] OR outcome OR efficacy OR effectiveness)

# 4. Add filters
AND 2015:2024[Publication Date]
AND ("Clinical Trial"[Publication Type] OR "Randomized Controlled Trial"[Publication Type])
AND English[Language]
AND humans[MeSH Terms]
```

### 查找临床试验

```
# Specific disease + clinical trials
"Alzheimer Disease"[MeSH] 
  AND ("Clinical Trial"[Publication Type] 
       OR "Randomized Controlled Trial"[Publication Type])
  AND 2020:2024[Publication Date]

# Specific drug trials
"Metformin"[MeSH] 
  AND "Diabetes Mellitus, Type 2"[MeSH]
  AND "Randomized Controlled Trial"[Publication Type]
```

### 查找评论

```
# Systematic reviews on topic
"CRISPR-Cas Systems"[MeSH] 
  AND ("Systematic Review"[Publication Type] OR "Meta-Analysis"[Publication Type])

# Reviews in high-impact journals
cancer immunotherapy 
  AND "Review"[Publication Type]
  AND ("Nature"[Journal] OR "Science"[Journal] OR "Cell"[Journal])
```

### 查找近期论文

```
# Papers from last year
"machine learning"[Title/Abstract] 
  AND "drug discovery"[Title/Abstract]
  AND 2024[Publication Date]

# Recent papers in specific journal
"CRISPR"[Title/Abstract] 
  AND "Nature"[Journal]
  AND 2023:2024[Publication Date]
```

### 作者追踪

```
# Specific author's recent work
"Doudna JA"[Author] AND 2020:2024[Publication Date]

# Author + topic
"Church GM"[Author] AND "synthetic biology"[Title/Abstract]
```

### 高质量证据

```
# Meta-analyses and systematic reviews
(diabetes OR "diabetes mellitus") 
  AND (treatment OR therapy)
  AND ("Meta-Analysis"[Publication Type] OR "Systematic Review"[Publication Type])

# RCTs only
cancer immunotherapy 
  AND "Randomized Controlled Trial"[Publication Type]
  AND 2020:2024[Publication Date]
```

## 脚本集成

### search_pubmed.py 用法

* *基本搜索**：
```bash
python scripts/search_pubmed.py "diabetes treatment"
```

* *使用 MeSH 术语**：
```bash
python scripts/search_pubmed.py \
  --query '"Diabetes Mellitus"[MeSH] AND "Drug Therapy"[MeSH]'
```

* *日期范围过滤器**:
```bash
python scripts/search_pubmed.py "CRISPR" \
  --date-start 2020-01-01 \
  --date-end 2024-12-31 \
  --limit 200
```

* *发布类型过滤器**:
```bash
python scripts/search_pubmed.py "cancer immunotherapy" \
  --publication-types "Clinical Trial,Randomized Controlled Trial" \
  --limit 100
```

* *导出到BibTeX**:
```bash
python scripts/search_pubmed.py "Alzheimer's disease" \
  --limit 100 \
  --format bibtex \
  --output alzheimers.bib
```

* *来自的复杂查询file**:
```bash
# Save complex query in query.txt
cat > query.txt << 'EOF'
("Diabetes Mellitus, Type 2"[MeSH] OR "diabetes"[Title/Abstract])
AND ("Metformin"[MeSH] OR "metformin"[Title/Abstract])
AND "Randomized Controlled Trial"[Publication Type]
AND 2015:2024[Publication Date]
AND English[Language]
EOF

# Run search
python scripts/search_pubmed.py --query-file query.txt --limit 500
```

### 批量搜索

```bash
# Search multiple topics
TOPICS=("diabetes treatment" "cancer immunotherapy" "CRISPR gene editing")

for topic in "${TOPICS[@]}"; do
  python scripts/search_pubmed.py "$topic" \
    --limit 100 \
    --output "${topic// /_}.json"
  sleep 1
done
```

### 提取元数据

```bash
# Search returns PMIDs
python scripts/search_pubmed.py "topic" --output results.json

# Extract full metadata
python scripts/extract_metadata.py \
  --input results.json \
  --output references.bib
```

## 提示和最佳实践

### 搜索结构

1. **从 MeSH 术语开始**：
  - 使用 MeSH 浏览器查找正确的术语
  - 比关键字搜索更精确
  - 捕获有关主题的所有论文，无论术语如何

2. **包括文字变体**：
 ```
 # 更好的覆盖范围
（“糖尿病”[MeSH] OR 糖尿病 OR 糖尿病）
 ```

3. **适当使用字段标签**：
  - `[MeSH]` 用于标准化概念 
  - `[Title/Abstract]` 用于特定术语 
  - `[Author]` 用于已知作者 
  - `[Journal]` 用于特定场所 

4. **增量构建**：
 ```
 # 步骤 1：基本搜索
糖尿病
 
 # 步骤 2：添加特异性
"Diabetes Mellitus，Type 2"[MeSH]
 
 # 步骤3：添加治疗
“2 型糖尿病”[MeSH] AND“二甲双胍”[MeSH]
 
 # 步骤 4：添加研究类型
“2 型糖尿病”[MeSH] AND“二甲双胍”[MeSH] 
 AND “临床试验”[发表类型]
 
 # 步骤5：添加日期范围
... AND 2020:2024[发表日期]
 ```

### 优化结果

1. **结果太多**：添加过滤器
  - 限制发布类型
  - 缩小日期范围
  - 添加更具体的MeSH术语
  - 使用主要主题：`[MeSH Major Topic]`

2. **结果太少**：扩大搜索
  - 删除限制性过滤器
  - 使用OR作为同义词
  - 扩大日期范围
  - 使用MeSH爆炸（默认）

3. **不相关的结果**：优化术语
  - 使用更具体的MeSH术语
  - 使用NOT
添加排除项 - 使用标题字段而不是所有字段
 - 添加MeSH副标题

### 质量控制

1. **文档搜索策略**：
  - 保存精确查询字符串
  - 记录搜索日期
  - 记录结果数量
  - 保存使用的过滤器

2. **系统导出**：
  - 使用一致的文件命名
  - 导出为 JSON 以提高灵活性
  - 根据需要转换为 BibTeX
  - 保留原始搜索结果

3. **验证检索到的引文**：
 ```bash
 python script/validate_itations.py pubmed_results.bib
 ```

### 保持最新状态

1. **设置搜索警报**：
  - PubMed → 保存搜索
  - 接收电子邮件更新
  - 每日、每周或每月

2. **跟踪特定期刊**：
 ```
 "Nature"[期刊] AND CRISPR[标题]
 ```

3. **关注主要作者**：
 ```
 "教会总经理"[作者]
 ```

## 常见问题和解决方案

### 问题：MeSH 术语未找到

* *解决方案**：
- 检查拼写
- 使用MeSH浏览器
- 尝试相关术语
- 使用文本单词搜索作为后备

### 问题：零结果

* *解决方案**：
- 删除过滤器
- 检查查询语法
- 使用OR更广泛搜索
- 尝试同义词

### 问题：质量较差

* *解决方案**：
- 添加出版物类型过滤器
- 限制到最近几年
- 使用MeSH 主要主题
- 按期刊质量过滤

### 问题：来自不同来源的重复

* *解决方案**：
```bash
python scripts/format_bibtex.py results.bib \
  --deduplicate \
  --output clean.bib
```

### 问题：API 速率限制

* *解决方案**：
- 获取 API 密钥（将限制增加到 10/秒）
- 添加延迟脚本
- 批量处理
- 使用非高峰时间

## 总结

PubMed 提供权威生物医学文献检索：

✓ **策划内容**：MeSH 索引、质量控制 
✓ **精准搜索**：字段标签、MeSH 术语、过滤器
✓ **程序化访问**：电子实用程序API 
✓ **免费访问**：无需订阅 
✓ **全面**：3500万+引用，每日更新 

关键策略：
- 使用MeSH术语进行精确搜索
- 结合文字词进行全面覆盖范围
- 应用适当的字段标签
- 按出版物类型和日期过滤
- 使用电子实用程序API进行自动化
- 文档搜索策略以实现可重复性

为了更广泛地覆盖跨学科，请补充Google Scholar。
