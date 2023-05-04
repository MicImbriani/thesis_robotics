import os
import pickle
import argparse
from copy import deepcopy
from numpy import array,argsort
from multiprocessing import Pool

from utils.qlearn_utils import save_policy, load_policy

from q_learn import QLearn
from simulation import Simulation

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", help="Version of the simulation", type=int)
parser.add_argument("-d", "--demo", help="Demo", action='store_true', default=False)
parser.add_argument("--headless", help="Whether to create and show display", action='store_true', default=False)
args = parser.parse_args()

if args.headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"


# Q-LEARNING 
Q_LEARN = True
training_speed = 10

# Parameters
exploration_rho = 0.3
lr_alpha = 0.2
discount_rate_gamma = 0.9
walk_len_nu = 0.2
train_iterations = 5000
# MULTI-VERSE
learning_worlds = 3
formation_discount = 0.9
trajectory_discount = 0.7


"""
PROGRESS
-1: Demo
0: Simple running of the sim
1: Simple q-learning
2: Q-learn with world info exchange
"""
PROGRESS = 2 if args.version is None else args.version
PROGRESS = -1 if args.demo else PROGRESS



if __name__ == "__main__" and PROGRESS==0:
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
                                exploration_rho, walk_len_nu, training_speed)
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


if __name__ == "__main__" and PROGRESS==1:
    if not Q_LEARN:
        my_sim = Simulation()
        my_sim.run()
    else:
        def one_iter_funct(previous_Q_table):
            global i
            # Setup
            my_sim = QLearn(lr_alpha, discount_rate_gamma,
                            exploration_rho, walk_len_nu, training_speed)
            if i != 0: my_sim.set_Q_tables(previous_Q_table)
            # Start
            my_sim.run()
            # Store
            tables = my_sim.get_Q_tables()
            # Reset
            del my_sim
            return tables

        previous_Q_tables = [[] for _ in range(learning_worlds)]
        for i in range(train_iterations):
            print(f"Iterations {i}")

            # Stup and run all learning worlds in parallel
            with Pool(learning_worlds) as p:
                previous_Q_tables = p.map(one_iter_funct, previous_Q_tables)

            # Perform exchange of info across worlds

            # Save results
            if i % 100 == 0:
                save_policy(my_sim)




if __name__ == "__main__" and PROGRESS == 2:
    if not Q_LEARN:
        my_sim = Simulation()
        my_sim.run()
    else:
        def one_iter_funct(previous_Q_table):
            global i
            # Setup
            my_sim = QLearn(lr_alpha, discount_rate_gamma,
                            exploration_rho, walk_len_nu, training_speed)
            if i != 0:
                my_sim.set_Q_tables(previous_Q_table)
            # Start
            my_sim.run()
            # Store
            formation_disr, traj_disr = my_sim.compute_world_score(formation_discount, 
                                                                   trajectory_discount)
            tables = my_sim.get_Q_tables()
            # Reset
            del my_sim
            return formation_disr, traj_disr, tables

        previous_Q_tables = [[] for _ in range(learning_worlds)]
        iter_counter = 0
        info_exch_counter = 0
        for i in range(train_iterations):
            print(f"Iterations {i}")
            iter_counter += 1
            # Stup and run all learning worlds in parallel

            with Pool(learning_worlds) as p:
                world_scores = p.map(one_iter_funct, previous_Q_tables)

            # HARDCODED: 3 WORLDS ONLY
            world1, world2, world3 = world_scores[0], world_scores[1], world_scores[2]

            # Compute best performing world
            all_world_scores = []
            world_results_dict = {idx: world[2] for idx, world in enumerate(world_scores)}
            for idx, world in enumerate(world_scores):
                world_list = list(world)
                world_list.insert(0, idx)
                all_world_scores.append(world_list)

            all_world_scores_copy = deepcopy([x[:3] for x in all_world_scores])
            array_all_world_scores = array(all_world_scores_copy)
            sort_by_form = array_all_world_scores[array_all_world_scores[:, 1].argsort()].tolist()
            sort_by_traj = array_all_world_scores[array_all_world_scores[:, 2].argsort()].tolist()
            
            # Check if the BEST FORMation world is also the BEST VARIANCE world
            if int(sort_by_form[0][0]) == int(sort_by_traj[0][0]):
                # If so, do the exchange...
                info_exch_counter += 1
                print(f"EXCHANGE {info_exch_counter}")
                previous_Q_tables = [deepcopy(world_results_dict[sort_by_form[0][0]]) for _ in range(learning_worlds)]
            # otherwise, just use previous iteration's q-tables.
            else:
                previous_Q_tables = [world[2] for world in world_scores]

            # Save results
            if i % 10 == 0:
                save_policy(previous_Q_tables)
        # ON END
        with open("test_output.txt", "w") as myfile:
            myfile.write(f"{iter_counter} total iterations,"
                         "INFO EXCHANGED {info_exch_counter} TIMES.")


        print("INFO EXCHANGED: ", info_exch_counter)


if __name__ == "__main__" and PROGRESS == -1:
    fr = open('trained_controller', 'rb')
    q_tables = pickle.load(fr)
    for world_q_tables in q_tables:
        # Setup
        my_sim = QLearn(alpha=0, gamma=discount_rate_gamma,
                        rho=0, nu=walk_len_nu, training_speed=5)
        # Load Q-tables
        my_sim.set_Q_tables(world_q_tables)
        # Start
        my_sim.run()

