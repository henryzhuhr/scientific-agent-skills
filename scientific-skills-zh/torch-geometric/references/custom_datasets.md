# 自定义数据集 — 完整参考

如何创建自己的图形数据集并从原始源（CSV、pandas、numpy 等）加载图形数据。

## 快速：不需要数据集类

对于合成数据或一次性图形，跳过数据集机制 — 只需创建 `Data` 对象并将它们传递给`DataLoader`:

```python
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader

data_list = [Data(x=..., edge_index=..., y=...) for _ in range(100)]
loader = DataLoader(data_list, batch_size=32)
```

## InMemoryDataset（适合 RAM）

用于适合 CPU 内存的可重用数据集。覆盖 4 个方法：

```python
from torch_geometric.data import InMemoryDataset, download_url

class MyDataset(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None, pre_filter=None):
        super().__init__(root, transform, pre_transform, pre_filter)
        self.load(self.processed_paths[0])

    @property
    def raw_file_names(self):
        # Files in raw_dir that must exist to skip download()
        return ['data.csv']

    @property
    def processed_file_names(self):
        # Files in processed_dir that must exist to skip process()
        return ['data.pt']

    def download(self):
        # Download raw files to self.raw_dir
        download_url('https://example.com/data.csv', self.raw_dir)

    def process(self):
        # Read raw data and create a list of Data objects
        data_list = [...]

        if self.pre_filter is not None:
            data_list = [d for d in data_list if self.pre_filter(d)]
        if self.pre_transform is not None:
            data_list = [self.pre_transform(d) for d in data_list]

        # save() collates list into one big Data + slices dict, then saves
        self.save(data_list, self.processed_paths[0])
```

* *自动创建的目录结构：**
```
root/
├── raw/          # raw_dir — downloaded files go here
│   └── data.csv
└── processed/    # processed_dir — processed .pt files go here
    └── data.pt
```

* *关键行为：**
- `download()` 仅在 `raw_file_names` 中缺少文件时运行`raw_dir`
- 仅当 `processed_file_names` 中的文件从 `processed_dir`
 中丢失时，`process()` 才运行 - 如果更改 `pre_transform`，请删除 `processed/` 目录以重新处理`processed/`## 数据集（不适合RAM)

对于非常大的数据集，单独保存每个图形：

```python
import os.path as osp
import torch
from torch_geometric.data import Dataset, download_url

class LargeDataset(Dataset):
    def __init__(self, root, transform=None, pre_transform=None):
        super().__init__(root, transform, pre_transform)

    @property
    def raw_file_names(self):
        return ['graph_data.csv']

    @property
    def processed_file_names(self):
        return [f'data_{i}.pt' for i in range(1000)]

    def download(self):
        download_url('...', self.raw_dir)

    def process(self):
        for idx in range(1000):
            data = Data(...)  # Build graph from raw data
            if self.pre_filter is not None and not self.pre_filter(data):
                continue
            if self.pre_transform is not None:
                data = self.pre_transform(data)
            torch.save(data, osp.join(self.processed_dir, f'data_{idx}.pt'))

    def len(self):
        return 1000

    def get(self, idx):
        return torch.load(osp.join(self.processed_dir, f'data_{idx}.pt'))
```

## 从CSV加载图形

A常见模式：将节点/边数据从CSV文件加载到HeteroData对象中。

### 步骤1：加载节点features

```python
import pandas as pd
import torch

def load_node_csv(path, index_col, encoders=None):
    df = pd.read_csv(path, index_col=index_col)
    # Map original IDs to consecutive 0..N-1 indices
    mapping = {idx: i for i, idx in enumerate(df.index.unique())}

    x = None
    if encoders is not None:
        xs = [encoder(df[col]) for col, encoder in encoders.items()]
        x = torch.cat(xs, dim=-1)

    return x, mapping
```

### 步骤 2：加载边

```python
def load_edge_csv(path, src_index_col, src_mapping, dst_index_col, dst_mapping,
                  encoders=None):
    df = pd.read_csv(path)
    src = [src_mapping[idx] for idx in df[src_index_col]]
    dst = [dst_mapping[idx] for idx in df[dst_index_col]]
    edge_index = torch.tensor([src, dst])

    edge_attr = None
    if encoders is not None:
        edge_attrs = [encoder(df[col]) for col, encoder in encoders.items()]
        edge_attr = torch.cat(edge_attrs, dim=-1)

    return edge_index, edge_attr
```

### 步骤 3：组装 HeteroData

```python
from torch_geometric.data import HeteroData

# Load nodes
movie_x, movie_mapping = load_node_csv('movies.csv', 'movieId',
    encoders={'genres': GenresEncoder()})
_, user_mapping = load_node_csv('ratings.csv', 'userId')

# Load edges
edge_index, edge_label = load_edge_csv('ratings.csv',
    src_index_col='userId', src_mapping=user_mapping,
    dst_index_col='movieId', dst_mapping=movie_mapping,
    encoders={'rating': IdentityEncoder(dtype=torch.long)})

# Build HeteroData
data = HeteroData()
data['user'].num_nodes = len(user_mapping)
data['movie'].x = movie_x
data['user', 'rates', 'movie'].edge_index = edge_index
data['user', 'rates', 'movie'].edge_label = edge_label
```

### 通用编码器

```python
class IdentityEncoder:
    """Encode a numeric column as-is."""
    def __init__(self, dtype=None):
        self.dtype = dtype
    def __call__(self, df):
        return torch.from_numpy(df.values).view(-1, 1).to(self.dtype)

class GenresEncoder:
    """Multi-hot encode a pipe-separated categorical column."""
    def __init__(self, sep='|'):
        self.sep = sep
    def __call__(self, df):
        genres = set(g for col in df.values for g in col.split(self.sep))
        mapping = {genre: i for i, genre in enumerate(genres)}
        x = torch.zeros(len(df), len(mapping))
        for i, col in enumerate(df.values):
            for genre in col.split(self.sep):
                x[i, mapping[genre]] = 1
        return x
```

对于文本特征，使用句子转换器：

```python
from sentence_transformers import SentenceTransformer

class SequenceEncoder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    @torch.no_grad()
    def __call__(self, df):
        return self.model.encode(df.values, convert_to_tensor=True).cpu()
```

## 来自网络X

```python
from torch_geometric.utils import from_networkx
import networkx as nx

G = nx.karate_club_graph()
data = from_networkx(G)
# Node attributes become data.x, edge attributes become data.edge_attr
```

## 来自scipy稀疏邻接矩阵

```python
from torch_geometric.utils import from_scipy_sparse_matrix

edge_index, edge_attr = from_scipy_sparse_matrix(adj_matrix)
data = Data(x=features, edge_index=edge_index)
```

## 无特征节点

如果节点没有特征，常用选项：
- 在训练时使用`torch.nn.Embedding`学习特征
- 设置`data['node_type'].num_nodes = N`（用于HeteroData）
- 使用结构特征：度、聚类系数等。
- 使用`data.x = torch.eye(num_nodes)`（one-hot，仅适用于小图）
