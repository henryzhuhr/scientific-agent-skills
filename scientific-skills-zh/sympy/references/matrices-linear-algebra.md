# SymPy 矩阵和线性代数

本文档涵盖了 SymPy 的矩阵运算、线性代数能力以及线性方程组的求解。

## 矩阵创建

### 基本矩阵构造

```python
from sympy import Matrix, eye, zeros, ones, diag

# From list of rows
M = Matrix([[1, 2], [3, 4]])
M = Matrix([
    [1, 2, 3],
    [4, 5, 6]
])

# Column vector
v = Matrix([1, 2, 3])

# Row vector
v = Matrix([[1, 2, 3]])
```

### 特别矩阵

```python
# Identity matrix
I = eye(3)  # 3x3 identity
# [[1, 0, 0],
#  [0, 1, 0],
#  [0, 0, 1]]

# Zero matrix
Z = zeros(2, 3)  # 2 rows, 3 columns of zeros

# Ones matrix
O = ones(3, 2)   # 3 rows, 2 columns of ones

# Diagonal matrix
D = diag(1, 2, 3)
# [[1, 0, 0],
#  [0, 2, 0],
#  [0, 0, 3]]

# Block diagonal
from sympy import BlockDiagMatrix
A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])
BD = BlockDiagMatrix(A, B)
```

## 矩阵属性和访问

### 形状和尺寸

```python
M = Matrix([[1, 2, 3], [4, 5, 6]])

M.shape  # (2, 3) - returns tuple (rows, cols)
M.rows   # 2
M.cols   # 3
```

### 访问元素

```python
M = Matrix([[1, 2, 3], [4, 5, 6]])

# Single element
M[0, 0]  # 1 (zero-indexed)
M[1, 2]  # 6

# Row access
M[0, :]   # Matrix([[1, 2, 3]])
M.row(0)  # Same as above

# Column access
M[:, 1]   # Matrix([[2], [5]])
M.col(1)  # Same as above

# Slicing
M[0:2, 0:2]  # Top-left 2x2 submatrix
```

### 修改

```python
M = Matrix([[1, 2], [3, 4]])

# Insert row
M = M.row_insert(1, Matrix([[5, 6]]))
# [[1, 2],
#  [5, 6],
#  [3, 4]]

# Insert column
M = M.col_insert(1, Matrix([7, 8]))

# Delete row
M = M.row_del(0)

# Delete column
M = M.col_del(1)
```

## 基本矩阵运算

### 算术运算

```python
from sympy import Matrix

A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])

# Addition
C = A + B

# Subtraction
C = A - B

# Scalar multiplication
C = 2 * A

# Matrix multiplication
C = A * B

# Element-wise multiplication (Hadamard product)
C = A.multiply_elementwise(B)

# Power
C = A**2  # Same as A * A
C = A**3  # A * A * A
```

### 转置和共轭

```python
M = Matrix([[1, 2], [3, 4]])

# Transpose
M.T
# [[1, 3],
#  [2, 4]]

# Conjugate (for complex matrices)
M.conjugate()

# Conjugate transpose (Hermitian transpose)
M.H  # Same as M.conjugate().T
```

### 逆

```python
M = Matrix([[1, 2], [3, 4]])

# Inverse
M_inv = M**-1
M_inv = M.inv()

# Verify
M * M_inv  # Returns identity matrix

# Check if invertible
M.is_invertible()  # True or False
```

## 高级线性代数

### 行列式

```python
M = Matrix([[1, 2], [3, 4]])
M.det()  # -2

# For symbolic matrices
from sympy import symbols
a, b, c, d = symbols('a b c d')
M = Matrix([[a, b], [c, d]])
M.det()  # a*d - b*c
```

### Trace

```python
M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
M.trace()  # 1 + 5 + 9 = 15
```

### 行梯形形式

```python
M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Reduced Row Echelon Form
rref_M, pivot_cols = M.rref()
# rref_M is the RREF matrix
# pivot_cols is tuple of pivot column indices
```

### Rank

```python
M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
M.rank()  # 2 (this matrix is rank-deficient)
```

### 空空间和列空间

```python
M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Nullspace (kernel)
null = M.nullspace()
# Returns list of basis vectors for nullspace

# Column space
col = M.columnspace()
# Returns list of basis vectors for column space

# Row space
row = M.rowspace()
# Returns list of basis vectors for row space
```

### 正交化

```python
# Gram-Schmidt orthogonalization
vectors = [Matrix([1, 2, 3]), Matrix([4, 5, 6])]
ortho = Matrix.orthogonalize(*vectors)

# With normalization
ortho_norm = Matrix.orthogonalize(*vectors, normalize=True)
```

## 特征值和特征向量

### 计算特征值

```python
M = Matrix([[1, 2], [2, 1]])

# Eigenvalues with multiplicities
eigenvals = M.eigenvals()
# Returns dict: {eigenvalue: multiplicity}
# Example: {3: 1, -1: 1}

# Just the eigenvalues as a list
eigs = list(M.eigenvals().keys())
```

### 计算特征向量

```python
M = Matrix([[1, 2], [2, 1]])

# Eigenvectors with eigenvalues
eigenvects = M.eigenvects()
# Returns list of tuples: (eigenvalue, multiplicity, [eigenvectors])
# Example: [(3, 1, [Matrix([1, 1])]), (-1, 1, [Matrix([1, -1])])]

# Access individual eigenvectors
for eigenval, multiplicity, eigenvecs in M.eigenvects():
    print(f"Eigenvalue: {eigenval}")
    print(f"Eigenvectors: {eigenvecs}")
```

### 对角化

```python
M = Matrix([[1, 2], [2, 1]])

# Check if diagonalizable
M.is_diagonalizable()  # True or False

# Diagonalize (M = P*D*P^-1)
P, D = M.diagonalize()
# P: matrix of eigenvectors
# D: diagonal matrix of eigenvalues

# Verify
P * D * P**-1 == M  # True
```

### 特征多项式

```python
from sympy import symbols
lam = symbols('lambda')

M = Matrix([[1, 2], [2, 1]])
charpoly = M.charpoly(lam)
# Returns characteristic polynomial
```

### Jordan 正态形式

```python
M = Matrix([[2, 1, 0], [0, 2, 1], [0, 0, 2]])

# Jordan form (for non-diagonalizable matrices)
P, J = M.jordan_form()
# J is the Jordan normal form
# P is the transformation matrix
```

## 矩阵分解

### LU 分解

```python
M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 10]])

# LU decomposition
L, U, perm = M.LUdecomposition()
# L: lower triangular
# U: upper triangular
# perm: permutation indices
```

### QR 分解

```python
M = Matrix([[1, 2], [3, 4], [5, 6]])

# QR decomposition
Q, R = M.QRdecomposition()
# Q: orthogonal matrix
# R: upper triangular matrix
```

### Cholesky 分解

```python
# For positive definite symmetric matrices
M = Matrix([[4, 2], [2, 3]])

L = M.cholesky()
# L is lower triangular such that M = L*L.T
```

### 奇异值分解 (SVD)

```python
M = Matrix([[1, 2], [3, 4], [5, 6]])

# SVD (note: may require numerical evaluation)
U, S, V = M.singular_value_decomposition()
# M = U * S * V
```

## 求解线性系统

### 使用矩阵方程

```python
# Solve Ax = b
A = Matrix([[1, 2], [3, 4]])
b = Matrix([5, 6])

# Solution
x = A.solve(b)  # or A**-1 * b

# Least squares (for overdetermined systems)
x = A.solve_least_squares(b)
```

### 使用 linsolve

```python
from sympy import linsolve, symbols

x, y = symbols('x y')

# Method 1: List of equations
eqs = [x + y - 5, 2*x - y - 1]
sol = linsolve(eqs, [x, y])
# {(2, 3)}

# Method 2: Augmented matrix
M = Matrix([[1, 1, 5], [2, -1, 1]])
sol = linsolve(M, [x, y])

# Method 3: A*x = b form
A = Matrix([[1, 1], [2, -1]])
b = Matrix([5, 1])
sol = linsolve((A, b), [x, y])
```

### 欠定和超定系统

```python
# Underdetermined (infinite solutions)
A = Matrix([[1, 2, 3]])
b = Matrix([6])
sol = A.solve(b)  # Returns parametric solution

# Overdetermined (least squares)
A = Matrix([[1, 2], [3, 4], [5, 6]])
b = Matrix([1, 2, 3])
sol = A.solve_least_squares(b)
```

## 符号矩阵

### 使用符号条目

```python
from sympy import symbols, Matrix

a, b, c, d = symbols('a b c d')
M = Matrix([[a, b], [c, d]])

# All operations work symbolically
M.det()  # a*d - b*c
M.inv()  # Matrix([[d/(a*d - b*c), -b/(a*d - b*c)], ...])
M.eigenvals()  # Symbolic eigenvalues
```

### 矩阵函数

```python
from sympy import exp, sin, cos, Matrix

M = Matrix([[0, 1], [-1, 0]])

# Matrix exponential
exp(M)

# Trigonometric functions
sin(M)
cos(M)
```

## 可变与不可变矩阵

```python
from sympy import Matrix, ImmutableMatrix

# Mutable (default)
M = Matrix([[1, 2], [3, 4]])
M[0, 0] = 5  # Allowed

# Immutable (for use as dictionary keys, etc.)
I = ImmutableMatrix([[1, 2], [3, 4]])
# I[0, 0] = 5  # Error: ImmutableMatrix cannot be modified
```

## 稀疏矩阵

对于具有许多零项的大型矩阵：

```python
from sympy import SparseMatrix

# Create sparse matrix
S = SparseMatrix(1000, 1000, {(0, 0): 1, (100, 100): 2})
# Only stores non-zero elements

# Convert dense to sparse
M = Matrix([[1, 0, 0], [0, 2, 0]])
S = SparseMatrix(M)
```

## 常见线性代数模式

### 模式1：求解Ax = b以获得多个b向量

```python
A = Matrix([[1, 2], [3, 4]])
A_inv = A.inv()

b1 = Matrix([5, 6])
b2 = Matrix([7, 8])

x1 = A_inv * b1
x2 = A_inv * b2
```

### 模式 2：基础变化

```python
# Given vectors in old basis, convert to new basis
old_basis = [Matrix([1, 0]), Matrix([0, 1])]
new_basis = [Matrix([1, 1]), Matrix([1, -1])]

# Change of basis matrix
P = Matrix.hstack(*new_basis)
P_inv = P.inv()

# Convert vector v from old to new basis
v = Matrix([3, 4])
v_new = P_inv * v
```

### 模式 3：矩阵条件数

```python
# Estimate condition number (ratio of largest to smallest singular value)
M = Matrix([[1, 2], [3, 4]])
eigenvals = M.eigenvals()
cond = max(eigenvals.keys()) / min(eigenvals.keys())
```

### 模式 4：投影矩阵

```python
# Project onto column space of A
A = Matrix([[1, 0], [0, 1], [1, 1]])
P = A * (A.T * A).inv() * A.T
# P is projection matrix onto column space of A
```

## 重要说明

1. **零测试：** SymPy 的符号零测试会影响准确性。对于数值工作，请考虑使用 `evalf()` 或数值库.

2. **性能：** 对于大型数值矩阵，可以考虑使用 `lambdify` 转换为 NumPy 或直接使用数值线性代数库 

3. **符号计算：** 对于大型矩阵，具有符号条目的矩阵运算的计算成本可能很高。

4. **假设：** 使用符号假设（例如，`real=True`、`positive=True`）来帮助 SymPy 正确简化矩阵表达式。
