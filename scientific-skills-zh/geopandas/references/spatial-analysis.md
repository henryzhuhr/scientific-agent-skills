# 空间分析

## 属性联接

使用标准pandas merge 组合基于公共变量的数据集：

```python
# Merge on common column
result = gdf.merge(df, on='common_column')

# Left join
result = gdf.merge(df, on='common_column', how='left')

# Important: Call merge on GeoDataFrame to preserve geometry
# This works: gdf.merge(df, ...)
# This doesn't: df.merge(gdf, ...) # Returns DataFrame, not GeoDataFrame
```

## 空间联接

基于空间关系组合数据集。

### 二元谓词联接(sjoin)

基于几何谓词加入：

```python
# Intersects (default)
joined = gpd.sjoin(gdf1, gdf2, how='inner', predicate='intersects')

# Available predicates
joined = gpd.sjoin(gdf1, gdf2, predicate='contains')
joined = gpd.sjoin(gdf1, gdf2, predicate='within')
joined = gpd.sjoin(gdf1, gdf2, predicate='touches')
joined = gpd.sjoin(gdf1, gdf2, predicate='crosses')
joined = gpd.sjoin(gdf1, gdf2, predicate='overlaps')

# Join types
joined = gpd.sjoin(gdf1, gdf2, how='left')   # Keep all from left
joined = gpd.sjoin(gdf1, gdf2, how='right')  # Keep all from right
joined = gpd.sjoin(gdf1, gdf2, how='inner')  # Intersection only
```

`how` 参数决定保留哪些几何图形：
- **left**：保留左 GeoDataFrame 的索引和几何图形 
- **right**：保留右 GeoDataFrame 的索引和几何图形几何
- **内部**：使用索引的交集，保留左侧几何

### 最近连接（sjoin_nearest）

连接到最近的特征：

```python
# Find nearest neighbor
nearest = gpd.sjoin_nearest(gdf1, gdf2)

# Add distance column
nearest = gpd.sjoin_nearest(gdf1, gdf2, distance_col='distance')

# Limit search radius (significantly improves performance)
nearest = gpd.sjoin_nearest(gdf1, gdf2, max_distance=1000)

# Find k nearest neighbors
nearest = gpd.sjoin_nearest(gdf1, gdf2, k=5)
```

## 叠加操作

组合两个几何图形的集合理论操作GeoDataFrames:

```python
# Intersection - keep areas where both overlap
intersection = gpd.overlay(gdf1, gdf2, how='intersection')

# Union - combine all areas
union = gpd.overlay(gdf1, gdf2, how='union')

# Difference - areas in first not in second
difference = gpd.overlay(gdf1, gdf2, how='difference')

# Symmetric difference - areas in either but not both
sym_diff = gpd.overlay(gdf1, gdf2, how='symmetric_difference')

# Identity - intersection + difference
identity = gpd.overlay(gdf1, gdf2, how='identity')
```

Result 包括来自两个输入 GeoDataFrames.

## 溶解（聚合）

基于属性值的聚合几何图形：

```python
# Dissolve by attribute
dissolved = gdf.dissolve(by='region')

# Dissolve with aggregation functions
dissolved = gdf.dissolve(by='region', aggfunc='sum')
dissolved = gdf.dissolve(by='region', aggfunc={'population': 'sum', 'area': 'mean'})

# Dissolve all into single geometry
dissolved = gdf.dissolve()

# Preserve internal boundaries
dissolved = gdf.dissolve(by='region', as_index=False)
```

## 裁剪

将几何图形剪切到另一个几何图形的边界：

```python
# Clip to polygon boundary
clipped = gpd.clip(gdf, boundary_polygon)

# Clip to another GeoDataFrame
clipped = gpd.clip(gdf, boundary_gdf)
```

## 附加

组合多个GeoDataFrame：

```python
import pandas as pd

# Concatenate GeoDataFrames (CRS must match)
combined = pd.concat([gdf1, gdf2], ignore_index=True)

# With keys for identification
combined = pd.concat([gdf1, gdf2], keys=['source1', 'source2'])
```

## 空间索引

提高空间性能操作：

```python
# GeoPandas uses spatial index automatically for most operations
# Access the spatial index directly
sindex = gdf.sindex

# Query geometries intersecting a bounding box
possible_matches_index = list(sindex.intersection((xmin, ymin, xmax, ymax)))
possible_matches = gdf.iloc[possible_matches_index]

# Query geometries intersecting a polygon
possible_matches_index = list(sindex.query(polygon_geometry))
possible_matches = gdf.iloc[possible_matches_index]
```

空间索引显着加快：
- 空间联接
- 叠加操作
- 使用几何谓词的查询

## 距离计算

```python
# Distance between geometries
distances = gdf1.geometry.distance(gdf2.geometry)

# Distance to single geometry
distances = gdf.geometry.distance(single_point)

# Minimum distance to any feature
min_dist = gdf.geometry.distance(point).min()
```

## 面积和长度计算

为了准确测量，请确保正确的CRS：

```python
# Reproject to appropriate projected CRS for area/length calculations
gdf_projected = gdf.to_crs(epsg=3857)  # Or appropriate UTM zone

# Calculate area (in CRS units, typically square meters)
areas = gdf_projected.geometry.area

# Calculate length/perimeter (in CRS units)
lengths = gdf_projected.geometry.length
```
