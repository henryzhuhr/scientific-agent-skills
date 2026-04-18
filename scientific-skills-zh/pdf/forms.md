* *重要：您必须按顺序完成这些步骤。不要跳到编写代码。**

如果您需要填写 PDF 表单，请首先检查 PDF 是否具有可填写的表单字段。从此文件的目录运行此脚本：
 `python scripts/check_fillable_fields <file.pdf>`，并根据结果转到“可填写字段”或“不可填写字段”并按照这些说明进行操作。

# 可填写字段
如果 PDF 具有可填写表单字段：
- 从此文件目录运行此脚本： `python scripts/extract_form_field_info.py <input.pdf> <field_info.json>`。它将创建一个包含以下格式字段列表的 JSON 文件：
```
[
  {
    "field_id": (unique ID for the field),
    "page": (page number, 1-based),
    "rect": ([left, bottom, right, top] bounding box in PDF coordinates, y=0 is the bottom of the page),
    "type": ("text", "checkbox", "radio_group", or "choice"),
  },
  // Checkboxes have "checked_value" and "unchecked_value" properties:
  {
    "field_id": (unique ID for the field),
    "page": (page number, 1-based),
    "type": "checkbox",
    "checked_value": (Set the field to this value to check the checkbox),
    "unchecked_value": (Set the field to this value to uncheck the checkbox),
  },
  // Radio groups have a "radio_options" list with the possible choices.
  {
    "field_id": (unique ID for the field),
    "page": (page number, 1-based),
    "type": "radio_group",
    "radio_options": [
      {
        "value": (set the field to this value to select this radio option),
        "rect": (bounding box for the radio button for this option)
      },
      // Other radio options
    ]
  },
  // Multiple choice fields have a "choice_options" list with the possible choices:
  {
    "field_id": (unique ID for the field),
    "page": (page number, 1-based),
    "type": "choice",
    "choice_options": [
      {
        "value": (set the field to this value to select this option),
        "text": (display text of the option)
      },
      // Other choice options
    ],
  }
]
```
- 使用此脚本（从该文件的目录运行）将 PDF 转换为 PNG（每页一个图像）：
`python scripts/convert_pdf_to_images.py <file.pdf> <output_directory>`
然后分析图像以确定每个表单字段的用途（确保转换边界框） PDF 坐标到图像坐标）。
 - 使用要为每个字段输入的值创建此格式的 `field_values.json` 文件：
```
[
  {
    "field_id": "last_name", // Must match the field_id from `extract_form_field_info.py`
    "description": "The user's last name",
    "page": 1, // Must match the "page" value in field_info.json
    "value": "Simpson"
  },
  {
    "field_id": "Checkbox12",
    "description": "Checkbox to be checked if the user is 18 or over",
    "page": 1,
    "value": "/On" // If this is a checkbox, use its "checked_value" value to check it. If it's a radio button group, use one of the "value" values in "radio_options".
  },
  // more fields
]
```
 - 从此文件的目录运行 `fill_fillable_fields.py` 脚本以创建填充的PDF:
`python scripts/fill_fillable_fields.py <input pdf> <field_values.json> <output pdf>`
此脚本将验证您提供的字段 ID 和值是否有效；如果它打印错误消息，请更正相应的字段，然后重试。

# 不可填写的字段
如果 PDF 没有可填写的表单字段，您将添加文本注释。首先尝试从 PDF 结构中提取坐标（更准确），然后根据需要退回到视觉估计。

## 步骤 1：首先尝试结构提取

运行此脚本以提取文本标签、线条和复选框及其精确的 PDF 坐标：
`python scripts/extract_form_structure.py <input.pdf> form_structure.json`

这将创建一个 JSON 文件，其中包含：
- **标签**：具有精确坐标的每个文本元素（PDF 点中的 x0、顶部、x1、底部）
- **行**：定义行边界的水平线
- **复选框**：作为复选框的小矩形（带有中心坐标）
- **row_boundaries**：行从水平线计算的顶部/底部位置

* *检查结果**：如果`form_structure.json`具有有意义的标签（对应于表单字段的文本元素），请使用**方法A：基于结构的坐标**。如果 PDF 是扫描/基于图像且标签很少或没有标签，请使用 **方法 B：视觉估计**。

- --

## 方法 A：基于结构的坐标（首选）

当 `extract_form_structure.py` 在 PDF 中找到文本标签时使用此方法。

### A.1：分析结构

读取form_struct.json并识别：

1. **标签组**：形成单个标签的相邻文本元素（例如“姓氏”+“姓名”）
2. **行结构**：具有相似`top`值的标签位于同一行
3中。 **字段列**：输入区域在标签结束后开始（x0 = label.x1 + 间隙）
4. **复选框**：直接使用结构中的复选框坐标

* *坐标系**：PDF 坐标，其中 y=0 位于页面顶部，y 向下增加。

### A.2：检查缺失元素

结构提取可能无法检测所有表单元素。常见情况：
- **圆形复选框**：仅将方形矩形检测为复选框
- **复杂图形**：装饰元素或非标准表单控件
- **褪色或浅色元素**：可能无法提取

如果您在PDF图像中看到表单字段，而PDF图像中没有form_struct.json，您需要对这些特定字段使用**可视化分析**（请参阅下面的“混合方法”）。

### A.3：使用 PDF 坐标创建 fields.json

对于每个字段，从提取的结构中计算条目坐标：

* *文本字段：**
- 条目x0 =标签x1 + 5（标签后的小间隙）
- 条目x1 =下一个标签的x0，或行边界
- 条目顶部=与标签顶部相同
- 条目底部=下面的行边界线，或标签底部+ row_height

* *复选框：**
- 直接从 form_struct.json 使用复选框矩形坐标
- entry_bounding_box = [checkbox.x0, checkbox.top, checkbox.x1, checkbox.bottom]

 使用 `pdf_width` 和 `pdf_height` 创建 fields.json （信号PDF 坐标）：
```json
{
  "pages": [
    {"page_number": 1, "pdf_width": 612, "pdf_height": 792}
  ],
  "form_fields": [
    {
      "page_number": 1,
      "description": "Last name entry field",
      "field_label": "Last Name",
      "label_bounding_box": [43, 63, 87, 73],
      "entry_bounding_box": [92, 63, 260, 79],
      "entry_text": {"text": "Smith", "font_size": 10}
    },
    {
      "page_number": 1,
      "description": "US Citizen Yes checkbox",
      "field_label": "Yes",
      "label_bounding_box": [260, 200, 280, 210],
      "entry_bounding_box": [285, 197, 292, 205],
      "entry_text": {"text": "X"}
    }
  ]
}
```

* *重要**：使用 `pdf_width`/`pdf_height` 和直接来自 form_struct.json.

### A.4：验证边界框

在填充之前，检查边界框错误：
`python scripts/check_bounding_boxes.py fields.json`

这会检查对于字体大小来说太小的相交边界框和输入框。在填充之前修复任何报告的错误。

- --

## 方法B：视觉估计（后备）

当扫描PDF/基于图像并且结构提取发现没有可用的文本标签时使用此方法（例如，所有文本显示为“（cid：X）”模式）。

#### B.1：转换PDF 到图像

`python scripts/convert_pdf_to_images.py <input.pdf> <images_dir/>`

### B.2：初始字段识别

检查每个页面图像以识别表单部分并获得字段位置的**粗略估计**：
- 表单字段标签及其大致位置
- 输入区域（文本的行、框或空白区域）输入）
- 复选框及其大致位置

对于每个字段，记下近似像素坐标（它们不需要精确）。

### B.3：缩放细化（对于准确性至关重要）

对于每个字段，在估计位置周围裁剪一个区域以精确细化坐标。

* *使用 ImageMagick 创建缩放裁剪：**
```bash
magick <page_image> -crop <width>x<height>+<x>+<y> +repage <crop_output.png>
```

其中：
- `<x>, <y>` = 裁剪区域的左上角（使用粗略估计减去填充）
- `<width>, <height>` = 裁剪区域的大小（字段区域加上每个区域上约 50 像素的填充） side)

* *示例：**要细化估计在 (100, 150)左右的“名称”字段：
```bash
magick images_dir/page_1.png -crop 300x80+50+120 +repage crops/name_field.png
```

（注意：如果 `magick` 命令不可用，请尝试使用相同参数的 `convert`）。

* *检查裁剪后的图像**以确定精确值坐标：
1. 识别输入区域开始的确切像素（在标签之后）
2. 确定输入区域结束的位置（下一个字段或边缘之前）
3. 识别输入线/框的顶部和底部

* *将裁剪坐标转换回完整图像坐标：**
- full_x =crop_x +crop_offset_x
- full_y =crop_y +crop_offset_y

示例：如果裁剪从 (50, 120)开始，输入框从 (52, 18）作物内：
- entry_x0 = 52 + 50 = 102
- entry_top = 18 + 120 = 138

* *对每个田地重复**，尽可能将附近的田地分组为单一作物。

### B.4：使用Refined创建fields.json坐标

使用`image_width`和`image_height`（信号图像坐标）创建fields.json：
```json
{
  "pages": [
    {"page_number": 1, "image_width": 1700, "image_height": 2200}
  ],
  "form_fields": [
    {
      "page_number": 1,
      "description": "Last name entry field",
      "field_label": "Last Name",
      "label_bounding_box": [120, 175, 242, 198],
      "entry_bounding_box": [255, 175, 720, 218],
      "entry_text": {"text": "Smith", "font_size": 10}
    }
  ]
}
```

* *重要**：使用`image_width`/`image_height`和缩放的细化像素坐标Analysis.

### B.5：验证边界框

在填充之前，检查边界框是否有错误：
`python scripts/check_bounding_boxes.py fields.json`

这将检查相交的边界框和对于字体大小来说太小的输入框。在填充之前修复任何报告的错误。

- --

## 混合方法：结构+视觉

当结构提取适用于大多数字段但错过一些元素（例如，圆形复选框，不常见的表单控件）时使用此方法。

1. **对 form_struct.json
2 中检测到的字段使用方法 A**。 **将 PDF 转换为图像**，以对缺失字段 
3 进行可视化分析。 **对缺失字段使用缩放细化**（来自方法 B）
4. **组合坐标**：对于结构提取的字段，使用 `pdf_width`/`pdf_height`。对于视觉估计字段，您必须将图像坐标转换为 PDF 坐标：
  - pdf_x = image_x * (pdf_width / image_width)
  - pdf_y = image_y * (pdf_height / image_height)
5. **在 fields.json 中使用单一坐标系** - 使用 `pdf_width`/`pdf_height`

- --

## 将所有坐标转换为 PDF 坐标 ** 步骤 2：填充前验证 

* * 始终先验证边界框填充：**
`python scripts/check_bounding_boxes.py fields.json`

这会检查：
- 相交的边界框（这会导致文本重叠）
- 对于指定字体大小来说太小的输入框

在继续之前修复fields.json中报告的任何错误。

## 步骤3：填写表单

填充脚本自动检测坐标系并处理转换：
`python scripts/fill_pdf_form_with_annotations.py <input.pdf> fields.json <output.pdf>`

## 步骤4：验证输出

将填充的PDF转换为图像并验证文本位置：
`python scripts/convert_pdf_to_images.py <output.pdf> <verify_images/>`

If文本位置错误：
- **方法 A**：检查您是否正在将 form_struct.json 中的 PDF 坐标与 `pdf_width`/`pdf_height`
- **方法 B**：检查图像尺寸是否匹配且坐标是准确的像素
- **混合**：确保坐标转换正确目视估计视场
