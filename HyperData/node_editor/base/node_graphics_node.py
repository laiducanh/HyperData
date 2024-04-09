from PyQt6.QtWidgets import QGraphicsItem, QGraphicsSceneHoverEvent, QGraphicsProxyWidget, QWidget
from PyQt6.QtGui import QPainter
from ui.base_widgets.menu import Menu
from node_editor.graphics.graphics_node import GraphicsNode
from node_editor.graphics.graphics_socket import GraphicsSocket

SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4
PIPELINE_IN = 5
PIPELINE_OUT = 6
DEBUG = False

class NodeGraphicsSocket (GraphicsSocket):
    def __init__(self, node:'NodeGraphicsNode', index=0, socket_type=SINGLE_IN, data=None, parent=None):
        super().__init__(socket_type, parent)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setAcceptHoverEvents(True)

        self.node = node # node that socket is attached to so that we can get socket position from 'NodeGraphicsNode' class
        self.index = index
        self.edges = [] # assigns a list of edges connected to (self) socket, init with an empty list, has type of list[NodeGraphicsEdge]
        self.socket_data = data

        self.setTitle()
        
    def setTitle (self, title=None):
        if title == None:
            if self.socket_type == SINGLE_IN:
                self.title = 'Single Input'
            elif self.socket_type == MULTI_IN:
                self.title = 'Multiple Inputs'
            elif self.socket_type == SINGLE_OUT:
                self.title = 'Single Output'
            elif self.socket_type == MULTI_OUT:
                self.title = 'Multiple Outputs'
            elif self.socket_type in [PIPELINE_IN, PIPELINE_OUT]:
                self.title = "Pipeline"
        else:
            self.title = title
        
        self._text.setPlainText(self.title)
        self._text.setPos(16,-13)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent | None) -> None:
        self._text.show()
        self.node.content.hide()
        self.hovered = True
        self.update()
    
    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent | None) -> None:
        self._text.hide()
        self.node.content.show()
        self.hovered = False
        self.update()

    def getSocketPosition(self):
        """ This method use getSocketPosition method in NodeGraphicsNode to calculate the position of socket for drawing edges """
        """ return a list contains x, y """
        pos = self.node.getSocketPosition(self.index, self.socket_type)
        return pos
    
    def addEdge(self, edge):   
        self.edges.append(edge)
        if DEBUG: print('Add edge', edge, 'from node', edge.start_socket.node, 'to node', edge.end_socket.node)
        if DEBUG: print(self.edges)
        if self.socket_type in [SINGLE_IN, MULTI_IN]: edge.end_socket.node.content.eval()
          
    def removeEdge(self, edge):
        if edge in self.edges: 
            self.edges.remove(edge)
            if self.socket_type in [SINGLE_IN, MULTI_IN]: edge.end_socket.node.content.eval()

        else: print("Socket::removeEdge", "wanna remove edge", edge, "from self.edges but it's not in the list!")

    def removeAllEdges(self):
        raise NotImplemented("This method might be used in future")
        self.edges = []

    def hasEdge(self):
        """ return True if there is at least one edge attached to the socket """
        return self.edges is not []    
    
    def serialize(self):
        return {"id":self.id,
                "index":self.index,
                "socket_type":self.socket_type}

    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        hashmap[data['id']] = self
        return True



class NodeGraphicsNode (GraphicsNode):
    def __init__(self, title:str, inputs=[], outputs=[], parent=None):
        super().__init__(title, parent)

        #self.content = None
        self.content_change = False
        self.content = None
        self.menu = Menu()

        # create socket for inputs and outputs
        self.input_sockets = [] # keeps track input sockets by a list
        self.input_sockets: list[NodeGraphicsSocket]
        self.output_sockets = [] # keeps track output sockets by a list
        self.output_sockets: list[NodeGraphicsSocket]

        for index, item in enumerate(inputs):
            self.addSocket(index=index,socket_type=item)
            
        for index, item in enumerate(outputs):
            self.addSocket(index=index,socket_type=item)

        # add pipeline sockets
        self.socket_pipeline_in = NodeGraphicsSocket(node=self, index=0, socket_type=PIPELINE_IN, parent=self)
        self.socket_pipeline_in.setPos(0, self.getSocketPosition(index=0, socket_type=PIPELINE_IN)[1])
        self.socket_pipeline_out = NodeGraphicsSocket(node=self, index=0, socket_type=PIPELINE_OUT, parent=self)
        self.socket_pipeline_out.setPos(self.width, self.getSocketPosition(index=0, socket_type=PIPELINE_OUT)[1])

    def updateConnectedEdges(self):
        """ This method will update the edge attached to the socket that is moved """
        for socket in self.input_sockets + self.output_sockets:
            for edge in socket.edges:
                edge.updatePositions()
        for edge in self.socket_pipeline_in.edges:
            edge.updatePositions()
        for edge in self.socket_pipeline_out.edges:
            edge.updatePositions()


    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        
        if self.content != None:
            if self.width != self.content.width() + 6*self.edge_size:
                self.width = self.content.width() + 6*self.edge_size
                self.content_change = True
            else: self.content_change = False
            self.height = self.title_height + min(self.content.sizeHint().height(), self.content.height()) + 2*self._padding
        
        if self.content_change:
            # update socket positions when content was enlarged
            for socket in self.output_sockets:
                socket.setPos(self.width, socket.pos().y())
            # update title position
            self.title_item.setTextWidth(self.width)
            # update edges
            self.updateConnectedEdges()
       
        return super().paint(painter, QStyleOptionGraphicsItem, widget)
        
    def set_Content(self, content:QWidget):
        self.content = content
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(int(self.edge_size)+10, int(self.title_height + self.edge_size),
                                 int(self.width - 2*self.edge_size-20), int(self.height - 2*self.edge_size-self.title_height))
        self.grContent.setWidget(content)
        self.height = max(self.height, self.title_height + self.content.height() + 2*self._padding)

    def getSocketPosition(self, index, socket_type):
        """ 
        This method is used to compute socket position, temporarily set socket position always on top 
        """

        x = 0 if (socket_type in (SINGLE_IN, MULTI_IN)) else self.width

        if socket_type in (SINGLE_OUT, MULTI_OUT):
            # start from bottom
            y = self.height - self.edge_size - self._padding - index * self.socket_spacing

        # start from top
        y = self.title_height + self._padding + self.edge_size + index * self.socket_spacing

        return [x, y]
    
    def addSocket (self, index, socket_type):

        # add data sockets
        index += 1
        socket = NodeGraphicsSocket(node=self, index=index, socket_type=socket_type, parent=self)
        socket.setPos(*self.getSocketPosition(index=index, socket_type=socket_type))
        if DEBUG: print("Input Socket",socket, "-- creating with", index, "for node", self)
        
        if socket_type in (SINGLE_IN, MULTI_IN): self.input_sockets.append(socket)
        else: self.output_sockets.append(socket)

        
    def serialize(self):
        inputs, outputs = dict(), dict()
        for socket in self.input_sockets: inputs[socket.id] = socket.serialize()
        for socket in self.output_sockets: outputs[socket.id] = socket.serialize()
        return {"id":self.id,
                "title":self.title,
                "pos_x":self.scenePos().x(),
                "pos_y":self.scenePos().y(),
                "inputs":inputs,
                "outputs":outputs,
                "content":self.content.serialize()}
    
    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        hashmap[data['id']] = self

        self.setPos(data['pos_x'], data['pos_y'])
        self.title = data['title']

        #data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000 )
        #data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000 )

        self.input_sockets = []
        for socket_data in data['inputs'].keys():
            path = data['inputs'][socket_data]
            new_socket = NodeGraphicsSocket(node=self, index=path['index'], socket_type=path['socket_type'],parent=self)
            new_socket.setPos(*self.getSocketPosition(index=path['index'], socket_type=path['socket_type']))
            new_socket.deserialize(path, hashmap)
            self.input_sockets.append(new_socket)

        self.output_sockets = []
        for socket_data in data['outputs'].keys():
            path = data['outputs'][socket_data]
            new_socket = NodeGraphicsSocket(node=self, index=path['index'], socket_type=path['socket_type'],parent=self)
            new_socket.setPos(*self.getSocketPosition(index=path['index'], socket_type=path['socket_type']))
            new_socket.deserialize(path, hashmap)
            self.output_sockets.append(new_socket)


        return True


    

