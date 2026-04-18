# GeoMaster 故障排除指南

常见地理空间问题的解决方案和调试策略。

## 安装问题

### GDAL安装问题

```bash
# Problem: "gdal-config not found" or rasterio install fails

# Solution 1: Use conda (recommended)
conda install -c conda-forge gdal rasterio

# Solution 2: System packages (Ubuntu/Debian)
sudo apt-get install gdal-bin libgdal-dev
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
pip install rasterio

# Solution 3: Wheel files
pip install rasterio --find-links=https://gis.wheelwrights.com/

# Verify installation
python -c "from osgeo import gdal; print(gdal.__version__)"
python -c "import rasterio; print(rasterio.__version__)"
```

### Python绑定问题

```bash
# Problem: "DLL load failed" on Windows
# Solution: Reinstall with conda
conda install -c conda-forge --force-reinstall gdal rasterio fiona

# Problem: "Symbol not found" on macOS
# Solution: Rebuild from source or use conda
brew install gdal
pip install rasterio --no-binary rasterio

# Problem: GEOS errors
brew install geos
pip install shapely --no-binary shapely
```

## 运行时错误

### CRS 转换错误

```python
# Problem: "Invalid projection" or "CRS mismatch"
import geopandas as gpd

# Check CRS
print(f"CRS: {gdf.crs}")

# If None, set it
if gdf.crs is None:
    gdf.set_crs("EPSG:4326", inplace=True)

# If unknown, try to detect
gdf = gdf.to_crs(gdf.estimate_utm_crs())
```

### 大型栅格的内存错误

```python
# Problem: "MemoryError" when reading large files
# Solution: Read in chunks or use windows

import rasterio
from rasterio.windows import Window

# Windowed reading
with rasterio.open('large.tif') as src:
    window = Window(0, 0, 1000, 1000)  # (col_off, row_off, width, height)
    subset = src.read(1, window=window)

# Block-by-block processing
with rasterio.open('large.tif') as src:
    for i, window in src.block_windows(1):
        block = src.read(1, window=window)
        # Process block...

# Use Dask for very large files
import dask.array as da
dask_array = da.from_rasterio('large.tif', chunks=(1, 1024, 1024))
```

### 几何验证错误

```python
# Problem: "TopologyException" or "Self-intersection"
import geopandas as gpd
from shapely.validation import make_valid

# Check invalid geometries
invalid = gdf[~gdf.is_valid]
print(f"Invalid geometries: {len(invalid)}")

# Fix invalid geometries
gdf['geometry'] = gdf.geometry.make_valid()

# Buffer with 0 to fix (alternative method)
gdf['geometry'] = gdf.geometry.buffer(0)
```

### 坐标顺序混乱

```python
# Problem: Points in wrong location (lon/lat swapped)
from pyproj import Transformer

# Common mistake: lon, lat vs lat, lon
# Always specify axis order
transformer = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32610",
    always_xy=True  # Input: x=lon, y=lat (not y=lat, x=lon)
)

# Correct usage
x, y = transformer.transform(lon, lat)  # not lat, lon
```

## 性能问题

### 缓慢的空间连接

```python
# Problem: sjoin takes too long
import geopandas as gpd

# Solution: Use spatial index
gdf1.sindex  # Auto-created
gdf2.sindex

# For nearest neighbor joins, use specialized function
result = gpd.sjoin_nearest(gdf1, gdf2, max_distance=1000)

# Use intersection predicate (faster than 'intersects' for points)
result = gpd.sjoin(points, polygons, predicate='within')

# Clip to bounding box first
bbox = gdf1.total_bounds
gdf2_clipped = gdf2.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]
result = gpd.sjoin(gdf1, gdf2_clipped, predicate='intersects')
```

### 缓慢的光栅I/O

```python
# Problem: Reading/writing rasters is slow
import rasterio

# Solution 1: Use compression when writing
profile.update(
    compress='DEFLATE',
    predictor=2,
    zlevel=4
)

# Solution 2: Use tiled output
profile.update(
    tiled=True,
    blockxsize=256,
    blockysize=256
)

# Solution 3: Enable caching
from osgeo import gdal
gdal.SetCacheMax(2**30)  # 1GB

# Solution 4: Use COG format for cloud access
from rio_cogeo.cogeo import cog_translate
cog_translate('input.tif', 'output.tif', profile)
```

### 慢重投影

```python
# Problem: to_crs() is very slow
import geopandas as gpd

# Solution 1: Simplify geometry first
gdf_simple = gdf.geometry.simplify(tolerance=0.0001)
gdf_reproj = gdf_simple.to_crs(target_crs)

# Solution 2: Use lower precision for display
gdf_reproj = gdf.to_crs(target_crs, geometry_precision=2)

# Solution 3: Reproject in parallel
import multiprocessing as mp
from functools import partial

def reproj_chunk(chunk, target_crs):
    return chunk.to_crs(target_crs)

chunks = np.array_split(gdf, mp.cpu_count())
with mp.Pool() as pool:
    results = pool.map(partial(reproj_chunk, target_crs=target_crs), chunks)
gdf_reproj = gpd.GeoDataFrame(pd.concat(results))
```

## 常见陷阱

### 面积（以度为单位）

```python
# WRONG: Area in square degrees
gdf = gpd.read_file('data.geojson')
area = gdf.geometry.area  # Wrong!

# CORRECT: Use projected CRS
gdf_proj = gdf.to_crs(gdf.estimate_utm_crs())
area_sqm = gdf_proj.geometry.area
area_sqkm = area_sqm / 1_000_000
```

### 地理缓冲区CRS

```python
# WRONG: Buffer of 1000 degrees
gdf['buffer'] = gdf.geometry.buffer(1000)

# CORRECT: Project first
gdf_proj = gdf.to_crs("EPSG:32610")
gdf_proj['buffer_km'] = gdf_proj.geometry.buffer(1000)  # 1000 meters
```

### Web 墨卡托失真

```python
# WRONG: Area calculation in Web Mercator
gdf = gdf.to_crs("EPSG:3857")
area = gdf.geometry.area  # Significant distortion!

# CORRECT: Use appropriate projection
gdf = gdf.to_crs(gdf.estimate_utm_crs())
area = gdf.geometry.area  # Accurate
```

### 混合 CRS

```python
# WRONG: Spatial join without checking CRS
result = gpd.sjoin(gdf1, gdf2, predicate='intersects')

# CORRECT: Ensure same CRS
if gdf1.crs != gdf2.crs:
    gdf2 = gdf2.to_crs(gdf1.crs)
result = gpd.sjoin(gdf1, gdf2, predicate='intersects')
```

## 数据问题

### 缺失/缺失 CRS

```python
# Problem: CRS is None
gdf = gpd.read_file('data.geojson')
if gdf.crs is None:
    # Try to detect from data extent
    lon_min, lat_min, lon_max, lat_max = gdf.total_bounds

    if -180 <= lon_min <= 180 and -90 <= lat_min <= 90:
        gdf.set_crs("EPSG:4326", inplace=True)
        print("Assumed WGS 84 (EPSG:4326)")
    else:
        gdf.set_crs(gdf.estimate_utm_crs(), inplace=True)
        print("Estimated UTM zone")
```

### 无效坐标

```python
# Problem: Coordinates out of valid range
gdf = gpd.read_file('data.geojson')

# Check for invalid coordinates
invalid_lon = (gdf.geometry.x < -180) | (gdf.geometry.x > 180)
invalid_lat = (gdf.geometry.y < -90) | (gdf.geometry.y > 90)

if invalid_lon.any() or invalid_lat.any():
    print("Warning: Invalid coordinates found")
    gdf = gdf[~invalid_lon & ~invalid_lat]
```

### 空几何图形

```python
# Problem: Processing fails with empty geometries
# Remove empty geometries
gdf = gdf[~gdf.geometry.is_empty]

# Or fill with None
gdf.loc[gdf.geometry.is_empty, 'geometry'] = None

# Check before operations
if gdf.geometry.is_empty.any():
    print(f"Warning: {gdf.geometry.is_empty.sum()} empty geometries")
```

## 遥感问题

### Sentinel-2 Band Ordering

```python
# Problem: Wrong band indices
# Sentinel-2 L2A SAFE structure:
# B01 (60m), B02 (10m), B03 (10m), B04 (10m), B05 (20m),
# B06 (20m), B07 (20m), B08 (10m), B08A (20m), B09 (60m),
# B11 (20m), B12 (20m)

# Sentinel-2 (resampled to 10m):
# B02=1, B03=2, B04=3, B05=4, B06=5, B07=6, B08=7, B8A=8, B11=9, B12=10

# For 10m bands only:
blue = src.read(1)   # B02
green = src.read(2)  # B03
red = src.read(3)    # B04
nir = src.read(4)    # B08
```

### Cloud Shadow Masking

```python
# Problem: Clouds and shadows not properly masked
def improved_cloud_mask(scl):
    """
    Improved cloud masking using SCL layer.
    Classes: 0=No data, 1=Saturated, 2=Dark, 3=Cloud shadow,
    4=Vegetation, 5=Bare soil, 6=Water, 7=Cloud low prob,
    8=Cloud med prob, 9=Cloud high prob, 10=Thin cirrus
    """
    # Mask: clouds, cloud shadows, saturated
    mask = scl.isin([0, 1, 3, 8, 9, 10])
    return mask

# Apply
scl = s2_image.select('SCL')
cloud_mask = improved_cloud_mask(scl)
image_clean = s2_image.updateMask(cloud_mask.Not())
```

## 错误消息参考

|错误 |原因 |解决方案 |
|-------|--------|----------|
| `CRS mismatch` |不同的坐标系| `gdf2 = gdf2.to_crs(gdf1.crs)` |
| `TopologyException` |无效/自相交几何 | `gdf.geometry = gdf.geometry.make_valid()` |
| `MemoryError` |大数据集|使用 Dask 或分块读取 |
| `Invalid projection` |未知的 CRS 代码 |检查EPSG代码，使用`CRS.from_user_input()` |
| `Empty geometry` |空几何 | `gdf = gdf[~gdf.geometry.is_empty]` |
| `Bounds error` |坐标超出范围 |过滤无效坐标|
| `DLL load failed` | GDAL 未安装 |使用conda：`conda install gdal` |
| `Symbol not found` |库链接问题 |使用二进制轮或 conda |
| 重新安装`Self-intersection` |无效的多边形 | Buffer(0)或 make_valid() |

## 调试策略

### 1. 检查数据完整性

```python
def check_geodataframe(gdf):
    """Comprehensive GeoDataFrame health check."""
    print(f"Shape: {gdf.shape}")
    print(f"CRS: {gdf.crs}")
    print(f"Bounds: {gdf.total_bounds}")
    print(f"Invalid geometries: {(~gdf.is_valid).sum()}")
    print(f"Empty geometries: {gdf.geometry.is_empty.sum()}")
    print(f"None geometries: {gdf.geometry.isna().sum()}")
    print(f"Duplicate geometries: {gdf.geometry.duplicated().sum()}")
    print("\nGeometry types:")
    print(gdf.geometry.type.value_counts())
    print("\nCoordinate range:")
    print(f"  X: {gdf.geometry.x.min():.2f} to {gdf.geometry.x.max():.2f}")
    print(f"  Y: {gdf.geometry.y.min():.2f} to {gdf.geometry.y.max():.2f}")

check_geodataframe(gdf)
```

### 2. 测试转换

```python
def test_reprojection(gdf, target_crs):
    """Test if reprojection is reversible."""
    original = gdf.copy()
    gdf_proj = gdf.to_crs(target_crs)
    gdf_back = gdf_proj.to_crs(gdf.crs)

    diff = original.geometry.distance(gdf_back.geometry).max()
    if diff > 1:  # More than 1 meter
        print(f"Warning: Max error: {diff:.2f}m")
        return False
    return True
```

### 3. 型材代码

```python
import time

def time_operation(func, *args, **kwargs):
    """Time a geospatial operation."""
    start = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start
    print(f"{func.__name__}: {elapsed:.2f}s")
    return result

# Usage
time_operation(gdf.to_crs, "EPSG:32610")
```

## 获取帮助

### 检查版本

```python
import sys
import geopandas as gpd
import rasterio
from osgeo import gdal

print(f"Python: {sys.version}")
print(f"GeoPandas: {gpd.__version__}")
print(f"Rasterio: {rasterio.__version__}")
print(f"GDAL: {gdal.__version__}")
print(f"PROJ: {gdal.VersionInfo('PROJ')}")
```

### 有用资源

- **GeoPandas 文档**：https://geopandas.org/
- **Rasterio 文档**： https://rasterio.readthedocs.io/
- **PROJ datab**：https://epsg.org/
- **Stack Overflow**：使用 `gis` 和 `python`
- **GIS Stack Exchange**：https://gis.stackexchange.com/
