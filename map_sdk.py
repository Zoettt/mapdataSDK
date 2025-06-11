from typing import List, Dict, Optional, Tuple
import math
from dataclasses import dataclass

@dataclass
class Node:
    id: int
    x: float
    y: float
    tags: Dict[str, str]

@dataclass
class Link:
    id: int
    from_node: int
    to_node: int
    tags: Dict[str, str]

@dataclass
class Relation:
    id: int
    node_id: int
    inlinks: List[int]
    outlinks: List[int]

class MapData:
    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        self.links: Dict[int, Link] = {}
        self.relations: Dict[int, Relation] = {}
        self._update_callbacks = []

    def add_update_callback(self, callback):
        """
        Add data update callback function
        Args:
            callback: Function to be called when data is updated
        """
        self._update_callbacks.append(callback)

    def _notify_update(self, update_type: str, data_id: int):
        """
        Notify data update
        Args:
            update_type: Update type ('node', 'link', 'relation')
            data_id: Updated data ID
        """
        for callback in self._update_callbacks:
            callback(update_type, data_id)

    def update_node(self, node_id: int, new_point: Tuple[float, float]) -> bool:
        """
        Update node location
        Args:
            node_id: Node ID
            new_point: New location
        Returns:
            bool: Whether the update was successful
        """
        if node_id not in self.nodes:
            return False
        
        node = self.nodes[node_id]
        node.x, node.y = new_point
        self._notify_update('node', node_id)
        return True

    def update_link(self, link_id: int, new_start_node: int = None, new_end_node: int = None) -> bool:
        """
        Update road connection relationship
        Args:
            link_id: Road section ID
            new_start_node: New starting node
            new_end_node: New ending node
        Returns:
            bool: Whether the update was successful
        """
        if link_id not in self.links:
            return False
        
        link = self.links[link_id]
        if new_start_node:
            link.from_node = new_start_node
        if new_end_node:
            link.to_node = new_end_node
        
        self._notify_update('link', link_id)
        return True

    def update_relation(self, relation_id: int, new_inlink: int = None, 
                       new_node: int = None, new_outlink: int = None) -> bool:
        """
        Update relationship
        Args:
            relation_id: Relationship ID
            new_inlink: New incoming road
            new_node: New node
            new_outlink: New outgoing road
        Returns:
            bool: Whether the update was successful
        """
        if relation_id not in self.relations:
            return False
        
        relation = self.relations[relation_id]
        if new_inlink:
            relation.inlinks = [new_inlink]
        if new_node:
            relation.node_id = new_node
        if new_outlink:
            relation.outlinks = [new_outlink]
        
        self._notify_update('relation', relation_id)
        return True

    def batch_update(self, updates: List[tuple]):
        """
        Batch update data
        Args:
            updates: Update list, each element is a tuple of (update_type, data_id, new_data)
        """
        for update_type, data_id, new_data in updates:
            if update_type == 'node':
                self.update_node(data_id, new_data)
            elif update_type == 'link':
                self.update_link(data_id, **new_data)
            elif update_type == 'relation':
                self.update_relation(data_id, **new_data)

    def add_node(self, node: Node):
        self.nodes[node.id] = node

    def add_link(self, link: Link):
        self.links[link.id] = link

    def add_relation(self, relation: Relation):
        self.relations[relation.id] = relation

    def get_node(self, node_id: int) -> Optional[Node]:
        return self.nodes.get(node_id)

    def get_link(self, link_id: int) -> Optional[Link]:
        return self.links.get(link_id)

    def get_relation(self, relation_id: int) -> Optional[Relation]:
        return self.relations.get(relation_id)

    def get_all_nodes(self) -> List[Node]:
        return list(self.nodes.values())

    def get_all_links(self) -> List[Link]:
        return list(self.links.values())

    def get_all_relations(self) -> List[Relation]:
        return list(self.relations.values())

    def find_nodes_in_rectangle(self, min_x: float, min_y: float, max_x: float, max_y: float) -> List[Node]:
        return [
            node for node in self.nodes.values()
            if min_x <= node.x <= max_x and min_y <= node.y <= max_y
        ]

    def find_links_in_rectangle(self, min_x: float, min_y: float, max_x: float, max_y: float) -> List[Link]:
        nodes_in_rect = self.find_nodes_in_rectangle(min_x, min_y, max_x, max_y)
        node_ids = {node.id for node in nodes_in_rect}
        return [
            link for link in self.links.values()
            if link.from_node in node_ids or link.to_node in node_ids
        ]

    def find_relations_in_rectangle(self, min_x: float, min_y: float, max_x: float, max_y: float) -> List[Relation]:
        nodes_in_rect = self.find_nodes_in_rectangle(min_x, min_y, max_x, max_y)
        node_ids = {node.id for node in nodes_in_rect}
        return [
            relation for relation in self.relations.values()
            if relation.node_id in node_ids
        ]

    def find_nearest_node(self, x: float, y: float) -> Optional[Node]:
        if not self.nodes:
            return None
        
        min_dist = float('inf')
        nearest_node = None
        
        for node in self.nodes.values():
            dist = math.sqrt((node.x - x) ** 2 + (node.y - y) ** 2)
            if dist < min_dist:
                min_dist = dist
                nearest_node = node
                
        return nearest_node

    def get_elements_in_rectangle(self, 
                                min_x: float, 
                                min_y: float, 
                                max_x: float, 
                                max_y: float) -> Tuple[List[Node], List[Link]]:
        nodes = []
        links = []
        
        # Get nodes within rectangle
        for node in self.nodes.values():
            if min_x <= node.x <= max_x and min_y <= node.y <= max_y:
                nodes.append(node)
                
        # Get links related to these nodes
        node_ids = {node.id for node in nodes}
        for link in self.links.values():
            if link.from_node in node_ids or link.to_node in node_ids:
                links.append(link)
                
        return nodes, links 