from objects import GameObject
import colors
import utils
from constants import Constants
from objectnames import ObjectIds
objectids = ObjectIds()
constants = Constants()

class Button(GameObject):
    def __init__(self,name,x,y,width,height,color=colors.red):
        super().__init__(name,x=x,y=y,width=width,height=height,color=color)

    def draw(self):
        super().draw()
        w, h = utils.get_font_size(self.name)
        utils.draw_text(self.name,self.x + self.width//2 - w//2 ,self.y + self.height//2 - h//2,color=colors.black)

class StartGameButton(Button):
    def __init__(self,x,y,width,height):
        super().__init__(name,x=x,y=y,width=width,height=height,color=colors.red)

class OrderButton(Button):
    def __init__(self,x,y,width,height):
        super().__init__(objectids.ORDERBUTTON,x=x,y=y,width=width,height=height,color=colors.red)

class CookButton(Button):
    def __init__(self,x,y,width,height):
        super().__init__(objectids.COOKBUTTON,x=x,y=y,width=width,height=height,color=colors.red)

class BuildButton(Button):
    def __init__(self,x,y,width,height):
        super().__init__(objectids.BUILDBUTTON,x=x,y=y,width=width,height=height,color=colors.red)

class SidesButton(Button):
    def __init__(self,x,y,width,height):
        super().__init__(objectids.SIDESBUTTON,x=x,y=y,width=width,height=height,color=colors.red)


class TakeOrderButton(Button):
    def __init__(self,x,y,width,height):
        super().__init__(objectids.TAKEORDERBUTTON,x=x,y=y,width=width,height=height,color=colors.red)

class SubmitOrderButton(Button):
    def __init__(self,x,y,width,height):
        super().__init__(objectids.SUBMITORDERBUTTON,x=x,y=y,width=width,height=height,color=colors.red)

class TossWaffleButton(Button):
    def __init__(self,x,y,width,height):
        super().__init__(objectids.TOSSWAFFLEBUTTON,x=x,y=y,width=width,height=height,color=colors.red)

class JudgeOkButton(Button):
    def __init__(self,x,y,width,height):
        super().__init__(objectids.JUDGEOKBUTTON,x=x,y=y,width=width,height=height,color=colors.red)
