# LaminDB 设置和部署

本文档涵盖 LaminDB 的安装、配置、实例管理、存储选项和部署策略。

## 安装

### 基本安装

```bash
# Install LaminDB
pip install lamindb

# Or with pip3
pip3 install lamindb
```

### 使用 Extras 安装

为特定安装可选依赖项功能：

```bash
# Google Cloud Platform support
pip install 'lamindb[gcp]'

# Flow cytometry formats
pip install 'lamindb[fcs]'

# Array storage and streaming (Zarr support)
pip install 'lamindb[zarr]'

# AWS S3 support (usually included by default)
pip install 'lamindb[aws]'

# Multiple extras
pip install 'lamindb[gcp,zarr,fcs]'
```

### 模块插件

```bash
# Biological ontologies (Bionty)
pip install bionty

# Wet lab functionality
pip install lamindb-wetlab

# Clinical data (OMOP CDM)
pip install lamindb-clinical
```

### 验证安装

```python
import lamindb as ln
print(ln.__version__)

# Check available modules
import bionty as bt
print(bt.__version__)
```

## 身份验证

### 创建帐户

1. 访问 https://lamin.ai
2. 注册一个免费帐户
3. 导航到帐户设置以生成 API 密钥

### 登录

```bash
# Login with API key
lamin login

# You'll be prompted to enter your API key
# API key is stored locally at ~/.lamin/
```

### 身份验证详细信息

* *数据隐私：** LaminDB 身份验证仅收集基本元数据（电子邮件、用户信息）。您的实际数据保持私密，不会发送到 LaminDB 服务器。

* *本地与云：** 即使仅本地使用也需要身份验证才能启用协作功能和实例管理。

## 实例初始化

### 本地 SQLite 实例

用于本地开发和小型数据集：

```bash
# Initialize in current directory
lamin init --storage ./mydata

# Initialize in specific directory
lamin init --storage /path/to/data

# Initialize with specific modules
lamin init --storage ./mydata --modules bionty

# Initialize with multiple modules
lamin init --storage ./mydata --modules bionty,wetlab
```

### Cloud Storage with SQLite

使用云存储但使用本地 SQLite 数据库：

```bash
# AWS S3
lamin init --storage s3://my-bucket/path

# Google Cloud Storage
lamin init --storage gs://my-bucket/path

# S3-compatible (MinIO, Cloudflare R2)
lamin init --storage 's3://bucket?endpoint_url=http://endpoint:9000'
```

### Cloud Storage with PostgreSQL

用于生产部署：

```bash
# S3 + PostgreSQL
lamin init --storage s3://my-bucket/path \
  --db postgresql://user:password@hostname:5432/dbname \
  --modules bionty

# GCS + PostgreSQL
lamin init --storage gs://my-bucket/path \
  --db postgresql://user:password@hostname:5432/dbname \
  --modules bionty
```

### 实例命名

```bash
# Specify instance name
lamin init --storage ./mydata --name my-project

# Default name uses directory name
lamin init --storage ./mydata  # Instance name: "mydata"
```

## 连接到实例

### 连接到您自己的实例

```bash
# By name
lamin connect my-project

# By full path
lamin connect account_handle/my-project
```

### 连接共享实例

```bash
# Connect to someone else's instance
lamin connect other-user/their-project

# Requires appropriate permissions
```

### 实例切换

```bash
# List available instances
lamin info

# Switch instance
lamin connect another-instance

# Close current instance
lamin close
```

## 存储配置

### 本地存储

* *优点：**
- 速度快访问
- 无需互联网
- 简单设置

* *设置：**
```bash
lamin init --storage ./data
```

### AWS S3 存储

* * 优点：**
- 可扩展
- 协作
- Durable

* *设置：**
```bash
# Set credentials
export AWS_ACCESS_KEY_ID=your_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1

# Initialize
lamin init --storage s3://my-bucket/project-data \
  --db postgresql://user:pwd@host:5432/db
```

* *所需的S3权限：**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket/*",
        "arn:aws:s3:::my-bucket"
      ]
    }
  ]
}
```

### Google Cloud存储

* *设置：**
```bash
# Authenticate
gcloud auth application-default login

# Or use service account
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# Initialize
lamin init --storage gs://my-bucket/project-data \
  --db postgresql://user:pwd@host:5432/db
```

### S3 兼容存储

对于 MinIO、Cloudflare R2 或其他 S3 兼容服务：

```bash
# MinIO example
export AWS_ACCESS_KEY_ID=minioadmin
export AWS_SECRET_ACCESS_KEY=minioadmin

lamin init --storage 's3://my-bucket?endpoint_url=http://minio.example.com:9000'

# Cloudflare R2 example
export AWS_ACCESS_KEY_ID=your_r2_access_key
export AWS_SECRET_ACCESS_KEY=your_r2_secret_key

lamin init --storage 's3://bucket?endpoint_url=https://account-id.r2.cloudflarestorage.com'
```

## 数据库配置

### SQLite（默认）

* *优点：**
- 没有单独的数据库服务器
- 设置简单
- 适合开发

* *限制：**
- 不适合并发写入
- 有限的可扩展性

* *设置：**
```bash
# SQLite is default
lamin init --storage ./data
# Database stored at ./data/.lamindb/
```

### PostgreSQL

* *优点：**
- 生产就绪
- 并发访问
- 更好的性能scale

* *设置：**
```bash
# Full connection string
lamin init --storage s3://bucket/path \
  --db postgresql://username:password@hostname:5432/database

# With SSL
lamin init --storage s3://bucket/path \
  --db "postgresql://user:pwd@host:5432/db?sslmode=require"
```

* *PostgreSQL 版本：** 兼容 PostgreSQL 12+

### 数据库架构管理

```bash
# Check current schema version
lamin migrate check

# Upgrade schema
lamin migrate deploy

# View migration history
lamin migrate history
```

## 缓存配置

### 缓存目录

LaminDB维护云文件的本地缓存：

```python
import lamindb as ln

# View cache location
print(ln.settings.cache_dir)
```

### 配置缓存位置

```bash
# Set cache directory
lamin cache set /path/to/cache

# View current cache settings
lamin cache get
```

### 系统范围缓存（多用户）

适用于多个共享系统用户：

```bash
# Create system settings file
sudo mkdir -p /system/settings
sudo nano /system/settings/system.env
```

添加到`system.env`：
```bash
lamindb_cache_path=/shared/cache/lamindb
```

确保权限：
```bash
sudo chmod 755 /shared/cache/lamindb
sudo chown -R shared-user:shared-group /shared/cache/lamindb
```

### 缓存管理

```python
import lamindb as ln

# Clear cache for specific artifact
artifact = ln.Artifact.get(key="data.h5ad")
artifact.delete_cache()

# Check if artifact is cached
if artifact.is_cached():
    print("Already cached")

# Manually clear entire cache
import shutil
shutil.rmtree(ln.settings.cache_dir)
```

## 设置管理

### 查看当前设置

```python
import lamindb as ln

# User settings
print(ln.setup.settings.user)
# User(handle='username', email='user@email.com', name='Full Name')

# Instance settings
print(ln.setup.settings.instance)
# Instance(name='my-project', storage='s3://bucket/path')
```

### 配置设置

```bash
# Set development directory for relative keys
lamin settings set dev-dir /path/to/project

# Configure git sync
lamin settings set sync-git-repo https://github.com/user/repo.git

# View all settings
lamin settings
```

### 环境变量

```bash
# Cache directory
export LAMIN_CACHE_DIR=/path/to/cache

# Settings directory
export LAMIN_SETTINGS_DIR=/path/to/settings

# Git sync
export LAMINDB_SYNC_GIT_REPO=https://github.com/user/repo.git
```

## 实例管理

### 查看实例信息

```bash
# Current instance info
lamin info

# List all instances
lamin ls

# View instance details
lamin instance details
```

### 实例协作

```bash
# Set instance visibility (requires LaminHub)
lamin instance set-visibility public
lamin instance set-visibility private

# Invite collaborators (requires LaminHub)
lamin instance invite user@email.com
```

### 实例迁移

```bash
# Backup instance
lamin backup create

# Restore from backup
lamin backup restore backup_id

# Export instance metadata
lamin export instance-metadata.json
```

### 删除实例

```bash
# Delete instance (preserves data, removes metadata)
lamin delete --force instance-name

# This only removes the LaminDB metadata
# Actual data in storage location remains
```

## 生产部署模式

### 模式1：本地开发→云端生产

* *开发：**
```bash
# Local development
lamin init --storage ./dev-data --modules bionty
```

* *生产：**
```bash
# Cloud production
lamin init --storage s3://prod-bucket/data \
  --db postgresql://user:pwd@db-host:5432/prod-db \
  --modules bionty \
  --name production
```

* *迁移：**从开发导出工件，导入到prod
```python
# Export from dev
artifacts = ln.Artifact.filter().all()
for artifact in artifacts:
    artifact.export("/tmp/export/")

# Switch to prod
lamin connect production

# Import to prod
for file in Path("/tmp/export/").glob("*"):
    ln.Artifact(str(file), key=file.name).save()
```

### 模式2：多区域部署

在多个区域部署实例以实现数据主权：

```bash
# US instance
lamin init --storage s3://us-bucket/data \
  --db postgresql://user:pwd@us-db:5432/db \
  --name us-production

# EU instance
lamin init --storage s3://eu-bucket/data \
  --db postgresql://user:pwd@eu-db:5432/db \
  --name eu-production
```

### 模式3：共享存储、个人实例

多用户、共享data:

```bash
# Shared storage with user-specific DB
lamin init --storage s3://shared-bucket/data \
  --db postgresql://user1:pwd@host:5432/user1_db \
  --name user1-workspace

lamin init --storage s3://shared-bucket/data \
  --db postgresql://user2:pwd@host:5432/user2_db \
  --name user2-workspace
```

## 性能优化

### 数据库性能

```python
# Use connection pooling for PostgreSQL
# Configure in database server settings

# Optimize queries with indexes
# LaminDB creates indexes automatically for common queries
```

### 存储性能

```bash
# Use appropriate storage classes
# S3: STANDARD for frequent access, INTELLIGENT_TIERING for mixed access

# Configure multipart upload thresholds
export AWS_CLI_FILE_IO_BANDWIDTH=100MB
```

### 缓存优化

```python
# Pre-cache frequently used artifacts
artifacts = ln.Artifact.filter(key__startswith="reference/")
for artifact in artifacts:
    artifact.cache()  # Download to cache

# Use backed mode for large arrays
adata = artifact.backed()  # Don't load into memory
```

## 安全最佳实践

1. **凭证管理：**
  - 使用环境变量，而不是硬编码凭证
  - 使用 AWS/GCP 上的 IAM 角色而不是访问密钥
  - 定期轮换凭证

2. **访问控制：**
  - 使用 PostgreSQL 进行多用户访问控制
  - 配置存储桶策略
  - 启用审核日志记录

3. **网络安全：**
  - 使用 SSL/TLS 进行数据库连接
  - 使用 VPC 进行云部署
  - 尽可能限制 IP 地址

4. **数据保护：**
  - 启用静态加密（S3、GCS）
  - 使用传输中加密（HTTPS、SSL）
  - 实施备份策略

## 监控和维护

### 运行状况检查

```python
import lamindb as ln

# Check database connection
try:
    ln.Artifact.filter().count()
    print("✓ Database connected")
except Exception as e:
    print(f"✗ Database error: {e}")

# Check storage access
try:
    test_artifact = ln.Artifact("test.txt", key="healthcheck.txt").save()
    test_artifact.delete(permanent=True)
    print("✓ Storage accessible")
except Exception as e:
    print(f"✗ Storage error: {e}")
```

### 日志记录

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# LaminDB operations will produce detailed logs
```

### 备份策略

```bash
# Regular database backups (PostgreSQL)
pg_dump -h hostname -U username -d database > backup_$(date +%Y%m%d).sql

# Storage backups (S3 versioning)
aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled

# Metadata export
lamin export metadata_backup.json
```

## 故障排除

### 常见问题

* *问题：无法连接到实例**
```bash
# Check instance exists
lamin ls

# Verify authentication
lamin login

# Re-connect
lamin connect instance-name
```

* *问题：存储权限被拒绝**
```bash
# Check AWS credentials
aws s3 ls s3://your-bucket/

# Check GCS credentials
gsutil ls gs://your-bucket/

# Verify IAM permissions
```

* *问题：数据库连接错误**
```bash
# Test PostgreSQL connection
psql postgresql://user:pwd@host:5432/db

# Check database version compatibility
lamin migrate check
```

* *问题：缓存full**
```python
# Clear cache
import lamindb as ln
import shutil
shutil.rmtree(ln.settings.cache_dir)

# Set larger cache location
lamin cache set /larger/disk/cache
```

## 升级和迁移

### 升级 LaminDB

```bash
# Upgrade to latest version
pip install --upgrade lamindb

# Upgrade database schema
lamin migrate deploy
```

### 架构兼容性

检查兼容性矩阵以确保您的数据库架构版本与您安装的兼容LaminDB 版本。

### 重大更改

主要版本升级可能需要迁移：

```bash
# Check for breaking changes
lamin migrate check

# Review migration plan
lamin migrate plan

# Execute migration
lamin migrate deploy
```

## 最佳实践

1. **启动本地，扩展云**：本地开发，部署到云进行生产
2. **使用 PostgreSQL 进行生产**：SQLite 仅用于开发
3. **配置适当的缓存**：根据工作集
4调整缓存大小。 **启用版本控制**：使用 S3/GCS 版本控制进行数据保护
5. **监控成本**：跟踪云部署中的存储和计算成本
6. **文档配置**：保留基础设施即代码以实现可重复性
7. **测试备份**：定期验证备份和恢复过程
8. **设置监控**：实施健康检查和警报
9. **有策略地使用模块**：仅安装所需的插件以降低复杂性
10. **规划规模**：考虑并发用户和数据增长
