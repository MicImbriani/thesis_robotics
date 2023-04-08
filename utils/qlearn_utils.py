import pickle
# Saves the Q-table.

def save_policy(sim):
    fw = open('trained_controller', 'wb')
    pickle.dump(sim.get_Q_tables(), fw)
    fw.close()

# Loads a Q-table.
def load_policy(sim, file):
    fr = open(file, 'rb')
    sim.set_Q_tables(pickle.load(fr))
    fr.close()



from utils.constants import TOO_CLOSE, TOO_FAR, IN_RANGE

def get_spacing_from_dist(dists: dict) -> dict:
    """
    Returns a dictionary. Each entry is the distance to
    each other robot in the system
    """
    def is_in_range(dist):
        ideal_dist = 55
        dist = ideal_dist-dist # 55 - 40 15
        if dist >= 5:
            return TOO_CLOSE
        elif dist <= -5:
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




from utils.utils import distance
def _dist_to_goal(robot_position, final_coordinate):
    return distance(robot_position, final_coordinate)


# checks if the robot is traveling in the right direction
def in_correct_direction(robot_path, final_coordinate):
    if len(robot_path) <= 1:
        return False
    return True if _dist_to_goal(robot_path[-1], final_coordinate) < _dist_to_goal(robot_path[-2], final_coordinate) else False




def compute_discounted_total_rewards(swarm):
    count = 0
    for robot in swarm:
        count += robot.discounted_total_rewards
    return count