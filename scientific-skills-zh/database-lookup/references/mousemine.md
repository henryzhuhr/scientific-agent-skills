# MouseMine（小鼠基因组信息学，基于 InterMine）

## 基本 URL
```
https://www.mousemine.org/mousemine/service
```

## Auth
对于大多数查询没有身份验证。保存列表需要免费帐户令牌。

## 关键端点

|端点|描述 |
|----------|-------------|
| `/search?q={query}&format=json` |跨所有对象的关键字搜索|
| `/template/results?name={template}&op1=LOOKUP&value1={value}&format=json` |运行预构建的模板查询 |
| `/query/results`（邮政）|运行自定义 PathQuery (XML) |
| `/model` |检索数据模型 |

## 调用示例
```
# Keyword search for Brca1
https://www.mousemine.org/mousemine/service/search?q=Brca1&format=json

# Template: Gene → GO terms
https://www.mousemine.org/mousemine/service/template/results?name=Gene_GO&op1=LOOKUP&value1=Pax6&format=json
```

## 自定义查询（POST）
```
POST /query/results
Content-Type: application/x-www-form-urlencoded
query=<query model="genomic" view="Gene.symbol Gene.name" sortOrder="Gene.symbol asc"><constraint path="Gene.organism.name" op="=" value="Mus musculus"/></query>&format=json
```

## 响应格式
JSON：`{"results": [...], "statusCode": 200}`。还通过 `format` 参数支持 XML、TSV、CSV。

## 速率限制
没有发布的限制。讲道理吧。
