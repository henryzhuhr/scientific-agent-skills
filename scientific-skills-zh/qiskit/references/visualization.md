# Qiskit中的可视化

Qiskit为量子电路、测量结果和量子态提供全面的可视化工具。

## 安装

安装可视化依赖项：

```bash
uv pip install "qiskit[visualization]" matplotlib
```

## 电路可视化

### 基于文本图纸

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)

# Simple text output
print(qc.draw())

# Text with more detail
print(qc.draw('text', fold=-1))  # Don't fold long circuits
```

### Matplotlib 图纸

```python
# High-quality matplotlib figure
qc.draw('mpl')

# Save to file
fig = qc.draw('mpl')
fig.savefig('circuit.png', dpi=300, bbox_inches='tight')
```

### LaTeX 图纸

```python
# Generate LaTeX circuit diagram
qc.draw('latex')

# Save LaTeX source
latex_source = qc.draw('latex_source')
with open('circuit.tex', 'w') as f:
    f.write(latex_source)
```

## 自定义电路图纸

### 样式选项

```python
from qiskit.visualization import circuit_drawer

# Reverse qubit order
qc.draw('mpl', reverse_bits=True)

# Fold long circuits
qc.draw('mpl', fold=20)  # Fold at 20 columns

# Show idle wires
qc.draw('mpl', idle_wires=False)

# Add initial state
qc.draw('mpl', initial_state=True)
```

### 颜色自定义

```python
style = {
    'displaycolor': {
        'h': ('#FA74A6', '#000000'),     # Hadamard: pink
        'cx': ('#A8D0DB', '#000000'),    # CNOT: light blue
        'measure': ('#F7E7B4', '#000000') # Measure: yellow
    }
}

qc.draw('mpl', style=style)
```

## 结果可视化

### 计数直方图

```python
from qiskit.visualization import plot_histogram
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()

# Plot histogram
plot_histogram(counts)

# Compare multiple experiments
counts1 = {'00': 500, '11': 524}
counts2 = {'00': 480, '11': 544}
plot_histogram([counts1, counts2], legend=['Run 1', 'Run 2'])

# Save figure
fig = plot_histogram(counts)
fig.savefig('histogram.png', dpi=300, bbox_inches='tight')
```

### 直方图选项

```python
# Customize colors
plot_histogram(counts, color=['#1f77b4', '#ff7f0e'])

# Sort by value
plot_histogram(counts, sort='value')

# Set bar labels
plot_histogram(counts, bar_labels=True)

# Set target distribution (for comparison)
target = {'00': 0.5, '11': 0.5}
plot_histogram(counts, target=target)
```

## 状态可视化

### Bloch Sphere

可视化 Bloch 球体上的单量子位状态：

```python
from qiskit.visualization import plot_bloch_vector
from qiskit.quantum_info import Statevector
import numpy as np

# Visualize a specific state vector
# State |+⟩: equal superposition of |0⟩ and |1⟩
state = Statevector.from_label('+')
plot_bloch_vector(state.to_bloch())

# Custom vector
plot_bloch_vector([0, 1, 0])  # |+⟩ state on X-axis
```

### 多量子位 Bloch Sphere

```python
from qiskit.visualization import plot_bloch_multivector

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

state = Statevector.from_instruction(qc)
plot_bloch_multivector(state)
```

### 州城市图

将状态振幅可视化为 3D 城市：

```python
from qiskit.visualization import plot_state_city
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(3)
qc.h(range(3))
state = Statevector.from_instruction(qc)

plot_state_city(state)

# Customize
plot_state_city(state, color=['#FF6B6B', '#4ECDC4'])
```

### QSphere

将量子态可视化球体：

```python
from qiskit.visualization import plot_state_qsphere

state = Statevector.from_instruction(qc)
plot_state_qsphere(state)
```

### Hinton 图

显示状态幅度：

```python
from qiskit.visualization import plot_state_hinton

state = Statevector.from_instruction(qc)
plot_state_hinton(state)
```

## 密度矩阵可视化

```python
from qiskit.visualization import plot_state_density
from qiskit.quantum_info import DensityMatrix

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

state = DensityMatrix.from_instruction(qc)
plot_state_density(state)
```

## 门图可视化

可视化后端耦合图：

```python
from qiskit.visualization import plot_gate_map
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

# Show qubit connectivity
plot_gate_map(backend)

# Show with error rates
plot_gate_map(backend, plot_error_rates=True)
```

## 错误图可视化

显示后端错误率：

```python
from qiskit.visualization import plot_error_map

plot_error_map(backend)
```

## 电路属性显示

```python
from qiskit.visualization import plot_circuit_layout

# Show how circuit maps to physical qubits
transpiled_qc = transpile(qc, backend=backend)
plot_circuit_layout(transpiled_qc, backend)
```

## 脉冲可视化

用于脉冲电平控制：

```python
from qiskit import pulse
from qiskit.visualization import pulse_drawer

# Create pulse schedule
with pulse.build(backend) as schedule:
    pulse.play(pulse.Gaussian(duration=160, amp=0.1, sigma=40), pulse.drive_channel(0))

# Visualize
schedule.draw()
```

## 交互式小部件（Jupyter）

### 电路作曲家Widget

```python
from qiskit.tools.jupyter import QuantumCircuitComposer

composer = QuantumCircuitComposer()
composer.show()
```

### 交互式状态可视化

```python
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Enable interactive mode
plt.ion()
plot_histogram(counts)
plt.show()
```

## 比较图

### 多个直方图

```python
# Compare results from different backends
counts_sim = {'00': 500, '11': 524}
counts_hw = {'00': 480, '01': 20, '10': 24, '11': 500}

plot_histogram(
    [counts_sim, counts_hw],
    legend=['Simulator', 'Hardware'],
    figsize=(12, 6)
)
```

### 之前/之后翻译

```python
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))

# Original circuit
qc.draw('mpl', ax=ax1)
ax1.set_title('Original Circuit')

# Transpiled circuit
qc_transpiled = transpile(qc, backend=backend, optimization_level=3)
qc_transpiled.draw('mpl', ax=ax2)
ax2.set_title('Transpiled Circuit')

plt.tight_layout()
plt.show()
```

## 保存可视化

### 保存为各种格式

```python
# PNG
fig = qc.draw('mpl')
fig.savefig('circuit.png', dpi=300, bbox_inches='tight')

# PDF
fig.savefig('circuit.pdf', bbox_inches='tight')

# SVG (vector graphics)
fig.savefig('circuit.svg', bbox_inches='tight')

# Histogram
hist_fig = plot_histogram(counts)
hist_fig.savefig('results.png', dpi=300, bbox_inches='tight')
```

## 样式最佳实践

### 出版质量图

```python
import matplotlib.pyplot as plt

# Set matplotlib style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'sans-serif'

# Create high-quality visualization
fig = qc.draw('mpl', style='iqp')
fig.savefig('publication_circuit.png', dpi=600, bbox_inches='tight')
```

### 可用样式

```python
# Default style
qc.draw('mpl')

# IQP style (IBM Quantum)
qc.draw('mpl', style='iqp')

# Colorblind-friendly
qc.draw('mpl', style='bw')  # Black and white
```

## 可视化故障排除

### 常见问题

* *问题**：“没有名为“matplotlib”的模块”
```bash
uv pip install matplotlib
```

* *问题**：电路太大而无法显示
```python
# Use folding
qc.draw('mpl', fold=50)

# Or export to file instead of displaying
fig = qc.draw('mpl')
fig.savefig('large_circuit.png', dpi=150, bbox_inches='tight')
```

* *问题**：Jupyter笔记本不显示绘图
```python
# Add magic command at notebook start
%matplotlib inline
```

* *问题**：LaTeX 可视化不起作用
```bash
# Install LaTeX support
uv pip install pylatexenc
```
