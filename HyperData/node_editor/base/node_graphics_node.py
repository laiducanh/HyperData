from PySide6.QtGui import QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt
from ui.base_widgets.menu import Menu
from node_editor.graphics.graphics_node import GraphicsNode
from node_editor.base.node_graphics_socket import NodeGraphicsSocket
from config.settings import logger, GLOBAL_DEBUG
from ui.utils import isDark

SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4
PIPELINE_IN = 5
PIPELINE_OUT = 6
CONNECTOR_IN = 7
CONNECTOR_OUT = 8
DEBUG = False


class NodeGraphicsNode(GraphicsNode):
    def __init__(self, title:str, inputs=[], outputs=[], parent=None):
        super().__init__(title, parent)

        
        self.content_change = False
        self.menu = Menu()

        # create socket for inputs and outputs
        self.input_sockets:list[NodeGraphicsSocket] = list() # keeps track input sockets by a list
        self.output_sockets:list[NodeGraphicsSocket] = list() # keeps track output sockets by a list

        for index, item in enumerate(inputs):
            self.addSocket(index=index,socket_type=item)
            
        for index, item in enumerate(outputs):
            self.addSocket(index=index,socket_type=item)

        # add pipeline sockets
        self.socket_pipeline_in = NodeGraphicsSocket(node=self, index=0, socket_type=PIPELINE_IN, parent=self)
        self.socket_pipeline_in.setPos(0, self.getSocketPosition(index=0, socket_type=PIPELINE_IN)[1])
        self.socket_pipeline_out = NodeGraphicsSocket(node=self, index=0, socket_type=PIPELINE_OUT, parent=self)
        self.socket_pipeline_out.setPos(self._width, self.getSocketPosition(index=0, socket_type=PIPELINE_OUT)[1])

        logger.info(f"Initialize node {self.title} {self.id}, Node.input_sockets {[i.id for i in self.input_sockets]}, "
                    f"Node.output_sockets {[i.id for i in self.output_sockets]}.")

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
        
        if self.content:
            if self._width != self.content.width() + 6*self._edge_size:
                self._width = self.content.width() + 6*self._edge_size
                self.content_change = True
            else: self.content_change = False
            self._height = self._title_height + min(self.content.sizeHint().height(), self.content.height()) + 2*self._padding
        
        if self.content_change:
            # update socket positions when content was enlarged
            for socket in self.output_sockets:
                socket.setPos(self._width, socket.pos().y())
            self.socket_pipeline_out.setPos(self._width, self.socket_pipeline_out.pos().y())
            # update title position
            self.title_item.setTextWidth(self._width)
            # update edges
            self.updateConnectedEdges()
            logger.info(f"{self.title} {self.id}: content changes, all graphics are updated accordingly.")
       
        return super().paint(painter, QStyleOptionGraphicsItem, widget)
    
    
    def getSocketPosition(self, index, socket_type):
        """ 
        This method is used to compute socket position, temporarily set socket position always on top 
        """

        x = 0 if (socket_type in (SINGLE_IN, MULTI_IN)) else self._width

        if socket_type in (SINGLE_OUT, MULTI_OUT):
            # start from bottom
            y = self._height - self._edge_size - self._padding - index * self._socket_spacing

        # start from top
        y = self._title_height + self._padding + self._edge_size + index * self._socket_spacing

        return [x, y]
    
    def addSocket(self, index, socket_type):
      
        # add data sockets
        index += 1
        socket = NodeGraphicsSocket(node=self, index=index, socket_type=socket_type, parent=self)
        socket.setPos(*self.getSocketPosition(index=index, socket_type=socket_type))
                
        if socket_type in (SINGLE_IN, MULTI_IN): self.input_sockets.append(socket)
        else: self.output_sockets.append(socket)

    def removeSocket(self, index=None, socket_type=None, socket:NodeGraphicsSocket=None):
        if index and socket_type:
            index += 1
            for _socket in self.childItems():
                if isinstance(_socket, NodeGraphicsSocket):
                    if index == _socket.index and socket_type == _socket.socket_type:
                        _socket.removeAllEdges()
                        self.scene().removeItem(socket)
                        if socket_type in (SINGLE_IN, MULTI_IN): self.input_sockets.remove(_socket)
                        else: self.output_sockets.remove(_socket)
        if socket: 
            socket.removeAllEdges()
            self.scene().removeItem(socket)
            if socket.socket_type in (SINGLE_IN, MULTI_IN): self.input_sockets.remove(socket)
            else: self.output_sockets.remove(socket)
        
    def serialize(self):
        inputs, outputs = dict(), dict()
        for socket in self.input_sockets: inputs[socket.id] = socket.serialize()
        for socket in self.output_sockets: outputs[socket.id] = socket.serialize()

        logger.info(f"Serializing node {self.title} {self.id}.")

        return {"id":self.id,
                "title":self.title,
                "pos_x":self.scenePos().x(),
                "pos_y":self.scenePos().y(),
                "input sockets":inputs,
                "output sockets":outputs,
                "color": self._brush_background.color().name(),
                "content":self.content.serialize()}
    
    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        hashmap[data['id']] = self

        self.setPos(data['pos_x'], data['pos_y'])
        self.title = data['title']
        self._brush_background = QBrush(data['color'])

        for socket_data, socket in zip(data['input sockets'].keys(), self.input_sockets):
            path = data['input sockets'][socket_data]
            socket.deserialize(path, hashmap)

        for socket_data, socket in zip(data['output sockets'].keys(), self.output_sockets):
            path = data['output sockets'][socket_data]
            socket.deserialize(path, hashmap)
       
        self.content.deserialize(data['content'])

        logger.info(f"Deserializing node {self.title} {self.id}.")
    
class NodeEditor (GraphicsNode):
    def __init__(self, title:str, socket_type, parent=None):
        super().__init__(title, parent)
        
        self.content = None

        
        self.socket = NodeGraphicsSocket(node=self, index=0, socket_type=socket_type, parent=self)
        self.socket.setPos(*self.getSocketPosition(index=0, socket_type=socket_type))
        self.socket_type = socket_type
    
    
    def updateConnectedEdges(self):
        """ This method will update the edge attached to the socket that is moved """
        for edge in self.socket.edges:
            edge.updatePositions()
       
    
    def getSocketPosition(self, index, socket_type):
        """ 
        This method is used to compute socket position, temporarily set socket position always on top 
        """

        x = 0 if (socket_type in (SINGLE_IN, MULTI_IN, CONNECTOR_IN, PIPELINE_IN)) else self.width

        if socket_type in (SINGLE_OUT, MULTI_OUT, CONNECTOR_OUT, PIPELINE_OUT):
            # start from bottom
            y = self._height - self._edge_size - self._padding - index * self._socket_spacing

        # start from top
        y = self._title_height + self._padding + self._edge_size + index * self._socket_spacing

        return [x, y]

    def setColor(self):
        
        self._color = QColor("#7F000000")
        self._color_selected = QColor("#252525")
        self._color_hovered = QColor("#FF37A6FF")

        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(2.0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(2.0)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(3.0)

        if isDark():
            self._brush_background = QBrush(QColor("#232323"))
            self._brush_title = QBrush(QColor("#444444"))
            self._title_color = Qt.GlobalColor.white
        else:
            self._brush_background = QBrush(QColor("#FF4848"))
            #self._brush_title = QBrush(QColor("#434343"))
            self._brush_title = QBrush(QColor("#E2E2E2"))
            self._title_color = Qt.GlobalColor.black

            if self.hovered:
                self._brush_background = QBrush(QColor("#FF8484"))

        