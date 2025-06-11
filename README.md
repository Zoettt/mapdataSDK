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

## Test Data

The SDK includes a sample map data file (`mapdata.txt`) that contains:
- Real road network data from Shanghai area
- Approximately 100,000 nodes and 200,000 links
- Data format: Custom text format with the following structure:
  ```
  N <node_id> <x> <y> <z> [tags]
  L <link_id> <from_node> <to_node> <length> <lane_num_s2e> <lane_num_e2s> <speed_limit_s2e> <speed_limit_e2s> <traffic_light_s2e> <traffic_light_e2s> <junction> <geometry> [tags]
  R <relation_id> <node_id> <inlinks> <outlinks> [tags]
  ```

## Usage Examples

### 1. Loading and Basic Data Access

```python
from map_sdk import MapDataLoader

# Load map data from file
map_data = MapDataLoader.load_from_file('mapdata.txt')

# Access loaded data
nodes = map_data.get_all_nodes()
links = map_data.get_all_links()
relations = map_data.get_all_relations()

print(f"Loaded {len(nodes)} nodes, {len(links)} links, and {len(relations)} relations")
```

### 2. Point-based Query (Find Nearest Node)

```python
# Find the nearest node to a given point
test_point = (121.4670874, 31.23096049)  # A point in Shanghai
nearest_node = map_data.find_nearest_node(test_point[0], test_point[1])
print(f"Nearest node: {nearest_node.id} at ({nearest_node.x}, {nearest_node.y})")
```

### 3. Radius-based Query

```python
from example import find_elements_within_radius

# Find all elements within 100 meters of a point
test_point = (121.4670874, 31.23096049)
nodes, links, relations = find_elements_within_radius(map_data, test_point[0], test_point[1], 100)

print(f"Found {len(nodes)} nodes, {len(links)} links, and {len(relations)} relations within 100m")
```

### 4. Rectangle-based Query

```python
# Find all elements within a rectangle
rect_min_x = 121.4670874 - 0.001
rect_min_y = 31.23096049 - 0.001
rect_max_x = 121.4670874 + 0.001
rect_max_y = 31.23096049 + 0.001

nodes, links = map_data.get_elements_in_rectangle(rect_min_x, rect_min_y, rect_max_x, rect_max_y)
print(f"Found {len(nodes)} nodes and {len(links)} links in the rectangle")
```

### 5. Vehicle Trajectory Simulation

```python
from example import simulate_vehicle_trajectory, find_elements_within_radius

# Simulate a vehicle trajectory
start_point = (121.4670874, 31.23096049)
trajectory = simulate_vehicle_trajectory(start_point[0], start_point[1], duration=60)

# Find elements around each trajectory point
for i, (x, y) in enumerate(trajectory):
    print(f"\nTime point {i+1} ({i*10} seconds):")
    print(f"Vehicle position: ({x}, {y})")
    
    # Find elements within 2km
    nodes, links, relations = find_elements_within_radius(map_data, x, y, 2000)
    print(f"Found {len(nodes)} nodes, {len(links)} links, and {len(relations)} relations within 2km")
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

## 测试数据

SDK包含一个示例地图数据文件（`mapdata.txt`），其中包含：
- 某地区的实际路网数据
- 约10万个节点和20万个路段
- 数据格式：自定义文本格式，结构如下：
  ```
  N <节点ID> <x坐标> <y坐标> <z坐标> [标签]
  L <路段ID> <起始节点> <终止节点> <长度> <正向车道数> <反向车道数> <正向限速> <反向限速> <正向信号灯> <反向信号灯> <路口> <几何形状> [标签]
  R <关系ID> <节点ID> <入路段> <出路段> [标签]
  ```

## 使用示例

### 1. 数据加载和基本访问

```python
from map_sdk import MapDataLoader

# 从文件加载地图数据
map_data = MapDataLoader.load_from_file('mapdata.txt')

# 访问加载的数据
nodes = map_data.get_all_nodes()
links = map_data.get_all_links()
relations = map_data.get_all_relations()

print(f"加载了 {len(nodes)} 个节点，{len(links)} 个路段，{len(relations)} 个关系")
```

### 2. 点查询（查找最近节点）

```python
# 查找给定点最近的节点
test_point = (121.4670874, 31.23096049)  # 上海的一个点
nearest_node = map_data.find_nearest_node(test_point[0], test_point[1])
print(f"最近的节点: {nearest_node.id} 位于 ({nearest_node.x}, {nearest_node.y})")
```

### 3. 半径查询

```python
from example import find_elements_within_radius

# 查找点周围100米范围内的所有要素
test_point = (121.4670874, 31.23096049)
nodes, links, relations = find_elements_within_radius(map_data, test_point[0], test_point[1], 100)

print(f"100米范围内找到 {len(nodes)} 个节点，{len(links)} 个路段，{len(relations)} 个关系")
```

### 4. 矩形查询

```python
# 查找矩形范围内的所有要素
rect_min_x = 121.4670874 - 0.001
rect_min_y = 31.23096049 - 0.001
rect_max_x = 121.4670874 + 0.001
rect_max_y = 31.23096049 + 0.001

nodes, links = map_data.get_elements_in_rectangle(rect_min_x, rect_min_y, rect_max_x, rect_max_y)
print(f"矩形范围内找到 {len(nodes)} 个节点和 {len(links)} 个路段")
```

### 5. 根据车辆实时位置拉取数据

```python
from example import simulate_vehicle_trajectory, find_elements_within_radius

# 模拟车辆轨迹
start_point = (121.4670874, 31.23096049)
trajectory = simulate_vehicle_trajectory(start_point[0], start_point[1], duration=60)

# 查找每个轨迹点周围的要素
for i, (x, y) in enumerate(trajectory):
    print(f"\n时间点 {i+1}（{i*10}秒）:")
    print(f"车辆位置: ({x}, {y})")
    
    # 查找2公里范围内的要素
    nodes, links, relations = find_elements_within_radius(map_data, x, y, 2000)
    print(f"2公里范围内找到 {len(nodes)} 个节点，{len(links)} 个路段，{len(relations)} 个关系")
``` 