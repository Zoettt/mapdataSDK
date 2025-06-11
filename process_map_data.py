import json
import math
from typing import Dict, List, Tuple

class MapDataProcessor:
    def __init__(self):
        self.nodes: Dict[str, Dict] = {}  # Node data
        self.links: Dict[str, Dict] = {}  # Link data
        self.relations: Dict[str, Dict] = {}  # Relation data
        
    def process_node(self, node_info: Dict):
        position = eval(node_info['position'])  # Parse coordinate string
        self.nodes[node_info['id']] = {
            'x': position[0],  # Longitude
            'y': position[1],  # Latitude
            'z': position[2],  # Altitude
            'raw_data': node_info  # Save raw data
        }
        
    def process_link(self, link_data: Dict):
        # Process geometry
        geometry = []
        for point in link_data['geometry']:
            geometry.append((point[0], point[1]))
            
        # Calculate link length
        length = 0
        for i in range(len(geometry) - 1):
            x1, y1 = geometry[i]
            x2, y2 = geometry[i + 1]
            length += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * 111000  # Convert to meters
            
        self.links[link_data['id']] = {
            'from_node': link_data['from_node'],
            'to_node': link_data['to_node'],
            'length': length,
            'lane_num_s2e': link_data.get('lane_num_s2e', 1),
            'lane_num_e2s': link_data.get('lane_num_e2s', 1),
            'speed_limit_s2e': link_data.get('speed_limit_s2e', 60),
            'speed_limit_e2s': link_data.get('speed_limit_e2s', 60),
            'traffic_light_s2e': link_data.get('traffic_light_s2e', False),
            'traffic_light_e2s': link_data.get('traffic_light_e2s', False),
            'junction': link_data.get('junction', False),
            'geometry': geometry,
            'raw_data': link_data  # Save raw data
        }
        
    def process_relation(self, link_data: Dict):
        # Create relation
        self.relations[link_data['id']] = {
            'node_id': link_data['node_id'],
            'inlinks': link_data.get('in_link_ids', []),  # Use get method, return empty list if not exists
            'outlinks': link_data.get('out_link_ids', []),  # Use get method, return empty list if not exists
            'raw_data': {  # Save raw data
                'node_id': link_data['node_id'],
                'in_link_ids': link_data.get('in_link_ids', []),
                'out_link_ids': link_data.get('out_link_ids', [])
            }
        }
        
    def save_to_file(self, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            # Write node data
            for node_id, node_data in self.nodes.items():
                f.write(f"N {node_id} {node_data['x']} {node_data['y']} {node_data['z']}\n")
                
            # Write link data
            for link_id, link_data in self.links.items():
                geometry_str = ';'.join([f"{x},{y}" for x, y in link_data['geometry']])
                f.write(f"L {link_id} {link_data['from_node']} {link_data['to_node']} "
                       f"{link_data['length']} {link_data['lane_num_s2e']} {link_data['lane_num_e2s']} "
                       f"{link_data['speed_limit_s2e']} {link_data['speed_limit_e2s']} "
                       f"{int(link_data['traffic_light_s2e'])} {int(link_data['traffic_light_e2s'])} "
                       f"{int(link_data['junction'])} {geometry_str}\n")
                
            # Write relation data
            for relation_id, relation_data in self.relations.items():
                f.write(f"R {relation_id} {relation_data['node_id']} "
                       f"{','.join(relation_data['inlinks'])} {','.join(relation_data['outlinks'])}\n")
                
def process_json_file(input_file: str, output_file: str):
    # Read JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Process data
    processor = MapDataProcessor()
    
    # Process nodes
    for node in data.get('nodes', []):
        processor.process_node(node)
        
    # Process links
    for link in data.get('links', []):
        processor.process_link(link)
        
    # Process relations
    for relation in data.get('relations', []):
        processor.process_relation(relation)
        
    # Save data
    processor.save_to_file(output_file)

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