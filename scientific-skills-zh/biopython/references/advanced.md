# 高级 Biopython 功能

## 使用 Bio.motifs 的序列 Motifs

### 创建 Motifs

```python
from Bio import motifs
from Bio.Seq import Seq

# Create motif from instances
instances = [
    Seq("TACAA"),
    Seq("TACGC"),
    Seq("TACAC"),
    Seq("TACCC"),
    Seq("AACCC"),
    Seq("AATGC"),
    Seq("AATGC"),
]

motif = motifs.create(instances)
```

### Motif 共识和简并序列

```python
# Get consensus sequence
print(motif.counts.consensus)

# Get degenerate consensus (IUPAC ambiguity codes)
print(motif.counts.degenerate_consensus)

# Access counts matrix
print(motif.counts)
```

### 位置权重矩阵（PWM）

```python
# Create position weight matrix
pwm = motif.counts.normalize(pseudocounts=0.5)
print(pwm)

# Calculate information content
ic = motif.counts.information_content()
print(f"Information content: {ic:.2f} bits")
```

### 搜索 Motifs

```python
from Bio.Seq import Seq

# Search sequence for motif
test_seq = Seq("ATACAGGACAGACATACGCATACAACATTACAC")

# Get Position Specific Scoring Matrix (PSSM)
pssm = pwm.log_odds()

# Search sequence
for position, score in pssm.search(test_seq, threshold=5.0):
    print(f"Position {position}: score = {score:.2f}")
```

### 从文件中读取 Motifs

```python
# Read motif from JASPAR format
with open("motif.jaspar") as handle:
    motif = motifs.read(handle, "jaspar")

# Read multiple motifs
with open("motifs.jaspar") as handle:
    for m in motifs.parse(handle, "jaspar"):
        print(m.name)

# Supported formats: jaspar, meme, transfac, pfm
```

### 写入Motifs

```python
# Write motif in JASPAR format
with open("output.jaspar", "w") as handle:
    handle.write(motif.format("jaspar"))
```

## 使用 Bio.PopGen 进行群体遗传学

### 使用 GenePop 文件

```python
from Bio.PopGen import GenePop

# Read GenePop file
with open("data.gen") as handle:
    record = GenePop.read(handle)

# Access populations
print(f"Number of populations: {len(record.populations)}")
print(f"Loci: {record.loci_list}")

# Iterate through populations
for pop_idx, pop in enumerate(record.populations):
    print(f"\nPopulation {pop_idx + 1}:")
    for individual in pop:
        print(f"  {individual[0]}: {individual[1]}")
```

### 计算群体统计

```python
from Bio.PopGen.GenePop.Controller import GenePopController

# Create controller
ctrl = GenePopController()

# Calculate basic statistics
result = ctrl.calc_allele_genotype_freqs("data.gen")

# Calculate Fst
fst_result = ctrl.calc_fst_all("data.gen")
print(f"Fst: {fst_result}")

# Test Hardy-Weinberg equilibrium
hw_result = ctrl.test_hw_pop("data.gen", "probability")
```

## Bio.SeqUtils 的序列实用程序

### GC 内容

```python
from Bio.SeqUtils import gc_fraction
from Bio.Seq import Seq

seq = Seq("ATCGATCGATCG")
gc = gc_fraction(seq)
print(f"GC content: {gc:.2%}")
```

### 分子重量

```python
from Bio.SeqUtils import molecular_weight

# DNA molecular weight
dna_seq = Seq("ATCG")
mw = molecular_weight(dna_seq, seq_type="DNA")
print(f"DNA MW: {mw:.2f} g/mol")

# Protein molecular weight
protein_seq = Seq("ACDEFGHIKLMNPQRSTVWY")
mw = molecular_weight(protein_seq, seq_type="protein")
print(f"Protein MW: {mw:.2f} Da")
```

### 熔解温度

```python
from Bio.SeqUtils import MeltingTemp as mt

# Calculate Tm using nearest-neighbor method
seq = Seq("ATCGATCGATCG")
tm = mt.Tm_NN(seq)
print(f"Tm: {tm:.1f}°C")

# Use different salt concentration
tm = mt.Tm_NN(seq, Na=50, Mg=1.5)  # 50 mM Na+, 1.5 mM Mg2+

# Wallace rule (for primers)
tm_wallace = mt.Tm_Wallace(seq)
```

### GC 偏差

```python
from Bio.SeqUtils import gc_skew

# Calculate GC skew
seq = Seq("ATCGATCGGGCCCAAATTT")
skew = gc_skew(seq, window=100)
print(f"GC skew: {skew}")
```

### ProtParam - 蛋白质分析

```python
from Bio.SeqUtils.ProtParam import ProteinAnalysis

protein_seq = "ACDEFGHIKLMNPQRSTVWY"
analyzed_seq = ProteinAnalysis(protein_seq)

# Molecular weight
print(f"MW: {analyzed_seq.molecular_weight():.2f} Da")

# Isoelectric point
print(f"pI: {analyzed_seq.isoelectric_point():.2f}")

# Amino acid composition
print(f"Composition: {analyzed_seq.get_amino_acids_percent()}")

# Instability index
print(f"Instability: {analyzed_seq.instability_index():.2f}")

# Aromaticity
print(f"Aromaticity: {analyzed_seq.aromaticity():.2f}")

# Secondary structure fraction
ss = analyzed_seq.secondary_structure_fraction()
print(f"Helix: {ss[0]:.2%}, Turn: {ss[1]:.2%}, Sheet: {ss[2]:.2%}")

# Extinction coefficient (assumes Cys reduced, no disulfide bonds)
print(f"Extinction coefficient: {analyzed_seq.molar_extinction_coefficient()}")

# Gravy (grand average of hydropathy)
print(f"GRAVY: {analyzed_seq.gravy():.3f}")
```

## 使用Bio.Restriction进行限制性分析

```python
from Bio import Restriction
from Bio.Seq import Seq

# Analyze sequence for restriction sites
seq = Seq("GAATTCATCGATCGATGAATTC")

# Use specific enzyme
ecori = Restriction.EcoRI
sites = ecori.search(seq)
print(f"EcoRI sites at: {sites}")

# Use multiple enzymes
rb = Restriction.RestrictionBatch(["EcoRI", "BamHI", "PstI"])
results = rb.search(seq)
for enzyme, sites in results.items():
    if sites:
        print(f"{enzyme}: {sites}")

# Get all enzymes that cut sequence
all_enzymes = Restriction.Analysis(rb, seq)
print(f"Cutting enzymes: {all_enzymes.with_sites()}")
```

## 序列翻译表

```python
from Bio.Data import CodonTable

# Standard genetic code
standard_table = CodonTable.unambiguous_dna_by_id[1]
print(standard_table)

# Mitochondrial code
mito_table = CodonTable.unambiguous_dna_by_id[2]

# Get specific codon
print(f"ATG codes for: {standard_table.forward_table['ATG']}")

# Get stop codons
print(f"Stop codons: {standard_table.stop_codons}")

# Get start codons
print(f"Start codons: {standard_table.start_codons}")
```

## 使用聚类分析Bio.Cluster

```python
from Bio.Cluster import kcluster
import numpy as np

# Sample data matrix (genes x conditions)
data = np.array([
    [1.2, 0.8, 0.5, 1.5],
    [0.9, 1.1, 0.7, 1.3],
    [0.2, 0.3, 2.1, 2.5],
    [0.1, 0.4, 2.3, 2.2],
])

# Perform k-means clustering
clusterid, error, nfound = kcluster(data, nclusters=2)
print(f"Cluster assignments: {clusterid}")
print(f"Error: {error}")
```

## GenomeDiagram 的基因组图

```python
from Bio.Graphics import GenomeDiagram
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio import SeqIO
from reportlab.lib import colors

# Read GenBank file
record = SeqIO.read("sequence.gb", "genbank")

# Create diagram
gd_diagram = GenomeDiagram.Diagram("Genome Diagram")
gd_track = gd_diagram.new_track(1, greytrack=True)
gd_feature_set = gd_track.new_set()

# Add features
for feature in record.features:
    if feature.type == "CDS":
        color = colors.blue
    elif feature.type == "gene":
        color = colors.lightblue
    else:
        color = colors.grey

    gd_feature_set.add_feature(
        feature,
        color=color,
        label=True,
        label_size=6,
        label_angle=45
    )

# Draw and save
gd_diagram.draw(format="linear", pagesize="A4", fragments=1)
gd_diagram.write("genome_diagram.pdf", "PDF")
```

## 与 Bio.pairwise2

的序列比较**注意**：Bio.pairwise2 已弃用。请改用 Bio.Align.PairwiseAligner（请参阅alignment.md）。

然而，对于旧代码：

```python
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

# Global alignment
alignments = pairwise2.align.globalxx("ACCGT", "ACGT")

# Print top alignments
for alignment in alignments[:3]:
    print(format_alignment(*alignment))
```

## 使用 PubChem

```python
from Bio import Entrez

Entrez.email = "your.email@example.com"

# Search PubChem
handle = Entrez.esearch(db="pccompound", term="aspirin")
result = Entrez.read(handle)
handle.close()

compound_id = result["IdList"][0]

# Get compound information
handle = Entrez.efetch(db="pccompound", id=compound_id, retmode="xml")
compound_data = handle.read()
handle.close()
```

## 序列功能Bio.SeqFeature

```python
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

# Create a feature
feature = SeqFeature(
    location=FeatureLocation(start=10, end=50),
    type="CDS",
    strand=1,
    qualifiers={"gene": ["ABC1"], "product": ["ABC protein"]}
)

# Add feature to record
record = SeqRecord(Seq("ATCG" * 20), id="seq1")
record.features.append(feature)

# Extract feature sequence
feature_seq = feature.extract(record.seq)
print(feature_seq)
```

## 序列歧义

```python
from Bio.Data import IUPACData

# DNA ambiguity codes
print(IUPACData.ambiguous_dna_letters)

# Protein ambiguity codes
print(IUPACData.ambiguous_protein_letters)

# Resolve ambiguous bases
print(IUPACData.ambiguous_dna_values["N"])  # Any base
print(IUPACData.ambiguous_dna_values["R"])  # A or G
```

## 质量得分 (FASTQ)

```python
from Bio import SeqIO

# Read FASTQ with quality scores
for record in SeqIO.parse("reads.fastq", "fastq"):
    print(f"ID: {record.id}")
    print(f"Sequence: {record.seq}")
    print(f"Quality: {record.letter_annotations['phred_quality']}")

    # Calculate average quality
    avg_quality = sum(record.letter_annotations['phred_quality']) / len(record)
    print(f"Average quality: {avg_quality:.2f}")

    # Filter by quality
    min_quality = min(record.letter_annotations['phred_quality'])
    if min_quality >= 20:
        print("High quality read")
```

## 最佳实践

1. **使用适当的模块** - 选择适合您的分析的工具
2. **处理伪计数** - 对于基序分析很重要
3. **验证输入数据** - 检查文件格式和数据质量
4. **考虑性能** - 某些操作可能是计算密集型的
5. **缓存结果** - 存储大型分析的中间结果
6. **使用正确的遗传密码** - 选择适当的翻译表
7. **文档参数** - 记录使用的阈值和设置
8. **验证统计结果** - 了解测试的局限性
9. **处理边缘情况** - 检查空结果或无效输入
10. **组合模块** - 一起利用多个 Biopython 工具

## 常见用例

### 查找 ORF

```python
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

def find_orfs(seq, min_length=100):
    """Find all ORFs in sequence."""
    orfs = []

    for strand, nuc in [(+1, seq), (-1, seq.reverse_complement())]:
        for frame in range(3):
            trans = nuc[frame:].translate()
            trans_len = len(trans)

            aa_start = 0
            while aa_start < trans_len:
                aa_end = trans.find("*", aa_start)
                if aa_end == -1:
                    aa_end = trans_len

                if aa_end - aa_start >= min_length // 3:
                    start = frame + aa_start * 3
                    end = frame + aa_end * 3
                    orfs.append({
                        'start': start,
                        'end': end,
                        'strand': strand,
                        'frame': frame,
                        'length': end - start,
                        'sequence': nuc[start:end]
                    })

                aa_start = aa_end + 1

    return orfs

# Use it
record = SeqIO.read("sequence.fasta", "fasta")
orfs = find_orfs(record.seq, min_length=300)
for orf in orfs:
    print(f"ORF: {orf['start']}-{orf['end']}, strand={orf['strand']}, length={orf['length']}")
```

### 分析密码子用法

```python
from Bio import SeqIO
from Bio.SeqUtils import CodonUsage

def analyze_codon_usage(fasta_file):
    """Analyze codon usage in coding sequences."""
    codon_counts = {}

    for record in SeqIO.parse(fasta_file, "fasta"):
        # Ensure sequence is multiple of 3
        seq = record.seq[:len(record.seq) - len(record.seq) % 3]

        # Count codons
        for i in range(0, len(seq), 3):
            codon = str(seq[i:i+3])
            codon_counts[codon] = codon_counts.get(codon, 0) + 1

    # Calculate frequencies
    total = sum(codon_counts.values())
    codon_freq = {k: v/total for k, v in codon_counts.items()}

    return codon_freq
```

### 计算序列复杂度

```python
def sequence_complexity(seq, k=2):
    """Calculate k-mer complexity (Shannon entropy)."""
    import math
    from collections import Counter

    # Generate k-mers
    kmers = [str(seq[i:i+k]) for i in range(len(seq) - k + 1)]

    # Count k-mers
    counts = Counter(kmers)
    total = len(kmers)

    # Calculate entropy
    entropy = 0
    for count in counts.values():
        freq = count / total
        entropy -= freq * math.log2(freq)

    # Normalize by maximum possible entropy
    max_entropy = math.log2(4 ** k)  # For DNA

    return entropy / max_entropy if max_entropy > 0 else 0

# Use it
from Bio.Seq import Seq
seq = Seq("ATCGATCGATCGATCG")
complexity = sequence_complexity(seq, k=2)
print(f"Sequence complexity: {complexity:.3f}")
```

### 提取启动子区域

```python
def extract_promoters(genbank_file, upstream=500):
    """Extract promoter regions upstream of genes."""
    from Bio import SeqIO

    record = SeqIO.read(genbank_file, "genbank")
    promoters = []

    for feature in record.features:
        if feature.type == "gene":
            if feature.strand == 1:
                # Forward strand
                start = max(0, feature.location.start - upstream)
                end = feature.location.start
            else:
                # Reverse strand
                start = feature.location.end
                end = min(len(record.seq), feature.location.end + upstream)

            promoter_seq = record.seq[start:end]
            if feature.strand == -1:
                promoter_seq = promoter_seq.reverse_complement()

            promoters.append({
                'gene': feature.qualifiers.get('gene', ['Unknown'])[0],
                'sequence': promoter_seq,
                'start': start,
                'end': end
            })

    return promoters
```
