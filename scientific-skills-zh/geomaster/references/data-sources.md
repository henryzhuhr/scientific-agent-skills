# 地理空间数据源

用于地理空间分析的卫星图像、矢量数据和 API 的综合目录。

## 卫星数据源

### 哨兵任务 (ESA)

|平台|分辨率|覆盖范围|访问 |
|----------|------------|---------|--------|
| **哨兵-2** | 10-60m |全球| https://scihub.copernicus.eu/ |
| **哨兵-1** | 5-40m（SAR）|全球| https://scihub.copernicus.eu/ |
| **哨兵-3** | 300m-1km|全球| https://scihub.copernicus.eu/ |
| **哨兵-5P** |各种|全球| https://scihub.copernicus.eu/ |

```python
# Access via Sentinelsat
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

api = SentinelAPI('user', 'password', 'https://scihub.copernicus.eu/dhus')

# Search
products = api.query(geojson_to_wkt(aoi_geojson),
                     date=('20230101', '20231231'),
                     platformname='Sentinel-2',
                     cloudcoverpercentage=(0, 20))

# Download
api.download_all(products)
```

### 陆地卫星 (USGS/NASA)

|平台|分辨率|覆盖范围|访问 |
|----------|------------|---------|--------|
| **陆地卫星 9** | 30m |全球| https://earthexplorer.usgs.gov/ |
| **陆地卫星 8** | 30m |全球| https://earthexplorer.usgs.gov/ |
| **陆地卫星 7** | 15-60m |全球| https://earthexplorer.usgs.gov/ |
| **陆地卫星 5-7** | 30-60m |全球| https://earthexplorer.usgs.gov/ |

### 商业卫星数据

|供应商|平台|分辨率| API |
|----------|---------|------------|-----|
| **行星** | PlanetScope、SkySat | 0.5-3m| Planet.com |
| **麦克萨** | WorldView、GeoEye | 0.3-1.2m| maxar.com |
| **空客** |昴宿星团，斑点| 0.5-2m|空中客车.com |
| **卡佩拉** | Capella-2（SAR）| 0.5-1m| capellaspace.com |

## 海拔数据

|数据集 |分辨率|覆盖范围|来源 |
|---------|------------|---------|--------|
| **AW3D30** | 30m |全球| https://www.eorc.jaxa.jp/ALOS/en/aw3d30/ |
| **SRTM** | 30m | 56°S-60°N | https://www.usgs.gov/ |
| **ASTER GDEM** | 30m | 83°S-83°N | https://asterweb.jpl.nasa.gov/ |
| **哥白尼 DEM** | 30m |全球| https://copernicus.eu/ |
| **北极DEM** | 2-10m |北极| https://www.pgc.umn.edu/ |

```python
# Download SRTM via API
import elevation

# Download SRTM 1 arc-second (30m)
elevation.clip(bounds=(-122.5, 37.7, -122.3, 37.9), output='srtm.tif')

# Clean and fill gaps
elevation.clean('srtm.tif', 'srtm_filled.tif')
```

## 土地覆盖数据

|数据集 |分辨率|课程 |来源 |
|---------|------------|---------|--------|
| **欧空局环球报道** | 10m | 11 节课 | https://worldcover2021.esa.int/ |
| **ESRI 土地覆盖** | 10m | 10 节课 | https://www.esri.com/ |
| **哥白尼全球** | 100m | 23 节课 | https://land.copernicus.eu/ |
| **MODIS MCD12Q1** | 500m | 17 节课 | https://lpdaac.usgs.gov/ |
| **NLCD（美国）** | 30m | 20 节课 | https://www.mrlc.gov/ |

## 气候和天气数据

### 再分析数据

|数据集 |分辨率|颞叶 |访问 |
|---------|------------|---------|--------|
| **ERA5** | 31公里 |每小时 (1979+) | https://cds.climate.copernicus.eu/ |
| **MERRA-2** | 50公里|每小时 (1980+) | https://gmao.gsfc.nasa.gov/ |
| **JRA-55** | 55公里 | 3 小时（1958 年以上）| https://jra.kishou.go.jp/ |

```python
# Download ERA5 via CDS API
import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'variable': '2m_temperature',
        'year': '2023',
        'month': '01',
        'day': '01',
        'time': '12:00',
        'area': [37.9, -122.5, 37.7, -122.3],
        'format': 'netcdf'
    },
    'era5_temp.nc'
)
```

## OpenStreetMap 数据

### 访问方法

```python
# Via OSMnx
import osmnx as ox

# Download place boundary
gdf = ox.geocode_to_gdf('San Francisco, CA')

# Download street network
G = ox.graph_from_place('San Francisco, CA', network_type='drive')

# Download building footprints
buildings = ox.geometries_from_place('San Francisco, CA', tags={'building': True})

# Via Overpass API
import requests

overpass_url = "http://overpass-api.de/api/interpreter"
query = """
    [out:json];
    way["highway"](37.7,-122.5,37.9,-122.3);
    out geom;
"""

response = requests.get(overpass_url, params={'data': query})
data = response.json()
```

## 矢量数据源

### 自然地球

```python
import geopandas as gpd

# Admin boundaries (scale: 10m, 50m, 110m)
countries = gpd.read_file('https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_admin_0_countries.zip')
urban_areas = gpd.read_file('https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_urban_areas.zip')
ports = gpd.read_file('https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_ports.zip')
```

### 其他来源

|数据集 |类型 |访问|
|---------|-----|--------|
| **GADM** |管理边界 | https://gadm.org/ |
| **HydroSHEDS** |河流、盆地| https://www.hydrosheds.org/ |
| **全球发电厂** |发电厂| https://datasets.wri.org/ |
| **世界流行** |人口| https://www.worldpop.org/ |
| **GPW** |人口| https://sedac.ciesin.columbia.edu/ |
| **HDX** |人道主义数据| https://data.humdata.org/ |

## API

### Google 地图平台

```python
import requests

# Geocoding
url = "https://maps.googleapis.com/maps/api/geocode/json"
params = {
    'address': 'Golden Gate Bridge',
    'key': YOUR_API_KEY
}

response = requests.get(url, params=params)
data = response.json()
location = data['results'][0]['geometry']['location']
```

### Mapbox

```python
# Geocoding
import requests

url = "https://api.mapbox.com/geocoding/v5/mapbox.places/Golden%20Gate%20Bridge.json"
params = {'access_token': YOUR_ACCESS_TOKEN}

response = requests.get(url, params=params)
data = response.json()
```

### OpenWeatherMap

```python
# Current weather
url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    'lat': 37.7,
    'lon': -122.4,
    'appid': YOUR_API_KEY
}

response = requests.get(url, params=params)
weather = response.json()
```

## Python 中的数据 API

### STAC（时空资产目录）

```python
import pystac_client

# Connect to STAC catalog
catalog = pystac_client.Client.open("https://earth-search.aws.element84.com/v1")

# Search
search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=[-122.5, 37.7, -122.3, 37.9],
    datetime="2023-01-01/2023-12-31",
    query={"eo:cloud_cover": {"lt": 20}}
)

items = search.get_all_items()
```

### Planetary计算机

```python
import planetary_computer
import pystac_client

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace
)

# Search and sign items
items = catalog.search(...)
signed_items = [planetary_computer.sign(item) for item in items]
```

## 下载脚本

### 自动下载脚本

```python
from sentinelsat import SentinelAPI
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import os

def download_and_process_sentinel2(aoi, date_range, output_dir):
    """
    Download and process Sentinel-2 imagery.
    """
    # Initialize API
    api = SentinelAPI('user', 'password', 'https://scihub.copernicus.eu/dhus')

    # Search
    products = api.query(
        aoi,
        date=date_range,
        platformname='Sentinel-2',
        processinglevel='Level-2A',
        cloudcoverpercentage=(0, 20)
    )

    # Download
    api.download_all(products, directory_path=output_dir)

    # Process each product
    for product in products:
        product_path = f"{output_dir}/{product['identifier']}.SAFE"
        processed = process_sentinel2_product(product_path)
        save_rgb_composite(processed, f"{output_dir}/{product['identifier']}_rgb.tif")

def process_sentinel2_product(product_path):
    """Process Sentinel-2 L2A product."""
    # Find 10m bands (B02, B03, B04, B08)
    bands = {}
    for band_id in ['B02', 'B03', 'B04', 'B08']:
        band_path = find_band_file(product_path, band_id, resolution='10m')
        with rasterio.open(band_path) as src:
            bands[band_id] = src.read(1)
            profile = src.profile

    # Stack bands
    stacked = np.stack([bands['B04'], bands['B03'], bands['B02']])  # RGB

    return stacked, profile
```

## 数据质量评估

```python
def assess_data_quality(raster_path):
    """
    Assess quality of geospatial raster data.
    """
    import rasterio
    import numpy as np

    with rasterio.open(raster_path) as src:
        data = src.read()
        profile = src.profile

    quality_report = {
        'nodata_percentage': np.sum(data == src.nodata) / data.size * 100,
        'data_range': (data.min(), data.max()),
        'mean': np.mean(data),
        'std': np.std(data),
        'has_gaps': np.any(data == src.nodata),
        'projection': profile['crs'],
        'resolution': (profile['transform'][0], abs(profile['transform'][4]))
    }

    return quality_report
```

数据访问代码示例，请参见[代码示例.md](代码示例.md).
