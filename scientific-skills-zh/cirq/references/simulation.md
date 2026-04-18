# Cirq

中的仿真本指南涵盖量子电路仿真，包括精确和噪声仿真、参数扫描和量子虚拟机 (QVM)。

## 精确仿真

### 基本仿真

```python
import cirq
import numpy as np

# Create circuit
q0, q1 = cirq.LineQubit.range(2)
circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.measure(q0, q1, key='result')
)

# Simulate
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=1000)

# Get measurement results
print(result.histogram(key='result'))
```

### 状态向量仿真

```python
# Simulate without measurement to get final state
simulator = cirq.Simulator()
result = simulator.simulate(circuit_without_measurement)

# Access state vector
state_vector = result.final_state_vector
print(f"State vector: {state_vector}")

# Get amplitudes
print(f"Amplitude of |00⟩: {state_vector[0]}")
print(f"Amplitude of |11⟩: {state_vector[3]}")
```

### 密度矩阵仿真

```python
# Use density matrix simulator for mixed states
simulator = cirq.DensityMatrixSimulator()
result = simulator.simulate(circuit)

# Access density matrix
density_matrix = result.final_density_matrix
print(f"Density matrix shape: {density_matrix.shape}")
```

### 分步仿真

```python
# Simulate moment-by-moment
simulator = cirq.Simulator()
for step in simulator.simulate_moment_steps(circuit):
    print(f"State after moment {step.moment}: {step.state_vector()}")
```

## 采样和测量

### 运行多个镜头

```python
# Run circuit multiple times
result = simulator.run(circuit, repetitions=10000)

# Access measurement counts
counts = result.histogram(key='result')
print(f"Measurement counts: {counts}")

# Get raw measurements
measurements = result.measurements['result']
print(f"Shape: {measurements.shape}")  # (repetitions, num_qubits)
```

### 期望值

```python
# Measure observable expectation value
from cirq import PauliString

observable = PauliString({q0: cirq.Z, q1: cirq.Z})
result = simulator.simulate_expectation_values(
    circuit,
    observables=[observable]
)
print(f"⟨ZZ⟩ = {result[0]}")
```

## 参数扫描

### 扫描参数

```python
import sympy

# Create parameterized circuit
theta = sympy.Symbol('theta')
q = cirq.LineQubit(0)
circuit = cirq.Circuit(
    cirq.ry(theta)(q),
    cirq.measure(q, key='m')
)

# Define parameter sweep
sweep = cirq.Linspace(key='theta', start=0, stop=2*np.pi, length=50)

# Run sweep
simulator = cirq.Simulator()
results = simulator.run_sweep(circuit, params=sweep, repetitions=1000)

# Process results
for params, result in zip(sweep, results):
    theta_val = params['theta']
    counts = result.histogram(key='m')
    print(f"θ={theta_val:.2f}: {counts}")
```

### 多个参数

```python
# Sweep over multiple parameters
theta = sympy.Symbol('theta')
phi = sympy.Symbol('phi')

circuit = cirq.Circuit(
    cirq.ry(theta)(q0),
    cirq.rz(phi)(q1)
)

# Product sweep (all combinations)
sweep = cirq.Product(
    cirq.Linspace('theta', 0, np.pi, 10),
    cirq.Linspace('phi', 0, 2*np.pi, 10)
)

results = simulator.run_sweep(circuit, params=sweep, repetitions=100)
```

### Zip Sweep（成对参数）

```python
# Sweep parameters together
sweep = cirq.Zip(
    cirq.Linspace('theta', 0, np.pi, 20),
    cirq.Linspace('phi', 0, 2*np.pi, 20)
)

results = simulator.run_sweep(circuit, params=sweep, repetitions=100)
```

## 噪声模拟

### 添加噪声通道

```python
# Create noisy circuit
noisy_circuit = circuit.with_noise(cirq.depolarize(p=0.01))

# Simulate noisy circuit
simulator = cirq.DensityMatrixSimulator()
result = simulator.run(noisy_circuit, repetitions=1000)
```

### 自定义噪声模型

```python
# Apply different noise to different gates
noise_model = cirq.NoiseModel.from_noise_model_like(
    cirq.ConstantQubitNoiseModel(cirq.depolarize(0.01))
)

# Simulate with noise model
result = cirq.DensityMatrixSimulator(noise=noise_model).run(
    circuit, repetitions=1000
)
```

有关全面的噪声建模详细信息，请参阅 `noise.md`。

## 状态直方图

### 可视化结果

```python
import matplotlib.pyplot as plt

# Get histogram
result = simulator.run(circuit, repetitions=1000)
counts = result.histogram(key='result')

# Plot
plt.bar(counts.keys(), counts.values())
plt.xlabel('State')
plt.ylabel('Counts')
plt.title('Measurement Results')
plt.show()
```

### 状态概率分布

```python
# Get state vector
result = simulator.simulate(circuit_without_measurement)
state_vector = result.final_state_vector

# Compute probabilities
probabilities = np.abs(state_vector) ** 2

# Plot
plt.bar(range(len(probabilities)), probabilities)
plt.xlabel('Basis State Index')
plt.ylabel('Probability')
plt.show()
```

## 量子虚拟机（QVM）

QVM 使用特定于设备的约束和噪声来模拟现实的量子硬件。

### 使用虚拟设备

```python
# Use a virtual Google device
import cirq_google

# Get virtual device
device = cirq_google.Sycamore

# Create circuit on device
qubits = device.metadata.qubit_set
circuit = cirq.Circuit(device=device)

# Add operations respecting device constraints
circuit.append(cirq.CZ(qubits[0], qubits[1]))

# Validate circuit against device
device.validate_circuit(circuit)
```

### 噪声虚拟硬件

```python
# Simulate with device noise
processor = cirq_google.get_engine().get_processor('weber')
noise_props = processor.get_device_specification()

# Create realistic noisy simulator
noisy_sim = cirq.DensityMatrixSimulator(
    noise=cirq_google.NoiseModelFromGoogleNoiseProperties(noise_props)
)

result = noisy_sim.run(circuit, repetitions=1000)
```

## 高级仿真技术

### 自定义初始状态

```python
# Start from custom state
initial_state = np.array([1, 0, 0, 1]) / np.sqrt(2)  # |00⟩ + |11⟩

simulator = cirq.Simulator()
result = simulator.simulate(circuit, initial_state=initial_state)
```

### 部分跟踪

```python
# Trace out subsystems
result = simulator.simulate(circuit)
full_state = result.final_state_vector

# Compute reduced density matrix for first qubit
from cirq import partial_trace
reduced_dm = partial_trace(result.final_density_matrix, keep_indices=[0])
```

### 中间状态访问

```python
# Get state at specific moment
simulator = cirq.Simulator()
for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
    if i == 5:  # After 5th moment
        state = step.state_vector()
        print(f"State after moment 5: {state}")
        break
```

## 仿真性能

### 优化大型仿真

1. **将状态向量用于纯状态**：比密度矩阵
2更快。 **尽可能避免密度矩阵**：
3 的价格呈指数级增长。 **批量参数扫描**：比单独运行
4更高效。 **使用适当的重复**：平衡精度与计算时间

```python
# Efficient: Single sweep
results = simulator.run_sweep(circuit, params=sweep, repetitions=100)

# Inefficient: Multiple individual runs
results = [simulator.run(circuit, param_resolver=p, repetitions=100)
           for p in sweep]
```

### 内存注意事项

```python
# For large systems, monitor state vector size
n_qubits = 20
state_size = 2**n_qubits * 16  # bytes (complex128)
print(f"State vector size: {state_size / 1e9:.2f} GB")
```

## 稳定器模拟

对于仅具有Clifford门的电路，使用高效稳定器模拟：

```python
# Clifford circuit (H, S, CNOT)
circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.S(q1),
    cirq.CNOT(q0, q1)
)

# Use stabilizer simulator (exponentially faster)
simulator = cirq.CliffordSimulator()
result = simulator.run(circuit, repetitions=1000)
```

## 最佳实践

1. **选择合适的模拟器**：对于纯态使用 Simulator，对于混合态使用 DensityMatrixSimulator
2. **使用参数扫描**：比运行单个电路
3更高效。 **验证电路**：在长时间仿真之前检查电路有效性
4. **监控资源使用情况**：跟踪大规模模拟的内存
5. **使用稳定器模拟**：当电路仅包含 Clifford 门 
6 时。 **保存中间结果**：用于长参数扫描或优化运行
