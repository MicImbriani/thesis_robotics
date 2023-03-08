from utils.qlearn_utils import get_spacing_from_dist

from simulation import Simulation

class QLearn(Simulation):
    def __init__(self):
        super().__init__()


    def get_state(self):
        dists = get_spacing_from_dist(self.formation.get_distances())
        # ADD MORE STUFF TO STATE

    def get_random_actions(self):
        return
    
    def take_action(self):
        #  TODO: in order to take an action, the LearnRobot needs to be 
        # able to "be communicated" which action it should take next.
        # Basically, gotta implement a simple controller that is based
        # on orientation i.e. given RIGHT/LEFT/STRAIGHT, it goes there.
        return

    def learn(self):
        # 1) get state of world
        self.get_state()
        # 2) select random action for each robot
        self.get_random_actions()
        # 3) take/simulate the action 
        # get new state
        self.take_action()