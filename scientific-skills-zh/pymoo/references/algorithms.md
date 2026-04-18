# Pymoo 算法参考

pymoo.

## 单目标优化算法

### 遗传算法(GA)
* *用途：**通用单目标进化优化
* *最适合：**连续、离散或混合变量问题
* *算法类型：**（μ+λ）遗传算法

* *关键参数：**
- `pop_size`：种群大小（默认：100）
- `sampling`：初始种群生成策略
- `selection`：父选择机制（默认：锦标赛）
- `crossover`：重组算子（默认：SBX）
- `mutation`：变分算子（默认：多项式）
- `eliminate_duplicates`：删除冗余解（默认：True）
- `n_offsprings`：每代后代

* *用法：**
```python
from pymoo.algorithms.soo.nonconvex.ga import GA
algorithm = GA(pop_size=100, eliminate_duplicates=True)
```

### 差分进化（DE）
* *用途：**单目标连续优化
* *最适合：**具有良好全局性的连续参数优化搜索
* *算法类型：**基于群体的差分进化

* *变体：**提供多种DE策略（rand/1/bin、best/1/bin等）

### 粒子群优化（PSO）
* *用途：**通过群体智能进行单目标优化
* *Best用于：**连续问题，平滑景观上的快速收敛

### CMA-ES
* *目的：**协方差矩阵适应进化策略
* *最适合：**连续优化，特别是对于噪声或病态问题

### 模式搜索
* *目的：**直接搜索方法
* *最适合：**梯度信息不可用的问题

### Nelder-Mead
* *目的：**基于单纯形的优化
* *最适合：**连续函数的局部优化

## 多目标优化算法

### NSGA-II（非支配排序遗传算法II）
* *用途：**具有2-3个目标的多目标优化
* *最适合：**需要良好分布的Pareto前沿的双目标和三目标问题
* *选择策略：**非支配排序+拥挤距离

* *关键特征：**
- 快速非支配排序
- 多样性的拥挤距离
- 精英方法
- 二元锦标赛交配选择

* *关键参数：**
- `pop_size`：种群规模（默认：100）
- `sampling`：初始种群策略
- `crossover`：连续的默认SBX
- `mutation`：默认多项式变异
- `survival`： RankAndCrowding

* *用法：**
```python
from pymoo.algorithms.moo.nsga2 import NSGA2
algorithm = NSGA2(pop_size=100)
```

* *何时使用：**
- 2-3 个目标
- 需要跨 Pareto 前沿的分布式解决方案
- 标准多目标基准

### NSGA-III
* *用途：**多目标优化（4个以上目标）
* *最适合：**需要统一帕累托前沿覆盖的4个或更多目标的问题
* *选择策略：**基于参考方向的多样性维护

* *主要特点：**
- 参考方向引导群体
- 保持高维目标空间的多样性
- 通过参考点保留利基
- 代表性不足的参考方向选择

* *关键参数：**
- `ref_dirs`：参考方向（必需）
- `pop_size`：默认为参考数量方向
- `crossover`：默认 SBX
- `mutation`：默认多项式变异

* *用法：**
```python
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.util.ref_dirs import get_reference_directions

ref_dirs = get_reference_directions("das-dennis", n_dim=4, n_partitions=12)
algorithm = NSGA3(ref_dirs=ref_dirs)
```

* *NSGA-II 与 NSGA-III：**
- 将 NSGA-II 用于 2-3 个目标
- 将 NSGA-III 用于 4 个以上目标
- NSGA-III 提供更均匀的分布
- NSGA-II 具有较低的计算开销

### R-NSGA-II（基于参考点的 NSGA-II）
* *目的：** 带偏好表达的多目标优化
* *最适合：** 当决策者有 Pareto 前沿的首选区域

### U-NSGA-III（统一 NSGA-III）
* *目的：** 改进版本处理各种场景
* *最适合：**具有额外鲁棒性的多目标问题

### MOEA/D（基于分解的多目标进化算法）
* *用途：**基于分解的多目标优化
* *最适合：**分解为标量子问题的问题effective

### AGE-MOEA
* *用途：**自适应几何估计
* *最适合：**具有自适应机制的多目标和多目标问题

### RVEA（参考向量引导进化算法）
* *用途：**基于参考向量的多目标优化
* *最适合：**具有自适应参考向量的多目标问题

### SMS-EMOA
* *目的：** S-度量选择进化多目标算法
* *最适合：**超体积指标至关重要的问题
* *选择：**使用主导超体积贡献

## 动态多目标算法

### D-NSGA-II
* *目的：**动态多目标问题
* *最适合：**时变目标函数或约束

### KGB-DMOEA
* *目的：**知识引导的动态多目标优化
* *最适合：**利用历史信息的动态问题

## 约束优化

### SRES（随机排名进化策略）
* *用途：**单目标约束优化
* *最适合：**强约束问题

### ISRES（改进的SRES）
* *目的：**增强约束优化
* *最适合：**复杂约束景观

## 算法选择指南

* *对于单目标问题：**
- 从 GA 开始解决一般问题
- 使用 DE 进行连续优化
- 尝试 PSO 来在平滑问题上更快收敛
- 使用 CMA-ES 来解决困难/嘈杂的景观

* *对于多目标问题：**
- 2-3 个目标： NSGA-II
- 4+ 目标：NSGA-III
- 优先接合：R-NSGA-II
- 分解友好：MOEA/D
- 超体积焦点：SMS-EMOA

* *对于受限问题：**
- 基于可行性的生存选择（适用于大多数算法）
- 重约束：SRES/ISRES
- 算法兼容性的惩罚方法

* *对于动态问题：**
- 时变：D-NSGA-II
- 历史知识有用：KGB-DMOEA
