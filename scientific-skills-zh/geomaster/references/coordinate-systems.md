# 坐标参考系 (CRS)

地理空间数据坐标系、投影和转换的完整指南。

## 目录

1. [基础知识](#基础知识)
2. [常见 CRS 代码](#common-crs-codes)
3. [投影与地理](#projected-vs-geographic)
4. [UTM 区域](#utm-zones)
5. [变换](#transformations)
6. [最佳实践](#best-practices)

## 基础知识

### 什么是 CRS？

A 坐标参考系定义坐标如何与地球上的位置相关：

- **地理 CRS**：使用纬度/经度（度）
- **投影 CRS**：使用笛卡尔坐标（米、英尺）
- **垂直 CRS**：定义高度/深度（例如，椭圆体高度）

### 组件

1. **基准面**：地球形状的数学模型
  - WGS 84 (EPSG:4326) - Global GPS
  - NAD 83 (EPSG:4269) - 北美
  - ETRS89 (EPSG:4258) - 欧洲

2. **投影**：从曲面到平面的转换
  - 圆柱（墨卡托）
  - 圆锥（兰伯特等形）
  - 方位角（极地立体）

3. **单位**：度、米、英尺等。

## 常见 CRS 代码

### 地理 CRS（纬度/经度）

| EPSG |名称 |面积 |备注 |
|------|------|-----|--------|
| 4326 | WGS 84 |全球| GPS默认，用于存储|
| 4269 | 4269 NAD83 |北美 | USGS数据，与WGS84略有不同|
| 4258 | 4258 ETRS89 |欧洲 |欧洲参考系|
| 4612 | GDA94 |澳大利亚 |澳大利亚基准面 |

### 预计 CRS（米）

| EPSG |名称 |面积 |畸变|备注|
|------|------|-----|------------|--------|
| 3857 | 3857墨卡托网络 |全球（85°S-85°N）|近两极高 |网络地图（Google、OSM）|
| 32601-32660 | UTM N 区 |全球（1° 波段）|每个区域 <1% |公制计算|
| 32701-32760 | UTM S 区 |全球（1° 波段）|每个区域 <1% |南半球|
| 3395 | 3395墨卡托|世界 |中等|世界地图|
| 5070 | 5070阿尔伯斯圆锥 |美国（连续）|低|美国国家测绘|
| 2154 | 2154兰伯特-93 |法国 |非常低|法国国家投影 |

### 区域投影

* *美国：**
- EPSG:5070 - 美国国家地图集等面积 (CONUS)
- EPSG:6350 - 美国国家地图集（阿拉斯加）
- EPSG:102003 - 美国连续阿尔伯斯等面积面积
- EPSG:2227 - 加利福尼亚州 3 区（美国英尺）

* *欧洲：**
- EPSG:3035 - 欧洲等面积 2001
- EPSG:3857 - Web 墨卡托（网络映射）
- EPSG:2154 - 兰伯特93（法国）
- EPSG:25832-25836 - UTM 区域 (ETRS89)

* *其他：**
- EPSG:3112 - GDA94 / MGA 区域 52（澳大利亚）
- EPSG:2056 - CH1903+ / LV95（瑞士）
- EPSG:4326 - WGS 84（全局默认）

## 投影与地理

### 何时使用地理（EPSG:4326）

✅ 存储数据（数据库、文件）
✅ 全球数据集
✅ Web API（GeoJSON、KML）
✅ 纬度/经度查询
✅ GPS 坐标

```python
# Bad: Distance calculation in geographic CRS
gpd.geographic_crs = "EPSG:4326"
distance = gdf.geometry.length  # WRONG! Returns degrees, not meters

# Good: Calculate distance in projected CRS
gdf_projected = gdf.to_crs("EPSG:32633")  # UTM Zone 33N
distance_m = gdf_projected.geometry.length  # Correct: meters
```

### 何时使用投影

✅ 面积/距离计算
✅ 缓冲区操作
✅ 空间分析
✅ 高分辨率映射
✅ 工程应用

```python
import geopandas as gpd

# Project to appropriate UTM zone
gdf = gpd.to_crs(gdf.estimate_utm_crs())

# Now area and distance are accurate
area_sqm = gdf.geometry.area
buffer_1km = gdf.geometry.buffer(1000)  # 1000 meters
```

### Web Mercator 警告

⚠️ **EPSG:3857 (Web Mercator)用于可视化仅**

```python
# DON'T use Web Mercator for area calculations
gdf_web = gdf.to_crs("EPSG:3857")
area = gdf_web.geometry.area  # WRONG! Significant distortion

# DO use appropriate projection
gdf_utm = gdf.to_crs("EPSG:32633")  # or estimate_utm_crs()
area = gdf_utm.geometry.area  # Correct
```

## UTM 区域

### 了解UTM 区域

E 地球分为 60 个区域（每个区域 6° 经度）：
- 区域 1-60：从西到东 
- 每个区域分为北（326xx）和南 (327xx)

### 寻找您的 UTM 区域

```python
def get_utm_zone(longitude, latitude):
    """Get UTM zone EPSG code from coordinates."""
    import math

    zone = math.floor((longitude + 180) / 6) + 1

    if latitude >= 0:
        epsg = 32600 + zone  # Northern hemisphere
    else:
        epsg = 32700 + zone  # Southern hemisphere

    return f"EPSG:{epsg}"

# Example
get_utm_zone(-122.4, 37.7)  # Returns 'EPSG:32610' (Zone 10N)
```

### 使用 GeoPandas 自动检测 UTM 区域

```python
import geopandas as gpd

# Load data
gdf = gpd.read_file('data.geojson')

# Estimate best UTM zone
utm_crs = gdf.estimate_utm_crs()
print(f"Best UTM CRS: {utm_crs}")

# Reproject
gdf_projected = gdf.to_crs(utm_crs)
```

### 特殊 UTM 案例

* *UPS（通用极立体）：**
- EPSG:5041 - UPS 北方（北极）
- EPSG:5042 - UPS South（南极）

* *UTM 非标准：**
- EPSG:31466-31469 - 德国 Gauss-Krüger 区
- EPSG:2056 - 瑞士 LV95（基于 UTM 原理）

## 转换

### 基本转换

```python
from pyproj import Transformer

# Create transformer
transformer = Transformer.from_crs(
    "EPSG:4326",  # WGS 84 (lat/lon)
    "EPSG:32633", # UTM Zone 33N (meters)
    always_xy=True  # Input: x=lon, y=lat (not y=lat, x=lon)
)

# Transform single point
lon, lat = -122.4, 37.7
x, y = transformer.transform(lon, lat)
print(f"Easting: {x:.2f}, Northing: {y:.2f}")
```

### 批量转换

```python
import numpy as np
from pyproj import Transformer

# Arrays of coordinates
lon_array = [-122.4, -122.3]
lat_array = [37.7, 37.8]

transformer = Transformer.from_crs("EPSG:4326", "EPSG:32610", always_xy=True)
xs, ys = transformer.transform(lon_array, lat_array)
```

### 使用 PyProj 进行转换 CRS

```python
from pyproj import CRS

# Get CRS information
crs = CRS.from_epsg(32633)

print(f"Name: {crs.name}")
print(f"Type: {crs.type_name}")
print(f"Area of use: {crs.area_of_use.name}")
print(f"Datum: {crs.datum.name}")
print(f"Ellipsoid: {crs.ellipsoid_name}")
```

## 最佳实践

### 1. 始终了解您的 CRS

```python
import geopandas as gpd

gdf = gpd.read_file('data.geojson')

# Check CRS immediately
print(f"CRS: {gdf.crs}")  # Should never be None!

# If None, set it
if gdf.crs is None:
    gdf.set_crs("EPSG:4326", inplace=True)
```

### 2. 在操作之前验证 CRS

```python
def ensure_same_crs(gdf1, gdf2):
    """Ensure two GeoDataFrames have same CRS."""
    if gdf1.crs != gdf2.crs:
        gdf2 = gdf2.to_crs(gdf1.crs)
        print(f"Reprojected gdf2 to {gdf1.crs}")
    return gdf1, gdf2

# Use before spatial operations
zones, points = ensure_same_crs(zones_gdf, points_gdf)
result = gpd.sjoin(points, zones, predicate='within')
```

### 3. 使用适当的投影

```python
# For local analysis (< 500km extent)
gdf_local = gdf.to_crs(gdf.estimate_utm_crs())

# For national/regional analysis
gdf_us = gdf.to_crs("EPSG:5070")  # US National Atlas Equal Area
gdf_eu = gdf.to_crs("EPSG:3035")  # Europe Equal Area

# For web visualization
gdf_web = gdf.to_crs("EPSG:3857")  # Web Mercator
```

### 4.保留原始 CRS

```python
# Keep original as backup
gdf_original = gdf.copy()
original_crs = gdf.crs

# Do analysis in projected CRS
gdf_projected = gdf.to_crs(gdf.estimate_utm_crs())
result = gdf_projected.geometry.buffer(1000)

# Convert back if needed
result = result.to_crs(original_crs)
```

## 常见陷阱

### 错误 1：以度为单位的面积

```python
# WRONG: Area in square degrees
gdf = gpd.read_file('data.geojson')
area = gdf.geometry.area  # Wrong!

# CORRECT: Use projected CRS
gdf_proj = gdf.to_crs(gdf.estimate_utm_crs())
area_sqm = gdf_proj.geometry.area
area_sqkm = area_sqm / 1_000_000
```

### 错误 2：地理缓冲区CRS

```python
# WRONG: Buffer of 1000 degrees
gdf['buffer'] = gdf.geometry.buffer(1000)

# CORRECT: Project first
gdf_proj = gdf.to_crs("EPSG:32610")
gdf_proj['buffer_km'] = gdf_proj.geometry.buffer(1000)  # 1000 meters
```

### 错误 3：混合 CRS

```python
# WRONG: Spatial join without checking CRS
result = gpd.sjoin(gdf1, gdf2, predicate='intersects')

# CORRECT: Ensure same CRS
if gdf1.crs != gdf2.crs:
    gdf2 = gdf2.to_crs(gdf1.crs)
result = gpd.sjoin(gdf1, gdf2, predicate='intersects')
```

## 快速参考

```python
# Common operations

# Check CRS
gdf.crs
rasterio.open('file.tif').crs

# Reproject
gdf.to_crs("EPSG:32633")

# Auto-detect UTM
gdf.estimate_utm_crs()

# Transform single point
from pyproj import Transformer
tx = Transformer.from_crs("EPSG:4326", "EPSG:32610", always_xy=True)
x, y = tx.transform(lon, lat)

# Create custom CRS
from pyproj import CRS
custom_crs = CRS.from_proj4(
    "+proj=utm +zone=10 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
)
```

有关详细信息，请参阅：
- [EPSG 注册表](https://epsg.org/)
- [PROJ 文档](https://proj.org/)
- [pyproj 文档](https://pyproj4.github.io/pyproj/)
