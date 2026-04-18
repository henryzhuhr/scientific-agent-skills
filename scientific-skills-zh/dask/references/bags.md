# Dask Bags

## 概述

Dask Bag 对通用 Python 对象实现了 `map`、`filter`、`fold` 和 `groupby` 等功能操作。它并行处理数据，同时通过 Python 迭代器保持较小的内存占用。 Bags 的功能相当于“PyToolz 的并行版本或 PySpark RDD 的 Pythonic 版本”。

## 核心概念

A Dask Bag 是跨分区分布的 Python 对象的集合：
- 每个分区包含通用 Python 对象
- 操作使用函数式编程模式
- 处理使用内存流/迭代器效率
- 非结构化或半结构化数据的理想选择

## 关键功能

### 函数操作
- `map`：转换每个元素
- `filter`：根据条件选择元素
- `fold`：通过组合减少元素功能
- `groupby`：按键对元素进行分组
- `pluck`：从记录中提取字段
- `flatten`：压平嵌套结构

### 用例
- 文本处理和日志分析
- JSON记录处理
- 非结构化数据上的ETL
- 结构化分析之前的数据清理

## 何时使用Dask Bags

* *何时使用Bag**：
- 处理需要灵活计算的一般Python 对象
- 数据不适合结构化数组或表格格式
- 处理文本、JSON 或自定义Python 对象
- 需要初始数据清理和ETL
- 内存高效流很重要

* *使用其他集合**：
- 数据是结构化的（使用DataFrames 代替）
- 数值计算（使用数组）相反）
- 操作需要复杂的groupby或shuffle（使用DataFrames）

* *关键建议**：使用Bag来清理和处理数据，然后将其转换为数组或DataFrame，然后再开始需要shuffle步骤的更复杂的操作。

## 重要限制

Bags 为了通用性而牺牲性能：
- 依赖多处理调度（而不是线程）
- 保持不可变（为更改创建新包）
- 比数组/DataFrame 等价物操作慢
- 处理 `groupby` 效率低下（在以下情况下使用 `foldby`）可能）
- 需要大量工作人员间通信的操作很慢

## 创建包

### 来自序列
```python
import dask.bag as db

# From Python list
bag = db.from_sequence([1, 2, 3, 4, 5], partition_size=2)

# From range
bag = db.from_sequence(range(10000), partition_size=1000)
```

### 来自文本文件
```python
# Single file
bag = db.read_text('data.txt')

# Multiple files with glob
bag = db.read_text('data/*.txt')

# With encoding
bag = db.read_text('data/*.txt', encoding='utf-8')

# Custom line processing
bag = db.read_text('logs/*.log', blocksize='64MB')
```

### 来自延迟对象
```python
import dask

@dask.delayed
def load_data(filename):
    with open(filename) as f:
        return [line.strip() for line in f]

files = ['file1.txt', 'file2.txt', 'file3.txt']
partitions = [load_data(f) for f in files]
bag = db.from_delayed(partitions)
```

### 来自自定义源
```python
# From any iterable-producing function
def read_json_files():
    import json
    for filename in glob.glob('data/*.json'):
        with open(filename) as f:
            yield json.load(f)

# Create bag from generator
bag = db.from_sequence(read_json_files(), partition_size=10)
```

## 常用操作

### 映射（变换）
```python
import dask.bag as db

bag = db.read_text('data/*.json')

# Parse JSON
import json
parsed = bag.map(json.loads)

# Extract field
values = parsed.map(lambda x: x['value'])

# Complex transformation
def process_record(record):
    return {
        'id': record['id'],
        'value': record['value'] * 2,
        'category': record.get('category', 'unknown')
    }

processed = parsed.map(process_record)
```

### Filter
```python
# Filter by condition
valid = parsed.filter(lambda x: x['status'] == 'valid')

# Multiple conditions
filtered = parsed.filter(lambda x: x['value'] > 100 and x['year'] == 2024)

# Filter with custom function
def is_valid_record(record):
    return record.get('status') == 'valid' and record.get('value') is not None

valid_records = parsed.filter(is_valid_record)
```

### Pluck（提取字段）
```python
# Extract single field
ids = parsed.pluck('id')

# Extract multiple fields (creates tuples)
key_pairs = parsed.pluck(['id', 'value'])
```

### Flatten
```python
# Flatten nested lists
nested = db.from_sequence([[1, 2], [3, 4], [5, 6]])
flat = nested.flatten()  # [1, 2, 3, 4, 5, 6]

# Flatten after map
bag = db.read_text('data/*.txt')
words = bag.map(str.split).flatten()  # All words from all files
```

### GroupBy （昂贵）
```python
# Group by key (requires shuffle)
grouped = parsed.groupby(lambda x: x['category'])

# Aggregate after grouping
counts = grouped.map(lambda key_items: (key_items[0], len(list(key_items[1]))))
result = counts.compute()
```

### FoldBy（聚合首选）
```python
# FoldBy is more efficient than groupby for aggregations
def add(acc, item):
    return acc + item['value']

def combine(acc1, acc2):
    return acc1 + acc2

# Sum values by category
sums = parsed.foldby(
    key='category',
    binop=add,
    initial=0,
    combine=combine
)

result = sums.compute()
```

### 减少
```python
# Count elements
count = bag.count().compute()

# Get all distinct values (requires memory)
distinct = bag.distinct().compute()

# Take first n elements
first_ten = bag.take(10)

# Fold/reduce
total = bag.fold(
    lambda acc, x: acc + x['value'],
    initial=0,
    combine=lambda a, b: a + b
).compute()
```

## 转换为其他集合

### 到DataFrame
```python
import dask.bag as db
import dask.dataframe as dd

# Bag of dictionaries
bag = db.read_text('data/*.json').map(json.loads)

# Convert to DataFrame
ddf = bag.to_dataframe()

# With explicit columns
ddf = bag.to_dataframe(meta={'id': int, 'value': float, 'category': str})
```

### 到列表/计算
```python
# Compute to Python list (loads all in memory)
result = bag.compute()

# Take sample
sample = bag.take(100)
```

## 常见模式

### JSON处理
```python
import dask.bag as db
import json

# Read and parse JSON files
bag = db.read_text('logs/*.json')
parsed = bag.map(json.loads)

# Filter valid records
valid = parsed.filter(lambda x: x.get('status') == 'success')

# Extract relevant fields
processed = valid.map(lambda x: {
    'user_id': x['user']['id'],
    'timestamp': x['timestamp'],
    'value': x['metrics']['value']
})

# Convert to DataFrame for analysis
ddf = processed.to_dataframe()

# Analyze
summary = ddf.groupby('user_id')['value'].mean().compute()
```

### 日志分析
```python
# Read log files
logs = db.read_text('logs/*.log')

# Parse log lines
def parse_log_line(line):
    parts = line.split(' ')
    return {
        'timestamp': parts[0],
        'level': parts[1],
        'message': ' '.join(parts[2:])
    }

parsed_logs = logs.map(parse_log_line)

# Filter errors
errors = parsed_logs.filter(lambda x: x['level'] == 'ERROR')

# Count by message pattern
error_counts = errors.foldby(
    key='message',
    binop=lambda acc, x: acc + 1,
    initial=0,
    combine=lambda a, b: a + b
)

result = error_counts.compute()
```

### 文本处理
```python
# Read text files
text = db.read_text('documents/*.txt')

# Split into words
words = text.map(str.lower).map(str.split).flatten()

# Count word frequencies
def increment(acc, word):
    return acc + 1

def combine_counts(a, b):
    return a + b

word_counts = words.foldby(
    key=lambda word: word,
    binop=increment,
    initial=0,
    combine=combine_counts
)

# Get top words
top_words = word_counts.compute()
sorted_words = sorted(top_words, key=lambda x: x[1], reverse=True)[:100]
```

### 数据清理Pipeline
```python
import dask.bag as db
import json

# Read raw data
raw = db.read_text('raw_data/*.json').map(json.loads)

# Validation function
def is_valid(record):
    required_fields = ['id', 'timestamp', 'value']
    return all(field in record for field in required_fields)

# Cleaning function
def clean_record(record):
    return {
        'id': int(record['id']),
        'timestamp': record['timestamp'],
        'value': float(record['value']),
        'category': record.get('category', 'unknown'),
        'tags': record.get('tags', [])
    }

# Pipeline
cleaned = (raw
    .filter(is_valid)
    .map(clean_record)
    .filter(lambda x: x['value'] > 0)
)

# Convert to DataFrame
ddf = cleaned.to_dataframe()

# Save cleaned data
ddf.to_parquet('cleaned_data/')
```

## 性能考虑因素

### 高效操作
- 映射、过滤、拔取：非常高效（流）
- 扁平化：高效
- 具有良好密钥分配的 FoldBy：合理
- Take和 head：高效（仅处理需要的分区）

### 昂贵的操作
- GroupBy：需要随机播放，可能会很慢
- Distinct：需要收集所有唯一值
- 需要完整数据实现的操作

### 优化技巧

* *1.使用 FoldBy 而不是 GroupBy**
```python
# Better: Use foldby for aggregations
result = bag.foldby(key='category', binop=add, initial=0, combine=sum)

# Worse: GroupBy then reduce
result = bag.groupby('category').map(lambda x: (x[0], sum(x[1])))
```

* *2。提前转换为 DataFrame**
```python
# For structured operations, convert to DataFrame
bag = db.read_text('data/*.json').map(json.loads)
bag = bag.filter(lambda x: x['status'] == 'valid')
ddf = bag.to_dataframe()  # Now use efficient DataFrame operations
```

* *3。控制分区大小**
```python
# Balance between too many and too few partitions
bag = db.read_text('data/*.txt', blocksize='64MB')  # Reasonable partition size
```

* *4。使用惰性求值**
```python
# Chain operations before computing
result = (bag
    .map(process1)
    .filter(condition)
    .map(process2)
    .compute()  # Single compute at the end
)
```

## 调试技巧

### 检查分区
```python
# Get number of partitions
print(bag.npartitions)

# Take sample
sample = bag.take(10)
print(sample)
```

### 验证小数据
```python
# Test logic on small subset
small_bag = db.from_sequence(sample_data, partition_size=10)
result = process_pipeline(small_bag).compute()
# Validate results, then scale
```

### 检查中间结果
```python
# Compute intermediate steps to debug
step1 = bag.map(parse).take(5)
print("After parsing:", step1)

step2 = bag.map(parse).filter(validate).take(5)
print("After filtering:", step2)
```

## 内存管理

Bags 设计用于内存高效处理：

```python
# Streaming processing - doesn't load all in memory
bag = db.read_text('huge_file.txt')  # Lazy
processed = bag.map(process_line)     # Still lazy
result = processed.compute()          # Processes in chunks
```

对于非常大的结果，避免计算到内存：

```python
# Don't compute huge results to memory
# result = bag.compute()  # Could overflow memory

# Instead, convert and save to disk
ddf = bag.to_dataframe()
ddf.to_parquet('output/')
```
