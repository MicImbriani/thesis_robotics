from utils.utils import connect2
from scipy.spatial.distance import euclidean

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
    def __init__(self, name, swarm):
        self.swarm = swarm
        match name:
            case "triangle":    self.formation = self._triangle_formation()
            case "line":        self.formation = self._line_formation()
            case "square":        self.formation = self._square_formation()
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
        id = 0
        for robot, formation_coords in zip(self.swarm, self.formation):
            traj = Trajectory(formation_coords)
            robot.trajectory = traj  # [(start),(end)]
            robot.x, robot.y = traj.start
            robot.id = id
            id += 1
    
    def get_goal_distances(self):
        start = [x[0] for x in self.formation]
        return {(0,1): (abs(start[0][0]-start[1][0]), abs(start[0][1]-start[1][1])),
                (0,2): (abs(start[0][0]-start[2][0]), abs(start[0][1]-start[2][1])),
                (1,2): (abs(start[2][0]-start[1][0]), abs(start[2][1]-start[1][1]))}

    def assign_dists(self):
        starts = [x[0] for x in self.formation]
        for robot in self.swarm:
            robot.distances = {}
            robot.distances_log = {}
            for id, entry in enumerate(starts):
                if id == robot.id:
                    continue
                else:
                    dist = euclidean(robot.position, entry)
                    self.dists[(robot.id, id)] = dist
                    robot.distances[id] = (abs(dist))
                    robot.distances_log[id] = []
