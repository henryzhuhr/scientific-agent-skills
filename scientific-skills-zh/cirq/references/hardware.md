# 硬件集成

本指南介绍了通过 Cirq 的设备接口和服务提供商在真正的量子硬件上运行量子电路。

## 设备表示

### 设备类

```python
import cirq

# Define device with connectivity
class MyDevice(cirq.Device):
    def __init__(self, qubits, connectivity):
        self.qubits = qubits
        self.connectivity = connectivity

    @property
    def metadata(self):
        return cirq.DeviceMetadata(
            self.qubits,
            self.connectivity
        )

    def validate_operation(self, operation):
        # Check if operation is valid on this device
        if len(operation.qubits) == 2:
            q0, q1 = operation.qubits
            if (q0, q1) not in self.connectivity:
                raise ValueError(f"Qubits {q0} and {q1} not connected")
```

### 设备约束

```python
# Check device metadata
device = cirq_google.Sycamore

# Get qubit topology
qubits = device.metadata.qubit_set
print(f"Available qubits: {len(qubits)}")

# Check connectivity
for q0 in qubits:
    neighbors = device.metadata.nx_graph.neighbors(q0)
    print(f"{q0} connected to: {list(neighbors)}")

# Validate circuit against device
try:
    device.validate_circuit(circuit)
    print("Circuit is valid for device")
except ValueError as e:
    print(f"Invalid circuit: {e}")
```

## 量子位选择

### 最佳量子位选择

```python
import cirq_google

# Get calibration metrics
processor = cirq_google.get_engine().get_processor('weber')
calibration = processor.get_current_calibration()

# Find qubits with lowest error rates
def select_best_qubits(calibration, n_qubits):
    """Select n qubits with best single-qubit gate fidelity."""
    qubit_fidelities = {}

    for qubit in calibration.keys():
        if 'single_qubit_rb_average_error_per_gate' in calibration[qubit]:
            error = calibration[qubit]['single_qubit_rb_average_error_per_gate']
            qubit_fidelities[qubit] = 1 - error

    # Sort by fidelity
    best_qubits = sorted(
        qubit_fidelities.items(),
        key=lambda x: x[1],
        reverse=True
    )[:n_qubits]

    return [q for q, _ in best_qubits]

best_qubits = select_best_qubits(calibration, n_qubits=10)
```

### 拓扑感知选择

```python
def select_connected_qubits(device, n_qubits):
    """Select connected qubits forming a path or grid."""
    graph = device.metadata.nx_graph

    # Find connected subgraph
    import networkx as nx
    for node in graph.nodes():
        subgraph = nx.ego_graph(graph, node, radius=n_qubits)
        if len(subgraph) >= n_qubits:
            return list(subgraph.nodes())[:n_qubits]

    raise ValueError(f"Could not find {n_qubits} connected qubits")
```

## 服务提供商

### Google Quantum AI (Cirq-Google)

#### 设置

```python
import cirq_google

# Authenticate (requires Google Cloud project)
# Set environment variable: GOOGLE_CLOUD_PROJECT=your-project-id

# Get quantum engine
engine = cirq_google.get_engine()

# List available processors
processors = engine.list_processors()
for processor in processors:
    print(f"Processor: {processor.processor_id}")
```

#### 在 Google 硬件上运行

```python
# Create circuit for Google device
import cirq_google

# Get processor
processor = engine.get_processor('weber')
device = processor.get_device()

# Create circuit on device qubits
qubits = sorted(device.metadata.qubit_set)[:5]
circuit = cirq.Circuit(
    cirq.H(qubits[0]),
    cirq.CZ(qubits[0], qubits[1]),
    cirq.measure(*qubits, key='result')
)

# Validate and run
device.validate_circuit(circuit)
job = processor.run(circuit, repetitions=1000)

# Get results
results = job.results()[0]
print(results.histogram(key='result'))
```

### IonQ

#### 设置

```python
import cirq_ionq

# Set API key
# Option 1: Environment variable
# export IONQ_API_KEY=your_api_key

# Option 2: In code
service = cirq_ionq.Service(api_key='your_api_key')
```

#### 在 Ion 上运行Q

```python
import cirq_ionq

# Create service
service = cirq_ionq.Service(api_key='your_api_key')

# Create circuit (IonQ uses generic qubits)
qubits = cirq.LineQubit.range(3)
circuit = cirq.Circuit(
    cirq.H(qubits[0]),
    cirq.CNOT(qubits[0], qubits[1]),
    cirq.CNOT(qubits[1], qubits[2]),
    cirq.measure(*qubits, key='result')
)

# Run on simulator
result = service.run(
    circuit=circuit,
    repetitions=1000,
    target='simulator'
)
print(result.histogram(key='result'))

# Run on hardware
result = service.run(
    circuit=circuit,
    repetitions=1000,
    target='qpu'
)
```

#### IonQ 作业管理

```python
# Create job
job = service.create_job(circuit, repetitions=1000, target='qpu')

# Check job status
status = job.status()
print(f"Job status: {status}")

# Wait for completion
job.wait_until_complete()

# Get results
results = job.results()
```

#### IonQ 校准数据

```python
# Get current calibration
calibration = service.get_current_calibration()

# Access metrics
print(f"Fidelity: {calibration['fidelity']}")
print(f"Timing: {calibration['timing']}")
```

### Azure Quantum

#### 设置

```python
from azure.quantum import Workspace
from azure.quantum.cirq import AzureQuantumService

# Create workspace connection
workspace = Workspace(
    resource_id="/subscriptions/.../resourceGroups/.../providers/Microsoft.Quantum/Workspaces/...",
    location="eastus"
)

# Create Cirq service
service = AzureQuantumService(workspace)
```

#### 在 Azure Quantum 上运行 (IonQ后端）

```python
# List available targets
targets = service.targets()
for target in targets:
    print(f"Target: {target.name}")

# Run on IonQ simulator
result = service.run(
    circuit=circuit,
    repetitions=1000,
    target='ionq.simulator'
)

# Run on IonQ QPU
result = service.run(
    circuit=circuit,
    repetitions=1000,
    target='ionq.qpu'
)
```

#### 在 Azure Quantum 上运行（Honeywell 后端）

```python
# Run on Honeywell System Model H1
result = service.run(
    circuit=circuit,
    repetitions=1000,
    target='honeywell.hqs-lt-s1'
)

# Check Honeywell-specific options
target_info = service.get_target('honeywell.hqs-lt-s1')
print(f"Target info: {target_info}")
```

### AQT（Alpine Quantum Technologies）

#### 设置

```python
import cirq_aqt

# Set API token
# export AQT_TOKEN=your_token

# Create service
service = cirq_aqt.AQTSampler(
    remote_host='https://gateway.aqt.eu',
    access_token='your_token'
)
```

#### 运行于 AQT

```python
# Create circuit
qubits = cirq.LineQubit.range(3)
circuit = cirq.Circuit(
    cirq.H(qubits[0]),
    cirq.CNOT(qubits[0], qubits[1]),
    cirq.measure(*qubits, key='result')
)

# Run on simulator
result = service.run(
    circuit,
    repetitions=1000,
    target='simulator'
)

# Run on device
result = service.run(
    circuit,
    repetitions=1000,
    target='device'
)
```

### Pasqal

#### 设置

```python
import cirq_pasqal

# Create Pasqal device
device = cirq_pasqal.PasqalDevice(qubits=cirq.LineQubit.range(10))
```

#### 运行于Pasqal

```python
# Create sampler
sampler = cirq_pasqal.PasqalSampler(
    remote_host='https://api.pasqal.cloud',
    access_token='your_token',
    device=device
)

# Run circuit
result = sampler.run(circuit, repetitions=1000)
```

## 硬件最佳实践

### 硬件电路优化

```python
def optimize_for_hardware(circuit, device):
    """Optimize circuit for specific hardware."""
    from cirq.transformers import (
        optimize_for_target_gateset,
        merge_single_qubit_gates_to_phxz,
        drop_negligible_operations
    )

    # Get device gateset
    if hasattr(device, 'gateset'):
        gateset = device.gateset
    else:
        gateset = cirq.CZTargetGateset()  # Default

    # Optimize
    circuit = merge_single_qubit_gates_to_phxz(circuit)
    circuit = drop_negligible_operations(circuit)
    circuit = optimize_for_target_gateset(circuit, gateset=gateset)

    return circuit
```

### 错误缓解

```python
def run_with_readout_error_mitigation(circuit, sampler, repetitions):
    """Mitigate readout errors using calibration."""

    # Measure readout error
    cal_circuits = []
    for state in range(2**len(circuit.qubits)):
        cal_circuit = cirq.Circuit()
        for i, q in enumerate(circuit.qubits):
            if state & (1 << i):
                cal_circuit.append(cirq.X(q))
        cal_circuit.append(cirq.measure(*circuit.qubits, key='m'))
        cal_circuits.append(cal_circuit)

    # Run calibration
    cal_results = [sampler.run(c, repetitions=1000) for c in cal_circuits]

    # Build confusion matrix
    # ... (implementation details)

    # Run actual circuit
    result = sampler.run(circuit, repetitions=repetitions)

    # Apply correction
    # ... (apply inverse of confusion matrix)

    return result
```

### 作业管理

```python
def submit_jobs_in_batches(circuits, sampler, batch_size=10):
    """Submit multiple circuits in batches."""
    jobs = []

    for i in range(0, len(circuits), batch_size):
        batch = circuits[i:i+batch_size]
        job_ids = []

        for circuit in batch:
            job = sampler.run_async(circuit, repetitions=1000)
            job_ids.append(job)

        jobs.extend(job_ids)

    # Wait for all jobs
    results = [job.result() for job in jobs]
    return results
```

## 设备规格

### 检查设备功能

```python
def print_device_info(device):
    """Print device capabilities and constraints."""

    print(f"Device: {device}")
    print(f"Number of qubits: {len(device.metadata.qubit_set)}")

    # Gate support
    print("\nSupported gates:")
    if hasattr(device, 'gateset'):
        for gate in device.gateset.gates:
            print(f"  - {gate}")

    # Connectivity
    print("\nConnectivity:")
    graph = device.metadata.nx_graph
    print(f"  Edges: {graph.number_of_edges()}")
    print(f"  Average degree: {sum(dict(graph.degree()).values()) / graph.number_of_nodes():.2f}")

    # Duration constraints
    if hasattr(device, 'gate_durations'):
        print("\nGate durations:")
        for gate, duration in device.gate_durations.items():
            print(f"  {gate}: {duration}")
```

## 身份验证和访问

### 设置凭据

* *Google云：**
```bash
# Install gcloud CLI
# Visit: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth application-default login

# Set project
export GOOGLE_CLOUD_PROJECT=your-project-id
```

* *离子Q：**
```bash
# Set API key
export IONQ_API_KEY=your_api_key
```

* *Azure量子：**
```python
# Use Azure CLI or workspace connection string
# See: https://docs.microsoft.com/azure/quantum/
```

* *AQT：**
```bash
# Request access token from AQT
export AQT_TOKEN=your_token
```

* *Pasqal：**
```bash
# Request API access from Pasqal
export PASQAL_TOKEN=your_token
```

## 最佳实践

1. **提交前验证电路**：使用 device.validate_ Circuit()
2. **针对目标硬件进行优化**：分解为本机门
3. **选择最佳量子位**：使用校准数据进行量子位选择
4. **监控作业状态**：在检索结果之前检查作业完成情况
5. **实施错误缓解**：使用读出错误校正
6. **高效批处理作业**：一起提交多个电路
7. **尊重率限制**：遵循提供商特定的 API 限制
8. **存储结果**：立即保存昂贵的硬件结果
9. **首先在模拟器上测试**：在硬件
10之前在模拟器上进行验证。 **保持电路浅**：硬件的相干时间有限
