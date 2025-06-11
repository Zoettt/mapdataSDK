from typing import List, Set, Tuple
import math
from map_sdk import MapData, Node, Link, Point

class NetworkQuery:
    def __init__(self, map_data: MapData):
        self.map_data = map_data

    def _calculate_distance(self, point1: Point, point2: Point) -> float:
        return math.sqrt(
            (point2.x - point1.x) ** 2 +
            (point2.y - point1.y) ** 2
        )

    def _get_nodes_within_radius(self, center_point: Point, radius: float) -> Set[Node]:
        nodes_within_radius = set()
        for node in self.map_data.get_all_nodes():
            if self._calculate_distance(center_point, node.point) <= radius:
                nodes_within_radius.add(node)
        return nodes_within_radius

    def _get_connected_links(self, nodes: Set[Node]) -> Set[Link]:
        links = set()
        for node in nodes:
            links.update(node.links)
        return links

    def get_network_within_radius(self, center_point: Point, radius: float = 2000) -> Tuple[List[Node], List[Link]]:
        """
        Get all nodes within radius
        
        Args:
            center_point: center point coordinates
            radius: query radius (meters), default 2000 meters
            
        Returns:
            Tuple[List[Node], List[Link]]: return list of nodes and links within the radius
        """
        # Get all nodes within radius
        nodes = self._get_nodes_within_radius(center_point, radius)
        
        # Get all links related to these nodes
        links = self._get_connected_links(nodes)
        
        # Get all nodes related to these links (may include nodes outside radius)
        all_related_nodes = set()
        for link in links:
            all_related_nodes.add(link.start_node)
            all_related_nodes.add(link.end_node)
        
        return list(all_related_nodes), list(links) 