# 连接和会话管理

此参考内容涵盖使用 BlitzGateway 建立和管理与 OMERO 服务器的连接。

## 基本连接

### 标准连接模式

```python
from omero.gateway import BlitzGateway

# Create connection
conn = BlitzGateway(username, password, host=host, port=4064)

# Connect to server
if conn.connect():
    print("Connected successfully")
    # Perform operations
    conn.close()
else:
    print("Failed to connect")
```

### 连接参数

- **用户名** (str): OMERO 用户帐户name
- **password** (str)：用户密码
- **host** (str)：OMERO 服务器主机名或 IP 地址
- **port** (int)：服务器端口（默认：4064）
- **secure** (bool)：强制加密连接（默认：False）

### 安全连接

确保所有数据传输都加密：

```python
conn = BlitzGateway(username, password, host=host, port=4064, secure=True)
conn.connect()
```

## 上下文管理器模式（推荐）

使用上下文管理器进行自动连接管理和清理：

```python
from omero.gateway import BlitzGateway

with BlitzGateway(username, password, host=host, port=4064) as conn:
    # Connection automatically established
    for project in conn.getObjects('Project'):
        print(project.getName())
    # Connection automatically closed on exit
```

* *优点：**
- 自动 `connect()` 调用 
- 退出时自动调用 `close()`
- 异常安全的资源清理
- 清理器code

## 会话管理

### 来自现有客户端的连接

从现有`omero.client`会话创建BlitzGateway：

```python
import omero.clients
from omero.gateway import BlitzGateway

# Create client and session
client = omero.client(host, port)
session = client.createSession(username, password)

# Create BlitzGateway from existing client
conn = BlitzGateway(client_obj=client)

# Use connection
# ...

# Close when done
conn.close()
```

### 检索会话信息

```python
# Get current user information
user = conn.getUser()
print(f"User ID: {user.getId()}")
print(f"Username: {user.getName()}")
print(f"Full Name: {user.getFullName()}")
print(f"Is Admin: {conn.isAdmin()}")

# Get current group
group = conn.getGroupFromContext()
print(f"Current Group: {group.getName()}")
print(f"Group ID: {group.getId()}")
```

### 检查管理员权限

```python
if conn.isAdmin():
    print("User has admin privileges")

if conn.isFullAdmin():
    print("User is full administrator")
else:
    # Check specific admin privileges
    privileges = conn.getCurrentAdminPrivileges()
    print(f"Admin privileges: {privileges}")
```

## 组上下文管理

OMERO使用组来管理数据访问权限。用户可以属于多个组。

### 获取当前组上下文

```python
# Get the current group context
group = conn.getGroupFromContext()
print(f"Current group: {group.getName()}")
print(f"Group ID: {group.getId()}")
```

### 跨所有组查询

使用组ID `-1`跨所有可访问的组查询：

```python
# Set context to query all groups
conn.SERVICE_OPTS.setOmeroGroup('-1')

# Now queries span all accessible groups
image = conn.getObject("Image", image_id)
projects = conn.listProjects()
```

### 切换到特定组

切换上下文以在特定组中工作：

```python
# Get group ID from an object
image = conn.getObject("Image", image_id)
group_id = image.getDetails().getGroup().getId()

# Switch to that group's context
conn.SERVICE_OPTS.setOmeroGroup(group_id)

# Subsequent operations use this group context
projects = conn.listProjects()
```

### 列出可用组

```python
# Get all groups for current user
for group in conn.getGroupsMemberOf():
    print(f"Group: {group.getName()} (ID: {group.getId()})")
```

## 高级连接功能

### 替代用户连接（仅限管理员）

管理员可以创建充当其他用户的连接：

```python
# Connect as admin
admin_conn = BlitzGateway(admin_user, admin_pass, host=host, port=4064)
admin_conn.connect()

# Get target user
target_user = admin_conn.getObject("Experimenter", user_id).getName()

# Create connection as that user
user_conn = admin_conn.suConn(target_user)

# Operations performed as target user
for project in user_conn.listProjects():
    print(project.getName())

# Close substitute connection
user_conn.close()
admin_conn.close()
```

### 列出管理员

```python
# Get all administrators
for admin in conn.getAdministrators():
    print(f"ID: {admin.getId()}, Name: {admin.getFullName()}, "
          f"Username: {admin.getOmeName()}")
```

## 连接生命周期

### 关闭连接

始终关闭与空闲服务器的连接资源：

```python
try:
    conn = BlitzGateway(username, password, host=host, port=4064)
    conn.connect()

    # Perform operations

except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()
```

### 检查连接状态

```python
if conn.isConnected():
    print("Connection is active")
else:
    print("Connection is closed")
```

## 错误处理

### 稳健连接模式

```python
from omero.gateway import BlitzGateway
import traceback

def connect_to_omero(username, password, host, port=4064):
    """
    Establish connection to OMERO server with error handling.

    Returns:
        BlitzGateway connection object or None if failed
    """
    try:
        conn = BlitzGateway(username, password, host=host, port=port, secure=True)
        if conn.connect():
            print(f"Connected to {host}:{port} as {username}")
            return conn
        else:
            print("Failed to establish connection")
            return None
    except Exception as e:
        print(f"Connection error: {e}")
        traceback.print_exc()
        return None

# Usage
conn = connect_to_omero(username, password, host)
if conn:
    try:
        # Perform operations
        pass
    finally:
        conn.close()
```

## 常见连接模式

### 模式1：简单脚本

```python
from omero.gateway import BlitzGateway

# Connection parameters
HOST = 'omero.example.com'
PORT = 4064
USERNAME = 'user'
PASSWORD = 'pass'

# Connect
with BlitzGateway(USERNAME, PASSWORD, host=HOST, port=PORT) as conn:
    print(f"Connected as {conn.getUser().getName()}")
    # Perform operations
```

### 模式2：基于配置的连接

```python
import yaml
from omero.gateway import BlitzGateway

# Load configuration
with open('omero_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Connect using config
with BlitzGateway(
    config['username'],
    config['password'],
    host=config['host'],
    port=config.get('port', 4064),
    secure=config.get('secure', True)
) as conn:
    # Perform operations
    pass
```

### 模式3：环境变量

```python
import os
from omero.gateway import BlitzGateway

# Get credentials from environment
USERNAME = os.environ.get('OMERO_USER')
PASSWORD = os.environ.get('OMERO_PASSWORD')
HOST = os.environ.get('OMERO_HOST', 'localhost')
PORT = int(os.environ.get('OMERO_PORT', 4064))

# Connect
with BlitzGateway(USERNAME, PASSWORD, host=HOST, port=PORT) as conn:
    # Perform operations
    pass
```

## 最佳实践

1. **使用上下文管理器**：始终首选上下文管理器进行自动清理
2. **安全连接**：生产环境使用 `secure=True`
3. **错误处理**：将连接代码包装在 try- except 块
4 中。 **关闭连接**：完成后始终关闭连接
5. **组上下文**：在查询之前设置适当的组上下文
6. **凭证安全**：切勿对凭证进行硬编码；使用环境变量或配置文件
7. **连接池**：对于 Web 应用程序，实现连接池
8. **超时**：考虑为长时间运行的操作实施连接超时

## 故障排除

### 连接被拒绝

```
Unable to contact ORB
```

* *解决方案：**
- 验证主机和端口是否正确
- 检查防火墙设置
- 确保OMERO 服务器正在运行
- 验证网络连接

### 身份验证失败

```
Cannot connect to server
```

* *解决方案：**
- 验证用户名和密码
- 检查用户帐户是否处于活动状态
- 验证组成员身份
- 检查服务器日志以获取详细信息

### 会话超时

* *解决方案：**
- 增加服务器上的会话超时
- 实现会话保持活动
- 超时重新连接
- 使用连接池进行长时间运行应用领域
