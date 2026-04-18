# 有效基因组大小

## 定义

有效基因组大小是指“可映射”基因组的长度，即可以通过测序读数唯一映射的区域。该指标对于许多 deepTools 命令中的正确标准化至关重要。

## 为什么重要

- RPGC 标准化所需 (`--normalizeUsing RPGC`)
- 影响覆盖率计算的准确性
- 必须匹配您的数据处理方法（过滤与未过滤的读取）

## 计算方法

1. **非 N 碱基**：基因组序列 
2 中非 N 核苷酸的计数。 **独特的可映射性**：可以唯一映射的特定大小的区域（可以考虑编辑距离）

## 常见生物体值

### 使用非N碱基方法

|有机体 |组装|有效尺寸|完整命令 |
|---------|----------|----------------|------------------------|
|人类 | GRCh38/hg38 | 2,913,022,398 | 2,913,022,398 `--effectiveGenomeSize 2913022398` |
|人类 | GRCh37/hg19 | GRCh37/hg19 2,864,785,220 | `--effectiveGenomeSize 2864785220` |
|鼠标| GRCm39/mm39 | 2,654,621,837 | 2,654,621,837 `--effectiveGenomeSize 2654621837` |
|鼠标| GRCm38/mm10 | 2,652,783,500 | `--effectiveGenomeSize 2652783500` |
|斑马鱼 | GRCz11 | 1,368,780,147 | 1,368,780,147 `--effectiveGenomeSize 1368780147` |
| *果蝇* | DM6 | 142,573,017 | 142,573,017 `--effectiveGenomeSize 142573017` |
| *C。线虫* | WBcel235/ce11 | 100,286,401 | `--effectiveGenomeSize 100286401` |
| *C。线虫* | CE10 | 100,258,171 | 100,258,171 `--effectiveGenomeSize 100258171` |

### Human (GRCh38)（按读长）

对于质量过滤的读长，值因读长而异：

|阅读长度 |有效尺寸|
|------------------------|----------------|
| 50bp|约 27 亿 |
| 75bp |约 28 亿 |
| 100bp|约 28 亿 |
| 150bp|约 29 亿 |
| 250bp|约 29 亿 |

### 鼠标 (GRCm38)（按读长计算）

|阅读长度 |有效尺寸|
|------------------------|----------------|
| 50bp|约 23 亿 |
| 75bp |约 25 亿 |
| 100bp|约 26 亿 |

## 在 DeepTools 中的使用

有效基因组大小最常用于：

### bam 与 RPGC 标准化的覆盖
```bash
bamCoverage --bam input.bam --outFileName output.bw \
    --normalizeUsing RPGC \
    --effectiveGenomeSize 2913022398
```

### bam 与 RPGC 标准化比较
```bash
bamCompare -b1 treatment.bam -b2 control.bam \
    --outFileName comparison.bw \
    --scaleFactorsMethod RPGC \
    --effectiveGenomeSize 2913022398
```

### 计算GCBias / 正确GCBias
```bash
computeGCBias --bamfile input.bam \
    --effectiveGenomeSize 2913022398 \
    --genome genome.2bit \
    --fragmentLength 200 \
    --biasPlot bias.png
```

## 选择正确的值

* *对于大多数分析：**对参考基因组使用非N碱基方法值

* *对于过滤后的数据：**如果您应用严格的质量过滤器或删除多重映射读取，请考虑使用特定于读取长度的值

* *当不确定时：**使用保守的非N碱基值 - 它更广泛适用

## 常见Shortcuts

deepTools 在某些上下文中也接受这些简写值：

- `hs` 或 `GRCh38`：2913022398
- `mm` 或 `GRCm38`： 2652783500
- `dm` 或 `dm6`: 142573017
- `ce` 或 `ce10`: 100286401

 检查您的特定 deepTools 版本文档

## 计算自定义值

对于自定义基因组或组装体，计算非N碱基计数：

```bash
# Using faCount (UCSC tools)
faCount genome.fa | grep "total" | awk '{print $2-$7}'

# Using seqtk
seqtk comp genome.fa | awk '{x+=$2}END{print x}'
```

## 参考文献

有关最新的有效基因组大小和详细计算方法，请参阅：
- deepTools 文档：https://deeptools.readthedocs.io/en/latest/content/feature/ effectiveGenomeSize.html
- 参考基因组详细信息的 ENCODE 文档
