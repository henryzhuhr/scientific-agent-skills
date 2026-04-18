# Qiskit 原语

原语是执行量子电路的基本构建块。 Qiskit 提供两个主要原语：**采样器**（用于测量位串）和 **估计器**（用于计算期望值）。

## 原语类型

### Sampler
计算量子电路中位串的概率或准概率。当您需要时使用：
- 测量结果
- 输出概率分布
- 从量子态采样

### 估计器
计算量子电路可观测值的期望值。当您需要时使用：
- 能量计算
- 可观测测量
- 变分算法优化

## V2 接口（当前标准）

Qiskit 使用V2 原语（BaseSamplerV2、BaseEstimatorV2）作为当前标准。 V1原语是遗留的。

## 采样器原语

### 状态向量采样器（本地模拟）

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Create circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Run with Sampler
sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()

# Access results
counts = result[0].data.meas.get_counts()
print(counts)  # e.g., {'00': 523, '11': 501}
```

### 多个电路

```python
qc1 = QuantumCircuit(2)
qc1.h(0)
qc1.measure_all()

qc2 = QuantumCircuit(2)
qc2.x(0)
qc2.measure_all()

# Run multiple circuits
sampler = StatevectorSampler()
job = sampler.run([qc1, qc2], shots=1000)
results = job.result()

# Access individual results
counts1 = results[0].data.meas.get_counts()
counts2 = results[1].data.meas.get_counts()
```

### 使用参数

```python
from qiskit.circuit import Parameter

theta = Parameter('θ')
qc = QuantumCircuit(1)
qc.ry(theta, 0)
qc.measure_all()

# Run with parameter values
sampler = StatevectorSampler()
param_values = [[0], [np.pi/4], [np.pi/2]]
result = sampler.run([(qc, param_values)], shots=1024).result()
```

## 估计器基元

### 状态向量估计器（局部模拟）

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

# Create circuit WITHOUT measurements
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# Define observable
observable = SparsePauliOp(["ZZ", "XX"])

# Run Estimator
estimator = StatevectorEstimator()
result = estimator.run([(qc, observable)]).result()

# Access expectation values
exp_value = result[0].data.evs
print(f"Expectation value: {exp_value}")
```

### 多个可观测值

```python
from qiskit.quantum_info import SparsePauliOp

qc = QuantumCircuit(2)
qc.h(0)

obs1 = SparsePauliOp(["ZZ"])
obs2 = SparsePauliOp(["XX"])

estimator = StatevectorEstimator()
result = estimator.run([(qc, obs1), (qc, obs2)]).result()

ev1 = result[0].data.evs
ev2 = result[1].data.evs
```

### 参数化估计器

```python
from qiskit.circuit import Parameter
import numpy as np

theta = Parameter('θ')
qc = QuantumCircuit(1)
qc.ry(theta, 0)

observable = SparsePauliOp(["Z"])

# Run with multiple parameter values
estimator = StatevectorEstimator()
param_values = [[0], [np.pi/4], [np.pi/2], [np.pi]]
result = estimator.run([(qc, observable, param_values)]).result()
```

## IBM Quantum Runtime Primitives

对于在真实硬件上运行，请使用运行时原语：

### Runtime Sampler

```python
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Run on real hardware
sampler = Sampler(backend)
job = sampler.run([qc], shots=1024)
result = job.result()
counts = result[0].data.meas.get_counts()
```

### Runtime Estimator

```python
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator
from qiskit.quantum_info import SparsePauliOp

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

observable = SparsePauliOp(["ZZ"])

# Run on real hardware
estimator = Estimator(backend)
job = estimator.run([(qc, observable)])
result = job.result()
exp_value = result[0].data.evs
```

## 迭代工作负载的会话

会话将多个作业分组以减少队列等待时间：

```python
from qiskit_ibm_runtime import Session

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

with Session(backend=backend) as session:
    sampler = Sampler(session=session)

    # Run multiple jobs in session
    job1 = sampler.run([qc1], shots=1024)
    result1 = job1.result()

    job2 = sampler.run([qc2], shots=1024)
    result2 = job2.result()
```

## 并行作业的批处理模式

批处理模式运行独立作业并行：

```python
from qiskit_ibm_runtime import Batch

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

with Batch(backend=backend) as batch:
    sampler = Sampler(session=batch)

    # Submit multiple independent jobs
    job1 = sampler.run([qc1], shots=1024)
    job2 = sampler.run([qc2], shots=1024)

    # Retrieve results when ready
    result1 = job1.result()
    result2 = job2.result()
```

## 结果处理

### 采样器结果

```python
result = sampler.run([qc], shots=1024).result()

# Get counts
counts = result[0].data.meas.get_counts()

# Get probabilities
probs = {k: v/1024 for k, v in counts.items()}

# Get metadata
metadata = result[0].metadata
```

### 估计器结果

```python
result = estimator.run([(qc, observable)]).result()

# Expectation value
exp_val = result[0].data.evs

# Standard deviation (if available)
std_dev = result[0].data.stds

# Metadata
metadata = result[0].metadata
```

## 与V1的差异基元

* *V2 改进：**
- 更灵活的参数绑定
- 更好的结果结构
- 改进的性能
- 更简洁的API 设计

* *从 V1 迁移：**
- 使用 `StatevectorSampler` 代替 `Sampler`
- 使用 `StatevectorEstimator` 代替 `Estimator`
- 结果访问从 `.result().quasi_dists[0]` 更改为 `.result()[0].data.meas.get_counts()`
