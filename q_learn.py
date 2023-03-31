import pygame
from random import choice, uniform

from utils.constants import *
from utils.qlearn_utils import get_spacing_from_dist, save_policy
from utils.simulation_utils import check_stop_game
from utils.counter import Counter

from state import State
from simulation import Simulation
from robots.learn_robot import LearnRobot

class QLearn(Simulation):
    def __init__(self, alpha, gamma, rho, nu):
        super().__init__()
        self.dt = 0
        self.last_time = pygame.time.get_ticks()
        # Q-learn params
        self.alpha = alpha
        self.gamma = gamma
        self.rho = rho
        self.nu = nu

    # FOR EVERY ROBOT IN SWARM:
    # DO THE LEARNING INDIVIDUALLY

    def q_learning(self, iterations):
        state = self.last_state
        current_distances = self.formation.get_distances()
        dists_to_endpoint = self.formation.dist_to_end_poit()
        problem = self.swarm

        rand_nu = uniform(0, 1)
        # TODO: maybe make method for computing state?
        if rand_nu < self.nu or state is None:
            state = problem.getRandomState()

        for robot in self.swarm:
            if state is None:
                state = robot.get_state()
            # Get all possible actions
            possible_actions = robot.get_legal_actions()
            # (Explore vs Exploit)
            rand_rho = uniform(0, 1)
            action = choice(possible_actions) if rand_rho < self.exploration_rho\
                else robot.get_action(state, possible_actions)

            robot.take_next_action(action, self.dt)
            reward = robot.compute_reward(current_distances[robot.id], dists_to_endpoint[robot.id])
            new_state = robot.get_new_state()

            Q = robot.get_Q_value(state, action)
            maxQ = robot.get_max_Q(new_state, ALL_ACTIONS)
            new_Q = (1 - self.alpha) * Q + self.alpha * (reward + self.gamma * maxQ - Q)
            robot.update_Q(state, action, new_Q)

            self.last_state = new_state


    @property
    def distances(self):
        return self.formation.get_distances()


    def update(self):
        while not check_stop_game():
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

        # Check for exit
        if check_stop_game():
            return

        # Update clock
        dt = (pygame.time.get_ticks() - last_time)/1000
        last_time = pygame.time.get_ticks()

        # Update map
        self.gfx.map.blit(self.gfx.map_img, (0, 0))

        # ---------------------- Main ----------------------
        self.q_learning()
        self.swarm.update_swarm(dt)
        self.gfx.update()
        pygame.display.update()
        self.formation.get_distances()
        
        # Start training
        self.update()

        # make_plots(self.formation, self.swarm.robots)
