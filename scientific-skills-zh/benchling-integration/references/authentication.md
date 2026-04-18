# Benchling 身份验证参考

## 身份验证方法

Benchling 支持三种身份验证方法，每种方法适合不同的用例。

### 1. API 密钥身份验证（基本身份验证）

* *最适合：** 个人脚本、原型设计、单用户集成

* *工作原理：**
- 使用您的 API 密钥作为 HTTP 基本身份验证中的用户名
- 将密码字段留空
- 所有请求必须使用 HTTPS

* *获取 API 密钥：**
1. 登录您的 Benchling 帐户
2. 导航至配置文件设置
3. 找到 API 密钥部分
4. 生成新的 API 密钥
5. 安全存储（只会显示一次）

* *Python SDK 用法：**
```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key_here")
)
```

* *直接 HTTP 用法：**
```bash
curl -X GET \
  https://your-tenant.benchling.com/api/v2/dna-sequences \
  -u "your_api_key_here:"
```

 请注意没有密码的 API 密钥后面的冒号。

* *环境变量模式：**
```python
import os
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

api_key = os.environ.get("BENCHLING_API_KEY")
tenant_url = os.environ.get("BENCHLING_TENANT_URL")

benchling = Benchling(
    url=tenant_url,
    auth_method=ApiKeyAuth(api_key)
)
```

### 2. OAuth 2.0 客户端凭据

* *最适合：** 多用户应用程序、服务帐户、生产集成

* *工作原理：**
1. 在 Benchling 的开发者控制台 
2 中注册应用程序。获取客户端ID和客户端秘密
3. 交换访问令牌 
4 的凭据。使用 API 请求的访问令牌
5. 过期刷新令牌

* *注册应用程序：**
1. 以管理员 
2 身份登录 Benchling。导航到开发者控制台
3. 创建一个新的App
4. 记录客户端 ID 和客户端密钥
5. 配置 OAuth 重定向 URI 和权限

* *Python SDK 用法：**
```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.client_credentials_oauth2 import ClientCredentialsOAuth2

auth_method = ClientCredentialsOAuth2(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=auth_method
)
```

SDK 自动处理令牌刷新。

* *直接 HTTP 令牌流：**
```bash
# Get access token
curl -X POST \
  https://your-tenant.benchling.com/api/v2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=your_client_id" \
  -d "client_secret=your_client_secret"

# Response:
# {
#   "access_token": "token_here",
#   "token_type": "Bearer",
#   "expires_in": 3600
# }

# Use access token
curl -X GET \
  https://your-tenant.benchling.com/api/v2/dna-sequences \
  -H "Authorization: Bearer access_token_here"
```

### 3. OpenID Connect (OIDC)

* *最适合：** 与现有身份提供商、SSO 场景的企业集成

* *工作原理：**
- 通过身份提供商（Okta、Azure AD 等）对用户进行身份验证 
- 身份提供商通过电子邮件声明发出 ID 令牌
- 基准测试根据 OpenID 配置端点验证令牌
- 通过电子邮件匹配经过身份验证的用户

* *要求：**
- 企业基准测试帐户
- 配置的身份提供商（IdP）
- IdP 必须颁发带有电子邮件声明的令牌
- 令牌中的电子邮件必须与基准用户电子邮件匹配

* *身份提供商配置：**
1. 配置您的 IdP 以颁发 OpenID Connect 令牌
2. 确保令牌包含 `email` 声明 
3. 向基准测试提供您的 IdP 的 OpenID 配置 URL
4. 基准测试将根据此配置验证令牌

* *Python 用法：**
```python
# Assuming you have an ID token from your IdP
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.oidc_auth import OidcAuth

auth_method = OidcAuth(id_token="id_token_from_idp")

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=auth_method
)
```

* *直接 HTTP 用法：**
```bash
curl -X GET \
  https://your-tenant.benchling.com/api/v2/dna-sequences \
  -H "Authorization: Bearer id_token_here"
```

## 安全最佳实践

### 凭证存储

* *DO:**
- 将凭证存储在环境变量中
- 使用密码管理器或秘密管理服务（AWS Secrets Manager、HashiCorp Vault）
- 静态加密凭证
- 对开发/登台/生产使用不同的凭证

* *不要:**
- 将凭证提交到版本control
- 在源文件中硬编码凭证
- 通过电子邮件或聊天共享凭证
- 在纯文本文件中存储凭证

* *环境变量示例：**
```python
import os
from dotenv import load_dotenv  # python-dotenv package

# Load from .env file (add .env to .gitignore!)
load_dotenv()

api_key = os.environ["BENCHLING_API_KEY"]
tenant = os.environ["BENCHLING_TENANT_URL"]
```

### 凭证轮换

* *API 密钥旋转：**
1. 在配置文件设置中生成新的 API 密钥
2. 更新您的应用程序以使用新密钥
3. 验证新密钥是否有效 
4. 删除旧的API密钥

* *应用程序秘密轮换：**
1. 导航到开发者控制台
2. 选择您的应用程序
3. 生成新的客户端密钥
4. 更新您的应用程序配置
5. 验证后删除旧密文

* *最佳实践：** 定期（例如每 90 天）轮换凭据，如果受到威胁，请立即轮换。

### 访问控制

* *最小权限原则：**
- 仅授予最低必要权限
- 使用服务帐户（应用程序）而不是个人帐户进行自动化
- 查看和审核权限定期

* *应用程序权限：**
应用程序需要明确的访问权限授予：
- 组织
- 团队
- 项目
- 文件夹

设置应用程序时在开发者控制台中配置这些。

* *用户权限：**
API 访问镜像 UI 权限：
- 用户只能访问他们有权在 UI 中查看/编辑的数据
- 暂停的用户失去 API 访问权限
- 存档的应用程序在取消存档之前失去 API 访问权限

### 网络安全

* *HTTPS仅：**
所有 Benchling API 请求都必须使用 HTTPS。 HTTP请求将被拒绝。

* *IP 白名单（企业）：**
 某些企业帐户可以将 API 访问限制为特定 IP 范围。联系 Benchling 支持进行配置。

* *速率限制：**
Benchling 实现速率限制以防止滥用：
- 默认：每个用户/应用每 10 秒 100 个请求
- 超出速率限制时返回 429 状态代码
- SDK 使用指数退避自动重试

### 审核日志记录

* *跟踪 API 使用情况：**
- 所有 API 调用均使用用户/应用程序身份进行记录
- OAuth 应用程序显示带有用户属性的正确审核跟踪
- API 密钥调用归因于密钥所有者
- 在 Benchling 的管理控制台中查看审核日志

* *最佳实践应用程序：**
 当多个用户通过您的应用程序进行交互时，使用 OAuth 而不是 API 密钥。这可确保正确审核归因于实际用户，而不仅仅是应用程序。

## 故障排除

### 常见身份验证错误

* *401 未经授权：**
- 凭据无效或过期
- API 密钥格式不正确
- 缺少“授权”标头

* *解决方案：**
- 验证凭据是否正确
- 检查 API 密钥未过期或删除
- 确保标头格式正确： `Authorization: Bearer <token>`

* *403 禁止：**
- 有效凭据但权限不足
- 用户无权访问所请求的资源
- 应用程序未获得组织/项目的访问权限

* *解决方案：**
- 检查用户/应用程序权限Benchling
- 在开发者控制台中授予必要的访问权限（对于应用程序）
- 验证资源是否存在且用户有权访问

* *429 请求过多：**
- 超出速率限制
- 短时间内请求过多

* *解决方案：**
- 实施指数backoff
- SDK 自动处理此问题
- 考虑缓存结果
- 随着时间的推移传播请求

### 测试身份验证

* *使用curl快速测试：**
```bash
# Test API key
curl -X GET \
  https://your-tenant.benchling.com/api/v2/users/me \
  -u "your_api_key:" \
  -v

# Test OAuth token
curl -X GET \
  https://your-tenant.benchling.com/api/v2/users/me \
  -H "Authorization: Bearer your_token" \
  -v
```

`/users/me`端点返回经过身份验证的用户信息，对于验证凭据很有用。

* *Python SDK测试：**
```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

try:
    benchling = Benchling(
        url="https://your-tenant.benchling.com",
        auth_method=ApiKeyAuth("your_api_key")
    )

    # Test authentication
    user = benchling.users.get_me()
    print(f"Authenticated as: {user.name} ({user.email})")

except Exception as e:
    print(f"Authentication failed: {e}")
```

## 多租户注意事项

如果使用多个基准租户：

```python
# Configuration for multiple tenants
tenants = {
    "production": {
        "url": "https://prod.benchling.com",
        "api_key": os.environ["PROD_API_KEY"]
    },
    "staging": {
        "url": "https://staging.benchling.com",
        "api_key": os.environ["STAGING_API_KEY"]
    }
}

# Initialize clients
clients = {}
for name, config in tenants.items():
    clients[name] = Benchling(
        url=config["url"],
        auth_method=ApiKeyAuth(config["api_key"])
    )

# Use specific client
prod_sequences = clients["production"].dna_sequences.list()
```

## 高级：自定义 HTTPS 客户端

对于具有自签名证书或公司代理的环境：

```python
import httpx
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

# Custom httpx client with certificate verification
custom_client = httpx.Client(
    verify="/path/to/custom/ca-bundle.crt",
    timeout=30.0
)

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key"),
    http_client=custom_client
)
```

## 参考资料

- **官方身份验证文档：** https://docs.benchling.com/docs/authentication
- **开发者控制台：** https://your-tenant.benchling.com/developer
- **SDK 文档：** https://benchling.com/sdk-docs/
