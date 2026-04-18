# 机器学习集成

此参考涵盖了 Vaex 的机器学习功能，包括 transformers、编码器、特征工程、模型集成以及在大型数据集上构建 ML 管道。

## 概述

Vaex 提供了与大型数据集无缝协作的全面 ML 框架 (`vaex.ml`)。该框架包括：
- 用于特征缩放和工程的Transformers
- 分类变量的编码器
- 降维(PCA)
- 聚类算法
- 与scikit-learn、XGBoost、LightGBM、CatBoost和Keras集成
- 生产部署的状态管理

* *主要优点：**所有转换都会创建虚拟列，因此预处理不会增加内存使用量。

## 功能缩放

### 标准缩放器

```python
import vaex
import vaex.ml

df = vaex.open('data.hdf5')

# Fit standard scaler
scaler = vaex.ml.StandardScaler(features=['age', 'income', 'score'])
scaler.fit(df)

# Transform (creates virtual columns)
df = scaler.transform(df)

# Scaled columns created as: 'standard_scaled_age', 'standard_scaled_income', etc.
print(df.column_names)
```

### MinMax定标器

```python
# Scale to [0, 1] range
minmax_scaler = vaex.ml.MinMaxScaler(features=['age', 'income'])
minmax_scaler.fit(df)
df = minmax_scaler.transform(df)

# Custom range
minmax_scaler = vaex.ml.MinMaxScaler(
    features=['age'],
    feature_range=(-1, 1)
)
```

### MaxAbs定标器

```python
# Scale by maximum absolute value
maxabs_scaler = vaex.ml.MaxAbsScaler(features=['values'])
maxabs_scaler.fit(df)
df = maxabs_scaler.transform(df)
```

### 稳健定标器

```python
# Scale using median and IQR (robust to outliers)
robust_scaler = vaex.ml.RobustScaler(features=['income', 'age'])
robust_scaler.fit(df)
df = robust_scaler.transform(df)
```

## 分类编码

### 标签编码器

```python
# Encode categorical to integers
label_encoder = vaex.ml.LabelEncoder(features=['category', 'region'])
label_encoder.fit(df)
df = label_encoder.transform(df)

# Creates: 'label_encoded_category', 'label_encoded_region'
```

### 单热编码器

```python
# Create binary columns for each category
onehot = vaex.ml.OneHotEncoder(features=['category'])
onehot.fit(df)
df = onehot.transform(df)

# Creates columns like: 'category_A', 'category_B', 'category_C'

# Control prefix
onehot = vaex.ml.OneHotEncoder(
    features=['category'],
    prefix='cat_'
)
```

### 频率编码器

```python
# Encode by category frequency
freq_encoder = vaex.ml.FrequencyEncoder(features=['category'])
freq_encoder.fit(df)
df = freq_encoder.transform(df)

# Each category replaced by its frequency in the dataset
```

### 目标编码器(均值编码器)

```python
# Encode category by target mean (for supervised learning)
target_encoder = vaex.ml.TargetEncoder(
    features=['category'],
    target='target_variable'
)
target_encoder.fit(df)
df = target_encoder.transform(df)

# Handles unseen categories with global mean
```

### 证据权重编码器

```python
# Encode for binary classification
woe_encoder = vaex.ml.WeightOfEvidenceEncoder(
    features=['category'],
    target='binary_target'
)
woe_encoder.fit(df)
df = woe_encoder.transform(df)
```

## 特征工程

### 分箱/离散化

```python
# Bin continuous variable into discrete bins
binner = vaex.ml.Discretizer(
    features=['age'],
    n_bins=5,
    strategy='uniform'  # or 'quantile'
)
binner.fit(df)
df = binner.transform(df)
```

### 循环变换

```python
# Transform cyclic features (hour, day, month)
cyclic = vaex.ml.CycleTransformer(
    features=['hour', 'day_of_week'],
    n=[24, 7]  # Period for each feature
)
cyclic.fit(df)
df = cyclic.transform(df)

# Creates sin and cos components for each feature
```

### PCA（主成分分析）

```python
# Dimensionality reduction
pca = vaex.ml.PCA(
    features=['feature1', 'feature2', 'feature3', 'feature4'],
    n_components=2
)
pca.fit(df)
df = pca.transform(df)

# Creates: 'PCA_0', 'PCA_1'

# Access explained variance
print(pca.explained_variance_ratio_)
```

### 随机投影

```python
# Fast dimensionality reduction
projector = vaex.ml.RandomProjection(
    features=['x1', 'x2', 'x3', 'x4', 'x5'],
    n_components=3
)
projector.fit(df)
df = projector.transform(df)
```

## 聚类

### K-Means

```python
# Cluster data
kmeans = vaex.ml.KMeans(
    features=['feature1', 'feature2', 'feature3'],
    n_clusters=5,
    max_iter=100
)
kmeans.fit(df)
df = kmeans.transform(df)

# Creates 'prediction' column with cluster labels

# Access cluster centers
print(kmeans.cluster_centers_)
```

## 与外部库集成

### Scikit-Learn

```python
from sklearn.ensemble import RandomForestClassifier
import vaex.ml

# Prepare data
train_df = df[df.split == 'train']
test_df = df[df.split == 'test']

# Features and target
features = ['feature1', 'feature2', 'feature3']
target = 'target'

# Train scikit-learn model
model = RandomForestClassifier(n_estimators=100)

# Fit using Vaex data
sklearn_model = vaex.ml.sklearn.Predictor(
    features=features,
    target=target,
    model=model,
    prediction_name='rf_prediction'
)
sklearn_model.fit(train_df)

# Predict (creates virtual column)
test_df = sklearn_model.transform(test_df)

# Access predictions
predictions = test_df.rf_prediction.values
```

### XGBoost

```python
import xgboost as xgb
import vaex.ml

# Create XGBoost booster
booster = vaex.ml.xgboost.XGBoostModel(
    features=features,
    target=target,
    prediction_name='xgb_pred'
)

# Configure parameters
params = {
    'max_depth': 6,
    'eta': 0.1,
    'objective': 'reg:squarederror',
    'eval_metric': 'rmse'
}

# Train
booster.fit(
    df=train_df,
    params=params,
    num_boost_round=100
)

# Predict
test_df = booster.transform(test_df)
```

### LightGBM

```python
import lightgbm as lgb
import vaex.ml

# Create LightGBM model
lgb_model = vaex.ml.lightgbm.LightGBMModel(
    features=features,
    target=target,
    prediction_name='lgb_pred'
)

# Parameters
params = {
    'objective': 'binary',
    'metric': 'auc',
    'num_leaves': 31,
    'learning_rate': 0.05
}

# Train
lgb_model.fit(
    df=train_df,
    params=params,
    num_boost_round=100
)

# Predict
test_df = lgb_model.transform(test_df)
```

### CatBoost

```python
from catboost import CatBoostClassifier
import vaex.ml

# Create CatBoost model
catboost_model = vaex.ml.catboost.CatBoostModel(
    features=features,
    target=target,
    prediction_name='catboost_pred'
)

# Parameters
params = {
    'iterations': 100,
    'depth': 6,
    'learning_rate': 0.1,
    'loss_function': 'Logloss'
}

# Train
catboost_model.fit(train_df, **params)

# Predict
test_df = catboost_model.transform(test_df)
```

### Keras/TensorFlow

```python
from tensorflow import keras
import vaex.ml

# Define Keras model
def create_model(input_dim):
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(input_dim,)),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Wrap in Vaex
keras_model = vaex.ml.keras.KerasModel(
    features=features,
    target=target,
    model=create_model(len(features)),
    prediction_name='keras_pred'
)

# Train
keras_model.fit(
    train_df,
    epochs=10,
    batch_size=10000
)

# Predict
test_df = keras_model.transform(test_df)
```

## 构建机器学习管道

### 顺序管道

```python
import vaex.ml

# Create preprocessing pipeline
pipeline = []

# Step 1: Encode categorical
label_enc = vaex.ml.LabelEncoder(features=['category'])
pipeline.append(label_enc)

# Step 2: Scale features
scaler = vaex.ml.StandardScaler(features=['age', 'income'])
pipeline.append(scaler)

# Step 3: PCA
pca = vaex.ml.PCA(features=['age', 'income'], n_components=2)
pipeline.append(pca)

# Fit pipeline
for step in pipeline:
    step.fit(df)
    df = step.transform(df)

# Or use fit_transform
for step in pipeline:
    df = step.fit_transform(df)
```

### 完整的机器学习管道

```python
import vaex
import vaex.ml
from sklearn.ensemble import RandomForestClassifier

# Load data
df = vaex.open('data.hdf5')

# Split data
train_df = df[df.year < 2020]
test_df = df[df.year >= 2020]

# Define pipeline
# 1. Categorical encoding
cat_encoder = vaex.ml.LabelEncoder(features=['category', 'region'])

# 2. Feature scaling
scaler = vaex.ml.StandardScaler(features=['age', 'income', 'score'])

# 3. Model
features = ['label_encoded_category', 'label_encoded_region',
            'standard_scaled_age', 'standard_scaled_income', 'standard_scaled_score']
model = vaex.ml.sklearn.Predictor(
    features=features,
    target='target',
    model=RandomForestClassifier(n_estimators=100),
    prediction_name='prediction'
)

# Fit pipeline
train_df = cat_encoder.fit_transform(train_df)
train_df = scaler.fit_transform(train_df)
model.fit(train_df)

# Apply to test
test_df = cat_encoder.transform(test_df)
test_df = scaler.transform(test_df)
test_df = model.transform(test_df)

# Evaluate
accuracy = (test_df.prediction == test_df.target).mean()
print(f"Accuracy: {accuracy:.4f}")
```

## 状态管理和部署

### 保存管道状态

```python
# After fitting all transformers and model
# Save the entire pipeline state
train_df.state_write('pipeline_state.json')

# In production: Load fresh data and apply transformations
prod_df = vaex.open('new_data.hdf5')
prod_df.state_load('pipeline_state.json')

# All transformations and models are applied
predictions = prod_df.prediction.values
```

### 在数据帧之间传输状态

```python
# Fit on training data
train_df = cat_encoder.fit_transform(train_df)
train_df = scaler.fit_transform(train_df)
model.fit(train_df)

# Save state
train_df.state_write('model_state.json')

# Apply to test data
test_df.state_load('model_state.json')

# Apply to validation data
val_df.state_load('model_state.json')
```

### 通过转换导出

```python
# Export DataFrame with all virtual columns materialized
df_with_features = df.copy()
df_with_features = df_with_features.materialize()
df_with_features.export_hdf5('processed_data.hdf5')
```

## 模型评估

### 分类指标

```python
# Binary classification
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score

y_true = test_df.target.values
y_pred = test_df.prediction.values
y_proba = test_df.prediction_proba.values if hasattr(test_df, 'prediction_proba') else None

accuracy = accuracy_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
if y_proba is not None:
    auc = roc_auc_score(y_true, y_proba)

print(f"Accuracy: {accuracy:.4f}")
print(f"F1 Score: {f1:.4f}")
if y_proba is not None:
    print(f"AUC-ROC: {auc:.4f}")
```

### 回归指标

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

y_true = test_df.target.values
y_pred = test_df.prediction.values

mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)

print(f"RMSE: {rmse:.4f}")
print(f"MAE: {mae:.4f}")
print(f"R²: {r2:.4f}")
```

### 交叉验证

```python
# Manual K-fold cross-validation
import numpy as np

# Create fold indices
df['fold'] = np.random.randint(0, 5, len(df))

results = []
for fold in range(5):
    train = df[df.fold != fold]
    val = df[df.fold == fold]

    # Fit pipeline
    train = encoder.fit_transform(train)
    train = scaler.fit_transform(train)
    model.fit(train)

    # Validate
    val = encoder.transform(val)
    val = scaler.transform(val)
    val = model.transform(val)

    accuracy = (val.prediction == val.target).mean()
    results.append(accuracy)

print(f"CV Accuracy: {np.mean(results):.4f} ± {np.std(results):.4f}")
```

## 特征选择

### 基于相关性的

```python
# Compute correlations with target
correlations = {}
for feature in features:
    corr = df.correlation(df[feature], df.target)
    correlations[feature] = abs(corr)

# Sort by correlation
sorted_features = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
top_features = [f[0] for f in sorted_features[:10]]

print("Top 10 features:", top_features)
```

#### 基于方差的

```python
# Remove low-variance features
feature_variances = {}
for feature in features:
    var = df[feature].std() ** 2
    feature_variances[feature] = var

# Keep features with variance above threshold
threshold = 0.01
selected_features = [f for f, v in feature_variances.items() if v > threshold]
```

## 处理不平衡数据

### 类别权重

```python
# Compute class weights
class_counts = df.groupby('target', agg='count')
total = len(df)
weights = {
    0: total / (2 * class_counts[0]),
    1: total / (2 * class_counts[1])
}

# Use in model
model = RandomForestClassifier(class_weight=weights)
```

### 欠采样

```python
# Undersample majority class
minority_count = df[df.target == 1].count()

# Sample from majority class
majority_sampled = df[df.target == 0].sample(n=minority_count)
minority_all = df[df.target == 1]

# Combine
df_balanced = vaex.concat([majority_sampled, minority_all])
```

### 过采样（SMOTE替代）

```python
# Duplicate minority class samples
minority = df[df.target == 1]
majority = df[df.target == 0]

# Replicate minority
minority_oversampled = vaex.concat([minority] * 5)

# Combine
df_balanced = vaex.concat([majority, minority_oversampled])
```

## 常见模式

### 模式：端到端分类管道

```python
import vaex
import vaex.ml
from sklearn.ensemble import RandomForestClassifier

# Load and split
df = vaex.open('data.hdf5')
train = df[df.split == 'train']
test = df[df.split == 'test']

# Preprocessing
# Categorical encoding
cat_enc = vaex.ml.LabelEncoder(features=['cat1', 'cat2'])
train = cat_enc.fit_transform(train)

# Feature scaling
scaler = vaex.ml.StandardScaler(features=['num1', 'num2', 'num3'])
train = scaler.fit_transform(train)

# Model training
features = ['label_encoded_cat1', 'label_encoded_cat2',
            'standard_scaled_num1', 'standard_scaled_num2', 'standard_scaled_num3']
model = vaex.ml.sklearn.Predictor(
    features=features,
    target='target',
    model=RandomForestClassifier(n_estimators=100)
)
model.fit(train)

# Save state
train.state_write('production_pipeline.json')

# Apply to test
test.state_load('production_pipeline.json')

# Evaluate
accuracy = (test.prediction == test.target).mean()
print(f"Test Accuracy: {accuracy:.4f}")
```

### 模式：特征工程管道

```python
# Create rich features
df['age_squared'] = df.age ** 2
df['income_log'] = df.income.log()
df['age_income_interaction'] = df.age * df.income

# Binning
df['age_bin'] = df.age.digitize([0, 18, 30, 50, 65, 100])

# Cyclic features
df['hour_sin'] = (2 * np.pi * df.hour / 24).sin()
df['hour_cos'] = (2 * np.pi * df.hour / 24).cos()

# Aggregate features
avg_by_category = df.groupby('category').agg({'income': 'mean'})
# Join back to create feature
df = df.join(avg_by_category, on='category', rsuffix='_category_mean')
```

## 最佳实践

1. **使用虚拟列** - Transformers 创建虚拟列（无内存开销）
2. **保存状态文件** - 实现轻松部署和复制
3. **批量操作** - 计算多个特征时使用 `delay=True`
4. **特征缩放** - 始终在 PCA 或基于距离的算法
5 之前缩放特征。 **编码类别** - 使用适当的编码器（标签、one-hot、目标）
6. **交叉验证** - 始终验证保留的数据
7. **监控内存** - 使用 `df.byte_size()`
8 检查内存使用情况。 **导出检查点** - 将中间结果保存在长管道中

## 相关资源

 - 对于数据预处理：请参阅`data_processing.md`
  - 对于性能优化：请参阅`performance.md`
  - 对于DataFrame操作：请参阅`core_dataframes.md`
