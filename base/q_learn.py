import pygame
from math import sqrt
from statistics import variance
from random import choice, uniform
from time import time as get_seconds

from utils.constants import *
from utils.dimensions import *
from utils.utils import distance
from utils.simulation_utils import check_stop_game
from utils.qlearn_utils import sim_duration

from formation import Formation
from simulation import Simulation
from robots.swarm import LearnSwarm
from robots.learn_robot import LearnRobot



class QLearn(Simulation):
    def __init__(self, alpha, gamma, rho, training_speed, demo):
        self.setup_swarm()
        self.setup_simulation()
        # Training
        self.training_speed = training_speed
        self.timer_step = 0.05 / self.training_speed
        self.timer = get_seconds() + self.timer_step
        # Q-learn params
        self.alpha = alpha
        self.gamma = gamma
        self.exploration_rho = rho
        self.demo = demo
        self.total_rewards = 0
        self.random_start = True

        # Learning worlds info
        self.tot_form_disr = 0
        self.tot_traj_disr = 0
        self.swarm.set_base_formation_area()

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



    # The q-learning step
    def q_learning(self, simcounter, sim_iterations):
        current_distances = self.formation.get_distances()
        dists_to_endpoint = self.formation.dist_to_end_poit()

        for robot in self.swarm.robots:
            state = robot.last_state[-1] if robot.last_state \
                else robot.state.get_current_state(current_distances[robot.id])
            # Get all possible actions
            possible_actions = robot.get_legal_actions()
            # (Explore vs Exploit)
            if uniform(0, 1) < self.exploration_rho:
                action = choice(possible_actions)
            else:
                action = robot.get_best_action(state, possible_actions)
            if not self.demo:
                # RANDOM START
                if self.random_start:
                    action = choice(possible_actions)
                # STRAIGHT START
                if simcounter <= sim_iterations/8 and self.straight_start:
                    action =  STRAIGHT

            # Take action and get reward
            robot.take_next_action(action)
            reward = robot.compute_reward(current_distances[robot.id], dists_to_endpoint[robot.id])
            self.total_rewards += reward

            # Get new state
            new_state = robot.get_new_state(current_distances[robot.id])

            # Update Q-table
            Q = robot.get_Q_value(state, action)
            maxQ = robot.get_max_Q(new_state, ALL_ACTIONS)
            new_Q = Q + self.alpha * (reward + self.gamma * maxQ - Q)
            robot.update_Q(state, action, new_Q)

            # Set state for next iteration, and store last action
            robot.last_state.append(new_state)
            robot.last_action.append(action)


    def update(self, tick):
        sim_counter = 0
        sim_iterations = sim_duration / self.training_speed
        while not check_stop_game() and sim_counter <= sim_iterations:
            # Update clock
            dt = (pygame.time.get_ticks() - tick)/1000 * self.training_speed
            tick = pygame.time.get_ticks()

            # Update map
            self.gfx.map.blit(self.gfx.map_img, (0, 0))

            # ---------------------- Main ----------------------
            # Q-LEARN
            if get_seconds() >= self.timer:
                self.q_learning(sim_counter, sim_iterations)
                self.timer = get_seconds() + self.timer_step
            # UPDATES
            self.swarm.update_swarm(dt)
            self.gfx.update()
            pygame.display.update()
            # DISTANCES 
            self.formation.get_distances()
            sim_counter += 1
            # FORMATION DISRUPTION
            self.tot_form_disr += self.swarm.formation_disruption

    def run(self, random_start, straight_start):
        self.random_start = random_start
        self.straight_start = straight_start
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
        # self.q_learning(dt, 0)
        self.swarm.update_swarm(dt)
        self.gfx.update()
        pygame.display.update()
        self.formation.get_distances()

        self.update(tick)

        # TOTAL TRAJECTORY DISRUPTION FOR EACH ROBOT
        traj_disrs = []
        for robot in self.swarm.robots:
             traj_disrs.append(robot.trajectory.compute_total_traj_disruption(robot.history))
        self.tot_traj_disr = variance(traj_disrs)




    def get_Q_tables(self):
        return [robot.q_table for robot in self.swarm.robots]


    def set_Q_tables(self, q_tables):
        for robot, q_table in zip(self.swarm.robots, q_tables):
            robot.q_table = q_table




    # WORLDS EXCHANGE
    def compute_world_score(self, discount1, discount2):
        return self.tot_form_disr * discount1, self.tot_traj_disr * discount2
