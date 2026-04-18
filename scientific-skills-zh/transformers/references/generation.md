# 文本生成

## 概述

使用 `generate()` 方法使用语言模型生成文本。通过生成策略和参数控制输出质量和风格。

## 基本生成

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Tokenize input
inputs = tokenizer("Once upon a time", return_tensors="pt")

# Generate
outputs = model.generate(**inputs, max_new_tokens=50)

# Decode
text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(text)
```

## 生成策略

### 贪心解码

在每一步选择最高概率token（确定性）：

```python
outputs = model.generate(
    **inputs,
    max_new_tokens=50,
    do_sample=False  # Greedy decoding (default)
)
```

* *使用用于**：事实文本、翻译，需要确定性的地方。

### 采样

从概率分布中随机采样：

```python
outputs = model.generate(
    **inputs,
    max_new_tokens=50,
    do_sample=True,
    temperature=0.7,
    top_k=50,
    top_p=0.95
)
```

* *用于**：创意写作、多样化输出、开放式生成。

### Beam Search

探索并行多个假设：

```python
outputs = model.generate(
    **inputs,
    max_new_tokens=50,
    num_beams=5,
    early_stopping=True
)
```

* *用于**：翻译、摘要，质量至关重要。

### 对比搜索

平衡质量和多样性：

```python
outputs = model.generate(
    **inputs,
    max_new_tokens=50,
    penalty_alpha=0.6,
    top_k=4
)
```

* *用于**：长格式

## 关键参数

### 长度控制

* *max_new_tokens**：生成的最大令牌
```python
max_new_tokens=100  # Generate up to 100 new tokens
```

* *max_length**：最大总长度（输入+输出）
```python
max_length=512  # Total sequence length
```

* *min_new_tokens**：生成的最小令牌
```python
min_new_tokens=50  # Force at least 50 tokens
```

* *min_length**：最小总长度
```python
min_length=100
```

### 温度

控制随机性（仅在采样时）：

```python
temperature=1.0   # Default, balanced
temperature=0.7   # More focused, less random
temperature=1.5   # More creative, more random
```

较低温度→更具确定性
较高温度→更具随机性

### Top-K采样

仅考虑最有可能的top K tokens：

```python
do_sample=True
top_k=50  # Sample from top 50 tokens
```

* *常用值**：平衡输出40-100，集中输出10-20。

### Top-P（Nucleus）采样

考虑累积概率≥的token P:

```python
do_sample=True
top_p=0.95  # Sample from smallest set with 95% cumulative probability
```

* *常用值**：平衡为 0.9-0.95，专注为 0.7-0.85。

### 重复罚分

Discourage重复：

```python
repetition_penalty=1.2  # Penalize repeated tokens
```

* *值**：1.0 = 无惩罚，1.2-1.5 = 中等，2.0+ = 强烈惩罚。

### 波束搜索参数

* *num_beams**：光束数量
```python
num_beams=5  # Keep 5 hypotheses
```

* *early_stopping**：当num_beams句子完成时停止
```python
early_stopping=True
```

* *no_repeat_ngram_size**：防止n-gram重复
```python
no_repeat_ngram_size=3  # Don't repeat any 3-gram
```

### 输出控制

* *num_return_sequences**：生成多个输出
```python
outputs = model.generate(
    **inputs,
    max_new_tokens=50,
    num_beams=5,
    num_return_sequences=3  # Return 3 different sequences
)
```

* *pad_token_id**：指定填充token
```python
pad_token_id=tokenizer.eos_token_id
```

* *eos_token_id**：在特定token处停止生成
```python
eos_token_id=tokenizer.eos_token_id
```

## 高级功能

### 批量生成

生成多个提示：

```python
prompts = ["Hello, my name is", "Once upon a time"]
inputs = tokenizer(prompts, return_tensors="pt", padding=True)

outputs = model.generate(**inputs, max_new_tokens=50)

for i, output in enumerate(outputs):
    text = tokenizer.decode(output, skip_special_tokens=True)
    print(f"Prompt {i}: {text}\n")
```

### 流生成

生成的流令牌：

```python
from transformers import TextIteratorStreamer
from threading import Thread

streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True)

generation_kwargs = dict(
    inputs,
    streamer=streamer,
    max_new_tokens=100
)

thread = Thread(target=model.generate, kwargs=generation_kwargs)
thread.start()

for text in streamer:
    print(text, end="", flush=True)

thread.join()
```

### 约束生成

强制特定令牌序列：

```python
# Force generation to start with specific tokens
force_words = ["Paris", "France"]
force_words_ids = [tokenizer.encode(word, add_special_tokens=False) for word in force_words]

outputs = model.generate(
    **inputs,
    force_words_ids=force_words_ids,
    num_beams=5
)
```

### 指导和控制

* *防止坏词：**
```python
bad_words = ["offensive", "inappropriate"]
bad_words_ids = [tokenizer.encode(word, add_special_tokens=False) for word in bad_words]

outputs = model.generate(
    **inputs,
    bad_words_ids=bad_words_ids
)
```

### 生成配置

保存并重用生成参数：

```python
from transformers import GenerationConfig

# Create config
generation_config = GenerationConfig(
    max_new_tokens=100,
    temperature=0.7,
    top_k=50,
    top_p=0.95,
    do_sample=True
)

# Save
generation_config.save_pretrained("./my_generation_config")

# Load and use
generation_config = GenerationConfig.from_pretrained("./my_generation_config")
outputs = model.generate(**inputs, generation_config=generation_config)
```

## 模型特定生成

### 聊天模型

使用聊天模板：

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]

input_text = tokenizer.apply_chat_template(messages, tokenize=False)
inputs = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(**inputs, max_new_tokens=100)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### 编码器-解码器模型

For T5、BART、等：

```python
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
tokenizer = AutoTokenizer.from_pretrained("t5-small")

# T5 uses task prefixes
input_text = "translate English to French: Hello, how are you?"
inputs = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(**inputs, max_new_tokens=50)
translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

## 优化

### 缓存

启用KV缓存以加快生成速度：

```python
outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    use_cache=True  # Default, faster generation
)
```

### 静态缓存

用于固定序列长度：

```python
from transformers import StaticCache

cache = StaticCache(model.config, max_batch_size=1, max_cache_len=1024, device="cuda")

outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    past_key_values=cache
)
```

### 注意力实现

使用 Flash 注意力提高速度：

```python
model = AutoModelForCausalLM.from_pretrained(
    "model-id",
    attn_implementation="flash_attention_2"
)
```

## 生成食谱

### 创意写入

```python
outputs = model.generate(
    **inputs,
    max_new_tokens=200,
    do_sample=True,
    temperature=0.8,
    top_k=50,
    top_p=0.95,
    repetition_penalty=1.2
)
```

### 事实生成

```python
outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    do_sample=False,  # Greedy
    repetition_penalty=1.1
)
```

### 多样化输出

```python
outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    num_beams=5,
    num_return_sequences=5,
    temperature=1.5,
    do_sample=True
)
```

### 长格式生成

```python
outputs = model.generate(
    **inputs,
    max_new_tokens=1000,
    penalty_alpha=0.6,  # Contrastive search
    top_k=4,
    repetition_penalty=1.2
)
```

### 翻译/总结

```python
outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    num_beams=5,
    early_stopping=True,
    no_repeat_ngram_size=3
)
```

## 常见问题

* *重复输出：**
- 增加repetition_penalty (1.2-1.5)
- 使用 no_repeat_ngram_size (2-3)
- 尝试对比搜索
- 较低温度

* *质量差：**
- 使用波束搜索 (num_beams=5)
- 较低温度
- 调整top_k/top_p

* *太确定性：**
- 启用采样(do_sample=True)
- 增加温度(0.7-1.0)
- 调整top_k/top_p

* *缓慢生成：**
- 减少批量大小
- 启用use_cache=True
- 使用Flash Attention
- 减少max_new_tokens

## 最佳实践

1. **从默认值开始**：然后根据输出
2进行调整。 **使用适当的策略**：贪图事实，采样创意
3. **设置 max_new_tokens**：避免不必要的长生成 
4. **启用缓存**：为了更快的顺序生成
5. **调整温度**：对采样最有影响的参数
6. **仔细使用波束搜索**：速度较慢但质量更高
7. **测试不同的种子**：为了保证采样 
8 的再现性。 **监控内存**：大光束使用大量内存
