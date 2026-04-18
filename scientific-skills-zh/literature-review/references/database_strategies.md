# 文献数据库检索策略

本文档为系统有效地检索多个文献数据库提供了全面的指导。

## 可用数据库和技能

### 生物医学与生命科学

#### PubMed / PubMed Central
- **访问**：使用`gget`技能或WebFetch工具
- **覆盖范围**：生物医学文献中超过3500万次引用
- **最适合**：临床研究、生物医学研究、遗传学、分子生物学
- **搜索提示**：使用MeSH术语、布尔运算符（AND、OR、NOT）、字段标签[标题]，[作者]
- **示例**： `"CRISPR"[Title] AND "gene editing"[Title/Abstract] AND 2020:2024[Publication Date]`

#### bioRxiv / medRxiv
- **访问**：使用 `gget` 技能或直接 API
- **覆盖范围**：生物学和医学预印本
- **最适合**：最新未发表的研究、前沿发现
- **注**：未经同行评审；谨慎验证结果
- **搜索提示**：按类别搜索（生物信息学、基因组学等）

### 一般科学文献

#### arXiv
- **访问**：直接API访问
- **覆盖范围**：物理、数学、计算机科学、定量领域的预印本生物学
- **最适合**：计算方法、生物信息学算法、理论工作
- **类别**：q-bio（定量生物学）、cs.LG（机器学习）、stat.ML（统计学）
- **搜索格式**：`cat:q-bio.QM AND title:"single cell"`

#### 语义Scholar
- **访问**：直接 API（需要 API 密钥）
- **覆盖范围**：所有领域 2 亿多篇论文
- **最适合**：跨学科搜索、引文图、论文推荐
- **功能**：有影响力的引用、论文摘要、相关paper
- **速率限制**：100 个请求/5 分钟，使用 API 密钥

#### Google Scholar
- **访问**：网页抓取（谨慎使用）或手动搜索
- **覆盖**：涵盖所有领域
- **最适合**：查找高被引论文、会议记录、论文
- **限制**：无官方 API，速率限制
- **导出**：使用“引用”功能格式化引文

### 专业数据库

#### ChEMBL / PubChem
- **访问**：使用 `gget` 技能或 `bioservices` 技能
- **覆盖范围**：化学化合物、生物活性数据、药物分子
- **最适合**：药物发现、化学生物学、医学化学
- **ChEMBL**：2M+ 化合物，生物活性数据
- **PubChem**：110M+ 化合物，测定数据

#### UniProt
- **访问**：使用 `gget` 技能或 `bioservices` 技能
- **覆盖范围**：蛋白质序列和功能信息
- **最适合**：蛋白质研究、序列分析、功能注释
- **搜索方式**：蛋白质名称、基因名称、有机体、功能

#### KEGG（京都基因和基因组百科全书）
- **访问**：使用`bioservices`技能
- **覆盖**：通路、疾病、药物、基因
- **最适合**：通路分析、系统生物学、代谢研究

#### COSMIC（癌症体细胞突变目录）
- **访问**：使用`gget`技能或直接下载
- **覆盖范围**：癌症基因组学、体细胞突变
- **最适合**：癌症研究、突变分析

#### AlphaFold 数据库
- **访问**：使用 `gget` 技能和 `alphafold` 命令
- **覆盖范围**：200M+ 蛋白质结构预测
- **最适合**：结构生物学、蛋白质建模

#### PDB（蛋白质数据库）
- **访问**：使用`gget`或直接API
- **覆盖范围**：蛋白质、核酸的实验3D结构
- **最适合**：结构生物学、药物设计、分子建模

### 引文和参考文献管理

#### OpenAlex
- **访问**：直接 API（免费，无需密钥）
- **覆盖**：250M+ 作品，全面的元数据
- **最适合**：引文分析、作者消歧、机构研究
- **功能**：开放访问，非常适合文献计量学

#### 维度
- **访问**：提供免费套餐
- **覆盖范围**：出版物、拨款、专利、临床试验
- **最适合**：研究影响、资金分析、转化研究

- --

## 搜索策略框架

### 1. 定义研究问题 (PICO框架）

用于临床/生物医学评论：
- **P**群体：研究对象是谁？
- **I**干预：正在测试什么？
- **C**比较：与什么相比？
- **O**结果：什么是结果？

* *示例**：“与标准治疗 (C)相比，CRISPR-Cas9 基因疗法 (I)治疗镰状细胞病 (P)在改善患者预后 (O)方面的功效如何？”

### 2. 开发搜索词

#### 主要概念
从您的研究中识别 2-4 个主要概念问题。

* *示例**：
- 概念 1：CRISPR、Cas9、基因编辑
- 概念 2：镰状细胞病、SCD、血红蛋白疾病
- 概念 3：基因治疗、治疗性编辑

#### 同义词和相关术语
列出替代术语， 

* *工具**：使用 MeSH（医学主题词）浏览器查看标准化术语

#### 布尔运算符
- **AND**：缩小搜索范围（必须包括两个术语）
- **OR**：扩大搜索范围（包括任一术语）
- **NOT**：排除术语

* *示例**：`(CRISPR OR Cas9 OR "gene editing") AND ("sickle cell" OR SCD) AND therapy`

#### 通配符和截断
- `*` 或 `%`：匹配任何字符
- `?`：匹配单个字符字符

* *示例**：`genom*` 匹配基因组、基因组、基因组

### 3. 设置包含/排除标准

#### 纳入标准
- **日期范围**：例如，2015-2024（过去10年）
- **语言**：英语（或指定多语言）
- **出版物类型**：同行评审的文章、评论、预印本
- **研究设计**： RCT、队列研究、荟萃分析
- **人群**：人类、动物模型、体外

#### 排除标准
- 病例报告 (n<5)
- 无全文的会议摘要
- 非原创研究（社论、评论）
- 重复出版物
- 撤稿文章

### 4. 数据库选择策略

#### 多数据库方法
搜索至少3个互补数据库：

1. **主要数据库**：PubMed（生物医学）或 arXiv（计算）
2. **预印本服务器**：bioRxiv/medRxiv 或 arXiv
3. **综合数据库**：Semantic Sc​​holar 或 Google Scholar
4. **专用数据库**：ChEMBL、UniProt 或特定领域的

#### 数据库特定语法

|数据库|字段标签 |示例 |
|----------|------------|---------|
|考研| [标题]、[作者]、[MeSH] | “CRISPR”[标题]和 2020:2024[DP] |
| arXiv | ti:, au:, cat: | ti:“机器学习” AND cat:q-bio.QM |
|语义学者|标题：，作者：，年份：|标题：《深度学习》年份：2020-2024 |

- --

## 搜索执行工作流程

### 第一阶段：试点搜索
1. 使用广义术语 
2 运行初始搜索。查看前 50 个结果的相关性
3. 注意常见关键字和 MeSH 术语
4. 细化搜索策略

### 第二阶段：综合搜索
1. 在所有选定的数据库中执行精细搜索
2. 以标准格式（RIS、BibTeX、JSON）
3 导出结果。每个数据库的文档搜索字符串和日期
4. 每个数据库的记录结果数

### 第 3 阶段：重复数据删除
1. 将所有结果导入到单个文件中 
2. 使用 `search_databases.py --deduplicate` 删除重复项 
3. 通过 DOI（主要）或标题（后备）
4 识别重复项。保留元数据最完整的版本

### 第4阶段：筛选
1. **标题筛选**：审查标题，排除明显不相关的
2. **摘要筛选**：阅读摘要，应用纳入/排除标准
3. **全文筛选**：获取并审阅全文
4. 记录每个阶段排除的原因

### 第 5 阶段：质量评估
1. 使用适当的工具评估研究质量：
  - **RCT**：Cochrane 偏倚风险工具
  - **观察**：纽卡斯尔-渥太华量表
  - **系统评价**：AMSTAR 2
2. 证据质量等级（高、中、低、极低）
3. 考虑排除质量非常低的研究

- --

## 搜索文档模板

### 所需文档
所有搜索都必须记录以确保可重复性：

```markdown
## Search Strategy

### Database: PubMed
- **Date searched**: 2024-10-25
- **Date range**: 2015-01-01 to 2024-10-25
- **Search string**:
  ```
  ("CRISPR"[Title] OR "Cas9"[Title] OR "gene editing"[Title/Abstract])
  AND ("sickle cell disease"[MeSH] OR "SCD"[Title/Abstract])
  AND ("gene therapy"[MeSH] OR "therapeutic editing"[Title/Abstract])
  AND 2015:2024[Publication Date]
  AND English[Language]
  ```
- **Results**: 247 articles
- **After deduplication**: 189 articles

### Database: bioRxiv
- **Date searched**: 2024-10-25
- **Date range**: 2015-01-01 to 2024-10-25
- **Search string**: "CRISPR" AND "sickle cell" (in title/abstract)
- **Results**: 34 preprints
- **After deduplication**: 28 preprints

### Total Unique Articles
- **Combined results**: 217 unique articles
- **After title screening**: 156 articles
- **After abstract screening**: 89 articles
- **After full-text screening**: 52 articles included in review
```

- --

## 高级搜索技术

### 优先考虑高影响力论文（关键）

* *始终根据引用次数、地点质量和作者声誉来优先考虑论文。** 质量比数量更重要。

#### 数据库搜索中的引用指标

使用引用计数来识别有影响力的作品：

|纸时代|引文|分类|
|---------|------------------------|----------------|
| 0-3岁| 20+ |值得关注|
| 0-3岁| 100+ |极具影响力|
| 3-7年| 100+ |重要|
| 3-7年| 500+ |地标|
| 7 年以上 | 500+ |开创性|
| 7 年以上 | 1000+ |基础 |

* *数据库特定的引文特征：**
- **Google Scholar：** 按引文计数排序，使用“引用者”功能
- **语义学者：** “高度影响力的引文”指标，引用速度
- **OpenAlex：** 引文计数，引文上下文分析
- **PubMed：** 使用PMC 中的“引用者”，通过 Google Scholar 检查引用计数

#### 按期刊质量过滤

优先考虑来自较高级别场所的论文：

* *第 1 层（始终优先）：**
- Nature、Science、Cell、NEJM、Lancet、JAMA、PNAS
- Nature Medicine、Nature生物技术、自然方法
- 搜索提示：Google Scholar 中的 `source:Nature` 或 `journal:Nature`

* *第 2 层（高优先级）：**
- 高影响力专业期刊（影响因子 >10）
- 顶级会议：NeurIPS、ICML、ICLR、CVPR、 ACL

* *第 3 层（相关时包含）：**
- 受尊重的特定领域期刊 (IF 5-10)

* *PubMed 期刊过滤：**
```
"Nature"[Journal] OR "Science"[Journal] OR "Cell"[Journal]
```

* *Google Scholar 期刊过滤：**
```
source:Nature source:Science source:Cell
```

#### 利用“被引用”功能

* *找到有影响力的工作：**
1. 从已知的关键论文
2开始。单击“引用者”可查找引用它的论文
3. 按引用次数对施引论文进行排序
4. 高被引的施引论文表明重要的后续工作

* *确定开创性论文：**
1. 广泛搜索您的主题
2. 注意哪些论文在参考文献列表中重复出现
3. 您的许多结果引用的论文可能具有开创性
4. 检查引用计数以确认影响力

* *语义学者功能：**
- “高度影响力的引用”显示显着建立在论文基础上的引用
- “引用速度”显示最近的引用增长
- 基于引用网络的论文推荐

### 引用链条

#### 正向引文搜索
查找引用关键论文的论文：
- 使用 Google Scholar“被引用”功能
- 使用 OpenAlex 或 Semantic Scholar API
- 识别基于开创性工作的较新研究 
- **提示：** 按引用计数排序以查找最有影响力的后续研究工作

#### 向后引文搜索
审查关键论文中的参考文献：
- 从包含的论文中提取参考文献
- 搜索高引用参考文献（旧论文的引用次数超过500次）
- 识别基础研究
- **提示：**重点关注多篇论文中出现的参考文献参考书目

### 雪球采样
1. 从 3-5 篇高度相关的论文开始**来自 Tier-1 场地**
2. 提取所有参考文献
3. 查看多篇论文引用了哪些参考文献
4. 查看那些高度重叠的参考文献 - 这些可能具有开创性的
5. 对新确定的关键论文
6重复上述操作。 **每一步都优先考虑高引用次数的论文**

### 作者搜索
关注该领域多产且享有盛誉的作者：
- 在数据库中按作者姓名搜索
- 检查作者简介（ORCID、Google Scholar）以获取 h 索引和出版地点
- 审查最近的出版物和预印本
- **优先选择多篇Tier-1出版物**和高h指数（>40）的作者
- 寻找被公认的领域领导者的资深作者

### 相关文章特征
许多数据库推荐相关文章：
- PubMed“类似文章”
- 语义学者“推荐论文”
- 用于发现关键词搜索遗漏的论文
- **按引用次数和场地质量过滤推荐**

- --

## 质量控制清单

### 搜索之前
- [ ]明确定义研究问题
- [ ]建立PICO 标准（如果适用）
- [ ]列出搜索术语和同义词
- [ ]记录包含/排除标准
- [ ]选择的目标数据库（至少3 个）
- [ ]日期范围确定

### 搜索期间
- [ ]搜索字符串经过测试和优化
- [ ]导出带有完整元数据的结果
- [ ]记录搜索参数
- [ ]每个数据库记录的结果数
- [ ]记录搜索日期

### 之后搜索
- [ ]删除重复项
- [ ]遵循筛选协议
- [ ]记录排除原因
- [ ]完成质量评估
- [ ]所有引文均通过verify_itations.py
- [ ]记录在搜索方法中回顾

- --

## 要避免的常见陷阱

1. **搜索范围太窄**：缺少相关论文
  - 解决方案：包括同义词、相关术语、更广泛的概念

2. **搜索范围太广**：数千个不相关的结果
  - 解决方案：使用 AND 添加特定概念，使用字段标签

3. **单一数据库**：覆盖不完整
  - 解决方案：搜索至少3个互补数据库

4. **忽略预印本**：缺少最新发现
  - 解决方案：包括bioRxiv、medRxiv 或arXiv

5. **无文档**：不可重复的搜索
  - 解决方案：记录每个搜索字符串、日期和结果计数

6. **手动去重**：耗时且容易出错
  - 解决方案：使用search_databases.py脚本

7. **未经验证的引文**：DOI 损坏、元数据不正确
  - 解决方案：在最终参考列表

8 上运行 verify_itations.py。 **发表偏倚**：仅包括已发表的阳性结果
 - 解决方案：搜索试验注册中心，联系作者获取未发表的数据

- --

## 多数据库搜索工作流程示例

```python
# Example workflow using available skills

# 1. Search PubMed via gget
search_term = "CRISPR AND sickle cell disease"
# Use gget search pubmed search_term

# 2. Search bioRxiv
# Use gget search biorxiv search_term

# 3. Search arXiv for computational papers
# Search arXiv with: cat:q-bio AND "CRISPR" AND "sickle cell"

# 4. Search Semantic Scholar via API
# Use semantic scholar API with search query

# 5. Aggregate and deduplicate results
# python search_databases.py combined_results.json --deduplicate --format markdown --output review_papers.md

# 6. Verify all citations
# python verify_citations.py review_papers.md

# 7. Generate final PDF
# python generate_pdf.py review_papers.md --citation-style nature
```

- --

## 资源

### MeSH 浏览器
https://meshb.nlm.nih.gov/search

### 布尔搜索教程
https://www.ncbi.nlm.nih.gov/books/NBK3827/

### 引文风格指南
请参阅引用/引用_styles.md技能

### PRISMA指南
系统评价和荟萃分析的首选报告项目：
http://www.prisma-statement.org/
