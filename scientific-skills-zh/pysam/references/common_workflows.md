# 使用 Pysam 的常见生物信息学工作流程

## 概述

本文档提供使用 pysam 的常见生物信息学工作流程的实际示例，演示如何组合不同的文件类型和操作。

## 质量控制工作流程

### 计算 BAM统计

```python
import pysam

def calculate_bam_stats(bam_file):
    """Calculate basic statistics for BAM file."""
    samfile = pysam.AlignmentFile(bam_file, "rb")

    stats = {
        "total_reads": 0,
        "mapped_reads": 0,
        "unmapped_reads": 0,
        "paired_reads": 0,
        "proper_pairs": 0,
        "duplicates": 0,
        "total_bases": 0,
        "mapped_bases": 0
    }

    for read in samfile.fetch(until_eof=True):
        stats["total_reads"] += 1

        if read.is_unmapped:
            stats["unmapped_reads"] += 1
        else:
            stats["mapped_reads"] += 1
            stats["mapped_bases"] += read.query_alignment_length

        if read.is_paired:
            stats["paired_reads"] += 1
            if read.is_proper_pair:
                stats["proper_pairs"] += 1

        if read.is_duplicate:
            stats["duplicates"] += 1

        stats["total_bases"] += read.query_length

    samfile.close()

    # Calculate derived statistics
    stats["mapping_rate"] = stats["mapped_reads"] / stats["total_reads"] if stats["total_reads"] > 0 else 0
    stats["duplication_rate"] = stats["duplicates"] / stats["total_reads"] if stats["total_reads"] > 0 else 0

    return stats
```

### 检查参考一致性

```python
def check_bam_reference_consistency(bam_file, fasta_file):
    """Verify that BAM reads match reference genome."""
    samfile = pysam.AlignmentFile(bam_file, "rb")
    fasta = pysam.FastaFile(fasta_file)

    mismatches = 0
    total_checked = 0

    for read in samfile.fetch():
        if read.is_unmapped:
            continue

        # Get reference sequence for aligned region
        ref_seq = fasta.fetch(
            read.reference_name,
            read.reference_start,
            read.reference_end
        )

        # Get read sequence aligned to reference
        aligned_pairs = read.get_aligned_pairs(with_seq=True)

        for query_pos, ref_pos, ref_base in aligned_pairs:
            if query_pos is not None and ref_pos is not None and ref_base is not None:
                read_base = read.query_sequence[query_pos]
                if read_base.upper() != ref_base.upper():
                    mismatches += 1
                total_checked += 1

        if total_checked >= 10000:  # Sample first 10k positions
            break

    samfile.close()
    fasta.close()

    error_rate = mismatches / total_checked if total_checked > 0 else 0
    return {
        "positions_checked": total_checked,
        "mismatches": mismatches,
        "error_rate": error_rate
    }
```

## 覆盖率分析

### 计算每个碱基的覆盖率

```python
def calculate_coverage(bam_file, chrom, start, end):
    """Calculate coverage for each position in region."""
    samfile = pysam.AlignmentFile(bam_file, "rb")

    # Initialize coverage array
    length = end - start
    coverage = [0] * length

    # Count coverage at each position
    for pileupcolumn in samfile.pileup(chrom, start, end):
        if start <= pileupcolumn.pos < end:
            coverage[pileupcolumn.pos - start] = pileupcolumn.nsegments

    samfile.close()

    return coverage
```

### 识别低覆盖率区域

```python
def find_low_coverage_regions(bam_file, chrom, start, end, min_coverage=10):
    """Find regions with coverage below threshold."""
    samfile = pysam.AlignmentFile(bam_file, "rb")

    low_coverage_regions = []
    in_low_region = False
    region_start = None

    for pileupcolumn in samfile.pileup(chrom, start, end):
        pos = pileupcolumn.pos
        if pos < start or pos >= end:
            continue

        coverage = pileupcolumn.nsegments

        if coverage < min_coverage:
            if not in_low_region:
                region_start = pos
                in_low_region = True
        else:
            if in_low_region:
                low_coverage_regions.append((region_start, pos))
                in_low_region = False

    # Close last region if still open
    if in_low_region:
        low_coverage_regions.append((region_start, end))

    samfile.close()

    return low_coverage_regions
```

### 计算覆盖率统计

```python
def coverage_statistics(bam_file, chrom, start, end):
    """Calculate coverage statistics for region."""
    samfile = pysam.AlignmentFile(bam_file, "rb")

    coverages = []

    for pileupcolumn in samfile.pileup(chrom, start, end):
        if start <= pileupcolumn.pos < end:
            coverages.append(pileupcolumn.nsegments)

    samfile.close()

    if not coverages:
        return None

    coverages.sort()
    n = len(coverages)

    return {
        "mean": sum(coverages) / n,
        "median": coverages[n // 2],
        "min": coverages[0],
        "max": coverages[-1],
        "positions": n
    }
```

## 变异分析

### 提取区域中的变异

```python
def extract_variants_in_genes(vcf_file, bed_file):
    """Extract variants overlapping gene regions."""
    vcf = pysam.VariantFile(vcf_file)
    bed = pysam.TabixFile(bed_file)

    variants_by_gene = {}

    for gene in bed.fetch(parser=pysam.asBed()):
        gene_name = gene.name
        variants_by_gene[gene_name] = []

        # Find variants in gene region
        for variant in vcf.fetch(gene.contig, gene.start, gene.end):
            variant_info = {
                "chrom": variant.chrom,
                "pos": variant.pos,
                "ref": variant.ref,
                "alt": variant.alts,
                "qual": variant.qual
            }
            variants_by_gene[gene_name].append(variant_info)

    vcf.close()
    bed.close()

    return variants_by_gene
```

### 注释有覆盖的变体

```python
def annotate_variants_with_coverage(vcf_file, bam_file, output_file):
    """Add coverage information to variants."""
    vcf = pysam.VariantFile(vcf_file)
    samfile = pysam.AlignmentFile(bam_file, "rb")

    # Add DP to header if not present
    if "DP" not in vcf.header.info:
        vcf.header.info.add("DP", "1", "Integer", "Total Depth from BAM")

    outvcf = pysam.VariantFile(output_file, "w", header=vcf.header)

    for variant in vcf:
        # Get coverage at variant position
        coverage = samfile.count(
            variant.chrom,
            variant.pos - 1,  # Convert to 0-based
            variant.pos
        )

        # Add to INFO field
        variant.info["DP"] = coverage

        outvcf.write(variant)

    vcf.close()
    samfile.close()
    outvcf.close()
```

### 通过读取支持过滤变体

```python
def filter_variants_by_support(vcf_file, bam_file, output_file, min_alt_reads=3):
    """Filter variants requiring minimum alternate allele support."""
    vcf = pysam.VariantFile(vcf_file)
    samfile = pysam.AlignmentFile(bam_file, "rb")
    outvcf = pysam.VariantFile(output_file, "w", header=vcf.header)

    for variant in vcf:
        # Count reads supporting each allele
        allele_counts = {variant.ref: 0}
        for alt in variant.alts:
            allele_counts[alt] = 0

        # Pileup at variant position
        for pileupcolumn in samfile.pileup(
            variant.chrom,
            variant.pos - 1,
            variant.pos
        ):
            if pileupcolumn.pos == variant.pos - 1:  # 0-based
                for pileupread in pileupcolumn.pileups:
                    if not pileupread.is_del and not pileupread.is_refskip:
                        base = pileupread.alignment.query_sequence[
                            pileupread.query_position
                        ]
                        if base in allele_counts:
                            allele_counts[base] += 1

        # Check if any alt allele has sufficient support
        has_support = any(
            allele_counts.get(alt, 0) >= min_alt_reads
            for alt in variant.alts
        )

        if has_support:
            outvcf.write(variant)

    vcf.close()
    samfile.close()
    outvcf.close()
```

## 序列提取

### 提取周围的序列变体

```python
def extract_variant_contexts(vcf_file, fasta_file, output_file, window=50):
    """Extract reference sequences around variants."""
    vcf = pysam.VariantFile(vcf_file)
    fasta = pysam.FastaFile(fasta_file)

    with open(output_file, 'w') as out:
        for variant in vcf:
            # Get sequence context
            start = max(0, variant.pos - window - 1)  # Convert to 0-based
            end = variant.pos + window

            context = fasta.fetch(variant.chrom, start, end)

            # Mark variant position
            var_pos_in_context = variant.pos - 1 - start

            out.write(f">{variant.chrom}:{variant.pos} {variant.ref}>{variant.alts}\n")
            out.write(context[:var_pos_in_context].lower())
            out.write(context[var_pos_in_context:var_pos_in_context+len(variant.ref)].upper())
            out.write(context[var_pos_in_context+len(variant.ref):].lower())
            out.write("\n")

    vcf.close()
    fasta.close()
```

### 提取基因序列

```python
def extract_gene_sequences(bed_file, fasta_file, output_fasta):
    """Extract sequences for genes from BED file."""
    bed = pysam.TabixFile(bed_file)
    fasta = pysam.FastaFile(fasta_file)

    with open(output_fasta, 'w') as out:
        for gene in bed.fetch(parser=pysam.asBed()):
            sequence = fasta.fetch(gene.contig, gene.start, gene.end)

            # Handle strand
            if hasattr(gene, 'strand') and gene.strand == '-':
                # Reverse complement
                complement = str.maketrans("ATGCatgcNn", "TACGtacgNn")
                sequence = sequence.translate(complement)[::-1]

            out.write(f">{gene.name} {gene.contig}:{gene.start}-{gene.end}\n")

            # Write sequence in 60-character lines
            for i in range(0, len(sequence), 60):
                out.write(sequence[i:i+60] + "\n")

    bed.close()
    fasta.close()
```

## 读取过滤和子集

### 按区域过滤BAM并质量

```python
def filter_bam(input_bam, output_bam, chrom, start, end, min_mapq=20):
    """Filter BAM file by region and mapping quality."""
    infile = pysam.AlignmentFile(input_bam, "rb")
    outfile = pysam.AlignmentFile(output_bam, "wb", template=infile)

    for read in infile.fetch(chrom, start, end):
        if read.mapping_quality >= min_mapq and not read.is_duplicate:
            outfile.write(read)

    infile.close()
    outfile.close()

    # Create index
    pysam.index(output_bam)
```

### 特定变体的提取读取

```python
def extract_reads_at_variants(bam_file, vcf_file, output_bam, window=100):
    """Extract reads overlapping variant positions."""
    samfile = pysam.AlignmentFile(bam_file, "rb")
    vcf = pysam.VariantFile(vcf_file)
    outfile = pysam.AlignmentFile(output_bam, "wb", template=samfile)

    # Collect all reads (using set to avoid duplicates)
    reads_to_keep = set()

    for variant in vcf:
        start = max(0, variant.pos - window - 1)
        end = variant.pos + window

        for read in samfile.fetch(variant.chrom, start, end):
            reads_to_keep.add(read.query_name)

    # Write all reads
    samfile.close()
    samfile = pysam.AlignmentFile(bam_file, "rb")

    for read in samfile.fetch(until_eof=True):
        if read.query_name in reads_to_keep:
            outfile.write(read)

    samfile.close()
    vcf.close()
    outfile.close()

    pysam.index(output_bam)
```

## 集成工作流程

### 创建覆盖率跟踪BAM

```python
def create_coverage_bedgraph(bam_file, output_file, chrom=None):
    """Create bedGraph coverage track from BAM."""
    samfile = pysam.AlignmentFile(bam_file, "rb")

    chroms = [chrom] if chrom else samfile.references

    with open(output_file, 'w') as out:
        out.write("track type=bedGraph name=\"Coverage\"\n")

        for chrom in chroms:
            current_cov = None
            region_start = None

            for pileupcolumn in samfile.pileup(chrom):
                pos = pileupcolumn.pos
                cov = pileupcolumn.nsegments

                if cov != current_cov:
                    # Write previous region
                    if current_cov is not None:
                        out.write(f"{chrom}\t{region_start}\t{pos}\t{current_cov}\n")

                    # Start new region
                    current_cov = cov
                    region_start = pos

            # Write final region
            if current_cov is not None:
                out.write(f"{chrom}\t{region_start}\t{pos+1}\t{current_cov}\n")

    samfile.close()
```

### 合并多个 VCF 文件

```python
def merge_vcf_samples(vcf_files, output_file):
    """Merge multiple single-sample VCFs."""
    # Open all input files
    vcf_readers = [pysam.VariantFile(f) for f in vcf_files]

    # Create merged header
    merged_header = vcf_readers[0].header.copy()
    for vcf in vcf_readers[1:]:
        for sample in vcf.header.samples:
            merged_header.samples.add(sample)

    outvcf = pysam.VariantFile(output_file, "w", header=merged_header)

    # Get all variant positions
    all_variants = {}
    for vcf in vcf_readers:
        for variant in vcf:
            key = (variant.chrom, variant.pos, variant.ref, variant.alts)
            if key not in all_variants:
                all_variants[key] = []
            all_variants[key].append(variant)

    # Write merged variants
    for key, variants in sorted(all_variants.items()):
        # Create merged record from first variant
        merged = outvcf.new_record(
            contig=variants[0].chrom,
            start=variants[0].start,
            stop=variants[0].stop,
            alleles=variants[0].alleles
        )

        # Add genotypes from all samples
        for variant in variants:
            for sample in variant.samples:
                merged.samples[sample].update(variant.samples[sample])

        outvcf.write(merged)

    # Close all files
    for vcf in vcf_readers:
        vcf.close()
    outvcf.close()
```

## 工作流程的性能提示

1. **对所有随机访问操作使用索引文件**
2. **分析多个独立区域时并行处理区域**
3. **尽可能流式传输数据** - 避免将整个文件加载到内存中
4. **明确关闭文件**以释放资源
5. **使用`until_eof=True`**对整个文件
6进行顺序处理。 **对同一文件进行批量操作**，以最大限度地减少 I/O
7. **考虑高覆盖率区域 
8 上的堆积操作的内存使用情况**。 **当只需要计数时使用 count()而不是 pileup()**

## 常见集成模式

1. **BAM + Reference**：验证比对，提取比对序列
2. **BAM + VCF**：验证变异，计算等位基因频率
3. **VCF + BED**：用基因/区域信息
4注释变体。 **BAM + BED**：计算特定区域的覆盖统计数据
5. **FASTA + VCF**：提取变体上下文序列
6. **多个 BAM**：比较样本 
7 的覆盖范围或变体。 **BAM + FASTQ**：提取未对齐的读数以重新对齐
