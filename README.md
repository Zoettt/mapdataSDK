# Offline Map Data Processing SDK

This SDK provides functionality for processing and querying offline map data, including nodes, links, and their relationships.

## Features

1. **Basic Data Models**
   - Node: Represents a point in the road network with coordinates and tags
   - Link: Represents a road segment connecting two nodes with geometry and attributes
   - Relation: Represents the relationship between links and nodes (inlink -> node -> outlink)

2. **Data Loading and Processing**
   - Support for loading map data from text files
   - Efficient data parsing and storage
   - Flexible tag system for additional attributes

3. **Query Capabilities**
   - Full data traversal
   - Point-based queries (find nearest node)
   - Rectangle-based queries (find elements within a rectangle)
   - Radius-based queries (find elements within a specified radius)
   - Vehicle trajectory simulation and tracking

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the Repository**
```bash
git clone [repository-url]
cd [repository-name]
```

2. **Install Dependencies**
```bash
# Make setup script executable
chmod +x setup.sh

# Run setup script
./setup.sh
```

3. **Activate Virtual Environment**
```bash
source venv/bin/activate
```

4. **Verify Installation**
```bash
# Run example
python example.py
```

## Project Structure

```
.
├── map_sdk.py          # Core data models and basic operations
├── network_sdk.py      # Network query functionality
├── example.py          # General usage examples
├── process_map_data.py # Map data processing utilities
├── requirements.txt    # Python dependencies
├── setup.sh           # Environment setup script
└── mapdata.txt        # Sample map data file
```

## Dependencies

- typing-extensions >= 4.0.0
- dataclasses (for Python < 3.7)

## Usage Examples

### Basic Usage

```python
from map_sdk import MapData, Node, Link, Relation

# Create map data instance
map_data = MapData()

# Add nodes
node1 = Node(id=1, x=0.0, y=0.0, tags={"type": "intersection"})
node2 = Node(id=2, x=100.0, y=0.0, tags={"type": "intersection"})
map_data.add_node(node1)
map_data.add_node(node2)

# Add links
link1 = Link(id=1, from_node=1, to_node=2, tags={"type": "road"})
map_data.add_link(link1)

# Add relations
relation1 = Relation(id=1, node_id=2, inlinks=[1], outlinks=[])
map_data.add_relation(relation1)

# Find nearest node
nearest = map_data.find_nearest_node(50.0, 10.0)

# Get elements in rectangle
nodes, links = map_data.get_elements_in_rectangle(0.0, 0.0, 150.0, 150.0)
```

### Loading Map Data from File

```python
from map_sdk import MapDataLoader

# Load map data from file
map_data = MapDataLoader.load_from_file('mapdata.txt')

# Access loaded data
nodes = map_data.get_all_nodes()
links = map_data.get_all_links()
relations = map_data.get_all_relations()
```

### Vehicle Trajectory Simulation

```python
from example import simulate_vehicle_trajectory, find_elements_within_radius

# Simulate vehicle trajectory
start_point = (121.4670874, 31.23096049)
trajectory = simulate_vehicle_trajectory(start_point[0], start_point[1], duration=60)

# Find elements around each trajectory point
for x, y in trajectory:
    nodes, links, relations = find_elements_within_radius(map_data, x, y, 2000)
    # Process the found elements...
```

---

# 离线地图数据处理SDK

本SDK提供了处理和查询离线地图数据的功能，包括节点、路段及其关系。

## 功能特点

1. **基础数据模型**
   - Node（节点）：表示路网中的点，包含坐标和属性标签
   - Link（路段）：表示连接两个节点的道路段，包含几何形状和属性
   - Relation（关系）：表示路段和节点之间的关系（入路段 -> 节点 -> 出路段）

2. **数据加载和处理**
   - 支持从文本文件加载地图数据
   - 高效的数据解析和存储
   - 灵活的标签系统，支持额外属性

3. **查询功能**
   - 全要素遍历
   - 点查询（查找最近节点）
   - 矩形查询（查找矩形范围内的要素）
   - 半径查询（查找指定半径范围内的要素）
   - 车辆轨迹模拟和跟踪

## 安装说明

### 环境要求
- Python 3.6 或更高版本
- pip（Python包管理器）

### 安装步骤

1. **克隆仓库**
```bash
git clone [仓库地址]
cd [仓库名称]
```

2. **安装依赖**
```bash
# 添加执行权限
chmod +x setup.sh

# 运行安装脚本
./setup.sh
```

3. **激活虚拟环境**
```bash
source venv/bin/activate
```

4. **验证安装**
```bash
# 运行示例
python example.py
```

## 项目结构

```
.
├── map_sdk.py          # 核心数据模型和基本操作
├── network_sdk.py      # 路网查询功能
├── example.py          # 通用使用示例
├── process_map_data.py # 地图数据处理工具
├── requirements.txt    # Python依赖
├── setup.sh           # 环境配置脚本
└── mapdata.txt        # 示例地图数据文件
```

## 依赖要求

- typing-extensions >= 4.0.0
- dataclasses (Python < 3.7 需要)

## 使用示例

### 基本使用

```python
from map_sdk import MapData, Node, Link, Relation

# 创建地图数据实例
map_data = MapData()

# 添加节点
node1 = Node(id=1, x=0.0, y=0.0, tags={"type": "intersection"})
node2 = Node(id=2, x=100.0, y=0.0, tags={"type": "intersection"})
map_data.add_node(node1)
map_data.add_node(node2)

# 添加路段
link1 = Link(id=1, from_node=1, to_node=2, tags={"type": "road"})
map_data.add_link(link1)

# 添加关系
relation1 = Relation(id=1, node_id=2, inlinks=[1], outlinks=[])
map_data.add_relation(relation1)

# 查找最近节点
nearest = map_data.find_nearest_node(50.0, 10.0)

# 获取矩形范围内的要素
nodes, links = map_data.get_elements_in_rectangle(0.0, 0.0, 150.0, 150.0)
```

### 从文件加载地图数据

```python
from map_sdk import MapDataLoader

# 从文件加载地图数据
map_data = MapDataLoader.load_from_file('mapdata.txt')

# 访问加载的数据
nodes = map_data.get_all_nodes()
links = map_data.get_all_links()
relations = map_data.get_all_relations()
```

### 车辆轨迹模拟

```python
from example import simulate_vehicle_trajectory, find_elements_within_radius

# 模拟车辆轨迹
start_point = (121.4670874, 31.23096049)
trajectory = simulate_vehicle_trajectory(start_point[0], start_point[1], duration=60)

# 查找每个轨迹点周围的要素
for x, y in trajectory:
    nodes, links, relations = find_elements_within_radius(map_data, x, y, 2000)
    # 处理找到的要素...
``` 