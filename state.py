from copy import deepcopy
from utils.utils import distance
from utils.qlearn_utils import in_correct_direction, get_spacing_from_dist

class State:
    def __init__(self, robot, other_robots):
        self.robot = robot
        self.other_robots = other_robots

    def get_current_state(self, current_distances):
        """
        FINAL LOOK OF STATE
        [my heading
        going towards goal
        robot2 spacing
        robot2 heading
        robot3 spacing
        robot3 heading]
        """
        print("XDD")
        print("ME", self.robot.id)
        r1, r2 = self.other_robots
        print("OTHERS", r1.id, r2.id)
        spacings = get_spacing_from_dist(current_distances)
        print("AAAAAAA",spacings)
        print()
        return [self.robot.heading,
                self._towards_goal,
                spacings[r1.id],
                r1.heading,
                spacings[r2.id],
                r2.heading]


    def _get_dist_logs(self):
        """
        Returns a dictionary where keys are other robots, and values are the 
        lists of recorded distances between the self.robot and that robot
        e.g.
        0: {1: [50.0, 55.90169943749474], 2: [50.0, 55.90169943749474]}
        """
        return self.distances[self.robot.id]
    

    # def _get_relative_position(self, other_robot):
    #     return distance(self.position, other_robot.position)
    
    
    @property
    def _towards_goal(self):
        return in_correct_direction(self.robot.path, self.robot.end_mid_point)
