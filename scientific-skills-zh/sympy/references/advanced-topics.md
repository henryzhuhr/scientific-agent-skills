# SymPy 高级主题

本文档涵盖了 SymPy 的高级数学功能，包括几何、数论、组合、逻辑和集合、统计、多项式和特殊函数。

## 几何

### 2D 几何

```python
from sympy.geometry import Point, Line, Circle, Triangle, Polygon

# Points
p1 = Point(0, 0)
p2 = Point(1, 1)
p3 = Point(1, 0)

# Distance between points
dist = p1.distance(p2)

# Lines
line = Line(p1, p2)
line_from_eq = Line(Point(0, 0), slope=2)

# Line properties
line.slope       # Slope
line.equation()  # Equation of line
line.length      # oo (infinite for lines)

# Line segment
from sympy.geometry import Segment
seg = Segment(p1, p2)
seg.length       # Finite length
seg.midpoint     # Midpoint

# Intersection
line2 = Line(Point(0, 1), Point(1, 0))
intersection = line.intersection(line2)  # [Point(1/2, 1/2)]

# Circles
circle = Circle(Point(0, 0), 5)  # Center, radius
circle.area           # 25*pi
circle.circumference  # 10*pi

# Triangles
tri = Triangle(p1, p2, p3)
tri.area       # Area
tri.perimeter  # Perimeter
tri.angles     # Dictionary of angles
tri.vertices   # Tuple of vertices

# Polygons
poly = Polygon(Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1))
poly.area
poly.perimeter
poly.vertices
```

### 几何查询

```python
# Check if point is on line/curve
point = Point(0.5, 0.5)
line.contains(point)

# Check if parallel/perpendicular
line1 = Line(Point(0, 0), Point(1, 1))
line2 = Line(Point(0, 1), Point(1, 2))
line1.is_parallel(line2)  # True
line1.is_perpendicular(line2)  # False

# Tangent lines
from sympy.geometry import Circle, Point
circle = Circle(Point(0, 0), 5)
point = Point(5, 0)
tangents = circle.tangent_lines(point)
```

### 3D 几何

```python
from sympy.geometry import Point3D, Line3D, Plane

# 3D Points
p1 = Point3D(0, 0, 0)
p2 = Point3D(1, 1, 1)
p3 = Point3D(1, 0, 0)

# 3D Lines
line = Line3D(p1, p2)

# Planes
plane = Plane(p1, p2, p3)  # From 3 points
plane = Plane(Point3D(0, 0, 0), normal_vector=(1, 0, 0))  # From point and normal

# Plane equation
plane.equation()

# Distance from point to plane
point = Point3D(2, 3, 4)
dist = plane.distance(point)

# Intersection of plane and line
intersection = plane.intersection(line)
```

### 曲线和椭圆

```python
from sympy.geometry import Ellipse, Curve
from sympy import sin, cos, pi

# Ellipse
ellipse = Ellipse(Point(0, 0), hradius=3, vradius=2)
ellipse.area          # 6*pi
ellipse.eccentricity  # Eccentricity

# Parametric curves
from sympy.abc import t
curve = Curve((cos(t), sin(t)), (t, 0, 2*pi))  # Circle
```

## 数论

### 素数数字

```python
from sympy.ntheory import isprime, primerange, prime, nextprime, prevprime

# Check if prime
isprime(7)    # True
isprime(10)   # False

# Generate primes in range
list(primerange(10, 50))  # [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

# nth prime
prime(10)     # 29 (10th prime)

# Next and previous primes
nextprime(10)  # 11
prevprime(10)  # 7
```

### 质因数分解

```python
from sympy import factorint, primefactors, divisors

# Prime factorization
factorint(60)  # {2: 2, 3: 1, 5: 1} means 2^2 * 3^1 * 5^1

# List of prime factors
primefactors(60)  # [2, 3, 5]

# All divisors
divisors(60)  # [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60]
```

### GCD 和LCM

```python
from sympy import gcd, lcm, igcd, ilcm

# Greatest common divisor
gcd(60, 48)   # 12
igcd(60, 48)  # 12 (integer version)

# Least common multiple
lcm(60, 48)   # 240
ilcm(60, 48)  # 240 (integer version)

# Multiple arguments
gcd(60, 48, 36)  # 12
```

### 模块化算术

```python
from sympy.ntheory import mod_inverse, totient, is_primitive_root

# Modular inverse (find x such that a*x ≡ 1 (mod m))
mod_inverse(3, 7)  # 5 (because 3*5 = 15 ≡ 1 (mod 7))

# Euler's totient function
totient(10)  # 4 (numbers less than 10 coprime to 10: 1,3,7,9)

# Primitive roots
is_primitive_root(2, 5)  # True
```

### 丢番图方程

```python
from sympy.solvers.diophantine import diophantine
from sympy.abc import x, y, z

# Linear Diophantine: ax + by = c
diophantine(3*x + 4*y - 5)  # {(4*t_0 - 5, -3*t_0 + 5)}

# Quadratic forms
diophantine(x**2 + y**2 - 25)  # Pythagorean-type equations

# More complex equations
diophantine(x**2 - 4*x*y + 8*y**2 - 3*x + 7*y - 5)
```

### 连分数

```python
from sympy import nsimplify, continued_fraction_iterator
from sympy import Rational, pi

# Convert to continued fraction
cf = continued_fraction_iterator(Rational(415, 93))
list(cf)  # [4, 2, 6, 7]

# Approximate irrational numbers
cf_pi = continued_fraction_iterator(pi.evalf(20))
```

## 组合学

### 排列和组合

```python
from sympy import factorial, binomial, factorial2
from sympy.functions.combinatorial.numbers import nC, nP

# Factorial
factorial(5)  # 120

# Binomial coefficient (n choose k)
binomial(5, 2)  # 10

# Permutations nPk = n!/(n-k)!
nP(5, 2)  # 20

# Combinations nCk = n!/(k!(n-k)!)
nC(5, 2)  # 10

# Double factorial n!!
factorial2(5)  # 15 (5*3*1)
factorial2(6)  # 48 (6*4*2)
```

### 排列对象

```python
from sympy.combinatorics import Permutation

# Create permutation (cycle notation)
p = Permutation([1, 2, 0, 3])  # Sends 0->1, 1->2, 2->0, 3->3
p = Permutation(0, 1, 2)(3)    # Cycle notation: (0 1 2)(3)

# Permutation operations
p.order()       # Order of permutation
p.is_even       # True if even permutation
p.inversions()  # Number of inversions

# Compose permutations
q = Permutation([2, 0, 1, 3])
r = p * q       # Composition
```

### 分区

```python
from sympy.utilities.iterables import partitions
from sympy.functions.combinatorial.numbers import partition

# Number of integer partitions
partition(5)  # 7 (5, 4+1, 3+2, 3+1+1, 2+2+1, 2+1+1+1, 1+1+1+1+1)

# Generate all partitions
list(partitions(4))
# {4: 1}, {3: 1, 1: 1}, {2: 2}, {2: 1, 1: 2}, {1: 4}
```

### 加泰罗尼亚语和斐波那契数数字

```python
from sympy import catalan, fibonacci, lucas

# Catalan numbers
catalan(5)  # 42

# Fibonacci numbers
fibonacci(10)  # 55
lucas(10)      # 123 (Lucas numbers)
```

### 群论

```python
from sympy.combinatorics import PermutationGroup, Permutation

# Create permutation group
p1 = Permutation([1, 0, 2])
p2 = Permutation([0, 2, 1])
G = PermutationGroup(p1, p2)

# Group properties
G.order()        # Order of group
G.is_abelian     # Check if abelian
G.is_cyclic()    # Check if cyclic
G.elements       # All group elements
```

## 逻辑和集合

### 布尔逻辑

```python
from sympy import symbols, And, Or, Not, Xor, Implies, Equivalent
from sympy.logic.boolalg import truth_table, simplify_logic

# Define boolean variables
x, y, z = symbols('x y z', bool=True)

# Logical operations
expr = And(x, Or(y, Not(z)))
expr = Implies(x, y)  # x -> y
expr = Equivalent(x, y)  # x <-> y
expr = Xor(x, y)  # Exclusive OR

# Simplification
expr = (x & y) | (x & ~y)
simplified = simplify_logic(expr)  # Returns x

# Truth table
expr = Implies(x, y)
print(truth_table(expr, [x, y]))
```

### 集合

```python
from sympy import FiniteSet, Interval, Union, Intersection, Complement
from sympy import S  # For special sets

# Finite sets
A = FiniteSet(1, 2, 3, 4)
B = FiniteSet(3, 4, 5, 6)

# Set operations
union = Union(A, B)              # {1, 2, 3, 4, 5, 6}
intersection = Intersection(A, B)  # {3, 4}
difference = Complement(A, B)     # {1, 2}

# Intervals
I = Interval(0, 1)              # [0, 1]
I_open = Interval.open(0, 1)    # (0, 1)
I_lopen = Interval.Lopen(0, 1)  # (0, 1]
I_ropen = Interval.Ropen(0, 1)  # [0, 1)

# Special sets
S.Reals        # All real numbers
S.Integers     # All integers
S.Naturals     # Natural numbers
S.EmptySet     # Empty set
S.Complexes    # Complex numbers

# Set membership
3 in A  # True
7 in A  # False

# Subset and superset
A.is_subset(B)    # False
A.is_superset(B)  # False
```

### 集合论运算

```python
from sympy import ImageSet, Lambda
from sympy.abc import x

# Image set (set of function values)
squares = ImageSet(Lambda(x, x**2), S.Integers)
# {x^2 | x ∈ ℤ}

# Power set
from sympy.sets import FiniteSet
A = FiniteSet(1, 2, 3)
# Note: SymPy doesn't have direct powerset, but can generate
```

## 多项式

### 多项式运算

```python
from sympy import Poly, symbols, factor, expand, roots
x, y = symbols('x y')

# Create polynomial
p = Poly(x**2 + 2*x + 1, x)

# Polynomial properties
p.degree()       # 2
p.coeffs()       # [1, 2, 1]
p.as_expr()      # Convert back to expression

# Arithmetic
p1 = Poly(x**2 + 1, x)
p2 = Poly(x + 1, x)
p3 = p1 + p2
p4 = p1 * p2
q, r = div(p1, p2)  # Quotient and remainder
```

### 多项式根

```python
from sympy import roots, real_roots, count_roots

p = Poly(x**3 - 6*x**2 + 11*x - 6, x)

# All roots
r = roots(p)  # {1: 1, 2: 1, 3: 1}

# Real roots only
r = real_roots(p)

# Count roots in interval
count_roots(p, a, b)  # Number of roots in [a, b]
```

### 多项式GCD 和因式分解

```python
from sympy import gcd, lcm, factor, factor_list

p1 = Poly(x**2 - 1, x)
p2 = Poly(x**2 - 2*x + 1, x)

# GCD and LCM
g = gcd(p1, p2)
l = lcm(p1, p2)

# Factorization
f = factor(x**3 - x**2 + x - 1)  # (x - 1)*(x**2 + 1)
factors = factor_list(x**3 - x**2 + x - 1)  # List form
```

### Groebner 基

```python
from sympy import groebner, symbols

x, y, z = symbols('x y z')
polynomials = [x**2 + y**2 + z**2 - 1, x*y - z]

# Compute Groebner basis
gb = groebner(polynomials, x, y, z)
```

## 统计

### 随机变量

```python
from sympy.stats import (
    Normal, Uniform, Exponential, Poisson, Binomial,
    P, E, variance, density, sample
)

# Define random variables
X = Normal('X', 0, 1)  # Normal(mean, std)
Y = Uniform('Y', 0, 1)  # Uniform(a, b)
Z = Exponential('Z', 1)  # Exponential(rate)

# Probability
P(X > 0)  # 1/2
P((X > 0) & (X < 1))

# Expected value
E(X)  # 0
E(X**2)  # 1

# Variance
variance(X)  # 1

# Density function
density(X)(x)  # sqrt(2)*exp(-x**2/2)/(2*sqrt(pi))
```

### 离散分布

```python
from sympy.stats import Die, Bernoulli, Binomial, Poisson

# Die
D = Die('D', 6)
P(D > 3)  # 1/2

# Bernoulli
B = Bernoulli('B', 0.5)
P(B)  # 1/2

# Binomial
X = Binomial('X', 10, 0.5)
P(X == 5)  # Probability of exactly 5 successes in 10 trials

# Poisson
Y = Poisson('Y', 3)
P(Y < 2)  # Probability of less than 2 events
```

### 联合分布

```python
from sympy.stats import Normal, P, E
from sympy import symbols

# Independent random variables
X = Normal('X', 0, 1)
Y = Normal('Y', 0, 1)

# Joint probability
P((X > 0) & (Y > 0))  # 1/4

# Covariance
from sympy.stats import covariance
covariance(X, Y)  # 0 (independent)
```

## 特殊函数

### 常见特殊函数

```python
from sympy import (
    gamma,      # Gamma function
    beta,       # Beta function
    erf,        # Error function
    besselj,    # Bessel function of first kind
    bessely,    # Bessel function of second kind
    hermite,    # Hermite polynomial
    legendre,   # Legendre polynomial
    laguerre,   # Laguerre polynomial
    chebyshevt, # Chebyshev polynomial (first kind)
    zeta        # Riemann zeta function
)

# Gamma function
gamma(5)  # 24 (equivalent to 4!)
gamma(1/2)  # sqrt(pi)

# Bessel functions
besselj(0, x)  # J_0(x)
bessely(1, x)  # Y_1(x)

# Orthogonal polynomials
hermite(3, x)    # 8*x**3 - 12*x
legendre(2, x)   # (3*x**2 - 1)/2
laguerre(2, x)   # x**2/2 - 2*x + 1
chebyshevt(3, x) # 4*x**3 - 3*x
```

### 超几何函数

```python
from sympy import hyper, meijerg

# Hypergeometric function
hyper([1, 2], [3], x)

# Meijer G-function
meijerg([[1, 1], []], [[1], [0]], x)
```

## 常见模式

### 模式1：符号几何问题

```python
from sympy.geometry import Point, Triangle
from sympy import symbols

# Define symbolic triangle
a, b = symbols('a b', positive=True)
tri = Triangle(Point(0, 0), Point(a, 0), Point(0, b))

# Compute properties symbolically
area = tri.area  # a*b/2
perimeter = tri.perimeter  # a + b + sqrt(a**2 + b**2)
```

### 模式2：数论计算

```python
from sympy.ntheory import factorint, totient, isprime

# Factor and analyze
n = 12345
factors = factorint(n)
phi = totient(n)
is_prime = isprime(n)
```

### 模式3：组合生成

```python
from sympy.utilities.iterables import multiset_permutations, combinations

# Generate all permutations
perms = list(multiset_permutations([1, 2, 3]))

# Generate combinations
combs = list(combinations([1, 2, 3, 4], 2))
```

### 模式4：概率计算

```python
from sympy.stats import Normal, P, E, variance

X = Normal('X', mu, sigma)

# Compute statistics
mean = E(X)
var = variance(X)
prob = P(X > a)
```

## 重要说明

1. **假设：** 许多操作受益于符号假设（例如，`positive=True`、`integer=True`）。

2. **符号与数字：** 这些操作是符号性的。使用 `evalf()` 获得数值结果。

3. **性能：** 复杂的符号操作可能会很慢。考虑大规模计算的数值方法。

4. **精确算术：** SymPy 保持精确表示（例如，`sqrt(2)` 而不是 `1.414...`）。
