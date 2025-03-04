from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt, QEvent, QPoint, QTimeLine, Signal
from PySide6.QtGui import QPaintEvent, QPainter, QMouseEvent, QDragEnterEvent, QDropEvent, QCursor
from node_editor.base.node_graphics_node import NodeGraphicsSocket, NodeGraphicsNode, NodeEditor
from node_editor.base.node_graphics_edge import NodeGraphicsEdgeBezier, NodeGraphicsEdgeDirect, NodeGraphicsEdge
from node_editor.base.node_graphics_scene import NodeGraphicsScene
from node_editor.node_node import Node
from ui.base_widgets.menu import Menu, Action
from config.settings import logger

MODE_EDGE_DRAG = True

EDGE_DRAG_START_THRESHOLD = 10
SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4
PIPELINE_IN = 5
PIPELINE_OUT = 6
CONNECTOR_IN = 7
CONNECTOR_OUT = 8

class NodeGraphicsView(QGraphicsView):
    def __init__(self, grScene:NodeGraphicsScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.initUI()
        self.initMenu()

        self.setScene(self.grScene)

        self.drag_mode = False

        self.currentScale = 1
        self._pan = False
        self._pan_start_x = 0
        self._pan_start_y = 0
        self._numScheduledScalings = 0

    def initUI(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.LosslessImageRendering | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setAcceptDrops(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
    
    def initMenu(self):
        self.menu = Menu(parent=self)
        action = Action(text="Select All", shortcut="Ctrl+A", parent=self.menu)
        action.triggered.connect(self.selectAll)
        self.menu.addAction(action)            
        action = Action(text="Zoom in", shortcut="Ctrl+Up", parent=self.menu)
        action.triggered.connect(lambda: self.scaling_time(1.2))
        self.menu.addAction(action)
        action = Action(text="Zoom out", shortcut="Ctrl+Down", parent=self.menu)
        action.triggered.connect(lambda: self.scaling_time(0.8))
        self.menu.addAction(action)
        self.menu.addSeparator()

        data_processing = Menu(text="Data Processing")
        self.menu.addMenu(data_processing)
        for text in ["Data Reader", "Data Concator", "Data Transpose", "Data Inserter",
                     "Data Combiner", "Data Merge", "Data Compare","Data Correlator",
                     "Data Locator","Data Splitter","Data Filter", "Data Holder","Data Sorter",
                     "Data Pivot","Data Unpivot","Data Stack","Data Unstack",
                     "Data Scaler","Data Normalizer","Pairwise Measurer",
                     "Nan Eliminator", "Nan Imputer", "Drop Duplicate",]:
            action = Action(text=text, parent=data_processing)
            action.triggered.connect(lambda _, text=text: self.addNode(text))
            data_processing.addAction(action)
        machine_learning = Menu(text="Machine Learning")
        self.menu.addMenu(machine_learning)
        for text in ["Classifier","Bagging-Classifier","Voting-Classifier",
                     "Regressor","Clustering","Decomposition",
                     "CV Splitter","Train/Test Splitter",
                     "Predictor","Feature Expander","Feature Selector",
                     "Label Encoder","Label Binarizer","Ordinal Encoder","One-Hot Encoder",]:
            action = Action(text=text, parent=machine_learning)
            action.triggered.connect(lambda _, text=text: self.addNode(text))
            machine_learning.addAction(action)
        deep_learning = Menu(text="Deep Learning")
        self.menu.addMenu(deep_learning)
        for text in ["Input Layer","Dense Layer","Normalization Layer","DL Model"]:
            action = Action(text=text, parent=deep_learning)
            action.triggered.connect(lambda _, text=text: self.addNode(text))
            deep_learning.addAction(action)
        visualization = Menu(text="Visualization")
        self.menu.addMenu(visualization)
        for text in ["Figure 2D", "Figure 3D","Multi-Figure"]:
            action = Action(text=text, parent=visualization)
            action.triggered.connect(lambda _, text=text: self.addNode(text))
            visualization.addAction(action)
        misc = Menu(text="Misc")
        self.menu.addMenu(misc)
        for text in ["Executor", "Looper", "Undefined Node"]:
            action = Action(text=text, parent=misc)
            action.triggered.connect(lambda _, text=text: self.addNode(text))
            misc.addAction(action)
        
    def addNode(self, node_title:str):
        node = Node(title=node_title,parent=self)
        self.grScene.addNode(node)
        node.setPos(self.last_rmb_click_scene_pos.x(), self.last_rmb_click_scene_pos.y())

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
            if isinstance(item, (Node, NodeEditor)): item.updateConnectedEdges()
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
            if not self.drag_mode and item.socket_type in [SINGLE_OUT, MULTI_OUT, PIPELINE_OUT, CONNECTOR_OUT]:
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

        self.last_rmb_click_scene_pos = self.mapToScene(event.pos())

    def rightMouseButtonRelease(self, event:QMouseEvent):
        item = self.itemAt(event.pos())
        pos = self.mapToGlobal(event.pos())
        if item:
            if isinstance(item, Node):
                item.setSelected(True)
                item.menu.exec(pos)
                
            elif isinstance(item.parentItem(), Node):
                item.parentItem().setSelected(True)
                item.parentItem().menu.exec(pos)
        else:
            self.menu.exec(pos)

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
        node = Node(title=event.mimeData().text(),parent=self)
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

        self.anim.valueChanged.connect(lambda: self.scaling_time(None))
        self.anim.finished.connect(self.anim_finished)
        self.anim.start()

    def scaling_time(self, factor=None):
        """
        Updates the current scale based on the wheel events.

        """

        if not factor: factor = 1.0 + self._numScheduledScalings / 300.0
                
        if self.currentScale*factor <= 1:
            self.currentScale *= factor
            self.scale(factor, factor)
        else: 
            factor = 1/self.currentScale
            self.scale(factor, factor)
            self.currentScale = 1
            
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

        if isinstance(item, NodeGraphicsSocket) and self.dragEdge.start_socket.socket_type == PIPELINE_OUT:
            if item.socket_type == PIPELINE_IN:
                self.dragEdge.end_socket = item
                self.dragEdge.end_socket.addEdge(self.dragEdge)
                logger.info(f'View::edgeDragEnd: assign end socket index {item.index} of node {item.node.id} to drag edge.')
                self.dragEdge.updatePositions()
                return True

        elif isinstance(item, NodeGraphicsSocket) and item.socket_type in [SINGLE_IN, MULTI_IN, CONNECTOR_IN] and item.node != self.dragEdge.start_socket.node:
            # remove edge in single in, connector in
            if item.socket_type in [SINGLE_IN, CONNECTOR_IN] and item.hasEdge(): 
                for edge in item.edges:
                    edge.remove()
                    self.grScene.removeEdge(edge) 
                    logger.info(f'View::edgeDragEnd: remove Edge for single-in socket.')
                            
            # remove edge in single out
            if self.dragEdge.start_socket.socket_type in [SINGLE_OUT]: 
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
        elif event.key() == Qt.Key.Key_Escape:
            self.deselectSelected()
        elif event.key() == Qt.Key.Key_A and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.selectAll()
        elif event.key() == Qt.Key.Key_Up and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.scaling_time(factor=1.2)
        elif event.key() == Qt.Key.Key_Down and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.scaling_time(factor=1/1.2)
        else:
            super().keyPressEvent(event)

    def selectAll(self):
        for item in self.grScene.items(): 
            item.setSelected(True)
    
    def deselectSelected(self):
        for item in self.grScene.selectedItems():
            item.setSelected(False)

    def deleteSelected(self):
        for item in self.grScene.selectedItems():
            if isinstance(item, NodeGraphicsEdge):
                self.grScene.removeEdge(item)
            elif isinstance(item, NodeGraphicsNode):
                self.grScene.removeNode(item)
                
        # also delete edges if connected node has been deleted        
        for item in self.grScene.items():
            if isinstance(item, NodeGraphicsEdge):
                if item.start_socket not in self.grScene.items() or item.end_socket not in self.grScene.items():
                    self.grScene.removeEdge(item)
    
    def paintEvent(self, event: QPaintEvent) -> None:
        self.grScene.setBackgroundColor()
        return super().paintEvent(event)