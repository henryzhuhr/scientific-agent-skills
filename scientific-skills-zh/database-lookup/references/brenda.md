# BRENDA 酶数据库 (SOAP API)

## 重要提示：BRENDA 使用 SOAP，而不是 REST。需要带有 `zeep` 库的 Python。

## SOAP 端点
```
https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl
```

## Auth
需要在 https://www.brenda-enzymes.org/register.php
 进行免费注册每个凭证（电子邮件 + SHA-256 哈希密码） call.

## 关键 SOAP 方法

所有方法都以 `email`、`password` (SHA-256)和 `ecNumber` 作为基本参数。方法|描述|
|--------|-------------|
| `getKmValue` |米氏常数(Km)|
| `getTurnoverNumber` |成交量（千猫）|
| `getKcatKmValue` |催化效率（kcat/Km）|
| `getKiValue` |抑制常数(Ki)|
| `getIc50Value` | IC50值|
| `getSpecificActivity` |比活度|
| `getPhOptimum` |最适pH |
| `getTemperatureOptimum` |最适温度|
| `getSubstrate` |基材|
| `getProduct` |产品|
| `getInhibitors` |抑制剂|
| `getCofactor` |辅因子|
| `getOrganism` |来源生物|
| `getReaction` |反应方程式|
| `getSequence` |蛋白质序列|
| `getDisease` |相关疾病 |

## 参数语法
`fieldName*value` 格式。空值=返回全部。

```
ecNumber*1.1.1.1           # Required: EC number
organism*Homo sapiens      # Optional: filter by organism
substrate*ethanol          # Optional: filter by substrate
kmValue*                   # Return field (empty = all)
```

## Python示例
```python
import hashlib
from zeep import Client

client = Client("https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl")
email = "your@email.com"
password = hashlib.sha256("your_password".encode()).hexdigest()

# Get Km values for alcohol dehydrogenase
result = client.service.getKmValue(
    email, password,
    "ecNumber*1.1.1.1", "organism*Homo sapiens",
    "kmValue*", "substrate*", "literature*"
)
```

## 响应格式
返回用`!`（记录分隔符）解析的字符串和`#`/`*`（字段分隔符）。必须手动解析。

## 速率限制
没有发布的限制。 SOAP 响应可能需要 1-5 秒。尊重——免费的学术服务。

## 此技能的注意事项
由于 BRENDA 使用 SOAP（而不是 REST），因此进行调用需要使用 `zeep` 编写和执行 Python 脚本。使用 Bash 运行脚本而不是 WebFetch.
