import numpy as np
import colors
import utils
from objects import GameObject, Dragable
from constants import Constants
constants = Constants()

IMAGE_LOOKUP = {
    constants.BANANA_BATTER : "waffle_banana_big",
    constants.BLUEBERRY_BATTER : "waffle_blueberry_big",
    constants.BUTTER_BATTER : "waffle_butter_big",
    constants.CHERRY_BATTER : "waffle_cherry_big",
    constants.CHOCOLATE_BATTER : "waffle_chocolate_big",
    constants.PUMPKIN_BATTER : "waffle_pumpkin_big",
    constants.RAINBOW_BATTER : "waffle_rainbow_big",
}
IMAGE_SIDE_LOOKUP = {
    constants.BANANA_BATTER : "waffle_banana_side",
    constants.BLUEBERRY_BATTER : "waffle_blueberry_side",
    constants.BUTTER_BATTER : "waffle_butter_side",
    constants.CHERRY_BATTER : "waffle_cherry_side",
    constants.CHOCOLATE_BATTER : "waffle_chocolate_side",
    constants.PUMPKIN_BATTER : "waffle_pumpkin_side",
    constants.RAINBOW_BATTER : "waffle_rainbow_side",
}

class WaffleSmall:
    def __init__(self, cook_time,batter_type):
        self.cook_time = cook_time
        self.batter_type = batter_type
        self.image = utils.load_image(IMAGE_SIDE_LOOKUP[batter_type])[0]

class WaffleStack(GameObject):
    def __init__(self,x,y):
        super().__init__(name="WaffleStack",image=utils.load_image("plate"),x=x,y=y,width=200,height=80,color=colors.blue)
        self.waffle_stack = list()

    def add_waffle(self, waffle):
        self.waffle_stack.append(waffle)

    def remove_waffle(self):
        if len(self.waffle_stack) > 0:
            return self.waffle_stack.pop(0)
        return None

    def draw(self):
        super().draw()
        for i in range(len(self.waffle_stack)):
            utils.draw_image(self.waffle_stack[i].image,self.x+25,self.y+20 - i*12.5)

    def get_waffle_stack(self):
        return self.waffle_stack

    def set_waffle_stack(self, stack):
        self.waffle_stack = stack

class WaffleEditor(GameObject):
    def __init__(self,x,y):
        super().__init__(name="WaffleEditor",image=utils.load_image("bigplate"),x=x,y=y,width=constants.WAFFLE_EDITOR_WIDTH,height=constants.WAFFLE_EDITOR_HEIGHT)
        self.waffle = None
        self.toppings = list()

    def has_waffle(self):
        return self.waffle is not None

    def set_waffle(self, waffle):
        waffle.x = self.x + (self.width-waffle.width)/2
        waffle.y = self.y + (self.height-waffle.height)/2
        self.waffle = waffle

    def norm_transform(self, topping):
        t_center= np.array(topping.center())
        my_center= np.array(self.center())
        radius = np.array([self.width//2, self.height//2])
        centered = t_center - my_center
        centered_norm = centered / radius
        return centered_norm, topping.topping_name

    def remove_waffle(self):
        waffle = self.waffle
        self.waffle = None
        toppings = list(map(self.norm_transform,self.toppings.copy()))
        self.toppings.clear()
        return waffle, toppings

    def add_topping(self, topping):
        self.toppings.append(topping)

    def draw(self):
        super().draw()
        if self.waffle is not None:
            self.waffle.draw()
            utils.draw_circle(self.center()[0], self.center()[1],radius=(constants.CENTER_RADIUS*self.width)//2,color=colors.yellow)
            utils.draw_circle(self.center()[0], self.center()[1],radius=(constants.MIDDLE_RADIUS*self.width)//2,color=colors.yellow)

        for topping in self.toppings:
            topping.draw()



class WaffleBig(GameObject):
    def __init__(self,x,y, cook_time,batter_type):

        super().__init__(name="WaffleBig",image=utils.load_image(IMAGE_LOOKUP[batter_type]),x=x,y=y,width=constants.BIG_WAFFLE_WIDTH,height=constants.BIG_WAFFLE_HEIGHT)
        self.cook_time = cook_time
        self.batter_type = batter_type
