# DiffDock 配置参数参考

本文档提供有关所有 DiffDock 配置参数和命令行选项的全面详细信息。

## 模型和检查点设置

### 模型路径
- **`--model_dir`**：包含分数模型检查点的目录
  - 默认： `./workdir/v1.1/score_model`
  - DiffDock-L 模型（当前默认值）

- **`--confidence_model_dir`**：包含置信度模型检查点的目录
  - 默认值：`./workdir/v1.1/confidence_model`

- **`--ckpt`**：评分模型检查点文件的名称
  - 默认值： `best_ema_inference_epoch_model.pt`

- **`--confidence_ckpt`**：置信模型检查点文件的名称
  - 默认：`best_model_epoch75.pt`

### 模型版本标志
- **`--old_score_model`**：使用原始 DiffDock 模型代替DiffDock-L
  - 默认：`false`（使用 DiffDock-L）

- **`--old_filtering_model`**：使用传统置信过滤方法
  - 默认：`true`

## 输入/输出选项

### 输入规格
- **`--protein_path`**：蛋白质PDB文件的路径
  - 示例：`--protein_path protein.pdb`
  - `--protein_sequence`

- **`--protein_sequence`**：用于ESM折叠折叠的氨基酸序列
  - 自动从序列生成蛋白质结构
  - `--protein_path`

- **`--ligand`**的替代方案：配体规格（SMILES 字符串或文件路径）
  - SMILES 字符串：`--ligand "COc(cc1)ccc1C#N"`
  - 文件路径：`--ligand ligand.sdf` 或`.mol2`

- **`--protein_ligand_csv`**：用于批处理的 CSV 文件
  - 必填列：`complex_name`、`protein_path`、`ligand_description`、`protein_sequence`
  - 示例： `--protein_ligand_csv data/protein_ligand_example.csv`

### 输出控制
- **`--out_dir`**：预测的输出目录
  - 示例：`--out_dir results/user_predictions/`

- **`--save_visualisation`**：将预测分子导出为 SDF 文件
  - 启用可视化结果

## 推理参数

### 扩散步骤
- **`--inference_steps`**：计划的推理迭代次数
  - 默认值：`20`
  - 较高的值可能会提高准确性，但会增加运行时间

- **`--actual_steps`**：执行的实际扩散步骤
  - 默认值： `19`

- **`--no_final_step_noise`**：在最终扩散步骤中忽略噪声
  - 默认值：`true`

### 采样设置
- **`--samples_per_complex`**：每个复合体生成的样本数
  - 默认值： `10`
  - 更多样本提供更好的覆盖范围，但会增加计算量

- **`--sigma_schedule`**：噪声计划类型
  - 默认：`expbeta`（指数-beta）

- **`--initial_noise_std_proportion`**：初始噪声标准偏差缩放
  - 默认：`1.46`

### 温度参数

#### 采样温度（控制预测的多样性）
- **`--temp_sampling_tr`**：平移采样温度
  - 默认：`1.17`

- **`--temp_sampling_rot`**：旋转采样温度
  - 默认：`2.06`

- **`--temp_sampling_tor`**：扭转采样温度
  - 默认：`7.04`

#### Psi 角度温度
- **`--temp_psi_tr`**：平移 psi 温度
  - 默认：`0.73`

- **`--temp_psi_rot`**：旋转 psi 温度
  - 默认：`0.90`

- **`--temp_psi_tor`**：扭转 psi温度
  - 默认：`0.59`

#### Sigma 数据温度
- **`--temp_sigma_data_tr`**：平移数据分布缩放
  - 默认：`0.93`

- **`--temp_sigma_data_rot`**：旋转数据分布缩放
  - 默认：`0.75`

- **`--temp_sigma_data_tor`**：扭转数据分布缩放
  - 默认：`0.69`

## 处理选项

### 性能
- **`--batch_size`**：处理批量大小
  - 默认：`10`
  - 较大的值会增加吞吐量，但需要更多内存

- **`--tqdm`**：启用进度条可视化
  - 用于监控长时间运行的作业

### 蛋白质结构
- **`--chain_cutoff`**：要处理的最大蛋白质链数量
  - 示例：`--chain_cutoff 10`
  - 对于大型多链有用复合物

- **`--esm_embeddings_path`**：预先计算的ESM2蛋白质嵌入的路径
  - 通过重用嵌入加速推理
  - 可选优化

### 数据集选项
- **`--split`**：数据集分割以使用(train/test/val)
  - 用于标准基准测试的评估

## 高级标志

### 调试和测试
- **`--no_model`**：禁用模型推理（调试）
  - 默认：`false`

- **`--no_random`**：禁用随机化
  - 默认：`false`
  - 对于再现性测试有用

### 替代采样
- **`--ode`**：使用 ODE 求解器而不是 SDE
  - 默认： `false`
  - 替代采样方法

- **`--different_schedules`**：每个组件使用不同的噪声计划
  - 默认：`false`

### 错误处理
- **`--limit_failures`**：之前允许的最大失败次数停止
  - 默认：`5`

## 配置文件

所有参数都可以在YAML配置文件（通常为`default_inference_args.yaml`）中指定或通过命令行覆盖：

```bash
python -m inference --config default_inference_args.yaml --samples_per_complex 20
```

命令行参数优先于配置文件值.
