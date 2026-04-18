# TimesFM API 参考

## 模型类

### `timesfm.TimesFM_2p5_200M_torch`

TimesFM 2.5 的主要模型类（200M 参数，PyTorch 后端）。

#### `from_pretrained()`

```python
model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(
    "google/timesfm-2.5-200m-pytorch",
    cache_dir=None,         # Optional: custom cache directory
    force_download=True,    # Re-download even if cached
)
```

|参数|类型 |默认|描述 |
| --------- | ---- | -------- | ----------- |
| `model_id` | STR | `"google/timesfm-2.5-200m-pytorch"` |抱脸模特ID |
| `revision` |字符串\|无 |无 |具体型号改版|
| `cache_dir` |字符串\|路径\|无 |无 |自定义缓存目录|
| `force_download` |布尔 |真实|强制重新下载权重|

* *返回**：初始化的`TimesFM_2p5_200M_torch`实例（尚未编译）。

#### `compile()`

使用给定的预测配置编译模型。 **必须在 `forecast()` 之前调用。**

```python
model.compile(
    timesfm.ForecastConfig(
        max_context=1024,
        max_horizon=256,
        normalize_inputs=True,
        per_core_batch_size=32,
        use_continuous_quantile_head=True,
        force_flip_invariance=True,
        infer_is_positive=True,
        fix_quantile_crossing=True,
    )
)
```

* *引发**：无任何内容（但如果未编译，`forecast()` 将引发 `RuntimeError`）。

#### `forecast()`

在一个或一个上运行推理更多时间序列。

```python
point_forecast, quantile_forecast = model.forecast(
    horizon=24,
    inputs=[array1, array2, ...],
)
```

|参数|类型 |描述 |
| --------- | ---- | ----------- |
| `horizon` |整数 |预测未来步数|
| `inputs` |列表[np.ndarray] |一维numpy数组列表（每个都是时间序列）|

* *返回**：`tuple[np.ndarray, np.ndarray]`

- `point_forecast`：形状 `(batch_size, horizon)` - 中位数（0.5分位数）
- `quantile_forecast`：形状`(batch_size, horizon, 10)` — [mean, q10, q20, ..., q90]

* *Raises**：如果未编译模型，则为 `RuntimeError`。

* *关键行为**：

- 自动删除前导 NaN 值
- 内部 NaN 值呈线性interpolated
- 长于 `max_context` 的系列被截断（最后使用 `max_context` 点） 
- 短于 `max_context` 的系列被填充

#### `forecast_with_covariates()`

使用外生变量运行推理（需要`timesfm[xreg]`).

```python
point, quantiles = model.forecast_with_covariates(
    inputs=inputs,
    dynamic_numerical_covariates={"temp": [temp_array1, temp_array2]},
    dynamic_categorical_covariates={"dow": [dow_array1, dow_array2]},
    static_categorical_covariates={"region": ["east", "west"]},
    xreg_mode="xreg + timesfm",
)
```

|参数|类型 |描述|
| --------- | ---- | ----------- |
| `inputs` |列表[np.ndarray] |目标时间序列|
| `dynamic_numerical_covariates` |字典[str, 列表[np.ndarray]] |时变数值特征|
| `dynamic_categorical_covariates` |字典[str, 列表[np.ndarray]] |时变分类特征|
| `static_categorical_covariates` |字典[str，列表[str]] |每个系列的固定分类特征 |
| `xreg_mode` | STR | `"xreg + timesfm"` 或 `"timesfm + xreg"` |

* *注意**：每个系列的动态协变量必须具有长度 `context + horizon`。

- --

## `timesfm.ForecastConfig`

控制所有预测的不可变数据类behavior.

```python
@dataclasses.dataclass(frozen=True)
class ForecastConfig:
    max_context: int = 0
    max_horizon: int = 0
    normalize_inputs: bool = False
    per_core_batch_size: int = 1
    use_continuous_quantile_head: bool = False
    force_flip_invariance: bool = True
    infer_is_positive: bool = True
    fix_quantile_crossing: bool = False
    return_backcast: bool = False
    quantiles: list[float] = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    decode_index: int = 5
```

### 参数详细信息

#### `max_context` (int, default=0)

用作上下文的历史时间点的最大数量。

- **0**：使用模型支持的最大上下文（16,384 v2.5)
- **N**：截断序列到最后 N 个点
- **最佳实践**：设置为最长序列的长度，或速度为 512–2048

#### `max_horizon`（int，默认=0）

最大预测范围。

- **0**：使用模型的最大值
- **N**：预测最多N步（仍然可以调用`forecast(horizon=M)`，其中M ≤ N）
- **最佳实践**：设置为您预期的最大预测长度

#### `normalize_inputs`（bool，默认=False）

是否进行z-归一化

- **True** （推荐）：将每个系列标准化为零均值，单位方差
- **False**：直接传递原始值
- **当 False 可以**：仅当您的系列已经标准化或非常接近比例 1.0

#### `per_core_batch_size` (int,默认=1)

每批次中每个设备处理的系列数。

- 增加吞吐量，如果OOM则减少
- 请参阅`references/system_requirements.md`了解硬件推荐值

#### `use_continuous_quantile_head`（布尔，默认=False）

使用 30M 参数连续分位数头进行更好的间隔校准。

- **True**（推荐）：更准确的预测间隔，特别是对于较长的视野
- **False**：使用固定分位数桶（更快但不太准确的间隔）

#### `force_flip_invariance`（布尔，默认=True）

确保模型满足 `f(-x) = -f(x)`.

- **True** （推荐）：数学一致性 - 预测对符号翻转保持不变
- **False**：稍快但可能产生不对称预测

#### `infer_is_positive`（bool，默认=True）

自动检测是否所有输入值为正且钳制预测 ≥ 0.

- **True**：对于销售、需求、计数、价格、数量来说是安全的
- **False**：对于温度、回报、PnL 以及任何可能为负的序列来说是必需的

#### `fix_quantile_crossing`（布尔值，默认=False）

后处理分位数以确保单调性(q10 ≤ q20 ≤ ... ≤ q90).

- **True** (推荐): 保证分位数有序
- **False**: 速度稍快，但分位数偶尔可能交叉

#### `return_backcast` (bool, default=False)

返回除了预测之外，模型还对输入进行重建（反向预测）。

- **True**：用于协变量工作流程和诊断
- **False**：仅返回预测

- --

## 可用模型检查点

|型号 ID |版本 |参数|后端|上下文|
| -------- | -------- | ------ | -------- | -------- |
| `google/timesfm-2.5-200m-pytorch` | 2.5 | 2.5 200M | PyTorch | 16,384 |
| `google/timesfm-2.5-200m-flax` | 2.5 | 2.5 200M | JAX/亚麻| 16,384 |
| `google/timesfm-2.5-200m-transformers` | 2.5 | 2.5 200M | Transformers | 16,384 |
| `google/timesfm-2.0-500m-pytorch` | 2.0 | 500M | PyTorch | 2,048 |
| `google/timesfm-2.0-500m-jax` | 2.0 | 500M |贾克斯| 2,048 |
| `google/timesfm-1.0-200m-pytorch` | 1.0 | 200M | PyTorch | 2,048 |
| `google/timesfm-1.0-200m` | 1.0 | 200M |贾克斯| 2,048 |

- --

## 输出形状参考

|输出|形状|描述 |
| ------ | -----| ----------- |
| `point_forecast` | `(B, H)` | B 系列、H 步的中位预测 |
| `quantile_forecast` | `(B, H, 10)` |全分位数分布|
| `quantile_forecast[:,:,0]` | `(B, H)` |平均值 |
| `quantile_forecast[:,:,1]` | `(B, H)` |第 10 个百分位数 |
| `quantile_forecast[:,:,5]` | `(B, H)` |第 50 个百分位（= point_forecast）|
| `quantile_forecast[:,:,9]` | `(B, H)` | 90% |

其中 `B` = 批量大小（输入系列数），`H` = 预测范围。

- --

## 错误处理

|错误 |原因 |修复|
| -----| -----| ---|
| `RuntimeError: Model is not compiled` |在`compile()`之前叫`forecast()` |先拨打`model.compile(ForecastConfig(...))`|
| `torch.cuda.OutOfMemoryError` |批次对于 GPU 来说太大 |减少`per_core_batch_size` |
| `ValueError: inputs must be list` |传递数组而不是列表 |包含在列表中：`[array]` |
| `HfHubHTTPError` |下载失败 |检查网络，将`HF_HOME`设置为可写目录|
