from utils.dimensions import *
from utils.constants import *
from utils.utils import ray_distance, _ro_ij, _p_ij_tilda, print_flag
from pygame import Vector2
import pygame
from utils.utils import get_color
from time import sleep

from .robot import Robot

class DistanceRobot(Robot):
    def __init__(self, game_map, startpos=None):
        super().__init__(game_map, startpos)
        self.name = "DistanceRobot"
        self.K = 2

    def set_wheel_speed(self):
        x_tot, y_tot = self.get_velocity()
        
        v_star = (self.minspeed-x_tot, self.minspeed-y_tot)
        self.speedL = v_star[0] 
        self.speedR = v_star[1]


    def get_velocity(self):
        tot_x = 0
        tot_y = 0
        for neigh in self.other_robots:
            ro = _ro_ij(self.position, neigh.position,
                        self.K, self.distances[neigh.id])
            pij = _p_ij_tilda(self.position, neigh.position)
            result = [n*ro for n in pij]
            res_x, res_y = result
            tot_x += res_x
            tot_y += res_y
        return tot_x, tot_y


    # robot velocity
    # linear and angular velocities of the robot in three-dimensional space
    # thetha = robot heading
    # v = (v * math.cos(self.heading), v * math.sin(self.heading), w)
    def kinematics(self, dt):
        L = self.w  # distance between the wheels (aka wheelbase)
        tot_x, tot_y = self.get_velocity()
        # linear velocity of the robot
        # average velocity of the robot based on the speeds of left and right wheels
        self.x += ((self.speedL + self.speedR) / 2 * math.cos(self.heading) - tot_x)* dt
        self.y -= ((self.speedL + self.speedR) / 2 * math.sin(self.heading) + tot_y) * dt

        # angular velocity of the robot
        if print_flag: print((self.speedR - self.speedL) / self.w * dt)
        self.heading += (self.speedR - self.speedL) / self.w * dt
        if self.heading > 2*math.pi or self.heading < -2*math.pi:
            self.heading = 0


    def update(self, dt):
        self.set_wheel_speed()
        self.kinematics(dt)
        self.store_distances()
