import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class DraggableResizableRectangle:
    def __init__(self, rect:Rectangle):

        self.rect = rect
        self.press = None
        self.resizing = False

        x, y = rect.get_x(), rect.get_y()
        w, h = rect.get_width(), rect.get_height()
        # Create corner handle (bottom-right for this example)
        self.handle_size = 0.01
        self.handle_botleft = Rectangle(
            (x-self.handle_size/2, y-self.handle_size/2),
            self.handle_size, self.handle_size, facecolor='red',
            transform=rect.figure.transFigure
        )
        rect.figure.add_artist(self.handle_botleft)

        self.cidpress = self.rect.figure.canvas.mpl_connect('button_press_event', lambda e: self.on_press(e))
        self.cidrelease = self.rect.figure.canvas.mpl_connect('button_release_event', lambda e: self.on_release(e))
        self.cidmotion = self.rect.figure.canvas.mpl_connect('motion_notify_event', lambda e: self.on_motion(e))

    def on_press(self, event):

        # Check if handle is clicked for resizing
        contains_handle, _ = self.handle_botleft.contains(event)
        if contains_handle:
            x0, y0 = self.rect.get_xy()
            w0, h0 = self.rect.get_width(), self.rect.get_height()
            self.press = (x0, y0, w0, h0, event.x, event.y)
            self.resizing = True
            print('dpwoin', self.press)
            return

        # Check if rectangle is clicked for dragging
        contains_rect, _ = self.rect.contains(event)
        if contains_rect:
            x0, y0 = self.rect.get_xy()
            self.press = (x0, y0, event.xdata, event.ydata)
            self.resizing = False

    def on_motion(self, event):
        if self.press is None:
            return

        if self.resizing:
            x0, y0, w0, h0, xpress, ypress = self.press
            new_w = max(0.1, w0 + (event.xdata - xpress))
            new_h = max(0.1, h0 + (event.ydata - ypress))
            self.rect.set_width(new_w)
            self.rect.set_height(new_h)
            self.rect.set_xy((event.xdata - self.handle_size/2, event.ydata - self.handle_size/2))
            
        else:
            x0, y0, xpress, ypress = self.press
            dx = event.xdata - xpress
            dy = event.ydata - ypress
            self.rect.set_x(x0 + dx)
            self.rect.set_y(y0 + dy)
            # Move handle along
            new_w = self.rect.get_width()
            new_h = self.rect.get_height()
            self.handle_botleft.set_xy((x0 + dx + new_w - self.handle_size/2, y0 + dy + new_h - self.handle_size/2))

        self.rect.figure.canvas.draw()

    def on_release(self, event):
        self.press = None
        self.resizing = False
        self.rect.figure.canvas.draw()

