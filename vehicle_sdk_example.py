from map_sdk import MapData, Node, Link, Point
from network_sdk import NetworkQuery

class VehicleSDK:
    """
    车端SDK示例
    仅提供数据获取功能，不包含数据处理逻辑
    """
    def __init__(self):
        self.map_data = MapData()
        self.network_query = NetworkQuery(self.map_data)
    
    def get_network_data(self, position: Point, radius: float = 2000) -> tuple[list[Node], list[Link]]:
        """
        获取指定位置周围的路网数据
        
        Args:
            position: 车辆当前位置
            radius: 查询半径（米），默认2000米
            
        Returns:
            tuple[list[Node], list[Link]]: 返回范围内的节点和路段列表
        """
        return self.network_query.get_network_within_radius(position, radius)
    
    def get_nearest_node(self, position: Point) -> Node:
        """
        获取最近的节点
        
        Args:
            position: 车辆当前位置
            
        Returns:
            Node: 最近的节点
        """
        return self.map_data.find_nearest_node(position)
    
    def get_rectangle_data(self, min_x: float, min_y: float, max_x: float, max_y: float) -> tuple[list[Node], list[Link]]:
        """
        获取矩形范围内的路网数据
        
        Args:
            min_x: 矩形最小x坐标
            min_y: 矩形最小y坐标
            max_x: 矩形最大x坐标
            max_y: 矩形最大y坐标
            
        Returns:
            tuple[list[Node], list[Link]]: 返回范围内的节点和路段列表
        """
        nodes = self.map_data.find_nodes_in_rectangle(min_x, min_y, max_x, max_y)
        links = self.map_data.find_links_in_rectangle(min_x, min_y, max_x, max_y)
        return nodes, links

def main():
    # 创建SDK实例
    sdk = VehicleSDK()
    
    # 示例：获取车辆周围路网数据
    vehicle_position = Point(500, 500)
    
    # 1. 获取2km范围内的路网数据
    nodes, links = sdk.get_network_data(vehicle_position)
    print(f"获取到 {len(nodes)} 个节点和 {len(links)} 个路段")
    
    # 2. 获取最近的节点
    nearest_node = sdk.get_nearest_node(vehicle_position)
    print(f"最近的节点ID: {nearest_node.id}")
    
    # 3. 获取矩形范围内的数据
    rect_nodes, rect_links = sdk.get_rectangle_data(0, 0, 1000, 1000)
    print(f"矩形范围内有 {len(rect_nodes)} 个节点和 {len(rect_links)} 个路段")

if __name__ == "__main__":
    main() 