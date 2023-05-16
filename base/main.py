import os
import pickle
import argparse
from random import choice
from copy import deepcopy
from statistics import mean
from numpy import array,argsort
from multiprocessing import Pool

from utils.qlearn_utils import save_element, load_policy, make_plots, \
                        store_distances_logs, sim_duration

from q_learn import QLearn
from simulation import Simulation
import time
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", help="Version of the simulation", type=int)
parser.add_argument("-d", "--demo", help="Demo", action='store_true', default=False)
parser.add_argument("--headless", help="Whether to create and show display", action='store_true', default=False)
args = parser.parse_args()

if args.headless:
    os.environ["SDL_VIDEODRIVER"] = "dummy"


# Q-LEARNING 
Q_LEARN = True
training_speed = 1
sim_duration = sim_duration

# Parameters
exploration_rho = 0.2
lr_alpha = 0.8
discount_rate_gamma = 0.9
walk_len_nu = 0.2
train_iterations = 1000

# MULTI-VERSE
learning_worlds = 1
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


if __name__ == "__main__" and PROGRESS == 0:
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
                

                # Reset
                del my_sim

        with Pool(learning_worlds) as p:
            p.map(train, list(range(learning_worlds)))


if __name__ == "__main__" and PROGRESS == 0:
    if not Q_LEARN:
        my_sim = Simulation()
        my_sim.run()
    else:
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
            

            

            # Reset
            del my_sim



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
            




if __name__ == "__main__" and PROGRESS == 2:
    if not Q_LEARN:
        my_sim = Simulation()
        my_sim.run()
    else:
        def one_iter_funct(previous_Q_table):
            global i, last_iter, local_sum_rewards
            # Setup
            my_sim = QLearn(lr_alpha, discount_rate_gamma,
                            exploration_rho, walk_len_nu, training_speed)
            if i != 0:
                my_sim.set_Q_tables(previous_Q_table)
            # Start
            random_start = True if i <= train_iterations/100 else False
            my_sim.run(random_start)
            # Store
            formation_disr, traj_disr = my_sim.compute_world_score(
                                                        formation_discount,
                                                        trajectory_discount)
            tables = my_sim.get_Q_tables()
            # Rewards
            rewards = my_sim.total_rewards
            # Distances
            dists_avgs = store_distances_logs(my_sim.formation.dists,
                                         my_sim.swarm.robots)

            # Reset
            del my_sim
            return formation_disr, traj_disr, tables, rewards, dists_avgs

        # Variables needed for storing the information
        tot_avg_rewards = []
        tot_min_rewards = []
        tot_max_rewards = []
        all_dists_logs = {(0,1):[], (0,2):[], (1,3):[]}
        # Variables needed for executing the various learning worlds
        previous_Q_tables = [[] for _ in range(learning_worlds)]
        iter_counter = 0
        info_exch = []
        info_exch_counter = 0
        last_iter = False
        for i in range(train_iterations):
            print()
            print(f"Iterations {i}")
            if i == train_iterations - 1:
                last_iter = True
            iter_counter += 1

            # Reset local sum of rewards
            local_sum_rewards = 0

            # Stup and run all learning worlds in parallel
            with Pool(learning_worlds) as p:
                world_scores = p.map(one_iter_funct, previous_Q_tables)

            # Store info of rewards to global counter
            rewards_list = [world[-2] for world in world_scores]
            tot_avg_rewards.append(mean(rewards_list))
            tot_min_rewards.append(min(rewards_list))
            tot_max_rewards.append(max(rewards_list))

            # Store info of distances log
            dists_list = [world[-1] for world in world_scores][0] \
                if learning_worlds == 1 else [world[-1] for world in world_scores]
            [all_dists_logs[pair].append(pair_dist) for pair, pair_dist in zip(all_dists_logs, dists_list)]

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
                info_exch.append(i)
                info_exch_counter += 1
                print(f"EXCHANGE {info_exch_counter}")
                previous_Q_tables = [deepcopy(world_results_dict[sort_by_form[0][0]]) for _ in range(learning_worlds)]
            # otherwise, just use previous iteration's q-tables.
            else:
                previous_Q_tables = [world[2] for world in world_scores]
            print(f"Q-TABLE {len(previous_Q_tables[0][0])}")

            # Save results
            if i % 10 == 0:
                save_element(previous_Q_tables, 'trained_controller')
                save_element(tot_avg_rewards, 'tot_avg_rewards')
                save_element(tot_min_rewards, 'tot_min_rewards')
                save_element(tot_max_rewards, 'tot_max_rewards')
                save_element(all_dists_logs, 'all_dists_logs')
                save_element(info_exch_counter, 'info_exch_counter')

            # ON END
            with open("test_output.txt", "a") as myfile:
                myfile.write(f"{iter_counter} total iterations,"
                            f"INFO EXCHANGED {info_exch_counter} TIMES.")

        print("LOGS", all_dists_logs)
        print("REWARDS", tot_avg_rewards)
        print("INFO EXCHANGED: ", info_exch_counter)


if __name__ == "__main__" and PROGRESS == -1:
    fr = open('trained_controller', 'rb')
    q_tables = pickle.load(fr)
    ALL = False
    if not ALL:
        q_tables = [choice(q_tables)]
        print(len(q_tables))
    for world_q_tables in q_tables:
        # Setup
        my_sim = QLearn(alpha=0, gamma=discount_rate_gamma,
                        rho=0, nu=walk_len_nu, training_speed=1)
        # Load Q-tables
        my_sim.set_Q_tables(world_q_tables)
        # Start
        my_sim.run()
