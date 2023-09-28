from dataclasses import dataclass
import pyxel
from typing import Callable

@dataclass
class Character:
    # position
    position_x:int = 0
    position_y:int = 0
    # direction {0:front, 1:back, 2:right, 3:left}
    direction:int = 0
    # state {1:stop, 0~2:move}
    state:int = 1
    
    # parameters
    # movement 
    speed:int = 1
    motion_interval:int = 8//speed
    
    @property
    def position(self) -> list:
        return self.position_x, self.position_y
    @position.setter
    def position(self, _position:list):
        self.position_x, self.position_y = _position
        
    @property
    def _next_state(self) -> int:
        if not hasattr(self, "_next_state_counter"):
            self._next_state_counter = -1
        self._next_state_counter += 1
        
        count = self._next_state_counter
        if count%self.motion_interval == 0:
            if (count//self.motion_interval)%4 == 0:
                return 0
            if (count//self.motion_interval)%2 == 0:
                return 2
            return 1
        return self.state
    
    def move(self, direction, _change_position=True) -> None:
        self.direction = direction
        self.state = self._next_state
        if _change_position:
            if direction == 0:
                self.position_y += self.speed
            if direction == 1:
                self.position_y -= self.speed
            if direction == 2:
                self.position_x += self.speed
            if direction == 3:
                self.position_x -= self.speed

@dataclass
class Avatar(Character):
    # move_keys (front, back, right, left)
    move_keys:tuple = (
        pyxel.KEY_S,
        pyxel.KEY_W,
        pyxel.KEY_D,
        pyxel.KEY_A,
    )
    
    @property
    def style(self) -> tuple:
        return self.head, self.head_color, self.body_color
    @style.setter
    def style(self, _style:tuple):
        self.head, self.head_color, self.body_color = _style
    
    def __init__(
            self,
            head:int=0,
            head_color:int=1,
            body_color:int=1,
            draw_parts:tuple=(True,True)
        ):
        self._draw_head, self._draw_body = draw_parts
        self.head, self.head_color, self.body_color = head, head_color, body_color
    
    def key_move(self, _change_position=True) -> dict:
        if pyxel.btn(pyxel.KEY_SHIFT):
            self.speed = 1.5
        else:
            self.speed = 1
        for direction, key in enumerate(self.move_keys):
            if pyxel.btn(key):
                self.move(direction, _change_position)
                return {"move":True, "position":self.position}
        self.state = 1
        self._next_state_counter = -1
        return {"move":False, "position":self.position}
    
    def draw(self) -> None:
        # head
        if self._draw_head:
            pyxel.blt(
                x=self.position_x,
                y=self.position_y+((self.state-1)%2),
                img=0,
                u=self.head_color%16*16,
                v=(self.head%4*32)+(8*self.direction),
                w=16,
                h=8,
                colkey=11
            )
        # body
        if self._draw_body:
            pyxel.blt(
                x=self.position_x,
                y=self.position_y+8,
                img=0,
                u=(self.body_color%16%5*48)+16*(self.state),
                v=128+(self.body_color%16//5*32)+(8*self.direction),
                w=16,
                h=8,
                colkey=11
            )

@dataclass
class Editor:
    flag:bool = False
    process_pause:bool = True
    trigger_key:int = pyxel.KEY_E
    
    @property
    def position(self) -> list:
        return self._position
    @position.setter
    def position(self, _position) -> None:
        self._position = _position
        self.x, self.y = _position
        self.avatar.position = self._justification((16,16))
    
    def __init__(self, _position:list=(0,0)) -> None:
        self.avatar = Avatar()
        self.position = _position
        
    def _justification(self, parameter:tuple) -> list:
        return self.x+parameter[0], self.y+parameter[1]
avatar_editor = Editor()


_head_sample_1 = Avatar(
    draw_parts=(True,False)
)
_head_sample_2 = Avatar(
    draw_parts=(True,False)
)
_body_sample = Avatar(
    draw_parts=(False,True)
)

def _collision_detection(p1:list, p2:list) -> bool:
    x1, y1 = avatar_editor._justification(p1)
    x2, y2 = avatar_editor._justification(p2)
    if x1 <= pyxel.mouse_x <= x2:
        if y1 <= pyxel.mouse_y <= y2:
            return True
    return False

def _button_manager() -> bool:
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        # head type button
        if _collision_detection((65,17), (79,31)):
            _head_sample_1.head+=1
            avatar_editor.avatar.head = _head_sample_1.head
            _head_sample_2.head = _head_sample_1.head
            return True
        # hair type button
        if _collision_detection((17,65), (31,79)):
            avatar_editor.avatar.head_color = _head_sample_2.head_color
            return True
        # clothes type button
        if _collision_detection((17,81), (31,95)):
            avatar_editor.avatar.body_color = _body_sample.body_color
            return True
        # color buttons
        for yi, y in enumerate(range(8,12)):
            for xi, x in enumerate(range(6,10)):
                if _collision_detection((x*8,y*8), ((x+1)*8,(y+1)*8)):
                    color = yi*4+xi
                    _head_sample_2.head_color = color
                    _body_sample.body_color = color
                    return True
        return False

def _editor_process():
    # place sample
    _head_sample_1.position = avatar_editor._justification((64,19))
    _head_sample_2.position = avatar_editor._justification((16,67))
    _body_sample.position = avatar_editor._justification((16,76))
    # move sample
    avatar_editor.avatar.key_move(False)
    # _head_sample_1.key_move(False)
    # _head_sample_2.key_move(False)
    # _body_sample.key_move(False)
    # listen click events
    _button_manager()
    # modify sample
    
    
def _editor_draw():
    # draw background
    pyxel.bltm(avatar_editor.x,avatar_editor.y,0,0,0,16*6,16*7)
    # draw sample
    avatar_editor.avatar.draw()
    _head_sample_1.draw()
    _head_sample_2.draw()
    _body_sample.draw()
    

def avatar_editor_update(update:Callable):
    def wrapper(self, *args, **kwargs) -> None:
        # trigger
        if pyxel.btnp(avatar_editor.trigger_key):
                avatar_editor.flag = not avatar_editor.flag
        # editor's process
        if avatar_editor.flag:
            _editor_process()
            if not avatar_editor.process_pause:
                update(self,*args, **kwargs)
        # user's process
        else:
            update(self,*args, **kwargs)
    return wrapper

def avatar_editor_draw(draw:Callable):
    def wrapper(self, *args, **kwargs) -> None:
        pyxel.cls(11)
        # user's draw
        draw(self, *args, **kwargs)
        # editor's draw
        if avatar_editor.flag:
            _editor_draw()
    return wrapper