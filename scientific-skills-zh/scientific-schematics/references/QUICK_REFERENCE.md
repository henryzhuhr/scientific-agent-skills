# 科学原理图 - 快速参考

* *工作原理：** 描述您的图表 → Nano Banana 2 自动生成它

## 设置（一次性）

```bash
# Get API key from https://openrouter.ai/keys
export OPENROUTER_API_KEY='sk-or-v1-your_key_here'

# Add to shell profile for persistence
echo 'export OPENROUTER_API_KEY="sk-or-v1-your_key"' >> ~/.bashrc  # or ~/.zshrc
```

## 基本用法

```bash
# Describe your diagram, Nano Banana 2 creates it
python scripts/generate_schematic.py "your diagram description" -o output.png

# That's it! Automatic:
# - Iterative refinement (3 rounds)
# - Quality review and improvement
# - Publication-ready output
```

## 常见示例

### CONSORT流程图
```bash
python scripts/generate_schematic.py \
  "CONSORT flow: screened n=500, excluded n=150, randomized n=350" \
  -o consort.png
```

### 神经网络
```bash
python scripts/generate_schematic.py \
  "Transformer architecture with encoder and decoder stacks" \
  -o transformer.png
```

### 生物通路
```bash
python scripts/generate_schematic.py \
  "MAPK pathway: EGFR → RAS → RAF → MEK → ERK" \
  -o mapk.png
```

### 电路 Diagram
```bash
python scripts/generate_schematic.py \
  "Op-amp circuit with 1kΩ resistor and 10µF capacitor" \
  -o circuit.png
```

## Command Options

|选项 |描述 | Example |
|--------|-------------|---------|
| `-o, --output` |输出文件路径 | `-o figures/diagram.png` |
| `--iterations N` |细化次数 (1-2) | `--iterations 2` |
| `-v, --verbose` |显示详细输出 | `-v` |
| `--api-key KEY` |提供API密钥| `--api-key sk-or-v1-...` |

## 提示提示

### ✓ 良好提示（具体）
- "CONSORT 流程图，筛选 (n=500)、排除 (n=150)、随机化 (n=350)"
- "Transformer 架构：编码器在左侧，6 层，解码器在右，交叉注意力连接"
- "MAPK信号：受体→RAS→RAF→MEK→ERK→细胞核，标记每个磷酸化"

### ✗避免（太模糊）
- "制作流程图"
- "神经网络"
- "路径图表“

## 输出文件

对于输入`diagram.png`，您得到：
- `diagram_v1.png` - 第一次迭代
- `diagram_v2.png` - 第二次迭代
- `diagram_v3.png` - 最终迭代
- `diagram.png` - 最终副本 
- `diagram_review_log.json` - 质量分数和评论

## 审核日志

```json
{
  "iterations": [
    {
      "iteration": 1,
      "score": 7.0,
      "critique": "Good start. Font too small..."
    },
    {
      "iteration": 2,
      "score": 8.5,
      "critique": "Much improved. Minor spacing issues..."
    },
    {
      "iteration": 3,
      "score": 9.5,
      "critique": "Excellent. Publication ready."
    }
  ],
  "final_score": 9.5
}
```

## Python API

```python
from scripts.generate_schematic_ai import ScientificSchematicGenerator

# Initialize
gen = ScientificSchematicGenerator(api_key="your_key")

# Generate
results = gen.generate_iterative(
    user_prompt="diagram description",
    output_path="output.png",
    iterations=2
)

# Check quality
print(f"Score: {results['final_score']}/10")
```

## 故障排除

### 未找到 API 密钥
```bash
# Check if set
echo $OPENROUTER_API_KEY

# Set it
export OPENROUTER_API_KEY='your_key'
```

### 导入错误
```bash
# Install requests
pip install requests
```

### 低质量分数
- 使提示更具体
- 包括布局详细信息（从左到右，从上到下）
- 指定标签要求
- 增加迭代：`--iterations 2`

## 测试

```bash
# Verify installation
python test_ai_generation.py

# Should show: "6/6 tests passed"
```

## 成本

每个图的典型成本（最多2个） iterations):
- Simple (1 iteration): $0.05-0.15
- Complex (2 iterations): $0.10-0.30

## Nano Banana 2 的工作原理

* *用自然语言简单描述您的图表：**
- ✓ 无需编码
- ✓ 无需模板
- ✓ 无需手动绘图
- ✓ 自动质量审查
- ✓ 可供出版的输出
- ✓ 适用于任何图表类型

* *只需描述你想要的内容，它就会自动生成。**

## 获取帮助

```bash
# Show help
python scripts/generate_schematic.py --help

# Verbose mode for debugging
python scripts/generate_schematic.py "diagram" -o out.png -v
```

## 快速入门清单

- [ ]设置`OPENROUTER_API_KEY`环境变量
- [ ]运行`python test_ai_generation.py` （应该通过 6/6）
- [ ]尝试：`python scripts/generate_schematic.py "test diagram" -o test.png`
- [ ]检查输出文件（test_v1.png、v2、v3、review_log.json）
- [ ]阅读 SKILL.md 了解详细文档
- [ ]检查 README.md 了解示例

## 资源

- 完整文档：`SKILL.md`
- 详细指南：`README.md`
- 实现详细信息：`IMPLEMENTATION_SUMMARY.md`
- 示例脚本：`example_usage.sh`
- 获取 API 密钥： https://openrouter.ai/keys
