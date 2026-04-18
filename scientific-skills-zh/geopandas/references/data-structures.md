# GeoPandas 数据结构

## GeoSeries

A GeoSeries 是一个向量，其中每个条目都是与一个观察相对应的一组形状（类似于 pandas Series，但具有几何数据）。

```python
import geopandas as gpd
from shapely.geometry import Point, Polygon

# Create a GeoSeries from geometries
points = gpd.GeoSeries([Point(1, 1), Point(2, 2), Point(3, 3)])

# Access geometric properties
points.area
points.length
points.bounds
```

## GeoDataFrame

A GeoDataFrame 是包含 GeoSeries 的表格数据结构（类似于 pandas DataFrame，但包含地理数据）。

```python
# Create from dictionary
gdf = gpd.GeoDataFrame({
    'name': ['Point A', 'Point B'],
    'value': [100, 200],
    'geometry': [Point(1, 1), Point(2, 2)]
})

# Create from pandas DataFrame with coordinates
import pandas as pd
df = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 2, 3], 'name': ['A', 'B', 'C']})
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.x, df.y))
```

## 关键属性

- **geometry**：活动几何列（可以有多个几何列）
- **crs**：坐标参考系
- **bounds**：所有的边界框geometries
- **total_bounds**：总体边界框

## 设置活动几何图形

当GeoDataFrame具有多个几何列时：

```python
# Set active geometry column
gdf = gdf.set_geometry('other_geom_column')

# Check active geometry column
gdf.geometry.name
```

## 索引和选择

使用标准pandas索引和空间数据：

```python
# Select by label
gdf.loc[0]

# Boolean indexing
large_areas = gdf[gdf.area > 100]

# Select columns
gdf[['name', 'geometry']]
```
