class Swarm:
    def __init__(self, swarm):
        self.robots = swarm
        for robot in self.robots:
            robot.other_robots = [x for x in self.robots if x is not robot]


    def get_state(self):
        return


    def update_swarm(self, dt):
        [robot.update(dt) for robot in self.robots]
