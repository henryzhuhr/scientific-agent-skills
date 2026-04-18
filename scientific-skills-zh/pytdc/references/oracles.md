# TDC 分子生成 Oracles

Oracles 是评估跨特定维度生成的分子质量的函数。 TDC 为从头药物设计中的分子优化任务提供了 17 多个预言机函数。

## 概述

预言机测量分子特性并有两个主要目的：

1. **目标导向生成**：优化分子以最大化/最小化特定属性
2. **分布学习**：评估生成的分子是否匹配所需的属性分布

## 使用 Oracles

### 基本用法

```python
from tdc import Oracle

# Initialize oracle
oracle = Oracle(name='GSK3B')

# Evaluate single molecule (SMILES string)
score = oracle('CC(C)Cc1ccc(cc1)C(C)C(O)=O')

# Evaluate multiple molecules
scores = oracle(['SMILES1', 'SMILES2', 'SMILES3'])
```

### Oracle 类别

TDC 预言机根据正在评估的分子属性分为几个类别。

## 生物化学Oracles

预测针对生物靶点的结合亲和力或活性。

### 目标特异性 Oracles

* *DRD2 - 多巴胺受体 D2**
```python
oracle = Oracle(name='DRD2')
score = oracle(smiles)
```
- 测量与 DRD2 受体的结合亲和力
- 对于神经和精神药物很重要开发
- 分数越高表示结合力越强

* *GSK3B - 糖原合成酶激酶-3 Beta**
```python
oracle = Oracle(name='GSK3B')
score = oracle(smiles)
```
- 预测 GSK3β 抑制
- 与阿尔茨海默病、糖尿病和癌症研究相关
- 分数越高表示越好抑制

* *JNK3 - c-Jun N 末端激酶 3**
```python
oracle = Oracle(name='JNK3')
score = oracle(smiles)
```
- 测量 JNK3 激酶抑制
- 神经退行性疾病的靶点
- 分数越高表明抑制作用越强

* *5HT2A - 血清素 2A受体**
```python
oracle = Oracle(name='5HT2A')
score = oracle(smiles)
```
- 预测血清素受体结合
- 对于精神科药物很重要
- 分数越高表示结合力越强

* *ACE - 血管紧张素转换酶**
```python
oracle = Oracle(name='ACE')
score = oracle(smiles)
```
- 测量 ACE抑制
- 高血压治疗的目标
- 分数越高表明抑制效果越好

* *MAPK - 丝裂原激活蛋白激酶**
```python
oracle = Oracle(name='MAPK')
score = oracle(smiles)
```
-预测MAPK抑制
- 癌症和炎症性疾病的目标

* *CDK - 细胞周期蛋白依赖性激酶**
```python
oracle = Oracle(name='CDK')
score = oracle(smiles)
```
- 测量 CDK 抑制
- 对于癌症药物开发很重要

* *P38 - p38 MAP 激酶**
```python
oracle = Oracle(name='P38')
score = oracle(smiles)
```
- 预测 p38 MAPK 抑制
- 炎症靶标疾病

* *PARP1 - 聚（ADP-核糖）聚合酶 1**
```python
oracle = Oracle(name='PARP1')
score = oracle(smiles)
```
- 测量 PARP1 抑制
- 癌症治疗靶点（DNA 修复机制）

* *PIK3CA - 磷脂酰肌醇-4,5-二磷酸3-激酶**
```python
oracle = Oracle(name='PIK3CA')
score = oracle(smiles)
```
- 预测 PIK3CA 抑制
- 肿瘤学中的重要靶标

## 理化 Oracles

E 评估药物样特性和 ADME 特征。

### 药物相似性 Oracles

* *QED -药物相似性的定量估计**
```python
oracle = Oracle(name='QED')
score = oracle(smiles)
```
-结合多种理化特性
- 评分范围从0（非药物样）到1（药物样）
- 基于Bickerton等人。标准

* *Lipinski - 五规则**
```python
oracle = Oracle(name='Lipinski')
score = oracle(smiles)
```
- 违反 Lipinski 规则的次数
- 规则：MW ≤ 500、logP ≤ 5、HBD ≤ 5、HBA ≤ 10
- 0 分表示完全合规

### 分子特性

* *SA - 合成可及性**
```python
oracle = Oracle(name='SA')
score = oracle(smiles)
```
- 估计合成的难易程度
- 分数范围从1（容易）到10（困难）
- 较低的分数表示更容易合成

* *LogP - 辛醇-水分配系数**
```python
oracle = Oracle(name='LogP')
score = oracle(smiles)
```
- 测量亲脂性
- 对膜渗透性很重要
- 典型药物范围：0-5

* *MW - 分子量**
```python
oracle = Oracle(name='MW')
score = oracle(smiles)
```
- 返回分子量Daltons
- 类药范围通常为 150-500 Da

## 复合 Oracles

组合多个属性进行多目标优化。

* *异构体 Meta**
```python
oracle = Oracle(name='Isomer_Meta')
score = oracle(smiles)
```
- 评估特定异构体属性
- 用于立体化学优化

* *中值分子**
```python
oracle = Oracle(name='Median1', 'Median2')
score = oracle(smiles)
```
-测试生成具有中值特性的分子的能力
- 对于分布学习基准有用

* *重新发现**
```python
oracle = Oracle(name='Rediscovery')
score = oracle(smiles)
```
-测量与已知参考分子的相似性
- 测试再生现有药物的能力

* *相似性**
```python
oracle = Oracle(name='Similarity')
score = oracle(smiles)
```
-计算与目标分子的结构相似性
- 基于分子指纹（通常是Tanimoto）相似性）

* *唯一性**
```python
oracle = Oracle(name='Uniqueness')
scores = oracle(smiles_list)
```
-测量生成的分子集中的多样性
- 返回独特分子的分数

* *新颖性**
```python
oracle = Oracle(name='Novelty')
scores = oracle(smiles_list, training_set)
```
-测量生成的分子与训练集的不同
- 分数越高表示越新颖结构

## 专用 Oracle

* *ASKCOS - 逆合成评分**
```python
oracle = Oracle(name='ASKCOS')
score = oracle(smiles)
```
- 使用逆合成评估合成可行性
- 需要 ASKCOS 后端 (IBM RXN)
- 基于逆合成路线的分数可用性

* *对接分数**
```python
oracle = Oracle(name='Docking')
score = oracle(smiles)
```
-针对目标蛋白的分子对接分数
- 需要蛋白质结构和对接软件
- 较低的分数通常表明更好的结合

* *Vina - AutoDock Vina分数**
```python
oracle = Oracle(name='Vina')
score = oracle(smiles)
```
-使用AutoDock Vina进行蛋白质-配体对接
- 以kcal/mol为单位预测结合亲和力
- 负分数越多表示结合力越强

## 多目标优化

组合多个预言以获得多特性优化：

```python
from tdc import Oracle

# Initialize multiple oracles
qed_oracle = Oracle(name='QED')
sa_oracle = Oracle(name='SA')
drd2_oracle = Oracle(name='DRD2')

# Define custom scoring function
def multi_objective_score(smiles):
    qed = qed_oracle(smiles)
    sa = 1 / (1 + sa_oracle(smiles))  # Invert SA (lower is better)
    drd2 = drd2_oracle(smiles)

    # Weighted combination
    return 0.3 * qed + 0.3 * sa + 0.4 * drd2

# Evaluate molecule
score = multi_objective_score('CC(C)Cc1ccc(cc1)C(C)C(O)=O')
```

## Oracle 性能注意事项

### 速度
- **快速**：QED、SA、LogP、MW、Lipinski（基于规则的计算）
- **中**：特定于目标的 ML 模型（DRD2、GSK3B、等）
- **慢**：基于对接的预言机（Vina、ASKCOS）

### 可靠性
- 预言机是在特定数据集上训练的 ML 模型
- 可能无法推广到所有化学空间
- 使用多个预言机来验证结果

### 批处理
```python
# Efficient batch evaluation
oracle = Oracle(name='GSK3B')
smiles_list = ['SMILES1', 'SMILES2', ..., 'SMILES1000']
scores = oracle(smiles_list)  # Faster than individual calls
```

## 常见工作流程

### 目标导向生成
```python
from tdc import Oracle
from tdc.generation import MolGen

# Load training data
data = MolGen(name='ChEMBL_V29')
train_smiles = data.get_data()['Drug'].tolist()

# Initialize oracle
oracle = Oracle(name='GSK3B')

# Generate molecules (user implements generative model)
# generated_smiles = generator.generate(n=1000)

# Evaluate generated molecules
scores = oracle(generated_smiles)
best_molecules = [(s, score) for s, score in zip(generated_smiles, scores)]
best_molecules.sort(key=lambda x: x[1], reverse=True)

print(f"Top 10 molecules:")
for smiles, score in best_molecules[:10]:
    print(f"{smiles}: {score:.3f}")
```

### 分布学习
```python
from tdc import Oracle
import numpy as np

# Initialize oracle
oracle = Oracle(name='QED')

# Evaluate training set
train_scores = oracle(train_smiles)
train_mean = np.mean(train_scores)
train_std = np.std(train_scores)

# Evaluate generated set
gen_scores = oracle(generated_smiles)
gen_mean = np.mean(gen_scores)
gen_std = np.std(gen_scores)

# Compare distributions
print(f"Training: μ={train_mean:.3f}, σ={train_std:.3f}")
print(f"Generated: μ={gen_mean:.3f}, σ={gen_std:.3f}")
```

## 与TDC集成基准

```python
from tdc.generation import MolGen

# Use with GuacaMol benchmark
data = MolGen(name='GuacaMol')

# Oracles are automatically integrated
# Each GuacaMol task has associated oracle
benchmark_results = data.evaluate_guacamol(
    generated_molecules=your_molecules,
    oracle_name='GSK3B'
)
```

## 注释

- Oracle 分数是预测，而不是实验测量
- 始终通过实验验证最佳候选者
- 不同的预言机可能有不同的分数范围和解释
- 某些预言机需要额外的依赖项或API 访问
- 检查预言机文档以了解具体详细信息：https://tdcommons.ai/functions/oracles/

## 添加自定义Oracles

要创建自定义预言机函数：

```python
class CustomOracle:
    def __init__(self):
        # Initialize your model/method
        pass

    def __call__(self, smiles):
        # Implement your scoring logic
        # Return score or list of scores
        pass

# Use like built-in oracles
custom_oracle = CustomOracle()
score = custom_oracle('CC(C)Cc1ccc(cc1)C(C)C(O)=O')
```

## 参考文献

- TDC Oracles 文档：https://tdcommons.ai/functions/oracles/
- GuacaMol 论文：“GuacaMol：从头分子的基准模型设计》
- MOSES 论文：《分子集（MOSES）：分子生成模型的基准平台》
