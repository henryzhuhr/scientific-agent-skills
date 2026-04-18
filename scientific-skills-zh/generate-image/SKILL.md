---
name: generate-image
description: 使用 AI 模型（FLUX、Nano Banana 2）生成或编辑图像。用于生成通用图像，包括照片、插图、艺术作品、视觉资产、概念艺术以及任何非技术图表或原理图的图像。对于流程图、电路、路径和技术图表，请改用 scientific-schematics 技能。
license: MIT license
compatibility: Requires an OpenRouter API key
metadata:
    skill-author: K-Dense Inc.
---

# 生成图像

使用 OpenRouter 的图像生成模型（包括 FLUX.2 Pro 和 Gemini 3.1 Flash 图像预览）生成和编辑高质量图像。

## 何时使用此技能

* *使用 generate-image 用于：**
- 照片和真实感图像
- 艺术插图和艺术品
- 概念艺术和视觉概念
- 演示文稿或文档的视觉资产
- 图像编辑和修改
- 任何通用图像生成需求

* *使用scientific-schematics 代替：**
- 流程图和过程图
- 电路图和电气原理图
- 生物途径和信号级联
- 系统架构图
- CONSORT图和方法流程图
- 任何技术/示意图

## 快速入门

使用`scripts/generate_image.py`脚本生成或编辑images:

```bash
# Generate a new image
python scripts/generate_image.py "A beautiful sunset over mountains"

# Edit an existing image
python scripts/generate_image.py "Make the sky purple" --input photo.jpg
```

这会生成/编辑图像并将其保存为当前目录中的`generated_image.png`。

## API密钥设置

* *关键**：该脚本需要OpenRouter API密钥。运行之前，检查用户是否配置了 API 密钥：

1. 在项目目录或父目录
2中查找`.env`文件。检查`.env`文件
3中是否有`OPENROUTER_API_KEY=<key>`。如果未找到，请通知用户需要：
 - 使用 `OPENROUTER_API_KEY=your-api-key-here`
 创建 `.env` 文件 - 或设置环境变量：`export OPENROUTER_API_KEY=your-api-key-here`
 - 从以下位置获取 API 密钥：https://openrouter.ai/keys

 该脚本将自动检测`.env` 文件并在 API 密钥丢失时提供清晰的错误消息。

## 型号选择

* *默认型号**：`google/gemini-3.1-flash-image-preview`（高质量，推荐）

* *可用于生成和编辑的型号**：
- `google/gemini-3.1-flash-image-preview` - 高品质，支持生成 +编辑
- `black-forest-labs/flux.2-pro` - 快速、高质量、支持生成+编辑

* *仅限一代**：
- `black-forest-labs/flux.2-flex` - 快速且便宜，但质量不如 pro

 选择基于：
- **质量**：使用gemini-3.1-flash-image-preview或flux.2-pro
- **编辑**：使用gemini-3.1-flash-image-preview或Flux.2-pro（均支持图像编辑）
- **成本**：仅使用flux.2-flex进行生成

## 常用模式

### 基本生成
```bash
python scripts/generate_image.py "Your prompt here"
```

### 指定型号
```bash
python scripts/generate_image.py "A cat in space" --model "black-forest-labs/flux.2-pro"
```

### 自定义输出路径
```bash
python scripts/generate_image.py "Abstract art" --output artwork.png
```

### 编辑现有图像
```bash
python scripts/generate_image.py "Make the background blue" --input photo.jpg
```

### 使用特定模型编辑
```bash
python scripts/generate_image.py "Add sunglasses to the person" --input portrait.png --model "black-forest-labs/flux.2-pro"
```

### 使用自定义编辑输出
```bash
python scripts/generate_image.py "Remove the text from the image" --input screenshot.png --output cleaned.png
```

### 多个图像
使用不同的提示或输出路径多次运行脚本：
```bash
python scripts/generate_image.py "Image 1 description" --output image1.png
python scripts/generate_image.py "Image 2 description" --output image2.png
```

## 脚本参数

- `prompt`（必需）：要生成的图像的文本描述，或编辑说明
- `--input`或`-i`：输入编辑的图片路径（启用编辑模式）
- `--model`或`-m`：OpenRouter型号ID（默认：google/gemini-3.1-flash-image-preview）
- `--output` 或 `-o`：输出文件路径（默认： generated_image.png）
- `--api-key`：OpenRouter API 密钥（覆盖 .env 文件）

## 示例用例

### 用于科学文档
```bash
# Generate a conceptual illustration for a paper
python scripts/generate_image.py "Microscopic view of cancer cells being attacked by immunotherapy agents, scientific illustration style" --output figures/immunotherapy_concept.png

# Create a visual for a presentation
python scripts/generate_image.py "DNA double helix structure with highlighted mutation site, modern scientific visualization" --output slides/dna_mutation.png
```

### 用于演示文稿和海报
```bash
# Title slide background
python scripts/generate_image.py "Abstract blue and white background with subtle molecular patterns, professional presentation style" --output slides/background.png

# Poster hero image
python scripts/generate_image.py "Laboratory setting with modern equipment, photorealistic, well-lit" --output poster/hero.png
```

### 用于一般视觉内容
```bash
# Website or documentation images
python scripts/generate_image.py "Professional team collaboration around a digital whiteboard, modern office" --output docs/team_collaboration.png

# Marketing materials
python scripts/generate_image.py "Futuristic AI brain concept with glowing neural networks" --output marketing/ai_concept.png
```

## 错误处理

该脚本提供清晰的错误消息对于：
- 缺少 API 密钥（带有设置说明）
- API 错误（带有状态代码）
- 意外的响应格式
- 缺少依赖项（请求库）

如果脚本失败，请在重试之前阅读错误消息并解决问题。

## 注释

- 图像以 base64 编码的数据 URL 返回，并自动保存为 PNG 文件
  - 该脚本支持来自不同 OpenRouter 型号的 `images` 和 `content` 响应格式
  - 生成时间因型号而异（通常为 5-30 秒）
  - 对于图像编辑，输入图像被编码为 base64 并发送到model
- 支持的输入图像格式：PNG、JPEG、GIF、WebP
- 检查 OpenRouter 定价以获取成本信息：https://openrouter.ai/models

## 图像编辑提示

- 具体说明您想要的更改（例如，“将天空更改为日落颜色”与“编辑天空”）
- 参考中的特定元素尽可能使用图像
- 为了获得最佳效果，请使用清晰详细的编辑说明
- Gemini 3.1 Flash Image Preview 和 FLUX.2 Pro 都支持通过 OpenRouter 进行图像编辑

## 与其他技能集成

- **scientific-schematics**：用于技术图表、流程图、电路、路径
- **generate-image**：用于照片、插图、艺术品、视觉概念
- **scientific-slides**：与 generate-image 结合使用，实现视觉丰富的演示
- **latex-posters**：使用 generate-image 进行海报视觉效果和英雄图像
