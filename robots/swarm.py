class Swarm:
    def __init__(self, swarm):
        self.robots = swarm
        self.assign_ids()

    def assign_ids(self):
        self.ids = []
        for idx, robot in enumerate(self.robots):
            robot.other_robots = [x for x in self.robots if x is not robot]
            robot.id = idx
            self.ids.append(idx)

    def get_state(self):
        return


    def update_swarm(self, dt):
        [robot.update(dt) for robot in self.robots]
