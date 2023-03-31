import pygame 
import math
from time import sleep
from numpy import dot, cross

from utils.dimensions import *
from utils.constants import *
from utils.utils import *
from utils.utils import _ro_ij, _p_ij_tilda

from sensor import Ultrasonic

class Robot:
    def __init__(self, game_map, startpos=None):
        # robot dims 
        self.name = "Robot"
        self.w = robot_width
        self._m2p = 3779.52 #meters -> pixels
        self.game_map = game_map

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

        # SWARM


    @property
    def position(self):
        return (self.x, self.y)

    def compute_wheel_vel(self, sensors_rays, collisions):
        l_speed, r_speed = self.avoid_obstacles(sensors_rays, collisions)
        self.speedR = l_speed
        self.speedL = r_speed

    def avoid_obstacles(self, sensors, collisions):
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
        # linear velocity of the robot
        # average velocity of the robot based on the speeds of left and right wheels
        v = (self.speedL + self.speedR) / 2

        # equation space-time-velocity
        # S(t) = S(t-1) + k*v(t)
        self.x += v * math.cos(self.heading) * dt
        self.y -= v * math.sin(self.heading) * dt

        # angular velocity of the robot
        L = self.w # distance between the wheels (aka wheelbase)
        self.heading += (self.speedR - self.speedL) / self.w * dt
        if self.heading > 2*math.pi or self.heading< -2*math.pi:
            self.heading = 0

    def store_distances(self):
        for neigh in self.other_robots:
            self.distances_log[neigh.id].append(distance(self.position, neigh.position))

    def _sense_obstacles(self):
        # returns: sensors_rays, collisions
        return self.sensor.sense_obstacles(self.x, self.y, self.heading)

    def update(self, dt):
        sensor_rays, collisions = self._sense_obstacles()
        self.compute_wheel_vel(sensor_rays, collisions)
        self.kinematics(dt)
        self.store_distances()
