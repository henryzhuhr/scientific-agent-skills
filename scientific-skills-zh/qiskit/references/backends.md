# 硬件后端和执行

Qiskit 与后端无关，支持在来自多个提供商的模拟器和真实量子硬件上执行。

## 后端类型

### 本地模拟器
- 在您的计算机上运行
- 无需帐户
- 非常适合开发和测试

### 基于云的硬件
- IBM Quantum（100+ 量子位系统）
- IonQ（捕获离子）
- Amazon Braket（Rigetti、IonQ、Oxford Quantum Circuits）
- 通过插件的其他提供商

## IBM Quantum 后端

### 连接到 IBM Quantum

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# First time: save credentials
QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token="YOUR_IBM_QUANTUM_TOKEN"
)

# Subsequent sessions: load credentials
service = QiskitRuntimeService()
```

### 列出可用后端

```python
# List all available backends
backends = service.backends()
for backend in backends:
    print(f"{backend.name}: {backend.num_qubits} qubits")

# Filter by minimum qubits
backends_127q = service.backends(min_num_qubits=127)

# Get specific backend
backend = service.backend("ibm_brisbane")
backend = service.least_busy()  # Get least busy backend
```

### 后端属性

```python
backend = service.backend("ibm_brisbane")

# Basic info
print(f"Name: {backend.name}")
print(f"Qubits: {backend.num_qubits}")
print(f"Version: {backend.version}")
print(f"Status: {backend.status()}")

# Coupling map (qubit connectivity)
print(backend.coupling_map)

# Basis gates
print(backend.configuration().basis_gates)

# Qubit properties
print(backend.qubit_properties(0))  # Properties of qubit 0
```

### 检查后端状态

```python
status = backend.status()
print(f"Operational: {status.operational}")
print(f"Pending jobs: {status.pending_jobs}")
print(f"Status message: {status.status_msg}")
```

## 在 IBM Quantum 硬件上运行

### 使用运行时基元

```python
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

# Create and transpile circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Transpile for backend
transpiled_qc = transpile(qc, backend=backend, optimization_level=3)

# Run with Sampler
sampler = Sampler(backend)
job = sampler.run([transpiled_qc], shots=1024)

# Retrieve results
result = job.result()
counts = result[0].data.meas.get_counts()
print(counts)
```

### 作业管理

```python
# Submit job
job = sampler.run([qc], shots=1024)

# Get job ID (save for later retrieval)
job_id = job.job_id()
print(f"Job ID: {job_id}")

# Check job status
print(job.status())

# Wait for completion
result = job.result()

# Retrieve job later
service = QiskitRuntimeService()
retrieved_job = service.job(job_id)
result = retrieved_job.result()
```

### 作业排队

```python
# Check queue position
job_status = job.status()
print(f"Queue position: {job.queue_position()}")

# Cancel job if needed
job.cancel()
```

## 会话模式

使用会话进行迭代算法（VQE，QAOA）以减少排队时间：

```python
from qiskit_ibm_runtime import Session, SamplerV2 as Sampler

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

with Session(backend=backend) as session:
    sampler = Sampler(session=session)

    # Multiple iterations in same session
    for iteration in range(10):
        # Parameterized circuit
        qc = create_parameterized_circuit(params[iteration])
        job = sampler.run([qc], shots=1024)
        result = job.result()

        # Update parameters based on results
        params[iteration + 1] = optimize(result)
```

会话好处：
- 减少之间的队列等待迭代
- 会话期间保证后端可用性
- 更适合变分算法

## 批处理模式

对独立并行作业使用批处理模式：

```python
from qiskit_ibm_runtime import Batch, SamplerV2 as Sampler

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

with Batch(backend=backend) as batch:
    sampler = Sampler(session=batch)

    # Submit multiple independent jobs
    jobs = []
    for qc in circuit_list:
        job = sampler.run([qc], shots=1024)
        jobs.append(job)

    # Collect all results
    results = [job.result() for job in jobs]
```

## 本地模拟器

### StatevectorSampler（理想）模拟）

```python
from qiskit.primitives import StatevectorSampler

sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
```

### Aer模拟器（真实噪声）

```python
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

# Ideal simulation
simulator = AerSimulator()

# Simulate with backend noise model
backend = service.backend("ibm_brisbane")
noisy_simulator = AerSimulator.from_backend(backend)

# Run simulation
transpiled_qc = transpile(qc, simulator)
sampler = Sampler(simulator)
job = sampler.run([transpiled_qc], shots=1024)
result = job.result()
```

### Aer GPU加速

```python
# Use GPU for faster simulation
simulator = AerSimulator(method='statevector', device='GPU')
```

## 第三方提供商

### IonQ

IonQ 提供具有全方位连接的俘获离子量子计算机：

```python
from qiskit_ionq import IonQProvider

provider = IonQProvider("YOUR_IONQ_API_TOKEN")

# List IonQ backends
backends = provider.backends()
backend = provider.get_backend("ionq_qpu")

# Run circuit
job = backend.run(qc, shots=1024)
result = job.result()
```

### Amazon Braket

```python
from qiskit_braket_provider import BraketProvider

provider = BraketProvider()

# List available devices
backends = provider.backends()

# Use specific device
backend = provider.get_backend("Rigetti")
job = backend.run(qc, shots=1024)
result = job.result()
```

## 错误缓解

### 测量误差缓解

```python
from qiskit_ibm_runtime import SamplerV2 as Sampler, Options

# Configure error mitigation
options = Options()
options.resilience_level = 1  # 0=none, 1=minimal, 2=moderate, 3=heavy

sampler = Sampler(backend, options=options)
job = sampler.run([qc], shots=1024)
result = job.result()
```

### 错误缓解级别

- **级别0**：无缓解
- **级别1**：读出错误缓解
- **级别2**：级别1 + 门错误缓解
- **级别 3**：级别 2 + 先进技术

* *Qiskit 的 Samplomatic 包** 可以通过概率误差消除将采样开销减少多达 100 倍。

### 零噪声外推 (ZNE)

```python
options = Options()
options.resilience_level = 2
options.resilience.zne_mitigation = True

sampler = Sampler(backend, options=options)
```

## 监控使用情况和成本

### 检查帐户使用情况

```python
# For IBM Quantum
service = QiskitRuntimeService()

# Check remaining credits
print(service.usage())
```

### 估计作业成本

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

backend = service.backend("ibm_brisbane")

# Estimate job cost
estimator = Estimator(backend)
# Cost depends on circuit complexity and shots
```

## 最佳实践

### 1.始终在运行之前进行转换

```python
# Bad: Run without transpilation
job = sampler.run([qc], shots=1024)

# Good: Transpile first
qc_transpiled = transpile(qc, backend=backend, optimization_level=3)
job = sampler.run([qc_transpiled], shots=1024)
```

### 2.首先使用模拟器进行测试

```python
# Test with noisy simulator before hardware
noisy_sim = AerSimulator.from_backend(backend)
qc_test = transpile(qc, noisy_sim, optimization_level=3)

# Verify results look reasonable
# Then run on hardware
```

### 3. 使用适当的镜头计数

```python
# For optimization algorithms: fewer shots (100-1000)
# For final measurements: more shots (10000+)

# Adaptive shots based on stage
shots_optimization = 500
shots_final = 10000
```

### 4. 战略性地选择后端

```python
# For testing: Use least busy backend
backend = service.least_busy(min_num_qubits=5)

# For production: Use backend matching requirements
backend = service.backend("ibm_brisbane")  # 127 qubits
```

### 5. 使用变分算法的会话

会话非常适合VQE， 

### 6. 监控作业状态

```python
import time

job = sampler.run([qc], shots=1024)

while job.status().name not in ['DONE', 'ERROR', 'CANCELLED']:
    print(f"Status: {job.status().name}")
    time.sleep(10)

result = job.result()
```

## 故障排除

### 问题：“未找到后端”
```python
# List available backends
print([b.name for b in service.backends()])
```

### 问题：“无效凭证“
```python
# Re-save credentials
QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token="YOUR_TOKEN",
    overwrite=True
)
```

### 问题：排队时间长
```python
# Use least busy backend
backend = service.least_busy(min_num_qubits=5)

# Or use batch mode for multiple independent jobs
```

### 问题：作业因“电路太大”而失败 
```python
# Reduce circuit complexity
# Use higher transpilation optimization
qc_opt = transpile(qc, backend=backend, optimization_level=3)
```

## 后端比较

|供应商|连接性|门套|备注 |
|----------|------------|---------|--------|
| IBM 量子 |有限公司| CX、RZ、SX、X | 100+量子比特系统，高品质|
|离子Q |全部到全部 | GPI、GPI2、MS |离子捕获，错误率低|
|里杰蒂|有限公司| CZ、RZ、RX |超导量子位|
|牛津量子电路|有限公司| ECR、RZ、SX |同轴科技|
