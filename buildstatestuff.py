import colors
import utils
from objects import GameObject, Dragable
from constants import Constants
constants = Constants()

IMAGE_LOOKUP = {
    constants.CHOCOLATE_TOPPING:"chocolatechip_bin",
    constants.CHERRY_TOPPING:"cherry_bin",
    constants.RAZZBERRY_TOPPING:"razzberry_bin",
    constants.STRAWBERRY_TOPPING:"strawberry_bin",
    constants.BANANA_TOPPING:"banana_bin",
    constants.PEPPERMINT_TOPPING:"peppermint_bin",
    constants.BUTTER_TOPPING:"butter_bin",
    constants.BACON_TOPPING:"bacon_bin",
}

class ToppingBin(GameObject):
    def __init__(self,x,y,topping_name):
        super().__init__("ToppingBin",image=utils.load_image(IMAGE_LOOKUP[topping_name]), x=x,y=y,width=constants.TOPPING_BIN_WIDTH,height=constants.TOPPING_BIN_HEIGHT)
        self.topping_name = topping_name

    def get_topping(self):
        return Topping(self.x + self.width // 2 - constants.TOPPING_SIZE//2, self.y + self.height // 2 - constants.TOPPING_SIZE//2, self.topping_name)

class Topping(GameObject,Dragable):
    def __init__(self,x,y,topping_name):
        super().__init__("Topping",image=utils.load_image(topping_name), x=x,y=y,width=constants.TOPPING_SIZE,height=constants.TOPPING_SIZE)
        self.topping_name = topping_name
