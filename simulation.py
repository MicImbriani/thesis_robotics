import pygame
from time import sleep
import matplotlib.pyplot as plt

from utils.dimensions import *
from utils.utils import check_stop_game, get_distances_log

from robots.robot import Robot
from robots.robot_distance import DistanceRobot
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
        # robot4 = DistanceRobot(self.map)
        self.swarm = Swarm([self.robot1, self.robot2, self.robot3])

        # TRAJECTORY/ FORMATION
        self.formation = Formation("triangle", self.swarm)

        # GRAPHICS
        self.gfx = Graphics(self.swarm.robots, self.map, MAP_SIZE, './sprites/robot.png', './sprites/MAP_empty.png')


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


    def make_plots(self):
        distances = self.formation.dists
        distances_log = get_distances_log(self.swarm.robots)
        r01 = distances_log[0][1]
        r02 = distances_log[0][2]
        r12 = distances_log[1][2]
        length = len(r01)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.plot(range(length), [val-distances[(0,1)] for val in r01], color='tab:blue')
        ax.plot(range(length), [val-distances[(0,2)] for val in r02], color='tab:green')
        ax.plot(range(length), [val-distances[(1,2)] for val in r12], color='tab:red')

        plt.savefig("lol.png")