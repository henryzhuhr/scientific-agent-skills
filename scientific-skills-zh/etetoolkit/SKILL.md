---
name: etetoolkit
description: 系统发育树工具包（ETE）。树操作 (Newick/NHX)、进化事件检测、直系同源/旁系同源、NCBI 分类、可视化 (PDF/SVG)，用于系统发育学。
license: GPL-3.0 license
metadata:
    skill-author: K-Dense Inc.
---

# ETE 工具包技能

## 概述

ETE（树探索环境）是一个用于系统发育和层次树分析的工具包。操作树、分析进化事件、可视化结果并与生物数据库集成，以进行系统发育研究和聚类分析。

## 核心功能

### 1. 树操作和分析

加载、操作和分析分层树结构，支持：

- **树 I/O**：读写 Newick、NHX、PhyloXML 和 NeXML格式
- **树遍历**：使用前序、后序或层序策略导航树
- **拓扑修改**：剪枝、根、折叠节点、解析多分体
- **距离计算**：计算节点之间的分支长度和拓扑距离
- **树比较**：计算Robinson-Foulds距离并识别拓扑差异

* *常见模式：**

```python
from ete3 import Tree

# Load tree from file
tree = Tree("tree.nw", format=1)

# Basic statistics
print(f"Leaves: {len(tree)}")
print(f"Total nodes: {len(list(tree.traverse()))}")

# Prune to taxa of interest
taxa_to_keep = ["species1", "species2", "species3"]
tree.prune(taxa_to_keep, preserve_branch_length=True)

# Midpoint root
midpoint = tree.get_midpoint_outgroup()
tree.set_outgroup(midpoint)

# Save modified tree
tree.write(outfile="rooted_tree.nw")
```

使用`scripts/tree_operations.py`进行命令行树操作：

```bash
# Display tree statistics
python scripts/tree_operations.py stats tree.nw

# Convert format
python scripts/tree_operations.py convert tree.nw output.nw --in-format 0 --out-format 1

# Reroot tree
python scripts/tree_operations.py reroot tree.nw rooted.nw --midpoint

# Prune to specific taxa
python scripts/tree_operations.py prune tree.nw pruned.nw --keep-taxa "sp1,sp2,sp3"

# Show ASCII visualization
python scripts/tree_operations.py ascii tree.nw
```

### 2.系统发育分析

用进化事件分析基因树检测：

- **序列比对集成**：将树链接到多个序列比对（FASTA、Phylip）
- **物种命名**：从基因名称中自动或自定义物种提取
- **进化事件**：使用物种重叠或树协调检测重复和物种形成事件
- **直系检测**：识别基于进化事件的直系同源物和旁系同源物
- **基因家族分析**：通过重复分裂树，折叠谱系特异性扩展

* *基因树分析的工作流程：**

```python
from ete3 import PhyloTree

# Load gene tree with alignment
tree = PhyloTree("gene_tree.nw", alignment="alignment.fasta")

# Set species naming function
def get_species(gene_name):
    return gene_name.split("_")[0]

tree.set_species_naming_function(get_species)

# Detect evolutionary events
events = tree.get_descendant_evol_events()

# Analyze events
for node in tree.traverse():
    if hasattr(node, "evoltype"):
        if node.evoltype == "D":
            print(f"Duplication at {node.name}")
        elif node.evoltype == "S":
            print(f"Speciation at {node.name}")

# Extract ortholog groups
ortho_groups = tree.get_speciation_trees()
for i, ortho_tree in enumerate(ortho_groups):
    ortho_tree.write(outfile=f"ortholog_group_{i}.nw")
```

* *寻找直向同源物和paralogs:**

```python
# Find orthologs to query gene
query = tree & "species1_gene1"

orthologs = []
paralogs = []

for event in events:
    if query in event.in_seqs:
        if event.etype == "S":
            orthologs.extend([s for s in event.out_seqs if s != query])
        elif event.etype == "D":
            paralogs.extend([s for s in event.out_seqs if s != query])
```

### 3. NCBI 分类集成

集成 NCBI 分类数据库中的分类信息：

- **数据库访问**：NCBI分类标准自动下载和本地缓存（~300MB）
- **分类/名称翻译**：分类ID和科学名称之间的转换
- **谱系检索**：获取完整的进化谱系
- **分类树**：构建连接指定分类的物种树
- **树注释**：自动使用分类信息注释树

* *构建基于分类的树：**

```python
from ete3 import NCBITaxa

ncbi = NCBITaxa()

# Build tree from species names
species = ["Homo sapiens", "Pan troglodytes", "Mus musculus"]
name2taxid = ncbi.get_name_translator(species)
taxids = [name2taxid[sp][0] for sp in species]

# Get minimal tree connecting taxa
tree = ncbi.get_topology(taxids)

# Annotate nodes with taxonomy info
for node in tree.traverse():
    if hasattr(node, "sci_name"):
        print(f"{node.sci_name} - Rank: {node.rank} - TaxID: {node.taxid}")
```

* *注释现有树：**

```python
# Get taxonomy info for tree leaves
for leaf in tree:
    species = extract_species_from_name(leaf.name)
    taxid = ncbi.get_name_translator([species])[species][0]

    # Get lineage
    lineage = ncbi.get_lineage(taxid)
    ranks = ncbi.get_rank(lineage)
    names = ncbi.get_taxid_translator(lineage)

    # Add to node
    leaf.add_feature("taxid", taxid)
    leaf.add_feature("lineage", [names[t] for t in lineage])
```

### 4. 树可视化

创建出版物质量的树可视化：

- **输出格式**：用于出版物的 PNG（光栅）、PDF 和 SVG（矢量）
- **布局模式**：矩形和圆形树布局
- **交互式 GUI**：通过缩放、平移和搜索交互地探索树
- **自定义样式**：节点外观的 NodeStyle（颜色、 
- **面**：向节点添加图形元素（文本、图像、图表、热图）
- **布局功能**：基于节点属性的动态样式

  * *基本可视化工作流程：**

```python
from ete3 import Tree, TreeStyle, NodeStyle

tree = Tree("tree.nw")

# Configure tree style
ts = TreeStyle()
ts.show_leaf_name = True
ts.show_branch_support = True
ts.scale = 50  # pixels per branch length unit

# Style nodes
for node in tree.traverse():
    nstyle = NodeStyle()

    if node.is_leaf():
        nstyle["fgcolor"] = "blue"
        nstyle["size"] = 8
    else:
        # Color by support
        if node.support > 0.9:
            nstyle["fgcolor"] = "darkgreen"
        else:
            nstyle["fgcolor"] = "red"
        nstyle["size"] = 5

    node.set_style(nstyle)

# Render to file
tree.render("tree.pdf", tree_style=ts)
tree.render("tree.png", w=800, h=600, units="px", dpi=300)
```

使用`scripts/quick_visualize.py`进行快速可视化：

```bash
# Basic visualization
python scripts/quick_visualize.py tree.nw output.pdf

# Circular layout with custom styling
python scripts/quick_visualize.py tree.nw output.pdf --mode c --color-by-support

# High-resolution PNG
python scripts/quick_visualize.py tree.nw output.png --width 1200 --height 800 --units px --dpi 300

# Custom title and styling
python scripts/quick_visualize.py tree.nw output.pdf --title "Species Phylogeny" --show-support
```

* *带面的高级可视化：**

```python
from ete3 import Tree, TreeStyle, TextFace, CircleFace

tree = Tree("tree.nw")

# Add features to nodes
for leaf in tree:
    leaf.add_feature("habitat", "marine" if "fish" in leaf.name else "land")

# Layout function
def layout(node):
    if node.is_leaf():
        # Add colored circle
        color = "blue" if node.habitat == "marine" else "green"
        circle = CircleFace(radius=5, color=color)
        node.add_face(circle, column=0, position="aligned")

        # Add label
        label = TextFace(node.name, fsize=10)
        node.add_face(label, column=1, position="aligned")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_leaf_name = False

tree.render("annotated_tree.pdf", tree_style=ts)
```

### 5.聚类分析

通过数据集成分析层次聚类结果：

- **ClusterTree**：聚类的专用类树状图
- **数据矩阵链接**：将树叶连接到数值剖面
- **聚类指标**：剪影系数、Dunn 指数、聚类间/聚类内距离
- **验证**：使用不同距离度量测试聚类质量
- **热图可视化**：旁边显示数据矩阵树

* *聚类工作流程：**

```python
from ete3 import ClusterTree

# Load tree with data matrix
matrix = """#Names\tSample1\tSample2\tSample3
Gene1\t1.5\t2.3\t0.8
Gene2\t0.9\t1.1\t1.8
Gene3\t2.1\t2.5\t0.5"""

tree = ClusterTree("((Gene1,Gene2),Gene3);", text_array=matrix)

# Evaluate cluster quality
for node in tree.traverse():
    if not node.is_leaf():
        silhouette = node.get_silhouette()
        dunn = node.get_dunn()

        print(f"Cluster: {node.name}")
        print(f"  Silhouette: {silhouette:.3f}")
        print(f"  Dunn index: {dunn:.3f}")

# Visualize with heatmap
tree.show("heatmap")
```

### 6.树比较

量化树之间的拓扑差异：

- **Robinson-Foulds 距离**：树比较的标准度量
- **标准化 RF**：尺度不变距离（0.0 到 1.0）
- **分区分析**：识别唯一和共享的二分
- **共识树**：分析多棵树的支持
- **批量比较**：比较多棵树pairwise

* *比较两棵树：**

```python
from ete3 import Tree

tree1 = Tree("tree1.nw")
tree2 = Tree("tree2.nw")

# Calculate RF distance
rf, max_rf, common_leaves, parts_t1, parts_t2 = tree1.robinson_foulds(tree2)

print(f"RF distance: {rf}/{max_rf}")
print(f"Normalized RF: {rf/max_rf:.3f}")
print(f"Common leaves: {len(common_leaves)}")

# Find unique partitions
unique_t1 = parts_t1 - parts_t2
unique_t2 = parts_t2 - parts_t1

print(f"Unique to tree1: {len(unique_t1)}")
print(f"Unique to tree2: {len(unique_t2)}")
```

* *比较多棵树：**

```python
import numpy as np

trees = [Tree(f"tree{i}.nw") for i in range(4)]

# Create distance matrix
n = len(trees)
dist_matrix = np.zeros((n, n))

for i in range(n):
    for j in range(i+1, n):
        rf, max_rf, _, _, _ = trees[i].robinson_foulds(trees[j])
        norm_rf = rf / max_rf if max_rf > 0 else 0
        dist_matrix[i, j] = norm_rf
        dist_matrix[j, i] = norm_rf
```

## 安装和设置

安装ETE工具包：

```bash
# Basic installation
uv pip install ete3

# With external dependencies for rendering (optional but recommended)
# On macOS:
brew install qt@5

# On Ubuntu/Debian:
sudo apt-get install python3-pyqt5 python3-pyqt5.qtsvg

# For full features including GUI
uv pip install ete3[gui]
```

* *首次 NCBI 分类设置：**

 第一次实例化 NCBITaxa 时，它会自动将 NCBI 分类数据库（~300MB）下载到 `~/.etetoolkit/taxa.sqlite`。这种情况仅发生一次：

```python
from ete3 import NCBITaxa
ncbi = NCBITaxa()  # Downloads database on first run
```

更新分类数据库：

```python
ncbi.update_taxonomy_database()  # Download latest NCBI data
```

## 常见用例

### 用例1：系统基因组管道

从基因树到直系同源的完整工作流程识别：

```python
from ete3 import PhyloTree, NCBITaxa

# 1. Load gene tree with alignment
tree = PhyloTree("gene_tree.nw", alignment="alignment.fasta")

# 2. Configure species naming
tree.set_species_naming_function(lambda x: x.split("_")[0])

# 3. Detect evolutionary events
tree.get_descendant_evol_events()

# 4. Annotate with taxonomy
ncbi = NCBITaxa()
for leaf in tree:
    if leaf.species in species_to_taxid:
        taxid = species_to_taxid[leaf.species]
        lineage = ncbi.get_lineage(taxid)
        leaf.add_feature("lineage", lineage)

# 5. Extract ortholog groups
ortho_groups = tree.get_speciation_trees()

# 6. Save and visualize
for i, ortho in enumerate(ortho_groups):
    ortho.write(outfile=f"ortho_{i}.nw")
```

### 用例 2：树预处理和格式化

用于分析的批处理树：

```bash
# Convert format
python scripts/tree_operations.py convert input.nw output.nw --in-format 0 --out-format 1

# Root at midpoint
python scripts/tree_operations.py reroot input.nw rooted.nw --midpoint

# Prune to focal taxa
python scripts/tree_operations.py prune rooted.nw pruned.nw --keep-taxa taxa_list.txt

# Get statistics
python scripts/tree_operations.py stats pruned.nw
```

### 用例 3：出版质量数据

创建样式可视化：

```python
from ete3 import Tree, TreeStyle, NodeStyle, TextFace

tree = Tree("tree.nw")

# Define clade colors
clade_colors = {
    "Mammals": "red",
    "Birds": "blue",
    "Fish": "green"
}

def layout(node):
    # Highlight clades
    if node.is_leaf():
        for clade, color in clade_colors.items():
            if clade in node.name:
                nstyle = NodeStyle()
                nstyle["fgcolor"] = color
                nstyle["size"] = 8
                node.set_style(nstyle)
    else:
        # Add support values
        if node.support > 0.95:
            support = TextFace(f"{node.support:.2f}", fsize=8)
            node.add_face(support, column=0, position="branch-top")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_scale = True

# Render for publication
tree.render("figure.pdf", w=200, units="mm", tree_style=ts)
tree.render("figure.svg", tree_style=ts)  # Editable vector
```

### 用例 4：自动树分析

系统地处理多棵树：

```python
from ete3 import Tree
import os

input_dir = "trees"
output_dir = "processed"

for filename in os.listdir(input_dir):
    if filename.endswith(".nw"):
        tree = Tree(os.path.join(input_dir, filename))

        # Standardize: midpoint root, resolve polytomies
        midpoint = tree.get_midpoint_outgroup()
        tree.set_outgroup(midpoint)
        tree.resolve_polytomy(recursive=True)

        # Filter low support branches
        for node in tree.traverse():
            if hasattr(node, 'support') and node.support < 0.5:
                if not node.is_leaf() and not node.is_root():
                    node.delete()

        # Save processed tree
        output_file = os.path.join(output_dir, f"processed_{filename}")
        tree.write(outfile=output_file)
```

## 参考文档

有关全面的 API 文档、代码示例和详细指南，请参阅`references/` 目录：

- **`api_reference.md`**：所有 ETE 类和方法（Tree、PhyloTree、ClusterTree、NCBITaxa）的完整 API 文档，包括参数、返回类型和代码示例
- **`workflows.md`**：按任务组织的常见工作流模式（树操作、系统发育分析、树比较、分类集成、聚类）分析）
- **`visualization.md`**：全面的可视化指南，涵盖TreeStyle、NodeStyle、Faces、布局功能和高级可视化技术

需要详细信息时加载这些参考：

```python
# To use API reference
# Read references/api_reference.md for complete method signatures and parameters

# To implement workflows
# Read references/workflows.md for step-by-step workflow examples

# To create visualizations
# Read references/visualization.md for styling and rendering options
```

## 故障排除

* *导入错误：**

```bash
# If "ModuleNotFoundError: No module named 'ete3'"
uv pip install ete3

# For GUI and rendering issues
uv pip install ete3[gui]
```

* *渲染问题：**

如果`tree.render()`或`tree.show()`失败Qt 相关错误，安装系统依赖项：

```bash
# macOS
brew install qt@5

# Ubuntu/Debian
sudo apt-get install python3-pyqt5 python3-pyqt5.qtsvg
```

* *NCBI 分类数据库：**

如果数据库下载失败或损坏：

```python
from ete3 import NCBITaxa
ncbi = NCBITaxa()
ncbi.update_taxonomy_database()  # Redownload database
```

* *大型树的内存问题：**

对于非常大的树（>10,000 个叶子），使用迭代器而不是列表推导式：

```python
# Memory-efficient iteration
for leaf in tree.iter_leaves():
    process(leaf)

# Instead of
for leaf in tree.get_leaves():  # Loads all into memory
    process(leaf)
```

## Newick 格式参考

ETE 支持多种 Newick 格式规范 (0-100)：

- **格式 0**：灵活使用分支长度（默认）
- **格式1**：使用内部节点名称
- **格式 2**：使用引导/支持值
- **格式 5**：内部节点名称 + 分支长度
- **格式 8**：所有特征（名称、距离、支持）
- **格式 9**：仅叶名称
- **格式 100**：仅拓扑

读取/写入时指定格式：

```python
tree = Tree("tree.nw", format=1)
tree.write(outfile="output.nw", format=5)
```

NHX（新罕布什尔扩展）格式保留自定义功能：

```python
tree.write(outfile="tree.nhx", features=["habitat", "temperature", "depth"])
```

## 最佳实践

1. **保留分支长度**：进行系统发育分析时修剪时使用 `preserve_branch_length=True`
2. **缓存内容**：使用`get_cached_content()`重复访问大树
3上的节点内容。 **使用迭代器**：采用 `iter_*` 方法对大型树 
4 进行内存高效处理。 **选择合适的遍历**：后序用于自下而上分析，预序用于自上而下
5. **验证单系**：始终检查返回的进化枝类型（单系/并系/多系）
6. **用于发布的矢量格式**：使用 PDF 或 SVG 来发布图形（可缩放、可编辑）
7. **交互式测试**：在渲染到文件
8之前使用`tree.show()`测试可视化效果。 **用于系统发育学的 PhyloTree**：使用 PhyloTree 类进行基因树和进化分析
9. **复制方法选择**：“newick”用于速度，“cpickle”用于完全保真度，“deepcopy”用于复杂对象
10. **NCBI查询缓存**：存储NCBI分类查询结果以避免重复数据库访问
