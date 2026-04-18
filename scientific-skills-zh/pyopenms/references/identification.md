# 肽和蛋白质鉴定

## 概述

PyOpenMS 通过与搜索引擎集成支持肽/蛋白质鉴定，并提供用于后处理鉴定结果的工具，包括 FDR 控制、蛋白质推理和注释。

## 支持的搜索引擎

PyOpenMS 与这些搜索引擎集成：

- **Comet**：快速串联 MS search
- **Mascot**：商业搜索引擎
- **MSGFPlus**：基于谱概率的搜索
- **XTandem**：开源搜索工具
- **OMSSA**：NCBI 搜索引擎
- **Myrimatch**：高通量搜索
- **MSFragger**：超快速搜索

## 读取鉴定数据

### idXML格式

```python
import pyopenms as ms

# Load identification results
protein_ids = []
peptide_ids = []

ms.IdXMLFile().load("identifications.idXML", protein_ids, peptide_ids)

print(f"Protein identifications: {len(protein_ids)}")
print(f"Peptide identifications: {len(peptide_ids)}")
```

### 获取肽鉴定

```python
# Iterate through peptide IDs
for peptide_id in peptide_ids:
    # Spectrum metadata
    print(f"RT: {peptide_id.getRT():.2f}")
    print(f"m/z: {peptide_id.getMZ():.4f}")

    # Get peptide hits (ranked by score)
    hits = peptide_id.getHits()
    print(f"Number of hits: {len(hits)}")

    for hit in hits:
        sequence = hit.getSequence()
        print(f"  Sequence: {sequence.toString()}")
        print(f"  Score: {hit.getScore()}")
        print(f"  Charge: {hit.getCharge()}")
        print(f"  Mass error (ppm): {hit.getMetaValue('mass_error_ppm')}")

        # Get modifications
        if sequence.isModified():
            for i in range(sequence.size()):
                residue = sequence.getResidue(i)
                if residue.isModified():
                    print(f"    Modification at position {i}: {residue.getModificationName()}")
```

### 获取蛋白质标识

```python
# Access protein-level information
for protein_id in protein_ids:
    # Search parameters
    search_params = protein_id.getSearchParameters()
    print(f"Search engine: {protein_id.getSearchEngine()}")
    print(f"Database: {search_params.db}")

    # Protein hits
    hits = protein_id.getHits()
    for hit in hits:
        print(f"  Accession: {hit.getAccession()}")
        print(f"  Score: {hit.getScore()}")
        print(f"  Coverage: {hit.getCoverage()}")
        print(f"  Sequence: {hit.getSequence()}")
```

## 错误发现率 (FDR)

### FDR 过滤

应用 FDR 过滤来控制误报：

```python
# Create FDR object
fdr = ms.FalseDiscoveryRate()

# Apply FDR at PSM level
fdr.apply(peptide_ids)

# Filter by FDR threshold
fdr_threshold = 0.01  # 1% FDR
filtered_peptide_ids = []

for peptide_id in peptide_ids:
    # Keep hits below FDR threshold
    filtered_hits = []
    for hit in peptide_id.getHits():
        if hit.getScore() <= fdr_threshold:  # Lower score = better
            filtered_hits.append(hit)

    if filtered_hits:
        peptide_id.setHits(filtered_hits)
        filtered_peptide_ids.append(peptide_id)

print(f"Peptides passing FDR: {len(filtered_peptide_ids)}")
```

### 分数转换

转换分数到 q 值：

```python
# Apply score transformation
fdr.apply(peptide_ids)

# Access q-values
for peptide_id in peptide_ids:
    for hit in peptide_id.getHits():
        q_value = hit.getMetaValue("q-value")
        print(f"Sequence: {hit.getSequence().toString()}, q-value: {q_value}")
```

## 蛋白质推断 

### ID Mapper

将肽标识映射到蛋白质：

```python
# Create mapper
mapper = ms.IDMapper()

# Map to features
feature_map = ms.FeatureMap()
ms.FeatureXMLFile().load("features.featureXML", feature_map)

# Annotate features with IDs
mapper.annotate(feature_map, peptide_ids, protein_ids)

# Check annotated features
for feature in feature_map:
    pep_ids = feature.getPeptideIdentifications()
    if pep_ids:
        for pep_id in pep_ids:
            for hit in pep_id.getHits():
                print(f"Feature {feature.getMZ():.4f}: {hit.getSequence().toString()}")
```

### 蛋白质分组

按共享对蛋白质进行分组肽：

```python
# Create protein inference algorithm
inference = ms.BasicProteinInferenceAlgorithm()

# Run inference
inference.run(peptide_ids, protein_ids)

# Access protein groups
for protein_id in protein_ids:
    hits = protein_id.getHits()
    if len(hits) > 1:
        print("Protein group:")
        for hit in hits:
            print(f"  {hit.getAccession()}")
```

## 肽序列处理

### AASequence 对象

使用肽序列：

```python
# Create peptide sequence
seq = ms.AASequence.fromString("PEPTIDE")

print(f"Sequence: {seq.toString()}")
print(f"Monoisotopic mass: {seq.getMonoWeight():.4f}")
print(f"Average mass: {seq.getAverageWeight():.4f}")
print(f"Length: {seq.size()}")

# Access individual amino acids
for i in range(seq.size()):
    residue = seq.getResidue(i)
    print(f"Position {i}: {residue.getOneLetterCode()}, mass: {residue.getMonoWeight():.4f}")
```

### 修饰序列

处理翻译后修改：

```python
# Sequence with modifications
mod_seq = ms.AASequence.fromString("PEPTIDEM(Oxidation)K")

print(f"Modified sequence: {mod_seq.toString()}")
print(f"Mass with mods: {mod_seq.getMonoWeight():.4f}")

# Check if modified
print(f"Is modified: {mod_seq.isModified()}")

# Get modification info
for i in range(mod_seq.size()):
    residue = mod_seq.getResidue(i)
    if residue.isModified():
        print(f"Residue {residue.getOneLetterCode()} at position {i}")
        print(f"  Modification: {residue.getModificationName()}")
```

### 肽消化

模拟酶消化：

```python
# Create digestion enzyme
enzyme = ms.ProteaseDigestion()
enzyme.setEnzyme("Trypsin")

# Set missed cleavages
enzyme.setMissedCleavages(2)

# Digest protein sequence
protein_seq = "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL"

# Get peptides
peptides = []
enzyme.digest(ms.AASequence.fromString(protein_seq), peptides)

print(f"Generated {len(peptides)} peptides")
for peptide in peptides[:5]:  # Show first 5
    print(f"  {peptide.toString()}, mass: {peptide.getMonoWeight():.2f}")
```

## 理论谱图生成

### 碎片离子计算

生成理论碎片离子：

```python
# Create peptide
peptide = ms.AASequence.fromString("PEPTIDE")

# Generate b and y ions
fragments = []
ms.TheoreticalSpectrumGenerator().getSpectrum(fragments, peptide, 1, 1)

print(f"Generated {fragments.size()} fragment ions")

# Access fragments
mz, intensity = fragments.get_peaks()
for m, i in zip(mz[:10], intensity[:10]):  # Show first 10
    print(f"m/z: {m:.4f}, intensity: {i}")
```

## 完整的鉴定工作流程

### 端到端示例

```python
import pyopenms as ms

def identification_workflow(spectrum_file, fasta_file, output_file):
    """
    Complete identification workflow with FDR control.

    Args:
        spectrum_file: Input mzML file
        fasta_file: Protein database (FASTA)
        output_file: Output idXML file
    """

    # Step 1: Load spectra
    exp = ms.MSExperiment()
    ms.MzMLFile().load(spectrum_file, exp)
    print(f"Loaded {exp.getNrSpectra()} spectra")

    # Step 2: Configure search parameters
    search_params = ms.SearchParameters()
    search_params.db = fasta_file
    search_params.precursor_mass_tolerance = 10.0  # ppm
    search_params.fragment_mass_tolerance = 0.5  # Da
    search_params.enzyme = "Trypsin"
    search_params.missed_cleavages = 2
    search_params.modifications = ["Oxidation (M)", "Carbamidomethyl (C)"]

    # Step 3: Run search (example with Comet adapter)
    # Note: Requires search engine to be installed
    # comet = ms.CometAdapter()
    # protein_ids, peptide_ids = comet.search(exp, search_params)

    # For this example, load pre-computed results
    protein_ids = []
    peptide_ids = []
    ms.IdXMLFile().load("raw_identifications.idXML", protein_ids, peptide_ids)

    print(f"Initial peptide IDs: {len(peptide_ids)}")

    # Step 4: Apply FDR filtering
    fdr = ms.FalseDiscoveryRate()
    fdr.apply(peptide_ids)

    # Filter by 1% FDR
    filtered_peptide_ids = []
    for peptide_id in peptide_ids:
        filtered_hits = []
        for hit in peptide_id.getHits():
            q_value = hit.getMetaValue("q-value")
            if q_value <= 0.01:
                filtered_hits.append(hit)

        if filtered_hits:
            peptide_id.setHits(filtered_hits)
            filtered_peptide_ids.append(peptide_id)

    print(f"Peptides after FDR (1%): {len(filtered_peptide_ids)}")

    # Step 5: Protein inference
    inference = ms.BasicProteinInferenceAlgorithm()
    inference.run(filtered_peptide_ids, protein_ids)

    print(f"Identified proteins: {len(protein_ids)}")

    # Step 6: Save results
    ms.IdXMLFile().store(output_file, protein_ids, filtered_peptide_ids)
    print(f"Results saved to {output_file}")

    return protein_ids, filtered_peptide_ids

# Run workflow
protein_ids, peptide_ids = identification_workflow(
    "spectra.mzML",
    "database.fasta",
    "identifications_fdr.idXML"
)
```

## 谱库搜索

### 谱库匹配

```python
# Load spectral library
library = ms.MSPFile()
library_spectra = []
library.load("spectral_library.msp", library_spectra)

# Load experimental spectra
exp = ms.MSExperiment()
ms.MzMLFile().load("data.mzML", exp)

# Compare spectra
spectra_compare = ms.SpectraSTSimilarityScore()

for exp_spec in exp:
    if exp_spec.getMSLevel() == 2:
        best_match_score = 0
        best_match_lib = None

        for lib_spec in library_spectra:
            score = spectra_compare.operator()(exp_spec, lib_spec)
            if score > best_match_score:
                best_match_score = score
                best_match_lib = lib_spec

        if best_match_score > 0.7:  # Threshold
            print(f"Match found: score {best_match_score:.3f}")
```

## 最佳实践

### 诱饵数据库

使用目标诱饵方法进行FDR计算：

```python
# Generate decoy database
decoy_generator = ms.DecoyGenerator()

# Load target database
fasta_entries = []
ms.FASTAFile().load("target.fasta", fasta_entries)

# Generate decoys
decoy_entries = []
for entry in fasta_entries:
    decoy_entry = decoy_generator.reverseProtein(entry)
    decoy_entries.append(decoy_entry)

# Save combined database
all_entries = fasta_entries + decoy_entries
ms.FASTAFile().store("target_decoy.fasta", all_entries)
```

### 分数解读

了解不同分数类型发动机：

```python
# Interpret scores based on search engine
for peptide_id in peptide_ids:
    search_engine = peptide_id.getIdentifier()

    for hit in peptide_id.getHits():
        score = hit.getScore()

        # Score interpretation varies by engine
        if "Comet" in search_engine:
            # Comet: higher E-value = worse
            print(f"E-value: {score}")
        elif "Mascot" in search_engine:
            # Mascot: higher score = better
            print(f"Ion score: {score}")
```
