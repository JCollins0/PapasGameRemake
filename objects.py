import pygame
import utils
import colors

screen = None
def init_objects(screen_ref):
    global screen
    screen = screen_ref

class Dragable:
    pass

class GameObject:
    def __init__(self,name,image=None,x=0,y=0,width=0,height=0,color=colors.black):
        self.name = name
        self.images = image
        self.image_state = 0
        self.x = x
        self.y = y
        self.width= width
        self.height = height
        self.color = color
        self.should_render = True
        # print(name, image == None, x, y, width, height, color)
        # if image is not None:
        #     print(len(image))



    def drag(self,mouse_x_start, mouse_y_start, mouse_x, mouse_y):
        if isinstance(self, Dragable):
            self.move(dx = mouse_x-mouse_x_start, dy = mouse_y-mouse_y_start)

    def move_to(self, x=None, y=None):
        if y is not None:
            self.y = y
        if x is not None:
            self.x = x

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def show(self):
        self.should_render= True

    def hide(self):
        self.should_render= False

    def center(self):
        return [self.x + self.width // 2 , self.y + self.height //2]

    def contains(self, px,py):
        return self.x <= px <= self.x + self.width and self.y <= py <= self.y + self.height

    def contains_obj(self, obj):
        return self.x <= obj.x <= self.x + self.width and \
               self.y <= obj.y <= self.y + self.height and \
               self.x <= obj.x + obj.width <= self.x + self.width and \
               self.y <= obj.y + obj.height <= self.y + self.height

    def contains_center_obj(self, obj):
        return self.contains(*obj.center())


    def intersects(self, other):
        x1,y1 = self.x,self.y
        x2,y2 = self.x + self.width, self.y + self.height

        x3,y3 = other.x,other.y
        x4,y4 = other.x + other.width, other.y + other.height

        x5 = max(x1, x3)
        y5 = max(y1, y3)
        x6 = min(x2, x4)
        y6 = min(y2, y4)

        if (x5 > x6 or y5 > y6):
            return False
        return True

    def draw(self):
        if self.should_render:
            if self.images is not None:
                utils.draw_image(self.images[self.image_state],self.x,self.y)
            else:
                utils.draw_rect(self.color, self.x,self.y,self.width,self.height)

    def update(self):
        pass

    def interact(self, state, m_x, m_y):
        pass

    def on_mouse_down(self,mouse_x, mouse_y):
        pass

    def on_mouse_up(self,mouse_x, mouse_y):
        pass
