import pygame
from random import choice, uniform

from utils.constants import *
from utils.dimensions import *
from utils.qlearn_utils import get_spacing_from_dist, save_policy
from utils.simulation_utils import check_stop_game
from utils.counter import Counter

from state import State
from simulation import Simulation
from robots.learn_robot import LearnRobot
from robots.swarm import Swarm
from graphics import Graphics
from formation import Formation


class QLearn(Simulation):
    def __init__(self, alpha, gamma, rho, nu):
        super().__init__()
        # Q-learn params
        self.alpha = alpha
        self.gamma = gamma
        self.exploration_rho = rho
        self.nu = nu

    def setup_swarm(self):
        # MAP
        self.map = pygame.display.set_mode(MAP_SIZE)

        # ROBOTS
        self.robot1 = LearnRobot(self.map)
        self.robot2 = LearnRobot(self.map)
        self.robot3 = LearnRobot(self.map)
        # self.robot4 = DistanceRobot(self.map)
        self.swarm = Swarm(
            [self.robot1, self.robot2, self.robot3])


    # The q-learning step
    def q_learning(self, dt):
        current_distances = self.formation.get_distances()
        dists_to_endpoint = self.formation.dist_to_end_poit()

        # rand_nu = uniform(0, 1)
        # # TODO: maybe make method for computing state?
        # if rand_nu < self.nu or state is None:
        #     state = problem.getRandomState()

        for robot in self.swarm:
            state = robot.last_state
            if state is None:
                state = robot.get_state()
            # Get all possible actions
            possible_actions = robot.get_legal_actions()
            # (Explore vs Exploit)
            rand_rho = uniform(0, 1)
            if rand_rho < self.exploration_rho:
                print("POSSIBLE", possible_actions)
                action = choice(possible_actions)
            else:
                action = robot.get_action(state, possible_actions)

            # Take action and get reward and next state
            robot.take_next_action(action, dt)
            reward = robot.compute_reward(current_distances[robot.id], dists_to_endpoint[robot.id])
            new_state = robot.get_new_state(current_distances[robot.id])

            # Update Q-table
            Q = robot.get_Q_value(state, action)
            maxQ = robot.get_max_Q(new_state, ALL_ACTIONS)
            new_Q = (1 - self.alpha) * Q + self.alpha * (reward + self.gamma * maxQ - Q)
            robot.update_Q(state, action, new_Q)

            # Set state for next iteration
            robot.last_state = new_state


    @property
    def distances(self):
        return self.formation.get_distances()


    def update(self, tick):
        while not check_stop_game():  
            # Update clock
            dt = (pygame.time.get_ticks() - tick)/1000
            tick = pygame.time.get_ticks()

            # Update map
            self.gfx.map.blit(self.gfx.map_img, (0, 0))

            # ---------------------- Main ----------------------
            self.q_learning(dt)
            self.swarm.update_swarm(dt)
            self.gfx.update()
            pygame.display.update()
            self.formation.get_distances()


    def run(self):
        tick = pygame.time.get_ticks()

        for robot in self.swarm:
            robot.init_state()


        # First iteration update
        # Update clock
        dt = (pygame.time.get_ticks() - tick)/1000
        tick = pygame.time.get_ticks()

        # Update map
        self.gfx.map.blit(self.gfx.map_img, (0, 0))

        # ---------------------- Main ----------------------
        self.q_learning(dt)
        self.swarm.update_swarm(dt)
        self.gfx.update()
        pygame.display.update()
        self.formation.get_distances()
        
        self.update(tick)
        
