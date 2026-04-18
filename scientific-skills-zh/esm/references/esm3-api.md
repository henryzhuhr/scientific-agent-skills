# ESM3 API 参考

## 概述

ESM3 是一种前沿多模态生成语言模型，可对蛋白质的序列、结构和功能进行推理。它使用迭代掩码语言建模来同时生成这三种模式。

## 模型架构

* *ESM3 系列模型：**

|型号 ID |参数|可用性 |最适合 |
|----------|------------|----------------|----------|
| `esm3-sm-open-v1` | 1.4B|开放重量（局部）|开发、测试、学习|
| `esm3-medium-2024-08` | 7B|仅限 Forge API |生产，质量/速度均衡|
| `esm3-large-2024-03` | 98B | 98B仅限 Forge API |最高品质，研究 |
| `esm3-medium-multimer-2024-09` | 7B|仅限 Forge API |蛋白质复合物（实验）|

* *主要特点：**
- 跨序列、结构和功能的同时推理
- 步骤数量可控的迭代生成
- 支持跨模式的部分提示
- 复杂设计的思想链生成
- 用于生成多样性的温度控制

## 核心API组件

### ESMProtein类

代表具有可选序列、结构和功能信息的蛋白质的中心数据结构。

* *构造函数：**

```python
from esm.sdk.api import ESMProtein

protein = ESMProtein(
    sequence="MPRTKEINDAGLIVHSP",           # Amino acid sequence (optional)
    coordinates=coordinates_array,          # 3D structure (optional)
    function_annotations=[...],             # Function labels (optional)
    secondary_structure="HHHEEEECCC",       # SS annotations (optional)
    sasa=sasa_array                        # Solvent accessibility (optional)
)
```

* *密钥方法：**

```python
# Load from PDB file
protein = ESMProtein.from_pdb("protein.pdb")

# Export to PDB format
pdb_string = protein.to_pdb()

# Save to file
with open("output.pdb", "w") as f:
    f.write(protein.to_pdb())
```

* *屏蔽约定：**

使用`_`（下划线）表示生成的屏蔽位置：

```python
# Mask positions 5-10 for generation
protein = ESMProtein(sequence="MPRT______AGLIVHSP")

# Fully masked sequence (generate from scratch)
protein = ESMProtein(sequence="_" * 200)

# Partial structure (some coordinates None)
protein = ESMProtein(
    sequence="MPRTKEIND",
    coordinates=partial_coords  # Some positions can be None
)
```

### GenerationConfig Class

控制生成行为和参数.

* *基本配置：**

```python
from esm.sdk.api import GenerationConfig

config = GenerationConfig(
    track="sequence",              # Track to generate: "sequence", "structure", or "function"
    num_steps=8,                  # Number of demasking steps
    temperature=0.7,              # Sampling temperature (0.0-1.0)
    top_p=None,                   # Nucleus sampling threshold
    condition_on_coordinates_only=False  # For structure conditioning
)
```

* *参数详细信息：**

- **track**：生成哪种模态
  - `"sequence"`：生成氨基酸序列
  - `"structure"`：生成3D坐标
  - `"function"`：生成函数注释

- **num_steps**：迭代解掩码步骤数
  - 较高 = 较慢但可能质量更好
  - 典型范围：8-100，具体取决于序列长度
  - 对于完整序列生成：大约序列长度/2

  - **温度**：控制随机性
  - 0.0：完全确定性（贪婪）解码）
  - 0.5-0.7：平衡探索
  - 1.0：最大多样性
  - 较高的值会增加新颖性，但可能会降低质量

- **top_p**：核采样参数
  - 限制采样到最高概率质量
  - 值：0.0-1.0 （例如，0.9 = 来自顶部 90% 概率质量的样本）
  - 用于受控多样性，无需极端采样

- **condition_on_coordinates_only**：结构调节模式
  - `True`：仅在主干坐标上进行条件（忽略序列）
  - 用于反向折叠任务

### ESM3InferenceClient Interface

本地和远程推理的统一接口。

* *本地模型加载：**

```python
from esm.models.esm3 import ESM3

# Load with automatic device placement
model = ESM3.from_pretrained("esm3-sm-open-v1").to("cuda")

# Or explicitly specify device
model = ESM3.from_pretrained("esm3-sm-open-v1").to("cpu")
```

* *生成方法：**

```python
# Basic generation
protein_output = model.generate(protein_input, config)

# With explicit track specification
protein_output = model.generate(
    protein_input,
    GenerationConfig(track="sequence", num_steps=16, temperature=0.6)
)
```

* *正向传递（高级）：**

```python
# Get raw model logits for custom sampling
protein_tensor = model.encode(protein)
output = model.forward(protein_tensor)
logits = model.decode(output)
```

## 常用模式

### 1. 序列完成

填充蛋白质的屏蔽区域序列：

```python
# Define partial sequence
protein = ESMProtein(sequence="MPRTK____LIVHSP____END")

# Generate missing positions
config = GenerationConfig(track="sequence", num_steps=12, temperature=0.5)
completed = model.generate(protein, config)

print(f"Original:  {protein.sequence}")
print(f"Completed: {completed.sequence}")
```

### 2. 结构预测

根据序列预测 3D 结构：

```python
# Input: sequence only
protein = ESMProtein(sequence="MPRTKEINDAGLIVHSPQWFYK")

# Generate structure
config = GenerationConfig(track="structure", num_steps=len(protein.sequence))
protein_with_structure = model.generate(protein, config)

# Save as PDB
with open("predicted_structure.pdb", "w") as f:
    f.write(protein_with_structure.to_pdb())
```

### 3. 反向折叠

为目标设计序列结构：

```python
# Load target structure
target = ESMProtein.from_pdb("target.pdb")

# Remove sequence, keep structure
target.sequence = None

# Generate sequence that folds to this structure
config = GenerationConfig(
    track="sequence",
    num_steps=50,
    temperature=0.7,
    condition_on_coordinates_only=True
)
designed = model.generate(target, config)

print(f"Designed sequence: {designed.sequence}")
```

### 4.功能条件生成

生成特定功能的蛋白：

```python
from esm.sdk.api import FunctionAnnotation

# Specify desired function
protein = ESMProtein(
    sequence="_" * 150,
    function_annotations=[
        FunctionAnnotation(
            label="enzymatic_activity",
            start=30,
            end=90
        )
    ]
)

# Generate sequence with this function
config = GenerationConfig(track="sequence", num_steps=75, temperature=0.6)
functional_protein = model.generate(protein, config)
```

### 5.多轨迹生成（Chain-of-Thought）

迭代生成跨多个轨道：

```python
# Start with partial sequence
protein = ESMProtein(sequence="MPRT" + "_" * 100)

# Step 1: Complete sequence
protein = model.generate(
    protein,
    GenerationConfig(track="sequence", num_steps=50, temperature=0.6)
)

# Step 2: Predict structure for completed sequence
protein = model.generate(
    protein,
    GenerationConfig(track="structure", num_steps=50)
)

# Step 3: Predict function
protein = model.generate(
    protein,
    GenerationConfig(track="function", num_steps=20)
)

print(f"Final sequence: {protein.sequence}")
print(f"Functions: {protein.function_annotations}")
```

### 6. 变体生成

生成蛋白质的多个变体：

```python
import numpy as np

base_sequence = "MPRTKEINDAGLIVHSPQWFYK"
variants = []

for i in range(10):
    # Mask random positions
    seq_list = list(base_sequence)
    mask_indices = np.random.choice(len(seq_list), size=5, replace=False)
    for idx in mask_indices:
        seq_list[idx] = '_'

    protein = ESMProtein(sequence=''.join(seq_list))

    # Generate variant
    variant = model.generate(
        protein,
        GenerationConfig(track="sequence", num_steps=8, temperature=0.8)
    )
    variants.append(variant.sequence)

print(f"Generated {len(variants)} variants")
```

## 高级主题

### 温度调度

期间改变温度为了更好的控制生成：

```python
def generate_with_temperature_schedule(model, protein, temperatures):
    """Generate with decreasing temperature for annealing."""
    current = protein
    steps_per_temp = 10

    for temp in temperatures:
        config = GenerationConfig(
            track="sequence",
            num_steps=steps_per_temp,
            temperature=temp
        )
        current = model.generate(current, config)

    return current

# Example: Start diverse, end deterministic
result = generate_with_temperature_schedule(
    model,
    protein,
    temperatures=[1.0, 0.8, 0.6, 0.4, 0.2]
)
```

### 约束生成

在生成过程中保留特定区域：

```python
# Keep active site residues fixed
def mask_except_active_site(sequence, active_site_positions):
    """Mask everything except specified positions."""
    seq_list = ['_'] * len(sequence)
    for pos in active_site_positions:
        seq_list[pos] = sequence[pos]
    return ''.join(seq_list)

# Define active site
active_site = [23, 24, 25, 45, 46, 89]
constrained_seq = mask_except_active_site(original_sequence, active_site)

protein = ESMProtein(sequence=constrained_seq)
result = model.generate(protein, GenerationConfig(track="sequence", num_steps=50))
```

### 二级结构条件

在生成中使用二级结构信息：

```python
# Define secondary structure (H=helix, E=sheet, C=coil)
protein = ESMProtein(
    sequence="_" * 80,
    secondary_structure="CCHHHHHHHEEEEECCCHHHHHHCC" + "C" * 55
)

# Generate sequence with this structure
result = model.generate(
    protein,
    GenerationConfig(track="sequence", num_steps=40, temperature=0.6)
)
```

## 性能优化

### 内存管理

用于大型蛋白质或批量处理：

```python
import torch

# Clear CUDA cache between generations
torch.cuda.empty_cache()

# Use half precision for memory efficiency
model = ESM3.from_pretrained("esm3-sm-open-v1").to("cuda").half()

# Process in chunks for very long sequences
def chunk_generate(model, long_sequence, chunk_size=500):
    chunks = [long_sequence[i:i+chunk_size]
              for i in range(0, len(long_sequence), chunk_size)]
    results = []

    for chunk in chunks:
        protein = ESMProtein(sequence=chunk)
        result = model.generate(protein, GenerationConfig(track="sequence"))
        results.append(result.sequence)

    return ''.join(results)
```

### 批量处理提示

处理多个蛋白质时：

1. 按序列长度排序以实现高效批处理
2. 对相似长度的序列使用填充
3. 可用时在 GPU 上进行处理 
4. 为长时间运行的作业实施检查点
5. 使用Forge API进行大规模处理（参见`forge-api.md`）

## 错误处理

```python
try:
    protein = model.generate(protein_input, config)
except ValueError as e:
    print(f"Invalid input: {e}")
    # Handle invalid sequence or structure
except RuntimeError as e:
    print(f"Generation failed: {e}")
    # Handle model errors
except torch.cuda.OutOfMemoryError:
    print("GPU out of memory - try smaller model or CPU")
    # Fallback to CPU or smaller model
```

## 模型特定注意事项

* *esm3-sm-open-v1:**
- 适合开发和测试
- 较低质量优于较大模型
- 在消费类 GPU 上快速推理
- 开放权重允许微调

* *esm3-medium-2024-08:**
- 生产质量
- 速度和准确性的良好平衡
- 需要 Forge API access
- 推荐用于大多数应用

* *esm3-large-2024-03:**
- 最先进的质量
- 最慢的推理
- 用于关键应用
- 最适合新颖的蛋白质设计

## 引用

如果在研究中使用ESM3，引用：

```
Hayes, T. et al. (2025). Simulating 500 million years of evolution with a language model.
Science. DOI: 10.1126/science.ads0018
```
