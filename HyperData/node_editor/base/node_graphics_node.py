from PyQt6.QtWidgets import QGraphicsItem, QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent, QGraphicsTextItem, QGraphicsProxyWidget, QWidget, QGraphicsPathItem
from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QPen, QFont, QBrush, QColor, QPainterPath, QPainter, QTextOption, QAction
import pandas as pd
from ui.base_widgets.menu import Menu

SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4
PIPELINE_IN = 5
PIPELINE_OUT = 6
DEBUG = False

class NodeGraphicsSocket (QGraphicsItem):
    def __init__(self, node:'NodeGraphicsNode', index=0, socket_type=SINGLE_IN, parent=None):
        super().__init__(parent)

        self.radius = 6.0
        self.outline_width = 2.5
        self._colors = [
            QColor("#FFA04D"),
            QColor("#FA6D6D"),
            QColor("#6DAFFA"),
            QColor("#6DFA8D"),
            QColor("#f0f1f2"),
            QColor("#f0f1f2"),
        ]
        self._color_background = self._colors[socket_type-1]
        self._color_outline = QColor("#FF000000")

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        """ Temporarily turn off hover events since it conflicts with mouse press in view """
        #self.setAcceptHoverEvents(True)

        self.node = node # node that socket is attached to so that we can get socket position from 'NodeGraphicsNode' class
        self.index = index
        self.edges = [] # assigns a list of edges connected to (self) socket, init with an empty list, has type of list[NodeGraphicsEdge]
        self.socket_type = socket_type
        self.hovered = False
        self.id = id(self)

        self._pen_default = QPen(self._color_outline)
        self._pen_default.setWidthF(self.outline_width)
        self._pen_hovered = QPen(self._color_outline)
        self._pen_hovered.setWidthF(self.outline_width+1)
        self._brush = QBrush(self._color_background)    
        self._text = QGraphicsTextItem(self)

        self.setTitle()
        
    def setTitle (self):
        if self.socket_type == SINGLE_IN:
            self.title = 'Single Input'
        elif self.socket_type == MULTI_IN:
            self.title = 'Multiple Inputs'
        elif self.socket_type == SINGLE_OUT:
            self.title = 'Single Output'
        elif self.socket_type == MULTI_OUT:
            self.title = 'Multiple Outputs'

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent | None) -> None:
        self._text.setPlainText(self.title)
        self.hovered = True
        self.update()
    
    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent | None) -> None:
        self._text.setPlainText('')
        self.hovered = False
        self.update()

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        # painting circle
        painter.setBrush(self._brush)
        
        if self.hovered:
            painter.setPen(self._pen_hovered)
            painter.drawEllipse(int(-self.radius), int(-self.radius), int(2 * self.radius), int(2 * self.radius))
        else:
            painter.setPen(self._pen_default)
            painter.drawEllipse(int(-self.radius), int(-self.radius), int(2 * self.radius), int(2 * self.radius))
        
    def boundingRect(self):
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )

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



class NodeGraphicsNode (QGraphicsItem):
    def __init__(self, title:str, inputs=[], outputs=[], parent=None):
        super().__init__(parent)

        self._title_color = Qt.GlobalColor.lightGray
        self._title_color_hovered = Qt.GlobalColor.white
        self._title_font = QFont("Monospace", 10, 700)
        self.title = title
        self.edge_size = 5.0
        self.title_height = 24.0
        self._padding = 4.0
        self.socket_spacing = 22
        self.width = 180
        self.height = (self.socket_spacing)*(max(len(inputs),len(outputs))) + self.title_height + 2*self._padding
        #self.content = None
        self.data_in = pd.DataFrame()
        self.data_out = pd.DataFrame()
        self.hovered = False
        self.id = id(self)
        self.content_change = False
        self.menu = Menu()

        self._color = QColor("#7F000000")
        self._color_selected = QColor("#252525")
        self._color_hovered = QColor("#FF37A6FF")

        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(2.0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(2.0)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(3.0)

        #self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_title = QBrush(QColor("#434343"))
        #self._brush_background = QBrush(QColor("#E3212121"))
        self._brush_background = QBrush(Qt.GlobalColor.white)

        self.setTitle()
        

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        self.wasMoved = False

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
        

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()     

    def setTitle(self):
        self.title_item = QGraphicsTextItem(self.title.upper(),parent=self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        #self.title_item.setPos(self._padding, 0)
        self.title_item.document().setDefaultTextOption(QTextOption(Qt.AlignmentFlag.AlignCenter))
        self.title_item.setTextWidth(self.width)
    
    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        super().hoverEnterEvent(event)
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        super().hoverLeaveEvent(event)
        self.hovered = False
        self.update()

    
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        #self.updateConnectedEdges() # already implemented in node_graphics_view class
        self.wasMoved = True
    
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if self.wasMoved:
            self.wasMoved = False
            if DEBUG: print('node moved')
        
        for socket in self.input_sockets + self.output_sockets:
            for edge in socket.edges:
                if DEBUG: print('Node', self, edge.start_socket.node)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        super().mousePressEvent(event)

        for socket in self.input_sockets:
            if DEBUG: print(socket.edges)
        for socket in self.output_sockets:
            if DEBUG: print(socket.edges)

 
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

        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.FillRule.WindingFill)
        path_title.addRoundedRect(0,0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())


        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.FillRule.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())


        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if self.hovered:
            painter.setPen(self._pen_hovered)
            painter.drawPath(path_outline.simplified())
            self.title_item.setDefaultTextColor(self._title_color_hovered)
            
        else:
            painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
            painter.drawPath(path_outline.simplified())
            self.title_item.setDefaultTextColor(self._title_color)
        
        if self.content_change:
            # update socket positions when content was enlarged
            for socket in self.output_sockets:
                socket.setPos(self.width, socket.pos().y())
            # update title position
            self.title_item.setTextWidth(self.width)
            # update edges
            self.updateConnectedEdges()

        
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


    

