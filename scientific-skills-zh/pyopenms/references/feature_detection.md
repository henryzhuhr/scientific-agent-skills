# 特征检测和链接

## 概述

特征检测可识别 LC-MS 数据中的持续信号（色谱峰）。特征链接结合了多个样品的特征进行定量比较。

## 特征检测基础

A 特征表示具有以下特征的色谱峰：
- m/z 值（质荷比）
- 保留时间 (RT)
- 强度
- 质量得分
- 凸船体（RT-m/z 空间中的空间范围）

## 特征查找

### 特征查找器倍数 (FFM)

质心数据中特征检测的标准算法：

```python
import pyopenms as ms

# Load centroided data
exp = ms.MSExperiment()
ms.MzMLFile().load("centroided.mzML", exp)

# Create feature finder
ff = ms.FeatureFinder()

# Get default parameters
params = ff.getParameters("centroided")

# Modify key parameters
params.setValue("mass_trace:mz_tolerance", 10.0)  # ppm
params.setValue("mass_trace:min_spectra", 7)  # Min scans per feature
params.setValue("isotopic_pattern:charge_low", 1)
params.setValue("isotopic_pattern:charge_high", 4)

# Run feature detection
features = ms.FeatureMap()
ff.run("centroided", exp, features, params, ms.FeatureMap())

print(f"Detected {features.size()} features")

# Save features
ms.FeatureXMLFile().store("features.featureXML", features)
```

### 代谢组学特征查找器

针对小型进行优化分子：

```python
# Create feature finder for metabolomics
ff = ms.FeatureFinder()

# Get metabolomics-specific parameters
params = ff.getParameters("centroided")

# Configure for metabolomics
params.setValue("mass_trace:mz_tolerance", 5.0)  # Lower tolerance
params.setValue("mass_trace:min_spectra", 5)
params.setValue("isotopic_pattern:charge_low", 1)  # Mostly singly charged
params.setValue("isotopic_pattern:charge_high", 2)

# Run detection
features = ms.FeatureMap()
ff.run("centroided", exp, features, params, ms.FeatureMap())
```

## 访问特征数据

### 迭代特征

```python
# Load features
feature_map = ms.FeatureMap()
ms.FeatureXMLFile().load("features.featureXML", feature_map)

# Access individual features
for feature in feature_map:
    print(f"m/z: {feature.getMZ():.4f}")
    print(f"RT: {feature.getRT():.2f}")
    print(f"Intensity: {feature.getIntensity():.0f}")
    print(f"Charge: {feature.getCharge()}")
    print(f"Quality: {feature.getOverallQuality():.3f}")
    print(f"Width (RT): {feature.getWidth():.2f}")

    # Get convex hull
    hull = feature.getConvexHull()
    print(f"Hull points: {hull.getHullPoints().size()}")
```

### 特征下属（同位素模式）

```python
# Access isotopic pattern
for feature in feature_map:
    # Get subordinate features (isotopes)
    subordinates = feature.getSubordinates()

    if subordinates:
        print(f"Main feature m/z: {feature.getMZ():.4f}")
        for sub in subordinates:
            print(f"  Isotope m/z: {sub.getMZ():.4f}")
            print(f"  Isotope intensity: {sub.getIntensity():.0f}")
```

### 导出到 Pandas

```python
import pandas as pd

# Convert to DataFrame
df = feature_map.get_df()

print(df.columns)
# Typical columns: RT, mz, intensity, charge, quality

# Analyze features
print(f"Mean intensity: {df['intensity'].mean()}")
print(f"RT range: {df['RT'].min():.1f} - {df['RT'].max():.1f}")
```

## 功能链接

### 地图对齐

在链接前对齐保留时间：

```python
# Load multiple feature maps
fm1 = ms.FeatureMap()
fm2 = ms.FeatureMap()
ms.FeatureXMLFile().load("sample1.featureXML", fm1)
ms.FeatureXMLFile().load("sample2.featureXML", fm2)

# Create aligner
aligner = ms.MapAlignmentAlgorithmPoseClustering()

# Align maps
fm_aligned = []
transformations = []
aligner.align([fm1, fm2], fm_aligned, transformations)
```

### 功能链接算法

跨链接功能样本：

```python
# Create feature grouping algorithm
grouper = ms.FeatureGroupingAlgorithmQT()

# Configure parameters
params = grouper.getParameters()
params.setValue("distance_RT:max_difference", 30.0)  # Max RT difference (s)
params.setValue("distance_MZ:max_difference", 10.0)  # Max m/z difference (ppm)
params.setValue("distance_MZ:unit", "ppm")
grouper.setParameters(params)

# Prepare feature maps
feature_maps = [fm1, fm2, fm3]

# Create consensus map
consensus_map = ms.ConsensusMap()

# Link features
grouper.group(feature_maps, consensus_map)

print(f"Created {consensus_map.size()} consensus features")

# Save consensus map
ms.ConsensusXMLFile().store("consensus.consensusXML", consensus_map)
```

## 共识功能

### 访问共识数据

```python
# Load consensus map
consensus_map = ms.ConsensusMap()
ms.ConsensusXMLFile().load("consensus.consensusXML", consensus_map)

# Iterate through consensus features
for cons_feature in consensus_map:
    print(f"Consensus m/z: {cons_feature.getMZ():.4f}")
    print(f"Consensus RT: {cons_feature.getRT():.2f}")

    # Get features from individual maps
    for handle in cons_feature.getFeatureList():
        map_idx = handle.getMapIndex()
        intensity = handle.getIntensity()
        print(f"  Sample {map_idx}: intensity {intensity:.0f}")
```

### 共识图元数据

```python
# Access file descriptions (map metadata)
file_descriptions = consensus_map.getColumnHeaders()

for map_idx, description in file_descriptions.items():
    print(f"Map {map_idx}:")
    print(f"  Filename: {description.filename}")
    print(f"  Label: {description.label}")
    print(f"  Size: {description.size}")
```

## 加合物检测

识别同一分子的不同电离形式：

```python
# Create adduct detector
adduct_detector = ms.MetaboliteAdductDecharger()

# Configure parameters
params = adduct_detector.getParameters()
params.setValue("potential_adducts", "[M+H]+,[M+Na]+,[M+K]+,[M-H]-")
params.setValue("charge_min", 1)
params.setValue("charge_max", 1)
params.setValue("max_neutrals", 1)
adduct_detector.setParameters(params)

# Detect adducts
feature_map_out = ms.FeatureMap()
adduct_detector.compute(feature_map, feature_map_out, ms.ConsensusMap())
```

## 完整的特征检测工作流程

### 端到端示例

```python
import pyopenms as ms

def feature_detection_workflow(input_files, output_consensus):
    """
    Complete workflow: feature detection and linking across samples.

    Args:
        input_files: List of mzML file paths
        output_consensus: Output consensusXML file path
    """

    feature_maps = []

    # Step 1: Detect features in each file
    for mzml_file in input_files:
        print(f"Processing {mzml_file}...")

        # Load experiment
        exp = ms.MSExperiment()
        ms.MzMLFile().load(mzml_file, exp)

        # Find features
        ff = ms.FeatureFinder()
        params = ff.getParameters("centroided")
        params.setValue("mass_trace:mz_tolerance", 10.0)
        params.setValue("mass_trace:min_spectra", 7)

        features = ms.FeatureMap()
        ff.run("centroided", exp, features, params, ms.FeatureMap())

        # Store filename in feature map
        features.setPrimaryMSRunPath([mzml_file.encode()])

        feature_maps.append(features)
        print(f"  Found {features.size()} features")

    # Step 2: Align retention times
    print("Aligning retention times...")
    aligner = ms.MapAlignmentAlgorithmPoseClustering()
    aligned_maps = []
    transformations = []
    aligner.align(feature_maps, aligned_maps, transformations)

    # Step 3: Link features
    print("Linking features across samples...")
    grouper = ms.FeatureGroupingAlgorithmQT()
    params = grouper.getParameters()
    params.setValue("distance_RT:max_difference", 30.0)
    params.setValue("distance_MZ:max_difference", 10.0)
    params.setValue("distance_MZ:unit", "ppm")
    grouper.setParameters(params)

    consensus_map = ms.ConsensusMap()
    grouper.group(aligned_maps, consensus_map)

    # Save results
    ms.ConsensusXMLFile().store(output_consensus, consensus_map)

    print(f"Created {consensus_map.size()} consensus features")
    print(f"Results saved to {output_consensus}")

    return consensus_map

# Run workflow
input_files = ["sample1.mzML", "sample2.mzML", "sample3.mzML"]
consensus = feature_detection_workflow(input_files, "consensus.consensusXML")
```

## 特征过滤

### 过滤依据质量

```python
# Filter features by quality score
filtered_features = ms.FeatureMap()

for feature in feature_map:
    if feature.getOverallQuality() > 0.5:  # Quality threshold
        filtered_features.push_back(feature)

print(f"Kept {filtered_features.size()} high-quality features")
```

### 按强度过滤

```python
# Keep only intense features
min_intensity = 10000

filtered_features = ms.FeatureMap()
for feature in feature_map:
    if feature.getIntensity() >= min_intensity:
        filtered_features.push_back(feature)
```

### 按m/z范围过滤

```python
# Extract features in specific m/z range
mz_min = 200.0
mz_max = 800.0

filtered_features = ms.FeatureMap()
for feature in feature_map:
    mz = feature.getMZ()
    if mz_min <= mz <= mz_max:
        filtered_features.push_back(feature)
```

## 特征注释

### 添加标识信息

```python
# Annotate features with peptide identifications
# Load identifications
protein_ids = []
peptide_ids = []
ms.IdXMLFile().load("identifications.idXML", protein_ids, peptide_ids)

# Create ID mapper
mapper = ms.IDMapper()

# Map IDs to features
mapper.annotate(feature_map, peptide_ids, protein_ids)

# Check annotations
for feature in feature_map:
    peptide_ids_for_feature = feature.getPeptideIdentifications()
    if peptide_ids_for_feature:
        print(f"Feature at {feature.getMZ():.4f} m/z identified")
```

## 最佳实践

### 参数优化

针对您的数据类型优化参数：

```python
# Test different tolerance values
mz_tolerances = [5.0, 10.0, 20.0]  # ppm

for tol in mz_tolerances:
    ff = ms.FeatureFinder()
    params = ff.getParameters("centroided")
    params.setValue("mass_trace:mz_tolerance", tol)

    features = ms.FeatureMap()
    ff.run("centroided", exp, features, params, ms.FeatureMap())

    print(f"Tolerance {tol} ppm: {features.size()} features")
```

### 视觉检查

的导出功能可视化：

```python
# Convert to DataFrame for plotting
df = feature_map.get_df()

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.scatter(df['RT'], df['mz'], s=df['intensity']/1000, alpha=0.5)
plt.xlabel('Retention Time (s)')
plt.ylabel('m/z')
plt.title('Feature Map')
plt.colorbar(label='Intensity (scaled)')
plt.show()
```
