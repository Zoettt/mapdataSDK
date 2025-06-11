import json
import math
from typing import Dict, List, Tuple

class MapDataProcessor:
    def __init__(self):
        self.nodes: Dict[str, Dict] = {}  # 节点数据
        self.links: Dict[str, Dict] = {}  # 路段数据
        self.relations: Dict[str, Dict] = {}  # 关系数据
        
    def process_node(self, node_info: Dict) -> str:
        """处理节点信息"""
        node_id = node_info['id']
        position = eval(node_info['position'])  # 解析坐标字符串
        
        self.nodes[node_id] = {
            'id': node_id,
            'x': position[0],  # 经度
            'y': position[1],  # 纬度
            'z': position[2],  # 高度
            'raw_data': node_info  # 保存原始数据
        }
        return node_id
        
    def process_link(self, link_data: Dict) -> str:
        """处理路段信息"""
        link_id = link_data['link_id']
        
        # 处理几何形状
        geometry = []
        for point in link_data['geometry']:
            geometry.append((point['x'], point['y']))
            
        # 计算路段长度
        length = 0
        for i in range(len(geometry) - 1):
            x1, y1 = geometry[i]
            x2, y2 = geometry[i + 1]
            length += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            
        self.links[link_id] = {
            'id': link_id,
            'from_node': link_data['start_node_info']['id'],
            'to_node': link_data['end_node_info']['id'],
            'geometry': geometry,
            'length': length,
            'lane_num_s2e': link_data['lane_num_s2e'],
            'lane_num_e2s': link_data['lane_num_e2s'],
            'speed_limit_s2e': link_data['speed_limit_s2e'],
            'speed_limit_e2s': link_data['speed_limit_e2s'],
            'traffic_light_s2e': link_data['traffic_light_s2e'],
            'traffic_light_e2s': link_data['traffic_light_e2s'],
            'junction': link_data['junction'],
            'raw_data': link_data  # 保存原始数据
        }
        return link_id
        
    def process_relation(self, link_data: Dict) -> str:
        """处理关系信息"""
        link_id = link_data['link_id']
        node_id = link_data['end_node_info']['id']
        
        # 创建关系
        relation_id = f"{link_id}:{node_id}"
        self.relations[relation_id] = {
            'id': relation_id,
            'node_id': node_id,
            'inlinks': [link_id],
            'outlinks': link_data.get('out_link_ids', []),  # 使用get方法，如果不存在则返回空列表
            'raw_data': {  # 保存原始数据
                'link_id': link_id,
                'node_id': node_id,
                'out_link_ids': link_data.get('out_link_ids', [])
            }
        }
        return relation_id
        
    def save_to_file(self, filename: str):
        """保存数据到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            # 写入节点数据
            f.write("# Nodes\n")
            for node_id, node_data in self.nodes.items():
                raw_data = node_data['raw_data']
                f.write(f"N {node_id} {node_data['x']} {node_data['y']} {node_data['z']} "
                       f"raw_id={raw_data.get('id', '')} "
                       f"raw_position={raw_data.get('position', '')}\n")
                
            # 写入路段数据
            f.write("\n# Links\n")
            for link_id, link_data in self.links.items():
                raw_data = link_data['raw_data']
                geometry_str = ';'.join([f"{x},{y}" for x, y in link_data['geometry']])
                f.write(f"L {link_id} {link_data['from_node']} {link_data['to_node']} "
                       f"{link_data['length']} {link_data['lane_num_s2e']} {link_data['lane_num_e2s']} "
                       f"{link_data['speed_limit_s2e']} {link_data['speed_limit_e2s']} "
                       f"{int(link_data['traffic_light_s2e'])} {int(link_data['traffic_light_e2s'])} "
                       f"{int(link_data['junction'])} {geometry_str} "
                       f"raw_id={raw_data.get('raw_id', '')} "
                       f"dr_link_id_backward={raw_data.get('dr_link_id_backward', '')} "
                       f"dr_link_id_forward={raw_data.get('dr_link_id_forward', '')} "
                       f"master_id={raw_data.get('master_id', '')} "
                       f"tp_id={raw_data.get('tp_id', '')} "
                       f"usage={raw_data.get('usage', [])}\n")
                
            # 写入关系数据
            f.write("\n# Relations\n")
            for relation_id, relation_data in self.relations.items():
                raw_data = relation_data['raw_data']
                inlinks_str = ','.join(relation_data['inlinks'])
                outlinks_str = ','.join(relation_data['outlinks'])
                f.write(f"R {relation_id} {relation_data['node_id']} {inlinks_str} {outlinks_str} "
                       f"raw_link_id={raw_data.get('link_id', '')} "
                       f"raw_node_id={raw_data.get('node_id', '')} "
                       f"raw_out_links={raw_data.get('out_link_ids', [])}\n")

def main():
    # 读取JSON文件
    with open('/Users/guanjie/Downloads/tencent_data/557040055.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 处理数据
    processor = MapDataProcessor()
    
    print("开始处理数据...")
    for link_data in data:
        # 处理节点
        start_node_id = processor.process_node(link_data['start_node_info'])
        end_node_id = processor.process_node(link_data['end_node_info'])
        
        # 处理路段
        link_id = processor.process_link(link_data)
        
        # 处理关系
        relation_id = processor.process_relation(link_data)
        
    # 保存数据
    print("保存数据到文件...")
    processor.save_to_file('mapdata.txt')
    print("处理完成！")

if __name__ == "__main__":
    main() 