# FluidSim Solvers

FluidSim 为不同的流体动力学方程提供了多个求解器。所有求解器均使用 FFT 伪谱方法在周期域上工作。

## 可用求解器

### 2D 不可压缩纳维斯托克斯

* *求解器密钥**：ZXQINLINE0QX

* *导入**：
```python
from fluidsim.solvers.ns2d.solver import Simul
# or dynamically
Simul = fluidsim.import_simul_class_from_key("ns2d")
```

* *使用用于**：2D 湍流研究、涡动力学、基本流体流动模拟

* *主要功能**：能量和熵级联、涡量动力学

### 3D 不可压缩纳维-斯托克斯

* *求解器密钥**： `ns3d`

* *导入**：
```python
from fluidsim.solvers.ns3d.solver import Simul
```

* *用途**：3D 湍流、真实流体模拟、高分辨率 DNS

* *主要功能**：完整 3D 湍流动力学、并行计算支持

### 分层流(2D/3D)

* *解算器键**：`ns2d.strat`、`ns3d.strat`

* *导入**：
```python
from fluidsim.solvers.ns2d.strat.solver import Simul  # 2D
from fluidsim.solvers.ns3d.strat.solver import Simul  # 3D
```

* *用于**：海洋和大气流、密度驱动流

* *主要功能**：Boussinesq近似、浮力效应、恒定 Brunt-Väisälä 频率

* *参数**：通过 `params.N` 设置分层（Brunt-Väisälä 频率）

### 浅水方程

* *求解器密钥**：`sw1l` （一层）

* *导入**：
```python
from fluidsim.solvers.sw1l.solver import Simul
```

* *用途**：地球物理流、海啸建模、旋转流

* *主要功能**：旋转框架支撑、地转平衡

* *参数**：通过`params.f`设置旋转（科里奥利参数）

### Föppl-von Kármán 方程

* *求解器密钥**：`fvk`（弹性板方程）

* *导入**：
```python
from fluidsim.solvers.fvk.solver import Simul
```

* *用于**：弹性板动力学，流固耦合研究

## 求解器选择指南

根据物理问题选择求解器：

1. **二维湍流，快速测试**：使用`ns2d`
2. **3D 流动，真实模拟**：使用 `ns3d`
3. **密度分层流**：使用 `ns2d.strat` 或 `ns3d.strat`
4. **地球物理流，旋转系统**：使用 `sw1l`
5. **弹性板**：使用 `fvk`

## 修改版本

许多求解器都修改了带有附加物理场的版本：
- 强制项
- 不同的边界条件
- 附加标量场

 检查 `fluidsim.solvers` 模块以获得完整的结果列表.
