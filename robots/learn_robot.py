from random import choice, uniform
from numpy import array, add
from math import cos, sin, pi
from time import time as get_seconds

from utils.constants import *
from utils.counter import Counter
from utils.utils import get_direction_from_dir, get_direction_from_heading, get_relative_directions, get_heading_from_direction
from utils.qlearn_utils import in_correct_direction, get_spacing_from_dist

from state import State
from .robot import Robot

class LearnRobot(Robot):
    def __init__(self, game_map, startpos=None):
        super().__init__(game_map, startpos)
        self.name = "LearnRobot"
        self.timer_step = 0.5
        self.timer = get_seconds() + self.timer_step
        self.history = [self.position]
        _, self.collisions = self._sense_obstacles()


        # Q-LEARN
        self.q_table = Counter()
        self.last_state = []
        self.last_action = []
        self.current_dists = {}

    def init_state(self):
        print("AAAAA", [r.id for r in self.other_robots])
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

    

    def kinematics(self, dt):
        if get_seconds() >= self.timer:
            new_dir = self._get_new_direction(choice([LEFT, RIGHT, STRAIGHT]))
            # new_speedL, new_speedR = direction_coord[0]*self.minspeed, direction_coord[1]*self.minspeed
            # self.speedL += new_speedL
            # self.speedR += new_speedR

            # HARDCODED HEADING CHANGE
            self.heading = get_heading_from_direction(new_dir)

            # Add current position to the history of robot's positions
            self.history.append(self.position)
            # Check if it's going in right direction
            print(in_correct_direction(self.path, self.end_mid_point))

            self.timer = get_seconds() + self.timer_step

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
        self.speedL *= 10
        self.speedR *= 10


    def decelerate(self):
        self.speedL /= 2
        self.speedR /= 2


    def get_legal_actions(self):
        # Returns a list of legal actions
        # Accelerate and decellerate are always legal
        left = self.collisions[0] and self.collisions[1]
        right = self.collisions[3] and self.collisions[4]
        mid = self.collisions[2]
        # Basically zips [LEFT, RIGHT, STRAIGHT] with [left sensors, right sensors, mid sensor]
        return [action for action, obstacle_sensed in zip(ALL_ACTIONS[:3], [left, right, mid]) if not obstacle_sensed]


    # Given list of possible actions and the current state, returns the best action
    def get_action(self, state, possible_actions):
        state = state if not state is None else self.state.current_state

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


    # Called as the last iteration
    def on_end(self, score):
        # Update Q-values.
        reward = score - self.old_score
        last_state = self.last_state[-1]
        last_action = self.last_action[-1]
        self._update_Q(last_state, last_action, reward, 0)
        # Reset attributes.
        self.old_score = 0
        self.lastState = []
        self.lastAction = []


    def take_next_action(self, next_action, dt):
        relative_dir = self._get_new_direction(next_action)

        # HARDCODED HEADING CHANGE
        self.heading = get_heading_from_direction(relative_dir)

        # Add current position to the history of robot's positions
        self.history.append(self.position)
        # Check if it's going in right direction
        print(in_correct_direction(self.path, self.end_mid_point))

        v = (self.speedL + self.speedR) / 2
        # equation space-time-velocity
        # S(t) = S(t-1) + k*v(t)
        self.x += v * cos(self.heading) * dt
        self.y -= v * sin(self.heading) * dt


    def _get_new_direction(self, turn) -> dict:
        """ 
        Given the relative direction in which the robot should turn, 
        computes the absolute direction in which the robot should go.
        Thresholding the values is needed bcos all directions have max 
        value of 1.
        """
        relative_direction = get_relative_directions(
            self.current_direction, turn)
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
        return self.q_table[str([state, action])]
    
    def compute_reward(self, current_distances, dist_to_endpoint):
        # 1) distance error between robot and r1
        # 2) distance error between robot and r2
        # 3) distance to end goal
        dists = list(current_distances.values())
        dist_r1 = dists[0]
        dist_r2 = dists[1]
        return dist_r1 + dist_r2 + dist_to_endpoint