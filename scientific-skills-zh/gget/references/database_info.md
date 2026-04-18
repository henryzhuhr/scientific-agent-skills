# gget 数据库信息

gget 模块查询的数据库概述，包括更新频率和重要注意事项。

## 重要说明

gget 查询的数据库正在不断更新，有时会改变其结构。 gget 模块每两周自动测试一次，并在必要时更新以匹配新的数据库结构。始终保持 gget 更新：

```bash
pip install --upgrade gget
```

## 数据库目录

### 基因组参考数据库

#### Ensembl
- **使用者：** gget 参考、gget 搜索、gget info, gget seq
- **描述：** 全面的基因组数据库，带有脊椎动物和无脊椎动物物种的注释
- **更新频率：** 定期发布（编号）；大约每 3 个月发布一次新版本
- **访问：** FTP 下载、REST API
- **网站：** https://www.ensembl.org/
- **注释：**
  - 支持脊椎动物和无脊椎动物基因组
  - 可以指定版本号重现性
  - 适用于常见物种（“人类”、“小鼠”）的快捷方式

#### UCSC 基因组浏览器
- **使用者：** gget blat
- **描述：** 带 BLAT 比对工具的基因组浏览器数据库
- **更新频率：** 定期更新具有新组件
- **访问：** Web服务API
- **网站：** https://genome.ucsc.edu/
- **注释：**
  - 可用的多个基因组组件（hg38、mm39等）
  - 针对脊椎动物优化的BLAT基因组

### 蛋白质和结构数据库

#### UniProt
- **使用者：** gget 信息、gget seq（氨基酸序列）、gget elm
- **描述：** 通用蛋白质资源，全面的蛋白质序列和功能信息
- **更新频率：** 定期发布（Swiss-Prot 每周发布，Swiss-Prot 每月发布） TrEMBL)
- **访问：** REST API
- **网站：** https://www.uniprot.org/
- **注释：**
  - Swiss-Prot：手动注释和审查
  - TrEMBL：自动注释

#### NCBI（国家生物技术中心）信息）
- **使用者：** gget 信息、gget bgee（对于非 Ensembl 物种）
- **描述：** 具有广泛交叉引用的基因和蛋白质数据库
- **更新频率：** 持续更新
- **访问：** 电子实用程序API
- **网站：** https://www.ncbi.nlm.nih.gov/
- **数据库：** 基因、蛋白质、RefSeq

#### RCSB PDB（蛋白质数据库）
- **使用者：** gget pdb
- **描述：**蛋白质和核酸的 3D 结构数据存储库
- **更新频率：**每周更新
- **访问：** REST API
- **网站：** https://www.rcsb.org/
- **注释：**
  - 实验确定的结构（X 射线、NMR、冷冻电镜）
  - 包括有关实验和出版物的元数据

#### ELM（真核线性基序）
- **使用者：** gget elm
- **描述：** 真核蛋白质功能位点数据库
- **更新频率：** 定期更新
- **访问：** 下载的数据库（通过 gget 设置 elm）
- **网站：** http://elm.eu.org/
- **注释：**
  - 首次使用前需要本地下载
  - 包含经过验证的图案和模式

### 序列相似性数据库

#### BLAST 数据库 (NCBI)
- **使用者：** ggetblast
- **描述：** 用于 BLAST 搜索的预格式化数据库
- **更新频率：** 定期更新
- **访问：** NCBI BLAST API
- **数据库：**
  - **核苷酸：** nt（所有 GenBank）、refseq_rna、pdbnt
  - **蛋白质：** nr（非冗余）、swissprot、pdbaa、refseq_ Protein
- **注释：**
  - nt 和 nr 非常大数据库
  - 考虑专用数据库以实现更快、更集中的搜索

### 表达和相关数据库

#### ARCHS4
- **使用者：** gget archs4
- **描述：** 大规模挖掘公开可用的RNA-seq数据
- **更新频率：**定期更新新样本
- **访问：** HTTP API
- **网站：** https://maayanlab.cloud/archs4/
- **数据：**
  - 人类和小鼠 RNA 序列数据
  - 相关矩阵
  - 组织表达atlases
- **引用：** Lachmann et al., Nature Communications, 2018

#### CZ CELLxGENE Discover
- **使用者：** gget cellxgene
- **描述：** 来自多项研究的单细胞 RNA-seq 数据
- **更新频率：** 不断添加新数据集
- **访问：** Census API（通过 cellxgene-census 包）
- **网站：** https://cellxgene.cziscience.com/
- **数据：**
  - 单细胞 RNA-seq 计数矩阵
  - 细胞类型注释
  - 组织和疾病元数据
- **注释：**
  - 需要gget设置cellxgene
  - 基因符号区分大小写
  - 可能不支持最新的Python版本

#### Bgee
- **使用作者：** gget bgee
- **描述：** 基因表达和直系同源数据库
- **更新频率：** 定期发布
- **访问：** REST API
- **网站：** https://www.bgee.org/
- **数据：**
  - 跨组织和发育阶段的基因表达
  - 跨物种的直系关系
- **引文：** Bastian et al., 2021

### 功能和通路数据库

#### Enrichr / modEnrichr
- **使用者：** gget richr
- **描述：** 基因集富集分析 Web 服务
- **更新频率：** 定期更新底层数据库
- **访问：** REST API
- **网站：** https://maayanlab.cloud/Enrichr/
- **包括的数据库：**
  - KEGG 通路
  - 基因本体论 (GO)
  - 转录因子目标 (ChEA)
  - 疾病关联（GWAS 目录）
  - 细胞类型标记(PanglaoDB)
- **注释：**
  - 支持多种模式生物
  - 可以提供背景基因列表用于自定义富集

### 疾病和药物数据库

#### 开放目标
- **使用者：** gget opentargets
- **描述：** 疾病目标关联的综合平台
- **更新频率：** 定期发布（每季度）
- **访问：** GraphQL API
- **网站：** https://www.opentargets.org/
- **数据：**
  - 疾病协会
  - 药物信息和临床试验
  - 靶标可处理性
  - 药物遗传学
  - 基因表达
  - DepMap 基因疾病影响
  - 蛋白质-蛋白质相互作用

#### cBioPortal
- **使用者：** gget cbio
- **描述：** 癌症基因组学数据门户
- **更新频率：** 不断添加新研究
- **访问：** Web API，可下载数据集
- **网站：** https://www.cbioportal.org/
- **数据：**
  - 突变、拷贝数改变、结构变异
  - 基因表达
  - 临床数据
- **注释：**
  - 大型数据集；推荐缓存
  - 多种癌症类型和研究可用

#### COSMIC（癌症体细胞突变目录）
- **使用者：** gget cosmic
- **描述：**综合癌症突变数据库
- **更新频率：** 定期发布
- **获取方式：** 下载（商业使用需要帐号和许可证）
- **网站：** https://cancer.sanger.ac.uk/cosmic
- **数据：**
  - 癌症中的体细胞突变
  - 基因普查
  - 细胞系数据
  - 耐药突变
- **重要：**
  - 免费用于学术use
  - 商业用途需支付许可费
  - 需要 COSMIC 帐户凭据
  - 查询前必须下载数据库

### AI 和预测服务

#### AlphaFold2 (DeepMind)
- **使用者：** gget alphafold
- **描述：** 用于蛋白质结构预测的深度学习模型
- **模型版本：** 用于本地执行的简化版本
- **访问：** 本地计算（需要通过 gget 设置下载模型）
- **网站：** https://alphafold.ebi.ac.uk/
- **注意：**
  - 需要 ~4GB 模型参数下载
  - 需要 OpenMM 安装
  - 计算密集型
  - Python 版本特定要求

#### OpenAI API
- **使用者：** gget gpt
- **描述：** 大语言模型 API
- **更新频率：** 定期发布新模型
- **访问：** REST API（需要 API 密钥）
- **网站：** https://openai.com/
- **注释：**
  - 默认模型： gpt-3.5-turbo
  - 免费套餐仅限帐户创建后 3 个月
  - 设置计费限额以控制成本

## 数据一致性和再现性

### 版本控制
为了确保分析的再现性：

1. **指定数据库版本/版本：**
 ```python
 # 使用特定的 Ensembl 版本
gget.ref("homo_sapiens", release=110)

 # 使用特定的人口普查版本
gget.cellxgene(基因=["PAX7"], census_version="2023-07-25")
 ```

2. **文档gget版本：**
 ```python
 import gget
 print(gget.__version__)
 ```

3. **保存原始数据：**
 ```python
 # 始终保存结果以确保重现性
results = gget.search(["ACE2"],species="homo_sapiens")
 results.to_csv("search_results_2025-01-15.csv", index=False)
 ```

### 处理数据库更新

1. **定期 gget 更新：**
  - 每两周更新 gget 以匹配数据库结构更改
  - 检查发行说明以了解重大更改

2. **错误处理：**
  - 数据库结构更改可能会导致临时故障
  - 检查GitHub问题：https://github.com/pachterlab/gget/issues
  - 如果发生错误则更新gget

3. **API速率限制：**
  - 实现大规模查询的延迟
  - 尽可能使用本地数据库（DIAMOND、COSMIC）
  - 缓存结果以避免重复查询

## 数据库特定最佳实践

### Ensembl
 - 使用物种快捷方式（'人类'， 'mouse')为方便起见
- 指定版本号以实现重现性
- 使用 `gget ref --list_species`

### UniProt
- UniProt ID 比基因名称更稳定 
- Swiss-Prot 注释是手动策划的，更可靠 
- 使用gget 信息中的 PDB 标志仅在需要时（增加运行时间）

### BLAST/BLAT
 - 从默认参数开始，然后优化
  - 使用专用数据库（swissprot、refseq_ Protein）进行重点搜索
  - 考虑基于查询的 E 值截止长度

### 表达数据库
- 基因符号在CELLxGENE
中区分大小写-ARCHS4相关数据基于共表达模式
- 解释结果时考虑组织特异性

### 癌症数据库
- cBioPortal：在本地缓存数据以进行重复分析
- COSMIC：根据您的需求下载适当的数据库子集
- 尊重商业用途的许可协议

## 引用

使用 gget 时，请引用 gget 出版物和基础数据库：

* *gget:**
Luebbert, L. & Pachter, L. (2023)。使用 gget 高效查询基因组参考数据库。生物信息学。 https://doi.org/10.1093/bioinformatics/btac836

* *数据库特定引用：**检查参考文献/目录或数据库网站是否有适当的引用。
