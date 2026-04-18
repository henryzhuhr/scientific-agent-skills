---
name: hypogenic
description: 自动生成 LLM 驱动的假设并在表格数据集上进行测试。当您想要系统地探索有关经验数据模式的假设（例如，欺骗检测、内容分析）时使用。将文献见解与数据驱动的假设检验相结合。对于手动假设制定，请使用 hypothesis-generation；对于创意构思，请使用 scientific-brainstorming。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Hypogenic

## 概述

Hypogenic 使用大型语言模型提供自动假设生成和测试，以加速科学发现。该框架支持三种方法：HypoGeniC（数据驱动的假设生成）、HypoRefine（协同文献和数据集成）和 Union 方法（文献和数据驱动的假设的机械组合）。

## 快速入门

开始使用 Hypogenic分钟：

```bash
# Install the package
uv pip install hypogenic

# Clone example datasets
git clone https://github.com/ChicagoHAI/HypoGeniC-datasets.git ./data

# Run basic hypothesis generation
hypogenic_generation --config ./data/your_task/config.yaml --method hypogenic --num_hypotheses 20

# Run inference on generated hypotheses
hypogenic_inference --config ./data/your_task/config.yaml --hypotheses output/hypotheses.json
```

* *或使用Python API：**

```python
from hypogenic import BaseTask

# Create task with your configuration
task = BaseTask(config_path="./data/your_task/config.yaml")

# Generate hypotheses
task.generate_hypotheses(method="hypogenic", num_hypotheses=20)

# Run inference
results = task.inference(hypothesis_bank="./output/hypotheses.json")
```

## 何时使用此技能

在处理：
- 从观察数据集生成科学假设
- 测试多个竞争假设时使用此技能系统地
- 将文献见解与经验模式相结合
- 通过自动假设构思加速研究发现
- 需要假设驱动分析的领域：欺骗检测、人工智能生成的内容识别、心理健康指标、预测建模或其他实证研究

## 主要特征

* *自动假设生成**
- 在几分钟内从数据生成 10-20 多个可测试的假设
- 基于验证性能的迭代细化
- 支持基于 API 的（OpenAI、Anthropic）和本地 LLM

* *文献集成**
- 通过 PDF 从研究论文中提取见解处理
- 将理论基础与经验模式相结合
- 使用 GROBID 的系统文献到假设管道

* *性能优化**
- Redis 缓存降低重复实验的 API 成本
- 用于大规模假设检验的并行处理
- 自适应细化侧重于挑战示例

* *灵活配置**
- 带变量注入的基于模板的提示工程
- 针对特定领域任务的自定义标签提取
- 易于扩展的模块化架构

* *经过验证的结果**
- 与少数基线相比提高 8.97%
- 与纯文献方法相比提高 15.75%
- 80-84% 假设多样性（非冗余见解）
- 人类评估者报告显着的决策改进

## 核心功能

### 1. HypoGeniC：数据驱动的假设生成

仅通过迭代细化从观测数据生成假设。

* *过程：**
1. 使用小数据子集初始化以生成候选假设
2. 基于性能
3迭代地完善假设。用具有挑战性的示例中的新假设替换表现不佳的假设

* *最适合：**没有现有文献的探索性研究，新颖数据集中的模式发现

### 2. HypoRefine：文献和数据集成

通过代理将现有文献与经验数据协同结合框架.

* *流程：**
1. 从相关研究论文（通常是 10 篇论文）
2 中提取见解。从文献 
3 中生成基于理论的假设。从观察模式生成数据驱动的假设
4. 通过迭代改进完善两个假设库

* *最适合：**在已建立的理论基础上进行研究，验证或扩展现有理论

### 3.联合方法

将纯文献假设与框架输出机械地结合起来。

* *变体：**
- **文献∪ HypoGeniC**：将文献假设与数据驱动生成相结合
- **文献∪ HypoRefine**：将文献假设与集成方法相结合

* *最适合：**全面的假设覆盖，消除冗余，同时保持多样化的观点

## 安装

通过 pip 安装：
```bash
uv pip install hypogenic
```

* *可选依赖项：**
- **Redis 服务器**（端口 6832）：启用 LLM 响应缓存，以在迭代假设生成期间显着降低 API 成本
- **s2orc-doc2json**：在 HypoRefine 中处理文献 PDF 时需要工作流程
- **GROBID**：PDF 预处理所需（参见文献处理部分）

* *克隆示例数据集：**
```bash
# For HypoGeniC examples
git clone https://github.com/ChicagoHAI/HypoGeniC-datasets.git ./data

# For HypoRefine/Union examples
git clone https://github.com/ChicagoHAI/Hypothesis-agent-datasets.git ./data
```

## 数据集格式

数据集必须遵循具有特定命名约定的 HuggingFace 数据集格式：

* *必需文件：**
- `<TASK>_train.json`：训练数据
- `<TASK>_val.json`：验证数据 
- `<TASK>_test.json`：测试数据

* *JSON 中所需的密钥：**
- `text_features_1` 到 `text_features_n`：包含特征值的字符串列表
- `label`：包含真实标签的字符串列表

* *示例（标题点击预测）：**
```json
{
  "headline_1": [
    "What Up, Comet? You Just Got *PROBED*",
    "Scientists Made a Breakthrough in Quantum Computing"
  ],
  "headline_2": [
    "Scientists Everywhere Were Holding Their Breath Today. Here's Why.",
    "New Quantum Computer Achieves Milestone"
  ],
  "label": [
    "Headline 2 has more clicks than Headline 1",
    "Headline 1 has more clicks than Headline 2"
  ]
}
```

* *重要说明：**
- 所有列表必须具有相同的长度
- 标签格式必须匹配您的 `extract_label()` 函数输出格式
- 可以自定义功能键以匹配您的域（例如，`review_text`、`post_content` 等）

## 配置

E 每个任务需要一个 `config.yaml` 文件，指定：

* *必需元素：**
- 数据集路径（训练/验证/测试）
- 提示模板：
  - 观测生成
  - 批量假设生成
  - 假设推理
  - 相关性检查
  - 自适应方法（用于HypoRefine)

* *模板功能：**
- 用于动态变量注入的数据集占位符（例如，`${text_features_1}`、`${num_hypotheses}`）
- 用于特定域解析的自定义标签提取函数
- 基于角色的提示结构（系统、用户、助理）角色）

* *配置结构：**
```yaml
task_name: your_task_name

train_data_path: ./your_task_train.json
val_data_path: ./your_task_val.json
test_data_path: ./your_task_test.json

prompt_templates:
  # Extra keys for reusable prompt components
  observations: |
    Feature 1: ${text_features_1}
    Feature 2: ${text_features_2}
    Observation: ${label}
  
  # Required templates
  batched_generation:
    system: "Your system prompt here"
    user: "Your user prompt with ${num_hypotheses} placeholder"
  
  inference:
    system: "Your inference system prompt"
    user: "Your inference user prompt"
  
  # Optional templates for advanced features
  few_shot_baseline: {...}
  is_relevant: {...}
  adaptive_inference: {...}
  adaptive_selection: {...}
```

完整的示例配置参考`references/config_template.yaml`。

## 文献处理（HypoRefine/Union方法）

要使用基于文献的假设生成，您必须预处理 PDF 论文。

> **注意：** 以下命令在克隆的 [HypoGenic 存储库](https://github.com/ChicagoHAI/hypothesis- Generation)中运行，而不是从此技能目录中运行。

* *步骤 1：设置 GROBID**（第一次）仅）
```bash
bash ./modules/setup_grobid.sh
```

* *步骤 2：添加 PDF 文件**
将研究论文放入 `literature/YOUR_TASK_NAME/raw/`

* *步骤 3：处理 PDF**
```bash
# Start GROBID service
bash ./modules/run_grobid.sh

# Process PDFs for your task
cd examples
python pdf_preprocess.py --task_name YOUR_TASK_NAME
```

这会将 PDF 转换为结构化格式用于假设提取。未来版本将支持自动文献检索。

## CLI 用法

### 假设生成

```bash
hypogenic_generation --help
```

* *关键参数：**
- 任务配置文件路径
- 模型选择（基于API 或本地）
- 生成方法（HypoGeniC、HypoRefine 或 Union）
- 生成的假设数量
- 假设库的输出目录

### 假设推理

```bash
hypogenic_inference --help
```

* *关键参数：**
- 任务配置文件路径
- 假设库文件路径
- 测试数据集路径
- 推理方法（默认或多重假设）
- 结果的输出文件

## Python API 使用

对于编程控制和自定义工作流程，请直接在Python 中使用Hypogenic代码：

### 基本HypoGeniC生成

```python
from hypogenic import BaseTask

# Clone example datasets first
# git clone https://github.com/ChicagoHAI/HypoGeniC-datasets.git ./data

# Load your task with custom extract_label function
task = BaseTask(
    config_path="./data/your_task/config.yaml",
    extract_label=lambda text: extract_your_label(text)
)

# Generate hypotheses
task.generate_hypotheses(
    method="hypogenic",
    num_hypotheses=20,
    output_path="./output/hypotheses.json"
)

# Run inference
results = task.inference(
    hypothesis_bank="./output/hypotheses.json",
    test_data="./data/your_task/your_task_test.json"
)
```

### HypoRefine/Union方法

```python
# For literature-integrated approaches
# git clone https://github.com/ChicagoHAI/Hypothesis-agent-datasets.git ./data

# Generate with HypoRefine
task.generate_hypotheses(
    method="hyporefine",
    num_hypotheses=15,
    literature_path="./literature/your_task/",
    output_path="./output/"
)
# This generates 3 hypothesis banks:
# - HypoRefine (integrated approach)
# - Literature-only hypotheses
# - Literature∪HypoRefine (union)
```

### 多重假设Inference

```python
from examples.multi_hyp_inference import run_multi_hypothesis_inference

# Test multiple hypotheses simultaneously
results = run_multi_hypothesis_inference(
    config_path="./data/your_task/config.yaml",
    hypothesis_bank="./output/hypotheses.json",
    test_data="./data/your_task/your_task_test.json"
)
```

### 自定义标签提取

`extract_label()` 函数对于解析 LLM 输出至关重要。根据您的任务实现它：

```python
def extract_label(llm_output: str) -> str:
    """Extract predicted label from LLM inference text.
    
    Default behavior: searches for 'final answer:\s+(.*)' pattern.
    Customize for your domain-specific output format.
    """
    import re
    match = re.search(r'final answer:\s+(.*)', llm_output, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return llm_output.strip()
```

* *重要：**提取的标签必须与数据集中的 `label` 值的格式匹配，才能正确计算准确性。

## 工作流程示例

### 示例 1：数据驱动假设生成(HypoGeniC)

* *场景：**在没有先验理论框架的情况下检测人工智能生成的内容

* *步骤：**
1. 准备包含文本样本和标签（人类与人工智能生成）
2 的数据集。使用适当的提示模板
3创建`config.yaml`。运行假设生成：
 ```bash
 hyperogenic_ G​​eneration --config config.yaml --method hypogenic --num_hypotheses 20
 ```
4. 在测试集上运行推理：
 ```bash
 hyperogenic_inference --config config.yaml --hypotheses output/hypotheses.json --test_data data/test.json
 ```
5. 分析形式、语法精度和语气差异等模式的结果

### 示例 2：基于文献的假设检验 (HypoRefine)

* *场景：** 基于现有研究的酒店评论中的欺骗检测

* *步骤：**
1. 收集10篇关于语言欺骗线索的相关论文
2. 准备包含真实和欺诈评论的数据集
3. 配置`config.yaml`文献处理和数据生成模板
4. 运行 HypoRefine:
 ```bash
 hyperogenic_ G​​eneration --config config.yaml --methodhyporefine --papers papers/ --num_hypotheses 15
 ```
5. 测试假设，检查代词频率、细节特异性和其他语言模式
6. 比较基于文献和数据驱动的假设性能

### 示例3：综合假设覆盖率（联合方法）

* *场景：**精神压力检测最大化假设多样性

* *步骤：**
1. 从心理健康研究论文 
2 中生成文献假设。从社交媒体帖子生成数据驱动的假设
3. 运行 Union 方法进行合并和去重：
 ```bash
 hyperogenic_ G​​eneration --config config.yaml --method union --literature_hypotheses lit_hyp.json
 ```
4. 推理捕获理论结构（发布行为变化）和数据模式（情感语言转变）

## 性能优化

* *缓存：**启用Redis缓存以减少重复LLM调用的API成本和计算时间

* *并行处理：**利用多个工作人员进行大规模假设生成和测试

* *自适应细化：**使用具有挑战性的示例来迭代提高假设质量

## 预期结果

使用hypogenic的研究有证明：
- AI 内容检测任务的准确度提高了 14.19%
- 欺骗检测任务的准确度提高了 7.44%
- 80-84% 的假设对提供了独特的、非冗余的见解
- 跨多个研究领域的人类评估者给出了高有用性评级

## 故障排除

* *问题：**生成的假设太通用
* *解决方案：**优化`config.yaml`中的提示模板，以请求更具体、可测试的假设

* *问题：**推理性能较差
* *解决方案：**确保数据集有足够的训练示例，调整假设生成参数，或增加假设生成参数的数量假设

* *问题：**标签提取失败
* *解决方案：**为特定于域的输出解析实现自定义`extract_label()`函数

* *问题：**GROBID PDF处理失败
* *解决方案：**确保GROBID服务正在运行（来自克隆存储库的 `bash ./modules/run_grobid.sh`）和 PDF 是有效的研究论文

## 创建自定义任务

要将新任务或数据集添加到 Hypogenic：

### 步骤 1：准备数据集

按照所需格式创建三个 JSON 文件：
- `your_task_train.json`
- `your_task_val.json`
- `your_task_test.json`

E每个文件必须具有文本特征的键（`text_features_1`等）和`label`.

### 步骤2：创建配置.yaml

使用以下内容定义任务配置：
- 任务名称和数据集路径
- 用于观察、生成、推理的提示模板
- 可重用提示组件的任何额外键
- 占位符变量（例如，`${text_features_1}`、`${num_hypotheses}`）

### 步骤3：实施extract_label函数

创建一个自定义标签提取函数，用于解析您的域的LLM输出：

```python
from hypogenic import BaseTask

def extract_my_label(llm_output: str) -> str:
    """Custom label extraction for your task.
    
    Must return labels in same format as dataset 'label' field.
    """
    # Example: Extract from specific format
    if "Final prediction:" in llm_output:
        return llm_output.split("Final prediction:")[-1].strip()
    
    # Fallback to default pattern
    import re
    match = re.search(r'final answer:\s+(.*)', llm_output, re.IGNORECASE)
    return match.group(1).strip() if match else llm_output.strip()

# Use your custom task
task = BaseTask(
    config_path="./your_task/config.yaml",
    extract_label=extract_my_label
)
```

### 步骤4：（可选）处理文献

对于HypoRefine/Union方法：
1. 创建`literature/your_task_name/raw/`目录
2. 添加相关研究论文 PDFs
3. 运行 GROBID 预处理
4. 使用 `pdf_preprocess.py`

### 步骤 5：生成和测试

使用 CLI 或 Python API 运行假设生成和推理：

```bash
# CLI approach
hypogenic_generation --config your_task/config.yaml --method hypogenic --num_hypotheses 20
hypogenic_inference --config your_task/config.yaml --hypotheses output/hypotheses.json

# Or use Python API (see Python API Usage section)
```

## 存储库结构

了解存储库布局：

```
hypothesis-generation/
├── hypogenic/              # Core package code
├── hypogenic_cmd/          # CLI entry points
├── hypothesis_agent/       # HypoRefine agent framework
├── literature/            # Literature processing utilities
├── modules/               # GROBID and preprocessing modules
├── examples/              # Example scripts
│   ├── generation.py      # Basic HypoGeniC generation
│   ├── union_generation.py # HypoRefine/Union generation
│   ├── inference.py       # Single hypothesis inference
│   ├── multi_hyp_inference.py # Multiple hypothesis inference
│   └── pdf_preprocess.py  # Literature PDF processing
├── data/                  # Example datasets (clone separately)
├── tests/                 # Unit tests
└── IO_prompting/          # Prompt templates and experiments
```

* *关键目录：**
- **hypogenic/**：带有BaseTask和生成逻辑的主包
- **示例/**：常见工作流程的参考实现
- **文献/**：PDF处理和文献的工具提取
- **模块/**：外部工具集成（GROBID 等）

## 相关出版物

### HypoBench (2025)

Liu, H.、Huang, S.、Hu, J.、Zhou, Y. 和 Tan, C. (2025)。 HypoBench：迈向假设生成的系统性和原则性基准测试。 arXiv 预印本 arXiv:2504.11524.

- **论文：** https://arxiv.org/abs/2504.11524
- **描述：** 用于系统评估假设生成的基准框架方法

* *BibTeX：**
```bibtex
@misc{liu2025hypobenchsystematicprincipledbenchmarking,
      title={HypoBench: Towards Systematic and Principled Benchmarking for Hypothesis Generation}, 
      author={Haokun Liu and Sicong Huang and Jingyu Hu and Yangqiaoyu Zhou and Chenhao Tan},
      year={2025},
      eprint={2504.11524},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2504.11524}, 
}
```

### 文献遇见数据（2024）

Liu, H., Zhou, Y., Li, M., Yuan, C., & Tan, C. (2024)。文献与数据的结合：假设生成的协同方法。 arXiv 预印本 arXiv:2410.17309.

- **论文：** https://arxiv.org/abs/2410.17309
- **代码：** https://github.com/ChicagoHAI/hypothesis- Generation
- **描述：** 介绍 HypoRefine 并演示基于文献和数据驱动的假设的协同组合Generation

* *BibTeX：**
```bibtex
@misc{liu2024literaturemeetsdatasynergistic,
      title={Literature Meets Data: A Synergistic Approach to Hypothesis Generation}, 
      author={Haokun Liu and Yangqiaoyu Zhou and Mingxuan Li and Chenfei Yuan and Chenhao Tan},
      year={2024},
      eprint={2410.17309},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2410.17309}, 
}
```

### 大型语言模型的假设生成 (2024)

Zhou, Y., Liu, H., Srivastava, T., Mei, H., & Tan, C. (2024)。使用大型语言模型生成假设。 In Proceedings of EMNLP Workshop of NLP for Science.

- **论文：** https://aclanthology.org/2024.nlp4science-1.10/
- **描述：** 用于数据驱动假设的原始 HypoGeniC 框架Generation

* *BibTeX:**
```bibtex
@inproceedings{zhou2024hypothesisgenerationlargelanguage,
      title={Hypothesis Generation with Large Language Models}, 
      author={Yangqiaoyu Zhou and Haokun Liu and Tejes Srivastava and Hongyuan Mei and Chenhao Tan},
      booktitle = {Proceedings of EMNLP Workshop of NLP for Science},
      year={2024},
      url={https://aclanthology.org/2024.nlp4science-1.10/},
}
```

## 其他资源

### 官方链接

- **GitHub 存储库：** https://github.com/ChicagoHAI/hypothesis- Generation
- **PyPI 包：** https://pypi.org/project/hypogenic/
- **许可证：** MIT 许可证
- **问题和支持：** https://github.com/ChicagoHAI/hypothesis- Generation/issues

### 示例数据集

克隆这些存储库以供随时使用示例：

```bash
# HypoGeniC examples (data-driven only)
git clone https://github.com/ChicagoHAI/HypoGeniC-datasets.git ./data

# HypoRefine/Union examples (literature + data)
git clone https://github.com/ChicagoHAI/Hypothesis-agent-datasets.git ./data
```

### 社区与贡献

- **贡献者：** 7+ 活跃贡献者
- **星星：** GitHub 上 89+ 
- **主题：** 研究工具、可解释性、hypothesis-generation、科学发现、LLM-应用

有关贡献或问题，请访问 GitHub 存储库并检查问题页面。

## 本地资源

### 引用/

`config_template.yaml` - 包含所有必需的提示模板和参数的完整示例配置文件。这包括：
- 用于任务配置的完整YAML结构
- 所有方法的示例提示模板
- 占位符变量文档
- 基于角色的提示示例

### 脚本/

脚本目录可用于：
- 自定义数据准备实用程序
- 格式转换工具
- 分析和评估脚本
- 与外部工具集成

### asset/

Assets 目录可用于：
- 示例数据集和模板
- 示例假设银行
- 可视化输出
- 文档补充
