---
name: literature-review
description: 使用多个学术数据库（PubMed、arXiv、bioRxiv、Semantic Sc​​holar 等）进行全面、系统的文献综述。在跨生物医学、科学和技术领域进行系统文献综述、荟萃分析、研究综合或综合文献检索时，应使用此技能。创建专业格式的 Markdown 文档和 PDF，并以多种引文样式（APA、Nature、Vancouver 等）验证引文。
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 文献综述

## 概述

遵循严格的学术方法论进行系统、全面的文献综述。搜索多个文献数据库，按主题综合研究结果，验证所有引文的准确性，并生成 Markdown 和 PDF 格式的专业输出文档。

此技能使用 **parallel-web 技能** (`parallel-cli search`)作为广泛学术文献发现的主要网络搜索工具，并辅以专门的数据库访问技能（gget、bioservices、数据共享客户端）。它提供了用于引文验证、结果聚合和文档生成的专用工具。

## 何时使用此技能

在以下情况下使用此技能：
- 为研究或出版进行系统文献综述
- 综合多个来源的特定主题的当前知识
- 执行荟萃分析或范围界定评论
- 撰写文献综述部分研究论文或论文的
- 调查研究领域的最新技术
- 确定研究差距和未来方向
- 需要经过验证的引文和专业格式

## 科学示意图的视觉增强

* *⚠️强制：每篇文献综述必须至少包括1-2 使用scientific-schematics技能的AI生成的人物。**

这不是可选的。没有视觉元素的文献评论是不完整的。在最终确定任何文件之前：
1. 至少生成一张原理图或图表（例如，用于系统审查的 PRISMA 流程图）
2. 优先选择2-3张图进行综合综述（检索策略流程图、主题综合图、概念框架）

* *如何生成图形：**
- 使用 **scientific-schematics** 技能生成人工智能驱动的出版物质量图表
- 用自然语言简单描述您想要的图表
- Nano Banana Pro 将自动生成、审查和完善原理图

* *如何生成原理图：**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

人工智能将自动：
- 创建具有适当格式的出版质量图像
- 通过多次迭代进行审查和完善
- 确保可访问性（色盲友好，高对比度）
- 将输出保存在图形/目录中

* *何时添加示意图：**
- 系统综述的 PRISMA 流程图
- 文献检索策略流程图
- 主题综合图
- 研究差距可视化图
- 引文网络图
- 概念框架插图
- 任何受益于的复杂概念可视化

有关创建原理图的详细指导，请参阅scientific-schematics技能文档。

- --

## 核心工作流程

文献评审遵循结构化的多阶段工作流程：

### 阶段1：规划和范围界定

1. **定义研究问题**：使用 PICO 框架（群体、干预、比较、结果）进行临床/生物医学审查
  - 示例：“与标准护理 (C)相比，CRISPR-Cas9 (I)治疗镰状细胞病 (P)的功效如何？”

2. **建立范围和目标**：
  - 定义清晰、具体的研究问题
  - 确定评论类型（叙述性、系统性、范围界定、荟萃分析）
  - 设置边界（时间段、地理范围、研究类型）

3. **制定搜索策略**：
  - 从研究问题中识别 2-4 个主要概念
  - 列出每个概念的同义词、缩写和相关术语
  - 计划布尔运算符（AND、OR、NOT）来组合术语
  - 选择至少 3 个互补数据库
  - **使用 parallel-web 技能(`parallel-cli search`)用于初始范围界定**，以便在正式数据库搜索之前快速评估情况

4. **设置纳入/排除标准**：
  - 日期范围（例如，过去 10 年：2015-2024）
  - 语言（通常为英语，或指定多语言）
  - 出版物类型（同行评审、预印本、评论）
  - 研究设计（RCT、观察性、体外、等）
  - 清楚地记录所有标准

### 第 2 阶段：系统文献检索

1. **多数据库搜索**：

 选择适合该域的数据库。 **始终从 parallel-web 开始以获得广泛的学术覆盖**，然后补充特定领域的数据库。

 * *基于网络的学术搜索（parallel-web 技能 — 从这里开始）：**
  - 使用 `parallel-cli search` 进行学术领域过滤以实现广泛的学术覆盖
  - 运行两种搜索：以学术为重点的 + 一般性的以捕获所有相关的resources
 ```bash
 # 跨学术来源的学术搜索
并行 cli 搜索 "你的研究主题" -q "keyword1" -q "keyword2" \
 - -json --max-results 10 --excerpt-max-chars-total 27000 \
  - -include-domains “scholar.google.com、arxiv.org、pubmed.ncbi.nlm.nih.gov、semanticscholar.org、biorxiv.org、medrxiv.org、ncbi.nlm.nih.gov、nature.com、science.org、ieee.org、acm.org、springer.com、wiley.com、cell.com、pnas.org、nih.gov”\
  - o来源/litreview_<主题>-academic.json

# 一般搜索补充来源
parallel-cli search "your研究主题" -q "keyword1" -q "keyword2" \
 - -json --max-results 10 --excerpt-max-chars-total 27000 \
  - osources/litreview_<topic>-general.json
 ```
 - 使用 `parallel-cli extract` 从搜索结果中找到的特定论文 URL 或 PDF 中获取完整内容
 ```bash
 并行 cli 提取 "https://arxiv.org/abs/XXXX.XXXXX" --json
 ```

 * *生物医学和生命科学：**
  - 使用`gget` 技能：`gget search pubmed "search terms"` 用于 PubMed/PMC
  - 使用 `gget` 技能：`gget search biorxiv "search terms"` 用于预印本
  - 使用 `bioservices` 技能用于 ChEMBL、KEGG、UniProt 等 

  * *General Scientific文献：**
  - 通过直接 API 搜索 arXiv（物理、数学、CS、q-bio 中的预印本）
  - 通过 API 搜索语义学者（2 亿多篇论文，跨学科）
  - 使用 Google Scholar 进行全面覆盖（手动或仔细抓取）

  * *专业数据库：**
  - 使用 `gget alphafold` 获取蛋白质结构
  - 使用 `gget cosmic` 获取癌症基因组学
  - 使用 `datacommons-client` 获取人口/统计数据
  - 使用适合域的专用数据库

2. **文档搜索参数**：
 ```markdown
 ## 搜索策略

 ### 数据库：PubMed
 - **搜索日期**：2024-10-25
  - **日期范围**：2015-01-01 至2024-10-25
  - **搜索字符串**：
``
（“CRISPR”[标题] OR“Cas9”[标题]）
 AND（“镰状细胞”[MeSH] OR“SCD”[标题/摘要]）
 AND 2015:2024[发布日期]
 ```
 - **结果**：247 篇文章
 ```

 对搜索的每个数据库重复。

3. **导出和聚合结果**：
  - 从每个数据库以 JSON 格式导出结果
  - 将所有结果合并到一个文件中
  - 使用 `scripts/search_databases.py` 进行后处理：
 ```bash
 python search_databases.py linked_results.json \
 - -deduplicate \
  - -format markdown \
  - -outputaggreged_results.md
 ```

### 第 3 阶段：筛选和选择

1. **重复数据删除**：
 ```bash
 python search_databases.py results.json --deduplicate --output unique_results.json
 ```
 - 按 DOI（主要）或标题（后备）删除重复项 
  - 删除重复项的文档数量

2. **标题筛选**：
  - 根据纳入/排除标准审查所有标题
  - 排除明显不相关的研究
  - 此阶段排除的文献编号

3. **摘要筛选**：
  - 阅读剩余研究的摘要
  - 严格应用纳入/排除标准
  - 记录排除的原因

4. **全文筛选**：
  - 获取剩余研究的全文
  - 根据所有标准进行详细审查
  - 记录排除的具体原因
  - 记录纳入研究的最终数量

5. **创建 PRISMA 流程图**：
 ```
 初始检索：n = X
 ├─ 去重后：n = Y
 ├─ 标题筛选后：n = Z
 ├─ 摘要筛选后：n = A
 └─ 包含在审查：n = B
 ```

### 第 4 阶段：数据提取和质量评估

1. **从每项纳入的研究中提取关键数据**：
  - 研究元数据（作者、年份、期刊、DOI）
  - 研究设计和方法
  - 样本量和人群特征
  - 主要发现和结果
  - 作者指出的局限性
  - 资金来源和冲突兴趣

2. **评估研究质量**：
  - **对于随机对照试验**：使用 Cochrane 偏倚风险工具
  - **对于观察性研究**：使用纽卡斯尔-渥太华量表
  - **对于系统评价**：使用 AMSTAR 2
  - 对每项研究进行评级：高、中、低或极低质量
  - 考虑不包括质量非常低的研究

3. **按主题组织**：
  - 确定研究中的 3-5 个主要主题
  - 按主题进行分组研究（研究可能出现在多个主题中）
  - 注意模式、共识和争议

### 第 5 阶段：综合和分析

1. **从模板创建评论文档**：
 ```bash
 cp asset/review_template.md my_literature_review.md
 ```

2. **撰写主题综合**（不是逐个研究的摘要）：
  - 按主题或研究问题组织结果部分
  - 综合每个主题内多项研究的发现
  - 比较和对比不同的方法和结果
  - 确定共识领域和争议点
  - 突出最强的证据

 示例结构：
 ```markdown
 #### 3.3.1 主题：CRISPR 递送方法

已经研究了用于治疗性
 基因编辑的多种递送方法。 15 项研究中使用了病毒载体 (AAV)^1-15^，
 显示出高转导效率 (65-85%)，但提高了免疫原性
 问题^3,7,12^。相比之下，脂质纳米粒子表现出较低的
效率（40-60%），但改善了安全性^16-23^.
 ```

3. **批判性分析**：
  - 评估研究中方法论的优势和局限性
  - 评估证据的质量和一致性
  - 确定知识差距和方法论差距
  - 注明需要未来研究的领域

4. **撰写讨论**：
  - 在更广泛的背景下解释研究结果
  - 讨论临床、实践或研究意义
  - 承认评论本身的局限性
  - 如果适用，与之前的评论进行比较
  - 提出具体的未来研究方向

### 第6阶段：引文验证

* *关键**：在最终提交之前，必须验证所有引文的准确性。

1. **验证所有 DOI**：
 ```bash
 python script/verify_itations.py my_literature_review.md
 ```

 此脚本：
 - 从文档中提取所有 DOI
  - 验证每个 DOI 是否正确解析
  - 从 CrossRef
 检索元数据 - 生成验证报告
 - 输出格式正确的引文

2. **审查验证报告**：
  - 检查是否有任何失败的 DOIs
  - 验证作者姓名、标题和出版物详细信息是否匹配
  - 更正原始文档中的任何错误
  - 重新运行验证，直到所有引用通过

3. **一致地格式化引文**：
  - 选择一种引文样式并在整个过程中使用（请参阅 `references/citation_styles.md`）
  - 常见样式：APA、Nature、Vancouver、Chicago、IEEE
  - 使用验证脚本输出正确格式化引文
  - 确保文本引文匹配参考列表格式

### 第 7 阶段：文档生成

1. **生成 PDF**:
 ```bash
 python script/generate_pdf.py my_literature_review.md \
 - -引用样式 apa \
  - -output my_review.pdf
 ```

选项：
 - `--citation-style`：apa、nature、chicago、vancouver、ieee
  - `--no-toc`：禁用目录
  - `--no-numbers`：禁用章节编号
  - `--check-deps`：检查pandoc/xelatex是否为已安装

2. **查看最终输出**：
  - 检查 PDF 格式和布局
  - 验证所有部分是否存在
  - 确保引文正确呈现
  - 检查数字/表格是否正确显示
  - 验证目录是否准确

3. **质量检查表**：
  - [ ]所有 DOI 均通过 verify_itations.py 验证 
  - [ ]引文格式一致
  - [ ]包括 PRISMA 流程图（用于系统评价）
  - [ ]完整记录检索方法
  - [ ]明确说明纳入/排除标准
  - [ ]按主题组织的结果（不是逐个研究）
  - [ ]已完成质量评估
  - [ ]已确认局限性
  - [ ]参考文献完整且准确
  - [ ] PDF 生成无错误

## 数据库特定搜索指导

### PubMed / PubMed Central

通过`gget`访问技能：
```bash
# Search PubMed
gget search pubmed "CRISPR gene editing" -l 100

# Search with filters
# Use PubMed Advanced Search Builder to construct complex queries
# Then execute via gget or direct Entrez API
```

* *搜索提示**：
- 使用MeSH术语：`"sickle cell disease"[MeSH]`
- 字段标签： `[Title]`、`[Title/Abstract]`、`[Author]`
- 日期过滤器：`2020:2024[Publication Date]`
- 布尔运算符：AND、OR、NOT
- 请参阅 MeSH 浏览器：https://meshb.nlm.nih.gov/search

### bioRxiv / medRxiv

通过`gget`访问技能：
```bash
gget search biorxiv "CRISPR sickle cell" -l 50
```

* *重要注意事项**：
- 预印本未经同行评审
- 谨慎验证结果
- 检查预印本是否已通过已发布（CrossRef）
- 注意预印本版本和日期

### arXiv

通过直接API或WebFetch访问：
```python
# Example search categories:
# q-bio.QM (Quantitative Methods)
# q-bio.GN (Genomics)
# q-bio.MN (Molecular Networks)
# cs.LG (Machine Learning)
# stat.ML (Machine Learning Statistics)

# Search format: category AND terms
search_query = "cat:q-bio.QM AND ti:\"single cell sequencing\""
```

### Semantic Scholar

通过直接API访问（需要API密钥，或使用免费层）：
- 跨所有领域的 200M+ 论文
- 非常适合跨学科搜索
- 提供引用图和论文推荐
- 用于查找极具影响力的论文

### 专业生物医学数据库

使用适当的技能：
- **ChEMBL**：`bioservices` 化学生物活性技能 
- **UniProt**：`gget` 或 `bioservices` 蛋白质信息技能 
- **KEGG**：`bioservices` 通路和基因技能 
- **COSMIC**：用于癌症突变的 `gget` 技能
- **AlphaFold**：用于蛋白质结构的 `gget alphafold`
- **PDB**：用于实验结构的 `gget` 或直接 API

### 引文链 

通过引文网络扩展搜索：

1. **转发引用**（引用关键论文的论文）：
  - 使用 `parallel-cli search` 查找引用特定作品的论文：
 ```bash
 并行 cli 搜索“引用 [作者等人年份] [论文标题]的论文” \
 - q “引用” -q “[关键作者]” \
  - -json --max-results 10 --excerpt-max-chars-total 27000 \
  - -include-domains "scholar.google.com,semanticscholar.org,arxiv.org,pubmed.ncbi.nlm.nih.gov" \
  - o resources/litreview_forward_itations.json
 ```
 - 使用 Google Scholar“引用者”
  - 使用语义学者或 OpenAlex API
  - 识别基于开创性工作 

2 的较新研究。 **向后引用**（关键论文的引用）：
 - 使用 `parallel-cli extract` 获取关键论文的全文并提取其参考文献列表：
 ```bash
 parallel-cli extract "https://doi.org/10.xxxx/yyyy" --json
 ```
 - 从包含的论文中提取参考文献
  - 识别被高度引用的基础工作
  - 查找多个包含的研究引用的论文

## 引文风格指南

详细的格式指南位于`references/citation_styles.md`。快速参考：

### APA（第 7 版）
- 文本内：（Smith 等人，2023）
- 参考文献：Smith, J. D.、Johnson, M. L. 和 Williams, K. R. (2023)。标题。 *期刊*，*22*(4)，301-318。 https://doi.org/10.xxx/yyy

### Nature
- 文本内：上标数字^1,2^
- 参考文献：Smith, J. D.、Johnson, M. L. 和 Williams, K. R. 标题。 *纳特。 Rev. Drug Discov.* **22**, 301-318 (2023).

### 温哥华
- 文本内：上标数字 ^1,2^
- 参考文献：Smith JD、Johnson ML、Williams KR。标题。 Nat Rev 药物发现。 2023;22(4):301-18.

* *在最终确定之前，始终使用 verify_itations.py 验证引文**。

### 优先考虑高影响力论文（关键）

* *始终优先考虑来自知名作者和顶级场所的有影响力、高引用率的论文。** 文献中的质量比数量更重要评论。

#### 引用计数阈值

使用引用计数来识别最具影响力的论文：

|纸时代|引用阈值 |分类|
|---------|--------------------------------|----------------|
| 0-3岁| 20+ 次引用 |值得注意|
| 0-3岁| 100 多次引用 |极具影响力|
| 3-7年| 100 多次引用 |重要|
| 3-7年| 500 多次引用 |地标纸|
| 7 年以上 | 500 多次引用 |开创性工作|
| 7 年以上 | 1000+ 次引用 |基础 |

#### 期刊和场所级别

优先考虑来自较高级别场所的论文：

- **第 1 级（始终优先）：** Nature、Science、Cell、NEJM、Lancet、JAMA、PNAS、Nature Medicine、Nature Biotechnology
- **第 2 级（强烈优先）：**高影响力的专业期刊 (IF>10)、顶级会议 (NeurIPS、ICML for ML/AI)
- **第 3 层（相关时包含）：** 受人尊敬的专业期刊 (IF 5-10)
- **第 4 层（谨慎使用）：** 影响力较低的同行评审场所

#### 作者声誉评估

优先选择以下来源的论文：
- **具有高h指数（在既定领域> 40）的高级研究人员** 
- **知名机构（哈佛、斯坦福、麻省理工学院、牛津等）的领先研究小组** 
- **在相关领域发表多篇Tier-1出版物的作者** 
- **具有公认专业知识的研究人员**（奖项、编辑）职位、学会研究员）

#### 识别开创性论文

对于任何主题，通过以下方式识别基础工作：
1. **高引用次数**（5 年以上论文的引用次数通常为 500 以上）
2. **经常被其他纳入的研究引用**（出现在许多参考文献列表中）
3. **在一级场所发表**（自然、科学、细胞家族）
4. **由领域先驱撰写**（通常被引用为建立概念）

## 最佳实践

### 搜索策略
1. **从 parallel-web 开始**：在查询专业数据库 
2 之前，使用 `parallel-cli search` 与学术领域进行初步广泛覆盖。 **使用多个数据库**（至少 3 个）：确保全面覆盖 — parallel-web 算作一个来源 
3. **包括预印本服务器**：捕获最新未发表的发现
4. **记录一切**：搜索字符串、日期、结果计数以实现可重复性 - 将所有并行 cli 输出保存到 `sources/`
5. **测试和完善**：运行试点搜索，查看结果，调整搜索词
6. **按引用排序**：如果可用，请按引用计数对搜索结果进行排序，以首先显示有影响力的作品
7. **使用parallel-cli extract**：从搜索过程中找到的有希望的URL中获取完整内容，以在全文筛选之前验证相关性

### 筛选和选择
1. **使用多个数据库**（至少 3 个）：确保全面覆盖 
2. **包括预印本服务器**：捕获最新未发表的发现
3. **记录一切**：搜索字符串、日期、结果计数以实现可重复性
4. **测试和完善**：运行试点搜索，审查结果，调整搜索词

### 筛选和选择
1. **使用明确的标准**：筛选前记录纳入/排除标准
2. **系统筛选**：标题→摘要→全文
3. **文件排除**：记录排除研究的原因
4. **考虑双重筛选**：对于系统评价，请两名审稿人独立筛选

### Synthesis
1. **按主题组织**：按主题分组，而不是按个人研究
2. **跨研究综合**：比较、对比、识别模式
3. **保持批判性**：评估证据的质量和一致性
4. **找出差距**：注意遗漏或未充分研究的内容

### 质量和再现性
1. **评估研究质量**：使用适当的质量评估工具
2. **验证所有引文**：运行 verify_itations.py 脚本
3. **文档方法**：提供足够的细节供其他人重现
4. **遵循指南**：使用 PRISMA 进行系统评价

### 写作
1. **客观**：公平地提供证据，承认局限性
2. **系统化**：遵循结构化模板
3. **具体**：包括数字、统计数据、效果大小（如果有）
4. **清晰**：使用清晰的标题、逻辑流程、主题组织

## 要避免的常见陷阱

1. **单一数据库检索**：遗漏相关论文；总是搜索多个数据库
2. **没有搜索文档**：使得审查不可重复；记录所有搜索
3. **逐项研究总结**：缺乏综合；按主题组织，而不是
4. **未经验证的引用**：导致错误；始终运行 verify_itations.py
5. **搜索范围太广**：产生数千个不相关的结果；使用特定术语进行细化
6. **搜索范围太窄**：错过相关论文；包括同义词和相关术语
7. **忽略预印本**：错过最新发现；包括bioRxiv、medRxiv、arXiv
8. **无质量评估**：平等对待所有证据；评估并报告质量
9. **发表偏倚**：仅发表正面结果；注意潜在的偏差
10. **过时的搜索**：领域发展迅速；明确说明检索日期

## 工作流程示例

生物医学文献综述的完整工作流程：

```bash
# 1. Create review document from template
cp assets/review_template.md crispr_sickle_cell_review.md

# 2. Start with parallel-web for broad academic search
parallel-cli search "CRISPR Cas9 sickle cell disease gene therapy efficacy" \
  -q "CRISPR" -q "sickle cell" -q "gene therapy" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  --include-domains "scholar.google.com,arxiv.org,pubmed.ncbi.nlm.nih.gov,semanticscholar.org,biorxiv.org,nature.com,science.org,cell.com,pnas.org,nih.gov" \
  -o sources/litreview_crispr_scd-academic.json

parallel-cli search "CRISPR sickle cell disease clinical trials treatment" \
  -q "CRISPR" -q "sickle cell" \
  --json --max-results 10 --excerpt-max-chars-total 27000 \
  -o sources/litreview_crispr_scd-general.json

# 3. Search specialized databases using appropriate skills
# - Use gget skill for PubMed, bioRxiv
# - Use direct API access for arXiv, Semantic Scholar
# - Export results in JSON format

# 4. Aggregate and process results (combine parallel-cli + database results)
python scripts/search_databases.py combined_results.json \
  --deduplicate \
  --rank citations \
  --year-start 2015 \
  --year-end 2024 \
  --format markdown \
  --output search_results.md \
  --summary

# 5. Screen results and extract data
# - Use parallel-cli extract to fetch full content from promising URLs
# - Manually screen titles, abstracts, full texts
# - Extract key data into the review document
# - Organize by themes

# 6. Write the review following template structure
# - Introduction with clear objectives
# - Detailed methodology section
# - Results organized thematically
# - Critical discussion
# - Clear conclusions

# 7. Verify all citations
python scripts/verify_citations.py crispr_sickle_cell_review.md

# Review the citation report
cat crispr_sickle_cell_review_citation_report.json

# Fix any failed citations and re-verify
python scripts/verify_citations.py crispr_sickle_cell_review.md

# 8. Generate professional PDF
python scripts/generate_pdf.py crispr_sickle_cell_review.md \
  --citation-style nature \
  --output crispr_sickle_cell_review.pdf

# 9. Review final PDF and markdown outputs
```

## 与其他技能的集成

此技能与其他科学技能无缝配合：

### 网络搜索和提取（parallel-web技能- PRIMARY)
- **parallel-cli 搜索**：具有域过滤功能的广泛学术和一般网络搜索 — 用于初始范围界定、查找论文、引文链接和补充搜索
- **parallel-cli 提取**：从论文 URL、期刊网站和预印本服务器获取完整内容 — 用于阅读摘要、提取参考文献列表和验证论文详细信息
- **parallel-cli 搜索 --include-domains**：跨学术领域（arxiv.org、pubmed、nature.com 等）的学术搜索 

### 数据库访问技能
- **gget**：PubMed、bioRxiv、COSMIC、AlphaFold、Ensembl、UniProt
- **bioservices**：ChEMBL、KEGG、Reactome、UniProt、PubChem
- **datacommons-client**：人口统计、经济学、健康统计

### 分析技能
- **pydeseq2**：RNA-seq差异表达（用于方法部分）
- **scanpy**：单细胞分析（用于方法部分）
- **anndata**：单细胞数据（用于方法部分）
- **biopython**：序列分析（用于背景部分）

### 可视化技能
- **matplotlib**：生成图形和绘图以供审阅
- **seaborn**：统计可视化

### 写作技能
- **品牌指南**：将机构品牌应用于 PDF
- **内部通信**：针对不同受众调整审阅

## 资源

### 捆绑资源

* *脚本：**
- `scripts/verify_citations.py`：验证 DOI 并生成格式化引文
- `scripts/generate_pdf.py`：将 markdown 转换为专业 PDF
- `scripts/search_databases.py`：处理、重复数据删除和格式化搜索结果

* *参考文献：**
- `references/citation_styles.md`：详细的引文格式指南（APA、Nature、Vancouver、Chicago、IEEE）
- `references/database_strategies.md`：综合数据库检索策略

* *资产：**
- `assets/review_template.md`：包含所有部分的完整文献综述模板

### 外部资源

* *指南：**
- PRISMA（系统综述）： http://www.prisma-statement.org/
- Cochrane 手册：https://training.cochrane.org/handbook
- AMSTAR 2（审核质量）：https://amstar.ca/

* *工具：**
- MeSH 浏览器： https://meshb.nlm.nih.gov/search
  - PubMed 高级搜索：https://pubmed.ncbi.nlm.nih.gov/advanced/
  - 布尔搜索指南：https://www.ncbi.nlm.nih.gov/books/NBK3827/

* *引文风格：**
- APA 风格：https://apastyle.apa.org/
- 自然作品集：https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards
- NLM/Vancouver： https://www.nlm.nih.gov/bsd/uniform_requirements.html

## 依赖项

### 所需的 CLI 工具
```bash
# parallel-cli (PRIMARY — for web search and URL extraction)
curl -fsSL https://parallel.ai/install.sh | bash
# Or: uv tool install "parallel-web-tools[cli]"
# Authenticate: parallel-cli auth
```

### 所需的 Python 包
```bash
pip install requests  # For citation verification
```

### 所需的系统工具
```bash
# For PDF generation
brew install pandoc  # macOS
apt-get install pandoc  # Linux

# For LaTeX (PDF generation)
brew install --cask mactex  # macOS
apt-get install texlive-xetex  # Linux
```

Check依赖项：
```bash
python scripts/generate_pdf.py --check-deps
```

## 总结

此literature-review技能提供：

1. **系统方法**遵循学术最佳实践
2. **Parallel-web 支持的搜索** 使用 `parallel-cli search` 通过学术领域过滤 
3 进行快速、广泛的学术文献发现。 **多数据库集成**通过现有的科学技能（gget、bioservices、datacommons-client）
4. **引文验证**确保准确性和可信度
5. **专业输出**，采用 Markdown 和 PDF 格式 
6. **全面指导**涵盖整个审核过程
7. **质量保证** 使用验证和确认工具
8. **可重复性**通过详细的文档要求

进行全面、严格的文献综述，以满足学术标准并提供任何领域当前知识的全面综合。
