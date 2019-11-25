import pygame
import numpy as np
import utils
from buttons import Button, StartGameButton, OrderButton, CookButton, BuildButton,TakeOrderButton, SubmitOrderButton, TossWaffleButton,JudgeOkButton
from objectnames import ObjectIds
from customers import Customer,CustomerPreTakeOrderLine,CustomerPostTakeOrderLine
from order import OrderTicket,OrderLine,OrderReceptacle
from cookstatestuff import CookMeter, WaffleMaker
from buildstatestuff import ToppingBin, Topping
from waffles import WaffleStack, WaffleEditor, WaffleBig
from judge import judge_waffle
from constants import Constants
import colors
constants = Constants()
objectids = ObjectIds()

menu_image = utils.load_image("menu.jpg")[0]

ORDERBUTTON = OrderButton(100,650,100,50)
COOKBUTTON = CookButton(300,650,100,50)
BUILDBUTTON = BuildButton(500,650,100,50)
TAKEORDERBUTTON = TakeOrderButton(775,550,200,50)
SUBMITORDERBUTTON = SubmitOrderButton(775,550,200,50)
TOSSWAFFLEBUTTON = TossWaffleButton(775,650,200,50)
JUDGEOKBUTTON = JudgeOkButton(300,650,100,50)

PRETAKEORDERLINE = CustomerPreTakeOrderLine(200,350)
POSTTAKEORDERLINE = CustomerPostTakeOrderLine(300,150)

ORDERLINE = OrderLine()
ORDERRECEPTACLE = OrderReceptacle()

WAFFLE_QUEUE_COOK = WaffleStack(775,650)
WAFFLE_EDITOR = WaffleEditor(175,200)


TOPPING_BINS = list()
TOPPING_BINS.append(ToppingBin(25,175,constants.CHOCOLATE_TOPPING))
TOPPING_BINS.append(ToppingBin(25,290,constants.CHERRY_TOPPING))
TOPPING_BINS.append(ToppingBin(25,405,constants.RAZZBERRY_TOPPING))
TOPPING_BINS.append(ToppingBin(25,520,constants.STRAWBERRY_TOPPING))
TOPPING_BINS.append(ToppingBin(600,175,constants.BANANA_TOPPING))
TOPPING_BINS.append(ToppingBin(600,290,constants.PEPPERMINT_TOPPING))
TOPPING_BINS.append(ToppingBin(600,405,constants.BUTTER_TOPPING))
TOPPING_BINS.append(ToppingBin(600,520,constants.BACON_TOPPING))

screen = None
def init_states(screen_ref):
    global screen
    screen = screen_ref


def get_menu_state():
    return MENUSTATE

def update_states():
    ORDERSTATE.update()
    COOKSTATE.update()
    BUILDSTATE.update()

class State:
    def __init__(self,name):
        self.name = name
        self.game_objects = list()
        self.selected_object = None

    def add_game_object(self,obj,priority=0):
        if priority == 0:
            self.game_objects.append(obj)
        else:
            self.game_objects.insert(0,obj)

    def remove_game_object(self,obj):
        self.game_objects.remove(obj)

    def draw(self):
        if screen is not None:
            for obj in self.game_objects:
                obj.draw()

    def get_object_over(self,state, mouse_x, mouse_y):
        for object in reversed(self.game_objects):
            if object.contains(mouse_x, mouse_y):
                return state, object
        return state, None

    def update(self):
        for object in self.game_objects:
            object.update()

    def interact_drag(self,state, mouse_x_start, mouse_y_start, mouse_x, mouse_y):
        if self.selected_object is not None:
            self.selected_object.drag(mouse_x_start, mouse_y_start, mouse_x, mouse_y)
        return state, None

    def interact_mouse_down(self,state,mouse_x, mouse_y):
        _ , obj = self.get_object_over(state,mouse_x,mouse_y)
        self.selected_object = obj
        return state, obj

    def interact_mouse_up(self,state,mouse_x, mouse_y):
        self.selected_object = None
        _ , obj = self.get_object_over(state,mouse_x,mouse_y)
        return state, obj

    def clear_selected_object(self):
        self.selected_object = None

class MenuState(State):
    def __init__(self):
        super().__init__("Menu")
        self.add_game_object(Button(objectids.STARTGAME,100,480,100,50))

    def draw(self):
        if screen is not None:
            screen.blit(menu_image, (0,0))
            for obj in self.game_objects:
                obj.draw()

    def interact_mouse_down(self,state,mouse_x, mouse_y):
        _, obj = super().interact_mouse_down(state,mouse_x,mouse_y)
        if obj is not None:
            if obj.name is objectids.STARTGAME:
                return ORDERSTATE, None
        return state, obj


class GameState(State):
    def __init__(self,name):
        super().__init__(name)
        self.add_game_object(ORDERBUTTON)
        self.add_game_object(COOKBUTTON)
        self.add_game_object(BUILDBUTTON)
        self.add_game_object(ORDERLINE)
        self.add_game_object(ORDERRECEPTACLE)

    def draw(self):
        super().draw()

    def update(self):
        for object in self.game_objects:
            object.update()

    def interact_mouse_down(self,state,mouse_x, mouse_y):
        _ , obj = super().interact_mouse_down(state,mouse_x,mouse_y)
        next_state = state
        if obj is not None:
            if isinstance(obj, OrderTicket):
                obj.on_mouse_down(mouse_x, mouse_y)
            elif obj is ORDERRECEPTACLE:
                ticket = ORDERRECEPTACLE.remove_order_ticket()
                if ticket is not None:
                    self.add_game_object(ticket)
                    self.selected_object = ticket
                    ticket.on_mouse_down(mouse_x, mouse_y)
            elif obj is ORDERLINE:
                ticket = ORDERLINE.remove_ticket(mouse_x,mouse_y)
                if ticket is not None:
                    self.add_game_object(ticket)
                    self.selected_object = ticket
                    ticket.on_mouse_down(mouse_x, mouse_y)

        if next_state is not state:
            self.clear_selected_object()
        return next_state, obj

    def pull_waffle_from_queue(self):
        # pull waffle from queue and put in big view
        if not WAFFLE_EDITOR.has_waffle():
            waffle = WAFFLE_QUEUE_COOK.remove_waffle()
            if waffle is not None:
                big_waffle = WaffleBig(0,0,waffle.cook_time,waffle.batter_type)
                WAFFLE_EDITOR.set_waffle(big_waffle)

    def interact_mouse_up(self,state,mouse_x, mouse_y):
        # _ , obj = super().interact_mouse_up(state,mouse_x,mouse_y)
        obj = self.selected_object
        next_state = state
        if obj is not None: # should this be callback based?
            if isinstance(obj, OrderButton):
                next_state, obj =  ORDERSTATE, None
            elif isinstance(obj, CookButton):
                next_state, obj = COOKSTATE, None
            elif isinstance(obj, BuildButton):
                next_state, obj = BUILDSTATE, None


                # pull waffle from queue and put in big view
                self.pull_waffle_from_queue()
                # if not WAFFLE_EDITOR.has_waffle():
                #     waffle = WAFFLE_QUEUE_COOK.remove_waffle()
                #     if waffle is not None:
                #         big_waffle = WaffleBig(0,0,waffle.cook_time,waffle.batter_type)
                #         WAFFLE_EDITOR.set_waffle(big_waffle)


            elif isinstance(obj, OrderTicket):
                if obj.intersects(ORDERRECEPTACLE) and ORDERRECEPTACLE.contains(mouse_x, mouse_y) and not ORDERRECEPTACLE.has_ticket():
                    ORDERRECEPTACLE.set_order_ticket(obj)
                    self.remove_game_object(obj)
                else: # snap back, TODO maybe combine above clause
                    ORDERLINE.add_ticket(obj)
                    self.remove_game_object(obj)
        if next_state is not state:
            self.clear_selected_object()
        return next_state, obj


class OrderState(GameState):
    def __init__(self):
        super().__init__("OrderState")
        # self.view = get_order_view()
        customer = Customer(objectids.CUSTOMER,400,400)
        customer2 = Customer(objectids.CUSTOMER,700,400)
        customer3 = Customer(objectids.CUSTOMER,800,400)

        self.add_game_object(PRETAKEORDERLINE)
        self.add_game_object(POSTTAKEORDERLINE)
        PRETAKEORDERLINE.add_customer(customer)
        PRETAKEORDERLINE.add_customer(customer2)
        PRETAKEORDERLINE.add_customer(customer3)

        self.add_game_object(TAKEORDERBUTTON)

    def interact_mouse_up(self,state, mouse_x, mouse_y):
        next_state , obj = super().interact_mouse_up(state, mouse_x,mouse_y)
        if obj is not None:
            if isinstance(obj, TakeOrderButton):
                obj = None
                # Todo take order by adding customers order ticket to
                if PRETAKEORDERLINE.has_waiting_customer():
                    customer = PRETAKEORDERLINE.remove_first_customer()
                    POSTTAKEORDERLINE.add_customer(customer)
                    ticket = ORDERRECEPTACLE.remove_order_ticket()
                    if ticket is not None:
                        ORDERLINE.add_ticket(ticket)
                    ORDERRECEPTACLE.set_order_ticket(customer.get_ticket())

        return next_state, obj

    def draw(self):
        super().draw()

class CookState(GameState):
    def __init__(self):
        super().__init__("CookState")
        self.add_game_object(WaffleMaker(100,150))
        self.add_game_object(WaffleMaker(450,150))
        self.add_game_object(WaffleMaker(100,400))
        self.add_game_object(WaffleMaker(450,400))
        self.add_game_object(WAFFLE_QUEUE_COOK,priority=1)

    def draw(self):
        super().draw()

    def interact_mouse_down(self,state, mouse_x, mouse_y):
        next_state , obj = super().interact_mouse_down(state, mouse_x,mouse_y)
        if obj is not None:
            if isinstance(obj, WaffleMaker):
                waffle = obj.on_mouse_down(mouse_x,mouse_y)
                if waffle is not None:
                    WAFFLE_QUEUE_COOK.add_waffle(waffle)

        return next_state, obj

class BuildState(GameState):
    def __init__(self):
        super().__init__("BuildState")
        self.add_game_object(SUBMITORDERBUTTON)
        self.add_game_object(TOSSWAFFLEBUTTON)
        self.add_game_object(WAFFLE_EDITOR)
        for topping_bin in TOPPING_BINS:
            self.add_game_object(topping_bin)

    def interact_mouse_up(self,state, mouse_x, mouse_y):
        next_state , obj = super().interact_mouse_up(state, mouse_x,mouse_y)
        if obj is not None:
            if isinstance(obj, SubmitOrderButton):
                obj = None
                if WAFFLE_EDITOR.has_waffle():
                    ticket = ORDERRECEPTACLE.remove_order_ticket()
                    if ticket is not None:
                            waffle,toppings  = WAFFLE_EDITOR.remove_waffle()
                            customer = POSTTAKEORDERLINE.remove_customer(ticket.customerID)
                            wait_score, cook_score, build_score = judge_waffle(ticket,customer, waffle, toppings)
                            JUDGESTATE.set_scores(wait_score, cook_score, build_score)
                            next_state = JUDGESTATE
                            # self.pull_waffle_from_queue()
            if isinstance(obj, TossWaffleButton):
                obj = None
                if WAFFLE_EDITOR.has_waffle():
                    WAFFLE_EDITOR.remove_waffle()
                    self.pull_waffle_from_queue()

            if isinstance(obj, Topping):
                if WAFFLE_EDITOR.contains_center_obj(obj) and WAFFLE_EDITOR.has_waffle():
                    WAFFLE_EDITOR.add_topping(obj)
                    self.selected_object = obj =  None
                else:
                    self.selected_object = None

        return next_state, obj

    def interact_mouse_down(self,state,mouse_x,mouse_y):
        next_state, obj = super().interact_mouse_down(state,mouse_x,mouse_y)
        if obj is not None:
            if isinstance(obj, ToppingBin):
                topping = obj.get_topping()
                topping.x = mouse_x - topping.width//2
                topping.y = mouse_y - topping.height//2
                self.selected_object = topping
        return next_state, obj

    def draw(self):
        super().draw()
        if self.selected_object is not None:
            if isinstance(self.selected_object, Topping):
                self.selected_object.draw()

class JudgeState(State):
    def __init__(self):
        super().__init__("JudgeState")
        self.wait_score = 0
        self.cook_score = 0
        self.build_score = 0
        self.add_game_object(JUDGEOKBUTTON)

    def set_scores(self, wait_score, cook_score, build_score):
        self.wait_score = wait_score
        self.cook_score = cook_score
        self.build_score = build_score

    def draw(self):
        super().draw()
        utils.draw_text("Wait Score : %d" % int(self.wait_score), 100,100,color=colors.white)
        utils.draw_text("Cook Score : %d" % int(self.cook_score), 100,200,color=colors.white)
        utils.draw_text("Build Score : %d" % int(self.build_score), 100,300,color=colors.white)

    def interact_mouse_up(self,state, mouse_x, mouse_y):
        next_state , obj = super().interact_mouse_down(state, mouse_x,mouse_y)
        if obj is not None:
            if isinstance(obj, JudgeOkButton):
                obj = None
                PRETAKEORDERLINE.add_customer(Customer(objectids.CUSTOMER,400,400))
                next_state = ORDERSTATE # Maybe change ?
                # do stuff
        return next_state, obj

MENUSTATE = MenuState()
ORDERSTATE = OrderState()
COOKSTATE = CookState()
BUILDSTATE = BuildState()
JUDGESTATE = JudgeState()
