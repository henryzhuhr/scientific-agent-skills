# 模型加载和管理

## 概述

transformers 库提供灵活的模型加载，具有自动架构检测、设备管理和配置控制功能。

## 加载模型

### AutoModel 类

使用 AutoModel 类进行自动架构选择：

```python
from transformers import AutoModel, AutoModelForSequenceClassification, AutoModelForCausalLM

# Base model (no task head)
model = AutoModel.from_pretrained("bert-base-uncased")

# Sequence classification
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")

# Causal language modeling (GPT-style)
model = AutoModelForCausalLM.from_pretrained("gpt2")

# Masked language modeling (BERT-style)
from transformers import AutoModelForMaskedLM
model = AutoModelForMaskedLM.from_pretrained("bert-base-uncased")

# Sequence-to-sequence (T5-style)
from transformers import AutoModelForSeq2SeqLM
model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
```

### 常用 AutoModel 类

* *NLP 任务：**
- `AutoModelForSequenceClassification`：文本分类、情感分析
- `AutoModelForTokenClassification`：NER、POS 标记
- `AutoModelForQuestionAnswering`：提取 QA
- `AutoModelForCausalLM`：文本生成（GPT、Llama）
- `AutoModelForMaskedLM`：掩码语言建模（BERT）
- `AutoModelForSeq2SeqLM`：翻译、摘要（T5、BART）

* *视觉任务：**
- `AutoModelForImageClassification`：图像分类
- `AutoModelForObjectDetection`：目标检测
- `AutoModelForImageSegmentation`：图像分割

* *音频任务：**
- `AutoModelForAudioClassification`：音频分类
- `AutoModelForSpeechSeq2Seq`：语音识别

* *多模态：**
- `AutoModelForVision2Seq`：图像字幕、VQA

## 加载参数

### 基本参数

* *pretrained_model_name_or_path**：模型标识符或本地路径
```python
model = AutoModel.from_pretrained("bert-base-uncased")  # From Hub
model = AutoModel.from_pretrained("./local/model/path")  # From disk
```

* *num_labels**：分类的输出标签数量
```python
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=3
)
```

* *cache_dir**：自定义缓存位置
```python
model = AutoModel.from_pretrained("model-id", cache_dir="./my_cache")
```

### 设备管理

* *device_map**：大模型自动分配设备
```python
# Automatically distribute across GPUs and CPU
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    device_map="auto"
)

# Sequential placement
model = AutoModelForCausalLM.from_pretrained(
    "model-id",
    device_map="sequential"
)

# Custom device map
device_map = {
    "transformer.layers.0": 0,      # GPU 0
    "transformer.layers.1": 1,      # GPU 1
    "transformer.layers.2": "cpu",  # CPU
}
model = AutoModel.from_pretrained("model-id", device_map=device_map)
```

手动设备放置：
```python
import torch
model = AutoModel.from_pretrained("model-id")
model.to("cuda:0")  # Move to GPU 0
model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
```

### 精准控制

* *torch_dtype**：设置模型precision
```python
import torch

# Float16 (half precision)
model = AutoModel.from_pretrained("model-id", torch_dtype=torch.float16)

# BFloat16 (better range than float16)
model = AutoModel.from_pretrained("model-id", torch_dtype=torch.bfloat16)

# Auto (use original dtype)
model = AutoModel.from_pretrained("model-id", torch_dtype="auto")
```

### Attention Implement

* *attn_implementation**：选择注意力机制
```python
# Scaled Dot Product Attention (PyTorch 2.0+, fastest)
model = AutoModel.from_pretrained("model-id", attn_implementation="sdpa")

# Flash Attention 2 (requires flash-attn package)
model = AutoModel.from_pretrained("model-id", attn_implementation="flash_attention_2")

# Eager (default, most compatible)
model = AutoModel.from_pretrained("model-id", attn_implementation="eager")
```

### 内存优化

* *low_cpu_mem_usage**：在执行过程中减少CPU内存加载
```python
model = AutoModelForCausalLM.from_pretrained(
    "large-model-id",
    low_cpu_mem_usage=True,
    device_map="auto"
)
```

* *load_in_8bit**：8位量化（需要位和字节）
```python
model = AutoModelForCausalLM.from_pretrained(
    "model-id",
    load_in_8bit=True,
    device_map="auto"
)
```

* *load_in_4bit**：4位量化
```python
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

model = AutoModelForCausalLM.from_pretrained(
    "model-id",
    quantization_config=quantization_config,
    device_map="auto"
)
```

## 模型配置

#### 使用自定义配置加载

```python
from transformers import AutoConfig, AutoModel

# Load and modify config
config = AutoConfig.from_pretrained("bert-base-uncased")
config.hidden_dropout_prob = 0.2
config.attention_probs_dropout_prob = 0.2

# Initialize model with custom config
model = AutoModel.from_pretrained("bert-base-uncased", config=config)
```

#### 仅从配置初始化

```python
config = AutoConfig.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_config(config)  # Random weights
```

## 模型模式

### 训练与评估模式

默认情况下在评估模式下加载模型：

```python
model = AutoModel.from_pretrained("model-id")
print(model.training)  # False

# Switch to training mode
model.train()

# Switch back to evaluation mode
model.eval()
```

E 评估模式禁用 dropout 并使用批量规范统计。

## 保存模型

### 保存本地

```python
model.save_pretrained("./my_model")
```

这将创建：
- `config.json`：模型配置
- `pytorch_model.bin`或`model.safetensors`：模型权重

### 保存到拥抱面Hub

```python
model.push_to_hub("username/model-name")

# With custom commit message
model.push_to_hub("username/model-name", commit_message="Update model")

# Private repository
model.push_to_hub("username/model-name", private=True)
```

## 型号检查

### 参数计数

```python
# Total parameters
total_params = model.num_parameters()

# Trainable parameters only
trainable_params = model.num_parameters(only_trainable=True)

print(f"Total: {total_params:,}")
print(f"Trainable: {trainable_params:,}")
```

### 内存占用

```python
memory_bytes = model.get_memory_footprint()
memory_mb = memory_bytes / 1024**2
print(f"Memory: {memory_mb:.2f} MB")
```

### 型号架构

```python
print(model)  # Print full architecture

# Access specific components
print(model.config)
print(model.base_model)
```

## 前向传递

基本推理：

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("model-id")
model = AutoModelForSequenceClassification.from_pretrained("model-id")

inputs = tokenizer("Sample text", return_tensors="pt")
outputs = model(**inputs)

logits = outputs.logits
predictions = logits.argmax(dim=-1)
```

## 模型格式

### SafeTensors vs PyTorch

SafeTensors 速度更快，更安全：

```python
# Save as safetensors (recommended)
model.save_pretrained("./model", safe_serialization=True)

# Load either format automatically
model = AutoModel.from_pretrained("./model")
```

### ONNX Export

导出以优化推理：

```python
from transformers.onnx import export

# Export to ONNX
export(
    tokenizer=tokenizer,
    model=model,
    config=config,
    output=Path("model.onnx")
)
```

## 最佳实践

1. **使用 AutoModel 类**：自动架构检测
2. **明确指定dtype**：控制精度和内存
3. **使用device_map="auto"**：适用于大型型号
4. **启用low_cpu_mem_usage**：加载大型模型
5时。 **使用安全张量格式**：更快、更安全的序列化
6. **检查 model.training**：确保任务
7 的模式正确。 **考虑量化**：适用于资源受限设备
8上的部署。 **本地缓存模型**：设置 TRANSFORMERS_CACHE 环境变量

## 常见问题

* *CUDA内存不足：**
```python
# Use smaller precision
model = AutoModel.from_pretrained("model-id", torch_dtype=torch.float16)

# Or use quantization
model = AutoModel.from_pretrained("model-id", load_in_8bit=True)

# Or use CPU
model = AutoModel.from_pretrained("model-id", device_map="cpu")
```

* *加载缓慢：**
```python
# Enable low CPU memory mode
model = AutoModel.from_pretrained("model-id", low_cpu_mem_usage=True)
```

* *模型不可用发现：**
```python
# Verify model ID on hub.co
# Check authentication for private models
from huggingface_hub import login
login()
```
