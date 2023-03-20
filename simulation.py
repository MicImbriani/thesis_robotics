import pygame
from time import sleep
import matplotlib.pyplot as plt

from utils.dimensions import *
from utils.simulation_utils import check_stop_game, make_plots

from robots.robot import Robot
from robots.distance_robot import DistanceRobot
from robots.learn_robot import LearnRobot
from robots.swarm import Swarm
from graphics import Graphics
from formation import Formation




class Simulation:
    def __init__(self):
        # MAP
        self.map = pygame.display.set_mode(MAP_SIZE)

        # ROBOTS
        self.robot1 = DistanceRobot(self.map)
        self.robot2 = Robot(self.map)
        self.robot3 = DistanceRobot(self.map)
        # self.robot4 = DistanceRobot(self.map)
        self.swarm = Swarm(
            [self.robot1, self.robot2, self.robot3])

        # TRAJECTORY/ FORMATION
        self.formation = Formation("triangle", self.swarm.robots, self.swarm.ids)
        self.end_coord = self.swarm.get_end_mid_point(self.formation.end_middle_coordinate)

        # GRAPHICS
        self.gfx = Graphics(self.swarm.robots, self.map, MAP_SIZE, './sprites/robot.png', './sprites/MAP_empty.png', self.formation.end_middle_coordinate)


    def run(self):
        dt = 0
        last_time = pygame.time.get_ticks()

        while True:
            # Check for exit
            if not check_stop_game():
                break

            # Update clock
            dt = (pygame.time.get_ticks() - last_time)/1000
            last_time = pygame.time.get_ticks()

            # Update map
            self.gfx.map.blit(self.gfx.map_img, (0,0))


            # ---------------------- Main ----------------------
            self.swarm.update_swarm(dt)
            self.gfx.update()
            pygame.display.update()
            self.formation.get_distances()

        # make_plots(self.formation, self.swarm.robots)
