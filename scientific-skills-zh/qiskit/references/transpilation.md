# 电路转译和优化

转译是重写量子电路以匹配特定量子设备的拓扑和门集的过程，同时优化在嘈杂的量子计算机上的执行。

## 为什么转译？

* *问题**：抽象量子电路可能使用硬件上不可用的门并假设所有量子位连接。

* *解决方案**：转译将电路变换为：
1. 仅使用硬件本机门（基础门）
2. 尊重物理量子位连接
3. 最小化电路深度和门数
4. 优化以减少噪声设备上的错误

## 基本转换

### 简单转换

```python
from qiskit import QuantumCircuit, transpile

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)

# Transpile for a specific backend
transpiled_qc = transpile(qc, backend=backend)
```

### 优化级别

选择优化级别0-3:

```python
# Level 0: No optimization (fastest)
qc_0 = transpile(qc, backend=backend, optimization_level=0)

# Level 1: Light optimization
qc_1 = transpile(qc, backend=backend, optimization_level=1)

# Level 2: Moderate optimization (default)
qc_2 = transpile(qc, backend=backend, optimization_level=2)

# Level 3: Heavy optimization (slowest, best results)
qc_3 = transpile(qc, backend=backend, optimization_level=3)
```

* *Qiskit SDK v2.2** 与竞争对手相比，提供**83x 更快的转译速度**。

## 转译阶段

转译器管道由六个阶段组成：

### 1. 初始化阶段
- 验证电路指令
- 将多量子位门转换为标准形式

### 2.布局阶段
- 将虚拟量子位映射到物理量子位
- 考虑量子位连接性和错误rates

```python
from qiskit.transpiler import CouplingMap

# Define custom coupling
coupling = CouplingMap([(0, 1), (1, 2), (2, 3)])
qc_transpiled = transpile(qc, coupling_map=coupling)
```

### 3. 路由阶段
- 插入SWAP 门以满足连接性约束
- 最大限度地减少额外的SWAP 开销

### 4. 转换阶段
- 将门转换为硬件基础门
- 典型基础：{RZ、SX、X、CX}

```python
# Specify basis gates
basis_gates = ['cx', 'id', 'rz', 'sx', 'x']
qc_transpiled = transpile(qc, basis_gates=basis_gates)
```

### 5. 优化阶段
- 减少门数和电路深度
- 应用门取消和换向规则
- 使用**虚拟排列省略**（级别2-3)
- 查找可分离操作进行分解

### 6. 调度阶段
- 添加脉冲电平控制的时序信息

## 高级优化功能

### 虚拟排列消除

在优化级别 2-3，Qiskit 分析交换结构，通过跟踪虚拟量子位排列来消除不必要的交换门。

### 门取消

识别并删除取消的门对：
- X-X → I
- H-H → I
- CNOT-CNOT → I

### 数值分解

分割两个量子位门，可以表示为可分离的一个量子位操作。

## 通用转换参数

### 初始布局

指定要使用哪些物理量子位使用：

```python
# Use specific physical qubits
initial_layout = [0, 2, 4]  # Maps circuit qubits 0,1,2 to physical qubits 0,2,4
qc_transpiled = transpile(qc, backend=backend, initial_layout=initial_layout)
```

### 近似度

较少门的交易精度（0.0 = 最大近似，1.0 = 无近似）：

```python
# Allow 5% approximation error for fewer gates
qc_transpiled = transpile(qc, backend=backend, approximation_degree=0.95)
```

### 的种子重现性

```python
qc_transpiled = transpile(qc, backend=backend, seed_transpiler=42)
```

### 调度方法

```python
# Add timing constraints
qc_transpiled = transpile(
    qc,
    backend=backend,
    scheduling_method='alap'  # As Late As Possible
)
```

## 模拟器的转译

即使对于模拟器，转译也可以优化电路：

```python
from qiskit_aer import AerSimulator

simulator = AerSimulator()
qc_optimized = transpile(qc, backend=simulator, optimization_level=3)

# Compare gate counts
print(f"Original: {qc.size()} gates")
print(f"Optimized: {qc_optimized.size()} gates")
```

## 目标感知转换

使用`Target`对象获取详细的后端规范：

```python
from qiskit.transpiler import Target

# Transpile with target specification
qc_transpiled = transpile(qc, target=backend.target)
```

## 电路分析后Transpilation

```python
qc_transpiled = transpile(qc, backend=backend, optimization_level=3)

# Analyze results
print(f"Depth: {qc_transpiled.depth()}")
print(f"Gate count: {qc_transpiled.size()}")
print(f"Operations: {qc_transpiled.count_ops()}")

# Check two-qubit gate count (major error source)
two_qubit_gates = qc_transpiled.count_ops().get('cx', 0)
print(f"Two-qubit gates: {two_qubit_gates}")
```

* *Qiskit 生成的电路比领先的替代方案少了 29% 的两个量子位门**，从而显着减少了错误。

## 多电路转换 

转换多个电路高效：

```python
circuits = [qc1, qc2, qc3]
transpiled_circuits = transpile(
    circuits,
    backend=backend,
    optimization_level=3
)
```

## 预编译最佳实践

### 1. 在 Mind 中使用硬件拓扑进行设计

设计电路时考虑后端耦合图：

```python
# Check backend coupling
print(backend.coupling_map)

# Design circuits that align with coupling
```

### 2. 使用 Native Gates可能的

一些后端支持超出{CX, RZ, SX, X}的门：

```python
# Check available basis gates
print(backend.configuration().basis_gates)
```

### 3.最小化双量子位门

双量子位门的错误率明显更高：
- 设计算法以最小化CNOT Gates
- 使用门标识来减少计数

### 4. 首先使用模拟器进行测试

```python
from qiskit_aer import AerSimulator

# Test transpilation locally
sim_backend = AerSimulator.from_backend(backend)
qc_test = transpile(qc, backend=sim_backend, optimization_level=3)
```

## 不同提供程序的转换

### IBM Quantum

```python
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")
qc_transpiled = transpile(qc, backend=backend)
```

### IonQ

```python
# IonQ has all-to-all connectivity, different basis gates
basis_gates = ['gpi', 'gpi2', 'ms']
qc_transpiled = transpile(qc, basis_gates=basis_gates)
```

### 亚马逊 Braket

转译取决于特定设备（Rigetti、IonQ 等）

## 性能提示

1. **缓存转译电路** - 转译成本高昂，尽可能重用
2. **使用适当的优化级别** - 3 级速度较慢，但​​最适合生产 
3. **利用 v2.2 速度改进** - 更新到最新的 Qiskit，速度提升 83 倍
4. **并行转译** - Qiskit 在转译多个电路时自动并行化

## 常见问题和解决方案

### 问题：转译后电路太深
* *解决方案**：使用更高的优化级别或重新设计更少层数的电路

### 问题：插入太多SWAP门
* *解决方案**：调整initial_layout以更好地匹配量子位拓扑

### 问题：转换时间太长
* *解决方案**：降低优化级别或更新到Qiskit v2.2+以提高速度

### 问题：意外的门分解
* *解决方案**：检查basic_gates并考虑指定自定义分解规则
