# 输出和分析

## 输出类型

FluidSim 在模拟过程中自动保存多种类型的输出。

### 物理场

* *文件格式**: HDF5 (`.h5`)

* *位置**: `simulation_dir/state_phys_t*.h5`

* *内容**:特定时间的速度、涡度和其他物理空间场

* *访问**：
```python
sim.output.phys_fields.plot()
sim.output.phys_fields.plot("vorticity")
sim.output.phys_fields.plot("vx")
sim.output.phys_fields.plot("div")  # check divergence

# Save manually
sim.output.phys_fields.save()

# Get data
vorticity = sim.state.state_phys.get_var("rot")
```

### 空间手段

* *文件格式**：文本文件（`.txt`）

* *位置**： `simulation_dir/spatial_means.txt`

* *内容**：体积平均量与时间（能量、熵等）

* *访问**：
```python
sim.output.spatial_means.plot()

# Load from file
from fluidsim import load_sim_for_plot
sim = load_sim_for_plot("simulation_dir")
sim.output.spatial_means.load()
spatial_means_data = sim.output.spatial_means
```

### Spectra

* *文件格式**：HDF5 (`.h5`)

* *位置**：`simulation_dir/spectra_*.h5`

* *内容**：能量和熵光谱与波数

* *访问**：
```python
sim.output.spectra.plot1d()  # 1D spectrum
sim.output.spectra.plot2d()  # 2D spectrum

# Load spectra data
spectra = sim.output.spectra.load2d_mean()
```

### 光谱能量预算

* *文件格式**：HDF5 (`.h5`)

* *位置**：`simulation_dir/spect_energy_budg_*.h5`

* *内容**：秤之间的能量传输

* *访问**：
```python
sim.output.spect_energy_budg.plot()
```

## 后处理

### 加载分析模拟

#### 快速加载（只读）

```python
from fluidsim import load_sim_for_plot

sim = load_sim_for_plot("simulation_dir")

# Access all output types
sim.output.phys_fields.plot()
sim.output.spatial_means.plot()
sim.output.spectra.plot1d()
```

 使用此功能进行快速可视化和分析。不初始化完整模拟状态。

#### 完整状态加载

```python
from fluidsim import load_state_phys_file

sim = load_state_phys_file("simulation_dir/state_phys_t10.000.h5")

# Can continue simulation
sim.time_stepping.start()
```

#### 可视化工具

#### 内置绘图

FluidSim通过以下方式提供基本绘图matplotlib:

```python
# Physical fields
sim.output.phys_fields.plot("vorticity")
sim.output.phys_fields.animate("vorticity")

# Time series
sim.output.spatial_means.plot()

# Spectra
sim.output.spectra.plot1d()
```

#### 高级可视化

对于出版质量或 3D 可视化：

* *ParaView**：打开 `.h5` 文件直接
```bash
paraview simulation_dir/state_phys_t*.h5
```

* *VisIt**：类似于大型数据集的ParaView

* *自定义Python**：
```python
import h5py
import matplotlib.pyplot as plt

# Load field manually
with h5py.File("state_phys_t10.000.h5", "r") as f:
    vx = f["state_phys"]["vx"][:]
    vy = f["state_phys"]["vy"][:]

# Custom plotting
plt.contourf(vx)
plt.show()
```

## 分析示例

### 能源演化

```python
from fluidsim import load_sim_for_plot
import matplotlib.pyplot as plt

sim = load_sim_for_plot("simulation_dir")
df = sim.output.spatial_means.load()

plt.figure()
plt.plot(df["t"], df["E"], label="Kinetic Energy")
plt.xlabel("Time")
plt.ylabel("Energy")
plt.legend()
plt.show()
```

### 光谱分析

```python
sim = load_sim_for_plot("simulation_dir")

# Plot energy spectrum
sim.output.spectra.plot1d(tmin=5.0, tmax=10.0)  # average over time range

# Get spectral data
k, E_k = sim.output.spectra.load1d_mean(tmin=5.0, tmax=10.0)

# Check for power law
import numpy as np
log_k = np.log(k)
log_E = np.log(E_k)
# fit power law in inertial range
```

### 参数研究分析

使用不同参数运行多个仿真时：

```python
import os
import pandas as pd
from fluidsim import load_sim_for_plot

# Collect results from multiple simulations
results = []
for sim_dir in os.listdir("simulations"):
    if not os.path.isdir(f"simulations/{sim_dir}"):
        continue

    sim = load_sim_for_plot(f"simulations/{sim_dir}")

    # Extract key metrics
    df = sim.output.spatial_means.load()
    final_energy = df["E"].iloc[-1]

    # Get parameters
    nu = sim.params.nu_2

    results.append({
        "nu": nu,
        "final_energy": final_energy,
        "sim_dir": sim_dir
    })

# Analyze results
results_df = pd.DataFrame(results)
results_df.plot(x="nu", y="final_energy", logx=True)
```

### 字段操作

```python
sim = load_sim_for_plot("simulation_dir")

# Load specific time
sim.output.phys_fields.set_of_phys_files.update_times()
times = sim.output.phys_fields.set_of_phys_files.times

# Load field at specific time
field_file = sim.output.phys_fields.get_field_to_plot(time=5.0)
vorticity = field_file.get_var("rot")

# Compute derived quantities
import numpy as np
vorticity_rms = np.sqrt(np.mean(vorticity**2))
vorticity_max = np.max(np.abs(vorticity))
```

## 输出目录结构

```
simulation_dir/
├── params_simul.xml         # Simulation parameters
├── stdout.txt               # Standard output log
├── state_phys_t*.h5         # Physical fields at different times
├── spatial_means.txt        # Time series of spatial averages
├── spectra_*.h5            # Spectral data
├── spect_energy_budg_*.h5  # Energy budget data
└── info_solver.txt         # Solver information
```

## 性能监控

```python
# During simulation, check progress
sim.output.print_stdout.complete_timestep()

# After simulation, review performance
sim.output.print_stdout.plot_deltat()  # plot time step evolution
sim.output.print_stdout.plot_clock_times()  # plot computation time
```

## 数据导出

转换fluidsim输出为其他格式：

```python
import h5py
import numpy as np

# Export to numpy array
with h5py.File("state_phys_t10.000.h5", "r") as f:
    vx = f["state_phys"]["vx"][:]
    np.save("vx.npy", vx)

# Export to CSV
df = sim.output.spatial_means.load()
df.to_csv("spatial_means.csv", index=False)
```
