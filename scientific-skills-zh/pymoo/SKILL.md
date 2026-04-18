---
name: pymoo
description: 多目标优化框架。 NSGA-II、NSGA-III、MOEA/D、帕累托前沿、约束处理、基准（ZDT、DTLZ），用于工程设计和优化问题。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# Pymoo - Python 中的多目标优化

## 概述

Pymoo 是一个全面的 Python 优化框架，重点关注多目标问题。使用最先进的算法（NSGA-II/III、MOEA/D）、基准问题（ZDT、DTLZ）、可定制的遗传算子和多标准决策方法来解决单目标和多目标优化。擅长为目标冲突的问题找到权衡解决方案（帕累托前沿）。

## 何时使用此技能

此技能应在以下情况下使用：
- 解决具有一个或多个目标的优化问题
- 查找帕累托最优解决方案并分析权衡
- 实施进化算法（GA、DE、PSO、 NSGA-II/III)
- 处理约束优化问题
- 标准测试问题的基准测试算法（ZDT、DTLZ、WFG）
- 定制遗传算子（交叉、变异、选择）
- 可视化高维优化结果
- 从多个竞争中做出决策解决方案
- 处理二元、离散、连续或混合变量问题

## 核心概念

### 统一接口

Pymoo对所有优化任务使用一致的`minimize()`函数：

```python
from pymoo.optimize import minimize

result = minimize(
    problem,        # What to optimize
    algorithm,      # How to optimize
    termination,    # When to stop
    seed=1,
    verbose=True
)
```

* *结果对象包含：**
- `result.X`：最优解的决策变量 
- `result.F`：最优解的目标值 
- `result.G`：约束违规（如果有约束） 
- `result.algorithm`：算法对象历史

### 问题类型

* *单目标：**一个目标最小化/最大化
* *多目标：**2-3个相互冲突的目标→帕累托前沿
* *多目标：**4个以上目标→高维帕累托前沿
* *约束：**目标+不等式/等式约束
* *动态：**随时间变化的目标或约束

## 快速启动工作流程

#### 工作流程1：单目标优化

* *何时：** 优化一个目标函数

* *步骤：**
1. 定义或选择问题
2. 选择单目标算法（GA、DE、PSO、CMA-ES）
3. 配置终止条件
4. 运行优化
5. 提取最佳解决方案

* *示例：**
```python
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.problems import get_problem
from pymoo.optimize import minimize

# Built-in problem
problem = get_problem("rastrigin", n_var=10)

# Configure Genetic Algorithm
algorithm = GA(
    pop_size=100,
    eliminate_duplicates=True
)

# Optimize
result = minimize(
    problem,
    algorithm,
    ('n_gen', 200),
    seed=1,
    verbose=True
)

print(f"Best solution: {result.X}")
print(f"Best objective: {result.F[0]}")
```

* *参见：** `scripts/single_objective_example.py` 完整示例

### 工作流程 2：多目标优化（2-3 个目标）

* *何时：** 优化 2-3 个相互冲突的目标，需要帕累托前面

* *算法选择：** NSGA-II（双/三目标标准）

* *步骤：**
1. 定义多目标问题
2. 配置 NSGA-II
3. 运行优化得到Pareto front
4. 可视化权衡
5. 应用决策（可选）

* *示例：**
```python
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

# Bi-objective benchmark problem
problem = get_problem("zdt1")

# NSGA-II algorithm
algorithm = NSGA2(pop_size=100)

# Optimize
result = minimize(problem, algorithm, ('n_gen', 200), seed=1)

# Visualize Pareto front
plot = Scatter()
plot.add(result.F, label="Obtained Front")
plot.add(problem.pareto_front(), label="True Front", alpha=0.3)
plot.show()

print(f"Found {len(result.F)} Pareto-optimal solutions")
```

* *请参阅：** `scripts/multi_objective_example.py` 了解完整示例

### 工作流程 3：多目标优化（4 个以上目标）

* *何时：** 优化 4 个或更多目标目标

* *算法选择：** NSGA-III（为许多目标而设计）

* *关键区别：**必须提供人口指导的参考方向

* *步骤：**
1. 定义多目标问题
2. 生成参考方向
3. 配置 NSGA-III 参考方向 
4. 运行优化
5. 使用并行坐标图进行可视化

* *示例：**
```python
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.visualization.pcp import PCP

# Many-objective problem (5 objectives)
problem = get_problem("dtlz2", n_obj=5)

# Generate reference directions (required for NSGA-III)
ref_dirs = get_reference_directions("das-dennis", n_dim=5, n_partitions=12)

# Configure NSGA-III
algorithm = NSGA3(ref_dirs=ref_dirs)

# Optimize
result = minimize(problem, algorithm, ('n_gen', 300), seed=1)

# Visualize with Parallel Coordinates
plot = PCP(labels=[f"f{i+1}" for i in range(5)])
plot.add(result.F, alpha=0.3)
plot.show()
```

* *请参阅：** `scripts/many_objective_example.py` 了解完整示例

### 工作流程 4：自定义问题定义

* *何时：** 解决特定于域的优化问题

* *步骤：**
1. 扩展`ElementwiseProblem`类
2. 使用问题尺寸和边界 
3 定义 `__init__`。针对目标（和约束）
4 实施 `_evaluate` 方法。与任何算法一起使用

* *无约束示例：**
```python
from pymoo.core.problem import ElementwiseProblem
import numpy as np

class MyProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,              # Number of variables
            n_obj=2,              # Number of objectives
            xl=np.array([0, 0]),  # Lower bounds
            xu=np.array([5, 5])   # Upper bounds
        )

    def _evaluate(self, x, out, *args, **kwargs):
        # Define objectives
        f1 = x[0]**2 + x[1]**2
        f2 = (x[0]-1)**2 + (x[1]-1)**2

        out["F"] = [f1, f2]
```

 * *约束示例：**
```python
class ConstrainedProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=2,        # Inequality constraints
            n_eq_constr=1,         # Equality constraints
            xl=np.array([0, 0]),
            xu=np.array([5, 5])
        )

    def _evaluate(self, x, out, *args, **kwargs):
        # Objectives
        out["F"] = [f1, f2]

        # Inequality constraints (g <= 0)
        out["G"] = [g1, g2]

        # Equality constraints (h = 0)
        out["H"] = [h1]
```

 * *约束制定规则：**
- 不等式：表示为 `g(x) <= 0`（当 ≤ 时可行） 0)
- 相等：表示为 `h(x) = 0`（= 0 时可行）
- 将 `g(x) >= b` 转换为 `-(g(x) - b) <= 0`

* *参见：** `scripts/custom_problem_example.py` 完整示例

### 工作流程 5：约束处理

* *何时：**问题具有可行性约束

* *方法选项：**

* *1。可行性第一（默认 - 推荐）**
```python
from pymoo.algorithms.moo.nsga2 import NSGA2

# Works automatically with constrained problems
algorithm = NSGA2(pop_size=100)
result = minimize(problem, algorithm, termination)

# Check feasibility
feasible = result.CV[:, 0] == 0  # CV = constraint violation
print(f"Feasible solutions: {np.sum(feasible)}")
```

* *2。处罚方法**
```python
from pymoo.constraints.as_penalty import ConstraintsAsPenalty

# Wrap problem to convert constraints to penalties
problem_penalized = ConstraintsAsPenalty(problem, penalty=1e6)
```

* *3.约束为目标**
```python
from pymoo.constraints.as_obj import ConstraintsAsObjective

# Treat constraint violation as additional objective
problem_with_cv = ConstraintsAsObjective(problem)
```

* *4。专业算法**
```python
from pymoo.algorithms.soo.nonconvex.sres import SRES

# SRES has built-in constraint handling
algorithm = SRES()
```

* *参见：** `references/constraints_mcdm.md` 全面约束处理指南

### 工作流程6：从帕累托前沿决策

* *何时：** 有帕累托前沿，需要选择首选解决方案

* *步骤：**
1. 运行多目标优化
2. 将目标标准化为 [0, 1]
3. 定义偏好权重
4. 应用MCDM方法
5. 可视化选定的解决方案

* *使用伪权重的示例：**
```python
from pymoo.mcdm.pseudo_weights import PseudoWeights
import numpy as np

# After obtaining result from multi-objective optimization
# Normalize objectives
F_norm = (result.F - result.F.min(axis=0)) / (result.F.max(axis=0) - result.F.min(axis=0))

# Define preferences (must sum to 1)
weights = np.array([0.3, 0.7])  # 30% f1, 70% f2

# Apply decision making
dm = PseudoWeights(weights)
selected_idx = dm.do(F_norm)

# Get selected solution
best_solution = result.X[selected_idx]
best_objectives = result.F[selected_idx]

print(f"Selected solution: {best_solution}")
print(f"Objective values: {best_objectives}")
```

* *其他MCDM方法：**
- 折衷编程：选择最接近理想点
- 拐点：找到平衡的权衡解决方案
- 超体积贡献：选择最多样化的子集

* *参见：**
- `scripts/decision_making_example.py` 了解完整示例
- `references/constraints_mcdm.md` 了解详细的 MCDM 方法

### 工作流程 7：可视化

* *根据数量选择可视化目标：**

* *2 个目标：散点图**
```python
from pymoo.visualization.scatter import Scatter

plot = Scatter(title="Bi-objective Results")
plot.add(result.F, color="blue", alpha=0.7)
plot.show()
```

* *3 个目标：3D 散点图**
```python
plot = Scatter(title="Tri-objective Results")
plot.add(result.F)  # Automatically renders in 3D
plot.show()
```

* *4+ 个目标：平行坐标绘图**
```python
from pymoo.visualization.pcp import PCP

plot = PCP(
    labels=[f"f{i+1}" for i in range(n_obj)],
    normalize_each_axis=True
)
plot.add(result.F, alpha=0.3)
plot.show()
```

* *解决方案比较：花瓣图**
```python
from pymoo.visualization.petal import Petal

plot = Petal(
    bounds=[result.F.min(axis=0), result.F.max(axis=0)],
    labels=["Cost", "Weight", "Efficiency"]
)
plot.add(solution_A, label="Design A")
plot.add(solution_B, label="Design B")
plot.show()
```

* *参见：** `references/visualization.md` 了解所有可视化类型和用法

## 算法选择指南

### 单目标问题

|算法|最适合 |主要特性|
|---------|----------|-------------|
| **GA** |通用|灵活、可定制的运算符|
| **德国** |持续优化|好全局搜索|
| **粒子群算法** |流畅的风景|快速收敛|
| **CMA-ES** |困难/吵闹的问题|自适应 |

### 多目标问题（2-3个目标）

|算法|最适合 |主要特点|
|---------|----------|-------------|
| **NSGA-II** |标准基准|快速、可靠、经过充分测试 |
| **R-NSGA-II** |偏好地区 |参考点引导|
| **经济部/D** |可分解问题|标量化方法 |

### 多目标问题（4 个以上目标）

|算法|最适合 |主要特点|
|---------|----------|-------------|
| **NSGA-III** | 4-15 个目标 |基于参考方向|
| **RVEA** |自适应搜索 |参考向量演化|
| **年龄-MOEA** |复杂的景观|自适应几何 |

### 约束问题

|方法|算法|何时使用 |
|---------|------------|------------|
|可行性第一 |任何算法 |大可行区域|
|专业| SRES、ISRES |重约束|
|处罚| GA + 惩罚 |算法兼容性 |

* *参见：** `references/algorithms.md` 全面算法参考

## 基准问题

### 快速问题访问：
```python
from pymoo.problems import get_problem

# Single-objective
problem = get_problem("rastrigin", n_var=10)
problem = get_problem("rosenbrock", n_var=10)

# Multi-objective
problem = get_problem("zdt1")        # Convex front
problem = get_problem("zdt2")        # Non-convex front
problem = get_problem("zdt3")        # Disconnected front

# Many-objective
problem = get_problem("dtlz2", n_obj=5, n_var=12)
problem = get_problem("dtlz7", n_obj=4)
```

* *参见：** `references/problems.md` 完整测试问题参考

## 遗传算子定制

### 标准算子配置：
```python
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM

algorithm = GA(
    pop_size=100,
    crossover=SBX(prob=0.9, eta=15),
    mutation=PM(eta=20),
    eliminate_duplicates=True
)
```

### 按变量类型选择算子：

* *连续变量：**
- 交叉：SBX（模拟二元交叉）
- 突变：PM（多项式突变）

* *二元变量：**
- 交叉：TwoPointCrossover、UniformCrossover
- 突变：BitflipMutation

* *排列（TSP、调度）：**
- 交叉：OrderCrossover (OX)
- 突变：InversionMutation

* *请参阅：** `references/operators.md` 获取全面的操作参考

## 性能和故障排除

### 常见问题和解决方案：

* *问题：算法不收敛**
- 增加种群规模
- 增加代数
- 检查问题是否是多峰的（尝试不同的算法）
- 验证约束是否正确制定

* *问题：帕累托前沿分布较差**
- 对于NSGA-III：调整参考方向
- 增加人口规模
- 检查重复消除
- 验证问题缩放

* *问题：几乎没有可行的解决方案**
- 使用约束作为目标方法
- 应用修复运算符
- 尝试SRES/ISRES进行约束问题
- 检查约束公式（应为 g <= 0）

* *问题：高计算成本**
- 减少种群大小
- 减少生成数
- 使用更简单的运算符
- 启用并行化（如果问题支持）

### 最佳做法：

1. **当尺度差异显着时，标准化目标**
2. **设置随机种子**以实现再现性
3. **保存历史记录**以分析收敛性：`save_history=True`
4. **可视化结果**以了解解决方案质量
5. **与真正的帕累托前沿相比**（可用时）
6. **使用适当的终止标准**（代数、评估、公差）
7. **针对问题特征调整算子参数**

## 资源

该技能包括全面的参考文档和可执行示例：

### 参考文献/
深入理解的详细文档：

- **algorithms.md**：包含参数、用法和选择指南的完整算法参考
- **problems.md**：具有特征的基准测试问题（ZDT、DTLZ、WFG）
- **operators.md**：具有配置的遗传算子（采样、选择、交叉、突变）
- **visualization.md**：带有示例和选择的所有可视化类型指南
- **constraints_mcdm.md**：约束处理技术和多准则决策方法

* *参考搜索模式：**
- 算法详细信息： `grep -r "NSGA-II\|NSGA-III\|MOEA/D" references/`
- 约束方法： `grep -r "Feasibility First\|Penalty\|Repair" references/`
- 可视化类型： `grep -r "Scatter\|PCP\|Petal" references/`

### 脚本/
演示常见工作流程的可执行示例：

- **single_objective_example.py**：使用GA
进行基本单目标优化- **multi_objective_example.py**：使用NSGA-II进行多目标优化，可视化
- **many_objective_example.py**：使用NSGA-III进行多目标优化，参考方向
- **custom_problem_example.py**：定义自定义问题（约束和无约束）
- **decision_making_example.py**：具有不同偏好的多标准决策

* *运行示例：**
```bash
python3 scripts/single_objective_example.py
python3 scripts/multi_objective_example.py
python3 scripts/many_objective_example.py
python3 scripts/custom_problem_example.py
python3 scripts/decision_making_example.py
```

## 附加说明

* *安装：**
```bash
uv pip install pymoo
```

* *依赖项：** NumPy、SciPy、matplotlib、autograd（对于基于梯度）

* *文档：** https://pymoo.org/

* *版本：** 该技能基于 pymoo 0.6.x

* *常见模式：**
- 始终使用 `ElementwiseProblem` 解决自定义问题
- 约束公式为`g(x) <= 0` 和 `h(x) = 0`
  - NSGA-III
 所需的参考方向 - 在 MCDM
 之前标准化目标 - 使用适当的终端：`('n_gen', N)` 或 `get_termination("f_tol", tol=0.001)`
