import numpy as np
from copy import copy
from numpy import array
from numpy import trapz

from utils.utils import connect, distance

class Trajectory:
    def __init__(self, coords):
        self.start = coords[0]
        self.end = coords[1]
        self.line = connect(array([[self.start[0], self.start[1]],
                                   [self.end[0], self.end[1]]]))


    # Calculate at the end of train episode
    def compute_total_traj_disruption(self, robot_history):
        robot_history = array(robot_history)
        robot_history_sorted = robot_history[robot_history[:, 1].argsort()]
        x_robot = []
        y_robot = []
        for point in robot_history_sorted:
            if point[0] == 0 and point[1]==0: continue
            x_robot.append(point[0] - self.start[0])
            y_robot.append(-1*(point[1] - self.start[1]))
        robot_area = trapz(x=x_robot, y=y_robot)
        return abs(robot_area)



class Formation:
    def __init__(self, name, robots, ids):
        self.robots = robots
        self.ids = ids
        if name ==  "triangle":    self.formation = self._triangle_formation()
        elif name ==  "line":        self.formation = self._line_formation()
        elif name ==  "square":        self.formation = self._square_formation()
        # self.formation final look:
        #  [[(200, 100), (700, 100)], [(250, 100), (750, 100)], [(225, 150), (725, 150)]]
        self.end_middle_coordinate = self._compute_end_point()
        self.dists = {}
        self.assign_trajs()
        self.assign_dists()

    def _triangle_formation(self):
        start = [(50, 100), (50, 150), (93, 125)]
        end = list(map(lambda coords: (coords[0]+500, coords[1]), start))
        return [[x,y] for x,y in zip(start, end)]

    def _line_formation(self):
        start = [(200, 100), (200, 130), (200, 160)]
        end = list(map(lambda coords: (coords[0]+500, coords[1]), start))
        return [[x, y] for x, y in zip(start, end)]
    
    def _square_formation(self):
        start = [(200, 100), (200, 130), (230, 130), (230,100)]
        end = list(map(lambda coords: (coords[0]+500, coords[1]), start))
        return [[x, y] for x, y in zip(start, end)]

    def assign_trajs(self):
        """ Assigns desired trajectory to each robot, respectively.
        """
        for robot, formation_coords in zip(self.robots, self.formation):
            traj = Trajectory(formation_coords)
            robot.trajectory = traj  # [(start),(end)]
            robot.x, robot.y = traj.start
    
    # def get_goal_distances(self):
    #     start = [x[0] for x in self.formation]
    #     return {(0,1): (abs(start[0][0]-start[1][0]), abs(start[0][1]-start[1][1])),
    #             (0,2): (abs(start[0][0]-start[2][0]), abs(start[0][1]-start[2][1])),
    #             (1,2): (abs(start[2][0]-start[1][0]), abs(start[2][1]-start[1][1]))}

    def assign_dists(self):
        """ For each robot in the swarm, assigns the desired distance to mantain 
        with respects to every other robot in the swarm.
        """
        starts = [x[0] for x in self.formation]
        for robot in self.robots:
            robot.distances = {}
            robot.distances_log = {}
            for id, entry in enumerate(starts):
                if id == robot.id:
                    continue
                else:
                    dist = distance(robot.position, entry)
                    self.dists[(robot.id, id)] = dist
                    robot.distances[id] = (abs(dist))
                    robot.distances_log[id] = [(abs(dist))]

    def get_distances(self) -> dict:
        """ Gets current distances between robots.
        """
        dists = {}
        for robot in self.robots:
            new_ids = copy(self.ids)
            new_ids.remove(robot.id)
            for id in new_ids:
                dists[robot.id] = dict.fromkeys(new_ids, robot.distances_log[id][-1])
        return dists

    def _compute_end_point(self):
        # [[(200, 100), (700, 100)], [(250, 100), (750, 100)], [(225, 150), (725, 150)]]
        all_ends = [start_and_end[1] for start_and_end in self.formation]
        ends_x = [end[0] for end in all_ends]
        ends_y = [end[1] for end in all_ends]
        return (sum(ends_x)/len(ends_x), sum(ends_y)/len(ends_y))

    def dist_to_end_poit(self):
        return [distance(robot.position, self.end_middle_coordinate) for robot in self.robots]
