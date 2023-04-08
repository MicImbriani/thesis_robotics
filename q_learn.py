import pygame
from math import sqrt
from random import choice, uniform
from time import time as get_seconds

from utils.constants import *
from utils.dimensions import *
from utils.utils import distance
from utils.simulation_utils import check_stop_game

from formation import Formation
from simulation import Simulation
from robots.swarm import LearnSwarm
from robots.learn_robot import LearnRobot


class QLearn(Simulation):
    def __init__(self, alpha, gamma, rho, nu):
        self.setup_swarm()
        self.setup_simulation()
        self.timer_step = 0.05 / training_speed
        self.timer = get_seconds() + self.timer_step
        # Q-learn params
        self.alpha = alpha
        self.gamma = gamma
        self.exploration_rho = rho
        self.nu = nu

        # Learning worlds info
        self.total_formation_disruption = 0

    def setup_swarm(self):
        # MAP
        self.map = pygame.display.set_mode(MAP_SIZE)

        # ROBOTS
        self.robot1 = LearnRobot(self.map)
        self.robot2 = LearnRobot(self.map)
        self.robot3 = LearnRobot(self.map)
        # self.robot4 = DistanceRobot(self.map)
        self.swarm = LearnSwarm(
            [self.robot1, self.robot2, self.robot3])

    def setup_simulation(self):
        # TRAJECTORY/ FORMATION
        self.formation = Formation(
            "triangle", self.swarm.robots, self.swarm.ids)
        self.swarm.set_formation(self.formation)
        self.swarm.set_base_formation_area()
        self.end_coord = self.swarm.get_end_mid_point(
            self.formation.end_middle_coordinate)


    # The q-learning step
    def q_learning(self, dt):
        current_distances = self.formation.get_distances()
        dists_to_endpoint = self.formation.dist_to_end_poit()

        # rand_nu = uniform(0, 1)
        # # TODO: maybe make method for computing state?
        # if rand_nu < self.nu or state is None:
        #     state = problem.getRandomState()

        for robot in self.swarm.robots:
            state = robot.last_state
            # if state is None:
            #     state = robot.get_state()
            # Get all possible actions
            possible_actions = robot.get_legal_actions()
            # (Explore vs Exploit)
            rand_rho = uniform(0, 1)
            action =  STRAIGHT#choice(possible_actions)
            # if rand_rho < self.exploration_rho:
            #     action = choice(possible_actions)
            # else:
            #     action = robot.get_action(state, possible_actions)

            # Take action and get reward and next state
            robot.take_next_action(action)
            reward = robot.compute_reward(current_distances[robot.id], dists_to_endpoint[robot.id])
            new_state = robot.get_new_state(current_distances[robot.id])

            # Update Q-table
            Q = robot.get_Q_value(state, action)
            maxQ = robot.get_max_Q(new_state, ALL_ACTIONS)
            new_Q = (1 - self.alpha) * Q + self.alpha * (reward + self.gamma * maxQ - Q)
            robot.update_Q(state, action, new_Q)

            # Set state for next iteration
            robot.last_state = new_state
            # print(robot.q_table)


    @property
    def distances(self):
        return self.formation.get_distances()


    def update(self, tick):
        sim_counter = 0
        sim_iterations = 2000 / training_speed
        while not check_stop_game() and sim_counter <= sim_iterations:
            # Update clock
            dt = (pygame.time.get_ticks() - tick)/1000 * training_speed
            tick = pygame.time.get_ticks()

            # Update map
            self.gfx.map.blit(self.gfx.map_img, (0, 0))

            # ---------------------- Main ----------------------
            if get_seconds() >= self.timer:
                self.q_learning(dt)
                self.timer = get_seconds() + self.timer_step
            self.swarm.update_swarm(dt)
            self.gfx.update()
            pygame.display.update()
            self.formation.get_distances()
            sim_counter += 1


    def run(self):
        tick = pygame.time.get_ticks()

        for robot in self.swarm.robots:
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

        for robot in self.swarm.robots:
            print(robot.trajectory.compute_total_disruption_area(robot.history))


    def get_Q_tables(self):
        return [robot.q_table for robot in self.swarm.robots]


    def set_Q_tables(self, q_tables):
        for robot, q_table in zip(self.swarm.robots, q_tables):
            robot.q_table = q_table




    # WORLDS EXCHANGE

    def compute_world_score(self):
        return

