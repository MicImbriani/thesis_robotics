import pickle
import matplotlib.pyplot as plt
from statistics import mean
from utils.simulation_utils import get_distance_errors_log
# Saves the Q-table.

sim_duration = 1500


def save_element(element, file_name):
    fw = open(file_name, 'wb')
    pickle.dump(element, fw)
    fw.close()

# Loads a Q-table.
def load_policy(sim, file):
    fr = open(file, 'rb')
    sim.set_Q_tables(pickle.load(fr))
    fr.close()
    return sim.get_Q_tables()

def make_plots(swarm, formation):
    distances = formation.dists
    distances_log = get_distances_log(swarm)
    r01 = distances_log[0][1]
    r02 = distances_log[0][2]
    r12 = distances_log[1][2]
    length = len(r01)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(range(length), [val-distances[(0, 1)] for val in r01], color='tab:blue')
    ax.plot(range(length), [val-distances[(0, 2)] for val in r02], color='tab:green')
    ax.plot(range(length), [val-distances[(1, 2)] for val in r12], color='tab:red')
    plt.savefig("../lol.png")


def store_distances_logs(distances, swarm):
    distances_log = get_distance_errors_log(swarm)
    r01 = distances_log[0][1]
    r02 = distances_log[0][2]
    r12 = distances_log[1][2]
    avgs = []
    for log in [r01, r02, r12]:
        dist_in_one_iter = [val for val in log]
        avgs.append(mean(dist_in_one_iter))
    return avgs




from utils.constants import TOO_CLOSE, TOO_FAR, IN_RANGE

def get_spacing_from_dist(dists: dict) -> dict:
    """
    Returns a dictionary. Each entry is the distance to
    each other robot in the system
    """
    def is_in_range(dist):
        ideal_dist = 50
        dist = ideal_dist-dist # 55 - 40 15
        if dist >= 15:
            return TOO_CLOSE
        elif dist <= -15:
            return TOO_FAR
        else:
            return IN_RANGE

    # Substitute every value of distances with IN_RANGE, TOO_FAR or TOO_CLOSE
    new_dists = {}
    for other_robot, dist in dists.items():
        new_dists[other_robot] = is_in_range(dist)
    return new_dists

from math import atan2
from utils.utils import get_direction_from_heading
def get_relative_pos_from_coords(point1, point2):
    a, b = point1
    x, y = point2
    tang = atan2(-(y-b), x-a)
    return get_direction_from_heading(tang)


from utils.utils import get_direction_from_heading_4_dirs
def get_relative_pos_from_coords2(point1, point2):
    a, b = point1
    x, y = point2
    tang = atan2(-(y-b), x-a)
    return get_direction_from_heading_4_dirs(tang)



def in_correct_direction(robot_pos, robot_heading, final_coord):
    robot_to_end_dir = get_relative_pos_from_coords2(robot_pos, final_coord)
    return True if get_direction_from_heading_4_dirs(robot_heading) == robot_to_end_dir \
        else False



def compute_discounted_total_rewards(swarm):
    count = 0
    for robot in swarm:
        count += robot.discounted_total_rewards
    return count


from utils.constants import *

GLOBAL_DIRECTIONS = [UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN_LEFT, LEFT, DOWN_LEFT]
LOCAL_DIRECTIONS = [STRAIGHT, STRAIGHT_LEFT, LEFT, BEHIND_LEFT, BEHIND, BEHIND_RIGHT, RIGHT, STRAIGHT_RIGHT]
