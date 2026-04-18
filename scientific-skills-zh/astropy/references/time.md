# 时间处理 (astropy.time)

`astropy.time` 模块提供了强大的工具来操作时间和日期，支持各种时间尺度和格式。

## 创建时间对象

### 基本创建

```python
from astropy.time import Time
import astropy.units as u

# ISO format (automatically detected)
t = Time('2023-01-15 12:30:45')
t = Time('2023-01-15T12:30:45')

# Specify format explicitly
t = Time('2023-01-15 12:30:45', format='iso', scale='utc')

# Julian Date
t = Time(2460000.0, format='jd')

# Modified Julian Date
t = Time(59945.0, format='mjd')

# Unix time (seconds since 1970-01-01)
t = Time(1673785845.0, format='unix')
```

### 数组时间

```python
# Multiple times
times = Time(['2023-01-01', '2023-06-01', '2023-12-31'])

# From arrays
import numpy as np
jd_array = np.linspace(2460000, 2460100, 100)
times = Time(jd_array, format='jd')
```

## 时间格式

### 支持的格式

```python
# ISO 8601
t = Time('2023-01-15 12:30:45', format='iso')
t = Time('2023-01-15T12:30:45.123', format='isot')

# Julian dates
t = Time(2460000.0, format='jd')          # Julian Date
t = Time(59945.0, format='mjd')           # Modified Julian Date

# Decimal year
t = Time(2023.5, format='decimalyear')
t = Time(2023.5, format='jyear')          # Julian year
t = Time(2023.5, format='byear')          # Besselian year

# Year and day-of-year
t = Time('2023:046', format='yday')       # 46th day of 2023

# FITS format
t = Time('2023-01-15T12:30:45', format='fits')

# GPS seconds
t = Time(1000000000.0, format='gps')

# Unix time
t = Time(1673785845.0, format='unix')

# Matplotlib dates
t = Time(738521.0, format='plot_date')

# datetime objects
from datetime import datetime
dt = datetime(2023, 1, 15, 12, 30, 45)
t = Time(dt)
```

## 时间刻度

### 可用时间刻度

```python
# UTC - Coordinated Universal Time (default)
t = Time('2023-01-15 12:00:00', scale='utc')

# TAI - International Atomic Time
t = Time('2023-01-15 12:00:00', scale='tai')

# TT - Terrestrial Time
t = Time('2023-01-15 12:00:00', scale='tt')

# TDB - Barycentric Dynamical Time
t = Time('2023-01-15 12:00:00', scale='tdb')

# TCG - Geocentric Coordinate Time
t = Time('2023-01-15 12:00:00', scale='tcg')

# TCB - Barycentric Coordinate Time
t = Time('2023-01-15 12:00:00', scale='tcb')

# UT1 - Universal Time
t = Time('2023-01-15 12:00:00', scale='ut1')
```

### 转换时间刻度

```python
t = Time('2023-01-15 12:00:00', scale='utc')

# Convert to different scales
t_tai = t.tai
t_tt = t.tt
t_tdb = t.tdb
t_ut1 = t.ut1

# Check offset
print(f"TAI - UTC = {(t.tai - t.utc).sec} seconds")
# TAI - UTC = 37 seconds (leap seconds)
```

## 格式转换

### 更改输出格式

```python
t = Time('2023-01-15 12:30:45')

# Access in different formats
print(t.jd)           # Julian Date
print(t.mjd)          # Modified Julian Date
print(t.iso)          # ISO format
print(t.isot)         # ISO with 'T'
print(t.unix)         # Unix time
print(t.decimalyear)  # Decimal year

# Change default format
t.format = 'mjd'
print(t)  # Displays as MJD
```

### 高精度输出

```python
# Use subfmt for precision control
t.to_value('mjd', subfmt='float')    # Standard float
t.to_value('mjd', subfmt='long')     # Extended precision
t.to_value('mjd', subfmt='decimal')  # Decimal (highest precision)
t.to_value('mjd', subfmt='str')      # String representation
```

## 时间算术

### TimeDelta 对象

```python
from astropy.time import TimeDelta

# Create time difference
dt = TimeDelta(1.0, format='jd')      # 1 day
dt = TimeDelta(3600.0, format='sec')  # 1 hour

# Subtract times
t1 = Time('2023-01-15')
t2 = Time('2023-02-15')
dt = t2 - t1
print(dt.jd)   # 31 days
print(dt.sec)  # 2678400 seconds
```

### 加/减时间

```python
t = Time('2023-01-15 12:00:00')

# Add TimeDelta
t_future = t + TimeDelta(7, format='jd')  # Add 7 days

# Add Quantity
t_future = t + 1*u.hour
t_future = t + 30*u.day
t_future = t + 1*u.year

# Subtract
t_past = t - 1*u.week
```

### 时间范围

```python
# Create range of times
start = Time('2023-01-01')
end = Time('2023-12-31')
times = start + np.linspace(0, 365, 100) * u.day

# Or using TimeDelta
times = start + TimeDelta(np.linspace(0, 365, 100), format='jd')
```

## 观测相关功能

### 恒星时

```python
from astropy.coordinates import EarthLocation

# Define observer location
location = EarthLocation(lat=40*u.deg, lon=-120*u.deg, height=1000*u.m)

# Create time with location
t = Time('2023-06-15 23:00:00', location=location)

# Calculate sidereal time
lst_apparent = t.sidereal_time('apparent')
lst_mean = t.sidereal_time('mean')

print(f"Local Sidereal Time: {lst_apparent}")
```

### 光传播时间校正

```python
from astropy.coordinates import SkyCoord, EarthLocation

# Define target and observer
target = SkyCoord(ra=10*u.deg, dec=20*u.deg)
location = EarthLocation.of_site('Keck Observatory')

# Observation times
times = Time(['2023-01-01', '2023-06-01', '2023-12-31'],
             location=location)

# Calculate light travel time to solar system barycenter
ltt_bary = times.light_travel_time(target, kind='barycentric')
ltt_helio = times.light_travel_time(target, kind='heliocentric')

# Apply correction
times_barycentric = times.tdb + ltt_bary
```

### 地球旋转角度

```python
# Earth rotation angle (for celestial to terrestrial transformations)
era = t.earth_rotation_angle()
```

## 处理丢失或无效的时间

### 屏蔽时间

```python
import numpy as np

# Create times with missing values
times = Time(['2023-01-01', '2023-06-01', '2023-12-31'])
times[1] = np.ma.masked  # Mark as missing

# Check for masks
print(times.mask)  # [False True False]

# Get unmasked version
times_clean = times.unmasked

# Fill masked values
times_filled = times.filled(Time('2000-01-01'))
```

## 时间精度和表示

### 内部表示

Time 对象使用两个 64 位浮点数（jd1、jd2）来实现高精度：

```python
t = Time('2023-01-15 12:30:45.123456789', format='iso', scale='utc')

# Access internal representation
print(t.jd1, t.jd2)  # Integer and fractional parts

# This allows sub-nanosecond precision over astronomical timescales
```

### Precision

```python
# High precision for long time intervals
t1 = Time('1900-01-01')
t2 = Time('2100-01-01')
dt = t2 - t1
print(f"Time span: {dt.sec / (365.25 * 86400)} years")
# Maintains precision throughout
```

## 时间格式化

### 自定义字符串格式

```python
t = Time('2023-01-15 12:30:45')

# Strftime-style formatting
t.strftime('%Y-%m-%d %H:%M:%S')  # '2023-01-15 12:30:45'
t.strftime('%B %d, %Y')          # 'January 15, 2023'

# ISO format subformats
t.iso                    # '2023-01-15 12:30:45.000'
t.isot                   # '2023-01-15T12:30:45.000'
t.to_value('iso', subfmt='date_hms')  # '2023-01-15 12:30:45.000'
```

## 常见用例

### 格式之间的转换

```python
# MJD to ISO
t_mjd = Time(59945.0, format='mjd')
iso_string = t_mjd.iso

# ISO to JD
t_iso = Time('2023-01-15 12:00:00')
jd_value = t_iso.jd

# Unix to ISO
t_unix = Time(1673785845.0, format='unix')
iso_string = t_unix.iso
```

### 不同单位的时间差异

```python
t1 = Time('2023-01-01')
t2 = Time('2023-12-31')

dt = t2 - t1
print(f"Days: {dt.to(u.day)}")
print(f"Hours: {dt.to(u.hour)}")
print(f"Seconds: {dt.sec}")
print(f"Years: {dt.to(u.year)}")
```

### 创建规则时间系列

```python
# Daily observations for a year
start = Time('2023-01-01')
times = start + np.arange(365) * u.day

# Hourly observations for a day
start = Time('2023-01-15 00:00:00')
times = start + np.arange(24) * u.hour

# Observations every 30 seconds
start = Time('2023-01-15 12:00:00')
times = start + np.arange(1000) * 30 * u.second
```

### 时区处理

```python
# UTC to local time (requires datetime)
t = Time('2023-01-15 12:00:00', scale='utc')
dt_utc = t.to_datetime()

# Convert to specific timezone using pytz
import pytz
eastern = pytz.timezone('US/Eastern')
dt_eastern = dt_utc.replace(tzinfo=pytz.utc).astimezone(eastern)
```

### 重心校正示例

```python
from astropy.coordinates import SkyCoord, EarthLocation

# Target coordinates
target = SkyCoord(ra='23h23m08.55s', dec='+18d24m59.3s')

# Observatory location
location = EarthLocation.of_site('Keck Observatory')

# Observation times (must include location)
times = Time(['2023-01-15 08:30:00', '2023-01-16 08:30:00'],
             location=location)

# Calculate barycentric correction
ltt_bary = times.light_travel_time(target, kind='barycentric')

# Apply correction to get barycentric times
times_bary = times.tdb + ltt_bary

# For radial velocity correction
rv_correction = ltt_bary.to(u.km, equivalencies=u.dimensionless_angles())
```

## 性能注意事项

1. **数组操作速度快**：作为数组
2进行多次处理。 **格式转换被缓存**：重复访问高效
3. **比例转换可能需要 IERS 数据**：自动下载
4. **保持高精度**：跨天文时间尺度的亚纳秒精度
