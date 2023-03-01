from dimensions import *
from constants import *
from utils import ray_distance, _ro_ij, _p_ij_tilda
from pygame import Vector2
import pygame
from utils import get_color
from time import sleep

from .robot import Robot

class DistanceRobot(Robot):
    def __init__(self, game_map, startpos=None):
        super().__init__(game_map, startpos)
        self.name = "DistanceRobot"
        self.K = 2

    def compute_wheel_vel(self):
        l_speed, r_speed = self.get_velocity()
        print("L_SPEED", l_speed)
        print("R_SPEED", r_speed)
        self.speedR = l_speed
        self.speedL = r_speed
        self.x2 = self.x
        self.y2 = self.y

    def get_velocity(self):
        tot_x = 0
        tot_y = 0
        for neigh in self.other_robots:
            print(neigh.id)
            ro = _ro_ij(self.position, neigh.position,
                        self.K, self.distances[neigh.id])
            pij = _p_ij_tilda(self.position, neigh.position)
            result = [n*ro for n in pij]
            # result = cross(_ro_ij(self.position, neigh.position, self.K, self.distances[neigh.id]),
            #              _p_ij_tilda(self.position, neigh.position))
            # print("RESULT", result)
            res_x, res_y = result
            tot_x += res_x
            tot_y += res_y
        # sleep(10)
        print("TOTALLLLL", tot_x, tot_y)
        return tot_x, tot_y

    def get_vy_star(self):
        # linear velocity of the robot
        # average velocity of the robot based on the speeds of left and right wheels
        v = (self.speedL + self.speedR) / 2
        # angular velocity of the robot
        L = self.w  # distance between the wheels (aka wheelbase)
        w = (self.speedR - self.speedL) / L

        # robot velocity
        # linear and angular velocities of the robot in three-dimensional space
        # thetha = robot heading
        v = (v * math.cos(self.heading), v * math.sin(self.heading), w)

    def kinematics(self, dt):
        tot_x, tot_y = self.get_velocity()
        v = (self.speedL + self.speedR) / 2
        self.x += (v * math.cos(self.heading) - tot_x) * dt
        self.y += (v * math.sin(self.heading) - tot_y) * dt
        # vec.normalize_ip()
        # print("VECTOR", vec)
        # print()

        # pygame.draw.line(self.game_map, get_color("red"), 
        #                  (100,100), 
        #                  (vec[0]+100,vec[1]+100))
        
        self.heading += (self.speedR - self.speedL) / self.w * dt
        if self.heading > 2*math.pi or self.heading < -2*math.pi:
            self.heading = 0

    def update(self, dt):
        self.compute_wheel_vel()
        self.kinematics(dt)