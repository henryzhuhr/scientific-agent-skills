# 模拟工作流程

## 标准工作流程

按照以下步骤运行 fluidsim 模拟：

### 1. 导入求解器

```python
from fluidsim.solvers.ns2d.solver import Simul

# Or use dynamic import
import fluidsim
Simul = fluidsim.import_simul_class_from_key("ns2d")
```

### 2. 创建默认值参数

```python
params = Simul.create_default_params()
```

这将返回包含所有模拟设置的分层`Parameters`对象。

### 3.配置参数

根据需要修改参数。参数对象通过针对不存在的参数引发 `AttributeError` 来防止拼写错误：

```python
# Domain and resolution
params.oper.nx = 256  # grid points in x
params.oper.ny = 256  # grid points in y
params.oper.Lx = 2 * pi  # domain size x
params.oper.Ly = 2 * pi  # domain size y

# Physical parameters
params.nu_2 = 1e-3  # viscosity (negative Laplacian)

# Time stepping
params.time_stepping.t_end = 10.0  # end time
params.time_stepping.deltat0 = 0.01  # initial time step
params.time_stepping.USE_CFL = True  # adaptive time step

# Initial conditions
params.init_fields.type = "noise"  # or "dipole", "vortex", etc.

# Output settings
params.output.periods_save.phys_fields = 1.0  # save every 1.0 time units
params.output.periods_save.spectra = 0.5
params.output.periods_save.spatial_means = 0.1
```

### 4. 实例化仿真

```python
sim = Simul(params)
```

此初始化：
- 运算符（FFT、微分）运算符）
- 状态变量（速度、涡度等）
- 输出处理程序
- 时间步进方案

### 5. 运行仿真

```python
sim.time_stepping.start()
```

 仿真运行直到 `t_end` 或指定数量的

### 6. 仿真期间/之后分析结果

```python
# Plot physical fields
sim.output.phys_fields.plot()
sim.output.phys_fields.plot("vorticity")
sim.output.phys_fields.plot("div")

# Plot spatial means
sim.output.spatial_means.plot()

# Plot spectra
sim.output.spectra.plot1d()
sim.output.spectra.plot2d()
```

## 加载先前的仿真

### 快速加载（仅用于绘图）

```python
from fluidsim import load_sim_for_plot

sim = load_sim_for_plot("path/to/simulation")
sim.output.phys_fields.plot()
sim.output.spatial_means.plot()
```

 快速加载，无需完全状态初始化。用于后处理。

### 完整状态加载（用于重新启动）

```python
from fluidsim import load_state_phys_file

sim = load_state_phys_file("path/to/state_file.h5")
sim.time_stepping.start()  # continue simulation
```

加载完整状态以继续模拟。

## 重新启动模拟

从保存的重新启动state:

```python
params = Simul.create_default_params()
params.init_fields.type = "from_file"
params.init_fields.from_file.path = "path/to/state_file.h5"

# Optionally modify parameters for the continuation
params.time_stepping.t_end = 20.0  # extend simulation

sim = Simul(params)
sim.time_stepping.start()
```

## 在集群上运行

FluidSim 与集群提交系统集成：

```python
from fluiddyn.clusters.legi import Calcul8 as Cluster

# Configure cluster job
cluster = Cluster()
cluster.submit_script(
    "my_simulation.py",
    name_run="my_job",
    nb_nodes=4,
    nb_cores_per_node=24,
    walltime="24:00:00"
)
```

Script 应包含标准工作流程步骤（导入、配置、运行）。

## 完成示例

```python
from fluidsim.solvers.ns2d.solver import Simul
from math import pi

# Create and configure parameters
params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 256
params.oper.Lx = params.oper.Ly = 2 * pi
params.nu_2 = 1e-3
params.time_stepping.t_end = 10.0
params.init_fields.type = "dipole"
params.output.periods_save.phys_fields = 1.0

# Run simulation
sim = Simul(params)
sim.time_stepping.start()

# Analyze results
sim.output.phys_fields.plot("vorticity")
sim.output.spatial_means.plot()
```
