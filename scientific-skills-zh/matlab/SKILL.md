---
name: matlab
description: MATLAB 和 GNU Octave 数值计算，用于矩阵运算、数据分析、可视化和科学计算。在编写用于线性代数、信号处理、图像处理、微分方程、优化、统计或创建科学可视化的 MATLAB/Octave 脚本时使用。当用户需要 MATLAB 语法、函数的帮助或想要在 MATLAB 和 Python 代码之间进行转换时，也可以使用。脚本可以使用 MATLAB 或开源 GNU Octave 解释器执行。
license: For MATLAB (https://www.mathworks.com/pricing-licensing.html) and for Octave (GNU General Public License version 3)
compatibility: Requires either MATLAB or Octave to be installed for testing, but not required for just generating scripts.
metadata:
    skill-author: K-Dense Inc.
---

# MATLAB/Octave 科学计算

MATLAB 是一个针对矩阵运算和科学计算而优化的数值计算环境。 GNU Octave 是一个免费的开源替代品，具有高 MATLAB 兼容性。

## 快速入门

* *运行 MATLAB 脚本：**
```bash
# MATLAB (commercial)
matlab -nodisplay -nosplash -r "run('script.m'); exit;"

# GNU Octave (free, open-source)
octave script.m
```

* *安装 GNU Octave:**
```bash
# macOS
brew install octave

# Ubuntu/Debian
sudo apt install octave

# Windows - download from https://octave.org/download
```

## 核心功能

### 1. 矩阵运算

MATLAB 从根本上对矩阵和数组进行运算：

```matlab
% Create matrices
A = [1 2 3; 4 5 6; 7 8 9];  % 3x3 matrix
v = 1:10;                     % Row vector 1 to 10
v = linspace(0, 1, 100);      % 100 points from 0 to 1

% Special matrices
I = eye(3);          % Identity matrix
Z = zeros(3, 4);     % 3x4 zero matrix
O = ones(2, 3);      % 2x3 ones matrix
R = rand(3, 3);      % Random uniform
N = randn(3, 3);     % Random normal

% Matrix operations
B = A';              % Transpose
C = A * B;           % Matrix multiplication
D = A .* B;          % Element-wise multiplication
E = A \ b;           % Solve linear system Ax = b
F = inv(A);          % Matrix inverse
```

 有关完整的矩阵运算，请参阅[references/matrices-arrays.md](references/matrices-arrays.md).

### 2.线性代数

```matlab
% Eigenvalues and eigenvectors
[V, D] = eig(A);     % V: eigenvectors, D: diagonal eigenvalues

% Singular value decomposition
[U, S, V] = svd(A);

% Matrix decompositions
[L, U] = lu(A);      % LU decomposition
[Q, R] = qr(A);      % QR decomposition
R = chol(A);         % Cholesky (symmetric positive definite)

% Solve linear systems
x = A \ b;           % Preferred method
x = linsolve(A, b);  % With options
x = inv(A) * b;      % Less efficient
```

综合线性代数请参见[references/mathematics.md](references/mathematics.md).

### 3. 绘图和可视化

```matlab
% 2D Plots
x = 0:0.1:2*pi;
y = sin(x);
plot(x, y, 'b-', 'LineWidth', 2);
xlabel('x'); ylabel('sin(x)');
title('Sine Wave');
grid on;

% Multiple plots
hold on;
plot(x, cos(x), 'r--');
legend('sin', 'cos');
hold off;

% 3D Surface
[X, Y] = meshgrid(-2:0.1:2, -2:0.1:2);
Z = X.^2 + Y.^2;
surf(X, Y, Z);
colorbar;

% Save figures
saveas(gcf, 'plot.png');
print('-dpdf', 'plot.pdf');
```

完整的可视化指南，请参见[references/graphics-visualization.md](references/graphics-visualization.md)。

### 4. 数据导入/导出

```matlab
% Read tabular data
T = readtable('data.csv');
M = readmatrix('data.csv');

% Write data
writetable(T, 'output.csv');
writematrix(M, 'output.csv');

% MAT files (MATLAB native)
save('data.mat', 'A', 'B', 'C');  % Save variables
load('data.mat');                   % Load all
S = load('data.mat', 'A');         % Load specific

% Images
img = imread('image.png');
imwrite(img, 'output.jpg');
```

完整的I/O 指南，请参见 [references/data-import-export.md](references/data-import-export.md)。

### 5. 控制流程和功能

```matlab
% Conditionals
if x > 0
    disp('positive');
elseif x < 0
    disp('negative');
else
    disp('zero');
end

% Loops
for i = 1:10
    disp(i);
end

while x > 0
    x = x - 1;
end

% Functions (in separate .m file or same file)
function y = myfunction(x, n)
    y = x.^n;
end

% Anonymous functions
f = @(x) x.^2 + 2*x + 1;
result = f(5);  % 36
```

 完整的编程指南，请参见[references/programming.md](references/programming.md).

### 6.统计与数据分析

```matlab
% Descriptive statistics
m = mean(data);
s = std(data);
v = var(data);
med = median(data);
[minVal, minIdx] = min(data);
[maxVal, maxIdx] = max(data);

% Correlation
R = corrcoef(X, Y);
C = cov(X, Y);

% Linear regression
p = polyfit(x, y, 1);  % Linear fit
y_fit = polyval(p, x);

% Moving statistics
y_smooth = movmean(y, 5);  % 5-point moving average
```

统计参考参见[references/mathematics.md](references/mathematics.md).

### 7.微分方程

```matlab
% ODE solving
% dy/dt = -2y, y(0) = 1
f = @(t, y) -2*y;
[t, y] = ode45(f, [0 5], 1);
plot(t, y);

% Higher-order: y'' + 2y' + y = 0
% Convert to system: y1' = y2, y2' = -2*y2 - y1
f = @(t, y) [y(2); -2*y(2) - y(1)];
[t, y] = ode45(f, [0 10], [1; 0]);
```

有关ODE求解器指南，请参阅[references/mathematics.md](references/mathematics.md)。

### 8.信号处理

```matlab
% FFT
Y = fft(signal);
f = (0:length(Y)-1) * fs / length(Y);
plot(f, abs(Y));

% Filtering
b = fir1(50, 0.3);           % FIR filter design
y_filtered = filter(b, 1, signal);

% Convolution
y = conv(x, h, 'same');
```

有关信号处理，请参阅[references/mathematics.md](references/mathematics.md).

## 常见模式

### 模式 1：数据分析管道

```matlab
% Load data
data = readtable('experiment.csv');

% Clean data
data = rmmissing(data);  % Remove missing values

% Analyze
grouped = groupsummary(data, 'Category', 'mean', 'Value');

% Visualize
figure;
bar(grouped.Category, grouped.mean_Value);
xlabel('Category'); ylabel('Mean Value');
title('Results by Category');

% Save
writetable(grouped, 'results.csv');
saveas(gcf, 'results.png');
```

### 模式 2：数值模拟

```matlab
% Parameters
L = 1; N = 100; T = 10; dt = 0.01;
x = linspace(0, L, N);
dx = x(2) - x(1);

% Initial condition
u = sin(pi * x);

% Time stepping (heat equation)
for t = 0:dt:T
    u_new = u;
    for i = 2:N-1
        u_new(i) = u(i) + dt/(dx^2) * (u(i+1) - 2*u(i) + u(i-1));
    end
    u = u_new;
end

plot(x, u);
```

### 模式3：批处理

```matlab
% Process multiple files
files = dir('data/*.csv');
results = cell(length(files), 1);

for i = 1:length(files)
    data = readtable(fullfile(files(i).folder, files(i).name));
    results{i} = analyze(data);  % Custom analysis function
end

% Combine results
all_results = vertcat(results{:});
```

## 参考文件

- **[matrices-arrays.md](references/matrices-arrays.md)** - 矩阵创建、索引、操作和运算
- **[mathematics.md](references/mathematics.md)** - 线性代数、微积分、ODE、优化、统计
- **[graphics-visualization.md](references/graphics-visualization.md)** - 2D/3D 绘图、自定义、导出
- **[data-import-export.md](references/data-import-export.md)** - 文件 I/O、表格、数据格式
- **[programming.md](references/programming.md)** - 函数、脚本、控制流，OOP
- **[python-integration.md](references/python-integration.md)** - 从 MATLAB 调用 Python，反之亦然
- **[octave-compatibility.md](references/octave-compatibility.md)** - MATLAB 和 GNU 之间的差异Octave
- **[executing-scripts.md](references/executing-scripts.md)** - 执行生成的脚本并进行测试

## GNU Octave 兼容性

GNU Octave 与 MATLAB 高度兼容。大多数脚本无需修改即可运行。主要区别：

- 使用 `#` 或 `%` 进行注释（MATLAB 仅限 `%`）
- Octave 允许 `++`、`--`、`+=` 运算符
- 某些工具箱功能在Octave
- 对 Octave 软件包使用 `pkg load`

有关完整的兼容性指南，请参阅 [references/octave-compatibility.md](references/octave-compatibility.md)。

## 最佳实践

1. **矢量化操作** - 尽可能避免循环：
 ```matlab
 % Slow
 for i = 1:1000
 y(i) = sin(x(i));
 end

 % Fast
 y = sin(x);
 ```

2. **预分配数组** - 避免在循环中增长数组：
 ```matlab
 % Slow
 for i = 1:1000
 y(i) = i^2;
 end

 % Fast
 y =零(1, 1000);
 对于 i = 1:1000
 y(i) = i^2;
 end
 ```

3. **使用适当的数据类型** - 混合数据表，数字矩阵：
 ```matlab
 % 数字数据
 M = readmatrix('numbers.csv');

 % 带标题的混合数据
 T = readtable('mixed.csv');
 ``

4. **注释和文档** - 使用函数帮助：
 ```matlab
 function y = myfunction(x)
 %MYFUNCTION 简要描述
 % Y = MYFUNCTION(X)详细描述
 %
 % 示例：
 % y = myfunction(5);
 y = x.^2;
 end
 ```

## 其他资源

- MATLAB 文档：https://www.mathworks.com/help/matlab/
- GNU Octave 手册： https://docs.octave.org/latest/
- MATLAB Onramp（免费课程）：https://www.mathworks.com/learn/tutorials/matlab-onramp.html
- 文件交换：https://www.mathworks.com/matlabcentral/fileexchange/