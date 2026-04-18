# Pymoo 约束和决策参考

pymoo.

## 约束处理和多标准决策参考

### 定义约束

约束在问题中指定定义：

```python
from pymoo.core.problem import ElementwiseProblem
import numpy as np

class ConstrainedProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=2,    # Number of inequality constraints
            n_eq_constr=1,      # Number of equality constraints
            xl=np.array([0, 0]),
            xu=np.array([5, 5])
        )

    def _evaluate(self, x, out, *args, **kwargs):
        # Objectives
        f1 = x[0]**2 + x[1]**2
        f2 = (x[0]-1)**2 + (x[1]-1)**2

        out["F"] = [f1, f2]

        # Inequality constraints (formulated as g(x) <= 0)
        g1 = x[0] + x[1] - 5  # x[0] + x[1] >= 5 → -(x[0] + x[1] - 5) <= 0
        g2 = x[0]**2 + x[1]**2 - 25  # x[0]^2 + x[1]^2 <= 25

        out["G"] = [g1, g2]

        # Equality constraints (formulated as h(x) = 0)
        h1 = x[0] - 2*x[1]

        out["H"] = [h1]
```

* *约束制定规则：**
- 不等式：`g(x) <= 0`（负数或零时可行）
- 等式：`h(x) = 0`（零时可行）
- 将 `g(x) >= 0` 转换为`-g(x) <= 0`

### 约束处理技术

#### 1. 可行性优先（默认）
* *机制：** 总是优先考虑可行而不是不可行的解决方案
* *比较：**
1. 两者都可行→按客观值比较
2. 一种可行，一种不可行→可行胜
3. 两者都不可行→按约束违规进行比较

* *用法：**
```python
from pymoo.algorithms.moo.nsga2 import NSGA2

# Feasibility first is default for most algorithms
algorithm = NSGA2(pop_size=100)
```

* *优点：**
- 适用于任何基于排序的算法
- 简单有效
- 无参数调优

* *缺点：**
- 可能会遇到小的可行区域
- 可以忽略好的不可行解决方案

#### 2. 惩罚方法
* *机制：** 基于约束违规对目标添加惩罚
* *公式：** `F_penalized = F + penalty_factor * violation`

* *用法：**
```python
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.constraints.as_penalty import ConstraintsAsPenalty

# Wrap problem with penalty
problem_with_penalty = ConstraintsAsPenalty(problem, penalty=1e6)

algorithm = GA(pop_size=100)
```

* *参数：**
- `penalty`：惩罚系数（根据问题规模调整）

* *优点：**
- 转换约束为无约束问题
- 适用于任何优化算法

* *缺点：**
- 惩罚参数敏感
- 可能需要针对特定问题进行调整

#### 3. 约束为目标
* *机制：** 将约束违规视为附加Objective
* *结果：** M+1个目标的多目标问题（M原始+约束）

* *用法：**
```python
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.constraints.as_obj import ConstraintsAsObjective

# Add constraint violation as objective
problem_with_cv_obj = ConstraintsAsObjective(problem)

algorithm = NSGA2(pop_size=100)
```

* *优点：**
- 无需参数调整
- 维护可能的不可行解有用的
- 当可行区域很小时效果很好

* *缺点：**
- 增加问题维度
- 更复杂的Pareto前沿分析

#### 4. Epsilon-约束处理
* *机制：**动态可行性阈值
* *概念：**逐渐收紧约束容差世代

* *优点：**
- 平滑过渡到可行区域
- 有助于解决困难的约束景观

* *缺点：**
- 特定于算法的实现
- 需要参数调整

#### 5.修复算子
* *机制：**修改不可行解以满足约束
* *应用：**交叉/变异后，修复后代

* *用法：**
```python
from pymoo.core.repair import Repair

class MyRepair(Repair):
    def _do(self, problem, X, **kwargs):
        # Project X onto feasible region
        # Example: clip to bounds
        X = np.clip(X, problem.xl, problem.xu)
        return X

from pymoo.algorithms.soo.nonconvex.ga import GA

algorithm = GA(pop_size=100, repair=MyRepair())
```

* *优点：**
- 自始至终保持可行性优化
- 可以编码领域知识

* *缺点：**
- 需要针对特定问题实现
- 可能限制搜索

### 约束处理算法

一些算法具有内置约束处理：

#### SRES（随机）排名进化策略）
* *用途：**单目标约束优化
* *机制：**随机排名平衡目标和约束

* *用法：**
```python
from pymoo.algorithms.soo.nonconvex.sres import SRES

algorithm = SRES()
```

#### ISRES（改进） SRES)
* *用途：**增强约束优化
* *改进：**更好的参数自适应

* *用法：**
```python
from pymoo.algorithms.soo.nonconvex.isres import ISRES

algorithm = ISRES()
```

### 约束处理指南

* *基于选择技术上：**

|问题特征|推荐技术 |
|------------------------------------|------------------------|
|大可行域|可行性第一|
|小可行域|约束为目标，修复|
|严重受限| SRES/ISRES，Epsilon 约束 |
|线性约束 |修复（投影）|
|非线性约束|可行性第一，惩罚|
|已知可行的解决方案|有偏初始化 |

## 多标准决策 (MCDM)

获得帕累托前沿后，MCDM帮助选择首选解决方案。

### 决策背景

* *帕累托前沿特征：**
- 多个非支配解决方案
- 每个代表不同的权衡
- 没有客观的“最佳”解决方案
- 需要决策者偏好

### Pymoo中的MCDM方法

#### 1.伪权重
* *概念：**对每个目标进行加权，选择最小化加权和的解决方案
* *公式：** `score = w1*f1 + w2*f2 + ... + wM*fM`

* *用法：**
```python
from pymoo.mcdm.pseudo_weights import PseudoWeights

# Define weights (must sum to 1)
weights = np.array([0.3, 0.7])  # 30% weight on f1, 70% on f2

dm = PseudoWeights(weights)
best_idx = dm.do(result.F)
best_solution = result.X[best_idx]
```

* *何时使用：**
- 提供明确的偏好表达
- 可通约的目标
- 线性权衡可接受的

* *限制：**
- 需要权重规范
- 线性假设可能无法捕获偏好
- 对目标缩放敏感

#### 2.妥协编程
* *概念：**选择最接近理想点的解决方案
* *度量：**到理想点的距离（例如，欧几里德、切比雪夫）

* *用法：**
```python
from pymoo.mcdm.compromise_programming import CompromiseProgramming

dm = CompromiseProgramming()
best_idx = dm.do(result.F, ideal=ideal_point, nadir=nadir_point)
```

* *何时使用：**
- 已知或可估计的理想目标值
- 平衡考虑所有目标
- 没有明确的权重偏好

#### 3.交互式决策
* *概念：**迭代偏好细化
* *过程：**
1. 向决策者
2展示代表性解决方案。收集有关偏好的反馈
3. 重点搜索首选区域
4. 重复直到找到满意的解决方案

* *方法：**
- 参考点方法
- 权衡分析
- 渐进偏好表达

### 决策工作流程

* *步骤1：标准化目标**
```python
# Normalize to [0, 1] for fair comparison
F_norm = (result.F - result.F.min(axis=0)) / (result.F.max(axis=0) - result.F.min(axis=0))
```

* *步骤 2：分析权衡**
```python
from pymoo.visualization.scatter import Scatter

plot = Scatter()
plot.add(result.F)
plot.show()

# Identify knee points, extreme solutions
```

* *步骤 3：应用 MCDM 方法**
```python
from pymoo.mcdm.pseudo_weights import PseudoWeights

weights = np.array([0.4, 0.6])  # Based on preferences
dm = PseudoWeights(weights)
selected = dm.do(F_norm)
```

* *步骤 4：验证选择**
```python
# Visualize selected solution
from pymoo.visualization.petal import Petal

plot = Petal()
plot.add(result.F[selected], label="Selected")
# Add other candidates for comparison
plot.show()
```

### 高级 MCDM 技术

#### 拐点检测
* *概念：** 一个目标的微小改进导致其他目标大幅下降的解决方案

* *用法：**
```python
from pymoo.mcdm.knee import KneePoint

km = KneePoint()
knee_idx = km.do(result.F)
knee_solutions = result.X[knee_idx]
```

* *何时使用：**
- 没有明确的偏好
- 所需的平衡权衡
- 凸帕累托前沿

#### 超体积贡献
* *概念：**选择对以下方面贡献最大的解决方案hypervolume
* *用例：**维护解决方案的不同子集

* *用法：**
```python
from pymoo.indicators.hv import HV

hv = HV(ref_point=reference_point)
hv_contributions = hv.calc_contributions(result.F)

# Select top contributors
top_k = 5
top_indices = np.argsort(hv_contributions)[-top_k:]
selected_solutions = result.X[top_indices]
```

### 决策指南

* *当决策者有：**

|偏好信息 |推荐方法|
|------------------------------------|--------------------|
|明确的目标权重|伪权重|
|理想目标值|妥协编程|
|没有优先偏好 |拐点，目视检查|
|相互矛盾的标准 |互动方式|
|需要不同的子集 | Hypervolume 贡献 |

* *最佳实践：**
1. **在 MCDM
2 之前标准化目标**。 **可视化帕累托前沿**以了解权衡
3. **考虑多种方法**进行稳健选择
4. **与领域专家
5 验证结果**。 **文件假设**和偏好来源
6. **对权重/参数执行敏感性分析**

### 集成示例

包含约束处理和决策的完整工作流程：

```python
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.mcdm.pseudo_weights import PseudoWeights
import numpy as np

# Define constrained problem
problem = MyConstrainedProblem()

# Setup algorithm with feasibility-first constraint handling
algorithm = NSGA2(
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

# Filter feasible solutions only
feasible_mask = result.CV[:, 0] == 0  # Constraint violation = 0
F_feasible = result.F[feasible_mask]
X_feasible = result.X[feasible_mask]

# Normalize objectives
F_norm = (F_feasible - F_feasible.min(axis=0)) / (F_feasible.max(axis=0) - F_feasible.min(axis=0))

# Apply MCDM
weights = np.array([0.5, 0.5])
dm = PseudoWeights(weights)
best_idx = dm.do(F_norm)

# Get final solution
best_solution = X_feasible[best_idx]
best_objectives = F_feasible[best_idx]

print(f"Selected solution: {best_solution}")
print(f"Objective values: {best_objectives}")
```
