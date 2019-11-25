from objects import GameObject, Dragable
import colors
import utils
from order import OrderTicket
import recipes
import numpy as np

STAND_STILL = 0
WALKING_TO_COUNTER = 1
WAITING_FOR_TAKE_ORDER = 2
WAITING_FOR_FOOD = 3

actions = ["STAND_STILL", "WALKING_TO_COUNTER", "WAITING_FOR_TAKE_ORDER", "WAITING_FOR_FOOD"]

customerId = 0

recipe_list = [recipes.CrispyPumpkin(),
               recipes.ButterLover(),
               recipes.StrawBerryWaffle(),
               recipes.RainbowBaconWaffle(),
               recipes.BerryLoverWaffle(),
               recipes.ChocoBananaWaffle(),
               recipes.PlainJane()]

WAIT_UPDATE_DELAY = 60
class Customer(GameObject,Dragable):
    def __init__(self,name,x,y):
        super().__init__(name,x=x,y=y,width=75,height=150,color=colors.green)
        self.status = WALKING_TO_COUNTER
        self.recipe = recipe_list[int(np.random.choice(len(recipe_list),1))]
        self.wait_update_delay_count = 0
        self.wait_time = 0
        self.max_wait_time = 120
        global customerId
        self.id = customerId
        customerId += 1


    def get_max_wait_time(self):
        return self.max_wait_time

    def get_wait_time(self):
        return self.wait_time  #TODO implement and change variable in update

    def get_ticket(self):
        return OrderTicket("name",0,0,self.id,self.recipe)

    def walk_to_counter(self,line,customerBehind):
        if customerBehind is None:
            if self.x > line.x:
                self.move(dx=-1)
            else:
                self.status = WAITING_FOR_TAKE_ORDER
        else:
            if self.x > customerBehind.x + customerBehind.width + 10:
                self.move(dx=-1)

    def walk_in_post_take_order_line(self,line,customerBehind):
        if customerBehind is None:
            if self.x > line.x:
                self.move(dx=-1)
        else:
            if self.x > customerBehind.x + customerBehind.width + 10:
                self.move(dx=-1)

    def update(self,line,customerBehind):
        if self.status is WALKING_TO_COUNTER:
            self.walk_to_counter(line,customerBehind)
        elif self.status is WAITING_FOR_FOOD:
            self.walk_in_post_take_order_line(line,customerBehind)

        if self.wait_update_delay_count >= WAIT_UPDATE_DELAY:
            self.wait_update_delay_count = 0
            self.wait_time += 1
        else:
            self.wait_update_delay_count += 1

    def draw(self):
        super().draw()
        utils.draw_small_text(actions[self.status], self.x, self.y)
        utils.draw_small_text(str(self.id), self.x,self.y+16)
        utils.draw_small_text(str(self.wait_time), self.x,self.y+32)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id

class CustomerOrderLine(GameObject):
    def __init__(self,x,y,width=800,height=150):
        super().__init__("CustomerOrderLine",x=x,y=y,width=width,height=height,color=colors.white)
        self.customers = list()

    def update(self):
        for i in range(len(self.customers)):
            customer = self.customers[i]
            customerBehind = None
            if i > 0:
                customerBehind = self.customers[i-1]
            customer.update(self,customerBehind)

    def add_customer(self, customer):
        if customer not in self.customers:
            customer.move_to(x=self.x+self.width,y=self.y)
            customer.status = WALKING_TO_COUNTER
            self.customers.append(customer)
            return True
        return False

    def remove_first_customer(self):
        if len(self.customers) > 0:
            return self.customers.pop(0)

    def draw(self):
        super().draw()
        for customer in self.customers:
            customer.draw()

    def has_waiting_customer(self):
        if len(self.customers) > 0:
            if self.customers[0].status is WAITING_FOR_TAKE_ORDER:
                return True

class CustomerPreTakeOrderLine(CustomerOrderLine):
    def __init__(self,x,y):
        super().__init__(x=x,y=y,width=550)

class CustomerPostTakeOrderLine(CustomerOrderLine):
    def __init__(self,x,y):
        super().__init__(x=x,y=y,width=450)

    def add_customer(self, customer):
        if super().add_customer(customer):
            customer.status = WAITING_FOR_FOOD
            return True
        return False

    def remove_customer(self, customerID):
        customer = None
        for c in self.customers:
            if c.id is customerID:
                customer = c
        if customer is not None:
            self.customers.remove(customer)
        return customer
