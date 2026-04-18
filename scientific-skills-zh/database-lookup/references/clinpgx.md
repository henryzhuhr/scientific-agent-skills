# PharmGKB（临床药物基因组学）

## 基本 URL
```
https://api.pharmgkb.org/v1/data/
```

## Auth
只读访问不需要 API 密钥。

## 关键端点

### 常规搜索
```
GET https://api.pharmgkb.org/v1/search?q={term}&page=0&size=10
```

### 基因数据
```
GET /gene?symbol={symbol}
```
示例：`/gene?symbol=CYP2D6`

响应包括：id、symbol、chromosome、hasGuideline、hasClinicalAnnotation、cpicGene

### Drug数据
```
GET /drug?name={name}
```
示例：`/drug?name=warfarin`

响应包括：id、name、genericNames、tradeNames、rxNormId、atcCodes

### 临床注释（药物-基因相互作用）
```
GET /clinicalAnnotation?gene={symbol}&drug={name}&level={level}
```

E证据水平：`1A`、`1B`、`2A`、`2B`、`3`、`4`

示例：
```
/clinicalAnnotation?gene=CYP2C19&drug=clopidogrel&level=1A
```

响应包括：水平、基因、药物、表型、显着性、变体，url

### CPIC/DPWG 指南
```
GET /guideline?gene={symbol}&drug={name}&source=CPIC
```

### 药代动力学途径
```
GET /pathway?drug={name}
```

### 药物标签（FDA、 EMA)
```
GET /drugLabel?drug={name}&source=FDA
```

## 速率限制
没有硬性发布的限制。讲道理。通过 PharmGKB 下载页面获取批量数据。
