# UCSC 基因组浏览器 REST API 参考

## 概述
提供对基因组注释、基因轨迹、序列数据、
 以及 UCSC 基因组浏览器数据库中的其他资源的编程访问。

## 基本 URL
`https://api.genome.ucsc.edu`

## Auth
不需要（公开，未经身份验证）。

## 所有端点的响应格式
JSON。

## 关键端点

### 列出可用基因组
```
GET /list/ucscGenomes
```
返回所有基因组组件（hg38、mm39 等）及描述。

### 列出曲目对于基因组
```
GET /list/tracks?genome=hg38
```
返回可用于指定程序集的所有注释轨道。

### 列出染色体/重叠群
```
GET /list/chromosomes?genome=hg38
```
可选：添加`&track=<trackName>`以限制该轨道中数据的染色体。

### 列出a中的表track
```
GET /list/schema?genome=hg38&track=knownGene
```
返回表模式，包括字段名称、类型和SQL创建语句。

### 获取轨迹数据（注释）
```
GET /getData/track?genome=hg38&track=knownGene&chrom=chr1&start=11873&end=14409
```
参数：
- `genome` -- 程序集名称（必填）
- `track` -- 轨道名称（必填）
- `chrom` -- 染色体（可选，限制为 1 个 chrom）
- `start`、`end` -- 从 0 开始的半开坐标（可选，需要 chrom）
- `maxItemsOutput` -- 返回的项目数量限制（默认）某些曲目为 1000)

### 获取序列
```
GET /getData/sequence?genome=hg38&chrom=chr1&start=11873&end=11893
```
 返回指定区域的 DNA 序列。坐标是从 0 开始的半开。

### 搜索术语
```
GET /search?search=BRCA1&genome=hg38
```
返回跨轨迹的匹配位置（基因名称、种质等）。

### 获取中心基因组数据
```
GET /list/hubGenomes?hubUrl=<hubURL>
```
列出轨迹中心中可用的基因组。

## 示例致电

### 获取某个区域的RefSeq基因注释
```
GET https://api.genome.ucsc.edu/getData/track?genome=hg38&track=ncbiRefSeq&chrom=chr17&start=43044295&end=43125483
```

### 获取DNA序列
```
GET https://api.genome.ucsc.edu/getData/sequence?genome=hg38&chrom=chr7&start=117119148&end=117119178
```

### 响应示例（序列）
```json
{
  "genome": "hg38",
  "chrom": "chr7",
  "start": 117119148,
  "end": 117119178,
  "dna": "atgcagatatcagcgatgcagatcgatcg..."
}
```

### 响应示例（轨迹）数据）
```json
{
  "genome": "hg38",
  "track": "ncbiRefSeq",
  "chrom": "chr17",
  "start": 43044295,
  "end": 43125483,
  "ncbiRefSeq": [
    {
      "chrom": "chr17",
      "chromStart": 43044295,
      "chromEnd": 43125483,
      "name": "NM_007294.4",
      "strand": "-",
      "name2": "BRCA1",
      "exonCount": 23,
      "exonStarts": "43044295,43047642,...",
      "exonEnds": "43045802,43047703,..."
    }
  ]
}
```

## 坐标系
所有坐标都是**基于0，半开**（标准BED格式）。这意味着 
`start` 是包容性的，而 `end` 是排他性的。批量下载应使用
 MySQL公共服务器（genome-mysql.soe.ucsc.edu）或BigBed/BigWig文件下载
- 返回非常大结果集的请求可能会通过`maxItemsOutput`

## 常见基因组值
- `hg38` -- Human GRCh38 （当前）
- `hg19` -- 人类 GRCh37
- `mm39` -- 小鼠 GRCm39
- `mm10` -- 小鼠 GRCm38
- `dm6` --果蝇
- `danRer11` -- 斑马鱼
- `sacCer3` -- 酵母
