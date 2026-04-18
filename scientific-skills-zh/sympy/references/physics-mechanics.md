# SymPy 物理与力学

本文档涵盖了SymPy的物理模块，包括经典力学、量子力学、矢量分析、单位、光学、连续介质力学和控制系统。

## 矢量分析

### 创建参考系和向量

```python
from sympy.physics.vector import ReferenceFrame, dynamicsymbols

# Create reference frames
N = ReferenceFrame('N')  # Inertial frame
B = ReferenceFrame('B')  # Body frame

# Create vectors
v = 3*N.x + 4*N.y + 5*N.z

# Time-varying quantities
t = dynamicsymbols._t
x = dynamicsymbols('x')  # Function of time
v = x.diff(t) * N.x  # Velocity vector
```

### 向量运算

```python
from sympy.physics.vector import dot, cross

v1 = 3*N.x + 4*N.y
v2 = 1*N.x + 2*N.y + 3*N.z

# Dot product
d = dot(v1, v2)

# Cross product
c = cross(v1, v2)

# Magnitude
mag = v1.magnitude()

# Normalize
v1_norm = v1.normalize()
```

### 框架方向

```python
# Rotate frame B relative to N
from sympy import symbols, cos, sin
theta = symbols('theta')

# Simple rotation about z-axis
B.orient(N, 'Axis', [theta, N.z])

# Direction cosine matrix (DCM)
dcm = N.dcm(B)

# Angular velocity of B in N
omega = B.ang_vel_in(N)
```

### 点和运动学

```python
from sympy.physics.vector import Point

# Create points
O = Point('O')  # Origin
P = Point('P')

# Set position
P.set_pos(O, 3*N.x + 4*N.y)

# Set velocity
P.set_vel(N, 5*N.x + 2*N.y)

# Get velocity of P in frame N
v = P.vel(N)

# Get acceleration
a = P.acc(N)
```

## 经典力学

### 拉格朗日力学

```python
from sympy import symbols, Function
from sympy.physics.mechanics import dynamicsymbols, LagrangesMethod

# Define generalized coordinates
q = dynamicsymbols('q')
qd = dynamicsymbols('q', 1)  # q dot (velocity)

# Define Lagrangian (L = T - V)
from sympy import Rational
m, g, l = symbols('m g l')
T = Rational(1, 2) * m * (l * qd)**2  # Kinetic energy
V = m * g * l * (1 - cos(q))           # Potential energy
L = T - V

# Apply Lagrange's method
LM = LagrangesMethod(L, [q])
LM.form_lagranges_equations()
eqs = LM.rhs()  # Right-hand side of equations of motion
```

### 凯恩法

```python
from sympy.physics.mechanics import KanesMethod, ReferenceFrame, Point
from sympy.physics.vector import dynamicsymbols

# Define system
N = ReferenceFrame('N')
q = dynamicsymbols('q')
u = dynamicsymbols('u')  # Generalized speed

# Create Kane's equations
kd = [u - q.diff()]  # Kinematic differential equations
KM = KanesMethod(N, [q], [u], kd)

# Define forces and bodies
# ... (define particles, forces, etc.)
# KM.kanes_equations(bodies, loads)
```

### 系统刚体和惯性

```python
from sympy.physics.mechanics import RigidBody, Inertia, Point, ReferenceFrame
from sympy import symbols

# Mass and inertia parameters
m = symbols('m')
Ixx, Iyy, Izz = symbols('I_xx I_yy I_zz')

# Create reference frame and mass center
A = ReferenceFrame('A')
P = Point('P')

# Define inertia dyadic
I = Inertia(A, Ixx, Iyy, Izz)

# Create rigid body
body = RigidBody('Body', P, A, m, (I, P))
```

### 关节框架

```python
from sympy.physics.mechanics import Body, PinJoint, PrismaticJoint

# Create bodies
parent = Body('P')
child = Body('C')

# Create pin (revolute) joint
pin = PinJoint('pin', parent, child)

# Create prismatic (sliding) joint
slider = PrismaticJoint('slider', parent, child, axis=parent.frame.z)
```

### 线性化

```python
# Linearize equations of motion about an equilibrium
operating_point = {q: 0, u: 0}  # Equilibrium point
A, B = KM.linearize(q_ind=[q], u_ind=[u],
                     A_and_B=True,
                     op_point=operating_point)
# A: state matrix, B: input matrix
```

## 量子力学

### 状态和算子

```python
from sympy.physics.quantum import Ket, Bra, Operator, Dagger

# Define states
psi = Ket('psi')
phi = Ket('phi')

# Bra states
bra_psi = Bra('psi')

# Operators
A = Operator('A')
B = Operator('B')

# Hermitian conjugate
A_dag = Dagger(A)

# Inner product
inner = bra_psi * psi
```

### 换向器和反换向器

```python
from sympy.physics.quantum import Commutator, AntiCommutator

# Commutator [A, B] = AB - BA
comm = Commutator(A, B)
comm.doit()

# Anti-commutator {A, B} = AB + BA
anti = AntiCommutator(A, B)
anti.doit()
```

### 量子谐波振荡器

```python
from sympy.physics.quantum.qho_1d import RaisingOp, LoweringOp, NumberOp

# Creation and annihilation operators
a_dag = RaisingOp('a')  # Creation operator
a = LoweringOp('a')      # Annihilation operator
N = NumberOp('N')        # Number operator

# Number states
from sympy.physics.quantum.qho_1d import Ket as QHOKet
n = QHOKet('n')
```

### 自旋系统

```python
from sympy.physics.quantum.spin import (
    JzKet, JxKet, JyKet,  # Spin states
    Jz, Jx, Jy,            # Spin operators
    J2                     # Total angular momentum squared
)

# Spin-1/2 state
from sympy import Rational
psi = JzKet(Rational(1, 2), Rational(1, 2))  # |1/2, 1/2⟩

# Apply operator
result = Jz * psi
```

### 量子门

```python
from sympy.physics.quantum.gate import (
    H,      # Hadamard gate
    X, Y, Z,  # Pauli gates
    CNOT,    # Controlled-NOT
    SWAP     # Swap gate
)

# Apply gate to quantum state
from sympy.physics.quantum.qubit import Qubit
q = Qubit('01')
result = H(0) * q  # Apply Hadamard to qubit 0
```

### 量子算法

```python
from sympy.physics.quantum.grover import grover_iteration, OracleGate

# Grover's algorithm components available
# from sympy.physics.quantum.shor import <components>
# Shor's algorithm components available
```

## 单位和尺寸

### 使用单位

```python
from sympy.physics.units import (
    meter, kilogram, second,
    newton, joule, watt,
    convert_to
)

# Define quantities
distance = 5 * meter
mass = 10 * kilogram
time = 2 * second

# Calculate force
force = mass * distance / time**2

# Convert units
force_in_newtons = convert_to(force, newton)
```

### 单位系统

```python
from sympy.physics.units import SI, gravitational_constant, speed_of_light

# SI units
print(SI._base_units)  # Base SI units

# Physical constants
G = gravitational_constant
c = speed_of_light
```

### 自定义单位

```python
from sympy.physics.units import Quantity, meter, second

# Define custom unit
parsec = Quantity('parsec')
parsec.set_global_relative_scale_factor(3.0857e16 * meter, meter)
```

### 尺寸分析

```python
from sympy.physics.units import Dimension, length, time, mass

# Check dimensions
from sympy.physics.units import convert_to, meter, second
velocity = 10 * meter / second
print(velocity.dimension)  # Dimension(length/time)
```

## 光学

### 高斯光学

```python
from sympy.physics.optics import (
    BeamParameter,
    FreeSpace,
    FlatRefraction,
    CurvedRefraction,
    ThinLens
)

# Gaussian beam parameter
q = BeamParameter(wavelen=532e-9, z=0, w=1e-3)

# Propagation through free space
q_new = FreeSpace(1) * q

# Thin lens
q_focused = ThinLens(f=0.1) * q
```

### 波和偏振

```python
from sympy.physics.optics import TWave

# Plane wave
wave = TWave(amplitude=1, frequency=5e14, phase=0)

# Medium properties (refractive index, etc.)
from sympy.physics.optics import Medium
medium = Medium('glass', permittivity=2.25)
```

## 连续体力学

### 梁分析

```python
from sympy.physics.continuum_mechanics.beam import Beam
from sympy import symbols

# Define beam
E, I = symbols('E I', positive=True)  # Young's modulus, moment of inertia
length = 10

beam = Beam(length, E, I)

# Apply loads
from sympy.physics.continuum_mechanics.beam import Beam
beam.apply_load(-1000, 5, -1)  # Point load of -1000 at x=5

# Calculate reactions
beam.solve_for_reaction_loads()

# Get shear force, bending moment, deflection
x = symbols('x')
shear = beam.shear_force()
moment = beam.bending_moment()
deflection = beam.deflection()
```

### 桁架分析

```python
from sympy.physics.continuum_mechanics.truss import Truss

# Create truss
truss = Truss()

# Add nodes
truss.add_node(('A', 0, 0), ('B', 4, 0), ('C', 2, 3))

# Add members
truss.add_member(('AB', 'A', 'B'), ('BC', 'B', 'C'))

# Apply loads
truss.apply_load(('C', 1000, 270))  # 1000 N at 270° at node C

# Solve
truss.solve()
```

### 电缆分析

```python
from sympy.physics.continuum_mechanics.cable import Cable

# Create cable
cable = Cable(('A', 0, 10), ('B', 10, 10))

# Apply loads
cable.apply_load(-1, 5)  # Distributed load

# Solve for tension and shape
cable.solve()
```

## 控制系统

### 传递函数和状态空间

```python
from sympy.physics.control import TransferFunction, StateSpace
from sympy.abc import s

# Transfer function
tf = TransferFunction(s + 1, s**2 + 2*s + 1, s)

# State-space representation
A = [[0, 1], [-1, -2]]
B = [[0], [1]]
C = [[1, 0]]
D = [[0]]

ss = StateSpace(A, B, C, D)

# Convert between representations
ss_from_tf = tf.to_statespace()
tf_from_ss = ss.to_TransferFunction()
```

### 系统分析

```python
# Poles and zeros
poles = tf.poles()
zeros = tf.zeros()

# Stability
is_stable = tf.is_stable()

# Step response, impulse response, etc.
# (Often requires numerical evaluation)
```

## 生物力学

### 肌肉腱模型

```python
from sympy.physics.biomechanics import (
    MusculotendonDeGroote2016,
    FirstOrderActivationDeGroote2016
)

# Create musculotendon model
mt = MusculotendonDeGroote2016('muscle')

# Activation dynamics
activation = FirstOrderActivationDeGroote2016('muscle_activation')
```

## 高能物理

### 粒子物理

```python
# Gamma matrices and Dirac equations
from sympy.physics.hep.gamma_matrices import GammaMatrix

gamma0 = GammaMatrix(0)
gamma1 = GammaMatrix(1)
```

## 常见物理模式

### 模式 1：设置力学问题

```python
from sympy.physics.mechanics import dynamicsymbols, ReferenceFrame, Point
from sympy import symbols

# 1. Define reference frame
N = ReferenceFrame('N')

# 2. Define generalized coordinates
q = dynamicsymbols('q')
q_dot = dynamicsymbols('q', 1)

# 3. Define points and vectors
O = Point('O')
P = Point('P')

# 4. Set kinematics
P.set_pos(O, length * N.x)
P.set_vel(N, length * q_dot * N.x)

# 5. Define forces and apply Lagrange or Kane method
```

### 模式 2：量子态操纵

```python
from sympy.physics.quantum import Ket, Operator, qapply

# Define state
psi = Ket('psi')

# Define operator
H = Operator('H')  # Hamiltonian

# Apply operator
result = qapply(H * psi)
```

### 模式 3：单位转换工作流程

```python
from sympy.physics.units import convert_to, meter, foot, second, minute

# Define quantity with units
distance = 100 * meter
time = 5 * minute

# Perform calculation
speed = distance / time

# Convert to desired units
speed_m_per_s = convert_to(speed, meter/second)
speed_ft_per_min = convert_to(speed, foot/minute)
```

### 模式 4：光束挠度分析

```python
from sympy.physics.continuum_mechanics.beam import Beam
from sympy import symbols

E, I = symbols('E I', positive=True, real=True)
beam = Beam(10, E, I)

# Apply boundary conditions
beam.apply_support(0, 'pin')
beam.apply_support(10, 'roller')

# Apply loads
beam.apply_load(-1000, 5, -1)  # Point load
beam.apply_load(-50, 0, 0, 10)  # Distributed load

# Solve
beam.solve_for_reaction_loads()

# Get results at specific locations
x = 5
deflection_at_mid = beam.deflection().subs(symbols('x'), x)
```

## 重要注意事项

1. **时变变量：** 对于力学问题中的时变量，使用 `dynamicsymbols()`。

2. **单位：** 始终使用 `sympy.physics.units` 模块显式指定单位进行物理计算。

3. **参考系：** 明确定义矢量分析的参考系及其相对方向。

4. **数值评估：** 许多物理计算需要数值评估。使用`evalf()`或转换为NumPy进行数值计算。

5. **假设：** 对符号使用适当的假设（例如，`positive=True`、`real=True`）以帮助 SymPy 正确简化物理表达式。
