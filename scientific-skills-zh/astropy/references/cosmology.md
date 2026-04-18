# 宇宙学计算（astropy.cosmology）

`astropy.cosmology`子包提供了基于各种宇宙学模型进行宇宙学计算的工具。

## 使用内置宇宙学

基于WMAP和普朗克的预加载宇宙学观测值：

```python
from astropy.cosmology import Planck18, Planck15, Planck13
from astropy.cosmology import WMAP9, WMAP7, WMAP5
from astropy import units as u

# Use Planck 2018 cosmology
cosmo = Planck18

# Calculate distance to z=4
d = cosmo.luminosity_distance(4)
print(f"Luminosity distance at z=4: {d}")

# Age of universe at z=0
age = cosmo.age(0)
print(f"Current age of universe: {age.to(u.Gyr)}")
```

## 创建自定义宇宙学

### FlatLambdaCDM（最常见）

具有宇宙学常数的平坦宇宙：

```python
from astropy.cosmology import FlatLambdaCDM

# Define cosmology
cosmo = FlatLambdaCDM(
    H0=70 * u.km / u.s / u.Mpc,  # Hubble constant at z=0
    Om0=0.3,                      # Matter density parameter at z=0
    Tcmb0=2.725 * u.K             # CMB temperature (optional)
)
```

### LambdaCDM （非平坦）

具有宇宙学常数的非平坦宇宙：

```python
from astropy.cosmology import LambdaCDM

cosmo = LambdaCDM(
    H0=70 * u.km / u.s / u.Mpc,
    Om0=0.3,
    Ode0=0.7  # Dark energy density parameter
)
```

### wCDM和w0wzCDM

具有状态方程参数的暗能量：

```python
from astropy.cosmology import FlatwCDM, w0wzCDM

# Constant w
cosmo_w = FlatwCDM(H0=70 * u.km/u.s/u.Mpc, Om0=0.3, w0=-0.9)

# Evolving w(z) = w0 + wz * z
cosmo_wz = w0wzCDM(H0=70 * u.km/u.s/u.Mpc, Om0=0.3, Ode0=0.7,
                   w0=-1.0, wz=0.1)
```

## 距离计算

### 同动距离

视线同动距离：

```python
d_c = cosmo.comoving_distance(z)
```

### 光度距离

根据观测计算光度的距离通量:

```python
d_L = cosmo.luminosity_distance(z)

# Calculate absolute magnitude from apparent magnitude
M = m - 5*np.log10(d_L.to(u.pc).value) + 5
```

### 角直径距离

从角度尺寸计算物理尺寸的距离:

```python
d_A = cosmo.angular_diameter_distance(z)

# Calculate physical size from angular size
theta = 10 * u.arcsec  # Angular size
physical_size = d_A * theta.to(u.radian).value
```

### 同动横向距离

横向同移距离（等于平坦宇宙中的同移距离）：

```python
d_M = cosmo.comoving_transverse_distance(z)
```

### 距离模量

```python
dm = cosmo.distmod(z)
# Relates apparent and absolute magnitudes: m - M = dm
```

## 尺度计算

### kpc 每弧分

给定物理尺度redshift:

```python
scale = cosmo.kpc_proper_per_arcmin(z)
# e.g., "50 kpc per arcminute at z=1"
```

### 移动体积

测量体积计算的体积元素:

```python
vol = cosmo.comoving_volume(z)  # Total volume to redshift z
vol_element = cosmo.differential_comoving_volume(z)  # dV/dz
```

## 时间计算

### 给定宇宙的年龄

Age redshift:

```python
age = cosmo.age(z)
age_now = cosmo.age(0)  # Current age
age_at_z1 = cosmo.age(1)  # Age at z=1
```

### Lookback Time

自光子发射以来的时间:

```python
t_lookback = cosmo.lookback_time(z)
# Time between z and z=0
```

## Hubble Parameter

Hubble 参数作为函数redshift:

```python
H_z = cosmo.H(z)  # H(z) in km/s/Mpc
E_z = cosmo.efunc(z)  # E(z) = H(z)/H0
```

## 密度参数

E 密度参数与红移的演化：

```python
Om_z = cosmo.Om(z)        # Matter density at z
Ode_z = cosmo.Ode(z)      # Dark energy density at z
Ok_z = cosmo.Ok(z)        # Curvature density at z
Ogamma_z = cosmo.Ogamma(z)  # Photon density at z
Onu_z = cosmo.Onu(z)      # Neutrino density at z
```

## 关键和特征密度

```python
rho_c = cosmo.critical_density(z)  # Critical density at z
rho_m = cosmo.critical_density(z) * cosmo.Om(z)  # Matter density
```

## 反演计算

查找特定值对应的红移：

```python
from astropy.cosmology import z_at_value

# Find z at specific lookback time
z = z_at_value(cosmo.lookback_time, 10*u.Gyr)

# Find z at specific luminosity distance
z = z_at_value(cosmo.luminosity_distance, 1000*u.Mpc)

# Find z at specific age
z = z_at_value(cosmo.age, 1*u.Gyr)
```

## 数组操作

所有方法都接受数组输入：

```python
import numpy as np

z_array = np.linspace(0, 5, 100)
d_L_array = cosmo.luminosity_distance(z_array)
H_array = cosmo.H(z_array)
age_array = cosmo.age(z_array)
```

## 中微子效应

包括大量中微子：

```python
from astropy.cosmology import FlatLambdaCDM

# With massive neutrinos
cosmo = FlatLambdaCDM(
    H0=70 * u.km/u.s/u.Mpc,
    Om0=0.3,
    Tcmb0=2.725 * u.K,
    Neff=3.04,  # Effective number of neutrino species
    m_nu=[0., 0., 0.06] * u.eV  # Neutrino masses
)
```

注意：大量中微子使性能降低 3-4 倍，但提供更准确的结果。

## 克隆和修改宇宙学

宇宙学对象是不可变的。创建修改后的副本：

```python
# Clone with different H0
cosmo_new = cosmo.clone(H0=72 * u.km/u.s/u.Mpc)

# Clone with modified name
cosmo_named = cosmo.clone(name="My Custom Cosmology")
```

## 常见用例

### 计算绝对幅度

```python
# From apparent magnitude and redshift
z = 1.5
m_app = 24.5  # Apparent magnitude
d_L = cosmo.luminosity_distance(z)
M_abs = m_app - cosmo.distmod(z).value
```

### 测量体积计算

```python
# Volume between two redshifts
z_min, z_max = 0.5, 1.5
volume = cosmo.comoving_volume(z_max) - cosmo.comoving_volume(z_min)

# Convert to Gpc^3
volume_gpc3 = volume.to(u.Gpc**3)
```

### 物理尺寸角度大小

```python
theta = 1 * u.arcsec  # Angular size
z = 2.0
d_A = cosmo.angular_diameter_distance(z)
size_kpc = (d_A * theta.to(u.radian)).to(u.kpc)
```

#### 大爆炸以来的时间

```python
# Age at specific redshift
z_formation = 6
age_at_formation = cosmo.age(z_formation)
time_since_formation = cosmo.age(0) - age_at_formation
```

## 宇宙学比较

```python
# Compare different models
from astropy.cosmology import Planck18, WMAP9

z = 1.0
print(f"Planck18 d_L: {Planck18.luminosity_distance(z)}")
print(f"WMAP9 d_L: {WMAP9.luminosity_distance(z)}")
```

## 性能考虑

- 计算对于大多数用途来说速度很快
- 大量中微子显着降低速度
- 阵列操作矢量化且高效
- 结果对 z < 5000-6000 有效（取决于型号）
