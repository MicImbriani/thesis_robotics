from utils.utils import connect2, distance
from copy import copy

class Trajectory:
    def __init__(self, coords):
        self.start = coords[0]
        self.end = coords[1]
        

    @property
    def coord(self):
        return (self.start, self.end)
    
    def _set_traj_coords(self):
        points = connect2(self.start, self.end)



class Formation:
    def __init__(self, name, robots, ids):
        self.robots = robots
        self.ids = ids
        match name:
            case "triangle":    self.formation = self._triangle_formation()
            case "line":        self.formation = self._line_formation()
            case "square":        self.formation = self._square_formation()
        self.end_middle_coordinate = self._compute_end_point()
        self.dists = {}
        self.assign_trajs()
        self.assign_dists()
    
    def _triangle_formation(self):
        start = [(200, 100), (250, 100), (225, 150)]
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
                    dist = euclidean(robot.position, entry)
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
