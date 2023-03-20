import pygame
from random import choice

from utils.constants import *
from utils.qlearn_utils import get_spacing_from_dist, save_policy
from utils.simulation_utils import check_stop_game
from utils.counter import Counter

from state import State
from simulation import Simulation
from robots.learn_robot import LearnRobot

class QLearn(Simulation):
    def __init__(self):
        super().__init__()
        self.dt = 0
        self.last_time = pygame.time.get_ticks()

    # FOR EVERY ROBOT IN SWARM:
    # DO THE LEARNING INDIVIDUALLY






    @property
    def distances(self):
        return self.formation.get_distances()


    def update(self):
        # if not check_stop_game():
        #     break

        # Update clock
        self.dt = (pygame.time.get_ticks() - self.last_time)/1000
        self.last_time = pygame.time.get_ticks()

        # Update map
        self.gfx.map.blit(self.gfx.map_img, (0, 0))

        # ---------------------- Main ----------------------
        self.swarm.update_swarm(self.dt)
        self.gfx.update()
        pygame.display.update()
        self.formation.get_distances()


    def start(self):
        dt = 0
        last_time = pygame.time.get_ticks()

        while True:
            # Check for exit
            if check_stop_game():
                break

            # Update clock
            dt = (pygame.time.get_ticks() - last_time)/1000
            last_time = pygame.time.get_ticks()

            # Update map
            self.gfx.map.blit(self.gfx.map_img, (0, 0))

            # ---------------------- Main ----------------------
            self.swarm.update_swarm(dt)
            self.gfx.update()
            pygame.display.update()
            self.formation.get_distances()

        # make_plots(self.formation, self.swarm.robots)
