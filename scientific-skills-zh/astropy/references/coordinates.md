# 天文坐标 (astropy.coordinates)

`astropy.coordinates` 包提供了表示天体坐标和不同坐标系之间转换的工具。

## 使用 SkyCoord 创建坐标

推荐使用高级 `SkyCoord` 类接口：

```python
from astropy import units as u
from astropy.coordinates import SkyCoord

# Decimal degrees
c = SkyCoord(ra=10.625*u.degree, dec=41.2*u.degree, frame='icrs')

# Sexagesimal strings
c = SkyCoord(ra='00h42m30s', dec='+41d12m00s', frame='icrs')

# Mixed formats
c = SkyCoord('00h42.5m +41d12m', unit=(u.hourangle, u.deg))

# Galactic coordinates
c = SkyCoord(l=120.5*u.degree, b=-23.4*u.degree, frame='galactic')
```

## 数组坐标

使用数组高效处理多个坐标：

```python
# Create array of coordinates
coords = SkyCoord(ra=[10, 11, 12]*u.degree,
                  dec=[41, -5, 42]*u.degree)

# Access individual elements
coords[0]
coords[1:3]

# Array operations
coords.shape
len(coords)
```

## 访问组件

```python
c = SkyCoord(ra=10.68*u.degree, dec=41.27*u.degree, frame='icrs')

# Access coordinates
c.ra        # <Longitude 10.68 deg>
c.dec       # <Latitude 41.27 deg>
c.ra.hour   # Convert to hours
c.ra.hms    # Hours, minutes, seconds tuple
c.dec.dms   # Degrees, arcminutes, arcseconds tuple
```

## 字符串格式设置

```python
c.to_string('decimal')      # '10.68 41.27'
c.to_string('dms')          # '10d40m48s 41d16m12s'
c.to_string('hmsdms')       # '00h42m43.2s +41d16m12s'

# Custom formatting
c.ra.to_string(unit=u.hour, sep=':', precision=2)
```

## 坐标变换

参考系之间的变换：

```python
c_icrs = SkyCoord(ra=10.68*u.degree, dec=41.27*u.degree, frame='icrs')

# Simple transformations (as attributes)
c_galactic = c_icrs.galactic
c_fk5 = c_icrs.fk5
c_fk4 = c_icrs.fk4

# Explicit transformations
c_icrs.transform_to('galactic')
c_icrs.transform_to(FK5(equinox='J1975'))  # Custom frame parameters
```

## 常用坐标系

### 天体框架
- **ICRS**：国际天体参考系（默认，最常见）
- **FK5**：第五基本目录（默认为春分 J2000.0）
- **FK4**：第四基本目录（较旧，需要春分规范）
- **GCRS**：地心天体参考系统
- **CIRS**：天体中间参考系统

### 银河框架
- **银河**：IAU 1958 银河坐标
- **超级银河**：De Vaucoulurs 超银河坐标
- **银河中心**：基于银河中心的3D坐标

### 水平框架
- **AltAz**：高度-方位角（取决于观察者）
- **HADec**：小时偏角

### 黄道框架
- **GeocentricMeanEcliptic**：地心平均值黄道
- **BarycentricMeanEcliptic**：重心平均黄道
- **HeliocentricMeanEcliptic**：日心平均黄道

## 观察者相关变换

对于高度-方位角坐标，指定观测时间和位置：

```python
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz

# Define observer location
observing_location = EarthLocation(lat=40.8*u.deg, lon=-121.5*u.deg, height=1060*u.m)
# Or use named observatory
observing_location = EarthLocation.of_site('Apache Point Observatory')

# Define observation time
observing_time = Time('2023-01-15 23:00:00')

# Transform to alt-az
aa_frame = AltAz(obstime=observing_time, location=observing_location)
aa = c_icrs.transform_to(aa_frame)

print(f"Altitude: {aa.alt}")
print(f"Azimuth: {aa.az}")
```

## 使用距离

添加 3D 坐标的距离信息：

```python
# With distance
c = SkyCoord(ra=10*u.degree, dec=9*u.degree, distance=770*u.kpc, frame='icrs')

# Access 3D Cartesian coordinates
c.cartesian.x
c.cartesian.y
c.cartesian.z

# Distance from origin
c.distance

# 3D separation
c1 = SkyCoord(ra=10*u.degree, dec=9*u.degree, distance=10*u.pc)
c2 = SkyCoord(ra=11*u.degree, dec=10*u.degree, distance=11.5*u.pc)
sep_3d = c1.separation_3d(c2)  # 3D distance
```

## 角度间隔

计算天空分隔：

```python
c1 = SkyCoord(ra=10*u.degree, dec=9*u.degree, frame='icrs')
c2 = SkyCoord(ra=11*u.degree, dec=10*u.degree, frame='fk5')

# Angular separation (handles frame conversion automatically)
sep = c1.separation(c2)
print(f"Separation: {sep.arcsec} arcsec")

# Position angle
pa = c1.position_angle(c2)
```

## 目录匹配

将坐标与目录源匹配：

```python
# Single target matching
catalog = SkyCoord(ra=ra_array*u.degree, dec=dec_array*u.degree)
target = SkyCoord(ra=10.5*u.degree, dec=41.2*u.degree)

# Find closest match
idx, sep2d, dist3d = target.match_to_catalog_sky(catalog)
matched_coord = catalog[idx]

# Match with maximum separation constraint
matches = target.separation(catalog) < 1*u.arcsec
```

## 命名对象

从在线检索坐标目录：

```python
# Query by name (requires internet)
m31 = SkyCoord.from_name("M31")
crab = SkyCoord.from_name("Crab Nebula")
psr = SkyCoord.from_name("PSR J1012+5307")
```

## 地球位置

定义观察者位置：

```python
# By coordinates
location = EarthLocation(lat=40*u.deg, lon=-120*u.deg, height=1000*u.m)

# By named observatory
keck = EarthLocation.of_site('Keck Observatory')
vlt = EarthLocation.of_site('Paranal Observatory')

# By address (requires internet)
location = EarthLocation.of_address('1002 Holy Grail Court, St. Louis, MO')

# List available observatories
EarthLocation.get_site_names()
```

## 速度信息

包括自行和径向速度：

```python
# Proper motion
c = SkyCoord(ra=10*u.degree, dec=41*u.degree,
             pm_ra_cosdec=15*u.mas/u.yr,
             pm_dec=5*u.mas/u.yr,
             distance=150*u.pc)

# Radial velocity
c = SkyCoord(ra=10*u.degree, dec=41*u.degree,
             radial_velocity=20*u.km/u.s)

# Both
c = SkyCoord(ra=10*u.degree, dec=41*u.degree, distance=150*u.pc,
             pm_ra_cosdec=15*u.mas/u.yr, pm_dec=5*u.mas/u.yr,
             radial_velocity=20*u.km/u.s)
```

## 表示类型

在坐标表示之间切换：

```python
# Cartesian representation
c = SkyCoord(x=1*u.kpc, y=2*u.kpc, z=3*u.kpc,
             representation_type='cartesian', frame='icrs')

# Change representation
c.representation_type = 'cylindrical'
c.rho  # Cylindrical radius
c.phi  # Azimuthal angle
c.z    # Height

# Spherical (default for most frames)
c.representation_type = 'spherical'
```

## 性能提示

1. **使用数组，而不是循环**：将多个坐标作为单个数组
2处理。 **预计算帧**：重复使用帧对象进行多个转换
3. **使用广播**：多次高效地变换多个位置
4. **启用插值**：对于密集时间采样，请使用 ErfaAstromInterpolator

```python
# Fast approach
coords = SkyCoord(ra=ra_array*u.degree, dec=dec_array*u.degree)
coords_transformed = coords.transform_to('galactic')

# Slow approach (avoid)
for ra, dec in zip(ra_array, dec_array):
    c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree)
    c_transformed = c.transform_to('galactic')
```
