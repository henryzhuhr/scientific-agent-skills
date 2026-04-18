# 电路转换

本指南涵盖了使用 Cirq 转换框架的电路优化、编译和操作。

## 转换器框架

### 基本转换器

```python
import cirq

# Example circuit
qubits = cirq.LineQubit.range(3)
circuit = cirq.Circuit(
    cirq.H(qubits[0]),
    cirq.CNOT(qubits[0], qubits[1]),
    cirq.CNOT(qubits[1], qubits[2])
)

# Apply built-in transformer
from cirq.transformers import optimize_for_target_gateset

# Optimize to specific gate set
optimized = optimize_for_target_gateset(
    circuit,
    gateset=cirq.SqrtIswapTargetGateset()
)
```

### 合并单量子位Gates

```python
from cirq.transformers import merge_single_qubit_gates_to_phxz

# Circuit with multiple single-qubit gates
circuit = cirq.Circuit(
    cirq.H(q),
    cirq.T(q),
    cirq.S(q),
    cirq.H(q)
)

# Merge into single operation
merged = merge_single_qubit_gates_to_phxz(circuit)
```

### 删除可忽略的操作

```python
from cirq.transformers import drop_negligible_operations

# Remove gates below threshold
circuit_with_small_rotations = cirq.Circuit(
    cirq.rz(1e-10)(q),  # Very small rotation
    cirq.H(q)
)

cleaned = drop_negligible_operations(circuit_with_small_rotations, atol=1e-8)
```

## 自定义变压器

### 变压器装饰器

```python
from cirq.transformers import transformer_api

@transformer_api.transformer
def remove_z_gates(circuit: cirq.Circuit) -> cirq.Circuit:
    """Remove all Z gates from circuit."""
    new_moments = []
    for moment in circuit:
        new_ops = [op for op in moment if not isinstance(op.gate, cirq.ZPowGate)]
        if new_ops:
            new_moments.append(cirq.Moment(new_ops))
    return cirq.Circuit(new_moments)

# Use custom transformer
transformed = remove_z_gates(circuit)
```

### 变压器类

```python
from cirq.transformers import transformer_primitives

class HToRyTransformer(transformer_primitives.Transformer):
    """Replace H gates with Ry(π/2)."""

    def __call__(self, circuit: cirq.Circuit, *, context=None) -> cirq.Circuit:
        def map_op(op: cirq.Operation, _) -> cirq.OP_TREE:
            if isinstance(op.gate, cirq.HPowGate):
                return cirq.ry(np.pi/2)(op.qubits[0])
            return op

        return transformer_primitives.map_operations(
            circuit,
            map_op,
            deep=True
        ).unfreeze(copy=False)

# Apply transformer
transformer = HToRyTransformer()
result = transformer(circuit)
```

## 门分解

### 分解到目标门集

```python
from cirq.transformers import optimize_for_target_gateset

# Decompose to CZ + single-qubit rotations
target_gateset = cirq.CZTargetGateset()
decomposed = optimize_for_target_gateset(circuit, gateset=target_gateset)

# Decompose to √iSWAP gates
sqrt_iswap_gateset = cirq.SqrtIswapTargetGateset()
decomposed = optimize_for_target_gateset(circuit, gateset=sqrt_iswap_gateset)
```

### 自定义门分解

```python
class Toffoli(cirq.Gate):
    def _num_qubits_(self):
        return 3

    def _decompose_(self, qubits):
        """Decompose Toffoli into basic gates."""
        c1, c2, t = qubits
        return [
            cirq.H(t),
            cirq.CNOT(c2, t),
            cirq.T(t)**-1,
            cirq.CNOT(c1, t),
            cirq.T(t),
            cirq.CNOT(c2, t),
            cirq.T(t)**-1,
            cirq.CNOT(c1, t),
            cirq.T(c2),
            cirq.T(t),
            cirq.H(t),
            cirq.CNOT(c1, c2),
            cirq.T(c1),
            cirq.T(c2)**-1,
            cirq.CNOT(c1, c2)
        ]

# Use decomposition
circuit = cirq.Circuit(Toffoli()(q0, q1, q2))
decomposed = cirq.decompose(circuit)
```

## 电路优化

### 弹出 Z 门

```python
from cirq.transformers import eject_z

# Move Z gates to end of circuit
circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.Z(q0),
    cirq.CNOT(q0, q1)
)

ejected = eject_z(circuit)
```

### 弹出阶段门

```python
from cirq.transformers import eject_phased_paulis

# Consolidate phase gates
optimized = eject_phased_paulis(circuit, atol=1e-8)
```

### 丢弃空时刻

```python
from cirq.transformers import drop_empty_moments

# Remove moments with no operations
cleaned = drop_empty_moments(circuit)
```

### 对齐测量

```python
from cirq.transformers import dephase_measurements

# Move measurements to end and remove operations after
aligned = dephase_measurements(circuit)
```

## 电路编译

#### 硬件编译

```python
import cirq_google

# Get device specification
device = cirq_google.Sycamore

# Compile circuit to device
from cirq.transformers import optimize_for_target_gateset

compiled = optimize_for_target_gateset(
    circuit,
    gateset=cirq_google.SycamoreTargetGateset()
)

# Validate compiled circuit
device.validate_circuit(compiled)
```

### 两量子位门编译

```python
# Compile to specific two-qubit gate
from cirq import two_qubit_to_cz

# Convert all two-qubit gates to CZ
cz_circuit = cirq.Circuit()
for moment in circuit:
    for op in moment:
        if len(op.qubits) == 2:
            cz_circuit.append(two_qubit_to_cz(op))
        else:
            cz_circuit.append(op)
```

## 量子位路由

### 将电路路由到器件拓扑

```python
from cirq.transformers import route_circuit

# Define device connectivity
device_graph = cirq.NamedTopology(
    {
        (0, 0): [(0, 1), (1, 0)],
        (0, 1): [(0, 0), (1, 1)],
        (1, 0): [(0, 0), (1, 1)],
        (1, 1): [(0, 1), (1, 0)]
    }
)

# Route logical qubits to physical qubits
routed_circuit = route_circuit(
    circuit,
    device_graph=device_graph,
    routing_algo=cirq.RouteCQC(device_graph)
)
```

### SWAP 网络插入

```python
# Manually insert SWAPs for routing
def insert_swaps(circuit, swap_locations):
    """Insert SWAP gates at specified locations."""
    new_circuit = cirq.Circuit()
    moment_idx = 0

    for i, moment in enumerate(circuit):
        if i in swap_locations:
            q0, q1 = swap_locations[i]
            new_circuit.append(cirq.SWAP(q0, q1))
        new_circuit.append(moment)

    return new_circuit
```

## 高级转换

### 统一编译

```python
import scipy.linalg

# Compile arbitrary unitary to gate sequence
def compile_unitary(unitary, qubits):
    """Compile 2x2 unitary using KAK decomposition."""
    from cirq.linalg import kak_decomposition

    decomp = kak_decomposition(unitary)
    operations = []

    # Add single-qubit gates before
    operations.append(cirq.MatrixGate(decomp.single_qubit_operations_before[0])(qubits[0]))
    operations.append(cirq.MatrixGate(decomp.single_qubit_operations_before[1])(qubits[1]))

    # Add interaction (two-qubit) part
    x, y, z = decomp.interaction_coefficients
    operations.append(cirq.XXPowGate(exponent=x/np.pi)(qubits[0], qubits[1]))
    operations.append(cirq.YYPowGate(exponent=y/np.pi)(qubits[0], qubits[1]))
    operations.append(cirq.ZZPowGate(exponent=z/np.pi)(qubits[0], qubits[1]))

    # Add single-qubit gates after
    operations.append(cirq.MatrixGate(decomp.single_qubit_operations_after[0])(qubits[0]))
    operations.append(cirq.MatrixGate(decomp.single_qubit_operations_after[1])(qubits[1]))

    return operations
```

### 电路简化

```python
from cirq.transformers import (
    merge_k_qubit_unitaries,
    merge_single_qubit_gates_to_phxz
)

# Merge adjacent single-qubit gates
simplified = merge_single_qubit_gates_to_phxz(circuit)

# Merge adjacent k-qubit unitaries
simplified = merge_k_qubit_unitaries(circuit, k=2)
```

### 基于换向的优化

```python
# Commute Z gates through CNOT
def commute_z_through_cnot(circuit):
    """Move Z gates through CNOT gates."""
    new_moments = []

    for moment in circuit:
        ops = list(moment)
        # Find Z gates before CNOT
        z_ops = [op for op in ops if isinstance(op.gate, cirq.ZPowGate)]
        cnot_ops = [op for op in ops if isinstance(op.gate, cirq.CXPowGate)]

        # Apply commutation rules
        # Z on control commutes, Z on target anticommutes
        # (simplified logic here)

        new_moments.append(cirq.Moment(ops))

    return cirq.Circuit(new_moments)
```

## 变换管线

### 组成多个变压器

```python
from cirq.transformers import transformer_api

# Build transformation pipeline
@transformer_api.transformer
def optimization_pipeline(circuit: cirq.Circuit) -> cirq.Circuit:
    # Step 1: Merge single-qubit gates
    circuit = merge_single_qubit_gates_to_phxz(circuit)

    # Step 2: Drop negligible operations
    circuit = drop_negligible_operations(circuit)

    # Step 3: Eject Z gates
    circuit = eject_z(circuit)

    # Step 4: Drop empty moments
    circuit = drop_empty_moments(circuit)

    return circuit

# Apply pipeline
optimized = optimization_pipeline(circuit)
```

## 验证与分析

### 电路深度减少

```python
# Measure circuit depth before and after
print(f"Original depth: {len(circuit)}")
optimized = optimization_pipeline(circuit)
print(f"Optimized depth: {len(optimized)}")
```

### 门数分析

```python
def count_gates(circuit):
    """Count gates by type."""
    counts = {}
    for moment in circuit:
        for op in moment:
            gate_type = type(op.gate).__name__
            counts[gate_type] = counts.get(gate_type, 0) + 1
    return counts

original_counts = count_gates(circuit)
optimized_counts = count_gates(optimized)
print(f"Original: {original_counts}")
print(f"Optimized: {optimized_counts}")
```

## 最佳实践

1. **从高级 transformers 开始**：在编写自定义 transformers2 之前使用内置 transformers。 **链transformers**：按顺序应用多个优化
3. **改造后验证**：确保电路正确性和器件兼容性
4. **措施改进**：轨道深度和门数减少
5. **使用适当的门集**：匹配目标硬件功能
6. **考虑交换性**：利用门换向进行优化
7. **首先在小型电路上进行测试**：在缩放
之前验证transformers是否正常工作
