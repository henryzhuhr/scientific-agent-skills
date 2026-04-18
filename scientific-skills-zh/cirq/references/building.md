# 构建量子电路

本指南涵盖了 Cirq 中的电路构建，包括量子位、门、操作和电路模式。

## 基本电路构建

### 创建电路

```python
import cirq

# Create a circuit
circuit = cirq.Circuit()

# Create qubits
q0 = cirq.GridQubit(0, 0)
q1 = cirq.GridQubit(0, 1)
q2 = cirq.LineQubit(0)

# Add gates to circuit
circuit.append([
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.measure(q0, q1, key='result')
])
```

### 量子位类型

* *GridQubit**:用于类似硬件布局的 2D 网格拓扑
```python
qubits = cirq.GridQubit.square(2)  # 2x2 grid
qubit = cirq.GridQubit(row=0, col=1)
```

* *LineQubit**：1D 线性拓扑
```python
qubits = cirq.LineQubit.range(5)  # 5 qubits in a line
qubit = cirq.LineQubit(3)
```

* *NamedQubit**：自定义命名的量子位
```python
qubit = cirq.NamedQubit('my_qubit')
```

## 通用门和操作

### 单量子位门

```python
# Pauli gates
cirq.X(qubit)  # NOT gate
cirq.Y(qubit)
cirq.Z(qubit)

# Hadamard
cirq.H(qubit)

# Rotation gates
cirq.rx(angle)(qubit)  # Rotation around X-axis
cirq.ry(angle)(qubit)  # Rotation around Y-axis
cirq.rz(angle)(qubit)  # Rotation around Z-axis

# Phase gates
cirq.S(qubit)  # √Z gate
cirq.T(qubit)  # ⁴√Z gate
```

### 两量子位门

```python
# CNOT (Controlled-NOT)
cirq.CNOT(control, target)
cirq.CX(control, target)  # Alias

# CZ (Controlled-Z)
cirq.CZ(q0, q1)

# SWAP
cirq.SWAP(q0, q1)

# iSWAP
cirq.ISWAP(q0, q1)

# Controlled rotations
cirq.CZPowGate(exponent=0.5)(q0, q1)
```

### 测量操作

```python
# Measure single qubit
cirq.measure(qubit, key='m')

# Measure multiple qubits
cirq.measure(q0, q1, q2, key='result')

# Measure all qubits in circuit
circuit.append(cirq.measure(*qubits, key='final'))
```

## 高级电路构造

### 参数化门

```python
import sympy

# Create symbolic parameters
theta = sympy.Symbol('theta')
phi = sympy.Symbol('phi')

# Use in gates
circuit = cirq.Circuit(
    cirq.rx(theta)(q0),
    cirq.ry(phi)(q1),
    cirq.CNOT(q0, q1)
)

# Resolve parameters later
resolved = cirq.resolve_parameters(circuit, {'theta': 0.5, 'phi': 1.2})
```

### 通过Unitaries定制门

```python
import numpy as np

# Define unitary matrix
unitary = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
]) / np.sqrt(2)

# Create gate from unitary
gate = cirq.MatrixGate(unitary)
operation = gate(q0, q1)
```

### 门分解

```python
# Define custom gate with decomposition
class MyGate(cirq.Gate):
    def _num_qubits_(self):
        return 1

    def _decompose_(self, qubits):
        q = qubits[0]
        return [cirq.H(q), cirq.T(q), cirq.H(q)]

    def _circuit_diagram_info_(self, args):
        return 'MyGate'

# Use the custom gate
my_gate = MyGate()
circuit.append(my_gate(q0))
```

## 电路组织

### 时刻

电路被组织成时刻（并行操作）：

```python
# Explicit moment construction
circuit = cirq.Circuit(
    cirq.Moment([cirq.H(q0), cirq.H(q1)]),
    cirq.Moment([cirq.CNOT(q0, q1)]),
    cirq.Moment([cirq.measure(q0, key='m0'), cirq.measure(q1, key='m1')])
)

# Access moments
for i, moment in enumerate(circuit):
    print(f"Moment {i}: {moment}")
```

### 电路操作

```python
# Concatenate circuits
circuit3 = circuit1 + circuit2

# Insert operations
circuit.insert(index, operation)

# Append with strategy
circuit.append(operations, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
```

## 电路模式

### 响铃状态准备

```python
def bell_state_circuit():
    q0, q1 = cirq.LineQubit.range(2)
    return cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1)
    )
```

### GHZ状态

```python
def ghz_circuit(qubits):
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    for i in range(len(qubits) - 1):
        circuit.append(cirq.CNOT(qubits[i], qubits[i+1]))
    return circuit
```

### 量子傅里叶变换

```python
def qft_circuit(qubits):
    circuit = cirq.Circuit()
    for i, q in enumerate(qubits):
        circuit.append(cirq.H(q))
        for j in range(i + 1, len(qubits)):
            circuit.append(cirq.CZPowGate(exponent=1/2**(j-i))(qubits[j], q))

    # Reverse qubit order
    for i in range(len(qubits) // 2):
        circuit.append(cirq.SWAP(qubits[i], qubits[len(qubits) - i - 1]))

    return circuit
```

## 电路导入/导出

### OpenQASM

```python
# Export to QASM
qasm_str = circuit.to_qasm()

# Import from QASM
from cirq.contrib.qasm_import import circuit_from_qasm
circuit = circuit_from_qasm(qasm_str)
```

### 电路 JSON

```python
import json

# Serialize
json_str = cirq.to_json(circuit)

# Deserialize
circuit = cirq.read_json(json_text=json_str)
```

## 使用 Qudits

Qudits 是高维量子系统（qutrits、ququarts、等）：

```python
# Create qutrit (3-level system)
qutrit = cirq.LineQid(0, dimension=3)

# Custom qutrit gate
class QutritXGate(cirq.Gate):
    def _qid_shape_(self):
        return (3,)

    def _unitary_(self):
        return np.array([
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0]
        ])

gate = QutritXGate()
circuit = cirq.Circuit(gate(qutrit))
```

## 可观察量

从泡利运算符创建可观察量：

```python
# Single Pauli observable
obs = cirq.Z(q0)

# Pauli string
obs = cirq.X(q0) * cirq.Y(q1) * cirq.Z(q2)

# Linear combination
from cirq import PauliSum
obs = 0.5 * cirq.X(q0) + 0.3 * cirq.Z(q1)
```

## 最佳实践

1. **使用适当的量子位类型**：GridQubit 用于类似硬件的拓扑，LineQubit 用于一维问题
2. **保持电路模块化**：构建可重复使用的电路功能
3. **使用符号参数**：用于参数扫描和优化
4. **清晰地标记测量结果**：使用测量结果的描述性按键
5. **记录自定义门**：包括用于可视化的电路图信息
