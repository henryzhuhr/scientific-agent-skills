# 编辑演示文稿

## 基于模板的工作流程

当使用现有演示文稿作为模板时：

1. **分析现有幻灯片**：
 ```bash
 python script/thumbnail.py template.pptx
 python -m markitdown template.pptx
 ```
 查看 `thumbnails.jpg` 以查看布局，并查看 markitdown 输出以查看占位符文本.

2. **规划幻灯片映射**：对于每个内容部分，选择一个模板幻灯片。

 ⚠️ **使用各种布局** — 单调的演示是一种常见的失败模式。不要默认使用基本标题+项目符号幻灯片。积极寻找：
 - 多列布局（2列，3列）
  - 图像+文本组合
  - 带文本覆盖的全出血图像
  - 引用或标注幻灯片
  - 部分分隔符
  - 统计/数字callouts
  - 图标网格或图标 + 文本行

  * *避免：** 对每张幻灯片重复相同的文本布局。

 将内容类型与布局样式相匹配（例如，关键点 → 项目符号幻灯片、团队信息 → 多列、感言 → 引用幻灯片）。

3. **拆开包装**：`python scripts/office/unpack.py template.pptx unpacked/`

4. **构建演示文稿**（您自己执行此操作，而不是使用子代理）：
  - 删除不需要的幻灯片（从 `<p:sldIdLst>` 中删除）
  - 您想要重复使用的重复幻灯片 (`add_slide.py`)
  - 在 `<p:sldIdLst>`
 中重新排序幻灯片 - **在步骤之前完成所有结构更改5**

5. **编辑内容**：更新每个 `slide{N}.xml`.
 中的文本 **如果可用，请在此处使用子代理** — 幻灯片是单独的 XML 文件，因此子代理可以并行编辑。

6. **清洁**：`python scripts/clean.py unpacked/`

7. **包**：`python scripts/office/pack.py unpacked/ output.pptx --original template.pptx`

- --

## 脚本

|脚本 |目的|
|--------|---------|
| `unpack.py` |提取并漂亮打印 PPTX |
| `add_slide.py` |复制幻灯片或从布局创建|
| `clean.py` |删除孤立文件 |
| `pack.py` |重新包装并验证|
| `thumbnail.py` |创建幻灯片的可视网格 |

### unpack.py

```bash
python scripts/office/unpack.py input.pptx unpacked/
```

Extracts PPTX，漂亮的打印 XML，转义智能引号。

### add_slide.py

```bash
python scripts/add_slide.py unpacked/ slide2.xml      # Duplicate slide
python scripts/add_slide.py unpacked/ slideLayout2.xml # From layout
```

Prints `<p:sldId>` 添加到 `<p:sldIdLst>` 的所需位置。

### clean.py

```bash
python scripts/clean.py unpacked/
```

 删除不在 `<p:sldIdLst>` 中的幻灯片、未引用的媒体、孤立的关系。

### pack.py

```bash
python scripts/office/pack.py unpacked/ output.pptx --original input.pptx
```

验证、修复、压缩XML、重新编码智能引号。

### 缩略图.py

```bash
python scripts/thumbnail.py input.pptx [output_prefix] [--cols N]
```

创建`thumbnails.jpg`，以幻灯片文件名作为标签。默认 3 列，每个网格最多 12 列。

* *仅用于模板分析**（选择布局）。对于视觉 QA，使用 `soffice` + `pdftoppm` 创建全分辨率的单个幻灯片图像 - 请参阅 SKILL.md.

- --

## 幻灯片操作

幻灯片顺序为 `ppt/presentation.xml` → `<p:sldIdLst>`.

* *重新排序**：重新排列`<p:sldId>`元素。

* *删除**：删除`<p:sldId>`，然后运行`clean.py`。

* *添加**：使用`add_slide.py`。切勿手动复制幻灯片文件 - 该脚本会处理手动复制会错过的注释引用、Content_Types.xml 和关系 ID。

- --

## 编辑内容

* *子代理：** 如果可用，请在此处使用它们（完成步骤 4 后）。每张幻灯片都是一个单独的 XML 文件，因此子代理可以并行编辑。在对子代理的提示中，包括：
- 要编辑的幻灯片文件路径
- **“使用编辑工具进行所有更改”**
- 下面的格式规则和常见陷阱

 对于每张幻灯片：
1. 阅读幻灯片的 XML
2. 识别所有占位符内容 - 文本、图像、图表、图标、标题
3. 将每个占位符替换为最终内容

* *使用编辑工具，而不是 sed 或 Python 脚本。** 编辑工具强制指定要替换的内容和位置，从而产生更好的可靠性。

### 格式规则

- **将所有标题、副标题和内联标签加粗**：在 `<a:rPr>` 上使用 `b="1"`。这包括：
  - 幻灯片标题
  - 幻灯片中的节标题
  - 行开头的内联标签（例如：“状态：”、“描述：”）
- **切勿使用 unicode 项目符号 (•)**：使用 `<a:buChar>` 或 `<a:buChar>` 正确的列表格式`<a:buAutoNum>`
- **项目符号一致性**：让项目符号继承布局。仅指定 `<a:buChar>` 或 `<a:buNone>`。

- --

## 常见陷阱

### 模板适配

当源内容的项数少于模板时：
- **完全删除多余元素**（图像、形状、文本框），不要只是清除text
- 清除文本内容后检查孤立的视觉效果
- 运行视觉 QA 以捕获不匹配的计数

用不同长度内容替换文本时：
- **较短的替换**：通常安全
- **较长的替换**：可能会意外溢出或换行
- 使用视觉进行测试文本更改后的质量检查
- 考虑截断或拆分内容以适应模板的设计约束

* *模板槽≠源项目**：如果模板有4个团队成员但源有3个用户，则删除第4个成员的整个组（图像+文本框），而不仅仅是文本。

### 多项目内容

如果源有多个项目（编号列表，多个部分），为每个元素创建单独的 `<a:p>` 元素 — **切勿连接成一个字符串**。

* *❌ 错误** — 一个段落中的所有项目：
```xml
<a:p>
  <a:r><a:rPr .../><a:t>Step 1: Do the first thing. Step 2: Do the second thing.</a:t></a:r>
</a:p>
```

* *✅ 正确** — 用粗体分隔各个段落headers:
```xml
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" b="1" .../><a:t>Step 1</a:t></a:r>
</a:p>
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" .../><a:t>Do the first thing.</a:t></a:r>
</a:p>
<a:p>
  <a:pPr algn="l"><a:lnSpc><a:spcPts val="3919"/></a:lnSpc></a:pPr>
  <a:r><a:rPr lang="en-US" sz="2799" b="1" .../><a:t>Step 2</a:t></a:r>
</a:p>
<!-- continue pattern -->
```

 从原始段落复制 `<a:pPr>` 以保留行距。在标题上使用 `b="1"`。

### 智能引号

由解包/打包自动处理。但编辑工具会将智能引号转换为 ASCII。

* *添加带引号的新文本时，请使用 XML 实体：**

```xml
<a:t>the &#x201C;Agreement&#x201D;</a:t>
```

|人物 |名称 |统一码 | XML 实体 |
|---------|------|---------|------------|
| `“` |左双引号 | U+201C | `&#x201C;` |
| `”` |右双引号 | U+201D | `&#x201D;` |
| `‘` |左单引号 | U+2018 | `&#x2018;` |
| `’` |右单引号 | U+2019 | `&#x2019;` |

### 其他

- **空白**：在 `<a:t>` 上使用 `xml:space="preserve"`，并带有前导/尾随空格
- **XML 解析**：使用 `defusedxml.minidom`，而不是 `xml.etree.ElementTree`（损坏）命名空间）
