# 参数配置

## 参数对象

`Parameters` 对象是分层的并组织成逻辑组。使用点表示法访问：

```python
params = Simul.create_default_params()
params.group.subgroup.parameter = value
```

## 关键参数组

### 运算符 (`params.oper`)

定义域和分辨率：

```python
params.oper.nx = 256  # number of grid points in x
params.oper.ny = 256  # number of grid points in y
params.oper.nz = 128  # number of grid points in z (3D only)

params.oper.Lx = 2 * pi  # domain length in x
params.oper.Ly = 2 * pi  # domain length in y
params.oper.Lz = pi      # domain length in z (3D only)

params.oper.coef_dealiasing = 2./3.  # dealiasing cutoff (default 2/3)
```

* *分辨率指导**：使用 2 的幂以获得最佳 FFT性能（128、256、512、1024等）

### 物理参数

#### 粘度

```python
params.nu_2 = 1e-3  # Laplacian viscosity (negative Laplacian)
params.nu_4 = 0     # hyperviscosity (optional)
params.nu_8 = 0     # hyper-hyperviscosity (very high wavenumber damping)
```

高阶粘度（`nu_4`、`nu_8`）阻尼高波数而不影响大波数scales.

#### 分层（分层求解器）

```python
params.N = 1.0  # Brunt-Väisälä frequency (buoyancy frequency)
```

#### 旋转（浅水）

```python
params.f = 1.0  # Coriolis parameter
params.c2 = 10.0  # squared phase velocity (gravity wave speed)
```

### 时间步进(`params.time_stepping`)

```python
params.time_stepping.t_end = 10.0  # simulation end time
params.time_stepping.it_end = 100  # or maximum iterations

params.time_stepping.deltat0 = 0.01  # initial time step
params.time_stepping.USE_CFL = True  # adaptive CFL-based time step
params.time_stepping.CFL = 0.5  # CFL number (if USE_CFL=True)

params.time_stepping.type_time_scheme = "RK4"  # or "RK2", "Euler"
```

* *推荐**：将 `USE_CFL=True` 与 `CFL=0.5` 结合使用以实现自适应时间步进。

### 初始字段(`params.init_fields`)

```python
params.init_fields.type = "noise"  # initialization method
```

* *可用类型**：
- `"noise"`：随机噪声
- `"dipole"`：涡旋偶极子
- `"vortex"`：单vortex
- `"taylor_green"`：Taylor-Green vortex
- `"from_file"`：从文件加载
- `"in_script"`：在脚本中定义

#### 来自文件

```python
params.init_fields.type = "from_file"
params.init_fields.from_file.path = "path/to/state_file.h5"
```

#### 脚本中

```python
params.init_fields.type = "in_script"

# Define initialization after creating sim
sim = Simul(params)

# Access state fields
vx = sim.state.state_phys.get_var("vx")
vy = sim.state.state_phys.get_var("vy")

# Set fields
X, Y = sim.oper.get_XY_loc()
vx[:] = np.sin(X) * np.cos(Y)
vy[:] = -np.cos(X) * np.sin(Y)

# Run simulation
sim.time_stepping.start()
```

#### 输出设置(`params.output`)

#### 输出目录

```python
params.output.sub_directory = "my_simulation"
```

目录在`$FLUIDSIM_PATH`或当前目录中创建。

#### 保存周期

```python
params.output.periods_save.phys_fields = 1.0  # save fields every 1.0 time units
params.output.periods_save.spectra = 0.5      # save spectra
params.output.periods_save.spatial_means = 0.1  # save spatial averages
params.output.periods_save.spect_energy_budg = 0.5  # spectral energy budget
```

设置为`0`以禁用特定输出类型。

#### 打印控制

```python
params.output.periods_print.print_stdout = 0.5  # print status every 0.5 time units
```

#### 在线绘图

```python
params.output.periods_plot.phys_fields = 2.0  # plot every 2.0 time units

# Must also enable the output module
params.output.ONLINE_PLOT_OK = True
params.output.phys_fields.field_to_plot = "vorticity"  # or "vx", "vy", etc.
```

### 强制(`params.forcing`)

添加强制项以维护能量：

```python
params.forcing.enable = True
params.forcing.type = "tcrandom"  # time-correlated random forcing

# Forcing parameters
params.forcing.nkmax_forcing = 5  # maximum forced wavenumber
params.forcing.nkmin_forcing = 2  # minimum forced wavenumber
params.forcing.forcing_rate = 1.0  # energy injection rate
```

* *常见强迫类型**：
- `"tcrandom"`：时间相关随机强迫
- `"proportional"`：比例强迫（保持特定频谱）
- `"in_script"`：脚本中定义的自定义强制

## 参数安全

参数对象在访问不存在的参数时引发`AttributeError`：

```python
params.nu_2 = 1e-3  # OK
params.nu2 = 1e-3   # ERROR: AttributeError
```

这可以防止在基于文本的配置文件中被静默忽略的拼写错误。

## 查看所有参数

```python
# Print all parameters
params._print_as_xml()

# Get as dictionary
param_dict = params._make_dict()
```

## 保存参数配置

参数随模拟输出自动保存：

```python
params._save_as_xml("simulation_params.xml")
params._save_as_json("simulation_params.json")
```
