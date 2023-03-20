from simulation import Simulation
from q_learn import QLearn

from utils.qlearn_utils import save_policy

Q_LEARN = True

my_sim = QLearn() if Q_LEARN else Simulation()


def train(self, iterations=100):
      for i in range(iterations):
            if i % 1000 == 0:
                print("Iterations {}".format(i))
            if i % 200 == 0:
                save_policy()
            sim = Simulation()
            sim.setup_simulation()
            sim.update()
            # self.updateState(sim.ghosts, pacman_target)
            sim.start()


if __name__ == "__main__":
    if not Q_LEARN:
        my_sim.run()
    else:
        