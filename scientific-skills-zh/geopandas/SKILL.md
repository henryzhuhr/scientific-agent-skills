---
name: geopandas
description: 用于处理地理空间矢量数据（包括 shapefile、GeoJSON 和 GeoPackage 文件）的 Python 库。在处理地理数据进行空间分析、几何运算、坐标变换、空间连接、叠加操作、分区统计图或涉及读取/写入/分析矢量地理数据的任何任务时使用。支持 PostGIS 数据库、交互式地图以及与 matplotlib/folium/cartopy 的集成。用于缓冲区分析、数据集之间的空间连接、溶解边界、裁剪数据、计算面积/距离、重新投影坐标系、创建地图或在空间文件格式之间进行转换等任务。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# GeoPandas

GeoPandas 扩展了 pandas 以支持几何类型的空间操作。它结合了 pandas 和 shapely 的功能，用于地理空间数据分析。

## 安装

```bash
uv pip install geopandas
```

### 可选依赖项

```bash
# For interactive maps
uv pip install folium

# For classification schemes in mapping
uv pip install mapclassify

# For faster I/O operations (2-4x speedup)
uv pip install pyarrow

# For PostGIS database support
uv pip install psycopg2
uv pip install geoalchemy2

# For basemaps
uv pip install contextily

# For cartographic projections
uv pip install cartopy
```

## 快速入门

```python
import geopandas as gpd

# Read spatial data
gdf = gpd.read_file("data.geojson")

# Basic exploration
print(gdf.head())
print(gdf.crs)
print(gdf.geometry.geom_type)

# Simple plot
gdf.plot()

# Reproject to different CRS
gdf_projected = gdf.to_crs("EPSG:3857")

# Calculate area (use projected CRS for accuracy)
gdf_projected['area'] = gdf_projected.geometry.area

# Save to file
gdf.to_file("output.gpkg")
```

## 核心概念

### 数据结构

- **GeoSeries**：具有空间操作的几何向量
- **GeoDataFrame**：具有几何列的表格数据结构

 详细信息请参见[data-structs.md](references/data-structurals.md)。

### 读写Data

GeoPandas 读取/写入多种格式：Shapefile、GeoJSON、GeoPackage、PostGIS、Parquet。

```python
# Read with filtering
gdf = gpd.read_file("data.gpkg", bbox=(xmin, ymin, xmax, ymax))

# Write with Arrow acceleration
gdf.to_file("output.gpkg", use_arrow=True)
```

有关全面的 I/O 操作，请参阅 [data-io.md](references/data-io.md)。

### 坐标参考系统

始终检查和管理CRS以实现准确的空间操作：

```python
# Check CRS
print(gdf.crs)

# Reproject (transforms coordinates)
gdf_projected = gdf.to_crs("EPSG:3857")

# Set CRS (only when metadata missing)
gdf = gdf.set_crs("EPSG:4326")
```

有关CRS操作请参阅[crs-management.md](references/crs-management.md)。

## 常用操作

### 几何操作

缓冲、简化、质心、凸包、仿射变换：

```python
# Buffer by 10 units
buffered = gdf.geometry.buffer(10)

# Simplify with tolerance
simplified = gdf.geometry.simplify(tolerance=5, preserve_topology=True)

# Get centroids
centroids = gdf.geometry.centroid
```

所有操作请参见 [geometric-operations.md](references/geometric-operations.md)。

### 空间分析

空间连接、叠加操作、溶解：

```python
# Spatial join (intersects)
joined = gpd.sjoin(gdf1, gdf2, predicate='intersects')

# Nearest neighbor join
nearest = gpd.sjoin_nearest(gdf1, gdf2, max_distance=1000)

# Overlay intersection
intersection = gpd.overlay(gdf1, gdf2, how='intersection')

# Dissolve by attribute
dissolved = gdf.dissolve(by='region', aggfunc='sum')
```

分析操作参见[spatial-analysis.md](references/spatial-analysis.md)。

### 可视化

创建静态和交互式地图：

```python
# Choropleth map
gdf.plot(column='population', cmap='YlOrRd', legend=True)

# Interactive map
gdf.explore(column='population', legend=True).save('map.html')

# Multi-layer map
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
gdf1.plot(ax=ax, color='blue')
gdf2.plot(ax=ax, color='red')
```

参见[visualization.md](references/visualization.md)用于映射技术。

## 详细文档

- **[数据结构](references/data-structs.md)** - GeoSeries 和 GeoDataFrame 基础知识
- **[数据 I/O](references/data-io.md)** - 读/写文件、PostGIS、Parquet
- **[几何操作](references/geometric-operations.md)** - 缓冲、简化、仿射变换
- **[空间分析](references/spatial-analysis.md)** - 连接、叠加、溶解、裁剪
- **[可视化](references/visualization.md)** - 绘图、等值线图、交互式地图
- **[CRS 管理](references/crs-management.md)** - 坐标参考系和投影

## 常用工作流程

### 加载、转换、分析、导出

```python
# 1. Load data
gdf = gpd.read_file("data.shp")

# 2. Check and transform CRS
print(gdf.crs)
gdf = gdf.to_crs("EPSG:3857")

# 3. Perform analysis
gdf['area'] = gdf.geometry.area
buffered = gdf.copy()
buffered['geometry'] = gdf.geometry.buffer(100)

# 4. Export results
gdf.to_file("results.gpkg", layer='original')
buffered.to_file("results.gpkg", layer='buffered')
```

### 空间连接和聚合

```python
# Join points to polygons
points_in_polygons = gpd.sjoin(points_gdf, polygons_gdf, predicate='within')

# Aggregate by polygon
aggregated = points_in_polygons.groupby('index_right').agg({
    'value': 'sum',
    'count': 'size'
})

# Merge back to polygons
result = polygons_gdf.merge(aggregated, left_index=True, right_index=True)
```

### 多源数据集成

```python
# Read from different sources
roads = gpd.read_file("roads.shp")
buildings = gpd.read_file("buildings.geojson")
parcels = gpd.read_postgis("SELECT * FROM parcels", con=engine, geom_col='geom')

# Ensure matching CRS
buildings = buildings.to_crs(roads.crs)
parcels = parcels.to_crs(roads.crs)

# Perform spatial operations
buildings_near_roads = buildings[buildings.geometry.distance(roads.union_all()) < 50]
```

## 性能提示

1. **使用空间索引**：GeoPandas 自动为大多数操作创建空间索引
2. **读取期间过滤**：使用`bbox`、`mask`或`where`参数仅加载所需的数据
3. **使用箭头进行 I/O**：添加 `use_arrow=True` 可使读/写速度提高 2-4 倍 
4. **简化几何图形**：当精度不重要时，使用 `.simplify()` 来降低复杂性
5. **批量操作**：向量化操作比迭代行
6快得多。 **使用适当的 CRS**：针对面积/距离、地理可视化的投影 CRS

## 最佳实践

1. **在空间操作之前始终检查 CRS**
2. **使用投影 CRS** 进行面积和距离计算
3. **在空间连接或叠加之前匹配 CRS**
4. **在操作 
5 之前使用 `.is_valid` 验证几何形状**。 **修改几何列时使用 `.copy()`** 以避免副作用
6. **简化分析时保留拓扑**
7. **使用 GeoPackage** 格式进行现代工作流程（优于 Shapefile）
8. **在 sjoin_nearest 中设置 max_distance** 以获得更好的性能
