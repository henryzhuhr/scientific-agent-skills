# 坐标参考系 (CRS)

A 坐标参考系定义坐标如何与地球上的位置相关。

## 了解 CRS

CRS 信息存储为 `pyproj.CRS` 对象：

```python
# Check CRS
print(gdf.crs)

# Check if CRS is set
if gdf.crs is None:
    print("No CRS defined")
```

## 设置与重新投影

### 设置CRS

当坐标正确但缺少 CRS 元数据时使用 `set_crs()`：

```python
# Set CRS (doesn't transform coordinates)
gdf = gdf.set_crs("EPSG:4326")
gdf = gdf.set_crs(4326)
```

* *警告**：仅在缺少 CRS 元数据时使用。这不会转换坐标。

### 重新投影

使用`to_crs()`在坐标系之间转换坐标：

```python
# Reproject to different CRS
gdf_projected = gdf.to_crs("EPSG:3857")  # Web Mercator
gdf_projected = gdf.to_crs(3857)

# Reproject to match another GeoDataFrame
gdf1_reprojected = gdf1.to_crs(gdf2.crs)
```

## CRS格式

GeoPandas通过以下方式接受多种格式`pyproj.CRS.from_user_input()`:

```python
# EPSG code (integer)
gdf.to_crs(4326)

# Authority string
gdf.to_crs("EPSG:4326")
gdf.to_crs("ESRI:102003")

# WKT string (Well-Known Text)
gdf.to_crs("GEOGCS[...]")

# PROJ string
gdf.to_crs("+proj=longlat +datum=WGS84")

# pyproj.CRS object
from pyproj import CRS
crs_obj = CRS.from_epsg(4326)
gdf.to_crs(crs_obj)
```

* *最佳实践**：使用 WKT2 或权限字符串 (EPSG)保留完整的 CRS 信息。

## 常见 EPSG 代码

### 地理坐标系统

```python
# WGS 84 (latitude/longitude)
gdf.to_crs("EPSG:4326")

# NAD83
gdf.to_crs("EPSG:4269")
```

### 投影坐标系

```python
# Web Mercator (used by web maps)
gdf.to_crs("EPSG:3857")

# UTM zones (example: UTM Zone 33N)
gdf.to_crs("EPSG:32633")

# UTM zones (Southern hemisphere, example: UTM Zone 33S)
gdf.to_crs("EPSG:32733")

# US National Atlas Equal Area
gdf.to_crs("ESRI:102003")

# Albers Equal Area Conic (North America)
gdf.to_crs("EPSG:5070")
```

## CRS 操作要求

### 需要匹配CRS

的操作这些操作需要相同的CRS:

```python
# Spatial joins
gpd.sjoin(gdf1, gdf2, ...)  # CRS must match

# Overlay operations
gpd.overlay(gdf1, gdf2, ...)  # CRS must match

# Appending
pd.concat([gdf1, gdf2])  # CRS must match

# Reproject first if needed
gdf2_reprojected = gdf2.to_crs(gdf1.crs)
result = gpd.sjoin(gdf1, gdf2_reprojected)
```

### 投影 CRS

中的最佳操作面积和距离计算应使用投影 CRS:

```python
# Bad: area in degrees (meaningless)
areas_degrees = gdf.geometry.area  # If CRS is EPSG:4326

# Good: reproject to appropriate projected CRS first
gdf_projected = gdf.to_crs("EPSG:3857")
areas_meters = gdf_projected.geometry.area  # Square meters

# Better: use appropriate local UTM zone for accuracy
gdf_utm = gdf.to_crs("EPSG:32633")  # UTM Zone 33N
accurate_areas = gdf_utm.geometry.area
```

## 为面积/距离选择适当的 CRS

### 计算

使用等面积投影：

```python
# Albers Equal Area Conic (North America)
gdf.to_crs("EPSG:5070")

# Lambert Azimuthal Equal Area
gdf.to_crs("EPSG:3035")  # Europe

# UTM zones (for local areas)
gdf.to_crs("EPSG:32633")  # Appropriate UTM zone
```

### 对于距离保持（导航）

使用等距投影：

```python
# Azimuthal Equidistant
gdf.to_crs("ESRI:54032")
```

### 对于形状保持（角度）

使用等角投影：

```python
# Web Mercator (conformal but distorts area)
gdf.to_crs("EPSG:3857")

# UTM zones (conformal for local areas)
gdf.to_crs("EPSG:32633")
```

### 用于Web映射

```python
# Web Mercator (standard for web maps)
gdf.to_crs("EPSG:3857")
```

## 估计UTM区域

```python
# Estimate appropriate UTM CRS from data
utm_crs = gdf.estimate_utm_crs()
gdf_utm = gdf.to_crs(utm_crs)
```

## 多个具有不同CRS

GeoPandas 0.8+支持每个几何列不同的CRS：

```python
# Set CRS for specific geometry column
gdf = gdf.set_crs("EPSG:4326", allow_override=True)

# Active geometry determines operations
gdf = gdf.set_geometry('other_geom_column')

# Check CRS mismatch
try:
    result = gdf1.overlay(gdf2)
except ValueError as e:
    print("CRS mismatch:", e)
```

## CRS信息

```python
# Get full CRS details
print(gdf.crs)

# Get EPSG code if available
print(gdf.crs.to_epsg())

# Get WKT representation
print(gdf.crs.to_wkt())

# Get PROJ string
print(gdf.crs.to_proj4())

# Check if CRS is geographic (lat/lon)
print(gdf.crs.is_geographic)

# Check if CRS is projected
print(gdf.crs.is_projected)
```

## 转换个体几何形状

```python
from pyproj import Transformer

# Create transformer
transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

# Transform point
x_new, y_new = transformer.transform(x, y)
```
