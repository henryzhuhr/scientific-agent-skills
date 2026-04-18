---
name: database-lookup
description: 通过 REST API 搜索 78 个公共科学、生物医学、材料科学和经济数据库。涵盖物理/天文学（NASA、NIST、SDSS、SIMBAD）、地球/环境（USGS、NOAA、EPA）、化学/药物（PubChem、ChEMBL、DrugBank、FDA、KEGG、ZINC、BindingDB）、材料（Materials Project、COD）、生物学/基因组学（Reactome、UniProt、STRING、Ensembl、NCBI Gene、GEO、GTEx、PDB、 AlphaFold、InterPro、BioGRID、基因本体论、dbSNP、gnomAD、ENCODE、人类蛋白质图谱、人类细胞图谱）、疾病/临床（COSMIC、Open Targets、ClinicalTrials.gov、OMIM、ClinVar、GDC/TCGA、cBioPortal、DisGeNET、GWAS Catalog）、监管（FDA、USPTO、SEC EDGAR）、经济/金融（FRED、世界银行、美国财政部）、人口统计（美国人口普查、欧盟统计局、世界卫生组织）。在查找化合物、基因、蛋白质、途径、变体、临床试验、专利、经济指标或任何公共数据库 API 查询时使用。
metadata:
  skill-author: K-Dense Inc.
---

# 数据库查找

您可以通过 REST API 访问 78 个公共数据库。您的工作是找出哪些数据库与用户的问题相关，对其进行查询，然后返回原始 JSON 结果以及您使用的数据库。

## 核心工作流程

1. **理解查询** — 用户在寻找什么？化合物？基因？一条路？专利？表达数据？经济指标？这决定了要命中哪个数据库。

2. **选择数据库** — 使用下面的数据库选择指南。如有疑问，请搜索多个数据库——广撒网总比错过相关数据要好。

3. **阅读参考文件** — 每个数据库在 `references/` 中都有一个参考文件，其中包含端点详细信息、查询格式和示例调用。在进行 API 调用之前，请阅读相关文件。

4. **进行 API 调用** — 请参阅下面的 **进行 API 调用** 部分，了解要在您的平台上使用哪个 HTTP 获取工具。

5. **返回结果** — 始终返回：
  - 来自每个数据库的 **原始 JSON** 响应
  - 使用特定端点查询的**数据库列表**
  - 如果查询未返回结果，请明确说明而不是省略它

## 数据库选择指南

将用户的意图与正确的数据库相匹配。许多查询受益于访问多个数据库。

### 物理与天文学
|用户询问... |主数据库 |另请考虑 |
|---|---|---|
|近地天体、小行星|美国宇航局（NeoWs）| — |
|火星探测器图像|美国宇航局（火星漫游者照片）| — |
|系外行星，轨道参数|美国宇航局系外行星档案 | — |
|天文物体的名称/坐标|辛巴德 | SDSS |
|星系/恒星光谱、光度测定 | SDS | SIMBAD |
|物理常数|美国国家标准技术研究院 | — |
|原子光谱、谱线| NIST（ASD）| — |

### 地球与环境科学
|用户询问... |主数据库 |还要考虑 |
|---|---|---|
|地震、地震事件|美国地质调查局地震 | — |
|水数据、径流量、地下水 |美国地质调查局水服务 | — |
|天气（当前、预报、历史）|打开天气地图 | NOAA |
|气候数据、历史气象站| NOAA（CDO）| — |
|空气质量、有毒物质释放| EPA（环境事实）| — |

### 化学与药物
|用户询问... |主数据库 |另请考虑 |
|---|---|---|
|化合物、分子 |公共化学| ChEMBL |
|分子特性（重量、分子式、SMILES）|公共化学| — |
|药物同义词、CAS 编号 | PubChem（同义词）|药物银行|
|生物活性数据、IC50、结合测定 |化学分子生物学 | BindingDB、PubChem |
|药物结合亲和力（Ki、IC50、Kd）| ChEMBL、BindingDB | PubChem |
|药物-靶点相互作用| ChEMBL，药物银行 | BindingDB，开放目标 |
|蛋白质靶标的配体（由 UniProt 提供）|绑定数据库 | ChEMBL |
|从化合物结构识别目标| BindingDB（SMILES 相似度）| ChEMBL |
|药品标签、不良事件、召回 | FDA（OpenFDA）|每日医学|
|药品标签（结构性产品标签）|每日医学 | FDA（OpenFDA）|
|药物药理学、适应症|药物银行| FDA |
|化学交叉引用 | PubChem（外部参照）| ChEMBL |
|用于筛选的市售化合物 |锌 | PubChem |
|相似性/子结构搜索（可购买）|锌 | PubChem、ChEMBL |
|类药化合物库、构建模块 |锌 | — |
| FDA 批准的药物结构 |锌（FDA 子集）| PubChem、FDA |
|复合可购买性，供应商目录|锌 | — |

### 材料科学与晶体学
|用户询问... |主数据库 |还要考虑 |
|---|---|---|
|分子式或元素材料|材料项目|货到付款|
|带隙，电子结构|材料项目| — |
|晶体结构、CIF 文件 |货到付款 |材料项目|
|弹性/机械性能 |材料项目| — |
|形成能、热力学|材料项目| — |
|晶胞参数、空间群 |货到付款 |材料项目|

### 生物学与基因组学
|用户询问... |主数据库 |还要考虑 |
|---|---|---|
|生物途径|反应组，KEGG | — |
|基因/蛋白质处于什么途径？ Reactome（绘图），KEGG | — |
|酶动力学、催化活性|布伦达 | KEGG |
|代谢组学研究、代谢物概况 |代谢组学工作台| PubChem |
| m/z 或精确质量查找 |代谢组学工作台 (moverz/exactmass) | PubChem |
|蛋白质序列、功能、注释 |尤尼普罗特|合奏|
|蛋白质-蛋白质相互作用|字符串 | BioGRID |
|基因信息、基因组位置| NCBI 基因 |合奏|
|基因组序列、变体、转录本 |合奏 | NCBI基因|
|基因表达数据集 | GEO（NCBI 电子实用程序）| — |
|跨组织基因表达| GTEx |人类蛋白质图谱|
|基因表达特征 (CMap/L1000) | LINCS L1000 |地理|
|基因集富集与 GEO |鲁玛GEO |地理|
|蛋白质序列 (NCBI) | NCBI 蛋白质 | UniProt |
|分类学分类| NCBI 分类 | — |
| SNP/变异数据 (dbSNP) | dbSNP | ClinVar，gnomAD |
|群体变异频率|侏儒AD | dbSNP |
|测序运行元数据 | SRA | ENA、GEO |
|核苷酸序列（欧洲档案）|埃纳 | SRA、NCBI基因|
|基因组组装、原始读取（欧洲）|埃纳 | SRA，合奏|
|序列加入的交叉引用| ENA（外部参考）| NCBI 基因，UniProt |
|基因组注释、轨迹 | UCSC 基因组浏览器 |合奏|
| 3D 蛋白质结构（实验）| PDB（RCSB）| EMDB |
| 3D 蛋白质结构（预测）| AlphaFold 数据库 | PDB |
|电子显微镜图、冷冻电子显微镜结构 | EMDB | PDB |
|蛋白质家族、结构域 | InterPro | UniProt |
|化学实体（生物）|切埃比 | PubChem |
|蛋白质/遗传相互作用|生物网格|字符串 |
|基因功能注释（GO ter女士）|快走 |基因本体|
|调控元件、ChIP-seq、ATAC-seq |编码 | — |
| TF 结合概况/基序 |贾斯帕|编码|
|跨组织蛋白表达|人类蛋白质图谱| UniProt |
|单细胞图谱项目|人类细胞图谱| — |
|蛋白质组学数据集 |骄傲| — |
|小鼠基因数据|鼠标地雷 | NCBI基因|
|质粒库|添加基因 | — |

* *生物体/物种很重要。**大多数生物学数据库涵盖多种生物体。如果用户的查询是关于特定的生物体，请明确地传递它——不要假设是人类。常见模式：Ensembl 在 URL 路径中使用 `{species}`（例如 `homo_sapiens`），STRING/BioGRID/QuickGO 使用 NCBI 分类单元 ID（`species=9606` 表示人类，`10090` 表示小鼠），UniProt 在搜索查询中使用 `organism_id:9606`，KEGG 使用生物体代码（`hsa`， `mmu`）。 GTEx 和人类蛋白质图谱仅适用于人类。各数据库具体参数请查看参考文件。

### 疾病与临床
|用户询问... |主数据库 |另请考虑 |
|---|---|---|
|癌症中的体细胞突变宇宙 |开放目标，cBioPortal |
|癌症基因组学 (TCGA) | GDC (TCGA) | COSMIC，cBioPortal |
|癌症研究突变、CNA、表达 | cBioPortal | GDC (TCGA)、COSMIC |
|肿瘤临床数据（生存、分期）| cBioPortal | GDC (TCGA) |
|药物-靶标-疾病关联|开放目标 | ChEMBL |
|基因-疾病关联| DisGeNET |开放目标，君主|
|孟德尔疾病与基因的关系|欧米姆| NCBI基因|
|变异的临床意义| ClinVar (NCBI) | OMIM |
| GWAS SNP 性状关联 | GWAS 目录 | — |
|疾病-表型-基因联系|君主倡议| HPO|
|表型本体论，HPO 术语 |磷酸二氢钾|君主|
|药物基因组学、药物-基因相互作用| ClinPGx (PharmGKB) |药物银行|
|药物/疾病的临床试验|临床试验.gov | FDA |
|疾病相关表达数据|地理 |开放目标 |

### 专利与监管
|用户询问... |主数据库 |还要考虑 |
|---|---|---|
|按关键字或技术划分的专利 |美国专利商标局（专利查看）| — |
|发明人或受让人的专利|美国专利商标局（专利查看）| — |
|专利申请状况|美国专利商标局 (PEDS) | — |
|商标查询|美国专利商标局 (TSDR) | — |
| SEC 公司备案，10-K、10-Q | SEC 埃德加 | — |

### 经济与金融
|用户询问... |主数据库 |另请考虑 |
|---|---|---|
|美国经济时间序列（GDP、CPI、利率）|弗雷德 |东亚银行|
|就业、工资、劳动力统计|美国劳工统计局 |弗雷德 |
| GDP、国民账户|东亚银行 |弗雷德，世界银行 |
|国际发展指标|世界银行|弗雷德 |
|利率、货币供应量|美联储|弗雷德 |
|欧元汇率、欧洲央行货币统计|欧洲央行 | — |
|美国债务、收益率曲线、财政数据|美国财政部|弗雷德 |
|股票价格、外汇、加密货币 |阿尔法优势| — |
|跨多个主题的统计数据 |数据共享 | — |

### 社会科学与人口统计学
|用户询问... |主数据库 |另请考虑 |
|---|---|---|
|美国人口、住房、收入数据|美国人口普查|数据共享|
|欧盟统计（经济、贸易、卫生）|欧盟统计局|世界银行|
|全球健康指标（死亡率、疾病）|世界卫生组织 GHO |世界银行|

### 跨域查询
|用户询问... |主数据库 |还要考虑 |
|---|---|---|
|关于化合物的一切 | PubChem + ChEMBL + DrugBank | BindingDB、ZINC、Reactome、FDA |
|关于基因的一切| NCBI 基因 + UniProt + Ensembl | Reactome、STRING、COSMIC、cBioPortal、ENA |
|关于变体的一切 | dbSNP + ClinVar + gnomAD | GWAS 目录、COSMIC、cBioPortal |
|药物靶点通路| ChEMBL + 反应组 |开放目标，GEO |
|化学发明的现有技术|美国专利商标局 + PubChem | ChEMBL |
|关于材料的一切 |材料项目 + COD | — |
|美国经济概况|弗雷德 + BLS + BEA |美联储|

当用户的查询跨越多个域时（例如“我们对阿司匹林了解多少”或“找到有关BRCA1的一切”），并行查询所有相关数据库。

## 通用标识符格式

不同的数据库使用不同的标识符系统。如果查询失败，则可能是标识符格式错误。这是一个快速参考：

|标识符 |格式|示例|由 |
|---|---|---|---|
| 使用UniProt 加入 | `P#####` 或 `Q#####` | `P04637` (TP53) | UniProt、STRING、AlphaFold、Reactome 作图 |
|整体基因 ID | `ENSG###########` | `ENSG00000141510` | Ensembl、开放目标、GTEx |
| NCBI 基因 ID |整数 | `7157` (TP53) | NCBI 基因、GEO、DisGeNET、HPO |
| HGNC ID | `HGNC:#####` | `HGNC:11998` |君主|
| PubChem CID |整数 | `2244`（阿司匹林）| PubChem |
|锌 ID | `ZINC` + 15 位数字 | `ZINC000000000053`（阿司匹林）|锌 |
| ENA 项目 | `PRJEB` + 数字 | `PRJEB40665` | ENA |
| ENA 运行 | `ERR` + 数字 | `ERR1234567` | ENA |
| ENA实验| `ERX` + 数字 | `ERX1234567` | ENA |
| ENA 样本 | `ERS` + 数字 | `ERS1234567` | ENA |
| ChEMBL ID | `CHEMBL####` | `CHEMBL25`（阿司匹林）| ChEMBL |
| Reactome 稳定 ID | `R-HSA-######` | `R-HSA-109581` |反应组|
|惠普术语 | `HP:#######` | `HP:0001250`（扣押）| HPO（URL 冒号编码为 %3A）|
|蒙多病 | `MONDO:#######` | `MONDO:0007947` |君主|
| GO 术语 | `GO:#######` | `GO:0008150` | QuickGO，基因本体|
| dbSNP rsID | dbSNP rsID | `rs########` | `rs334` | dbSNP、GWAS 目录、gnomAD |
|基因代码 ID | `ENSG###.##`（版本）| `ENSG00000139618.17` | GTEx（需要版本后缀）|

### 标识符解析

当数据库无法识别标识符时，请使用以下工作流程进行转换：

* *基因**：符号（例如“TP53”）→在**NCBI基因**中查找（按符号搜索）→获取NCBI基因ID→通过**Ensembl**转换为Ensembl ID `/xrefs/symbol/homo_sapiens/{symbol}`，或通过 **UniProt** 搜索 (`gene_exact:{symbol} AND organism_id:9606`).

 加入 UniProt**化合物**：名称 → **PubChem** `/compound/name/{name}/cids/JSON` → 获取 CID → 通过 **UniChem** 或 **ChEMBL** 分子搜索转换为 ChEMBL ID。如果名称查找失败，请尝试 SMILES、InChIKey 或 CAS 编号。

* *变体**：rsID（例如“rs334”）直接在 **dbSNP**、**ClinVar**、**GWAS Catalog**、**gnomAD** 中工作。对于基因组坐标，使用 **Ensembl** VEP 获取结果注释和链接的 rsID。

* *疾病**：名称 → **开放目标** 或 **Monarch** 搜索 → 获取 EFO 或 MONDO ID → 在下游查询中使用。

## POST-Only APIs

这些数据库需要 HTTP POST，并且**无法与 WebFetch**（仅 GET）一起使用。通过平台的 shell 工具使用 `curl`：

|数据库|为什么需要 POST |示例 |
|---|---|---|
|开放目标 | GraphQL 端点 | `curl -X POST -H "Content-Type: application/json" -d '{"query":"..."}' https://api.platform.opentargets.org/api/v4/graphql` |
|侏儒AD | GraphQL 端点 | `curl -X POST -H "Content-Type: application/json" -d '{"query":"..."}' https://gnomad.broadinstitute.org/api` |
|鲁玛GEO |仅后期充实 | `curl -X POST -H "Content-Type: application/json" -d '{"genes":["..."]}' https://rummageo.com/api/enrich` |
| GDC/TCGA |复杂的过滤查询| `curl -X POST -H "Content-Type: application/json" -d '{"filters":...}' https://api.gdc.cancer.gov/ssms` |
| SEC 埃德加 |需要 User-Agent 标头 | `curl -H "User-Agent: YourApp you@email.com" https://efts.sec.gov/LATEST/search-index?q=...` |

## API 密钥和访问限制

某些数据库需要 API 密钥或具有访问限制。当需要 API 密钥时：

1. **首先检查当前环境** — 密钥可能已导出为 shell 环境变量（例如 `$FRED_API_KEY`）。直接从环境中读取。
2. **回退到 `.env`** — 如果该变量不在环境中，请检查当前工作目录中的 `.env` 文件。
3. **如果两者都没有** — 在没有密钥的情况下继续（大多数 API 仍然在较低的速率限制下工作）并告诉用户缺少哪个密钥以及如何获取密钥。

### 需要 API 密钥的数据库（免费注册）

|数据库|环境变量 |注册网址 |
|---|---|---|
|弗雷德 | `FRED_API_KEY` | https://fred.stlouisfed.org/docs/api/api_key.html |
|东亚银行 | `BEA_API_KEY` | https://apps.bea.gov/API/signup/ |
|美国劳工统计局 | `BLS_API_KEY` | https://data.bls.gov/registrationEngine/ |
| NCBI（GEO、基因）| `NCBI_API_KEY` | https://www.ncbi.nlm.nih.gov/account/settings/ |
|开放FDA | `OPENFDA_API_KEY` | https://open.fda.gov/apis/authentication/ |
|美国专利商标局（专利查看）| `PATENTSVIEW_API_KEY` | https://patentsview.org/apis/keyrequest |
|数据共享 | `DATACOMMONS_API_KEY` |谷歌云控制台|
|材料项目| `MP_API_KEY` | https://materialsproject.org（免费帐户）|
|美国宇航局 | `NASA_API_KEY` | https://api.nasa.gov（免费，DEMO_KEY可用）|
| NOAA（CDO）| `NOAA_API_KEY` | https://www.ncdc.noaa.gov/cdo-web/token |
|打开天气地图 | `OPENWEATHERMAP_API_KEY` | https://openweathermap.org/appid |
|欧米姆| `OMIM_API_KEY` | https://omim.org/api（免费学术）|
|生物网格| `BIOGRID_API_KEY` | https://webservice.thebiogrid.org（免费）|
|阿尔法优势| `ALPHAVANTAGE_API_KEY` | https://www.alphavantage.co/support/#api-key |
|美国人口普查| `CENSUS_API_KEY` | https://api.census.gov/data/key_signup.html |
| DisGeNET | `DISGENET_API_KEY` | https://www.disgenet.org（免费学术）|
|添加基因 | `ADDGENE_API_KEY` | https://www.addgene.org（免费帐户）|
| LINCS L1000（线索）| `CLUE_API_KEY` | https://clue.io（免费学术）|

这些都是免费获取的。 API 无需密钥即可工作，但速率限制较低。始终先尝试使用密钥 - 如果未设置环境变量，请在不使用密钥的情况下继续，并在响应中注明速率限制可能较低。

### 具有付费或受限访问权限的数据库

|数据库|限制|免费替代|
|---|---|---|
|药物银行|需要付费 API 许可证 |使用 **ChEMBL** + **PubChem** + **OpenFDA** 代替 |
|宇宙 |需要免费学术注册（JWT auth）|使用 **开放目标** 获取癌症突变数据 |
|布伦达 |需要免费注册（SOAP，不是 REST）|使用 **KEGG** 获取酶/通路数据 |

当数据库需要付费访问或用户尚未设置的注册时：
1. **退回到可以回答相同问题的免费替代方案**
2. **告诉用户**您无法访问哪个数据库、原因以及您使用了什么替代
3. 如果用户特别请求受限数据库，请解释访问要求，以便他们进行设置

### 加载 API 密钥

* *步骤 1 — 检查当前环境。** 该密钥可能已导出为 shell 变量。例如，在 Claude Code 中，您可以使用 Bash 检查：`echo $FRED_API_KEY`。如果该变量已设置且非空，则使用它。

* *步骤 2 — 检查 `.env` 文件。**如果未设置环境变量，则从当前工作目录读取 `.env`。格式：
```
FRED_API_KEY=your_key_here
BEA_API_KEY=your_key_here
```

* *步骤 3 — 无需密钥即可继续。** 如果两个源都没有密钥，则无需密钥即可继续（大多数 API 仍以较低的速率限制工作）并向用户提及这一点。

## 进行 API 调用

使用环境的 HTTP 获取工具来调用 REST 端点。工具名称因平台而异：

|平台| HTTP 获取工具 |后备|
|---|---|---|
|克劳德·代码 | `WebFetch` | `curl` 通过 Bash |
|双子座 CLI | `web_fetch` | `curl` 通过外壳 |
|风帆冲浪 | `read_url_content` | `curl` 通过终端 |
|光标|没有专用的抓取工具| `curl` 通过 `run_terminal_cmd` |
|法典 CLI |没有专用的抓取工具| `curl` 通过 `shell` |
|克莱恩 |没有专用的抓取工具| `curl` 通过 `execute_command` |

 如果您无法识别您的平台或获取工具失败，请通过任何可用的 shell/终端工具回退到 `curl`。示例：
```bash
curl -s -H "Accept: application/json" "https://api.example.com/endpoint"
```

### 请求指南

- 在支持的情况下设置 `Accept: application/json` 标头
- 对查询参数中的特殊字符进行 URL 编码 — SMILES 字符串（`/`、`#`、`=`、 `@`）、带括号的复合名称和带冒号的本体术语（`HP:0001250` → `HP%3A0001250`）是常见的失败来源。对于 `curl`，请使用 `--data-urlencode` 以确保安全。
- **并行 OK**：查询*不同*数据库（例如，PubChem + ChEMBL + Reactome）时，并行运行它们 - 大多数 API 都有很大的速率限制。
- **将请求序列化到速率受限的 API**：NCBI API（Gene、 GEO、蛋白质、分类学、dbSNP、SRA），无密钥时为 3 请求/秒，有密钥时为 10 请求/秒。另请注意：Ensembl（15 个请求/秒）、BLS v1（25 个请求/天，无密钥）、SEC EDGAR（10 个请求/秒）、NOAA（5 个请求/秒，带令牌）。
- 如果出现速率限制错误（HTTP 429 或 503），请短暂等待并重试一次

### 错误恢复

如果 API 返回错误或空结果：
1. **检查标识符格式** — 使用上面的通用标识符格式表。基因符号可能需要先转换为 NCBI Gene ID 或 Ensembl ID。
2. **尝试替代标识符** — 如果复合名称在 PubChem 中失败，请尝试 SMILES、InChIKey 或 CID。如果基因符号失败，请尝试 NCBI 基因 ID.
3. **尝试不同的数据库** — 如果一个数据库出现故障或未返回任何内容，请检查选择指南中的“另请考虑”列以获取替代方案。
4. **报告失败** — 告诉用户哪个数据库失败、错误以及您尝试了什么。

### 分页

许多 API 返回分页结果 — 如果您只读取第一页，则可能会丢失数据。常见模式：

- **偏移/限制**：`offset=0&limit=100` → 按下一页的限制增加偏移量（ChEMBL、FRED、NOAA、USGS、NCBI E-utilities、ENA、GDC、FDA）
- **基于光标**：响应包括 `nextPageToken` 或 `cursor` 值 - 将其传递到下一个请求（ClinicalTrials.gov、UniProt）
- **页码**：`page=1&per_page=50` → 增量页面（世界银行、cBioPortal、ZINC）

 检查参考文件中每个数据库的具体分页参数。如果响应包含 `total`、`totalCount` 或 `next`，且返回结果数小于总数，则页数较多。

 对于定向查找（单基因、单化合物），第一页通常就足够了。当用户需要综合结果时分页（例如，“X 的所有临床试验”或“基因 Y 中的所有已知变异”）。

## 输出格式

像这样构建您的响应：

```
## Databases Queried
- **PubChem** — /compound/name/aspirin/property/...
- **Reactome** — /search/query?query=aspirin

## Results

### PubChem
[raw JSON response]

### Reactome
[raw JSON response]
```

 如果结果非常大，请呈现最相关的部分，并注意有其他数据可用。但默认显示完整的原始 JSON — 用户要求它。

## 添加新数据库

这项技能旨在不断成长。每个数据库都是`references/`中一个独立的参考文件。添加新数据库：

1. 按照与现有文件 
2 相同的格式创建 `references/<database-name>.md`。在上面的数据库选择指南中添加一个条目
3. 参考文件应包括：基本 URL、关键端点、查询参数格式、示例调用、速率限制和响应结构

## 可用数据库

在进行任何 API 调用之前阅读相关参考文件。

### 物理与天文学
|数据库|参考文件|涵盖内容 |
|---|---|---|
|美国宇航局 | `references/nasa.md` |近地天体小行星、火星探测器、APOD |
|美国宇航局系外行星档案 | `references/nasa-exoplanet-archive.md` |系外行星，轨道参数|
|美国国家标准技术研究院 | `references/nist.md` |物理常数，原子光谱|
| SDS | `references/sdss.md` |星系/恒星光谱、光度测定|
|辛巴德 | `references/simbad.md` |天文物体目录 |

### 地球与环境科学
|数据库|参考文件|涵盖内容 |
|---|---|---|
|美国地质勘探局| `references/usgs.md` |地震、水利数据|
|美国国家海洋和大气管理局 | `references/noaa.md` |气候、气象站数据|
|美国环保局| `references/epa.md` |空气质量、有毒物质释放|
|打开天气地图 | `references/openweathermap.md` |当前天气/预报 |

### 化学与药物
|数据库|参考文件|涵盖内容 |
|---|---|---|
|公共化学| `references/pubchem.md` |化合物、性质、同义词 |
|化学分子生物学 | `references/chembl.md` |生物活性、药物发现|
|药物银行| `references/drugbank.md` |药物数据、相互作用（付费）|
| FDA（OpenFDA）| `references/fda.md` |药品标签、不良事件、召回|
|每日医学 | `references/dailymed.md` |药品标签 (NIH/NLM) |
|凯格 | `references/kegg.md` |通路、基因、化合物|
|切埃比 | `references/chebi.md` |具有生物意义的化学实体|
|锌 | `references/zinc.md` |市售化合物，虚拟筛选|
|绑定数据库 | `references/bindingdb.md` |实验测量的结合亲和力 |

### 材料科学
|数据库|参考文件|涵盖内容 |
|---|---|---|
|材料项目| `references/materials-project.md` |带隙、弹性特性、晶体结构|
|货到付款 | `references/cod.md` |晶体结构，CIF 文件 |

### 生物学与基因组学
|数据库|参考文件|涵盖内容 |
|---|---|---|
|反应组 | `references/reactome.md` |生物途径、反应|
|布伦达 | `references/brenda.md` |酶动力学、催化 (SOAP) |
|尤尼普罗特| `references/uniprot.md` |蛋白质序列、功能|
|字符串 | `references/string.md` |蛋白质-蛋白质相互作用|
|合奏 | `references/ensembl.md` |基因组、变异、序列 |
| NCBI 基因 | `references/ncbi-gene.md` |基因信息、链接|
| NCBI 蛋白质 | `references/ncbi-protein.md` |蛋白质序列、记录|
| NCBI 分类 | `references/ncbi-taxonomy.md` |分类学分类|
| GEO（NCBI）| `references/geo.md` |基因表达数据集|
| GTEx | `references/gtex.md` |跨组织基因表达|
| PDB| `references/pdb.md` |蛋白质3D结构|
| AlphaFold 数据库 | `references/alphafold.md` |预测的蛋白质结构|
| EMDB | `references/emdb.md` |电子显微镜图|
| InterPro | `references/interpro.md` |蛋白质家族、结构域 |
|生物网格| `references/biogrid.md` |蛋白质/遗传相互作用|
|基因本体论| `references/gene-ontology.md` | GO术语、基因注释|
|快走 | `references/quickgo.md` | GO注释（EBI，推荐）|
| dbSNP | `references/dbsnp.md` | SNP/变异数据|
| SRA | `references/sra.md` |测序运行元数据 |
|侏儒AD | `references/gnomad.md` |群体变异频率 (POST) |
| UCSC 基因组浏览器 | `references/ucsc-genome.md` |基因组注释、轨迹 |
|编码 | `references/encode.md` | DNA 元件、ChIP-seq、ATAC-seq |
|贾斯帕| `references/jaspar.md` | TF 结合图谱/基序 |
|人类蛋白质图谱| `references/human-protein-atlas.md` |跨组织蛋白表达|
|人类细胞图谱| `references/hca.md` |单细胞图谱数据|
| LINCS L1000 | `references/lincs-l1000.md` |基因表达特征（CMap）|
|鲁玛GEO | `references/rummageo.md` | GEO 基因集富集 (POST) |
|骄傲| `references/pride.md` |蛋白质组学数据存储库|
|代谢组学工作台| `references/metabolomics-workbench.md` |代谢组学研究，代谢物|
|鼠标地雷 | `references/mousemine.md` |小鼠基因组信息学|
|埃纳 | `references/ena.md` |核苷酸序列、读数、组装、分类 (EMBL-EBI) |
|添加基因 | `references/addgene.md` |质粒库|

### 疾病与临床
|数据库|参考文件|涵盖内容 |
|---|---|---|
|开放目标 | `references/opentargets.md` |目标疾病关联 (POST) |
|宇宙 | `references/cosmic.md` |癌症中的体细胞突变|
| ClinPGx (PharmGKB) | `references/clinpgx.md` |药物基因组学|
|临床试验.gov | `references/clinicaltrials.md` |临床试验注册|
|欧米姆| `references/omim.md` |孟德尔疾病基因数据|
|临床Var | `references/clinvar.md` |变异临床意义|
| GDC (TCGA) | `references/tcga-gdc.md` |癌症基因组学、突变（POST）|
| cBioPortal | `references/cbioportal.md` |癌症研究突变、CNA、表达、临床数据|
| DisGeNET | `references/disgenet.md` |基因-疾病关联|
| GWAS 目录 | `references/gwas-catalog.md` | GWAS SNP 性状关联 |
|君主倡议| `references/monarch.md` |疾病-表型-基因联系|
|磷酸二氢钾| `references/hpo.md` |人类表型本体 |

### 专利与监管
|数据库|参考文件|涵盖内容|
|---|---|---|
|美国专利商标局 | `references/uspto.md` |专利、商标|
| SEC 埃德加 | `references/sec-edgar.md` |公司备案（需要用户代理标头） |

### 经济与金融
|数据库|参考文件|涵盖内容 |
|---|---|---|
|弗雷德 | `references/fred.md` |美国经济时间序列|
|美联储| `references/federal-reserve.md` |货币/金融数据|
|东亚银行 | `references/bea.md` | GDP，国民账户|
|美国劳工统计局 | `references/bls.md` |就业、工资、CPI |
|世界银行| `references/worldbank.md` |发展指标|
|欧洲央行 | `references/ecb.md` |欧元汇率、货币统计|
|美国财政部| `references/treasury.md` |债务、收益率曲线、财政数据|
|阿尔法优势| `references/alphavantage.md` |股票、外汇、加密货币|
|数据共享 | `references/datacommons.md` |统计知识图谱|

### 社会科学与人口统计
|数据库|参考文件|涵盖内容 |
|---|---|---|
|美国人口普查| `references/census.md` |人口、住房、经济调查|
|欧盟统计局| `references/eurostat.md` |欧盟统计|
|世界卫生组织 GHO | `references/who.md` |全球健康指标|
