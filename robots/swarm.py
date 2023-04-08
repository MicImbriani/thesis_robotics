from math import sqrt

from utils.utils import distance

class Swarm:
    def __init__(self, swarm):
        self.robots = swarm
        self.assign_ids()


    def set_formation(self, formation):
        self.formation = formation


    def __getitem__(self, idx: int):
        return [robot for robot in self.robots if robot.id == idx][0]


    def assign_ids(self):
        self.ids = []
        for idx, robot in enumerate(self.robots):
            robot.other_robots = [x for x in self.robots if x is not robot]
            robot.id = idx
            self.ids.append(idx)


    def get_end_mid_point(self, point):
        for robot in self.robots:
            robot.end_mid_point = point


    def update_swarm(self, dt):
        [robot.update(dt) for robot in self.robots]





class LearnSwarm(Swarm):
    def __init__(self, swarm):
        super().__init__(swarm)
        self.base_formation_area = 0.  #value is assigned during q-learning init

    # WORLDS EXCHANGE

    # HARDCODED TO 3 ROBOTS ONLY
    def compute_triangle_area(self, p1, p2, p3):
        l1 = distance(p1, p2)
        l2 = distance(p2, p3)
        l3 = distance(p1, p3)
        s = (l1 + l2 + l3) / 2
        return sqrt(s * (s-l1)*(s-l2)*(s-l3))

    @property
    def formation_disruption(self):
        r1, r2, r3 = [robot.position for robot in self.robots]
        return abs(self.compute_triangle_area(r1, r2, r3) - self.base_formation_area)


    def set_base_formation_area(self):
        r1, r2, r3 = [robot[0] for robot in self.formation]
        self.base_formation_area= self.compute_triangle_area(r1, r2, r3)
