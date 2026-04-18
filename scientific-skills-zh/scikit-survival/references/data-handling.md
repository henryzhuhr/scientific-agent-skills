# 数据处理和预处理

## 了解生存数据

### scikit-survival中的Surv对象

生存数据使用具有两个字段的结构化数组表示：
- **event**：指示事件是否发生（True）或被审查（False）的布尔值
- **time**：事件发生的时间或审查

```python
from sksurv.util import Surv

# Create survival outcome from separate arrays
event = np.array([True, False, True, False, True])
time = np.array([5.2, 10.1, 3.7, 8.9, 6.3])

y = Surv.from_arrays(event=event, time=time)
print(y.dtype)  # [('event', '?'), ('time', '<f8')]
```

### 审查类型

* *正确审查**（最常见）：
- 受试者在研究结束时没有经历事件
- 受试者失去后续
- 受试者退出研究

* *左删失**：
- 在观察开始之前发生的事件
- 实践中很少见

* *间隔删失**：
- 在已知时间间隔内发生的事件
- 需要专门的方法

scikit-生存主要处理右删失数据。

## 加载数据

#### 内置数据集

```python
from sksurv.datasets import (
    load_aids,
    load_breast_cancer,
    load_gbsg2,
    load_veterans_lung_cancer,
    load_whas500
)

# Load dataset
X, y = load_breast_cancer()

# X is pandas DataFrame with features
# y is structured array with 'event' and 'time'
print(f"Features shape: {X.shape}")
print(f"Number of events: {y['event'].sum()}")
print(f"Censoring rate: {1 - y['event'].mean():.2%}")
```

#### 加载自定义数据

#### 来自 Pandas DataFrame

```python
import pandas as pd
from sksurv.util import Surv

# Load data
df = pd.read_csv('survival_data.csv')

# Separate features and outcome
X = df.drop(['time', 'event'], axis=1)
y = Surv.from_dataframe('event', 'time', df)
```

#### 来自带有 Surv.from_arrays

```python
import numpy as np
import pandas as pd
from sksurv.util import Surv

# Load data
df = pd.read_csv('survival_data.csv')

# Create feature matrix
X = df.drop(['time', 'event'], axis=1)

# Create survival outcome
y = Surv.from_arrays(
    event=df['event'].astype(bool),
    time=df['time'].astype(float)
)
```

### 加载 ARFF 文件的 CSV

```python
from sksurv.io import loadarff

# Load ARFF format (Weka format)
data = loadarff('survival_data.arff')

# Extract X and y
X = data[0]  # pandas DataFrame
y = data[1]  # structured array
```

## 数据预处理

### 处理分类变量

#### 方法 1：OneHotEncoder (scikit-survival)

```python
from sksurv.preprocessing import OneHotEncoder
import pandas as pd

# Identify categorical columns
categorical_cols = ['gender', 'race', 'treatment']

# One-hot encode
encoder = OneHotEncoder()
X_encoded = encoder.fit_transform(X[categorical_cols])

# Combine with numerical features
numerical_cols = [col for col in X.columns if col not in categorical_cols]
X_processed = pd.concat([X[numerical_cols], X_encoded], axis=1)
```

#### 方法 2：encode_categorical

```python
from sksurv.preprocessing import encode_categorical

# Automatically encode all categorical columns
X_encoded = encode_categorical(X)
```

#### 方法 3：Pandas get_dummies

```python
import pandas as pd

# One-hot encode categorical variables
X_encoded = pd.get_dummies(X, drop_first=True)
```

### 标准化

标准化对于以下方面很重要：
- 具有正则化的Cox模型
- SVM
- 对特征尺度敏感的模型

```python
from sklearn.preprocessing import StandardScaler

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Convert back to DataFrame
X_scaled = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
```

### 处理丢失数据

#### 检查丢失值

```python
# Check missing values
missing = X.isnull().sum()
print(missing[missing > 0])

# Visualize missing data
import seaborn as sns
sns.heatmap(X.isnull(), cbar=False)
```

#### 插补策略

```python
from sklearn.impute import SimpleImputer

# Mean imputation for numerical features
num_imputer = SimpleImputer(strategy='mean')
X_num = X.select_dtypes(include=[np.number])
X_num_imputed = num_imputer.fit_transform(X_num)

# Most frequent for categorical
cat_imputer = SimpleImputer(strategy='most_frequent')
X_cat = X.select_dtypes(include=['object', 'category'])
X_cat_imputed = cat_imputer.fit_transform(X_cat)
```

#### 高级插补

```python
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# Iterative imputation
imputer = IterativeImputer(random_state=42)
X_imputed = imputer.fit_transform(X)
```

#### 特征选择

#### 方差阈值

```python
from sklearn.feature_selection import VarianceThreshold

# Remove low variance features
selector = VarianceThreshold(threshold=0.01)
X_selected = selector.fit_transform(X)

# Get selected feature names
selected_features = X.columns[selector.get_support()]
```

#### 单变量特征选择

```python
from sklearn.feature_selection import SelectKBest
from sksurv.util import Surv

# Select top k features
selector = SelectKBest(k=10)
X_selected = selector.fit_transform(X, y)

# Get selected features
selected_features = X.columns[selector.get_support()]
```

## 完整的预处理管道

### 使用sklearn管道

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sksurv.linear_model import CoxPHSurvivalAnalysis

# Create preprocessing and modeling pipeline
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('model', CoxPHSurvivalAnalysis())
])

# Fit pipeline
pipeline.fit(X, y)

# Predict
predictions = pipeline.predict(X_test)
```

### 自定义预处理函数

```python
def preprocess_survival_data(X, y=None, scaler=None, encoder=None):
    """
    Complete preprocessing pipeline for survival data

    Parameters:
    -----------
    X : DataFrame
        Feature matrix
    y : structured array, optional
        Survival outcome (for filtering invalid samples)
    scaler : StandardScaler, optional
        Fitted scaler (for test data)
    encoder : OneHotEncoder, optional
        Fitted encoder (for test data)

    Returns:
    --------
    X_processed : DataFrame
        Processed features
    scaler : StandardScaler
        Fitted scaler
    encoder : OneHotEncoder
        Fitted encoder
    """
    from sklearn.preprocessing import StandardScaler
    from sksurv.preprocessing import encode_categorical

    # 1. Handle missing values
    # Remove rows with missing outcome
    if y is not None:
        mask = np.isfinite(y['time']) & (y['time'] > 0)
        X = X[mask]
        y = y[mask]

    # Impute missing features
    X = X.fillna(X.median())

    # 2. Encode categorical variables
    if encoder is None:
        X_processed = encode_categorical(X)
        encoder = None  # encode_categorical doesn't return encoder
    else:
        X_processed = encode_categorical(X)

    # 3. Standardize numerical features
    if scaler is None:
        scaler = StandardScaler()
        X_processed = pd.DataFrame(
            scaler.fit_transform(X_processed),
            columns=X_processed.columns,
            index=X_processed.index
        )
    else:
        X_processed = pd.DataFrame(
            scaler.transform(X_processed),
            columns=X_processed.columns,
            index=X_processed.index
        )

    if y is not None:
        return X_processed, y, scaler, encoder
    else:
        return X_processed, scaler, encoder

# Usage
X_train_processed, y_train_processed, scaler, encoder = preprocess_survival_data(X_train, y_train)
X_test_processed, _, _ = preprocess_survival_data(X_test, scaler=scaler, encoder=encoder)
```

## 数据质量检查

### 验证生存数据

```python
def validate_survival_data(y):
    """Check survival data quality"""

    # Check for negative times
    if np.any(y['time'] <= 0):
        print("WARNING: Found non-positive survival times")
        print(f"Negative times: {np.sum(y['time'] <= 0)}")

    # Check for missing values
    if np.any(~np.isfinite(y['time'])):
        print("WARNING: Found missing survival times")
        print(f"Missing times: {np.sum(~np.isfinite(y['time']))}")

    # Censoring rate
    censor_rate = 1 - y['event'].mean()
    print(f"Censoring rate: {censor_rate:.2%}")

    if censor_rate > 0.7:
        print("WARNING: High censoring rate (>70%)")
        print("Consider using Uno's C-index instead of Harrell's")

    # Event rate
    print(f"Number of events: {y['event'].sum()}")
    print(f"Number of censored: {(~y['event']).sum()}")

    # Time statistics
    print(f"Median time: {np.median(y['time']):.2f}")
    print(f"Time range: [{np.min(y['time']):.2f}, {np.max(y['time']):.2f}]")

# Use validation
validate_survival_data(y)
```

### 检查对于足够的事件

```python
def check_events_per_feature(X, y, min_events_per_feature=10):
    """
    Check if there are sufficient events per feature.
    Rule of thumb: at least 10 events per feature for Cox models.
    """
    n_events = y['event'].sum()
    n_features = X.shape[1]
    events_per_feature = n_events / n_features

    print(f"Number of events: {n_events}")
    print(f"Number of features: {n_features}")
    print(f"Events per feature: {events_per_feature:.1f}")

    if events_per_feature < min_events_per_feature:
        print(f"WARNING: Low events per feature ratio (<{min_events_per_feature})")
        print("Consider:")
        print("  - Feature selection")
        print("  - Regularization (CoxnetSurvivalAnalysis)")
        print("  - Collecting more data")

    return events_per_feature

# Use check
check_events_per_feature(X, y)
```

## 训练测试分割

### 随机分割

```python
from sklearn.model_selection import train_test_split

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

#### 分层分割

确保相似的审查率和时间分布：

```python
from sklearn.model_selection import train_test_split

# Create stratification labels
# Stratify by event status and time quartiles
time_quartiles = pd.qcut(y['time'], q=4, labels=False)
strat_labels = y['event'].astype(int) * 10 + time_quartiles

# Stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=strat_labels, random_state=42
)

# Verify similar distributions
print("Training set:")
print(f"  Censoring rate: {1 - y_train['event'].mean():.2%}")
print(f"  Median time: {np.median(y_train['time']):.2f}")

print("Test set:")
print(f"  Censoring rate: {1 - y_test['event'].mean():.2%}")
print(f"  Median time: {np.median(y_test['time']):.2f}")
```

## 工作与时变协变量

注意：scikit-survival不直接支持时变协变量。对于此类数据，请考虑：
1. 时间分层分析
2. 标志方法
3. 使用其他包（例如生命线）

## 总结：完整的数据准备工作流程

```python
from sksurv.util import Surv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sksurv.preprocessing import encode_categorical
import pandas as pd
import numpy as np

# 1. Load data
df = pd.read_csv('data.csv')

# 2. Create survival outcome
y = Surv.from_dataframe('event', 'time', df)

# 3. Prepare features
X = df.drop(['event', 'time'], axis=1)

# 4. Validate data
validate_survival_data(y)
check_events_per_feature(X, y)

# 5. Handle missing values
X = X.fillna(X.median())

# 6. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 7. Encode categorical variables
X_train = encode_categorical(X_train)
X_test = encode_categorical(X_test)

# 8. Standardize
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Convert back to DataFrames
X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)

# Now ready for modeling!
```
