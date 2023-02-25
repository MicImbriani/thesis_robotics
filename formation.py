from utils import connect2
from scipy.spatial import distance
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

    def assign_trajs(self):
        id = 0
        for robot, formation_coords in zip(self.swarm, self.formation):
            traj = Trajectory(formation_coords)
            robot.trajectory = traj  # [(start),(end)]
            robot.x, robot.y = traj.start
            robot.id = id
            id += 1
    
    # def get_goal_distances(self):
    #     start = [x[0] for x in self.formation]
    #     return {(0,1): (abs(start[0][0]-start[1][0]), abs(start[0][1]-start[1][1])),
    #             (0,2): (abs(start[0][0]-start[2][0]), abs(start[0][1]-start[2][1])),
    #             (1,2): (abs(start[2][0]-start[1][0]), abs(start[2][1]-start[1][1]))}

    def assign_dists(self):
        starts = [x[0] for x in self.formation]
        for robot in self.swarm:
            robot.distances = {}
            for id, entry in enumerate(starts):
                if id == robot.id:
                    continue
                else:
                    dist = distance.euclidean(robot.position, entry)
                    # robot.distances[id] = (abs(robot.x-entry[0]), abs(robot.y-entry[1]))
                    robot.distances[id] = (abs(dist))