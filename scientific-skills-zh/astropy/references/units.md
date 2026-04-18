# 单位和数量 (astropy.units)

`astropy.units` 模块处理物理量的定义、转换和算术运算。

## 创建数量

将数值乘以或除以内置单位以创建数量对象：

```python
from astropy import units as u
import numpy as np

# Scalar quantities
distance = 42.0 * u.meter
velocity = 100 * u.km / u.s

# Array quantities
distances = np.array([1., 2., 3.]) * u.m
wavelengths = [500, 600, 700] * u.nm
```

通过`.value`和`.unit`访问组件属性：
```python
distance.value  # 42.0
distance.unit   # Unit("m")
```

## 单位转换

使用`.to()`方法转换：

```python
distance = 1.0 * u.parsec
distance.to(u.km)  # <Quantity 30856775814671.914 km>

wavelength = 500 * u.nm
wavelength.to(u.angstrom)  # <Quantity 5000. Angstrom>
```

## 算术运算

数量支持具有自动单位管理的标准算术：

```python
# Basic operations
speed = 15.1 * u.meter / (32.0 * u.second)  # <Quantity 0.471875 m / s>
area = (5 * u.m) * (3 * u.m)  # <Quantity 15. m2>

# Units cancel when appropriate
ratio = (10 * u.m) / (5 * u.m)  # <Quantity 2. (dimensionless)>

# Decompose complex units
time = (3.0 * u.kilometer / (130.51 * u.meter / u.second))
time.decompose()  # <Quantity 22.986744310780782 s>
```

## 单位系统

主要单位之间的转换系统：

```python
# SI to CGS
pressure = 1.0 * u.Pa
pressure.cgs  # <Quantity 10. Ba>

# Find equivalent representations
(u.s ** -1).compose()  # [Unit("Bq"), Unit("Hz"), ...]
```

## 等价

特定于域的转换需要等价：

```python
# Spectral equivalency (wavelength ↔ frequency)
wavelength = 1000 * u.nm
wavelength.to(u.Hz, equivalencies=u.spectral())
# <Quantity 2.99792458e+14 Hz>

# Doppler equivalencies
velocity = 1000 * u.km / u.s
velocity.to(u.Hz, equivalencies=u.doppler_optical(500*u.nm))

# Other equivalencies
u.brightness_temperature(500*u.GHz)
u.doppler_radio(1.4*u.GHz)
u.mass_energy()
u.parallax()
```

## 对数单位

用于幅度、分贝和dex:

```python
# Magnitudes
flux = -2.5 * u.mag(u.ct / u.s)

# Decibels
power_ratio = 3 * u.dB(u.W)

# Dex (base-10 logarithm)
abundance = 8.5 * u.dex(u.cm**-3)
```

## 常用单位

### 长度
`u.m, u.km, u.cm, u.mm, u.micron, u.angstrom, u.au, u.pc, u.kpc, u.Mpc, u.lyr`

### 时间
`u.s, u.min, u.hour, u.day, u.year, u.Myr, u.Gyr`

### 质量
`u.kg, u.g, u.M_sun, u.M_earth, u.M_jup`

### 温度
`u.K, u.deg_C`

### 角度
`u.deg, u.arcmin, u.arcsec, u.rad, u.hourangle, u.mas`

### 能量/功率
`u.J, u.erg, u.eV, u.keV, u.MeV, u.GeV, u.W, u.L_sun`

### 频率
`u.Hz, u.kHz, u.MHz, u.GHz`

### Flux
`u.Jy, u.mJy, u.erg / u.s / u.cm**2`

## 性能优化

数组操作的预计算复合单元：

```python
# Slow (creates intermediate quantities)
result = array * u.m / u.s / u.kg / u.sr

# Fast (pre-computed composite unit)
UNIT_COMPOSITE = u.m / u.s / u.kg / u.sr
result = array * UNIT_COMPOSITE

# Fastest (avoid copying with <<)
result = array << UNIT_COMPOSITE  # 10000x faster
```

## 字符串格式化

使用标准Python格式化数量语法：

```python
velocity = 15.1 * u.meter / (32.0 * u.second)
f"{velocity:0.03f}"     # '0.472 m / s'
f"{velocity:.2e}"       # '4.72e-01 m / s'
f"{velocity.unit:FITS}" # 'm s-1'
```

## 定义自定义单位

```python
# Create new unit
bakers_fortnight = u.def_unit('bakers_fortnight', 13 * u.day)

# Enable in string parsing
u.add_enabled_units([bakers_fortnight])
```

## 常量

使用单位访问物理常量：

```python
from astropy.constants import c, G, M_sun, h, k_B

speed_of_light = c.to(u.km/u.s)
gravitational_constant = G.to(u.m**3 / u.kg / u.s**2)
```
