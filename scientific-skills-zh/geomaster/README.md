# GeoMaster 地理空间科学技能

## 概述

GeoMaster 是一项全面的地理空间科学技能，涵盖：
- **关于地理空间科学主题的 70 多个章节**
- **跨 7 种编程语言的 500 多个代码示例**
- **300 多个地理空间库** 和工具
- 遥感、GIS、空间统计、用于地球观测的ML/AI

## 内容

### 主要文档
- **SKILL.md** - 主要技能文档，包括安装、快速入门、核心概念、常用操作和工作流程

### 参考文档
1. **core-libraries.md** - GDAL、Rasterio、Fiona、Shapely、PyProj、GeoPandas
2. **remote-sensing.md** - 卫星任务、光学/SAR/高光谱分析、图像处理
3. **gis-software.md** - QGIS/PyQGIS、ArcGIS/ArcPy、GRASS GIS、SAGA GIS 集成
4. **scientific-domains.md** - 海洋、大气、水文学、农业、林业应用
5. **advanced-gis.md** - 3D GIS，时空分析，拓扑，网络分析
6. **programming-languages.md** - R、Julia、JavaScript、C++、Java、Go 地理空间工具
7. **machine-learning.md** - 针对地理空间
8 的 RS、空间 ML、GNN、XAI 的深度学习。 **big-data.md** - 分布式处理、云平台、GPU 加速
9. **行业应用.md** - 城市规划、灾害管理、公用事业、交通
10. **specialized-topics.md** - 地统计学、优化、道德、最佳实践
11. **data-sources.md** - 卫星数据目录、开放数据存储库、API 访问
12. **code-examples.md** - 跨 7 种编程语言的 500 多个代码示例

## 涵盖的关键主题

### 遥感
- Sentinel-1/2/3、Landsat、MODIS、Planet、Maxar
- SAR、高光谱、LiDAR、热成像
- 光谱指数、分类、变化检测

### GIS 操作
- 矢量数据（点、线、多边形）
- 栅格数据处理
- 坐标参考系统
- 空间分析和统计

### 机器学习
- 随机森林、SVM、CNN、U-Net
- 空间统计、地统计
- 图形神经网络
- 可解释的AI

### 编程语言
- **Python** - GDAL、Rasterio、GeoPandas、TorchGeo、RSGISLib
- **R** - sf、terra、栅格、星星
- **Julia** - ArchGDAL、GeoStats.jl
- JavaScript **** - Turf.js、Leaflet
- **C++** - GDAL C++ API
- **Java** - GeoTools
- **Go** - 简单功能 Go

## 安装

See [SKILL.md](SKILL.md)详细安装说明。

### Core Python Stack
```bash
conda install -c conda-forge gdal rasterio fiona shapely pyproj geopandas
```

### 遥感
```bash
pip install rsgislib torchgeo earthengine-api
```

## 快速示例

### 计算 NDVI Sentinel-2
```python
import rasterio
import numpy as np

with rasterio.open('sentinel2.tif') as src:
    red = src.read(4)
    nir = src.read(8)
    ndvi = (nir - red) / (nir + red + 1e-8)
```

### 使用 GeoPandas 进行空间分析
```python
import geopandas as gpd

zones = gpd.read_file('zones.geojson')
points = gpd.read_file('points.geojson')
joined = gpd.sjoin(points, zones, predicate='within')
```

## 许可证

MIT 许可证

## 作者

K-Dense Inc.

## 贡献

此技能是 K-Dense-AI/scientific-agent-skills 存储库的一部分。
有关贡献，请参阅主存储库指南。
