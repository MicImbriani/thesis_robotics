class Trajectory:
    def __init__(self, coords):
        self.start = coords[0]
        self.end = coords[1]

    @property
    def coord(self):
        return (self.start, self.end)



class Formation:
    def __init__(self, name, swarm):
        self.swarm = swarm
        match name:
            case "triangle":    self.formation = self._triangle_formation()
            case "line":        self.formation = self._line_formation()
        self.assign_trajs()
    
    def _triangle_formation(self):
        start = [(200, 100), (250, 100), (225, 150)]
        end = list(map(lambda coords: (coords[0]+500, coords[1]), start))
        return [[x,y] for x,y in zip(start, end)]

    def _line_formation(self):
        start = [(200, 100), (200, 130), (200, 160)]
        end = list(map(lambda coords: (coords[0]+500, coords[1]), start))
        return [[x, y] for x, y in zip(start, end)]

    def assign_trajs(self):
        for robot, formation_coords in zip(self.swarm, self.formation):
            print(formation_coords)
            import time
            # time.sleep(1)
            traj = Trajectory(formation_coords)
            robot.trajectory = traj  # [(start),(end)]
            robot.x, robot.y = traj.start