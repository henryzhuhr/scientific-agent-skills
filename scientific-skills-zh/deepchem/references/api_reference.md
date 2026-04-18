# DeepChem API 参考

本文档提供了 DeepChem 核心 API 的全面参考，按功能组织。

## 数据处理

### 数据加载器

#### 文件格式加载器
- **CSVLoader**：具有可自定义功能的从 CSV 文件加载表格数据处理
- **UserCSVLoader**：用户定义的CSV加载，具有灵活的列规格
- **SDFLoader**：处理分子结构文件（SDF格式）
- **JsonLoader**：导入JSON结构的数据集
- **ImageLoader**：加载计算机视觉任务的图像数据

#### 生物数据Loaders
- **FASTALoader**：处理FASTA格式的蛋白质/DNA序列
- **FASTQLoader**：处理带有质量分数的FASTQ测序数据
- **SAMLoader/BAMLoader/CRAMLoader**：支持序列比对格式

#### 专用Loaders
- **DFTYamlLoader**：处理密度泛函理论计算数据
- **InMemoryLoader**：直接从Python对象加载数据

### 数据集类

- **NumpyDataset**：包装NumPy数组以进行内存中数据操作
- **DiskDataset**：管理存储在磁盘上的较大数据集，减少内存开销
- **ImageDataset**：用于基于图像的ML任务的专用容器

### 数据分割器

#### 通用分割器
- **RandomSplitter**：随机数据集分区
- **IndexSplitter**：按指定索引分割
- **SpecifiedSplitter**：使用预定义分割
- **RandomStratifiedSplitter**：分层随机分割
- **SingletaskStratifiedSplitter**：单任务分层分割
- **TaskSplitter**：多任务场景分割

#### 分子特异性拆分器
- **ScaffoldSplitter**：通过结构支架划分分子（防止数据泄露）
- **ButinaSplitter**：基于聚类的分子拆分
- **FingerprintSplitter**：根据分子指纹拆分
- **MaxMinSplitter**：最大化之间的多样性训练/测试集
- **MolecularWeightSplitter**：按分子量属性分割

* *最佳实践**：对于药物发现任务，使用ScaffoldSplitter来防止相似分子结构上的过度拟合。

### Transformers

#### 归一化
- **NormalizationTransformer**：标准归一化（平均值=0， std=1)
- **MinMaxTransformer**：将特征缩放到 [0,1]范围
- **LogTransformer**：应用对数变换
- **PowerTransformer**：Box-Cox 和 Yeo-Johnson 变换
- **CDFTransformer**：累积分布函数归一化

#### 特定任务
- **BalancingTransformer**：地址类不平衡
- **FeaturizationTransformer**：应用动态特征工程
- **CoulombFitTransformer**：量子化学特定
- **DAGTransformer**：有向非循环图转换
- **RxnSplitTransformer**：化学反应预处理

## 分子特征化器

### 基于图的特征化器
将它们与图神经网络（GCN、MPNN 等）一起使用：

- **ConvMolFeaturizer**：图卷积的图表示网络
- **WeaveFeaturizer**：“编织”图嵌入
- **MolGraphConvFeaturizer**：图卷积就绪表示
- **EquivariantGraphFeaturizer**：保持几何不变性
- **DMPNNFeaturizer**：定向消息传递神经网络输入
- **GroverFeaturizer**：预训练的分子嵌入

### 基于指纹的特征化器
将其与传统ML（随机森林、SVM、XGBoost）结合使用：

- **MACCSKeysFingerprint**：167 位结构密钥
- **CircularFingerprint**：扩展连接指纹（摩根指纹）
  - 参数：`radius`（默认 2）、`size`（默认 2048）、`useChirality`（默认 False）
- **PubChemFingerprint**：881 位结构描述符
- **Mol2VecFingerprint**：学习的分子向量表示

### 描述符特征器
直接计算分子属性：

- **RDKitDescriptors**：约200 个分子描述符（MW、LogP、H 供体、 H-受体、TPSA 等）
- **MordredDescriptors**：综合结构和物理化学描述符
- **库仑矩阵**：3D 结构的原子间距离矩阵

### 基于序列的特征化器
用于循环网络和transformers:

- **SmilesToSeq**：将 SMILES 字符串转换为序列
- **SmilesToImage**：从 SMILES 生成 2D 图像表示
- **RawFeaturizer**：传递未更改的原始分子数据

### 选择指南

|使用案例|推荐特征器 |型号|
|----------|------------------------|------------|
|图神经网络 | ConvMolFeaturizer、MolGraphConvFeaturizer | GCN、MPNN、GAT |
|传统机器学习 | CircularFingerprint、RDKitDescriptors |随机森林、XGBoost、SVM |
|深度学习（非图）|圆形指纹、Mol2VecFingerprint |密集网络，CNN |
|序列模型|微笑到序列 | LSTM、GRU、变压器 |
| 3D 分子结构 |库仑矩阵|专业3D模型|
|快速基线| RDKit 描述符 |线性、岭、套索 |

## 模型

### Scikit-Learn 集成
- **SklearnModel**：任何 scikit-learn 算法的包装
  - 用法：`SklearnModel(model=RandomForestRegressor())`

### 渐变Boosting
- **GBDTModel**：梯度提升决策树（XGBoost、LightGBM）

### PyTorch 模型

#### 分子特性预测
- **多任务回归器**：具有共享表示的多任务回归
- **多任务分类器**：多任务分类
- **多任务FitTransformRegressor**：具有学习变换的回归
- **GCN模型**：图卷积网络
- **GATModel**：图注意力网络
- **AttentiveFPModel**：注意力指纹网络
- **DMPNNModel**：定向消息传递神经网络
- **GroverModel**：GROVER 预训练变压器
- **MATModel**：分子注意力变压器

#### 材料Science
- **CGCNN模型**：晶体图卷积网络
- **MEGNetModel**：材料图网络
- **LCNN模型**：材料的晶格CNN

#### 生成模型
- **GAN模型**：生成对抗网络
- **WGANModel**：Wasserstein GAN
- **BasicMolGANModel**：分子 GAN
- **LSTMGenerator**：基于 LSTM 的分子生成
- **SeqToSeqModel**：序列到序列模型

#### 物理信息模型
- **PINNModel**：物理信息神经网络
- **HNNModel**：哈密顿神经网络
- **LNN**：拉格朗日神经网络
- **FNOModel**：傅立叶神经算子

#### 计算机视觉
- **CNN**：卷积神经网络网络
- **UNetModel**：用于分割的U-Net架构
- **InceptionV3Model**：预训练的Inception v3
- **MobileNetV2Model**：轻量级移动网络

### Hugging Face Models

- **HuggingFaceModel**：HF的通用包装器Transformer
- **Chemberta**：用于分子特性预测的化学 BERT
- **MoLFormer**：分子变压器架构
- **ProtBERT**：蛋白质序列 BERT
- **DeepAbLLM**：抗体大语言模型

### 模型选择指南

|任务|推荐型号 |特征化器|
|------|--------------------|------------|
|小数据集（<1000 个样本）| SklearnModel（随机森林）|圆形指纹|
|中等数据集 (1K-100K) | GBDT模型或多任务回归器| CircularFingerprint 或 ConvMolFeaturizer |
|大型数据集 (>100K) | GCN 模型、AttentiveFP 模型或 DMPNN | MolGraphConvFeaturizer |
|迁移学习 | GroverModel，Chemberta，MoL前任 |特定型号|
|材料特性| CGCNN模型、MEGNet模型 |基于结构|
|分子生成| BasicMolGAN 模型、LSTM 生成器 | SmilesToSeq |
|蛋白质序列|普特伯特 |基于序列 |

## MoleculeNet 数据集

通过 `dc.molnet.load_*()` 函数快速访问 30 多个基准数据集。

### 分类数据集
- **load_bace()**：BACE-1 抑制剂（二元分类）
- **load_bbbp()**：血脑屏障穿透
- **load_clintox()**：临床毒性
- **load_hiv()**：HIV 抑制活性
- **load_muv()**：PubChem BioAssay（具有挑战性，稀疏）
- **load_pcba()**：PubChem 筛选data
- **load_sider()**：药物不良反应（多标签）
- **load_tox21()**：12 种毒性测定（多任务）
- **load_toxcast()**：EPA ToxCast 筛选

### 回归数据集
- **load_delaney()**：水溶性 (ESOL)
- **load_freesolv()**：溶剂化自由能
- **load_lipo()**：亲油性（辛醇-水分配）
- **load_qm7/qm8/qm9()**：量子力学性能
- **load_hopv()**：有机光伏特性

### 蛋白质-配体结合
- **load_pdbbind()**：结合亲和力数据

### 材料科学
- **load_perovskite()**：钙钛矿稳定性
- **load_mp_formation_energy()**：材料项目形成能
- **load_mp_metalicity()**：金属与非金属分类
- **load_bandgap()**：电子带隙预测

### 化学反应
- **load_uspto()**：USPTO 反应数据集

### 使用模式
```python
tasks, datasets, transformers = dc.molnet.load_bbbp(
    featurizer='GraphConv',  # or 'ECFP', 'GraphConv', 'Weave', etc.
    splitter='scaffold',      # or 'random', 'stratified', etc.
    reload=False              # set True to skip caching
)
train, valid, test = datasets
```

## 指标

`dc.metrics` 中提供的常用评估指标：

### 分类指标
- **roc_auc_score**：ROC 曲线下的面积（二元/多类）
- **prc_auc_score**：精确回忆曲线下的面积
- **accuracy_score**：分类精度
- **balanced_accuracy_score**：不平衡数据集的平衡精度
- **recall_score**：灵敏度/召回
- ** precision_score**：Precision
- **f1_score**：F1 分数

### 回归指标
- **mean_absolute_error**：MAE
- **mean_squared_error**： MSE
- **root_mean_squared_error**：RMSE
- **r2_score**：R² 决定系数
- **pearson_r2_score**：皮尔逊相关
- **spearman_correlation**：斯皮尔曼等级相关

### 多任务指标
大多数指标支持通过对任务进行平均来进行多任务评估。

## 训练模式

标准DeepChem工作流程：

```python
# 1. Load data
loader = dc.data.CSVLoader(tasks=['task1'], feature_field='smiles',
                           featurizer=dc.feat.CircularFingerprint())
dataset = loader.create_dataset('data.csv')

# 2. Split data
splitter = dc.splits.ScaffoldSplitter()
train, valid, test = splitter.train_valid_test_split(dataset)

# 3. Transform data (optional)
transformers = [dc.trans.NormalizationTransformer(dataset=train)]
for transformer in transformers:
    train = transformer.transform(train)
    valid = transformer.transform(valid)
    test = transformer.transform(test)

# 4. Create and train model
model = dc.models.MultitaskRegressor(n_tasks=1, n_features=2048, layer_sizes=[1000])
model.fit(train, nb_epoch=50)

# 5. Evaluate
metric = dc.metrics.Metric(dc.metrics.r2_score)
train_score = model.evaluate(train, [metric])
test_score = model.evaluate(test, [metric])
```

## 常见模式

### 模式1：快速基线MoleculeNet
```python
tasks, datasets, transformers = dc.molnet.load_tox21(featurizer='ECFP')
train, valid, test = datasets
model = dc.models.MultitaskClassifier(n_tasks=len(tasks), n_features=1024)
model.fit(train)
```

### 模式 2：使用图网络自定义数据
```python
featurizer = dc.feat.MolGraphConvFeaturizer()
loader = dc.data.CSVLoader(tasks=['activity'], feature_field='smiles',
                           featurizer=featurizer)
dataset = loader.create_dataset('my_data.csv')
train, test = dc.splits.RandomSplitter().train_test_split(dataset)
model = dc.models.GCNModel(mode='classification', n_tasks=1)
model.fit(train)
```

### 模式 3：使用预训练模型进行迁移学习
```python
model = dc.models.GroverModel(task='classification', n_tasks=1)
model.fit(train_dataset)
predictions = model.predict(test_dataset)
```
