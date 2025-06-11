from map_sdk import MapData, Node, Link, Relation
import math
import time
from typing import List, Tuple, Dict
import random

class MapDataLoader:
    @staticmethod
    def load_from_file(filename: str) -> MapData:
        """从文件加载地图数据"""
        map_data = MapData()
        
        with open(filename, 'r', encoding='utf-8') as f:
            current_section = None
            
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                parts = line.split()
                if not parts:
                    continue
                    
                if parts[0] == 'N':  # 节点
                    node_id = parts[1]
                    x = float(parts[2])
                    y = float(parts[3])
                    z = float(parts[4])
                    tags = {}
                    
                    # 解析原始数据
                    for part in parts[5:]:
                        if '=' in part:
                            key, value = part.split('=', 1)
                            tags[key] = value
                            
                    node = Node(id=node_id, x=x, y=y, tags=tags)
                    map_data.add_node(node)
                    
                elif parts[0] == 'L':  # 路段
                    link_id = parts[1]
                    from_node = parts[2]
                    to_node = parts[3]
                    length = float(parts[4])
                    lane_num_s2e = int(parts[5])
                    lane_num_e2s = int(parts[6])
                    speed_limit_s2e = int(parts[7])
                    speed_limit_e2s = int(parts[8])
                    traffic_light_s2e = bool(int(parts[9]))
                    traffic_light_e2s = bool(int(parts[10]))
                    junction = bool(int(parts[11]))
                    
                    # 解析几何形状
                    geometry_str = parts[12]
                    geometry = []
                    for point_str in geometry_str.split(';'):
                        x, y = map(float, point_str.split(','))
                        geometry.append((x, y))
                        
                    tags = {
                        'length': str(length),
                        'lane_num_s2e': str(lane_num_s2e),
                        'lane_num_e2s': str(lane_num_e2s),
                        'speed_limit_s2e': str(speed_limit_s2e),
                        'speed_limit_e2s': str(speed_limit_e2s),
                        'traffic_light_s2e': str(traffic_light_s2e),
                        'traffic_light_e2s': str(traffic_light_e2s),
                        'junction': str(junction)
                    }
                    
                    # 解析原始数据
                    for part in parts[13:]:
                        if '=' in part:
                            key, value = part.split('=', 1)
                            tags[key] = value
                            
                    link = Link(id=link_id, from_node=from_node, to_node=to_node, tags=tags)
                    map_data.add_link(link)
                    
                elif parts[0] == 'R':  # 关系
                    relation_id = parts[1]
                    node_id = parts[2]
                    inlinks = parts[3].split(',')
                    outlinks = parts[4].split(',')
                    
                    tags = {}
                    # 解析原始数据
                    for part in parts[5:]:
                        if '=' in part:
                            key, value = part.split('=', 1)
                            tags[key] = value
                            
                    relation = Relation(id=relation_id, node_id=node_id, inlinks=inlinks, outlinks=outlinks)
                    map_data.add_relation(relation)
                    
        return map_data

def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """计算两点之间的距离（米）"""
    # 简化的距离计算，实际应用中应该使用更精确的球面距离计算
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * 111000  # 粗略转换为米

def find_elements_within_radius(map_data: MapData, center_x: float, center_y: float, radius: float) -> Tuple[List[Node], List[Link], List[Relation]]:
    """查找指定半径范围内的要素"""
    nodes = []
    links = []
    relations = []
    
    # 查找范围内的节点
    for node in map_data.get_all_nodes():
        dist = calculate_distance(center_x, center_y, node.x, node.y)
        if dist <= radius:
            nodes.append(node)
            
    # 查找与这些节点相关的路段
    node_ids = {node.id for node in nodes}
    for link in map_data.get_all_links():
        if link.from_node in node_ids or link.to_node in node_ids:
            links.append(link)
            
    # 查找与这些节点相关的关系
    for relation in map_data.get_all_relations():
        if relation.node_id in node_ids:
            relations.append(relation)
            
    return nodes, links, relations

def simulate_vehicle_trajectory(start_x: float, start_y: float, duration: int = 60) -> List[Tuple[float, float]]:
    """模拟车辆轨迹"""
    trajectory = []
    current_x, current_y = start_x, start_y
    
    # 模拟车辆沿着一个方向移动
    for _ in range(duration // 10):  # 每10秒一个点
        # 随机方向变化
        angle = random.uniform(-0.1, 0.1)  # 小角度变化
        distance = random.uniform(0.0001, 0.0003)  # 移动距离
        
        # 计算新位置
        current_x += distance * math.cos(angle)
        current_y += distance * math.sin(angle)
        
        trajectory.append((current_x, current_y))
        
    return trajectory

def main():
    # 加载地图数据
    print("加载地图数据...")
    map_data = MapDataLoader.load_from_file('mapdata.txt')
    print(f"加载完成：{len(map_data.get_all_nodes())}个节点，{len(map_data.get_all_links())}个路段，{len(map_data.get_all_relations())}个关系")
    
    # 查询1：遍历查询
    print("\n1. 遍历查询示例：")
    print("节点示例：")
    for node in list(map_data.get_all_nodes())[:5]:  # 只显示前5个节点
        print(f"节点 {node.id}: ({node.x}, {node.y})")
        
    print("\n路段示例：")
    for link in list(map_data.get_all_links())[:5]:  # 只显示前5个路段
        print(f"路段 {link.id}: {link.from_node} -> {link.to_node}")
        
    print("\n关系示例：")
    for relation in list(map_data.get_all_relations())[:5]:  # 只显示前5个关系
        print(f"关系 {relation.id}: 节点 {relation.node_id}")
        print(f"  入路段: {relation.inlinks}")
        print(f"  出路段: {relation.outlinks}")
    
    # 查询2：点查询（100m范围）
    print("\n2. 点查询示例（100m范围）：")
    test_point = (121.4670874, 31.23096049)  # 使用地图中的一个实际点
    nodes, links, relations = find_elements_within_radius(map_data, test_point[0], test_point[1], 100)
    print(f"找到 {len(nodes)} 个节点、{len(links)} 个路段和 {len(relations)} 个关系")
    
    # 显示一些详细信息
    if nodes:
        print("\n节点示例：")
        for node in nodes[:3]:  # 显示前3个节点
            print(f"节点 {node.id}: ({node.x}, {node.y})")
            
    if links:
        print("\n路段示例：")
        for link in links[:3]:  # 显示前3个路段
            print(f"路段 {link.id}: {link.from_node} -> {link.to_node}")
            
    if relations:
        print("\n关系示例：")
        for relation in relations[:3]:  # 显示前3个关系
            print(f"关系 {relation.id}: 节点 {relation.node_id}")
            print(f"  入路段: {relation.inlinks}")
            print(f"  出路段: {relation.outlinks}")
    
    # 查询3：矩形查询
    print("\n3. 矩形查询示例：")
    # 使用测试点周围的矩形
    rect_min_x = test_point[0] - 0.001
    rect_min_y = test_point[1] - 0.001
    rect_max_x = test_point[0] + 0.001
    rect_max_y = test_point[1] + 0.001
    
    nodes, links = map_data.get_elements_in_rectangle(rect_min_x, rect_min_y, rect_max_x, rect_max_y)
    # 获取与这些节点相关的关系
    node_ids = {node.id for node in nodes}
    relations = [r for r in map_data.get_all_relations() if r.node_id in node_ids]
    
    print(f"矩形范围：({rect_min_x}, {rect_min_y}) -> ({rect_max_x}, {rect_max_y})")
    print(f"找到 {len(nodes)} 个节点、{len(links)} 个路段和 {len(relations)} 个关系")
    
    # 显示一些详细信息
    if nodes:
        print("\n节点示例：")
        for node in nodes[:3]:  # 显示前3个节点
            print(f"节点 {node.id}: ({node.x}, {node.y})")
            
    if links:
        print("\n路段示例：")
        for link in links[:3]:  # 显示前3个路段
            print(f"路段 {link.id}: {link.from_node} -> {link.to_node}")
            
    if relations:
        print("\n关系示例：")
        for relation in relations[:3]:  # 显示前3个关系
            print(f"关系 {relation.id}: 节点 {relation.node_id}")
            print(f"  入路段: {relation.inlinks}")
            print(f"  出路段: {relation.outlinks}")
    
    # 查询4：模拟车辆轨迹
    print("\n4. 模拟车辆轨迹查询（2km范围）：")
    trajectory = simulate_vehicle_trajectory(test_point[0], test_point[1])
    
    for i, (x, y) in enumerate(trajectory):
        print(f"\n时间点 {i+1}（{i*10}秒）:")
        print(f"车辆位置: ({x}, {y})")
        
        # 查找2km范围内的要素
        nodes, links, relations = find_elements_within_radius(map_data, x, y, 2000)
        print(f"2km范围内找到 {len(nodes)} 个节点、{len(links)} 个路段和 {len(relations)} 个关系")
        
        # 显示一些详细信息
        if nodes:
            print("节点示例：")
            for node in nodes[:2]:  # 显示前2个节点
                print(f"节点 {node.id}: ({node.x}, {node.y})")
                
        if links:
            print("路段示例：")
            for link in links[:2]:  # 显示前2个路段
                print(f"路段 {link.id}: {link.from_node} -> {link.to_node}")
                
        if relations:
            print("关系示例：")
            for relation in relations[:2]:  # 显示前2个关系
                print(f"关系 {relation.id}: 节点 {relation.node_id}")
                print(f"  入路段: {relation.inlinks}")
                print(f"  出路段: {relation.outlinks}")
        
        # 模拟实时更新间隔
        time.sleep(1)  # 实际演示时使用1秒间隔，而不是10秒

if __name__ == "__main__":
    main() 