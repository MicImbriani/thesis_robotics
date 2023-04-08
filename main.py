from copy import deepcopy
from numpy import array,argsort
from multiprocessing import Pool

from utils.qlearn_utils import save_policy

from q_learn import QLearn
from simulation import Simulation

# Q-LEARNING 
Q_LEARN = True
training_speed = 1

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


PROGRESS = 2



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
        info_exch_counter = 0
        for i in range(train_iterations):
            print(f"Iterations {i}")

            # Stup and run all learning worlds in parallel
            with Pool(learning_worlds) as p:
                world_scores = p.map(one_iter_funct, previous_Q_tables)
            
            # print(len(world_score))
            # print()
            # [print(x[:3]) for x in world_score]
            
            # HARDCODED TO 3 WORLDS ONLY
            world, world2, world3 = world_scores[0], world_scores[1], world_scores[2]
            
            # Compute best performing world
            all_world_scores = []
            for idx, world in enumerate(world_scores):
                world_list = list(world)
                world_list.insert(0, idx)
                all_world_scores.append(world_list)
            # print("SCORES", len(all_world_scores))
            # [print(sublist) for sublist in all_world_scores]
            # [print(x[:3]) for x in all_world_scores]

            all_world_scores_copy = deepcopy([x[:3] for x in all_world_scores])
            print(all_world_scores_copy)
            array_all_world_scores = array(all_world_scores_copy)
            print(array_all_world_scores)
            sort_by_form = array_all_world_scores[array_all_world_scores[:, 1].argsort()]
            sort_by_traj = array_all_world_scores[array_all_world_scores[:, 2].argsort()]
            
            # Check if the BEST FORMation world is also the BEST VARIANCE world
            if int(sort_by_form[0][0]) == int(sort_by_traj[0][0]):
                # If so, do the exchange...
                previous_Q_tables = [deepcopy(sort_by_form[0]) for _ in range(learning_worlds)]
                print("INFO EXCHANGE")
                info_exch_counter += 1
            # otherwise, just use previous iteration's q-tables.
            else:
                # Save results
                if i % 100 == 0:
                    save_policy(previous_Q_tables)

        print("INFO EXCHANGED: ", info_exch_counter)
