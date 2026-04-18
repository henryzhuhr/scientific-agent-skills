---
name: docx
description: "每当用户想要创建、阅读、编辑或操作 Word 文档（.docx 文件）时，请使用此技能。触发因素包括：任何提及“Word doc”、“word 文档”、“.docx”的行为，或要求生成具有目录、标题、页码或信头等格式的专业文档。还可以在从 .docx 文件中提取或重新组织内容、在文档中插入或替换图像、在 Word 文件中执行查找和替换、处理跟踪的更改或注释或将内容转换为精美的 Word 文档时使用。如果用户要求“报告”、“备忘录”、“信件”、“模板”或类似的 Word 或 .docx 文件形式的可交付成果，请使用此技能。请勿用于 PDF、电子表格、Google 文档或与文档生成无关的一般编码任务。"
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX 创建、编辑和分析

## 概述

A .docx 文件是包含 XML 文件的 ZIP 存档。

## 快速参考

|任务|接近|
|------|----------|
|阅读/分析内容 | `pandoc` 或解压原始 XML |
|创建新文档 |使用 `docx-js` - 请参阅下面的创建新文档 |
|编辑现有文档 |解包 → 编辑 XML → 重新打包 - 请参阅下面的编辑现有文档 |

### 将 .doc 转换为 .docx

旧版 `.doc` 文件在编辑之前必须进行转换：

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

### 阅读内容

```bash
# Text extraction with tracked changes
pandoc --track-changes=all document.docx -o output.md

# Raw XML access
python scripts/office/unpack.py document.docx unpacked/
```

### 转换为图像

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### 接受跟踪更改

要生成接受所有跟踪更改的干净文档（需要LibreOffice):

```bash
python scripts/accept_changes.py input.docx output.docx
```

- --

## 创建新文档

使用 JavaScript 生成 .docx 文件，然后验证。安装：`npm install -g docx`

### 安装
```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        InternalHyperlink, Bookmark, FootnoteReferenceRun, PositionalTab,
        PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader,
        TabStopType, TabStopPosition, Column, SectionType,
        TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageNumber, PageBreak } = require('docx');

const doc = new Document({ sections: [{ children: [/* content */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### 验证
创建文件后，验证它。如果验证失败，请解压、修复 XML，然后重新打包。
```bash
python scripts/office/validate.py doc.docx
```

### 页面大小

```javascript
// CRITICAL: docx-js defaults to A4, not US Letter
// Always set page size explicitly for consistent results
sections: [{
  properties: {
    page: {
      size: {
        width: 12240,   // 8.5 inches in DXA
        height: 15840   // 11 inches in DXA
      },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 inch margins
    }
  },
  children: [/* content */]
}]
```

* *常见页面大小（DXA 单位，1440 DXA = 1 英寸）：**

|纸|宽度|身高|内容宽度（1 英寸边距） |
|-------|-------|--------|---------------------------|
| US Letter | 12,240 | 15,840 | 9,360 |
| A4（默认）| 11,906 | 16,838 | 9,026 |

* *横向：** docx-js 在内部交换宽度/高度，因此传递纵向尺寸并让它处理交换：
```javascript
size: {
  width: 12240,   // Pass SHORT edge as width
  height: 15840,  // Pass LONG edge as height
  orientation: PageOrientation.LANDSCAPE  // docx-js swaps them in the XML
},
// Content width = 15840 - left margin - right margin (uses the long edge)
```

### 样式（覆盖内置标题）

使用 Arial 作为默认字体（普遍支持）。 zXQNL38QXZ```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 12pt default
    paragraphStyles: [
      // IMPORTANT: Use exact IDs to override built-in styles
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // outlineLevel required for TOC
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Title")] }),
    ]
  }]
});
```

### 列表（切勿使用 unicode 项目符号）

```javascript
// ❌ WRONG - never manually insert bullet characters
new Paragraph({ children: [new TextRun("• Item")] })  // BAD
new Paragraph({ children: [new TextRun("\u2022 Item")] })  // BAD

// ✅ CORRECT - use numbering config with LevelFormat.BULLET
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Bullet item")] }),
      new Paragraph({ numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Numbered item")] }),
    ]
  }]
});

// ⚠️ Each reference creates INDEPENDENT numbering
// Same reference = continues (1,2,3 then 4,5,6)
// Different reference = restarts (1,2,3 then 1,2,3)
```

### 表

**关键：表需要双宽度** - 在表上同时设置 `columnWidths` 和每个单元格上都有 `width`。如果没有两者，表格在某些平台上渲染不正确。

```javascript
// CRITICAL: Always set table width for consistent rendering
// CRITICAL: Use ShadingType.CLEAR (not SOLID) to prevent black backgrounds
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9360, type: WidthType.DXA }, // Always use DXA (percentages break in Google Docs)
  columnWidths: [4680, 4680], // Must sum to table width (DXA: 1440 = 1 inch)
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 4680, type: WidthType.DXA }, // Also set on each cell
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, // CLEAR not SOLID
          margins: { top: 80, bottom: 80, left: 120, right: 120 }, // Cell padding (internal, not added to width)
          children: [new Paragraph({ children: [new TextRun("Cell")] })]
        })
      ]
    })
  ]
})
```

**表格宽度计算：**

始终使用 `WidthType.DXA` — `WidthType.PERCENTAGE` 在 Google Docs 中中断。

```javascript
// Table width = sum of columnWidths = content width
// US Letter with 1" margins: 12240 - 2880 = 9360 DXA
width: { size: 9360, type: WidthType.DXA },
columnWidths: [7000, 2360]  // Must sum to table width
```

**宽度规则：**
- **始终使用 `WidthType.DXA`** — 从不 `WidthType.PERCENTAGE`（与 Google Docs 不兼容）
- 表宽度必须等于总和`columnWidths`
- 单元格 `width` 必须匹配相应的 `columnWidth`
- 单元格 `margins` 是内部填充 - 它们减少内容区域，而不是添加到单元格宽度
- 对于全角表格：使用内容宽度（页面宽度减去左右边距）

###图片

```javascript
// CRITICAL: type parameter is REQUIRED
new Paragraph({
  children: [new ImageRun({
    type: "png", // Required: png, jpg, jpeg, gif, bmp, svg
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 },
    altText: { title: "Title", description: "Desc", name: "Name" } // All three required
  })]
})
```

### 分页符

```javascript
// CRITICAL: PageBreak must be inside a Paragraph
new Paragraph({ children: [new PageBreak()] })

// Or use pageBreakBefore
new Paragraph({ pageBreakBefore: true, children: [new TextRun("New page")] })
```

### 超链接

```javascript
// External link
new Paragraph({
  children: [new ExternalHyperlink({
    children: [new TextRun({ text: "Click here", style: "Hyperlink" })],
    link: "https://example.com",
  })]
})

// Internal link (bookmark + reference)
// 1. Create bookmark at destination
new Paragraph({ heading: HeadingLevel.HEADING_1, children: [
  new Bookmark({ id: "chapter1", children: [new TextRun("Chapter 1")] }),
]})
// 2. Link to it
new Paragraph({ children: [new InternalHyperlink({
  children: [new TextRun({ text: "See Chapter 1", style: "Hyperlink" })],
  anchor: "chapter1",
})]})
```

###脚注

```javascript
const doc = new Document({
  footnotes: {
    1: { children: [new Paragraph("Source: Annual Report 2024")] },
    2: { children: [new Paragraph("See appendix for methodology")] },
  },
  sections: [{
    children: [new Paragraph({
      children: [
        new TextRun("Revenue grew 15%"),
        new FootnoteReferenceRun(1),
        new TextRun(" using adjusted metrics"),
        new FootnoteReferenceRun(2),
      ],
    })]
  }]
});
```

### 制表位

```javascript
// Right-align text on same line (e.g., date opposite a title)
new Paragraph({
  children: [
    new TextRun("Company Name"),
    new TextRun("\tJanuary 2025"),
  ],
  tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
})

// Dot leader (e.g., TOC-style)
new Paragraph({
  children: [
    new TextRun("Introduction"),
    new TextRun({ children: [
      new PositionalTab({
        alignment: PositionalTabAlignment.RIGHT,
        relativeTo: PositionalTabRelativeTo.MARGIN,
        leader: PositionalTabLeader.DOT,
      }),
      "3",
    ]}),
  ],
})
```

### 多列布局

```javascript
// Equal-width columns
sections: [{
  properties: {
    column: {
      count: 2,          // number of columns
      space: 720,        // gap between columns in DXA (720 = 0.5 inch)
      equalWidth: true,
      separate: true,    // vertical line between columns
    },
  },
  children: [/* content flows naturally across columns */]
}]

// Custom-width columns (equalWidth must be false)
sections: [{
  properties: {
    column: {
      equalWidth: false,
      children: [
        new Column({ width: 5400, space: 720 }),
        new Column({ width: 3240 }),
      ],
    },
  },
  children: [/* content */]
}]
```

 使用以下命令强制在新节中进行分栏`type: SectionType.NEXT_COLUMN`.

### 目录

```javascript
// CRITICAL: Headings must use HeadingLevel ONLY - no custom styles
new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" })
```

### 页眉/页脚

```javascript
sections: [{
  properties: {
    page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } // 1440 = 1 inch
  },
  headers: {
    default: new Header({ children: [new Paragraph({ children: [new TextRun("Header")] })] })
  },
  footers: {
    default: new Footer({ children: [new Paragraph({
      children: [new TextRun("Page "), new TextRun({ children: [PageNumber.CURRENT] })]
    })] })
  },
  children: [/* content */]
}]
```

### docx-js 的关键规则

- **明确设置页面大小** - docx-js 默认为 A4；对美国文档使用 US Letter (12240 x 15840 DXA)
- **横向：传递纵向尺寸** - docx-js 在内部交换宽度/高度；将短边传递为 `width`，将长边传递为 `height`，并设置 `orientation: PageOrientation.LANDSCAPE`
- **切勿使用 `\n`** - 使用单独的段落元素
- **切勿使用 unicode 项目符号** - 使用带有编号配置的 `LevelFormat.BULLET`
- **PageBreak 必须位于段落中** - 独立创建无效的 XML
- **ImageRun 需要 `type`** - 始终指定 png/jpg/etc
- **始终使用 DXA 设置表 `width`** - 切勿使用 `WidthType.PERCENTAGE`（Google 文档中的中断）
- **表格需要双宽度** - `columnWidths` 数组和单元格 `width`，两者都必须匹配
- **表宽度 = 列宽度总和** - 对于 DXA，确保它们精确相加
- **始终添加单元格边距** - 使用 `margins: { top: 80, bottom: 80, left: 120, right: 120 }` 进行可读填充
- **使用 `ShadingType.CLEAR`** - 从不实体对于表格着色
- **切勿使用表格作为分隔符/规则** - 单元格具有最小高度并呈现为空框（包括在页眉/页脚中）；在段落上使用 `border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } }` 代替。对于两列页脚，使用制表位（请参阅制表位部分），而不是表格
- **TOC 仅需要 HeadingLevel** - 标题段落上没有自定义样式
- **覆盖内置样式** - 使用确切的 ID：“标题 1”、“标题 2”等。
- **包括 `outlineLevel`** - 需要TOC（0 表示 H1，1 表示 H2 等）

---

## 编辑现有文档

**按顺序执行所有 3 个步骤。**

### 步骤 1：解包
```bash
python scripts/office/unpack.py document.docx unpacked/
```
 提取 XML、漂亮打印、合并相邻运行，并将智能引号转换为 XML 实体（`&#x201C;` 等），以便它们在编辑后仍然存在。使用 `--merge-runs false` 跳过运行合并。

### 步骤 2：编辑 XML

在`unpacked/word/`中编辑文件。请参阅下面的 XML 参考以了解模式。

**使用“Claude”作为作者**来跟踪更改和注释，除非用户明确请求使用不同的名称。

**直接使用编辑工具进行字符串替换。不要编写 Python 脚本。** 脚本会带来不必要的复杂性。编辑工具准确显示正在替换的内容。

**关键：对新内容使用智能引号。**添加带撇号或引号的文本时，使用 XML 实体生成智能引号：
```xml
<!-- Use these entities for professional typography -->
<w:t>Here&#x2019;s a quote: &#x201C;Hello&#x201D;</w:t>
```
|实体|字符 |
|--------|-----------|
| `&#x2018;` | ‘（左单）|
| `&#x2019;` | ’（右单/撇号）|
| `&#x201C;` | “ (左双) |
| `&#x201D;` | ” (右双) |

**添加注释：** 使用 `comment.py` 处理跨多个 XML 文件的样板（文本必须预先转义 XML）：
```bash
python scripts/comment.py unpacked/ 0 "Comment text with &amp; and &#x2019;"
python scripts/comment.py unpacked/ 1 "Reply text" --parent 0  # reply to comment 0
python scripts/comment.py unpacked/ 0 "Text" --author "Custom Author"  # custom author name
```
 然后向 document.xml 添加标记（请参阅 XML 中的注释）参考).

### 步骤 3：打包
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```
 使用自动修复进行验证，压缩 XML，并创建 DOCX。使用 `--validate false` 跳过。

**自动修复将修复：**
- `durableId` >= 0x7FFFFFFF（重新生成有效 ID）
- `<w:t>` 上缺少 `xml:space="preserve"`空白

**自动修复无法修复：**
- 格式错误的 XML、无效元素嵌套、缺少关系、模式冲突

### 常见陷阱

- **替换整个 `<w:r>` 元素**：添加跟踪更改时，将整个 `<w:r>...</w:r>` 块替换为`<w:del>...<w:ins>...` 作为兄弟姐妹。不要在运行中注入跟踪更改标签。
- **保留 `<w:rPr>` 格式**：将原始运行的 `<w:rPr>` 块复制到跟踪更改运行中，以保持粗体、字体大小等。

---

## XML 参考

### 架构合规性

- **`<w:pPr>` 中的元素顺序**：`<w:pStyle>`、`<w:numPr>`、`<w:spacing>`、`<w:ind>`、`<w:jc>`、`<w:rPr>` 最后
- **空白**：将 `xml:space="preserve"` 添加到`<w:t>` 带有前导/尾随空格
- **RSID**：必须是 8 位十六进制（例如，`00AB1234`）

### 已跟踪更改

**插入：**
```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>
```

**删除：**
```xml
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
```

**在`<w:del>`**内：使用`<w:delText>`而不是`<w:t>`，并且`<w:delInstrText>` 而不是 `<w:instrText>`.

 **最少编辑** - 仅标记更改内容：
```xml
<!-- Change "30 days" to "60 days" -->
<w:r><w:t>The term is </w:t></w:r>
<w:del w:id="1" w:author="Claude" w:date="...">
  <w:r><w:delText>30</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="Claude" w:date="...">
  <w:r><w:t>60</w:t></w:r>
</w:ins>
<w:r><w:t> days.</w:t></w:r>
```

 **删除整个段落/列表项** - 从段落中删除所有内容时，还将段落标记标记为已删除，以便与下一个段落合并。在 `<w:pPr><w:rPr>` 中添加 `<w:del/>`：
```xml
<w:p>
  <w:pPr>
    <w:numPr>...</w:numPr>  <!-- list numbering if present -->
    <w:rPr>
      <w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z"/>
    </w:rPr>
  </w:pPr>
  <w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
    <w:r><w:delText>Entire paragraph content being deleted...</w:delText></w:r>
  </w:del>
</w:p>
```
 如果没有 `<w:pPr><w:rPr>` 中的 `<w:del/>`，接受更改会留下一个空段落/列表项。

**拒绝其他作者的插入** - 在其内部嵌套删除插入：
```xml
<w:ins w:author="Jane" w:id="5">
  <w:del w:author="Claude" w:id="10">
    <w:r><w:delText>their inserted text</w:delText></w:r>
  </w:del>
</w:ins>
```

**恢复其他作者的删除** - 在之后添加插入（不要修改他们的删除）：
```xml
<w:del w:author="Jane" w:id="5">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
<w:ins w:author="Claude" w:id="10">
  <w:r><w:t>deleted text</w:t></w:r>
</w:ins>
```

### Comments

运行`comment.py`后（参见步骤2），将标记添加到文档.xml。对于回复，请在父级内部使用 `--parent` 标志和嵌套标记。

**关键：`<w:commentRangeStart>` 和 `<w:commentRangeEnd>` 是 `<w:r>` 的兄弟姐妹，从不在内部`<w:r>`.**

```xml
<!-- Comment markers are direct children of w:p, never inside w:r -->
<w:commentRangeStart w:id="0"/>
<w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted</w:delText></w:r>
</w:del>
<w:r><w:t> more text</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>

<!-- Comment 0 with reply 1 nested inside -->
<w:commentRangeStart w:id="0"/>
  <w:commentRangeStart w:id="1"/>
  <w:r><w:t>text</w:t></w:r>
  <w:commentRangeEnd w:id="1"/>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="1"/></w:r>
```

### 图片

1。将图像文件添加到`word/media/`
2。添加与 `word/_rels/document.xml.rels`:
```xml
<Relationship Id="rId5" Type=".../image" Target="media/image1.png"/>
```
3 的关系。将内容类型添加到 `[Content_Types].xml`:
```xml
<Default Extension="png" ContentType="image/png"/>
```
4。 document.xml 中参考：
```xml
<w:drawing>
  <wp:inline>
    <wp:extent cx="914400" cy="914400"/>  <!-- EMUs: 914400 = 1 inch -->
    <a:graphic>
      <a:graphicData uri=".../picture">
        <pic:pic>
          <pic:blipFill><a:blip r:embed="rId5"/></pic:blipFill>
        </pic:pic>
      </a:graphicData>
    </a:graphic>
  </wp:inline>
</w:drawing>
```

- --

## 依赖项

- **pandoc**：文本提取
- **docx**：`npm install -g docx`（新文档）
- **LibreOffice**： PDF 转换（通过 `scripts/office/soffice.py` 自动配置沙盒环境）
- **Poppler**：用于图像的 `pdftoppm`
