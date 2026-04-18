# PennyLane

入门## PennyLane 是什么？

PennyLane 是一个用于量子计算、量子机器学习和量子化学的跨平台 Python 库。它可以通过自动微分和与经典机器学习框架无缝集成来训练神经网络等量子计算机。

## 安装

使用uv安装PennyLane：

```bash
uv pip install pennylane
```

适用于特定设备插件（IBM、Amazon Braket、Google、Rigetti、等）：

```bash
# IBM Qiskit
uv pip install pennylane-qiskit

# Amazon Braket
uv pip install amazon-braket-pennylane-plugin

# Google Cirq
uv pip install pennylane-cirq

# Rigetti
uv pip install pennylane-rigetti
```

## 核心概念

### 量子节点（QNode）

A QNode是一个可以在量子设备上评估的量子函数。它将量子电路定义与设备相结合：

```python
import pennylane as qml

# Define a device
dev = qml.device('default.qubit', wires=2)

# Create a QNode
@qml.qnode(dev)
def circuit(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.PauliZ(0))
```

### 设备

设备执行量子电路。 PennyLane 支持：
- **模拟器**：`default.qubit`、`default.mixed`、`lightning.qubit`
- **硬件**：通过插件访问（IBM、Amazon Braket、Rigetti、等）

```python
# Local simulator
dev = qml.device('default.qubit', wires=4)

# Lightning high-performance simulator
dev = qml.device('lightning.qubit', wires=10)
```

### 测量

PennyLane 支持多种测量类型：

```python
@qml.qnode(dev)
def measure_circuit():
    qml.Hadamard(wires=0)
    # Expectation value
    return qml.expval(qml.PauliZ(0))

@qml.qnode(dev)
def measure_probs():
    qml.Hadamard(wires=0)
    # Probability distribution
    return qml.probs(wires=[0, 1])

@qml.qnode(dev)
def measure_samples():
    qml.Hadamard(wires=0)
    # Sample measurements
    return qml.sample(qml.PauliZ(0))
```

## 基本工作流程

### 1. 构建一个电路

```python
import pennylane as qml
import numpy as np

dev = qml.device('default.qubit', wires=3)

@qml.qnode(dev)
def quantum_circuit(weights):
    # Apply gates
    qml.RX(weights[0], wires=0)
    qml.RY(weights[1], wires=1)
    qml.CNOT(wires=[0, 1])
    qml.RZ(weights[2], wires=2)

    # Measure
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1))
```

### 2. 计算梯度

```python
# Automatic differentiation
grad_fn = qml.grad(quantum_circuit)
weights = np.array([0.1, 0.2, 0.3])
gradients = grad_fn(weights)
```

### 3. 优化参数

```python
from pennylane import numpy as np

# Define optimizer
opt = qml.GradientDescentOptimizer(stepsize=0.1)

# Optimization loop
weights = np.array([0.1, 0.2, 0.3], requires_grad=True)
for i in range(100):
    weights = opt.step(quantum_circuit, weights)
    if i % 20 == 0:
        print(f"Step {i}: Cost = {quantum_circuit(weights)}")
```

## 器件独立编程

一次编写电路，随处运行：

```python
# Same circuit, different backends
@qml.qnode(qml.device('default.qubit', wires=2))
def circuit_simulator(x):
    qml.RX(x, wires=0)
    return qml.expval(qml.PauliZ(0))

# Switch to hardware (if available)
@qml.qnode(qml.device('qiskit.ibmq', wires=2))
def circuit_hardware(x):
    qml.RX(x, wires=0)
    return qml.expval(qml.PauliZ(0))
```

## 常见模式

### 参数化电路

```python
@qml.qnode(dev)
def parameterized_circuit(params, x):
    # Encode data
    qml.RX(x, wires=0)

    # Apply parameterized layers
    for param in params:
        qml.RY(param, wires=0)
        qml.CNOT(wires=[0, 1])

    return qml.expval(qml.PauliZ(0))
```

### 电路模板

使用内置模板进行常见模式：

```python
from pennylane.templates import StronglyEntanglingLayers

@qml.qnode(dev)
def template_circuit(weights):
    StronglyEntanglingLayers(weights, wires=range(3))
    return qml.expval(qml.PauliZ(0))

# Generate random weights for template
n_layers = 2
n_wires = 3
shape = StronglyEntanglingLayers.shape(n_layers, n_wires)
weights = np.random.random(shape)
```

## 调试和可视化

### 打印电路结构

```python
print(qml.draw(circuit)(params))
print(qml.draw_mpl(circuit)(params))  # Matplotlib visualization
```

### 检查操作

```python
with qml.tape.QuantumTape() as tape:
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])

print(tape.operations)
print(tape.measurements)
```

## 下一步步骤

有关特定主题的详细信息：
- **构建电路**：请参阅 `references/quantum_circuits.md`
- **Quantum ML**：请参阅 `references/quantum_ml.md`
- **化学应用**：请参阅 `references/quantum_chemistry.md`
- **设备管理**：请参阅`references/devices_backends.md`
- **优化**：参见 `references/optimization.md`
- **高级功能**：参见 `references/advanced_features.md`

## 资源

- 官方文档：https://docs.pennylane.ai
  - 代码书：https://pennylane.ai/codebook
  - QML 演示：https://pennylane.ai/qml/demonstrations
  - 社区论坛：https://discuss.pennylane.ai
