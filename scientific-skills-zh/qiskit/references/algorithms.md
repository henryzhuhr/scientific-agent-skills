# 量子算法和应用

Qiskit 支持多种用于优化、化学、机器学习和物理模拟的量子算法。

## 目录

1. [优化算法](#optimization-algorithms)
2. [化学与材料科学](#chemistry-and-materials-science)
3. [机器学习](#machine-learning)
4. [算法库](#algorithm-libraries)

## 优化算法

### 变分量子特征求解器 (VQE)

VQE 使用混合量子经典方法查找哈密顿量的最小特征值。

* *用例：**
- 分子基态能量
- 组合优化
- 材料模拟

* *实现：**
```python
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator, Session
from qiskit.quantum_info import SparsePauliOp
from scipy.optimize import minimize
import numpy as np

def vqe_algorithm(hamiltonian, ansatz, backend, initial_params):
    """
    Run VQE algorithm

    Args:
        hamiltonian: Observable (SparsePauliOp)
        ansatz: Parameterized quantum circuit
        backend: Quantum backend
        initial_params: Initial parameter values
    """

    with Session(backend=backend) as session:
        estimator = Estimator(session=session)

        def cost_function(params):
            # Bind parameters to circuit
            bound_circuit = ansatz.assign_parameters(params)

            # Transpile for hardware
            qc_isa = transpile(bound_circuit, backend=backend, optimization_level=3)

            # Compute expectation value
            job = estimator.run([(qc_isa, hamiltonian)])
            result = job.result()
            energy = result[0].data.evs

            return energy

        # Classical optimization
        result = minimize(
            cost_function,
            initial_params,
            method='COBYLA',
            options={'maxiter': 100}
        )

    return result.fun, result.x

# Example: H2 molecule Hamiltonian
hamiltonian = SparsePauliOp(
    ["IIII", "ZZII", "IIZZ", "ZZZI", "IZZI"],
    coeffs=[-0.8, 0.17, 0.17, -0.24, 0.17]
)

# Create ansatz
qc = QuantumCircuit(4)
# ... define ansatz structure ...

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

energy, params = vqe_algorithm(hamiltonian, qc, backend, np.random.rand(10))
print(f"Ground state energy: {energy}")
```

### 量子近似优化算法（QAOA）

QAOA解决组合优化问题，如MaxCut， TSP 和图形着色。

* *用例：**
- MaxCut 问题
- 投资组合优化
- 车辆路线
- 调度问题

* *实现：**
```python
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import networkx as nx

def qaoa_maxcut(graph, p, backend):
    """
    QAOA for MaxCut problem

    Args:
        graph: NetworkX graph
        p: Number of QAOA layers
        backend: Quantum backend
    """
    num_qubits = len(graph.nodes())
    qc = QuantumCircuit(num_qubits)

    # Initial superposition
    qc.h(range(num_qubits))

    # Alternating layers
    betas = [Parameter(f'β_{i}') for i in range(p)]
    gammas = [Parameter(f'γ_{i}') for i in range(p)]

    for i in range(p):
        # Problem Hamiltonian (MaxCut)
        for edge in graph.edges():
            u, v = edge
            qc.cx(u, v)
            qc.rz(2 * gammas[i], v)
            qc.cx(u, v)

        # Mixer Hamiltonian
        for qubit in range(num_qubits):
            qc.rx(2 * betas[i], qubit)

    qc.measure_all()
    return qc, betas + gammas

# Example: MaxCut on 4-node graph
G = nx.Graph()
G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])

qaoa_circuit, params = qaoa_maxcut(G, p=2, backend=backend)

# Run with Sampler and optimize parameters
# ... (similar to VQE optimization loop)
```

### Grover 算法

量子搜索算法为非结构化搜索提供二次加速。

* *用例：**
- 数据库搜索
- SAT求解
- 查找标记项

* *实现：**
```python
from qiskit import QuantumCircuit

def grover_oracle(marked_states):
    """Create oracle that marks target states"""
    num_qubits = len(marked_states[0])
    qc = QuantumCircuit(num_qubits)

    for target in marked_states:
        # Flip phase of target state
        for i, bit in enumerate(target):
            if bit == '0':
                qc.x(i)

        # Multi-controlled Z
        qc.h(num_qubits - 1)
        qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
        qc.h(num_qubits - 1)

        for i, bit in enumerate(target):
            if bit == '0':
                qc.x(i)

    return qc

def grover_diffusion(num_qubits):
    """Create Grover diffusion operator"""
    qc = QuantumCircuit(num_qubits)

    qc.h(range(num_qubits))
    qc.x(range(num_qubits))

    qc.h(num_qubits - 1)
    qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    qc.h(num_qubits - 1)

    qc.x(range(num_qubits))
    qc.h(range(num_qubits))

    return qc

def grover_algorithm(marked_states, num_iterations):
    """Complete Grover's algorithm"""
    num_qubits = len(marked_states[0])
    qc = QuantumCircuit(num_qubits)

    # Initialize superposition
    qc.h(range(num_qubits))

    # Grover iterations
    oracle = grover_oracle(marked_states)
    diffusion = grover_diffusion(num_qubits)

    for _ in range(num_iterations):
        qc.compose(oracle, inplace=True)
        qc.compose(diffusion, inplace=True)

    qc.measure_all()
    return qc

# Search for state |101⟩ in 3-qubit space
marked = ['101']
iterations = int(np.pi/4 * np.sqrt(2**3))  # Optimal iterations
qc_grover = grover_algorithm(marked, iterations)
```

## 化学与材料科学

### 分子基态能量

* *安装Qiskit性质：**
```bash
uv pip install qiskit-nature qiskit-nature-pyscf
```

* *示例：H2分子**
```python
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper, ParityMapper
from qiskit_nature.second_q.circuit.library import UCCSD, HartreeFock

# Define molecule
driver = PySCFDriver(
    atom="H 0 0 0; H 0 0 0.735",
    basis="sto3g",
    charge=0,
    spin=0
)

# Get electronic structure problem
problem = driver.run()

# Map fermionic operators to qubits
mapper = JordanWignerMapper()
hamiltonian = mapper.map(problem.hamiltonian.second_q_op())

# Create initial state
num_particles = problem.num_particles
num_spatial_orbitals = problem.num_spatial_orbitals

init_state = HartreeFock(
    num_spatial_orbitals,
    num_particles,
    mapper
)

# Create ansatz
ansatz = UCCSD(
    num_spatial_orbitals,
    num_particles,
    mapper,
    initial_state=init_state
)

# Run VQE
energy, params = vqe_algorithm(
    hamiltonian,
    ansatz,
    backend,
    np.zeros(ansatz.num_parameters)
)

# Add nuclear repulsion energy
total_energy = energy + problem.nuclear_repulsion_energy
print(f"Ground state energy: {total_energy} Ha")
```

### 不同的分子作图器

```python
# Jordan-Wigner mapping
jw_mapper = JordanWignerMapper()
ham_jw = jw_mapper.map(problem.hamiltonian.second_q_op())

# Parity mapping (often more efficient)
parity_mapper = ParityMapper()
ham_parity = parity_mapper.map(problem.hamiltonian.second_q_op())

# Bravyi-Kitaev mapping
from qiskit_nature.second_q.mappers import BravyiKitaevMapper
bk_mapper = BravyiKitaevMapper()
ham_bk = bk_mapper.map(problem.hamiltonian.second_q_op())
```

### 兴奋状态

```python
from qiskit_nature.second_q.algorithms import QEOM

# Quantum Equation of Motion for excited states
qeom = QEOM(estimator, ansatz, 'sd')  # Singles and doubles excitations
excited_states = qeom.solve(problem)
```

## 机器学习

### 量子内核

量子计算机可以计算机器学习的内核函数。

* *安装Qiskit机器学习：**
```bash
uv pip install qiskit-machine-learning
```

* *示例：使用量子核进行分类**
```python
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_algorithms.state_fidelities import ComputeUncompute
from qiskit.circuit.library import ZZFeatureMap
from sklearn.svm import SVC
import numpy as np

# Create feature map
num_features = 2
feature_map = ZZFeatureMap(feature_dimension=num_features, reps=2)

# Create quantum kernel
fidelity = ComputeUncompute(sampler=sampler)
qkernel = FidelityQuantumKernel(fidelity=fidelity, feature_map=feature_map)

# Use with scikit-learn
X_train = np.random.rand(50, 2)
y_train = np.random.choice([0, 1], 50)

# Compute kernel matrix
kernel_matrix = qkernel.evaluate(X_train)

# Train SVM with quantum kernel
svc = SVC(kernel='precomputed')
svc.fit(kernel_matrix, y_train)

# Predict
X_test = np.random.rand(10, 2)
kernel_test = qkernel.evaluate(X_test, X_train)
predictions = svc.predict(kernel_test)
```

### 变分量子分类器（VQC）

```python
from qiskit_machine_learning.algorithms import VQC
from qiskit.circuit.library import RealAmplitudes

# Create feature map and ansatz
feature_map = ZZFeatureMap(2)
ansatz = RealAmplitudes(2, reps=1)

# Create VQC
vqc = VQC(
    sampler=sampler,
    feature_map=feature_map,
    ansatz=ansatz,
    optimizer='COBYLA'
)

# Train
vqc.fit(X_train, y_train)

# Predict
predictions = vqc.predict(X_test)
accuracy = vqc.score(X_test, y_test)
```

### 量子神经网络 (QNN)

```python
from qiskit_machine_learning.neural_networks import SamplerQNN
from qiskit.circuit import QuantumCircuit, Parameter

# Create parameterized circuit
qc = QuantumCircuit(2)
params = [Parameter(f'θ_{i}') for i in range(4)]

# Network structure
for i, param in enumerate(params[:2]):
    qc.ry(param, i)

qc.cx(0, 1)

for i, param in enumerate(params[2:]):
    qc.ry(param, i)

qc.measure_all()

# Create QNN
qnn = SamplerQNN(
    circuit=qc,
    sampler=sampler,
    input_params=[],  # No input parameters for this example
    weight_params=params
)

# Use with PyTorch or TensorFlow for training
```

## 算法库

### Qiskit 算法

量子算法的标准实现：

```bash
uv pip install qiskit-algorithms
```

* *可用算法：**
- 幅度估计
- 相位估计
- 肖尔算法
- 量子傅里叶变换
- HHL （线性系统）

* *示例：量子相位估计**
```python
from qiskit.circuit.library import QFT
from qiskit_algorithms import PhaseEstimation

# Create unitary operator
num_qubits = 3
unitary = QuantumCircuit(num_qubits)
# ... define unitary ...

# Phase estimation
pe = PhaseEstimation(num_evaluation_qubits=3, quantum_instance=backend)
result = pe.estimate(unitary=unitary, state_preparation=initial_state)
```

### Qiskit 优化

优化问题求解器：

```bash
uv pip install qiskit-optimization
```

* *支持问题：**
- 二次规划
- 整数规划
- 线性规划
- 约束满足

* *示例：投资组合优化**
```python
from qiskit_optimization.applications import PortfolioOptimization
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA

# Define portfolio problem
returns = [0.1, 0.15, 0.12]  # Expected returns
covariances = [[1, 0.5, 0.3], [0.5, 1, 0.4], [0.3, 0.4, 1]]
budget = 2  # Number of assets to select

portfolio = PortfolioOptimization(
    expected_returns=returns,
    covariances=covariances,
    budget=budget
)

# Convert to quadratic program
qp = portfolio.to_quadratic_program()

# Solve with QAOA
qaoa = QAOA(sampler=sampler, optimizer='COBYLA', reps=2)
optimizer = MinimumEigenOptimizer(qaoa)

result = optimizer.solve(qp)
print(f"Optimal portfolio: {result.x}")
```

## 物理模拟

### 时间演化

```python
from qiskit.synthesis import SuzukiTrotter
from qiskit.quantum_info import SparsePauliOp

# Define Hamiltonian
hamiltonian = SparsePauliOp(["XX", "YY", "ZZ"], coeffs=[1.0, 1.0, 1.0])

# Time evolution
time = 1.0
evolution_gate = SuzukiTrotter(order=2, reps=10).synthesize(
    hamiltonian,
    time
)

qc = QuantumCircuit(2)
qc.append(evolution_gate, range(2))
```

### 偏微分方程

* *用例：**用于求解具有潜在指数加速的偏微分方程的量子算法。

```python
# Quantum PDE solver implementation
# Requires advanced techniques like HHL algorithm
# and amplitude encoding of solution vectors
```

## 基准测试

### Benchpress Toolkit

基准量子算法：

```python
# Benchpress provides standardized benchmarks
# for comparing quantum algorithm performance

# Examples:
# - Quantum volume circuits
# - Random circuit sampling
# - Application-specific benchmarks
```

## 最佳实践

### 1. 启动Simple
从小问题实例开始，验证您的算法做法：
```python
# Test with 2-3 qubits first
# Scale up after confirming correctness
```

### 2. 使用模拟器进行开发
```python
from qiskit.primitives import StatevectorSampler

# Develop with local simulator
sampler_sim = StatevectorSampler()

# Switch to hardware for production
# sampler_hw = Sampler(backend)
```

### 3. 监控收敛
```python
convergence_data = []

def tracked_cost_function(params):
    energy = cost_function(params)
    convergence_data.append(energy)
    return energy

# Plot convergence after optimization
import matplotlib.pyplot as plt
plt.plot(convergence_data)
plt.xlabel('Iteration')
plt.ylabel('Energy')
plt.show()
```

### 4. 参数初始化
```python
# Use problem-specific initialization when possible
# Random initialization
initial_params = np.random.uniform(0, 2*np.pi, num_params)

# Or use classical preprocessing
# initial_params = classical_solution_to_params(classical_result)
```

### 5.保存中间结果
```python
import json

checkpoint = {
    'iteration': iteration,
    'params': params.tolist(),
    'energy': energy,
    'timestamp': time.time()
}

with open(f'checkpoint_{iteration}.json', 'w') as f:
    json.dump(checkpoint, f)
```

## 资源和进一步阅读

* *官方文档：**
- [Qiskit教材](https://qiskit.org/learn)
- [Qiskit Nature 文档](https://qiskit.org/ecosystem/nature)
- [Qiskit 机器学习文档](https://qiskit.org/ecosystem/machine-learning)
- [Qiskit 优化文档](https://qiskit.org/ecosystem/optimization)

* *研究论文：**
- VQE：Peruzzo 等人，Nature Communications (2014)
- QAOA：Farhi 等人，arXiv:1411.4028
- 量子内核： Havlíček 等人，《自然》(2019)
