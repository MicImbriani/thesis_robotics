IN_RANGE = 0
TOO_FAR = 1
TOO_CLOSE = -1

def get_spacing_from_dist(dists: dict) -> dict:
    """
    Returns a dictionary. Each entry is the distance to
    each other robot in the system
    """
    def is_in_range(dist):
        if 3 <= dist <= 7:
            return IN_RANGE
        elif dist < 3:
            return TOO_CLOSE
        else:
            return TOO_FAR

    # Substitute every value of distances with IN_RANGE, TOO_FAR or TOO_CLOSE
    for robot, other_robots in dists.items():
        for k, v in other_robots.items():
            dists[robot][k] = is_in_range(v)
    return dists


from utils.utils import distance
def _dist_to_goal(robot_position, final_coordinate):
    return distance(robot_position, final_coordinate)


# checks if the robot is traveling in the right direction
def in_correct_direction(robot_path, final_coordinate):
    if len(robot_path) <= 1:
        return False
    return True if _dist_to_goal(robot_path[-1], final_coordinate) < _dist_to_goal(robot_path[-2], final_coordinate) else False


import pickle
# Saves the Q-table.
def save_policy(self):
    fw = open('trained_controller', 'wb')
    pickle.dump(self.states_value, fw)
    fw.close()

# Loads a Q-table.
def load_policy(self, file):
    fr = open(file, 'rb')
    self.states_value = pickle.load(fr)
    fr.close()
