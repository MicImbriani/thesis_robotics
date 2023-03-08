from utils.dimensions import *
from utils.constants import *
from utils.utils import _ro_ij, _p_ij_tilda
from pygame import Vector2
from utils.utils import get_color
from time import sleep
from numpy.matlib import cross
from math import sin, cos

from .robot import Robot

class DistanceRobot(Robot):
    def __init__(self, game_map, startpos=None):
        super().__init__(game_map, startpos)
        self.name = "DistanceRobot"
        self.K = 2

    def compute_wheel_vel(self):
        l_speed, r_speed = self.get_velocity()
        self.speedR = l_speed
        self.speedL = r_speed
        self.x2 = self.x
        self.y2 = self.y

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
        tot_x, tot_y = self.get_velocity()
        # linear velocity of the robot
        # average velocity of the robot based on the speeds of left and right wheels
        Mx = [[sin(self.heading) + cos(self.heading), sin(self.heading) - cos(self.heading)],
              [sin(self.heading) - cos(self.heading), sin(self.heading) + cos(self.heading)]]
        print("MX", Mx)
        result = cross(Mx, [tot_x,tot_y]) 
        v = (self.speedL + self.speedR) / 2
        vx = (v * math.cos(self.heading) - result[0]) * dt 
        vy = (v * math.sin(self.heading) - result[1]) * dt
        print([vx, vy])
        # print("RESULT:",result)
        self.x += vx 
        self.y -= vy

        # angular velocity of the robot
        L = self.w  # distance between the wheels (aka wheelbase)
        self.heading += (self.speedR - self.speedL) / L * dt
        if self.heading > 2*math.pi or self.heading < -2*math.pi:
            self.heading = 0

    def update(self, dt):
        self.compute_wheel_vel()
        self.kinematics(dt)
        self.store_distances()
