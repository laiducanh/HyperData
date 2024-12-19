from ui.utils import icon

def load_MenuIcon():
    """ this function will preload icons used for Menu to avoid delays """
    global icon_line, icon_bar, icon_scatter, icon_pie, icon_statistics, icon_surface, icon_function, icon_none
    icon_line = icon("line.png")
    icon_bar = icon("bar.png")
    icon_scatter = icon("scatter.png")
    icon_pie = icon("pie.png")
    icon_statistics = icon("statistics.png")
    icon_surface = icon("surface.png")
    icon_function = icon("function.png")
    icon_none = icon("delete.png")

def load_InputIcon():
    """ this function will preload icons used for Input widgets to avoid delays """
    global icon_axisbot, icon_axistop, icon_axisleft, icon_axisright, icon_open

    icon_axisbot = icon("axis-bottom.png")
    icon_axistop = icon("axis-top.png")
    icon_axisleft = icon("axis-left.png")
    icon_axisright = icon("axis-right.png")
    icon_open = icon("open.png")