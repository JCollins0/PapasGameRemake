import numpy as np
import colors
import utils
from constants import Constants
from order import Order, WaitCriteria
constants = Constants()

WAFFLE_RADIUS = constants.BIG_WAFFLE_WIDTH / constants.WAFFLE_EDITOR_WIDTH

def dist_from_center(topping):
# (array([ 0.98 , -0.015]), 'chocolatechips')
    topping_pos = topping[0]
    dist = np.linalg.norm(topping_pos-np.array([0,0]))
    return dist

def degree(topping):
    pos = topping[0]
    degrees = np.degrees(np.arctan2(pos[0],pos[1]))
    # fix - to + degrees
    if degrees < 0:
        degrees += 360
    degrees -= 90 # rotate
    # fix - to + degrees
    if degrees < 0:
        degrees += 360
    return degrees

class MetaData:
    def __init__(self,wait_time,batter_type,cook_time,topping_metadata_dict):
        self.wait_time = wait_time
        self.batter_type = batter_type
        self.cook_time = cook_time
        self.topping_data = topping_metadata_dict


class ToppingMetaData:
    def __init__(self,topping):
        self.pos = topping[0]
        self.degrees = degree(topping)
        self.dist = dist_from_center(topping)
        self.processed = False

    def is_on_waffle(self):
        return self.dist <= WAFFLE_RADIUS

    def is_on_side(self,side):
        if side == constants.TOP:
            return self.on_top_side()
        if side == constants.BOTTOM:
            return self.on_bottom_side()
        if side == constants.LEFT:
            return self.on_left_side()
        if side == constants.RIGHT:
            return self.on_right_side()

    def on_left_side(self):
        return self.is_on_waffle() and self.pos[0] < 0

    def on_right_side(self):
        return self.is_on_waffle() and self.pos[0] > 0

    def on_top_side(self):
        return self.is_on_waffle() and self.pos[1] < 0

    def on_bottom_side(self):
        return self.is_on_waffle() and self.pos[1] > 0

    def on_outer_ring(self):
        return self.is_on_waffle() and self.dist > constants.MIDDLE_RADIUS
    def on_middle_ring(self):
        return self.is_on_waffle() and constants.CENTER_RADIUS <= self.dist <= constants.MIDDLE_RADIUS
    def on_center_ring(self):
        return self.is_on_waffle() and self.dist < constants.CENTER_RADIUS

    def get_ring_on(self):
        o, m, c = self.on_outer_ring(), self.on_middle_ring(), self.on_center_ring()
        return constants.OUTER if o else constants.MIDDLE if m else constants.CENTER if c else "BAD"

    def __repr__(self):
        attr= [
            'pos %s' % self.pos,
            'deg %0f' % self.degrees,
            'dist %2f' % self.dist,
            'on %s' % self.is_on_waffle(),
            'left %s' % self.on_left_side(),
            'right %s' % self.on_right_side(),
            'top %s' % self.on_top_side(),
            'bottom %s' % self.on_bottom_side(),
            'outer %s' % self.on_outer_ring(),
            'middle %s' % self.on_middle_ring(),
            'center %s' % self.on_center_ring(),
            'processed %s' % self.processed,
        ]
        return ' '.join(attr)

    def __str__(self):
        return self.__repr__()


def split_toppings(toppings):
    d = {}
    for topping in toppings:
        type = topping[1]

        tmeta = ToppingMetaData(topping)
        ring = tmeta.get_ring_on()
        if ring not in d:
            d[ring] = dict()
            if type not in d[ring]:
                d[ring][type] = list()
        elif type not in d[ring]:
            d[ring][type] = list()
        d[ring][type].append(tmeta)
    return d


def judge_waffle(ticket,customer, waffle, toppings_normalized):
    toppings = toppings_normalized
    topping_dictionary = split_toppings(toppings)
    metadata = MetaData(wait_time=customer.get_wait_time(),batter_type=waffle.batter_type,cook_time=waffle.cook_time,topping_metadata_dict=topping_dictionary)
    print("judge_waffle",topping_dictionary)
    order = Order()
    order.set_criterion(ticket.recipe.criterion)
    order.add_criteria(WaitCriteria(customer.get_max_wait_time()))
    wait_score, cook_score, build_score = order.judge(metadata)
    print(wait_score, cook_score, build_score)
    return wait_score, cook_score, build_score
    # for topping in toppings:
    #     print(topping_is_on_waffle(waffle,topping))
    #     degree(topping)
