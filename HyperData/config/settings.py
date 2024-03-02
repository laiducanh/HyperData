import string, itertools, matplotlib

# list_name is replaced by column_labels
list_name =list(string.ascii_lowercase)
for j in [''.join(i) for i in itertools.product(string.ascii_lowercase, repeat = 2)]:
    list_name.append(j) # can handle maximum of 702 columns

cmap_map = {
        'Perceptually Uniform Sequential':['viridis', 'plasma', 'inferno', 'magma', 'cividis'],
        'Sequential':['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                      'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                      'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'],
        'Sequential (2)':['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone',
                      'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
                      'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper'],
        'Diverging':['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                      'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic'],
        'Cyclic':['twilight', 'twilight_shifted', 'hsv'],
        'Qualitative': ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2',
                      'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
                      'tab20c'],
        'Miscellaneous':['flag', 'prism', 'ocean', 'gist_earth', 'terrain',
                      'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
                      'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
                      'turbo', 'nipy_spectral', 'gist_ncar'],}

from matplotlib import font_manager
font_lib = font_manager.get_font_names()
font_lib.append('sans-serif')

linestyle_lib = {'-': 'Solid',
              '--': 'Dashed',
              '-.': 'DashDot',
              ':': 'Dotted',
              'None': 'None',
              }

marker_lib = {'.': 'point', ',': 'pixel', 'o': 'circle', 'v': 'triangle down', '^': 'triangle up', '<': 'triangle left',
              '>': 'triangle right', '1': 'tri down', '2': 'tri up', '3': 'tri left', '4': 'tri right', '8': 'octagon', 
              's': 'square', 'p': 'pentagon', '*': 'star', 'h': 'hexagon1', 'H': 'hexagon2', '+': 'plus', 'x': 'x', 
              'D': 'diamond', 'd': 'thin_diamond', '|': 'vline', '_': 'hline', 'P': 'plus filled', 'X': 'x filled', 
              0: 'tickleft', 1: 'tickright', 2: 'tickup', 3: 'tickdown', 4: 'caretleft', 5: 'caretright', 6: 'caretup', 
              7: 'caretdown', 8: 'caretleftbase', 9: 'caretrightbase', 10: 'caretupbase', 11: 'caretdownbase', 
              'None': 'none'}

hatch_lib = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']

model_dict = {'model 1':{'algorithm':{'algorithm':'none',},'X train':'',"Y train":'','X validate':'','Y validate':'','result':'',
                         'test option':'percentage split','k-fold':5,'train repeat':1,'percentage split':0.2,}}


matplotlib.rcParams['font.family'] = 'DejaVu Sans'

#seaborn.set_palette(palette='bright',n_colors=20)    
color_lib = matplotlib.rcParams["axes.prop_cycle"].by_key()["color"]

if matplotlib.rcParams['legend.fancybox']:
        style = 'round'
else:
        style = 'square'
