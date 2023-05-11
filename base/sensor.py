import pygame
import math
import sys 
import numpy as np
from utils.utils import *
from utils.dimensions import *

class Ultrasonic:
    def __init__(self, sensor_range, map):
        self.sensor_distance = sensor_range[0]
        self.sensor_range = sensor_range[1]
        self.map = map
        self.map_width, self.map_height = pygame.display.get_surface().get_size()
        self.n_rays = n_rays

    def sense_obstacles(self, x, y, heading):
        obstacles = [[sys.maxsize, sys.maxsize]] * self.n_rays
        collision = [False] * self.n_rays
        x1, y1, = x, y 
        start_angle = heading - self.sensor_range
        finish_angle = heading + self.sensor_range
        for id, angle in enumerate(np.linspace(start_angle, finish_angle, self.n_rays, True)):
            x2 = x1 + self.sensor_distance * math.cos(angle)
            y2 = y1 - self.sensor_distance * math.sin(angle)
            for i in range(0,100):
                u = i/100
                x = int(x2 * u + x1 * (1-u))
                y = int(y2 * u + y1 * (1-u))
                if 0 < x < self.map_width and 0 < y < self.map_height:
                    # Collision detection
                    # For each ray, check if it is colliding with something
                    if i <= collision_distance:
                        collision_color = self.map.get_at((x, y))
                        collision[id] = True if (collision_color[0],
                                                 collision_color[1],
                                                 collision_color[2]) == get_color("black") else False
                    # Normal distance
                    color = self.map.get_at((x,y))
                    self.map.set_at((x,y), (0,208,255))
                    if (color[0], color[1], color[2]) == get_color("black"):
                        obstacles[id] = [x,y]
                        break
        return obstacles, collision
