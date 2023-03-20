from random import choice, uniform

from utils.constants import *
from utils.qlearn_utils import get_spacing_from_dist
from utils.counter import Counter

from state import State
from simulation import Simulation

class QLearn(Simulation):
    def __init__(self):
        super().__init__()
        self.q_table = Counter()
        self.states_history = []
        self.last_action = []


    @property
    def distances(self):
        return self.formation.get_distances()

    def learn(self):
        # 1) get state of world
        self.get_state()
        # 2) select random action for each robot
        random_actions = self.get_random_actions()
        # 3) take/simulate the action
        # get new state
        self.take_actions(random_actions)
        # 4) assess how good the action was for the previous state, based on the current state
        # 5) update previous state
        # 6) repeat from 1 with new state



    # STATES
    def get_states(self):
        # dists = get_spacing_from_dist(self.formation.get_distances())
        # # ADD MORE STUFF TO STATE
        # return State(dists, )
        return [robot.get_state() for robot in self.swarm]


    def store_state(self, state):
        self.states_history.append(state)



    # ACTIONS
    def take_actions(self):
        all_actions = []
        for robot in self.swarm:
            # if the action is legal, robot.take_action will return true, else false
            rand_act = self._get_random_action()
            while not robot.set_action(rand_act):
                rand_act = self._get_random_action()
            all_actions.append(rand_act)

    def _get_random_action(self):
        return choice(available_actions)



    # Q-LEARN
    # Given a state and possible actions, returns the highest Q value
    def get_max_Q(self, state, possible_actions):
        q_list = []
        for action in possible_actions:
            q_list.append(self._get_Q_value(state, action))
        return 0 if not q_list else max(q_list)
    
    # Given a state and possible actions, returns the action of the highest Q value
    def get_action_max_Q(self, state, possible_actions):
        tmp = Counter()
        for action in possible_actions:
          tmp[action] = self.getQValue(state, action)
        return tmp.argMax()
    
    # Update the Q value of a given state-action entry
    def update_Q(self, state, action, reward, qmax):
        q = self._get_Q_value(state, action)
        self.q_table[str([state, action])] = (1 - self.lr_alpha) * q + self.lr_alpha * (reward + self.discount_rate_gamma*qmax - q)
        # MAYBE REWRITE QLEARN EQUATION
    
    # Return Q-value of a given state-action pair
    def _get_Q_value(self, state, action):
        return self.q_table[str([state, action])]

    # The main method 
    def on_tick(self, state, possible_directions, score):
        # print("___________________________")
        # print(self.states_value)

        # Update Q-value
        reward = score - self.old_score # CHANGE HOW ITS COMPUTED
        if self.states_history:
            last_state = self.states_history[-1]
            last_action = self.last_action[-1]
            max_q = self.get_max_Q(state, possible_directions)
            self.update_Q(last_state, last_action, reward, max_q)

        # (Explore vs Exploit)
        rand_rho = uniform(0, 1)
        action = choice(possible_directions) if rand_rho < self.exploration_rho else  self.takeBestAction(state, possible_directions)

        # Update attributes.
        self.states_history.append(state)
        self.last_action.append(action)

        return action

    # Called as the last iteration
    def on_end(self, score):
        # Update Q-values.
        reward = score - self.old_score
        last_state = self.states_history[-1]
        last_action = self.last_action[-1]
        self.update_Q(last_state, last_action, reward, 0)
        # Reset attributes.
        self.old_score = 0
        self.lastState = []
        self.lastAction = []

    def run(self):
        self.get_states()
        x = State(0, self.swarm, self.distances)

"""
q_learn -> learn_robot -> state 
"""