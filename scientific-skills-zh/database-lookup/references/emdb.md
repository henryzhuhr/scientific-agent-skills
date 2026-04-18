# EMDB（电子显微镜数据库）

## 基本 URL
```
https://www.ebi.ac.uk/emdb/api/
```

## 身份验证
无需身份验证。

## 关键端点

|端点|描述 |
|----------|-------------|
| `/entry/{emdb_id}` |完整条目元数据（例如 EMD-1234）|
| `/entry/map/{emdb_id}` |地图/体积元数据 |
| `/entry/experiment/{emdb_id}` |实验详情|
| `/entry/fitted/{emdb_id}` |适配PDB型号|
| `/search/{query}?rows={n}` |按关键字搜索条目 |

## 调用示例
```
# Entry metadata
https://www.ebi.ac.uk/emdb/api/entry/EMD-1234

# Search for ribosome entries
https://www.ebi.ac.uk/emdb/api/search/ribosome?rows=5

# Experimental details
https://www.ebi.ac.uk/emdb/api/entry/experiment/EMD-1234
```

## 响应格式
JSON。搜索包括分页和匹配条目数组。

## 速率限制
EBI 合理使用政策。可通过 FTP 进行批量访问的地图文件 (MRC/CCP4)。
