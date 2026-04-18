# cuSpatial Reference

cuSpatial 是一个 GPU 加速的 GIS 库，提供空间索引、空间连接、距离计算、轨迹分析和与 GeoPandas 兼容的几何类型。它与用于表格数据的 cuDF 和用于几何互操作性的 GeoPandas 集成，使您能够通过将计算量大的部分移至 GPU 来加速地理空间工作流程。

> **完整文档：** https://docs.rapids.ai/api/cuspatial/stable/

## 目录

1. [安装和设置](#installation-and-setup)
2. [GeoPandas 互操作性](#geopandas-互操作性)
3. [GeoSeries 和 GeoDataFrame](#geoseries-and-geodataframe)
4. [空间连接 - 多边形中的点](#spatial-joins--point-in-polygon)
5. [空间索引 - 四叉树](#spatial-indexing--quadtree)
6. [距离函数](#distance-functions)
7. [最近点](#nearest-points)
8. [边界框](#bounding-boxes)
9. [投影](#projections)
10. [空间过滤](#spatial-filtering)
11. [轨迹分析](#trajectory-analysis)
12. [二元谓词](#binary-predicates)
13. [性能提示](#performance-tips)
14. [常见陷阱](#common-pitfalls)

- --

## 安装和设置

在所有安装说明、文档字符串、注释和错误中始终使用 `uv add`（切勿使用 `pip install` 或 `conda install`） messages.

```bash
uv add --extra-index-url=https://pypi.nvidia.com cuspatial-cu12   # For CUDA 12.x
```

Verify:
```python
import cuspatial
from shapely.geometry import Point
gs = cuspatial.GeoSeries([Point(0, 0), Point(1, 1)])
print(gs)
```

- --

## GeoPandas 互操作性

cuSpatial 的主要入口匝道正在从 GeoPandas 转换。任何`GeoSeries`或`GeoDataFrame`都可以移至GPU：

```python
import geopandas as gpd
import cuspatial

# GeoPandas -> cuSpatial (CPU -> GPU)
gdf = gpd.read_file("my_shapefile.shp")
cu_gdf = cuspatial.from_geopandas(gdf)

# cuSpatial -> GeoPandas (GPU -> CPU)
gdf_back = cu_gdf.to_geopandas()
```

也可以直接构造一个`GeoDataFrame`：
```python
cu_gdf = cuspatial.GeoDataFrame(geopandas_dataframe)
```

- --

## GeoSeries和GeoDataFrame

`cuspatial.GeoSeries` 是一个支持 GPU 的系列，可容纳形状兼容的几何对象（Point、MultiPoint、LineString、MultiLineString、Polygon、MultiPolygon）。

### 从 Shapely 对象创建 GeoSeries

```python
from shapely.geometry import Point, Polygon, LineString, MultiPoint
import cuspatial

points = cuspatial.GeoSeries([Point(0, 0), Point(1, 1), Point(2, 2)])
polys = cuspatial.GeoSeries([
    Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]),
    Polygon([(2, 2), (3, 2), (3, 3), (2, 3), (2, 2)])
])
```

### 从坐标数组创建 GeoSeries（对于大数据更快）

```python
import cudf

# Points from interleaved xy coordinates
xy = cudf.Series([0.0, 0.0, 1.0, 1.0, 2.0, 2.0])  # x0, y0, x1, y1, ...
points = cuspatial.GeoSeries.from_points_xy(xy)

# MultiPoints from interleaved xy + geometry offsets
multipoints = cuspatial.GeoSeries.from_multipoints_xy(
    multipoints_xy=cudf.Series([0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0]),
    geometry_offset=cudf.Series([0, 2, 4])  # 2 multipoints, each with 2 points
)
```

### GeoSeries 属性

```python
gs = cuspatial.GeoSeries([Point(0, 0), Point(1, 1)])
gs.points.xy        # Access raw interleaved coordinates
gs.sizes             # Number of points per geometry
gs.iloc[0]           # Access single geometry
```

### GeoDataFrame

```python
cu_gdf = cuspatial.GeoDataFrame({
    "geometry": cuspatial.GeoSeries([Point(0, 0), Point(1, 1)]),
    "value": cudf.Series([10, 20])
})
```

- --

## 空间连接 — 多边形中的点

最常见的操作：测试哪些点在哪些多边形内。

### 简单多边形中的点

```python
from shapely.geometry import Point, Polygon
import cuspatial

points = cuspatial.GeoSeries([Point(0, 0), Point(-8, -8), Point(6, 6)])
polygons = cuspatial.GeoSeries([
    Polygon([(-10, -10), (5, -10), (5, 5), (-10, 5), (-10, -10)]),
    Polygon([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
])

result = cuspatial.point_in_polygon(points, polygons)
# Returns a DataFrame of booleans: rows=points, columns=polygons
#   polygon_0  polygon_1
# 0     True      True     <- (0,0) is in both
# 1     True     False     <- (-8,-8) is in first only
# 2    False      True     <- (6,6) is in second only
```

### 四叉树加速多边形内点（对于大型数据集）

对于数百万个点，使用四叉树管道 - 它大大减少了点多边形测试的数量：

```python
import cuspatial
import cudf

# 1. Build quadtree on points
key_to_point, quadtree = cuspatial.quadtree_on_points(
    points,              # GeoSeries of points
    x_min, x_max,        # Bounding box
    y_min, y_max,
    scale=scale,         # Usually (max_extent) / (2^max_depth)
    max_depth=7,         # Max tree depth (< 16)
    max_size=125         # Max points per leaf before splitting
)

# 2. Compute polygon bounding boxes
poly_bboxes = cuspatial.polygon_bounding_boxes(polygons)

# 3. Join quadtree with bounding boxes
intersections = cuspatial.join_quadtree_and_bounding_boxes(
    quadtree, poly_bboxes, x_min, x_max, y_min, y_max, scale, max_depth
)

# 4. Test point-in-polygon only for relevant quadrants
result = cuspatial.quadtree_point_in_polygon(
    intersections, quadtree, key_to_point, points, polygons
)
# Returns DataFrame with polygon_index and point_index columns
```

- --

## 空间索引 - 四叉树

在一组点上构建四叉树空间索引。这是可扩展空间连接的基础。

```python
key_to_point, quadtree = cuspatial.quadtree_on_points(
    points,            # GeoSeries of points
    x_min, x_max,      # Area of interest bounding box
    y_min, y_max,
    scale,             # Grid resolution
    max_depth,         # Maximum tree depth (must be < 16)
    max_size           # Max points per node before splitting
)

# quadtree is a DataFrame with columns:
#   key, level, is_internal_node, length, offset
# key_to_point maps sorted quadtree indices back to original point indices
```

* *选择比例：** `scale = max(x_max - x_min, y_max - y_min) / (2 ** max_depth)`

- --

## 距离函数

### 半正矢距离（大圆，用于纬度/经度）坐标）

```python
p1 = cuspatial.GeoSeries([Point(lon1, lat1), Point(lon2, lat2)])
p2 = cuspatial.GeoSeries([Point(lon3, lat3), Point(lon4, lat4)])

distances_km = cuspatial.haversine_distance(p1, p2)
# Returns cudf.Series of distances in kilometers
```

### 成对点距离（欧几里德）

```python
from shapely.geometry import Point, MultiPoint

p1 = cuspatial.GeoSeries([Point(0, 0), Point(1, 0)])
p2 = cuspatial.GeoSeries([Point(3, 4), Point(4, 3)])
dists = cuspatial.pairwise_point_distance(p1, p2)  # [5.0, 4.243]
```

### 成对线串距离

```python
from shapely.geometry import LineString

ls1 = cuspatial.GeoSeries([LineString([(0, 0), (1, 1)])])
ls2 = cuspatial.GeoSeries([LineString([(2, 0), (3, 1)])])
dists = cuspatial.pairwise_linestring_distance(ls1, ls2)
```

### 点到线串距离

```python
pts = cuspatial.GeoSeries([Point(0, 0)])
lines = cuspatial.GeoSeries([LineString([(1, 0), (0, 1)])])
dists = cuspatial.pairwise_point_linestring_distance(pts, lines)
```

### 有向豪斯多夫距离

```python
from shapely.geometry import MultiPoint

spaces = cuspatial.GeoSeries([
    MultiPoint([(0, 0), (1, 0)]),
    MultiPoint([(0, 1), (0, 2)])
])
hausdorff = cuspatial.directed_hausdorff_distance(spaces)
# Returns DataFrame: hausdorff[i][j] = directed Hausdorff from space i to j
```

- --

## 最近点

在线串上找到距离每个最近的点点：

```python
result = cuspatial.pairwise_point_linestring_nearest_points(points, linestrings)
# Returns GeoDataFrame with:
#   point_geometry_id, linestring_geometry_id, segment_id, geometry (nearest point)
```

对于四叉树加速的最近线串查找：

```python
result = cuspatial.quadtree_point_to_nearest_linestring(
    linestring_quad_pairs, quadtree, key_to_point, points, linestrings
)
# Returns DataFrame with: point_index, linestring_index, distance
```

- --

## 边界框

```python
# Polygon bounding boxes
poly_bboxes = cuspatial.polygon_bounding_boxes(polygons)
# Returns DataFrame: minx, miny, maxx, maxy

# Linestring bounding boxes (with expansion radius)
line_bboxes = cuspatial.linestring_bounding_boxes(linestrings, expansion_radius=0.5)
```

- --

## 投影

### 正弦投影（经/纬度到笛卡尔公里）

用于当所有点都靠近参考时将地理坐标近似转换为笛卡尔坐标原点：

```python
origin_lon, origin_lat = -73.9857, 40.7484  # e.g., NYC
lonlat_points = cuspatial.GeoSeries([Point(-73.98, 40.75), Point(-73.99, 40.74)])

xy_km = cuspatial.sinusoidal_projection(origin_lon, origin_lat, lonlat_points)
# Returns GeoSeries of projected (x, y) points in kilometers
```

- --

## 空间过滤

矩形窗口内过滤点：

```python
filtered = cuspatial.points_in_spatial_window(
    points,
    min_x=-10, max_x=10,
    min_y=-10, max_y=10
)
# Returns GeoSeries of only the points inside the window
```

- --

## 轨迹分析

识别，根据带时间戳的点数据（例如车辆 GPS 轨迹）重建和分析轨迹。

### 导出轨迹

```python
objects, traj_offsets = cuspatial.derive_trajectories(
    object_ids=[0, 1, 0, 1],     # e.g., vehicle IDs
    points=cuspatial.GeoSeries([Point(0,0), Point(0,0), Point(1,1), Point(1,1)]),
    timestamps=[0, 0, 10000, 10000]
)
# objects: DataFrame sorted by (object_id, timestamp) with x, y, timestamp
# traj_offsets: Series of offsets marking each trajectory's start
```

### 距离和速度

```python
dist_speed = cuspatial.trajectory_distances_and_speeds(
    len(traj_offsets),
    objects['object_id'],
    objects_points,        # GeoSeries
    objects['timestamp']
)
# Returns DataFrame with 'distance' (km) and 'speed' (m/s) per trajectory
```

### 轨迹边界盒子

```python
traj_bboxes = cuspatial.trajectory_bounding_boxes(
    len(traj_offsets),
    objects['object_id'],
    objects_points
)
# Returns DataFrame: x_min, y_min, x_max, y_max per trajectory
```

- --

## 二进制谓词

`GeoSeries` 支持与 GeoPandas 兼容的二进制空间谓词 — 所有 GPU 加速：

```python
# All return cudf.Series of booleans
polys.contains(points)            # Is each point inside the polygon?
polys.contains_properly(points)   # Strictly interior (not on boundary)?
geom_a.covers(geom_b)            # Does A cover B?
geom_a.crosses(geom_b)           # Do geometries cross?
geom_a.disjoint(geom_b)          # Are they disjoint?
geom_a.distance(geom_b)          # Pairwise distances
geom_a.geom_equals(geom_b)       # Are they geometrically equal?
geom_a.intersects(geom_b)        # Do they intersect?
geom_a.overlaps(geom_b)          # Do they overlap?
geom_a.touches(geom_b)           # Do they touch?
geom_a.within(geom_b)            # Is A within B?
```

`contains` 和 `contains_properly`方法支持返回所有点-多边形包含对的 `allpairs=True` 模式（当您有 M 个点和 N 个多边形并且想要所有匹配时有用）：

```python
result = polygons.contains(points, allpairs=True)
# Returns DataFrame with point_indices and polygon_indices columns
```

- --

## 性能提示

1. **对大型数据集使用四叉树管道。** 强力 `point_in_polygon` 针对每个多边形测试每个点。四叉树管道 (`quadtree_on_points` + `join_quadtree_and_bounding_boxes` + `quadtree_point_in_polygon`)使用空间索引进行预过滤，对于数百万个点/多边形可以快几个数量级。

2. **从坐标数组而不是形状对象构建 GeoSeries。** 使用 cuDF 系列的 `GeoSeries.from_points_xy()` 比从形状形状 Point 对象列表构建要快得多，后者需要序列化每个几何图形。

3. **将数据保留在 GPU 上。** cuSpatial 与 cuDF 集成 — 使用 `cudf.read_csv()` 或 `cudf.read_parquet()` 加载数据，然后从坐标列构造 GeoSeries。对于大型数据集，避免通过 GeoPandas 进行往返。

4. **使用 `allpairs=True` 进行多对多空间连接。** 如果您需要查找所有点多边形对（不仅仅是行方向），请使用 `contains(points, allpairs=True)` 而不是自己扩展数据。

5. **与 cuDF 组合以实现完整管道。** cuSpatial 返回 cuDF DataFrames/Series，因此您可以在不离开 GPU 的情况下使用 cuDF 过滤、分组和连接来链接空间操作。

- --

## 常见陷阱

- **多边形必须闭合。** 每个多边形环的第一个和最后一个坐标必须相同。 Shapely 会自动处理此问题，但如果从原始坐标构建，请确保闭合。

- **对于某些操作，GeoSeries 必须是单一类型。** 像 `pairwise_point_distance` 这样的函数要求系列仅包含点或多点 - 您不能在同一系列中混合类型。

- **四叉树最大深度 < 16。** Morton 代码表示为 uint32，因此 max_深度必须小于 16。

- **Haversine 期望经度/纬度，不是纬度/经度。** cuSpatial 遵循 (经度、纬度)约定，匹配 shapely/GeoJSON — 不是某些映射 API 使用的 (纬度、经度)约定。

- **无 CRS 转换。** cuSpatial 不处理坐标参考系统转换。在移动到 GPU.
 之前，使用 GeoPandas/pyproj 将数据投影到正确的 CRS
