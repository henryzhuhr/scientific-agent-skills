# LabArchives 身份验证指南

## 先决条件

### 1. 企业许可证

API 访问需要企业 LabArchives 许可证。请联系您的 LabArchives 管理员或 sales@labarchives.com：
- 验证您的机构是否具有企业访问权限
- 为您的帐户请求 API 访问启用
- 获取机构 API 凭证

### 2. API 凭证

您需要两套凭证：

#### 机构 API 凭证（来自LabArchives 管理员)
- **访问密钥 ID**：机构级标识符
- **访问密码**：机构级秘密

#### 用户身份验证凭据（自行配置）
- **电子邮件**：您的 LabArchives 帐户电子邮件（例如，researcher@university.edu）
- **外部应用程序密码**：在您的 LabArchives 帐户设置中设置 

## 设置外部应用程序密码

外部应用程序密码与您常规的 LabArchives 登录密码不同。它提供 API 访问，而无需暴露您的主要凭据。

* *创建外部应用程序密码的步骤：**

1. 通过 mynotebook.labarchives.com（或您的机构 URL）
2 登录您的 LabArchives 帐户。导航至 **帐户设置**（单击右上角您的姓名）
3. 选择**安全和隐私**选项卡
4. 查找 **外部应用** 部分 
5. 单击**生成新密码**或**重置密码**
6. 复制并安全地存储此密码（您将不会再看到它）
7. 使用此密码进行所有 API 身份验证

* *安全说明：** 将此密码视为 API 令牌。如果受到威胁，请立即从帐户设置重新生成它。

## 配置文件设置

创建一个`config.yaml`文件以安全地存储您的凭据：

```yaml
# Regional API endpoint
api_url: https://api.labarchives.com/api

# Institutional credentials (from administrator)
access_key_id: YOUR_ACCESS_KEY_ID_HERE
access_password: YOUR_ACCESS_PASSWORD_HERE

# User credentials (for user-specific operations)
user_email: researcher@university.edu
user_external_password: YOUR_EXTERNAL_APP_PASSWORD_HERE
```

* *替代：环境变量**

为了增强安全性，请使用环境变量而不是配置文件：

```bash
export LABARCHIVES_API_URL="https://api.labarchives.com/api"
export LABARCHIVES_ACCESS_KEY_ID="your_key_id"
export LABARCHIVES_ACCESS_PASSWORD="your_access_password"
export LABARCHIVES_USER_EMAIL="researcher@university.edu"
export LABARCHIVES_USER_PASSWORD="your_external_app_password"
```

## 区域端点

为您的机构选择正确的区域 API 端点：

|地区 |端点|如果您的 LabArchives URL 为 |
|--------|------------|--------------------------------|
|，请使用美国/国际 | `https://api.labarchives.com/api` | `mynotebook.labarchives.com` |
|澳大利亚 | `https://auapi.labarchives.com/api` | `aunotebook.labarchives.com` |
|英国 | `https://ukapi.labarchives.com/api` | `uknotebook.labarchives.com` |

 即使使用正确的凭据，使用错误的区域端点也会导致身份验证失败。

## 身份验证流程

### 选项 1：使用 labarchives-py Python 包装器

```python
from labarchivespy.client import Client
import yaml

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize client with institutional credentials
client = Client(
    config['api_url'],
    config['access_key_id'],
    config['access_password']
)

# Authenticate as specific user to get UID
login_params = {
    'login_or_email': config['user_email'],
    'password': config['user_external_password']
}
response = client.make_call('users', 'user_access_info', params=login_params)

# Parse response to extract UID
import xml.etree.ElementTree as ET
uid = ET.fromstring(response.content)[0].text
print(f"Authenticated as user ID: {uid}")
```

### 选项 2：使用 Python 直接 HTTP 请求requests

```python
import requests
import yaml

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Construct API call
url = f"{config['api_url']}/users/user_access_info"
params = {
    'access_key_id': config['access_key_id'],
    'access_password': config['access_password'],
    'login_or_email': config['user_email'],
    'password': config['user_external_password']
}

# Make authenticated request
response = requests.get(url, params=params)

if response.status_code == 200:
    print("Authentication successful!")
    print(response.content.decode('utf-8'))
else:
    print(f"Authentication failed: {response.status_code}")
    print(response.content.decode('utf-8'))
```

### 选项 3：使用 R

```r
library(httr)
library(xml2)

# Configuration
api_url <- "https://api.labarchives.com/api"
access_key_id <- "YOUR_ACCESS_KEY_ID"
access_password <- "YOUR_ACCESS_PASSWORD"
user_email <- "researcher@university.edu"
user_external_password <- "YOUR_EXTERNAL_APP_PASSWORD"

# Make authenticated request
response <- GET(
    paste0(api_url, "/users/user_access_info"),
    query = list(
        access_key_id = access_key_id,
        access_password = access_password,
        login_or_email = user_email,
        password = user_external_password
    )
)

# Parse response
if (status_code(response) == 200) {
    content <- content(response, as = "text", encoding = "UTF-8")
    xml_data <- read_xml(content)
    uid <- xml_text(xml_find_first(xml_data, "//uid"))
    print(paste("Authenticated as user ID:", uid))
} else {
    print(paste("Authentication failed:", status_code(response)))
}
```

## OAuth 身份验证（新集成）

LabArchives 现在使用 OAuth 2.0 进行新的第三方集成。旧版 API 密钥身份验证（如上所述）继续适用于直接 API 访问。

* *OAuth 流程（适用于应用程序开发人员）：**

1. 向 LabArchives
2 注册您的应用程序。获取客户端ID和客户端密钥
3. 实现OAuth 2.0授权代码流程
4. 交换访问令牌
5的授权码。使用 API 请求的访问令牌

联系 LabArchives 开发人员支持 OAuth 集成文档。

## 身份验证问题故障排除

### 401 未经授权错误

* *可能的原因和解决方案：**

1. **access_key_id 或 access_password 不正确**
  - 与 LabArchives 管理员验证凭据
  - 检查配置文件 

2 中是否存在拼写错误或额外空格。 **外部应用程序密码错误**
 - 确认您使用的是外部应用程序密码，而不是常规登录密码
  - 在帐户设置中重新生成外部应用程序密码

3. **API 访问未启用**
  - 联系您的 LabArchives 管理员为您的帐户启用 API 访问
  - 验证您的机构是否拥有企业许可证

4. **错误的区域端点**
  - 确认您的 api_url 与您机构的 LabArchives 实例匹配
  - 检查您是否使用 .com、.auapi 或 .ukapi 域

### 403 禁止错误

 * *可能的原因和解决方案：**

1. **权限不足**
  - 验证您的帐户角色是否具有必要的权限
  - 检查您是否有权访问特定笔记本（nbid）

2. **帐户已暂停或过期**
  - 请联系您的 LabArchives 管理员检查帐户状态

### 网络和连接问题

* *防火墙/代理配置：**

如果您的机构使用防火墙或代理：

```python
import requests

# Configure proxy
proxies = {
    'http': 'http://proxy.university.edu:8080',
    'https': 'http://proxy.university.edu:8080'
}

# Make request with proxy
response = requests.get(url, params=params, proxies=proxies)
```

* *SSL 证书验证：**

对于自签名证书（不建议用于生产）：

```python
# Disable SSL verification (use only for testing)
response = requests.get(url, params=params, verify=False)
```

## 安全最佳实践

1. **切勿将凭据提交给版本控制**
  - 将 `config.yaml` 添加到 `.gitignore`
  - 使用环境变量或秘密管理系统

2. **定期轮换凭证**
  - 每 90 天更改一次外部应用程序密码
  - 每年重新生成 API 密钥

3. **使用最小权限原则**
  - 仅请求必要的API权限
  - 为不同的应用程序创建单独的API凭证

4. **监控 API 使用情况**
  - 定期查看 API 访问日志
  - 设置异常活动警报

5. **安全存储**
  - 静态加密配置文件
  - 使用系统钥匙串或秘密管理工具（例如，AWS Secrets Manager、Azure Key Vault）

## 测试身份验证

使用此脚本验证您的身份验证设置：

```python
#!/usr/bin/env python3
"""Test LabArchives API authentication"""

from labarchivespy.client import Client
import yaml
import sys

def test_authentication():
    try:
        # Load config
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)

        print("Configuration loaded successfully")
        print(f"API URL: {config['api_url']}")

        # Initialize client
        client = Client(
            config['api_url'],
            config['access_key_id'],
            config['access_password']
        )
        print("Client initialized")

        # Test authentication
        login_params = {
            'login_or_email': config['user_email'],
            'password': config['user_external_password']
        }
        response = client.make_call('users', 'user_access_info', params=login_params)

        if response.status_code == 200:
            print("✅ Authentication successful!")

            # Extract UID
            import xml.etree.ElementTree as ET
            uid = ET.fromstring(response.content)[0].text
            print(f"User ID: {uid}")

            # Get user info
            user_response = client.make_call('users', 'user_info_via_id', params={'uid': uid})
            print("✅ User information retrieved successfully")

            return True
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(response.content.decode('utf-8'))
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_authentication()
    sys.exit(0 if success else 1)
```

运行此脚本以确认所有配置均正确：

```bash
python3 test_auth.py
```

## 获取帮助

如果排除故障后身份验证仍然失败：

1. 请联系您所在机构的实验室档案管理员
2. 向 LabArchives 支持发送电子邮件：support@labarchives.com
3. 包括：
  - 您的机构名称
  - 您的 LabArchives 帐户电子邮件
  - 错误消息和响应代码
  - 您使用的区域端点
  - 编程语言和库版本
