from PyQt6.QtWidgets import QGraphicsView, QMenu
from PyQt6.QtCore import Qt, QEvent, QPoint, QTimeLine, pyqtSignal
from PyQt6.QtGui import QPainter, QMouseEvent, QDragEnterEvent, QDropEvent
from node_editor.base.node_graphics_node import NodeGraphicsSocket, NodeGraphicsNode
from node_editor.base.node_graphics_edge import NodeGraphicsEdgeBezier, NodeGraphicsEdgeDirect, NodeGraphicsEdge
from node_editor.base.node_graphics_scene import NodeGraphicsScene
from node_editor.node_node import Node
from ui.base_widgets.menu import Menu
from config.settings import logger

MODE_EDGE_DRAG = True

EDGE_DRAG_START_THRESHOLD = 10
SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4
PIPELINE_IN = 5
PIPELINE_OUT = 6

class NodeGraphicsView(QGraphicsView):
    def __init__(self, grScene:NodeGraphicsScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.parent = parent
        self.initUI()

        self.setScene(self.grScene)

        self.drag_mode = False

        self.currentScale = 1
        self._pan = False
        self._pan_start_x = 0
        self._pan_start_y = 0
        self._numScheduledScalings = 0
        self.lastMousePos = QPoint()


    def initUI(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.LosslessImageRendering | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setAcceptDrops(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)
        
    def mouseMoveEvent(self, event):
        self.mouse_position = self.mapToScene(event.pos())
        if self.drag_mode:
            pos = self.mapToScene(event.pos())
            self.dragEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.update()
            
        for item in self.grScene.selectedItems():
            if isinstance(item, Node): item.updateConnectedEdges()
            pass
                

        super().mouseMoveEvent(event)

    def middleMouseButtonPress(self, event: QMouseEvent):
        releaseEvent = QMouseEvent(QEvent.Type.MouseButtonRelease, event.pos().toPointF(), event.globalPosition(),
                                   Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.pos().toPointF(), event.globalPosition(),
                                Qt.MouseButton.LeftButton, event.buttons() | Qt.MouseButton.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event:QMouseEvent):
        fakeEvent = QMouseEvent(event.type(), event.pos().toPointF(), event.globalPosition(),
                                Qt.MouseButton.LeftButton, event.buttons() & ~Qt.MouseButton.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)


    def leftMouseButtonPress(self, event:QMouseEvent):
        super().mousePressEvent(event)
        
        # get item which we clicked on
        item = self.itemAt(event.pos())

        # we store the position of last LMB click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        # logic
        if type(item) is NodeGraphicsSocket:
            if not self.drag_mode and item.socket_type in [SINGLE_OUT, MULTI_OUT, PIPELINE_OUT]:
                self.drag_mode = True
                self.edgeDragStart(item)
                return

        if self.drag_mode:
            res = self.edgeDragEnd(item)
            if res: return

        


    def leftMouseButtonRelease(self, event:QMouseEvent):
        super().mouseReleaseEvent(event)

        # get item which we release mouse button on
        item = self.itemAt(event.pos())

        # logic
        if self.drag_mode:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res: return


        


    def rightMouseButtonPress(self, event:QMouseEvent):
        super().mousePressEvent(event)

    def rightMouseButtonRelease(self, event:QMouseEvent):
        item = self.itemAt(event.pos())
        pos = self.mapToGlobal(event.pos())
        if item != None:
            if isinstance(item, Node):
                item.menu.exec(pos)
            elif isinstance(item.parentItem(), Node):
                item.parentItem().menu.exec(pos)
            
        else:
            menu = Menu(parent=self)
            menu.exec(pos)
        super().mouseReleaseEvent(event)

    def dragEnterEvent(self, event:QDragEnterEvent):
        """
        This method is called when a drag and drop event enters the view. It checks if the mime data has text
        and accepts or ignores the event accordingly.
        """
        if event.mimeData().text():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """
        This method is called when a drag and drop event is dropped onto the view. It retrieves the name of the dropped node
        from the mime data and add the corresponding node.
        """
        node = Node(title=event.mimeData().text(),parent=self.parent)
        self.grScene.addNode(node)
        mouse_position = event.position()
        scene_position = self.grScene.views()[0].mapToScene(mouse_position.toPoint())
        node.setPos(scene_position.x(), scene_position.y())

    def wheelEvent(self, event):
        """
        Handles the wheel events, e.g. zoom in/out.

        :param event: Wheel event.
        """
        # sometimes you can triger the wheen when panning so we disable when panning
        if self._pan:
            return

        num_degrees = event.angleDelta() / 8.0
        num_steps = num_degrees.y() / 5.0
        self._numScheduledScalings += num_steps

        # If the user moved the wheel another direction, we reset previously scheduled scalings
        if self._numScheduledScalings * num_steps < 0:
            self._numScheduledScalings = num_steps

        self.anim = QTimeLine(350)
        self.anim.setUpdateInterval(20)

        self.anim.valueChanged.connect(self.scaling_time)
        self.anim.finished.connect(self.anim_finished)
        self.anim.start()

    def scaling_time(self, x):
        """
        Updates the current scale based on the wheel events.

        :param x: The value of the current time.
        """
        factor = 1.0 + self._numScheduledScalings / 300.0

        self.currentScale *= factor

        self.scale(factor, factor)

    def anim_finished(self):
        """
        Called when the zoom animation is finished.
        """
        if self._numScheduledScalings > 0:
            self._numScheduledScalings -= 1
        else:
            self._numScheduledScalings += 1
    
    def edgeDragStart(self, item:NodeGraphicsSocket):

        logger.info('View::edgeDragStart: start dragging edge.')
        logger.info(f'View::edgeDragStart: assign start socket to socket index {item.index} of node {item.node.id}.')
        
        #self.last_start_socket = item
        self.dragEdge = NodeGraphicsEdgeBezier(start_socket=item, end_socket=None)
        #item.addEdge(self.dragEdge)
        self.dragEdge.updatePositions()
        self.grScene.addEdge(self.dragEdge)

    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.drag_mode = False
        if type(item) is NodeGraphicsSocket and self.dragEdge.start_socket.socket_type == PIPELINE_OUT:
            if item.socket_type == PIPELINE_IN:
                self.dragEdge.end_socket = item
                self.dragEdge.end_socket.addEdge(self.dragEdge)
                self.dragEdge.setColor(Qt.GlobalColor.green)
                logger.info(f'View::edgeDragEnd: assign end socket index {item.index} of node {item.node.id} to drag edge.')
                self.dragEdge.updatePositions()
                return True

        elif type(item) is NodeGraphicsSocket and item.socket_type in [SINGLE_IN, MULTI_IN] and item.node != self.dragEdge.start_socket.node:
            if item.socket_type == SINGLE_IN and item.hasEdge(): 
                for edge in item.edges:
                    edge.remove()
                    self.grScene.removeEdge(edge) 
                    logger.info(f'View::edgeDragEnd: remove Edge for single-in socket.')
                            
                        
            if self.dragEdge.start_socket.socket_type == SINGLE_OUT: 
                for edge in self.dragEdge.start_socket.edges:
                    if edge != self.dragEdge:
                        edge.remove()
                        self.grScene.removeEdge(edge)
                        logger.info(f'View::edgeDragEnd: remove Edge for single-out socket')
                        
            self.dragEdge.end_socket = item
            self.dragEdge.end_socket.addEdge(self.dragEdge)

            logger.info(f'View::edgeDragEnd: assign end socket index {item.index} of node {item.node.id} to drag edge.')
            self.dragEdge.updatePositions()
            return True

        logger.info('View::edgeDragEnd: finish dragging edge.')
        self.grScene.removeEdge(self.dragEdge)
        self.dragEdge = None
        logger.info('View::edgeDragEnd: everything done.')


        return False

        
    def distanceBetweenClickAndReleaseIsOff(self, event:QMouseEvent):
        """ measures if we are far enough from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()) > edge_drag_threshold_sq

    def keyPressEvent(self, event):
        logger.info(f"View::keyPressEvent: {event.key()} pressed.")

        if event.key() == Qt.Key.Key_Delete:
            self.deleteSelected()
        elif event.key() == Qt.Key.Key_A and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            for item in self.grScene.items(): item.setSelected(True)

        else:
            super().keyPressEvent(event)


    def deleteSelected(self):
        for item in self.grScene.selectedItems():
            if isinstance(item, NodeGraphicsEdge):
                self.grScene.removeEdge(item)
                item.remove()
            elif isinstance(item, NodeGraphicsNode):
                self.grScene.removeNode(item)
                
        # also delete edges if connected node has been deleted        
        for item in self.grScene.items():
            if isinstance(item, NodeGraphicsEdge):
                if item.start_socket not in self.grScene.items() or item.end_socket not in self.grScene.items():
                    self.grScene.removeEdge(item)
                    item.remove()

