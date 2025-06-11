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
        获取指定点周围指定半径范围内的路网数据
        
        Args:
            center_point: 中心点坐标
            radius: 查询半径（米），默认2000米
            
        Returns:
            Tuple[List[Node], List[Link]]: 返回范围内的节点和路段列表
        """
        # 获取半径范围内的所有节点
        nodes = self._get_nodes_within_radius(center_point, radius)
        
        # 获取这些节点关联的所有路段
        links = self._get_connected_links(nodes)
        
        # 获取这些路段关联的所有节点（可能包含半径外的节点）
        all_related_nodes = set()
        for link in links:
            all_related_nodes.add(link.start_node)
            all_related_nodes.add(link.end_node)
        
        return list(all_related_nodes), list(links) 