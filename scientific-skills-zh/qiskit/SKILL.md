---
name: qiskit
description: IBM 量子计算框架。当针对 IBM Quantum 硬件、使用 Qiskit Runtime 处理生产工作负载或需要 IBM 优化工具时使用。最适合 IBM 硬件执行、量子错误缓解和企业量子计算。对于 Google 硬件，请使用 cirq；对于基于梯度的量子机器学习，使用 pennylane；对于开放量子系统模拟，请使用 qutip。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# Qiskit

## 概述

Qiskit 是全球最受欢迎的开源量子计算框架，下载量超过 1300 万次。构建量子电路，优化硬件，在模拟器或真实量子计算机上执行，并分析结果。支持 IBM Quantum（100 多个量子位系统）、IonQ、Amazon Braket 和其他提供商。

* *主要特性：**
- 转译速度比竞争对手快 83 倍
- 优化电路中的两个量子位门减少 29%
- 与后端无关的执行（本地模拟器或云）硬件）
- 用于优化、化学和 ML

## 快速入门

### 安装

```bash
uv pip install qiskit
uv pip install "qiskit[visualization]" matplotlib
```

### 第一电路

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# Create Bell state (entangled qubits)
qc = QuantumCircuit(2)
qc.h(0)           # Hadamard on qubit 0
qc.cx(0, 1)       # CNOT from qubit 0 to 1
qc.measure_all()  # Measure both qubits

# Run locally
sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
print(counts)  # {'00': ~512, '11': ~512}
```

### 可视化

```python
from qiskit.visualization import plot_histogram

qc.draw('mpl')           # Circuit diagram
plot_histogram(counts)   # Results histogram
```

## 核心功能

### 1. 设置和安装
有关详细安装、身份验证和 IBM Quantum 帐户设置：
- **请参阅 `references/setup.md`**

 涵盖的主题：
- 使用 uv 安装
- Python 环境设置
- IBM Quantum 帐户和 API 令牌配置
- 本地执行与云执行

### 2. 构建量子电路
用于构建具有门、测量和组合的量子电路：
- **参见`references/circuits.md`**

涵盖的主题：
- 使用 QuantumCircuit 创建电路
- 单量子位门（H、X、Y、Z、旋转、相位门）
- 多量子位门（CNOT、SWAP、Toffoli）
- 测量和障碍
- 电路组成和特性
- 变分算法的参数化电路

### 3.原语（采样器和估计器）
用于执行量子电路和计算结果：
- **参见`references/primitives.md`**

涵盖的主题：
- **Sampler**：获取位串测量和概率分布
- **Estimator**：计算可观测值的期望值
- V2 接口（StatevectorSampler、StatevectorEstimator）
- 用于硬件的 IBM Quantum Runtime 原语
- 会话和批处理模式
- 参数绑定

### 4. 转译和优化
用于优化电路和准备硬件执行：
- **参见`references/transpilation.md`**

涵盖的主题：
- 为什么需要转译
- 优化级别(0-3)
- 六个编译阶段（初始化、布局、路由、翻译、优化、调度）
- 高级功能（虚拟排列省略、门取消）
- 常用参数（初始布局、近似度、种子）
- 高效电路的最佳实践

### 5.可视化
用于显示电路、结果和量子态：
- **参见`references/visualization.md`**

涵盖的主题：
- 电路图（文本、matplotlib、LaTeX）
- 结果直方图
- 量子态可视化（布洛赫球、州城市、QSphere）
- 后端拓扑和错误图
- 自定义和样式
- 保存出版质量的数据

### 6. 硬件后端
用于在模拟器和真实量子计算机上运行：
- **参见`references/backends.md`**

涵盖的主题：
- IBM Quantum 后端和身份验证
- 后端属性和状态
- 使用运行时原语在真实硬件上运行
- 作业管理和排队
- 会话模式（迭代）算法）
- 批处理模式（并行作业）
- 本地模拟器（StatevectorSampler、Aer）
- 第三方提供商（IonQ、Amazon Braket）
- 错误缓解策略

### 7. Qiskit 模式工作流程
用于实施四步量子计算工作流程：
- **参见 `references/patterns.md`**

涵盖的主题：
- **映射**：将问题转换为量子电路
- **优化**：硬件转换
- **执行**：使用原语运行
- **后处理**：提取和分析结果
- 完整的VQE示例
- 会话与批量执行
- 常见工作流程模式

### 8. 量子算法和应用
用于实现特定的量子算法：
- **参见`references/algorithms.md`**

涵盖的主题：
- **优化**：VQE、QAOA、Grover 算法
- **化学**：分子基态、激发态、哈密顿量
- **机器学习**：量子内核、VQC、QNN
- **算法库**：Qiskit Nature、Qiskit ML、Qiskit 优化
- 物理模拟和基准测试

## 工作流程决策指南

* *如果您需要：**

- 安装 Qiskit 或设置 IBM 量子帐户 → `references/setup.md`
- 构建新的量子电路 → `references/circuits.md`
- 了解门和电路操作 → `references/circuits.md`
- 运行电路并获取测量结果 → `references/primitives.md`
- 计算期望值 → `references/primitives.md`
- 针对硬件优化电路 → `references/transpilation.md`
- 可视化电路或结果 → `references/visualization.md`
- 在 IBM Quantum 硬件上执行 → `references/backends.md`
- 连接第三方提供商 → `references/backends.md`
- 实施端到端量子工作流程 → `references/patterns.md`
- 构建特定算法（VQE、QAOA 等） → `references/algorithms.md`
- 解决化学或优化问题→ `references/algorithms.md`

## 最佳实践

### 开发工作流程

1. **从模拟器开始**：使用硬件之前在本地进行测试
 ```python
 from qiskit.primitives import StatevectorSampler
 Sampler = StatevectorSampler()
 ```

2. **始终编译**：在执行前优化电路
 ```python
 from qiskit import transpile
 qc_optimized = transpile(qc, backend=backend, optimization_level=3)
 ```

3. **使用适当的基元**：
  - 位串采样器（优化算法）
  - 期望值估计器（化学、物理）

4. **选择执行模式**：
  - 会话：迭代算法（VQE、QAOA）
  - 批量：独立并行作业
  - 单个作业：一次性实验

### 性能优化

- 使用 optimization_level=3 进行生产
- 最小化两个量子位门（主要错误）源）
- 在硬件之前使用噪声模拟器进行测试
- 保存并重用转译电路
- 监视变分算法的收敛

### 硬件执行

- 提交前检查后端状态
- 使用least_busy()进行测试
- 保存作业ID 以供以后使用检索
- 应用错误缓解（弹性_级别）
- 从更少的镜头开始，增加最终运行

## 常见模式

### 模式1：简单电路执行

```python
from qiskit import QuantumCircuit, transpile
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
```

### 模式2：硬件执行转译

```python
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit import transpile

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

qc_optimized = transpile(qc, backend=backend, optimization_level=3)

sampler = Sampler(backend)
job = sampler.run([qc_optimized], shots=1024)
result = job.result()
```

### 模式 3：变分算法 (VQE)

```python
from qiskit_ibm_runtime import Session, EstimatorV2 as Estimator
from scipy.optimize import minimize

with Session(backend=backend) as session:
    estimator = Estimator(session=session)

    def cost_function(params):
        bound_qc = ansatz.assign_parameters(params)
        qc_isa = transpile(bound_qc, backend=backend)
        result = estimator.run([(qc_isa, hamiltonian)]).result()
        return result[0].data.evs

    result = minimize(cost_function, initial_params, method='COBYLA')
```

## 其他资源

- **官方文档**：https://quantum.ibm.com/docs
- **Qiskit 教科书**：https://qiskit.org/learn
- **API 参考**：https://docs.quantum.ibm.com/api/qiskit
- **模式指南**：https://quantum.cloud.ibm.com/docs/en/guides/intro-to-patterns
