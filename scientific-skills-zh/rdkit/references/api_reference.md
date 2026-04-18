# RDKit API 参考

本文档提供了 RDKit 的 Python API 的全面参考，按功能组织。

## 核心模块：rdkit.Chem

用于处理分子的基本模块。

### 分子 I/O

* *阅读分子：**

- `Chem.MolFromSmiles(smiles, sanitize=True)` - 解析 SMILES 字符串
- `Chem.MolFromSmarts(smarts)` - 解析 SMARTS 模式
- `Chem.MolFromMolFile(filename, sanitize=True, removeHs=True)` - 读取 MOL 文件
- `Chem.MolFromMolBlock(molblock, sanitize=True, removeHs=True)` - 解析 MOL 块字符串
- `Chem.MolFromMol2File(filename, sanitize=True, removeHs=True)` - 读取 MOL2 文件
- `Chem.MolFromMol2Block(molblock, sanitize=True, removeHs=True)` - 解析 MOL2 块
- `Chem.MolFromPDBFile(filename, sanitize=True, removeHs=True)` - 读取 PDB 文件
- `Chem.MolFromPDBBlock(pdbblock, sanitize=True, removeHs=True)` - 解析 PDB 块
- `Chem.MolFromInchi(inchi, sanitize=True, removeHs=True)` - 解析 InChI字符串
- `Chem.MolFromSequence(seq, sanitize=True)` - 从肽序列创建分子

* *写入分子：**

- `Chem.MolToSmiles(mol, isomericSmiles=True, canonical=True)` - 转换为SMILES
- `Chem.MolToSmarts(mol, isomericSmarts=False)` - 转换为SMARTS
- `Chem.MolToMolBlock(mol, includeStereo=True, confId=-1)` -转换为 MOL 块
- `Chem.MolToMolFile(mol, filename, includeStereo=True, confId=-1)` - 写入 MOL 文件
- `Chem.MolToPDBBlock(mol, confId=-1)` - 转换为 PDB 块
- `Chem.MolToPDBFile(mol, filename, confId=-1)` - 写入 PDB 文件
- `Chem.MolToInchi(mol, options='')` - 转换为 InChI
- `Chem.MolToInchiKey(mol, options='')` - 生成 InChI 密钥
- `Chem.MolToSequence(mol)` - 转换为肽序列

* *批量 I/O：**

- `Chem.SDMolSupplier(filename, sanitize=True, removeHs=True)` - SDF 文件阅读器
- `Chem.ForwardSDMolSupplier(fileobj, sanitize=True, removeHs=True)` - 仅正向 SDF读取器
- `Chem.MultithreadedSDMolSupplier(filename, numWriterThreads=1)` - 并行SDF读取器
- `Chem.SmilesMolSupplier(filename, delimiter=' ', titleLine=True)` - SMILES文件读取器
- `Chem.SDWriter(filename)` - SDF文件写入器
- `Chem.SmilesWriter(filename, delimiter=' ', includeHeader=True)` - SMILES文件写入器

### 分子操作

* *消毒：**

- `Chem.SanitizeMol(mol, sanitizeOps=SANITIZE_ALL, catchErrors=False)` - 消毒分子
- `Chem.DetectChemistryProblems(mol, sanitizeOps=SANITIZE_ALL)` - 检测消毒问题
- `Chem.AssignStereochemistry(mol, cleanIt=True, force=False)` - 分配立体化学
- `Chem.FindPotentialStereo(mol)` -查找潜在的立体中心
- `Chem.AssignStereochemistryFrom3D(mol, confId=-1)` - 从3D坐标分配立体

* *氢管理：**

- `Chem.AddHs(mol, explicitOnly=False, addCoords=False)` - 添加显式氢
- `Chem.RemoveHs(mol, implicitOnly=False, updateExplicitCount=False)` - 删除氢
- `Chem.RemoveAllHs(mol)` - 去除所有氢

* *芳香性：**

- `Chem.SetAromaticity(mol, model=AROMATICITY_RDKIT)` - 设置芳香性模型
- `Chem.Kekulize(mol, clearAromaticFlags=False)` - Kekulize芳香键
- `Chem.SetConjugation(mol)` - 设置共轭标志

* *片段：**

- `Chem.GetMolFrags(mol, asMols=False, sanitizeFrags=True)` - 获取断开连接的片段
- `Chem.FragmentOnBonds(mol, bondIndices, addDummies=True)` - 特定键上的片段
- `Chem.ReplaceSubstructs(mol, query, replacement, replaceAll=False)` - 替换子结构
- `Chem.DeleteSubstructs(mol, query, onlyFrags=False)` - 删除子结构

* *立体化学：**

- `Chem.FindMolChiralCenters(mol, includeUnassigned=False, useLegacyImplementation=False)` - 查找手性中心
- `Chem.FindPotentialStereo(mol, cleanIt=True)` - 查找潜在的立体中心

### 子结构搜索

* *基本匹配：**

- `mol.HasSubstructMatch(query, useChirality=False)` - 检查对于子结构匹配
- `mol.GetSubstructMatch(query, useChirality=False)` - 获取第一个匹配
- `mol.GetSubstructMatches(query, uniquify=True, useChirality=False)` - 获取所有匹配
- `mol.GetSubstructMatches(query, maxMatches=1000)` - 限制匹配数量

### 分子属性

 * *原子方法：** 

- `atom.GetSymbol()` - 原子符号
- `atom.GetAtomicNum()` - 原子序数
- `atom.GetDegree()` - 键数
- `atom.GetTotalDegree()` - 包括氢
- `atom.GetFormalCharge()` - 形式电荷
- `atom.GetNumRadicalElectrons()` - 自由基电子
- `atom.GetIsAromatic()` - 芳香标记
- `atom.GetHybridization()` - 杂交（SP、SP2、SP3等）
- `atom.GetIdx()` - 原子索引
- `atom.IsInRing()` - 在任何环中
- `atom.IsInRingSize(size)` - 在特定尺寸的环中
- `atom.GetChiralTag()` - 手性标签

* *键合方法：**

- `bond.GetBondType()` - 键合类型（单、双、三、芳香）
- `bond.GetBeginAtomIdx()` - 起始原子索引
- `bond.GetEndAtomIdx()` - 结束原子索引
- `bond.GetIsConjugated()` - 共轭标志
- `bond.GetIsAromatic()` - 芳香性标记
- `bond.IsInRing()` - 在任何环中
- `bond.GetStereo()` - 立体化学（STEREONONE、STEREOZ、STEREOE 等）

* *分子方法：**

- `mol.GetNumAtoms(onlyExplicit=True)` - 数量原子
- `mol.GetNumHeavyAtoms()` - 重原子数量
- `mol.GetNumBonds()` - 键数量
- `mol.GetAtoms()` - 原子迭代器
- `mol.GetBonds()` - 键迭代器
- `mol.GetAtomWithIdx(idx)` - 获取特定原子
- `mol.GetBondWithIdx(idx)` - 获取特定键
- `mol.GetRingInfo()` - 环信息对象

* *环信息：**

- `Chem.GetSymmSSSR(mol)` - 获取最小环的最小集合
- `Chem.GetSSSR(mol)` - GetSymmSSSR
 的别名- `ring_info.NumRings()` - 环数
- `ring_info.AtomRings()` - 环中原子索引的元组
- `ring_info.BondRings()` - 环中键索引的元组

## rdkit.Chem.AllChem

扩展化学功能。

### 2D/3D坐标生成

- `AllChem.Compute2DCoords(mol, canonOrient=True, clearConfs=True)` - 生成2D坐标
- `AllChem.EmbedMolecule(mol, maxAttempts=0, randomSeed=-1, useRandomCoords=False)` - 生成3D conformer
- `AllChem.EmbedMultipleConfs(mol, numConfs=10, maxAttempts=0, randomSeed=-1)` - 生成多个conformer
- `AllChem.ConstrainedEmbed(mol, core, useTethers=True)` - 约束嵌入
- `AllChem.GenerateDepictionMatching2DStructure(mol, reference, refPattern=None)` - 对齐模板

### 力场优化

- `AllChem.UFFOptimizeMolecule(mol, maxIters=200, confId=-1)` - UFF优化
- `AllChem.MMFFOptimizeMolecule(mol, maxIters=200, confId=-1, mmffVariant='MMFF94')` - MMFF 优化
- `AllChem.UFFGetMoleculeForceField(mol, confId=-1)` - 获取UFF力场对象
- `AllChem.MMFFGetMoleculeForceField(mol, pyMMFFMolProperties, confId=-1)` - 获取MMFF力场

### 适形分析

- `AllChem.GetConformerRMS(mol, confId1, confId2, prealigned=False)` - 计算RMSD
- `AllChem.GetConformerRMSMatrix(mol, prealigned=False)` - RMSD 矩阵
- `AllChem.AlignMol(prbMol, refMol, prbCid=-1, refCid=-1)` - 对齐分子
- `AllChem.AlignMolConformers(mol)` - 对齐所有构象异构体

### 反应

- `AllChem.ReactionFromSmarts(smarts, useSmiles=False)` - 创建反应SMARTS
- `reaction.RunReactants(reactants)` - 应用反应
- `reaction.RunReactant(reactant, reactionIdx)` - 适用于特定反应物
- `AllChem.CreateDifferenceFingerprintForReaction(reaction)` - 反应指纹

### 指纹

- `AllChem.GetMorganFingerprint(mol, radius, useFeatures=False)` - 摩根指纹
- `AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=2048)` - 摩根位向量
- `AllChem.GetHashedMorganFingerprint(mol, radius, nBits=2048)` - 哈希摩根
- `AllChem.GetErGFingerprint(mol)` - ErG 指纹

## rdkit.Chem.Descriptors

分子描述符计算。

### 通用描述符

- `Descriptors.MolWt(mol)` - 分子量
- `Descriptors.ExactMolWt(mol)` - 精确分子量
- `Descriptors.HeavyAtomMolWt(mol)` - 重原子分子量
- `Descriptors.MolLogP(mol)` - LogP（亲油性）
- `Descriptors.MolMR(mol)` -摩尔折射率
- `Descriptors.TPSA(mol)` - 拓扑极性表面积
- `Descriptors.NumHDonors(mol)` - 氢键供体
- `Descriptors.NumHAcceptors(mol)` - 氢键受体
- `Descriptors.NumRotatableBonds(mol)` - 可旋转键
- `Descriptors.NumAromaticRings(mol)` - 芳香环
- `Descriptors.NumSaturatedRings(mol)` - 饱和环
- `Descriptors.NumAliphaticRings(mol)` - 脂肪族环
- `Descriptors.NumAromaticHeterocycles(mol)` - 芳香杂环
- `Descriptors.NumRadicalElectrons(mol)` -自由基电子
- `Descriptors.NumValenceElectrons(mol)` - 价电子

### 批量计算

- `Descriptors.CalcMolDescriptors(mol)` - 将所有描述符计算为字典

### 描述符列表

- `Descriptors._descList` - 列表（名称，函数）所有描述符的元组

## rdkit.Chem.Draw

分子可视化。

### 图像生成

- `Draw.MolToImage(mol, size=(300,300), kekulize=True, wedgeBonds=True, highlightAtoms=None)` - 生成PIL图像
- `Draw.MolToFile(mol, filename, size=(300,300), kekulize=True, wedgeBonds=True)` - 保存到文件
- `Draw.MolsToGridImage(mols, molsPerRow=3, subImgSize=(200,200), legends=None)` - 分子网格
- `Draw.MolsMatrixToGridImage(mols, molsPerRow=3, subImgSize=(200,200), legends=None)` - 嵌套网格
- `Draw.ReactionToImage(rxn, subImgSize=(200,200))` - 反应图像

### 指纹可视化

- `Draw.DrawMorganBit(mol, bitId, bitInfo, whichExample=0)` - 可视化摩根bit
- `Draw.DrawMorganBits(bits, mol, bitInfo, molsPerRow=3)` - 多个 Morgan 位
- `Draw.DrawRDKitBit(mol, bitId, bitInfo, whichExample=0)` - 可视化 RDKit bit

### IPython 集成

- `Draw.IPythonConsole` - Jupyter 集成模块
- `Draw.IPythonConsole.ipython_useSVG` - 使用 SVG (True)或 PNG (False)
- `Draw.IPythonConsole.molSize` - 默认分子图像大小

### 绘图选项

- `rdMolDraw2D.MolDrawOptions()` - 获取绘图选项对象
  - `.addAtomIndices` - 显示原子指数
  - `.addBondIndices` - 显示键指数
  - `.addStereoAnnotation` - 显示立体化学
  - `.bondLineWidth` - 线宽
  - `.highlightBondWidthMultiplier` - 突出显示宽度
  - `.minFontSize` - 最小字体大小
  - `.maxFontSize` - 最大字体大小

## rdkit.Chem.rdMolDescriptors

附加描述符计算。

- `rdMolDescriptors.CalcNumRings(mol)` - 环数
- `rdMolDescriptors.CalcNumAromaticRings(mol)` - 芳香环
- `rdMolDescriptors.CalcNumAliphaticRings(mol)` - 脂肪族环
- `rdMolDescriptors.CalcNumSaturatedRings(mol)` - 饱和环
- `rdMolDescriptors.CalcNumHeterocycles(mol)` -杂环
- `rdMolDescriptors.CalcNumAromaticHeterocycles(mol)` - 芳香杂环
- `rdMolDescriptors.CalcNumSpiroAtoms(mol)` - 螺原子
- `rdMolDescriptors.CalcNumBridgeheadAtoms(mol)` - 桥头原子
- `rdMolDescriptors.CalcFractionCsp3(mol)` - sp3 碳的分数
- `rdMolDescriptors.CalcLabuteASA(mol)` - Labute可及表面积
- `rdMolDescriptors.CalcTPSA(mol)` - TPSA
- `rdMolDescriptors.CalcMolFormula(mol)` - 分子式

## rdkit.Chem.Scaffolds

支架分析。

### Murcko Scaffolds

- `MurckoScaffold.GetScaffoldForMol(mol)` - 获取 Murcko 脚手架
- `MurckoScaffold.MakeScaffoldGeneric(mol)` - 通用脚手架
- `MurckoScaffold.MurckoDecompose(mol)` - 分解为脚手架和侧链

## rdkit.Chem.rdMolHash

分子哈希和标准化。

- `rdMolHash.MolHash(mol, hashFunction)` - 生成哈希
  - `rdMolHash.HashFunction.AnonymousGraph` - 匿名结构
  - `rdMolHash.HashFunction.CanonicalSmiles` - Canonical SMILES
  - `rdMolHash.HashFunction.ElementGraph` - 元素图
  - `rdMolHash.HashFunction.MurckoScaffold` - Murcko 支架
  - `rdMolHash.HashFunction.Regioisomer` - 区域异构体（无立体）
  - `rdMolHash.HashFunction.NetCharge` - 净电荷
  - `rdMolHash.HashFunction.HetAtomProtomer` - 杂原子原异构体
  - `rdMolHash.HashFunction.HetAtomTautomer` - 杂原子互变异构体

## rdkit.Chem.MolStandardize

分子标准化。

- `rdMolStandardize.Normalize(mol)` - 标准化功能组
- `rdMolStandardize.Reionize(mol)` - 修复电离状态
- `rdMolStandardize.RemoveFragments(mol)` - 删除小碎片
- `rdMolStandardize.Cleanup(mol)` - 全面清理（标准化+重新电离+删除）
- `rdMolStandardize.Uncharger()` - 创建卸充电器object
  - `.uncharge(mol)` - 删除费用
- `rdMolStandardize.TautomerEnumerator()` - 枚举互变异构体
  - `.Enumerate(mol)` - 生成互变异构体
  - `.Canonicalize(mol)` - 获取规范互变异构体

## rdkit.DataStructs

指纹相似度和操作。

### 相似度度量

- `DataStructs.TanimotoSimilarity(fp1, fp2)` - 谷本系数
- `DataStructs.DiceSimilarity(fp1, fp2)` - 骰子系数
- `DataStructs.CosineSimilarity(fp1, fp2)` - 余弦相似度
- `DataStructs.SokalSimilarity(fp1, fp2)` - 索卡尔相似度
- `DataStructs.KulczynskiSimilarity(fp1, fp2)` - Kulczynski相似度
- `DataStructs.McConnaugheySimilarity(fp1, fp2)` - McConnaughey 相似度

### 批量操作

- `DataStructs.BulkTanimotoSimilarity(fp, fps)` - Tanimoto 指纹列表
- `DataStructs.BulkDiceSimilarity(fp, fps)` - 列表骰子
- `DataStructs.BulkCosineSimilarity(fp, fps)` -列表的余弦

### 距离度量

- `DataStructs.TanimotoDistance(fp1, fp2)` - 1 - Tanimoto
- `DataStructs.DiceDistance(fp1, fp2)` - 1 - Dice

## rdkit.Chem.AtomPairs

Atom 对指纹。

- `Pairs.GetAtomPairFingerprint(mol, minLength=1, maxLength=30)` - 原子对指纹
- `Pairs.GetAtomPairFingerprintAsBitVect(mol, minLength=1, maxLength=30, nBits=2048)` - 作为位向量
- `Pairs.GetHashedAtomPairFingerprint(mol, nBits=2048, minLength=1, maxLength=30)` - 散列版本

## rdkit.Chem.Torsions

拓扑扭转指纹。

- `Torsions.GetTopologicalTorsionFingerprint(mol, targetSize=4)` - 扭转指纹
- `Torsions.GetTopologicalTorsionFingerprintAsIntVect(mol, targetSize=4)` - 作为 int 向量
- `Torsions.GetHashedTopologicalTorsionFingerprint(mol, nBits=2048, targetSize=4)` - 哈希版本

## rdkit.Chem.MACCSkeys

MACCS结构密钥。

- `MACCSkeys.GenMACCSKeys(mol)` - 生成166位MACCS密钥

## rdkit.Chem.ChemicalFeatures

药效团特征。

- `ChemicalFeatures.BuildFeatureFactory(featureFile)` - 创建特征工厂
- `factory.GetFeaturesForMol(mol)` - 获取药效团特征
- `feature.GetFamily()` - 特征族（供体、受体等）
- `feature.GetType()` - 特征类型
- `feature.GetAtomIds()` - 参与特征的原子

## rdkit.ML.Cluster.Butina

聚类算法。

- `Butina.ClusterData(distances, nPts, distThresh, isDistData=True)` - Butina聚类
  - 返回具有聚类成员的元组的元组

## rdkit.Chem.rdFingerprintGenerator

现代指纹生成API (RDKit 2020.09+).

- `rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)` - 摩根生成器
- `rdFingerprintGenerator.GetRDKitFPGenerator(minPath=1, maxPath=7, fpSize=2048)` - RDKit FP生成器
- `rdFingerprintGenerator.GetAtomPairGenerator(minDistance=1, maxDistance=30)` - 原子对生成器
- `generator.GetFingerprint(mol)` - 生成指纹
- `generator.GetCountFingerprint(mol)` - 基于计数的指纹

## 常用参数

### 清理操作

- `SANITIZE_NONE` - 无清理
- `SANITIZE_ALL` - 所有操作（默认）
- `SANITIZE_CLEANUP` - 基本清理
- `SANITIZE_PROPERTIES` - 计算属性
- `SANITIZE_SYMMRINGS` - 对称环
- `SANITIZE_KEKULIZE` - Kekulize芳香环
- `SANITIZE_FINDRADICALS` - 查找自由基电子
- `SANITIZE_SETAROMATICITY` - 设置芳香性
- `SANITIZE_SETCONJUGATION` - 设置共轭
- `SANITIZE_SETHYBRIDIZATION` - 设置杂交
- `SANITIZE_CLEANUPCHIRALITY` - 净化手性

### 键类型

- `BondType.SINGLE` - 单键
- `BondType.DOUBLE` - 双键
- `BondType.TRIPLE` - 三键
- `BondType.AROMATIC` - 芳香键
- `BondType.DATIVE` - 配位键
- `BondType.UNSPECIFIED` - 未指定

### 杂化

- `HybridizationType.S` - S
- `HybridizationType.SP` - SP
- `HybridizationType.SP2` - SP2
- `HybridizationType.SP3` - SP3
- `HybridizationType.SP3D` - SP3D
- `HybridizationType.SP3D2` - SP3D2

### 手性

- `ChiralType.CHI_UNSPECIFIED` - 未指定
- `ChiralType.CHI_TETRAHEDRAL_CW` - 顺时针
- `ChiralType.CHI_TETRAHEDRAL_CCW` -逆时针

## 安装

```bash
# Using conda (recommended)
conda install -c conda-forge rdkit

# Using pip
pip install rdkit-pypi
```

## 导入

```python
# Core functionality
from rdkit import Chem
from rdkit.Chem import AllChem

# Descriptors
from rdkit.Chem import Descriptors

# Drawing
from rdkit.Chem import Draw

# Similarity
from rdkit import DataStructs
```
