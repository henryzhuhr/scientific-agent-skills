# Qiskit设置和安装

## 安装

使用uv安装Qiskit：

```bash
uv pip install qiskit
```

用于可视化功能：

```bash
uv pip install "qiskit[visualization]" matplotlib
```

## Python环境设置

创建并激活虚拟环境隔离依赖关系：

```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

## 支持的Python版本

检查[Qiskit PyPI页面](https://pypi.org/project/qiskit/)当前支持的Python版本。截至 2025 年，Qiskit 通常支持 Python 3.8+。

## IBM Quantum 帐户设置

要在真正的 IBM Quantum 硬件上运行电路，您需要一个 IBM Quantum 帐户和 API 令牌。

### 创建帐户

1. 访问[IBM 量子平台](https://quantum.ibm.com/)
2. 注册一个免费帐户
3. 导航到您的帐户设置以检索 API 令牌

### 配置身份验证

保存您的 IBM Quantum 凭证：

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Save credentials (first time only)
QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token="YOUR_IBM_QUANTUM_TOKEN"
)

# Later sessions - load saved credentials
service = QiskitRuntimeService()
```

### 环境变量方法

或者，将 API 令牌设置为环境变量：

```bash
export QISKIT_IBM_TOKEN="YOUR_IBM_QUANTUM_TOKEN"
```

## 本地开发（无需帐户）

您可以使用模拟器在本地构建和测试量子电路，而无需 IBM Quantum 帐户：

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Run locally with simulator
sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
```

## 验证安装

测试您的安装方式：

```python
import qiskit
print(qiskit.__version__)

from qiskit import QuantumCircuit
qc = QuantumCircuit(2)
print("Qiskit installed successfully!")
```
