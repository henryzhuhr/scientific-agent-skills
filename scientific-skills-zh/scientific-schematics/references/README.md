# 科学示意图 - Nano Banana 2

* *通过用自然语言描述来生成任何科学图表。**

Nano Banana 2 自动创建出版物质量的图表 - 无需编码、无需模板、无需手动绘图。

## 快速入门

### 生成任何图表

```bash
# Set your OpenRouter API key
export OPENROUTER_API_KEY='your_api_key_here'

# Generate any scientific diagram
python scripts/generate_schematic.py "CONSORT participant flow diagram" -o figures/consort.png

# Neural network architecture
python scripts/generate_schematic.py "Transformer encoder-decoder architecture" -o figures/transformer.png

# Biological pathway
python scripts/generate_schematic.py "MAPK signaling pathway" -o figures/pathway.png
```

### 您将获得什么

- **最多两次迭代**（v1、v2），逐步细化
- **每次迭代后自动质量审核**
- **详细的审核日志**，包含分数和评论（JSON 格式）
- **可发布的图像** 遵循科学标准

## 功能

### 迭代细化过程

1. **第一代**：根据您的描述
2 创建初始图表。 **评论 1**：人工智能评估清晰度、标签、准确性、可访问性
3. **第 2 代**：基于 critique
4 进行改进。 **评论 2**：第二次评估，具体反馈
5. **第 3 代**：最终抛光版本

### 自动质量标准

所有图表自动遵循：
- 干净的白色/浅色背景
- 高对比度以提高可读性
- 清晰的标签（最小10pt字体）
- 专业排版
- 色盲友好的颜色
- 元素之间适当的间距
- 适当的比例尺、图例、轴

## 安装

### 用于AI生成

```bash
# Get OpenRouter API key
# Visit: https://openrouter.ai/keys

# Set environment variable
export OPENROUTER_API_KEY='sk-or-v1-...'

# Or add to .env file
echo "OPENROUTER_API_KEY=sk-or-v1-..." >> .env

# Install Python dependencies (if not already installed)
pip install requests
```

## 使用示例

### 示例1：CONSORT流程图

```bash
python scripts/generate_schematic.py \
  "CONSORT participant flow diagram for RCT. \
   Assessed for eligibility (n=500). \
   Excluded (n=150): age<18 (n=80), declined (n=50), other (n=20). \
   Randomized (n=350) into Treatment (n=175) and Control (n=175). \
   Lost to follow-up: 15 and 10 respectively. \
   Final analysis: 160 and 165." \
  -o figures/consort.png
```

* *输出：**
- `figures/consort_v1.png` - 初始生成
- `figures/consort_v2.png` - 第一次审核后
- `figures/consort_v3.png` - 最终版本
- `figures/consort.png` - 最终版本的副本
- `figures/consort_review_log.json` - 详细回顾日志

### 示例2：神经网络架构

```bash
python scripts/generate_schematic.py \
  "Transformer architecture with encoder on left (input embedding, \
   positional encoding, multi-head attention, feed-forward) and \
   decoder on right (masked attention, cross-attention, feed-forward). \
   Show cross-attention connection from encoder to decoder." \
  -o figures/transformer.png \
  --iterations 2
```

### 示例3：生物Pathway

```bash
python scripts/generate_schematic.py \
  "MAPK signaling pathway: EGFR receptor → RAS → RAF → MEK → ERK → nucleus. \
   Label each step with phosphorylation. Use different colors for each kinase." \
  -o figures/mapk.png
```

### 示例 4：系统架构

```bash
python scripts/generate_schematic.py \
  "IoT system block diagram: sensors (bottom) → microcontroller → \
   WiFi module and display (middle) → cloud server → mobile app (top). \
   Label all connections with protocols." \
  -o figures/iot_system.png
```

## 命令行选项

```bash
python scripts/generate_schematic.py [OPTIONS] "description" -o output.png

Options:
  --iterations N          Number of AI refinement iterations (default: 2, max: 2)
  --api-key KEY          OpenRouter API key (or use env var)
  -v, --verbose          Verbose output
  -h, --help             Show help message
```

## Python API

```python
from scripts.generate_schematic_ai import ScientificSchematicGenerator

# Initialize
generator = ScientificSchematicGenerator(
    api_key="your_key",
    verbose=True
)

# Generate with iterative refinement
results = generator.generate_iterative(
    user_prompt="CONSORT flowchart",
    output_path="figures/consort.png",
    iterations=2
)

# Access results
print(f"Final score: {results['final_score']}/10")
print(f"Final image: {results['final_image']}")

# Review iterations
for iteration in results['iterations']:
    print(f"Iteration {iteration['iteration']}: {iteration['score']}/10")
    print(f"Critique: {iteration['critique']}")
```

## 提示工程技巧

### 具体说明布局
✓“垂直流的流程图，从上到下”
✓“左侧编码器，右侧解码器的架构图”
✗“制作图表”（太模糊）

### 包括定量细节
✓“神经网络：输入（784），隐藏（128），输出(10)" 
✓“流程图：n=500 筛选，n=150 排除，n=350 随机” 
✗“一些数字”（非具体）

### 指定视觉风格
✓“线条清晰的简约框图” 
✓“带有蛋白质结构的详细生物途径” 
✓“带有工程符号的技术原理图”

### 请求特定标签
✓“用激活/抑制标记所有箭头”
✓“在每个框中包含层尺寸”
✓“用时间戳显示时间进度”

### 提及颜色要求
✓“使用色盲友好的颜色”
✓“灰度兼容设计”
✓“按功能进行颜色代码：蓝色=输入，绿色=处理，红色=输出”

## 审核日志格式

每次生成都会生成JSON审核log:

```json
{
  "user_prompt": "CONSORT participant flow diagram...",
  "iterations": [
    {
      "iteration": 1,
      "image_path": "figures/consort_v1.png",
      "prompt": "Full generation prompt...",
      "critique": "Score: 7/10. Issues: font too small...",
      "score": 7.0,
      "success": true
    },
    {
      "iteration": 2,
      "image_path": "figures/consort_v2.png",
      "score": 8.5,
      "critique": "Much improved. Remaining issues..."
    },
    {
      "iteration": 3,
      "image_path": "figures/consort_v3.png",
      "score": 9.5,
      "critique": "Excellent. Publication ready."
    }
  ],
  "final_image": "figures/consort_v3.png",
  "final_score": 9.5,
  "success": true
}
```

## 为什么使用 Nano Banana 2

* *简单地描述你想要什么 - Nano Banana 2 创建它：**

- ✓ **快速**：在几分钟内得到结果
- ✓ **简单**：自然语言描述（无编码）
- ✓ **质量**：自动审查和细化
- ✓ **通用**：适用于所有图表类型
- ✓ **出版就绪**：立即高质量输出

* *只需描述您的图表，它就会自动生成。**

## 故障排除

### API 密钥问题

```bash
# Check if key is set
echo $OPENROUTER_API_KEY

# Set temporarily
export OPENROUTER_API_KEY='your_key'

# Set permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export OPENROUTER_API_KEY="your_key"' >> ~/.bashrc
```

### 导入错误

```bash
# Install requests library
pip install requests

# Or use the package manager
pip install -r requirements.txt
```

### 生成失败

```bash
# Use verbose mode to see detailed errors
python scripts/generate_schematic.py "diagram" -o out.png -v

# Check API status
curl https://openrouter.ai/api/v1/models
```

### 低质量得分

如果迭代得分始终低于7/10：
1. 让您的提示更加具体
2. 包括有关布局和标签的更多详细信息
3. 明确指定视觉要求
4. 增加迭代次数：`--iterations 2`

## 测试

运行验证测试：

```bash
python test_ai_generation.py
```

此测试：
- 文件结构
- 模块导入
- 类初始化
- 错误处理
- 提示工程
- 包装器脚本

## 成本考虑

OpenRouter 定价使用的模型：
- **Nano Banana 2**：~$2/M 输入代币，~$12/M 输出代币

 每个图的典型成本：
- 简单图（1 次迭代）：~$0.05-0.15
- 复杂图（2 次迭代）： ~$0.10-0.30

## 示例库

请参阅完整的 SKILL.md 以获取广泛的示例，包括：
- CONSORT 流程图
- 神经网络架构（Transformers、CNN、RNN）
- 生物路径
- 电路图
- 系统架构
- 框图

## 支持

如有问题或疑问：
1. 检查 SKILL.md 了解详细文档
2. 运行 test_ai_ Generation.py 来验证 setup
3. 使用详细模式（-v）查看详细错误
4. 查看 review_log.json 以获取质量反馈

## 许可证

科学作家包的一部分。请参阅主存储库以获取许可证信息。
