# Offline Map Data Processing SDK

This SDK provides functionality for processing and querying offline map data, including nodes, links, and their relationships.

## Features

1. **Basic Data Models**
   - Node: Represents a point in the road network
   - Link: Represents a road segment connecting two nodes
   - Relation: Represents the relationship between links and nodes (inlink -> node -> outlink)

2. **Query Capabilities**
   - Full data traversal
   - Point-based queries (find nearest node)
   - Rectangle-based queries (find elements within a rectangle)
   - 2km radius network queries

3. **Vehicle SDK**
   - Real-time network data query based on vehicle position
   - Efficient data retrieval for vehicle applications
   - Simple and focused API design

## Installation

### Ubuntu 20.04

1. **Install Dependencies**
```bash
# Make setup script executable
chmod +x setup.sh

# Run setup script
./setup.sh
```

2. **Activate Virtual Environment**
```bash
source venv/bin/activate
```

3. **Verify Installation**
```bash
# Run examples
python example.py
python vehicle_sdk_example.py
```

## Project Structure

```
.
├── map_sdk.py          # Core data models and basic operations
├── network_sdk.py      # Network query functionality
├── example.py          # General usage examples
├── vehicle_sdk_example.py # Vehicle SDK usage examples
├── requirements.txt    # Python dependencies
└── setup.sh           # Environment setup script
```

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

### Vehicle SDK Usage

```python
from vehicle_sdk import VehicleSDK

# Initialize SDK
sdk = VehicleSDK(map_data)

# Get network data around vehicle position
vehicle_pos = (100.0, 100.0)
nodes, links = sdk.get_network_around_position(vehicle_pos)

# Find nearest node
nearest_node = sdk.find_nearest_node(vehicle_pos)

# Get data in rectangle
rect_data = sdk.get_data_in_rectangle(0.0, 0.0, 200.0, 200.0)
```

---

# 离线地图数据处理SDK

本SDK提供了处理和查询离线地图数据的功能，包括节点、路段及其关系。

## 功能特点

1. **基础数据模型**
   - Node（节点）：表示路网中的点
   - Link（路段）：表示连接两个节点的道路段
   - Relation（关系）：表示路段和节点之间的关系（入路段 -> 节点 -> 出路段）

2. **查询功能**
   - 全要素遍历
   - 点查询（查找最近节点）
   - 矩形查询（查找矩形范围内的要素）
   - 2公里半径路网查询

3. **车端SDK**
   - 基于车辆位置的实时路网数据查询
   - 高效的数据获取机制
   - 简洁专注的API设计

## 安装说明

### Ubuntu 20.04

1. **安装依赖**
```bash
# 添加执行权限
chmod +x setup.sh

# 运行安装脚本
./setup.sh
```

2. **激活虚拟环境**
```bash
source venv/bin/activate
```

3. **验证安装**
```bash
# 运行示例
python example.py
python vehicle_sdk_example.py
```

## 项目结构

```
.
├── map_sdk.py          # 核心数据模型和基本操作
├── network_sdk.py      # 路网查询功能
├── example.py          # 通用使用示例
├── vehicle_sdk_example.py # 车端SDK使用示例
├── requirements.txt    # Python依赖
└── setup.sh           # 环境配置脚本
```

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

### 车端SDK使用

```python
from vehicle_sdk import VehicleSDK

# 初始化SDK
sdk = VehicleSDK(map_data)

# 获取车辆位置周围的路网数据
vehicle_pos = (100.0, 100.0)
nodes, links = sdk.get_network_around_position(vehicle_pos)

# 查找最近节点
nearest_node = sdk.find_nearest_node(vehicle_pos)

# 获取矩形范围内的数据
rect_data = sdk.get_data_in_rectangle(0.0, 0.0, 200.0, 200.0)
``` 