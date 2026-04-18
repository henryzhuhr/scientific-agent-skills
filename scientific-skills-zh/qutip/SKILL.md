---
name: qutip
description: 开放量子系统的量子物理模拟库。在研究主方程、Lindblad 动力学、退相干、量子光学或腔 QED 时使用。最适合物理研究、开放系统动力学和教育模拟。不适用于基于电路的量子计算 - 使用 qiskit、cirq 或 pennylane 进行量子算法和硬件执行。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# QuTiP：Python 中的量子工具箱

## 概述

QuTiP 提供用于模拟和分析量子力学系统的综合工具。它可以处理封闭（酉）和开放（耗散）量子系统，并具有针对不同场景优化的多个求解器。

## 安装

```bash
uv pip install qutip
```

用于附加功能的可选包：

```bash
# Quantum information processing (circuits, gates)
uv pip install qutip-qip

# Quantum trajectory viewer
uv pip install qutip-qtrl
```

## 快速开始

```python
from qutip import *
import numpy as np
import matplotlib.pyplot as plt

# Create quantum state
psi = basis(2, 0)  # |0⟩ state

# Create operator
H = sigmaz()  # Hamiltonian

# Time evolution
tlist = np.linspace(0, 10, 100)
result = sesolve(H, psi, tlist, e_ops=[sigmaz()])

# Plot results
plt.plot(tlist, result.expect[0])
plt.xlabel('Time')
plt.ylabel('⟨σz⟩')
plt.show()
```

## 核心功能

### 1.量子对象和状态

创建和操纵量子态和运算符：

```python
# States
psi = basis(N, n)  # Fock state |n⟩
psi = coherent(N, alpha)  # Coherent state |α⟩
rho = thermal_dm(N, n_avg)  # Thermal density matrix

# Operators
a = destroy(N)  # Annihilation operator
H = num(N)  # Number operator
sx, sy, sz = sigmax(), sigmay(), sigmaz()  # Pauli matrices

# Composite systems
psi_AB = tensor(psi_A, psi_B)  # Tensor product
```

* *参见**`references/core_concepts.md`全面覆盖量子对象、状态、运算符、 

### 2. 时间演化和动力学

针对不同场景的多种求解器：

```python
# Closed systems (unitary evolution)
result = sesolve(H, psi0, tlist, e_ops=[num(N)])

# Open systems (dissipation)
c_ops = [np.sqrt(0.1) * destroy(N)]  # Collapse operators
result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])

# Quantum trajectories (Monte Carlo)
result = mcsolve(H, psi0, tlist, c_ops, ntraj=500, e_ops=[num(N)])
```

* *求解器选择指南：**
- `sesolve`：纯状态，酉演化
- `mesolve`：混合态、耗散、通用开放系统
- `mcsolve`：量子跃迁、光子计数、单独轨迹
- `brmesolve`：弱系统浴耦合
- `fmmesolve`：时间周期哈密顿量(Floquet)

* *请参见** `references/time_evolution.md` 了解详细的求解器文档、瞬态哈密顿量和高级选项。

### 3. 分析和测量

计算物理量：

```python
# Expectation values
n_avg = expect(num(N), psi)

# Entropy measures
S = entropy_vn(rho)  # Von Neumann entropy
C = concurrence(rho)  # Entanglement (two qubits)

# Fidelity and distance
F = fidelity(psi1, psi2)
D = tracedist(rho1, rho2)

# Correlation functions
corr = correlation_2op_1t(H, rho0, taulist, c_ops, A, B)
w, S = spectrum_correlation_fft(taulist, corr)

# Steady states
rho_ss = steadystate(H, c_ops)
```

* *请参见** `references/analysis.md` 了解熵，保真度、测量、相关函数和稳态计算。

### 4. 可视化

可视化量子态和动力学：

```python
# Bloch sphere
b = Bloch()
b.add_states(psi)
b.show()

# Wigner function (phase space)
xvec = np.linspace(-5, 5, 200)
W = wigner(psi, xvec, xvec)
plt.contourf(xvec, xvec, W, 100, cmap='RdBu')

# Fock distribution
plot_fock_distribution(psi)

# Matrix visualization
hinton(rho)  # Hinton diagram
matrix_histogram(H.full())  # 3D bars
```

* *参见** `references/visualization.md`，了解布洛赫球体动画、维格纳函数、Q 函数和矩阵

### 5. 高级方法

复杂场景的专业技术：

```python
# Floquet theory (periodic Hamiltonians)
T = 2 * np.pi / w_drive
f_modes, f_energies = floquet_modes(H, T, args)
result = fmmesolve(H, psi0, tlist, c_ops, T=T, args=args)

# HEOM (non-Markovian, strong coupling)
from qutip.nonmarkov.heom import HEOMSolver, BosonicBath
bath = BosonicBath(Q, ck_real, vk_real)
hsolver = HEOMSolver(H_sys, [bath], max_depth=5)
result = hsolver.run(rho0, tlist)

# Permutational invariance (identical particles)
psi = dicke(N, j, m)  # Dicke states
Jz = jspin(N, 'z')  # Collective operators
```

* *请参阅** `references/advanced.md`，了解 Floquet 理论、HEOM、排列不变性、随机求解器、超级算子和性能优化。

## 常见工作流程

### 模拟阻尼谐波振荡器

```python
# System parameters
N = 20  # Hilbert space dimension
omega = 1.0  # Oscillator frequency
kappa = 0.1  # Decay rate

# Hamiltonian and collapse operators
H = omega * num(N)
c_ops = [np.sqrt(kappa) * destroy(N)]

# Initial state
psi0 = coherent(N, 3.0)

# Time evolution
tlist = np.linspace(0, 50, 200)
result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])

# Visualize
plt.plot(tlist, result.expect[0])
plt.xlabel('Time')
plt.ylabel('⟨n⟩')
plt.title('Photon Number Decay')
plt.show()
```

### 二量子位纠缠动力学

```python
# Create Bell state
psi0 = bell_state('00')

# Local dephasing on each qubit
gamma = 0.1
c_ops = [
    np.sqrt(gamma) * tensor(sigmaz(), qeye(2)),
    np.sqrt(gamma) * tensor(qeye(2), sigmaz())
]

# Track entanglement
def compute_concurrence(t, psi):
    rho = ket2dm(psi) if psi.isket else psi
    return concurrence(rho)

tlist = np.linspace(0, 10, 100)
result = mesolve(qeye([2, 2]), psi0, tlist, c_ops)

# Compute concurrence for each state
C_t = [concurrence(state.proj()) for state in result.states]

plt.plot(tlist, C_t)
plt.xlabel('Time')
plt.ylabel('Concurrence')
plt.title('Entanglement Decay')
plt.show()
```

### Jaynes-Cummings 模型

```python
# System parameters
N = 10  # Cavity Fock space
wc = 1.0  # Cavity frequency
wa = 1.0  # Atom frequency
g = 0.05  # Coupling strength

# Operators
a = tensor(destroy(N), qeye(2))  # Cavity
sm = tensor(qeye(N), sigmam())  # Atom

# Hamiltonian (RWA)
H = wc * a.dag() * a + wa * sm.dag() * sm + g * (a.dag() * sm + a * sm.dag())

# Initial state: cavity in coherent state, atom in ground state
psi0 = tensor(coherent(N, 2), basis(2, 0))

# Dissipation
kappa = 0.1  # Cavity decay
gamma = 0.05  # Atomic decay
c_ops = [np.sqrt(kappa) * a, np.sqrt(gamma) * sm]

# Observables
n_cav = a.dag() * a
n_atom = sm.dag() * sm

# Evolve
tlist = np.linspace(0, 50, 200)
result = mesolve(H, psi0, tlist, c_ops, e_ops=[n_cav, n_atom])

# Plot
fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
axes[0].plot(tlist, result.expect[0])
axes[0].set_ylabel('⟨n_cavity⟩')
axes[1].plot(tlist, result.expect[1])
axes[1].set_ylabel('⟨n_atom⟩')
axes[1].set_xlabel('Time')
plt.tight_layout()
plt.show()
```

## 高效技巧模拟

1. **截断希尔伯特空间**：使用捕获动态的最小维度
2. **选择合适的求解器**：对于纯态，`sesolve` 比 `mesolve`
3 更快。 **与时间相关的术语**：字符串格式（例如，`'cos(w*t)'`）是最快的
4. **仅存储需要的数据**：使用`e_ops`而不是存储所有状态
5. **调整公差**：通过 `Options`
6 平衡精度与计算时间。 **并行轨迹**：`mcsolve`自动使用多个CPU
7. **检查收敛性**：改变 `ntraj`、希尔伯特空间大小和容差 

## 故障排除

 * *内存问题**：减少希尔伯特空间维度，使用 `store_final_state` 选项，或考虑 Krylov 方法

  * *慢速模拟**：使用基于字符串的时间依赖性，稍微增加容差，或尝试`method='bdf'` 用于刚性问题

* *数值不稳定性**：减少时间步长（`nsteps` 选项），增加容差，或检查哈密顿量/运算符是否正确定义

* *导入错误**：确保 QuTiP 安装正确；量子门需要`qutip-qip`封装

## 参考资料

本技能包含详细参考文档：

- **`references/core_concepts.md`**：量子对象、状态、运算符、张量积、复合系统
- **`references/time_evolution.md`**：所有求解器（sesolve、mesolve、mcsolve、brmesolve 等）、瞬态哈密顿量、求解器选项
- **`references/visualization.md`**：布洛赫球、维格纳函数、Q 函数、福克分布、矩阵图
- **`references/analysis.md`**：期望值、熵、保真度、纠缠度量、相关函数、稳态
- **`references/advanced.md`**：Floquet 理论、HEOM、排列不变性、随机方法、超级算子、性能Tips

## 外部资源

- 文档：https://qutip.readthedocs.io/
- 教程：https://qutip.org/qutip-tutorials/
- API参考：https://qutip.readthedocs.io/en/stable/apidoc/apidoc.html
- GitHub： https://github.com/qutip/qutip
