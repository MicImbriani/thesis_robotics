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

DIRECTIONS = [STRAIGHT, UP, UP_RIGHT,RIGHT,DOWN_RIGHT, DOWN, DOWN_LEFT,LEFT,UP_LEFT]

ACCELERATE = 1
DECELERATE = -1

ALL_ACTIONS = [LEFT, RIGHT, STRAIGHT, ACCELERATE, DECELERATE]
