# Tokenizers

## 概述

Tokenizers 将文本转换为模型可以处理的数字表示（标记）。它们处理特殊标记、填充、截断和注意掩码。

## 加载标记器

### AutoTokenizer

自动为模型加载正确的标记器：

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
```

从本地加载路径：
```python
tokenizer = AutoTokenizer.from_pretrained("./local/tokenizer/path")
```

## 基本标记化

### 编码文本

```python
# Simple encoding
text = "Hello, how are you?"
tokens = tokenizer.encode(text)
print(tokens)  # [101, 7592, 1010, 2129, 2024, 2017, 1029, 102]

# With text tokenization
tokens = tokenizer.tokenize(text)
print(tokens)  # ['hello', ',', 'how', 'are', 'you', '?']
```

### 解码标记

```python
token_ids = [101, 7592, 1010, 2129, 2024, 2017, 1029, 102]
text = tokenizer.decode(token_ids)
print(text)  # "hello, how are you?"

# Skip special tokens
text = tokenizer.decode(token_ids, skip_special_tokens=True)
print(text)  # "hello, how are you?"
```

## `__call__`方法

主要分词接口：

```python
# Single text
inputs = tokenizer("Hello, how are you?")

# Returns dictionary with input_ids, attention_mask
print(inputs)
# {
#   'input_ids': [101, 7592, 1010, 2129, 2024, 2017, 1029, 102],
#   'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1]
# }
```

多文本：
```python
texts = ["Hello", "How are you?"]
inputs = tokenizer(texts, padding=True, truncation=True)
```

## 关键参数

### 返回Tensors

* *return_tensors**：输出格式("pt", "tf", "np")
```python
# PyTorch tensors
inputs = tokenizer("text", return_tensors="pt")

# TensorFlow tensors
inputs = tokenizer("text", return_tensors="tf")

# NumPy arrays
inputs = tokenizer("text", return_tensors="np")
```

### Padding

* *padding**：将序列填充到相同长度
```python
# Pad to longest sequence in batch
inputs = tokenizer(texts, padding=True)

# Pad to specific length
inputs = tokenizer(texts, padding="max_length", max_length=128)

# No padding
inputs = tokenizer(texts, padding=False)
```

* *pad_to_multiple_of**：填充到指定的多个value
```python
inputs = tokenizer(texts, padding=True, pad_to_multiple_of=8)
```

### 截断

* *截断**：限制序列长度
```python
# Truncate to max_length
inputs = tokenizer(text, truncation=True, max_length=512)

# Truncate first sequence in pairs
inputs = tokenizer(text1, text2, truncation="only_first")

# Truncate second sequence
inputs = tokenizer(text1, text2, truncation="only_second")

# Truncate longest first (default for pairs)
inputs = tokenizer(text1, text2, truncation="longest_first", max_length=512)
```

### 最大长度

* *max_length**：最大序列length
```python
inputs = tokenizer(text, max_length=512, truncation=True)
```

### 附加输出

* *return_attention_mask**：包括注意掩码（默认 True）
```python
inputs = tokenizer(text, return_attention_mask=True)
```

* *return_token_type_ids**：句子的段 ID pairs
```python
inputs = tokenizer(text1, text2, return_token_type_ids=True)
```

* *return_offsets_mapping**：字符位置映射（仅限快速分词器）
```python
inputs = tokenizer(text, return_offsets_mapping=True)
```

* *return_length**：包括序列长度
```python
inputs = tokenizer(texts, padding=True, return_length=True)
```

## 特殊令牌

### 预定义特殊令牌

访问特殊令牌：
```python
print(tokenizer.cls_token)      # [CLS] or <s>
print(tokenizer.sep_token)      # [SEP] or </s>
print(tokenizer.pad_token)      # [PAD]
print(tokenizer.unk_token)      # [UNK]
print(tokenizer.mask_token)     # [MASK]
print(tokenizer.eos_token)      # End of sequence
print(tokenizer.bos_token)      # Beginning of sequence

# Get IDs
print(tokenizer.cls_token_id)
print(tokenizer.sep_token_id)
```

### 添加特殊令牌

手动control:
```python
# Automatically add special tokens (default True)
inputs = tokenizer(text, add_special_tokens=True)

# Skip special tokens
inputs = tokenizer(text, add_special_tokens=False)
```

### 自定义特殊标记

```python
special_tokens_dict = {
    "additional_special_tokens": ["<CUSTOM>", "<SPECIAL>"]
}

num_added = tokenizer.add_special_tokens(special_tokens_dict)
print(f"Added {num_added} tokens")

# Resize model embeddings after adding tokens
model.resize_token_embeddings(len(tokenizer))
```

## 句子对

Tokenize 文本对:

```python
text1 = "What is the capital of France?"
text2 = "Paris is the capital of France."

# Automatically handles separation
inputs = tokenizer(text1, text2, padding=True, truncation=True)

# Results in: [CLS] text1 [SEP] text2 [SEP]
```

## 批量编码

处理多个文本：

```python
texts = ["First text", "Second text", "Third text"]

# Basic batch encoding
batch = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

# Access individual encodings
for i in range(len(texts)):
    input_ids = batch["input_ids"][i]
    attention_mask = batch["attention_mask"][i]
```

## 快速分词器

使用基于Rust的分词器提高速度：

```python
from transformers import AutoTokenizer

# Automatically loads Fast version if available
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Check if Fast
print(tokenizer.is_fast)  # True

# Force Fast tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased", use_fast=True)

# Force slow (Python) tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased", use_fast=False)
```

### 快速分词器功能

* *偏移映射** （字符位置）：
```python
inputs = tokenizer("Hello world", return_offsets_mapping=True)
print(inputs["offset_mapping"])
# [(0, 0), (0, 5), (6, 11), (0, 0)]  # [CLS], "Hello", "world", [SEP]
```

* *标记到单词映射**：
```python
encoding = tokenizer("Hello world")
word_ids = encoding.word_ids()
print(word_ids)  # [None, 0, 1, None]  # [CLS]=None, "Hello"=0, "world"=1, [SEP]=None
```

## 保存分词器

本地保存：
```python
tokenizer.save_pretrained("./my_tokenizer")
```

推送到集线器：
```python
tokenizer.push_to_hub("username/my-tokenizer")
```

## 高级用法

### 词汇

访问词汇：
```python
vocab = tokenizer.get_vocab()
vocab_size = len(vocab)

# Get token for ID
token = tokenizer.convert_ids_to_tokens(100)

# Get ID for token
token_id = tokenizer.convert_tokens_to_ids("hello")
```

### 编码详细信息

获取详细编码信息：

```python
encoding = tokenizer("Hello world", return_tensors="pt")

# Original methods still available
tokens = encoding.tokens()
word_ids = encoding.word_ids()
sequence_ids = encoding.sequence_ids()
```

### 自定义预处理

自定义行为的子类：

```python
class CustomTokenizer(AutoTokenizer):
    def __call__(self, text, **kwargs):
        # Custom preprocessing
        text = text.lower().strip()
        return super().__call__(text, **kwargs)
```

## 聊天模板

用于对话型号：

```python
messages = [
    {"role": "system", "content": "You are helpful."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "How are you?"}
]

# Apply chat template
text = tokenizer.apply_chat_template(messages, tokenize=False)
print(text)

# Tokenize directly
inputs = tokenizer.apply_chat_template(messages, tokenize=True, return_tensors="pt")
```

## 常见模式

### 模式1：简单文本分类

```python
texts = ["I love this!", "I hate this!"]
labels = [1, 0]

inputs = tokenizer(
    texts,
    padding=True,
    truncation=True,
    max_length=512,
    return_tensors="pt"
)

# Use with model
outputs = model(**inputs, labels=torch.tensor(labels))
```

### 模式2：问题回答

```python
question = "What is the capital?"
context = "Paris is the capital of France."

inputs = tokenizer(
    question,
    context,
    padding=True,
    truncation=True,
    max_length=384,
    return_tensors="pt"
)
```

### 模式 3：文本生成

```python
prompt = "Once upon a time"

inputs = tokenizer(prompt, return_tensors="pt")

# Generate
outputs = model.generate(
    inputs["input_ids"],
    max_new_tokens=50,
    pad_token_id=tokenizer.eos_token_id
)

# Decode
text = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### 模式 4：数据集标记化

```python
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=512
    )

# Apply to dataset
tokenized_dataset = dataset.map(tokenize_function, batched=True)
```

## 最佳做法

1. **始终指定 return_tensors**：对于模型输入
2. **使用填充和截断**：用于批处理
3. **显式设置 max_length**：防止内存问题
4. **使用快速分词器**：适用于 speed
5 时。 **处理 pad_token**：如果生成 
6 为 None，则设置为 eos_token。 **添加特殊令牌**：保持启用状态（默认），除非有特殊原因
7. **调整嵌入大小**：添加自定义标记
8后。 **使用skip_special_tokens解码**：为了更清晰的输出
9. **使用批处理**：为了提高数据集
10的效率。 **将标记生成器与模型一起保存**：确保兼容性

## 常见问题

* *未设置填充标记：**
```python
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
```

* *序列太长：**
```python
# Enable truncation
inputs = tokenizer(text, truncation=True, max_length=512)
```

* *不匹配词汇：**
```python
# Always load tokenizer and model from same checkpoint
tokenizer = AutoTokenizer.from_pretrained("model-id")
model = AutoModel.from_pretrained("model-id")
```

* *注意掩码问题：**
```python
# Ensure attention_mask is passed
outputs = model(
    input_ids=inputs["input_ids"],
    attention_mask=inputs["attention_mask"]
)
```
