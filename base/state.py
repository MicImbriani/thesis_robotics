from copy import deepcopy
from utils.utils import distance
from utils.qlearn_utils import in_correct_direction, get_spacing_from_dist, get_relative_pos_from_coords
from utils.utils import get_direction_from_heading_4_dirs


class State:
    def __init__(self, robot, other_robots):
        self.current_state = []
        self.robot = robot
        self.other_robots = other_robots

    def get_current_state(self, current_distances):
        """
        FINAL LOOK OF STATE
        [my heading
        going towards goal
        robot2 spacing
        robot2 direction relative to robot
        robot3 spacing
        robot3 direction relative to robot]
        """
        r1, r2 = self.other_robots
        spacings = get_spacing_from_dist(current_distances)
        my_pos = self.robot.position
        return [self.robot.heading,
                self._towards_goal,
                spacings[r1.id],
                get_relative_pos_from_coords(my_pos, r1.position),
                spacings[r2.id],
                get_relative_pos_from_coords(my_pos, r2.position)]


    def _get_dist_logs(self):
        """
        Returns a dictionary where keys are other robots, and values are the 
        lists of recorded distances between the self.robot and that robot
        e.g.
        0: {1: [50.0, 55.90169943749474], 2: [50.0, 55.90169943749474]}
        """
        return self.distances[self.robot.id]

    @property
    def _towards_goal(self):
        # if self.robot.id == 0:
            # print(get_direction_from_heading_4_dirs(self.robot.heading))
        return in_correct_direction(self.robot.position, self.robot.heading, self.robot.end_mid_point)
