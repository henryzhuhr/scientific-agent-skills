# 引文质量检查表

使用此检查表可确保您的引文在最终提交之前准确、完整且格式正确。

## 提交前检查表

### ✓ 元数据准确性

- [ ]所有作者姓名均正确且格式正确
- [ ]文章标题与实际出版物相符
- [ ]期刊/会议名称完整（除非需要，否则不缩写）
- [ ]出版年份准确 
- [ ]卷号和期号正确 
- [ ]页面范围准确 

### ✓ 必填字段 

- [ ]所有 @article 条目都有：作者、标题、期刊、 year
- [ ]所有 @book 条目均具有：作者/编辑、标题、出版商、year
- [ ]所有 @inproceedings 条目均具有：作者、标题、书名、年份
- [ ]现代论文 (2000+)包括可用的 DOI
- [ ]所有条目均具有唯一引用键

### ✓ DOI 验证

- [ ]所有 DOI 格式均正确 (10.XXXX/...)
- [ ] DOI 正确解析为文章
- [ ] BibTeX 字段中没有 DOI 前缀（没有“doi:”或"https://doi.org/")
- [ ] CrossRef 中的元数据与您的 BibTeX 条目相匹配 
- [ ]运行： `python scripts/validate_citations.py references.bib --check-dois`

### ✓ 格式一致性

- [ ]页面范围使用双连字符 (--)而不是单连字符 (-)
- [ ]没有“页”。页面字段中的前缀
- [ ]作者姓名使用“和”分隔符（不是分号或与号）
- [ ]标题中的大写保护（{AlphaFold}、{CRISPR}等）
- [ ]月份名称使用标准缩写（如果包含）
- [ ]引文键遵循一致格式

### ✓ 重复检测

- [ ]参考书目中没有重复的DOI
- [ ]没有重复的引文关键字
- [ ]没有接近重复的标题
- [ ]预印本在可用时更新为已发布的版本
- [ ]运行： `python scripts/validate_citations.py references.bib`

### ✓ 特殊字符

- [ ]重音字符格式正确（例如，{\"u} 表示 ü）
- [ ]数学符号使用 LaTeX 命令
- [ ]化学公式格式正确 
- [ ]没有未转义的特殊字符（%、&、$、# 等）

### ✓ BibTeX语法

- [ ]所有条目都有平衡大括号 {}
- [ ]以逗号分隔的字段
- [ ]每个条目中最后一个字段后没有逗号
- [ ]有效条目类型（@article、@book 等）
- [ ]运行： `python scripts/validate_citations.py references.bib`

### ✓ 文件组织

- [ ]参考书目按逻辑顺序排序（按年份、作者或关键词）
- [ ]整个格式保持一致
- [ ]条目之间没有格式不一致
- [ ]运行： `python scripts/format_bibtex.py references.bib --sort year`

## 自动验证

### 步骤 1：格式化和清理

```bash
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output clean_references.bib
```

* *作用**：
- 删除重复项
- 标准化格式
- 修复常见问题（页面范围、DOI 格式等）
- 按年份排序（最新的在前）

### 步骤 2：验证

```bash
python scripts/validate_citations.py clean_references.bib \
  --check-dois \
  --report validation_report.json \
  --verbose
```

* *作用**：
- 检查必填字段
- 验证 DOI解析
- 检测重复项
- 验证语法
- 生成详细报告

### 步骤3：查看报告

```bash
cat validation_report.json
```

* *解决任何**：
- **错误**：必须修复（缺少字段、损坏） DOI、语法错误）
- **警告**：应修复（缺少推荐字段、格式问题）
- **重复**：删除或合并

### 步骤 4：最终检查

```bash
python scripts/validate_citations.py clean_references.bib --verbose
```

* *目标**：零错误，最小警告

## 手动审核清单

### 关键引用（前 10-20 个最重要）

对于最重要的引用，请手动验证：

- [ ]访问 DOI 链接并确认其是正确的文章
- [ ]根据实际出版物检查作者姓名
- [ ]验证年份是否与出版日期匹配
- [ ]确认期刊/会议名称是否正确
- [ ]检查卷/页数是否匹配

### 需要注意的常见问题

* *缺少信息**：
- [ ] 2000 年之后发表的论文没有 DOI
- [ ]缺少期刊文章的卷号或页码 
- [ ]缺少书籍出版商 
- [ ]缺少会议记录的会议地点 

  * *格式错误**：
- [ ] Single页码范围中的连字符 (123-145 → 123--145)
- [ ]作者列表中的 & 符号 (Smith & Jones → Smith and Jones)
- []标题中不受保护的首字母缩写词 (DNA → {DNA})
- [ ] DOI 包括 URL 前缀 (https://doi.org/10.xxx → 10.xxx)

* *元数据不匹配**：
- [ ]作者姓名与出版物不同
- [ ]年份为在线出版物，而不是印刷出版物
- [ ]期刊名称在应完整时缩写
- [ ]卷/期号交换

* *重复项**：
- [ ]以不同的引文关键字引用同一篇论文
- [ ]预印本和出版版本均被引用
- [ ]会议论文和期刊版本均被引用

## 特定领域检查

### 生物医学Sciences

- [ ] PubMed Central ID (PMCID)包括（如果可用）
- [ ] MeSH 术语适当（如果使用）
- [ ]包括临床试验注册号（如果适用）
- [ ]准确引用的所有治疗/药物参考

### 计算机科学

- [ ]预印本中包含 arXiv ID
- []正确引用会议记录（不仅仅是“NeurIPS”）
- []软件/数据集引用包括版本号
- [] GitHub 链接稳定且永久

### General Sciences

- []正确数据可用性声明被引用的
- [ ]已识别并删除的撤回论文
- [ ]检查已发布版本的预印本
- [ ]关键时引用的补充材料

## 最终预提交步骤

### 提交前1周

- [ ]通过 DOI 检查运行全面验证
- [ ]修复所有错误和严重警告
- [ ]手动验证前 10-20 个最重要的引文 
- [ ]检查任何撤回的论文

### 提交前 3 天

- [ ]在任何手动操作后重新运行验证edits
- [ ]确保所有文内引文都有相应的参考书目条目
- [ ]确保文本中引用所有参考书目条目
- [ ]检查引文风格是否符合期刊要求

### 提交前1天

- [ ]最终验证检查
- [ ] LaTeX编译成功，没有警告
- [ ] PDF 正确呈现所有引用
- [ ]参考书目以正确的格式显示
- [ ]无占位符引用（Smith 等人 XXXX）

### 提交日

- [ ]一次最终验证run
- [ ]没有最后一刻的编辑，无需重新验证
- [ ]提交包中包含的参考书目文件
- [ ]文本中引用的图/表匹配参考书目

## 质量指标

### 优秀参考书目

- ✓ 100% 的条目有 DOI（对于现代论文）
- ✓ 零验证错误
- ✓ 零缺失必填字段
- ✓ 零损坏的 DOI
- ✓ 零重复 
- ✓ 始终保持一致的格式
- ✓ 所有手动引用抽查

### 可接受的参考书目

- ✓ 90%以上的现代条目有DOIs
- ✓ 零高严重性错误
- ✓ 仅轻微警告（例如，缺少推荐字段）
- ✓ 手动验证关键引文
- ✓ 编译成功，没有错误

### 需要改进

- ✗ 最近论文缺少 DOI
- ✗ 高严重性验证错误
- ✗ 损坏或不正确的 DOIs
- ✗ 重复条目
- ✗格式不一致
- ✗ 编译警告或错误

## 紧急修复

如果您在最后一刻发现问题：

### 损坏的 DOI

```bash
# Find correct DOI
# Option 1: Search CrossRef
# https://www.crossref.org/

# Option 2: Search on publisher website
# Option 3: Google Scholar

# Re-extract metadata
python scripts/extract_metadata.py --doi CORRECT_DOI
```

### 缺失信息

```bash
# Extract from DOI
python scripts/extract_metadata.py --doi 10.xxxx/yyyy

# Or from PMID (biomedical)
python scripts/extract_metadata.py --pmid 12345678

# Or from arXiv
python scripts/extract_metadata.py --arxiv 2103.12345
```

### 重复条目

```bash
# Auto-remove duplicates
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --output fixed_references.bib
```

### 格式错误

```bash
# Auto-fix common issues
python scripts/format_bibtex.py references.bib \
  --output fixed_references.bib

# Then validate
python scripts/validate_citations.py fixed_references.bib
```

## 长期最佳实践

### 研究期间

- [ ]在找到引用时将其添加到参考书目文件
- [ ]立即使用提取元数据DOI
- [ ]每添加 10-20 次后进行验证
- [ ]将参考书目文件置于版本控制之下

### 写作期间

- [ ]边写边引用
- [ ]使用一致的引用键
- [ ]不要延迟添加参考文献
- [ ]每周验证

### 提交前

- [ ]允许2-3 天进行引文清理
- [ ]不要等到最后一天
- [ ]自动化你能做的
- [ ]手动验证关键引用

## 工具快速参考

### 提取元数据

```bash
# From DOI
python scripts/doi_to_bibtex.py 10.1038/nature12345

# From multiple sources
python scripts/extract_metadata.py \
  --doi 10.1038/nature12345 \
  --pmid 12345678 \
  --arxiv 2103.12345 \
  --output references.bib
```

### 验证

```bash
# Basic validation
python scripts/validate_citations.py references.bib

# With DOI checking (slow but thorough)
python scripts/validate_citations.py references.bib --check-dois

# Generate report
python scripts/validate_citations.py references.bib \
  --report validation.json \
  --verbose
```

### 格式和Clean

```bash
# Format and fix issues
python scripts/format_bibtex.py references.bib

# Remove duplicates and sort
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output clean_refs.bib
```

## 摘要

* *最低要求**：
1. 运行`format_bibtex.py --deduplicate`
2. 运行`validate_citations.py`
3. 修复所有错误
4. 编译成功

* *推荐**：
1. 格式化、重复数据删除和排序
2. 使用 `--check-dois`
3 进行验证。修复所有错误和警告
4. 手动验证最高引用
5. 修复后重新验证

* *最佳实践**：
1. 在整个研究过程中进行验证
2. 始终如一地使用自动化工具
3. 保持参考书目整洁有序
4. 记录任何特殊情况
5. 提交前 1-3 天进行最终验证

* *记住**：引用错误对您的奖学金影响不佳。花时间确保准确性是值得的！
