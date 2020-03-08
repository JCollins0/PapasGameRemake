from objects import GameObject, Dragable
import colors
from constants import Constants
from objectnames import ObjectIds
import utils
objectids = ObjectIds()
constants = Constants()

def sort_by_degree_func(obj1):
    return obj1.degrees

COOK_TIME_IMAGES = {
constants.FROZEN_TIME : utils.load_image("cook_frozen")[0],
constants.UNDERCOOKED_TIME: utils.load_image("cook_undercook")[0],
constants.MEDIUM_COOOKED_TIME: utils.load_image("cook_medium")[0],
constants.COOKED_WELL_TIME: utils.load_image("cook_well")[0],
constants.BURNT_TIME: utils.load_image("cook_burnt")[0]
}

COOK_BATTER_IMAGES = {
constants.BANANA_BATTER : utils.load_image("bananabatter")[0],
constants.BLUEBERRY_BATTER : utils.load_image("blueberrybatter")[0],
constants.BUTTER_BATTER : utils.load_image("butterbatter")[0],
constants.CHERRY_BATTER : utils.load_image("cherrybatter")[0],
constants.CHOCOLATE_BATTER : utils.load_image("chocolatebatter")[0],
constants.PUMPKIN_BATTER : utils.load_image("pumpkinbatter")[0],
constants.RAINBOW_BATTER : utils.load_image("rainbowbatter")[0],
}

TOPPING_IMAGES = {
    constants.CHOCOLATE_TOPPING:utils.load_image("chocolatechip")[0],
    constants.CHERRY_TOPPING:utils.load_image("cherry")[0],
    constants.RAZZBERRY_TOPPING:utils.load_image("razzberry")[0],
    constants.STRAWBERRY_TOPPING:utils.load_image("strawberry")[0],
    constants.BANANA_TOPPING:utils.load_image("banana")[0],
    constants.PEPPERMINT_TOPPING:utils.load_image("peppermint")[0],
    constants.BUTTER_TOPPING:utils.load_image("butter")[0],
    constants.BACON_TOPPING:utils.load_image("bacon")[0],
}

RING_IMAGES = {
    constants.LEFT:{
        constants.OUTER: utils.load_image_and_rotate("outer_ring_sided",180)[0],
        constants.MIDDLE: utils.load_image_and_rotate("middle_ring_sided",180)[0],
        constants.CENTER: utils.load_image_and_rotate("center_ring_sided",180)[0],
    },
    constants.RIGHT:{
        constants.OUTER: utils.load_image("outer_ring_sided")[0],
        constants.MIDDLE: utils.load_image("middle_ring_sided")[0],
        constants.CENTER: utils.load_image("center_ring_sided")[0],
    },
    constants.TOP:{
        constants.OUTER: utils.load_image_and_rotate("outer_ring_sided",90)[0],
        constants.MIDDLE: utils.load_image_and_rotate("middle_ring_sided",90)[0],
        constants.CENTER: utils.load_image_and_rotate("center_ring_sided",90)[0],
    },
    constants.BOTTOM:{
        constants.OUTER: utils.load_image_and_rotate("outer_ring_sided",-90)[0],
        constants.MIDDLE: utils.load_image_and_rotate("middle_ring_sided",-90)[0],
        constants.CENTER: utils.load_image_and_rotate("center_ring_sided",-90)[0],
    },
    constants.WHOLE:{
        constants.OUTER: utils.load_image("outer_ring_whole")[0],
        constants.MIDDLE: utils.load_image("middle_ring_whole")[0],
        constants.CENTER: utils.load_image("center_ring_whole")[0],
    },
}

class Criteria:
    def __init__(self): pass
    def eval(self,metadata): return 0
    def draw(self,x,y,width_scale,height_scale,parent_width,parent_height): pass

class WaitCriteria(Criteria):
    def __init__(self, max_wait_time):
        self.max_wait_time = max_wait_time

    def eval(self, metadata):
        time = metadata.wait_time
        if time <= self.max_wait_time:
            return 100
        else:
            return max(0,100-.5*( (time-self.max_wait_time)**2 / self.max_wait_time ))

    def __str__(self):
        return self.max_wait_time

class SideCriteria(Criteria):
    def __init__(self):
        pass

    def eval(self,metadata): return 0
    def draw(self,x,y,width_scale,height_scale,parent_width,parent_height):
        pass

class CookCriteria(Criteria):
    def __init__(self, type, cook_time):
        self.type = type
        self.cook_time = cook_time

    def eval(self, metadata):
        cook_percent = max((1 - 2 * abs(self.cook_time - metadata.cook_time) / constants.MAX_COOK_TIME) * 100,0)
        dough_percent = 100 if self.type == metadata.batter_type else 0
        return (cook_percent + dough_percent) / 2

    def draw(self,x,y,width_scale, height_scale,parent_width,parent_height):
        scale = 50/25
        batter_image = COOK_BATTER_IMAGES[self.type]
        batter_image_width, batter_image_height = batter_image.get_width(), batter_image.get_height()
        utils.draw_image_scaled(batter_image,x,y,batter_image_width,batter_image_height,int(batter_image_width*width_scale*scale),int(batter_image_height*height_scale*scale))
        image = COOK_TIME_IMAGES[self.cook_time]
        image_width, image_height = image.get_width(), image.get_height()
        utils.draw_image_scaled(image,x+int(1.2*batter_image_width*width_scale*scale),y,image_width,image_height,int(image_width*width_scale),int(image_height*height_scale))

    def __str__(self):
        return self.type + " " + str(self.cook_time)

class ToppingCriteria(Criteria):
    def __init__(self, amount, name, ring, sided=False, side=constants.WHOLE):
        self.amount = amount
        self.topping_name = name
        self.ring = ring
        self.sided = sided
        self.side = side

    def draw(self,x,y,width_scale, height_scale,parent_width,parent_height):
        scale = 50/25
        image = TOPPING_IMAGES[self.topping_name]
        ring_image = RING_IMAGES[self.side][self.ring]
        ring_image_width, ring_image_height = ring_image.get_width(), ring_image.get_height()
        utils.draw_image_scaled(ring_image,x,y,ring_image_width,ring_image_height,int(ring_image_width*width_scale*scale),int(ring_image_height*height_scale*scale))
        utils.draw_big_text_scaled(str(self.amount),int(x + 1.5 * ring_image_width*width_scale*scale),y,parent_width/250,parent_height/500 )
        image_width, image_height = image.get_width(), image.get_height()
        utils.draw_image_scaled(image,x+3*image_width*width_scale,y,image_width,image_height,int(image_width*width_scale),int(image_height*height_scale))

    def eval(self, metadata):
        penalty = 0
        data = metadata.topping_data
        if self.ring not in data:
            return 0
        elif self.topping_name not in data[self.ring]:
            return 0

        topping_data = data[self.ring][self.topping_name]
        target_degrees = 360 / self.amount
        if self.sided:
            target_degrees = 180 / self.amount
            reduced_topping_data = list(filter(lambda x: x.is_on_side(self.side),topping_data))
            if len(reduced_topping_data) == 0: # didnt place any on correct side
                return 0
            if len(reduced_topping_data) is not self.amount:
                # penalty or just stop maybe we dont care
                if len(reduced_topping_data) > self.amount:
                    print("Too much %s on the %s side" % (self.topping_name,self.side))
                if len(reduced_topping_data) < self.amount:
                    print("Not enough %s on the %s side" % (self.topping_name,self.side))
                penalty += constants.JUDGE_TOPPING_DIFFERENT_AMOUNT_PENALTY * abs(len(reduced_topping_data) - self.amount)
            topping_data = reduced_topping_data
            # change angles to be on 180 to 0 on right side
            if self.side == constants.RIGHT:
                topping_data = self.change_degrees_for_right(topping_data)
        else:
            if len(topping_data) is not self.amount:
                print("Not enough %s" % self.topping_name)
                penalty += constants.JUDGE_TOPPING_DIFFERENT_AMOUNT_PENALTY * abs(len(topping_data)-self.amount)

        for topping in topping_data:
            topping.processed = True

        dxs,p = self.calc_dtheta(topping_data)
        penalty += p
        penalty += self.check_target_degrees(dxs,target_degrees)
        penalty += self.calc_ddtheta_penalty(dxs)

        print(dxs, penalty)
        # print(metadata.topping_data)
        return max(0, 100-penalty)

    def check_target_degrees(self,dxs, target):
        penalty = 0
        for dx in dxs:
            if abs(dx - target) > constants.JUDGE_TOPPING_ANGLE_LENIENCY:
                print("bad placement cheater!!", dx, target, )
                penalty += 20
        return penalty

    def change_degrees_for_right(self,topping_list):
        for topping in topping_list:
            topping.degrees = ( topping.degrees + 90 ) % 360
        return topping_list

    def calc_dtheta(self, toppings):
        if len(toppings) == 0:  return [0],0
        if len(toppings) == 1:
            if not self.sided:
                return [360],0
            else:
                return [180],0
        toppings = sorted(toppings,key = sort_by_degree_func)
        penalty = 0
        dxs = list()
        if not self.sided:
            # only care about distance arround pizza if the toppings go on whole waffle
            dxs.append((toppings[0].degrees-toppings[-1].degrees+360) %360)
        else:
            angle = (toppings[0].degrees-toppings[-1].degrees+360) %360
            compareto = 180 + (360 / self.amount)//2 +10
            penalty = constants.JUDGE_TOPPING_ANGLE_NOT_EQUAL_PENALTY if angle > compareto  else 0 #constants.JUDGE_TOPPING_ANGLE_SIDED_LENIENCY
            print("penalty:%f %f vs %f" % (penalty, angle, compareto))

        for i in range(1,len(toppings)):
            dxs.append(toppings[i].degrees-toppings[i-1].degrees)
        return dxs,penalty

    def calc_ddtheta_penalty(self, dxs):
        penalty = 0
        for i in range(1,len(dxs)):
            diff = abs(dxs[i]-dxs[i-1])
            if diff > constants.JUDGE_TOPPING_ANGLE_LENIENCY:
                print("Bad Placement",dxs[i],dxs[i-1],diff)
                penalty += constants.JUDGE_TOPPING_ANGLE_NOT_EQUAL_PENALTY
        return penalty

class Order:
    def __init__(self):
        self.criterion = list()

    def set_criterion(self, criterion):
        self.criterion = criterion.copy()

    def add_criteria(self, criteria):
        self.criterion.append(criteria)

    def judge(self, metadata):
        topping_criteria = list(map(lambda y: y.amount, filter(lambda x: isinstance(x, ToppingCriteria), self.criterion)))
        wait_score,cook_score,build_score = 0, 0, 0
        wait_count,cook_count,build_count = 0, 0, 0
        for criteria in self.criterion:
            score = criteria.eval(metadata)
            if isinstance(criteria, CookCriteria):
                cook_score += score
                cook_count += 1
            if isinstance(criteria, WaitCriteria):
                wait_score += score
                wait_count += 1
            if isinstance(criteria, ToppingCriteria):
                build_score += score
                build_count += 1
        if cook_count == 0:
            cook_count = 1
        if wait_count == 0:
            wait_count = 1
        if build_count == 0:
            build_count = 1

        extra_build_penalty = 0
        num_toppings_required = sum(topping_criteria)
        toppings_on_editor = 0
        toppings_not_processed= 0
        for ring in metadata.topping_data:
            for topping_name in metadata.topping_data[ring]:
                for topping in metadata.topping_data[ring][topping_name]:
                    toppings_on_editor += 1
                    if not topping.processed:
                        toppings_not_processed += 1

        if len(topping_criteria) > 0:
            # punish extra toppings
            extra_build_penalty = constants.JUDGE_TOPPING_EXTRA_TOPPING_PENALTY * toppings_not_processed

            print("Sum",num_toppings_required, toppings_on_editor )
            if num_toppings_required > toppings_on_editor:
                extra_build_penalty += abs(num_toppings_required - toppings_on_editor) * constants.JUDGE_MISSING_TOPPINGS_PENALTY

        else:
            build_score = 100
            build_count = 1
            if num_toppings_required < toppings_on_editor:
                build_score = 0
                extra_build_penalty = constants.JUDGE_TOPPING_EXTRA_TOPPING_PENALTY * toppings_not_processed

        extra_build_penalty = min(100, extra_build_penalty)
        extra_build_score = 100 - extra_build_penalty
        print(wait_score, wait_count,cook_score , cook_count, extra_build_score,build_score , (build_count+1))
        return wait_score / wait_count,cook_score / cook_count, (extra_build_score+build_score) / (build_count+1)

class OrderLine(GameObject):
    def __init__(self):
        super().__init__(objectids.ORDERLINE,image=utils.load_image("orderline"),x=0,y=25,width=constants.SCREEN_WIDTH-250,height=100)
        self.tickets = list()

    def add_ticket(self, ticket):
        ticket.width, ticket.height = 50, 100
        snapto_y = self.y

        furthest_x = self.width-ticket.width

        for t in self.tickets:
            for r in self.tickets:
                if r.x == furthest_x:
                    furthest_x -= 55

        snapto_x = min(furthest_x, ticket.x)
        ticket.move_to(x=snapto_x,y=snapto_y)
        self.tickets.append(ticket)

    def remove_ticket(self,mouse_x,mouse_y):
        ticket = None
        for t in reversed(self.tickets):
            if t.contains(mouse_x,mouse_y):
                ticket = t
                break
        if ticket is not None:
            self.tickets.remove(ticket)
        return ticket

    def draw(self):
        super().draw()
        for ticket in self.tickets:
            ticket.draw()

class OrderReceptacle(GameObject):
    def __init__(self):
        super().__init__(objectids.ORDERRECEPTACLE,image=utils.load_image("ticket_holder"),x=constants.SCREEN_WIDTH-250,y=0,width=250,height=500,color=colors.red)
        self.order_ticket = None

    def set_order_ticket(self, ticket):
        self.order_ticket = ticket
        if self.order_ticket is not None:
            self.order_ticket.width, self.order_ticket.height = 250, 500
            self.order_ticket.move_to(x=self.x,y=self.y)

    def remove_order_ticket(self):
        ticket = self.order_ticket
        self.order_ticket = None
        return ticket

    def has_ticket(self):
        return self.order_ticket is not None

    def draw(self):
        super().draw()
        if self.order_ticket is not None:
            self.order_ticket.draw()

class OrderTicket(GameObject, Dragable):
    def __init__(self,name,x,y,customerID,recipe):
        super().__init__(name,image=utils.load_image("ticket"),x=x,y=y,width=50,height=100,color=colors.blue)
        self.small_width = self.width
        self.small_height = self.height
        self.customerID = customerID
        self.recipe = recipe

    def drag(self,mouse_x_start, mouse_y_start, mouse_x, mouse_y):
        if isinstance(self, Dragable):
            self.move(dx = mouse_x-mouse_x_start, dy = mouse_y-mouse_y_start)

    def on_mouse_down(self,mouse_x, mouse_y):
        orig_width, orig_height = self.width, self.height
        self.width, self.height = self.small_width, self.small_height
        x , y = mouse_x - ( mouse_x - self.x ) / (orig_width / self.width) , mouse_y - ( mouse_y - self.y ) / (orig_height / self.height)
        self.move_to(x=x,y=y)

    def draw(self):
        super().draw_scaled()
        utils.draw_big_text_scaled(str(self.customerID),int(self.x+self.width//2-utils.get_big_font_size(str(self.customerID))[0]/2*self.width/250), self.y,self.width/250,self.height/500)
        if self.recipe is not None:
            for i,criterion in enumerate(self.recipe.criterion,1):
                criterion.draw(self.x+(self.width-constants.CRITERIA_IMAGE_WIDTH*self.width/250)//2,self.y+self.height-i*(constants.CRITERIA_IMAGE_HEIGHT*self.height/500+20*self.height/500),self.width/250, self.height/500,self.width,self.height)
                # utils.draw_small_text(str(criterion),self.x,self.y+i*32,color=colors.white)
