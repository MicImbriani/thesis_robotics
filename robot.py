import pygame 
import math
from time import sleep
from numpy import dot, cross

from dimensions import *
from constants import *
from utils import *
from utils import _ro_ij, _p_ij_tilda

from sensor import Ultrasonic

class Robot:
    def __init__(self, game_map, startpos=None):
        # robot dims 
        self.w = robot_width
        self._m2p = 3779.52 #meters -> pixels
        self.flag = False

        # start positions
        if startpos:
            self.x, self.y = startpos[0], startpos[1]
        else:
            self.x, self.y = 0, 0
        self.heading = 0
        self.path = []
        self.trajectory = None

        # speeds in m/s
        self.speedL = 0.01 * self._m2p
        self.speedR = 0.01 * self._m2p
        self.maxspeed = 0.02 * self._m2p
        self.minspeed = 0.01 * self._m2p
        self.K = 0.4

        # SENSORS
        self.sensor = Ultrasonic(sensor_range, game_map)
        # Obstalce logic
        self.min_obstalce_distance = sensor_dist

    @property
    def position(self):
        return (self.x, self.y)

    @property
    def direction(self):
        return get_direction(self.heading)

    def avoid_obstacles(self, collision, dt):
        if self.flag == False:
            l_speed, r_speed = self.compute_wheel_vel(self.sensors_rays, collision)
        else:
            l_speed, r_speed = self.get_velocity()
            print("L_SPEED", l_speed)
            print("R_SPEED", r_speed)
        self.speedR = l_speed
        self.speedL = r_speed

    def compute_wheel_vel(self, sensors, collisions):
        correction = list(map(lambda x: ray_distance(x, self.position, self.min_obstalce_distance), sensors))
        l2, l1, m, r1, r2 = correction
        correction = l2 + 2*l1 + 8.5*m - 2*r1 - r2
        correction = correction / 100000
        left_collide, mid_collide, right_collide = self.prevent_collision(collisions)
        left_wheel_velocity = self.minspeed + correction if not left_collide else 0
        right_wheel_velocity = self.minspeed - correction if not right_collide else 0
        return left_wheel_velocity, right_wheel_velocity

    def prevent_collision(self, collision):
        left_collide = True if True in collision[:2] else False
        right_collide = True if True in collision[3:] else False
        mid_collide = True if collision[2] else False
        return left_collide, mid_collide, right_collide
            

    def kinematics(self, dt):
        self.x += ((self.speedL + self.speedR)/2) * math.cos(self.heading) * dt
        self.y -= ((self.speedL + self.speedR)/2) * math.sin(self.heading) * dt
        self.heading += (self.speedR - self.speedL) / self.w * dt
        # print(self.heading)
        if self.heading > 2*math.pi or self.heading< -2*math.pi:
            self.heading = 0

    def get_velocity(self):
        v_star = self.minspeed, self.minspeed, self.minspeed
        tot_x = 0
        tot_y = 0
        tot_z = 0
        for neigh in self.other_robots:
            result = cross(_ro_ij(self.position, neigh.position, self.K, self.distances[neigh.id]),
                         _p_ij_tilda(self.position, neigh.position))
            print("RESULT", result)
            res_x, res_y, res_z = result
            tot_x += res_x 
            tot_y += res_y
            tot_z += res_z
        v_i = v_star[0] - tot_x, v_star[1] - tot_y, v_star[2] - tot_z
        print(v_i)
        return v_i[0], v_i[2]


    def get_vy_star(self):
        # get Vx (current X coord of robot)
        # compute Vy (ideal y coord of robot if it were following trajectory)
        vx = self.x 
        # vy_star = self.

    def update(self, dt):
        self.sensors_rays, collision = self.sensor.sense_obstacles(self.x, self.y, self.heading)
        self.avoid_obstacles(collision, dt)
        self.kinematics(dt)
        self.get_velocity()
