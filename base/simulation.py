import pygame
from math import sqrt
from time import sleep
import matplotlib.pyplot as plt

from utils.dimensions import *
from utils.utils import distance
from utils.simulation_utils import check_stop_game, make_plots

from robots.robot import Robot
from robots.distance_robot import DistanceRobot
from robots.learn_robot import LearnRobot
from robots.swarm import Swarm
from graphics import Graphics
from formation import Formation




class Simulation:
    def __init__(self):
        self.setup_swarm()
        self.setup_simulation()
        r1, r2, r3 = [robot.position for robot in self.swarm]
        self.base_formation_area = self.compute_triangle_area(r1, r2, r3)
        self.all_form_areas = []


    def setup_swarm(self):
        # MAP
        self.map = pygame.display.set_mode(MAP_SIZE)

        # ROBOTS
        self.robot1 = DistanceRobot(self.map)
        self.robot2 = Robot(self.map)
        self.robot3 = DistanceRobot(self.map)
        # self.robot4 = DistanceRobot(self.map)
        self.swarm = Swarm(
            [self.robot1, self.robot2, self.robot3])

    def setup_simulation(self):
        # TRAJECTORY/ FORMATION
        self.formation = Formation(
            "triangle", self.swarm.robots, self.swarm.ids)
        self.swarm.set_formation(self.formation)
        self.end_coord = self.swarm.get_end_mid_point(
            self.formation.end_middle_coordinate)

        # GRAPHICS
        self.gfx = Graphics(self.swarm.robots, self.map, MAP_SIZE, './sprites/robot.png',
                            './sprites/MAP.png', self.formation.end_middle_coordinate)

    def update(self, tick):
        # Check for exit
        while not check_stop_game():

            # Update clock
            dt = (pygame.time.get_ticks() - tick)/1000
            tick = pygame.time.get_ticks()

            # Update map
            self.gfx.map.blit(self.gfx.map_img, (0, 0))

            # ---------------------- Main ----------------------
            self.swarm.update_swarm(dt)
            self.gfx.update()
            pygame.display.update()
            self.formation.get_distances()
            self.all_form_areas.append(self.formation_disruption())

    def run(self):
        tick = pygame.time.get_ticks()

        for robot in self.swarm:
            if robot.name == "LearnRobot":
                robot.init_state()

        self.update(tick)

    def compute_triangle_area(self, p1, p2, p3):
        l1 = distance(p1, p2)
        l2 = distance(p2, p3)
        l3 = distance(p1, p3)
        s = (l1 + l2 + l3) / 2
        return sqrt(abs(s * (s-l1)*(s-l2)*(s-l3)))
    
    def formation_disruption(self):
        r1, r2, r3 = [robot.position for robot in self.swarm]
        return abs(self.compute_triangle_area(r1, r2, r3) - self.base_formation_area)
