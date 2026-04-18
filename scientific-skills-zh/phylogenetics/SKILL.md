---
name: phylogenetics
description: 使用 MAFFT（多重比对）、IQ-TREE 2（最大似然）和 FastTree（快速 NJ/ML）构建和分析系统发育树。使用 ETE3 或 FigTree 进行可视化。用于进化分析、微生物基因组学、病毒系统动力学、蛋白质家族分析和分子钟研究。
license: Unknown
metadata:
    skill-author: Kuan-lin Huang
---

# 系统发育学

## 概述

系统发育分析通过推断后代的分支模式来重建生物序列（基因、蛋白质、基因组）的进化历史。该技能涵盖标准管道：

1. **MAFFT** — 多序列比对
2. **IQ-TREE 2** — 使用模型选择的最大似然树推理 
3. **FastTree** - 快速近似最大似然（对于大型数据集）
4. **ETE3** - 用于树操作和可视化的 Python 库

* *安装：**
```bash
# Conda (recommended for CLI tools)
conda install -c bioconda mafft iqtree fasttree
pip install ete3
```

## 何时使用此技能

何时使用系统发育：

- **进化关系**：哪个生物体/基因与我的序列最密切相关？
- **病毒系统动力学**：追踪疫情传播并估计传播日期
- **蛋白质家族分析**：推断基因家族内的进化关系
- **水平基因转移检测**：识别具有不一致物种/基因树的基因
- **祖先序列重建**：推断祖先蛋白质序列
- **分子钟分析**：使用时间采样估计分歧日期
- **GWAS 伴侣**：将变异置于进化背景中（例如 SARS-CoV-2 变异）
- **微生物学**：来自 16S rRNA 的物种系统发育或核心基因组系统发育

## 标准工作流程

### 1. 多序列比对MAFFT

```python
import subprocess
import os

def run_mafft(input_fasta: str, output_fasta: str, method: str = "auto",
               n_threads: int = 4) -> str:
    """
    Align sequences with MAFFT.

    Args:
        input_fasta: Path to unaligned FASTA file
        output_fasta: Path for aligned output
        method: 'auto' (auto-select), 'einsi' (accurate), 'linsi' (accurate, slow),
                'fftnsi' (medium), 'fftns' (fast), 'retree2' (fast)
        n_threads: Number of CPU threads

    Returns:
        Path to aligned FASTA file
    """
    methods = {
        "auto": ["mafft", "--auto"],
        "einsi": ["mafft", "--genafpair", "--maxiterate", "1000"],
        "linsi": ["mafft", "--localpair", "--maxiterate", "1000"],
        "fftnsi": ["mafft", "--fftnsi"],
        "fftns": ["mafft", "--fftns"],
        "retree2": ["mafft", "--retree", "2"],
    }

    cmd = methods.get(method, methods["auto"])
    cmd += ["--thread", str(n_threads), "--inputorder", input_fasta]

    with open(output_fasta, 'w') as out:
        result = subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"MAFFT failed:\n{result.stderr}")

    # Count aligned sequences
    with open(output_fasta) as f:
        n_seqs = sum(1 for line in f if line.startswith('>'))
    print(f"MAFFT: aligned {n_seqs} sequences → {output_fasta}")

    return output_fasta

# MAFFT method selection guide:
# Few sequences (<200), accurate: linsi or einsi
# Many sequences (<1000), moderate: fftnsi
# Large datasets (>1000): fftns or auto
# Ultra-fast (>10000): mafft --retree 1
```

### 2. 修剪对齐（可选但推荐）

```python
def trim_alignment_trimal(aligned_fasta: str, output_fasta: str,
                            method: str = "automated1") -> str:
    """
    Trim poorly aligned columns with TrimAl.

    Methods:
    - 'automated1': Automatic heuristic (recommended)
    - 'gappyout': Remove gappy columns
    - 'strict': Strict gap threshold
    """
    cmd = ["trimal", f"-{method}", "-in", aligned_fasta, "-out", output_fasta, "-fasta"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"TrimAl warning: {result.stderr}")
        # Fall back to using the untrimmed alignment
        import shutil
        shutil.copy(aligned_fasta, output_fasta)
    return output_fasta
```

### 3. IQ-TREE 2 — 最大似然Tree

```python
def run_iqtree(aligned_fasta: str, output_prefix: str,
                model: str = "TEST", bootstrap: int = 1000,
                n_threads: int = 4, extra_args: list = None) -> dict:
    """
    Build a maximum likelihood tree with IQ-TREE 2.

    Args:
        aligned_fasta: Aligned FASTA file
        output_prefix: Prefix for output files
        model: 'TEST' for automatic model selection, or specify (e.g., 'GTR+G' for DNA,
               'LG+G4' for proteins, 'JTT+G' for proteins)
        bootstrap: Number of ultrafast bootstrap replicates (1000 recommended)
        n_threads: Number of threads ('AUTO' to auto-detect)
        extra_args: Additional IQ-TREE arguments

    Returns:
        Dict with paths to output files
    """
    cmd = [
        "iqtree2",
        "-s", aligned_fasta,
        "--prefix", output_prefix,
        "-m", model,
        "-B", str(bootstrap),   # Ultrafast bootstrap
        "-T", str(n_threads),
        "--redo"                # Overwrite existing results
    ]

    if extra_args:
        cmd.extend(extra_args)

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"IQ-TREE failed:\n{result.stderr}")

    # Print model selection result
    log_file = f"{output_prefix}.log"
    if os.path.exists(log_file):
        with open(log_file) as f:
            for line in f:
                if "Best-fit model" in line:
                    print(f"IQ-TREE: {line.strip()}")

    output_files = {
        "tree": f"{output_prefix}.treefile",
        "log": f"{output_prefix}.log",
        "iqtree": f"{output_prefix}.iqtree",  # Full report
        "model": f"{output_prefix}.model.gz",
    }

    print(f"IQ-TREE: Tree saved to {output_files['tree']}")
    return output_files

# IQ-TREE model selection guide:
# DNA:     TEST → GTR+G, HKY+G, TrN+G
# Protein: TEST → LG+G4, WAG+G, JTT+G, Q.pfam+G
# Codon:   TEST → MG+F3X4

# For temporal (molecular clock) analysis, add:
# extra_args = ["--date", "dates.txt", "--clock-test", "--date-CI", "95"]
```

### 4. FastTree — 快速近似 ML

对于 IQ-TREE 太慢的大型数据集（>1000 个序列）：

```python
def run_fasttree(aligned_fasta: str, output_tree: str,
                  sequence_type: str = "nt", model: str = "gtr",
                  n_threads: int = 4) -> str:
    """
    Build a fast approximate ML tree with FastTree.

    Args:
        sequence_type: 'nt' for nucleotide or 'aa' for amino acid
        model: For nt: 'gtr' (recommended) or 'jc'; for aa: 'lg', 'wag', 'jtt'
    """
    if sequence_type == "nt":
        cmd = ["FastTree", "-nt", "-gtr"]
    else:
        cmd = ["FastTree", f"-{model}"]

    cmd += [aligned_fasta]

    with open(output_tree, 'w') as out:
        result = subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"FastTree failed:\n{result.stderr}")

    print(f"FastTree: Tree saved to {output_tree}")
    return output_tree
```

### 5. 树分析和可视化ETE3

```python
from ete3 import Tree, TreeStyle, NodeStyle, TextFace, PhyloTree
import matplotlib.pyplot as plt

def load_tree(tree_file: str) -> Tree:
    """Load a Newick tree file."""
    t = Tree(tree_file)
    print(f"Tree: {len(t)} leaves, {len(list(t.traverse()))} nodes")
    return t

def basic_tree_stats(t: Tree) -> dict:
    """Compute basic tree statistics."""
    leaves = t.get_leaves()
    distances = [t.get_distance(l1, l2) for l1 in leaves[:min(50, len(leaves))]
                 for l2 in leaves[:min(50, len(leaves))] if l1 != l2]

    stats = {
        "n_leaves": len(leaves),
        "n_internal_nodes": len(t) - len(leaves),
        "total_branch_length": sum(n.dist for n in t.traverse()),
        "max_leaf_distance": max(distances) if distances else 0,
        "mean_leaf_distance": sum(distances)/len(distances) if distances else 0,
    }
    return stats

def find_mrca(t: Tree, leaf_names: list) -> Tree:
    """Find the most recent common ancestor of a set of leaves."""
    return t.get_common_ancestor(*leaf_names)

def visualize_tree(t: Tree, output_file: str = "tree.png",
                    show_branch_support: bool = True,
                    color_groups: dict = None,
                    width: int = 800) -> None:
    """
    Render phylogenetic tree to image.

    Args:
        t: ETE3 Tree object
        color_groups: Dict mapping leaf_name → color (for coloring taxa)
        show_branch_support: Show bootstrap values
    """
    ts = TreeStyle()
    ts.show_leaf_name = True
    ts.show_branch_support = show_branch_support
    ts.mode = "r"  # 'r' = rectangular, 'c' = circular

    if color_groups:
        for node in t.traverse():
            if node.is_leaf() and node.name in color_groups:
                nstyle = NodeStyle()
                nstyle["fgcolor"] = color_groups[node.name]
                nstyle["size"] = 8
                node.set_style(nstyle)

    t.render(output_file, tree_style=ts, w=width, units="px")
    print(f"Tree saved to: {output_file}")

def midpoint_root(t: Tree) -> Tree:
    """Root tree at midpoint (use when outgroup unknown)."""
    t.set_outgroup(t.get_midpoint_outgroup())
    return t

def prune_tree(t: Tree, keep_leaves: list) -> Tree:
    """Prune tree to keep only specified leaves."""
    t.prune(keep_leaves, preserve_branch_length=True)
    return t
```

### 6. 完整分析脚本

```python
import subprocess, os
from ete3 import Tree

def full_phylogenetic_analysis(
    input_fasta: str,
    output_dir: str = "phylo_results",
    sequence_type: str = "nt",
    n_threads: int = 4,
    bootstrap: int = 1000,
    use_fasttree: bool = False
) -> dict:
    """
    Complete phylogenetic pipeline: align → trim → tree → visualize.

    Args:
        input_fasta: Unaligned FASTA
        sequence_type: 'nt' (nucleotide) or 'aa' (amino acid/protein)
        use_fasttree: Use FastTree instead of IQ-TREE (faster for large datasets)
    """
    os.makedirs(output_dir, exist_ok=True)
    prefix = os.path.join(output_dir, "phylo")

    print("=" * 50)
    print("Step 1: Multiple Sequence Alignment (MAFFT)")
    aligned = run_mafft(input_fasta, f"{prefix}_aligned.fasta",
                         method="auto", n_threads=n_threads)

    print("\nStep 2: Tree Inference")
    if use_fasttree:
        tree_file = run_fasttree(
            aligned, f"{prefix}.tree",
            sequence_type=sequence_type,
            model="gtr" if sequence_type == "nt" else "lg"
        )
    else:
        model = "TEST" if sequence_type == "nt" else "TEST"
        iqtree_files = run_iqtree(
            aligned, prefix,
            model=model,
            bootstrap=bootstrap,
            n_threads=n_threads
        )
        tree_file = iqtree_files["tree"]

    print("\nStep 3: Tree Analysis")
    t = Tree(tree_file)
    t = midpoint_root(t)

    stats = basic_tree_stats(t)
    print(f"Tree statistics: {stats}")

    print("\nStep 4: Visualization")
    visualize_tree(t, f"{prefix}_tree.png", show_branch_support=True)

    # Save rooted tree
    rooted_tree_file = f"{prefix}_rooted.nwk"
    t.write(format=1, outfile=rooted_tree_file)

    results = {
        "aligned_fasta": aligned,
        "tree_file": tree_file,
        "rooted_tree": rooted_tree_file,
        "visualization": f"{prefix}_tree.png",
        "stats": stats
    }

    print("\n" + "=" * 50)
    print("Phylogenetic analysis complete!")
    print(f"Results in: {output_dir}/")
    return results
```

## IQ-TREE 模型指南

### DNA 模型

|型号|描述 |用例 |
|--------|-------------|---------|
| `GTR+G4` |一般时间可逆+伽玛 |最灵活的DNA模型|
| `HKY+G4` |长谷川-岸野-矢野+伽马|二费率型号（普通）|
| `TrN+G4` |田村宁|不等过渡|
| `JC` |朱克斯-坎托|最简单；所有费率均相同 |

### 蛋白质模型

|型号|描述 |用例 |
|--------|-------------|---------|
| `LG+G4` |勒加斯丘尔 + 伽玛 |最佳平均蛋白质模型|
| `WAG+G4` |惠兰-戈德曼 |应用广泛|
| `JTT+G4` |琼斯-泰勒-桑顿 |经典款|
| `Q.pfam+G4` |受过 pfam 培训 |对于 Pfam 样蛋白家族 |
| `Q.bird+G4` |鸟类专用|脊椎动物蛋白|

* *提示：**使用`-m TEST`让IQ-TREE自动选择最佳模型。

## 最佳实践

- **比对质量第一**：比对不良→树不可靠；手动检查对齐
- **使用 `linsi` 进行小对齐（<200 seq），使用 `fftns` 或 `auto` 进行大对齐**
- **模型选择**：除非有特定原因，否则始终使用 `-m TEST` 进行 IQ-TREE
- **引导程序**：使用≥1000个超快引导程序（`-B 1000`）来支持分支
- **给树生根**：无根的树可能会产生误导；使用外群或中点生根
- **FastTree for >5000 个序列**：IQ-TREE 变慢； FastTree 快 10–100 倍
- **修剪长对齐**：TrimAl 删除不可靠的列；提高树的准确性
- **在构建树之前检查病毒/细菌序列中的重组**（`RDP4`、`GARD`）

## 其他资源

- **MAFFT**：https://mafft.cbrc.jp/al​​ignment/software/
- **IQ-TREE 2**：http://www.iqtree.org/ |教程：https://www.iqtree.org/workshop/molevol2022
- **FastTree**：http://www.microbesonline.org/fasttree/
- **ETE3**：http://etetoolkit.org/
- **FigTree**（GUI 可视化）： https://tree.bio.ed.ac.uk/software/figtree/
- **iTOL**（网络可视化）：https://itol.embl.de/
- **MUSCLE**（替代对准器）：https://www.drive5.com/muscle/
- **TrimAl**（对准修剪）： https://vicfero.github.io/trimal/
