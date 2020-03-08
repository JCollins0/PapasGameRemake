class Constants:
    def __init__(self):
        # Game Basic Constants
        self.SCREEN_HEIGHT = 750
        self.SCREEN_WIDTH = 1000
        self.FONT_SIZE = 32
        self.FONT_SIZE_SMALL = 16
        self.TEXT_CENTERED = 0x1

        # Order Constants
        self.CRITERIA_IMAGE_WIDTH = 210
        self.CRITERIA_IMAGE_HEIGHT = 50

        # Customer Constants
        self.MAX_WAIT_TIME_NORMAL = 120
        self.MAX_WAIT_TIME_PICKY = 80
        self.MAX_WAIT_TIME_LENIENT = 160

        # Cook Constants
        self.BATTER_ICON_SIZE = 25
        self.WAFFLE_MAKER_SIZE = 200
        self.COOK_METER_WIDTH = 20
        self.MAX_COOK_TIME = 40
        self.FROZEN_TIME = 0
        self.UNDERCOOKED_TIME = self.MAX_COOK_TIME //  4
        self.MEDIUM_COOOKED_TIME = self.MAX_COOK_TIME // 2
        self.COOKED_WELL_TIME = (self.MAX_COOK_TIME// 4) * 3
        self.BURNT_TIME = self.MAX_COOK_TIME
        self.BATTER_OUTLINE_WIDTH = 3
        # Build Constants
        self.WAFFLE_EDITOR_WIDTH = 400
        self.WAFFLE_EDITOR_HEIGHT = 400
        self.CENTER_RADIUS = .25
        self.MIDDLE_RADIUS = .55
        self.BIG_WAFFLE_WIDTH = 360
        self.BIG_WAFFLE_HEIGHT = 360

        # Batter Constants
        self.BANANA_BATTER = "bananabatter"
        self.BLUEBERRY_BATTER = "blueberrybatter"
        self.BUTTER_BATTER = "butterbatter"
        self.CHERRY_BATTER = "cherrybatter"
        self.CHOCOLATE_BATTER = "chocolatebatter"
        self.PUMPKIN_BATTER = "pumpkinbatter"
        self.RAINBOW_BATTER = "rainbowbatter"
        self.DUMP_BATTER = "dumpbatter"

        #Topping Constants
        self.TOPPING_SIZE = 50
        self.TOPPING_BIN_WIDTH = 63
        self.TOPPING_BIN_HEIGHT = 50
        self.CHOCOLATE_TOPPING="chocolatechip"
        self.CHERRY_TOPPING="cherry"
        self.RAZZBERRY_TOPPING="razzberry"
        self.STRAWBERRY_TOPPING="strawberry"
        self.BANANA_TOPPING="banana"
        self.PEPPERMINT_TOPPING="peppermint"
        self.BUTTER_TOPPING="butter"
        self.BACON_TOPPING="bacon"

        self.TOP = "T"
        self.BOTTOM = "B"
        self.LEFT = "L"
        self.RIGHT = "R"
        self.WHOLE = "W"
        self.OUTER = "O"
        self.MIDDLE = "M"
        self.CENTER = "C"
        self.JUDGE_TOPPING_DIFFERENT_AMOUNT_PENALTY = 10
        self.JUDGE_TOPPING_ANGLE_NOT_EQUAL_PENALTY = 10
        self.JUDGE_TOPPING_ANGLE_SIDED_LENIENCY = 250
        self.JUDGE_TOPPING_ANGLE_LENIENCY = 10 # degrees
        self.JUDGE_TOPPING_EXTRA_TOPPING_PENALTY = 20 # degrees
        self.JUDGE_MISSING_TOPPINGS_PENALTY = 50
