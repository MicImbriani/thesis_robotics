from .robot import Robot

class LearnRobot(Robot):
    def __init__(self, game_map, startpos=None):
        super().__init__(game_map, startpos)