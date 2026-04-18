# MarkItDown API参考

## 核心类

### MarkItDown

文件转换为Markdown的主类。

```python
from markitdown import MarkItDown

md = MarkItDown(
    llm_client=None,
    llm_model=None,
    llm_prompt=None,
    docintel_endpoint=None,
    enable_plugins=False
)
```

#### 参数

|参数|类型 |默认|描述 |
|-----------|------|---------|------------|
| `llm_client` | OpenAI 客户端 | `None` |用于 AI 图像描述的 OpenAI 兼容客户端 |
| `llm_model` | STR | `None` |图像描述的模型名称（例如“anthropic/claude-opus-4.5”）|
| `llm_prompt` | STR | `None` |图片描述自定义提示|
| `docintel_endpoint` | STR | `None` | Azure 文档智能端点 |
| `enable_plugins` |布尔 | `False` |启用第 3 方插件 |

#### 方法

##### Convert()

将文件转换为 Markdown。

```python
result = md.convert(
    source,
    file_extension=None
)
```

* *参数**:
- `source` (str): 文件路径Convert
- `file_extension`（str，可选）：覆盖文件扩展名检测

* *返回**：`DocumentConverterResult`对象

* *示例**：
```python
result = md.convert("document.pdf")
print(result.text_content)
```

##### Convert_stream()

从类文件二进制流转换。

```python
result = md.convert_stream(
    stream,
    file_extension
)
```

* *参数**：
- `stream` (BinaryIO)：类二进制文件对象（例如，在 `"rb"` 中打开的文件） mode)
- `file_extension` (str)：确定转换方法的文件扩展名（例如“.pdf”）

* *返回**：`DocumentConverterResult` object

* *示例**：
```python
with open("document.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
    print(result.text_content)
```

* *重要**：流必须以二进制模式（`"rb"`）打开，而不是文本模式。

## Result Object

### DocumentConverterResult

转换的结果操作。

#### 属性

|属性 |类型 |描述|
|---------|------|----------|
| `text_content` | STR |转换后的 Markdown 文本 |
| `title` | STR |文档标题（如果有） |

#### 示例

```python
result = md.convert("paper.pdf")

# Access content
content = result.text_content

# Access title (if available)
title = result.title
```

## 自定义转换器

您可以通过实现 `DocumentConverter` 接口来创建自定义文档转换器。

### DocumentConverter Interface

```python
from markitdown import DocumentConverter

class CustomConverter(DocumentConverter):
    def convert(self, stream, file_extension):
        """
        Convert a document from a binary stream.
        
        Parameters:
            stream (BinaryIO): Binary file-like object
            file_extension (str): File extension (e.g., ".custom")
            
        Returns:
            DocumentConverterResult: Conversion result
        """
        # Your conversion logic here
        pass
```

### 注册自定义转换器

```python
from markitdown import MarkItDown, DocumentConverter, DocumentConverterResult

class MyCustomConverter(DocumentConverter):
    def convert(self, stream, file_extension):
        content = stream.read().decode('utf-8')
        markdown_text = f"# Custom Format\n\n{content}"
        return DocumentConverterResult(
            text_content=markdown_text,
            title="Custom Document"
        )

# Create MarkItDown instance
md = MarkItDown()

# Register custom converter for .custom files
md.register_converter(".custom", MyCustomConverter())

# Use it
result = md.convert("myfile.custom")
```

## 插件系统

### 查找插件

在 GitHub 中搜索 `#markitdown-plugin` 标签。

### 使用插件

```python
from markitdown import MarkItDown

# Enable plugins
md = MarkItDown(enable_plugins=True)
result = md.convert("document.pdf")
```

### 创建插件

插件是用MarkItDown.

* *插件注册转换器的Python包结构**:
```
my-markitdown-plugin/
├── setup.py
├── my_plugin/
│   ├── __init__.py
│   └── converter.py
└── README.md
```

* *setup.py**:
```python
from setuptools import setup

setup(
    name="markitdown-my-plugin",
    version="0.1.0",
    packages=["my_plugin"],
    entry_points={
        "markitdown.plugins": [
            "my_plugin = my_plugin.converter:MyConverter",
        ],
    },
)
```

* *converter.py**:
```python
from markitdown import DocumentConverter, DocumentConverterResult

class MyConverter(DocumentConverter):
    def convert(self, stream, file_extension):
        # Your conversion logic
        content = stream.read()
        markdown = self.process(content)
        return DocumentConverterResult(
            text_content=markdown,
            title="My Document"
        )
    
    def process(self, content):
        # Process content
        return "# Converted Content\n\n..."
```

## AI增强转换

### 使用OpenRouter进行图像描述

```python
from markitdown import MarkItDown
from openai import OpenAI

# Initialize OpenRouter client (OpenAI-compatible API)
client = OpenAI(
    api_key="your-openrouter-api-key",
    base_url="https://openrouter.ai/api/v1"
)

# Create MarkItDown with AI support
md = MarkItDown(
    llm_client=client,
    llm_model="anthropic/claude-opus-4.5",  # recommended for scientific vision
    llm_prompt="Describe this image in detail for scientific documentation"
)

# Convert files with images
result = md.convert("presentation.pptx")
```

### 通过OpenRouter提供的型号

具有视觉支持的热门型号：
- `anthropic/claude-opus-4.5` - **推荐用于科学视觉**
- `google/gemini-3-pro-preview` - Gemini Pro Vision

请参阅 https://openrouter.ai/models 了解完整列表。

### 自定义提示

```python
# For scientific diagrams
scientific_prompt = """
Analyze this scientific diagram or chart. Describe:
1. The type of visualization (graph, chart, diagram, etc.)
2. Key data points or trends
3. Labels and axes
4. Scientific significance
Be precise and technical.
"""

md = MarkItDown(
    llm_client=client,
    llm_model="anthropic/claude-opus-4.5",
    llm_prompt=scientific_prompt
)
```

## Azure 文档智能

### 设置

1. 创建 Azure 文档智能资源
2. 获取端点 URL
3. 设置身份验证

### 用法

```python
from markitdown import MarkItDown

md = MarkItDown(
    docintel_endpoint="https://YOUR-RESOURCE.cognitiveservices.azure.com/"
)

result = md.convert("complex_document.pdf")
```

### 身份验证

设置环境变量：
```bash
export AZURE_DOCUMENT_INTELLIGENCE_KEY="your-key"
```

或以编程方式传递凭据。

## 错误处理

```python
from markitdown import MarkItDown

md = MarkItDown()

try:
    result = md.convert("document.pdf")
    print(result.text_content)
except FileNotFoundError:
    print("File not found")
except ValueError as e:
    print(f"Invalid file format: {e}")
except Exception as e:
    print(f"Conversion error: {e}")
```

## 性能提示

### 1.重用MarkItDown实例

```python
# Good: Create once, use many times
md = MarkItDown()

for file in files:
    result = md.convert(file)
    process(result)
```

### 2.使用流处理大型文件

```python
# For large files
with open("large_file.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
```

### 3. 批处理

```python
from concurrent.futures import ThreadPoolExecutor

md = MarkItDown()

def convert_file(filepath):
    return md.convert(filepath)

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(convert_file, file_list)
```

## 重大更改（v0.0.1 到 v0.1.0）

1. **依赖项**：现在组织成可选功能组
 ```bash
 # Old
pip install markitdown
 
 # New
pip install 'markitdown[all]'
 ``

2. **convert_stream()**: 现在需要类似二进制文件的对象
 ```python
 # 旧的（也接受文本）
with open("file.pdf", "r") as f: # 文本模式
 result = md.convert_stream(f)
 
 # 新（仅限二进制）
with open("file.pdf", "rb") as f: # 二进制模式
 result = md.convert_stream(f, file_extension=".pdf")
 ```

3. **DocumentConverter Interface**：更改为从流读取而不是文件路径
  - 未创建临时文件
  - 内存效率更高
  - 插件需要更新

## 版本兼容性

- **Python**：需要3.10或更高版本
- **依赖项**：检查`setup.py` 版本限制
- **OpenAI**：兼容 OpenAI Python SDK v1.0+

## 环境变量

|变量|描述 |示例 |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` |用于图像描述的 OpenRouter API 密钥 | `sk-or-v1-...` |
| `AZURE_DOCUMENT_INTELLIGENCE_KEY` | Azure DI 身份验证 | `key123...` |
| `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT` | Azure DI 端点 | `https://...` |
