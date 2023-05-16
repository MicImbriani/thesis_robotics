print_flag = False


STRAIGHT =      {"coord": (0, 0),   "name": "STRAIGHT"}
UP =            {"coord":(0,-1),    "name": "UP"}
UP_RIGHT =      {"coord":(1,-1),    "name": "UP_RIGHT"}
RIGHT =         {"coord":(1,0),     "name": "RIGHT"}
DOWN_RIGHT =    {"coord":(1,1),     "name": "DOWN_RIGHT"}
DOWN =          {"coord":(0,1),     "name": "DOWN"}
DOWN_LEFT =     {"coord":(-1,1),    "name": "DOWN_LEFT"}
LEFT =          {"coord":(-1,0),    "name": "LEFT"}
UP_LEFT =       {"coord":(-1,-1),   "name": "UP_LEFT"}

STRAIGHT =      (0, 0)
UP =            (0,-1)
UP_RIGHT =      (1,-1)
RIGHT =         (1,0)
DOWN_RIGHT =    (1,1)
DOWN =          (0,1)
DOWN_LEFT =     (-1,1)
LEFT =          (-1,0)
UP_LEFT =       (-1,-1)


# STRAIGHT =  "0"
STRAIGHT_RIGHT = "1"
STRAIGHT_LEFT  ="2"
# RIGHT = "3"
# LEFT =  "7"
BEHIND_RIGHT =  "4"
BEHIND =    "5"
BEHIND_LEFT =   "6"


ACCELERATE = 1
DECELERATE = -1


GLOBAL_DIRECTIONS = [UP, UP_LEFT, LEFT, DOWN_LEFT, DOWN, DOWN_RIGHT, RIGHT, UP_RIGHT]
LOCAL_DIRECTIONS = [BEHIND, BEHIND_RIGHT, RIGHT, STRAIGHT_RIGHT, STRAIGHT, 
                    STRAIGHT_LEFT, LEFT, BEHIND_LEFT]

local_dir_LUT = {}

ALL_ACTIONS = [LEFT, RIGHT, STRAIGHT, ACCELERATE, DECELERATE, UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT]

IN_RANGE = "IN RANGE"
TOO_FAR = "TOO FAR"
TOO_CLOSE = "TOO CLOSE"
