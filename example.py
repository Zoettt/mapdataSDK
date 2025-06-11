from map_sdk import MapData, Node, Link, Relation

def main():
    # 创建地图数据实例
    map_data = MapData()
    
    # 添加一些测试数据
    # 添加节点
    node1 = Node(id=1, x=0.0, y=0.0, tags={"type": "intersection"})
    node2 = Node(id=2, x=100.0, y=0.0, tags={"type": "intersection"})
    node3 = Node(id=3, x=100.0, y=100.0, tags={"type": "intersection"})
    
    map_data.add_node(node1)
    map_data.add_node(node2)
    map_data.add_node(node3)
    
    # 添加路段
    link1 = Link(id=1, from_node=1, to_node=2, tags={"type": "road"})
    link2 = Link(id=2, from_node=2, to_node=3, tags={"type": "road"})
    
    map_data.add_link(link1)
    map_data.add_link(link2)
    
    # 添加关系
    relation1 = Relation(id=1, node_id=2, inlinks=[1], outlinks=[2])
    map_data.add_relation(relation1)
    
    # 测试查询功能
    print("\n测试查询功能:")
    print("1. 查找最近节点:")
    nearest = map_data.find_nearest_node(50.0, 10.0)
    print(f"最近节点: {nearest.id if nearest else None}")
    
    print("\n2. 矩形查询:")
    nodes, links = map_data.get_elements_in_rectangle(0.0, 0.0, 150.0, 150.0)
    print(f"找到 {len(nodes)} 个节点和 {len(links)} 个路段")
    
    # 测试更新功能
    print("\n测试更新功能:")
    print("1. 更新节点位置:")
    map_data.update_node(1, (10.0, 10.0))
    print(f"节点1新位置: x={map_data.get_node(1).x}, y={map_data.get_node(1).y}")
    
    print("\n2. 更新路段连接:")
    map_data.update_link(1, new_start_node=3)
    print(f"路段1新起点: {map_data.get_link(1).from_node}")
    
    print("\n3. 更新关系:")
    map_data.update_relation(1, new_inlink=2)
    print(f"关系1新入路段: {map_data.get_relation(1).inlinks}")

if __name__ == "__main__":
    main() 