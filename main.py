from simulation import Simulation
from q_learn import QLearn

from utils.qlearn_utils import save_policy

# Q-LEARNING 
Q_LEARN = True
# Parameters
exploration_rho = 0.3
lr_alpha = 0.2
discount_rate_gamma = 0.9
walk_len_nu = 0.2
train_iterations = 5




if __name__ == "__main__":
    if not Q_LEARN:
        my_sim = Simulation()
        my_sim.run()
    else:
        for i in range(train_iterations):
            if i % 100 == 0:
                print("Iterations {}".format(i))
                # save_policy()
            my_sim = QLearn(lr_alpha, discount_rate_gamma, exploration_rho,
                            walk_len_nu)
            my_sim.run()
            del my_sim
