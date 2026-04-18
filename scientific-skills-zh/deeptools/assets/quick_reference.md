# deepTools 快速参考

## 最常用命令

### BAM 到 bigWig（标准化）
```bash
bamCoverage --bam input.bam --outFileName output.bw \
    --normalizeUsing RPGC --effectiveGenomeSize 2913022398 \
    --binSize 10 --numberOfProcessors 8
```

### 比较两个 BAM 文件
```bash
bamCompare -b1 treatment.bam -b2 control.bam -o ratio.bw \
    --operation log2 --scaleFactorsMethod readCount
```

### 相关性热图
```bash
multiBamSummary bins --bamfiles *.bam -o counts.npz
plotCorrelation -in counts.npz --corMethod pearson \
    --whatToShow heatmap -o correlation.png
```

### TSS
```bash
computeMatrix reference-point -S signal.bw -R genes.bed \
    -b 3000 -a 3000 --referencePoint TSS -o matrix.gz

plotHeatmap -m matrix.gz -o heatmap.png
```

### ChIP 富集检查
```bash
plotFingerprint -b input.bam chip.bam -o fingerprint.png \
    --extendReads 200 --ignoreDuplicates
```

## 有效基因组大小

周围的热图有机体 |组装|尺寸|
|----------|----------|------|
|人类 | HG38 | 2913022398 |
|鼠标|毫米10 | 2652783500 |
|飞翔| DM6 | 142573017 |

## 常见归一化方法

- **RPGC**：1× 基因组覆盖率（需要 -- effectiveGenomeSize）
- **CPM**：每百万计数（对于固定 bin）
- **RPKM**：每百万每 kb 读取数（对于基因）

## 典型工作流程

1. **QC**：图指纹，图Correlation
2. **覆盖率**：bam标准化覆盖率
3. **比较**：bam比较治疗与对照
4. **可视化**：computeMatrix→plotHeatmap/plotProfile
