from random import choice
from numpy import array, add
from math import cos, sin, pi

from utils.constants import *
from utils.counter import Counter
from utils.utils import get_direction_from_dir, get_direction_from_heading, get_relative_directions, get_heading_from_direction
from utils.qlearn_utils import get_spacing_from_dist

from state import State
from .robot import Robot

class LearnRobot(Robot):
    def __init__(self, game_map, startpos=None):
        super().__init__(game_map, startpos)
        self.name = "LearnRobot"
        self.history = [self.position]
        _, self.collisions = self._sense_obstacles()
        # MOVEMENT SPEEDS
        self.max_speed = 50
        self.min_speed = -10
        self.acc_increment = 10
        self.dec_increment = 10

        # Q-LEARN
        self.q_table = Counter()
        self.last_state = []
        self.last_action = []
        self.current_dists = {}
        self.discount_factor = 0.8
        self.discounted_total_rewards = 0

    def init_state(self):
        self.state = State(self, self.other_robots)
    

    ################ UPDATE ################
    def update(self, dt):
        """ TODO: update is called from the Swarm object.
        Need to make it so that the update method executes the whole
        learning for the robot.
        The current hierarchy is:
        Main: manages the iteration of the learning 
        > Q-Learn(Simulation): manages each tick in a simulation;
            at each tick, the Swarm is used
        >> Swarm: execs the training step of all the robots
        >> > LearnRobot: Executes the individual Q-learn
        >>>>> State: gets updated to give information about the current state
        """ 
        _, self.collisions = self._sense_obstacles()
        self.kinematics(dt)
        self.store_distances()
        # Add current position to the history of robot's positions
        self.history.append(self.position)


    def kinematics(self, dt):
        v = (self.speedL + self.speedR) / 2
        # equation space-time-velocity
        # S(t) = S(t-1) + k*v(t)
        self.x += v * cos(self.heading) * dt
        self.y -= v * sin(self.heading) * dt



    ################ STATE ################

    def get_new_state(self, current_distances):
        return self.state.get_current_state(current_distances)


    ################   ACTIONS   ################

    def accelerate(self):
        # RIGHT
        if self.speedL + self.acc_increment <= self.max_speed:
            self.speedL += self.acc_increment
        else: self.speedL = self.max_speed
        # LEFT
        if self.speedR + self.acc_increment <= self.max_speed: 
            self.speedR += self.acc_increment
        else: self.speedR = self.max_speed


    def decelerate(self):
        # RIGHT
        if self.speedL - self.dec_increment >= self.min_speed:
            self.speedR -= self.dec_increment
        else: self.speedR = self.min_speed
        # LEFT
        if self.speedL - self.dec_increment >= self.min_speed:
            self.speedL -= self.dec_increment
        else: self.speedL = self.min_speed


    def get_legal_actions(self):
        """GET LEGAL GLOBAL ACTIONS"""
        new_collisions = self.collisions[4:] + self.collisions[:4]
        # LOCAL_DIRECTIONS = [STRAIGHT, STRAIGHT_LEFT, LEFT, BEHIND_LEFT, BEHIND, BEHIND_RIGHT, RIGHT, STRAIGHT_RIGHT]
        my_dir = get_direction_from_heading(self.heading)
        dir_id = GLOBAL_DIRECTIONS.index(my_dir)
        legal_actions = [DECELERATE]
        for idx, action in enumerate(GLOBAL_DIRECTIONS):
            if not new_collisions[idx - dir_id]:
                legal_actions.append(action)
        # Accelerate and decellerate are always legal
        return legal_actions + [ACCELERATE] if STRAIGHT in legal_actions \
            else legal_actions


    # Given list of possible actions and the current state, returns the best action
    def get_action(self, state, possible_actions):
        state = state if state is not None else self.state.current_state
        action = self.get_best_action(state, possible_actions)
        # Update attributes.
        self.last_state.append(state)
        self.last_action.append(action)
        return action


    # Given a state and possible actions, returns the action of the highest Q value
    def get_best_action(self, state, possible_actions):
        tmp = Counter()
        for action in possible_actions:
            tmp[action] = self.get_Q_value(state, action)
        return tmp.argMax()


    def take_next_action(self, next_action):
        if next_action == ACCELERATE:
            self.accelerate()
        elif next_action == DECELERATE:
            self.decelerate()
        elif next_action == STRAIGHT:
            return # heading stays the same
        else:
            # HARDCODED HEADING CHANGE
            self.heading = get_heading_from_direction(next_action)


    def _get_new_direction(self, next_action):
        relative_direction = get_relative_directions(
            self.current_direction, next_action)
        new_direction = add(array(self.current_direction),
                            array(relative_direction))

        def treshold(x):
            sign = 1 if x >= 0 else -1
            return 1*sign if x > 1 or x < -1 else x
        new_direction = list(map(treshold, new_direction))
        return get_direction_from_dir((new_direction[0], new_direction[1]))


    @property
    def current_direction(self):
        return get_direction_from_heading(self.heading)




    ################ Q-LEARN ################
    
    # Update the Q value of a given state-action entry
    def update_Q(self, state, action, new_Q):
        self.q_table[str([state, action])] = new_Q
        # MAYBE REWRITE QLEARN EQUATION


    # Given a state and possible actions, returns the highest Q value
    def get_max_Q(self, state, possible_actions):
        q_list = []
        for action in possible_actions:
            q_list.append(self.get_Q_value(state, action))
        return 0 if not q_list else max(q_list)


    # Return Q-value of a given state-action pair
    def get_Q_value(self, state, action):
        if state == []:
            return 0
        return self.q_table[str([state, action])]
    
    def compute_reward(self, current_distances, dist_to_endpoint):
        # Distance to end goal. Closer -> more points
        reward = 1/ dist_to_endpoint * 1000
        # Reward if robots stay in range of each other,
        # penalize if too far or too close
        spacings = list(get_spacing_from_dist(current_distances).values())
        for robot_spacing in spacings:
            if robot_spacing == TOO_FAR:
                reward -= 10
            elif robot_spacing == TOO_CLOSE:
                reward -= 1
            elif robot_spacing == IN_RANGE:
                reward += 100
            else:
                raise Exception("Error when converting distances to spacing. Returned value is not TOO_FAR, TOO_CLOSE or IN_RANGE")
        # Penalize every second to encourage faster solutions
        reward -= 1
        self._update_discounted_total_rewards(reward)
        return reward


    def _update_discounted_total_rewards(self, reward):
        self.discounted_total_rewards += self.discount_factor * reward
