# FluidSim 安装

## 要求

- Python >= 3.9
- 推荐虚拟环境

## 安装方法

### 基本安装

使用安装fluidsim uv:

XQBLOCK0QXZ
### 具有 FFT 支持（伪谱求解器所需）

大多数 fluidsim 求解器使用基于傅里叶的方法并需要 FFT 库：

```bash
uv pip install "fluidsim[fft]"
```

这将安装 Fluidfft 和 pyfftw依赖项.

### 具有MPI和FFT（用于并行模拟）

用于高性能并行计算：

```bash
uv pip install "fluidsim[fft,mpi]"
```

注：这会触发mpi4py的本地编译。

## 环境配置

### 输出目录

设置环境变量来控制模拟数据的存储位置：

```bash
export FLUIDSIM_PATH=/path/to/simulation/outputs
export FLUIDDYN_PATH_SCRATCH=/path/to/working/directory
```

### FFT方法选择

指定FFT实现（可选）：

```bash
export FLUIDSIM_TYPE_FFT2D=fft2d.with_fftw
export FLUIDSIM_TYPE_FFT3D=fft3d.with_fftw
```

## 验证

测试安装：

```bash
pytest --pyargs fluidsim
```

## 无需身份验证

FluidSim 不需要 API 密钥或身份验证令牌。
