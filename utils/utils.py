import pygame
from numpy import array
from scipy.spatial.distance import euclidean

def distance(point1, point2):
    return euclidean(point1, point2)

# used for sensors rays only
def ray_distance(point1, point2, dist):
    res = distance(point1, point2)
    return 0 if res >= dist else res


# relative_displacement
def _p_ij_tilda(robot1, robot2):
    return robot1[0]-robot2[0], robot1[1]-robot2[1]

def _beta_ij(robot1, robot2):
    p_ij = _p_ij_tilda(robot1, robot2)
    return norm(p_ij)**2

# partial derivative of gamma_ij (differentiable potential function with 1 minim)
# with respect to beta_ij ()
def _ro_ij(robot1, robot2, K, distance):
    beta = _beta_ij(robot1, robot2)
    beta += 2.2250738585072014e-308
    ro = K * (beta**2 - distance**4) / beta**2
    return ro


# COLORS
def get_color(color):
    match color:
        case "black"    : return (0,0,0)
        case "white"    : return (255,255,255)
        case "green"    : return (0,255,0)
        case "blue"     : return (0,0,255)
        case "red"      : return (255,0,0)
        case "yellow"   : return (255,255,0)




from utils.constants import *

def get_direction_from_heading(heading) -> dict:
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


def get_direction_from_dir(dir):
    match dir:
        case (0,0): return STRAIGHT
        case (0, -1): return UP
        case (1,-1): return UP_RIGHT
        case (1,0): return RIGHT
        case (1,1): return DOWN_RIGHT
        case (0,1): return DOWN
        case (-1,1): return DOWN_LEFT
        case (-1,0): return LEFT
        case (-1,-1): return UP_LEFT

relative_directions = [UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT]
def get_relative_directions(current_dir, new_dir):
    idx = relative_directions.index(current_dir)
    if new_dir == LEFT:
        return relative_directions[idx-2]
    else:
        id_right = idx + 2 if idx+2 <= len(relative_directions) else idx+2-len(relative_directions)
        return relative_directions[id_right]


def get_heading_from_direction(dir):
    match dir['name']:
        case 'STRAIGHT':          return 0
        case 'UP':            return 1.57
        case 'UP_RIGHT':      return 0.785
        case 'RIGHT':         return 0
        case 'DOWN_RIGHT':    return 5.495
        case 'DOWN':          return 4.71
        case 'DOWN_LEFT':     return 3.925
        case 'LEFT':          return 3.14
        case 'UP_LEFT':       return 2.355





# COMPUTING COORDS ALONG TWO POINTS
import numpy as np
def connect(ends):
    d0, d1 = np.abs(np.diff(ends, axis=0))[0]
    if d0 > d1: 
        return np.c_[np.linspace(ends[0, 0], ends[1, 0], d0+1, dtype=np.int32),
                     np.round(np.linspace(ends[0, 1], ends[1, 1], d0+1))
                     .astype(np.int32)]
    else:
        return np.c_[np.round(np.linspace(ends[0, 0], ends[1, 0], d1+1))
                     .astype(np.int32),
                     np.linspace(ends[0, 1], ends[1, 1], d1+1, dtype=np.int32)]

def connect2(ends):
    d0, d1 = np.diff(ends, axis=0)[0]
    if np.abs(d0) > np.abs(d1): 
        return np.c_[np.arange(ends[0, 0], ends[1,0] + np.sign(d0), np.sign(d0), dtype=np.int32),
                     np.arange(ends[0, 1] * np.abs(d0) + np.abs(d0)//2,
                               ends[0, 1] * np.abs(d0) + np.abs(d0)//2 + (np.abs(d0)+1) * d1, d1, dtype=np.int32) // np.abs(d0)]
    else:
        return np.c_[np.arange(ends[0, 0] * np.abs(d1) + np.abs(d1)//2,
                               ends[0, 0] * np.abs(d1) + np.abs(d1)//2 + (np.abs(d1)+1) * d0, d0, dtype=np.int32) // np.abs(d1),
                     np.arange(ends[0, 1], ends[1,1] + np.sign(d1), np.sign(d1), dtype=np.int32)]

def connect_nd(ends):
    d = np.diff(ends, axis=0)[0]
    j = np.argmax(np.abs(d))
    D = d[j]
    aD = np.abs(D)
    return ends[0] + (np.outer(np.arange(aD + 1), d) + (aD//2)) // aD


ends = np.array([[0, 0],
                 [0,-10]])





