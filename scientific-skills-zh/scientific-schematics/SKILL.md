---
name: scientific-schematics
description: 使用 Nano Banana 2 AI 和智能迭代细化创建出版质量的科学图表。使用 Gemini 3.1 Pro Preview 进行质量审核。仅当质量低于文档类型的阈值时才重新生成。专注于神经网络架构、系统图、流程图、生物路径和复杂的科学可视化。
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# 科学原理图和图表

## 概述

科学原理图和图表将复杂的概念转化为清晰的视觉表示以供出版。 **此技能使用 Nano Banana 2 AI 通过 Gemini 3.1 Pro Preview 质量审核来生成图表。**

* *工作原理：**
- 用自然语言描述您的图表
- Nano Banana 2 自动生成出版物质量的图像
- **Gemini 3.1 Pro Preview 根据文档类型阈值审核质量**
- **智能迭代**：仅如果质量低于阈值，则重新生成
- 在几分钟内即可出版的输出
- 无需编码、模板或手动绘图

* *按文档类型划分的质量阈值：**
|文件类型 |门槛|描述 |
|---------------|------------|------------|
|期刊| 8.5/10 |自然、科学、同行评审期刊 |
|会议| 8.0/10 |会议论文|
|论文| 8.0/10 |学位论文、论文|
|授予| 8.0/10 |资助提案|
|预印本 | 7.5/10 | arXiv、bioRxiv 等 |
|报告| 7.5/10 |技术报告|
|海报| 7.0/10 |学术海报|
|介绍| 6.5/10 |幻灯片、演讲 |
|默认 | 7.5/10 |通用 |

* *只需描述您想要的内容，Nano Banana 2 即可创建它。**所有图表都存储在图形/子文件夹中，并在论文/海报中引用。

## 快速入门：生成任何图表

通过简单描述即可创建任何科学图表。 Nano Banana 2 通过**智能迭代**自动处理一切：

```bash
# Generate for journal paper (highest quality threshold: 8.5/10)
python scripts/generate_schematic.py "CONSORT participant flow diagram with 500 screened, 150 excluded, 350 randomized" -o figures/consort.png --doc-type journal

# Generate for presentation (lower threshold: 6.5/10 - faster)
python scripts/generate_schematic.py "Transformer encoder-decoder architecture showing multi-head attention" -o figures/transformer.png --doc-type presentation

# Generate for poster (moderate threshold: 7.0/10)
python scripts/generate_schematic.py "MAPK signaling pathway from EGFR to gene transcription" -o figures/mapk_pathway.png --doc-type poster

# Custom max iterations (max 2)
python scripts/generate_schematic.py "Complex circuit diagram with op-amp, resistors, and capacitors" -o figures/circuit.png --iterations 2 --doc-type journal
```

* *幕后发生的事情：**
1. **第一代**：Nano Banana 2 按照科学图表最佳实践 
2 创建初始图像。 **评论 1**：**Gemini 3.1 Pro Preview** 根据文档类型阈值 
3 评估质量。 **决策**：如果质量 >= 阈值 → **完成**（不再需要迭代！）
4. **如果低于阈值**：根据批评改进提示，重新生成
5. **重复**：直到质量达到阈值或达到最大迭代次数

* *智能迭代的好处：**
- ✅ 如果第一代足够好，则节省 API 调用
- ✅ 期刊论文的更高质量标准
- ✅ 演示文稿/海报的周转速度更快
- ✅ 每次使用的适当质量case

* *输出**：版本化图像以及包含质量分数、评论和早期停止信息的详细审核日志。

### 配置

设置您的 OpenRouter API 密钥：
```bash
export OPENROUTER_API_KEY='your_api_key_here'
```

在以下位置获取 API 密钥： https://openrouter.ai/keys

### AI生成最佳实践

* *科学图表的有效提示：**

✓ **好的提示**（具体、详细）：
- 《CONSORT流程图显示从筛选（n=500）到随机化到最终分析的参与者流程》
-》Transformer左侧为编码器堆栈，右侧为解码器堆栈的神经网络架构，显示多头注意力和交叉注意力连接"
- "生物信号级联：EGFR受体→RAS→RAF→MEK→ERK→细胞核，磷酸化步骤标记为"
- "物联网系统框图：传感器→微控制器→WiFi模块→云服务器→移动应用程序"

✗ **避免模糊提示**：
- “制作流程图”（太通用）
- “神经网络”（哪种类型？什么组件？）
- “路径图”（哪个路径？什么分子？）

* *要包含的关键元素：**
- **类型**：流程图、架构图、路径、电路等。
- **组件**：要包含的特定元素
- **流程/方向**：元素如何连接（从左到右、从上到下）
- **标签**：要包含的关键注释或文本
- **样式**：任何特定的视觉要求

* *科学质量指南**（自动应用）：
- 干净的白色/浅色背景
- 高对比度以提高可读性
- 清晰、可读的标签（至少10pt）
- 专业排版（无衬线字体）
- 色盲友好颜色（Okabe-Ito 调色板）
- 适当的间距以防止拥挤
- 适当的比例尺、图例、轴

## 何时使用此技能

此技能应在以下情况下使用：
- 创建神经网络架构图（Transformers、CNN、RNN、等）
- 说明系统架构和数据流程图
- 绘制研究设计的方法流程图（CONSORT、PRISMA）
- 可视化算法工作流程和处理管道
- 创建电路图和电气原理图
- 描绘生物途径和分子相互作用
- 生成网络拓扑和层次结构
- 说明概念框架和理论模型
- 为技术论文设计框图

## 如何使用此技能

* *用自然语言简单地描述你的图表。** Nano Banana 2 生成它自动：

```bash
python scripts/generate_schematic.py "your diagram description" -o output.png
```

* *就是这样！** AI 处理：
- ✓ 布局和构图
- ✓ 标签和注释
- ✓ 颜色和造型
- ✓ 质量审查和细化
- ✓ 出版就绪输出

* *适用于所有图表类型：**
- 流程图（CONSORT、PRISMA 等）
- 神经网络架构
- 生物途径
- 电路图
- 系统架构
- 模块图表
- 任何科学可视化

* *无需编码，无需模板，无需手动绘图。**

- --

# AI 生成模式（Nano Banana 2 + Gemini 3.1 Pro 预览版审查）

## 智能迭代细化工作流程

AI 生成系统使用 **智能迭代** - 仅当质量低于您的文档类型的阈值时才重新生成：

### 如何智能迭代工作

```
┌─────────────────────────────────────────────────────┐
│  1. Generate image with Nano Banana 2             │
│                    ↓                                │
│  2. Review quality with Gemini 3.1 Pro Preview                │
│                    ↓                                │
│  3. Score >= threshold?                             │
│       YES → DONE! (early stop)                      │
│       NO  → Improve prompt, go to step 1            │
│                    ↓                                │
│  4. Repeat until quality met OR max iterations      │
└─────────────────────────────────────────────────────┘
```

### 迭代1：初始生成
* *提示构建：**
```
Scientific diagram guidelines + User request
```

* *输出：** `diagram_v1.png`

### Gemini 3.1 Pro的质量审查Preview

Gemini 3.1 Pro Preview 评估图表：
1. **科学准确性**（0-2 分） - 正确的概念、符号、关系
2. **清晰度和可读性**（0-2 分） - 易于理解，层次清晰
3. **标签质量**（0-2 分）- 完整、可读、一致的标签
4. **布局和构图**（0-2分） - 逻辑流程、平衡、无重叠
5. **专业外观**（0-2 分）- 可供出版的质量

* *审核输出示例：**
```
SCORE: 8.0

STRENGTHS:
- Clear flow from top to bottom
- All phases properly labeled
- Professional typography

ISSUES:
- Participant counts slightly small
- Minor overlap on exclusion box

VERDICT: ACCEPTABLE (for poster, threshold 7.0)
```

### 决策点：继续还是停止？

|如果得分... |动作 |
|-------------|--------|
| >= 阈值 | **停止** - 对于此文档类型而言，质量足够好 |
| <阈值|使用改进的提示继续下一次迭代 |

* *示例：**
- 对于 **海报**（阈值 7.0）：分数 7.5 → **1 次迭代后完成！**
- 对于 **期刊**（阈值 8.5）：分数 7.5 → 继续改进

### 后续迭代（仅在需要时）

如果质量低于阈值，系统：
1. 从 Gemini 3.1 Pro Preview 的评论 
2 中提取具体问题。通过改进说明增强提示
3. 使用纳米香蕉 2
4 再生。再次使用 Gemini 3.1 Pro Preview
5 进行评测。重复直到达到阈值或达到最大迭代次数

### 审核日志
所有迭代均以包含早期停止信息的 JSON 审核日志保存：
```json
{
  "user_prompt": "CONSORT participant flow diagram...",
  "doc_type": "poster",
  "quality_threshold": 7.0,
  "iterations": [
    {
      "iteration": 1,
      "image_path": "figures/consort_v1.png",
      "score": 7.5,
      "needs_improvement": false,
      "critique": "SCORE: 7.5\nSTRENGTHS:..."
    }
  ],
  "final_score": 7.5,
  "early_stop": true,
  "early_stop_reason": "Quality score 7.5 meets threshold 7.0 for poster"
}
```

* *注意：** 使用智能迭代，如果提早达到质量，您可能只会看到 1 个迭代，而不是完整的 2 个迭代！

## 高级 AI 生成用法

### Python API

```python
from scripts.generate_schematic_ai import ScientificSchematicGenerator

# Initialize generator
generator = ScientificSchematicGenerator(
    api_key="your_openrouter_key",
    verbose=True
)

# Generate with iterative refinement (max 2 iterations)
results = generator.generate_iterative(
    user_prompt="Transformer architecture diagram",
    output_path="figures/transformer.png",
    iterations=2
)

# Access results
print(f"Final score: {results['final_score']}/10")
print(f"Final image: {results['final_image']}")

# Review individual iterations
for iteration in results['iterations']:
    print(f"Iteration {iteration['iteration']}: {iteration['score']}/10")
    print(f"Critique: {iteration['critique']}")
```

### 命令行选项

```bash
# Basic usage (default threshold 7.5/10)
python scripts/generate_schematic.py "diagram description" -o output.png

# Specify document type for appropriate quality threshold
python scripts/generate_schematic.py "diagram" -o out.png --doc-type journal      # 8.5/10
python scripts/generate_schematic.py "diagram" -o out.png --doc-type conference   # 8.0/10
python scripts/generate_schematic.py "diagram" -o out.png --doc-type poster       # 7.0/10
python scripts/generate_schematic.py "diagram" -o out.png --doc-type presentation # 6.5/10

# Custom max iterations (1-2)
python scripts/generate_schematic.py "complex diagram" -o diagram.png --iterations 2

# Verbose output (see all API calls and reviews)
python scripts/generate_schematic.py "flowchart" -o flow.png -v

# Provide API key via flag
python scripts/generate_schematic.py "diagram" -o out.png --api-key "sk-or-v1-..."

# Combine options
python scripts/generate_schematic.py "neural network" -o nn.png --doc-type journal --iterations 2 -v
```

### 提示工程提示

* *1.具体布局：**
```
✓ "Flowchart with vertical flow, top to bottom"
✓ "Architecture diagram with encoder on left, decoder on right"
✓ "Circular pathway diagram with clockwise flow"
```

* *2。包括定量详细信息：**
```
✓ "Neural network with input layer (784 nodes), hidden layer (128 nodes), output (10 nodes)"
✓ "Flowchart showing n=500 screened, n=150 excluded, n=350 randomized"
✓ "Circuit with 1kΩ resistor, 10µF capacitor, 5V source"
```

* *3。指定视觉样式：**
```
✓ "Minimalist block diagram with clean lines"
✓ "Detailed biological pathway with protein structures"
✓ "Technical schematic with engineering notation"
```

* *4。请求特定标签：**
```
✓ "Label all arrows with activation/inhibition"
✓ "Include layer dimensions in each box"
✓ "Show time progression with timestamps"
```

* *5。提及颜色要求：**
```
✓ "Use colorblind-friendly colors"
✓ "Grayscale-compatible design"
✓ "Color-code by function: blue for input, green for processing, red for output"
```

## AI生成示例

### 示例1：CONSORT流程图
```bash
python scripts/generate_schematic.py \
  "CONSORT participant flow diagram for randomized controlled trial. \
   Start with 'Assessed for eligibility (n=500)' at top. \
   Show 'Excluded (n=150)' with reasons: age<18 (n=80), declined (n=50), other (n=20). \
   Then 'Randomized (n=350)' splits into two arms: \
   'Treatment group (n=175)' and 'Control group (n=175)'. \
   Each arm shows 'Lost to follow-up' (n=15 and n=10). \
   End with 'Analyzed' (n=160 and n=165). \
   Use blue boxes for process steps, orange for exclusion, green for final analysis." \
  -o figures/consort.png
```

### 示例2：神经网络架构
```bash
python scripts/generate_schematic.py \
  "Transformer encoder-decoder architecture diagram. \
   Left side: Encoder stack with input embedding, positional encoding, \
   multi-head self-attention, add & norm, feed-forward, add & norm. \
   Right side: Decoder stack with output embedding, positional encoding, \
   masked self-attention, add & norm, cross-attention (receiving from encoder), \
   add & norm, feed-forward, add & norm, linear & softmax. \
   Show cross-attention connection from encoder to decoder with dashed line. \
   Use light blue for encoder, light red for decoder. \
   Label all components clearly." \
  -o figures/transformer.png --iterations 2
```

### 示例3：生物途径
```bash
python scripts/generate_schematic.py \
  "MAPK signaling pathway diagram. \
   Start with EGFR receptor at cell membrane (top). \
   Arrow down to RAS (with GTP label). \
   Arrow to RAF kinase. \
   Arrow to MEK kinase. \
   Arrow to ERK kinase. \
   Final arrow to nucleus showing gene transcription. \
   Label each arrow with 'phosphorylation' or 'activation'. \
   Use rounded rectangles for proteins, different colors for each. \
   Include membrane boundary line at top." \
  -o figures/mapk_pathway.png
```

### 示例4：系统架构
```bash
python scripts/generate_schematic.py \
  "IoT system architecture block diagram. \
   Bottom layer: Sensors (temperature, humidity, motion) in green boxes. \
   Middle layer: Microcontroller (ESP32) in blue box. \
   Connections to WiFi module (orange box) and Display (purple box). \
   Top layer: Cloud server (gray box) connected to mobile app (light blue box). \
   Show data flow arrows between all components. \
   Label connections with protocols: I2C, UART, WiFi, HTTPS." \
  -o figures/iot_architecture.png
```

- --

## 命令行使用

生成科学原理图的主要入口点：

```bash
# Basic usage
python scripts/generate_schematic.py "diagram description" -o output.png

# Custom iterations (max 2)
python scripts/generate_schematic.py "complex diagram" -o diagram.png --iterations 2

# Verbose mode
python scripts/generate_schematic.py "diagram" -o out.png -v
```

* *注：** Nano Banana 2 AI生成系统在其迭代细化过程中包括自动质量审查。每次迭代都会评估科学准确性、清晰度和可访问性。

## 最佳实践摘要

### 设计原则

1. **清晰胜于复杂** - 简化，删除不必要的元素
2. **一致的样式** - 使用模板和样式文件
3. **色盲辅助功能** - 使用 Okabe-Ito 调色板，冗余编码
4. **适当的排版** - 无衬线字体，至少 7-8 pt
5. **矢量格式** - 始终使用 PDF/SVG 进行发布

### 技术要求

1. **分辨率** - 首选矢量，或光栅 
2 为 300+ DPI。 **文件格式** - LaTeX 为 PDF，Web 为 SVG，PNG 作为备用 
3. **色彩空间** - RGB 用于数字，CMYK 用于打印（如果需要则转换）
4. **线宽** - 最小 0.5 pt，典型 1-2 pt
5. **文本大小** - 最终大小至少 7-8 pt

### 集成指南

1. **包含在 LaTeX 中** - 使用 `\includegraphics{}` 生成图像
2. **完整的标题** - 描述所有元素和缩写
3. **文本参考** - 叙述流程中的解释图
4. **保持一致性** - 论文 
5 中所有图形的风格相同。 **版本控制** - 将提示和生成的图像保留在存储库中

## 常见问题故障排除

### AI生成问题

* *问题**：重叠文本或元素
- **解决方案**：AI生成自动处理间距
- **解决方案**：增加迭代：`--iterations 2`以获得更好的效果细化

* *问题**：元素未正确连接
- **解决方案**：让您的提示更具体地了解连接和布局
- **解决方案**：增加迭代以获得更好的细化

### 图像质量问题

* *问题**：导出质量较差
- **解决方案**：AI生成产生自动生成高质量图像
- **解决方案**：增加迭代以获得更好的结果：`--iterations 2`

* *问题**：生成后元素重叠
- **解决方案**：AI生成自动处理间距
- **解决方案**：增加迭代：`--iterations 2`以获得更好的细化
- **解决方案**：使提示更具体地说明布局和间距要求

### 质量检查问题

* *问题**：误报重叠检测
- **解决方案**：调整阈值：`detect_overlaps(image_path, threshold=0.98)`
- **解决方案**：手动检查可视报告中的标记区域

* *问题**：生成的图像质量较低
- **解决方案**：AI生成默认生成高质量图像
- **解决方案**：增加迭代以获得更好的结果：`--iterations 2`

* *问题**：色盲模拟显示对比度较差
- **解决方案**：在中明确切换到Okabe-Ito调色板代码
- **解决方案**：添加冗余编码（形状、图案、线条样式）
- **解决方案**：增加颜色饱和度和亮度差异

* *问题**：检测到高度严重的重叠
- **解决方案**：查看overlap_report.json以获取确切位置
- **解决方案**：增加这些特定位置中的间距地区
- **解决方案**：使用调整后的参数重新运行并再次验证

  * *问题**：可视化报告生成失败
- **解决方案**：检查Pillow和matplotlib安装
- **解决方案**：确保图像文件可读：`Image.open(path).verify()`
- **解决方案**：检查是否有足够的磁盘空间用于生成报告

### 可访问性问题

* *问题**：灰度中的颜色无法区分
- **解决方案**：运行可访问性检查器：`verify_accessibility(image_path)`
- **解决方案**：添加图案、形状或线条样式以实现冗余
- **解决方案**：增加相邻元素之间的对比度

  * *问题**：打印时文本太小
- **解决方案**：运行分辨率验证器：`validate_resolution(image_path)`
- **解决方案**：按最终尺寸设计，使用最小7-8 pt字体
- **解决方案**：检查分辨率中的物理尺寸报告

* *问题**：可访问性检查始终失败
- **解决方案**：查看accessibility_report.json以了解特定故障
- **解决方案**：将颜色对比度增加至少20％
- **解决方案**：在最终确定之前使用实际灰度转换进行测试

## 资源和参考文献

### 详细参考文献

加载这些文件以获取有关特定主题的全面信息：

- **`references/best_practices.md`** - 出版标准和可访问性指南

### 外部资源

* *Python 库**
- Schemdraw 文档：https://schemdraw.readthedocs.io/
- NetworkX 文档：https://networkx.org/documentation/
- Matplotlib 文档：https://matplotlib.org/

* *出版标准**
- 自然图形指南：https://www.nature.com/nature/for-authors/final-submission
- 科学图形指南：https://www.science.org/content/page/instructions-preparing-initial-manuscript
- CONSORT 图：http://www.consort-statement.org/consort-statement/flow-diagram

## 与其他技能集成

此技能与以下技能协同工作：

- **科学写作** - 图表遵循图形最佳实践
- **科学可视化** - 共享调色板和样式
- **LaTeX 海报** - 生成海报演示图表
- **研究资助** - 提案的方法图
- **同行评审** - 评估图表清晰度和可访问性

## 快速参考清单

在提交图表之前，验证：

### 视觉质量
- [ ]高质量图像格式（AI 生成的 PNG）
- [ ]无重叠元素（AI 自动处理）
- [ ]所有组件之间有足够的间距（AI 优化）
- [ ]干净、专业的对齐
- [ ]所有箭头正确连接到预期目标

### 可访问性
- [ ]使用色盲安全调色板（Okabe-Ito）
- [ ]以灰度工作（使用可访问性检查器进行测试）
- [ ]元素之间有足够的对比度（已验证）
- [ ]在适当的情况下进行冗余编码（形状+颜色）
- [ ]色盲模拟通过所有检查

### 排版和可读性
- [ ]最终尺寸的文本最小 7-8 磅
- [ ]所有元素均清晰完整地标记
- [ ]一致的字体系列和尺寸
- [ ]无文本重叠或截断
- [ ]包括适用的单位

### 出版物标准
- [ ]与稿件中其他图形保持一致的样式
- [ ]定义了所有缩写的综合标题
- [ ]在稿件文本中适当引用
- [ ]符合期刊特定的尺寸要求
- [ ]以期刊要求的格式导出(PDF/EPS/TIFF)

### 质量验证（必需）
- [ ]运行 `run_quality_checks()` 并获得 PASS 状态
- [ ]审核重叠检测报告（零高严重性重叠）
- [ ]通过可访问性验证（灰度和色盲）
- [ ]在目标 DPI 下验证分辨率（打印时为 300+）
- [ ]生成并审核视觉质量报告
- [ ]所有质量报告与图形文件一起保存

### 文档和版本控制
- [ ]保存源文件（.tex、.py）供将来使用revision
- []质量报告存档在 `quality_reports/` 目录中
- []记录配置参数（颜色、间距、大小）
- [] Git 提交包括源、输出和质量报告
- []自述文件或注释解释如何重新生成图

### 最终集成检查
- [ ]图在编译的手稿中正确显示
- [ ]交叉引用工作（`\ref{}` 指向正确的图）
- [ ]图编号与文本引用匹配
- [ ]标题出现在相对于图的正确页面上
- [ ]没有与以下相关的编译警告或错误图

## 环境设置

```bash
# Required
export OPENROUTER_API_KEY='your_api_key_here'

# Get key at: https://openrouter.ai/keys
```

## 入门

* *最简单的可能用法：**
```bash
python scripts/generate_schematic.py "your diagram description" -o output.png
```

- --

使用此技能可以创建清晰、易于理解、达到出版质量的图表，从而有效地传达复杂的科学概念。由人工智能驱动的工作流程通过迭代细化确保图表符合专业标准。
