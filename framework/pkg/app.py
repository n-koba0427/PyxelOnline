import pyxel
from .utils import *
from .pyxel_avatar import *

class Params:
    WINDOW_SIZE = (8*12,8*14)
    SOURCE = get_data_path("data/img.pyxres")

class App:
    def __init__(self, params:Params) -> None:
        # initialize window
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = params.WINDOW_SIZE
        pyxel.init(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        pyxel.mouse(True)
        
        # load data
        pyxel.load(params.SOURCE)
        
        # initialize variables
        self._reset(params)
        
        # run app
        pyxel.run(self._update, self._draw)
    
    # initialize variables
    def _reset(self, params:Params):
        self.params = params
        # initialize avatar
        self.avatar = Avatar()
    
    # process
    @avatar_editor_update
    def _update(self):
        # reflect editing results
        self.avatar.style = avatar_editor.avatar.style
        # move avatar
        self.avatar.key_move()
      
    # visualize
    @avatar_editor_draw
    def _draw(self):
        pyxel.cls(11)
        # draw avatar
        self.avatar.draw()