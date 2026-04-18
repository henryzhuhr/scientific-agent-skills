# 高级功能

## 自定义强制

### 强制类型

FluidSim 支持多种强制机制来维持湍流或驱动特定动态。

#### 时间相关随机强制

最常见于持续湍流：

```python
params.forcing.enable = True
params.forcing.type = "tcrandom"
params.forcing.nkmin_forcing = 2  # minimum forced wavenumber
params.forcing.nkmax_forcing = 5  # maximum forced wavenumber
params.forcing.forcing_rate = 1.0  # energy injection rate
params.forcing.tcrandom_time_correlation = 1.0  # correlation time
```

#### 比例强迫

维持特定的能量分布：

```python
params.forcing.type = "proportional"
params.forcing.forcing_rate = 1.0
```

#### 脚本中的自定义强迫

直接在启动中定义强迫脚本：

```python
params.forcing.enable = True
params.forcing.type = "in_script"

sim = Simul(params)

# Define custom forcing function
def compute_forcing_fft(sim):
    """Compute forcing in Fourier space"""
    forcing_vx_fft = sim.oper.create_arrayK(value=0.)
    forcing_vy_fft = sim.oper.create_arrayK(value=0.)

    # Add custom forcing logic
    # Example: force specific modes
    forcing_vx_fft[10, 10] = 1.0 + 0.5j

    return forcing_vx_fft, forcing_vy_fft

# Override forcing method
sim.forcing.forcing_maker.compute_forcing_fft = lambda: compute_forcing_fft(sim)

# Run simulation
sim.time_stepping.start()
```

## 自定义初始条件

### 脚本内初始化

完全控制初始字段：

```python
from math import pi
import numpy as np

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = 256
params.oper.Lx = params.oper.Ly = 2 * pi

params.init_fields.type = "in_script"

sim = Simul(params)

# Get coordinate arrays
X, Y = sim.oper.get_XY_loc()

# Define velocity fields
vx = sim.state.state_phys.get_var("vx")
vy = sim.state.state_phys.get_var("vy")

# Taylor-Green vortex
vx[:] = np.sin(X) * np.cos(Y)
vy[:] = -np.cos(X) * np.sin(Y)

# Initialize state in Fourier space
sim.state.statephys_from_statespect()

# Run simulation
sim.time_stepping.start()
```

### 层初始化（分层流）

设置密度层：

```python
from fluidsim.solvers.ns2d.strat.solver import Simul

params = Simul.create_default_params()
params.N = 1.0  # stratification
params.init_fields.type = "in_script"

sim = Simul(params)

# Define dense layer
X, Y = sim.oper.get_XY_loc()
b = sim.state.state_phys.get_var("b")  # buoyancy field

# Gaussian density anomaly
x0, y0 = pi, pi
sigma = 0.5
b[:] = np.exp(-((X - x0)**2 + (Y - y0)**2) / (2 * sigma**2))

sim.state.statephys_from_statespect()
sim.time_stepping.start()
```

## 使用MPI进行并行计算

### 运行MPI模拟

使用MPI支持安装：
```bash
uv pip install "fluidsim[fft,mpi]"
```

运行MPI:
```bash
mpirun -np 8 python simulation_script.py
```

FluidSim 自动检测 MPI 并分配计算。

### MPI 特定参数

```python
# No special parameters needed
# FluidSim handles domain decomposition automatically

# For very large 3D simulations
params.oper.nx = 512
params.oper.ny = 512
params.oper.nz = 512

# Run with: mpirun -np 64 python script.py
```

### 使用 MPI

输出输出文件从 0 级处理器写入。分析脚本对于串行和 MPI 运行的工作方式相同。

## 参数研究

### 运行多个模拟

用于生成和运行多个参数组合的脚本：

```python
from fluidsim.solvers.ns2d.solver import Simul
import numpy as np

# Parameter ranges
viscosities = [1e-3, 5e-4, 1e-4, 5e-5]
resolutions = [128, 256, 512]

for nu in viscosities:
    for nx in resolutions:
        params = Simul.create_default_params()

        # Configure simulation
        params.oper.nx = params.oper.ny = nx
        params.nu_2 = nu
        params.time_stepping.t_end = 10.0

        # Unique output directory
        params.output.sub_directory = f"nu{nu}_nx{nx}"

        # Run simulation
        sim = Simul(params)
        sim.time_stepping.start()
```

### 集群提交

将多个作业提交到一个cluster:

```python
from fluiddyn.clusters.legi import Calcul8 as Cluster

cluster = Cluster()

for nu in viscosities:
    for nx in resolutions:
        script_content = f"""
from fluidsim.solvers.ns2d.solver import Simul

params = Simul.create_default_params()
params.oper.nx = params.oper.ny = {nx}
params.nu_2 = {nu}
params.time_stepping.t_end = 10.0
params.output.sub_directory = "nu{nu}_nx{nx}"

sim = Simul(params)
sim.time_stepping.start()
"""

        with open(f"job_nu{nu}_nx{nx}.py", "w") as f:
            f.write(script_content)

        cluster.submit_script(
            f"job_nu{nu}_nx{nx}.py",
            name_run=f"sim_nu{nu}_nx{nx}",
            nb_nodes=1,
            nb_cores_per_node=24,
            walltime="12:00:00"
        )
```

### 分析参数研究

```python
import os
import pandas as pd
from fluidsim import load_sim_for_plot
import matplotlib.pyplot as plt

results = []

# Collect data from all simulations
for sim_dir in os.listdir("simulations"):
    sim_path = f"simulations/{sim_dir}"
    if not os.path.isdir(sim_path):
        continue

    try:
        sim = load_sim_for_plot(sim_path)

        # Extract parameters
        nu = sim.params.nu_2
        nx = sim.params.oper.nx

        # Extract results
        df = sim.output.spatial_means.load()
        final_energy = df["E"].iloc[-1]
        mean_energy = df["E"].mean()

        results.append({
            "nu": nu,
            "nx": nx,
            "final_energy": final_energy,
            "mean_energy": mean_energy
        })
    except Exception as e:
        print(f"Error loading {sim_dir}: {e}")

# Analyze results
results_df = pd.DataFrame(results)

# Plot results
plt.figure(figsize=(10, 6))
for nx in results_df["nx"].unique():
    subset = results_df[results_df["nx"] == nx]
    plt.plot(subset["nu"], subset["mean_energy"],
             marker="o", label=f"nx={nx}")

plt.xlabel("Viscosity")
plt.ylabel("Mean Energy")
plt.xscale("log")
plt.legend()
plt.savefig("parametric_study_results.png")
```

## 自定义求解器

### 扩展现有求解器

通过继承现有求解器创建新求解器一：

```python
from fluidsim.solvers.ns2d.solver import Simul as SimulNS2D
from fluidsim.base.setofvariables import SetOfVariables

class SimulCustom(SimulNS2D):
    """Custom solver with additional physics"""

    @staticmethod
    def _complete_params_with_default(params):
        """Add custom parameters"""
        SimulNS2D._complete_params_with_default(params)
        params._set_child("custom", {"param1": 0.0})

    def __init__(self, params):
        super().__init__(params)
        # Custom initialization

    def tendencies_nonlin(self, state_spect=None):
        """Override to add custom tendencies"""
        tendencies = super().tendencies_nonlin(state_spect)

        # Add custom terms
        # tendencies.vx_fft += custom_term_vx
        # tendencies.vy_fft += custom_term_vy

        return tendencies
```

使用自定义求解器：
```python
params = SimulCustom.create_default_params()
# Configure params...
sim = SimulCustom(params)
sim.time_stepping.start()
```

## 在线可视化

仿真时显示字段：

```python
params.output.ONLINE_PLOT_OK = True
params.output.periods_plot.phys_fields = 1.0  # plot every 1.0 time units
params.output.phys_fields.field_to_plot = "vorticity"

sim = Simul(params)
sim.time_stepping.start()
```

绘图实时显示

## 检查点和重新启动

### 自动检查点

```python
params.output.periods_save.phys_fields = 1.0  # save every 1.0 time units
```

 仿真过程中自动保存字段。

### 手动检查点

```python
# During simulation
sim.output.phys_fields.save()
```

### 从检查点

```python
params = Simul.create_default_params()
params.init_fields.type = "from_file"
params.init_fields.from_file.path = "simulation_dir/state_phys_t5.000.h5"
params.time_stepping.t_end = 20.0  # extend simulation

sim = Simul(params)
sim.time_stepping.start()
```

## 内存和性能优化

### 减少内存使用

```python
# Disable unnecessary outputs
params.output.periods_save.spectra = 0  # disable spectra saving
params.output.periods_save.spect_energy_budg = 0  # disable energy budget

# Reduce spatial field saves
params.output.periods_save.phys_fields = 10.0  # save less frequently
```

### 优化FFT性能

```python
import os

# Select FFT library
os.environ["FLUIDSIM_TYPE_FFT2D"] = "fft2d.with_fftw"
os.environ["FLUIDSIM_TYPE_FFT3D"] = "fft3d.with_fftw"

# Or use MKL if available
# os.environ["FLUIDSIM_TYPE_FFT2D"] = "fft2d.with_mkl"
```

### 时间步优化

```python
# Use adaptive time stepping
params.time_stepping.USE_CFL = True
params.time_stepping.CFL = 0.8  # slightly larger CFL for faster runs

# Use efficient time scheme
params.time_stepping.type_time_scheme = "RK4"  # 4th order Runge-Kutta
```
