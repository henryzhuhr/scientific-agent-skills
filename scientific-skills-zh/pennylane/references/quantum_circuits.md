# PennyLane

## 中的量子电路目录
1. [基本门和操作](#basic-gates-and-operations)
2. [多量子位门](#multi-qubit-gates)
3. [受控操作](#受控操作)
4. [测量值](#测量值)
5. [电路构造模式](#电路构造模式)
6. [动态电路](#dynamic- Circuits)
7. [电路检查](#电路检查)

## 基本门和操作

### 单量子位门

```python
import pennylane as qml

# Pauli gates
qml.PauliX(wires=0)  # X gate (bit flip)
qml.PauliY(wires=0)  # Y gate
qml.PauliZ(wires=0)  # Z gate (phase flip)

# Hadamard gate (superposition)
qml.Hadamard(wires=0)

# Phase gates
qml.S(wires=0)       # S gate (π/2 phase)
qml.T(wires=0)       # T gate (π/4 phase)
qml.PhaseShift(phi, wires=0)  # Arbitrary phase

# Rotation gates (parameterized)
qml.RX(theta, wires=0)  # Rotation around X-axis
qml.RY(theta, wires=0)  # Rotation around Y-axis
qml.RZ(theta, wires=0)  # Rotation around Z-axis

# General single-qubit rotation
qml.Rot(phi, theta, omega, wires=0)

# Universal gate (any single-qubit unitary)
qml.U3(theta, phi, delta, wires=0)
```

### 基础状态准备

```python
# Computational basis state
qml.BasisState([1, 0, 1], wires=[0, 1, 2])  # |101⟩

# Amplitude encoding
amplitudes = [0.5, 0.5, 0.5, 0.5]  # Must be normalized
qml.MottonenStatePreparation(amplitudes, wires=[0, 1])
```

## 多量子位门

### 二量子位门

```python
# CNOT (Controlled-NOT)
qml.CNOT(wires=[0, 1])  # control=0, target=1

# CZ (Controlled-Z)
qml.CZ(wires=[0, 1])

# SWAP gate
qml.SWAP(wires=[0, 1])

# Controlled rotations
qml.CRX(theta, wires=[0, 1])
qml.CRY(theta, wires=[0, 1])
qml.CRZ(theta, wires=[0, 1])

# Ising coupling gates
qml.IsingXX(phi, wires=[0, 1])
qml.IsingYY(phi, wires=[0, 1])
qml.IsingZZ(phi, wires=[0, 1])
```

### 多量子位门

```python
# Toffoli gate (CCNOT)
qml.Toffoli(wires=[0, 1, 2])  # control=0,1, target=2

# Multi-controlled X
qml.MultiControlledX(control_wires=[0, 1, 2], wires=3)

# Multi-qubit Pauli rotations
qml.MultiRZ(theta, wires=[0, 1, 2])
```

## 受控操作

### 通用控制操作

```python
# Apply controlled version of any operation
qml.ctrl(qml.RX(0.5, wires=1), control=0)

# Multiple control qubits
qml.ctrl(qml.RY(0.3, wires=2), control=[0, 1])

# Negative controls (activate when control is |0⟩)
qml.ctrl(qml.Hadamard(wires=2), control=0, control_values=[0])
```

### 条件操作

```python
@qml.qnode(dev)
def conditional_circuit():
    qml.Hadamard(wires=0)

    # Mid-circuit measurement
    m = qml.measure(0)

    # Apply gate conditionally
    qml.cond(m, qml.PauliX)(wires=1)

    return qml.expval(qml.PauliZ(1))
```

## 测量

### 期望值

```python
@qml.qnode(dev)
def measure_expectation():
    qml.Hadamard(wires=0)

    # Single observable
    return qml.expval(qml.PauliZ(0))

@qml.qnode(dev)
def measure_tensor():
    qml.Hadamard(wires=0)
    qml.Hadamard(wires=1)

    # Tensor product of observables
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1))
```

### 概率分布

```python
@qml.qnode(dev)
def measure_probabilities():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])

    # Probabilities of all basis states
    return qml.probs(wires=[0, 1])  # Returns [p(|00⟩), p(|01⟩), p(|10⟩), p(|11⟩)]
```

### 样本和计数

```python
@qml.qnode(dev)
def measure_samples(shots=1000):
    qml.Hadamard(wires=0)

    # Raw samples
    return qml.sample(qml.PauliZ(0))

@qml.qnode(dev)
def measure_counts(shots=1000):
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])

    # Count occurrences
    return qml.counts(wires=[0, 1])
```

### 方差

```python
@qml.qnode(dev)
def measure_variance():
    qml.RX(0.5, wires=0)

    # Variance of observable
    return qml.var(qml.PauliZ(0))
```

### 中电路测量

```python
@qml.qnode(dev)
def mid_circuit_measure():
    qml.Hadamard(wires=0)

    # Measure qubit 0 during circuit
    m0 = qml.measure(0)

    # Use measurement result
    qml.cond(m0, qml.PauliX)(wires=1)

    # Final measurement
    return qml.expval(qml.PauliZ(1))
```

## 电路构造模式

### 基于层的构造

```python
def layer(weights, wires):
    """Single layer of parameterized gates."""
    for i, wire in enumerate(wires):
        qml.RY(weights[i], wires=wire)

    for wire in wires[:-1]:
        qml.CNOT(wires=[wire, wire+1])

@qml.qnode(dev)
def layered_circuit(weights):
    n_layers = len(weights)
    wires = range(4)

    for i in range(n_layers):
        layer(weights[i], wires)

    return qml.expval(qml.PauliZ(0))
```

### 数据编码

```python
def angle_encoding(x, wires):
    """Encode classical data as rotation angles."""
    for i, wire in enumerate(wires):
        qml.RX(x[i], wires=wire)

def amplitude_encoding(x, wires):
    """Encode data as quantum state amplitudes."""
    qml.MottonenStatePreparation(x, wires=wires)

def basis_encoding(x, wires):
    """Encode binary data in computational basis."""
    for i, val in enumerate(x):
        if val:
            qml.PauliX(wires=i)
```

### Ansatz模式

```python
# Hardware-efficient ansatz
def hardware_efficient_ansatz(weights, wires):
    n_layers = len(weights) // len(wires)

    for layer in range(n_layers):
        # Rotation layer
        for i, wire in enumerate(wires):
            qml.RY(weights[layer * len(wires) + i], wires=wire)

        # Entanglement layer
        for wire in wires[:-1]:
            qml.CNOT(wires=[wire, wire+1])

# Alternating layered ansatz
def alternating_ansatz(weights, wires):
    for w in weights:
        for wire in wires:
            qml.RX(w[wire], wires=wire)
        for wire in wires[:-1]:
            qml.CNOT(wires=[wire, wire+1])
```

## 动态电路

### For 循环

```python
@qml.qnode(dev)
def dynamic_for_loop(n_iterations):
    qml.Hadamard(wires=0)

    # Dynamic for loop
    for i in range(n_iterations):
        qml.RX(0.1 * i, wires=0)

    return qml.expval(qml.PauliZ(0))
```

### While 循环（带催化剂）

```python
@qml.qjit  # Just-in-time compilation
@qml.qnode(dev)
def dynamic_while_loop():
    qml.Hadamard(wires=0)

    # Dynamic while loop
    @qml.while_loop(lambda i: i < 5)
    def loop(i):
        qml.RX(0.1, wires=0)
        return i + 1

    loop(0)
    return qml.expval(qml.PauliZ(0))
```

### 自适应电路

```python
@qml.qnode(dev)
def adaptive_circuit():
    qml.Hadamard(wires=0)

    # Measure and adapt
    m = qml.measure(0)

    # Different paths based on measurement
    if m:
        qml.RX(0.5, wires=1)
    else:
        qml.RY(0.5, wires=1)

    return qml.expval(qml.PauliZ(1))
```

## 电路检查

### 绘制电路

```python
# Text representation
print(qml.draw(circuit)(params))

# ASCII art
print(qml.draw(circuit, wire_order=[0,1,2])(params))

# Matplotlib visualization
fig, ax = qml.draw_mpl(circuit)(params)
```

### 分析电路结构

```python
# Get circuit specs
specs = qml.specs(circuit)(params)
print(f"Gates: {specs['gate_sizes']}")
print(f"Depth: {specs['depth']}")
print(f"Parameters: {specs['num_trainable_params']}")

# Resource estimation
resources = qml.resource.resource_estimation(circuit)(params)
print(f"Total gates: {resources['num_gates']}")
```

### 胶带检查

```python
# Record operations
with qml.tape.QuantumTape() as tape:
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    qml.expval(qml.PauliZ(0))

# Inspect tape contents
print("Operations:", tape.operations)
print("Measurements:", tape.measurements)
print("Wires used:", tape.wires)
```

### 电路改造

```python
# Expand composite operations
expanded = qml.transforms.expand_tape(tape)

# Cancel adjacent operations
optimized = qml.transforms.cancel_inverses(tape)

# Commute measurements to end
commuted = qml.transforms.commute_controlled(tape)
```

## 最佳实践

1. **使用本机门** - 首选目标器件
2支持的门。 **最小化电路深度** - 减少退相干效应
3. **高效编码** - 选择编码匹配数据结构
4. **重用电路** - 尽可能缓存编译电路
5. **验证测量** - 确保可观测量为 Hermitian
6. **检查量子位计数** - 验证设备有足够的电线
7. **轮廓电路** - 使用 `qml.specs()` 分析复杂度

## 常见模式

### 贝尔状态准备

```python
@qml.qnode(dev)
def bell_state():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.state()  # Returns |Φ+⟩ = (|00⟩ + |11⟩)/√2
```

### GHZ 状态

```python
@qml.qnode(dev)
def ghz_state(n_qubits):
    qml.Hadamard(wires=0)
    for i in range(n_qubits-1):
        qml.CNOT(wires=[0, i+1])
    return qml.state()
```

### 量子傅立叶变换

```python
def qft(wires):
    """Quantum Fourier Transform."""
    n_wires = len(wires)
    for i in range(n_wires):
        qml.Hadamard(wires=wires[i])
        for j in range(i+1, n_wires):
            qml.CRZ(np.pi / (2**(j-i)), wires=[wires[j], wires[i]])
```

### 逆QFT

```python
def inverse_qft(wires):
    """Inverse Quantum Fourier Transform."""
    n_wires = len(wires)
    for i in range(n_wires-1, -1, -1):
        for j in range(n_wires-1, i, -1):
            qml.CRZ(-np.pi / (2**(j-i)), wires=[wires[j], wires[i]])
        qml.Hadamard(wires=wires[i])
```
