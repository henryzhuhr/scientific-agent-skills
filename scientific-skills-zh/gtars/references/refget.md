# 参考序列管理

refget模块处理参考序列检索和摘要计算，遵循refget协议进行序列识别。

## RefgetStore

RefgetStore管理参考序列及其摘要：

```python
import gtars

# Create RefgetStore
store = gtars.RefgetStore()

# Add sequence
store.add_sequence("chr1", sequence_data)

# Retrieve sequence
seq = store.get_sequence("chr1")

# Get sequence digest
digest = store.get_digest("chr1")
```

## Sequence Digests

计算和验证序列摘要：

```python
# Compute digest for sequence
from gtars.refget import compute_digest

digest = compute_digest(sequence_data)

# Verify digest matches
is_valid = store.verify_digest("chr1", expected_digest)
```

## 与参考基因组集成

使用标准参考基因组：

```python
# Load reference genome
store = gtars.RefgetStore.from_fasta("hg38.fa")

# Get chromosome sequences
chr1 = store.get_sequence("chr1")
chr2 = store.get_sequence("chr2")

# Get subsequence
region_seq = store.get_subsequence("chr1", 1000, 2000)
```

## CLI 用法

从命令管理参考序列line:

```bash
# Compute digest for FASTA file
gtars refget digest --input genome.fa --output digests.txt

# Verify sequence digest
gtars refget verify --sequence sequence.fa --digest expected_digest
```

## Refget 协议合规性

refget 模块遵循 GA4GH refget 协议:

### 摘要计算

摘要使用截断为 48 的 SHA-512 计算字节：

```python
# Compute refget-compliant digest
digest = gtars.refget.compute_digest(sequence)
# Returns: "SQ.abc123..."
```

### 序列检索

通过摘要检索序列：

```python
# Get sequence by refget digest
seq = store.get_sequence_by_digest("SQ.abc123...")
```

## 使用案例

### 参考验证

验证参考基因组完整性：

```python
# Compute digests for reference
store = gtars.RefgetStore.from_fasta("reference.fa")
digests = {chrom: store.get_digest(chrom) for chrom in store.chromosomes}

# Compare with expected digests
for chrom, expected in expected_digests.items():
    actual = digests[chrom]
    if actual != expected:
        print(f"Mismatch for {chrom}: {actual} != {expected}")
```

### 序列提取

提取特定基因组区域：

```python
# Extract regions of interest
store = gtars.RefgetStore.from_fasta("hg38.fa")

regions = [
    ("chr1", 1000, 2000),
    ("chr2", 5000, 6000),
    ("chr3", 10000, 11000)
]

sequences = [store.get_subsequence(c, s, e) for c, s, e in regions]
```

### 交叉引用比较

比较不同基因组之间的序列参考文献：

```python
# Load two reference versions
hg19 = gtars.RefgetStore.from_fasta("hg19.fa")
hg38 = gtars.RefgetStore.from_fasta("hg38.fa")

# Compare digests
for chrom in hg19.chromosomes:
    digest_19 = hg19.get_digest(chrom)
    digest_38 = hg38.get_digest(chrom)
    if digest_19 != digest_38:
        print(f"{chrom} differs between hg19 and hg38")
```

## 性能说明

- 按需加载序列
- 计算后缓存摘要
- 高效子序列提取
- 大型基因组的内存映射文件支持
