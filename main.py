from multiprocessing import Pool

from utils.qlearn_utils import save_policy

from simulation import Simulation
from q_learn import QLearn

# Q-LEARNING 
Q_LEARN = True

# Parameters
exploration_rho = 0.3
lr_alpha = 0.2
discount_rate_gamma = 0.9
walk_len_nu = 0.2
train_iterations = 5000
# MULTIPROCESSING
learning_worlds = 1






if __name__ == "__main__":
    if not Q_LEARN:
        my_sim = Simulation()
        my_sim.run()
    else:
        def train(n):
            print("Learning World", n)
            for i in range(train_iterations):
                print(f"Iterations {i}")
                # Setup
                my_sim = QLearn(lr_alpha, discount_rate_gamma,
                                exploration_rho, walk_len_nu)
                if i != 0:
                    my_sim.set_Q_tables(last_q_tables)

                # Start
                my_sim.run()

                # Save results
                last_q_tables = my_sim.get_Q_tables()
                if i % 100 == 0:
                    save_policy(my_sim)

                # Reset
                del my_sim

        with Pool(learning_worlds) as p:
            p.map(train, list(range(learning_worlds)))


if __name__ == "__main__":
    if not Q_LEARN:
        my_sim = Simulation()
        my_sim.run()
    else:
        def one_iter_funct(previous_Q_table):
            global i
            # Setup
            my_sim = QLearn(lr_alpha, discount_rate_gamma,
                            exploration_rho, walk_len_nu)
            if i != 0: my_sim.set_Q_tables(previous_Q_table)
            # Start
            my_sim.run()
            tables = my_sim.get_Q_tables()
            # Reset
            del my_sim
            return tables

        previous_Q_tables = [[] for _ in range(learning_worlds)]
        for i in range(train_iterations):
            print(f"Iterations {i}")

            # Stup and run all learning worlds in parallel
            with Pool(learning_worlds) as p:
                all_tables = p.map(one_iter_funct, previous_Q_tables)

            # Perform exchange of info across worlds

            # Save results
            if i % 100 == 0:
                save_policy(my_sim)
