# QuTiP 可视化

## Bloch Sphere

可视化 Bloch 球体上的量子位状态。

### 基本用法

```python
from qutip import *
import matplotlib.pyplot as plt

# Create Bloch sphere
b = Bloch()

# Add states
psi = (basis(2, 0) + basis(2, 1)).unit()
b.add_states(psi)

# Add vectors
b.add_vectors([1, 0, 0])  # X-axis

# Display
b.show()
```

### 多个状态

```python
# Add multiple states
states = [(basis(2, 0) + basis(2, 1)).unit(),
          (basis(2, 0) + 1j*basis(2, 1)).unit()]
b.add_states(states)

# Add points
b.add_points([[0, 1, 0], [0, -1, 0]])

# Customize colors
b.point_color = ['r', 'g']
b.point_marker = ['o', 's']
b.point_size = [20, 20]

b.show()
```

### 动画

```python
# Animate state evolution
states = result.states  # From sesolve/mesolve

b = Bloch()
b.vector_color = ['r']
b.view = [-40, 30]  # Viewing angle

# Create animation
from matplotlib.animation import FuncAnimation

def animate(i):
    b.clear()
    b.add_states(states[i])
    b.make_sphere()
    return b.axes

anim = FuncAnimation(b.fig, animate, frames=len(states),
                      interval=50, blit=False, repeat=True)
plt.show()
```

### 自定义

```python
b = Bloch()

# Sphere appearance
b.sphere_color = '#FFDDDD'
b.sphere_alpha = 0.1
b.frame_alpha = 0.1

# Axes
b.xlabel = ['$|+\\\\rangle$', '$|-\\\\rangle$']
b.ylabel = ['$|+i\\\\rangle$', '$|-i\\\\rangle$']
b.zlabel = ['$|0\\\\rangle$', '$|1\\\\rangle$']

# Font sizes
b.font_size = 20
b.font_color = 'black'

# View angle
b.view = [-60, 30]

# Save figure
b.save('bloch.png')
```

## 维格纳函数

相空间拟概率分布。

### 基本计算

```python
# Create state
psi = coherent(N, alpha)

# Calculate Wigner function
xvec = np.linspace(-5, 5, 200)
W = wigner(psi, xvec, xvec)

# Plot
fig, ax = plt.subplots(1, 1, figsize=(6, 6))
cont = ax.contourf(xvec, xvec, W, 100, cmap='RdBu')
ax.set_xlabel('Re(α)')
ax.set_ylabel('Im(α)')
plt.colorbar(cont, ax=ax)
plt.show()
```

### 特殊色彩图

```python
# Wigner colormap emphasizes negative values
from qutip import wigner_cmap

W = wigner(psi, xvec, xvec)

fig, ax = plt.subplots()
cont = ax.contourf(xvec, xvec, W, 100, cmap=wigner_cmap(W))
ax.set_title('Wigner Function')
plt.colorbar(cont)
plt.show()
```

### 3D 曲面图

```python
from mpl_toolkits.mplot3d import Axes3D

X, Y = np.meshgrid(xvec, xvec)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, W, cmap='RdBu', alpha=0.8)
ax.set_xlabel('Re(α)')
ax.set_ylabel('Im(α)')
ax.set_zlabel('W(α)')
plt.show()
```

### 比较状态

```python
# Compare different states
states = [coherent(N, 2), fock(N, 2), thermal_dm(N, 2)]
titles = ['Coherent', 'Fock', 'Thermal']

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, (state, title) in enumerate(zip(states, titles)):
    W = wigner(state, xvec, xvec)
    cont = axes[i].contourf(xvec, xvec, W, 100, cmap='RdBu')
    axes[i].set_title(title)
    axes[i].set_xlabel('Re(α)')
    if i == 0:
        axes[i].set_ylabel('Im(α)')

plt.tight_layout()
plt.show()
```

## Q函数（Husimi）

平滑相空间分布（始终为正）。

### 基本用法

```python
from qutip import qfunc

Q = qfunc(psi, xvec, xvec)

fig, ax = plt.subplots()
cont = ax.contourf(xvec, xvec, Q, 100, cmap='viridis')
ax.set_xlabel('Re(α)')
ax.set_ylabel('Im(α)')
ax.set_title('Q-Function')
plt.colorbar(cont)
plt.show()
```

### 高效批量计算

```python
from qutip import QFunc

# For calculating Q-function at many points
qf = QFunc(rho)
Q = qf.eval(xvec, xvec)
```

## 福克状态概率分布

可视化光子数分布。

### 基本直方图

```python
from qutip import plot_fock_distribution

# Single state
psi = coherent(N, 2)
fig, ax = plot_fock_distribution(psi)
ax.set_title('Coherent State')
plt.show()
```

### 比较分布

```python
states = {
    'Coherent': coherent(20, 2),
    'Thermal': thermal_dm(20, 2),
    'Fock': fock(20, 2)
}

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, (title, state) in zip(axes, states.items()):
    plot_fock_distribution(state, fig=fig, ax=ax)
    ax.set_title(title)
    ax.set_ylim([0, 0.3])

plt.tight_layout()
plt.show()
```

### 时间演化

```python
# Show evolution of photon distribution
result = mesolve(H, psi0, tlist, c_ops)

# Plot at different times
times_to_plot = [0, 5, 10, 15]
fig, axes = plt.subplots(1, 4, figsize=(16, 4))

for ax, t_idx in zip(axes, times_to_plot):
    plot_fock_distribution(result.states[t_idx], fig=fig, ax=ax)
    ax.set_title(f't = {tlist[t_idx]:.1f}')
    ax.set_ylim([0, 1])

plt.tight_layout()
plt.show()
```

## 矩阵可视化

### Hinton图

使用加权可视化矩阵结构squares.

```python
from qutip import hinton

# Density matrix
rho = bell_state('00').proj()

hinton(rho)
plt.title('Bell State Density Matrix')
plt.show()
```

### 矩阵直方图

3D 矩阵元素条形图。

```python
from qutip import matrix_histogram

# Show real and imaginary parts
H = sigmaz()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

matrix_histogram(H.full(), xlabels=['0', '1'], ylabels=['0', '1'],
                 fig=fig, ax=axes[0])
axes[0].set_title('Real Part')

matrix_histogram(H.full(), bar_type='imag', xlabels=['0', '1'],
                 ylabels=['0', '1'], fig=fig, ax=axes[1])
axes[1].set_title('Imaginary Part')

plt.tight_layout()
plt.show()
```

### 复相图

```python
# Visualize complex matrix elements
rho = coherent_dm(10, 2)

# Plot complex elements
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Absolute value
matrix_histogram(rho.full(), bar_type='abs', fig=fig, ax=axes[0])
axes[0].set_title('Absolute Value')

# Phase
matrix_histogram(rho.full(), bar_type='phase', fig=fig, ax=axes[1])
axes[1].set_title('Phase')

plt.tight_layout()
plt.show()
```

## 能量水平图

```python
# Visualize energy eigenvalues
H = num(N) + 0.1 * (create(N) + destroy(N))**2

# Get eigenvalues and eigenvectors
evals, ekets = H.eigenstates()

# Plot energy levels
fig, ax = plt.subplots(figsize=(8, 6))

for i, E in enumerate(evals[:10]):
    ax.hlines(E, 0, 1, linewidth=2)
    ax.text(1.1, E, f'|{i}⟩', va='center')

ax.set_ylabel('Energy')
ax.set_xlim([-0.2, 1.5])
ax.set_xticks([])
ax.set_title('Energy Spectrum')
plt.show()
```

## 量子过程断层扫描

可视化量子通道/门动作。

```python
from qutip.qip.operations import cnot
from qutip_qip.tomography import qpt, qpt_plot_combined

# Define process (e.g., CNOT gate)
U = cnot()

# Perform QPT
chi = qpt(U, method='choicm')

# Visualize
fig = qpt_plot_combined(chi)
plt.show()
```

## 期望值超过时间

```python
# Standard plotting of expectation values
result = mesolve(H, psi0, tlist, c_ops, e_ops=[num(N)])

fig, ax = plt.subplots()
ax.plot(tlist, result.expect[0])
ax.set_xlabel('Time')
ax.set_ylabel('⟨n⟩')
ax.set_title('Photon Number Evolution')
ax.grid(True)
plt.show()
```

### 多个可观测值

```python
# Plot multiple expectation values
e_ops = [a.dag() * a, a + a.dag(), 1j * (a - a.dag())]
labels = ['⟨n⟩', '⟨X⟩', '⟨P⟩']

result = mesolve(H, psi0, tlist, c_ops, e_ops=e_ops)

fig, axes = plt.subplots(3, 1, figsize=(8, 9))

for i, (ax, label) in enumerate(zip(axes, labels)):
    ax.plot(tlist, result.expect[i])
    ax.set_ylabel(label)
    ax.grid(True)

axes[-1].set_xlabel('Time')
plt.tight_layout()
plt.show()
```

## 相关函数和频谱

```python
# Two-time correlation function
taulist = np.linspace(0, 10, 200)
corr = correlation_2op_1t(H, rho0, taulist, c_ops, a.dag(), a)

# Plot correlation
fig, ax = plt.subplots()
ax.plot(taulist, np.real(corr))
ax.set_xlabel('τ')
ax.set_ylabel('⟨a†(τ)a(0)⟩')
ax.set_title('Correlation Function')
plt.show()

# Power spectrum
from qutip import spectrum_correlation_fft

w, S = spectrum_correlation_fft(taulist, corr)

fig, ax = plt.subplots()
ax.plot(w, S)
ax.set_xlabel('Frequency')
ax.set_ylabel('S(ω)')
ax.set_title('Power Spectrum')
plt.show()
```

## 保存人物

```python
# High-resolution saves
fig.savefig('my_plot.png', dpi=300, bbox_inches='tight')
fig.savefig('my_plot.pdf', bbox_inches='tight')
fig.savefig('my_plot.svg', bbox_inches='tight')
```
