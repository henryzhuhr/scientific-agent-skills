# scikit-bio API 参考

本文档提供详细的 API 信息、高级示例以及使用 scikit-bio.

## 目录
1 的故障排除指南。 [序列类](#sequence-classes)
2. [对齐方法](#alignment-methods)
3. [系统发育树](#phylogenesis-trees)
4. [多样性指标](#diversity-metrics)
5. [排序](#ordination)
6. [统计测试](#statistical-tests)
7. [距离矩阵](#distance-matrices)
8. [文件I/O](#file-io)
9. [疑难解答](#疑难解答)

## 序列类

### DNA、RNA 和蛋白质类

```python
from skbio import DNA, RNA, Protein, Sequence

# Creating sequences
dna = DNA('ATCGATCG', metadata={'id': 'seq1', 'description': 'Example'})
rna = RNA('AUCGAUCG')
protein = Protein('ACDEFGHIKLMNPQRSTVWY')

# Sequence operations
dna_rc = dna.reverse_complement()  # Reverse complement
rna = dna.transcribe()  # DNA -> RNA
protein = rna.translate()  # RNA -> Protein

# Using genetic code tables
protein = rna.translate(genetic_code=11)  # Bacterial code
```

### 序列搜索和模式匹配

```python
# Find motifs using regex
dna = DNA('ATGCGATCGATGCATCG')
motif_locs = dna.find_with_regex('ATG.{3}')  # Start codons

# Find all positions
import re
for match in re.finditer('ATG', str(dna)):
    print(f"ATG found at position {match.start()}")

# k-mer counting
from skbio.sequence import _motifs
kmers = dna.kmer_frequencies(k=3)
```

### 处理序列元数据

```python
# Sequence-level metadata
dna = DNA('ATCG', metadata={'id': 'seq1', 'source': 'E. coli'})
print(dna.metadata['id'])

# Positional metadata (per-base quality scores from FASTQ)
from skbio import DNA
seqs = DNA.read('reads.fastq', format='fastq', phred_offset=33)
quality_scores = seqs.positional_metadata['quality']

# Interval metadata (features/annotations)
dna.interval_metadata.add([(5, 15)], metadata={'type': 'gene', 'name': 'geneA'})
```

### 距离计算

```python
from skbio import DNA

seq1 = DNA('ATCGATCG')
seq2 = DNA('ATCG--CG')

# Hamming distance (default)
dist = seq1.distance(seq2)

# Custom distance function
from skbio.sequence.distance import kmer_distance
dist = seq1.distance(seq2, metric=kmer_distance)
```

## 对齐方法

### 成对对齐

```python
from skbio.alignment import local_pairwise_align_ssw, global_pairwise_align
from skbio import DNA, Protein

# Local alignment (Smith-Waterman via SSW)
seq1 = DNA('ATCGATCGATCG')
seq2 = DNA('ATCGGGGATCG')
alignment = local_pairwise_align_ssw(seq1, seq2)

# Access alignment details
print(f"Score: {alignment.score}")
print(f"Start position: {alignment.target_begin}")
aligned_seqs = alignment.aligned_sequences

# Global alignment with custom scoring
from skbio.alignment import AlignScorer

scorer = AlignScorer(
    match_score=2,
    mismatch_score=-3,
    gap_open_penalty=5,
    gap_extend_penalty=2
)

alignment = global_pairwise_align(seq1, seq2, scorer=scorer)

# Protein alignment with substitution matrix
from skbio.alignment import StripedSmithWaterman

protein_query = Protein('ACDEFGHIKLMNPQRSTVWY')
protein_target = Protein('ACDEFMNPQRSTVWY')

aligner = StripedSmithWaterman(
    str(protein_query),
    gap_open_penalty=11,
    gap_extend_penalty=1,
    substitution_matrix='blosum62'
)
alignment = aligner(str(protein_target))
```

### 多重序列比对

```python
from skbio.alignment import TabularMSA
from skbio import DNA

# Read MSA from file
msa = TabularMSA.read('alignment.fasta', constructor=DNA)

# Create MSA manually
seqs = [
    DNA('ATCG--'),
    DNA('ATGG--'),
    DNA('ATCGAT')
]
msa = TabularMSA(seqs)

# MSA operations
consensus = msa.consensus()
majority_consensus = msa.majority_consensus()

# Calculate conservation
conservation = msa.conservation()

# Access sequences
first_seq = msa[0]
column = msa[:, 2]  # Third column

# Filter gaps
degapped_msa = msa.omit_gap_positions(maximum_gap_frequency=0.5)

# Calculate position-specific scores
position_entropies = msa.position_entropies()
```

### CIGAR 字符串处理

```python
from skbio.alignment import AlignPath

# Parse CIGAR string
cigar = "10M2I5M3D10M"
align_path = AlignPath.from_cigar(cigar, target_length=100, query_length=50)

# Convert alignment to CIGAR
alignment = local_pairwise_align_ssw(seq1, seq2)
cigar_string = alignment.to_cigar()
```

## 系统发育树

### 树构建

```python
from skbio import TreeNode, DistanceMatrix
from skbio.tree import nj, upgma

# Distance matrix
dm = DistanceMatrix([[0, 5, 9, 9],
                     [5, 0, 10, 10],
                     [9, 10, 0, 8],
                     [9, 10, 8, 0]],
                    ids=['A', 'B', 'C', 'D'])

# Neighbor joining
nj_tree = nj(dm)

# UPGMA (assumes molecular clock)
upgma_tree = upgma(dm)

# Balanced Minimum Evolution (scalable for large trees)
from skbio.tree import bme
bme_tree = bme(dm)
```

### 树操作

```python
from skbio import TreeNode

# Read tree
tree = TreeNode.read('tree.nwk', format='newick')

# Traversal
for node in tree.traverse():
    print(node.name)

# Preorder, postorder, levelorder
for node in tree.preorder():
    print(node.name)

# Get tips only
tips = list(tree.tips())

# Find specific node
node = tree.find('taxon_name')

# Root tree at midpoint
rooted_tree = tree.root_at_midpoint()

# Prune tree to specific taxa
pruned = tree.shear(['taxon1', 'taxon2', 'taxon3'])

# Get subtree
lca = tree.lowest_common_ancestor(['taxon1', 'taxon2'])
subtree = lca.copy()

# Add/remove nodes
parent = tree.find('parent_name')
child = TreeNode(name='new_child', length=0.5)
parent.append(child)

# Remove node
node_to_remove = tree.find('taxon_to_remove')
node_to_remove.parent.remove(node_to_remove)
```

### 树距离和比较

```python
# Patristic distance (branch-length distance)
node1 = tree.find('taxon1')
node2 = tree.find('taxon2')
patristic = node1.distance(node2)

# Cophenetic matrix (all pairwise distances)
cophenetic_dm = tree.cophenetic_matrix()

# Robinson-Foulds distance (topology comparison)
rf_dist = tree.robinson_foulds(other_tree)

# Compare with unweighted RF
rf_dist, max_rf = tree.robinson_foulds(other_tree, proportion=False)

# Tip-to-tip distances
tip_distances = tree.tip_tip_distances()
```

### 树可视化

```python
# ASCII art visualization
print(tree.ascii_art())

# For advanced visualization, export to external tools
tree.write('tree.nwk', format='newick')

# Then use ete3, toytree, or ggtree for publication-quality figures
```

## 多样性指标

### Alpha多样性

```python
from skbio.diversity import alpha_diversity, get_alpha_diversity_metrics
import numpy as np

# Sample count data (samples x features)
counts = np.array([
    [10, 5, 0, 3],
    [2, 0, 8, 4],
    [5, 5, 5, 5]
])
sample_ids = ['Sample1', 'Sample2', 'Sample3']

# List available metrics
print(get_alpha_diversity_metrics())

# Calculate various alpha diversity metrics
shannon = alpha_diversity('shannon', counts, ids=sample_ids)
simpson = alpha_diversity('simpson', counts, ids=sample_ids)
observed_otus = alpha_diversity('observed_otus', counts, ids=sample_ids)
chao1 = alpha_diversity('chao1', counts, ids=sample_ids)

# Phylogenetic alpha diversity (requires tree)
from skbio import TreeNode

tree = TreeNode.read('tree.nwk')
feature_ids = ['OTU1', 'OTU2', 'OTU3', 'OTU4']

faith_pd = alpha_diversity('faith_pd', counts, ids=sample_ids,
                          tree=tree, otu_ids=feature_ids)
```

### Beta 多样性

```python
from skbio.diversity import beta_diversity, partial_beta_diversity

# Beta diversity (all pairwise comparisons)
bc_dm = beta_diversity('braycurtis', counts, ids=sample_ids)

# Jaccard (presence/absence)
jaccard_dm = beta_diversity('jaccard', counts, ids=sample_ids)

# Phylogenetic beta diversity
unifrac_dm = beta_diversity('unweighted_unifrac', counts,
                           ids=sample_ids,
                           tree=tree,
                           otu_ids=feature_ids)

weighted_unifrac_dm = beta_diversity('weighted_unifrac', counts,
                                    ids=sample_ids,
                                    tree=tree,
                                    otu_ids=feature_ids)

# Compute only specific pairs (more efficient)
pairs = [('Sample1', 'Sample2'), ('Sample1', 'Sample3')]
partial_dm = partial_beta_diversity('braycurtis', counts,
                                   ids=sample_ids,
                                   id_pairs=pairs)
```

### 稀疏和子采样

```python
from skbio.diversity import subsample_counts

# Rarefy to minimum depth
min_depth = counts.min(axis=1).max()
rarefied = [subsample_counts(row, n=min_depth) for row in counts]

# Multiple rarefactions for confidence intervals
import numpy as np
rarefactions = []
for i in range(100):
    rarefied_counts = np.array([subsample_counts(row, n=1000) for row in counts])
    shannon_rare = alpha_diversity('shannon', rarefied_counts)
    rarefactions.append(shannon_rare)

# Calculate mean and std
mean_shannon = np.mean(rarefactions, axis=0)
std_shannon = np.std(rarefactions, axis=0)
```

## 排序

### 主坐标分析(PCoA)

```python
from skbio.stats.ordination import pcoa
from skbio import DistanceMatrix
import numpy as np

# PCoA from distance matrix
dm = DistanceMatrix(...)
pcoa_results = pcoa(dm)

# Access coordinates
pc1 = pcoa_results.samples['PC1']
pc2 = pcoa_results.samples['PC2']

# Proportion explained
prop_explained = pcoa_results.proportion_explained

# Eigenvalues
eigenvalues = pcoa_results.eigvals

# Save results
pcoa_results.write('pcoa_results.txt')

# Plot with matplotlib
import matplotlib.pyplot as plt
plt.scatter(pc1, pc2)
plt.xlabel(f'PC1 ({prop_explained[0]*100:.1f}%)')
plt.ylabel(f'PC2 ({prop_explained[1]*100:.1f}%)')
```

### 规范对应分析(CCA)

```python
from skbio.stats.ordination import cca
import pandas as pd
import numpy as np

# Species abundance matrix (samples x species)
species = np.array([
    [10, 5, 3],
    [2, 8, 4],
    [5, 5, 5]
])

# Environmental variables (samples x variables)
env = pd.DataFrame({
    'pH': [6.5, 7.0, 6.8],
    'temperature': [20, 25, 22],
    'depth': [10, 15, 12]
})

# CCA
cca_results = cca(species, env,
                 sample_ids=['Site1', 'Site2', 'Site3'],
                 species_ids=['SpeciesA', 'SpeciesB', 'SpeciesC'])

# Access constrained axes
cca1 = cca_results.samples['CCA1']
cca2 = cca_results.samples['CCA2']

# Biplot scores for environmental variables
env_scores = cca_results.biplot_scores
```

### 冗余分析(RDA)

```python
from skbio.stats.ordination import rda

# Similar to CCA but for linear relationships
rda_results = rda(species, env,
                 sample_ids=['Site1', 'Site2', 'Site3'],
                 species_ids=['SpeciesA', 'SpeciesB', 'SpeciesC'])
```

## 统计测试

### PERMANOVA

```python
from skbio.stats.distance import permanova
from skbio import DistanceMatrix
import numpy as np

# Distance matrix
dm = DistanceMatrix(...)

# Grouping variable
grouping = ['Group1', 'Group1', 'Group2', 'Group2', 'Group3', 'Group3']

# Run PERMANOVA
results = permanova(dm, grouping, permutations=999)

print(f"Test statistic: {results['test statistic']}")
print(f"p-value: {results['p-value']}")
print(f"Sample size: {results['sample size']}")
print(f"Number of groups: {results['number of groups']}")
```

### ANOSIM

```python
from skbio.stats.distance import anosim

# ANOSIM test
results = anosim(dm, grouping, permutations=999)

print(f"R statistic: {results['test statistic']}")
print(f"p-value: {results['p-value']}")
```

### PERMDISP

```python
from skbio.stats.distance import permdisp

# Test homogeneity of dispersions
results = permdisp(dm, grouping, permutations=999)

print(f"F statistic: {results['test statistic']}")
print(f"p-value: {results['p-value']}")
```

### Mantel 测试

```python
from skbio.stats.distance import mantel
from skbio import DistanceMatrix

# Two distance matrices to compare
dm1 = DistanceMatrix(...)  # e.g., genetic distance
dm2 = DistanceMatrix(...)  # e.g., geographic distance

# Mantel test
r, p_value, n = mantel(dm1, dm2, method='pearson', permutations=999)

print(f"Correlation: {r}")
print(f"p-value: {p_value}")
print(f"Sample size: {n}")

# Spearman correlation
r_spearman, p, n = mantel(dm1, dm2, method='spearman', permutations=999)
```

### 部分Mantel 测试

```python
from skbio.stats.distance import mantel

# Control for a third matrix
dm3 = DistanceMatrix(...)  # controlling variable

r_partial, p_value, n = mantel(dm1, dm2, method='pearson',
                               permutations=999, alternative='two-sided')
```

## 距离矩阵

### 创建和操作距离矩阵

```python
from skbio import DistanceMatrix, DissimilarityMatrix
import numpy as np

# Create from array
data = np.array([[0, 1, 2],
                 [1, 0, 3],
                 [2, 3, 0]])
dm = DistanceMatrix(data, ids=['A', 'B', 'C'])

# Access elements
dist_ab = dm['A', 'B']
row_a = dm['A']

# Slicing
subset_dm = dm.filter(['A', 'C'])

# Asymmetric dissimilarity matrix
asym_data = np.array([[0, 1, 2],
                      [3, 0, 4],
                      [5, 6, 0]])
dissim = DissimilarityMatrix(asym_data, ids=['X', 'Y', 'Z'])

# Read/write
dm.write('distances.txt')
dm2 = DistanceMatrix.read('distances.txt')

# Convert to condensed form (for scipy)
condensed = dm.condensed_form()

# Convert to dataframe
df = dm.to_data_frame()
```

## 文件 I/O

### 读取序列

```python
import skbio

# Read single sequence
dna = skbio.DNA.read('sequence.fasta', format='fasta')

# Read multiple sequences (generator)
for seq in skbio.io.read('sequences.fasta', format='fasta', constructor=skbio.DNA):
    print(seq.metadata['id'], len(seq))

# Read into list
sequences = list(skbio.io.read('sequences.fasta', format='fasta',
                               constructor=skbio.DNA))

# Read FASTQ with quality scores
for seq in skbio.io.read('reads.fastq', format='fastq', constructor=skbio.DNA):
    quality = seq.positional_metadata['quality']
    print(f"Mean quality: {quality.mean()}")
```

### 写入序列

```python
# Write single sequence
dna.write('output.fasta', format='fasta')

# Write multiple sequences
sequences = [dna1, dna2, dna3]
skbio.io.write(sequences, format='fasta', into='output.fasta')

# Write with custom line wrapping
dna.write('output.fasta', format='fasta', max_width=60)
```

### BIOM 表

```python
from skbio import Table

# Read BIOM table
table = Table.read('table.biom', format='hdf5')

# Access data
sample_ids = table.ids(axis='sample')
feature_ids = table.ids(axis='observation')
matrix = table.matrix_data.toarray()  # if sparse

# Filter samples
abundant_samples = table.filter(lambda row, id_, md: row.sum() > 1000, axis='sample')

# Filter features (OTUs/ASVs)
prevalent_features = table.filter(lambda col, id_, md: (col > 0).sum() >= 3,
                                 axis='observation')

# Normalize
relative_abundance = table.norm(axis='sample', inplace=False)

# Write
table.write('filtered_table.biom', format='hdf5')
```

### 格式转换

```python
# FASTQ to FASTA
seqs = skbio.io.read('input.fastq', format='fastq', constructor=skbio.DNA)
skbio.io.write(seqs, format='fasta', into='output.fasta')

# GenBank to FASTA
seqs = skbio.io.read('genes.gb', format='genbank', constructor=skbio.DNA)
skbio.io.write(seqs, format='fasta', into='genes.fasta')
```

## 故障排除

### 常见问题和解决方案

#### 问题：“ValueError：ID 必须是唯一的”
```python
# Problem: Duplicate sequence IDs
# Solution: Make IDs unique or filter duplicates
seen = set()
unique_seqs = []
for seq in sequences:
    if seq.metadata['id'] not in seen:
        unique_seqs.append(seq)
        seen.add(seq.metadata['id'])
```

#### 问题：“ValueError：计数必须是整数"
```python
# Problem: Relative abundances instead of counts
# Solution: Convert to integer counts or use appropriate metrics
counts_int = (abundance_table * 1000).astype(int)
```

#### 问题：大文件出现内存错误
```python
# Problem: Loading entire file into memory
# Solution: Use generators
for seq in skbio.io.read('huge.fasta', format='fasta', constructor=skbio.DNA):
    # Process one at a time
    process(seq)
```

#### 问题：树提示与 OTU ID 不匹配
```python
# Problem: Mismatch between tree tip names and feature IDs
# Solution: Verify and align IDs
tree_tips = {tip.name for tip in tree.tips()}
feature_ids = set(feature_ids)
missing_in_tree = feature_ids - tree_tips
missing_in_table = tree_tips - feature_ids

# Prune tree to match table
tree_pruned = tree.shear(feature_ids)
```

#### 问题：不同序列的对齐失败长度
```python
# Problem: Trying to align pre-aligned sequences
# Solution: Degap sequences first or ensure sequences are unaligned
seq1_degapped = seq1.degap()
seq2_degapped = seq2.degap()
alignment = local_pairwise_align_ssw(seq1_degapped, seq2_degapped)
```

### 性能提示

1. **使用适当的数据结构**：用于大型表的 BIOM HDF5，用于大型序列文件的生成器
2. **并行处理**：使用`partial_beta_diversity()`进行可并行化的子集计算
3. **对大型数据集进行子采样**：对于探索性分析，请首先使用子采样数据
4. **缓存结果**：保存距离矩阵和排序结果以避免重新计算

### 集成示例

#### 与pandas
```python
import pandas as pd
from skbio import DistanceMatrix

# Distance matrix to DataFrame
dm = DistanceMatrix(...)
df = dm.to_data_frame()

# Alpha diversity to DataFrame
alpha = alpha_diversity('shannon', counts, ids=sample_ids)
alpha_df = pd.DataFrame({'shannon': alpha})
```

#### 与matplotlib/seaborn
```python
import matplotlib.pyplot as plt
import seaborn as sns

# PCoA plot
fig, ax = plt.subplots()
scatter = ax.scatter(pc1, pc2, c=grouping, cmap='viridis')
ax.set_xlabel(f'PC1 ({prop_explained[0]*100:.1f}%)')
ax.set_ylabel(f'PC2 ({prop_explained[1]*100:.1f}%)')
plt.colorbar(scatter)

# Heatmap of distance matrix
sns.heatmap(dm.to_data_frame(), cmap='viridis')
```

#### 与QIIME 2
```python
# scikit-bio objects are compatible with QIIME 2
# Export from QIIME 2
# qiime tools export --input-path table.qza --output-path exported/

# Read in scikit-bio
table = Table.read('exported/feature-table.biom')

# Process with scikit-bio
# ...

# Import back to QIIME 2 if needed
table.write('processed-table.biom')
# qiime tools import --input-path processed-table.biom --output-path processed.qza
```
