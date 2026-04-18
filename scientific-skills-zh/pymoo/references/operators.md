# Pymoo遗传算子参考

pymoo中遗传算子的综合参考。

## 采样算子

采样算子在优化开始时初始化种群。

### 随机采样
* *用途：**生成随机初始值解决方案
* *类型：**
- `FloatRandomSampling`：连续变量
- `BinaryRandomSampling`：二元变量
- `IntegerRandomSampling`：整数变量
- `PermutationRandomSampling`：基于排列问题

* *用法：**
```python
from pymoo.operators.sampling.rnd import FloatRandomSampling
sampling = FloatRandomSampling()
```

### 拉丁超立方采样（LHS）
* *目的：**空间填充初始群体
* *好处：**比搜索空间更好的覆盖范围random
* *类型：**
- `LHS`：标准拉丁超立方体

* *用法：**
```python
from pymoo.operators.sampling.lhs import LHS
sampling = LHS()
```

### 自定义采样
通过 Population 对象或 NumPy 提供初始总体数组

## 选择算子

选择算子选择父母进行繁殖。

### 锦标赛选择
* *目的：**通过锦标赛比赛选择父母
* *机制：**随机选择k个体，选择最好的
* *参数：**
- `pressure`：锦标赛规模（默认：2）
- `func_comp`：比较函数

* *用法：**
```python
from pymoo.operators.selection.tournament import TournamentSelection
selection = TournamentSelection(pressure=2)
```

### 随机选择
* *用途：**统一随机父代选择
* *用例：**基线或探索型算法

* *用法：**
```python
from pymoo.operators.selection.rnd import RandomSelection
selection = RandomSelection()
```

## 交叉算子

交叉算子重新组合父解决方案以创建后代。

### 对于连续变量

#### 模拟二进制交叉（SBX）
* *用途：**连续优化的主交叉
* *机制：**模拟二进制编码变量的单点交叉
* *参数：**
- `prob`：交叉概率（默认： 0.9)
- `eta`：分布指数（默认：15）
  - 较高的eta→后代更接近父母
  - 较低的eta→更多的探索

* *用法：**
```python
from pymoo.operators.crossover.sbx import SBX
crossover = SBX(prob=0.9, eta=15)
```

* *字符串简写：** `"real_sbx"`

#### 差异进化交叉
* *用途：**DE特异性重组
* *变体：**
- `DE/rand/1/bin`
- `DE/best/1/bin`
- `DE/current-to-best/1/bin`

* *参数：**
- `CR`：交叉率
- `F`：缩放因子

### 对于二元变量

#### 单点交叉
* *用途：**剪切和交换一点
* *用法：**
```python
from pymoo.operators.crossover.pntx import SinglePointCrossover
crossover = SinglePointCrossover()
```

#### 两点交叉
* *用途：**两点之间剪切和交换
* *用法：**
```python
from pymoo.operators.crossover.pntx import TwoPointCrossover
crossover = TwoPointCrossover()
```

#### K 点交叉
* *目的：**多个切割点
* *参数：**
- `n_points`：交叉点的数量

#### 均匀交叉
* *目的：**每个基因独立于任一基因parent
* *参数：**
- `prob`：每基因交换概率（默认：0.5）

* *用途：**
```python
from pymoo.operators.crossover.ux import UniformCrossover
crossover = UniformCrossover(prob=0.5)
```

#### 半均匀交叉（HUX）
* *用途：**交换正好有一半的不同基因
* *好处：**保持遗传多样性

### 对于排列

#### 顺序交叉（OX）
* *目的：**保留父母的相对顺序
* *用例：**旅行推销员，日程安排问题

* *用法：**
```python
from pymoo.operators.crossover.ox import OrderCrossover
crossover = OrderCrossover()
```

#### 边缘重组交叉 (ERX)
* *用途：** 保留来自父级的边缘信息
* *用例：** 边缘连接性很重要的路由问题

#### 部分映射交叉(PMX)
* *目的：**交换片段，同时保持排列有效性

## 变异算子

变异算子引入变异以保持多样性。

### 对于连续变量

#### 多项式变异 (PM)
* *目的：** 连续的初级变异优化
* *机制：**多项式概率分布
* *参数：**
- `prob`：每变量突变概率
- `eta`：分布指数（默认：20）
  - 更高的eta→更小扰动
  - 较低的eta→较大的扰动

* *用法：**
```python
from pymoo.operators.mutation.pm import PM
mutation = PM(prob=None, eta=20)  # prob=None means 1/n_var
```

* *字符串简写：** `"real_pm"`

* *概率指南：**
- `None` 或 `1/n_var`：标准推荐
- 更高用于更多探索
- 降低更多利用

#### 对于二进制变量

#### 位翻转突变
* *目的：** 以指定概率翻转位
* *参数：**
- `prob`：每位翻转概率

* *用法：**
```python
from pymoo.operators.mutation.bitflip import BitflipMutation
mutation = BitflipMutation(prob=0.05)
```

#### 对于整数变量

#### 整数多项式变异
* *目的：**适用于整数的PM
* *确保：**之后的有效整数值突变

### 对于排列

#### 反转突变
* *目的：** 反转排列的一段
* *用例：** 维持某种顺序结构

* *用法：**
```python
from pymoo.operators.mutation.inversion import InversionMutation
mutation = InversionMutation()
```

#### Scramble Mutation
* *用途：**随机打乱一个segment

### Custom Mutation
通过扩展`Mutation`定义自定义mutation类

## 修复运算符

修复运算符修复约束违规或确保解决方案的可行性。

### 舍入修复
* *用途：**舍入到最接近的有效值
* *用例：**具有绑定约束的整数/离散变量

### 反弹修复
* *目的：**将越界值反射回可行区域
* *用例：**盒子约束的连续问题

### 投影修复
* *目的：**将不可行的解决方案投影到可行区域
* *用例：**线性约束

### 自定义修复
* *目的：**特定于域的约束处理
* *实现：**扩展`Repair`类

* *示例：**
```python
from pymoo.core.repair import Repair

class MyRepair(Repair):
    def _do(self, problem, X, **kwargs):
        # Modify X to satisfy constraints
        # Return repaired X
        return X
```

## 算子配置指南

### 参数调优

* *交叉概率：**
- 高（0.8-0.95）：大多数问题的标准
- 较低：更强调突变

* *变异概率：**
- `1/n_var`：标准推荐
- 较高：更多探索，收敛速度较慢
- 较低：收敛速度较快，有过早收敛的风险

* *分布指数（eta）：**
- 交叉eta（15-30）：本地搜索较高
- 突变eta（20-50）：更高的利用

### 针对特定问题的选择

* *连续问题：**
- 交叉：SBX
- 突变：多项式突变
- 选择：锦标赛

* *二进制问题：**
- 交叉：两点或均匀 
- 突变：Bitflip
- 选择：锦标赛

* *排列问题：**
- 交叉：顺序交叉 (OX)
- 突变：反转或Scramble
- 选择：锦标赛

* *混合变量问题：**
- 每个变量类型使用适当的运算符
- 确保运算符兼容性

### 基于字符串的配置

Pymoo 支持方便的基于字符串的运算符规格：

```python
from pymoo.algorithms.soo.nonconvex.ga import GA

algorithm = GA(
    pop_size=100,
    sampling="real_random",
    crossover="real_sbx",
    mutation="real_pm"
)
```

* *可用字符串：**
- 采样：`"real_random"`、`"real_lhs"`、`"bin_random"`、`"perm_random"`
- 分频： `"real_sbx"`、`"real_de"`、`"int_sbx"`、`"bin_ux"`、`"bin_hux"`
- 突变：`"real_pm"`、`"int_pm"`、`"bin_bitflip"`、 `"perm_inv"`

## 运算符组合示例

### 标准连续GA:
```python
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.selection.tournament import TournamentSelection

sampling = FloatRandomSampling()
crossover = SBX(prob=0.9, eta=15)
mutation = PM(eta=20)
selection = TournamentSelection()
```

### 二进制GA:
```python
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation

sampling = BinaryRandomSampling()
crossover = TwoPointCrossover()
mutation = BitflipMutation(prob=0.05)
```

### 排列GA (TSP):
```python
from pymoo.operators.sampling.rnd import PermutationRandomSampling
from pymoo.operators.crossover.ox import OrderCrossover
from pymoo.operators.mutation.inversion import InversionMutation

sampling = PermutationRandomSampling()
crossover = OrderCrossover()
mutation = InversionMutation()
```
