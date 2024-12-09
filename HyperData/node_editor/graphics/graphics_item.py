from node_editor.graphics.graphics_edge import EdgeItem
from node_editor.graphics.graphics_socket import SocketItem
from node_editor.graphics.graphics_node import NodeItem
from node_editor.graphics.graphics_content import ContentItem

class GraphicsEdge(EdgeItem):
    def __init__(self, start_socket: 'GraphicsSocket' = None, end_socket: 'GraphicsSocket' = None, parent=None):
        super().__init__(parent)

        self.start_socket = start_socket
        self.end_socket = end_socket

class GraphicsSocket(SocketItem):
    def __init__(self, node:'GraphicsNode', socket_type, parent=None):
        super().__init__(socket_type, parent)

        self.node = node

class GraphicsNode(NodeItem):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)

class GraphicsContent(ContentItem):
    def __init__(self, parent=None):
        super().__init__(parent)