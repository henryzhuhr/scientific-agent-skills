# COSMIC（癌症体细胞突变目录）

## 基本 URL
```
https://cancer.sanger.ac.uk/cosmic/api/v1/
```

## Auth
* *需要注册。** 免费学术帐户或付费商业许可证。

登录获取 JWT 令牌：
```
POST /auth/login
Content-Type: application/json
{"email": "you@example.com", "password": "yourpassword"}
```
将令牌传递为： `Authorization: Bearer <token>`

## 关键端点

### 按基因搜索突变
```
GET /mutations/search?q={gene_symbol}&page=1&page_size=5
```

### 获取基因信息
```
GET /genes/{gene_symbol}
```
示例：`/genes/BRAF`

响应包括：gene_symbol、gene_name、染色体，cancer_census（bool），tier，mutation_count，sample_count

### 通过COSMIC ID获取特定突变
```
GET /mutations/{cosmic_mutation_id}
```
示例：`/mutations/COSV56056643`

响应包括：gene，cds_mutation，aa_mutation，mutation_type，fathmm_prediction，genome_coordinates， Organization_distribution

### 癌症基因普查
```
GET /cancer-gene-census?tier=1&page_size=10
```

### 组织/组织学突变
```
GET /mutations/distribution/{gene_symbol}
```

## 速率限制
未正式发布。批量数据需要 SFTP 下载（已许可）。

## 重要
- COSMIC 要求对所有 API 调用进行身份验证
- 商业用途需要付费许可证
- 对于大型查询，通过 SFTP 进行批量数据访问优于 API 
- API 结构可能会因 COSMIC 版本而变化
