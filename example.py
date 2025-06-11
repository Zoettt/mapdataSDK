from map_sdk import MapData, Node, Link, Relation
import math
import time
from typing import List, Tuple, Dict
import random

class MapDataLoader:
    @staticmethod
    def load_from_file(filename: str) -> MapData:
        """Load map data from file"""
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
                    
                if parts[0] == 'N':  # Node
                    node_id = parts[1]
                    x = float(parts[2])
                    y = float(parts[3])
                    z = float(parts[4])
                    tags = {}
                    
                    # Parse raw data
                    for part in parts[5:]:
                        if '=' in part:
                            key, value = part.split('=', 1)
                            tags[key] = value
                            
                    node = Node(id=node_id, x=x, y=y, tags=tags)
                    map_data.add_node(node)
                    
                elif parts[0] == 'L':  # Link
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
                    
                    # Parse geometry
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
                    
                    # Parse raw data
                    for part in parts[13:]:
                        if '=' in part:
                            key, value = part.split('=', 1)
                            tags[key] = value
                            
                    link = Link(id=link_id, from_node=from_node, to_node=to_node, tags=tags)
                    map_data.add_link(link)
                    
                elif parts[0] == 'R':  # Relation
                    relation_id = parts[1]
                    node_id = parts[2]
                    inlinks = parts[3].split(',')
                    outlinks = parts[4].split(',')
                    
                    tags = {}
                    # Parse raw data
                    for part in parts[5:]:
                        if '=' in part:
                            key, value = part.split('=', 1)
                            tags[key] = value
                            
                    relation = Relation(id=relation_id, node_id=node_id, inlinks=inlinks, outlinks=outlinks)
                    map_data.add_relation(relation)
                    
        return map_data

def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate distance between two points (in meters)"""
    # Simplified distance calculation, should use more accurate spherical distance in practice
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * 111000  # Rough conversion to meters

def find_elements_within_radius(map_data: MapData, center_x: float, center_y: float, radius: float) -> Tuple[List[Node], List[Link], List[Relation]]:
    """Find elements within specified radius"""
    nodes = []
    links = []
    relations = []
    
    # Find nodes within radius
    for node in map_data.get_all_nodes():
        dist = calculate_distance(center_x, center_y, node.x, node.y)
        if dist <= radius:
            nodes.append(node)
            
    # Find links related to these nodes
    node_ids = {node.id for node in nodes}
    for link in map_data.get_all_links():
        if link.from_node in node_ids or link.to_node in node_ids:
            links.append(link)
            
    # Find relations related to these nodes
    for relation in map_data.get_all_relations():
        if relation.node_id in node_ids:
            relations.append(relation)
            
    return nodes, links, relations

def simulate_vehicle_trajectory(start_x: float, start_y: float, duration: int = 60) -> List[Tuple[float, float]]:
    """Simulate vehicle trajectory"""
    trajectory = []
    current_x, current_y = start_x, start_y
    
    # Simulate vehicle moving in one direction
    for _ in range(duration // 10):  # One point every 10 seconds
        # Random direction change
        angle = random.uniform(-0.1, 0.1)  # Small angle change
        distance = random.uniform(0.0001, 0.0003)  # Movement distance
        
        # Calculate new position
        current_x += distance * math.cos(angle)
        current_y += distance * math.sin(angle)
        
        trajectory.append((current_x, current_y))
        
    return trajectory

def main():
    # Load map data
    print("Loading map data...")
    map_data = MapDataLoader.load_from_file('mapdata.txt')
    print(f"Loaded: {len(map_data.get_all_nodes())} nodes, {len(map_data.get_all_links())} links, {len(map_data.get_all_relations())} relations")
    
    # Query 1: Traversal query
    print("\n1. Traversal query example:")
    print("Node examples:")
    for node in list(map_data.get_all_nodes())[:5]:  # Show first 5 nodes
        print(f"Node {node.id}: ({node.x}, {node.y})")
        
    print("\nLink examples:")
    for link in list(map_data.get_all_links())[:5]:  # Show first 5 links
        print(f"Link {link.id}: {link.from_node} -> {link.to_node}")
        
    print("\nRelation examples:")
    for relation in list(map_data.get_all_relations())[:5]:  # Show first 5 relations
        print(f"Relation {relation.id}: Node {relation.node_id}")
        print(f"  Inlinks: {relation.inlinks}")
        print(f"  Outlinks: {relation.outlinks}")
    
    # Query 2: Point query (100m radius)
    print("\n2. Point query example (100m radius):")
    test_point = (121.4670874, 31.23096049)  # Use an actual point from the map
    nodes, links, relations = find_elements_within_radius(map_data, test_point[0], test_point[1], 100)
    print(f"Found {len(nodes)} nodes, {len(links)} links, and {len(relations)} relations")
    
    # Show some details
    if nodes:
        print("\nNode examples:")
        for node in nodes[:3]:  # Show first 3 nodes
            print(f"Node {node.id}: ({node.x}, {node.y})")
            
    if links:
        print("\nLink examples:")
        for link in links[:3]:  # Show first 3 links
            print(f"Link {link.id}: {link.from_node} -> {link.to_node}")
            
    if relations:
        print("\nRelation examples:")
        for relation in relations[:3]:  # Show first 3 relations
            print(f"Relation {relation.id}: Node {relation.node_id}")
            print(f"  Inlinks: {relation.inlinks}")
            print(f"  Outlinks: {relation.outlinks}")
    
    # Query 3: Rectangle query
    print("\n3. Rectangle query example:")
    # Use rectangle around test point
    rect_min_x = test_point[0] - 0.001
    rect_min_y = test_point[1] - 0.001
    rect_max_x = test_point[0] + 0.001
    rect_max_y = test_point[1] + 0.001
    
    nodes, links = map_data.get_elements_in_rectangle(rect_min_x, rect_min_y, rect_max_x, rect_max_y)
    # Get relations related to these nodes
    node_ids = {node.id for node in nodes}
    relations = [r for r in map_data.get_all_relations() if r.node_id in node_ids]
    
    print(f"Rectangle range: ({rect_min_x}, {rect_min_y}) -> ({rect_max_x}, {rect_max_y})")
    print(f"Found {len(nodes)} nodes, {len(links)} links, and {len(relations)} relations")
    
    # Show some details
    if nodes:
        print("\nNode examples:")
        for node in nodes[:3]:  # Show first 3 nodes
            print(f"Node {node.id}: ({node.x}, {node.y})")
            
    if links:
        print("\nLink examples:")
        for link in links[:3]:  # Show first 3 links
            print(f"Link {link.id}: {link.from_node} -> {link.to_node}")
            
    if relations:
        print("\nRelation examples:")
        for relation in relations[:3]:  # Show first 3 relations
            print(f"Relation {relation.id}: Node {relation.node_id}")
            print(f"  Inlinks: {relation.inlinks}")
            print(f"  Outlinks: {relation.outlinks}")
    
    # Query 4: Vehicle trajectory simulation
    print("\n4. Vehicle trajectory simulation query (2km radius):")
    trajectory = simulate_vehicle_trajectory(test_point[0], test_point[1])
    
    for i, (x, y) in enumerate(trajectory):
        print(f"\nTime point {i+1} ({i*10} seconds):")
        print(f"Vehicle position: ({x}, {y})")
        
        # Find elements within 2km
        nodes, links, relations = find_elements_within_radius(map_data, x, y, 2000)
        print(f"Found {len(nodes)} nodes, {len(links)} links, and {len(relations)} relations within 2km")
        
        # Show some details
        if nodes:
            print("Node examples:")
            for node in nodes[:2]:  # Show first 2 nodes
                print(f"Node {node.id}: ({node.x}, {node.y})")
                
        if links:
            print("Link examples:")
            for link in links[:2]:  # Show first 2 links
                print(f"Link {link.id}: {link.from_node} -> {link.to_node}")
                
        if relations:
            print("Relation examples:")
            for relation in relations[:2]:  # Show first 2 relations
                print(f"Relation {relation.id}: Node {relation.node_id}")
                print(f"  Inlinks: {relation.inlinks}")
                print(f"  Outlinks: {relation.outlinks}")
        
        # Simulate real-time update interval
        time.sleep(1)  # Use 1 second interval for actual demo, instead of 10 seconds

if __name__ == "__main__":
    main() 