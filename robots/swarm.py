class Swarm:
    def __init__(self, swarm):
        self.robots = swarm
        self.assign_ids()


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

    def get_actions(self):
        return [robot.get_action() for robot in self.swarm]
    
    def take_actions(self):
        for robot in self.swarm:
            
    
    def get_states(self):
        states = []
        for robot in self.robots:
            states.append(robot.get_state())
