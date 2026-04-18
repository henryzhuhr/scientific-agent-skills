# SRA（序列读取存档）API 参考

## 概述
测序运行元数据：实验、样本、研究和运行。可通过 `db=sra` 的电子实用程序进行访问。返回描述测序实验、平台、库策略和示例属性的 XML 元数据。

## 基本 URL
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

## 身份验证
- **API 密钥**（推荐）：附加 `&api_key=YOUR_KEY`.
- 没有密钥：3 请求/秒。 With key: 10 req/sec.
- 提供 `tool` 和 `email` 参数。

## Key Endpoints

### 1. ESearch -- 搜索 SRA 记录
```
GET esearch.fcgi?db=sra&term=QUERY&retmax=N&retmode=json
```

* *示例 -- 搜索 RNA-seq 实验human:**
```
GET esearch.fcgi?db=sra&term=RNA-seq[Strategy] AND Homo sapiens[Organism]&retmax=5&retmode=json
```
Response:
```json
{
  "esearchresult": {
    "count": "584231",
    "retmax": "5",
    "idlist": ["28574913", "28574912", "28574911", ...]
  }
}
```

* *示例 -- 按加入搜索:**
```
GET esearch.fcgi?db=sra&term=SRP123456[Accession] OR SRR123456[Accession]&retmode=json
```

### 2. EFetch -- 检索完整的 SRA 元数据 (XML仅）
```
GET efetch.fcgi?db=sra&id=IDS&rettype=full&retmode=xml
```

* *示例 -- 获取 SRA 记录的元数据：**
```
GET efetch.fcgi?db=sra&id=28574913&rettype=full&retmode=xml
```
响应（缩写 XML）：
```xml
<EXPERIMENT_PACKAGE_SET>
  <EXPERIMENT_PACKAGE>
    <EXPERIMENT accession="SRX12345" alias="...">
      <TITLE>RNA-seq of human liver tissue</TITLE>
      <STUDY_REF accession="SRP12345"/>
      <DESIGN>
        <LIBRARY_DESCRIPTOR>
          <LIBRARY_STRATEGY>RNA-Seq</LIBRARY_STRATEGY>
          <LIBRARY_SOURCE>TRANSCRIPTOMIC</LIBRARY_SOURCE>
          <LIBRARY_SELECTION>cDNA</LIBRARY_SELECTION>
          <LIBRARY_LAYOUT><PAIRED/></LIBRARY_LAYOUT>
        </LIBRARY_DESCRIPTOR>
      </DESIGN>
      <PLATFORM>
        <ILLUMINA><INSTRUMENT_MODEL>Illumina NovaSeq 6000</INSTRUMENT_MODEL></ILLUMINA>
      </PLATFORM>
    </EXPERIMENT>
    <SUBMISSION accession="SRA12345" center_name="GEO"/>
    <Organization><Name>Some Institute</Name></Organization>
    <STUDY accession="SRP12345">
      <DESCRIPTOR>
        <STUDY_TITLE>Transcriptomic analysis of human tissues</STUDY_TITLE>
        <STUDY_TYPE existing_study_type="Transcriptome Analysis"/>
      </DESCRIPTOR>
    </STUDY>
    <SAMPLE accession="SRS12345">
      <TITLE>Human liver RNA</TITLE>
      <SAMPLE_ATTRIBUTES>
        <SAMPLE_ATTRIBUTE><TAG>tissue</TAG><VALUE>liver</VALUE></SAMPLE_ATTRIBUTE>
        <SAMPLE_ATTRIBUTE><TAG>cell_type</TAG><VALUE>hepatocyte</VALUE></SAMPLE_ATTRIBUTE>
      </SAMPLE_ATTRIBUTES>
    </SAMPLE>
    <RUN_SET>
      <RUN accession="SRR12345" total_spots="45000000" total_bases="9000000000">
        <Statistics nreads="2">
          <Read average="150" count="45000000"/>
        </Statistics>
      </RUN>
    </RUN_SET>
  </EXPERIMENT_PACKAGE>
</EXPERIMENT_PACKAGE_SET>
```

### 3. ESummary -- 简要 SRA摘要
```
GET esummary.fcgi?db=sra&id=IDS&retmode=json
```
返回：实验标题、平台、总运行/点/碱基、创建日期、研究/样本加入作为 `expxml` 和 `runs` 字段中的 XML 字符串。

### 4. ELink -- 交叉链接到其他 NCBI数据库
```
GET elink.fcgi?dbfrom=sra&db=biosample&id=SRA_UID
GET elink.fcgi?dbfrom=sra&db=gds&id=SRA_UID
```

## SRA 登录类型
|前缀|实体|
|--------|--------|
| `SRP` / `ERP` / `DRP` |学习|
| `SRX` / `ERX` / `DRX` |实验|
| `SRS` / `ERS` / `DRS` |样品|
| `SRR` / `ERR` / `DRR` |运行|
| `SRA` |提交|

## 常见搜索模式
```
# By organism and strategy
term=Mus musculus[Organism] AND WGS[Strategy]

# By platform
term=Illumina[Platform] AND ATAC-seq[Strategy] AND human[Organism]

# By study accession
term=SRP123456[Accession]

# By BioProject
term=PRJNA123456[BioProject]

# By date range
term=("2024/01/01"[Publication Date] : "2024/12/31"[Publication Date])

# By library source
term=GENOMIC[Source] AND ChIP-Seq[Strategy] AND cancer[Text Word]

# By read count range
term=10000000:100000000[ReadLength]

# Combined complex query
term=(RNA-Seq[Strategy] AND paired[Layout] AND Homo sapiens[Organism] AND Illumina[Platform])
```

## 速率限制
- 无 API 密钥：3 个请求/秒
- 有 API 密钥：10 个请求/秒
- 对于批量元数据：使用 `usehistory=y` `WebEnv`/`query_key`，批量获取
- 实际序列数据（FASTQ）无法通过电子实用程序获得；使用 SRA 工具包 (`fastq-dump`/`fasterq-dump`)或 SRA 云 URL
