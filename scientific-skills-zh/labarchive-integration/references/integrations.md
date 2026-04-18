# LabArchives 第三方集成

## 概述

LabArchives 与众多科学软件平台集成，以简化研究工作流程。本文档涵盖了每个受支持平台的编程集成方法、自动化策略和最佳实践。

## 集成类别

### 1. 协议管理

#### Protocols.io Integration

将协议直接从 Protocols.io 导出到 LabArchives 笔记本。

* *用例：**
- 标准化整个实验室的实验程序笔记本
- 维护协议的版本控制
- 将协议链接到实验结果

* *设置：**
1. 在 LabArchives 设置中启用 Protocols.io 集成 
2. 使用 Protocols.io 帐户
3 进行身份验证。浏览并选择要导出的协议

* *编程方法：**
```python
# Export Protocols.io protocol as HTML/PDF
# Then upload to LabArchives via API

def import_protocol_to_labarchives(client, uid, nbid, protocol_id):
    """Import Protocols.io protocol to LabArchives entry"""
    # 1. Fetch protocol from Protocols.io API
    protocol_data = fetch_protocol_from_protocolsio(protocol_id)

    # 2. Create new entry in LabArchives
    entry_params = {
        'uid': uid,
        'nbid': nbid,
        'title': f"Protocol: {protocol_data['title']}",
        'content': protocol_data['html_content']
    }
    response = client.make_call('entries', 'create_entry', params=entry_params)

    # 3. Add protocol metadata as comment
    entry_id = extract_entry_id(response)
    comment_params = {
        'uid': uid,
        'nbid': nbid,
        'entry_id': entry_id,
        'comment': f"Protocols.io ID: {protocol_id}<br>Version: {protocol_data['version']}"
    }
    client.make_call('entries', 'create_comment', params=comment_params)

    return entry_id
```

* *更新：** 2025年9月22日

### 2.数据分析工具

#### GraphPad Prism Integration（版本8+）

Export 

* *用例：**
- 使用原始数据存档统计分析
- 出版物的文档图形生成
- 维护合规分析审计跟踪

* *设置：**
1. 安装 GraphPad Prism 8 或更高版本
2. 在 Prism 首选项 
3 中配置 LabArchives 连接。使用“文件”菜单中的“导出到 LabArchives”选项

* *编程方法：**
```python
# Upload Prism files to LabArchives via API

def upload_prism_analysis(client, uid, nbid, entry_id, prism_file_path):
    """Upload GraphPad Prism file to LabArchives entry"""
    import requests

    url = f'{client.api_url}/entries/upload_attachment'
    files = {'file': open(prism_file_path, 'rb')}
    params = {
        'uid': uid,
        'nbid': nbid,
        'entry_id': entry_id,
        'filename': os.path.basename(prism_file_path),
        'access_key_id': client.access_key_id,
        'access_password': client.access_password
    }

    response = requests.post(url, files=files, data=params)
    return response
```

* *支持的文件类型：**
- .pzfx（Prism 项目文件）
- .png、.jpg、 .pdf（导出的图表）
- .xlsx（导出的数据表）

* *更新：** 2025 年 9 月 8 日

### 3. 分子生物学和生物信息学

#### SnapGene Integration

Direct分子生物学工作流程、质粒图谱和序列分析的集成。

* *使用案例：**
- 文档克隆策略
- 将质粒图谱与实验记录存档
- 将序列链接到实验结果

* *设置：**
1. 安装 SnapGene 软件
2. 在 SnapGene 首选项 
3 中启用 LabArchives 导出。使用“发送到实验室档案”功能

* *文件格式支持：**
- .dna（SnapGene 文件）
- .gb、.gbk（GenBank 格式）
- .fasta（序列文件）
- .png、.pdf（质粒图谱）导出）

* *编程工作流程：**
```python
def upload_snapgene_file(client, uid, nbid, entry_id, snapgene_file):
    """Upload SnapGene file with preview image"""
    # Upload main SnapGene file
    upload_attachment(client, uid, nbid, entry_id, snapgene_file)

    # Generate and upload preview image (requires SnapGene CLI)
    preview_png = generate_snapgene_preview(snapgene_file)
    upload_attachment(client, uid, nbid, entry_id, preview_png)
```

#### Geneious Integration

生物信息学分析从Geneious导出到LabArchives。

* *用例：**
- 存档序列比对和系统发育树
- 文档NGS 分析管道
- 将生物信息学工作流程链接到湿实验室实验

* *支持的导出：**
- 序列比对
- 系统发育树
- 组装报告
- 变异调用结果

* *文件格式：**
- .geneious（Geneious 文档）
- .fasta、.fastq（序列数据）
- .bam、.sam（比对文件）
- .vcf（变体文件）

### 4. 计算笔记本

#### Jupyter 集成

将 Jupyter 笔记本嵌入为可重复计算研究的 LabArchives 条目。

* *用例：**
- 文档数据分析工作流程
- 存档计算实验
- 链接代码、结果和叙述

* *工作流程：**

```python
def export_jupyter_to_labarchives(notebook_path, client, uid, nbid):
    """Export Jupyter notebook to LabArchives"""
    import nbformat
    from nbconvert import HTMLExporter

    # Load notebook
    with open(notebook_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)

    # Convert to HTML
    html_exporter = HTMLExporter()
    html_exporter.template_name = 'classic'
    (body, resources) = html_exporter.from_notebook_node(nb)

    # Create entry in LabArchives
    entry_params = {
        'uid': uid,
        'nbid': nbid,
        'title': f"Jupyter Notebook: {os.path.basename(notebook_path)}",
        'content': body
    }
    response = client.make_call('entries', 'create_entry', params=entry_params)

    # Upload original .ipynb file as attachment
    entry_id = extract_entry_id(response)
    upload_attachment(client, uid, nbid, entry_id, notebook_path)

    return entry_id
```

* *最佳实践：**
- 包含输出的导出（导出前运行所有单元）
- 包含environment.yml或requirements.txt作为附件
- 在中添加执行时间戳和系统信息评论

### 5. 临床研究

#### REDCap 集成

临床数据采集与 LabArchives 集成，以实现研究合规性和审计跟踪。

* *用例：**
- 将临床数据收集链接到研究笔记本
- 维护监管审计跟踪合规性
- 记录临床试验方案和修订

* *集成方法：**
- REDCap API 将数据导出到LabArchives 条目
- 纵向研究的自动数据同步
- 符合HIPAA 的数据处理

* *示例工作流程：**
```python
def sync_redcap_to_labarchives(redcap_api_token, client, uid, nbid):
    """Sync REDCap data to LabArchives"""
    # Fetch REDCap data
    redcap_data = fetch_redcap_data(redcap_api_token)

    # Create LabArchives entry
    entry_params = {
        'uid': uid,
        'nbid': nbid,
        'title': f"REDCap Data Export {datetime.now().strftime('%Y-%m-%d')}",
        'content': format_redcap_data_html(redcap_data)
    }
    response = client.make_call('entries', 'create_entry', params=entry_params)

    return response
```

* *合规性功能：**
- 21 CFR Part 11 合规性
- 审计跟踪维护
- 数据完整性验证

### 6. 研究出版

#### Qeios集成

用于预印本和同行评审的研究发布平台集成。

* *用例：**
- 将研究结果导出到预印本服务器
- 文档发布工作流程
- 将已发表的文章链接到实验室笔记本

* *工作流程：**
- 从导出格式化条目LabArchives
- 提交到 Qeios 平台
- 维护笔记本和出版物之间的双向链接

#### SciSpace Integration

文献管理和引文集成。

* *用例：**
- 链接实验程序的参考文献
- 维护文献综述笔记本
- 生成报告参考书目

* *功能：**
- 引文从SciSpace 导入到LabArchives
- PDF 注释同步
- 参考管理

## OAuth 身份验证集成

LabArchives 现在使用 OAuth 2.0 进行新的第三方集成。

* *应用程序开发人员的 OAuth 流程：**

```python
def labarchives_oauth_flow(client_id, client_secret, redirect_uri):
    """Implement OAuth 2.0 flow for LabArchives integration"""
    import requests

    # Step 1: Get authorization code
    auth_url = "https://mynotebook.labarchives.com/oauth/authorize"
    auth_params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'read write'
    }
    # User visits auth_url and grants permission

    # Step 2: Exchange code for access token
    token_url = "https://mynotebook.labarchives.com/oauth/token"
    token_params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
        'code': authorization_code  # From redirect
    }

    response = requests.post(token_url, data=token_params)
    tokens = response.json()

    return tokens['access_token'], tokens['refresh_token']
```

* *OAuth 优点：**
- 比 API 密钥更安全
- 细粒度权限control
- 长时间运行集成的令牌刷新
- 可撤销访问

## 自定义集成开发

### 常规工作流程

对于未正式支持的工具，开发自定义集成：

1. **从源应用程序导出数据**（API 或文件导出）
2. **将格式转换**为 HTML 或支持的文件类型
3. **使用 LabArchives API
4 进行身份验证**。 **创建条目**或上传附件
5. **通过注释添加元数据**以实现可追溯性

### 示例：自定义集成模板

```python
class LabArchivesIntegration:
    """Template for custom LabArchives integrations"""

    def __init__(self, config_path):
        self.client = self._init_client(config_path)
        self.uid = self._authenticate()

    def _init_client(self, config_path):
        """Initialize LabArchives client"""
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return Client(config['api_url'],
                     config['access_key_id'],
                     config['access_password'])

    def _authenticate(self):
        """Get user ID"""
        # Implementation from authentication_guide.md
        pass

    def export_data(self, source_data, nbid, title):
        """Export data to LabArchives"""
        # Transform data to HTML
        html_content = self._transform_to_html(source_data)

        # Create entry
        params = {
            'uid': self.uid,
            'nbid': nbid,
            'title': title,
            'content': html_content
        }
        response = self.client.make_call('entries', 'create_entry', params=params)

        return extract_entry_id(response)

    def _transform_to_html(self, data):
        """Transform data to HTML format"""
        # Custom transformation logic
        pass
```

## 集成最佳实践

1. **版本控制：** 跟踪哪个软件版本生成了数据
2. **元数据保存：**包括时间戳、用户信息和处理参数
3. **文件格式标准：** 尽可能使用开放格式（CSV、JSON、HTML）
4. **批量操作：**对批量上传实施速率限制
5. **错误处理：** 使用指数退避 
6 实现重试逻辑。 **审核跟踪：** 记录所有 API 操作以确保合规性
7. **测试：** 在生产使用之前验证测试笔记本中的集成

## 集成故障排除

### 常见问题

 * *集成未出现在实验室档案中：**
- 验证管理员是否启用了集成
- 如果使用 OAuth
，则检查 OAuth 权限
- 确保兼容软件版本

* *文件上传失败：**
- 验证文件大小限制（通常每个文件 2GB）
- 检查文件格式兼容性
- 确保足够的存储配额

* *身份验证错误：**
- 验证 API 凭据是否为最新
- 检查集成特定令牌是否具有已过期
- 确认用户拥有必要的权限

### 集成支持

对于特定于集成的问题：
- 检查软件供应商文档（例如 GraphPad、Protocols.io）
- 联系 LabArchives 支持：support@labarchives.com
- 查看 LabArchives 知识基地：help.labarchives.com

## 未来集成机会

定制开发的潜在集成：
- 电子数据采集（EDC）系统
- 实验室信息管理系统（LIMS）
- 仪器数据系统（色谱、光谱）
- 云存储平台（Box， Dropbox、Google Drive）
- 项目管理工具（Asana、Monday.com）
- 拨款管理系统

 如需定制集成开发，请联系 LabArchives 获取 API 合作机会。
