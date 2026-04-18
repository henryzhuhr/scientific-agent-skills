# Protocols.io Authentication

## 概述

protocols.io API 支持两种类型的访问令牌进行身份验证，从而可以访问公共内容和私有内容。

## 访问令牌类型

### 1. CLIENT_ACCESS_TOKEN

- **用途**：允许访问客户端的公共内容和私有内容user
- **用例**：访问您自己的协议和公共协议时
- **范围**：仅限于令牌所有者的私有内容以及所有公共内容

### 2. OAUTH_ACCESS_TOKEN

- **目的**：授予对特定用户的私有内容以及所有公共内容的访问权限
- **用例**：构建以下应用程序时需要在其许可的情况下访问其他用户的内容
- **范围**：对授权用户的私有内容以及所有公共内容的完全访问权限

## 身份验证标头

所有API请求都必须包含授权标头：

```
Authorization: Bearer [ACCESS_TOKEN]
```

## OAuth Flow

### 步骤1：生成授权链接

将用户引导至授权URL以授予访问权限：

```
GET https://protocols.io/api/v3/oauth/authorize
```

* *参数：**
- `client_id`（必需）：您的应用程序的客户端ID
- `redirect_uri`（必需）：之后重定向用户的URL授权
- `response_type`（必需）：设置为“code”
- `state`（可选但推荐）：防止CSRF攻击的随机字符串

* *示例：**
```
https://protocols.io/api/v3/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code&state=RANDOM_STRING
```

### 步骤2：交换授权代码Token

用户授权后，protocols.io 会使用授权码重定向到您的 `redirect_uri`。将此代码交换为访问令牌：

```
POST https://protocols.io/api/v3/oauth/token
```

* *参数：**
- `grant_type`：设置为“authorization_code”
- `code`：收到的授权代码
- `client_id`：您的应用程序的客户端ID
- `client_secret`：您的应用程序的客户端密钥
- `redirect_uri`：必须与步骤 1 中使用的redirect_uri 匹配

* *响应包括：**
- `access_token`：用于 API 请求的 OAuth 访问令牌
- `token_type`：“承载”
- `expires_in`：令牌生命周期（以秒为单位）（通常为 1 年） 
- `refresh_token`：用于刷新访问令牌

### 步骤3：刷新访问令牌

在访问令牌过期前（通常为1年），使用刷新令牌获取新的访问令牌：

```
POST https://protocols.io/api/v3/oauth/token
```

* *参数：**
- `grant_type`：设置为"refresh_token"
- `refresh_token`：在步骤 2 中收到的刷新令牌
- `client_id`：您的应用程序的客户端 ID
- `client_secret`：您的应用程序的客户端密钥

## 速率限制

进行速率限制时请注意API 请求：

- **标准端点**：每个用户每分钟 100 个请求
- **PDF 端点** (`/view/[protocol-uri].pdf`)：
  - 登录用户：每分钟 5 个请求
  - 未签名用户：每分钟 3 个请求

## 最佳做法

1. **安全地存储令牌**：切勿在客户端代码或版本控制
2中公开访问令牌。 **处理令牌过期**：在过期前实现令牌自动刷新
3. **遵守速率限制**：针对速率限制错误 
4 实施指数退避。 **使用状态参数**：为了安全起见，始终在 OAuth 流程中包含状态参数
5. **验证redirect_uri**：确保授权和令牌请求之间的重定向URI完全匹配
