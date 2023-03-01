import pygame
import math
import sys
import numpy as np

from dimensions import *
from utils import *


class Graphics:
    def __init__(self, swarm, map, dimensions, robot_img_path, map_img_path):
        pygame.init()
        self.swarm = swarm
        self.robot_path = []

        # MAP
        # load imgs
        self.robot_img = pygame.image.load(robot_img_path)
        self.map_img = pygame.image.load(map_img_path)
        # dimensions
        self.robot_img = pygame.transform.scale(self.robot_img, ROBOT_SIZE)
        self.map_img = pygame.transform.scale(self.map_img, (dimensions))
        self.h, self.w = dimensions[1], dimensions[0]
        # window settings
        pygame.display.set_caption("Obstacle Avoidance")
        self.map = map
        self.map.blit(self.map_img, (0, 0))


    def update_robot(self, robot):
        rotated = pygame.transform.rotozoom(self.robot_img, math.degrees(robot.heading), 1)
        rect = rotated.get_rect(center=robot.position)
        self.map.blit(rotated, rect)    

    def update_senors(self, robot):
        if robot.name == "DistanceRobot":
            return
        for ray in robot.sensors_rays:
            if ray == [sys.maxsize, sys.maxsize]:
                continue
            pygame.draw.circle(self.map, get_color("red"), ray, 3, 0)
            pygame.draw.line(self.map, get_color("red"), robot.position, ray)
            pygame.draw.circle(self.map, get_color("yellow"),
                               robot.position, sensor_dist, 1)

    def draw_robot_path(self, robot):
        for point in robot.path:
            pygame.draw.circle(self.map, get_color("red"), point, 1, 0)

    def draw_trajectory(self,robot):
        pygame.draw.line(self.map, get_color("green"), robot.trajectory.start, robot.trajectory.end)

    def update(self):
        for robot in self.swarm:
            self.draw_trajectory(robot)
            self.update_robot(robot)
            self.update_senors(robot)
            self.draw_robot_path(robot)
            robot.path.append(robot.position)