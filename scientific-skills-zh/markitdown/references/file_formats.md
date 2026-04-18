# 文件格式支持

本文档提供了MarkItDown支持的每种文件格式的详细信息。

## 文档格式

### PDF (.pdf)

* *功能**：
- 文本提取
- 表检测
- 元数据提取
- 扫描文档的OCR（具有依赖项）

* *依赖项**：
```bash
pip install 'markitdown[pdf]'
```

* *最适合**：
- 科学论文
- 报告
- 书籍
- 表单

* *限制**：
- 复杂的布局可能无法保留完美的格式
- 扫描的PDF 需要OCR 设置
- 某些PDF 功能（注释、表单）可能无法保留转换

* *示例**：
```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("research_paper.pdf")
print(result.text_content)
```

* *使用Azure文档智能增强**：
```python
md = MarkItDown(docintel_endpoint="https://YOUR-ENDPOINT.cognitiveservices.azure.com/")
result = md.convert("complex_layout.pdf")
```

- --

### Microsoft Word (.docx)

* *功能**：
- 文本提取
- 表格转换
- 标题层次结构
- 列表格式
- 基本文本格式（粗体、斜体）

* *依赖项**：
```bash
pip install 'markitdown[docx]'
```

* *最适合**：
- 研究论文
- 报告
- 文档
- 手稿

* *保留元素**：
- 标题（转换为 Markdown 标题）
- 表格（转换为 Markdown 表格）
- 列表（项目符号和编号）
- 基本格式（粗体、斜体）
- 段落

* *示例**：
```python
result = md.convert("manuscript.docx")
```

- --

### PowerPoint (.pptx)

* *功能**：
- 幻灯片内容提取
- 扬声器注释
- 表提取
- 图像描述（带AI）

* *依赖项**：
```bash
pip install 'markitdown[pptx]'
```

* *最适合**：
- 演示
- 讲座幻灯片
- 会议演讲

* *输出格式**:
```markdown
# Slide 1: Title

Content from slide 1...

**Notes**: Speaker notes appear here

---

# Slide 2: Next Topic

...
```

* *带有AI图像描述**:
```python
from openai import OpenAI

client = OpenAI()
md = MarkItDown(llm_client=client, llm_model="gpt-4o")
result = md.convert("presentation.pptx")
```

- --

### Excel (.xlsx, .xls)

* *功能**：
- 工作表提取
- 表格格式化
- 数据保存
- 公式值（计算）

* *依赖项**：
```bash
pip install 'markitdown[xlsx]'  # Modern Excel
pip install 'markitdown[xls]'   # Legacy Excel
```

* *最佳对于**：
- 数据表
- 研究数据
- 统计结果
- 实验数据

* *输出格式**：
```markdown
# Sheet: Results

| Sample | Control | Treatment | P-value |
|--------|---------|-----------|---------|
| 1      | 10.2    | 12.5      | 0.023   |
| 2      | 9.8     | 11.9      | 0.031   |
```

 * *示例**：
```python
result = md.convert("experimental_data.xlsx")
```

- --

## 图像格式

### 图像（.jpg，.jpeg，.png，.gif， .webp)

* *功能**：
- EXIF 元数据提取
- OCR 文本提取
- AI 驱动的图像描述

* *依赖项**：
```bash
pip install 'markitdown[all]'  # Includes image support
```

* *最适合**：
- 扫描文档
- 图表和图表
- 科学图表
- 带文本的照片

* *无AI输出**：
```markdown
![Image](image.jpg)

**EXIF Data**:
- Camera: Canon EOS 5D
- Date: 2024-01-15
- Resolution: 4000x3000
```

* *带AI输出**：
```python
from openai import OpenAI

client = OpenAI()
md = MarkItDown(
    llm_client=client,
    llm_model="gpt-4o",
    llm_prompt="Describe this scientific diagram in detail"
)
result = md.convert("graph.png")
```

* *文本OCR提取**：
需要Tesseract OCR：
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt-get install tesseract-ocr
```

- --

## 音频格式

### 音频（.wav，.mp3）

* *功能**：
- 元数据提取
- 语音到文本转录
- 持续时间和技术信息

* *依赖项**：
```bash
pip install 'markitdown[audio-transcription]'
```

* *最适合**：
- 讲座录音
- 访谈
- 播客
- 会议录音

* *输出格式**:
```markdown
# Audio: interview.mp3

**Metadata**:
- Duration: 45:32
- Bitrate: 320kbps
- Sample Rate: 44100Hz

**Transcription**:
[Transcribed text appears here...]
```

* *示例**:
```python
result = md.convert("lecture.mp3")
```

- --

## Web格式

### HTML (.html, .htm)

* *功能**：
- 干净的 HTML 到 Markdown 转换
- 链接保留
- 表格转换
- 列表格式

* *最适合**：
- Web页面
- 文档
- 博客文章
- 在线文章

* *输出格式**：保留链接和结构的干净Markdown

* *示例**：
```python
result = md.convert("webpage.html")
```

- --

### YouTube URL

* *功能**：
- 获取视频转录
- 提取视频元数据
- 字幕下载

* *依赖项**：
```bash
pip install 'markitdown[youtube-transcription]'
```

* *最适合**：
- 教育视频
- 讲座
- 讲座
- 教程

* *示例**:
```python
result = md.convert("https://www.youtube.com/watch?v=VIDEO_ID")
```

- --

## 数据格式

### CSV (.csv)

* *功能**：
- 自动表格转换
- 分隔符检测
- 标头保留

* *输出格式**：Markdown表

* *示例**：
```python
result = md.convert("data.csv")
```

* *输出**：
```markdown
| Column1 | Column2 | Column3 |
|---------|---------|---------|
| Value1  | Value2  | Value3  |
```

- --

### JSON (.json)

* *功能**：
- 结构化表示
- 漂亮的格式
- 嵌套数据可视化

* *最适合**：
- API 响应
- 配置文件
- 数据Exports

* *示例**:
```python
result = md.convert("data.json")
```

- --

### XML (.xml)

* *功能**:
- 结构保存
- 属性提取
- 格式化输出

* *最适合**：
- 配置文件
- 数据交换
- 结构化文档

* *示例**：
```python
result = md.convert("config.xml")
```

- --

## 存档格式

### ZIP (.zip)

* *功能**：
- 迭代存档内容
- 单独转换每个文件
- 维护输出中的目录结构

* *最适合**：
- 文档集合
- 项目存档
- 批处理转换

* *输出格式**:
```markdown
# Archive: documents.zip

## File: document1.pdf
[Content from document1.pdf...]

---

## File: document2.docx
[Content from document2.docx...]
```

* *示例**:
```python
result = md.convert("archive.zip")
```

- --

## 电子书格式

### EPUB (.epub)

* *功能**：
- 全文提取
- 章节结构
- 元数据提取

* *最适合**：
- 电子书
- 数字出版物
- 长格式内容

* *输出格式**：保留章节结构的Markdown

* *示例**：
```python
result = md.convert("book.epub")
```

- --

## 其他格式

### Outlook消息(.msg)

* *功能**：
- 电子邮件内容提取
- 附件列表
- 元数据（从、到、主题、日期）

* *依赖项**：
```bash
pip install 'markitdown[outlook]'
```

* *最佳对于**：
- 电子邮件存档
- 通讯记录

* *示例**：
```python
result = md.convert("message.msg")
```

- --

## 格式特定提示

### PDF最佳做法

1. **使用 Azure 文档智能进行复杂布局**：
 ```python
 md = MarkItDown(docintel_endpoint="endpoint_url")
 ```

2. **对于扫描的 PDF，请确保设置 OCR**：
 ```bash
 brew install tesseract # macOS
 ```

3. **在转换之前分割非常大的 PDF** 以获得更好的性能

### PowerPoint 最佳实践

1. **将 AI 用于视觉内容**：
 ```python
 md = MarkItDown(llm_client=client, llm_model="gpt-4o")
 ```

2. **检查演讲者备注** - 它们包含在输出

3 中。 **不会捕获复杂的动画** - 仅静态内容

### Excel 最佳实践

1. **大型电子表格**可能需要一些时间来转换

2. **公式转换为其计算值**

3. **多张**均包含在输出中

4. **图表成为文字描述**（使用AI以获得更好的描述）

### 图像最佳实践

1. **使用AI进行有意义的描述**：
 ```python
 md = MarkItDown(
 llm_client=client,
 llm_model="gpt-4o",
 llm_prompt="详细描述这个科学数字"
 )
 ```

2. **对于文本较多的图像，请确保安装 OCR 依赖项**

3. **高分辨率图像**可能需要更长的时间来处理

### 音频最佳实践

1. **清晰的音频**产生更好的转录

2. **长时间录音**可能需要大量时间

3. **考虑分割长音频文件**以加快处理速度

- --

## 不支持的格式

如果您需要转换不支持的格式：

1. **创建自定义转换器**（参见`api_reference.md`）
2. **在 GitHub (#markitdown-plugin)
3 上查找插件**。 **预转换为支持的格式**（例如，将.rtf转换为.docx）

- --

## 格式检测

MarkItDown自动检测来自：

1的格式。 **文件扩展名**（主要方法）
2. **MIME 类型**（后备）
3. **文件签名**（魔术字节，后备）

* *覆盖检测**：
```python
# Force specific format
result = md.convert("file_without_extension", file_extension=".pdf")

# With streams
with open("file", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
```
