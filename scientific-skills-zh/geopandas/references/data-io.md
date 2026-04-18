# 读写空间数据

## 读取文件

使用`geopandas.read_file()`导入矢量空间数据：

```python
import geopandas as gpd

# Read from file
gdf = gpd.read_file("data.shp")
gdf = gpd.read_file("data.geojson")
gdf = gpd.read_file("data.gpkg")

# Read from URL
gdf = gpd.read_file("https://example.com/data.geojson")

# Read from ZIP archive
gdf = gpd.read_file("data.zip")
```

### 性能：箭头加速

读取速度提高2-4倍，使用Arrow：

```python
gdf = gpd.read_file("data.gpkg", use_arrow=True)
```

需要PyArrow：`uv pip install pyarrow`

### 在读取期间过滤

预过滤数据以仅加载需要的内容：

```python
# Load specific rows
gdf = gpd.read_file("data.gpkg", rows=100)  # First 100 rows
gdf = gpd.read_file("data.gpkg", rows=slice(10, 20))  # Rows 10-20

# Load specific columns
gdf = gpd.read_file("data.gpkg", columns=['name', 'population'])

# Spatial filter with bounding box
gdf = gpd.read_file("data.gpkg", bbox=(xmin, ymin, xmax, ymax))

# Spatial filter with geometry mask
gdf = gpd.read_file("data.gpkg", mask=polygon_geometry)

# SQL WHERE clause (requires Fiona 1.9+ or Pyogrio)
gdf = gpd.read_file("data.gpkg", where="population > 1000000")

# Skip geometry (returns pandas DataFrame)
df = gpd.read_file("data.gpkg", ignore_geometry=True)
```

## 写入文件

使用`to_file()` 要导出：

```python
# Write to Shapefile
gdf.to_file("output.shp")

# Write to GeoJSON
gdf.to_file("output.geojson", driver='GeoJSON')

# Write to GeoPackage (supports multiple layers)
gdf.to_file("output.gpkg", layer='layer1', driver="GPKG")

# Arrow acceleration for faster writing
gdf.to_file("output.gpkg", use_arrow=True)
```

### 支持的格式

列出所有可用的驱动程序：

```python
import pyogrio
pyogrio.list_drivers()
```

 常见格式：Shapefile、GeoJSON、GeoPackage (GPKG)、KML、MapInfo File、CSV（带有WKT 几何）

## Parquet 和 Feather

保留空间信息并支持多个几何列的列格式：

```python
# Write
gdf.to_parquet("data.parquet")
gdf.to_feather("data.feather")

# Read
gdf = gpd.read_parquet("data.parquet")
gdf = gpd.read_feather("data.feather")
```

 优点：
- 比传统格式更快的 I/O
- 更好的压缩
- 保留多个几何列
- 架构版本控制支持

## PostGIS数据库

### 从PostGIS读取

```python
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:password@host:port/database')

# Read entire table
gdf = gpd.read_postgis("SELECT * FROM table_name", con=engine, geom_col='geometry')

# Read with SQL query
gdf = gpd.read_postgis("SELECT * FROM table WHERE population > 100000", con=engine, geom_col='geometry')
```

### 写入PostGIS

```python
# Create or replace table
gdf.to_postgis("table_name", con=engine, if_exists='replace')

# Append to existing table
gdf.to_postgis("table_name", con=engine, if_exists='append')

# Fail if table exists
gdf.to_postgis("table_name", con=engine, if_exists='fail')
```

要求： `uv pip install psycopg2` 或 `uv pip install psycopg` 和 `uv pip install geoalchemy2`

## 文件类对象

从文件句柄或内存缓冲区中读取：

```python
# From file handle
with open('data.geojson', 'r') as f:
    gdf = gpd.read_file(f)

# From StringIO
from io import StringIO
geojson_string = '{"type": "FeatureCollection", ...}'
gdf = gpd.read_file(StringIO(geojson_string))
```

## 远程存储（fsspec）

从云访问数据存储：

```python
# S3
gdf = gpd.read_file("s3://bucket/data.gpkg")

# Azure Blob Storage
gdf = gpd.read_file("az://container/data.gpkg")

# HTTP/HTTPS
gdf = gpd.read_file("https://example.com/data.geojson")
```
