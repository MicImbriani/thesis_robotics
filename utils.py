import numpy as np
import pygame
from constants import *

def distance(point1, point2):
    point1 = np.array(point1)
    point2 = np.array(point2)
    # print(point1, point2)
    return np.linalg.norm(point1-point2)

def ray_distance(point1, point2, dist):
    res = distance(point1, point2)
    # print("res", res)
    return 0 if res >= dist else res

# COLORS
def get_color(color):
    match color:
        case "black"    : return (0,0,0)
        case "white"    : return (255,255,255)
        case "green"    : return (0,255,0)
        case "blue"     : return (0,0,255)
        case "red"      : return (255,0,0)
        case "yellow"   : return (255,255,0)



def check_stop_game():
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    return running



def update_swarm(swarm, dt):
    [robot.update(dt) for robot in swarm]


def get_direction(heading):
    if ((heading == 0)      # RIGHT
        or (0 < heading <= 0.39269908169872414) \
        or (5.890486225480862 < heading <= 6.283185307179586) \
        or (-6.283185307179586 <= heading <= -5.890486225480862) \
            or (-0.39269908169872414 < heading <= 0)):
        return RIGHT
    elif (0.39269908169872414 < heading <= 1.1780972450961724)\
            or (-5.890486225480862 < heading <= -5.105088062083414):
        return UP_RIGHT
    elif (1.1780972450961724 < heading <= 1.9634954084936207)\
            or (-5.105088062083414 < heading <= -4.319689898685966):
        return UP
    elif (1.9634954084936207 < heading <= 2.748893571891069)\
            or (-4.319689898685966 < heading <= -3.5342917352885177):
        return UP_LEFT
    elif (2.748893571891069 < heading <= 3.5342917352885173)\
            or (-3.5342917352885173 < heading <= -2.7488935718910694):
        return LEFT
    elif (3.5342917352885173 < heading <= 4.319689898685966)\
            or (-2.7488935718910694 < heading <= -1.9634954084936207):
        return DOWN_LEFT
    elif (4.319689898685966 < heading <= 5.105088062083414)\
            or (-1.9634954084936207 < heading <= -1.1780972450961724):
        return DOWN
    elif (5.105088062083414 < heading < 5.890486225480862)\
            or (-1.1780972450961724 < heading <= -0.39269908169872414):
        return DOWN_RIGHT
    else:
        raise Exception("NO DIRECTION FOUND FROM HEADING")
