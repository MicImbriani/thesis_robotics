from random import choice
from numpy import array, add
from math import cos, sin
from time import time as get_seconds

from utils.constants import *
from utils.utils import get_direction

from .robot import Robot

class LearnRobot(Robot):
    def __init__(self, game_map, startpos=None):
        super().__init__(game_map, startpos)
        self.name = "LearnRobot"
        self.timer = int(get_seconds()) + 3

    def move_in_direction(self, direction) -> dict:
        new_direction = add(array(self.current_direction['coord']), 
                            array(direction['coord']))
        return get_direction(new_direction)
    
    def accelerate(self):
        return self.speedL*10, self.speedR*10
    
    def decelerate(self):
        return self.speedL/2, self.speedR/2

    def update(self, dt):
        new_dir = self.move_in_direction(choice([STRAIGHT, RIGHT, LEFT]))
        if int(get_seconds()) == self.timer:
            print(dir_coord)
            dir_coord = new_dir['coord']
            new_speedL, new_speedR = dir_coord[0]*self.minspeed, dir_coord[1]*self.minspeed
            self.speedL += new_speedL
            self.speedR += new_speedR
            self.timer = int(get_seconds()) + 3

        # print("TIMER", self.timer)
        # if int(get_seconds()) == self.timer:
        #     new_dir = choice([STRAIGHT, RIGHT, LEFT])
        #     if new_dir == STRAIGHT:
        #         self.heading = 0
        #     elif new_dir == RIGHT:
        #         self.heading = 3.14
        #     elif new_dir == LEFT:
        #         self.heading = 5
        #     self.timer = int(get_seconds()) + 1


        v = (self.speedL + self.speedR) / 2

        # equation space-time-velocity
        # S(t) = S(t-1) + k*v(t)
        self.x += v * cos(self.heading) * dt
        self.y -= v * sin(self.heading) * dt
