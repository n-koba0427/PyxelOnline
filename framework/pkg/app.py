import pyxel
import asyncio

from .utils import *
from .pyxel_avatar import *
from .multiplay import *

import threading



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
        self.name="naoyashi"
        self.frame = 0
        self.others = {}
    
    async def _callback(self):
        result = await Transmission(self.name, self.avatar.position, self.avatar.style)
        for data in result.split("|"):
            ip, info = data.split(":")
            info = info.split(",")
            
            if not ip in self.others:
                self.others[ip] = Avatar()
            
            _name = info[0]
            _position = list(map(int, info[1:3]))
            _style = list(map(int, info[3:]))
            self.others[ip].name = _name
            self.others[ip].position = _position
            self.others[ip].style = _style
                
        
    def threaded_callback(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._callback())
    
    # process
    @avatar_editor_update
    def _update(self):
        # reflect editing results
        self.avatar.style = avatar_editor.avatar.style
        # move avatar
        self.avatar.key_move()
        self._callback()
        if self.frame%30==0:
            threading.Thread(target=self.threaded_callback).start()
        self.frame+=1
        
    # visualize
    @avatar_editor_draw
    def _draw(self):
        pyxel.cls(11)
        # draw avatar
        self.avatar.draw()
        
        for others_avatar in self.others.values():
            others_avatar.draw()