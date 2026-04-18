# SymPy 核心能力

本文档涵盖了SymPy的基本操作：符号计算基础知识、代数、微积分、简化和方程求解。

## 创建符号和基本操作

### 符号创建

* *单符号：**
```python
from sympy import symbols, Symbol
x = Symbol('x')
# or more commonly:
x, y, z = symbols('x y z')
```

* *带有假设：**
```python
x = symbols('x', real=True, positive=True)
n = symbols('n', integer=True)
```

常见假设：`real`、`positive`、`negative`、`integer`、`rational`、 `prime`、`even`、`odd`、`complex`

### 基本算术

SymPy 支持符号表达式的标准 Python 运算符：
- 加法：`x + y`
- 减法： `x - y`
- 乘法：`x * y`
- 除法：`x / y`
- 求幂：`x**y`

* *重要问题：** 使用 `sympy.Rational()` 或`S()` 对于精确有理数：
```python
from sympy import Rational, S
expr = Rational(1, 2) * x  # Correct: exact 1/2
expr = S(1)/2 * x          # Correct: exact 1/2
expr = 0.5 * x             # Creates floating-point approximation
```

### 替换和计算

* *替换值：**
```python
expr = x**2 + 2*x + 1
expr.subs(x, 3)  # Returns 16
expr.subs({x: 2, y: 3})  # Multiple substitutions
```

* *数值评估：**
```python
from sympy import pi, sqrt
expr = sqrt(8)
expr.evalf()      # 2.82842712474619
expr.evalf(20)    # 2.8284271247461900976 (20 digits)
pi.evalf(100)     # 100 digits of pi
```

## Simplification

SymPy 提供了多个简化函数，每个函数都有不同的策略：

### General Simplification

```python
from sympy import simplify, expand, factor, collect, cancel, trigsimp

# General simplification (tries multiple methods)
simplify(sin(x)**2 + cos(x)**2)  # Returns 1

# Expand products and powers
expand((x + 1)**3)  # x**3 + 3*x**2 + 3*x + 1

# Factor polynomials
factor(x**3 - x**2 + x - 1)  # (x - 1)*(x**2 + 1)

# Collect terms by variable
collect(x*y + x - 3 + 2*x**2 - z*x**2 + x**3, x)

# Cancel common factors in rational expressions
cancel((x**2 + 2*x + 1)/(x**2 + x))  # (x + 1)/x
```

### Trigonometric化简

```python
from sympy import sin, cos, tan, trigsimp, expand_trig

# Simplify trig expressions
trigsimp(sin(x)**2 + cos(x)**2)  # 1
trigsimp(sin(x)/cos(x))          # tan(x)

# Expand trig functions
expand_trig(sin(x + y))  # sin(x)*cos(y) + sin(y)*cos(x)
```

### 幂和对数化简

```python
from sympy import powsimp, powdenest, log, expand_log, logcombine

# Simplify powers
powsimp(x**a * x**b)  # x**(a + b)

# Expand logarithms
expand_log(log(x*y))  # log(x) + log(y)

# Combine logarithms
logcombine(log(x) + log(y))  # log(x*y)
```

## 微积分

### 导数

```python
from sympy import diff, Derivative

# First derivative
diff(x**2, x)  # 2*x

# Higher derivatives
diff(x**4, x, x, x)  # 24*x (third derivative)
diff(x**4, x, 3)     # 24*x (same as above)

# Partial derivatives
diff(x**2*y**3, x, y)  # 6*x*y**2

# Unevaluated derivative (for display)
d = Derivative(x**2, x)
d.doit()  # Evaluates to 2*x
```

### 积分

* *不定积分：**
```python
from sympy import integrate

integrate(x**2, x)           # x**3/3
integrate(exp(x)*sin(x), x)  # exp(x)*sin(x)/2 - exp(x)*cos(x)/2
integrate(1/x, x)            # log(x)
```

* *注意：** SymPy 不包括积分常数。如果需要，请手动添加 `+ C`。

* *定积分：**
```python
from sympy import oo, pi, exp, sin

integrate(x**2, (x, 0, 1))    # 1/3
integrate(exp(-x), (x, 0, oo)) # 1
integrate(sin(x), (x, 0, pi))  # 2
```

* *多重积分：**
```python
integrate(x*y, (x, 0, 1), (y, 0, x))  # 1/12
```

* *数值积分（符号时）失败）：**
```python
integrate(x**x, (x, 0, 1)).evalf()  # 0.783430510712134
```

### Limits

```python
from sympy import limit, oo, sin

# Basic limits
limit(sin(x)/x, x, 0)  # 1
limit(1/x, x, oo)      # 0

# One-sided limits
limit(1/x, x, 0, '+')  # oo
limit(1/x, x, 0, '-')  # -oo

# Use limit() for singularities (not subs())
limit((x**2 - 1)/(x - 1), x, 1)  # 2
```

* *重要：**在奇点处使用 `limit()` 而不是 `subs()`，因为无穷大对象不能可靠地跟踪增长rates.

### 系列扩展

```python
from sympy import series, sin, exp, cos

# Taylor series expansion
expr = sin(x)
expr.series(x, 0, 6)  # x - x**3/6 + x**5/120 + O(x**6)

# Expansion around a point
exp(x).series(x, 1, 4)  # Expands around x=1

# Remove O() term
series(exp(x), x, 0, 4).removeO()  # 1 + x + x**2/2 + x**3/6
```

### 有限差分（数值导数）

```python
from sympy import Function, differentiate_finite
f = Function('f')

# Approximate derivative using finite differences
differentiate_finite(f(x), x)
f(x).as_finite_difference()
```

## 方程求解

### 代数方程 -求解器

* *主要函数：** `solveset(equation, variable, domain)`

```python
from sympy import solveset, Eq, S

# Basic solving (assumes equation = 0)
solveset(x**2 - 1, x)  # {-1, 1}
solveset(x**2 + 1, x)  # {-I, I} (complex solutions)

# Using explicit equation
solveset(Eq(x**2, 4), x)  # {-2, 2}

# Specify domain
solveset(x**2 - 1, x, domain=S.Reals)  # {-1, 1}
solveset(x**2 + 1, x, domain=S.Reals)  # EmptySet (no real solutions)
```

 * *返回类型：**有限集、区间或图像集

### 方程组

* *线性系统 - linsolve:**
```python
from sympy import linsolve, Matrix

# From equations
linsolve([x + y - 2, x - y], x, y)  # {(1, 1)}

# From augmented matrix
linsolve(Matrix([[1, 1, 2], [1, -1, 0]]), x, y)

# From A*x = b form
A = Matrix([[1, 1], [1, -1]])
b = Matrix([2, 0])
linsolve((A, b), x, y)
```

* *非线性系统 - nonlinsolve:**
```python
from sympy import nonlinsolve

nonlinsolve([x**2 + y - 2, x + y**2 - 3], x, y)
```

* *注意：** 目前 nonlinsolve 不返回 LambertW.

### 多项式形式的解根

```python
from sympy import roots, solve

# Get roots with multiplicities
roots(x**3 - 6*x**2 + 9*x, x)  # {0: 1, 3: 2}
# Means x=0 (multiplicity 1), x=3 (multiplicity 2)
```

### 通用求解器 - 求解

超越方程更灵活的替代方案：
```python
from sympy import solve, exp, log

solve(exp(x) - 3, x)     # [log(3)]
solve(x**2 - 4, x)       # [-2, 2]
solve([x + y - 1, x - y + 1], [x, y])  # {x: 0, y: 1}
```

### 微分方程 - dsolve

```python
from sympy import Function, dsolve, Derivative, Eq

# Define function
f = symbols('f', cls=Function)

# Solve ODE
dsolve(Derivative(f(x), x) - f(x), f(x))
# Returns: Eq(f(x), C1*exp(x))

# With initial conditions
dsolve(Derivative(f(x), x) - f(x), f(x), ics={f(0): 1})
# Returns: Eq(f(x), exp(x))

# Second-order ODE
dsolve(Derivative(f(x), x, 2) + f(x), f(x))
# Returns: Eq(f(x), C1*sin(x) + C2*cos(x))
```

## 常见模式和最佳实践

### 模式 1：增量构建复杂表达式
```python
from sympy import *
x, y = symbols('x y')

# Build step by step
expr = x**2
expr = expr + 2*x + 1
expr = simplify(expr)
```

### 模式 2：使用假设
```python
# Define symbols with physical constraints
x = symbols('x', positive=True, real=True)
y = symbols('y', real=True)

# SymPy can use these for simplification
sqrt(x**2)  # Returns x (not Abs(x)) due to positive assumption
```

### 模式 3：转换为数值函数
```python
from sympy import lambdify
import numpy as np

expr = x**2 + 2*x + 1
f = lambdify(x, expr, 'numpy')

# Now can use with numpy arrays
x_vals = np.linspace(0, 10, 100)
y_vals = f(x_vals)
```

### 模式 4：漂亮打印
```python
from sympy import init_printing, pprint
init_printing()  # Enable pretty printing in terminal/notebook

expr = Integral(sqrt(1/x), x)
pprint(expr)  # Displays nicely formatted output
```
