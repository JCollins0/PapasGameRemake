from order import CookCriteria, ToppingCriteria
from constants import Constants
constants = Constants()

class Recipe:
    def __init__(self,name):
        self.criterion = list()

    def add_criteria(self, criteria):
        self.criterion.append(criteria)


class FrozenWaffle(Recipe):
    def __init__(self, name,batter):
        super().__init__(name)
        self.add_criteria(CookCriteria(type=batter, cook_time=constants.FROZEN_TIME))
class UnderCookedWaffle(Recipe):
    def __init__(self, name,batter):
        super().__init__(name)
        self.add_criteria(CookCriteria(type=batter, cook_time=constants.UNDERCOOKED_TIME))
class MediumCookedWaffle(Recipe):
    def __init__(self, name,batter):
        super().__init__(name)
        self.add_criteria(CookCriteria(type=batter, cook_time=constants.MEDIUM_COOOKED_TIME))

class FullCookedWaffle(Recipe):
    def __init__(self,name,batter):
        super().__init__(name)
        self.add_criteria(CookCriteria(type=batter, cook_time=constants.COOKED_WELL_TIME))

class BurntWaffle(Recipe):
    def __init__(self,name,batter):
        super().__init__(name)
        self.add_criteria(CookCriteria(type=batter, cook_time=constants.BURNT_TIME))


class StrawBerryWaffle(MediumCookedWaffle):
    def __init__(self):
        super().__init__("StrawBerryWaffle",constants.BUTTER_BATTER)
        self.add_criteria(ToppingCriteria(8, constants.STRAWBERRY_TOPPING, constants.OUTER))
        self.add_criteria(ToppingCriteria(8, constants.STRAWBERRY_TOPPING, constants.MIDDLE))
        self.add_criteria(ToppingCriteria(4, constants.STRAWBERRY_TOPPING, constants.CENTER))
        self.add_criteria(ToppingCriteria(1, constants.BUTTER_TOPPING, constants.CENTER))

class RainbowBaconWaffle(MediumCookedWaffle):
    def __init__(self):
        super().__init__("RainbowBaconWaffle",constants.RAINBOW_BATTER)
        self.add_criteria(ToppingCriteria(8, constants.BACON_TOPPING, constants.OUTER))
        self.add_criteria(ToppingCriteria(4, constants.BACON_TOPPING, constants.MIDDLE))
        self.add_criteria(ToppingCriteria(1, constants.BUTTER_TOPPING, constants.CENTER))

class CrispyPumpkin(BurntWaffle):
    def __init__(self):
        super().__init__("CrispyPumkinWaffle",constants.PUMPKIN_BATTER)
        self.add_criteria(ToppingCriteria(4, constants.BUTTER_TOPPING, constants.CENTER))

class ButterLover(FrozenWaffle):
    def __init__(self):
        super().__init__("ButterLoverWaffle",constants.BUTTER_BATTER)
        self.add_criteria(ToppingCriteria(16, constants.BUTTER_TOPPING, constants.OUTER))
        self.add_criteria(ToppingCriteria(8, constants.BUTTER_TOPPING, constants.MIDDLE))
        self.add_criteria(ToppingCriteria(4, constants.BUTTER_TOPPING, constants.CENTER))

class PlainJane(FullCookedWaffle):
    def __init__(self):
        super().__init__("PlainJaneWaffle",constants.BUTTER_BATTER)

class BerryLoverWaffle(FullCookedWaffle):
    def __init__(self):
        super().__init__("BerryLoverWaffle",constants.CHERRY_BATTER)
        self.add_criteria(ToppingCriteria(8, constants.STRAWBERRY_TOPPING, constants.OUTER))
        self.add_criteria(ToppingCriteria(4, constants.RAZZBERRY_TOPPING, constants.MIDDLE))
        self.add_criteria(ToppingCriteria(1, constants.CHERRY_TOPPING, constants.CENTER))

class ChocoBananaWaffle(FullCookedWaffle):
    def __init__(self):
        super().__init__("ChocoBananaWaffle",constants.CHOCOLATE_BATTER)
        self.add_criteria(ToppingCriteria(4, constants.CHOCOLATE_TOPPING, constants.OUTER,sided=True,side=constants.RIGHT))
        self.add_criteria(ToppingCriteria(4, constants.BANANA_TOPPING, constants.OUTER,sided=True,side=constants.LEFT))
        self.add_criteria(ToppingCriteria(4, constants.CHOCOLATE_TOPPING, constants.MIDDLE,sided=True,side=constants.RIGHT))
        self.add_criteria(ToppingCriteria(4, constants.BANANA_TOPPING, constants.MIDDLE,sided=True,side=constants.LEFT))
