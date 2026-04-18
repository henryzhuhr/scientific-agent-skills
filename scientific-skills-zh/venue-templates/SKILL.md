---
name: venue-templates
description: 访问主要科学出版场所（Nature、Science、PLOS、IEEE、ACM）、学术会议（NeurIPS、ICML、CVPR、CHI）、研究海报和资助提案（NSF、NIH、DOE、DARPA）的全面 LaTeX 模板、格式要求和提交指南。在准备期刊投稿、会议论文、研究海报或拨款提案的手稿并需要特定于场地的格式要求和模板时，应使用此技能。
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 场地模板

## 概述

访问主要科学出版场地、学术会议、研究海报和资助提案的综合 LaTeX 模板、格式要求和提交指南。此技能为成功跨学科学术提交提供现成的模板和详细规范。

 在准备提交期刊、会议论文、研究海报或资助提案的手稿并需要特定地点的格式要求和模板时使用此技能。

## 何时使用此技能

此技能应在以下情况下使用：
- 准备提交给特定期刊的手稿（《自然》、《科学》、 PLOS、IEEE 等）
- 撰写具有特定格式要求的会议论文（NeurIPS、ICML、CHI 等）
- 为会议创建学术研究海报
- 为联邦机构（NSF、NIH、DOE、DARPA）或私人基金会起草资助提案
- 检查目标的格式要求和页数限制场地
- 使用作者信息和项目详细信息自定义模板
- 验证文档是否符合场地规范

## 科学原理图的视觉增强

* *使用此技能创建文档时，请始终考虑添加科学图表和原理图以增强视觉传达。**

如果您的文档尚未包含原理图或图表：
- 使用 **scientific-schematics** 技能生成人工智能驱动的出版质量图表
- 用自然语言简单地描述您想要的图表
- Nano Banana Pro 将自动生成、审查和完善原理图

* *对于新文档：** 应默认生成科学原理图，以直观地表示中描述的关键概念、工作流程、架构或关系文字.

* *如何生成原理图：**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

人工智能将自动：
- 创建具有正确格式的出版质量图像
- 通过多次迭代进行审查和完善
- 确保可访问性（色盲友好，高对比度）
- 在图中保存输出/目录

* *何时添加原理图：**
- 论文方法流程图
- 概念框架图
- 系统架构图
- 数据流程图
- 实验设计可视化
- 研究工作流程图
- 任何受益于的复杂概念可视化

有关创建原理图的详细指导，请参阅scientific-schematics技能文档。

- --

## 核心功能

### 1.期刊文章模板

访问50多种跨学科主要科学期刊的LaTeX模板和格式指南：

* *自然组合**：
- 自然、自然方法、自然生物技术、自然机器智能
- 自然通讯、自然协议
- 科学报告

* *科学家族**：
- 科学、科学进展、科学转化医学
- 科学免疫学、科学机器人学

* *PLOS（公共科学图书馆）**：
- PLOS ONE、PLOS 生物学、PLOS 计算生物学
- PLOS 医学、PLOS 遗传学

* *细胞出版社**：
- 细胞、神经元、免疫、细胞报告
- 分子细胞，发育细胞

* *IEEE出版物**：
- IEEE Transactions（各学科）
- IEEE Access，IEEE期刊模板

* *ACM出版物**：
- ACM Transactions，ACM会议通讯
- ACM会议会议记录

* *其他主要出版商**：
- Springer 期刊（各学科）
- Elsevier 期刊（自定义模板）
- Wiley 期刊
- BMC 期刊
- Frontiers 期刊

### 2. 会议论文模板

具有适合主要学术会议格式的会议特定模板：

* *机器学习和人工智能**：
- NeurIPS（神经信息处理系统）
- ICML（国际机器学习会议）
- ICLR（国际学习表示会议）
- CVPR（计算机视觉与模式）识别）
- AAAI（人工智能促进协会）

* *计算机科学**：
- ACM CHI（人机交互）
- SIGKDD（知识发现和数据挖掘）
- EMNLP（自然语言经验方法）处理）
- SIGIR（信息检索）
- USENIX 会议

* *生物学与生物信息学**：
- ISMB（分子生物学智能系统）
- RECOMB（计算分子研究）生物学）
- PSB（太平洋生物计算研讨会）

* *工程**：
- IEEE会议模板（各学科）
- ASME、AIAA会议

### 3.研究海报模板

会议学术海报模板演示：

* *标准格式**：
- A0 (841 × 1189 mm / 33.1 × 46.8 in)
- A1 (594 × 841 mm / 23.4 × 33.1 in)
- 36" × 48" (914 × 1219 mm) - 常见美国尺寸
- 42" × 56" (1067 × 1422 mm)
- 48" × 36"（横向）

* *模板包**：
- **beamerposter**：经典学术海报模板
- **tikzposter**：现代、丰富多彩的海报设计
- **baposter**：结构化多列布局

* *设计功能**：
- 远距离可读的最佳字体大小
- 配色方案（色盲安全调色板）
- 网格布局和列结构
- 补充材料二维码集成

### 4.拨款提案模板

主要资助机构的模板和格式要求：

* *NSF（国家科学基金会）**：
- 完整提案模板（15 页项目描述）
- 项目摘要（1 页：概述、智力优点、更广泛的影响）
- 预算和预算理由
- 传记草图（3 页限制）
- 设施、设备和其他资源
- 数据管理计划

* *NIH（美国国立卫生研究院）**：
- R01 研究补助金（多年）
- R21 探索/发展补助金
- K 奖（职业发展）
- 具体目标页（1 页，最关键的组成部分）
- 研究策略（意义、创新、方法）
- 传记概要（5 页限制）

* *DOE（能源部）**：
- 科学提案办公室
- ARPA-E 模板
- 技术成熟度 (TRL)描述
- 商业化和影响章节

* *DARPA（国防高级研究计划局）**：
- BAA（广泛机构公告）响应
- Heilmeier 教义问答框架
- 技术方法和里程碑
- 过渡规划

* *私人基金会**：
- 盖茨基金会
- Wellcome Trust
- 霍华德休斯医学研究所 (HHMI)
- 陈·扎克伯格倡议 (CZI)

## 工作流程：查找和使用模板

### 第 1 步：确定目标地点

确定具体的发布地点、会议或资助机构：

```
Example queries:
- "I need to submit to Nature"
- "What are the requirements for NeurIPS 2025?"
- "Show me NSF proposal formatting"
- "I'm creating a poster for ISMB"
```

### 步骤2：查询模板和要求

访问特定地点的模板和格式指南：

* *对于期刊**：
```bash
# Load journal formatting requirements
Reference: references/journals_formatting.md
Search for: "Nature" or specific journal name

# Retrieve template
Template: assets/journals/nature_article.tex
```

* *会议用**：
```bash
# Load conference formatting
Reference: references/conferences_formatting.md
Search for: "NeurIPS" or specific conference

# Retrieve template
Template: assets/journals/neurips_article.tex
```

* *海报用**：
```bash
# Load poster guidelines
Reference: references/posters_guidelines.md

# Retrieve template
Template: assets/posters/beamerposter_academic.tex
```

* *用补助金**：
```bash
# Load grant requirements
Reference: references/grants_requirements.md
Search for: "NSF" or specific agency

# Retrieve template
Template: assets/grants/nsf_proposal_template.tex
```

### 步骤 3：查看格式要求

在定制之前检查关键规格：

* *验证的关键要求**：
- 页面限制（因地点而异）
- 字体大小和系列
- 页边距规格
- 行间距
- 引文样式（APA、温哥华、自然等）
- 图/表格要求
- 文件格式（PDF、Word、LaTeX 源）
- 匿名（用于双盲审核）
- 补充材料限制

### 步骤 4：自定义模板

使用帮助程序脚本或手动自定义：

* *选项 1：帮助程序脚本（推荐）**：
```bash
python scripts/customize_template.py \
  --template assets/journals/nature_article.tex \
  --title "Your Paper Title" \
  --authors "First Author, Second Author" \
  --affiliations "University Name" \
  --output my_nature_paper.tex
```

* *选项2：手动编辑**：
- 打开模板文件
- 替换占位符文本（用注释标记）
- 填写标题，作者，所属单位，摘要
- 将您的内容添加到每个第 5 步：验证格式

检查是否符合场地要求：

```bash
python scripts/validate_format.py \
  --file my_paper.pdf \
  --venue "Nature" \
  --check-all
```

* *验证检查**：
- 页数在限制内
- 字体大小正确
- 边距符合要求规格
- 参考格式正确
- 图形满足分辨率要求

### 步骤6：编译和审查

编译LaTeX并审查输出：

```bash
# Compile LaTeX
pdflatex my_paper.tex
bibtex my_paper
pdflatex my_paper.tex
pdflatex my_paper.tex

# Or use latexmk for automated compilation
latexmk -pdf my_paper.tex
```

审查清单：
- []所有部分均存在且正确formatted
- [ ]引文正确呈现
- [ ]数字显示时带有正确的标题
- [ ]限制内的页数
- [ ]遵循作者指南
- [ ]准备的补充材料（如果需要）

## 与其他集成技能

此技能与其他科学技能无缝配合：

### 科学写作
- 使用**scientific-writing**技能进行内容指导（IMRaD结构、清晰度、精度）
- 应用此技能中的特定场地模板进行格式化
- 结合以完成完整的稿件准备

### 文学回顾
- 使用**literature-review**技能进行系统文献检索和综合
- 根据场地要求应用适当的引文风格
- 根据模板规范格式化参考文献

### 同行评审
- 使用 **peer-review** 技能评估稿件质量
- 使用此技能验证格式合规性
- 确保遵守报告指南（CONSORT、STROBE 等）

### 研究资助
- 与内容的 **research-grants** 技能交叉引用策略
- 使用此技能进行机构特定的模板和格式设置
- 结合进行全面的赠款提案准备

### LaTeX 海报
- 此技能提供与场地无关的海报模板
- 用于会议特定的海报要求
- 与图形创建的可视化技能集成

## 模板分类

### 按文档类型

|类别 |模板计数 |常用场地 |
|---------|---------------|---------------|
| **期刊文章** | 30+ |自然、科学、PLOS、IEEE、ACM、细胞出版社 |
| **会议论文** | 20+ | NeurIPS、ICML、CVPR、CHI、ISMB |
| **研究海报** | 10+ | A0、A1、36×48、各种封装|
| **拨款提案** | 15+ | NSF、NIH、DOE、DARPA、基金会 |

### 按学科 

|纪律 |支持场地 |
|------------------------|--------------------|
| **生命科学** | Nature、Cell Press、PLOS、ISMB、RECOMB |
| **物理科学** |科学、物理评论、ACS、APS |
| **工程** | IEEE、ASME、AIAA、ACM |
| **计算机科学** | ACM、IEEE、NeurIPS、ICML、ICLR |
| **医学** | NEJM、柳叶刀、JAMA、BMJ |
| **跨学科** | PNAS、自然通讯、科学进展 |

## 帮助程序脚本

### query_template.py

按地点名称、类型或关键字搜索和检索模板：

```bash
# Find templates for a specific journal
python scripts/query_template.py --venue "Nature" --type "article"

# Search by keyword
python scripts/query_template.py --keyword "machine learning"

# List all available templates
python scripts/query_template.py --list-all

# Get requirements for a venue
python scripts/query_template.py --venue "NeurIPS" --requirements
```

### customize_template.py

使用作者和项目自定义模板信息：

```bash
# Basic customization
python scripts/customize_template.py \
  --template assets/journals/nature_article.tex \
  --output my_paper.tex

# With author information
python scripts/customize_template.py \
  --template assets/journals/nature_article.tex \
  --title "Novel Approach to Protein Folding" \
  --authors "Jane Doe, John Smith, Alice Johnson" \
  --affiliations "MIT, Stanford, Harvard" \
  --email "[email protected]" \
  --output my_paper.tex

# Interactive mode
python scripts/customize_template.py --interactive
```

### validate_format.py

检查文档是否符合场地要求：

```bash
# Validate a compiled PDF
python scripts/validate_format.py \
  --file my_paper.pdf \
  --venue "Nature" \
  --check-all

# Check specific aspects
python scripts/validate_format.py \
  --file my_paper.pdf \
  --venue "NeurIPS" \
  --check page-count,margins,fonts

# Generate validation report
python scripts/validate_format.py \
  --file my_paper.pdf \
  --venue "Science" \
  --report validation_report.txt
```

## 最佳实践

### 模板选择
1. **验证货币**：检查模板日期并与最新的作者指南
2进行比较。 **查看官方来源**：许多期刊都提供官方 LaTeX 课程
3. **测试编译**：添加内容之前编译模板
4. **阅读评论**：模板包括有用的内嵌评论

### 定制
1. **保留结构**：不要删除所需的部分或包
2. **遵循占位符**：系统地替换标记的占位符文本
3. **保持格式**：不要覆盖特定于场地的格式
4. **保留备份**：定制前保存原始模板

### 合规性
1. **检查页面限制**：最终提交前验证
2. **验证引文**：对场地
3 使用正确的引文样式。 **测试图形**：确保图形满足分辨率要求
4. **审查匿名化**：如果需要，请删除识别信息

### 提交
1. **遵循说明**：阅读完整的作者指南
2. **包括所有文件**：LaTeX 源代码、图表、参考书目
3. **正确生成**：使用推荐的编译方式
4. **检查输出**：验证 PDF 是否符合预期

## 常见格式要求

### 页面限制（典型）

|场地类型 |典型限值|注释 |
|------------|----------------|--------|
| **自然文章** | 5 页 |约 3000 字，不包括参考文献 |
| **科学报告** | 5 页 |数字计入限制|
| **公共公共图书馆** |无限制|无限长度|
| **NeurIPS** | 8 页 | + 无限参考/附录 |
| **ICML** | 8 页 | + 无限参考/附录 |
| **NSF 提案** | 15 页 |仅项目描述|
| **NIH R01** | 12 页 |研究策略 |

### 不同地点的引文风格

|地点 |引文风格|格式 |
|-------|----------------|--------|
| **自然** |编号（上标）|自然风格|
| **科学** |编号（上标）|科学风格|
| **公共科学图书馆** |编号（括号）|温哥华|
| **细胞压榨** |作者年份 |单元样式|
| **ACM** |编号| ACM风格|
| **IEEE** |编号（括号）| IEEE风格|
| **APA 期刊** |作者年份 | APA 7th |

### 身材要求

|地点 |分辨率|格式|颜色 |
|-------|-----------|--------|--------|
| **自然** | 300+ dpi | TIFF、EPS、PDF | RGB 或 CMYK |
| **科学** | 300+ dpi | TIFF，PDF | RGB |
| **公共科学图书馆** | 300-600 dpi | TIFF、EPS | RGB |
| **IEEE** | 300+ dpi | EPS，PDF | RGB 或灰度 |

## 写作风格指南

除了格式化之外，此技能还提供了全面的**写作风格指南**，捕捉论文在不同场合应该如何*阅读*，而不仅仅是它们应该如何看起来。

### 为什么风格很重要

为 Nature 撰写的相同研究与为 NeurIPS 撰写的相同研究读起来会有很大不同：
- **自然/科学**：非专业人士也可访问，故事驱动，意义广泛
- **Cell Press**：机制深度、全面数据、所需图形摘要
- **医学期刊**：以患者为中心、证据分级、结构化摘要
- **机器学习会议**：贡献要点、消融研究、再现性焦点
- **CS会议**：特定领域的会议，不同的评估标准

### 可用的风格指南

|指南|封面|关键主题 |
|--------|--------|------------|
| `venue_writing_styles.md` |大师概述|风格谱，快速参考|
| `nature_science_style.md` |自然、科学、美国国家科学院院刊 |无障碍、讲故事、影响广泛 |
| `cell_press_style.md` |细胞、神经元、免疫 |图形摘要、eTOC、亮点 |
| `medical_journal_styles.md` | NEJM、柳叶刀、JAMA、BMJ |结构化摘要，证据语言|
| `ml_conference_style.md` | NeurIPS、ICML、ICLR、CVPR |贡献子弹，消融|
| `cs_conference_style.md` | ACL、EMNLP、CHI、SIGKDD |特定领域约定|
| `reviewer_expectations.md` |所有场馆 |审稿人寻找什么，反驳技巧 |

### 写作示例

具体示例可在 `assets/examples/` 中找到：
- `nature_abstract_examples.md`：高影响力期刊的流畅段落摘要
- `neurips_introduction_example.md`：ML 会议介绍与贡献项目符号
- `cell_summary_example.md`：细胞新闻摘要、亮点、eTOC 格式
- `medical_structured_abstract.md`：NEJM、Lancet、JAMA 结构化格式

### 工作流程：适应场地

1. **确定目标场地**并加载适当的风格指南
2. **复习写作惯例**：语气、声音、摘要格式、结构
3. **检查示例**了解特定部分的指导
4. **评审期望**：该场地的评审者优先考虑什么？
5. **应用格式**：使用`assets/`

- --

## 资源

### 捆绑资源

* *写作风格指南**（在`references/`中）的LaTeX模板：
- `venue_writing_styles.md`：主风格概述和比较
- `nature_science_style.md`：自然/科学写作惯例
- `cell_press_style.md`：Cell Press期刊风格
- `medical_journal_styles.md`：医学期刊写作指南
- `ml_conference_style.md`：ML会议写作惯例
- `cs_conference_style.md`：CS会议写作指南
- `reviewer_expectations.md`：审稿人按场地寻找什么

* *格式要求**（`references/`）：
- `journals_formatting.md`：综合期刊格式要求
- `conferences_formatting.md`：会议论文规范
- `posters_guidelines.md`：研究海报设计和尺寸
- `grants_requirements.md`：资助提案要求Agency

* *写作示例**（`assets/examples/`）：
- `nature_abstract_examples.md`：高影响力期刊摘要示例
- `neurips_introduction_example.md`：ML会议介绍格式
- `cell_summary_example.md`：Cell Press摘要/亮点/eTOC
- `medical_structured_abstract.md`：NEJM/Lancet/JAMA 摘要格式

* *模板**（在 `assets/` 中）：
- `journals/`：期刊文章 LaTeX 模板
- `posters/`：研究海报模板
- `grants/`：拨款提案模板

* *脚本**（在`scripts/`中）：
- `query_template.py`：搜索和检索模板
- `customize_template.py`：使用作者信息进行自定义
- `validate_format.py`：检查是否符合要求

### 外部资源

* *期刊作者指南**：
- 自然：https://www.nature.com/nature/for-authors
- 科学：https://www.science.org/content/page/instructions-authors
- PLOS： https://plos.org/resources/for-authors/
- Cell Press：https://www.cell.com/author-guidelines

* *会议格式**：
- NeurIPS：https://neurips.cc/Conferences/2024/CallForPapers
- ICML： https://icml.cc/Conferences/2024/StyleAuthorInstructions
- CVPR：https://cvpr.thecvf.com/Conferences/2024/AuthorGuidelines

* *拨款资源**：
- NSF PAPPG： https://www.nsf.gov/publications/pub_summ.jsp?ods_key=pappg
- NIH 表格：https://grants.nih.gov/grants/how-to-apply-application-guide.html
- DOE 资助：https://science.osti.gov/grants

## 用法示例

### 示例 1：Nature 文章提交

```markdown
User: "I need to prepare a manuscript for Nature"

Response:
1. Load Nature formatting requirements (references/journals_formatting.md)
2. Retrieve Nature template (assets/journals/nature_article.tex)
3. Key requirements:
   - Length: ~3000 words, ~5 pages
   - Format: Single column, 12pt font
   - Citations: Numbered superscript (Nature style)
   - Figures: 300+ dpi, RGB color
4. Customize template with your title, authors, affiliations
5. Compile and validate against requirements
```

### 示例 2：NeurIPS 会议论文

```markdown
User: "What are the formatting requirements for NeurIPS?"

Response:
From references/conferences_formatting.md:
- Page limit: 8 pages main text + unlimited references/appendix
- Format: Two-column, 10pt font
- Template: neurips_2024.sty (official style file)
- Anonymization: Required for initial submission
- Citations: Numbered (brackets)
- Figures: High resolution, colorblind-safe recommended
```

### 示例 3：NSF 提案

```markdown
User: "Help me format an NSF proposal"

Response:
NSF requirements (from references/grants_requirements.md):
- Project Description: 15 pages maximum
- Project Summary: 1 page (Overview, Intellectual Merit, Broader Impacts)
- Budget Justification: 3-5 pages
- Biographical Sketch: 3 pages per senior personnel
- Font: Minimum 10pt, Times Roman or similar
- Margins: 1 inch all sides
Template: assets/grants/nsf_proposal_template.tex
```

### 示例 4：会议海报

```markdown
User: "I need to create a poster for ISMB"

Response:
ISMB poster specifications:
- Size: Typically A0 portrait (33.1 × 46.8 inches)
- Recommended template: beamerposter or tikzposter
- Font sizes: Title 60-85pt, Headers 36-48pt, Body 24-32pt
- Include: QR code for paper/supplementary materials
Available templates:
- assets/posters/beamerposter_academic.tex
```

## 更新和维护

* *模板货币**：
- 模板每年更新或在场馆发布新指南时更新
- 最后更新： 2024
- 检查官方场地网站了解最新要求

* *报告问题**：
- 模板编译错误
- 过时的格式要求
- 缺少场地模板
- 不正确的规格

## 摘要

The venue-templates 技能提供对：

1 的全面访问。 **50 多个跨学科的出版场所模板**
2. **期刊、会议、海报、赠款的详细格式要求**
3. **用于模板发现、自定义和验证的帮助脚本**
4. **与其他科学写作技能的整合**
5. **成功学术提交的最佳实践**

每当您需要特定场地的格式指导或学术出版模板时，请使用此技能。
