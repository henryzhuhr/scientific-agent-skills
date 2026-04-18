---
name: sympy
description: 在 Python 中处理符号数学时可以使用此技能。该技能应用于符号计算任务，包括代数求解方程、执行微积分运算（导数、积分、极限）、操作代数表达式、符号处理矩阵、物理计算、数论问题、几何计算以及从数学表达式生成可执行代码。当用户需要精确的符号结果而不是数值近似值时，或者在使用包含变量和参数的数学公式时，可以应用此技能。
license: https://github.com/sympy/sympy/blob/master/LICENSE
metadata:
    skill-author: K-Dense Inc.
---

# SymPy - Python 中的符号数学

## 概述

SymPy 是一个用于符号数学的 Python 库，它可以使用数学符号而不是数值近似进行精确计算。此技能为使用 SymPy 执行符号代数、微积分、线性代数、方程求解、物理计算和代码生成提供全面指导。

## 何时使用此技能

在以下情况下使用此技能：
- 以符号方式求解方程（代数、微分、方程组）
- 执行微积分运算（导数、积分、极限、级数）
- 操作和简化代数表达式
- 象征性地处理矩阵和线性代数
- 进行物理计算（力学、量子力学、矢量分析）
- 数论计算（素数、因式分解、模算术）
- 几何计算（2D/3D 几何、解析几何）
- 将数学表达式转换为可执行代码（Python、C、Fortran）
- 生成 LaTeX 或其他格式的数学输出
- 需要精确的数学结果（例如，`sqrt(2)` 而不是 `1.414...`）

## 核心功能

### 1.符号计算基础

* *创建符号和表达式：**
```python
from sympy import symbols, Symbol
x, y, z = symbols('x y z')
expr = x**2 + 2*x + 1

# With assumptions
x = symbols('x', real=True, positive=True)
n = symbols('n', integer=True)
```

* *简化和操作：**
```python
from sympy import simplify, expand, factor, cancel
simplify(sin(x)**2 + cos(x)**2)  # Returns 1
expand((x + 1)**3)  # x**3 + 3*x**2 + 3*x + 1
factor(x**2 - 1)    # (x - 1)*(x + 1)
```

* *详细基础知识：**参见`references/core-capabilities.md`

### 2. 微积分

* *导数：**
```python
from sympy import diff
diff(x**2, x)        # 2*x
diff(x**4, x, 3)     # 24*x (third derivative)
diff(x**2*y**3, x, y)  # 6*x*y**2 (partial derivatives)
```

* *积分：**
```python
from sympy import integrate, oo
integrate(x**2, x)              # x**3/3 (indefinite)
integrate(x**2, (x, 0, 1))      # 1/3 (definite)
integrate(exp(-x), (x, 0, oo))  # 1 (improper)
```

* *极限和系列：**
```python
from sympy import limit, series
limit(sin(x)/x, x, 0)  # 1
series(exp(x), x, 0, 6)  # 1 + x + x**2/2 + x**3/6 + x**4/24 + x**5/120 + O(x**6)
```

* *详细微积分运算：**参见`references/core-capabilities.md`

### 3.方程求解

* *代数方程：**
```python
from sympy import solveset, solve, Eq
solveset(x**2 - 4, x)  # {-2, 2}
solve(Eq(x**2, 4), x)  # [-2, 2]
```

* *系统方程组：**
```python
from sympy import linsolve, nonlinsolve
linsolve([x + y - 2, x - y], x, y)  # {(1, 1)} (linear)
nonlinsolve([x**2 + y - 2, x + y**2 - 3], x, y)  # (nonlinear)
```

* *微分方程组：**
```python
from sympy import Function, dsolve, Derivative
f = symbols('f', cls=Function)
dsolve(Derivative(f(x), x) - f(x), f(x))  # Eq(f(x), C1*exp(x))
```

* *详细求解方法：**参见`references/core-capabilities.md`

### 4.矩阵与线性代数

* *矩阵创建和运算：**
```python
from sympy import Matrix, eye, zeros
M = Matrix([[1, 2], [3, 4]])
M_inv = M**-1  # Inverse
M.det()        # Determinant
M.T            # Transpose
```

* *特征值和特征向量：**
```python
eigenvals = M.eigenvals()  # {eigenvalue: multiplicity}
eigenvects = M.eigenvects()  # [(eigenval, mult, [eigenvectors])]
P, D = M.diagonalize()  # M = P*D*P^-1
```

* *求解线性系统：**
```python
A = Matrix([[1, 2], [3, 4]])
b = Matrix([5, 6])
x = A.solve(b)  # Solve Ax = b
```

* *关于综合线性代数：**参见`references/matrices-linear-algebra.md`

### 5.物理与力学

* *经典力学：**
```python
from sympy.physics.mechanics import dynamicsymbols, LagrangesMethod
from sympy import symbols

# Define system
q = dynamicsymbols('q')
m, g, l = symbols('m g l')

# Lagrangian (T - V)
L = m*(l*q.diff())**2/2 - m*g*l*(1 - cos(q))

# Apply Lagrange's method
LM = LagrangesMethod(L, [q])
```

* *矢量分析：**
```python
from sympy.physics.vector import ReferenceFrame, dot, cross
N = ReferenceFrame('N')
v1 = 3*N.x + 4*N.y
v2 = 1*N.x + 2*N.z
dot(v1, v2)  # Dot product
cross(v1, v2)  # Cross product
```

* *量子力学：**
```python
from sympy.physics.quantum import Ket, Bra, Commutator
psi = Ket('psi')
A = Operator('A')
comm = Commutator(A, B).doit()
```

* *详细物理能力：**参见`references/physics-mechanics.md`

### 6.高级数学

该技能包括全面支持：

- **几何：** 2D/3D解析几何、点、线、圆、多边形、变换
- **数论：** 素数、分解、GCD/LCM、模算术、丢番图方程
- **组合学：** 排列、组合、划分、群论
- **逻辑和集合：** 布尔逻辑、集合论、有限和无限集合
- **统计：** 概率分布、随机变量、期望、方差
- **特殊函数：** Gamma、Bessel、正交多项式、超几何函数
- **多项式：** 多项式代数、根、因式分解、Groebner 基

* *详细的高级主题：** 请参阅 `references/advanced-topics.md`

### 7.代码生成与输出

* *转换为可执行函数：**
```python
from sympy import lambdify
import numpy as np

expr = x**2 + 2*x + 1
f = lambdify(x, expr, 'numpy')  # Create NumPy function
x_vals = np.linspace(0, 10, 100)
y_vals = f(x_vals)  # Fast numerical evaluation
```

* *生成C/Fortran代码：**
```python
from sympy.utilities.codegen import codegen
[(c_name, c_code), (h_name, h_header)] = codegen(
    ('my_func', expr), 'C'
)
```

* *LaTeX输出：**
```python
from sympy import latex
latex_str = latex(expr)  # Convert to LaTeX for documents
```

* *用于全面的代码生成：**参见 `references/code-generation-printing.md`

## 使用 SymPy：最佳实践

### 1. 始终定义符号首先

```python
from sympy import symbols
x, y, z = symbols('x y z')
# Now x, y, z can be used in expressions
```

### 2.使用假设可以更好地简化

```python
x = symbols('x', positive=True, real=True)
sqrt(x**2)  # Returns x (not Abs(x)) due to positive assumption
```

常见假设：`real`、`positive`、`negative`、 `integer`、`rational`、`complex`、`even`、`odd`

### 3. 使用精确算术

```python
from sympy import Rational, S
# Correct (exact):
expr = Rational(1, 2) * x
expr = S(1)/2 * x

# Incorrect (floating-point):
expr = 0.5 * x  # Creates approximate value
```

### 4. 数值计算需要

```python
from sympy import pi, sqrt
result = sqrt(8) + pi
result.evalf()    # 5.96371554103586
result.evalf(50)  # 50 digits of precision
```

### 5.转换为NumPy以获得性能

```python
# Slow for many evaluations:
for x_val in range(1000):
    result = expr.subs(x, x_val).evalf()

# Fast:
f = lambdify(x, expr, 'numpy')
results = f(np.arange(1000))
```

### 6. 使用适当的求解器

- `solveset`：代数方程（初级）
- `linsolve`：线性系统
- `nonlinsolve`：非线性系统
- `dsolve`：微分方程
- `solve`：通用（传统，但灵活）

## 参考文件结构

此技能使用不同功能的模块化参考文件：

1. **`core-capabilities.md`**：符号、代数、微积分、简化、方程求解
  - 加载时间：基本符号计算、微积分或求解方程

2. **`matrices-linear-algebra.md`**：矩阵运算、特征值、线性系统
  - 加载时间：处理矩阵或线性代数问题

3. **`physics-mechanics.md`**：经典力学、量子力学、向量、单位
  - 加载时间：物理计算或力学问题

4. **`advanced-topics.md`**：几何、数论、组合学、逻辑、统计
  - 加载时间：基本代数和微积分之外的高级数学主题

5. **`code-generation-printing.md`**：Lambdify、codegen、LaTeX 输出、打印
  - 加载时间：将表达式转换为代码或生成格式化输出

## 常见用例模式

### 模式 1：求解和验证

```python
from sympy import symbols, solve, simplify
x = symbols('x')

# Solve equation
equation = x**2 - 5*x + 6
solutions = solve(equation, x)  # [2, 3]

# Verify solutions
for sol in solutions:
    result = simplify(equation.subs(x, sol))
    assert result == 0
```

### 模式2：符号到数字管道

```python
# 1. Define symbolic problem
x, y = symbols('x y')
expr = sin(x) + cos(y)

# 2. Manipulate symbolically
simplified = simplify(expr)
derivative = diff(simplified, x)

# 3. Convert to numerical function
f = lambdify((x, y), derivative, 'numpy')

# 4. Evaluate numerically
results = f(x_data, y_data)
```

### 模式3：记录数学结果

```python
# Compute result symbolically
integral_expr = Integral(x**2, (x, 0, 1))
result = integral_expr.doit()

# Generate documentation
print(f"LaTeX: {latex(integral_expr)} = {latex(result)}")
print(f"Pretty: {pretty(integral_expr)} = {pretty(result)}")
print(f"Numerical: {result.evalf()}")
```

## 与科学工作流程集成

### 与NumPy

```python
import numpy as np
from sympy import symbols, lambdify

x = symbols('x')
expr = x**2 + 2*x + 1

f = lambdify(x, expr, 'numpy')
x_array = np.linspace(-5, 5, 100)
y_array = f(x_array)
```

### 与 Matplotlib

```python
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, lambdify, sin

x = symbols('x')
expr = sin(x) / x

f = lambdify(x, expr, 'numpy')
x_vals = np.linspace(-10, 10, 1000)
y_vals = f(x_vals)

plt.plot(x_vals, y_vals)
plt.show()
```

### 与 SciPy

```python
from scipy.optimize import fsolve
from sympy import symbols, lambdify

# Define equation symbolically
x = symbols('x')
equation = x**3 - 2*x - 5

# Convert to numerical function
f = lambdify(x, equation, 'numpy')

# Solve numerically with initial guess
solution = fsolve(f, 2)
```

## 快速参考：最常见函数

```python
# Symbols
from sympy import symbols, Symbol
x, y = symbols('x y')

# Basic operations
from sympy import simplify, expand, factor, collect, cancel
from sympy import sqrt, exp, log, sin, cos, tan, pi, E, I, oo

# Calculus
from sympy import diff, integrate, limit, series, Derivative, Integral

# Solving
from sympy import solve, solveset, linsolve, nonlinsolve, dsolve

# Matrices
from sympy import Matrix, eye, zeros, ones, diag

# Logic and sets
from sympy import And, Or, Not, Implies, FiniteSet, Interval, Union

# Output
from sympy import latex, pprint, lambdify, init_printing

# Utilities
from sympy import evalf, N, nsimplify
```

## 入门示例

### 示例 1：求解二次方程
```python
from sympy import symbols, solve, sqrt
x = symbols('x')
solution = solve(x**2 - 5*x + 6, x)
# [2, 3]
```

### 示例 2：计算导数
```python
from sympy import symbols, diff, sin
x = symbols('x')
f = sin(x**2)
df_dx = diff(f, x)
# 2*x*cos(x**2)
```

### 示例 3：计算积分
```python
from sympy import symbols, integrate, exp
x = symbols('x')
integral = integrate(x * exp(-x**2), (x, 0, oo))
# 1/2
```

### 示例 4：矩阵特征值
```python
from sympy import Matrix
M = Matrix([[1, 2], [2, 1]])
eigenvals = M.eigenvals()
# {3: 1, -1: 1}
```

### 示例 5：生成 Python 函数
```python
from sympy import symbols, lambdify
import numpy as np
x = symbols('x')
expr = x**2 + 2*x + 1
f = lambdify(x, expr, 'numpy')
f(np.array([1, 2, 3]))
# array([ 4,  9, 16])
```

## 常见问题故障排除

1. **“NameError：名称'x'未定义”**
  - 解决方案：在使用

2之前始终使用`symbols()`定义符号。 **意外的数值结果**
 - 问题：使用 `0.5` 等浮点数代替 `Rational(1, 2)`
  - 解决方案：使用 `Rational()` 或 `S()` 进行精确算术

3. **循环性能缓慢**
  - 问题：重复使用 `subs()` 和 `evalf()`
  - 解决方案：使用 `lambdify()` 创建快速数值函数 

4. **“无法求解此方程”**
  - 尝试不同的求解器：`solve`、`solveset`、`nsolve`（数值）
  - 检查方程是否可代数求解
  - 如果不存在封闭式解，则使用数值方法

5. **简化未按预期工作**
  - 尝试不同的简化函数：`simplify`、`factor`、`expand`、`trigsimp`
  - 向符号添加假设（例如，`positive=True`）
  - 使用`simplify(expr, force=True)` 用于积极简化

## 其他资源

- 官方文档：https://docs.sympy.org/
- 教程：https://docs.sympy.org/latest/tutorials/intro-tutorial/index.html
- API 参考： https://docs.sympy.org/latest/reference/index.html
- 示例：https://github.com/sympy/sympy/tree/master/examples
