# 人类细胞图谱 (HCA)

## 基本 URL
```
https://service.azul.data.humancellatlas.org/
```

## 身份验证
无需身份验证。

## 关键端点

|端点|描述 |
|----------|-------------|
| `/index/projects?size={n}&catalog=dcp2` |列出/搜索项目|
| `/index/samples?size={n}&catalog=dcp2` |列出/搜索样本|
| `/index/files?size={n}&catalog=dcp2` |列出/搜索文件|
| `/index/summary?catalog=dcp2` |汇总统计 |

## 调用示例
```
# List projects
https://service.azul.data.humancellatlas.org/index/projects?size=5&catalog=dcp2

# Summary stats
https://service.azul.data.humancellatlas.org/index/summary?catalog=dcp2
```

 支持器官、物种、文库构建等 JSON 过滤参数。

## 响应格式
JSON。 `hits` 数组，包含项目/样本/文件元数据 + 分页。

## 速率限制
没有发布的限制。讲道理吧。
