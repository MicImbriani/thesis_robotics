from random import choice
from numpy import array, add
from math import cos, sin
from time import time as get_seconds

from utils.constants import *
from utils.utils import get_direction_from_dir, get_direction_from_heading, get_relative_directions, get_heading_from_direction
from utils.qlearn_utils import in_correct_direction, get_spacing_from_dist

from state import State
from .robot import Robot

class LearnRobot(Robot):
    def __init__(self, game_map, startpos=None):
        super().__init__(game_map, startpos)
        self.name = "LearnRobot"
        self.timer_step = 1
        self.timer = get_seconds() + self.timer_step
        self.history = [self.position]



    def update(self, dt):
        if get_seconds() >= self.timer:
            new_dir = self.get_new_direction(choice([LEFT]))
            # new_speedL, new_speedR = direction_coord[0]*self.minspeed, direction_coord[1]*self.minspeed
            # self.speedL += new_speedL
            # self.speedR += new_speedR

            # HARDCODED HEADING CHANGE
            self.heading = get_heading_from_direction(new_dir)

            # Add current position to the history of robot's positions
            self.history.append(self.position)
            # Check if it's going in right direction
            print(in_correct_direction(self.path, self.end_mid_point))

            self.timer = get_seconds() + self.timer_step

        v = (self.speedL + self.speedR) / 2
        # equation space-time-velocity
        # S(t) = S(t-1) + k*v(t)
        self.x += v * cos(self.heading) * dt
        self.y -= v * sin(self.heading) * dt


    @property
    def current_direction(self):
        return get_direction_from_heading(self.heading)


    
    def set_action(self, action):
        if action in self._get_legal_actions():
            self.next_action = action
            return True
        return False


    def _get_legal_actions(self):
        # Returns a list of legal actions
        # Accelerate and decellerate are always legal
        left = self.collisions[0] and self.collisions[1]
        right = self.collisions[3] and self.collisions[4]
        mid = self.collisions[2]
        # Basicalli zips [LEFT, RIGHT, STRAIGHT] with [left sensors, right sensors, mid sensor]
        return [action for action, is_legal in zip(available_actions[:3], [left,right,mid]) if is_legal]
    


    def get_new_direction(self, turn) -> dict:
        """ 
        Given the relative direction in which the robot should turn, 
        computes the absolute direction in which the robot should go.
        Thresholding the values is needed bcos all directions have max 
        value of 1.
        """
        relative_direction = get_relative_directions(self.current_direction, turn)
        new_direction = add(array(self.current_direction['coord']), 
                    array(relative_direction['coord']))
        def treshold(x):
            sign = 1 if x >= 0 else -1
            return 1*sign if x > 1 or x < -1 else x
        new_direction = list(map(treshold, new_direction))
        return get_direction_from_dir((new_direction[0], new_direction[1]))


    def accelerate(self):
        self.speedL *= 10
        self.speedR *= 10


    def decelerate(self):
        self.speedL /= 2
        self.speedR /= 2

    def get_distance_to_robots(self):
        return get_spacing_from_dist(self.distances_log)


    def get_state(self) -> State:
        s = State(self.id, self.other_robots, self.dists)
        return s.get_state()