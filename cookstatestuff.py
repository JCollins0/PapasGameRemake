import colors
import utils
from objects import GameObject
from waffles import WaffleSmall
from constants import Constants

constants = Constants()

class WaffleMaker(GameObject):
    def __init__(self,x,y):
        super().__init__("WaffleMaker",image=utils.load_sprite_sheet("wafflemaker",constants.WAFFLE_MAKER_SIZE,constants.WAFFLE_MAKER_SIZE), x=x,y=y,width=constants.WAFFLE_MAKER_SIZE,height=constants.WAFFLE_MAKER_SIZE)
        self.waffle = None
        self.cook_meter = CookMeter(x=self.x - constants.COOK_METER_WIDTH - 10, y=self.y,height=self.height)
        self.batter_selector = BatterSelector(x=self.x+self.width+10, y=self.y, height=self.height)
        self.selected_batter = constants.DUMP_BATTER

    def set_waffle(self, waffle):
        if self.waffle is None:
            self.waffle = waffle
            return True
        return False

    def has_waffle(self):
        return self.waffle is not None

    def draw(self):
        super().draw()
        self.cook_meter.draw()
        self.batter_selector.draw()
        if self.selected_batter is not constants.DUMP_BATTER:
            utils.draw_rect(colors.black,
             self.batter_selector.x-constants.BATTER_OUTLINE_WIDTH,
             self.batter_selector.y+constants.BATTER_ICON_SIZE*BATTER_NAMES.index(self.selected_batter)-constants.BATTER_OUTLINE_WIDTH,
             constants.BATTER_ICON_SIZE+constants.BATTER_OUTLINE_WIDTH*2,
             constants.BATTER_ICON_SIZE+constants.BATTER_OUTLINE_WIDTH*2,
             outline_width=constants.BATTER_OUTLINE_WIDTH)
        # utils.draw_text(self.selected_batter, self.x, self.y)

    def update(self):
        super().update()
        if self.selected_batter is not constants.DUMP_BATTER:
            self.cook_meter.update()

    def on_mouse_down(self, mouse_x,mouse_y):
        if self.batter_selector.contains(mouse_x,mouse_y):
            batter = self.batter_selector.get_selected_batter(mouse_x,mouse_y)
            if batter == constants.DUMP_BATTER:
                self.reset()
            elif self.selected_batter is constants.DUMP_BATTER:
                self.selected_batter = batter
                self.image_state = 1
        else:
            if self.selected_batter is not constants.DUMP_BATTER:
                # clicking on waffle maker
                time_cooked = self.cook_meter.cook_time
                batter_cooked = self.selected_batter

                # reset
                self.reset()
                return WaffleSmall(time_cooked, batter_cooked)
        return None

    def reset(self):
        self.selected_batter = constants.DUMP_BATTER
        self.image_state = 0
        self.cook_meter.reset()

    def contains(self, mouse_x,mouse_y):
        return super().contains(mouse_x,mouse_y) or self.batter_selector.contains(mouse_x,mouse_y)

class BatterSelector(GameObject):
    def __init__(self,x,y,height):
        super().__init__("BatterSelector",x=x,y=y,width=constants.BATTER_ICON_SIZE,height=height,color=colors.red)
        self.batters = list()
        for i in range(len(BATTER_NAMES)):
            batter = BATTER_NAMES[i]
            self.batters.append(BatterIcon(name=batter,image=utils.load_sprite_sheet(batter,constants.BATTER_ICON_SIZE,constants.BATTER_ICON_SIZE),x=self.x,y=self.y+i*constants.BATTER_ICON_SIZE))

    def draw(self):
        super().draw()
        for batter in self.batters:
            batter.draw()

    def update(self):
        super().update()

    def get_selected_batter(self,mouse_x,mouse_y):
        num_batters = len(self.batters)
        item_dy = self.height/num_batters
        dy = (mouse_y-self.y)
        batter = self.batters[min(int(dy//item_dy),num_batters-1)]
        return batter.name

class BatterIcon(GameObject):
    def __init__(self,name,image,x,y):
        super().__init__(name=name,image=image,x=x,y=y,width=constants.BATTER_ICON_SIZE,height=constants.BATTER_ICON_SIZE)

class CookMeter(GameObject):
    def __init__(self,x,y,height):
        super().__init__("CookMeter",image=utils.load_image("cook_time_single"),x=x,y=y,width=constants.COOK_METER_WIDTH,height=height,color=colors.red)
        self.cook_time = 0
        self.delay = 0

    def draw(self):
        super().draw()
        if self.cook_time < constants.MAX_COOK_TIME:
            utils.draw_rect(colors.gray, self.x+1, self.y+self.height-2, self.width-2,-(self.height-int(( (self.cook_time+1)/constants.MAX_COOK_TIME)*self.height)))
        utils.draw_small_text(str(self.cook_time),self.x,self.y)

    def update(self):
        super().update()
        self.delay += 1
        if self.cook_time < constants.MAX_COOK_TIME:
            if self.delay % 60 == 0:
                self.cook_time += 1
                self.delay = 0
                # if self.cook_time % (constants.MAX_COOK_TIME // 4) == 0:
                #     self.image_state += 1

    def reset(self):
        self.delay = 0
        # self.image_state = 0
        self.cook_time = 0


BATTER_NAMES =[constants.BANANA_BATTER,constants.BLUEBERRY_BATTER,
constants.BUTTER_BATTER,constants.CHERRY_BATTER,constants.CHOCOLATE_BATTER,
constants.PUMPKIN_BATTER,constants.RAINBOW_BATTER,constants.DUMP_BATTER]
