---
name: astropy
description: 用于天文学和天体物理学的综合 Python 库。在处理天文数据（包括天体坐标、物理单位、FITS 文件、宇宙学计算、时间系统、表格、世界坐标系 (WCS)和天文数据分析）时，应使用此技能。当任务涉及坐标变换、单位转换、FITS 文件操作、宇宙距离计算、时间尺度转换或天文数据处理时使用。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# Astropy

## 概述

Astropy 是天文学的核心 Python 包，为天文学研究和数据分析提供基本功能。使用 astropy 进行坐标变换、单位和数量计算、FITS 文件操作、宇宙学计算、精确时间处理、表格数据操作和天文图像处理。

## 何时使用此技能

当任务涉及以下内容时，请使用 astropy：
- 在天体坐标系（ICRS、银河、FK5、AltAz 等）之间进行转换 
- 使用物理单位和数量（将 Jy 转换为 mJy，将秒差距转换为 km 等）
- 读取、写入或操作 FITS 文件（图像或表）
- 宇宙学计算（光度距离、回溯时间、哈勃参数）
- 不同时间尺度（UTC、TAI、TT、TDB）和格式（JD、MJD、ISO）的精确时间处理
- 表操作（读取目录、交叉匹配、过滤、连接）
- 像素和世界之间的 WCS 转换坐标
- 天文常数和计算

## 快速入门

```python
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.io import fits
from astropy.table import Table
from astropy.cosmology import Planck18

# Units and quantities
distance = 100 * u.pc
distance_km = distance.to(u.km)

# Coordinates
coord = SkyCoord(ra=10.5*u.degree, dec=41.2*u.degree, frame='icrs')
coord_galactic = coord.galactic

# Time
t = Time('2023-01-15 12:30:00')
jd = t.jd  # Julian Date

# FITS files
data = fits.getdata('image.fits')
header = fits.getheader('image.fits')

# Tables
table = Table.read('catalog.fits')

# Cosmology
d_L = Planck18.luminosity_distance(z=1.0)
```

## 核心能力

### 1.单位和数量(`astropy.units`)

用单位处理物理量，进行单位换算，保证量纲的一致性计算.

* *关键操作：**
- 通过将值与单位相乘来创建数量
- 使用 `.to()` 方法在单位之间进行转换
- 使用自动单位处理执行算术
- 使用等效项进行特定于域的转换（光谱、多普勒、视差）
- 使用对数单位（幅度、分贝）

* *请参阅：** `references/units.md`，了解全面的文档、单位系统、等效项、性能优化和单位算术。

### 2. 坐标系 (`astropy.coordinates`)

表示天体位置以及不同坐标系之间的变换。

* *关键操作：**
- 在任何坐标系（ICRS、银河、FK5、AltAz 等）中使用 `SkyCoord` 创建坐标 
- 坐标系之间的转换
- 计算角度间隔和位置角度
- 将坐标与目录匹配
- 包括 3D 坐标的距离操作
- 处理自行和径向速度
- 从在线数据库查询命名对象

* *请参阅：** `references/coordinates.md` 了解详细的坐标系描述、变换、依赖于观察者的坐标系（AltAz）、目录匹配和性能提示。

### 3. 宇宙学计算(`astropy.cosmology`)

使用标准宇宙学模型进行宇宙学计算。

* *关键操作：**
- 使用内置宇宙学（Planck18、WMAP9等）
- 创建自定义宇宙学模型
- 计算距离（光度、同动、角直径）
- 计算年龄和回溯时间
- 确定任意时刻的哈勃参数redshift
- 计算密度参数和体积
- 执行逆计算（找到给定距离的 z）

* *请参阅：** `references/cosmology.md` 了解可用模型、距离计算、时间计算、密度参数和中微子效应。

### 4. FITS 文件处理 (`astropy.io.fits`)

阅读、写入和操作 FITS（灵活图像传输系统）文件。

* *关键操作：**
- 使用上下文管理器打开 FITS 文件
- 通过索引或名称访问 HDU（标头数据单元）
- 读取和修改标头（关键字、注释、历史记录）
- 处理图像数据（NumPy 数组）
- 处理表数据（二进制和 ASCII）表）
- 创建新的 FITS 文件（单或多扩展）
- 对大文件使用内存映射
- 访问远程 FITS 文件（S3、HTTP）

* *请参阅：** `references/fits.md` 了解全面的文件操作、标头操作、图像和表处理、多扩展文件以及性能注意事项。

### 5.表格操作（`astropy.table`）

处理表格数据，支持单位、元数据和各种文件格式。

* *关键操作：**
- 从数组、列表或字典创建表
- 读/写多种格式的表（FITS、CSV、HDF5、VOTable）
- 访问和修改列和行
- 对表进行排序、过滤和索引
- 执行数据库式操作（联接、分组、聚合）
- 堆栈和连接表
- 使用单元感知列（QTable）
- 使用屏蔽处理缺失数据

* *请参阅：** `references/tables.md` 用于表创建、I/O 操作、数据操作、排序、过滤、联接、分组和性能提示。

### 6. 时间处理(`astropy.time`)

精确的时间表示以及时间尺度和格式之间的转换。

* *关键操作：**
- 创建各种格式的时间对象（ISO、JD、MJD、Unix 等） 
- 在时间尺度之间转换（UTC、TAI、TT、TDB 等） 
- 使用 TimeDelta 执行时间算术 
- 计算观测者的恒星时 
- 计算光行时校正（重心、 heliocentric)
- 高效处理时间数组
- 处理屏蔽（缺失）时间

* *参见：** `references/time.md` 了解时间格式、时间尺度、转换、算术、观测特征和精度处理。

### 7. 世界坐标系 (`astropy.wcs`)

Transform 

* *关键操作：**
- 从FITS标头读取WCS
- 将像素坐标转换为世界坐标（反之亦然）
- 计算图像足迹
- 访问WCS参数（参考像素、投影、比例）
- 创建自定义WCS对象

* *参见：** `references/wcs_and_other_modules.md` 用于 WCS 操作和转换。

## 其他功能

`references/wcs_and_other_modules.md` 文件还涵盖：

### NDData 和 CCDData
用于包含元数据、不确定性、屏蔽和 WCS 信息的 n 维数据集的容器。

### 建模
用于创建数学模型并将其拟合到天文数据的框架。

### 可视化
用于通过适当的拉伸和缩放显示天文图像的工具。

### 常数
具有适当单位的物理和天文常数（光速、太阳质量、普朗克常数、 

### 卷积
用于平滑和滤波的图像处理内核。

### 统计
强大的统计功能，包括西格玛裁剪和离群值拒绝。

## 安装

```bash
# Install astropy
uv pip install astropy

# With optional dependencies for full functionality
uv pip install astropy[all]
```

## 通用工作流程

### 在系统之间转换坐标

```python
from astropy.coordinates import SkyCoord
import astropy.units as u

# Create coordinate
c = SkyCoord(ra='05h23m34.5s', dec='-69d45m22s', frame='icrs')

# Transform to galactic
c_gal = c.galactic
print(f"l={c_gal.l.deg}, b={c_gal.b.deg}")

# Transform to alt-az (requires time and location)
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz

observing_time = Time('2023-06-15 23:00:00')
observing_location = EarthLocation(lat=40*u.deg, lon=-120*u.deg)
aa_frame = AltAz(obstime=observing_time, location=observing_location)
c_altaz = c.transform_to(aa_frame)
print(f"Alt={c_altaz.alt.deg}, Az={c_altaz.az.deg}")
```

### 读取和分析 FITS 文件

```python
from astropy.io import fits
import numpy as np

# Open FITS file
with fits.open('observation.fits') as hdul:
    # Display structure
    hdul.info()

    # Get image data and header
    data = hdul[1].data
    header = hdul[1].header

    # Access header values
    exptime = header['EXPTIME']
    filter_name = header['FILTER']

    # Analyze data
    mean = np.mean(data)
    median = np.median(data)
    print(f"Mean: {mean}, Median: {median}")
```

### 宇宙学距离计算

```python
from astropy.cosmology import Planck18
import astropy.units as u
import numpy as np

# Calculate distances at z=1.5
z = 1.5
d_L = Planck18.luminosity_distance(z)
d_A = Planck18.angular_diameter_distance(z)

print(f"Luminosity distance: {d_L}")
print(f"Angular diameter distance: {d_A}")

# Age of universe at that redshift
age = Planck18.age(z)
print(f"Age at z={z}: {age.to(u.Gyr)}")

# Lookback time
t_lookback = Planck18.lookback_time(z)
print(f"Lookback time: {t_lookback.to(u.Gyr)}")
```

### 交叉匹配目录

```python
from astropy.table import Table
from astropy.coordinates import SkyCoord, match_coordinates_sky
import astropy.units as u

# Read catalogs
cat1 = Table.read('catalog1.fits')
cat2 = Table.read('catalog2.fits')

# Create coordinate objects
coords1 = SkyCoord(ra=cat1['RA']*u.degree, dec=cat1['DEC']*u.degree)
coords2 = SkyCoord(ra=cat2['RA']*u.degree, dec=cat2['DEC']*u.degree)

# Find matches
idx, sep, _ = coords1.match_to_catalog_sky(coords2)

# Filter by separation threshold
max_sep = 1 * u.arcsec
matches = sep < max_sep

# Create matched catalogs
cat1_matched = cat1[matches]
cat2_matched = cat2[idx[matches]]
print(f"Found {len(cat1_matched)} matches")
```

## 最佳实践

1. **始终使用单位**：将单位附加到数量以避免错误并确保尺寸一致性
2. **对 FITS 文件使用上下文管理器**：确保正确的文件关闭
3. **优先使用数组而不是循环**：将多个坐标/时间作为数组处理以获得更好的性能
4. **检查坐标系**：在变换之前验证坐标系
5. **使用适当的宇宙学**：为您的分析选择正确的宇宙学模型
6. **处理缺失数据**：对缺失值的表使用屏蔽列
7. **指定时间尺度**：明确时间尺度（UTC、TT、TDB）以实现精确计时
8. **将 QTable 用于单位感知表**：当表列具有单位
9 时。 **检查 WCS 有效性**：在使用转换 
10 之前验证 WCS。 **缓存常用值**：可以缓存昂贵的计算（例如宇宙距离）

## 文档和资源

- Astropy 官方文档：https://docs.astropy.org/en/stable/
  - 教程：https://learn.astropy.org/
  - GitHub：https://github.com/astropy/astropy

## 参考文件

有关具体的详细信息模块：
- `references/units.md` - 单位、数量、换算和等值
- `references/coordinates.md` - 坐标系、转换和目录匹配
- `references/cosmology.md` - 宇宙学模型和计算
- `references/fits.md` - FITS 文件操作和操作
- `references/tables.md` - 表创建、I/O 和操作
- `references/time.md` - 时间格式、比例和计算
- `references/wcs_and_other_modules.md` - WCS、ND 数据、建模、可视化、常量和实用程序
