# IQ-TREE 2 系统发育推断参考

## 基本命令语法

```bash
iqtree2 -s alignment.fasta --prefix output -m TEST -B 1000 -T AUTO --redo
```

## 关键参数

|旗帜|描述 |默认 |
|------|-------------|---------|
| `-s` |输入对齐文件 |必填|
| `--prefix` |输出文件前缀|对齐名称 |
| `-m` |替代模型（或测试）| GTR+G |
| `-B` |超快引导复制 |关 |
| `-b` |标准引导复制（慢）|关闭|
| `-T` |线程数（或自动）| 1 |
| `-o` |外类群分类单元名称 |无（无根）|
| `--redo` |覆盖现有结果 |关闭|
| `-alrt` | SH-aLRT 测试重复 |关闭 |

## 型号选择

```bash
# Full model testing (automatically selects best model)
iqtree2 -s alignment.fasta -m TEST --prefix test_run -B 1000 -T 4

# Specify model explicitly
iqtree2 -s alignment.fasta -m GTR+G4 --prefix gtr_run -B 1000

# Protein sequences
iqtree2 -s protein.fasta -m TEST --prefix prot_tree -B 1000

# Codon-based analysis
iqtree2 -s codon.fasta -m GY --prefix codon_tree -B 1000
```

## 自举方法

### 超快速自举（UFBoot，推荐）
```bash
iqtree2 -s alignment.fasta -B 1000  # 1000 replicates
# Values ≥95 are reliable
# ~10× faster than standard bootstrap
```

### 标准Bootstrap
```bash
iqtree2 -s alignment.fasta -b 100  # 100 replicates (very slow)
```

### SH-aLRT测试（快速替代）
```bash
iqtree2 -s alignment.fasta -alrt 1000 -B 1000  # Both SH-aLRT and UFBoot
# SH-aLRT ≥80 AND UFBoot ≥95 = well-supported branch
```

## 分支支持解读

|引导值|解读|
|----------------|----------------|
| ≥ 95 | Well-supported（强烈支持）|
| 70–94 |中等支持|
| 50–69 |弱支持|
| < 50 |不可靠（不支持） |

## 输出文件

|文件 |描述 |
|------|--------------|
| `{prefix}.treefile` | Newick 格式的最佳 ML 树 |
| `{prefix}.iqtree` |完整分析报告|
| `{prefix}.log` |计算日志|
| `{prefix}.contree` | bootstrap 的共识树 |
| `{prefix}.splits.nex` |网络分裂|
| `{prefix}.bionj` | BioNJ 起始树 |
| `{prefix}.model.gz` |已保存的模型参数 |

## 高级分析

### 分子钟（约会）

```bash
# Temporal analysis with sampling dates
iqtree2 -s alignment.fasta -m GTR+G \
        --date dates.tsv \           # Tab-separated: taxon_name  YYYY-MM-DD
        --clock-test \               # Test for clock-like evolution
        --date-CI 95 \              # 95% CI for node dates
        --prefix dated_tree
```

### 一致性因子

```bash
# Gene concordance factor (gCF) - requires multiple gene alignments
iqtree2 --gcf gene_trees.nwk \
        --tree main_tree.treefile \
        --cf-verbose \
        --prefix cf_analysis
```

### 祖先序列重建

```bash
iqtree2 -s alignment.fasta -m LG+G4 \
        -asr \                      # Marginal ancestral state reconstruction
        --prefix anc_tree
# Output: {prefix}.state (ancestral sequences per node)
```

### 分区模型（多基因）

```bash
# Create partition file (partitions.txt):
# DNA, gene1 = 1-500
# DNA, gene2 = 501-1000

iqtree2 -s concat_alignment.fasta \
        -p partitions.txt \
        -m TEST \
        -B 1000 \
        --prefix partition_tree
```

## IQ-TREE日志解析

```python
def parse_iqtree_log(log_file: str) -> dict:
    """Extract key results from IQ-TREE log file."""
    results = {}
    with open(log_file) as f:
        for line in f:
            if "Best-fit model" in line:
                results["best_model"] = line.split(":")[1].strip()
            elif "Log-likelihood of the tree:" in line:
                results["log_likelihood"] = float(line.split(":")[1].strip())
            elif "Number of free parameters" in line:
                results["free_params"] = int(line.split(":")[1].strip())
            elif "Akaike information criterion" in line:
                results["AIC"] = float(line.split(":")[1].strip())
            elif "Bayesian information criterion" in line:
                results["BIC"] = float(line.split(":")[1].strip())
            elif "Total CPU time used" in line:
                results["cpu_time"] = line.split(":")[1].strip()
    return results

# Example:
# results = parse_iqtree_log("output.log")
# print(f"Best model: {results['best_model']}")
# print(f"Log-likelihood: {results['log_likelihood']:.2f}")
```

## 常见问题和解决方案

|问题 |可能的原因 |解决方案|
|-------|-------------|---------|
|所有引导值 = 0 |类群太少|引导程序需要 ≥4 个类群 |
|很长的树枝|对准工件 |重新修剪对齐；检查异常值 |
|内存错误 |序列太多 |使用FastTree；或将 `-T` 减少为 1 |
|模型拟合不佳|错误的字母 |检查核苷酸与蛋白质规格 |
|相同的序列|重复序列 |对齐前删除重复项 |

## MAFFT 对齐指南

```bash
# Accurate (< 200 sequences)
mafft --localpair --maxiterate 1000 input.fasta > aligned.fasta

# Medium (200-1000 sequences)
mafft --auto input.fasta > aligned.fasta

# Fast (> 1000 sequences)
mafft --fftns input.fasta > aligned.fasta

# Very large (> 10000 sequences)
mafft --retree 1 input.fasta > aligned.fasta

# Using multiple threads
mafft --thread 8 --auto input.fasta > aligned.fasta
```
